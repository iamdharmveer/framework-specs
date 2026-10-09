# DEPLOY NOTES — release 2026.10.09 (GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC)
Over verified production 9f43769; commit once, push main, push main:production.

Changed:  Framework_MockTestCreate.md (v5.85 -> v5.86), Framework_MockTestExplain.md (v1.51.0 -> v1.51.1),
          audit_canonical.py (v2.31), final_assembly.py (v1.8)
Release:  VERSION, CHANGELOG.md, DEPLOY_NOTES.md
Generated (must ship together — bootstrap verifies every session against MANIFEST.json):
          MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 bootstrap.py                    -> [OK] FRAMEWORK 2026.10.09 VERIFIED — 53/53
  python3 audit_canonical.py --self-test  -> 384/384
  python3 final_assembly.py --self-test   -> 139/139

Per exam: NOTHING to do. Step 7 now refreshes [ExamCode]_mock_test_audit.py from the verified
clone automatically whenever the project copy differs (prints "AUDITOR REFRESHED"). Replacing the
project file with audit_canonical.py (same [ExamCode]_ name) only silences that notice.
A paper already in progress resumes unaffected; its Final Assembly runs on the fixed engines.
