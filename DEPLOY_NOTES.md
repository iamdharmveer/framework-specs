# DEPLOY NOTES — combined push: 2026.09.02.1 (Release A) + 2026.09.02.2 (Release B)
# Bundle rev 2 — supersedes the MS-3-blocked bundle. 24 files.

One manual deploy covers BOTH releases of GAP-2026-09-01-SYLLABUS-TRANSITION
(rev 4.5). Copy every file over the production checkout; place validate.yml
at .github/workflows/validate.yml; commit once; push. VERSION lands at
2026.09.02.2.

CHANGES vs the blocked bundle (deploy report DEPLOY_BLOCKED_..._MS3):
- Framework_MockTestAnalyse.md: the three emitted-stamp contract lines now
  read v2.57 (header parity — MS-3).
- analyse_engine.py JOINS the bundle: its three stamp assignments read
  v2.57 per the spec's CROSS-FILE SYNC RULE (MINOR bump => engine bump),
  with a changelog note. Everything else in it is byte-identical.
- .github/workflows/validate.yml: CI now installs rdkit + openpyxl, waking
  the 14 corpus_io assertions and explain_engine V31 that were dormant on
  every CI run (the deploy report's §7 note — closed).
- This file: the previous "known pre-existing explain_engine failure" note
  was WRONG — a missing rdkit in the build container, not a corpus defect.
  With deps installed the measured results are explain_engine 196/196,
  corpus_io 383/383, analyse_engine 216/216, mock_sync_audit exit 0.
  No excuse-notes remain: a red gate blocks, always.

Post-push checks (fresh clone, after `pip install python-docx matplotlib
pillow numpy rdkit openpyxl`): bootstrap.py => 53/53 VERIFIED at
2026.09.02.2; regression_pyq_fixtures 124/124; blueprint_core 661/661;
corpus_io 383/383; syllabus_provenance 23/23; analyse_engine 216/216;
explain_engine 196/196; mock_sync_audit => "OK — all checks agree";
validate_framework_md Framework_*.md => 0 issues / 23 specs;
run_ci_gates.py fully green.

Release C (Transition Allocation & Generation, GAP §5) awaits operator
go-ahead after this push is verified.
