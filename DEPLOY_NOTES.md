# DEPLOY NOTES — release 2026.11.28 (GAP-2026-11-21-A3-OMML-PARITY) over release 2026.11.27
Built on production 6f40774b587f1ef3fbcd05f1ba47e81ee3dafcff (release 2026.11.27). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for every exam
(MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production has any content change beyond 6f40774 when you deploy (git diff 6f40774 production not empty), stop and
send me the production commit — the bundle must be rebuilt on it.

UPLOAD LIST (the files that differ from 2026.11.27, plus DEPLOY_NOTES.md and SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md                 (this file)
Framework_DeliveryFooter.md     (v1.57.0 — the A3-TEXT disclosure line)
Framework_MockTestOrchestrate.md (v1.12.0 — O3-8: a STEP A3 refusal is an instruction, never a stop)
Framework_MockTestCreate.md     (v8.7 — STEP A3 text: one reader both sides, at most one refusal, then bind + disclose;
                                 S13-2L.0 collects batch_state['a3_footer'])
MANIFEST.json                   (regenerated)
SHA256SUMS.txt                  (checksums of this upload)
SPEC_MANIFEST.json              (regenerated)
SPEC_SECTIONS.json              (regenerated)
STEP_CONTRACTS.json             (floors: Create 8.7, MockTestOrchestrate 1.12.0, DeliveryFooter 1.57.0)
VERSION                         (2026.11.28)
audit_canonical.py              (v2.47 — --item-texts writes the structure-preserving reading per paragraph; 694)
blueprint_core.py               (v2.13 — Cluster A3: omml_struct_text, a3_same_question, a3_guard_step; 1629)
final_assembly.py               (v1.29.0 — STEP A3 compares like with like; bounded text guard; 32-construct fixture; 262)

SKILL / TRIGGERS / ROUTES: unchanged.

RESUME THE HALTED PAPER (CSIR_NET_MATHEMATICAL_SCIENCES TestCreate P1, batch 1): after deploy, in that paper's session
say "continue" — Step 0 loads 2026.11.28; then run STEP B (the auditor with --item-hashes and --item-texts) and STEP A3.
Q5 and Q6 bind (measured on the incident's own blocks). Nothing else to redo.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 2026.11.28, 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.27 files (production 6f40774) together — its auditor writes item_texts in its own string
format again, and it ignores the batch_state keys a3_text_guard / a3_footer. (Rolling back re-opens the STEP A3 halt.)
