"""audit_deep.py — checks NOT covered by validate_framework_md.py or audit_sync.py.
  1 duplicate function defs within one spec, differing bodies
  2 cross-spec function drift (same name, different logic, 2+ specs)
  3 JSON artefact fields read but produced nowhere in the corpus
  4 declared triggers absent from routes.json
  5 engine-owned logic re-localised inside a spec (delegation contract)
  6 disabled/commented safety assertions in the engines
Docstrings are stripped before comparison: a docstring difference is documentation, not
logic drift. An UNDEFINED-NAME check was built and DELIBERATELY REMOVED — spec code blocks
execute with runtime-supplied context (manifest ids, loaded config, tool names), so
"not assigned in any block" does not imply undefined at runtime, and a check that cannot
tell the two apart trains its readers to ignore it."""
import ast, json, os, re, sys
from collections import defaultdict

DIVERGENCE_BASELINE_FILE = 'XSPEC_DIVERGENCE_BASELINE.json'

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
    acquisition block — `acquire_paper`, `plan_transport`, `probe_drive_channel`, the
    entire Drive transport contract — into something that did not parse, so the
    caller's try/except discarded it and this auditor reported `findings: 0` over code
    it had never read. Measured on the deployed corpus: regex 261 of 264 fences parse,
    line scanner 263 of 263.

    A line-based scanner keyed on the fence markers was built and measured MONTHS
    earlier and then WITHDRAWN, because switching it on surfaced three XSPEC-DRIFT
    findings and this auditor had nowhere to record that they were intentional. That
    was the wrong trade: it kept a clean report by keeping the auditor blind. The
    exemption mechanism now exists (XSPEC_DIVERGENCE_BASELINE.json, and it is a
    ratchet — see load_divergence_baseline), so the scanner ships.

    The scanner takes the fence markers literally: a line whose STRIP is exactly
    ```python opens, a line whose strip is exactly ``` closes. An unterminated fence
    at EOF is dropped rather than swallowing the rest of the file.

    KNOWN LIMIT, STATED RATHER THAN HIDDEN. A nested marker ALONE ON ITS OWN LINE
    inside a docstring would still close the fence early. The regex failed on the
    INLINE shape (``` appearing mid-sentence in prose), which is the shape the corpus
    actually contains and the one that hid the Drive transport contract; this scanner
    handles that. MEASURED 2026-08-20 across all 23 specs: zero fences fail to parse,
    so the residual case is not reachable today. If it ever is, the symptom is a fence
    that stops parsing — loud, not silent — and the fix is docstring-aware tracking.
    That is markdown parsing, and it is not worth building against zero occurrences.
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



def _fp_hash(text):
    import hashlib
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def fingerprint(fn, src):
    """v2 (2026-08-21, GAP-2026-08-21-FINGERPRINT-ENV-DEPENDENCE) — ENVIRONMENT-STABLE.

    v1 hashed ast.dump(ast.parse(ast.unparse(fn))). Both ast.unparse and ast.dump
    change output across CPython versions (quote/format choices; fields such as
    FunctionDef.type_params exist only from 3.12), so IDENTICAL FILE BYTES
    fingerprinted differently in different environments. Measured consequence,
    release 2026.08.21.4: a builder on 3.12 saw all four declared divergences as
    STALE while the deploy environment saw them as current — the builder then
    "refreshed" correct data into values valid only on 3.12, and the deploy gate
    correctly blocked the release. transport_core.py had not changed since
    2026.08.20.3; a fingerprint of an unchanged file that moves means the
    MEASURER moved. The check must measure the artefact, not the interpreter.

    v2 hashes the TOKENIZED SOURCE SEGMENT instead — never unparses, never dumps:
      * COMMENT / NL / NEWLINE / INDENT / DEDENT / ENDMARKER tokens dropped, so
        comments, blank lines and nesting depth do not affect the hash (the v1
        insensitivity that matters, kept);
      * the docstring (when the parsed body starts with one) dropped, as in v1;
      * FSTRING_START/MIDDLE/END runs (3.12+) coalesced back into ONE synthetic
        STRING token whose text is the verbatim source slice — byte-identical to
        the single STRING token 3.11 emits for the same source, so both sides of
        the 3.11/3.12 tokenizer change produce the same fingerprint;
      * token TYPE NAMES (tokenize.tok_name), not numbers, so a renumbering
        between versions cannot rotate hashes.
    STRICTER THAN v1 on formatting: a quote-style or line-wrap edit now changes
    the fingerprint and goes STALE for re-review. That is the correct direction
    for a reviewed-exemption ratchet — what was reviewed is the SOURCE.
    A pinned-digest self-test fixture makes any residual environment drift fail
    the suite loudly instead of silently rotating every fingerprint again.
    """
    import tokenize, io as _io
    seg = ast.get_source_segment(src, fn) or ''
    raw = []
    try:
        for t in tokenize.generate_tokens(_io.StringIO(seg).readline):
            name = tokenize.tok_name.get(t.type, str(t.type))
            if name in ('COMMENT', 'NL', 'NEWLINE', 'INDENT', 'DEDENT',
                        'ENDMARKER', 'ENCODING'):
                continue
            raw.append((name, t.string))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        raw = [('RAW', seg)]
    # Coalesce f-string token runs (3.12+) into one STRING token = the 3.11 shape.
    toks, i = [], 0
    while i < len(raw):
        name, text = raw[i]
        if name == 'FSTRING_START':
            depth, buf = 1, [text]
            i += 1
            while i < len(raw) and depth:
                n2, t2 = raw[i]
                if n2 == 'FSTRING_START':
                    depth += 1
                elif n2 == 'FSTRING_END':
                    depth -= 1
                buf.append(t2)
                i += 1
            toks.append(('STRING', ''.join(buf)))
            continue
        toks.append((name, text))
        i += 1
    # Drop the docstring exactly when the AST says the body starts with one.
    if (fn.body and isinstance(fn.body[0], ast.Expr)
            and isinstance(fn.body[0].value, ast.Constant)
            and isinstance(fn.body[0].value.value, str)):
        depth = 0
        for i, (name, text) in enumerate(toks):
            if name == 'OP' and text in '([{':
                depth += 1
            elif name == 'OP' and text in ')]}':
                depth -= 1
            elif name == 'OP' and text == ':' and depth == 0:
                for j in range(i + 1, len(toks)):
                    if toks[j][0] == 'STRING':
                        del toks[j]
                        break
                break
    return '\x1f'.join(name + '\x1e' + text for name, text in toks)


def _self_test():
    """GAP-2026-08-14-AUDITOR-SELFTESTS. This auditor is a top-to-bottom script,
    so fixtures run it as a SUBPROCESS against a mutated copy of the corpus and
    assert the finding fires — the same mutate-and-expect-red pattern as
    notes_sync_audit. Dispatched BEFORE the corpus loads, so `--self-test`
    works from any directory state."""
    import shutil, subprocess, tempfile
    passed, fails = 0, []
    here = os.path.dirname(os.path.abspath(__file__)) or '.'

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def run_in(root):
        r = subprocess.run([sys.executable, os.path.join(root, 'audit_deep.py')],
                           cwd=root, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def corpus_copy(dst):
        for f in os.listdir(here):
            # XSPEC_DIVERGENCE_BASELINE.json must travel with the corpus, or the
            # "clean copy passes" fixture measures a corpus WITHOUT the declared
            # divergences and reports three findings that the real run does not have.
            if f.endswith(('.md', '.py')) or f in ('routes.json', 'MANIFEST.json',
                                                   DIVERGENCE_BASELINE_FILE):
                shutil.copy(os.path.join(here, f), os.path.join(dst, f))
        return dst

    def mutated(mutate):
        d = tempfile.mkdtemp()
        corpus_copy(d)
        mutate(d)
        rc, out = run_in(d)
        shutil.rmtree(d, ignore_errors=True)
        return rc, out

    def append(root, fname, text):
        with open(os.path.join(root, fname), 'a', encoding='utf-8') as f:
            f.write(text)

    # ── fingerprint v2: environment-stability fixtures (GAP-2026-08-21-
    #    FINGERPRINT-ENV-DEPENDENCE). These run IN-PROCESS, before the corpus
    #    fixtures, because they pin the measuring instrument itself. ──────────
    def _fp(src):
        return _fp_hash(fingerprint(ast.parse(src).body[0], src))
    _base = "def _fx(a, b):\n    total = a + b\n    return f'{total!r} ok'\n"
    _docd = ("def _fx(a, b):\n    '''doc line.'''\n    total = a + b\n"
             "    return f'{total!r} ok'\n")
    _cmtd = ("def _fx(a, b):\n    # comment\n\n    total = a + b\n"
             "    return f'{total!r} ok'   # tail\n")
    _diff = "def _fx(a, b):\n    total = a - b\n    return f'{total!r} ok'\n"
    check("fp2 docstring-insensitive", _fp(_base) == _fp(_docd))
    check("fp2 comment/blank-insensitive", _fp(_base) == _fp(_cmtd))
    check("fp2 different bodies differ", _fp(_base) != _fp(_diff))
    # PINNED DIGEST — the whole point. Computed once, hard-coded. If ANY
    # environment (a future tokenizer change, a different CPython) produces a
    # different value for this fixed source, the suite fails LOUDLY here,
    # instead of silently rotating every declared-divergence fingerprint the
    # way v1 did between 3.11 and 3.12. The fixture source deliberately holds
    # an f-string (the 3.11/3.12 tokenizer split the FSTRING coalescer exists
    # for), a docstring, a comment and a blank line.
    check("fp2 pinned digest is environment-stable",
          _fp(_docd) == 'b6c41f3d5da1100a')
    check("fp2 nested-fstring coalesces to one STRING token",
          fingerprint(ast.parse(_base).body[0], _base).count('STRING') == 1)

    d0 = tempfile.mkdtemp(); corpus_copy(d0)
    rc, out = run_in(d0); shutil.rmtree(d0, ignore_errors=True)
    check("clean corpus copy passes", rc == 0 and 'findings: 0' in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\ndef slugify(x):\n    return x.lower().replace(' ', '-')\n```\n"))
    check("DELEGATION fires on a re-localised engine-owned function",
          rc == 1 and 'DELEGATION' in out and 'slugify' in out)

    rc, out = mutated(lambda r: append(r, 'blueprint_core.py',
        "\nif False:\n    assert 1 == 1\n"))
    check("DISABLED-GUARD fires on an `if False:` assertion",
          rc == 1 and 'DISABLED-GUARD' in out)

    rc, out = mutated(lambda r: append(r, 'blueprint_core.py',
        "\n# assert total == sum(parts)\n"))
    check("DISABLED-GUARD fires on a commented-out assertion",
          rc == 1 and 'commented out' in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n# Trigger: Bogustrigger\n"))
    check("TRIGGER-GRAMMAR fires on a trigger absent from routes.json",
          rc == 1 and 'TRIGGER-GRAMMAR' in out and 'Bogustrigger' in out)

    # GAP-2026-08-15-BAREQ (T-3). Three Q-detection dialects lived in production for
    # the life of the framework because no check could see an anonymous inline regex.
    # This fixture proves check 8 fires — and the two negatives below prove it does
    # NOT fire on the label STRIPPERS or on the canonical tables, which is what makes
    # it usable rather than something readers learn to ignore.
    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nm = re.match(r'^Q\\.?\\s*(\\d+)', t)\n```\n"))
    check("INLINE-QREGEX fires on a private inline question regex",
          rc == 1 and 'INLINE-QREGEX' in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nt = re.sub(r'^Q\\.?\\d+\\.?\\s*', '', t)\n```\n"))
    check("INLINE-QREGEX does NOT fire on a label stripper (re.sub)",
          'INLINE-QREGEX' not in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\n```python\nif bc.detect_question_start(t) is not None:\n    pass\n```\n"))
    check("INLINE-QREGEX does NOT fire on a delegating call",
          'INLINE-QREGEX' not in out)

    rc, out = mutated(lambda r: append(r, 'Framework_PYQSort.md',
        "\nThe step then reads registry['zz_selftest_phantom'] for the count.\n"))
    check("JSON-PARITY fires on a field read that nothing writes",
          rc == 1 and 'JSON-PARITY' in out and 'zz_selftest_phantom' in out)

    def xdrift(r):
        append(r, 'Framework_PYQSort.md',
               "\n```python\ndef shared_selftest_fn(a):\n    return a + 1\n```\n")
        append(r, 'Framework_PYQCount.md',
               "\n```python\ndef shared_selftest_fn(a):\n    return a * 2\n```\n")
    rc, out = mutated(xdrift)
    check("XSPEC-DRIFT fires on the same public function defined differently "
          "in two specs", rc == 1 and 'XSPEC-DRIFT' in out)

    # ══ THE DIVERGENCE RATCHET (2026-08-20) ══════════════════════════════
    # This mechanism SUPPRESSES findings, so it is the most dangerous code in the
    # file: every fixture below exists to prove it cannot suppress anything it was
    # not reviewed for. An exemption mechanism without these is just a mute button.
    import json as _js

    def _base(root):
        return _js.load(open(os.path.join(root, DIVERGENCE_BASELINE_FILE),
                             encoding='utf-8'))

    def _put(root, data):
        with open(os.path.join(root, DIVERGENCE_BASELINE_FILE), 'w',
                  encoding='utf-8') as fh:
            _js.dump(data, fh, indent=2, ensure_ascii=False)

    # 1. THE FENCE SHAPE THE REGEX COULD NOT READ — a SYNTHETIC fixture.
    #    The first version of this check asserted against the live corpus, naming three
    #    functions in Framework_MockTestAnalyse.md's S8-1 fence. One release later that
    #    fence was extracted into transport_core.py and the fixture went RED for a reason
    #    that had nothing to do with the scanner. A fixture keyed to corpus CONTENT
    #    measures the corpus; one keyed to the SHAPE measures the code. This builds the
    #    shape, so it cannot go dormant or false-fail when the corpus moves again.
    #
    #    The shape is an INLINE nested marker — ``` mid-sentence inside a docstring —
    #    which is what the corpus actually contained and what the non-greedy regex ended
    #    its capture on.
    _tricky = ('```python\n'
               'def outer(a):\n'
               '    """This contract lives in a ```python fence ON PURPOSE."""\n'
               '    return a + 1\n'
               '\n'
               'def after_the_marker(b):\n'
               '    return b * 2\n'
               '```\n')
    _got = blocks(_tricky)
    check("scanner returns ONE block for a fence with an inline nested marker",
          len(_got) == 1)
    check("scanner does not truncate at the inline marker",
          bool(_got) and 'after_the_marker' in _got[0])
    check("the recovered block parses and yields BOTH functions",
          bool(_got) and _names_in(_got[0]) == {'outer', 'after_the_marker'})
    # ...and the OLD regex must demonstrably fail the same input, or this fixture is
    # asserting a property nothing ever lacked.
    _old = [b for b in re.findall(r"```python\n(.*?)```", _tricky, re.S)]
    check("the regex this replaced DOES truncate the same input",
          bool(_old) and 'after_the_marker' not in _old[0])

    # 2. An UNDECLARED divergence must still fail. (The xdrift fixture above already
    #    proves this with the baseline present, which is the point: a populated
    #    baseline does not weaken the check for names it does not list.)

    # 3. A declared divergence whose BODY CHANGED must go STALE, not stay silent.
    #    This is the difference between a ratchet and a mute button.
    def _stale_fp(r):
        d = _base(r)
        d['plan_transport']['files']['Framework_PYQCount.md'] = '0' * 16
        _put(r, d)

    rc, out = mutated(_stale_fp)
    check("XSPEC-BASELINE-STALE fires when a declared body no longer matches",
          rc == 1 and 'XSPEC-BASELINE-STALE' in out and 'plan_transport' in out)

    # 4. A reason outside the closed vocabulary must fail. A free-text reason is how a
    #    closed vocabulary becomes a comment field.
    def _bad_reason(r):
        d = _base(r)
        d['acquire_paper']['reason'] = 'because it is fine'
        _put(r, d)
    rc, out = mutated(_bad_reason)
    check("XSPEC-BASELINE-STALE fires on a reason outside the closed vocabulary",
          rc == 1 and 'XSPEC-BASELINE-STALE' in out and 'acquire_paper' in out)

    # 5. An exemption for a divergence that NO LONGER EXISTS must fail, so it cannot
    #    lie dormant and silently cover the next divergence of that name.
    def _dormant(r):
        d = _base(r)
        d['zz_selftest_never_diverged'] = {
            'files': {'Framework_PYQSort.md': 'dead', 'Framework_PYQCount.md': 'dead'},
            'reason': 'step_label_only', 'note': 'fixture'}
        _put(r, d)
    rc, out = mutated(_dormant)
    check("XSPEC-BASELINE-STALE fires on a dormant exemption",
          rc == 1 and 'zz_selftest_never_diverged' in out)

    # 6. DELETING the baseline must resurface every declared divergence. If it does
    #    not, the suppression is coming from somewhere else and the file is decorative.
    #    After batch 9 these three are SPEC-vs-ENGINE pairs, so the finding class is
    #    XSPEC-ENGINE-DRIFT rather than XSPEC-DRIFT — and that is precisely why check
    #    3b exists: without it, extracting one side of a declared pair would have
    #    silently retired the exemption AND the thing it exempted.
    def _drop(r):
        os.remove(os.path.join(r, DIVERGENCE_BASELINE_FILE))
    # v2026.08.22.6 (Item 1c): the expected names are READ FROM THE BASELINE
    # ITSELF, never hardcoded. The previous tuple pinned 'omath' and went red the
    # day Item 1c resolved that divergence for real — a fixture keyed to corpus
    # CONTENT breaks when the corpus moves (WAVE2-PART-C rule: key to the SHAPE).
    # The shape asserted here is the invariant that matters: EVERY entry the live
    # baseline declares must resurface as a finding when the baseline is removed,
    # and the set must be NON-EMPTY so an emptied baseline cannot vacuously pass.
    _declared = [k for k in json.load(open(os.path.join(here,
                     DIVERGENCE_BASELINE_FILE), encoding='utf-8'))
                 if not k.startswith('_')]
    rc, out = mutated(_drop)
    check("removing the baseline resurfaces every declared divergence",
          rc == 1 and bool(_declared) and all(n in out for n in _declared))

    # 7. The printer must never write. A writer is how spec_name_audit re-froze two
    #    defects it had just fixed.
    def _print_only(r):
        before = open(os.path.join(r, DIVERGENCE_BASELINE_FILE), encoding='utf-8').read()
        subprocess.run([sys.executable, os.path.join(r, 'audit_deep.py'),
                        '--print-divergence-baseline'],
                       cwd=r, capture_output=True, text=True)
        after = open(os.path.join(r, DIVERGENCE_BASELINE_FILE), encoding='utf-8').read()
        if before != after:
            append(r, 'Framework_PYQSort.md', '\nzz_printer_wrote_the_baseline\n')
    rc, out = mutated(_print_only)
    check("--print-divergence-baseline does NOT write the file",
          'zz_printer_wrote_the_baseline' not in out)

    # META-ASSERTION: a skipped check is not a passing one.
    EXPECTED = 24
    _total = passed + len(fails)
    if _total != EXPECTED:
        fails.append(f"suite_ran_every_check (ran {_total}, expected {EXPECTED})")
    else:
        passed += 1

    print(f"audit_deep self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


def _names_in(src):
    """Top-level function names in a source block; {} when it does not parse."""
    try:
        return {n.name for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}
    except SyntaxError:
        return set()

if __name__ == '__main__' and '--self-test' in sys.argv:
    sys.exit(0 if _self_test() else 1)

# --print-divergence-baseline: emit a CANDIDATE for a human to paste. It never writes.
# Every entry must therefore arrive as a reviewable diff carrying a reason and a note.
_PRINT_DIVERGENCE = '--print-divergence-baseline' in sys.argv

SPECS=sorted(f for f in os.listdir('.') if f.startswith('Framework_') and f.endswith('.md'))
TXT={f:open(f,encoding='utf-8').read() for f in SPECS}
# The engine set is DERIVED from MANIFEST.json's tracked .py files, not hardcoded.
# It used to be a 4-name tuple while the framework tracked 16 engines, so 12 of them —
# every notes_* engine, corpus_io, figural_core, reconcile_taxonomy and the rest — were
# invisible to check 4 below, and a field those engines write read as "written nowhere".
# Deriving it means the set cannot go stale as engines are added or retired.
_TRACKED=('blueprint_core','paper_pipeline','explain_engine','syllabus_provenance')
try:
    import json as _json
    _TRACKED=tuple(sorted(k[:-3] for k in
                          _json.load(open('MANIFEST.json',encoding='utf-8'))['files']
                          if k.endswith('.py')))
except Exception:
    pass   # no manifest here — fall back to the historical set rather than crashing
ENG={m:open(m+'.py',encoding='utf-8').read() for m in _TRACKED
     if os.path.exists(m+'.py')}
I=defaultdict(list)
def rec(c,m): I[c].append(m)
# ── DECLARED CROSS-SPEC DIVERGENCE (2026-08-20) ──────────────────────────────
# Two specs may legitimately define the same function differently: Step 4 and Step 5
# both perform a CLASS T Drive acquisition, and their contracts genuinely differ (see
# Framework_PYQCount v1.5 and Framework_MockTestAnalyse v2.51.0, where the divergences
# are declared in prose and enforced by mock_sync_audit MS-13).
#
# THIS FILE IS A RATCHET, NOT AN ALLOWANCE, and it is deliberately stricter than the
# other baselines in this repo: an entry pins the sha256 of BOTH bodies. Change either
# side and the exemption goes STALE and FAILS THE BUILD, because the thing that was
# reviewed and declared intentional is no longer the thing in the file. A name-only
# suppression would let real drift accumulate for ever underneath a decision made once.
#
# THERE IS NO WRITER. `--print-divergence-baseline` prints a candidate to stdout for a
# human to paste, so every entry arrives as a reviewable diff. A --write flag is how
# spec_name_audit re-froze two defects it had just fixed (v2.53.1, D5/D6); that switch
# is not built here.
DIVERGENCE_REASONS = {
    'step_label_only':
        'bodies differ only in a printed step identifier (S5-x vs S8-x)',
    'declared_step_divergence':
        'the steps genuinely differ and BOTH specs name the divergence in prose',
    'declared_law_scope':
        'a law applies to one step and is declared out of scope for the other, '
        'with the reason stated in the spec that does not carry it',
    'inherited_pre_existing':
        'a divergence that PRE-DATES the check that found it, entered as debt so the '
        'check could ship. NOT a judgement that the divergence is correct',
}



def load_divergence_baseline(path=DIVERGENCE_BASELINE_FILE):
    """{name: {'files': {file: fp_hash}, 'reason': str, 'note': str}} or {}."""
    if not os.path.exists(path):
        return {}
    try:
        raw = json.load(open(path, encoding='utf-8'))
    except Exception:
        return {}
    return {k: v for k, v in raw.items() if not k.startswith('_')}
# ── 2 DUPLICATE function defs within one spec, with DIFFERENT bodies ────────
for f,t in TXT.items():
    seen=defaultdict(list)
    for b in blocks(t):
        try: tree=ast.parse(b)
        except SyntaxError: continue
        for n in tree.body:
            if isinstance(n,ast.FunctionDef):
                seen[n.name].append(fingerprint(n, b))
    for name,bodies in seen.items():
        if len(bodies)>1 and len(set(bodies))>1:
            rec('DUP-DRIFT',f"{f}: '{name}' defined {len(bodies)}x with DIFFERENT bodies")

# ── 3 CROSS-SPEC function drift (same name, different body, 2+ specs) ───────
glob=defaultdict(dict)
for f,t in TXT.items():
    for b in blocks(t):
        try: tree=ast.parse(b)
        except SyntaxError: continue
        for n in tree.body:
            if isinstance(n,ast.FunctionDef): glob[n.name][f]=fingerprint(n, b)
# THE BASELINE READS ENGINES TOO (Wave 2 Part C B9, 2026-08-20).
# XSPEC-DRIFT compares SPEC against SPEC, which is right: it exists to catch the same
# instruction copied into two step files and then edited in one. The declared-divergence
# baseline needs a wider view, because a divergence does not stop existing when one side
# is extracted into an engine — it stops being VISIBLE.
#
# Measured this release: moving Step 5's Drive transport into transport_core.py made all
# three entries report "no longer diverges", one release after the ratchet was built. The
# ratchet was right that something had changed and wrong about what: `plan_transport`
# still differs from Framework_PYQCount's copy, exactly as declared. Had the entries
# simply been deleted, this refactor would have quietly retired the only check watching
# those three pairs — an extraction silently buying itself an exemption, which is the
# move every baseline in this repo exists to make visible.
glob_all = defaultdict(dict)
for _f, _byfile in glob.items():
    glob_all[_f].update(_byfile)
for _mod, _src in ENG.items():
    try:
        _tree = ast.parse(_src)
    except SyntaxError:
        continue
    for _n in _tree.body:
        if isinstance(_n, ast.FunctionDef):
            glob_all[_n.name][_mod + '.py'] = fingerprint(_n, _src)

DIVERGENCE = load_divergence_baseline()
for name,byfile in glob.items():
    # A leading-underscore name is a FILE-PRIVATE helper by convention; two specs may
    # legitimately use the same private name for unrelated jobs (verified: _norm normalises
    # a Format string in one spec and math dashes in another). Not drift, a name collision.
    if name.startswith('_'): continue
    if len(byfile)>1 and len(set(byfile.values()))>1:
        if name not in DIVERGENCE:
            rec('XSPEC-DRIFT',f"'{name}' defined differently in {sorted(byfile)}")
if _PRINT_DIVERGENCE:
    cand = {'_schema': 'name -> {files: {spec: fingerprint_hash}, reason, note}',
            '_policy': ('THE ONLY LEGITIMATE EDIT IS A DELETION. An entry pins the '
                        'sha256 of BOTH bodies; change either side and it goes STALE '
                        'and fails the build. There is no writer — this candidate is '
                        'printed for a human to paste, so every entry lands as a '
                        'reviewable diff.'),
            '_reasons': DIVERGENCE_REASONS}
    # NEW spec-vs-spec divergences, plus REFRESHED fingerprints for names already
    # declared — an entry goes stale when either side is edited OR when one side is
    # extracted into an engine, and both need the same paste-a-diff workflow.
    _named = set(load_divergence_baseline())
    for _n, _bf in sorted(glob_all.items()):
        if _n.startswith('_'):
            continue
        _spec_only = glob.get(_n, {})
        _new_drift = len(_spec_only) > 1 and len(set(_spec_only.values())) > 1
        if not (_new_drift or _n in _named):
            continue
        if len(_bf) > 1 and len(set(_bf.values())) > 1:
            cand[_n] = {'files': {f: _fp_hash(fp) for f, fp in sorted(_bf.items())},
                        'reason': '<one of _reasons>',
                        'note': '<where the divergence is declared, and why>'}
    print(json.dumps(cand, indent=2, ensure_ascii=False))
    sys.exit(0)

# ── 3b CROSS-BOUNDARY drift: a SPEC copy of a name a routed ENGINE defines ──
# XSPEC-DRIFT compares spec against spec, so the moment one side of a shared function
# is extracted into an engine the pair stops being watched. That is not hypothetical:
# batch 9 extracted Step 5's Drive transport and all three declared divergences
# immediately reported "no longer diverges".
#
# ADAPTERS ARE EXEMPT BY CONSTRUCTION, not by list. A spec-side copy whose entire body
# forwards to the engine (`return bc.<name>(...)`) has nothing to drift from — check 5
# already uses that test, and reusing it here is what keeps this from firing on every
# correctly-delegated function in the estate. MEASURED at introduction: 10 non-adapter
# copies corpus-wide, of which 7 pre-date this release.
#
# Those 7 are entered in XSPEC_DIVERGENCE_BASELINE.json as inherited debt rather than
# used as a reason to withhold the check. Withholding is what happened to the line
# scanner for months — a clean report bought by keeping the auditor blind — and this
# batch exists because that trade was wrong.
_ADAPTER_PREFIXES = ('bc', 'blueprint_core', 'corpus_io', 'cio', 'ee', 'tc',
                     'transport_core', 'explain_engine', 't3_mathcomp')


def _is_delegating_adapter(node):
    body = [x for x in node.body if not (isinstance(x, ast.Expr)
                                         and isinstance(x.value, ast.Constant))]
    if len(body) != 1:
        return False
    src = ast.unparse(node)
    return any(f'{p}.{node.name}' in src for p in _ADAPTER_PREFIXES)


_spec_nonadapter = defaultdict(dict)
for f, t in TXT.items():
    for b in blocks(t):
        try:
            tree = ast.parse(b)
        except SyntaxError:
            continue
        for n in tree.body:
            if isinstance(n, ast.FunctionDef) and not _is_delegating_adapter(n):
                _spec_nonadapter[n.name][f] = fingerprint(n, b)
_engine_defs = defaultdict(dict)
for _mod, _src in ENG.items():
    try:
        _tree = ast.parse(_src)
    except SyntaxError:
        continue
    for _n in _tree.body:
        if isinstance(_n, ast.FunctionDef):
            _engine_defs[_n.name][_mod + '.py'] = fingerprint(_n, _src)

for name in sorted(set(_spec_nonadapter) & set(_engine_defs)):
    if name.startswith('_'):
        continue
    pair = dict(_spec_nonadapter[name])
    pair.update(_engine_defs[name])
    if len(set(pair.values())) < 2:
        continue                                  # identical bodies are not drift
    if name in DIVERGENCE:
        continue                                  # declared; pinned by the check below
    rec('XSPEC-ENGINE-DRIFT',
        f"'{name}' is defined in {sorted(_spec_nonadapter[name])} AND differently in "
        f"{sorted(_engine_defs[name])}, and the spec copy is not a delegating adapter. "
        f"Either delegate to the engine, or declare the divergence with a reason in "
        f"{DIVERGENCE_BASELINE_FILE}.")

# EVERY BASELINE ENTRY IS VALIDATED HERE, iterating the BASELINE rather than the
# findings. The first version validated inside the XSPEC-DRIFT loop, which only runs
# for names defined in 2+ SPECS — so the moment batch 9 extracted one side into an
# engine, the fingerprint pin stopped being checked at all while the file still looked
# authoritative. A pin that is only checked when the finding would have fired anyway is
# not a pin. Iterating the declarations is the only version that cannot go quiet.
for name in sorted(DIVERGENCE):
    entry = DIVERGENCE[name]
    byfile = glob_all.get(name, {})
    # An exemption for a divergence that no longer exists is dead weight that will
    # silently cover a FUTURE divergence of the same name. The only legitimate edit to
    # this file is a deletion, so the auditor asks for that deletion out loud.
    if not (len(byfile) > 1 and len(set(byfile.values())) > 1):
        rec('XSPEC-BASELINE-STALE',
            f"'{name}' is declared in {DIVERGENCE_BASELINE_FILE} but no longer "
            f"diverges. DELETE the entry — a dormant exemption will silently cover "
            f"the next divergence of this name.")
        continue
    # DECLARED — but only for the EXACT bodies that were reviewed. A stale entry is its
    # own finding, never a pass: silently extending a once-reviewed exemption over
    # newly-changed code is the failure mode every baseline in this repo prevents.
    want = entry.get('files') or {}
    have = {f: _fp_hash(fp) for f, fp in byfile.items()}
    if entry.get('reason') not in DIVERGENCE_REASONS:
        rec('XSPEC-BASELINE-STALE',
            f"'{name}' declared with unknown reason {entry.get('reason')!r} — "
            f"legal reasons: {sorted(DIVERGENCE_REASONS)}")
    elif have != want:
        rec('XSPEC-BASELINE-STALE',
            f"'{name}' is declared as an intentional divergence, but the bodies "
            f"CHANGED since it was reviewed (declared {want}, found {have}). "
            f"Re-review the divergence and update {DIVERGENCE_BASELINE_FILE}, or "
            f"delete the entry if the functions should now agree.")

# ── 4 JSON artefact write/read parity (field must be produced SOMEWHERE) ───
CORPUS="\n".join(TXT.values())+"\n".join(ENG.values())
for art in ('registry','exam_config','subtopic_manifest','blueprint'):
    for f,t in TXT.items():
        for m in re.finditer(rf"\b{art}(?:\.json)?\[['\"]([a-z_]+)['\"]\]",t):
            fld=m.group(1)
            # Count BOTH quote styles. The read pattern above accepts ['"], but the
            # write count used to accept only 'fld' — so a corpus written in double
            # quotes (every notes_* engine and spec) counted zero writers and every
            # such field reported as unwritten. Quote style is not evidence.
            if CORPUS.count(f"'{fld}'")+CORPUS.count(f'"{fld}"')<2:
                rec('JSON-PARITY',f"{f}: reads {art}['{fld}'] but nothing in the corpus writes it")

# ── 5 declared triggers must exist in routes.json ──────────────────────────
ROUTES=json.load(open('routes.json'))
for f,t in TXT.items():
    for m in re.finditer(r'^#?\s*Trigger(?:\s+FORMAT)?:\s*(?:Step\s*\d+[a-z]?:\s*)?([A-Z][A-Za-z]+)\b',t,re.M):
        name=m.group(1)
        if name in ('Step','This','The','See','Same','Note'): continue
        if name not in ROUTES:
            rec('TRIGGER-GRAMMAR',f"{f}: declares Trigger '{name}' not in routes.json")


# ── 5 DELEGATION CONTRACT: shared engine logic must never be re-localised ───
#   Mutation testing exposed this blind spot. XSPEC-DRIFT only fires when the SAME name is
#   defined differently in 2+ SPECS. Once a function is correctly delegated to the engine,
#   only ONE spec-local definition remains possible — so re-localising it in a single spec
#   produces zero drift signal and the check goes green. That is precisely how the Step-4 /
#   Step-5 heading-parser drift could return the day after it was fixed.
#   Rule: any name the engine owns must NOT be defined inside a spec's code blocks.
ENGINE_OWNED = {'parse_taxonomy_level','is_taxonomy_heading','detect_question_start',
                'extract_year_from_filename','classify_paper_era','exam_config_bounds',
                'type_resolver_from_config','paper_eras_from_progress',
                'filter_progress_to_eras','rescale_to_total','largest_remainder_apportion',
                'derive_axis_schedule','difficulty_counts','compute_r_avg','slugify'}
for f,t in TXT.items():
    for b in blocks(t):
        try: tree=ast.parse(b)
        except SyntaxError: continue
        for n in tree.body:
            if isinstance(n,ast.FunctionDef) and n.name in ENGINE_OWNED:
                # A thin ADAPTER that just forwards to bc.<name> is compliant: it exists to
                # bind a spec-local argument (e.g. is_option) and holds no logic of its own.
                body=[x for x in n.body if not (isinstance(x,ast.Expr)
                      and isinstance(x.value,ast.Constant))]
                src=ast.unparse(n) if body else ''
                delegating = (len(body)==1 and f'bc.{n.name}' in src)
                if not delegating:
                    rec('DELEGATION',f"{f}: defines '{n.name}' locally — the engine owns it. "
                        f"Re-localising shared logic is how cross-step drift returns.")

# ── 6 DISABLED SAFETY NETS in the engines ──────────────────────────────────
#   Also from mutation testing: turning `assert sum(...) == total` into
#   `if False: assert ...` broke nothing visible, because no test feeds the invalid input
#   the assertion exists to catch. A safety net that never fires is undetectable
#   behaviourally — only statically.
for mod,src in ENG.items():
    try: tree=ast.parse(src)
    except SyntaxError: continue
    for n in ast.walk(tree):
        if isinstance(n,ast.If) and isinstance(n.test,ast.Constant) and n.test.value is False:
            if any(isinstance(x,ast.Assert) for x in ast.walk(n)):
                rec('DISABLED-GUARD',f"{mod}.py L{n.lineno}: assertion disabled by `if False:`")
        if isinstance(n,ast.If) and isinstance(n.test,ast.Constant) and n.test.value is False:
            rec('DEAD-BRANCH',f"{mod}.py L{n.lineno}: unreachable `if False:` branch")
    for i,l in enumerate(src.split('\n'),1):
        # A COMMENTED-OUT assertion still parses as python once the '#' is stripped.
        # An English sentence that merely begins with the word "assert" (a wrapped
        # prose comment: "... C1-C7 / assert ledger completeness and ...") does not.
        # Without this discriminator the check reported prose as a disabled guard,
        # which is how it read the moment the engine set widened past four files.
        if re.match(r'\s*#\s*assert\b',l):
            try: ast.parse(re.sub(r'^\s*#\s*','',l))
            except SyntaxError: continue
            rec('DISABLED-GUARD',f"{mod}.py L{i}: assertion commented out")

# ── 7 SHARED DATA-TABLE PARITY ─────────────────────────────────────────────
#   Delegating the FUNCTION is not enough if each spec still carries its own copy of the
#   table the function reads.
#
#   2026-07-25 — THIS CHECK COULD NOT FIRE. The old extraction regex was
#       r'Q_PATTERNS\s*=\s*\[(.*?)\]'
#   whose non-greedy body stops at the FIRST ']' — and the third documented pattern,
#   r'^Question\s+(\d+)\s*[:.]', contains one. So on a five-entry spec table it captured
#   only the first two entries, compared those against the engine's two, found them equal,
#   and reported clean. Every spec in the corpus passed while three of them documented
#   five patterns against an engine that implements two.
#   That is worse than a missing check: the specs cite this check by name as their
#   guarantee, so the silence read as evidence, and the obvious "fix" it invited — widening
#   the engine to match the documented tables — would be catastrophic. In a normalised
#   document, questions are "Q.N" and options are "N. text", so the bare-number pattern
#   matches every OPTION: a 100-question paper would parse as 500 questions.
#   The body now matches whole quoted entries rather than scanning for a bracket.
#
#   SOURCE_-prefixed tables are deliberately exempt. Step 1 parses RAW exam dumps, where
#   "1." and "(1)" are genuine question numbering and options are not yet canonical; that
#   is a different contract from the engine's normalised-document detector, and conflating
#   the two is what produced the divergence above.
_ENTRY = r"r'((?:[^'\\]|\\.)*)'"          # one quoted raw-string entry, escape-aware
def _table(text, name):
    m = re.search(name + r'\s*=\s*\[', text)
    if not m:
        return None
    depth, i = 0, m.end() - 1
    while i < len(text):                    # walk to the matching close bracket
        if text[i] == '[': depth += 1
        elif text[i] == ']':
            depth -= 1
            if depth == 0: break
        i += 1
    return tuple(re.findall(_ENTRY, text[m.end():i]))

canon = _table(ENG.get('blueprint_core',''), 'Q_PATTERNS')
if canon:
    for f,t in TXT.items():
        local = _table(t, r'(?<!SOURCE_)\bQ_PATTERNS')
        if local is not None and local != canon:
            rec('TABLE-PARITY',f"{f}: local Q_PATTERNS has {len(local)} entry(ies), "
                f"blueprint_core's canonical table has {len(canon)} — the two would parse "
                f"the same paper differently. If the extra entries are for RAW source "
                f"detection, name the table SOURCE_Q_PATTERNS; do NOT widen the engine.")

# ── 8 INLINE Q-DETECTION REGEX (GAP-2026-08-15-BAREQ, R-6) ─────────────────
#   TABLE-PARITY compares NAMED tables. DELEGATION compares FunctionDefs. An inline
#   ANONYMOUS r'^Q...' literal handed straight to re.match/search/fullmatch/compile is
#   neither, which is how three incompatible Q-detection dialects lived in production
#   alongside the canonical table for the entire life of the framework:
#       A  engine   ^Q\.\s*(\d+)\s+ / ^Q(\d+)\.\s+     Steps 3, 5
#       B  Step 4   ^Q\.?\s*(\d+)                       PYQCount, PYQCore
#       C  Step 1   ^Q\.(\d+)                           PYQPrepare CHECK 1/2/12/15/21
#   B and C matched a bare "Q.4"; A did not. So Step 1 CERTIFIED a 60-question file
#   that Step 3 read as 56 and Step 4 counted as 60 again — three steps, three answers,
#   no gate. Post-remedy the three dialects agree ACCIDENTALLY, which is precisely the
#   failure mode blueprint_core.py documents for the old Step-4 copy; agreement reached
#   by coincidence is not a contract. This check makes the private copy unrepresentable.
#
#   MATCH context only. A re.sub(r'^Q\.?\d+\.?\s*', '', t) is a label STRIPPER, not a
#   detector — it cannot disagree about whether a question exists — and is allowed.
#   The TABLES themselves are list literals, not calls, so they are untouched here and
#   remain TABLE-PARITY's business.
_QLIT = re.compile(r'\^Q')
_MATCHERS = {'match', 'search', 'fullmatch', 'compile'}
for f, t in TXT.items():
    for b in blocks(t):
        try: tree = ast.parse(b)
        except SyntaxError: continue
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call) or not n.args: continue
            fn = n.func
            if not (isinstance(fn, ast.Attribute) and fn.attr in _MATCHERS
                    and isinstance(fn.value, ast.Name) and fn.value.id == 're'):
                continue
            a0 = n.args[0]
            if not (isinstance(a0, ast.Constant) and isinstance(a0.value, str)): continue
            v = a0.value
            if _QLIT.match(v) and '\\d' in v:
                rec('INLINE-QREGEX',
                    f"{f}: inline question regex r'{v}' passed to re.{fn.attr}() — "
                    f"delegate to bc.detect_question_start() (a Q-number) or "
                    f"bc.is_bare_q_label() (the bare-label SHAPE). A private copy is how "
                    f"producer and consumer came to disagree (GAP-2026-08-15-BAREQ).")

tot=sum(len(v) for v in I.values())
print(f"specs: {len(SPECS)} | engines: {len(ENG)} | findings: {tot}\n")
for c in sorted(I):
    print(f"[{c}] {len(I[c])}")
    for m in sorted(set(I[c]))[:10]: print("   -",m)
    print()
sys.exit(1 if tot else 0)
