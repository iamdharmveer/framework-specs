# DEPLOY NOTES — release 2026.11.21 (GAP-2026-11-16-DIFFICULTY-YARDSTICK, Cluster R3) over release 2026.11.20
Built on production a688cc0 (release 2026.11.20). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly a688cc0 when you deploy (any other change on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (19 files = the 18 files that differ from 2026.11.20 + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.52.0 — §2R difficulty-yardstick footer lines)
Framework_MockReview.md                 (v2.3.0 — S2-2R enumerated defect codes; 300 lines = one read chunk)
Framework_MockTestAnalyse.md            (v2.63.0 — S11-1d the difficulty ladder, built once per exam in Step 5)
Framework_MockTestCreate.md             (v8.0 — mode ladder / counted; writer packet; STEP A2; footer lines)
MANIFEST.json                           (regenerated)
SESSION_BUDGET.json                     (the ladder run file is staged for TestCreate / MockCreate)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (MockReview v2.2.0 entry moved — MockReview stays one read chunk)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 8.0, MockReview 2.3.0, MockTestAnalyse 2.63.0, Footer 1.52.0)
VERSION                                 (2026.11.21)
analyse_engine.py                       (ladder_row / ladder_prepare / ladder_merge; stamps v2.63)
blueprint_core.py                       (Cluster R3: ladder, placement, defect codes, deterministic gates, rules)
corpus_io.py                            (G-LABELSIZE: atom-label boxes as wide as their text)
final_assembly.py                       (v1.25.0 — mode freeze, ladder load, r3 reviewer jobs, footer report)
handshake_audit.py                      (H-BV / H-BC pinned to mode br1; +1 H-BC-3R; +17 H-R3; 262 checks)

SKILL CHANGE: none. TRIGGERS: unchanged.

AFTER DEPLOY — WHAT EACH EXAM PROJECT DOES (once per exam, then nothing):
  1. Re-run Step 5 (PYQExtract) once. It now also ranks the exam's past questions blind (S11-1d, fresh sub-agents,
     about 25 jobs for a 360-question exam — a one-off cost) and delivers [ExamCode]_difficulty_ladder.json.
  2. Keep that file with the registry and the exemplar bank, and attach it to every TestCreate / MockCreate run
     (like the exemplar bank — a RUN FILE). Keeping it in the project's Files also works.
  3. Until an exam has its ladder, its papers run difficulty mode 'counted' (rule r2.1, decision depth) and the
     footer says so in one AMBER line. Nothing stops.
  Papers already in progress continue on the 2026.11.20 rule (their batch_state has review records and no mode).
  An exam that must keep the old rule sets "difficulty_mode": "br1" in its blueprint (owner opt-out).

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK
