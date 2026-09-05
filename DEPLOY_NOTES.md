# DEPLOY NOTES — patch 2026.09.05.1 (syllabus filename tolerance)
13 files over the verified 2026.09.03.3 production; commit once, push.
Files: blueprint_core.py, regression_pyq_fixtures.py,
Framework_PYQDraft.md, Framework_PYQCore.md,
Framework_NotesBlueprint.md, VERSION, CHANGELOG.md, SPEC_HISTORY.md,
DEPLOY_NOTES.md, MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json,
SHA256SUMS.txt. Includes R-e: drift identity by sha256, names display-only
(FX-ST-RE1..RE4). Post-push: regression_pyq_fixtures 156/156;
validate_framework_md 0 issues; run_ci_gates green. Acceptance: with
the CSIR project's hyphen-stripped files
(CSIR_NET_LIFESCIENCES_Syllabus_202612/202606.pdf) and Effective
From 2026-12, PYQDraft resolution must end RESOLVED with CURRENT =
the 202612 file; then any drift-guarded step (e.g. PYQSort) must pass
with NO HS-ST10 despite the stored block naming the hyphenated forms. No excuse-notes: a red gate blocks, always.

# DEPLOY NOTES — patch 2026.09.03.3 (PYQFormat v1.6.0 page border)
9 files over the verified 2026.09.03.2 production; commit once, push.
Post-push (deps: lxml python-docx):
bootstrap 53/53 at 2026.09.03.3; validate_framework_md 0 issues;
spec_sections --check clean; run_ci_gates green. Acceptance: run
PYQFormat on one real paper and open the output in Microsoft Word —
the border frames every page. No excuse-notes: a red gate blocks, always.
