"""spec_name_audit.py v1.0 — cross-block undefined-name auditor for spec-inline python.

THE GAP THIS CLOSES (GAP-2026-08-12-SPEC-INLINE-NAME-AUDIT). The framework's
Framework_*.md specs carry ```python blocks that a session executes
sequentially, notebook-cell style: a name bound in an earlier block is
readable in every later one. validate_framework_md.py Check B parses each
block for SYNTAX only, and Check AJ's undefined-name scan covers only the
.py engine files — so a name READ in spec-inline code that is bound in NO
earlier block was invisible to every automated check in this repo. That is
exactly how GAP-2026-08-12-S13-4-UNDEFINED-BATCHES-COMPLETED (a NameError
on every Final Assembly run) survived 7+ releases: nothing EXECUTES or
name-flow-analyses the .md blocks. This tool is the missing analysis.

WHAT IT DOES. For each spec file: extract every ```python fence in file
order, dedent, apply the same placeholder substitutions Check B uses,
ast-parse, and simulate sequential execution — collecting names BOUND at
each block's top level (assignments incl. tuple/star targets, aug/ann-
assign, walrus, imports, def/class, for/with/except targets, global) and
names READ (Load ctx), with function/lambda/comprehension scopes handled
correctly (their params/targets are local; their free reads count against
the enclosing block). Any read of a name never bound by an earlier-or-same
block and not a builtin is a FINDING. Reads inside try/except blocks whose
handlers catch NameError/Exception/bare are exempt (a real framework idiom
for optional names).

WHAT A FINDING MEANS — READ THIS BEFORE "FIXING". File order approximates
but does not equal execution order, and the specs deliberately contain
three legitimate finding-producing shapes: (1) ILLUSTRATIVE FRAGMENTS /
USAGE DOCS (a snippet showing an API call, inputs defined in prose);
(2) PROSE-CONTRACT INPUTS (a block whose comment documents "counts[sid] =
..." as the session's obligation to compute first); (3) SESSION/TRIGGER-
PROVIDED NAMES (EXAM, N, LEVEL... bound by the step trigger, not by any
block). A finding is therefore a LEAD, not automatically a bug — but every
CONFIRMED bug of this class (batches_completed; bc read at S3-17b before
its S7 import; axis1_paper_counts never initialised; sys.exit with sys
never imported) was found by exactly this analysis. Hence the BASELINE
RATCHET below: triaged findings are frozen in spec_name_audit_baseline.json
and CI fails only on NEW findings, so this class of bug can never silently
enter the corpus again, while known-benign shapes stay documented, not
erased.

USAGE
    python3 spec_name_audit.py Framework_*.md
        Report all findings (human triage mode).
    python3 spec_name_audit.py --write-baseline BASELINE.json Framework_*.md
        Freeze current findings as the accepted baseline.
    python3 spec_name_audit.py --check-baseline BASELINE.json Framework_*.md
        Exit 1 if any finding is NOT in the baseline (the CI ratchet).
        A finding that DISAPPEARS is reported as fixed (informational).
    python3 spec_name_audit.py --self-test
        Run the embedded fixture suite (includes the batches_completed-
        shaped calibration fixture: the buggy shape MUST be flagged, the
        fixed shape MUST NOT).

Tracked, repo-level auditor — NOT routed to any trigger (same standing as
validate_framework_md.py / notes_sync_audit.py). Stdlib only.
"""
import ast
import builtins
import json
import os
import re
import sys
import textwrap

BUILTINS = set(dir(builtins)) | {'__name__', '__file__', '__doc__'}


# ───────────────────────── block extraction ─────────────────────────
def extract_blocks(md_text):
    """Return [(md_lineno_of_first_code_line, dedented_source), ...] for
    every ```python fence, in file order."""
    lines = md_text.split('\n')
    out, i = [], 0
    while i < len(lines):
        if lines[i].strip() == '```python':
            j = i + 1
            while j < len(lines) and lines[j].strip() != '```':
                j += 1
            out.append((i + 2, textwrap.dedent('\n'.join(lines[i + 1:j]))))
            i = j + 1
        else:
            i += 1
    return out


def substitute_placeholders(src):
    """Same placeholder handling as validate_framework_md.py Check B."""
    src = re.sub(r'\[ExamCode\]', 'EXAMCODE', src)
    src = re.sub(r'\[N\]', 'NNN', src)
    src = re.sub(r'\[ExamName\]', 'EXAMNAME', src)
    src = re.sub(r'<<[^>]+>>', 'PLACEHOLDER_URL', src)
    return src


# ───────────────────────── scope analysis ─────────────────────────
def _target_names(t):
    out = set()
    if isinstance(t, ast.Name):
        out.add(t.id)
    elif isinstance(t, (ast.Tuple, ast.List)):
        for e in t.elts:
            out |= _target_names(e)
    elif isinstance(t, ast.Starred):
        out |= _target_names(t.value)
    return out


def _function_free_reads(fn):
    """Names read inside a function/lambda body that are not its params or
    locals — these count as reads of the enclosing block scope."""
    params = set()
    a = fn.args
    for p in a.posonlyargs + a.args + a.kwonlyargs:
        params.add(p.arg)
    if a.vararg:
        params.add(a.vararg.arg)
    if a.kwarg:
        params.add(a.kwarg.arg)
    body = fn.body if isinstance(fn.body, list) else [ast.Expr(fn.body)]
    mod = ast.Module(body=body, type_ignores=[])
    local = set(params)
    for node in ast.walk(mod):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            local.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            local.add(node.name)
            # A NESTED function's own parameters are bound in ITS scope, not free reads
            # of the enclosing block. Without this, every closure that uses its own
            # arguments — `def make_x(cache):  def inner(fid, page_token=None): ...` —
            # reported `fid` and `page_token` as unbound names of the outer block.
            # Found 2026-08-15 while making Framework_MockTestAnalyse's S1-1 fence
            # inspectable for the first time (GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION):
            # the pattern had always been a false positive, and was simply never reached
            # because the fences that contained it did not compile.
            # Outer-scope names read inside the nested body still count, which is the
            # whole point of the check and is unaffected.
            if not isinstance(node, ast.ClassDef):
                _a = node.args
                for _p in _a.posonlyargs + _a.args + _a.kwonlyargs:
                    local.add(_p.arg)
                if _a.vararg:
                    local.add(_a.vararg.arg)
                if _a.kwarg:
                    local.add(_a.kwarg.arg)
        elif isinstance(node, ast.Lambda):
            _a = node.args
            for _p in _a.posonlyargs + _a.args + _a.kwonlyargs:
                local.add(_p.arg)
            if _a.vararg:
                local.add(_a.vararg.arg)
            if _a.kwarg:
                local.add(_a.kwarg.arg)
        elif isinstance(node, ast.comprehension):
            local |= _target_names(node.target)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for al in node.names:
                local.add((al.asname or al.name).split('.')[0])
        elif isinstance(node, ast.ExceptHandler) and node.name:
            local.add(node.name)
    reads = []
    for node in ast.walk(mod):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) \
                and node.id not in local:
            reads.append((node.id, getattr(node, 'lineno', 0)))
    return reads


class _BlockScope(ast.NodeVisitor):
    """Names bound at block top level + free reads, for one code block."""

    def __init__(self):
        self.bound = set()
        self.reads = []          # (name, block_lineno, inside_guard)
        self._guard_depth = 0

    def _bind(self, t):
        if isinstance(t, ast.Name):
            self.bound.add(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            for e in t.elts:
                self._bind(e)
        elif isinstance(t, ast.Starred):
            self._bind(t.value)

    def visit_Assign(self, n):
        self.visit(n.value)
        for t in n.targets:
            if isinstance(t, (ast.Attribute, ast.Subscript)):
                self.visit(t)
            else:
                self._bind(t)

    def visit_AugAssign(self, n):
        self.visit(n.value)
        if isinstance(n.target, ast.Name):
            self.reads.append((n.target.id, n.lineno, self._guard_depth > 0))
            self.bound.add(n.target.id)
        else:
            self.visit(n.target)

    def visit_AnnAssign(self, n):
        if n.value:
            self.visit(n.value)
        if isinstance(n.target, ast.Name):
            self.bound.add(n.target.id)
        else:
            self.visit(n.target)

    def visit_NamedExpr(self, n):
        self.visit(n.value)
        self._bind(n.target)

    def visit_Import(self, n):
        for a in n.names:
            self.bound.add((a.asname or a.name).split('.')[0])

    def visit_ImportFrom(self, n):
        for a in n.names:
            self.bound.add(a.asname or a.name)

    def visit_FunctionDef(self, n):
        for d in n.decorator_list:
            self.visit(d)
        for dflt in list(n.args.defaults) + [d for d in n.args.kw_defaults if d]:
            self.visit(dflt)
        self.bound.add(n.name)
        for name, ln in _function_free_reads(n):
            self.reads.append((name, ln, self._guard_depth > 0))

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Lambda(self, n):
        for name, ln in _function_free_reads(n):
            self.reads.append((name, ln, self._guard_depth > 0))

    def visit_ClassDef(self, n):
        for d in n.decorator_list:
            self.visit(d)
        for b in n.bases:
            self.visit(b)
        self.bound.add(n.name)
        for stmt in n.body:
            self.visit(stmt)

    def visit_For(self, n):
        self.visit(n.iter)
        self._bind(n.target)
        for s in n.body + n.orelse:
            self.visit(s)

    visit_AsyncFor = visit_For

    def visit_With(self, n):
        for item in n.items:
            self.visit(item.context_expr)
            if item.optional_vars:
                self._bind(item.optional_vars)
        for s in n.body:
            self.visit(s)

    visit_AsyncWith = visit_With

    def visit_Try(self, n):
        guards = any(h.type is None for h in n.handlers) or any(
            h.type is not None and (
                (isinstance(h.type, ast.Name)
                 and h.type.id in ('NameError', 'Exception'))
                or (isinstance(h.type, ast.Tuple) and any(
                    isinstance(e, ast.Name)
                    and e.id in ('NameError', 'Exception')
                    for e in h.type.elts)))
            for h in n.handlers)
        if guards:
            self._guard_depth += 1
        for s in n.body:
            self.visit(s)
        if guards:
            self._guard_depth -= 1
        for h in n.handlers:
            if h.name:
                self.bound.add(h.name)
            for s in h.body:
                self.visit(s)
        for s in n.orelse + n.finalbody:
            self.visit(s)

    def _comp(self, n):
        local = set()
        for gen in n.generators:
            self.visit(gen.iter)
            local |= _target_names(gen.target)
        reads_before = len(self.reads)
        for gen in n.generators:
            for cond in gen.ifs:
                self.visit(cond)
        if isinstance(n, ast.DictComp):
            self.visit(n.key)
            self.visit(n.value)
        else:
            self.visit(n.elt)
        # comprehension targets are scope-local: reads of them recorded
        # during the body visit must not leak to the cross-block filter
        self.reads = self.reads[:reads_before] + [
            r for r in self.reads[reads_before:] if r[0] not in local]

    visit_ListComp = visit_SetComp = _comp
    visit_GeneratorExp = visit_DictComp = _comp

    def visit_Global(self, n):
        for name in n.names:
            self.bound.add(name)

    def visit_Name(self, n):
        if isinstance(n.ctx, ast.Load):
            self.reads.append((n.id, n.lineno, self._guard_depth > 0))
        elif isinstance(n.ctx, (ast.Store, ast.Del)):
            self.bound.add(n.id)


def audit_text(md_text):
    """Return [(md_lineno, name), ...] — first occurrence per unique name."""
    session_bound = set()
    findings, seen = [], set()
    for md_line, raw in extract_blocks(md_text):
        src = substitute_placeholders(raw)
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue        # syntax is Check B's jurisdiction
        sc = _BlockScope()
        for stmt in tree.body:
            sc.visit(stmt)
        for name, ln, guarded in sc.reads:
            if guarded or name in BUILTINS or name in session_bound \
                    or name in sc.bound or name in seen:
                continue
            seen.add(name)
            findings.append((md_line + ln - 1, name))
        session_bound |= sc.bound
    return findings


def audit_file(path):
    return audit_text(open(path, encoding='utf-8').read())


# ───────────────────────── baseline ratchet ─────────────────────────
# TYPED BASELINE — GAP-2026-08-16-BASELINE-SUPPRESSED-NAMEERRORS.
#
# The baseline used to be {spec: [name, ...]}. A bare name asserts only "this is
# unbound and that is accepted", and TWO completely different facts hide under that
# sentence:
#
#   (a) the name is an INPUT to an illustrative fragment a reader supplies mentally
#       — legitimately unbound, forever; and
#   (b) the name is READ inside a real `def` that the pipeline CALLS — a guaranteed
#       NameError the moment that function runs.
#
# The flat list could not tell them apart, so (b) kept being accepted as (a). It hid
# `collections` and `present_files` (P1 and P3 of
# GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE) for eleven and ten days, and then hid
# `n_vision` and `options_count` through the release that fixed those two — because
# `--write-baseline` re-freezes whatever is currently unbound, including defects the
# previous run introduced. A ratchet wired to a detector, with a switch in between
# that silently accepts everything the detector finds, is not a ratchet.
#
# So every entry now carries a REASON from a closed vocabulary, and one class cannot
# be baselined at any price.
REASONS = {
    'illustrative':   'input to a documented pseudocode/illustrative fragment; no '
                      'executable caller exists',
    'session_global': 'bound by the model at session start, outside compiling python; '
                      'MUST name the section that binds it',
    'model_performed':'a CLASS: T tool call the model performs in its own turn',
    'forward_ref':    'bound by a later fence that executes before any caller runs',
}
UNBASELINEABLE = 'read_in_called_function'
# The ONE reason that names existing debt rather than excusing it. It may never be
# WRITTEN by --write-baseline; it can only be placed by hand and can only be removed.
# Every entry carrying it is a guaranteed NameError somebody has signed for, listed in
# the baseline's own _grandfathered block, and visible in every CI run's summary.
GRANDFATHERED = 'GRANDFATHERED_MUST_FIX'


def load_baseline(path):
    """Accept the typed form; migrate the legacy flat form in memory.

    Legacy {spec: [name]} is read as {spec: {name: {'reason': None}}} so an existing
    baseline keeps working, but an untyped entry can never be WRITTEN again.
    """
    raw = json.load(open(path, encoding='utf-8'))
    out = {}
    for spec, v in raw.items():
        if spec.startswith('_'):
            continue
        if isinstance(v, list):
            out[spec] = {n: {'reason': None} for n in v}
        else:
            out[spec] = {n: (e if isinstance(e, dict) else {'reason': e})
                         for n, e in v.items()}
    return out


def classify(spec, name):
    """Is this name READ inside a function the spec itself calls?

    That is the one class that may never be baselined: it is not a judgement call
    about intent, it is a statement about what python will do.
    """
    try:
        blocks = extract_blocks(open(spec, encoding='utf-8').read())
    except OSError:
        return None
    # MODULE-SCOPE BINDING, ACROSS ALL FENCES.
    #
    # audit_text() models SEQUENTIAL execution: a name is unbound if nothing has bound
    # it YET at the point of use. That is the right model for top-level statements and
    # the wrong one for FUNCTION BODIES, which do not run until every fence has
    # executed. §3's process_pyq_paper() calling §5's tag_axes() is a forward
    # reference, not a defect — which is why the baseline legitimately holds names
    # like tag_axes, extract_presorted and save_progress.
    #
    # So the unbaselineable class is narrower than "audit_text reported it": the name
    # must ALSO be bound nowhere at module scope in ANY fence. Getting this wrong in
    # the strict direction is not harmless — a refusal rule that cries wolf on 37
    # names, most of them fine, is one somebody switches off.
    module_bound, called, sites = set(), set(), []
    for start, src in blocks:
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                module_bound.add(n.name)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for a in n.names:
                    module_bound.add((a.asname or a.name).split('.')[0])
            else:
                for x in ast.walk(n):
                    if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store):
                        module_bound.add(x.id)
        for a in ast.walk(tree):
            if isinstance(a, ast.Call) and isinstance(a.func, ast.Name):
                called.add(a.func.id)
        for top in tree.body:
            if not isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            local = set()
            for a in ast.walk(top):
                if isinstance(a, ast.Name) and isinstance(a.ctx, ast.Store):
                    local.add(a.id)
                if isinstance(a, ast.arg):
                    local.add(a.arg)
                if isinstance(a, (ast.Import, ast.ImportFrom)):
                    for al in a.names:
                        local.add((al.asname or al.name).split('.')[0])
                if isinstance(a, (ast.FunctionDef, ast.AsyncFunctionDef)) and a is not top:
                    local.add(a.name)
            if name in local:
                continue
            for a in ast.walk(top):
                if isinstance(a, ast.Name) and a.id == name and isinstance(a.ctx, ast.Load):
                    sites.append((top.name, start + a.lineno))
    if name in module_bound:
        return None                     # forward reference; bound before any call
    for fn, ln in sites:
        if fn in called:
            return (fn, ln)
    return None


def write_baseline(path, per_file, reasons=None):
    """Write the TYPED baseline. REFUSES to accept the unbaselineable class.

    This is the whole mechanism. `--write-baseline` is the move that converted every
    detection into an acceptance, so it is the move that has to say no.
    """
    reasons = reasons or {}
    existing, meta = {}, {}
    if os.path.exists(path):
        try:
            existing = load_baseline(path)
            # PRESERVE THE HEADER. load_baseline drops '_'-prefixed keys because they
            # are not spec entries; writing `data` alone would therefore destroy
            # _schema, _policy and — worst of all — the _grandfathered record, which is
            # the only human-readable list of signed-for debt. A baseline writer that
            # silently erases the record of what it is carrying is the exact failure
            # this file exists to prevent.
            raw = json.load(open(path, encoding='utf-8'))
            meta = {k: v for k, v in raw.items() if k.startswith('_')}
        except Exception:                                   # noqa: BLE001
            existing, meta = {}, {}
    refused = []
    data = {}
    for f, finds in sorted(per_file.items()):
        if not finds:
            continue
        # ONE dict per file, built in place. An earlier version accumulated
        # grandfathered names into `data[f]` and everything else into a separate
        # `entry`, then did `data[f] = entry` — which overwrote the grandfathered
        # names and dropped them from the baseline silently. The next --check-baseline
        # then failed on them as NEW findings, and the debt record was gone.
        entry = data.setdefault(f, {})
        for name in sorted({n for _, n in finds}):
            hit = classify(f, name)
            prior_reason = (existing.get(f, {}).get(name) or {}).get('reason')
            if hit and prior_reason != GRANDFATHERED:
                refused.append((f, name, hit[0], hit[1]))
                continue
            if hit:
                # Signed-for debt: carried verbatim, never silently re-created.
                entry[name] = {'reason': GRANDFATHERED,
                               'site': f'{hit[0]}() L{hit[1]}'}
                continue
            prior = existing.get(f, {}).get(name) or {}
            reason = reasons.get((f, name)) or prior.get('reason')
            entry[name] = {'reason': reason}
        if not entry:
            del data[f]
    if refused:
        print('SPEC-NAME-AUDIT: REFUSING to write the baseline.\n')
        print(f'{len(refused)} name(s) are READ inside a function this spec CALLS. '
              f'Each is a guaranteed NameError\nwhen that function runs, so none of '
              f'them may be baselined at any price:\n')
        for f, name, fn, ln in refused:
            print(f'  {f} L{ln}: {name}  (read in {fn}(), which this spec calls)')
        print('\nFix the binding. If you believe one of these is genuinely '
              'unreachable, make that\ntrue in the spec — delete the dead function or '
              'mark the fragment as pseudocode —\nrather than asserting it here.')
        return None
    missing = [(f, n) for f, e in data.items() for n, v in e.items() if not v.get('reason')]
    # Rebuild _grandfathered from what is ACTUALLY in the file, so the human-readable
    # record can never drift from the machine-readable entries.
    meta['_grandfathered'] = sorted(
        f"{f}: {n} — {v.get('site', 'site unrecorded')}"
        for f, e in data.items() for n, v in e.items()
        if v.get('reason') == GRANDFATHERED)
    meta.setdefault('_schema', 'TYPED BASELINE v2 — every entry carries a reason. '
                               'See spec_name_audit.py REASONS.')
    meta.setdefault('_policy', 'A name READ inside a function this spec CALLS may NEVER '
                               'be baselined. --write-baseline refuses to create such an '
                               'entry. The only exception is GRANDFATHERED_MUST_FIX, '
                               'which must be placed BY HAND, is listed in '
                               '_grandfathered, and can only be removed — never added '
                               'by tooling.')
    out = dict(meta)
    out.update(data)
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1, sort_keys=True)
    if missing:
        print(f'NOTE: {len(missing)} entry(ies) carry no reason yet. Add one from '
              f'{sorted(REASONS)}:')
        for f, n in missing[:20]:
            print(f'  {f}: {n}')
    return data


def check_baseline(baseline, per_file):
    """Return (new, fixed): findings not in baseline / baseline entries gone."""
    new, fixed = [], []
    for f, finds in per_file.items():
        allowed = set(baseline.get(f, {}))     # typed baseline: dict keyed by name
        for ln, name in finds:
            if name not in allowed:
                new.append((f, ln, name))
    for f, names in baseline.items():
        current = {n for _, n in per_file.get(f, [])}
        for name in names:                      # dict iteration yields the names
            if name not in current:
                fixed.append((f, name))
    return new, fixed


# ───────────────────────── self-test ─────────────────────────
_FIXTURE_BUGGY = '''
Header prose.
```python
bs = json.load(open('state.json'))
```
More prose.
```python
commit(batches_completed=len(batches_completed))
```
'''

_FIXTURE_FIXED = '''
```python
bs = json.load(open('state.json'))
batches_completed = len(bs.get('batches_completed', []))
```
```python
commit(batches_completed=batches_completed)
```
'''

_FIXTURE_SHAPES = '''
```python
import os
paths = [p for p in os.listdir('.')]
labels = {k: v for k, v in mapping.items()}
def helper(x):
    return x + offset
total = sum(n for n in paths)
try:
    maybe = optional_name
except NameError:
    maybe = None
with open('f') as fh:
    data = fh.read()
for row in data:
    last = row
q = last
```
'''


def self_test():
    passed = total = 0
    fails = []

    def check(name, cond):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
        else:
            fails.append(name)

    # ── TYPED-BASELINE ROUND TRIP ────────────────────────────────────────────
    # Three defects shipped in the first cut of the typed baseline and were caught
    # only by hand-review before deploy. Each is pinned here, because all three had
    # the same shape: the writer SILENTLY DESTROYED the record it exists to keep.
    #   1. `data[f] = entry` overwrote grandfathered names accumulated via setdefault,
    #      so signed-for debt vanished and the next --check-baseline failed on it.
    #   2. '_'-prefixed metadata (_schema/_policy/_grandfathered) was dropped on write.
    #   3. main() called .values() on the None a refusal returns → AttributeError
    #      traceback burying the refusal message that had just been printed.
    import tempfile as _tf
    _fx_dir = _tf.mkdtemp()
    _spec = os.path.join(_fx_dir, 'Framework_ZZTest.md')
    # `helper` is read inside caller(), and caller() is called -> UNBASELINEABLE.
    # `later_ref` is read in a function but bound at module scope in a later fence
    # -> a legitimate forward reference that must NOT be refused.
    open(_spec, 'w', encoding='utf-8').write(
        '```python\n'
        'def caller():\n'
        '    return helper(1)\n'
        'def uses_forward():\n'
        '    return later_ref\n'
        'caller()\n'
        'uses_forward()\n'
        '```\n\n'
        '```python\n'
        'later_ref = 3\n'
        '```\n')
    _per = {_spec: audit_file(_spec)}
    _bpath = os.path.join(_fx_dir, 'b.json')

    check('refusal_returns_None_not_a_dict', write_baseline(_bpath, _per) is None)
    check('refusal_writes_nothing', not os.path.exists(_bpath))

    # Hand-place the grandfather + metadata, exactly as an operator would.
    json.dump({'_schema': 'x', '_policy': 'y', '_grandfathered': [],
               os.path.basename(_spec): {}},
              open(_bpath, 'w', encoding='utf-8'))
    json.dump({'_schema': 'x', '_policy': 'y', '_grandfathered': [],
               _spec: {'helper': {'reason': GRANDFATHERED}}},
              open(_bpath, 'w', encoding='utf-8'))
    _d = write_baseline(_bpath, _per)
    check('grandfathered_lets_write_proceed', _d is not None)
    if _d is not None:
        _after = json.load(open(_bpath, encoding='utf-8'))
        _entry = _after.get(_spec, {})
        check('grandfathered_entry_survives_write',
              _entry.get('helper', {}).get('reason') == GRANDFATHERED)
        check('forward_ref_not_refused', 'later_ref' in _entry)
        check('metadata_keys_survive_write',
              {'_schema', '_policy', '_grandfathered'} <= set(_after))
        check('grandfathered_record_rebuilt',
              len(_after.get('_grandfathered', [])) == 1)
    import shutil as _sh
    _sh.rmtree(_fx_dir, ignore_errors=True)

    # calibration: the exact bug shape this tool exists to catch
    buggy = audit_text(_FIXTURE_BUGGY)
    check('calibration_buggy_shape_flagged',
          any(n == 'batches_completed' for _, n in buggy))
    fixed = audit_text(_FIXTURE_FIXED)
    check('calibration_fixed_shape_clean',
          not any(n == 'batches_completed' for _, n in fixed))

    # scope shapes that must NOT false-positive
    shapes = audit_text(_FIXTURE_SHAPES)
    names = {n for _, n in shapes}
    check('comprehension_target_not_flagged', 'p' not in names and 'k' not in names
          and 'v' not in names and 'n' not in names)
    check('function_param_not_flagged', 'x' not in names)
    check('with_target_not_flagged', 'fh' not in names)
    check('for_target_not_flagged', 'row' not in names)
    check('cross_statement_binding_seen', 'last' not in names and 'q' not in names)
    check('nameerror_guard_exempts_read', 'optional_name' not in names)

    # ...and the ones that MUST be flagged in the same fixture
    check('true_unbound_mapping_flagged', 'mapping' in names)
    check('function_free_read_flagged', 'offset' in names)

    # cross-block persistence: import in block 1 readable in block 2
    two = audit_text('```python\nimport json\n```\n```python\nd = json.loads("{}")\n```')
    check('cross_block_import_persists', not any(n == 'json' for _, n in two))

    # sequential order matters: read-before-bind across blocks IS flagged
    ooo = audit_text('```python\nuse(thing)\n```\n```python\nthing = 1\n```')
    check('read_before_later_bind_flagged', any(n == 'thing' for _, n in ooo))

    # baseline ratchet mechanics
    per_file = {'A.md': [(10, 'alpha'), (20, 'beta')]}
    base = {'A.md': ['alpha']}
    new, fixed_entries = check_baseline(base, per_file)
    check('baseline_new_finding_detected',
          new == [('A.md', 20, 'beta')])
    base2 = {'A.md': ['alpha', 'beta', 'gone']}
    new2, fixed2 = check_baseline(base2, per_file)
    check('baseline_fixed_finding_reported',
          new2 == [] and fixed2 == [('A.md', 'gone')])

    # syntax-error blocks are skipped (Check B's jurisdiction), not fatal
    syn = audit_text('```python\ndef broken(:\n```\n```python\nok = 1\n```')
    check('syntax_error_block_skipped_not_fatal', isinstance(syn, list))

    # placeholder substitution mirrors Check B
    ph = audit_text('```python\nx = f"/tmp/[ExamCode]_M[N].json"\n```')
    check('placeholders_substituted', not any(n in ('ExamCode', 'N') for _, n in ph))

    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


# ───────────────────────── CLI ─────────────────────────
def main(argv):
    if '--self-test' in argv:
        return 0 if self_test() else 1

    write_to = check_to = None
    files = []
    i = 0
    while i < len(argv):
        if argv[i] == '--write-baseline':
            write_to = argv[i + 1]; i += 2
        elif argv[i] == '--check-baseline':
            check_to = argv[i + 1]; i += 2
        else:
            files.append(argv[i]); i += 1

    if not files:
        print(__doc__)
        return 2

    per_file = {f: audit_file(f) for f in files}

    if write_to:
        data = write_baseline(write_to, per_file)
        if data is None:
            # REFUSED. write_baseline has already printed which names and why; exit
            # non-zero on the refusal itself rather than on an AttributeError, so the
            # message is the last thing a CI log shows instead of a traceback burying it.
            return 1
        n = sum(len(v) for v in data.values())
        g = sum(1 for e in data.values() for v in e.values()
                if v.get('reason') == GRANDFATHERED)
        print(f"BASELINE WRITTEN: {write_to} — {n} accepted finding(s) "
              f"across {len(data)} file(s)"
              + (f", {g} GRANDFATHERED_MUST_FIX carried" if g else ""))
        return 0

    if check_to:
        # A CI misconfiguration must produce a diagnosis, not a traceback: the whole
        # point of this tool is that failures are legible at the moment they happen.
        if not os.path.exists(check_to):
            print(f"SPEC-NAME-AUDIT: baseline not found: {check_to}\n"
                  f"  Create it with --write-baseline, or correct the path.")
            return 2
        try:
            baseline = load_baseline(check_to)
        except (json.JSONDecodeError, ValueError, AttributeError) as exc:
            print(f"SPEC-NAME-AUDIT: baseline is not readable JSON: {check_to}\n"
                  f"  {exc}\n"
                  f"  Refusing to run: an unreadable baseline cannot be distinguished "
                  f"from an EMPTY one, and treating it as empty would silently accept "
                  f"every finding in the corpus.")
            return 2
        new, fixed = check_baseline(baseline, per_file)
        for f, name in fixed:
            print(f"FIXED (remove from baseline when convenient): {f}: {name}")
        if new:
            print(f"SPEC-NAME-AUDIT: {len(new)} NEW unbound-name finding(s) "
                  f"not in baseline — the batches_completed class:")
            for f, ln, name in new:
                print(f"  {f} L{ln}: {name}")
            print("Either bind the name in an earlier-or-same block (the fix), "
                  "or — only for a triaged illustrative fragment / prose-contract "
                  "input — regenerate the baseline with --write-baseline.")
            return 1
        print(f"SPEC-NAME-AUDIT: OK — no new findings across {len(files)} file(s) "
              f"({sum(len(v) for v in per_file.values())} baselined).")
        return 0

    total = 0
    for f in files:
        finds = per_file[f]
        if finds:
            print(f"\n{f}: {len(finds)} unique unbound name(s)")
            for ln, name in finds:
                print(f"  L{ln}: {name}")
            total += len(finds)
    print(f"\nTOTAL unique findings: {total}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
