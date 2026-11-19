# DEPLOY NOTES — release 2026.11.25 (GAP-2026-11-19-S13-2F-LOOP + GAP-2026-11-19-FIGURE-LOSS) over release 2026.11.24
Built on production b7027b687ca519d845647ea34bc3ed365feb550e (release 2026.11.24). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly b7027b6 when you deploy (any other change on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (17 files = the 15 files that differ from 2026.11.24 + DEPLOY_NOTES.md + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md                         (this file)
Framework_DeliveryFooter.md             (v1.54.0 — §LADDER-NF: shape-mix disclosure, plan relief, figure floor, moved grant)
Framework_MockTestCreate.md             (v8.4 — S13-2F RUN-BLOCK rewritten (persistent counter, bc.s13_2f_plan, total cap,
                                         no chain / no re-author on a BATCH-COMPLETE paper); S0-BC LAW-BC-2 / -6 / -8
                                         amended; S3-12d effective targets + plan relief; S4-7 STEP A2 new pre-review
                                         gates and rung-3 kinds; STEP B last batch = fa.bc_last_batch_apply; S4-12.2
                                         migration; S13-2L / S13-2R refuse a BATCH-COMPLETE paper)
Framework_MockTestOrchestrate.md        (v1.11.0 — O3-8: every [HS:LADDER] is an instruction; no worker-composed stop)
LAW_REGISTRY.json                       (NEW LAW-FA-TERM-1 / LAW-PLAN-CHECK-1 / LAW-RECORD-READER-1; LAW-BC-2 / -6 / -8 amended)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 8.4, Orchestrate 1.11.0, DeliveryFooter 1.54.0)
VERSION                                 (2026.11.25)
audit_canonical.py                      (v2.45 — check 9 mode-aware; dispositions + structured qs; settled / disclosed
                                         items accepted; --escalate-early; A-SHAPEMIX effective targets + relief +
                                         disclosure; A-CLASSMIX partial mode; A-AXIS1 moved grant + figure floor; 691 checks)
audit_sync.py                           (NEW FA-TERM static check on the S13-2F block)
blueprint_core.py                       (v2.10 — s13_2f_plan / persistent counter / total cap / termination harness;
                                         mode-aware check 9; engine-owned difficulty_obs; shape vocabulary, effective
                                         targets, balanced planner + relief; rung-3 kinds, R5b figure preference,
                                         figure gates, re-grant, floor; migration; 1575 checks)
final_assembly.py                       (v1.26.0 — engine-owned difficulty_obs; G-SHAPEPLAN / G-FIG-SCALE context;
                                         re-grant; bc_last_batch_route / _apply; difficulty_mode committed; 245 checks)
handshake_audit.py                      (NEW H5-S13-2F-TERMINATION — real S13-2F block + real auditor; 268 checks)

SKILL CHANGE: none. TRIGGERS: unchanged. ROUTES: unchanged.

AFTER DEPLOY:
  1. Nothing to change in any of the ~200 projects. Every fix is engine / spec level and reaches every project on its
     next Step 0. Spec copies in a project's Files below the new floors (Create 8.4, Orchestrate 1.11.0,
     DeliveryFooter 1.54.0) are not loaded — remove them to silence the [STALE — NOT LOADED] line.
  2. No blueprint refresh is needed: shape targets that do not sum to the paper's question count, and alias spellings
     ('match' / 'matching'), are normalised by the engine (bc.shape_targets_effective) for planner and auditor alike.
     A ScopedBlueprint / MockBlueprint refresh at the project's next natural run is optional.
  3. A paper in progress resumes unchanged; on its next resume S4-12.2 migrates its state once (recorded in
     batch_state['migrations']). A paper parked at Final Assembly by the S13-2F loop: type `continue` in its original
     chat — Final Assembly resumes and certifies (AMBER lines where something is disclosed). No question is rewritten.
  4. Stale project copies of `<EXAM>_mock_test_audit.py` in a project's Files are never imported (engines are
     repo-only); they can be deleted.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.24 files (production b7027b6).
