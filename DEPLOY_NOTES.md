# DEPLOY NOTES — patch 2026.09.14.3 (GAP-2026-09-14-SCAN-ORPHAN-AT-SOURCE)
11 files over the verified 2026.09.14.2 production; commit once, push main, push main:production.

Changed:  Framework_PYQScan.md (v1.5.0 -> v1.6.0), Framework_PYQApprove.md (v1.2.0 -> v1.3.0),
          reconcile_taxonomy.py (v1.4 -> v1.5, SCHEMA_VERSION unchanged)
Release:  VERSION, CHANGELOG.md, SPEC_HISTORY.md, DEPLOY_NOTES.md
Generated (must ship together — bootstrap verifies every session against MANIFEST.json):
          MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json, SHA256SUMS.txt

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 bootstrap.py            -> [OK] FRAMEWORK 2026.09.14.3 VERIFIED — 53/53
  python3 reconcile_taxonomy.py --self-test   -> 104/104

Operator tool shipped alongside (NOT a repo file): audit_orphans.py — read-only fleet audit
of [ExamCode]_classifications.json + _scan_progress.json pairs. Run before the next PYQApprove
of any exam scanned under <= PYQScan v1.5.0; a flagged exam is repaired by resuming PYQScan
under v1.6.0, never by hand.
