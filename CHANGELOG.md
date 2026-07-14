# Changelog

## 2026.07.14
- Framework_PYQPrepare.md: v1.6 -> v1.7.
- Added mocktestframework_SKILL.md — canonical account-level skill (STEP 0 load-and-verify
  bootstrap; trigger list synced to the live 13-trigger routing). Added an explicit no-DR-mirror
  guard that hard-stops when MIRROR == PRIMARY instead of silently re-cloning the same URL.
- Added check_triggers.py — enforces that the skill trigger list, routes.json, and the validator
  PIPELINE dict stay in sync; wired into CI (validate.yml) so drift fails the build.
- Deprecated docs/CUSTOM_INSTRUCTIONS.md to a pointer at the skill (single source of truth).

## 2026.07.12
- Deliverable filename rename across the delivery contract and the Create/Explain/Deliver
  specs: Step 7 -> Create, Step 8 -> Create_Complete, Step 9 -> Explanation,
  Step 10 -> Explanation_Complete, Step 11 -> Final.
- Specs updated to: MockTestAnalyse v2.24.2, MockTestCreate v5.20, MockTestCreateAudit v2.7.2,
  DeliveryFooter v1.6, MockTestExplain v1.14, MockTestExplainAudit v1.8 (content refresh),
  MockDeliver v1.5.
- validate_framework_md.py: permanently exempt "MANDATE/RA N equivalent" descriptive phrasing
  from the anchor checks (O-MANDATE/N-RA false-positive fix; genuine dangling refs still caught).
- MockDeliver: fixed stray internal "End of v1.3" marker.
- Added CLAUDE.md documenting the release-manager protocol (approved_framework, seal_release,
  guardrails) so future sessions inherit it.

## 2026.07.11
- Framework_MockTestAnalyse.md: v2.24 -> v2.24.1
- Framework_Blueprint.md: v1.27 content refresh
- Framework_MockDeliver.md: v1.3 -> v1.4
- Framework_MockTestExplain.md: v1.12 -> v1.13
- Framework_MockTestExplainAudit.md: v1.7 -> v1.8
- explain_engine.py: FIGURE-section tests replaced with FIGURAL-NO-FIGURE-SECTION regression lock (self-test 44/44, audit 10/10)
- routes.json: 10 -> 13 triggers (Framework_DeliveryFooter.md on all routes; Blueprint renamed to MockBlueprint; new PYQDraft/PYQScan/PYQApprove; engine deps on explain routes)
- tooling: validate_framework_md.py hardened (word-boundary stale markers, corpus-wide MANDATE/RA anchor resolution, accepts "vX changes:" changelog format); CI gates validator on Framework_*.md and installs python-docx; .verified gitignored; auto-manifest workflow removed

## 2026.07.10
- Initial release of the version-pinned, integrity-verified framework repo.
- 11 .md specs + 3 .py engines/gates under load-and-verify gate (bootstrap.py).
