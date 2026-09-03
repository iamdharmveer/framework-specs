# DEPLOY NOTES — release 2026.09.03.1 (Release C — GAP COMPLETE)

Single push over the verified 2026.09.02.2 production. 15 files: copy all
over the production checkout, commit once, push.

Post-push checks (fresh clone, deps: python-docx matplotlib pillow numpy
rdkit openpyxl): bootstrap.py => 53/53 VERIFIED at 2026.09.03.1;
regression_pyq_fixtures 140/140; blueprint_core 661/661; corpus_io 383/383;
syllabus_provenance 23/23; analyse_engine 216/216; explain_engine 196/196;
mock_sync_audit => "OK — all checks agree" AND --self-test 69/69;
validate_framework_md Framework_*.md => 0 issues / 23 specs;
run_ci_gates.py fully green. No excuse-notes: a red gate blocks, always.

With this release every GAP stage (A declaration/detection, B crosswalk/
era/labeling, C allocation/generation) is live. The driving-exam sequence
before any new-syllabus mock ships: PYQDraft (diff) -> crosswalk approval
-> PYQScan/PYQApprove (R30) -> PYQSort -> PYQCount -> MockTestAnalyse ->
MockBlueprint -> MockTestCreate -> MockDeliver. Reminder: unify the
ExamCode spelling across each transitioning project's files first (HS-ST4
stops on mismatch by design).
