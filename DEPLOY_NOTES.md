# DEPLOY NOTES — release 2026.11.23 (GAP-2026-11-17-CERT-DISCLOSED-CONTRACT) over release 2026.11.22
Built on production 95899e0 (release 2026.11.22). Commit once, push main, push main:production.
Upload EVERY file below in ONE commit, flat (no folders). A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).
If production is NOT exactly 95899e0 when you deploy (any other change on it), stop and send me the production
commit. The bundle must be rebuilt on that commit, never merged by hand.

UPLOAD LIST (13 files = the 11 files that differ from 2026.11.22 + DEPLOY_NOTES.md + SHA256SUMS.txt; none is new):
CHANGELOG.md
DEPLOY_NOTES.md                         (this file)
Framework_MockTestCreate.md             (v8.2 — S3-14/S3-16 producer_release; S13-2F CERT-CONTRACT stop; NEW §S13-CERT;
                                         S13-4c CERT-CONTRACT branch, no heal; registry staged at S13-7 only)
LAW_REGISTRY.json                       (NEW LAW-CERT-1 ONE-CERTIFICATE-CONTRACT; LAW-BC-8 amended)
MANIFEST.json                           (regenerated)
SHA256SUMS.txt                          (checksums of this upload)
SPEC_MANIFEST.json                      (regenerated)
SPEC_SECTIONS.json                      (regenerated)
STEP_CONTRACTS.json                     (floor: Create 8.2; deliverables / end states / user actions unchanged)
VERSION                                 (2026.11.23)
audit_canonical.py                      (v2.44 — cert_contract, gate_cert, gate_cert_late, certificate schema 3,
                                         AUDITOR_ID, per-batch label; self-test 674 checks, CERTGAP-1..30)
audit_sync.py                           (NEW CERT-CONTRACT family; detect rule certificate_contract_rule)
handshake_audit.py                      (H5 schema 3; NEW H5-CERT-DISCLOSED x4, H5-V7-SIDECAR; 267 checks)

SKILL CHANGE: none. TRIGGERS: unchanged.

AFTER DEPLOY:
  1. Nothing to change in any of the ~200 projects. Every run audits with the verified repo audit_canonical.py
     (Create S3 copies it over a differing project copy). Replacing a stale [ExamCode]_mock_test_audit.py in a
     project's Files only silences the "AUDITOR REFRESHED" notice.
  2. If a project's Files section holds a Framework_MockTestCreate.md copy below 8.2, it is not loaded (floor) —
     remove it to silence the [STALE — NOT LOADED] line.
  3. A paper parked at "HARD STOP [HS:INFRA] (S13-4c re-sweep ...)" with an A-CERT "unresolved item finding(s)" line:
     type `continue` in that same chat. Step 0 re-verifies the new commit; S13-2F re-runs, writes a schema-3
     certificate and S13-4c passes (CERTIFIED WITH DISCLOSURES). No question is re-authored.
     Do NOT upload the [ExamCode]_registry.json the stopped run left in outputs; the resumed run removes it and
     delivers the certified one.

VERIFY BEFORE PUSH (on the commit, before main:production):
  1. python3 gen_manifest.py && git diff --exit-code MANIFEST.json      -> no diff
  2. python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  3. python3 bootstrap.py                                               -> 60/60 VERIFIED
  4. python3 run_ci_gates.py --skip Install                             -> every step PASS
  5. sha256sum -c SHA256SUMS.txt                                        -> every file OK

ROLLBACK: re-deploy the 2026.11.22 bundle (production 95899e0).
