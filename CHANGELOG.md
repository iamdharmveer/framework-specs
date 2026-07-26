# Changelog

## 2026.07.26.2
- GAP-2026-07-26-002 closed (image-option integrity + intra-spec wiring). Three parts:
- (1) is_option consolidated to ONE engine predicate (audit_deep [XSPEC-DRIFT]). v2.34/v2.35
  made is_option() image-option-aware in MockTestAnalyse only; the same-named copies in PYQSort
  and PYQAnalyse kept the text-only form while their docstrings still claimed alignment. Not
  cosmetic: PYQSort USES its copy to count options, so the defect fixed in Step 5 was live in
  Step 1 — measured on IIT_JAM_BIOTECHNOLOGY 2022, 156 options counted against 160 actual. Fix:
  corpus_io v1.5 -> v1.6 now owns is_option + BARE_OPT_PATTERNS + para_has_image as the single
  shared predicate; MockTestAnalyse v2.35 -> v2.36, PYQAnalyse v2.28 -> v2.29, PYQSort v1.16 ->
  v1.17 all delegate (is_option = corpus_io.is_option), and PYQSort passes the paragraph element
  at both call sites so image options are actually counted.
- (2) IMG-6 probe protocol hardened (PYQPrepare v1.9.1 -> v1.10). The v1.6 protocol was
  single-attempt/single-token and recorded nothing, while score_vision_probe() returned False on
  an empty string — so "I did not look" was indistinguishable from a blind session and produced a
  false session-terminating halt in Step 5 on first production use. Now 3 attempts, 3 distinct
  tokens, observation mandatory.
- (3) New auditor audit_callgraph.py (intra-spec call-graph): asserts every documented-required
  parameter is supplied at each call site, every multi-return function has one shape, and every
  public engine function is reached from executable spec code (not prose). Now tracked in
  SPEC_MANIFEST (33 -> 34 files). blueprint_core self-test 184/184; corpus_io 228/228.
- Follow-ups (recorded): add an is_option self-test fixture to corpus_io (bare-marker + OPT_PATTERNS
  cases); update audit_specs_ext's stale V-SYNC that false-fires on the delegation adapters.

## 2026.07.26.1
- GAP-2026-07-26-001 (a multi-paragraph stem is not a heading): PYQSort EC-S8 emits stems
  whose continuation lines are bold, not-date, not-option, not-next-question — character for
  character the level-3 taxonomy-heading predicate in `blueprint_core.is_taxonomy_heading()`.
  Level 3 is the only taxonomy level with no textual prefix, so boldness was its sole positive
  signal; the moment the producer emitted bold body text, a stem continuation and a subtopic
  heading became the same object. Two classes, one predicate, on opposite sides of the repo,
  never compared.
- Fix: `is_taxonomy_heading()` now takes the next paragraph's text (`is_taxonomy_heading(para,
  is_option, next_text)`) so a line followed by more stem body is no longer classified as a
  heading; MockTestAnalyse S3-2 passes `next_text` at both extraction loops — an older engine
  raises `TypeError` rather than silently truncating stems.
- Impact this closed was the silent half: Step 4's phantom-triple gate HARD STOPs loudly, but
  the extractor half kept question counts right (QV parity held, every gate passed) while
  truncating stems at the figure and orphaning every option after it — corruption that flowed
  into section_rules.md, the manifest, the Frequency xlsx, and on into Step 6 allocation and
  Step 7 generation. Measured on IIT_JAM_BIOTECHNOLOGY (22 papers / 1719 questions): 20
  spurious headings across 10 papers, 128 counted triples vs 126 real, 2 phantom triples.
- Specs: Framework_MockTestAnalyse v2.32 -> v2.33, Framework_PYQAnalyse v2.27 -> v2.28.
  Engine: blueprint_core.py (self-test 178/178) — heading predicate gains the `next_text`
  parameter. MANIFEST.json + SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0
  issues across 17 files.

## 2026.07.26
- GAP-2026-07-25-003 (taxonomy read consolidated to ONE reader + lock gate reaches every
  consumer): the last hand-written and prose readers of the approved taxonomy are removed.
  Every step now loads through `corpus_io.load_taxonomy()` and asserts identity through
  `corpus_io.assert_taxonomy_lock()` — one implementation, called everywhere, instead of the
  four-plus transcriptions that produced GAP-2026-07-25-002. The read and the lock assertion,
  previously two calls (and in some steps two independent reads of the same artefact), collapse
  to a single call at each site.
- Preferred source moves from the Analysis Word document to `approval_record.json`: where the
  record carries the taxonomy (reconcile_taxonomy >= v1.3) the consuming steps parse no Word
  document at all; pre-1.3 records fall back to the doc, fully gated, and need no re-run.
- Specs: Framework_Blueprint v1.39 -> v1.41 (S2-2 asserts the lock, then loads through
  load_taxonomy — Step 6 was the worst place for a silently-wrong taxonomy); Framework_MockTestAnalyse
  v2.30 -> v2.32 (both Step-5 readers gated then load through load_taxonomy; a second latent
  defect in `_extract_taxonomy_tuples_from_*` fixed while wiring the gate); Framework_PYQAnalyse
  v2.24 -> v2.27 (Task 2.5 was the last hand-parser — read/write through Cluster K, lock delegated
  to the shared gate, then load through load_taxonomy); Framework_PYQSort v1.14 -> v1.16 (taxonomy
  loaded once from JSON where available; S1-0b/S1-2 collapse to one call; ingest form surfaced,
  EC-S20/S21 recorded).
- Engines: reconcile_taxonomy.py (self-test 69/69) records the approved taxonomy inside
  approval_record.json beside its validating fingerprint; corpus_io.py -> v1.4 (self-test 226/226)
  owns `load_taxonomy()` + `assert_taxonomy_lock()` as the single reader/gate. MANIFEST.json +
  SPEC_MANIFEST.json regenerated; bootstrap 25/25, validator 0 issues across 17 files.

## 2026.07.25.2
- GAP-2026-07-25-002 (Analysis-doc reader delegation): MockTestAnalyse v2.29.1 -> v2.30
  delegates both Analysis-doc readers (score_difficulty / determine_strip_mode) to
  blueprint_core Cluster E — the byte-identical second copy is replaced by a thin adapter,
  so one definition is called from both places. Blueprint v1.38 -> v1.39 (S2-2 reader
  delegated), PYQAnalyse v2.23 -> v2.24 (S4-2 de-stubbed, taxonomy attested, name-length
  gate), PYQSort v1.13 -> v1.14 (reader delegated + S1-0b content cross-check).
- Engines: blueprint_core (164/164), corpus_io (138/138), reconcile_taxonomy (59/59),
  validate_framework_md.py — +batch checks AF (deliverable-filename contract) and AG
  (shared-artefact readers); Check Z widened to the engine's whole public surface.
- routes.json: engine routing broadened across the PYQ steps. CLAUDE.md: guardrails added —
  deliverable rename/cardinality is a cross-step contract change; a shared artefact has ONE
  reader; producer-enforced bounds. MANIFEST.json + SPEC_MANIFEST.json regenerated.

## 2026.07.25.1
- GAP-2026-07-25-001 (S4-0 silent check-skip): reconcile_taxonomy.py v1.0 -> v1.1 — the
  early `return` inside C4's style-aware branch that disabled C5/C6/C7 for every
  syllabus_style exam is removed; reconcile() is now SINGLE-EXIT. Adds CheckLedger
  (INV-7 completeness, INV-8 measured-domain), materialise() (INV-9 no-derivation,
  INV-10 resolvable-target), DEGRADED mode, C6 scale-relative, C4 normalized subject
  match; self-test 54/54. PYQAnalyse v2.22.1 -> v2.23 (S4-0 check-completeness
  architecture). PYQSort v1.12.2 -> v1.13 and DeliveryFooter v1.6 -> v1.7 wire the
  [ExamCode]_approval_record.json contract (produced at Step 2c, consumed at PYQSort entry).
  validate_framework_md.py +Check AC (aggregator single-exit) so the drift cannot return;
  routes.json routes reconcile_taxonomy.py to PYQApprove.
- CLAUDE.md release-manager protocol updated: corpus-level checks AA-AE are part of the
  gate; "a red check is never advisory"; corrected engine-load model (engines load from
  the repo clone, /mnt/project is data-only, no per-project provisioning). SPEC_MANIFEST.json
  33-file workbench baseline regenerated to match production.

## 2026.07.25
- NEW audit_sync.py — cross-step synchronisation auditor (engine-API, trigger/route/SKILL
  parity, version xrefs, filename chain, blueprint.json schema). Untracked dev tool.
- PYQAnalyse v2.16 -> v2.22.1 + 3 NEW engines: corpus_io.py (Drive acquisition / image
  integrity / size governor), reconcile_taxonomy.py (S4-0), syllabus_provenance.py (S2-3e);
  blueprint_core.py +Clusters F-J (pattern-era, taxonomy parse, acquisition, image-gate,
  size governor; self-test 57 -> 164). Tracked set 21 -> 24.
- Corpus-transport migration wave: NEW spec PYQCompress v1.0 (Layer-2 doc size remediation;
  new trigger, tracked set -> 25); Blueprint v1.35 -> v1.38, MockTestAnalyse v2.24.10 ->
  v2.29.1, MockTestExplainAudit -> v1.16.1, PYQPrepare -> v1.9.1, PYQSort -> v1.12.2,
  PYQExplain -> v1.1, PYQExplainAudit -> v1.1.1, PYQFormat -> v1.4.1, PYQDeliver -> v1.5.1
  (delegate engine-owned functions to blueprint_core/corpus_io; remove local copies).
  validate_framework_md.py +5 checks (V-DRIVEGUARD/W-ENUMSIZE/X-DURABILITY/Y-IMGGATE/
  Z-DELEGATION). NEW audit_deep.py (deep drift/delegation/table-parity auditor).
- PYQCompress v1.0 -> v1.1 + corpus_io v1.0.1 -> v1.0.3 (v1.0.2 media-stem-collision fix
  [silent figure loss]; v1.0.3 optimize_docx always= param). Shipped as an atomic pair.

## 2026.07.23.1
- blueprint_core.py +Cluster E — score_difficulty / determine_strip_mode /
  map_difficulty_level, the canonical shared difficulty scorer for Step 5 and PYQ-4.
  Self-test 33 -> 57 PASS; byte-identical to MockTestAnalyse E-9/E-10 (V-SYNC verified).
- NEW audit_specs_ext.py — supplementary corpus auditor (V-SYNC cross-file parity,
  W-DECISION decision-ID integrity, X-NUMBER list contiguity, Y-CONFIG field-contract,
  Z-VERSION full 3-part compare). Untracked dev tool; 0 issues across the corpus.
- Framework_PYQDeliver.md v1.0 -> v1.2.1: date/session tag removal (§4A), three-tier
  deterministic Complexity resolver via blueprint_core Cluster E (D11 supersedes D4),
  adversarial audit fixes (marks_default declared, JSON int-key normalization,
  difficulty_labels fallback). RELEASE-MANAGER FIX: converted blueprint_core.py sourcing
  from /mnt/project-only to dual-path (/tmp/fw first, else /mnt/project) so GitHub-connected
  projects no longer HARD STOP. routes.json: PYQDeliver now lists blueprint_core.py.
- Framework_MockTestAnalyse.md v2.24.9 -> v2.24.10: annotation-only (E-9/E-10 canonical
  copy moved to blueprint_core Cluster E; zero logic change).
- routes.json reformatted to the generator's pretty-printed emit style (no functional change).

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
