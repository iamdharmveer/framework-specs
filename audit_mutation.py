#!/usr/bin/env python3
"""
AUDIT MUTATION — mechanical hollow-branch detector for audit_canonical.py.

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
import tempfile

ENGINE_DEFAULT = 'audit_canonical.py'

# A "finding emission" is the statement where a gate records that something is
# wrong. Neutralising it makes the gate silently accept the defect it exists to
# catch — which is precisely the condition a fixture is supposed to notice.
EMIT_RE = re.compile(
    r'^(bad|bad_[a-z_]+|figtext_prose|composite|multi_per_line|math_raster|'
    r'warn_view|bad_opt|bad_grade|issues|findings)\.append\('
)


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


def run_self_test(path, cwd):
    try:
        r = subprocess.run([sys.executable, path, '--self-test'],
                           capture_output=True, text=True, cwd=cwd, timeout=600)
    except subprocess.TimeoutExpired:
        return False, 'TIMEOUT'          # timeout counts as KILLED
    tail = r.stdout.strip().split('\n')[-1] if r.stdout.strip() else ''
    green = (r.returncode == 0 and 'PASS' in tail and 'FAIL' not in tail)
    return green, tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--engine', default=ENGINE_DEFAULT)
    ap.add_argument('--gate', default=None,
                    help='restrict to one function, e.g. gate_dossier')
    ap.add_argument('--max-survivors', type=int, default=None,
                    help='CI budget; exit 1 if survivors exceed it')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    if not os.path.exists(args.engine):
        print(f'ERROR: {args.engine} not found (run from the repo root).')
        sys.exit(2)

    base = open(args.engine, encoding='utf-8').read()
    lines = base.split('\n')
    tree = ast.parse(base)

    # Sanity: the UNMUTATED engine must be green, or every result is meaningless.
    tmp = tempfile.mkdtemp()
    ref = os.path.join(tmp, os.path.basename(args.engine))
    open(ref, 'w', encoding='utf-8').write(base)
    green, tail = run_self_test(ref, tmp)
    if not green:
        print('ERROR: the UNMUTATED engine does not pass its own self-test.')
        print(f'       last line: {tail}')
        print('       Mutation results would be meaningless. Fix the build first.')
        sys.exit(2)
    print(f'baseline self-test: {tail}')

    targets = find_targets(lines, tree, args.gate)
    print(f'finding emissions under test: {len(targets)}'
          + (f'  (restricted to {args.gate})' if args.gate else ''))
    print('=' * 78)

    survivors, killed = [], 0
    for n, (idx, fn, text) in enumerate(targets, 1):
        mut = lines[:]
        indent = len(mut[idx]) - len(mut[idx].lstrip())
        # Preserve any trailing `continue`/`break` so control flow still type-checks;
        # we neutralise the FINDING, not the loop structure.
        tail_stmt = ''
        for kw in ('continue', 'break'):
            if re.search(r';\s*' + kw + r'\s*$', mut[idx]):
                tail_stmt = '; ' + kw
        mut[idx] = ' ' * indent + 'pass' + tail_stmt + '  # MUTANT'
        p = os.path.join(tmp, os.path.basename(args.engine))
        open(p, 'w', encoding='utf-8').write('\n'.join(mut))
        still_green, _ = run_self_test(p, tmp)
        if still_green:
            survivors.append((idx + 1, fn, text))
        else:
            killed += 1
        if not args.quiet:
            print(f'\r  {n}/{len(targets)} tested · killed {killed} · '
                  f'survived {len(survivors)}', end='')
    if not args.quiet:
        print()

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
