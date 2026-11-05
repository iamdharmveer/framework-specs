# DEPLOY NOTES — release 2026.11.04 (GAP-2026-11-04-STEP7-CONTRACT-RESTORE)
Over verified production 816d5e4 (2026.11.03); commit once, push main, push main:production.
Upload EVERY file below (25 files, one NEW) in ONE commit. A partial upload fails bootstrap for
every exam (MANIFEST.json / SPEC_MANIFEST.json / SPEC_SECTIONS.json hash every engine and spec).

Engines:  blueprint_core.py (v1.30 -> v1.31)     audit_canonical.py (v2.35 -> v2.36)
          final_assembly.py (v1.12 -> v1.13)
Auditors: mock_sync_audit.py (+MS-27 STEP-CONTRACT)   audit_sync.py (+step_contract_spec)
          handshake_audit.py (H5-LEGACY, H6 in-session review, H7 D5; 66 checks)
          validate_framework_md.py (PIPELINE −MockReview/TestReview 7R)
          gen_manifest.py (tracks STEP_CONTRACTS.json)
          spec_source.py (contract floor: a stale project copy of a contract spec is never loaded)
Specs:    Framework_MockTestCreate.md (v5.90 -> v5.91)   Framework_MockReview.md (v1.0.0 -> v2.0.0, internal brief)
          Framework_MockDeliver.md (v1.24.0 -> v1.25.0)  Framework_DeliveryFooter.md (v1.38.0 -> v1.39.0)
Governance: routes.json (−MockReview, −TestReview; Framework_MockReview.md routed with MockCreate/TestCreate),
          SKILL.md + mocktestframework_SKILL.md (trigger list −MockReview, −TestReview),
          LAW_REGISTRY.json (+STEP-CONTRACT-LAW), STEP_CONTRACTS.json (NEW),
          CLAUDE.md (FRAMEWORK COUNTS 57 / 60 / 23)
Release:  VERSION (2026.11.04), CHANGELOG.md, DEPLOY_NOTES.md
Generated (must ship together):  MANIFEST.json, SPEC_MANIFEST.json, SPEC_SECTIONS.json

Verify after push (fresh clone of production):
  python3 gen_manifest.py && git diff --exit-code MANIFEST.json
  python3 build_spec_manifest.py --check && python3 spec_sections.py --check
  python3 check_triggers.py                -> TRIGGERS CONSISTENT: 23
  python3 bootstrap.py                     -> [OK] FRAMEWORK 2026.11.04 VERIFIED — 57/57
  python3 handshake_audit.py --self-test   -> HANDSHAKE AUDIT: 70 ok, 0 FAIL
  python3 validate_framework_md.py Framework_*.md   -> 0 issues across 24 file(s)
  python3 mock_sync_audit.py               -> OK — all checks agree (MS-27 included)
  python3 audit_sync.py                    -> findings: 0
  python3 run_ci_gates.py --skip Install   -> ALL GREEN

Owner action outside the repo: if the installed claude.ai skill's description lists
`MockReview, TestReview`, remove them (same line as in SKILL.md). Nothing else changes outside the repo.

WHAT THE OPERATOR SEES (every exam, every paper — no per-exam action required):
  TestCreate / MockCreate: type "continue" between batches. The final batch's response ends with
  EXACTLY [ExamCode]_[slug]_Create.docx + [ExamCode]_registry.json. The independent review, its
  repairs and its second round run inside that response; no review packet, no new chat, no
  verdict file, no --resume. If a response is interrupted, type "continue" in the same chat.
  A-TEMPLATE on a project whose Step 5 predates the QUALITY measurement prints DORMANT and never
  stamps an item; no paper is NOT CERTIFIED because of it.

MIGRATION:
  - Paper parked at AWAITING_REVIEW / REVIEW_REPAIR under 2026.11.03: in the SAME author chat type
    "continue" (or TestCreate P[N] resume). It runs the review internally and delivers the two
    files. A verdict file already produced is used if attached (found by content). If that chat's
    working files are gone, regenerate the paper — nothing was committed for it.
  - Paper already committed NOT CERTIFIED only by A-TEMPLATE: TestDeliver / MockDeliver re-certifies
    it automatically (one informational line); no --accept-uncertified needed.
  - A project holding an OLD copy of Framework_MockTestCreate.md / Framework_MockReview.md /
    Framework_MockDeliver.md / Framework_DeliveryFooter.md in Files: handled AUTOMATICALLY — the
    copy is below the contract floor, is not loaded, and Step 0 prints [STALE — NOT LOADED].
    Deleting it from Files is optional tidying only.
  - Optional, never blocking: re-run Step 5 under this release to turn the measured quality
    controls (template caps included) from DORMANT to ACTIVE for that exam.
