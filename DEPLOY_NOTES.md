# DEPLOY NOTES — release 2026.11.01 (GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY)
Over verified production 4ab7be4 (2026.10.27); commit once, push main, push main:production.

NEW:      figure_types.py (v1.0 — the figure-type registry; routed to PYQExtract, MockBlueprint,
          ScopedBlueprint, MockCreate, TestCreate, MockExplain, TestExplain)
Engines:  corpus_io.py (v1.15 -> v1.16)         paper_pipeline.py (v5.39 -> v5.40)
          final_assembly.py (v1.8 -> v1.10)      blueprint_core.py (v1.27 -> v1.28)
          audit_canonical.py (v2.31 -> v2.33)   analyse_engine.py (Phase-C normalisation, QV-14 line)
          explain_engine.py (canonical_structure twin — byte-identical to corpus_io's)
Specs:    Framework_MockTestCreate.md (v5.87 -> v5.88)      Framework_ScopedBlueprint.md (v1.10.1 -> v1.11.0)
          Framework_Blueprint.md (v1.60.1 -> v1.61.0)      Framework_MockTestAnalyse.md (v2.57.2 -> v2.57.3)
          Framework_MockTestExplain.md (v1.51.1 -> v1.51.2) Framework_MockDeliver.md (v1.22.0 -> v1.23.0)
          Framework_DeliveryFooter.md (v1.35.1 -> v1.36.0)
Governance: LAW_REGISTRY.json (+3 laws), mock_sync_audit.py (MS-21..MS-25), audit_sync.py (+3 detect rules),
          routes.json, gen_manifest.py (TRACKED_PY + figure_types.py), CLAUDE.md (counts 54 / 58),
          SKILL.md + mocktestframework_SKILL.md (18 routed engines)
Release:  VERSION, CHANGELOG.md, DEPLOY_NOTES.md
Generated (must ship together — bootstrap verifies every session against MANIFEST.json):
          MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 bootstrap.py                    -> [OK] FRAMEWORK 2026.11.01 VERIFIED — 54/54
  python3 run_ci_gates.py --skip Install  -> ALL GREEN (verified in the release environment before packaging)

Per exam: NOTHING to do for the engines (they come from the clone). Three notes:
  1. The per-exam [ExamCode]_mock_test_audit.py copy is refreshed automatically by Step 7 S3-9
     from the verified clone when it differs (v5.78+); a stale copy of a FIGURAL paper is a
     HARD STOP at S13-4c by design (no A-FIGTYPE-KIND line).
  2. A scoped blueprint built by ScopedBlueprint < v1.11.0 still runs: S3-2a prints the
     figural_present correction and S13-4 commits the figure record on existence. Regenerate
     the scoped blueprint (ScopedBlueprint P[N] …) to retire the printed line and to get the
     KIND-COVERAGE verdict recorded in the blueprint.
  3. Optional: exam_config.figure_fallback_policy = "text_disclosed" lets a subtopic whose
     dominant figure type is UNSUPPORTED (photograph / micrograph families) render TEXT with a
     footer disclosure instead of HARD STOPPING at Step 6. Default: hard_stop.
  A project that OVERRIDES any of the seven changed specs in its Files section opts out of
  that spec's part of this fix (CLAUDE.md project-first); remove or update the override.
