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
SPECS=sorted(f for f in os.listdir('.') if f.startswith('Framework_') and f.endswith('.md'))
TXT={f:open(f,encoding='utf-8').read() for f in SPECS}
ENG={m:open(m+'.py',encoding='utf-8').read() for m in
     ('blueprint_core','paper_pipeline','explain_engine','explain_audit_gate','syllabus_provenance')
     if os.path.exists(m+'.py')}
I=defaultdict(list)
def rec(c,m): I[c].append(m)
def blocks(t): return re.findall(r"```python\n(.*?)```",t,re.S)
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
            if CORPUS.count(f"'{fld}'")<2:
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
        if re.match(r'\s*#\s*assert\b',l):
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

tot=sum(len(v) for v in I.values())
print(f"specs: {len(SPECS)} | engines: {len(ENG)} | findings: {tot}\n")
for c in sorted(I):
    print(f"[{c}] {len(I[c])}")
    for m in sorted(set(I[c]))[:10]: print("   -",m)
    print()
sys.exit(1 if tot else 0)
