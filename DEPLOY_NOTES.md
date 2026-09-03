# DEPLOY NOTES — patch 2026.09.03.2 (correspondence k-floor hardening)
9 files over the verified 2026.09.03.1 production; commit once, push.
Post-push (deps: python-docx matplotlib pillow numpy rdkit openpyxl):
bootstrap 53/53 at 2026.09.03.2; fixtures 144/144; syllabus_provenance
23/23; mock_sync_audit "OK" + --self-test 69/69; validator 0/23;
run_ci_gates green. No excuse-notes: a red gate blocks, always.
