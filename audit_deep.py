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
            if f.endswith(('.md', '.py')) or f in ('routes.json', 'MANIFEST.json'):
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

    print(f"audit_deep self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails

if __name__ == '__main__' and '--self-test' in sys.argv:
    sys.exit(0 if _self_test() else 1)

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

    KNOWN REMAINING LIMIT — 2 of 147 blocks, DELIBERATELY NOT FIXED HERE.
    The non-greedy `(.*?)` ends the capture at the FIRST ``` in the body, so a fence
    containing a triple backtick inside a docstring is cut mid-string
    (Framework_MockTestAnalyse.md's S8-1 batch-loop acquisition block truncates at its
    line 250). A line-based scanner keyed on the fence markers fixes it and was built
    and measured — it takes this extractor to 146/146 — but it surfaces three
    pre-existing XSPEC-DRIFT findings (acquire_paper, plan_transport,
    probe_drive_channel differ between Framework_MockTestAnalyse.md and
    Framework_PYQCount.md), and this auditor has no exemption mechanism: its own
    self-test asserts the live corpus reports `findings: 0`.
    Two of those three are INTENTIONAL step divergence — probe_drive_channel differs
    only in its step label (S8-0 vs S5-0), and Step 5's plan_transport carries the
    v2.51.0 SESSION-BUDGET LAW that Step 4 never received. Whether Step 4 SHOULD
    receive it is a real open question under the LAW-PROPAGATION LAW, and it is a
    behavioural decision about Step 4 for every exam in the estate — not something to
    settle inside a fence-extraction fix. Tracked as backlog; see the GAP doc.
    """
    import textwrap
    return [textwrap.dedent(b) for b in
            re.findall(r"```python\n(.*?)```", t, re.S)]
def fingerprint(fn):
    fn=ast.parse(ast.unparse(fn)).body[0]
    if (fn.body and isinstance(fn.body[0], ast.Expr)
            and isinstance(fn.body[0].value, ast.Constant)
            and isinstance(fn.body[0].value.value, str)):
        fn.body = fn.body[1:] or [ast.Pass()]
    return ast.dump(fn)

# ── 2 DUPLICATE function defs within one spec, with DIFFERENT bodies ────────
for f,t in TXT.items():
    seen=defaultdict(list)
    for b in blocks(t):
        try: tree=ast.parse(b)
        except SyntaxError: continue
        for n in tree.body:
            if isinstance(n,ast.FunctionDef):
                seen[n.name].append(fingerprint(n))
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
            if isinstance(n,ast.FunctionDef): glob[n.name][f]=fingerprint(n)
for name,byfile in glob.items():
    # A leading-underscore name is a FILE-PRIVATE helper by convention; two specs may
    # legitimately use the same private name for unrelated jobs (verified: _norm normalises
    # a Format string in one spec and math dashes in another). Not drift, a name collision.
    if name.startswith('_'): continue
    if len(byfile)>1 and len(set(byfile.values()))>1:
        rec('XSPEC-DRIFT',f"'{name}' defined differently in {sorted(byfile)}")

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
