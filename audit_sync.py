"""audit_sync.py — CROSS-STEP SYNCHRONISATION AUDIT.
Does not test behaviour; tests whether the 11 steps AGREE with each other."""
import ast, json, os, re, sys
from collections import defaultdict

# GAP-2026-08-16-AUDITOR-FENCE-BLINDNESS: dedent each fence before it is
# parsed. MEASURED 2026-08-16: this extractor yielded 147 blocks across five
# specs and 61 of them failed ast.parse purely on uniform leading whitespace,
# so 41% of the python it appeared to audit was silently discarded.
# textwrap.dedent strips only the COMMON prefix and adds/removes no line, so
# nested code is untouched and every line number stays valid.
def blocks(t):
    """Return the dedented source of every ```python fence.

    GAP-2026-08-16-AUDITOR-FENCE-BLINDNESS. The dedent is the fix. A fence whose ```
    marker and body are BOTH indented yields uniformly-indented source, which
    ast.parse rejects as "unexpected indent", so the caller's try/except discarded it
    in silence. MEASURED across five specs: 61 of 147 blocks — 41% of the python this
    auditor appeared to be checking. textwrap.dedent strips only the COMMON prefix and
    adds or removes no line, so nested code is unaffected and every line number stays
    valid. Verified over all 259 fences in the corpus: nothing that parsed before
    stopped parsing, and no fence changed line count.

    THE REGEX IS GONE (2026-08-20). The non-greedy `(.*?)` ended the capture at the
    FIRST ``` in the body, so a fence containing a triple backtick inside a docstring
    was cut mid-string. That truncated Framework_MockTestAnalyse.md's S8-1 batch-loop
    acquisition fence — the whole Drive transport contract — into something that did
    not parse, so the caller's try/except discarded it and this auditor scanned code it
    had never read. Same fix, same release and same reasoning as audit_deep.py; see
    XSPEC_DIVERGENCE_BASELINE.json for the exemption mechanism that unblocked it there.
    Measured on the deployed corpus: regex 261 of 264 fences parse, line scanner
    263 of 263.
    """
    import textwrap
    out, cur = [], None
    for line in t.split('\n'):
        stripped = line.strip()
        if cur is None:
            if stripped == '```python':
                cur = []
            continue
        if stripped == '```':
            out.append(textwrap.dedent('\n'.join(cur)))
            cur = None
        else:
            cur.append(line)
    return out

def _self_test():
    """GAP-2026-08-14-AUDITOR-SELFTESTS. Script-style auditor, so fixtures run
    it as a SUBPROCESS against a mutated corpus copy and assert each check
    class still fires. Dispatched before the corpus loads."""
    import shutil, subprocess, tempfile
    passed, fails = 0, []
    here = os.path.dirname(os.path.abspath(__file__)) or '.'

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def run_in(root, env=None):
        _env = dict(os.environ, **env) if env else None
        r = subprocess.run([sys.executable, os.path.join(root, 'audit_sync.py')],
                           cwd=root, capture_output=True, text=True, env=_env)
        return r.returncode, r.stdout + r.stderr

    def _tracked_nonspec():
        """Every non-.md/.py artefact gen_manifest tracks, plus the release files.

        Read from gen_manifest itself so the two can never disagree. Falls back to a
        literal set only if gen_manifest is unimportable, which would be a broken
        checkout rather than a drift.
        """
        base = {'routes.json', 'MANIFEST.json', 'VERSION', 'CHANGELOG.md'}
        try:
            import importlib
            gm = importlib.import_module('gen_manifest')
            base |= set(getattr(gm, 'TRACKED_JSON', []))
            base |= set(getattr(gm, 'TRACKED_DOC', []))
        except Exception:
            base |= {'SPEC_MANIFEST.json', 'SPEC_SECTIONS.json',
                     'MUTATION_BUDGETS.json', 'LAW_REGISTRY.json', 'SPEC_HISTORY.md'}
        base.add('SPEC_MANIFEST.json')      # built by build_spec_manifest, not gen_manifest
        return base

    def mutated(mutate=None, env=None):
        d = tempfile.mkdtemp()
        for f in os.listdir(here):
            # SPEC_MANIFEST.json joins this list for DOC-COUNT (2026.08.15.7):
            # a fixture corpus missing it cannot verify CLAUDE.md's declared counts,
            # so the clean-copy baseline would fail for a reason that is not a defect.
            # SPEC_SECTIONS.json and MUTATION_BUDGETS.json join it for the SAME reason
            # (2026.08.15.11): every tracked non-.md/.py artefact must be copied, or
            # DOC-COUNT compares CLAUDE.md's declared total against a fixture corpus
            # that is short by exactly the files this list forgot. The recurrence is
            # the point — the list is hand-maintained and has now drifted twice, so
            # anything added to gen_manifest.TRACKED_JSON must be added here too.
            # DERIVED FROM gen_manifest, NEVER HAND-LISTED (2026.08.15.14). This
            # list drifted three times in six releases — SPEC_MANIFEST.json,
            # then SPEC_SECTIONS.json + MUTATION_BUDGETS.json, then SPEC_HISTORY.md
            # — and each time the symptom was identical: DOC-COUNT compared
            # CLAUDE.md's declared total against a fixture corpus short by exactly
            # the files this list forgot. Correcting the instance and not the class
            # is the failure the LAW-PROPAGATION LAW exists to remove, so the class
            # is removed here: whatever gen_manifest.py tracks, the fixture copies.
            if f.endswith(('.md', '.py')) or f in _tracked_nonspec():
                shutil.copy(os.path.join(here, f), os.path.join(d, f))
        if mutate:
            mutate(d)
        rc, out = run_in(d, env=env)
        shutil.rmtree(d, ignore_errors=True)
        return rc, out

    def append(root, fname, text):
        with open(os.path.join(root, fname), 'a', encoding='utf-8') as f:
            f.write(text)

    rc, out = mutated()
    check("clean corpus copy passes", rc == 0)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nimport blueprint_core as bc\nx = bc.no_such_fn_selftest(1)\n```\n"))
    check("ENGINE-API fires on a call into an API that does not exist",
          rc == 1 and 'ENGINE-API' in out and 'no_such_fn_selftest' in out)

    def relsync(r):
        open(os.path.join(r, 'VERSION'), 'w', encoding='utf-8').write('9999.99.99.9\n')
    rc, out = mutated(relsync)
    check("REL-SYNC fires when VERSION and CHANGELOG top entry disagree",
          rc == 1 and 'REL-SYNC' in out)

    def badroute(r):
        p = os.path.join(r, 'routes.json')
        routes = json.load(open(p, encoding='utf-8'))
        routes['PYQSort'] = routes['PYQSort'] + ['no_such_file_selftest.py']
        json.dump(routes, open(p, 'w', encoding='utf-8'))
    rc, out = mutated(badroute)
    check("ROUTE-MISSING fires on a routed file that does not exist",
          rc == 1 and 'ROUTE-MISSING' in out and 'no_such_file_selftest' in out)

    def chainbreak(r):
        p = os.path.join(r, 'Framework_MockDeliver.md')
        s = open(p, encoding='utf-8').read().replace('_Final.docx', '_FinalX.docx')
        open(p, 'w', encoding='utf-8').write(s)
    rc, out = mutated(chainbreak)
    check("FILENAME-CHAIN fires when a step stops naming its output suffix",
          rc == 1 and 'FILENAME-CHAIN' in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\nSee Framework_Blueprint v99.99 for the schedule.\n"))
    check("VERSION-XREF fires on a forward reference to a version that "
          "does not exist", rc == 1 and 'VERSION-XREF' in out)

    # ── GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION (P7) ─────────────────────
    def drop_from_governs(r):
        pth = os.path.join(r, 'LAW_REGISTRY.json')
        reg = json.load(open(pth, encoding='utf-8'))
        law = reg['laws']['EXECUTION-BOUNDARY-LAW']
        law['governs'] = [g for g in law['governs'] if g != 'Framework_PYQCount.md']
        json.dump(reg, open(pth, 'w', encoding='utf-8'), indent=2)
    rc, out = mutated(drop_from_governs)
    check("LAW-COVERAGE fires when a spec performs a governed operation but is "
          "absent from the registry",
          rc == 1 and 'LAW-COVERAGE' in out and 'Framework_PYQCount.md' in out)

    def break_the_law(r):
        pth = os.path.join(r, 'Framework_PYQCount.md')
        s = open(pth, encoding='utf-8').read().replace(
            'return corpus_io.fetch_drive_docx(resolver, paper, work_dir)',
            'return corpus_io.fetch_drive_docx(gdrive_download_file_selftest, '
            'paper, work_dir)')
        open(pth, 'w', encoding='utf-8').write(s)
    rc, out = mutated(break_the_law)
    check("LAW-VERIFY fires when a governed spec stops satisfying its verifier",
          rc == 1 and 'LAW-VERIFY' in out)

    rc, out = mutated(lambda r: os.remove(os.path.join(r, 'LAW_REGISTRY.json')))
    check("LAW-REGISTRY fires when the registry is missing",
          rc == 1 and 'LAW-REGISTRY' in out)

    def _bend_count(r):
        pth = os.path.join(r, 'CLAUDE.md')
        t = open(pth, encoding='utf-8').read()
        t = re.sub(r'(routes\.json triggers\s*:\s*)\d+', r'\g<1>999', t)
        open(pth, 'w', encoding='utf-8').write(t)
    rc, out = mutated(_bend_count)
    check("DOC-COUNT fires when a declared count drifts from the files on disk",
          rc == 1 and 'DOC-COUNT' in out and '999' in out)

    def _drop_count_line(r):
        pth = os.path.join(r, 'CLAUDE.md')
        t = open(pth, encoding='utf-8').read()
        t = re.sub(r'^\s*MANIFEST\.json files\s*:\s*\d+\s*$', '', t, flags=re.M)
        open(pth, 'w', encoding='utf-8').write(t)
    rc, out = mutated(_drop_count_line)
    check("DOC-COUNT fires when a required count line is missing entirely",
          rc == 1 and 'DOC-COUNT' in out)

    def _reintroduce_idiom(r):
        with open(os.path.join(r, 'CLAUDE.md'), 'a', encoding='utf-8') as f:
            f.write('\nThe workbench baseline is currently 51 files, including tooling.\n')
    rc, out = mutated(_reintroduce_idiom)
    check("DOC-COUNT-IDIOM fires when a live count is hand-written back into prose",
          rc == 1 and 'DOC-COUNT-IDIOM' in out)

    # ══ B12 (2026-08-21) — THE THIRTEEN UNMEASURED EMISSIONS ═════════════════
    # The first FULL mutation measurement of this auditor (28 emissions; the prior
    # record was 9, from 2026.08.15.13) found 13 survivors — near half the gate was
    # unproven. Six of them shared one cause: every SKILL.md-dependent check read the
    # file from a session mount that exists on no CI runner, so those branches had
    # never executed in the environment that gates the build. The fixtures below give
    # every previously-unproven emission a mutant-killer. Each mutates a corpus COPY
    # and asserts the finding fires — the same mutate-and-expect-red pattern as the
    # rest of this suite.

    def replace(root, fname, old, new):
        q = os.path.join(root, fname)
        t = open(q, encoding='utf-8').read()
        assert old in t, f'fixture stale: {old[:40]!r} not in {fname}'
        open(q, 'w', encoding='utf-8').write(t.replace(old, new))

    def remove(root, fname):
        os.remove(os.path.join(root, fname))

    # L305 — SKILL-INVENTORY, routed-engine count.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md',
        'All 17 routed engine scripts', 'All 99 routed engine scripts'))
    check("SKILL-INVENTORY fires on a wrong routed-engine count",
          rc == 1 and 'SKILL-INVENTORY' in out and '99' in out)

    # L307 — SKILL-INVENTORY, tracked-but-never-routed count. This exact claim WAS
    # stale on the live corpus (said 3, reality 6) the day the check was revived —
    # proof the parity matters, preserved here as the fixture's shape.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md',
        'plus the 6 tracked-but-never-routed', 'plus the 2 tracked-but-never-routed'))
    check("SKILL-INVENTORY fires on a wrong tracked-not-routed count",
          rc == 1 and 'SKILL-INVENTORY' in out and 'tracked-but' in out)

    # ...and the re-point tripwire: reword the inventory line entirely and the check
    # must SAY it can no longer verify, not silently match nothing. That silent
    # no-match is exactly how the previous regex died.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md',
        'All 17 routed engine scripts, plus the 6 tracked-but-never-routed',
        'Seventeen engines ride along, and some other scripts too'))
    check("SKILL-INVENTORY fires when the inventory line is reworded away",
          rc == 1 and 'no longer carries' in out)

    # L343 — INFO when VERSION/CHANGELOG is unreadable. An INFO is still an emission:
    # a release-sync check that skips SILENTLY is the ENV-SKEW shape.
    rc, out = mutated(lambda r: remove(r, 'VERSION'))
    check("INFO fires when VERSION is unreadable (release sync skipped LOUDLY)",
          'release sync not checked' in out)

    # L350 — TRIGGER-SYNC, forward: a routed trigger SKILL.md never mentions.
    rc, out = mutated(lambda r: replace(r, 'SKILL.md', 'PYQCompress', 'PYQSquash'))
    check("TRIGGER-SYNC fires on a routed trigger missing from SKILL.md",
          rc == 1 and "trigger 'PYQCompress' not mentioned" in out)

    # L353 — TRIGGER-SYNC, reverse: SKILL.md naming a trigger that routes nowhere.
    # (PYQSquash from the same mutation matches the trigger-shaped regex.)
    check("TRIGGER-SYNC fires on a SKILL.md trigger routes.json lacks",
          "'PYQSquash' but routes.json has no such trigger" in out)

    # L355 — the not-readable INFO. With the B12 loader this branch means the repo
    # carries NO copy at all — which must be said, not skipped.
    _repo_only = {'AUDIT_SYNC_SKILL_PATHS':
                  os.pathsep.join(('SKILL.md', 'mocktestframework_SKILL.md'))}
    rc, out = mutated(lambda r: (remove(r, 'SKILL.md'),
                                 remove(r, 'mocktestframework_SKILL.md')),
                      env=_repo_only)
    check("INFO fires when no SKILL.md copy exists anywhere",
          'SKILL.md not readable' in out)

    # Watch the watcher: prove the override actually CONTROLS the search surface —
    # on a CLEAN copy (repo SKILL.md present), a search list naming only a file
    # that does not exist must produce the same INFO. If this fixture goes green
    # with the env plumbing removed, the loader has stopped honouring the
    # injection and the fixture above is back to being environment-dependent.
    rc, out = mutated(env={'AUDIT_SYNC_SKILL_PATHS': 'no_such_skill_selftest.md'})
    check("SKILL search-surface injection is honoured (override yields the INFO)",
          'SKILL.md not readable' in out)

    # L376 — ERA-SYNC: nobody writes pattern_eras. Neutralise the writer's mention.
    # (The producer string now lives in Framework_Blueprint.md — the Step 5 writer
    # moved into analyse_engine.py at Wave 2 Part C, so the spec-side mention that
    # keeps this check satisfied is the Blueprint consumer contract.)
    rc, out = mutated(lambda r: replace(r, 'Framework_Blueprint.md',
        'pattern_eras', 'zz_pattern_eras_gone'))
    check("ERA-SYNC fires when no spec writes manifest['pattern_eras']",
          rc == 1 and "no spec writes manifest['pattern_eras']" in out)

    # L379 — ERA-SYNC: frequency_scope used with no --frequency-scope flag declared.
    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        '\nThis step also honours frequency_scope when present.\n'))
    check("ERA-SYNC fires on frequency_scope without a declared trigger flag",
          rc == 1 and 'declares no --frequency-scope' in out)

    # L382 — ERA-SYNC: OUT_OF_PATTERN not sourced from the engine.
    # PYQSort already sources bc.OUT_OF_PATTERN, so a mutation there cannot trip the
    # per-file test — measured while writing this fixture. PYQApprove carries neither
    # spelling, so it isolates exactly the condition.
    rc, out = mutated(lambda r: append(r, 'Framework_PYQApprove.md',
        '\nRows tagged OUT_OF_PATTERN are excluded here.\n'))
    check("ERA-SYNC fires on OUT_OF_PATTERN not sourced from bc",
          rc == 1 and 'without sourcing it from the engine' in out)

    # L395 — BP-SCHEMA: a reader consuming a blueprint field the writer never documents.
    rc, out = mutated(lambda r: append(r, 'Framework_MockTestCreate.md',
        "\n```python\nzz = bp['zz_phantom_field']\n```\n"))
    check("BP-SCHEMA fires on an undocumented blueprint field read",
          rc == 1 and 'zz_phantom_field' in out)

    # L432 — LAW-REGISTRY: the registry exists but is not JSON. Distinct from the
    # already-proven missing-file emission: corruption must not read as absence.
    rc, out = mutated(lambda r: open(os.path.join(r, 'LAW_REGISTRY.json'), 'w',
                                     encoding='utf-8').write('{not json'))
    check("LAW-REGISTRY fires on a corrupt registry file",
          rc == 1 and 'not valid JSON' in out)

    # L498 — LAW-VERIFY: a governed spec that fails its declared verifier. The
    # mutation plants a C10 violation (a partition downstream of a CLASS T
    # acquisition, no consumed=) in a spec EXECUTION-BOUNDARY/SESSION-BUDGET governs,
    # then requires the finding to be relayed AS a LAW-VERIFY line — the whole point
    # of the registry is that the law's verdict surfaces here, not only in the
    # verifier's own run.
    rc, out = mutated(lambda r: append(r, 'Framework_PYQCount.md',
        '\nA2. CHANNEL PROBE — download exactly ONE paper.\n\n'
        '```python\npart = bc.partition_by_transport(papers, channel=channel)\n```\n'))
    # The DETAIL is asserted, not just the category. LAW-VERIFY has two emissions:
    # the per-finding relay (which carries the verifier's own [C10] line) and a
    # catch-all fallback ("audit_callgraph exited 1"). A fixture that only asks for
    # the category passes with the relay deleted, because the fallback still speaks —
    # measured: that mutant survived the first B12 run at 28/29. The [C10] tag exists
    # only in the relayed line, so this kills exactly that mutant.
    check("LAW-VERIFY relays a verifier failure on a governed spec",
          rc == 1 and 'LAW-VERIFY' in out and '[C10]' in out)

    # L541 — DOC-COUNT when the manifests are unreadable. A count that cannot be
    # verified must fail the build, not pass vacuously: DOC-COUNT exists precisely
    # because unverified counts drift.
    rc, out = mutated(lambda r: remove(r, 'SPEC_MANIFEST.json'))
    check("DOC-COUNT fires when a manifest needed for verification is unreadable",
          rc == 1 and 'could not read a manifest' in out)

    # ── The fence SHAPE the old regex could not read (2026-08-20) ────────────
    # This fixture was written at 2026.08.20.2 against corpus CONTENT — it named the
    # three functions in Framework_MockTestAnalyse.md's S8-1 fence. One release later
    # batch 9 extracted that fence into transport_core.py and the fixture went RED for
    # a reason that had nothing to do with the scanner. A fixture keyed to content
    # measures the corpus; one keyed to the SHAPE measures the code. This builds the
    # shape — an INLINE nested marker, ``` mid-sentence inside a docstring, which is
    # what the corpus actually contained and what the non-greedy regex ended on.
    _tricky = ('```python\n'
               'def outer(a):\n'
               '    """This contract lives in a ```python fence ON PURPOSE."""\n'
               '    return a + 1\n'
               '\n'
               'def after_the_marker(b):\n'
               '    return b * 2\n'
               '```\n')
    _got = blocks(_tricky)
    check("line scanner does not truncate a fence at an inline nested marker",
          len(_got) == 1 and 'after_the_marker' in _got[0])
    # ...and the regex this replaced must demonstrably fail the same input, or the
    # fixture asserts a property nothing ever lacked.
    _old = re.findall(r"```python\n(.*?)```", _tricky, re.S)
    check("the regex this replaced DOES truncate the same input",
          bool(_old) and 'after_the_marker' not in _old[0])

    print(f"audit_sync self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails

if __name__ == '__main__' and '--self-test' in sys.argv:
    sys.exit(0 if _self_test() else 1)

SPECS = sorted(f for f in os.listdir('.') if f.startswith('Framework_') and f.endswith('.md'))
TXT = {f: open(f, encoding='utf-8').read() for f in SPECS}
ROUTES = json.load(open('routes.json'))
ISSUES = defaultdict(list)
# ── SKILL.md — REPO ROOT FIRST (B12, 2026-08-21) ────────────────────────────
# This loader read ONLY '/mnt/skills/user/mock-test-framework/SKILL.md' — a session-
# sandbox mount that exists on NO CI runner. So SKILL-INVENTORY and both TRIGGER-SYNC
# directions never executed in the environment that gates the build; they ran only in
# an interactive session that happened to have the skill mounted, and the 'SKILL.md
# not readable' INFO printed everywhere else looked routine enough that nobody asked
# why a parity check against a file THE REPO ITSELF CARRIES needed a mount to run.
# Same class as GAP-2026-08-17-B4-ENV-SKEW: a check that silently skips in the gating
# environment is indistinguishable from one that passes. Found by the B12 full
# mutation measurement — all six SKILL-dependent emissions survived, including the
# fallback INFO itself, which is the signature of a branch that never runs.
# The repo copy is authoritative: it is version-controlled beside the routes.json it
# must agree with. The mount stays as a last resort for environments with no clone.
# The search list is ENV-INJECTABLE (AUDIT_SYNC_SKILL_PATHS, os.pathsep-separated)
# so the self-test can constrain the search surface: the "no SKILL.md copy exists
# anywhere" fixture removes both repo copies from its corpus COPY but cannot remove
# the session mount, so in any session with /mnt/skills mounted the fixture failed
# while CI (no mount) passed — the GAP-2026-08-17-B4-ENV-SKEW shape, inverted.
# Injecting the list is the same remedy as search_dirs/out_dir. Default UNCHANGED.
_skill_env = os.environ.get('AUDIT_SYNC_SKILL_PATHS')
SKILL_SEARCH_PATHS = (tuple(q for q in _skill_env.split(os.pathsep) if q)
                      if _skill_env is not None else
                      ('SKILL.md', 'mocktestframework_SKILL.md',
                       '/mnt/skills/user/mock-test-framework/SKILL.md'))
skill_txt = None
for _sp in SKILL_SEARCH_PATHS:
    if os.path.exists(_sp):
        skill_txt = open(_sp, encoding='utf-8').read()
        break
def rec(cat, msg): ISSUES[cat].append(msg)

def public(mod):
    try:
        src = open(mod + '.py', encoding='utf-8').read()
    except FileNotFoundError:
        return None
    names = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            names.add(n.name)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            # A re-exported import IS part of the module's public surface: after
            # `from t3_mathcomp import _T3_STATS as T3_STATS`, explain_engine.T3_STATS
            # resolves at runtime exactly like an assignment would. Collecting only
            # def/class/assign made every such name look absent, so a spec that used
            # one was reported as calling into an API that does not exist.
            for a in n.names:
                if a.name != '*':
                    names.add(a.asname or a.name.split('.')[0])
    return names

ALIAS = {'bc': 'blueprint_core', 'pp': 'paper_pipeline', 'ee': 'explain_engine'}
API = {a: public(m) for a, m in ALIAS.items()}
# Scope PER CODE BLOCK: an alias only means the module inside a block that imports it as
# that alias. `pp` is also a common local for doc.add_paragraph(), and `bc` for other locals
# — checking file-wide produces false positives (verified: Framework_MockTestCreate v5.29
# explicitly documents the pp module/paragraph name coexistence as safe).
for f, t in TXT.items():
    for blk in blocks(t):
        bound = {}
        for m in re.finditer(r'^\s*import\s+(\w+)\s+as\s+(\w+)', blk, re.M):
            if m.group(1) in ALIAS.values():
                bound[m.group(2)] = m.group(1)
        for alias, mod in bound.items():
            names = public(mod)
            if not names:
                continue
            # a local rebind of the alias inside the same block disqualifies it
            if re.search(rf'^\s*{alias}\s*=', blk, re.M):
                continue
            for m in re.finditer(rf'\b{alias}\.([A-Za-z_][A-Za-z0-9_]*)', blk):
                if m.group(1) not in names:
                    rec('ENGINE-API', f"{f}: {alias}.{m.group(1)} not found in {mod}.py")

# ── 1b. SKILL.md claimed inventory vs reality ───────────────────────────────
if skill_txt:
    # The claims that ACTUALLY exist in SKILL.md, not the sentence this check was
    # written against. The old regex looked for 'The N framework specs and M engine
    # scripts' — that phrasing left SKILL.md at some point and the check matched
    # nothing thereafter, a silent no-op even where the file WAS readable. Checking a
    # quote nobody maintains is checking nothing; these two phrases are the live
    # inventory line, and if they are ever reworded this check must be re-pointed —
    # which the mspec-is-None branch below now says out loud instead of passing.
    mspec = re.search(r'All\s+(\d+)\s+routed engine scripts, plus the\s+(\d+)\s+'
                      r'tracked-but-never-routed', skill_txt)
    if mspec:
        claim_routed, claim_unrouted = int(mspec.group(1)), int(mspec.group(2))
        _routed = {f for v in ROUTES.values() for f in v if f.endswith('.py')}
        real_routed = len(_routed)
        try:
            _tracked = {k for k in json.load(open('MANIFEST.json',
                        encoding='utf-8'))['files'] if k.endswith('.py')}
            real_unrouted = len(_tracked - _routed)
        except (OSError, ValueError, KeyError):
            real_unrouted = None
        if claim_routed != real_routed:
            rec('SKILL-INVENTORY', f"SKILL.md claims {claim_routed} routed engine "
                                   f"scripts, routes.json routes {real_routed}")
        if real_unrouted is not None and claim_unrouted != real_unrouted:
            rec('SKILL-INVENTORY', f"SKILL.md claims {claim_unrouted} tracked-but-"
                                   f"never-routed scripts, MANIFEST.json minus "
                                   f"routes.json gives {real_unrouted}")
    else:
        rec('SKILL-INVENTORY', "SKILL.md no longer carries the 'All N routed engine "
                               "scripts, plus the M tracked-but-never-routed' line "
                               "this check verifies. Re-point the check at the new "
                               "phrasing — an inventory claim nobody checks is how "
                               "the last one went stale by three engines.")

# ── 2. VERSION CROSS-REFERENCE SYNC ─────────────────────────────────────────
CUR = {}
for f, t in TXT.items():
    m = re.search(r'^#\s*(Framework_\w+)\s+v([0-9][0-9.]*)', t, re.M)
    if m:
        CUR[m.group(1)] = m.group(2)
for f, t in TXT.items():
    for m in re.finditer(r'(Framework_\w+)\s+v([0-9][0-9.]*)', t):
        name, ver = m.group(1), m.group(2)
        if name not in CUR or name == f[:-3]:
            continue
        cur = CUR[name]
        if ver != cur:
            # only flag FORWARD refs (claiming a version that doesn't exist yet)
            try:
                newer = tuple(int(x) for x in ver.split('.')) > tuple(int(x) for x in cur.split('.'))
            except ValueError:
                newer = False
            if newer:
                rec('VERSION-XREF', f"{f}: references {name} v{ver} but current is v{cur}")

# ── 2b. RELEASE SYNC: VERSION file vs CHANGELOG top entry (added after the
#        2026.07.31.4 partial deployment, where CHANGELOG.md missed the release
#        entry while VERSION/MANIFEST shipped — no checker caught it) ──────────
try:
    _ver = open('VERSION', encoding='utf-8').read().strip()
    _top = None
    for _l in open('CHANGELOG.md', encoding='utf-8'):
        _m = re.match(r'^## (\S+)', _l)
        if _m: _top = _m.group(1); break
    if _ver and _top and _ver != _top:
        rec('REL-SYNC', f"VERSION is {_ver} but CHANGELOG top entry is {_top} — "
                        f"partial deployment or unrecorded release")
except OSError:
    rec('INFO', 'VERSION or CHANGELOG.md unreadable — release sync not checked')

# ── 3. TRIGGER SYNC: routes.json vs SKILL.md vs specs ───────────────────────
skill = skill_txt
if skill:
    for trig in ROUTES:
        if not re.search(rf'\b{trig}\b', skill):
            rec('TRIGGER-SYNC', f"routes.json trigger '{trig}' not mentioned in SKILL.md")
    for m in re.finditer(r'\b(PYQ[A-Z]\w+|Mock[A-Z]\w+|Test[A-Z]\w+|ScopedBlueprint)\b', skill):
        if m.group(1) not in ROUTES:
            rec('TRIGGER-SYNC', f"SKILL.md names '{m.group(1)}' but routes.json has no such trigger")
else:
    rec('INFO', 'SKILL.md not readable from here — trigger/route parity vs SKILL not checked')

# ── 4. ROUTED FILES EXIST ───────────────────────────────────────────────────
for trig, files in ROUTES.items():
    for fl in files:
        if not os.path.exists(fl):
            rec('ROUTE-MISSING', f"{trig}: routed file {fl} does not exist")

# ── 5. PIPELINE FILENAME CHAIN (Steps 7, 9, 11) ─────────────────────────────
CHAIN = ['_Create.docx', '_Explanation.docx', '_Final.docx']
OWNER = {'_Create.docx': 'Framework_MockTestCreate.md',
         '_Explanation.docx': 'Framework_MockTestExplain.md',
         '_Final.docx': 'Framework_MockDeliver.md'}
for suffix, owner in OWNER.items():
    if suffix not in TXT.get(owner, ''):
        rec('FILENAME-CHAIN', f"{owner} never mentions its output suffix {suffix}")

# ── 6. PATTERN-ERA ARTEFACT SYNC (the new work) ─────────────────────────────
producers = [f for f, t in TXT.items() if "manifest['pattern_eras']" in t or '"pattern_eras"' in t]
consumers = [f for f, t in TXT.items() if "pattern_eras'" in t and f not in producers]
if not producers:
    rec('ERA-SYNC', "no spec writes manifest['pattern_eras']")
for f, t in TXT.items():
    if 'frequency_scope' in t and '--frequency-scope' not in t and f != 'Framework_Blueprint.md':
        rec('ERA-SYNC', f"{f}: uses frequency_scope but declares no --frequency-scope trigger flag")
for f, t in TXT.items():
    if 'OUT_OF_PATTERN' in t and 'bc.OUT_OF_PATTERN' not in t:
        rec('ERA-SYNC', f"{f}: references OUT_OF_PATTERN without sourcing it from the engine")

# ── 7. BLUEPRINT.JSON SCHEMA SYNC (writer §14 vs readers) ───────────────────
bp = TXT.get('Framework_Blueprint.md', '')
declared = set(re.findall(r'^([a-z_][a-z0-9_]*)\s*:\s', bp, re.M))
readers = ['Framework_MockTestCreate.md',
           'Framework_MockTestExplain.md', 'Framework_MockDeliver.md']
KNOWN = {'axis_schedule', 'difficulty_schedule', 'marking_scheme', 'subtopic_allocations',
         'mocks', 'exam_code', 'blueprint_version', 'sections', 'zero_pyq_rotation'}
for r in readers:
    for m in re.finditer(r"\bbp\.get\('([a-z_]+)'|\bbp\['([a-z_]+)'\]", TXT.get(r, '')):
        fld = m.group(1) or m.group(2)
        if fld not in bp:
            rec('BP-SCHEMA', f"{r}: reads blueprint['{fld}'] — not documented in Framework_Blueprint.md")

# ── 8. LAW PROPAGATION REGISTRY (GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION, P7) ──
# The deepest cause of that GAP was not the undefined name. It was that a LAW was
# remediated FILE BY FILE from a changelog list, so a path nobody listed kept the
# defect, and a later "content byte-identical" split copied it into a brand-new file.
# Nothing in the repo could answer the question "which specs must carry this law, and
# do they all still carry it?" — so nothing noticed for 20 days.
#
# This check answers it in both directions, and the second direction is the one a
# hand-maintained list can never provide:
#   FORWARD  — every spec listed in 'governs' must still satisfy 'verified_by'.
#   REVERSE  — every spec that PERFORMS the governed operation must be listed. A spec
#              that performs it and is absent is a FAIL, so a new file (or a split
#              half) cannot inherit the law's surface without inheriting its checks.
_INJ_LIVE = re.compile(
    r'\b(fetch_drive_docx|collect_corpus_files|stage_drive_payload)\(\s*'
    r'[A-Za-z_][A-Za-z0-9_]*\s*[,)]')


def _live_text(t):
    """Full-line comments blanked. A spec is expected to QUOTE the defect it fixed;
    a commented-out call is documentation, not a call site."""
    return '\n'.join('' if ln.lstrip().startswith('#') else ln
                      for ln in t.split('\n'))


try:
    _REG = json.load(open('LAW_REGISTRY.json', encoding='utf-8'))
except FileNotFoundError:
    _REG = None
    rec('LAW-REGISTRY', "LAW_REGISTRY.json is missing. Every law the framework "
                        "enforces must be machine-checkable; without the registry "
                        "no check can tell whether a law reached every spec it "
                        "governs (GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION P7).")
except ValueError as _exc:
    _REG = None
    rec('LAW-REGISTRY', f"LAW_REGISTRY.json is not valid JSON: {_exc}")

if _REG is not None:
    if not _REG.get('laws'):
        rec('LAW-REGISTRY', "LAW_REGISTRY.json declares no laws — an empty registry "
                            "passes silently and is indistinguishable from no "
                            "enforcement at all.")
    for _law, _meta in sorted((_REG.get('laws') or {}).items()):
        _governs = _meta.get('governs') or []
        _verifiers = _meta.get('verified_by') or []
        if not _verifiers:
            rec('LAW-REGISTRY', f"{_law}: no 'verified_by' — a law with no verifier "
                                f"is a comment, not a check.")
        for _g in _governs:
            if not os.path.exists(_g):
                rec('LAW-REGISTRY', f"{_law}: governs '{_g}', which does not exist. "
                                    f"A stale entry silently shrinks the law's reach.")
        _rule = _meta.get('detect')
        if _rule not in ('live_injection_point_call',
                         'budget_spender_upstream_of_partition'):
            rec('LAW-REGISTRY', f"{_law}: unknown detect rule "
                                f"{_meta.get('detect')!r}; audit_sync cannot derive "
                                f"the performing set, so the REVERSE direction of "
                                f"this law is unenforced.")
            continue

        # REVERSE — derive the performing set from the corpus, never from the list.
        # The half a hand-maintained 'governs' list can never supply: a NEW spec, or
        # the half of a split file, cannot inherit a law's SURFACE without inheriting
        # its CHECKS. GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION is exactly that shape.
        if _rule == 'budget_spender_upstream_of_partition':
            # GAP-2026-08-16-STEP5-SESSION-EXHAUSTION. A spec performs a SESSION-BUDGET
            # operation when it partitions a context budget in a file that also
            # acquires (so the acquisition is a spender), or when it writes the listing
            # cache the model transcribes. Prose does not count — the corollary law is
            # that anything a CI check must inspect has to live where it can read it.
            _performing = set()
            for _f, _t in TXT.items():
                _live = _live_text(_t)
                if ('partition_by_transport' in _live
                        and any(k in _t for k in ('CHANNEL PROBE', 'probe_drive_channel',
                                                  'probe_direct_egress'))):
                    _performing.add(_f)
                elif 'DRIVE_LISTING_CACHE' in _t and 'search_files' in _t:
                    _performing.add(_f)
        else:
            _performing = {f for f, t in TXT.items() if _INJ_LIVE.search(_live_text(t))}
        for _f in sorted(_performing - set(_governs)):
            rec('LAW-COVERAGE',
                f"{_f} performs a {_law} operation (it calls a documented injection "
                f"point) but is NOT listed in LAW_REGISTRY.json 'governs'. Add it, "
                f"and make it satisfy {', '.join(_verifiers)}. This is the exact "
                f"shape of GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION: a spec "
                f"inherited a law's SURFACE without inheriting its CHECKS.")

        # FORWARD — every governed spec must still pass its verifiers.
        _cg = {v.split(':')[1] for v in _verifiers if v.startswith('audit_callgraph:')}
        if _cg and os.path.exists('audit_callgraph.py'):
            import subprocess as _sp
            _targets = [g for g in _governs if os.path.exists(g)]
            if _targets:
                _r = _sp.run([sys.executable, 'audit_callgraph.py'] + _targets,
                             capture_output=True, text=True)
                if _r.returncode != 0:
                    for _line in (_r.stdout + _r.stderr).split('\n'):
                        if re.match(r'\s*\[C\d', _line):
                            rec('LAW-VERIFY', f"{_law}: " + _line.strip()[:240])
                    if not any(c == 'LAW-VERIFY' for c in ISSUES):
                        rec('LAW-VERIFY', f"{_law}: audit_callgraph exited "
                                          f"{_r.returncode} on the governed specs.")

# ── 9. DOC COUNTS (2026.08.15.7) — no hand-maintained live count survives ────
# WHY. CLAUDE.md's deploy gate carried "39/39 — 23 specs + 16 engines" through six
# releases that changed both halves, and its SPEC_MANIFEST paragraph carried "51 files"
# against an actual 57. Neither was caught by any check; both were corrected by hand,
# one at a time, as reviewers happened to notice them. Correcting the instance and not
# the class is the same failure the LAW-PROPAGATION LAW was added to remove — so the
# class is removed here instead.
#
# TWO CHECKS, and the second is the one that makes it permanent:
#   DOC-COUNT       — the FRAMEWORK COUNTS block must equal the files on disk. The
#                     finding states the CORRECT value, so a drift is a build failure
#                     with the fix already written in the error message.
#   DOC-COUNT-IDIOM — a hand-written live count ANYWHERE ELSE in the document is itself
#                     a failure. You cannot reintroduce the defect by writing more prose.
#
# Historical measurements are deliberately untouched: "0 of 1719 questions", "153/153
# figural" and every CHANGELOG figure are frozen EVIDENCE, not live claims, and the
# idiom check is written to the "currently N <noun>" form precisely so it can never
# fire on them.
_DOC = 'CLAUDE.md'
_COUNT_LINE = re.compile(
    r'^\s*(MANIFEST\.json files|SPEC_MANIFEST\.json entries|routes\.json triggers)'
    r'\s*:\s*([0-9]+)\s*$', re.M)
_LIVE_COUNT_IDIOM = re.compile(r'currently\s+\**([0-9]+)\**\s+'
                               r'(files|entries|specs|engines|triggers|scripts)\b', re.I)

if os.path.exists(_DOC):
    _doc = open(_DOC, encoding='utf-8').read()
    try:
        _truth = {
            'MANIFEST.json files':
                len(json.load(open('MANIFEST.json', encoding='utf-8'))['files']),
            'SPEC_MANIFEST.json entries':
                len(json.load(open('SPEC_MANIFEST.json', encoding='utf-8'))['files']),
            'routes.json triggers': len(ROUTES),
        }
    except (OSError, ValueError, KeyError) as _exc:
        _truth = None
        rec('DOC-COUNT', f"could not read a manifest to verify {_DOC}'s counts: {_exc}")

    if _truth is not None:
        _claimed = {m.group(1): int(m.group(2)) for m in _COUNT_LINE.finditer(_doc)}
        for _label, _actual in sorted(_truth.items()):
            if _label not in _claimed:
                rec('DOC-COUNT',
                    f"{_DOC}: the FRAMEWORK COUNTS block has no '{_label}' line. It must "
                    f"read '{_label} : {_actual}'. A count that is not declared cannot be "
                    f"checked, and an unchecked count is the defect this rule removes.")
            elif _claimed[_label] != _actual:
                rec('DOC-COUNT',
                    f"{_DOC}: FRAMEWORK COUNTS says '{_label} : {_claimed[_label]}' but "
                    f"the files on disk give {_actual}. Correct value: {_actual}.")

    # the block's own lines are the ONLY place a live count may be written
    _block_spans = [m.span() for m in _COUNT_LINE.finditer(_doc)]
    for _m in _LIVE_COUNT_IDIOM.finditer(_doc):
        if any(a <= _m.start() < b for a, b in _block_spans):
            continue
        _ln = _doc[:_m.start()].count('\n') + 1
        rec('DOC-COUNT-IDIOM',
            f"{_DOC}:{_ln}: '{_m.group(0)}' is a hand-maintained live count written in "
            f"prose. Every such number in this file has gone stale at least once. Delete "
            f"it and refer to the FRAMEWORK COUNTS block, which audit_sync keeps true.")

# ── REPORT ──────────────────────────────────────────────────────────────────
total = sum(len(v) for v in ISSUES.values())
print(f"specs audited: {len(SPECS)} | triggers: {len(ROUTES)} | findings: {total}\n")
for cat in sorted(ISSUES):
    print(f"[{cat}] {len(ISSUES[cat])}")
    for m in sorted(set(ISSUES[cat]))[:12]:
        print("   -", m)
    print()
sys.exit(1 if any(c != 'INFO' for c in ISSUES) else 0)
