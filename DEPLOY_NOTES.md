# DEPLOY NOTES — release 2026.11.12 (GAP-2026-11-12-RULER-ANCHORS + HANDOVER-CHECKPOINT + BATCH-SPEED — real past questions to compare against, a handover that keeps the work, 3 reviewers per batch)
Over verified production 6dfd377 (2026.11.11); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (17 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.47.0 — AMBER line naming the difficulty-anchor basis)
Framework_MockTestCreate.md             (v6.2 — S0-BV BV-7..9; S4-7 STEP A2 reviewer jobs + handover; S0-OP-0 back-fill no longer holds Q1)
Framework_MockTestOrchestrate.md        (v1.4.0 — checkpoint command + planned handover; reviewer jobs in ONE message; O2-9 no mid-run question)
LAW_REGISTRY.json                       (+LAW-BV-7..9)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (moved version entries)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 6.2, Orchestrate 1.4.0, DeliveryFooter 1.47.0)
VERSION                                 (2026.11.12)
blueprint_core.py                       (v2.2 — ruler anchor content + PYQExplain-band fallback; 3-reviewer batch jobs)
bootstrap.py                            (--checkpoint make|restore|drop; --when handover; worker prompt)
final_assembly.py                       (v1.18 — bv_batch_step: 3 reviewer jobs per round)
handshake_audit.py                      (213 checks: real-shape ruler, reviewer jobs, handover keeps the batch)

routes.json: UNCHANGED (do not upload).
SKILL CHANGE: none (SKILL.md / mocktestframework_SKILL.md unchanged — no re-sync needed).

AFTER DEPLOY: start the stopped Organic test again with TestCreate (do not "continue" it — its batch-1 grades were
made with no past questions to compare against). No other step: the ruler with past-question content is built
automatically at the start of the run.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx scikit-image openpyxl --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT
  python3 bootstrap.py                     -> VERIFIED (60/60)
  python3 blueprint_core.py --self-test    -> SELF-TEST: 1407/1407 PASS
  python3 final_assembly.py --self-test    -> SELF-TEST: 188/188 PASS
  python3 bootstrap.py --self-test         -> SELF-TEST: 72/72 PASS
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 213 ok, 0 FAIL
  python3 run_ci_gates.py --skip Install   -> every gate PASS
  (or let .github/workflows/validate.yml run on the push)

WHAT THE OWNER SEES: every batch is checked by 3 fresh reviewers started together (was 40 checkers, often one by
one); the reviewers and the author compare each question with real past questions of the exam (same topic first);
a handover between workers keeps every written question and grade; no framework question is asked mid-run; Q1
starts without waiting for the PYQ back-fill. One AMBER footer line says the anchors use the PYQExplain levels while
the exam has no blind-graded past questions.
