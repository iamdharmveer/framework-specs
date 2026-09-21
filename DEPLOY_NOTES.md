# DEPLOY NOTES — release 2026.09.21 (GAP-2026-09-21-LINKED-PLACEMENT)
Over verified production e8362cd; commit once, push main, push main:production.

Changed:  Framework_MockTestCreate.md (v5.84 -> v5.85), Framework_MockTestAnalyse.md (v2.57.1 -> v2.57.2),
          Framework_DeliveryFooter.md (v1.35 -> v1.35.1),
          blueprint_core.py (Cluster SG), audit_canonical.py (v2.30), final_assembly.py (v1.7),
          mock_sync_audit.py (MS-11 delivery-name set), validate_framework_md.py (Check AM contract)
Release:  VERSION, CHANGELOG.md, DEPLOY_NOTES.md
Generated (must ship together — bootstrap verifies every session against MANIFEST.json):
          MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 bootstrap.py                    -> [OK] FRAMEWORK 2026.09.21 VERIFIED — 53/53
  python3 blueprint_core.py --self-test   -> 727/727
  python3 audit_canonical.py --self-test  -> 352/352
  python3 final_assembly.py --self-test   -> 124/124

Per exam, ONCE, before its next NEW mock/test (a paper already in progress is unaffected):
  PYQExtract --stimulus-profile   (needs [ExamCode]_analysis_progress.json in Project Files)
  -> upload [ExamCode]_stimulus_profile.json to Project Files.
  Until then TestCreate/MockCreate HARD STOP at the start of a new paper (S3-12b SAFETY LOCK).
  SSC_CGL_TIER2: the profile is shipped with this release — upload it at deploy time.
