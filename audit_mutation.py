#!/usr/bin/env python3
"""
AUDIT MUTATION — mechanical hollow-branch detector for the EXAM auditor AND for
the REPO AUDITORS (the gates that guard the corpus itself).

WHY THIS EXISTS
───────────────
This corpus has now recorded EIGHT occurrences of the same defect class: a code
path that ships, reports green, and is never actually exercised by any fixture.

    v2.10  `bc` read at three sites, bound at none
    v2.12  A-FIGPROFILE primary branch never executed by any fixture
    v2.13  Block.images never populated — no fixture put an image in a block
    v2.15  unknown-schema guard deletable with every fixture still green
    v2.16  no fixture had ever simulated a vision outage
    v2.20  the `exam` leg of the identity triple never passed by the call site
    v2.21  no dossier fixture ever rendered a non-text option; the "lock"
           fixture was a TAUTOLOGY (f(x) == <inline body of f>)
    v2.21.1 the A-DOSSIER nat leg was clamped on an assumption R13 forbids

Every one of them was found by a HUMAN READING CODE, after shipping. Reading is
not a control: a green self-test is exactly what a hollow branch looks like.
CHECK AO catches the tautology SHAPE; it cannot catch a finding that is simply
never triggered. This tool catches that, mechanically and deterministically.

WHAT IT DOES
────────────
For every finding emission in the engine (a `bad.append(...)`-class statement —
the moment a gate decides something is wrong), it produces a MUTANT with that
one statement neutralised, then runs `--self-test` against the mutant.

    mutant KILLED   → some fixture noticed the finding disappear. The logic is
                      genuinely covered.
    mutant SURVIVED → NO fixture can tell the difference between a gate that
                      reports this defect and a gate that does not. The finding
                      is UNTESTED. It may be correct; nothing proves it is, and
                      nothing would notice if a future edit broke it.

A surviving mutant is not automatically a bug. It is an ABSENCE OF EVIDENCE, and
this corpus's own history says absence of evidence is where the bugs live.

USAGE
─────
    python3 audit_mutation.py                    # full run
    python3 audit_mutation.py --gate gate_dossier   # one function
    python3 audit_mutation.py --max-survivors 16    # CI budget; exit 1 if over

EXIT CODES
──────────
    0  survivors <= budget (default: no budget, always 0 unless --max-survivors)
    1  survivors exceed the declared budget → the release added an untested finding

RELEASE POLICY (spec §21): the survivor count MUST NOT INCREASE release over
release. A new gate ships with fixtures that kill its own mutants, or it does not
ship. Ratcheting the budget DOWN is the mechanism by which the estate's 16
inherited survivors get retired one release at a time.
"""
import argparse
import ast
import os
import re
import subprocess
import sys
import concurrent.futures
import json
import queue
import shutil
import tempfile

ENGINE_DEFAULT = 'audit_canonical.py'

# ── GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, deployment review ────────────────
# THIS TOOL HAS NEVER COVERED THE REPO AUDITORS, AND THAT IS HOW FIVE UNTESTED
# GATES SHIPPED. Release 2026.08.15.9 added C10, C11, MS-12, MS-13 and
# SPEC-BUDGET. Every one of them survived deletion: gut the check to `return []`
# and audit_callgraph stayed 23/23, mock_sync_audit 29/29, audit_specs_ext 6/6.
# audit_mutation reported 35/35 killed, 100%, through that release — because
# ENGINE_DEFAULT is audit_canonical.py, the EXAM auditor, and the repo auditors
# were simply outside its universe. The tool was working perfectly on a target
# that did not include the thing that broke.
#
# THREE THINGS BLOCKED IT, and none of them was the mutation engine:
#   1. EMIT_RE knew `bad.append(`-class names only. The repo auditors emit via
#      `problems.append(`, `add(...)` and `rec(...)`.
#   2. Greenness was decided by `'PASS' in tail`. Most repo auditors print
#      "N passed, 0 failed" — no uppercase PASS — so the BASELINE check judged a
#      perfectly healthy auditor as failing and aborted with exit 2 before
#      testing a single mutant.
#   3. Mutants ran in a bare tempdir holding one file. audit_canonical.py is
#      self-contained; a repo auditor READS THE CORPUS, so in a bare tempdir its
#      "live corpus" fixtures pass vacuously against zero files and every mutant
#      survives for the wrong reason.
# All three are fixed below. The mutation logic itself is unchanged.

# Repo auditors, with the per-engine survivor budget CI ratchets DOWN. A budget
# is a debt, never an allowance: the only legitimate edit is a decrease.
AUDITOR_BUDGETS_FILE = 'MUTATION_BUDGETS.json'

# An emitter is the statement where a gate DECIDES something is wrong. Names are
# an explicit allowlist, not a pattern: `out.append(` in a collector helper is
# not a finding, and mutating it would produce a survivor that means nothing.
EMITTER_NAMES = ('bad', 'bad_[a-z_]+', 'figtext_prose', 'composite',
                 'multi_per_line', 'math_raster', 'warn_view', 'bad_opt',
                 'bad_grade', 'issues', 'findings', 'problems')
EMITTER_CALLS = ('add', 'rec')

# A "finding emission" is the statement where a gate records that something is
# wrong. Neutralising it makes the gate silently accept the defect it exists to
# catch — which is precisely the condition a fixture is supposed to notice.
EMIT_RE = re.compile(
    r'^(?:(?:' + '|'.join(EMITTER_NAMES) + r')\.append\(|'
    r'(?:' + '|'.join(EMITTER_CALLS) + r')\()'
)


# ─────────────────── PIPELINE ENGINES (Wave 2 Part C B4) ────────────────────
# audit_mutation was built for AUDITORS: it neutralises a FINDING EMISSION and asks
# whether a fixture notices. Pointed at analyse_engine.py — 4,847 lines of Step 5
# pipeline — it reports `0 emission(s)`, because a pipeline does not emit findings; it
# computes values. So the corpus's largest new engine sat OUTSIDE the mutation gate
# while CI reported 100%.
#
# That is precisely the failure this file's own budget doc describes: "The tool was
# working perfectly on a target that did not include the thing that broke."
#
# A pipeline's equivalent of a neutralised gate is a DECISION SILENTLY CHANGED. The
# rules below are not a generic operator sweep — each one reproduces a defect class
# this corpus has ACTUALLY SHIPPED, which is why the gate is worth its runtime:
#
#   sorted( -> list(        GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE D4. Set order over
#                           str depends on PYTHONHASHSEED, so section_rules.md was never
#                           reproducible: same 433,260 bytes, different sha256, 34 lines
#                           differing. A fixture must span >1 value or it proves nothing.
#   raise -> pass           Guard removal. extract_shift_from_filename() raises when
#                           session_re is missing rather than guessing a keyword; a
#                           silent default mislabels every paper's shift — a WRONG
#                           ANSWER, not an error. Same shape as the v2.39 vision_pending
#                           accumulator guard.
#   .startswith( -> False   Branch removal. print_qv routes '_'-prefixed keys to the
#                           counter line instead of unpacking them; losing that branch
#                           IS defect D1, which stopped Step 5 emitting anything for
#                           eleven days.
#   return True -> False    Predicate inversion on a gate's verdict.
#
# --deep adds the generic operator flips (and/or, </<=, ==/!=): 451 further targets,
# ~7 minutes, and many are equivalent mutants. Useful on demand, deliberately NOT the
# CI gate — a slow gate with a high equivalent-mutant rate is one people learn to skip.
PIPELINE_RULES = [
    ('sorted->list',        re.compile(r'\bsorted\('),        'list('),
    ('raise->pass',         re.compile(r'^(\s*)raise\b'),      '\\1pass  #'),
    ('startswith->False',   re.compile(r'\.startswith\('),     None),
    ('returnTrue->False',   re.compile(r'^(\s*)return True\b'), '\\1return False'),
]
PIPELINE_DEEP = [
    ('and->or',   re.compile(r'\band\b'), 'or'),
    ('or->and',   re.compile(r'\bor\b'),  'and'),
    ('lt->le',    re.compile(r'(?<![<>=!])<(?!=)'), '<='),
    ('eq->ne',    re.compile(r'(?<![<>=!])==(?!=)'), '!='),
]


def find_pipeline_targets(lines, tree, only_gate=None, deep=False):
    """Decision points whose silent change is a real defect class."""
    rules = PIPELINE_RULES + (PIPELINE_DEEP if deep else [])
    out = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        fn = enclosing_function(tree, i + 1)
        if only_gate and fn != only_gate:
            continue
        # NEVER MUTATE THE TEST SCAFFOLDING. A mutated assertion fails trivially and
        # scores as KILLED, inflating the result while proving nothing about the code
        # the fixture is supposed to guard. Mirrors the existing self_test/test_/_test
        # exclusion the auditor path already applies.
        if fn.startswith(('self_test', 'test_', '_test')):
            continue
        for label, rx, repl in rules:
            if not rx.search(line):
                continue
            # VALIDATE THE MUTATION AT FIND TIME. A rule can match a line and still
            # produce no change (e.g. `sorted(` inside an f-string the sub does not
            # reach). Listing such a target and discovering it later means the run
            # either crashes or, worse, banks it as KILLED without ever mutating
            # anything — a survivor counted as a kill is the one outcome this whole
            # tool exists to prevent.
            if mutate_pipeline(lines, i, label) is None:
                continue
            out.append((i, fn, f'[{label}] {stripped[:70]}', label))
            break
    return out


def mutate_pipeline(lines, idx, label):
    """Apply the rule that matched, producing a semantically different pipeline."""
    mut = lines[:]
    line = mut[idx]
    for lab, rx, repl in PIPELINE_RULES + PIPELINE_DEEP:
        if lab != label:
            continue
        if lab == 'startswith->False':
            # Neutralise the CONDITION, not the call: `if k.startswith('_'):` -> `if False:`
            mut[idx] = re.sub(r'\b[\w\.\[\]\'\"]+\.startswith\([^)]*\)', 'False', line)
        elif lab == 'raise->pass':
            ind = len(line) - len(line.lstrip())
            mut[idx] = ' ' * ind + 'pass  # MUTANT (raise removed)'
        else:
            mut[idx] = rx.sub(repl, line, count=1)
        break
    if mut[idx] == line:                      # rule did not bite; skip rather than lie
        return None
    if not mut[idx].rstrip().endswith('# MUTANT (raise removed)'):
        mut[idx] = mut[idx].rstrip() + '  # MUTANT'
    return '\n'.join(mut)


def enclosing_function(tree, lineno):
    """Innermost function containing this line, for reporting."""
    best = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            end = node.end_lineno or node.lineno
            if node.lineno <= lineno <= end:
                if best is None or node.lineno > best.lineno:
                    best = node
    return best.name if best else '<module>'


def find_targets(lines, tree, only_gate=None):
    out = []
    for i, line in enumerate(lines):
        if not EMIT_RE.match(line.strip()):
            continue
        fn = enclosing_function(tree, i + 1)
        if only_gate and fn != only_gate:
            continue
        out.append((i, fn, line.strip()))
    return out


_FAILCOUNT_RE = re.compile(r'(\d+)\s+failed', re.I)
_RATIO_RE = re.compile(r'(\d+)\s*/\s*(\d+)\s+PASS')


def is_green(returncode, tail):
    """Did this suite report a clean run?

    ENGINE-AGNOSTIC ON PURPOSE. The old rule was `'PASS' in tail`, which is the
    audit_canonical.py banner and nothing else. Every repo auditor prints
    "N passed, 0 failed" instead, so the old rule judged all of them as FAILING
    and main() aborted at the baseline check with exit 2 — the tool never ran on
    them, and nobody noticed because nobody had pointed it at them.

    A non-zero exit is always a kill: a mutant that crashes the suite has been
    detected, if crudely. Beyond that, both reported shapes are parsed, and a
    suite whose banner cannot be parsed at all is treated as NOT green — an
    unreadable result must never be scored as a survivor, because a survivor is
    a claim about coverage and this tool would have no evidence for it.
    """
    if returncode != 0:
        return False
    m = _FAILCOUNT_RE.search(tail)
    if m:
        return int(m.group(1)) == 0
    m = _RATIO_RE.search(tail)
    if m:
        return m.group(1) == m.group(2)
    if 'PASS' in tail and 'FAIL' not in tail:
        return True
    return False


# PYTHONHASHSEED IS PINNED FOR EVERY MUTANT. GAP-2026-08-17-B4-MUTATION-FLAKE.
# Without it each mutant subprocess draws a FRESH random seed, so any fixture whose
# oracle depends on set-iteration order scores differently run to run. Measured on
# analyse_engine.py L451 (`'all_observed': sorted(set(fmts))`): the mutant survived
# 8 of 40 fresh processes — 20% — because with a three-element string set
# `list(set(...))` comes out already sorted often enough to satisfy the assertion.
#
# THE CONSEQUENCE IS WORSE THAN A WRONG NUMBER: it makes the BUDGET UNSTATABLE. 28 was
# too low one run in five, and 29 would be an INCREASE, which MUTATION_BUDGETS.json
# forbids in its own words. There is no lawful number for a nondeterministic gate —
# the nondeterminism has to go, not be renumbered.
#
# A fixed seed makes the score reproducible BY CONSTRUCTION, which is what the
# VERIFY-THE-VERIFIER LAW's serial==parallel clause asks for, generalised from
# processes to runs. This does NOT hide real ordering defects: the fixtures that
# detect them compare against an explicitly sorted expectation, so they fail under
# ANY seed. Pinning removes the coin-flip, not the check — and
# `--hash-seed random` is available to re-introduce the sweep deliberately.
HASH_SEED_DEFAULT = '0'


def run_self_test(path, cwd, hash_seed=HASH_SEED_DEFAULT):
    env = dict(os.environ)
    if str(hash_seed) == 'random':
        env.pop('PYTHONHASHSEED', None)
    else:
        env['PYTHONHASHSEED'] = str(hash_seed)
    try:
        r = subprocess.run([sys.executable, path, '--self-test'],
                           capture_output=True, text=True, cwd=cwd, timeout=900,
                           env=env)
    except subprocess.TimeoutExpired:
        return False, 'TIMEOUT'          # timeout counts as KILLED
    tail = r.stdout.strip().split('\n')[-1] if r.stdout.strip() else ''
    return is_green(r.returncode, tail), tail


def make_workdir(engine, repo_root):
    """A mutant of a REPO auditor must run against the REAL corpus.

    audit_canonical.py is self-contained and its fixtures are synthetic, so a
    tempdir holding one file was enough. A repo auditor READS Framework_*.md,
    routes.json and MANIFEST.json; in a bare tempdir its live-corpus fixtures
    pass vacuously against zero files, so EVERY mutant survives and the score is
    a fiction. Copy the corpus once per worker, then rewrite only the engine.
    """
    d = tempfile.mkdtemp(prefix='mut_')
    for name in os.listdir(repo_root):
        if name.startswith('.'):
            continue
        src = os.path.join(repo_root, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(d, name))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--engine', default=ENGINE_DEFAULT)
    ap.add_argument('--kind', choices=('auditor', 'pipeline'), default=None,
                    help='auditor: mutate finding emissions (default for auditors). '
                         'pipeline: mutate decision points — for engines that compute '
                         'values rather than emit findings. Auto-detected when omitted: '
                         'an engine with zero emissions is treated as a pipeline, so a '
                         'new engine can never silently score 0/0 = 100%.')
    ap.add_argument('--hash-seed', default=HASH_SEED_DEFAULT,
                    help="PYTHONHASHSEED for every mutant subprocess. Pinned by "
                         "default so the score is reproducible; pass 'random' to "
                         "deliberately sweep seeds and expose order-dependent fixtures.")
    ap.add_argument('--deep', action='store_true',
                    help='pipeline only: add generic operator flips (and/or, </<=, '
                         '==/!=). ~7 min and many equivalent mutants; not the CI gate.')
    ap.add_argument('--gate', default=None,
                    help='restrict to one function, e.g. gate_dossier')
    ap.add_argument('--max-survivors', type=int, default=None,
                    help='CI budget; exit 1 if survivors exceed it')
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--jobs', type=int, default=1,
                    help='parallel mutants. ONLY USEFUL ON A MULTI-CORE RUNNER. The '
                         'mutants are CPU-bound subprocesses: measured on a 1-core '
                         'container, 7 mutants at --jobs 7 did not finish in 240 s '
                         'while ONE at --jobs 1 took 140 s. On a multi-core CI box '
                         'this takes audit_sync from ~30 min to ~4 min; on one core '
                         'it buys nothing and adds contention — use --shard there.')
    ap.add_argument('--budget-file', default=AUDITOR_BUDGETS_FILE,
                    help='per-engine survivor budgets, ratcheted DOWN only')
    ap.add_argument('--indices', default=None, metavar='I,J,K',
                    help='test only these emission indices (0-based, as printed by '
                         '--list). Sharding re-tests emissions already measured, which '
                         'on a 63 s-per-mutant engine is the difference between '
                         'finishing a measurement and abandoning it. Use this to work '
                         'through the PENDING set, and to re-test one emission after '
                         'adding a fixture for it. Like --shard, a partial run NEVER '
                         'enforces a budget.')
    ap.add_argument('--list', action='store_true',
                    help='print every emission with its index and exit; nothing is run')
    ap.add_argument('--shard', default=None, metavar='K/N',
                    help='test only shard K of N (1-based), e.g. 2/4. audit_sync is '
                         '28 emissions at ~63 s each — ~30 min serial, ~4 min at '
                         '--jobs 8, and still beyond a CI step with a 5-minute wall. '
                         'Sharding makes a long engine measurable in bounded pieces '
                         'instead of unmeasured forever. A sharded run NEVER enforces '
                         'a budget: a fraction of the survivors cannot be compared '
                         'against a whole-engine number, and pretending otherwise '
                         'would let a shard report "within budget" while the engine '
                         'as a whole is not.')
    args = ap.parse_args()

    # A per-engine budget beats one global number: the estate's inherited
    # survivors live in audit_canonical.py, and folding them into the same total
    # as a brand-new repo gate would let a new untested finding hide inside an
    # old debt. Absent file, absent key -> no budget, report only.
    budgets = {}
    if os.path.exists(args.budget_file):
        try:
            budgets = json.load(open(args.budget_file, encoding='utf-8')).get('engines', {})
        except Exception:
            budgets = {}
    if args.max_survivors is None:
        args.max_survivors = budgets.get(os.path.basename(args.engine))

    if not os.path.exists(args.engine):
        print(f'ERROR: {args.engine} not found (run from the repo root).')
        sys.exit(2)

    base = open(args.engine, encoding='utf-8').read()
    lines = base.split('\n')
    tree = ast.parse(base)

    # Sanity: the UNMUTATED engine must be green, or every result is meaningless.
    repo_root = os.path.dirname(os.path.abspath(args.engine)) or '.'
    tmp = make_workdir(args.engine, repo_root)
    ref = os.path.join(tmp, os.path.basename(args.engine))
    open(ref, 'w', encoding='utf-8').write(base)
    green, tail = run_self_test(ref, tmp, args.hash_seed)
    if not green:
        print('ERROR: the UNMUTATED engine does not pass its own self-test.')
        print(f'       last line: {tail}')
        print('       Mutation results would be meaningless. Fix the build first.')
        sys.exit(2)
    print(f'baseline self-test: {tail}')

    # KIND SELECTION. Auto-detect deliberately: an engine with zero finding emissions
    # is a PIPELINE, and treating it as an auditor is how analyse_engine.py — 4,847
    # lines, the largest engine in the corpus — scored `0 emission(s)` and sat outside
    # the gate while CI reported 100%. Zero targets must never read as success.
    kind = args.kind
    emission_targets = find_targets(lines, tree, args.gate)
    if kind is None:
        kind = 'auditor' if emission_targets else 'pipeline'
    if kind == 'pipeline':
        targets = [(i, fn, text) for i, fn, text, _lab in
                   find_pipeline_targets(lines, tree, args.gate, deep=args.deep)]
        labels = {i: lab for i, _fn, _t, lab in
                  find_pipeline_targets(lines, tree, args.gate, deep=args.deep)}
        unit = 'decision point'
    else:
        targets = emission_targets
        labels = {}
        unit = 'emission'
    total_targets = len(targets)
    if total_targets == 0:
        print(f'NO {unit.upper()}S FOUND in {args.engine} (kind={kind}).')
        print('A mutation run with nothing to mutate is not a pass. Either the engine '
              'is mis-classified\n(try --kind pipeline / --kind auditor) or the rules '
              'do not fit it — say so in\nMUTATION_BUDGETS.json rather than banking a '
              'vacuous 100%.')
        sys.exit(1)
    if args.list:
        for i, (idx, fn, text) in enumerate(targets):
            print(f'[{i:3}] L{idx + 1:<6} {fn:34} {text[:60]}')
        print(f'{total_targets} {unit}(s) in {args.engine}')
        sys.exit(0)
    shard_note = ''
    if args.indices:
        try:
            want = {int(x) for x in args.indices.replace(' ', '').split(',') if x != ''}
        except ValueError:
            print(f'ERROR: --indices must be a comma-separated list of integers, '
                  f'got {args.indices!r}')
            sys.exit(2)
        bad = sorted(i for i in want if not 0 <= i < total_targets)
        if bad:
            print(f'ERROR: index out of range for {total_targets} emissions: {bad}')
            sys.exit(2)
        targets = [t for i, t in enumerate(targets) if i in want]
        shard_note = f'  (indices {sorted(want)} of {total_targets})'
        if args.max_survivors is not None:
            print('note: budget suppressed for a partial run '
                  '(a subset cannot be compared against a whole-engine number)')
            args.max_survivors = None
    if args.shard:
        try:
            k, n = (int(x) for x in args.shard.split('/'))
            assert 1 <= k <= n
        except Exception:
            print(f'ERROR: --shard must be K/N with 1 <= K <= N, got {args.shard!r}')
            sys.exit(2)
        targets = [t for i, t in enumerate(targets) if i % n == (k - 1)]
        shard_note = f'  (shard {k}/{n} of {total_targets})'
        # A shard cannot enforce a whole-engine budget. Silently dropping it would be
        # worse than refusing: the run would print "within budget" on a fraction.
        if args.max_survivors is not None:
            print(f'note: budget suppressed for a sharded run '
                  f'(shard {k}/{n} cannot be compared against a whole-engine number)')
            args.max_survivors = None
    print(f'targets under test: {len(targets)}' + shard_note
          + (f'  (restricted to {args.gate})' if args.gate else ''))
    print('=' * 78)

    def mutate(idx):
        if kind == 'pipeline':
            return mutate_pipeline(lines, idx, labels.get(idx, ''))
        mut = lines[:]
        indent = len(mut[idx]) - len(mut[idx].lstrip())
        # Preserve any trailing `continue`/`break` so control flow still type-checks;
        # we neutralise the FINDING, not the loop structure.
        tail_stmt = ''
        for kw in ('continue', 'break'):
            if re.search(r';\s*' + kw + r'\s*$', mut[idx]):
                tail_stmt = '; ' + kw
        mut[idx] = ' ' * indent + 'pass' + tail_stmt + '  # MUTANT'
        return '\n'.join(mut)

    njobs = max(1, args.jobs)
    # ONE WORKDIR PER WORKER, LEASED THROUGH A QUEUE — never indexed by job number.
    # Each mutant rewrites the engine file IN PLACE, so two concurrent mutants
    # sharing a directory test each other's mutation and the entire run is
    # silently wrong. Assigning `pool_dirs[job_index % njobs]` LOOKS safe and is
    # not: nothing pins job i to the worker that finished job i-njobs, so a slow
    # worker still holding dir 0 can be joined there by a fast worker starting
    # job njobs. A lease makes the invariant structural — a directory is held by
    # exactly one mutant at a time, by construction rather than by arithmetic.
    pool_dirs = [tmp] + [make_workdir(args.engine, repo_root)
                         for _ in range(njobs - 1)]
    lease = queue.Queue()
    for d in pool_dirs:
        lease.put(d)

    def test_one(idx):
        workdir = lease.get()
        try:
            pth = os.path.join(workdir, os.path.basename(args.engine))
            open(pth, 'w', encoding='utf-8').write(mutate(idx))
            still_green, _ = run_self_test(pth, workdir, args.hash_seed)
            open(pth, 'w', encoding='utf-8').write(base)   # restore before release
            return idx, still_green
        finally:
            lease.put(workdir)

    survivors, killed, done = [], 0, 0
    by_idx = {i: (fn, text) for i, fn, text in targets}
    with concurrent.futures.ThreadPoolExecutor(max_workers=njobs) as ex:
        for idx, still_green in ex.map(test_one, [i for i, _, _ in targets]):
            done += 1
            if still_green:
                fn, text = by_idx[idx]
                survivors.append((idx + 1, fn, text))
            else:
                killed += 1
            if not args.quiet:
                print(f'\r  {done}/{len(targets)} tested · killed {killed} · '
                      f'survived {len(survivors)}', end='')
    if not args.quiet:
        print()
    for d in pool_dirs[1:]:
        shutil.rmtree(d, ignore_errors=True)

    print('=' * 78)
    print(f'KILLED    {killed:>3}  — a fixture detected the loss of this finding')
    print(f'SURVIVED  {len(survivors):>3}  — NO fixture detects the loss of this finding')
    if targets:
        print(f'mutation score: {100.0 * killed / len(targets):.1f}%')
    if survivors:
        print()
        print('SURVIVING MUTANTS (untested findings — each needs a fixture that FAILS')
        print('when the emission is removed):')
        print('-' * 78)
        bygate = {}
        for ln, fn, text in survivors:
            bygate.setdefault(fn, []).append((ln, text))
        for fn in sorted(bygate):
            print(f'  {fn}')
            for ln, text in bygate[fn]:
                print(f'      L{ln:<6} {text[:66]}')

    if args.max_survivors is not None and len(survivors) > args.max_survivors:
        print()
        print(f'RESULT: FAIL — {len(survivors)} survivors exceeds the declared '
              f'budget of {args.max_survivors}.')
        print('        A new gate must ship with fixtures that kill its own mutants.')
        sys.exit(1)
    print()
    print('RESULT: within budget.' if args.max_survivors is not None else 'RESULT: reported.')
    sys.exit(0)


if __name__ == '__main__':
    main()
