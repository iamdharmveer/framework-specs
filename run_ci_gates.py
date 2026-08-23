#!/usr/bin/env python3
"""run_ci_gates.py — execute .github/workflows/validate.yml's gate steps VERBATIM.

GAP-2026-08-23-GATE-INVOCATION. A release verification ran `audit_specs_ext.py`
with no arguments (an invocation that audits nothing and exits 2) inside a shell
pipeline that reported tail's exit status instead of the auditor's. Every check
printed green; the one red gate in the bundle — SPEC-BUDGET on the PYQScan route —
was first seen by the deploy manager, who correctly STOPped the release.

Two failure modes, one root cause: the local gate suite was a hand-maintained
COPY of CI, and copies drift. This runner removes the copy. It parses the
workflow file the deploy gate actually runs, executes each step's `run:` block
through bash unchanged, captures the TRUE exit status of the whole block
(`set -o pipefail` is applied, so a pipeline cannot launder a failing command
through its last stage), and exits non-zero if ANY step failed. A release
verification that calls this runner is, by construction, running what CI runs.

USAGE
    python3 run_ci_gates.py               # run every step, summary at the end
    python3 run_ci_gates.py --list        # print step names, run nothing
    python3 run_ci_gates.py --only NAME   # run steps whose name contains NAME
    python3 run_ci_gates.py --skip NAME   # skip steps whose name contains NAME
                                          # (repeatable; e.g. --skip "Install")

Tracked, repo-level runner — NOT routed to any trigger (same standing as
validate_framework_md.py / mock_sync_audit.py). Stdlib only. The YAML subset it
parses is exactly the shape validate.yml uses (steps with `name:` and either a
single-line `run: cmd` or a block `run: |`); it HARD-FAILS on a step it cannot
parse rather than skipping it, because a runner that silently skips steps is the
defect this file exists to prevent.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKFLOW = os.path.join(HERE, '.github', 'workflows', 'validate.yml')

SELF_TEST_EXPECTED = 7  # parser fixtures below; ratchet like every other suite


def parse_steps(text):
    """Return [(name, run_block_or_None)] for every `- name:` step, in order.

    A step with `uses:` and no `run:` (checkout, setup-python) parses to
    (name, None) and is reported SKIP(no-run). A step whose body cannot be
    classified raises ValueError — loud, never a silent skip.
    """
    lines = text.split('\n')
    # locate every '- name:' at any indent, then read its block
    starts = [i for i, ln in enumerate(lines)
              if re.match(r'\s*-\s+name:\s*\S', ln)]
    steps = []
    for si, i in enumerate(starts):
        end = starts[si + 1] if si + 1 < len(starts) else len(lines)
        name = re.match(r'\s*-\s+name:\s*(.+?)\s*$', lines[i]).group(1)
        body = lines[i + 1:end]
        run = None
        for bi, bl in enumerate(body):
            m1 = re.match(r'(\s*)run:\s*\|\s*$', bl)
            m2 = re.match(r'\s*run:\s*(\S.*?)\s*$', bl)
            if m1:
                # block scalar: collect lines more-indented than 'run:'
                base = len(m1.group(1))
                blk = []
                for cl in body[bi + 1:]:
                    if cl.strip() == '':
                        blk.append('')
                        continue
                    ind = len(cl) - len(cl.lstrip())
                    if ind <= base:
                        break
                    blk.append(cl)
                # strip the common indent of the block
                pads = [len(x) - len(x.lstrip()) for x in blk if x.strip()]
                cut = min(pads) if pads else 0
                run = '\n'.join(x[cut:] if x.strip() else '' for x in blk).rstrip()
                break
            if m2:
                run = m2.group(1)
                break
            if re.match(r'\s*uses:\s*\S', bl):
                run = None
                break
        else:
            raise ValueError(f'step {name!r}: no run: and no uses: — refusing to '
                             f'guess (a skipped gate is the defect this runner '
                             f'exists to prevent)')
        steps.append((name, run))
    if not steps:
        raise ValueError('no steps parsed from workflow — refusing to report green')
    return steps


def run_step(run_block):
    """Execute one run block through bash with pipefail; return (rc, tail)."""
    # GAP-2026-08-23-AUDITSYNC-FIXTURE-STALE: GitHub Actions executes run blocks
    # under `bash --noprofile --norc -e -o pipefail`. `-e` is not optional
    # fidelity: without it a multi-line block's exit status is its LAST command's,
    # so `python3 audit_sync.py --self-test` failing on line 1 was hidden by the
    # live audit passing on line 2. Same laundering family as pipefail, one
    # statement separator over.
    proc = subprocess.run(
        ['bash', '--noprofile', '--norc', '-e', '-o', 'pipefail', '-c', run_block],
        cwd=HERE, capture_output=True, text=True)
    out = (proc.stdout + proc.stderr).strip().split('\n')
    return proc.returncode, '\n'.join(out[-6:])


def main(argv):
    if '--self-test' in argv:
        return 0 if self_test() else 1
    only = [argv[i + 1] for i, a in enumerate(argv) if a == '--only']
    skip = [argv[i + 1] for i, a in enumerate(argv) if a == '--skip']
    text = open(WORKFLOW, encoding='utf-8').read()
    steps = parse_steps(text)
    if '--list' in argv:
        for name, run in steps:
            print(('RUN ' if run else 'uses') + '  ' + name)
        return 0
    results = []
    for name, run in steps:
        if only and not any(o.lower() in name.lower() for o in only):
            continue
        if skip and any(s.lower() in name.lower() for s in skip):
            results.append((name, 'SKIP(--skip)', ''))
            print(f'~ SKIP  {name}')
            continue
        if run is None:
            results.append((name, 'SKIP(no-run)', ''))
            continue
        rc, tail = run_step(run)
        verdict = 'PASS' if rc == 0 else f'FAIL rc={rc}'
        results.append((name, verdict, tail))
        mark = 'v' if rc == 0 else 'X'
        print(f'{mark} {verdict:9}  {name}')
        if rc != 0:
            print('  ' + tail.replace('\n', '\n  '))
    fails = [r for r in results if r[1].startswith('FAIL')]
    ran = [r for r in results if r[1] in ('PASS',) or r[1].startswith('FAIL')]
    print(f'\nRUN-CI-GATES: {len(ran)} step(s) executed, '
          f'{len(fails)} failed'
          + (' — ' + '; '.join(n for n, v, t in fails) if fails else ' — ALL GREEN'))
    return 1 if fails else 0


def self_test():
    """Parser fixtures — the shapes validate.yml actually uses, plus the refusals."""
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))
        print(('  PASS: ' if cond else '  FAIL: ') + name)

    y1 = ('jobs:\n  v:\n    steps:\n'
          '      - name: A single\n        run: echo one\n'
          '      - name: B uses-only\n        uses: actions/checkout@v4\n'
          '      - name: C block\n        run: |\n'
          '          echo two\n          echo three | grep three\n')
    s = parse_steps(y1)
    check('parses three steps in order',
          [n for n, _ in s] == ['A single', 'B uses-only', 'C block'])
    check('single-line run captured', s[0][1] == 'echo one')
    check('uses-only step has run None', s[1][1] is None)
    check('block scalar joined and dedented',
          s[2][1] == 'echo two\necho three | grep three')
    try:
        parse_steps('jobs:\n  v:\n    steps:\n      - name: broken\n        if: x\n')
        check('unclassifiable step refuses loudly', False)
    except ValueError:
        check('unclassifiable step refuses loudly', True)
    rc, _ = run_step('false | true')
    check('pipefail defeats rc laundering through a pipeline', rc != 0)
    rc, _ = run_step('false\ntrue')
    check('-e makes an early-line failure fail the whole block (GH parity)',
          rc != 0)

    passed = sum(1 for _, ok in checks if ok)
    fails = [n for n, ok in checks if not ok]
    if len(checks) != SELF_TEST_EXPECTED:
        fails.append(f'suite_ran_every_check (ran {len(checks)}, '
                     f'expected {SELF_TEST_EXPECTED})')
    print(f'run_ci_gates self-test: {passed} passed, {len(fails)} failed'
          + (' — ' + '; '.join(fails) if fails else ''))
    return not fails


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
