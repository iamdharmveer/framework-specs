# DEPLOY NOTES — release 2026.10.27 (GAP-2026-10-27-SCOPED-STIMULUS-SECTIONS)
Over verified production 0533b95; commit once, push main, push main:production.

Changed:  Framework_MockTestCreate.md (v5.86 -> v5.87)
Release:  VERSION, CHANGELOG.md, DEPLOY_NOTES.md
Generated (must ship together — bootstrap verifies every session against MANIFEST.json):
          MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 bootstrap.py                    -> [OK] FRAMEWORK 2026.10.27 VERIFIED — 53/53

Per exam: NOTHING to do. A scoped TestCreate that hard-stopped at S3-12b ("exam_section ... is not
a section of this exam") simply re-runs the same trigger.
