# DEPLOY NOTES — release 2026.11.14 (GAP-2026-11-14-CARRY + EDGE-RECOUNT + FINAL-COUNT — no extra reviewer round in a batch, a second count on the band edge, one ruler at Final Assembly)
Over verified production b1a24b2 (2026.11.13); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (17 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.49.0 — batch line: level being re-checked with the next batch)
Framework_MockTestCreate.md             (v6.4 — S0-BV BV-13..15; S13-1B final counting round; short batch report)
Framework_MockTestOrchestrate.md        (v1.6.0 — rewritten questions measured with the next batch)
LAW_REGISTRY.json                       (+LAW-BV-13..15)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (moved version entries)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floors: Create 6.4, Orchestrate 1.6.0, DeliveryFooter 1.49.0)
VERSION                                 (2026.11.14)
blueprint_core.py                       (v2.4 — edge re-count; short author view; short reviewer examples)
bootstrap.py                            (python session: nested definitions kept, indirect ones listed)
final_assembly.py                       (v1.20 — carry to the next batch; final counting round)
handshake_audit.py                      (218 checks)

routes.json: UNCHANGED (do not upload).
SKILL CHANGE: none (SKILL.md / mocktestframework_SKILL.md unchanged — no re-sync needed).

AFTER DEPLOY: start the Organic test fresh with TestCreate. A paper begun under an earlier release can be continued:
its saved grades are kept.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx scikit-image openpyxl --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT
  python3 bootstrap.py                     -> VERIFIED (60/60)
  python3 blueprint_core.py --self-test    -> SELF-TEST: 1427/1427 PASS
  python3 final_assembly.py --self-test    -> SELF-TEST: 196/196 PASS
  python3 bootstrap.py --self-test         -> SELF-TEST: 87/87 PASS
  python3 spec_sections.py --self-test     -> SELF-TEST: 35/35 PASS
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 218 ok, 0 FAIL
  python3 run_ci_gates.py --skip Install   -> every gate PASS
  (or let .github/workflows/validate.yml run on the push)

WHAT THE OWNER SEES: no extra checking round inside a batch (a rewritten question is checked with the next batch and
named in the batch report); a question right on the line between two levels is counted by 6 reviewers instead of 3;
Final Assembly measures every remaining level with the same counting rule; a shorter batch report (full gate list
kept in a file). Still stops after each batch for "continue".
