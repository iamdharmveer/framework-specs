# DEPLOY NOTES — release 2026.11.13 (GAP-2026-11-13-DIFFICULTY-RUBRIC + GAP-2026-11-13-RUN-NOT-READ — one ruler for past and new questions; code that is run, not read)
Over verified production 6c1b7f2 (2026.11.12); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (19 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_DeliveryFooter.md             (v1.48.0 — AMBER line for a band judged, not counted)
Framework_MockTestCreate.md             (v6.3 — S1-0R PYTHON SESSION; S0-BV BV-10..12; 48 blocks marked ENGINE-RUN)
Framework_MockTestOrchestrate.md        (v1.5.0 — a worker problem switches to DIRECT MODE, never a stop)
LAW_REGISTRY.json                       (+LAW-BV-10..12)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_HISTORY.md                         (moved version entries)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated — engine_ranges)
STEP_CONTRACTS.json                     (floors: Create 6.3, Orchestrate 1.5.0, DeliveryFooter 1.48.0)
VERSION                                 (2026.11.13)
audit_specs_ext.py                      (FINAL read size excludes engine-run code)
blueprint_core.py                       (v2.3 — Cluster BR: reviewers' counts scored with the PYQ rubric)
bootstrap.py                            (--session-start / --run-block: the python session of a paper; worker prompt)
final_assembly.py                       (v1.19 — no reviewer is never a stop)
handshake_audit.py                      (217 checks: + rubric band, + run-not-read)
spec_sections.py                        (engine_ranges: marked code is never served by the read)

routes.json: UNCHANGED (do not upload).
SKILL CHANGE: none (SKILL.md / mocktestframework_SKILL.md unchanged — no re-sync needed).

AFTER DEPLOY: start the Organic test fresh with TestCreate. A paper begun under an earlier release can be continued:
its saved grades are kept, new batches use the new measurement.

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx scikit-image openpyxl --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT
  python3 bootstrap.py                     -> VERIFIED (60/60)
  python3 blueprint_core.py --self-test    -> SELF-TEST: 1417/1417 PASS
  python3 final_assembly.py --self-test    -> SELF-TEST: 190/190 PASS
  python3 bootstrap.py --self-test         -> SELF-TEST: 85/85 PASS
  python3 spec_sections.py --self-test     -> SELF-TEST: 35/35 PASS
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 217 ok, 0 FAIL
  python3 run_ci_gates.py --skip Install   -> every gate PASS
  (or let .github/workflows/validate.yml run on the push)

WHAT THE OWNER SEES: each question's level is measured with the same scoring rule that set the levels of the
exam's past questions (tested on 31 real CSIR Organic questions: 22 matched, was 14; every miss one level); the
writer gets the slot's real target from past questions of the same topic; each worker reads about 100,000 fewer
tokens and never retypes the setup code; no stop when a reviewer or a worker cannot start. Still stops after each
batch for "continue", as before.
