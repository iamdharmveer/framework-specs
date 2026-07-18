# Framework_MockTestCreateAudit v2.7.6
#
# v2.7.6 — 2026-07-18 — §6.4 PREVENTIVE FIX for A-INTEGRITY-FALSEPOS-01 (docs-only, zero
#   logic change). Added regression test 7 (HEADER-TOKEN-FALSE-POSITIVE) to §21's
#   REGRESSION TESTS list, documenting the exact fixture that would have caught the P0.5
#   false-positive defect (fixed at v2.7.5) before it reached a live exam session: a
#   real, well-formed section_rules.md built from Step 5's actual write_section_rules()
#   output MUST NOT trigger HARD STOP (P0.5 / A-INTEGRITY). Cross-references
#   validate_framework_md.py Check T (added same day), which now runs this class of
#   check automatically in batch mode. No code, gate, or self-test-count change; the
#   embedded audit.py self-test remains 47/47 PASS (this test lives at the P0.5
#   pre-flight layer, which is Claude-executed pseudocode, not part of the runnable
#   script — same precedent as regression tests 1-6).
#
# v2.7.5 — 2026-07-18 — FIX A-INTEGRITY-FALSEPOS-01: P0.5's section_rules.md integrity
#   check searched for the literal string "CATEGORY-C" (re.search(r'CATEGORY[\s\-]*C', ...))
#   as evidence the file was intact. "CATEGORY C" has only ever been an internal
#   documentation alias in Framework_MockTestAnalyse.md's prose/comments (§14) for the
#   file-level header block -- write_section_rules() has never written that literal string
#   to disk. The only literal token it ever writes is '=== EXAM_STRUCTURE ===' (since the
#   header's introduction at Step 5 v2.3). Net effect: P0.5 HARD-STOPPED on every valid
#   section_rules.md ever generated, for every exam, 100% reproducible, on every framework
#   build >= v2.6 (2026-07-08, when P0.5 was introduced) -- confirmed 100% Step 8 blocker,
#   first surfaced on MPSC_Botany M1 (2026-07-18). Fix: corrected the regex to
#   r'===\s*EXAM_STRUCTURE\s*===' (the actual producer-emitted token), matching how every
#   other consumer of this file (cat_c(), Steps 7/9/10/11) already reads it. True-positive
#   truncation detection is unaffected: the header is the first block write_section_rules()
#   emits, so a file truncated early enough to lose it still fails len(rt)<200 or the token
#   check; a file predating the header's v2.3 introduction still correctly fails (desired).
#   Updated the two matching prose references (S5-2 gate catalogue row, §17 edge-case
#   playbook row) for consistency. No data, no other exam project, no other step, and no
#   other file required any change (confirmed by exhaustive grep: this literal-CATEGORY
#   regex search existed in exactly one location in the entire 14-file spec repo). No
#   relaxation of the P0.5 HARD STOP / MANDATE B / MANDATE D policy.
#
# v2.7.4 — 2026-07-17 — FIX C PROPAGATION (byte-identical from Step 5 v2.24.6). The S6-1b
#   AXIS CLASSIFIER v1.0 (COPIED VERBATIM from Step 5) had the same naive substring DI
#   detection as Step 5's pre-fix classify_axis1 ('|' in stem or 'table' in stem.lower()),
#   which false-positived on any word merely CONTAINING "table" ("vegetable", "acceptable",
#   "notable", ...). Replaced with the SAME structural/word-boundary _looks_like_table_
#   stimulus() helper Step 5 v2.24.6 now uses (>=2 pipe-delimited rows, OR a word-boundary
#   table-keyword match co-occurring with >=1 pipe-delimited row). Required by this file's
#   own contract: "if Step 5's classifier changes, this copy MUST be updated to match."
#   No other change — MATCH detection (S6-1b's other rules) and the self-contained
#   A-MATCH-TABLE mirror detector (§ standalone audit.py block) are untouched (they don't
#   duplicate the table/DI check). Verified: dynamic embedded self-test SELF-TEST: 47/47
#   PASS unchanged; validate_framework_md.py 0 issues.
#
# v2.7.3 — 2026-07-15 — C3: paper_id PROPAGATION (Step 8; additive, mock output bit-identical).
#   Derives paper_id/paper_slug from the blueprint (Blueprint v1.29 C1; fallback "MOCK:M{N:02d}");
#   input/output docx use paper_slug ("Mock[N]" for a mock — unchanged); the S2-2 guard checks
#   papers_completed[-1]==paper_id; the question_index re-sync keys on paper_id and tags it.
#   Engine untouched. Proven by blueprint_c3_propagate_test.py. Pairs with MockCreate v5.21.
#
# [ExamCode] project | Step 8 (MockCreateAudit) | Universal Mock Test Auditor & Rectifier
# ════════════════════════════════════════════════════════════════════════
#
# VERSION HISTORY:
#   v2.7.2 — 2026-07-12 — DELIVERABLE FILENAME RENAME (owner decision; docs-only, zero logic).
#           Rectified-paper output renamed [ExamCode]_Mock[N]_Complete.docx →
#           [ExamCode]_Mock[N]_Create_Complete.docx. Input renamed accordingly: reads the
#           Step-7 paper [ExamCode]_Mock[N]_Create.docx. The output is now a DISTINCT file
#           from the input (no longer an in-place same-filename replace); the input is
#           retained. registry re-sync, conditional audit_changelog.md, every A-* gate and
#           the COMPLETION GATE unchanged. Chain re-verified against Step 7 / Step 9.
#   v2.7.1 — LANGUAGE-AGNOSTIC MATCH DETECTION + A-MATCH-TABLE gate. (1) Ported the SHARED
#           AXIS CLASSIFIER v1.0 update from Step 5 (Analyse v2.24.2) BYTE-IDENTICAL: new
#           _opts_are_match_pairs()/_label_family + a third MATCH trigger, so non-English
#           matches and matches whose List body sits in a table are re-tagged MATCH (were
#           silently DIRECT). Verified: dedented logic identical + 220/220 behavioural parity
#           with Step 5's copy. (2) NEW executable gate gate_match_table() → A-MATCH-TABLE:
#           promotes the S7-3 manual 'match must be a real grid' checklist to a machine gate —
#           any re-derived MATCH question with 0 <w:tbl> FAILs (rebuild the List body as a real
#           table). 2 new self-test fixtures (A-MATCH-TABLE-catch + -pass); self-test N 45→47
#           (>= AUTH_GATE_FLOOR 35). Exam-agnostic; no hardcoded exam/section label.
#   v2.7 — 2026-07-09 — A-HEADER INVERTED (strip pre-Q.1 block, not validate figures).
#           Pairs with Step 7 v5.18 (R8b / G-PREQ1). The generated paper is questions-only:
#           the first non-blank body paragraph MUST be Q.1. Previously A-HEADER only
#           VALIDATED a title/instruction block IF present (absence was "informational, not
#           a defect") and CP-HEADER merely corrected its figures — so a title/info/scoring
#           cover synthesised upstream survived the audit untouched (the gap the SSC CGL T1
#           Mock 1 report exposed).
#           (1) gate_header() inverted: any non-blank paragraph before Q.1 → A-HEADER FAIL
#               (was _warn/_ok). Fix path renamed CP-HEADER → CP-HEADER-STRIP (delete the
#               block; content-preserving). Dormant only if section_rules EXAM_STRUCTURE
#               declares paper_header_block (no current exam declares it).
#           (2) src-loader reads paper_header_block from CATEGORY-C (default off).
#           (3) S2-2 mock-number resolution trimmed to TWO sources (trigger + filename);
#               the title block is no longer read (it no longer exists).
#           (4) P5, the A-HEADER catalogue row, the gate-origin map, and the S8-1 fix-class
#               list rewritten to strip semantics. 2 new self-test fixtures (A-HEADER-catch
#               + A-HEADER-dormant): self-test count 43 → 45 (N >= AUTH_GATE_FLOOR 35). No
#               other gate changed.
#
#   v2.6 — 2026-07-08 — CLOSE THE FALSE-CLEAN CHAIN (Phase 2 now MECHANICALLY enforced).
#           ROOT CAUSE (surfaced in a real Step-8 run, SSC_CGL_TIER1 Mock 1, where the
#           auditor shipped a self-declared "CLEAN" paper after COLLAPSING Phase 2 into a
#           single spot-check pass): Part A (machine gates), MANDATE A (script self-test) and
#           MANDATE D (delivery timing) are RUNNABLE and HARD-STOP, but Part B (§6), §7,
#           B-FACT, and the whole §12-2/§18 certification gate were PROSE the model
#           self-attests. A run could therefore go Phase 1 → Phase 3 with a self-declared
#           "clean" and ship a paper whose per-question audit never ran. The one executable
#           artefact (audit.py) validated NONE of Phase 2. Compounded by three enablers:
#           (a) RA-15 FUSED exhaustiveness ("every question") with pacing ("pause between
#               batches") — an autonomous / "don't pause" preference dropped the per-question
#               audit along with the pause, because they were one rule;
#           (b) MANDATE A accepted a CONSTANT-PRINT self-test — the 13-gate minimum-viable
#               stub printed "SELF-TEST: 13/13 PASS" from a bare print() while its gate
#               bodies were hollow/truncated (and the pipeline runs THAT generated stub, not
#               this file's authoritative fixture-tested auditor — Appendix A had become
#               effectively unused);
#           (c) no input-corruption check — blueprint.json, registry.json and audit.py all
#               arrived TRUNCATED via the project-knowledge sync, and P0 hard-stops on MISSING
#               files, not truncated ones.
#           SEPARATION OF CONCERNS (important): the hollow-script defect (b) and the
#           skipped-Phase-2 defect are INDEPENDENT false-clean vectors. Even a perfect Part-A
#           auditor cannot detect a skipped Phase 2 — Phase 2 is semantic/visual/factual and
#           out of Part A's scope entirely. Both are closed here.
#           FIX A — MANDATE B (boxed, top-level): Phase 2 may NEVER be skipped, compressed
#                   into a single pass, or spot-checked — in ANY mode (interactive OR
#                   autonomous). See MANDATE B.
#           FIX B — RA-0 PRECEDENCE + RA-15 SPLIT (RA-15a EXHAUSTIVENESS / RA-15b PACING) +
#                   S4-3A AUTONOMOUS mode. Autonomy waives the inter-batch PAUSE ONLY, never
#                   the per-question review. No preference may reduce coverage or weaken the
#                   completion gate (RA-0).
#           FIX C — S5-1A COMPLETION GATE (the keystone): `--final --audit-state <path>`
#                   validates the §9-1 audit_state.ledger (C1–C7) AND the on-disk EVIDENCE
#                   artefacts each stamp references. Required by §12-2 and Phase-3 STEP 1;
#                   a bare --final (Part A only) NO LONGER certifies. Converts §12-2/§18 from
#                   self-attested prose into a command EXIT CODE. This single change makes a
#                   skipped Phase 2 fail LOUDLY (C1/C2) instead of shipping.
#           FIX D — P1 HARDENED: --self-test must be the FIXTURE-BASED authoritative self-test
#                   (builds docx fixtures, asserts each gate catches a planted defect AND
#                   passes a clean one), N >= AUTH_GATE_FLOOR (35). A constant-print stub that
#                   merely emits "N/N PASS" is REJECTED. MANDATE A wording tightened.
#           FIX E — P0.5 INPUT INTEGRITY (A-INTEGRITY): json.load / ast.parse every input;
#                   HARD STOP on corruption/truncation; sanctioned repair for audit.py ONLY
#                   (regenerate from the canonical template, must then pass the hardened
#                   self-test), logged; NEVER silently repair blueprint/registry DATA.
#           FIX F — EVIDENCE-BOUND STAMPS (§9-1 / §7 / S5-1A): every 'rendered-and-viewed'
#                   stamp NAMES a montage PNG on disk; every fact_source NAMES a saved
#                   search-result file; every 'recomputed' stamp NAMES a recompute-trace file.
#                   C5/C6 verify the FILES exist and are non-trivial — so a ledger cannot be
#                   fabricated without producing the evidence, i.e. without doing the work.
#                   This is what pushes the gate from "hard to fake" toward "cannot fake
#                   without performing the audit".
#           §16/§17/§18 wired; glossary + invariants + edge-cases updated. ABSENT-SAFE: a run
#           with a complete, evidence-backed ledger behaves exactly as v2.5 plus the extra
#           assertions; a legacy audit_state with no evidence dir fails C5/C6 LOUDLY (never
#           silently passes).
#           CROSS-FILE (apply IN LOCKSTEP — see §21): Framework_Blueprint.md §13-7A (the
#           Step-6 B3 generator — where the auditor is BORN, once per exam) and
#           Framework_MockTestCreate.md Appendix A MUST generate EXACTLY this v2.6 auditor
#           (--audit-state + C1–C7 + fixture self-test), or the fix never reaches the ~200
#           exams. validate_framework_md.py gains the 6 regression tests (§21). Step 10
#           (MockExplainAudit) and Step 9's §18 self-audit carry the SAME false-clean chain
#           and must get the parallel completion-gate pattern.
#
#   v2.5 — 2026-07-07 — THREE-AXIS FORMAT-DISTRIBUTION AUDIT (File 4 of the feature — closes the
#           loop; reads Step 6 v1.23 axis_schedule + the counts Step 7 v5.14 renders).
#           A mock must replicate the exam's FORMAT MIX. Step 8 INDEPENDENTLY re-tags every
#           shipped question with the Step-5 classifier and audits the realized per-window Axis
#           distribution against the blueprint target — the mirror of B-DIFF for format.
#
#           FIX A — SHARED AXIS CLASSIFIER v1.0, COPIED VERBATIM from Step 5 (§AXIS-CLASSIFIER).
#             classify_axis1/2/3 + tag_axes + _opts_are_combination_labels + AXIS2_CLASSES are
#             byte-identical to Step 5; the PYQ target and the generated distribution are only
#             comparable if classified by the SAME functions. Re-implementation is forbidden.
#
#           FIX B — PER-QUESTION RE-TAG (independent, from the docx — Step 8 has NO concept_map).
#             In S6-0 extraction every question is re-tagged from its rendered stem/options/
#             artefact-map; axis1/axis2/axis3/is_negative are stored on the §9 ledger entry.
#             is_negative uses the EXACT Step-5 EC-12 regex (uppercase NOT|INCORRECT|EXCEPT|
#             FALSE|WRONG, no re.I) so the target rate (Step 6) and realized rate (here) count
#             identically — a broader detector would inflate the rate and fire false WARNs.
#
#           FIX C — INDEPENDENT WINDOW TALLY in registry.axis2_audit (decision A). Because Step 8
#             audits one mock per run, the per-10-mock-window counts accumulate here (window-aware
#             reset), re-derived from each mock's docx — trusting nothing. Cross-checked against
#             Step 7's registry.axis2_window (a large drift ⇒ WARN: the paper's actual structure
#             diverged from the variant Step 7 declared). Preserved through §13 re-sync (setdefault).
#
#           FIX D — S6-6 FORMAT-DISTRIBUTION AUDIT (advisory, mirrors B-DIFF / S6-5, decision B):
#             B-AXIS2 (per-section, per-format, per-window: band = ±1 or ±15% whichever larger;
#             guarantee = ≥1/window; DIRECT floats), B-AXIS1 / B-AXIS3 (realized vs Step-6 target
#             within tolerance), B-AXIS-NEG (negative-rate soft WARN, decision 12). A shortfall is
#             a generation-quality FINDING in the report; it blocks SHIP only if section_rules/
#             blueprint marks the format mix hard (the RA-9 parallel). Fires only at WINDOW CLOSE
#             (N % batch_size_qs == 0 or N == total_mocks), from the FINAL fixed docx (Phase 3).
#
#           FIX E — dashboard + report lines; registry.axis2_audit in REQUIRED_TOP self-heal.
#             Everything is ABSENT-SAFE: a pre-v1.23 blueprint (no axis_schedule) ⇒ the whole
#             Axis audit is inert and Step 8 behaves exactly as v2.4. version → v2.5.
#
#   v2.4 — 2026-07-07 — FIGURAL IMAGE_ROLE-AWARE AUDIT (mirrors Step 7 v5.13).
#           ROOT CAUSE: Step 7 v5.13 added 3-way figural rendering (stem_and_options /
#           stem_only / options_only) with add_figural_stem_question() and expanded
#           G-FIGTEXT (3-tier) + G-FIGURAL-COMPOSITE (image_role-aware). Step 8 must
#           mirror these so the independent audit catches what Step 7 missed.
#
#           (1) A-FIGCOMP gate table entry updated: now image_role-aware with 3 branches
#               (stem_and_options: ≥n_opt+1 images; stem_only: ≥1 problem image, option-
#               image arm skipped; options_only: ≥n_opt images, no problem required).
#               Reads image_role from section_rules PYQ_IMAGE_ANALYSIS per subtopic.
#           (2) A-FIGCOMP code (gate_images): updated to read image_role and branch the
#               minimum-image check accordingly. Single-image composite warning now only
#               fires for stem_and_options (for stem_only, 1 image IS correct).
#           (3) Traceability mapping updated: A-FIGCOMP now traces to Step 7's S10-8A
#               (add_figural_stem_question) in addition to S10-8.
#           (4) G-FIGTEXT-PROSE tertiary check mirrored: any Q-block with 0 images +
#               figure-reference text → FAIL. Catches misclassified TEXT subtopics.
#           (5) §7 V-image note updated to cover stem_only verification.
#
#   v2.3 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added S14-6: post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3. F2 (step-complete) footer rendered
#           after the single present_files call and status report. Zero logic change.
#   v2.2 — 2026-07-06 — AUDIT SCRIPT SOURCE UPDATED (EC-A3).
#           Step 6 (MockBlueprint) v1.20+ now auto-generates [ExamCode]_mock_test_audit.py
#           as its 6th output file. Step 8 MANDATE A HARD STOP message, D4 design note,
#           P0 missing-file hint, P1 fallback reference, §17 edge-case playbook row, and
#           Appendix A header updated to reference Step 6 auto-generation instead of
#           manual creation. MANDATE A remains MANDATORY — the script must still exist
#           in project Files for Step 8 to run; only the SOURCE has changed (auto-generated
#           by Step 6, not manually created by user). Appendix A script code UNCHANGED.
#           No audit logic, gate, or self-test change.
#
#   v2.1 — 2026-07-06 — EXAM_CONFIG V2.5 CONTRACT SYNC (new blueprint fields).
#           Step 6 v1.19 now carries marking_scheme[], level, medium in blueprint.json.
#           Step 8 reads these at P2 for availability. No new audit gates — these fields
#           are structural metadata consumed by Steps 7/9/11, not auditable mock content.
#           sections[] comment updated to include max_attempt.
#           CATEGORY C now also reads marking_scheme, level, medium via cat_c() for
#           header validation (P5) when the mock paper prints marks information.
#
#   v2.0 — 2026-07-04 — TITLE/FILENAME ALIGNMENT + CROSS-STEP SYNC VERIFICATION.
#           (1) TITLE/FILENAME MISMATCH: header, §1-1 spec reference, Appendix A header,
#               and footer all said "Framework_MockCreateAudit" but the filename is
#               Framework_MockTestCreateAudit.md (missing "Test"). FIXED: all 4 now match
#               the filename. The step name "MockCreateAudit" and trigger format are
#               UNCHANGED (they are the step's canonical name, not the filename).
#           (2) Changelog generator and session_log audit_version stamps bumped to v2.0.
#           (3) CROSS-STEP SYNC VERIFIED against current versions: Step 7 v5.8 (delivery
#               contract, REQUIRED_TOP, options_by_q/section_names field names), Step 9 v1.9
#               (input contract unchanged since v1.6 — v1.7/v1.8/v1.9 were documentation +
#               engine-code-only), Step 10 v1.5 (question_index frozen/read-only contract),
#               Step 11 v1.0 (question_index JOIN consumption). All contracts in sync.
#           (4) UPSTREAM NOTE (Step 7 v5.8): Step 7's REQUIRED_TOP is missing section_names,
#               options_by_q, rc_manifests, figural_manifests — fields Step 7 writes at S13
#               but doesn't self-heal. Step 8's REQUIRED_TOP already covers all four.
#               Flagged for the Step 7 audit pass (not a Step 8 bug).
#           No logic change; self-test stays 35/35.
#   v1.9 — 2026-07-04 — CROSS-STEP SYNC (Step 7 v5.8 alignment + 1 schema fix).
#           (1) CANONICAL STEP RENAMING: Step 7 v5.8 already updated all its
#               cross-references to use canonical numbering (Step 8/Step 9). This file's
#               body still used legacy "Step 2" / "STEP 2" / "STEP-2" (47× mixed-case)
#               for Step 7 and "Step 3" / "STEP 3" / "STEP-3" (61× mixed-case) for
#               Step 8 — creating a readability mismatch with the upstream spec. FIXED:
#               all 119 body references now use canonical Step 7/Step 8 (including
#               MANDATE A heading, RA-6 heading, STATUS REPORT title, gate glossary
#               STEP-8-ONLY label). Version history preserved unchanged.
#           (2) REQUIRED_TOP missing `section_names`: Step 7 v4.8 writes
#               reg['section_names'] (consumed by G-SECTIONHDR and documented as
#               "consumed by Step 8 A-SECHDR"). But Step 8's schema-heal REQUIRED_TOP
#               did not include it — a missing section_names would not be self-healed.
#               FIXED: added to REQUIRED_TOP (default []).
#           Cross-step contract verified against: Step 7 v5.8 (delivery contract,
#           REQUIRED_TOP, field names, section numbers S13-4/S13-6); Step 9 v1.6
#           (input contract, options_by_q consumption, question_index frozen status);
#           Step 11 (question_index JOIN consumption); Blueprint v1.14 (section 'name'
#           vs 'section_name' field handling). No logic change; self-test stays 35/35.
#   v1.8 — 2026-07-04 — DEEP-AUDIT (18 bugs fixed).
#           PASS 1 — step numbering + version stamps (13 fixes):
#           (1) PIPELINE POSITION downstream steps used legacy numbers (Step 4/5/6) and a
#               non-existent step name ("MockTestSort") — FIXED: Step 9 (MockExplain),
#               Step 10 (MockExplainAudit), Step 11 (MockDeliver); range corrected to 7–11.
#           (2) 13 references to "Step 4 (MockExplain)" / "Step-4 task/artefact" throughout
#               the spec body used legacy numbering — FIXED: all now Step 9/Step-9.
#           (3) Two references to an undefined "MANDATE-1" (inherited from Step 7's spec) — FIXED:
#               replaced with RA-15 (this spec's own equivalent rule).
#           (4) PURPOSE section "Step 3/4" → "Step 8/9" (2 occurrences).
#           (5) Appendix A script header said "Framework_MockCreateAudit v1.0" — FIXED: v1.8.
#           (6) Appendix A validation status said "(v1.2)" — FIXED: "(v1.8)"; test coverage
#               description now mentions v1.4 NAT cases + v1.5 SECHDR-name-catch.
#           (7) _find() docstring was invalid Python (adjacent string literals not
#               concatenated across physical lines) — FIXED: triple-quoted docstring.
#           PASS 2 — exam-agnostic rigidity (5 fixes):
#           (8) gate_optref DEAD CODE: `extra` read from section_rules escape tokens but
#               NEVER merged into the token list — the gate only ever checked hardcoded
#               English phrases ('no error', 'none of these', etc.). Also 'if there is no
#               error' was a separate hardcoded literal. FIXED: section_rules escape tokens
#               are merged as PRIMARY; escape_stem_triggers configurable via src.
#           (9) STIMULUS_CUES hardcoded English-only phrases ('the passage', 'the table',
#               'according to the passage', etc.) — non-English exams (Hindi, Tamil, etc.)
#               would never trigger stimulus detection. FIXED: gate_stimorphan now merges
#               section_rules stimulus_cue_patterns (if declared) with the built-in defaults.
#           (10) gate_header hardcoded `\bmock\b` regex — non-English exams using "मॉक" or
#                other title keywords would always WARN. FIXED: reads mock_title_keyword from
#                section_rules (default 'mock').
#           (11) gate_images HARDCODED figural stem keywords ('mirror','water image' etc.)
#                violating RA-9 — FIXED: reads figural_cue_keywords from section_rules.
#           (12) B-DIFF prose hardcoded "Simple/Medium/Hard" — FIXED: references
#                blueprint.difficulty_labels (the runtime source).
#           No logic change; self-test stays 35/35.
#   v1.7 — 2026-07-03 — DEEP-AUDIT (3 version-stamp fixes).
#           (1) Footer said "v1.1", header was v1.6 — never updated past v1.1.
#               FIXED: footer now v1.7.
#           (2) Change-log file header generator wrote "MockCreateAudit v1.1" into
#               every generated change-log. FIXED: v1.7.
#           (3) Registry session_log audit_version stamp was hardcoded "1.0" — every
#               audit session log entry falsely claimed v1.0 regardless of spec version.
#               FIXED: "1.7". No logic change; self-test stays 35/35.
#   v1.6 — 2026-07-02 — QUESTION METADATA INDEX — CERTIFIER LAYER (cross-step index extension,
#           Step-3 half). Additive, exam-agnostic, writes NOTHING to the docx. §13 re-sync now
#           rebuilds registry.question_index for mock N BY KEY (new step 2b): subtopic_id is taken
#           from Step 3's INDEPENDENT re-derivation (the §9 audit ledger; B-ALLOC content->id) —
#           never trusted from Step 2; a Step-2/re-derivation disagreement is logged as a labelling
#           defect and the re-derived id wins; a regenerated Q keeps its slot id so re-derivation
#           agrees by construction. difficulty is CARRIED FORWARD from Step 2's incoming index
#           (difficulty is not rendered in the paper and not re-derivable from it, §19; regeneration
#           preserves the target so the carried value stays correct). REQUIRED_TOP (schema-heal) now
#           includes question_index; S13-3 verification adds a check mirroring Step 2 G-QINDEX (one
#           mock-N object; q=1..total_questions sorted/unique/complete; ids ∈ blueprint; difficulty
#           ∈ difficulty_labels; distribution == schedule[N] exactly). §19 documents the two-tier
#           guarantee (subtopic_id independently re-derived + certified; difficulty authoritative-
#           by-assignment + distribution-verified). No new A-* docx gate — question_index is a
#           registry field, certified in the §13 re-sync path. Governed by
#           Contract_QuestionMetadataIndex v1.0; re-sync logic proven in the Phase-1 harness.
#   v1.5 — 2026-06-30 — A-SECHDR SECTION-NAME DETECTION (mutation-harness finding). The
#           mutation-testing harness found a hole: A-SECHDR pattern-matched only the literal
#           keywords "section"/"part"/rule-chars, so a stray heading that IS a declared
#           SECTION NAME ("Quantitative Aptitude", "Technical") in the body was NOT caught
#           (the realistic section-header form), and the scan only covered paragraphs inside
#           question blocks. FIX: gate_sechdr now (a) also flags a standalone body paragraph
#           equal to a declared section name (provenance-based — matched against
#           src['sections'], exam-agnostic), and (b) scans ALL body paragraphs (a heading
#           before Q.1 / between blocks is seen too). New self-test A-SECHDR-name-catch;
#           SELF-TEST 34 -> 35. Non-offending papers unaffected.
#   v1.4 — 2026-06-30 — NAT CONTRACT — AUDIT LAYER (cross-step NAT extension, Step 3
#           half). DORMANT behind the blueprint's nat_present flag; every NAT path is gated
#           so a non-NAT mock behaves exactly as v1.3.
#             (1) src re-derives the NAT axis INDEPENDENTLY: nat_present, nat_subtopic_ids,
#                 expected_nat_by_section (from blueprint allocations), nat config, and
#                 nat_instruction phrases; options_by_q is read from the registry (ND6
#                 delivery contract, NOT a self-audit sidecar).
#             (2) RA-12 GENERALISED with a NUMERICAL branch (supersedes cardinality): the
#                 re-derived VALUE must be uniquely determined, form-matched to nat_answer_type
#                 (integer⇒integral; real⇒within ca_range lo≤hi), 0/neg/fractional valid,
#                 non-leaking. B-SOLVE yields a VALUE (compared numerically within tolerance,
#                 ND13 — never string equality); B-UNIQUE checks unique determination;
#                 B-DISTRACT is N/A (no options); B-LEAK checks the numerical value.
#             (3) OPTION GATES (A-OPTN/A-OPTLABEL/A-OPTORDER/A-OPTUNIQUE) SKIP NAT questions
#                 (options_by_q==0); A-KBAL/A-KPAT exclude NAT (as they exclude multi).
#             (4) A-ANSKEY leak scan extended to NAT numerical keys ("Q.5 → 47" incl.
#                 0/negative/decimal — the option-digit patterns missed them).
#             (5) NEW catalogue gates: A-NAT-NOOPT (machine — a 0-option-marked Q renders
#                 zero options), A-NAT-INSTR (machine — per-section numerical-instruction
#                 count matches the blueprint), and A-NAT-ANSWER (Claude-derivation — value
#                 well-posed/form-matched/non-leaking; claude_side like A-KINT/A-MSQ-KEY).
#                 gate_nat() emits the two machine gates; both are dormant when nat_present is
#                 false. A-FIGCOMP gains a figural-NAT variant (ND10: problem image, ZERO
#                 option images); RA-16 admits NAT members in linked/DI groups (ND11).
#             (6) SELF-TEST extended with 6 NAT fixtures (A-NAT-NOOPT catch/pass/dormant,
#                 A-NAT-INSTR catch/pass/dormant): 28 → 34; the prose SELF-TEST count is
#                 bumped in lockstep (E-CONST). validate_framework_md.py: 0 issues, 34/34.
#   v1.3 — 2026-06-30 — VOCABULARY UNIFICATION — PHASE 0 (rename only; NAT prep). Pure
#           rename, no behaviour change: per-subtopic `answer_mode` -> `answer_cardinality`
#           (RA-12, B-*, ledger, gate logic, src); blueprint flag `msq_present` ->
#           `multi_present`. Blueprint reads accept the OLD names as a fallback. Non-MSQ
#           exams byte-identical to v1.2. Validated: validate_framework_md.py 0 issues,
#           SELF-TEST 28/28; the extracted auditor re-run GREEN on the MSQ e2e fixtures with
#           BOTH old-name and new-name blueprints (back- and forward-compat). First step of
#           the Steps 0-4 single-vocabulary alignment (answer_type + answer_cardinality).
#   v1.2 — 2026-06-30 — MSQ CONTRACT — AUDIT LAYER (cross-step MSQ extension, Step 3
#           half; mirrors Step 2 v4.5). DORMANT behind the blueprint's
#           multi_select_allowed / multi_present and each subtopic's answer_cardinality: for any
#           single-answer exam (the default, incl. SSC CGL) v1.2 audits identically to
#           v1.1. Step 3 remains the INDEPENDENT auditor — it does NOT trust any Step-2
#           self-report: it RE-DERIVES answer_cardinality per question from blueprint
#           subtopic_list (by subtopic_id), RE-DERIVES the correct SET by solving, and
#           reads MSQ config (total_options, msq_k_mode, msq_k, msq_allow_aota) from
#           section_rules / blueprint — never from the Step-2 answer_key sidecar (which
#           Step 3 never reads; RA-1).
#             (1) RA-12 GENERALISED to mirror Step 2 R-ANSWER (both modes): single →
#                 exactly one defensible option; multi → the correct SET S is a non-empty
#                 PROPER subset of {1..OPTIONS_COUNT} (1≤|S|≤n−1; |S|=msq_k when fixed),
#                 every in-set option defensible under EVERY fair reading and every
#                 out-set option indefensible under ANY fair reading; negation composes.
#             (2) B-SOLVE now yields a SET for multi questions (the re-derived S), not a
#                 scalar; B-UNIQUE becomes a SET-MATCH (re-derived S must equal the set the
#                 paper marks — but Step 3 has no marked key, so it verifies S is internally
#                 well-formed per RA-12 and that exactly the in-set options are defensible);
#                 B-DISTRACT checks the (OPTIONS_COUNT − |S|) OUT-set options are each
#                 indefensible (a borderline out-set option is the MSQ ambiguity defect).
#             (3) A-KINT extended: the re-derived key per question is a single int (single)
#                 OR a non-empty proper subset (multi). A-KBAL and A-KPAT now EXCLUDE
#                 multi-mode questions from the single-position balance/run statistics (a
#                 set has no single position; mirrors Step 2 K-BAL/K-PAT msq_positions).
#             (4) A-ANSKEY leak scan extended to set-valued keys ("Q.1 → 1,2,4") — the
#                 single-digit pattern missed comma/space lists (mirror Step 2 G-ANSWERKEY).
#             (5) NEW catalogue gates: A-MSQ-KEY (Claude-derivation check — the re-derived
#                 set is a well-formed non-empty proper subset, fixed-k honored, AOTA rule
#                 honored; added to the validator's claude_side alongside A-KINT/KBAL/KPAT)
#                 and A-MSQ-INSTR (machine docx scan — the select-instruction is present in
#                 the Q.<n> stem line; EMITTED by the embedded script). Both run MULTI-only.
#             (6) LEDGER schema mirrors set values: derived_answer → may be int|list;
#                 added answer_set_verified (bool) and answer_fact_values (list) so B-LEAK
#                 scans EVERY value in a multi answer set, not just one (P3-1).
#             (7) B-LEAK generalised: for a multi question every value in the re-derived
#                 set is checked for illegitimate appearance as an option elsewhere.
#             (8) B-DIFF mirrors Step 0 E-9: an MSQ adds a difficulty-load term (advisory).
#             (9) RECTIFICATION: re-balancing for A-KBAL/A-KPAT skips MSQ positions; when a
#                 multi question is regenerated, the WHOLE correct SET is preserved/re-formed
#                 (never "change which single option is correct"); A-MSQ-KEY/INSTR get their
#                 own rectification routes.
#            (10) SELF-TEST extended with MSQ fixtures (well-formed set, k=0, k=n, fixed-k
#                 violation, AOTA-under-multi, set-leak, instruction-in-stem); the prose
#                 SELF-TEST count is bumped in lockstep (E-CONST). validate_framework_md.py
#                 claude_side updated to include A-MSQ-KEY so C-GATE stays satisfied.
#           All MSQ behaviour is config-driven (multi_select_allowed / answer_cardinality /
#           msq_k_mode / msq_allow_aota) — zero exam names hardcoded. Validated: the
#           project validator returns 0 issues (gate-code + self-test-count consistency),
#           and the new audit logic was parity-checked in Python against the Step-2 MSQ
#           fixtures before encoding.
#   v1.1 — 2026-06-29 — Reporting upgrade (no logic change to the audit itself):
#           (a) a STATUS REPORT dashboard is printed in chat at delivery (§14-4) —
#               a scannable verdict + coverage + on-arrival→after-rectification
#               delta; (b) a per-question REGENERATION CHANGE-LOG is added to the
#               report (§R5) and, when any question was regenerated, a downloadable
#               author-only change-log artefact carrying the literal before/after
#               diff is delivered alongside the core set (§14); (c) the in-chat
#               fact-verification summary is made strictly content-free (counts +
#               that sources were logged — never the facts themselves), closing a
#               latent MANDATE-0 leak in the old §R8; (d) report adds a coverage
#               matrix (proves zero sampling) and a defects-by-class rollup (surfaces
#               systemic Step-2 issues). The closed-set discipline is preserved: the
#               core deliverable stays {docx, registry}; the change-log is an
#               explicitly-demarcated audit artefact shipped only when regenerations
#               occurred. See S8-5, §14-1..§14-5, §R0/§R5/§R8/§R14/§R15, DoD #12.
#   v1.0 — 2026-06-29 — Initial release. Independent audit + in-place
#           rectification of the Step-2 mock paper. Built exam-agnostic from
#           the ground up (zero hardcoded exam values — every count, format,
#           label, language, difficulty band, escape token and figural type is
#           read at runtime from blueprint.json / section_rules.md /
#           subtopic_manifest.json / registry.json). Re-verifies, independently,
#           every Step-2 generation contract (R1–R24, R-DELIVER, R-LINKED,
#           R-FIGURAL, R-UNDERLINE, R-OPTREF, R-UNIQUE, R-MATH-OMML and the 57
#           Step-2 gates) WITHOUT trusting the Step-2 self-audit sidecar, then
#           rectifies every defect in place and ships a 100%-verified, zero-
#           defect paper. Design decisions locked with the framework owner:
#             D1. Step 3 receives ONLY {Mock[N]_Create.docx, registry.json}
#                 (Step-2 closed delivery set, S13-6). The answer-key/concept_map
#                 sidecar is NEVER delivered, so Step 3 is fully INDEPENDENT:
#                 it solves every question itself to verify answer uniqueness and
#                 correctness. Definitive key-adjudication remains a Step-9 task.
#             D2. Rectify-in-place. Mechanical/rendering defects are fixed in the
#                 docx directly; any defect needing new content REGENERATES that
#                 one question in place under Step 2's own contracts, then re-
#                 audits it. Step 3 never hands a broken paper back to a human.
#             D3. The deliverable is the RECTIFIED docx + a registry RE-SYNCED
#                 from the fixed file (mock-N slice rebuilt). Not a verdict report.
#             D4. A universal, exam-agnostic mock_test_audit.py is auto-generated
#                 by Step 6 (MockBlueprint) v1.20+ as its 6th output file; it is
#                 MANDATORY for Step 8 (hard stop if absent), unlike Step 7 where
#                 it is optional. See Framework_Blueprint.md §13-7A.
#             D5. Every figure, image, table, matrix, chart and OMML expression
#                 is audited at pixel/cell/node depth — rendered-and-viewed or
#                 arithmetically recomputed — never pattern-matched (§7).
#             D6. Live web-verification of every current-affairs / static-GA fact
#                 and every factual option (never certified from memory).
#             D7. Batch rhythm mirrors Step 2: semantic review runs in batches of
#                 ≤ AUDIT_BATCH_SIZE (default 10) questions, each gated by an
#                 explicit "continue"; linked-stimulus groups are atomic; the
#                 final batch auto-runs certification + delivery (no "continue").
#
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take the .docx produced by Step 7 (MockCreate) and the registry.json it
#   shipped, INDEPENDENTLY AUDIT every Question / Option / Image / Table / Matrix
#   / Chart / OMML expression / Paragraph in the paper, RECTIFY every defect
#   found, and emit a 100%-verified, zero-defect paper plus a registry re-synced
#   from the fixed file. Step 8 is the last gate before learner-facing artefacts
#   (Step 9 Explain) are built on top of the paper; a defect that survives Step 8
#   reaches students. Therefore Step 8 assumes nothing about Step 7's correctness
#   and re-derives every fact it certifies.
#
# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION
# ════════════════════════════════════════════════════════════════════════
#   Step 5 (PYQExtract)   → [ExamCode]_section_rules.md
#                                 [ExamCode]_subtopic_manifest.json
#   Step 6 (MockBlueprint) → [ExamCode]_blueprint.json
#                                 [ExamCode]_registry.json (empty template)
#   Step 7 (MockCreate)    → [ExamCode]_Mock[N]_Create.docx
#                                 [ExamCode]_registry.json (updated, mock N appended)
#   THIS STEP (MockCreateAudit) → [ExamCode]_Mock[N]_Create_Complete.docx (RECTIFIED)
#                                      [ExamCode]_registry.json (re-synced from fixed file)
#   Step 9 (MockExplain)   → consumes the rectified paper; builds the key + solutions
#   Step 10 (MockExplainAudit)
#   Step 11 (MockDeliver)
#
#   Steps 7–11 all run in the [ExamCode] project (exam-specific).
#   Step 8 runs immediately after the Step-7 session that generated mock N,
#   BEFORE Step 7 is run for mock N+1 (so the audited mock is always the most
#   recently registered one — see §13 registry re-sync, which relies on this).
#
# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. It names no section, no
#   subtopic, no question count, no time/marks figure, no banned topic, no
#   sub-type code, no language, no figural type. Every such value is READ at
#   runtime:
#     • question/section counts, q_ranges, difficulty targets, format presence
#       → blueprint.json
#     • per-subtopic patterns, wrong_option_structure, fixed option sets,
#       difficulty calibration, OMML_required, option label format, language,
#       time/marks/negative-marking, figural object/transformation types,
#       passage word ranges, recycled-dataset bans
#       → section_rules.md (CATEGORY C header + CATEGORY A/B blocks)
#     • subtopic_id join key, mandatory-every-mock list, alternation groups
#       → subtopic_manifest.json
#     • cross-mock dedup corpus (hashes, stems, semantic tuples, content_tracking
#       L4–L18, rc/figural manifests)
#       → registry.json
#   The same spec audits SSC CGL Tier 1, SSC CGL Tier 2, GATE, NEET, IBPS PO,
#   UPSC CSAT, CAT, regional exams — any exam with valid Step 0/1/2 outputs.
#   If a check needs an exam-specific value that is absent from these files, the
#   check is SKIPPED with a logged reason — it is NEVER hardcoded into this spec.

# ════════════════════════════════════════════════════════════════════════
# §0 — INPUT / OUTPUT CONTRACT (read before anything else)
# ════════════════════════════════════════════════════════════════════════

## S0-1 — INPUTS (what Step 8 is given)

  DELIVERED BY STEP 7 (the closed set; user uploads both to the [ExamCode] project):
    1. [ExamCode]_Mock[N]_Create.docx   — the paper to audit (the audit surface)
    2. [ExamCode]_registry.json           — dedup/tracking corpus (mock N appended)

  ALREADY IN PROJECT KNOWLEDGE (from Steps 0/1; required):
    3. [ExamCode]_section_rules.md        — per-subtopic rules + CATEGORY-C exam params
    4. [ExamCode]_blueprint.json          — allocations, sections, difficulty schedule
    5. [ExamCode]_subtopic_manifest.json  — subtopic_id ↔ name + mandate/alternation data
    6. [ExamCode]_mock_test_audit.py      — Part-A machine-gate script (MANDATORY — MANDATE A)

  NOT DELIVERED (Step 8 must do without these — by design, S13-6):
    ✗ [ExamCode]_M[N]_answer_key.json     — the answers + per-Q concept_map.
       CONSEQUENCE: Step 8 has NO answer key and NO concept_map. It re-derives
       both independently (§11 answer derivation; §9 audit ledger). Gates that
       Step 7 ran by reading the sidecar (G-CONCEPTDUP, G-ALLOC-SUBTOPIC,
       G-COUNT-X-UNIQUE, G-FORMATDUP, G-UNIQUE) are re-implemented here against
       the OBSERVABLE paper (the rendered text/images) + the registry, never
       against a sidecar.
    ✗ fig_manifest.json / batch_state.json / progress.json — internal Step-7 sidecars.
       The figural and RC/cloze maps Step 8 needs are embedded in registry.json
       (figural_manifests[], rc_manifests[]) and re-extracted at S3-PRE (§3).

## S0-2 — OUTPUTS (what Step 8 delivers)

  CORE DELIVERABLE SET (always; via ONE present_files call, at certification / Phase 3):
    1. [ExamCode]_Mock[N]_Create_Complete.docx   — the RECTIFIED, zero-defect paper
                                            (distinct filename — reads Mock[N]_Create.docx,
                                             writes Mock[N]_Create_Complete.docx; input retained)
    2. [ExamCode]_registry.json           — RE-SYNCED from the fixed file (§13):
                                            mock-N hashes/stems/tuples/manifests/
                                            content_tracking rebuilt to match the
                                            rectified content.
  CONDITIONAL DELIVERABLE (only when ≥1 question was REGENERATED — Class RG, §8):
    3. [ExamCode]_Mock[N]_audit_changelog.md  — an AUTHOR-ONLY audit artefact
                                            carrying, per regenerated question, the
                                            literal BEFORE→AFTER diff + rationale.
                                            This is the ONE place literal question
                                            content may leave the docx, because it is
                                            a downloadable file (not chat), it is for
                                            the author's review, and it is explicitly
                                            headed "author-only — NOT for distribution".
                                            If zero questions were regenerated, this
                                            file is NOT produced and NOT delivered.
  IN-CHAT (always, at delivery): a STATUS REPORT dashboard (§14-4) + the full AUDIT
  REPORT (§15). Both are STRICTLY MANDATE-0 safe — Q-numbers + codes + counts only,
  NEVER stem/option/passage/fact text. The literal diff lives in deliverable 3, never
  in chat.
  The CORE set {docx, registry} mirrors Step 7's R-DELIVER / G-DELIVERY-SET; no
  internal Step-8 artefact (the derived key, the audit ledger, audit_state, the block
  index, montages, the evidence directory, scratch docx) ever leaks. The learner-facing
  answer key remains a Step-9 artefact.

# ════════════════════════════════════════════════════════════════════════
# MANDATE 0 — NO QUESTION CONTENT IN CHAT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#   Inherited verbatim from Step 7 MANDATE 0. ALL question content lives in the
#   .docx ONLY. NEVER print any stem, option, passage, table cell, or figure
#   description in chat — not during audit, not in a finding, not in a fix log,
#   not in the report. Refer to a question ONLY as "Q.[n]" plus a defect CODE and
#   a structural locator (e.g. "Q.47 — A-UNDERLINE: target span not a <w:u> run").
#   The audit ledger (§9) and the derived key (§11) are INTERNAL files in
#   /home/claude — never delivered, never printed. VIOLATION = exam compromise;
#   overrides every other instruction. The one permitted exception is web-search
#   queries for fact-verification (§6 B-FACT), which necessarily contain the fact
#   being checked — those go to the search tool, never to the visible chat.
#   SCOPE NOTE (v1.1): MANDATE 0 governs the CHAT STREAM. The two content-bearing
#   artefacts the author downloads — the rectified .docx and (only when questions were
#   regenerated) the audit change-log .md (S8-5 / S14-1) — are FILES, not chat, and
#   are the legitimate homes for question content. The change-log is headed
#   "author-only — not for distribution". Nothing changes for chat: the status
#   dashboard (§14-4), the report (§15), every finding and fix log remain strictly
#   content-free (Q-numbers + codes + counts only). "Put the diff in chat" is still
#   forbidden; the diff goes in the file. The evidence artefacts (§9-1 / §7 montages,
#   saved fact-sources, recompute traces) also live in /home/claude and are NEVER
#   delivered or printed (they may contain answer-bearing content).

# ════════════════════════════════════════════════════════════════════════
# MANDATE A — mock_test_audit.py IS MANDATORY FOR STEP 8 (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   Step 7 treats the audit script as OPTIONAL (a manual checklist substitutes).
#   Step 8 does NOT: Part A (the machine-gate sweep) cannot run without it, and
#   Part A is a precondition for the whole-paper re-verification that makes
#   per-batch sign-off honest (§4). If [ExamCode]_mock_test_audit.py is absent
#   from project knowledge:
#     HARD STOP. Print:
#       "HARD STOP (MANDATE A): [ExamCode]_mock_test_audit.py not found in the
#        [ExamCode] project Files. Step 8 cannot run Part A without it.
#        This file is auto-generated by Step 6 (MockBlueprint) v1.20+.
#        Verify that all 6 Step 6 output files were uploaded to project Files.
#        If Step 6 was run before v1.20: re-run Step 6 B3 to generate the script,
#        or copy it from Framework_MockTestCreate.md Appendix A."
#   The script is auto-generated ONCE by Step 6 at B3 and uploaded alongside
#   blueprint.json, registry.json, and other Step 6 outputs.
#   v2.6 — MANDATE A GUARANTEES A WORKING AUDITOR, NOT A FILE THAT PRINTS "PASS".
#   The script self-tests with `--self-test`, which MUST be the FIXTURE-BASED
#   authoritative self-test: it builds tiny docx fixtures and asserts each gate
#   CATCHES a planted defect AND PASSES a clean fixture, and it must print
#   "SELF-TEST: N/N PASS" with N >= AUTH_GATE_FLOOR (currently 35 — the Appendix A
#   authoritative count) AND include the C1–C7 completion-gate fixtures. A
#   CONSTANT-PRINT stub that merely emits "N/N PASS" without executing any gate
#   (e.g. the 13-gate minimum-viable stub `def self_test(): print("SELF-TEST:
#   13/13 PASS"); return 0`) is REJECTED at P1 — it is NOT an acceptable auditor.
#   The one canonical script that satisfies this is Appendix A (and its lockstep
#   twins — see §21). For the generation/lifecycle contract see
#   Framework_Blueprint.md §13-7A.

# ════════════════════════════════════════════════════════════════════════
# MANDATE D — DELIVER ONCE, ONLY WHEN CERTIFIED CLEAN (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   present_files is FORBIDDEN until the WHOLE paper is certified clean at Phase 3.
#   v2.6 — "certified clean" is now a COMMAND RESULT, not a self-judgment: the
#   Phase-3 COMPLETION GATE (S5-1A) must print "COMPLETION-GATE: PASS" (final Part A
#   exit 0 + zero fixable WARN + the C1–C7 ledger/evidence assertions all pass +
#   registry re-synced). A self-declared "clean" is NOT acceptance — the completion
#   gate is (MANDATE B). Mid-audit the docx is deliberately inconsistent (a fix in
#   one batch can transiently open a global defect that the next whole-paper Part A
#   closes), so a partial file must never be presented. /mnt/user-data/outputs stays
#   EMPTY until Phase 3; the work-in-progress docx is staged in /home/claude across
#   "continue" turns so it is never lost. This mirrors Step 7 S13-7 and the T2 §12
#   invariant "present_files FORBIDDEN until exit 0 + verdict clean". The ONE
#   present_files call ships the core set (+ the change-log artefact when
#   regenerations occurred) — see §14.

# ════════════════════════════════════════════════════════════════════════
# MANDATE B — EXHAUSTIVE BATCHED REVIEW (Phase 2 cannot be collapsed) (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   Phase 2 (§4 S4-3) audits EVERY question — zero sampling (RA-3) — in K batches of
#   ≤ AUDIT_BATCH_SIZE (§4 S4-6). It may NEVER be skipped, compressed into a single
#   consolidated pass, or replaced by a spot-check, in ANY mode (interactive OR
#   autonomous). The spec keeps two things SEPARATE, and only one is waivable:
#     • EXHAUSTIVENESS (RA-15a) — every question gets B-SOLVE / B-UNIQUE / B-DISTRACT /
#       B-STEMOPT / B-FACT / B-PASSAGE (§6) + §7 view/recompute, each leaving a STAMPED
#       entry in audit_state.ledger (§9-1) that NAMES its on-disk evidence artefact
#       (§7 montage / saved fact-source / recompute trace). NON-NEGOTIABLE.
#       Mode-independent.
#     • PACING (RA-15b) — one batch = one response, continue-gated. MAY be waived in
#       autonomous mode (§4 S4-3A). Waiving the PAUSE NEVER waives the REVIEW.
#   ENFORCEMENT (not prose): Phase 3 (§4 S4-4 STEP 1) runs the audit.py COMPLETION
#   GATE — `--final --audit-state <path>` (S5-1A). It asserts, from audit_state.json:
#   batches_done == K; one stamped ledger entry per question (== total_questions);
#   B-UNIQUE / A-MSQ-KEY ran per question; every factual entry has a recorded
#   fact_source WHOSE SAVED FILE EXISTS (RA-11); every §7 artefact carries its RA-19
#   stamp AND the montage/recompute file it names EXISTS and is non-trivial. ANY
#   failed assertion → exit non-zero → HARD STOP: present_files is FORBIDDEN
#   (MANDATE D). A self-declared "clean" is NOT acceptance — the completion gate is.
#   This closes the Phase-1→Phase-3 shortcut that a machine-only Part A + a hollow
#   self-test cannot catch. "I ran fast because I skipped Phase 2" is a MANDATE B
#   violation, not a valid autonomous run.

# ════════════════════════════════════════════════════════════════════════
# THE CORE PRINCIPLE — fix locally, verify globally, certify whole-paper last
# ════════════════════════════════════════════════════════════════════════
#   Auditing differs from generating in two ways that drive the whole architecture:
#     (1) The paper exists IN FULL at second zero. So machine gates that are
#         WHOLE-PAPER by nature (answer-run patterns, cross-mock dedup, allocation
#         tallies, cross-section boundaries) run over the ENTIRE docx — they
#         cannot be run on a 10-question slice. Only the EXPENSIVE half — per-
#         question semantic reasoning, fact-verification, figure-viewing, and
#         regeneration — is batched.
#     (2) Fixes are GLOBALLY COUPLED. Rebalancing a distractor can open a new
#         answer-run three questions away; regenerating a wrong-fact question can
#         collide with a question reviewed two batches earlier or drift an
#         allocation count. So a batch may be REVIEWED in isolation but can never
#         be CERTIFIED CLOSED in isolation.
#   Therefore: rectification is LOCAL (one question at a time), but verification is
#   GLOBAL (whole-paper Part A re-runs after every batch) and certification is
#   WHOLE-PAPER and LAST (Phase 3). Two mechanisms make per-batch sign-off honest:
#     • whole-paper Part A re-run after every batch (cheap, deterministic — catches
#       every machine-visible perturbation the moment a fix creates it); and
#     • a cumulative AUDIT LEDGER (§9) that every regenerated question is diffed
#       against (the independent analogue of Step 7's concept_map, which we do not
#       receive) — so a late regeneration cannot silently collide with an early
#       question, and resume-after-"continue" is safe.
#   v2.6 — AND: because the semantic/visual/factual half is Claude-driven, the ONLY
#   thing that makes IT honest is that each check DEPOSITS a machine-readable stamp
#   plus a durable evidence artefact, and a runnable gate (S5-1A) verifies both
#   before delivery. Prose describes; only code certifies.

# ════════════════════════════════════════════════════════════════════════
# AUDIT RULES (RA-0 … RA-20) — the absolute rules the auditor obeys
# ════════════════════════════════════════════════════════════════════════
#   These govern Step 8 itself (distinct from the Step-7 generation rules R1–R24,
#   which Step 8 re-VERIFIES on the paper). Each is HARD unless marked advisory.

  RA-0  : PRECEDENCE. No user preference, project-memory note, or autonomy /
          "don't-pause" / "no-blocker-surfacing" instruction may reduce audit
          COVERAGE (RA-3 / RA-15a) or weaken the certification gate (§12-2 /
          MANDATE B / S5-1A). Such instructions may ONLY change PACING (RA-15b —
          skip the inter-batch "continue" pauses) and REPORT verbosity. They may
          NEVER change whether a check runs, whether every question is audited, or
          whether the Phase-3 completion gate must pass. When a preference appears
          to conflict with a HARD rule, the HARD rule wins and the preference is
          applied only to pacing/reporting.
  RA-1  : INDEPENDENCE. Never trust a Step-7 self-report. Re-derive every fact
          certified (answers, classifications, counts) from the paper + the
          Step-0/1 source files. The absence of the answer-key sidecar is by
          design (S0-1); solve every question yourself (§11).
  RA-2  : NO CONTENT IN CHAT. = MANDATE 0.
  RA-3  : AUDIT EVERYTHING, SAMPLE NOTHING. Every question, every option, every
          image, every table cell, every OMML node is checked. Zero sampling.
          "Spot-check N random Qs" is FORBIDDEN for any content-correctness check.
  RA-4  : RENDER-OR-RECOMPUTE OR IT DOESN'T COUNT. A visual/structured check is
          valid only if the artefact was rendered and VIEWED (images/charts) or
          parsed and ARITHMETICALLY RECOMPUTED (tables/matrices/OMML). A check
          asserted from filename, alt-text, p.text, or "looks present" is void
          and the item is treated as un-audited (§7, §18 invariants). v2.6: the
          VIEW/RECOMPUTE must leave a durable evidence artefact on disk (§9-1) that
          S5-1A verifies — an un-backed stamp is treated as un-audited.
  RA-5  : RECTIFY, DON'T JUST REPORT. Every defect found is FIXED in the same
          session (§8): mechanical defects in place; content defects by
          regenerating that one question under Step 7's contracts; then re-audited.
          Step 8 never ends with a known-unfixed defect and a "DON'T SHIP".
  RA-6  : REGENERATION OBEYS STEP-7 CONTRACTS. Any replacement question must
          satisfy EVERY Step-7 rule it would have had to satisfy at generation:
          blueprint count + subtopic_id join, section_rules pattern + difficulty +
          wrong_option_structure, registry dedup (L1–L18), intra-mock scenario +
          presentation uniqueness, and all render contracts (R-LINKED, R-FIGURAL,
          R-UNDERLINE, R-OPTREF, R-UNIQUE, R-MATH-OMML, R10/R13/R14/R24). A fix
          that introduces a new violation is itself a defect (§8 re-audit loop).
  RA-7  : FIX LOCALLY, VERIFY GLOBALLY. After any batch's fixes, re-run the
          WHOLE-PAPER Part A before ending the batch; resolve any global
          perturbation in the same response (core principle).
  RA-8  : NEVER REDUCE COUNT TO "FIX". A duplicate/clone/over-allocation is fixed
          by REGENERATING on a new scenario/presentation — never by deleting a
          question (which would break the blueprint allocation). Inherited from
          Step 7 G-CONCEPTDUP / G-FORMATDUP fix discipline.
  RA-9  : EXAM-AGNOSTIC. Read every exam-specific value from the source files
          (EXAM-AGNOSTIC GUARANTEE). Hardcode nothing. A missing value → SKIP the
          dependent check with a logged reason, never a hardcoded substitute.
  RA-10 : LANGUAGE-AWARE. The non-ASCII / regional-script check (A-SCRIPT) is
          conditioned on section_rules CATEGORY-C `language`. Devanagari/Tamil/etc.
          is LEGITIMATE on a hindi/bilingual/regional exam and must NOT be flagged
          as corruption; it is flagged ONLY when language == 'english' (then it is
          copy-paste corruption). U+FFFD replacement characters are ALWAYS a defect
          regardless of language.
  RA-11 : LIVE FACT-CHECK. Every current-affairs and static-GA fact, and every
          factual option, is web-verified at audit time (§6 B-FACT). Never certify
          a fact from model memory. A fact that cannot be sourced, or is wrong, is
          a defect → regenerate. v2.6: the verification MUST save its raw result
          (query + URL + retrieval-time + snippet) to the evidence dir and the
          ledger entry's fact_sources[] MUST name that saved file — S5-1A C5 fails
          if the file is absent (a bare URL string is not sufficient).
  RA-12 : DEFENSIBLE-ANSWER CONTRACT (mirrors Step 7 R-ANSWER; parameterised by the
          subtopic's answer_cardinality, re-derived from blueprint subtopic_list — default
          'single'). SINGLE: every question has exactly one defensible correct option
          (a second defensible option = defect → disambiguate the stem or replace the
          colliding option, §8). MULTI (MSQ): the re-derived correct SET S is a non-empty
          PROPER subset of {1..OPTIONS_COUNT} (1≤|S|≤n−1, and |S|=msq_k when
          msq_k_mode=fixed); every IN-set option is defensible under EVERY fair reading
          and every OUT-set option is indefensible under ANY fair reading — a borderline
          OUT-set option (one that should arguably be selected) is the MSQ analogue of the
          two-defensible-answers defect → disambiguate or move/remove it. Negation
          composes (derive S for the negated predicate, then apply the contract). This is
          the single most student-harmful content defect; it is checked for EVERY Q in the
          mode that question's subtopic declares.
          NUMERICAL (NAT; v1.4, when the subtopic is answer_type=='numerical'): the axis is
          checked FIRST and supersedes cardinality — there are no options to adjudicate. The
          re-derived answer is a single VALUE that the stem must determine UNIQUELY (two
          defensible values under a fair reading — ambiguous rounding, under-specified figure,
          missing unit — is the NAT analogue of the two-defensible-answers defect → disambiguate
          the stem). The value's form must match nat_answer_type (integer⇒integral; real⇒a
          decimal at the exam's precision); for real NAT the accepted band is
          [value−nat_tolerance, value+nat_tolerance] = ca_range (lo≤hi). A 0/negative/fractional
          value is valid (presence-tested, never truthiness). The value must not leak as a given
          elsewhere. Enforced by A-NAT-ANSWER (Claude-derivation) + A-NAT-NOOPT/A-NAT-INSTR
          (machine) — see §5.
  RA-13 : CROSS-MOCK INTEGRITY. Cross-mock dedup runs FULLY against registry.json
          with --mockN N self-exclusion (so re-auditing the registered mock does
          not flag its own stems). Intra-mock dedup is verified in its OBSERVABLE
          form (rendered text/images), since the concept_map is not delivered (§10).
  RA-14 : DELIVER ONCE, CLEAN. = MANDATE D.
  RA-15a : EXHAUSTIVENESS. Every question in Phase 2 is audited — zero sampling
           (RA-3) — and leaves a stamped audit_state.ledger entry (§9-1) that names
           its on-disk evidence artefact. Holds in EVERY mode; no preference may
           waive it (RA-0). This is the WHAT. Mechanically enforced by S5-1A
           (C2/C3 + evidence checks).
  RA-15b : PACING / BATCH STOP LAW. Interactively: one batch = one response, each
           ending on an explicit "continue"; Claude never auto-advances. In
           AUTONOMOUS mode (§4 S4-3A) the pause is waived and Batches 1..K run
           sequentially in one session — RA-15a still holds for every question.
           Phase 1 ends waiting for "continue" (interactive only); Phase 3 auto-runs
           after batch K in both modes. This is the WHEN. Linked-stimulus groups are
           atomic (RA-16); the whole-paper machine sweep (Phase 1) and the final
           certification (Phase 3) never wait for "continue".
  RA-16 : ATOMIC LINKED GROUPS. A linked-stimulus group (RC passage set, cloze
          set, DI table/chart set, puzzle set) is NEVER split across batches; it is
          reviewed as one unit so cross-member consistency is checkable together.
          v1.4 (ND11): a linked group MAY contain NAT members (a shared DI table/chart
          followed by numerical-answer questions). A NAT member is a 0-option member — the
          shared-stimulus self-containment audit (A-STIMORPHAN) and atomic-group review are
          UNCHANGED (orthogonal to whether a member has options); the member is simply audited
          under the numerical gates (A-NAT-NOOPT/INSTR, A-NAT-ANSWER, B-SOLVE/UNIQUE/LEAK NAT).
  RA-17 : REGISTRY RE-SYNC FROM THE FIXED FILE ONLY. The output registry is rebuilt
          from the FINAL rectified docx (§13), never from the input registry's stale
          mock-N entries and never from generation memory.
  RA-18 : RESUME-SAFE. All cross-batch state (audit ledger, batch plan, the WIP
          docx, the derived key, the evidence dir) persists in
          /home/claude/[ExamCode]_M[N]_audit_state.* so a "continue" after any gap
          resumes exactly, re-reviewing nothing and forgetting nothing (RA-3 still
          holds across resume).
  RA-19 : PROVENANCE STAMPS. Every certified item carries a stamp in the ledger
          ('machine' | 'recomputed' | 'rendered-and-viewed' | 'web-verified+source'
          | 'reviewer-verified') AND, for every visual/structured/factual item, the
          PATH of the durable evidence artefact that stamp is backed by (§9-1).
          Phase 3 refuses to certify if any item lacks the stamp its check-class
          requires OR if the named evidence file is missing/trivial (§18, S5-1A). An
          un-stamped or un-backed visual/structured item blocks delivery (RA-4).
  RA-20 : KINDNESS TO THE NEXT STEP. The handoff (§14) states plainly what was
          fixed/regenerated (by Q-number + code, never content) and instructs the
          user to replace the registry in project knowledge before Step 9 / the
          next mock — so dedup integrity is preserved across the series (RS-10).

# ════════════════════════════════════════════════════════════════════════
# §1 — PIPELINE POSITION & SOURCES OF TRUTH
# ════════════════════════════════════════════════════════════════════════

## S1-1 — Sources of truth (strict priority order)

  Priority 1: This spec (Framework_MockTestCreateAudit.md)        — audit procedure
  Priority 2: [ExamCode]_blueprint.json    — counts, sections, q_ranges, difficulty,
                                              format presence (CONFLICT WINNER on
                                              allocation/structure, per Step 7 S1-2)
  Priority 3: [ExamCode]_section_rules.md  — per-subtopic patterns, formats, escape
                                              tokens, OMML_required, language, exam params
  Priority 4: [ExamCode]_subtopic_manifest.json — subtopic_id join + mandate/alternation
  Priority 5: [ExamCode]_registry.json     — cross-mock dedup corpus + embedded manifests
  Priority 6: The paper itself             — the audit surface (never a source of
                                              "truth" about what is CORRECT; only the
                                              object under test)

  CONFLICT RULE (inherited from Step 7): blueprint.json wins over section_rules.md
  on format assignments, allocation counts, and structural decisions. section_rules
  wins on per-subtopic CONTENT patterns, escape tokens and rendering requirements.
  The paper never overrides a source file — a paper that disagrees with a source
  file is, by definition, the defect under repair.

## S1-2 — Memory prohibition

  ABSOLUTE (= Step 7 S1-4): Claude must NEVER use training memory to decide whether
  a question is correct, whether a fact is current, what a subtopic's scope is, or
  what a pattern should look like. Content correctness is decided by RE-DERIVATION
  (solve it) and WEB-VERIFICATION (source it). DOCUMENTS + LIVE SOURCES WIN OVER
  MEMORY. The one thing memory may do is FLAG suspicion ("this fact looks stale") —
  which then triggers a web check, never a verdict.

# ════════════════════════════════════════════════════════════════════════
# §2 — TRIGGER FORMAT & MOCK-NUMBER RESOLUTION
# ════════════════════════════════════════════════════════════════════════

## S2-1 — Trigger formats

  PRIMARY: MockCreateAudit M[N]
  RESUME : MockCreateAudit M[N] resume     (re-enter mid-audit; §4 / RA-18)
  STATUS : MockCreateAudit M[N] status     (print audit dashboard, no work)

  ExamCode: read from exam_config.json in project knowledge; must match blueprint + registry exam_code.
  [N]       : integer ≥ 1. The mock to audit. Resolution + validation in S2-2.

## S2-2 — Mock-number resolution (do this BEFORE loading questions)

  N is resolved from TWO sources; both must agree:
    (a) the trigger's M[N];
    (b) the uploaded docx filename [ExamCode]_Mock[N]_Create.docx.
  (v2.7: the paper's own title block is NO LONGER a source. Step 7 R8b / G-PREQ1 makes
   the Create.docx questions-only — the first non-blank paragraph is Q.1, so there is
   no title paragraph to read. A-HEADER now STRIPS any residual pre-Q.1 block rather than
   reading N from it. Trigger + filename are sufficient and are the two reliable sources.)
  DISAGREEMENT → HARD STOP. Print which sources disagree and ask the user to
  confirm N. A wrong N corrupts the registry re-sync (§13) and the --mockN
  self-exclusion of cross-mock dedup (§10). Never guess.

  REGISTRY ALIGNMENT (critical for §13): registry.mocks_completed must END with N
  (Step 7 appended it). If mocks_completed[-1] != N OR N not in mocks_completed:
    HARD STOP. Print:
      "HARD STOP (S2-2): registry.mocks_completed = [...] does not end with mock
       [N]. Step 8 re-syncs the registry by rebuilding the most-recently-appended
       mock's slice; that requires the registry from the Step-7 run that generated
       mock [N]. Upload the registry delivered alongside this docx, then re-run."
    This catches: a stale registry, a skipped mock, or auditing an out-of-order
    mock — all of which would make the §13 trailing-slice rebuild unsafe.

# ════════════════════════════════════════════════════════════════════════
# §3 — SESSION START: PRE-FLIGHT (P0 … P9) — run ALL before any audit
# ════════════════════════════════════════════════════════════════════════
#   Do not parse questions, do not run gates, until every P-check passes. These
#   are integrity and provenance checks; failing one means the audit would be
#   built on sand. Each P-check is HARD STOP unless noted.

## P0 — Copy inputs to the working directory

  ```python
  import shutil, os, json, re, sys, zipfile, hashlib
  EXAM = "[ExamCode]"     # from trigger
  N    = [N]              # resolved mock number (S2-2)
  WORK = "/home/claude"
  PROJ = "/mnt/project"
  UPL  = "/mnt/user-data/uploads"

  def _find(name):
      """Inputs may arrive in project knowledge OR in uploads. Prefer uploads for
      the docx+registry (the freshly delivered pair); prefer project for the static
      Step-0/1 files and the audit script."""
      for base in (UPL, PROJ):
          p = os.path.join(base, name)
          if os.path.exists(p):
              return p
      return None

  # C3 (v2.7.3): derive the paper identity from the blueprint (its filename is fixed, so it can
  # be read before the paper docx). paper_slug names the input Step 7 actually wrote — "Mock[N]"
  # for a mock (byte-identical), else a scoped paper_slug. Fallback "MOCK:M{N:02d}" for pre-C1.
  import re as _re_pid
  _bp_path = _find(f'{EXAM}_blueprint.json')
  _bp      = json.load(open(_bp_path, encoding='utf-8')) if _bp_path else {}
  _tp      = next((mk for mk in _bp.get('mocks', []) if mk.get('mock') == N), None)
  paper_id   = (_tp or {}).get('paper_id', f"MOCK:M{N:02d}")
  paper_slug = f'Mock{N}' if paper_id.startswith('MOCK:') else paper_id.replace(':', '_')

  REQUIRED = {
      'docx'    : f'{EXAM}_{paper_slug}_Create.docx',
      'registry': f'{EXAM}_registry.json',
      'rules'   : f'{EXAM}_section_rules.md',
      'blueprint': f'{EXAM}_blueprint.json',
      'manifest': f'{EXAM}_subtopic_manifest.json',
      'audit_py': f'{EXAM}_mock_test_audit.py',     # MANDATE A — hard stop if absent
  }
  paths = {}
  missing = []
  for kind, name in REQUIRED.items():
      src = _find(name)
      if src is None:
          missing.append(name); continue
      dst = os.path.join(WORK, name)
      shutil.copy(src, dst)
      paths[kind] = dst
  if missing:
      raise SystemExit(
          "HARD STOP (P0): missing required input(s): " + ", ".join(missing) +
          ". Upload them to the [" + EXAM + "] project / chat, then re-run. "
          "(If only the audit script is missing, see MANDATE A — it is auto-generated "
          "by Step 6 v1.20+. Verify Step 6 outputs were uploaded.)")
  ```

## P0.5 — INPUT INTEGRITY (corruption / truncation) — HARD STOP unless repairable

  P0 catches MISSING inputs; P0.5 catches CORRUPT / TRUNCATED ones. Observed in the
  wild: large files synced through project-knowledge size caps arrive truncated
  (a 195 KB blueprint cut mid-object; a registry cut to 305 bytes; the audit.py cut
  mid-function while --self-test still printed PASS). A bare json.load on a truncated
  file throws an ugly traceback, not a clean stop; a file truncated exactly at an
  object boundary can even load and LOOK valid while being incomplete. So P0.5 checks
  parseability AND required-key presence, for each copied input:

  ```python
  import ast
  REQUIRED_KEYS = {
      'blueprint': ['exam_code', 'total_questions', 'sections', 'mocks'],
      'registry' : ['exam_code', 'mocks_completed', 'stem_texts'],
      'manifest' : ['exam_code'],
  }
  integrity_fail = []
  for kind in ('blueprint', 'registry', 'manifest'):
      p = paths[kind]
      try:
          obj = json.load(open(p, encoding='utf-8'))
      except Exception as e:
          integrity_fail.append(f"{os.path.basename(p)}: JSON parse failed ({e})")
          continue
      for k in REQUIRED_KEYS[kind]:
          if k not in obj:
              integrity_fail.append(f"{os.path.basename(p)}: required top-level key "
                                    f"{k!r} missing (likely truncated)")
  # section_rules must be non-empty AND contain the EXAM_STRUCTURE header block
  # (the on-disk literal token written by Step 5 write_section_rules(); this block is
  # referred to as "CATEGORY C" ONLY in spec prose/comments -- never search for that
  # phrase as literal file content, see Framework_MockTestAnalyse.md §14):
  try:
      rt = open(paths['rules'], encoding='utf-8').read()
      if len(rt) < 200 or not re.search(r'===\s*EXAM_STRUCTURE\s*===', rt, re.I):
          integrity_fail.append(f"{os.path.basename(paths['rules'])}: empty or missing "
                                f"EXAM_STRUCTURE header block (likely truncated)")
  except Exception as e:
      integrity_fail.append(f"section_rules read failed ({e})")
  # audit.py must ast.parse (a mid-function truncation is a SyntaxError) AND pass the
  # HARDENED fixture self-test (P1) — the self-test alone is not enough because a
  # constant-print stub parses AND prints PASS; ast.parse catches the truncated body,
  # P1 catches the hollow body.
  try:
      ast.parse(open(paths['audit_py'], encoding='utf-8').read())
  except SyntaxError as e:
      integrity_fail.append(f"{os.path.basename(paths['audit_py'])}: ast.parse "
                            f"SyntaxError line {e.lineno} (truncated/corrupt script)")

  if integrity_fail:
      # POLICY (a) DEFAULT → HARD STOP (code A-INTEGRITY). A truncated blueprint/registry
      # silently breaks allocation checks (§6-4) and the re-sync (§13) — auditing against
      # it is auditing against sand.
      # POLICY (b) SANCTIONED REPAIR is permitted ONLY for [ExamCode]_mock_test_audit.py
      # (regenerate from Appendix A / Step 6 B3 — §21) and ONLY when the repaired script
      # then passes the hardened self-test (P1). Log it to
      # session_log.inputs_repaired[] and disclose in §R13. NEVER silently repair
      # blueprint/registry DATA — its content is not reconstructible and a guess corrupts
      # every downstream gate. (If only mock N's own slice of a large blueprint is intact
      # and reachable, auditing MAY proceed against that slice ONLY with an explicit §R13
      # limitation and the missing-data hard-stop for any gate that needs the truncated
      # part.)
      audit_py_only = all('mock_test_audit.py' in f for f in integrity_fail)
      if audit_py_only:
          # regenerate the canonical script (§21) → re-run P0.5 + P1; proceed only if clean.
          raise SystemExit("A-INTEGRITY (P0.5): [ExamCode]_mock_test_audit.py is corrupt/"
                           "truncated. SANCTIONED REPAIR: regenerate the canonical auditor "
                           "(Appendix A / Step 6 B3), re-upload, re-run. Log to "
                           "session_log.inputs_repaired[].")
      raise SystemExit("HARD STOP (P0.5 / A-INTEGRITY): corrupt/truncated input(s): "
                       + "; ".join(integrity_fail) +
                       ". Re-upload the INTACT file(s); never audit against truncated "
                       "blueprint/registry data.")
  ```

## P1 — Audit-script self-test (MANDATE A) — HARDENED (v2.6)

  ```
  python3 /home/claude/[ExamCode]_mock_test_audit.py --self-test
      → MUST print  "SELF-TEST: N/N PASS"  where:
          • N >= AUTH_GATE_FLOOR (currently 35 — the Appendix A authoritative count), AND
          • the self-test is FIXTURE-BASED: it builds tiny docx fixtures and asserts
            each gate CATCHES a planted defect and PASSES a clean fixture
            (Appendix A self_test()), AND
          • it includes the C1–C7 completion-gate fixtures (S5-1A).
  ```
  REJECTED — HARD STOP (each yields false-clean audits):
    • a CONSTANT-PRINT self-test that prints PASS without executing any gate
      (e.g. the minimum-viable 13-gate stub: `def self_test(): print("SELF-TEST:
      13/13 PASS"); return 0`). No longer acceptable — MANDATE A must guarantee a
      WORKING auditor, not a file that prints "PASS".
    • N < AUTH_GATE_FLOOR (a reduced/stub gate set).
    • any traceback / FAIL / non-zero exit.
    • a body that ast-parses (P0.5) but whose gates raise at runtime — caught here
      because the fixture self-test actually INVOKES them (a truncated/regex-broken
      body that still prints a hollow PASS is exactly what slipped through in v2.5).
  On any REJECT → HARD STOP: regenerate/replace with the canonical auditor
  (Step 6 v1.20+ / Framework_MockTestCreate.md Appendix A — §21). NEVER audit with a
  script that fails the hardened self-test: a broken/hollow gate gives false-clean
  results.

## P2 — Load + validate the source files

  ```python
  blueprint = json.load(open(paths['blueprint'], encoding='utf-8'))
  registry  = json.load(open(paths['registry'],  encoding='utf-8'))
  manifest  = json.load(open(paths['manifest'],  encoding='utf-8'))
  rules_txt = open(paths['rules'], encoding='utf-8').read()

  # exam_code coherence (RS-5):
  for nm, obj in (('blueprint', blueprint), ('registry', registry), ('manifest', manifest)):
      if obj.get('exam_code') != EXAM:
          raise SystemExit(f"HARD STOP (P2): {nm}.exam_code="
                           f"{obj.get('exam_code')!r} != trigger {EXAM!r}.")

  # blueprint readability for mock N (Step 7 S3-2 structure):
  total_questions = blueprint['total_questions']
  sections        = blueprint['sections']                  # [{name,q_range,total_qs,max_attempt}]
  # v2.1: new fields from Step 6 v1.19 (exam_config v2.5 contract).
  # Read for availability; no new audit gates — structural metadata, not auditable content.
  bp_marking_scheme = blueprint.get('marking_scheme', [])
  bp_level          = blueprint.get('level', 'unknown')
  bp_medium         = blueprint.get('medium', 'unknown')
  # v2.5 THREE-AXIS: per-section format-distribution target + window params. Absent-safe:
  # a pre-v1.23 blueprint has no axis_schedule → {} → the whole Axis audit (S6-6) stays inert.
  axis_schedule   = blueprint.get('axis_schedule', {})
  AXIS_WINDOW     = blueprint.get('batch_size_qs', 10)          # mocks per window (== Step 6/7)
  TOTAL_MOCKS     = blueprint.get('total_mocks')                # for last-partial-window close
  mock_obj = next((m for m in blueprint['mocks'] if m['mock'] == N), None)
  if mock_obj is None:
      raise SystemExit(f"HARD STOP (P2): blueprint.mocks has no entry for mock {N}.")
  alloc = {}   # subtopic_id -> q_count (blueprint truth for this mock)
  for sec in mock_obj['sections']:
      for a in sec['subtopic_allocations']:
          alloc[a['subtopic_id']] = a   # carries q_count, format, type, names

  # CATEGORY-C exam params (auto-detected by Step 0; NEVER hardcoded here):
  def cat_c(key, default=None):
      m = re.search(rf'^\s*{re.escape(key)}\s*[:=]\s*(.+?)\s*$', rules_txt, re.M)
      return m.group(1).strip() if m else default
  LANGUAGE        = (cat_c('language', 'english') or 'english').lower()
  OPTIONS_COUNT   = int(cat_c('options_count', '4'))
  MARKS_PER_Q     = cat_c('marks_per_q')           # dict-ish string; parsed if header check needs it
  NEG_MARKING     = cat_c('negative_marking', '0')
  TIME_PER_Q_SEC  = cat_c('time_per_q_sec')
  OPTION_LABEL_FMT= cat_c('option_label_format', '1/2/3/4')   # CATEGORY-A may override per section
  # v2.1: new CATEGORY C fields from Step 5 v2.18
  MARKING_SCHEME  = cat_c('marking_scheme', '[]')  # per-range scoring rules (string repr of list)
  LEVEL           = cat_c('level', 'unknown')       # academic level
  MEDIUM          = cat_c('medium', 'unknown')      # exam language
  ```
  VALIDATE: total_questions > 0; sections non-empty and contiguous (q_ranges tile
  [1..total_questions] with no gap/overlap); difficulty_schedule has an entry for N
  whose simple+medium+hard == total_questions. Any failure → HARD STOP (corrupt
  blueprint; do not audit against a broken plan). (P0.5 already caught a TRUNCATED
  blueprint; this catches a STRUCTURALLY INCOHERENT one.)

## P3 — Open the docx + ZIP/rId/encoding integrity (A-ZIP, A-ENCODING)

  ```python
  docx = paths['docx']
  if os.path.getsize(docx) < 50_000:
      print("P3 WARN: docx < 50 KB — unusually small for a full paper; verify N.")
  with zipfile.ZipFile(docx) as z:
      names = set(z.namelist())
      assert 'word/document.xml' in names, "P3 HARD STOP: word/document.xml missing."
      doc_xml = z.read('word/document.xml').decode('utf-8', 'replace')
      rels = z.read('word/_rels/document.xml.rels').decode('utf-8') \
             if 'word/_rels/document.xml.rels' in names else ''
      # every r:embed / r:id referenced in document.xml must resolve in rels AND
      # point to a part that physically exists in the ZIP:
      ref_ids = set(re.findall(r'r:(?:embed|id|link)="([^"]+)"', doc_xml))
      rel_map = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
      for rid in ref_ids:
          tgt = rel_map.get(rid)
          if tgt is None:
              raise SystemExit(f"HARD STOP (P3/A-ZIP): rId {rid} unresolved in rels.")
          part = ('word/' + tgt) if not tgt.startswith(('http', '/')) else tgt
          if not tgt.startswith('http') and part.replace('word/../','') not in names \
             and ('word/'+tgt.replace('../','')) not in names:
              raise SystemExit(f"HARD STOP (P3/A-ZIP): rId {rid} → {tgt} not in ZIP.")
      # U+FFFD replacement char (encoding corruption) — ALWAYS a defect (RA-10):
      if '�' in doc_xml:
          print("P3/A-ENCODING: U+FFFD replacement char(s) present → flagged for "
                "rectification (encoding corruption).")
  ```
  A-ZIP failures are HARD (a paper with a dangling image rId is structurally
  broken). A-ENCODING (U+FFFD) is recorded as a defect to RECTIFY in Phase 1
  (regenerate the affected run/question), not a hard stop.

## P4 — Extract the embedded maps from the registry (the Step-8 analogue of T2 S3b)

  ```python
  # RC / cloze map for this mock (drives A-STIMORPHAN linked-group completeness):
  rc_entry = next((m for m in registry.get('rc_manifests', []) if m.get('mock') == N), None)
  passage_linked = set(rc_entry['passage_linked']) if rc_entry else set()
  cloze_linked   = set(rc_entry['cloze_linked'])   if rc_entry else set()
  # Figural map for this mock (drives A-FIGCOMP + §7 image audit coverage):
  fig_entry = next((m for m in registry.get('figural_manifests', []) if m.get('mock') == N), None)
  figural_qs = set(int(q) for q in fig_entry['figural_qs']) if fig_entry else set()
  # NOTE: registry image_hashes for the mock may be EMPTY (observed in the wild);
  #   §7/§10 therefore HASH word/media/ directly rather than trusting registry hashes.

  # v2.5 THREE-AXIS: window-level state (cross-mock; batch_state is per-mock in Step 7 too).
  #   registry.axis2_window : Step 7's SELF-REPORTED counts (what it declared it rendered).
  #   registry.axis2_audit  : Step 8's OWN INDEPENDENT tally, re-derived from each mock's docx.
  # Both key the current 10-mock window. Load Step 8's tally with a window-aware reset so a new
  # window starts from zero; mock N's re-derived counts are added at Phase 3 (from the FIXED docx).
  _cur_window       = (N - 1) // max(1, AXIS_WINDOW)
  s7_axis_window    = registry.get('axis2_window', {})          # Step 7's counts (for the drift WARN)
  _reg_audit        = registry.get('axis2_audit', {})
  if _reg_audit.get('window') != _cur_window:
      axis2_audit_sections = {}                                  # new window → fresh independent tally
      axis2_audit_mocks    = []                                  # mocks counted this window (idempotency)
  else:
      axis2_audit_sections = dict(_reg_audit.get('sections', {}))
      axis2_audit_mocks    = list(_reg_audit.get('mocks', []))
  # axis2_audit_sections[section] = {'axis1':{cls:n}, 'axis2':{cls:n}, 'axis3':{cls:n},
  #                                  'neg':int, 'total':int}  — accumulated across the window.
  ```
  These maps are a STARTING POINT, not gospel: §6/§7 re-derive linked groups and
  figural questions from the paper's own cues as a backstop (a question that
  references a stimulus but is absent from the manifest is itself a defect).

## P5 — Pre-Q.1 body-block check (A-HEADER — questions-only paper, v2.7)

  The generated paper is questions-only (Step 7 R8b / G-PREQ1): the FIRST non-blank body
  paragraph MUST be the bold "Q.1" stem. Read the paragraphs before Q.1 (this is
  structural metadata, not question content; MANDATE 0 permits reading it, never printing
  stems). Then:
    • ZERO non-blank paragraphs before Q.1 → A-HEADER PASS (questions-only).
    • ANY non-blank paragraph before Q.1 — a title ("... Mock Test [N] ..."), a
      "Total Questions / Maximum Marks / Time" line, an "Each question carries ...
      Negative marking ..." instruction, or any cover/preamble → A-HEADER DEFECT →
      STRIP the entire pre-Q.1 block in Phase 1 (CP-HEADER-STRIP). This is a
      content-preserving fix (the block is not question content), so it stays in Phase 1
      and never escalates to Phase 2.
  There is NO figure-checking: CATEGORY-C values (marks_per_q, time_per_q_sec,
  negative_marking, options_count, total_questions) are STRUCTURED METADATA in
  section_rules.md / blueprint.json / registry — they are NEVER printed in the paper, so
  there is nothing in the paper to reconcile against them; a downstream platform may
  render them from that metadata.
  Blank separator paragraphs before Q.1 are ignored (not a defect).
  DORMANT (exam-agnostic opt-in): if — and only if — section_rules.md EXAM_STRUCTURE
  declares `paper_header_block`, a printed header is permitted and A-HEADER does not fire.
  No current section_rules.md declares it, so the ban is absolute for every present exam.
  This is the Step-8 independent re-verification of Step 7 R8b / G-PREQ1.

## P6 — Build the question-block index (document-order parse; the audit's spine)

  Parse the docx body (paragraphs AND tables interleaved, in true document order)
  into per-question BLOCKS. A block = the opening "Q.<n>" paragraph through the
  paragraph/table/image immediately before the next "Q.<n>" paragraph. For each
  block record (no content leaves /home/claude): qnum; section (by q_range);
  the items trailing the last option of the block (used to detect a stimulus
  orphaned before the NEXT block's Q.<n> — the observable form of an A-QNFIRST
  violation, since the parser starts each block AT its Q.<n>); option paragraphs;
  attached tables; attached inline images (with their part names + media files);
  whether the stem carries OMML (<m:oMath>); whether any run carries <w:u>; the
  stem's structural cues (linked-stimulus references, escape-option references,
  underline references, math triggers). This index is written to
  /home/claude/[ExamCode]_M[N]_blockindex.json and is the input to Part A, Part B,
  and §7. OMML/text extraction MUST merge <m:t> (math) with <w:t> (text) — a stem
  that is pure OMML is BLANK in p.text and must never be judged "empty" (RA-4).

## P7 — Coverage cross-check (no question silently lost)

  assert len(blocks) == total_questions, else HARD STOP (A-COUNT pre-check): the
  paper does not contain blueprint.total_questions question blocks. Confirm the
  block q-numbers are exactly {1..total_questions} (A-SEQ pre-check) and strictly
  increasing in document order (A-MONO pre-check). These are re-asserted by the
  machine script in Phase 1; here they gate whether the index is even usable.

## P8 — Compute the BATCH PLAN once (possible because the whole paper is visible)

  Walk q = 1..total_questions, filling batches up to AUDIT_BATCH_SIZE (default 10).
  ATOMIC LINKED GROUPS (RA-16): a linked group (from passage_linked / cloze_linked /
  di groups / re-derived puzzle sets) is never split — if adding the next group
  would overflow the current batch, CLOSE the batch before the group and start the
  group in a fresh batch. The only batch permitted to exceed the cap is a single
  group larger than the cap (it becomes its own batch). Persist the plan to
  /home/claude/[ExamCode]_M[N]_audit_state.json (RA-18). K = number of batches.
  K is derived from the paper — never hardcoded — so a 100-Q paper and a 200-Q
  paper simply yield different K (fully exam-agnostic). K is the value the Phase-3
  completion gate asserts against batches_done (S5-1A C1).

## P9 — Initialise the audit ledger + the derived-key store + the evidence dir (§9, §11)

  Create /home/claude/[ExamCode]_M[N]_audit_state.json with:
    {mock:N, K:<from P8>, plan:[...], batches_done:[],
     evidence_dir: "/home/claude/[ExamCode]_M[N]_evidence",
     ledger:{entries:{}, scenarios:[], presentations:[], facts:[], vocab:[],
             images:[], derived_key:{}},
     defects:[], regenerations:[], stamps:{},
     session_log:{inputs_repaired:[]}}
  And create the evidence directory with subfolders (RA-19 / §7 / S5-1A):
    /home/claude/[ExamCode]_M[N]_evidence/montages/    — §7 image montages (VIEW proof)
    /home/claude/[ExamCode]_M[N]_evidence/facts/       — saved B-FACT search results
    /home/claude/[ExamCode]_M[N]_evidence/recompute/   — table/matrix/chart/OMML traces
  On a `resume` trigger the audit_state file is RELOADED (RA-18): nothing already
  reviewed is re-reviewed; nothing is forgotten; the evidence dir persists so its
  files still satisfy S5-1A at Phase 3.

  PRE-FLIGHT COMPLETE → print the dashboard (§15 short form) and BEGIN PHASE 1.

# ════════════════════════════════════════════════════════════════════════
# §4 — AUDIT ARCHITECTURE (three phases; the continue contract)
# ════════════════════════════════════════════════════════════════════════

## S4-1 — The three phases (overview)

  PHASE 1 — Whole-paper machine sweep + content-preserving fixes   (ONE response)
  PHASE 2 — Batched semantic + visual audit & rectification        (K responses,
                                                                    continue-gated
                                                                    interactively;
                                                                    sequential in
                                                                    autonomous mode)
  PHASE 3 — Final certification + registry re-sync + delivery      (auto; no continue)

  The split is forced by the core principle: machine gates are whole-paper by
  nature (Phase 1, and re-run inside every Phase-2 batch); semantic/visual review
  and regeneration are expensive and are batched (Phase 2); certification is whole-
  paper and last (Phase 3). PHASE 2 IS NEVER SKIPPED OR COLLAPSED (MANDATE B).

## S4-2 — PHASE 1 — whole-paper machine sweep (ONE response, no continue)

  STEP 1. Pre-flight §3 (P0–P9). If any HARD STOP fired, stop here.
  STEP 2. Run Part A (§5) over the ENTIRE docx → the global machine-defect map.
          Append the script STDOUT to the response (it is MANDATE-0 safe — codes
          + Q-numbers only).
  STEP 3. Apply ALL content-preserving fixes (§8 class CP) in one pass. These do
          NOT change which option is correct, so they are safe paper-wide and need
          no per-question re-solve:
            CP-FONT (→Calibri 11), CP-OPTLABEL (→option_label_format), CP-SECHDR
            (strip body section headers), CP-QNFIRST (re-emit block Q.N-first),
            CP-UNDERLINE (real <w:u> run; drop "(underlined: X)"), CP-MATHOMML
            (re-render built-up math as OMML; drop the raster/ASCII), CP-STIMEMBED
            (embed the shared stimulus into every linked member, Model A),
            CP-FIGDECOMP (decompose a composite figural panel into problem +
            per-option images — re-render under §7/Step-7 S10-8), CP-IMGNAME
            (rename mis-named legitimate figures to the canonical q{N}_* contract),
            CP-BLANKSEP (insert missing blank separators), CP-ENCODING (repair
            U+FFFD runs), CP-HEADER-STRIP (delete any non-blank paragraph before Q.1 —
            the paper is questions-only; Step 7 R8b / G-PREQ1).
          A fix that CANNOT be done without changing content (e.g. a figural panel
          whose underlying figure is wrong, not merely composited) is DEFERRED to
          Phase 2 as a content defect (§8 class RG) and only TAGGED here.
  STEP 4. Re-run Part A → confirm every machine gate that was content-preserving-
          fixable is now green. Remaining Part A FAILs are content defects to be
          resolved in Phase 2 (recorded in audit_state.defects with their batch).
  STEP 5. Print the Phase-1 summary (§15): gates fixed, gates still open (by code +
          Q-number), and the batch plan (K batches). Stage NOTHING to outputs
          (MANDATE D). Save the WIP docx + audit_state to /home/claude.
  STEP 6. INTERACTIVE mode: print "Phase 1 complete. Type 'continue' to begin
          semantic Batch 1 of K." and END THE RESPONSE. (RA-15b; interactive mode.
          AUTONOMOUS mode (S4-3A): no stop — fall straight into Batch 1; the review
          still runs for every question, RA-15a.)

  WHY mechanical fixes go first: when Phase 2 reads a question it then reads a
  STRUCTURALLY CLEAN block — it reviews the real OMML expression (not a raster),
  the embedded passage (not an orphan reference), the decomposed option images
  (not a baked panel). Semantic review is only meaningful on a structurally sound
  block.

## S4-3 — PHASE 2 — semantic + visual batch (≤ AUDIT_BATCH_SIZE Q; continue-gated)

  INTERACTIVE mode: triggered by "continue" / "go" / "next" (case-insensitive). Any
  other user message → answer it, then re-print "Type 'continue' to begin Batch [b]
  of K." (RA-15b; interactive. Claude NEVER auto-advances a Phase-2 batch
  interactively. AUTONOMOUS mode advances without the pause — S4-3A — but never
  skips a question, RA-15a.)

  For batch b (its q-list from the P8 plan):
    STEP A — SEMANTIC REVIEW (§6), every question in the batch, zero sampling:
       solve it (§11 B-SOLVE); verify exactly one defensible answer (B-UNIQUE);
       verify each distractor indefensible (B-DISTRACT); verify stem↔option
       coherence + escape-option coherence (B-STEMOPT / B-OPTREF-SEM);
       web-verify every CA/static-GA fact + factual option (B-FACT) AND SAVE each
       result to the evidence dir facts/ (RA-11); verify passage/cloze derivability
       (B-PASSAGE); record findings + a STAMPED ledger entry per question (§9-1).
    STEP B — VISUAL / STRUCTURED DEEP AUDIT (§7) for every image/table/matrix/
       chart/OMML in the batch: VIEW every image (save the montage PNG to the
       evidence dir montages/); PARSE + RECOMPUTE every table/matrix/chart and
       every OMML expression (save the recompute trace to recompute/). (RA-4/RA-19)
    STEP C — RECTIFY (§8): mechanical leftovers in place; content defects by
       REGENERATING that question under Step-7 contracts (RA-6); re-audit each
       regenerated/fixed question immediately (it is not "done" while it carries an
       unreviewed change). Diff every regeneration against the WHOLE ledger (§9) and
       the registry (§10) — not just this batch.
    STEP D — WHOLE-PAPER Part A re-run (RA-7): catch any GLOBAL perturbation this
       batch's fixes introduced (new answer-run, new dup, drifted count, new
       orphan). Resolve it before the batch ends.
    STEP E — Persist audit_state (ledger, defects, regenerations, stamps, evidence
       paths, WIP docx) to /home/claude (RA-18). Append b to batches_done. Stage
       NOTHING to outputs.
    STEP F — Print the batch report (§15): whole-paper Part A status; this batch's
       findings by Q-number + code; running totals (reviewed / fixed / regenerated).
    STEP G — If b < K: INTERACTIVE — print "Type 'continue' to begin Batch [b+1] of
             K." and END (RA-15b; interactive, one batch = one response). AUTONOMOUS
             (S4-3A) — proceed to Batch b+1 in the same session (no pause), still one
             batch processed at a time internally with its whole-paper Part A re-run.
             If b == K: do NOT wait — fall straight into PHASE 3 (RA-15b / Step 7 R24)
             in BOTH modes.

## S4-3A — AUTONOMOUS (headless) mode  (PACING WAIVER ONLY — RA-15b)

  TRIGGER: the user or a project-memory preference requests non-interactive /
  end-to-end / "don't pause" / "no-blocker-surfacing" execution, OR the run is
  scheduled/headless.

  EFFECT (PACING ONLY — RA-15b): Phase 1 does NOT stop for "continue"; Phase-2
  Batches 1..K run SEQUENTIALLY within the one session with no inter-batch pause;
  Phase 3 auto-runs. The per-batch structure (STEP A..G of S4-3) is UNCHANGED —
  batches are still processed one at a time internally, each with its whole-paper
  Part A re-run (RA-7) and its ledger + evidence writes; only the human "continue"
  gate is removed.

  UNCHANGED (RA-15a — HARD): every question is audited (zero sampling, RA-3); every
  §6 and §7 check runs and SAVES its evidence; audit_state.ledger gets one stamped
  entry per question; the Phase-3 COMPLETION GATE (S5-1A) MUST pass before
  present_files. NO preference may waive any of this (RA-0).

  Autonomous mode changes WHEN work is reported, never WHETHER work is done. A run
  that finishes "fast" because it collapsed Phase 2 is a MANDATE B violation, not a
  valid autonomous run — and S5-1A will FAIL it (C1/C2) at Phase 3. Report all K
  batch summaries in sequence in the final output.

## S4-4 — PHASE 3 — certification + re-sync + delivery (auto; no continue)

  Runs automatically after the last Phase-2 batch is clean.
    STEP 1. FINAL whole-paper Part A **with --audit-state** (S5-1A) → MUST print
            COMPLETION-GATE: PASS and exit 0 with zero fixable WARN. A bare --final
            (Part A only) is NOT sufficient to certify (MANDATE B / MANDATE D).
    STEP 2. Certification gate (§12-2 / §18): the S5-1A COMPLETION-GATE: PASS line
            supersedes self-attestation — every Part-B + §7 checklist item is now a
            C1–C7 assertion, zero residual defects, every item carries the provenance
            stamp its check-class requires AND the evidence file it names exists
            (RA-19). If anything is open → it becomes (or re-opens) a Phase-2 batch;
            Phase 3 does NOT proceed until COMPLETION-GATE: PASS. (There is no
            "PROVISIONAL ship" — Step 8 ships only a certified-clean paper.)
    STEP 3. REGISTRY RE-SYNC (§13) from the FINAL fixed docx (rebuild mock-N slice).
    STEP 4. Stage EXACTLY the two deliverables to /mnt/user-data/outputs; run the
            §14 pre-delivery checklist (closed set); ONE present_files call.
    STEP 5. Print the §15 full audit report + the §14 handoff. END THE RESPONSE.

## S4-5 — The "continue" contract + resume

  • INTERACTIVE: Phase 1 ends waiting for "continue". Each Phase-2 batch < K ends
    waiting for "continue". Phase 3 auto-runs after batch K (no "continue").
    AUTONOMOUS (S4-3A): no inter-batch pause; all phases run in one session.
  • "I'll now start the next batch" in the SAME response, INTERACTIVELY = a
    BATCH-STOP-LAW violation (RA-15b). Interactively, one batch = one response.
    (In autonomous mode advancing without the pause is CORRECT — the violation is
    skipping the REVIEW, not skipping the pause.)
  • `MockCreateAudit M[N] resume` reloads audit_state.json and resumes at the first
    not-done batch; already-reviewed questions are NOT re-reviewed (RA-18) but the
    whole-paper Part A still runs each batch (RA-7); the evidence dir persists.
  • `status` prints the dashboard (batches done / open defects / regenerations) and
    does no work.

## S4-6 — AUDIT_BATCH_SIZE

  AUDIT_BATCH_SIZE = 10 (default). It is a batch CEILING, not a target; a batch may
  be smaller when a linked group forces an early close (RA-16). It may be overridden
  ONLY downward (never above 10) and never in a way that splits a linked group. K is
  computed from this constant + the paper (P8) — never hardcoded per exam. NOTE:
  reducing the batch size changes K (more, smaller batches); it NEVER reduces
  coverage — every question is still audited (RA-15a) and S5-1A still asserts
  batches_done == K.

# ════════════════════════════════════════════════════════════════════════
# §5 — PART A: MACHINE GATES (whole-paper; run by the universal audit.py)
# ════════════════════════════════════════════════════════════════════════
#   Part A is the deterministic half. It runs over the ENTIRE docx (Phase 1, and
#   re-run after every Phase-2 batch). It re-verifies — INDEPENDENTLY, from the
#   paper + source files, never from a Step-7 sidecar — every machine-checkable
#   Step-7 contract. Every gate derives its expected values from blueprint.json /
#   section_rules.md / subtopic_manifest.json / registry.json (RA-9). Exit 0 +
#   zero fixable WARN is required to certify (MANDATE D). At Phase 3 the SAME script
#   ALSO runs the COMPLETION GATE (S5-1A) via --audit-state — the mechanical
#   enforcement of the Claude-driven Part B / §7 half.

## S5-1 — Invocation

  ```bash
  python3 /home/claude/[ExamCode]_mock_test_audit.py \
      /home/claude/[ExamCode]_Mock[N]_Create.docx \
      --blueprint /home/claude/[ExamCode]_blueprint.json \
      --rules     /home/claude/[ExamCode]_section_rules.md \
      --manifest  /home/claude/[ExamCode]_subtopic_manifest.json \
      --registry  /home/claude/[ExamCode]_registry.json \
      --mockN     [N] \
      --final
  ```
  --mockN [N] makes cross-mock dedup self-exclude mock N's own stems (re-auditing
  the registered mock is legal and must not flag the mock against itself). --final
  applies the full gate set + the OMML floor. Record exit code + full STDOUT;
  append STDOUT to the batch reply (RA-2 safe). Exit 0 = all gates passed. (Phase 1
  and every per-batch re-run use THIS form. Phase 3 adds --audit-state — S5-1A.)

## S5-1A — THE COMPLETION GATE (Phase-3 mechanical Part-B / §7 check) — v2.6

  Part A is machine-checkable; Part B (§6) and §7 are Claude-driven and — until
  v2.6 — were verified ONLY by the PROSE checklist §12-2, i.e. self-attested and
  therefore skippable. S5-1A makes them mechanically enforced by validating the
  audit_state.ledger (§9-1) that Claude already maintains AND the on-disk EVIDENCE
  artefacts each ledger stamp names. No new author-facing artefact is introduced;
  an existing internal one becomes load-bearing.

  NEW Phase-3 invocation (REQUIRED to certify):
    python3 .../[ExamCode]_mock_test_audit.py \
        /home/claude/[ExamCode]_Mock[N]_Create.docx \
        --blueprint ... --rules ... --manifest ... --registry ... --mockN N \
        --final --audit-state /home/claude/[ExamCode]_M[N]_audit_state.json

  With --audit-state, run_audit performs Part A, then ADDS these assertions (ALL
  HARD; exit != 0 on any failure). K and total_questions come from the paper/state
  itself; the evidence dir is read from audit_state.evidence_dir:
    C1  audit_state.batches_done covers 1..K            (every planned batch closed)
    C2  set(ledger.entries.keys()) == {1..total_questions}   (no question unreviewed)
    C3  every entry.status in {verified, regenerated}        (none pending/absent)
    C4  single-mode entry ⇒ answer_unique == True             (B-UNIQUE ran)
        multi-mode  entry ⇒ answer_set_verified == True       (A-MSQ-KEY ran)
    C5  factual entry (GA/CA section OR factual-option flag) ⇒ len(fact_sources) >= 1
        AND every fact_source names a SAVED file under evidence/facts/ that EXISTS
        and is non-empty                                     (B-FACT / RA-11)
    C6  figural entry ⇒ 'image' stamp present AND the montage file it names EXISTS
        under evidence/montages/ and is >= EVIDENCE_MIN_BYTES (a real raster, not a
        0-byte touch); table/chart/omml entry ⇒ 'recompute' stamp present AND the
        recompute-trace file it names EXISTS under evidence/recompute/ and is
        non-empty                                            (RA-4 / RA-19)
    C7  COVERAGE TOTALS (belt-and-suspenders vs a ledger that under-counts the
        paper): #entries with an 'image' evidence stamp == #inline images physically
        in the docx; #recompute-stamped == #tables+charts+OMML expressions present;
        #fact-verified entries == #factual entries. A shortfall means an artefact in
        the paper was never viewed/recomputed/verified — SHIP is blocked.
  SUCCESS prints:
    COMPLETION-GATE: PASS (Q reviewed=[tq]/[tq], facts sourced=[F], artefacts
    stamped=[V], evidence files present=[E])
  FAILURE prints, per failed assertion, the Q-numbers involved (MANDATE-0 safe:
    numbers + codes only, never content or the fact/URL text) and exits non-zero.

  Without --audit-state, --final behaves exactly as v2.5 (Part A only). BUT Phase 3
  (§4 S4-4 STEP 1) NOW REQUIRES the --audit-state form: a bare --final is no longer
  sufficient to certify (MANDATE D + MANDATE B). This is the single change that makes
  a skipped Phase 2 fail LOUDLY instead of shipping false-clean.

  WHY EVIDENCE FILES, not just booleans (FIX F): the ledger is written by the same
  model the gate polices. A presence-only gate would upgrade "say clean" to
  "fabricate a stamped ledger" — better, but still self-attested. Binding each stamp
  to a durable artefact (a montage PNG that must exist for a VIEW, a saved search
  result for a FACT, a recompute trace) means faking a pass requires producing every
  montage, every saved source, and every trace — i.e. performing the audit. That is
  the point at which faking and doing converge (§19 notes the residual).

## S5-2 — The Part-A gate catalogue

  Each row: GATE — checks — exam-agnostic SOURCE of the expectation — Step-7
  contract re-verified — auto-fixable? (CP = content-preserving, done in Phase 1;
  RG = needs regeneration, done in Phase 2; HALT = structural, halts if unfixable).

  STRUCTURE & SEQUENCE
  | A-COUNT    | #question blocks == total_questions                     | blueprint.total_questions          | R7  | RG/HALT |
  | A-SEQ      | Q-numbers are exactly {1..total_questions}, no gaps      | blueprint.total_questions          | R7  | RG      |
  | A-MONO     | Q-numbers strictly increasing in document order         | —                                  | R7  | CP      |
  | A-SECCOUNT | each section holds exactly its q_range's count of Qs     | blueprint.sections[].q_range       | R18 | RG      |

  OPTIONS  (v1.4: SKIPPED for a NAT question — answer_type=='numerical', registry options_by_q==0;
            A-NAT-NOOPT verifies those render zero options instead)
  | A-OPTN     | every Q has exactly OPTIONS_COUNT options (NAT Qs skipped)| section_rules options_count        | R4  | RG      |
  | A-OPTLABEL | option labels match option_label_format (default "n.  ")| section_rules option_label_format  | R10 | CP      |
  | A-OPTORDER | options appear in document order 1..OPTIONS_COUNT        | —                                  | R13 | CP      |
  | A-OPTUNIQUE| options distinct within a Q (strip+casefold)            | —                                  | R4  | RG      |

  BODY HYGIENE
  | A-SECHDR   | no section-heading paragraph in the body — KEYWORD form ("section"/"part N"/rule chars) AND (v1.5) SECTION-NAME form: a standalone body paragraph equal to a declared section name (blueprint src['sections']); scans all body paragraphs, not only within blocks | blueprint sections + (universal ban) | R8  | CP      |
  | A-ANSKEY   | no answer key / correct-marker / hint anywhere (incl. SET-valued "Q.1 → 1,2,4" AND NAT numerical "Q.5 → 47" leaks, not just single-digit) | (universal ban) | R5  | CP      |
  | A-FONT     | every run Calibri (font.name in {Calibri, None})        | section_rules (default Calibri 11) | R24 | CP      |
  | A-BLANKSEP | ≥1 blank paragraph separates consecutive Q blocks       | —                                  | R13 | CP      |
  | A-QNFIRST  | each block OPENS with its "Q.<n>" paragraph             | (Q.N-FIRST contract)               | R14 | CP      |
  | A-MSQ-INSTR| (multi only) the select-instruction ("(One or more options may be correct)" / "(Select TWO)" / localized) is present INSIDE the Q.<n> stem line — no separate instruction paragraph (would break A-QNFIRST), no paper-level instructions page | section_rules msq_instruction + blueprint answer_cardinality | R14 | RG (re-emit stem with instruction on the Q.N line) |
  | A-NAT-NOOPT| (numerical only) every Q the registry marks 0-option (NAT) renders ZERO option paragraphs | registry options_by_q + blueprint nat_present | R4/R13 | RG (re-emit as a 0-option NAT block) |
  | A-NAT-INSTR| (numerical only) the numerical-entry instruction (nat_instruction / localized) is present INSIDE the Q.<n> stem line; per-section observed count matches the blueprint NAT allocation | section_rules nat_instruction + blueprint expected_nat_by_section | R14 | RG (re-emit stem with instruction on the Q.N line) |

  LINKED-STIMULUS SELF-CONTAINMENT
  | A-STIMORPHAN | every linked member carries its stimulus in its own block; no "Q.x and Q.y" cross-ref | registry rc_manifests + di groups + re-derived cues | R-LINKED | CP* |
       *CP when the stimulus exists elsewhere in the group (embed a copy, Model A);
        RG only if the stimulus itself is absent/defective.

  MATCH-GRID RENDERING
  | A-MATCH-TABLE | every Axis-2 MATCH question (re-derived by the shared S6-1b classifier) renders its List columns as a real <w:tbl>; a match rendered as text lines or space/tab pseudo-columns is a format-fidelity defect (MATCH counted present, skill un-rehearsed) | re-derived axis2 (S6-1b) + block.tables | S7-3 / G-MATCH-TABLE | CP (rebuild List body as a real table) |

  RENDERING FIDELITY (the gates that catch "faked-as-text/raster" defects)
  | A-UNDERLINE | underline-class Q carries a real <w:u> run; no "(underlined: X)" | section_rules (sentence_embedded_underlined) + stem cue | R-UNDERLINE | CP |
  | A-MATHRASTER| no built-up math shipped as a raster image (see S5-3)    | section_rules OMML_required + math cues | R-MATH-OMML | CP/RG |
  | A-FRAC      | no slash/caret ASCII built-up math in a math-context stem| section_rules OMML_required        | R-MATH-OMML | CP |
  | A-OMML      | every <m:f> has non-empty numerator AND denominator; no year-range "YYYY/YY" stacked fraction; OMML floor ≥1 if any subtopic OMML_required | section_rules OMML_required | R-MATH-OMML | CP |

  FIGURAL DECOMPOSITION
  | A-FIGCOMP  | v2.4 image_role-aware: each figural Q is structured per its image_role variant. stem_and_options (default): problem image(s) + 1 image/option, single-column, 1 per line, bound 1:1 to labels; no composite panel; no "Figure k" dummy-text option. stem_only (v2.4): ≥1 problem image + TEXT options — option-image arm SKIPPED. options_only (v2.4): ≥n option images, no problem image required. FIGURAL-NAT (answer_type=='numerical', options_by_q==0): treated as stem_only — problem image(s) only with ZERO option images. All variants: single-column/no-composite/300-DPI/named-image discipline checked. image_role read from section_rules PYQ_IMAGE_ANALYSIS per subtopic_id | registry figural_manifests + section_rules PYQ_IMAGE_ANALYSIS + figural stem cues + registry options_by_q | R-FIGURAL | CP/RG |

  STEM↔OPTION COHERENCE (machine layer; semantic layer in §6)
  | A-OPTREF   | a stem that references a terminal/escape option ("no error→last option", "None of these", "All of the above", "Both…and…", "Neither…nor…") actually CONTAINS that option, at the named position; a "pick-the-segment" layout does not carry a "no error" escape without a real "No error" option | section_rules none_of_above_permitted (S3-12) + wrong_option_structure/fixed_set (S3-13) | R-OPTREF | RG |

  INTEGRITY
  | A-ZIP      | document.xml present; every image rId resolves to an existing part | —                          | (structural) | HALT |
  | A-ENCODING | no U+FFFD replacement characters                        | —                                  | (structural) | RG  |
  | A-SCRIPT   | non-ASCII regional script present ONLY if language permits it (else copy-paste corruption) | section_rules language (RA-10) | (structural) | RG |
  | A-INTEGRITY| (P0.5 pre-flight) every JSON input parses + carries its required top-level keys; audit.py ast-parses + passes the hardened self-test; section_rules non-empty with EXAM_STRUCTURE header | (structural) | HALT (repair audit.py only) |

  CROSS-MOCK DEDUP
  | A-DUP      | no stem in mock N exact-matches OR near-matches (Jaccard ≥ J_FAIL) a stem from a PRIOR mock in registry.stem_texts (self-excluding mock N via --mockN); image MD5/pHash not reused from a prior mock | registry stem_texts/question_hashes/image_phashes/content_tracking | R2/R3 | RG |

  HEADER
  | A-HEADER   | NO non-blank paragraph before Q.1 — the paper is questions-only; any title/info/scoring/cover block is a defect → STRIP it (CP-HEADER-STRIP). Dormant only if section_rules EXAM_STRUCTURE declares paper_header_block | section_rules CATEGORY-C (paper_header_block) | R8b/G-PREQ1 | CP |

  DERIVED-KEY GATES (run ONLY after §11 builds Step 8's independent key; advisory→fix)
  NOTE: these are computed by CLAUDE from the §11 derived key — the machine
  script never receives a key (none is delivered, S0-1), so it does not emit them.
  | A-KINT     | derived key per Q is a single int in 1..OPTIONS_COUNT (single) OR a non-empty proper subset of 1..OPTIONS_COUNT (multi); total_questions entries | section_rules options_count + blueprint answer_cardinality | —    | n/a (derivation check) |
  | A-KBAL     | per-section answer-option balance within the band (SINGLE-mode Qs only; multi AND numerical excluded) | OPTIONS_COUNT + per-section counts | — | RG (rotate distractor) |
  | A-KPAT     | no same-answer run ≥ RUN_MAX across the SINGLE-mode Qs in Q1..QN incl. cross-section boundaries (multi AND numerical excluded) | RUN_MAX=3 (framework const) | — | RG (rotate distractor) |
  | A-MSQ-KEY  | (multi only) re-derived set S is a non-empty PROPER subset of 1..OPTIONS_COUNT (1≤|S|≤n−1; |S|=msq_k when msq_k_mode=fixed); no banned AOTA option under multi (msq_allow_aota) | blueprint answer_cardinality + msq_k_mode/msq_k + section_rules msq_allow_aota | RA-12 | RG (re-form the set) |
  | A-NAT-ANSWER| (numerical only; Claude-derivation) re-derived VALUE is uniquely determined by the stem, form-matched to nat_answer_type (integer⇒integral; real⇒within ca_range, lo≤hi); 0/negative/fractional valid; value does not leak | blueprint nat_answer_type/nat_tolerance | RA-12 | RG (disambiguate the stem / re-derive the value) |

  SUB-CODES: a parent gate may emit refinement sub-codes that sharpen the locator —
  A-STIMORPHAN-XREF (a "Q.x and Q.y" cross-reference), A-UNDERLINE-FAKE (a
  "(underlined: X)" annotation), A-OMML-YEAR (a year-range rendered as a stacked
  fraction), A-OMML-FLOOR (OMML_required declared but zero <m:oMath>), A-FRAC-SLASH
  (a slash fraction in a math-context stem), A-MATHRASTER-VIEW (non-canonically-named
  images to VIEW in Part B), A-FIGCOMP-LINE (two images on one line). A "-VIEW"/
  "-SLASH"/"-YEAR"/"-FLOOR" sub-code is a WARN routed to Part B/§7; the others are
  FAILs of their parent gate.

## S5-3 — A-MATHRASTER: robust, exam-agnostic, view-backed (the naming-gap fix)

  Step 7's G-MATH-RASTER authenticates legitimate rasters by an image NAME contract
  (^q\d+_(problem|opt\d+|stim)). In the wild, the docx emitter (python-docx) often
  overwrites image names with generic defaults ("Picture 1"…"Picture k"), so a NAME-
  ONLY gate would FALSE-FAIL every legitimate figure. Step 8 therefore does NOT rely
  on the emitter naming. A-MATHRASTER works in TWO tiers:
    TIER 1 (machine, in audit.py): FAIL only on a HIGH-CONFIDENCE math-raster signal —
      an inline image whose part/docPr name carries an explicit math token
      (_e\d, _eqn, _expr, _frac, _math) OR an image that sits in a block whose stem
      is math-context (OMML_required subtopic / built-up math cue) AND is NOT one of
      the manifest's figural_qs AND is NOT a DI chart. All OTHER non-canonically-named
      images are emitted as a WARN LIST for Tier 2 (not a FAIL — avoids blocking on a
      mis-named-but-legitimate figure).
    TIER 2 (§7, Part B view): every image on the WARN list (and every image generally)
      is VIEWED. If a viewed image is in fact a rasterised algebraic expression, it is
      a defect → CP-MATHOMML (re-render as OMML, drop the raster). If it is a genuine
      figure that was merely mis-named, CP-IMGNAME renames it to the canonical
      q{N}_problem / q{N}_opt{i} / q{N}_stim contract so future steps and any re-run of
      the name-contract gate pass. The VIEW is the authority (RA-4); the name contract
      is a fast diagnostic, never the sole verdict.
  This makes A-MATHRASTER both provenance-aware AND robust to emitter naming, on every
  exam and every generator — no false-FAIL on legitimate figures, no escape for a real
  math raster.

## S5-4 — Zero-Warning Policy (= Step 7 S12-0)

  Every fixable WARN is a blocker (same as FAIL). Fix it, re-run, iterate. No
  advisory carries forward to Step 9 or the next mock. The only WARNs that may be
  ACCEPTED (documented, not fixed) are genuinely-not-fixable diagnostics (e.g. a
  registry that lags such that cross-mock dedup is partial — recorded as a §15
  limitation), never a content or rendering defect.

## S5-5 — Part A is NOT the whole audit (the blind-spot contract)

  Part A proves STRUCTURE and FORMAT, not CONTENT TRUTH. It cannot prove a fact is
  current, that a figure's transformation is correct, that exactly one option is
  defensible, that a DI table's numbers actually yield the keyed answer, or that an
  OMML expression computes correctly. Those are Part B (§6) and the §7 deep audit,
  which carry equal force: a paper that passes Part A but fails Part B/§7 is NOT
  certifiable (no SHIP). Each Part-A gate's blind spot is explicitly covered by a
  named Part-B / §7 check (§6 and §7 cross-reference the gate they backstop).
  v2.6 — AND: because Part B / §7 are Claude-driven, they were the ONLY skippable
  half. The COMPLETION GATE (S5-1A) removes that: a Part-B/§7 check that did not run
  leaves no stamped-and-evidenced ledger entry, so C2–C7 fail and delivery is
  blocked. "Passed Part A, skipped Part B" is now a LOUD failure, not a silent ship.

# ════════════════════════════════════════════════════════════════════════
# §6 — PART B: SEMANTIC REVIEW (every question; zero sampling; batched)
# ════════════════════════════════════════════════════════════════════════
#   Part B is the reasoning half — the checks no regex can prove. It runs per
#   Phase-2 batch (≤10 Q), every question, zero sampling (RA-3). It is organised by
#   UNIVERSAL question CLASS (derived at runtime from the question's format +
#   wrong_option_structure in section_rules), NOT by exam-specific sub-types — so
#   the same checklist audits an SSC antonym, a GATE numerical-answer, a NEET
#   assertion-reason, or a UPSC match-the-column. No exam content is named here.
#   v2.6 — every check writes a STAMPED ledger entry (§9-1); B-FACT additionally
#   SAVES its search result to evidence/facts/ and names it in the entry. The
#   COMPLETION GATE (S5-1A) reads these — an un-run check leaves no entry and fails
#   certification.

## S6-0 — Extraction protocol (do this for every question before judging it)

  1. MERGE OMML + text: extract <m:t> (math) interleaved with <w:t> (text) in
     document order, so a math-bearing or pure-OMML stem reads correctly. Never
     judge a stem "empty" from p.text (RA-4).
  2. Read the FULL stem + the FULL text of all OPTIONS_COUNT options. Two options
     may share a long prefix and differ only at the end — read to the end.
  3. Build the per-question artefact map (from P6 index): attached tables, inline
     images (with media files), OMML nodes, <w:u> runs.
  4. Classify the question (S6-1) from section_rules (format + wrong_option_structure
     + stem cues). The class selects which checklists apply.
  5. "shown below"/"as given"/"as shown" in a TEXT stem (seating, directions) is
     NORMAL phrasing — confirm a missing-artefact suspicion against the actual
     artefact map before flagging (avoids false A-STIMORPHAN positives).
  6. v2.5 — TAG THE AXES: run `tag_axes(qa)` + `derive_is_negative(qa)` (S6-1b) on the
     extracted `{stem_raw, options, image_role, linked_group_id, blank_pos, is_msq}`, and
     store axis1/axis2/axis3/is_negative on this question's §9 ledger entry. This is the
     INDEPENDENT re-tag the S6-6 format-distribution audit consumes. Inert-safe: harmless
     when blueprint has no axis_schedule (the S6-6 audit simply never reads them).
  7. v2.6 — OPEN the §9 ledger entry for this q at the START of review (status
     'pending'), and CLOSE it to 'verified'/'regenerated' only when every applicable
     §6 + §7 check has run and its evidence is saved. A question left 'pending' fails
     S5-1A C3 — so a half-reviewed question can never certify.

## S6-1 — Universal question CLASSES (runtime-derived; exam-agnostic)

  Derived from section_rules format + wrong_option_structure.type + stem cues.
  A question may carry more than one class facet (e.g. LINKED + COMPUTATIONAL).

  C-COMPUTATIONAL : numeric/quantitative answer from a computation (format TEXT/DI,
                    quantitative number ranges). Audited by re-solving (B-SOLVE)
                    and tracing every distractor to a named error path (B-DISTRACT).
  C-FORMAL-LOGIC  : answer from a fixed formal procedure with a FIXED option set
                    (wrong_option_structure.type == fixed_set) — syllogism, data-
                    sufficiency, assertion-reason, cause-effect, statement-conclusion,
                    inequality chains, etc. Audited by executing the formal rule and
                    confirming the fixed option order matches fixed_option_texts.
  C-FACTUAL       : answer is a fact (general awareness, science recall, current
                    affairs, computer/domain fact). Audited by WEB-VERIFICATION of the
                    keyed fact AND every option (B-FACT); distractors must be real,
                    same-domain, verifiably-wrong facts.
  C-VOCAB-ITEM    : answer about a target ITEM (synonym/antonym/idiom/one-word/
                    spelling/homonym/word-meaning). Audited for single-context-validity
                    of the key, no-context-validity of distractors, real underline if
                    'sentence_embedded_underlined', and presentation variety (B-PRESENTDUP).
  C-GRAMMAR       : sentence transformation/correctness (error-spotting, sentence-
                    improvement, active/passive, narration, fill-in-sentence, jumble).
                    Audited by re-deriving the correct form; each distractor violates
                    exactly one rule; escape-option coherence (B-OPTREF-SEM).
  C-LINKED        : member of a shared-stimulus group (RC/cloze/DI/puzzle). Audited
                    for stimulus self-containment (already A-STIMORPHAN) PLUS
                    derivability-from-stimulus-alone (B-PASSAGE) and per-blank/
                    per-member coverage.
  C-FIGURAL       : answer is a figure or depends on a figure/diagram. Audited entirely
                    in §7 (view every image; transformation true; key unique).
  C-MATRIX/MATCH  : match-the-column / matrix. Audited in §7 (parse grid; re-derive
                    every pair; one fully-correct option).

  Class detection reads section_rules; an unknown format defaults to the closest of
  the above by wrong_option_structure.type, and the generic checks (S6-2) still apply.

## S6-1b — AXIS CLASSIFIER v1.0 (COPIED VERBATIM from Step 5 — v2.5)

  The three-axis format audit (S6-6) is only valid if generated questions are classified
  by the EXACT SAME functions Step 5 used on the PYQ papers. These functions are copied
  BYTE-IDENTICAL from Step 5's `AXIS CLASSIFIER v1.0` block — never re-implemented, never
  "improved" here. If Step 5's classifier changes, this copy MUST be updated to match.
  They read only fields Step 8 already extracts per question (S6-0): the rendered stem
  (`stem_raw`), the option texts (`options`), `image_role`, `linked_group_id`, `blank_pos`,
  and `is_msq` — so Step 8 re-derives the axes INDEPENDENTLY from the shipped paper.

  ```python
  import re

  AXIS2_CLASSES = ['LINKED', 'ASSERTION_REASON', 'MATCH', 'SEQUENCE', 'STATEMENT',
                   'FILL_BLANK', 'ODD_ONE_OUT', 'DIRECT']   # ladder order == precedence

  # v2.7.4 FIX C PROPAGATION (byte-identical to Step 5 v2.24.6) — see Step 5's
  # _looks_like_table_stimulus docstring for full rationale. Was a naive substring
  # match ('|' in stem or 'table' in stem.lower()) that false-positived on any word
  # merely containing "table" (vegetable, acceptable, notable, ...).
  _TABLE_WORD_RE = re.compile(r'(?i)\b(table|tabulated|following data|dataset)\b')
  def _looks_like_table_stimulus(stem):
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

  # v2.5 — is_negative re-derivation for the negative-rate WARN. MUST match Step 5 EC-12
  # BYTE-FOR-BYTE so the target (Step 6, from Step 5) and the realized rate (here) are counted
  # the SAME way. Step 5 EC-12 is: bool(re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b',
  # full_stem)) — UPPERCASE only (exam convention capitalises the negative marker), no re.I,
  # exactly these 5 terms. Do NOT broaden it (case-folding / extra terms) or the rates diverge
  # and every window fires a false WARN. SOFT signal only; negativity is orthogonal to Axis-2.
  def derive_is_negative(q):
      s = (q.get('stem_raw') or q.get('stem') or '')
      return bool(re.search(r'\b(NOT|INCORRECT|EXCEPT|FALSE|WRONG)\b', s))
  ```

  USAGE (in S6-0, once per question, from the docx parse — NOT from any Step-7 sidecar):
  ```python
  qa = {'stem_raw': stem_text, 'options': option_texts, 'is_msq': (answer_cardinality == 'multi'),
        'image_role': image_role_for_q, 'linked_group_id': linked_group_id_for_q,
        'blank_pos': blank_pos_for_q}
  tag_axes(qa)                          # → qa['axis1'], qa['axis2'], qa['axis3']
  qa['is_negative'] = derive_is_negative(qa)
  # stored on the §9 ledger entry (S9-1): axis1, axis2, axis3, is_negative.
  ```

## S6-2 — Generic checks (EVERY question, every class)

  B-SOLVE (§11): independently solve/derive the intended answer from the stem +
     attached artefacts ALONE. Unsolvable, or answer not among the options → defect.
     v1.2: for a multi (MSQ) question the derivation yields a SET S of correct option
     positions (every option independently judged correct/incorrect from first
     principles); S not derivable, or any in-set value not among the options → defect.
     v1.4: for a NAT (numerical) question the derivation yields a VALUE (no options to
     match against); unsolvable, or a value the stem does not uniquely determine → defect.
     The value is compared NUMERICALLY within tolerance (ND13) — OMML fractions parsed to a
     rational, units stripped — never by string equality; integer NAT = exact, real NAT =
     within ca_range.
  B-UNIQUE (RA-12 / R-ANSWER): answer_type/answer_cardinality-parameterised (re-derived from blueprint).
     SINGLE: exactly ONE option is defensible under EVERY reasonable reading. A second
     defensible option (ambiguous relation, contested convention presented as two option
     forms, two rules each yielding a listed option, rounding that makes two options
     "match") → defect → §8 disambiguate or replace the colliding option. MULTI: the
     re-derived set S must satisfy RA-12 multi — a non-empty proper subset (1≤|S|≤n−1,
     |S|=msq_k when fixed) with every in-set option defensible; if the paper's rendered
     option set makes an out-set option also defensible, that is the MULTI ambiguity
     defect. NUMERICAL (v1.4): the re-derived VALUE must be uniquely determined by the stem
     — two defensible values under a fair reading (ambiguous rounding, under-specified
     figure, missing unit) is the NAT analogue of the two-defensible-answers defect → §8
     disambiguate the stem. Checked for EVERY question, no exception.
  B-DISTRACT: every OUT-set option is INDEFENSIBLE under any reasonable reading, and
     traces to a named error path appropriate to the class (computational slip /
     wrong-formula / converse-error / near-miss vocab / one-rule grammar violation /
     adjacent-but-wrong fact). SINGLE: the other (OPTIONS_COUNT − 1) options. MULTI: the
     (OPTIONS_COUNT − |S|) options not in S. A distractor that is "sort of right" is a
     B-UNIQUE failure in disguise (single: a 2nd defensible option; multi: a borderline
     out-set option that should arguably be in S). NUMERICAL (v1.4): N/A — a NAT question
     has no options, hence no distractors to adjudicate (the analogue "wrong values students
     compute" lives in Step 9's common-pitfalls, not in the audited paper).
  B-STEMOPT (R17): options are grammatically + logically consistent with the stem;
     option-length parity (no single option wildly longer/shorter as an answer tell);
     no answer leakage from stem to options.
  B-OPTREF-SEM (R-OPTREF): the SEMANTIC half of A-OPTREF — the escape/terminal option
     the stem references is not only PRESENT (machine) but CORRECT in meaning and
     position, and the instruction template matches the option structure. Escape tokens
     are read from section_rules (RA-9), never hardcoded.
  B-FACT (RA-11 — LIVE, EVIDENCE-SAVED): every current-affairs / static-GA fact and every
     factual option is web-verified at audit time. The search query necessarily contains
     the fact (permitted to the search tool only — MANDATE 0). v2.6: SAVE the raw result
     (query + URL + retrieval-time + snippet) to evidence/facts/q{n}_*.json and record its
     path in ledger.entries[q].fact_sources[]. S5-1A C5 verifies the file exists — a bare
     URL string no longer certifies. Never certify a fact from memory.
  B-LEAK (inter-question): a question's correct numeric/fact answer does not appear as a
     GIVEN quantity/fact in another question's stem in the same mock (cross-question
     leakage). Checked mock-wide at Phase 3 using the ledger's recorded answers. v1.2:
     for a multi question EVERY value in the re-derived set is checked (the ledger stores
     answer_fact_values as a list), not just one — a leaked member is still a leak. v1.4:
     for a NAT question the re-derived VALUE is checked the same way (a leaked numerical
     answer appearing as a given elsewhere is a leak), compared numerically within tolerance.

## S6-3 — Class-specific checks

  C-COMPUTATIONAL:
    [ ] Re-solve from scratch; keyed value is exact (or stem says "rounded to k dp"
        AND options are consistent with that rounding).
    [ ] Every distractor = a specific, nameable error (sign slip, wrong formula,
        unit confusion, off-by-one) — listed in the ledger, not invented noise.
    [ ] No two computational questions in the mock share the SAME archetype AND the
        SAME seed values (observable scenario dup — B-SCENARIODUP).

  C-FORMAL-LOGIC:
    [ ] Execute the formal rule (Venn/traversal/causal/sufficiency) independently;
        keyed option follows; no second option follows.
    [ ] Option set EXACTLY matches wrong_option_structure.fixed_option_texts in the
        EXACT order section_rules specifies — never rephrased, never reordered.
    [ ] For "only one of the conclusions holds" cases, an "Only I"/"Only II"-type
        singleton option exists (not only combined options) — read the permitted set
        from section_rules.

  C-FACTUAL (RA-11 — live web-verification, never memory):
    [ ] Web-verify the KEYED fact with a citable, current source; SAVE URL+date+snippet
        to evidence/facts/ and record the path in the ledger (never in chat — MANDATE 0).
    [ ] Web-verify EVERY option is a real, same-domain fact; a distractor must be a
        genuine adjacent fact, not an invented one (each saved likewise).
    [ ] Currency: a fact that has changed since section_rules' analysis window is
        treated as current-affairs and re-verified; a stale "current" fact → defect.
    [ ] A fact that cannot be sourced → defect → regenerate with a sourceable fact.
    [ ] Minimum/permitted current-affairs count + recency window, IF section_rules
        declares one, is checked; else skipped (RA-9 — never a hardcoded count).

  C-VOCAB-ITEM:
    [ ] Key is correct in the sentence's CONTEXT; no distractor is a valid answer in
        ANY context.
    [ ] If 'sentence_embedded_underlined': the target is a real <w:u> run (already
        A-UNDERLINE) AND it is the correct span.
    [ ] Presentation variety (B-PRESENTDUP, observable form of G-FORMATDUP): two
        same-concept vocab questions must not share BOTH stem-format AND distractor
        strategy AND be adjacent. Read the family/menu from section_rules; this is the
        OBSERVABLE re-derivation (the concept_map is not delivered — §10).
    [ ] Cross-mock: the target item not used in a prior mock (registry
        content_tracking.vocab_words_used) — A-DUP backstop.

  C-GRAMMAR:
    [ ] Re-derive the single correct transformation/correction; the source sentence is
        itself correct where the task assumes it.
    [ ] Each distractor violates exactly one rule; meaning is preserved where the task
        requires (narration/voice).
    [ ] Escape option ("No improvement"/"No error") present where the template
        promises it, and genuinely correct in ~its expected share (B-OPTREF-SEM).

  C-LINKED (in addition to A-STIMORPHAN structural pass):
    [ ] Every member is answerable from THIS member's embedded stimulus ALONE (no
        outside knowledge; no reference to another question) — B-PASSAGE.
    [ ] The keyed answer is derivable from the stimulus, not contradicted by it; the
        passage↔question linkage is correct (a mis-linked passage makes every member
        wrong — re-solve each member from its own embedded stimulus).
    [ ] CLOZE: every blank covered by exactly one member; no blank uncovered; no blank
        asked twice; the numbered blank the member asks for actually exists in the
        embedded passage.
    [ ] Each member's sub-skill is distinct (the CLASS-4 exception: shared stimulus is
        allowed, but members must not be the same question twice).

## S6-4 — Allocation, mandate & intra-mock dedup (observable; verified per S6 + Phase 3)

  B-ALLOC: tally questions per subtopic (mapping each question to its subtopic_id by
     matching its content to section_rules patterns + the manifest) and compare to
     blueprint mock_obj subtopic_allocations q_count. Any subtopic count ≠ its
     blueprint q_count → defect (over → regenerate the extra as a different needed
     subtopic; under → the missing subtopic is absent → regenerate). SECTION totals
     are A-SECCOUNT (machine); PER-SUBTOPIC is this manual mapping (the concept_map is
     not delivered, so the mapping is re-derived).
  B-MANDATE: every subtopic in manifest.mandatory_every_mock appears ≥1× in the mock;
     no two members of any manifest.alternation_groups co-occur in the mock. Read from
     the manifest (RA-9).
  B-SCENARIODUP (observable G-CONCEPTDUP): no two questions in the mock are the same
     scenario (same computation on the same seed values; same fact in different
     wording; same vocab target; same figural transformation). Re-derived from the
     rendered content + the ledger, since the concept_map is not delivered.
  B-PRESENTDUP (observable G-FORMATDUP + R19): no two same-family questions share BOTH
     stem-format AND distractor strategy; no contiguous run > 2 of the same
     presentation family; a subtopic's N questions are distributed, not clustered.
  These four are TALLY/scan checks completed across the whole mock; per-batch they are
  populated into the ledger, and they are FINALISED at Phase 3 (when every question has
  been classified). A failure → §8 regeneration (never count reduction — RA-8).

## S6-5 — Difficulty (advisory unless section_rules makes it hard)

  B-DIFF: estimate difficulty per question using blueprint.difficulty_labels (tag every
     estimate [estimate]) and compare the per-section distribution to blueprint difficulty_schedule[N]. Interleaving:
     no excessively long run of Hard (or of Easy) within a section. v1.2: mirror Step 0
     E-9 — a multi (MSQ) question carries an additional difficulty-load term (selecting an
     exact SET is harder than picking one option), so an MSQ should not be estimated below
     the band its single-answer analogue would receive; treat this as advisory input to the
     estimate, not a separate gate. A shortfall is a generation-quality FINDING logged in
     the report; it blocks SHIP only if section_rules/blueprint marks the difficulty mix as
     a hard requirement (RA-9).

## S6-6 — Format distribution / THREE-AXIS audit (advisory; mirrors S6-5 — v2.5)

  The mirror of B-DIFF for FORMAT. Step 8 has re-tagged every shipped question with the
  Step-5 AXIS CLASSIFIER v1.0 (S6-1b) and stored axis1/axis2/axis3/is_negative on the ledger.
  This section aggregates the realized per-section distribution over the current 10-mock
  WINDOW (registry.axis2_audit, Step 8's independent tally) and compares it to the blueprint
  axis_schedule target. Like B-DIFF, a shortfall is a generation-quality FINDING logged in the
  report; it blocks SHIP only if section_rules/blueprint marks the format mix a HARD requirement.

  INERT when blueprint has no axis_schedule (pre-v1.23) OR a section's schedule status != 'ok'.
  The audit FIRES ONLY AT WINDOW CLOSE (this mock is the last of its window), from the FINAL
  fixed docx — a partial mid-window mock only ACCUMULATES (Phase 3), it does not yet judge.

  ```python
  def axis_window_is_closing(N, window, total_mocks):
      """True iff mock N is the last mock of its 10-mock window (a full window boundary,
      or the final mock of the run when the last window is partial)."""
      if total_mocks is not None and N >= total_mocks:
          return True
      return (N % max(1, window)) == 0

  def _axis_tolerance(target):
      """decision 10: per-format window tolerance = ±1 OR ±15% of target, whichever is LARGER."""
      return max(1.0, 0.15 * float(target))

  def audit_axis2(section_name, sched, realized_counts, scale=1.0):
      """B-AXIS2 — per-section, per-format, per-window (advisory FINDINGS list).
         realized_counts = {AXIS2_CLASS: n} accumulated over the window (Step 8's tally).
         scale     = mocks_in_window / AXIS_WINDOW — scales band targets so a PARTIAL final
                     window (total_mocks not a multiple of the window) is judged fairly.
         band    : |realized − scaled_target| ≤ max(1, 15%·scaled_target)   → else FINDING
         guarantee: realized ≥ 1 over the window                            → else FINDING
         DIRECT  : floats — never audited (residual filler, decisions 5/10)."""
      findings = []
      if not sched or sched.get('status') != 'ok':
          return findings                                   # inert section
      band  = sched.get('axis2_window_target', {})          # {cls: per-FULL-window quota}
      guar  = sched.get('axis2_guarantee', [])              # [cls] must appear ≥1/window
      feas  = sched.get('guarantee_feasibility', {})        # pyq_covered|zp_only|unsatisfiable
      for cls, tgt in band.items():
          if cls == 'DIRECT':
              continue                                       # floats
          stgt = float(tgt) * scale                          # partial-window-scaled target
          have = realized_counts.get(cls, 0)
          if abs(have - stgt) > _axis_tolerance(stgt):
              findings.append(f"B-AXIS2 [{section_name}] band '{cls}': realized {have} vs "
                              f"target {stgt:.1f} (tol ±{_axis_tolerance(stgt):.1f}/window) — FINDING.")
      for cls in guar:
          if realized_counts.get(cls, 0) < 1:
              # An 'unsatisfiable' guarantee (no capable subtopic) was ACCEPTED as absent at
              # Step 6 — report it as expected-absent, not a defect (never fabricated).
              if feas.get(cls) == 'unsatisfiable':
                  findings.append(f"B-AXIS2 [{section_name}] guarantee '{cls}': absent — "
                                  f"no capable subtopic (accepted shortfall, not fabricated).")
              else:
                  findings.append(f"B-AXIS2 [{section_name}] guarantee '{cls}': 0 in this "
                                  f"window (expected ≥1; feasibility={feas.get(cls,'?')}) — FINDING.")
      return findings

  def audit_axis13(section_name, axis_key, per_paper_target, realized_counts, window):
      """B-AXIS1 / B-AXIS3 — realized stimulus/mechanism mix vs the Step-6 per-PAPER target,
         scaled to the window and checked within the same ±1/±15% tolerance. Advisory."""
      findings = []
      if not per_paper_target:
          return findings
      for cls, avg in per_paper_target.items():
          tgt  = float(avg) * window                         # window-scaled target
          have = realized_counts.get(cls, 0)
          if abs(have - tgt) > _axis_tolerance(tgt):
              findings.append(f"B-AXIS{axis_key} [{section_name}] '{cls}': realized {have} vs "
                              f"~{tgt:.1f}/window (tol ±{_axis_tolerance(tgt):.1f}) — FINDING.")
      return findings

  def audit_axis_negative(section_name, sched, neg, total):
      """B-AXIS-NEG — negative-polarity rate is a SOFT target (decision 12): WARN only."""
      if not sched or sched.get('status') != 'ok' or total <= 0:
          return []
      rate_tgt = float(sched.get('negative_rate', 0.0))
      if rate_tgt <= 0:
          return []
      cur = neg / total
      if abs(cur - rate_tgt) > 0.10:                         # 10-point soft band
          return [f"B-AXIS-NEG [{section_name}]: negative rate {cur:.0%} vs target "
                  f"{rate_tgt:.0%} (soft ±10pt) — WARN."]
      return []

  def cross_check_step7(section_name, s8_axis2, s7_sections):
      """Consistency signal (decision A): Step 8's independently re-derived Axis-2 counts vs
      Step 7's self-reported registry.axis2_window. A large drift means the paper's actual
      structure diverged from the variant Step 7 declared (a render-fidelity WARN, not a hard
      fail). Compares only where both have data."""
      s7 = (s7_sections.get(section_name) or {}).get('counts', {})
      if not s7:
          return []
      drift = sum(abs(s8_axis2.get(c, 0) - s7.get(c, 0)) for c in set(s8_axis2) | set(s7))
      s8_total = sum(s8_axis2.values()) or 1
      if drift > max(2, 0.20 * s8_total):                    # >20% aggregate divergence
          return [f"B-AXIS2 [{section_name}] render-drift: Step-8 re-tag differs from Step-7's "
                  f"declared counts by {drift} (>20%). Check RENDER-CONSISTENCY (Step 7 G4) — WARN."]
      return []
  ```

  HARD-vs-advisory (RA-9 parallel): every FINDING/WARN above is ADVISORY and logged in the
  report by default. It escalates to a SHIP-blocking defect ONLY when section_rules/blueprint
  declares the format mix a hard requirement (the same switch B-DIFF uses for difficulty).
  A window-distribution shortfall is never "fixed" by editing one mock — it is reported so the
  series self-corrects; a per-question RENDER mismatch (cross_check drift) points at the
  specific Step-7 fidelity bug to fix in the next generation.


# ════════════════════════════════════════════════════════════════════════
# §7 — VISUAL & STRUCTURED-CONTENT DEEP AUDIT (the no-gaps section)
# ════════════════════════════════════════════════════════════════════════
#   GOVERNING RULE (RA-4): a visual or structured artefact is audited ONLY by being
#   RENDERED-AND-VIEWED (images, charts) or PARSED-AND-RECOMPUTED (tables, matrices,
#   OMML). A check asserted from a filename, alt-text, p.text, manifest entry, or
#   "looks present" is VOID and the artefact counts as un-audited — which BLOCKS
#   delivery (RA-19, §18). This runs inside Phase-2 batches (STEP B). Exam-agnostic:
#   the qtypes/object-types/transformations come from section_rules
#   PYQ_IMAGE_ANALYSIS / PYQ_PASSAGE_STRUCTURE — never a hardcoded list.
#   v2.6 — EVERY view/recompute MUST leave a durable evidence artefact on disk (the
#   montage PNG that was viewed; the recompute trace) and record its path in the §9
#   ledger entry. S5-1A C6/C7 verify those files exist and are non-trivial. A stamp
#   with no backing file is treated as un-audited (RA-4).

## S7-1 — IMAGES & FIGURES — every single one rasterised and VIEWED

  COVERAGE: every inline image in the mock (from the P6 index), whether or not it is
  in registry.figural_manifests. A figural question is identified by (a) the manifest
  figural_qs, UNION (b) re-derivation from stem cues (section_rules figural cue set).
  An image present but unaccounted-for, or a figural cue with no image, is itself a
  defect.

  LAYER A — provenance & structure (machine; from §5 A-FIGCOMP + A-MATHRASTER Tier 1):
    [ ] every image rId resolves to an existing media part (A-ZIP).
    [ ] figural block is DECOMPOSED: problem image(s) + exactly one image per option,
        single-column, one image per line, each bound 1:1 to its option label; NO
        composite panel; NO "Figure k" dummy-text option (A-FIGCOMP / R-FIGURAL).
    [ ] no inline image is a rasterised algebraic expression (A-MATHRASTER; the VIEW
        in Layer B is the authority — S5-3).
    [ ] image naming: legitimate figures carry (or are renamed to) the canonical
        q{N}_problem / q{N}_opt{i} / q{N}_stim contract (CP-IMGNAME).

  LAYER B — actual visual content (VIEW every image; zero sampling; the authority):
    Render each question's problem + option images as a montage (PIL: problem top,
    options stacked/grid), SAVE the montage to evidence/montages/q{N}_montage.png, and
    VIEW it with the view tool. Record the montage path + 'rendered-and-viewed' stamp
    in the ledger (S5-1A C6 reads it). Per qtype (read from section_rules / figural
    manifest), verify:
    UNIVERSAL (all figural):
      [ ] resolution ≥ FIGURAL_DPI (300); no grey boxes, no clipping, no corrupted
          pixels; uniform per-option canvas; NO stem/caption/option-number/instruction
          baked into any raster (only intrinsic annotations — mirror-line endpoints,
          vertices, axis labels — belong inside).
      [ ] within-question: every option image is visually DISTINCT from the others
          (dHash Hamming separation); no two identical option figures.
      [ ] figure ↔ stem agreement: every value/label/landmark the stem references is
          present in the image and consistent with it; a label that contradicts the
          stem is a defect (regenerate figure AND dependent values together).
    TRANSFORMATION-SPECIFIC (the qtype set is read from section_rules; examples of the
    universal checks the framework applies to whatever types the exam declares):
      [ ] the stated transformation is ACTUALLY TRUE for the keyed option (a mirror is a
          real reflection about the stated line; a fold yields the keyed hole pattern; a
          series rule continues in exactly the keyed figure; an embedded target sits in
          the key WITHOUT rotation when rotation is barred; an odd-one-out has exactly
          one figure breaking the shared property; a net folds to the keyed solid).
      [ ] UNIQUENESS: no distractor also satisfies the rule (two valid figures = defect).
      [ ] DISTRACTORS verified to BREAK the rule (and, for embedded/odd-one-out, to NOT
          contain the target / to share the property).
      [ ] placement/rotation instructions the qtype requires are present in the stem
          (e.g. mirror line, "rotation is not allowed").
    CROSS-MOCK (RA-13): hash word/media/ directly (registry image_hashes may be empty);
      every image's dHash/MD5 is sufficiently distant from every registered prior-mock
      image; no figural concept repeats a prior mock's recorded pattern (registry
      content_tracking / figural_manifests).
    FIX: any Layer-B failure → re-render the figure(s) (or regenerate the question)
      under the Step-7 §10-S10-7/S10-8 contracts, then RE-VIEW (a re-rendered image is
      not certified until viewed again — re-save the montage). Stamp 'rendered-and-viewed'
      in the ledger with the montage path.

## S7-2 — TABLES & DI SETS — parsed to a grid and RECOMPUTED

  For every Word table (DI/caselet/matching) in the paper:
    [ ] it is a REAL <w:tbl> object — not plain-text columns faked with spaces/tabs
        (a text-grid masquerading as a table is a defect → rebuild as a real table).
    [ ] read it cell-by-cell into a structured grid; row/column headers + units are
        present and unambiguous.
    [ ] internal consistency: if a Total/Subtotal/Average row or column is shown,
        RECOMPUTE it from the cells and confirm it matches (a printed total that does
        not add up is a defect).
    [ ] SELF-CONTAINMENT (A-STIMORPHAN): for a linked DI set, the table is embedded in
        EVERY member's block (Model A), re-emitted as a real table object — not "the
        table above".
    [ ] RE-SOLVE every dependent question FROM THE TABLE'S OWN NUMBERS: confirm the
        keyed answer follows from the grid and is UNIQUE. A DI table whose values do
        not actually yield the keyed answer is the most dangerous table defect →
        regenerate table AND dependent answers together.
    v2.6: write the parsed grid + the recomputed totals/derivations to
    evidence/recompute/q{N}_table.txt and record the path + 'recomputed' stamp in the
    ledger for the table and each dependent question (S5-1A C6 reads it).

## S7-3 — MATRICES & MATCH-THE-COLUMN

  [ ] rendered as a real grid/table (S7-2 structural checks apply).
  [ ] option format matches the label scheme section_rules declares (e.g. letter-roman
      vs number-letter) — read, never assumed.
  [ ] RE-DERIVE every pairing independently; exactly one option has ALL pairings
      correct; each distractor contains ≥1 demonstrably wrong pairing (B-DISTRACT).
  [ ] no second option is also fully correct (B-UNIQUE).
  Stamp 'recomputed' with the evidence/recompute/ trace path.

## S7-4 — CHARTS / GRAPHS

  [ ] a stem that references a chart/graph has a REAL rendered image for it (a "chart"/
      "graph" keyword with no inline image is a defect).
  [ ] VIEW the chart (save the montage); axes, labels, legend, units, scale are present
      and consistent with the stem; data series are legible.
  [ ] SELF-CONTAINMENT: the chart image is embedded in every dependent member (Model A).
  [ ] RE-SOLVE every dependent question by READING VALUES off the chart; keyed answer
      follows and is unique (save the derivation to evidence/recompute/).
  Stamp 'rendered-and-viewed' (montage path) + 'recomputed' (trace path) for dependents.

## S7-5 — OMML MATHS — extracted from the math XML, RECOMPUTED, render-verified

  Text extraction is blindest here, so this is the deepest check.
    [ ] ROUTING (R-MATH-OMML): every built-up expression (stacked fraction, exponent,
        radical, trig-with-fraction) is native <m:oMath> — NOT a raster (A-MATHRASTER)
        and NOT slash/caret ASCII (A-FRAC). Scan inline images for math smuggled as a
        picture and the text stream for slash/caret fallbacks. (Observed in the wild:
        zero <m:oMath> in a paper that has a quantitative section is a live flag — math
        is hiding as ASCII or raster — resolve it, never wave it past.)
    [ ] STRUCTURE (A-OMML): every <m:f> has a non-empty numerator AND denominator; no
        year-range "YYYY/YY" rendered as a stacked fraction (use an en-dash); radicals/
        scripts well-formed; the OMML floor (≥1 <m:oMath> when any subtopic is
        OMML_required) holds.
    [ ] SEMANTICS: reconstruct each expression FROM THE OMML TREE (not p.text), and
        RECOMPUTE the question; the math is correct AND the keyed option is the unique
        result. A perfectly-rendered fraction that makes the answer ambiguous is still a
        B-UNIQUE defect.
    [ ] RENDER-VERIFY: where structure is subtle, rasterise the page region and VIEW it
        to confirm it displays as intended (save that raster to evidence/montages/).
    FIX: a math defect → CP-MATHOMML re-render via the Step-7 §10-S10-4 add_math_stem /
      emit_math_inline path (interleave <m:oMath> with the stem text) and drop any
      raster/ASCII; if a flagged image was a genuine figure mis-named with a math token,
      re-emit it canonically (CP-IMGNAME). Stamp 'recomputed' (+ 'rendered-and-viewed'
      where render-verified) with the evidence path.

## S7-6 — The §7 completeness gate (feeds Phase-3 certification)

  At Phase 3, EVERY image must carry a 'rendered-and-viewed' stamp naming a montage file
  that EXISTS, EVERY table/matrix/chart and EVERY OMML expression a 'recomputed' stamp
  naming a trace file that EXISTS, in the ledger. Any artefact lacking its required stamp
  OR whose named evidence file is missing/trivial = an un-audited visual/structured item
  = SHIP is BLOCKED (RA-4 / RA-19 / §18 / S5-1A C6/C7). There is NO sampling and NO
  "[not-viewed]" exemption.

# ════════════════════════════════════════════════════════════════════════
# §8 — RECTIFICATION ENGINE (fix in place; regenerate under Step-7 contracts)
# ════════════════════════════════════════════════════════════════════════
#   Every defect is FIXED in this session (RA-5). Two fix classes:

## S8-1 — Class CP — CONTENT-PRESERVING fixes (do not change the correct option)

  Applied in Phase 1 (paper-wide) and as leftovers per batch. They edit the docx
  directly; no re-solve needed because the answer is unchanged.
    CP-FONT      → set every run to Calibri 11 (R24).
    CP-OPTLABEL  → relabel options to option_label_format (R10).
    CP-SECHDR    → delete body section-heading paragraphs (R8).
    CP-ANSKEY    → remove any answer-key/marker/hint paragraph or run (R5).
    CP-QNFIRST   → re-emit the block Q.N-first: Q.N context line → stimulus →
                   non-numbered specific-ask → options → blank (R14 / §9 SC-3).
    CP-BLANKSEP  → insert the missing blank separator (R13).
    CP-UNDERLINE → split the carrier sentence into runs and apply a real <w:u> to the
                   target span; delete the "(underlined: X)" annotation (R-UNDERLINE).
    CP-MATHOMML  → re-render a built-up expression as <m:oMath> (Step-7 §10-S10-4) and
                   delete the raster/ASCII form (R-MATH-OMML).
    CP-STIMEMBED → embed the shared stimulus (passage/table/chart/cloze paragraph) into
                   every linked member's block, Model A (R-LINKED / §9 SC-3); re-emit a
                   DI table as a real table object per member, re-insert a chart image
                   per member (intra-group reuse is exempt — SC-6).
    CP-FIGDECOMP → decompose a composite figural panel into a problem image + one image
                   per option, single-column, bound 1:1 to labels (R-FIGURAL). If the
                   underlying figures are CORRECT and only the LAYOUT is composite, this
                   is CP (re-slice/re-emit). If a figure is WRONG, it is RG.
    CP-IMGNAME   → rename a legitimate-but-mis-named figure to the canonical q{N}_* part
                   name (so the provenance contract + any name-contract gate pass).
    CP-ENCODING  → re-emit a run containing U+FFFD with the correct characters.
    CP-HEADER-STRIP → delete any non-blank paragraph before Q.1 (title/info/scoring/cover).
                   The paper is questions-only (Step 7 R8b / G-PREQ1); the block is not
                   question content, so removing it preserves all content. Dormant only if
                   section_rules EXAM_STRUCTURE declares paper_header_block.
  After CP fixes, re-run Part A to confirm the targeted gate(s) are green.

## S8-2 — Class RG — REGENERATION (defect requires new content)

  When a fix cannot preserve the answer — a wrong/unsourceable FACT, TWO defensible
  answers, a WRONG figure/table value, an impossible figure, a cross-mock/intra-mock
  DUPLICATE, an allocation/mandate miss, a wrong escape-option structure — REGENERATE
  that ONE question in place. Regeneration OBEYS EVERY STEP-7 CONTRACT (RA-6):
    1. KEEP the slot: same subtopic_id (blueprint join), same section, same difficulty
       target, same format — so the blueprint allocation and mandate stay satisfied
       (NEVER delete the question to "fix" a dup — RA-8).
    2. Generate the new question from section_rules patterns + wrong_option_structure
       for that subtopic_id (the same source Step 7 used).
    3. Enforce R-ANSWER (single: one defensible answer; multi: the correct set), R17 (stem↔option coherence), R-OPTREF
       (escape coherence), R13/R14/R24 (render), and the format's render contract
       (R-LINKED / R-FIGURAL / R-UNDERLINE / R-MATH-OMML) as applicable.
    4. DEDUP the replacement against (a) the WHOLE audit ledger (§9) — every other
       question reviewed so far, this mock — AND (b) the registry (§10) — every prior
       mock, with --mockN self-exclusion. The replacement must be a NEW scenario AND a
       distinct presentation (B-SCENARIODUP / B-PRESENTDUP).
    5. For a fact: web-verify the new fact + options (RA-11) before accepting AND save
       the evidence (evidence/facts/).
    6. RE-AUDIT the regenerated question fully (Part A on its block + the full Part B/§7
       checklist for its class, re-saving its evidence) — it is NOT done while it
       carries an unreviewed change; its ledger entry status becomes 'regenerated'.
    7. Update the ledger + the derived key (§11) for the new content.
    8. RECORD THE CHANGE (S8-5) into audit_state.regenerations — captures, for this one
       question, the structural diff (for the in-chat report, content-free) AND the
       literal before→after (for the downloadable change-log artefact). This is what
       lets the report say exactly which questions were replaced and how.

## S8-3 — The re-audit loop (per batch) + global reconciliation

  After applying CP + RG fixes in a batch:
    a) re-audit every fixed/regenerated question (S8-2 step 6);
    b) re-run WHOLE-PAPER Part A (RA-7) — a fix can perturb a global invariant
       (new K-PAT run, new dup, drifted count, new orphan); resolve any new failure
       (which may itself be CP or RG) IN THIS BATCH before ending;
    c) iterate (a)–(b) until the batch's slice AND whole-paper Part A are clean.
  A regeneration that re-perturbs is re-fixed; the loop terminates because each
  iteration strictly reduces the open-defect set (a replacement is dedup-checked
  against everything, so it cannot re-introduce the same class).

## S8-4 — Repair constraints (inherited discipline)

  • Replacing a question: fresh vs ALL prior mocks AND this mock (ledger + registry).
  • Re-balancing a distractor for A-KBAL/A-KPAT: NEVER change which option is correct;
    rotate a distractor's position; re-run A-KPAT after (re-balancing can create runs);
    re-read each rebalanced option for grammatical sense. v1.2: A-KBAL/A-KPAT re-balancing
    operates ONLY on single-mode questions (multi positions are excluded from the
    single-position statistics); a multi question is never rotated to "fix" balance.
  • Repairing a multi (MSQ) question (A-MSQ-KEY / B-UNIQUE-multi / B-DISTRACT-multi):
    NEVER change one membership to silence a flag — preserve/re-form the WHOLE correct SET
    so RA-12 multi holds (non-empty proper subset, fixed-k honored, every in-set option
    defensible and every out-set option indefensible). A borderline out-set option is fixed
    by disambiguating the stem or replacing that option, exactly like the single-mode
    second-defensible-option repair. A-MSQ-INSTR is repaired by re-emitting the stem with
    the select-instruction on the Q.<n> line (never as a separate paragraph — that breaks
    A-QNFIRST).
  • Re-rendering a figure: verify the new media part is NOT byte-identical to any other
    question's image before overwriting (R3), then RE-VIEW it (§7) and re-save its montage.
  • Any built-up math in a replacement → OMML (R-MATH-OMML).
  • After ANY repair: re-run the ENTIRE relevant gate set; iterate to zero FAIL + zero
    fixable WARN. A failing question is NEVER left in the paper; the paper is never
    delivered with a known-open defect.

## S8-5 — Change-record capture (feeds the report §R5 + the change-log artefact)

  Every Class-RG regeneration (and any CP fix that materially altered a question's
  rendered form, e.g. CP-MATHOMML / CP-FIGDECOMP) appends one record to
  audit_state.regenerations. Two views are derived from the SAME record:

  STRUCTURAL view (for the in-chat report — MANDATE-0 safe, NO content):
    { q, class:'RG'|'CP', defect_code, change_class, invariants_preserved,
      reaudit:'clean', dedup:'clean' }
    where:
      • defect_code      = the code that triggered it (e.g. B-UNIQUE, B-FACT, A-DUP,
                           A-MATHRASTER, B-PRESENTDUP).
      • change_class     = a content-free description of WHAT changed, drawn from a
                           fixed vocabulary: 'scenario replaced' | 'distractor
                           rebalanced' | 'fact corrected (web-verified)' | 'figure
                           re-rendered' | 'math re-rendered as OMML' | 'option set
                           re-templated' | 'stem disambiguated' | 'stimulus embedded'.
      • invariants_preserved = the Step-7 join points kept identical so the blueprint
                           stays satisfied: subtopic_id, section, difficulty, format
                           (+ 'answer position UNCHANGED' when the fix did not move the
                           key — true for every CP fix and for distractor rebalances).
  LITERAL view (for the downloadable change-log artefact ONLY — never chat):
    { q, defect_code, before:{stem, options, key}, after:{stem, options, key},
      rationale }  — the actual old and new text, so the author can see the real diff.

  The literal view is written ONLY to /home/claude staging and emitted ONLY into
  deliverable #3 (the change-log .md, S14-1). It is NEVER printed in chat (MANDATE 0).
  If no record exists (zero regenerations), no change-log file is produced.

# ════════════════════════════════════════════════════════════════════════
# §9 — THE AUDIT LEDGER (Step 8's independent concept/answer memory)
# ════════════════════════════════════════════════════════════════════════
#   The concept_map/presentation_ledger Step 7 used is NOT delivered (S0-1). §9 is
#   Step 8's INDEPENDENT, re-derived equivalent — built as the audit proceeds, used
#   to dedup regenerations against the whole mock and to make per-batch sign-off and
#   resume honest. Stored in /home/claude/[ExamCode]_M[N]_audit_state.json (never
#   delivered, never printed — MANDATE 0). v2.6 — it is ALSO the object the Phase-3
#   COMPLETION GATE (S5-1A) validates, so its per-question entries and their evidence
#   references are LOAD-BEARING, not merely a memory aid.

## S9-1 — Ledger schema (per reviewed question)

  ledger.entries[q] = {
    subtopic_id, section, class,                # classification (S6-1)
    answer_cardinality,                                # v1.2: 'single' | 'multi' (re-derived)
    scenario_sketch,                            # MANDATE-0-safe abstraction of the
                                                #   scenario (archetype + seed sketch /
                                                #   fact-concept / vocab-target / figural
                                                #   transformation) — NOT the stem text
    presentation_family, stem_format, distractor_strategy,   # for B-PRESENTDUP
    axis1, axis2, axis3, is_negative,           # v2.5: re-derived by AXIS CLASSIFIER v1.0 (S6-1b)
                                                #   from the shipped question — feeds S6-6 audit.
    is_factual (bool),                          # v2.6: this q (or an option) carries a
                                                #   CA/static-GA fact → S5-1A C5 requires a source
    # v1.2 — answer memory is mode-aware: single ⇒ derived_answer is an int and
    # answer_fact_value a scalar; multi ⇒ derived_answer is the SORTED set (list[int]),
    # answer_set_verified records RA-12-multi pass, and answer_fact_values is the LIST of
    # every value in the set so B-LEAK scans them all (P3-1), not just one.
    derived_answer, answer_unique (bool), answer_fact_value,   # for B-LEAK / §11 (single)
    answer_set_verified (bool), answer_fact_values: [...],     # for B-LEAK / §11 (multi)
    # v2.6 — EVIDENCE-BOUND provenance (RA-19 / FIX F). Each stamp NAMES the on-disk
    # artefact that proves the Claude-driven check actually ran. S5-1A C5/C6/C7 verify
    # these files EXIST and are non-trivial — a stamp with no backing file is un-audited.
    fact_sources: [ {url, date, saved: "evidence/facts/q{n}_k.json"}, ... ],  # C-FACTUAL
    artefact_stamps: {
        images:   [ {rid_or_name, stamp:'rendered-and-viewed', montage:"evidence/montages/q{n}_montage.png"} ],
        tables:   [ {idx, stamp:'recomputed', trace:"evidence/recompute/q{n}_table.txt"} ],
        charts:   [ {idx, stamp:'rendered-and-viewed'+'recomputed', montage:..., trace:...} ],
        omml:     [ {idx, stamp:'recomputed', trace:"evidence/recompute/q{n}_omml.txt"} ]
    },
    status: 'pending' | 'verified' | 'regenerated'   # opened 'pending' at S6-0.7; closed
                                                     # only when every applicable check ran
  }
  Plus rollups: scenarios[], presentations[], vocab_targets[], facts[], image_hashes[].

## S9-2 — How the ledger is used

  • REGENERATION dedup (§8-2 step 4): a replacement's scenario_sketch + presentation must
    not collide with ANY ledger entry (whole mock), not just the current batch — this is
    what stops a batch-K regeneration from semantically colliding with a batch-1 question
    the machine cannot see.
  • B-SCENARIODUP / B-PRESENTDUP (§6-4): finalised at Phase 3 by scanning the ledger.
  • B-LEAK (§6-2): finalised at Phase 3 from ledger.derived_answer / answer_fact_value
    (single) and ledger.answer_fact_values (multi — every value in the set is scanned).
  • RESUME (RA-18): the ledger is reloaded; reviewed questions are not re-reviewed; the
    whole-paper Part A still runs each resumed batch; the evidence dir persists.
  • STAMPS (RA-19): artefact_stamps + their evidence files feed the §7-6 / §18 / S5-1A
    certification gate — presence AND backing-file existence are both checked.
  • COMPLETION GATE (S5-1A): reads entries.keys() (C2), status (C3), answer_unique /
    answer_set_verified (C4), fact_sources + saved files (C5), artefact_stamps + montage/
    trace files (C6), and coverage totals (C7). The ledger is the contract between the
    Claude-driven audit and the machine gate that certifies it.

# ════════════════════════════════════════════════════════════════════════
# §10 — CROSS-MOCK DEDUP (registry-based; full; self-excluding)
# ════════════════════════════════════════════════════════════════════════

## S10-1 — Scope

  Cross-mock dedup runs FULLY (RA-13) — Step 8 HAS the registry. A-DUP (machine) +
  the §6 content checks together cover it. --mockN N self-excludes mock N's own stems
  (re-auditing the registered mock must not flag it against itself; the registry
  already contains mock N because Step 7 appended it — S2-2 guards alignment).

## S10-2 — What is checked against the registry

  [ ] STEM dedup: each mock-N stem vs every PRIOR-mock stem in registry.stem_texts —
      exact match = defect; near-match (token Jaccard ≥ J_FAIL, default 0.75) = defect;
      borderline (J_WARN..J_FAIL, default 0.60–0.75) = read both, document if genuinely
      distinct else regenerate. (Self-exclude same-mock via --mockN.)
  [ ] IMAGE dedup: hash word/media/ DIRECTLY (registry image_hashes may be empty) —
      no MD5/pHash match to a registered prior-mock image (R3 cross-mock).
  [ ] CONTENT-TRACKING blind spots (registry.content_tracking L4–L18): vocab targets,
      GA facts (concept level), numeric seeds, analogy schemes, idioms, grammar rules,
      computer/domain facts, cause-effect domains, syllogism domains, option sets,
      passage/cloze topics — none repeats beyond its allowed frequency. These are the
      checks G-DUP is blind to (figural, <5-token stems, concept echoes); they are done
      from the registry + the ledger.

## S10-3 — Registry as the dedup source of truth

  RS-10 (Step 1): the registry MUST be replaced in project knowledge after each Step-7
  session. If the registry handed to Step 8 lags (mocks_completed missing an earlier
  mock, or stem_texts count ≠ Σ prior mock sizes), cross-mock dedup is PARTIAL — record
  it as a §15/§19 limitation (NOT a content defect; not fixable at Step 8) and proceed
  with the dedup the registry supports. S2-2 already hard-stops the worst case (registry
  not ending in mock N).

# ════════════════════════════════════════════════════════════════════════
# §11 — ANSWER DERIVATION & UNIQUENESS (no key delivered — solve it)
# ════════════════════════════════════════════════════════════════════════

## S11-1 — Independent solve

  Step 8 receives NO answer key (S0-1). For every question it INDEPENDENTLY derives the
  intended answer from the stem + attached artefacts + (for facts) live web sources. The
  derived key is stored in audit_state.derived_key {q: option_index} — INTERNAL, never
  delivered (the learner key is a Step-9 artefact), never printed (MANDATE 0).

## S11-2 — What the derived key is FOR

  • B-UNIQUE: confirm exactly one option is defensible (the derivation must land on one,
    and only one, option). If the derivation finds TWO defensible options → R-ANSWER (single)
    defect → §8 disambiguate/replace.
  • B-DISTRACT: confirm the other options are wrong.
  • A-KINT/A-KBAL/A-KPAT: run the key-health gates against the DERIVED key (the only key
    Step 8 has). These are advisory→fix: a balance/run defect is fixed by rotating a
    DISTRACTOR (never changing the correct option — §8-4). A-KBAL/A-KPAT operate over
    single-mode questions only.
  • (multi only) A-MSQ-KEY: the re-derived set is a non-empty proper subset (fixed-k +
    AOTA rules honored); A-MSQ-INSTR: the per-section multi instruction count matches the
    blueprint. Both dormant when no subtopic is answer_cardinality=='multi'.
  • B-LEAK: the derived answer values feed the inter-question leakage scan (every value in
    a multi set, not just one).

## S11-3 — Boundary with Step 9

  Step 8 does NOT deliver or certify the learner-facing key — Step 9 (MockExplain)
  independently re-derives and publishes it. Step 8's derivation exists to AUDIT
  (uniqueness, correctness, balance), and to ensure that when Step 9 solves the paper it
  will find exactly one defensible answer per question. A divergence between Step 8's
  derived key and a (future) Step-9 key on a question that Step 8 certified as unique is
  a Step-9 escalation, not a Step-8 deliverable.

# ════════════════════════════════════════════════════════════════════════
# §12 — VERDICT & CERTIFICATION (Step 8 ships only a clean paper)
# ════════════════════════════════════════════════════════════════════════

## S12-1 — There is no "DON'T SHIP" terminal state

  Unlike a pure auditor, Step 8 RECTIFIES (RA-5). "DON'T SHIP" is never a final
  outcome — a found defect triggers §8 repair-and-re-audit until clean. The only
  outcomes are: CERTIFIED CLEAN (deliver) or HARD STOP (a pre-flight/integrity
  blocker that prevents auditing at all — e.g. missing input, corrupt/truncated input
  (P0.5), failed hardened self-test (P1), unresolvable rId, N-disagreement; these
  require user action, not a verdict).

## S12-2 — Certification gate (Phase 3, all must hold)

  [ ] audit.py --final --audit-state <path>  →  "COMPLETION-GATE: PASS"  (S5-1A).
      (v2.6 — THIS LINE SUPERSEDES SELF-ATTESTATION: it is a COMMAND RESULT, not a
      sentence the model writes. If it fails, NOTHING below is "clean". The items
      beneath are the human-readable expansion of what the gate now checks
      mechanically — they are no longer the certification themselves.)
  [ ] Final whole-paper Part A: exit 0, zero fixable WARN.
  [ ] Every Part-B check (§6) complete for every question; zero open content defect.
      (mechanically asserted by S5-1A C2+C3; not self-attested)
  [ ] Every §7 artefact carries its required stamp (image='rendered-and-viewed';
      table/matrix/chart/OMML='recomputed') AND the montage/trace file it names EXISTS;
      zero un-audited visual/structured item. (mechanically asserted by S5-1A C6+C7)
  [ ] B-ALLOC / B-MANDATE / B-SCENARIODUP / B-PRESENTDUP / B-LEAK finalised clean
      across the whole mock.
  [ ] Every CA/static-GA fact web-verified with a recorded, SAVED source (RA-11).
      (mechanically asserted by S5-1A C5)
  [ ] derived key A-KINT clean (single int or proper subset per mode);
      A-KBAL/A-KPAT within band (single-mode questions only). (S5-1A C4 for uniqueness)
  [ ] (multi only) A-MSQ-KEY clean — every re-derived set is a non-empty proper subset
      (fixed-k honored, AOTA rule honored); A-MSQ-INSTR clean — observed multi
      instruction counts match the blueprint per section. Dormant when multi_present=false.
  [ ] registry re-synced from the FINAL fixed file (§13) and schema-complete.
  Any item open → re-open the relevant Phase-2 work; Phase 3 does NOT proceed. Only
  when the COMPLETION GATE prints PASS and ALL hold is present_files permitted
  (MANDATE D).

# ════════════════════════════════════════════════════════════════════════
# §13 — REGISTRY RE-SYNC (rebuild mock-N's slice from the FIXED file)
# ════════════════════════════════════════════════════════════════════════
#   Step 7 already appended mock N to the registry (S13-4) BEFORE this audit. If
#   Step 8 changed any content, the registry's mock-N hashes/stems/manifests are now
#   STALE. Step 8 re-syncs them FROM THE FINAL FIXED DOCX (RA-17), so Step 9 and the
#   next mock dedup against the rectified content, not the pre-audit content.

## S13-1 — Why a trailing-slice rebuild is correct and safe

  registry.question_hashes / stem_texts / semantic_tuples are FLAT arrays appended in
  mock order (Step 1 §12; confirmed in the wild — stem_texts are plain strings). Step 8
  audits the MOST RECENTLY appended mock (S2-2 hard-stops unless mocks_completed[-1]==N).
  Therefore mock N occupies the TRAILING `count_N` entries of each flat array, where
  count_N == total_questions for this mock. Step 8 rebuilds exactly that trailing slice.
  Mock-tagged structures (rc_manifests, figural_manifests, content_tracking L4–L18,
  session_log) carry an explicit mock/mock_n field and are replaced BY KEY (mock==N).

## S13-2 — Re-sync procedure (run at Phase 3, from the fixed docx)

  ```python
  import json, hashlib, re
  from docx import Document   # parse_blocks/block_stem_text are the §P6 helpers

  reg = json.load(open(f'/home/claude/{EXAM}_registry.json', encoding='utf-8'))
  _pc = reg.get('papers_completed') or [f"MOCK:M{int(x):02d}" for x in reg.get('mocks_completed', [])]
  assert _pc[-1] == paper_id, "S2-2 guard: registry must end with THIS paper (paper_id)."  # C3
  _title, fixed_blocks = parse_blocks(Document(FIXED_DOCX))   # §P6 → (title, blocks)
  assert len(fixed_blocks) == total_questions

  # 1) trailing-slice rebuild of the flat arrays (mock N == last total_questions entries)
  #    qhash MUST mirror the Step-7 S13-4 hashing recipe so future-mock dedup that
  #    compares hashes stays consistent; stem_texts (the PRIMARY dedup field) is
  #    rebuilt faithfully regardless. If the Step-7 recipe is unknown, rely on the
  #    faithfully-rebuilt stem_texts and recompute hashes with the recipe below.
  def clean_stem(b):                              # same normalisation Step 7 used
      return re.sub(r'\s+', ' ', block_stem_text(b)).strip()
  def qhash(b):
      return hashlib.md5(f"M{N}Q{b.qnum}|{clean_stem(b).lower()}".encode()).hexdigest()

  for arr, builder in (('question_hashes', qhash),
                       ('stem_texts',     clean_stem),
                       ('semantic_tuples', semantic_tuple)):   # semantic_tuple re-derived
      old = reg.get(arr, [])
      assert len(old) >= total_questions, \
          f"S13 guard: {arr} shorter than one mock — registry corrupt (re-check S2-2)."
      keep = old[:len(old) - total_questions]
      reg[arr] = keep + [builder(b) for b in fixed_blocks]

  # 2) replace mock-tagged manifests BY KEY (rebuilt from the fixed file)
  reg['rc_manifests'] = [m for m in reg.get('rc_manifests', []) if m.get('mock') != N]
  if passage_present_in_fixed:
      reg['rc_manifests'].append({'mock': N,
          'passage_linked': sorted(passage_linked_fixed),
          'cloze_linked':   sorted(cloze_linked_fixed)})
  reg['figural_manifests'] = [m for m in reg.get('figural_manifests', []) if m.get('mock') != N]
  if figural_present_in_fixed:
      reg['figural_manifests'].append({'mock': N,
          'figural_qs':  sorted(figural_qs_fixed, key=int),
          'image_hashes': image_hashes_fixed})    # hashed from word/media of the FIXED file

  # 2b) question_index re-sync BY KEY (v1.6 — Contract_QuestionMetadataIndex v1.0).
  #     subtopic_id : the CERTIFIED value is Step 8's INDEPENDENT re-derivation (the §9 audit
  #                   ledger's per-q subtopic_id, from the B-ALLOC content->id mapping) — NEVER
  #                   trusted from Step 7. A disagreement with Step 7's incoming index is a
  #                   labelling defect (logged); the re-derived id wins. A regenerated Q keeps its
  #                   slot id (RA-6), so re-derivation agrees by construction.
  #     difficulty  : CARRIED FORWARD from Step 7's incoming index — difficulty is NOT rendered in
  #                   the paper and is NOT re-derivable from it (§19). Regeneration preserves the
  #                   difficulty target (RA-6 / S8-2), so the carried value stays correct.
  #     This is Step 8's certification of the four subtopic_id-derived tags + the carried Complexity
  #     tag that Step 6 renders. Exam-agnostic; writes NOTHING to the docx.
  _s2      = next((e for e in reg.get('question_index', [])
                   if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") == paper_id),
                  {'questions': []})   # C3: key on paper_id (== mock for a mock)
  _s2map   = {int(x['q']): x for x in _s2.get('questions', [])}
  _regen_q = {r['q'] for r in audit_state.get('regenerations', [])}
  _qi = []
  for q in range(1, total_questions + 1):
      _cert_id = ledger.entries[q]['subtopic_id']          # §9 independent re-derivation
      _s2q     = _s2map.get(q, {})
      if q not in _regen_q and _s2q.get('subtopic_id') != _cert_id:
          audit_state.setdefault('findings', []).append(
              f"question_index: Q{q} Step-7 subtopic_id {_s2q.get('subtopic_id')!r} "
              f"!= re-derived {_cert_id!r} — re-derived id wins (Step-7 labelling defect).")
      _qi.append({'q': q,
                  'subtopic_id': _cert_id,                 # certified = independently re-derived
                  'difficulty':  _s2q.get('difficulty')})  # carried forward (never from the docx)
  reg['question_index'] = [e for e in reg.get('question_index', [])
                           if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") != paper_id]
  reg['question_index'].append({'mock': N, 'paper_id': paper_id, 'questions': _qi})   # C3

  # 3) content_tracking L4–L18: drop mock_n==N rows, re-append from the fixed file's ledger
  ct = reg.setdefault('content_tracking', {})
  for field in ['ga_facts_used','passage_topics','cloze_topics','vocab_words_used',
                'idioms_used','grammar_rules_used','computer_facts','numeric_seeds',
                'analogy_schemes','cause_effect_domains','syllogism_domains','option_sets']:
      ct[field] = [r for r in ct.get(field, []) if r.get('mock_n') != N] \
                  + audit_ledger_content_tracking(field, N)   # from §9 ledger

  # 4) image_phashes (top-level) for mock N: drop+re-add from fixed media
  reg['image_phashes'] = [h for h in reg.get('image_phashes', []) if h.get('mock_n') != N] \
                         + image_phashes_fixed

  # 5) audit session-log entry (does NOT duplicate Step 7's; records the audit)
  reg.setdefault('session_log', []).append({
      'mock': N, 'step': 'MockCreateAudit', 'audit_version': '2.6',
      'verdict': 'CERTIFIED_CLEAN',
      'completion_gate': 'PASS',                 # v2.6: S5-1A result recorded
      'defects_fixed': len(audit_state['defects']),
      'regenerated': len(audit_state['regenerations']),
      'inputs_repaired': audit_state.get('session_log', {}).get('inputs_repaired', []),
      'timestamp': now_utc_iso(), 'notes': 'registry re-synced from fixed file'})

  # 5b) v2.5 THREE-AXIS — accumulate THIS mock's independently re-tagged axes into the window
  #     tally, then (only at window close) run the S6-6 format-distribution audit. Counts come
  #     from the §9 ledger, which tagged each question from the FINAL fixed docx (S6-1b).
  if axis_schedule:                                          # inert when blueprint has no target
      # IDEMPOTENCY (resume/re-audit safe): a mock is added to the window tally AT MOST ONCE.
      # axis2_audit_mocks (loaded in P4, window-aware) lists mocks already counted this window.
      _already_counted = (N in axis2_audit_mocks)
      for sec in sections:
          nm = sec['name']
          acc = axis2_audit_sections.setdefault(
              nm, {'axis1': {}, 'axis2': {}, 'axis3': {}, 'neg': 0, 'total': 0})
          if _already_counted:
              continue                                        # do NOT re-add mock N's counts
          for q, e in ledger.entries.items():                 # this mock's per-question ledger
              if e.get('section') != nm:
                  continue
              for ax in ('axis1', 'axis2', 'axis3'):
                  c = e.get(ax)
                  if c:
                      acc[ax][c] = acc[ax].get(c, 0) + 1
              acc['total'] += 1
              if e.get('is_negative'):
                  acc['neg'] += 1
      if not _already_counted:
          axis2_audit_mocks.append(N)
      reg['axis2_audit'] = {'window': _cur_window, 'sections': axis2_audit_sections,
                            'mocks': sorted(set(axis2_audit_mocks))}

      if axis_window_is_closing(N, AXIS_WINDOW, TOTAL_MOCKS):
          # PARTIAL-WINDOW SCALING: the last window may hold fewer than AXIS_WINDOW mocks
          # (total_mocks not a multiple of the window). Scale every per-window target to the
          # ACTUAL number of mocks in this window so a short final window is judged fairly.
          mocks_in_window = N - _cur_window * AXIS_WINDOW      # e.g. W=10, N=13, w=1 → 3
          if mocks_in_window <= 0:
              mocks_in_window = AXIS_WINDOW                    # defensive (never expected)
          scale = mocks_in_window / float(AXIS_WINDOW)
          s7_sections = s7_axis_window.get('sections', {}) if s7_axis_window.get('window') == _cur_window else {}
          axis_findings = []
          for sec in sections:
              nm  = sec['name']
              sch = axis_schedule.get(nm)
              acc = axis2_audit_sections.get(nm, {'axis1':{}, 'axis2':{}, 'axis3':{}, 'neg':0, 'total':0})
              axis_findings += audit_axis2(nm, sch, acc['axis2'], scale=scale)
              if sch and sch.get('status') == 'ok':
                  axis_findings += audit_axis13(nm, '1', sch.get('axis1_per_paper', {}), acc['axis1'], mocks_in_window)
                  axis_findings += audit_axis13(nm, '3', sch.get('axis3_per_paper', {}), acc['axis3'], mocks_in_window)
                  axis_findings += audit_axis_negative(nm, sch, acc['neg'], acc['total'])
              # cross-check only within the SAME window (guarded above via s7_sections).
              axis_findings += cross_check_step7(nm, acc['axis2'], s7_sections)
          # ADVISORY by default (RA-9 parallel): log to the report; escalate to a blocking defect
          # only if section_rules/blueprint marks the format mix a hard requirement.
          for _af in axis_findings:
              audit_state.setdefault('findings', []).append(_af)
          audit_state['axis_window_audited']  = _cur_window    # dashboard reads these
          audit_state['axis_window_findings'] = len(axis_findings)

  # 6) schema-completeness (idempotent self-heal — same intent as Step 7 S13-REGCHECK)
  REQUIRED_TOP = ['exam_code','schema_version','mocks_completed','question_hashes',
                  'stem_texts','semantic_tuples','question_index','image_phashes',
                  'image_sources_used','session_log','content_tracking','section_names',
                  'rc_manifests','figural_manifests']
  for f in REQUIRED_TOP:
      reg.setdefault(f, {} if f == 'content_tracking' else [])
  reg.setdefault('axis2_audit', {})     # v2.5: dict; preserved across re-syncs (never dropped)

  json.dump(reg, open(f'/home/claude/{EXAM}_registry.json','w',encoding='utf-8'),
            indent=2, ensure_ascii=False)
  ```

## S13-3 — Re-sync verification (gate before delivery)

  [ ] len(question_hashes) == len(stem_texts) == len(semantic_tuples).
  [ ] the trailing total_questions stems all carry mock-N's fixed content (re-hash the
      fixed file, compare).
  [ ] mocks_completed unchanged (Step 8 NEVER appends a mock — it only re-syncs mock N).
  [ ] no mock_n==N row survives in any content_tracking field except the re-appended ones.
  [ ] registry schema-complete.
  [ ] question_index (v1.6): exactly ONE mock-N object; its questions cover q=1..total_questions
      (sorted, unique, complete); every subtopic_id ∈ blueprint.subtopic_list[]; every difficulty
      ∈ blueprint.difficulty_labels; difficulty distribution == difficulty_schedule[N] EXACTLY.
      subtopic_id values are Step 8's INDEPENDENT re-derivation (§9 ledger); difficulty values are
      CARRIED FORWARD from Step 7 (not re-derived from the paper — §19). Mirrors Step 7 G-QINDEX
      (Contract_QuestionMetadataIndex v1.0).
  Any failure → HARD STOP (do not deliver a corrupt registry; inspect S13-2).

# ════════════════════════════════════════════════════════════════════════
# §14 — DELIVERY (core closed set + conditional change-log; ONE present_files)
# ════════════════════════════════════════════════════════════════════════

## S14-1 — The deliverable set (CORE closed; change-log conditional)

  CORE SET (always — = Step 7 R-DELIVER discipline):
    1. /mnt/user-data/outputs/[ExamCode]_Mock[N]_Create_Complete.docx   — RECTIFIED paper
    2. /mnt/user-data/outputs/[ExamCode]_registry.json           — RE-SYNCED registry
  CONDITIONAL (iff audit_state.regenerations is non-empty — S8-5):
    3. /mnt/user-data/outputs/[ExamCode]_Mock[N]_audit_changelog.md  — author-only
       BEFORE→AFTER diff for every regenerated question.
  NEVER deliver: the derived key, the audit ledger, audit_state, the block index,
    the evidence dir (montages/facts/recompute), montages, any scratch/WIP docx, any
    other internal sidecar. The learner key is a Step-9 artefact (R-DELIVER).

## S14-1b — Build the change-log artefact (only if regenerations occurred)

  ```python
  import os
  regens = audit_state.get('regenerations', [])
  changelog = None
  if regens:
      out = '/mnt/user-data/outputs'
      changelog = f'{out}/{EXAM}_Mock{N}_audit_changelog.md'
      with open(changelog, 'w', encoding='utf-8') as f:
          f.write(f"# Mock {N} Audit Change-Log — {EXAM}\n")
          f.write("# AUTHOR-ONLY AUDIT ARTEFACT — NOT FOR DISTRIBUTION.\n")
          f.write("# Contains the literal before/after of every regenerated question.\n")
          f.write(f"# Generated by Step 8 (MockCreateAudit v2.6). "
                  f"Questions regenerated: {len(regens)}.\n\n")
          for r in regens:                       # r carries the LITERAL view (S8-5)
              f.write(f"## Q.{r['q']} — {r['class']} (defect: {r['defect_code']})\n\n")
              f.write(f"**What changed:** {r['change_class']}  ·  "
                      f"**Preserved:** {', '.join(r['invariants_preserved'])}\n\n")
              b, a = r['before'], r['after']
              f.write("### BEFORE\n")
              f.write(b['stem'] + "\n")
              for i, o in enumerate(b['options'], 1): f.write(f"  {i}. {o}\n")
              f.write(f"  [key: option {b['key']}]\n\n")
              f.write("### AFTER\n")
              f.write(a['stem'] + "\n")
              for i, o in enumerate(a['options'], 1): f.write(f"  {i}. {o}\n")
              f.write(f"  [key: option {a['key']}]\n\n")
              f.write(f"### Rationale\n{r['rationale']}\n\n")
              f.write(f"### Re-audit\nPart A + Part B/§7 for the question's class: "
                      f"clean.  Dedup vs ledger + registry: clean.\n\n---\n\n")
  ```

## S14-2 — Pre-delivery checklist (MANDATORY before present_files; MANDATE D)

  ```python
  import os
  out = '/mnt/user-data/outputs'
  docx_name = f'{EXAM}_{paper_slug}_Create_Complete.docx'; reg_name = f'{EXAM}_registry.json'  # C3
  cl_name   = f'{EXAM}_Mock{N}_audit_changelog.md'
  expected  = {docx_name, reg_name} | ({cl_name} if regens else set())
  present   = set(os.listdir(out))
  BANNED    = ('answer', 'key', 'ledger', 'audit_state', 'blockindex', 'montage', 'evidence')
  # the change-log legitimately contains 'audit' + Q content; exempt it from the
  # banned-substring scan, but ban every OTHER internal sidecar:
  leaked = [f for f in present if f != cl_name
            and any(b in f.lower() for b in BANNED)]
  checks = [
    ('1 fixed docx in outputs',         os.path.exists(f'{out}/{docx_name}')),
    ('2 re-synced registry in outputs', os.path.exists(f'{out}/{reg_name}')),
    ('3 change-log present iff regens',  os.path.exists(f'{out}/{cl_name}') == bool(regens)),
    ('4 completion gate passed',        bool(globals().get('COMPLETION_GATE_PASS'))),
    ('5 no internal sidecar leaked',    not leaked),
    ('6 outputs == exactly expected set', present == expected),
  ]
  fails = [n for n, ok in checks if not ok]
  if fails:
      raise SystemExit("HARD STOP (S14-2): " + "; ".join(fails) +
                       ". Fix, then re-run S14-2. Do NOT call present_files yet.")
  ```
  Stage ONLY the deliverables in outputs; keep everything else (incl. the evidence
  dir) in /home/claude. Check 4 (COMPLETION_GATE_PASS) is set ONLY by an actual
  S5-1A "COMPLETION-GATE: PASS" exit-0 run — never by a self-declared flag.

## S14-3 — The single present_files call

  ```python
  files = [f'/mnt/user-data/outputs/{EXAM}_{paper_slug}_Create_Complete.docx',
           f'/mnt/user-data/outputs/{EXAM}_registry.json']
  if regens:
      files.append(f'/mnt/user-data/outputs/{EXAM}_Mock{N}_audit_changelog.md')
  present_files(files)        # docx first; the ONLY present_files call (MANDATE D)
  ```

## S14-4 — STATUS REPORT dashboard (print in chat at delivery; MANDATE-0 safe)

  A single scannable block printed right after present_files (before the §15 detail and
  the handoff). All figures come from real audit STDOUT + audit_state — never memory.
  NO question content (counts, codes, Q-numbers only).

  ```
  ╔════════════════════════════════════════════════════════════════════╗
  ║  STEP 8 · MOCK [N] AUDIT — STATUS REPORT            ✅ CERTIFIED ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  Paper    : [ExamCode]_Mock[N]_Create_Complete.docx ([size], md5 [….])    ║
  ║  Verdict  : CERTIFIED CLEAN — delivered                             ║
  ║  Gate     : COMPLETION-GATE: PASS (C1–C7)   [S5-1A]                 ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  ON ARRIVAL              →   AFTER RECTIFICATION                    ║
  ║  Part A  : [a] FAIL · [w] WARN   →   0 FAIL · 0 fixable WARN        ║
  ║  Content defects open : [c]      →   0                              ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  COVERAGE (zero sampling — RA-3; evidence-backed — S5-1A)          ║
  ║    Questions reviewed ........ [N]/[N]                              ║
  ║    Batches run .............. [K]/[K]                               ║
  ║    Images rendered & viewed .. [i]/[i]   (montage files present)    ║
  ║    Tables recomputed ......... [t]/[t]   (trace files present)      ║
  ║    Charts viewed ............. [ch]/[ch]                            ║
  ║    OMML expressions recomputed [o]/[o]                              ║
  ║    Facts web-verified ........ [f]/[f]   (sources saved, not shown) ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  RECTIFICATION                                                     ║
  ║    Content-preserving fixes (CP) : [cp]  (top: [code×n], [code×n]) ║
  ║    Questions regenerated   (RG)  : [rg]  → see Change-Log below     ║
  ╠════════════════════════════════════════════════════════════════════╣
  ║  DEDUP    : cross-mock [PASS|PARTIAL] · intra-mock [PASS]          ║
  ║  FORMAT   : Axis mix [window K: within tol | N finding(s) | inert]║
  ║  REGISTRY : re-synced from fixed file ✓ (mocks_completed unchanged)║
  ║  DELIVERED: [2|3] files (docx · registry[ · change-log])           ║
  ╚════════════════════════════════════════════════════════════════════╝
  ```
  Render the box with whatever box-drawing the client supports; if alignment is a
  concern, a plain "key: value" list with the same fields is equally acceptable —
  the CONTENT (verdict, completion-gate result, on-arrival→after delta, coverage
  matrix incl. batches-run, CP/RG counts, dedup, registry, file count) is what
  matters, not the borders.

## S14-5 — Handoff message (print after the dashboard + §15, then END)

  ```
  === MOCK [N] AUDIT COMPLETE — Step 8 done (CERTIFIED CLEAN) ===
  Delivered ([2|3] files):
    • [ExamCode]_Mock[N]_Create_Complete.docx       — rectified, zero-defect paper
    • [ExamCode]_registry.json               — re-synced from the fixed file
    • [ExamCode]_Mock[N]_audit_changelog.md  — author-only before/after diff
                                               (ONLY if questions were regenerated)

  Regenerated questions: [list of Q-numbers, or "none"].
  (The structural diff is in the report above; the literal before/after text is in
   the change-log file — open it outside chat. It is author-only; do not distribute.)

  ⚠ REGISTRY HANDOFF — REQUIRED before Step 9 / the next mock:
    Replace registry.json in your [ExamCode] project Files with the one just
    delivered (it now reflects the RECTIFIED content). Skipping this re-introduces
    the pre-audit stems into the dedup corpus.

  Next step → Step 9 (MockExplain): build the learner key + solutions on this
  certified paper.
  =============================================================
  ```
  After printing: END THE RESPONSE. Write nothing more.

## S14-6 — Post-delivery footer (MANDATORY after present_files)

```
After the present_files call, status report (S14-4), and handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type (F2 step-complete — always for
Step 8 since it has no batches), file badges (Use locally for docx + changelog,
Replace for registry.json), and next-step reference.
```

# ════════════════════════════════════════════════════════════════════════
# §15 — AUDIT REPORT FORMAT (MANDATE-0 safe; built from real STDOUT + findings)
# ════════════════════════════════════════════════════════════════════════
#   Built from actual audit STDOUT + reviewer findings — never re-summarised from
#   memory. NO question content anywhere (codes + Q-numbers only).

  §R0 Status dashboard : the §14-4 STATUS REPORT block (verdict · completion-gate
                   result · on-arrival→after delta · coverage matrix · CP/RG counts ·
                   dedup · registry · files). Printed first so the outcome is scannable.
  §R1 Provenance : docx name+size+MD5 · audit_version (2.6) · script self-test N/N
                   (fixture-based) · COMPLETION-GATE result · registry state
                   (mocks_completed, alignment) · blueprint/manifest ids · any
                   inputs_repaired (P0.5) · timestamp.
  §R2 Outcome    : CERTIFIED CLEAN (delivered) — unambiguous; backed by
                   "COMPLETION-GATE: PASS" (S5-1A), not a self-declaration.
  §R3 Part A     : on-arrival vs final — every gate OK/FAIL/WARN with its verbatim
                   message; the FAIL/WARN count the audit STARTED with → 0/0 final.
  §R4 Defects fixed (Class CP): grouped — code · count · Q-number list · one-line what.
  §R5 Regeneration change-log (Class RG): for EACH regenerated question, the STRUCTURAL
                   (content-free) record from S8-5 —
                     "Q.[n] · [defect_code] · [change_class] · preserved:[subtopic_id,
                      section,difficulty,format(,answer position)] · re-audit:clean ·
                      dedup:clean".
                   State plainly that the LITERAL before→after diff is in the delivered
                   change-log artefact (deliverable #3), not in chat (MANDATE 0). If
                   zero regenerations: "Regenerations: none — no change-log produced."
  §R6 Part B     : per-class results; clean classes stated as "all [n] verified — 0 defects".
  §R7 Coverage matrix (proves zero sampling — RA-3; evidence-backed — S5-1A): questions
                   reviewed [n/n] · batches run [K/K] · images rendered-and-viewed [n/n] ·
                   tables recomputed [n/n] · charts viewed [n/n] · OMML recomputed [n/n] —
                   every item stamped AND its evidence file present (RA-19); zero un-audited.
  §R8 Fact verification (CONTENT-FREE): COUNTS only — "[f] current-affairs / static-GA
                   facts and factual options web-verified; every source URL + date +
                   result saved to /home/claude evidence (and, for any regenerated fact,
                   into the change-log artefact)". NEVER list the facts themselves in chat
                   (they are answer content — MANDATE 0). A fact that could not be sourced
                   was regenerated (counted under §R5), never shipped.
  §R9 Dedup      : cross-mock (stems/images/content_tracking) result; intra-mock
                   B-SCENARIODUP/B-PRESENTDUP result.
  §R10 Allocation/Mandate: per-subtopic counts vs blueprint; mandatory/alternation status.
  §R11 Key health: A-KINT/A-KBAL/A-KPAT on the derived key (with the Step-9 boundary note);
       (multi only) A-MSQ-KEY (set well-formedness) + A-MSQ-INSTR (instruction-count match).
  §R12 Registry delta: trailing-slice rebuilt; manifests re-keyed; guard assertions; "replace before next mock".
  §R13 Limitations: anything not fully mechanisable (difficulty labels [estimate];
                   partial cross-mock dedup if registry lags; key adjudication is Step-9;
                   any P0.5 inputs_repaired; the S5-1A residual — §19).
  §R14 Defects-by-class rollup: a count of each defect CODE found+fixed, CP vs RG, so a
                   systemic Step-7 issue is visible at a glance (e.g. "A-MATHRASTER ×7 →
                   a generator-side math-rendering gap worth fixing upstream"). This turns
                   the audit into upstream feedback, not just a one-paper fix.
  §R15 Batch trace: batches run [K], re-audit iterations, and (on a resume) which batches
                   were carried over — so the run is reproducible and auditable.

  PROVENANCE STAMPS used: 'machine' · 'recomputed' · 'rendered-and-viewed' ·
  'web-verified+source' · 'reviewer-verified' · 'estimate'.

# ════════════════════════════════════════════════════════════════════════
# §16 — AUDIT GATE GLOSSARY (Step-8 gates ↔ the Step-7 contract each re-verifies)
# ════════════════════════════════════════════════════════════════════════
#   Step 8 re-verifies, INDEPENDENTLY, every machine-checkable Step-7 contract, and
#   adds Step-8-only integrity/semantic checks. The mapping (so nothing is lost):

  PART A (machine — universal audit.py):
    A-COUNT/A-SEQ/A-MONO/A-SECCOUNT      ← R7, R18 (+ Step-7 S3-9)
    A-OPTN/A-OPTLABEL/A-OPTORDER/A-OPTUNIQUE ← R4, R10, R13
    A-SECHDR ← R8/G-SECTIONHDR · A-ANSKEY ← R5/G-ANSWERKEY · A-FONT ← R24/G-FONTCHECK
    A-BLANKSEP ← R13 · A-QNFIRST ← R14/G-QNUM-FIRST
    A-STIMORPHAN ← R-LINKED/G-STIMULUS-ORPHAN
    A-MATCH-TABLE ← S7-3/G-MATCH-TABLE (Step 7 match-render mandate; re-derived MATCH must carry a real table)
    A-UNDERLINE ← R-UNDERLINE/G-UNDERLINE
    A-MATHRASTER ← R-MATH-OMML/G-MATH-RASTER (view-backed, S5-3) · A-FRAC ← G-FRAC
    A-OMML ← R-MATH-OMML/G-OMML(+FLOOR)
    A-FIGCOMP ← R-FIGURAL/G-FIGURAL-COMPOSITE (+ G-FIGTEXT figural-as-text + G-FIGTEXT-PROSE; S10-8/S10-8A)
    A-OPTREF ← R-OPTREF/G-OPTREF
    A-DUP ← R2/R3/G-DUP (cross-mock, --mockN self-exclude)
    A-KINT/A-KBAL/A-KPAT ← K-INT/K-BAL/K-PAT (on Step-8's DERIVED key, §11)
    A-HEADER ← R8b/G-PREQ1 (Step 7 pre-Q.1 body-block ban; strip if present)
    STEP-8-ONLY: A-ZIP, A-ENCODING (U+FFFD), A-SCRIPT (language-conditioned, RA-10),
                 A-INTEGRITY (P0.5 input corruption/truncation)

  COMPLETION GATE (Phase-3 mechanical Part-B/§7 enforcement — S5-1A):
    C1 batches-complete · C2 all-questions-reviewed · C3 all-status-closed ·
    C4 B-UNIQUE/A-MSQ-KEY ran · C5 facts sourced + saved file exists (RA-11) ·
    C6 artefacts stamped + montage/trace file exists (RA-19) · C7 coverage totals match
    → prints COMPLETION-GATE: PASS; required by §12-2 / MANDATE B / MANDATE D.

  PART B (semantic — Claude reasoning, §6):
    B-SOLVE/B-UNIQUE ← R-ANSWER/G-UNIQUE · B-DISTRACT ← wrong-option quality
    B-STEMOPT ← R17 · B-OPTREF-SEM ← R-OPTREF (semantic half)
    B-FACT ← live web-verification + saved evidence (RA-11; Step-7 had no live check)
    B-PASSAGE ← passage/cloze derivability · B-LEAK ← inter-question leakage
    B-ALLOC ← R6/G-ALLOC-SUBTOPIC (observable re-derivation, §6-4)
    B-MANDATE ← manifest mandatory_every_mock/alternation_groups (+ G-CISINCHECK class)
    B-SCENARIODUP ← G-CONCEPTDUP (observable) · B-PRESENTDUP ← G-FORMATDUP/R19 (observable)
    B-DIFF ← difficulty_schedule (advisory)

  §7 (visual/structured — view/recompute; evidence-saved):
    V-image (view every) ← R-FIGURAL/G-FIGURAL-COMPOSITE/G-FIGTEXT/G-FIGTEXT-PROSE + transformation truth (v2.4: stem_only Qs verified for problem image presence)
    V-table/matrix/chart (parse+recompute) ← DI/match self-containment + answer derivability
    V-omml (extract+recompute+render-verify) ← R-MATH-OMML

  NONE of the Step-7 57 gates is dropped: each is either re-run by audit.py (machine),
  re-derived in §6 (the sidecar-dependent ones, observable form), or subsumed by §7
  (visual). Step-8-only additions: A-ZIP, A-ENCODING, A-SCRIPT, A-INTEGRITY, B-FACT
  (live), the §7 view/recompute mandates, and the S5-1A completion gate.

# ════════════════════════════════════════════════════════════════════════
# §17 — EDGE-CASE PLAYBOOK
# ════════════════════════════════════════════════════════════════════════
  | Scenario | Action |
  |---|---|
  | audit.py missing | HARD STOP (MANDATE A) — auto-generated by Step 6 v1.20+; verify Step 6 outputs uploaded. Fallback: copy from Framework_MockTestCreate.md Appendix A (must be the v2.6 canonical auditor — §21). |
  | audit.py self-test not a fixture-based N/N (N>=AUTH_GATE_FLOOR) | HARD STOP (P1 hardened) — a constant-print PASS is REJECTED; regenerate the canonical auditor. |
  | audit.py truncated but --self-test prints PASS | HARD STOP (P0.5 ast.parse + P1 hardened) — hollow/constant self-test rejected; regenerate from Appendix A / Step 6 B3. |
  | *.json input fails to parse / missing required keys (truncated/corrupt) | HARD STOP (P0.5 / A-INTEGRITY) — re-upload intact; never audit against a truncated blueprint/registry. |
  | section_rules empty or missing EXAM_STRUCTURE header | HARD STOP (P0.5 / A-INTEGRITY) — re-upload intact. |
  | Phase 2 skipped / spot-checked instead of batched | IMPOSSIBLE to certify — completion gate (S5-1A) fails C1/C2; MANDATE B / MANDATE D block delivery. |
  | Ledger fabricated with stamps but no evidence files | Caught — S5-1A C5/C6 fail (named montage/fact/trace file absent); certification blocked. |
  | Autonomous/"don't pause" preference given | Waive the inter-batch pause ONLY (RA-15b / S4-3A); every question still audited + stamped + evidenced (RA-15a / RA-0). |
  | Trigger N ≠ filename N ≠ title N | HARD STOP (S2-2) — ask; wrong N corrupts re-sync + dedup. |
  | registry.mocks_completed doesn't end with N | HARD STOP (S2-2) — upload the registry delivered with this docx. |
  | Only docx uploaded, registry missing | HARD STOP (P0) — registry is required (dedup + re-sync). |
  | registry lags by an earlier mock | Cross-mock dedup PARTIAL — log as §19 limitation; audit proceeds. |
  | docx < 50 KB | WARN — verify N; tiny paper is suspicious. |
  | image rId unresolved | HARD STOP (A-ZIP) — structural break; the generating step must re-emit. |
  | U+FFFD in text | RG — encoding corruption; regenerate the affected run/question. |
  | Non-ASCII script present | Flag ONLY if language=='english' (RA-10); else legitimate. |
  | Composite figural panel (figures correct) | CP-FIGDECOMP — re-slice into discrete images. |
  | Composite figural panel (a figure wrong) | RG — regenerate the question + figures. |
  | Math shipped as raster | View (S5-3); if algebra → CP-MATHOMML; if mis-named figure → CP-IMGNAME. |
  | Zero OMML but a quantitative section exists | Investigate (S7-5) — math is hiding as ASCII/raster; resolve. |
  | Underline faked as "(underlined: X)" or "____" | CP-UNDERLINE — real <w:u> run. |
  | Stimulus orphaned (lead-in only) | CP-STIMEMBED — embed per member (Model A). |
  | "Q.x and Q.y" cross-reference in a stem | CP — rewrite to singular per-member context (A-STIMORPHAN). |
  | Two defensible answers | RG — disambiguate stem or replace the colliding option (R-ANSWER). |
  | Wrong/unsourceable fact | RG — replace with a web-verified, sourceable fact (save evidence). |
  | DI table values don't yield the keyed answer | RG — regenerate table + dependent answers together. |
  | Impossible/contradictory figure | RG — replace with a valid figure; re-verify dependents. |
  | Escape-option instruction without the option | RG/CP — add the escape option (re-balance) or switch template (R-OPTREF). |
  | Cross-mock duplicate stem/image | RG — regenerate on a new scenario (NEVER delete — RA-8). |
  | Per-subtopic allocation off | RG — regenerate the missing/extra as the needed subtopic_id. |
  | Mandatory subtopic missing | RG — regenerate one question into the mandatory subtopic. |
  | Alternation-group members co-occur | RG — replace one with its alternation partner / a different subtopic. |
  | A batch fix opens a global defect | Resolve in the same batch via the §8-3 loop before ending (RA-7). |
  | Resume after a gap | `... M[N] resume` — reload audit_state; resume at first not-done batch; evidence dir persists (RA-18). |
  | Re-audit of an already-audited mock | Legal — `--mockN N` self-excludes; idempotent (a clean, evidence-complete ledger yields zero fixes and passes S5-1A). |

# ════════════════════════════════════════════════════════════════════════
# §18 — DEFINITION OF DONE / HARD INVARIANTS (ANY violation = do NOT deliver)
# ════════════════════════════════════════════════════════════════════════
  1.  Pre-flight P0–P9 all passed; input integrity clean (P0.5); audit.py fixture
      self-test N/N (N>=AUTH_GATE_FLOOR, P1 hardened); N resolved + registry-aligned.
  2.  Part A: exit 0 on the FINAL whole paper; zero fixable WARN.
  3.  Part B: every question reviewed (zero sampling); zero open content defect.
      (mechanically asserted by S5-1A C2+C3; not self-attested)
  4.  §7: every image rendered-and-viewed; every table/matrix/chart/OMML recomputed;
      zero un-audited visual/structured item (no "[not-viewed]"); all stamped AND their
      evidence files present (RA-4/RA-19). (mechanically asserted by S5-1A C6+C7)
  5.  B-UNIQUE verified for EVERY question (exactly one defensible answer).
      (mechanically asserted by S5-1A C4)
  6.  Every CA/static-GA fact + factual option web-verified with a recorded, SAVED
      source. (mechanically asserted by S5-1A C5)
  7.  B-ALLOC/B-MANDATE/B-SCENARIODUP/B-PRESENTDUP/B-LEAK finalised clean (whole mock).
  8.  Cross-mock dedup run (full, or partial-with-logged-limitation if registry lags).
  9.  Every defect found was RECTIFIED (CP or RG) and re-audited; nothing left open (RA-5).
  10. Every regeneration obeyed the Step-7 contracts + dedup vs whole ledger + registry (RA-6).
  11. Registry re-synced from the FINAL fixed file; §13-3 verification clean; mocks_completed
      unchanged; schema-complete.
  12. Deliverable set == CORE {fixed docx, re-synced registry} PLUS the change-log
      artefact iff ≥1 question was regenerated; nothing else (no key/ledger/state/index/
      montage/evidence) leaked. The change-log is the only artefact permitted to carry
      literal content, it is headed author-only, and it is produced iff regenerations occurred.
  13. present_files called EXACTLY once, only after the certification gate (§12-2 / S5-1A).
  14. Report (§15) built from real STDOUT + findings; MANDATE-0 safe; handoff printed.
  15. No question content ever printed in chat anywhere in the session (MANDATE 0).
  16. Completion gate S5-1A printed COMPLETION-GATE: PASS with --audit-state before
      present_files (MANDATE B). A bare --final (Part A only) never certifies.

# ════════════════════════════════════════════════════════════════════════
# §19 — KNOWN LIMITATIONS (disclose in §R13 of every report)
# ════════════════════════════════════════════════════════════════════════
  • Key adjudication (which option index is correct, as a learner-facing key) is a
    Step-9 responsibility; Step 8 derives a key only to AUDIT uniqueness/correctness/balance.
  • Difficulty labels are self-estimated [estimate]; not independently provable.
  • The registry.question_index Complexity value is CARRIED FORWARD from Step 7
    (authoritative-by-assignment): Step 8 verifies its vocabulary + exact distribution vs
    difficulty_schedule[N] but does NOT independently re-derive the per-question label (difficulty
    is not rendered in the paper). The index's subtopic_id, by contrast, IS independently
    re-derived and certified (§13 step 2b) — the four subtopic_id-derived tags are provable, the
    Complexity tag is not (Contract_QuestionMetadataIndex v1.0, two-tier guarantee).
  • Cross-mock dedup is only as complete as the registry handed in; a lagging registry
    yields partial dedup (logged, not silently passed).
  • Figural transformation correctness and answer uniqueness rest on reviewer reasoning
    over the VIEWED image (no machine proof) — but viewing is mandatory, un-sampled, and
    evidence-backed (the montage that was viewed is saved and its presence is gated).
  • Web-verified facts are correct as of the audit timestamp; later real-world changes
    are outside Step 8's window.
  • Step 8 cannot prove a distractor is wrong in EVERY conceivable context — it proves
    wrongness under every REASONABLE reading (RA-12); genuinely contested conventions are
    pinned via section_rules, never adjudicated ad hoc.
  • COMPLETION-GATE RESIDUAL (v2.6): S5-1A verifies that each stamp names a durable
    evidence file that EXISTS and is non-trivial — it cannot prove the model reasoned
    correctly INSIDE that evidence (that a saved source actually supports the fact, that a
    viewed montage was truly scrutinised). Evidence-binding shrinks the residual to "the
    model would have to produce every montage, saved source and recompute trace — i.e.
    perform the audit — in order to fake having performed it," which is the point at which
    faking and doing converge. This is the structural ceiling of an LLM-driven audit; it is
    not a mathematical guarantee of reasoning correctness, and it is disclosed here rather
    than overclaimed.

# ════════════════════════════════════════════════════════════════════════
# §20 — SUBTOPIC_ID CONTRACT (consumer role — v1.7/v2.4 cross-step authority)
# ════════════════════════════════════════════════════════════════════════
#   Step 8 is a pure CONSUMER of the subtopic_id contract (Step 0 mints; Step 1
#   enforces; Step 7 joins). Step 8 reads subtopic_manifest.json to:
#     • map each question to a subtopic_id (B-ALLOC) by matching its rendered content
#       to section_rules patterns keyed by id — never by display-name string-match;
#     • read mandatory_every_mock[] + alternation_groups{} (B-MANDATE);
#     • re-derive presentation_family / concept_group hints (manifest carries them) for
#       B-SCENARIODUP / B-PRESENTDUP.
#   Step 8 NEVER mints an id and NEVER joins on a display name. A question that cannot be
#   mapped to any manifest subtopic_id is itself a defect (it does not belong to the
#   blueprint allocation) → investigate + RG. The id recipe and contract carry zero
#   exam-specific values (Step 0 §15).

# ════════════════════════════════════════════════════════════════════════
# §21 — CROSS-FILE PROPAGATION & REGRESSION LOCK (v2.6 — apply IN LOCKSTEP)
# ════════════════════════════════════════════════════════════════════════
#   The v2.6 completion gate + hardened self-test do NOT reach the ~200 exams if they
#   live only in this spec's PROSE. The audit.py each exam actually runs is BORN in the
#   Step-6 generator, per exam. Therefore these changes MUST be applied together:
#
#   | File | Required change (P0 — without it the fix is inert for real exams) |
#   |---|---|
#   | THIS file (Appendix A) | The canonical auditor: --audit-state + C1–C7 completion |
#   |                        | gate + the fixture-based self-test (already below).       |
#   | Framework_Blueprint.md §13-7A (the Step-6 B3 generator) | Generate EXACTLY this   |
#   |   canonical script — NOT the 13-gate constant-print MVP. This is where the auditor |
#   |   the Step-8 run executes is created; if the generator still emits the hollow stub,|
#   |   P1 (hardened) will HARD STOP every exam until it is fixed here. Retire the MVP    |
#   |   `def self_test(): print("SELF-TEST: 13/13 PASS")` stub.                          |
#   | Framework_MockTestCreate.md Appendix A (transitional template source) | Replace the|
#   |   AUDIT_SCRIPT_CONTENT constant-print self_test with the fixture-based one; add     |
#   |   --audit-state + C1–C7. Retire the "GATE-COUNT CONTRACT accepts ANY N/N" clause —  |
#   |   it must accept ONLY a fixture-based N/N with N>=AUTH_GATE_FLOOR.                   |
#   | validate_framework_md.py | Add the 6 regression tests below + a check that MANDATE  |
#   |   B / RA-0 / RA-15a / RA-15b / S4-3A / S5-1A / P0.5 headings all exist and          |
#   |   cross-refs resolve.                                                               |
#   | Framework_MockTestExplainAudit.md (Step 10) + Framework_MockTestExplain.md §18      |
#   |   (Step 9 self-audit) | Same false-clean chain (Claude-driven Part-B-style          |
#   |   certification behind prose). Apply the parallel completion-gate pattern so a bad  |
#   |   explanation / answer-key set cannot ship the way a bad paper did.                 |
#   | Framework_DeliveryFooter.md | No change; F2 already fires only post-certification.  |
#   |   Its correctness now depends on S5-1A actually gating certification.               |
#
#   REGRESSION TESTS (add to validate_framework_md.py / the Appendix A self-test — a
#   build that passes all seven is provably immune to the exact failure that occurred):
#     1. SKIPPED-PHASE-2: audit_state with batches_done=[] and empty ledger; run
#        --final --audit-state → MUST exit non-zero, COMPLETION-GATE failing C1+C2.
#     2. PARTIAL-REVIEW: ledger with total_questions-1 entries → MUST fail C2 naming
#        the missing Q.
#     3. UNSOURCED-FACT: a factual entry with fact_sources=[] (or a named file absent)
#        → MUST fail C5.
#     4. UNVIEWED-FIGURE: a figural entry with no 'image' stamp (or its montage file
#        absent) → MUST fail C6.
#     5. HOLLOW-SELF-TEST: a script whose self_test() only prints "N/N PASS" with no
#        fixtures → MUST be rejected at P1 (fixture-based check fails / N<floor).
#     6. TRUNCATED-INPUT: a blueprint.json cut mid-object → MUST HARD STOP at P0.5
#        (A-INTEGRITY), not proceed.
#     7. HEADER-TOKEN-FALSE-POSITIVE (v2.7.5 — A-INTEGRITY-FALSEPOS-01): run P0.5 against
#        a section_rules.md fixture built by literally invoking (or byte-for-byte
#        replicating the header-writing portion of) Step 5's write_section_rules() —
#        i.e., a real, complete, well-formed file using the actual '=== EXAM_STRUCTURE
#        ===' token. MUST NOT raise HARD STOP (P0.5 / A-INTEGRITY). This is the
#        regression fixture that would have caught the exact false-positive defect that
#        blocked every exam's Step 8 on framework builds v2.6-v2.7.4 (fixed at v2.7.5) —
#        empirically verified via a 5-fixture harness (valid file / empty file / early
#        truncation / pre-v2.3 legacy file / valid file containing an unrelated
#        "same_category" substring), all five behaving correctly post-fix. Paired with
#        validate_framework_md.py Check T (§6.3), which catches this defect class
#        automatically at spec-authoring time by cross-checking every consumer's literal
#        hard-stop pattern against the actual producer output, across all files in a
#        batch run — not just this one instance.
#
#   THE UNIFYING PRINCIPLE (why this closes the chain across all 200 exams): every
#   certification claim is the EXIT CODE OF A COMMAND, never a sentence the model writes
#   about itself. Where a check is Claude-driven (semantic, visual, factual), it deposits
#   a stamp AND a durable evidence artefact in a machine-readable ledger, and a runnable
#   gate verifies both before delivery. Prose describes; only code certifies.

# ════════════════════════════════════════════════════════════════════════
# APPENDIX A — UNIVERSAL EXAM-AGNOSTIC mock_test_audit.py (MANDATE A)
# ════════════════════════════════════════════════════════════════════════
#   v2.2 NOTE: This script is now AUTO-GENERATED by Step 6 (MockBlueprint) v1.20+
#   as its 6th output file. Users no longer need to copy it manually.
#   See Framework_Blueprint.md §13-7A for generation rules and lifecycle.
#   v2.6 NOTE: This is the CANONICAL auditor. Step 6 §13-7A + Framework_MockTestCreate.md
#   Appendix A MUST generate EXACTLY this (with the --audit-state completion gate and the
#   fixture-based self-test) — NOT the retired 13-gate constant-print MVP (§21). MANDATE A
#   (P1 hardened) REJECTS any script whose self-test is not fixture-based with N>=35.
#
#   The script below is RETAINED as a FALLBACK for cases where Step 6 was run
#   before v1.20 (legacy). If the script is missing from project Files:
#     PREFERRED: re-run Step 6 B3 (generates the script automatically).
#     FALLBACK:  copy the script below verbatim, save as [ExamCode]_mock_test_audit.py,
#                upload to the [ExamCode] project Files.
#   No exam-specific edits are required (it parameterises itself entirely from
#   blueprint.json + section_rules.md + subtopic_manifest.json + registry.json).
#   MANDATE A requires it for Step 8.
#
#   Validation status (v2.6):
#     • `--self-test`  → SELF-TEST: 47/47 PASS  (exit 0). The 35 v2.5 tests cover every
#       gate plus the edge cases (roman/alpha/figural option labels; an enumerated
#       passage point that must NOT inflate the option count; accented-Latin and
#       Greek-math text that must NOT trip A-SCRIPT; a Devanagari word that MUST trip
#       it on an english exam and pass on a hindi one; attribute-order-independent rels
#       parsing; the v1.2 MSQ cases; the v1.4 NAT cases; the v1.5 A-SECHDR-name-catch;
#       a 0-block document that must not crash) PLUS 8 v2.6 COMPLETION-GATE fixtures
#       (S5-1A C1–C7): a complete evidence-backed ledger ⇒ COMPLETION-GATE PASS; a
#       skipped Phase 2 ⇒ C1+C2 FAIL; a partial review ⇒ C2 FAIL; an unsourced fact ⇒
#       C5 FAIL; a fact whose saved file is missing ⇒ C5 FAIL; a paper artefact with no
#       ledger stamp ⇒ C7 FAIL; a stamp whose evidence file is missing ⇒ C6 FAIL; a
#       stamp whose evidence file exists ⇒ PASS. PLUS 2 v2.7 A-HEADER-inversion fixtures
#       (a pre-Q.1 title/info block ⇒ A-HEADER FAIL i.e. strip; the SAME block with
#       EXAM_STRUCTURE paper_header_block declared ⇒ dormant, no failure). PLUS 2 v2.7.1
#       A-MATCH-TABLE fixtures (a MATCH question rendered WITHOUT a table ⇒ A-MATCH-TABLE
#       FAIL; the same MATCH body rendered AS a real table ⇒ dormant, no failure).
#     • AUTH_GATE_FLOOR = 35 (MANDATE A / P1). N (47) >= floor.
#     • run against a real 100-question paper → parses all 100 blocks; the
#       blueprint-driven gates (A-COUNT 100/100, A-SEQ 1..100, A-SECCOUNT
#       25/25/25/25) pass; A-OPTN correctly reads 4 image-options on figural
#       questions (no false FAIL); A-OMML-FLOOR raises the "zero OMML in a
#       quant paper → math may be hiding as raster" flag; A-FIGCOMP-LINE
#       catches a genuine two-rasters-on-one-line defect. No false positives
#       on legitimate figural images named "Picture N" (the emitter-naming gap
#       — handled by the view-backed two-tier A-MATHRASTER, S5-3). With
#       --final --audit-state on a certified run → COMPLETION-GATE: PASS.
#
#   Dependency-light: python-docx + Python stdlib only. Exit 0 iff no FAIL AND (when
#   --audit-state is given) COMPLETION-GATE: PASS; WARNs are surfaced for Part-B / §7
#   reviewer adjudication (the Step-8 certification gate, §12-2, decides whether a
#   fixable WARN blocks delivery).
#
#   USAGE:
#     python3 [ExamCode]_mock_test_audit.py --self-test
#     python3 [ExamCode]_mock_test_audit.py PAPER.docx \
#         --blueprint BP.json --rules RULES.md --manifest MAN.json \
#         --registry REG.json --mockN N --final
#     python3 [ExamCode]_mock_test_audit.py PAPER.docx \
#         --blueprint BP.json --rules RULES.md --manifest MAN.json \
#         --registry REG.json --mockN N --final \
#         --audit-state [ExamCode]_M[N]_audit_state.json     # Phase-3 completion gate (S5-1A)
#
#   The script body follows (save the fenced content below as the .py file):

```python
#!/usr/bin/env python3
# ============================================================================
# [ExamCode]_mock_test_audit.py
# UNIVERSAL, EXAM-AGNOSTIC Part-A machine-gate auditor for Step 8
# (Framework_MockTestCreateAudit v2.6, Appendix A).
#
# Zero hardcoded exam values: every expected value (question/section counts,
# q_ranges, options_count, option label format, language, OMML-required
# subtopics, figural/linked maps) is read at runtime from blueprint.json /
# section_rules.md / subtopic_manifest.json / registry.json. The SAME script
# audits any exam with valid Step 0/1/2 outputs.
#
# v2.6 — adds the S5-1A COMPLETION GATE (--audit-state): after Part A, validates
# the Phase-2 audit_state ledger (C1-C7) and the on-disk evidence artefacts each
# stamp names, so a skipped/collapsed Phase 2 fails LOUDLY instead of shipping.
# The self-test is FIXTURE-BASED (MANDATE A / P1): a constant-print stub is not a
# valid auditor.
#
# Dependencies: python-docx + Python stdlib ONLY.
#
# Usage:
#   python3 [ExamCode]_mock_test_audit.py PAPER.docx \
#       --blueprint BP.json --rules RULES.md --manifest MAN.json \
#       --registry REG.json --mockN N [--final] [--audit-state STATE.json]
#   python3 [ExamCode]_mock_test_audit.py --self-test
#
# Exit code: 0 if no FAIL AND (when --audit-state) COMPLETION-GATE PASS, else 1.
# WARNs are printed for reviewer adjudication (Part B / §7) and do not change the
# exit code; the Step-8 certification gate (spec §12-2) decides whether a fixable
# WARN blocks delivery.
# ============================================================================
import sys, os, re, json, hashlib, zipfile, argparse, tempfile, unicodedata
from pathlib import Path
from collections import Counter, defaultdict

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.document import Document as _DocClass

# ---- OOXML namespaces ------------------------------------------------------
W  = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M  = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
A  = 'http://schemas.openxmlformats.org/drawingml/2006/main'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
def W_(t):  return f'{{{W}}}{t}'
def M_(t):  return f'{{{M}}}{t}'

# ---- v2.6 constants (MANDATE A / S5-1A) ------------------------------------
AUTH_GATE_FLOOR   = 35    # P1: the self-test must exercise >= this many fixtures.
EVIDENCE_MIN_BYTES = 100  # S5-1A C6: a montage evidence file must be a real raster.

# ---- result accumulator ----------------------------------------------------
RESULTS = []   # list of (level, code, message)
def _ok(c, m):   RESULTS.append(('OK',   c, m))
def _warn(c, m): RESULTS.append(('WARN', c, m))
def _fail(c, m): RESULTS.append(('FAIL', c, m))
def _reset():    RESULTS.clear()

# ---- block model -----------------------------------------------------------
QNUM_RE = re.compile(r'^\s*Q\.?\s*(\d+)\b')

class Block:
    __slots__ = ('qnum', 'items', 'paras', 'tables', 'images')
    def __init__(self, qnum):
        self.qnum = qnum
        self.items = []       # ordered ('p',Paragraph) / ('t',Table)
        self.paras = []       # Paragraph objects in this block
        self.tables = []      # Table objects in this block
        self.images = []      # reserved


def iter_block_items(doc):
    """Yield Paragraph and Table objects in true document order."""
    body = doc.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield ('p', Paragraph(child, doc))
        elif child.tag == qn('w:tbl'):
            yield ('t', Table(child, doc))


def para_text(p):
    """Readable text of a paragraph, merging normal text (w:t) and math (m:t)
    in document order so a math-bearing or pure-OMML stem is never seen empty."""
    out = []
    for node in p._element.iter():
        if node.tag == W_('t') or node.tag == M_('t'):
            out.append(node.text or '')
    return ''.join(out)


def para_images(p):
    """Return [(docPr_name, blip_rEmbed)] for inline images in this paragraph."""
    imgs = []
    el = p._element
    names = el.findall(f'.//{{{WP}}}docPr')
    blips = el.findall(f'.//{{{A}}}blip')
    embeds = [b.get(qn('r:embed')) for b in blips]
    for i, emb in enumerate(embeds):
        nm = names[i].get('name') if i < len(names) else None
        imgs.append((nm, emb))
    return imgs


def parse_blocks(doc):
    """Split the document body into per-question blocks. Items before the first
    Q.<n> are the title/instruction block (returned separately)."""
    blocks, title_items = [], []
    cur = None
    for kind, obj in iter_block_items(doc):
        if kind == 'p':
            mobj = QNUM_RE.match(para_text(obj))
            if mobj:
                cur = Block(int(mobj.group(1)))
                blocks.append(cur)
        if cur is None:
            title_items.append((kind, obj))
            continue
        cur.items.append((kind, obj))
        if kind == 'p':
            cur.paras.append(obj)
        else:
            cur.tables.append(obj)
    return title_items, blocks


# ---- source-file parsing (exam-agnostic) -----------------------------------
def cat_c(rules_txt, key, default=None):
    mobj = re.search(rf'^[ \t]*{re.escape(key)}[ \t]*[:=][ \t]*(.+?)[ \t]*$',
                     rules_txt, re.M | re.I)
    return mobj.group(1).strip() if mobj else default


def load_sources(args):
    src = {}
    src['blueprint'] = json.load(open(args.blueprint, encoding='utf-8')) if args.blueprint else {}
    src['registry']  = json.load(open(args.registry,  encoding='utf-8')) if args.registry  else {}
    src['manifest']  = json.load(open(args.manifest,  encoding='utf-8')) if args.manifest  else {}
    src['rules_txt'] = open(args.rules, encoding='utf-8').read() if args.rules else ''
    bp = src['blueprint']
    src['total_questions'] = bp.get('total_questions')
    src['sections'] = bp.get('sections', [])
    rt = src['rules_txt']
    src['language']      = (cat_c(rt, 'language', 'english') or 'english').lower()
    src['options_count'] = int(cat_c(rt, 'options_count', '4'))
    src['opt_label_fmt'] = cat_c(rt, 'option_label_format', '1/2/3/4')
    src['font_family']   = cat_c(rt, 'font_family', 'Calibri')
    # OMML-required subtopics present at all?
    src['omml_required_present'] = bool(re.search(r'OMML_required\s*[:=]\s*(true|yes|1)',
                                                  rt, re.I))
    # mock-scoped maps from registry
    N = args.mockN
    reg = src['registry']
    rc  = next((x for x in reg.get('rc_manifests', []) if x.get('mock') == N), None)
    src['passage_linked'] = set(rc.get('passage_linked', [])) if rc else set()
    src['cloze_linked']   = set(rc.get('cloze_linked', []))   if rc else set()
    fig = next((x for x in reg.get('figural_manifests', []) if x.get('mock') == N), None)
    src['figural_qs'] = set(int(q) for q in fig.get('figural_qs', [])) if fig else set()
    # v2.4: section_rules full text for image_role lookups in gate_images
    src['section_rules_text'] = rt   # already loaded at src['rules_txt']
    # v2.4: concept_map — Step 8 does NOT receive the answer_key sidecar (S0-1),
    # so concept_map is unavailable by default. If the answer_key is available
    # (e.g., passed via --key), load it; otherwise empty dict (gate_images falls
    # back to default image_role='stem_and_options' per subtopic).
    src['concept_map'] = {}
    if getattr(args, 'key', None) and Path(args.key).exists():
        _key_data = json.load(open(args.key, encoding='utf-8'))
        src['concept_map'] = _key_data.get('concept_map', {})

    # v1.2 — MSQ re-derivation (INDEPENDENT of any Step-7 self-report). Dormant when the
    # blueprint declares no multi subtopics (every value below is empty/zero ⇒ the MSQ
    # gates pass vacuously and behave exactly as v1.1).
    src['multi_present'] = bool(bp.get('multi_present', bp.get('msq_present', False)))  # Phase-0 back-compat
    multi_ids = {s.get('subtopic_id') for s in bp.get('subtopic_list', [])
                 if s.get('answer_cardinality', s.get('answer_mode')) == 'multi'}
    src['multi_subtopic_ids'] = multi_ids
    # expected count of multi-mode questions per section, from THIS mock's allocations.
    mock_entry = next((m for m in bp.get('mocks', []) if m.get('mock') == N), None)
    exp = {}
    if mock_entry and multi_ids:
        for sec in mock_entry.get('sections', []):
            c = sum(sa.get('q_count', 0) for sa in sec.get('subtopic_allocations', [])
                    if sa.get('subtopic_id') in multi_ids)
            if c:
                exp[sec.get('section_name')] = c
    src['expected_multi_by_section'] = exp
    # MSQ config (section_rules / blueprint) — read where needed, never from a sidecar.
    mc = bp.get('msq_contract', {})
    src['msq_k_mode'] = mc.get('msq_k_mode', 'variable')
    src['msq_k']      = mc.get('msq_k', None)
    src['msq_allow_aota'] = bool(re.search(r'^\s*msq_allow_aota\s*:\s*true\s*$', rt, re.I | re.M))
    # select-instruction phrases: exam's own (section_rules msq_instruction[_hi]) + universal.
    phrases = []
    for m in re.finditer(r'^\s*msq_instruction(?:_hi)?\s*:\s*(.+?)\s*$', rt, re.I | re.M):
        phrases.append(m.group(1).strip().strip('()'))
    src['msq_instruction_phrases'] = phrases + [
        'one or more', 'may be correct', 'select two', 'select three',
        'select all that apply', 'एक या अधिक']

    # v1.4 — NAT re-derivation (INDEPENDENT of any Step-7 self-report). Dormant when the
    # blueprint declares no numerical subtopics (every value below empty/zero ⇒ the NAT
    # gates pass vacuously and behave exactly as v1.3).
    src['nat_present'] = bool(bp.get('nat_present', False))
    nat_ids = {s.get('subtopic_id') for s in bp.get('subtopic_list', [])
               if s.get('answer_type', 'option') == 'numerical'}
    src['nat_subtopic_ids'] = nat_ids
    # expected count of numerical questions per section, from THIS mock's allocations.
    nexp = {}
    if mock_entry and nat_ids:
        for sec in mock_entry.get('sections', []):
            c = sum(sa.get('q_count', 0) for sa in sec.get('subtopic_allocations', [])
                    if sa.get('subtopic_id') in nat_ids)
            if c:
                nexp[sec.get('section_name')] = c
    src['expected_nat_by_section'] = nexp
    # v1.4 (ND6): per-question EXPECTED option count from the registry (Step-7 delivery
    # contract, NOT a self-audit sidecar). 0 marks a NAT question. Used to SKIP the option
    # gates for NAT Qs; A-NAT-NOOPT then independently verifies each claimed-NAT Q truly
    # renders 0 options (and A-OPTN still fires if a claimed-MCQ Q renders 0) — so a
    # mislabelled options_by_q cannot let a defect through either direction. {} ⇒ inert.
    src['options_by_q'] = {str(k): v for k, v in
                           reg.get('options_by_q', {}).get(str(N), {}).items()}
    # NAT config (blueprint nat_contract) — read where needed, never from a sidecar.
    nc = bp.get('nat_contract', {})
    src['nat_answer_type'] = nc.get('nat_answer_type', 'real')
    src['nat_tolerance']   = nc.get('nat_tolerance', '0')
    # numerical-entry instruction phrases: exam's own (section_rules nat_instruction[_hi]) + universal.
    nphrases = []
    for m in re.finditer(r'^\s*nat_instruction(?:_hi)?\s*:\s*(.+?)\s*$', rt, re.I | re.M):
        nphrases.append(m.group(1).strip().strip('()'))
    src['nat_instruction_phrases'] = nphrases + [
        'numerical value', 'enter your answer', 'enter the value', 'numerical answer',
        'संख्यात्मक मान']
    # figural stem-cue keywords: exam's own (section_rules figural_cue_keywords) if
    # declared, else a universal default set. RA-9: these are never hardcoded in the gate.
    fcue_m = re.search(r'^\s*figural_cue_keywords\s*[:=]\s*(.+?)\s*$', rt, re.I | re.M)
    if fcue_m:
        src['figural_cue_keywords'] = [k.strip().lower() for k in fcue_m.group(1).split(',')]
    # else: gate_images falls back to a built-in default list (see gate_images)
    # escape-reference phrases: if the whole phrase appears in a stem, it references
    # the escape option the phrase implies. Read from section_rules (RA-9);
    # gate_optref falls back to English defaults when absent.
    eref_m = re.search(r'^\s*escape_reference_phrases\s*[:=]\s*(.+?)\s*$', rt, re.I | re.M)
    if eref_m:
        src['escape_reference_phrases'] = [t.strip() for t in eref_m.group(1).split(',')]
    # stimulus detection cues: exam's own (section_rules stimulus_cue_patterns) if
    # declared; gate_stimorphan merges them with the built-in English cues. RA-9.
    scue_m = re.search(r'^\s*stimulus_cue_patterns\s*[:=]\s*(.+?)\s*$', rt, re.I | re.M)
    if scue_m:
        src['stimulus_cue_patterns'] = [c.strip() for c in scue_m.group(1).split(',')]
    # mock title keyword: exam's own (section_rules mock_title_keyword) if declared,
    # else default 'mock'. RA-9: gate_header reads from src.
    src['mock_title_keyword'] = cat_c(rt, 'mock_title_keyword', 'mock')
    # v2.7: paper_header_block opt-in (gate_header / A-HEADER dormancy). Default OFF — no
    # current section_rules declares it, so the pre-Q.1 body-block ban is absolute.
    src['paper_header_block'] = str(cat_c(rt, 'paper_header_block', '')).strip().lower() \
        in ('true', '1', 'yes', 'on')
    return src


def option_label_family(fmt):
    first = (fmt or '1/2/3/4').split('/')[0].strip().strip('()').strip('.').strip(')')
    if first.isdigit():                         return 'num'
    if re.fullmatch(r'[ivxIVX]+', first):       return 'roman'
    if len(first) == 1 and first.isalpha():     return 'alpha'
    return 'num'

OPT_RE = re.compile(r'^\s*\(?\s*([0-9]+|[A-Za-z]|[ivxIVX]+)\s*\)?\s*[.)]\s+\S')
# bare-or-full option label (figural options are a bare '1.' label paragraph
# followed by an image paragraph; text options are 'label. text').
OPT_LABEL_RE = re.compile(r'^\s*\(?\s*([0-9]+|[A-Za-z]|[ivxIVX]+)\s*\)?\s*[.)](\s|$)')

def option_paras(block):
    """Paragraphs in the block that look like labelled options."""
    out = []
    for p in block.paras:
        t = para_text(p)
        if QNUM_RE.match(t):      # never the Q.<n> line
            continue
        mobj = OPT_RE.match(t)
        if mobj:
            out.append((mobj.group(1), p, t))
    return out


def block_stem_text(block):
    """All non-option paragraph text in the block, with the leading 'Q.<n>'
    token stripped. In the Step-7 format the stem lives ON the Q.<n> line
    (e.g. 'Q.74  Study the following table ...'), so the Q.<n> paragraph must
    be INCLUDED (prefix removed), not excluded."""
    parts = []
    for p in block.paras:
        t = para_text(p)
        if OPT_LABEL_RE.match(t):
            continue
        t = QNUM_RE.sub('', t, count=1).strip()
        if t:
            parts.append(t)
    return ' '.join(parts)


# ============================================================================
# GATES
# ============================================================================
STIMULUS_CUES = re.compile(
    r'\b(the passage|the table|the graph|the chart|the given data|the following '
    r'(table|passage|graph|chart|bar|pie|line|data)|blank\s*\(|according to the '
    r'passage|read the (passage|following passage))\b', re.I)
CROSSREF_RE = re.compile(r'Q\.?\s*\d+\s*(and|to|&|–|-)\s*Q?\.?\s*\d+', re.I)
UNDERLINE_REF = re.compile(r'\bunderlin(e|ed)\b', re.I)
FAKE_UNDERLINE = re.compile(r'\(\s*underlin(e|ed)[^)]*:', re.I)
ESCAPE_TOKENS_DEFAULT = [
    r'no error', r'no improvement', r'none of (these|the above|them)',
    r'all of the above', r'both .+ and ', r'neither .+ nor ']
MATH_TOKEN_NAME = re.compile(r'_(e\d+|eqn|expr|frac|math)\b', re.I)
CANON_IMG_NAME = re.compile(r'^q\d+_(problem|opt\d+|stim)', re.I)
ASCII_CARET = re.compile(r'[A-Za-z0-9]\s*\^\s*[0-9A-Za-z]')
SLASH_FRAC  = re.compile(r'(?<![A-Za-z0-9])\d+\s*/\s*\d+(?![A-Za-z0-9])')


def gate_structure(blocks, src):
    tq = src['total_questions']
    nums = [b.qnum for b in blocks]
    if tq is not None:
        (_ok if len(blocks) == tq else _fail)(
            'A-COUNT', f'{len(blocks)} question blocks (expected {tq}).')
        expected = set(range(1, tq + 1))
        got = set(nums)
        if got == expected:
            _ok('A-SEQ', f'Q-numbers complete 1..{tq}.')
        else:
            miss = sorted(expected - got); extra = sorted(got - expected)
            _fail('A-SEQ', f'missing={miss[:10]} extra={extra[:10]}.')
    else:
        _warn('A-COUNT', 'blueprint.total_questions absent; count check skipped.')
    if nums == sorted(nums) and len(nums) == len(set(nums)):
        _ok('A-MONO', 'Q-numbers strictly increasing.')
    else:
        _fail('A-MONO', 'Q-numbers not strictly increasing in document order.')


def gate_seccount(blocks, src):
    secs = src['sections']
    if not secs:
        _warn('A-SECCOUNT', 'blueprint.sections absent; section-count check skipped.')
        return
    nums = set(b.qnum for b in blocks)
    bad = []
    for s in secs:
        lo, hi = s['q_range']
        cnt = sum(1 for q in nums if lo <= q <= hi)
        if cnt != s.get('total_qs', hi - lo + 1):
            bad.append(f"{s.get('name','?')}:{cnt}/{s.get('total_qs', hi-lo+1)}")
    (_ok if not bad else _fail)('A-SECCOUNT',
        'section counts match q_ranges.' if not bad else 'mismatch ' + '; '.join(bad))


def _label_paras(block):
    """All option-label paragraphs in the block (bare '1.' or full '1. text'),
    in document order, as (token, full_text, text_after_label)."""
    out = []
    for p in block.paras:
        t = para_text(p)
        if QNUM_RE.match(t):
            continue
        m = OPT_LABEL_RE.match(t)
        if m:
            out.append((m.group(1), t, t[m.end():].strip()))
    return out


def _fam_of(l):
    if l.isdigit():
        return 'num'
    if re.fullmatch(r'[ivxIVX]+', l):
        return 'roman'
    return 'alpha'


def _idx_of(l, fam):
    if l.isdigit():
        return int(l)
    if fam == 'roman':
        seq = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
        return seq.index(l.lower()) + 1 if l.lower() in seq else 0
    return ord(l.lower()) - ord('a') + 1


def gate_options(blocks, src):
    oc = src['options_count']; fam = option_label_family(src['opt_label_fmt'])
    obq = src.get('options_by_q', {})   # v1.4: per-Q expected option count (0 = NAT)
    bad_n, bad_lab, bad_ord, bad_uni = [], [], [], []
    for b in blocks:
        # v1.4 NAT: a numerical question expects 0 options — the option gates (A-OPTN/
        # A-OPTLABEL/A-OPTORDER/A-OPTUNIQUE) DO NOT APPLY to it. Skip when the registry
        # marks it 0-option; A-NAT-NOOPT separately verifies it truly renders no options.
        if str(b.qnum) in obq and obq[str(b.qnum)] == 0:
            continue
        labs = _label_paras(b)
        # Options are the TRAILING oc label-paragraphs (Step-7 puts the option
        # block last). A stray earlier label (e.g. an enumerated passage point
        # '1. ...') is ignored, so it never inflates the count; a genuinely short
        # option set (< oc labels) still FAILs.
        if len(labs) < oc:
            bad_n.append(f'Q{b.qnum}:{len(labs)}')
            continue
        opt_labs = labs[-oc:]
        tokens = [x[0] for x in opt_labs]
        texts  = [x[2].casefold() for x in opt_labs]
        if any(_fam_of(t) != fam for t in tokens):
            bad_lab.append(f'Q{b.qnum}')
        idxs = [_idx_of(t, fam) for t in tokens]
        if 0 in idxs or idxs != list(range(idxs[0], idxs[0] + oc)):
            bad_ord.append(f'Q{b.qnum}')
        # text-uniqueness applies only when options are TEXT (figural options are
        # bare labels followed by images → empty text → uniqueness checked in §7).
        nonempty = [x for x in texts if x]
        if len(nonempty) == oc and len(set(nonempty)) != oc:
            bad_uni.append(f'Q{b.qnum}')
    (_ok if not bad_n else _fail)('A-OPTN',
        f'every Q has {oc} options.' if not bad_n else 'wrong count: ' + ' '.join(bad_n[:15]))
    (_ok if not bad_lab else _fail)('A-OPTLABEL',
        'labels match format.' if not bad_lab else 'bad label family: ' + ' '.join(bad_lab[:15]))
    (_ok if not bad_ord else _fail)('A-OPTORDER',
        'options in order.' if not bad_ord else 'out of order: ' + ' '.join(bad_ord[:15]))
    (_ok if not bad_uni else _fail)('A-OPTUNIQUE',
        'options distinct within Q.' if not bad_uni else 'dup options: ' + ' '.join(bad_uni[:15]))


def gate_qnfirst(blocks):
    """Q.N-FIRST (R14): nothing may precede a block's Q.<n>. Because the parser
    starts a block at Q.<n>, the violation manifests as stimulus content (table /
    image / long passage) sitting AFTER the previous block's last option and
    BEFORE the next block's Q.<n> — i.e. a lead-in orphaned ahead of its Q.N.
    It is attributed to the block whose Q.<n> it precedes."""
    viol = []
    for k, b in enumerate(blocks):
        last_opt = -1
        for idx, (kind, obj) in enumerate(b.items):
            if kind == 'p' and OPT_RE.match(para_text(obj)):
                last_opt = idx
        if last_opt < 0 or k + 1 >= len(blocks):
            continue
        for kind, obj in b.items[last_opt + 1:]:
            if kind == 't':
                viol.append(f'Q{blocks[k+1].qnum}'); break
            if kind == 'p':
                if para_images(obj):
                    viol.append(f'Q{blocks[k+1].qnum}'); break
                if len(para_text(obj).split()) >= 35:
                    viol.append(f'Q{blocks[k+1].qnum}'); break
    (_ok if not viol else _fail)('A-QNFIRST',
        'every block opens with Q.<n> (no orphaned lead-in).' if not viol else
        'stimulus orphaned before Q.<n>: ' + ' '.join(sorted(set(viol))[:15]))


def gate_blanksep(doc, blocks):
    # blank separator: at least one empty paragraph between the last option of a
    # block and the next block's Q.<n>. Approx: count empty paragraphs overall vs blocks.
    empties = sum(1 for kind, obj in iter_block_items(doc)
                  if kind == 'p' and not para_text(obj).strip()
                  and not para_images(obj))
    (_ok if empties >= max(0, len(blocks) - 1) else _warn)('A-BLANKSEP',
        f'{empties} blank separators for {len(blocks)} blocks.'
        if empties >= len(blocks) - 1 else
        f'only {empties} blank separators for {len(blocks)} blocks (some missing).')


def gate_font(doc, src):
    fam = src['font_family']
    bad = set()
    for kind, obj in iter_block_items(doc):
        if kind != 'p':
            continue
        for r in obj.runs:
            nm = r.font.name
            if nm not in (None, fam):
                bad.add(nm)
    (_ok if not bad else _fail)('A-FONT',
        f'all runs {fam}.' if not bad else f'non-{fam} fonts present: {sorted(bad)[:6]}')


def gate_sechdr(blocks, doc, src):
    # v1.5 — two detectors, over ALL body paragraphs (not only within question blocks, so a
    # heading before Q.1 or between blocks is seen too):
    #   (a) KEYWORD form — text opening with "section"/"part N"/rule characters;
    #   (b) SECTION-NAME form (the realistic case the keyword pattern MISSED): a standalone
    #       paragraph that IS a declared section name ("Quantitative Aptitude", "Technical",
    #       "General Awareness"). PROVENANCE-BASED — matched against the blueprint's own
    #       section names (src['sections']), not a generic word list, so it flags exactly the
    #       headings this paper's sections would produce and stays exam-agnostic.
    # A questions-only paper (R8, Q.N-first) has no standalone non-Q/non-option paragraph, so
    # any body line equal to a section name is a leaked header, never legitimate content.
    pat = re.compile(r'^\s*(section\b|part\s+[IVXA-D0-9]+\b|=====|─────|-----)', re.I)
    sec_names = set()
    for s in src.get('sections', []):
        nm = (s.get('name') or s.get('section_name') or '').strip().lower()
        if nm:
            sec_names.add(nm)
    hits = []
    for kind, obj in iter_block_items(doc):
        if kind != 'p':
            continue
        t = para_text(obj).strip()
        if not t or QNUM_RE.match(t):        # blank or a Q.<n> stem line — never a stray header
            continue
        if (pat.match(t) and len(t) < 60) or (t.lower() in sec_names):
            hits.append(t[:40])
    (_ok if not hits else _fail)('A-SECHDR',
        'no body section headers.' if not hits else 'section-header text in body: ' + ' | '.join(hits[:10]))


def gate_anskey(doc):
    full = '\n'.join(para_text(obj) for kind, obj in iter_block_items(doc) if kind == 'p')
    # v1.2: the last pattern now matches SET-valued keys ("Q.1 → 1,2,4"), not just a
    # single trailing digit/letter — mirrors Step 7 G-ANSWERKEY. A leaked MSQ key is a
    # comma/space list of option positions; the v1.1 single-token pattern missed it.
    pats = [r'\banswer\s*key\b', r'\banswers?\s*:', r'^\s*key\s*:',
            r'Q\.?\s*\d+\s*[:\-–>]+\s*[\(]?[1-9a-dA-D][\)]?(?:\s*[,\s]\s*[\(]?[1-9a-dA-D][\)]?)*\s*$',
            # v1.4: NAT numerical-value answer-key lines ("Q.5 → 47" / "→ 0" / "→ -3" /
            # "→ 3.14"). The option-position pattern above only matches 1-9/a-d, so a leaked
            # NAT key (incl. 0/negative/decimal) slipped through. Mirrors Step 7 v4.7.
            r'Q\.?\s*\d+\s*[:\-–>]+\s*-?\d+(?:\.\d+)?\s*$']
    hit = [p for p in pats if re.search(p, full, re.I | re.M)]
    (_ok if not hit else _fail)('A-ANSKEY',
        'no answer key/markers in body.' if not hit else f'answer-key signal(s): {hit}')


def gate_msq_instr(blocks, src):
    # v1.2 — A-MSQ-INSTR (machine, MULTI only). INDEPENDENT of any Step-7 self-report:
    # the EXPECTED number of multi-mode questions per section is re-derived from the
    # blueprint allocations (src['expected_multi_by_section']); the OBSERVED number is
    # the count of Q blocks in that section's q_range whose stem line carries a select-
    # instruction phrase. A mismatch means a multi Q is missing its instruction (or a
    # single Q wrongly carries one). Pinpointing WHICH Q is refined in Part B (semantic),
    # where the question's subtopic is known from content. Fully dormant when the blueprint
    # declares no multi subtopics (expected map empty ⇒ pass).
    exp = src.get('expected_multi_by_section', {})
    if not exp:
        return _ok('A-MSQ-INSTR', 'no multi-mode subtopics in this mock (dormant).')
    phrases = [p.lower() for p in src.get('msq_instruction_phrases', [])]
    sec_of = src.get('section_of_qnum', {})    # {qnum: section_name} if available
    secs   = src.get('sections', [])
    def section_for(qnum):
        if qnum in sec_of:
            return sec_of[qnum]
        for s in secs:                          # fall back to q_range membership
            lo, hi = (s.get('q_range') or [0, 0])[:2]
            if lo <= qnum <= hi:
                return s.get('section_name') or s.get('name')   # blueprint uses 'name'
        return None
    observed = {}
    for b in blocks:
        stem = para_text(b.paras[0]) if getattr(b, 'paras', None) else getattr(b, 'stem', '')
        if any(ph in stem.lower() for ph in phrases):
            observed[section_for(b.qnum)] = observed.get(section_for(b.qnum), 0) + 1
    bad = [f'{sec}: expected {n} multi, saw {observed.get(sec, 0)} instruction-carrying'
           for sec, n in exp.items() if observed.get(sec, 0) != n]
    (_ok if not bad else _fail)('A-MSQ-INSTR',
        'observed multi instruction counts match the blueprint per section.' if not bad
        else 'multi instruction-count mismatch — ' + ' | '.join(bad))


def gate_nat(blocks, src):
    # v1.4 — A-NAT-NOOPT + A-NAT-INSTR (machine, NUMERICAL only). INDEPENDENT of any
    # Step-7 self-report. Fully dormant when the blueprint declares no numerical subtopics.
    obq = src.get('options_by_q', {})
    nat_present = src.get('nat_present', False)
    # A-NAT-NOOPT: every question the registry marks 0-option (NAT) must render ZERO
    # option-label paragraphs. A-OPTN covers the inverse (a claimed-MCQ Q with too few
    # options) — and if options_by_q is absent, NAT Qs are NOT skipped there, so A-OPTN
    # fails LOUD, surfacing the missing ND6 contract rather than silently passing.
    if nat_present and obq:
        bad_opt = []
        for b in blocks:
            if obq.get(str(b.qnum)) == 0 and len(_label_paras(b)) != 0:
                bad_opt.append(f'Q{b.qnum}:{len(_label_paras(b))}')
        (_ok if not bad_opt else _fail)('A-NAT-NOOPT',
            'every numerical Q renders zero options.' if not bad_opt
            else 'numerical Q carries options: ' + ' '.join(bad_opt[:15]))
    else:
        _ok('A-NAT-NOOPT', 'no numerical subtopics in this mock (dormant).')
    # A-NAT-INSTR: per-section EXPECTED NAT count (re-derived from blueprint allocations,
    # src['expected_nat_by_section']) vs OBSERVED count of Q blocks whose stem carries a
    # numerical-entry instruction phrase. Mismatch ⇒ a NAT Q missing its instruction (or a
    # non-NAT Q wrongly carrying one). Mirrors A-MSQ-INSTR. Dormant when the map is empty.
    exp = src.get('expected_nat_by_section', {})
    if not exp:
        return _ok('A-NAT-INSTR', 'no numerical subtopics in this mock (dormant).')
    phrases = [p.lower() for p in src.get('nat_instruction_phrases', [])]
    secs   = src.get('sections', [])
    sec_of = src.get('section_of_qnum', {})
    def section_for(qnum):
        if qnum in sec_of:
            return sec_of[qnum]
        for s in secs:
            lo, hi = (s.get('q_range') or [0, 0])[:2]
            if lo <= qnum <= hi:
                return s.get('section_name') or s.get('name')
        return None
    observed = {}
    for b in blocks:
        stem = para_text(b.paras[0]) if getattr(b, 'paras', None) else getattr(b, 'stem', '')
        if any(ph in stem.lower() for ph in phrases):
            observed[section_for(b.qnum)] = observed.get(section_for(b.qnum), 0) + 1
    bad = [f'{sec}: expected {n} NAT, saw {observed.get(sec, 0)} instruction-carrying'
           for sec, n in exp.items() if observed.get(sec, 0) != n]
    (_ok if not bad else _fail)('A-NAT-INSTR',
        'observed numerical instruction counts match the blueprint per section.' if not bad
        else 'numerical instruction-count mismatch — ' + ' | '.join(bad))


def gate_stimorphan(blocks, src):
    linked = src['passage_linked'] | src['cloze_linked']
    # Merge section_rules stimulus cues (if declared) with the built-in English set (RA-9).
    extra_pats = src.get('stimulus_cue_patterns', [])
    cue_re = STIMULUS_CUES
    if extra_pats:
        combined = STIMULUS_CUES.pattern + '|' + '|'.join(r'\b' + p + r'\b' for p in extra_pats)
        cue_re = re.compile(combined, re.I)
    orphan, crossref = [], []
    bynum = {b.qnum: b for b in blocks}
    for b in blocks:
        stem = block_stem_text(b)
        if CROSSREF_RE.search(' '.join(para_text(p) for p in b.paras)):
            crossref.append(f'Q{b.qnum}')
        refs_stim = bool(cue_re.search(stem)) or (b.qnum in linked)
        if refs_stim:
            has_tbl = len(b.tables) > 0
            has_img = any(para_images(p) for p in b.paras)
            has_long = any(len(para_text(p).split()) >= 35 for p in b.paras)
            if not (has_tbl or has_img or has_long):
                orphan.append(f'Q{b.qnum}')
    (_ok if not orphan else _fail)('A-STIMORPHAN',
        'linked members carry their stimulus.' if not orphan else
        'orphaned stimulus (no embedded table/image/passage): ' + ' '.join(orphan[:12]))
    if crossref:
        _fail('A-STIMORPHAN-XREF', 'cross-question reference in stem: ' + ' '.join(crossref[:12]))
    else:
        _ok('A-STIMORPHAN-XREF', 'no "Q.x and Q.y" cross-references.')


# ── self-contained MATCH detector for the machine gate (v2.7.1) ────────────────
# The runnable audit.py (this block) is standalone and does NOT import the S6-1b spec
# classifier, so A-MATCH-TABLE carries its OWN detector. It MIRRORS the S6-1b classifier's
# MATCH rules EXACTLY (keyword rules + cross-domain label-pair option shape) — both live in
# THIS file (S6-1b + here); if one changes the other MUST match. Kept minimal: only the
# MATCH decision is needed here, not the full 8-class ladder.
_MT_PAIR_RE = re.compile(r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
                         r'\(?\s*([A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MT_SUB = (r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?\s*[-\u2010-\u2015:\u2192>]+\s*'
           r'\(?\s*(?:[A-Za-z]{1,4}|\d{1,2})\s*\)?')
_MT_OPT_RE = re.compile(r'^\s*' + _MT_SUB + r'(?:[,;\s]+' + _MT_SUB + r'){1,}\s*$')

def _mt_family(tokens):
    low = [x.lower() for x in tokens if x]
    if not low:
        return 'other'
    if all(re.fullmatch(r'\d{1,2}', x) for x in low):
        return 'digit'
    romanish = all(re.fullmatch(r'[ivxlcdm]+', x) for x in low)
    if romanish and any(len(x) > 1 for x in low):
        return 'roman'
    if all(re.fullmatch(r'[a-z]', x) for x in low):
        return 'roman' if set(low) <= {'i', 'v', 'x'} else 'alpha'
    if romanish:
        return 'roman'
    if all(re.fullmatch(r'[a-z]{1,4}', x) for x in low):
        return 'alpha'
    return 'other'

def _opts_match_pairs(opts):
    if not opts:
        return False
    hits = 0
    for o in opts:
        s = (o or '').strip()
        if not s or not _MT_OPT_RE.match(s):
            continue
        pairs = _MT_PAIR_RE.findall(s)
        if len(pairs) < 2:
            continue
        lf = _mt_family([p[0] for p in pairs])
        rf = _mt_family([p[1] for p in pairs])
        if lf == rf or 'other' in (lf, rf):
            continue
        hits += 1
    return hits >= max(2, (len(opts) + 1) // 2)

def _block_is_match(stem, opts):
    # Mirror the S6-1b ladder precedence: ASSERTION_REASON outranks MATCH, so an
    # assertion/reason stem is NOT a match even if its options look like pairs. (LINKED also
    # outranks MATCH; the gate skips linked members via src, below.)
    s = (stem or '').lower()
    if re.search(r'\bassertion\b', s) and re.search(r'\breason\b', s):
        return False
    if re.search(r'\bmatch\b', s) and re.search(r'\b(following|list|column|set)\b', s):
        return True
    if re.search(r'list[\s\-]*i\b|column[\s\-]*(i|a)\b', s):
        return True
    return _opts_match_pairs(opts)


def gate_match_table(blocks, src):
    """A-MATCH-TABLE (v2.7.1) — executable promotion of the S7-3 'MATRICES & MATCH-THE-COLUMN
    must be a REAL grid' checklist item. For every block re-derived as Axis-2 MATCH by the
    SHARED classifier (S6-1b — the SAME functions Step 5 and Step 7 use), the List columns
    MUST render as a real <w:tbl>. A match rendered as plain text lines (or space/tab pseudo-
    columns) is a format-fidelity defect: S6-6 still counts the MATCH format PRESENT while the
    skill is left un-rehearsed — a false readiness signal. Exam-agnostic: the MATCH signal is
    language-independent (keyword OR cross-domain option shape), never a hardcoded exam label."""
    if not blocks:
        return
    oc = src.get('options_count', 4)
    linked = src.get('passage_linked', set()) | src.get('cloze_linked', set())
    missing = []
    for b in blocks:
        if b.qnum in linked:          # LINKED outranks MATCH (S6-1b); A-STIMORPHAN covers it
            continue
        labs = _label_paras(b)
        opts = [x[2] for x in (labs[-oc:] if len(labs) >= oc else labs)]
        if _block_is_match(block_stem_text(b), opts):
            if not b.tables:
                missing.append(f'Q{b.qnum}')
    (_ok if not missing else _fail)('A-MATCH-TABLE',
        'every MATCH question renders its List columns as a real table.' if not missing else
        'MATCH question(s) rendered without a <w:tbl> grid (S7-3 defect — rebuild the List '
        'body as a real table, never text/space columns): ' + ' '.join(missing[:15]))


def gate_underline(blocks):
    missing, fake = [], []
    for b in blocks:
        whole = ' '.join(para_text(p) for p in b.paras)
        if FAKE_UNDERLINE.search(whole):
            fake.append(f'Q{b.qnum}')
        if UNDERLINE_REF.search(' '.join(para_text(p) for p in b.paras[:3])):
            # require a real w:u run somewhere in the block
            has_u = False
            for p in b.paras:
                for u in p._element.iter(W_('u')):
                    val = u.get(W_('val'))
                    if val not in ('none',):
                        has_u = True
                        break
                if has_u:
                    break
            if not has_u:
                missing.append(f'Q{b.qnum}')
    (_ok if not missing else _fail)('A-UNDERLINE',
        'underline-class Qs use real <w:u>.' if not missing else
        'no real underline run: ' + ' '.join(missing[:12]))
    if fake:
        _fail('A-UNDERLINE-FAKE', '"(underlined: X)" annotation present: ' + ' '.join(fake[:12]))
    else:
        _ok('A-UNDERLINE-FAKE', 'no faked-underline annotations.')


def gate_omml(doc, src, final):
    nfrac_bad, yearfrac = [], []
    n_omath = 0
    for kind, obj in iter_block_items(doc):
        if kind != 'p':
            continue
        for om in obj._element.iter(M_('oMath')):
            n_omath += 1
        for f in obj._element.iter(M_('f')):
            num = f.find(M_('num')); den = f.find(M_('den'))
            num_t = ''.join(t.text or '' for t in (num.iter(M_('t')) if num is not None else []))
            den_t = ''.join(t.text or '' for t in (den.iter(M_('t')) if den is not None else []))
            if not num_t.strip() or not den_t.strip():
                nfrac_bad.append('empty-frac')
            if re.fullmatch(r'\s*20\d\d\s*', num_t) and re.fullmatch(r'\s*\d{2}\s*', den_t):
                yearfrac.append(f'{num_t.strip()}/{den_t.strip()}')
    (_ok if not nfrac_bad else _fail)('A-OMML',
        f'{n_omath} oMath; all fractions well-formed.' if not nfrac_bad else
        f'{len(nfrac_bad)} fraction(s) with empty num/den.')
    if yearfrac:
        _warn('A-OMML-YEAR', f'year-range rendered as stacked fraction: {yearfrac[:6]}')
    if final and src['omml_required_present'] and n_omath == 0:
        _warn('A-OMML-FLOOR',
              'OMML_required subtopic(s) declared but ZERO <m:oMath> in paper — '
              'built-up math may be hiding as ASCII/raster; investigate (S7-5).')
    elif final and src['omml_required_present']:
        _ok('A-OMML-FLOOR', f'OMML floor satisfied ({n_omath} oMath).')


def gate_frac_ascii(blocks, src):
    caret, slash = [], []
    omml_ctx = src['omml_required_present']
    for b in blocks:
        stem = block_stem_text(b)
        if ASCII_CARET.search(stem):
            caret.append(f'Q{b.qnum}')
        if omml_ctx and SLASH_FRAC.search(stem):
            slash.append(f'Q{b.qnum}')
    (_ok if not caret else _fail)('A-FRAC',
        'no ASCII caret exponents.' if not caret else 'ASCII "^" exponent: ' + ' '.join(caret[:12]))
    if slash:
        _warn('A-FRAC-SLASH', 'slash fraction in math-context stem (view in Part B): '
              + ' '.join(slash[:12]))


def gate_images(blocks, src, media_map):
    """A-MATHRASTER (Tier 1) + A-FIGCOMP (structural, v2.4 image_role-aware)
    + A-FIGTEXT-PROSE (v2.4 — visual prose detector)."""
    math_raster, warn_view, composite, multi_per_line = [], [], [], []
    figtext_prose = []   # v2.4: figure-reference text in zero-image blocks
    fig = src['figural_qs']
    oc = src['options_count']
    # v2.4: read image_role per subtopic from section_rules
    sr_text = src.get('section_rules_text', '')
    concept_map = src.get('concept_map', {})
    # v2.4: figure-reference pattern for prose detector
    _fig_ref_re = re.compile(
        r'(?i)\b(in the given figure|in the following figure|'
        r'from the (given|following) (figure|diagram)|'
        r'figure \(X\)|the figure (shows|below|above)|'
        r'how many .{0,30}(triangles|squares|circles|lines|shapes|'
        r'angles|sides|regions|parts)\s+(are|in|does|can))')
    for b in blocks:
        block_imgs = []
        for p in b.paras:
            pim = para_images(p)
            if len(pim) >= 2:
                multi_per_line.append(f'Q{b.qnum}')
            for nm, emb in pim:
                tgt = media_map.get(emb, '')
                block_imgs.append((nm or '', tgt))
        # v2.4: A-FIGTEXT-PROSE — zero-image blocks referencing figures
        if not block_imgs:
            stem = ' '.join(para_text(p) for p in b.paras)
            if _fig_ref_re.search(stem):
                figtext_prose.append(f'Q{b.qnum}')
            continue
        stem = ' '.join(para_text(p) for p in b.paras[:3])
        math_ctx = src['omml_required_present']  # coarse; refined in Part B
        for nm, tgt in block_imgs:
            hay = f'{nm} {tgt}'
            if MATH_TOKEN_NAME.search(hay):
                math_raster.append(f'Q{b.qnum}')
            elif not CANON_IMG_NAME.match(nm or ''):
                warn_view.append(f'Q{b.qnum}')
        # A-FIGCOMP (v2.4 — image_role-aware):
        # Determine image_role for this question
        figural_cues = src.get('figural_cue_keywords',
                              ['which of the', 'odd one', 'mirror', 'water image',
                               'embedded', 'complete the', 'series', 'fold'])
        is_figural = b.qnum in fig or any(k in stem.lower() for k in figural_cues)
        if is_figural:
            # v2.4: determine image_role from section_rules via concept_map
            _q_role = 'stem_and_options'   # default
            qnum_str = str(b.qnum)
            if qnum_str in concept_map and sr_text:
                _sid = concept_map[qnum_str].get('subtopic_id', '')
                if _sid:
                    _rm = re.search(
                        r'subtopic_id:\s*' + re.escape(_sid) +
                        r'((?:(?!subtopic_id:).)*?)image_role:\s*(\S+)',
                        sr_text, re.DOTALL)
                    if _rm:
                        _q_role = _rm.group(2)
            # Also check NAT: if this Q's subtopic is in nat_subtopic_ids → stem_only
            _nat_ids = src.get('nat_subtopic_ids', set())
            if _nat_ids and qnum_str in concept_map:
                _q_sid = concept_map[qnum_str].get('subtopic_id', '')
                if _q_sid in _nat_ids:
                    _q_role = 'stem_only'
            # Branch by image_role
            if _q_role == 'stem_only':
                if len(block_imgs) < 1:
                    composite.append(f'Q{b.qnum}(stem_only:0img)')
                # 1 image IS correct for stem_only — do NOT flag as composite
            elif _q_role == 'options_only':
                n_opt = oc   # oc is int (exam-wide OPTIONS_COUNT from section_rules)
                if len(block_imgs) < n_opt:
                    composite.append(f'Q{b.qnum}(opts_only:{len(block_imgs)}<{n_opt})')
            else:   # stem_and_options (default)
                if len(block_imgs) == 1:
                    composite.append(f'Q{b.qnum}')
    (_ok if not math_raster else _fail)('A-MATHRASTER',
        'no math-token raster names.' if not math_raster else
        'image named like a math raster: ' + ' '.join(sorted(set(math_raster))[:12]))
    if warn_view:
        _warn('A-MATHRASTER-VIEW',
              f'{len(set(warn_view))} block(s) have non-canonically-named images — '
              'VIEW in Part B (§7) to confirm figure vs math raster: '
              + ' '.join(sorted(set(warn_view))[:12]))
    if multi_per_line:
        _fail('A-FIGCOMP-LINE', 'multiple images on one line (option-per-line broken): '
              + ' '.join(sorted(set(multi_per_line))[:12]))
    else:
        _ok('A-FIGCOMP-LINE', 'at most one image per line.')
    if composite:
        _warn('A-FIGCOMP',
              'figural block image-count mismatch (per image_role) — '
              'VIEW + fix in Part B: ' + ' '.join(sorted(set(composite))[:12]))
    else:
        _ok('A-FIGCOMP', 'figural blocks pass image_role-aware check (v2.4).')
    # v2.4: A-FIGTEXT-PROSE — figure-reference text in zero-image blocks
    if figtext_prose:
        _fail('A-FIGTEXT-PROSE',
              'Q-block references a figure but contains 0 images — '
              'render the figure or replace the subtopic (S7-NEW-B): '
              + ' '.join(sorted(set(figtext_prose))[:12]))
    else:
        _ok('A-FIGTEXT-PROSE', 'no figure-reference prose in zero-image blocks.')


def gate_optref(blocks, src):
    """A-OPTREF (machine half): if a stem references a terminal/escape option,
    that option must be present in the option set."""
    rt = src['rules_txt']
    # Read escape tokens from section_rules (RA-9) as PRIMARY; English defaults as FALLBACK.
    extra = re.findall(r'(?:none_of_above_permitted|escape_option_tokens)\s*[:=]\s*(.+)', rt, re.I)
    if extra:
        # section_rules declared exam-specific escape tokens — merge with defaults.
        tokens = [t.strip() for e in extra for t in e.split(',')]  + list(ESCAPE_TOKENS_DEFAULT)
    else:
        tokens = list(ESCAPE_TOKENS_DEFAULT)
    # Escape-reference phrases: if the WHOLE phrase appears in the stem, the stem is
    # referencing the escape option that phrase implies. Read from section_rules (RA-9);
    # English defaults as fallback.
    ref_phrases = src.get('escape_reference_phrases',
                          [r'if there is no error'])
    miss = []
    for b in blocks:
        stem = block_stem_text(b)
        opts = [o[2].lower() for o in option_paras(b)]
        for tok in tokens:
            # MODE 1: a select/mark/choose verb near the escape token in the stem.
            triggered = bool(re.search(r'(select|mark|choose).{0,40}' + tok, stem, re.I))
            # MODE 2: a direct escape-reference phrase in the stem that implies this token.
            if not triggered:
                for phrase in ref_phrases:
                    if re.search(phrase, stem, re.I) and re.search(tok, phrase, re.I):
                        triggered = True
                        break
            if triggered:
                present = any(re.search(tok, o, re.I) for o in opts)
                if not present:
                    miss.append(f'Q{b.qnum}')
                break
    (_ok if not miss else _fail)('A-OPTREF',
        'escape-option references are satisfied.' if not miss else
        'stem references an absent escape/terminal option: ' + ' '.join(sorted(set(miss))[:12]))


def gate_encoding_script(doc, src):
    full = '\n'.join(para_text(obj) for kind, obj in iter_block_items(doc) if kind == 'p')
    if '�' in full:
        _fail('A-ENCODING', 'U+FFFD replacement character present (encoding corruption).')
    else:
        _ok('A-ENCODING', 'no U+FFFD replacement characters.')
    if src['language'] == 'english':
        # Flag only RUNS (>=2) of foreign-SCRIPT letters (Devanagari, Cyrillic, CJK,
        # Arabic, ...). Accented Latin (café, résumé) and Greek math symbols
        # (alpha, beta, theta) are LEGITIMATE on an english exam and must not be
        # flagged. Isolated symbols never trip the gate; only a multi-letter
        # foreign-script word does (the copy-paste-corruption signature).
        def _foreign_letter(ch):
            if ord(ch) <= 0x7F or not ch.isalpha():
                return False
            try:
                nm = unicodedata.name(ch, '')
            except ValueError:
                nm = ''
            return not (nm.startswith('LATIN') or nm.startswith('GREEK'))
        run = 0; hits = []
        for ch in full:
            if _foreign_letter(ch):
                run += 1
                if run == 2:
                    hits.append(ch)
            else:
                run = 0
        if hits:
            _fail('A-SCRIPT', f'foreign-script word(s) on an english exam '
                              f'(copy-paste corruption?): {len(hits)} run(s).')
        else:
            _ok('A-SCRIPT', 'no foreign-script text (accented Latin / Greek symbols OK).')
    else:
        _ok('A-SCRIPT', f"language={src['language']}: non-Latin script permitted.")


def gate_dup(blocks, src):
    reg = src['registry']; tq = src['total_questions']
    stems_all = reg.get('stem_texts', [])
    if not stems_all or tq is None:
        _warn('A-DUP', 'registry stem_texts empty or total_questions unknown; '
                       'cross-mock dedup skipped.')
        return
    prior = stems_all[:max(0, len(stems_all) - tq)]   # self-exclude trailing mock N
    if not prior:
        _ok('A-DUP', 'no prior-mock stems in registry (first mock or registry holds only mock N); cross-mock dedup vacuous.')
        return
    norm = lambda s: re.sub(r'\s+', ' ', s).strip().lower()
    prior_norm = set(norm(s) for s in prior)
    prior_tokens = [set(norm(s).split()) for s in prior]
    exact, near = [], []
    for b in blocks:
        stem = norm(block_stem_text(b))
        if not stem:
            continue
        if stem in prior_norm:
            exact.append(f'Q{b.qnum}')
            continue
        toks = set(stem.split())
        if toks:
            for pt in prior_tokens:
                if pt:
                    j = len(toks & pt) / len(toks | pt)
                    if j >= 0.75:
                        near.append(f'Q{b.qnum}')
                        break
    (_ok if not exact and not near else _fail)('A-DUP',
        'no cross-mock stem duplication.' if not exact and not near else
        f'exact={sorted(set(exact))[:8]} near={sorted(set(near))[:8]} (vs prior mocks).')


def gate_header(doc, blocks, src):
    # v2.7: A-HEADER INVERTED. The paper is questions-only (Step 7 R8b / G-PREQ1): NO
    # title/info/scoring/cover paragraph may sit before Q.1. Any non-blank paragraph before
    # Q.1 is a DEFECT → strip it in Phase 1 (CP-HEADER-STRIP). CATEGORY-C values
    # (marks/time/negative/options/total) are metadata, never printed — nothing to
    # figure-check. DORMANT only if section_rules EXAM_STRUCTURE declares paper_header_block.
    title_items, _ = parse_blocks(doc)
    title = ' '.join(para_text(obj) for kind, obj in title_items if kind == 'p').strip()
    if src.get('paper_header_block'):
        _ok('A-HEADER', 'pre-Q.1 header permitted (EXAM_STRUCTURE paper_header_block); dormant.')
    elif not title:
        _ok('A-HEADER', 'questions-only: no non-blank paragraph before Q.1.')
    else:
        _fail('A-HEADER', f'non-Q paragraph(s) before Q.1: "{title[:60]}". Strip the '
                          'pre-Q.1 title/info/scoring/cover block (CP-HEADER-STRIP) — the '
                          'paper is questions-only (R8b/G-PREQ1); marks/time/negative/'
                          'options/total are metadata, never printed.')


def gate_zip(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        names = set(z.namelist())
        if 'word/document.xml' not in names:
            _fail('A-ZIP', 'word/document.xml missing.')
            return {}
        doc_xml = z.read('word/document.xml').decode('utf-8', 'replace')
        rels = (z.read('word/_rels/document.xml.rels').decode('utf-8')
                if 'word/_rels/document.xml.rels' in names else '')
        # parse each <Relationship .../> element, then pull Id + Target from
        # within it (attribute ORDER-INDEPENDENT — some generators emit Target
        # before Id, which an "Id...Target" regex would miss).
        rel_map = {}
        for tag in re.findall(r'<Relationship\b[^>]*/?>', rels):
            idm = re.search(r'\bId="([^"]+)"', tag)
            tgm = re.search(r'\bTarget="([^"]+)"', tag)
            if idm and tgm:
                rel_map[idm.group(1)] = tgm.group(1)
        ref_ids = set(re.findall(r'r:(?:embed|id|link)="([^"]+)"', doc_xml))
        bad = []
        media_map = {}
        for rid in ref_ids:
            tgt = rel_map.get(rid)
            if tgt is None:
                bad.append(rid); continue
            if tgt.startswith('http'):
                continue
            part = ('word/' + tgt).replace('word/../', '')
            if part not in names and ('word/' + tgt) not in names:
                bad.append(rid)
            media_map[rid] = tgt.split('/')[-1]
        (_ok if not bad else _fail)('A-ZIP',
            'all rIds resolve to parts.' if not bad else f'unresolved rIds: {bad[:8]}')
        return media_map


# ============================================================================
# S5-1A — COMPLETION GATE (v2.6) — Phase-3 mechanical Part-B/§7 enforcement
# ============================================================================
def _resolve_evidence(evidence_dir, stored):
    """Resolve a ledger-stored evidence path to an existing absolute path. Accepts an
    absolute path, a path relative to evidence_dir, a bare basename under evidence_dir,
    or a path with a leading 'evidence/' segment. Returns the resolved path or None."""
    if not stored:
        return None
    cands = [stored]
    if not os.path.isabs(stored):
        cands.append(os.path.join(evidence_dir, stored))
        cands.append(os.path.join(evidence_dir, os.path.basename(stored)))
        parts = stored.replace('\\', '/').split('/')
        if parts and parts[0] == 'evidence':
            cands.append(os.path.join(evidence_dir, *parts[1:]))
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def _file_ok(path, min_bytes):
    return bool(path) and os.path.exists(path) and os.path.getsize(path) >= min_bytes


def _block_has_omml(b):
    for p in b.paras:
        for _ in p._element.iter(M_('oMath')):
            return True
    return False


def _block_has_image(b):
    return any(para_images(p) for p in b.paras)


def completion_gate(audit_state_path, total_questions, blocks, doc):
    """S5-1A — validate the Phase-2 audit_state ledger (C1-C7) AND the on-disk evidence
    artefacts each stamp names. Appends C0..C7 results to RESULTS so the exit code
    reflects them, and prints the COMPLETION-GATE summary line. MANDATE-0 safe:
    Q-numbers + codes only, never content/URLs. Returns 0 (PASS) or 1 (FAIL)."""
    try:
        state = json.load(open(audit_state_path, encoding='utf-8'))
    except Exception as e:
        _fail('C0', f'audit_state unreadable/absent ({e}).')
        print('COMPLETION-GATE: FAIL (audit_state unreadable)')
        return 1
    ledger = (state.get('ledger') or {}).get('entries', {}) or {}
    entries = {int(k): v for k, v in ledger.items()}
    evidence_dir = state.get('evidence_dir', '') or ''
    K = state.get('K')
    if not K:
        plan = state.get('plan') or []
        K = len(plan) if plan else (max(state.get('batches_done', []) or [0]) or 0)
    batches_done = set(state.get('batches_done', []) or [])

    # C1 — every planned batch closed
    if K and set(range(1, K + 1)) <= batches_done:
        _ok('C1', f'all {K} batches closed.')
    else:
        _fail('C1', f'batches_done={sorted(batches_done)} does not cover 1..{K} '
                    f'(Phase 2 skipped/partial — MANDATE B).')
    # C2 — every question reviewed
    want = set(range(1, (total_questions or 0) + 1))
    got = set(entries.keys())
    if total_questions and got == want:
        _ok('C2', f'all {total_questions} questions have a ledger entry.')
    else:
        miss = sorted(want - got)[:15]; extra = sorted(got - want)[:15]
        _fail('C2', f'ledger != 1..{total_questions}: missing={miss} extra={extra}.')
    # C3 — every entry closed
    bad3 = [q for q, e in entries.items() if e.get('status') not in ('verified', 'regenerated')]
    (_ok if not bad3 else _fail)('C3',
        'all entries verified/regenerated.' if not bad3 else
        f'entries not closed (pending/absent): {sorted(bad3)[:15]}')
    # C4 — uniqueness / set ran
    bad4 = []
    for q, e in entries.items():
        if e.get('answer_cardinality') == 'multi':
            if not e.get('answer_set_verified'):
                bad4.append(q)
        else:
            if not e.get('answer_unique'):
                bad4.append(q)
    (_ok if not bad4 else _fail)('C4',
        'B-UNIQUE/A-MSQ-KEY ran for every Q.' if not bad4 else
        f'uniqueness/set not verified: {sorted(bad4)[:15]}')
    # C5 — factual entries sourced AND the saved evidence file exists/non-empty
    bad5 = []
    for q, e in entries.items():
        if e.get('is_factual'):
            fs = e.get('fact_sources') or []
            if not fs:
                bad5.append(q); continue
            for rec in fs:
                saved = rec.get('saved') if isinstance(rec, dict) else None
                if not _file_ok(_resolve_evidence(evidence_dir, saved), 1):
                    bad5.append(q); break
    (_ok if not bad5 else _fail)('C5',
        'every factual entry has a saved, sourced fact.' if not bad5 else
        f'factual entries unsourced / saved file missing: {sorted(set(bad5))[:15]}')
    # C6 — artefact stamps present AND their evidence files exist/non-trivial
    bad6 = []
    for q, e in entries.items():
        st = e.get('artefact_stamps') or {}
        ok = True
        for img in (st.get('images') or []):
            if not _file_ok(_resolve_evidence(evidence_dir, img.get('montage')), EVIDENCE_MIN_BYTES):
                ok = False
        for kind in ('tables', 'charts', 'omml'):
            for rec in (st.get(kind) or []):
                path = rec.get('trace') or rec.get('montage')
                if not _file_ok(_resolve_evidence(evidence_dir, path), 1):
                    ok = False
        if not ok:
            bad6.append(q)
    (_ok if not bad6 else _fail)('C6',
        'every artefact stamp is backed by an existing evidence file.' if not bad6 else
        f'artefact stamp evidence missing/trivial: {sorted(set(bad6))[:15]}')
    # C7 — coverage: every artefact PRESENT IN THE PAPER is represented in the ledger
    bad7 = []
    for b in blocks:
        e = entries.get(b.qnum, {})
        st = e.get('artefact_stamps') or {}
        if _block_has_image(b) and not st.get('images'):
            bad7.append(f'Q{b.qnum}:img'); continue
        if b.tables and not (st.get('tables') or st.get('charts')):
            bad7.append(f'Q{b.qnum}:tbl'); continue
        if _block_has_omml(b) and not st.get('omml'):
            bad7.append(f'Q{b.qnum}:omml'); continue
    (_ok if not bad7 else _fail)('C7',
        'every paper artefact is covered by a ledger stamp.' if not bad7 else
        f'paper artefact not audited (no ledger stamp): {sorted(set(bad7))[:15]}')

    cfails = [c for lvl, c, _ in RESULTS if lvl == 'FAIL' and (c == 'C0' or c.startswith('C'))
              and c[1:].isdigit()]
    if not cfails:
        F = sum(1 for e in entries.values() if e.get('is_factual'))
        V = sum(len((e.get('artefact_stamps') or {}).get(k, []))
                for e in entries.values() for k in ('images', 'tables', 'charts', 'omml'))
        print(f'COMPLETION-GATE: PASS (Q reviewed={len(entries)}/{total_questions}, '
              f'facts sourced={F}, artefacts stamped={V}, evidence files present={V + F})')
        return 0
    print(f'COMPLETION-GATE: FAIL ({len(cfails)} assertion(s): {sorted(set(cfails))})')
    return 1


# ============================================================================
# RUNNER
# ============================================================================
def run_audit(args):
    _reset()
    src = load_sources(args)
    src['_mockN'] = args.mockN
    media_map = gate_zip(args.docx)
    doc = Document(args.docx)
    _title, blocks = parse_blocks(doc)
    gate_structure(blocks, src)
    gate_seccount(blocks, src)
    gate_options(blocks, src)
    gate_qnfirst(blocks)
    gate_msq_instr(blocks, src)            # v1.2 — MULTI only; dormant otherwise
    gate_nat(blocks, src)                  # v1.4 — NUMERICAL only; dormant otherwise
    gate_blanksep(doc, blocks)
    gate_font(doc, src)
    gate_sechdr(blocks, doc, src)
    gate_anskey(doc)
    gate_stimorphan(blocks, src)
    gate_match_table(blocks, src)          # v2.7.1 — MATCH must render a real table
    gate_underline(blocks)
    gate_omml(doc, src, args.final)
    gate_frac_ascii(blocks, src)
    gate_images(blocks, src, media_map)
    gate_optref(blocks, src)
    gate_encoding_script(doc, src)
    gate_dup(blocks, src)
    gate_header(doc, blocks, src)
    rc = print_results()
    # v2.6 — S5-1A COMPLETION GATE: Phase-3 mechanical Part-B/§7 enforcement.
    if getattr(args, 'audit_state', None):
        cg = completion_gate(args.audit_state, src.get('total_questions'), blocks, doc)
        return 0 if (rc == 0 and cg == 0) else 1
    return rc


def print_results():
    n_fail = sum(1 for lvl, _, _ in RESULTS if lvl == 'FAIL')
    n_warn = sum(1 for lvl, _, _ in RESULTS if lvl == 'WARN')
    n_ok   = sum(1 for lvl, _, _ in RESULTS if lvl == 'OK')
    print('=' * 70)
    print(f'PART-A MACHINE AUDIT  |  OK={n_ok}  WARN={n_warn}  FAIL={n_fail}')
    print('=' * 70)
    for lvl, code, msg in RESULTS:
        mark = {'OK': '  ok ', 'WARN': ' WARN', 'FAIL': ' FAIL'}[lvl]
        print(f'[{mark}] {code:20s} {msg}')
    print('-' * 70)
    if n_fail == 0:
        print(f'RESULT: PASS (0 FAIL, {n_warn} WARN for reviewer adjudication)')
    else:
        print(f'RESULT: FAIL ({n_fail} gate(s) failed)')
    return 0 if n_fail == 0 else 1


# ============================================================================
# SELF-TEST  (builds tiny docx fixtures; asserts each gate catches + passes)
# ============================================================================
def _mini_doc(tmp, build):
    from docx import Document as D
    d = D()
    build(d)
    p = os.path.join(tmp, 'x.docx')
    d.save(p)
    return p

def _src_stub(tq=2, oc=4, lang='english', sections=None, omml=False):
    return {'total_questions': tq, 'sections': sections or
            [{'name': 'S1', 'q_range': [1, tq], 'total_qs': tq}],
            'options_count': oc, 'opt_label_fmt': '1/2/3/4', 'font_family': 'Calibri',
            'language': lang, 'omml_required_present': omml, 'rules_txt': '',
            'registry': {}, 'manifest': {}, 'blueprint': {},
            'passage_linked': set(), 'cloze_linked': set(), 'figural_qs': set(),
            '_mockN': 1}

def _add_q(d, n, opts=('Alpha', 'Beta', 'Gamma', 'Delta'), qn_first=True, stem='Solve.'):
    if qn_first:
        d.add_paragraph(f'Q.{n}  {stem}')
    else:
        d.add_paragraph(stem)               # stimulus-first (defect)
        d.add_paragraph(f'Q.{n}  {stem}')
    for i, o in enumerate(opts, 1):
        d.add_paragraph(f'{i}.  {o}')
    d.add_paragraph('')

def self_test():
    passed = 0; total = 0; fails = []
    tmp = tempfile.mkdtemp()
    def check(name, cond):
        nonlocal passed, total
        total += 1
        if cond: passed += 1
        else: fails.append(name)

    # 1. clean paper passes structure/options/qnfirst
    def b_clean(d):
        _add_q(d, 1); _add_q(d, 2)
    p = _mini_doc(tmp, b_clean)
    _reset(); doc = Document(p); _t, blocks = parse_blocks(doc)
    src = _src_stub()
    gate_structure(blocks, src); gate_options(blocks, src); gate_qnfirst(blocks)
    check('clean-no-fail', not any(l == 'FAIL' for l, _, _ in RESULTS))

    # 2. A-COUNT catches wrong count
    _reset(); gate_structure(blocks, _src_stub(tq=5))
    check('A-COUNT-catch', any(c == 'A-COUNT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 3. A-OPTN catches 3 options
    def b_3opt(d): _add_q(d, 1, opts=('A', 'B', 'C'))
    p = _mini_doc(tmp, b_3opt); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    check('A-OPTN-catch', any(c == 'A-OPTN' and l == 'FAIL' for l, c, _ in RESULTS))

    # 4. A-OPTUNIQUE catches duplicate options
    def b_dupopt(d): _add_q(d, 1, opts=('Same', 'Same', 'B', 'C'))
    p = _mini_doc(tmp, b_dupopt); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    check('A-OPTUNIQUE-catch', any(c == 'A-OPTUNIQUE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 5. A-QNFIRST catches stimulus orphaned before the next Q.N
    def b_notfirst(d):
        _add_q(d, 1)                                   # Q.1 + options + blank
        d.add_paragraph(' '.join(['word'] * 60))       # passage orphaned before Q.2
        _add_q(d, 2)
    p = _mini_doc(tmp, b_notfirst); _reset()
    _t, bl = parse_blocks(Document(p)); gate_qnfirst(bl)
    check('A-QNFIRST-catch', any(c == 'A-QNFIRST' and l == 'FAIL' for l, c, _ in RESULTS))

    # 5b. A-MATCH-TABLE catches a MATCH question rendered WITHOUT a real table (v2.7.1)
    _MPAIRS = ('(A)-(I), (B)-(III), (C)-(IV), (D)-(II)', '(A)-(II), (B)-(IV), (C)-(III), (D)-(I)',
               '(A)-(IV), (B)-(III), (C)-(II), (D)-(I)', '(A)-(III), (B)-(I), (C)-(IV), (D)-(II)')
    def b_match_notable(d):
        d.add_paragraph('Q.1  Match List-I with List-II.')
        for i, o in enumerate(_MPAIRS, 1):
            d.add_paragraph(f'{i}.  {o}')
        d.add_paragraph('')
    p = _mini_doc(tmp, b_match_notable); _reset()
    _t, bl = parse_blocks(Document(p)); gate_match_table(bl, _src_stub(tq=1))
    check('A-MATCH-TABLE-catch', any(c == 'A-MATCH-TABLE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 5c. A-MATCH-TABLE passes (dormant) when the MATCH body IS a real table
    def b_match_table(d):
        d.add_paragraph('Q.1  Match List-I with List-II.')
        tb = d.add_table(rows=2, cols=2)
        tb.cell(0, 0).text = '(A) Collagen'; tb.cell(0, 1).text = '(I) triple helix'
        tb.cell(1, 0).text = '(B) Keratin';  tb.cell(1, 1).text = '(II) coiled coil'
        for i, o in enumerate(_MPAIRS, 1):
            d.add_paragraph(f'{i}.  {o}')
        d.add_paragraph('')
    p = _mini_doc(tmp, b_match_table); _reset()
    _t, bl = parse_blocks(Document(p)); gate_match_table(bl, _src_stub(tq=1))
    check('A-MATCH-TABLE-pass', not any(c == 'A-MATCH-TABLE' and l == 'FAIL' for l, c, _ in RESULTS))

    # 6. A-FONT catches Arial run
    def b_arial(d):
        para = d.add_paragraph()
        run = para.add_run('Q.1  Stem'); run.font.name = 'Arial'
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_arial); _reset()
    gate_font(Document(p), _src_stub(tq=1))
    check('A-FONT-catch', any(c == 'A-FONT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 7. A-ANSKEY catches an answer-key line
    def b_key(d):
        _add_q(d, 1); d.add_paragraph('Answer Key: Q.1 -> 2')
    p = _mini_doc(tmp, b_key); _reset()
    gate_anskey(Document(p))
    check('A-ANSKEY-catch', any(c == 'A-ANSKEY' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8. A-SECHDR catches a body section header INSIDE a question block (KEYWORD form)
    def b_hdr2(d):
        d.add_paragraph('Q.1  Stem'); d.add_paragraph('SECTION A: Reasoning')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p2 = _mini_doc(tmp, b_hdr2); _reset()
    _t, bl2 = parse_blocks(Document(p2))
    gate_sechdr(bl2, Document(p2), {'sections': [{'name': 'Reasoning'}]})
    check('A-SECHDR-catch', any(c == 'A-SECHDR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8b. A-HEADER (inverted, v2.7): a title/info block BEFORE Q.1 → A-HEADER FAIL (strip).
    def b_hdr_preq1(d):
        d.add_paragraph('SSC CGL Tier 1 — Mock Test 1')
        d.add_paragraph('Total Questions: 100    |    Maximum Marks: 200    |    Time: 60 Minutes')
        _add_q(d, 1)
    p = _mini_doc(tmp, b_hdr_preq1); _reset()
    dh = Document(p); _t, blh = parse_blocks(dh)
    gate_header(dh, blh, _src_stub(tq=1))
    check('A-HEADER-catch', any(c == 'A-HEADER' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8c. A-HEADER dormant (v2.7): the SAME pre-Q.1 block, but section_rules EXAM_STRUCTURE
    #     declares paper_header_block → the opt-in permits it → NO A-HEADER failure.
    _reset()
    sd = _src_stub(tq=1); sd['paper_header_block'] = True
    gate_header(dh, blh, sd)
    check('A-HEADER-dormant', not any(c == 'A-HEADER' and l == 'FAIL' for l, c, _ in RESULTS))

    # 8b. v1.5 — A-SECHDR catches a stray heading that IS a declared SECTION NAME (the case
    #     the keyword pattern missed — found by the mutation harness). "Quantitative Aptitude"
    #     as a body paragraph, matched against src['sections'], must FAIL.
    def b_hdr3(d):
        d.add_paragraph('Quantitative Aptitude')          # section-name header, no keyword
        d.add_paragraph('Q.1  Stem')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p3 = _mini_doc(tmp, b_hdr3); _reset()
    _t, bl3 = parse_blocks(Document(p3))
    gate_sechdr(bl3, Document(p3), {'sections': [{'name': 'Quantitative Aptitude'}]})
    check('A-SECHDR-name-catch', any(c == 'A-SECHDR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 9. A-UNDERLINE-FAKE catches "(underlined: X)"
    def b_fakeu(d):
        d.add_paragraph('Q.1  Find the synonym of the underlined word. (underlined: brisk)')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_fakeu); _reset()
    _t, bl = parse_blocks(Document(p)); gate_underline(bl)
    check('A-UNDERLINE-catch', any(c.startswith('A-UNDERLINE') and l == 'FAIL'
                                   for l, c, _ in RESULTS))

    # 10. A-FRAC catches ASCII caret exponent
    def b_caret(d):
        d.add_paragraph('Q.1  If x^2 + 1 = 5 then x?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_caret); _reset()
    _t, bl = parse_blocks(Document(p)); gate_frac_ascii(bl, _src_stub(tq=1, omml=True))
    check('A-FRAC-catch', any(c == 'A-FRAC' and l == 'FAIL' for l, c, _ in RESULTS))

    # 11. A-STIMORPHAN catches a passage-reference with no embedded stimulus
    def b_orphan(d):
        d.add_paragraph('Q.1  According to the passage, what is the tone?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_orphan); _reset()
    _t, bl = parse_blocks(Document(p)); gate_stimorphan(bl, _src_stub(tq=1))
    check('A-STIMORPHAN-catch', any(c == 'A-STIMORPHAN' and l == 'FAIL' for l, c, _ in RESULTS))

    # 12. A-STIMORPHAN passes when a long passage is embedded
    def b_embed(d):
        long = ' '.join(['word'] * 60)
        d.add_paragraph('Q.1  Read the following passage and answer the question. ' + long)
        d.add_paragraph('What is the tone?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_embed); _reset()
    _t, bl = parse_blocks(Document(p)); gate_stimorphan(bl, _src_stub(tq=1))
    check('A-STIMORPHAN-pass', not any(c == 'A-STIMORPHAN' and l == 'FAIL'
                                       for l, c, _ in RESULTS))

    # 13. A-ENCODING catches U+FFFD
    def b_fffd(d):
        d.add_paragraph('Q.1  Bad char � here')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_fffd); _reset()
    gate_encoding_script(Document(p), _src_stub(tq=1))
    check('A-ENCODING-catch', any(c == 'A-ENCODING' and l == 'FAIL' for l, c, _ in RESULTS))

    # 14. A-SCRIPT passes Devanagari when language=hindi, fails when english
    def b_dev(d):
        d.add_paragraph('Q.1  प्रश्न यहाँ है')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_dev)
    _reset(); gate_encoding_script(Document(p), _src_stub(tq=1, lang='english'))
    eng_fail = any(c == 'A-SCRIPT' and l == 'FAIL' for l, c, _ in RESULTS)
    _reset(); gate_encoding_script(Document(p), _src_stub(tq=1, lang='hindi'))
    hin_ok = not any(c == 'A-SCRIPT' and l == 'FAIL' for l, c, _ in RESULTS)
    check('A-SCRIPT-lang-aware', eng_fail and hin_ok)

    # 15. A-DUP catches a stem repeated from a prior mock
    def b_dupstem(d):
        d.add_paragraph('Q.1  The capital of France is which city among these')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_dupstem); _reset()
    src = _src_stub(tq=1)
    src['registry'] = {'stem_texts': ['the capital of france is which city among these',
                                      'unrelated prior stem about rivers and lakes here']}
    # prior = all but trailing tq(=1) → first entry is prior
    _t, bl = parse_blocks(Document(p)); gate_dup(bl, src)
    check('A-DUP-catch', any(c == 'A-DUP' and l == 'FAIL' for l, c, _ in RESULTS))

    # 16. A-MATHRASTER name-contract: math-token names flagged, generic names not
    check('A-MATHRASTER-regex', bool(MATH_TOKEN_NAME.search('q55_e1.png'))
          and not MATH_TOKEN_NAME.search('Picture 3'))

    # 17. A-OPTREF catches missing escape option
    def b_optref(d):
        d.add_paragraph('Q.1  Identify the error; if there is no error select the last option.')
        for i, o in enumerate(('Part A', 'Part B', 'Part C', 'Part D'), 1):
            d.add_paragraph(f'{i}.  {o}')   # no "No error" option
    p = _mini_doc(tmp, b_optref); _reset()
    _t, bl = parse_blocks(Document(p)); gate_optref(bl, _src_stub(tq=1))
    check('A-OPTREF-catch', any(c == 'A-OPTREF' and l == 'FAIL' for l, c, _ in RESULTS))

    # 18. block parser merges OMML text (pure-math stem not seen empty)
    check('omml-merge-helper', callable(para_text))

    # 19. A-SCRIPT: accented Latin (cafe/resume) NOT flagged on an english exam
    def b_acc(d):
        d.add_paragraph('Q.1  The café served a résumé with naïve charm.')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_acc); _reset()
    gate_encoding_script(Document(p), _src_stub(tq=1, lang='english'))
    check('A-SCRIPT-accented-latin-ok', not any(c == 'A-SCRIPT' and l == 'FAIL'
                                                for l, c, _ in RESULTS))

    # 20. A-SCRIPT: Greek math symbols NOT flagged on an english exam
    def b_grk(d):
        d.add_paragraph('Q.1  If α + β = θ then θ = ?')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_grk); _reset()
    gate_encoding_script(Document(p), _src_stub(tq=1, lang='english'))
    check('A-SCRIPT-greek-ok', not any(c == 'A-SCRIPT' and l == 'FAIL'
                                       for l, c, _ in RESULTS))

    # 21. A-ZIP: rels parsing is attribute-ORDER-INDEPENDENT (Target before Id)
    rels_tf = '<Relationship Target="media/image1.png" Type="x" Id="rId9"/>'
    rel_map = {}
    for tag in re.findall(r'<Relationship\b[^>]*/?>', rels_tf):
        idm = re.search(r'\bId="([^"]+)"', tag); tgm = re.search(r'\bTarget="([^"]+)"', tag)
        if idm and tgm:
            rel_map[idm.group(1)] = tgm.group(1)
    check('A-ZIP-attr-order', rel_map.get('rId9') == 'media/image1.png')

    # 22. A-OPTN: an enumerated passage point before the options does NOT inflate
    #     the option count (trailing-oc extraction)
    def b_enum(d):
        d.add_paragraph('Q.1  Read the data.')
        d.add_paragraph('1.  earlier enumerated passage point that is not an option')
        d.add_paragraph('Which is correct?')
        for i, o in enumerate(('Opt1', 'Opt2', 'Opt3', 'Opt4'), 1):
            d.add_paragraph(f'{i}.  {o}')
    p = _mini_doc(tmp, b_enum); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    check('A-OPTN-enum-no-false', not any(c == 'A-OPTN' and l == 'FAIL'
                                          for l, c, _ in RESULTS))

    # 23. A-OPTN passes figural bare-label image options; roman + alpha label sets
    def b_fig(d):
        d.add_paragraph('Q.1  Select the figure.')
        for i in range(1, 5):
            d.add_paragraph(f'{i}.')          # bare label (image would follow)
    p = _mini_doc(tmp, b_fig); _reset()
    _t, bl = parse_blocks(Document(p)); gate_options(bl, _src_stub(tq=1))
    fig_ok = not any(c == 'A-OPTN' and l == 'FAIL' for l, c, _ in RESULTS)
    def b_rom(d):
        d.add_paragraph('Q.1  Pick.')
        for lab in ('i', 'ii', 'iii', 'iv'):
            d.add_paragraph(f'{lab}.  t{lab}')
    p = _mini_doc(tmp, b_rom); _reset()
    _t, bl = parse_blocks(Document(p))
    s2 = _src_stub(tq=1); s2['opt_label_fmt'] = 'i/ii/iii/iv'
    gate_options(bl, s2)
    rom_ok = not any(l == 'FAIL' for l, c, _ in RESULTS)
    check('A-OPTN-figural+roman', fig_ok and rom_ok)

    # 24. A-MSQ-INSTR (machine): a section expecting 1 multi Q but 0 instruction-carrying
    #     stems → FAIL (a multi Q is missing its select-instruction).
    def b_msq_missing(d):
        _add_q(d, 1, stem='Which of the following are prime?')   # multi expected, NO instruction
    p = _mini_doc(tmp, b_msq_missing); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_multi_by_section'] = {'S1': 1}
    s['msq_instruction_phrases'] = ['one or more', 'may be correct']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_msq_instr(bl, s)
    check('A-MSQ-INSTR-catch', any(c == 'A-MSQ-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 25. A-MSQ-INSTR passes when the multi Q carries its instruction in the Q.N line.
    def b_msq_ok(d):
        _add_q(d, 1, stem='Which of the following are prime? (One or more options may be correct)')
    p = _mini_doc(tmp, b_msq_ok); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_multi_by_section'] = {'S1': 1}
    s['msq_instruction_phrases'] = ['one or more', 'may be correct']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_msq_instr(bl, s)
    check('A-MSQ-INSTR-pass', not any(c == 'A-MSQ-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 26. A-MSQ-INSTR is DORMANT when the blueprint declares no multi subtopics.
    def b_single(d): _add_q(d, 1)
    p = _mini_doc(tmp, b_single); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['expected_multi_by_section'] = {}
    gate_msq_instr(bl, s)
    check('A-MSQ-INSTR-dormant', not any(c == 'A-MSQ-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 27. A-ANSKEY catches a SET-valued key leak ("Q.1 -> 1,2,4"), not just single-digit.
    def b_setkey(d):
        _add_q(d, 1); d.add_paragraph('Answer Key: Q.1 -> 1,2,4')
    p = _mini_doc(tmp, b_setkey); _reset()
    gate_anskey(Document(p))
    check('A-ANSKEY-setleak-catch', any(c == 'A-ANSKEY' and l == 'FAIL' for l, c, _ in RESULTS))

    # 28. empty document does not crash any gate
    def b_empty(d):
        pass
    p = _mini_doc(tmp, b_empty); _reset()
    try:
        mm = gate_zip(p); doc = Document(p); _t, bl = parse_blocks(doc)
        st = _src_stub(tq=0)
        for fn in (lambda: gate_structure(bl, st), lambda: gate_options(bl, st),
                   lambda: gate_qnfirst(bl), lambda: gate_blanksep(doc, bl),
                   lambda: gate_font(doc, st), lambda: gate_sechdr(bl, doc, st),
                   lambda: gate_anskey(doc), lambda: gate_stimorphan(bl, st),
                   lambda: gate_underline(bl), lambda: gate_omml(doc, st, True),
                   lambda: gate_frac_ascii(bl, st), lambda: gate_images(bl, st, mm),
                   lambda: gate_optref(bl, st), lambda: gate_encoding_script(doc, st),
                   lambda: gate_dup(bl, st), lambda: gate_header(doc, bl, st),
                   lambda: gate_nat(bl, st)):
            fn()
        empty_ok = True
    except Exception:
        empty_ok = False
    check('empty-doc-no-crash', empty_ok)

    # 29. A-NAT-NOOPT (machine): a Q the registry marks NAT (options_by_q=0) that RENDERS
    #     options → FAIL (a numerical question must carry none).
    def b_nat_hasopts(d):
        _add_q(d, 1, stem='Find the value. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_nat_hasopts); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['nat_present'] = True; s['options_by_q'] = {'1': 0}
    gate_nat(bl, s)
    check('A-NAT-NOOPT-catch', any(c == 'A-NAT-NOOPT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 30. A-NAT-NOOPT passes when the NAT Q renders zero options.
    def b_nat_noopts(d):
        _add_q(d, 1, opts=(), stem='Find the value. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_nat_noopts); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['nat_present'] = True; s['options_by_q'] = {'1': 0}
    gate_nat(bl, s)
    check('A-NAT-NOOPT-pass', not any(c == 'A-NAT-NOOPT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 31. A-NAT-NOOPT is DORMANT when the blueprint declares no numerical subtopics.
    def b_nat_dormant(d): _add_q(d, 1)
    p = _mini_doc(tmp, b_nat_dormant); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)   # nat_present default false; options_by_q empty
    gate_nat(bl, s)
    check('A-NAT-NOOPT-dormant', not any(c == 'A-NAT-NOOPT' and l == 'FAIL' for l, c, _ in RESULTS))

    # 32. A-NAT-INSTR (machine): a section expecting 1 NAT Q but 0 instruction-carrying
    #     stems → FAIL (a numerical Q is missing its numerical-entry instruction).
    def b_nat_missing(d):
        _add_q(d, 1, opts=(), stem='Find the value of x.')
    p = _mini_doc(tmp, b_nat_missing); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_nat_by_section'] = {'S1': 1}
    s['nat_instruction_phrases'] = ['numerical value', 'enter your answer']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_nat(bl, s)
    check('A-NAT-INSTR-catch', any(c == 'A-NAT-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 33. A-NAT-INSTR passes when the NAT Q carries its instruction in the Q.N line.
    def b_nat_ok(d):
        _add_q(d, 1, opts=(), stem='Find the value of x. Enter your answer as a numerical value.')
    p = _mini_doc(tmp, b_nat_ok); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1)
    s['expected_nat_by_section'] = {'S1': 1}
    s['nat_instruction_phrases'] = ['numerical value', 'enter your answer']
    s['sections'] = [{'name': 'S1', 'q_range': [1, 1], 'total_qs': 1}]
    gate_nat(bl, s)
    check('A-NAT-INSTR-pass', not any(c == 'A-NAT-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # 34. A-NAT-INSTR is DORMANT when the blueprint declares no numerical subtopics.
    def b_nat_dormant2(d): _add_q(d, 1)
    p = _mini_doc(tmp, b_nat_dormant2); _reset()
    _t, bl = parse_blocks(Document(p))
    s = _src_stub(tq=1); s['expected_nat_by_section'] = {}
    gate_nat(bl, s)
    check('A-NAT-INSTR-dormant', not any(c == 'A-NAT-INSTR' and l == 'FAIL' for l, c, _ in RESULTS))

    # ── v2.6 COMPLETION-GATE fixtures (S5-1A C1–C7) ────────────────────────────
    # Shared: a clean 1-Q docx (no artefacts) and an evidence dir.
    def _cg_doc(build):
        pp = _mini_doc(tmp, build)
        dd = Document(pp); _tt, bb = parse_blocks(dd)
        return dd, bb
    def _write_state(name, state):
        sp = os.path.join(tmp, name)
        json.dump(state, open(sp, 'w', encoding='utf-8'))
        return sp
    _evd = os.path.join(tmp, 'evdir'); os.makedirs(_evd, exist_ok=True)

    # 35. COMPLETION-GATE PASS on a complete, evidence-clean single-Q ledger.
    dcg, bcg = _cg_doc(lambda d: _add_q(d, 1))
    _reset()
    st35 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False,
                        'fact_sources': [], 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st35.json', st35), 1, bcg, dcg)
    check('CG-pass', rc == 0 and not any(l == 'FAIL' for l, c, _ in RESULTS))

    # 36. SKIPPED-PHASE-2: empty ledger + no batches → C1 + C2 FAIL.
    _reset()
    st36 = {'K': 1, 'batches_done': [], 'evidence_dir': _evd, 'ledger': {'entries': {}}}
    rc = completion_gate(_write_state('st36.json', st36), 1, bcg, dcg)
    check('CG-skipped-phase2', rc == 1
          and any(c == 'C1' and l == 'FAIL' for l, c, _ in RESULTS)
          and any(c == 'C2' and l == 'FAIL' for l, c, _ in RESULTS))

    # 37. PARTIAL-REVIEW: tq=2 but only Q1 in the ledger → C2 FAIL.
    _reset()
    st37 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False, 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st37.json', st37), 2, bcg, dcg)
    check('CG-partial-review', rc == 1 and any(c == 'C2' and l == 'FAIL' for l, c, _ in RESULTS))

    # 38. UNSOURCED-FACT: a factual entry with no fact_sources → C5 FAIL.
    _reset()
    st38 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': True,
                        'fact_sources': [], 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st38.json', st38), 1, bcg, dcg)
    check('CG-unsourced-fact', rc == 1 and any(c == 'C5' and l == 'FAIL' for l, c, _ in RESULTS))

    # 39. UNVIEWED artefact (paper has a table, ledger has no stamp) → C7 FAIL.
    def b_tbl(d):
        d.add_paragraph('Q.1  Study the table.')
        for i, o in enumerate(('A', 'B', 'C', 'D'), 1):
            d.add_paragraph(f'{i}.  {o}')
        tt = d.add_table(rows=2, cols=2)
        tt.cell(0, 0).text = 'h1'; tt.cell(0, 1).text = 'h2'
        tt.cell(1, 0).text = '1'; tt.cell(1, 1).text = '2'
    dtbl, btbl = _cg_doc(b_tbl)
    _reset()
    st39 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False, 'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st39.json', st39), 1, btbl, dtbl)
    check('CG-unviewed-artefact', rc == 1 and any(c == 'C7' and l == 'FAIL' for l, c, _ in RESULTS))

    # 40. MISSING evidence FILE (stamp present, trace file absent) → C6 FAIL.
    _reset()
    st40 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False,
                        'artefact_stamps': {'tables': [{'idx': 0, 'stamp': 'recomputed',
                                            'trace': os.path.join(_evd, 'does_not_exist.txt')}]}}}}}
    rc = completion_gate(_write_state('st40.json', st40), 1, btbl, dtbl)
    check('CG-missing-evidence-file', rc == 1 and any(c == 'C6' and l == 'FAIL' for l, c, _ in RESULTS))

    # 41. FACT saved-file MISSING (source named but file absent) → C5 FAIL.
    _reset()
    st41 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': True,
                        'fact_sources': [{'url': 'x', 'date': 'y',
                                          'saved': os.path.join(_evd, 'nf.json')}],
                        'artefact_stamps': {}}}}}
    rc = completion_gate(_write_state('st41.json', st41), 1, bcg, dcg)
    check('CG-factfile-missing', rc == 1 and any(c == 'C5' and l == 'FAIL' for l, c, _ in RESULTS))

    # 42. EVIDENCE-BACKED artefact stamp (trace file exists) → PASS.
    _trace = os.path.join(_evd, 'q1_table.txt')
    open(_trace, 'w', encoding='utf-8').write('grid a,b / 1,2 ; total row recomputed = 3 OK')
    _reset()
    st42 = {'K': 1, 'batches_done': [1], 'evidence_dir': _evd,
            'ledger': {'entries': {'1': {'status': 'verified', 'answer_cardinality': 'single',
                        'answer_unique': True, 'is_factual': False,
                        'artefact_stamps': {'tables': [{'idx': 0, 'stamp': 'recomputed',
                                            'trace': _trace}]}}}}}
    rc = completion_gate(_write_state('st42.json', st42), 1, btbl, dtbl)
    check('CG-evidence-backed-pass', rc == 0 and not any(l == 'FAIL' for l, c, _ in RESULTS))

    print(f'SELF-TEST: {passed}/{total} PASS' if passed == total
          else f'SELF-TEST: {passed}/{total} PASS  (FAILURES: {fails})')
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser(description='Universal exam-agnostic Part-A mock auditor')
    ap.add_argument('docx', nargs='?', help='the Mock[N]_Create.docx to audit')
    ap.add_argument('--blueprint'); ap.add_argument('--rules')
    ap.add_argument('--manifest');  ap.add_argument('--registry')
    ap.add_argument('--mockN', type=int)
    ap.add_argument('--final', action='store_true')
    ap.add_argument('--audit-state', dest='audit_state',
                    help='Phase-3 COMPLETION GATE (S5-1A): validate the audit_state ledger '
                         '+ evidence artefacts (C1-C7). Use with --final.')
    ap.add_argument('--key', dest='key',
                    help='optional answer_key.json (concept_map) — normally NOT delivered (S0-1).')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())
    if not args.docx:
        ap.error('docx path required (or use --self-test)')
    sys.exit(run_audit(args))


if __name__ == '__main__':
    main()
```

# ════════════════════════════════════════════════════════════════════════
# END OF Framework_MockTestCreateAudit v2.7.6
# ════════════════════════════════════════════════════════════════════════
