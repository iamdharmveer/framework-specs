#!/usr/bin/env python3
"""figural_vision.py — figural PRE-TRANSCRIPTION support for PYQExplain §13A.

WHY THIS ENGINE EXISTS
──────────────────────
`view` is a CLASS T operation (CLAUDE.md EXECUTION-BOUNDARY LAW): it can only
happen BETWEEN model turns, never inside a running Python process. Before this
engine, PYQ-1 viewed each figure lazily, at solve time, inside whichever batch
happened to contain it. Two consequences, both measured:

  1. VOLATILITY. An image held in context is not durable. A long run — clone,
     bootstrap, two specs read in full per the skill's RULE 2, then six batches —
     consumes a great deal of context before the LAST figural batch is reached.
     The image channel degrades before the run ends, and a figure viewed in
     batch 1 is not still legible in batch 6. Measured in a single session on
     pixel-verified non-blank files: early views returned perceptible content,
     later views on the SAME files returned empty payloads, and a retry did not
     recover.
  2. LATE DETECTION. A dead image channel surfaced as a halt inside a batch,
     after extraction and role-binding work, rather than at preflight.

The fix is not a better view call. It is to stop treating the image as the
durable artefact. This engine supports a ONE-TIME pass that views every figure
at the earliest executable moment and persists what was seen as TEXT on disk.
Text does not degrade. Every later batch reads the transcription.

WHAT THIS ENGINE IS AND IS NOT
──────────────────────────────
It is Phase A and Phase C of MATERIALISE-THEN-INJECT. It NEVER performs or
models a tool call:

    PHASE A (this engine)  extract + role-bind figures, emit a work queue
    PHASE B (model, prose) view each queued figure IN-TURN, write transcriptions
    PHASE C (this engine)  verify coverage, report, continue deterministically

There is deliberately no `view_figure()` function, not even a stub. A CLASS T
name modelled in Python is unreachable code returning a default forever
(GAP-2026-07-26-003), and audit_callgraph C6 exists to catch exactly that.

NEVER HALTS
───────────
CLAUDE.md: "A CLASS T failure must be LOUD, and must NOT halt." Phase C reports
a shortfall at FAIL severity and returns; it does not raise. Severity follows
the corpus three-tier model: AMBER (paper completes, footer is amber),
VOID_ITEM (this one question carries no derived answer), BLOCKING (never used
here — no vision condition may stop a paper).

Pure stdlib: zipfile, xml.etree, re, json, os, hashlib. No PIL, no docx, no
network. Media parts are written out byte-identical, so nothing is re-encoded
and §12 byte-identity is untouched — this engine never writes to the delivered
document.
"""

import hashlib
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG_REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'

# A transcription shorter than this cannot describe a figure well enough to
# derive an answer from. Chosen as a floor, not a target: the shortest honest
# transcription of a real exam figure in the reference corpus was 118 chars.
MIN_TRANSCRIPT_CHARS = 80

# A transcription must name at least this many DISTINCT visible elements
# (labels, axes, arrows, shapes, values). One element is a caption, not a
# transcription.
MIN_TRANSCRIPT_ELEMENTS = 3

SEVERITY = ('AMBER', 'VOID_ITEM', 'BLOCKING')

# Status vocabulary for a single queued figure.
ST_OK = 'OK'
ST_MISSING = 'MISSING'          # Phase B never wrote anything for this item
ST_EMPTY = 'EMPTY'              # written but blank / whitespace
ST_THIN = 'THIN'                # written but below the transcription floor
ST_STALE = 'STALE'              # written against a different image (sha mismatch)

FAIL_STATUSES = (ST_MISSING, ST_EMPTY, ST_THIN, ST_STALE)

DEPENDENCIES = {'stdlib_only': True}


class FiguralVisionError(ValueError):
    """Raised ONLY for programmer error in Phase A (bad docx, bad arguments).

    Never raised for a vision shortfall — that is a reported condition, not an
    exception. See NEVER HALTS in the module docstring.
    """


# ─────────────────────────────────────────────────────────────────────────────
# PHASE A — extract, role-bind, emit the work queue
# ─────────────────────────────────────────────────────────────────────────────

def preflight():
    """Report what this engine needs. It needs nothing beyond the stdlib."""
    return {'available': {'stdlib': True}, 'missing': [], 'degraded': False}


def _rels_map(zf):
    """rId -> media part name, from word/_rels/document.xml.rels."""
    out = {}
    try:
        raw = zf.read('word/_rels/document.xml.rels')
    except KeyError:
        return out
    for rel in ET.fromstring(raw):
        rid = rel.get('Id')
        target = rel.get('Target') or ''
        if not rid or not target:
            continue
        tgt = target.replace('\\', '/')
        if tgt.startswith('/'):
            tgt = tgt[1:]
        elif not tgt.startswith('word/'):
            tgt = 'word/' + tgt
        out[rid] = tgt
    return out


def _para_text(para):
    """Concatenated w:t text of one paragraph."""
    return ''.join(t.text or '' for t in para.iter('{%s}t' % W_NS))


def _para_embeds(para):
    """Ordered r:embed ids for every drawing in one paragraph."""
    return [b.get('{%s}embed' % R_NS)
            for b in para.iter('{%s}blip' % W_NS.replace(
                'wordprocessingml/2006/main',
                'drawingml/2006/main'))
            if b.get('{%s}embed' % R_NS)]


def extract_figures(docx_path, out_dir, q_re, opt_re):
    """Extract every figure, bind it to (question, role), write it to out_dir.

    q_re / opt_re come from EngineConfig (section_rules CATEGORY C) — this
    engine hardcodes no exam value (RE-9).

    Role binding is READ FROM THE DOCUMENT, never inferred from extraction
    order: a drawing in a paragraph whose text starts with an option label is
    bound to that option; otherwise it is a stem figure. S13-2's warning that
    "an unbound view can key the wrong index" is what this addresses.

    Returns a list of item dicts, in document order.
    """
    if not os.path.exists(docx_path):
        raise FiguralVisionError('docx not found: %s' % docx_path)
    q_pat = re.compile(q_re)
    o_pat = re.compile(opt_re)
    os.makedirs(out_dir, exist_ok=True)

    items = []
    with zipfile.ZipFile(docx_path) as zf:
        rels = _rels_map(zf)
        doc = ET.fromstring(zf.read('word/document.xml'))
        body = doc.find('{%s}body' % W_NS)
        if body is None:
            raise FiguralVisionError('docx has no w:body: %s' % docx_path)
        cur_q = None
        seq = {}
        for para in body.iter('{%s}p' % W_NS):
            text = _para_text(para).strip()
            qm = q_pat.match(text)
            if qm:
                cur_q = int(qm.group(1))
            embeds = _para_embeds(para)
            if not embeds or cur_q is None:
                continue
            om = o_pat.match(text)
            for rid in embeds:
                part = rels.get(rid)
                if not part:
                    continue
                try:
                    blob = zf.read(part)
                except KeyError:
                    continue
                seq[cur_q] = seq.get(cur_q, 0) + 1
                idx = seq[cur_q]
                role = ('opt%s' % om.group(1)) if om else 'stem'
                ext = os.path.splitext(part)[1] or '.bin'
                name = 'Q%03d_%s%s' % (cur_q, role, ext)
                path = os.path.join(out_dir, name)
                with open(path, 'wb') as fh:
                    fh.write(blob)
                items.append({
                    'q': cur_q,
                    'role': role,
                    'ordinal': idx,
                    'path': path,
                    'media_part': part,
                    'sha256': hashlib.sha256(blob).hexdigest(),
                    'bytes': len(blob),
                })
    return items


def write_queue(items, queue_path):
    """Phase A output: the work queue Phase B walks."""
    payload = {
        '_meta': {
            'engine': 'figural_vision.py',
            'phase': 'A',
            'contract': 'view each item.path IN-TURN; write transcriptions to '
                        'the transcripts file keyed by item key',
            'count': len(items),
        },
        'items': items,
    }
    with open(queue_path, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    return queue_path


def item_key(item):
    """Stable key joining a queue item to its transcription."""
    return 'Q%d:%s:%d' % (item['q'], item['role'], item['ordinal'])


def load_queue(queue_path):
    with open(queue_path, encoding='utf-8') as fh:
        return json.load(fh)['items']


# ─────────────────────────────────────────────────────────────────────────────
# PHASE C — verify what Phase B produced; report; never halt
# ─────────────────────────────────────────────────────────────────────────────

def count_elements(text):
    """How many DISTINCT visible elements a transcription names.

    Deliberately crude and exam-agnostic: semicolon/newline/bullet separated
    clauses. A transcription that names one thing is a caption.
    """
    parts = [p.strip() for p in re.split(r'[;\n\u2022]|(?<=[.])\s+', text or '')]
    return len([p for p in parts if len(p) >= 8])


def coerce_text(value):
    """Turn ANY Phase B payload into a string. Never raises.

    Phase B is model-authored JSON with no schema, no validator, and no type
    coercion on the way in — by design, because Phase B cannot be code. So this
    engine must not assume a shape. A list of clauses is not an exotic input
    here: the queue contract asks Phase B to name distinct visible elements,
    which is an enumeration, and count_elements() already splits on exactly the
    separators such an enumeration collapses to. A list is the same data one
    serialisation step earlier, so it is JOINED rather than rejected — a model
    that wrote a list did transcribe the figure.

    The NEVER HALTS contract is void the moment a shape assumption can throw,
    and it is worst exactly when it is least affordable: a degraded vision
    channel is when Phase B output is most likely to be irregular, which is the
    condition §13A exists to survive.
    """
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return '; '.join(coerce_text(v) for v in value)
    if isinstance(value, dict):
        return '; '.join(coerce_text(v) for v in value.values())
    return str(value)


def classify_transcript(item, transcript):
    """Status for ONE queued figure. Pure; never raises, for ANY input shape."""
    if transcript is None:
        return ST_MISSING
    if isinstance(transcript, dict) and 'text' in transcript:
        sha = transcript.get('sha256')
        if sha and item.get('sha256') and coerce_text(sha) != item['sha256']:
            return ST_STALE
        text = coerce_text(transcript.get('text'))
    else:
        text = coerce_text(transcript)
    if not text.strip():
        return ST_EMPTY
    if len(text.strip()) < MIN_TRANSCRIPT_CHARS:
        return ST_THIN
    if count_elements(text) < MIN_TRANSCRIPT_ELEMENTS:
        return ST_THIN
    return ST_OK


def verify_transcripts(items, transcripts):
    """Phase C. Returns a report dict. NEVER raises, NEVER halts.

    transcripts: {item_key: str | {'text':..., 'sha256':...}}
    """
    per_item = []
    for it in items:
        st = classify_transcript(it, (transcripts or {}).get(item_key(it)))
        per_item.append({'key': item_key(it), 'q': it['q'], 'role': it['role'],
                         'status': st})
    bad = [r for r in per_item if r['status'] in FAIL_STATUSES]
    void_qs = sorted({r['q'] for r in bad})
    ok_qs = sorted({r['q'] for r in per_item} - set(void_qs))
    return {
        'total_items': len(items),
        'ok_items': len(per_item) - len(bad),
        'failed_items': len(bad),
        'per_item': per_item,
        'void_questions': void_qs,
        'usable_questions': ok_qs,
        'severity': 'AMBER' if bad else None,
        'clean': not bad,
    }


def vision_report_line(report):
    """One MANDATE-0-safe line. Names no stem, option, or figure content."""
    if report['clean']:
        return ('FIGURAL VISION: %d/%d artefact(s) transcribed — all usable.'
                % (report['ok_items'], report['total_items']))
    return ('FIGURAL VISION: %d of %d artefact(s) NOT usable (%s). '
            'Question(s) %s are VOID_ITEM — no derived answer will be published '
            'for them. Severity AMBER: the paper still completes and delivers. '
            'Remedy: re-run PYQExplain in a session with a working view tool.'
            % (report['failed_items'], report['total_items'],
               ', '.join(sorted({r['status'] for r in report['per_item']
                                 if r['status'] in FAIL_STATUSES})),
               ', '.join('Q.%d' % q for q in report['void_questions'])))


def write_manifest(items, transcripts, report, path):
    """The durable artefact every later batch reads instead of re-viewing."""
    by_q = {}
    for it in items:
        k = item_key(it)
        t = (transcripts or {}).get(k)
        raw = t.get('text') if (isinstance(t, dict) and 'text' in t) else t
        # Store the COERCED string, never the raw payload: transcript_for() is
        # read at solve time and a derivation must always receive text.
        text = coerce_text(raw) if raw is not None else None
        by_q.setdefault(str(it['q']), []).append({
            'role': it['role'], 'ordinal': it['ordinal'],
            'sha256': it['sha256'], 'transcript': text,
            'status': classify_transcript(it, t),
        })
    payload = {'_meta': {'engine': 'figural_vision.py', 'phase': 'C',
                         'severity_model': list(SEVERITY)},
               'figural_questions': sorted({it['q'] for it in items}),
               'void_questions': report['void_questions'],
               'by_question': by_q}
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    return path


def load_manifest(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def transcript_for(manifest, q, role=None):
    """Read a persisted transcription. Returns None when unusable."""
    if not manifest:
        return None
    entries = (manifest.get('by_question') or {}).get(str(q)) or []
    for e in entries:
        if role is not None and e.get('role') != role:
            continue
        if e.get('status') == ST_OK:
            return e.get('transcript')
    return None


# ─────────────────────────────────────────────────────────────────────────────
# SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

def _mk_docx(path):
    """Minimal 2-question docx: Q.1 stem figure, Q.2 four option figures."""
    dml = 'http://schemas.openxmlformats.org/drawingml/2006/main'

    def para(text, rids=()):
        blips = ''.join('<a:blip xmlns:a="%s" r:embed="%s"/>' % (dml, r)
                        for r in rids)
        return ('<w:p><w:r><w:t>%s</w:t>%s</w:r></w:p>' % (text, blips))

    doc = ('<?xml version="1.0"?><w:document xmlns:w="%s" xmlns:r="%s"><w:body>'
           % (W_NS, R_NS)
           + para('Q.1 stem here', ['rId1'])
           + para('Q.2 stem here')
           + para('1.', ['rId2']) + para('2.', ['rId3'])
           + para('3.', ['rId4']) + para('4.', ['rId5'])
           + '</w:body></w:document>')
    rels = ('<?xml version="1.0"?><Relationships xmlns="%s">' % PKG_REL_NS
            + ''.join('<Relationship Id="rId%d" Target="media/image%d.png" '
                      'Type="x"/>' % (i, i) for i in range(1, 6))
            + '</Relationships>')
    with zipfile.ZipFile(path, 'w') as zf:
        zf.writestr('word/document.xml', doc)
        zf.writestr('word/_rels/document.xml.rels', rels)
        for i in range(1, 6):
            zf.writestr('word/media/image%d.png' % i, b'PNGBYTES%d' % i)


def self_test():
    passed = 0
    total = 0
    msgs = []

    def ck(label, cond):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
        else:
            msgs.append('FAIL: ' + label)

    import tempfile
    tmp = tempfile.mkdtemp()
    dpath = os.path.join(tmp, 't.docx')
    _mk_docx(dpath)
    items = extract_figures(dpath, os.path.join(tmp, 'fig'),
                            r'^\s*Q\.?\s*(\d+)', r'^\s*\(?([1-4])[\).]')

    ck('extracts every drawing', len(items) == 5)
    ck('Q.1 bound as stem',
       [i for i in items if i['q'] == 1][0]['role'] == 'stem')
    ck('Q.2 option roles read from the label, not extraction order',
       [i['role'] for i in items if i['q'] == 2]
       == ['opt1', 'opt2', 'opt3', 'opt4'])
    ck('bytes written byte-identical',
       open(items[0]['path'], 'rb').read() == b'PNGBYTES1')
    ck('sha recorded', all(len(i['sha256']) == 64 for i in items))

    qpath = write_queue(items, os.path.join(tmp, 'q.json'))
    ck('queue round-trips', len(load_queue(qpath)) == 5)

    good = ('A right-angled triangle labelled ABC; the vertical leg is marked '
            '3 cm; the horizontal leg is marked 4 cm; the hypotenuse carries '
            'an arrow pointing away from vertex A.')

    # ── THE DEFECT FIXTURE (CLAUDE.md: a self-test must fail on the defect it
    #    was written for). The defect: a blank view payload being accepted as a
    #    successful observation. Each of these MUST be caught.
    ck('DEFECT — empty payload is caught',
       classify_transcript(items[0], '') == ST_EMPTY)
    ck('DEFECT — whitespace payload is caught',
       classify_transcript(items[0], '   \n  ') == ST_EMPTY)
    ck('DEFECT — absent payload is caught',
       classify_transcript(items[0], None) == ST_MISSING)
    ck('DEFECT — caption-length payload is caught',
       classify_transcript(items[0], 'A triangle.') == ST_THIN)
    ck('DEFECT — long but single-element payload is caught',
       classify_transcript(items[0], 'x' * 200) == ST_THIN)
    ck('DEFECT — transcription of a DIFFERENT image is caught',
       classify_transcript(items[0],
                           {'text': good, 'sha256': 'f' * 64}) == ST_STALE)
    ck('a real transcription passes',
       classify_transcript(items[0], good) == ST_OK)
    ck('sha-matched transcription passes',
       classify_transcript(items[0],
                           {'text': good,
                            'sha256': items[0]['sha256']}) == ST_OK)

    # ── THE CHAR-FLOOR FIXTURE. MIN_TRANSCRIPT_CHARS and MIN_TRANSCRIPT_ELEMENTS
    #    are two independent bounds, and every other THIN fixture fails BOTH — so
    #    deleting the character floor left the suite fully green. This payload
    #    separates them: 3 elements (passes the element floor) but under 80
    #    characters, so ONLY the character floor can catch it.
    short_rich = 'The x axis; The y axis; The arrow'
    ck('DEFECT — short but element-rich payload is caught by the CHAR floor',
       classify_transcript(items[0], short_rich) == ST_THIN)
    ck('char-floor fixture really does clear the ELEMENT floor',
       count_elements(short_rich) >= MIN_TRANSCRIPT_ELEMENTS)
    ck('char-floor fixture really is under the CHAR floor',
       len(short_rich) < MIN_TRANSCRIPT_CHARS)

    # ── THE NEVER-HALT FIXTURES. Phase B is model-authored JSON with no schema.
    #    Every shape below raised AttributeError before coercion existed, which
    #    made the engine written to stop a vision failure halting PYQ-1 halt
    #    PYQ-1 itself — the same defect one layer down.
    listed = ['The vertical axis is labelled velocity in metres per second',
              'The horizontal axis is labelled time in seconds',
              'A straight line rises from the origin to the point marked P']
    ck('NEVER-HALT — list payload is joined, not raised',
       classify_transcript(items[0], listed) == ST_OK)
    ck('NEVER-HALT — scalar int payload never raises',
       classify_transcript(items[0], 12345) == ST_THIN)
    ck('NEVER-HALT — scalar float payload never raises',
       classify_transcript(items[0], 3.14) == ST_THIN)
    ck('NEVER-HALT — bool payload never raises',
       classify_transcript(items[0], True) == ST_THIN)
    ck('NEVER-HALT — dict with list text never raises',
       classify_transcript(items[0], {'text': ['a', 'b'],
                                      'sha256': items[0]['sha256']}) == ST_THIN)
    ck('NEVER-HALT — dict with int text never raises',
       classify_transcript(items[0], {'text': 99}) == ST_THIN)
    ck('NEVER-HALT — dict with nested dict text never raises',
       classify_transcript(items[0], {'text': {'v': 1}}) == ST_THIN)
    ck('NEVER-HALT — empty list is EMPTY, not a crash',
       classify_transcript(items[0], []) == ST_EMPTY)
    ck('NEVER-HALT — dict with null text is EMPTY, not a crash',
       classify_transcript(items[0], {'text': None}) == ST_EMPTY)
    ck('a dict WITHOUT a text key is coerced, not treated as a wrapper',
       classify_transcript(items[0], {'a': 'x'}) == ST_THIN)

    # ── THE GENERAL GUARD. The never-halt contract stated as a test rather than
    #    as a docstring: EVERY json shape must yield a report, never an
    #    exception. This binds shapes no fixture above enumerates.
    SHAPES = [None, '', '   ', 'x', good, listed, [], {}, {'text': None},
              {'text': ''}, {'text': []}, {'text': {}}, {'text': 0},
              {'sha256': 'f' * 64}, 0, 1, -1, 3.14, True, False,
              [[], {}], {'text': [{'a': 1}, ['b']]}, ('a', 'b')]
    guard_ok = True
    for shp in SHAPES:
        try:
            r = verify_transcripts(items, {item_key(items[0]): shp})
            if not isinstance(r, dict) or r.get('severity') == 'BLOCKING':
                guard_ok = False
        except Exception:
            guard_ok = False
    ck('NEVER-HALT — every json shape returns a report, none raises', guard_ok)

    all_ok = {item_key(i): good for i in items}
    rep_ok = verify_transcripts(items, all_ok)
    ck('clean report is clean', rep_ok['clean'] and rep_ok['severity'] is None)
    ck('clean report voids nothing', rep_ok['void_questions'] == [])

    partial = dict(all_ok)
    partial[item_key(items[0])] = ''
    rep_bad = verify_transcripts(items, partial)
    ck('shortfall is reported', not rep_bad['clean'])
    ck('shortfall severity is AMBER, never BLOCKING',
       rep_bad['severity'] == 'AMBER')
    ck('only the affected question is voided',
       rep_bad['void_questions'] == [1])
    ck('unaffected questions stay usable', rep_bad['usable_questions'] == [2])

    # NEVER-HALT contract: total vision loss must still RETURN a report.
    rep_dead = verify_transcripts(items, {})
    ck('total vision loss returns, never raises', isinstance(rep_dead, dict))
    ck('total loss is still AMBER, never BLOCKING',
       rep_dead['severity'] == 'AMBER')
    ck('total loss voids every figural question',
       rep_dead['void_questions'] == [1, 2])
    ck('BLOCKING is never emitted by this engine',
       all(r['severity'] != 'BLOCKING'
           for r in (rep_ok, rep_bad, rep_dead)))

    mpath = write_manifest(items, partial, rep_bad, os.path.join(tmp, 'm.json'))
    man = load_manifest(mpath)
    ck('manifest records void questions', man['void_questions'] == [1])
    ck('manifest serves a usable transcription',
       transcript_for(man, 2, 'opt1') == good)
    ck('manifest refuses an unusable transcription',
       transcript_for(man, 1, 'stem') is None)

    # ── THE MANIFEST-COERCION FIXTURE. transcript_for() is read at SOLVE time,
    #    so what the manifest stores is what a derivation receives. Storing the
    #    raw payload would hand a list to the solver and reintroduce the same
    #    shape defect one artefact further downstream — where no gate looks.
    listed_t = {item_key(i): listed for i in items}
    rep_l = verify_transcripts(items, listed_t)
    man_l = load_manifest(write_manifest(items, listed_t, rep_l,
                                         os.path.join(tmp, 'ml.json')))
    served = transcript_for(man_l, 1, 'stem')
    ck('manifest stores a STRING even when Phase B wrote a list',
       isinstance(served, str))
    ck('manifest join preserves every element Phase B listed',
       all(part in (served or '') for part in listed))
    ck('report line names no figure content',
       'triangle' not in vision_report_line(rep_bad).lower())
    ck('report line names the void question',
       'Q.1' in vision_report_line(rep_bad))
    ck('no CLASS T name is modelled in python',
       not any(n.startswith('view_') for n in globals()))

    for m in msgs:
        print(m)
    print("SELF-TEST: %d/%d PASS" % (passed, total))
    return passed == total


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    print("figural_vision.py — figural pre-transcription support. "
          "Run with --self-test.")
