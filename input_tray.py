"""
input_tray.py v1.0 — INPUT-SOURCE-LAW: the ONE place a step's exam input files come from.
GAP-2026-11-27-ATTACHMENT-INPUT-LANE (owner decision 2026-11-27).

THE DEFECT THIS CLOSES
  An exam's input files (section_rules.md, blueprint.json, subtopic_manifest.json, ...) reach a
  session by one of two lanes: uploaded to the project's Files section (mounted READ-ONLY at
  /mnt/project) or attached to the trigger in chat (/mnt/user-data/uploads, each name carrying an
  8-hex upload prefix: '3f2fe80c-X_blueprint.json'). Only two inputs (the registry and the stimulus
  profile) were read from both lanes, and even those looked for the EXACT name, which a prefixed
  attachment never has. Every other input was read from /mnt/project alone. bootstrap
  --stage-inputs could repair that only on a surface WITHOUT /mnt/project (it copies attachments
  into the project dir); on the Projects surface the dir is read-only, the copy is impossible, and
  a step whose Files section was full HARD STOPPED on the first input that lived only in chat
  (measured 2026-11-27: TestCreate CSIR_NET_CHEMICALSCIENCES, section_rules.md attached, stop at
  the session start).

THE LAW
  Every step reads its exam inputs from ONE folder, INPUT_DIR (/tmp/fw_inputs), built by ensure():
    1. every regular, non-dot file at the top level of Project Files (/mnt/project);
    2. then every chat attachment (/mnt/user-data/uploads and /mnt/user-data/attachments, walked
       recursively), the 8-hex upload prefix removed. An attachment WINS over a Project Files file
       of the same name (the REGISTRY-SOURCE-LAW rule, applied to every input). The same name
       attached more than once: the newest copy wins (ties broken by path, so the pick never
       depends on the host).
  A .json / .py / .md attachment is checked before it is used (non-empty, UTF-8, parses /
  compiles). A broken attachment is NEVER used and the Project Files copy of that name is NEVER
  used in its place (a silent fall-back would generate from a file the user did not mean). If its
  name belongs to the exam (starts with '<ExamCode>_', or is exam_config.json) ensure() HARD STOPS
  naming it; otherwise it is reported and withheld.
  A Framework_*.md attachment is never placed in the folder: specs come only from GitHub or from
  Project Files via spec_source.py (unchanged).
  ATTACH_VIEW_DIR (/tmp/fw_inputs_attached) holds the valid attachments alone, under their plain
  names — it is lane 1 of paper_pipeline.resolve_registry, which keeps its own both-lane report
  and its run pin (R4).
  require() checks a step's whole list of mandatory inputs at once and names EVERY missing or
  broken file in one HARD STOP, with any near-miss name (a browser download renamed
  'X_registry (1).json') so the operator knows to rename it.

WHAT IT NEVER DOES
  * It never places INPUT_DIR or ATTACH_VIEW_DIR on sys.path — a .py in it is data (the per-exam
    auditor is byte-checked against audit_canonical.py by Step 7, as before), never an import.
  * It never writes to /mnt/project or to the attachment folders.
  * It never decides which spec runs.

COST (measured 2026-11-27): one copy pass, ~1 s for 30 files / 20 MB; a later call in the same
session whose sources did not change copies nothing. The printed report is one line per
attachment plus one summary line.

Stdlib only. Every path is overridable for hermetic tests: FW_INPUT_DIR, FW_INPUT_ATTACH_VIEW,
FW_PROJECT_DIR, FW_UPLOADS_DIR, FW_ATTACH_DIR (the last three are bootstrap.py's own names).
"""
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys

VERSION = '1.0'
GAP_ID = 'GAP-2026-11-27-ATTACHMENT-INPUT-LANE'
LAW = 'INPUT-SOURCE-LAW'

INPUT_DIR = '/tmp/fw_inputs'
ATTACH_VIEW_DIR = '/tmp/fw_inputs_attached'
PROJECT_DIR = '/mnt/project'
UPLOADS_DIR = '/mnt/user-data/uploads'
ATTACHMENTS_DIR = '/mnt/user-data/attachments'
RECORD_NAME = '.input_sources.json'

LANE_ATTACHMENT = 'attachment'
LANE_PROJECT = 'project'

UPLOAD_PREFIX_RE = re.compile(r'^[0-9a-f]{8}-(?=.)')
COPY_SUFFIX_RE = re.compile(r'^(?P<stem>.+?) \(\d+\)(?P<ext>\.[^.]+)?$')


# ── paths (resolved at CALL time, so a harness can redirect them) ────────────────────────
def input_dir():
    return os.environ.get('FW_INPUT_DIR', INPUT_DIR)


def attach_view_dir():
    return os.environ.get('FW_INPUT_ATTACH_VIEW', ATTACH_VIEW_DIR)


def project_dir():
    return os.environ.get('FW_PROJECT_DIR', PROJECT_DIR)


def attach_dirs():
    return (os.environ.get('FW_UPLOADS_DIR', UPLOADS_DIR),
            os.environ.get('FW_ATTACH_DIR', ATTACHMENTS_DIR))


def path(name):
    """The one path a spec or engine opens for the exam input `name`. Self-ensuring: the
    folder is built (or refreshed — cached when nothing changed) first, so a prose-driven call
    never depends on an earlier block having run."""
    build()
    return os.path.join(input_dir(), name)


# ── pure core ─────────────────────────────────────────────────────────────────────────────
def plain_name(basename):
    """An attachment's file name without the 8-hex upload prefix."""
    return UPLOAD_PREFIX_RE.sub('', basename, count=1)


def is_spec(name):
    return name.startswith('Framework_') and name.endswith('.md')


def check_bytes(name, data):
    """None when `data` is usable as the input `name`, else a one-line reason."""
    if not data:
        return 'the file is empty'
    low = name.lower()
    if low.endswith(('.json', '.py', '.md')):
        try:
            text = data.decode('utf-8-sig')
        except UnicodeDecodeError as e:
            return f'not UTF-8 text ({e.reason} at byte {e.start})'
        if not text.strip():
            return 'the file holds only whitespace'
        if low.endswith('.json'):
            try:
                json.loads(text)
            except ValueError as e:
                return f'not valid JSON ({e})'
        elif low.endswith('.py'):
            try:
                compile(text, name, 'exec')
            except SyntaxError as e:
                return f'does not compile (line {e.lineno}: {e.msg})'
    return None


def pick_newest(cands):
    """cands: [(path, size, mtime_ns)] for one plain name. Newest mtime wins; a tie is broken
    by the larger path string — a total order that never depends on listing order."""
    return max(cands, key=lambda c: (c[2], c[0]))


def plan(project, attach):
    """PURE. project: {name: (path, size, mtime_ns)}; attach: {name: [(path, size, mtime_ns)]}.
    Returns {'entries': {name: {'src', 'lane', 'project_src'}}, 'ignored': [name]}."""
    entries, ignored = {}, []
    for name, rec in project.items():
        if is_spec(name):
            continue
        entries[name] = {'src': rec[0], 'lane': LANE_PROJECT, 'project_src': rec[0]}
    for name, cands in attach.items():
        if is_spec(name):
            ignored.append(name)
            continue
        best = pick_newest(cands)
        prj = project.get(name)
        entries[name] = {'src': best[0], 'lane': LANE_ATTACHMENT,
                         'project_src': prj[0] if prj and not is_spec(name) else None}
    return {'entries': entries, 'ignored': sorted(ignored)}


def is_exam_input(name, exam):
    return bool(exam) and (name.startswith(f'{exam}_') or name == 'exam_config.json')


def near_misses(missing, present):
    """{missing name: [present names that are a renamed copy of it]} — a ' (N)' copy suffix or
    a case difference. Never used to pick a file; only to tell the operator what to rename."""
    out = {}
    for want in missing:
        if '*' in want:
            continue
        hits = []
        for have in present:
            if have == want:
                continue
            m = COPY_SUFFIX_RE.match(have)
            base = (m.group('stem') + (m.group('ext') or '')) if m else have
            if base == want or have.lower() == want.lower() or base.lower() == want.lower():
                hits.append(have)
        if hits:
            out[want] = sorted(hits)
    return out


def missing_report(required, present, invalid):
    """PURE. required: names or fnmatch patterns ('X*_blueprint.json'). present: names in the
    folder. invalid: {name: reason}. Returns (missing, broken)."""
    missing, broken = [], []
    for want in required:
        if '*' in want or '?' in want:
            if not any(fnmatch.fnmatchcase(p, want) for p in present):
                bad = sorted(n for n in invalid if fnmatch.fnmatchcase(n, want))
                (broken.extend(bad) if bad else missing.append(want))
        elif want in invalid:
            broken.append(want)
        elif want not in present:
            missing.append(want)
    return missing, sorted(set(broken))


# ── I/O shell ─────────────────────────────────────────────────────────────────────────────
def _sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def scan(project=None, attach=None):
    """Read both lanes from disk. Returns (project, attach) in plan()'s shapes."""
    project = project_dir() if project is None else project
    attach = attach_dirs() if attach is None else attach
    prj = {}
    if os.path.isdir(project):
        for f in sorted(os.listdir(project)):
            p = os.path.join(project, f)
            if f.startswith('.') or not os.path.isfile(p):
                continue
            st = os.stat(p)
            prj[f] = (p, st.st_size, st.st_mtime_ns)
    att = {}
    for d in attach:
        if not d or not os.path.isdir(d):
            continue
        for root, dirs, files in os.walk(d):
            dirs[:] = sorted(x for x in dirs if not x.startswith('.'))
            for f in sorted(files):
                p = os.path.join(root, f)
                name = plain_name(f)
                if name.startswith('.') or not os.path.isfile(p):    # a dot-file stays hidden, prefixed or not
                    continue
                st = os.stat(p)
                att.setdefault(name, []).append((p, st.st_size, st.st_mtime_ns))
    return prj, att


def _signature(prj, att):
    rows = [[LANE_PROJECT, n, *r] for n, r in sorted(prj.items())]
    rows += [[LANE_ATTACHMENT, n, *c] for n, cs in sorted(att.items()) for c in sorted(cs)]
    return hashlib.sha256(json.dumps(rows).encode('utf-8')).hexdigest()


def _place(src, dst):
    """Byte copy through a temp file + os.replace: a reader never sees a half-written file."""
    tmp = f'{dst}.tmp{os.getpid()}'
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)


def _load_record(folder):
    try:
        with open(os.path.join(folder, RECORD_NAME), encoding='utf-8') as fh:
            rec = json.load(fh)
        return rec if isinstance(rec, dict) else None
    except (OSError, ValueError):
        return None


def build(project=None, attach=None, out=None, view=None):
    """Build (or refresh) the input folder. Returns the record dict (also written to
    <out>/.input_sources.json). Copies only when the sources changed. Serialised by an
    exclusive lock, so an orchestrator and a worker building at once never race."""
    out = input_dir() if out is None else out
    view = attach_view_dir() if view is None else view
    import fcntl
    os.makedirs(os.path.dirname(os.path.abspath(out)) or '/', exist_ok=True)
    with open(os.path.abspath(out).rstrip('/') + '.lock', 'a') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            return _build_locked(project, attach, out, view)
        finally:
            fcntl.flock(lk, fcntl.LOCK_UN)


def _build_locked(project, attach, out, view):
    prj, att = scan(project, attach)
    sig = _signature(prj, att)
    rec = _load_record(out)
    if (rec and rec.get('signature') == sig and rec.get('version') == VERSION
            and all(os.path.isfile(os.path.join(out, n)) for n in rec.get('files', {}))
            and all(os.path.isfile(os.path.join(view, n)) for n, v in rec.get('files', {}).items()
                    if v.get('lane') == LANE_ATTACHMENT)):
        rec['cached'] = True
        return rec
    pl = plan(prj, att)
    os.makedirs(out, exist_ok=True)
    os.makedirs(view, exist_ok=True)
    files, invalid = {}, {}
    for name in sorted(pl['entries']):
        e = pl['entries'][name]
        if e['lane'] == LANE_ATTACHMENT:
            try:
                with open(e['src'], 'rb') as fh:
                    reason = check_bytes(name, fh.read())
            except OSError as ex:
                reason = f'could not be read ({type(ex).__name__}: {ex})'
            if reason:
                invalid[name] = {'reason': reason, 'src': e['src'],
                                 'project_copy': bool(e['project_src'])}
                continue
        _place(e['src'], os.path.join(out, name))
        info = {'lane': e['lane'], 'src': e['src'], 'sha256': _sha(os.path.join(out, name))}
        if e['lane'] == LANE_ATTACHMENT:
            _place(e['src'], os.path.join(view, name))
            if e['project_src']:
                info['project'] = ('same' if _sha(e['project_src']) == info['sha256']
                                   else 'differs')
        files[name] = info
    for folder, keep in ((out, set(files) | {RECORD_NAME}),
                         (view, {n for n, v in files.items() if v['lane'] == LANE_ATTACHMENT})):
        for f in os.listdir(folder):
            p = os.path.join(folder, f)
            if f not in keep and os.path.isfile(p):
                os.unlink(p)
    rec = {'law': LAW, 'version': VERSION, 'signature': sig, 'files': files,
           'invalid': invalid, 'ignored_specs': pl['ignored'], 'cached': False}
    with open(os.path.join(out, RECORD_NAME), 'w', encoding='utf-8') as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    return rec


def report_lines(rec):
    """The operator-facing lines a spec PRINTS (one per attachment + a summary)."""
    files = rec.get('files', {})
    n_att = sum(1 for v in files.values() if v['lane'] == LANE_ATTACHMENT)
    lines = [f'INPUT SOURCES ({LAW}): {len(files)} file(s) in {input_dir()} — '
             f'{n_att} from chat attachments, {len(files) - n_att} from Project Files'
             + (' (unchanged since the last check)' if rec.get('cached') else '') + '.']
    for name in sorted(files):
        v = files[name]
        if v['lane'] != LANE_ATTACHMENT:
            continue
        note = {'same': ' (Project Files holds an identical copy)',
                'differs': ' (Project Files holds a DIFFERENT copy — the attachment is used)'
                }.get(v.get('project'), '')
        lines.append(f'  ATTACHMENT  {name}{note}')
    for name in sorted(rec.get('invalid', {})):
        v = rec['invalid'][name]
        lines.append(f'  BROKEN      {name} — {v["reason"]}; NOT used'
                     + (' (the Project Files copy is not used in its place)'
                        if v.get('project_copy') else ''))
    for name in rec.get('ignored_specs', []):
        lines.append(f'  IGNORED     {name} — an attached spec is never loaded (specs come from '
                     f'GitHub, or from Project Files)')
    return lines


def ensure(exam=None, quiet=False, **kw):
    """Build/refresh the folder, print the report, and HARD STOP on a broken attachment that
    belongs to `exam`. Safe to call any number of times (cached when nothing changed)."""
    rec = build(**kw)
    if not quiet:
        lines = report_lines(rec)
        for line in (lines[:1] if rec.get('cached') else lines):
            print(line)
    bad = sorted(n for n in rec.get('invalid', {}) if is_exam_input(n, exam))
    if bad:
        raise SystemExit(
            f'HARD STOP [HS:INPUT] ({LAW}): the attached file(s) '
            + '; '.join(f'{n} ({rec["invalid"][n]["reason"]})' for n in bad)
            + ' cannot be used. A broken attachment is never replaced by the Project Files copy. '
              'Attach a correct copy (or, in a new chat, leave it out to use the Project Files '
              'copy), then retry.')
    return rec


_BROKEN_SHOWN = set()


def lanes(legacy):
    """For an ENGINE's search order: the input folder FIRST (refreshed — cached when nothing
    changed), then the engine's own legacy lanes unchanged, as a safety net. Never raises: if
    the folder cannot be built the legacy lanes are returned as before. A broken attachment is
    printed once per process even here (never silent)."""
    legacy = tuple(legacy)
    try:
        rec = build()
    except Exception:                                    # noqa: BLE001 — degrade to legacy
        return legacy
    for name in sorted(rec.get('invalid', {})):
        if name not in _BROKEN_SHOWN:
            _BROKEN_SHOWN.add(name)
            print(f'INPUT SOURCES ({LAW}): BROKEN attachment {name} — '
                  f'{rec["invalid"][name]["reason"]}; NOT used')
    first = input_dir() + ('/' if legacy and str(legacy[0]).endswith('/') else '')
    return (first,) + tuple(d for d in legacy if d.rstrip('/') != input_dir().rstrip('/'))


def require(exam, names, step='this step', rec=None):
    """HARD STOP listing EVERY missing or broken mandatory input at once. `names` may hold
    fnmatch patterns ('X*_blueprint.json'). Returns the record when all are present."""
    rec = rec if rec is not None else build()
    out = input_dir()
    present = sorted(f for f in (os.listdir(out) if os.path.isdir(out) else [])
                     if not f.startswith('.'))
    missing, broken = missing_report(names, present, rec.get('invalid', {}))
    if not missing and not broken:
        return rec
    parts = []
    if missing:
        parts.append(f'{len(missing)} required input file(s) not found in chat attachments or '
                     f'Project Files: ' + ', '.join(missing) + '.')
    if broken:
        parts.append('attached but broken (never used, and the Project Files copy is not used '
                     'in its place): ' + ', '.join(
                         f'{n} ({rec["invalid"][n]["reason"]})' for n in broken) + '.')
    near = near_misses(missing, present)
    if near:
        parts.append('Renamed copies seen — rename them to the exact name: ' + '; '.join(
            f"'{h}' -> '{w}'" for w, hs in sorted(near.items()) for h in hs) + '.')
    tag = f' [{exam}]' if exam else ''
    raise SystemExit(f'HARD STOP [HS:INPUT] ({LAW}) — {step}{tag}: ' + ' '.join(parts)
                     + ' Attach each file to the trigger in chat OR upload it to the project '
                       'Files section (either works; an attachment wins over Files), then retry.')


# ── self-test ─────────────────────────────────────────────────────────────────────────────
def self_test():
    import tempfile
    results = []

    def ck(name, cond):
        results.append((name, bool(cond)))

    # pure core
    ck('prefix-stripped', plain_name('3f2fe80c-EX_registry.json') == 'EX_registry.json')
    ck('prefix-only-8-hex', plain_name('3F2FE80C-EX_a.json') == '3F2FE80C-EX_a.json'
       and plain_name('3f2fe80-EX_a.json') == '3f2fe80-EX_a.json'
       and plain_name('EX_a.json') == 'EX_a.json')
    ck('prefix-never-empties', plain_name('3f2fe80c-') == '3f2fe80c-')
    ck('check-empty', check_bytes('a.json', b'') is not None)
    ck('check-bad-json', check_bytes('a.json', b'{"x":') is not None)
    ck('check-good-json', check_bytes('a.json', b'{"x": 1}') is None)
    ck('check-bom-json', check_bytes('a.json', b'\xef\xbb\xbf{"x": 1}') is None)
    ck('check-bad-py', check_bytes('a.py', b'def (:\n') is not None)
    ck('check-good-py', check_bytes('a.py', b'x = 1\n') is None)
    ck('check-bad-utf8-md', check_bytes('a.md', b'\xff\xfe\x00') is not None)
    ck('check-blank-md', check_bytes('a.md', b'  \n\n') is not None)
    ck('check-binary-docx-unchecked', check_bytes('a.docx', b'PK\x03\x04') is None)
    ck('newest-wins', pick_newest([('/u/a', 1, 5), ('/u/b', 1, 9)])[0] == '/u/b')
    ck('newest-tie-host-independent',
       pick_newest([('/u/a', 1, 5), ('/u/z', 1, 5)])[0] == '/u/z'
       and pick_newest([('/u/z', 1, 5), ('/u/a', 1, 5)])[0] == '/u/z')
    p = plan({'EX_a.json': ('/p/EX_a.json', 1, 1), 'EX_b.md': ('/p/EX_b.md', 1, 1),
              'Framework_X.md': ('/p/Framework_X.md', 1, 1)},
             {'EX_a.json': [('/u/1-EX_a.json', 1, 2)], 'Framework_Y.md': [('/u/Framework_Y.md', 1, 2)]})
    ck('attachment-wins', p['entries']['EX_a.json']['lane'] == LANE_ATTACHMENT
       and p['entries']['EX_a.json']['project_src'] == '/p/EX_a.json')
    ck('project-kept', p['entries']['EX_b.md']['lane'] == LANE_PROJECT)
    ck('specs-never-inputs', 'Framework_X.md' not in p['entries']
       and 'Framework_Y.md' not in p['entries'] and p['ignored'] == ['Framework_Y.md'])
    ck('exam-input', is_exam_input('EX_a.json', 'EX') and is_exam_input('exam_config.json', 'EX')
       and not is_exam_input('EXB_a.json', 'EX') and not is_exam_input('EX_a.json', None))
    ck('near-miss-copy-suffix', near_misses(['EX_registry.json'], ['EX_registry (1).json'])
       == {'EX_registry.json': ['EX_registry (1).json']})
    ck('near-miss-case', near_misses(['EX_a.json'], ['ex_a.json']) == {'EX_a.json': ['ex_a.json']})
    ck('near-miss-none', near_misses(['EX_a.json'], ['EX_b.json']) == {})
    m, b = missing_report(['EX_a.json', 'EX*_blueprint.json', 'EX_c.json', 'EX_d.json'],
                          ['EX_a.json'], {'EX_c.json': {'reason': 'r'}})
    ck('missing-all-at-once', m == ['EX*_blueprint.json', 'EX_d.json'] and b == ['EX_c.json'])
    m2, _ = missing_report(['EX*_blueprint.json'], ['EX_SCOPE_blueprint.json'], {})
    ck('pattern-satisfied', m2 == [])
    m3, b3 = missing_report(['EX*_blueprint.json'], [], {'EX_blueprint.json': {'reason': 'r'}})
    ck('pattern-broken-not-missing', m3 == [] and b3 == ['EX_blueprint.json'])

    # I/O shell, hermetic
    with tempfile.TemporaryDirectory() as td:
        prj, up, att, out, view = (os.path.join(td, x) for x in ('p', 'u', 'a', 'o', 'v'))
        for d in (prj, up):
            os.makedirs(d)

        def w(p_, data, mt):
            os.makedirs(os.path.dirname(p_), exist_ok=True)
            with open(p_, 'wb') as fh:
                fh.write(data)
            os.utime(p_, ns=(mt, mt))
        w(os.path.join(prj, 'EX_section_rules.md'), b'# rules\n', 10)
        w(os.path.join(prj, 'EX_registry.json'), b'{"exam_code": "EX", "v": 1}', 10)
        w(os.path.join(prj, 'EX_blueprint.json'), b'{"exam_code": "EX"}', 10)
        w(os.path.join(prj, '.in_memory'), b'', 10)
        w(os.path.join(prj, 'Framework_MockDeliver.md'), b'# spec\n', 10)
        w(os.path.join(up, '3f2fe80c-EX_registry.json'), b'{"exam_code": "EX", "v": 2}', 20)
        w(os.path.join(up, 'aaaaaaaa-EX_blueprint.json'), b'{"exam_code": "EX"}', 20)
        w(os.path.join(up, '11111111-EX_subtopic_manifest.json'), b'{"s": 1}', 20)
        w(os.path.join(up, '22222222-EX_subtopic_manifest.json'), b'{"s": 2}', 30)
        w(os.path.join(up, 'cccccccc-Framework_MockTestCreate.md'), b'# spec\n', 20)
        w(os.path.join(up, '.DS_Store'), b'x', 20)
        w(os.path.join(up, '99999999-.hidden.json'), b'{}', 20)
        w(os.path.join(att, 'sess', 'dddddddd-EX_style_profile.json'), b'{"st": 1}', 20)
        kw = dict(project=prj, attach=(up, att), out=out, view=view)
        rec = build(**kw)
        f = rec['files']
        ck('io-prefixed-attachment-seen', 'EX_subtopic_manifest.json' in f
           and f['EX_subtopic_manifest.json']['lane'] == LANE_ATTACHMENT)
        ck('io-newest-duplicate-wins', open(os.path.join(out, 'EX_subtopic_manifest.json'),
                                            'rb').read() == b'{"s": 2}')
        ck('io-attachment-wins-bytes', json.load(open(os.path.join(out, 'EX_registry.json')))['v'] == 2)
        ck('io-differs-reported', f['EX_registry.json'].get('project') == 'differs')
        ck('io-same-reported', f['EX_blueprint.json'].get('project') == 'same')
        ck('io-project-only-kept', f['EX_section_rules.md']['lane'] == LANE_PROJECT)
        ck('io-nested-attachments-dir', 'EX_style_profile.json' in f)
        ck('io-dotfiles-skipped', '.in_memory' not in f and '.DS_Store' not in f and '.hidden.json' not in f
           and not os.path.exists(os.path.join(view, '.DS_Store')))
        ck('io-specs-skipped', 'Framework_MockDeliver.md' not in f
           and not os.path.exists(os.path.join(out, 'Framework_MockTestCreate.md'))
           and rec['ignored_specs'] == ['Framework_MockTestCreate.md'])
        ck('io-view-attachments-only', sorted(os.listdir(view)) == sorted(
            ['EX_registry.json', 'EX_blueprint.json', 'EX_subtopic_manifest.json',
             'EX_style_profile.json']))
        ck('io-report-lines', any('DIFFERENT copy' in ln for ln in report_lines(rec))
           and report_lines(rec)[0].startswith('INPUT SOURCES'))
        rec2 = build(**kw)
        ck('io-cached-second-call', rec2.get('cached') is True)
        # a broken attachment: withheld, project copy NOT substituted, HARD STOP for exam inputs
        w(os.path.join(up, 'eeeeeeee-EX_section_rules.md'), b'', 40)
        rec3 = build(**kw)
        ck('io-rebuilt-on-change', rec3.get('cached') is False)
        ck('io-broken-withheld', 'EX_section_rules.md' in rec3['invalid']
           and not os.path.exists(os.path.join(out, 'EX_section_rules.md')))
        stopped = False
        try:
            ensure(exam='EX', quiet=True, **kw)
        except SystemExit as e:
            stopped = 'EX_section_rules.md' in str(e) and 'HARD STOP' in str(e)
        ck('io-broken-exam-input-stops', stopped)
        ok_other = True
        try:
            ensure(exam='OTHER', quiet=True, **kw)
        except SystemExit:
            ok_other = False
        ck('io-broken-foreign-file-no-stop', ok_other)
        os.unlink(os.path.join(up, 'eeeeeeee-EX_section_rules.md'))
        rec4 = build(**kw)
        ck('io-recovered-after-removal', rec4['files'].get('EX_section_rules.md', {}).get('lane')
           == LANE_PROJECT and not rec4['invalid'])
        # require(): every missing name at once + near-miss
        w(os.path.join(up, 'ffffffff-EX_exemplar_bank (1).json'), b'{}', 50)
        rec5 = build(**kw)
        old = os.environ.get('FW_INPUT_DIR')
        os.environ['FW_INPUT_DIR'] = out
        try:
            msg = ''
            try:
                require('EX', ['EX_section_rules.md', 'EX_exemplar_bank.json',
                               'EX_stimulus_profile.json', 'EX*_blueprint.json'], 'TestCreate', rec5)
            except SystemExit as e:
                msg = str(e)
            ck('require-lists-all-missing', 'EX_exemplar_bank.json' in msg
               and 'EX_stimulus_profile.json' in msg and '2 required' in msg)
            ck('require-near-miss', "'EX_exemplar_bank (1).json' -> 'EX_exemplar_bank.json'" in msg)
            msg2 = ''
            try:
                require('', ['EX_none.json'], 'TestDeliver', rec5)
            except SystemExit as e:
                msg2 = str(e)
            ck('require-no-exam-no-bracket', 'TestDeliver:' in msg2 and '[]' not in msg2)
            ck('require-passes-when-present',
               require('EX', ['EX_section_rules.md', 'EX*_blueprint.json'], 'T', rec5) is rec5)
        finally:
            if old is None:
                os.environ.pop('FW_INPUT_DIR', None)
            else:
                os.environ['FW_INPUT_DIR'] = old
        # a file that vanished from both lanes leaves the folder
        os.unlink(os.path.join(prj, 'EX_section_rules.md'))
        rec6 = build(**kw)
        ck('io-stale-removed', 'EX_section_rules.md' not in rec6['files']
           and not os.path.exists(os.path.join(out, 'EX_section_rules.md')))
        # no project dir at all (cloud surface) still builds from attachments
        rec7 = build(project=os.path.join(td, 'absent'), attach=(up,), out=out, view=view)
        ck('io-no-project-dir', rec7['files'].get('EX_registry.json', {}).get('lane')
           == LANE_ATTACHMENT and 'EX_blueprint.json' in rec7['files'])
        # lanes(): input folder first, legacy kept, trailing-slash style preserved
        old_env = {k: os.environ.get(k) for k in ('FW_INPUT_DIR', 'FW_INPUT_ATTACH_VIEW',
                                                   'FW_PROJECT_DIR', 'FW_UPLOADS_DIR', 'FW_ATTACH_DIR')}
        os.environ.update({'FW_INPUT_DIR': out, 'FW_INPUT_ATTACH_VIEW': view, 'FW_PROJECT_DIR': prj,
                           'FW_UPLOADS_DIR': up, 'FW_ATTACH_DIR': att})
        try:
            ln = lanes(('/mnt/project/', '/mnt/user-data/uploads/'))
            ck('lanes-folder-first', ln == (out + '/', '/mnt/project/', '/mnt/user-data/uploads/'))
            ln2 = lanes(('/mnt/user-data/uploads', '/mnt/project'))
            ck('lanes-no-slash-style', ln2[0] == out and ln2[1:] == ('/mnt/user-data/uploads', '/mnt/project'))
            ck('lanes-built-folder', os.path.isfile(os.path.join(out, 'EX_registry.json')))
        finally:
            for k, v in old_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        # never on sys.path
        ck('never-on-sys-path', out not in sys.path and view not in sys.path
           and INPUT_DIR not in sys.path)

    passed = sum(1 for _, ok in results if ok)
    for name, ok in results:
        if not ok:
            print(f'  FAIL  {name}')
    print(f'SELF-TEST: {passed}/{len(results)} PASS')
    return passed == len(results)


def main(argv):
    if '--self-test' in argv:
        return 0 if self_test() else 1
    if '--build' in argv:
        exam = argv[argv.index('--exam') + 1] if '--exam' in argv else None
        ensure(exam=exam)
        return 0
    print('input_tray.py — INPUT-SOURCE-LAW input folder. Run with --build [--exam CODE] or '
          '--self-test.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
