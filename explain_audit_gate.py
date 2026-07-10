#!/usr/bin/env python3
# explain_audit_gate.py — Step 10 (MockExplainAudit) / Step 9 (MockExplain)
# MECHANICAL COMPLETION GATE for the explanation-audit pipeline (v1.0).
#
# WHY THIS EXISTS (parallel to Framework_MockTestCreateAudit.md S5-1A):
#   Step 10 already names the right guarantees — the per-question EVIDENCE gate
#   (§17 mechanism 2), the zero-sampling COVERAGE assertion (§17 mechanism 3), and
#   the pre-delivery SCOPE assertion (§18). But those were PROSE the model
#   self-attests, and the engine's verify_fidelity / verify_structure /
#   verify_explanations check the DOCUMENT, never the audit ledger + evidence
#   sidecars. So a collapsed or partial Phase-2 run could self-declare clean and
#   ship — the same false-clean chain closed for Step 8.
#   This module makes those assertions a COMMAND EXIT CODE: it reads the Step-10
#   audit ledger (audit_progress.json) + its evidence sidecars and refuses to
#   certify unless every question was reviewed, every verdict is CLEAN/FIXED, and
#   every class-required evidence artefact EXISTS on disk (evidence-binding — a
#   fabricated ledger cannot pass without the work that produces the files).
#
#   Prose describes; only code certifies. Run at Phase 3 (§20) before present_files;
#   MANDATE D forbids delivery unless this prints AUDIT-COMPLETION-GATE: PASS.
#
# Exam-agnostic: no exam value is read here — only the ledger the audit maintains.
# Dependency-light: Python stdlib only (json, os). --self-test needs no docx.
#
# Usage:
#   python3 explain_audit_gate.py --audit-progress [ExamCode]_Mock[N]_audit_progress.json
#   python3 explain_audit_gate.py --self-test
#
# Exit code: 0 iff AUDIT-COMPLETION-GATE: PASS, else 1.
import json, os, sys

# ── ledger schema (audit_progress.json — §18, made load-bearing) ─────────────
#   {mock, total_questions, evidence_dir,
#    batch_plan: [[q,...], ...],            # frozen tiling of 1..total_questions
#    batches_closed: [batch_index, ...],    # 1-based indices into batch_plan
#    questions: { "<q>": {
#        verdict: "CLEAN"|"FIXED"|"ESCALATED"|"UNVERIFIED",
#        classes: [ "C-COMPUTATIONAL", "C-FIGURAL", "C-FACTUAL", ... ],
#        answer_derived: bool,              # §9 independent re-derivation done
#        derivation_routes: [ "direct", "estimate", ... ],   # >=1
#        viewed_images: [ path, ... ],      # figural only (RXA-8 / §11)
#        web_sources:   [ path, ... ],      # factual/vocab only (RXA-12 / §9)
#        reproduce_checks: [ path, ... ],   # wrong-option/pitfall honesty (RXA-9 / §8.7)
#    } } }
# Every evidence path must resolve to an existing, non-empty file (evidence-binding).

C_HELP = {
    'CA1': 'batches complete (every planned batch closed — MANDATE B)',
    'CA2': 'coverage exact 1..total_questions (no gap, no look-ahead)',
    'CA3': 'every verdict CLEAN/FIXED (no open ESCALATED/UNVERIFIED)',
    'CA4': 'every answer independently re-derived with >=1 route (RXA-1)',
    'CA5': 'figural Q grounded in a viewed image, file present (RXA-8/§11)',
    'CA6': 'factual/vocab Q web-sourced, file present (RXA-12/§9)',
    'CA7': 'reproduce-check evidence present for every Q (RXA-9/§8.7)',
}


def audit_completion_gate(progress_path):
    """Validate the Step-10 audit ledger + evidence sidecars (CA1-CA7). Prints
    'AUDIT-COMPLETION-GATE: PASS/FAIL' (MANDATE-0 safe: Q-numbers + codes only) and
    returns 0 (PASS) or 1 (FAIL)."""
    fails = []
    def bad(code, msg): fails.append((code, msg))
    try:
        st = json.load(open(progress_path, encoding='utf-8'))
    except Exception as e:
        print(f'AUDIT-COMPLETION-GATE: FAIL (CA0: audit_progress unreadable/absent — {e})')
        return 1
    tq = st.get('total_questions')
    evd = st.get('evidence_dir', '') or ''
    plan = st.get('batch_plan') or []
    closed = set(st.get('batches_closed') or [])
    qs = {int(k): v for k, v in (st.get('questions') or {}).items()}

    def _file_ok(path):
        cands = [path]
        if path and not os.path.isabs(str(path)):
            cands += [os.path.join(evd, path), os.path.join(evd, os.path.basename(path))]
            parts = str(path).replace('\\', '/').split('/')
            if parts and parts[0] == 'evidence':
                cands.append(os.path.join(evd, *parts[1:]))
        for c in cands:
            if c and os.path.exists(c) and os.path.getsize(c) >= 1:
                return True
        return False

    # CA1 — every planned batch closed (a skipped/collapsed Phase 2 fails here)
    if not (plan and set(range(1, len(plan) + 1)) <= closed):
        bad('CA1', f'batches_closed={sorted(closed)} does not cover all {len(plan)} '
                   f'planned batches')
    # CA2 — coverage exact (no gap, no look-ahead beyond the plan)
    want = set(range(1, (tq or 0) + 1)); got = set(qs.keys())
    if not (tq and got == want):
        bad('CA2', f'questions != 1..{tq}: missing={sorted(want - got)[:15]} '
                   f'extra(look-ahead)={sorted(got - want)[:15]}')
    # CA3 — every verdict CLEAN or FIXED
    openv = [q for q, e in qs.items() if e.get('verdict') not in ('CLEAN', 'FIXED')]
    if openv:
        bad('CA3', f'not certifiable (ESCALATED/UNVERIFIED/absent verdict): {sorted(openv)[:15]}')
    # CA4 — every answer independently re-derived, >=1 route
    b4 = [q for q, e in qs.items()
          if not (e.get('answer_derived') and (e.get('derivation_routes') or []))]
    if b4:
        bad('CA4', f'answer not independently re-derived: {sorted(b4)[:15]}')
    # CA5 — figural evidence present AND file exists
    b5 = [q for q, e in qs.items()
          if any('FIGURAL' in c for c in (e.get('classes') or []))
          and not ((e.get('viewed_images') or [])
                   and all(_file_ok(p) for p in e.get('viewed_images') or []))]
    if b5:
        bad('CA5', f'figural Q with no/again-missing viewed-image evidence: {sorted(set(b5))[:15]}')
    # CA6 — factual/vocab evidence present AND file exists
    b6 = [q for q, e in qs.items()
          if any(('FACTUAL' in c) or ('VOCAB' in c) for c in (e.get('classes') or []))
          and not ((e.get('web_sources') or [])
                   and all(_file_ok(p) for p in e.get('web_sources') or []))]
    if b6:
        bad('CA6', f'factual/vocab Q unsourced / source file missing: {sorted(set(b6))[:15]}')
    # CA7 — reproduce-check evidence present AND file exists (every Q)
    b7 = [q for q, e in qs.items()
          if not ((e.get('reproduce_checks') or [])
                  and all(_file_ok(p) for p in e.get('reproduce_checks') or []))]
    if b7:
        bad('CA7', f'no reproduce-check evidence: {sorted(set(b7))[:15]}')

    if not fails:
        F = sum(1 for e in qs.values() if any(('FACTUAL' in c) or ('VOCAB' in c)
                                              for c in (e.get('classes') or [])))
        V = sum(1 for e in qs.values() if any('FIGURAL' in c for c in (e.get('classes') or [])))
        print(f'AUDIT-COMPLETION-GATE: PASS (Q reviewed={len(qs)}/{tq}, '
              f'figural viewed={V}, facts sourced={F}, all verdicts CLEAN/FIXED, '
              f'all evidence files present)')
        return 0
    for code, msg in fails:
        print(f'  {code} [{C_HELP.get(code, "")}]: {msg}')
    print(f'AUDIT-COMPLETION-GATE: FAIL ({len(fails)} assertion(s): {[c for c, _ in fails]})')
    return 1


# ── fixture-based self-test (pure json/os; no docx) ──────────────────────────
def self_test():
    import tempfile, copy
    res = []
    def chk(n, c): res.append((n, bool(c)))
    tmp = tempfile.mkdtemp()
    evd = os.path.join(tmp, 'ev'); os.makedirs(evd, exist_ok=True)
    def ef(name):
        p = os.path.join(evd, name); open(p, 'w').write('evidence'); return p
    def wp(name, st):
        p = os.path.join(tmp, name); json.dump(st, open(p, 'w')); return p

    img = ef('q1_stem.png'); src = ef('q1_fact.json')
    rc1 = ef('q1_repro.json'); rc2 = ef('q2_repro.json')
    base = {
        'mock': 1, 'total_questions': 2, 'evidence_dir': evd,
        'batch_plan': [[1, 2]], 'batches_closed': [1],
        'questions': {
            '1': {'verdict': 'FIXED', 'classes': ['C-FIGURAL', 'C-FACTUAL'],
                  'answer_derived': True, 'derivation_routes': ['direct', 'elim'],
                  'viewed_images': [img], 'web_sources': [src], 'reproduce_checks': [rc1]},
            '2': {'verdict': 'CLEAN', 'classes': ['C-COMPUTATIONAL'],
                  'answer_derived': True, 'derivation_routes': ['direct', 'estimate'],
                  'viewed_images': [], 'web_sources': [], 'reproduce_checks': [rc2]},
        }}
    # 1 clean, evidence-backed ledger → PASS
    chk('ACG-pass', audit_completion_gate(wp('p.json', base)) == 0)
    # 2 SKIPPED Phase 2: no batches closed + empty questions → CA1+CA2
    s = copy.deepcopy(base); s['batches_closed'] = []; s['questions'] = {}
    chk('ACG-skipped-phase2', audit_completion_gate(wp('s.json', s)) == 1)
    # 3 PARTIAL review: tq=2 but only Q1 → CA2
    s = copy.deepcopy(base); del s['questions']['2']
    chk('ACG-partial-review', audit_completion_gate(wp('pa.json', s)) == 1)
    # 4 OPEN verdict: Q2 ESCALATED → CA3
    s = copy.deepcopy(base); s['questions']['2']['verdict'] = 'ESCALATED'
    chk('ACG-open-verdict', audit_completion_gate(wp('ov.json', s)) == 1)
    # 5 UNVIEWED figure: Q1 figural, empty viewed_images → CA5
    s = copy.deepcopy(base); s['questions']['1']['viewed_images'] = []
    chk('ACG-unviewed-figure', audit_completion_gate(wp('uf.json', s)) == 1)
    # 6 MISSING evidence file: Q1 names a nonexistent image → CA5 (evidence-binding)
    s = copy.deepcopy(base); s['questions']['1']['viewed_images'] = [os.path.join(evd, 'nope.png')]
    chk('ACG-missing-evidence-file', audit_completion_gate(wp('me.json', s)) == 1)
    # 7 UNSOURCED fact: Q1 factual, empty web_sources → CA6
    s = copy.deepcopy(base); s['questions']['1']['web_sources'] = []
    chk('ACG-unsourced-fact', audit_completion_gate(wp('us.json', s)) == 1)
    # 8 NOT re-derived: Q2 answer_derived False → CA4
    s = copy.deepcopy(base); s['questions']['2']['answer_derived'] = False
    chk('ACG-not-derived', audit_completion_gate(wp('nd.json', s)) == 1)

    passed = sum(1 for _, ok in res if ok); total = len(res)
    for n, ok in res:
        if not ok:
            print(f'  COMPLETION-FAIL: {n}')
    print(f'COMPLETION-SELF-TEST: {passed}/{total} PASS')
    return passed == total


def main():
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    if '--audit-progress' in sys.argv:
        i = sys.argv.index('--audit-progress')
        if i + 1 < len(sys.argv):
            sys.exit(audit_completion_gate(sys.argv[i + 1]))
    print('explain_audit_gate.py — Step-10 mechanical completion gate. '
          '--audit-progress <audit_progress.json> or --self-test.')
    sys.exit(2)


if __name__ == '__main__':
    main()
