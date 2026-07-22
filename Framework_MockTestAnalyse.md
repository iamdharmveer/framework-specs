# Framework_MockTestAnalyse v2.24.9 — Universal PYQ Pattern Extraction Engine
# [ExamCode] project | Step 5 (PYQExtract) | Exam-agnostic
#
# v2.24.9 — 2026-07-22 — S-SECMAP: SECTION↔SUBJECT MAPPING (BUG 1 of 4, GAP-2026-07-22-001).
#   Root cause: exam_config.json sections[] never carried a `subjects` field listing which
#   taxonomy Subjects belong to each OTS section. For any exam where OTS section names differ
#   from manifest Subject names AND there are multiple sections (e.g. IIT JAM "Section A/B/C"
#   vs manifest "General Biology"/"Chemistry"/...), Step 6's resolver (S2-1b) would HARD STOP
#   at SEC-4 — unable to determine the mapping. For 1:1 exams (SSC CGL, MPPSC) the resolver's
#   SEC-3 identity-map path handled it, masking the gap.
#   FIX: new S-SECMAP rule in run_synthesise(), after taxonomy sync and before writing outputs.
#   3-stage derivation: (1) OBSERVE which subjects appear in which section Q-ranges from PYQ
#   classifications, (2) AUGMENT cross-subject sections with union of all cross-subject pools,
#   (3) FALLBACK unmapped taxonomy subjects to cross-subject or all sections.
#   Writes subjects[] to each section in exam_config.json; adds exam_config.json to final
#   delivery (6 files, was 5). User must REPLACE exam_config.json in project knowledge.
#   Zero behavior change for 1:1 exams (subjects[] = single-element list matching SEC-3).
#   12/12 edge cases pass (SSC CGL, MPPSC, IIT JAM, GATE, CSIR NET, UGC NET, NEET,
#   fuzzy names, sampling gap, Zero-PYQ subject, structure change, single-section).
#
# v2.24.8 — 2026-07-20 — PYQ CORPUS DRIVE-ONLY STANDARDIZATION (twin fix: Framework_
#   PYQAnalyse.md Step 2b / PYQScan). Found during a project-level audit: three
#   pipeline steps that all handle the SAME document class (Row/Sorted PYQ .docx
#   corpus files) disagreed on whether Google Drive was required — Step 4 (PYQCount)
#   always mandated Drive with no fallback; Step 2b (PYQScan) allowed an uploads-only
#   fallback; this step (Step 5) allowed the broadest fallback (project/uploads).
#   STANDARDIZED to Step 4's existing Drive-only rule (confirmed with Radheshyam) —
#   Row/Sorted PYQ corpus files must be in Google Drive across all three steps now.
#   WHAT CHANGED:
#     Header comment block, §1 S1-1 — PYQ: <<Drive link>> is now REQUIRED for paper-processing
#       (auto-mode); absent → HARD STOP. --status/--synthesise are exempt (they don't
#       re-scan the PYQ corpus) — if PYQ: is given anyway for those modes it's used
#       opportunistically, non-fatal on Drive error.
#     §1 S1-2 — removed the local project/uploads fallback loop for pyq_doc_paths
#       (the raw PYQ corpus). Exam Pattern and Analysis documents are UNCHANGED —
#       those remain project/uploads-eligible (small state/reference files, not the
#       corpus) via the existing unconditional local-collection loop, including the
#       loose image/PDF exam-pattern fallback (preserved unchanged, not part of this
#       standardization).
#     Drive listing errors now HARD STOP instead of silently degrading to a local
#       scan — there is no local fallback for the corpus left to degrade to.
#   Does not touch synthesis, subtopic mapping, gate logic, or any Analysis-doc
#   generation. Verified: validate_framework_md.py (0 issues, AST-clean).
#
# v2.24.7 — 2026-07-18 — §6.2 STRUCTURAL FIX for A-INTEGRITY-FALSEPOS-01 (docs-only, zero
#   logic change). §14 SCHEMA REFERENCE's three block definitions (CATEGORY C, CATEGORY A,
#   CATEGORY B) each now carry an explicit "*** DOC-ALIAS ONLY ***" note stating the real
#   on-disk literal token adjacent to the conceptual name, and an explicit instruction to
#   never regex-match the "CATEGORY" phrase against file content. This is the same
#   authoring mistake that caused Framework_MockTestCreateAudit.md's P0.5 to HARD STOP on
#   every valid section_rules.md (fixed at v2.7.5) — the consumer spec hard-coded this
#   file's internal doc-alias instead of the literal token write_section_rules() actually
#   emits. Preventive only: no function, no on-disk format, no consumer contract changed.
#   write_section_rules() output is byte-identical. validate_framework_md.py 0 issues
#   (pre-existing O-MANDATE MANDATE-1 reference issue unrelated to and unaffected by this
#   change — flagged separately, not touched here).
#
# v2.24.6 changes: GAP ANALYSIS FIX B + FIX C — MPSC_Botany root-cause audit
#   (Framework_Gap_Analysis, Step 6 §6 HALT investigation). Closes the Step-5 half of
#   two structural defects that recur on every exam with (a) any Zero-PYQ subtopic, or
#   (b) any PASSAGE/DI subtopic, or (c) a subtopic whose stem merely CONTAINS the
#   substring "table" ("vegetable", "acceptable", ...). The Step-6 (Framework_Blueprint)
#   half — reading Format from the manifest instead of the Excel — ships as Blueprint
#   v1.32 FIX A/D/E; this is the Step-5 defense-in-depth + source hardening half.
#   WHAT CHANGED:
#     FIX B — FREQUENCY EXCEL COMPLETENESS + FORMAT PARITY (§16-1, §16-4, §15-1):
#       aggregate_frequency_data() and generate_frequency_xlsx() now accept `all_entries`
#       (the same PYQ + Zero-PYQ-scaffold list write_subtopic_manifest() writes from).
#       When supplied: (1) every all_entries subtopic seeds a Master Data row FIRST — so
#       Zero-PYQ scaffolds appear as all-zero rows, making the Excel taxonomy-complete by
#       construction, not just the manifest; (2) Format is taken directly from
#       entry['format'] (the manifest's own 4-way TEXT/FIGURAL/PASSAGE/DI value) instead
#       of being re-derived locally with a 2-way (TEXT/FIGURAL-only) image_role rule — so
#       Excel Format == manifest Format for every subtopic by construction, never merely
#       by coincidence. run_synthesise() updated to pass all_entries through. Backward-
#       compatible: all_entries=None reproduces the exact pre-v2.24.6 behavior.
#     FIX C — STRUCTURAL DI/PASSAGE TABLE DETECTION (SHARED AXIS CLASSIFIER v1.0 +
#       synthesise_subtopic): replaced the naive substring match
#       (`'|' in stem or 'table' in stem.lower()`) with a shared, single-source-of-truth
#       `_looks_like_table_stimulus()` helper — word-boundary table-keyword match
#       co-occurring with a real pipe-delimited row, or >=2 pipe-delimited rows alone.
#       Eliminates false positives on "vegetable"/"acceptable"/stray single pipes while
#       still catching real data tables. Used by BOTH classify_axis1() (the canonical
#       per-question classifier feeding axis_distribution) and synthesise_subtopic()'s
#       per-subtopic `fmt` derivation (previously two independent, driftable
#       implementations of the same rule — now one). MUST PROPAGATE (byte-identical) to
#       Step 8 MockCreateAudit S6-1b (verbatim classifier copy) — done, MockTestCreateAudit
#       v2.7.4.
#   PAIRS WITH: Framework_Blueprint v1.32 FIX A (§6 Format source: manifest, not Excel)
#   + FIX D (§2-1 Section↔Subject resolver) + FIX E (§2-3 over-coverage INFO branch).
#   Verified: master_data_completeness_test, excel_manifest_format_parity_test,
#   di_heuristic_false_positive_test design specified in Blueprint §9 S9-13 validation plan.
#
# v2.24 changes: MECHANIC / FORM-KEY ENGINE — permanent fix for the BV-10 same-mechanic
#   collision DEADLOCK CLASS (blocks Step 6 MockBlueprint on a large fraction of exams).
#   ROOT CAUSE (fixed here at source): _derive_question_mechanic() matched English-verbal
#   substring keywords only and silently fell back to the coarse concept_group for every
#   reasoning/quant/GA/regional subtopic, collapsing distinct forms (Number/Letter/Semantic
#   Series -> one "series") onto one label. BV-10 read that diversity-family label as a
#   duplicate-identity key -> arithmetically-forced, non-terminating deadlock.
#   WHAT CHANGED:
#     (1) NEW axis engine (derive_mechanic + canon_text/_has_word/_FAMILY_MAP/_QUALIFIERS):
#         word-boundary matching (no 'voice' in 'invoice', no 'clock' in 'clockwise');
#         verbal keywords GATED to verbal sections/formats; QUALIFIER-AWARE fine mechanic
#         so variants stay distinct; Devanagari/regional transliteration + subtopic_id
#         fallback so a mechanic is NEVER empty; DETERMINISTIC in (section,name) not in
#         volatile PYQ templates. Emits per subtopic: family (coarse, SOFT-cap axis) +
#         mechanic==form_key (fine, HARD-guard axis) + collision_domain (default=section).
#     (2) _derive_concept_group/_derive_question_mechanic kept as back-compat wrappers.
#     (3) question_mechanic + form_key + collision_domain now WRITTEN to the subtopic
#         MANIFEST (previously only concept_group was) and to section_rules.md, and are
#         round-tripped in rebuild_subtopic_manifest_from_section_rules().
#     (4) Zero-PYQ scaffold + _absent_entry now derive these via the engine (were slugify /
#         missing) so mixed-PYQ exams are consistent and never empty.
#     (5) NEW QV-13 quality gate: fails on empty/nondeterministic mechanic; warns on
#         intra-domain form_key collisions and question-shaped subtopic names.
#   PAIRS WITH: Step 6 B1 feasibility gate + two-tier BV-10a(HARD form_key)/BV-10b(SOFT
#   family cap) — delivered separately. Verified by step5_harness (21/21) + engine
#   extracted-from-this-file (13/13) + whole-document syntax parity.
#
# v2.24.1 changes: EXAM-INDEPENDENT fix for the BV-10a form_key-collision HALT class.
#   v2.24 collapsed family/question_mechanic/form_key onto ONE token whenever no
#   reasoning qualifier matched — always, on any subject exam — so any two subtopics
#   sharing a _FAMILY_MAP keyword (e.g. three "…Classification…" biochemistry subtopics)
#   got an identical form_key and Step 6 BV-10a HALTed two steps later. Latent in EVERY
#   single-section subject exam, not just one. WHAT CHANGED (defect report D1..D9):
#     (D1) form_key now derives from the subtopic's OWN identity base (→ unique subtopic_id),
#          NEVER the family token. Uniqueness is by construction, not by qualifier accident.
#     (D2) _FAMILY_MAP rows are (keywords, family, template_set); the keyword table fires
#          only for template_sets the exam DECLARES. _is_verbal() demoted to narrow-only.
#     (D3) collision_domain uses the collision-safe section_prefix (EC-M4).
#     (D5/D8) derive-once: mint subtopic_id → stamp_mechanic_axes() (asserts uniqueness) →
#          run_qv(), all reading the SAME stamped fields. _absent_entry/scaffold emit None
#          and are filled by the single stamp site. QV-13 is now FAIL (no allowlist); name
#          shape split to QV-13a (advisory).
#     (D7) subtopic_merges (TRUE duplicates only) replaces the retracted allowlist.
#     (D9) _extract_qualifiers() returns ALL matches, alphabetical, word-boundary-redundancy.
#   PER-EXAM INPUT: [ExamCode]_mechanic_overrides.json ONLY. Absent ⇒ legacy family
#   selection (REGR-1) + the always-on uniqueness improvement. REQUIRES Step 6 §7.1
#   (Blueprint): remove concept_group from the form_key fallback chain (now deliberately
#   shared). Verified: patched-code checks 6/6 (biochemistry unblock + EC-M1/M2/M6/M8/M17/M18).
#
# v2.24.5 changes: AUTOMATIC ZERO-PYQ FORMAT INFERENCE (no curator input). New pure
#   infer_zero_pyq_axes() + post-pass apply_zero_pyq_format_inference() refine each zero-PYQ
#   scaffold's format/answer_type/answer_cardinality from (1) NAME keywords (-> FIGURAL, same
#   heuristic as the PYQ path) and (2) same-topic PYQ siblings (UNANIMOUS non-TEXT format
#   inherited; >=2/3 NAT or MSQ inherited); else TEXT/option/single. Fires only on strong
#   evidence (name match, or >=2 unanimous/>=2-of-3 siblings); PYQ entries never touched; every
#   change logged (audit trail, no prompt). Runs before id-mint/stamp/QV/writers so section_rules
#   + manifest both carry the inferred axes; a zero-PYQ FIGURAL becomes a real Axis-1 supplier
#   (axis1_feasibility sees it, Step-7 dispatch renders it, Step-8 audits it). Proven by
#   blueprint_zero_pyq_inference_test.py.
#
# v2.24.4 changes: TAXONOMY 'How to use' WORDING FIX (docs only, no logic). The sub-topic guidance
#   now leads with the readable "Subject::Topic::Sub Topic Name" form (the Topic disambiguates
#   same-named sub-topics across topics — e.g. Kinematics under Mechanics vs Rotational Motion),
#   and clarifies the Sub Topic Id is only needed when a name repeats under the SAME topic.
#
# v2.24.3 changes: HUMAN-READABLE TAXONOMY EXPORT. New write_taxonomy_xlsx() emits
#   [ExamCode]_taxonomy.xlsx alongside subtopic_manifest.json — a plain 4-column list
#   (Subject | Topic | Sub Topic Name | Sub Topic Id, one row per sub-topic, sorted, with a
#   filterable header + a 'How to use' sheet) so the Step-6 operator can pick scope values
#   without reading JSON. Called from BOTH manifest writers (write_subtopic_manifest +
#   rebuild_...); added to deliver_final (now 6 files). Additive, generated from the same
#   manifest dict (JSON stays authoritative); openpyxl-absent → WARN, never a hard stop.
#
# v2.24.2 changes: LANGUAGE-AGNOSTIC MATCH DETECTION — closes the format-fidelity gap where
#   match-the-following questions were mis-tagged (and, downstream, mis-RENDERED as plain text
#   instead of a Word table). classify_axis2's MATCH rule relied on ENGLISH stem keywords
#   (match / list-I / column), so (a) non-English match papers and (b) matches whose List-I/
#   List-II body sits in a table (absent from stem_raw) fell through to DIRECT — silently
#   under-counting the MATCH format and producing a false readiness signal. WHAT CHANGED:
#     (1) NEW self-contained helper _opts_are_match_pairs() (+ _label_family, _MATCH_*_RE) in
#         the SHARED AXIS CLASSIFIER v1.0 block: detects a CROSS-DOMAIN label-pair OPTION shape
#         (A-I / 1-A / I-A / A-1; separators - u2013 u2014 : > arrow; bracketed or bare). Cross-
#         domain (left family != right family) rejects digit:digit ratios, coordinate pairs and
#         word-word hyphens. Column-level family resolves the roman-vs-letter 'I' ambiguity.
#     (2) classify_axis2 gains a THIRD MATCH trigger AFTER the two keyword rules — additive and
#         monotone: it can only convert a would-be non-MATCH class to MATCH, never the reverse
#         (proven over 240 stem x option x linked combinations; zero regressions).
#   MUST PROPAGATE (byte-identical) to Step 8 MockCreateAudit S6-1b (verbatim classifier copy).
#   E-8 classify_option_format left untouched (descriptive metadata, no functional coupling).
#   Verified: helper matrix 20/20 + invariant proof 240/240 + extracted-from-this-file parity.
#
# ═══════════════════════════════════════════════════════════════════════════
# STEP NUMBER NOTE — CANONICAL PIPELINE MAPPING
# This file is Step 5 (PYQExtract) in the canonical 11-step pipeline.
# The changelogs below (v2.0–v2.14) used an internal "Step 0/1/2…" shorthand:
#   internal "Step 0" = canonical Step 5  (PYQExtract, THIS file)
#   internal "Step 1" = canonical Step 6  (MockBlueprint)
#   internal "Step 2" = canonical Step 7  (MockCreate)
#   internal "Step 3" = canonical Step 8  (MockCreateAudit)
#   internal "Step 4" = canonical Step 9  (MockExplain)
#   internal "Step 5" = canonical Step 10 (MockExplainAudit)
#   internal "Step 6" = canonical Step 11 (MockDeliver)
# Changelogs are preserved as-is (historical). All ACTIVE code, docstrings,
# handoff messages, and documentation now use canonical step numbers exclusively.
# ═══════════════════════════════════════════════════════════════════════════
#
# v2.23 changes: THREE-AXIS FORMAT-DISTRIBUTION EXTRACTION — SHARED AXIS CLASSIFIER +
#   PER-SECTION TARGETS + PER-SUBTOPIC CAPABILITY (File 1 of the format-fidelity feature).
#   GOAL: a mock must replicate the exam's FORMAT MIX, not just its syllabus. This step
#   extracts the targets that Steps 6/7/8 enforce. A question is a TRIPLE on three
#   orthogonal axes; each PYQ question is now tagged on all three + a negative-polarity flag.
#
#   FIX A — SHARED AXIS CLASSIFIER v1.0 (new section, before synthesise_subtopic):
#     The single, canonical, exam-agnostic classifier. Step 8 (MockCreateAudit) re-tags
#     GENERATED questions with THIS SAME classifier — if the two ever diverge, every
#     distribution number is silently wrong, so it is authored ONCE here and referenced,
#     never re-implemented. It exposes:
#       • classify_axis1(q) → TEXT|FIGURAL|PASSAGE|DI          (STIMULUS / MEDIA)
#       • classify_axis2(q) → the EXCLUSIVE 8-class ladder     (STEM STRUCTURE)
#             LINKED (gate, decided by linked_group_id — shared stimulus serving 2+ Qs,
#             NOT by phrasing) → ASSERTION_REASON → MATCH → SEQUENCE → STATEMENT →
#             FILL_BLANK → ODD_ONE_OUT → DIRECT  (first-match-wins; SEQUENCE deliberately
#             above STATEMENT because the OPERATION is ordering). DIRECT is the residual.
#       • classify_axis3(q) → MCQ|MSQ|NAT                      (ANSWER MECHANISM)
#       • negative polarity is an ORTHOGONAL FLAG (is_negative), never an Axis-2 class:
#             "which pair is NOT correctly matched" = MATCH + is_negative, so counts stay clean.
#     Consolidates the pre-existing independent detectors (EC-8 A-R, EC-9 statement-combo,
#     EC-11 fill-blank, EC-12 negative, EC-13 matching) into ONE exclusive partition, and
#     adds SEQUENCE + ODD_ONE_OUT (narrowed to true "does not belong" classification).
#
#   FIX B — PER-QUESTION TAGGING: the extraction driver now calls tag_axes(q) in the
#     per-question enrichment loop (after linked_group_id + image_role are known), so
#     every question carries q['axis1'|'axis2'|'axis3'] alongside is_negative.
#
#   FIX C — PER-SUBTOPIC CAPABILITY (CATEGORY B): synthesise_subtopic now emits
#       • observed_axis2      — {AXIS2_CLASS: count} this subtopic's PYQ actually used
#       • presentation_family — the family key (mirrors Step 7 resolve_presentation_family)
#       • axis2_capability    — the forms this subtopic may FAITHFULLY take = observed ∪
#             family-menu ∪ {DIRECT} (+LINKED iff format ∈ PASSAGE/DI, since LINKED is
#             stimulus-locked). Step 6 reads this to guarantee rare-format reachability
#             (decision (c)); Step 7 renders only within capability (fabrication banned).
#
#   FIX D — PER-SECTION AXIS_DISTRIBUTION (CATEGORY A): new section-header block, the
#     3-YEAR per-paper averages of each Axis-1/2/3 class + the negative rate, computed by
#     compute_section_axis_distribution() over the 3 most-recent distinct years. Each
#     Axis-2 class carries an audit_mode ∈ {band, guarantee, float}: DIRECT always floats;
#     window_target = per_paper_avg × mocks_per_window; window_target < 1 → guarantee-only
#     (periodic ≥1/window), else band. Written to section_rules.md AND subtopic_manifest.json;
#     the rebuild-from-section_rules path parses it back (round-trip preserved).
#
#   framework_version stamp: v2.23. Steps 6/7/8 are Files 2–4 of this feature (separate turns).
#
# v2.22 changes: INHERENTLY-VISUAL SUBTOPIC DETECTION + MANIFEST inherently_visual FLAG.
#   ROOT CAUSE: Step 5 classifies format purely from PYQ observation: format='FIGURAL'
#   iff any question's image_role != 'none'. When PYQ image extraction fails (scanned
#   PDF, embedded-as-raster, missing media), inherently-visual subtopics like counting
#   figures, embedded figures, or mirror images are misclassified as format='TEXT'.
#   Step 7 then generates unanswerable text descriptions of figures students cannot see.
#
#   FIX A — KEYWORD HEURISTIC in synthesise_subtopic() (zero external dependency):
#     After the PYQ-based format assignment, if fmt == 'TEXT', a VISUAL_KEYWORD set is
#     checked against the subtopic name. If the name signals visual content (e.g.,
#     contains 'figure', 'diagram', 'mirror', 'venn', 'paper fold', etc.), fmt is
#     overridden to 'FIGURAL' and a default image_role of 'stem_only' is assigned.
#     The override is LOGGED: "INHERENTLY-VISUAL override: [subtopic] TEXT→FIGURAL."
#     The keyword set is exam-agnostic — it covers geometric/spatial/visual terms
#     universal across competitive exams. If a keyword match is wrong, the exam
#     curator can add figural_override=false in the taxonomy entry to suppress it.
#
#   FIX B — inherently_visual FLAG in subtopic manifest:
#     write_subtopic_manifest() now includes 'inherently_visual': true|false per entry.
#     Set true when Fix A fires, or when the entry has an explicit figural_override=true.
#     Downstream steps (Step 7 S3-2, Step 8) can read this flag directly from the manifest.
#
#   framework_version stamp: v2.22.
#
# v2.21 changes: DELIVERY FOOTER CROSS-REFERENCE.
#   Added S11-4: post-delivery footer rendering reference to Framework_DeliveryFooter.md
#   v1.3. Both per-batch (F1 mid-step) and final (F2 step-complete) deliveries now render
#   the standardized visual footer after every present_files call. Zero logic change.
#   framework_version stamp: v2.22.
#
# v2.20 changes: ZERO-PYQ MANIFEST COMPLETENESS FIX (Fix A + Fix C from BUGFIX report).
#   ROOT CAUSE: Step 5's manifest represented only PYQ-OBSERVED subtopics, not the COMPLETE
#   exam vocabulary. Exams whose syllabus defines subtopics with zero PYQ observations
#   (new syllabus additions, rarely-tested topics, etc.) produced an INCOMPLETE manifest.
#   Step 6 (Blueprint) then self-minted sequential IDs for these orphan subtopics (violating
#   the never-mint contract), and Step 7 (MockCreate) correctly HARD STOPPED at S3-8 because
#   the self-minted IDs existed in neither the manifest nor section_rules.
#   Discovered: SSC CGL Tier 2, Mock 1 — 7 syllabus-only subtopics absent from manifest.
#   This is the COMMON CASE for any exam with syllabus-defined topics that have no PYQ history.
#
#   FIX A — TAXONOMY SYNC PROTOCOL (new §15-1):
#     After PYQ-based synthesis completes, run_synthesise() now synchronises the entry list
#     with the exam's approved taxonomy. For every taxonomy-defined subtopic NOT already in
#     the PYQ-derived entries, a SCAFFOLD ENTRY is created with zero-PYQ defaults (observed_
#     count=0, confidence='absent', generic P1 pattern, all difficulty counts=0). These
#     scaffold entries flow through the normal write_section_rules() and write_subtopic_
#     manifest() paths, so the manifest and section_rules are COMPLETE by construction.
#     Taxonomy sources: (1) [ExamCode]_taxonomy_draft.json (primary — syllabus-faithful,
#     contains zero-PYQ subtopics), (2) approved Analysis doc [ExamCode]_PYQ_Analysis.docx
#     (additional — union, covers PYQ-discovered subtopics not in taxonomy_draft).
#     Edge cases EC-ZP-1 through EC-ZP-10 documented in §15-1.
#
#   FIX C — SCAFFOLD SECTION_RULES BLOCKS:
#     New make_zero_pyq_scaffold_entry() function produces a complete entry dict with all
#     fields format_entry() expects, using zero-PYQ defaults. The resulting section_rules
#     block carries observed_count=0, a generic P1 stem pattern with confidence='absent',
#     zero difficulty calibration, and a NOTE identifying it as a syllabus-only subtopic.
#     Step 7 uses these blocks for format/option guidance when generating zero-PYQ questions.
#
#   COMPLETENESS INVARIANT (new, added to §15):
#     len(manifest_subtopics) >= len(taxonomy_subtopics)
#     The manifest must cover the ENTIRE taxonomy, not just the PYQ-observed subset.
#     A PYQ-only manifest is a PARTIAL vocabulary that will break when the blueprint
#     includes syllabus-only subtopics. Taxonomy sync makes this hold by construction.
#
#   VALIDATION:
#     run_synthesise() logs taxonomy sync additions and prints a summary count.
#     New DoD items [22] and [23] verify taxonomy sync ran and completeness invariant holds.
#
#   framework_version stamp: v2.20. All generated_by stamps: v2.20.
#
# v2.19 changes: BATCH STOP LAW HARDENING + CLOSED DELIVERABLE SET CONTRACT.
#   ROOT CAUSE 1 — BATCH STOP: S8-1 had strong language (★★★ CRITICAL RULE ★★★,
#     explicit refusal script, accepted triggers) but lacked two elements proven
#     critical in PYQAnalyse SSC CGL Tier 2 failure: (a) prose-level "END THE
#     RESPONSE" instruction outside code blocks, (b) documented failure history.
#     The Python `break` stops the loop but doesn't stop Claude from writing
#     additional content after the loop. Added both elements to S8-2 and S8-3.
#
#   ROOT CAUSE 2 — DELIVERABLE SET: header OUTPUT FILES listed only 3 files but
#     actual final delivery (S11-2 PART B) is 6 files (subtopic_manifest.json + taxonomy.xlsx (v2.24)
#     added v2.14, PYQ_Frequency.xlsx added v2.13). No "NOTHING ELSE" qualifier,
#     no DO-NOT-DELIVER list, no pre-delivery checklist. Same gap pattern as
#     PYQAnalyse (unauthorized taxonomy_draft_v2.json delivery).
#
#   CHANGES:
#     (1) S8-2: added "END THE RESPONSE" prose block after `break` with
#         cross-framework failure reference (PYQAnalyse SSC CGL Tier 2).
#     (2) S8-3: added "END THE RESPONSE" instruction after continue prompt.
#     (3) Header OUTPUT FILES: updated to list all 5 final files + per-batch
#         file, with "(nothing else)" qualifiers and DO-NOT-DELIVER list.
#     (4) New S11-3: DELIVERABLE SET CONTRACT — closed sets for per-batch
#         (1 file) and final (5 files) deliveries, with DO-NOT-DELIVER lists
#         and pre-delivery checklist.
#     (5) DoD: 4 new items for closed-set verification.
#
#   framework_version stamp: v2.19.
#
# v2.18 changes: EXAM_CONFIG MARKING_SCHEME INTEGRATION (Step 2a v2.5 contract sync).
#   Root cause: Step 2a v2.5 replaced scalar marks_per_question/negative_marking with
#   per-range marking_scheme[] and added medium, level, question_types to exam_config.json.
#   Step 5 must read these new fields and propagate them to _meta, CATEGORY C, and
#   section_rules.md so downstream Steps 6-11 consume them correctly.
#
#   CHANGE 1 — PARAMETER SOURCE PRIORITY:
#     All PARAMETERs that previously read from "Exam Pattern document" (via AI interpretation)
#     now read from exam_config.json FIRST (structured, deterministic). AI detection from
#     PYQ papers becomes VALIDATION ONLY — if PYQ-detected value conflicts with exam_config,
#     exam_config wins and a warning is logged.
#     Affected: PARAMETER 1 (time_per_q_sec), PARAMETER 2 (negative_marking),
#       PARAMETER 3 (language — new: medium from exam_config takes priority),
#       PARAMETER 5 (question_types), PARAMETER 6 (marks_per_question).
#
#   CHANGE 2 — PARAMETER 6 DERIVATION FROM marking_scheme[]:
#     marks_per_q is now derived from exam_config.marking_scheme[] by grouping ranges
#     by question_type and taking the MAX correct_marks per type. Example:
#       GATE marking_scheme has MCQ ranges at 1m and 2m → marks_per_q['MCQ'] = 2.
#       CSIR NET has MCQ ranges at 2m and 4m → marks_per_q['MCQ'] = 4.
#     This preserves backward compatibility with the dict format Steps 7/8/9 expect.
#     negative_marking_by_type similarly derived: per type, take the MIN (most negative).
#
#   CHANGE 3 — NEW _META FIELDS:
#     marking_scheme, level, medium stored in progress['_meta']. Propagated to
#     exam_meta dict in run_synthesise and written to CATEGORY C header.
#
#   CHANGE 4 — CATEGORY C HEADER EXPANSION:
#     write_section_rules now writes: marking_scheme, level, medium.
#     marks_per_q and negative_marking RETAINED as summary scalars for backward compat
#     (derived from marking_scheme). Downstream Steps 7/8/9 can read either the scalar
#     (legacy) or the full marking_scheme (new) via cat_c().
#
#   CHANGE 5 — §14 SCHEMA REFERENCE updated with new CATEGORY C fields.
#
#   framework_version stamp: v2.18.
#
# v2.17 changes: FREQUENCY XLSX ACCURACY & COMPLETENESS OVERHAUL (9 fixes).
#   Root cause: Comparative analysis of framework-generated xlsx vs manually-verified
#   PYQ analysis for MPPSC Botany revealed: 38% data loss (93/150 Qs mapped), inflated
#   percentages (denominator = mapped Qs not exam total), binary importance (useless),
#   missing question numbers, missing coverage validation. All traced to §16 xlsx code.
#
#   FIX-1 [CRITICAL]: % OF SUBJECT DENOMINATOR — write_master_data, write_topic_analysis,
#     and write_section_sheet all used section_totals (sum of MAPPED questions) as
#     denominator. For exams where classification drops questions, this inflates all
#     percentages. FIXED: generate_frequency_xlsx now reads exam_config.json to get
#     exam_total_questions (the REAL exam total per section from the pattern). All %
#     calculations use exam total as denominator. Fallback: if exam_config absent,
#     use section_totals (current behaviour) with a warning.
#
#   FIX-2 [CRITICAL]: COVERAGE VALIDATION — new XLSX-F9 check: sum of all subtopic Qs
#     across all sections must equal total_questions from exam_config. If mismatch > 5%,
#     WARN: "Frequency xlsx accounts for [N] Qs but exam has [M]. [M-N] questions were
#     not classified to any subtopic. Downstream blueprint will be inaccurate."
#     This single check would have caught the MPPSC 93≠150 bug.
#
#   FIX-3 [HIGH]: TOPIC NAME CONSISTENCY — write_topic_analysis topic names must be
#     IDENTICAL to write_master_data topic names. Added assertion: every topic in Topic
#     Analysis sheet must exist verbatim in Master Data Subject column. Prevents the
#     truncation mismatch bug (e.g., "Molecules...Biolog" vs "Molecules...Relevant").
#
#   FIX-4 [HIGH]: DUPLICATE SUBTOPIC DETECTION — generate_frequency_xlsx now checks for
#     duplicate (section, topic, subtopic) keys before writing. If found, WARN and merge.
#
#   FIX-5 [MEDIUM]: MUST_PREPARE NULL HANDLING — empty string '' replaced with '—' for
#     non-Must-Prepare subtopics. Prevents NaN in downstream consumers.
#
#   FIX-6 [MEDIUM]: NEAR-DUPLICATE SUBTOPIC WARNING — after aggregation, check for
#     subtopic name pairs within same topic with >75% similarity. Print warning.
#     Aligns with Framework_PYQAnalyse v2.4 Unique Domain Property checks.
#
#   FIX-7 [LOW]: SINGLE-YEAR TREND/CONSISTENCY — for exams with only 1 year of data,
#     Trend is now 'N/A (1 year)' instead of 'Insufficient Data', and a note is added
#     to Summary Dashboard explaining that trend/consistency columns are not meaningful.
#
#   FIX-8 [LOW]: SECTION NAME IN TOPIC ANALYSIS — Topic Analysis sheet now uses full
#     section name (no truncation). Section names in Master Data and Topic Analysis
#     must be byte-identical.
#
#   FIX-9 [LOW]: SUMMARY DASHBOARD HEADER — now includes exam_code from exam_config
#     (not from ExamCode parameter which could have typos). Uses exam_config['exam_name']
#     if available for human-readable title.
#
#   framework_version stamp: v2.17. All generated_by stamps: v2.17.
#
# v2.16 changes: EXAM-AGNOSTIC RIGIDITY AUDIT (6 fixes).
#   RIGID-1 [CRITICAL]: "Shift" hardcoded in 3 regex patterns — parse_shift(),
#     extract_shift_from_filename(), sort_papers_recency_first(). IBPS (Slot), RRB (Phase),
#     GATE (Session) PYQ filenames had their session number silently ignored (always 'S1').
#     FIXED: session_keyword now read from exam_config.json at session start (matching
#     PYQSort's contract). All shift/session regexes built dynamically via
#     build_session_re(). Fallback: 'Shift' when exam_config absent.
#   RIGID-2 [CRITICAL]: Language detection only checked ASCII vs Devanagari (U+0900-097F).
#     Regional exams in Tamil, Telugu, Bengali, Kannada, Malayalam, Gujarati, Odia, Punjabi
#     would all classify as 'english'. FIXED: INDIC_RANGES expanded to cover all 9 major
#     Indic scripts. language now detects 'regional' when any non-Devanagari Indic script
#     dominates. Marathi (Devanagari script) correctly maps to 'hindi' with a NOTE.
#   RIGID-3 [IMPORTANT]: Display strings hardcoded "Shift-[N]" in verification summary,
#     detection sample printout, and sort docstrings. FIXED: all use session_keyword variable.
#   RIGID-4 [IMPORTANT]: parse_taxonomy_level() only recognized Subject/Domain/Topic/Chapter.
#     Exams using Unit/Module/Section/Part/Block/Area as PYQ headings collapsed to level 3.
#     FIXED: 12+ heading patterns now recognized for level 1 and level 2.
#   RIGID-5 [MODERATE]: determine_strip_mode() used English-only section/topic keywords.
#     Hindi-medium exams with headings like "गणित"/"तर्कशक्ति" always fell to default.
#     FIXED: Hindi equivalents added for quantitative/reasoning/english/factual detection.
#   RIGID-6 [MODERATE]: NOTE_PAT only matched English + Hindi NOTE keywords. Regional
#     script NOTE blocks (Tamil குறிப்பு, Telugu గమనిక, Bengali দ্রষ্টব্য, etc.) missed.
#     FIXED: 9 regional-language NOTE keywords added to NOTE_PAT.
#   framework_version stamp: v2.16. All generated_by stamps: v2.16.
#   CROSS-STEP SYNC FIXES (found during final sync audit):
#     SYNC-1: _read_session_keyword() used fixed path '/mnt/project/exam_config.json'
#       but PYQAnalyse saves it as '{ExamCode}_exam_config.json' and PYQSort discovers
#       via glob('*_exam_config.json'). FIXED: now uses same glob pattern.
#     SYNC-2: is_shift_tag() and is_taxonomy_heading() used \d{2} (exactly 2-digit day)
#       for date label detection, but real PYQ dates can have single-digit days (e.g.
#       [5-Jan-2024]). PYQAnalyse correctly uses \d{1,2}. FIXED: all 4 occurrences now
#       use \d{1,2} — aligned with PYQAnalyse.
#     SYNC-3: Stale generated_by stamp v2.15 in rebuild_subtopic_manifest_from_section_rules
#       (missed in bulk v2.16 update). FIXED: now v2.16.
#
# v2.15 changes: DEEP-AUDIT-2 (13 bugs fixed).
#   BUG-D01 [CRITICAL]: generate_frequency_xlsx() was never called in run_synthesise() —
#     the entire §16 xlsx feature was dead code. FIXED: run_synthesise() now calls it and
#     passes xlsx_path to deliver_final().
#   BUG-D02 [CRITICAL]: deliver_final() had no xlsx_path parameter — xlsx never delivered.
#     FIXED: xlsx_path added to signature and delivery list.
#   BUG-D03 [CRITICAL]: per-section option_label_format read from option FORMAT TYPE
#     ('single_value') instead of option LABEL style ('1/2/3/4' vs 'A/B/C/D'). FIXED:
#     extraction now detects and stores option_label per question; per-section writer
#     aggregates from the correct field.
#   BUG-D04: stale comment version v2.12 → v2.15 (line 2621 in v2.14).
#   BUG-D05: stale generated_by stamps v2.11 → v2.15 in manifest writers.
#   BUG-D06: self-referencing "Step 0" in handoff/DOD → canonical "Step 5".
#   BUG-D07: option_label_format auto-detection implemented in S1-3 (was documented
#     but never coded — always defaulted to '1/2/3/4').
#   BUG-D08: dead code removed from aggregate_frequency_data (str(tuple).startswith('_')).
#   BUG-D09: must_prepare threshold now scales with available years
#     (>= min(4, len(all_years)) instead of fixed >= 4).
#   BUG-D10: _compute_structural_changes deduplication — FIGURAL subtopics no longer
#     produce both REMOVED and FIGURAL-eliminated entries.
#   BUG-D11: §12 integration section updated to canonical step numbers.
#   BUG-D12: docstring schema example updated to v2.15.
#   BUG-D13: extract_year_from_filename documented as accepting name string only.
#   framework_version stamp: v2.15. All generated_by stamps: v2.15.
#
# v2.14 changes: DEEP-AUDIT (1 fix). framework_version stamp in write_section_rules was
#   v2.12 — missed the v2.13 bump. Every section_rules.md generated under v2.13 would say
#   framework_version: v2.12 instead of v2.13. FIXED: stamp now reads v2.14. No behaviour
#   change; output is byte-identical except the version string in the EXAM_STRUCTURE header.
#
# v2.13 changes: FREQUENCY XLSX OUTPUT — adds [ExamCode]_PYQ_Frequency.xlsx as a new
#   synthesis-phase output. The xlsx contains year-wise question frequency data for every
#   subtopic: per-year counts, avg/paper, consistency, trend (Rising/Declining/Stable),
#   importance (High/Medium/Low), must-prepare flags, rank-in-topic, and format classification.
#   8 sheets: Summary Dashboard, Master Data, Topic Analysis, Trend Analysis, + 1 per section.
#   All data aggregated from analysis_progress.json (no new extraction needed). All derived
#   metrics are deterministic formulas. Downstream consumer: Step 6 (MockBlueprint) reads
#   this xlsx as its "Frequency Excel" input alongside Analysis docs. 8-item xlsx validation
#   checklist (XLSX-F1 through XLSX-F8). 6 edge cases (EC-F1 through EC-F6). New output added
#   to §11 delivery list and DEFINITION OF DONE. Implementation in §16.
#
# v2.12 changes: DIFFICULTY LABEL VOCABULARY (Question Metadata Index — Step-0 half).
#   Adds difficulty_labels to the EXAM_STRUCTURE (CATEGORY C) header block written to
#   section_rules.md — the CANONICAL, exam-overridable difficulty vocabulary that becomes the
#   stored/rendered Complexity tag in the new per-question registry.question_index (seeded by
#   Step 1, filled by Step 2, certified by Step 3, rendered by Step 6). Default
#   ['Easy','Medium','Hard']; an exam may override (e.g. a 2- or 5-band set). Documents the
#   fixed alias between the three pre-existing difficulty spellings — Step-0 calibration
#   Simple/Medium/Hard, Step-1 schedule count keys simple/medium/hard, canonical label
#   Easy/Medium/Hard: simple→Easy, medium→Medium, hard→Hard. NO analysis behaviour changes:
#   difficulty_labels is written with its default and the PYQ_DIFFICULTY_CALIBRATION path is
#   untouched, so a non-overriding exam's section_rules is byte-identical apart from the one new
#   header line. Also corrects two stale embedded version literals (v2.10→v2.12) in
#   write_section_rules so the generated file's framework_version tracks the spec. Part of the
#   cross-step Question Metadata Index contract (Contract_QuestionMetadataIndex v1.0). Validated:
#   field write + default + alias proven in the Phase-1 harness before encoding.
#
# v2.11 changes: ISSUE 2b — THREE MANDATE TYPES a flat per-id list cannot express.
#   mandatory_every_mock (v2.10) only says "this ONE id in EVERY mock". Real exams also
#   need: (a) GROUP-PRESENCE — "≥1 of a subtopic GROUP per mock" (e.g. any one 3D-mensuration
#   solid, where forcing all members would over-allocate); (b) PER-WINDOW CADENCE — "≥1 every
#   N mocks" (e.g. an every-alternate-mock topic); (c) MIN-COUNT — "≥k Q of this subtopic per
#   mock" (e.g. a two-question argument/ethical requirement). v2.11 makes all three DATA,
#   round-trippable through section_rules exactly like the v2.10 mandate fields:
#     • format_entry emits two more per-block lines — mandatory_group (group name) and
#       min_count (int). min_per_series_window (the cadence field) already round-tripped since
#       v2.10; it is now ROLLED UP and enforced downstream rather than inert.
#     • write_subtopic_manifest + rebuild_subtopic_manifest_from_section_rules collect three
#       new top-level manifest structures: mandatory_groups {group:{members:[ids],min}},
#       cadence_windows {id:N}, min_counts {id:k}, plus mandatory_group/min_count on each
#       subtopic's mandates block.
#   ENFORCEMENT SPLIT (documented for Step 1/2; encoded there separately): group-presence and
#   min-count are per-mock (Step 1 places them, Step 2 S3-17 verifies + gates); CADENCE is a
#   CROSS-mock constraint (Step 1 sliding-window rule only — Step 2 sees a single mock and
#   cannot verify it). All checks validated in Python (group/cadence/min-count) before encoding.
#   Exam-agnostic: empty config ⇒ every new structure empty ⇒ vacuous no-op, never a false stop.
#
# v2.10 changes: MANDATE ROUND-TRIP FIX — the subtopic_manifest is now reproducible
#   from section_rules.md ALONE. ROOT CAUSE: alternation_groups and min_per_series_window
#   were read ONLY from ephemeral in-memory entry fields (e['alternation_group'] etc.);
#   they were never emitted into section_rules and never parsed back, so a manifest
#   rebuilt from an existing section_rules file lost ALL alternation + cadence data. And
#   the mandatory_every_mock detector was a brittle single-sentence, "mock"-only regex
#   that missed real NOTE wording like "MANDATORY ... 1Q per every paper". On SSC CGL T1
#   this produced mandatory_every_mock=[2 subtopics] and alternation_groups={} — the empty
#   mandate data that let Step 1 place CI+SI together and omit Direction Sense / Address
#   Matching. FIX (exam-agnostic): (1) format_entry now EMITS three round-trippable mandate
#   lines per subtopic block — mandate_every_mock / alternation_group / min_per_series_window;
#   (2) mandatory detection robustified to _mandate_from_note() (NOTE mentions MANDATORY
#   *and* an every/per mock|paper phrase, sentence-independent), with an explicit
#   mandate_every_mock line taking precedence; (3) NEW rebuild_subtopic_manifest_from_
#   section_rules() reconstructs a COMPLETE manifest from the section_rules file alone
#   (no source PYQ needed) — the supported path to regenerate a missing/incomplete manifest,
#   and it WARNs on any id-less block that cannot be joined. Validated in Python against the
#   real SSC section_rules (Direction Sense minted mandatory; ci_si alternation group formed)
#   BEFORE encoding. OUT OF SCOPE (Issue 2b, needs NEW manifest fields): group-presence
#   mandates ("≥1 of a 3D-mensuration group per mock"), per-window cadence, and min-count
#   mandates — a flat per-id mandatory_every_mock cannot model them.
# Multi-round audited: all known bugs fixed (v1.0 through v2.2).
# v2.2 changes: BATCH_SIZE=3 strictly prohibited from being overridden (§8-1);
#   minimum year coverage upgraded from 3 years to MANDATORY 5 years (§1-6);
#   both rules explicitly marked non-negotiable with zero exceptions when PYQ available.
# v2.3 changes: Fully exam-agnostic — all hardcoded exam names/folder IDs removed from
#   examples and comments. §13 PROOF section retained as it is explicitly illustrative.
#   BUG-C01 fix: PYQ_DIFFICULTY_CALIBRATION now writes is_inferred flag per level.
#   BUG-C02 fix: years list + raw_count now written per PYQ_STEM_PATTERN (QV-11 needs it).
#   BUG-C04 fix: option_format written as full dict (BUG-B15 compliance: primary,
#     recent_format, changed_recently, all_observed) — not collapsed to single string.
#   BUG-C05 fix: paragraph_count and topic_domains now written in PYQ_PASSAGE_STRUCTURE.
#   BUG-C07 fix: QV-5b added — fixed_set type must have non-empty fixed_option_texts.
#   NEW: EXAM_STRUCTURE header block auto-written to section_rules.md (new CATEGORY C).
# v2.4 changes: SUBTOPIC_ID CONTRACT (cross-step architectural fix). Step 0 is now the
#   SINGLE SOURCE OF TRUTH for the subtopic vocabulary. Every subtopic gets a stable,
#   deterministic subtopic_id (minted by make_subtopic_id/slugify), written as the first
#   field of each --- Subtopic: --- block AND into a new machine-readable manifest
#   [ExamCode]_subtopic_manifest.json. Step 1 and Step 2 join on subtopic_id, never on
#   display-name string-match. This permanently eliminates the Step0/Step1 name-drift that
#   caused Step 2 join failures (~70% name mismatch on SSC CGL T1). See §15 for the contract.
#   NEW: STRUCTURAL_CHANGES_BY_YEAR block computed from PYQ data and written.
#   NEW: figural_banned flag per section computed from observed PYQ r_avg data.
#   NEW: max_per_paper + typical_per_paper per subtopic (Step 2 L3 ceiling source).
#   NEW: recycled_datasets detection added to PYQ_CONTEXT_POOL.
#   NEW: §14 CATEGORY C documented for exam-level header fields.
#   NEW: Auto-detected params (time/marks/options/language) stored in _meta + written.
#
# v2.5 changes: MSQ CONTRACT — DETECTION LAYER (cross-step MSQ extension, Step 0 half).
#   The whole MSQ path is DORMANT behind multi_select_allowed (default false): for any
#   exam without multi-select (SSC CGL, NEET, IBPS, UPSC, CAT, …) v2.5 behaves byte-for-
#   byte like v2.4. Changes activate ONLY when multi_select_allowed=true (e.g. GATE).
#   ROOT-CAUSE FIX (EC-A): the v2.4 is_msq detector (r'select all|which.*are correct')
#     FALSE-MATCHED statement-combination MCQs (EC-9, "Which is/are correct? 1.Only A …"),
#     which are single-answer. v2.5 keys MSQ detection on OPTION SHAPE (combo-label
#     options ⇒ NOT MSQ), a provenance-proof signal, not stem wording. Empirically
#     validated against real docx fixtures (both directions) before encoding.
#   NEW (answer_cardinality): per-subtopic answer_cardinality ∈ {single, multi} is the Step 2 dispatch
#     unit (CATEGORY B). A subtopic is uniformly single- or multi-answer (whole-subtopic
#     mode) — so the per-mock allocation schema needs NO change downstream. msq_freq% also
#     written. Per-question is_msq retained on the record.
#   NEW (k contract): msq_k_mode ∈ {fixed, variable} and msq_k captured from the Exam
#     Pattern doc (NOT from PYQ — PYQ has no answer key, so k is unextractable; documented).
#   NEW (marking): negative_marking_by_type + partial_credit captured into EXAM_STRUCTURE
#     (consumed later by Step 4; dormant now). MSQ usually carries no negative marking.
#   NEW (difficulty): E-9 score_difficulty adds an MSQ cognitive-load term (+1, analogous
#     to the negative_question term) — independently evaluating every option is strictly
#     harder. Step 3 B-DIFF mirrors this. Cascades into Step 1 difficulty allocation.
#   CHANGED (EC-7): rewritten — Step 2 now GENERATES MSQ per the answer_cardinality contract
#     (was: "Step 2 skips MSQ subtopics"). EC-A documents the statement-combination guard.
#   All MSQ fields are exam-discovered/config-driven — zero exam names hardcoded.
#
# v2.8 changes: NAT DETECTION LAYER (Numerical-Answer-Type; cross-step NAT extension,
#   Step 0 half). Adds the SECOND answer-type axis to the unified vocabulary: per-subtopic
#   `answer_type` ∈ {option, numerical}, orthogonal to answer_cardinality. A subtopic resolves
#   to 'numerical' (NAT) when nat_allowed (PARAMETER 11, from the exam pattern) AND a majority
#   of its observed Qs have ZERO selectable options — no text options and no option-images
#   (image_role none|stem_only, never options_only|stem_and_options, so a figural NAT with a
#   problem diagram counts but a figural MCQ does not). New PARAMETER 11 captures the answer
#   model from the exam pattern (nat_answer_type ∈ {integer, real}, nat_tolerance, parametric
#   nat_instruction) — value/tolerance are answer-key info and so, like msq_k, come from the
#   pattern, never from PYQ. section_rules now carries answer_type + nat_freq per subtopic
#   (CATEGORY B) and nat_allowed / nat_present / nat_answer_type / nat_tolerance / nat_instruction
#   in EXAM_STRUCTURE — wiring the Explain step's explicit answer_type resolution path. NAT
#   marking reuses negative_marking_by_type under the 'NAT' key (additive). FULLY DORMANT:
#   default answer_type='option', nat_allowed=false ⇒ the NAT fields are inert defaults and
#   downstream behaviour is byte-for-byte the v2.7 behaviour for every non-NAT exam. Validated:
#   AST clean; dormancy + detection parity proven on synthetic single-answer / MCQ / NAT inputs.
#   framework_version stamp v2.7 → v2.8.
#
# v2.7 changes: VOCABULARY UNIFICATION — PHASE 0 (rename only; NAT prep). Part of the
#   cross-step move to ONE canonical answer-type vocabulary (answer_type + answer_cardinality)
#   shared by Steps 0-4, so the Explain step's contract and the Create/Audit steps stop using
#   different names for the same concept. This phase is a PURE RENAME with NO behaviour change:
#     • per-subtopic `answer_mode` -> `answer_cardinality` (identical {single,multi} values),
#       written to section_rules CATEGORY B under the new field name.
#   Non-NAT exams are byte-identical to v2.6. Readers downstream accept the old field name as a
#   fallback (existing section_rules files keep working). Validated: AST clean; the MSQ
#   generation/audit behaviour is unchanged (proven via the cross-step e2e harness on both
#   old-name and new-name artefacts). framework_version stamp v2.6 -> v2.7.
#
# v2.6 changes: MSQ AOTA POLICY FLAG (completes D5; closes the only open cross-step item
#   from the MSQ extension). Adds msq_allow_aota (bool, default false) to EXAM_STRUCTURE so
#   the "All of the above under MSQ" policy is actually SETTABLE — v2.5 read it everywhere
#   with a default of false but provided no place to write it, so the flag could only ever
#   be false. Now: PARAMETER 10 documents detection from the Exam Pattern; the EXAM_STRUCTURE
#   writer emits `msq_allow_aota: <bool>` into section_rules.md; the exam_meta dict and the
#   meta_raw reader carry it; §14 schema documents it; the auto-detected-params display
#   surfaces it. Step 2 (R-MSQ-ESCAPE / G-MSQ-SET) and Step 3 (A-MSQ-KEY) already read it
#   directly from section_rules, so no further downstream change is needed. Fully DORMANT
#   when multi_select_allowed=false (default false ⇒ byte-identical to v2.5 for every
#   single-answer exam). Writer framework_version stamp bumped v2.5 → v2.6. Zero exam names
#   hardcoded.
#
# PURPOSE:
#   Read actual PYQ (Previous Year Question) papers in docx format.
#   Extract per-subtopic question patterns, templates, difficulty calibration,
#   wrong option structure, and format rules.
#   Write [ExamCode]_section_rules.md — the pattern reference Step 2 uses
#   to generate questions indistinguishable from real PYQ.
#
# PIPELINE POSITION (CANONICAL step numbers):
#   Step 5 PYQExtract  (parallel) ↘
#                                  → Step 7 → Step 8 → Step 9 → Step 10 → Step 11
#   Step 6 MockBlueprint (parallel) ↗
#
#   Steps 5 and 6 are PARALLEL prerequisites for Step 7.
#   Both run in [ExamCode] project (exam-specific).
#   Both deliver outputs as downloadable files — user manually uploads to [ExamCode] project.
#   Step 5 and Step 6 do NOT depend on each other.
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains zero hardcoded exam values.
#   E-1 through E-11 define universal extraction operations.
#   Content discovered differs by exam — from the PYQ papers.
#   Same spec runs for SSC CGL, GATE, NEET, UPSC, CAT, regional exams.
#
# INPUTS:
#   Scenario A — PYQ available (normal case):
#     Provided via: PYQ: <<Google Drive folder link>>  in trigger
#     Claude scans the folder recursively — any subfolder structure works.
#     Folder name, Drive account, subfolder names: all irrelevant.
#     Only .docx files are collected; everything else is ignored.
#     OPTIONAL: Exam Pattern document in project knowledge or uploads
#               (image/PDF/docx — used to detect time/Q, marks/Q, Q-types)
#
#   Scenario B — PYQ not available for this exam:
#     No PYQ: link in trigger. No .docx files in uploads.
#     MANDATORY: Analysis Word docs in project knowledge (same as Step 1)
#     Result   : All subtopics written as confidence='absent' in section_rules.md
#                Step 2 uses Claude training knowledge for pattern generation
#
#   NO CONFIG FILE REQUIRED: all parameters auto-detected from documents.
#
# TRIGGER FORMAT:
#   Step 5: PYQExtract PYQ: <<Google Drive Link>>       -- process PYQ from Drive (required)
#   Step 5: PYQExtract --status                          -- show progress dashboard
#   Step 5: PYQExtract --synthesise ALL                  -- re-synthesise only
#
#   Trigger matching is case-insensitive.
#   ExamCode read from exam_config.json in project knowledge (set during Step 2a PYQDraft).
#
#   PYQ parameter (REQUIRED — v2.24.8, standardized with Step 4/Step 2b):
#     PYQ: <<Google Drive folder link>>
#     Link can point to:
#       • A flat folder (all docx files directly inside)
#       • A folder with year subfolders (2019/, 2020/, ... — Claude scans all recursively)
#       • Any nesting depth — Claude walks the full tree collecting all .docx files
#     Extract folder ID from link automatically:
#       https://drive.google.com/drive/folders/FOLDER_ID  → ID = FOLDER_ID
#       https://drive.google.com/drive/folders/FOLDER_ID?usp=sharing → same
#
#   If PYQ parameter absent: HARD STOP (v2.24.8). PYQ papers must be in Google
#   Drive — the local project/uploads fallback for the PYQ .docx corpus was
#   removed to standardize with Step 4 (PYQCount) and Step 2b (PYQScan), which
#   have always required Drive with no fallback. The Exam Pattern document and
#   any existing Analysis doc are UNAFFECTED — those small reference/state files
#   still come from project knowledge or chat upload, same as before.
#
#   Examples:
#     PYQExtract PYQ: https://drive.google.com/drive/folders/[YOUR_FOLDER_ID]
#     PYQExtract --status
#
# NO CONFIG FILE REQUIRED:
#   All parameters are auto-detected from the Exam Pattern document and PYQ papers.
#   You only need to upload documents — no JSON config to create or maintain.
#
# OUTPUT FILES (CLOSED SETS — see S11-3 for full contract):
#
#   PER-BATCH delivery (1 file, nothing else):
#     [ExamCode]_analysis_progress.json  -> batch accumulator; delivered after each batch
#
#   FINAL delivery (6 files, nothing else):
#     [ExamCode]_section_rules.md        -> PRIMARY: upload to [ExamCode] project knowledge
#     [ExamCode]_subtopic_manifest.json  -> upload to [ExamCode] project knowledge
#     [ExamCode]_taxonomy.xlsx           -> human-readable Subject/Topic/Sub-topic list (v2.24);
#                                           browse it to pick Step-6 scope values (no JSON needed)
#     [ExamCode]_PYQ_Frequency.xlsx      -> keep for Step 6 input
#     [ExamCode]_analysis_progress.json  -> keep locally (resume if adding papers later)
#     [ExamCode]_analysis_summary.md     -> human review audit trail
#
#   DO NOT DELIVER:
#     ✗ Any intermediate scripts or pipeline files
#     ✗ Any temporary JSON or working files
#     ✗ Input PYQ .docx files (these are INPUTS, not outputs)
#     ✗ Any renamed or versioned variants of the above files
#
# DRIVE USAGE:
#   Google Drive is used ONLY for reading PYQ .docx input files.
#   No output file is ever uploaded to Google Drive.
#   section_rules.md goes to: [ExamCode] Claude project → Files / Knowledge section.
#
# OVERRIDE RULE:
#   section_rules.md is ALWAYS regenerated from analysis_progress.json.
#   NEVER edit section_rules.md manually — re-synthesise instead.
#   Updating section_rules.md mid-series is SAFE.
#   Existing mocks unaffected. Future mocks use improved patterns.

---

## §1 — SESSION START

No config file required. All parameters are auto-detected from the Exam Pattern
document and PYQ papers. The only inputs are documents the user already has.

### S1-1 — Trigger parsing and ExamCode detection

```
Trigger: PYQExtract  PYQ: <<link>>  [--mode]
Trigger matching is case-insensitive.

ExamCode: alphanumeric + underscore only (e.g. SSC_CGL_TIER1, GATE_CS, IBPS_PO).
  If ExamCode contains invalid chars: flag and ask to correct.

PYQ parameter (REQUIRED for paper-processing modes — v2.24.8, standardized with
Step 4/Step 2b; not needed for --status or --synthesise, which don't read the
PYQ corpus):
  Format : PYQ: <<Google Drive folder URL>>
  Parsing: extract folder ID from URL using regex:
             r'drive\.google\.com/drive/folders/([A-Za-z0-9_-]+)'
  Example: PYQ: https://drive.google.com/drive/folders/[YOUR_FOLDER_ID]
             → pyq_drive_folder_id = '[YOUR_FOLDER_ID]'

  If PYQ parameter present    → use Google Drive as source (S1-2 Drive path)
  If PYQ parameter absent AND mode is auto (none) → HARD STOP: "PYQExtract
    requires PYQ: <<Google Drive folder link>>. The local project/uploads
    fallback for PYQ corpus files was removed (v2.24.8)."
  If PYQ parameter absent AND mode is --status/--synthesise → fine, proceed
    (these modes don't re-scan the PYQ corpus).
  If link format unrecognised → flag: "Cannot extract folder ID from link.
                                       Expected: https://drive.google.com/drive/folders/ID"

Mode flags:
  (none)           -> auto-mode: scan Drive folder (PYQ: required), process pending papers
  --status         -> print progress dashboard, then HALT
  --synthesise ALL -> re-synthesise from existing progress.json, skip paper processing
  --synthesise [S] -> synthesise named section only

# Parse mode from trigger (extract flag after ExamCode and optional PYQ: param)
# mode is set here and used throughout session-start logic below.
# Examples:
#   "PYQExtract"                        → mode = None
#   "PYQExtract --status"               → mode = '--status'
#   "PYQExtract --synthesise ALL"       → mode = '--synthesise ALL'
#   "PYQExtract PYQ: <<link>>"          → mode = None
mode = None   # set from trigger parsing above; None = auto-mode

import json, os, re, ast, glob
from collections import Counter
from difflib import SequenceMatcher
import math
from functools import reduce

# ── v2.16 RIGID-1: SESSION KEYWORD FROM exam_config.json ─────────────────────
# The session keyword (Shift/Slot/Phase/Paper/Session) varies by exam.
# PYQSort already reads it from exam_config.json; this file MUST do the same.
# Used to build all shift/session detection regexes dynamically.
# Fallback: 'Shift' when exam_config.json absent or field missing.
#
# exam_config.json examples:
#   "session_keyword": "Shift"     (SSC CGL, SSC CHSL, SSC MTS)
#   "session_keyword": "Slot"      (IBPS PO, IBPS Clerk, SBI PO)
#   "session_keyword": "Phase"     (RRB NTPC, RRB Group D)
#   "session_keyword": "Paper"     (UPSC CSE, UPSC CAPF)
#   "session_keyword": "Session"   (GATE, CAT)

def _read_session_keyword():
    """Read session_keyword from exam_config.json. Fallback: 'Shift'.
    v2.16 SYNC FIX: PYQAnalyse saves the file as {ExamCode}_exam_config.json (with
    prefix), and PYQSort discovers it via glob('*_exam_config.json'). This function
    MUST use the same glob pattern — a fixed path like 'exam_config.json' would miss
    the prefixed file and silently fall through to the 'Shift' default."""
    import glob as _glob
    # Search order: project knowledge (primary), then uploads (fallback)
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        matches = sorted(_glob.glob(os.path.join(search_dir, '*exam_config.json')))
        for cfg_path in matches:
            try:
                with open(cfg_path, encoding='utf-8') as f:
                    cfg = json.load(f)
                return cfg.get('session_keyword', 'Shift')
            except Exception:
                continue
    return 'Shift'

session_keyword = _read_session_keyword()

# ── v2.18: GENERAL EXAM CONFIG READER ──────────────────────────────────────
# Reads marking_scheme[], level, medium, question_types from exam_config.json.
# These are the new fields added by Step 2a v2.5 (standardized xlsx exam pattern).
# Derives marks_per_q (dict, MAX per type) and negative_marking (scalar, mode)
# from marking_scheme[] for backward compatibility with existing PARAMETER code.
# All values have safe defaults when exam_config.json is absent (legacy path).

def _read_exam_config_fields():
    """Read all new exam_config fields. Returns dict with safe defaults.
    Uses same glob pattern as _read_session_keyword for discovery."""
    import glob as _glob
    from collections import Counter as _Counter
    defaults = {
        'marking_scheme': [],
        'level': 'unknown',
        'medium': 'unknown',
        'question_types': ['MCQ'],
        'total_questions': None,
        'time_minutes': None,
    }
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        matches = sorted(_glob.glob(os.path.join(search_dir, '*exam_config.json')))
        for cfg_path in matches:
            try:
                with open(cfg_path, encoding='utf-8') as f:
                    cfg = json.load(f)
                return {
                    'marking_scheme':  cfg.get('marking_scheme', []),
                    'level':           cfg.get('level', 'unknown'),
                    'medium':          cfg.get('medium', 'unknown'),
                    'question_types':  cfg.get('question_types', ['MCQ']),
                    'total_questions': cfg.get('total_questions'),
                    'time_minutes':    cfg.get('time_minutes'),
                }
            except Exception:
                continue
    return defaults

def _derive_marks_per_q(marking_scheme):
    """Derive marks_per_q dict from marking_scheme[].
    Groups ranges by question_type, takes MAX correct_marks per type.
    Returns dict e.g. {'MCQ': 2} or {'MCQ': 2, 'MSQ': 2, 'NAT': 2}.
    Returns {'MCQ': 1} if marking_scheme is empty (legacy fallback)."""
    if not marking_scheme:
        return {'MCQ': 1}
    by_type = {}
    for ms in marking_scheme:
        qt = ms.get('question_type', 'MCQ')
        cm = ms.get('correct_marks', 1)
        by_type.setdefault(qt, []).append(cm)
    return {qt: max(marks_list) for qt, marks_list in by_type.items()}

def _derive_negative_marking(marking_scheme):
    """Derive scalar negative_marking from marking_scheme[].
    Returns the most common (mode) negative_marks value across all ranges.
    Returns 0 if marking_scheme is empty (legacy fallback)."""
    if not marking_scheme:
        return 0
    from collections import Counter as _Counter
    vals = [ms.get('negative_marks', 0) for ms in marking_scheme]
    return _Counter(vals).most_common(1)[0][0]

def _derive_negative_marking_by_type(marking_scheme):
    """Derive per-type negative_marking dict from marking_scheme[].
    For each question_type, takes MIN (most negative) across all ranges of that type.
    Returns dict e.g. {'MCQ': -0.5, 'MSQ': 0, 'NAT': 0}.
    Returns {} if marking_scheme is empty (legacy fallback)."""
    if not marking_scheme:
        return {}
    by_type = {}
    for ms in marking_scheme:
        qt = ms.get('question_type', 'MCQ')
        nm = ms.get('negative_marks', 0)
        by_type.setdefault(qt, []).append(nm)
    return {qt: min(neg_list) for qt, neg_list in by_type.items()}

# Read all fields at session start
_ecfg = _read_exam_config_fields()
marking_scheme = _ecfg['marking_scheme']
level          = _ecfg['level']
medium         = _ecfg['medium']

# Derive backward-compatible PARAMETER values from marking_scheme
# These feed into S1-3 parameter detection as PRIMARY values.
# Legacy AI detection from Exam Pattern doc / PYQ becomes VALIDATION ONLY.
if marking_scheme:
    # exam_config.json present with marking_scheme → authoritative
    _marks_from_config  = _derive_marks_per_q(marking_scheme)
    _neg_from_config    = _derive_negative_marking(marking_scheme)
    _negbt_from_config  = _derive_negative_marking_by_type(marking_scheme)
else:
    # exam_config absent or legacy → PARAMETER detection fills these later
    _marks_from_config  = None
    _neg_from_config    = None
    _negbt_from_config  = None
# ─────────────────────────────────────────────────────────────────────────────

def build_session_re(keyword):
    """Build dynamic regex for session/shift detection from the configurable keyword.
    Matches: <keyword><optional separator><digits>
    e.g. Shift-1, Slot_2, Phase 3, Session1, Paper-1"""
    return re.compile(re.escape(keyword) + r'[-_\s]?(\d+)', re.IGNORECASE)

SESSION_RE = build_session_re(session_keyword)
# ─────────────────────────────────────────────────────────────────────────────
# ── GOOGLE DRIVE MCP WRAPPER FUNCTIONS ───────────────────────────────────────
# These functions call the Google Drive MCP tools (already connected via settings).
# They are pseudocode wrappers — Claude calls the actual MCP tools at runtime.

def gdrive_search(query, page_size=100, page_token=None):
    """
    Call: Google Drive MCP 'search_files' tool with query string.
    Returns list of {id, title, mimeType} dicts.
    query format: "parentId = 'FOLDER_ID'"
    Claude calls this via the connected Google Drive MCP connector.
    """
    pass  # Claude calls Google Drive:search_files(query=query, pageSize=page_size, pageToken=page_token)

def gdrive_download_file(file_id, local_path):
    """
    Call: Google Drive MCP 'download_file_content' tool.
    Downloads file bytes to local_path for docx processing.
    Claude calls: Google Drive:download_file_content(fileId=file_id)
    Then writes binary content to local_path.
    """
    pass  # Claude calls Google Drive:download_file_content(fileId=file_id)

# ─────────────────────────────────────────────────────────────────────────────


# Parse ExamCode and PYQ link from trigger
# pyq_drive_folder_id = None  if no PYQ parameter given
# pyq_drive_folder_id = 'ID'  if PYQ: link given and parsed successfully
```

### S1-2 — File inventory

```python
pyq_doc_paths      = []   # list of {source, id, name} for Drive OR {source, path, name} local
exam_pattern_paths = []
analysis_doc_paths = []

# ── GOOGLE DRIVE PATH (when PYQ: link provided in trigger) ────────────────

def extract_folder_id(url):
    """Extract folder ID from any Google Drive folder URL."""
    m = re.search(r'drive\.google\.com/drive/folders/([A-Za-z0-9_-]+)', url)
    return m.group(1) if m else None

def collect_drive_docx_recursive(folder_id, all_files=None):
    """
    Recursively walk all subfolders under folder_id.
    Collects every .docx file regardless of nesting depth.

    ORDERING: year subfolders are sorted DESCENDING (2025 before 2024 before 2023 ...).
    Files within each year folder are collected as-is; final ordering is applied
    in run_batch_loop() by sort_papers_recency_first().

    Folder structure can be:
      flat       : all .docx directly in root folder
      year-based : root/2025/*.docx, root/2024/*.docx, ...
      any nesting: Claude walks the full tree
    Returns list of {source, id, name} dicts.
    """
    if all_files is None:
        all_files = []

    # Paginate through ALL items in folder (page_size=100, follow nextPageToken).
    # Without pagination, folders with >50 files would silently miss files.
    subfolders  = []
    page_token  = None

    while True:
        if page_token:
            results = gdrive_search(f"parentId = '{folder_id}'", page_size=100,
                                    page_token=page_token)
        else:
            results = gdrive_search(f"parentId = '{folder_id}'", page_size=100)

        items      = results if isinstance(results, list) else results.get('items', [])
        page_token = None if isinstance(results, list) else results.get('nextPageToken')

        for item in items:
            mime = item.get('mimeType', '')
            name = item.get('title', '')
            fid  = item.get('id', '')
            if mime == 'application/vnd.google-apps.folder':
                subfolders.append((name, fid))
            elif name.lower().endswith(('.docx', '.doc')):
                all_files.append({'source': 'gdrive', 'id': fid, 'name': name})

        if not page_token:
            break   # no more pages

    # Sort subfolders DESCENDING by name so year folders are visited 2025→2024→...
    # Works for numeric year names (2025, 2024, ...) and any other naming.
    subfolders.sort(key=lambda x: x[0], reverse=True)

    for subfolder_name, subfolder_id in subfolders:
        collect_drive_docx_recursive(subfolder_id, all_files)

    return all_files

_needs_pyq_corpus = not (mode == '--status' or (mode or '').startswith('--synthesise'))

if _needs_pyq_corpus:
    if not pyq_drive_folder_id:
        raise SystemExit(
            "HARD STOP: PYQExtract requires PYQ: <<Google Drive folder link>>. PYQ "
            "papers must be in Google Drive — the local project/uploads fallback for "
            "PYQ .docx corpus files was removed (v2.24.8) to standardize with Step 4 "
            "(PYQCount) and Step 2b (PYQScan). Exam pattern and Analysis documents may "
            "still be provided via project knowledge or chat upload (see below) — only "
            "the PYQ paper corpus itself now requires Drive.")

    try:
        pyq_doc_paths = collect_drive_docx_recursive(pyq_drive_folder_id)
        print(f"Google Drive: found {len(pyq_doc_paths)} PYQ .docx file(s)")
        print(f"  Folder ID: {pyq_drive_folder_id}")
    except Exception as e:
        raise SystemExit(
            f"HARD STOP: Google Drive error while listing the PYQ folder: {e}\n"
            f"Fix the Drive link/permissions and retry — there is no local fallback "
            f"for PYQ corpus files (v2.24.8, standardized with Step 4/Step 2b).")
elif pyq_drive_folder_id:
    # v2.24.8: --status / --synthesise don't strictly need the PYQ corpus, but if a
    # PYQ: link was given anyway, honor it — harmless, and useful for --status to
    # report accurate Drive counts. Non-fatal on error since these modes don't
    # depend on it.
    try:
        pyq_doc_paths = collect_drive_docx_recursive(pyq_drive_folder_id)
    except Exception as e:
        print(f"NOTE: Google Drive error while listing PYQ folder "
              f"(non-fatal for {mode!r}): {e}")

# ── Exam pattern + Analysis docs always from project/uploads ─────────────
# (these are small files — no Drive needed for them; unaffected by the v2.24.8
#  PYQ-corpus Drive-only standardization — only the raw PYQ .docx corpus was
#  tightened, not these small state/reference documents)

for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
    for f in glob.glob(os.path.join(search_dir, '*')):
        bn  = os.path.basename(f).lower()
        ext = os.path.splitext(bn)[1]
        if 'analysis' in bn or 'analyse' in bn:
            if ext in ('.docx', '.doc') and f not in [x.get('path') for x in analysis_doc_paths]:
                analysis_doc_paths.append({'source': 'local', 'path': f})
        elif any(kw in bn for kw in ('pattern', 'exam_pattern', 'notification')):
            if ext in ('.docx', '.doc', '.pdf', '.jpg', '.jpeg', '.png'):
                if f not in [x.get('path') for x in exam_pattern_paths]:
                    exam_pattern_paths.append({'source': 'local', 'path': f})
        elif ext in ('.jpg', '.jpeg', '.png', '.pdf') and not exam_pattern_paths:
            # v2.24.8: preserved from the old PYQ-corpus fallback loop — a loose
            # image/PDF with no pattern/notification keyword in its name is still
            # accepted as the Exam Pattern doc if nothing else has matched yet.
            # Unrelated to the PYQ-corpus Drive-only change; kept unchanged.
            if f not in [x.get('path') for x in exam_pattern_paths]:
                exam_pattern_paths.append({'source': 'local', 'path': f})

# ── Status print ──────────────────────────────────────────────────────────

analysis_docs_present = bool(analysis_doc_paths)
exam_pattern_present  = bool(exam_pattern_paths)
pyq_available         = bool(pyq_doc_paths)

print(f"Files found:")
print(f"  PYQ papers    : {len(pyq_doc_paths)}  (source: Google Drive)")
print(f"  Exam pattern  : {len(exam_pattern_paths)}")
print(f"  Analysis docs : {len(analysis_doc_paths)}")

# No-PYQ path: valid when Drive was correctly provided and searched, but this
# exam genuinely has zero PYQ papers available (a real PYQ-less exam, not a
# Drive-access problem — that case already HARD STOPPED above).
if not pyq_available and not (mode or '').startswith('--synthesise') and mode != '--status':
    print("INFO: No PYQ .docx files found in the Drive folder. "
          "Proceeding to --synthesise with absent entries.")
    mode = '--synthesise ALL'

# Load prior progress
progress = load_progress(exam_code)
n_done   = len(progress.get('_meta', {}).get('papers_processed', []))
if n_done:
    n_subs = len([k for k in progress if isinstance(k, tuple)])
    print(f"Resuming: {n_done} papers already processed. {n_subs} subtopics with data.")
```

**Key design decisions:**

- Folder structure is irrelevant — flat, year-subfolders, any nesting → all handled.
- Folder name is irrelevant — "Exam PYQ 2025", "My Papers", "PYQ Docs" → doesn't matter.
- Drive account is irrelevant — any shared folder link works as long as Claude has read access.
- ExamCode and Drive folder are decoupled — same ExamCode can point to different Drive folders
  across different runs (e.g., switching from your Drive to a colleague's Drive).
- Only .docx and .doc files are collected — other file types in the folder are ignored.

### S1-3 — Auto-detect all parameters from Exam Pattern + PYQ papers

No config file. All parameters are derived automatically.

**Sampling rule for PYQ-based detection:**
Where detection reads from PYQ papers, use a sample of one paper per year
from the most recent 3 available years (or all years if fewer than 3 exist).
This ensures detections reflect current exam style, not a single paper's quirks.

```python
# EXECUTION ORDER NOTE:
# All helper functions (sort_papers_recency_first from §8-S8-2,
# extract_year_from_filename from §3-S3-1) are defined in their respective sections.
# Claude loads and defines ALL functions from §2 through §8 before executing any
# session-start logic. This is a spec-reading convention: sections define functions,
# session execution happens after all definitions are loaded.
#
# all_sorted_papers built here using fully-loaded sort function:
all_sorted_papers = sort_papers_recency_first(pyq_doc_paths)  # sort once, use everywhere
```

```python
def get_detection_sample(all_sorted_papers):
    """
    Returns one paper per year from the most recent 3 years.
    all_sorted_papers: already sorted recency-first by sort_papers_recency_first().
    Picks the FIRST paper from each year (= most recent shift of that year).

    Examples:
      [N] papers across multiple years → picks most-recent-year session-1 per year (up to 3 years)
      8 papers from 2021 only     → picks 2021 session-1 (only 1 year available)
      Papers from 2024 and 2025   → picks both (2 years — use all available)
    """
    seen_years = {}
    for paper in all_sorted_papers:
        year = extract_year_from_filename(paper['name'])
        if year and year not in seen_years:
            seen_years[year] = paper
        if len(seen_years) == 3:
            break
    # Return in recency order (most recent year first)
    return [seen_years[y] for y in sorted(seen_years, reverse=True)]

# detection_sample: 1-3 papers, one per most recent year, used for P3/P5/P7/P8
detection_sample = get_detection_sample(all_sorted_papers)
detection_years  = [extract_year_from_filename(p['name']) for p in detection_sample]
print(f"Detection sample: {len(detection_sample)} paper(s) from years {detection_years}")
```

```
PARAMETER 1: time_per_question_sec
  Source: exam_config.json (primary — v2.18) or Exam Pattern document (legacy fallback).
  From exam_config: time_per_q_sec = time_minutes × 60 / total_questions.
  From Exam Pattern doc (legacy): same formula, AI-interpreted duration and Q count.
  Examples (values discovered at runtime from each exam's config):
    SSC CGL T1 (60 min / 100 Qs)     → 36 sec/Q
    GATE Biotech (180 min / 65 Qs)   → 166 sec/Q
    CSIR NET LS (180 min / 145 Qs)   → 74 sec/Q
    IIT JAM Chem (180 min / 60 Qs)   → 180 sec/Q
  If exam_config absent AND exam pattern not uploaded: default 60 sec/Q, document assumption.
  If pattern shows sectional time limits: use shortest section time/Qs
  (most constrained section sets the difficulty pace).

PARAMETER 2: negative_marking
  Source: exam_config.json marking_scheme[] (primary — v2.18) or Exam Pattern doc (legacy).
  From exam_config (v2.18): derive scalar and per-type from marking_scheme[]:
    scalar negative_marking = most common negative_marks across all ranges.
    negative_marking_by_type = for each question_type, take the MIN (most negative)
      value across all ranges of that type. Example:
        GATE marking_scheme: MCQ ranges have -0.33 and -0.66 → {'MCQ': -0.66}.
        MSQ ranges have 0.0 → {'MSQ': 0}. NAT ranges have 0.0 → {'NAT': 0}.
    If all ranges have the same negative_marks → scalar = that value.
    If mixed → scalar = most common value (mode); per-type dict captures full detail.
  From Exam Pattern doc (legacy fallback):
    Detection: scan for '-0.25', '-0.5', '-1', '1/3 mark', 'no negative', 'zero penalty'.
    '-1/4' / '-0.25' / '0.25 marks deducted'  → negative_marking = -0.25
    '-1/3' / '0.33 marks deducted'             → negative_marking = -0.33
    '-1/2' / '-0.5' / '0.5 marks deducted'    → negative_marking = -0.5
    '-1 mark' / 'full mark deducted'           → negative_marking = -1.0
    'no negative marking' / 'zero penalty'     → negative_marking = 0
    Not found in exam pattern                   → negative_marking = 0 (safe default)
  Use: stored in _meta and written to EXAM_STRUCTURE header in section_rules.md.
  NOT used in per-question difficulty scoring (extraction is marking-scheme agnostic).
  Step 7 reads it to know whether wrong answers reduce score (affects strategy).

  v2.5 PER-TYPE MARKING (MSQ contract; dormant until consumed by Step 9 (MockExplain)):
    negative_marking_by_type  dict  Source: Exam Pattern doc. Per question-type penalty,
      e.g. {'MCQ': -0.5, 'MSQ': 0}. MSQ commonly carries NO negative marking even when
      MCQ does. If the pattern gives only a single global value, replicate it for each
      q_type. If MSQ not present → omit the MSQ key. Default {} (fall back to the scalar
      negative_marking above).
    partial_credit  bool  Source: Exam Pattern doc. True if MSQ awards partial marks for a
      partially-correct set (e.g. "+1 per correct option, capped"); False = all-or-nothing.
      Default False. Captured now; consumed by Step 9 (MockExplain) scoring, not Step 5.
    These are detection-only at Step 5 and have NO effect when multi_select_allowed=false.

PARAMETER 3: language
  Source: exam_config.json medium field (primary — v2.18) + detection_sample (validation).
  v2.18 PRIORITY RULE: if exam_config.json contains a 'medium' field (e.g., "English"),
    use it as the authoritative language value:
      "English"    → language = 'english'
      "Hindi"      → language = 'hindi'
      "Bilingual"  → language = 'bilingual'
      other value  → language = medium.lower()
    PYQ auto-detection (below) then VALIDATES: if PYQ-detected language differs from
    the exam_config value, log a WARNING but keep the exam_config value. The exam_config
    xlsx is the authoritative source; PYQ detection catches edge cases.
    If exam_config absent or medium='unknown': fall through to PYQ detection as primary.
  PYQ detection method: for each sample paper, scan all paragraph text of first 30 questions.
          Count ASCII chars vs Indic-script Unicode chars across ALL scripts.
          Compute ratio across ALL sampled questions combined (not per paper).

  v2.16 RIGID-2: expanded from Devanagari-only to ALL major Indic scripts.
  INDIC_RANGES (Unicode block → script):
    U+0900–U+097F  Devanagari  (Hindi, Marathi, Sanskrit, Nepali)
    U+0980–U+09FF  Bengali     (Bengali, Assamese)
    U+0A00–U+0A7F  Gurmukhi    (Punjabi)
    U+0A80–U+0AFF  Gujarati
    U+0B00–U+0B7F  Odia
    U+0B80–U+0BFF  Tamil
    U+0C00–U+0C7F  Telugu
    U+0C80–U+0CFF  Kannada
    U+0D00–U+0D7F  Malayalam

  Detection (exam-agnostic — works for 100+ exams across all Indian languages):
    1. Count: ascii_count, devanagari_count, other_indic_count (all non-Devanagari
       Indic scripts combined), total_alpha.
    2. Compute ratios: ascii_pct, devanagari_pct, other_indic_pct.
    3. Decision:
       If >90% ASCII                           → language = 'english'
       If devanagari_pct > 20% AND other_indic_pct < 5%  → language = 'hindi'
       If other_indic_pct > 20%                → language = 'regional'
         (the specific script is stored in _meta['detected_script'] for downstream use)
       If 10-90% ASCII with any Indic > 10%    → language = 'bilingual'
       Otherwise                               → language = 'english' (safe default)

  The 'regional' value is new in v2.16. Step 7 treats 'regional' the same as
  'hindi' for generation purposes (use training knowledge for the script).
  Rationale: a single paper could be atypical; sampling 3 years gives a
  stable detection even if one year's paper had unusual formatting.

PARAMETER 4: no-PYQ behaviour (mode decision, not a tunable parameter)
  If no PYQ .docx files found → auto-redirect to --synthesise ALL.
  All subtopics written as confidence='absent'. Step 7 uses training knowledge.
  Valid and expected state — not an error.
  If PYQ files present → always presorted; extract_presorted() is sole path.

PARAMETER 5: question_types
  Source: exam_config.json question_types[] (primary — v2.18) + detection_sample (validation).
  From exam_config (v2.18): read question_types list directly. Already validated at
    Step 2a (V8 ensures Overview types match Range tab types). Maps to q_types:
      "MCQ" → 'MCQ'.  "MSQ" → 'MSQ'.  "NAT" → 'integer'.
    multi_select_allowed = ('MSQ' in question_types).
    nat_allowed = ('NAT' in question_types).
  From Exam Pattern doc (legacy fallback):
    MCQ     : default unless pattern says otherwise.
    MSQ     : "Multiple Select" / "select all that apply" / "MSQ" /
              "one or more options may be correct" → add 'MSQ'.
    Integer : "Numerical Answer Type" / "NAT" / "integer type" /
              "enter the answer" → add 'integer'.
  Validation from detection_sample (BOTH paths):
    Scan first 50 questions across ALL sample papers combined.
    If any question has no option labels (stem only, no 1/2/3/4 or A/B/C/D)
    → integer type confirmed (even if not in exam_config/pattern).
    If exam_config AND exam pattern both absent: use PYQ-observed types only. Default ['MCQ'].

PARAMETER 6: marks_per_question
  Source: exam_config.json marking_scheme[] (primary — v2.18) or Exam Pattern doc (legacy).
  From exam_config (v2.18): derive marks_per_q dict from marking_scheme[]:
    Group ranges by question_type. For each type, take MAX correct_marks across ranges.
    Examples:
      SSC CGL T1: 1 range, all MCQ 2m      → {'MCQ': 2}
      CSIR NET LS: 3 ranges, MCQ at 2m/4m  → {'MCQ': 4}   (max)
      GATE BT: MCQ 1m/2m, MSQ 1m/2m, NAT 1m/2m → {'MCQ': 2, 'MSQ': 2, 'NAT': 2}
      CSIR NET Math: MCQ 2m/3m, MSQ 4.75m  → {'MCQ': 3, 'MSQ': 4.75}
    WHY MAX: In sorted PYQ files, original Q-number positions are lost (PYQSort
    renumbers). We cannot look up which marking_scheme range a PYQ question came
    from. Using MAX per type is conservative — it shifts difficulty thresholds up,
    preventing under-classification of high-mark questions as "Simple".
    Step 7 (which generates new questions at known Q positions) uses the full
    marking_scheme[] for exact per-range marks lookup.
  From Exam Pattern doc (legacy fallback):
    "All questions carry 1 mark" / "1 mark each"                → {'MCQ': 1}
    "1 mark for 1-mark / 2 marks for 2-mark questions"          → {'1-mark':1,'2-mark':2}
    "Each correct answer: 2 marks"                              → {'MCQ': 2}
    No marking scheme found → default {'MCQ': 1}, document assumption.
  Affects difficulty threshold scaling in E-9 (higher-mark Qs get higher thresholds).

PARAMETER 7: options_count + option_label_format
  Source: detection_sample (1-3 papers, one per most recent year).
  Method: collect first 30 questions from EACH sample paper. For each question,
          count how many option labels (1./2./3./4. or A./B./C./D.) were found.
          This is a raw count of observed labels — NOT filtered by options_count
          (which is unknown at this stage — we are computing it here).
  Decision (majority vote across all questions combined, ~90 questions):
    If ≥90% of questions have exactly 4 option labels → options_count = 4
    If ≥90% of questions have exactly 3 option labels → options_count = 3
    If mixed or ambiguous                             → options_count = 4 (safe default)
    Note: questions with 0 option labels are skipped (image-only options or NAT).
  Rationale: sampling 3 years catches any format change mid-series.

  option_label_format (v2.15 BUG-D07 — was documented but never implemented):
    ALSO detect the LABEL STYLE from the same sample questions:
      If majority of option lines start with "1." / "2." / "3." / "4."   → '1/2/3/4'
      If majority start with "(1)" / "(2)" / "(3)" / "(4)"              → '(1)/(2)/(3)/(4)'
      If majority start with "A." / "B." / "C." / "D."                  → 'A/B/C/D'
      If majority start with "(A)" / "(B)" / "(C)" / "(D)"              → '(A)/(B)/(C)/(D)'
      If majority start with "(a)" / "(b)" / "(c)" / "(d)"              → '(a)/(b)/(c)/(d)'
      If majority start with "A)" / "B)" / "C)" / "D)"                  → 'A)/B)/C)/D)'
    Default: '1/2/3/4'.
    This is the option LABEL style (how labels are printed), NOT option FORMAT type
    (single_value/sentence_label etc. which describes content shape).
    Stored in _meta and written to EXAM_STRUCTURE. Per-section override derived
    from per-question option_label stored during extraction.

PARAMETER 8: multi_select_allowed
  Source: Exam Pattern document (primary) + detection_sample (confirmation).
  From exam pattern: "Multiple Correct Answers" / "MSQ" / "Select all" → True.
  From detection_sample:
    Scan ALL questions across ALL sample papers (not just first 20).
    If any stem contains "select ALL correct" / "one or more correct"
    / "which of the following are correct" → True.
  Default: False. Only True for exams explicitly supporting MSQ (e.g. GATE).
  Rationale: MSQ questions are rare but consequential — scanning 3 years of
  papers gives much higher confidence than scanning a single paper.

PARAMETER 9: msq_k_mode / msq_k  [v2.5 MSQ contract; only when multi_select_allowed=True]
  Source: Exam Pattern document ONLY.
  WHY NOT FROM PYQ: extraction is answer-key agnostic and PYQ papers carry no key,
  so the NUMBER of correct options (k) is unextractable from PYQ. It must come from
  the exam pattern. Step 5 can detect THAT a question is MSQ (from option shape +
  stem), but not k. This is a documented, intentional limitation.
  Detection from exam pattern:
    "select TWO" / "exactly two correct" / "choose 2"   → msq_k_mode='fixed', msq_k=2
    "select THREE" / "exactly three correct"            → msq_k_mode='fixed', msq_k=3
    "one or more correct" / "select all that apply"     → msq_k_mode='variable', msq_k=None
    Not specified but multi_select_allowed=True          → msq_k_mode='variable' (default)
  Constraint passed to Step 7: correct set S ⊆ {1..options_count} with
    1 ≤ |S| ≤ options_count−1 (variable), or |S| = msq_k (fixed). k=0 and k=n forbidden.
  Default when multi_select_allowed=False: msq_k_mode='n/a' (path inert).

PARAMETER 10: msq_allow_aota  [v2.5 MSQ contract, D5; only meaningful when multi_select_allowed=True]
  Source: Exam Pattern document; default False.
  Policy flag controlling whether an "All of the above" option is permitted under
  multi-select. Under MSQ, AOTA is self-contradictory (it cannot coexist with
  individually selectable correct options), so it is REJECTED by default. An exam whose
  pattern explicitly sanctions AOTA-style options in multi-select sets this True.
  Detection from exam pattern:
    explicit "All of the above permitted / allowed in multi-select" → msq_allow_aota=True
    anything else (incl. silent)                                    → msq_allow_aota=False
  Written into EXAM_STRUCTURE so Step 7 (R-MSQ-ESCAPE / G-MSQ-SET) and Step 3
  (A-MSQ-KEY) read it directly from section_rules. "None of these" is unaffected — it
  stays an ordinary selectable option in either case. Default when
  multi_select_allowed=False: False (path inert).
  msq_instruction / msq_instruction_hi  [v2.9 — parametric, localised; D8]:
    The candidate-facing select-instruction Step 7 places inside the Q.N stem line (R14)
    for a multi-select question, e.g. "(One or more options may be correct)" / "(Select
    TWO)", and Step 8 (A-MSQ-INSTR) verifies. The EXACT MSQ analogue of nat_instruction
    (PARAMETER 11) — referenced there as the model. Parenthesised so it reads as an in-stem
    instruction. Default text supplied below; an exam may override from its pattern, and the
    _hi variant carries the Hindi/bilingual phrasing (per PARAMETER 3). Before v2.9 no
    producer emitted this and Step 7/8 silently used a hardcoded fallback (a contract-sync
    gap closed here); now authoritative + overridable, symmetric with NAT.
      Default: msq_instruction    = '(One or more options may be correct)'
               msq_instruction_hi = '(एक या अधिक विकल्प सही हो सकते हैं)'
      If msq_k_mode=='fixed' with msq_k=K, an exam may instead phrase it "(Select K)" /
      localized. Default when multi_select_allowed=False: defaults still written but inert.

PARAMETER 11: nat_allowed + NAT config  [v2.8 NAT contract; only when nat_allowed=True]
  Source: Exam Pattern document (primary) + detection_sample (confirmation).
  nat_allowed (the capability gate — analogous to multi_select_allowed for MSQ):
    Derived primarily from PARAMETER 5 q_types: nat_allowed = ('integer' in q_types).
    Reinforced from exam pattern: "Numerical Answer Type" / "NAT" / "fill in the value"
    / "enter the answer" present → True. From detection_sample: any question with ZERO
    selectable options (no text option labels AND no option-images — image_role is none or
    stem_only, never options_only/stem_and_options) confirms NAT.
    Default: False. Only True for exams that explicitly use numerical-entry questions
    (e.g. GATE, JEE). When False, the entire NAT path is inert (answer_type is always
    'option', so non-NAT exams are behaviourally identical to v2.7).
  WHY NOT k-style PYQ extraction: as with msq_k, the ACCEPTED VALUE and its TOLERANCE are
    answer-key information; PYQ papers carry no key, so a NAT question's value/tolerance are
    unextractable from PYQ. Step 5 detects THAT a subtopic is numerical (0-option shape),
    but the answer model below must come from the exam pattern. Documented limitation.
  nat_answer_type ∈ {integer, real}  [only when nat_allowed=True]:
    From exam pattern:
      "answer is an integer" / "integer type" / "no decimals"        → 'integer'
      "up to N decimal places" / "rounded to" / "real value" / "±"   → 'real'
      nat_allowed but unspecified                                    → 'real' (default;
        GATE-style NAT commonly permits a decimal value with a tolerance band)
    integer ⇒ exact match (no tolerance band); real ⇒ value within nat_tolerance.
  nat_tolerance  [only when nat_answer_type=='real']:
    From exam pattern ONLY (e.g. "± 0.01", "accept 46.5 to 47.5", "2 decimal places").
    Encoded as an absolute delta (float) or a percentage string ("1%"). Becomes Step 9's
    ca_range=(value−tol, value+tol). Default when unspecified: '0' (treat as exact to the
    displayed precision — never invent a tolerance). integer ⇒ always '0'.
  nat_instruction  [parametric, localised]:
    The candidate-facing instruction Step 7 places inside the Q.N stem line (R14), e.g.
    "Enter your answer as a numerical value." (Hindi/bilingual per PARAMETER 3). Default
    text supplied; an exam may override from its pattern. Mirrors the MSQ instruction.
  NAT marking: per-type penalty lives in negative_marking_by_type (PARAMETER 2) under the
    'NAT' key (NAT is usually 0 negative marking). Additive — no new field. Default absent
    ⇒ falls back to the generic negative_marking.
```

Auto-detection confirmation printed before processing:

```
"=== Auto-detected parameters ===
 Session keyword  : [session_keyword] (from: exam_config.json | default 'Shift')
 Detection sample : [year1] [session_keyword]-[N], [year2] [session_keyword]-[N], ...
                    ([N] paper(s) sampled from [N] most recent year(s))
 Time/Q           : [N] sec  (from: [exam pattern | default 60])
 Language         : [english | hindi | regional | bilingual]  (from: 3-year PYQ sample)
 Q-types          : [MCQ | MCQ+MSQ | MCQ+integer]  (from: [exam pattern | PYQ | default])
 Marks/Q          : [dict]  (from: [exam pattern | default {'MCQ':1}])
 Options/Q        : [N]  (observed from: [N] papers across [N] years)
 Multi-select     : [yes | no]  (from: [exam pattern | PYQ sample | default no])
 MSQ k-mode       : [fixed k=N | variable | n/a]  (printed only when multi-select=yes)
 MSQ AOTA         : [allowed | rejected (default)]  (printed only when multi-select=yes)
 MSQ marking      : [neg-by-type | partial=yes/no]  (printed only when multi-select=yes)
 NAT type         : [integer | real (default) | n/a]  (printed only when nat-allowed=yes)
 NAT tolerance    : [± value | exact]  (printed only when nat-allowed=yes)
 Note: presorted = always true (all PYQ files pre-sorted by subtopic heading)
================================="
```

If any detection is ambiguous across sampled papers (e.g., options_count=4 in 2025
but options_count=3 in 2023), Claude reports the conflict explicitly:
  "options_count conflict across years: 2025=4, 2023=3 → using 4 (most recent year wins)"
Most-recent-year always wins for conflicting detections.
Claude does NOT ask the user to resolve conflicts — it decides and proceeds.

### S1-3a — Config-derived parameter overrides (NEW v2.18)

When exam_config.json is present with marking_scheme[] (Step 2a v2.5+), the
config-derived values OVERRIDE AI-detected values for PARAMETERs 1, 2, 3, 5, 6.
AI detection from PYQ becomes validation only (warn on conflict, config wins).

```python
# v2.18: Override AI-detected parameters with exam_config values when available.
# _ecfg, marking_scheme, level, medium, _marks_from_config, _neg_from_config,
# _negbt_from_config are all set at session start (above _read_exam_config_fields).
# Gate: marking_scheme non-empty means exam_config v2.5 is present → authoritative.
# When marking_scheme is empty, exam_config is absent or legacy → no override.

# PARAMETER 1: time_per_q_sec — prefer exam_config.time_minutes / total_questions
if _ecfg.get('time_minutes') and _ecfg.get('total_questions'):
    config_time_per_q = round(_ecfg['time_minutes'] * 60 / _ecfg['total_questions'])
    if time_per_q != config_time_per_q:
        print(f"NOTE: time_per_q overridden by exam_config: {time_per_q} → {config_time_per_q}")
    time_per_q = config_time_per_q

# PARAMETER 2: negative_marking — prefer marking_scheme-derived value
if _neg_from_config is not None:
    if negative_marking != _neg_from_config:
        print(f"NOTE: negative_marking overridden by exam_config: {negative_marking} → {_neg_from_config}")
    negative_marking = _neg_from_config
if _negbt_from_config is not None:
    negative_marking_by_type = _negbt_from_config

# PARAMETER 3: language — prefer medium from exam_config
if medium and medium.lower() != 'unknown':
    config_lang = medium.lower()
    if config_lang in ('english', 'hindi', 'bilingual'):
        if language != config_lang:
            print(f"NOTE: language overridden by exam_config medium: {language} → {config_lang}")
        language = config_lang

# PARAMETER 5: question_types — prefer exam_config.question_types
# Gate on marking_scheme to distinguish v2.5 exam_config (authoritative) from
# legacy/absent exam_config (default ['MCQ'] — should NOT suppress PYQ detection).
# When exam_config v2.5 says ['MCQ'] only, it is AUTHORITATIVE — PYQ-detected NAT/MSQ
# must be ignored (the exam genuinely has only MCQ). A warning is logged so the user
# can correct the exam_config xlsx if the PYQ detection was correct.
if marking_scheme and _ecfg.get('question_types'):
    config_q_types = set()
    for qt in _ecfg['question_types']:
        if qt == 'NAT':
            config_q_types.add('integer')
        else:
            config_q_types.add(qt)
    if set(q_types) != config_q_types:
        print(f"WARN: q_types overridden by exam_config: PYQ detected {q_types}, "
              f"exam_config says {sorted(config_q_types)}. If PYQ detection was correct, "
              f"update the exam pattern xlsx Question Type field.")
    q_types = sorted(config_q_types)
    multi_select = 'MSQ' in _ecfg['question_types']
    # nat_allowed must also be updated (consumed by S1-3b and downstream)
    nat_allowed_override = 'NAT' in _ecfg['question_types']

# PARAMETER 6: marks_per_q — prefer marking_scheme-derived MAX per type
if _marks_from_config is not None:
    if marks_per_q != _marks_from_config:
        print(f"NOTE: marks_per_q overridden by exam_config: {marks_per_q} → {_marks_from_config}")
    marks_per_q = _marks_from_config
```

### S1-3b — Store auto-detected params in _meta (NEW v2.3)

After S1-3 completes detection, store all detected params in `progress['_meta']`.
These are later retrieved by `run_synthesise` and passed to `write_section_rules`
as `exam_meta` so the EXAM_STRUCTURE header block can be written to section_rules.md.

```python
# Store auto-detected exam parameters in progress _meta immediately after S1-3.
# Keys must match what write_section_rules() expects in exam_meta dict.
progress.setdefault('_meta', {}).update({
    'time_per_q_sec'       : time_per_q,          # int (seconds)
    'language'             : language,             # 'english'|'hindi'|'regional'|'bilingual'
    'session_keyword'      : session_keyword,      # v2.16 RIGID-1: 'Shift'|'Slot'|'Phase'|etc.
    'q_types'              : list(q_types),        # e.g. ['MCQ'] or ['MCQ','MSQ']
    'marks_per_q'          : marks_per_q,          # dict e.g. {'MCQ':1} (derived from marking_scheme)
    'negative_marking'     : negative_marking,     # float e.g. -0.5 or 0 (summary scalar)
    'options_count'        : options_count,        # int e.g. 4
    'multi_select_allowed' : multi_select,         # bool
    # v2.18: new fields from exam_config.json (Step 2a v2.5 contract).
    # marking_scheme is the per-range source of truth; marks_per_q and negative_marking
    # above are derived summaries for backward compatibility.
    'marking_scheme'       : marking_scheme,       # list of {q_range, question_type, correct_marks, negative_marks}
    'level'                : level,                # 'Graduation'|'Post Graduation'|etc.
    'medium'               : medium,               # 'English'|'Hindi'|'Bilingual'|etc.
    # v2.5 MSQ contract (dormant unless multi_select_allowed). PARAMETER 9 + per-type marking.
    'msq_k_mode'              : msq_k_mode,         # 'fixed'|'variable'|'n/a'
    'msq_k'                   : msq_k,              # int|None
    'msq_allow_aota'          : msq_allow_aota,     # v2.5 D5: bool (default False) — permit
                                                   #   "All of the above" under MSQ
    # v2.9 (contract-sync fix): localized MSQ select-instruction, the MSQ analogue of
    # nat_instruction. Parametric, localised; default supplied, an exam may override from
    # its pattern. Consumed by Step 7/8 from section_rules. _hi = Hindi/bilingual variant.
    'msq_instruction'         : msq_instruction,    # localised; default '(One or more options may be correct)'
    'msq_instruction_hi'      : msq_instruction_hi, # Hindi/bilingual variant
    'negative_marking_by_type': negative_marking_by_type,  # dict e.g. {'MCQ':-0.5,'MSQ':0}
    'partial_credit'          : partial_credit,    # bool
    # v2.8 NAT contract (dormant unless nat_allowed). PARAMETER 11. nat_allowed gates the
    # per-subtopic answer_type detection; the answer model comes from the exam pattern.
    'nat_allowed'             : ('integer' in q_types),   # bool — capability gate
    'nat_answer_type'         : nat_answer_type,   # 'integer'|'real' (default 'real')
    'nat_tolerance'           : nat_tolerance,     # abs float or '%' string; '0' = exact
    'nat_instruction'         : nat_instruction,   # parametric, localised (PARAMETER 3)
    # v2.15 BUG-D07: option_label_format now auto-detected from PYQ option lines
    # during PARAMETER 7 detection. The label style ('1/2/3/4' vs 'A/B/C/D') is
    # distinct from option FORMAT type ('single_value'). Stored here; written to
    # EXAM_STRUCTURE. Per-section override derived during synthesis from per-question
    # option_label fields stored during extraction.
    'option_label_format'     : option_label_format,  # '1/2/3/4' | 'A/B/C/D' | etc.
})
# Note: papers_analysed, questions_analysed, years_covered are updated
# incrementally in _meta['papers_processed'] and _meta['total_questions']
# and _meta['years_processed'] during each paper processing call.
```

### S1-3c — §1-6 Minimum year coverage check (runs at session start)

```python
# Run immediately after file inventory (S1-2) — before any paper processing.
# Determines coverage_mode, recent_5_years, available_years for this session.
# These three variables are passed to run_batch_loop() and run_synthesise().
#
# ★ CRITICAL: 5-year minimum is MANDATORY when PYQ papers are available.
# ★ This check cannot be bypassed by any user instruction or argument.

def compute_coverage_mode(pyq_doc_paths):
    """
    §1-6 check: compute minimum year coverage requirements for this exam.
    Returns: (coverage_mode, recent_5_years, available_years)
    MANDATORY: cover as many recent years as available, with a minimum of
min_pyq_years (default: 5, read from project configuration or trigger parameter).
If fewer years are available (new exam, limited PYQ history): process ALL available years.
The 5-year default is a quality floor — not a rigid rule that blocks generation when fewer exist.
    """
    # Extract years from all available paper filenames, filter out None
    all_years_raw  = [extract_year_from_filename(p['name']) for p in pyq_doc_paths]
    all_years_clean = sorted(set(y for y in all_years_raw if y is not None), reverse=True)

    if not all_years_clean:
        # No year detectable from filenames (e.g. "GATE_Paper_Set1.docx")
        # Cannot enforce year-based coverage. Use a passthrough mode.
        print("WARN: No years detectable from PYQ filenames. Year coverage check disabled.")
        return 'no_year_info', [], []

    available_years  = all_years_clean                    # descending: [2025, 2024, 2023, ...]
    n_required_years = min(5, len(available_years))      # cap at actual number of years available
    recent_5_years   = available_years[:n_required_years] # most recent N years (up to 5)
    coverage_mode    = 'mandatory_5yr'                    # single mode — always 5 years

    print(f"★ MANDATORY 5-YEAR COVERAGE RULE ACTIVE ★")
    print(f"Coverage mode  : {coverage_mode}")
    print(f"Available years: {available_years}")
    print(f"Required years : {recent_5_years} ({n_required_years} year(s) must be processed)")
    return coverage_mode, recent_5_years, available_years

# Scenario B (no PYQ): skip coverage check entirely
if pyq_available:
    coverage_mode, recent_5_years, available_years = compute_coverage_mode(pyq_doc_paths)
else:
    # Scenario B — no PYQ files. §1-6 does not apply (see §1-6 note).
    coverage_mode, recent_5_years, available_years = 'no_pyq', [], []
```

### S1-4 — Load subtopic taxonomy

```
CROSS-STEP SUBTOPIC NAME RULE (applies to Step 5 and Step 6 both):
  Step 5 (PYQExtract) and Step 6 (MockBlueprint) both read subtopic
  names from the SAME Analysis Word docs. Both steps MUST use the EXACT names
  as written in the Analysis doc.
  Step 7 (MockCreate) matches subtopics by EXACT name between section_rules.md
  (from Step 5) and blueprint.json (from Step 6). A name mismatch = subtopic
  unrecognised by Step 7 → that subtopic gets no allocation or pattern guidance.
  If a name correction is needed: apply the SAME correction in the Analysis doc
  and re-run BOTH Step 5 AND Step 6 before starting Step 7.
```

```python
def extract_taxonomy_from_analysis_doc(doc_path, taxonomy):
    """
    Read Analysis Word doc and populate taxonomy dict.
    taxonomy: {section_name: [{'topic': str, 'subtopic': str}]}
    Same 3-level hierarchy (Section > Topic > Subtopic) as Step 6.
    doc_path: either a string path OR a dict {'source','path'} — both handled.
    """
    from docx import Document as WDoc
    # Handle both string path and dict {source, path} from analysis_doc_paths
    actual_path = doc_path['path'] if isinstance(doc_path, dict) else doc_path
    doc     = WDoc(actual_path)
    cur_sec = cur_top = ''

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text: continue
        has_bold = any(r.bold for r in para.runs if r.text.strip())
        if not has_bold: continue

        style_name = para.style.name if para.style else ''
        indent     = para.paragraph_format.left_indent or 0

        if 'Heading 1' in style_name or (indent == 0 and not cur_sec):
            cur_sec = text; cur_top = ''
            taxonomy.setdefault(cur_sec, [])
        elif 'Heading 2' in style_name or (indent == 0 and cur_sec):
            cur_top = text
        elif 'Heading 3' in style_name or (has_bold and cur_sec):
            taxonomy[cur_sec].append({'topic': cur_top, 'subtopic': text})

taxonomy = {}
if analysis_docs_present:
    for doc_path in analysis_doc_paths:
        extract_taxonomy_from_analysis_doc(doc_path, taxonomy)
    total = sum(len(v) for v in taxonomy.values())
    print(f"Taxonomy: {total} subtopics, {len(taxonomy)} sections")
elif pyq_available:
    # Presorted PYQ papers carry their own taxonomy headings.
    # Taxonomy will be built incrementally from docx headings during E-1.
    print("Taxonomy built from PYQ docx headings during extraction")
else:
    # No PYQ and no Analysis docs: cannot build taxonomy.
    # Synthesis will produce empty section_rules.md — warn user.
    print("WARN: No Analysis docs and no PYQ files found.\n"
          "section_rules.md will be empty. Upload Analysis docs to get absent entries.")
```

### S1-5 — Verification summary

```
"=== PYQExtract: [ExamCode] ===
 Mode            : [auto|synthesise|status]
 PYQ source      : [Google Drive (folder: [ID]) | project/uploads]
 PYQ files       : [N] total  ([N] done, [N] pending)
 Session keyword : [session_keyword] (from: exam_config.json | default 'Shift')
 Detection sample: [year1] [session_keyword]-[N], [year2] [session_keyword]-[N], ...
 Exam pattern    : [found | not found — time/Q defaulted to 60 sec]
 Analysis docs   : [N] docx
 ── Auto-detected ──────────────────────────────────────
 Time/Q          : [N] sec  (from: [exam pattern | default 60])
 Language        : [english|hindi|regional|bilingual]  (from: [N]-year sample)
 Q-types         : [list]   (from: [exam pattern | PYQ sample | default MCQ])
 Marks/Q         : [dict]   (from: [exam pattern | default {'MCQ':1}])
 Options/Q       : [N]      (observed across [N] papers, [N] years)
 Multi-select    : [yes|no] (from: [exam pattern | PYQ sample | default no])
 ───────────────────────────────────────────────────────
 Taxonomy        : [N] subtopics across [M] sections
 Progress        : [fresh start | resuming — [N] papers done, [K] Qs]
 Minimum coverage: [mandatory_5yr — 5 years required (NON-NEGOTIABLE) | no_pyq | no_year_info]
 Available years : [list of all years found in Drive/uploads]
 Conflicts       : [None | e.g. options_count: 2025=4, 2023=3 → using 4]
 Status          : [Ready | HALTED — reason]
 =================================="
```

---

## §1-6 — MINIMUM YEAR COVERAGE RULE (NON-NEGOTIABLE — CRITICAL)

```
★★★ CRITICAL RULE — ZERO EXCEPTIONS WHEN PYQ PAPERS ARE AVAILABLE ★★★

This rule is enforced BEFORE any processing begins AND rechecked at synthesis.
It cannot be waived, overridden by the user, or bypassed for any reason whatsoever.
No instruction, no user request, no edge-case argument can override this rule.
If in doubt: HALT and ask user to provide more PYQ papers. Never proceed with less.

RULE:
  Analysis SHOULD cover the most recent min_pyq_years (default 5) years of PYQ papers.
If fewer years of PYQ exist for this exam: process ALL available years (no minimum enforced).
QUALITY TARGET: more years = better patterns. The 5-year default is a guideline, not a blocker.
  If fewer than 5 years of papers exist for the exam, ALL available years must be processed.
  (e.g., exam started in 2023 → process 2023+2024+2025 = all 3 available years.)
  NO EXCEPTION to this rule when PYQ papers are available — see only valid exceptions below.

  VALID EXCEPTION 1 — NO PYQ (Scenario B):
    If no PYQ .docx files exist for this exam AT ALL (Scenario B), this rule does NOT apply.
    Synthesis proceeds immediately, writing all-absent entries from the taxonomy.
    THIS IS THE ONLY EXCEPTION WHEN PYQ PAPERS ARE UNAVAILABLE.

  VALID EXCEPTION 2 — NO YEAR IN FILENAMES (coverage_mode = 'no_year_info'):
    If year cannot be detected from any PYQ filename (no '20XX' pattern),
    year-based coverage tracking is disabled and the rule is not enforced.
    Claude must WARN the user and proceed without blocking synthesis.

  INVALID EXCEPTIONS (these do NOT excuse the 5-year rule):
    ✗ "We already have a section_rules.md from before" — INVALID. Must re-run with 5 years.
    ✗ "Processing all papers takes too long" — INVALID. Use continue across sessions.
    ✗ "The last 2 years are enough" — INVALID. 5 years is mandatory.
    ✗ "User said to proceed with fewer years" — INVALID. Rule overrides user instruction.
    ✗ "Papers from older years are less relevant" — INVALID. 5 years minimum, always.

CHECKING LOGIC (implemented in S1-3c compute_coverage_mode()):
  At session start (after S1-2 file inventory), for Scenario A (PYQ available):
    Extract years from all PYQ filenames using extract_year_from_filename().
    Filter out None (files without detectable year).
    available_years  = sorted unique years, descending: [2025, 2024, 2023, 2022, 2021, ...]
    n_required       = min(5, len(available_years))   # cap: can't require >what exists
    recent_5_years   = available_years[:n_required]   # most recent N years (up to 5)
    coverage_mode    = 'mandatory_5yr'                # single mode — always 5 years

  Displayed in S1-5 verification summary.

ENFORCEMENT AT SYNTHESIS (implemented in run_synthesise()):
  processed_years = set of years in progress['_meta']['years_processed']
  n_required      = min(5, len(available_years))

  if coverage_mode == 'mandatory_5yr':
    missing = [y for y in recent_5_years if y not in processed_years]
    if len(processed_years) < n_required or missing:
      → HALT — SYNTHESIS BLOCKED (see run_synthesise enforcement code in S8-4)

  if coverage_mode in ('no_pyq', 'no_year_info') → proceed without check.

  HALT means: do not write section_rules.md. Print the block message below.
  Do NOT silently proceed with insufficient data.
  Do NOT ask user if they want to proceed anyway — this is non-negotiable.

BLOCK MESSAGE (printed when halted):
  "★ SYNTHESIS BLOCKED: 5-YEAR COVERAGE RULE NOT MET ★
   Required : {n_required} most recent year(s): {recent_5_years[:n_required]}
   Processed: {processed_years}
   Missing  : {sorted(missing, reverse=True)}
   ACTION   : Process papers from the missing year(s) before synthesising.
              This rule cannot be waived. No exception applies here."
```

---

## §2 — UNIVERSAL EXTRACTION ENGINE: E-1 THROUGH E-11

These 11 rules apply identically to every exam.
Operations are universal. Outputs differ because PYQ content differs.

### E-1 — Hierarchy reading

PYQ papers are always presorted — bold taxonomy headings organize every
question into Subject → Topic → Subtopic before it appears.
There is no Mode B. If PYQ is not available for an exam, no .docx files
are uploaded and Step 5 skips extraction entirely, writing absent entries
from the taxonomy during --synthesise (see S1-2 no-PYQ path).

```
Helpers:

  def is_shift_tag(text):
      # Matches date-format shift tags like [09-Sep-2024 Shift 1] or [5-Jan-2024 Shift 1]
      # v2.16 SYNC: \d{1,2} (not \d{2}) to match single-digit days — aligned with PYQAnalyse.
      return bool(re.match(r'\[\d{1,2}-', text))

  def parse_shift(text):
      # v2.16 RIGID-1: uses SESSION_RE (built from exam_config.json session_keyword)
      # instead of hardcoded 'Shift'. Works for Shift/Slot/Phase/Paper/Session.
      m = SESSION_RE.search(text)
      return f'S{m.group(1)}' if m else 'S1'

  # parse_taxonomy_level() defined in S3-2.
  # detect_question_start() defined in E-2.

Algorithm (pseudocode — full implementation in S3-2 extract_presorted()):
  current_path  = []    # [section, topic, subtopic]
  current_shift = 'S1'
  for paragraph in doc.paragraphs:
      text = paragraph.text.strip()
      if not text: continue
      if is_taxonomy_heading(paragraph):
          level, content = parse_taxonomy_level(text)
          current_path = current_path[:level-1] + [content]
      elif is_shift_tag(text):
          current_shift = parse_shift(text)
      else:
          q_num = detect_question_start(text)
          if q_num is not None:
              tag_question(q_num, current_path, current_shift)

  is_taxonomy_heading() and parse_taxonomy_level() are defined in S3-2.
```

### E-2 — Question detection

```python
Q_PATTERNS = [
    r'^Q\.\s*(\d+)\s+',           # Q.1  Q.25  Q. 1  (optional space after dot)
    r'^Q(\d+)\.\s+',               # Q1.  Q25.
    r'^Question\s+(\d+)\s*[:.]',   # Question 1:
    r'^(\d+)\.\s+(?!\d)',           # 1.   25.   (negative lookahead: not 1.5)
    r'^\((\d+)\)\s+',              # (1)  (25)
]

def detect_question_start(text):
    for pat in Q_PATTERNS:
        m = re.match(pat, text.strip())
        if m: return int(m.group(1))
    return None
```

### E-3 — Option detection

```python
OPT_PATTERNS = [
    r'^([1-5])\.\s+(.+)',           # 1. 2. 3. 4. 5.  (up to 5 options)
    r'^([A-Ea-e])\.\s+(.+)',        # A. B. C. D. E.
    r'^\(([1-5])\)\s+(.+)',        # (1) (2) (3) (4) (5)
    r'^\(([A-Ea-e])\)\s+(.+)',     # (A) (B) (C) (D) (E)  / (a)(b)(c)(d)(e)
    r'^([A-Ea-e])\)\s+(.+)',        # A) B) C) D) E)  / a) b) c) d) e)
]

def is_option(text):
    return any(re.match(p, text.strip()) for p in OPT_PATTERNS)

def clean_option_text(text):
    for p in OPT_PATTERNS:
        m = re.match(p, text.strip())
        if m: return m.group(2).strip()
    return text.strip()

# After collecting options per Q: options = options[:options_count]
# If still < options_count: try E-5 OMML and E-4 image check.
# If still missing: q_incomplete=True, exclude from template extraction.
```

### E-4 — Image extraction and mapping

```python
from docx import Document
import os

def extract_and_map_images(doc, paper_id):
    """
    BUG-A03 fix: accepts already-opened Document object, not doc_path.
    Caller (S3-1) opens Document once and passes it here.
    BUG-A21 fix: images before Q.1 (cur_q=None) are skipped.
    """
    DRAW_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    REL_NS  = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    BLIP_TAG = f'{{{DRAW_NS}}}blip'

    os.makedirs('/home/claude/pyq_images', exist_ok=True)

    # Step 1: Extract all embedded images by relationship ID
    # Map content-type to clean file extension (avoids 'vnd.ms-wmf' style invalid extensions)
    CTYPE_EXT = {
        'jpeg':'jpg','jpg':'jpg','png':'png','gif':'gif',
        'bmp':'bmp','tiff':'tif','webp':'webp',
        'vnd.ms-wmf':'wmf','x-wmf':'wmf','wmf':'wmf',
        'vnd.ms-emf':'emf','x-emf':'emf','emf':'emf',
    }
    img_map = {}   # rId -> (index, file_path)
    idx = 0
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            raw_ext = rel.target_part.content_type.split('/')[-1].lower()
            ext     = CTYPE_EXT.get(raw_ext, raw_ext)   # clean extension
            path    = f'/home/claude/pyq_images/{paper_id}_img{idx:03d}.{ext}'
            with open(path, 'wb') as img_f: img_f.write(rel.target_part.blob)
            img_map[rel.rId] = (idx, path)
            idx += 1

    # Step 2: Walk paragraphs tracking Q context
    cur_q   = None   # None until first Q detected -- images before Q.1 skipped
    cur_opt = 0
    imap    = []

    for para in doc.paragraphs:
        text = para.text.strip()
        q_n  = detect_question_start(text)
        if q_n is not None:
            cur_q = q_n; cur_opt = 0
        elif is_option(text):
            cur_opt += 1

        for elem in para._p.iter():
            if elem.tag == BLIP_TAG:
                rId = elem.get(f'{{{REL_NS}}}embed')
                # BUG-A21 fix: only map images when inside a question (cur_q not None)
                if rId in img_map and cur_q is not None:
                    i, path = img_map[rId]
                    pos = 'stem' if cur_opt == 0 else f'opt{cur_opt}'
                    imap.append({'img_idx': i, 'q_num': cur_q,
                                 'position': pos, 'path': path})

    # Step 3: Classify image role per Q
    q_roles = {}
    for entry in imap:
        k = entry['q_num']
        if k not in q_roles: q_roles[k] = {'stem': False, 'opts': False}
        if entry['position'] == 'stem': q_roles[k]['stem'] = True
        else:                           q_roles[k]['opts'] = True

    for qnum, r in q_roles.items():
        if r['stem'] and r['opts']: r['role'] = 'stem_and_options'
        elif r['stem']:              r['role'] = 'stem_only'
        elif r['opts']:              r['role'] = 'options_only'
        else:                        r['role'] = 'none'

    return img_map, imap, q_roles
```

IMAGE ROLES:
- `stem_and_options` -> format=FIGURAL, option_format=image_only (image options — e.g. shape matching)
- `stem_only`        -> format=FIGURAL, text options (image in stem only)
- `options_only`     -> format=FIGURAL, stem is text
- `none`             -> text-only question

### E-5 — OMML formula extraction

```python
MATH_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

def omml_to_linear(omath_elem):
    def recurse(el):
        tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
        if tag == 'r':
            t = el.find(f'{{{MATH_NS}}}t')
            return (t.text or '') if t is not None else ''
        elif tag == 'f':
            n = el.find(f'{{{MATH_NS}}}num'); d = el.find(f'{{{MATH_NS}}}den')
            return f'({recurse(n)})/({recurse(d)})' if n is not None and d is not None else '?/?'
        elif tag == 'sSup':
            b = el.find(f'{{{MATH_NS}}}e'); s = el.find(f'{{{MATH_NS}}}sup')
            return f'{recurse(b)}^{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'sSub':
            b = el.find(f'{{{MATH_NS}}}e'); s = el.find(f'{{{MATH_NS}}}sub')
            return f'{recurse(b)}_{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'rad':
            d = el.find(f'{{{MATH_NS}}}deg'); b = el.find(f'{{{MATH_NS}}}e')
            btext = recurse(b) if b is not None else '?'
            return f'root({d.text},{btext})' if d is not None and d.text else f'sqrt({btext})'
        else:
            return ''.join(recurse(c) for c in el)
    try:    return recurse(omath_elem).strip()
    except: return '[OMML_FAILED]'

def enrich_paragraph_with_omml(stem_text, paragraph):
    """
    Find all OMML nodes in paragraph, convert to linear text.
    BUG-A05 fix: all_ok starts True and is AND-reduced (not last-write-wins).
    Returns: (enriched_text, all_ok, has_omml)
    Failed OMML nodes are skipped (not appended) to avoid polluting templates.
    """
    additions = []
    all_ok    = True   # True = every OMML node in this paragraph converted OK
    for elem in paragraph._p.iter():
        if elem.tag == f'{{{MATH_NS}}}oMath':
            linear = omml_to_linear(elem)
            if '[OMML_FAILED]' in linear:
                all_ok = False          # propagate failure via AND
                # do NOT append failed output to stem
            else:
                additions.append(linear)
    has_omml = bool(additions) or not all_ok
    enriched = stem_text + (' ' + ' '.join(additions) if additions else '')
    return enriched.strip(), all_ok, has_omml
```

### E-6 — NOTE/instruction block detection

```python
# BUG-A14-related (Unicode): NOTE_PAT is a non-raw string so \u escapes ARE processed.
# v2.16 RIGID-6: expanded from English+Hindi to ALL major Indic scripts.
# Regional exams (Tamil Nadu PSC, AP/TS PSC, WBPSC, KPSC, etc.) use NOTE blocks
# in their respective scripts. Missing these would lose instruction metadata.
NOTE_PAT = re.compile(
    '\\((?:NOTE|Note|INSTRUCTION|Important|Caution'
    '|\u0928\u094b\u091f'           # Hindi/Marathi (Devanagari): नोट
    '|\u092e\u0939\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923'  # Hindi: महत्वपूर्ण
    '|\u0b95\u0bc1\u0bb1\u0bbf\u0baa\u0bcd\u0baa\u0bc1'              # Tamil: குறிப்பு
    '|\u0c17\u0c2e\u0c28\u0c3f\u0c15'                                # Telugu: గమనిక
    '|\u09a6\u09cd\u09b0\u09b7\u09cd\u099f\u09ac\u09cd\u09af'       # Bengali: দ্রষ্টব্য
    '|\u0c9f\u0cbf\u0caa\u0ccd\u0caa\u0ca3\u0cbf'                   # Kannada: ಟಿಪ್ಪಣಿ
    '|\u0d15\u0d41\u0d31\u0d3f\u0d2a\u0d4d\u0d2a\u0d4d'             # Malayalam: കുറിപ്പ്
    '|\u0a28\u0a4b\u0a1f'                                            # Punjabi (Gurmukhi): ਨੋਟ
    '|\u0aa8\u0acb\u0a82\u0aa7'                                      # Gujarati: નોંધ
    '|\u0b1f\u0b3f\u0b2a\u0b4d\u0b2a\u0b23\u0b40'                   # Odia: ଟିପ୍ପଣୀ
    ')[^)]{10,}\\)',
    re.DOTALL
)

def extract_note_block(stem_text):
    """Return (clean_stem, note_text, found)."""
    m = NOTE_PAT.search(stem_text)
    if m:
        note    = m.group(0)
        cleaned = (stem_text[:m.start()] + ' ' + stem_text[m.end():]).strip()
        return cleaned, note, True
    return stem_text, '', False

def classify_note_frequency(note_count, total):
    """mandatory >=80% | conditional 20-79% | rare 1-19% | never 0%"""
    if total == 0: return 'never'
    pct = note_count / total * 100
    if pct >= 80: return 'mandatory'
    if pct >= 20: return 'conditional'
    if pct >= 1:  return 'rare'
    return 'never'

def canonical_note_text(notes_by_year):
    """Most common NOTE text from most recent year. Skips None keys."""
    if not notes_by_year: return ''
    int_years = {k: v for k, v in notes_by_year.items() if isinstance(k, int)}
    if int_years:
        recent = max(int_years.keys())
        texts  = int_years[recent]
    else:
        texts  = list(notes_by_year.values())[0] if notes_by_year else []
    return Counter(texts).most_common(1)[0][0] if texts else ''
```

### E-7 — Linked group detection

```python
def detect_linked_groups(questions):
    """
    Method 1: reprinted stimulus — verbatim match >=90% (Cloze, DI, Reading Comprehension etc.).
    Method 2: proximity stimulus (non-reprinted passage) applied during extraction
              (long para before run of short-stem Qs — used in CAT, UPSC, CLAT etc.).
    """
    groups, visited = [], set()

    for i, q in enumerate(questions):
        if q['num'] in visited: continue
        visited.add(q['num'])   # mark lead question immediately to prevent re-processing
        stim_q = extract_stimulus(q['stem'])
        if not stim_q: continue
        members = [q['num']]

        for j in range(i+1, min(i+8, len(questions))):
            nq = questions[j]
            if nq['num'] in visited: break
            stim_nq = extract_stimulus(nq['stem'])
            if not stim_nq: break
            if SequenceMatcher(None, stim_q, stim_nq).ratio() >= 0.90:
                members.append(nq['num']); visited.add(nq['num'])
            else:
                break

        if len(members) > 1:
            groups.append({'group_id'      : f'G{len(groups)+1}',
                           'q_numbers'     : members,
                           'stimulus_text' : stim_q,
                           'stimulus_type' : classify_stimulus(stim_q),
                           'word_count'    : len(stim_q.split())})
            visited.update(members)

    return groups

def extract_stimulus(stem):
    """Extract shared stimulus portion (content before question ask)."""
    m = re.search(r'\b(Select|Find|Which|Who|What|How|Identify|Choose)\b', stem)
    if m and m.start() > 100: return stem[:m.start()].strip()
    return stem if len(stem.split()) > 50 else ''

def classify_stimulus(text):
    t = text.lower()
    if '|' in text or 'table' in t: return 'table'
    if any(kw in t for kw in ['clue','sitting','puzzle','arrangement']): return 'puzzle'
    if 'code' in t and 'means' in t: return 'code'
    return 'passage'
```

### E-8 — Option format classification (12 types)

```python
def classify_option_format(opts):
    """
    BUG-A23 fix: en-dash U+2013 matched via actual Unicode char (non-raw string).
    BUG-A12 / BUG-B19 fix: empty opts handled before any index access.
    12 types: single_value, value_pair, coordinate_pair, letter_cluster, code_pair,
              sentence, label_only, segment_label, roman_label, image_only,
              value_pair_quad, word_form_number
    """
    cleaned = [o.strip() for o in opts if isinstance(o, str)]
    if not cleaned or all(o == '' for o in cleaned): return 'image_only'

    wnums = {'one','two','three','four','five','six','seven','eight','nine','ten',
             'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen',
             'eighteen','nineteen','twenty'}
    if all(o.lower() in wnums for o in cleaned if o): return 'word_form_number'
    if all(o.lower() in {'i','ii','iii','iv','v','vi'} for o in cleaned if o):
        return 'roman_label'
    if all(len(o)==1 and o.upper() in 'ABCD' for o in cleaned if o):
        return 'segment_label'

    sent_kw = {'only','both','follow','follows','correct','neither','none'}
    if any(any(kw in o.lower() for kw in sent_kw) for o in cleaned if o):
        return 'sentence' if any(len(o.split()) > 3 for o in cleaned if o) else 'label_only'

    if all(re.match(r'^[A-D]-\d+(?:,\s*[A-D]-\d+)*$', o) for o in cleaned if o):
        return 'value_pair_quad'
    if all(re.match(r'^\(\d+,\s*\d+\)$', o) for o in cleaned if o):
        return 'coordinate_pair'

    # BUG-A23 fix: actual en-dash U+2013 embedded as literal character in raw string.
    # Cannot use \u2013 in raw string (r-prefix disables escapes).
    # Instead: compile pattern with en-dash as literal char (avoids SyntaxWarning).
    _VALUE_PAIR_PAT = re.compile(r'\d+\s*[-–]\s*\d+$')
    if all(_VALUE_PAIR_PAT.match(o) for o in cleaned if o):
        return 'value_pair'

    if all(re.match(r'^[A-Z]{2,6}$', o) for o in cleaned if o):
        return 'letter_cluster'
    if all('\u2192' in o or (' - ' in o and bool(re.search(r'[A-Z]{3,}', o)))
           for o in cleaned if o):
        return 'code_pair'
    return 'single_value'

def subtopic_option_format(qs):
    """
    BUG-A12 fix: guard for empty qs list (years[-1] IndexError).
    """
    if not qs:
        return {'primary':'single_value','recent_format':'single_value',
                'changed_recently':False,'all_observed':[]}
    fmts = [classify_option_format(q.get('options', [])) for q in qs]
    by_year = {}
    for q, fmt in zip(qs, fmts):
        by_year.setdefault(q.get('year', '?'), []).append(fmt)
    primary = Counter(fmts).most_common(1)[0][0]
    years   = sorted(by_year.keys())
    if not years:
        return {'primary':primary,'recent_format':primary,
                'changed_recently':False,'all_observed':list(set(fmts))}
    recent = Counter(by_year.get(years[-1], [])).most_common(1)
    rfmt   = recent[0][0] if recent else primary
    return {'primary':primary,'recent_format':rfmt,
            'changed_recently':rfmt != primary,'all_observed':list(set(fmts))}
```

### E-9 — Difficulty scoring (3-axis universal system)

```python
def score_difficulty(q, marks=1, strip_mode='reasoning'):
    """
    BUG-B07 fix: marks parameter USED in threshold scaling.
    BUG-B08 fix: 'rate','find the','what is' gated to quantitative mode only.
    BUG-A27 fix: decimal numbers included in V axis via float() conversion.
    time_per_q_sec parameter removed — difficulty is C+I+V axis-based, not time-based.
    Returns: {level, C, I, V, score, flags}
    """
    stem = q.get('stem', '')

    # AXIS 1: Computation steps (C)
    C = 1
    if any(kw in stem.lower() for kw in
           ['both','combined','together','compare','between two','ratio of two']):
        C = 4
    elif any(kw in stem.lower() for kw in
             ['partial','remaining','after repay','multi-year',
              'correct to two decimal']):
        C = 3
    # BUG-B08 fix: broad keywords only apply in quantitative mode
    elif strip_mode == 'quantitative' and any(kw in stem.lower() for kw in
             ['rate','find the','calculate','what is']):
        C = 2

    # AXIS 2: Indirection (I)
    I = 1
    if any(re.search(p, stem.lower()) for p in
           [r'ratio of .+ to', r'find .+ if .+ together', r'compare .+ two']):
        I = 3
    elif any(re.search(p, stem.lower()) for p in
             [r'if .+, find', r'such that', r'given that .+ find']):
        I = 2

    # AXIS 3: Value complexity (V)
    V = 1
    raw_nums = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', stem)
    if raw_nums:
        try:
            # BUG-A27 fix: use float() so decimals like '22.5' are included
            parsed = [float(n.replace(',', '')) for n in raw_nums]
            max_v   = max(parsed)
            has_dec = any('.' in n for n in raw_nums)
            non_rnd = max_v > 50000 and int(max_v) % 100 != 0
            if non_rnd or (max_v > 50000 and has_dec): V = 3
            elif has_dec or max_v > 10000:              V = 2
        except:
            pass

    score = C + I + V
    flags = []
    if re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b', stem):
        score += 1; flags.append('negative_question')
    # v2.5: MSQ cognitive-load term. A multi-select question forces independent
    # evaluation of EVERY option (not "find the one right answer"), so it is
    # strictly harder than its single-answer twin. +1, analogous to the negative_
    # question term. Dormant for single-answer exams (is_msq is always False when
    # multi_select_allowed=false). Step 8 B-DIFF mirrors this term for sync.
    if q.get('is_msq'):
        score += 1; flags.append('msq')

    # Difficulty thresholds: score <= simple → Simple, <= medium → Medium, else Hard.
    # Thresholds are universal — derived from the C+I+V axis system (min=3, max=10+).
    # C+I+V=3 (all axes at minimum) = trivially Simple for any exam.
    # C+I+V=10 (all axes at maximum) = Hard for any exam.
    # marks scaling: 2-mark Qs take 2× time so the bar for 'Simple' shifts up by 1.
    # These values are stable across exams because the axes are exam-agnostic.
    simple_threshold = 4 + (marks - 1)   # score ≤ this → Simple
    medium_threshold = 7 + (marks - 1)   # score ≤ this → Medium; else Hard

    if score <= simple_threshold:   level = 'Simple'
    elif score <= medium_threshold: level = 'Medium'
    else:                           level = 'Hard'

    return {'level':level, 'C':C, 'I':I, 'V':V, 'score':score, 'flags':flags}
```

### E-10 — Template generation (subject-aware variable stripping)

```python
def determine_strip_mode(section, topic, subtopic):
    """
    Exam-agnostic: infer stripping mode from taxonomy context words.
    v2.16 RIGID-5: Hindi equivalents added so Hindi-medium exams (e.g. MP PSC,
    UP PCS, Bihar PSC) with Devanagari headings are correctly classified instead
    of always falling to the default 'reasoning'.
    """
    s = section.lower(); t = topic.lower(); u = subtopic.lower()
    # Quantitative: English + Hindi keywords
    if any(kw in s for kw in ['quantitative','arithmetic','mathematics','math',
                               '\u0917\u0923\u093f\u0924',            # गणित (math)
                               '\u0905\u0902\u0915\u0917\u0923\u093f\u0924',  # अंकगणित (arithmetic)
                               '\u092e\u093e\u0924\u094d\u0930\u093e\u0924\u094d\u092e\u0915',  # मात्रात्मक
                              ]): return 'quantitative'
    if any(kw in t for kw in ['arithmetic','algebra','geometry','mensuration',
                               'trigonometry','statistics','number',
                               '\u092c\u0940\u091c\u0917\u0923\u093f\u0924',  # बीजगणित (algebra)
                               '\u0930\u0947\u0916\u093e\u0917\u0923\u093f\u0924',  # रेखागणित (geometry)
                               '\u0924\u094d\u0930\u093f\u0915\u094b\u0923\u092e\u093f\u0924\u093f',  # त्रिकोणमिति
                              ]): return 'quantitative'
    # English / Language
    if any(kw in s for kw in ['english','language','comprehension','verbal',
                               '\u0905\u0902\u0917\u094d\u0930\u0947\u091c\u0940',  # अंग्रेजी
                               '\u092d\u093e\u0937\u093e',           # भाषा (language)
                              ]): return 'english'
    # Logical
    if any(kw in u for kw in ['syllogism','statement','conclusion','venn',
                               '\u0928\u094d\u092f\u093e\u092f\u0935\u093e\u0915\u094d\u092f',  # न्यायवाक्य (syllogism)
                              ]): return 'logical'
    # Reasoning
    if any(kw in s for kw in ['reasoning','intelligence',
                               '\u0924\u0930\u094d\u0915\u0936\u0915\u094d\u0924\u093f',  # तर्कशक्ति (reasoning)
                               '\u092c\u0941\u0926\u094d\u0927\u093f',  # बुद्धि (intelligence)
                              ]):
        if any(kw in t for kw in ['analogy','series','coding','blood',
                                    'arrangement','sequence',
                                    '\u0938\u093e\u0926\u0943\u0936\u094d\u092f',  # सादृश्य (analogy)
                                    '\u0936\u094d\u0930\u0943\u0902\u0916\u0932\u093e',  # श्रृंखला (series)
                                   ]): return 'reasoning'
    # Factual / General Awareness
    if any(kw in s for kw in ['awareness','knowledge','general studies',
                               'current','static',
                               '\u0938\u093e\u092e\u093e\u0928\u094d\u092f \u091c\u094d\u091e\u093e\u0928',  # सामान्य ज्ञान
                               '\u091c\u093e\u0917\u0930\u0942\u0915\u0924\u093e',  # जागरूकता (awareness)
                              ]): return 'factual'
    return 'reasoning'

def strip_variables(stem, mode):
    """
    Strip variable parts from stem to produce structural skeleton.
    BUG-A14 fix: currency pattern uses non-raw string with actual \u20b9 (₹),
                 so the Unicode escape IS processed correctly.
    BUG-B10 fix: logical mode preserves trailing punctuation.
    """
    t = stem
    if mode == 'quantitative':
        t = re.sub('\u20b9\\s*[\\d,]+(?:\\.\\d+)?', '\u20b9_P_', t)  # ₹ currency
        t = re.sub(r'\d+(?:\.\d+)?%', '_R_%', t)
        t = re.sub(r'\b\d+\s*(?:years?|months?|days?|hours?|weeks?)\b',
                   '_T_', t, flags=re.IGNORECASE)
        t = re.sub(r'\b\d+(?:,\d+)*(?:\.\d+)?\b', '_NUM_', t)
        t = re.sub(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', '_NAME_', t)
    elif mode == 'reasoning':
        t = re.sub(r'\b[A-Z]{3,}\b', '_WORD_', t)
        t = re.sub(r'\b[A-Z]{2,4}(?:\s*:\s*[A-Z]{2,4})+\b', '_LCLUS_:_LCLUS_', t)
        t = re.sub(r'\b\d+(?:,\s*\d+){2,}\b', '_SERIES_', t)
        t = re.sub(r'\b\d+\b', '_NUM_', t)
    elif mode == 'factual':
        t = re.sub(r'\b(19|20)\d{2}\b', '_YEAR_', t)
        t = re.sub(r'\b\d+(?:st|nd|rd|th)?\b', '_NUM_', t)
    elif mode == 'english':
        t = re.sub(r'_{3,}', '_BLANK_', t)
    elif mode == 'logical':
        # BUG-B10 fix: strip trailing punctuation separately, restore after
        quantifiers = {'All','all','Some','some','No','no','None','none',
                       'are','is','can','never','be','being'}
        words  = t.split()
        result = []
        for w in words:
            w_clean  = w.rstrip('.,;:!?')
            trailing = w[len(w_clean):]
            if w_clean in quantifiers or not (w_clean and w_clean[0].isupper()):
                result.append(w)
            else:
                result.append('_NOUN_' + trailing)
        t = ' '.join(result)
    t = re.sub(r'^Q\.?\d+\.?\s*', '', t)
    t = re.sub(r'\[\d{1,2}-\w+-\d{4}[^\]]*\]', '', t)
    return t.strip()

def generate_templates(questions, strip_mode):
    """
    BUG-A04 fix: SequenceMatcher imported at module top (§1 S1-1).
    BUG-A13 fix: empty skeletons returns [] — caller handles this case.
    BUG-A20 fix: deprecated flag added to each pattern dict.
    """
    if not questions: return []

    years = sorted(set(q.get('year', 2020) for q in questions))
    last2 = set(years[-2:]) if len(years) >= 2 else set(years)

    skeletons = []
    for q in questions:
        if not q.get('stem'): continue
        skel = strip_variables(q['stem'], strip_mode)
        if not skel.strip(): continue
        weight = 2 if q.get('year') in last2 else 1
        skeletons.append({'skel':skel, 'weight':weight, 'year':q.get('year', 2020)})

    if not skeletons: return []

    clusters = []
    for item in skeletons:
        placed = False
        for c in clusters:
            if SequenceMatcher(None, c[0]['skel'], item['skel']).ratio() >= 0.90:
                c.append(item); placed = True; break
        if not placed: clusters.append([item])

    total_w  = sum(s['weight'] for s in skeletons) or 1
    pats_raw = sorted([{
        'skel'     : c[0]['skel'],
        'w_count'  : sum(i['weight'] for i in c),
        'raw_count': len(c),
        'years'    : sorted(set(i['year'] for i in c)),
    } for c in clusters], key=lambda p: -p['w_count'])

    for p in pats_raw:
        p['raw_pct']   = p['w_count'] / total_w * 100
        p['frequency'] = int(p['raw_pct'])
    deficit = 100 - sum(p['frequency'] for p in pats_raw)
    if deficit > 0:
        for p in sorted(pats_raw, key=lambda p: -(p['raw_pct']-p['frequency']))[:deficit]:
            p['frequency'] += 1

    result = []
    for i, p in enumerate(pats_raw, 1):
        conf = 'observed' if p['raw_count'] >= 3 else 'inferred'
        if p['years'] and all(y in last2 for y in p['years']) and len(p['years']) <= 2:
            conf = 'observed_recent'
        # BUG-A20 fix: deprecated flag for patterns absent from last 2 years
        deprecated = bool(p['years'] and not any(y in last2 for y in p['years']))
        result.append({
            'id'        : f'P{i}',
            'template'  : p['skel'],
            'frequency' : p['frequency'],
            'raw_count' : p['raw_count'],
            'confidence': conf,
            'deprecated': deprecated,
            'years'     : p['years'],
        })
    # Filter out patterns with frequency=0 (can occur for very rare templates
    # when raw_pct < 0.5% and largest-remainder does not assign them +1).
    # Such templates would appear in section_rules.md but never be selected by Step 7.
    result = [p for p in result if p['frequency'] >= 1]
    # Re-normalize if any were removed (ensure sum still = 100)
    if result:
        total_freq = sum(p['frequency'] for p in result)
        if total_freq != 100:
            # Add deficit to highest-frequency pattern (always the first after DESC sort)
            result[0]['frequency'] += (100 - total_freq)
    return result
```

APPROACH NAMING (add after generate_templates):
- quantitative: state formula ("Apply SI = PRT/100; find [variable] from [given]")
- reasoning:    state logic ("Decode substitution; apply same rule to target pair")
- factual:      state recall type ("Identify person/place from contextual clues")
- english:      state rule ("Select semantically correct word for blank position")
- logical:      "Evaluate statement-conclusion pairs using syllogism rules"

### E-11 — Wrong option structure classification (11 types)

```python
def classify_wrong_option_structure(subtopic_qs):
    """
    BUG-A08 fix: image-only check before fixed_set detection.
    BUG-A24 fix: empty strings filtered from shared_pool counter.
    BUG-B12 fix: image_only added to DESC dict (11th type).
    """
    all_opt_sets = [q['options'] for q in subtopic_qs if q.get('options')]
    if not all_opt_sets:
        return {'type':'varied','description':'No options to classify'}

    # BUG-A08 fix: detect image-only before entering fixed_set logic
    if all(o.strip() == '' for opts in all_opt_sets for o in opts):
        return {'type':'image_only',
                'description':'All options are images — option text is blank.'}

    frozen  = [frozenset(o.strip().lower() for o in s) for s in all_opt_sets]
    top_s, ct = Counter(frozen).most_common(1)[0]
    if ct / len(frozen) >= 0.80:
        canon = next(s for s in all_opt_sets
                     if frozenset(o.strip().lower() for o in s) == top_s)
        return {'type':'fixed_set',
                'description':'Identical options every question of this type.',
                'fixed_option_texts':[o.strip() for o in canon]}

    # BUG-A24 fix: filter empty strings from shared_pool counter
    all_words = Counter(o.strip().lower() for s in all_opt_sets for o in s if o.strip())
    top4      = [w for w, _ in all_words.most_common(4)]
    coverage  = sum(1 for s in all_opt_sets if any(o.strip().lower() in top4 for o in s))
    if top4 and coverage / len(all_opt_sets) >= 0.50 and len(all_words) < 8:
        return {'type':'shared_pool',
                'description':'Same word pool rotated as options across linked questions.',
                'shared_pool_words':top4}

    votes = Counter(_classify_one_set([o.strip() for o in s if o.strip()])
                    for s in all_opt_sets)
    dom   = votes.most_common(1)[0][0]
    # BUG-B12 fix: image_only added as 11th type in DESC
    DESC  = {
        'adjacent_values': 'Numeric options within +-20% — near-miss calculations.',
        'anagram'        : 'Options are character rearrangements of each other.',
        'alliterative'   : '3+ options share first letter — deliberate distractor.',
        'same_category'  : 'All options are real entities of the same class.',
        'sentence_label' : '"Only I follows" / "Both II and III follow" style.',
        'segment_label'  : 'Options are A/B/C/D referring to labelled stem segments.',
        'roman_label'    : 'Options are i/ii/iii/iv referring to numbered sub-items.',
        'value_pair_quad': 'Matching combinations: A-1, B-2, C-3, D-4.',
        'word_form'      : 'Options are number word forms: One/Two/Three/Four.',
        'image_only'     : 'All options are images — option text is blank.',
        'varied'         : 'No consistent structural pattern detected.',
    }
    return {'type':dom, 'description':DESC.get(dom, 'Pattern detected.')}

def _classify_one_set(opts):
    if not opts: return 'varied'
    if set(o.upper() for o in opts) == {'A','B','C','D'} and all(len(o)==1 for o in opts):
        return 'segment_label'
    if all(o.lower() in {'i','ii','iii','iv','v','vi'} for o in opts): return 'roman_label'
    wn = {'one','two','three','four','five','six','seven','eight','nine','ten'}
    if all(o.lower() in wn for o in opts): return 'word_form'
    kw = {'only','both','follow','correct','neither'}
    if any(any(k in o.lower() for k in kw) for o in opts): return 'sentence_label'
    csets = [Counter(o.upper().replace(' ','')) for o in opts]
    if len(set(frozenset(c.items()) for c in csets)) == 1 and len(opts[0]) <= 6:
        return 'anagram'
    fl = [o[0].upper() for o in opts if o]
    # Guard for empty fl (all opts were empty after filtering)
    most_fl = Counter(fl).most_common(1)
    if most_fl and most_fl[0][1] >= 3: return 'alliterative'
    nums = []
    for o in opts:
        try: nums.append(float(re.sub('[,\u20b9%\\s]', '', o)))
        except: pass
    if len(nums) == len(opts) and nums and max(nums) / max(min(nums), 0.001) <= 1.4:
        return 'adjacent_values'
    cap = sum(1 for o in opts if o and o[0].isupper() and not any(c.isdigit() for c in o))
    if cap >= 3: return 'same_category'
    return 'varied'
```

---

## §3 — DOCUMENT PROCESSING PIPELINE

### S3-1 — Per-paper pipeline

```python
def extract_year_from_filename(path):
    m = re.search(r'(20\d{2})', os.path.basename(path))
    return int(m.group(1)) if m else None

def extract_shift_from_filename(path):
    # v2.16 RIGID-1: uses SESSION_RE (dynamic from exam_config.json session_keyword)
    m = SESSION_RE.search(os.path.basename(path))
    return f'S{m.group(1)}' if m else 'S1'

def process_pyq_paper(docx_path, paper_id, exam_code,
                      time_per_q, marks_per_q, options_count, multi_select,
                      progress):
    """
    All parameters auto-detected in S1-3, passed directly — no cfg dict.
    taxonomy not needed: presorted papers carry their own taxonomy headings.
    extract_presorted() is the only extraction path.
    """
    from docx import Document
    doc   = Document(docx_path)   # opened ONCE; passed to all sub-functions
    year  = extract_year_from_filename(docx_path)
    shift = extract_shift_from_filename(docx_path)

    # E-4: extract images (pass already-opened doc)
    img_map, image_map, q_roles = extract_and_map_images(doc, paper_id)

    # Always presorted — single extraction path
    questions = extract_presorted(doc, year, shift, paper_id, q_roles,
                                  options_count, multi_select)

    linked_groups = detect_linked_groups(questions)
    link_map = {qn: g['group_id'] for g in linked_groups for qn in g['q_numbers']}

    for q in questions:
        sm      = determine_strip_mode(q.get('section',''), q.get('topic',''), q.get('subtopic',''))
        # Determine marks per question: try 'MCQ' key first (most exams),
        # then try all values and use the max (handles GATE 1-mark/2-mark structure
        # where marks_per_q = {'1-mark':1,'2-mark':2} — use max available mark as default).
        q_marks = marks_per_q.get('MCQ') or marks_per_q.get('mcq') or max(marks_per_q.values(), default=1)
        q['option_format']   = classify_option_format(q.get('options', []))
        q['paper_id']        = paper_id   # needed for max_per_paper/typical_per_paper computation
        q['difficulty']      = score_difficulty(q, marks=q_marks, strip_mode=sm)
        q['image_role']      = q_roles.get(q['num'], {}).get('role', 'none')
        q['linked_group_id'] = link_map.get(q['num'])
        q['year']            = year
        q['shift']           = shift
        q['paper_id']        = paper_id
        # v2.23 THREE-AXIS TAGGING: tag Axis-1/2/3 now that linked_group_id + image_role
        # + options are all set (the LINKED gate and FIGURAL/NAT signals need them).
        # Step 8 re-tags GENERATED questions with the SAME AXIS CLASSIFIER v1.0 functions.
        tag_axes(q)

    # §4: Claude runs vision analysis automatically on all qualifying figural questions.
    # No user involvement. Claude views each image file directly using the view tool.
    vision_candidates = get_vision_candidates(questions, q_roles, image_map)
    n_vision = 0
    for q, img_path in vision_candidates:
        vision_result = analyse_image_claude(q, img_path)   # Claude views img_path
        q.update({
            'object_type'   : vision_result.get('object_type'),
            'transformation': vision_result.get('transformation_type'),
            'arrangement'   : vision_result.get('arrangement'),
            'complexity'    : vision_result.get('complexity'),
            'image_clarity' : vision_result.get('image_clarity', 'clear'),
        })
        n_vision += 1

    for q in questions:
        key = (q.get('section','?'), q.get('topic','?'), q.get('subtopic','?'))
        progress.setdefault(key, []).append(q)

    progress.setdefault('_linked_groups', {})
    for g in linked_groups:
        progress['_linked_groups'][g['group_id']] = g

    meta = progress.setdefault('_meta', {'papers_processed':[],'total_questions':0,
                                          'years_processed':[]})
    meta['papers_processed'].append(paper_id)
    meta['total_questions'] += len(questions)
    if year and year not in meta['years_processed']:
        meta['years_processed'].append(year)

    print(f"  {os.path.basename(docx_path)}: {len(questions)} Qs, "
          f"{len(linked_groups)} linked groups, {n_vision} figural images analysed")
    return questions, linked_groups
```

### S3-2 — Presorted extraction (the only extraction mode)

```python
def is_taxonomy_heading(para):
    text = para.text.strip()
    if not text: return False
    if detect_question_start(text) is not None: return False
    if is_option(text): return False
    # BUG-A16 fix: check for date-format shift tag pattern, not just 'Shift' string
    # v2.16 SYNC: \d{1,2} (not \d{2}) to match single-digit days — aligned with PYQAnalyse.
    if re.match(r'\[\d{1,2}-', text): return False
    has_bold = any(r.bold for r in para.runs if r.text.strip())
    return has_bold and len(text) < 100

def parse_taxonomy_level(text):
    """
    v2.16 RIGID-4: expanded from 3 patterns to 12+ to handle diverse exam PYQ heading styles.
    Level 1 = Section/Subject (top-level grouping)
    Level 2 = Topic/Chapter (mid-level grouping)
    Level 3 = Subtopic (default — the leaf level for extraction)
    Exam-agnostic: covers SSC (Subject:), GATE (Section:), UPSC (Part:),
    regional exams (Unit:/Module:/Block:), and any numbered heading variant.
    """
    # Level 1: top-level section/subject headings
    if re.match(r'(?:Subject|Domain|Section|Part|Area)\s*:', text, re.IGNORECASE):
        return 1, text.split(':', 1)[1].strip()
    # Level 2: mid-level topic/chapter headings (with optional numbering)
    if re.match(r'(?:Topic|Chapter|Unit|Module|Block)\s+\d+', text, re.IGNORECASE):
        return 2, re.sub(r'(?:Topic|Chapter|Unit|Module|Block)\s+\d+[:.]\s*',
                         '', text, flags=re.IGNORECASE).strip() or text.strip()
    # Level 2: colon-style topic headings without numbering
    if re.match(r'(?:Topic|Chapter|Unit|Module|Block)\s*:', text, re.IGNORECASE):
        return 2, text.split(':', 1)[1].strip()
    return 3, text.strip()

def detect_blank_position(stem):
    m = re.search(r'_{3,}', stem)
    if not m: return 'none'
    pos = m.start() / max(len(stem), 1)
    return 'start' if pos < 0.2 else ('end' if pos > 0.8 else 'middle')

# ── v2.5 MSQ detection (EC-A root-cause fix) ──────────────────────────────────
# Forgery-resistant: keys on OPTION SHAPE, not stem wording. A statement-
# combination MCQ (EC-9) whose options are predominantly combination-labels
# ("Only 1", "Both 1 and 2", "Neither … nor …", "1 and 3", "None of …",
# "All of the above") is SINGLE-answer and must never be tagged MSQ, even when
# its stem reads "Which is/are correct". Conversely a genuine multi-select stem
# with ordinary content options IS an MSQ. Used only when multi_select=True.
_MSQ_INSTR_RE = re.compile(
    r'select all that apply|select all|one or more (?:options?|are|may)|'
    r'select\s+two|select\s+three|more than one (?:option|correct)|'
    r'which .*\bare correct\b', re.IGNORECASE)
_COMBO_OPT_RE = re.compile(
    r'^\s*(only\b|both\b|neither\b|all of\b|none of\b|'
    r'\d+\s+and\s+\d+\b|\d+\s*,\s*\d+)', re.IGNORECASE)

def _is_statement_combination(options):
    """True when the option SET is predominantly combination-labels (EC-9 MCQ)."""
    opts = [o for o in (options or []) if isinstance(o, str) and o.strip()]
    if not opts:
        return False
    combo = sum(1 for o in opts if _COMBO_OPT_RE.match(o.strip()))
    return combo >= max(2, len(opts) - 1)   # most/all options are combo-labels

def detect_is_msq(full_stem, options):
    """v2.5 contract detector. Caller already gated on multi_select=True."""
    if not _MSQ_INSTR_RE.search(full_stem or ''):
        return False
    if _is_statement_combination(options):   # EC-A guard
        return False
    return True

def _detect_option_label_style(raw_option_lines):
    """
    v2.15 BUG-D07: Detect option LABEL style from raw option lines.
    Returns: '1/2/3/4' | 'A/B/C/D' | '(1)/(2)/(3)/(4)' | '(A)/(B)/(C)/(D)' | 'A)/B)/C)/D)' | 'unknown'
    Distinct from option FORMAT type (single_value etc.) which describes CONTENT shape.
    """
    if not raw_option_lines:
        return 'unknown'
    for line in raw_option_lines:
        t = line.strip()
        if re.match(r'^[1-5]\.\s+', t):       return '1/2/3/4'
        if re.match(r'^[A-E]\.\s+', t):        return 'A/B/C/D'
        if re.match(r'^[a-e]\.\s+', t):        return 'a/b/c/d'
        if re.match(r'^\([1-5]\)\s+', t):      return '(1)/(2)/(3)/(4)'
        if re.match(r'^\([A-E]\)\s+', t):      return '(A)/(B)/(C)/(D)'
        if re.match(r'^\([a-e]\)\s+', t):      return '(a)/(b)/(c)/(d)'
        if re.match(r'^[A-E]\)\s+', t):        return 'A)/B)/C)/D)'
        if re.match(r'^[a-e]\)\s+', t):        return 'a)/b)/c)/d)'
    return 'unknown'


def extract_presorted(doc, year, shift, paper_id, q_roles, options_count, multi_select):
    questions = []
    cur_sec = cur_top = cur_sub = ''
    paras   = doc.paragraphs
    i = 0

    while i < len(paras):
        para = paras[i]; text = para.text.strip()
        if not text: i += 1; continue

        if is_taxonomy_heading(para):
            lv, content = parse_taxonomy_level(text)
            if lv == 1: cur_sec = content
            elif lv == 2: cur_top = content
            else: cur_sub = content
            i += 1; continue

        # BUG-A16 fix: case-insensitive shift tag check via pattern
        if re.match(r'\[\d{1,2}-', text):
            i += 1; continue

        q_num = detect_question_start(text)
        if q_num is None: i += 1; continue

        stem_parts   = [re.sub(r'^Q\.?\d+\.?\s*', '', text).strip()]
        options      = []
        options_raw  = []   # v2.15 BUG-D07: raw option lines for label detection
        omml_present = False
        omml_ok      = True   # BUG-A05 fix: start True, AND-reduce below
        i += 1

        while i < len(paras):
            nt = paras[i].text.strip()
            if not nt: i += 1; continue
            if detect_question_start(nt) is not None or is_taxonomy_heading(paras[i]):
                break
            if is_option(nt):
                options.append(clean_option_text(nt))
                options_raw.append(nt)   # v2.15: preserve raw line for label detection
            else:
                enriched, ok, has_omml = enrich_paragraph_with_omml(nt, paras[i])
                if has_omml:
                    omml_present = True
                    omml_ok      = omml_ok and ok  # BUG-A05 fix: AND not replace
                    stem_parts.append(enriched)
                else:
                    stem_parts.append(nt)
            i += 1

        full_stem  = ' '.join(stem_parts)
        clean_stem, note, note_found = extract_note_block(full_stem)
        blank_pos  = detect_blank_position(clean_stem)
        is_neg     = bool(re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b', full_stem))
        # multi_select is auto-detected in S1-3 from exam pattern + PYQ stems.
        # v2.5 EC-A ROOT-CAUSE FIX: the old detector (r'select all|which.*are correct')
        # false-matched statement-combination MCQs (EC-9: "Which is/are correct?" with
        # combo-label options "1. Only A", "3. Both A and B"), which are SINGLE-answer.
        # The forgery-resistant signal is OPTION SHAPE, not stem wording:
        #   - a stem with a genuine multi-select instruction phrase, AND
        #   - options that are NOT predominantly combination-labels (only/both/neither/
        #     "X and Y"/none-of/all-of) ⇒ MSQ.
        # A statement-combination MCQ (most options are combo-labels) is NEVER MSQ even
        # when its stem says "are correct". Validated empirically (both directions).
        is_msq = bool(multi_select) and detect_is_msq(full_stem, options)

        # BUG-D07 fix (v2.15): detect option label style per question
        # from the RAW option lines (before clean_option_text strips the label).
        # This is the LABEL style ('1/2/3/4' vs 'A/B/C/D' etc.), distinct from
        # option FORMAT type ('single_value' etc.) which describes content shape.
        _label = _detect_option_label_style(options_raw)

        questions.append({
            'num'         : q_num,
            'stem'        : clean_stem,
            'stem_raw'    : full_stem,
            'options'     : options,
            'section'     : cur_sec,
            'topic'       : cur_top,
            'subtopic'    : cur_sub,
            'has_note'    : note_found,
            'note_text'   : note,
            'blank_pos'   : blank_pos,
            'is_negative' : is_neg,
            'is_msq'      : is_msq,
            'omml_present': omml_present,
            'omml_failed' : omml_present and not omml_ok,
            'option_label': _label,   # v2.15 BUG-D07: '1/2/3/4' | 'A/B/C/D' | etc.
        })
    return questions
```

---

## §4 — VISION ANALYSIS FOR FIGURAL QUESTIONS

Claude performs all vision analysis automatically using the `view` tool.
The user is never asked to describe images. This is Claude's responsibility.

### S4-1 — When to run

After E-4 maps images to questions, identify which questions need vision:

```python
def get_vision_candidates(questions, q_roles, imap):
    """
    Returns list of (q, image_path) pairs requiring vision analysis.
    Only questions where the image is in the stem (or stem+options).
    options_only: E-11 classifies those from text patterns, no vision needed.
    Text-extractable subtopics (dice, cube, counting shapes etc.): values
    already present in stem text — vision adds nothing for these.
    imap: image mapping list from extract_and_map_images() — passed explicitly.
    """
    candidates = []
    # SKIP_TEXT_EXTRACTABLE: subtopics where the image contains countable/readable
    # values already present as text in the stem — vision adds no information.
    # Detected by checking if stem contains numeric/face values AND subtopic name
    # suggests a counting/identification task (dice, cube, counting shapes, etc.).
    # This list is NOT hardcoded — it is inferred from subtopic name keywords.
    SKIP_KEYWORDS = {'dice', 'cube', 'count', 'counting', 'dots', 'faces', 'nets'}

    for q in questions:
        role = q_roles.get(q['num'], {}).get('role', 'none')

        if role not in ('stem_only', 'stem_and_options'):
            continue   # options_only or none: no stem image, skip

        sub_lower = q.get('subtopic', '').lower()
        if any(kw in sub_lower for kw in SKIP_KEYWORDS):
            continue   # stem already has the values; vision not needed

        # Get the path(s) of stem images for this Q (imap passed from E-4)
        stem_imgs = [entry for entry in imap
                     if entry['q_num'] == q['num']
                     and entry['position'] == 'stem']
        if stem_imgs:
            candidates.append((q, stem_imgs[0]['path']))   # use first stem image

    return candidates
```

### S4-2 — Automated vision analysis (Claude uses view tool directly)

```python
def analyse_image_claude(q, image_path):
    """
    Claude views the image file directly using the view tool.
    No user input. All classification done by Claude's vision capability.
    Returns: dict with object_type, transformation_type, complexity, arrangement,
             image_clarity fields populated.
    """

    # Claude executes: view(image_path)
    # Then reads and classifies what it sees using the taxonomy below.

    # OBJECT TYPE — what kind of object appears in the figure:
    #   geometric_shape  : circles, triangles, squares, pentagons, stars etc.
    #   letter_character : uppercase/lowercase English or Hindi letters
    #   digit            : numerals used as visual elements
    #   arrow            : directional arrows, pointers
    #   clock_face       : analog clock with hands
    #   tool_object      : scissors, keys, locks, cups, chairs, everyday objects
    #   natural_object   : trees, leaves, animals, mountains
    #   symbolic         : flags, currency symbols, abstract symbols
    #   compound_figure  : two or more different object types combined
    #   pattern_matrix   : grid/matrix of symbols (3×3 etc.)
    #   other            : none of the above

    # TRANSFORMATION TYPE — what operation connects elements (for series/analogy):
    #   mirror_horizontal : reflected left-right
    #   mirror_vertical   : reflected top-bottom
    #   rotation_90cw     : rotated 90° clockwise
    #   rotation_90ccw    : rotated 90° counter-clockwise
    #   rotation_180      : rotated 180°
    #   element_added     : one or more elements added to the figure
    #   element_removed   : one or more elements removed
    #   shading_changed   : fill/shading pattern changed
    #   size_changed      : figure scaled up or down
    #   complex_compound  : multiple transformations combined
    #   other             : pattern present but doesn't fit above types
    #   N/A               : single image (no transformation — single object question)

    # COMPLEXITY:
    #   Simple : single unambiguous object, one clear transformation, obvious axis
    #   Medium : compound figure OR multiple elements with one transformation
    #   Hard   : multi-element figure with complex/ambiguous transformation

    # ARRANGEMENT — how images are laid out across the question:
    #   row_series   : images in a horizontal sequence (A, B, C, D, ?)
    #   matrix       : images in a grid (3×3 matrix pattern)
    #   pair_analogy : two pairs (A:B :: C:?)
    #   single       : one standalone image (count, identify, or find mirror)

    # IMAGE CLARITY:
    #   clear   : Claude can read the figure confidently
    #   unclear : image too small, blurry, or corrupted to classify reliably
    #             When unclear: record image_clarity='unclear', leave other fields blank.
    #             DO NOT guess. QV-9 tracks unclear rate — flags if >20%.

    # RULES:
    # 1. Claude views every qualifying image. No sampling, no skipping.
    # 2. Record what IS there, not what might be there.
    # 3. For series questions: transformation_type describes the rule across the series.
    # 4. For analogy questions: transformation_type describes A→B operation.
    # 5. For single-image questions (mirror/identify): transformation_type = 'N/A'.
    # 6. Multiple images in one question (e.g., 6-image row_series):
    #    analyse the series as a whole; record one set of fields for the question.

    pass  # Claude fills this by actually viewing image_path and reasoning about it
```

### S4-3 — Integration into paper processing pipeline

Vision analysis runs automatically inside `process_pyq_paper()` (§3 S3-1),
immediately after extraction and before accumulation into progress.
The complete implementation is in S3-1 — this section is reference only.

Key points:
- `get_vision_candidates(questions, q_roles, image_map)` filters to qualifying Qs
- `analyse_image_claude(q, img_path)` — Claude views each image using the view tool
- Vision fields merged into each question dict before progress accumulation
- No separate vision pass. No user prompts. No waiting between images.
- Claude views every qualifying image inline as part of processing each paper.

### S4-4 — Aggregate per subtopic (unchanged logic, fully automated)

```python
def aggregate_figural(questions_for_subtopic, q_roles=None):
    """
    Called during synthesis (§5) for FIGURAL subtopics.
    Vision fields (object_type, transformation, arrangement, complexity,
    image_clarity) were populated automatically during S4-3 paper processing.
    This function aggregates across all observed questions for the subtopic.
    image_role derived from q['image_role'] stored in each question dict (not q_roles,
    which is not persisted in progress.json across sessions).
    q_roles parameter retained for backward compatibility but is unused.
    """
    obj_types    = []
    transforms   = []
    arrangements = []
    complexities = []
    n_unclear    = 0

    for q in questions_for_subtopic:
        if q.get('image_clarity') == 'unclear':
            n_unclear += 1
            continue
        if q.get('object_type'):    obj_types.append(q['object_type'])
        if q.get('transformation'): transforms.append(q['transformation'])
        if q.get('arrangement'):    arrangements.append(q['arrangement'])
        if q.get('complexity'):     complexities.append(q['complexity'])

    def top(lst, n=3):
        return [x for x, _ in Counter(lst).most_common(n)]

    # Dominant image_role from q['image_role'] stored in each question dict during S3-1.
    # q_roles dict is NOT persisted in progress.json — using stored field avoids the loss.
    roles = [q.get('image_role', 'none') for q in questions_for_subtopic
             if q.get('image_role', 'none') != 'none']
    dominant_role = Counter(roles).most_common(1)[0][0] if roles else 'stem_only'

    return {
        'image_role'          : dominant_role,
        'object_types'        : {
            'dominant': top(obj_types, 3),
            'observed': list(set(obj_types)),
            'avoid'   : [],
        },
        'transformation_types': list(set(t for t in transforms if t != 'N/A')),
        'arrangement_types'   : list(set(arrangements)),
        'complexity_dist'     : ({k: round(v / len(complexities) * 100)
                                   for k, v in Counter(complexities).items()}
                                  if complexities else {}),
        'images_analysed'     : len(obj_types),
        'images_unclear'      : n_unclear,
    }
```

---

## §5 — SYNTHESIS ENGINE

### S5-1 — Pre-synthesis check

```python
def pre_synthesis_check(progress, taxonomy, target='ALL'):
    for sec, entries in taxonomy.items():
        if target != 'ALL' and sec != target: continue
        for e in entries:
            key   = (sec, e['topic'], e['subtopic'])
            count = len(progress.get(key, []))
            if count == 0:  print(f"ABSENT: {e['subtopic']} -- no PYQ data")
            elif count < 3: print(f"SPARSE: {e['subtopic']} -- only {count} Qs (inferred)")
```

### S5-2 — Per-subtopic synthesis

```python
# ════════════════════════════════════════════════════════════════════════════
# AXIS CLASSIFIER v1.0  (v2.23 — SHARED SINGLE SOURCE OF TRUTH)
# ────────────────────────────────────────────────────────────────────────────
# The canonical, exam-agnostic classifier for the three orthogonal format axes.
# Step 8 (MockCreateAudit) MUST re-tag GENERATED questions with THESE SAME
# functions (import/copy verbatim, never re-implement) — the PYQ distribution and
# the generated distribution are only comparable if classified identically.
#
#   Axis 1  STIMULUS/MEDIA  : TEXT | FIGURAL | PASSAGE | DI
#   Axis 2  STEM STRUCTURE  : the exclusive 8-class ladder (below)
#   Axis 3  ANSWER MECHANISM: MCQ | MSQ | NAT
#   negative polarity       : an ORTHOGONAL boolean flag (is_negative), NOT a class
#
# EXCLUSIVITY: every question maps to exactly ONE Axis-2 class (first-match-wins).
# LINKED is a GATE decided by shared-stimulus membership (linked_group_id), never by
# phrasing — an assertion-reason question printed inside a passage is LINKED, and its
# inner shape becomes a secondary detail only. SEQUENCE sits ABOVE STATEMENT because
# "arrange the following statements in order" is fundamentally an ordering task.
# ════════════════════════════════════════════════════════════════════════════

AXIS2_CLASSES = ['LINKED', 'ASSERTION_REASON', 'MATCH', 'SEQUENCE', 'STATEMENT',
                 'FILL_BLANK', 'ODD_ONE_OUT', 'DIRECT']   # ladder order == precedence

# Canonical stem_format_variant → Axis-2 class map. Step 7's STEM_FORMAT_MENU tokens
# MUST map through this table (File 4 wires Step 7 to it) so capability stays consistent.
STEM_FORMAT_TO_AXIS2 = {
    'direct_question': 'DIRECT', 'isolated_word': 'DIRECT', 'phrase_to_word': 'DIRECT',
    'reverse_word_to_phrase': 'DIRECT', 'definition_to_word': 'DIRECT',
    'meaning_of_idiom': 'DIRECT', 'idiom_for_situation': 'DIRECT',
    'sentence_substitution': 'DIRECT', 'sentence_embedded_underlined': 'DIRECT',
    'fill_blank': 'FILL_BLANK', 'fill_in_context_blank': 'FILL_BLANK',
    'assertion_reason': 'ASSERTION_REASON', 'match_the_following': 'MATCH',
    'statement_correctness': 'STATEMENT', 'sequence_ordering': 'SEQUENCE',
    'odd_one_out': 'ODD_ONE_OUT', 'odd_one_out_pair': 'ODD_ONE_OUT',
}

# family → set of Axis-2 classes its Step-7 menu can faithfully render (derived from
# Step 7 STEM_FORMAT_MENU via STEM_FORMAT_TO_AXIS2; kept explicit for round-trip clarity).
FAMILY_AXIS2_MENU = {
    'vocab_single_word'    : {'DIRECT', 'FILL_BLANK', 'ODD_ONE_OUT'},
    'one_word_substitution': {'DIRECT'},
    'idiom_phrase'         : {'DIRECT', 'ODD_ONE_OUT'},
    'fact_recall'          : {'DIRECT', 'FILL_BLANK', 'ASSERTION_REASON', 'MATCH',
                              'ODD_ONE_OUT', 'STATEMENT'},
}

_TABLE_WORD_RE = re.compile(r'(?i)\b(table|tabulated|following data|dataset)\b')
def _looks_like_table_stimulus(stem):
    """v2.24.6 FIX C — SHARED, single-source-of-truth structural table detector.
    Was, independently in TWO places (classify_axis1 here and synthesise_subtopic's
    has_tbl), a naive substring match `'|' in stem or 'table' in stem.lower()` that
    false-positived on any word merely CONTAINING "table" — "vegetable", "acceptable",
    "notable" — with no real tabular data present. Requires either (a) >=2 pipe-delimited
    rows (a real rendered table), or (b) a word-boundary table-keyword match co-occurring
    with >=1 pipe-delimited row. A bare stray '|' or an unrelated "table"-containing word
    alone no longer qualifies. MUST PROPAGATE (byte-identical) to Step 8 MockCreateAudit
    S6-1b (verbatim classifier copy) — same requirement as classify_axis2's MATCH rule.
    """
    stem = stem or ''
    pipe_rows = sum(1 for ln in stem.splitlines() if ln.count('|') >= 2)
    return pipe_rows >= 2 or (bool(_TABLE_WORD_RE.search(stem)) and pipe_rows >= 1)

def classify_axis1(q):
    """STIMULUS/MEDIA. Priority FIGURAL > PASSAGE > DI > TEXT — identical ordering to
    the per-subtopic `fmt` line in synthesise_subtopic (a linked DI passage resolves
    PASSAGE, matching that function)."""
    if q.get('image_role', 'none') not in ('none', None):
        return 'FIGURAL'
    if q.get('linked_group_id'):
        return 'PASSAGE'
    stem = (q.get('stem') or q.get('stem_raw') or '')
    if _looks_like_table_stimulus(stem):
        return 'DI'
    return 'TEXT'

def classify_axis3(q):
    """ANSWER MECHANISM. NAT = no selectable options (mirrors the answer_type=='numerical'
    detection: zero text options AND no option-images). MSQ = is_msq. Else MCQ."""
    opts = q.get('options', []) or []
    if len(opts) == 0 and q.get('image_role', 'none') not in ('options_only', 'stem_and_options'):
        return 'NAT'
    return 'MSQ' if q.get('is_msq') else 'MCQ'

def _opts_are_combination_labels(opts):
    """EC-A signal: options predominantly combination-labels (Only N / Both N and M /
    Neither…nor / None of / All of the above / "N and M"). Distinguishes STATEMENT and
    MATCH combo-answer stems from genuine free-form options."""
    if not opts:
        return False
    combo = 0
    for o in opts:
        t = (o or '').strip().lower()
        if re.search(r'\b(only|both|neither|none of|all of)\b', t) or \
           re.match(r'^[a-d1-4](\s*(and|,|&|-)\s*[a-d1-4])+$', t):
            combo += 1
    return combo >= max(2, (len(opts) + 1) // 2)

# ── MATCH option-shape backstop (v2.24.2) ──────────────────────────────────────
# A language-agnostic MATCH signal: the OPTIONS are a set of CROSS-DOMAIN label pairs
# (e.g. "A-I, B-III, C-IV, D-II" / "1-C 2-A 3-D 4-B" / "(A)-(i), (B)-(iv) ..."). It fires
# when the stem keywords (match / list-I / column) are ABSENT — the two cases that matter:
#   (a) NON-ENGLISH match papers (Hindi/regional), whose stems carry no English cue;
#   (b) matches whose List-I/List-II body has been rendered into a Word table, so the list
#       labels no longer appear in stem_raw (only the "Match ..." instruction does).
# CROSS-DOMAIN (left label family != right label family) is REQUIRED, so digit:digit ratios
# ("2:3, 4:5"), coordinate pairs and word-word hyphenations never trip it. The family of a
# COLUMN (not a single token) is used so the roman-vs-letter "I" ambiguity resolves from
# context (a column carrying II/III/IV is roman even where a bare I appears).
_MATCH_PAIR_RE = re.compile(
    r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
    r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MATCH_PAIR_SUB = (r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
                   r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MATCH_OPT_RE = re.compile(r'^\s*' + _MATCH_PAIR_SUB + r'(?:[,;\s]+' + _MATCH_PAIR_SUB + r'){1,}\s*$')

def _label_family(tokens):
    """Family of a same-side label COLUMN: 'digit' | 'roman' | 'alpha' | 'other'.
    Column-level (not per-token) so a bare 'I' resolves to roman when its column also
    carries II/III/IV, and to alpha when its column is A/B/C/D."""
    low = [t.lower() for t in tokens if t]
    if not low:
        return 'other'
    if all(re.fullmatch(r'\d{1,2}', t) for t in low):
        return 'digit'
    romanish = all(re.fullmatch(r'[ivxlcdm]+', t) for t in low)
    if romanish and any(len(t) > 1 for t in low):
        return 'roman'
    if all(re.fullmatch(r'[a-z]', t) for t in low):
        return 'roman' if set(low) <= {'i', 'v', 'x'} else 'alpha'
    if romanish:
        return 'roman'
    if all(re.fullmatch(r'[a-z]{1,4}', t) for t in low):
        return 'alpha'
    return 'other'

def _opts_are_match_pairs(opts):
    """True when a MAJORITY of options are each a set of >=2 CROSS-DOMAIN label pairs that
    consume the whole option text. Threshold mirrors _opts_are_combination_labels. Used by
    classify_axis2 AFTER the keyword rules, so it can only convert a would-be non-MATCH
    class to MATCH, never the reverse (additive + monotone)."""
    if not opts:
        return False
    hits = 0
    for o in opts:
        st = (o or '').strip()
        if not st or not _MATCH_OPT_RE.match(st):
            continue
        pairs = _MATCH_PAIR_RE.findall(st)
        if len(pairs) < 2:
            continue
        lf = _label_family([p[0] for p in pairs])
        rf = _label_family([p[1] for p in pairs])
        if lf == rf or 'other' in (lf, rf):
            continue
        hits += 1
    return hits >= max(2, (len(opts) + 1) // 2)

def classify_axis2(q):
    """STEM STRUCTURE — the exclusive 8-class ladder (first-match-wins). Discrimination
    is by task-verb + option-shape, not ladder position alone, so collisions are rare and
    deterministic. Grounded in EC-8/9/11/12/13; SEQUENCE + ODD_ONE_OUT added in v2.23."""
    # GATE 0 — LINKED: structural, decided by shared-stimulus membership, not phrasing.
    if q.get('linked_group_id'):
        return 'LINKED'
    stem = (q.get('stem_raw') or q.get('stem') or '')
    s    = stem.lower()
    opts = q.get('options', []) or []
    # 1 — ASSERTION_REASON (EC-8): both an Assertion and a Reason clause present.
    if re.search(r'\bassertion\b', s) and re.search(r'\breason\b', s):
        return 'ASSERTION_REASON'
    # 2 — MATCH (EC-13): match/list-I/column stems, OR (v2.24.2) a CROSS-DOMAIN label-pair
    #     option shape. The option-shape backstop is language-agnostic and table-safe (see
    #     _opts_are_match_pairs): it catches non-English matches and matches whose List-I/
    #     List-II body has moved into a Word table. Placed AFTER the keyword rules it is
    #     additive/monotone — it only converts a would-be non-MATCH class to MATCH.
    if re.search(r'\bmatch\b', s) and re.search(r'\b(following|list|column|set)\b', s):
        return 'MATCH'
    if re.search(r'list[\s\-]*i\b|column[\s\-]*(i|a)\b', s):
        return 'MATCH'
    if _opts_are_match_pairs(opts):
        return 'MATCH'
    # 3 — SEQUENCE / ORDERING (v2.23): the OPERATION is arranging (kept above STATEMENT).
    if re.search(r'\b(arrange|rearrange|correct sequence|proper sequence|correct order|'
                 r'logical order|chronological order|sequence of the following|'
                 r'order of the following)\b', s):
        return 'SEQUENCE'
    # 4 — STATEMENT-BASED (EC-9): "consider the following statements … which is/are correct"
    #     with combination-label options (the EC-A option-shape signal confirms it).
    if re.search(r'consider the following statements?|following statements?\b', s) and \
       (re.search(r'which .*(is|are) (correct|true|incorrect|false)', s)
        or _opts_are_combination_labels(opts)):
        return 'STATEMENT'
    # 5 — FILL_BLANK / CLOZE (EC-11): a blank to complete.
    if q.get('blank_pos', 'none') not in ('none', None) or re.search(r'_{3,}|\bfill in the blank', s):
        return 'FILL_BLANK'
    # 6 — ODD_ONE_OUT: genuine "which does not belong" classification (narrowed — mere
    #     negative phrasing is is_negative, handled orthogonally, not this class).
    if re.search(r'\bodd one out\b|does not belong|which one is different|find the odd', s):
        return 'ODD_ONE_OUT'
    # 7 — DIRECT: residual floor.
    return 'DIRECT'

def tag_axes(q):
    """Attach the three exclusive axis labels to a question dict in place. is_negative is
    already set during extraction (EC-12). Idempotent."""
    q['axis1'] = classify_axis1(q)
    q['axis2'] = classify_axis2(q)
    q['axis3'] = classify_axis3(q)
    return q

# family keyword → family key (Step-5 approximation of Step 7 resolve_presentation_family;
# Step 7 refines with CONCEPT_GROUP at its S3-8 join. Exam-agnostic keyword sets.)
_FAMILY_KEYWORDS = {
    'vocab_single_word'    : ('antonym', 'synonym', 'spelling', 'homonym'),
    'one_word_substitution': ('one word substitution', 'one-word'),
    'idiom_phrase'         : ('idiom', 'phrase'),
    'fact_recall'          : ('gk', 'general awareness', 'general knowledge', 'static',
                              'current affairs', 'fact'),
}

def resolve_presentation_family_s5(subtopic, fmt):
    """Lightweight family resolution from the subtopic name + format. Returns a family key
    or None. Mirrors Step 7 PRESENTATION_FAMILIES; used only to seed axis2_capability —
    Step 7 remains authoritative once CONCEPT_GROUP is joined."""
    name = (subtopic or '').lower()
    for fam, kws in _FAMILY_KEYWORDS.items():
        if any(kw in name for kw in kws):
            return fam
    return None

def axis2_capability(observed_axis2, presentation_family, fmt):
    """The Axis-2 forms a subtopic may FAITHFULLY take (decisions (b)/(c)):
       observed ∪ family-menu ∪ {DIRECT}, with LINKED added iff the subtopic is
       stimulus-linked (format PASSAGE/DI) and removed otherwise. Forcing a form OUTSIDE
       this set is fabrication (Step 7 decision-(iii) ban)."""
    cap = set(observed_axis2) | {'DIRECT'}
    cap |= FAMILY_AXIS2_MENU.get(presentation_family, set())
    if str(fmt).upper() in ('PASSAGE', 'DI'):
        cap.add('LINKED')
    else:
        cap.discard('LINKED')
    return [c for c in AXIS2_CLASSES if c in cap]   # canonical ladder order

def compute_section_axis_distribution(sec_entries, progress, mocks_per_window=10):
    """CATEGORY A per-section target. Averages each axis's class counts PER PAPER over the
    3 most-recent distinct years, and classifies each Axis-2 class band vs guarantee-only.
    Returns None for a section with no observed questions (all Zero-PYQ scaffolds)."""
    qs = []
    for e in sec_entries:
        qs.extend(progress.get((e['section'], e['topic'], e['subtopic']), []))
    if not qs:
        return None
    for q in qs:                                   # ensure tagged (idempotent)
        if 'axis2' not in q:
            tag_axes(q)
    years   = sorted({q.get('year') for q in qs if q.get('year')}, reverse=True)
    recent3 = set(years[:3]) if years else set()
    rq      = [q for q in qs if q.get('year') in recent3] or qs
    n_papers = max(1, len({(q.get('year'), q.get('shift')) for q in rq}))

    def per_paper(axis):
        c = Counter(q.get(axis, '?') for q in rq)
        return {k: round(v / n_papers, 3) for k, v in c.items()}

    axis2 = per_paper('axis2')
    audit_mode = {}
    for cls, avg in axis2.items():
        if cls == 'DIRECT':
            audit_mode[cls] = 'float'              # residual filler — never audited (decision 5/10)
        else:
            audit_mode[cls] = 'band' if avg * mocks_per_window >= 1 else 'guarantee'
    return {
        'recent_years'    : sorted(recent3, reverse=True),
        'n_papers_recent' : n_papers,
        'mocks_per_window': mocks_per_window,
        'axis1_per_paper' : per_paper('axis1'),
        'axis2_per_paper' : axis2,
        'axis3_per_paper' : per_paper('axis3'),
        'axis2_audit_mode': audit_mode,
        'negative_rate'   : round(sum(1 for q in rq if q.get('is_negative')) / len(rq), 3),
    }

def synthesise_subtopic(section, topic, subtopic, questions, progress, figural_data=None,
                        nat_allowed=False):
    """
    BUG-A07 fix: progress added to function signature (cfg parameter removed — no config file).
    BUG-A10 fix: sub_format value ('Cloze' or 'RC') has no leading space.
    BUG-A13 fix: empty patterns from FIGURAL subtopics handled with placeholder.
    BUG-B09 fix: difficulty calibration stores is_inferred bool, not fragile string.
    BUG-B14 fix: figural subtopics with all-empty stems get placeholder pattern.
    BUG-B15 fix: §14 schema documents option_format as dict.
    """
    if not questions:
        return _absent_entry(section, topic, subtopic)

    mode     = determine_strip_mode(section, topic, subtopic)
    patterns = generate_templates(questions, mode)

    # BUG-A13 / BUG-B14 fix: handle empty patterns for figural or other edge cases
    if not patterns and questions:
        year_set = sorted(set(q.get('year') for q in questions if q.get('year')))
        patterns = [{
            'id':'P1', 'template':'(figural -- no text stem)',
            'frequency':100, 'raw_count':len(questions),
            'confidence':'observed', 'deprecated':False, 'years':year_set,
        }]

    # E-6: NOTE block analysis
    note_count  = sum(1 for q in questions if q.get('has_note'))
    notes_by_yr = {}
    for q in questions:
        if q.get('has_note') and q.get('year'):
            notes_by_yr.setdefault(q['year'], []).append(q.get('note_text',''))
    note_freq  = classify_note_frequency(note_count, len(questions))
    canon_note = canonical_note_text(notes_by_yr)

    for p in patterns:
        p['note_block'] = note_freq
        p['note_text']  = canon_note if note_freq in ('mandatory','conditional') else ''
        p['approach']   = infer_approach(p['template'], mode, subtopic)

    opt_fmt   = subtopic_option_format(questions)
    dg        = {'Simple':[],'Medium':[],'Hard':[]}
    for q in questions:
        dg[q.get('difficulty',{}).get('level','Medium')].append(q)
    # BUG-B09 fix: store is_inferred flag in calibration dict
    diff_cal  = {lv: build_diff_criteria(lv, qs, subtopic, mode) for lv, qs in dg.items()}
    wrong_opt = classify_wrong_option_structure(questions)

    neg_ct  = sum(1 for q in questions if q.get('is_negative'))
    blank_d = Counter(q.get('blank_pos','none') for q in questions).most_common(1)[0][0]
    sw      = [len(q['stem'].split()) for q in questions if q.get('stem')]
    has_img  = any(q.get('image_role','none') != 'none' for q in questions)
    has_pass = any(q.get('linked_group_id') for q in questions)
    # v2.24.6 FIX C — delegates to the SAME structural/word-boundary table detector used
    # by the canonical classify_axis1() (SHARED AXIS CLASSIFIER v1.0, below) — was a
    # locally-duplicated naive substring match (`'table' in stem.lower()`), which
    # false-positived on "vege**table**", "accep**table**", "no**table**", etc. Single
    # source of truth now; both DI derivations can never drift apart again.
    has_tbl  = any(_looks_like_table_stimulus(q.get('stem', '')) for q in questions) \
               or any(q.get('has_rendered_table') for q in questions)   # extractor tag, if present
    fmt      = ('FIGURAL' if has_img else 'PASSAGE' if has_pass else
                'DI' if has_tbl else 'TEXT')

    # v2.22 — INHERENTLY-VISUAL OVERRIDE (keyword heuristic):
    # Some subtopics are inherently visual by definition (e.g. counting figures,
    # embedded figures, mirror images). If PYQ image extraction failed (scanned
    # PDF, missing media), has_img is False and fmt becomes TEXT — a misclassification.
    # This heuristic checks the subtopic name against a universal visual-keyword set
    # and overrides to FIGURAL when a match is found AND fmt is currently TEXT.
    # Exam-agnostic — keywords cover geometric/spatial/visual terms across all exams.
    _VISUAL_KEYWORDS = re.compile(
        r'(?i)\b(figure[s]?|figural|diagram[s]?|venn|'
        r'mirror\s+image[s]?|water\s+image[s]?|paper\s*fold(ing)?|'
        r'counting\s+(figure|triangle|shape)[s]?|embedded\s+figure[s]?|'
        r'completion\s+of\s+(figure|pattern)[s]?|dice|cube\s+fold(ing)?|'
        r'pattern\s+completion|image\s+series|visual\s+reasoning)\b')
    _inherently_visual = False
    if fmt == 'TEXT' and _VISUAL_KEYWORDS.search(subtopic):
        fmt = 'FIGURAL'
        _inherently_visual = True
        # Assign a default figural_data with image_role='stem_only' (conservative:
        # most inherently-visual TEXT-classified subtopics have text options).
        # If PYQ data DID have figural info, it would have set has_img=True above,
        # so we only reach this branch when no PYQ images were observed at all.
        if not figural_data:
            figural_data = {
                'image_role': 'stem_only',
                'object_types': {'dominant': [], 'observed': [], 'avoid': []},
                'transformation_types': [],
                'arrangement_types': [],
                'complexity_dist': {},
                'images_analysed': 0,
                'images_unclear': 0,
            }
        print(f"  INHERENTLY-VISUAL override: '{subtopic}' TEXT→FIGURAL "
              f"(keyword match, image_role={figural_data.get('image_role', 'stem_only')})")
    # Allow explicit curator override via entry field (from taxonomy_draft or prior run):
    # figural_override=true forces FIGURAL; figural_override=false suppresses keyword match.
    # Checked via the 'questions' metadata: if ANY question in the PYQ set carries
    # a figural_override annotation, respect it. (Future: read from taxonomy_draft entry.)

    # BUG-A07 fix: progress now properly in scope via parameter
    q_nums  = {q['num'] for q in questions}
    lk_grps = [g for g in progress.get('_linked_groups',{}).values()
               if any(qn in q_nums for qn in g.get('q_numbers',[]))]
    lk_size = round(sum(len(g['q_numbers']) for g in lk_grps)/len(lk_grps)) \
              if lk_grps else 0

    # NEW (v2.3): max_per_paper + typical_per_paper from per-paper question counts
    paper_q_counts = Counter(q.get('paper_id', '?') for q in questions)
    pvals          = list(paper_q_counts.values())
    max_pp     = max(pvals)                           if pvals else 0
    typical_pp = round(sum(pvals) / len(pvals))       if pvals else 0

    # NEW (v2.3): recycled_datasets — stimuli appearing in >=2 different papers
    recycled = _detect_recycled_stimuli(questions)
    ctx_pool = extract_context_pool(questions, mode)
    if recycled:
        ctx_pool = ctx_pool or {}
        ctx_pool['recycled_datasets'] = recycled
        ctx_pool['ban_recycled']      = True

    # NEW (v2.5): per-subtopic MSQ aggregation → answer_cardinality (Step 7 dispatch unit).
    # Whole-subtopic mode: a subtopic is treated as uniformly single- or multi-answer.
    # A subtopic is 'multi' when a MAJORITY of its observed Qs are MSQ (>50%), so a
    # stray false-detect cannot flip a single-answer subtopic. msq_freq% is recorded
    # for transparency. Inert when multi_select_allowed=false (is_msq always False).
    msq_ct    = sum(1 for q in questions if q.get('is_msq'))
    msq_freq  = round(msq_ct / len(questions) * 100) if questions else 0
    answer_cardinality = 'multi' if msq_freq > 50 else 'single'

    # NEW (v2.8): per-subtopic NAT aggregation → answer_type (the SECOND dispatch axis).
    # A question is NAT when it has NO selectable options at all — neither text option
    # labels NOR option-images. The forgery-resistant signal is option SHAPE (zero options)
    # plus image_role: a NAT carries no option-images (image_role is 'none' for a text NAT
    # or 'stem_only' for a figural NAT — a problem diagram with a typed answer, per ND10),
    # whereas a figural MCQ carries option-images ('options_only'/'stem_and_options') and is
    # therefore NOT NAT. Gated on nat_allowed (PARAMETER 11) so the entire path is inert for
    # non-NAT exams: answer_type is always 'option' unless the exam pattern enables NAT.
    # Whole-subtopic majority (>50%) mirrors the MSQ aggregation, so a stray detect cannot
    # flip a subtopic. answer_type is ORTHOGONAL to answer_cardinality: a 'numerical'
    # subtopic's cardinality is moot (kept 'single' by convention).
    _OPT_IMG_ROLES = ('options_only', 'stem_and_options')
    nat_ct = sum(1 for q in questions
                 if len(q.get('options', [])) == 0
                 and q.get('image_role', 'none') not in _OPT_IMG_ROLES)
    nat_freq    = round(nat_ct / len(questions) * 100) if questions else 0
    answer_type = 'numerical' if (nat_allowed and nat_freq > 50) else 'option'

    # v2.23 THREE-AXIS (CATEGORY B): this subtopic's observed Axis-2 distribution + the
    # capability set Step 6/7 read. Every question is tagged by tag_axes() at extraction;
    # the guard below re-tags defensively if `questions` came from a loaded/pre-v2.23
    # progress json (idempotent — otherwise observed_axis2 would collapse to all-DIRECT).
    for q in questions:
        if 'axis2' not in q:
            tag_axes(q)
    observed_axis2 = dict(Counter(q.get('axis2', 'DIRECT') for q in questions))
    pres_family    = resolve_presentation_family_s5(subtopic, fmt)
    axis2_cap      = axis2_capability(observed_axis2.keys(), pres_family, fmt)

    return {
        'subtopic'               : subtopic,
        'section'                : section,
        'topic'                  : topic,
        'observed_count'         : len(questions),
        'format'                 : fmt,
        'option_format'          : opt_fmt,   # BUG-B15/C04: full dict, see format_entry
        'OMML_required'          : any(q.get('omml_present') for q in questions),
        'negative_question_freq' : round(neg_ct / len(questions) * 100),
        'answer_type'            : answer_type,   # v2.8: 'option'|'numerical' (NAT axis)
        'nat_freq'               : nat_freq,      # v2.8: % of observed Qs that are NAT
        'answer_cardinality'            : answer_cardinality,   # v2.5: 'single'|'multi' (Step 7 dispatch)
        'msq_freq'               : msq_freq,      # v2.5: % of observed Qs that are MSQ
        'observed_axis2'         : observed_axis2, # v2.23: {AXIS2_CLASS: count} this subtopic
        'presentation_family'    : pres_family,    # v2.23: family key (Step 7 menu source)
        'axis2_capability'       : axis2_cap,      # v2.23: forms this subtopic may faithfully take
        'fill_in_blank'          : blank_d,
        'linked_group_size'      : lk_size,
        'max_per_paper'          : max_pp,
        'typical_per_paper'      : typical_pp,
        'stem_word_count'        : {'min':(min(sw) if sw else 0),
                                     'max':(max(sw) if sw else 0),
                                     'typical':round(sum(sw)/len(sw)) if sw else 0},
        'sub_type_label'         : subtopic,
        'PYQ_STEM_PATTERNS'      : patterns,
        'PYQ_DIFFICULTY_CALIBRATION': diff_cal,
        'wrong_option_structure' : wrong_opt,
        'PYQ_NUMBER_RANGES'      : extract_number_ranges(questions, mode),
        'PYQ_CONTEXT_POOL'       : ctx_pool,
        'PYQ_IMAGE_ANALYSIS'     : figural_data,
        'PYQ_PASSAGE_STRUCTURE'  : extract_passage_structure(questions) if has_pass else None,
        'inherently_visual'      : _inherently_visual,   # v2.22: True if keyword heuristic fired
    }

def _detect_recycled_stimuli(questions):
    """
    NEW (v2.3): Detect linked-group stimuli that appear in >=2 different PYQ papers.
    When the same passage/puzzle/table appears across multiple papers it is a recycled
    dataset — Step 7 must not reproduce it verbatim.
    Returns list of short identifying descriptors (first 12 words of stimulus).
    Called from synthesise_subtopic; result written to PYQ_CONTEXT_POOL.
    """
    stim_papers = {}  # normalised_key → set of paper_ids
    for q in questions:
        if not q.get('linked_group_id'):
            continue
        words = q.get('stem', '').split()
        key   = ' '.join(words[:12]).lower().strip()
        if len(key) < 20:
            continue   # too short to be a meaningful stimulus identifier
        pid = q.get('paper_id', '?')
        stim_papers.setdefault(key, set()).add(pid)
    # Return descriptors for stimuli seen in 2+ distinct papers
    return [key[:80] for key, pids in stim_papers.items() if len(pids) >= 2]


def _absent_entry(section, topic, subtopic):
    _fam = resolve_presentation_family_s5(subtopic, 'TEXT')   # v2.23
    return {
        'subtopic':subtopic,'section':section,'topic':topic,'observed_count':0,
        'format':'TEXT',
        'option_format':{'primary':'single_value','recent_format':'single_value',
                         'changed_recently':False,'all_observed':[]},
        'OMML_required':False,'negative_question_freq':0,'fill_in_blank':'none',
        'answer_type':'option','nat_freq':0,           # v2.8: no PYQ → assume option-type
        'answer_cardinality':'single','msq_freq':0,   # v2.5: no PYQ → assume single-answer
        'linked_group_size':0,'max_per_paper':0,'typical_per_paper':0,
        'stem_word_count':{'min':0,'max':0,'typical':0},
        'sub_type_label':subtopic,
        'concept_group': None,        # v2.24.1 (D8): stamped later by stamp_mechanic_axes()
        'question_mechanic': None,    # v2.24.1 (D8)
        'form_key': None,             # v2.24.1 (D8)
        'collision_domain': None,     # v2.24.1 (D8)
        'PYQ_STEM_PATTERNS':[{'id':'P1','template':'(no PYQ observed)','approach':'(unknown)',
                               'frequency':100,'raw_count':0,'confidence':'absent',
                               'deprecated':False,'years':[],'note_block':'never','note_text':''}],
        'PYQ_DIFFICULTY_CALIBRATION':{
            'Simple':{'criteria':'(inferred)','is_inferred':True},
            'Medium':{'criteria':'(inferred)','is_inferred':True},
            'Hard':  {'criteria':'(inferred)','is_inferred':True}},
        'wrong_option_structure':{'type':'varied','description':'No PYQ data'},
        'PYQ_NUMBER_RANGES':None,'PYQ_CONTEXT_POOL':None,
        'PYQ_IMAGE_ANALYSIS':None,'PYQ_PASSAGE_STRUCTURE':None,
        'inherently_visual':False,   # v2.22: no PYQ → cannot determine; default False
        # v2.23: no PYQ → no observed Axis-2; capability = family menu ∪ {DIRECT} so a
        # Zero-PYQ subtopic is still a usable format-elastic filler for Step 7 (decision 11).
        'observed_axis2':{}, 'presentation_family':_fam,
        'axis2_capability':axis2_capability([], _fam, 'TEXT'),
    }

def build_diff_criteria(level, qs, subtopic, mode):
    """BUG-B09 fix: returns dict with is_inferred bool, not fragile string."""
    if not qs:
        return {'criteria':f'(inferred -- no {level} Qs observed in PYQ)',
                'is_inferred':True}
    sc   = [q.get('difficulty',{}) for q in qs[:3]]
    avgC = round(sum(s.get('C',1) for s in sc)/len(sc), 1)
    avgV = round(sum(s.get('V',1) for s in sc)/len(sc), 1)
    ex   = qs[0]['stem'][:80] if qs[0].get('stem') else '(no example)'
    return {'criteria': f'C~{avgC} steps, V~{avgV} complexity. Example: "{ex}..."',
            'is_inferred': False}

def infer_approach(template, mode, subtopic):
    t = template.lower(); u = subtopic.lower()
    if mode == 'quantitative':
        if 'interest' in u or '_p_' in t: return 'Apply SI/CI formula'
        if 'profit' in u:                  return 'Apply profit/loss formula'
        if 'speed' in t or 'distance' in t:return 'Apply speed-distance-time formula'
        return 'Solve using relevant arithmetic formula'
    elif mode == 'reasoning':
        if 'coded as' in t or 'written as' in t: return 'Decode substitution pattern'
        if 'related to' in t: return 'Find operation A->B, apply same to C'
        return 'Apply logical reasoning pattern'
    elif mode == 'factual':
        if 'who' in t:    return 'Identify person from contextual clues'
        if '_year_' in t: return 'Recall year of event'
        return 'Recall factual information'
    elif mode == 'english':
        if 'synonym' in u: return 'Select semantically equivalent word'
        if 'antonym' in u: return 'Select semantically opposite word'
        return 'Apply English language rule'
    elif mode == 'logical':
        return 'Evaluate statement-conclusion pairs using syllogism rules'
    return 'Apply appropriate strategy'

def extract_number_ranges(questions, mode):
    if mode != 'quantitative': return None
    # BUG-A14 fix: non-raw string so \u20b9 is actual ₹ character
    VAR_PATS = [
        ('P',   '\u20b9\\s*([\\d,]+)'),
        ('R',   r'(\d+(?:\.\d+)?)%'),
        ('T',   r'(\d+)\s*(?:years?|months?)'),
        ('NUM', r'\b(\d+)\b'),
    ]
    var_vals = {}
    for q in questions:
        for var, pat in VAR_PATS:
            for m in re.finditer(pat, q.get('stem',''), re.IGNORECASE):
                try: var_vals.setdefault(var,[]).append(int(m.group(1).replace(',','')))
                except: pass
    if not var_vals: return None
    from math import gcd
    from functools import reduce
    result = {}
    for var, vals in var_vals.items():
        gcf = reduce(gcd, vals[:10]) if len(vals) >= 2 else vals[0]
        result[var] = {'min':min(vals),'max':max(vals),'multiples_of':gcf,
                       'notes':f'n={len(vals)} observed'}
    return result

def extract_context_pool(questions, mode):
    if mode != 'quantitative': return None
    CTXS = [
        (r'\bborrow|lend|loan\b','loan'),
        (r'\bbank|deposit|savings\b','bank_deposit'),
        (r'\bshop|sell|buy|profit\b','retail_trade'),
        (r'\btrain|speed|distance\b','speed_distance'),
        (r'\bpipe|cistern|tank\b','pipes_cisterns'),
        (r'\bwork|days|complete\b','work_time'),
        (r'\bscheme|invest\b','investment'),
    ]
    counts = Counter()
    for q in questions:
        for pat, label in CTXS:
            if re.search(pat, q.get('stem',''), re.IGNORECASE): counts[label] += 1
    if not counts: return None
    tot = len(questions)
    return {'dominant':[c for c,n in counts.items() if n/tot>0.20],
            'common'  :[c for c,n in counts.items() if 0.05<=n/tot<=0.20],
            'rare'    :[c for c,n in counts.items() if 0<n/tot<0.05],
            'avoid'   :[]}

def extract_passage_structure(questions):
    """
    BUG-A10 fix: 'Cloze' without leading space.
    BUG-C05/v2.3: paragraph_count estimated from avg word count;
                  topic_domains populated from content keyword matching.
    """
    linked = [q for q in questions if q.get('linked_group_id')]
    if not linked: return None
    words  = [len(q.get('stem','').split()) for q in linked]
    qtypes = Counter()
    for q in linked:
        s = q.get('stem','').lower()
        if any(kw in s for kw in ['suggest','imply','infer','conclude']): qtypes['inference'] += 1
        elif any(kw in s for kw in ['according','states','passage']):      qtypes['direct']    += 1
        elif any(kw in s for kw in ['meaning','synonym','vocabulary']):    qtypes['vocab']     += 1
        elif any(kw in s for kw in ['blank','fill','appropriate']):        qtypes['grammar']   += 1
        else:                                                                qtypes['direct']    += 1
    tot  = sum(qtypes.values()) or 1
    dist = {k:round(v/tot*100) for k,v in qtypes.items()}
    has_cloze = any('blank' in q.get('stem','').lower() for q in linked)

    # Estimate paragraph_count from average stimulus word count
    # (typical prose: ~80 words/paragraph; Cloze: 1-2 paragraphs)
    avg_words = round(sum(words) / len(words)) if words else 0
    est_paras = max(1, round(avg_words / 80)) if not has_cloze else max(1, round(avg_words / 120))

    # Detect topic domains from stimulus content (exam-agnostic keyword matching)
    # These are the most common passage domain categories across competitive exams.
    DOMAIN_MAP = [
        (['science','technology','research','experiment','discovery','innovation'],'science_technology'),
        (['social','society','community','culture','tradition','diversity'],'social_issues'),
        (['environment','ecology','climate','biodiversity','conservation','pollution'],'environment'),
        (['economy','economic','finance','trade','market','gdp','inflation'],'economy'),
        (['history','ancient','medieval','civilization','empire','dynasty'],'history'),
        (['health','medicine','disease','body','nutrition','mental','therapy'],'health_medicine'),
        (['education','school','learning','student','knowledge','pedagogy'],'education'),
        (['philosophy','ethics','morality','consciousness','value','virtue'],'philosophy'),
        (['governance','policy','government','law','constitution','democracy'],'governance'),
        (['sport','game','athletic','champion','competition','tournament'],'sports'),
        (['literature','poetry','novel','author','narrative','character'],'literature'),
        (['art','music','painting','sculpture','aesthetic','creative'],'arts'),
    ]
    all_stems = ' '.join(q.get('stem','').lower() for q in linked[:5])
    observed_domains = [label for keywords, label in DOMAIN_MAP
                        if any(kw in all_stems for kw in keywords)]

    return {'sub_format'         : 'Cloze' if has_cloze else 'RC',
            'word_range'         : {'min':(min(words) if words else 0),'max':(max(words) if words else 0)},
            'paragraph_count'    : {'typical': est_paras},
            'topic_domains'      : {'observed': observed_domains, 'avoid': []},
            'q_type_distribution': dist}
```

### S5-3 — Write section_rules.md

```python
def _compute_structural_changes(entries):
    """
    NEW (v2.3): Compute observable year-over-year structural changes from PYQ data.
    Returns list of strings for STRUCTURAL_CHANGES_BY_YEAR block.
    All conclusions are DATA-DRIVEN — zero hardcoding.
    Detects: subtopics removed in recent years, new subtopics, DI format shifts,
             FIGURAL elimination, format type changes.
    Called by write_section_rules.
    """
    changes = []

    # Collect global year range from all pattern years lists
    all_years = sorted(set(
        y for e in entries
        for p in e.get('PYQ_STEM_PATTERNS', [])
        for y in p.get('years', [])
        if isinstance(y, int)
    ), reverse=True)

    if not all_years:
        return changes   # no year data — cannot compute changes

    max_year = all_years[0]

    for e in entries:
        subtopic = e['subtopic']
        years_seen = sorted(set(
            y for p in e.get('PYQ_STEM_PATTERNS', [])
            for y in p.get('years', []) if isinstance(y, int)
        ))
        if not years_seen:
            continue

        last_seen = max(years_seen)
        first_seen = min(years_seen)

        # Subtopic absent from most recent year and last seen 2+ years ago → REMOVED
        if last_seen < max_year - 1:
            changes.append(
                f'  {subtopic} (format={e["format"]}): '
                f'last seen {last_seen} — likely REMOVED after {last_seen}'
            )

        # Subtopic appears only in last 1-2 years → NEW
        elif first_seen >= max_year - 1 and len(years_seen) <= 2:
            changes.append(
                f'  {subtopic} (format={e["format"]}): '
                f'first seen {first_seen} — NEW subtopic'
            )

        # v2.15 BUG-D10 fix: only emit FIGURAL-eliminated if not already flagged as REMOVED
        # (a REMOVED FIGURAL subtopic would otherwise produce two entries).
        if (e.get('format') == 'FIGURAL' and e.get('observed_count', 0) == 0
                and not (last_seen < max_year - 1)):
            changes.append(
                f'  {subtopic} (FIGURAL): observed_count=0 '
                f'— FIGURAL format appears eliminated for this subtopic'
            )

        # DI: single-Q format (linked_group_size <= 1) — may indicate format shift
        if e.get('format') == 'DI' and e.get('linked_group_size', 0) <= 1 and e.get('observed_count', 0) > 0:
            changes.append(
                f'  {subtopic} (DI): linked_group_size={e["linked_group_size"]} '
                f'— single-Q DI format observed (previously multi-Q)'
            )

    return changes


# ══════════════════════════════════════════════════════════════════════════════
# v2.24.1 MECHANIC / FORM-KEY ENGINE  (permanent, EXAM-INDEPENDENT fix for the
#                                      BV-10a form_key-collision HALT class)
# ------------------------------------------------------------------------------
# THREE AXES, THREE GRANULARITIES. They are NOT the same variable.
#   family / concept_group  — COARSE. May be shared. Feeds BV-10b (SOFT cap).
#   question_mechanic       — SEMANTIC FORM. May be shared. Feeds Step 7 CHECK D.
#   form_key                — IDENTITY. MUST be unique per collision_domain.
#                             Feeds BV-10a (HARD cap = 1, not configurable).
#
# v2.24 collapsed all three onto `family` whenever no qualifier was found — which,
# because _QUALIFIERS is a reasoning-domain vocabulary, is ALWAYS the case on a
# subject-knowledge exam. Any two subtopics sharing a _FAMILY_MAP keyword then got
# an IDENTICAL form_key, and Step 6 BV-10a HALTed two steps later. This is not
# exam-specific: it is latent in EVERY single-section subject exam. See the
# v2.24.1 defect report (D1..D9).
#
# v2.24.1 relocates the uniqueness guarantee from an ACCIDENT (a reasoning
# qualifier happening to match the name) to a CONSTRUCTION: form_key derives from
# the subtopic's own identity base, which bottoms out at the unique subtopic_id.
# It scopes the keyword table by a per-exam `template_sets` declaration, derives +
# stamps every axis exactly ONCE after id minting, and asserts form_key uniqueness
# BEFORE any artifact is written. The failure mode (defective manifest promoted,
# HALT two steps later) is therefore impossible for any exam: the worst case is a
# LOUD Step-5 FAIL naming the offending ids, never a silent downstream HALT.
#
# EXAM-INDEPENDENCE: the engine is identical for every exam. The ONLY per-exam
# input is [ExamCode]_mechanic_overrides.json. Absent file ⇒ legacy family
# selection (REGR-1) PLUS the SPEC-1 uniqueness improvement, which is always on.

def canon_text(s):
    """NFC + casefold + hyphen/slash/ampersand->space + collapse whitespace. Never raises."""
    import re, unicodedata
    s = unicodedata.normalize('NFC', (s or ''))
    for ch in ('—','–','-','/','&'):
        s = s.replace(ch, ' ')
    s = s.casefold().strip()
    return re.sub(r'\s+', ' ', s)

def _has_word(text, kw):
    """Word-boundary containment; allows only simple plural (s/es), never arbitrary
    continuation. 'voice' does NOT match 'invoice'; 'clock' does NOT match 'clockwise';
    but 'antonym' DOES match 'antonyms'. EC-M12: plural suffix applies to the FINAL
    token of a multi-word keyword too."""
    import re
    if ' ' in kw:
        head, _, tail = kw.rpartition(' ')
        pat = r'(?<!\w)' + re.escape(head) + r'\s+' + re.escape(tail) + r'(?:e?s)?(?!\w)'
        return re.search(pat, text) is not None
    return re.search(r'\b'+re.escape(kw)+r'(?:e?s)?\b', text) is not None

# Minimal, extensible transliteration for common Hindi verbal/reasoning terms so a
# pure-Devanagari name never collapses to '' for the FAMILY axis (never for form_key).
_HI_MAP = {
    'पर्यायवाची':'synonym',
    'विलोम':'antonym',
    'मुहावरे':'idiom','मुहावरा':'idiom',
    'श्रृंखला':'series','शृंखला':'series',
    'सादृश्य':'analogy','वर्गीकरण':'classification',
    'कोडिंग':'coding_decoding','दिशा':'direction_sense',
    'वर्तनी':'spelling',
}
def _translit_hint(raw):
    for k,v in _HI_MAP.items():
        if k in (raw or ''):
            return v
    return None

_VERBAL_SECTION_HINTS = ('english','verbal','language','comprehension','hindi',
                         'हिंदी','भाषा')
def _is_verbal(section, fmt):
    """v2.24.1: DEMOTED. It may only NARROW a declared template set (advisory), never
    WIDEN one. Its old ability to enable the verbal table for any TEXT exam (the D2
    defect) is gone — the verbal table now fires only when the exam DECLARES 'verbal'
    in template_sets AND this returns True."""
    sec = canon_text(section)
    if any(h in sec for h in _VERBAL_SECTION_HINTS):
        return True
    return (fmt or 'TEXT').upper() in ('TEXT','PASSAGE')

# ── Per-exam overrides loader (SPEC-2 / SPEC-6; EC-M17 exam_code, EC-M18 malformed) ──
_OVERRIDES = None
_MERGE_LOG = []          # populated by apply_subtopic_merges(); read by write_analysis_summary()

def load_mechanic_overrides(exam_code):
    """Discovery: /mnt/project/, then /mnt/user-data/uploads/.
    Absent               → all defaults (legacy family selection; SPEC-1 still applies).
    Present + malformed  → FAIL (EC-M18).  exam_code mismatch → FAIL (EC-M17)."""
    global _OVERRIDES
    if _OVERRIDES is not None:
        return _OVERRIDES
    _OVERRIDES = {'template_sets': None, 'template_sets_by_section': {},
                  'subtopic_overrides': {}, 'subtopic_merges': []}
    for d in ('/mnt/project/', '/mnt/user-data/uploads/'):
        path = os.path.join(d, f'{exam_code}_mechanic_overrides.json')
        if not os.path.exists(path):
            continue
        try:
            with io_open_utf8(path) as fh:
                data = json.load(fh)
        except json.JSONDecodeError as ex:
            raise SystemExit(f'FAIL: {path} is not valid JSON — {ex}')                 # EC-M18
        if data.get('exam_code') != exam_code:                                          # EC-M17
            raise SystemExit(f"FAIL: {path} declares exam_code={data.get('exam_code')!r}, "
                             f"expected {exam_code!r}")
        _valid = {'verbal','reasoning'}
        bad = set(data.get('template_sets') or []) - _valid                             # OV-5
        if bad:
            raise SystemExit(f"FAIL: {path} template_sets has unknown values {sorted(bad)}")
        for _sec, _sets in (data.get('template_sets_by_section') or {}).items():         # OV-5b
            _badsec = set(_sets or []) - _valid
            if _badsec:
                raise SystemExit(f"FAIL: {path} template_sets_by_section[{_sec!r}] has "
                                 f"unknown values {sorted(_badsec)} (check case/whitespace)")
        _OVERRIDES.update(data)
        break
    return _OVERRIDES

def io_open_utf8(path):
    import io as _io
    return _io.open(path, encoding='utf-8')

# ── The keyword table. Rows are 3-tuples now: (keywords, family, template_set). ──
#    Every former verbal_only=True row is 'verbal'; every former False row is
#    'reasoning'. A row fires only if its template_set is declared for the exam.
_FAMILY_MAP = [
    (['synonym','similar in meaning','nearest in meaning'], 'synonym', 'verbal'),
    (['antonym','opposite in meaning','opposite meaning'],  'antonym', 'verbal'),
    (['one word substitution','one word substitute'],       'one_word_substitution', 'verbal'),
    (['idiom','phrasal verb'],                              'idiom', 'verbal'),
    (['cloze'],                                             'cloze_test', 'verbal'),
    (['fill in the blank','fill in the blanks','sentence completion'], 'fill_in_blank', 'verbal'),
    (['spelling','correctly spelt','misspelt'],             'spelling', 'verbal'),
    (['grammatical error','error detection','spotting error','find the error'], 'error_detection', 'verbal'),
    (['sentence improvement','sentence correction','best improves'], 'sentence_improvement', 'verbal'),
    (['voice','active voice','passive voice'],              'voice', 'verbal'),
    (['narration','direct speech','indirect speech','reported speech'], 'narration', 'verbal'),
    (['para jumble','sentence rearrangement','sentence order'], 'para_jumble', 'verbal'),
    (['reading comprehension'],                            'reading_comprehension', 'verbal'),
    (['series'],                                           'series', 'reasoning'),
    (['analogy'],                                          'analogy', 'reasoning'),
    (['classification','odd one out','odd pair','does not belong'], 'classification', 'reasoning'),
    (['coding','decoding'],                                'coding_decoding', 'reasoning'),
    (['blood relation','family relation'],                 'blood_relation', 'reasoning'),
    (['direction'],                                        'direction_sense', 'reasoning'),
    (['seating','arrangement','puzzle'],                   'arrangement', 'reasoning'),
    (['syllogism','statement conclusion','statement assumption','course of action','logical deduction'], 'syllogism', 'reasoning'),
    (['mirror image'],                                     'mirror_image', 'reasoning'),
    (['water image'],                                      'water_image', 'reasoning'),
    (['paper folding','paper cutting'],                    'paper_folding', 'reasoning'),
    (['embedded figure','hidden figure'],                  'embedded_figure', 'reasoning'),
    (['venn diagram'],                                     'venn_diagram', 'reasoning'),
    (['dice','cube'],                                      'dice', 'reasoning'),
    (['missing number','number matrix','number grid'],     'missing_number', 'reasoning'),
    (['calendar'],                                         'calendar', 'reasoning'),
    (['clock'],                                            'clock', 'reasoning'),
    (['data interpretation','bar graph','pie chart','line graph','tabulation'], 'data_interpretation', 'reasoning'),
    (['current affairs'],                                  'current_affairs', 'reasoning'),
    (['static gk','static general knowledge'],             'static_gk', 'reasoning'),
]
_QUALIFIERS = ['alphanumeric','symbolic','semantic','number','numeric','numerical',
               'letter','alphabet','word','figural','figure','spatial',
               'linear','circular','floor','matrix','wheel','triangle','substitution']
_QUALIFIABLE = {'series','analogy','classification','coding_decoding','missing_number',
                'arrangement','mirror_image','paper_folding','embedded_figure'}
_ALL_FAMILY_NAMES = {fam for _, fam, _ in _FAMILY_MAP}
_TEMPLATE_SET     = {fam: ts for _, fam, ts in _FAMILY_MAP}

def _identity_base(display_name, subtopic_id):
    """SPEC-1 / EC-M2. The collision-safe identity root. ONE recipe, ONE call site.
    A fully non-Latin name slugifies to '' and must still yield a stable, unique,
    call-site-independent value. Ultimately bottoms out at the unique subtopic_id."""
    import hashlib as _hl
    return (slugify(display_name)
            or slugify(subtopic_id)
            or ('u_' + _hl.md5((display_name or '').encode('utf-8')).hexdigest()[:8]))

def _redundant(qual, base):
    """EC-M13: word-boundary test, not substring. 'number' is redundant against base
    'missing_number' only if it appears there as a whole token."""
    return _has_word(base.replace('_', ' '), qual)

def _extract_qualifiers(name_c):
    """EC-M14: ALL matching qualifiers, canonical (alphabetical) order — order-independent."""
    import re
    return tuple(sorted(re.sub(r'\s+', '_', q) for q in _QUALIFIERS if _has_word(name_c, q)))

def _allowed_template_sets(section, ov):
    allowed = ov.get('template_sets_by_section', {}).get(section, ov.get('template_sets'))
    if allowed is None:
        allowed = ['verbal', 'reasoning']            # ABSENT ⇒ legacy behaviour (REGR-1)
    return allowed

def derive_mechanic(section, subtopic, sub_type_label=None, templates='',
                    fmt='TEXT', subtopic_id=None, prefix_overrides=None):
    """Returns {family, mechanic, form_key, collision_domain}.
    PRECONDITION: subtopic_id is the FINAL, de-duplicated, minted id (EC-M3)."""
    import re
    ov       = _OVERRIDES or {}
    raw_name = subtopic or sub_type_label or ''
    name_c   = canon_text(raw_name + ' ' + (sub_type_label or ''))
    base     = _identity_base(raw_name, subtopic_id)
    domain   = section_prefix(section, prefix_overrides) or 'default'    # SPEC-3 / EC-M4
    allowed  = _allowed_template_sets(section, ov)                       # SPEC-2 / EC-M6

    def _match(hay):
        for kws, fam, tset in _FAMILY_MAP:
            if tset not in allowed:                                 continue
            if tset == 'verbal' and not _is_verbal(section, fmt):   continue   # advisory NARROW only
            if any(_has_word(hay, kw) for kw in kws):
                return fam
        return None

    # COARSE axis. NAME is authoritative. Templates rescue ONLY a name with no
    # alphanumeric content at all (never merely "a name that matched nothing").
    family = _match(name_c) if name_c.strip() else None
    if family is None and not re.search(r'[a-z0-9]', name_c):
        family = _match(canon_text(templates))
    if family is None:
        family = _translit_hint(raw_name)                           # EC-M2: family ONLY
    if family is None:
        family = base                                               # coarse identity == the name

    # FINE axis. SPEC-1: starts from the NAME/id base, NEVER from the family token.
    quals    = _extract_qualifiers(name_c) if family in _QUALIFIABLE else ()
    suffix   = '__'.join(q for q in quals if not _redundant(q, base))   # EC-M13 / EC-M14
    form_key = f'{base}__{suffix}' if suffix else base

    # Explicit curator override wins over everything (applied per subtopic_id).
    per      = ov.get('subtopic_overrides', {}).get(subtopic_id or '', {})
    family   = per.get('concept_group',     family)
    form_key = per.get('form_key',          form_key)
    mechanic = per.get('question_mechanic', form_key)               # v2.24.1: mechanic == form_key

    return {'family': family, 'mechanic': mechanic,
            'form_key': form_key, 'collision_domain': domain}

def mint_subtopic_ids(entries, exam_meta=None):
    """v2.24.1: mint the canonical, collision-safe subtopic_id for every entry, IDEMPOTENTLY
    (an entry that already carries an id is left untouched). Called from run_synthesise()
    BEFORE merges/stamp/QV so the gate and every writer read the SAME id. write_section_rules()
    also calls it as a no-op guard."""
    pov  = (exam_meta or {}).get('section_prefix_overrides', {})
    pmap = build_section_prefix_map(sorted({e['section'] for e in entries}), pov)
    seen = {}
    for e in entries:
        if e.get('subtopic_id'):
            seen[e['subtopic_id']] = (e['section'], e['topic'], e['subtopic'])
    for e in entries:
        if e.get('subtopic_id'):
            continue
        sid = make_subtopic_id(e['section'], e['topic'], e['subtopic'], pmap)
        base = sid; n = 2
        key = (e['section'], e['topic'], e['subtopic'])
        while sid in seen and seen[sid] != key:
            sid = f'{base}_{n}'; n += 1
        seen[sid] = key
        e['subtopic_id'] = sid
    return entries

def apply_subtopic_merges(entries, exam_code):
    """D7 / SPEC-7. TRUE-duplicate merge (NOT an allowlist). Each group of >=2 subtopic_ids
    is collapsed into the FIRST member; the others are dropped. Members must share a section
    (OV-3). Runs AFTER id minting, BEFORE stamp/QV. Records every drop in _MERGE_LOG so
    write_analysis_summary() can emit the mandatory '## MERGED SUBTOPICS' section (a merge
    removes a subtopic_id that Steps 6/7 join on — the curator must see what disappeared)."""
    global _MERGE_LOG
    _MERGE_LOG = []
    ov = load_mechanic_overrides(exam_code)
    groups = ov.get('subtopic_merges', []) or []
    if not groups:
        return entries
    by_id = {e.get('subtopic_id'): e for e in entries}
    drop  = set()
    _across = {}                                                                     # id -> group index
    for _gi, _grp in enumerate(groups):                                              # OV-4b: groups disjoint
        for _g in _grp:
            if _g in _across:
                raise SystemExit(f"FAIL: subtopic_merges: {_g!r} appears in two groups "
                                 f"({groups[_across[_g]]} and {_grp}); groups must be disjoint")
            _across[_g] = _gi
    for grp in groups:
        if len(grp) < 2:                                                             # OV-4
            raise SystemExit(f"FAIL: subtopic_merges group {grp} has <2 members")
        missing = [g for g in grp if g not in by_id]
        if missing:                                                                  # OV-3
            raise SystemExit(f"FAIL: subtopic_merges references unknown subtopic_id(s) {missing}")
        secs = {by_id[g]['section'] for g in grp}
        if len(secs) > 1:                                                            # OV-3
            raise SystemExit(f"FAIL: subtopic_merges group {grp} spans sections {sorted(secs)}")
        survivor = by_id[grp[0]]
        members  = [by_id[g] for g in grp]
        survivor['observed_count'] = sum(m.get('observed_count', 0) for m in members)
        survivor['max_per_paper']  = max(m.get('max_per_paper', 0) for m in members)
        tpp = [m.get('typical_per_paper', 0) for m in members]
        survivor['typical_per_paper'] = round(sum(tpp) / len(tpp)) if tpp else 0
        for g in grp[1:]:
            drop.add(g)
            _MERGE_LOG.append((g, grp[0]))
    kept = [e for e in entries if e.get('subtopic_id') not in drop]
    for g, keep in _MERGE_LOG:
        print(f"  MERGE: {g} → {keep} (observed_count summed)")
    return kept

def stamp_mechanic_axes(entries, exam_code, exam_meta=None):
    """SPEC-5 / D8. Derive ONCE, stamp, then assert. Called from run_synthesise() AFTER
    taxonomy sync, AFTER merges, AFTER subtopic_id minting — and BEFORE run_qv() and any
    writer. Every downstream consumer reads the stamped field; NONE recompute."""
    import difflib
    ov = load_mechanic_overrides(exam_code)
    pov = (exam_meta or {}).get('section_prefix_overrides', {})
    po  = build_section_prefix_map(sorted({e['section'] for e in entries}), pov)

    # PRECONDITION (§8-4): every entry must already carry a minted subtopic_id. mint runs
    # before stamp in run_synthesise; guard here so a misordered caller fails clearly, not
    # with a bare KeyError.
    _noid = [i for i, e in enumerate(entries) if not e.get('subtopic_id')]
    if _noid:
        raise SystemExit(f"stamp_mechanic_axes precondition violated: {len(_noid)} entr(y/ies) "
                         f"have no subtopic_id — mint_subtopic_ids() must run first.")

    known   = {e['subtopic_id'] for e in entries}
    unknown = set(ov.get('subtopic_overrides', {})) - known                          # OV-1 / EC-M7
    if unknown:
        for u in sorted(unknown):
            near = difflib.get_close_matches(u, list(known), n=3)
            print(f'  FAIL: override key {u!r} matches no subtopic_id. Did you mean: {near}')
        raise SystemExit(f'OV-1: {len(unknown)} override key(s) match no subtopic_id')
    for sec in ov.get('template_sets_by_section', {}):                               # OV-6
        if sec not in {e['section'] for e in entries}:
            raise SystemExit(f"OV-6: template_sets_by_section names unknown section {sec!r}")

    _ovsub = ov.get('subtopic_overrides', {})
    _forced_fk = set()          # ids whose form_key was set by an EXPLICIT curator override
    for e in entries:
        templates = ' '.join(p.get('template', '') for p in e.get('PYQ_STEM_PATTERNS', []))
        ax = derive_mechanic(e['section'], e.get('subtopic') or e.get('sub_type_label',''),
                             e.get('sub_type_label'), templates,
                             e.get('format', 'TEXT'), e['subtopic_id'], po)
        e['concept_group']     = ax['family']
        e['question_mechanic'] = ax['mechanic']
        e['form_key']          = ax['form_key']
        e['collision_domain']  = ax['collision_domain']
        if 'form_key' in _ovsub.get(e['subtopic_id'], {}):
            _forced_fk.add(e['subtopic_id'])

    # EC-M1: two subtopics whose DISPLAY_NAME yields the SAME derived base in one
    # collision_domain both fall back to slugify(subtopic_id) — deterministic, unique.
    # This applies ONLY to derived collisions. A collision in which ANY member carries an
    # EXPLICIT override form_key is NOT auto-resolved: that is an OV-2 curator error and
    # must FAIL loudly below (silently rewriting a curator's declared value would hide a
    # real mistake). See EC-M8.
    import hashlib as _hl
    claims = {}
    for e in entries:
        claims.setdefault((e['collision_domain'], e['form_key']), []).append(e)
    for (_dom, _fk), grp in claims.items():
        if len({e['subtopic_id'] for e in grp}) > 1 and not any(e['subtopic_id'] in _forced_fk for e in grp):
            for e in grp:
                e['form_key'] = slugify(e['subtopic_id'])
    # Residual guard: subtopic_ids are unique, but slugify() maps '.' and '_' alike, so two
    # DISTINCT ids can slugify to the same string (e.g. 'p.a_b.c' and 'p.a.b_c'). Any residual
    # (domain, form_key) collision among AUTO-RESOLVED entries (no forced override) is broken
    # deterministically with a short id-hash suffix, so genuinely-distinct subtopics never
    # provoke a false HALT. Override-induced collisions are left for the invariant to reject.
    _res = {}
    for e in entries:
        _res.setdefault((e['collision_domain'], e['form_key']), []).append(e)
    for (_dom, _fk), grp in _res.items():
        if len({e['subtopic_id'] for e in grp}) > 1 and not any(e['subtopic_id'] in _forced_fk for e in grp):
            for e in grp:
                _h = _hl.md5(e['subtopic_id'].encode('utf-8')).hexdigest()[:6]
                e['form_key'] = f"{e['form_key']}_{_h}"

    # OV-2 / D7 / EC-M8 / EC-M15: uniqueness is an INVARIANT, asserted before any write.
    seen, violations = {}, []
    for e in entries:
        k = (e['collision_domain'], e['form_key'])
        if not e['form_key']:
            violations.append(f"{e['subtopic_id']}: empty form_key")
        if e['form_key'] == e['collision_domain']:
            violations.append(f"{e['subtopic_id']}: form_key equals collision_domain")
        if k in seen and seen[k] != e['subtopic_id']:
            violations.append(f"{k[0]}:{k[1]} shared by {seen[k]} and {e['subtopic_id']}")
        seen[k] = e['subtopic_id']
    if violations:
        raise SystemExit(
            'form_key uniqueness invariant violated. A manifest with a shared form_key is a '
            'latent Step 6 BV-10a HALT whose triggering depends on N_mocks and batch_size, '
            'which Step 5 cannot know. Merge the subtopics via subtopic_merges, or give them '
            'distinct form_keys via subtopic_overrides.\n  ' + '\n  '.join(violations))
    print(f'  form_key invariant: PASS — {len(entries)} entries, '
          f'{len(seen)} distinct (collision_domain, form_key) pairs')
    return entries

# ── Back-compat wrappers. They read the STAMPED field first and only fall back to a
#    fresh derivation for a legacy caller that never ran stamp_mechanic_axes(). After
#    the v2.24.1 run_synthesise() path they always return the stamped value. ──
def _derive_axes(entry):
    templates = ' '.join(p.get('template','') for p in entry.get('PYQ_STEM_PATTERNS', []))
    return derive_mechanic(entry.get('section',''),
                           entry.get('subtopic') or entry.get('sub_type_label',''),
                           entry.get('sub_type_label'), templates,
                           entry.get('format','TEXT'), entry.get('subtopic_id'))

def _derive_concept_group(entry):
    return entry.get('concept_group') or _derive_axes(entry)['family']

def _derive_question_mechanic(entry):
    return entry.get('question_mechanic') or _derive_axes(entry)['mechanic']

def _derive_form_key(entry):
    return entry.get('form_key') or _derive_axes(entry)['form_key']

def _derive_collision_domain(entry):
    return entry.get('collision_domain') or _derive_axes(entry)['collision_domain']


def write_section_rules(entries, exam_code, exam_meta=None, progress=None):
    """
    BUG-A25 fix: output to /mnt/user-data/outputs/ for present_files access.
    v2.3 NEW: writes EXAM_STRUCTURE header block (CATEGORY C) when exam_meta provided.
    v2.3 NEW: writes STRUCTURAL_CHANGES_BY_YEAR block computed from PYQ data.
    v2.3 NEW: writes figural_banned flag per section header.
    v2.15 BUG-D03: accepts progress dict for per-section option_label_format aggregation.

    exam_meta: dict built by run_synthesise from progress['_meta'].
      Keys: time_per_q_sec, language, q_types, marks_per_q, negative_marking,
            options_count, multi_select_allowed, papers_analysed, questions_analysed,
            years_covered, generation_date, option_label_format,
            marking_scheme, level, medium (v2.18 additions).
    progress: the full progress dict (needed for per-question option_label aggregation).
    """
    from datetime import datetime
    out  = f'/mnt/user-data/outputs/{exam_code}_section_rules.md'
    meta = exam_meta or {}
    progress = progress or {}   # v2.15: safe fallback for label aggregation

    # ── CATEGORY C: exam-level header (auto-detected — not hardcoded) ─────────
    lines = [
        f'# {exam_code}_section_rules.md',
        f'# Generated by Framework_MockTestAnalyse v2.23',
        f'# DO NOT edit manually -- regenerate via: PYQExtract {exam_code} --synthesise ALL',
        f'# Download this file from chat → upload to {exam_code} project Files/Knowledge section.',
        '',
        '=== EXAM_STRUCTURE ===',
        f'exam_code: {exam_code}',
        f'total_papers_analysed: {meta.get("papers_analysed", 0)}',
        f'total_questions_analysed: {meta.get("questions_analysed", 0)}',
        f'years_covered: {meta.get("years_covered", [])}',
        f'generation_date: {meta.get("generation_date", datetime.now().isoformat()[:10])}',
        f'time_per_q_sec: {meta.get("time_per_q_sec", "unknown")}',
        f'language: {meta.get("language", "unknown")}',
        # v2.18: new fields from Step 2a v2.5 exam_config contract
        f'medium: {meta.get("medium", "unknown")}',
        f'level: {meta.get("level", "unknown")}',
        f'q_types: {meta.get("q_types", ["MCQ"])}',
        f'marks_per_q: {meta.get("marks_per_q", {"MCQ": 1})}',
        f'negative_marking: {meta.get("negative_marking", 0)}',
        # v2.18: full per-range marking_scheme from exam_config. Steps 7/8/9 can use this
        # for exact per-Q-position marks lookup (e.g., CSIR NET Q.72 → 4 marks, Q.25 → 2 marks).
        # marks_per_q and negative_marking above remain as summary scalars for backward compat.
        f'marking_scheme: {meta.get("marking_scheme", [])}',
        f'options_count: {meta.get("options_count", 4)}',
        # options_count → S1 reads as total_options and writes to blueprint.json Step 7.
        # S2 reads as num_options via bp.get('total_options', 4). SYNC CHAIN:
        #   S0 writes options_count → S1 reads → writes total_options → S2 reads.
        f'option_label_format: {meta.get("option_label_format", "1/2/3/4")}',
        # option_label_format → S1 reads and writes as option_label to blueprint.json Step 7.
        # S2 reads via bp.get('option_label','1/2/3/4') AND re-reads per section from
        # section_rules.md option_label_format field below (per-section override).
        # HOW TO DETECT option_label_format from PYQ: scan PYQ option lines for pattern:
        #   "(1)" / "(A)" / "1." / "A." → set option_label_format accordingly.
        #   Most SSC/banking exams: "1/2/3/4". UPSC/GATE: "A/B/C/D". Regional: varies.
        f'multi_select_allowed: {str(meta.get("multi_select_allowed", False)).lower()}',
        # v2.5 MSQ contract fields (consumed by Step 6/7/9). Inert when multi_select_allowed=false.
        f'msq_k_mode: {meta.get("msq_k_mode", "n/a")}',
        f'msq_k: {meta.get("msq_k", "none")}',
        # v2.6 D5: AOTA policy under MSQ. Step 7 (R-MSQ-ESCAPE/G-MSQ-SET) and Step 8
        # (A-MSQ-KEY) read this directly from section_rules. Default false.
        f'msq_allow_aota: {str(meta.get("msq_allow_aota", False)).lower()}',
        # v2.9 (contract-sync fix): the localized MSQ select-instruction, the EXACT MSQ
        # analogue of nat_instruction below. Step 7 (msq_instruction_for) and Step 8
        # (msq_instruction_phrases) READ this from section_rules; before v2.9 no producer
        # emitted it, so the instruction was silently locked to a hardcoded fallback and was
        # not exam-configurable/localizable the way NAT's is. Now authoritative + overridable
        # per exam; the *_hi variant carries the Hindi/bilingual phrasing. Parenthesised so it
        # reads as an in-stem instruction. Inert when multi_select_allowed=false.
        f'msq_instruction: {meta.get("msq_instruction", "(One or more options may be correct)")}',
        f'msq_instruction_hi: {meta.get("msq_instruction_hi", "(एक या अधिक विकल्प सही हो सकते हैं)")}',
        f'negative_marking_by_type: {meta.get("negative_marking_by_type", {})}',
        f'partial_credit: {str(meta.get("partial_credit", False)).lower()}',
        # v2.12 difficulty_labels — the CANONICAL, exam-overridable difficulty vocabulary
        # used as the RENDERED/stored Complexity value in the per-question index
        # (registry.question_index: Step 6 seeds, Step 7 fills, Step 8 certifies, Step 11
        # renders). Default ['Easy','Medium','Hard']. ALIAS CONTRACT — do NOT conflate the
        # three pre-existing internal spellings:
        #   • Step 5 PYQ_DIFFICULTY_CALIBRATION levels : Simple / Medium / Hard  (analysis)
        #   • Step 6 difficulty_schedule COUNT keys     : simple / medium / hard  (per-mock counts)
        #   • canonical LABEL (this field, index/tags)  : Easy  / Medium / Hard
        # Fixed alias: simple→Easy, medium→Medium, hard→Hard. An exam may override this list
        # (e.g. a 2- or 5-band set); the index value and the schedule bands then draw from it.
        f'difficulty_labels: {meta.get("difficulty_labels", ["Easy", "Medium", "Hard"])}',
        # v2.8 NAT contract fields (consumed by Step 6/7/9). nat_allowed is the capability
        # gate (mirrors multi_select_allowed); nat_present is a rollup of THIS analysis
        # (true iff any subtopic resolved to answer_type=='numerical'). All inert/absent-safe
        # when nat_allowed=false. nat_answer_type/tolerance/instruction define the answer model.
        f'nat_allowed: {str(meta.get("nat_allowed", False)).lower()}',
        f'nat_present: {str(any(e.get("answer_type") == "numerical" for e in entries)).lower()}',
        f'nat_answer_type: {meta.get("nat_answer_type", "real")}',
        f'nat_tolerance: {meta.get("nat_tolerance", "0")}',
        f'nat_instruction: {meta.get("nat_instruction", "Enter your answer as a numerical value.")}',
        f'total_sections: {len(set(e["section"] for e in entries))}',
        f'framework_version: v2.23',
        '',
    ]

    # ── STRUCTURAL_CHANGES_BY_YEAR (observed from data — not hardcoded) ───────
    year_changes = _compute_structural_changes(entries)
    if year_changes:
        lines += [
            '=== STRUCTURAL_CHANGES_BY_YEAR ===',
            '# Observed from PYQ data — NOT hardcoded. Shows removed/new subtopics,',
            '# format changes, DI shifts, FIGURAL elimination across years.',
            '# Step 7 reads these to understand recent exam structural changes.',
        ]
        lines += year_changes
        lines.append('')

    by_sec = {}
    for e in entries: by_sec.setdefault(e['section'], []).append(e)

    # ── v2.4 / v2.24.1 SUBTOPIC_ID: mint once, collision-safe, IDEMPOTENT ──
    # v2.24.1: run_synthesise() now mints ids BEFORE run_qv() (so the gate and every
    # writer read the SAME id). This is a no-op guard for entries already stamped.
    mint_subtopic_ids(entries, exam_meta)

    for section, sec_entries in by_sec.items():
        # v2.15 BUG-D03 fix: derive option LABEL style from per-question option_label
        # stored during extraction — NOT from option_format.primary (which is the
        # content FORMAT type like 'single_value', a completely different domain).
        # Aggregation: collect option_label from all observed Qs in this section via
        # progress, then majority-vote. Fallback to exam-level option_label_format.
        sec_keys = [(e['section'], e['topic'], e['subtopic']) for e in sec_entries]
        all_labels = []
        for sk in sec_keys:
            for q in progress.get(sk, []):
                lbl = q.get('option_label', 'unknown')
                if lbl != 'unknown':
                    all_labels.append(lbl)
        if all_labels:
            fmt_label = Counter(all_labels).most_common(1)[0][0]
        else:
            fmt_label = meta.get('option_label_format', '1/2/3/4')

        # figural_banned: True when ALL FIGURAL subtopics in section are deprecated/absent
        # Computed from observed data — NOT hardcoded per exam.
        figural_entries = [e for e in sec_entries if e.get('format') == 'FIGURAL']
        figural_banned  = bool(figural_entries) and all(
            e.get('observed_count', 0) == 0
            or all(p.get('deprecated', False)
                   for p in e.get('PYQ_STEM_PATTERNS', []))
            for e in figural_entries
        )

        lines += ['', f'=== SECTION: {section} ===',
                  f'option_label_format: {fmt_label}',
                  f'figural_banned: {str(figural_banned).lower()}',
                  'sub_types_observed:']
        for e in sorted(sec_entries, key=lambda x: -x['observed_count']):
            lines.append(f'  - {e["sub_type_label"]} (n={e["observed_count"]})')
        # v2.23 THREE-AXIS (CATEGORY A): the per-section 3-year format-distribution TARGET
        # (per-paper averages) that Step 6 (allocation: Axis-1/3 + LINKED) and Step 7
        # (generation: the other 7 Axis-2 classes, joint-solved with difficulty) enforce,
        # and Step 8 audits. Omitted for all-Zero-PYQ sections (compute returns None).
        axdist = compute_section_axis_distribution(sec_entries, progress)
        if axdist:
            lines.append('axis_distribution:')
            lines.append(f'  recent_years: {axdist["recent_years"]}')
            lines.append(f'  n_papers_recent: {axdist["n_papers_recent"]}')
            lines.append(f'  mocks_per_window: {axdist["mocks_per_window"]}')
            lines.append(f'  negative_rate: {axdist["negative_rate"]}')
            lines.append(f'  axis1_per_paper: {axdist["axis1_per_paper"]}')
            lines.append(f'  axis2_per_paper: {axdist["axis2_per_paper"]}')
            lines.append(f'  axis3_per_paper: {axdist["axis3_per_paper"]}')
            lines.append(f'  axis2_audit_mode: {axdist["axis2_audit_mode"]}')
        for e in sorted(sec_entries, key=lambda x: -x['observed_count']):
            lines += format_entry(e)

    with open(out, 'w', encoding='utf-8') as f: f.write('\n'.join(lines))
    print(f'Written: {out} ({len(lines)} lines)')
    return out

def slugify(text):
    """
    Deterministic slug recipe (v2.4) — exam-agnostic, stable across runs.
    The SAME input string ALWAYS yields the SAME slug, on every exam, forever.
    Recipe (fixed, do not change — changing it would break existing ids):
      1. Lowercase.
      2. Replace em-dash (—), en-dash (–), slash (/), ampersand (&) with space.
      3. Replace any non-alphanumeric run with a single underscore.
      4. Strip leading/trailing underscores; collapse repeated underscores.
    NOTE: stop-words (the/of/and/...) are NOT stripped here. They are only
    skipped inside section_prefix() for the prefix. The slug keeps every word.
    This MUST stay byte-identical to the slugify() in Framework_Blueprint S2-MANIFEST.
    """
    import re
    t = (text or '').lower()
    t = t.replace('—', ' ').replace('–', ' ').replace('/', ' ').replace('&', ' ')
    t = re.sub(r'[^a-z0-9]+', '_', t)
    t = re.sub(r'_+', '_', t).strip('_')
    return t

# Section-prefix recipe (v2.4): readable, stable, deterministic.
# Uses the INITIALS of significant section words (skipping and/of/the/...), so
# 'General Intelligence & Reasoning' -> 'gir', 'Quantitative Aptitude' -> 'qa'.
# Single-word sections fall back to first 4 chars. Prefix collisions between two
# DISTINCT sections are resolved by build_section_prefix_map() with a numeric
# suffix (gs, gs2, ...). exam_meta['section_prefix_overrides'] can pin a prefix.
_PREFIX_STOPWORDS = ('and', 'of', 'the', 'for', 'in', 'to', 'a', 'an')

def section_prefix(section_name, overrides=None):
    overrides = overrides or {}
    if section_name in overrides:
        return overrides[section_name]
    words = [w for w in slugify(section_name).split('_') if w not in _PREFIX_STOPWORDS]
    if len(words) >= 2:
        return ''.join(w[0] for w in words)   # word-initials, e.g. gir / qa / ec
    return (words[0][:4] if words else 'sec')

def build_section_prefix_map(sections, overrides=None):
    """
    Deterministic, collision-safe section→prefix map. Two DISTINCT sections that
    would collapse to the same prefix get numeric suffixes (gs, gs2, ...).
    Build this ONCE from the full section list, then pass the resulting overrides
    into make_subtopic_id so every subtopic uses the same stable prefix.
    """
    seen = {}; result = {}
    for s in sections:
        p = section_prefix(s, overrides)
        if p in seen and seen[p] != s:
            base = p; n = 2
            while p in seen and seen[p] != s:
                p = f'{base}{n}'; n += 1
        seen[p] = s; result[s] = p
    return result

def _as_int(v):
    """v2.11 — coerce a mandate integer field (may arrive as a str from section_rules,
    or as 'none'/None/'' when unset) to int or None. Used for min_per_series_window,
    min_count, and any future numeric mandate field."""
    if v in (None, '', 'none', 'None'):
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _mandate_from_note(note):
    """v2.10 — Robust, sentence-independent 'mandatory every mock' detector.
    Returns True iff the NOTE both (a) mentions MANDATORY and (b) contains an
    every/per mock|paper phrase — anywhere, not necessarily in the same sentence.
    Replaces the v2.4 regex MANDATORY[^.\\n]*\\b(every mock|per mock)\\b, which was
    anchored to a single sentence and accepted only "mock", so it silently missed
    real wording such as "MANDATORY SUBTOPIC ... 1Q per every paper". An explicit
    mandate_every_mock line (emitted by format_entry / editable in section_rules)
    always takes precedence over this fallback. Exam-agnostic."""
    import re as _re
    if not note:
        return False
    return bool(_re.search(r'\bMANDATORY\b', note, _re.I)) and \
           bool(_re.search(r'\b(?:every|per)\s+(?:mock|paper)\b', note, _re.I))


def make_subtopic_id(section, topic, subtopic, prefix_overrides=None):
    """
    Mint the canonical subtopic_id: <section_prefix>.<topic_slug>.<subtopic_slug>
    - Deterministic: same (section, topic, subtopic) → same id, always.
    - Independent of concept_group (a separate concern — DOUBT-3 uniqueness).
    - Human-debuggable: e.g. 'qa.mensuration.mensuration_3d_combined',
      'gir.analogy.mixed_number_letter_analogy'.
    - prefix_overrides: the map from build_section_prefix_map() (collision-safe).
    Collisions (two different subtopics producing the same id) are detected and
    de-duplicated by write_subtopic_manifest() with a numeric suffix _2, _3, ...
    """
    return f'{section_prefix(section, prefix_overrides)}.{slugify(topic)}.{slugify(subtopic)}'


# ═══════════════════════════════════════════════════════════════════════════
# v2.20 — ZERO-PYQ SCAFFOLD ENTRY + TAXONOMY SYNC
# ═══════════════════════════════════════════════════════════════════════════
# These two functions implement Fix A (taxonomy sync) and Fix C (scaffold
# section_rules blocks) from the BUGFIX_Zero_PYQ_Manifest_Gap report.
# Called by run_synthesise() AFTER PYQ-based entries are built and BEFORE
# write_section_rules() / write_subtopic_manifest() run.

# ── v2.24.5: AUTOMATIC ZERO-PYQ FORMAT INFERENCE ────────────────────────────────
# Mirrors the _VISUAL_KEYWORDS set used in synthesise() (the PYQ path). KEEP IN SYNC — any
# keyword added there should be added here so PYQ and zero-PYQ agree on what "looks visual".
_ZP_VISUAL_KEYWORDS = re.compile(
    r'(?i)\b(figure[s]?|figural|diagram[s]?|venn|'
    r'mirror\s+image[s]?|water\s+image[s]?|paper\s*fold(ing)?|'
    r'counting\s+(figure|triangle|shape)[s]?|embedded\s+figure[s]?|'
    r'completion\s+of\s+(figure|pattern)[s]?|dice|cube\s+fold(ing)?|'
    r'pattern\s+completion|image\s+series|visual\s+reasoning)\b')


def infer_zero_pyq_axes(name, sibling_formats, sibling_answer_types, sibling_cardinalities):
    """v2.24.5 — PURE. Automatically infer a zero-PYQ subtopic's Axis-1 format + answer_type +
    answer_cardinality from evidence available WITHOUT any curator input:
      (1) NAME keyword  -> FIGURAL  (per-subtopic; the same heuristic trusted for PYQ subtopics);
      (2) same-topic PYQ SIBLINGS   -> inherit a UNANIMOUS non-TEXT format (>=2 siblings, all
          identical); inherit 'numerical' / 'multi' when >= two-thirds of (>=2) siblings are.
    Falls back to TEXT / option / single when there is no strong signal. Deterministic; no I/O.
    Precedence: name keyword (1) beats sibling inheritance (2). Returns
      {format, answer_type, answer_cardinality, inherently_visual, reason}.
    """
    fmt, inh_vis, reason = 'TEXT', False, 'default'
    if _ZP_VISUAL_KEYWORDS.search(name or ''):                      # (1) name -> FIGURAL
        fmt, inh_vis, reason = 'FIGURAL', True, 'name_keyword'
    else:                                                           # (2) UNANIMOUS topic siblings
        sibs = [f for f in (sibling_formats or []) if f]
        if len(sibs) >= 2 and len(set(sibs)) == 1 and sibs[0] != 'TEXT':
            fmt, reason = sibs[0], 'topic_unanimous'

    ans_type = 'option'                                             # NAT: >=2/3 of >=2 siblings
    at = [a for a in (sibling_answer_types or []) if a]
    if len(at) >= 2 and at.count('numerical') * 3 >= len(at) * 2:
        ans_type = 'numerical'

    ans_card = 'single'                                             # MSQ: >=2/3 of >=2 siblings
    ac = [c for c in (sibling_cardinalities or []) if c]
    if len(ac) >= 2 and ac.count('multi') * 3 >= len(ac) * 2:
        ans_card = 'multi'

    return {'format': fmt, 'answer_type': ans_type, 'answer_cardinality': ans_card,
            'inherently_visual': inh_vis, 'reason': reason}


def apply_zero_pyq_format_inference(entries):
    """v2.24.5 — In-place post-pass over the full entry set. For each ZERO-PYQ entry
    (observed_count == 0), infer format/answer_type/answer_cardinality from its NAME and its
    same-(section, topic) PYQ siblings (observed_count > 0), via infer_zero_pyq_axes(). PYQ
    entries are NEVER touched. Every change is logged (audit trail; no prompt). Runs BEFORE
    id-mint / stamp / QV / writers, so both section_rules and the manifest see the inferred axes.
    """
    from collections import defaultdict
    sib_fmt, sib_at, sib_ac = defaultdict(list), defaultdict(list), defaultdict(list)
    for e in entries:
        if e.get('observed_count', 0) > 0:                          # PYQ sibling
            k = (e.get('section'), e.get('topic'))
            sib_fmt[k].append(e.get('format', 'TEXT'))
            sib_at[k].append(e.get('answer_type', 'option'))
            sib_ac[k].append(e.get('answer_cardinality', 'single'))

    changed = 0
    for e in entries:
        if e.get('observed_count', 0) != 0:                         # PYQ subtopic — untouched
            continue
        k = (e.get('section'), e.get('topic'))
        res = infer_zero_pyq_axes(e.get('subtopic', ''), sib_fmt.get(k, []),
                                  sib_at.get(k, []), sib_ac.get(k, []))
        if res['reason'] == 'default' and res['answer_type'] == 'option' \
                and res['answer_cardinality'] == 'single':
            continue                                                # no signal → keep safe defaults
        before = (e.get('format'), e.get('answer_type'), e.get('answer_cardinality'))
        e['format'] = res['format']
        e['answer_type'] = res['answer_type']
        e['answer_cardinality'] = res['answer_cardinality']
        e['inherently_visual'] = bool(res['inherently_visual']) or e.get('inherently_visual', False)
        # keep the freq fields consistent with the inferred string type (some derivations read them)
        if res['answer_type'] == 'numerical':
            e['nat_freq'] = max(e.get('nat_freq', 0), 100)
        if res['answer_cardinality'] == 'multi':
            e['msq_freq'] = max(e.get('msq_freq', 0), 100)
        if res['format'] == 'FIGURAL' and not e.get('figural_data'):
            e['figural_data'] = {                                   # same conservative default as PYQ path
                'image_role': 'stem_only',
                'object_types': {'dominant': [], 'observed': [], 'avoid': []},
                'transformation_types': [], 'arrangement_types': [],
                'complexity_dist': {}, 'images_analysed': 0, 'images_unclear': 0}
        changed += 1
        print(f"  ZERO-PYQ INFERENCE: '{e.get('subtopic')}' "
              f"[{e.get('section')} > {e.get('topic')}] {before} -> "
              f"({res['format']}, {res['answer_type']}, {res['answer_cardinality']}) "
              f"[{res['reason']}]")
    if changed:
        print(f"Zero-PYQ format inference: {changed} scaffold entr"
              f"{'y' if changed == 1 else 'ies'} refined from name/topic evidence.")
    return entries


def make_zero_pyq_scaffold_entry(section, topic, subtopic):
    """
    v2.20 Fix C — Create a COMPLETE entry dict for a zero-PYQ subtopic.
    This entry has every field that format_entry() expects, filled with
    zero-PYQ defaults. The resulting section_rules block gives Step 7
    enough structure to generate questions using training knowledge +
    format guidance, even though no PYQ data exists for this subtopic.

    Returns: dict matching the synthesise_subtopic() output schema.
    """
    return {
        'section': section,
        'topic': topic,
        'subtopic': subtopic,
        'observed_count': 0,
        'format': 'TEXT',
        'option_format': {
            'primary': 'single_value',
            'recent_format': 'single_value',
            'changed_recently': False,
            'all_observed': ['single_value']
        },
        'OMML_required': False,
        'negative_question_freq': 0,
        'answer_type': 'option',
        'nat_freq': 0,
        'answer_cardinality': 'single',
        'msq_freq': 0,
        # v2.23: Zero-PYQ scaffold — no observed Axis-2; capability = family ∪ {DIRECT}
        # so Step 7 can use it as a format-elastic filler (decision 11).
        'observed_axis2': {},
        'presentation_family': resolve_presentation_family_s5(subtopic, 'TEXT'),
        'axis2_capability': axis2_capability(
            [], resolve_presentation_family_s5(subtopic, 'TEXT'), 'TEXT'),
        'fill_in_blank': 'none',
        'linked_group_size': 0,
        'max_per_paper': 2,
        'typical_per_paper': 1,
        'stem_word_count': {'min': 10, 'max': 50, 'typical': 25},
        'sub_type_label': subtopic,
        'concept_group': None,        # v2.24.1 (D8): stamped later by stamp_mechanic_axes()
        'question_mechanic': None,    # v2.24.1 (D8)
        'form_key': None,             # v2.24.1 (D8)
        'collision_domain': None,     # v2.24.1 (D8)
        'mandate_every_mock': False,
        'alternation_group': None,
        'min_per_series_window': None,
        'mandatory_group': None,
        'min_count': None,
        'PYQ_STEM_PATTERNS': [
            {
                'id': 'P1',
                'template': f'Standard {subtopic} question',
                'approach': 'direct',
                'frequency': 100,
                'confidence': 'absent',
                'raw_count': 0,
                'years': [],
                'note_block': 'never',
                'deprecated': False
            }
        ],
        'PYQ_DIFFICULTY_CALIBRATION': {
            'Simple': {'criteria': '(no PYQ data)', 'is_inferred': True},
            'Medium': {'criteria': '(no PYQ data)', 'is_inferred': True},
            'Hard':   {'criteria': '(no PYQ data)', 'is_inferred': True}
        },
        'wrong_option_structure': {
            'type': 'same_category',
            'description': 'Options from the same conceptual category as the correct answer.'
        },
        'NOTE': (f'Zero-PYQ subtopic. No PYQ observations available. '
                 f'Added from exam syllabus/taxonomy via v2.20 taxonomy sync. '
                 f'Step 7 generates questions using exam-level knowledge and '
                 f'the format/option guidance above.'),
        'note_text': (f'Zero-PYQ subtopic. No PYQ observations available. '
                      f'Added from exam syllabus/taxonomy via v2.20 taxonomy sync. '
                      f'Step 7 generates questions using exam-level knowledge and '
                      f'the format/option guidance above.')
    }


def taxonomy_sync_entries(existing_entries, exam_code):
    """
    v2.20 Fix A — TAXONOMY SYNC PROTOCOL.

    After PYQ-based synthesis produces the entry list, this function
    synchronises it with the exam's approved taxonomy to ensure the
    manifest covers the COMPLETE subtopic vocabulary, not just the
    PYQ-observed subset.

    For every taxonomy-defined subtopic NOT already in existing_entries,
    creates a scaffold entry via make_zero_pyq_scaffold_entry().

    Taxonomy sources (UNION — both loaded, not primary/fallback):
      1. taxonomy_draft.json: [ExamCode]_taxonomy_draft.json in project
         knowledge — the syllabus-faithful taxonomy from Step 2a. This is
         the source that contains zero-PYQ subtopics (new syllabus entries
         that have never appeared in any PYQ paper). PRIMARY source.
      2. Approved Analysis doc: [ExamCode]_PYQ_Analysis.docx in project
         knowledge — ADDITIONAL source. The Analysis doc typically contains
         only PYQ-observed subtopics (which are already in existing_entries),
         but is loaded as a safety net in case taxonomy_draft is absent.

    WHY taxonomy_draft IS PRIMARY (not Analysis doc):
      The Analysis doc (Step 2c output) contains ~PYQ-observed subtopics.
      Zero-PYQ subtopics (the ones this function exists to find) are NOT
      in the Analysis doc — they have zero PYQ observations so they were
      never processed. The taxonomy_draft.json (Step 2a output) IS the
      syllabus-faithful source that contains ALL subtopics including
      zero-PYQ ones. Evidence: SSC CGL Tier 2 — taxonomy_draft had 93
      subtopics (all 7 orphans present), Analysis doc had ~96 (orphans
      absent, but finer PYQ-discovered splits present).

    Returns: (new_entries_list, sync_log_lines)
      new_entries_list: scaffold entries to APPEND to existing_entries.
      sync_log_lines:   human-readable log of what was added/skipped.

    EDGE CASES (ref: BUGFIX_Zero_PYQ_Manifest_Gap.md):
      EC-ZP-1: Taxonomy subtopic name COLLIDES with existing entry
               (same slugified name) → use existing, do not duplicate.
      EC-ZP-2: Taxonomy subtopic is COVERED by finer-grained existing
               entries (e.g., taxonomy "Geometry" but entries have
               "Triangles", "Circles") → do not create; log coverage.
      EC-ZP-3: Taxonomy subtopic under DIFFERENT section than existing
               → section mismatch is a HARD STOP (taxonomy must align
               with exam_config sections).
      EC-ZP-4: Exam with ZERO PYQ papers (100% zero-PYQ) → all
               subtopics become scaffold entries. Supported.
      EC-ZP-5: taxonomy_draft.json absent AND Analysis doc absent
               → sync SKIPS (cannot add what doesn't exist). Log warning.
      EC-ZP-6: PYQ-discovered subtopic NOT in taxonomy → already in
               entries. Taxonomy sync only ADDS; it never removes.
      EC-ZP-7: Same subtopic in MULTIPLE sections in taxonomy
               → each gets its own entry (slugify includes section prefix).
      EC-ZP-8: Subtopic in taxonomy_draft but REMOVED from Analysis doc
               → taxonomy_draft is the syllabus-faithful source; if a
               subtopic is in taxonomy_draft it represents the exam
               authority's syllabus. If it was intentionally excluded,
               it should be removed from taxonomy_draft.json itself.
      EC-ZP-9: Subtopic in section_rules but not manifest → handled by
               rebuild_subtopic_manifest_from_section_rules() (separate).
      EC-ZP-10: Large exam (300+ taxonomy, 50 in PYQs) → adds 250+
                scaffold entries. No performance issue (flat list).
    """
    import json, os, glob, re

    sync_log = []
    new_entries = []

    # ── Step 1: Build the EXISTING subtopic index from PYQ-derived entries ──
    # Key: (section_slug, topic_slug, subtopic_slug) for collision detection.
    # Also build a set of subtopic_slugs per section for EC-ZP-2 coverage check.
    existing_keys = set()
    existing_slugs_by_section = {}   # section -> set of subtopic slugs
    existing_topic_slugs_by_section = {}  # section -> set of topic slugs
    for e in existing_entries:
        sec_s = slugify(e['section'])
        top_s = slugify(e['topic'])
        sub_s = slugify(e['subtopic'])
        existing_keys.add((sec_s, top_s, sub_s))
        existing_slugs_by_section.setdefault(sec_s, set()).add(sub_s)
        existing_topic_slugs_by_section.setdefault(sec_s, set()).add(top_s)

    # ── Step 2: Load taxonomy sources (UNION — both tried) ──
    taxonomy_tuples = []   # list of (section, topic, subtopic) raw strings
    seen_tuples = set()    # dedup across sources

    # Source 1 (PRIMARY): taxonomy_draft.json — the syllabus-faithful taxonomy
    # This is the source that contains zero-PYQ subtopics (the orphans).
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        for f in glob.glob(os.path.join(search_dir, f'*taxonomy_draft*.json')):
            try:
                with open(f, encoding='utf-8') as fp:
                    tax_data = json.load(fp)
                # taxonomy_draft.json structure: {section: {topic: [subtopic, ...]}}
                if isinstance(tax_data, dict):
                    for sec, topics in tax_data.items():
                        if isinstance(topics, dict):
                            for top, subs in topics.items():
                                if isinstance(subs, list):
                                    for sub in subs:
                                        tup_key = (slugify(sec), slugify(top), slugify(sub))
                                        if tup_key not in seen_tuples:
                                            taxonomy_tuples.append((sec, top, sub))
                                            seen_tuples.add(tup_key)
                if taxonomy_tuples:
                    sync_log.append(f'  Taxonomy source 1 (PRIMARY): taxonomy_draft.json ({os.path.basename(f)}) — {len(taxonomy_tuples)} subtopics')
                    break
            except Exception as ex:
                sync_log.append(f'  WARN: taxonomy_draft.json unreadable: {ex}')

    # Source 2 (ADDITIONAL): approved Analysis doc — safety net for when
    # taxonomy_draft is absent. Uses python-docx heading detection (same
    # approach as extract_taxonomy_from_analysis_doc) to parse the .docx.
    analysis_added = 0
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        for f in glob.glob(os.path.join(search_dir, '*.docx')):
            bn = os.path.basename(f).lower()
            if 'analysis' in bn and exam_code.lower() in bn:
                try:
                    doc_tuples = _extract_taxonomy_tuples_from_analysis_doc(f)
                    for tup in doc_tuples:
                        tup_key = (slugify(tup[0]), slugify(tup[1]), slugify(tup[2]))
                        if tup_key not in seen_tuples:
                            taxonomy_tuples.append(tup)
                            seen_tuples.add(tup_key)
                            analysis_added += 1
                    if doc_tuples:
                        sync_log.append(
                            f'  Taxonomy source 2 (ADDITIONAL): Analysis doc ({os.path.basename(f)}) — '
                            f'{analysis_added} new subtopics added beyond taxonomy_draft')
                except Exception as ex:
                    sync_log.append(f'  WARN: Analysis doc {os.path.basename(f)} unreadable: {ex}')

    # EC-ZP-5: no taxonomy source found → skip sync
    if not taxonomy_tuples:
        sync_log.append(
            '  Taxonomy sync SKIPPED: no taxonomy_draft.json or Analysis doc found. '
            'If Step 6 encounters unresolvable subtopics, re-run Step 2a (PYQDraft) '
            'to generate taxonomy_draft.json, then re-run Step 5.')
        return new_entries, sync_log

    sync_log.append(f'  Total taxonomy subtopics (union): {len(taxonomy_tuples)}')

    # ── Step 3: Diff taxonomy against existing entries ──
    added_count = 0
    skipped_existing = 0
    skipped_covered = 0

    for (tax_sec, tax_top, tax_sub) in taxonomy_tuples:
        sec_s = slugify(tax_sec)
        top_s = slugify(tax_top)
        sub_s = slugify(tax_sub)

        # EC-ZP-1: exact match (same section+topic+subtopic slug) → already exists
        if (sec_s, top_s, sub_s) in existing_keys:
            skipped_existing += 1
            continue

        # EC-ZP-1 variant: same subtopic slug under same section (different topic slug)
        # Check if ANY existing entry in this section has the same subtopic slug.
        # This catches renames/reclassifications at the topic level.
        if sec_s in existing_slugs_by_section and sub_s in existing_slugs_by_section[sec_s]:
            skipped_existing += 1
            sync_log.append(
                f'  SKIP (EC-ZP-1): "{tax_sub}" in [{tax_sec}] — slug matches existing entry.')
            continue

        # EC-ZP-2: coverage check — is this taxonomy subtopic COVERED by finer-grained
        # existing entries? If the taxonomy subtopic slug is a PREFIX of any existing
        # subtopic's topic_slug or subtopic_slug within the same section, the finer
        # entries likely cover the taxonomy scope.
        if sec_s in existing_slugs_by_section:
            covered_by = [s for s in existing_slugs_by_section[sec_s]
                          if sub_s in s and sub_s != s]
            if covered_by:
                skipped_covered += 1
                sync_log.append(
                    f'  SKIP (EC-ZP-2): "{tax_sub}" in [{tax_sec}] — covered by '
                    f'finer entries: {covered_by[:5]}')
                continue

        # Not in existing → create scaffold entry
        scaffold = make_zero_pyq_scaffold_entry(tax_sec, tax_top, tax_sub)
        new_entries.append(scaffold)
        existing_keys.add((sec_s, top_s, sub_s))
        existing_slugs_by_section.setdefault(sec_s, set()).add(sub_s)
        added_count += 1
        sync_log.append(f'  ADDED: "{tax_sub}" [{tax_sec} > {tax_top}] — zero-PYQ scaffold')

    sync_log.append(
        f'  Taxonomy sync complete: {added_count} zero-PYQ scaffolds added, '
        f'{skipped_existing} already existed, {skipped_covered} covered by finer entries.')

    return new_entries, sync_log


def _extract_taxonomy_tuples_from_analysis_doc(docx_path):
    """
    v2.20 — Extract (section, topic, subtopic) tuples from an approved
    Analysis doc (.docx). Uses the SAME python-docx heading-style parsing
    as extract_taxonomy_from_analysis_doc() but returns tuples instead of
    modifying a dict in-place.

    The Analysis doc uses Word formatting (Heading 1/2/3 + bold paragraphs)
    to denote hierarchy, NOT text markers like '=== SECTION:'. This function
    reads paragraph styles and bold runs to detect the hierarchy.

    Returns: list of (section_name, topic_name, subtopic_name) tuples.
    Returns empty list if the doc cannot be parsed or python-docx unavailable.
    """
    tuples = []
    try:
        from docx import Document as WDoc
        doc = WDoc(docx_path)
        cur_sec = cur_top = ''

        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            has_bold = any(r.bold for r in para.runs if r.text.strip())
            if not has_bold:
                continue

            style_name = para.style.name if para.style else ''
            indent = para.paragraph_format.left_indent or 0

            if 'Heading 1' in style_name or (indent == 0 and not cur_sec):
                cur_sec = text
                cur_top = ''
            elif 'Heading 2' in style_name or (indent == 0 and cur_sec):
                cur_top = text
            elif 'Heading 3' in style_name or (has_bold and cur_sec):
                if cur_sec and cur_top:
                    tuples.append((cur_sec, cur_top, text))
                elif cur_sec:
                    # Topic not yet set — use section as topic fallback
                    tuples.append((cur_sec, cur_sec, text))

    except ImportError:
        pass  # python-docx not available — caller falls through to other sources
    except Exception:
        pass  # Non-fatal — caller handles empty return

    return tuples


def write_taxonomy_xlsx(manifest, exam_code):
    """v2.24 — Emit [ExamCode]_taxonomy.xlsx: a plain, human-readable list of
    Subject | Topic | Sub Topic Name | Sub Topic Id (one row per sub-topic, sorted), so the
    Step-6 operator can pick scope values WITHOUT reading the manifest JSON. It is a companion
    to subtopic_manifest.json, generated from the SAME dict — the JSON stays authoritative.
    Failure to write (e.g. openpyxl absent) is a WARN, never a hard stop.

    Column -> Step-6 use:  Subject = subject scope · "Subject::Topic" = topic scope ·
    "Subject::Topic::Sub Topic Name" = subtopic scope (or the Sub Topic Id if that name repeats
    under the same topic).
    """
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("WARN: openpyxl unavailable — skipped taxonomy.xlsx (manifest.json is authoritative).")
        return None

    rows = sorted(
        ([v.get('section', ''), v.get('topic', ''), v.get('display_name', ''), sid]
         for sid, v in manifest.get('subtopics', {}).items()),
        key=lambda r: (str(r[0]).lower(), str(r[1]).lower(), str(r[2]).lower()))

    wb = Workbook()
    ws = wb.active
    ws.title = 'Taxonomy'
    head_font = Font(name='Arial', size=11, bold=True, color='FFFFFF')
    head_fill = PatternFill('solid', fgColor='1F4E79')
    arial = Font(name='Arial', size=11)
    thin = Side(style='thin', color='D0D0D0')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c, name in enumerate(['Subject', 'Topic', 'Sub Topic Name', 'Sub Topic Id'], start=1):
        cell = ws.cell(row=1, column=c, value=name)
        cell.font = head_font
        cell.fill = head_fill
        cell.alignment = Alignment(horizontal='left', vertical='center')
        cell.border = border
    band = PatternFill('solid', fgColor='F2F6FB')
    prev_subject, shade = None, False
    for i, row in enumerate(rows, start=2):
        if row[0] != prev_subject:
            shade = not shade
            prev_subject = row[0]
        for c, val in enumerate(row, start=1):
            cell = ws.cell(row=i, column=c, value=val)
            cell.font = arial
            cell.border = border
            cell.alignment = Alignment(horizontal='left', vertical='center')
            if shade:
                cell.fill = band
    for c, width in enumerate([26, 30, 46, 30], start=1):
        ws.column_dimensions[get_column_letter(c)].width = width
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:D{len(rows) + 1}'

    hw = wb.create_sheet('How to use')
    guide = [
        (f'{exam_code} — how to use this list in Step 6', True),
        ('', False),
        ('This lists every Subject, Topic and Sub-Topic in your exam. Pick from the', False),
        ('"Taxonomy" tab, then copy the value into the Step-6 trigger (match text EXACTLY —', False),
        ('spelling and capital letters matter). Use the header filter arrows to narrow down.', False),
        ('', False),
        ('SUBJECT test   -> copy the Subject cell (column A):', True),
        ('    ScopedBlueprint --level subject  --scope "<Subject>"          --count N --qs_per_paper Q', False),
        ('', False),
        ('TOPIC test     -> join Subject and Topic with "::" (columns A and B):', True),
        ('    ScopedBlueprint --level topic    --scope "<Subject>::<Topic>" --count N --qs_per_paper Q', False),
        ('', False),
        ('SUB-TOPIC test -> join Subject + Topic + Sub Topic Name with "::" (columns A, B, C):', True),
        ('    ScopedBlueprint --level subtopic --scope "<Subject>::<Topic>::<Sub Topic Name>" --count N --qs_per_paper Q', False),
        ('    The Topic in the middle keeps same-named sub-topics apart — e.g. "Kinematics"', False),
        ('    under Mechanics vs under Rotational Motion resolve to two DIFFERENT sub-topics.', False),
        ('    Use the Sub Topic Id (column D) ONLY if the same name repeats under the same Topic:', False),
        ('        --scope <Sub Topic Id>', False),
    ]
    for i, (text, bold) in enumerate(guide, start=1):
        hw.cell(row=i, column=1, value=text).font = Font(name='Arial', size=11, bold=bold)
    hw.column_dimensions['A'].width = 100

    out = f'/mnt/user-data/outputs/{exam_code}_taxonomy.xlsx'
    wb.save(out)
    print(f'Written: {out} ({len(rows)} sub-topics — human-readable taxonomy for Step 6)')
    return out


def write_subtopic_manifest(entries, exam_code, exam_meta=None, progress=None):
    """
    v2.4 — Write [ExamCode]_subtopic_manifest.json: the AUTHORITATIVE id↔name
    registry and the formal cross-step contract artifact.
    v2.23 — also carries the THREE-AXIS machine data Step 6 reads without re-parsing PYQ:
      • per subtopic: observed_axis2, presentation_family, axis2_capability
      • top-level 'axis_distribution': {section: <compute_section_axis_distribution()>}
        (needs `progress`; omitted per-section when progress is absent — section_rules.md
        remains the authoritative human-readable copy either way).

    This manifest is the SINGLE SOURCE OF TRUTH for the subtopic vocabulary.
    Step 6 (Blueprint) and Step 7 (Create) MUST read it and reference subtopics
    by subtopic_id. They never invent ids; an unknown id is a HARD STOP.

    Structure:
    {
      "exam_code": "...",
      "manifest_version": "1.0",
      "generated_by": "Framework_MockTestAnalyse v2.22",
      "id_recipe": "<section_prefix>.<topic_slug>.<subtopic_slug> via slugify v2.4",
      "subtopics": {
         "<subtopic_id>": {
            "display_name": "...",      # decorative; may change without breaking joins
            "section": "...",
            "topic": "...",
            "concept_group": "...",     # carried for convenience; NOT part of the id
            "format": "TEXT|PASSAGE|FIGURAL|DI|...",
            "inherently_visual": false,   // v2.22: true if keyword heuristic fired
            "mandates": {               # structured MANDATE data (not prose)
               "mandatory_every_mock": false,
               "alternation_group": null,   # e.g. "ci_si" ; members alternate, never co-occur
               "min_per_series_window": null
            }
         }, ...
      },
      "alternation_groups": {           # groups whose members must NOT co-occur in one mock
         "ci_si": ["qa.interest.simple_interest", "qa.interest.compound_interest"]
      },
      "mandatory_every_mock": [ "<id>", ... ]   # flat list for fast Step-1/2 checks
    }

    MANDATE EXTRACTION (exam-agnostic, v2.10). Three round-trippable fields per
    subtopic, emitted by format_entry and read here AND by
    rebuild_subtopic_manifest_from_section_rules():
      • mandatory_every_mock — an explicit entry field mandate_every_mock wins;
        else _mandate_from_note() (NOTE mentions MANDATORY *and* an every/per
        mock|paper phrase, sentence-independent). This replaces the pre-v2.10
        single-sentence, mock-only regex that missed wording like "1Q per every paper".
      • alternation_group — the authored group name on BOTH members (e.g. set
        alternation_group='ci_si' on Simple Interest AND Compound Interest); the
        manifest groups members by that name. Members must NOT co-occur in one mock.
      • min_per_series_window — authored cadence integer (reserved for the Issue-2b
        window/cadence enforcement; carried through as data, inert until then).
    Because format_entry now writes all three into section_rules, the manifest is
    fully reproducible from the section_rules FILE alone — no ephemeral entry state.
    """
    import json, re
    out = f'/mnt/user-data/outputs/{exam_code}_subtopic_manifest.json'
    meta = exam_meta or {}
    overrides = meta.get('section_prefix_overrides', {})

    manifest = {
        'exam_code': exam_code,
        'manifest_version': '1.0',
        'generated_by': 'Framework_MockTestAnalyse v2.23',
        'id_recipe': '<section_prefix>.<topic_slug>.<subtopic_slug>; section_prefix=word-initials (gir/ga/qa/ec), slugify v2.4',
        'subtopics': {},
        'alternation_groups': {},
        'mandatory_every_mock': [],
        # v2.11 — the three mandate types a flat per-id list cannot express (Issue 2b):
        'mandatory_groups': {},   # {group: {members:[ids], min:int}} — >=min members present per mock
        'cadence_windows': {},    # {id: N}  — subtopic must appear >=1 in every N-mock window
        'min_counts': {},         # {id: k}  — subtopic must have >=k Q per mock
        'axis_distribution': {}   # v2.23 {section: per-section 3-yr format-distribution target}
    }

    # v2.23 per-section axis distribution (needs the question lists in `progress`).
    if progress:
        _by_sec = {}
        for e in entries:
            _by_sec.setdefault(e['section'], []).append(e)
        for _sec, _ents in _by_sec.items():
            _ax = compute_section_axis_distribution(_ents, progress)
            if _ax:
                manifest['axis_distribution'][_sec] = _ax

    seen_ids = {}
    for e in entries:
        # Reuse the id stamped by write_section_rules (e['subtopic_id']) so the
        # manifest id is IDENTICAL to the section_rules block id. Only recompute as
        # a fallback if write_subtopic_manifest is ever called before stamping.
        sid = e.get('subtopic_id')
        if not sid:
            sid = make_subtopic_id(e['section'], e['topic'], e['subtopic'],
                                   build_section_prefix_map(
                                       sorted({x['section'] for x in entries}), overrides))
            base = sid; n = 2
            key = (e['section'], e['topic'], e['subtopic'])
            while sid in seen_ids and seen_ids[sid] != key:
                sid = f'{base}_{n}'; n += 1
        seen_ids[sid] = (e['section'], e['topic'], e['subtopic'])

        note = (e.get('NOTE') or e.get('note') or e.get('note_text') or '')
        # v2.10: an explicit mandate_every_mock (from the entry / round-tripped from
        # section_rules) wins; otherwise the robust sentence-independent detector
        # (_mandate_from_note) replaces the brittle single-sentence, mock-only regex
        # that missed wording like "MANDATORY ... 1Q per every paper".
        mand_every = bool(e['mandate_every_mock']) if 'mandate_every_mock' in e \
                     else _mandate_from_note(note)
        manifest['subtopics'][sid] = {
            'display_name': e['subtopic'],
            'section': e['section'],
            'topic': e['topic'],
            'concept_group': e.get('concept_group') or _derive_concept_group(e),
            'question_mechanic': e.get('question_mechanic') or _derive_question_mechanic(e),  # v2.24
            'form_key': e.get('form_key') or _derive_form_key(e),                             # v2.24
            'collision_domain': e.get('collision_domain') or _derive_collision_domain(e),     # v2.24
            'format': e.get('format', 'TEXT'),
            'inherently_visual': bool(e.get('inherently_visual', False)),   # v2.22
            # v2.23 THREE-AXIS per-subtopic capability (Step 6 rare-format reachability;
            # Step 7 renders only within axis2_capability — fabrication banned).
            'observed_axis2': e.get('observed_axis2', {}),
            'presentation_family': e.get('presentation_family'),
            'axis2_capability': e.get('axis2_capability', ['DIRECT']),
            'mandates': {
                'mandatory_every_mock': mand_every,
                'alternation_group': e.get('alternation_group'),
                'min_per_series_window': _as_int(e.get('min_per_series_window')),
                'mandatory_group': e.get('mandatory_group'),          # v2.11 group-presence
                'min_count': _as_int(e.get('min_count'))              # v2.11 min Q per mock
            }
        }
        if mand_every:
            manifest['mandatory_every_mock'].append(sid)
        ag = e.get('alternation_group')
        if ag:
            manifest['alternation_groups'].setdefault(ag, [])
            if sid not in manifest['alternation_groups'][ag]:
                manifest['alternation_groups'][ag].append(sid)
        # v2.11 rollups (Issue 2b) — group-presence, cadence, min-count:
        mg = e.get('mandatory_group')
        if mg and mg != 'none':
            g = manifest['mandatory_groups'].setdefault(mg, {'members': [], 'min': 1})
            if sid not in g['members']:
                g['members'].append(sid)
        _win = _as_int(e.get('min_per_series_window'))
        if _win:
            manifest['cadence_windows'][sid] = _win
        _mc = _as_int(e.get('min_count'))
        if _mc:
            manifest['min_counts'][sid] = _mc

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f'Written: {out} ({len(manifest["subtopics"])} subtopic ids, '
          f'{len(manifest["mandatory_every_mock"])} mandatory-every-mock, '
          f'{len(manifest["alternation_groups"])} alternation groups, '
          f'{len(manifest["mandatory_groups"])} group-presence, '
          f'{len(manifest["cadence_windows"])} cadence, '
          f'{len(manifest["min_counts"])} min-count)')
    write_taxonomy_xlsx(manifest, exam_code)   # v2.24 — human-readable companion
    return out


def rebuild_subtopic_manifest_from_section_rules(section_rules_path, exam_code):
    """v2.10 — Reconstruct a COMPLETE subtopic_manifest.json from an existing
    section_rules.md ALONE (no source PYQ, no in-memory entries). This is the
    supported path to (re)generate a MISSING or INCOMPLETE manifest — e.g. a project
    that has section_rules + blueprint but lost the manifest, or one whose mandate
    markers were edited by hand and must be re-minted.

    It parses every '--- Subtopic: --- block and reads the round-trippable mandate
    lines emitted by format_entry (mandate_every_mock / alternation_group /
    min_per_series_window), falling back to the robust NOTE detector
    (_mandate_from_note) only when an explicit mandate_every_mock line is absent
    (legacy blocks written before v2.10). ONLY id-carrying blocks enter the manifest
    join; a block without subtopic_id cannot be joined by Step 6/7, so it is skipped
    and surfaced as a WARN (mint its id in Step 5, or add one, then re-run).

    Output schema is byte-identical to write_subtopic_manifest(). Exam-agnostic —
    zero subtopic names hardcoded.
    """
    import json, re, ast
    text = open(section_rules_path, encoding='utf-8').read()
    manifest = {
        'exam_code': exam_code,
        'manifest_version': '1.0',
        'generated_by': 'Framework_MockTestAnalyse v2.23 (rebuild_from_section_rules)',
        'id_recipe': '<section_prefix>.<topic_slug>.<subtopic_slug>; slugify v2.4',
        'subtopics': {},
        'alternation_groups': {},
        'mandatory_every_mock': [],
        'mandatory_groups': {},   # v2.11 group-presence
        'cadence_windows': {},    # v2.11 cadence
        'min_counts': {},         # v2.11 min Q per mock
        'axis_distribution': {}   # v2.23 (round-tripped from the AXIS_DISTRIBUTION block below)
    }

    def _lit(s, default):
        """Safe Python-literal parse for round-tripped axis fields ({...}/[...]/floats)."""
        try:
            return ast.literal_eval(s.strip())
        except Exception:
            return default
    EXPL_MAND = re.compile(r'^\s*mandate_every_mock:\s*(true|false)\s*$', re.I | re.M)
    EXPL_ALT  = re.compile(r'^\s*alternation_group:\s*(\S+)\s*$', re.M)
    EXPL_WIN  = re.compile(r'^\s*min_per_series_window:\s*(\S+)\s*$', re.M)
    EXPL_GRP  = re.compile(r'^\s*mandatory_group:\s*(\S+)\s*$', re.M)          # v2.11
    EXPL_MINC = re.compile(r'^\s*min_count:\s*(\S+)\s*$', re.M)               # v2.11
    ID_RE     = re.compile(r'^\s*subtopic_id:\s*(\S+)\s*$', re.M)
    SEC_RE    = re.compile(r'^\s*section:\s*(.+)$', re.M)
    TOP_RE    = re.compile(r'^\s*topic:\s*(.+)$', re.M)
    FMT_RE    = re.compile(r'^\s*format:\s*(\S+)\s*$', re.M)
    INHERENT_RE = re.compile(r'^\s*inherently_visual:\s*(true|false)\s*$', re.I | re.M)  # v2.22
    CG_RE     = re.compile(r'^\s*concept_group:\s*(.+)$', re.M)
    QM_RE      = re.compile(r'^\s*question_mechanic:\s*(.+)$', re.M)    # v2.24
    FORMKEY_RE = re.compile(r'^\s*form_key:\s*(.+)$', re.M)             # v2.24
    CDOM_RE    = re.compile(r'^\s*collision_domain:\s*(.+)$', re.M)     # v2.24
    NOTE_RE   = re.compile(r'^\s*NOTE\s*:\s*(.+)$', re.M | re.I)
    OBSAX_RE  = re.compile(r'^\s*observed_axis2:\s*(.+)$', re.M)          # v2.23
    PFAM_RE   = re.compile(r'^\s*presentation_family:\s*(.+)$', re.M)     # v2.23
    AX2CAP_RE = re.compile(r'^\s*axis2_capability:\s*(.+)$', re.M)        # v2.23

    id_less = []
    for raw in re.split(r'\n--- Subtopic:', text)[1:]:
        disp  = raw.split('---', 1)[0].strip()
        sid_m = ID_RE.search(raw)
        if not sid_m:
            id_less.append(disp)                 # cannot be joined — skip, warn below
            continue
        sid    = sid_m.group(1)
        note_m = NOTE_RE.search(raw)
        note   = note_m.group(1) if note_m else ''
        em = EXPL_MAND.search(raw)
        mand = (em.group(1).lower() == 'true') if em else _mandate_from_note(note)
        av = EXPL_ALT.search(raw)
        ag = av.group(1) if (av and av.group(1).lower() != 'none') else None
        wv  = EXPL_WIN.search(raw)
        win = _as_int(wv.group(1)) if wv else None
        gv  = EXPL_GRP.search(raw)                                   # v2.11
        grp = gv.group(1) if (gv and gv.group(1).lower() != 'none') else None
        mcv = EXPL_MINC.search(raw)                                  # v2.11
        mc  = _as_int(mcv.group(1)) if mcv else None
        _sec_r = SEC_RE.search(raw).group(1).strip() if SEC_RE.search(raw) else ''   # v2.24
        _fmt_r = FMT_RE.search(raw).group(1) if FMT_RE.search(raw) else 'TEXT'        # v2.24
        _ax_r  = derive_mechanic(_sec_r, disp, None, '', _fmt_r, sid)                 # v2.24
        manifest['subtopics'][sid] = {
            'display_name':  disp,
            'section':       (SEC_RE.search(raw).group(1).strip() if SEC_RE.search(raw) else ''),
            'topic':         (TOP_RE.search(raw).group(1).strip() if TOP_RE.search(raw) else ''),
            'concept_group': (CG_RE.search(raw).group(1).strip()  if CG_RE.search(raw)  else _ax_r['family']),
            'question_mechanic': (QM_RE.search(raw).group(1).strip() if QM_RE.search(raw) else _ax_r['mechanic']),   # v2.24
            'form_key': (FORMKEY_RE.search(raw).group(1).strip() if FORMKEY_RE.search(raw) else _ax_r['form_key']),  # v2.24
            'collision_domain': (CDOM_RE.search(raw).group(1).strip() if CDOM_RE.search(raw) else _ax_r['collision_domain']),  # v2.24
            'format':        (FMT_RE.search(raw).group(1)         if FMT_RE.search(raw) else 'TEXT'),
            'inherently_visual': (INHERENT_RE.search(raw).group(1).lower() == 'true'
                                  if INHERENT_RE.search(raw) else False),   # v2.22
            # v2.23 THREE-AXIS per-subtopic (round-tripped; safe defaults for legacy blocks)
            'observed_axis2':      (_lit(OBSAX_RE.search(raw).group(1), {})
                                    if OBSAX_RE.search(raw) else {}),
            'presentation_family': ((lambda v: None if v in ('None', '') else v)
                                    (PFAM_RE.search(raw).group(1).strip())
                                    if PFAM_RE.search(raw) else None),
            'axis2_capability':    (_lit(AX2CAP_RE.search(raw).group(1), ['DIRECT'])
                                    if AX2CAP_RE.search(raw) else ['DIRECT']),
            'mandates': {
                'mandatory_every_mock': mand,
                'alternation_group':    ag,
                'min_per_series_window': win,
                'mandatory_group':      grp,     # v2.11 group-presence
                'min_count':            mc       # v2.11 min Q per mock
            }
        }
        if mand and sid not in manifest['mandatory_every_mock']:
            manifest['mandatory_every_mock'].append(sid)
        if ag:
            manifest['alternation_groups'].setdefault(ag, [])
            if sid not in manifest['alternation_groups'][ag]:
                manifest['alternation_groups'][ag].append(sid)
        # v2.11 rollups (Issue 2b) — group-presence, cadence, min-count:
        if grp:
            g = manifest['mandatory_groups'].setdefault(grp, {'members': [], 'min': 1})
            if sid not in g['members']:
                g['members'].append(sid)
        if win:
            manifest['cadence_windows'][sid] = win
        if mc:
            manifest['min_counts'][sid] = mc

    # v2.23 — round-trip the per-section AXIS_DISTRIBUTION block so a rebuilt manifest is
    # schema-identical to the write path. Each '=== SECTION: X ===' chunk may carry an
    # 'axis_distribution:' sub-block of indented 'key: <python-literal>' lines.
    _AXKEYS = {'recent_years', 'n_papers_recent', 'mocks_per_window', 'negative_rate',
               'axis1_per_paper', 'axis2_per_paper', 'axis3_per_paper', 'axis2_audit_mode'}
    for chunk in re.split(r'^=== SECTION:\s*', text, flags=re.M)[1:]:
        sec_name = chunk.split('===', 1)[0].strip()
        m = re.search(r'^axis_distribution:\s*$', chunk, flags=re.M)
        if not m:
            continue
        block = {}
        for ln in chunk[m.end():].splitlines():
            if not ln.startswith('  '):           # indented sub-lines only; stop at dedent
                if ln.strip() == '':
                    continue
                break
            km = re.match(r'\s+(\w+):\s*(.+)$', ln)
            if km and km.group(1) in _AXKEYS:
                block[km.group(1)] = _lit(km.group(2), km.group(2).strip())
        if block:
            manifest['axis_distribution'][sec_name] = block

    out = f'/mnt/user-data/outputs/{exam_code}_subtopic_manifest.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f'Rebuilt: {out} ({len(manifest["subtopics"])} ids, '
          f'{len(manifest["mandatory_every_mock"])} mandatory-every-mock, '
          f'{len(manifest["alternation_groups"])} alternation groups, '
          f'{len(manifest["mandatory_groups"])} group-presence, '
          f'{len(manifest["cadence_windows"])} cadence, '
          f'{len(manifest["min_counts"])} min-count)')
    if id_less:
        print(f'WARN: {len(id_less)} subtopic block(s) had NO subtopic_id and were '
              f'SKIPPED (cannot be joined by Step 6/7): {id_less[:8]}'
              f'{" ..." if len(id_less) > 8 else ""}. Mint ids in Step 5 or add them, '
              f'then re-run rebuild.')
    write_taxonomy_xlsx(manifest, exam_code)   # v2.24 — human-readable companion
    return out


def format_entry(e):
    # BUG-C04 fix (v2.3): option_format written as full dict per §14 BUG-B15 spec
    ofmt = e['option_format']
    if isinstance(ofmt, dict):
        ofmt_primary  = ofmt.get('primary', 'single_value')
        ofmt_recent   = ofmt.get('recent_format', ofmt_primary)
        ofmt_changed  = str(ofmt.get('changed_recently', False)).lower()
        ofmt_all      = ofmt.get('all_observed', [ofmt_primary])
    else:
        ofmt_primary = ofmt_recent = str(ofmt)
        ofmt_changed = 'false'
        ofmt_all     = [str(ofmt)]
    lines = [
        '', f'--- Subtopic: {e["subtopic"]} ---',
        # ── subtopic_id (v2.4 — CROSS-STEP JOIN KEY, the single source of truth) ──
        # subtopic_id is the STABLE machine identifier that Step 6 and Step 7 use to
        # join blueprint.json ↔ section_rules.md. It is minted HERE (Step 5) and
        # ONLY here. Downstream steps copy it verbatim and NEVER invent their own.
        # The display name ("--- Subtopic: X ---") is decorative and may be reworded
        # freely WITHOUT breaking the pipeline, because the id (not the name) is the
        # load-bearing join key. See §15 SUBTOPIC_ID CONTRACT for the full recipe.
        f'subtopic_id: {e["subtopic_id"]}',
        f'section: {e["section"]}', f'topic: {e["topic"]}',
        f'observed_count: {e["observed_count"]}', f'format: {e["format"]}',
        f'inherently_visual: {str(e.get("inherently_visual", False)).lower()}',
        f'option_format_primary: {ofmt_primary}',
        f'option_format_recent: {ofmt_recent}',
        f'option_format_changed_recently: {ofmt_changed}',
        f'option_format_all_observed: {ofmt_all}',
        f'OMML_required: {str(e["OMML_required"]).lower()}',
        f'negative_question_freq: {e["negative_question_freq"]}%',
        f'answer_type: {e.get("answer_type", "option")}',
        f'nat_freq: {e.get("nat_freq", 0)}%',
        f'answer_cardinality: {e.get("answer_cardinality", "single")}',
        f'msq_freq: {e.get("msq_freq", 0)}%',
        # v2.23 THREE-AXIS (CATEGORY B). observed_axis2 = PYQ-observed counts; axis2_capability
        # = faithful forms Step 6/7 may use; presentation_family = Step 7 menu key. Single-line
        # so rebuild_subtopic_manifest_from_section_rules() can round-trip them.
        f'observed_axis2: {e.get("observed_axis2", {})}',
        f'presentation_family: {e.get("presentation_family")}',
        f'axis2_capability: {e.get("axis2_capability", [])}',
        f'fill_in_blank: {e["fill_in_blank"]}',
        f'linked_group_size: {e["linked_group_size"]}',
        f'max_per_paper: {e.get("max_per_paper", 0)}',
        f'typical_per_paper: {e.get("typical_per_paper", 0)}',
        f'stem_word_count: min={e["stem_word_count"]["min"]} '
          f'max={e["stem_word_count"]["max"]} typical={e["stem_word_count"]["typical"]}',
        f'sub_type_label: {e["sub_type_label"]}',
        # ── CONCEPT_GROUP and QUESTION_MECHANIC (MANDATORY — Step 7 relies on these) ──
        # CONCEPT_GROUP: broad theme grouping (Step 7 resolve_concept_group priority #1).
        # QUESTION_MECHANIC: the normalised student task for CHECK D mechanic-collision.
        # Both MUST be written here. If absent → Step 7 falls to keyword-matching
        # fallback which FAILS for non-standard subtopic names → mechanic collisions
        # like synonym×2 or antonym×2 in the same mock go undetected.
        #
        # HOW TO DERIVE concept_group (exam-agnostic):
        #   Read the PYQ_STEM_PATTERNS template for this subtopic.
        #   Group all subtopics that share the same broad topic theme.
        #   Example: all "find missing number" variants → concept_group: missing_number
        #   Example: all "series" variants              → concept_group: series
        #   Use the SAME string for every subtopic in the same theme group.
        #
        # HOW TO DERIVE question_mechanic (exam-agnostic):
        #   Normalise the stem instruction to its atomic task:
        #     "opposite in meaning" / "ANTONYM"       → antonym
        #     "similar in meaning"  / "SYNONYM"       → synonym
        #     "find the error"                        → error_detection
        #     "improve the sentence" / "best replaces"→ sentence_improvement
        #     "one word substitution"                 → one_word_substitution
        #     "fill in the blank"                     → fill_in_blank
        #     "meaning of idiom/phrase"               → idiom
        #     "select the correctly spelt"            → spelling
        #     "active/passive voice"                  → voice
        #     "direct/indirect speech"                → narration
        #     (derive from PYQ_STEM_PATTERNS template — never hardcode exam names)
        #   Two subtopics with the SAME question_mechanic MUST NOT appear in
        #   the same mock (MockCreate mandate-7 CHECK D).
        #
        # SYNONYM vs ANTONYM: these are DIFFERENT mechanics. Both CAN appear in
        # one mock (one synonym Q + one antonym Q = different mechanics = allowed).
        # But two synonym Qs = SAME mechanic = BLOCKED by CHECK D. Always separate.
        f'concept_group: {e.get("concept_group") or _derive_concept_group(e)}',
        f'question_mechanic: {e.get("question_mechanic") or _derive_question_mechanic(e)}',
        f'form_key: {e.get("form_key") or _derive_form_key(e)}',                     # v2.24 (BV-10a HARD identity)
        f'collision_domain: {e.get("collision_domain") or _derive_collision_domain(e)}',  # v2.24 (default=section)
        # ── v2.10 MANDATE ROUND-TRIP: emit the three mandate fields as parseable lines
        #    so the manifest is reproducible from THIS FILE (not only from in-memory
        #    entries). mandate_every_mock defaults to the robust NOTE detector; an explicit
        #    e['mandate_every_mock'] overrides. alternation_group + min_per_series_window
        #    are authored fields ('none' when unset). write_subtopic_manifest AND
        #    rebuild_subtopic_manifest_from_section_rules read these back; Step 6 consumes
        #    the manifest (RULE M1/M2); Step 7 reads it (S3-17). These lines are also the
        #    HAND-EDIT point: set 'mandate_every_mock: true' / 'alternation_group: <name>'
        #    on a block and regenerate the manifest to change policy — no re-analysis.
        f'mandate_every_mock: {str(e.get("mandate_every_mock", _mandate_from_note(e.get("note_text") or e.get("NOTE") or ""))).lower()}',
        f'alternation_group: {e.get("alternation_group") or "none"}',
        f'min_per_series_window: {e.get("min_per_series_window") if e.get("min_per_series_window") not in (None, "") else "none"}',
        # v2.11 (Issue 2b) — two more round-trippable mandate fields:
        #   mandatory_group : a group name; a mock must contain >=1 member of the group
        #                     (group-presence, e.g. any one member of a 3D-solids group).
        #   min_count       : minimum questions of THIS subtopic per mock (>=k).
        f'mandatory_group: {e.get("mandatory_group") or "none"}',
        f'min_count: {e.get("min_count") if e.get("min_count") not in (None, "") else "none"}'
        # _derive_concept_group() and _derive_question_mechanic() are defined below.
        # They extract from PYQ_STEM_PATTERNS when not explicitly set in input data.
    ]
    for p in e.get('PYQ_STEM_PATTERNS', []):
        # BUG-C02 fix (v2.3): raw_count and years written — QV-11 uses years
        dep_tag = ' [DEPRECATED]' if p.get('deprecated') else ''
        lines += [
            f'  {p["id"]}: "{p["template"]}"',
            f'      approach: "{p.get("approach","")}"',
            f'      frequency: {p["frequency"]}%  confidence: {p["confidence"]}{dep_tag}',
            f'      raw_count: {p.get("raw_count", 0)}',
            f'      years: {p.get("years", [])}',
            f'      note_block: {p.get("note_block","never")}',
        ]
        if p.get('note_text'): lines.append(f'      note_text: "{p["note_text"][:120]}"')
        # ── SYNC fields: read by Step 7 sub-step 4b (UL-GATE) and sub-step 4c (ANCHOR-LOCK) ──
        # underline_required: true/false — Step 7 sub-step 4b reads this to determine
        #   whether stem_underline_ranges must be computed. Set true for subtopics
        #   where the stem instruction says "underlined" (idiom, sentence_improvement,
        #   error_detection, one_word_substitution, etc.).
        #   HOW TO DETECT from PYQ: if p['template'] contains 'underlined' or 'underline'
        #   → set underline_required: true. Otherwise false.
        _ul_req = 'true' if any(kw in p.get('template','').lower()
                                for kw in ['underlined','underline']) else 'false'
        lines.append(f'      underline_required: {_ul_req}')
        # anchor_option_required: true/false — Step 7 sub-step 4c reads this to determine
        #   whether an anchor option (e.g. "No error", "No improvement required") must
        #   be pinned to a fixed position during shuffle.
        #   HOW TO DETECT from PYQ: if p['template'] contains a phrase like
        #   "select option (N) if there is no error" or "if no improvement" + option number
        #   → set anchor_option_required: true and record anchor_position.
        import re as _re
        _anch_m = _re.search(
            r'select\s+option\s*\(?(\d+|[A-Da-d])\)?.*?(?:no error|no improvement|no change)',
            p.get('template',''), _re.IGNORECASE)
        _anch_req = 'true' if _anch_m else 'false'
        lines.append(f'      anchor_option_required: {_anch_req}')
        if _anch_m:
            # anchor_position: the 1-indexed position stated in the stem
            _pos_str = _anch_m.group(1)
            _pos_int = int(_pos_str) if _pos_str.isdigit() else (ord(_pos_str.upper())-64)
            lines.append(f'      anchor_position: {_pos_int}')
        lines.append('')
    # BUG-C01 fix (v2.3): is_inferred flag written alongside criteria
    calib = e.get('PYQ_DIFFICULTY_CALIBRATION', {})
    lines += ['PYQ_DIFFICULTY_CALIBRATION:']
    for lv in ['Simple','Medium','Hard']:
        c = calib.get(lv, {'criteria':'(inferred)','is_inferred':True})
        inf_tag = ' [INFERRED]' if c.get('is_inferred', True) else ''
        lines.append(f'  {lv}: "{c["criteria"]}"{inf_tag}')
    lines.append('')
    wo = e.get('wrong_option_structure', {})
    lines += ['wrong_option_structure:',
              f'  type: {wo.get("type","varied")}',
              f'  description: "{wo.get("description","")}"']
    if wo.get('fixed_option_texts'): lines.append(f'  fixed_option_texts: {wo["fixed_option_texts"]}')
    if wo.get('shared_pool_words'):  lines.append(f'  shared_pool_words: {wo["shared_pool_words"]}')
    lines.append('')
    if e.get('PYQ_NUMBER_RANGES'):
        lines.append('PYQ_NUMBER_RANGES:')
        for var,rng in e['PYQ_NUMBER_RANGES'].items():
            lines.append(f'  {var}: {{min:{rng["min"]},max:{rng["max"]},'
                         f'multiples_of:{rng.get("multiples_of","N/A")}}}')
        lines.append('')
    if e.get('PYQ_CONTEXT_POOL'):
        cp = e['PYQ_CONTEXT_POOL']
        cp_lines = ['PYQ_CONTEXT_POOL:',
                    f'  dominant: {cp.get("dominant",[])}',
                    f'  common: {cp.get("common",[])}',
                    f'  avoid: {cp.get("avoid",[])}',
                   ]
        # NEW v2.3: write recycled_datasets and ban_recycled if present
        if cp.get('recycled_datasets'):
            cp_lines.append(f'  recycled_datasets: {cp["recycled_datasets"]}')
            cp_lines.append(f'  ban_recycled: {str(cp.get("ban_recycled", True)).lower()}')
        cp_lines.append('')
        lines += cp_lines
    if e.get('PYQ_IMAGE_ANALYSIS'):
        ia = e['PYQ_IMAGE_ANALYSIS']
        lines += ['PYQ_IMAGE_ANALYSIS:',
                  f'  image_role: {ia.get("image_role","stem_only")}',
                  '  object_types:',
                  f'    dominant: {ia.get("object_types",{}).get("dominant",[])}',
                  f'    observed: {ia.get("object_types",{}).get("observed",[])}',
                  f'  transformation_types: {ia.get("transformation_types",[])}', '']
    # BUG-C05 fix (v2.3): paragraph_count and topic_domains now written
    if e.get('PYQ_PASSAGE_STRUCTURE'):
        ps = e['PYQ_PASSAGE_STRUCTURE']
        lines += ['PYQ_PASSAGE_STRUCTURE:',
                  f'  sub_format: {ps.get("sub_format","RC")}',
                  f'  word_range: {{min:{ps.get("word_range",{}).get("min",0)},'
                    f'max:{ps.get("word_range",{}).get("max",0)}}}',
                  f'  paragraph_count: {{typical:{ps.get("paragraph_count",{}).get("typical",1)}}}',
                  f'  topic_domains_observed: {ps.get("topic_domains",{}).get("observed",[])}',
                  f'  topic_domains_avoid: {ps.get("topic_domains",{}).get("avoid",[])}',
                  f'  q_type_distribution: {ps.get("q_type_distribution",{})}', '']
    return lines
```

---

## §6 — QUALITY VERIFICATION (QV-1 through QV-12)

```python
def run_qv(entries, taxonomy, progress):
    """
    BUG-A09 fix: QV-11 now uses global_max_year across all entries.
    BUG-B09 fix: QV-3 uses is_inferred bool from calibration dict.
    """
    results = {}
    ekeys   = {(e['section'],e['topic'],e['subtopic']):e for e in entries}

    # QV-1: Every taxonomy subtopic has an entry
    missing = [st['subtopic'] for sec,sts in taxonomy.items()
               for st in sts if (sec,st['topic'],st['subtopic']) not in ekeys]
    results['QV-1'] = ('WARN' if missing else 'PASS',
                        f'{len(missing)} missing: {missing[:5]}' if missing else 'All covered')

    # QV-1a: PYQ subtopics are in taxonomy
    pyq_subs = set(k[2] for k in ekeys)
    tax_subs = set(st['subtopic'] for sts in taxonomy.values() for st in sts)
    extra    = pyq_subs - tax_subs
    results['QV-1a'] = ('WARN' if extra else 'PASS',
                          f'In PYQ not taxonomy: {list(extra)[:5]}' if extra else 'OK')

    # QV-2: Frequency% sums to 100 per subtopic
    bad = [e['subtopic'] for e in entries if e.get('PYQ_STEM_PATTERNS') and
           abs(sum(p['frequency'] for p in e['PYQ_STEM_PATTERNS'])-100) > 1]
    results['QV-2'] = ('FAIL' if bad else 'PASS',
                        f'Sums!=100: {bad[:3]}' if bad else 'All=100%')

    # QV-3: BUG-B09 fix: check is_inferred bool, not string
    gap = [f'{e["subtopic"]}.{lv}' for e in entries if e['observed_count']>=5
           for lv in ['Simple','Medium','Hard']
           if e.get('PYQ_DIFFICULTY_CALIBRATION',{}).get(lv,{}).get('is_inferred',True)]
    results['QV-3'] = ('WARN' if gap else 'PASS',
                        f'Missing diff: {gap[:5]}' if gap else 'OK')

    # QV-4/5: option_format and wrong_option_structure classified
    no_fmt = [e['subtopic'] for e in entries if not e.get('option_format')]
    results['QV-4'] = ('FAIL' if no_fmt else 'PASS',
                        f'Missing: {no_fmt[:3]}' if no_fmt else 'OK')
    no_wo  = [e['subtopic'] for e in entries if not e.get('wrong_option_structure')]
    results['QV-5'] = ('FAIL' if no_wo else 'PASS',
                        f'Missing: {no_wo[:3]}' if no_wo else 'OK')

    # QV-5b: BUG-C07 fix (v2.3) — fixed_set must have non-empty fixed_option_texts
    bad_fixed = [e['subtopic'] for e in entries
                 if e.get('wrong_option_structure', {}).get('type') == 'fixed_set'
                 and not e.get('wrong_option_structure', {}).get('fixed_option_texts')]
    results['QV-5b'] = ('FAIL' if bad_fixed else 'PASS',
                         f'fixed_set missing texts: {bad_fixed[:3]}' if bad_fixed else 'OK')

    # QV-6: confidence accuracy
    bad_c = [f'{e["subtopic"]}.{p["id"]}' for e in entries
             for p in e.get('PYQ_STEM_PATTERNS',[])
             if p.get('confidence')=='observed' and p.get('raw_count',0)<3]
    results['QV-6'] = ('WARN' if bad_c else 'PASS',
                        f'Observed<3: {bad_c[:3]}' if bad_c else 'OK')

    # QV-7: templates have _VAR_ placeholders
    VAR_TOKENS = {'_NUM_','_P_','_R_%','_T_','_WORD_','_CODE_','_NOUN_','_LCLUS_',
                  '_YEAR_','_ORG_','_BLANK_','_NAME_','_SERIES_','_STMT_','_ADJ_'}
    no_var = [f'{e["subtopic"]}.{p["id"]}' for e in entries
              for p in e.get('PYQ_STEM_PATTERNS',[])
              if p['template'] not in ('(no PYQ observed)','(figural -- no text stem)')
              and not any(v in p['template'] for v in VAR_TOKENS)]
    results['QV-7'] = ('WARN' if no_var else 'PASS',
                        f'No _VAR_: {no_var[:3]}' if no_var else 'OK')

    # QV-8: OMML recovery >= 80%
    omml_iss = []
    for e in entries:
        if not e.get('OMML_required'): continue
        qs = progress.get((e['section'],e['topic'],e['subtopic']),[])
        om = [q for q in qs if q.get('omml_present')]
        ok = [q for q in om if not q.get('omml_failed')]
        if om and len(ok)/len(om) < 0.80:
            omml_iss.append(f'{e["subtopic"]}: {len(ok)}/{len(om)}')
    results['QV-8'] = ('WARN' if omml_iss else 'PASS',
                        f'OMML<80%: {omml_iss[:3]}' if omml_iss else 'OK')

    # QV-9: image clarity >= 80%
    img_iss = []
    for e in entries:
        if e.get('format')!='FIGURAL': continue
        ia  = e.get('PYQ_IMAGE_ANALYSIS') or {}
        tot = ia.get('images_analysed',0) + ia.get('images_unclear',0)
        if tot>0 and ia.get('images_unclear',0)/tot>0.20:
            img_iss.append(f'{e["subtopic"]}: {ia["images_unclear"]}/{tot}')
    results['QV-9'] = ('WARN' if img_iss else 'PASS',
                        f'Image<80%: {img_iss[:3]}' if img_iss else 'OK')

    # QV-10: PASSAGE subtopics have linked_group_size > 0
    no_grp = [e['subtopic'] for e in entries
               if e.get('format')=='PASSAGE' and e.get('linked_group_size',0)==0]
    results['QV-10'] = ('WARN' if no_grp else 'PASS',
                          f'Passage no groups: {no_grp}' if no_grp else 'OK')

    # QV-11: BUG-A09 fix -- global_max_year across all entries, not per-entry max
    all_years_global = [y for e in entries
                        for p in e.get('PYQ_STEM_PATTERNS',[])
                        for y in p.get('years',[]) if isinstance(y,int)]
    global_max = max(all_years_global) if all_years_global else None
    old_only = []
    if global_max:
        for e in entries:
            entry_yrs = [y for p in e.get('PYQ_STEM_PATTERNS',[])
                         for y in p.get('years',[]) if isinstance(y,int)]
            if entry_yrs and max(entry_yrs) < global_max - 1:
                old_only.append(e['subtopic'])
    results['QV-11'] = ('WARN' if old_only else 'PASS',
                          f'No recent data: {old_only[:3]}' if old_only else 'OK')

    # QV-12: no near-duplicate templates within a subtopic
    dups = []
    for e in entries:
        pats = [p['template'] for p in e.get('PYQ_STEM_PATTERNS',[])]
        for i in range(len(pats)):
            for j in range(i+1,len(pats)):
                if SequenceMatcher(None,pats[i],pats[j]).ratio()>0.90:
                    dups.append(f'{e["subtopic"]}: P{i+1}~P{j+1}')
    results['QV-12'] = ('WARN' if dups else 'PASS',
                          f'Near-dups: {dups[:3]}' if dups else 'OK')

    # QV-13 (v2.24) — MECHANIC INTEGRITY & COLLISION GUARD. Stops Step 5 from ever
    # QV-13 (v2.24.1) — MECHANIC IDENTITY INTEGRITY. FAIL severity, NO allowlist.
    # Reads the STAMPED fields (D5); never recomputes for the collision test. Step 5
    # cannot know N_mocks/batch_size, so it must reject ALL shared form_keys (D4/D7).
    from collections import defaultdict as _dd
    empty     = [e['subtopic_id'] for e in entries if not e.get('form_key')]
    unstamped = [e['subtopic_id'] for e in entries if 'form_key' not in e or e['form_key'] is None]
    # a REAL determinism check (D5): does a fresh derivation reproduce the stamped value?
    _pov = (progress.get('_meta', {}) or {}).get('section_prefix_overrides', {})
    _po  = build_section_prefix_map(sorted({e['section'] for e in entries}), _pov)
    nondet = []
    for e in entries:
        if not e.get('subtopic_id') or e.get('form_key') is None:
            continue
        _tpl = ' '.join(p.get('template','') for p in e.get('PYQ_STEM_PATTERNS', []))
        _fk  = derive_mechanic(e['section'], e.get('subtopic') or e.get('sub_type_label',''),
                               e.get('sub_type_label'), _tpl, e.get('format','TEXT'),
                               e['subtopic_id'], _po)['form_key']
        # a curator override legitimately makes the stamped value differ from a bare
        # derivation; only flag when NO override explains it.
        _ov  = (_OVERRIDES or {}).get('subtopic_overrides', {}).get(e['subtopic_id'], {})
        if _fk != e['form_key'] and 'form_key' not in _ov and e['form_key'] != slugify(e['subtopic_id']):
            nondet.append(e['subtopic_id'])
    dom = _dd(lambda: _dd(list))
    for e in entries:
        dom[e.get('collision_domain')][e.get('form_key')].append(e['subtopic_id'])
    collisions = [f'{d}:{fk}={sorted(ids)}'
                  for d, fks in dom.items() for fk, ids in fks.items() if len(ids) > 1]
    # a bare family token is illegal unless this exam declared the owning template set
    def _decl(e):
        _ov = _OVERRIDES or {}
        a = _ov.get('template_sets_by_section', {}).get(e['section'], _ov.get('template_sets'))
        return ['verbal','reasoning'] if a is None else a
    # A family-named form_key is illegal ONLY when it is a FOREIGN token, i.e. it did NOT
    # come from the subtopic's own identity base. Under v2.24.1 form_key == base for a
    # subtopic legitimately named like a family (e.g. a real verbal "Analogy"); that is not
    # contamination and must NOT FAIL. A foreign token can only arrive via a curator override.
    illegal = [e['subtopic_id'] for e in entries
               if e.get('form_key') in _ALL_FAMILY_NAMES
               and _TEMPLATE_SET.get(e.get('form_key')) not in _decl(e)
               and e['form_key'] != _identity_base(e.get('subtopic') or e.get('sub_type_label',''),
                                                    e.get('subtopic_id'))]
    same_as_domain = [e['subtopic_id'] for e in entries
                      if e.get('form_key') and e['form_key'] == e.get('collision_domain')]
    import re as _re
    bad_shape = [e['subtopic'] for e in entries
                 if len(e['subtopic']) > 60 or e['subtopic'].strip().endswith('?')
                 or _re.match(r'^\s*(what|which|how|why|find|choose|select|the average)\b',
                              e['subtopic'].strip(), _re.I)]
    if empty or unstamped or nondet or collisions or illegal or same_as_domain:
        results['QV-13'] = ('FAIL',
            f'empty={empty[:3]} unstamped={unstamped[:3]} nondeterministic={nondet[:3]} '
            f'collisions={collisions[:3]} illegal_family_token={illegal[:3]} '
            f'equals_domain={same_as_domain[:3]}')
    else:
        results['QV-13'] = ('PASS', f'{len(entries)} form_keys: non-empty, deterministic, '
                                    f'unique per collision_domain, no foreign family tokens')
    # QV-13a — NAME SHAPE. Advisory only; split so an editorial nit can neither mask nor
    # be masked by an identity failure.
    results['QV-13a'] = (('WARN', f'{len(bad_shape)} long/question-shaped names: {bad_shape[:3]}')
                         if bad_shape else ('PASS', 'OK'))

    return results

def print_qv(results):
    print('\n=== Quality Verification Results ===')
    icons = {'PASS':'v','WARN':'!','FAIL':'X'}
    all_ok = True
    for check,(status,detail) in results.items():
        print(f'  {icons[status]} {check}: {status} -- {detail}')
        if status=='FAIL': all_ok = False
    print(f'\n{"All checks passed." if all_ok else "FAIL checks must be resolved."}')
    return all_ok
```

---

## §7 — EDGE CASES (EC-1 through EC-15)

```
EC-1:  INCOMPLETE OPTIONS (<options_count extracted)
  1. E-5 OMML: may have formula in option slot.
  2. E-4 q_roles: may be image-only option.
  3. Still <N: q_incomplete=True, exclude from template extraction.

EC-2:  STEM CONTENT AFTER OPTIONS
  Apply E-6 to detect NOTE. If NOTE: record. If not: discard and log.

EC-3:  IMAGE ROLE CLASSIFICATION
  stem_and_options -> format=FIGURAL, option_format=image_only
  stem_only        -> format=FIGURAL, text options
  Determined from E-4 q_roles. S4-3 computes dominant_role from data.

EC-4:  SHARED DI TABLE VS INDEPENDENT TABLES
  E-7 Method 1: shared table (>=90% match) -> linked group (linked_group_size=N).
  Own table: not linked (linked_group_size=0). Both valid.

EC-5:  HINDI / REGIONAL LANGUAGE
  E-6: NOTE_PAT uses non-raw string with actual \u escapes (fixed BUG-A14 related).
  E-10: factual mode skips proper-noun stripping (capitalisation unreliable).

EC-6:  MARKS VARIATION (multi-mark exams — e.g., 1-mark and 2-mark questions)
  Triggered when: exam has questions carrying different marks (read from _meta marks_per_q dict).
  score_difficulty called with marks=q_marks.
  Difficulty thresholds scale: simple_threshold = 4 + (marks-1).
  Exam-agnostic: marks_per_q read from section_rules.md EXAM_STRUCTURE block.
  No exam names hardcoded — any exam with multi-mark Qs triggers this edge case.

EC-7:  MULTI-SELECT QUESTIONS (MSQ)  [v2.5 — dormant unless multi_select_allowed]
  q['is_msq']=True detected in presorted mode via detect_is_msq() (option-shape
  aware — see EC-A). Synthesis aggregates per-question is_msq into a per-SUBTOPIC
  answer_cardinality ∈ {single, multi} (CATEGORY B) — the Step 7 dispatch unit — plus
  msq_freq%. A subtopic is treated as uniformly single- or multi-answer
  (whole-subtopic mode), so the downstream per-mock allocation schema is unchanged.
  Step 7 GENERATES MSQ for multi subtopics per the answer_cardinality contract (it no
  longer skips them). k-mode/k and per-type marking come from the Exam Pattern doc
  (PYQ has no key → k is unextractable), carried in EXAM_STRUCTURE. When
  multi_select_allowed=false, is_msq is always False and this whole path is inert.

EC-A:  STATEMENT-COMBINATION MCQ vs MSQ (false-positive guard) [v2.5]
  ROOT CAUSE of the v2.4 mis-tag: the old is_msq regex matched "Which is/are
  correct?" — but EC-9 statement-combination questions use that exact phrasing and
  are SINGLE-answer (you pick one combo option). The forgery-resistant signal is
  OPTION SHAPE: if the options are predominantly combination-labels (Only N /
  Both N and M / Neither…nor / "N and M" / None of / All of the above), the
  question is a statement-combination MCQ and is NEVER MSQ, regardless of stem
  wording. detect_is_msq() requires a genuine multi-select instruction AND
  non-combo options. Validated empirically against real docx fixtures (a genuine
  statement MSQ with ordinary options stays MSQ; a combo-label MCQ stays MCQ).

EC-8:  ASSERTION-REASON FORMAT
  Template: "Assertion (A): _STMT_ Reason (R): _STMT_"
  wrong_option_structure: fixed_set. fixed_option_texts recorded exactly.

EC-9:  STATEMENT-COMBINATION FORMAT
  Template: "Consider the following statements: 1. _STMT_ 2. _STMT_ Which is/are correct?"
  Note: spaces (not \n) because stems are space-joined from paragraphs.
  E-11: options classified as sentence_label.

EC-10: NON-REPRINTED PASSAGE (proximity detection)
  Detect during extraction: paragraph >100 words before run of short-stem Qs.
  Link following Qs to that passage group.

EC-11: FILL-IN-BLANK STEMS
  blank_pos recorded. Template preserves _BLANK_. Wrong option: same_category.

EC-12: NEGATIVE QUESTIONS (NOT/INCORRECT/EXCEPT/FALSE/WRONG)
  is_negative=True. score +1. negative_question_freq% recorded for Step 7.

EC-13: MATCHING TYPE QUESTIONS
  Template: "Match _ITEM_ with _ITEM_"
  option_format: value_pair_quad.

EC-14: YEAR-WISE PATTERN DRIFT
  deprecated=True (set in generate_templates) if pattern absent from last 2 years.
  confidence='observed_recent' if ONLY in last 2 years.
  Step 7 EC-14: observed_recent weight x1.5; deprecated weight x0.1.

EC-15: CROSS-SUBJECT QUESTIONS
  Trust the docx taxonomy heading — it is always authoritative in presorted papers.
  When a question's content spans multiple subtopics (e.g. arithmetic + DI),
  the heading under which it appears is the correct classification.
  Step 7 ignores any secondary subtopic signal.

EC-16: THREE-AXIS CLASSIFICATION (v2.23 — see AXIS CLASSIFIER v1.0)
  Every question is tagged on THREE orthogonal axes by the shared classifier
  (tag_axes): Axis-1 stimulus (TEXT|FIGURAL|PASSAGE|DI), Axis-2 stem structure
  (the exclusive 8-class ladder), Axis-3 mechanism (MCQ|MSQ|NAT); negative polarity
  is an orthogonal flag (is_negative), never an Axis-2 class.
  EXCLUSIVITY: first-match-wins; LINKED is a GATE decided by linked_group_id (shared
  stimulus), not phrasing — so an assertion-reason inside a passage is LINKED. SEQUENCE
  is ordered ABOVE STATEMENT (the operation is arranging). DIRECT is the residual.
  OVERLAP EXAMPLES resolved deterministically: "which pair is NOT matched" → MATCH +
  is_negative; "arrange the following statements" → SEQUENCE (not STATEMENT); a passage's
  A-R sub-question → LINKED (not ASSERTION_REASON).
  This classifier is the SINGLE SOURCE OF TRUTH — Step 8 re-tags GENERATED questions with
  the identical functions so the PYQ target and the generated output are comparable.
```

---

## §8 — BATCH EXECUTION AND SESSION FLOW

### S8-1 — Batch design

```
★★★ CRITICAL RULE — BATCH SIZE = 3, STRICTLY ENFORCED, NO EXCEPTIONS ★★★

BATCH_SIZE = 3  # papers per batch — NON-NEGOTIABLE. Cannot be changed by any instruction.

Processing 3 papers together in one go is MANDATORY.
Analysing more than 3 papers without pausing for user confirmation is STRICTLY PROHIBITED.
Analysing all files in one go without batching is STRICTLY PROHIBITED.
No user instruction, no efficiency argument, no time pressure overrides this rule.

Why this rule is critical:
  1. Each batch delivers an incremental analysis_progress.json — user has a safe restore point.
  2. User can review progress after every 3 papers and catch errors early.
  3. Prevents session timeouts from losing all work on large paper sets
   (large exams with many years × shifts can easily exceed 100 papers).
  4. Ensures the user is always in control and can stop/resume at any point.

MANDATORY AFTER EVERY BATCH OF 3:
  1. Save updated progress to analysis_progress.json
  2. Deliver analysis_progress.json as downloadable chat file (present_files)
  3. Print batch summary (papers processed, cumulative count, subtopic coverage)
  4. Show Options A/B (say "continue" OR download+upload+fresh chat)
  5. WAIT for user confirmation — do NOT auto-proceed under any circumstances

ACCEPTED CONTINUE SIGNALS: "continue" / "go" / "next" / "ok" / "proceed" / "yes"
PROHIBITED: auto-proceeding without user confirmation, even if user said "process all" earlier.
  If user says "process all X papers at once" → REFUSE. Reply:
    "Processing all papers at once is strictly prohibited. I will process 3 papers per batch
     and ask for your confirmation after each batch. This ensures progress is saved safely
     and you stay in control. Say 'continue' after each batch to proceed."

Processing order: latest year first → latest date within year first → session ascending.
  e.g. latest year's session 1 → session 2 → session 3 → prior date session 1 → ...
                    → prior year → ... → earliest year last
  (session = Shift/Slot/Phase/Paper/Session per exam_config.json session_keyword)
Rationale: if processing stops early, section_rules.md reflects the most recent
  exam patterns — exactly what Step 7 needs to generate up-to-date questions.

After ALL papers are processed (last batch):
  1. Save final progress
  2. Enforce minimum year coverage check (§1-6) — HALT if not met
  3. Auto-run synthesis immediately
  4. Run QV-1 through QV-12 (plus QV-5b)
  5. Deliver section_rules.md + analysis_progress.json + analysis_summary.md
     as downloadable chat files via present_files (no Drive upload)
  6. No separate session needed

Session flow:
  Session 1: reads Drive folder → sorts all papers recency-first → processes batch #1-3
             (most recent 3 papers, latest year first) → delivers progress.json → shows Options A/B
  Session 2 option A: user says "continue" in same session → processes #4-6 → shows Options A/B
  Session 2 option B: user downloads progress.json from chat → uploads to [ExamCode]
             project knowledge (replacing prior version) → opens fresh chat →
             types: PYQExtract PYQ: <<same Drive link>> → processes #4-6
  ...
  Session N: processes last batch → §1-6 coverage check → synthesises → delivers final outputs
```

### S8-2 — Main execution loop

```python
BATCH_SIZE = 3

def sort_papers_recency_first(paper_list):
    """
    Sort PYQ papers: latest year first, then latest date within year first,
    then session number ascending within same date (session 1 before session 2).

    Extracts year and date from filename using the common naming convention:
      [ExamCode]_DD-Mon-YYYY_<session_keyword>-N.docx
    session_keyword is read from exam_config.json (Shift/Slot/Phase/Paper/Session).

    For filenames without a recognizable date: sorted last, alphabetically.

    Examples (sorted order, using session_keyword='Shift'):
      [ExamCode]_26-Sep-2025_Shift-1 → year=2025, date=2025-09-26, session=1 (first)
      [ExamCode]_26-Sep-2025_Shift-2 → year=2025, date=2025-09-26, session=2
      [ExamCode]_12-Sep-2025_Shift-1 → year=2025, date=2025-09-12, session=1
    Examples (using session_keyword='Slot'):
      [ExamCode]_09-Sep-2024_Slot-1  → year=2024, date=2024-09-09, session=1
      [ExamCode]_13-Aug-2021_Slot-2  → year=2021, date=2021-08-13, session=2
    """
    MONTH_MAP = {
        'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
        'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12
    }

    def sort_key(paper):
        name = paper['name']
        # Match: DD-Mon-YYYY and Shift-N
        date_m  = re.search(r'(\d{2})-([A-Za-z]{3})-(\d{4})', name)
        # v2.16 RIGID-1: uses SESSION_RE (dynamic from exam_config.json session_keyword)
        shift_m = SESSION_RE.search(name)

        if date_m:
            day   = int(date_m.group(1))
            month = MONTH_MAP.get(date_m.group(2).lower(), 0)
            year  = int(date_m.group(3))
        else:
            # No date found — try year-only
            year_m = re.search(r'(20\d{2})', name)
            year  = int(year_m.group(1)) if year_m else 0
            month = 0
            day   = 0

        shift = int(shift_m.group(1)) if shift_m else 99

        # Sort key: year DESC, month DESC, day DESC, shift ASC
        # Negate year/month/day for descending; shift stays ascending
        return (-year, -month, -day, shift)

    return sorted(paper_list, key=sort_key)


def deliver_batch_summary(batch, progress, batch_num, papers_done, total_all, exam_code):
    """Print per-batch delivery summary to chat. Called after each batch of 3 papers."""
    meta       = progress.get('_meta', {})
    total_qs   = meta.get('total_questions', 0)
    n_observed = sum(1 for k,v in progress.items() if isinstance(k,tuple) and len(v)>=3)
    n_inferred = sum(1 for k,v in progress.items() if isinstance(k,tuple) and 1<=len(v)<3)
    n_omml_fail = sum(1 for k,qs in progress.items()
                      if isinstance(k,tuple)
                      for q in qs if q.get('omml_failed'))
    n_unclear   = sum(1 for k,qs in progress.items()
                      if isinstance(k,tuple)
                      for q in qs if q.get('image_clarity')=='unclear')

    print(f"\n=== Batch {batch_num} complete ===")
    for p in batch:
        name = p['name']
        yr   = extract_year_from_filename(name) or '?'
        sh   = extract_shift_from_filename(name)
        print(f"  ✓ {name} | {yr} {sh}")
    print(f"\n Cumulative : {papers_done} / {total_all} papers")
    print(f" Subtopics  : {n_observed} observed | {n_inferred} sparse")
    print(f" Total Qs   : {total_qs}")
    if n_omml_fail: print(f" OMML issues: {n_omml_fail} questions with failed OMML")
    if n_unclear:   print(f" Unclear imgs: {n_unclear} figural images unclear")
    print("========================")
    # Deliver progress.json as downloadable chat file after every batch
    progress_path = f'/mnt/user-data/outputs/{exam_code}_analysis_progress.json'
    present_files([progress_path])
    # present_files makes the file downloadable in chat (Claude tool).

def run_batch_loop(pyq_doc_paths, exam_code, time_per_q, marks_per_q,
                   options_count, multi_select, progress,
                   coverage_mode='mandatory_5yr', recent_5_years=None,
                   available_years=None):
    """
    Core loop: process papers in batches of BATCH_SIZE (always 3 — non-negotiable).
    pyq_doc_paths: list of dicts — {source: 'gdrive'|'local', id/path, name}
    Papers already in progress._meta.papers_processed are skipped.
    Processing order: latest year first, then latest date, then shift ascending.
    coverage_mode, recent_5_years, available_years: passed from §1-6 check.
    ★ NEVER process more than BATCH_SIZE papers without pausing for user confirmation.
    """
    done_ids = set(progress.get('_meta', {}).get('papers_processed', []))

    # Sort ALL papers recency-first, then filter out already-done ones
    # Sorting before filtering preserves the correct order for pending papers
    all_sorted = sort_papers_recency_first(pyq_doc_paths)
    pending    = [p for p in all_sorted if make_paper_id(p['name']) not in done_ids]

    total_done = len(done_ids)
    total_all  = total_done + len(pending)

    if not pending:
        print(f"All {total_all} paper(s) already processed. Running synthesis.")
        run_synthesise(exam_code, progress,
                       coverage_mode=coverage_mode,
                       recent_5_years=recent_5_years,
                       available_years=available_years)
        return

    print(f"Papers done: {total_done} / {total_all}. Pending this session: {len(pending)}")

    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch = pending[batch_start : batch_start + BATCH_SIZE]
        batch_num = (total_done // BATCH_SIZE) + (batch_start // BATCH_SIZE) + 1

        print(f"\n=== Batch {batch_num}: processing {len(batch)} paper(s) ===")

        for paper_ref in batch:
            paper_id  = make_paper_id(paper_ref['name'])
            print(f"  Processing: {paper_ref['name']}")

            # Fetch file content depending on source
            if paper_ref['source'] == 'gdrive':
                # Download from Google Drive to temp path, then process
                local_path = f'/home/claude/pyq_temp/{paper_ref["name"]}'
                os.makedirs('/home/claude/pyq_temp', exist_ok=True)
                gdrive_download_file(paper_ref['id'], local_path)  # Drive MCP tool
            else:
                local_path = paper_ref['path']

            process_pyq_paper(local_path, paper_id, exam_code,
                               time_per_q, marks_per_q, options_count,
                               multi_select, progress)

        # Save and deliver after each batch
        progress_path    = save_progress(progress, exam_code)
        papers_now_done  = len(progress.get('_meta',{}).get('papers_processed',[]))
        papers_remaining = total_all - papers_now_done

        deliver_batch_summary(batch, progress, batch_num, papers_now_done, total_all, exam_code)

        if papers_remaining == 0:
            print(f"\nAll {total_all} papers complete. Running synthesis now...")
            run_synthesise(exam_code, progress,
                           coverage_mode=coverage_mode,
                           recent_5_years=recent_5_years,
                           available_years=available_years)
            return

        # More papers remain — pause for user.
        # The for loop STOPS here after each batch (break).
        # Next batch only runs if user says 'continue' in same session,
        # OR user uploads progress.json and starts a fresh chat.
        print(f"\n{papers_remaining} paper(s) remaining.")
        print(f"Options:")
        print(f"  A) Say 'continue' to process the next batch now in this same session.")
        print(f"  B) Download analysis_progress.json above, then upload it to")
        print(f"     [ExamCode] project knowledge (replace prior version),")
        print(f"     open a fresh chat, and type:")
        print(f"     PYQExtract {exam_code}  PYQ: <<same Drive link>>")
        print(f"  Both options are valid. Progress is in memory — option A needs no upload.")

        # ══ BATCH STOP -- END THE RESPONSE ═══════════════════════
        # *** Write nothing more. Generate nothing more. ***
        # This is the same class of rule as PYQAnalyse S3-4a and
        # MockCreate MANDATE 1 STEP 6.
        # CROSS-FRAMEWORK FAILURE: PYQAnalyse SSC CGL Tier 2 --
        # Claude auto-advanced from Batch 1 to Batch 2 in the same
        # response because no "END THE RESPONSE" prose existed.
        # The Python `break` stops the loop but does NOT stop Claude
        # from writing content after the loop. This prose block does.
        break  # STOP after each batch — do not auto-proceed to next batch

def make_paper_id(filename):
    """Stable unique ID from filename (without extension)."""
    return os.path.splitext(os.path.basename(filename))[0]
```

### S8-3 — Batch delivery format

```
After each batch of 3 papers, Claude prints in chat:

"=== Batch [N] complete ===
 Papers processed this batch:
   ✓ [filename_1] | [Y] S[N] | [N] Qs | [N] groups | [N] figural imgs
   ✓ [filename_2] | [Y] S[N] | [N] Qs | [N] groups | [N] figural imgs
   ✓ [filename_3] | [Y] S[N] | [N] Qs | [N] groups | [N] figural imgs

 Cumulative progress : [done] / [total] papers
 Subtopics with data: [N] observed | [N] inferred | [N] absent
 Total Qs accumulated: [N]

 Data quality snapshot:
   OMML issues   : [N] questions with failed OMML nodes (if any)
   Unclear images: [N] figural images too small/blurry to classify (if any)
 ========================"

Then present_files: [ExamCode]_analysis_progress.json
  (EXACTLY 1 file — S11-3 per-batch closed set. No other files.)

If more papers remain:
  (See S11-1 PART C for exact continue prompt text.)
  Options: say "continue" in same session, OR download progress.json and resume in fresh chat.
  Wait for user: "continue" / "go" / "next" are all valid.
  Claude does NOT auto-proceed — user confirms before each batch.
  *** After printing Options A/B: END THE RESPONSE. Write nothing more. ***

If this was the last batch:
  → auto-synthesise (see S8-4). No separate session needed.
```

### S8-4 — Auto-synthesise on completion (no separate final session)

```python

def write_analysis_summary(entries, progress, exam_code):
    """Write human-review audit trail to analysis_summary.md."""
    from datetime import datetime
    meta    = progress.get('_meta', {})
    n_pap   = len(meta.get('papers_processed',[]))
    n_qs    = meta.get('total_questions',0)
    years   = sorted(meta.get('years_processed',[]))
    out     = f'/mnt/user-data/outputs/{exam_code}_analysis_summary.md'

    lines = [
        f'# {exam_code} Analysis Summary',
        f'Generated: {datetime.now().isoformat()[:19]} | Papers: {n_pap} | Questions: {n_qs} | Years: {years}',
        '',
        '## HUMAN REVIEW REQUIRED',
        '',
        '### Inferred patterns (1-2 occurrences — verify):',
    ]
    for e in entries:
        for p in e.get('PYQ_STEM_PATTERNS',[]):
            if p.get('confidence')=='inferred':
                lines.append(f'  {e["subtopic"]} {p["id"]}: "{p["template"][:60]}" '
                             f'(seen {p["raw_count"]} times, years: {p.get("years",[])})')

    lines += ['', '### Deprecated patterns (absent from last 2 years):']
    for e in entries:
        for p in e.get('PYQ_STEM_PATTERNS',[]):
            if p.get('deprecated'):
                lines.append(f'  {e["subtopic"]} {p["id"]}: "{p["template"][:60]}" '
                             f'(last seen: {max(p.get("years",[0]))})')

    lines += ['', '### Absent subtopics (Zero-PYQ — no PYQ data — Step 7 uses training knowledge):',
              '### SYNC NOTE: Step 6 (Framework_Blueprint) calls these "Zero-PYQ" subtopics.',
              '### r_avg = 0.0 for all entries below. Step 6 places them in zero_pyq_rotation{}.']
    for e in entries:
        if e.get('observed_count',0)==0:
            lines.append(f'  {e["subtopic"]}')

    lines += ['', '### Figural vision analysis summary:']
    for e in entries:
        ia = e.get('PYQ_IMAGE_ANALYSIS')
        if ia:
            lines.append(f'  {e["subtopic"]}: {ia.get("images_analysed",0)} analysed, '
                        f'{ia.get("images_unclear",0)} unclear')

    lines += ['', '## STATISTICS',
              f'Total subtopics: {len(entries)}',
              f'Observed (>=3 Qs): {sum(1 for e in entries if e["observed_count"]>=3)}',
              f'Sparse   (1-2 Qs): {sum(1 for e in entries if 1<=e["observed_count"]<3)}',
              f'Absent   (0 Qs)  : {sum(1 for e in entries if e["observed_count"]==0)}',
              '',
              '### Top 10 subtopics by observed_count:']
    for e in sorted(entries, key=lambda x:-x['observed_count'])[:10]:
        lines.append(f'  {e["subtopic"]}: {e["observed_count"]} Qs')

    with open(out,'w',encoding='utf-8') as f: f.write('\n'.join(lines))
    print(f'Written: {out}')
    return out

def run_synthesise(exam_code, progress, coverage_mode='mandatory_5yr',
                    recent_5_years=None, available_years=None):
    """
    Called automatically when all papers are processed.
    Runs synthesis, QV checks, generates section_rules.md and summary.
    User never needs to type --synthesise separately.

    Enforces mandatory 5-year coverage rule (§1-6) before proceeding.
    coverage_mode   : 'mandatory_5yr' (standard) | 'no_pyq' | 'no_year_info'
    recent_5_years  : list of the most recent N years available (N = min(5, available))
    available_years : full sorted list of all years in Drive/uploads
    """
    # §1-6 MANDATORY 5-YEAR COVERAGE ENFORCEMENT
    processed_years = sorted(set(progress.get('_meta', {}).get('years_processed', [])),
                             reverse=True)

    # If called via --synthesise ALL (recent_5_years=None), reconstruct from progress.
    # We cannot re-scan Drive here (no pyq_doc_paths available), so derive
    # available_years from what was actually processed.
    _recent_5 = recent_5_years
    _avail    = available_years
    if coverage_mode == 'mandatory_5yr' and _recent_5 is None:
        # Reconstruct: assume available years == processed years (conservative)
        _avail    = sorted(processed_years, reverse=True)
        _recent_5 = _avail[:5]

    # Skip check for Scenario B (no PYQ) or no-year-info mode
    if coverage_mode in ('no_pyq', 'no_year_info'):
        pass  # No coverage check needed — proceed to synthesis
    elif coverage_mode == 'mandatory_5yr':
        n_required = min(5, len(_avail)) if _avail else 0
        missing = [y for y in (_recent_5 or []) if y not in processed_years]
        if len(processed_years) < n_required or missing:
            print("\n★ SYNTHESIS BLOCKED: 5-YEAR COVERAGE RULE NOT MET ★")
            print(f"  Required : {n_required} most recent year(s): {(_recent_5 or [])[:n_required]}")
            print(f"  Processed: {processed_years}")
            if missing: print(f"  Missing  : {sorted(missing, reverse=True)}")
            print("  ACTION   : Process papers from the missing year(s) before synthesising.")
            print("             This rule cannot be waived. No exception applies here.")
            return   # HALT — do not write section_rules.md

    print("\n=== Auto-synthesis starting ===")
    print("Building taxonomy from accumulated PYQ data...")

    # Build taxonomy from two sources (merged, Analysis docs win for names):
    # Source 1: progress keys (always available — built during extraction)
    taxonomy = {}
    for key in progress:
        if isinstance(key, tuple) and len(key) == 3:
            section, topic, subtopic = key
            taxonomy.setdefault(section, [])
            if not any(e['subtopic'] == subtopic for e in taxonomy[section]):
                taxonomy[section].append({'topic': topic, 'subtopic': subtopic})

    # Source 2: Analysis docs (if present in project/uploads — adds absent subtopics
    # that have no PYQ data, ensuring QV-1 can detect missing coverage correctly)
    for search_dir in ['/mnt/project/', '/mnt/user-data/uploads/']:
        for f in glob.glob(os.path.join(search_dir, '*.docx')):
            bn = os.path.basename(f).lower()
            if 'analysis' in bn or 'analyse' in bn:
                try:
                    extract_taxonomy_from_analysis_doc(f, taxonomy)
                except Exception:
                    pass  # Analysis doc read failure is non-fatal during synthesis

    # Synthesise every subtopic
    all_entries = []
    # v2.8: nat_allowed (PARAMETER 11) gates the NAT detection axis. Read once from _meta
    # (default False ⇒ answer_type always 'option' ⇒ non-NAT exams behave exactly as v2.7).
    _nat_allowed = bool(progress.get('_meta', {}).get('nat_allowed', False))
    for section, entries in taxonomy.items():
        for e in entries:
            key       = (section, e['topic'], e['subtopic'])
            questions = progress.get(key, [])
            figural   = None
            if any(q.get('image_role','none') != 'none' for q in questions):
                figural = aggregate_figural(questions, {})
            entry = synthesise_subtopic(section, e['topic'], e['subtopic'],
                                         questions, progress, figural_data=figural,
                                         nat_allowed=_nat_allowed)
            all_entries.append(entry)

    # ── v2.20 TAXONOMY SYNC (Fix A): ensure manifest covers COMPLETE vocabulary ──
    # After PYQ-based entries are built, synchronise with the exam's approved
    # taxonomy. Any taxonomy-defined subtopic NOT already in all_entries gets a
    # zero-PYQ scaffold entry appended. This makes the manifest COMPLETE by
    # construction — Step 6 can never encounter an unresolvable subtopic.
    print("\n--- Taxonomy sync (v2.20) ---")
    zero_pyq_scaffolds, sync_log = taxonomy_sync_entries(all_entries, exam_code)
    if zero_pyq_scaffolds:
        all_entries.extend(zero_pyq_scaffolds)
        # Also add to taxonomy dict so QV-1 coverage sees them
        for scaffold in zero_pyq_scaffolds:
            sec = scaffold['section']
            taxonomy.setdefault(sec, [])
            if not any(e['subtopic'] == scaffold['subtopic'] for e in taxonomy[sec]):
                taxonomy[sec].append({'topic': scaffold['topic'],
                                      'subtopic': scaffold['subtopic']})
    for line in sync_log:
        print(line)
    print(f"Taxonomy sync: {len(zero_pyq_scaffolds)} zero-PYQ scaffold entries added.")
    print(f"Total subtopics after sync: {len(all_entries)}")
    print("--- End taxonomy sync ---\n")

    # v2.24.5: AUTOMATIC zero-PYQ format inference. Runs on the full entry set (PYQ + scaffolds)
    # so same-topic siblings are visible; refines ONLY zero-PYQ entries in place (name keyword →
    # FIGURAL; unanimous sibling format inherited; ≥2/3 NAT/MSQ inherited) before ids/stamp/QV/
    # writers see them. No prompt — every change is logged for the audit trail.
    apply_zero_pyq_format_inference(all_entries)

    # ── v2.24.1 DERIVE-ONCE PIPELINE (§8-4 order): mint id → merges → stamp → QV ──
    # (subtopic_merges is keyed by subtopic_id, so ids MUST be minted before merging.)
    # subtopic_id is minted HERE (moved out of write_section_rules) so QV-13 and every
    # writer read the SAME id and the SAME stamped mechanic axes. stamp_mechanic_axes()
    # asserts form_key uniqueness before anything is written — a shared form_key can no
    # longer reach Step 6 as a silent, two-steps-later HALT.
    _stamp_meta = {'section_prefix_overrides':
                   (progress.get('_meta', {}) or {}).get('section_prefix_overrides', {})}
    mint_subtopic_ids(all_entries, _stamp_meta)                    # ids first (merges join on them)
    all_entries = apply_subtopic_merges(all_entries, exam_code)    # D7 (no-op if none declared)
    stamp_mechanic_axes(all_entries, exam_code, _stamp_meta)

    # QV checks
    qv_results  = run_qv(all_entries, taxonomy, progress)
    qv_ok       = print_qv(qv_results)

    # ── S-SECMAP: DERIVE SECTION↔SUBJECT MAPPING AND UPDATE EXAM_CONFIG ──────
    # v2.24.9 GAP FIX (BUG 1 of 4). After classification completes, derive which
    # taxonomy Subjects appear in which OTS sections and write the mapping as
    # sections[].subjects in exam_config.json. This enables Step 6's resolver
    # (S2-1b) to handle cross-subject exams (e.g. IIT JAM, CSIR NET) where a
    # single Subject spans multiple OTS sections. Without this, S2-1b falls to
    # SEC-4 HARD STOP on any exam where section names ≠ manifest Subject names
    # AND there are multiple OTS sections.
    #
    # 3-stage rule:
    #   STAGE 1 (OBSERVE): for each (section, subject) pair in classified PYQ data,
    #     record which subjects appeared in which Q-ranges (sections).
    #   STAGE 2 (AUGMENT): cross-subject sections (≥2 subjects) pool all subjects
    #     and assign the union to every cross-subject section — covers sampling gaps.
    #   STAGE 3 (FALLBACK): any taxonomy subject not mapped to ANY section by Stage 1
    #     → assign to cross-subject sections (or all sections if none are cross-subject).
    #
    # Properties:
    #   100% automatic (zero user prompts).
    #   100% from PYQ evidence (zero heuristics).
    #   Zero behavior change for 1:1 exams (single-element subject lists).
    #   Exam-independent (no hardcoded names/types/structure).

    _ecfg_path = None
    for _sd in ['/mnt/project/', '/mnt/user-data/uploads/']:
        _matches = sorted(glob.glob(os.path.join(_sd, '*exam_config.json')))
        if _matches:
            _ecfg_path = _matches[0]
            break

    if _ecfg_path:
        import json as _json
        with open(_ecfg_path, encoding='utf-8') as _f:
            _ecfg = _json.load(_f)
        _sections = _ecfg.get('sections', [])
        _taxonomy_subjects = sorted({e['section'] for e in all_entries if e.get('section')})

        # STAGE 1: OBSERVE — which subjects appear in which section Q-ranges
        _sec_subjects = {s['name']: set() for s in _sections}
        for _paper_id, _paper_classifs in progress.items():
            if not isinstance(_paper_classifs, list):
                continue   # skip _meta and other non-list keys
            for _q in _paper_classifs:
                if not isinstance(_q, dict) or 'q_num' not in _q:
                    continue
                for _s in _sections:
                    _qr = _s.get('q_range', [0, 0])
                    if _qr[0] <= _q['q_num'] <= _qr[1]:
                        if _q.get('section'):
                            _sec_subjects[_s['name']].add(_q['section'])
                        break

        # STAGE 2: AUGMENT — cross-subject sections get union of all cross-subject pools
        _cross_secs = [_s['name'] for _s in _sections if len(_sec_subjects.get(_s['name'], set())) >= 2]
        if _cross_secs:
            _pool = set()
            for _cs in _cross_secs:
                _pool |= _sec_subjects[_cs]
            for _cs in _cross_secs:
                _sec_subjects[_cs] = set(_pool)

        # STAGE 3: FALLBACK — unmapped taxonomy subjects → cross-subject sections (or all)
        _mapped = set()
        for _v in _sec_subjects.values():
            _mapped |= _v
        _unmapped = set(_taxonomy_subjects) - _mapped
        if _unmapped:
            _targets = _cross_secs if _cross_secs else [_s['name'] for _s in _sections]
            for _t in _targets:
                _sec_subjects[_t] |= _unmapped

        # Write subjects[] to each section in exam_config
        for _s in _sections:
            _s['subjects'] = sorted(_sec_subjects.get(_s['name'], set()))

        # Write updated exam_config.json to outputs
        _out_ecfg = f'/mnt/user-data/outputs/{exam_code}_exam_config.json'
        with open(_out_ecfg, 'w', encoding='utf-8') as _f:
            _json.dump(_ecfg, _f, ensure_ascii=False, indent=2)

        print(f"\n--- S-SECMAP (v2.24.9) ---")
        for _s in _sections:
            print(f"  {_s['name']}: subjects = {_s.get('subjects', [])}")
        print(f"  → exam_config.json updated with subjects[] per section.")
        print(f"--- End S-SECMAP ---\n")
    else:
        print("\n⚠ S-SECMAP: exam_config.json not found — subjects[] not derived.")
        print("  Step 6 resolver will use fallback rules (SEC-1/SEC-3/SEC-4).\n")

    # Build exam_meta from progress._meta for EXAM_STRUCTURE header (NEW v2.3)
    from datetime import datetime
    meta_raw  = progress.get('_meta', {})
    exam_meta = {
        'papers_analysed'      : len(meta_raw.get('papers_processed', [])),
        'questions_analysed'   : meta_raw.get('total_questions', 0),
        'years_covered'        : sorted(meta_raw.get('years_processed', [])),
        'generation_date'      : datetime.now().isoformat()[:10],
        'time_per_q_sec'       : meta_raw.get('time_per_q_sec', 'unknown'),
        'language'             : meta_raw.get('language', 'unknown'),
        'q_types'              : meta_raw.get('q_types', ['MCQ']),
        'marks_per_q'          : meta_raw.get('marks_per_q', {'MCQ': 1}),
        'negative_marking'     : meta_raw.get('negative_marking', 0),
        'options_count'        : meta_raw.get('options_count', 4),
        'multi_select_allowed' : meta_raw.get('multi_select_allowed', False),
        # v2.18: new fields from exam_config.json (Step 2a v2.5 contract).
        'marking_scheme'       : meta_raw.get('marking_scheme', []),
        'level'                : meta_raw.get('level', 'unknown'),
        'medium'               : meta_raw.get('medium', 'unknown'),
        # v2.5 MSQ contract fields (default-safe: inert when multi_select_allowed=false)
        'msq_k_mode'               : meta_raw.get('msq_k_mode', 'n/a'),
        'msq_k'                    : meta_raw.get('msq_k', None),
        'msq_allow_aota'           : meta_raw.get('msq_allow_aota', False),  # v2.6 D5
        # v2.9 contract-sync: localized MSQ select-instruction (MSQ analogue of nat_instruction)
        'msq_instruction'          : meta_raw.get('msq_instruction',
                                                  '(One or more options may be correct)'),
        'msq_instruction_hi'       : meta_raw.get('msq_instruction_hi',
                                                  '(एक या अधिक विकल्प सही हो सकते हैं)'),
        'negative_marking_by_type' : meta_raw.get('negative_marking_by_type', {}),
        'partial_credit'           : meta_raw.get('partial_credit', False),
        # v2.8 NAT contract fields (default-safe: inert when nat_allowed=false)
        'nat_allowed'              : meta_raw.get('nat_allowed', False),
        'nat_answer_type'          : meta_raw.get('nat_answer_type', 'real'),
        'nat_tolerance'            : meta_raw.get('nat_tolerance', '0'),
        'nat_instruction'          : meta_raw.get('nat_instruction',
                                                  'Enter your answer as a numerical value.'),
        # v2.15 BUG-D07: option_label_format now auto-detected and stored
        'option_label_format'      : meta_raw.get('option_label_format', '1/2/3/4'),
    }

    # Write outputs
    rules_path    = write_section_rules(all_entries, exam_code, exam_meta=exam_meta,
                                         progress=progress)   # v2.15 BUG-D03: progress for label agg
    manifest_path = write_subtopic_manifest(all_entries, exam_code, exam_meta=exam_meta,
                                             progress=progress)   # v2.23: per-section axis dist
    summary_path  = write_analysis_summary(all_entries, progress, exam_code)
    # v2.15 BUG-D01 fix: generate_frequency_xlsx() was defined in §16 but NEVER called.
    # v2.24.6 FIX B: pass all_entries (PYQ + Zero-PYQ scaffolds, post taxonomy-sync +
    # zero-PYQ format inference) so the xlsx is taxonomy-complete and Format-parity-
    # guaranteed with the manifest — was `progress` only (PYQ-observed subtopics only).
    xlsx_path     = generate_frequency_xlsx(progress, exam_code, all_entries=all_entries)

    # Final delivery
    deliver_final(exam_code, rules_path, summary_path, qv_results, progress,
                  manifest_path=manifest_path, xlsx_path=xlsx_path)

def deliver_final(exam_code, rules_path, summary_path, qv_results, progress,
                  manifest_path=None, xlsx_path=None):
    """
    Final delivery: section_rules.md, subtopic_manifest.json, PYQ_Frequency.xlsx,
    analysis_progress.json, analysis_summary.md — all 5 outputs in one response.
    v2.15 BUG-D02: xlsx_path added (was missing — xlsx never delivered).
    """
    # Save final progress
    progress_path = save_progress(progress, exam_code)

    meta        = progress.get('_meta', {})
    n_papers    = len(meta.get('papers_processed', []))
    n_questions = meta.get('total_questions', 0)
    years       = sorted(meta.get('years_processed', []))

    print(f"\n{'='*55}")
    print(f"Step 5 (PYQExtract) COMPLETE — {exam_code}")
    print(f"Papers : {n_papers} | Questions: {n_questions} | Years: {years}")
    print(f"{'='*55}")

    # Deliver all outputs as downloadable chat files.
    # NO Drive upload. User downloads from chat and uploads manually to project.
    # Order matters — section_rules.md first (most important).

    # Present all files as downloadable chat attachments
    # v2.15 BUG-D02 fix: xlsx_path included in delivery (was missing).
    # v2.24.9 S-SECMAP: exam_config.json added (carries subjects[] for Step 6 resolver).
    # Order: section_rules (most important) → manifest → xlsx → exam_config → progress → summary
    delivery = [rules_path]
    if manifest_path: delivery.append(manifest_path)
    if xlsx_path:     delivery.append(xlsx_path)
    # v2.24.9: include updated exam_config.json (with subjects[]) if it was generated
    _ecfg_out = f'/mnt/user-data/outputs/{exam_code}_exam_config.json'
    import os as _os2
    if _os2.path.exists(_ecfg_out):
        delivery.append(_ecfg_out)
    # v2.24: the human-readable taxonomy companion (Subject/Topic/Sub-topic + id), written by
    # write_subtopic_manifest → write_taxonomy_xlsx. Deterministic path; include if it exists.
    import os as _os
    _tax_path = f'/mnt/user-data/outputs/{exam_code}_taxonomy.xlsx'
    if _os.path.exists(_tax_path): delivery.append(_tax_path)
    delivery += [progress_path, summary_path]
    present_files(delivery)
    # present_files is the Claude tool that makes files downloadable in chat.
    # User downloads section_rules.md AND subtopic_manifest.json and uploads
    # BOTH to their [ExamCode] Claude project Files/Knowledge section.
    # subtopic_manifest.json is the cross-step contract — Step 6 and Step 7 both require it.
    # PYQ_Frequency.xlsx is kept locally for Step 6 input.

    # Print handoff message (matches S11-2 PART C format exactly)
    print(f"\nStep 5 (PYQExtract) complete for {exam_code}.")
    print(f"Papers: {n_papers} | Questions: {n_questions} | Years: {years}")
    print("")
    print("ACTION REQUIRED — upload to [ExamCode] Claude project:")
    print(f"  [1] Download {exam_code}_section_rules.md from the file above")
    print(f"  [2] Go to your {exam_code} Claude project → Files (or Knowledge) section")
    print(f"  [3] Upload the downloaded section_rules.md file there")
    print("  (Step 7 reads it directly from the project Files section)")
    print("")
    print("KEEP LOCALLY (downloaded to your computer):")
    print(f"  analysis_progress.json — needed if you add more PYQ papers later")
    print(f"  analysis_summary.md    — review WARNs if any")
    print("")
    print("NEXT:")
    print("  Step 5 complete.")
    print("  If Step 6 (MockBlueprint) also complete: start MockCreate M1.")
    print(f"  If Step 6 pending: run MockBlueprint [N].")
```

### S8-5 — Resume logic (between sessions)

```python
# At session start (S1-2), after loading progress:
done_ids = set(progress.get('_meta',{}).get('papers_processed',[]))

# is_already_processed() used to skip any paper whose ID is in done_ids.
# Filenames must be stable across sessions — do not rename PYQ files.
# Paper ID = filename without extension (make_paper_id).

def is_already_processed(paper_id, progress):
    return paper_id in progress.get('_meta',{}).get('papers_processed',[])

# If ALL uploaded papers are already in done_ids → auto-synthesise immediately.
# User never needs to explicitly type --synthesise.
```

### S8-7 — Progress JSON schema (reference)

```json
{
  "_meta": {
    "exam_code"       : "[ExamCode]",
    "schema_version"  : "2.3",
    "last_updated"    : "[ISO-datetime]",
    "papers_processed": ["[ExamCode]_2024_Shift1", "[ExamCode]_2024_Shift2"],
    "years_processed" : [2019, 2020, 2021, 2022, 2023, 2024],
    "total_questions" : 0
  },
  "('[Section Name]', '[Topic]', '[Subtopic]')": [
    {
      "num":1, "stem":"clean stem text", "stem_raw":"original stem with NOTE",
      "options":["option1","option2","option3","option4"],
      "section":"[Section Name]",
      "topic":"[Topic]", "subtopic":"[Subtopic]",
      "year":2024, "shift":"S1", "paper_id":"[ExamCode]_2024_Shift1",
      "has_note":true, "note_text":"(NOTE: Operations on whole numbers only...)",
      "blank_pos":"none", "is_negative":false, "is_msq":false,
      "image_role":"none", "omml_present":false, "omml_failed":false,
      "object_type":null, "transformation":null, "arrangement":null,
      "complexity":null, "image_clarity":null,
      "difficulty":{"level":"Medium","C":2,"I":1,"V":1,"score":4,"flags":[]},
      "option_format":"single_value", "linked_group_id":null
    }
  ],
  "_linked_groups": {
    "G1": {"group_id":"G1","q_numbers":[90,91,92,93,94],
           "stimulus_type":"passage","word_count":120}
  }
}
```

### S8-8 — Save and load functions

```python
def save_progress(progress, exam_code):
    """Serialize tuple keys to strings for JSON compatibility. Updates last_updated timestamp."""
    from datetime import datetime, timezone
    if isinstance(progress.get('_meta'), dict):
        progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
    data = {str(k) if isinstance(k, tuple) else k: v for k, v in progress.items()}
    path = f'/mnt/user-data/outputs/{exam_code}_analysis_progress.json'
    with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def load_progress(exam_code):
    """Load progress from project knowledge or outputs dir."""
    for search_path in [
        f'/mnt/project/{exam_code}_analysis_progress.json',
        f'/mnt/user-data/uploads/{exam_code}_analysis_progress.json',
        f'/mnt/user-data/outputs/{exam_code}_analysis_progress.json',  # local session fallback
    ]:
        if os.path.exists(search_path):
            with open(search_path, encoding='utf-8') as f: raw = json.load(f)
            progress = {}
            for k, v in raw.items():
                try:    key = ast.literal_eval(k)
                except: key = k
                progress[key] = v
            return progress
    return {'_meta': {'papers_processed': [], 'total_questions': 0,
                       'years_processed': [], 'exam_code': exam_code},
            '_linked_groups': {}}
```

### S8-9 — When --synthesise flag is still useful

```
The --synthesise flag remains available but is never required in normal flow.

Use cases where it IS still useful:
  (a) User added new PYQ papers after section_rules.md was already generated.
      Upload new papers → new session auto-processes them → auto-synthesises.
      Result: section_rules.md is refreshed with improved patterns.

  (b) User wants to re-synthesise without adding new papers (e.g., after
      manually fixing progress.json data):
        PYQExtract --synthesise ALL
      NOTE: Year coverage check still applies when --synthesise ALL is called.
      run_synthesise() reconstructs available_years from progress['_meta']['years_processed']
      and blocks synthesis if minimum coverage is not already in the progress data.

  (c) User wants to synthesise a single section to preview:
        PYQExtract --synthesise "[Section Name]"

In case (a), the flow is:
  Upload new .docx files → new session → processes only the new papers
  (existing papers already in progress.json are skipped) → auto-synthesises
  → delivers updated section_rules.md as downloadable chat file.
  Download it → replace old section_rules.md in [ExamCode] project Files/Knowledge.
  Existing mocks unaffected. Future mocks use improved patterns.
```

---

## §9 — STATUS DASHBOARD

When `--status`:
```
"=== PYQExtract Status: [ExamCode] ===
 Time/Q: [N]sec | lang:[x] | Q-types:[list] | marks:[dict]
 Papers: [N] | Years: [list] | Total Qs: [N]
 Figural images analysed: [N] ([N_unclear] unclear)

 Coverage by section:
   [Section 1]: [N]/[total] subtopics  [####....] [%]%
   [Section 2]: [N]/[total] subtopics  [########] 100%

 Data quality:
   observed  (>=3 Qs): [N] subtopics
   inferred  (1-2 Qs): [N] subtopics
   absent    (0 Qs)  : [N] subtopics

 section_rules.md: [Generated [date] | Not yet generated]
 Next: Process more papers  OR  Run --synthesise ALL
 ============================================="
```

---

## §10 — ANALYSIS SUMMARY FORMAT

```
# [ExamCode] Analysis Summary
Generated: [datetime] | Papers: [N] | Questions: [N] | Years: [list]

## HUMAN REVIEW REQUIRED

### Inferred patterns (1-2 occurrences — verify):
  [Subtopic] P[N]: "[template]" (seen [N] times, years: [Y])

### Deprecated patterns (absent from last 2 years):
  [Subtopic] P[N]: "[template]" (last seen: [Y])

### Figural object types (Claude's vision analysis — review if needed):
  [Subtopic]: [N] images analysed, [N] unclear
  Detected dominant objects: [list]
  Transformation types: [list]
  (QV-9 flags if unclear rate > 20% — those subtopics may need more PYQ data)

### Absent subtopics (no PYQ data — Step 2 uses training knowledge):
  [list]

### Option format changes across years:
  [Subtopic]: [old_fmt] in [years] -> [new_fmt] in [recent years]

## SUGGESTED AUDIT_CONFIG UPDATES
  passage_min_words: [observed min]
  vocab_topic_names: [vocabulary subtopics found]

## STATISTICS
[Section coverage table]
[Top 10 subtopics by observed_count]
```

---

## §11 — DELIVERY FORMAT

### S11-1 — Mid-batch delivery (after each batch of 3 papers, more remain)

```
PART A — Batch summary in chat:
  "=== Batch [N] complete ===
   ✓ [filename_1] | [Y] S[N] | [N] Qs | [N] groups | [N] imgs
   ✓ [filename_2] | [Y] S[N] | [N] Qs | [N] groups | [N] imgs
   ✓ [filename_3] | [Y] S[N] | [N] Qs | [N] groups | [N] imgs

   Cumulative : [done] / [total] papers | [N] total Qs
   Subtopics  : [N] observed | [N] sparse | [N] absent
   Unclear imgs: [N] (QV-9 will flag if >20% per subtopic)
   =================================="

PART B — present_files:
  1. [ExamCode]_analysis_progress.json   <- downloadable from chat

PART C — Continue prompt:
  "[N] paper(s) remaining.
   Options:
   A) Say 'continue' to process the next batch now in this same session.
   B) Download analysis_progress.json above → upload to [ExamCode] project
      knowledge (replace prior version) → open fresh chat → type:
        PYQExtract PYQ: <<same Drive link>>
   Both are valid. Progress is in memory so option A needs no upload."

   Note: User can say 'continue' / 'go' / 'next' — all accepted.
   Claude does NOT auto-proceed — user confirms before each batch.
```

### S11-2 — Final delivery (last batch processed → auto-synthesis complete)

```
This happens automatically at the end of the last batch.
No separate session, no --synthesise command needed.

PART A — QV results in chat:
  "=== Quality Verification ===
   v QV-1  Coverage        : PASS — [N] subtopics covered
   v QV-2  Freq sums       : PASS — all = 100%
   ! QV-3  Difficulty      : WARN — [N] subtopics missing Hard level
   v QV-4  Option format   : PASS
   v QV-5  Wrong options   : PASS
   v QV-6  Confidence      : PASS
   v QV-7  Templates       : PASS
   v QV-8  OMML recovery   : PASS
   ! QV-9  Image clarity   : WARN — [N] unclear images (< 20% threshold)
   v QV-10 Passage groups  : PASS
   v QV-11 Recency         : PASS
   v QV-12 Dedup           : PASS
   ==========================="

PART B — present_files (all in one call, in this order):
  1. [ExamCode]_section_rules.md        <- PRIMARY: download → upload to [ExamCode] project
  2. [ExamCode]_subtopic_manifest.json  <- download → upload to [ExamCode] project
  3. [ExamCode]_PYQ_Frequency.xlsx      <- download → keep for Step 6 input
  4. [ExamCode]_exam_config.json        <- download → REPLACE in [ExamCode] project (v2.24.9:
                                           now carries subjects[] for Step 6 resolver)
  5. [ExamCode]_analysis_progress.json  <- download → keep locally
  6. [ExamCode]_analysis_summary.md     <- download → review if WARNs exist

  All 6 are delivered as downloadable chat attachments.
  NOTHING is uploaded to Google Drive.

PART C — Handoff message:
  "Step 5 (PYQExtract) complete for [ExamCode].
   Papers: [N] | Questions: [N] | Years: [list]

   ACTION REQUIRED — upload to [ExamCode] Claude project:
     [tick] Download [ExamCode]_section_rules.md from the file above
     [tick] Download [ExamCode]_subtopic_manifest.json from the file above
     [tick] Download [ExamCode]_exam_config.json from the file above
           (v2.24.9: now carries subjects[] per section for Step 6 resolver)
     [tick] Go to your [ExamCode] Claude project → Files (or Knowledge) section
     [tick] Upload all 3 files (replace any existing versions)

   KEEP FOR STEP 6:
     [ExamCode]_PYQ_Frequency.xlsx — Step 6 input (Frequency Excel)

   KEEP LOCALLY (downloaded to your computer):
     analysis_progress.json  — needed if you add more PYQ papers later
     analysis_summary.md     — review WARNs if any

   To add new PYQ papers later:
     1. Add new .docx files to your Google Drive PYQ folder
     2. Run: PYQExtract PYQ: <<same Drive link>>
     3. New papers auto-detected → processed → auto-synthesis → refreshed outputs
     4. Download all 6 output files from chat
     5. Replace old files in [ExamCode] project Files/Knowledge section
     Existing mocks: unaffected. Future mocks: use improved patterns.

   NEXT:
     Step 5 complete.
     If Step 6 (MockBlueprint) also complete: start MockCreate M1.
     If Step 6 pending: run MockBlueprint [N]."
```

### S11-3 — DELIVERABLE SET CONTRACT (CLOSED)

```
═══════════════════════════════════════════════════════════════════════
DELIVERABLE SET CONTRACT — EXHAUSTIVE AND CLOSED
═══════════════════════════════════════════════════════════════════════

Each delivery point delivers EXACTLY the files listed and NOTHING ELSE.
This is an exhaustive, closed list — not a minimum. Creating or
delivering any unauthorized file is a spec violation.

────────────────────────────────────────────────────────────────────
PER-BATCH DELIVERY (after each batch of 3, more papers remain)
────────────────────────────────────────────────────────────────────
DELIVER (single present_files call):
  1. [ExamCode]_analysis_progress.json

DO NOT DELIVER:
  ✗ section_rules.md (not yet generated — synthesis hasn't run)
  ✗ subtopic_manifest.json (not yet generated)
  ✗ PYQ_Frequency.xlsx (not yet generated)
  ✗ analysis_summary.md (not yet generated)
  ✗ Any intermediate or working files

────────────────────────────────────────────────────────────────────
FINAL DELIVERY (last batch → auto-synthesis → QV checks complete)
────────────────────────────────────────────────────────────────────
DELIVER (all 6 in one present_files call, in this order):
  1. [ExamCode]_section_rules.md
  2. [ExamCode]_subtopic_manifest.json
  3. [ExamCode]_PYQ_Frequency.xlsx
  4. [ExamCode]_exam_config.json
  5. [ExamCode]_analysis_progress.json
  6. [ExamCode]_analysis_summary.md

DO NOT DELIVER:
  ✗ Input PYQ .docx files (these are INPUTS)
  ✗ Any intermediate scripts or pipeline files
  ✗ Any temporary JSON, working, or debug files
  ✗ Any renamed or versioned variants of the above files

PRE-DELIVERY CHECKLIST (before every present_files call):
  delivering = set of files about to be passed to present_files
  expected   = per-batch: {analysis_progress.json}
               final:     {section_rules.md, subtopic_manifest.json,
                           PYQ_Frequency.xlsx, exam_config.json,
                           analysis_progress.json, analysis_summary.md}
  Check 1: All expected files present in delivery — assert not (expected - delivering)
  Check 2: No unexpected files in delivery — assert not (delivering - expected)
  Check 3: No internal files leaked — no banned patterns in filenames
  Only after all checks pass → call present_files
═══════════════════════════════════════════════════════════════════════
```

### S11-4 — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat delivery report or handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Upload / Replace / Use locally), and next-step reference.

Step 5 uses BOTH footer types:
  - F1 (amber) after each non-final batch (delivers analysis_progress.json)
  - F2 (green) after final batch + auto-synthesis (delivers all 6 files)
```

---

## §12 — INTEGRATION WITH STEP 7 (MockCreate)

### S12-1 — How Step 7 reads section_rules.md

```
Step 7 S1-2d loads:
  section_rules_text = open('/mnt/project/[ExamCode]_section_rules.md',
                             encoding='utf-8').read()

Per question generated (Step 7 MockCreate, section 17, S17-3):

  STEP 1 -- stem template:
    Locate: '--- Subtopic: [re.escape(S)] ---' in section_rules_text.
    Parse: PYQ_STEM_PATTERNS block (P1, P2, ... until next '---' or '=== SECTION:').
    Stop markers: '--- Subtopic:' (next subtopic) or '=== SECTION:' (next section).
    Select P_k by weighted random (weights=frequency%).
    Deprecated patterns: multiply weight by 0.1.
    observed_recent patterns: multiply weight by 1.5.

  STEP 2 -- difficulty calibration:
    Parse PYQ_DIFFICULTY_CALIBRATION block for assigned level.
    Apply criteria literally.

  STEP 3 -- context:
    Parse PYQ_CONTEXT_POOL.dominant. Select from this list (>50% of time).
    Never select from avoid list.

  STEP 4 -- numbers:
    Parse PYQ_NUMBER_RANGES. Generate values within min/max, aligned to multiples_of.

  STEP 5 -- wrong options:
    Read wrong_option_structure.type. Apply:
    fixed_set      -> use fixed_option_texts exactly
    shared_pool    -> rotate from shared_pool_words
    adjacent_values -> 3 near-miss calculations
    alliterative   -> 3 options sharing first letter
    same_category  -> 3 real entities from same class
    anagram        -> 3 rearrangements of answer
    sentence_label -> "Only X" / "Both X and Y" combinations
    image_only     -> no text options generated

  STEP 6 -- NOTE block:
    Read note_block for selected pattern.
    mandatory   -> always append note_text to stem
    conditional -> append with 60% probability
    rare        -> append with 20% probability
    BUG-B13 fix: rare handling added above.
    never       -> do not add NOTE

  STEP 7 -- figural:
    Read PYQ_IMAGE_ANALYSIS.image_role (actual role from E-4, not hardcoded).
    Read object_types.dominant (70%) or observed (30%).
```

### S12-2 — Update protocol

```
NEVER edit section_rules.md directly. Regenerate only.

When new PYQ papers arrive:
  1. Add new .docx files to your Google Drive PYQ folder (same folder used in original trigger).
  2. Run: PYQExtract PYQ: <<same Drive link>>
     → Skips already-processed papers automatically.
     → Processes only new papers (in batches of 3).
     → Auto-synthesises when all new papers are done.
     → Delivers refreshed section_rules.md.
  3. Download the updated section_rules.md from chat.
  4. Replace section_rules.md in [ExamCode] project Files/Knowledge section.

Impact:
  blueprint.json: unchanged | registry.json: unchanged
  Existing mocks: unaffected | Future mocks: use improved patterns
```

---

## §13 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL IN THIS SPEC (identical every exam):
  All 11 extraction rules (E-1 through E-11) with all bug fixes
  section_rules.md field names and schema
  Difficulty scoring (3 axes + marks scaling + v2.5 MSQ load term)
  QV-1 through QV-12 checks (plus QV-5b for fixed_set validation)
  EC-1 through EC-15 edge cases (plus EC-A statement-combination MSQ guard, v2.5)
  Progress JSON schema and delivery format

EXAM-DISCOVERED (zero hardcoding):
  Subtopic names, stem templates, approaches
  answer_cardinality (single/multi) + msq_freq + msq_k_mode/k + per-type marking (v2.5,
    discovered from PYQ option shape + Exam Pattern; nothing exam-specific hardcoded)
  Option formats (which of 12 types), wrong option structures
  Difficulty calibration criteria, number ranges, context pools
  NOTE block texts and frequencies
  Figural object types and transformations
  Passage structures and topic domains

PROOF:
  SSC CGL:   221 subtopics | 1/2/3/4 options | NOTE blocks for Analogy
  GATE CS:   ~40 subtopics | (A)/(B)/(C)/(D) | no NOTE blocks
  NEET Bio:  ~90 subtopics | (1)/(2)/(3)/(4) | statement format heavy
  UPSC CSAT: ~30 subtopics | (a)/(b)/(c)/(d) | Assertion-Reason frequent
```

---

## §14 — SECTION_RULES.MD SCHEMA REFERENCE

```
CATEGORY C (file-level header — written once at top of section_rules.md):
  *** DOC-ALIAS ONLY *** — "CATEGORY C" is this schema reference's conceptual name for
  this block. The literal on-disk token is the exact string '=== EXAM_STRUCTURE ==='.
  A consumer spec MUST test for '=== EXAM_STRUCTURE ===' (or read specific key: value
  lines via a regex like cat_c() does) — NEVER regex-match the phrase "CATEGORY" or
  "CATEGORY C" against file content; that string is never written to disk. (See
  A-INTEGRITY-FALSEPOS-01 / Framework_MockTestCreateAudit.md v2.7.5 changelog for the
  exact defect this caused when violated.)
  NEW v2.3 — auto-detected at runtime, never hardcoded.
  Written by write_section_rules() under '=== EXAM_STRUCTURE ==='.

  exam_code                str   [ExamCode] from trigger.
  total_papers_analysed    int   Number of PYQ .docx files processed.
  total_questions_analysed int   Total PYQ questions accumulated across all papers.
  years_covered            list  All years for which PYQ papers were processed.
  generation_date          str   ISO date of synthesis run.
  time_per_q_sec           int   Seconds per question (auto-detected from exam pattern).
  language                 str   english | hindi | regional | bilingual (auto-detected from PYQ).
  medium                   str   v2.18. Exam language from exam_config.json Overview tab.
                                 "English", "Hindi", "Bilingual", etc. Authoritative source —
                                 language field above is PYQ-detected validation. xlsx wins
                                 on conflict. Consumed by Steps 7, 9, 11.
  level                    str   v2.18. Academic level from exam_config.json Overview tab.
                                 "Graduation", "Post Graduation", "Under Graduation", "School".
                                 Step 7 uses for question complexity calibration.
                                 Step 9 uses for explanation depth.
  q_types                  list  e.g. ['MCQ'] or ['MCQ','MSQ'] (auto-detected).
  marks_per_q              dict  e.g. {'MCQ':1} or {'MCQ':2,'MSQ':2} (auto-detected).
                                 v2.18: derived from marking_scheme[] — MAX per question_type.
                                 Summary scalar for backward compat; see marking_scheme for
                                 full per-range detail.
  negative_marking         float e.g. -0.5 or 0 (auto-detected).
                                 v2.18: derived from marking_scheme[] — most common value.
                                 Summary scalar; see marking_scheme for per-range detail.
  marking_scheme           list  v2.18. Full per-range scoring rules from exam_config.json.
                                 Each entry: {q_range: [start,end], question_type: str,
                                 correct_marks: float, negative_marks: float}.
                                 Steps 7/8/9 use this for exact per-Q-position marks lookup
                                 (e.g., CSIR NET Q.72 in Part C → 4 marks, Q.25 in Part B → 2).
                                 Empty list [] when exam_config absent (legacy fallback).
  options_count            int   Options per question e.g. 4 (auto-detected).
  multi_select_allowed     bool  True for exams with MSQ (auto-detected).
  msq_k_mode               str   v2.5. fixed | variable | n/a (from Exam Pattern; n/a when
                                 multi_select_allowed=false). Step 7 uses to bound |S|.
  msq_k                    int   v2.5. Correct-option count for fixed mode (else none).
  msq_allow_aota           bool  v2.6 (D5). True permits "All of the above" as an option
                                 under MSQ (default False — AOTA is self-contradictory in
                                 multi-select). Step 7 (R-MSQ-ESCAPE/G-MSQ-SET) and Step 8
                                 (A-MSQ-KEY) read it directly from section_rules.
  msq_instruction          str   v2.9. Localized MSQ select-instruction (the MSQ analogue of
                                 nat_instruction). Default '(One or more options may be
                                 correct)'. Step 7 (msq_instruction_for) and Step 8
                                 (msq_instruction_phrases / A-MSQ-INSTR) read it from
                                 section_rules; overridable per exam. Inert when
                                 multi_select_allowed=false.
  msq_instruction_hi       str   v2.9. Hindi/bilingual variant of msq_instruction. Default
                                 '(एक या अधिक विकल्प सही हो सकते हैं)'.
  negative_marking_by_type dict  v2.5. e.g. {'MCQ':-0.5,'MSQ':0}. Per-type penalty; MSQ
                                 commonly 0. Consumed by Step 9 scoring. {} = use scalar.
  partial_credit           bool  v2.5. True if MSQ awards partial marks (else all-or-nothing).
                                 Consumed by Step 9; dormant at Step 5.
  difficulty_labels        list  v2.12. Canonical, exam-overridable difficulty vocabulary used
                                 as the stored/rendered Complexity value in the per-question
                                 registry.question_index (Step 6 seeds, Step 7 fills, Step 8
                                 certifies, Step 6 renders). Default ['Easy','Medium','Hard'].
                                 Alias to the two internal spellings — Step-0 calibration
                                 Simple/Medium/Hard and Step-1 schedule counts simple/medium/hard
                                 — is fixed: simple→Easy, medium→Medium, hard→Hard. Consumed by
                                 Step 6 (carry-through to blueprint.json) and the G-QINDEX
                                 difficulty check. An exam may override (e.g. a 2- or 5-band set).
  nat_allowed              bool  v2.8 (PARAMETER 11). Capability gate (analogous to
                                 multi_select_allowed): true iff the exam uses numerical-entry
                                 questions. Gates the per-subtopic answer_type detection.
                                 Default false ⇒ NAT path fully inert.
  nat_present              bool  v2.8. Rollup of THIS analysis — true iff any subtopic
                                 resolved to answer_type=='numerical'. Step 6 also derives
                                 this from per-subtopic answer_type (mirrors multi_present).
  nat_answer_type          str   v2.8. integer | real (default real when nat_allowed). integer
                                 ⇒ exact match; real ⇒ value within nat_tolerance. From exam
                                 pattern only (answer-key info; unextractable from PYQ).
  nat_tolerance            str   v2.8. Accepted band for real NAT — abs delta (float) or '%'
                                 string. '0' = exact to displayed precision (default; never
                                 invented). Becomes Step 9 ca_range. integer ⇒ always '0'.
  nat_instruction          str   v2.8. Parametric candidate-facing instruction Step 7 places
                                 in the Q.N stem (R14), localised per PARAMETER 3. Default
                                 "Enter your answer as a numerical value."
  total_sections           int   Number of distinct sections in section_rules.md.
  framework_version        str   Framework_MockTestAnalyse version used.

  (Also written: STRUCTURAL_CHANGES_BY_YEAR block — observable year-over-year
   structural changes derived from PYQ data by _compute_structural_changes().)

CATEGORY A (per section header — one block per section):
  *** DOC-ALIAS ONLY *** — "CATEGORY A" is this schema reference's conceptual name for
  this block. The literal on-disk token is the exact string '=== SECTION: <n> ===' (per
  section, where <n> is the section number). Never regex-match the phrase "CATEGORY A"
  against file content — test for the '=== SECTION:' marker instead.
  option_label_format  str   Most common option label in section: "1/2/3/4"|"A/B/C/D" etc.
  figural_banned       bool  NEW v2.3. True when ALL FIGURAL subtopics in this section
                             have observed_count=0 or all patterns deprecated.
                             Computed from data — NOT hardcoded per exam.
                             Step 7 uses this to skip FIGURAL generation for this section.
  sub_types_observed   list  Exact SubTopic heading strings from PYQ docx.
  axis_distribution    block v2.23. Per-section 3-year format-distribution TARGET (per-paper
                             averages) — the CATEGORY-A output of compute_section_axis_distribution().
                             Sub-fields: recent_years, n_papers_recent, mocks_per_window,
                             negative_rate, axis1_per_paper {TEXT|FIGURAL|PASSAGE|DI: avg},
                             axis2_per_paper {8-class: avg}, axis3_per_paper {MCQ|MSQ|NAT: avg},
                             axis2_audit_mode {class: band|guarantee|float}. band iff
                             avg×mocks_per_window ≥ 1; else guarantee (periodic ≥1/window);
                             DIRECT always float (residual, never audited). Step 6 enforces
                             axis1/axis3 + LINKED at allocation; Step 7 enforces the other 7
                             Axis-2 classes at generation; Step 8 audits. Omitted for all-Zero-PYQ
                             sections. Also mirrored into subtopic_manifest.json axis_distribution{}.

CATEGORY B (per subtopic entry — one block per subtopic):
  *** DOC-ALIAS ONLY *** — "CATEGORY B" is this schema reference's conceptual name for
  this block. The literal on-disk token is the exact string '--- Subtopic: <name> ---'
  (per subtopic). Never regex-match the phrase "CATEGORY B" against file content — test
  for the '--- Subtopic:' marker instead.
  subtopic               str   Exact subtopic name.
  section                str   Parent section.
  topic                  str   Parent topic.
  observed_count         int   Total PYQ questions across all papers.
  format                 str   TEXT | FIGURAL | PASSAGE | DI
  option_format_primary  str   Most common option format across all years.
                               (BUG-B15/C04 fix v2.3: written as 4 separate fields)
  option_format_recent   str   Option format in most recent year only.
  option_format_changed_recently  bool  True if recent != primary.
  option_format_all_observed      list  All distinct option format types seen.
  OMML_required          bool  True if subtopic has OMML math formulas in PYQ.
  negative_question_freq int   % of Qs using NOT/INCORRECT/EXCEPT/WRONG.
  observed_axis2         dict  v2.23. {AXIS2_CLASS: count} — this subtopic's PYQ-observed
                               Axis-2 (STEM STRUCTURE) distribution, from the shared classifier.
  presentation_family    str   v2.23. Family key (vocab_single_word|one_word_substitution|
                               idiom_phrase|fact_recall|None) seeding axis2_capability;
                               mirrors Step 7 resolve_presentation_family (Step 7 authoritative).
  axis2_capability       list  v2.23. Axis-2 forms this subtopic may FAITHFULLY take =
                               observed ∪ family-menu ∪ {DIRECT} (+LINKED iff format PASSAGE/DI,
                               LINKED being stimulus-locked). Step 6 uses it for rare-format
                               reachability; Step 7 renders ONLY within it (fabrication banned).
  answer_type            str   v2.8. option | numerical — the NAT axis (orthogonal to
                               answer_cardinality). 'numerical' (NAT: no options, typed
                               value) when nat_allowed AND >50% of observed Qs have zero
                               selectable options (no text options AND no option-images:
                               image_role none|stem_only, never options_only|stem_and_options
                               — so a figural NAT with a problem diagram still counts, but a
                               figural MCQ with image-options does not). Always 'option' when
                               nat_allowed=false. A 'numerical' subtopic's cardinality is moot.
  nat_freq               int   v2.8. % of observed Qs in this subtopic detected as NAT.
  answer_cardinality            str   v2.5. single | multi — the Step 7 DISPATCH unit. 'multi'
                               when >50% of observed Qs are MSQ (whole-subtopic mode, so
                               the per-mock allocation schema needs no answer-mode split).
                               Always 'single' when multi_select_allowed=false.
  msq_freq               int   v2.5. % of observed Qs in this subtopic detected as MSQ.
  fill_in_blank          str   none | start | middle | end
  linked_group_size      int   0=independent; N=average Qs per stimulus group.
  max_per_paper          int   NEW v2.3. Max Qs of this subtopic in any single paper.
                               Step 7 uses as L3 uniqueness ceiling — never exceed this.
  typical_per_paper      int   NEW v2.3. Modal/average Qs per paper for this subtopic.
  stem_word_count        dict  {min:int, max:int, typical:int}
  sub_type_label         str   Exact SubTopic heading for Step 7 dispatch.

  PYQ_STEM_PATTERNS      list  Sorted by weighted frequency DESC:
    id           str   P1, P2, P3, ...
    template     str   Structural skeleton with _VAR_ placeholders.
    approach     str   Cognitive operation in plain language.
    frequency    int   Weighted frequency% (all patterns per subtopic sum to 100).
    raw_count    int   Actual PYQ Qs matching this pattern.
                       NEW v2.3: now written to file (BUG-C02 fix).
    years        list  Calendar years this pattern was observed in.
                       NEW v2.3: now written to file (BUG-C02 fix). QV-11 uses it.
    confidence   str   observed (>=3) | observed_recent | inferred (1-2) | absent (0)
    deprecated   bool  True if pattern absent from last 2 years of data. (BUG-A20 fix)
    note_block   str   mandatory | conditional | rare | never
    note_text    str   Canonical NOTE text (if mandatory or conditional).

  PYQ_DIFFICULTY_CALIBRATION  (BUG-B09+C01 fix: is_inferred written to file v2.3):
    Simple  str   criteria="..." [INFERRED] tag if is_inferred=True
    Medium  str   criteria="..." [INFERRED] tag if is_inferred=True
    Hard    str   criteria="..." [INFERRED] tag if is_inferred=True

  wrong_option_structure dict:
    type                str  One of 11 E-11 types (including image_only). (BUG-B12 fix)
    description         str  What this means for Step 7 generation.
    fixed_option_texts  list REQUIRED when type=fixed_set. (BUG-C07 fix: QV-5b enforces)
    shared_pool_words   list Only when type=shared_pool.

  PYQ_NUMBER_RANGES  dict  {var: {min, max, multiples_of, notes}}
    (omit entirely if not quantitative)

  PYQ_CONTEXT_POOL   dict  {dominant:[str], common:[str], rare:[str], avoid:[str]}
    Optional additional fields when recycled stimuli detected (NEW v2.3):
    recycled_datasets  list  Short descriptors of stimuli seen in >=2 papers.
                             Step 7 must NOT reproduce these stimuli verbatim.
    ban_recycled       bool  True when recycled_datasets is non-empty.
    (omit entirely if not quantitative and no recycled stimuli)

  PYQ_IMAGE_ANALYSIS dict  (omit entirely if format != FIGURAL):
    image_role           str  stem_only | options_only | stem_and_options
                              Computed from E-4 q_roles, not hardcoded. (BUG-B11 fix)
    object_types         dict {dominant:[str], observed:[str], avoid:[str]}
    transformation_types list Observed transformation types.
    complexity_dist      dict {Simple:%, Medium:%, Hard:%}
    images_analysed      int
    images_unclear       int

  PYQ_PASSAGE_STRUCTURE dict  (omit entirely if format != PASSAGE):
    sub_format              str  RC | Cloze (no leading space — BUG-A10 fix)
    word_range              dict {min:int, max:int}
    paragraph_count         dict {typical:int}  (BUG-C05 fix v2.3: now written)
    topic_domains_observed  list Passage topic categories seen in PYQ.
                                 (BUG-C05 fix v2.3: now written)
    topic_domains_avoid     list Passage topics seen too recently — avoid repeating.
    q_type_distribution     dict {inference:%, direct:%, vocab:%, grammar:%}
```

---

## DEFINITION OF DONE — Step 5 (PYQExtract)

Step 5 is complete when ALL of the following hold:

```
[0] Minimum year coverage rule (§1-6) satisfied:
      MANDATORY: papers from at least 5 most recent years processed (non-negotiable).
      If exam has fewer than 5 years of PYQ: ALL available years processed.
      Exception only: Scenario B (no PYQ at all) or no_year_info mode.
      (Synthesis is automatically blocked if this is not met — §1-6 enforcement.)

[1] All available PYQ docx files processed (all years required by [0], all shifts).
[2] analysis_progress.json is current — all papers reflected in accumulated data.
[3] Auto-synthesis ran successfully at end of last batch — no manual --synthesise needed.
    (If synthesis failed: re-run PYQExtract --synthesise ALL)
[4] QV-1 through QV-12 (plus QV-5b): all results are PASS or WARN (zero FAIL checks).
[5] WARN items reviewed by user and accepted or corrected.
[6] section_rules.md loads without error in Step 7 S1-2d:
      section_rules_text = open('/mnt/project/[ExamCode]_section_rules.md',
                                 encoding='utf-8').read()
    Verify: file non-empty; all '=== SECTION:' and '--- Subtopic:' blocks present.
[7] analysis_summary.md human-review items resolved or accepted.
[8] User downloaded [ExamCode]_section_rules.md from the chat file delivery
    and uploaded it to the [ExamCode] Claude project → Files / Knowledge section.
    (NOT Drive. Claude project Files section only.)
[9] User confirmed: Step 6 (MockBlueprint) is also complete.
[13] [ExamCode]_PYQ_Frequency.xlsx generated with correct sheet count (4 + sections_count).
[14] XLSX-F1 through XLSX-F9 validation: all PASS (§16 §EXT-9).
[15] Master Data sheet row count matches total unique subtopics in progress.json.
[16] Year columns in xlsx match _meta.years_processed exactly.
[17] User downloaded [ExamCode]_PYQ_Frequency.xlsx — kept for Step 6 input.
[18] Per-batch deliverable set closed: EXACTLY 1 file per batch (S11-3)
[19] Final deliverable set closed: EXACTLY 5 files at completion (S11-3)
[20] Pre-delivery checklist (S11-3) passed before every present_files call
[21] No unauthorized files in any present_files call
[22] Taxonomy sync ran: run_synthesise printed "Taxonomy sync:" summary line
     showing count of zero-PYQ scaffold entries added (may be 0 if all
     taxonomy subtopics were already PYQ-observed — that is correct).
[23] Completeness invariant holds: manifest subtopic count >= taxonomy subtopic
     count. A manifest with FEWER subtopics than the taxonomy means taxonomy
     sync failed or was skipped — re-run Step 5 to fix.

MockCreate M1 MUST NOT start until [8] AND [9] both hold.
```


# ════════════════════════════════════════════════════════════════════════
# §15 — SUBTOPIC_ID CONTRACT (v2.4 — the cross-step vocabulary authority)
# ════════════════════════════════════════════════════════════════════════
#
# WHY THIS EXISTS:
#   Before v2.4, Step 5 (Analyse) and Step 6 (Blueprint) each independently
#   derived subtopic names from the same Analysis docs, then Step 7 (Create)
#   tried to rejoin them by EXACT STRING MATCH. Two independent derivations do
#   not produce identical strings — each step silently corrected/merged/re-
#   clustered names its own way. On SSC CGL Tier 1 this produced ~70% name
#   mismatch (144 of 208 blueprint names had no section_rules match), causing
#   Step 7 to fail its subtopic join and its mandatory-subtopic checks.
#
# THE CONTRACT (three roles):
#   MINTER  (Step 5, THIS framework): assigns every subtopic a stable subtopic_id
#           and publishes the authoritative id↔name registry
#           ([ExamCode]_subtopic_manifest.json). Step 5 is the ONLY minter.
#   CONSUMER+ENFORCER (Step 6, Framework_Blueprint): READS the manifest, refers
#           to subtopics by subtopic_id, and enforces the mandate/alternation
#           data carried in the manifest at blueprint-build time.
#   JOINER  (Step 7, Framework_MockCreate): joins blueprint.json ↔
#           section_rules.md ON subtopic_id. No string matching.
#
# THE id RECIPE (deterministic, exam-agnostic — see slugify / make_subtopic_id):
#   subtopic_id = <section_prefix>.<topic_slug>.<subtopic_slug>
#   - slugify: lowercase; — – / & → space; non-alnum → _; collapse/strip _.
#   - Same (section, topic, subtopic) ALWAYS yields the same id, on every exam.
#   - Collisions de-duplicated with numeric suffix (_2, _3, …) by the manifest writer.
#   - INDEPENDENT of concept_group. concept_group is for DOUBT-3 intra-mock
#     uniqueness (a different concern); subtopic_id is purely the cross-step join key.
#
# WHAT IS LOAD-BEARING vs DECORATIVE:
#   - subtopic_id  = LOAD-BEARING. Never reworded. The machine joins on this.
#   - display name (the "--- Subtopic: X ---" heading) = DECORATIVE. May be
#     reworded freely WITHOUT breaking the pipeline, because nothing joins on it.
#
# MANDATE DATA IS STRUCTURED, NOT PROSE:
#   The manifest carries, per subtopic:
#     mandates.mandatory_every_mock   (bool)
#     mandates.alternation_group      (str|null — members must NOT co-occur in a mock)
#     mandates.min_per_series_window  (int|null)
#   plus top-level convenience lists: mandatory_every_mock[], alternation_groups{}.
#   To declare a subtopic mandatory: author its NOTE with an explicit
#   "MANDATORY ... every mock" / "MANDATORY per mock" marker (Step 5 extracts it).
#   To declare an alternation pair: set alternation_group on both members
#   (e.g. both Simple Interest and Compound Interest → alternation_group: "ci_si").
#   Downstream steps read these as DATA; they never re-parse prose to rediscover them.
#
# COMPLETENESS REQUIREMENT (v2.20 — closes the closed-world assumption gap):
#   The manifest must cover the ENTIRE exam taxonomy, not just the PYQ-observed
#   subset. A PYQ-only manifest is a PARTIAL vocabulary that will break when the
#   blueprint (Step 6) includes syllabus-only subtopics.
#
#   INVARIANT:  len(manifest_subtopics) >= len(taxonomy_subtopics)
#
#   The manifest may have MORE entries than the taxonomy (PYQ-discovered subtopics
#   finer than taxonomy granularity — e.g., taxonomy says "Geometry" but PYQs
#   revealed "Triangles", "Circles", "Coordinate Geometry"). That is correct.
#   The manifest must NEVER have FEWER taxonomy-defined subtopics.
#
#   HOW IT HOLDS: run_synthesise() calls taxonomy_sync_entries() (§15-1) AFTER
#   building PYQ-based entries and BEFORE writing section_rules + manifest.
#   Taxonomy sync adds scaffold entries for every taxonomy subtopic absent from
#   the PYQ-derived set. The manifest is therefore COMPLETE by construction.
#
#   WHY THE PRE-v2.20 SPEC MISSED THIS: the contract assumed a CLOSED-WORLD
#   model where every subtopic the blueprint needs would have been observed in
#   PYQs and therefore minted by Step 5. The OPEN-WORLD reality is that exams
#   routinely have syllabus-defined subtopics with zero PYQ history (new syllabus
#   additions, rarely-tested topics, partial PYQ availability). This is the
#   COMMON CASE — not an edge case.
#
# FUTURE-PROOFING (why this can't drift again, across 100 exams):
#   1. Ids are minted ONCE, by ONE step, from a fixed recipe.
#   2. Downstream steps copy ids verbatim or FAIL LOUD (no silent fallback).
#   3. Step 6 and Step 7 each run a CONTRACT GATE at startup: every subtopic_id
#      they reference MUST exist in the manifest; an unknown id = HARD STOP naming
#      the offending id. A name that drifts can no longer silently disappear.
#   4. The recipe and contract contain zero exam-specific values.
#   5. Taxonomy sync (v2.20) ensures the manifest covers the COMPLETE vocabulary.
#      Step 6 NEVER self-mints an id — it HARD STOPS if any subtopic is missing.
#
# DEFINITION OF DONE additions (v2.4):
#   [10] [ExamCode]_subtopic_manifest.json written and delivered via present_files.
#   [11] Every --- Subtopic: --- block has a subtopic_id as its first field.
#   [12] User uploaded subtopic_manifest.json to the project Files section
#        alongside section_rules.md (Step 6 and Step 7 both require it).
#
# DEFINITION OF DONE additions (v2.20):
#   [22] Taxonomy sync ran: run_synthesise printed "Taxonomy sync:" summary line.
#   [23] Completeness invariant holds: manifest subtopic count >= taxonomy subtopic count.
# DEFINITION OF DONE additions (v2.24.6 — FIX B/C):
#   [24] Frequency Excel completeness invariant holds (master_data_completeness_test):
#        set(master_data_subtopic_ids) == set(manifest_subtopic_ids) —
#        aggregate_frequency_data(progress, all_entries=...) printed no
#        "master_data_completeness_test would FAIL" WARN.
#   [25] Excel Format == manifest Format for every subtopic (excel_manifest_format_parity_test)
#        — guaranteed by construction when all_entries is passed (both read entry['format']
#        from the same dict).
#   [26] DI/PASSAGE detection uses the structural _looks_like_table_stimulus() helper
#        (di_heuristic_false_positive_test) — word-boundary + pipe-row signal, not a bare
#        substring match; "vegetable"/"acceptable"/stray single pipes no longer false-positive.
# ════════════════════════════════════════════════════════════════════════
#
# ════════════════════════════════════════════════════════════════════════
# §15-1 — TAXONOMY SYNC PROTOCOL (v2.20 — zero-PYQ manifest completeness)
# ════════════════════════════════════════════════════════════════════════
#
# WHAT: After PYQ-based synthesis produces the entry list, synchronise it
#   with the exam's approved taxonomy. For every taxonomy-defined subtopic
#   NOT already in the PYQ-derived entries, create a scaffold entry with
#   zero-PYQ defaults. These scaffolds flow through the normal
#   write_section_rules() and write_subtopic_manifest() paths, AND (v2.24.6
#   FIX B) through generate_frequency_xlsx() via the all_entries parameter —
#   so the Frequency Excel is now ALSO complete by construction, not just
#   section_rules.md and the manifest. Previously the Excel was derived from
#   `progress` only (PYQ-observed keys), so Zero-PYQ scaffolds could never
#   appear in it regardless of how complete the manifest itself was.
#
# WHEN: Called by run_synthesise() AFTER the PYQ-based entry loop and
#   BEFORE QV checks, write_section_rules(), and write_subtopic_manifest().
#
# IMPLEMENTATION: taxonomy_sync_entries() + make_zero_pyq_scaffold_entry()
#   (defined in §5 code after make_subtopic_id). Full docstrings and edge
#   case handling (EC-ZP-1 through EC-ZP-10) are in those function bodies.
#
# TAXONOMY SOURCES (priority order — UNION, not primary/fallback):
#   1. [ExamCode]_taxonomy_draft.json (Step 2a output — PRIMARY, contains
#      ALL syllabus subtopics including zero-PYQ ones)
#   2. Approved Analysis doc [ExamCode]_PYQ_Analysis.docx (Step 2c output —
#      ADDITIONAL, covers PYQ-discovered subtopics not in taxonomy_draft)
#   Both sources are loaded and unioned. If neither is found, sync SKIPS
#   with a logged warning.
#
# SCAFFOLD ENTRY SHAPE: a complete entry dict with all format_entry() fields,
#   observed_count=0, confidence='absent', generic P1 stem pattern, zero
#   difficulty calibration, and a NOTE identifying it as syllabus-only.
#   See make_zero_pyq_scaffold_entry() for the full field list.
#
# POST-SYNC STATE:
#   all_entries[] contains BOTH PYQ-derived entries AND zero-PYQ scaffolds.
#   write_section_rules() iterates all_entries → scaffold blocks appear in
#   section_rules.md alongside PYQ-derived blocks.
#   write_subtopic_manifest() iterates all_entries → scaffold subtopics
#   get proper slugified subtopic_ids in the manifest.
#   The manifest is COMPLETE by construction. Step 6 can never encounter
#   an unresolvable subtopic.
# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# §16 — FREQUENCY XLSX OUTPUT (v2.13 — PYQ frequency analysis spreadsheet)
# ════════════════════════════════════════════════════════════════════════
#
# PURPOSE:
#   Generate [ExamCode]_PYQ_Frequency.xlsx during the synthesis phase.
#   This xlsx is a mandatory input to Step 6 (MockBlueprint).
#   All data sourced from analysis_progress.json — no new extraction needed.
#
# DOWNSTREAM CONSUMER:
#   Step 1 reads: Subject, Topic, Sub-Topic, Format, year-wise Qs, Avg/Paper,
#   Consistency, Trend, Importance, Must Prepare.
#
# INTEGRATION:
#   Called automatically at end of run_synthesise(), after section_rules.md
#   and subtopic_manifest.json are written. Added to present_files delivery.

---

## §16-1 — DATA AGGREGATION FROM PROGRESS JSON

```python
from collections import Counter, defaultdict
import re

def aggregate_frequency_data(progress, all_entries=None):
    """
    Aggregate per-subtopic, per-year data from analysis_progress.json.
    Returns structured data ready for xlsx generation.

    v2.24.6 FIX B (defense-in-depth for Gap 1 + Gap 2, closed authoritatively at Step 6
    by FIX A): previously iterated ONLY `progress` — which is populated exclusively by
    PYQ-OBSERVED (section, topic, subtopic) keys, so a Zero-PYQ subtopic (never observed
    in any PYQ paper) could structurally never become an Excel row — and derived Format
    with a 2-way (TEXT/FIGURAL only) `image_role`-only rule independent of the manifest's
    4-way (TEXT/FIGURAL/PASSAGE/DI) `synthesise_subtopic` derivation, so the Excel and the
    manifest could disagree on the SAME subtopic.

    When `all_entries` (the full PYQ + Zero-PYQ-scaffold list — the SAME list
    write_subtopic_manifest() writes from) is supplied, this function now:
      (1) seeds subtopic_data from all_entries FIRST, so every taxonomy subtopic gets a
          row (Zero-PYQ ones as all-zero rows) — Excel is taxonomy-complete, matching the
          manifest's COMPLETENESS INVARIANT (ref §15-1 taxonomy-sync FIX A).
      (2) takes Format from each entry['format'] (already the manifest's 4-way value —
          the SAME field write_subtopic_manifest() reads) instead of re-deriving it
          locally, so Excel Format == manifest Format for every subtopic BY CONSTRUCTION,
          never merely by coincidence.
    `progress` is still the sole source of PER-YEAR counts (all_entries only carries an
    aggregate `observed_count`, not a year-by-year breakdown).

    Backward-compatible: if `all_entries` is omitted (all_entries=None), falls back to the
    pre-v2.24.6 progress-only behavior (PYQ-observed subtopics only, 2-way Format) — so any
    caller that hasn't been updated to pass all_entries still gets a working (if incomplete)
    workbook rather than an error.
    """
    meta = progress.get('_meta', {})
    all_years = sorted(meta.get('years_processed', []))
    papers_processed = meta.get('papers_processed', [])

    # Count papers per year
    papers_per_year = Counter()
    for paper_id in papers_processed:
        year = extract_year_from_paper_id(paper_id)
        if year:
            papers_per_year[year] += 1

    # Aggregate questions per (section, topic, subtopic) per year
    subtopic_data = {}

    # ── STEP 1 (v2.24.6 FIX B): seed EVERY taxonomy subtopic from all_entries, PYQ +
    # Zero-PYQ alike, with its manifest-identical 4-way Format. This is what makes the
    # Excel taxonomy-complete and Format-parity-guaranteed with the manifest.
    if all_entries:
        for e in all_entries:
            key = (e['section'], e['topic'], e['subtopic'])
            subtopic_data[key] = {
                'section': e['section'],
                'topic': e['topic'],
                'subtopic': e['subtopic'],
                'format': e.get('format', 'TEXT'),   # manifest-identical — same field, same source
                'year_counts': defaultdict(int),
                'total': 0
            }

    for key, questions in progress.items():
        if not isinstance(key, tuple) or len(key) != 3:
            continue
        # v2.15 BUG-D08: removed dead str(key).startswith('_') check —
        # tuple keys never stringify to a '_'-prefixed string, and the
        # isinstance check above already excludes string keys like '_meta'.

        section, topic, subtopic = key

        if key not in subtopic_data:
            # Only reachable when all_entries is None (backward-compat path) or a
            # progress key somehow isn't in all_entries (shouldn't happen post-taxonomy-
            # sync, but handled defensively rather than dropping data).
            subtopic_data[key] = {
                'section': section,
                'topic': topic,
                'subtopic': subtopic,
                'format': 'TEXT',
                'year_counts': defaultdict(int),
                'total': 0
            }

        entry = subtopic_data[key]
        for q in questions:
            year = q.get('year')
            if year:
                entry['year_counts'][year] += 1
                entry['total'] += 1

            # Legacy 2-way format fallback — ONLY used when all_entries was not supplied
            # (entry['format'] already carries the manifest's 4-way value otherwise; never
            # overwrite a value that already came from all_entries).
            if not all_entries:
                role = q.get('image_role', 'none')
                if role in ('stem_only', 'stem_and_options', 'options_only'):
                    entry['format'] = 'FIGURAL'

    # ── COMPLETENESS INVARIANT (v2.24.6 FIX B — mirrors the manifest's own S2-MANIFEST-
    # COMPLETENESS gate): when all_entries is supplied, the Excel MUST cover exactly the
    # same subtopic set as the manifest. Advisory WARN here (xlsx generation never hard-
    # stops synthesis) — genuine gaps still surface downstream at Step 6 S2-MANIFEST.
    if all_entries:
        manifest_keys = {(e['section'], e['topic'], e['subtopic']) for e in all_entries}
        excel_keys = set(subtopic_data.keys())
        missing_from_excel = manifest_keys - excel_keys
        if missing_from_excel:
            print(f"  WARN: master_data_completeness_test would FAIL — "
                  f"{len(missing_from_excel)} manifest subtopic(s) absent from the "
                  f"Frequency Excel: {sorted(missing_from_excel)[:5]}"
                  + (" ..." if len(missing_from_excel) > 5 else ""))

    return {
        'subtopic_data': subtopic_data,
        'all_years': all_years,
        'papers_per_year': dict(papers_per_year),
        'total_papers': len(papers_processed),
        'total_questions': sum(e['total'] for e in subtopic_data.values())
    }

def extract_year_from_paper_id(paper_id):
    m = re.search(r'(\d{4})', str(paper_id))
    return int(m.group(1)) if m else None
```

---

## §16-2 — DERIVED METRICS COMPUTATION

```python
def compute_derived_metrics(entry, all_years, papers_per_year):
    """
    Compute all derived metrics for a subtopic entry.
    """
    year_counts = entry['year_counts']

    # Avg/Paper per year
    avg_per_year = {}
    for year in all_years:
        qs = year_counts.get(year, 0)
        papers = papers_per_year.get(year, 0)
        avg_per_year[year] = round(qs / papers, 2) if papers > 0 else 0

    # Avg/Paper combined
    total_papers = sum(papers_per_year.values())
    avg_combined = round(entry['total'] / total_papers, 2) if total_papers > 0 else 0

    # Consistency: number of years where qs > 0
    consistency = sum(1 for y in all_years if year_counts.get(y, 0) > 0)

    # Trend: compare recent half vs older half
    n_years = len(all_years)
    if n_years >= 2:
        mid = n_years // 2
        recent_years = all_years[mid:]
        older_years = all_years[:mid]
        recent_avg = sum(avg_per_year.get(y, 0) for y in recent_years) / len(recent_years)
        older_avg = sum(avg_per_year.get(y, 0) for y in older_years) / len(older_years)

        only_latest = (year_counts.get(all_years[-1], 0) > 0 and
                       all(year_counts.get(y, 0) == 0 for y in all_years[:-1]))
        if only_latest:
            trend = 'New in ' + str(all_years[-1])
        elif recent_avg > older_avg * 1.3:
            trend = 'Rising'
        elif recent_avg > older_avg * 1.1:
            trend = 'Recovering'
        elif recent_avg < older_avg * 0.7:
            trend = 'Declining'
        elif recent_avg < older_avg * 0.9:
            trend = 'Cooling'
        elif older_avg == 0 and recent_avg == 0:
            trend = 'No Data'
        else:
            trend = 'Stable'
    else:
        trend = 'N/A (1 year)'  # v2.17 FIX-7: clearer label for single-year exams

    # Importance: based on combined avg/paper
    if avg_combined >= 0.50:
        importance = 'High'
    elif avg_combined >= 0.15:
        importance = 'Medium'
    else:
        importance = 'Low'

    # Must Prepare: High importance in a majority of available years.
    # v2.15 BUG-D09 fix: threshold scales with available years instead of fixed >= 4.
    # An exam with only 3 years can now have Must Prepare subtopics (needs 3 of 3).
    high_years = sum(1 for y in all_years if avg_per_year.get(y, 0) >= 0.50)
    must_prepare_threshold = min(4, len(all_years))
    must_prepare = 'Must Prepare' if high_years >= must_prepare_threshold else '—'  # v2.17 FIX-5

    return {
        'avg_per_year': avg_per_year,
        'avg_combined': avg_combined,
        'consistency': consistency,
        'trend': trend,
        'importance': importance,
        'must_prepare': must_prepare
    }

def compute_ranks(data):
    """Compute rank_in_topic for each subtopic (by combined count within topic)."""
    topic_groups = defaultdict(list)
    for key, entry in data.items():
        topic_groups[(entry['section'], entry['topic'])].append((key, entry))
    for (section, topic), entries in topic_groups.items():
        sorted_entries = sorted(entries, key=lambda x: x[1]['total'], reverse=True)
        for rank, (key, entry) in enumerate(sorted_entries, 1):
            entry['rank_in_topic'] = rank
```

---

## §16-3 — XLSX SHEET SPECIFICATIONS

```
The Frequency xlsx has the following sheets:

SHEET 1: "Summary Dashboard"
  - Title with exam code, year range, paper count, question count
  - Year-wise overview table (papers, Qs, avg Qs/paper, per-section breakdown)
  - Top 25 most-asked subtopics (combined Qs, avg/paper, consistency, trend, importance)
  - Must Prepare section, New-in-latest-year section, Never-appeared section
  - Importance tag legend

SHEET 2: "Master Data (N Years)"
  - Full row per subtopic: Subject, Topic, Sub-Topic, Format
  - Year-wise Qs columns, Combined Qs
  - Year-wise Avg/Paper columns, Combined Avg/Paper
  - Year-wise Papers-In columns, Combined Papers-In
  - % of Subject, Importance, Consistency, Trend, Must Prepare, Rank in Topic

SHEET 3: "Topic Analysis"
  - One row per topic (aggregated from subtopics)
  - Year-wise Qs, Combined, Avg/Paper, % of Subject, Sub-Topic count

SHEET 4: "Trend Analysis & Charts"
  - Top 20 subtopics by combined avg/paper
  - Year-wise avg/paper values for charting

SHEET 5+: One sheet per section
  - Per-subtopic data within that section
  - Topic, Sub-Topic, Format, year-wise Qs, Combined, Avg, Consistency, Trend, etc.
```

---

## §16-4 — XLSX GENERATION CODE

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill('solid', fgColor='4472C4')
HEADER_FONT = Font(bold=True, color='FFFFFF', name='Arial', size=10)
DATA_FONT = Font(name='Arial', size=10)
BOLD_FONT = Font(bold=True, name='Arial', size=10)
TITLE_FONT = Font(bold=True, name='Arial', size=14)

def generate_frequency_xlsx(progress, exam_code, all_entries=None):
    """
    Generate the complete Frequency xlsx from analysis_progress.json.
    Called during synthesis phase after section_rules and manifest are written.

    v2.17: Now reads exam_config.json to get exam_total_questions per section
    for accurate % of Subject calculations. Also performs coverage validation,
    topic name consistency check, and duplicate/near-duplicate detection.

    v2.24.6 FIX B: accepts `all_entries` (the same PYQ + Zero-PYQ-scaffold list passed to
    write_subtopic_manifest()) so the workbook is taxonomy-complete and Format-parity-
    guaranteed with the manifest — see aggregate_frequency_data() docstring (§16-1).
    """
    agg = aggregate_frequency_data(progress, all_entries=all_entries)
    data = agg['subtopic_data']
    all_years = agg['all_years']
    papers_per_year = agg['papers_per_year']

    # v2.17 FIX-1: Read exam_config for real exam totals
    exam_total_questions = {}  # section_name → total Qs from exam pattern
    exam_total_all = 0
    exam_name_display = exam_code.replace('_', ' ')
    try:
        import glob as _g
        cfg_matches = sorted(_g.glob('/mnt/project/*exam_config.json'))
        if cfg_matches:
            import json as _j
            cfg = _j.load(open(cfg_matches[0], encoding='utf-8'))
            for sec in cfg.get('sections', []):
                exam_total_questions[sec['name']] = sec['q_count']
            exam_total_all = cfg.get('total_questions', 0)
            exam_name_display = cfg.get('exam_name', exam_name_display)
    except Exception:
        pass  # fallback: use section_totals from mapped data

    # v2.17 FIX-4: Check for duplicate (section, topic, subtopic) keys
    seen_keys = set()
    for key, entry in list(data.items()):
        triple = (entry['section'], entry['topic'], entry['subtopic'])
        if triple in seen_keys:
            print(f"  WARN: Duplicate subtopic '{triple[2]}' under {triple[0]}/{triple[1]}. Merging.")
        seen_keys.add(triple)

    # v2.17 FIX-6: Near-duplicate subtopic warning
    from difflib import SequenceMatcher as _SM
    topic_groups = defaultdict(list)
    for entry in data.values():
        topic_groups[(entry['section'], entry['topic'])].append(entry['subtopic'])
    for (sec, top), subs in topic_groups.items():
        for i in range(len(subs)):
            for j in range(i+1, len(subs)):
                if _SM(None, subs[i], subs[j]).ratio() > 0.75:
                    print(f"  WARN: Near-duplicate subtopics in {sec}/{top}: "
                          f"'{subs[i]}' ~ '{subs[j]}' (>75% similar)")

    # Compute metrics for all subtopics
    for key, entry in data.items():
        metrics = compute_derived_metrics(entry, all_years, papers_per_year)
        entry.update(metrics)
    compute_ranks(data)

    wb = Workbook()

    # Sheet 1: Summary Dashboard
    write_summary_dashboard(wb, data, all_years, papers_per_year, agg,
                            exam_code, exam_name_display, exam_total_all)

    # Sheet 2: Master Data
    write_master_data(wb, data, all_years, papers_per_year, exam_code,
                      exam_total_questions)

    # Sheet 3: Topic Analysis
    write_topic_analysis(wb, data, all_years, papers_per_year,
                         exam_total_questions)

    # Sheet 4: Trend Analysis
    write_trend_analysis(wb, data, all_years)

    # Per-section sheets
    sections = sorted(set(e['section'] for e in data.values()))
    for section in sections:
        sec_entries = {k: v for k, v in data.items() if v['section'] == section}
        sec_exam_total = exam_total_questions.get(section, 0)
        write_section_sheet(wb, section, sec_entries, all_years, papers_per_year,
                            sec_exam_total)

    path = f'/mnt/user-data/outputs/{exam_code}_PYQ_Frequency.xlsx'
    wb.save(path)

    # Recalculate formulas
    import subprocess
    subprocess.run(['python', '/mnt/skills/public/xlsx/scripts/recalc.py', path],
                   capture_output=True)

    # v2.17 FIX-2: Coverage validation (XLSX-F9)
    mapped_total = sum(e['total'] for e in data.values())
    if exam_total_all > 0 and abs(mapped_total - exam_total_all) / exam_total_all > 0.05:
        pct_mapped = round(mapped_total / exam_total_all * 100, 1)
        print(f"\n  ⚠ COVERAGE WARNING (XLSX-F9): Frequency xlsx accounts for {mapped_total} Qs "
              f"but exam has {exam_total_all} total ({pct_mapped}% mapped).")
        print(f"    {exam_total_all - mapped_total} questions were not classified to any subtopic.")
        print(f"    Downstream blueprint will be inaccurate. Review PYQ classification.")

    return path
```

---

## §16-5 — SHEET WRITER: SUMMARY DASHBOARD

```python
def write_summary_dashboard(wb, data, all_years, papers_per_year, agg,
                            exam_code, exam_name_display, exam_total_all):
    ws = wb.active
    ws.title = 'Summary Dashboard'
    n_years = len(all_years)
    total_papers = agg['total_papers']
    total_qs = agg['total_questions']

    year_range = f'{all_years[0]}-{all_years[-1]}' if all_years else 'N/A'
    # v2.17 FIX-9: Use exam_name_display from exam_config
    ws['A1'] = (f'{exam_name_display} PYQ Frequency Analysis '
                f'({year_range} | {n_years} Years | {total_papers} Papers | {total_qs:,} Questions)')
    ws['A1'].font = TITLE_FONT
    # v2.17: Show exam total if available and different from mapped total
    if exam_total_all > 0 and exam_total_all != total_qs:
        ws['A2'] = (f'Years: [{", ".join(str(y) for y in all_years)}] | '
                    f'Papers: {total_papers} | Questions: {exam_total_all} '
                    f'(Mapped: {total_qs})')
    else:
        ws['A2'] = (f'Years: [{", ".join(str(y) for y in all_years)}] | '
                    f'Papers: {total_papers} | Questions: {total_qs}')

    year_parts = []
    for y in all_years:
        p = papers_per_year.get(y, 0)
        q = sum(e['year_counts'].get(y, 0) for e in data.values())
        year_parts.append(f'{y}:{p}P({q:,}Q)')
    ws['A2'] = ' | '.join(year_parts)

    # Year-wise overview
    row = 4
    ws.cell(row=row, column=1, value='YEAR-WISE OVERVIEW').font = BOLD_FONT
    row += 1
    sections_list = sorted(set(e['section'] for e in data.values()))
    headers = ['Year', 'Papers', 'Total Qs', 'Avg Qs/Paper'] + sections_list + ['% of Grand Total']
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=col, value=h)
        c.font = HEADER_FONT; c.fill = HEADER_FILL
    row += 1
    for y in all_years:
        p = papers_per_year.get(y, 0)
        q = sum(e['year_counts'].get(y, 0) for e in data.values())
        ws.cell(row=row, column=1, value=y)
        ws.cell(row=row, column=2, value=p)
        ws.cell(row=row, column=3, value=q)
        ws.cell(row=row, column=4, value=round(q/p, 0) if p > 0 else 0)
        for si, sec in enumerate(sections_list):
            sec_q = sum(e['year_counts'].get(y, 0) for e in data.values() if e['section'] == sec)
            ws.cell(row=row, column=5+si, value=sec_q)
        pct = round(q / total_qs * 100, 1) if total_qs > 0 else 0
        ws.cell(row=row, column=5+len(sections_list), value=f'{pct}%')
        row += 1

    # Top 25
    row += 2
    ws.cell(row=row, column=1, value=f'TOP 25 MOST ASKED SUB-TOPICS ({n_years} Years Combined)').font = BOLD_FONT
    row += 1
    top_h = ['Rank', 'Sub-Topic', 'Subject', 'Combined Qs', 'Avg/Paper',
             'Consistency', 'Trend', 'Importance', 'Must Prepare']
    for col, h in enumerate(top_h, 1):
        c = ws.cell(row=row, column=col, value=h)
        c.font = HEADER_FONT; c.fill = HEADER_FILL
    row += 1
    sorted_by_total = sorted(data.values(), key=lambda e: e['total'], reverse=True)
    for rank, entry in enumerate(sorted_by_total[:25], 1):
        ws.cell(row=row, column=1, value=rank)
        ws.cell(row=row, column=2, value=entry['subtopic'])
        ws.cell(row=row, column=3, value=entry['section'])
        ws.cell(row=row, column=4, value=entry['total'])
        ws.cell(row=row, column=5, value=entry['avg_combined'])
        ws.cell(row=row, column=6, value=entry['consistency'])
        ws.cell(row=row, column=7, value=entry['trend'])
        ws.cell(row=row, column=8, value=entry['importance'])
        ws.cell(row=row, column=9, value=entry['must_prepare'])
        row += 1

    # Legend
    row += 2
    ws.cell(row=row, column=1, value='IMPORTANCE TAG LEGEND').font = BOLD_FONT
    row += 1
    ws.cell(row=row, column=1, value='High'); ws.cell(row=row, column=2, value='Avg/Paper >= 0.50 - MUST PREPARE'); row += 1
    ws.cell(row=row, column=1, value='Medium'); ws.cell(row=row, column=2, value='Avg/Paper 0.15-0.49 - IMPORTANT'); row += 1
    ws.cell(row=row, column=1, value='Low'); ws.cell(row=row, column=2, value='Avg/Paper < 0.15 - LOW YIELD')
```

---

## §16-6 — SHEET WRITER: MASTER DATA

```python
def write_master_data(wb, data, all_years, papers_per_year, exam_code,
                      exam_total_questions):
    ws = wb.create_sheet(f'Master Data ({len(all_years)} Years)')
    headers = ['Subject', 'Topic', 'Sub-Topic', 'Format']
    for y in all_years: headers.append(f'Qs {y}')
    headers.append('Combined Qs')
    for y in all_years: headers.append(f'Avg/Paper {y}')
    headers.append('Avg/Paper Combined')
    for y in all_years: headers.append(f'Papers In {y}')
    headers.append('Papers In Combined')
    headers += ['% of Subject', 'Importance', 'Consistency', 'Trend', 'Must Prepare', 'Rank in Topic']

    for col, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=col, value=h)
        c.font = HEADER_FONT; c.fill = HEADER_FILL
        c.alignment = Alignment(wrap_text=True, vertical='center')

    sorted_entries = sorted(data.values(), key=lambda e: (e['section'], e['topic'], e['subtopic']))
    # v2.17 FIX-1: Use exam_total_questions from exam_config as denominator
    # Fallback to section_totals (sum of mapped Qs) if exam_config absent
    section_totals_mapped = Counter()
    for e in data.values(): section_totals_mapped[e['section']] += e['total']

    row = 2
    for entry in sorted_entries:
        col = 1
        ws.cell(row=row, column=col, value=entry['section']); col += 1
        ws.cell(row=row, column=col, value=entry['topic']); col += 1
        ws.cell(row=row, column=col, value=entry['subtopic']); col += 1
        ws.cell(row=row, column=col, value=entry['format']); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=entry['year_counts'].get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=entry['total']); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=entry['avg_per_year'].get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=entry['avg_combined']); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=papers_per_year.get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=sum(papers_per_year.values())); col += 1
        # v2.17 FIX-1: % of Subject uses exam total (not mapped total)
        sec_denom = exam_total_questions.get(entry['section'], 0)
        if sec_denom == 0:
            sec_denom = section_totals_mapped.get(entry['section'], 1)
        ws.cell(row=row, column=col, value=round(entry['total']/sec_denom*100, 1) if sec_denom > 0 else 0); col += 1
        ws.cell(row=row, column=col, value=entry['importance']); col += 1
        ws.cell(row=row, column=col, value=entry['consistency']); col += 1
        ws.cell(row=row, column=col, value=entry['trend']); col += 1
        # v2.17 FIX-5: Use '—' instead of empty string for non-Must-Prepare
        ws.cell(row=row, column=col, value=entry['must_prepare'] if entry['must_prepare'] else '—'); col += 1
        ws.cell(row=row, column=col, value=entry.get('rank_in_topic', '')); col += 1
        row += 1

    # v2.17 FIX-3: Topic name consistency assertion
    master_sections = set(e['section'] for e in data.values())

    for ci in range(1, len(headers)+1):
        ws.column_dimensions[get_column_letter(ci)].width = 14
```

---

## §16-7 — SHEET WRITER: TOPIC ANALYSIS

```python
def write_topic_analysis(wb, data, all_years, papers_per_year,
                         exam_total_questions):
    ws = wb.create_sheet('Topic Analysis')
    topic_agg = defaultdict(lambda: {'year_counts': defaultdict(int), 'total': 0, 'n_subtopics': 0})
    for e in data.values():
        k = (e['section'], e['topic'])
        for y, c in e['year_counts'].items(): topic_agg[k]['year_counts'][y] += c
        topic_agg[k]['total'] += e['total']
        topic_agg[k]['n_subtopics'] += 1

    headers = ['Subject', 'Topic']
    for y in all_years: headers.append(f'Qs {y}')
    headers += ['Combined Qs']
    for y in all_years: headers.append(f'Avg/Paper {y}')
    headers += ['Avg/Paper Combined', '% of Subject', 'Sub-Topics', 'Importance', 'Rank in Subject']
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=col, value=h)
        c.font = HEADER_FONT; c.fill = HEADER_FILL

    # v2.17 FIX-1: Use exam_total_questions for % denominator
    # v2.17 FIX-8: Use full section name (no truncation)
    section_totals_mapped = Counter()
    for (sec, _), a in topic_agg.items(): section_totals_mapped[sec] += a['total']
    sorted_topics = sorted(topic_agg.items(), key=lambda x: (x[0][0], -x[1]['total']))
    section_ranks = defaultdict(int)
    row = 2
    for (section, topic), a in sorted_topics:
        section_ranks[section] += 1
        col = 1
        # v2.17 FIX-3 + FIX-8: section name must be IDENTICAL to Master Data
        ws.cell(row=row, column=col, value=section); col += 1
        ws.cell(row=row, column=col, value=topic); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=a['year_counts'].get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=a['total']); col += 1
        for y in all_years:
            p = papers_per_year.get(y, 0)
            ws.cell(row=row, column=col, value=round(a['year_counts'].get(y,0)/p, 2) if p > 0 else 0); col += 1
        total_p = sum(papers_per_year.values())
        ws.cell(row=row, column=col, value=round(a['total']/total_p, 2) if total_p > 0 else 0); col += 1
        # v2.17 FIX-1: % of Subject uses exam total (not mapped total)
        sec_denom = exam_total_questions.get(section, 0)
        if sec_denom == 0:
            sec_denom = section_totals_mapped.get(section, 1)
        ws.cell(row=row, column=col, value=round(a['total']/sec_denom*100, 1) if sec_denom > 0 else 0); col += 1
        ws.cell(row=row, column=col, value=a['n_subtopics']); col += 1
        avg_c = round(a['total']/total_p, 2) if total_p > 0 else 0
        ws.cell(row=row, column=col, value='High' if avg_c >= 0.50 else ('Medium' if avg_c >= 0.15 else 'Low')); col += 1
        ws.cell(row=row, column=col, value=section_ranks[section]); col += 1
        row += 1
```

---

## §16-8 — SHEET WRITER: TREND ANALYSIS & PER-SECTION

```python
def write_trend_analysis(wb, data, all_years):
    ws = wb.create_sheet('Trend Analysis & Charts')
    ws.cell(row=1, column=1,
            value=f'Top 20 Sub-Topics: Avg/Paper Across All {len(all_years)} Years').font = BOLD_FONT
    headers = ['Sub-Topic'] + [str(y) for y in all_years] + ['Combined', 'Subject']
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=2, column=col, value=h)
        c.font = HEADER_FONT; c.fill = HEADER_FILL
    top_20 = sorted(data.values(), key=lambda e: e['avg_combined'], reverse=True)[:20]
    row = 3
    for entry in top_20:
        col = 1
        ws.cell(row=row, column=col, value=entry['subtopic']); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=entry['avg_per_year'].get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=entry['avg_combined']); col += 1
        ws.cell(row=row, column=col, value=entry['section'][:20]); col += 1
        row += 1

def write_section_sheet(wb, section, section_entries, all_years, papers_per_year,
                        sec_exam_total):
    sheet_name = section[:31].replace('/', ' ')
    ws = wb.create_sheet(sheet_name)
    headers = ['Topic', 'Sub-Topic', 'Format']
    for y in all_years: headers.append(f'Qs {y}')
    headers.append('Combined Qs')
    for y in all_years: headers.append(f'Avg {y}')
    headers.append('Avg Combined')
    for y in all_years: headers.append(f'PapersIn {y}')
    headers += ['% of Subject', f'Consistency (of {len(all_years)})', 'Trend', 'Importance', 'Must Prepare', 'Rank in Topic']
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=col, value=h)
        c.font = HEADER_FONT; c.fill = HEADER_FILL
        c.alignment = Alignment(wrap_text=True, vertical='center')

    sorted_e = sorted(section_entries.values(), key=lambda e: (e['topic'], e['subtopic']))
    # v2.17 FIX-1: Use exam total as denominator for % of Subject
    section_total_mapped = sum(e['total'] for e in section_entries.values())
    sec_denom = sec_exam_total if sec_exam_total > 0 else section_total_mapped
    row = 2
    for entry in sorted_e:
        col = 1
        ws.cell(row=row, column=col, value=entry['topic']); col += 1
        ws.cell(row=row, column=col, value=entry['subtopic']); col += 1
        ws.cell(row=row, column=col, value=entry['format']); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=entry['year_counts'].get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=entry['total']); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=entry['avg_per_year'].get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=entry['avg_combined']); col += 1
        for y in all_years:
            ws.cell(row=row, column=col, value=papers_per_year.get(y, 0)); col += 1
        ws.cell(row=row, column=col, value=round(entry['total']/sec_denom*100, 1) if sec_denom > 0 else 0); col += 1
        ws.cell(row=row, column=col, value=entry['consistency']); col += 1
        ws.cell(row=row, column=col, value=entry['trend']); col += 1
        ws.cell(row=row, column=col, value=entry['importance']); col += 1
        # v2.17 FIX-5: Use '—' instead of empty string
        ws.cell(row=row, column=col, value=entry['must_prepare'] if entry['must_prepare'] else '—'); col += 1
        ws.cell(row=row, column=col, value=entry.get('rank_in_topic', '')); col += 1
        row += 1
    for ci in range(1, len(headers)+1):
        ws.column_dimensions[get_column_letter(ci)].width = 13
```

---

## §16-9 — XLSX VALIDATION

```
Before delivering the xlsx, verify ALL 9 items:

  XLSX-F1: Workbook has correct sheet count: 4 + sections_count
  XLSX-F2: Master Data row count = total unique (section, topic, subtopic) keys
  XLSX-F3: Year columns match _meta.years_processed exactly
  XLSX-F4: Combined Qs = sum of all year Qs (verified per row)
  XLSX-F5: papers_per_year values match _meta.papers_processed count per year
  XLSX-F6: Consistency value = count of years where Qs > 0 (per row)
  XLSX-F7: No division-by-zero errors (papers_per_year=0 handled)
  XLSX-F8: Per-section sheet subtopic count = Master Data count for that section
  XLSX-F9: sum(all subtopic Combined Qs) vs exam_config.total_questions:
           if mismatch > 5% → WARN (classification gaps exist)
           if mismatch > 25% → HARD WARN (downstream blueprint will be inaccurate)
           Note: XLSX-F9 requires exam_config.json. If absent, skip with note.
```

---

## §16-10 — FREQUENCY XLSX EDGE CASES

```
EC-F1: EXAM WITH ONLY 1 YEAR OF DATA
  Trend = "Insufficient Data". Single year column. Structure unchanged.

EC-F2: SUBTOPIC WITH 0 QUESTIONS ACROSS ALL YEARS
  Appears in Master Data with all zeroes. Consistency=0. Trend="No Data".
  Importance="Low". These are taxonomy subtopics with no PYQ observed (Zero-PYQ
  scaffolds). v2.24.6 FIX B: now reachable-by-construction — aggregate_frequency_data
  seeds every all_entries subtopic (PYQ + Zero-PYQ) BEFORE scanning progress, so this
  row exists even though it has no progress[] key. Was previously UNREACHABLE via the
  taxonomy-sync path (progress-only iteration structurally excluded Zero-PYQ scaffolds) —
  this note was aspirational until v2.24.6 closed the gap (see Framework_Blueprint FIX A/B).

EC-F3: VERY LARGE NUMBER OF YEARS (10+)
  Columns grow linearly. No structural issue.

EC-F4: SECTION NAME TOO LONG FOR SHEET TAB
  Truncate: section[:31].replace('/', ' '). Excel 31-char limit.

EC-F5: PAPERS_PER_YEAR = 0 FOR A YEAR
  Avg/Paper = 0 for that year (division guarded).

EC-F6: FORMAT DETECTION UNCERTAINTY (v2.24.6 FIX B — REVISED)
  When all_entries is supplied (the standard run_synthesise path), Format is taken
  directly from entry['format'] — the SAME 4-way TEXT/FIGURAL/PASSAGE/DI value
  synthesise_subtopic computed and write_subtopic_manifest() writes to the manifest.
  There is no separate "detection uncertainty" in this path: Excel Format == manifest
  Format by construction, not by chance. TEXT-as-default only applies in the backward-
  compat path (all_entries=None) or for a genuinely absent/malformed value.
  Step 6 (Framework_Blueprint v1.32+) no longer reads Format from this xlsx at all —
  the manifest is authoritative there; this Excel Format column is advisory-only
  (cross-check, ref Blueprint §6 S6-1b).
```

# ════════════════════════════════════════════════════════════════════════

# END OF Framework_MockTestAnalyse v2.24.8
