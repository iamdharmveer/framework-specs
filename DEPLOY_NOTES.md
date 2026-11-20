# DEPLOY NOTES — release 2026.11.26 (GAP-2026-11-20-RUNG3-BIND-DEADLOCK) over release 2026.11.25
Built on production b26f78105f3bae62e88454e79fb8a35b64526a29 (release 2026.11.25). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly b26f781 when you deploy (any other change on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (13 files = the 11 files that differ from 2026.11.25 + DEPLOY_NOTES.md + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md                         (this file)
Framework_DeliveryFooter.md             (v1.55.0 — §LADDER-BC: F9 line "kept its figure"; "replaced by a text question"
                                         for the TEXT fallback only)
Framework_MockTestCreate.md             (v8.5 — S0-BC LAW-BC-2: one definition of the TEXT fallback + the F9 repair;
                                         S4-7 STEP A2 REWRITE: the F9 order; STEP A3: only the TEXT fallback is refused,
                                         and its repair is STEP A2)
LAW_REGISTRY.json                       (LAW-BC-2 / LAW-BC-7 amended 2026.11.26)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 8.5, DeliveryFooter 1.55.0)
VERSION                                 (2026.11.26)
blueprint_core.py                       (v2.11 — bc_is_text_fallback / bc_is_restored / bc_fallback_figure_open;
                                         F3 vision + solver records kept; F6 restore at most once; F8 per-order
                                         re-issue; F9 bounded repair (2 orders -> R5b once -> kept + AMBER); 1586 checks)
final_assembly.py                       (v1.27.0 — STEP A3 refuses a figure only on the TEXT fallback and names STEP A2;
                                         STEP A2 treats a fallback still carrying a figure as open (earlier batches too)
                                         and decides it in the same step; figure record put back when kept; 250 checks)

SKILL CHANGE: none. TRIGGERS: unchanged. ROUTES: unchanged.

AFTER DEPLOY:
  1. Nothing to change in any of the ~200 projects. Every fix is engine / spec level and reaches every project on its
     next Step 0. Spec copies in a project's Files below the new floors (Create 8.5, DeliveryFooter 1.55.0) are not
     loaded — remove them to silence the [STALE — NOT LOADED] line.
  2. The halted paper resumes from disk, nothing is regenerated: type `continue` in its original chat (or start the
     same `TestCreate` trigger in a new chat of the same project — RESUME mode finds the paper). STEP A2 runs, then
     STEP A3: every text / figure rebuild and R5b figure version binds at once; a TEXT fallback that still carries a
     figure gets one REWRITE order without the figure (at most 2), then R5b or "kept its figure" (AMBER). The batch
     then continues to STEP E as normal.
  3. A paper in progress on another project resumes unchanged; no migration is needed (the new fields are optional).

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 2026.11.26, 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.25 files (production b26f781).
