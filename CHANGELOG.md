# Changelog

## 2026.07.23
- Framework_PYQFormat.md v1.0 -> v1.3 (PYQ-3, self-contained formatter):
  v1.1 removes the per-question date/session tag paragraphs (only sanctioned deletion);
  v1.2 restyles explanation tag headers into colored bands + marker-glyph swaps
  (⬛->📘/🧮, ❌->⚠️), machine-verified by a full text-stream integrity check (S8-8);
  v1.3 promotes the exam header + IFAS footer to real page header/footer parts that
  repeat on every page, and updates the footer tagline. Trigger/step unchanged; no
  framework engine; bootstrap stays 21/21.

## 2026.07.22
- NEW PYQ Explanation Pipeline — 4 specs: PYQExplain (PYQ-1), PYQExplainAudit (PYQ-2),
  PYQFormat (PYQ-3), PYQDeliver (PYQ-4). Wired into routes.json / PIPELINE / skill
  (19 -> 23 triggers); tracked set 17 -> 21 (bootstrap now 21/21). PYQ-1/PYQ-2 reuse
  explain_engine.py (+ explain_audit_gate.py for PYQ-2); PYQ-3/PYQ-4 are self-contained
  (write their own format_pipeline.py / pyq_deliver_pipeline.py, no framework engine).
- validate_framework_md.py — S2-EXPLAINGATE now fires on an actual gate invocation
  (`explain_audit_gate.py --`) or the AUDIT-COMPLETION-GATE output, not on a bare name-drop,
  so specs that only DISCLAIM the gate (PYQ-1 delegation note; PYQ-3/PYQ-4 NOT-REQUIRED
  lists) no longer false-positive. Genuine gate-users (Step 10 / PYQ-2) still fully checked.
- GAP-2026-07-22-001 section<->subject mapping chain (shipped atomically):
  MockTestCreate v5.29 -> v5.30 (position-based question-type dispatch, §6);
  MockTestCreateAudit v2.9.1 -> v2.9.2 (position-based question-type in audit);
  MockTestAnalyse v2.24.8 -> v2.24.9 (BUG 1 — sections[].subjects);
  Blueprint v1.34 -> v1.35 (BUGS 2-4 — section<->subject mapping);
  ScopedBlueprint BLUEPRINT_SCHEMA_VERSION 1.23 -> 1.35 (schema sync to Blueprint);
  DeliveryFooter Step 5 deliverable-count doc fix (5 -> 6 files).
- routes.json — PYQ explanation triggers reordered to end (no functional change; syncs the
  repo to the generator's emit order).

## 2026.07.21
- NEW engine paper_pipeline.py — shared naming/numbering/registry plumbing for Steps 6-11
  (self-test 37/37; added to tracked set -> bootstrap now 17/17). Added 5 Test* trigger aliases
  (TestCreate/TestCreateAudit/TestExplain/TestExplainAudit/TestDeliver -> 19 triggers), wired into
  routes.json / PIPELINE / skill.
- Specs: MockTestCreate v5.29, MockTestCreateAudit v2.9.1, MockTestExplain v1.20, MockTestExplainAudit
  refresh; Blueprint v1.32 -> v1.34; MockTestAnalyse v2.24.7 -> v2.24.8; PYQAnalyse v2.15 -> v2.16;
  MockDeliver v1.8 -> v1.9; ScopedBlueprint v1.5 -> v1.7.
- Added manifest_to_taxonomy_xlsx.py (untracked helper: subtopic_manifest.json -> taxonomy Excel).

## 2026.07.20
- explain_engine.py core self-test 44/44 -> 62/62 (audit stays 10/10). MockTestExplain -> v1.18 and
  MockTestExplainAudit P0 corrected to 62-of-62, so Step 9/10 pre-flight demands exactly what the
  engine prints. Deployed as a version-matched bundle (engine + both Explain specs).
- MockTestCreate v5.24 -> v5.27; MockTestCreateAudit v2.7.6 -> v2.8.1; MockTestExplain v1.15 -> v1.18;
  MockTestExplainAudit v1.8 refresh; MockDeliver v1.7 -> v1.8.

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
