# Changelog

## 2026.07.18.1
- Framework_MockDeliver.md v1.6 -> v1.7.

## 2026.07.18
- validate_framework_md.py -> v2.8: adds Check T (cross-file token contract) and Check U (JSON
  producer/consumer field contract); generalises cross-file RA/MANDATE anchor resolution; drops
  the "equivalent"-exemption now that the MANDATE 8/9 prose is root-fixed in the specs.
  Re-added 'ScopedBlueprint': '6S' to the PIPELINE dict.
- Framework_MockTestCreate.md, Framework_MockTestAnalyse.md, Framework_PYQAnalyse.md,
  Framework_MockTestCreateAudit.md updated (MANDATE 8/9 "equivalent" prose removed at source).

## 2026.07.17.1
- Dual-path engine sourcing: Blueprint (Step 6), ScopedBlueprint (Step 6S), MockTestExplain
  (Step 9), MockTestExplainAudit (Step 10) now load their engines (blueprint_core.py /
  explain_engine.py / explain_audit_gate.py) from the framework clone (/tmp/fw) with fallback
  to the project Files (/mnt/project). GitHub-connected projects no longer need the engines
  uploaded to their Files; direct-upload projects continue to work.
- Framework_Blueprint.md v1.31 -> v1.32 (dual-path gate now in the spec source);
  Framework_MockTestAnalyse.md v2.24.5 -> v2.24.6; Framework_MockTestCreateAudit.md v2.7.3 -> v2.7.4.

## 2026.07.17
- NEW spec Framework_ScopedBlueprint.md v1.5 (Step 6S — scoped subject/topic/subtopic test
  blueprints). Wired into routes.json / PIPELINE / skill (14 triggers).
- NEW shared engine blueprint_core.py (added to the tracked set; self-test 33/33). Bootstrap
  count is now 16/16. Framework_Blueprint.md v1.27 -> v1.31 (allocation math extracted into
  blueprint_core.py). NOTE: blueprint_core.py must be uploaded to each project's /mnt/project/
  or Step 6/6S HARD STOPs (operational, outside this repo).
- Framework_MockTestAnalyse.md v2.24.2 -> v2.24.5.
- Framework_MockTestCreate.md v5.20 -> v5.23; Framework_MockTestCreateAudit.md v2.7.2 -> v2.7.3;
  Framework_MockDeliver.md v1.5 -> v1.6.
- Framework_MockTestExplain.md v1.14 -> v1.15; Framework_MockTestExplainAudit.md v1.8 refresh.

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
