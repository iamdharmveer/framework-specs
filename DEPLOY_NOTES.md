# DEPLOY NOTES — release 2026.11.17 (includes 2026.11.16) over production eaf40a9
Built on a fresh clone of production at eaf40a9 (2026.11.15 + the three hotfixes 869ee66, 104e056, eaf40a9).
It CONTAINS release 2026.11.16 (GAP-2026-11-14-BATCH-COMPLETE, never deployed) and 2026.11.17
(GAP-2026-11-14-SPEED-AND-FIDELITY) in ONE upload; the earlier 2026.11.16 / 2026.11.17 zips are withdrawn — do not
deploy them. Commit once, push main, push main:production. Discard the local branch held/release-2026.11.16.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

THE THREE PRODUCTION HOTFIXES ARE KEPT:
  eaf40a9 blueprint_core REVIEW-KEY-ANNOTATED — merged as-is (v2.5.1 code and test), and applied to the new in-batch
          review too (bc_answer_norm, bc_canon_key).
  869ee66 / 104e056 final_assembly v1.22 / v1.22.1 FINAL-ROUND-CAP-DEADLOCK — the S13-1B path they patched is replaced
          by the in-batch settlement (S0-BC); the live stranded state they fixed (round at the cap, slot unmeasured,
          open chain) is measured by the settlement batch — self-test bv_final_stranded_slot_migrates_and_is_measured.

UPLOAD LIST (23 files = the 22 files that differ from eaf40a9 + SHA256SUMS.txt; none is new):
CHANGELOG.md                            (2026.11.17 and 2026.11.16 entries)
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.51.0 — §LADDER-BC)
Framework_MockReview.md                 (v2.2.0 — legacy only; stays in the repo, no longer routed)
Framework_MockTestCreate.md             (v7.1)
Framework_MockTestOrchestrate.md        (v1.9.0)
LAW_REGISTRY.json                       (LAW-BC-1..9; amendments)
MANIFEST.json                           (regenerated)
SESSION_BUDGET.json                     (fa_work_unit_tokens 60,000)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (moved version entries)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated — legacy / trigger / feature ranges)
STEP_CONTRACTS.json                     (floors: Create 7.1, Orchestrate 1.9.0, DeliveryFooter 1.51.0, MockReview 2.2.0)
VERSION                                 (2026.11.17)
audit_canonical.py                      (v2.42)
audit_sync.py                           (BC-COVERAGE, BC-CHECKLIST-SYNC, TEST-NO-HANDWRITE, STOP-REPAIR-COVERAGE)
blueprint_core.py                       (v2.7 — includes the eaf40a9 hotfix)
bootstrap.py                            (trigger-scoped reads; --show-section LEGACY:<id>)
final_assembly.py                       (v1.23 — supersedes v1.22 / v1.22.1)
handshake_audit.py                      (244 checks)
routes.json                             (Framework_MockReview.md off the MockCreate / TestCreate routes)
spec_sections.py                        (legacy / trigger / feature cuts)

SKILL CHANGE: none (trigger names unchanged — no re-sync needed).
EXAM PROJECTS: nothing to change. A paper in progress continues (Create S4-12 LEGACY MIGRATION): the SSC_CGL_TIER1 P1
paper stranded at Final Assembly is measured by its settlement batch on the next "continue".

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> N/N VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> 23/23 PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

THEN THE TIMED RUN: CSIR NET Chemical Sciences — TestCreate P1 --level subject --scope "Organic Chemistry"; record
`python3 bootstrap.py --timing-show` and, per batch, SELF-COUNT lines, jobs per round, adjudications, rung uses.
