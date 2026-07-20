# Framework_PYQAnalyse v2.16 — Universal PYQ Analysis & Taxonomy Builder
#
# v2.16 — 2026-07-20 — PYQ CORPUS DRIVE-ONLY STANDARDIZATION, STEP 2b/PYQScan (twin fix:
#   Framework_MockTestAnalyse.md Step 5/PYQExtract v2.24.8). Found during a project-level
#   audit: three pipeline steps that all handle the SAME document class (Row/Sorted PYQ
#   .docx corpus files) disagreed on whether Google Drive was required — Step 4 (PYQCount,
#   this file) always mandated Drive with no fallback; this step (Step 2b/PYQScan) allowed
#   an uploads-only fallback; Step 5 (PYQExtract) allowed the broadest fallback (project/
#   uploads). STANDARDIZED to Step 4's existing Drive-only rule (confirmed with
#   Radheshyam) — Row files must be in Google Drive for --scan mode now, same as
#   --counts mode always required. WHAT CHANGED:
#     Header, S1-1 trigger parsing, S1-2 mode validation, S1-2 file inventory — PYQ:
#       <<Drive link>> is now REQUIRED for --scan mode; absent → HARD STOP (was: silent
#       fallback to /mnt/user-data/uploads/).
#     collect_row_files() (§3 S3-2) — removed the 'uploads' source branch entirely;
#       now takes drive_folder_id as a required argument and raises SystemExit if
#       absent, instead of silently scanning uploads/.
#   --taxonomy mode (Exam Syllabus/Pattern docs) and --approve mode (scan_progress.json)
#   are UNAFFECTED — those are a different document class (small config/state files),
#   not the PYQ corpus, and remain project/uploads-eligible per existing architecture.
#   Does not touch taxonomy-building logic, batch processing, or gate/mandate checks.
#   Verified: validate_framework_md.py (0 issues, AST-clean).
#
# v2.15 — 2026-07-18 — LOCAL-COPY CORRUPTION REPAIR (B-PYAST false positive; zero content/
#   logic change). This project's local Files-section copy of this spec had silently DROPPED
#   2 markdown code-fence lines somewhere between §D6-3 (the "pass" / NOTE comment ending the
#   dimensional-split-detection block) and §D6-4/D6-5 (the split-governance-guards block) —
#   a closing ``` after the v2.13 NOTE comment, and an opening ```python before
#   reclassify_after_refinement(). Missing fences caused validate_framework_md.py to parse
#   two separate, independently-valid Python blocks as one contiguous block, producing a
#   false "invalid syntax (line 188 of block)" AST error at the boundary. Verified via direct
#   byte-for-byte diff against the canonical framework-specs GitHub repo (production branch,
#   commit 74d395f) that the CANONICAL source was never affected — this was local-copy
#   corruption only, likely introduced during an earlier Files-section upload/sync, not a
#   spec defect. Fix: restored both fence lines exactly as they exist upstream. Confirmed
#   post-fix: this file is now byte-identical to the canonical GitHub copy in its entirety
#   (diff clean, matching line count). No prose, code, gate, or rule content changed.
#
# v2.14 changes: FORMAT AUTHORITY RECONCILIATION (register D6-11). S3-3b reconcile_format()
#   makes the authoritative full-parse format (PYQSort Phase A) supersede the lightweight
#   scan's provisional OMML-obscured/figure-inferred tokens, so a mis-scanned math/figural
#   item no longer drives the wrong Format/CONCEPT_GROUP/class downstream. reconcile_stats()
#   flags a >20% correction rate for review. Verified by fmt_harness (16/16).
#
# v2.13 changes: SPLIT GOVERNANCE GUARDS (register D6-4/D6-5). Deterministic helpers that
#   enforce the previously prose-only split rules: split_children_valid() flags near-duplicate
#   split children (over-split) so they are merged back (high-precision: singular/plural, paren-
#   variants, exact dups; borderline pairs left to Q3/QV-13 to avoid false merges); merge_record()
#   captures distinct forms merged into one subtopic (under-split) so Step 7 scenario_key still
#   separates them. Verified by split_harness (14/14).
#
# v2.12 changes: NAME-QUALITY GATES (register D6-1/D6-2).
#   (1) NAME-SHAPE VALIDATION: HARD STOP on question-shaped subtopic/topic names
#       (ends with '?', >80 chars, or interrogative-initial) — stops a raw PYQ question
#       being captured as a subtopic and then allocated/generated (occurred in the SSC CGL
#       run). High-precision: 0 false positives on 31 real labels.
#   (2) canon_name(): NFC + dash/whitespace/case folding for COMPARING/COUNTING names, so
#       trivial drift never phantom-splits a subtopic (complements Task 2.5). Display keeps
#       the original name. Verified by name_harness (46/46).
# [ExamCode] project | Steps 2a/2b/2c + 4 (PYQDraft/PYQScan/PYQApprove/PYQCount) | Exam-agnostic
#
# PURPOSE:
#   Build the authoritative 3-level taxonomy (Subject > Topic > Subtopic) and
#   produce a single merged Analysis Word Document for any competitive exam.
#   This Analysis doc is a mandatory input to Step 6 (MockBlueprint). The taxonomy also serves
#   as the classification reference for PYQSort (Framework_PYQSort.md).
#
# PIPELINE POSITION:
#   Step 1  PYQ Prepare  → raw PYQ .docx to Row file
#   PYQAnalyse           → THIS SPEC (taxonomy + Analysis doc)
#   Step 3  PYQSort      → 1 Row file → 1 Sorted PYQ (uses approved Analysis doc as taxonomy)
#   Step 5  PYQExtract   → Sorted PYQ → section_rules.md + manifest + Frequency .xlsx
#   Step 6  MockBlueprint → Analysis doc + Frequency xlsx → blueprint.json
#   Steps 7–11           → Mock test creation pipeline
#
#   PYQAnalyse has 4 modes that run at different points in the pipeline:
#     --taxonomy + --scan + --approve  run BEFORE PYQSort (build & lock taxonomy)
#     --counts                         runs AFTER  PYQSort (fill PYQ counts)
#
# PREREQUISITE:
#   Step 1 (PYQ Prepare) must have already converted raw exam dumps into standardized
#   Row files (.docx with Q.1–Q.N, date labels [DD-Mon-YYYY <session_keyword> X] or
#   [DD-Mon-YYYY] when session is not applicable, no answers/explanations/metadata).
#   Session part in date labels is OPTIONAL — single-session exams omit it.
#   PYQAnalyse and PYQSort both expect Row file format.
#   If Row files don't exist: run Step 1 PYQ Prepare first.
#
# INPUTS (by mode):
#   --taxonomy : Exam Syllabus (ANY format: image/PDF/.docx/plain text)
#                Exam Pattern  (ANY format: image/PDF/.docx/.xlsx/plain text)
#                  PREFERRED: .xlsx with 3 standardized tabs (Overview/Sections/Range)
#                  See S2-2 for xlsx parser specification.
#   --scan     : Row files (.docx) — from Google Drive (required, v2.16)
#                scan_progress.json (for resume across sessions)
#   --approve  : scan_progress.json (completed scan)
#   --counts   : Sorted PYQ files from Google Drive (output of PYQSort)
#
# OUTPUTS (by mode — CLOSED SETS, see §10 S10-1 for full contract):
#   --taxonomy : [ExamCode]_taxonomy_draft.json + [ExamCode]_exam_config.json
#                (2 files, nothing else)
#   --scan     : [ExamCode]_scan_progress.json + [ExamCode]_classifications.json
#                (2 files, nothing else — taxonomy lives INSIDE scan_progress.json)
#   --approve  : [ExamCode]_PYQ_Analysis.docx + [ExamCode]_exam_config.json
#                (2 files, nothing else)
#   --counts   : [ExamCode]_PYQ_Analysis.docx (UPDATED with PYQ counts)
#                (1 file, nothing else — count_progress.json is internal)
#
#   DELIVERABLE SET IS CLOSED: each mode delivers EXACTLY the files listed
#   and NOTHING ELSE. See §10 S10-1 for DO-NOT-DELIVER lists per mode
#   and S10-2 for the pre-delivery checklist. Creating unauthorized files
#   is a spec violation (same class as anti-editorializing violations).
#
# TRIGGER FORMAT:
#   Step 2a: PYQDraft [ExamCode]          (ExamCode provided ONLY here, saved in exam_config.json)
#   Step 2b: PYQScan                      (reads ExamCode from exam_config.json)
#   Step 2b: PYQScan PYQ: <<Google Drive folder link>>  (required, v2.16 — Drive source for Row files)
#   Step 2c: PYQApprove                   (reads ExamCode from exam_config.json)
#   Step 4:  PYQCount PYQ: <<Google Drive folder link>>  (reads ExamCode from exam_config.json)
#
#   Trigger matching is case-insensitive.
#   ExamCode: alphanumeric + underscore only (e.g. SSC_CGL_TIER1, GATE_CS).
#   ExamCode is typed ONCE in Step 2a, then auto-read from exam_config.json in all later steps.
#
# PROJECT SETUP:
#   ALL modes run in [ExamCode] project (exam-specific).
#   After --approve: Analysis doc + exam_config.json are already in project.
#   After --counts: user downloads updated Analysis doc → input for Step 5 + Step 6.
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains zero hardcoded exam values.
#   All section names, topic names, subtopic names → derived from syllabus + PYQ.
#   Same spec runs for SSC CGL (4 sections), GATE CS (1 section), or any exam.
#
# VERSION HISTORY:
#   v2.11 — 2026-07-07 — OPTIONAL SESSION IN DATE LABELS (Step 1 sync).
#           PREREQUISITE section updated: date labels can be [DD-Mon-YYYY] without
#           session (single-session exams). Framework_PYQPrepare v1.1 makes session
#           optional in the trigger. PYQAnalyse date detection (\d{1,2} day pattern)
#           already handles both forms — this is a documentation-only fix.
#   v2.10 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S10-4: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. All 4 modes (--taxonomy, --scan,
#           --approve, --counts) now render the standardized visual footer after
#           every present_files call. Zero logic change.
#   v2.9 — 2026-07-06 — BATCH STOP LAW + DELIVERABLE SET CONTRACT (1 new section, 2 rewrites, 10 fixes).
#           ROOT CAUSE 1 — BATCH STOP LAW: SSC CGL Tier 2 PYQScan — Claude
#           auto-advanced from Batch 1 to Batch 2 in the same response without
#           waiting for user's "continue" trigger. 7 structural gaps identified
#           by comparing how MockCreate enforces the same rule (MANDATE 1) vs
#           how PYQAnalyse expressed it (item 7 in Anti-Editorializing Rule).
#
#           ROOT CAUSE 2 — DELIVERABLE SET: SSC CGL Tier 2 PYQScan — Claude
#           delivered an unauthorized taxonomy_draft_v2.json alongside the
#           spec-defined scan outputs. The spec had no CLOSED DELIVERABLE SET
#           contract — outputs were listed in the header but nothing said
#           "these files and NOTHING ELSE." 4 structural gaps identified by
#           comparing how MockCreate enforces delivery (S13-6 closed set,
#           S13-7 pre-delivery checklist, R-DELIVER rule) vs PYQAnalyse
#           (one-liner in header, no DO-NOT-DELIVER, no pre-delivery gate).
#
#           BATCH STOP LAW CHANGES:
#           (1) NEW S3-4a — BATCH STOP LAW: dedicated mandate-level section
#               with failure history, continue trigger contract, small-corpus
#               clarification, final-batch exception, and forbidden behaviors.
#               Same architectural weight as MockCreate's MANDATE 1 / B-1..B-8.
#           (2) S3-4 convergence gate docstring: "CONTINUE scanning without
#               discussion" rewritten to explicitly say "STOP THE RESPONSE and
#               wait for user's continue trigger — without discussion means
#               do not editorialize, NOT auto-advance." This single line was
#               the primary cause of the failure — Claude read it as an
#               instruction to auto-advance silently.
#           (3) S3-5 run_scan() batch gate: expanded from 2-line comment to
#               6-line block with "Write nothing more. Generate nothing more."
#               and cross-reference to S3-4a + MockCreate MANDATE 1 STEP 6.
#           (4) S3-4 Anti-Editorializing items 7-8: added explicit note that
#               the response ENDS after printing items 1-7 (S3-4a reference).
#           (5) §12 DoD: batch gate checklist item expanded with S3-4a reference
#               and explicit "including small corpora" qualifier.
#           (6) S3-4a STEP 3 + S3-5 run_scan(): added present_files call for
#               scan_progress.json + classifications.json after each non-final
#               batch. Previously files were saved to disk silently with no
#               download link — user could not grab progress for session resume.
#               Matches MockTestAnalyse S8-3 pattern (summary → present_files
#               → continue prompt). Continue prompt is always the LAST line.
#
#           CROSS-FRAMEWORK NOTE: Phase B counting (S5-7/S5-8) uses a Python
#           script execution model where all batches run in one script call —
#           the Batch Stop Law does NOT apply to script-executed batches (the
#           script handles its own save-after-each-batch logic). The law applies
#           to interactive chat-based batch processing only (Phase 0b scan).
#           MockTestAnalyse (PYQExtract) has its own batch gate via Options A/B
#           pattern — verify that framework separately.
#
#           DELIVERABLE SET CONTRACT CHANGES:
#           (7) §10 REWRITTEN — DELIVERABLE SET CONTRACT: closed deliverable
#               sets for all 4 modes (--taxonomy, --scan, --approve, --counts).
#               Each mode defines EXACTLY which files to deliver and an explicit
#               DO-NOT-DELIVER list of internal/intermediate files. Pre-delivery
#               checklist (S10-2) blocks present_files until the call contains
#               EXACTLY the expected files and nothing else.
#               Mirrors MockCreate's S13-6 (closed set), S13-7 (pre-delivery
#               checklist), and R-DELIVER (named rule).
#               LIVE FAILURE: SSC CGL Tier 2 --scan delivered an unauthorized
#               taxonomy_draft_v2.json because no "NOTHING ELSE" qualifier
#               existed and no DO-NOT-DELIVER list blocked extra files.
#           (8) Header OUTPUTS section: updated with "(N files, nothing else)"
#               qualifiers and cross-reference to §10. classifications.json
#               now explicitly listed (was changelog-only since v1.7 C2).
#           (9) S2-6, S3-5, S3-7, S4-3, S5-5, S5-8: delivery instructions
#               updated to reference S10-1 closed set and S10-2 pre-delivery
#               checklist.
#           (10) §12 DoD: all 4 phases updated with closed-set verification
#               items and pre-delivery checklist pass requirement.
#
#   v2.8 — 2026-07-06 — SYLLABUS-ENUMERATED ITEMS MUST BECOME SUBTOPICS.
#           ROOT CAUSE: Comparative analysis of framework-generated (68 subtopics) vs
#           PYQ-grounded (209 subtopics) Analysis docs for SSC CGL Tier 1 revealed a
#           3× subtopic gap. The merge-over-split bias (v2.4) was too aggressive —
#           Claude interpreted it as "if the Topic name covers it, don't create
#           subtopics", producing 1:1 Topic=Subtopic mappings (e.g., "Geometry" → 1
#           subtopic "Geometry" despite the syllabus explicitly listing Triangles,
#           Circles, Polygons as separate items). This is data loss, not conservative
#           merging.
#
#           CHANGE 1 — S2-3 CORE PRINCIPLE: Added CRITICAL SCOPE OF MERGE BIAS
#             clarification. The merge bias applies ONLY to AI-invented splits, NOT
#             to items the syllabus itself explicitly enumerates. Suppressing
#             syllabus-enumerated items is data loss. Added SSC CGL Tier 1 counter-
#             evidence alongside the MPPSC Botany evidence.
#           CHANGE 2 — S2-3 Step 1 GROUPING RULE: Added GROUPED ITEMS ARE SUBTOPICS
#             mandatory rule. When multiple syllabus items are grouped into one Topic,
#             every grouped item MUST become a named subtopic. Includes 3 failure
#             examples (Geometry, Trigonometry, Polity) with correct vs wrong output.
#           CHANGE 3 — S2-3 Step 1 GROUPING RULE: Added 1:1 TOPIC=SUBTOPIC DETECTOR
#             self-check. After subtopic derivation, any Topic with exactly 1 subtopic
#             of the same name is flagged for re-derivation (unless the syllabus
#             genuinely lists it as a single atomic concept).
#           CHANGE 4 — §12 DoD Phase 0a: Added 1:1 Topic=Subtopic check item.
#
#   v2.7 — 2026-07-06 — CATCH-ALL / RESIDUAL TOPIC PROHIBITION.
#           ROOT CAUSE: Live execution on SSC CGL Tier 2 produced "Topic 17: Other
#           Sub-topics" containing Blood Relations, Seating Arrangement, Syllogism,
#           Dice and Cubes, Ranking and Ordering, Logical Sequence — all distinct
#           question types that should be separate Topics. Claude ran out of patience
#           while processing a long syllabus and dumped remaining items into a residual
#           bin, violating the Topic Integrity Test.
#
#           CHANGE 1 — S2-3 Step 1: Added CATCH-ALL / RESIDUAL TOPIC PROHIBITION
#             rule with explicit banned patterns (case-insensitive substring match):
#             "other", "miscellaneous", "misc", "remaining", "additional",
#             "general topics", "catch-all", "residual". Includes failure example
#             from SSC CGL Tier 2 and mandatory self-check after Topic derivation.
#           CHANGE 2 — S2-3 EXCLUSION RULES: Added matching prohibition at Subtopic
#             level — same banned patterns apply to Subtopic names.
#           CHANGE 3 — S2-3 QUALITY GATE: Added CATCH-ALL NAME CHECK as a mandatory
#             gate that runs after all other quality gates. HARD STOP if any
#             Topic or Subtopic name matches a banned pattern.
#           CHANGE 4 — §12 DoD Phase 0a: Added catch-all name check item.
#
#   v2.6 — 2026-07-06 — MERGED ANALYSIS DOC (single file replaces per-subject files).
#           ROOT CAUSE: Phase 0c produced one .docx per subject (e.g. 4 files for SSC
#           CGL Tier 1). This created unnecessary file management overhead: N+1 files
#           to upload, track, and version; risk of missing one subject's doc during
#           upload; partial-update risk during Phase B; and the "missing ONE subject"
#           fallback (S10-6 in downstream Blueprint) that was fragile. Every downstream
#           parser (PYQSort, Step 5, Step 6) already identifies sections by CONTENT
#           (the "Subject: [Name]" header inside the doc), not by filename — so the
#           per-file split had no technical justification.
#
#           CHANGE 1 — S4-1: Output is now a single [ExamCode]_PYQ_Analysis.docx
#             containing ALL subjects, separated by page breaks. Internal structure
#             per subject is unchanged (header block, master summary table, per-topic
#             subtopic tables, footer). File management drops from N+1 to 2 files
#             (1 Analysis doc + 1 exam_config.json).
#           CHANGE 2 — S4-2: generate_analysis_doc() → generate_merged_analysis_doc()
#             accepts full taxonomy dict, iterates all subjects with page breaks.
#           CHANGE 3 — S4-4: Approval gate message updated for single-file output.
#             Lists sections within the doc instead of separate filenames.
#           CHANGE 4 — S5-4b/S5-5/S5-8: Phase B references updated from plural
#             "Analysis docs" to singular "Analysis doc" — same parsing logic, single
#             file load/save instead of per-file iteration.
#           CHANGE 5 — S10-3/S10-4: Delivery sections updated for single file.
#           CHANGE 6 — §7 Name Consistency: "Analysis docs" → "Analysis doc".
#           CHANGE 7 — §12 DoD Phase 0c: "One Analysis .docx per subject" →
#             "Single merged Analysis .docx with all subjects".
#           CHANGE 8 — S1-2 --counts mode, EC-P1, EC-P29: plural → singular.
#
#           All downstream consumers (PYQSort, Step 5, Step 6) require NO spec
#           changes — they already parse by content pattern, not file boundary.
#           The downstream specs use glob patterns or direct file load; both work
#           with a single file. Cross-step contract unchanged.
#
#   v2.5 — 2026-07-06 — STANDARDIZED EXAM PATTERN XLSX + EXAM_CONFIG SCHEMA OVERHAUL.
#           ROOT CAUSE: Exam pattern was read via AI interpretation of image/PDF/docx —
#           ambiguous, non-deterministic, and unable to capture per-range marking schemes
#           (e.g., CSIR NET Part C: 4 marks/Q vs Part A/B: 2 marks/Q), attempt limits
#           (e.g., CSIR NET: attempt 15/20 in Part A), or academic level. Validated
#           against 7 exam patterns: SSC CGL T1/T2, MPSC Botany, CSIR NET Life Science,
#           CSIR NET Mathematical Science, GATE Biotechnology, IIT JAM Chemistry.
#
#           CHANGE 1 — S1-2 + S2-2: XLSX AS PREFERRED INPUT FORMAT:
#             Exam pattern now accepted as .xlsx with 3 standardized tabs:
#               Tab 1 "Overview": key-value pairs (Total Questions, Medium, Question Type,
#                 Total Marks, Duration, Level)
#               Tab 2 "Sections": table (Section, Total Question, Question Starts,
#                 Question Ends, Max Attempt)
#               Tab 3 "Range": table (Question Range, Question Type, Correct Marks,
#                 Negative Marks)
#             Deterministic parser replaces AI interpretation. Legacy image/PDF/docx
#             path preserved as backward-compatible fallback.
#
#           CHANGE 2 — S2-2: 10 STRUCTURAL VALIDATIONS ON XLSX:
#             V1: Σ(Total Question) == Total Questions (Overview)
#             V2: Q_Ends − Q_Starts + 1 == Total Question (per section)
#             V3: Section Q-ranges contiguous and non-overlapping
#             V4: Range tab tiles Q.1 through Total Questions completely
#             V5: All Negative Marks ≤ 0
#             V6: Σ(Max Attempt × correct_marks) == Total Marks
#             V7: 0 < Max Attempt ≤ Total Question (per section)
#             V8: Overview Question Type set == Range tab distinct types
#             V9: All Correct Marks > 0
#             V10: Total Questions > 0, Duration > 0
#             Any failure → HARD STOP with specific error.
#
#           CHANGE 3 — S2-2: SECTION ≠ SUBJECT CLARIFICATION:
#             Section names from Sections tab are OTS (Online Test Series) display labels
#             only. They do NOT define Subject names for the taxonomy. The syllabus
#             (provided separately) defines Subjects, Topics, and Subtopics. A single
#             Subject can span multiple sections (e.g., CSIR NET: "Cell Biology" questions
#             appear in both Part B and Part C). The framework must never conflate
#             Section with Subject.
#
#           CHANGE 4 — S2-5: EXAM_CONFIG.JSON SCHEMA OVERHAUL:
#             Removed: marks_per_question (single int), negative_marking (single float).
#             Added: medium (str), question_types (list), level (str),
#               marking_scheme[] (per-range: q_range, question_type, correct_marks,
#               negative_marks), max_attempt (per section).
#             Per-range marking replaces global scalars — handles CSIR NET (2m vs 4m),
#             GATE (1m vs 2m, MCQ vs MSQ vs NAT per range), IIT JAM (MCQ/MSQ/NAT
#             sections with mixed marks). Float marks supported (CSIR NET Math: 4.75).
#
#           CHANGE 5 — S2-6 DELIVERY MESSAGE: includes new fields.
#           CHANGE 6 — §12 DoD: updated for xlsx validation + new schema fields.
#
#   v2.4 — 2026-07-05 — TAXONOMY DEPTH ARCHITECTURE OVERHAUL (S2-3 rewrite).
#           ROOT CAUSE: v1.5's "when in doubt, SPLIT" + mandatory 6 pattern dimensions
#           produced 336 subtopics for MPPSC Botany (81 syllabus entries → 4.1× inflation).
#           PYQ classification then failed on 38% of questions (93/150 mapped). Root cause
#           traced via comparative analysis of 13 exam syllabi: SSC CGL T1/T2, CAT, MPPSC
#           Botany, CSIR NET Life Sci, GATE CS, GATE Biotech, IIT JAM Physics, UGC NET
#           History, CUET PG Math, CUET UG Political Sci, NEET, CTET Paper 1.
#
#           CORE PRINCIPLE — UNIQUE DOMAIN PROPERTY:
#             Every subtopic must uniquely claim a concept set that no other subtopic also
#             claims. Given any PYQ question, exactly ONE subtopic must be the unambiguous
#             best match. Over-splitting violates this by creating near-duplicate bins that
#             confuse the classifier. Over-merging preserves it (loses granularity but
#             classifies 100% of questions). Default bias: MERGE over SPLIT.
#
#           CHANGE 1 — S2-3 COMPLETE REWRITE:
#             Replaced "6 mandatory pattern dimensions applied to every Topic" with a
#             3-question per-entry decision tree (Q1: explicit identifier? Q2: internal
#             sub-structure? Q3: Unique Domain Check). The 6 dimensions are retained as
#             an OPTIONAL tool for undivided-block entries only, not a mandatory universal
#             procedure. Subtopic derivation default reversed from "SPLIT" to "follow
#             syllabus structure faithfully."
#           CHANGE 2 — EXCLUSION RULES:
#             Vocabulary lists, glossary terms, named reactions, individual organisms,
#             historical terms, and enumerated scope items within colon-descriptors are
#             explicitly excluded from becoming subtopics.
#           CHANGE 3 — SANITY CHECKS:
#             Added ratio guardrail (flag at 2.0×, hard-stop at 3.0×), near-duplicate
#             detection (>75% name similarity), keyword overlap check (<30%), and
#             total-coverage verification (every syllabus concept → exactly 1 subtopic).
#           CHANGE 4 — QUALITY GATE REWRITE:
#             Replaced fixed benchmark (150–250 subtopics) with ratio-based guardrail
#             that scales to any exam size.
#           CHANGE 5 — §3-6 REFINEMENT PASS DEFAULT BIAS:
#             Changed from "split broad subtopics" to "merge confused subtopics first,
#             split only with ≥15 Qs evidence + Q3 Unique Domain Check pass."
#           CHANGE 6 — §11 and §12 UPDATED:
#             Exam-agnostic guarantee and DoD updated to reflect new taxonomy rules.
#
#           Validated against 13 exams: all produce ratio ≤ 2.6×. The MPPSC Botany
#           disaster (4.1×) would be prevented (ratio = 1.0× under new rules).
#   v2.3 — 2026-07-05 — PHASE 0b CONSISTENCY FIXES (3 issues).
#           (1) MEDIUM — S3-2 vs S3-7 CONTRADICTION: S3-2 said "no re-listing
#               on resume" but S3-7 (v2.2) said "RE-LIST". FIXED: S3-2 cached
#               inventory section now defers to S3-7 for resume behaviour.
#               First-session caching unchanged; resume re-lists per S3-7.
#           (2) LOW-MEDIUM — ANTI-EDITORIALIZING RULE UPDATED (S3-4): the
#               "NOTHING ELSE" allowed list now explicitly includes v2.2's
#               per-section Q distribution and classification quality output.
#               Without this, Claude could interpret v2.2 additions as violating
#               the anti-editorializing rule.
#           (3) LOW — total_available META UPDATE (S3-5): run_scan now writes
#               total_available to progress['_meta']['total_available'] before
#               first batch. Without this, saved scan_progress.json permanently
#               showed total_available=0 (the init default), breaking convergence
#               gates on resume if they read from _meta instead of parameter.
#   v2.2 — 2026-07-05 — PHASE 0b DEEP-AUDIT (4 gap fixes).
#           (1) HIGH — POST-CONVERGENCE SUMMARY (S3-5 updated): before printing
#               "Run: PYQApprove", display a comprehensive summary: original
#               taxonomy size vs final (after scan + refinement), net discovery
#               (+N new, +M from splits, -K removed), classification quality
#               (normal vs OMML-obscured vs figure-inferred percentages),
#               per-section snapshot (section → topics → subtopics), and papers
#               scanned per year. User needs full visibility before locking.
#           (2) MEDIUM — CLASSIFICATION QUALITY TRACKING (S3-5 batch-end updated):
#               after each batch, show per-section Q-count AND quality breakdown
#               (normal / OMML-obscured / figure-inferred counts). Surfaces
#               degraded classification rates early — if 40%+ are OMML-obscured,
#               the scan might miss patterns.
#           (3) LOW-MEDIUM — BATCH-END PER-SECTION Q-COUNT (S3-5 batch-end
#               updated): show per-section classified Q distribution after each
#               batch. Catches section detection failures (wrong marker_mode or
#               Q-range config) within the first batch, not after 60+ papers.
#           (4) LOW-MEDIUM — RESUME DRIVE RE-VERIFICATION (S3-7 updated): resume
#               sessions now re-list Drive files and re-run S3-2a pre-scan gate
#               instead of relying on cached inventory. Catches files added or
#               removed between sessions. Aligned with Phase B's S5-7 pattern.
#           §12 Phase 0b DoD updated: 3 new items.
#   v2.1 — 2026-07-05 — PRE-SCAN CONFIRMATION GATE (1 addition).
#           (1) NEW S3-2a — PRE-SCAN CONFIRMATION GATE: after collecting and
#               ordering all Row files (S3-2) but before any batch scanning
#               (S3-3/S3-5), display a year-wise paper inventory table with
#               per-paper Q counts (verified by parsing or from filename
#               pattern). Wait for explicit user confirmation before proceeding.
#               Proves Claude can see every file and every question. Matches
#               the Step 4 (PYQCount) Task 1 pattern (S5-1a) for consistency.
#               §12 Phase 0b DoD updated with 2 new items.
#   v2.0 — 2026-07-05 — PHASE B FINAL DEEP-AUDIT (7 fixes).
#           (1) HIGH — CHILD POINTER RESET (S5-2): count_sorted_file() now
#               resets cur_top + cur_sub when a new Section heading is found,
#               and resets cur_sub when a new Topic heading is found. Matches
#               Step 5 E-1 pseudocode (current_path[:level-1] + [content]).
#               Without this, a question after a Topic heading but before its
#               first Subtopic would silently inherit the wrong subtopic from
#               the previous topic — invisible to all Task gates.
#           (2) HIGH — TASK 1 Q-COUNTING METHOD (S5-1a): now explicitly
#               specifies: use python-docx paragraph iteration with the SAME
#               Q-pattern (r'^Q\.?\s*\d+') as count_sorted_file(). Also
#               documents the PYQSort renumber_stem dependency (sorted files
#               always output Q.<N> format). Also specifies per-file Q-count
#               storage for Task 2 diagnostic.
#           (3) BUG — TASK 2 FLOW REFERENCE (S5-4a): "Proceed to S5-5" fixed
#               to "Proceed to S5-4b (Task 2.5)." Was skipping the taxonomy
#               name cross-check in the documented flow.
#           (4) HIGH — TASK 2.5 EXTRACTION METHOD (S5-4b): now specifies exact
#               rules for extracting (section, topic, subtopic) triples from
#               Analysis doc tables. Section name from doc header (strip
#               "[ExamCode] — " prefix). Topic name from master table cells
#               (strip "Topic N: " prefix via parse_taxonomy_level). Subtopic
#               name from per-topic table cells (raw text .strip()). Ensures
#               extracted names match parse_taxonomy_level() output.
#           (5) MEDIUM — TASK 2 PER-FILE DIAGNOSTIC (S5-4, S5-4a): batch
#               counting now tracks per_file_attributed[filename] = sum of
#               attributed counts. When Task 2 fails, compares against Task 1
#               per-file Q-counts to identify exactly which files have
#               discrepancies and by how many.
#           (6) MEDIUM — PHASE B EXECUTION MODEL (new S5-8): specifies Python
#               script-based execution via count_pipeline.py. Script processes
#               files in batches, writes results to JSON, runs all gates.
#               3-tool-call model: create_file → bash_tool → present_files.
#           (7) LOW — DEDUP REGEX MULTI-DATE FIX (S5-1): multi-date filenames
#               (containing "_to_") are now excluded from dedup — they represent
#               unique combined papers by definition.
#   v1.9 — 2026-07-05 — PHASE B DEEP-AUDIT (6 gap fixes).
#           (1) CRITICAL — TAXONOMY NAME CROSS-CHECK (new S5-4b, TASK 2.5):
#               after Task 2 passes, cross-check every counted (section, topic,
#               subtopic) triple against the Analysis doc taxonomy. Flag phantom
#               triples (counted but not in doc) and orphan subtopics (in doc but
#               not counted). Prevents silent count loss from name mismatches
#               (trailing spaces, dash variants, case differences). HARD STOP
#               if any phantom triples found.
#           (2) HIGH — ORPHAN QUESTION TRACKING (S5-2 updated): count_sorted_file()
#               now tracks orphan questions (Q found before any Subject/Subtopic
#               heading) separately. Returns orphan list with file, Q number, and
#               reason. Task 2 failure message includes orphan diagnostic.
#           (3) MEDIUM — SORTED FILE FILTERING (S5-1 updated): Drive listing now
#               filters for files matching sorted filename pattern (*_Sorted_*.docx).
#               Non-sorted .docx files (Row files, other docs) are skipped with
#               a logged warning. Prevents double-counting.
#           (4) MEDIUM — DUPLICATE SORTED FILE DETECTION (S5-1 updated): same-date
#               same-session dedup applied to sorted files. If two sorted files
#               share the same date+session, keep the larger file, skip the
#               smaller. Log the skip. Prevents inflated counts.
#           (5) MEDIUM — PHASE B SESSION MANAGEMENT (new S5-7): explicit session
#               protocol for large corpora. Resume via re-trigger with same Drive
#               link. count_progress.json tracks processed files for skip-on-resume.
#               Task 1 re-runs on resume (re-confirms full inventory).
#           (6) LOW-MEDIUM — ZERO-COUNT SUBTOPICS (S5-5 updated): explicit rule
#               that 0 is a valid count written as "0". No subtopic may remain
#               "—" after Phase B. Subtopics with 0 PYQs get "0" not "—".
#           New edge cases: EC-P27 (phantom triple), EC-P28 (orphan Q in sorted
#           file), EC-P29 (non-sorted file in Drive folder), EC-P30 (duplicate
#           sorted file).
#           §12 Phase B DoD updated: 6 new items.
#   v1.8 — 2026-07-05 — PHASE B QUALITY GATES + BATCH SIZE (4 tasks, 5 changes).
#           (1) TASK 1 — PRE-COUNT CONFIRMATION GATE (new S5-1a): after reading
#               all sorted PYQ files from Drive, display year-wise paper inventory
#               with per-paper Q counts before any subtopic counting begins. Wait
#               for explicit user confirmation. Proves all files and all questions
#               are visible.
#           (2) TASK 2 — POST-COUNT ACCURACY GATE (new S5-4a): after all batch
#               counting is complete, display full Subject > Topic > Subtopic
#               breakdown with counts. Grand total must exactly equal the confirmed
#               total from Task 1. If mismatch (even 1 Q) → re-scan and fix before
#               proceeding. Zero tolerance.
#           (3) TASK 3 — DOC-WRITING ACCURACY GUARANTEE (S5-5 expanded): every
#               number inserted into Analysis docs must be arithmetically verified
#               at 4 levels: subtopic cells, topic TOTAL rows, master summary table,
#               header line. Cross-check: header == GRAND TOTAL == sum(topic totals)
#               == sum(subtopic counts). Any mismatch → fix before delivering.
#           (4) TASK 4 — BATCH SIZE REDUCED: BATCH_SIZE_COUNTS changed from 15 → 5.
#               S5-1 prose updated from "batch 10-15 files" → "batch up to 5 files".
#               §11 batch model updated.
#           (5) §12 Phase B DoD updated: 4 new Task gates added.
#   v1.7 — 2026-07-04 — RUNTIME GAP FIXES (32 issues from live execution).
#           Source: PYQAnalyse_Gap_Analysis_v1.md — live execution against
#           SSC CGL Tier 1 (200 papers, 7 years) exposed 32 gaps in 9 categories.
#           3 CRITICAL, 7 HIGH, 12 MEDIUM, 10 LOW — all fixed.
#
#           CATEGORY A — CONVERGENCE ENFORCEMENT (6 fixes):
#           (A1) CRITICAL: Anti-editorializing rule for JSON — Claude added
#                convergence_recommendation, scan_analysis fields to progress JSON.
#                FIX: BANNED JSON FIELDS list + schema-only enforcement.
#           (A2) CRITICAL: Anti-editorializing rule for chat — Claude argued
#                "taxonomy is functionally stable" alongside FAIL gate statuses.
#                FIX: Mandatory batch-end message template + BANNED PHRASES list.
#           (A3) MEDIUM: Gate 3 counter cited before Gate 2 met. FIX: counter is
#                informational noise before Gate 2 — documented.
#           (A4) HIGH: Strongest language only in code comments. FIX: prose-level
#                MANDATE block added before S3-4 code block.
#           (A5) MEDIUM: No papers-per-session expectation. FIX: 4-5 batches/session
#                target added to new S3-7 session management.
#           (A6) LOW: offer_early_exit name primes exit-thinking. FIX: renamed to
#                report_gate_status.
#
#           CATEGORY B — BATCH PROCESSING (4 fixes):
#           (B1) HIGH: Partial batches (1-2 papers) counted as complete. FIX:
#                BATCH INTEGRITY RULE — partial batch does not increment/reset counter.
#           (B2) MEDIUM: No explicit increment/reset code. FIX: explicit code with
#                "2 empty + 1 discovery = RESET" annotation.
#           (B3) MEDIUM: No response budget guidance. FIX: response budget section
#                with fallback to 2-paper batches.
#           (B4) HIGH: File reading method unspecified — Drive read_file_content
#                strips OMML/images. FIX: Drive reading method spec with OMML/figural
#                fallback classification rules.
#
#           CATEGORY C — CLASSIFICATION QUALITY (5 fixes):
#           (C1) CRITICAL: Per-question classifications not stored — only paper
#                summaries. FIX: per-Q storage mandate + separate classifications
#                file for large corpora.
#           (C2) HIGH: scan_progress.json too large (6000+ records). FIX: split
#                classifications into [ExamCode]_classifications.json.
#           (C3) MEDIUM: No new-discovery validation protocol. FIX: 3-question
#                validation gate before adding new subtopic.
#           (C4) MEDIUM: Figural questions classified blind during scan. FIX:
#                text-clue inference rules + EC-P24.
#           (C5) LOW: No per-section Q-count validation. FIX: post-paper validation
#                with informational warnings.
#
#           CATEGORY D — TAXONOMY & SCHEMA (3 fixes):
#           (D1) MEDIUM: Taxonomy authority chain unclear. FIX: explicit chain
#                documented (taxonomy_draft → scan_progress → PYQApprove).
#           (D2) HIGH: Full taxonomy not stored — only deltas. FIX: scan_progress
#                ['taxonomy'] must be COMPLETE (original + discoveries).
#           (D3) LOW: No schema version enforcement. FIX: version check in
#                load_scan_progress with error message.
#
#           CATEGORY E — REFINEMENT PASS (4 fixes):
#           (E1) HIGH: Refinement data impractical at scale. FIX: per-subtopic
#                sequential execution model with 50-Q sampling.
#           (E2) MEDIUM: Post-refinement gate re-check ambiguous. FIX: EC-P19
#                updated — Gate 2 not re-checked, only Gate 3.
#           (E3) MEDIUM: check_dimensional_splits unimplemented. FIX: structured
#                Counter-based algorithm with concrete example.
#           (E4) LOW: No refinement output verification. FIX: orphan check.
#
#           CATEGORY F — SESSION MANAGEMENT (3 fixes):
#           (F1) HIGH: No session management for large corpora. FIX: new S3-7
#                session management section with protocol and formula.
#           (F2) LOW: Drive listing not cached. FIX: drive_file_inventory in
#                scan_progress.json.
#           (F3) LOW: No Drive rate limit handling. FIX: retry-once + save guidance.
#
#           CATEGORY G — PAPER SELECTION (2 fixes):
#           (G1) MEDIUM: Cherry-picking small files. FIX: date-asc/shift-asc
#                ordering within each year — no reordering by size.
#           (G2) LOW: Newest-year-first bias undocumented. FIX: design note added.
#
#           CATEGORY H — CROSS-STEP CONTRACT (2 fixes):
#           (H1) MEDIUM: PYQApprove required fields unspecified. FIX: explicit
#                field list added to S4-1.
#           (H2) LOW: taxonomy_draft → scan_progress copy not explicit. FIX:
#                source_taxonomy tracking in init + authority chain docs.
#
#           CATEGORY I — MISSING EDGE CASES (3 fixes):
#           (I1-I3) LOW: EC-P21 (mixed file types), EC-P22 (duplicate filenames),
#                EC-P23 (Drive folder structure variants).
#
#           Additional edge cases from other categories:
#           EC-P24 (figural scan misclassification), EC-P25 (OMML-obscured scan),
#           EC-P26 (partial batch on context limit).
#
#           Structural changes:
#           - S3-7 is now Session Management (new). Old S3-7 → S3-8.
#           - report_gate_status replaces report_gate_status.
#           - §11 updated: 26 edge cases.
#           - §12 DoD updated for session management and classification storage.
#   v1.6 — 2026-07-04 — CROSS-STEP SYNC + EXAM-AGNOSTIC FIX (6 bugs).
#           (1) MISSING FOOTER: no "END OF" marker — every other framework file has
#               one. FIXED: added.
#           (2) EXAM-SPECIFIC JSON EXAMPLE (S2-5): exam_config schema used hardcoded
#               SSC CGL Tier 1 values (exam_code, exam_name, 4 SSC section names with
#               specific q_ranges). FIXED: replaced with [ExamCode]/[Section N Name]
#               placeholders matching the exam-agnostic pattern of other framework files.
#           (3) 'TestSeriesRow' STALE NAME (3 refs in header): Step 1 PYQ Prepare was
#               still referenced by its old name. v1.2 fixed TestSeriesSort→PYQSort but
#               missed TestSeriesRow. FIXED: "Step 1 PYQ Prepare" / "Step 1 (PYQ Prepare)".
#           (4) PIPELINE POSITION MISSING STEP NUMBERS: PYQExtract and MockBlueprint
#               listed without canonical step numbers. FIXED: "Step 5 PYQExtract",
#               "Step 6 MockBlueprint", "Step 3 PYQSort".
#           (5) exam_config SCHEMA MISSING 3 FIELDS: session_keyword, page_size,
#               options_count — all consumed by PYQSort (v1.3/v1.4) but not defined in
#               the schema that creates exam_config.json. PYQSort used silent defaults
#               (Shift, A4, 4) which worked but weren't documented as the contract.
#               FIXED: all 3 added to S2-5 schema with field definitions + defaults.
#           (6) PREREQUISITE section hardcoded "Shift" in date label format description.
#               FIXED: uses "<session_keyword>" placeholder (configurable per exam).
#           Cross-step sync verified: PYQSort v1.4 (session_keyword, page_size,
#           options_count consumption), Step 5 (OPT_PATTERNS byte-identical — confirmed
#           in PYQSort audit), Step 6 Blueprint v1.17 (Analysis doc consumption).
#   v1.5 — 2026-07-04 — TAXONOMY-DEPTH OVERHAUL (5 architectural fixes).
#           ROOT CAUSE: v1.0–v1.4 produced shallow taxonomies (119 subtopics for
#           SSC CGL Tier 1 vs 221 required) because of 5 cascading failures:
#           (F1) S2-3 merged syllabus items into mega-Topics (4 English Topics
#                instead of 12) → subtopic space collapsed before scan began.
#           (F2) S2-3 subtopic derivation used FORMAT categories (Word/Number/
#                Letter/Figure) instead of QUESTION PATTERNS — and the rule
#                "when in doubt KEEP AS SINGLE" suppressed Claude's domain
#                knowledge, producing 15 English subtopics instead of 66.
#           (F3) check_convergence() 30% hard gate was not enforced at runtime —
#                Claude treated consecutive_empty as standalone trigger, scanning
#                only 13/198 papers (6.6%) instead of the required 59 (30%).
#           (F4) CONVERGENCE_CONSECUTIVE=3 meant 9 papers without a new subtopic
#                triggered convergence — meaningless when the coarse taxonomy
#                absorbed every question.
#           (F5) scan_paper() had no subtopic refinement — binary "fits / doesn't
#                fit" could never discover patterns WITHIN existing broad subtopics.
#
#           FIX 1 — S2-3 TOPIC MAPPING REWRITE:
#             Each individually-listed syllabus item that represents a distinct
#             question type = one Topic. "Group into mega-Topics" instruction
#             removed. New TOPIC INTEGRITY TEST added (3 questions).
#           FIX 2 — S2-3 SUBTOPIC DERIVATION REWRITE:
#             Default reversed: "When in doubt, SPLIT" (not keep-as-single).
#             6 mandatory pattern dimensions added (Format, Direction, Task,
#             Content/Thematic, Structural, Medium). Claude MUST apply all 6
#             to every Topic. Target = coaching-institute practice-set granularity.
#           FIX 3 — CONVERGENCE HARD GATES:
#             4-gate architecture: Gate 0 (small corpus → scan all), Gate 1
#             (all years covered), Gate 2 (30% papers), Gate 3 (7 consecutive
#             empty batches — raised from 3), Gate 4 (refinement pass done).
#             Language upgraded to non-bypassable absolute enforcement.
#           FIX 4 — SUBTOPIC REFINEMENT PASS (new §3-6):
#             Mandatory pass after gates 1-3. Reviews classified questions per
#             subtopic, applies 6 pattern dimensions, splits broad subtopics.
#             Runs BEFORE convergence can be declared.
#           FIX 5 — RULE 7 PATTERN METADATA:
#             scan_paper() now records question_task, question_format,
#             question_direction, thematic_domain per classification.
#             Enables refinement pass splitting decisions.
#
#           Additional changes:
#           - 4 new edge cases: EC-P17 (subtopic with 0 PYQs after split),
#             EC-P18 (refinement creates duplicate subtopic name across Topics),
#             EC-P19 (scan resume after refinement), EC-P20 (syllabus with
#             pre-grouped items vs individually-listed items).
#           - §11 updated: classification rules 1-7, 20 edge cases.
#           - §12 DoD updated for refinement pass items.
#           - scan_progress.json schema extended with pattern metadata and
#             refinement_pass_done flag.
#           SELF-AUDIT (5 additional fixes after domain-expert simulation):
#           (6) CRITICAL: check_dimensional_splits said "apply FIRST split
#               that works" — blocked multi-dimensional splitting (e.g.,
#               Analogy Dim 5 fires, Dim 6 Figural never applied). FIX:
#               replaced with holistic all-dimensions merge rule.
#           (7) S2-3 Step 2 Derivation Procedure lacked merge instruction
#               for subtopics from multiple dimensions + had zero QA
#               examples. FIX: added step 6 (merge across dimensions) with
#               overlap resolution rule + QA examples (Interest, Mensuration,
#               Trigonometry, Statistics/DI).
#           (8) EC-P2 (1-2 papers) had stale language ("no convergence check
#               needed") that predated Gate 0 architecture. FIX: references
#               Gate 0 + Gate 4 (refinement still applies).
#           (9) BATCH_SIZE comment said "locked" but EC-P15 said "reduce to 2
#               for 500+ subtopics". FIX: BATCH_SIZE comment changed to
#               "default" with flexibility note; EC-P15 aligned.
#           (10) EC-P1 (0 papers) didn't note that Step 2a's 6-dimension
#                derivation produces coaching-depth taxonomy without scanning.
#                FIX: added explicit note.
#           DEEP LINE-BY-LINE AUDIT (5 more fixes):
#           (11) CRITICAL: S2-1 had stale pre-v1.5 language ("Identify natural
#                groupings", "splitting broad items") that contradicted S2-3's
#                Topic Integrity Test. Claude reading S2-1 first would mentally
#                group items into mega-Topics before S2-3 could override.
#                FIX: S2-1 now says "preserve each item as-is" and defers
#                Topic/Subtopic decisions to S2-3.
#           (12) CRITICAL: Gate 3 required consecutive_empty >= 7 even when
#                total_available = 0 (or all papers scanned). With 0 papers,
#                no batches run → consecutive_empty stays 0 → Gate 3 returns
#                'continue' forever. Also scan_progress.json was never saved
#                in the 0-paper path (save only called inside batch loop).
#                FIX: Gate 3 now SKIPS when all_papers_scanned (scanned >=
#                total_available). run_scan "not pending" path now saves
#                progress before returning.
#           (13) CRITICAL: When all papers scanned but Gate 3 not met,
#                refinement pass was SKIPPED — the "else" branch just printed
#                "Run: PYQApprove" without running refinement. FIX: run_scan
#                "not pending" path now ALWAYS runs refinement if not done,
#                then saves progress, then prints proceed message.
#           (14) MEDIUM: S4-4 approval gate message said "correctly grouped"
#                — stale pre-v1.5 language encouraging mega-Topic review.
#                FIX: updated to match v1.5 rules (distinct Topics per
#                syllabus item, coaching-depth subtopics, benchmark count).
#           (15) LOW: S2-6 delivery message didn't include quality gate
#                benchmark result. User couldn't verify depth at delivery.
#                FIX: added benchmark line to delivery message.
#   v1.4 — 2026-07-04 — GAP FIX (1 fix).
#           (1) Step 2b (PYQScan) trigger had no PYQ: <<Drive link>> parameter,
#               even though S3-2 collect_row_files() already accepted drive_folder_id
#               and the header INPUTS section said "from uploads or Google Drive".
#               FIX: added optional PYQ: <<Drive link>> to Step 2b trigger format
#               (header, S1-1 trigger formats, S1-1 parse block, S1-2 file inventory).
#               Step 2b now has parity with Step 4/Step 5 Drive link syntax.
#               Row files via chat upload remain the fallback when PYQ: is absent.
#   v1.3 — 2026-07-03 — FINAL-AUDIT (4 fixes, 1 runtime crash).
#           (1) CRASH: round_robin_by_year() passed None-year keys to sorted(),
#               which raises TypeError in Python 3 (None < int). EC-P8 documents
#               year-extraction failure as valid, but the function didn't handle it.
#               FIX: filter None-year files into a separate tail group appended
#               after all year-keyed rounds, so sorted() never sees None.
#           (2) OPT_PATTERNS drift: PYQAnalyse patterns lacked the (.+) suffix
#               that Step 5's E-3 patterns have. Without (.+), a bare "1. " (no
#               content after label) matched as an option in PYQAnalyse but not in
#               Step 5. FIX: aligned patterns to include (.+), making is_option()
#               behaviour byte-identical to Step 5's.
#           (3) S2-2 exam_config field spec said "q_range_start, q_range_end" (two
#               separate fields), but S2-5 JSON schema, PYQSort code, and Blueprint
#               all use "q_range: [start, end]" (one array field). FIX: S2-2 aligned
#               to the array format that every consumer actually reads.
#           (4) v1.2 changelog entry (8) was a ghost fix — claimed "Pipeline diagram
#               line 15 corrected" but no change was needed or applied (line 16
#               "Steps 7–11" was already correct since MockBlueprint appears
#               separately on line 15). Removed the ghost entry.
#   v1.2 — 2026-07-03 — DEEP-AUDIT-2 (7 fixes, 1 critical runtime bug).
#           (1) CRITICAL: check_convergence() had `all_years = set()` — always
#               empty, so min_year_coverage was ALWAYS False and convergence
#               could NEVER be reached. FIX: accept `all_years` as a parameter
#               from the caller (derived from the full paper queue).
#           (2) Four "Step 1" references corrected to "Step 6" (MockBlueprint).
#               Step 1 = PYQ Prepare; BV-0A, ZP rotation, recency weighting
#               are Step 6 concepts. Lines: header L56, EC-P1 L1032, EC-P14
#               L1103, EC-P16 L1116.
#           (3) EC-P14 title still said "STEP 0" — missed by v1.1 audit. Fixed
#               to "Step 5" (PYQExtract).
#           (4) is_taxonomy_heading() DRIFT from Step 5's version: PYQAnalyse
#               used `re.match(r'^[1-5]\.\s')` for option filtering, but Step 5
#               uses `is_option()` matching 5 patterns (1./A./(1)/(A)/A)). Fixed:
#               aligned to full OPT_PATTERNS for contract compliance.
#           (5) Shift-tag regex aligned: `\d{1,2}` (PYQAnalyse) vs `\d{2}`
#               (Step 5). Standardised both-safe `\d{1,2}` and documented.
#           (6) Two stale "TestSeriesSort" references updated to "PYQSort"
#               (line 445 OMML reference, line 1048 EC-P4 passage reference).
#           (7) Missing function stubs added: save_scan_progress(), scan_paper(),
#               add_to_taxonomy() were called but never defined.
#   v1.1 — 2026-07-03 — DEEP-AUDIT (3 fixes, 0 runtime bugs).
#           (1) 15 "Step 0" references corrected to "Step 5" (PYQExtract). The heading
#               format contract, parser comments, name consistency chain, edge cases,
#               and DoD all referenced "Step 0" — the old internal name for PYQExtract,
#               whose canonical pipeline position is Step 5. No code logic changed.
#           (2) S1-1 trigger parsing said "--draft mode" for PYQDraft; the spec's own
#               mode definitions (header, §2, §3) all use "--taxonomy". FIXED: consistent.
#           (3) counts_by_year tuple-key restoration: load_scan_progress had a comment
#               "Restore tuple keys from string representation" but NO restoration code
#               — the keys stayed as Python repr strings, so Counter lookups with actual
#               tuple keys would miss. Added load_count_progress() with ast.literal_eval
#               restoration. Also: last_updated timestamp was init'd to None but never set
#               during the scan loop — added datetime.now(UTC) before save_scan_progress.
#   v1.0 — Initial release. 4-mode architecture (taxonomy/scan/approve/counts).
#          Smart scan with convergence. Heading format contract with Step 5.
#          16 edge cases documented. Validated against SSC CGL Tier 1 + Tier 2.

---

## §1 — SESSION START

### S1-1 — Trigger parsing

```
Trigger formats:
  Step 2a: PYQDraft [ExamCode]
  Step 2b: PYQScan
  Step 2b: PYQScan PYQ: <<Drive link>>
  Step 2c: PYQApprove
  Step 4:  PYQCount PYQ: <<Drive link>>

Trigger matching is case-insensitive.

Parse:
  PYQDraft → Step 2a (--taxonomy mode)
    ExamCode : alphanumeric + underscore only.
               Invalid chars → flag and ask to correct.
               Saved in exam_config.json for all future steps.
  PYQScan  → Step 2b (--scan mode)
    ExamCode : read from exam_config.json in project knowledge.
               If exam_config not found → "Run PYQDraft [ExamCode] first."
    PYQ:     : Google Drive folder link (REQUIRED — v2.16, standardized with Step 4)
               Extract folder ID: r'drive\.google\.com/drive/folders/([A-Za-z0-9_-]+)'
               If absent → HARD STOP: "PYQScan requires PYQ: <<Google Drive folder
               link>>. Row files must be in Google Drive — the local upload fallback
               was removed (v2.16) to match Step 4 (PYQCount)."
  PYQApprove → Step 2c (--approve mode)
    ExamCode : read from exam_config.json.
  PYQCount → Step 4 (--counts mode)
    ExamCode : read from exam_config.json.
    PYQ:     : Google Drive folder link (required)
               Extract folder ID: r'drive\.google\.com/drive/folders/([A-Za-z0-9_-]+)'

Mode validation:
  PYQDraft   → requires: Exam Syllabus + Exam Pattern in uploads or chat
  PYQScan    → requires: PYQ: Drive link to Row files + taxonomy_draft.json in project
  PYQApprove → requires: scan_progress.json in project or uploads
  PYQCount   → requires: PYQ: Drive link to sorted PYQ folder
```

### S1-2 — File inventory

```
List ALL received files immediately after trigger.

For --taxonomy mode:
  ✓ Exam Syllabus  : image (JPG/PNG), PDF, .docx, or plain text in chat
  ✓ Exam Pattern   : .xlsx (PREFERRED) or image/PDF/.docx/plain text (legacy)
      XLSX detection: file extension is .xlsx AND contains sheets
      named "Overview", "Sections", "Range" → use xlsx parser (S2-2a).
      Any other format → use legacy AI extraction (S2-2b).
  If either missing → ask user to provide.

For --scan mode:
  ✓ Row files (.docx) : from PYQ: Drive link (REQUIRED — v2.16, no local fallback)
  ✓ taxonomy_draft.json : from project knowledge or uploads
  Use Google Drive MCP to list files recursively.
  If PYQ: absent → HARD STOP: "PYQScan requires PYQ: <<Google Drive folder link>>.
  Row files must be in Google Drive — the local upload fallback was removed (v2.16)
  to match Step 4 (PYQCount)."
  If taxonomy_draft.json missing → "Run --taxonomy mode first."

For --approve mode:
  ✓ scan_progress.json : from project knowledge or uploads
  If missing → "Run --scan mode first until convergence or full coverage."

For --counts mode:
  ✓ Drive folder with sorted PYQ files
  ✓ Approved Analysis doc in project knowledge (to update with counts)
  If Analysis doc missing → "Run --approve mode first."
```

---

## §2 — PHASE 0a: TAXONOMY BUILDING FROM SYLLABUS

### S2-1 — Syllabus extraction

```
Claude reads the Exam Syllabus (any format — image, PDF, .docx, or text).
Extract ALL subject/topic items mentioned.

For each subject listed in the syllabus:
  1. Record subject name EXACTLY as syllabus states it
  2. List every individual topic/item mentioned under that subject
  3. Preserve each item as-is — do NOT merge or group items at this stage
     (S2-3's Topic Integrity Test determines final Topic structure)

TERMINOLOGY NOTE — "Subject" vs "Section":
  The SYLLABUS defines Subject names (the top-level taxonomy grouping).
  The EXAM PATTERN defines Section names (the OTS paper structure).
  These are independent — see S2-2a "SECTION ≠ SUBJECT" note.
  The taxonomy uses Subject > Topic > Subtopic throughout.
  In the framework code and JSON, the taxonomy key 'section' historically
  refers to the SUBJECT (from syllabus), not the OTS section (from exam
  pattern). This naming is preserved for backward compatibility with all
  downstream steps (PYQSort, PYQExtract, Blueprint, MockCreate, etc.).

S2-3 determines which items become Topics vs Subtopics using the
Topic Integrity Test and 6 Pattern Dimensions.
```

### S2-2 — Exam Pattern extraction

Two paths: S2-2a (xlsx — preferred) and S2-2b (legacy — fallback).

#### S2-2a — XLSX parser (deterministic, preferred)

```python
import pandas as pd
from openpyxl import load_workbook

def parse_exam_pattern_xlsx(xlsx_path, exam_code):
    """
    Parse the standardized 3-tab Exam Pattern xlsx.
    Returns exam_config dict ready for save_exam_config().
    Raises SystemExit on any validation failure.
    """
    wb = load_workbook(xlsx_path)
    required_sheets = {'Overview', 'Sections', 'Range'}
    if not required_sheets.issubset(set(wb.sheetnames)):
        missing = required_sheets - set(wb.sheetnames)
        raise SystemExit(
            f"HARD STOP: Exam Pattern xlsx missing required tab(s): {missing}. "
            f"Expected 3 tabs: Overview, Sections, Range.")

    # ── TAB 1: Overview (key-value, no header row) ────────────────────
    df_ov = pd.read_excel(xlsx_path, sheet_name='Overview', header=None)
    ov = dict(zip(df_ov[0].str.strip(), df_ov[1]))
    # Required fields
    for field in ['Total Questions', 'Medium', 'Question Type',
                  'Total Marks', 'Duration', 'Level']:
        if field not in ov:
            raise SystemExit(
                f"HARD STOP: Overview tab missing required field: '{field}'.")
    total_questions = int(ov['Total Questions'])
    total_marks     = float(ov['Total Marks'])
    medium          = str(ov['Medium']).strip()
    # question_types: comma-separated string → sorted list
    question_types  = sorted(set(
        t.strip() for t in str(ov['Question Type']).split(',')
    ))
    # duration: "180 Min" → 180 (expected format: "<number> Min")
    # Extracts all digits from the string. If duration is in hours,
    # the xlsx must convert to minutes before saving (e.g., "180 Min" not "3 Hours").
    dur_str = str(ov['Duration']).strip()
    time_minutes = int(''.join(c for c in dur_str if c.isdigit()))
    level = str(ov['Level']).strip()

    # ── TAB 2: Sections (table with header row) ──────────────────────
    df_sec = pd.read_excel(xlsx_path, sheet_name='Sections')
    required_cols = {'Section', 'Total Question', 'Question Starts',
                     'Question Ends', 'Max Attempt'}
    if not required_cols.issubset(set(df_sec.columns)):
        missing = required_cols - set(df_sec.columns)
        raise SystemExit(
            f"HARD STOP: Sections tab missing required column(s): {missing}.")
    sections = []
    for idx, row in df_sec.iterrows():
        sections.append({
            'name':        str(row['Section']).strip(),
            'q_count':     int(row['Total Question']),
            'q_range':     [int(row['Question Starts']),
                            int(row['Question Ends'])],
            'max_attempt': int(row['Max Attempt']),
            'subject_order': idx
        })

    # ── TAB 3: Range (table with header row) ─────────────────────────
    df_rng = pd.read_excel(xlsx_path, sheet_name='Range')
    required_cols_r = {'Question Range', 'Question Type',
                       'Correct Marks', 'Negative Marks'}
    if not required_cols_r.issubset(set(df_rng.columns)):
        missing = required_cols_r - set(df_rng.columns)
        raise SystemExit(
            f"HARD STOP: Range tab missing required column(s): {missing}.")
    marking_scheme = []
    for _, row in df_rng.iterrows():
        parts = str(row['Question Range']).split('-')
        rs, re_ = int(parts[0].strip()), int(parts[1].strip())
        marking_scheme.append({
            'q_range':        [rs, re_],
            'question_type':  str(row['Question Type']).strip(),
            'correct_marks':  float(row['Correct Marks']),
            'negative_marks': float(row['Negative Marks'])
        })

    # ── 10 STRUCTURAL VALIDATIONS ────────────────────────────────────
    issues = []

    # V1: Section sum = Total Questions
    sec_sum = sum(s['q_count'] for s in sections)
    if sec_sum != total_questions:
        issues.append(
            f"V1: Sum of section Total Question ({sec_sum}) ≠ "
            f"Overview Total Questions ({total_questions}).")

    # V2: Q_Ends − Q_Starts + 1 == Total Question per section
    for s in sections:
        computed = s['q_range'][1] - s['q_range'][0] + 1
        if computed != s['q_count']:
            issues.append(
                f"V2: Section '{s['name']}': Q{s['q_range'][0]}-"
                f"Q{s['q_range'][1]} = {computed} Qs but "
                f"Total Question = {s['q_count']}.")

    # V3: Section Q-ranges contiguous and non-overlapping
    prev_end = 0
    for s in sections:
        if s['q_range'][0] != prev_end + 1:
            issues.append(
                f"V3: Section '{s['name']}' starts at Q{s['q_range'][0]} "
                f"but previous section ended at Q{prev_end}. "
                f"Expected Q{prev_end + 1}.")
        prev_end = s['q_range'][1]
    if prev_end != total_questions:
        issues.append(
            f"V3: Last section ends at Q{prev_end}, not Q{total_questions}.")

    # V4: Range tab tiles Q.1 through Total Questions completely
    prev_end_r = 0
    for ms in marking_scheme:
        if ms['q_range'][0] != prev_end_r + 1:
            issues.append(
                f"V4: Range {ms['q_range']} starts at Q{ms['q_range'][0]} "
                f"but previous range ended at Q{prev_end_r}.")
        prev_end_r = ms['q_range'][1]
    if prev_end_r != total_questions:
        issues.append(
            f"V4: Last range ends at Q{prev_end_r}, not Q{total_questions}.")

    # V5: All Negative Marks ≤ 0
    for ms in marking_scheme:
        if ms['negative_marks'] > 0:
            issues.append(
                f"V5: Range {ms['q_range']} has positive Negative Marks "
                f"({ms['negative_marks']}). Must be ≤ 0.")

    # V6: Σ(Max Attempt × correct_marks) == Total Marks
    # Build per-Q marks lookup, then compute per-section attempt marks
    marks_by_q = {}
    for ms in marking_scheme:
        for q in range(ms['q_range'][0], ms['q_range'][1] + 1):
            marks_by_q[q] = ms['correct_marks']
    attempt_marks_total = 0.0
    for s in sections:
        sec_total = sum(
            marks_by_q.get(q, 0)
            for q in range(s['q_range'][0], s['q_range'][1] + 1)
        )
        if s['q_count'] == s['max_attempt']:
            attempt_marks_total += sec_total
        else:
            # Proportional (uniform marks within section assumed for
            # attempt-limited sections; exact when all ranges within
            # section have the same correct_marks)
            attempt_marks_total += sec_total * s['max_attempt'] / s['q_count']
    if abs(attempt_marks_total - total_marks) > 0.01:
        issues.append(
            f"V6: Attempt marks ({attempt_marks_total:.2f}) ≠ "
            f"Total Marks ({total_marks}). Check Max Attempt values.")

    # V7: max_attempt must be > 0 and ≤ q_count for every section
    for s in sections:
        if s['max_attempt'] <= 0:
            issues.append(
                f"V7: Section '{s['name']}' has max_attempt={s['max_attempt']}. "
                f"Must be > 0.")
        if s['max_attempt'] > s['q_count']:
            issues.append(
                f"V7: Section '{s['name']}' has max_attempt={s['max_attempt']} > "
                f"q_count={s['q_count']}. Cannot attempt more than total.")

    # V8: question_types from Overview must match distinct types in Range tab
    range_types = sorted(set(ms['question_type'] for ms in marking_scheme))
    if question_types != range_types:
        issues.append(
            f"V8: Overview Question Type {question_types} does not match "
            f"Range tab types {range_types}. Both must list the same set.")

    # V9: correct_marks must be > 0 for every range
    for ms in marking_scheme:
        if ms['correct_marks'] <= 0:
            issues.append(
                f"V9: Range {ms['q_range']} has correct_marks="
                f"{ms['correct_marks']}. Must be > 0.")

    # V10: total_questions and time_minutes must be > 0
    if total_questions <= 0:
        issues.append(f"V10: total_questions={total_questions}. Must be > 0.")
    if time_minutes <= 0:
        issues.append(f"V10: time_minutes={time_minutes}. Must be > 0.")

    if issues:
        msg = "HARD STOP: Exam Pattern xlsx failed validation:\n"
        for i, issue in enumerate(issues, 1):
            msg += f"  {i}. {issue}\n"
        msg += "Fix the xlsx and re-upload."
        raise SystemExit(msg)

    # ── BUILD EXAM_CONFIG ─────────────────────────────────────────────
    exam_config = {
        'exam_code':       exam_code,
        'exam_name':       '',    # filled by Claude from pattern/syllabus context
        'total_questions':  total_questions,
        'total_marks':      total_marks,
        'time_minutes':     time_minutes,
        'medium':           medium,
        'question_types':   question_types,
        'level':            level,
        'marker_mode':      False,   # determined from PYQ structure, not xlsx
        'session_keyword':  'Shift', # default; user may override
        'page_size':        'A4',
        'options_count':    4,       # auto-detected from PYQ at Step 5
        'sections':         sections,
        'marking_scheme':   marking_scheme
    }
    return exam_config
```

```
SECTION ≠ SUBJECT — CRITICAL ARCHITECTURAL NOTE:

  Section names from the Sections tab (e.g., "Part A", "Part B", "Part C" for
  CSIR NET; "General Aptitude", "Biotechnology" for GATE) are ONLINE TEST SERIES
  (OTS) display labels. They define how the test platform presents and organizes
  sections to the student during the exam.

  Section names are NOT Subject names for the taxonomy. The syllabus (provided
  separately in S2-1) defines Subjects, Topics, and Subtopics.

  A single Subject from the syllabus can have questions spanning MULTIPLE sections.
  Example: CSIR NET Life Science — "Cell Biology" questions appear in both Part B
  (Q.21-70, 2 marks) and Part C (Q.71-145, 4 marks).

  Conversely, for exams like SSC CGL, section names happen to align closely with
  subject areas, but the framework still derives subjects from the syllabus — never
  from section names.

  The framework uses section names ONLY for:
    1. Q-range boundaries (which question numbers belong to which section)
    2. Marking scheme linkage (which scoring rules apply to which questions)
    3. Max attempt enforcement (OTS platform concern, not paper generation)
    4. OTS display labels (passed through to the platform as metadata)
```

#### S2-2b — Legacy extraction (AI-interpreted, fallback)

```
Used when exam pattern is provided as image, PDF, .docx, or plain text
(not the standardized xlsx). Claude reads the document and extracts:

  exam_code           : from trigger
  sections            : list of {name, q_count, q_range: [start, end],
                         max_attempt (= q_count if not stated)}
  total_questions     : sum of all section q_counts
  total_marks         : from pattern
  time_minutes        : from pattern
  medium              : from pattern (default: "English")
  question_types      : from pattern (default: ["MCQ"])
  level               : from pattern (default: "Graduation")
  marking_scheme      : inferred from pattern — if a single marks value is stated
                         (e.g., "each question carries 2 marks"), produce one entry
                         covering Q.1 through total_questions. If per-section marks
                         are stated, produce one entry per section. If unclear,
                         ask user.
  marker_mode         : true if exam uses section separators in paper,
                        false if sections determined by Q-number range.
                        If unclear → ask user.

  After extraction, run the same 10 validations (V1-V10) as the xlsx path.
  Any failure → flag to user with specific issue and ask to correct.

  The legacy path produces the SAME exam_config schema as the xlsx path.
  All downstream steps consume exam_config.json identically regardless
  of which input path was used.
```

### S2-3 — Draft taxonomy generation

```
═══════════════════════════════════════════════════════════════════════
TAXONOMY CORE PRINCIPLE — THE UNIQUE DOMAIN PROPERTY:

  Every subtopic must UNIQUELY CLAIM a set of concepts that no other
  subtopic also claims. Given any PYQ question from this exam, EXACTLY
  ONE subtopic must be the unambiguous best match.

  When this holds  → classification is unambiguous → 100% question mapping.
  When this breaks → classification is ambiguous → questions vanish.

  DEFAULT BIAS: MERGE over SPLIT. An over-merged taxonomy loses some
  granularity but classifies 100% of questions. An over-split taxonomy
  creates near-duplicate bins that confuse the classifier and cause
  questions to disappear from the output entirely.

  CRITICAL SCOPE OF MERGE BIAS:
    The merge-over-split bias applies ONLY to AI-INVENTED subtopics —
    splits that Claude proposes from domain knowledge beyond what the
    syllabus explicitly states. It does NOT apply to items the syllabus
    itself explicitly enumerates. If the syllabus lists "Triangles,
    Circles, Polygons" under Geometry, those are syllabus-given items
    and MUST become subtopics regardless of the merge bias. Suppressing
    syllabus-enumerated items is data loss, not conservative merging.

  EVIDENCE: MPPSC Botany — 81 syllabus entries faithfully used as
  subtopics → 150/150 Qs mapped (100%). Same exam with 336 AI-generated
  micro-subtopics → 93/150 Qs mapped (62%). The 4.1× inflation created
  75 near-duplicate subtopic pairs that broke classification.

  COUNTER-EVIDENCE: SSC CGL Tier 1 — framework produced 68 subtopics
  from a syllabus that explicitly lists ~100 items. The 1:1 Topic=Subtopic
  mapping (e.g., "Geometry" → 1 subtopic "Geometry" despite syllabus
  listing Triangles + Circles + Polygons) lost syllabus-given items.
  The merge bias must never suppress what the syllabus explicitly names.
═══════════════════════════════════════════════════════════════════════

For each subject in the syllabus:

  ─── STEP 1: TOPIC DERIVATION (unchanged from v1.5) ───

  Each INDIVIDUALLY LISTED syllabus item that represents a DISTINCT
  QUESTION TYPE = one Topic.

  DO NOT merge syllabus items into super-categories like "Vocabulary",
  "Grammar", "Non-Verbal Reasoning". Those are SUBJECT-level or
  SECTION-level labels, NOT Topic-level labels.

  TOPIC INTEGRITY TEST — apply these 3 questions to every proposed Topic:
    Q1. Would a coaching institute teach this as a SEPARATE chapter?
    Q2. Would a student study for this INDEPENDENTLY of other Topics?
    Q3. Does the exam present this as a DISTINCT question type with its
        own recognisable format?
    If ANY answer is YES for a syllabus item → it is its OWN Topic.

  MERGE ONLY when two syllabus items are genuinely synonymous — i.e., they
  describe the SAME question type with different words.

  GROUPING is allowed ONLY for syllabus items that are sub-operations of
  a single concept where the exam never tests them independently:
    Example: "Percentage, Ratio, Average, Interest, P&L, Discount,
             Partnership, Mixture, SDT, Time & Work, Pipes & Cisterns"
             → Topic "Arithmetic" with each item as a subtopic.
    Example: "Triangle centres, Congruence, Similarity, Circles,
             Quadrilaterals" → Topic "Geometry" with each item as a subtopic.
    Counter-example: "Spot the Error" and "Sentence Improvement" must be
             SEPARATE Topics — distinct question types.

  ═══════════════════════════════════════════════════════════════════
  GROUPED ITEMS ARE SUBTOPICS (MANDATORY):

    When multiple syllabus items are GROUPED into one Topic, EVERY
    grouped item MUST become a named Subtopic under that Topic. The
    Topic name is the umbrella label; the individual items are the
    subtopics. A grouped Topic with only 1 subtopic (same name as
    the Topic) is ALWAYS WRONG — it means the grouped items were lost.

    EXAMPLE — Geometry:
      Syllabus says: "Triangle and its various kinds of centres,
      Congruence and similarity of triangles, Circle and its chords,
      tangents, Regular Polygons"
      ✗ WRONG: Topic "Geometry" → 1 subtopic "Geometry"
      ✓ RIGHT: Topic "Geometry" → subtopics:
          "Triangles — Centres, Congruence, Similarity"
          "Circles — Chords, Tangents, Common Tangents"
          "Regular Polygons"

    EXAMPLE — Trigonometry:
      Syllabus says: "Trigonometric ratio, Degree and Radian Measures,
      Standard Identities, Complementary angles, Heights and Distances"
      ✗ WRONG: Topic "Trigonometry" → 1 subtopic "Trigonometry"
      ✓ RIGHT: Topic "Trigonometry" → subtopics:
          "Trigonometric Ratios & Standard Identities"
          "Heights & Distances"
      (Heights & Distances is a different question type — applied word
      problems vs algebraic simplification. Different solving approach,
      separate textbook chapter, unambiguous classification.)

    EXAMPLE — Polity (GK):
      Syllabus says: "Constitution, Parliament, Judiciary, Executive,
      Fundamental Rights, Elections, etc."
      ✗ WRONG: Topic "Polity" → 1 subtopic "Indian Polity & Governance"
      ✓ RIGHT: Topic "Polity" → subtopics per distinct area

    SELF-CHECK — 1:1 TOPIC=SUBTOPIC DETECTOR:
      After completing subtopic derivation, scan for any Topic where:
        (a) the Topic has exactly 1 subtopic, AND
        (b) the subtopic name is identical or near-identical to the Topic name
      For each match: check if the syllabus listed multiple items under
      that heading. If YES → the items were silently dropped. Re-derive.
      A 1:1 mapping is valid ONLY when the syllabus genuinely lists that
      item as a single atomic concept with no sub-items (e.g., "Venn
      Diagrams" — one concept, one subtopic, no sub-items in syllabus).
  ═══════════════════════════════════════════════════════════════════

  PROOF OF CORRECT TOPIC COUNT (self-check):
    After Topic derivation, count the Topics per section.
    If a section has ≤ 4 Topics but the syllabus listed 10+ items → Topics
    are over-aggregated. Re-derive. The syllabus items ARE the Topics.

  ═══════════════════════════════════════════════════════════════════
  CATCH-ALL / RESIDUAL TOPIC PROHIBITION (MANDATORY):

    Claude MUST NEVER create a Topic or Subtopic named "Other",
    "Other Sub-topics", "Others", "Miscellaneous", "General",
    "Additional Topics", "Remaining Topics", or ANY label that serves
    as a catch-all / residual bin for items that "didn't fit elsewhere".

    EVERY syllabus item that passes the Topic Integrity Test (Q1/Q2/Q3
    = ANY YES) MUST become its own Topic. Items must NOT be grouped
    into a residual bucket.

    FAILURE EXAMPLE (SSC CGL Tier 2 Reasoning):
      ✗ "Topic 17: Other Sub-topics" containing Blood Relations,
        Seating Arrangement, Syllogism, Dice and Cubes, Ranking and
        Ordering, Logical Sequence.
      Each of these is a distinct question type taught as a separate
      chapter by every coaching institute. They MUST be separate Topics:
        ✓ Topic 17: Blood Relations
        ✓ Topic 18: Logical Sequence
        ✓ Topic 19: Seating Arrangement
        ✓ Topic 20: Dice and Cubes
        ✓ Topic 21: Ranking and Ordering
        ✓ Topic 22: Syllogism

    ROOT CAUSE: Claude runs out of patience while processing a long
    syllabus and dumps remaining items into a residual bin. The
    prohibition is unconditional — if a Topic name matches ANY of the
    banned patterns, it is a spec violation and must be re-derived.

    BANNED PATTERNS (case-insensitive, substring match):
      "other", "miscellaneous", "misc", "remaining", "additional",
      "general topics", "catch-all", "residual"

    SELF-CHECK: after completing Topic derivation for a section,
    scan all Topic names against the banned patterns. If ANY match
    → HARD STOP. Re-derive those items as individual Topics.
  ═══════════════════════════════════════════════════════════════════

  ═══════════════════════════════════════════════════════════════════
  NAME-SHAPE VALIDATION (v2.12 — D6-1/D6-2: reject question-strings; canonicalise)

    D6-1 — A raw PYQ QUESTION captured as a subtopic (an extraction defect) must
    NEVER enter the taxonomy. In the SSC CGL run a manifest contained a subtopic
    literally named "What is the average number of pages printed by printer Z during
    the 3 days?" — it was PYQ-based, so Step 6 ALLOCATED it and Step 7 was asked to
    "generate questions for" a question. This gate stops that at the source.

    HARD STOP if any Topic/Subtopic name is QUESTION-SHAPED: ends with '?', is
    > 80 chars, or begins with an interrogative (what / which / how many / …).
    WARN (review, not block) on softer signals (stem phrasing, > 12 words). The gate
    is HIGH-PRECISION — real syllabus labels ("Time, Speed and Distance", "Direct and
    Indirect Speech", "Assertion and Reason") never trip it (verified against 31 real
    labels + 4 question-strings, 0 false positives).

    D6-2 — CANONICALISE names before COMPARING / COUNTING with canon_name(): NFC
    (Unicode), dash variants (– — ‐ − → -), doubled / non-breaking whitespace, and
    case are folded, so trivial drift never splits one subtopic into a phantom pair.
    Display keeps the ORIGINAL name; only comparison/counting uses canon_name().
    This complements the Task 2.5 phantom-triple check (which DETECTS drift) by
    PREVENTING it at the point counts are aggregated.

```python
# Steps 1-3 name-quality gates (v-bump). Pure, deterministic, high-precision.
import re, unicodedata

def canon_name(s):
    """D6-2/D5-6: canonical form for COMPARING/COUNTING subtopic names so trivial drift
    (NFC/NFD, dash variants, doubled/〈nbsp〉whitespace, trailing spaces, case) never splits
    one subtopic into a phantom pair. NOT for display — display keeps the original."""
    s = unicodedata.normalize('NFC', s or '')
    s = s.replace(' ', ' ')                       # nbsp -> space
    for d in ('‐','‑','‒','–','—','−'):  # hyphen/dash variants
        s = s.replace(d, '-')
    s = re.sub(r'\s+', ' ', s).strip()
    return s.casefold()

_INTERROGATIVE = re.compile(
    r'^\s*(what|which|who|whom|whose|when|where|why|how\s+many|how\s+much|how\s+long|how\b)\b',
    re.I)
# stem phrases that only appear inside a question, never in a taxonomy label
_STEM_PHRASE = re.compile(
    r'\b(the average (number|value|of)|the value of x\b|is equal to\b|how many|of the following (is|are)\b'
    r'|printed by|find the value)\b', re.I)

def question_shape_verdict(name):
    """D6-1: is this 'subtopic' actually a raw question string? Returns (verdict, reason).
    verdict ∈ {'OK','HARD','WARN'}. HIGH-PRECISION: HARD only on signals a real syllabus
    label never has, so legitimate names are never blocked."""
    n = (name or '').strip()
    if not n:
        return ('HARD', 'empty name')
    if n.endswith('?'):
        return ('HARD', "ends with '?' — a question stem, not a label")
    if len(n) > 80:
        return ('HARD', f'{len(n)} chars — far longer than any taxonomy label')
    if _INTERROGATIVE.match(n):
        return ('HARD', 'begins with an interrogative — a question stem')
    if _STEM_PHRASE.search(n) and len(n.split()) >= 6:
        return ('WARN', 'contains question-stem phrasing; review that this is a label')
    if len(n.split()) > 12:
        return ('WARN', f'{len(n.split())} words — unusually long for a label; review')
    return ('OK', '')
```

    SELF-CHECK (runs after subtopic derivation, before S-QV / DoD):
      for name in all Topic names + all Subtopic names:
          verdict, reason = question_shape_verdict(name)
          if verdict == 'HARD':
              HARD STOP: f"Name-shape violation: '{name[:60]}' — {reason}. "
                         f"Re-extract this item as a proper taxonomy label, not a question."
          elif verdict == 'WARN':
              review_list.append((name, reason))     # surfaced at S-QV, non-blocking
      # counting/comparison of subtopic triples uses canon_name() on each of
      # (section, topic, subtopic) so NFC/dash/whitespace/case drift cannot phantom-split.
  ═══════════════════════════════════════════════════════════════════

  ─── STEP 2: SUBTOPIC DERIVATION (PER-ENTRY DECISION TREE) ───

  ═══════════════════════════════════════════════════════════════════
  EXCLUSION RULES — apply BEFORE the decision tree:

    ✗ VOCABULARY / GLOSSARY LISTS: Individual terms, named reactions,
      specific organisms, historical terms, concept glossaries
      (e.g., UGC NET History's 80+ terms like "Iqta, Jaziya, Mansab")
      → these define content SCOPE, not taxonomy structure.
      They are CONTENT WITHIN a subtopic, not subtopics themselves.

    ✗ ENUMERATED SCOPE ITEMS within a colon-descriptor:
      (e.g., "mitochondria, lysosomes, peroxisomes" within
      "Structural organization of intracellular organelles:")
      → these are scope markers listing what CAN be tested,
      not separate subtopics. All items share the same question
      type (factual recall of organelle biology).

    ✗ FORMAT QUALIFIERS (TEXT/FIGURAL/PASSAGE/DI):
      → tracked separately in the Format column. NOT taxonomy.

    ✗ CATCH-ALL / RESIDUAL SUBTOPICS:
      → Same prohibition as Topics (see above). Claude MUST NEVER create
      a Subtopic named "Other", "Others", "Miscellaneous", "General",
      or any residual bin. Every distinct concept = its own named Subtopic.
  ═══════════════════════════════════════════════════════════════════

  For each syllabus entry within a Topic, apply this decision tree:

  ┌─────────────────────────────────────────────────────────────┐
  │ Q1: Does this entry have an EXPLICIT IDENTIFIER?            │
  │     (Letter: A/B/C, Number: 1/2/3, bullet with titled      │
  │      header followed by colon + descriptor, or textbook     │
  │      chapter number)                                        │
  │                                                             │
  │   YES → This entry IS a subtopic candidate. Go to Q2.      │
  │                                                             │
  │   NO  → This is an UNDIVIDED BLOCK (paragraph without       │
  │          internal structure, e.g., GATE CS "Section 5:       │
  │          Algorithms" or IIT JAM "Section 2: Mechanics").    │
  │          → Apply DOMAIN KNOWLEDGE to identify 2–5 natural   │
  │            sub-domains within it (e.g., "Theory of           │
  │            Computation" → Regular Languages & FA, CFG & PDA, │
  │            Turing Machines & Undecidability).                │
  │          → Each proposed sub-domain MUST pass Q3.           │
  │          → If no natural sub-domains exist → the entire     │
  │            block = ONE subtopic.                             │
  │          → The 6 PATTERN DIMENSIONS (Format, Direction,     │
  │            Task, Content, Structural, Medium — see Appendix)│
  │            MAY be used as a tool for identifying sub-domains│
  │            in undivided blocks. They are NOT mandatory for  │
  │            entries that already have explicit identifiers.   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │ Q2: Does this entry contain INTERNAL SUB-STRUCTURE?         │
  │                                                             │
  │     Internal sub-structure means ANY of:                    │
  │     • Internal headers with colons (e.g., "Wave optics:     │
  │       wavefront and Huygens' principle" within a larger     │
  │       "Optics" unit)                                        │
  │     • Paragraph breaks with new titled sections             │
  │     • Nested bullets listing distinct domains               │
  │     • An UMBRELLA LABEL covering 2+ genuinely different     │
  │       academic sub-fields (e.g., "Algebra" covering both    │
  │       Abstract Algebra AND Linear Algebra — different       │
  │       university courses taught in different semesters)     │
  │                                                             │
  │   NO  → This entry = ONE subtopic. Use VERBATIM syllabus   │
  │          text (title portion before the colon). DONE.       │
  │          Example: "7K. Recombination: Homologous and        │
  │          non-homologous recombination including              │
  │          transposition" → subtopic "Recombination"          │
  │                                                             │
  │   YES → Each internal sub-section = potential subtopic.     │
  │          Go to Q3 for each proposed split.                  │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │ Q3: UNIQUE DOMAIN CHECK (for each proposed split):          │
  │                                                             │
  │   ALL THREE must be TRUE to justify the split:              │
  │                                                             │
  │   (a) DIFFERENT SOLVING APPROACH:                           │
  │       Would a student use a fundamentally different         │
  │       method/strategy for this vs the other split?          │
  │       "Group Theory" vs "Linear Algebra" → YES (different   │
  │        math). "Lysosomes" vs "Peroxisomes" → NO (same      │
  │        memorization approach for both).                     │
  │                                                             │
  │   (b) SEPARATE STUDY UNIT:                                  │
  │       Would a coaching institute or textbook teach this     │
  │       as a SEPARATE chapter or practice set?                │
  │       "Regular Languages" vs "Turing Machines" → YES.       │
  │       "Nitrate Assimilation" vs "Ammonium Assimilation" → NO│
  │       (same chapter: Nitrogen Metabolism).                  │
  │                                                             │
  │   (c) UNAMBIGUOUS CLASSIFICATION:                           │
  │       Given any question about concept X, could it ONLY     │
  │       belong to THIS split and not the other?               │
  │       If a question could plausibly go either way → the     │
  │       split creates classification ambiguity → DON'T SPLIT. │
  │       "BFS on adjacency list" → could be "Graph Algorithms" │
  │       OR "Graph Data Structures" → ambiguous → DON'T create │
  │       both as separate subtopics.                           │
  │                                                             │
  │   ALL THREE TRUE → Create the split.                        │
  │   ANY FALSE      → Keep the entry as ONE subtopic.          │
  └─────────────────────────────────────────────────────────────┘

  WORKED EXAMPLES ACROSS EXAM TYPES:

    SSC CGL T1 Reasoning: "Semantic Analogy, Figural Classification,
    Coding & Decoding, Venn Diagrams, Number Series..."
    → Each comma-separated label is a short label with implicit
      identifier. Q1=YES. Q2: each is already atomic (no internal
      sub-structure). → Each label = one subtopic. No splitting needed.
    → For Topics like "Analogy" grouped from multiple labels:
      "Semantic Analogy" + "Number Analogy" + "Figural Analogy"
      each becomes a subtopic under Topic "Analogy".

    MPPSC Botany: "2B. Structural organization of intracellular
    organelles: Cell wall, nucleus, mitochondria, Golgi bodies,
    lysosomes, ER, peroxisomes, plastids, vacuoles, chloroplast..."
    → Q1=YES (letter ID "2B"). Q2: the enumerated items (mitochondria,
      lysosomes...) are SCOPE MARKERS, not internal sub-structure.
      No internal headers, no paragraph breaks with new titles.
      Q2=NO. → ONE subtopic: "Structural organization of intracellular
      organelles." DONE.

    GATE CS: "Section 6: Theory of Computation — Regular expressions
    and finite automata. Context-free grammars and push-down automata.
    Regular and context-free languages, pumping lemma. Turing machines
    and undecidability."
    → Q1=NO (undivided block, no letter IDs within). Apply domain
      knowledge: 3 natural sub-domains (Regular/FA, CFG/PDA, TM).
      Q3 check for each: (a) Different approaches? YES — DFA
      minimization ≠ PDA stack operations ≠ TM halting proofs.
      (b) Separate textbook chapters? YES. (c) Unambiguous
      classification? YES — "pumping lemma for CFL" can ONLY be
      CFG/PDA. → Split into 3 subtopics. ✓

    CUET PG Math: "Algebra: Groups, subgroups, Abelian groups, cyclic
    groups, permutation groups; Normal subgroups, Lagrange's Theorem;
    Rings, Subrings, Ideal, Prime ideal; Maximal ideals; Fields;
    Vector spaces, Linear dependence, basis, dimension, linear
    transformations, matrix representation, eigenvalues..."
    → Q1=YES (header "Algebra" with colon). Q2: Does it contain
      internal sub-structure? YES — "Algebra" is an UMBRELLA LABEL
      covering Abstract Algebra (Groups/Rings/Fields) AND Linear
      Algebra (vector spaces/eigenvalues) — different university
      courses. Q3: (a) Different approaches? YES. (b) Separate
      chapters? YES. (c) Unambiguous? YES — "find eigenvalues" is
      always Linear Algebra, "prove Lagrange's Theorem" is always
      Abstract Algebra. → Split into 2 subtopics. ✓

    NEET Biology Unit 7: "Genetics and Evolution" with bullets:
    "• Heredity and variation: Mendelian Inheritance..."
    "• Molecular basis of Inheritance: DNA structure, RNA..."
    "• Evolution: Origin of life, Darwin's contribution..."
    → Q1=YES (bullets with titled headers). Q2: each bullet has a
      distinct titled header → YES, internal sub-structure. Q3 for
      each: Mendelian genetics ≠ molecular biology ≠ evolution —
      all three pass. → 3 subtopics under this Topic. ✓

    CTET Math Content: "• Geometry • Numbers • Addition and Subtraction
    • Multiplication • Division • Measurement • Weight • Time..."
    → Q1=YES (bullet labels). Q2: each is a short label (≤3 words)
      = atomic. No internal sub-structure. → Each bullet = one
      subtopic. 12 subtopics total. ✓

    UGC NET History Unit I: "Negotiating the Sources: Archaeological
    sources: Exploration, Excavation..." + "Indus/Harappa Civilization:
    Origin, extent, major sites..." + "Vedic and later Vedic periods..."
    → Q1=YES (named paragraphs with colon-titles within the unit).
      Each named paragraph = one subtopic. The separate "Concepts,
      Ideas and Terms" list (80+ items) → EXCLUDED by vocabulary
      exclusion rule. → ~5 subtopics for Unit I. ✓

  WHEN SYLLABUS ASSIGNS QUESTION COUNTS:
    If the syllabus itself assigns explicit question counts to a
    level (e.g., CTET: "a) Child Development — 15 Questions"),
    that level IS a meaningful taxonomy boundary. Do not split
    below it UNLESS internal items are clearly distinct question
    types (as with CTET Math Content's 12 labels under "15 Qs").

  ─── STEP 3: RECORD TAXONOMY ───

  taxonomy = {
    section_name: {
      topic_name: [subtopic_1, subtopic_2, ...],
      ...
    },
    ...
  }

  QUALITY GATE — RATIO-BASED GUARDRAIL (before saving):
    Count:
      total_subtopics = sum of all subtopics across all sections
      total_syllabus_entries = count of explicitly identified entries
        in the original syllabus (letters, numbers, bullets, named
        paragraphs — NOT individual enumerated scope items)
      ratio = total_subtopics / total_syllabus_entries

    Guardrails:
      ratio ≤ 2.0  → PASS. Proceed normally.
      2.0 < ratio ≤ 3.0 → FLAG. Print warning:
        "Taxonomy inflation ratio = [X]×. Review all splits for
         Unique Domain Property compliance. Proceed only if each
         split passes Q3 (Unique Domain Check)."
      ratio > 3.0  → HARD STOP. Print:
        "Taxonomy inflation ratio = [X]× exceeds 3.0× guardrail.
         Over-fragmentation will cause classification failures.
         Re-derive taxonomy with fewer splits."

    NEAR-DUPLICATE CHECK (mandatory):
      For every pair of subtopics (S_i, S_j) within the same Topic:
        If name similarity > 75% (by SequenceMatcher or equivalent):
          FLAG: "Subtopics '[S_i]' and '[S_j]' have >75% name similarity.
                 Merge or rename to disambiguate."
      Fix ALL flagged pairs before proceeding.

    COVERAGE CHECK (mandatory):
      Every concept explicitly named in the syllabus must map to
      EXACTLY ONE subtopic. No orphaned concepts (mentioned in syllabus
      but not covered by any subtopic). No duplicated concepts (claimed
      by 2+ subtopics).

    CATCH-ALL NAME CHECK (mandatory):
      Scan ALL Topic and Subtopic names against the banned patterns
      from the CATCH-ALL PROHIBITION rule (above). If ANY match →
      HARD STOP. Re-derive those items as individual named Topics/Subtopics.
      This check runs AFTER all other quality gates.

  ─── APPENDIX: 6 PATTERN DIMENSIONS (optional tool) ───

  The 6 pattern dimensions below are an OPTIONAL analytical tool for
  identifying sub-domains within UNDIVIDED BLOCK entries (Q1=NO path).
  They are NOT mandatory for entries with explicit identifiers.

  They remain useful for aptitude/reasoning exams (SSC, CAT, CTET)
  where a single Topic like "Series" genuinely produces distinct
  question types along format/medium dimensions.

  DIMENSION 1 — FORMAT VARIANT:
    Standalone vs In-context. Single-word vs Phrase vs Passage-embedded.
  DIMENSION 2 — DIRECTION VARIANT:
    A→B or B→A (Active→Passive, Direct→Indirect, Encode→Decode).
  DIMENSION 3 — TASK VARIANT:
    Identify error vs Correct vs Select vs Fill vs Find next vs Find wrong.
  DIMENSION 4 — CONTENT/THEMATIC DOMAIN:
    Same format but different knowledge areas tested.
  DIMENSION 5 — STRUCTURAL VARIANT:
    Single-statement vs Multi-statement. 2-pair vs Matrix. Individual vs Set-based.
  DIMENSION 6 — MEDIUM VARIANT:
    Text-based vs Figure/Image-based vs Mixed.

  WHEN USING DIMENSIONS: every proposed subtopic from dimensional
  analysis MUST pass Q3 (Unique Domain Check) before being accepted.
  If Q3(c) fails (ambiguous classification between two proposed
  subtopics) → merge them into one subtopic.
```

### S2-4 — Taxonomy draft output

```python
import json

def save_taxonomy_draft(taxonomy, exam_config, exam_code):
    draft = {
        'exam_code': exam_code,
        'version': 'draft',
        'source': 'syllabus + exam pattern',
        'sections': {},
        'exam_config': exam_config
    }
    for section, topics in taxonomy.items():
        draft['sections'][section] = {}
        for topic, subtopics in topics.items():
            draft['sections'][section][topic] = subtopics

    # Count totals
    total_subtopics = sum(
        len(subs) for topics in taxonomy.values()
        for subs in topics.values()
    )
    draft['total_subtopics'] = total_subtopics

    path = f'/mnt/user-data/outputs/{exam_code}_taxonomy_draft.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(draft, f, indent=2, ensure_ascii=False)
    return path

# Also save exam_config separately (PYQSort needs this)
def save_exam_config(exam_config, exam_code):
    path = f'/mnt/user-data/outputs/{exam_code}_exam_config.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(exam_config, f, indent=2, ensure_ascii=False)
    return path
```

### S2-5 — Exam config schema

```json
{
  "exam_code": "[ExamCode]",
  "exam_name": "[Exam Full Name]",
  "total_questions": 145,
  "total_marks": 200,
  "time_minutes": 180,
  "medium": "English",
  "question_types": ["MCQ"],
  "level": "Post Graduation",
  "marker_mode": false,
  "session_keyword": "Shift",
  "page_size": "A4",
  "options_count": 4,
  "sections": [
    {
      "name": "[Section 1 Name]",
      "q_count": 20,
      "q_range": [1, 20],
      "max_attempt": 15,
      "subject_order": 0
    },
    {
      "name": "[Section 2 Name]",
      "q_count": 50,
      "q_range": [21, 70],
      "max_attempt": 35,
      "subject_order": 1
    },
    {
      "name": "[Section 3 Name]",
      "q_count": 75,
      "q_range": [71, 145],
      "max_attempt": 25,
      "subject_order": 2
    }
  ],
  "marking_scheme": [
    {
      "q_range": [1, 20],
      "question_type": "MCQ",
      "correct_marks": 2,
      "negative_marks": -0.5
    },
    {
      "q_range": [21, 70],
      "question_type": "MCQ",
      "correct_marks": 2,
      "negative_marks": -0.5
    },
    {
      "q_range": [71, 145],
      "question_type": "MCQ",
      "correct_marks": 4,
      "negative_marks": -1.0
    }
  ]
}
```

Field definitions:
  exam_code          : alphanumeric + underscore (from trigger).
  exam_name          : human-readable exam name (from Exam Pattern doc or syllabus).
  total_questions    : sum of all section q_counts.
  total_marks        : maximum marks achievable (accounts for attempt limits).
  time_minutes       : total exam duration in minutes.
  medium             : exam language — "English", "Hindi", "Bilingual", etc.
                       From Overview tab. Step 5 auto-detection validates against this;
                       xlsx value takes priority on conflict.
  question_types     : sorted list of distinct question types across all ranges.
                       e.g., ["MCQ"] or ["MCQ", "MSQ", "NAT"]. Derived from Range tab's
                       Question Type column. Controls which Step 5 extensions activate:
                         ["MCQ"] only → MSQ/NAT dormant.
                         includes "MSQ" → multi_select_allowed = true.
                         includes "NAT" → nat_present = true.
  level              : academic level — "Graduation", "Post Graduation",
                       "Under Graduation", "School". From Overview tab.
                       Step 7 uses for question complexity calibration.
                       Step 9 uses for explanation depth.
  marker_mode        : true if exam uses === separators in PYQ papers, false if
                       sections determined by Q-number range. NOT in xlsx — determined
                       from PYQ structure at scan time; default false.
  session_keyword    : the keyword used in date labels (Shift/Slot/Phase/Paper/Session).
                       NOT in xlsx — read from Exam Pattern context or default "Shift".
                       Step 1 uses this when producing Row files; PYQSort reads it for
                       date parsing.
  page_size          : "A4" (default, Indian standard) or "Letter" (US). PYQSort reads
                       this for output .docx page setup.
  options_count      : default number of options per question (typically 4 or 5).
                       PYQSort reads this for option-count validation. Auto-detected
                       from PYQ at Step 5 (PARAMETER 7).
  sections[]         : per-section structural definitions.
    name             : OTS display label (NOT a Subject name for taxonomy — see S2-2a).
    q_count          : total questions in this section.
    q_range          : [start_inclusive, end_inclusive] Q-number boundaries.
    max_attempt      : max questions student may attempt in this section. The framework
                       generates ALL q_count questions; max_attempt is OTS platform
                       metadata. When max_attempt == q_count, there is no attempt limit.
                       Used ONLY for V6 marks validation:
                       Σ(max_attempt × correct_marks) must equal total_marks.
    subject_order    : 0-based display order.
  marking_scheme[]   : per-range scoring rules. Ordered by q_range start ascending.
    q_range          : [start_inclusive, end_inclusive] — must tile Q.1 through
                       total_questions with no gaps or overlaps (validated by V4).
                       A single section can contain multiple marking_scheme ranges
                       (e.g., GATE Biotechnology: section Q.11-65 has 6 ranges with
                       mixed MCQ/MSQ/NAT and mixed 1-mark/2-mark).
    question_type    : "MCQ", "MSQ", or "NAT" for this range.
    correct_marks    : marks awarded per correct answer. Float (supports 4.75 etc.).
    negative_marks   : penalty per wrong answer. Must be ≤ 0. Float.
                       0 = no negative marking for this range.

  HELPER — get marks/type for a specific question number:
    To find correct_marks for Q.72: scan marking_scheme[] for the entry where
    q_range[0] ≤ 72 ≤ q_range[1] → returns that entry's correct_marks.
    Same for question_type and negative_marks.
    Step 5, 6, 7, 8, 9 use this lookup pattern.

### S2-6 — Delivery and next step

```
TAXONOMY MODE DELIVERY (S10-1 closed set):
  Deliver via present_files: EXACTLY 2 files.
    1. [ExamCode]_taxonomy_draft.json
    2. [ExamCode]_exam_config.json
  No other files. Run S10-2 pre-delivery checklist before present_files.

Deliver taxonomy_draft.json and exam_config.json via present_files.

Print:
  "Phase 0a complete.
   Draft taxonomy: [N] sections, [M] topics, [K] subtopics.
   Syllabus entries: [E]. Ratio: [K/E]× (guardrail: ≤ 3.0×).
   Near-duplicate pairs: [D] (must be 0).

   Exam config:
     Total questions : [total_questions]
     Total marks     : [total_marks]
     Duration        : [time_minutes] min
     Medium          : [medium]
     Question types  : [question_types]
     Level           : [level]
     Sections        : [sections_count] ([section_names])
     Marking ranges  : [marking_scheme_count] range(s)
     Attempt limits  : [Yes/No] ([max_attempt per section if Yes])
     Validations     : V1-V10 PASSED

   NEXT: Upload both files to [ExamCode] project knowledge.
         Then run: PYQScan
         (with Row files uploaded or Drive link provided)"
```

---

## §3 — PHASE 0b: SMART SCAN FOR SUBTOPIC DISCOVERY

### S3-1 — Scan initialisation

```python
import json, os, re
from collections import Counter

BATCH_SIZE = 3  # papers per batch — default, same as Step 5
                # May be reduced to 2 for very large taxonomies (EC-P15: 500+ subtopics)
                # to fit classification context within Claude's context window.
CONVERGENCE_CONSECUTIVE = 7    # raised from 3 (v1.4) — 21 papers, not 9
MIN_COVERAGE_RATIO = 0.30      # 30% of total papers — ABSOLUTE MINIMUM
SMALL_CORPUS_THRESHOLD = 20    # below this: scan ALL papers, no convergence shortcut

def load_taxonomy_draft(exam_code):
    """Load taxonomy draft from project knowledge or uploads."""
    for base in ['/mnt/project/', '/mnt/user-data/uploads/']:
        path = f'{base}{exam_code}_taxonomy_draft.json'
        if os.path.exists(path):
            return json.load(open(path, encoding='utf-8'))
    return None

def load_scan_progress(exam_code):
    """Load scan progress for resume across sessions."""
    for base in ['/mnt/project/', '/mnt/user-data/uploads/']:
        path = f'{base}{exam_code}_scan_progress.json'
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            # v1.7: Schema version enforcement (Issue 20)
            sv = data.get('_meta', {}).get('schema_version')
            if sv != '2.0':
                raise ValueError(
                    f"scan_progress.json schema_version is {sv}, expected 2.0. "
                    f"Re-run PYQScan from scratch."
                )
            return data
    return None

def load_count_progress(exam_code):
    """Load count progress for resume across sessions.
    Restores counts_by_year keys from string repr back to tuples."""
    for base in ['/mnt/project/', '/mnt/user-data/uploads/']:
        path = f'{base}{exam_code}_count_progress.json'
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            # v1.1 FIX: restore tuple keys from JSON string representation.
            # JSON serialises tuple keys as their repr string, e.g.
            # "('Section', 'Topic', 'Subtopic')". Restore to actual tuples
            # so Counter lookups work with (section, topic, subtopic) keys.
            if 'counts_by_year' in data:
                import ast
                restored = {}
                for k, v in data['counts_by_year'].items():
                    try:
                        restored[ast.literal_eval(k)] = v
                    except (ValueError, SyntaxError):
                        restored[k] = v  # keep as-is if not a tuple repr
                data['counts_by_year'] = restored
            return data
    return None

def init_scan_progress(exam_code, taxonomy_draft):
    """Initialize scan_progress.json from taxonomy_draft.json.
    TAXONOMY AUTHORITY CHAIN (v1.7):
      Step 2a creates taxonomy_draft.json → uploaded to project knowledge.
      Step 2b modifies taxonomy IN scan_progress.json (not taxonomy_draft.json).
      Step 2c (PYQApprove) reads taxonomy FROM scan_progress.json.
      taxonomy_draft.json is NEVER modified after Step 2a.
      The authoritative taxonomy after scanning = scan_progress.json['taxonomy'].
    """
    total_subtopics = sum(
        len(subs) for topics in taxonomy_draft['sections'].values()
        for subs in topics.values()
    )
    return {
        '_meta': {
            'exam_code': exam_code,
            'phase': '0b_scan',
            'schema_version': '2.0',
            'source_taxonomy': 'taxonomy_draft.json',
            'source_taxonomy_subtopics': total_subtopics,
            'papers_scanned': 0,
            'total_available': 0,
            'years_covered': [],
            'convergence_status': 'in_progress',
            'consecutive_empty_batches': 0,
            'refinement_pass_done': False,
            'last_updated': None
        },
        'taxonomy': taxonomy_draft['sections'],  # FULL COPY — not delta
        'exam_config': taxonomy_draft['exam_config'],
        'papers_scanned_list': [],
        'discovery_log': [],
        'drive_file_inventory': []
        # v1.7: Per-question classifications stored in SEPARATE FILE
        # [ExamCode]_classifications.json — NOT in this file.
        # See S3-8 CLASSIFICATION STORAGE STRATEGY for details.
    }
```

```
TAXONOMY AUTHORITY CHAIN:
  taxonomy_draft.json (Step 2a) → FULL COPY into scan_progress.json['taxonomy']
  Step 2b modifies ONLY scan_progress.json['taxonomy'] (adds discoveries).
  taxonomy_draft.json is NEVER modified after Step 2a.
  Step 2c (PYQApprove) reads taxonomy FROM scan_progress.json['taxonomy'].
  scan_progress.json['taxonomy'] MUST contain the COMPLETE taxonomy —
  original from taxonomy_draft.json PLUS all scan discoveries. It is NOT
  a delta/additions-only field.

CLASSIFICATION STORAGE STRATEGY (v1.7):
  Per-question classifications are stored in a SEPARATE file:
    [ExamCode]_classifications.json
  NOT in scan_progress.json (which would grow to 6000+ records for large corpora).
  scan_progress.json contains: _meta, taxonomy, discovery_log, papers_scanned_list,
    drive_file_inventory.
  classifications.json contains: { paper_id: [ {q_num, section, topic, subtopic,
    question_task, question_format, question_direction, thematic_domain}, ... ] }
  Classifications file is cumulative — appended per batch, saved alongside
  scan_progress.json.
  Refinement pass reads the classifications file.
```

### S3-2 — Paper collection and round-robin ordering

```
FILE READING METHOD (v1.7):
  For Drive-sourced papers, use Google Drive:read_file_content for text extraction.
  This provides question stems and options but OMML formulas may render as
  placeholders and images will be absent.

  OMML HANDLING DURING SCAN:
    If a question stem is blank or contains only option numbers after
    read_file_content extraction, classify using:
      (a) Q-number position (which section it falls in)
      (b) Option content to infer section:
          - Mathematical expressions / numbers → quantitative / numerical section
          - Verbal / textual content → language / comprehension section
          - Domain-specific terminology → relevant domain section
          Use exam_config.sections to match inferred section type to actual names.
      (c) Surrounding question context
    Log: "OMML-obscured" in question_format field of classification.

  FIGURAL QUESTION HANDLING DURING SCAN:
    If question references a figure but no image is visible in text:
      (a) Classify under the section's figural/spatial subtopic (RULE 6)
      (b) Use stem text clues: "mirror image", "paper folding", "Venn diagram",
          "count triangles", "embedded figure", "dice" → map to known subtopic
    Log: "figure-inferred" in question_format field.

  FULL OMML/IMAGE PARSING IS NOT REQUIRED FOR SCAN.
  Scan classification is LIGHTWEIGHT — 80%+ accuracy is sufficient.
  PYQSort (Phase A) performs FULL parsing with python-docx for final classification.

DRIVE RATE LIMIT HANDLING:
  If Drive read_file_content fails with a rate-limit or timeout:
    Wait 5 seconds and retry once.
    If second attempt fails: save progress, end session, resume later.
    Log the failure in discovery_log for debugging.

DRIVE FILE INVENTORY CACHING (v1.7, updated v2.3):
  On first session: list all files from Drive → store in
  scan_progress.json['drive_file_inventory'] as:
    [{"name": "filename.docx", "id": "driveId", "year": 2025, "size": 50629}, ...]
  On RESUME sessions: RE-LIST from Drive (do NOT rely on cached inventory).
  See S3-7 RESUME PROTOCOL for full details. Files may have been added or
  removed between sessions — cached inventory could be stale.
  The fresh listing replaces drive_file_inventory in scan_progress.json.
```

### S3-3b — FORMAT AUTHORITY RECONCILIATION (v2.14 — register D6-11)

```
The scan (S3-3) is LIGHTWEIGHT (~80% accurate) and, on OMML math / figural questions,
records PROVISIONAL question_format tokens like "OMML-obscured" and "figure-inferred".
PYQSort Phase A does the FULL python-docx parse and is the AUTHORITY. Without reconciling
the two, a provisional/wrong scan format can silently drive the wrong Format column →
wrong CONCEPT_GROUP / SUBTOPIC_CLASS / passage_present / figural_present / di_present
downstream (Steps 5–7), so a math or figural item can be generated in the wrong form.

RULE (D6-11): before the Format column is finalised, reconcile every question's scan
question_format against its authoritative full-parse format with reconcile_format():
  • the authoritative (clean) full-parse format ALWAYS wins when present;
  • a differing scan value is 'corrected' (logged for review), not silently kept;
  • if the authority is absent, a clean scan value is used ('scan-only'); a provisional
    placeholder with no authority is 'unresolved' → defaults to TEXT and is flagged.
Aggregate with reconcile_stats(): if > 20% of questions were corrected/unresolved, the
scan or the parse has a quality problem — surface it at S-QV rather than shipping silently.
```

```python
# D6-11: reconcile the LIGHTWEIGHT scan question_format against the AUTHORITATIVE
# full python-docx parse (PYQSort Phase A). Scan is ~80% accurate on OMML/figural;
# the full parse wins, and disagreements are surfaced (not silently propagated to
# CONCEPT_GROUP / SUBTOPIC_CLASS / format flags downstream). Pure & deterministic.

_CLEAN = {'TEXT','FIGURAL','PASSAGE','DI'}
# map provisional/scan tokens -> a clean format (best-guess for when the authority is absent)
_SCAN_MAP = {
    'figure':'FIGURAL', 'figure-inferred':'FIGURAL', 'figural':'FIGURAL',
    'omml-obscured':'TEXT',            # math with obscured stem — text unless authority says else
    'word_list':'TEXT', 'number_set':'TEXT', 'text':'TEXT',
    'passage':'PASSAGE', 'rc':'PASSAGE',
    'di':'DI', 'data_interpretation':'DI', 'table':'DI',
}
_PLACEHOLDER = {'omml-obscured','figure-inferred','','none', None}

def _norm(f):
    if f is None: return None
    f=str(f).strip()
    return f.upper() if f.upper() in _CLEAN else f.lower()

def reconcile_format(scan_fmt, authoritative_fmt):
    """Return (final_format, status). status ∈
       {'confirmed','corrected','scan-only','unresolved'}.
       - authoritative (clean full-parse) format ALWAYS wins when present.
       - 'corrected' when it overrides a differing scan value → log for review.
       - 'scan-only' when authority absent but scan gave a usable value.
       - 'unresolved' when neither yields a clean format (WARN; default TEXT)."""
    a = _norm(authoritative_fmt)
    s = _norm(scan_fmt)
    scan_clean = s if s in _CLEAN else _SCAN_MAP.get(s)
    if a in _CLEAN:
        return (a, 'confirmed' if scan_clean == a else 'corrected')
    # authority absent / non-clean
    if scan_clean in _CLEAN:
        was_placeholder = (scan_fmt in _PLACEHOLDER) or (s in _PLACEHOLDER)
        return (scan_clean, 'scan-only' if not was_placeholder else 'unresolved')
    return ('TEXT', 'unresolved')

def reconcile_stats(pairs):
    """pairs: list of (scan_fmt, authoritative_fmt). Returns per-status counts +
    a WARN flag if the corrected/unresolved rate is high (scan quality problem)."""
    from collections import Counter
    st = Counter()
    for scan,auth in pairs:
        st[reconcile_format(scan,auth)[1]] += 1
    total = sum(st.values()) or 1
    bad = st['corrected'] + st['unresolved']
    return {'counts': dict(st), 'total': total,
            'corrected_pct': round(100*bad/total, 1),
            'flag': bad/total > 0.20}   # >20% mismatch → scan/parse quality review
```

```python
def collect_row_files(drive_folder_id, cached_inventory=None):
    """
    Collect all Row file paths, grouped by year, from Google Drive.
    v2.16: DRIVE-ONLY — the local /mnt/user-data/uploads/ fallback was REMOVED to
    standardize with Step 4 (PYQCount), which has always required Drive with no
    fallback (see S1-1's PYQCount PYQ: parameter). Row files via chat upload are
    no longer accepted for --scan mode; PYQ: <<Drive link>> is a required trigger
    parameter.
    cached_inventory: from scan_progress.json['drive_file_inventory']
                      Used ONLY on first session if already cached.
                      Resume sessions re-list from Drive (v2.3 — see S3-7).
    Returns: list of {name, path_or_id, source, year} sorted for round-robin.
    """
    # v2.3: On resume, caller passes cached_inventory=None to force re-listing.
    # On first session, caller may pass cached_inventory if available.
    if cached_inventory and len(cached_inventory) > 0:
        return cached_inventory

    if not drive_folder_id:
        raise SystemExit(
            "HARD STOP: PYQScan requires PYQ: <<Google Drive folder link>>. Row "
            "files must be in Google Drive — the local upload fallback was removed "
            "(v2.16) to match Step 4 (PYQCount). Provide the Drive link and retry.")

    files = []
    # Use Google Drive MCP to list files recursively
    # (same pattern as Step 5's S1-2 Drive path)
    # v1.7: Filter .docx only (EC-P21: skip PDFs, images, Google Docs)
    # Only files with mimeType = wordprocessingml.document
    pass  # Drive MCP calls

    # Extract year from filename
    for f in files:
        f['year'] = extract_year_from_filename(f['name'])

    # v1.7: Deduplicate (EC-P22): same date+shift → keep larger file
    files = deduplicate_files(files)

    return files

def extract_year_from_filename(filename):
    """Extract year from Row file filename."""
    m = re.search(r'(\d{4})', filename)
    return int(m.group(1)) if m else None

def deduplicate_files(files):
    """EC-P22: If two files have the same date+shift (ignoring trailing
    ' 1', ' 2' suffixes), keep the LARGER file. Skip the smaller."""
    # Group by normalized name (strip trailing ' N' suffixes)
    groups = {}
    for f in files:
        norm = re.sub(r'\s+\d+\.docx$', '.docx', f['name'])
        groups.setdefault(norm, []).append(f)
    result = []
    for norm, group in groups.items():
        if len(group) == 1:
            result.append(group[0])
        else:
            # Keep largest file (most likely to have images)
            result.append(max(group, key=lambda x: x.get('size', 0)))
    return result

def round_robin_by_year(files):
    """
    Order files round-robin by year to ensure early coverage of all years.
    E.g.: 2025-paper1, 2024-paper1, 2023-paper1, ..., 2025-paper2, ...
    Files with no extractable year (year=None) are appended at the end.

    DESIGN NOTE (v1.7): Round-robin uses newest-year-first ordering. This is
    intentional — if the exam introduced new question types in recent years,
    they are discovered early. Front-loading newest content is
    compatible with the 30% gate because the gate ensures adequate coverage
    of older years too.

    WITHIN EACH YEAR (v1.7): files are ordered by date ascending, then shift
    ascending. Claude MUST NOT reorder by file size. Smaller files may be
    text-only Row files; larger files contain embedded images for figural
    questions. Cherry-picking small files biases toward text-only types.
    """
    by_year = {}
    no_year = []  # EC-P8: files where year extraction failed
    for f in files:
        if f['year'] is None:
            no_year.append(f)
        else:
            by_year.setdefault(f['year'], []).append(f)

    # Sort years descending (newest first within each round)
    sorted_years = sorted(by_year.keys(), reverse=True)

    # v1.7: Within each year, sort by filename (date-asc, shift-asc)
    for year in sorted_years:
        by_year[year].sort(key=lambda x: x['name'])

    # Round-robin: take 1 from each year per round
    ordered = []
    max_per_year = max(len(v) for v in by_year.values()) if by_year else 0
    for round_idx in range(max_per_year):
        for year in sorted_years:
            year_files = by_year[year]
            if round_idx < len(year_files):
                ordered.append(year_files[round_idx])

    # Append no-year files at the end (still scanned, just not year-prioritised)
    ordered.extend(no_year)
    return ordered
```

### S3-2a — PRE-SCAN CONFIRMATION GATE

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before ANY scan classification begins.
═══════════════════════════════════════════════════════════════════════

After collecting and ordering all Row files (S3-2), but BEFORE running
any batch scanning (S3-5):

  1. Read EVERY Row file from the collected list.
     For Drive-sourced files: use Google Drive:read_file_content.
     For uploaded files: use python-docx or text read.
  2. For each file: count total questions using Q_PATTERNS from Step 5's E-2:
       Q_PATTERNS = [
         r'^Q\.\s*(\d+)\s+',        r'^Q(\d+)\.\s+',
         r'^Question\s+(\d+)\s*[:.] ', r'^(\d+)\.\s+(?!\d)',
         r'^\((\d+)\)\s+'
       ]
     Mark each count as:
       ✓ = verified by parsing (file content was readable, Q-patterns matched)
       * = from filename pattern (file unreadable but filename has Q range like Q1-Q150)
  3. Extract year from filename (reuse extract_year_from_filename from S3-2)
  4. Display a YEAR-WISE PAPER INVENTORY table:

     TASK 1 — PRE-SCAN CONFIRMATION

     | Year | Paper File | Q Count |
     |------|-----------|---------|
     | 2025 | [ExamCode]_12-Sep-2025_Shift-1_Q1-Q100.docx | 100 ✓ |
     | 2025 | [ExamCode]_13-Sep-2025_Shift-2_Q1-Q100.docx | 100 * |
     | ...  | ...       | ...     |
     | TOTAL | [N] papers | [T] questions |

     ✓ = verified by parsing, * = from filename pattern (same structure as verified files)

  5. Print summary:
     "Papers found: [N]
      Total questions across all papers: [T]
      Years covered: [year1] ([count1] papers), [year2] ([count2] papers), ...
      Duplicates detected: [D]
      Non-docx files skipped: [S]

      ★ CONFIRMATION REQUIRED ★
      Verify these numbers match your expectation.
      Once confirmed, I will proceed with subtopic-level scanning
      ([BATCH_SIZE] papers per batch).
      If anything looks wrong, tell me and I will re-scan."

  6. WAIT for explicit user confirmation. Do NOT proceed to S3-5 until
     confirmed. The confirmed paper count and total questions become the
     reference for scan progress tracking.

  7. On RESUME sessions (scan_progress.json exists): still display the
     inventory but also show progress:
       "Previously scanned: [M] papers. Remaining: [N-M] papers."
     User re-confirms before scanning resumes.

PURPOSE: proves that Claude can see every Row file and every question
inside each file without fail — BEFORE classification effort begins.
Catches Drive access issues, missing files, corrupt docs, or Q-pattern
parsing failures upfront. Consistent with Step 4's Task 1 (S5-1a).
```

### S3-3 — Scan classification (lightweight, OMML-aware, pattern-tracked)

```
For each paper in the batch:
  1. Read the Row file .docx (or Drive text via read_file_content — see S3-2)
  2. For each question (detected via Q_PATTERNS from Step 5's E-2):
     a. Extract stem text
     b. If OMML formula present and rendered → use rendered text
        If OMML-obscured (blank stem after extraction) → classify by
        Q-position + option content + context (see S3-2 OMML HANDLING)
     c. Determine SECTION:
        - If marker_mode=true: use module separator (=== Subject ===)
        - If marker_mode=false: use Q-number range from exam_config.sections
     d. Classify into (Topic, Subtopic) within that section:
        - Match against current taxonomy
        - Use universal classification rules (§8)
        - If figure-referenced but no image → use text clues for
          figural subtopic (S3-2 FIGURAL HANDLING)
        - If no subtopic fits → record as NEW DISCOVERY candidate
     e. Record PATTERN METADATA (RULE 7 — mandatory for refinement pass):
        - question_task: what the student is asked to DO
          (identify, select, correct, find, calculate, match, arrange,
           select_incorrect, select_correct, fill_blank, rearrange, etc.)
        - question_format: how content is presented
          (standalone_word, standalone_number, in_sentence, in_passage,
           word_list, number_set, figure, figure-inferred, OMML-obscured,
           mixed, table_based, etc.)
        - question_direction: transformation direction if applicable
          (a_to_b, b_to_a, null if not a transformation question)
        - thematic_domain: knowledge area if classifiable
          (e.g., "actions_behaviour", "persons_professionals",
           "subject_verb_agreement", "tense_errors", null if generic)
     f. Store classification in [ExamCode]_classifications.json:
        {q_num, section, topic, subtopic, is_new_discovery,
         question_task, question_format, question_direction, thematic_domain}

  3. NEW DISCOVERY VALIDATION (v1.7 — before adding to taxonomy):
     For each NEW DISCOVERY candidate, Claude MUST answer these 3 questions:
       Q1. Does ANY existing subtopic in this section cover this question type?
           If yes → classify there, NOT a new discovery.
       Q2. Would the existing subtopic's name mislead a student studying for
           this question type? If no → classify there, NOT a new discovery.
       Q3. Would a coaching institute create a SEPARATE practice set for this
           question type vs the closest existing subtopic?
           If no → classify there, NOT a new discovery.
     Only if all 3 answers confirm separation → add as new discovery.

  4. After all questions in paper classified:
     - Apply new discovery validation (step 3 above)
     - Genuinely new subtopics: add to taxonomy under appropriate section/topic
     - Record paper_id in papers_scanned_list

  5. POST-PAPER VALIDATION (v1.7 — informational, does not halt scanning):
     After classifying all questions in a paper:
       a. Count questions per section (using Q-range from exam_config)
       b. If any section has fewer questions than expected: log warning
          "Paper X: Section Y has N questions, expected M"
       c. If total questions ≠ exam_config.total_questions: log warning
       d. Warnings are informational only (EC-P9 handles variable Q counts)
```

### S3-4 — Convergence check (4 HARD GATES)

```
═══════════════════════════════════════════════════════════════════════
MANDATE: MINIMUM PAPER COVERAGE (v1.7 — PROSE-LEVEL, outside code block)
═══════════════════════════════════════════════════════════════════════

For any corpus > 20 papers, Claude MUST scan at least 30% of total
papers before convergence is possible. For a 200-paper corpus this
means MINIMUM 60 papers. This is not a recommendation. It is a hard
numerical floor. Scanning 59 papers and declaring convergence is a
spec violation regardless of discovery rates or empty-batch counts.

ANTI-EDITORIALIZING RULE (v1.7, updated v2.3):
  When ANY gate returns 'continue', Claude's batch-end message MUST contain:
    1. New subtopics count for this batch
    2. Current taxonomy size (total subtopics)
    3. Papers scanned / total, remaining count
    4. Per-section Q distribution for this batch (v2.2)
    5. Classification quality breakdown if any degraded (v2.2)
    6. Gate status (PASS/FAIL per gate)
    7. "Say 'continue' to process next batch."
    8. NOTHING ELSE — no editorial commentary beyond items 1-7.
       After printing items 1-7, the response ENDS (S3-4a Batch Stop Law).
       Claude MUST NOT process the next batch in the same response.
       Claude MUST NOT run the refinement pass in the same response
       (unless this is the final batch — see S3-4a FINAL BATCH EXCEPTION).

  Claude MUST NOT:
    - Describe taxonomy as "stable", "functionally complete", or "converged"
    - Use phrases like "low discovery rate", "diminishing returns",
      "near-zero value", "scanning more papers would yield..."
    - Recommend skipping to refinement/approve before all gates pass
    - Frame any gate as a "structural constraint" or "numerical threshold"
    - Suggest the user trigger PYQApprove early
    - Add any analysis, recommendation, or editorial commentary about
      whether scanning should continue — the GATES decide, not Claude

  This rule applies to BOTH chat output AND JSON content.
  scan_progress.json MUST contain ONLY schema-defined fields. Claude
  MUST NOT add editorial fields (convergence_recommendation, scan_analysis,
  recommendation, justification, assessment, or ANY field arguing for/against
  convergence). The JSON is a progress tracker, not an opinion document.

  consecutive_empty_batches accumulates from Batch 1 onward but is ONLY
  EVALUATED after Gate 2 passes. Claude MUST NOT cite the counter's value
  as evidence of stability before Gate 2 passes. Before Gate 2, the counter
  is informational noise — it has zero bearing on convergence.
```

```python
def check_convergence(progress, total_available, all_years):
    """
    ═══════════════════════════════════════════════════════════════
    CONVERGENCE HARD GATES — NON-NEGOTIABLE, NON-BYPASSABLE.

    Claude CANNOT declare convergence unless ALL 4 gates pass.
    There is NO override. NO shortcut. NO exception. NO early exit.
    There is NO "close enough". There is NO "probably sufficient".
    Treat these gates like physical locks that cannot be picked.

    If ANY gate returns 'continue' or 'refinement_needed':
      - DO NOT print "★ CONVERGENCE REACHED ★"
      - DO NOT offer early exit options
      - DO NOT ask user if they want to stop
      - Return 'continue' status in the batch-end summary, then
        STOP THE RESPONSE and wait for user's "continue" trigger
        (see S3-4a Batch Stop Law). "Without discussion" means
        do not editorialize — it does NOT mean auto-advance.
    ═══════════════════════════════════════════════════════════════

    all_years: set of all distinct years in the full paper pool
               (derived from round_robin_by_year's input).
    """
    meta = progress['_meta']
    scanned = meta['papers_scanned']
    years = meta['years_covered']
    consecutive_empty = meta['consecutive_empty_batches']

    # ── GATE 0: SMALL CORPUS — scan ALL papers, no convergence shortcut ──
    if total_available <= SMALL_CORPUS_THRESHOLD:
        if scanned < total_available:
            return 'continue', (
                f'GATE 0 LOCKED: Small corpus ({total_available} papers). '
                f'ALL papers must be scanned. No convergence shortcut allowed. '
                f'{scanned}/{total_available} done.'
            )
        # If scanned >= total_available in small corpus → skip gates 1-3,
        # but Gate 4 (refinement) still applies.

    # ── GATE 1: YEAR COVERAGE — every available year must appear ──
    if total_available > SMALL_CORPUS_THRESHOLD:
        min_year_coverage = len(all_years) > 0 and set(years) >= all_years
        if not min_year_coverage:
            covered = len(set(years))
            needed = len(all_years)
            return 'continue', (
                f'GATE 1 LOCKED: Year coverage incomplete. '
                f'Have {covered}/{needed} years. '
                f'Convergence is IMPOSSIBLE until ALL {needed} years are covered.'
            )

    # ── GATE 2: PAPER COVERAGE — minimum 30% of total papers ──
    if total_available > SMALL_CORPUS_THRESHOLD:
        min_papers = max(1, int(MIN_COVERAGE_RATIO * total_available))
        if scanned < min_papers:
            return 'continue', (
                f'GATE 2 LOCKED: {scanned}/{min_papers} papers scanned '
                f'({MIN_COVERAGE_RATIO*100:.0f}% minimum = {min_papers}). '
                f'Convergence is IMPOSSIBLE until {min_papers} papers are scanned.'
            )

    # ── GATE 3: CONSECUTIVE EMPTY BATCHES — stability signal ──
    #    Only checked AFTER gates 0-2 have all passed.
    #    SKIP when all papers have been scanned — stability is irrelevant
    #    because there are no more papers to test against.
    all_papers_scanned = (scanned >= total_available)
    if not all_papers_scanned and consecutive_empty < CONVERGENCE_CONSECUTIVE:
        return 'continue', (
            f'Gates 0-2 passed. Gate 3: Stability check — '
            f'{consecutive_empty}/{CONVERGENCE_CONSECUTIVE} consecutive empty batches. '
            f'Need {CONVERGENCE_CONSECUTIVE - consecutive_empty} more.'
        )

    # ── GATE 4: REFINEMENT PASS — mandatory before convergence ──
    #    Only checked AFTER gates 0-3 have all passed.
    if not progress['_meta'].get('refinement_pass_done', False):
        return 'refinement_needed', (
            f'Gates 0-3 passed. Gate 4: MANDATORY refinement pass required. '
            f'Run §3-6 Subtopic Refinement Pass before convergence can be declared.'
        )

    # ── ALL 4 GATES PASSED — convergence is legitimate ──
    return 'converged', (
        f'Taxonomy stable. {scanned}/{total_available} papers scanned. '
        f'All {len(all_years)} years covered. '
        f'Last {CONVERGENCE_CONSECUTIVE * BATCH_SIZE} papers added 0 new subtopics. '
        f'Refinement pass completed.'
    )

def report_gate_status(progress, total_available, all_years):
    status, msg = check_convergence(progress, total_available, all_years)
    if status == 'converged':
        print(f"\n★ CONVERGENCE REACHED ★")
        print(f"  {msg}")
        print(f"\n  Options:")
        print(f"    A) Stop scanning — proceed to --approve (recommended)")
        print(f"    B) Continue scanning remaining papers")
        return 'converged'
    elif status == 'refinement_needed':
        print(f"\n⚙ REFINEMENT PASS REQUIRED ⚙")
        print(f"  {msg}")
        return 'refinement_needed'
    else:
        # Gates not met — print status but DO NOT offer any exit option
        print(f"  Convergence: {msg}")
        return 'continue'

def print_convergence_summary(progress, classifications, exam_code):
    """
    v2.2: Comprehensive summary displayed BEFORE "Run: PYQApprove".
    The user is about to LOCK the taxonomy — they need full visibility.
    """
    meta = progress['_meta']
    taxonomy = progress['taxonomy']

    # ── TAXONOMY SIZE ──
    original_count = meta.get('source_taxonomy_subtopics', '?')
    final_sections = len(taxonomy)
    final_topics = sum(len(topics) for topics in taxonomy.values())
    final_subtopics = sum(
        len(subs) for topics in taxonomy.values() for subs in topics.values()
    )

    # ── DISCOVERY STATS ──
    scan_discoveries = 0
    refinement_new = 0
    refinement_removed = 0
    for entry in progress.get('discovery_log', []):
        if entry.get('batch') == 'refinement_pass':
            refinement_new += entry.get('count', 0)
            refinement_removed += len(entry.get('removed_subtopics', []))
        else:
            scan_discoveries += entry.get('count', 0)

    # ── CLASSIFICATION QUALITY ──
    total_qs = 0
    quality = Counter()  # normal / omml_obscured / figure_inferred
    sec_dist = Counter()
    for paper_id, paper_classifs in classifications.items():
        for c in paper_classifs:
            total_qs += 1
            sec_dist[c['section']] += 1
            fmt = c.get('question_format', '')
            if 'OMML-obscured' in str(fmt):
                quality['omml_obscured'] += 1
            elif 'figure-inferred' in str(fmt):
                quality['figure_inferred'] += 1
            else:
                quality['normal'] += 1

    normal_pct = (quality['normal'] / total_qs * 100) if total_qs else 0
    omml_pct = (quality['omml_obscured'] / total_qs * 100) if total_qs else 0
    fig_pct = (quality['figure_inferred'] / total_qs * 100) if total_qs else 0

    # ── PAPERS PER YEAR ──
    year_counts = Counter()
    for entry in progress.get('discovery_log', []):
        if entry.get('batch') != 'refinement_pass':
            for p in entry.get('papers', []):
                yr = extract_year_from_filename(p)
                if yr:
                    year_counts[yr] += 1

    # ── PRINT SUMMARY ──
    print(f"\n{'═' * 60}")
    print(f"  POST-CONVERGENCE SUMMARY — REVIEW BEFORE LOCKING TAXONOMY")
    print(f"{'═' * 60}")
    print(f"\n  TAXONOMY GROWTH:")
    print(f"    Step 2a original : {original_count} subtopics")
    print(f"    Final            : {final_subtopics} subtopics "
          f"({final_sections} sections, {final_topics} topics)")
    print(f"    Scan discoveries : +{scan_discoveries} new subtopics")
    print(f"    Refinement splits: +{refinement_new} new, "
          f"-{refinement_removed} removed")
    print(f"\n  PAPERS SCANNED: {meta['papers_scanned']}/{meta.get('total_available', '?')}")
    if year_counts:
        yr_str = ', '.join(f"{yr} ({cnt})" for yr, cnt
                           in sorted(year_counts.items(), reverse=True))
        print(f"    Per year: {yr_str}")
    print(f"\n  CLASSIFICATION QUALITY ({total_qs} total questions):")
    print(f"    Normal          : {quality['normal']} ({normal_pct:.1f}%)")
    print(f"    OMML-obscured   : {quality['omml_obscured']} ({omml_pct:.1f}%)")
    print(f"    Figure-inferred : {quality['figure_inferred']} ({fig_pct:.1f}%)")
    if omml_pct > 30:
        print(f"    ⚠ WARNING: {omml_pct:.0f}% OMML-obscured — scan may have "
              f"missed math-heavy patterns. Consider this before locking.")
    print(f"\n  PER-SECTION SNAPSHOT:")
    for sec_name in sorted(taxonomy.keys()):
        topics = taxonomy[sec_name]
        n_topics = len(topics)
        n_subs = sum(len(subs) for subs in topics.values())
        n_qs = sec_dist.get(sec_name, 0)
        print(f"    {sec_name}: {n_topics} topics, {n_subs} subtopics, "
              f"{n_qs} Qs classified")
    print(f"\n{'═' * 60}")
    print(f"  Run: PYQApprove")
    print(f"{'═' * 60}")
```

### S3-4a — BATCH STOP LAW (MANDATORY — same architectural class as convergence gates)

```
═══════════════════════════════════════════════════════════════════════
BATCH STOP LAW — AUTO-ADVANCE BETWEEN BATCHES IS PERMANENTLY BANNED
═══════════════════════════════════════════════════════════════════════

This rule has the same force as convergence gates and anti-editorializing.
It applies to EVERY batch in EVERY mode that processes batches:
  Phase 0b (--scan): scanning batches
  Phase B  (--counts): counting batches (when run interactively, not via script)

LIVE FAILURE (SSC CGL Tier 2, July 2026):
  Claude processed Batch 1 (3 papers, 35 new subtopics discovered) and
  immediately processed Batch 2 (2 papers) in the SAME response without
  waiting for user confirmation. The batch gate was not enforced because
  the spec buried it as item 7 in the Anti-Editorializing Rule (a section
  about banned phrases, not about response flow control). This failure
  will repeat across all 200+ exams unless enforced at mandate level.

THE BATCH STOP CONTRACT:

  After completing ANY scan batch (including the very first):
    STEP 1: Print the batch-end summary (items 1-6 from S3-4)
    STEP 2: Save scan_progress.json + classifications.json
    STEP 3: Call present_files with scan_progress.json + classifications.json
            (user needs a download link for session resume)
    STEP 4: Print: "Say 'continue' to process next batch."
    STEP 5: *** END THE RESPONSE. Write NOTHING more. ***

  The next batch begins ONLY when the user's NEW message is a
  continue trigger.

  ACCEPTED CONTINUE TRIGGERS (case-insensitive, trimmed):
    "continue", "continue.", "go", "next", "proceed", "go ahead",
    "next batch"

  IF the user message IS a continue trigger:
    → Process the next batch.

  IF the user message is NOT a continue trigger (a question,
  correction, or other instruction):
    → Answer the user's message.
    → Do NOT process the next batch.
    → End with: "Say 'continue' to process next batch."

  NOTE ON RESUME SESSIONS:
    Resume sessions (S3-7) use their own gate (re-list Drive files,
    re-run S3-2a pre-scan gate) and are NOT governed by the intra-session
    continue trigger contract. The Batch Stop Law applies to batch
    boundaries within a session, not to the session-start gate.

  APPLIES TO ALL CORPUS SIZES:
    "Scan ALL papers" (small corpus mode, < SMALL_CORPUS_THRESHOLD)
    means every paper WILL be scanned eventually. It does NOT mean
    they are scanned in one response without stopping. Even for a
    5-paper corpus, Claude MUST stop between batches.

  WHY THIS MATTERS:
    Between batches, the user may want to:
    - Review discovered subtopics for accuracy
    - Correct misclassifications before they propagate
    - Upload additional papers to the Drive folder
    - Pause and resume in a new session
    - Ask questions about the scan results so far
    Auto-advance removes all these checkpoints silently.

  FORBIDDEN IN THE SAME RESPONSE AFTER A BATCH SUMMARY:
    - Processing the next batch's papers
    - "I'll now continue with Batch N+1..."
    - "Proceeding to scan the remaining papers..."
    - Running the refinement pass (unless it's the final batch
      AND all papers are scanned — see S3-4a FINAL BATCH below)
    - ANY classification work beyond the current batch

  FINAL BATCH EXCEPTION:
    The LAST batch (all papers scanned, no pending papers) does NOT
    end with a continue prompt. Instead, it auto-runs:
      1. Refinement pass (if not already done)
      2. Post-convergence summary
      3. File delivery (scan_progress.json + classifications.json)
      4. "Run: PYQApprove"
    This matches MockCreate's final-batch exception (B-8).
═══════════════════════════════════════════════════════════════════════
```

### S3-5 — Batch processing loop

```
BATCH INTEGRITY RULE (v1.7):
  A batch counts toward consecutive_empty_batches ONLY if it contains
  exactly BATCH_SIZE papers (or remaining papers if fewer than BATCH_SIZE
  are left in the queue). A partial batch (context limit reached mid-batch)
  does NOT increment or reset the counter.

  If context fills before completing BATCH_SIZE:
    1. Save scan_progress.json and classifications.json with partial results
    2. Print: "Context limit. Download scan_progress.json → upload to
       project knowledge → new chat → Step 2b: PYQScan PYQ: <<link>>"
    3. New session resumes the incomplete batch (not a new batch)

RESPONSE BUDGET (v1.7):
  A single response reads BATCH_SIZE papers via Drive, classifies all
  questions, and saves progress. If context is insufficient for 3 papers:
    - Reduce to 2 papers per batch (EC-P15 allows this)
    - If even 2 papers won't fit: save progress, end session, resume
  Claude should note reduced batch size in the batch summary.

PER-QUESTION CLASSIFICATION STORAGE (v1.7):
  Every classified question MUST be stored with its full metadata in
  [ExamCode]_classifications.json. Storing only paper-level summaries
  (e.g., "5 new subtopics found") is a spec violation. The refinement
  pass REQUIRES per-question data to detect patterns.
```

```python
def run_scan(exam_code, progress, paper_queue, total_available):
    """Main scan loop — processes papers in batches."""

    # v2.3: Write total_available to _meta so saved JSON has correct value.
    # Without this, _meta.total_available stays 0 (the init default) and
    # convergence gates break on resume if they read from _meta.
    progress['_meta']['total_available'] = total_available

    # Derive all_years from the FULL paper queue (not just pending)
    all_years = set(p['year'] for p in paper_queue if p.get('year') is not None)

    done_ids = set(progress.get('papers_scanned_list', []))
    pending = [p for p in paper_queue if p['name'] not in done_ids]

    # v1.7: Load or init classifications file (separate from progress)
    classif_path = f'/mnt/user-data/outputs/{exam_code}_classifications.json'
    if os.path.exists(classif_path):
        with open(classif_path, encoding='utf-8') as f:
            classifications = json.load(f)
    else:
        classifications = {}

    if not pending:
        # All papers scanned (or 0 papers available).
        # Force refinement if not already done
        if not progress['_meta'].get('refinement_pass_done', False):
            run_refinement_pass(progress, classifications, exam_code)
        from datetime import datetime, timezone
        progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
        save_scan_progress(progress, exam_code)
        conv_status = report_gate_status(progress, total_available, all_years)
        print_convergence_summary(progress, classifications, exam_code)
        return

    print(f"Papers: {len(done_ids)} done / {total_available} total. "
          f"Pending: {len(pending)}")

    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch = pending[batch_start : batch_start + BATCH_SIZE]
        batch_num = (len(done_ids) // BATCH_SIZE) + (batch_start // BATCH_SIZE) + 1
        is_complete_batch = (len(batch) == BATCH_SIZE or
                             batch_start + BATCH_SIZE >= len(pending))

        print(f"\n=== Scan Batch {batch_num}: {len(batch)} paper(s) ===")

        new_subtopics_this_batch = []
        for paper_ref in batch:
            # Read and classify (lightweight scan with pattern metadata)
            paper_classifications, new_discoveries = scan_paper(
                paper_ref, progress['taxonomy'], progress['exam_config']
            )
            # v1.7: Store per-Q classifications in separate file
            paper_id = paper_ref['name']
            classifications[paper_id] = paper_classifications

            # Add validated new discoveries to taxonomy
            for disc in new_discoveries:
                add_to_taxonomy(progress['taxonomy'], disc)
                new_subtopics_this_batch.append(disc)

            # Update metadata
            progress['papers_scanned_list'].append(paper_id)
            progress['_meta']['papers_scanned'] += 1
            year = paper_ref.get('year')
            if year and year not in progress['_meta']['years_covered']:
                progress['_meta']['years_covered'].append(year)

        # v1.7: Update convergence tracking — ONLY for complete batches
        # A batch with 2 empty papers + 1 discovery = RESET (not increment)
        if is_complete_batch:
            if len(new_subtopics_this_batch) == 0:
                progress['_meta']['consecutive_empty_batches'] += 1
            else:
                progress['_meta']['consecutive_empty_batches'] = 0  # HARD RESET
        # Partial batches (context limit) do NOT affect the counter

        # Log discovery
        progress['discovery_log'].append({
            'batch': batch_num,
            'papers': [p['name'] for p in batch],
            'complete_batch': is_complete_batch,
            'new_subtopics': [f"{d['section']}/{d['topic']}/{d['subtopic']}"
                              for d in new_subtopics_this_batch],
            'count': len(new_subtopics_this_batch)
        })

        # Save progress + classifications
        from datetime import datetime, timezone
        progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
        save_scan_progress(progress, exam_code)
        save_classifications(classifications, exam_code)

        # Print batch summary
        total_subtopics = sum(
            len(subs) for topics in progress['taxonomy'].values()
            for subs in topics.values()
        )
        scanned = progress['_meta']['papers_scanned']
        remaining = total_available - scanned

        # v1.7: MANDATORY BATCH-END MESSAGE FORMAT
        # Claude MUST print EXACTLY this and NOTHING ELSE after it.
        # v2.2: Added per-section Q-count and classification quality.
        print(f"  New subtopics: {len(new_subtopics_this_batch)}")
        print(f"  Taxonomy: {total_subtopics} subtopics")
        print(f"  Papers: {scanned}/{total_available} ({remaining} remaining)")

        # v2.2: Per-section Q-count from this batch — catches section detection
        # failures early (e.g., all Qs going to 1 section in a 4-section exam).
        sec_counts = Counter()
        quality_counts = Counter()  # normal / OMML-obscured / figure-inferred
        for paper_ref in batch:
            paper_id = paper_ref['name']
            for c in classifications.get(paper_id, []):
                sec_counts[c['section']] += 1
                fmt = c.get('question_format', '')
                if 'OMML-obscured' in str(fmt):
                    quality_counts['omml_obscured'] += 1
                elif 'figure-inferred' in str(fmt):
                    quality_counts['figure_inferred'] += 1
                else:
                    quality_counts['normal'] += 1
        total_batch_qs = sum(sec_counts.values())
        print(f"  Batch Q distribution: {dict(sec_counts)}")
        if quality_counts['omml_obscured'] + quality_counts['figure_inferred'] > 0:
            print(f"  Quality: {quality_counts['normal']} normal, "
                  f"{quality_counts['omml_obscured']} OMML-obscured, "
                  f"{quality_counts['figure_inferred']} figure-inferred")

        # Gate status
        status, msg = check_convergence(progress, total_available, all_years)
        print(f"  Gates: {msg}")

        # Check convergence
        if status == 'refinement_needed':
            run_refinement_pass(progress, classifications, exam_code)
            status, msg = check_convergence(progress, total_available, all_years)
            if status == 'converged':
                save_scan_progress(progress, exam_code)
                print_convergence_summary(progress, classifications, exam_code)
                return
        elif status == 'converged':
            save_scan_progress(progress, exam_code)
            print_convergence_summary(progress, classifications, exam_code)
            return

        # ══ BATCH STOP LAW (S3-4a) — HARD STOP ══════════════
        # After printing batch summary: END THE RESPONSE.
        # *** Write nothing more. Generate nothing more. ***
        # This is the PYQScan equivalent of MockCreate's MANDATE 1 STEP 6.
        # Claude's response ENDS here. The next batch begins ONLY when
        # the user sends a new message with a continue trigger.
        # Auto-advancing to the next batch = S3-4a violation.

        # Deliver via present_files: EXACTLY 2 files (S10-1 --scan closed set).
        #   1. [ExamCode]_scan_progress.json
        #   2. [ExamCode]_classifications.json
        # No other files. The evolved taxonomy is INSIDE scan_progress.json.
        # DO NOT create separate taxonomy files (taxonomy_draft_v2, etc.).
        # Run S10-2 pre-delivery checklist before present_files.
        progress_path = f'/mnt/user-data/outputs/{exam_code}_scan_progress.json'
        classif_path  = f'/mnt/user-data/outputs/{exam_code}_classifications.json'
        present_files([progress_path, classif_path])

        print(f"\n  Say 'continue' to process next batch.")
        return  # EXIT — response ENDS here

def save_scan_progress(progress, exam_code):
    """Save scan progress JSON. Called after each batch.
    v1.7: BANNED JSON FIELDS — Claude MUST NOT add any of these:
      convergence_recommendation, scan_analysis, recommendation,
      justification, assessment, analysis, suggestion, or ANY field
      arguing for/against convergence. Only schema-defined fields."""
    path = f'/mnt/user-data/outputs/{exam_code}_scan_progress.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
    return path

def save_classifications(classifications, exam_code):
    """Save per-question classifications to SEPARATE file (v1.7).
    This file is cumulative — grows with each batch.
    Used by refinement pass and for audit."""
    path = f'/mnt/user-data/outputs/{exam_code}_classifications.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(classifications, f, indent=2, ensure_ascii=False)
    return path

def scan_paper(paper_ref, taxonomy, exam_config):
    """
    Lightweight classification of one Row file against current taxonomy.
    Returns: (classifications, new_discoveries)
      classifications: list of {q_num, section, topic, subtopic,
                                 question_task, question_format,
                                 question_direction, thematic_domain}
      new_discoveries: list of {section, topic, subtopic} for genuinely new subtopics
                       (AFTER passing new discovery validation — S3-3 step 3)
    Claude performs this classification using domain knowledge + universal rules (§8).
    Pattern metadata (RULE 7) is MANDATORY — every classification must include
    the 4 metadata fields. These enable the refinement pass (§3-6).
    """
    pass  # Claude classifies each Q at runtime using §8 rules + RULE 7

def add_to_taxonomy(taxonomy, discovery):
    """
    Add a newly discovered subtopic to the taxonomy dict.
    discovery: {section, topic, subtopic}
    taxonomy[section][topic] is a list of subtopic strings.
    """
    sec = discovery['section']
    top = discovery['topic']
    sub = discovery['subtopic'].strip()  # §7 NAME CONTRACT: always .strip()
    if sec not in taxonomy:
        taxonomy[sec] = {}
    if top not in taxonomy[sec]:
        taxonomy[sec][top] = []
    if sub not in taxonomy[sec][top]:
        taxonomy[sec][top].append(sub)
```

### S3-6 — Subtopic Refinement Pass (MANDATORY before convergence)

```
═══════════════════════════════════════════════════════════════════════
SUBTOPIC REFINEMENT PASS — GATE 4 PREREQUISITE
═══════════════════════════════════════════════════════════════════════

WHEN:
  Triggered automatically when Gates 0-3 all pass (check_convergence
  returns 'refinement_needed'). This pass runs ONCE. After completion,
  it sets refinement_pass_done = True, which unlocks Gate 4.

PURPOSE (v2.4 — revised default bias):
  Two goals, applied in this priority order:

  1. MERGE confused subtopics: If the classifier consistently assigns
     questions to subtopic A with low confidence because subtopic B is
     equally plausible (confidence < 70%), MERGE A and B into one.
     Over-splitting is worse than over-merging (ref: MPPSC Botany proof —
     4.1× inflation caused 38% data loss).

  2. SPLIT genuinely broad subtopics: If a subtopic accumulates ≥15
     classified questions AND contains 2+ genuinely distinct question
     patterns, propose a split — but ONLY if it passes the Q3 Unique
     Domain Check from S2-3 (different solving approach + separate coaching
     chapter + unambiguous classification).

  The refinement pass may use the 6 pattern dimensions from S2-3 Appendix
  as an analytical tool, but every proposed split MUST pass Q3 (Unique
  Domain Check) before being accepted. The default bias is MERGE over SPLIT.

ALGORITHM:
```

```python
def run_refinement_pass(progress, classifications, exam_code):
    """
    Mandatory refinement pass — reviews all classified questions per subtopic,
    detects broad subtopics, and splits them based on observed patterns.

    EXECUTION MODEL (v1.7):
      Processes one (section, topic, subtopic) at a time — NOT the entire
      classification set at once. Context holds one subtopic's data at a time.
      For subtopics with > 50 classified questions: sample 50 random questions
      for dimension analysis (sufficient to detect clusters).
    """
    taxonomy = progress['taxonomy']
    refinement_splits = []

    # 1. Aggregate all classified questions by (section, topic, subtopic)
    subtopic_questions = {}  # key: (sec, top, sub) → list of classification dicts
    for paper_id, paper_classifs in classifications.items():
        for c in paper_classifs:
            key = (c['section'], c['topic'], c['subtopic'])
            subtopic_questions.setdefault(key, []).append(c)

    # 2. For each subtopic with enough data, check for splittable patterns
    MIN_QUESTIONS_FOR_SPLIT = 15  # v2.4: raised from 5. Need substantial evidence before splitting.
    MIN_PATTERN_SIZE = 3          # v2.4: raised from 2. A pattern needs ≥3 Qs to justify a new subtopic.

    for (sec, top, sub), questions in subtopic_questions.items():
        if len(questions) < MIN_QUESTIONS_FOR_SPLIT:
            continue  # not enough data to split reliably

        # 3. Cluster by pattern metadata dimensions
        #    Check each dimension for distinct clusters
        splits_found = check_dimensional_splits(questions, sec, top, sub)

        if splits_found:
            refinement_splits.extend(splits_found)

    # 4. Apply splits to taxonomy
    for split in refinement_splits:
        old_sub = split['old_subtopic']
        sec = split['section']
        top = split['topic']
        new_subs = split['new_subtopics']

        # Remove old subtopic
        if old_sub in taxonomy.get(sec, {}).get(top, []):
            taxonomy[sec][top].remove(old_sub)

        # Add new subtopics
        for ns in new_subs:
            ns_clean = ns.strip()
            if ns_clean not in taxonomy[sec][top]:
                taxonomy[sec][top].append(ns_clean)

    # 5. Reclassify affected questions under new subtopics
    if refinement_splits:
        reclassify_after_refinement(classifications, refinement_splits)

    # 5b. Verify no orphaned classifications (v1.7)
    for paper_id, paper_classifs in classifications.items():
        for c in paper_classifs:
            sub = c['subtopic']
            sec = c['section']
            top = c['topic']
            if sub not in taxonomy.get(sec, {}).get(top, []):
                # Orphaned classification — reclassify missed this question
                # Force-assign to first new subtopic as fallback
                available = taxonomy.get(sec, {}).get(top, [])
                if available:
                    c['subtopic'] = available[0]  # fallback assignment

    # 6. Log refinement results
    progress['discovery_log'].append({
        'batch': 'refinement_pass',
        'papers': [],
        'new_subtopics': [
            f"{s['section']}/{s['topic']}/{ns}"
            for s in refinement_splits
            for ns in s['new_subtopics']
        ],
        'removed_subtopics': [
            f"{s['section']}/{s['topic']}/{s['old_subtopic']}"
            for s in refinement_splits
        ],
        'count': sum(len(s['new_subtopics']) for s in refinement_splits)
    })

    # 7. Update metadata
    progress['_meta']['refinement_pass_done'] = True

    # If refinement found new subtopics, reset consecutive_empty counter
    # because the taxonomy just changed — need to verify stability again
    if refinement_splits:
        progress['_meta']['consecutive_empty_batches'] = 0
        print(f"\n  Refinement pass: {len(refinement_splits)} subtopics split into "
              f"{sum(len(s['new_subtopics']) for s in refinement_splits)} new subtopics.")
        print(f"  consecutive_empty_batches reset to 0 — resume scanning to verify stability.")
    else:
        print(f"\n  Refinement pass: no splits needed. Taxonomy depth is adequate.")

    from datetime import datetime, timezone
    progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
    save_scan_progress(progress, exam_code)

def check_dimensional_splits(questions, sec, top, sub):
    """
    v2.4 REFINEMENT ANALYSIS — check if a subtopic should be split or merged.

    TWO-PHASE CHECK (v2.4 — merge-first, then split):

      PHASE A — MERGE CHECK (priority):
        If this subtopic frequently confuses with another subtopic during
        classification (tracked via confidence scores), recommend MERGE
        rather than split. Over-splitting causes data loss (MPPSC proof).

      PHASE B — SPLIT CHECK (only if no merge needed):
        For each of the 4 recorded metadata dimensions:
          1. Collect distinct values: Counter(q[dimension] for q in questions)
          2. Remove null values from consideration
          3. If >= 2 distinct values AND each has >= MIN_PATTERN_SIZE:
             → candidate split, BUT must pass Q3 Unique Domain Check:
               (a) Different solving approach?
               (b) Separate coaching chapter?
               (c) Unambiguous classification between proposed splits?

      CONCRETE EXAMPLE:
        Subtopic "Spotting Errors" with 30 classified questions:
          question_task: {identify_error: 30}  → NO split (1 value)
          question_format: {in_sentence: 30}   → NO split (1 value)
          question_direction: {null: 30}        → skip (all null)
          thematic_domain: {subject_verb: 8, tense: 7, pronoun: 5,
                           preposition: 4, article: 3, conjunction: 3}
                           → CANDIDATE split. Q3 check:
                             (a) Different approach? Debatable.
                             (b) Separate coaching chapter? Not usually.
                             (c) Unambiguous? A question about subject-verb
                                 agreement in a complex tense → ambiguous
                                 between "subject_verb" and "tense".
                           → Q3(c) FAILS → DON'T SPLIT.

    DIMENSION CHECK ORDER AND MERGE RULE:
      Check all 4 metadata dimensions. For each dimension that yields
      2+ clusters with >= MIN_PATTERN_SIZE:
        Record the candidate split.

      After checking all dimensions:
        - If 0 dimensions yielded splits → return empty (no split needed)
        - If 1+ dimensions yielded splits → select the MOST NATURAL split
          (the one whose clusters most clearly pass Q3 Unique Domain Check).
        - Do NOT blindly merge multiple dimension splits into a cross-product.
          Apply Q3(c) to every proposed subtopic pair — if any pair has
          ambiguous classification, merge those two back together.

    SPLIT DECISION CRITERIA (v2.4 — Q3 Unique Domain Check required):
      A split is warranted ONLY when ALL of:
        (a) ≥15 classified questions in the subtopic (MIN_QUESTIONS_FOR_SPLIT)
        (b) 2+ distinct values exist for a dimension with ≥3 each (MIN_PATTERN_SIZE)
        (c) The distinction passes Q3: different solving approach + separate
            coaching chapter + unambiguous classification
      If ANY condition fails → no split.

    Returns: list of {section, topic, old_subtopic, new_subtopics: [str]}
             or empty list if no split needed.
    """
    from collections import Counter as Ctr
    splits = []
    dims = ['question_task', 'question_format', 'question_direction', 'thematic_domain']
    for dim in dims:
        values = [q.get(dim) for q in questions if q.get(dim) is not None]
        counts = Ctr(values)
        valid = {k: v for k, v in counts.items() if v >= MIN_PATTERN_SIZE}
        if len(valid) >= 2:
            splits.append({'dimension': dim, 'clusters': valid})
    # Claude merges and names the subtopics using domain knowledge
    # Returns structured split recommendations
    pass
    # NOTE (v2.13): Claude produces the named `new_subtopics` at runtime, then MUST validate
    # them with the deterministic guards below before applying (D6-4/D6-5).
```

# ── v2.13 SPLIT GOVERNANCE GUARDS (register D6-4 over-split / D6-5 under-split) ──
# D6-4: after Claude proposes `new_subtopics` for a split, run split_children_valid();
#       any near-duplicate pair returned MUST be merged back (enforces Q3(c) — over-split
#       otherwise produces two subtopics that later collapse to one mechanic → false BV-10;
#       QV-13 (Step 5) + §4-1b (Step 6) are the downstream backstops).
# D6-5: when distinct forms are MERGED into one subtopic (len(questions) < 15, or Q3
#       ambiguous), call merge_record() and keep the record so Step 7's scenario_key can
#       still separate the merged forms (no silent loss of a distinct question form).

```python
# D6-4 / D6-5 split governance guards. Pure, deterministic.
import re, unicodedata

def _canon(s):
    s=unicodedata.normalize('NFC', s or '')
    for d in ('‐','‑','‒','–','—','−'): s=s.replace(d,'-')
    s=re.sub(r'\s+',' ',s).strip().casefold()
    return s

def _tokens(name):
    # tokenize; normalize trivial plural (trailing s/es) so "relations"=="relation"
    toks=[t for t in re.split(r'[^a-z0-9]+', _canon(name)) if t and t not in
          ('and','of','the','a','an','in','to','for','with','on','&')]
    return {re.sub(r'(es|s)$','',t) for t in toks}

def _jaccard(a,b):
    A,B=_tokens(a),_tokens(b)
    if not A or not B: return 0.0
    return len(A&B)/len(A|B)

def split_children_valid(children, sim_threshold=0.6):
    """D6-4 OVER-SPLIT guard. children = proposed split subtopic names. Returns list of
    (a, b, jaccard) pairs that are near-duplicates (ambiguous split) → the caller MUST
    merge those pairs back (enforces check_dimensional_splits Q3(c)). Empty = all distinct."""
    viol=[]
    for i in range(len(children)):
        for j in range(i+1, len(children)):
            if _canon(children[i])==_canon(children[j]):
                viol.append((children[i],children[j],1.0)); continue
            s=_jaccard(children[i],children[j])
            if s>=sim_threshold:
                viol.append((children[i],children[j],round(s,2)))
    return viol

def merge_record(kept_name, merged_forms, reason):
    """D6-5 UNDER-SPLIT record. When distinct forms are merged into one subtopic (below
    MIN_QUESTIONS_FOR_SPLIT or Q3-ambiguous), record the constituent forms so Step 7's
    scenario_key can still separate them. Returns a structured, serialisable record."""
    forms=sorted({f.strip() for f in merged_forms if f and f.strip()})
    return {'subtopic': kept_name.strip(), 'merged_forms': forms,
            'reason': reason, 'separate_by': 'scenario_key'}

# ── WIRING ──
# In check_dimensional_splits Q3(c) / the apply-splits loop:
#     viol = split_children_valid(split['new_subtopics'])
#     if viol:
#         # merge each near-duplicate pair back into one child, then re-name; do NOT emit
#         # two subtopics that a downstream mechanic would treat as identical.
#         ...  # collapse pairs in viol; record with merge_record(kept, [a,b], "Q3(c) near-dup")
# In the MERGE branch (subtopic kept whole because distinct forms are ambiguous/thin):
#     records.append(merge_record(sub, [f for f in distinct_forms], "below MIN_QUESTIONS_FOR_SPLIT"))
# These records travel with the taxonomy so Step 7 keeps the forms distinct at scenario_key.
```

```python
def reclassify_after_refinement(classifications, refinement_splits):
    """
    After refinement splits, update all existing classifications to use
    the new subtopic names instead of the old broad ones.

    For each split:
      - Find all classifications using old_subtopic
      - Re-examine each question's pattern metadata
      - Assign to the correct new subtopic
      - Update the classification dict in place
    """
    for split in refinement_splits:
        sec = split['section']
        top = split['topic']
        old_sub = split['old_subtopic']
        new_subs = split['new_subtopics']

        for paper_id, paper_classifs in classifications.items():
            for c in paper_classifs:
                if (c['section'] == sec and c['topic'] == top
                        and c['subtopic'] == old_sub):
                    # Claude re-examines the question's metadata and assigns
                    # to the best-fit new subtopic
                    c['subtopic'] = assign_to_refined_subtopic(
                        c, new_subs
                    )

def assign_to_refined_subtopic(classification, new_subtopics):
    """
    Given a classification dict with pattern metadata and a list of new
    subtopic names (from a refinement split), determine which new subtopic
    this question belongs to.

    Uses question_task, question_format, question_direction, thematic_domain
    to match against the new subtopic names.

    Claude performs this mapping using domain knowledge.
    Returns: the best-fit new subtopic name (str).
    """
    pass  # Claude maps at runtime using metadata + subtopic name semantics
```

### S3-7 — Session management for large corpora

```
EXPECTED THROUGHPUT (v1.7):
  Each chat session should process 4-5 complete batches (12-15 papers).
  If a session processes fewer than 3 complete batches, Claude MUST note
  this as below-target throughput in the batch-end message.

  Expected sessions: ~ceil(total_papers × MIN_COVERAGE_RATIO / 12) minimum.
    50 papers  → ~2 sessions
    100 papers → ~3 sessions
    200 papers → ~5-6 sessions

SESSION HANDOFF PROTOCOL:
  When context approaches capacity (after completing the current batch):
    1. Complete the current batch (never leave partial — EC-P26)
    2. Save scan_progress.json + classifications.json via present_files
       (EXACTLY these 2 files — S10-1 closed set. No other files.
        Run S10-2 pre-delivery checklist before present_files.)
    3. Print: "Session limit. [X]/[Y] papers scanned.
       Download scan_progress.json + classifications.json →
       upload to project knowledge.
       New chat → Step 2b: PYQScan PYQ: <<Drive link>>"
    4. END response. Do NOT process another batch.

RESUME PROTOCOL:
  New session loads:
    1. scan_progress.json from project knowledge (schema version checked)
    2. classifications.json from project knowledge
    3. RE-LIST Drive files (do NOT rely on cached inventory — files may
       have been added or removed between sessions). Update
       drive_file_inventory in scan_progress.json with fresh listing.
    4. RE-RUN S3-2a pre-scan gate: display full inventory with progress.
       Show "Previously scanned: [M] papers. Remaining: [N-M] papers."
       If total files differ from cached inventory → warn user:
         "Drive folder changed since last session: was [X] files, now [Y].
          [added/removed] files detected."
       User re-confirms before scanning resumes.
    5. Resume from first unscanned paper in round-robin queue
```

### S3-8 — Scan progress JSON schema

```json
{
  "_meta": {
    "exam_code": "[ExamCode]",
    "phase": "0b_scan",
    "schema_version": "2.0",
    "source_taxonomy": "taxonomy_draft.json",
    "source_taxonomy_subtopics": 209,
    "papers_scanned": 65,
    "total_available": 200,
    "years_covered": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "convergence_status": "converged",
    "consecutive_empty_batches": 7,
    "refinement_pass_done": true,
    "last_updated": "2026-07-02T10:30:00Z"
  },
  "taxonomy": {
    "Section 1 Name": {
      "Topic A": ["Subtopic A1", "Subtopic A2", "Subtopic A3"],
      "Topic B": ["Subtopic B1", "Subtopic B2"]
    }
  },
  "exam_config": { },
  "papers_scanned_list": ["Paper_12-Sep-2025_Shift-1_Q1-Q100", "..."],
  "drive_file_inventory": [
    {"name": "Paper_12-Sep-2025_Shift-1_Q1-Q100.docx",
     "id": "1jD5lA67...", "year": 2025, "size": 50629}
  ],
  "discovery_log": [
    {
      "batch": 1,
      "papers": ["Paper_12-Sep-2025_Shift-1_Q1-Q100", "..."],
      "complete_batch": true,
      "new_subtopics": ["Section1/TopicA/NewSubtopic", "..."],
      "count": 3
    },
    {
      "batch": "refinement_pass",
      "papers": [],
      "new_subtopics": ["Section1/TopicA/SplitSubtopic1", "..."],
      "removed_subtopics": ["Section1/TopicA/OldBroadSubtopic"],
      "count": 5
    }
  ]
}
```

```
SEPARATE FILE — [ExamCode]_classifications.json:
{
  "Paper_12-Sep-2025_Shift-1_Q1-Q100": [
    {"q_num": 1, "section": "Section 1 Name",
     "topic": "Topic A", "subtopic": "Subtopic A1",
     "question_task": "find_match", "question_format": "word_pair",
     "question_direction": null, "thematic_domain": "profession_workplace"},
    {"q_num": 2, "section": "Section 1 Name",
     "topic": "Topic A", "subtopic": "Subtopic A2",
     "question_task": "find_match", "question_format": "mixed_alphanumeric",
     "question_direction": null, "thematic_domain": null}
  ]
}

scan_progress.json REQUIRED FIELDS (v1.7 — PYQApprove reads these):
  _meta.exam_code          (string)
  _meta.papers_scanned     (int, informational)
  _meta.refinement_pass_done (bool, must be True for approve)
  _meta.schema_version     (string, must be "2.0")
  taxonomy                 (dict — COMPLETE Section > Topic > [Subtopics])
  exam_config              (dict — from taxonomy_draft)

BANNED JSON FIELDS (v1.7 — Claude MUST NOT add any of these):
  convergence_recommendation, scan_analysis, recommendation,
  justification, assessment, analysis, suggestion, editorial,
  or ANY field not listed in the schema above.
```

---

## §4 — PHASE 0c: ANALYSIS DOC GENERATION (for approval)

### S4-1 — Generate merged Analysis doc from taxonomy

```
After Phase 0b scan completes (convergence or full coverage):
  Run: PYQApprove

PYQApprove REQUIRES these fields from scan_progress.json (v1.7):
  _meta.exam_code                    → used in doc title and filename
  _meta.papers_scanned               → informational (approval gate message)
  _meta.refinement_pass_done         → must be True; if False → error
  _meta.schema_version               → must be "2.0"
  taxonomy                           → complete dict (Section > Topic > [Subtopics])
  exam_config                        → section names, Q counts, metadata
If any required field is missing → "scan_progress.json incomplete. Re-run PYQScan."

This generates a SINGLE merged .docx Analysis doc containing ALL subjects:

  [ExamCode]_PYQ_Analysis.docx

The doc contains one section per subject (taxonomy top-level), separated by
PAGE BREAKS. Internal format per subject matches the IFAS reference:

  ═══ PAGE BREAK before each subject (except the first) ═══

  HEADER:
    "[ExamCode] — [Section Name]"                          (bold, 14pt)
    "Subject: [Section Name]"                              (bold)
    "PYQ Topic & Subtopic-wise Count"                      (bold)
    "Total: — Questions  |  [N] Topics  |  [M] Subtopics" (bold)

  MASTER SUMMARY TABLE:
    | Topic | Total Subtopics | Total PYQs |
    | Topic 1: [Name] | [count] | — |
    | Topic 2: [Name] | [count] | — |
    | ...             |         |   |
    | GRAND TOTAL     | [total] | — |

  PER-TOPIC SECTIONS (one per topic):
    "Topic [N]: [Topic Name]"                              (bold, heading)
    "Total PYQs: —  |  Subtopics: [count]"                (bold)
    | Subtopic | PYQ Count |
    | [Subtopic 1] | — |
    | [Subtopic 2] | — |
    | ...          |   |
    | TOTAL        | — |

  FOOTER:
    "IFAS Edutech  —  [ExamCode] [Section] PYQ Analysis"

  NOTE: All PYQ Count values are "—" (em-dash) at this stage.
        Phase B (--counts) fills them with actual numbers.

SUBJECT ORDERING: subjects appear in the order defined by the exam pattern's
  section list (exam_config.sections[]). If the taxonomy has subjects not in
  the exam pattern (rare), they appear after all patterned sections in
  alphabetical order.
```

### S4-2 — Analysis doc generation script

```python
# Use docx-js (npm) to create .docx file matching reference format.
# See §6 HEADING FORMAT CONTRACT for heading text patterns.
# All subtopic names MUST be .strip()-ed before writing (§7 NAME CONTRACT).

def generate_merged_analysis_doc(taxonomy, exam_code, section_order):
    """
    Generate a SINGLE merged Analysis .docx containing ALL subjects.
    taxonomy: { section_name: { topic_name: [subtopic_1, ...] } }
    section_order: ordered list of section names (from exam_config.sections[])
    PYQ counts are '—' (to be filled by Phase B --counts).

    Each subject section is separated by a PAGE BREAK (except the first).
    Internal structure per subject: header block, master summary table,
    per-topic subtopic tables, footer — identical to the previous per-file format.
    """
    # Implementation uses npm docx package per SKILL.md
    # Iterate section_order → for each section:
    #   if not first section: insert page break
    #   write header block, master summary table, per-topic tables, footer
    # Output: single [ExamCode]_PYQ_Analysis.docx
    pass
```

### S4-3 — Exam config delivery

```
APPROVE MODE DELIVERY (S10-1 closed set):
  Deliver via present_files: EXACTLY 2 files.
    1. [ExamCode]_PYQ_Analysis.docx  (single merged doc)
    2. [ExamCode]_exam_config.json
  No other files. Run S10-2 pre-delivery checklist before present_files.
  scan_progress.json and classifications.json are INPUTS — do NOT forward.

Also deliver [ExamCode]_exam_config.json (from Phase 0a).
This file is needed by PYQSort for section detection in Q-range mode.

Both the Analysis doc and exam_config.json go to [ExamCode] project Files section.
```

### S4-4 — Approval gate

```
Print:
  "Phase 0c complete. Merged Analysis doc generated:
   • [ExamCode]_PYQ_Analysis.docx
     Sections:
       [Section1]: [N1] topics, [M1] subtopics
       [Section2]: [N2] topics, [M2] subtopics
       ...
     Grand total: [T] topics, [S] subtopics across [K] sections
   • [ExamCode]_exam_config.json

   ★ APPROVAL REQUIRED ★
   Review the Analysis doc carefully:
   - Are all subjects from the syllabus present as sections?
   - Does each distinct syllabus item have its own Topic
     (not merged into super-categories like 'Vocabulary' or 'Grammar')?
   - Are subtopics faithful to the syllabus structure — does each
     explicitly identified syllabus entry correspond to a subtopic?
   - Is anything MISSING that the syllabus mentions?
   - Is anything EXTRA that is NOT in the syllabus?
   - Taxonomy ratio: [total_subtopics] / [syllabus_entries] = [ratio]×
     (guardrail from S2-3: flag at 2.0×, hard-stop at 3.0×)
   - Near-duplicate check: 0 pairs with >75% name similarity

   After approval:
   1. Upload Analysis doc + exam_config.json to [ExamCode] project Files
   2. Taxonomy is LOCKED — no further changes after upload
   3. Start PYQSort: upload 1 Row file + trigger PYQSort in [ExamCode] project

   If changes needed:
   - Edit the taxonomy_draft.json or re-run --taxonomy
   - Re-run --scan if needed
   - Re-run --approve to regenerate the Analysis doc"
```

---

## §5 — PHASE B: COUNT FILLING (after all sorting done)

### S5-1 — Read sorted PYQ files from Drive

```
Trigger: PYQCount PYQ: <<Drive link>>

Phase B reads ALL sorted PYQ files from the Drive folder.
These are the output of PYQSort — one sorted .docx per original Row file.

Processing model: batch up to 5 files at a time (BATCH_SIZE_COUNTS = 5).
Accumulate counts in a count_progress.json across batches.

FILE FILTERING (prevent non-sorted files from contaminating counts):
  1. List all .docx files from Drive folder (recursive, per EC-P23).
  2. Filter: keep ONLY files matching the sorted filename pattern:
       r'_Sorted_Q\d+-Q\d+\.docx$'
     Files that do NOT match this pattern are SKIPPED with a warning:
       "Skipped non-sorted file: [filename]"
     This prevents Row files, the Analysis doc, or other .docx files in the
     same Drive folder from being processed.
  3. If 0 sorted files found → "No sorted PYQ files found in Drive folder.
     Sorted files must match pattern: *_Sorted_Q1-QN.docx"

DUPLICATE DETECTION (prevent inflated counts):
  After filtering, check for duplicate sorted files (same date + session):
  1. Separate multi-date files (filename contains "_to_") — these represent
     unique combined papers and are EXCLUDED from dedup.
  2. For single-date files, extract date + session from filename using:
       r'(\d{1,2}-[A-Za-z]{3}-\d{4})_.*?(\w+)-(\d+)_Sorted_'
       → captures (date, session_keyword, session_number)
  3. Group single-date files by (date, session_number) pair.
  4. If any group has >1 file → keep the LARGER file (more likely to have
     images intact), skip the smaller. If sizes equal, keep alphabetically-
     first filename. Log:
       "Duplicate detected: [file1] vs [file2] — keeping [larger]"
  5. Deduplicated list (single-date survivors + all multi-date files)
     becomes the input for Task 1 and all subsequent steps.
```

### S5-1a — TASK 1: Pre-Count Confirmation Gate

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before ANY subtopic counting begins.
═══════════════════════════════════════════════════════════════════════

After listing all sorted PYQ files from Drive (S5-1), but BEFORE running
the batch counting loop (S5-4):

  1. Read EVERY sorted PYQ file from Drive using python-docx (same method
     as count_sorted_file in S5-2 — paragraph iteration, NOT Drive
     read_file_content which may strip content).
  2. For each file: count total questions using the SAME Q-pattern as
     count_sorted_file():
       re.match(r'^Q\.?\s*\d+', para.text.strip())
     This pattern is sufficient because PYQSort always outputs Q.<N>
     format (Step 1 normalizes to Q.<N>, renumber_stem preserves it).
     Store per-file count: task1_per_file[filename] = q_count
  3. Extract year from filename (S5-3 logic)
  4. Display a YEAR-WISE PAPER INVENTORY table:

     | Year | Paper File | Q Count |
     |------|-----------|---------|
     | 2025 | [ExamCode]_12-Sep-2025_Shift-1_Sorted_Q1-Q100.docx | 100 |
     | 2025 | [ExamCode]_13-Sep-2025_Shift-2_Sorted_Q1-Q100.docx | 100 |
     | ...  | ...       | ...     |
     | TOTAL | [N] papers | [T] questions |

  5. Print:
     "TASK 1 — PRE-COUNT CONFIRMATION
      Papers found: [N]
      Total questions across all papers: [T]

      ★ CONFIRMATION REQUIRED ★
      Verify these numbers match your expectation.
      Once confirmed, I will proceed with subtopic-level counting.
      If anything looks wrong, tell me and I will re-scan."

  6. WAIT for explicit user confirmation. Do NOT proceed to S5-4 until
     confirmed. The confirmed total [T] becomes the ACCURACY TARGET
     for Task 2.

PURPOSE: proves that Claude can see every file and every question
inside each file without fail. Catches Drive access issues, missing
files, or parsing failures BEFORE counting effort is wasted.
```

### S5-2 — Heading parser (Step 5 E-1 compatible)

```python
# CRITICAL — HEADING FORMAT CONTRACT
# This parser MUST use the SAME patterns as Step 5's parse_taxonomy_level().
# If these diverge, Phase B counts won't match Step 5's Frequency xlsx.

def parse_taxonomy_level(text):
    """
    IDENTICAL to Step 5's parse_taxonomy_level() — DO NOT MODIFY independently.
    Any change here MUST be mirrored in Step 5's Framework_MockTestAnalyse.md.
    """
    if re.match(r'Subject:|Domain:', text):
        return 1, text.split(':', 1)[1].strip()
    if re.match(r'Topic\s+\d+:', text):
        return 2, re.sub(r'Topic\s+\d+:\s*', '', text).strip()
    if re.match(r'Chapter\s+\d+', text):
        return 2, text.strip()
    return 3, text.strip()

# Option patterns — MUST match Step 5's E-3 OPT_PATTERNS exactly.
# Capture groups are present for parity; is_option() only checks match/no-match.
# The (.+) suffix is critical: it requires actual option text after the label,
# preventing bare labels like "1. " from being treated as options.
OPT_PATTERNS = [
    r'^([1-5])\.\s+(.+)',           # 1. 2. 3. 4. 5.  (up to 5 options)
    r'^([A-Ea-e])\.\s+(.+)',        # A. B. C. D. E.
    r'^\(([1-5])\)\s+(.+)',         # (1) (2) (3) (4) (5)
    r'^\(([A-Ea-e])\)\s+(.+)',      # (A) (B) (C) (D) (E) / (a)(b)(c)(d)(e)
    r'^([A-Ea-e])\)\s+(.+)',        # A) B) C) D) E) / a) b) c) d) e)
]

def is_option(text):
    """Aligned with Step 5's is_option() — same patterns."""
    return any(re.match(p, text.strip()) for p in OPT_PATTERNS)

def is_taxonomy_heading(para):
    """IDENTICAL logic to Step 5's is_taxonomy_heading() — DO NOT MODIFY independently."""
    text = para.text.strip()
    if not text: return False
    if re.match(r'^Q\.?\s*\d+', text): return False
    if is_option(text): return False
    # Shift-tag detection: [DD-Mon-YYYY Shift X] — DD may be 1 or 2 digits
    if re.match(r'\[\d{1,2}-', text): return False
    has_bold = any(r.bold for r in para.runs if r.text.strip())
    return has_bold and len(text) < 100

def count_sorted_file(docx_path):
    """
    Walk a sorted PYQ .docx, count questions per (section, topic, subtopic).
    Returns: (counts, orphans)
      counts:  {(section, topic, subtopic): count}
      orphans: [(q_num, reason)]  — questions that couldn't be attributed
    """
    from docx import Document
    doc = Document(docx_path)
    counts = Counter()
    orphans = []
    cur_sec = cur_top = cur_sub = ''

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text: continue
        if is_taxonomy_heading(para):
            lv, content = parse_taxonomy_level(text)
            # CRITICAL — reset child pointers when parent changes.
            # Matches Step 5 E-1: current_path[:level-1] + [content]
            # Without this, a Q after a new Topic heading but before its
            # first Subtopic heading would silently inherit the WRONG
            # subtopic from the previous topic.
            if lv == 1:
                cur_sec = content; cur_top = ''; cur_sub = ''
            elif lv == 2:
                cur_top = content; cur_sub = ''
            else:
                cur_sub = content
        elif re.match(r'^Q\.?\s*\d+', text):
            q_match = re.match(r'^Q\.?\s*(\d+)', text)
            q_num = int(q_match.group(1)) if q_match else 0
            if not cur_sec:
                orphans.append((q_num, 'no_section_context'))
            elif not cur_sub:
                orphans.append((q_num, 'no_subtopic_context'))
            else:
                counts[(cur_sec, cur_top, cur_sub)] += 1

    return counts, orphans
```

### S5-3 — Year extraction from sorted files

```python
def extract_year_from_sorted_filename(filename):
    """
    Sorted PYQ filenames follow patterns:
      [ExamCode]_DD-Mon-YYYY_Shift-N_Sorted_Q1-QN.docx
      [ExamCode]_DD-Mon-YYYY_to_DD-Mon-YYYY_Sorted_Q1-QN.docx
    Extract the primary year.
    """
    m = re.search(r'(\d{1,2})-([A-Za-z]{3})-(\d{4})', filename)
    return int(m.group(3)) if m else None
```

### S5-4 — Batch counting loop

```
BATCH_SIZE_COUNTS = 5  # max 5 papers per batch

For each batch of sorted PYQ files (up to 5 per batch):
  1. Read each file → count_sorted_file() → (per-subtopic counts, orphans)
  2. Track per-file attributed count:
       per_file_attributed[filename] = sum(counts.values())
     This is compared against task1_per_file[filename] in Task 2 diagnostic.
  3. If orphans non-empty for any file → log:
       "WARNING: [filename] has [N] orphan questions: Q[x] (reason), ..."
     Accumulate all orphans in all_orphans[(filename, q_num)] = reason
  4. Extract year from filename
  5. Accumulate: counts_by_year[(section, topic, subtopic)][year] += count
  6. Track papers_per_year[year] += 1
  7. Save count_progress.json after each batch

After all files processed:
  If all_orphans is non-empty:
    Print "⚠ [N] orphan questions found across [M] files.
           These questions appear before any Subject/Subtopic heading
           and cannot be attributed to a taxonomy triple.
           This is a PYQSort bug — sorted files must have taxonomy
           headings before every question block."
    List all orphans with file + Q number + reason.
    HARD STOP — do not proceed until orphans are resolved.
  If all_orphans is empty:
    Run Task 2 accuracy gate (S5-4a).
```

### S5-4a — TASK 2: Post-Count Accuracy Gate

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before touching the Analysis doc.
Zero tolerance: not even 1 question may be missing or extra.
═══════════════════════════════════════════════════════════════════════

After all batches in S5-4 are complete, but BEFORE updating the Analysis doc
(S5-5):

  1. Compute grand_total = sum of ALL subtopic counts across all
     (section, topic, subtopic) triples.

  2. Compare grand_total against the CONFIRMED total from Task 1 (S5-1a).

  3. Display a FULL HIERARCHICAL BREAKDOWN:

     SUBJECT: [Section 1 Name]
       Topic 1: [Topic Name] — [topic_total] Qs
         [Subtopic A] — [count]
         [Subtopic B] — [count]
         ...
         Topic Total: [sum]
       Topic 2: [Topic Name] — [topic_total] Qs
         ...
       Section Total: [section_total]

     SUBJECT: [Section 2 Name]
       ...

     ═══════════════════════════════
     GRAND TOTAL: [grand_total] Qs
     TASK 1 CONFIRMED TOTAL: [T] Qs
     MATCH: ✓ / ✗
     ═══════════════════════════════

  4. ACCURACY CHECK:
     IF grand_total == confirmed_total (Task 1):
       Print "TASK 2 PASSED — all [T] questions accounted for."
       Proceed to S5-4b (Task 2.5).
     ELSE:
       Print "TASK 2 FAILED — mismatch: counted [grand_total], expected [T].
              Difference: [delta] questions."

       PER-FILE DIAGNOSTIC:
       Compare task1_per_file[filename] (Task 1 raw Q-count) against
       per_file_attributed[filename] (S5-4 heading-attributed count)
       for every file. Display files where the counts differ:
         | File | Task 1 Qs | Attributed Qs | Diff |
         | [filename1] | 100 | 98 | -2 |
         | ...
       This pinpoints exactly WHICH files have the gap and by how many.
       Common causes: heading parser missed a question (malformed heading
       above it), or orphan questions were present (should have been
       caught by orphan gate, but verify).

       Re-scan the identified files. Fix the root cause.
       Repeat until grand_total == confirmed_total.
       Do NOT proceed to S5-4b until match is exact.

PURPOSE: guarantees 100% accuracy — every question counted by Task 1
is classified into exactly one (section, topic, subtopic) triple.
No question silently dropped by the heading parser.
```

### S5-4b — TASK 2.5: Taxonomy Name Cross-Check

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before writing ANY count to the Analysis doc.
Prevents silent count loss from name mismatches.
═══════════════════════════════════════════════════════════════════════

After Task 2 passes, but BEFORE S5-5 (doc writing):

  1. Load the APPROVED Analysis doc from project knowledge.
  2. Extract the complete taxonomy: every (section, topic, subtopic) triple
     from the Analysis doc.

     EXTRACTION METHOD (must produce names matching parse_taxonomy_level output):

       SECTION NAME: from the doc header line "[ExamCode] — [Section Name]".
         Extract: strip "[ExamCode] — " prefix → section name.
         This MUST match what parse_taxonomy_level() returns for
         "Subject: [Section Name]" → text.split(':', 1)[1].strip().

       TOPIC NAME: from master summary table cells "Topic N: [Name]".
         Extract: apply parse_taxonomy_level() or equivalent strip:
         re.sub(r'Topic\s+\d+:\s*', '', cell_text).strip() → topic name.
         This MUST match what parse_taxonomy_level() returns for
         "Topic N: [Name]" headings in sorted files.

       SUBTOPIC NAME: from per-topic table cells (raw subtopic text).
         Extract: cell_text.strip() → subtopic name.
         Skip rows where cell text is "TOTAL" or "Subtopic" (header row).
         This MUST match what parse_taxonomy_level() returns for bare
         subtopic headings in sorted files (default → level 3, text.strip()).

     The key invariant: for every triple, the extracted string must be
     BYTE-IDENTICAL to what count_sorted_file() produces via
     parse_taxonomy_level(). If the Analysis doc has "Analogy" and the
     sorted file heading says "Analogy " (trailing space), Task 2.5
     catches it as a phantom triple.

  3. Build two sets:
       counted_triples  = set of all (section, topic, subtopic) from counting
       taxonomy_triples = set of all (section, topic, subtopic) from the Analysis doc

  4. Compute:
       phantom_triples = counted_triples - taxonomy_triples
         (counted in sorted files but NOT in the Analysis doc)
       uncounted_subtopics = taxonomy_triples - counted_triples
         (in the Analysis doc but have zero counted questions)

  5. PHANTOM TRIPLE CHECK:
     IF phantom_triples is non-empty:
       Print "TASK 2.5 FAILED — [N] phantom triples found.
              These subtopics were counted in sorted PYQ files but do NOT
              exist in the Analysis doc. Likely cause: name mismatch
              (trailing space, dash variant, case difference).

              Phantom triples:"
       For each phantom: print (section, topic, subtopic) with count.
       Also print the CLOSEST MATCH from taxonomy_triples (fuzzy match)
       to help diagnose the mismatch.

       HARD STOP — do not proceed to S5-5. Fix the name mismatch:
         Option A: re-sort the affected papers (PYQSort used wrong name)
         Option B: update the Analysis doc taxonomy (if doc has the typo)
       Either way, the names MUST match exactly before counts are written.

  6. UNCOUNTED SUBTOPICS (informational, not a stop):
     IF uncounted_subtopics is non-empty:
       Print "INFO: [N] subtopics in the Analysis doc have 0 PYQ counts.
              These will be written as '0' in the doc (not left as '—')."
       List them. This is expected for Zero-PYQ subtopics (EC-P17).

PURPOSE: catches the most dangerous silent failure in Phase B — a name
mismatch that causes counts to vanish. Task 2 total-match passes because
the question IS counted, just under a wrong name. Without this cross-check,
some subtopics get inflated counts and others get 0, and the error is
invisible until Step 6's BV-0A (too late).
```

### S5-5 — TASK 3: Update the Analysis doc with counts (doc-writing accuracy guarantee)

```
═══════════════════════════════════════════════════════════════════════
MANDATORY — every number in the Analysis doc must be arithmetically
perfect at ALL 4 levels. Not even 1 question mismatch tolerated.
═══════════════════════════════════════════════════════════════════════

Read the APPROVED Analysis doc (from project knowledge).
For each subject section in the doc:

  LEVEL 1 — SUBTOPIC CELLS:
    Replace every "—" PYQ Count cell with the exact count from the
    Task 2-verified aggregated data for that (section, topic, subtopic).
    ZERO-COUNT RULE: if a subtopic has 0 PYQs (present in Analysis doc
    taxonomy but absent from counted triples — per Task 2.5 uncounted
    list), write "0" explicitly. No subtopic cell may remain "—" after
    Phase B. "—" means "not yet counted"; "0" means "counted, none found".
    This distinction matters for Step 6 (Blueprint) zero-PYQ handling.

  LEVEL 2 — PER-TOPIC TOTAL ROWS:
    Each topic's TOTAL row = computed sum of all its subtopic counts.
    NOT a hardcoded number — always SUM(subtopic cells in that topic).
    Verify: TOTAL row == sum of subtopic cells above it.

  LEVEL 3 — MASTER SUMMARY TABLE:
    Each topic's "Total PYQs" cell in the master summary table =
    that topic's TOTAL row from Level 2.
    GRAND TOTAL row = sum of all topic "Total PYQs" cells.
    Verify: GRAND TOTAL == sum of all topic totals.

  LEVEL 4 — HEADER LINE:
    "Total: — Questions" updated to the section's actual total.
    Verify: header total == GRAND TOTAL from Level 3.

  CROSS-CHECK (must ALL be equal):
    header_total == grand_total == sum(topic_totals) == sum(all_subtopic_counts)
    If ANY level doesn't add up → fix before saving.

  Save updated .docx only after cross-check passes for ALL sections.

After ALL subject sections updated:
  Verify: sum of all section header totals == Task 1 confirmed total.
  If mismatch → fix before delivering.

COUNTS MODE DELIVERY (S10-1 closed set):
  Deliver via present_files: EXACTLY 1 file.
    1. [ExamCode]_PYQ_Analysis.docx  (UPDATED with PYQ counts)
  No other files. count_progress.json is INTERNAL — do NOT deliver
  at completion. (It IS delivered at session breaks for resume only.)
  Run S10-2 pre-delivery checklist before present_files.

Deliver the updated Analysis doc via present_files.
```

### S5-6 — Count progress JSON schema

```json
{
  "_meta": {
    "exam_code": "[ExamCode]",
    "phase": "B_counts",
    "files_processed": 150,
    "total_files": 200,
    "confirmed_total": 20000,
    "files_processed_list": [
      "[ExamCode]_12-Sep-2025_Shift-1_Sorted_Q1-Q100.docx",
      "[ExamCode]_13-Sep-2025_Shift-2_Sorted_Q1-Q100.docx"
    ]
  },
  "counts_by_year": {
    "('[Section 1 Name]', '[Topic A]', '[Subtopic A1]')": {
      "2019": 14, "2020": 9, "2021": 8, "2022": 50, "2023": 70,
      "2024": 46, "2025": 32
    }
  },
  "papers_per_year": {
    "2019": 19, "2020": 16, "2021": 8, "2022": 40,
    "2023": 39, "2024": 36, "2025": 46
  },
  "all_orphans": {}
}
```

### S5-7 — Phase B session management

```
═══════════════════════════════════════════════════════════════════════
SESSION MANAGEMENT — for large corpora spanning multiple sessions
═══════════════════════════════════════════════════════════════════════

Phase B with 200+ papers at 5/batch = 40+ batches may span multiple
chat sessions due to context limits. Protocol:

FIRST SESSION:
  1. S5-1: list + filter + dedup Drive files
  2. S5-1a: Task 1 inventory → user confirmation
  3. S5-4: batch counting (5/batch) until context limit reached
  4. Save count_progress.json with:
     - _meta.files_processed, _meta.total_files
     - _meta.confirmed_total (the Task 1 confirmed number)
     - _meta.files_processed_list (filenames already counted)
     - accumulated counts_by_year and papers_per_year
  5. Print session handoff message:
     "Phase B session paused. Progress: [N]/[T] files processed.
      count_progress.json saved.
      To resume: download count_progress.json → upload to [ExamCode]
      project → trigger: PYQCount PYQ: <<same Drive link>>"

RESUME SESSION:
  1. Trigger: PYQCount PYQ: <<Drive link>>
  2. Detect count_progress.json in project knowledge.
  3. Load progress: restore counts_by_year, papers_per_year, confirmed_total.
  4. Re-list Drive files (S5-1 filtering + dedup).
  5. RE-RUN Task 1 (S5-1a): display full inventory again. User re-confirms.
     This catches any files added/removed between sessions.
     If confirmed_total differs from previous session → warn user and
     ask which total to use as accuracy target.
  6. Skip already-processed files (check against files_processed_list).
  7. Continue batch counting from where it left off.

COMPLETION:
  When all files processed:
  8. Run Task 2 (S5-4a), Task 2.5 (S5-4b), Task 3 (S5-5) in sequence.
  9. Deliver the updated Analysis doc.

TARGET: 8-10 batches per session (40-50 papers). Adjust based on
context usage — counting is lighter than classification, so more
batches fit per session than Phase 0b.
```

### S5-8 — Phase B execution model

```
═══════════════════════════════════════════════════════════════════════
EXECUTION MODEL — Python script, 3 tool calls per session
═══════════════════════════════════════════════════════════════════════

Phase B counting is a mechanical operation (heading parsing + Q-pattern
matching) — NOT a judgment task. It MUST be executed via Python script,
not manual paragraph-by-paragraph Claude reading in chat.

PER-SESSION EXECUTION:

  CALL 1 — create_file: Write count_pipeline.py containing:
    1. Drive file listing via Google Drive MCP (list_files)
    2. File filtering (_Sorted_ pattern) and dedup logic
    3. Task 1: download each file via Drive MCP (download_file_content),
       parse with python-docx, count Q-patterns, build inventory table
    4. Heading parser functions (parse_taxonomy_level, is_taxonomy_heading,
       is_option, count_sorted_file — from S5-2, byte-identical)
    5. Batch counting loop (5/batch, accumulate counts_by_year)
    6. Orphan tracking and per-file attributed counts
    7. Save count_progress.json after each batch
    8. Print Task 1 inventory table for user confirmation

  CALL 2 — bash_tool: Run count_pipeline.py
    → Downloads files, counts, saves progress, prints inventory

  CALL 3 — (after user confirms Task 1)
    Either: continue counting (next session's CALL 1 if more files)
    Or:     run Task 2 + Task 2.5 + Task 3 gates and deliver

  For the FINAL session (all files counted):
    CALL 1 — create_file: Write count_finalize.py containing:
      1. Load count_progress.json
      2. Task 2: compute grand total, display breakdown, compare
      3. Task 2.5: load Analysis doc, extract taxonomy, cross-check
      4. Task 3: update Analysis doc with counts (all 4 levels + cross-check)
      5. Save updated .docx file to /mnt/user-data/outputs/
    CALL 2 — bash_tool: Run count_finalize.py
    CALL 3 — present_files: Deliver the updated Analysis doc
             (EXACTLY 1 file — S10-1 --counts closed set.
              count_progress.json is NOT delivered at completion.
              Run S10-2 pre-delivery checklist before present_files.)

NOTE: Task 1 inventory display happens in chat (printed by the script).
User confirmation is a chat response. The script pauses after Task 1
output — Task 2/2.5/3 run only after user confirms and all files are
processed.

DEPENDENCY: python-docx must be installed (pip install python-docx
--break-system-packages). Google Drive MCP tools must be connected.
```

---

## §6 — HEADING FORMAT CONTRACT

```
═══════════════════════════════════════════════════════════════════════
HEADING FORMAT CONTRACT — PYQSort ↔ Step 5 (PYQExtract) E-1 PARSER
═══════════════════════════════════════════════════════════════════════

PYQSort produces sorted PYQ files with headings in THIS EXACT format.
Step 5's parse_taxonomy_level() parses THIS EXACT format.
Phase B's count parser uses THIS EXACT format.

ANY deviation breaks the entire downstream pipeline.

LEVEL 1 (Subject — the taxonomy top-level, from syllabus):
  Text format: "Subject: <Subject Name>"
  Example:     "Subject: General Intelligence & Reasoning"
  Styling:     14pt, Bold, Navy #003366
  Parser:      re.match(r'Subject:|Domain:', text) → level 1
               content = text.split(':', 1)[1].strip()
  Result:      "General Intelligence & Reasoning"

LEVEL 2 (Topic):
  Text format: "Topic <N>: <Topic Name>"
  Example:     "Topic 1: Analogy"
  Styling:     12pt, Bold, Black #000000
  Parser:      re.match(r'Topic\s+\d+:', text) → level 2
               content = re.sub(r'Topic\s+\d+:\s*', '', text).strip()
  Result:      "Analogy"

LEVEL 3 (Subtopic):
  Text format: "<Subtopic Name>"  (no prefix — just the name)
  Example:     "Mixed Number-Letter Analogy"
  Styling:     11pt, Bold, Navy #003366
  Parser:      default → level 3, content = text.strip()
  Result:      "Mixed Number-Letter Analogy"

DATE LABEL:
  Text format: "[DD-Mon-YYYY Shift X]"
  Example:     "[12-Sep-2025 Shift 1]"
  Styling:     11pt, Bold, Navy #003366, Right-aligned
  NOT a heading → skipped by is_taxonomy_heading() via shift-tag detection

QUESTION:
  Text format: "Q.<N>  <stem text>"
  NOT a heading → skipped by is_taxonomy_heading() via Q-pattern detection
```

---

## §7 — NAME CONSISTENCY CONTRACT

```
═══════════════════════════════════════════════════════════════════════
NAME CONSISTENCY — SINGLE SOURCE OF TRUTH
═══════════════════════════════════════════════════════════════════════

The APPROVED Analysis doc is the SINGLE SOURCE OF TRUTH for all
display names (Section, Topic, Subtopic). Every downstream consumer
reads names from the Analysis doc or from files derived from it.

CHAIN:
  Phase 0c (Analysis doc) → PYQSort (reads taxonomy) → Sorted PYQ headings
  → Step 5 E-1 parser → section_rules.md → manifest.json
  → Step 6 (Blueprint) → Step 7 (Create)

RULES:
  1. ALL names MUST be .strip()-ed at WRITE time. No trailing/leading whitespace.
  2. PYQSort MUST copy subtopic names EXACTLY from the Analysis doc — no rewording,
     no punctuation changes, no case changes.
  3. Phase B MUST use the SAME heading parser as Step 5 (§5-2).
  4. If a name needs correction: update the Analysis doc, re-approve, re-sort
     ALL affected papers. Never fix downstream only.

KNOWN RISK — COSMETIC VARIATIONS:
  "Triangles — Centres, Congruence, Similarity" (em-dash)
  "Triangles - Centres, Congruence, Similarity"  (hyphen)
  These are DIFFERENT strings. The subtopic_id contract (Step 5 slugify)
  handles this: both produce the same slug. But for cleanliness, Phase 0c
  MUST use consistent punctuation throughout.

VERIFICATION:
  After Phase B --counts, compare subtopic names in the updated Analysis doc
  against names in Step 5's section_rules.md. If ANY mismatch → flag as error.
  The slugify-based subtopic_id contract tolerates cosmetic differences, but
  zero mismatches is the standard.
```

---

## §8 — CLASSIFICATION RULES (Universal)

```
═══════════════════════════════════════════════════════════════════════
UNIVERSAL CLASSIFICATION RULES — APPLY TO ALL EXAMS
═══════════════════════════════════════════════════════════════════════

These rules are embedded in the framework and apply to every PYQAnalyse
scan and every PYQSort invocation. Exam-specific precedents are loaded
from the Analysis doc or a companion config file.

RULE 1 — TOPICAL HOME WINS OVER SOLVE METHOD
  Pick the subtopic whose DOMAIN matches what the question is ABOUT,
  not what technique is USED to solve it.
  Example: Bank deposits earning interest → Simple Interest (not Percentage)
  Example: Two trains crossing → Trains/Boats (not Speed/Distance/Time)
  Example: Discount on marked price + resulting profit → Discount (not P&L)

RULE 2 — THE VERB AT THE END OF THE STEM DECIDES
  "find the ratio" → Ratio & Proportion
  "find the percentage" → Percentage
  "find the value of [trig expression]" → Trigonometry
  "find the average" → Average

RULE 3 — OMML-AWARE CLASSIFICATION IS MANDATORY
  When a question stem contains <m:oMath> math expressions, RENDER the math
  before classifying. Walk <m:t>, <m:r>, <m:f>, <m:sSup>, <m:sSub>, <m:rad>.
  "OMML obscured" is NEVER an acceptable reason to guess.
  PHASE 0b EXCEPTION: During lightweight scan via Drive read_file_content,
  OMML formulas may be stripped. Use fallback classification (S3-2 OMML
  HANDLING: Q-position + option content + context). Log "OMML-obscured"
  in question_format. This exception does NOT apply to PYQSort (Phase A)
  which MUST render OMML fully via python-docx.

RULE 4 — SECTION DETERMINED BY STRUCTURE, NOT CONTENT
  If marker_mode = true: section from module separator (=== Subject ===)
  If marker_mode = false: section from Q-number range in exam_config
  NEVER classify section from question content alone (a maths question in
  the Reasoning section stays in Reasoning — it might be Mathematical Operations).

RULE 5 — CLOSEST FIT FOR UNCLASSIFIABLE QUESTIONS
  If no subtopic fits perfectly, classify under the closest match.
  No flagging, no halting. Decide and move on.
  The closest match is determined by: topical home (Rule 1) > stem keywords >
  option structure > question format.

RULE 6 — IMAGE/FIGURAL QUESTIONS
  If question has image in stem with no meaningful text:
  Classify under the section's spatial/figural subtopic if one exists.
  If no figural subtopic in taxonomy: classify under the most general subtopic
  in the section.

RULE 7 — PATTERN METADATA RECORDING (Phase 0b scan ONLY)
  During Phase 0b scan, EVERY classification MUST include 4 pattern
  metadata fields in addition to (section, topic, subtopic):

  question_task: what the student is asked to DO
    Values: find_match, find_next, find_wrong, select_correct,
            select_incorrect, identify_error, correct_error,
            fill_blank, rearrange, calculate, determine, classify,
            match_pair, complete_figure, decode, interpret_data,
            find_answer (for RC), or other descriptive string.

  question_format: how the content is presented
    Values: standalone_word, standalone_number, word_pair, number_pair,
            in_sentence, in_passage, word_list, number_set, number_letter_mixed,
            figure, table_based, matrix, code_string, statement_based,
            dialogue_based, or other descriptive string.

  question_direction: transformation direction if applicable
    Values: a_to_b, b_to_a, null (if not a transformation question)
    Example: Active→Passive = a_to_b, Passive→Active = b_to_a

  thematic_domain: knowledge area if classifiable
    Values: use snake_case descriptors relevant to the Topic.
    Example for OWS: actions_behaviour, persons_professionals,
      government_legal, animals_nature, literary_arts, medical_phobias,
      branches_of_study, places_structures
    Example for Spotting Errors: subject_verb_agreement, tense_errors,
      pronoun_errors, article_errors, preposition_errors
    Value: null if the question is generic / domain-independent

  These fields are NOT used during PYQSort (Phase A) — they exist solely
  to enable the Subtopic Refinement Pass (§3-6). They are stored in
  scan_progress.json classifications and discarded after approval.

  The metadata does NOT need to be perfect — it needs to be CONSISTENT
  enough to detect clusters. If two questions with the same metadata
  pattern belong to different subtopics, the refinement pass will split.
```

---

## §9 — EDGE CASES

```
EC-P1: EXAM WITH 0 PYQ PAPERS
  Phase 0b has nothing to scan. Run PYQScan anyway — it detects 0 papers,
  runs refinement pass (with 0 classifications → no splits), saves
  scan_progress.json, and prints "Run: PYQApprove".
  Taxonomy = 100% from Step 2a's per-entry decision tree (S2-3 Step 2),
  which produces syllabus-faithful subtopics even without any PYQ papers.
  --approve generates the Analysis doc with all counts = "—" (filled by Phase B).
  PYQSort never runs (no Row files). Phase B never runs.
  Step 5: section_rules with all confidence='absent'.
  Step 6: handles zero-PYQ exam via §5 ZP rotation.

EC-P2: EXAM WITH 1-2 PYQ PAPERS ONLY
  Falls under Gate 0 (SMALL_CORPUS_THRESHOLD = 20): all papers scanned.
  Gate 4 (refinement pass) still applies after all papers are scanned.
  Taxonomy depth relies primarily on Step 2a's syllabus-faithful derivation;
  scanning 1-2 papers provides minimal discovery but validates coverage.
  Taxonomy may be incomplete but Step 2a's domain knowledge compensates.

EC-P3: CROSS-SHIFT DUPLICATE QUESTIONS
  Same question in Shift 1 and Shift 2 of same date.
  Both are scanned and classified. Convergence tracks NEW SUBTOPICS
  (not question volume), so duplicates don't inflate discovery count
  or falsely trigger early exit.

EC-P4: RC / CLOZE LINKED QUESTIONS (5 Qs per passage)
  Each sub-question counted as 1 PYQ. 5 passage questions = 5 PYQs.
  Classify each sub-question by its individual task/pattern:
    - Q asks for a word's meaning → "Vocabulary in Context" subtopic
    - Q asks for factual detail → "Direct/Factual Retrieval" subtopic
    - Q asks for main idea → "Main Idea/Theme/Purpose" subtopic
  Each sub-Q may belong to a DIFFERENT subtopic under the same Topic.
  Passage text preserved per question in sorted output (per PYQSort design).

EC-P5: FIGURAL-ONLY QUESTIONS DURING SCAN
  Question has image in stem, no meaningful text.
  Phase 0b: classify under section's figural/spatial subtopic.
  Phase A (PYQSort): has image access for better classification.
  The subtopic must exist in taxonomy from Phase 0a/0b.

EC-P6: SECTION DETECTION — MARKERS vs Q-RANGE
  Framework auto-detects:
    Check first few paragraphs for === separators.
    If found → marker_mode = true (read module names from separators)
    If not → marker_mode = false (use Q-range from exam_config)
  Both modes can coexist across exams. exam_config.marker_mode is authoritative.

EC-P7: SAME SUBTOPIC NAME IN MULTIPLE TOPICS
  Example: "Subject-Verb Agreement" under both Spotting Errors AND Sentence Improvement.
  The (Section, Topic, Subtopic) TRIPLE is unique. Both are valid taxonomy entries.
  Classification uses the full triple, not just the subtopic name.

EC-P8: YEAR EXTRACTION FROM FILENAME FAILS
  Filename doesn't contain a recognisable year pattern.
  Resolution: skip this file from year-wise counts in Phase B.
  Log a warning. The file still contributes to total PYQ count.

EC-P9: VARIABLE Q COUNT PER PAPER
  Some exams have papers with different Q counts (e.g., 96Q vs 100Q).
  Framework handles any Q count — no hardcoded total.
  Q-range mode: if paper has fewer Qs than expected, later sections may have
  0 questions. This is valid (partial paper).

EC-P10: BILINGUAL QUESTIONS (Hindi + English)
  Preserve non-Latin scripts in sorted output.
  Classification uses English portion of stem.
  Font fallback for Devanagari/regional scripts (Nirmala UI, Mangal, etc.).

EC-P11: DI TABLES IN QUESTIONS
  Full multi-row DI table → classify as Statistics / Data Tables (DI).
  Small 2-4 row reference table → classify by the arithmetic operation.
  Tables preserved verbatim in sorted output (original font size kept).

EC-P12: OMML FORMULAS IN STEMS
  Render OMML before classification. MANDATORY in both Phase 0b and Phase A.
  "OMML obscured" is never acceptable.

EC-P13: TAXONOMY APPROVED BUT USER FINDS ERROR LATER
  After approval, taxonomy is LOCKED. If error found after sorting has started:
  1. Correct the Analysis doc
  2. Re-upload to [ExamCode] project
  3. Re-sort ALL papers processed so far
  This is the cost of a taxonomy error. Framework documents this prominently
  in the approval gate message.

EC-P14: PHASE B AND STEP 5 COUNT MISMATCH
  Both parse sorted PYQ headings. Both use parse_taxonomy_level().
  If counts diverge: Step 6's BV-0A cross-check catches it.
  Root cause: one parser diverged from the heading format contract (§6).
  Fix: ensure both use IDENTICAL parser code.

EC-P15: VERY LARGE TAXONOMY (500+ subtopics)
  Some exams have many subtopics. Classification rules scale linearly.
  Context window may need BATCH_SIZE reduced to 2 for Phase 0b scan
  to fit the full taxonomy + 2 papers + classification output.
  Phase A (PYQSort) always processes 1 paper — unaffected by taxonomy size.
  Refinement pass (§3-6) also scales linearly — processes per-subtopic.

EC-P16: EXAM PATTERN CHANGES BETWEEN YEARS
  2024 exam has Figural questions, 2025 removes them.
  Taxonomy includes ALL subtopics from ALL years.
  Phase B counts will show 0 for 2025 on Figural subtopics.
  Step 6 handles year-specific patterns via recency weighting.

EC-P17: SUBTOPIC WITH 0 PYQS AFTER REFINEMENT SPLIT
  Refinement splits "Analogy" subtopic "Number Analogy" into 3 new subtopics.
  Some new subtopics may have 0 classified questions (if no questions in
  the scanned set matched that pattern). This is VALID — the subtopic
  exists because domain knowledge says it's a real exam pattern.
  Phase B will fill actual counts later. A 0-count subtopic is harmless;
  a missing subtopic is a taxonomy failure.

EC-P18: REFINEMENT CREATES DUPLICATE SUBTOPIC NAME ACROSS TOPICS
  Refinement splits create "Subject-Verb Agreement" under Topic "Spotting
  Errors" — but the same name already exists under Topic "Sentence
  Improvement". This is VALID per EC-P7: the (Section, Topic, Subtopic)
  TRIPLE is unique. Both are legitimate taxonomy entries because they
  represent different question types (finding the error vs improving
  the sentence) that happen to test the same grammar concept.

EC-P19: SCAN RESUME AFTER REFINEMENT PASS
  Refinement found splits → consecutive_empty_batches reset to 0.
  Scan must continue to verify stability of the expanded taxonomy.
  The refinement_pass_done flag stays True (refinement runs only once).
  Gate 3 must be re-satisfied: 7 more consecutive empty batches needed.
  Gate 2 does NOT need to be re-satisfied — it was already met before
  refinement triggered. The additional papers push total above 30%.
  Gate 4 stays True (refinement runs only once).
  Worst case: 60 (Gate 2) + 21 (post-refinement Gate 3) = 81 papers.
  If scan resumes and finds MORE new subtopics (from the freshly split
  taxonomy revealing finer patterns), consecutive_empty resets again.
  This is correct — it means the taxonomy is still evolving.

EC-P20: SYLLABUS WITH PRE-GROUPED ITEMS vs INDIVIDUALLY-LISTED ITEMS
  Some syllabi present items in groups:
    "Vocabulary: Synonyms, Antonyms, Spelling, OWS, Idioms"
  Others list items individually:
    "Synonyms/Homonyms, Antonyms, Spellings, Idioms & Phrases, OWS"

  For grouped syllabi: the GROUP NAME (e.g., "Vocabulary") is NOT a Topic.
    The ITEMS within the group are the Topics. Apply the Topic Integrity
    Test (S2-3 Step 1) to each item individually.
  For individually-listed syllabi: each item is already at Topic level.
    Apply the Topic Integrity Test to confirm.

  In BOTH cases, the result should be the same: each distinct question
  type = one Topic. The syllabus presentation format does not change
  the taxonomy structure.

EC-P21: DRIVE FOLDER CONTAINS NON-DOCX FILES
  Filter: only process files with mimeType =
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  Skip PDFs, images, Google Docs, folders. Log skipped files.
  Only .docx files count toward total_available for convergence gates.

EC-P22: DUPLICATE OR NEAR-DUPLICATE FILENAMES
  If two files have the same date + shift (ignoring trailing " 1", " 2"
  suffixes), they are duplicates. Process the LARGER file (more likely
  to have images). Skip the smaller. Log the skip.
  Both count as 1 paper for total_available (not 2).
  See deduplicate_files() in S3-2.

EC-P23: DRIVE FOLDER STRUCTURE VARIANTS
  The spec handles:
    a) Flat folder (all .docx directly inside) — collect all
    b) Year subfolders (2019/, 2020/, ...) — scan recursively
    c) Any nesting depth — walk full tree
  Year is extracted from FILENAME, not folder name. Folder names are
  used only for navigation, not year attribution.

EC-P24: FIGURAL QUESTION MISCLASSIFICATION DURING SCAN
  Scan-level classification of figural questions relies on text clues
  when images are unavailable via Drive read_file_content.
  If the stem says "Select the figure" with no further context, classify
  under Figure / Pattern Completion (default figural subtopic).
  PYQSort (Phase A) uses python-docx with full image access and will
  reclassify more accurately. Scan misclassification of figural questions
  is acceptable — it does not affect taxonomy structure (figural subtopics
  are created by Step 2a's syllabus-faithful derivation, not by scan discovery).

EC-P25: OMML-OBSCURED QUESTIONS DURING SCAN
  Drive read_file_content may strip OMML formulas, leaving blank stems.
  Classify using Q-position (section), option content analysis, and
  surrounding question context. Log "OMML-obscured" in question_format.
  Accuracy is lower (~70-80%) but acceptable for scan-level classification.
  PYQSort performs full OMML rendering for final classification.

EC-P26: PARTIAL BATCH ON CONTEXT LIMIT
  If context fills before completing BATCH_SIZE papers in a batch:
    1. The partial batch does NOT increment/reset consecutive_empty counter
    2. Save scan_progress.json + classifications.json with partial results
    3. Print session handoff message (see S3-7)
    4. New session resumes the incomplete batch — re-processes any papers
       from the partial batch that weren't fully classified

EC-P27: PHANTOM TRIPLE — NAME MISMATCH BETWEEN SORTED FILE AND ANALYSIS DOC
  A counted (section, topic, subtopic) triple does not exist in the Analysis
  doc taxonomy. Common causes:
    - Trailing/leading whitespace in sorted file heading (PYQSort bug)
    - Dash variant: em-dash (—) vs hyphen (-) vs en-dash (–)
    - Case difference: "DI" vs "di" vs "Di"
    - Punctuation: "Time & Work" vs "Time and Work"
  Task 2.5 (S5-4b) catches this with fuzzy matching to suggest the
  closest taxonomy triple. Resolution requires either re-sorting the
  affected papers or correcting the Analysis doc. Phase B cannot
  auto-fix because the correct name is ambiguous.

EC-P28: ORPHAN QUESTION IN SORTED FILE
  A question appears in a sorted PYQ file before any Subject or Subtopic
  heading. This means PYQSort emitted a question without taxonomy context.
  This is a PYQSort bug, not a Phase B issue. Phase B logs the orphan
  (file + Q number + reason) and HARD STOPs. Resolution: re-sort the
  affected paper in Step 3.

EC-P29: NON-SORTED FILE IN DRIVE FOLDER
  Drive folder contains .docx files that are NOT sorted PYQ outputs (e.g.,
  original Row files, the Analysis doc, exam_config docs, or other documents).
  S5-1 filters by sorted filename pattern (*_Sorted_Q*-Q*.docx).
  Non-matching .docx files are skipped with a warning log.
  If ALL .docx files are non-matching → error: "No sorted files found."

EC-P30: DUPLICATE SORTED FILE IN DRIVE FOLDER
  Drive folder contains two sorted files for the same date+session (e.g.,
  paper was re-sorted after a correction and both copies remain).
  S5-1 dedup logic keeps the larger file. The smaller is skipped with a
  warning. If sizes are equal, keep alphabetically-first filename.
  User should clean up duplicates from Drive after Phase B completes.
```

---

## §10 — DELIVERABLE SET CONTRACT

### S10-1 — Closed deliverable set (per mode)

```
═══════════════════════════════════════════════════════════════════════
DELIVERABLE SET CONTRACT — EXHAUSTIVE AND CLOSED
═══════════════════════════════════════════════════════════════════════

Each mode delivers EXACTLY the files listed below and NOTHING ELSE.
This is an exhaustive, closed list — not a minimum. Creating or
delivering any file not on this list is a spec violation with the
same force as an anti-editorializing violation.

LIVE FAILURE (SSC CGL Tier 2, July 2026):
  Claude delivered an unauthorized taxonomy_draft_v2.json alongside
  the spec-defined scan outputs. The file was redundant (taxonomy
  lives inside scan_progress.json per v1.7 D2) and unauthorized
  (not in the output contract). Root cause: no "NOTHING ELSE"
  qualifier, no DO-NOT-DELIVER list, no pre-delivery checklist.

────────────────────────────────────────────────────────────────────
MODE: --taxonomy (Step 2a: PYQDraft)
────────────────────────────────────────────────────────────────────
DELIVER (both mandatory, single present_files call):
  1. [ExamCode]_taxonomy_draft.json
  2. [ExamCode]_exam_config.json

DO NOT DELIVER:
  ✗ Exam Syllabus source files (these are INPUTS, not outputs)
  ✗ Exam Pattern source files (these are INPUTS, not outputs)
  ✗ Any intermediate parsing or extraction files
  ✗ Any renamed or versioned variants of the above 2 files

DESTINATION: User downloads → uploads to [ExamCode] project knowledge.

────────────────────────────────────────────────────────────────────
MODE: --scan (Step 2b: PYQScan)
────────────────────────────────────────────────────────────────────
DELIVER (both mandatory, single present_files call after each batch
         AND at scan completion):
  1. [ExamCode]_scan_progress.json
  2. [ExamCode]_classifications.json

DO NOT DELIVER:
  ✗ [ExamCode]_taxonomy_draft.json (INPUT — already in project)
  ✗ [ExamCode]_taxonomy_draft_v2.json or any versioned taxonomy file
     (the evolved taxonomy lives INSIDE scan_progress.json['taxonomy']
      per v1.7 D2 — a standalone copy is redundant and unauthorized)
  ✗ [ExamCode]_exam_config.json (INPUT — already in project)
  ✗ Any per-batch intermediate files
  ✗ Any summary, analysis, or report files not listed above
  ✗ Any file with "taxonomy" in its name (taxonomy is INSIDE
     scan_progress.json, never a separate deliverable in --scan mode)

DESTINATION: User downloads → uploads to [ExamCode] project knowledge.
             Replaces prior versions on each batch delivery.

NOTE: scan_progress.json MUST contain the COMPLETE evolved taxonomy
in its ['taxonomy'] field (v1.7 D2). This is the ONLY place the
scan-discovered taxonomy is stored. If Claude needs to work with
the taxonomy internally, it reads from scan_progress.json — it
does NOT create a separate file.

────────────────────────────────────────────────────────────────────
MODE: --approve (Step 2c: PYQApprove)
────────────────────────────────────────────────────────────────────
DELIVER (both mandatory, single present_files call):
  1. [ExamCode]_PYQ_Analysis.docx  (single merged doc, all subjects)
  2. [ExamCode]_exam_config.json   (may be updated with OTS boundaries)

DO NOT DELIVER:
  ✗ [ExamCode]_scan_progress.json (INPUT — consumed, not forwarded)
  ✗ [ExamCode]_classifications.json (INPUT — consumed, not forwarded)
  ✗ [ExamCode]_taxonomy_draft.json (INPUT — consumed, not forwarded)
  ✗ Per-subject Analysis docs (merged format replaced per-file in v2.6)
  ✗ Any intermediate generation files

DESTINATION: User downloads → uploads to [ExamCode] project knowledge.
             Taxonomy is LOCKED after upload — no further changes.

────────────────────────────────────────────────────────────────────
MODE: --counts (Step 4: PYQCount)
────────────────────────────────────────────────────────────────────
DELIVER (single file, single present_files call at completion):
  1. [ExamCode]_PYQ_Analysis.docx  (UPDATED with PYQ counts)

DO NOT DELIVER:
  ✗ [ExamCode]_count_progress.json (internal session persistence —
     saved to /home/claude for resume, never delivered to user)
  ✗ Any intermediate counting files or scripts
  ✗ count_pipeline.py or count_finalize.py (execution scripts)

INTERIM SESSION DELIVERY (session handoff only):
  When context limit forces session break during counting:
    Deliver [ExamCode]_count_progress.json via present_files
    for the user to upload to project knowledge for resume.
    This is a SESSION PERSISTENCE deliverable, not a final output.
    It is NOT delivered at completion — only at session breaks.

DESTINATION: User downloads → replaces prior Analysis doc in
             [ExamCode] project knowledge.
═══════════════════════════════════════════════════════════════════════
```

### S10-2 — Pre-delivery checklist (MANDATORY before every present_files call)

```python
import os

# ── MODE-SPECIFIC EXPECTED SET ──────────────────────────────
# Set `expected` based on current mode before running checks.

# --taxonomy mode:
expected_taxonomy = {
    f'{exam_code}_taxonomy_draft.json',
    f'{exam_code}_exam_config.json'
}

# --scan mode:
expected_scan = {
    f'{exam_code}_scan_progress.json',
    f'{exam_code}_classifications.json'
}

# --approve mode:
expected_approve = {
    f'{exam_code}_PYQ_Analysis.docx',
    f'{exam_code}_exam_config.json'
}

# --counts mode (completion):
expected_counts = {
    f'{exam_code}_PYQ_Analysis.docx'
}

# --counts mode (session break):
expected_counts_interim = {
    f'{exam_code}_count_progress.json'
}

# ── UNIVERSAL CHECKS ───────────────────────────────────────
expected = expected_scan  # ← set to current mode's expected set

# NOTE: Checks validate the present_files ARGUMENT LIST, not the
# full outputs directory (which may contain files from prior modes).

# files_for_present: the list of paths about to be passed to present_files
delivering = set(os.path.basename(f) for f in files_for_present)

# Check 1: All expected files present in the delivery list
missing = expected - delivering
assert not missing, f"MISSING deliverables: {missing}"

# Check 2: No unexpected files in the delivery list (CLOSED SET)
extra = delivering - expected
assert not extra, f"UNAUTHORIZED files in present_files call: {extra}. " \
                  f"Remove before calling present_files."

# Check 3: No internal/intermediate files leaked into the delivery
banned_patterns = [
    'taxonomy_draft_v2', 'taxonomy_draft_v3',  # versioned taxonomy
    'taxonomy_evolved', 'taxonomy_updated',     # renamed taxonomy
    'batch_', 'temp_', 'intermediate_',         # working files
    'pipeline', 'script',                       # execution scripts
]
leaked = [f for f in delivering
          if any(p in f.lower() for p in banned_patterns)]
assert not leaked, f"INTERNAL files leaked to delivery: {leaked}"

# Check 4: For --scan mode, verify taxonomy is INSIDE scan_progress
if mode == 'scan':
    import json
    sp_path = f'/mnt/user-data/outputs/{exam_code}_scan_progress.json'
    with open(sp_path) as f:
        sp = json.load(f)
    assert 'taxonomy' in sp, \
        "scan_progress.json missing ['taxonomy'] field (v1.7 D2)"
    assert isinstance(sp['taxonomy'], dict) and len(sp['taxonomy']) > 0, \
        "scan_progress.json['taxonomy'] is empty — must be COMPLETE"

print("Pre-delivery checklist: ALL PASS")
# Only after all checks pass → call present_files
```

### S10-3 — Delivery destinations (quick reference)

```
--taxonomy : User downloads → uploads to [ExamCode] project knowledge
             Next: PYQScan
--scan     : User downloads → uploads to [ExamCode] project knowledge
             (replaces prior version on each batch)
             Next: continue scanning OR PYQApprove
--approve  : User downloads → uploads to [ExamCode] project Files section
             Next: PYQSort (one Row file at a time, same project)
--counts   : User downloads → uploads to [ExamCode] project Files section
             (replaces the no-counts version)
             Next: Step 5 (PYQExtract) + Step 6 (MockBlueprint)
```

### S10-4 — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat delivery report or handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Upload / Replace / Use locally), and next-step reference.
```

---

## §11 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL IN THIS SPEC (identical every exam):
  Trigger parsing and mode detection
  Topic Integrity Test (3 questions — S2-3 Step 1)
  Per-entry decision tree for subtopic derivation (S2-3 Step 2: Q1/Q2/Q3)
  Unique Domain Property enforcement (no overlapping concept claims)
  6 Pattern Dimensions as optional tool for undivided blocks (S2-3 Appendix)
  Ratio-based guardrail (flag 2.0×, hard-stop 3.0×) and near-duplicate check
  Smart scan algorithm with 4-gate convergence
  Anti-editorializing rules (chat + JSON)
  Batch integrity rule (partial batches don't count)
  Session management protocol (S3-7)
  Drive reading method with OMML/figural fallback
  New discovery validation (3-question gate)
  Subtopic Refinement Pass (§3-6) with per-subtopic execution model
  Round-robin year sampling (newest-first, date-asc within year)
  Classification storage (separate file for large corpora)
  Analysis doc format (.docx with tables)
  Heading format contract (§6)
  Name consistency contract (§7)
  Universal classification rules 1-7 (§8)
  All 30 edge cases (§9)
  Progress JSON schemas (schema_version 2.0)
  Batch processing model (3/batch scan, 5/batch counts)
  Task 1 pre-count confirmation gate (S5-1a)
  Task 2 post-count accuracy gate (S5-4a)
  Task 2.5 taxonomy name cross-check (S5-4b)
  Task 3 doc-writing arithmetic verification (S5-5)
  Phase B execution model — Python script (S5-8)


EXAM-DISCOVERED (zero hardcoding):
  Section names, topic names, subtopic names → from syllabus + PYQ + refinement
  OTS section count, Q count per section, Q ranges → from exam pattern xlsx / doc
  Subject order → from exam pattern
  marker_mode → from PYQ structure detection
  Medium, question types, level → from exam pattern xlsx Overview tab
  Marking scheme (per-range type, marks, penalty) → from exam pattern xlsx Range tab
  Max attempt per section → from exam pattern xlsx Sections tab
  Classification precedents → from PYQ content discovery
  Refinement splits → from classified question pattern metadata

PROOF (validated against 13 exams — all produce ratio ≤ 2.6×):
  SSC CGL Tier 1:        ~30 entries → ~30 subtopics  (1.0×, short labels)
  SSC CGL Tier 2:        ~35 entries → ~35 subtopics  (1.0×, short labels)
  CAT:                   ~25 entries → ~25 subtopics  (1.0×, short labels)
  MPPSC Botany:           81 entries →  81 subtopics  (1.0×, lettered descriptors)
  CSIR NET Life Sci:    ~120 entries → ~120 subtopics (1.0×, lettered descriptors)
  GATE Biotech:          ~35 entries →  ~35 subtopics (1.0×, colon-headed topics)
  GATE CS:                10 sections → ~20 subtopics (2.0×, undivided blocks)
  IIT JAM Physics:         7 sections → ~14 subtopics (2.0×, undivided blocks)
  UGC NET History:       ~40 paras   →  ~40 subtopics (1.0×, named paragraphs)
  CUET PG Mathematics:     7 headers →   ~9 subtopics (1.3×, umbrella label split)
  CUET UG Political Sci:  16 chapters →  16 subtopics (1.0×, textbook chapters)
  NEET (3 subjects):     ~50 units   →  ~70 subtopics (1.4×, units with bullets)
  CTET Paper 1:          ~12 sub-sec →  ~31 subtopics (2.6×, content labels)
  Same spec handles all — zero exam-specific code.
```

---

## §12 — DEFINITION OF DONE

```
Phase 0a:
  ☐ Syllabus fully extracted (all subjects, all items)
  ☐ Exam pattern fully extracted — xlsx (preferred) or legacy format
  ☐ If xlsx: 3 tabs parsed (Overview, Sections, Range)
  ☐ If xlsx: all 10 structural validations passed (V1-V10):
    ☐ V1: Σ(Total Question) == Total Questions
    ☐ V2: Q_Ends − Q_Starts + 1 == Total Question (per section)
    ☐ V3: Section Q-ranges contiguous, non-overlapping
    ☐ V4: Range tab tiles Q.1 through Total Questions completely
    ☐ V5: All Negative Marks ≤ 0
    ☐ V6: Σ(Max Attempt × correct_marks) == Total Marks
    ☐ V7: 0 < Max Attempt ≤ Total Question (per section)
    ☐ V8: Overview Question Type set == Range tab distinct types
    ☐ V9: All Correct Marks > 0
    ☐ V10: Total Questions > 0, Duration > 0
  ☐ New fields populated: medium, question_types, level, marking_scheme[], max_attempt
  ☐ Section ≠ Subject principle applied (section names = OTS labels, not taxonomy)
  ☐ Topic Integrity Test applied — each distinct question type = one Topic
  ☐ Per-entry decision tree (Q1/Q2/Q3) applied to every syllabus entry
  ☐ Exclusion rules applied (vocabulary lists, scope markers, format qualifiers)
  ☐ Unique Domain Property verified — no two subtopics claim overlapping concepts
  ☐ Ratio guardrail passed: total_subtopics / syllabus_entries ≤ 3.0×
  ☐ Near-duplicate check passed: no pair with >75% name similarity
  ☐ Coverage check passed: every syllabus concept maps to exactly 1 subtopic
  ☐ Catch-all name check passed: zero Topics/Subtopics match banned patterns
  ☐ 1:1 Topic=Subtopic check passed: no Topic has a single subtopic with the
    same name UNLESS the syllabus genuinely lists it as a single atomic concept
  ☐ taxonomy_draft.json generated with correct structure
  ☐ exam_config.json generated with correct metadata (v2.5 schema)
  ☐ Both files delivered via present_files
  ☐ Deliverable set closed: EXACTLY 2 files delivered (S10-1 --taxonomy)
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call

Phase 0b:
  ☐ PRE-SCAN GATE: Year-wise paper inventory displayed with per-paper Q counts
  ☐ PRE-SCAN GATE: User confirmation received before scanning begins
  ☐ Round-robin year sampling applied (newest-first, date-asc within year)
  ☐ Drive file inventory cached in scan_progress.json (no re-listing on resume)
  ☐ File deduplication applied (EC-P22)
  ☐ Drive reading method used with OMML/figural fallback (S3-2)
  ☐ Pattern metadata (RULE 7) recorded for every classification
  ☐ Per-question classifications stored in [ExamCode]_classifications.json
  ☐ New discovery validation (3-question gate) applied before taxonomy changes
  ☐ Post-paper Q-count validation logged (informational)
  ☐ All new subtopics added to taxonomy (in scan_progress.json — FULL, not delta)
  ☐ 4-gate convergence enforced:
    ☐ Gate 0: small corpus (≤20 papers) → all papers scanned
    ☐ Gate 1: all available years covered
    ☐ Gate 2: ≥30% of total papers scanned (PROSE MANDATE enforced)
    ☐ Gate 3: ≥7 consecutive empty batches (after gates 0-2 pass)
    ☐ Gate 4: refinement pass completed
  ☐ Anti-editorializing enforced (no banned phrases in chat, no banned fields in JSON)
  ☐ Batch integrity enforced (partial batches don't affect counter)
  ☐ Subtopic Refinement Pass (§3-6) executed with per-subtopic model
  ☐ Orphan classification check passed after refinement
  ☐ Session management protocol followed (4-5 batches/session target)
  ☐ scan_progress.json saved after each batch (schema_version 2.0)
  ☐ classifications.json saved after each batch (separate file)
  ☐ Batch Stop Law enforced (S3-4a): each batch = one response;
    next batch starts ONLY after user's continue trigger;
    auto-advance is permanently banned including small corpora
  ☐ Batch-end message includes per-section Q-count distribution
  ☐ Batch-end message includes classification quality (normal/OMML/figural)
  ☐ Post-convergence summary displayed before "Run: PYQApprove"
  ☐ Resume sessions re-list Drive files and re-run S3-2a pre-scan gate
  ☐ Deliverable set closed: EXACTLY 2 files per batch (S10-1 --scan)
  ☐ Taxonomy stored INSIDE scan_progress.json (no separate taxonomy file)
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call

Phase 0c:
  ☐ Single merged Analysis .docx generated with all subjects (page-break separated)
  ☐ All topics and subtopics present in doc
  ☐ PYQ Count columns show "—" (not filled)
  ☐ Format matches IFAS reference (tables, headings, footer)
  ☐ All names .strip()-ed (no trailing whitespace)
  ☐ exam_config.json included in delivery
  ☐ Approval gate message printed with benchmark count
  ☐ Deliverable set closed: EXACTLY 2 files delivered (S10-1 --approve)
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call

Phase B:
  ☐ TASK 1: Year-wise paper inventory displayed with per-paper Q counts
  ☐ TASK 1: Q-counting uses same pattern as count_sorted_file (r'^Q\.?\s*\d+')
  ☐ TASK 1: Per-file Q counts stored in task1_per_file for Task 2 diagnostic
  ☐ TASK 1: User confirmation received before counting begins
  ☐ Sorted file filtering applied (*_Sorted_*.docx pattern)
  ☐ Duplicate sorted file detection applied (same date+session dedup)
  ☐ Multi-date files excluded from dedup
  ☐ Non-sorted files skipped with warning log
  ☐ All sorted PYQ files from Drive processed (5 per batch max)
  ☐ Heading parser matches Step 5's parse_taxonomy_level() exactly
  ☐ Child pointer reset on new parent heading (cur_sub reset on new Topic)
  ☐ Year extracted from each filename
  ☐ Counts aggregated correctly (per subtopic, per year)
  ☐ Per-file attributed counts tracked for Task 2 diagnostic
  ☐ Orphan questions tracked per file (zero orphans required)
  ☐ TASK 2: Full Subject > Topic > Subtopic breakdown displayed
  ☐ TASK 2: Grand total == Task 1 confirmed total (zero tolerance)
  ☐ TASK 2: Per-file diagnostic available on failure
  ☐ TASK 2.5: Taxonomy extracted from the Analysis doc using parse_taxonomy_level rules
  ☐ TASK 2.5: Every counted triple exists in the Analysis doc taxonomy
  ☐ TASK 2.5: Phantom triples = 0 (hard stop if any found)
  ☐ TASK 2.5: Uncounted subtopics listed (informational)
  ☐ TASK 3: Subtopic cells filled with exact verified counts
  ☐ TASK 3: Zero-count subtopics written as "0" (no "—" remains)
  ☐ TASK 3: Per-topic TOTAL rows == sum of subtopic cells
  ☐ TASK 3: Master summary topic PYQs == topic TOTAL rows
  ☐ TASK 3: GRAND TOTAL == sum of all topic totals
  ☐ TASK 3: Header total == GRAND TOTAL
  ☐ TASK 3: Cross-check: header == grand == sum(topics) == sum(subtopics)
  ☐ TASK 3: Sum of all section header totals == Task 1 confirmed total
  ☐ TASK 4: Batch size = 5 papers per batch (BATCH_SIZE_COUNTS = 5)
  ☐ Execution model: Python script (count_pipeline.py / count_finalize.py)
  ☐ Session management: count_progress.json saved with files_processed_list
  ☐ Updated Analysis doc delivered via present_files
  ☐ Deliverable set closed: EXACTLY 1 file at completion (S10-1 --counts)
  ☐ count_progress.json NOT delivered at completion (internal)
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call
```

---

# END OF Framework_PYQAnalyse v2.16
