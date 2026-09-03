# DEPLOY NOTES — patch 2026.09.03.3 (PYQFormat v1.6.0 page border)
9 files over the verified 2026.09.03.2 production; commit once, push.
Post-push (deps: lxml python-docx):
bootstrap 53/53 at 2026.09.03.3; validate_framework_md 0 issues;
spec_sections --check clean; run_ci_gates green. Acceptance: run
PYQFormat on one real paper and open the output in Microsoft Word —
the border frames every page. No excuse-notes: a red gate blocks, always.
