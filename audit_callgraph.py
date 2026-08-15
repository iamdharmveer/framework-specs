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

# ── INJECTION POINTS (C7/C8) ─────────────────────────────────────────────────
# GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION. An INJECTION POINT is an engine function
# that takes a CALLABLE the caller owns, precisely because the operation behind it is
# CLASS T — a tool call the model performs in its own turn. The argument must therefore
# be a RESOLVER over results that already exist. Map: name -> positional index of the
# injected argument.
INJECTION_POINTS = {
    'fetch_drive_docx':     0,   # download_fn / resolver
    'collect_corpus_files': 0,   # list_fn
}
INJ_CALL_RE = re.compile(
    r'\b(' + '|'.join(sorted(INJECTION_POINTS)) +
    # No whitespace between the callee and '(' — real code never has it, and prose
    # of the form "corpus_io.collect_corpus_files (recursive, paginated, per EC-P23)"
    # does. That one rule removed the only false positive found during development.
    r')\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*[,)]')
ENGINE_CALL_RE = re.compile(
    r'\b(?:corpus_io|bc|blueprint_core|reconcile_taxonomy|syllabus_provenance|'
    r'notes_core|explain_engine|final_assembly|paper_pipeline|figural_core)\.\w+\(')
BIND_RE = (r'(?:def\s+{n}\b|{n}\s*=|lambda[^:\n]*\b{n}\b|'
           r'def\s+\w+\s*\([^)]*\b{n}\b|import\s+.*\b{n}\b|as\s+{n}\b|'
           r'for\s+{n}\b|with\s+.*\bas\s+{n}\b)')

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


def _blank_comment_lines(text):
    """Replace every FULL-LINE comment with an empty line, preserving line numbers.

    A spec legitimately QUOTES the defect it fixed — Framework_PYQCount v1.3 reproduces
    the old `fetch_drive_docx(gdrive_download_file, ...)` call inside its CLASS T block
    so a future reader can see the shape being forbidden. A commented-out call is
    documentation, not a call site, and C7's text pass must not fire on it. Blanking
    rather than deleting keeps reported line numbers honest.
    """
    return '\n'.join('' if ln.lstrip().startswith('#') else ln
                      for ln in text.split('\n'))


def _spec_bound_names(path):
    """Every name a reader could resolve inside this spec's own python."""
    names = set(dir(__builtins__)) | {
        'corpus_io', 'bc', 'blueprint_core', 're', 'os', 'json', 'sys', 'math',
        'Counter', 'Document', 'datetime', 'defaultdict', 'base64', 'self',
    }
    for _, block in any_python_blocks(path):
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(n.name)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    a = n.args
                    for arg in list(a.args) + list(a.posonlyargs) + list(a.kwonlyargs):
                        names.add(arg.arg)
                    if a.vararg:
                        names.add(a.vararg.arg)
                    if a.kwarg:
                        names.add(a.kwarg.arg)
            elif isinstance(n, ast.Lambda):
                for arg in n.args.args:
                    names.add(arg.arg)
            elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                names.add(n.id)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for al in n.names:
                    names.add((al.asname or al.name).split('.')[0])
            elif isinstance(n, ast.ExceptHandler) and n.name:
                names.add(n.name)
            elif isinstance(n, (ast.For, ast.comprehension)):
                for t in ast.walk(n.target):
                    if isinstance(t, ast.Name):
                        names.add(t.id)
    return names


def c7_unbound_transport(path, findings):
    """C7 — UNBOUND TRANSPORT ARGUMENT (EXECUTION-BOUNDARY LAW, coverage half).

    GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION. C6 anchors on a pass-bodied `def`: it
    asks "here is a stub — is it tagged, and is it consumed?". That detects a
    MISLABELLED or MISUSED model-agency stub and structurally CANNOT detect a MISSING
    one. Framework_PYQCount passed the name `gdrive_download_file` into
    corpus_io.fetch_drive_docx while defining no stub at all, so there was no ast.Pass
    to anchor to and C6 correctly reported 0 findings against its own contract. The
    check was not broken; its COVERAGE MODEL was incomplete.

    C7 closes it from the other side: for every call to a documented INJECTION POINT,
    the injected argument must be BOUND somewhere in the same spec's own python. An
    unbound transport name is a CLASS T tool call written as python — executed
    literally it raises NameError, so the lane is unreachable on every run of every
    exam.

    C7 RUNS A TEXT PASS, NOT ONLY AN AST PASS. THIS IS THE CRUX. The real defect's call
    site lived in an UNTAGGED fence that does not parse as python (it mixed prose,
    box-drawing characters and indented pseudo-code), and every AST-based check in the
    repo skips such a block in its entirety. An AST-only implementation of this very
    check returns 0 findings on the very defect it was written for — verified both ways
    during the investigation. Do not "simplify" this by deleting the text pass.

    Together C6 and C7 are exhaustive over the injection surface:
      declared but passed  -> C6      not declared and passed -> C7
      resolver passed      -> both silent, which is the correct state.
    """
    seen = set()
    bound = _spec_bound_names(path)
    base = os.path.basename(path)

    # (a) AST pass — parseable fences, precise argument positions.
    for start, block in any_python_blocks(path):
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            fn = n.func
            name = getattr(fn, 'attr', getattr(fn, 'id', None))
            idx = INJECTION_POINTS.get(name)
            if idx is None or len(n.args) <= idx:
                continue
            arg = n.args[idx]
            if isinstance(arg, ast.Name) and arg.id not in bound:
                seen.add((name, arg.id, start + n.lineno - 1))

    # (b) TEXT pass — every fence, tagged or not, parseable or not.
    text = _blank_comment_lines(open(path, encoding='utf8').read())
    for m in INJ_CALL_RE.finditer(text):
        fn, arg = m.group(1), m.group(2)
        if re.search(BIND_RE.format(n=re.escape(arg)), text):
            continue
        seen.add((fn, arg, text[:m.start()].count('\n') + 1))

    for fn, arg, ln in sorted(seen, key=lambda t: t[2]):
        findings.append(
            f"[C7] {base}:{ln}: {fn}() is injected with `{arg}`, which is NEVER BOUND "
            f"anywhere in this spec. An injection point requires a RESOLVER over "
            f"already-materialised results; an unbound transport name is a "
            f"model-agency (CLASS T) tool call written as python. Executed literally "
            f"it raises NameError, so the lane is unreachable on every run of every "
            f"exam. Declare it `# CLASS: T` AND pass a resolver — see "
            f"Framework_MockTestAnalyse THE BRIDGE and Framework_PYQCount S5-0.")


def c8_executable_source_coverage(path, findings, warnings):
    """C8 — EXECUTABLE-SOURCE COVERAGE.

    A contract the CI cannot read is a contract the CI cannot enforce. Framework_PYQCount
    carried 36 fences of which 5 were ```python-tagged, and the acquisition contract —
    the single most load-bearing instruction in the step — was in an untagged one. That
    is why GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION survived a corpus-wide audit
    reporting zero findings.

    FAIL for the INJECTION SURFACE: a live (non-comment) call to a documented injection
    point must sit in a fence that is tagged ```python AND parses. The surface is small
    and the risk is proven, so this is enforced immediately rather than warned about.

    WARN for the rest: any other routed-engine call in an untagged fence is reported but
    does not fail the build — 28 such fences exist corpus-wide today and many are
    legitimately prose. Promoting those to FAIL is a separate, deliberate migration.
    """
    base = os.path.basename(path)
    lines = open(path, encoding='utf8').read().split('\n')
    fences = [(i + 1, l.strip()) for i, l in enumerate(lines) if l.strip().startswith('```')]
    for i in range(0, len(fences) - 1, 2):
        open_ln, tag = fences[i]
        close_ln = fences[i + 1][0]
        body = '\n'.join(lines[open_ln:close_ln - 1])
        live = _blank_comment_lines(body)
        if tag == '```python':
            try:
                ast.parse(body)
                continue                      # tagged and parses — fully inspectable
            except SyntaxError as exc:
                if INJ_CALL_RE.search(live):
                    findings.append(
                        f"[C8] {base}:{open_ln}: this fence is tagged ```python but "
                        f"does NOT parse ({exc.msg}), and it contains a call to an "
                        f"injection point. Every AST check skips it, so the contract "
                        f"inside it is unenforceable. Fix the syntax.")
                else:
                    warnings.append(f"[C8-WARN] {base}:{open_ln}: ```python fence does "
                                    f"not parse ({exc.msg}).")
                continue
        if INJ_CALL_RE.search(live):
            findings.append(
                f"[C8] {base}:{open_ln}: a live call to an injection point "
                f"({', '.join(sorted({m[0] for m in INJ_CALL_RE.findall(live)}))}) sits "
                f"in an UNTAGGED fence (closes at line {close_ln}). Every AST-based "
                f"check in the repo skips it, which is exactly how "
                f"GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION survived for 20 days. Move "
                f"the contract into a ```python fence that parses, and leave prose "
                f"here referring to it by name.")
        elif ENGINE_CALL_RE.search(live):
            warnings.append(
                f"[C8-WARN] {base}:{open_ln}: routed-engine call in an untagged fence "
                f"— not inspectable by any AST check.")


def governed_specs(root):
    """Specs LAW_REGISTRY says EXECUTION-BOUNDARY-LAW governs. Empty when absent.

    C6-PRE is scoped to these deliberately. Every spec in the corpus should ideally be
    inspectable, but only a GOVERNED spec has a law delegating verification to a check
    that a non-compiling fence can disarm — and that delegation is what turns an
    unreadable fence from untidy into unverifiable.
    """
    import json as _json
    reg = None
    for cand in ([os.path.join(r, 'LAW_REGISTRY.json') for r in root]
                 if isinstance(root, (list, tuple, set))
                 else [os.path.join(root, 'LAW_REGISTRY.json')]):
        if os.path.exists(cand):
            try:
                reg = _json.load(open(cand, encoding='utf-8'))
                break
            except (OSError, ValueError):
                return set()
    if reg is None:
        return set()
    law = (reg.get('laws') or {}).get('EXECUTION-BOUNDARY-LAW') or {}
    return set(law.get('governs') or [])


def _all_fences(path):
    """Yield (start_line, tag, body) for EVERY fence, compiling or not."""
    out, cur, start, tag = [], None, 0, ''
    for i, line in enumerate(open(path, encoding='utf8').read().split('\n'), 1):
        s = line.strip()
        if s.startswith('```'):
            if cur is None:
                cur, start, tag = [], i, s
            else:
                out.append((start, tag, '\n'.join(cur)))
                cur = None
            continue
        if cur is not None:
            cur.append(line)
    return out


def c6pre_inspectability(path, findings, governed):
    """C6-PRE — A GOVERNED SPEC MUST BE INSPECTABLE (EXECUTION-BOUNDARY LAW).

    GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. C6 anchors on pass-bodied defs found
    via any_python_blocks(), which yields ONLY fences that compile — deliberately, and
    for a good reason. The consequence nobody priced: a CLASS T stub inside a fence
    that does NOT compile is, to C6, a stub that does not exist. C6 then builds an
    empty class_t set, returns early at `if not class_t: return`, and never reaches the
    consumption sites — which live in the fence next door and compile fine.

    Measured 2026-08-15 on Framework_MockTestAnalyse.md: the untagged fence spanning
    lines 321-603 failed ast.parse at line 328 on an em-dash IN PROSE; both gdrive
    stubs (lines 544, 554) lived in it; C6 reported 0 findings against two live
    violations at lines 655 and 658, and audit_sync reported the law verified.

      A check that can be structurally disarmed by the shape of its input is not a
      check. It is a check-shaped hole.

    So the law's precondition is verified BEFORE the law: for every spec the registry
    governs, no CLASS marker may hide in a fence the inspector cannot read. This FAILS
    the build; it is not a warning. C8 already emitted a correct WARN for that exact
    line and it was one of 86, indistinguishable from the other 85.

    Splitting the fence is the fix. Deleting the em-dash is not: the next prose line in
    the same fence re-breaks it, and prose does not belong in a code fence at all.
    """
    if os.path.basename(path) not in governed:
        return
    for start, tag, body in _all_fences(path):
        if not re.search(r'CLASS:\s*[JT]\b', body):
            continue
        try:
            ast.parse(body)
        except SyntaxError as exc:
            findings.append(
                f"[C6-PRE] {os.path.basename(path)}:{start}: this spec is GOVERNED by "
                f"EXECUTION-BOUNDARY-LAW, but a 'CLASS: J/T' marker sits in a fence "
                f"that does NOT parse as python ({exc.msg} at fence line {exc.lineno}, "
                f"file line {start + (exc.lineno or 0)}). audit_callgraph inspects only "
                f"fences that compile, so every CLASS marker in this fence is invisible "
                f"to C6 — the law reports 0 findings on this file while it cannot "
                f"actually be verified here. SPLIT the fence: prose in an untagged "
                f"fence, code in a ```python fence that parses. Do NOT try to fix this "
                f"by deleting non-ASCII characters; a non-ASCII character inside a `#` "
                f"comment compiles fine, and the next prose line will re-break it.")


def c9_unfilled_container(path, findings):
    """C9 — UNFILLED INJECTION CONTAINER (EXECUTION-BOUNDARY LAW, producer half).

    GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. The three existing checks cover the
    injection SITE and nothing else:

        C6  declared as CLASS T and passed anyway        -> fires
        C7  not declared anywhere and passed             -> fires
        C9  correctly declared, correctly injected, and  -> NOTHING FIRED
            the container the resolver reads is never
            filled by any producer in the spec

    Framework_MockTestAnalyse v2.49.1 sat in that third state for its whole life. It
    declared tagged CLASS T stubs and injected a bound `drive_resolver`, so C6 and C7
    were both satisfied and correct. But the resolver read `drive_payloads`, a keyword
    parameter defaulting to None and collapsed to {} on the next line, with NO PRODUCER
    anywhere in the spec — no call site, no assignment, and a PHASE A described only in
    a prose comment that the execution order never reached. It could only ever be
    empty, so every paper raised TransportFallback and the entire corpus routed to
    manual upload on every run of every exam.

      C7 verifies that the injected NAME exists.
      Nothing verified that the injected CONTAINER is ever FILLED.

    A producer is one of exactly two things, and the second is what makes the rule
    tight rather than advisory:
      (a) an assignment in this spec's compiling python — a literal, a json.load(), an
          engine call, anything that binds the name to a value; or
      (b) a parameter WITH NO DEFAULT on the function that owns the resolver, so a
          caller that forgets it gets a TypeError rather than an empty dict.

    A parameter defaulting to None or {} is NOT a producer — that default IS the
    defect. Neither is a prose fence: a protocol the CI cannot parse is a protocol it
    cannot credit, which is the same rule C6-PRE enforces one level up.
    """
    base = os.path.basename(path)
    for start, block in any_python_blocks(path):
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue

        # ── who could FILL a container in this block ────────────────────────
        real_assign, defaulted, no_default, guarded = set(), {}, set(), set()
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                a = n.args
                pos = list(a.posonlyargs) + list(a.args)
                first_defaulted = len(pos) - len(a.defaults)
                for i, arg in enumerate(pos):
                    if i < first_defaulted:
                        no_default.add(arg.arg)
                    else:
                        defaulted.setdefault(arg.arg, []).append(n.name)
                for arg, dflt in zip(a.kwonlyargs, a.kw_defaults):
                    (no_default.add(arg.arg) if dflt is None
                     else defaulted.setdefault(arg.arg, []).append(n.name))
            elif isinstance(n, ast.If):
                # the FAIL-LOUDLY guard: `if name is None: raise ...`. A defaulted
                # parameter whose absence RAISES cannot silently reach the resolver,
                # so it is a legitimate producer contract — this is the shape
                # Framework_MockTestAnalyse already uses for vision_pending.
                t = n.test
                if (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name)
                        and any(isinstance(o, (ast.Is, ast.IsNot)) for o in t.ops)
                        and any(isinstance(x, ast.Raise) for x in ast.walk(n))):
                    guarded.add(t.left.id)

        for n in ast.walk(tree):
            if not isinstance(n, ast.Assign):
                continue
            rhs = {x.id for x in ast.walk(n.value) if isinstance(x, ast.Name)}
            for t in n.targets:
                if not isinstance(t, ast.Name):
                    continue
                # `x = x or {}` is NOT a producer — it is the defect wearing an
                # assignment's clothes: it binds the empty default and moves on.
                # Nor is `y = a or {}` where `a` is itself a defaulted parameter.
                if t.id in rhs or (rhs & set(defaulted)):
                    continue
                real_assign.add(t.id)

        producers = real_assign | no_default | guarded

        # ── resolvers handed to a documented injection point ────────────────
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            fname = getattr(n.func, 'attr', getattr(n.func, 'id', None))
            idx = INJECTION_POINTS.get(fname)
            if idx is None or len(n.args) <= idx:
                continue
            arg = n.args[idx]
            if not isinstance(arg, ast.Name):
                continue
            for d in ast.walk(tree):
                if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef)) and d.name == arg.id:
                    fn = d
                elif (isinstance(d, ast.Assign) and isinstance(d.value, ast.Lambda)
                      and any(isinstance(t, ast.Name) and t.id == arg.id
                              for t in d.targets)):
                    fn = d.value
                else:
                    continue
                if isinstance(fn, ast.Lambda):
                    local = {a2.arg for a2 in fn.args.args}
                else:
                    local = {a2.arg for a2 in list(fn.args.posonlyargs)
                             + list(fn.args.args) + list(fn.args.kwonlyargs)}
                container = None
                for s in ast.walk(fn):
                    if (isinstance(s, ast.Subscript) and isinstance(s.value, ast.Name)
                            and s.value.id not in local):
                        container = s.value.id
                        break
                if container is None or container in producers:
                    continue
                findings.append(
                    f"[C9] {base}:{start + n.lineno - 1}: {fname}() is injected with "
                    f"`{arg.id}`, which reads the container `{container}` — and nothing "
                    f"in this spec ever FILLS it"
                    + (f" (`{container}` is a parameter with a default, on "
                       f"{', '.join(sorted(set(defaulted[container])))}, and its "
                       f"absence is not guarded)" if container in defaulted else "")
                    + ". A correctly-injected resolver over an empty container fails "
                    "EVERY lookup, so every item degrades to the fallback lane on every "
                    "run — invisible to C6 and C7, which only check the injection SITE. "
                    "Fill it from this spec's own python, give it no default, or guard "
                    "it with `if <name> is None: raise ...`. A bare default of None or "
                    "{} is the defect, not the fix "
                    "(GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION).")


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

    findings, warnings = [], []
    _governed = governed_specs(
        [os.path.dirname(os.path.abspath(s)) for s in specs] + [root])
    for s in specs:
        funcs = spec_functions(s)
        c1_required_arg(s, funcs, findings)
        c2_return_shape(s, funcs, findings)
        c3_branch_parity(s, funcs, findings)
        c6pre_inspectability(s, findings, _governed)
        c6_model_agency_stubs(s, findings)
        c7_unbound_transport(s, findings)
        c8_executable_source_coverage(s, findings, warnings)
        c9_unfilled_container(s, findings)
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
    if warnings:
        print(f"\n{len(warnings)} C8 warning(s) — untagged fences carrying engine calls "
              f"(reported, not failing):")
        for w in warnings[:8]:
            print("  " + w)
        if len(warnings) > 8:
            print(f"  ... and {len(warnings) - 8} more")
    if not findings:
        print("\n[OK] 0 findings — every documented-required parameter is supplied at "
              "every call site,\n     every multi-return function has one shape, and every "
              "public engine function\n     is reached from executable spec code.")
        return 0
    for f in findings:
        print("\n" + f)
    print(f"\n{'=' * 78}\nTOTAL: {len(findings)} finding(s)")
    return 1


def self_test():
    """GAP-2026-08-14-AUDITOR-SELFTESTS. One synthetic spec fixture per wiring
    check (C1/C2/C3/C6), each run through a SUBPROCESS so module state never
    bleeds between verdicts, plus a clean fixture and the live corpus."""
    import subprocess, tempfile
    passed, fails = 0, []
    here = os.path.abspath(__file__)

    def check(name, cond):
        nonlocal passed
        if cond:
            passed += 1
        else:
            fails.append(name)

    def probe(body):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "Framework_Fixture.md")
        open(p, 'w', encoding='utf-8').write(
            "# Framework_Fixture v1.0 — self-test fixture\n\n```python\n"
            + body + "```\n")
        r = subprocess.run([sys.executable, here, p],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    rc, out = probe("def ok(a):\n    return a + 1\n\ny = ok(2)\n")
    check("clean fixture passes", rc == 0 and '0 findings' in out)

    rc, out = probe('def load(path=None):\n'
                    '    """Callers should always pass path."""\n'
                    '    return path\n\nx = load()\n')
    check("C1 fires on a documented-required argument no caller supplies",
          rc == 1 and '[C1]' in out)

    rc, out = probe("def duo(flag):\n    a, b = 1, 2\n    if flag:\n"
                    "        return a, b\n    return b, a\n\nx, y = duo(True)\n")
    check("C2 fires on equal-arity returns with a name at different positions",
          rc == 1 and '[C2]' in out)

    rc, out = probe("def build(flag):\n    if flag:\n        d = {'alpha': 1}\n"
                    "    else:\n        d = {}\n        d['alpha'] = 1\n"
                    "        d['beta'] = 2\n    return d\n\nr = build(True)\n")
    check("C3 fires on a dict built with different key sets per branch",
          rc == 1 and '[C3]' in out)

    rc, out = probe("def analyse_thing(x):\n    pass\n\n"
                    "val = analyse_thing(5)\nprint(val + 1)\n")
    check("C6 fires on a pass-bodied stub whose return value is consumed",
          rc == 1 and '[C6]' in out)

    def probe_raw(markdown):
        """Write an ARBITRARY spec body — needed for C7/C8, whose whole point is
        fences that are untagged and/or do not parse."""
        d = tempfile.mkdtemp()
        p = os.path.join(d, "Framework_Fixture.md")
        open(p, 'w', encoding='utf-8').write(
            "# Framework_Fixture v1.0 — self-test fixture\n\n" + markdown)
        r = subprocess.run([sys.executable, here, p], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    # ── C7 / C8 — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION ─────────────────
    rc, out = probe("import corpus_io\n"
                    "x = corpus_io.fetch_drive_docx(gdrive_download_file, p, d)\n")
    check("C7 fires on an injection point receiving a name bound nowhere",
          rc == 1 and '[C7]' in out)

    # THE REGRESSION. An AST-only implementation returns 0 findings here, which is
    # precisely why the live defect survived. If this fixture ever goes green with
    # the text pass removed, C7 has been silently reduced to C6's blind spot.
    rc, out = probe_raw("```\n"
                        "  ACQUIRE the file:\n"
                        "  \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n"
                        "      local_path = corpus_io.fetch_drive_docx(\n"
                        "          gdrive_download_file, paper, dest)\n"
                        "```\n")
    check("C7 fires when the call site is in an UNTAGGED, NON-PARSEABLE fence",
          rc == 1 and '[C7]' in out)
    check("C8 fires on an injection-point call in an untagged fence",
          '[C8]' in out)

    rc, out = probe("import corpus_io, json\n"
                    "payloads = json.load(open('cache.json'))\n"
                    "resolver = lambda fid: payloads[fid]\n"
                    "x = corpus_io.fetch_drive_docx(resolver, p, d)\n")
    check("C7 silent when the argument is an assigned lambda", rc == 0)

    rc, out = probe("import corpus_io, json\n"
                    "payloads = json.load(open('cache.json'))\n"
                    "def resolver(fid):\n    return payloads[fid]\n"
                    "x = corpus_io.fetch_drive_docx(resolver, p, d)\n")
    check("C7 silent when the argument is a def", rc == 0)

    rc, out = probe("import corpus_io\n"
                    "def go(list_fn):\n"
                    "    return corpus_io.collect_corpus_files(list_fn, fid)\n")
    check("C7 silent when the argument is a function parameter", rc == 0)

    rc, out = probe_raw("Enumerate via corpus_io.collect_corpus_files (recursive, "
                        "paginated, per EC-P23).\n")
    check("C7 silent on prose with whitespace before '('", rc == 0)

    rc, out = probe("import corpus_io, json\n"
                    "# historical defect, quoted deliberately:\n"
                    "#     corpus_io.fetch_drive_docx(gdrive_download_file, p, d)\n"
                    "payloads = json.load(open('cache.json'))\n"
                    "resolver = lambda fid: payloads[fid]\n"
                    "y = corpus_io.fetch_drive_docx(resolver, p, d)\n")
    check("C7 silent on a commented-out historical example", rc == 0)

    rc, out = probe_raw("```python\ndef gdrive_download_file(fid, path):\n"
                        "    \"\"\"CLASS: T — not executable python.\"\"\"\n"
                        "    pass  # CLASS: T\n"
                        "```\n\n```python\nimport corpus_io\n"
                        "x = corpus_io.fetch_drive_docx(gdrive_download_file, p, d)\n```\n")
    check("C6 catches the declared-but-passed case C7 deliberately does not",
          rc == 1 and '[C6]' in out)

    def probe_governed(markdown):
        """C6-PRE is scoped to LAW_REGISTRY.governs, so the fixture needs a registry
        naming it. Without one the check is correctly silent — which is itself the
        first assertion below."""
        import json as _json
        d = tempfile.mkdtemp()
        p = os.path.join(d, "Framework_Fixture.md")
        open(p, 'w', encoding='utf-8').write(
            "# Framework_Fixture v1.0 — self-test fixture\n\n" + markdown)
        _json.dump({"laws": {"EXECUTION-BOUNDARY-LAW": {
            "governs": ["Framework_Fixture.md"],
            "verified_by": ["audit_callgraph:C6"]}}},
            open(os.path.join(d, 'LAW_REGISTRY.json'), 'w', encoding='utf-8'))
        r = subprocess.run([sys.executable, here, p], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    # ── C6-PRE / C9 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION ───────────
    # THE REGRESSION. A CLASS T stub inside a fence that does not compile is, to C6,
    # a stub that does not exist — so C6 returns early and never scans the call sites,
    # which compile fine one fence away. That is how a dead Drive lane survived with
    # four auditors green. The em-dash below is in PROSE, exactly as it was in the
    # real defect; it is NOT the bug, the prose-inside-a-code-fence is.
    _hidden = ("```\n"
               "Trigger grammar \u2014 prose that cannot compile\n"
               "def gdrive_search(q):\n"
               "    \"\"\"CLASS: T \u2014 not executable python.\"\"\"\n"
               "    pass  # CLASS: T\n"
               "```\n")
    rc, out = probe_governed(_hidden)
    check("C6-PRE fires on a CLASS marker inside a NON-COMPILING fence of a "
          "governed spec", rc == 1 and '[C6-PRE]' in out)

    rc, out = probe(_hidden.replace('```\n', '', 1).replace('```\n', '', 1))
    check("C6-PRE is silent when the spec is not governed by the registry",
          '[C6-PRE]' not in out)

    rc, out = probe_governed("```python\n"
                             "def gdrive_search(q):\n"
                             "    \"\"\"CLASS: T \u2014 not executable python.\"\"\"\n"
                             "    pass  # CLASS: T\n"
                             "```\n")
    check("C6-PRE is silent once the CLASS marker sits in a fence that compiles",
          rc == 0 and '[C6-PRE]' not in out)

    rc, out = probe("import corpus_io\n"
                    "def run(a, drive_payloads=None):\n"
                    "    drive_payloads = drive_payloads or {}\n"
                    "    def r(fid):\n"
                    "        return drive_payloads[fid]\n"
                    "    return corpus_io.fetch_drive_docx(r, a, '/t')\n")
    check("C9 fires on a resolver over a container that has no producer",
          rc == 1 and '[C9]' in out)

    rc, out = probe("import corpus_io, json\n"
                    "payloads = json.load(open('c.json'))\n"
                    "def r(fid):\n    return payloads[fid]\n"
                    "x = corpus_io.fetch_drive_docx(r, p, '/t')\n")
    check("C9 is silent when the container is filled from json.load", rc == 0)

    rc, out = probe("import corpus_io\n"
                    "def mk(drive_payloads):\n"
                    "    def r(fid):\n        return drive_payloads[fid]\n"
                    "    return corpus_io.fetch_drive_docx(r, {}, '/t')\n")
    check("C9 is silent when the container is a parameter with NO default", rc == 0)

    rc, out = probe("import corpus_io\n"
                    "def run(a, drive_payloads=None):\n"
                    "    if drive_payloads is None:\n"
                    "        raise RuntimeError('PHASE A must supply this')\n"
                    "    def r(fid):\n        return drive_payloads[fid]\n"
                    "    return corpus_io.fetch_drive_docx(r, a, '/t')\n")
    check("C9 is silent when a defaulted container is guarded by a raising check",
          rc == 0)

    rc, out = probe("import corpus_io\n"
                    "def go(a=None):\n"
                    "    ghost = a or {}\n"
                    "    r = lambda fid: ghost[fid]\n"
                    "    return corpus_io.fetch_drive_docx(r, p, '/t')\n")
    check("C9 sees through `y = <defaulted param> or {}` — an assignment is not a "
          "producer when it only rebinds an empty default", rc == 1 and '[C9]' in out)

    r = subprocess.run([sys.executable, here], capture_output=True, text=True)
    check("live corpus passes the full-corpus run (C4 included)",
          r.returncode == 0 and '0 findings' in r.stdout)

    print(f"audit_callgraph self-test: {passed} passed, {len(fails)} failed"
          + (" — " + "; ".join(fails) if fails else ""))
    return not fails


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    sys.exit(main(sys.argv))
