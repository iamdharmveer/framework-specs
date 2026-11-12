# DEPLOY NOTES — release 2026.11.11 (GAP-2026-11-11-NONORGANIC-MOCK-FIDELITY + GAP-2026-11-11-BATCH-VERIFICATION — every subject, every item measured against the exam's own papers, every question verified in its own batch)
Over verified production b0db268 (2026.11.10); commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

UPLOAD LIST (27 files = every file that differs from production; none is new):
CHANGELOG.md
DEPLOY_NOTES.md
Framework_Blueprint.md                  (v1.65.0 — NEW §4-1c nested allocation, INVARIANTS 9-10, BV-11, §7-10 NF targets, S14-9)
Framework_DeliveryFooter.md             (v1.46.0 — NEW §LADDER-NF AMBER lines)
Framework_MockTestAnalyse.md            (v2.62.0 — §5-NF paper count + crosswalk / manifest_hash; stamps v2.62)
Framework_MockTestCreate.md             (v6.1 — NEW S0-BV + S4-7 STEP A2 (every question verified in its batch); NEW S0-NF-0..9; C4 for every item; C9 MIP; S13-2P NF measure; S13-4 text series registry)
Framework_MockTestOrchestrate.md        (v1.3.0 — GRADE_REQUEST / GRADE RETURNED (O3-9), ROTATE)
Framework_PYQExplain.md                 (v2.32 — decisions / mip / given_in_stem / class / computation_generic / concept on every record)
Framework_ScopedBlueprint.md            (v1.15.0 — §4-NF one level down)
LAW_REGISTRY.json                       (+LAW-NF-1..11, +LAW-BV-1..6)
MANIFEST.json
SHA256SUMS.txt
SPEC_HISTORY.md
SPEC_MANIFEST.json
SPEC_SECTIONS.json
STEP_CONTRACTS.json                     (override floors raised for the seven edited specs)
VERSION                                 (2026.11.11)
analyse_engine.py                       (v1.6 — paper_key; stamps v2.62)
audit_canonical.py                      (v2.41 — A-ALLOC, A-AXIS2 per subject x Part measured, A-OPTPART, A-INTRADUP, A-KEYLEAK, A-CLASSMIX, A-SUBJBAND, A-STEMFIG)
audit_sync.py                           (nonorganic_fidelity_rule, batch_verification_rule, BV-COVERAGE)
blueprint_core.py                       (v2.1 — Cluster NF + Cluster BV)
bootstrap.py                            (worker states GRADE_REQUEST, ROTATE)
figure_types.py                         (v1.4 — DATA_FIGURE_KINDS + render_data_figure)
final_assembly.py                       (v1.17 — QINDEX_NF_FIELDS, nf_disclosed, manifest_hash; bv_batch_step = S4-7 STEP A2)
handshake_audit.py                      (+25 H-BV checks: the whole in-batch chain end to end, 211 checks)
paper_pipeline.py                       (qindex_count_band mirror: a settled / last-resort row counts at its slot)
routes.json                             (MockCreate / TestCreate also route figural_vision.py — the in-batch vision read-back)

SKILL CHANGE: none (SKILL.md / mocktestframework_SKILL.md unchanged — no re-sync needed).

AFTER DEPLOY (automatic — no user step): the first PYQExtract / MockTestAnalyse run re-synthesises the per-paper
statistics (F-02); the first Create run back-fills the new PYQ record fields (O-BACKFILL); `MockBlueprint --refresh`
writes the new targets for UNREGISTERED mocks only. Delivered papers are never re-certified.
For CSIR NET Chemical Sciences run, in order: PYQExtract (--synthesise), MockBlueprint --refresh, then TestCreate.

OPTIONAL (owner, any time; never required): <ExamCode>_expert_grades.json in an exam project = {"<paper>:<q>": "Easy|Medium|Hard"}
for a sample of real items; when present the Blueprint checks the blind-grade calibration against it (amendment C).

Verify after push (fresh clone of production):
  pip install matplotlib pillow numpy scipy fonttools rdkit python-docx scikit-image openpyxl --break-system-packages
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT
  python3 bootstrap.py                     -> VERIFIED (60/60)
  python3 blueprint_core.py --self-test    -> SELF-TEST: 1399/1399 PASS
  python3 audit_canonical.py --self-test   -> SELF-TEST: 633/633 PASS
  python3 analyse_engine.py --self-test    -> 309 passed, 0 failed
  python3 bootstrap.py --self-test         -> SELF-TEST: 70/70 PASS
  python3 paper_pipeline.py --self-test    -> SELF-TEST: 257/257 PASS
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 211 ok, 0 FAIL
  python3 final_assembly.py --self-test    -> SELF-TEST: 187/187 PASS
  python3 figure_types.py --self-test      -> SELF-TEST: 988/988 PASS
  python3 run_ci_gates.py --skip Install   -> every gate PASS
  (or let .github/workflows/validate.yml run on the push)

WHAT THE OWNER SEES: mocks whose subject / topic counts per Part match the real paper in EVERY mock, the real formats
(match lists, multi-statement items) for every subject, difficulty measured for every item with a per-subject recipe,
no repeated templates or answer leaks inside a paper, metal figures drawn the exam's way, and an AMBER line naming any
shortfall the bounded repair could not close. Every batch is graded by fresh graders and solvers BEFORE it is
delivered (one write per question, at most one rewrite); Final Assembly does not re-write questions for difficulty.
Nothing new can stop a run.

A PAPER PARKED BEFORE THIS RELEASE (e.g. the Organic test stopped at REVIEW_REPAIR): its batches were written without
in-batch grading, so on "continue" it finishes the old way (its flagged repairs). To get the new behaviour, start
that test again with TestCreate.
