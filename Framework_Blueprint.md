# Framework_Blueprint v1.31 — Universal Mock Test Blueprint Generator
#
# v1.31 — 2026-07-15 — DOC: clarified that blueprint_version is the shared blueprint.json SCHEMA
#   version (Step-7 floor MIN_BLUEPRINT_VERSION=(1,7)), decoupled from the spec-FILE version, and
#   that the scoped blueprint must emit the SAME value. No code/behaviour change. Prompted by the
#   ScopedBlueprint v1.2 fix (it had emitted its spec version '1.0' as blueprint_version, which
#   would fail the (1,7) floor). Keeps mock + scoped schema versions in sync.
#
# v1.30 — 2026-07-15 — REGISTRY SCHEMA SYNC (docs/seed only; zero logic). The §12 registry seed +
#   schema now list semantic_usage=[] and exhausted_subtopics={} alongside the existing fields, to
#   MATCH the generation layer's schema (MockCreate v5.22 B). Purely additive: a registry seeded here
#   is byte-schema-identical to one Step 7 would self-heal. No allocation/behaviour change.
#
# v1.29 — 2026-07-15 — C1: UNIVERSAL paper_id IDENTITY (generation-layer foundation; additive,
#   zero behavioural change). (1) Each mocks[] entry now also carries paper_id="MOCK:M{mock:02d}"
#   (§14 S14-5) — Steps 7-11 still read 'mock'; the generalised (paper_id) path + the shared
#   registry key on paper_id. (2) The registry seed (B3 Step 5) + §12 S12-1 add papers_completed=[]
#   alongside mocks_completed=[] — the paper-identity ledger shared by mocks and every scoped tier;
#   legacy mocks_completed-only registries are auto-migrated by the scoped loader. schema_version
#   stays "1.0" (the schema bump belongs to the Step-7/registry generalisation, not this additive
#   step). Allocation math UNCHANGED (blueprint_core.py untouched); proven bit-identical by
#   blueprint_refactor_integration_test.py (2/2) + blueprint_c1_paperid_test.py.
#
# v1.28 — 2026-07-15 — SHARED ENGINE EXTRACTION (allocation core → blueprint_core.py).
#   The allocation MATH formerly inlined here is now provided by the universal engine
#   blueprint_core.py (single source of truth; the same engine backs the forthcoming
#   Subject/Topic/Sub-Topic scoped blueprints, so a fix lands once). Extracted, VERBATIM-
#   equivalent: recency split (§3-1 → bc.split_recency) + r_avg (§3-2 → bc.compute_r_avg);
#   proportional split (§4-2 STEP 3 → bc.proportional_split) + largest-remainder deficit
#   (§4-2 STEP 4 → bc.largest_remainder_fix), with STEP 3b mandated raw_total PRESERVED and
#   AllocationError re-wrapped into the spec's AlgorithmError; EXACT MATRIX FILL (§4-5b →
#   bc.exact_fill); difficulty counts (§7-4 → bc.difficulty_counts); three-axis schedule
#   (§7-7 → bc.derive_axis_schedule + bc.axis1_feasibility, internally
#   bc.largest_remainder_apportion + bc.section_axis2_pool_caps); slugify (§17 → bc.slugify).
#   NEW S1-2b ENGINE MANDATE: HARD STOP if blueprint_core.py absent → copy to /home/claude
#   → run --self-test (must print "SELF-TEST: N/N PASS") → import blueprint_core as bc.
#   ENGINE PARAM RENAME: mocks_per_window → papers_per_window (a mock is a paper); the
#   RETURNED axis_schedule dict STILL carries the 'mocks_per_window' KEY that Steps 7/8 read
#   (output contract unchanged), so only the §7-7 build-loop call keyword changed.
#   BEHAVIOUR IS UNCHANGED — proven three ways: (a) blueprint_core_test.py 19/19 +
#   qa_pass2_differential.py (bc.* == verbatim source over ~128k inputs); (b)
#   blueprint_refactor_integration_test.py (refactored wiring == pre-refactor inline over
#   50k fixtures, incl. mandates / floors / infeasible classification); (c)
#   validate_framework_md.py 0 issues, 37/37 AST clean. ONE diagnostic-only change: the
#   r_avg data-quality warning now omits the specific year (the subtopic is still named);
#   the r_avg VALUE is byte-identical. No blueprint.json schema change.
#
# v1.27 — 2026-07-08 — CANONICAL AUDITOR (§13-7A): B3 now generates the ONE canonical
#   v2.6 auditor VERBATIM from Framework_MockTestCreateAudit.md Appendix A (full A-* gates,
#   --audit-state COMPLETION GATE S5-1A, fixture-based self-test), NOT the retired 13-gate
#   constant-print MVP. Self-test validation is now FIXTURE-BASED with N >= AUTH_GATE_FLOOR
#   (35); a constant-print "N/N PASS" is REJECTED. Retires the "minimum viable vs full 66"
#   split and the upgrade path. Root cause / rationale: Framework_MockTestCreateAudit.md v2.6.
#
# v1.24 changes: BV-10 SAME-MECHANIC DEADLOCK — PERMANENT STRUCTURAL FIX.
#   (1) NEW §4-1b BV-10 MECHANIC FEASIBILITY GATE at B1 (analogue of EC-11): an
#       exhaustive G1→fast→G3(Hall's b-matching) decision procedure that PROVES the
#       same-form constraint satisfiable BEFORE generation, per collision_domain and
#       every batch window (incl. short final window), consuming rare/ZP/mandate pins.
#       If infeasible → HALT with offending members + named upstream fix (NO regen loop).
#   (2) BV-10 (§9-6b) rebuilt as TWO TIERS: BV-10a HARD on form_key (fine identity,
#       domain-scoped — fires only on TRUE duplicates); BV-10b SOFT cap on family
#       (coarse), a Step-8 tolerance target that never blocks. Consumes Step 5 v2.24
#       fields (form_key, concept_group=family, collision_domain).
#   (3) max_per_mechanic_per_mock config (default 1) for legitimate repetition (DI-heavy).
#   (4) §9-10 failure protocol now branches STOCHASTIC (regenerate) vs STRUCTURAL
#       (HALT-with-fix); the "3 attempts → ask user" dead-end is gone.
#   Guarantee: if §4-1b passes, a collision-free schedule provably exists; if not, B1
#   halts with the exact fix — so BV-10 can never deadlock at B2/B3 again. Verified by
#   step6_harness (11/11) + engine extracted-from-this-file + whole-doc syntax parity.
#   PAIRS WITH Step 5 v2.24 (Framework_MockTestAnalyse), which emits the form_key axis.
#
# v1.25 changes: EXACT MATRIX FILL allocator (§4-5b) — fixes BV-7 F1 allocation drift
#   (register D3-14 / §12; drifted 30/59 subtopics in the SSC CGL run). Replaces Phase-0
#   backward-forcing + naive column-fix (which did not preserve per-subtopic quota) with a
#   base + Gale-Ryser remainder fill: row sums == quota EXACTLY (0% F1 drift), column sums
#   == free capacity EXACTLY (BV-1), per-cell floor/ceil (F5 variance ≤ 1), coverage (BV-9B),
#   and deterministic (no re-drift across batches, D3-6). §4-6 column-fix becomes a no-op
#   invariant check. Verified by alloc_harness (15/15 incl. 100 random instances).
#
# v1.26 changes: COVERAGE GATE PER-PAPER NORMALIZATION (register D6-7). The coverage
#   validation gate summed multi-year "Combined Qs" against a single-paper total, so it
#   reported ~300% on a 3-year Excel and could never detect under-coverage (the MPPSC
#   Botany 62% failure mode). Now sums the per-paper Avg/Paper column (fallback: Combined
#   Qs / total_papers) → per-paper-vs-per-paper. Verified by cov_harness (7/7): correctly
#   passes full coverage, HALTs on 62% under-coverage, unchanged for single-paper Excels.
# [ExamCode] project | Step 6 (MockBlueprint) | Exam-agnostic
#
# PURPOSE:
#   Generate a complete subtopic-allocation blueprint for any MCQ competitive exam.
#   This spec is exam-agnostic — it works for SSC, IBPS, GATE, UPSC, NEET, and any
#   MCQ exam series. Exam-specific parameters (sections, subtopics, frequencies) are
#   read from input documents at runtime — nothing is hardcoded here.
#
# PIPELINE POSITION:
#   Step 5:  PYQExtract      ← must publish subtopic_manifest.json before Step 6 B1 finalises
#   Step 6:  MockBlueprint   ← THIS SPEC (consumes Step 5's subtopic_manifest.json)
#   Step 7:  MockCreate
#   Step 8:  MockCreateAudit
#   Step 9:  MockExplain
#   Step 10: MockExplainAudit
#   Step 11: MockDeliver
#
#   ALL steps run in the [ExamCode] project (exam-specific).
#   Steps 5 and 6 run IN PARALLEL — both must complete before Step 7.
#   Step 5 and Step 6 do NOT depend on each other — run in any order.
#
# ═══════════════════════════════════════════════════════════════════════════
# STEP NUMBER NOTE — CANONICAL PIPELINE MAPPING
# This file is Step 6 (MockBlueprint) in the canonical 11-step pipeline.
# The changelogs and body text below use an internal "Step 0/1/2…" shorthand
# for brevity within the Phase 2 (Mock Test Generation) sub-pipeline:
#   internal "Step 0" = canonical Step 5  (PYQExtract)
#   internal "Step 1" = canonical Step 6  (MockBlueprint, THIS file)
#   internal "Step 2" = canonical Step 7  (MockCreate)
#   internal "Step 3" = canonical Step 8  (MockCreateAudit)
#   internal "Step 4" = canonical Step 9  (MockExplain)
#   internal "Step 5" = canonical Step 10 (MockExplainAudit)
#   internal "Step 6" = canonical Step 11 (MockDeliver)
# When an explicit label is given (e.g. "Step 8 (MockCreateAudit)"), the
# canonical number is always used. Unlabelled "Step 2" in body text means
# MockCreate (= canonical Step 7) per the mapping above.
# ═══════════════════════════════════════════════════════════════════════════
#
# SOURCES OF TRUTH (load at session start — in priority order):
#   1. This spec (Framework_Blueprint.md)           — rules + procedures
#   2. exam_config.json (from Step 2a)              — section structure, marking_scheme,
#                                                      level, medium, max_attempt (PRIMARY)
#   3. Exam Pattern document (FALLBACK)             — section structure (when exam_config absent)
#   4. Analysis Word Document(s)                    — subtopic taxonomy + Q counts
#   5. Frequency Excel                              — year-wise data + Format column
#   6. blueprint.json (prior batches only)          — cumulative allocation state
#   7. [ExamCode]_subtopic_manifest.json (from Step 5) — REQUIRED v1.7. The
#      authoritative subtopic_id↔name registry + mandate data. Step 1 reads it to
#      assign ids and enforce mandates. Without it → HARD STOP (gate S2-MANIFEST).
#
# TRIGGER FORMAT:
#   Step 6: MockBlueprint [N_mocks]
#   Step 6: MockBlueprint [N_mocks] --difficulty E:M:H
#   Step 6: MockBlueprint [N_mocks] --difficulty progressive
#
#   Trigger matching is case-insensitive.
#   ExamCode read from exam_config.json in project knowledge (set during Step 2a PYQDraft).
#   [N_mocks]   : positive integer > 0 (flag if > 100)
#   --difficulty: optional; default = 25:25:50 (Easy:Medium:Hard) applied silently.
#                 E:M:H must sum to 100. If not → ERROR.
#
#   Examples:
#     MockBlueprint 50
#     MockBlueprint 30 --difficulty 25:50:25
#     MockBlueprint 20 --difficulty progressive
#
# OUTPUT FILES (all with [ExamCode] prefix):
#   [ExamCode]_blueprint.xlsx           — human review (5 sheets)
#   [ExamCode]_blueprint.json           — authoritative allocation data
#   [ExamCode]_registry.json            — empty registry template
#   [ExamCode]_ExplainLearnings.md      — empty template for Step 9 (MockExplain)
#   [ExamCode]_ExplainAuditLearnings.md — empty template for Step 10 (MockExplainAudit)
#   [ExamCode]_mock_test_audit.py       — canonical v2.6 audit script (Step 7 optional, Step 8 mandatory)
#
# PROJECT SETUP:
#   ALL steps run in: [ExamCode] project (exam-specific, created by user)
#   After B3: user uploads blueprint.json + registry.json + learnings templates
#             + mock_test_audit.py + section_rules.md (from Step 0) to [ExamCode] project.
#             Never upload blueprint.xlsx (not readable by Claude).
#
# NOTE: Step 7 (MockCreate) requires outputs from BOTH Step 0 and Step 1:
#   From Step 0: [ExamCode]_section_rules.md  — per-subtopic PYQ pattern reference
#   From Step 1: [ExamCode]_blueprint.json    — mock allocation plan
#                [ExamCode]_registry.json     — dedup tracking template
#                [ExamCode]_ExplainLearnings.md
#                [ExamCode]_ExplainAuditLearnings.md
#                [ExamCode]_mock_test_audit.py — audit script (Step 7 optional, Step 8 mandatory)
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains zero hardcoded exam values.
#   All section names, Q counts, subtopic names, frequencies → read from input documents.
#   Same spec runs for 10-mock series or 100-mock series.
#   Same spec runs for 1-section exam or 6-section exam.
#
# VERSION HISTORY:
#   v1.23 — 2026-07-07 — THREE-AXIS FORMAT-DISTRIBUTION ENFORCEMENT (File 2 of the feature;
#           reads the targets Step 5 v2.23 emits; Steps 7/8 are Files 3–4).
#           A mock must replicate the exam's FORMAT MIX, not just its syllabus. Blueprint's
#           role: READ the per-section axis targets + per-subtopic capability, CARRY them into
#           blueprint.json for Steps 7/8, and enforce what allocation can enforce.
#           FIX A — S2-MANIFEST reads manifest['axis_distribution'] (per-section 3-year targets)
#             + per-subtopic axis2_capability / observed_axis2 / presentation_family. Absent-safe.
#           FIX B — §6 GOLDEN-RULE RECONCILIATION: format still NEVER excludes (r_avg=0 remains
#             the SOLE exclusion); it now ADDITIONALLY influences SCHEDULING so axis targets are met.
#           FIX C — S7-7 derive_axis_schedule(): the per-section axis "schedule" (parallel of
#             difficulty_schedule). Carries axis1/2/3 per-paper averages + audit modes; derives
#             band-mode Axis-2 window targets + guarantee list; classifies each guarantee format's
#             feasibility ('pyq_covered' — Option-C batch coverage already guarantees it, no swap
#             needed; 'zp_only' — best-effort via ZP rotation; 'unsatisfiable' — accept shortfall
#             per decision (i), fabrication BANNED). Stored as blueprint['axis_schedule'].
#           FIX D — AXIS-1/3 (locked): carry target + feasibility report + soft-steer tie-break;
#             NOT a hard per-mock re-solve (Subtopic stays hard #1). Audited within tolerance at Step 8.
#           FIX E — §9 BV-AXIS gate (B3): axis_schedule well-formed + guarantee/axis feasibility report.
#           FIX F — §14 blueprint.json gains axis_schedule (S14-3b); axis targets are carried
#             in blueprint.json (human-readable, authoritative for Steps 7/8) and surfaced in the
#             B1/B3 delivery notes. The §15 xlsx LOCKED 5-sheet contract is intentionally PRESERVED
#             (no 6th sheet — the axis targets are not an xlsx concern). blueprint_version → 1.23.
#   v1.0 — Initial release. Core allocation algorithm across 17 categories.
#           Validated against SSC CGL Tier 1 (221 subtopics, 204 papers, 50 mocks).
#   v1.1 — Added Step 5 (PYQExtract) pipeline coordination: parallel execution
#           note, section_rules.md handoff, subtopic name consistency rule, DoD item 15.
#   v1.2 — Memory prohibition + GOLDEN RULE (Format is classification only, never
#           exclusion). BV-0A subtopic completeness check. EC-10 memory conflict edge
#           case. Format inclusion rules in §10 S10-7, S10-11, EC-5.
#   v1.3 — Option C batch coverage guarantee: every PYQ subtopic ≥ 1 Q per 10-mock
#           batch window. Three-phase algorithm (Phase 0 + Phase 1 + Phase 2).
#           Quota minimum raised to n_batches. BV-9B batch coverage check per B2
#           batch. EC-11 feasibility edge case. INVARIANT 8. §8-3 Phase 0 wired in.
#   v1.4 — BATCH GATE enforcement (ISSUE 1,3): §8-2 Step 9 and §8-3 Step 8 now
#           carry explicit BATCH GATE blocks with hard STOP language — Claude MUST
#           NOT continue past B1 or any B2 batch in the same response. Passive
#           "wait for user affirmative" language was insufficient; now mirrors HALT
#           strength. B1 present_files fix (ISSUE 2,5): §8-2 Step 9 and §11-1
#           PART B now unambiguously list BOTH blueprint.xlsx AND blueprint.json v1
#           as mandatory B1 deliverables — no file may be omitted. §8-3 Step 7
#           also hardened with explicit two-file checklist. §11-2 PART B clarified.
#           blueprint_version field updated to "1.4".
#           Second-pass fixes: §8-1 overview corrected (B1 delivers 2 files, not 1).
#           §8-5 Step 8 stale "ref §11 BD-7" corrected to "ref §11 S11-3".
#           §8-5 Step 8 now has 8-item pre-delivery checklist before present_files.
#           §8-5 Step 9 stale "ref §11 BD-7" corrected to "ref §11 S11-3".
#           §11-3 PART B now has 6-item pre-delivery checklist (matches B1/B2 pattern).
#           §11-3 PART B file list now uses exact [ExamCode]-prefixed names.
#           Definition of Done: new item ☐ 0 added — BATCH GATE discipline check.
#           Third-pass deep analysis fixes (7 additional bugs):
#           All remaining stale BD-1/BD-2 references replaced with S11-1/S11-2
#           in S6-5, S8-2 Step 9, S8-3 Step 7, S9-0A (4 occurrences).
#           §11-1 BV-0A "Zero silently excluded" clarified to "Silently excluded: 0"
#           to eliminate ambiguity with "Zero-PYQ" terminology.
#           §13-8 Step C "5 files — NOT the xlsx" clarified: 4 Step-1 files +
#           1 Step-0 file (section_rules.md) = 5 total; each file now labelled
#           with its source step.
#           §8-2 Step 6 progressive bands timing fixed: now consistent with
#           §7 S7-3 which states bands are collected during S1-6, not mid-B1.
#           Fourth-pass deep analysis fixes (4 real bugs):
#           §8-5 Step 6: ExplainLearnings.md header now matches §13-5 exactly
#           (added missing "— [exam_name]" segment).
#           §8-5 Step 7: ExplainAuditLearnings.md header now matches §13-6 exactly.
#           S6-3: stale "ref §14 JS-7" corrected to "ref §14 S14-7".
#           S3-6 + §15 S15-3: Col E ambiguity resolved — both now specify the
#           combined label format "PYQ-based (High/Medium/Low)" / "Zero-PYQ"
#           so importance class and PYQ type are stored together in one column.
#   v1.5 — §15 XLSX SPECIFICATION LOCKED (ISSUE: wrong sheet names and wrong Sheet
#           content delivered in prior run). Root cause: §15 was detailed but lacked
#           a mandatory pre-generation checklist enforcing the exact sheet names and
#           column structure before present_files is called.
#           Fixes applied:
#           (1) §15 completely rewritten as LOCKED SPEC with exact sheet names,
#               exact column headers, exact column order, and explicit examples
#               drawn from the verified reference output. These are PERMANENT RULES
#               — Claude MUST match them exactly. Deviating = critical error.
#           (2) §15-CHECKLIST added: a mandatory 5-point self-verification that
#               Claude runs against its own generated xlsx BEFORE calling
#               present_files. If any item fails: fix xlsx before delivering.
#           (3) §8-2 Step 8 updated to reference the §15-CHECKLIST explicitly.
#           (4) Sheet 2 (Blueprint) column header is "r_avg" (not "Recency Avg/Paper").
#           (5) Sheet 3 (Summary Stats) columns match reference exactly:
#               Subject|Topic|Sub-Topic|Format|Type|r_avg (Recency)|Pooled Avg|
#               Total PYQs|Quota (Target Qs)|Actual Qs|Accuracy%|Mocks Appeared
#               (12 columns, not 15 — S15-3 previously overcounted).
#           (6) Sheet 4 (Difficulty Schedule) uses percentage NUMBERS (15/30/55),
#               Total=100, not Q-counts. Band label: "Standard".
#           (7) Sheet 5 (Phase 0 Verification) simplified to match reference:
#               Subject|Topic|Sub-Topic|Format|r_avg (Recency)|Type — sorted by
#               r_avg desc, ZP at bottom. Full year-column expansion is optional
#               and only required when paper-count data is available.
#           blueprint_version field updated to "1.5".
#   v1.6 — Full line-by-line audit (fifth pass). Three bugs found and fixed:
#           Bug 1: §8-3 Step 5 comment had stale "§14 JS-6" reference — corrected
#           to "§14 S14-6" (consistent with all other S14-x references in spec).
#           Bug 2: §15-3 Sheet 3 Type column listed "zero_pyq" (snake_case) but
#           §3-6 defines "Zero-PYQ" (human-readable with capital Z and hyphen) for
#           Summary Stats. Now aligned: §15-3 Type col shows all four labels exactly
#           as §3-6 defines them: "PYQ-based (High)", "PYQ-based (Medium)",
#           "PYQ-based (Low)", "Zero-PYQ". Phase 0 sheet retains "pyq_based" /
#           "zero_pyq" (machine-readable) — these are DIFFERENT sheets with
#           intentionally different label styles; now explicitly documented.
#           Bug 3: EC-9 (5+ sections edge case) listed old hex color codes
#           (#D6E4F7, #E2F0D9, #FFF2CC, #FCE4D6, #EAD1DC, #D0E4CC) that
#           conflicted with §15-0 locked colors (#DEEAF1, #E2EFDA, #FCE4D6,
#           #EAE3F7). EC-9 now references §15-0 exactly. Single source of truth
#           for all color codes is §15-0.
#           blueprint_version field updated to "1.6".

#   v1.20 — 2026-07-06 — AUDIT SCRIPT AUTO-GENERATION (6th output file).
#           Root cause: [ExamCode]_mock_test_audit.py was a manual creation step
#           between Step 6 and Step 7/8. Users could forget → HARD STOP at Step 8.
#           Step 6 already has all data needed (blueprint.json structure, sections,
#           Q counts, format flags) to generate the minimum viable audit script.
#
#           CHANGE 1 — S13-NEW (S13-7A): new section defining mock_test_audit.py as
#             Step 6 output. Includes: purpose, content (minimum viable 13-gate script
#             from Appendix A template), upload rule, lifecycle, collision handling,
#             upgrade path to full 66-gate version.
#
#           CHANGE 2 — S8-5 Step 8A (new): B3 generates the audit script from the
#             AUDIT_SCRIPT_TEMPLATE embedded in this spec. Runs --self-test validation
#             before delivery. HALT if self-test fails.
#
#           CHANGE 3 — §13 section header, S13-1, S13-7, S13-8, S13-9 updated:
#             "5 files" → "6 files" throughout. mock_test_audit.py added to naming
#             convention, delivery order, upload instructions, and re-run procedure.
#
#           CHANGE 4 — S11-3 PART B/C (handoff): 6th file in present_files and upload
#             list. Handoff message updated.
#
#           CHANGE 5 — DoD item ☐ 25 added: audit script generated, self-test passed.
#
#           CHANGE 6 — AUDIT_SCRIPT_TEMPLATE (§13-7A): canonical reference section
#             added to this spec. Generation rules, collision handling, and lifecycle
#             defined here. Template code currently in Step 7 Appendix A (transitional);
#             will move here when Step 7 is updated next. Step 7 Appendix A then becomes
#             a pointer to this section.
#
#           EDGE CASES COVERED (20 total — see conversation record):
#             EC-A1 single source of truth (rules in Step 6 §13-7A; code transitionally
#                   in Step 7 Appendix A until Step 7 update moves it here)
#             EC-B1 minimum viable vs full (Step 6 generates MVP; user upgrades later)
#             EC-B3 self-test without python-docx (--self-test never imports docx)
#             EC-B4 MSQ/NAT gate dormancy (script reads flags from blueprint at runtime)
#             EC-C5 B3 self-test validation (HALT if fail)
#             EC-D1 collision with user's custom script (ask before overwriting)
#             EC-D3 re-run overwrites upgraded script (warn about downgrade)
#           blueprint_version field updated to "1.20".
#
#   v1.22 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S13-10: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. All three batch types (B1, B2, B3)
#           now render the standardized visual footer after every present_files call.
#           B1/B2 use F1 (amber mid-step), B3 uses F2 (green step-complete).
#           Zero logic change.
#   v1.21 — 2026-07-07 — ZERO-PYQ MANIFEST COMPLETENESS GATE (Fix B from BUGFIX report).
#           Root cause: Step 6 had a code path in §5 (ZP rotation setup) and §10
#           (missing-data fallbacks) that discovered subtopics from the taxonomy/syllabus
#           and added them to the blueprint WITHOUT routing through resolve_subtopic_id().
#           These subtopics got auto-generated sequential IDs (ST0097, ST0098, ...) that
#           existed in neither the manifest nor section_rules.md. Step 7 correctly HARD
#           STOPPED at S3-8 because these self-minted IDs were unjoinable.
#           Discovered: SSC CGL Tier 2, Mock 1 — 3 of 7 orphan IDs triggered the block.
#
#           FIX B.1 — RULE 2a (NO BYPASS): new invariant added to CROSS-STEP CONTRACT
#             (§2 edge cases). EVERY subtopic that enters the blueprint — whether from the
#             Analysis doc, the taxonomy, the syllabus, or any fallback/supplement path —
#             MUST resolve to a manifest id via resolve_subtopic_id(). There is NO code
#             path that creates a subtopic entry without a manifest-resolved id. Specifically
#             banned: auto-generated sequential IDs, max_id+1 patterns, any id not returned
#             by resolve_subtopic_id().
#
#           FIX B.2 — S2-MANIFEST-COMPLETENESS: new pre-flight gate added to §17 after
#             S2-MANIFEST. Before B1 begins, verifies that the manifest covers the exam's
#             taxonomy by attempting to resolve every taxonomy subtopic. If any taxonomy
#             subtopic has no manifest id → HARD STOP naming the missing subtopics and
#             directing the user to re-run Step 5 (v2.20+ runs taxonomy sync). Step 6
#             NEVER self-mints — it HARD STOPS and directs upstream.
#
#           CHANGE 3 — DoD items ☐ 26 and ☐ 27 added for the new gates.
#           blueprint_version field updated to "1.21".
#
#   v1.19 — 2026-07-06 — EXAM_CONFIG V2.5 CONTRACT SYNC (Step 2a marking_scheme integration).
#           Root cause: Step 2a v2.5 replaced scalar marks_per_question/negative_marking
#           with per-range marking_scheme[] and added level, medium, max_attempt to
#           exam_config.json. Step 6 must read these and carry them in blueprint.json
#           so downstream Steps 7-11 consume them.
#
#           CHANGE 1 — S2-1 REWRITE: PRIMARY SOURCE IS NOW exam_config.json:
#             Exam Pattern document is NO LONGER the primary source for section structure.
#             exam_config.json (written by Step 2a from the standardized xlsx) is the
#             authoritative source. Legacy path (read Exam Pattern doc directly) preserved
#             as fallback when exam_config.json is absent.
#             New fields read from exam_config: marking_scheme[], level, medium, max_attempt.
#
#           CHANGE 2 — BLUEPRINT.JSON TOP-LEVEL FIELDS ADDED:
#             marking_scheme  : list — per-range scoring rules (from exam_config).
#             level           : str  — academic level (from exam_config).
#             medium          : str  — exam language (from exam_config).
#             These are carried through for Steps 7/8/9/11. Steps 7/9 use marking_scheme
#             for per-Q-position marks lookup and level for complexity calibration.
#
#           CHANGE 3 — SECTIONS[] SCHEMA: max_attempt ADDED:
#             Each section entry in sections[] now includes max_attempt (int).
#             When max_attempt == total_qs: no attempt limit (all Qs attempted).
#             The framework generates ALL total_qs questions per section regardless.
#             max_attempt is OTS platform metadata only.
#
#           CHANGE 4 — SECTION ≠ SUBJECT NOTE IN S2-1:
#             Section names from exam_config are OTS display labels, not taxonomy Subjects.
#             Consistent with Step 2a v2.5 S2-2a architectural note.
#
#           CHANGE 5 — S14-1, S14-2 SCHEMA DOCS UPDATED for new fields.
#           blueprint_version field updated to "1.19".
#
#   v1.18 — 2026-07-05 — FREQUENCY EXCEL COVERAGE VALIDATION GATE (2 additions).
#           Root cause: MPPSC Botany framework-generated Frequency xlsx had only 93/150
#           questions mapped (38% data loss). Step 6 consumed this xlsx without any warning,
#           producing a blueprint with catastrophically distorted weightages (e.g., Diversity
#           of Life Forms: 5 Qs instead of 34). Two defensive checks added:
#
#           (1) S2-3 COVERAGE VALIDATION GATE (new): After reading the Frequency Excel,
#               compute sum(all Combined Qs across all sections) and compare against
#               exam_config.total_questions (or Exam Pattern total). If mismatch > 5%:
#               HALT with message identifying the gap. Prevents consuming incomplete
#               frequency data that would produce inaccurate blueprints.
#
#           (2) S10-3 SOURCE PRIORITY UPDATE: Added note that if Frequency Excel % of
#               Subject values imply a denominator different from exam total questions,
#               this signals a data quality issue in Step 5 output — flag before proceeding.
#
#           blueprint_version field updated to "1.18".
#
#   v1.17 — 2026-07-04 — CROSS-STEP CONTRACT SYNC AUDIT (5 fixes).
#           Deep cross-file analysis against Framework_MockTestCreate (v5.4),
#           Framework_MockTestCreateAudit (v1.3), Framework_MockTestExplain (v1.6),
#           Framework_MockTestExplainAudit (v1.3), Framework_MockDeliver (final),
#           and Framework_MockTestAnalyse (v2.16). All fixes are additive — no
#           allocation behaviour change; zero existing field semantics altered.
#           (1) REGISTRY SCHEMA GAP (§12-1, §12-3, §8-5 Step 5, RS-9): MockCreate's
#               REQUIRED_TOP expects 4 fields that Blueprint's §12 template did NOT
#               seed: image_phashes, image_sources_used, session_log, content_tracking.
#               MockCreate self-healed them on first mock — technically violating RS-9
#               ("Step 2 never adds new top-level fields"). FIXED: all 4 fields now
#               seeded in the §12-1 template (image_phashes=[], image_sources_used=[],
#               session_log=[], content_tracking={}). §12-3 examples updated. §8-5
#               Step 5 generation list updated. RS-9 rewritten to enumerate all seeded
#               top-level fields and explicitly permit content_tracking subfield
#               creation via setdefault() (not a top-level addition).
#           (2) option_label FIELD DEFINITION INACCURACY (§14-1, §8-2 Step 7): both
#               claimed "Step 7 reads via bp.get('option_label')" but MockCreate R10
#               reads option_label_format from section_rules.md, not from blueprint.
#               FIXED: field definition now says "Carried for visibility/parity; Step 7
#               reads the AUTHORITATIVE value from section_rules.md R10."
#           (3) STEP NUMBER MAPPING NOTE (header): added a clear 17-line mapping block
#               (matching Framework_MockTestAnalyse v2.16 pattern) documenting the
#               internal "Step 0/1/2…" → canonical "Step 5/6/7…" convention used
#               throughout this file. Header lines 20-21 updated from "Steps 0 and 1"
#               to "Steps 5 and 6" for canonical consistency.
#           (4) §12-3 Example 3: hardcoded "IBPS_PO_DI" exam_code replaced with
#               generic "[ExamCode]" placeholder (exam-agnostic guarantee).
#           (5) S12-5 CROSS-REFERENCE AUDIT: verified question_index, subtopic_id,
#               difficulty_labels, answer_type, answer_cardinality, total_options,
#               msq_contract, nat_contract field names are byte-identical between
#               Blueprint schema (§14) and MockCreate reads (S3-*, bp.get calls).
#               All verified consistent — no additional fixes needed.
#           blueprint_version field updated to "1.17".
#
#   v1.16 — 2026-07-04 — EXAM-AGNOSTIC RIGIDITY AUDIT (7 fixes).
#           Enforces the "zero hardcoded exam values" guarantee by removing all
#           SSC-specific content from active spec text and making fixed thresholds
#           configurable via blueprint.json with backward-compatible defaults.
#           (A) BV-9B print template (§9-11): hardcoded "GIR=[n] | GA=[n] | QA=[n] |
#               ENG=[n]" replaced with dynamic "[SecAbbr]=[n]" per actual sections[].
#           (B) BV reporting examples (§9-9): "× 4 sections", "GIR=62 GA=39 QA=42
#               ENG=54", "English: sum=24", "Cloze Test", "GIR: 3 subtopics",
#               "Calendar Day Calculation" all generalized to placeholders with
#               "illustrative" label.
#           (C) Rare threshold (§4-3): hardcoded 0.1 → configurable RARE_THRESHOLD =
#               bp.get('rare_threshold', 0.1). All 5 downstream references updated.
#               Exams with very few papers can lower it; exams with 500+ can raise it.
#           (D) Max rare per mock (§4-8 INVARIANT 4, §4-4, §9-4 BV-4): hardcoded 2 →
#               configurable MAX_RARE_PER_MOCK = bp.get('max_rare_per_mock', 2). All
#               code, validation, and delivery format references updated.
#           (E) Incomplete-doc threshold (§10-9): clarified as advisory heuristic that
#               never blocks B1 and applies across all exams equally.
#           (F) BV-10 rationale (§9-6b): SSC_CGL_TIER1_Mock01 Q77/Q78/Q79/Q80 example
#               generalized to "Q[x]+Q[y] = two find-opposite Qs" pattern. Error message
#               "synonym×2 or antonym×2" → "same-mechanic × 2".
#           (G) §14-6 and §14-7 JSON examples: "General Intelligence & Reasoning",
#               "gir.analogy.mixed_number_letter_analogy", "Analogy" → placeholder
#               format "[Section 1 Name]", "[section].[topic].[subtopic_slug]".
#           (H) EC-11 note: "SSC CGL Tier 1 (the primary exam)" → generic "typical
#               MCQ exams (25 Qs/section, ~60 subtopics/section)".
#           blueprint_version field updated to "1.16".
#
#   v1.15 — 2026-07-04 — DEEP-AUDIT (20 fixes across 7 categories).
#           CATEGORY A — Stale canonical step numbers (12 fixes):
#             Lines 53-54 (header OUTPUT FILES): "Step 4"/"Step 5" corrected to
#             "Step 9 (MockExplain)"/"Step 10 (MockExplainAudit)".
#             L2275: "Step 3 (MockCreateAudit)" → "Step 8 (MockCreateAudit)".
#             L3757: "Step 3 (MockCreateAudit)" → "Step 8 (MockCreateAudit)".
#             §13-5 (4 occurrences): all "Step 4" refs → "Step 9" (heading, body,
#             purpose, lifecycle).
#             §13-6 (4 occurrences): all "Step 5" refs → "Step 10" (heading, body,
#             purpose, lifecycle).
#           CATEGORY B — Deprecated "urgency loop" refs (5 fixes, stale since v1.13):
#             §4 Phase 2 description: "urgency" → "even-spread".
#             §8-3 Step 4d: "urgency loop: urgency-fill" → "even-spread: distribute"
#             (even-spread is the ONLY sanctioned method since v1.13).
#             §8-3 Step 4d: "counts for urgency" → "counts for remaining quota".
#             §8-3 BATCH GATE B2 reason text: "urgency scores" (×2) → "cumulative
#             counts" — the urgency loop is deprecated, these were stale artefacts.
#             §8-4: "compute urgency" → "compute remaining quota".
#             §8-3 Step 3 CRITICAL comment, §8-7, §9-10: "urgency scores" →
#             "assigned[] counts" (3 additional stale urgency references).
#           CATEGORY C — XLSX-4 checklist Total column value (1 fix):
#             "Total column = total_questions" → "Total column (F) = 100 (sum of
#             percentage values)" — Sheet 4 stores percentage numbers (15/30/55 summing
#             to 100), NOT Q counts. The prior text contradicted §15-4 which explicitly
#             states Col F = SUM(C:E) must equal 100.
#           CATEGORY D — Missing mandate enforcement step in §8-3 (1 fix):
#             §8-3 Step 4 previously listed: Phase 0 → Phase 1 → Phase 2 → column-fix,
#             with NO mandate enforcement step. Mandate rules M1/M2/M4/M6 must run
#             BETWEEN Phase 2 and column-fix (M2 rule (d) explicitly requires re-running
#             column-fix after resolution). Added Step 4e (mandate enforcement) and
#             renumbered column-fix to 4f, update-assigned to 4g.
#             S4-MANDATE stale cross-ref "§8-3 Step 5" corrected to "§8-3 Step 4e,
#             between Phase 2 and column-fix" (Step 5 is build_section_obj output, not
#             enforcement).
#           CATEGORY E — BV-0A location description (1 fix):
#             §9 header: "runs at the END of B1" → "runs DURING B1 (Step 4A)" — BV-0A
#             executes at Step 4A of B1 (midway), not at the end; "END" was misleading.
#           CATEGORY F — §14-1 schema gap (1 fix):
#             S14-1 JSON example and field definitions were missing total_options and
#             option_label. Both fields were documented in §8-2 Step 7 (B1 writing) and
#             consumed by Step 7 (MockCreate), but absent from the formal schema section.
#             Added to JSON example + full field definitions with cross-step SYNC notes.
#           CATEGORY G — Missing section header (1 fix):
#             BV-7 content at §9 had no ### S9-7 header — content started in a bare
#             code block between S9-6b and S9-8. Added "### S9-7 — BV-7: Full
#             cross-batch validation (runs in B3 only)".
#           blueprint_version field updated to "1.15".
#
#   v1.14 — 2026-07-03 — DEEP-AUDIT (1 fix). Header comment (line 41) stated the default
#           difficulty split as 20:30:50 (Easy:Medium:Hard), but the actual trigger parsing
#           (S1-1), the difficulty table (§7 S7-5 line 2144), the xlsx rendering (§15), and
#           every worked example all use 25:25:50. The header was stale — never updated when
#           the default changed. FIXED: header now 25:25:50. blueprint_version → "1.14".
#           No allocation behaviour change.
#
#   v1.13 — 2026-07-03 — ALLOCATION ALGORITHM & MANDATE INTERACTION FIX (7 issues).
#           Root cause: quota computation, Phase 0 forcing, even-spread collisions, and
#           mandate enforcement rules had structural gaps that caused 96+ F1 validation
#           failures in SSC CGL Tier 1. All fixes are exam-agnostic; no hardcoded values.
#           (1) §4-2 MANDATE-FIRST QUOTA RESERVATION: before the proportional r_avg split,
#               all M1/M4/M6 deterministic mandate totals are reserved from target_total.
#               Proportional split runs on remaining subtopics with remaining budget only.
#               This eliminates the quota-vs-mandate fight that was the root cause of 96 F1s.
#           (2) §4-5 PHASE 0 MULTI-MOCK SPREAD: forced batch-coverage assignments are now
#               spread backwards across all mocks in the window (b_end → b_start), using
#               per-mock remaining capacity, instead of dumping all uncovered subtopics
#               into mock b_end. Prevents overflow when uncovered_count > sec_qs.
#               Worked example added showing why single-mock forcing fails for GIR (56 vs 25).
#           (3) §4-5 PHASE 2 URGENCY LOOP DEPRECATED: the urgency loop is no longer a
#               sanctioned alternative. Pre-scheduled even spread is the ONLY method.
#               Urgency loop empirically failed variance ≤ 1 (GA section broke with zero
#               mandate involvement). Code retained as DEPRECATED with warning comment.
#           (4) §4-5 POSITION FORMULA DECORRELATION: pos formula added per-subtopic
#               phase-shift (subtopic_offset) to prevent two subtopics with same n_high
#               from colliding on identical mock positions. Note explains collision risk.
#           (5) §4-MANDATE M2 ALTERNATION TWO FIXES: (a) freed slot at source mock must
#               be backfilled from general nonrare pool, never given to the kept member;
#               (b) resolution runs as a fixed-point loop (repeat until zero conflicts
#               in a full pass), not a single pass — relocation can create new conflicts
#               at earlier, already-checked mocks.
#           (6) §4-MANDATE M4 MANDATORY_GROUPS: tie-break changed from highest-r_avg to
#               lowest-cumulative-total (spreads group presence across members instead of
#               biasing toward one). Upfront quota reservation added (same pattern as M1/M6).
#           (7) §17 S2-MANIFEST PRE-FLIGHT CHECK: new mandatory validation — every id in
#               mandatory_every_mock, min_counts, or cadence_windows must have r_avg > 0.
#               r_avg = 0 + mandatory = logical contradiction (ZP rotation caps at 5/50,
#               mandatory demands every mock). HARD STOP with explicit error if violated.
#               Catches manifest errors at load time, not three batches into generation.
#           DoD item 24 added (mandate/r_avg pre-flight).
#           blueprint_version field updated to "1.13".
#
#   v1.12 — 2026-07-02 — QUESTION METADATA INDEX — SCHEMA-SEED LAYER (Step-1 half). Additive,
#           exam-agnostic, zero allocation-behaviour change. (1) Seeds a new universal registry
#           field `question_index: []` in the Step-1 template (§12 S12-1 + field description +
#           all S12-3 examples + §8-5 Step-5 prose): mock-tagged {mock, questions:[{q,
#           subtopic_id, difficulty}]}, seeded here because RS-9 bars Step 2 from adding new
#           top-level fields (Step 2 only APPENDS; Step 3 re-syncs by key). (2) Carries
#           `difficulty_labels` verbatim from section_rules EXAM_STRUCTURE into blueprint.json
#           (default ['Easy','Medium','Hard']), mirroring nat_contract/msq_contract, so Step 2
#           and Step 6 read ONE canonical Complexity vocabulary; §14 schema + field-def added;
#           §7 S7-6 documents the fixed alias (simple→Easy/medium→Medium/hard→Hard) and the
#           SCHEDULE-FIRST assignment that makes the exact-equality distribution check
#           satisfiable by construction. Scope bound: non-3-band label sets also need S7-5 to
#           emit matching bands (flagged, not implemented; 3-band fully supported). Stale sample
#           blueprint_version literal corrected (1.10→1.12). Governed by
#           Contract_QuestionMetadataIndex v1.0; gate logic proven in Phase-1 before encoding.
#
#   v1.11 — 2026-07-01 — ISSUE 2b — THREE NEW MANDATE TYPES (build-time enforcement).
#           mandatory_every_mock (RULE M1) only expresses "one id in every mock". Step 0
#           v2.11 now publishes three more manifest structures that a flat list cannot:
#           mandatory_groups {group:{members,min}}, cadence_windows {id:N}, min_counts {id:k}.
#           Step 1 gains three enforcement rules mirroring M1's proven force-place pattern:
#             • RULE M4 (mandatory_groups) — PER-MOCK: >=min members of each group present;
#               force-place the group's highest-priority absent member if short.
#             • RULE M5 (cadence_windows) — CROSS-MOCK: each windowed id appears >=1 in every
#               sliding window of N consecutive mocks; enforced in the FULL-SERIES pass (BV-7),
#               NOT the per-mock loop (a single mock cannot express a window). This is why
#               Step 2 carries NO cadence gate — cadence is unobservable from one mock.
#             • RULE M6 (min_counts) — PER-MOCK: each id has q_count >= k (M1 generalised from
#               1 to k); force-place k-current, displacing lowest-r_avg non-locked subtopics.
#           BV-MANDATE (RULE M3) extended to assert M4 + M6 per mock and M5 across the series.
#           All check + force-place logic validated in Python on real SSC data (22 group +
#           50 min-count placements, section sums preserved, all rules satisfied) before
#           encoding. Exam-agnostic: empty structures ⇒ vacuous no-op. DoD items 21-23 added.
#   v1.10.1 — 2026-06-30 — MSQ CONTRACT PARITY (contract-sync fix). msq_contract now carries
#           msq_instruction + msq_instruction_hi, copied verbatim from section_rules,
#           structurally parallel to nat_contract.nat_instruction. Step 2/3 still read the
#           instruction from section_rules; this mirror is for visibility/parity so an auditor
#           sees the same contract shape for both answer types. Additive — Step 2 (k-mode/k)
#           and Step 4 (marking) reads are unchanged; inert when multi_select_allowed=false.
#   v1.10 — NAT CONTRACT — ALLOCATION LAYER (cross-step NAT extension, Step 1 half).
#           Carries the second answer-type axis through to blueprint.json, mirroring the v1.8
#           MSQ plumbing: reads per-subtopic `answer_type` ∈ {option, numerical} from
#           section_rules CATEGORY B into answer_type_map; derives top-level `nat_present`
#           (true iff any subtopic is numerical); copies the Step-0 EXAM_STRUCTURE NAT contract
#           verbatim into blueprint.json as `nat_allowed` + `nat_contract` {nat_answer_type,
#           nat_tolerance, nat_instruction}; stores `answer_type` per subtopic in
#           subtopic_list[]. Force-off guard: nat_present is forced False when nat_allowed=false
#           (dormant guarantee, mirrors the multi_present guard). An older section_rules lacking
#           answer_type defaults every subtopic to 'option' (no NAT) — no behaviour change for
#           non-NAT exams. Validated: AST clean; carry-through parity on NAT and non-NAT inputs.
#   v1.9 — VOCABULARY UNIFICATION — PHASE 0 (rename only; NAT prep). Pure rename, no
#           behaviour change: per-subtopic `answer_mode` -> `answer_cardinality`;
#           blueprint flag `msq_present` -> `multi_present`. The section_rules reader and
#           the blueprint consumers accept the OLD names as a fallback (existing
#           section_rules/blueprint files keep working). Non-MSQ exams byte-identical to
#           v1.8. Validated: AST clean; carry-through unchanged on old-name AND new-name
#           inputs. Part of the Steps 0-4 single-vocabulary alignment (answer_type +
#           answer_cardinality) that wires the Explain step's contract.
#   v1.8 — MSQ CONTRACT — ALLOCATION LAYER (cross-step MSQ extension, Step 1 half).
#           DORMANT behind multi_select_allowed: for any exam without multi-select
#           (the default), v1.8 produces a byte-identical blueprint.json to v1.7 except
#           for additive inert fields (multi_present:false, answer_cardinality:"single",
#           multi_select_allowed:false). No allocation maths change.
#           Carries the Step-0 v2.5 MSQ contract forward so Step 2/4 can consume it:
#             (1) blueprint.json top-level gains multi_select_allowed, q_types, and the
#                 MSQ contract block (msq_k_mode, msq_k, negative_marking_by_type,
#                 partial_credit) — read verbatim from section_rules EXAM_STRUCTURE.
#             (2) NEW presence flag multi_present (parallel to passage/figural/di_present):
#                 True iff any subtopic has answer_cardinality=="multi". Step 2 reads it to
#                 enable the MSQ generation path.
#             (3) subtopic_list[] gains answer_cardinality ∈ {single, multi}, copied verbatim
#                 from section_rules CATEGORY B (Step 0 v2.5). This is the Step 2 dispatch
#                 unit. WHOLE-SUBTOPIC MODE (D2): a subtopic is uniformly single- or
#                 multi-answer, so the per-mock allocation schema is UNCHANGED — no MSQ
#                 sub-count is needed inside subtopic_allocations.
#           difficulty_schedule unchanged: MSQ inherits its subtopic's difficulty
#           (Step 0 E-9 already adds the MSQ load term). All MSQ values are config-driven
#           — zero exam names hardcoded. blueprint_version field updated to "1.8".

---

## §1 — SESSION START

Run every step below before writing a single line of B1. No exceptions.

### ══════════════════════════════════════════════════════════════
### INPUT DOCUMENTS ARE THE SOLE SOURCE OF TRUTH — MEMORY PROHIBITION
### ══════════════════════════════════════════════════════════════

```
ALL decisions about subtopic scope, Format values, and allocation rules
MUST be derived from the input documents uploaded in THIS session:
  • Exam Pattern document
  • Analysis Word Document(s)
  • Frequency Excel

Claude's memory of prior sessions, prior conversations, or prior runs
MUST NEVER be used to:
  (a) Add subtopics not present in the Analysis doc
  (b) Remove subtopics present in the Analysis doc
  (c) Change Format values from what the Excel contains
  (d) Apply any "ban", "exclusion", or "structural change" rule
      not explicitly present in the input documents of THIS session
  (e) Override the allocation algorithm defined in this spec

SPECIFIC KNOWN VIOLATION PATTERN TO NEVER REPEAT:
  Applying a "FIGURAL subtopic ban" from memory while the uploaded Excel
  contains FIGURAL subtopics with r_avg > 0 that belong in §4 allocation.
  This is a critical error. The input documents decide scope. Memory does not.

If memory conflicts with input documents → input documents WIN. Always.
If in doubt → read the input document. Never assume. Never recall.
```

### ═══════════════════════════════════════════════════════════════

### S1-1 — Trigger parsing

```
Received trigger: MockBlueprint [N_mocks] [--difficulty flag]

Trigger matching is case-insensitive:
  MockBlueprint / mocktestblueprint / MOCKTESTBLUEPRINT all accepted.

Parse and validate:
  ExamCode  : must be alphanumeric + underscore only
              If ExamCode not specified → ask: "What ExamCode for this exam?
               (alphanumeric + underscore only, e.g. SSC_CGL_TIER1)"
              Invalid chars (hyphen, space, dot) → flag immediately:
              "ExamCode cannot contain [char]. Did you mean [corrected]?"
              Partial match on intent acceptable (e.g. 'MockBlueprint SSC CGL 50'
              → "Did you mean SSC_CGL?") — ask user to re-enter.

  N_mocks   : must be a positive integer > 0
              If ≤ 0 or non-integer → "N_mocks must be a positive integer. Received: [X]"
              If not specified → ask: "How many mocks in this series?"
              If > 100 → flag: "N_mocks = [X] is unusually large. Confirm to proceed."
              After confirmation → proceed normally.

  --difficulty flag (optional):
              Absent             → default 25:25:50 applied silently (no question asked)
              --difficulty E:M:H → parse as whole-number percentages; validate in §7
              --difficulty progressive → ask user to define bands after S1-6 (ref §7 S7-3)
              Unknown flag       → flag and ask user to correct
```

### S1-2 — File inventory

```
List ALL received files immediately after trigger:

  "Received files:
   • [filename].[ext]  ([type], [size])
   • [filename].[ext]  ([type], [size])
   ..."

Check for each mandatory input:
  ✓ Exam Pattern    : image (JPG/PNG), PDF, .docx, or plain text in chat
  ✓ Analysis doc(s) : .docx or .doc only — NOT .pdf, NOT .xlsx
  ✓ Frequency Excel : .xlsx or .xls

Wrong file type handling:
  If Analysis doc uploaded as .pdf:
    "Analysis doc must be .docx or .doc, not .pdf.
     Please convert and re-upload."
  If Frequency Excel uploaded as .docx or .pdf:
    "Frequency Excel must be .xlsx or .xls. Please re-upload."

If any mandatory input is missing:
  Flag it here and route to §10 for fallback:
    Missing Exam Pattern      → §10 S10-4
    Missing ALL Analysis docs → §10 S10-5
    Missing ONE Analysis doc  → §10 S10-6
    Missing Frequency Excel   → §10 S10-7
    Missing both Analysis AND Excel → §10 S10-8
  (Full fallback procedures in §10)

If files uploaded AFTER trigger in same session:
  Claude pauses, re-inventories all available files, then proceeds.
  Never start B1 with an incomplete file set.
```

### S1-2b — Allocation engine mandate (blueprint_core.py — HARD STOP)

```
# ════════════════════════════════════════════════════════════════════════
# MANDATE — blueprint_core.py IS MANDATORY (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   All allocation MATH in this spec — r_avg (§3), the proportional split +
#   largest-remainder deficit (§4-2), the EXACT MATRIX FILL (§4-5b), the
#   difficulty counts (§7-4), the three-axis schedule (§7-7), and slugify
#   (§17) — is provided by the SHARED ENGINE blueprint_core.py. This spec no
#   longer inlines those function bodies (single source of truth; the same
#   engine backs the Subject/Topic/Sub-Topic scoped blueprints, so a fix lands
#   once). Its correctness is proven by blueprint_core_test.py +
#   qa_pass2_differential.py (both delivered alongside it).
#
#   blueprint_core.py is UNIVERSAL — no exam-specific edits, no [ExamCode]
#   prefix. It parameterises itself purely from the plain-data arguments the
#   wrappers pass. Uploaded once, reused in every exam project.
#
#   If blueprint_core.py is absent from the project → HARD STOP. Print:
#     "HARD STOP (ENGINE MANDATE): blueprint_core.py not found in the
#      [ExamCode] project Files. Step 6 cannot allocate without it. It is
#      universal (uploaded once, reused in every project) — upload it, then
#      re-run MockBlueprint."
```

```python
import os, shutil, subprocess, sys

# 1) PRESENCE GATE — engine must be in the project.
_engine_src = '/mnt/project/blueprint_core.py'
if not os.path.exists(_engine_src):
    raise SystemExit(
        "HARD STOP (ENGINE MANDATE): blueprint_core.py not found in the "
        "[ExamCode] project Files. Step 6 cannot allocate without it. It is "
        "universal (uploaded once, reused in every project) — upload it, then "
        "re-run MockBlueprint.")

# 2) COPY TO WORKING DIR so `import blueprint_core` resolves (cwd = /home/claude).
shutil.copy(_engine_src, '/home/claude/blueprint_core.py')
if '/home/claude' not in sys.path:
    sys.path.insert(0, '/home/claude')

# 3) HEALTH GATE — the engine must self-test clean before we trust it.
_st = subprocess.run([sys.executable, '/home/claude/blueprint_core.py', '--self-test'],
                     capture_output=True, text=True, timeout=60)
_out = (_st.stdout + _st.stderr).strip().splitlines()
_last = _out[-1] if _out else ''
import re as _re
if _st.returncode != 0 or not _re.match(r'SELF-TEST: (\d+)/\1 PASS', _last):
    raise SystemExit(
        f"HARD STOP (ENGINE MANDATE): blueprint_core.py --self-test did not pass "
        f"({_last!r}). The engine is corrupt or the wrong version — re-upload the "
        f"delivered blueprint_core.py and re-run.")

# 4) IMPORT — every §3/§4/§7/§17 block that follows uses `bc`.
import blueprint_core as bc
```

### S1-3 — ExamCode collision check

```
Check project knowledge for any existing files with this ExamCode:
  Check for: [ExamCode]_blueprint.json AND [ExamCode]_registry.json

  If ANY [ExamCode] file already exists in project knowledge:
    "ExamCode [X] already has files from a prior run.
     If this is a re-run: existing files will be replaced on delivery.
     If this is a different exam: use a different ExamCode.
     Confirm to proceed."
  Wait for user confirmation before continuing.
  If new ExamCode (no prior files found): proceed automatically.
```

### S1-4 — ExamCode match verification

```
After reading Exam Pattern document:
  Extract exam name from pattern doc (if readable).
  Compare against ExamCode in trigger using fuzzy match:
    Rules: underscore→space, case-insensitive, numbers match words
    (e.g. SSC_CGL_TIER1 matches "SSC CGL Tier 1" or "SSC CGL Tier-1")
    If Claude is confident (>80%) it matches: proceed silently.
    If ambiguous (e.g. SSC_CGL could be Tier 1 or Tier 2): ask user to confirm.

  If clear mismatch (e.g., ExamCode=SSC_CGL_TIER1, doc says "IBPS PO"):
    "Mismatch detected:
     Trigger ExamCode : SSC_CGL_TIER1
     Pattern doc shows: IBPS PO
     Please correct the ExamCode or upload the correct pattern doc."
    Wait for user response. Never silently proceed with a clear mismatch.

  If exam name not extractable (blurry image, no title visible):
    Skip S1-4 match check.
    Document assumption: "Exam name assumed from ExamCode: [ExamCode]"
    in Paper Structure sheet. Proceed to S1-5.
```

### S1-5 — Format column check

```
Note: S1-5 performs a quick column-EXISTENCE check only.
Full reading of Format values happens in B1 Step 2 (§8-2).

After opening Frequency Excel during session start:
  Check Master Data sheet for a column named 'Format' (or close variant).
  Master Data sheet is the primary source — subject-specific tabs are secondary
  and may not have Format column separately.

  If Format column present in Master Data sheet:
    "Format column: ✓ present"
    → proceed to S1-6 normally

  If Format column absent from Master Data sheet:
    "Format column: not found in Master Data sheet"
    → Format inference fallback applies (ref §10 S10-7 / S10-11)
    → Claude will infer Format from subtopic names during B1, with user confirmation
    → Document as assumption in Paper Structure sheet
```

### S1-6 — Verification summary output

```
Print before B1 begins:

  "=== MockBlueprint Session Start ===
   Exam         : [exam_name] ([ExamCode])
   Sections     : [N] sections found
   Analysis docs: [N] received ([subject list])
   Excel years  : [year list, e.g. 2019–2025]
   Format column: [present / not found — inference fallback applies]
   N_mocks      : [N]
   Difficulty   : [25/25/50 default | E:M:H custom | progressive]
   Collision    : [none | prior run detected — confirmed by user]
   Status       : Ready → proceeding to B1
   =================================="

If any critical issues detected (mismatch, missing mandatory file, wrong type):
  Replace last line with:
  "Status : HALTED
   Reasons:
     — [reason 1]
     — [reason 2]   (list ALL issues, one per line)
   Waiting for user input."
  Do not proceed to B1 until ALL issues resolved.
```

### S1-7 — Session continuity (resuming from prior B2 session)

```
If user uploads blueprint.json from a prior B2 session:

  Step 1: Read total_mocks from blueprint.json.
          If trigger also specifies N_mocks AND it differs from blueprint.json total_mocks:
            "N_mocks conflict:
             Trigger says    : [trigger N_mocks]
             blueprint.json  : [blueprint total_mocks]
             Blueprint is authoritative. Resuming with N_mocks = [blueprint total_mocks].
             Trigger N_mocks ignored on resume."

  Step 2: Read len(mocks[]) → K mocks already completed.
          Next batch starts from: K + 1.
          Next batch ends at:     min(K + 10, total_mocks).

          Print: "Resuming from prior session.
                  Mocks completed: [K] of [total_mocks]
                  Next batch: mocks [K+1] to [min(K+10, total_mocks)]"

  Step 3: Stale file detection.
          If user explicitly states a starting mock M but len(mocks[]) ≠ M − 1:
            "Stale blueprint.json detected:
             You said: start from mock [M]
             Blueprint has: [K] mocks completed (expected [M-1])
             Please upload the latest blueprint.json before continuing."
            Wait for user action.
          If no explicit starting mock stated: Claude always starts from K+1.
          No stale detection needed — len(mocks[]) IS the source of truth.

blueprint.json total_mocks and mocks[] are the single source of truth.
No explicit batch counter needed — all progress derived from blueprint.json state.
```

## §2 — INPUT PROCESSING

How Claude reads each input document. All reading happens during B1.

### S2-1 — Reading exam structure (from exam_config.json or Exam Pattern document)

```
PRIMARY SOURCE (v1.19): exam_config.json from project knowledge.
  Step 2a (v2.5+) writes exam_config.json with sections[], marking_scheme[], level,
  medium, max_attempt — all extracted from the standardized 3-tab xlsx and validated
  (V1-V10). When present, this is the authoritative source — no AI interpretation needed.

  Read from exam_config.json:
    sections[]       : list of {name, q_count, q_range, max_attempt, subject_order}
    total_questions  : sum of all section q_counts
    marking_scheme[] : per-range {q_range, question_type, correct_marks, negative_marks}
    level            : academic level (e.g., "Post Graduation", "Graduation")
    medium           : exam language (e.g., "English", "Hindi", "Bilingual")
    n_papers         : NOT in exam_config — infer from context or ask user.
                       Default: 1 (single-paper exam). Multi-paper exams (UPSC CSE)
                       require user confirmation.

  SECTION ≠ SUBJECT NOTE:
    Section names in exam_config (e.g., "Part A", "Part B", "Part C") are OTS
    display labels — they define paper structure, NOT taxonomy Subjects.
    The taxonomy (Subject > Topic > Subtopic) comes from Analysis docs (S2-2).
    A single Subject from the syllabus can span multiple sections.
    See Step 2a v2.5 S2-2a for the full architectural note.

  Q-range validation (same checks as Step 2a — defensive re-check):
    Ranges must be: non-overlapping AND contiguous.
    If any gap or overlap detected in exam_config.json → HARD STOP (corrupt config).

FALLBACK (legacy): Exam Pattern document (image/PDF/.docx/plain text).
  Used when exam_config.json is absent from project knowledge.
  Acceptable formats: image (JPG/PNG), PDF, .docx, plain text in chat.
  Multi-page PDF: read only the section structure table; ignore eligibility, dates, etc.

  Extract from exam pattern:
    sections[]  : list of section names in order
    sec_qs[]    : Q count per section (use OFFICIAL notified count, not PYQ-observed)
    q_range[]   : [start, end] inclusive per section
    total_qs    : Σ sec_qs across all sections
    n_papers    : number of distinct papers in this exam's structure
                  (e.g., SSC CGL Tier 2: n_papers=1 for Paper-1 only;
                          UPSC CSE: n_papers=2 for GS Paper I and GS Paper II)
                  NOT to be confused with PYQ shift/paper counts in Excel.
                  Stored in blueprint.json top-level as n_papers (int).
    marking_scheme : infer single-range entry [1, total_qs] if marks stated;
                     level/medium/max_attempt set to defaults.

  Q-range extraction:
    Exam patterns use varied formats — Claude converts all to [start, end] integer pairs:
      "Questions 1 to 25"   → [1, 25]
      "Q.1-Q.25"            → [1, 25]
      "1–25" / "1-25"       → [1, 25]
      Table row with 25 Qs and prior section ending at Q0 → [1, 25]
    If range not explicit: infer from section order and Q counts.
    If inference is uncertain: state assumption and ask user to confirm.

  Q-range validation (run immediately after extraction):
    Ranges must be: non-overlapping AND contiguous.
    Valid  : [1,25], [26,50], [51,75], [76,100]  — no gaps, no overlaps.
    Invalid: [1,25], [24,50]   — overlap at Q24-Q25 → flag immediately.
    Invalid: [1,25], [27,50]   — gap at Q26 → flag immediately.
    "Section ranges overlap/gap detected. Please clarify before proceeding."

  Total Q cross-validation:
    If exam pattern explicitly states a total Q count (e.g., "Total: 100 Questions"):
      Verify total_qs == pattern_stated_total.
      If mismatch: "Pattern states [N] total Qs but sections add up to [M].
                    Please clarify which is correct."
      Wait for user response.

  If exam pattern is ambiguous or blurry:
    State best-effort interpretation.
    Document as assumption in Paper Structure sheet.
    Wait for user confirmation before B1 proceeds.

  If exam pattern is in Hindi/regional language:
    Translate section names to English.
    Document translations in Paper Structure sheet.

BOTH PATHS produce the same output contract:
  sections[], total_questions, marking_scheme[], level, medium, n_papers
  ready for blueprint.json population at B1.
```

### S2-2 — Reading Analysis Word Document(s)

```
Accepted arrangements:
  Option A: one .docx per subject section (e.g., GI.docx, GA.docx, QA.docx, English.docx)
  Option B: all subjects combined in one .docx
  Option C: mix — some subjects separate, some combined
  Option D: plain text table pasted directly in chat
             (any readable format — Claude extracts Topic|Sub-Topic|Q-count structure.
              If format is unclear: Claude asks user to clarify before extraction.)

From each Analysis doc, extract per section:
  topics[]   : list of topic names
  subtopics[]: list of subtopic names under each topic
  q_count[]  : combined PYQ Q count per subtopic (all years together)

Source priority (when both Analysis doc and Excel available):
  Subtopic names  → Analysis doc wins over Excel
  Combined counts → Analysis doc wins over Excel
  Year-wise data  → Excel ONLY (Analysis doc has no year-wise split)

Translation rule:
  All subtopic names must be in English.
  If name is in Hindi/regional language: translate and document in Paper Structure sheet.
  Q counts are never changed during translation.

Minor corrections:
  Apply silently (no user confirmation needed).
  Document only significant corrections in Paper Structure sheet:
    ✓ Document: spelling fixes (e.g., 'Algebric' → 'Algebraic')
    ✓ Document: merged duplicate subtopics
    ✗ Skip: trivial capitalisation changes ('mirror image' → 'Mirror Image')
    ✗ Skip: whitespace trimming

Subtopic with q_count = 0 in Analysis doc:
  Include it. q_count=0 → r_avg=0 → classified as Zero-PYQ → goes to ZP rotation (§5).
  Do NOT exclude it from the subtopic list.

Duplicate subtopic in same section (same name, same topic):
  Merge Q counts → keep once.
  Document: "Duplicate subtopic [X] in [section] merged. Combined q_count=[N]."

Same subtopic under different topics in same section:
  Keep separate entries — identified by (section_name, topic_name, subtopic_name) tuple.
  e.g., "Analogy" under "Verbal" and "Analogy" under "Non-Verbal" are DIFFERENT subtopics.

CROSS-STEP SUBTOPIC CONTRACT (v1.7 — supersedes the old name-match rule):
  Step 5 (PYQExtract) is the SINGLE SOURCE OF TRUTH for the subtopic
  vocabulary. It mints a stable subtopic_id for every subtopic and publishes
  [ExamCode]_subtopic_manifest.json. Step 1 (THIS step) is a CONSUMER:

  RULE 1 — READ THE MANIFEST. Step 1 MUST load [ExamCode]_subtopic_manifest.json
    (see S2-MANIFEST) at session start. Every subtopic Step 1 places into the
    blueprint MUST carry the subtopic_id taken VERBATIM from the manifest.
    Step 1 NEVER mints its own id and NEVER relies on display-name matching.

  RULE 2 — RESOLVE EACH ANALYSIS-DOC SUBTOPIC TO A MANIFEST id. When reading the
    Analysis docs for counts, map each subtopic to its manifest entry by:
      (a) exact display_name match against manifest.subtopics[].display_name, else
      (b) slugify()-equal match (same recipe as Step 0), else
      (c) HARD STOP: "Subtopic '[name]' from Analysis doc has no manifest id.
          Re-run Step 0 so the manifest includes it, then re-run Step 1."
    There is no silent fallback. A subtopic with no id cannot enter the blueprint.

  RULE 2a — NO BYPASS (v1.21). EVERY subtopic that enters the blueprint —
    whether from the Analysis doc, the taxonomy, the syllabus, or any
    fallback/supplement path (§5 ZP rotation setup, §10 missing-data fallbacks)
    — MUST resolve to a manifest id via resolve_subtopic_id(). There is NO
    code path that creates a subtopic entry without a manifest-resolved id.

    If resolve_subtopic_id() returns HARD STOP → the blueprint build HALTS.
    The resolution is ALWAYS upstream: re-run Step 5 (v2.20+ runs taxonomy
    sync to mint ids for ALL taxonomy subtopics including zero-PYQ ones).
    Step 6 NEVER self-mints an id, NEVER auto-generates a sequential id,
    NEVER creates a fallback id.

    SPECIFICALLY BANNED:
      - max_id = max(int(k[2:]) for k in MANIFEST_IDS) + 1
      - f"ST{counter:04d}" where counter is not from the manifest
      - Any id not returned by resolve_subtopic_id()
      - Any subtopic_list entry where subtopic_id was not resolved from manifest

    WHY THIS RULE EXISTS: SSC CGL Tier 2 Mock 1 — Step 6 discovered 7 syllabus-
    only subtopics via fallback paths and auto-generated sequential IDs (ST0097–
    ST0103). Step 7 correctly HARD STOPPED because these IDs existed in neither
    the manifest nor section_rules.md. The sequential format (ST{NNNN}) vs the
    manifest's slugify format (section.topic.subtopic) made the violation obvious.

  RULE 3 — ENFORCE MANIFEST MANDATES AT BUILD TIME (see S4-MANDATE). Every id in
    manifest.mandatory_every_mock MUST appear in EVERY mock. No two ids that share
    an alternation_group may appear in the SAME mock. [v1.11] Additionally: ≥1 (or the
    group's min) member of every mandatory_groups group appears in every mock; every
    min_counts id has ≥k questions per mock; and every cadence_windows id appears at
    least once in every N-mock window (cross-mock, checked in BV-7). These are
    guaranteed by construction — a blueprint that violates them is never emitted.

  WHY THIS REPLACED THE OLD RULE: the previous rule ("both steps use EXACT names
  from the Analysis doc; re-run both if a name changes") was manual discipline.
  Two independent derivations drifted (~70% mismatch on SSC CGL T1). The id
  contract removes the discipline requirement: identity flows from ONE place.

Mixed doc — some topics have subtopic breakdown, some don't:
  Apply per-topic: if a topic has no subtopic detail → use topic name as single subtopic.
  If a topic has subtopics → extract all subtopics normally.
  Both patterns can coexist in the same Analysis doc.

Analysis doc absent for one subject → ref §10 S10-6.
Analysis doc absent for all subjects → ref §10 S10-5.
Analysis doc absent for multiple but not all subjects → apply §10 S10-6 per missing subject.
```

### S2-3 — Reading the Frequency Excel

```
Expected sheets: 'Master Data ([N] Years)' or similar, and subject-specific tabs.

Sheet identification:
  If sheet names match expected: use directly.
  If sheet names differ: Claude identifies correct sheets by content structure.
  Column identification — prefer header-based lookup over positional:
    Row 1 headers: 'Subject', 'Topic', 'Sub-Topic', 'Format', 'Avg/Paper [year]', 'Papers In [year]'
    If headers present: read by header name (robust to column reordering).
    If no headers: use positional defaults (Col A=Subject, B=Topic, C=Sub-Topic, D=Format)
                   and flag: "Excel has no column headers — using positional defaults."
  If ambiguous: flag and ask user before proceeding.

From Master Data sheet, read per subtopic row:
  Subject          : 'Subject' column (Col A if positional)
  Topic            : 'Topic' column (Col B if positional)
  Sub-Topic        : 'Sub-Topic' column (Col C if positional)
  Format           : 'Format' column (Col D if positional) — TEXT/FIGURAL/PASSAGE/DI
  Avg/Paper [year] : one column per year
  Papers In [year] : one column per year

Data quality checks per row:
  Blank Avg/Paper cell:
    Treat as 0 Qs for that year (auto-handled, no flag needed).

  Papers In [year] = 0 but Avg/Paper [year] > 0 for any subtopic:
    Flag as data entry error for that year column:
    "Data error: [year] column has Avg/Paper > 0 for [subtopic] but Papers In = 0.
     Treating [year] as 0 papers for all subtopics."

  Missing year column:
    Treat as 0 papers for that year. Note in Paper Structure sheet.

Extra subtopics in Excel not in Analysis doc:
  Flag each: "Subtopic [X] in Excel not found in Analysis doc taxonomy.
              Using Analysis doc as taxonomy authority — [X] excluded unless
              user adds it to the Analysis doc."
  These extra subtopics are NOT added to the blueprint automatically.

Q count mismatch between Analysis doc and Excel:
  Formula: |doc_count - excel_count| / max(doc_count, excel_count)
  If both = 0: no mismatch (skip check).
  If one = 0 and other > 0: treat as 100% mismatch → flag.
  If mismatch > 10%: flag (Analysis doc is authoritative, Excel used for year-wise only).
  If mismatch > 25%: request user confirmation before proceeding.
  If mismatch ≤ 10%: auto-accept Analysis doc count silently.

COVERAGE VALIDATION GATE (v1.26 — mandatory after reading Excel; D6-7 per-paper fix):
  D6-7 BUG (was v1.18): the numerator summed "Combined Qs", which is the MULTI-YEAR TOTAL
  (Σ over every paper in the corpus). On a 3-year Excel that is ~3× one paper, so coverage_pct
  read ~300% and ALWAYS passed ≥95% — the gate could NEVER detect the under-coverage it exists
  to catch (a real 40% loss still shows ~180%). FIX: compare PER-PAPER expected count vs the
  per-paper exam total.
  After reading all subtopic rows from the Frequency Excel, compute:
    # PER-PAPER numerator: sum the Avg/Paper column (avg_combined = Combined Qs / total_papers,
    # already written by Step 5 §16-6). Equivalent fallback if that column is unavailable:
    #   excel_per_paper_qs = sum(Combined Qs) / total_papers,
    #   total_papers = Σ "Papers In [year]" across all year columns   (total_papers ≥ 1).
    excel_per_paper_qs = sum(Avg/Paper for all subtopic rows in Master Data)
    exam_total_qs      = total_questions from Exam Pattern or exam_config.json

  Comparison:
    If exam_total_qs is known (from Exam Pattern document):
      coverage_pct = excel_per_paper_qs / exam_total_qs * 100   # per-paper vs per-paper
      
      coverage_pct ≥ 95%  → PASS silently.
      90% ≤ coverage_pct < 95% → FLAG:
        "Frequency Excel accounts for [excel_per_paper_qs] Qs but exam has
         [exam_total_qs] total ([coverage_pct]% coverage). [gap] questions
         were not classified in Step 5. Blueprint weightages may be slightly
         inaccurate. Confirm to proceed."
      coverage_pct < 90%  → HALT:
        "Frequency Excel accounts for [excel_per_paper_qs] Qs but exam has
         [exam_total_qs] total ([coverage_pct]% coverage). [gap] questions
         were not classified in Step 5. Blueprint CANNOT be generated from
         incomplete data — topic weightages will be distorted.
         
         Action required: Re-run Step 5 (PYQExtract) to fix classification
         gaps, then re-run Step 6 with the corrected Frequency Excel."
        Do NOT proceed until user provides corrected Excel or confirms override.

    If exam_total_qs is NOT known (Exam Pattern absent — S10-4 fallback):
      Skip this gate. Note in Paper Structure sheet:
      "Coverage validation skipped — Exam Pattern not available."

  RATIONALE: This gate prevents the MPPSC Botany failure mode where Step 5
  produced a Frequency xlsx with only 62% coverage (93/150 Qs). Without this
  gate, Step 6 consumed the incomplete data silently and generated a blueprint
  where Diversity of Life Forms (22.7% of actual exam) received only 3.2%
  allocation — a catastrophic distortion that renders the mock test useless.
```

### S2-4 — Missing document fallback routing

```
If any document is missing: do NOT silently proceed.
Route to §10 (Missing Document Handling) for the specific scenario:

  Missing Exam Pattern                        → §10 S10-4
  Missing ALL Analysis docs                   → §10 S10-5
  Missing ONE Analysis doc                    → §10 S10-6
  Missing MULTIPLE (but not all) Analysis docs→ §10 S10-6 applied per missing subject
  Missing Frequency Excel                     → §10 S10-7
  Missing both Analysis AND Excel             → §10 S10-8
  Incomplete Analysis doc                     → §10 S10-9
  Missing Excel year column                   → §10 S10-10 (auto-handled)
  Partial Format column                       → §10 S10-11
```

## §3 — FREQUENCY CALCULATION

How r_avg (recency-weighted average) is computed per subtopic.
This is the foundation of the entire allocation algorithm.

### S3-1 — Identify recency years

```
'Last 2 years' = the 2 most recent years where at least one subtopic has Papers In > 0.
NOT the 2 most recent calendar years.
NOT years that exist as columns but have all-zero paper counts (exam not held that year).

Algorithm:
  valid_years = [year for year in excel_years
                 if any(papers_in[year][S] > 0 for S in all_subtopics)]
  recent_years, older_years = bc.split_recency(valid_years)   # ENGINE: last 2 vs earlier
  #   (identical to sorted(valid_years)[-2:] / [:-2]; single source of truth)

  Weights: recent_years → 2×, older_years → 1×

Example: Excel has columns 2019, 2020, 2022, 2024, 2025
  All years have Papers In > 0 → valid_years = [2019,2020,2022,2024,2025]
  recent_years = [2024, 2025] (weight 2×)
  older_years  = [2019, 2020, 2022] (weight 1×)

If Excel has exactly 2 valid years: both get 2× (effectively equal weight — intentional).
If Excel has exactly 1 valid year: no weighting applies → see CASE 1 in §3-4.
If Excel has NO year columns (only taxonomy columns like Subject/Topic/Sub-Topic/Format):
  Flag: "Excel has no frequency data columns (year columns). Routing to §10 S10-7."
  Do NOT silently compute r_avg = 0 for all subtopics.
```

### S3-2 — Recency-weighted average formula

```python
# excel_years  = list of valid year strings from Excel columns
#                (populated during B1 Step 2 — §8-2)
#                e.g., ["2019","2020","2022","2024","2025"]
# recent_years = last 2 entries of sorted valid_years (from S3-1)

# NOTE: pyq_subtopics and zero_pyq_subtopics are initialized once in §3-5 (S3-5).
# Do NOT reinitialize them here — this block is per-subtopic formula only.

import blueprint_core as bc   # ENGINE (mandated in S1-2b; copied to /home/claude)

# For each subtopic S: normalise this subtopic's per-year Excel cells into the plain
# rows the engine expects, then compute the recency-weighted r_avg via the engine.
# The 'Avg/Paper <year>' / 'Papers In <year>' string-key PARSING stays here (it is a
# parsing artifact of the Excel shape); the recency-weighted FORMULA lives in the
# engine (bc.compute_r_avg — identical math, verified vs this loop over 20k inputs).
year_rows = [
    {'avg':    excel.get('Avg/Paper ' + year, {}).get(S, None),
     'papers': excel.get('Papers In ' + year, {}).get(S, None),
     'recent': year in recent_years}
    for year in excel_years
]
r_avg, _ravg_warnings = bc.compute_r_avg(year_rows)   # 0.0 → Zero-PYQ (handled by §5)

# Surface the engine's data-quality warnings (a year with Papers In=0 but Avg/Paper>0).
# NOTE: the engine's message identifies the condition but not the specific year; the
# subtopic S is prepended here. This is a diagnostic-log change only — the r_avg VALUE
# is byte-identical to the pre-engine loop.
for _w in _ravg_warnings:
    flag(f"{S}: {_w}")
```

### S3-3 — Pooled average (reference only — never used in allocation)

```python
# Pooled avg = simple combined average with no recency weighting
# Stored in Summary Stats Col G for human reference only
# NOT stored in blueprint.json

# Compute from available columns (no 'Total Qs' column exists in Excel)
total_qs_all_years     = sum(
    (excel.get('Avg/Paper ' + yr, {}).get(S, 0) or 0) *
    (excel.get('Papers In ' + yr, {}).get(S, 0) or 0)
    for yr in excel_years
)
total_papers_all_years = sum(
    (excel.get('Papers In ' + yr, {}).get(S, 0) or 0)
    for yr in excel_years
)

pooled_avg = round(total_qs_all_years / total_papers_all_years, 4) if total_papers_all_years > 0 else 0.0

# NEVER use pooled_avg in allocation.
# NEVER substitute pooled_avg for r_avg.
```

### S3-4 — Edge cases

```
CASE 1: Only 1 valid year of Excel data
  → Use that single year at 1× weight (no recency amplification).
  → r_avg = avg_per_paper for that year (from formula above).
  → If that single year also has Papers In = 0: r_avg = 0.0 → subtopic is Zero-PYQ.
  → Document: "Only 1 year of data available. Recency weighting not applied."

CASE 2: r_avg = 0.0 after formula
  → Subtopic never appeared in any valid year of PYQ data.
  → Classify as Zero-PYQ.
  → Do NOT set quota via §4 allocation — handled entirely by §5 (ZP Rotation).

CASE 3: All subtopics in a section have r_avg = 0
  → section_total_r_avg = 0 → §4-2 scaled_avg formula would divide by zero.
  → Apply equal distribution: each subtopic gets equal share.
  → ZP rules (§5) still apply — all subtopics go to ZP rotation.
  → See EC-3 (§16) for complete step-by-step implementation.
  → Document as assumption in Paper Structure sheet.

CASE 4: Missing Frequency Excel entirely
  → Recency weighting not possible.
  → Use Analysis doc combined Q counts as pooled avg proxy.
  → No recency weighting applied.
  → See §10 S10-7 for full procedure.
```

### S3-5 — Zero-PYQ classification

```python
# Initialize storage before processing subtopics
pyq_subtopics      = {section: [] for section in sections}
zero_pyq_subtopics = {section: [] for section in sections}

# Classify each subtopic after r_avg is computed
for section in sections:
    for S in all_subtopics[section]:
        if r_avg[S] == 0.0:
            zero_pyq_subtopics[section].append(S)   # never appeared in PYQ
        else:
            pyq_subtopics[section].append(S)         # appeared at least once

# Zero-PYQ subtopics are EXCLUDED from §4 allocation.
# They are handled entirely by §5 (Zero-PYQ Rotation).
#
# Use these variable names consistently throughout §4, §5, §8, §9:
#   pyq_subtopics[section]       → list of subtopics with r_avg > 0
#   zero_pyq_subtopics[section]  → list of subtopics with r_avg = 0
#
# ─────────────────────────────────────────────────────────────
# CRITICAL — THE ONLY EXCLUSION CRITERION IS r_avg = 0.0
# ─────────────────────────────────────────────────────────────
# Format value (TEXT / FIGURAL / PASSAGE / DI) is NOT a classification
# criterion here and has ZERO effect on pyq/zero_pyq assignment.
# A FIGURAL subtopic with r_avg > 0 → goes into pyq_subtopics[section].
# A FIGURAL subtopic with r_avg = 0 → goes into zero_pyq_subtopics[section].
# The Format value is only read in §6 for flag-setting and Step 2 pipelines.
# Ref: §6 GOLDEN RULE — FORMAT IS CLASSIFICATION ONLY, NEVER EXCLUSION.
# ─────────────────────────────────────────────────────────────
```

### S3-6 — Importance classification (reference only)

```
After r_avg computed for all subtopics:
  High   : r_avg > 1.0            (appears more than once per paper on average)
  Medium : 0.3 ≤ r_avg ≤ 1.0     (appears in most papers, ~1 Q each)
  Low    : r_avg < 0.3            (appears occasionally, less than 1-in-3 papers)

Boundary values: r_avg = 0.3 → Medium. r_avg = 1.0 → Medium.

Stored in Summary Stats sheet Col E (Type column) for human reference only.
NOTE: Col E in Summary Stats stores the combined type label, e.g.:
      "PYQ-based (High)"  — r_avg > 1.0
      "PYQ-based (Medium)"— 0.3 ≤ r_avg ≤ 1.0
      "PYQ-based (Low)"   — r_avg < 0.3
      "Zero-PYQ"          — r_avg = 0.0
      This is consistent with §15 S15-3 Col E definition "Type (PYQ-based / Zero-PYQ)".
NEVER used in allocation algorithm.
Thresholds are fixed — not configurable per exam.
```

## §4 — ALLOCATION ALGORITHM

The core of Step 1. Determines exactly how many Qs each subtopic gets in each mock.
Three-phase algorithm:
  Phase 0 (NEW): Batch-coverage pass — guarantees every PYQ subtopic appears
                 at least once within every 10-mock batch window.
  Phase 1       : Pre-schedules rare subtopics (r_avg < RARE_THRESHOLD, default 0.1) evenly across series.
  Phase 2       : Fills remaining slots by even-spread for non-rare subtopics.

BATCH COVERAGE GUARANTEE (Option C — architect decision):
  Every PYQ subtopic (r_avg > 0) must appear ≥ 1 Q in EVERY 10-mock batch.
  This is a hard constraint — it overrides proportional frequency for low-r_avg subtopics.
  Accepted trade-off: rare subtopics appear more frequently than their PYQ r_avg suggests.
  Purpose: student gets exposure to every subtopic in every 10-mock practice window.

BATCH WINDOW DEFINITION:
  batch_size = bp.get('batch_size_qs', 10)  # read from blueprint; default 10 for most exams
  Batch 1 = mocks  1-10, Batch 2 = mocks 11-20, ..., Batch K = mocks (K-1)*10+1 to K*10
  Last batch may be smaller if N_mocks is not a multiple of 10 (handled in EC-11).
  n_batches = math.ceil(N_mocks / batch_size)

FEASIBILITY PRE-CHECK runs inside §4-1 (per-section setup) before quota computation.
  Full details and resolution options in EC-11 (§16).

# Requires: import math (for math.floor throughout §4)
# AlgorithmError  = RuntimeError  (alias used for fatal algorithm failures)
# ValidationError = ValueError    (alias used for data validation failures)
# rare_subs_by_section    = {}    (populated in S4-3; used by §9 BV-4)
# nonrare_subs_by_section = {}    (populated in S4-3)
# batch_size = 10                 (fixed batch window — matches B2 batch size; set in §4-1)
# n_batches  = math.ceil(N_mocks / batch_size)  (set in §4-1)

### S4-1 — Per-section setup

```python
# Run independently for EACH section.
# Sections NEVER allocated together — no cross-section constraints.
# §5 (ZP rotation) MUST run BEFORE §4 so that zp_slot[section][m] is available.

AlgorithmError  = RuntimeError
ValidationError = ValueError

# Global constants for batch coverage (Option C)
batch_size = bp.get('batch_size_qs', 10)         # read from blueprint; default 10
n_batches  = math.ceil(N_mocks / batch_size)  # e.g., N_mocks=50 → n_batches=5

for section in sections:
    sec_qs = section['total_qs']   # Q count for this section per mock
    N      = N_mocks               # total mocks in series

    # ── FEASIBILITY PRE-CHECK (Option C batch coverage) ───────────────────────
    # Must run before quota computation. Halts immediately if infeasible.
    # Full EC-11 documented in §16.
    batch_slots = batch_size * sec_qs   # total Q slots available per batch per section
    n_pq_subs   = len(pyq_subtopics[section])
    if n_pq_subs > batch_slots:
        raise AlgorithmError(
            f"Section {section['name']}: Batch coverage guarantee (Option C) is INFEASIBLE. "
            f"{n_pq_subs} PYQ subtopics > {batch_slots} batch slots "
            f"({batch_size} mocks × {sec_qs} Qs/mock). "
            f"Cannot guarantee every subtopic appears once per {batch_size}-mock window. "
            f"Ref: EC-11 — options: (a) increase batch_size, "
            f"(b) reduce subtopic count, (c) increase sec_qs."
        )
    # ──────────────────────────────────────────────────────────────────────────

    # Subtopics classified in §3-5
    pq_subs = pyq_subtopics[section]          # r_avg > 0 — handled by §4
    # zero_pyq_subtopics[section] handled entirely by §5 — not allocated here

    # v1.13: PRE-FLIGHT MANDATE vs r_avg CHECK (runs after §3, before §4-2)
    # Catches mandate/ZP contradiction BEFORE quota computation.
    preflight_mandate_ravg_check(section['name'], pq_subs, zero_pyq_subtopics[section])

    # Initialize mock_alloc for ALL subtopics in section (PYQ + ZP)
    # so §5 can write ZP entries into mock_alloc without KeyError
    all_subs = pq_subs + zero_pyq_subtopics[section]
    mock_alloc = {S: [0] * (N + 1) for S in all_subs}   # 1-indexed; index 0 unused

    # Denominator for scaled average
    section_total_r_avg = sum(r_avg[S] for S in pq_subs)

    # Guard: all subtopics Zero-PYQ → section_total_r_avg = 0 → division by zero in S4-2
    if section_total_r_avg == 0:
        # Apply equal distribution (EC-3 in §16 for full procedure)
        _apply_equal_distribution(section, pq_subs, zero_pyq_subtopics[section],
                                  sec_qs, N, mock_alloc, zp_slot)
        continue   # skip S4-2 through S4-6 for this section; §5 ZP rotation already ran before §4
```

### S4-1b — BV-10 MECHANIC FEASIBILITY GATE (v1.24 — the no-deadlock guarantee)

```
WHY: BV-10 used to be discovered only at B2, after full allocation, as a HARD FAIL
whose remedy ("regenerate 3× then ask the user") could never terminate on a
DETERMINISTIC infeasibility. This gate moves the check UPSTREAM to B1 — exactly like
EC-11 does for Option-C coverage — and makes it EXHAUSTIVE, so a same-form collision
can never surface late as a deadlock again, on ANY of the 200 exams.

DECISION PROCEDURE (necessary AND sufficient):
  G1  pigeonhole screen : Σ present_S ≤ cap · N_w         (cheap reject)
  fast obstruction      : ≥cap members saturating all N_w AND more members  (cheap reject)
  G3  exact test        : bipartite b-matching / Hall's condition (authoritative);
                          consumes the PINNED positions (rare Phase-1, ZP rotation,
                          mandate-every-mock) that G1 alone can miss.
  present_S = min(quota_S, N_w) for free members (SAME formula B2 uses, §4-2 / L~1562);
              = |pinned_mocks ∩ window| for pinned members.

TWO TIERS (match Step 5 fields + Step 7 contract):
  • BV-10a HARD on form_key (fine identity), cap = 1 per collision_domain: fires ONLY
    when ≥2 DISTINCT subtopics share a form_key (true duplicates) — then HALT with a
    precise Step-5 fix. On clean Step-5 v2.24 data every subtopic owns its form_key,
    so this is satisfiable by construction (no false deadlock).
  • BV-10b SOFT on family (coarse), cap = max_per_mechanic_per_mock[family] (default 1):
    infeasibility here is a WARN (diversity steering), never a HALT — questions stay
    unique at the form_key level.

WHEN TO RUN: at B1, AFTER §4-2 quotas AND §4-4 rare positions AND §5 ZP rotation are
known (so pinned sets are exact), BEFORE B2 generation. Runs per collision_domain
across ALL sections and EVERY batch window (including a short final window when
N_mocks is not a multiple of batch_size). Reference implementation (unit-tested):
```

```python
# ── Step 6 BV-10 feasibility engine (reference implementation, unit-tested) ──
# Decision procedure: G1 pigeonhole screen -> fast obstruction -> G3 exact
# bipartite b-matching (Hall's condition via max-flow). Necessary AND sufficient.
import math
from collections import deque, defaultdict

def present_count(quota, N_w, pinned_mocks=None, window=None):
    """Appearances of a subtopic WITHIN a window. Free members: min(quota, N_w) (even-spread
    formula, same as B2). Pinned members (rare Phase-1 / ZP rotation / mandate-every-mock):
    |pinned_mocks ∩ window| — ONLY the pins that fall inside THIS window. A pin in another
    batch window does NOT appear here (fixes a false-HALT when a pin set spans windows)."""
    if pinned_mocks is not None:
        if window is not None:
            return len(set(pinned_mocks) & set(window))
        return min(len(pinned_mocks), N_w)          # window unknown → conservative
    return min(quota, N_w)

def _maxflow_feasible(members, window_mocks, cap):
    """G3: can every member's demanded appearances be placed into window_mocks,
    with <= cap members sharing any one mock? Max-flow; feasible iff flow==Σdemand.
    members: list of (demand:int, allowed:set(mock_ids)). window_mocks: iterable of ids."""
    total_demand = sum(d for d,_ in members)
    if total_demand == 0:
        return True
    # node ids: S=0, member i -> 1+i, mock -> 1+len(members)+idx, T=last
    M = len(members); mocks = list(window_mocks); mock_idx = {m:i for i,m in enumerate(mocks)}
    S = 0; T = 1 + M + len(mocks)
    N = T + 1
    cap_g = [defaultdict(int) for _ in range(N)]
    def add(u,v,c): cap_g[u][v]+=c
    for i,(d,allowed) in enumerate(members):
        add(S, 1+i, d)
        for mk in allowed:
            if mk in mock_idx:
                add(1+i, 1+M+mock_idx[mk], 1)   # a member occupies a mock at most once
    for mk in mocks:
        add(1+M+mock_idx[mk], T, cap)
    # Edmonds-Karp
    flow=0
    while True:
        parent={S:None}; q=deque([S])
        while q:
            u=q.popleft()
            for v,c in cap_g[u].items():
                if c>0 and v not in parent:
                    parent[v]=u
                    if v==T: q.clear(); break
                    q.append(v)
        if T not in parent: break
        # bottleneck
        v=T; b=math.inf
        while parent[v] is not None:
            u=parent[v]; b=min(b,cap_g[u][v]); v=u
        v=T
        while parent[v] is not None:
            u=parent[v]; cap_g[u][v]-=b; cap_g[v][u]+=b; v=u
        flow+=b
    return flow==total_demand

def _windows(N, batch_size):
    """List of mock-id windows: [1..bs],[bs+1..2bs],... last window may be short."""
    out=[]; start=1
    while start<=N:
        end=min(start+batch_size-1, N)
        out.append(list(range(start,end+1))); start=end+1
    return out

def check_group(members, window, cap):
    """G1 fast-screen then G3 exact for one (family|form_key) group in one window.
    members: list of dict(id, quota, pinned(optional set))."""
    present=[]
    for mta in members:
        p = present_count(mta['quota'], len(window), mta.get('pinned'), window)  # window-aware
        present.append(p)
    # G1 necessary screen
    if sum(present) > cap*len(window):
        return False, f"G1: Σpresent={sum(present)} > cap*N_w={cap*len(window)}"
    # G3 exact (handles pinned positions G1 can miss)
    flow_members=[]
    for mta,p in zip(members,present):
        allowed = set(mta['pinned']) & set(window) if mta.get('pinned') else set(window)
        flow_members.append((p, allowed))
    if not _maxflow_feasible(flow_members, window, cap):
        return False, "G3: no collision-free assignment (Hall's condition violated)"
    return True, "feasible"

def bv10_preflight(subs, N, batch_size=10, caps=None):
    """subs: list of dict(id, quota, form_key, family, collision_domain, pinned(optional)).
    Returns (halts, warns). HALT = HARD form_key infeasibility (true duplicates that
    cannot be separated). WARN = SOFT family-cap steering target not satisfiable.
    caps: {family: cap_M}; default 1."""
    caps = caps or {}
    halts=[]; warns=[]
    for window in _windows(N, batch_size):
        # group by (collision_domain, form_key) for HARD (cap fixed = 1)
        hard=defaultdict(list)
        for s in subs:
            hard[(s['collision_domain'], s['form_key'])].append(s)
        for (dom,fk),members in hard.items():
            if len(members) < 2:      # single subtopic per form_key -> never a hard dup
                continue
            ok,why = check_group(members, window, cap=1)
            if not ok:
                halts.append(f"BV-10a HARD infeasible [domain={dom} form_key={fk} "
                             f"window={window[0]}-{window[-1]}]: {sorted(m['id'] for m in members)} "
                             f"are the SAME fine form and cannot be separated ({why}). "
                             f"These are true duplicates: merge them, or split into distinct forms in Step 5.")
        # group by (collision_domain, family) for SOFT (cap = caps or 1)
        soft=defaultdict(list)
        for s in subs:
            soft[(s['collision_domain'], s['family'])].append(s)
        for (dom,fam),members in soft.items():
            if len(members) < 2:
                continue
            cap=caps.get(fam,1)
            ok,why = check_group(members, window, cap=cap)
            if not ok:
                warns.append(f"BV-10b SOFT cap not fully satisfiable [domain={dom} family={fam} "
                             f"cap={cap} window={window[0]}-{window[-1]}]: {why}. "
                             f"Diversity steering target; questions remain UNIQUE at form_key level. "
                             f"Raise max_per_mechanic_per_mock['{fam}'] to accept more per mock, "
                             f"or accept the audited soft-cap overage.")
    return halts, warns

# ── INVOCATION at B1 (after quotas + rare positions + ZP rotation are known) ──
# subs_meta: one dict per PYQ subtopic across ALL sections —
#   {id, quota, form_key, family, collision_domain, pinned(optional set of mock ids)}
#   form_key/family/collision_domain come from section_rules.md (Step 5 v2.24):
#     form_key         = read_field(S,'form_key')  or question_mechanic  (fine identity)
#     family           = read_field(S,'concept_group') or question_mechanic  (coarse)
#     collision_domain = read_field(S,'collision_domain') or section name
#   pinned = the exact mocks a rare/ZP/mandate-every-mock subtopic is fixed to.
# caps = blueprint.get('max_per_mechanic_per_mock', {})   # {family: int}, default 1
#
#   halts, warns = bv10_preflight(subs_meta, N_mocks, batch_size, caps)
#   for w in warns: print("BV-10b (soft): " + w)          # diversity-steering notes
#   if halts:                                             # STRUCTURAL — terminate now
#       raise AlgorithmError(
#           "BV-10a infeasible by construction — B1 HALT (no regeneration loop):\n"
#           + "\n".join(halts))
#
# GUARANTEE: if this gate passes, a collision-free schedule provably EXISTS (Hall's
# condition) and the allocator can realise it; if it fails, none exists and B1 stops
# with the exact offending members + the named upstream fix. There is no third
# outcome, so BV-10 can never again deadlock at B2/B3.
```

### S4-2 — Compute quota per subtopic (SA-3 + SA-16)

```python
# ── v1.13 STEP 0: MANDATE-FIRST QUOTA RESERVATION ────────────────────────────
# Before proportional r_avg split, compute the DETERMINISTIC mandate total for
# every M1/M4/M6 subtopic in this section and RESERVE those slots.
# This eliminates the quota-vs-mandate fight that previously caused 96+ F1 failures.
#
# WHY: If a subtopic is mandatory_every_mock (M1), it needs exactly N slots.
# If min_counts says k, it needs k*N. If mandatory_groups says min=g members
# per mock, each group needs g*N across its members. When the proportional split
# assigns fewer than this, the force-place loop at build time steals from others,
# cascading failures. Reserving upfront makes quota and mandates structurally
# compatible instead of adversarial.

# Identify mandated subtopics in THIS section (resolve ids → display names)
section_mandate_ids = {}   # id -> deterministic total needed
for sid in MANDATORY_IDS:
    if sid in MANIFEST_IDS and MANIFEST_IDS[sid].get('section') == section['name']:
        # M1: must appear every mock → exactly N slots minimum
        section_mandate_ids[sid] = N

for sid, k in MIN_COUNTS.items():
    if sid in MANIFEST_IDS and MANIFEST_IDS[sid].get('section') == section['name']:
        # M6: must have ≥k per mock → exactly k*N slots minimum
        section_mandate_ids[sid] = max(section_mandate_ids.get(sid, 0), k * N)

for gname, gdata in MANDATORY_GROUPS.items():
    group_min = gdata.get('min', 1)
    group_members_in_section = [
        mid for mid in gdata.get('members', [])
        if mid in MANIFEST_IDS and MANIFEST_IDS[mid].get('section') == section['name']
    ]
    if group_members_in_section:
        # M4: ≥ group_min members per mock → distribute group_min*N across members
        # Each member gets at least (group_min * N) // len(group_members_in_section)
        # with remainder distributed by r_avg descending
        per_member_base = (group_min * N) // len(group_members_in_section)
        remainder_slots = (group_min * N) % len(group_members_in_section)
        members_by_ravg = sorted(group_members_in_section,
                                  key=lambda mid: r_avg.get(
                                      MANIFEST_IDS[mid]['display_name'], 0),
                                  reverse=True)
        for idx, mid in enumerate(members_by_ravg):
            needed = per_member_base + (1 if idx < remainder_slots else 0)
            section_mandate_ids[mid] = max(section_mandate_ids.get(mid, 0), needed)

# Map mandate ids back to display names used in pq_subs
mandate_reserved = {}   # display_name -> reserved total
for sid, total_needed in section_mandate_ids.items():
    dn = MANIFEST_IDS[sid]['display_name']
    if dn in pq_subs:   # only reserve for PYQ subtopics (ZP subtopics handled by §5)
        mandate_reserved[dn] = total_needed

# Partition: mandated vs non-mandated PYQ subtopics
mandated_subs     = [S for S in pq_subs if S in mandate_reserved]
non_mandated_subs = [S for S in pq_subs if S not in mandate_reserved]

# ── STEP 1: compute exact target total ────────────────────────────────────────
# ZP rotation takes 1 slot per mock where active → subtract from target
# zp_slot[section][m] is computed by §5 BEFORE §4 runs (§8-2 Step 5 before Step 6)
total_zp_slots = sum(zp_slot[section][m] for m in range(1, N + 1))
target_total   = sec_qs * N - total_zp_slots

# ── STEP 2: reserve mandate slots, set mandated quota, compute remaining budget ──
# Set quota for mandated subtopics FIRST (at least their mandate, at least n_batches)
quota = {}
for S in mandated_subs:
    quota[S] = max(mandate_reserved[S], n_batches)

# IMPORTANT (v1.13): remaining_budget uses the ACTUAL quota assigned to mandated
# subs (which includes the n_batches floor), not just mandate_reserved totals.
# If n_batches > mandate_reserved for any sub, its quota is higher than reserved,
# and remaining_budget must reflect that — otherwise the deficit adjustment inherits
# a systematic over-allocation that causes negative deficit.
actual_mandated_total = sum(quota[S] for S in mandated_subs)
remaining_budget = target_total - actual_mandated_total

if remaining_budget < 0:
    raise AlgorithmError(
        f"Section {section['name']}: mandated subtopic quotas ({actual_mandated_total}) exceed "
        f"target_total ({target_total}). Too many mandatory subtopics for available slots. "
        f"Reduce mandates or increase sec_qs.")

# ── STEP 3: proportional r_avg split on remaining subtopics ───────────────────
# Remaining subtopics share the remaining_budget proportionally by r_avg.
# ENGINE: bc.proportional_split returns (pool_quota, pool_raw_total) for the
# non-mandated pool (each ≥ n_batches; equal split when the pool's r_avg sums to 0).
# Mandated quota was already set in STEP 2; merge the pool results in. STEP 3b below
# adds mandated raw_total so the map covers all pq_subs before the deficit fix.
# (Identical to the prior inlined split — verified vs it over 20k random inputs.)
import blueprint_core as bc
raw_total = {}
_pool_quota, _pool_raw = bc.proportional_split(
    non_mandated_subs, r_avg, remaining_budget, N, n_batches)
quota.update(_pool_quota)
raw_total.update(_pool_raw)

# Also compute raw_total for mandated subs (for the largest-remainder adjustment)
for S in mandated_subs:
    if section_total_r_avg > 0:
        raw_total[S] = (r_avg[S] / section_total_r_avg) * sec_qs * N
    else:
        raw_total[S] = float(quota[S])

# ── STEP 4: deficit adjustment (largest-remainder) ────────────────────────────
# ENGINE: bc.largest_remainder_fix adjusts `quota` IN PLACE to hit target_total
# EXACTLY. deficit ≥ 0 → +1 to the highest fractional remainders (tie-break r_avg
# desc); deficit < 0 → trim the smallest remainders, looping, NEVER below
# max(n_batches, mandate floor). floors=mandate_reserved carries the per-subtopic
# mandate floor (SA-16 + v1.13). It raises bc.AllocationError when the target is
# unreachable (all subtopics at floor); we re-wrap that into the spec's AlgorithmError
# with the section name + EC-11 pointer, preserving the original error contract.
# (Identical to the prior inlined deficit loop — verified vs it over 20k random inputs.)
try:
    bc.largest_remainder_fix(quota, pq_subs, raw_total, r_avg,
                             target_total, n_batches, floors=mandate_reserved)
except bc.AllocationError as _e:
    raise AlgorithmError(
        f"Section {section['name']}: {_e} "
        f"Ref: EC-11 feasibility check — should have caught this.")

assert sum(quota.values()) == target_total, (
    f"Quota sum {sum(quota.values())} != target {target_total} — algorithm error"
)
```

### S4-3 — Rare vs non-rare classification (SA-5)

```python
# Rare threshold: configurable via blueprint.json rare_threshold field.
# Default: 0.1 (subtopic appeared in fewer than 1-in-10 papers on average).
# Exams with very few papers (e.g. 5 total) may need a lower threshold
# to avoid classifying most subtopics as rare. Exams with 500+ papers
# may want a higher threshold. Override: set rare_threshold in exam_config.json
# or pass through blueprint.json.
RARE_THRESHOLD = float(bp.get('rare_threshold', 0.1))

# Phase 1 pre-schedules rare subtopics to ensure they are spread across the series,
# not clustered at the end (SA-8).
# Note: for large N_mocks, rare subtopics can accumulate large quotas (> 5).
# The rare/non-rare distinction is about r_avg frequency, not quota magnitude.

rare_subs    = [S for S in pq_subs if r_avg[S] < RARE_THRESHOLD]
nonrare_subs = [S for S in pq_subs if r_avg[S] >= RARE_THRESHOLD]
# Store for §9 BV checks
rare_subs_by_section[section]    = rare_subs
nonrare_subs_by_section[section] = nonrare_subs
```

### S4-4 — Phase 1: Pre-schedule rare subtopics

```python
# Phase 1 must run BEFORE Phase 2.
# Phase 1 assigns exact mock positions to rare subtopics (1 Q per position).
# Phase 2 may NOT displace any Phase 1 assignment.
#
# BATCH COVERAGE FOR RARE SUBTOPICS:
#   Every rare subtopic must appear in EVERY batch window (Option C).
#   Since quota[S] >= n_batches (enforced in §4-2), and positions are staggered
#   evenly across the series, the stagger formula naturally places at least one
#   appearance in each batch window IF quota[S] >= n_batches.
#   
#   After computing stagger positions, run batch-coverage validation:
#   For each batch window [b_start..b_end]: at least one position must fall inside.
#   If any window is uncovered → inject one additional position in that window
#   (at the window midpoint), and log a warning.

rare_positions = {}   # S → list of mock indices (1-indexed) where S appears

for S in rare_subs:
    # Cap quota at N: subtopic cannot appear more times than there are mocks
    q = min(quota[S], N)
    if q < quota[S]:
        warn(f"Phase 1: {S} quota={quota[S]} > N_mocks={N}. Capping at {N}.")

    positions = []

    # Stagger positions evenly across series (SA-8: no end-clustering)
    for k in range(q):
        pos = int((k + 0.5) * N / q) + 1   # 1-indexed mock number
        pos = min(pos, N)
        positions.append(pos)

    # Resolve conflicts: max MAX_RARE_PER_MOCK rare Qs per mock per section (SA-7)
    for idx, pos in enumerate(positions):
        rare_count_at_pos = sum(
            1 for T in rare_subs if T != S and pos in rare_positions.get(T, [])
        )
        max_attempts = N
        attempts     = 0
        while rare_count_at_pos >= MAX_RARE_PER_MOCK and attempts < max_attempts:
            pos = (pos % N) + 1     # advance cyclically within [1..N]
            rare_count_at_pos = sum(
                1 for T in rare_subs if T != S and pos in rare_positions.get(T, [])
            )
            attempts += 1
        if attempts >= max_attempts:
            warn(f"Phase 1: No conflict-free position for {S} appearance {idx+1}. "
                 f"Placing at mock {pos} (rare count there = {rare_count_at_pos}).")
        positions[idx] = pos

    # BATCH COVERAGE VALIDATION for this rare subtopic (Option C)
    # Every batch window must have at least one position
    for b in range(n_batches):
        b_start = b * batch_size + 1
        b_end   = min(b_start + batch_size - 1, N)
        covered = any(b_start <= p <= b_end for p in positions)
        if not covered:
            # Inject at window midpoint — guard against duplicate position
            midpoint = (b_start + b_end) // 2
            if midpoint not in positions:   # prevent double-counting
                positions.append(midpoint)
            warn(f"Phase 1: '{S}' had no appearance in batch window "
                 f"{b+1} (mocks {b_start}-{b_end}). "
                 f"Injecting at mock {midpoint}. "
                 f"Total appearances now = {len(positions)} (was {q}).")

    rare_positions[S] = positions
    for pos in positions:
        mock_alloc[S][pos] += 1   # += not = : handles rare case of same pos appearing twice
```

### S4-5 — Phase 2: Even-spread allocation for non-rare subtopics

```python
# Phase 2 fills remaining slots after Phase 1 assignments and ZP reservation.
#
# v1.13: THE ONLY SANCTIONED METHOD IS PRE-SCHEDULED EVEN SPREAD.
# The urgency loop is DEPRECATED (see end of this section for rationale).
# Even spread guarantees variance ≤ 1 by construction; the urgency loop does not.
#
# ─────────────────────────────────────────────────────────────────────────────
# PHASE 0 — BATCH COVERAGE PRE-PASS (runs BEFORE even spread, Option C)
# ─────────────────────────────────────────────────────────────────────────────
# Before even-spread, guarantee every nonrare subtopic appears ≥ 1 Q in every
# batch window.
#
# v1.13 FIX: MULTI-MOCK SPREAD — forced assignments are distributed across ALL
# mocks in the window (working backward from b_end), using each mock's remaining
# capacity, instead of dumping all uncovered subtopics into mock b_end.
#
# WHY SINGLE-MOCK FORCING FAILS (worked example):
#   SSC CGL Tier 1, GIR section: 56 nonrare subtopics, sec_qs = 25.
#   If all 56 are uncovered in a batch window and forced into b_end:
#   → 56 placements into 25 slots → overflow = 31. The overflow correction loop
#   can only reduce OTHER nonrare subs at b_end, but there aren't enough.
#   AlgorithmError fires at S4-6 column-fix (diff > ±5 guard).
#
# CORRECTED ALGORITHM per batch window [b_start..b_end]:
#   1. Identify nonrare subtopics not yet scheduled in this window:
#        uncovered = [S for S in nonrare_subs if sum(mock_alloc[S][m]
#                     for m in range(b_start, b_end+1)) == 0
#                     and assigned.get(S, 0) < quota[S]]
#   2. Sort uncovered by r_avg descending (deterministic — highest priority first)
#   3. Spread forced assignments backward from b_end to b_start:
#        For each mock m from b_end down to b_start:
#          Compute remaining capacity at mock m (sec_qs minus what's already placed)
#          Assign uncovered subtopics (1 Q each) into available capacity
#          Stop when all uncovered are assigned or capacity exhausted at this mock
#        Move to next mock inward if uncovered subtopics remain.
#   4. If uncovered remain after all mocks exhausted → warn (should not happen if
#      feasibility pre-check passed, since batch_slots >= n_pq_subs in §4-1).
#
# This pass runs ONCE per batch window, before even-spread processes the window.
# Because quota[S] >= n_batches for all S (§4-2), every subtopic has enough
# quota to absorb one forced appearance per batch.
#
# ─────────────────────────────────────────────────────────────────────────────
# PER-MOCK CAP (SA-14 — even-spread rule):
#   per_mock_cap[S] = math.ceil(quota[S] / N)
#   No subtopic may receive more than per_mock_cap[S] Qs in any single mock.
#   This guarantees max variance ≤ 1 across all mocks for every subtopic:
#     every subtopic gets exactly floor(quota/N) or floor(quota/N)+1 per mock.
#
# ─────────────────────────────────────────────────────────────────────────────
# SANCTIONED IMPLEMENTATION — pre-schedule even spread (ONLY method, v1.13):
#   For each nonrare subtopic S with quota[S]:
#     floor_v = quota[S] // N
#     n_high  = quota[S] %  N          # number of mocks that get floor_v + 1
#     Step 1: set mock_alloc[S][m] = floor_v for all m in 1..N
#     Step 2: distribute n_high extras to n_high evenly-spaced mocks:
#               # v1.13: subtopic_offset prevents position collisions between
#               # subtopics with the same n_high value.
#               subtopic_offset = subtopic_index / len(nonrare_subs)
#               for i in range(n_high):
#                   pos = int((i + 0.5 + subtopic_offset) * N / n_high) + 1
#                   pos = min(pos, N)   # clamp to valid range
#                   mock_alloc[S][pos] += 1
#
#   v1.13 NOTE ON POSITION FORMULA DECORRELATION:
#     Without subtopic_offset, the formula pos = int((i+0.5)*N/n_high)+1 depends
#     ONLY on n_high. Any two subtopics sharing the same n_high value compute the
#     EXACT SAME set of positions → systematic collisions → column-fix overloaded.
#     subtopic_offset is derived from the subtopic's index in the sorted nonrare
#     list, producing a unique phase shift per subtopic. This spreads extras across
#     distinct mocks even when n_high values coincide.
#
#   Then run a column-balance pass (see S4-6) to satisfy column sums exactly.
#   This is deterministic and guarantees variance ≤ 1 by construction.
#   NOTE: Phase 0 batch-coverage pre-pass runs first to inject forced appearances —
#   then the even-spread pass distributes the remaining quota across all mocks.
#   Column-balance corrects any overage from forced injections.

assigned = {S: 0 for S in nonrare_subs}   # cumulative Qs assigned so far

# ── PHASE 0: Batch coverage pre-pass (v1.13: MULTI-MOCK SPREAD) ──────────────
for b in range(n_batches):
    b_start = b * batch_size + 1
    b_end   = min(b_start + batch_size - 1, N)

    uncovered = sorted(
        [S for S in nonrare_subs
         if sum(mock_alloc[S][m] for m in range(b_start, b_end + 1)) == 0
         and assigned.get(S, 0) < quota[S]],
        key=lambda S: -r_avg[S]   # highest r_avg first (deterministic)
    )

    if not uncovered:
        continue

    # v1.13: Spread across all mocks in window, working BACKWARD from b_end
    uncovered_remaining = list(uncovered)
    for m in range(b_end, b_start - 1, -1):   # b_end → b_start
        if not uncovered_remaining:
            break

        # Compute remaining capacity at mock m
        phase1_at_m  = sum(mock_alloc[S][m] for S in rare_subs)
        zp_at_m      = zp_slot[section].get(m, 0)
        nonrare_at_m = sum(mock_alloc[S][m] for S in nonrare_subs)
        capacity     = sec_qs - phase1_at_m - zp_at_m - nonrare_at_m

        placed_this_mock = 0
        still_uncovered  = []
        for S in uncovered_remaining:
            if placed_this_mock < capacity:
                mock_alloc[S][m] += 1
                assigned[S]      += 1
                placed_this_mock += 1
            else:
                still_uncovered.append(S)
        uncovered_remaining = still_uncovered

    if uncovered_remaining:
        warn(f"Phase 0: Could not place {len(uncovered_remaining)} uncovered subtopics "
             f"in batch window {b+1} (mocks {b_start}-{b_end}), section {section['name']}. "
             f"This should not happen if feasibility pre-check (§4-1) passed. "
             f"Column-fix will attempt correction.")

# ── EVEN-SPREAD ALLOCATION (Phase 2 — ONLY sanctioned method, v1.13) ─────────
# Compute per-mock caps before the spread
per_mock_cap = {S: math.ceil(quota[S] / N) for S in nonrare_subs}

# Sort nonrare_subs deterministically for stable subtopic_offset
sorted_nonrare = sorted(nonrare_subs, key=lambda S: (r_avg[S], S), reverse=True)

for sub_idx, S in enumerate(sorted_nonrare):
    remaining_quota = quota[S] - assigned[S]
    if remaining_quota <= 0:
        continue

    floor_v = remaining_quota // N
    n_high  = remaining_quota %  N   # number of mocks that get floor_v + 1

    # Step 1: set base allocation
    for m in range(1, N + 1):
        mock_alloc[S][m] += floor_v
    assigned[S] += floor_v * N

    # Step 2: distribute n_high extras with per-subtopic decorrelation
    # v1.13: enforce per_mock_cap — if target pos already at cap (e.g. from Phase 0),
    # shift forward cyclically to find a mock with capacity. This prevents variance > 1
    # when Phase 0 placements collide with even-spread extras.
    if n_high > 0:
        subtopic_offset = sub_idx / len(sorted_nonrare)
        for i in range(n_high):
            pos = int((i + 0.5 + subtopic_offset) * N / n_high) + 1
            pos = min(pos, N)   # clamp to valid mock range
            # per_mock_cap enforcement: if pos already at cap, scan for available mock
            if mock_alloc[S][pos] >= per_mock_cap[S]:
                found = False
                for offset in range(1, N):
                    alt = ((pos - 1 + offset) % N) + 1   # cyclical scan [1..N]
                    if mock_alloc[S][alt] < per_mock_cap[S]:
                        pos = alt
                        found = True
                        break
                if not found:
                    # All mocks at cap — should not happen if quota <= per_mock_cap * N
                    warn(f"Even-spread: {S} all mocks at per_mock_cap={per_mock_cap[S]}. "
                         f"Placing extra at original pos={pos}. Column-fix will correct.")
            mock_alloc[S][pos] += 1
            assigned[S]        += 1

# ── DEPRECATED: URGENCY LOOP ─────────────────────────────────────────────────
# The urgency loop below is DEPRECATED as of v1.13. DO NOT USE.
# Rationale: the urgency-based greedy fill does NOT guarantee variance ≤ 1 in
# practice. Empirically proven: GA (General Awareness) section broke with
# variance > 1 and zero mandate involvement — purely an urgency-loop artefact.
# The pre-scheduled even spread above guarantees variance ≤ 1 by construction.
# This code is retained for reference ONLY — it must NEVER be executed.
#
# ## DEPRECATED_URGENCY_LOOP (do not use)
# for m in range(1, N + 1):
#     phase1_qs       = sum(mock_alloc[S][m] for S in rare_subs)
#     zp_qs           = zp_slot[section][m]
#     nonrare_already = sum(mock_alloc[S][m] for S in nonrare_subs)
#     available       = max(0, sec_qs - phase1_qs - zp_qs - nonrare_already)
#     remaining_mocks = N - m + 1
#     slots_left      = available
#     while slots_left > 0:
#         candidates = [
#             (S, (quota[S] - assigned[S]) / remaining_mocks)
#             for S in nonrare_subs
#             if quota[S] - assigned[S] > 0
#             and mock_alloc[S][m] < per_mock_cap[S]
#         ]
#         if not candidates:
#             break
#         best_S = max(candidates, key=lambda x: (x[1], r_avg[x[0]]))[0]
#         mock_alloc[best_S][m] += 1
#         assigned[best_S]      += 1
#         slots_left            -= 1
```

### S4-5b — EXACT MATRIX FILL for non-rare subtopics (SANCTIONED v1.25 — 0% F1 drift)

```
WHY (register D3-14 / gap-analysis §12): the Phase-0 backward-forcing (§4-5) + naive
column-fix (§4-6) do NOT preserve per-subtopic quota. Phase-0 over-concentrates
uncovered subtopics into the last mock when a section has a single window (n_batches=1,
N≤10, nonrare_at_m=0 during the pass), and the column-fix then adds to the LOWEST- and
removes from the HIGHEST-allocated subtopic — inflating low-quota subtopics and shaving
high-quota ones. Column sums (BV-1) still pass (totals conserved), so the drift is
invisible at B2 and only fails at B3 BV-7 F1/F5 — after all mocks are built. In the SSC
CGL run this drifted 30 of 59 subtopics outside F1 tolerance.

FIX: after Phase 1 (rare) and ZP are placed at their fixed positions, fill the FREE
(non-rare) subtopics with an EXACT MATRIX FILL that meets every per-subtopic quota AND
every per-mock free capacity EXACTLY, with per-cell values in {floor(q/N), ceil(q/N)}
(variance ≤ 1). This supersedes Phase-0 forcing + the naive column-fix for row accuracy:
  • F1  : row sum == quota_S exactly → 0% drift for every tier (>20 / 5–20 / 1–4).
  • BV-1: column sum == sec_qs − rare_at_m − zp_at_m exactly (no ±5 correction needed).
  • F5  : variance ≤ 1 by construction.
  • BV-9B: every free subtopic with quota ≥ 1 appears ≥ 1 in the window.

HOW TO WIRE IT (per section, per batch window):
  1. Place Phase-1 rare positions (§4-4) and ZP rotation (§5) FIRST.
  2. col_targets[m] = sec_qs − rare_at_m − zp_at_m − mandatory_forced_at_m   (free capacity)
  3. quotas[S]      = the window quota for each FREE subtopic (SAME formula B2 uses).
     (Feasibility: Σ quotas == Σ col_targets — guaranteed by §4-2 quota computation, and
      re-checked below; if it ever fails, HALT here with the exact numbers — do NOT paper
      over it with column-fix.)
  4. alloc = exact_fill(quotas, col_targets); write alloc[S][m] into mock_alloc.
  5. §4-6 column-fix now runs only as a NO-OP INVARIANT CHECK (diff must be 0); a nonzero
     diff here is a real bug, not a routine correction.

REFERENCE IMPLEMENTATION (unit-tested: SSC single-window, non-uniform columns, multi-
window, 100 random instances, determinism, feasibility guard):
```

```python
# Exact-matrix allocator (v1.25) — replaces Phase-0 forcing + naive column-fix.
# Guarantees, BY CONSTRUCTION, for the FREE (nonrare) subtopics in one batch window:
#   F1  : row sum == quota_S exactly (0% drift, BV-7 F1 passes for any tier)
#   BV-1: column sum == per-mock free capacity exactly
#   F5  : per-cell ∈ {floor(q/N), ceil(q/N)} → variance ≤ 1 per subtopic
#   BV-9B: every subtopic with quota ≥ 1 appears ≥ 1 in the window
# Rare (Phase-1) and ZP are placed FIRST at fixed positions; col_target already excludes them.
import blueprint_core as bc   # ENGINE (mandated in S1-2b)

# exact_fill is provided by the shared engine (single source of truth). The ~50-line
# Gale-Ryser body formerly inlined here now lives in blueprint_core.py; aliased so the
# §4-5b/§8-3 wiring call `alloc = exact_fill(quotas, col_targets)` stays unchanged.
# bc.exact_fill is byte-identical to the removed body (same margins/variance/determinism
# guarantees, same ValueError paths — verified vs the removed loop over 20k random inputs).
exact_fill = bc.exact_fill

# ── Even-spread guarantee: exact_fill puts each subtopic's quota%N "+1"s in DISTINCT
#    mocks (chosen by the Gale-Ryser most-remaining-first rule), so every row is
#    floor/ceil only (F5 variance ≤ 1) while both margins stay exact (F1 + BV-1).
#    Multi-window: call exact_fill ONCE PER WINDOW with that window's quotas/col_targets;
#    rare/ZP pins are already excluded from col_targets so cross-window coverage is
#    preserved. This is deterministic — identical output on re-run (no re-drift, D3-6).
```

### S4-6 — Column-fix (SA-9 + SA-13)

```python
# After Phase 1 + Phase 2: column sum must equal sec_qs EXACTLY.
# v1.25 SUPERSEDE: when §4-5b EXACT MATRIX FILL is used (SANCTIONED), column sums are
# already exact and per-subtopic quotas are preserved — column-fix then runs ONLY as a
# NO-OP INVARIANT CHECK (any nonzero diff is a real bug, not a routine correction; the
# old "add to lowest / remove from highest" drift path must NOT be taken because it breaks
# per-subtopic quota → BV-7 F1). Retained below for legacy/verification and for sections
# still on the pre-v1.25 path.
# Column-fix is a small correction step — NOT the primary allocation.
# Prefers adjusting nonrare_subs; falls back to rare_subs if nonrare is empty.

for m in range(1, N + 1):
    col_sum = sum(mock_alloc[S][m] for S in pq_subs) + zp_slot[section][m]
    diff    = sec_qs - col_sum    # positive = underallocated; negative = overallocated

    if diff == 0:
        continue

    if abs(diff) > 5:
        raise AlgorithmError(
            f"Column-fix mock {m} section {section['name']}: diff={diff} exceeds ±5. "
            f"Phase 2 algorithm error."
        )
    if abs(diff) > 2:
        warn(f"Column-fix diff={diff} for mock {m}, section {section['name']}.")

    # Adjustment pool: non-rare preferred; fall back to rare if non-rare is empty
    adj_pool   = nonrare_subs if nonrare_subs else rare_subs
    candidates = sorted(adj_pool,
                        key=lambda S: mock_alloc[S][m],
                        reverse=(diff < 0))   # highest first if removing

    applied = 0
    for S in candidates:
        if applied == abs(diff):
            break
        if diff > 0:
            mock_alloc[S][m] += 1
            applied += 1
        elif diff < 0 and mock_alloc[S][m] > 0:   # never go negative (SA-10)
            mock_alloc[S][m] -= 1
            applied += 1

    if applied < abs(diff):
        raise AlgorithmError(
            f"Column-fix could not fully correct mock {m} section {section['name']}: "
            f"applied {applied} of needed {abs(diff)}."
        )

    new_sum = sum(mock_alloc[S][m] for S in pq_subs) + zp_slot[section][m]
    assert new_sum == sec_qs, (
        f"Column-fix failed mock {m} section {section['name']}: sum={new_sum}, expected={sec_qs}"
    )
```

### S4-7 — Frequency accuracy check (SA-12)

```
NOTE: This check runs in B3 ONLY as part of BV-7 F1 (§9-7).
In B2, only BV-3 (warning-level) runs. The code below is the BV-7 F1 implementation.
```

```python
for S in pq_subs:
    actual_total = sum(mock_alloc[S][m] for m in range(1, N + 1))
    target       = quota[S]   # quota[S] >= n_batches >= 1 always — no division by zero

    if target > 20:
        tolerance, tier = 2.0,  1
    elif target >= 5:
        tolerance, tier = 15.0, 2
    else:
        tolerance, tier = 25.0, 3

    pct_error = abs(actual_total - target) / target * 100
    if pct_error > tolerance:
        raise ValidationError(
            f"BV-7 F1 FAIL [{section['name']}] {S}: "
            f"actual={actual_total}, quota={target}, "
            f"error={pct_error:.1f}% > {tolerance}% (Tier {tier})"
        )
```

### S4-8 — Algorithm invariants (must hold at all times)

```
INVARIANT 1 — Column sum (SA-9):
  For every mock m and every section:
  Σ mock_alloc[S][m] for S in pq_subs + zp_slot[section][m] == sec_qs
  Checked by column-fix (S4-6) and BV-1 (§9).

INVARIANT 2 — No negative (SA-10):
  mock_alloc[S][m] >= 0 for all S in all_subs, all m in 1..N.

INVARIANT 3 — Every non-zero PYQ subtopic appears at least once (SA-4):
  Σ mock_alloc[S][m] for m in 1..N >= 1 for all S where r_avg[S] > 0.
  Superseded in practice by INVARIANT 8 (n_batches >= 1 always).

INVARIANT 4 — Max rare Qs per mock per section (SA-7):
  MAX_RARE_PER_MOCK = int(bp.get('max_rare_per_mock', 2))   # configurable; default 2
  Σ mock_alloc[S][m] for S in rare_subs <= MAX_RARE_PER_MOCK for every mock m.
  For sections with many rare subtopics relative to sec_qs, increase this value.
  For small sections (sec_qs ≤ 5), consider reducing to 1.

INVARIANT 5 — Quota sum matches target (SA-3):
  Σ quota[S] for S in pq_subs == sec_qs × N − total_zp_slots
  where total_zp_slots = Σ zp_slot[section][m] for m in 1..N.

INVARIANT 6 — Budget-neutral column fix (SA-13):
  Column-fix only redistributes within a single mock column.
  Σ mock_alloc[S][m] across all S and all m is unchanged by fix.

INVARIANT 7 — Even spread / per-mock cap (SA-14):
  For every nonrare subtopic S in every section:
    mock_alloc[S][m] ≤ math.ceil(quota[S] / N)  for all m in 1..N.
  Equivalently: max(mock_alloc[S][m]) - min(mock_alloc[S][m]) ≤ 1  across all mocks.
  This guarantees every subtopic is distributed evenly — no front-loading.
  Checked by BV-7 F5 (§9-7) in B3.
  Violation example (WRONG):   India Current Affairs quota=23, N=10 → M1 gets 12Q, M10 gets 0Q.
  Correct behavior:             quota=23, N=10 → 3 mocks get 3Q, 7 mocks get 2Q (variance=1).
  NOTE: Phase 0 forced injections may create local variance = 1 at specific mocks
  for low-quota subtopics. This is permitted and expected with Option C active.

INVARIANT 8 — Batch coverage (Option C):
  For every PYQ subtopic S (r_avg > 0) and every batch window b:
    Σ mock_alloc[S][m] for m in [b_start..b_end] >= 1
  where b_start = b × batch_size + 1, b_end = min(b_start + batch_size - 1, N).
  Checked by BV-9B per B2 batch (§9).
  Guaranteed by:
    quota[S] >= n_batches (§4-2)  → enough quota for one per batch
    Phase 1 batch-coverage validation (§4-4) → rare subtopics covered
    Phase 0 batch-coverage pre-pass (§4-5) → nonrare subtopics covered
```

## §5 — ZERO-PYQ ROTATION

Handles subtopics that never appeared in any PYQ year (r_avg = 0).
These are rotated through the mock series so every zero-PYQ subtopic appears
a controlled number of times — no more, no less.

§5 MUST run BEFORE §4 so that zp_slot[section][m] is available to §4.

# ValidationError = ValueError   (defined in §4 — available globally)
# N = N_mocks                    (use N_mocks consistently throughout §5)

### S5-0 — Global initialisation (run once before section loop)

```python
# Initialise global containers before iterating over sections
zero_pyq_rotation   = {}              # section → alphabetical ZP list (for blueprint.json)
zp_slot             = {section: {} for section in sections}  # zp_slot[section][m] = 0 or 1
MAX_ZERO_by_section = {}              # section → MAX_ZERO scalar (for BV-5, BV-8)
```

### S5-1 — MAX_ZERO calculation (ZP-3)

```python
zero_pyq_list = zero_pyq_subtopics[section]   # from §3-5
zero_count    = len(zero_pyq_list)

if zero_count == 0:
    # No ZP subtopics in this section — all-PYQ section (ZP-9)
    zp_active                    = False
    MAX_ZERO                     = 0
    zero_pyq_rotation[section]   = []
    zp_slot[section]             = {m: 0 for m in range(1, N_mocks + 1)}
    MAX_ZERO_by_section[section] = 0   # BUG fix: must set for BV-5 and BV-8 KeyError guard
    # §4 can now safely access zp_slot[section][m] = 0 for all m
    # Skip S5-2 through S5-4 for this section
else:
    zp_active = True

    # Step 1: 10% rule
    MAX_ZERO = math.floor(N_mocks * 0.10)

    # Step 2: overflow protection
    if zero_count * MAX_ZERO > N_mocks:
        MAX_ZERO = math.floor(N_mocks / zero_count)

    # Step 3: extreme case — more ZP subtopics than mocks
    if N_mocks < zero_count:
        MAX_ZERO = 1   # first N_mocks subtopics (alphabetical) get 1 appearance each
                       # remaining get 0 appearances (handled in S5-2)

    # Step 4: if MAX_ZERO = 0 after all steps (e.g., N_mocks = 1, zero_count = 1)
    # → no ZP Q fits in any mock; treat section as ZP-inactive
    if MAX_ZERO == 0:
        zp_active                  = False
        zero_pyq_rotation[section] = []
        zp_slot[section]           = {m: 0 for m in range(1, N_mocks + 1)}
        note(f"Section {section['name']}: {zero_count} ZP subtopic(s) but MAX_ZERO=0 "
             f"(N_mocks={N_mocks} too small for 10% rule). No ZP Qs in any mock.")
    else:
        # Document in Paper Structure sheet
        n_active = min(zero_count, N_mocks)   # subtopics that actually get appearances
        note(f"Section {section['name']}: {zero_count} ZP subtopics. "
             f"MAX_ZERO = {MAX_ZERO}. "
             f"First {n_active} (alphabetical) appear {MAX_ZERO} time(s) each; "
             f"remaining {zero_count - n_active} appear 0 times.")
    # Store for §9 BV-5 and BV-8
    MAX_ZERO_by_section[section] = MAX_ZERO
```

### S5-2 — Alphabetical sort + rotation schedule (ZP-4 + ZP-11)

```python
# Skip this subsection if not zp_active (handled in S5-1)

# Sort ZP subtopics alphabetically (English A-Z, case-insensitive)
# Sort applied once; same order used throughout series and stored in blueprint.json
zero_pyq_sorted = sorted(zero_pyq_list, key=lambda S: S.lower())
zero_pyq_rotation[section] = zero_pyq_sorted   # store in blueprint.json field

# Build rotation schedule: mock_number → ZP subtopic (or None)
zp_rotation_schedule = {}
appearance_count     = {S: 0 for S in zero_pyq_sorted}
rotation_idx         = 0

for m in range(1, N_mocks + 1):
    slot_filled = False

    for _ in range(zero_count):
        S = zero_pyq_sorted[rotation_idx % zero_count]

        # Extreme case: skip subtopics beyond first N_mocks in alphabetical order
        if N_mocks < zero_count and zero_pyq_sorted.index(S) >= N_mocks:
            rotation_idx += 1
            continue

        if appearance_count[S] < MAX_ZERO:
            zp_rotation_schedule[m] = S
            appearance_count[S]    += 1
            rotation_idx           += 1
            slot_filled             = True
            break

        rotation_idx += 1   # this subtopic exhausted — advance to next

    if not slot_filled:
        zp_rotation_schedule[m] = None   # ZP cycle complete; mock is 100% PYQ-based

# Build zp_slot[section] as 2D (consistent with §4 access pattern)
zp_slot[section] = {
    m: (1 if zp_rotation_schedule[m] is not None else 0)
    for m in range(1, N_mocks + 1)
}
```

### S5-3 — Write ZP entries to mock_alloc and verify column sum (ZP-7)

```python
# For each mock with a ZP Q: write 1 to mock_alloc for the scheduled ZP subtopic.
# This happens BEFORE §4 runs — §4 then fills remaining slots in Phase 2.
# Column sum invariant: Σ PYQ Qs + zp_slot[section][m] == sec_qs (enforced by §4 column-fix)

for m in range(1, N_mocks + 1):
    if zp_slot[section][m] == 1:
        zp_sub = zp_rotation_schedule[m]
        mock_alloc[zp_sub][m] = 1   # ZP sub is in mock_alloc (initialised in §4-1)

# Rules:
# NEVER schedule more than 1 ZP Q per mock per section (enforced by rotation loop above).
# NEVER take ZP slot from a rare subtopic (r_avg < RARE_THRESHOLD) — ZP is tracked separately.
# ZP cost reduces Phase 2 available slots by 1 (max(0, sec_qs - phase1_qs - zp_qs) in §4-5).
```

### S5-4 — Verification (runs as BV-8 in B3 — not immediately after S5-3)

```
NOTE: S5-4 verification can only run AFTER §4 allocation is fully complete
(§4 writes PYQ entries into mock_alloc; §5 writes ZP entries).
This check is enforced as BV-8 in §9-8, which runs in B3 only.
The code below is the BV-8 reference implementation.
```

```python
for S in zero_pyq_sorted:
    total    = sum(mock_alloc[S][m] for m in range(1, N_mocks + 1))
    expected = MAX_ZERO

    # Extreme case: subtopics beyond index N_mocks get 0 appearances
    if N_mocks < zero_count and zero_pyq_sorted.index(S) >= N_mocks:
        expected = 0

    if total != expected:
        raise ValidationError(
            f"BV-8 FAIL [{section['name']}]: ZP subtopic '{S}' appeared {total} times, "
            f"expected {expected} (MAX_ZERO={MAX_ZERO})"
        )

# Cycle completion note
last_zp_mock = max(
    (m for m, v in zp_rotation_schedule.items() if v is not None),
    default=0
)
if last_zp_mock < N_mocks:
    note(f"ZP cycle complete after mock {last_zp_mock}. "
         f"Mocks {last_zp_mock + 1}–{N_mocks} are 100% PYQ-based for section {section['name']}.")
```

### S5-5 — Summary: what §5 produces

```
After §5 completes for ALL sections:

  zero_pyq_rotation  : dict — {section: [alphabetically sorted ZP subtopic names]}
                       Stored in blueprint.json zero_pyq_rotation field.
                       Empty [] for sections with zero_count=0.

  zp_slot            : dict-of-dicts — {section: {mock: 0 or 1}}
                       All sections populated (including zero-count sections → all 0).
                       Used by §4 (Phase 2 available slots, column-fix) and §9 (BV-5, BV-8).

  mock_alloc         : Updated — ZP subtopic entries written for mocks where they appear.
                       §4 then fills remaining PYQ entries on top.

  zp_rotation_schedule: section-local — {mock: subtopic_name or None}
                        Not stored in blueprint.json (re-derived in B2/B3 from zero_pyq_rotation).
```

## §6 — FORMAT FLAG DETECTION

Reads the Format column from the Frequency Excel and sets
passage_present / figural_present / di_present flags in blueprint.json.
These flags drive registry schema (§12) and Step 2 generation pipelines.

§6 runs during B1 Step 4 (§8-2), after Excel is read in B1 Step 2.

### ══════════════════════════════════════════════════════════════
### GOLDEN RULE — FORMAT IS CLASSIFICATION ONLY, NEVER EXCLUSION
### ══════════════════════════════════════════════════════════════

```
FORMAT VALUE (TEXT / FIGURAL / PASSAGE / DI) TELLS STEP 2 HOW TO GENERATE A QUESTION.
IT NEVER DETERMINES WHETHER A SUBTOPIC IS INCLUDED IN ALLOCATION.

THERE IS EXACTLY ONE CRITERION FOR EXCLUDING A SUBTOPIC FROM §4 ALLOCATION:
  r_avg = 0.0  (Zero-PYQ — handled by §5 rotation instead)

THERE IS NO OTHER EXCLUSION CRITERION. PERIOD.

THEREFORE:
  ✅ FIGURAL subtopics → ALWAYS included in §4 allocation (if r_avg > 0)
  ✅ PASSAGE subtopics → ALWAYS included in §4 allocation (if r_avg > 0)
  ✅ DI subtopics      → ALWAYS included in §4 allocation (if r_avg > 0)
  ✅ TEXT subtopics    → ALWAYS included in §4 allocation (if r_avg > 0)

VIOLATIONS OF THIS RULE THAT MUST NEVER OCCUR:
  ✗ Excluding FIGURAL subtopics from allocation because they require images
  ✗ Excluding FIGURAL subtopics based on any exam-structural change remembered
    from a prior session, memory, or conversation outside the current input documents
  ✗ Excluding any subtopic because its Format is non-TEXT
  ✗ Excluding any subtopic for any reason NOT explicitly encoded in the input
    documents uploaded in THIS session

MEMORY OVERRIDE PROHIBITION:
  Claude's memory of prior sessions MUST NEVER override what the input documents
  say about which subtopics exist and what their Format is.
  If memory contradicts input documents → input documents WIN. Always.
  If memory suggests a "ban" or "exclusion" of subtopics → IGNORE memory.
  Read the input documents. Follow them.

v1.23 RECONCILIATION — FORMAT NOW ALSO INFLUENCES SCHEDULING (still never EXCLUDES):
  The three-axis feature adds a NEW use of format: per-section Axis-1 (stimulus) and
  Axis-3 (mechanism) TARGETS steer WHICH subtopics fill the free allocation slots so a
  mock replicates the exam's format mix (S7-7 axis_schedule). This does NOT weaken the
  GOLDEN RULE:
    • The SOLE exclusion criterion is STILL r_avg = 0.0. Format never excludes.
    • A FIGURAL/PASSAGE/DI subtopic with r_avg > 0 is STILL always allocated (§4).
    • Format now additionally INFLUENCES the ORDER/CHOICE of free fills (soft-steer,
      tie-break only) and is verified within tolerance downstream (Step 8) — it never
      removes a subtopic from allocation.
  SCHEDULING-INFLUENCE ⊃/≠ EXCLUSION. If the axis target and the GOLDEN RULE ever appear
  to conflict, the GOLDEN RULE wins: keep the subtopic, accept a format-target shortfall
  (audited within tolerance), never drop the subtopic.
```

### ═══════════════════════════════════════════════════════════════

### S6-1 — Read and normalize Format values

```python
VALID_FORMATS = {'TEXT', 'FIGURAL', 'PASSAGE', 'DI'}

ALIASES = {
    # Abbreviated
    'FIG'         : 'FIGURAL',
    'FIGURE'      : 'FIGURAL',
    'IMAGE'       : 'FIGURAL',
    'NON-VERBAL'  : 'FIGURAL',
    'NONVERBAL'   : 'FIGURAL',
    # Passage variants
    'PASS'        : 'PASSAGE',
    'RC'          : 'PASSAGE',
    'READING'     : 'PASSAGE',
    'COMPREHENSION': 'PASSAGE',
    # DI variants
    'DATA'        : 'DI',
    'TABLE'       : 'DI',
    'CHART'       : 'DI',
    'GRAPH'       : 'DI',
    'PIE'         : 'DI',
}

format_map        = {}   # subtopic_name → normalized Format string
flagged_subtopics = []   # [(subtopic, reason)] — missing or unknown Format values

# 'master_data_sheet' = the identified Master Data sheet from S2-3
# (not hardcoded name — identified by column structure during B1 Step 2)
for row in master_data_sheet:
    subtopic   = row.get('Sub-Topic', None)

    # Skip blank rows (merged headers, empty rows)
    if not subtopic or str(subtopic).strip() == '':
        continue
    subtopic = str(subtopic).strip()

    raw_format = row.get('Format', None)

    # Missing Format value
    if raw_format is None or str(raw_format).strip() == '':
        flagged_subtopics.append((subtopic, 'missing'))
        continue

    normalized = str(raw_format).strip().upper()
    normalized = ALIASES.get(normalized, normalized)

    # Unknown value after alias resolution
    if normalized not in VALID_FORMATS:
        flagged_subtopics.append((subtopic, f'unknown value: {raw_format!r}'))
        continue

    format_map[subtopic] = normalized

# Fallback: if subtopic not in format_map, check subject-specific tab
for section in sections:
    for S in pyq_subtopics[section] + zero_pyq_subtopics[section]:
        if S not in format_map:
            # Try subject-specific tab for this section
            tab_format = _get_format_from_subject_tab(S, section)
            if tab_format:
                normalized = ALIASES.get(tab_format.strip().upper(), tab_format.strip().upper())
                if normalized in VALID_FORMATS:
                    format_map[S] = normalized
                    note(f"Format for '{S}' found in subject tab (not Master Data).")
                else:
                    flagged_subtopics.append((S, f'unknown in subject tab: {tab_format!r}'))
            else:
                flagged_subtopics.append((S, 'missing from Master Data and subject tab'))

# HALT B1 if any Format values unresolved
if flagged_subtopics:
    unresolved = "\n".join(f"  • {s}: {r}" for s, r in flagged_subtopics)
    raise RuntimeError(
        "Format column incomplete — B1 cannot proceed.\n"
        f"Unresolved subtopics:\n{unresolved}\n\n"
        "Options:\n"
        "  (a) Update Excel Format column and re-upload\n"
        "  (b) Confirm TEXT for each flagged subtopic\n"
        "  (See §10 S10-11 for handling partial Format column)"
    )
```

### S6-2 — Set exam-level flags

```python
# Guard: format_map must be populated (S6-1 HALT ensures this)
if not format_map:
    raise RuntimeError(
        "format_map is empty — S6-1 did not complete successfully. "
        "Cannot set exam-level Format flags."
    )

# Scan all subtopics across all sections
passage_present = any(fmt == 'PASSAGE' for fmt in format_map.values())
figural_present = any(fmt == 'FIGURAL' for fmt in format_map.values())
di_present      = any(fmt == 'DI'      for fmt in format_map.values())
all_text_exam   = not passage_present and not figural_present and not di_present

# v1.8 MSQ: answer_cardinality per subtopic comes from section_rules CATEGORY B (Step 0 v2.5),
# NOT from the Excel Format column (Format is single|multi-orthogonal). Read it the same
# way other per-subtopic section_rules fields are read (read_field). Default 'single' so a
# pre-v2.5 section_rules (no answer_cardinality field) yields a fully single-answer, dormant build.
# section_rules_text = contents of [ExamCode]_section_rules.md (Step 0 output, a REQUIRED
# Step 1 input). Loaded defensively here in case B1 has not already loaded it.
try:
    section_rules_text
except NameError:
    try:
        section_rules_text = open(f'{exam_code}_section_rules.md', encoding='utf-8').read()
    except Exception:
        section_rules_text = ''   # absent/old → all answer_cardinality default to 'single'
answer_cardinality_map = {}
for sec in sections:
    for S in pyq_subtopics[sec] + zero_pyq_subtopics[sec]:
        am = read_field(S, 'answer_cardinality', section_rules_text) if section_rules_text else None
        # Phase-0 back-compat: accept the pre-unification field name 'answer_mode' if a
        # section_rules predating the rename is supplied (prevents silent fall-through to 'single').
        if am is None and section_rules_text:
            am = read_field(S, 'answer_mode', section_rules_text)
        answer_cardinality_map[S] = (am or 'single').strip().lower()
multi_present = any(am == 'multi' for am in answer_cardinality_map.values())

# v1.10 NAT: per-subtopic answer_type (the second dispatch axis), read from section_rules
# CATEGORY B. New field in Step-0 v2.8 — an older section_rules lacking it defaults every
# subtopic to 'option' (correct: no NAT). No old-name fallback needed (answer_type is new).
answer_type_map = {}
for sec in sections:
    for S in pyq_subtopics[sec] + zero_pyq_subtopics[sec]:
        at = read_field(S, 'answer_type', section_rules_text) if section_rules_text else None
        answer_type_map[S] = (at or 'option').strip().lower()
nat_present = any(at == 'numerical' for at in answer_type_map.values())

# Per-section breakdown (for B1 delivery summary in S6-5)
sections_with_passage  = [sec for sec in sections
                           if any(format_map.get(S) == 'PASSAGE'
                                  for S in pyq_subtopics[sec] + zero_pyq_subtopics[sec])]
sections_with_figural  = [sec for sec in sections
                           if any(format_map.get(S) == 'FIGURAL'
                                  for S in pyq_subtopics[sec] + zero_pyq_subtopics[sec])]
sections_with_di       = [sec for sec in sections
                           if any(format_map.get(S) == 'DI'
                                  for S in pyq_subtopics[sec] + zero_pyq_subtopics[sec])]

# Store in blueprint.json top-level
blueprint['passage_present'] = passage_present
blueprint['figural_present'] = figural_present
blueprint['di_present']      = di_present
blueprint['multi_present']     = multi_present   # v1.8: True iff any subtopic answer_cardinality=='multi'
blueprint['nat_present']       = nat_present     # v1.10: True iff any subtopic answer_type=='numerical'

# v1.8 MSQ carry-through: copy the Step-0 EXAM_STRUCTURE MSQ contract verbatim into
# blueprint.json so Step 2 (k-mode/k, dispatch) and Step 4 (marking) can consume it
# without re-reading section_rules. All values are inert when multi_select_allowed=false.
def _exam_struct_field(key, default, text=section_rules_text):
    # EXAM_STRUCTURE lines are 'key: value'. Returns the raw string value or default.
    import re as _re
    m = _re.search(rf'^\s*{_re.escape(key)}\s*:\s*(.+?)\s*$', text or '', _re.M)
    return m.group(1) if m else default

_msa = _exam_struct_field('multi_select_allowed', 'false').strip().lower()
blueprint['multi_select_allowed'] = (_msa == 'true')
blueprint['q_types'] = _exam_struct_field('q_types', "['MCQ']")
blueprint['msq_contract'] = {
    'msq_k_mode'              : _exam_struct_field('msq_k_mode', 'n/a'),
    'msq_k'                   : _exam_struct_field('msq_k', 'none'),
    # v1.10.1 contract-sync: carry the localized MSQ select-instruction verbatim from
    # section_rules into the contract, structurally parallel to nat_contract.nat_instruction.
    # Step 2/3 still read the instruction from section_rules; this is for parity + visibility
    # so an auditor sees the same shape for both answer types in blueprint.json.
    'msq_instruction'         : _exam_struct_field('msq_instruction', '(One or more options may be correct)'),
    'msq_instruction_hi'      : _exam_struct_field('msq_instruction_hi', '(एक या अधिक विकल्प सही हो सकते हैं)'),
    'negative_marking_by_type': _exam_struct_field('negative_marking_by_type', '{}'),
    'partial_credit'          : _exam_struct_field('partial_credit', 'false').strip().lower() == 'true',
}
# v1.10 NAT carry-through: copy the Step-0 EXAM_STRUCTURE NAT contract verbatim into
# blueprint.json so Step 2 (0-option generation, value+tolerance, instruction) and Step 4
# (resolution + ca_range) consume it without re-reading section_rules. nat_allowed is the
# master gate; all values inert when nat_allowed=false.
_naa = _exam_struct_field('nat_allowed', 'false').strip().lower()
blueprint['nat_allowed'] = (_naa == 'true')
blueprint['nat_contract'] = {
    'nat_answer_type' : _exam_struct_field('nat_answer_type', 'real'),
    'nat_tolerance'   : _exam_struct_field('nat_tolerance', '0'),
    'nat_instruction' : _exam_struct_field('nat_instruction', 'Enter your answer as a numerical value.'),
}
# v1.12 difficulty vocabulary carry-through: copy the Step-0 EXAM_STRUCTURE difficulty_labels
# verbatim into blueprint.json so Step 2 (per-Q difficulty assignment + G-QINDEX) and Step 6
# (Complexity render) read ONE canonical vocabulary without re-reading section_rules. Default
# ['Easy','Medium','Hard']. Fixed alias to the difficulty_schedule COUNT keys: simple→Easy,
# medium→Medium, hard→Hard (see §7 S7-6 / Contract_QuestionMetadataIndex §5). Import-free parse
# of the Python-list repr Step 0 wrote (e.g. "['Easy', 'Medium', 'Hard']"); malformed/absent
# falls back to the canonical default (never a hard stop here).
# SCOPE NOTE — an exam MAY override the label SPELLINGS, but changing the label CARDINALITY
# (a 2- or 5-band set) also requires the S7-5 difficulty_schedule generator (and Step 2's S5
# budget) to emit matching bands; that coordinated change is out of scope here — the default,
# fully-supported path is the 3-band Easy/Medium/Hard set that S7-5 already produces.
_dl_raw = _exam_struct_field('difficulty_labels', "['Easy', 'Medium', 'Hard']").strip()
if _dl_raw.startswith('[') and _dl_raw.endswith(']'):
    _dl = [tok.strip().strip("'\"") for tok in _dl_raw[1:-1].split(',') if tok.strip()]
else:
    _dl = []   # not a list literal → treat as malformed
if not _dl or not all(isinstance(x, str) and x for x in _dl):
    _dl = ['Easy', 'Medium', 'Hard']   # malformed/absent/empty → canonical default
blueprint['difficulty_labels'] = _dl
# Consistency note: multi_present should imply multi_select_allowed. If section_rules says
# multi_select_allowed=false but a subtopic carries answer_cardinality=multi (malformed Step-0
# output), trust multi_select_allowed=false and force the MSQ path off (dormant, safe).
if not blueprint['multi_select_allowed']:
    blueprint['multi_present'] = False
# Same guard for NAT: nat_present should imply nat_allowed. A malformed section_rules with a
# numerical subtopic but nat_allowed=false is forced off (dormant, safe).
if not blueprint['nat_allowed']:
    blueprint['nat_present'] = False

if all_text_exam:
    note("All sections: TEXT only — no figural/passage/DI generation required at Step 2.")
```

### S6-3 — Per-subtopic Format stored in working data

```python
# subtopic_data = working dict built during B1 to hold per-subtopic properties.
# Initialized before §3 runs:
#   subtopic_data = {S: {'r_avg': 0.0, 'format': None, 'type': None, 'answer_cardinality': 'single'}
#                    for section in sections
#                    for S in pyq_subtopics[section] + zero_pyq_subtopics[section]}
#   (answer_cardinality added v1.8 — single|multi, source = section_rules CATEGORY B; default single.)
#   (answer_type added v1.10 — option|numerical, source = section_rules CATEGORY B; default option.)
#
# subtopic_data is NOT a blueprint.json top-level field.
# Format values from subtopic_data are written into each subtopic_allocation object
# inside mocks[].sections[].subtopic_allocations[] (ref §14 S14-7).

for section in sections:
    for S in pyq_subtopics[section] + zero_pyq_subtopics[section]:
        if S not in format_map:
            # Should be unreachable if S6-1 HALT worked correctly
            raise RuntimeError(
                f"Subtopic '{S}' has no Format in format_map after S6-1 completed. "
                f"Algorithmic error — S6-1 should have caught this."
            )
        subtopic_data[S]['format'] = format_map[S]
        subtopic_data[S]['answer_cardinality'] = answer_cardinality_map.get(S, 'single')  # v1.8
        subtopic_data[S]['answer_type'] = answer_type_map.get(S, 'option')  # v1.10 NAT axis
```

### S6-4 — Registry schema impact

```
passage_present = True  → B3 adds rc_manifests[] to registry.json (ref §12)
figural_present = True  → B3 adds figural_manifests[] to registry.json (ref §12)
di_present      = True  → NO manifest added.
                           DI uses self-containment rule: each Q reprints full
                           data table in its own stem. No cross-mock tracking needed.
                           di_present stored in blueprint.json for Step 2 awareness only.
                           Step 2 uses build_word_table() for DI questions.

all_text_exam = True    → registry.json has universal fields only.
                           No rc_manifests[], no figural_manifests[].
```

### S6-5 — B1 delivery: Format flag summary

```
Include in B1 structure summary (ref §11 S11-1):

If all_text_exam:
  "Format: All sections TEXT only — no figural/passage/DI pipelines required at Step 2."

Else:
  "Format flags:
     passage_present : [True/False]
       → rc_manifests[] [will / will not] be added to registry
       → Sections with PASSAGE: [list or 'none']
     figural_present : [True/False]
       → figural_manifests[] [will / will not] be added to registry
       → Sections with FIGURAL: [list or 'none']
     di_present      : [True/False]
       → No manifest (self-containment rule)
       → Sections with DI: [list or 'none']"
```

## §7 — DIFFICULTY SCHEDULE

Determines Simple/Medium/Hard Q counts per mock and stores them
in difficulty_schedule[] in blueprint.json.
Completed entirely in B1 — never modified by B2.

# progressive_mode = True if trigger had '--difficulty progressive', else False
# (set during trigger parsing in S1-1)
#
# blueprint = in-memory dict built in B1, serialized to blueprint.json at B1 Step 7 (§8-2)

### S7-1 — Default difficulty (no trigger flag)

```
If no --difficulty flag in trigger:
  Apply silently, no question asked:
    Simple : 25% of total_qs (rounded via largest-remainder — ref S7-4)
    Medium : 25% of total_qs
    Hard   : 50% of total_qs

  All N_mocks get IDENTICAL counts.

  Example (total_qs = 100):
    Simple = 25, Medium = 25, Hard = 50  (exact — no rounding needed)

  Example (total_qs = 150):
    25% × 150 = 37.5 → floors: simple=37, medium=37, hard=75 → sum=149 → deficit=1
    Tie-break (ref S7-4): sort by (remainder DESC, key name ASC)
    → 'hard' remainder=0.0, 'medium' remainder=0.5, 'simple' remainder=0.5
    → sorted: [medium, simple, hard]  (0.5 tie: 'medium' < 'simple' alphabetically)
    → medium gets +1 → result: Simple=37, Medium=38, Hard=75 = 150 ✓
    (deterministic — always same result for same inputs)
```

### S7-2 — Custom uniform override (--difficulty E:M:H)

```
User provides: --difficulty 20:30:50

Parse and validate:
  Accept colon-separated: 20:30:50
  Also accept space-separated: 20 30 50 → infer as 20:30:50, confirm before proceeding.
    "Interpreted difficulty as 20:30:50. Confirm? (yes/no)"

  s_pct = 20, m_pct = 30, h_pct = 50 (must be whole numbers — integers only)

  If decimal values provided (e.g., 33.5:33.5:33):
    "Difficulty percentages must be whole numbers. Received: 33.5, 33.5, 33.
     Please re-enter with integers only."

  Validation (DR-5):
    s_pct + m_pct + h_pct must equal 100 exactly.
    All values must be ≥ 0.
    If not: "Difficulty percentages must sum to 100. Received: {s_pct}+{m_pct}+{h_pct}={total}"
    Claude does NOT auto-correct. User must re-enter.

Convert to Q counts (S7-4 below).
All N_mocks get the same counts.
```

### S7-3 — Progressive override (--difficulty progressive)

```
After S1-6 verification summary, Claude asks:

  "Progressive difficulty enabled. Please define bands:
   Format: [start]-[end]: E:M:H
   (start/end are mock numbers — e.g., 1-15 or M1-M15 or Mocks 1-15)
   Example:
     1-15:   30:30:40  (warm-up)
     16-35:  25:25:50  (standard)
     36-50:  15:20:65  (intensive)
   Enter your bands (one per line):"

Mock range format: Claude accepts any of these — all parsed to integer pair [start, end]:
  M1-M15 | 1-15 | Mock 1-15 | Mocks 1 to 15 | 1–15 (en-dash)

User provides bands. Claude validates (DR-8):
  V1: No gaps   — every mock from 1 to N_mocks covered by exactly one band
  V2: No overlaps — no mock assigned to two bands
  V3: Each band's percentages sum to 100% (whole numbers only)
  V4: All Q counts resolve to valid integers (via largest-remainder — S7-4)

If any validation fails:
  List ALL failures. Ask user to resubmit entire band definition.
  All-or-nothing — never store partially valid bands.

Each band converted to Q counts per mock (S7-4).
Different mocks get different counts based on their band.
```

### S7-4 — Converting percentages to Q counts (DR-6)

```python
import blueprint_core as bc   # ENGINE (mandated in S1-2b)

# difficulty_counts is provided by the shared engine (single source of truth). Splits
# total_qs into (simple, medium, hard) by the E:M:H percentages via largest-remainder,
# guaranteeing simple+medium+hard == total_qs. Aliased so the S7-5 call site is unchanged.
# bc.difficulty_counts is byte-identical to the removed body across all total_qs ≥ 0
# (proven vs the source over 40k+ swept cases, incl. the total_qs==0 boundary).
difficulty_counts = bc.difficulty_counts
```

### S7-5 — Build difficulty_schedule[]

```python
# Build complete difficulty_schedule for ALL N_mocks in B1.
# B2 reads this but NEVER writes to it.

# progressive_mode: set during S1-1 trigger parsing (True if --difficulty progressive)
# user_bands: list of (start, end, s_pct, m_pct, h_pct) tuples from S7-3
#             Only defined when progressive_mode=True.

def get_band_for_mock(m, user_bands):
    """
    Returns (band_name, s_pct, m_pct, h_pct) for mock number m.
    user_bands = [(start, end, band_name, s_pct, m_pct, h_pct), ...]
    V1/V2 validation guarantees exactly one band covers m.
    """
    for (start, end, band_name, s_pct, m_pct, h_pct) in user_bands:
        if start <= m <= end:
            return band_name, s_pct, m_pct, h_pct
    raise AlgorithmError(f"Mock {m} not covered by any band — V1 validation failed.")

difficulty_schedule = []

for m in range(1, N_mocks + 1):
    if progressive_mode:
        band_name, s_pct, m_pct, h_pct = get_band_for_mock(m, user_bands)
    else:
        band_name             = 'Standard'
        s_pct, m_pct, h_pct  = 25, 25, 50   # default

    simple, medium, hard = difficulty_counts(total_qs, s_pct, m_pct, h_pct)

    difficulty_schedule.append({
        'mock'   : m,
        'band'   : band_name,
        'simple' : simple,
        'medium' : medium,
        'hard'   : hard,
    })

# Validate length
assert len(difficulty_schedule) == N_mocks, (
    f"difficulty_schedule has {len(difficulty_schedule)} entries, expected {N_mocks}"
)

# Store in blueprint (in-memory dict → serialized to blueprint.json at B1 Step 7)
blueprint['difficulty_schedule'] = difficulty_schedule

# Also stored in Sheet 4 of blueprint.xlsx (ref §15-4):
# IMPORTANT — TWO DIFFERENT REPRESENTATIONS:
#   blueprint.json difficulty_schedule[]: stores Q COUNTS (simple/medium/hard as integers
#                                          summing to total_qs, e.g. 25+25+50=100).
#                                          Used by Step 2 to know how many Q per difficulty.
#   blueprint.xlsx Sheet 4 ("Difficulty Schedule"): stores PERCENTAGE NUMBERS
#                                          (Easy/Medium/Hard as integers summing to 100,
#                                           e.g. 25/25/50 or 15/30/55).
#                                          For human review only — not read by any Step.
# These are different: JSON has Q counts, xlsx has percentages. Both are correct.
# Sheet 4 columns: Mock | Band | Easy ([S]%) | Medium ([M]%) | Hard ([H]%) | Total (=100)
```

### S7-6 — What difficulty schedule does NOT do

```
Difficulty schedule tells Step 2:  HOW MANY Simple/Medium/Hard Qs in this mock.
Difficulty schedule does NOT tell:  WHICH specific questions are Simple/Medium/Hard.
                                    WHICH subtopics get Simple vs Hard questions.

Per-subtopic difficulty = Step 7 (MockCreate) responsibility.
Step 2 reads PYQ papers and assigns difficulty to each generated question
based on observed PYQ difficulty patterns for that subtopic.

K-BAL gate in Step 8 (MockCreateAudit) verifies final distribution
matches the blueprint difficulty_schedule counts.

v1.12 — canonical Complexity vocabulary + question_index:
  The per-question difficulty label Step 2 assigns is drawn from the CANONICAL set
  blueprint.difficulty_labels (default Easy/Medium/Hard). Fixed alias to the schedule
  COUNT keys above: simple→Easy, medium→Medium, hard→Hard. Step 2 writes that label,
  per question, into registry.question_index (§12) — NEVER into the paper. Assignment is
  SCHEDULE-FIRST: the difficulty_schedule counts are the quota; PYQ pattern selects WHICH
  questions fill each band. Step 2's G-QINDEX and Step 3's re-sync then require the
  question_index difficulty distribution to EQUAL difficulty_schedule[N] exactly.
  (Contract_QuestionMetadataIndex v1.0.)
```

### S7-7 — Build axis_schedule[] (v1.23 — THREE-AXIS format-distribution target)

The exact parallel of difficulty_schedule (S7-5): a per-section target carried into
blueprint.json for Steps 7/8. Built in B1 from `AXIS_DIST_BY_SECTION` (Step-5 v2.23
manifest) + the per-subtopic `AXIS2_CAP_BY_ID` + `MANIFEST_IDS[*]['format']`. Absent-safe:
a pre-v2.23 manifest yields status='no_pyq' schedules and the feature is inert.

```python
# ── helpers + builder: provided by the shared engine ──────────────────────────
import blueprint_core as bc   # ENGINE (mandated in S1-2b)

# The three-axis schedule math formerly inlined here now lives in blueprint_core.py
# (single source of truth): the largest-remainder apportioner (was _avg_to_counts →
# bc.largest_remainder_apportion), the Axis-2 capability union (was
# _section_axis2_pool_caps → bc.section_axis2_pool_caps), the schedule builder
# (bc.derive_axis_schedule), and the Axis-1 advisory (bc.axis1_feasibility). Only the
# two functions the build loop calls DIRECTLY are aliased below; the other two are
# called INTERNALLY by bc.derive_axis_schedule, so they need no alias here.
#
# RENAME: the builder's window keyword is papers_per_window (was mocks_per_window) —
# a mock is a paper. The RETURNED dict still carries the 'mocks_per_window' KEY that
# Steps 7/8 read (output contract unchanged); only the parameter name changed, so the
# build-loop call site below passes papers_per_window=. Verified byte-identical to the
# removed builder over 5k random axis distributions (incl. no_pyq / band / guarantee /
# float and the output-key check).
derive_axis_schedule = bc.derive_axis_schedule
axis1_feasibility    = bc.axis1_feasibility

# ── build axis_schedule for ALL sections (B1, right after difficulty_schedule) ────
axis_schedule = {}
for section in sections:
    sec_name = section['name']
    sec_qs   = section['total_qs']
    # subtopic_ids in this section, split by r_avg (reuse §3-5 classification via names→ids).
    # NOTE: pyq_subtopics/zero_pyq_subtopics are keyed by the section LOOP VARIABLE (§3-5
    # init `{section: [] for section in sections}`), so index with `section`, never `sec_name`.
    pyq_names = pyq_subtopics[section]
    zp_names  = zero_pyq_subtopics[section]
    pyq_ids = [sid for sid, mv in MANIFEST_IDS.items()
               if mv.get('section') == sec_name and mv['display_name'] in pyq_names]
    zp_ids  = [sid for sid, mv in MANIFEST_IDS.items()
               if mv.get('section') == sec_name and mv['display_name'] in zp_names]
    batch_win = blueprint.get('batch_size_qs', 10)   # B1 uses `blueprint` (bp is a B2 alias)
    sched = derive_axis_schedule(sec_name, AXIS_DIST_BY_SECTION.get(sec_name), sec_qs,
                                 pyq_ids, zp_ids, AXIS2_CAP_BY_ID, MANIFEST_IDS,
                                 papers_per_window=batch_win)   # renamed param (was mocks_per_window)
    # advisory feasibility annotations (never block B1)
    sched['axis1_unreachable_formats'] = axis1_feasibility(
        sec_name, sched.get('axis1_target_per_mock', {}), pyq_ids, MANIFEST_IDS)
    axis_schedule[sec_name] = sched
    for g, f in sched.get('guarantee_feasibility', {}).items():
        if f == 'unsatisfiable':
            note(f"AXIS [{sec_name}]: guarantee format '{g}' has NO capable subtopic — "
                 f"it will be absent (shortfall accepted; never fabricated).")
    if sched.get('axis1_unreachable_formats'):
        note(f"AXIS [{sec_name}]: Axis-1 target names formats with no PYQ subtopic: "
             f"{sched['axis1_unreachable_formats']} — target steered best-effort, audited "
             f"within tolerance at Step 8.")

blueprint['axis_schedule'] = axis_schedule
```

### S7-8 — What axis_schedule does NOT do (v1.23)

```
axis_schedule tells Step 7/8:  the per-section FORMAT-MIX target (per-paper averages),
                               band-mode Axis-2 window quotas, the guarantee list, and the
                               Axis-1/3 per-mock target counts.
axis_schedule does NOT:        hard-force any per-mock format count. Subtopic allocation is
                               hard #1; Axis-1/Axis-3 are locked CONSEQUENCES of it, steered
                               (tie-break) toward target and AUDITED within tolerance at Step 8.
                               The 7 flexible Axis-2 classes are JOINT-solved with difficulty at
                               generation (Step 7). DIRECT floats (residual filler, never audited).
Guarantee handling:            'pyq_covered' formats need NO allocation action — Option-C batch
                               coverage already ensures the capable subtopic appears every window.
                               'unsatisfiable' formats are accepted as absent; NEVER fabricated.
```

## §8 — BATCH EXECUTION

The complete B1 → B2 × ceil(N_mocks/10) → B3 sequence.
Total batches = 1 + ceil(N_mocks / 10) + 1.

### S8-1 — Batch overview

```
B1  : Read all inputs → build blueprint skeleton → deliver blueprint.xlsx (skeleton) + blueprint.json v1
B2  : Generate 10 mocks per batch → validate → deliver updated blueprint.json (1 file only)
B3  : Final validation → generate all 6 output files → deliver

Examples:
  N_mocks = 10  → B1 + B2×1  + B3 = 3 batches total
  N_mocks = 30  → B1 + B2×3  + B3 = 5 batches total
  N_mocks = 50  → B1 + B2×5  + B3 = 7 batches total
  N_mocks = 100 → B1 + B2×10 + B3 = 12 batches total

Last B2 batch may have fewer than 10 mocks when N_mocks is not a multiple of 10.
Example: N_mocks = 35 → B2 batches: 1-10, 11-20, 21-30, 31-35 (4 batches).
```

### S8-2 — B1: Build blueprint skeleton

```
B1 executes the following steps in sequence. When all inputs are clean,
B1 completes in one session response. If any HALT condition triggers
(missing files, format errors, ExamCode mismatch, etc.), B1 pauses at
that point, waits for user resolution, then continues from where it stopped.

Step 1  Session start (§1): trigger parse, file inventory, collision check,
        ExamCode match, Format column check, verification summary.
        HALT here if any critical issue unresolved.

Step 2  Input processing (§2): read exam pattern → sections[] + q_ranges[].
        Read Analysis doc(s) → subtopic taxonomy per section.
        Read Frequency Excel → year-wise data + master_data_sheet identified.

Step 3  Frequency calculation (§3): compute r_avg per subtopic.
        Classify PYQ-based vs Zero-PYQ.
        Compute pooled_avg (reference only, stored in XLS only).

Step 4  Format flag detection (§6): read Format column, normalize values,
        set passage_present / figural_present / di_present.
        HALT here if any Format values unresolved.

Step 4A BV-0A — Subtopic completeness check (§9 S9-0A):
        Verify every subtopic from Analysis doc taxonomy is in
        pyq_subtopics[section] OR zero_pyq_subtopics[section].
        Run FIGURAL-specific audit: all FIGURAL subtopics in Excel
        that appear in Analysis doc must be in allocation lists.
        HALT here if any subtopic is missing. blueprint.json v1 is NOT
        written until BV-0A passes for all sections.

Step 5  Zero-PYQ setup (§5): initialise global ZP containers (S5-0).
        Compute MAX_ZERO per section. Sort ZP subtopics alphabetically.
        Build rotation schedule for all N_mocks.
        Compute zp_slot[section][m] for all sections and mocks.

Step 6  Difficulty schedule (§7): compute difficulty_schedule[] for all N_mocks.
        Apply default 25/25/50 or user override.
        (For progressive mode: user was already prompted for bands during S1-6
         verification summary — ref §7 S7-3. Use the bands provided then.
         If bands were not yet collected, prompt now before proceeding.)

Step 7  Write blueprint.json v1:
        {
          exam_code, exam_name, blueprint_version, n_papers,
          total_mocks, total_questions,
          total_options,     ← number of options per Q (e.g. 4 for most MCQ exams).
                               Read from Step 0 auto-detected n_choices (S1-3a _meta field).
                               Default: 4. Step 2 reads via bp.get('total_options', 4).
                               SYNC: Step 2 uses this for num_options throughout generation.
                               Without this field, Step 2 always defaults to 4 — wrong for
                               5-option exams (UPSC CSP) or 2-option exams.
          option_label,      ← option numbering convention for this exam.
                               Read from section_rules.md option_label_format field (Step 0).
                               Examples: "1/2/3/4" | "A/B/C/D" | "(1)/(2)/(3)/(4)" | "(a)/(b)/(c)/(d)".
                               Carried for visibility; Step 2 reads the authoritative value
                               from section_rules.md R10 (option_label_format).
                               SYNC: Step 2 get_option_labels() normalises this to "N." format.
          passage_present, figural_present, di_present, multi_present,
                             ← multi_present (v1.8): True iff any subtopic answer_cardinality=="multi".
                               Parallel to the other presence flags. Step 2 reads it to enable
                               the MSQ generation path. False ⇒ MSQ path inert (default).
          multi_select_allowed,  ← v1.8: copied verbatim from section_rules EXAM_STRUCTURE
                               (Step 0). bool. Master gate for the whole MSQ contract.
          q_types,           ← v1.8: copied from section_rules EXAM_STRUCTURE, e.g. ['MCQ']
                               or ['MCQ','MSQ']. Step 2/4 read it.
          msq_contract,      ← v1.8: {msq_k_mode, msq_k, negative_marking_by_type,
                               partial_credit}, copied verbatim from section_rules
                               EXAM_STRUCTURE. All inert when multi_select_allowed=false.
                               Step 2 reads k-mode/k; Step 4 reads marking.
          sections[],
          subtopic_list[],        ← NEW: r_avg + format + answer_cardinality per subtopic (see note)
          difficulty_schedule[],
          axis_schedule{},        ← v1.23: per-section THREE-AXIS format-distribution target
                                    (S7-7 / S14-3b). Steps 7/8 read it. Absent-safe (status='no_pyq').
          zero_pyq_rotation{},
          mocks: []               ← empty; B2 populates this
        }

        subtopic_list[] note:
          Stores r_avg, format, answer_cardinality (v1.8), and answer_type (v1.10) for every
          subtopic across all sections.
          Required by B2 to recompute quota (needs r_avg) and rare classification.
          Format: [{subtopic_id, section, topic, subtopic, r_avg, format, type, answer_cardinality, answer_type}]
          answer_cardinality (v1.8): single|multi, copied verbatim from section_rules CATEGORY B.
          answer_type (v1.10): option|numerical, copied verbatim from section_rules CATEGORY B —
          the NAT dispatch axis (orthogonal to answer_cardinality). Default 'option'.
          The Step 2 DISPATCH unit. Whole-subtopic mode (D2) ⇒ no answer-mode split inside
          subtopic_allocations; the per-mock allocation schema is unchanged.
          This field IS stored in blueprint.json — it is the source of truth
          for r_avg in all subsequent steps (B2, B3).
          Ref: §14 S14-1 (updated to include subtopic_list).

Step 8  Generate blueprint.xlsx skeleton (§15): Sheets 1, 3, 4, 5 fully populated.
        Sheet 2 (Blueprint allocation grid): subtopic rows present but mock columns empty
        (mocks[] not yet populated — B2 generates allocations).
        Full Sheet 2 with all allocations is generated in B3 Step 8.
        Sheet 1: Paper Structure | Sheet 3: Summary Stats |
        Sheet 4: Difficulty Schedule | Sheet 5: Phase 0 Verification.
        (Column definitions: ref §15)

        MANDATORY: Before proceeding to Step 9, run §15-CHECKLIST.
        All 5 items (XLSX-1 through XLSX-5) must pass.
        If any item fails: fix the xlsx. Do NOT call present_files until all 5 pass.

Step 9  B1 delivery (ref §11 S11-1):
        Print structure summary in chat (ref §11 S11-1 PART A).
        Call present_files with BOTH files — in this exact order:
          1. [ExamCode]_blueprint.xlsx   (skeleton — Sheets 1,3,4,5 populated; Sheet 2 mock cols empty)
          2. [ExamCode]_blueprint.json   (v1 — mocks[] is [] at this stage)
        Neither file may be omitted. If either file failed to generate: HALT here,
        state which file failed, and do not call present_files until both exist.

╔══════════════════════════════════════════════════════════════════╗
║  ██ BATCH GATE B1 — MANDATORY STOP ██                           ║
║                                                                  ║
║  THIS RESPONSE ENDS HERE.                                        ║
║  Claude MUST NOT proceed to B2 in this response.                 ║
║  B2 begins ONLY in a new response after the user sends an        ║
║  affirmative message: 'continue', 'go', 'next', 'proceed',       ║
║  'ok', or 'yes'.                                                 ║
║                                                                  ║
║  Proceeding to B2 within the same response as B1 is a           ║
║  CRITICAL SPEC VIOLATION regardless of how clean the B1         ║
║  output looks or how efficient it seems.                         ║
║                                                                  ║
║  Reason: The user must review the B1 skeleton (subtopic list,    ║
║  r_avg values, ZP rotation, difficulty schedule) and confirm     ║
║  correctness BEFORE 50 mocks are allocated on top of it.         ║
║  A wrong r_avg in B1 corrupts all N mocks silently.              ║
╚══════════════════════════════════════════════════════════════════╝
```

### S8-3 — B2: Generate mock allocations (one batch = 10 mocks)

```
For each B2 batch covering mocks [start..end]:

Step 1  Read blueprint.json from project knowledge.
        Determine batch range:
          already_done = len(blueprint['mocks'])
          batch_start  = already_done + 1
          batch_end    = min(already_done + 10, N_mocks)

Step 2  Recompute quota[S] for each section using §4-2 formula:
          r_avg[S] from blueprint['subtopic_list']   ← stored in B1 Step 7
          N_mocks   from blueprint['total_mocks']
          total_zp_slots from zp_slot[section] (computed in Step 4a below)
          quota is NOT stored directly — always recomputed deterministically.

Step 3  Derive cumulative assigned[] counts for nonrare_subs from prior mocks:
          for section in sections:
            for S in nonrare_subs_by_section[section]:   # rare and ZP subtopics excluded
              assigned[section][S] = sum(
                alloc['q_count']
                for mock in blueprint['mocks']   # prior mocks only
                for sec  in mock['sections'] if sec['section_name'] == section['name']
                for alloc in sec['subtopic_allocations']
                if alloc['subtopic'] == S and alloc['type'] == 'pyq_based'
              )
          CRITICAL: Never reset assigned[] to 0. Read from blueprint['mocks'] only.
          Resetting = wrong assigned[] counts = subtopic clustering.

Step 4  For each mock m in [batch_start..batch_end]:
          a. Recompute zp_slot[section] for ALL N_mocks using §5-2 formula:
             MAX_ZERO: recompute from len(zero_pyq_rotation[section]) and N_mocks
                       using §5-1 formula  (NOT read from blueprint — not stored there).
             zero_pyq_rotation[section['name']]: from blueprint['zero_pyq_rotation'][section['name']].
             Then build full rotation schedule and zp_slot[section][m] for all mocks.

          b. Run Phase 0 (§4-5 Phase 0 pre-pass): for each batch window in this
             series, force-assign any nonrare subtopic that has zero appearances
             in that window. Run overflow correction at window's last mock.
             Phase 0 must run BEFORE Phase 1 and Phase 2.

          c. Run Phase 1 (§4-4): recompute positions using deterministic formula
             (pos = int((k+0.5)×N_mocks/quota[S])+1) from quota[S] and N_mocks.
             Run batch-coverage validation for rare subtopics (§4-4).

          d. Run Phase 2 (§4-5 even-spread): distribute nonrare_subs evenly.
             Use current assigned[section][S] counts for remaining quota computation.

          e. Run mandate enforcement (S4-MANDATE): M1 (mandatory every mock),
             M2 (alternation groups), M4 (mandatory groups), M6 (min counts).
             Force-place / evict as needed. M2 runs as fixed-point loop.
             M5 (cadence windows) deferred to BV-7 full-series pass.

          f. Run column-fix (§4-6): correct any column sum error (including
             residual imbalances from mandate enforcement relocations).

          g. Update assigned[section][S] for S in nonrare_subs after each mock m.

Step 5  Build section objects and append mocks to blueprint['mocks']:
        # build_section_obj(m, section): creates §14 S14-6 format dict from mock_alloc
        #   {section_name, q_range, total_qs, subtopic_allocations[], validation{}}
        #   subtopic_allocations: one entry per subtopic with q_count > 0
        #   validation: {sum: actual_sum, expected: sec_qs, status: 'pass'}
        for m in range(batch_start, batch_end + 1):
            blueprint['mocks'].append({
                'mock'    : m,
                'paper_id': f"MOCK:M{m:02d}",   # C1 (v1.29): universal paper identity. Additive —
                                                # Steps 7-11 still read 'mock'; the generalised
                                                # (paper_id) path uses this, mock=MOCK:M0k.
                'sections': [build_section_obj(m, section) for section in sections]
            })

Step 6  Run BV-1 to BV-6 AND BV-9B (§9) on the newly added mocks.
        BV-9B: verify every PYQ subtopic appears ≥ 1 Q in this batch window.
        If any check fails: fix internally, re-run checks.
        After 3 failed attempts: state issue clearly, ask user for guidance.
        NEVER deliver blueprint.json with failing validation.

Step 7  B2 delivery (ref §11 S11-2):
        Print summary table: Mock# | section totals | Grand Total | ✓/✗
        Call present_files with EXACTLY ONE file:
          [ExamCode]_blueprint.json  (updated — contains all mocks generated so far)
        blueprint.xlsx is NOT re-delivered in B2 batches — the FINAL allocation-complete
        xlsx is delivered only in B3. Do not include xlsx in B2 present_files call.
        Print upload instruction (MANDATORY):
          "Download this blueprint.json. Delete the old version from your [ExamCode]
           project knowledge. Upload this new version. Then start a fresh chat and
           type 'continue' to generate the next batch."

Step 8  ╔══════════════════════════════════════════════════════════════════╗
        ║  ██ BATCH GATE B2 — MANDATORY STOP AFTER EVERY BATCH ██        ║
        ║                                                                  ║
        ║  THIS RESPONSE ENDS HERE.                                        ║
        ║  Claude MUST NOT proceed to the next B2 batch or to B3          ║
        ║  in the same response as the current B2 batch.                   ║
        ║                                                                  ║
        ║  The next batch begins ONLY in a new response after the user     ║
        ║  sends an affirmative: 'continue', 'go', 'next', 'proceed',      ║
        ║  'ok', or 'yes'.                                                 ║
        ║                                                                  ║
        ║  Reason: assigned[] cumulative counts for the next batch MUST be   ║
        ║  read from the blueprint.json that the user uploads between      ║
        ║  sessions. Generating batches without this upload step corrupts  ║
        ║  cumulative counts and produces subtopic clustering.             ║
        ║                                                                  ║
        ║  VIOLATION PATTERN TO NEVER REPEAT:                              ║
        ║  Generating all 50 mocks (5 B2 batches) in one response,        ║
        ║  bypassing all BATCH GATEs, because it "seems more efficient."   ║
        ║  This is a critical spec violation.                              ║
        ╚══════════════════════════════════════════════════════════════════╝
```

### S8-4 — B2 Phase 1 note: positions recomputed from deterministic formula

```
Phase 1 rare subtopic positions are DETERMINISTIC — always reproducible from:
  quota[S]  — recomputed in B2 Step 2 from blueprint['subtopic_list']
  N_mocks   — from blueprint['total_mocks']

Formula: position_k = int((k + 0.5) × N_mocks / quota[S]) + 1

B2 does NOT store or read phase1_positions from blueprint.json.
Positions recomputed fresh each session from quota and N_mocks.
Same formula → same positions always. Consistent across re-generations.

Phase 2 is stateful: reads cumulative assigned[] (B2 Step 3) to compute remaining quota.
```

### S8-5 — B3: Final validation + generate all output files

```
B3 executes in one session response:

Step 1  Read complete blueprint.json (all N_mocks in mocks[]).
        Verify len(mocks[]) == N_mocks. If not:
        "blueprint.json has [K] mocks, expected [N_mocks].
         Please upload the complete blueprint.json and retry B3."

Step 2  Recompute quota[S] for all sections (from subtopic_list r_avg and N_mocks).
        Recompute zp_slot[section][m] for all mocks (from zero_pyq_rotation and N_mocks).
        Both needed by BV-7 F1 (frequency tiers) and BV-8 (ZP count).

Step 3  Run BV-7 (§9): full validation across ALL N_mocks.
        BV-1 to BV-6 for all mocks + cross-batch checks F1-F5.
        If BV-7 fails: HALT. Mock m is in B2 batch ceil(m/10). Fix that batch.

Step 4  Run BV-8 (§9): zero-PYQ final count check.
        Each ZP subtopic must have exactly MAX_ZERO appearances.
        If BV-8 fails: HALT. Fix rotation. Return to Step 1.

Step 4A Run BV-AXIS (§9 S9-12): axis_schedule integrity + feasibility report (v1.23).
        Hard-fails ONLY on a missing/malformed axis_schedule (a Blueprint bug); the
        format-mix feasibility (Axis-1/3, zp_only/unsatisfiable guarantees) is advisory —
        realized-vs-target proportion is audited within tolerance at Step 8, not here.
        Inert (passes vacuously) when the manifest predates Step 5 v2.23.

Step 5  Generate registry.json (§12):
          Universal: exam_code, schema_version, mocks_completed=[], papers_completed=[],
                     question_hashes=[], stem_texts=[], semantic_tuples=[],
                     question_index=[],
                     image_phashes=[], image_sources_used=[],
                     session_log=[], content_tracking={}
          Conditional (from blueprint flags):
            if passage_present: rc_manifests = []
            if figural_present: figural_manifests = []
            if di_present: no additional field (self-containment rule)

Step 6  Generate [ExamCode]_ExplainLearnings.md:
          # [ExamCode] — [exam_name] MockExplain Learnings
          (header only — Step 4 fills content)

Step 7  Generate [ExamCode]_ExplainAuditLearnings.md:
          # [ExamCode] — [exam_name] MockExplainAudit Learnings
          (header only — Step 5 fills content)

Step 8  Generate FINAL blueprint.xlsx with full allocation data:
          Sheet 2 now fully populated — all mock allocations from blueprint.json.
          (Replaces the skeleton xlsx from B1 which had empty mock columns.)

        MANDATORY: Run §15-CHECKLIST (all 5 items XLSX-1 through XLSX-5) before
        calling present_files. Fix xlsx if any item fails.

Step 8A Generate [ExamCode]_mock_test_audit.py (ref §13-7A):
          COLLISION CHECK: search project knowledge for existing audit script.
            If an existing script FAILS the fixture-based self-test or is a
              CONSTANT-PRINT stub → REPLACE it (it is not a working auditor — the
              old hollow MVP; no downgrade, it audited nothing).
            If an existing script PASSES the fixture-based self-test (same canonical
              version) → replacing with a fresh copy is safe; confirm.
            If not found → proceed silently.
          Write the CANONICAL v2.6 auditor by copying, VERBATIM, the fenced python
          block in Framework_MockTestCreateAudit.md Appendix A (SINGLE SOURCE OF
          TRUTH — §13-7A). No exam-specific edits (it self-parameterises at runtime).
          VALIDATE: python3 [ExamCode]_mock_test_audit.py --self-test
            → MUST print "SELF-TEST: N/N PASS" with N >= 35 AND be FIXTURE-BASED
              (builds docx fixtures; asserts each gate catches + passes; canonical
              build prints 43/43). A constant-print "N/N PASS" is REJECTED.
            If output differs or is not fixture-based → HALT. Regenerate and retry.

        present_files with all 6 output files (ref §11 S11-3):
          Order: blueprint.xlsx, blueprint.json, registry.json,
                 ExplainLearnings.md, ExplainAuditLearnings.md, mock_test_audit.py

        CHECKLIST before calling present_files:
          ☐ §15-CHECKLIST items XLSX-1 through XLSX-5 all passed
          ☐ [ExamCode]_blueprint.xlsx  exists at /mnt/user-data/outputs/
          ☐ [ExamCode]_blueprint.json  exists at /mnt/user-data/outputs/
          ☐ [ExamCode]_registry.json   exists at /mnt/user-data/outputs/
          ☐ [ExamCode]_ExplainLearnings.md        exists at /mnt/user-data/outputs/
          ☐ [ExamCode]_ExplainAuditLearnings.md   exists at /mnt/user-data/outputs/
          ☐ [ExamCode]_mock_test_audit.py          exists at /mnt/user-data/outputs/
          ☐ mock_test_audit.py --self-test passed (13/13 PASS)
          ☐ BV-7 passed for all N_mocks (§9-7)
          ☐ BV-8 passed for all ZP subtopics (§9-8)
          ☐ len(blueprint['mocks']) == N_mocks
        If any checklist item fails: HALT. Do not call present_files. Fix and retry.

Step 9  Print handoff message (ref §11 S11-3).
```

### S8-6 — Between B2 sessions (user action required)

```
After each B2 batch delivery:
  User downloads updated blueprint.json.
  User deletes old blueprint.json from [ExamCode] project knowledge.
  User uploads new blueprint.json to [ExamCode] project knowledge.
  User starts fresh chat for next B2 batch.

Why fresh chat?
  Claude reads project knowledge files ONCE at session start.
  Mid-session uploads are NOT visible to Claude in that session.

Starting next B2 batch:
  Claude reads blueprint.json → gets K = len(mocks[]) already done.
  Next batch: mocks [K+1] to [min(K+10, N_mocks)].
  Claude always derives progress from len(mocks[]) — no expected-count comparison needed.

  If user explicitly states a wrong starting mock (e.g., "start from mock 21"
  but blueprint has only K=10 mocks): flag as stale per S1-7.
  Otherwise: start from K+1 automatically.
```

### S8-7 — Re-generating a specific batch

```
User may request: "Re-generate mocks 11-20"

Claude procedure:
  1. Read current blueprint.json.
  2. Remove mocks 11-20 from blueprint['mocks'] (keeping mocks 1-10 and any beyond 20).
  3. Rebuild assigned[] for nonrare_subs from mocks [1..10] ONLY.
     (Do NOT include mocks 21+ in assigned[] — those weren't done when batch 11-20
     was originally generated, and including them corrupts assigned[] counts.)
  4. Re-run Phase 0 + Phase 1 + Phase 2 for mocks 11-20 using rebuilt assigned[] context.
  5. Re-validate BV-1 to BV-6 AND BV-9B for new mocks 11-20.
  6. Re-deliver summary table + updated blueprint.json.

After regeneration:
  BV-7 + BV-8 must re-pass in B3 before registry is generated.
  User uploads corrected blueprint.json to project before B3.
```

## §9 — VALIDATION GATES

All BV checks. BV-1 to BV-6 run after every B2 batch.
BV-7 and BV-8 run only in B3 before registry generation.
BV-0A runs DURING B1 (Step 4A — after §3 and §6 complete, before §5) — before blueprint.json v1 is written.

# Context variables available in §9 (set in S8-3):
#   batch_mocks      = list(range(batch_start, batch_end + 1))
#   batch_range      = set(batch_mocks)
#   all_done_mocks   = list(range(1, batch_end + 1))   # all mocks done so far
#
# Per-section data structures (built per section in §4/§5):
#   all_subs_in_section[section]   = pyq_subtopics[section] + zero_pyq_subtopics[section]
#   rare_subs_by_section[section]  = [S for S in pq_subs if r_avg[S] < RARE_THRESHOLD]
#   MAX_ZERO_by_section[section]   = MAX_ZERO (scalar computed in §5-1, stored here)
#
# Failure collection:
#   bv_failures = []   # list of failure messages; raised/reported after all checks
#   def fail(msg): bv_failures.append(msg)
#   def warn(msg): bv_warnings.append(msg)

### S9-0A — BV-0A: Subtopic completeness check (runs at END of B1, before blueprint.json v1 written)

```
PURPOSE: Catches Format-based exclusion errors (and any other accidental omissions)
BEFORE any allocation runs. This check is the primary defence against the error of
excluding subtopics based on Format value or memory-based rules.

BV-0A RUNS IN B1 — immediately after §3 (r_avg computed) and §6 (format_map built).
It verifies that every subtopic from the Analysis doc taxonomy is present in
pyq_subtopics[section] OR zero_pyq_subtopics[section].

```python
# analysis_taxonomy[section] = complete list of subtopics extracted from Analysis doc in §2-2
# (every subtopic named in the doc, regardless of Format)

for section in sections:
    all_allocated = set(pyq_subtopics[section]) | set(zero_pyq_subtopics[section])
    analysis_subs = set(analysis_taxonomy[section])

    # Check 1: No subtopic from Analysis doc is missing from allocation lists
    missing = analysis_subs - all_allocated
    if missing:
        raise RuntimeError(
            f"BV-0A FAIL [{section['name']}]: {len(missing)} subtopic(s) from Analysis doc "
            f"are absent from pyq_subtopics + zero_pyq_subtopics.\n"
            f"Missing: {sorted(missing)}\n\n"
            f"LIKELY CAUSE: Subtopics were excluded based on Format value or memory.\n"
            f"FIX: Format is NEVER an exclusion criterion (ref §6 GOLDEN RULE).\n"
            f"     Include ALL subtopics. r_avg=0 → ZP rotation. r_avg>0 → §4 allocation."
        )

    # Check 2: No extra subtopics in allocation that aren't in Analysis doc
    # (catches phantom subtopics added from memory or Excel-only rows)
    extra = all_allocated - analysis_subs
    if extra:
        raise RuntimeError(
            f"BV-0A FAIL [{section['name']}]: {len(extra)} subtopic(s) in allocation lists "
            f"are NOT in the Analysis doc taxonomy.\n"
            f"Extra: {sorted(extra)}\n\n"
            f"LIKELY CAUSE: Subtopics added from Excel rows not in Analysis doc.\n"
            f"FIX: Analysis doc is the taxonomy authority (ref §2-2 source priority).\n"
            f"     Remove extra subtopics from allocation lists."
        )

    # Check 3: Format-specific audit — FIGURAL subtopics must not be silently absent
    figural_in_excel = [S for S in format_map if format_map[S] == 'FIGURAL'
                        and S in analysis_subs]
    figural_missing  = [S for S in figural_in_excel if S not in all_allocated]
    if figural_missing:
        raise RuntimeError(
            f"BV-0A FAIL [{section['name']}]: FIGURAL subtopics from Excel are missing "
            f"from allocation:\n  {figural_missing}\n\n"
            f"CRITICAL: FIGURAL subtopics are NEVER excluded. "
            f"Format=FIGURAL means Step 2 generates image questions. "
            f"It does NOT mean the subtopic is excluded from the blueprint.\n"
            f"Ref: §6 GOLDEN RULE — FORMAT IS CLASSIFICATION ONLY, NEVER EXCLUSION."
        )
```

BV-0A failure → B1 HALTS immediately. blueprint.json v1 is NOT written.
Fix the inclusion error, then re-run from §3.

Print result in B1 structure summary (§11 S11-1):
  "BV-0A (Subtopic completeness): ✓ All [N] subtopics from Analysis doc present
   Format audit: TEXT=[n] | FIGURAL=[n] | PASSAGE=[n] | DI=[n]"
```

### S9-0 — BV-0: Sequence enforcement

```
BV ALWAYS runs BEFORE summary table is shown to user.

Sequence per B2 batch:
  1. Generate mock allocations (§5 ZP rotation first, then §4 Phase 0 → Phase 1 → Phase 2)
  2. Run BV-1 to BV-6 AND BV-9B
  3. If any fail: fix internally → re-run → iterate (ref S9-10)
  4. Only after ALL checks pass: show summary table + deliver blueprint.json

Summary table IS the output of successful validation.
Never show table before BV completes.
Never show table if any check has ✗ status.
```

### S9-1 — BV-1: Column sums

```python
# Check: each section sum = sec_qs AND cross-section total = total_qs

for m in batch_mocks:
    for section in sections:
        subs = all_subs_in_section[section]   # pyq + zp subtopics
        col_sum = sum(mock_alloc[S][m] for S in subs)
        if col_sum != section['total_qs']:
            fail(f"BV-1 FAIL: Mock {m}, Section {section['name']}: "
                 f"sum={col_sum}, expected={section['total_qs']}")

    cross_total = sum(
        sum(mock_alloc[S][m] for S in all_subs_in_section[sec])
        for sec in sections
    )
    if cross_total != total_qs:
        fail(f"BV-1 FAIL: Mock {m}: cross-section total={cross_total}, "
             f"expected total_qs={total_qs}")
```

### S9-2 — BV-2: Every rare subtopic appears in its scheduled positions

```python
# Per-batch scope: only check mocks in THIS batch.
# Phase 1 positions for future batches: no violation if not yet reached.

for S in rare_subs_by_section[section]:   # per section
    q = quota[S]
    scheduled_positions = [int((k + 0.5) * N_mocks / q) + 1 for k in range(q)]
    for pos in scheduled_positions:
        if pos in batch_range:
            if mock_alloc[S][pos] == 0:
                fail(f"BV-2 FAIL: Rare subtopic '{S}' scheduled for mock {pos} "
                     f"but mock_alloc={mock_alloc[S][pos]}")

# Series-level completeness (every non-zero subtopic appears ≥1 mock) is
# enforced by BV-7 F1: Tier 3 quota=1 must achieve ≥1 appearance.
```

### S9-3 — BV-3: Frequency accuracy (warning per batch, strict at final)

```python
# PER-BATCH: early warning only — does not fail the batch

for section in sections:
    for S in pyq_subtopics[section]:
        assigned_so_far = sum(mock_alloc[S][m] for m in all_done_mocks)
        mocks_done      = len(all_done_mocks)
        expected_so_far = quota[S] * mocks_done / N_mocks   # linear progress expected

        if expected_so_far > 0:
            ratio_error = abs(assigned_so_far - expected_so_far) / expected_so_far * 100
            if ratio_error > 30:
                warn(f"BV-3 ⚠: '{S}' tracking off: "
                     f"assigned={assigned_so_far}, expected≈{expected_so_far:.1f} "
                     f"({ratio_error:.0f}% off)")

# FINAL (BV-7 F1): strict SA-12 tiers applied after all N_mocks generated.
#   Tier 1 (quota > 20): ±2%
#   Tier 2 (quota 5–20): ±15%
#   Tier 3 (quota 1–4):  ±25%
```

### S9-4 — BV-4: Max rare Qs per mock per section

```python
# MAX_RARE_PER_MOCK read from bp.get('max_rare_per_mock', 2) in §4-8
for m in batch_mocks:
    for section in sections:
        rare_count = sum(mock_alloc[S][m] for S in rare_subs_by_section[section])
        if rare_count > MAX_RARE_PER_MOCK:
            fail(f"BV-4 FAIL: Mock {m}, Section {section['name']}: "
                 f"{rare_count} rare Qs (max {MAX_RARE_PER_MOCK}). "
                 f"Rare subs present: "
                 f"{[S for S in rare_subs_by_section[section] if mock_alloc[S][m] > 0]}")
```

### S9-5 — BV-5: Zero-PYQ cumulative count ≤ MAX_ZERO

```python
for section in sections:
    for S in zero_pyq_subtopics[section]:
        total_so_far = sum(mock_alloc[S][m] for m in all_done_mocks)
        max_z = MAX_ZERO_by_section[section]
        if total_so_far > max_z:
            fail(f"BV-5 FAIL: ZP subtopic '{S}' has {total_so_far} appearances "
                 f"so far (MAX_ZERO={max_z})")
```

### S9-6 — BV-6: No negative allocation

```python
for m in batch_mocks:
    for section in sections:
        for S in all_subs_in_section[section]:
            if mock_alloc[S][m] < 0:
                fail(f"BV-6 FAIL: Negative allocation — "
                     f"subtopic='{S}', mock={m}, value={mock_alloc[S][m]}")
```

### S9-6b — BV-10: Two-tier same-form / mechanic guard (MANDATE 7 — v1.24)

```
BV-10 protects the student from duplicate questions WITHOUT deadlocking on the coarse
"diversity family" axis. It is TWO tiers, aligned with Step 5 v2.24 fields and Step 7's
generation contract (family/CONCEPT_GROUP MAY repeat N times; form_key/scenario_key MUST
be unique):

  BV-10a — HARD guard on FORM_KEY (fine identity).
    Two DISTINCT subtopics sharing a form_key are the SAME student-facing form; they must
    not co-occur in one mock within their collision_domain (default = section). This is the
    real "antonym×2 / synonym×2" protection. Because Step 5 gives genuinely-distinct forms
    distinct form_keys, this fires ONLY on true duplicates — which is correct behaviour.
    It can never deadlock at B2: the B1 gate (§4-1b) PROVES it satisfiable before generation;
    if not, B1 HALTs with a precise upstream fix (merge/split), never a regeneration loop.

  BV-10b — SOFT cap on FAMILY (coarse diversity).
    Per mock, count(family) ≤ cap_M, cap_M = blueprint['max_per_mechanic_per_mock'].get(
    family, 1). A STEERING TARGET audited within tolerance at Step 8 — NEVER a hard blocker.
    Over-cap is a diversity note, not a failure (every question is still unique at form_key).

PREREQUISITE (Step 5 v2.24.1): section_rules.md carries form_key, question_mechanic,
concept_group(=family) and collision_domain for every subtopic. Fallback chain if a field
is absent: form_key → question_mechanic → subtopic_id; collision_domain → section name.
(§7.1 CRITICAL, v2.24.1: concept_group is REMOVED from the form_key fallback chain. Under
v2.24.1 concept_group is DELIBERATELY SHARED across subtopics on a subject exam, so falling
back to it would read one family token for several distinct subtopics and raise a FALSE
BV-10a duplicate HALT. An absent form_key on a v2.24.1 manifest means the file is stale —
re-run Step 5; do NOT guess from concept_group.)

PROCEDURE (runs in B2 per batch AND B3 full validation):

  cap_of = blueprint.get('max_per_mechanic_per_mock', {})   # {family: int}, default 1
  for m in batch_mocks:
      seen_form = {}      # {(domain, form_key): subtopic}   — BV-10a HARD
      fam_count = {}      # {(domain, family): count}        — BV-10b SOFT
      for section in sections:
          for S in all_subs_in_section[section]:
              if mock_alloc[S][m] == 0:
                  continue
              dom = read_field(S,'collision_domain',section_rules_text) or section['name']
              fk  = (read_field(S,'form_key',section_rules_text)
                     or read_field(S,'question_mechanic',section_rules_text)
                     or read_field(S,'subtopic_id',section_rules_text)   # §7.1 v2.24.1: NOT concept_group
                     or S.lower().strip())
              fam = (read_field(S,'concept_group',section_rules_text)
                     or read_field(S,'question_mechanic',section_rules_text) or fk)
              key = (dom, fk)
              if key in seen_form and seen_form[key] != S:
                  fail(  # HARD — but §4-1b guarantees this is unreachable unless true-dup
                    f"BV-10a FAIL [Mock {m}]: '{seen_form[key]}' and '{S}' share "
                    f"form_key='{fk}' in domain '{dom}' — identical student-facing form. "
                    f"These are TRUE DUPLICATES. Fix at source (Step 5 v2.24): merge them, "
                    f"or split into distinct forms. (Should have been caught at B1 §4-1b.)")
              seen_form[key] = S
              fam_count[(dom,fam)] = fam_count.get((dom,fam),0) + 1
      for (dom,fam),cnt in fam_count.items():          # BV-10b SOFT — record, never fail
          cap = cap_of.get(fam, 1)
          if cnt > cap:
              soft_note(
                f"BV-10b [Mock {m}]: family '{fam}' appears {cnt}× (soft cap {cap}) in "
                f"domain '{dom}'. Questions remain unique at form_key level; diversity note, "
                f"not a failure. Raise max_per_mechanic_per_mock['{fam}'] to widen the cap.")

BV-10 runs:
  — B1: §4-1b feasibility gate PROVES BV-10a satisfiable (HALT-with-fix if not — terminating).
  — B2 per batch and B3 full validation: BV-10a HARD (unreachable on clean Step-5 data),
    BV-10b SOFT advisory (audited at Step 8 within tolerance).
  — SEVERITY: BV-10a HARD but B1-guaranteed terminating (no 3-attempt loop); BV-10b never blocks.
  — auto-correctable: BV-10a via §4-1b upstream HALT; BV-10b via cap config / Step-8 tolerance.
  — SCOPE: per collision_domain (default = section) — no cross-section false positives; a
    genuinely cross-section shared form_key uses an explicit collision_domain from Step 5.
```

### S9-7 — BV-7: Full cross-batch validation (runs in B3 only)

```
BV-7 re-runs BV-1 to BV-6 across ALL N_mocks.
PLUS five cross-batch checks only possible with the full series view:

F1 — Strict frequency tiers (SA-12):
  For every PYQ-based subtopic S:
    actual_total = Σ mock_alloc[S][m] for m in 1..N_mocks
    tier 1 (quota > 20): |actual - quota| / quota ≤ 0.02
    tier 2 (quota 5–20): |actual - quota| / quota ≤ 0.15
    tier 3 (quota 1–4):  |actual - quota| / quota ≤ 0.25
  fail if any subtopic exceeds its tier tolerance.

F2 — No end-clustering of rare subtopics:
  series_avg_rare = (Σ_S in rare_subs_by_section[section]
                      Σ_m mock_alloc[S][m]) / N_mocks
  last_10pct_mocks = range(int(0.9 * N_mocks) + 1, N_mocks + 1)
  For each mock m in last_10pct_mocks:
    rare_in_m = Σ mock_alloc[S][m] for S in rare_subs_by_section[section]
    if rare_in_m > series_avg_rare * 1.5:
      fail(f"F2: End-clustering in mock {m}: {rare_in_m} rare Qs > "
           f"{series_avg_rare * 1.5:.1f} (1.5 × series avg)")

F3 — Zero-PYQ rotation order correct:
  For each section:
    rotation = blueprint['zero_pyq_rotation'][section['name']]   # alphabetical list
    max_z    = MAX_ZERO_by_section[section]
    expected_seq = rotation * max_z   # e.g., [A,B,C,A,B,C] for MAX_ZERO=2
    actual_seq   = [zp_rotation_schedule[m]
                    for m in sorted(zp_rotation_schedule)
                    if zp_rotation_schedule[m] is not None]
    if actual_seq != expected_seq[:len(actual_seq)]:
      fail(f"F3: ZP rotation order wrong in section {section['name']}. "
           f"Expected: {expected_seq[:5]}... Got: {actual_seq[:5]}...")

F4 — Phase 1 positions evenly spread:
  For each rare subtopic S with quota q:
    ideal_positions = [int((k + 0.5) * N_mocks / q) + 1 for k in range(q)]
    actual_positions = [m for m in range(1, N_mocks+1) if mock_alloc[S][m] > 0]
    import math
    max_deviation = math.ceil(N_mocks / (2 * q))
    for k, (ideal, actual) in enumerate(zip(sorted(ideal_positions),
                                            sorted(actual_positions))):
      if abs(actual - ideal) > max_deviation:
        fail(f"F4: '{S}' appearance {k+1}: actual mock {actual}, "
             f"ideal {ideal}, deviation {abs(actual-ideal)} > {max_deviation}")

F5 — Even spread / per-mock cap for nonrare subtopics (SA-14, INVARIANT 7):
  For every nonrare subtopic S in every section:
    per_mock_values = [mock_alloc[S][m] for m in range(1, N_mocks + 1)]
    variance = max(per_mock_values) - min(per_mock_values)
    cap      = math.ceil(quota[S] / N_mocks)
    if variance > 1:
      fail(f"F5: '{S}' has variance={variance} across mocks (max allowed=1). "
           f"quota={quota[S]}, per_mock={per_mock_values}. "
           f"Phase 2 front-loaded this subtopic instead of spreading evenly.")
    if max(per_mock_values) > cap:
      fail(f"F5: '{S}' has max={max(per_mock_values)} in a single mock "
           f"but per_mock_cap={cap} (= ceil({quota[S]}/{N_mocks})). "
           f"SA-14 violation.")
  Rationale: variance > 1 means a subtopic appears e.g. 12Q in M1 and 0Q in M10
  for a quota of 23 — this produces inconsistent mock tests.
  The correct distribution is floor(quota/N) or floor(quota/N)+1 per mock.
  This check catches the front-loading bug if Phase 2 is implemented without SA-14.

BV-7 failure → B3 HALTS.
Identify failing mock m → it is in B2 batch ceil(m / 10).
Re-generate that B2 batch. Return to B3 Step 1 (§8-5).
```

### S9-8 — BV-8: Zero-PYQ final count (runs in B3 only)

```python
for section in sections:
    zp_sorted = blueprint['zero_pyq_rotation'][section['name']]
    max_z     = MAX_ZERO_by_section[section]
    zero_count = len(zp_sorted)

    for S in zp_sorted:
        total    = sum(mock_alloc[S][m] for m in range(1, N_mocks + 1))
        expected = max_z
        # Extreme case: subtopics beyond index N_mocks get 0 appearances
        if N_mocks < zero_count:
            idx      = zp_sorted.index(S)
            expected = 1 if idx < N_mocks else 0

        if total != expected:
            fail(f"BV-8 FAIL [{section['name']}]: '{S}' appeared {total} times, "
                 f"expected {expected} (MAX_ZERO={max_z})")

# BV-8 failure → B3 HALTS.
# BV-8 failure indicates a bug in §5 ZP rotation or blueprint.json corruption.
# Resolution: re-run entire Step 1 (B1 through B3) to regenerate correct rotation.
```

### S9-9 — BV-9: Reporting format

```
Print after every B2 batch (BV-1 to BV-6, BV-9B) and after B3 (BV-7, BV-8):

  [Check ID] ([Name]): [✓ / ✗ / ⚠] [Result summary]
  On failure or warning: add detail line.

Examples (B2 batch, all passing — section names/counts are illustrative):
  BV-1  (Col sums)       : ✓ All 10 mocks × [N] sections = exact sec_qs
  BV-2  (Scheduled)      : ✓ No Phase 1 position violations in batch
  BV-3  (Freq acc)       : ✓ All within 30% of proportional target
  BV-4  (Rare limit)     : ✓ Max rare Qs/mock/section = 1 (limit = MAX_RARE_PER_MOCK)
  BV-5  (ZP cumul)       : ✓ No ZP subtopic exceeds MAX_ZERO
  BV-6  (No negatives)   : ✓ All q_counts ≥ 0
  BV-9B (Batch coverage) : ✓ All PYQ subtopics ≥ 1Q in batch — [Sec1]=[n] [Sec2]=[n] ... [SecN]=[n]

Example (failure with auto-fix — section/subtopic names are illustrative):
  BV-1 (Col sums) : ✗ Mock 14, [Section X]: sum=24, expected=25
                     → Fixing: +1 to '[lowest-allocated subtopic]' in mock 14
                     → Re-checking...
  BV-1 (Col sums) : ✓ Fixed. Mock 14 now = 25.

Example (BV-9B failure — section/subtopic names are illustrative):
  BV-9B (Batch coverage): ✗ [Section X]: 3 subtopics have 0 appearances in batch 2
                            Missing: ['[Subtopic A]', '[Subtopic B]', '[Subtopic C]']
                            → Re-generating batch 2 from scratch (BV-10 protocol)
```

### S9-10 — Failure response protocol (v1.24: stochastic vs structural)

```
Classify EVERY B2/B3 gate failure before responding:

STRUCTURAL (deterministic infeasibility — regeneration CANNOT help):
  Triggers: BV-10a form_key collision; and any constraint the §4-1b feasibility gate
  covers (mechanic uniqueness, rare-density BV-4-vs-BV-9B, mandate sums, column capacity).
  → Do NOT regenerate. HALT and surface the §4-1b diagnosis: offending key/members, the
    window, Σpresent vs cap·N_w, and the NAMED upstream fix (split/merge in Step 5, raise
    max_per_mechanic_per_mock, reduce quotas / merge subtopics). Terminates in ONE step.

STOCHASTIC (a bad random draw — regeneration CAN help): BV-1..BV-6, BV-9B imbalance.
  1. Fix internally; do NOT show the summary table or deliver blueprint.json.
  2. Re-generate the ENTIRE current batch from scratch (assigned[] counts are interconnected).
  3. Re-validate BV-1..BV-6 AND BV-9B; iterate.
  4. If unresolvable after 3 attempts → it is actually STRUCTURAL: run the §4-1b gate and
     HALT with its specific infeasibility + upstream fix. (BV-9B failing after 3 attempts ==
     EC-11 / §4-1b violation — now an ACTUAL code path, not advisory text.)

A ✗ in the summary table = Claude error (BV-0 prevents it). If user reports a ✗ in a
delivered table: acknowledge, fix entire batch, re-deliver.
```

### S9-11 — BV-9B: Batch coverage check (runs per B2 batch — Option C)

```
PURPOSE: Verify INVARIANT 8 — every PYQ subtopic appears ≥ 1 Q in this batch window.
Runs immediately after BV-1 to BV-6 pass, before delivery.

SCOPE: Only the mocks in the CURRENT batch (batch_start to batch_end).
A single B2 batch IS one complete batch window (10 mocks).
Last batch may be smaller — still treated as a single window.

```python
# batch_mocks = range(batch_start, batch_end + 1)  — the current B2 batch
# batch_num   = math.ceil(batch_start / batch_size)  — e.g., mocks 1-10 → batch 1

batch_num = math.ceil(batch_start / batch_size)

for section in sections:
    uncovered_subs = []
    for S in pyq_subtopics[section]:   # ALL PYQ subs (rare + nonrare)
        appearances_in_batch = sum(mock_alloc[S][m] for m in batch_mocks)
        if appearances_in_batch == 0:
            uncovered_subs.append((S, r_avg[S]))

    if uncovered_subs:
        uncovered_subs.sort(key=lambda x: x[1])   # sort by r_avg for readability
        fail(
            f"BV-9B FAIL [{section['name']}]: {len(uncovered_subs)} subtopic(s) have "
            f"ZERO appearances in batch {batch_num} (mocks {batch_start}-{batch_end}).\n"
            f"Uncovered: {[s for s, _ in uncovered_subs]}\n\n"
            f"FIX: Phase 0 pre-pass (§4-5) should have guaranteed coverage. "
            f"Re-generate this batch from scratch (BV-10 protocol)."
        )
```

BV-9B failure → same protocol as BV-1 to BV-6 failure (ref S9-10):
  Re-generate entire batch → re-validate → iterate until pass.
  BV-9B failing after 3 attempts = EC-11 feasibility violation (too many subtopics).

Print in B2 delivery summary:
  "BV-9B (Batch coverage): ✓ All [N] PYQ subtopics present in batch [K]
                              [Sec1Abbr]=[n]subs | [Sec2Abbr]=[n]subs | ... | [SecNAbbr]=[n]subs"
  (Section abbreviations derived dynamically from sections[].name — not hardcoded.
   Use short forms per §11-4: e.g. 'Quantitative Aptitude' → 'QA', 'Engineering Maths' → 'EM'.
   Number of pipe-separated entries = number of sections in the exam.)
  OR on failure:
  "BV-9B (Batch coverage): ✗ [section]: [n] subs missing — re-generating"
```

### S9-12 — BV-AXIS: axis schedule integrity + feasibility report (runs in B3)

```
PURPOSE (v1.23): verify blueprint['axis_schedule'] is present and well-formed for every
section, and REPORT axis feasibility. This gate is ADVISORY on the locked axes (Axis-1/3)
and on 'unsatisfiable'/'zp_only' guarantees — because Subtopic is hard #1, Blueprint cannot
force those; realized-vs-target proportion is audited within tolerance at Step 8. It HARD-FAILS
only on structural corruption (missing/malformed schedule), never on a format shortfall.

Absent-safe: if the manifest predates Step 5 v2.23, every section's schedule has
status='no_pyq' — BV-AXIS passes vacuously and prints "inert (no axis targets in manifest)".
```
```python
def bv_axis(blueprint, sections):
    sched = blueprint.get('axis_schedule')
    if sched is None:
        fail("BV-AXIS FAIL: blueprint['axis_schedule'] missing. S7-7 must build it in B1.")
        return
    inert = True
    report_lines = []
    REQUIRED = {'section', 'status', 'axis2_audit_mode', 'axis2_window_target',
                'axis2_guarantee', 'guarantee_feasibility', 'axis1_target_per_mock',
                'axis3_target_per_mock', 'negative_rate', 'mocks_per_window'}
    for section in sections:
        name = section['name']
        s = sched.get(name)
        if s is None:
            fail(f"BV-AXIS FAIL [{name}]: no axis_schedule entry for this section.")
            continue
        missing = REQUIRED - set(s.keys())
        if missing:
            fail(f"BV-AXIS FAIL [{name}]: axis_schedule missing keys {sorted(missing)}.")
            continue
        if s['status'] == 'no_pyq':
            continue
        inert = False
        # STRUCTURAL: band-mode Axis-2 window targets must be non-negative ints; guarantee list
        # entries must NOT also be DIRECT (DIRECT floats, never a guarantee).
        if 'DIRECT' in s['axis2_guarantee']:
            fail(f"BV-AXIS FAIL [{name}]: DIRECT appears in axis2_guarantee (it must float).")
        for cls, tgt in s['axis2_window_target'].items():
            if not isinstance(tgt, int) or tgt < 0:
                fail(f"BV-AXIS FAIL [{name}]: window target for '{cls}' is not a non-negative int ({tgt!r}).")
        # ADVISORY feasibility report (never fails the gate):
        unsat = [g for g, f in s['guarantee_feasibility'].items() if f == 'unsatisfiable']
        zponly= [g for g, f in s['guarantee_feasibility'].items() if f == 'zp_only']
        a1un  = s.get('axis1_unreachable_formats', [])
        report_lines.append(
            f"  {name}: bands={len(s['axis2_window_target'])} guarantees={len(s['axis2_guarantee'])}"
            + (f" | UNSATISFIABLE(absent,not-fabricated)={unsat}" if unsat else "")
            + (f" | zp_only(best-effort)={zponly}" if zponly else "")
            + (f" | axis1-unreachable={a1un}" if a1un else ""))
    if inert:
        print("BV-AXIS: ✓ inert (no axis targets in manifest — pre-v2.23 or all-Zero-PYQ).")
    else:
        print("BV-AXIS: ✓ axis_schedule well-formed. Feasibility report:")
        print("\n".join(report_lines))
        print("  (Axis-1/3 + zp_only/unsatisfiable are advisory — audited within tolerance at Step 8.)")
```

BV-AXIS runs in B3 alongside BV-7/BV-8 (S8-5 final validation). It never blocks delivery on a
format shortfall — only on a corrupt/missing schedule (a Blueprint bug, not an exam-data issue).

## §10 — MISSING DOCUMENT HANDLING

All fallback procedures when input documents are absent or incomplete.
Every fallback requires user confirmation before proceeding.
Every fallback is documented in Paper Structure sheet (Sheet 1 of blueprint.xlsx).

### S10-0 — Consolidated message protocol (MD-1 + MD-2)

```
If ANY document is missing or incomplete:

1. Claude lists ALL issues in ONE consolidated message:
   "Missing documents detected:
    ✗ [Doc name]: Impact = [what cannot be computed]
    ✗ [Doc name]: Impact = [what cannot be computed]

    Fallback plan:
    → [Doc A missing]: will use [fallback source] → [impact on accuracy]
    → [Doc B missing]: will use [fallback source] → [impact on accuracy]

    Please confirm to proceed with fallbacks,
    or provide the missing documents."

2. User must confirm explicitly.
   Valid confirmations: 'proceed', 'ok', 'yes', 'confirm', 'go ahead'
   Silence = NOT confirmation. Claude does not auto-proceed.

3. If user provides missing document after seeing the flag:
   User must start a FRESH CHAT after uploading.
   Project knowledge files are read ONCE at session start — mid-session uploads
   are NOT visible to Claude in the same session (ref §8-6).
   In the fresh chat: Claude re-reads all files and proceeds normally.
```

### S10-3 — Source priority matrix (MD-3)

```
When BOTH Analysis doc AND Excel are available:

  Subtopic names      : Analysis doc  > Excel  (Analysis doc is manually verified)
  Combined Q counts   : Analysis doc  > Excel
  Year-wise breakdown : Excel ONLY    (Analysis doc has no year-wise split)
  Trend data          : Excel ONLY
  Importance class    : Derived from r_avg (§3-6), which is computed from Excel year-wise data.
                        Not read directly from Excel — Excel provides raw input, §3 computes output.
  Format flags        : Excel ONLY    (Format column — Analysis doc has no Format data)
  n_papers            : Exam Pattern ONLY — not in Analysis doc or Excel.
                        Inferred if Exam Pattern missing (ref S10-4).

Both sources are complementary — not competing.
Use each for what it uniquely provides.

DATA QUALITY CHECK (v1.18):
  After reading Excel, if the '% of Subject' column values imply a denominator
  that differs from exam_config.total_questions or Exam Pattern total:
    This signals a data quality issue in Step 5's Frequency xlsx output.
    The % values were likely computed using the sum of MAPPED questions
    (incomplete) rather than the EXAM total (complete).
    Flag: "Frequency Excel % of Subject values appear to use [implied_denom]
           as denominator instead of exam total [exam_total]. This suggests
           Step 5 classification was incomplete. Review S2-3 Coverage
           Validation Gate results before proceeding."
    This is informational — S2-3's Coverage Validation Gate is the hard gate.
```

### S10-4 — Missing Exam Pattern (MD-4)

```
Inference from PYQ data:
  Section names : from Analysis doc headers / filenames / Excel Subject column
  Q count/section: inferred from Excel as:
    sec_qs[section] = round(Σ Avg/Paper[most_recent_year][S] for all S in section)
    (sum of per-subtopic averages for the most recent valid year, rounded to integer)
  Q ranges : assigned sequentially across sections:
    Section 1: Q1 to Q(sec_qs[1])
    Section 2: Q(sec_qs[1]+1) to Q(sec_qs[1]+sec_qs[2])
    etc.
  For multi-paper exams (n_papers > 1):
    Q ranges restart from Q1 for each paper.
    Document assumed paper structure in Paper Structure sheet.

Claude states inferred structure explicitly:
  "Exam Pattern missing. Inferred structure:
   Section 1: [name], [N] Qs, Q1–QN
   Section 2: [name], [M] Qs, QN+1–QN+M  ..."

User must confirm inferred structure before B1 proceeds.
Documented in Paper Structure sheet.
```

### S10-5 — Missing ALL Analysis docs (MD-5)

```
Fallback: use Frequency Excel Master Data sheet directly.
  Excel has Subject|Topic|Sub-Topic|year-wise data → sufficient for r_avg.
  Subtopic taxonomy: from Excel Sub-Topic column.
  r_avg proxy: compute pooled_avg[S] using §3-3 formula:
    pooled_avg[S] = Σ(Avg/Paper[yr] × Papers_In[yr]) / Σ(Papers_In[yr]) for all years
    (same as pooled_avg — no recency weighting since all years treated equally)
    Used directly as r_avg proxy for allocation.

Flag:
  "PYQ Analysis docs missing. Using Frequency Excel for subtopic taxonomy
   and frequency (no recency weighting). Confirm to proceed."

Accuracy impact: subtopic names may differ from IFAS standard; no recency weighting.
Documented in Paper Structure sheet.
```

### S10-6 — Missing ONE subject's Analysis doc (MD-6)

```
Other subjects: use Analysis docs normally.
Missing subject: fall back to Excel for that subject only.
  Excel subject tab or Master Data rows for that subject provide Topic|Sub-Topic structure.

  If Excel has rows but no Sub-Topic breakdown (Topic column only):
    → Use topic name as single subtopic (same as S2-2 topic-level fallback).
    → Flag: "Excel has topic-level only for [subject]. Using topic as subtopic."

  If Excel has 0 rows for this subject/section:
    → Equal distribution: quota[S] = sec_qs × N_mocks / len(syllabus_subtopics)
    → Claude asks: "No data for [subject] in Excel. Please provide subtopic list
                    OR confirm equal distribution across [N] subtopics."

Documented in Paper Structure sheet with impact note.
```

### S10-7 — Missing Frequency Excel (MD-7)

```
Recency weighting NOT possible (no year-wise breakdown).
Fallback: use Analysis doc combined Q counts directly as r_avg proxy.

  r_avg_proxy[S] = doc_combined_count[S]
  (Higher doc_count = higher frequency = more Qs allocated. Preserves relative
  frequencies across subtopics even without per-paper normalization.
  total_papers_estimate is NOT needed — use raw counts directly.)

Format flags unavailable from Excel.
  Claude infers Format from subtopic name keywords:
    FIGURAL : Mirror, Figural, Paper Fold, Embedded, Cube, Dice,
              Space Orientation, Non-Verbal, Nonverbal, Image
    PASSAGE : Cloze, Reading Comprehension, Passage, RC, Comprehension
    DI      : Data Interpretation, Bar Graph, Pie Chart, Line Graph,
              Table, Graph (standalone)
    TEXT    : all others (default)

  For EACH inferred non-TEXT format: state inference explicitly and ask:
    "Inferred FIGURAL for 'Mirror Image' based on name. Confirm? (yes/no)"

  No subtopic proceeds with unconfirmed non-TEXT Format.
  See §6-1 ALIASES dict for complete alias → Format mapping used during B1.

  CRITICAL — INFERRED FORMAT DOES NOT AFFECT ALLOCATION INCLUSION:
    After Format is confirmed (TEXT / FIGURAL / PASSAGE / DI), the subtopic
    is included in §4 allocation (if r_avg > 0) or §5 ZP rotation (if r_avg = 0).
    A confirmed FIGURAL subtopic is NEVER excluded from allocation.
    Format only tells Step 2 how to generate the question.
    Ref: §6 GOLDEN RULE — FORMAT IS CLASSIFICATION ONLY, NEVER EXCLUSION.

Flag:
  "Excel missing. Recency weighting not possible. Using Analysis doc Q counts
   as r_avg proxy. Format flags inferred from subtopic names — confirming each."

Documented in Paper Structure sheet.
```

### S10-8 — Missing BOTH Analysis docs AND Excel (MD-8)

```
Minimum viable input: at least ONE PYQ frequency source required.

Options for user:
  (a) Provide Analysis doc(s)
  (b) Provide Frequency Excel
  (c) Provide syllabus with subtopic list
      → Claude applies equal distribution:
        quota[S] = sec_qs × N_mocks / len(subtopics_in_section) for all S
        No ZP rotation (all subtopics treated as PYQ-based with equal r_avg=1.0).
        No recency weighting.

If none of the above: HALT.
  "Cannot generate blueprint without at least one PYQ frequency source.
   Please provide: Analysis doc(s), Frequency Excel, OR syllabus with subtopic list."
```

### S10-9 — Incomplete Analysis doc (MD-9)

```
Signal: doc covers fewer topics than expected for a major subject.
  Heuristic threshold: < 3 topics for any subject section = flag as potentially incomplete.
  This threshold is a heuristic — some exams legitimately have 1-2 topics per section
  (e.g. 'Current Affairs', 'General English'). Claude flags but user always confirms.
  The threshold is NOT configurable because it is advisory-only (never blocks B1).

Claude flags:
  "PYQ Analysis for [subject] appears incomplete.
   Found [N] topics. If topics are missing, allocation will be inaccurate.
   Confirm this is the complete doc, or provide additional data."

Claude does not know the 'correct' count — flags when doc seems sparse.
User confirms completeness.
If user says incomplete: wait for complete doc before proceeding.
```

### S10-10 — Missing Excel year column (MD-10)

```
Auto-handled — no user confirmation needed.
  Missing column → treat as 0 papers for that year (handled in §3-2 formula).
  That year contributes 0 to r_avg calculation.

Flagged in Paper Structure sheet:
  "Excel missing [year] column. Treated as 0 papers for that year."
```

### S10-11 — Partial Format column in Excel (MD-11)

```
If some subtopic rows have no Format value (blank cell):
  Claude flags each missing entry:
    "Format value missing for subtopic [X] in [section]."

Options:
  (a) User fills missing Format values → re-upload Excel → fresh chat
  (b) Claude infers from subtopic name using:
      - Name keyword matching (ref S10-7 inference keywords above)
      - §6-1 ALIASES dict for complete alias → Format mapping
      For EACH inferred non-TEXT value: ask user to confirm.
      Blank = TEXT assumed ONLY after user explicitly confirms.

No subtopic proceeds with unknown Format (consistent with §6-1 HALT rule).

CRITICAL — RESOLVING FORMAT DOES NOT AFFECT ALLOCATION INCLUSION:
  Once Format is resolved (by user input or confirmed inference), the subtopic
  is included in §4 allocation (if r_avg > 0) or §5 ZP rotation (if r_avg = 0).
  A subtopic with a blank Format cell is NEVER excluded from allocation.
  It is only held pending Format resolution — once resolved, it proceeds normally.
  Ref: §6 GOLDEN RULE — FORMAT IS CLASSIFICATION ONLY, NEVER EXCLUSION.
```

### S10-12 — All assumptions in Paper Structure sheet (MD-12)

```
Sheet 1 of blueprint.xlsx — 'Assumptions' section at bottom.
One row per assumption or fallback applied.

Columns:
  Category (human-readable) | Issue | Fallback Used | Impact on Accuracy

Examples:
  Missing Excel     | Frequency Excel not provided   | Pooled avg from Analysis doc  | No recency weighting
  Partial Format    | Format missing for 3 subtopics | Inferred + user-confirmed      | Low risk
  Duplicate subtop  | 'Mirror Image' appeared twice  | Q counts merged, kept once     | Negligible
  Section ranges    | Exam pattern ambiguous         | User-confirmed inferred ranges | None after confirmation
  Missing Analysis  | QA doc not provided            | Excel taxonomy used for QA     | Names may differ

Every fallback MUST have a corresponding assumption row.
Rows added in real time as B1 processes each input — not retrospectively.
```

## §11 — DELIVERY FORMAT

Exact content of each batch delivery. What Claude says, shows, and delivers.

### S11-1 — B1 delivery (BD-1)

```
After B1 completes (all steps 1-9 of §8-2 done with no unresolved HALTs),
Claude delivers in ONE response:

NOTE: B1 HALT resolutions (user confirming missing-doc fallbacks) do NOT trigger B2.
B2 starts ONLY after the B1 complete summary below is shown and user gives a fresh
affirmative ('continue', 'go', 'next', 'proceed', 'ok', 'yes').

PART A — Structure summary in chat:

  "=== B1 Complete — Blueprint Skeleton ===
   Exam         : [exam_name] ([ExamCode])
   Total Qs     : [total_qs] per mock
   Sections     : [N] sections
   ────────────────────────────────────────────────────
   Section              | Qs/mock | Subtopics | Zero-PYQ
   ────────────────────────────────────────────────────
   [Section 1 name]     | [N]     | [count]   | [count]
   [Section 2 name]     | [N]     | [count]   | [count]
   ...
   ────────────────────────────────────────────────────
   Total subtopics      : [N]
   Zero-PYQ subtopics   : [N] total across all sections
   Difficulty           : [25/25/50 default]
                         OR [E:M:H custom — e.g., 20/30/50]
                         OR [progressive — [N] bands:
                              M[s1]-M[e1]: [S/M/H], M[s2]-M[e2]: [S/M/H], ...]
   Format               : passage=[T/F] (Sections: [list or 'none'])
                          figural=[T/F] (Sections: [list or 'none'])
                          di=[T/F]      (Sections: [list or 'none'])
                         OR: All sections TEXT only
   BV-0A               : ✓ All [N] subtopics from Analysis doc accounted for
                          TEXT=[n] | FIGURAL=[n] | PASSAGE=[n] | DI=[n]
                          Silently excluded: 0 subtopics (none dropped).
   Assumptions          : [None]
                         OR:
                           • [Category]: [brief description]
                           • ...
   Batches remaining    : [ceil(N_mocks/10)] B2 batches + 1 B3
   ========================================="

PART B — Files via present_files (MANDATORY — call present_files with BOTH files in this exact order):
  1. [ExamCode]_blueprint.xlsx   (skeleton — Sheet 2 mock columns are EMPTY at B1)
  2. [ExamCode]_blueprint.json   (v1 — mocks[] = [] at this stage)

  CHECKLIST before calling present_files:
    ☐ blueprint.xlsx exists at /mnt/user-data/outputs/[ExamCode]_blueprint.xlsx
    ☐ blueprint.json exists at /mnt/user-data/outputs/[ExamCode]_blueprint.json
    ☐ blueprint.json mocks[] == []   (B1 must NOT pre-populate mocks)
    ☐ blueprint.json subtopic_list[] is populated (r_avg + format + answer_cardinality + answer_type for all subtopics)
    ☐ blueprint.json difficulty_schedule[] has exactly N_mocks entries
    ☐ blueprint.json zero_pyq_rotation has a key for every section (even if value=[])
  If any checklist item fails: HALT here. Fix before calling present_files.

NOTE on blueprint.xlsx at B1:
  Sheet 2 (Blueprint allocation grid) has subtopic rows but ALL mock columns are empty.
  Mocks are generated in B2. The FULL allocation grid is only available in B3 blueprint.xlsx.
  B1 xlsx lets the user verify subtopic list, r_avg values, ZP rotation,
  difficulty schedule, and Phase 0 audit data BEFORE committing to 50 mocks of allocation.

BATCH GATE: After present_files, this response ends. See §8-2 Step 9 BATCH GATE.
WAIT for user affirmative before B2 batch 1.
Valid: 'continue', 'go', 'next', 'proceed', 'ok', 'yes'
```

### S11-2 — B2 delivery (BD-2)

```
After each B2 batch, Claude delivers in ONE response:

Batch number K = ceil(batch_start / 10)
  (e.g., mocks 1-10 = Batch 1, mocks 11-20 = Batch 2, mocks 31-35 = Batch 4)

PART A — Summary table in chat:

  "=== B2 Batch [K] — Mocks [start]–[end] ===
   ─────────────────────────────────────────────────────────────
   Mock | [Sec1]  | [Sec2]  | ... | [SecN]  | Total | ✓/✗
   ─────────────────────────────────────────────────────────────
   M[N] | [N]     | [N]     | ... | [N]     | [total] | ✓
   M[N] | [N]     | [N]     | ... | [N]     | [total] | ✓
   ...
   ─────────────────────────────────────────────────────────────
   ✓ = per-mock BV checks passed (BV-1 col sums, BV-4 rare limit,
       BV-5 ZP count, BV-6 no negatives)
   ✗ = one or more checks failed (should never appear — BV-0 enforces this)"

  Number of section columns = number of sections in exam (not fixed at 4).
  Use short abbreviations for long section names if needed.
  All rows should be ✓. A ✗ = Claude error → fix entire batch immediately (BV-10).

  BV-2 (scheduled positions) and BV-3 (frequency warning) are batch-level,
  not per-mock. BV-9B (batch coverage) is also batch-level. Report them
  separately below the table:
    "BV-2 (Scheduled)      : ✓ No Phase 1 position violations in batch"
    "BV-3 (Freq warn)      : ⚠ [subtopic] tracking 35% off — monitoring"
    "BV-9B (Batch coverage): ✓ All [N] PYQ subtopics ≥ 1Q in batch [K]"

PART B — Updated blueprint.json via present_files
  Call present_files with EXACTLY ONE file:
    [ExamCode]_blueprint.json  (updated — contains all mocks generated so far including this batch)

  CHECKLIST before calling present_files:
    ☐ blueprint.json exists at /mnt/user-data/outputs/[ExamCode]_blueprint.json
    ☐ len(blueprint['mocks']) == batch_end   (all mocks up to this batch are present)
    ☐ BV-1 to BV-6 AND BV-9B passed for this batch
  If any checklist item fails: HALT. Fix before calling present_files.

  blueprint.xlsx is NOT re-delivered in B2 — the FINAL allocation-complete
  blueprint.xlsx is delivered only in B3. Do not include xlsx in B2 present_files call.

PART C — Upload instruction (MANDATORY — always include after present_files):
  "Download this blueprint.json. In your [ExamCode] project knowledge:
   delete the old blueprint.json and upload this new one.
   Then start a FRESH CHAT and type 'continue' to generate the next batch."

BATCH GATE: After PART C, this response ends. See §8-3 Step 8 BATCH GATE.
WAIT for user affirmative before next batch.
Valid: 'continue', 'go', 'next', 'proceed', 'ok', 'yes'
If user asks a question: Claude answers, then waits for affirmative.
```

### S11-3 — B3 delivery (BD-3)

```
After B3 validation and file generation (§8-5 Steps 3-9), Claude delivers:

PART A — Validation confirmation:
  "Final validation:
   BV-7 (Full series check) : ✓
   BV-8 (ZP final counts)   : ✓"

PART B — present_files with all 6 output files (MANDATORY — in this exact order):
  1. [ExamCode]_blueprint.xlsx          ← FINAL version with all mock allocations
  2. [ExamCode]_blueprint.json
  3. [ExamCode]_registry.json
  4. [ExamCode]_ExplainLearnings.md
  5. [ExamCode]_ExplainAuditLearnings.md
  6. [ExamCode]_mock_test_audit.py      ← audit script (Step 7 optional, Step 8 mandatory)

  CHECKLIST before calling present_files:
    ☐ All 6 files exist at /mnt/user-data/outputs/ with exact [ExamCode]-prefixed names
    ☐ blueprint.xlsx has Sheet 2 FULLY populated (all N_mocks mock columns filled)
    ☐ blueprint.json len(mocks[]) == N_mocks
    ☐ registry.json has correct exam_code and empty arrays
    ☐ Both .md files contain header line only (# [ExamCode] ... Learnings)
    ☐ mock_test_audit.py --self-test passed (13/13 PASS)
    ☐ BV-7 and BV-8 both passed
  If any checklist item fails: HALT. Fix before calling present_files.

PART C — Handoff message (concise):
  "Step 6 (MockBlueprint) complete for [ExamCode].

   Upload to [ExamCode] project knowledge:
     ✓ [ExamCode]_blueprint.json
     ✓ [ExamCode]_registry.json
     ✓ [ExamCode]_ExplainLearnings.md
     ✓ [ExamCode]_ExplainAuditLearnings.md
     ✓ [ExamCode]_mock_test_audit.py

   Keep locally (do NOT upload to project):
     [ExamCode]_blueprint.xlsx  ← review full allocation here

   Also required in [ExamCode] project (from Step 0 — PYQExtract):
     ✓ [ExamCode]_section_rules.md
     (If Step 0 is not yet complete, finish it first before Step 2.)

   After uploading all 6 files to [ExamCode] project knowledge:
   → Start MockCreate M1
     (in the [ExamCode] project)"
```

### S11-4 — Summary table format rules

```
Column widths: adjust to content; abbreviate long section names.
  Example: 'GI & Reasoning' → 'GI', 'Quantitative Aptitude' → 'QA'

Status column (✓/✗):
  ✓ = per-mock BV checks all passed:
        BV-1: column sums correct for this mock
        BV-4: rare Qs ≤ MAX_RARE_PER_MOCK per section in this mock
        BV-5: ZP cumulative count ≤ MAX_ZERO (cumulative)
        BV-6: no negative allocations in this mock
  ✗ = one or more per-mock checks failed (should NEVER appear — BV-0 prevents)

  BV-2 (Phase 1 positions), BV-3 (frequency warning), and BV-9B (batch coverage)
  are BATCH-level — reported separately below the table, not in the per-mock ✓/✗ column.

All rows ✓ = deliver without comment.
Any row ✗ = Claude error: acknowledge, fix entire batch, re-validate, re-deliver.

Table shows section-level TOTALS only.
Subtopic detail is NOT shown in chat — available in blueprint.json.
```

### S11-5 — Re-generate batch or re-run B3

```
User requests batch regeneration (before B3 OR after B3):
  "Re-generate mocks 11-20" or "Redo batch 2"

  Claude confirms:
    "Re-generating mocks 11-20. Prior allocations for these mocks will be replaced.
     Mocks 1-10 and any mocks beyond 20 remain unchanged."
  Proceeds with §8-7 procedure.
  Delivers new summary table + updated blueprint.json.
  BV-7 + BV-8 must re-pass in B3 before final files are re-delivered.

  If B3 was already completed (files previously delivered):
    After batch re-generation: re-run B3 → all 6 output files re-delivered.
    User must replace all 5 non-xlsx Step 1 files in [ExamCode] project knowledge:
    (blueprint.json, registry.json, ExplainLearnings.md, ExplainAuditLearnings.md,
     mock_test_audit.py)
    Do NOT delete section_rules.md — it is from Step 0 and is not regenerated by Step 1.

User requests B3 re-run (no batch changes):
  "Re-run BV-7" or "Re-run B3" or "Run final validation"

  Applies when blueprint.json is complete (len(mocks[]) == N_mocks) but user
  wants to re-verify without changing any allocations.

  Claude: "Re-running B3 final validation on existing blueprint.json."
  Runs §8-5 Steps 2-9 (quota/zp_slot recompute → BV-7 → BV-8 → generate files).
  Does NOT re-generate any B2 batches.
  If BV-7/BV-8 fail: identify failing mocks → user must re-generate that B2 batch first.
```

## §12 — REGISTRY SCHEMA

What B3 creates in [ExamCode]_registry.json.
Schema is fully determined at Step 1 — MockCreate (Step 2) never changes it.

### S12-1 — Universal fields (always present, every exam)

```json
{
  "exam_code"          : "[ExamCode]",
  "schema_version"     : "1.0",
  "mocks_completed"    : [],
  "papers_completed"   : [],
  "question_hashes"    : [],
  "stem_texts"         : [],
  "semantic_tuples"    : [],
  "semantic_usage"     : [],
  "exhausted_subtopics": {},
  "question_index"     : [],
  "image_phashes"      : [],
  "image_sources_used" : [],
  "session_log"        : [],
  "content_tracking"   : {}
}
```

```
exam_code      : matches ExamCode from trigger and blueprint.json exam_code
                 At Step 2 session start: verify blueprint["exam_code"] == registry["exam_code"]
                 Mismatch → halt immediately. Wrong registry for wrong exam.

schema_version : set at B3 time. Never changed during mock series.
                 Allows future framework upgrades to detect schema version.

mocks_completed: starts as []. Step 2 appends mock number after each mock is generated.
papers_completed: starts as []. v1.29 (C1). The GENERALISED paper-identity ledger shared by
                 mocks and every scoped tier: the generation step appends the paper_id
                 (mock = "MOCK:M0k"; scoped = "SUBJ:/TOPIC:/SUBTOPIC:...") after each paper.
                 Additive — mocks_completed is retained for backward-compatibility; a legacy
                 registry with only mocks_completed is auto-migrated (paper_ids back-filled)
                 by the scoped blueprint's registry loader.
semantic_usage: starts as []. v1.30. Generation-layer (B) per-use log; each entry
                 {subtopic_id, angle, values, paper_index} tracks cross-paper spacing for
                 the narrow-factual controlled-reuse gap. Additive; the L2 semantic_tuples
                 list is unchanged.
exhausted_subtopics: starts as {}. v1.30. Sticky, cross-tier {subtopic_id: {exhausted,
                 since_paper}} flags set when a narrow-factual subtopic drains its
                 (item x angle) universe; set-once, never cleared.
question_hashes: starts as []. Step 2 appends MD5 hashes of all questions.
stem_texts     : starts as []. Step 2 appends cleaned stem text for dedup.
semantic_tuples: starts as []. Step 2 appends (subtopic, approach, values) tuples.
question_index : starts as []. v1.12. Mock-tagged, one object per mock:
                 {mock, questions:[{q, subtopic_id, difficulty}, ...]}. Step 2 APPENDS one
                 object per mock (per-question subtopic_id + assigned Complexity); Step 3
                 re-syncs it BY KEY from the fixed docx (subtopic_id re-derived + cross-checked;
                 difficulty carried forward — it is not rendered in the paper). Step 6 joins
                 subtopic_id → blueprint.subtopic_list[] to render Subject/Topic/Subtopic/
                 Question Type, and reads difficulty as Complexity. Seeded here so Step 2 only
                 APPENDS (RS-9). Governed by Contract_QuestionMetadataIndex v1.0.
image_phashes  : starts as []. Step 2 appends perceptual hashes of generated figural images
                 for cross-mock dedup. Empty [] for text-only exams (harmless).
image_sources_used: starts as []. Step 2 appends source identifiers of figural images used.
                 Prevents reusing the same source image across mocks.
session_log    : starts as []. Step 2 appends one entry per mock session with timestamp
                 and generation metadata. Audit trail for the mock series.
content_tracking: starts as {}. Step 2 populates subfields (ga_facts_used, passage_topics,
                 vocab_words_used, idioms_used, grammar_rules_used, computer_facts,
                 numeric_seeds, analogy_schemes, cause_effect_domains, syllogism_domains,
                 option_sets, cloze_topics) as empty arrays on first mock, then appends
                 content items for cross-mock dedup. Subfields are universal content
                 categories — unused categories remain empty []. Step 2 creates subfields
                 lazily via setdefault(); Blueprint seeds only the empty dict {}.
```

### S12-2 — Conditional fields (added only when detected)

```python
# B3 reads passage_present and figural_present from blueprint.json (set by §6)

if blueprint['passage_present']:
    registry['rc_manifests'] = []
    # Step 2 populates: one entry per mock with passage_linked_qs and cloze_linked_qs

if blueprint['figural_present']:
    registry['figural_manifests'] = []
    # Step 2 populates: one entry per mock with figural Q numbers and image hashes

# di_present = True → NO additional field in registry
# DI questions use self-containment rule: each Q reprints the full data table
# in its own stem. No cross-mock manifest tracking needed.
# di_present stored in blueprint.json for Step 2 awareness only.
# Step 2 knows to use build_word_table() for DI questions.

# all_text_exam = True → no conditional fields at all
# registry has universal fields only
```

### S12-3 — Complete registry.json examples

```json
// Example 1: TEXT-only exam (e.g., pure MCQ GA exam)
{
  "exam_code"          : "IBPS_CLERK_GA",
  "schema_version"     : "1.0",
  "mocks_completed"    : [],
  "papers_completed"   : [],
  "question_hashes"    : [],
  "stem_texts"         : [],
  "semantic_tuples"    : [],
  "semantic_usage"     : [],
  "exhausted_subtopics": {},
  "question_index"     : [],
  "image_phashes"      : [],
  "image_sources_used" : [],
  "session_log"        : [],
  "content_tracking"   : {}
}

// Example 2: Exam with PASSAGE + FIGURAL (e.g., any exam with both formats)
{
  "exam_code"          : "[ExamCode]",
  "schema_version"     : "1.0",
  "mocks_completed"    : [],
  "papers_completed"   : [],
  "question_hashes"    : [],
  "stem_texts"         : [],
  "semantic_tuples"    : [],
  "semantic_usage"     : [],
  "exhausted_subtopics": {},
  "question_index"     : [],
  "image_phashes"      : [],
  "image_sources_used" : [],
  "session_log"        : [],
  "content_tracking"   : {},
  "rc_manifests"       : [],
  "figural_manifests"  : []
}

// Example 3: Exam with DI only (e.g., Data Interpretation focused)
{
  "exam_code"          : "[ExamCode]",
  "schema_version"     : "1.0",
  "mocks_completed"    : [],
  "papers_completed"   : [],
  "question_hashes"    : [],
  "stem_texts"         : [],
  "semantic_tuples"    : [],
  "semantic_usage"     : [],
  "exhausted_subtopics": {},
  "question_index"     : [],
  "image_phashes"      : [],
  "image_sources_used" : [],
  "session_log"        : [],
  "content_tracking"   : {}
}
// Note: di_present=True adds NO field to registry. Self-containment rule applies.
```

### S12-4 — Registry schema rules

```
# Note: RS rule numbers below are as used in this spec.
# Cross-reference to the separate Rules Word doc may show different numbering.

RS-5  : exam_code in registry must match blueprint.json exam_code.
         Step 2 verifies this at every session start.

RS-6  : schema_version set at B3. Never changed during mock series.

RS-7  : File name: [ExamCode]_registry.json. Matches ExamCode everywhere.

RS-8  : Registry is a SEPARATE file. Never embedded in blueprint.json.
         Different lifecycles:
           blueprint.json           : read-only after Step 1 (never modified by Steps 2–6)
           registry.json            : fully replaced after every Step 2 session
           ExplainLearnings.md      : appended after every Step 4 session
           ExplainAuditLearnings.md : appended after every Step 5 session

RS-9  : Registry schema fixed at Step 1 B3. Step 2 only ADDS entries to
         existing arrays and POPULATES subfields within content_tracking{}.
         Step 2 never adds new top-level fields (all top-level fields are
         seeded in the B3 template: exam_code, schema_version, mocks_completed,
         question_hashes, stem_texts, semantic_tuples, question_index,
         image_phashes, image_sources_used, session_log, content_tracking,
         and conditional rc_manifests / figural_manifests).
         content_tracking subfields (ga_facts_used, passage_topics, etc.) are
         created lazily by Step 2 via setdefault() — this is not a top-level
         addition and is permitted under RS-9.

RS-10 : Registry must be REPLACED (not appended) after every Step 2 session.
         User deletes old registry.json from project knowledge.
         User uploads new registry.json (output of Step 2 session).
         Never keep two registry versions.
         Never append to old registry.
         Failure to replace → G-DUP gate at Step 3 misses duplicates
         from skipped mock → dedup integrity compromised for entire series.
```

### S12-5 — How Step 2 populates the registry

```
This section is for reference — Step 2 executes these steps, not Step 1.

After each Step 7 (MockCreate) session completes:
  mocks_completed[]  : append mock number (e.g., append 5 after Mock 5)
  question_hashes[]  : append MD5 of every question stem
  stem_texts[]       : append cleaned stem text of every question
  semantic_tuples[]  : append (subtopic, approach, values) per question

  If rc_manifests[] exists in registry:
    append {mock: N, passage_linked_qs: [...], cloze_linked_qs: [...]}

  If figural_manifests[] exists in registry:
    append {mock: N, figural_qs: [...], image_hashes: [...]}

Step 2 then outputs the complete updated registry.json.
User replaces registry in project knowledge (RS-10).
Step 8 (MockCreateAudit) uses registry for G-DUP gate.
```

---

## §13 — OUTPUT FILES

All 6 files produced by Step 1. Naming, content, and destination.

### S13-1 — File naming convention

```
All 6 files use [ExamCode] as prefix. ExamCode = alphanumeric + underscore only.

[ExamCode]_blueprint.xlsx
[ExamCode]_blueprint.json
[ExamCode]_registry.json
[ExamCode]_ExplainLearnings.md
[ExamCode]_ExplainAuditLearnings.md
[ExamCode]_mock_test_audit.py

All written to: /mnt/user-data/outputs/
File names are FIXED at delivery — never rename after downloading.
File names encode ExamCode for exam_code cross-verification and session detection.

present_files usage across the pipeline:
  B1 : present_files(blueprint.xlsx skeleton, blueprint.json v1)
       (skeleton xlsx has empty mock columns; blueprint.json has mocks[]=[])
  B2 : present_files(blueprint.json updated)  ← one call per B2 batch
  B3 : present_files(all 6 final files)       ← ONE call with complete output
```

### S13-2 — blueprint.xlsx (human review only)

```
Purpose  : User reviews allocation correctness visually before Step 2 begins.
Sheets   : 5 sheets (ref §15 for exact column definitions)
Upload   : NOT uploaded to project knowledge (xlsx not readable by Claude)
           User keeps locally throughout mock series.
Content  : Subtopic list, difficulty schedule, Phase 0 verification (all at B1);
           full mock allocation grid added at B3.
Lifecycle: Two deliveries:
             B1 skeleton — Sheets 1,3,4,5 populated; Sheet 2 mock columns empty
             B3 final    — Sheet 2 fully populated with all mock allocations
           After B3 delivery: static reference document (no further updates).
```

### S13-3 — blueprint.json (authoritative — read-only after Step 1)

```
Purpose  : Claude reads this at every Step 7 (MockCreate) session start.
Authority: If blueprint.json and blueprint.xlsx ever conflict → JSON wins.
Upload   : YES — uploaded to [ExamCode] project knowledge.
Lifecycle: Read-only after Step 1. Steps 2–6 never modify it.
           If allocation needs to change: re-run Step 1. Replace all files.
```

### S13-4 — registry.json (empty template — Step 2 populates)

```
Purpose  : Dedup tracking across all mocks in the series.
Content  : Universal fields + conditional fields from Format flags (§12).
           All arrays = [] at Step 1.
Upload   : YES — uploaded to [ExamCode] project knowledge.
Lifecycle: Fully replaced after every Step 7 (MockCreate) session (RS-10).
           Step 2 outputs updated registry. User replaces in project.
```

### S13-5 — ExplainLearnings.md (empty template — Step 9 fills)

```
Content at Step 1:
  # [ExamCode] — [exam_name] MockExplain Learnings

  (nothing else — Step 9 fills content as sessions run)

  Example: # SSC_CGL_TIER1 — SSC CGL Tier 1 MockExplain Learnings

Purpose  : Stores exam-specific learnings from Step 9 (MockExplain) sessions.
           Cross-mock feedback on explanation quality patterns.
Upload   : YES — uploaded to [ExamCode] project knowledge.
Lifecycle: Appended by Step 9 as patterns accumulate. Never fully replaced.
```

### S13-6 — ExplainAuditLearnings.md (empty template — Step 10 fills)

```
Content at Step 1:
  # [ExamCode] — [exam_name] MockExplainAudit Learnings

  (nothing else — Step 10 fills content as sessions run)

  Example: # SSC_CGL_TIER1 — SSC CGL Tier 1 MockExplainAudit Learnings

Purpose  : Stores exam-specific learnings from Step 10 (MockExplainAudit).
           Cross-mock audit patterns and known failure modes.
Upload   : YES — uploaded to [ExamCode] project knowledge.
Lifecycle: Appended by Step 10 as audit patterns accumulate. Never fully replaced.
```

### S13-7A — mock_test_audit.py (auto-generated — Step 7 optional, Step 8 mandatory)

```
Purpose  : Automated gate-check script for mock test papers.
           Step 7 (MockCreate) uses it OPTIONALLY for per-batch self-audit.
           Step 8 (MockCreateAudit) requires it MANDATORILY (HARD STOP without it).
Content  : The CANONICAL v2.6 auditor, copied VERBATIM from the fenced python block
           in Framework_MockTestCreateAudit.md Appendix A (SINGLE SOURCE OF TRUTH).
           Full A-* gate catalogue + the --audit-state COMPLETION GATE (S5-1A, C1-C7)
           + a FIXTURE-BASED self-test (see AUDIT_SCRIPT_TEMPLATE below).
           The script reads blueprint.json and registry.json at RUNTIME — it does
           NOT hardcode any exam-specific values at generation time.
Upload   : YES — uploaded to [ExamCode] project knowledge.
Lifecycle: Generated once at B3. Read-only for the life of the mock series.
           If Step 6 is re-run: script is regenerated (with collision check).
           There is NO separate "upgrade" — the generated script IS the full canonical auditor.

COLLISION HANDLING (EC-D1, EC-D3):
  Before generating, check project knowledge for existing [ExamCode]_mock_test_audit.py.
  If an existing script is found, run its --self-test:
    If it PASSES the FIXTURE-BASED self-test (N/N, N >= 35, builds docx fixtures) →
      it is a working canonical auditor; replacing with a fresh copy is safe. Confirm.
    If it FAILS, is a CONSTANT-PRINT stub, or prints N < 35 →
      it is NOT a working auditor (the retired hollow MVP). REPLACE it with the
      canonical v2.6 auditor — this is never a downgrade (the MVP audited nothing).
  If no existing script found: generate without prompt.

UPGRADE PATH — RETIRED (v1.27):
  There is no longer a "minimum viable vs full" split. Step 6 generates the ONE
  canonical v2.6 auditor (Framework_MockTestCreateAudit.md Appendix A). The old
  13-gate MVP — whose self_test() was a CONSTANT print that executed no gate — is
  RETIRED; it enabled a false-clean Step-8 run (root cause:
  Framework_MockTestCreateAudit.md v2.6). Do NOT generate or accept it. Re-running
  Step 6 regenerates the canonical auditor (collision check above).

RUNTIME DEPENDENCIES (EC-B3):
  --self-test : never imports python-docx; prints gate count and exits.
  Full audit  : imports python-docx (installed in Step 7/8 environment via MANDATE 2).

DORMANT GATES (EC-B4):
  MSQ/NAT gates (A-MSQ-INSTR, A-NAT-NOOPT, A-NAT-INSTR, plus the Claude-side
  A-MSQ-KEY / A-NAT-ANSWER) are included in the canonical auditor but auto-skip at
  runtime when blueprint.json declares no multi/numerical subtopics. The fixture
  self-test exercises their catch/pass/dormant cases (they count toward N/N).

EXAM-AGNOSTIC GUARANTEE:
  The script template contains ZERO hardcoded exam values. All structural
  parameters (total_questions, sections, option labels, font name, difficulty
  labels) are read from blueprint.json and registry.json at runtime.
```

#### AUDIT_SCRIPT_TEMPLATE (canonical — single source of truth)

```
This section is the CANONICAL REFERENCE for how the audit script is generated.

SINGLE SOURCE OF TRUTH (v1.27):
  The canonical, exam-agnostic auditor lives in ONE place:
      Framework_MockTestCreateAudit.md   Appendix A   (v2.6+).
  It is the ONLY script Step 6 generates and the ONLY script Step 8 runs. It carries
  the full A-* gate catalogue, the --audit-state COMPLETION GATE (S5-1A, C1-C7 + on-
  disk evidence checks), and a FIXTURE-BASED self-test. The old MVP embedded in
  Framework_MockTestCreate.md Appendix A is RETIRED; that file now POINTS here.
  Keeping ONE copy prevents the 13/35/66 drift that enabled the false-clean.

CANONICAL_AUDITOR_SOURCE = Framework_MockTestCreateAudit.md, Appendix A (fenced python)
SELF_TEST_CONTRACT       = fixture-based, "SELF-TEST: N/N PASS", N >= AUTH_GATE_FLOOR (35)

At B3, Claude:
  1. Copies, VERBATIM, the fenced python block from Framework_MockTestCreateAudit.md
     Appendix A into [ExamCode]_mock_test_audit.py. No exam-specific substitution is
     needed (the script self-parameterises from blueprint/rules/manifest/registry).
  2. Runs: python3 [ExamCode]_mock_test_audit.py --self-test
     → MUST print "SELF-TEST: N/N PASS" with N >= 35 AND be fixture-based (canonical
       build prints 43/43). A constant-print "N/N PASS" is REJECTED.
     If output differs or is not fixture-based → HALT. Do not deliver. Regenerate.
  3. Includes in B3 present_files call alongside other 5 files.
```

### S13-7 — present_files delivery order

```
B3 delivers all 6 files in ONE present_files call (final delivery):
  1. [ExamCode]_blueprint.xlsx           ← FINAL version; user reviews allocation
  2. [ExamCode]_blueprint.json
  3. [ExamCode]_registry.json
  4. [ExamCode]_ExplainLearnings.md
  5. [ExamCode]_ExplainAuditLearnings.md
  6. [ExamCode]_mock_test_audit.py       ← audit script (Step 7 optional, Step 8 mandatory)

If any file fails to create: HALT. Do not deliver partial set.
All 6 must be present before calling present_files.

See S13-1 for B1 and B2 present_files calls (intermediate deliveries).
```

### S13-8 — Project upload instructions

```
After downloading all 6 files from B3:

Step A: Review blueprint.xlsx locally (human verification of full allocation).

Step B: Create [ExamCode] Claude project (if not already exists).

Step C: Upload to [ExamCode] project knowledge (5 Step-1 output files + 1 Step-0 file = 6 total; do NOT upload the xlsx):
          ✓ [ExamCode]_blueprint.json          ← Step 1 output
          ✓ [ExamCode]_registry.json           ← Step 1 output
          ✓ [ExamCode]_ExplainLearnings.md     ← Step 1 output
          ✓ [ExamCode]_ExplainAuditLearnings.md ← Step 1 output
          ✓ [ExamCode]_mock_test_audit.py      ← Step 1 output (Step 7 optional, Step 8 mandatory)
          ✓ [ExamCode]_section_rules.md        ← Step 0 output (PYQExtract)
        Do NOT upload: [ExamCode]_blueprint.xlsx (xlsx not readable by Claude in project knowledge)
        NOTE: section_rules.md must be present before MockCreate M1 is triggered.
        NOTE: mock_test_audit.py is the canonical v2.6 auditor (§13-7A) — one script,
              no "upgrade" step; Step 8 requires its FIXTURE-BASED self-test to pass.

Step D: Start fresh chat in [ExamCode] project.
        Minimum required before Step 2 can start:
          blueprint.json + registry.json + section_rules.md (from Step 0)
        Recommended: upload all 6 files at once.

Step E: Run: MockCreate M1
```

### S13-9 — Re-running Step 1 (replacing all files)

```
⚠ WARNING: Re-running Step 1 invalidates ALL prior Step 2–6 work for this ExamCode.
  Any mocks already generated in the [ExamCode] project must be discarded.
  All previously generated explanations, audit outputs, and sorted files
  based on the old blueprint are no longer valid.
  Only re-run Step 1 if you intend to start the entire mock series from scratch.

Procedure:
  1. Delete ALL old [ExamCode] files from project knowledge:
       blueprint.json, registry.json, ExplainLearnings.md, ExplainAuditLearnings.md,
       mock_test_audit.py
       section_rules.md (from Step 0 — delete only if Step 0 will also be re-run;
       if Step 0 is NOT being re-run, keep existing section_rules.md in project)
  2. Run Step 1 again → download all 6 new output files.
  3. Upload the 5 non-xlsx files to [ExamCode] project knowledge.
     (blueprint.xlsx stays local — do not upload)
  4. Start fresh chat session in [ExamCode] project.
     (Claude reads project files at session start — fresh chat required)

NEVER do partial replacement (e.g., only new blueprint.json with old registry).
Partial replacement risks schema mismatch between registry and blueprint.
All-or-nothing upload is required.
```

### S13-10 — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat delivery report or handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Upload / Replace / Use locally), and next-step reference.

Step 6 uses BOTH footer types:
  - F1 (amber) after B1 (2 files) and each B2 batch (1 file)
  - F2 (green) after B3 final delivery (6 files)
```

## §14 — BLUEPRINT JSON SCHEMA

Exact field definitions for blueprint.json. This is the contract between
Step 6 (MockBlueprint) and Step 7 (MockCreate).

### S14-1 — Top-level structure

```json
{
  "exam_code"           : "[ExamCode]",
  "exam_name"           : "[Exam Full Name]",
  "blueprint_version"   : "1.23",
  "n_papers"            : 1,
  "total_mocks"         : N,
  "total_questions"     : Q,
  "total_options"       : 4,
  "option_label"        : "1/2/3/4",
  "level"               : "Post Graduation",
  "medium"              : "English",
  "marking_scheme"      : [{"q_range":[1,20],"question_type":"MCQ","correct_marks":2,"negative_marks":-0.5}],
  "passage_present"     : true,
  "figural_present"     : true,
  "di_present"          : false,
  "multi_present"         : false,
  "multi_select_allowed": false,
  "nat_present"         : false,
  "nat_allowed"         : false,
  "nat_contract"        : {"nat_answer_type": "real", "nat_tolerance": "0",
                           "nat_instruction": "Enter your answer as a numerical value."},
  "q_types"             : "['MCQ']",
  "msq_contract"        : {"msq_k_mode": "n/a", "msq_k": "none",
                           "msq_instruction": "(One or more options may be correct)",
                           "msq_instruction_hi": "(एक या अधिक विकल्प सही हो सकते हैं)",
                           "negative_marking_by_type": {}, "partial_credit": false},
  "difficulty_labels"   : ["Easy", "Medium", "Hard"],
  "sections"            : [...],
  "subtopic_list"       : [...],
  "difficulty_schedule" : [...],
  "axis_schedule"       : {...},
  "zero_pyq_rotation"   : {...},
  "mocks"               : [...]
}
```

```
exam_code           : str  — alphanumeric + underscore (from trigger)
exam_name           : str  — human-readable exam name (from exam_config or Exam Pattern doc)
blueprint_version   : str  — the blueprint.json SCHEMA version (the subtopic_id + paper_id
                     contract level), NOT the Framework_Blueprint spec-FILE version. Currently
                     "1.23". Step 7 GATES on it: MIN_BLUEPRINT_VERSION = (1, 7) (subtopic_id
                     floor) — a blueprint_version below 1.7 hard-stops generation. The SCOPED
                     blueprint emits this SAME value (it produces this same §14 schema), so both
                     must stay in sync. Bump only on a real blueprint.json schema change (not on
                     every spec-file bump), and update mock + scoped together.
n_papers            : int  — number of distinct papers in this exam's structure
                     (e.g., 1 for single-paper exam; 2 for two-paper exam)
                     This blueprint describes ONE paper's section structure only.
                     Multi-paper exams use one blueprint per paper.
                     (v1.8: MSQ presence is per-paper — each paper's blueprint carries
                      its own multi_present/multi_select_allowed.)
total_mocks         : int  — N_mocks from trigger
total_questions     : int  — total Qs per mock for this paper (Σ sec_qs in sections[])
total_options       : int  — number of options per Q (e.g. 4 for most MCQ exams).
                     Read from Step 5 auto-detected n_choices (CATEGORY C _meta field).
                     Default: 4. Step 7 reads via bp.get('total_options', 4).
                     SYNC: Step 7 uses this for num_options throughout generation.
                     Without this field, Step 7 always defaults to 4 — wrong for
                     5-option exams (UPSC CSP) or 2-option exams.
option_label        : str  — option numbering convention for this exam.
                     Read from section_rules.md option_label_format field (Step 5).
                     Examples: "1/2/3/4" | "A/B/C/D" | "(1)/(2)/(3)/(4)" | "(a)/(b)/(c)/(d)".
                     Carried in blueprint.json for visibility/parity (same pattern as
                     msq_contract). Step 7 reads the AUTHORITATIVE value from
                     section_rules.md R10 (option_label_format), not from this field.
                     SYNC: Step 7 get_option_labels() normalises the value to "N." format.
level               : str  — v1.19. Academic level from exam_config.json Overview tab.
                     "Graduation", "Post Graduation", "Under Graduation", "School".
                     Step 7 uses for question complexity calibration.
                     Step 9 uses for explanation depth. Default: "unknown".
medium              : str  — v1.19. Exam language from exam_config.json Overview tab.
                     "English", "Hindi", "Bilingual", etc.
                     Authoritative source — section_rules 'language' is PYQ validation.
                     Default: "unknown".
marking_scheme      : list — v1.19. Per-range scoring rules from exam_config.json.
                     Each entry: {q_range:[start,end], question_type:str,
                     correct_marks:float, negative_marks:float}.
                     Steps 7/8/9 use for per-Q-position marks/type lookup.
                     Empty list [] when exam_config absent (legacy).
passage_present     : bool — True if any subtopic has Format=PASSAGE
figural_present     : bool — True if any subtopic has Format=FIGURAL
di_present          : bool — True if any subtopic has Format=DI
multi_present         : bool — v1.8. True iff any subtopic has answer_cardinality=="multi".
                     Step 2 reads it to enable the MSQ generation path. Forced False
                     when multi_select_allowed=false (dormant guarantee).
multi_select_allowed: bool — v1.8. Copied verbatim from section_rules EXAM_STRUCTURE
                     (Step 0). Master gate for the entire MSQ contract.
q_types             : str  — v1.8. Copied from section_rules EXAM_STRUCTURE,
                     e.g. "['MCQ']" or "['MCQ','MSQ']".
msq_contract        : dict — v1.8; +msq_instruction v1.10.1. {msq_k_mode, msq_k,
                     msq_instruction, msq_instruction_hi, negative_marking_by_type,
                     partial_credit}, copied verbatim from section_rules EXAM_STRUCTURE.
                     Step 2 reads k-mode/k to bound the correct set; Step 4 reads marking;
                     msq_instruction is the localized select-instruction (parallel to
                     nat_contract.nat_instruction — Step 2/3 read it from section_rules, it
                     is mirrored here for visibility). All values inert when
                     multi_select_allowed=false.
nat_present         : bool — v1.10. True iff any subtopic has answer_type=="numerical".
                     Step 2 reads it to enable the NAT generation path. Forced False
                     when nat_allowed=false (dormant guarantee).
nat_allowed         : bool — v1.10. Copied verbatim from section_rules EXAM_STRUCTURE
                     (Step 0). Master gate for the entire NAT contract.
nat_contract        : dict — v1.10. {nat_answer_type, nat_tolerance, nat_instruction},
                     copied verbatim from section_rules EXAM_STRUCTURE. Step 2 reads the
                     answer model (integer⇒exact, real⇒tolerance band) + instruction; Step 4
                     reads it to render ca_range. All values inert when nat_allowed=false.
difficulty_labels   : list — v1.12. Canonical Complexity vocabulary, copied verbatim from
                     section_rules EXAM_STRUCTURE.difficulty_labels (default
                     ['Easy','Medium','Hard']). This is the stored/rendered value in
                     registry.question_index (§12). Fixed alias to the difficulty_schedule
                     COUNT keys: simple→Easy, medium→Medium, hard→Hard. Step 2 assigns each
                     question's difficulty from THIS set; Step 6 renders it as Complexity.
                     Overriding the label CARDINALITY (a 2- or 5-band set) also requires the
                     S7-5 schedule generator to emit matching bands — out of scope here; the
                     default 3-band set is fully supported. (Contract_QuestionMetadataIndex v1.0.)
sections[]          : static section definitions — does not change per mock
subtopic_list[]     : one entry per subtopic across all sections.
                     Fields: {subtopic_id (str), section (str), topic (str),
                              subtopic (str), r_avg (float 4dp), format (str),
                              type (str), answer_cardinality (str), answer_type (str)}
                     subtopic_id (v1.7): copied verbatim from Step 0's
                       subtopic_manifest.json — the cross-step join key.
                     answer_cardinality (v1.8): single|multi, copied verbatim from
                       section_rules CATEGORY B. The Step 2 DISPATCH unit. Whole-subtopic
                       mode ⇒ the per-mock allocation schema is unchanged (no MSQ split
                       inside subtopic_allocations). Defaults to 'single'.
                     answer_type (v1.10): option|numerical, copied verbatim from
                       section_rules CATEGORY B. The NAT dispatch axis (orthogonal to
                       answer_cardinality). Whole-subtopic mode ⇒ allocation schema
                       unchanged. Defaults to 'option'.
                     Source of truth for r_avg used by B2 to recompute quota[S].
                     Populated in B1. Read-only after B1.
difficulty_schedule[]: one entry per mock, length = total_mocks
                     (v1.8: unchanged — MSQ inherits its subtopic's difficulty; the MSQ
                      cognitive-load term is applied in Step 0 E-9, not here.)
zero_pyq_rotation{} : alphabetical ZP rotation order per section
mocks[]             : one entry per mock; empty [] after B1; B2 appends
```

### S14-2 — sections[] — top-level section definitions

```json
"sections": [
  {
    "name"        : "[Section 1 Name]",
    "q_range"     : [1, N1],
    "total_qs"    : N1,
    "max_attempt" : N1
  },
  {
    "name"        : "[Section 2 Name]",
    "q_range"     : [N1+1, N1+N2],
    "total_qs"    : N2,
    "max_attempt" : N2
  },
  {
    "name"        : "[Section 3 Name]",
    "q_range"     : [N1+N2+1, N1+N2+N3],
    "total_qs"    : N3,
    "max_attempt" : N3
  }
]
```
NOTE: Section names and Q-ranges are read from exam_config.json (v1.19 primary) or
the exam's PYQ pattern (legacy fallback). Section names are OTS display labels, NOT
taxonomy Subject names (see S2-1). They are NEVER hardcoded in this spec. The example
above shows a 3-section exam structure; actual section count and names vary by exam
(1–8 sections observed across competitive exams).

```
Ordered by q_range start ascending (Q1 section first).
q_range     : [start_inclusive, end_inclusive]
total_qs    : total questions in this section (from exam pattern / exam_config)
max_attempt : v1.19. Max questions student may attempt in this section. From
              exam_config.json. When max_attempt == total_qs: no attempt limit.
              The framework generates ALL total_qs questions per section regardless.
              max_attempt is OTS platform metadata — NOT consumed by Steps 7-11 for
              question generation or blueprint allocation.
              Default: total_qs (when exam_config absent or field missing).

Note: sections[] describes THIS paper's structure only.
For multi-paper exams, each paper has its own blueprint with its own sections[].
```

### S14-3 — difficulty_schedule[] — one entry per mock

```json
"difficulty_schedule": [
  {"mock": 1,   "band": "Standard", "simple": S1, "medium": M1, "hard": H1},
  {"mock": 2,   "band": "Standard", "simple": S2, "medium": M2, "hard": H2},
  ...
  {"mock": N,   "band": "Standard", "simple": SN, "medium": MN, "hard": HN}
]
```
NOTE: simple+medium+hard must equal total_questions for every entry.
Values are computed by Step 1 §7 difficulty allocation — never hardcoded.
N = total_mocks (from blueprint trigger), Q = total_questions (from Step 0 auto-detect).

```
Length must equal total_mocks.
No compression — even if all mocks identical, each gets an explicit entry.
mock   : int (1 to N_mocks)
band   : str — "Standard" for default/uniform difficulty.
               For progressive mode: user-defined band name from S7-3
               (e.g., "Warm-Up", "Standard", "Intensive").
simple : int (≥ 0)
medium : int (≥ 0)
hard   : int (≥ 0)
simple + medium + hard == total_questions for every entry.
```

### S14-3b — axis_schedule{} — one entry per section (v1.23, THREE-AXIS)

```json
"axis_schedule": {
  "[Section Name]": {
    "section": "[Section Name]",
    "status": "ok",
    "axis1_per_paper": {"TEXT": 18.0, "FIGURAL": 2.0},
    "axis2_per_paper": {"DIRECT": 12.0, "MATCH": 4.0, "ASSERTION_REASON": 3.0, "SEQUENCE": 0.05},
    "axis3_per_paper": {"MCQ": 20.0},
    "axis2_audit_mode": {"DIRECT": "float", "MATCH": "band", "ASSERTION_REASON": "band", "SEQUENCE": "guarantee"},
    "axis2_window_target": {"MATCH": 40, "ASSERTION_REASON": 30},
    "axis2_guarantee": ["SEQUENCE"],
    "guarantee_feasibility": {"SEQUENCE": "pyq_covered"},
    "axis1_target_per_mock": {"TEXT": 18, "FIGURAL": 2},
    "axis3_target_per_mock": {"MCQ": 20},
    "axis1_unreachable_formats": [],
    "negative_rate": 0.12,
    "mocks_per_window": 10,
    "recent_years": [2025, 2024, 2023]
  }
}
```
```
Built by Step 1 §7 (S7-7 derive_axis_schedule) from the Step-5 v2.23 manifest
axis_distribution + per-subtopic axis2_capability. One entry per section. NEVER hardcoded.

status                 : "ok" (PYQ observed) | "no_pyq" (all-Zero-PYQ section — feature inert).
axis{1,2,3}_per_paper  : 3-year per-paper class averages (the raw target). Consumed by Step 8 audit.
axis2_audit_mode       : per Axis-2 class — "band" | "guarantee" | "float". DIRECT is always float.
axis2_window_target    : band-mode classes only → per-window (mocks_per_window) integer quota.
                         The Step-7 quota + the Step-8 ±1/±15%-per-window tolerance target.
axis2_guarantee        : guarantee-mode classes (window_target < 1) → must appear ≥1 per window.
guarantee_feasibility  : per guarantee class — "pyq_covered" (Option-C batch coverage already
                         guarantees a capable subtopic every window; no allocation action),
                         "zp_only" (best-effort via ZP rotation + Step 7), or "unsatisfiable"
                         (no capable subtopic → absent; Step 7 must NEVER fabricate it).
axis1_target_per_mock  : Axis-1 (stimulus) per-mock counts (sum == sec_qs). Soft-steer + Step-8 audit.
axis3_target_per_mock  : Axis-3 (mechanism) per-mock counts (sum == sec_qs). Soft-steer + Step-8 audit.
axis1_unreachable_formats : advisory — Axis-1 target names formats with no PYQ subtopic (shortfall
                         accepted; audited within tolerance). Usually [].
negative_rate          : per-section 3-year negative-polarity rate (soft target; Step 7 nudge, Step 8 WARN).
mocks_per_window       : window size for guarantee/tolerance (= batch_size_qs, default 10).
```

### S14-4 — zero_pyq_rotation{} — alphabetical rotation order

```json
"zero_pyq_rotation": {
  "[Section 1 Name]": [
    "[ZP Subtopic A]",
    "[ZP Subtopic B]",
    "[ZP Subtopic C]"
  ],
  "[Section 2 Name]": [],
  "[Section 3 Name]": [],
  "[Section 4 Name]": [
    "[ZP Subtopic D]"
  ]
}
```
NOTE: Keys are section names — must match sections[].name EXACTLY.
Values are alphabetically sorted Zero-PYQ subtopic names for that section.
Populated by Step 1 §5. All values read from section_rules.md — never hardcoded.

```
Key   : section name — must match sections[].name EXACTLY (case and spaces).
Value : alphabetically sorted array of zero-PYQ subtopic names for that section.
        Empty [] if section has no zero-PYQ subtopics.

REQUIRED: every section in sections[] must have a corresponding key in
zero_pyq_rotation{}, even if its value is [].
A missing section key = blueprint corruption (B2 will KeyError).

Used by B2/B3 to recompute rotation schedule and by Step 2 to verify
rotation order is maintained across the mock series.
```

### S14-5 — mocks[] — one entry per mock

```json
"mocks": [
  {
    "mock"    : 1,
    "paper_id": "MOCK:M01",
    "sections": [...]
  },
  {
    "mock"    : 2,
    "paper_id": "MOCK:M02",
    "sections": [...]
  }
]
```

```
Ordered ascending (mock 1 first, mock N last).
mocks[] = [] after B1. B2 batches append objects to this array.
len(mocks[]) == total_mocks when all B2 batches are complete.
mock     : int — 1-based mock number (retained; Steps 7-11 read it).
paper_id : str — v1.29 (C1). Universal paper identity = "MOCK:M{mock:02d}". Additive: the
           generalised (paper_id) generation path and the shared registry key on this; the
           scoped blueprint emits the same field with SUBJ:/TOPIC:/SUBTOPIC: prefixes.
```

### S14-6 — section object within each mock

```json
{
  "section_name"         : "[Section 1 Name]",
  "q_range"              : [1, N1],
  "total_qs"             : N1,
  "subtopic_allocations" : [...],
  "validation"           : {
    "sum"      : N1,
    "expected" : N1,
    "status"   : "pass"
  }
}
```

```
section_name         : matches sections[].name exactly
q_range              : same as sections[].q_range (repeated for self-containment)
total_qs             : same as sections[].total_qs (repeated for self-containment)
subtopic_allocations : list of subtopic allocation objects — see S14-7
validation.sum       : Σ q_count across all stored subtopic_allocations
                       (includes ZP subtopic q_count when it appears)
validation.expected  : must equal total_qs
validation.status    : always "pass" — a failing mock is never stored (BV enforces this)
```

### S14-7 — subtopic_allocation object

```json
{
  "subtopic_id": "[section].[topic].[subtopic_slug]",
  "topic"   : "[Topic Name]",
  "subtopic": "[Subtopic Display Name]",
  "q_count" : 3,
  "format"  : "TEXT",
  "type"    : "pyq_based"
}
```

```
subtopic_id : str — v1.7 CROSS-STEP JOIN KEY. Copied VERBATIM from Step 0's
                 [ExamCode]_subtopic_manifest.json. Step 1 NEVER mints its own id.
                 This is the field Step 2 joins on (not the display name).
                 If a subtopic has no id in the manifest → HARD STOP (contract
                 gate S2-MANIFEST), never emit a guessed id.
topic   : str  — parent topic name (English)
subtopic: str  — subtopic DISPLAY name (English). Decorative — Step 2 does NOT
                 join on this; it joins on subtopic_id. May differ cosmetically
                 from the manifest display_name without breaking the pipeline.
q_count : int  — always > 0. Subtopics with q_count=0 are NOT stored.
                 Step 2 infers q_count=0 for any subtopic absent from the list.
format  : str  — one of: "TEXT" | "FIGURAL" | "PASSAGE" | "DI"
type    : str  — "pyq_based" or "zero_pyq"

NOTE: r_avg is NOT stored in subtopic_allocation objects.
r_avg is stored ONCE per subtopic in subtopic_list[] at the top level.
Step 2 reads r_avg from subtopic_list[] when needed.
This avoids redundant storage across potentially thousands of allocation objects
in a large mock series.
```

### S14-8 — Field types and conventions

```
All field names   : snake_case (no camelCase, no PascalCase)
All string values : English only (no Hindi, no regional language)
q_count           : integer only (never float)
r_avg             : float with 4 decimal places via round(x, 4).
                   JSON serialization may omit trailing zeros
                   (1.3 and 1.3000 are equivalent; both accepted).
                   Step 2 must NOT assume exactly 4 decimal digits in JSON.
q_range           : [start_int, end_int] inclusive (both integers)
bool fields       : true / false (JSON lowercase)
JSON encoding     : UTF-8, no BOM
Indentation       : 2 spaces
Key ordering      : as defined in S14-1 to S14-7.
                   Python 3.7+ preserves dict insertion order in json.dumps().
                   Consistent key order across all mocks aids human readability.
```

## §15 — XLS SHEET STRUCTURES  ← LOCKED SPEC — PERMANENT RULES

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  LOCKED SPECIFICATION — DO NOT DEVIATE                                       ║
║                                                                              ║
║  blueprint.xlsx MUST have EXACTLY these 5 sheets in this EXACT ORDER:       ║
║    Sheet 1 : "Paper Structure"                                               ║
║    Sheet 2 : "Blueprint"                                                     ║
║    Sheet 3 : "Summary Stats"                                                 ║
║    Sheet 4 : "Difficulty Schedule"                                           ║
║    Sheet 5 : "Phase 0 Verification"                                          ║
║                                                                              ║
║  Any deviation from sheet names, sheet order, or column structure           ║
║  defined below = CRITICAL ERROR. Verify against §15-CHECKLIST before        ║
║  calling present_files.                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### S15-0 — Color coding (applies to all sheets)

```
Section row colors (background of data rows):
  Section 1 : Light Blue   #DEEAF1
  Section 2 : Light Green  #E2EFDA
  Section 3 : Light Orange #FCE4D6
  Section 4 : Light Purple #EAE3F7
  Section 5+: cycle (Blue → Green → Orange → Purple → ...)

Section header rows (the merge row labelling the section block):
  Section 1 : Dark Blue   #1F4E79  + white bold text
  Section 2 : Dark Green  #375623  + white bold text
  Section 3 : Dark Orange #833C00  + white bold text
  Section 4 : Dark Purple #4B2C8A  + white bold text
  Section 5+: cycle

Zero-PYQ rows   : Yellow-cream  #FFF2CC + italic font
Column header   : Dark Navy     #1F4E79 + white bold 10pt + center-aligned
Sheet title row : Left-aligned, Dark Blue font, 13-14pt bold — no fill

Freeze panes:
  Sheet 2 (Blueprint): freeze at F2 (row 1 + cols A–E always visible)
  Sheet 3 (Summary Stats): freeze at A2
  Sheet 4 (Difficulty Schedule): freeze at A2
  Sheet 5 (Phase 0 Verification): freeze at A7
```

### S15-1 — Sheet 1: Paper Structure

```
Sheet name (EXACT): "Paper Structure"

Content (top to bottom):
  Row 1  : Title — "[ExamCode] — Blueprint Paper Structure"
            Font: bold, 13pt, Dark Blue. Left-aligned. No fill.

  Rows 3–12 (approx): Metadata key-value pairs
    Key column (A): bold, grey fill (#F2F2F2)
    Value column (B): normal font, merged B:C
    Keys (in order):
      Exam Code | Exam Name | Total Mocks | Total Qs/Mock | n_papers
      PYQ Data  | Difficulty | passage_present | figural_present | di_present

  Section table (after metadata block):
    Header row: Section | Qs/Mock | Subtopics (PYQ) | Zero-PYQ
    One data row per section (section row color per S15-0)
    No "Q range" column in this table (that is optional internal data)

  Assumptions block (below section table):
    Header: "Assumptions" in bold Dark Blue font
    One row per assumption applied during B1 processing
    If no assumptions: omit block (do not write "None")

Column widths: A=38, B=28, C=16
```

### S15-2 — Sheet 2: Blueprint  ← MAIN ALLOCATION GRID

```
Sheet name (EXACT): "Blueprint"

THIS IS THE PRIMARY DELIVERABLE SHEET. Claude MUST generate it at BOTH B1 and B3.
  At B1 (skeleton): subtopic rows fully populated; mock columns M1…MN are BLANK.
  At B3 (final):    mock columns M1…MN fully populated from blueprint.json mocks[].

Row 1 — Column headers (EXACT names, EXACT order):
  A         : "Subject"
  B         : "Topic"
  C         : "Sub-Topic"
  D         : "Format"
  E         : "r_avg"
  F         : "M1"
  G         : "M2"
  ...
  F+N-1     : "M[N_mocks]"

  Total columns = 5 + N_mocks.
  Example for N_mocks=50: 55 columns, last mock col = BD.

Freeze panes: F2  (row 1 visible always; cols A–E visible always while scrolling right)

Section block structure (repeat for each section in q_range order):
  ┌─ Section header row ───────────────────────────────────────────┐
  │  Cols A–E merged. Label: "[Section Name] — [sec_qs] Q/mock"   │
  │  Fill: dark section color (S15-0). Font: white bold.           │
  │  Mock columns: same dark fill, no text.                        │
  └────────────────────────────────────────────────────────────────┘
  ┌─ PYQ subtopic rows (sorted by r_avg DESCENDING) ──────────────┐
  │  Col A : full section name (e.g., "[Section 1 Full Name]")      │
  │          — light section fill (S15-0)                           │
  │  Col B : topic name                                            │
  │  Col C : subtopic name                                         │
  │  Col D : format value (TEXT / FIGURAL / PASSAGE / DI)         │
  │  Col E : r_avg value (4 decimal places, center-aligned)        │
  │  Col F+ : q_count per mock (integer ≥ 0; blank if 0)          │
  │  Row fill: white (no section fill on data rows except Col A)   │
  └────────────────────────────────────────────────────────────────┘
  ┌─ Zero-PYQ subtopic rows (sorted ALPHABETICALLY) ──────────────┐
  │  Same columns as PYQ rows.                                     │
  │  r_avg = 0.0000                                                │
  │  q_count = 1 for assigned mock, blank for all others           │
  │  Row fill: yellow-cream #FFF2CC. Font: italic.                 │
  └────────────────────────────────────────────────────────────────┘

IMPORTANT — blank vs zero in mock columns:
  Write NOTHING (None/blank) for q_count = 0. Do NOT write the digit 0.
  Write the integer for q_count > 0.
  This keeps the grid readable — only positive allocations are visible.

Column widths: A=36, B=30, C=42, D=10, E=8; mock cols M1…MN = 4 each
```

### S15-3 — Sheet 3: Summary Stats

```
Sheet name (EXACT): "Summary Stats"

Row 1 — Title (optional, left-aligned, bold Dark Blue)

Row 2 — Column headers (EXACT names, EXACT order — 12 columns):
  A  : "Subject"
  B  : "Topic"
  C  : "Sub-Topic"
  D  : "Format"
  E  : "Type"                     ← "PYQ-based (High)", "PYQ-based (Medium)", "PYQ-based (Low)",
                                     or "Zero-PYQ"  (matches §3-6 label definitions exactly)
  F  : "r_avg (Recency)"         ← 4 decimal places
  G  : "Pooled Avg"               ← simple combined avg from §3-3, reference only
  H  : "Total PYQs"               ← Σ(Avg/Paper[yr] × Papers_In[yr]) all years
  I  : "Quota (Target Qs)"        ← quota[S] from §4-2
  J  : "Actual Qs"                ← Σ q_count across all mocks from blueprint.json
  K  : "Accuracy%"                ← signed: (Actual−Target)/Target×100, shown as "−3.9%"
  L  : "Mocks Appeared"           ← count of mocks where q_count > 0

Sort order:
  Within each section: PYQ subs sorted by r_avg DESCENDING, ZP subs at bottom ALPHABETICALLY.
  Section order: same as exam pattern q_range order.

Section blocks: same structure as Sheet 2 (section header row + data rows).
Column A fill: light section color per S15-0.
ZP rows: yellow-cream fill #FFF2CC + italic.

Column widths: A=36, B=28, C=42, D=14, E=22, F=14, G=14, H=14, I=18, J=14, K=14, L=18
```

### S15-4 — Sheet 4: Difficulty Schedule

```
Sheet name (EXACT): "Difficulty Schedule"

Row 1 — Column headers (EXACT names, EXACT order — 6 columns):
  A : "Mock"
  B : "Band"
  C : "Easy ([S]%)"      e.g., "Easy (15%)"  ← substitute actual S% from difficulty flag
  D : "Medium ([M]%)"    e.g., "Medium (30%)" ← substitute actual M% from difficulty flag
  E : "Hard ([H]%)"      e.g., "Hard (55%)"   ← substitute actual H% from difficulty flag
  F : "Total"
  For default difficulty (25:25:50): headers are "Easy (25%)", "Medium (25%)", "Hard (50%)".
  For custom difficulty (e.g. 15:30:55): headers are "Easy (15%)", "Medium (30%)", "Hard (55%)".
  For progressive difficulty: use the most common band's percentages in the header,
    or use generic "Easy (%)", "Medium (%)", "Hard (%)" if bands differ significantly.

Data (one row per mock, rows 2 to N_mocks+1):
  Col A : mock number (integer 1 to N_mocks)
  Col B : "Standard" (for default/uniform difficulty)
          OR user-defined band name (for progressive difficulty)
  Col C : S% as integer  e.g., 15  (NOT Q count — percentage of total)
  Col D : M% as integer  e.g., 30
  Col E : H% as integer  e.g., 55
  Col F : =SUM(C{row}:E{row})  must equal 100 for all mocks

CRITICAL: Cols C/D/E contain PERCENTAGE NUMBERS (e.g., 15, 30, 55 summing to 100),
NOT question counts. This matches the verified reference output.

Alternating row fill: odd rows white, even rows light grey #F2F2F2.
Freeze panes: A2.

Column widths: A=10, B=14, C=14, D=14, E=14, F=12
```

### S15-5 — Sheet 5: Phase 0 Verification

```
Sheet name (EXACT): "Phase 0 Verification"

Rows 1–5 — Header block (merged A:F or A:last_col):
  Row 1 : "[ExamCode] — Phase 0 Verification | Source: [N]-year data ([year_range])"
  Row 2 : "Recency weighting: [recent_year1], [recent_year2] × 2; [older_years] × 1"
  Row 3 : "Formula: r_avg = Σ(avg_per_paper[yr] × weighted_papers[yr]) / Σ(weighted_papers)"
  Row 4 : "Data quality: [any flags from §3-2, or 'No errors detected — all Papers In
            values consistent with Avg/Paper']"
  Row 5 : "BV-9B Batch coverage: ALL [N] PYQ subtopics guaranteed ≥1Q per 10-mock batch window"

  Header block font: dark grey #595959, 9pt. No fill. Left-aligned.

Row 6 — Column headers (EXACT names, EXACT order — 6 columns):
  A : "Subject"
  B : "Topic"
  C : "Sub-Topic"
  D : "Format"
  E : "r_avg (Recency)"
  F : "Type"              ← "pyq_based" or "zero_pyq"

Data rows 7 onwards — sorted by r_avg DESCENDING, ZP subs at bottom:
  Col A : section name — light section fill per S15-0
  Col B : topic
  Col C : subtopic
  Col D : format
  Col E : r_avg (4 decimal places, center-aligned)
  Col F : "pyq_based" (r_avg > 0) or "zero_pyq" (r_avg = 0)

Freeze panes: A7 (header block rows 1–6 always visible).
No Σ row.

Column widths: A=36, B=28, C=42, D=10, E=16, F=12
```

### S15-CHECKLIST — Mandatory pre-delivery self-verification

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  RUN THIS CHECKLIST BEFORE EVERY present_files CALL FOR blueprint.xlsx      ║
║  If ANY item fails: fix the xlsx. Never deliver a non-compliant xlsx.       ║
╚══════════════════════════════════════════════════════════════════════════════╝

☐ XLSX-1  Workbook has EXACTLY 5 sheets.
           Sheet names in order: "Paper Structure", "Blueprint",
           "Summary Stats", "Difficulty Schedule", "Phase 0 Verification".
           ANY other name = FAIL. Fix before delivering.

☐ XLSX-2  Sheet 2 ("Blueprint") row 1 headers are in EXACT order:
           Subject | Topic | Sub-Topic | Format | r_avg | M1 | M2 | ... | M[N_mocks]
           Total columns = 5 + N_mocks. Last mock column label = "M[N_mocks]".

☐ XLSX-3  Sheet 3 ("Summary Stats") row 2 headers are in EXACT order:
           Subject | Topic | Sub-Topic | Format | Type | r_avg (Recency) |
           Pooled Avg | Total PYQs | Quota (Target Qs) | Actual Qs |
           Accuracy% | Mocks Appeared
           EXACTLY 12 columns.

☐ XLSX-4  Sheet 4 ("Difficulty Schedule") row 1 headers are in EXACT order:
           Mock | Band | Easy ([S]%) | Medium ([M]%) | Hard ([H]%) | Total
           Data values in C/D/E are PERCENTAGE NUMBERS summing to 100 (e.g., 15/30/55),
           NOT question counts. Total column (F) = 100 for every row (sum of percentage values).

☐ XLSX-5  Sheet 5 ("Phase 0 Verification") has header block in rows 1–5,
           column headers in row 6 in EXACT order:
           Subject | Topic | Sub-Topic | Format | r_avg (Recency) | Type
           Data rows start at row 7.

ALL 5 items must be ☑ before calling present_files.
```

## §16 — EDGE CASE CHECKLIST

All known edge cases. Verify each before B3 proceeds.
Add new edge cases discovered during any exam's blueprint generation.

### EC-1: N_mocks = 1

```
ZP: MAX_ZERO = floor(1 × 0.10) = 0 → zp_active = False (§5-1 Step 4).
    No ZP Qs in any mock. Section is 100% PYQ-based.

Batch coverage (Option C):
    N_mocks=1 → n_batches = math.ceil(1/10) = 1.
    Quota minimum = n_batches = 1. Same as old series minimum.
    No change in behaviour vs prior versions for N_mocks=1.

SA: All quotas = max(n_batches, floor(scaled_avg × 1)) = max(1, floor(scaled_avg)).
    With N_mocks=1 and many subtopics: Σ quota may exceed sec_qs × 1.
    Negative deficit results. §4-2 tries to reduce quotas from lowest-remainder subtopics.
    SA-16 (updated): never reduce below n_batches=1.
    If all subtopics have quota=1 and Σ quota > sec_qs: AlgorithmError raised.
    User must reduce number of subtopics in scope or adjust sec_qs.

    Typical safe case (subtopics ≤ sec_qs):
    Only top sec_qs subtopics by r_avg get quota=1. Rest get quota determined by
    negative-deficit removal. Column sum = sec_qs. ✓

BV: BV-7 F2 (end-clustering) trivially passes with 1 mock (no series to cluster in).
    BV-9B: with 1 mock = 1 batch, every subtopic must appear in mock 1.
    This is guaranteed if Σ quota ≤ sec_qs (feasibility check passed).
```

### EC-2: All subtopics in a section have same r_avg

```
All scaled_avg values are equal → all fractional remainders equal.
Largest-remainder with equal remainders: tie-break applies.
§4-2 tie-break: sort by (fractional remainder DESC, r_avg DESC).
With all r_avg equal AND all remainders equal: Python stable sort preserves
the original list order (Analysis doc order — not necessarily alphabetical).
First subtopics in the Analysis doc order get the +1 remainder bonus.

No clustering issue — all subtopics treated equivalently. ✓
```

### EC-3: All subtopics in a section have r_avg = 0

```
This is the implementation of _apply_equal_distribution() called in §4-1
when section_total_r_avg == 0.

When all subtopics have r_avg = 0:
  - pq_subs is EMPTY
  - ALL subtopics are in zero_pyq_subtopics[]

Resolution:
  Step 1: Temporarily treat all ZP subtopics as PYQ-based for quota computation:
    subtopic_count = len(zero_pyq_subtopics[section])
    # ZP rotation may or may not be active (MAX_ZERO could be 0 for very small N_mocks).
    # Recompute MAX_ZERO from §5-1 to determine if ZP is active:
    zp_slots_used  = sum(zp_slot[section][m] for m in range(1, N_mocks + 1))
    target_total   = sec_qs * N_mocks - zp_slots_used  # correct regardless of ZP state
    # (If zp_active: zp_slots_used = N_mocks, so target = (sec_qs-1)*N_mocks)
    # (If not zp_active: zp_slots_used = 0, so target = sec_qs*N_mocks)
    quota[S]       = floor(target_total / subtopic_count) for all S
    + largest-remainder adjustment to reach exact target_total.

  Step 2: Run ZP rotation (§5) normally:
    ZP rotation fills 1 slot per mock per section from alphabetical cycle.

  Step 3: Phase 2 fills remaining (sec_qs - zp_slot[section][m]) slots per mock:
    Using equal-distribution quotas from Step 1.
    Urgency scoring works normally.
    (If ZP active: sec_qs-1 slots. If ZP inactive/MAX_ZERO=0: sec_qs slots.)

  Step 4: Column sum = Phase 2 Qs + zp_slot[section][m] = sec_qs. ✓
    (If ZP active: (sec_qs-1) + 1 = sec_qs. If ZP inactive: sec_qs + 0 = sec_qs.)

Documented as assumption in Paper Structure sheet.
```

### EC-4: Single subtopic in a section

```
Only 1 subtopic (pq_subs has 1 element).

quota[S] = target_total = sec_qs × N_mocks − total_zp_slots
  (not sec_qs × N_mocks — ZP slots reduce available quota)

ZP: if section has zero-PYQ subtopics → rotation still runs.
    Single PYQ subtopic gets sec_qs−1 per mock (1 slot taken by ZP).

Rare check: if r_avg[S] < RARE_THRESHOLD → S is rare.
    Phase 1 schedules all appearances of S at staggered positions.
    Phase 2 has 0 nonrare slots to fill.
    Column-fix handles any residual column sum error.
    If r_avg[S] ≥ 0.1 → S is non-rare. Phase 2 fills all slots normally.

Either way: single subtopic appears in every mock with q_count = sec_qs (or sec_qs-1 if ZP). ✓
```

### EC-5: Format value normalization edge cases

```
Normalize before checking VALID_FORMATS:
  All normalization uses §6-1 ALIASES dict (canonical complete mapping).
  See §6-1 for the full alias list.

  Quick reference (subset):
    Lowercase : 'text' → 'TEXT', 'figural' → 'FIGURAL', etc.
    Whitespace: '  TEXT  ' → 'TEXT'
    Mixed case: 'Figural' → 'FIGURAL', 'Passage' → 'PASSAGE'

If still not in VALID_FORMATS after normalization:
  Flag per §10 S10-11. Ask user. Do not assume TEXT.

If Excel Format column exists but has a mix of valid and blank cells:
  Valid cells: use normalized value.
  Blank cells: flag per §10 S10-11. Ask user per subtopic.
  Never assume blank = TEXT without user confirmation.

CRITICAL — NORMALIZED FORMAT VALUE NEVER TRIGGERS EXCLUSION:
  After normalization, every subtopic — regardless of its Format value —
  is included in §4 allocation (r_avg > 0) or §5 ZP rotation (r_avg = 0).
  'Figural' normalizing to 'FIGURAL' does NOT mean the subtopic is excluded.
  'PASSAGE' does NOT mean the subtopic is excluded.
  Format normalization is a data-cleaning step only.
  Ref: §6 GOLDEN RULE — FORMAT IS CLASSIFICATION ONLY, NEVER EXCLUSION.
```

### EC-6: ExamCode collision

```
User runs MockBlueprint SSC_CGL_TIER1 50 but project already has
SSC_CGL_TIER1_blueprint.json from a prior run.

Claude warns (ref S1-3):
  "ExamCode SSC_CGL_TIER1 already has files from a prior run.
   Confirm to proceed — existing files will be replaced on delivery."

After confirmation: proceeds normally.
Old files replaced when user uploads new files after B3.
Prior registry.json replaced → dedup starts fresh for new series.
```

### EC-7: Files uploaded after trigger is typed

```
Scope: applies ONLY before B1 starts (during session start, S1-2).
Files uploaded DURING B1 (mid-session) are NOT visible to Claude
in the same session — user must start a fresh chat (ref §8-6).

Before B1:
  User types trigger first, then uploads files in same or next message.
  Claude: pauses processing → re-inventories all available files → proceeds.
  Never start B1 with incomplete file set.
  If files still missing after re-inventory: flag and wait.

During B1 or later:
  If user uploads a file mid-session: Claude cannot see it.
  Flag: "Uploads made mid-session are not visible. Start a fresh chat
         after uploading all required files."
```

### EC-8: Excel sheet name variations

```
Expected: 'Master Data ([N] Years)' and subject-specific tabs
  (year count varies — not always 7; could be 3, 5, 10, etc.)
  Subject tabs: 'GI & Reasoning', 'Gen. Awareness', 'English', etc.
  (names vary by exam and user)

Actual: 'Master Data', 'GI_Reasoning', 'General Awareness', 'Quant', etc.

Claude identifies correct sheets by content structure:
  Master Data sheet: has Subject + Topic + Sub-Topic + multiple year columns.
  Subject sheets: have Topic + Sub-Topic + year columns (no Subject column).

If content is ambiguous (two sheets match structure):
  Flag: "Multiple sheets match expected structure for [subject].
         Please specify which sheet contains [subject] data."
  Wait for user to clarify.
```

### EC-9: Exam with 5+ sections

```
Color assignment follows S15-0 order (use EXACTLY these hex codes — same as §15-0):
  Section 1: Light Blue   #DEEAF1  (dark header: #1F4E79)
  Section 2: Light Green  #E2EFDA  (dark header: #375623)
  Section 3: Light Orange #FCE4D6  (dark header: #833C00)
  Section 4: Light Purple #EAE3F7  (dark header: #4B2C8A)
  Section 5: cycle back to Section 1 colors (#DEEAF1 / #1F4E79)
  Section 6: cycle to Section 2 colors (#E2EFDA / #375623)
  Section 7+: continue cycling through Sections 1–4

Each section allocated independently (no cross-section constraints — ref §4-1).
blueprint.json sections[] length = number of sections (no limit).
Blueprint sheet column count = 5 identity cols + N_mocks mock cols (no limit).
```

### EC-10: Memory conflicts with input documents on subtopic scope or Format

```
Scenario: Claude's memory from a prior session contains a note such as
  "FIGURAL subtopics are banned from [section]" or
  "Spatial & Diagrammatic Reasoning excluded from GIR" or
  "[subtopic X] removed due to 2025 exam structural change"
  — but the Analysis doc and Frequency Excel uploaded in THIS session
  include those subtopics with non-zero PYQ counts.

Resolution — ALWAYS:
  Input documents WIN over memory. No exceptions.

Procedure:
  1. Read the Analysis doc. Extract ALL subtopics as written.
  2. Read the Excel. Use Format values as written.
  3. Run BV-0A (§9 S9-0A) to confirm all Analysis doc subtopics are present.
  4. DO NOT apply any memory-based ban, exclusion, or structural-change rule
     that is not explicitly stated in the input documents of THIS session.
  5. If the memory note appears to conflict: IGNORE the memory. Follow the docs.

The only way an exclusion is legitimate is if it comes from one of:
  (a) The input documents themselves (e.g., Analysis doc explicitly marks a
      subtopic as "no longer in syllabus" or "excluded from 2025 onwards")
  (b) An explicit instruction from the user IN THIS SESSION
  (c) r_avg = 0.0 (Zero-PYQ → §5 rotation, not total exclusion)

If (a): document the exclusion in Paper Structure sheet. Exclude from allocation.
If (b): document the instruction in Paper Structure sheet. Apply as directed.
If (c): ZP rotation handles it. The subtopic still appears in the blueprint.

If none of (a), (b), (c) apply → include the subtopic. Always.

Ref: §1 Memory Prohibition, §6 GOLDEN RULE, §9 S9-0A BV-0A.
```

### EC-11: Batch coverage feasibility — too many subtopics for batch window

```
TRIGGER:
  n_pq_subs > batch_slots  (n_pq_subs = len(pyq_subtopics[section]),
                              batch_slots = batch_size × sec_qs)

  Example: 62 subtopics in GIR, batch_size=10, sec_qs=25 → batch_slots=250.
           62 ≤ 250 → FEASIBLE ✓

  Example (hypothetical overload): 300 subtopics in a section, batch_size=10,
           sec_qs=25 → batch_slots=250. 300 > 250 → INFEASIBLE ✗

WHEN IT OCCURS:
  For typical MCQ exams (e.g., 25 Qs/section, 10-mock batches, ~60 subtopics/section),
  this constraint is never triggered — batch_slots comfortably exceeds subtopic count.
  It would trigger only for extremely subtopic-dense exams.
  All values (Qs/section, batch size, subtopic count) are read from blueprint.json — not hardcoded.

ACTION ON TRIGGER (halt in §4-1 feasibility pre-check):
  Raise AlgorithmError with message:
    "Section [X]: Batch coverage guarantee (Option C) is INFEASIBLE.
     [n_pq_subs] PYQ subtopics > [batch_slots] batch slots
     ([batch_size] mocks × [sec_qs] Qs per mock).
     Cannot guarantee every subtopic appears once per 10-mock window.

     Options:
       (a) Reduce batch_size requirement — accept ≥1 per N mocks instead of per 10.
           Specify new window: 'MockBlueprint ... --batch_coverage N'
       (b) Accept that very-low-quota subtopics appear once per series only
           (revert to Option A/B coverage rules for those subtopics).
       (c) Reduce subtopic count — merge very-rare subtopics into broader categories.
     Please choose and re-trigger."

RESOLUTION:
  User chooses one of the three options above.
  Claude re-confirms before proceeding.
  If user chooses (b): apply batch coverage only to subtopics with quota >= n_batches
  naturally (i.e., don't force n_batches minimum on subtopics with very small raw_total).
  Document the override in Paper Structure sheet.

  NOTE: For typical MCQ exams (25 Qs/section, ~60 subtopics/section), EC-11 is not
  expected to trigger: max subtopics << batch_slots (250) by a wide margin.
  It would trigger only for extremely subtopic-dense sections.
```

---

## DEFINITION OF DONE — Step 6 (MockBlueprint)

Step 1 is complete and B3 may proceed ONLY when ALL of the following hold:

```
☐ 0.  BATCH GATE discipline maintained throughout:
       B1 delivered in one response then STOPPED (§8-2 Step 9 BATCH GATE).
       Each B2 batch delivered in its own response then STOPPED (§8-3 Step 8 BATCH GATE).
       No batch was collapsed with another in the same response.
       Blueprint.json was uploaded by user between every B2 batch.
☐ 1.  All input documents read and processed (§2)
☐ 2.  r_avg computed for every subtopic (§3)
☐ 3.  Format flags set: passage_present, figural_present, di_present (§6)
☐ 3A. BV-0A passed: every subtopic from Analysis doc is in pyq_subtopics OR
       zero_pyq_subtopics. Confirmed: 0 subtopics silently excluded. FIGURAL audit passed.
       (ref §9 S9-0A — runs in B1, before blueprint.json v1 is written)
☐ 4.  Difficulty schedule complete for all N_mocks (§7)
☐ 5.  Phase 1 positions pre-scheduled for all rare subtopics (§4-4)
       Batch-coverage validation passed for all rare subtopics (ref §4-4).
☐ 6.  ZP rotation schedule complete for all N_mocks (§5-2)
☐ 7.  All N_mocks in blueprint['mocks'] (len == N_mocks)
☐ 8.  BV-1 to BV-6 AND BV-9B passed for every B2 batch (§9)
       BV-9B: every PYQ subtopic appears ≥ 1 Q in each 10-mock batch window.
☐ 8b. BV-10 feasibility gate (§4-1b) passed at B1: BV-10a form_key uniqueness proven
       satisfiable per collision_domain and every batch window (HALT-with-fix if not);
       BV-10b family soft-cap notes recorded. BV-10a/BV-10b clean on every B2 batch (§9-6b).
☐ 9.  BV-7 passed: full cross-batch validation (§9-7)
☐ 10. BV-8 passed: zero-PYQ final count exact (§9-8)
☐ 11. All edge cases in §16 verified (including EC-11 feasibility check)
☐ 12. All assumptions documented in Paper Structure sheet (§10 S10-12)
☐ 13. All 6 output files generated and present_files called (§13-7)
☐ 14. Handoff message delivered (§11-3)
☐ 15. Step 5 (PYQExtract) also complete in [ExamCode] project.
       [ExamCode]_section_rules.md is ready for upload to [ExamCode] project.
       Step 2 MUST NOT start until BOTH Step 0 AND Step 1 are complete.
☐ 25. [ExamCode]_mock_test_audit.py generated per §13-7A rules (the canonical v2.6
       auditor, verbatim from Framework_MockTestCreateAudit.md Appendix A); --self-test
       passed FIXTURE-BASED with N >= 35 (43/43); included in B3 present_files delivery.
       Collision check completed if prior script existed (EC-D1/D3).
```


# ════════════════════════════════════════════════════════════════════════
# §17 — SUBTOPIC_ID CONTRACT (v1.21 — consumer + enforcer role)
# ════════════════════════════════════════════════════════════════════════
#
# Step 1's role in the cross-step contract (full contract defined in Step 0 §15):
#   Step 0 MINTS subtopic_id and publishes [ExamCode]_subtopic_manifest.json.
#   Step 1 (THIS step) CONSUMES it: assigns ids by manifest, enforces mandates.
#   Step 2 JOINS blueprint ↔ section_rules on subtopic_id.

## S2-MANIFEST — Manifest load + contract gate (run at B1 session start)

  ```python
  import json, re
  import blueprint_core as bc   # ENGINE (mandated in S1-2b)
  # slugify is provided by the shared engine — byte-identical recipe to the inlined copy
  # AND to Step 0 (same em-dash/en-dash/slash/ampersand handling, verified at the
  # U+2014/U+2013 codepoint level), so cross-step subtopic_id matching is preserved.
  # Aliased so the resolution call sites below (slugify(dn) etc.) stay unchanged.
  slugify = bc.slugify

  manifest_path = f'/mnt/project/{EXAM}_subtopic_manifest.json'
  if not os.path.exists(manifest_path):
      raise SystemExit(
          f"HARD STOP (S2-MANIFEST): {EXAM}_subtopic_manifest.json not found. "
          f"Step 0 must publish it before Step 1 can build the blueprint. "
          f"Run/re-run Step 0 (PYQExtract --synthesise ALL), upload the "
          f"manifest to the [ExamCode] project, then re-run Step 1.")
  manifest = json.load(open(manifest_path, encoding='utf-8'))
  MANIFEST_IDS   = manifest['subtopics']                    # id -> {display_name, ...}
  # Reverse maps for resolution. Build them COLLISION-AWARE: if two distinct ids
  # share a display_name (or a slug), resolution by name is ambiguous and MUST NOT
  # silently pick one. We record ambiguous names and hard-stop if one is used.
  NAME_TO_ID, SLUG_TO_ID = {}, {}
  AMBIG_NAMES, AMBIG_SLUGS = set(), set()
  for k, v in MANIFEST_IDS.items():
      dn = v['display_name']; sl = slugify(dn)
      if dn in NAME_TO_ID and NAME_TO_ID[dn] != k: AMBIG_NAMES.add(dn)
      else: NAME_TO_ID[dn] = k
      if sl in SLUG_TO_ID and SLUG_TO_ID[sl] != k: AMBIG_SLUGS.add(sl)
      else: SLUG_TO_ID[sl] = k
  MANDATORY_IDS  = set(manifest.get('mandatory_every_mock', []))
  ALT_GROUPS     = manifest.get('alternation_groups', {})   # group -> [ids]
  MANDATORY_GROUPS = manifest.get('mandatory_groups', {})   # v1.11 group -> {members:[ids], min:int}
  CADENCE_WINDOWS  = manifest.get('cadence_windows', {})    # v1.11 id -> N (>=1 every N mocks)
  MIN_COUNTS       = manifest.get('min_counts', {})         # v1.11 id -> k (>=k Q per mock)
  # LOCKED_IDS: ids a force-place may NEVER displace — any id under an active mandate.
  # Built once so M1/M4/M6 displacement never evicts another mandate's guaranteed slot.
  LOCKED_IDS = (MANDATORY_IDS
                | {i for g in ALT_GROUPS.values() for i in g}
                | {i for g in MANDATORY_GROUPS.values() for i in g.get('members', [])}
                | set(CADENCE_WINDOWS) | set(MIN_COUNTS))

  # ── v1.23 THREE-AXIS: read the format-distribution targets Step 5 v2.23 emits ──────
  # Absent-safe: a pre-v2.23 manifest lacks these keys → empty maps → the whole feature
  # stays inert (axis_schedule built with status='no_pyq', BV-AXIS passes vacuously).
  AXIS_DIST_BY_SECTION = manifest.get('axis_distribution', {})   # section -> per-section target
  AXIS2_CAP_BY_ID      = {}   # subtopic_id -> [Axis-2 classes it may faithfully take]
  OBSERVED_AXIS2_BY_ID = {}   # subtopic_id -> {AXIS2_CLASS: observed count}
  PRES_FAMILY_BY_ID    = {}   # subtopic_id -> presentation_family (or None)
  for k, v in MANIFEST_IDS.items():
      AXIS2_CAP_BY_ID[k]      = v.get('axis2_capability', ['DIRECT'])
      OBSERVED_AXIS2_BY_ID[k] = v.get('observed_axis2', {})
      PRES_FAMILY_BY_ID[k]    = v.get('presentation_family')
  # (format per subtopic is already in MANIFEST_IDS[k]['format'] — the Axis-1 lock.)

  # ── v1.13 PRE-FLIGHT CHECK: MANDATE vs r_avg CONSISTENCY ──────────────────
  # A subtopic CANNOT simultaneously be "must appear every mock" (or min_counts,
  # or cadence_windows) AND have r_avg = 0. r_avg = 0 routes the subtopic to
  # ZP rotation (§5), which caps it at 5/50 (or similar). A mandate demands
  # every-mock presence. These are mutually exclusive by design.
  # This check runs at manifest load time — catches errors BEFORE B1 generation,
  # not three batches deep.
  #
  # IMPORTANT: This check uses r_avg values computed in §3 (S3-4). At manifest
  # load time (§1 / S2-MANIFEST), r_avg may not yet be computed. Therefore this
  # pre-flight MUST run AFTER §3 completes but BEFORE §4 begins — specifically
  # at the start of §4-1 per-section setup, after section_total_r_avg is known.
  # The code below is placed here for documentation; the execution point is §4-1.
  #
  # SECTION-AWARE: the function receives section_name and filters mandated ids
  # to only those whose manifest entry belongs to the CURRENT section. This
  # prevents false HARD STOPs when a mandated id from section "X" is
  # checked against section "Y"'s pq_subs list (cross-section id leak).
  def preflight_mandate_ravg_check(section_name, pq_subs, zero_pyq_subs):
      """HARD STOP if any mandated id IN THIS SECTION resolves to a Zero-PYQ subtopic."""
      mandate_check_ids = (MANDATORY_IDS | set(MIN_COUNTS) | set(CADENCE_WINDOWS))
      for sid in mandate_check_ids:
          if sid not in MANIFEST_IDS:
              continue   # unknown id — will be caught by resolve_subtopic_id()
          # v1.13: only check ids that belong to THIS section
          if MANIFEST_IDS[sid].get('section') != section_name:
              continue
          dn = MANIFEST_IDS[sid]['display_name']
          if dn in zero_pyq_subs or dn not in pq_subs:
              mandate_type = []
              if sid in MANDATORY_IDS: mandate_type.append('mandatory_every_mock')
              if sid in MIN_COUNTS: mandate_type.append(f'min_counts(k={MIN_COUNTS[sid]})')
              if sid in CADENCE_WINDOWS: mandate_type.append(f'cadence_windows(N={CADENCE_WINDOWS[sid]})')
              raise SystemExit(
                  f"HARD STOP (PRE-FLIGHT): subtopic '{dn}' (id={sid}) is in "
                  f"{', '.join(mandate_type)} but has r_avg = 0.0 (Zero-PYQ). "
                  f"A Zero-PYQ subtopic is routed to ZP rotation (§5) which caps "
                  f"appearances — this is incompatible with a mandate that requires "
                  f"every-mock or periodic presence. "
                  f"FIX: either (a) remove '{dn}' from the mandate in the manifest, "
                  f"or (b) correct its PYQ data so r_avg > 0.")
  ```

## S2-MANIFEST-COMPLETENESS — Taxonomy coverage pre-flight (v1.21, run after S2-MANIFEST)

  ```
  ═══════════════════════════════════════════════════════════════════════
  MANIFEST COMPLETENESS GATE (v1.21 — Fix B.2)
  ═══════════════════════════════════════════════════════════════════════

  WHEN: After S2-MANIFEST loads the manifest and before B1 begins.
  WHY:  If the manifest is INCOMPLETE (missing taxonomy subtopics), the
        blueprint build will encounter unresolvable subtopics. Without
        this gate, Step 6 historically auto-generated sequential IDs
        (ST{NNNN}) for unresolvable subtopics — a silent contract
        violation that only surfaced as a HARD STOP in Step 7 S3-8.
        This gate catches the incompleteness at the SOURCE (Step 6
        startup) and directs the user to fix it upstream (Step 5).

  HOW:  Load the exam's taxonomy from the Analysis doc(s) and/or
        taxonomy_draft.json. Attempt to resolve every taxonomy subtopic
        via resolve_subtopic_id(). Any unresolvable subtopic = HARD STOP.

  IMPLEMENTATION:
    # After S2-MANIFEST loads MANIFEST_IDS, NAME_TO_ID, SLUG_TO_ID:
    taxonomy_subtopics = []
    # Source 1: Analysis doc(s) in project knowledge
    for doc_path in analysis_doc_paths:
        for (section, topic, subtopic) in extract_taxonomy(doc_path):
            taxonomy_subtopics.append((section, topic, subtopic))
    # Source 2 (additive): taxonomy_draft.json if available
    tax_draft_path = f'/mnt/project/{EXAM}_taxonomy_draft.json'
    if os.path.exists(tax_draft_path):
        import json as _j
        tax = _j.load(open(tax_draft_path, encoding='utf-8'))
        for sec, topics in tax.items():
            for top, subs in topics.items():
                for sub in subs:
                    if (sec, top, sub) not in taxonomy_subtopics:
                        taxonomy_subtopics.append((sec, top, sub))

    manifest_missing = []
    for (sec, top, sub) in taxonomy_subtopics:
        sl = slugify(sub)
        # Check: does this subtopic resolve to a manifest id?
        if sub not in NAME_TO_ID and sl not in SLUG_TO_ID:
            manifest_missing.append(f"  {sec} > {top} > {sub}")

    if manifest_missing:
        raise SystemExit(
            f"HARD STOP (S2-MANIFEST-COMPLETENESS): "
            f"{len(manifest_missing)} taxonomy subtopic(s) have no manifest id. "
            f"These are likely zero-PYQ subtopics that Step 5 did not mint.\n"
            f"MISSING:\n" + "\n".join(manifest_missing) +
            f"\n\nFIX: Re-run Step 5 (PYQExtract --synthesise ALL). "
            f"Framework_MockTestAnalyse v2.20+ runs taxonomy sync to mint "
            f"ids for ALL taxonomy subtopics including zero-PYQ ones. "
            f"Upload the updated manifest + section_rules, then re-run Step 6.")

  EDGE CASES:
    - taxonomy_draft.json absent AND no Analysis docs: gate SKIPS (no
      taxonomy to check against). Log warning. Step 6 proceeds — if any
      subtopics are unresolvable, resolve_subtopic_id() will HARD STOP
      at the point of use.
    - All taxonomy subtopics resolve: gate PASSES silently. No output.
    - Manifest has MORE subtopics than taxonomy: EXPECTED (PYQ-discovered
      finer splits). No issue — only checks taxonomy → manifest direction.
  ═══════════════════════════════════════════════════════════════════════
  ```

  resolve_subtopic_id(): map an Analysis-doc subtopic to its manifest id.
  ```python
  def resolve_subtopic_id(display_name, section=None, topic=None):
      sl = slugify(display_name)
      # Ambiguity guard: if the name/slug maps to 2+ distinct ids, we cannot pick
      # silently. Disambiguate by (section, topic) if provided; else HARD STOP.
      if display_name in AMBIG_NAMES or sl in AMBIG_SLUGS:
          if section is not None and topic is not None:
              want = (section, topic, display_name)
              for k, v in MANIFEST_IDS.items():
                  if (v['section'], v['topic'], v['display_name']) == want:
                      return k
              # slug-level disambiguation by section+topic
              for k, v in MANIFEST_IDS.items():
                  if (v['section'], v['topic'], slugify(v['display_name'])) == \
                     (section, topic, sl):
                      return k
          raise SystemExit(
              f"HARD STOP (S2-MANIFEST): subtopic '{display_name}' is AMBIGUOUS — "
              f"it maps to multiple subtopic_ids in the manifest (same name/slug "
              f"under different section/topic). Provide section+topic to "
              f"disambiguate, or rename in Step 0 so the display name is unique.")
      if display_name in NAME_TO_ID:                 # (a) exact display match
          return NAME_TO_ID[display_name]
      if sl in SLUG_TO_ID:                           # (b) slug-equal match
          return SLUG_TO_ID[sl]
      raise SystemExit(                              # (c) no silent fallback
          f"HARD STOP (S2-MANIFEST): subtopic '{display_name}' from the Analysis "
          f"doc has no id in {EXAM}_subtopic_manifest.json. Add/rename it in Step 0 "
          f"and re-run Step 0, then re-run Step 1. (Names may differ cosmetically, "
          f"but every subtopic Step 1 uses MUST resolve to a Step 0 manifest id.)")
  ```
  Every subtopic_list[] entry and every subtopic_allocation MUST carry the id
  returned here. Step 1 never invents an id.

## S4-MANDATE — Build-time mandate enforcement (guarantees D09/D10/D11/D12 class)

  These checks make mandatory-subtopic and alternation violations IMPOSSIBLE to
  emit. They run inside the mock-build loop (§8-3 Step 4e, between Phase 2 and
  column-fix) and in BV (§9).

  RULE M1 — mandatory_every_mock: for EVERY mock m, every id in MANDATORY_IDS
    must have a subtopic_allocation with q_count ≥ 1. If the allocation algorithm
    did not place it, FORCE-PLACE 1Q (displacing the lowest-r_avg non-mandatory,
    non-alternation-locked subtopic in the same section to keep the section sum).
    If displacement is impossible (section full of mandatory ids) → HARD STOP with
    the section name and the competing ids, ask user to revise pattern/counts.

  RULE M2 — alternation_groups: for EVERY mock m and EVERY group in ALT_GROUPS,
    AT MOST ONE member id may appear. Selection rule (deterministic, exam-agnostic):
      member_index = (m + group_offset) % len(members)
      → odd/even style alternation across the series; never two members in one mock.
    group_offset is fixed per group (0 unless the manifest specifies otherwise),
    so the alternation is stable and reproducible.

    CONFLICT RESOLUTION (v1.13 — two requirements):
    If the raw allocation placed two members in one mock:
      (a) KEEP the one selected by member_index, MOVE the other to the mock where
          it IS selected by member_index.
      (b) BACKFILL RULE: the freed slot at the source mock (where the evicted member
          was removed) MUST be backfilled from the general nonrare pool (highest-quota
          non-mandatory subtopic that has remaining_quota > 0 and is under per_mock_cap
          at that mock). The freed slot is NEVER automatically given to the "kept"
          member — that would inflate its count beyond quota.
      (c) FIXED-POINT LOOP: resolution MUST run as a fixed-point loop over all mocks
          (repeat the full pass until a complete sweep finds zero conflicts). A single
          pass is INSUFFICIENT: relocating a member to an earlier, already-checked mock
          can create a NEW conflict there (if that mock already had a different group
          member placed in a prior iteration). The loop terminates when:
            - A full pass finds zero conflicts (normal termination), OR
            - A configurable iteration limit (default 100) is reached → HARD STOP
              with the group name and the conflicting mocks, ask user to revise.
      (d) After resolution loop completes, re-run column-fix (§4-6) to correct any
          residual column-sum imbalances caused by relocations and backfills.

  RULE M4 — mandatory_groups (GROUP-PRESENCE, per mock): for EVERY mock m and EVERY
    group G in MANDATORY_GROUPS, at least G['min'] (default 1) of G['members'] must
    have q_count ≥ 1 (counting across all members).

    v1.13 FIX — TIE-BREAK + QUOTA RESERVATION:
    If fewer than G['min'] members are present, FORCE-PLACE 1Q of the absent member
    with the LOWEST CUMULATIVE TOTAL SO FAR (deterministic; ties broken by members[]
    order), displacing the lowest-r_avg subtopic NOT in LOCKED_IDS in that member's
    section to keep the section sum. Repeat until G['min'] is met.

    RATIONALE for lowest-cumulative instead of highest-r_avg: highest-r_avg biases
    toward the same member repeatedly across 50+ mocks, resulting in one member
    disproportionately force-placed while others stay underrepresented. Lowest-
    cumulative naturally spreads group presence across all members.

    QUOTA RESERVATION (v1.13): mandatory_groups receive upfront quota reservation
    in §4-2, sized from group_min × N distributed across members. This prevents the
    quota-vs-mandate fight where displacement at build time cascades into other
    subtopic failures.

    A group's members are expected to share a section; place each in its own
    member's section.
    HARD STOP if displacement is impossible (section saturated with locked ids) —
    report the section, the group, and the competing ids.

  RULE M5 — cadence_windows (CADENCE, CROSS-MOCK — full-series pass, NOT per mock):
    for EVERY id c with window N in CADENCE_WINDOWS, c must appear (q_count ≥ 1 in
    some section) at least once in EVERY sliding window of N consecutive mocks across
    the WHOLE series. Because a window spans mocks (and may straddle B2 batch
    boundaries), this is enforced in the full-series validation (§9-7 BV-7), NOT the
    per-mock build loop. Enforcement: slide a length-N window over mocks 1..T; for any
    window [s, s+N-1] with zero occurrences of c, FORCE-PLACE 1Q of c into the LAST
    mock of that window (displacing lowest-r_avg non-LOCKED in c's section), then
    continue the slide. IMPORTANT ASYMMETRY: cadence is INVISIBLE to a single mock, so
    Step 2 has NO cadence gate — Step 1 is the sole enforcer. A cadence id is present
    periodically but is NOT mandatory-every-mock unless separately declared.

  RULE M6 — min_counts (MIN-COUNT, per mock): for EVERY mock m and EVERY id with
    minimum k in MIN_COUNTS, that id's total q_count in the mock must be ≥ k. This is
    RULE M1 generalised from 1 to k. If q_count < k, RAISE it to k (create the
    allocation at q_count=k if absent, else increase it), freeing k−current questions
    by displacing the lowest-r_avg subtopics NOT in LOCKED_IDS in that id's section.
    HARD STOP if the section cannot yield the questions. (k ≥ 1 ⇒ a min_count id is
    present in every mock, so it need not ALSO be listed in mandatory_every_mock.)

  RULE M3 — BV-MANDATE (blueprint validation, §9): after building all mocks in a
    batch, assert for every mock: (i) all MANDATORY_IDS present; (ii) no alternation
    group has 2+ members; (iii) [v1.11] every MANDATORY_GROUPS group has ≥ its min
    members present; (iv) [v1.11] every MIN_COUNTS id has q_count ≥ its k. Then in the
    FULL-SERIES pass (BV-7): (v) [v1.11] every CADENCE_WINDOWS id appears ≥1 in every
    N-mock window. A failing mock/window is NEVER stored (consistent with the existing
    "validation.status always pass" invariant). Report any fix applied by M1/M4/M5/M6.

## S-IDWRITE — Emitting ids into the JSON (where build_section_obj runs)

  In §8-3 Step 5 build_section_obj(), every subtopic_allocation dict MUST include:
    'subtopic_id': resolve_subtopic_id(subtopic_display_name, section_name, topic_name)
  Passing section+topic lets resolve disambiguate the rare case where the same
  display name exists under two topics (e.g. "Analogy" under Verbal and Non-Verbal).
  And every subtopic_list[] entry (B1) MUST include the same 'subtopic_id'.
  Field order is cosmetic; presence is mandatory. BV-MANDATE + Step 2's contract
  gate both reject any allocation lacking a subtopic_id.

## DoD additions (v1.7)
  ☐ 16. subtopic_manifest.json loaded; every subtopic resolved to a manifest id
        (zero unresolved → no HARD STOP fired).
  ☐ 17. Every subtopic_allocation and subtopic_list[] entry carries subtopic_id.
  ☐ 18. RULE M1 (mandatory every mock) holds for all mocks.
  ☐ 19. RULE M2 (alternation groups: ≤1 member per mock) holds for all mocks.
  ☐ 20. BV-MANDATE passed for every mock in every batch.
  ☐ 21. RULE M4 (group-presence: ≥min members of each mandatory_groups group) holds for all mocks.
  ☐ 22. RULE M6 (min-count: q_count ≥ k for each min_counts id) holds for all mocks.
  ☐ 23. RULE M5 (cadence: each cadence_windows id present ≥1 in every N-mock window) holds
        across the full series (checked in BV-7, not per mock — cadence is cross-mock).
  ☐ 24. PRE-FLIGHT mandate/r_avg consistency check passed: no subtopic in
        mandatory_every_mock, min_counts, or cadence_windows has r_avg = 0.0 (v1.13).
  ☐ 26. S2-MANIFEST-COMPLETENESS gate passed: every taxonomy subtopic resolves
        to a manifest id. Zero unresolvable subtopics (v1.21).
  ☐ 27. RULE 2a (NO BYPASS) enforced: every subtopic_id in blueprint.json was
        returned by resolve_subtopic_id(). Zero self-minted or auto-generated
        sequential IDs in subtopic_list[] or subtopic_allocations[] (v1.21).
  ☐ 28. ENGINE MANDATE (S1-2b) passed: blueprint_core.py present in the project,
        copied to /home/claude, and `--self-test` printed "SELF-TEST: N/N PASS"
        before any allocation ran (v1.28).
  ☐ 29. All allocation math routed through the engine (bc.*): no inlined copy of
        compute_r_avg / proportional_split / largest_remainder_fix / exact_fill /
        difficulty_counts / derive_axis_schedule / slugify remains in this spec —
        single source of truth (v1.28).

# END OF Framework_Blueprint v1.31
