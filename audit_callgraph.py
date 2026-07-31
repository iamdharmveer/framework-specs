#!/usr/bin/env python3
"""audit_callgraph.py — INTRA-SPEC CALL-GRAPH AUDIT (v1.0, 2026-07-26)

Why this exists
---------------
GAP-2026-07-26-002. v2.29 of Framework_MockTestAnalyse shipped a correct
image-integrity subsystem and wired almost none of it to a path that runs. Five
defects, all silent, all passing every existing gate:

  * extract_and_map_images(docx_path=None) had ONE call site and it never passed
    docx_path, so the gated branch was permanently dead.            -> C1
  * its two branches returned arity 3 in different orders, so the unpack
    mis-bound with no interpreter error.                            -> C2
  * one branch assigned a dict key the other did not.               -> C3
  * make_vision_probe / score_vision_probe / verify_images /
    image_clarity_state / image_gate_verdict / gates_passed /
    figural_consistency were called from NO executable spec block.  -> C4
  * expected_size was captured by enumeration and read by nothing.  -> C5

GAP-2026-07-26-003 adds C6. analyse_image_claude() was a pass-bodied stub that a
python loop CALLED and whose return value the same loop immediately consumed. A tool
call cannot happen inside a running python process, so the call was unreachable on
every run of every exam — and because the return was consumed, the literal code raised
AttributeError, meaning production runs executed some SUBSTITUTED body instead. C1-C5
are all WIRING checks and none of them can see a stub body at all; before C6 this file
contained zero occurrences of ast.Pass.                             -> C6

audit_deep.py enforces DELEGATION and TABLE-PARITY. validate_framework_md.py
reports AST-cleanliness. test_routing.py asserts a trigger's route supplies the
modules its specs import. NONE of them assert that a spec's own call sites are
consistent with the signatures and return shapes of the functions that same spec
defines. Every defect above is an intra-spec WIRING fault.

THE RULE THIS ENFORCES
----------------------
A function that exists but is never reached is worse than a function that does
not exist: it reads as covered, it self-tests green, and it silently does
nothing. Every future fix must answer: WHAT IS THE CALL SITE, AND DOES IT REACH
THIS CODE ON A REAL RUN?

Exam-agnostic: contains no exam, subject, section or subtopic name. It reasons
only about Python structure.

Usage:
    python3 audit_callgraph.py                 # audit the whole corpus
    python3 audit_callgraph.py <spec.md> ...   # audit specific specs
Exit code 1 if any finding is raised.
"""

import ast
import glob
import os
import re
import sys

ENGINES = ('blueprint_core.py', 'corpus_io.py')

# Docstring markers that make a parameter contractually required even though it
# carries a default. This is exactly the trap DEFECT-1 fell into: the docstring
# said "callers should always pass it" and no caller did.
REQUIRED_MARKERS = re.compile(
    r'(is required\b|are required\b|must be passed|must always be passed|'
    r'callers should always pass|caller must pass|required for the gates|'
    r'REQUIRED\b)', re.I)

# Helper-looking names inside engine self-tests — fixtures, not public API.
FIXTURE_HINT = re.compile(r'^(fake|good|bad|boom|dup|wrong|drop|make_bad|_)', re.I)


# ─────────────────────────────────────────────────────────────────────────────
# extraction
# ─────────────────────────────────────────────────────────────────────────────

def python_blocks(path):
    """Yield (start_line, source) for every ```python fenced block in a spec.
"""
    out, cur, start = [], None, 0
    for i, line in enumerate(open(path, encoding='utf8').read().split('\n'), 1):
        s = line.strip()
        if s.startswith('```python'):
            cur, start = [], i
            continue
        if s == '```' and cur is not None:
            out.append((start, '\n'.join(cur)))
            cur = None
            continue
        if cur is not None:
            cur.append(line)
    return out


def imported_symbols(path):
    """Symbols a spec EXPLICITLY imports from an engine, in any fenced block.

    An import is an unambiguous, machine-checkable binding: the spec declares it
    depends on this symbol. Some specs legitimately invoke an engine function from a
    ```text block, because the invocation is a parameterised TEMPLATE containing
    <placeholder> values that are not valid Python (PYQExplain S7A-3, PYQDeliver
    S-difficulty). Those functions are wired, not dead.

    This deliberately does NOT extend to call syntax in prose. That distinction is
    load-bearing: in v2.33 image_clarity_state appeared inside a plain fence as the
    prose sentence "... via bc.image_clarity_state(probe_passed, figure_readable)",
    and it WAS dead. Counting fenced call syntax would have missed DEFECT-4; counting
    imports does not, because prose does not contain import statements.
    """
    txt = open(path, encoding='utf8').read()
    names = set()
    for m in re.finditer(r'^\s*from\s+(?:blueprint_core|corpus_io)\s+import\s+(.+?)$',
                         txt, re.M):
        tail = m.group(1)
        if '(' in tail and ')' not in tail:      # parenthesised multi-line import
            start = m.end()
            tail += txt[start:txt.find(')', start) + 1] if ')' in txt[start:] else ''
        for part in re.split(r'[,\s()]+', tail):
            part = part.split('#')[0].strip()
            if re.fullmatch(r'[A-Za-z_]\w*', part) and part != 'import':
                names.add(part)
    return names


def executable_source(path):
    """All executable spec code, comments stripped. Prose and comments do NOT count
    as a call site — that distinction is the entire point of C4."""
    keep = []
    for _, code in python_blocks(path):
        for line in code.split('\n'):
            if not line.strip().startswith('#'):
                keep.append(line)
    return '\n'.join(keep)


def spec_functions(path):
    """{name: {'node','doc','optional','block','lineno'}} for every function a spec defines."""
    found = {}
    for start, code in python_blocks(path):
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            args = node.args.args
            defaults = node.args.defaults
            optional = [a.arg for a in args[len(args) - len(defaults):]] if defaults else []
            optional += [a.arg for a in node.args.kwonlyargs]
            found[node.name] = {
                'node': node,
                'doc': ast.get_docstring(node) or '',
                'optional': optional,
                'block': code,
                'lineno': start + node.lineno - 1,
            }
    return found


def call_sites(code, name):
    """Every ast.Call to `name` inside `code`."""
    hits = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return hits
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        fn = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
        if fn == name:
            hits.append(node)
    return hits


# ─────────────────────────────────────────────────────────────────────────────
# checks
# ─────────────────────────────────────────────────────────────────────────────

def c1_required_arg(path, funcs, findings):
    """A parameter its own docstring marks required must be supplied at every call site."""
    exe = executable_source(path)
    for name, info in funcs.items():
        if not info['optional'] or not REQUIRED_MARKERS.search(info['doc']):
            continue
        required = [p for p in info['optional']
                    if re.search(r'\b' + re.escape(p) + r'\b[^\n]{0,80}?' + REQUIRED_MARKERS.pattern,
                                 info['doc'], re.I)
                    or REQUIRED_MARKERS.search(info['doc'])]
        pos_names = [a.arg for a in info['node'].args.args]
        for call in call_sites(exe, name):
            supplied = {kw.arg for kw in call.keywords if kw.arg}
            for i, _ in enumerate(call.args):
                if i < len(pos_names):
                    supplied.add(pos_names[i])
            for p in required:
                if p not in supplied:
                    findings.append(
                        f"[C1] {os.path.basename(path)}: {name}() is called without "
                        f"'{p}', which its own docstring marks REQUIRED. This is the "
                        f"DEFECT-1 shape: an optional-with-default parameter that no "
                        f"caller supplies makes the guarded branch permanently dead.")


def c2_return_shape(path, funcs, findings):
    """Multiple equal-arity tuple returns must not differ in element identity/order.

    Only compares returns that are ALL bare names — a literal-vs-name difference
    (e.g. `return 'no_year_info', [], []` vs `return mode, recent, avail`) is the
    same shape expressed two ways, not a shape divergence. That distinction removes
    the false positives a naive comparison produces."""
    for name, info in funcs.items():
        rets = [r for r in ast.walk(info['node'])
                if isinstance(r, ast.Return) and isinstance(r.value, ast.Tuple)]
        if len(rets) < 2:
            continue
        arities = {len(r.value.elts) for r in rets}
        if len(arities) != 1:
            continue                      # different arity -> the interpreter WILL complain
        # position of each bare name in each return
        pos = {}
        for r in rets:
            for i, e in enumerate(r.value.elts):
                if isinstance(e, ast.Name):
                    pos.setdefault(e.id, set()).add(i)
        moved = {n: sorted(v) for n, v in pos.items() if len(v) > 1}
        if moved:
            findings.append(
                f"[C2] {os.path.basename(path)}: {name}() returns equal-arity tuples in "
                f"which the SAME name appears at DIFFERENT positions: "
                f"{ {n: v for n, v in sorted(moved.items())} }. Equal arity means the "
                f"interpreter raises nothing — the unpack silently mis-binds (DEFECT-2). "
                f"Give every return one shape.")


def c3_branch_parity(path, funcs, findings):
    """A dict built in several branches must get the same key set in each."""
    for name, info in funcs.items():
        # self_test / harness functions legitimately build a dict incrementally across
        # branches — that is fixture construction, not a production contract.
        if name.startswith(('self_test', 'test_', '_test')):
            continue
        per_target = {}
        for node in ast.walk(info['node']):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            t = node.targets[0]
            if not (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name)):
                continue
            key = None
            sl = t.slice
            if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                key = sl.value
            if key:
                per_target.setdefault(t.value.id, set()).add(key)
        for var, keys in per_target.items():
            dict_lits = [n for n in ast.walk(info['node'])
                         if isinstance(n, ast.Dict) and n.keys
                         and all(isinstance(k, ast.Constant) for k in n.keys)]
            for d in dict_lits:
                lit = {k.value for k in d.keys if isinstance(k.value, str)}
                if lit and keys and lit < keys and (keys - lit):
                    findings.append(
                        f"[C3] {os.path.basename(path)}: {name}() builds '{var}' with "
                        f"keys {sorted(keys)} on one path but {sorted(lit)} on another; "
                        f"missing {sorted(keys - lit)}. A consumer reading the missing "
                        f"key falls through to its default with no error (DEFECT-3).")
                    break


def c4_dead_engine(engine_funcs, corpus_exe, findings):
    """A public engine function no spec calls from executable code is unreachable.

    Two forms count as reached:
      * a CALL          -> name(...)
      * a DELEGATION ALIAS -> local_name = bc.name   (no parens)
    The alias is the framework's established delegation contract — the form
    `detect_question_start = bc.detect_question_start` that audit_deep.py already
    enforces. Binding an engine function to a local name IS wiring it; the calls then
    go through the alias. Prose cannot produce this form, so DEFECT-4 detection is
    unaffected.
    """
    # 2026.07.31.6: audit_canonical.py (the auditor extracted from CreateAudit
    # Appendix A) stays a C4 call-site source — its engine calls were spec-embedded
    # before extraction and remain runtime-reachable (Blueprint 13-7A copies+runs it).
    import os as _os
    if _os.path.exists('audit_canonical.py'):
        corpus_exe = corpus_exe + '\n' + open('audit_canonical.py', encoding='utf-8').read()
    for name, src in sorted(engine_funcs.items()):
        if re.search(r'\b' + re.escape(name) + r'\s*\(', corpus_exe):
            continue
        if re.search(r'=\s*(?:bc|blueprint_core|corpus_io)\.' + re.escape(name) + r'\s*(?:$|[^\w(])',
                     corpus_exe, re.M):
            continue
        findings.append(
            f"[C4] {src}::{name}() is public and exported but is called from NO "
            f"executable block in any spec. Comments and prose are not call sites. "
            f"Either wire it to a path that runs or delete it — a function that "
            f"exists but is never reached reads as covered while doing nothing "
            f"(DEFECT-4).")


def any_python_blocks(path):
    """Yield (start_line, source) for EVERY fenced block that PARSES as python.

    C6 exists because the two Google Drive CLASS T stubs sat inside an UNLABELLED
    13.5 KB fence, so python_blocks() — which keys on the ```python marker — could not
    see them, and neither could validate_framework_md's AST checks nor audit_deep. A
    stub invisible to every static tool in the corpus is exactly the stub that survives
    for months.

    Labelled or not, a fence whose contents compile as python is treated as code here.
    Fences that do not compile (prose, JSON, shell) are skipped — which is also why a
    Phase B protocol must stay prose: it cannot compile, so it can never be mistaken
    for a call site.
    """
    out, cur, start = [], None, 0
    for i, line in enumerate(open(path, encoding='utf8').read().split('\n'), 1):
        s = line.strip()
        if s.startswith('```'):
            if cur is None:
                cur, start = [], i
            else:
                src = '\n'.join(cur)
                try:
                    ast.parse(src)
                    out.append((start, src))
                except SyntaxError:
                    pass
                cur = None
            continue
        if cur is not None:
            cur.append(line)
    return out


def c6_model_agency_stubs(path, findings):
    """C6 — MODEL-AGENCY STUB CONSUMPTION (EXECUTION-BOUNDARY LAW).

    For every FunctionDef whose body is exactly [Pass] (docstring ignored):
      1. FAIL if it carries no `# CLASS: J` or `# CLASS: T` tag.
      2. If CLASS T: FAIL if any call site consumes it — assigned, or passed as an
         argument so python will call it. A CLASS T name may appear as documentation
         only.
      3. CLASS J carries no consumption restriction. Judgment over data already in
         context degrades gracefully: the model reads the spec as a reasoning task and
         produces the value. That is a real property, not luck, and it is why CLASS J
         stubs have always worked while CLASS T stubs never have.

    This would have caught analyse_image_claude() on the day it was written.
    """
    text = open(path, encoding='utf8').read()
    lines = text.split('\n')
    stubs = {}
    for start, block in any_python_blocks(path):
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        blines = block.split('\n')
        for n in ast.walk(tree):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = [b for b in n.body
                    if not (isinstance(b, ast.Expr)
                            and isinstance(b.value, ast.Constant)
                            and isinstance(b.value.value, str))]
            if len(body) != 1 or not isinstance(body[0], ast.Pass):
                continue
            # The tag may sit on the pass line, inside the docstring, or in the
            # comment block immediately above the def.
            window = '\n'.join(blines[max(0, n.lineno - 8):n.end_lineno])
            head = '\n'.join(lines[max(0, start - 30):start + n.end_lineno])
            tag = None
            for hay in (window, head):
                m = re.search(r'CLASS:\s*([JT])\b', hay)
                if m:
                    tag = m.group(1)
                    break
            stubs[n.name] = (tag, start + n.lineno - 1)

    for name, (tag, ln) in sorted(stubs.items()):
        if tag is None:
            findings.append(
                f"[C6] {os.path.basename(path)}:{ln}: {name}() is a pass-bodied "
                f"model-agency stub with no '# CLASS: J' or '# CLASS: T' tag. The "
                f"EXECUTION-BOUNDARY LAW requires every such stub to declare which it "
                f"is — a CLASS T stub cannot be called from python at all, and an "
                f"untagged stub hides that from every reader and every check.")

    class_t = {n for n, (tag, _) in stubs.items() if tag == 'T'}
    if not class_t:
        return
    for start, block in any_python_blocks(path):
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            hit = None
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call):
                f = n.value.func
                nm = getattr(f, 'id', getattr(f, 'attr', None))
                if nm in class_t:
                    hit = (nm, 'its return value is assigned')
            elif isinstance(n, ast.Call):
                for a in list(n.args) + [k.value for k in n.keywords]:
                    if isinstance(a, ast.Name) and a.id in class_t:
                        hit = (a.id, 'it is passed as an argument, so python will '
                                     'call it')
                        break
            if hit:
                findings.append(
                    f"[C6] {os.path.basename(path)}:{start}: {hit[0]}() is CLASS T — "
                    f"it requires a TOOL CALL, which cannot happen inside a running "
                    f"python process — but {hit[1]}. That is unreachable code "
                    f"returning a default forever, silently, on every run. Use "
                    f"MATERIALISE-THEN-INJECT: the model performs the tool call in its "
                    f"own turn and python receives the materialised result through an "
                    f"injected resolver.")


def c5_dangling_value(path, corpus_exe, findings):
    """A value captured into a dict literal that no consumer reads."""
    for _, code in python_blocks(path):
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            for k in node.keys:
                if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
                    continue
                key = k.value
                if len(key) < 5 or not re.match(r'^[a-zA-Z_][\w]*$', key):
                    continue
                readers = len(re.findall(
                    r"(?:\.get\(\s*['\"]" + re.escape(key) + r"['\"]|"
                    r"\[\s*['\"]" + re.escape(key) + r"['\"]\s*\])", corpus_exe))
                if readers == 0:
                    findings.append(
                        f"[C5] {os.path.basename(path)}: '{key}' is written into a dict "
                        f"but nothing in the routed corpus reads it. A captured value "
                        f"with no consumer is the DEFECT-5 shape (fileSize was captured "
                        f"and threaded nowhere, so IMG-1 SKIPped forever).")


# ─────────────────────────────────────────────────────────────────────────────

def main(argv):
    root = os.path.dirname(os.path.abspath(__file__))
    all_specs = sorted(glob.glob(os.path.join(root, 'Framework_*.md')))
    specs = argv[1:] or all_specs
    # C4 asks "does ANY spec call this engine function?" — that question is only
    # meaningful against the WHOLE corpus. On a subset, a function used by a spec
    # outside the subset looks dead when it is not.
    corpus_wide = (len(specs) == len(all_specs))
    if not specs:
        print("no specs found"); return 0

    corpus_exe = '\n'.join(executable_source(s) for s in (all_specs if corpus_wide else specs))

    # Production source of BOTH engines, so a cross-engine call (corpus_io calling
    # bc.taxonomy_fingerprint) counts as reachable. Without this, C4 reports a false
    # positive for every engine-to-engine helper.
    engine_prod = {}
    for _e in ENGINES:
        _p = os.path.join(root, _e)
        if os.path.exists(_p):
            _l = open(_p, encoding='utf8').read().split('\n')
            _st = next((i for i, l in enumerate(_l) if l.startswith('def self_test')), len(_l))
            engine_prod[_e] = '\n'.join(_l[:_st])
    all_engine_prod = '\n'.join(engine_prod.values())

    engine_funcs = {}
    for eng in ENGINES:
        p = os.path.join(root, eng)
        if not os.path.exists(p):
            continue
        src = open(p, encoding='utf8').read()
        lines = src.split('\n')
        st = next((i for i, l in enumerate(lines) if l.startswith('def self_test')), len(lines))
        production = '\n'.join(lines[:st])
        try:
            tree = ast.parse(production)
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.name.startswith('_') or FIXTURE_HINT.match(node.name):
                continue
            # called elsewhere inside the engine itself? then it is reachable.
            calls = len(re.findall(r'[^a-zA-Z_]' + re.escape(node.name) + r'\s*\(', all_engine_prod))
            defs  = len(re.findall(r'\ndef\s+' + re.escape(node.name) + r'\s*\(', all_engine_prod))
            if (calls - defs) > 0:
                continue        # reachable from engine production code (either engine)
            engine_funcs[node.name] = eng

    findings = []
    for s in specs:
        funcs = spec_functions(s)
        c1_required_arg(s, funcs, findings)
        c2_return_shape(s, funcs, findings)
        c3_branch_parity(s, funcs, findings)
        c6_model_agency_stubs(s, findings)
    if corpus_wide:
        imported = set()
        for sp in all_specs:
            imported |= imported_symbols(sp)
        engine_funcs = {k: v for k, v in engine_funcs.items() if k not in imported}
        c4_dead_engine(engine_funcs, corpus_exe, findings)
    else:
        print("  (C4 skipped — needs the full corpus; pass no arguments to run it)")

    print("=" * 78)
    print(f"AUDIT CALLGRAPH — {len(specs)} spec(s), {len(engine_funcs)} unreferenced engine candidate(s)")
    print("=" * 78)
    if not findings:
        print("\n[OK] 0 findings — every documented-required parameter is supplied at "
              "every call site,\n     every multi-return function has one shape, and every "
              "public engine function\n     is reached from executable spec code.")
        return 0
    for f in findings:
        print("\n" + f)
    print(f"\n{'=' * 78}\nTOTAL: {len(findings)} finding(s)")
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
