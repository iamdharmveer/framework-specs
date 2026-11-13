# DEPLOY NOTES — release 2026.11.15 (GAP-2026-11-13-STEP7-SPEED — every question settled in its own batch, no forced fresh worker, half the read calls)
Over verified production 48c6502 (2026.11.14 + hotfix: linked-set repeats, A-QINDEX '; ' split, final-round index —
all three kept); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (20 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.50.0 — INFRA-CARRY line; FRAMEWORK NOTE timing line)
Framework_MockTestCreate.md             (v6.5 — questions settled in their own batch; RUN-BLOCKs; RESUME kept; S13-1B check; round-2 delta)
Framework_MockTestOrchestrate.md        (v1.7.0 — same worker by room; WARM STANDBY; reviewer waves; quota rule; timing)
LAW_REGISTRY.json                       (+LAW-BV-SETTLE, LAW-RUN-BLOCK, LAW-RESUME-AUTO; LAW-BV-13 retired)
MANIFEST.json                           (regenerated)
SESSION_BUDGET.json                     (+fa_work_unit_tokens, review_qs_per_job, parallel_jobs_max, minute targets)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (moved version entries)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated — run_block_ranges)
STEP_CONTRACTS.json                     (floors: Create 6.5, Orchestrate 1.7.0, DeliveryFooter 1.50.0)
VERSION                                 (2026.11.15)
audit_canonical.py                      (gate_distractor passes the stated formula)
blueprint_core.py                       (v2.5 — formula-only items; reviewer job split; reviewer-health minimum)
bootstrap.py                            (--run-section; automatic RESUME; packed reads; WARM STANDBY; timing)
final_assembly.py                       (v1.21 — in-batch settlement; INFRA-CARRY; paper_in_progress)
handshake_audit.py                      (219 checks)
spec_sections.py                        (RUN-BLOCK ranges; packed read calls)

routes.json: UNCHANGED (do not upload).
SKILL CHANGE: none (SKILL.md / mocktestframework_SKILL.md unchanged — no re-sync needed).

AFTER DEPLOY: start the next paper fresh with TestCreate / MockCreate. A paper begun under 2026.11.14 can be continued:
its saved grades are kept and any question it carried is measured in the next batch's first round.
