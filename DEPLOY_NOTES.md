# DEPLOY NOTES — release 2026.11.22 (GAP-2026-11-17-FALLBACK-CASCADE) over release 2026.11.21
Built on production ce406dd (release 2026.11.21). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly ce406dd when you deploy (any other change on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (15 files = the 14 files that differ from 2026.11.21 + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.52.1 — one more chain line: finding still open after rung 2, question kept)
Framework_MockReview.md                 (v2.3.1 — S2-2R: a blocking code acts when two reviewers name it)
Framework_MockTestCreate.md             (v8.1 — STEP A2: quorum, no split rewrite, no text fallback for a finding)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (MockReview v2.3.0 entry moved — MockReview stays one read chunk)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 8.1, MockReview 2.3.1, DeliveryFooter 1.52.1)
VERSION                                 (2026.11.22)
blueprint_core.py                       (R3_SPLIT_FIX_RUNGS 0, R3_CODE_QUORUM 2, R3_FINDING_MAX_RUNG 2; bc_apply)
final_assembly.py                       (self-test: the C3 restore scenario run in both modes)
handshake_audit.py                      (H-BC-3R: a split confirmed by the adjudicator settles; 262 checks)

SKILL CHANGE: none. TRIGGERS: unchanged.

AFTER DEPLOY:
  1. Nothing to re-run in Step 5 — keep the difficulty ladder you already made.
  2. If the project's Files section holds any Framework_*.md copy, remove it (or replace it with this release's copy).
     A copy below the new floors (Create 8.1, MockReview 2.3.1, DeliveryFooter 1.52.1) is not loaded anyway.
  3. Start the paper AGAIN in a NEW chat (do not attach the old M1 batch_state or progress file). Questions already
     settled under 2026.11.21 stay settled — batch 1 of the old run keeps its text fallbacks.
  Papers in mode 'br1' (begun before 2026.11.21, or opted out) are unchanged.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.21 bundle (production ce406dd).
