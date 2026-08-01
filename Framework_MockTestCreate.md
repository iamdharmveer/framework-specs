# Framework_MockTestCreate v5.34.1
# v5.34.1 — 2026-08-01 — self-test count refresh only (73/73 -> 78/78, B3).
# v5.34 — 2026-08-01 — FIGURESPEC TRANSPORT TO STEP 8
#   (GAP-2026-08-01-FIGSPEC-TRANSPORT D2). One additive field at S13-4; zero
#   change to any render, any question, any gate, any deliverable.
#
#   WHAT WAS WRONG. v5.33 renders every figure through figural_core, and
#   render_figure() MUTATES the FigureSpec with what actually happened —
#   png_px, png_dpi, placed_in, placement_scale, font_pt_native — after reading
#   the saved artefact back. write_spec_sidecar() then drops that record beside
#   the PNG as q{N}_*.figspec.json. Step 8's twelve v2.11 figure-conformance
#   gates are arithmetic over the PNG AND ITS SIDECAR.
#
#   But the sidecars live in THIS session's working directory, which is internal
#   and is never delivered (S0-1 / R-DELIVER lists the closed set: the docx and
#   the registry). So Step 8 saw spec == {} on every figure, fc.is_legacy() read
#   every v5.33 render as pre-v5.33 output, and EC-V18 leniency was applied to
#   papers that were not legacy at all. The gates could not fail on a real
#   regression because they never had the record to compare against.
#
#   THE FIX. S13-4 writes the sidecars into
#   registry.figural_manifests[].figure_specs, keyed by the canonical PNG name
#   S10-8 already stamps on each drawing (_name_last_drawing ->
#   "q{N}_problem.png" / "q{N}_opt{i}.png"), which is the same base
#   write_spec_sidecar() names the sidecar after. The registry is the sanctioned
#   channel for precisely this: it is the one artefact Step 8 receives, and it
#   is the precedent object_types/subtopic_ids set at v5.31 for the identical
#   reason. Absent-safe both ways — a session that rendered no figural_core
#   figure writes no sidecar, the field is {}, and Step 8 reads legacy, i.e.
#   exactly the pre-v5.34 behaviour. Nothing is written to the docx and nothing
#   new is delivered; B3/R-DELIVER cardinality is untouched.
#
# v5.33.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   1267 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_MockTestCreate'. The current companion block, the
#   v5.33 entry, and all structural notes remain in-file. Body byte-untouched.
#
# v5.33 — 2026-07-29 — FIGURE COLOUR, LABEL LEGIBILITY AND PLACEMENT SCALE
#   (GAP-2026-07-29-FIG-R2 + VERIFY-2026-07-29-FIG-R2).
#   Measured across 208 delivered drawings in four exhibits: 0 of 55 IIT JAM figures
#   contained a single coloured pixel; placement scale was 0.500 EXACTLY on 24 of 24
#   option canvases; on-page labels ran to a median of 6.7 pt; 0 of 208 drawings
#   carried alt text. The three GATE papers, believed correct, measured 115 of 153
#   figures below a 9 pt floor — they were not a working reference, only a quieter
#   failure, and their colour came from session code that bypassed this spec entirely
#   (three distinct document-assembly paths across four exhibits).
#   FOUR root causes, not one:
#     RC-1 S10-7 Q7 MANDATED "solid black". The monochrome output was CONFORMANT.
#          The implementation was faithful; this spec was the defect.
#     RC-2 FIG_NATIVE_HEADROOM=2.0 supersampled the canvas and was never compensated
#          in the font size, while placement width came from a CONFIGURATION constant
#          rather than the saved artefact. p_page = p_native x S, and the spec
#          controlled neither S nor p_page. A 10 pt label landed at 5 pt.
#     RC-3 Nothing required colour to be redundant with a second visual channel, so
#          greyscale printing and colour-blind readers were served by luck.
#     RC-4 (found by VERIFY, absent from the gap) render_figural_image() sets
#          ax.axis("off") in BOTH branches, and the corpus contained no set_xlabel,
#          no set_ylabel, no legend, no rcParams and no fontsize anywhere. It is an
#          abstract-geometry GLYPH renderer and was being used for scientific data
#          figures, which it structurally cannot label. S8-5, the section that would
#          hold the data-figure path, was an empty title; insert_chart_image(), the
#          function that would call it, was referenced and never defined.
#   Fix: (1) new engine figural_core.py — the data-figure renderer the framework never
#   had, beside (not replacing) the geometry-glyph path. (2) S10-6A FIGURE CLASS
#   taxonomy; class is declared, never defaulted. (3) S10-7 Q2/Q3/Q7 rewritten, Q7b and
#   Q9 added. (4) S10-8 places from the FigureSpec and stamps alt text. (5) S8-5 filled.
#   DISPLAY WIDTH IS A LAYOUT DECISION AND STAYS FIXED; the render is solved to fit it.
#   The inverse rule (place every figure at its native size) was measured and REJECTED:
#   it inflates figure area 1.84x and makes a four-option MCQ need 10.4 in of option
#   stack against a ~9.0 in page text height, orphaning options from their stem.
#   FIG_NATIVE_HEADROOM is retired to 1.0 and bbox_inches="tight" is banned on this
#   path; constrained_layout gives the same margins with a deterministic size, so
#   S == 1.0 by construction rather than by luck.
#   G-FIGLABEL is ARITHMETIC over recorded render-time font metrics, NOT pixel
#   connected components: verified counter-example — three renders at an identical
#   10 pt request and identical saved width, and the one whose axis titles carried
#   "µmol photons m⁻² s⁻¹" and "Net CO₂ assimilation" measured 8.5 pt while
#   short-label renders measured above the floor. A pixel gate is biased against
#   exactly the scientific notation Q9.4 mandates.
#
# ════════════════════════════════════════════════════════════════════════
#
# VERSION HISTORY:
# ════════════════════════════════════════════════════════════════════════
# QUESTION: IS mock_test_audit.py REQUIRED?
# ════════════════════════════════════════════════════════════════════════
#
# SHORT ANSWER: YES for Step 8 (MockCreateAudit). NO for Step 7 to operate.
#
# DETAILED ANSWER:
#
# Step 7 (THIS spec) performs a SELF-AUDIT after each batch.
# Step 8 (MockCreateAudit) performs an INDEPENDENT AUDIT of the finished mock.
#
# The mock_test_audit.py script is referenced in TWO different specs:
#
#   In THIS spec (Step 7): the script's --self-test is a FIXTURE-BASED working-auditor
#     check (v2.6). It must print "SELF-TEST: N/N PASS" with N >= AUTH_GATE_FLOOR (35) AND
#     be fixture-based (builds docx fixtures; asserts each gate CATCHES a planted defect and
#     PASSES a clean one). The canonical auditor (Framework_MockTestCreateAudit.md Appendix
#     A) self-tests 78/78. Request a corrected script if it prints N/M with N≠M, N < 35, is a
#     CONSTANT-PRINT stub (no fixtures), exits non-zero, or errors. (The old "24/24"/"13/13"
#     literals and the accept-ANY-N/N rule are superseded — see GATE-COUNT CONTRACT below.)
#     PURPOSE: Self-check before Q1 to verify the script works.
#     IF MISSING: Step 7 CANNOT run the script but CAN still run using
#     spec-level (Claude-executed) gate checking per S4-10/S4-11.
#     THE KEY INSIGHT: The original T2 spec was written assuming the audit
#     script ALWAYS exists. For universal Step 7, we must handle its absence.
#     v3.0 DECISION: audit.py absence → WARN (not HARD STOP) + manual checklist.
#
#   In Step 8 spec (MockCreateAudit): Framework_MockTestCreateAudit.md §1 says:
#     "mock_test_audit.py missing → HARD STOP: Upload mock_test_audit.py to project."
#     PURPOSE: Step 8 cannot run Part A (machine gates) without it.
#     IF MISSING: Step 8 CANNOT proceed at all.
#     v3.0 DECISION: HARD STOP in Step 8 is correct. User MUST create and upload it.
#
# THEREFORE:
#   Step 7 (MockCreate): audit.py OPTIONAL — recommended but not blocking
#   Step 8 (MockCreateAudit): audit.py MANDATORY — hard stop without it
#
# SOURCE OF AUDIT SCRIPT (v5.11):
#   Step 6 (MockBlueprint) v1.20+ auto-generates [ExamCode]_mock_test_audit.py
#   as its 6th output file (see Framework_Blueprint.md §13-7A).
#   The script is uploaded to [ExamCode] project Files alongside blueprint.json,
#   registry.json, and other Step 6 outputs.
#   If missing at Step 7 start: verify Step 6 outputs were uploaded to project.
#   The generated script IS the full canonical auditor (no separate "upgrade" step —
#   see Framework_MockTestCreateAudit.md Appendix A + Step 6 §13-7A).
#
# ── GATE-COUNT CONTRACT (v5.17 — ONE canonical auditor; fixture-based self-test) ──
# There is now ONE auditor across the pipeline, defined in
# Framework_MockTestCreateAudit.md Appendix A (v2.6+): the AUTHORITATIVE A-* gate set that
# gates Step-8 delivery, carrying the --audit-state COMPLETION GATE (S5-1A, C1-C7) and a
# FIXTURE-BASED self-test (SELF-TEST: N/N, N >= AUTH_GATE_FLOOR = 35; the canonical build
# self-tests 78/78). Step 6 generates it; Step 7 optionally runs it; Step 8 mandatorily runs
# it. The old two-auditor / 13-vs-66 split is RETIRED — it enabled the hollow-stub false-clean.
# RULE (v2.6 — kills BOTH count-drift AND the hollow stub): a caller runs `--self-test` and
#   accepts "SELF-TEST: N/N PASS" ONLY WHEN the self-test is FIXTURE-BASED (builds docx
#   fixtures; asserts each gate catches a planted defect and passes a clean one) AND
#   N >= AUTH_GATE_FLOOR (35), exit 0. A CONSTANT-PRINT "N/N PASS" that executes no fixtures
#   is REJECTED — it is not a working auditor (P1 hardened, Framework_MockTestCreateAudit.md).
#   The specific N (35, 43, …) above the floor is INFORMATIONAL; fixture-based + floor is the
#   pass/fail criterion. The stale literals "13/13", "24/24", "52", "65", "66/66" are superseded.
#
# ════════════════════════════════════════════════════════════════════════
# MANDATE 0 — NO QUESTION CONTENT IN CHAT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#
# ALL question content goes to the .docx file ONLY.
# NEVER print any question text in chat: not during generation, not for
# verification, not in debug output, not in status updates.
# If referencing a Q: use ONLY "Q.12 — gate failed" — never the actual stem.
# VIOLATION = exam compromise. This overrides every other instruction.

# ════════════════════════════════════════════════════════════════════════
# MANDATE 1 — BATCH STOP LAW (DERIVED FROM PRIMARY SOURCES)
# ════════════════════════════════════════════════════════════════════════
#
# SOURCE: T2_MockCreate.md R10, R22, R23, R24, §5 batch flow.
#
# R10:  "Wait for 'continue' trigger before each batch; do not auto-advance."
# R22:  "present_files FORBIDDEN until audit exit 0 + zero fixable WARNs;
#        MANDATORY immediately after."
# R23:  "Append audit STDOUT to batch reply."
# R24:  "Final Assembly runs automatically after Batch 13 (Computer)."
# §5:   "After every batch audit exits 0: call present_files with cumulative
#        docx — MANDATORY."
#
# WHAT THIS MEANS IN CONCRETE TERMS:
#
# After generating questions for ONE batch (max 10Q):
#   STEP 1: Run gate checks (script OR manual checklist)
#   STEP 2: Fix any fixable WARNs. Re-run checks. Iterate.
#   STEP 3: Print "=== BATCH [N] COMPLETE ===" with gate results
#   STEP 4: Call present_files with cumulative docx
#   STEP 5: Print "Type 'continue' to begin Batch [N+1]."
#   STEP 6: *** END THE RESPONSE *** — write NOTHING more
#
# STEP 6 IS THE KEY FAILURE POINT FROM M1.
# Claude generated all 100Q in one response without stopping at Step 6.
# This is now a NAMED MANDATE with equal force to MANDATE 0.
#
# THE "CONTINUE" CONTRACT:
#   - Only "continue" / "go" / "next" (case-insensitive) starts next batch
#   - Any other user message → answer it → end with "Type 'continue'..."
#   - Claude NEVER decides to continue without user trigger
#   - "I'll now start the next batch" in same response = MANDATE 1 violation
#
# FINAL BATCH EXCEPTION (R24):
#   The LAST batch triggers Final Assembly automatically after gate checks.
#   No "continue" needed for Final Assembly — it runs in same response.
#   But all batches BEFORE the last still require explicit "continue".

# ════════════════════════════════════════════════════════════════════════
# MANDATE 2 — GENERATION TECHNOLOGY (retained from v2.0 GAP-05)
# ════════════════════════════════════════════════════════════════════════
#
# For any exam section containing mathematical content (fractions, surds,
# exponents, trigonometry, algebra):
#   MANDATORY: Python + python-docx + OMML helpers (§10-S10-4)
#   BANNED: npm docx package (cannot produce OMML — math renders as plain text)
# For pure text-only exams: either Python or npm docx acceptable.
# NEVER use npm docx when a QA/math section is present.


# ════════════════════════════════════════════════════════════════════════
# §1 — PIPELINE POSITION & SOURCES OF TRUTH
# ════════════════════════════════════════════════════════════════════════

## S1-1 — Pipeline position

  Step 5 (PYQExtract)  → produces [ExamCode]_section_rules.md
  Step 6 (MockBlueprint) → produces [ExamCode]_blueprint.json,
                               [ExamCode]_registry.json (empty template),
                               [ExamCode]_ExplainLearnings.md,
                               [ExamCode]_ExplainAuditLearnings.md
  THIS STEP — Step 7 (MockCreate) → produces [ExamCode]_Mock[N]_Create.docx,
                               updated [ExamCode]_registry.json
  Step 8 (MockCreateAudit) → consumes outputs of this step

  PREREQUISITE: Step 0 AND Step 1 must both be complete.
  section_rules.md AND blueprint.json must both be in project knowledge.

## S1-2 — Sources of truth (strict priority order)

  Priority 1: This spec (Framework_MockTestCreate.md)
  Priority 2: [ExamCode]_blueprint.json  — allocation, format, structure
  Priority 3: [ExamCode]_section_rules.md — subtopic rules, templates, patterns
  Priority 4: [ExamCode]_registry.json   — cross-mock dedup state

  CONFLICT RULE: blueprint.json ALWAYS wins over section_rules.md on
  format assignments, allocation counts, and structural decisions.

## S1-3 — Exam-agnostic guarantee

  Zero hardcoded exam values. Same spec runs for SSC CGL Tier 1,
  SSC CGL Tier 2, GATE, NEET, IBPS PO, CAT, UPSC CSAT, any exam
  with valid Step 0/1 outputs.

## S1-4 — Memory prohibition

  ABSOLUTE: Claude must NEVER use training memory to decide subtopic scope,
  content facts, PYQ patterns, formats, ciphers, or approaches.
  ALL decisions come from files read at session start.
  For fact-recall content: web-verify before using. DOCUMENTS WIN OVER MEMORY.

# ════════════════════════════════════════════════════════════════════════
# §2 — TRIGGER FORMAT & UNIVERSAL ABSOLUTE RULES
# ════════════════════════════════════════════════════════════════════════

## S2-1 — Trigger formats

  PRIMARY: TestCreate P[N] [--level <mock|subject|topic|subtopic>] [--scope <Subject[::Topic]>]
  STATUS:  TestCreate status
  RESUME:  TestCreate P[N] resume   (v3.0 — see S4-12)

  ALIAS (v5.28 — mock-only, working alias, unchanged behaviour):
    MockCreate M[N]          == TestCreate P[N] --level mock
    MockCreate status        == TestCreate status
    MockCreate M[N] resume   == TestCreate P[N] --level mock resume

  --level: selects WHICH blueprint tier to generate from when more than one
    [ExamCode]*_blueprint.json is present (§3 S3-1/S3-2, pp.pick_blueprint).
    mock            → [ExamCode]_blueprint.json (no --scope needed)
    subject         → requires --scope <Subject>
    topic           → requires --scope <Subject::Topic>
    subtopic        → requires --scope identifying the subtopic-scoped blueprint
    Omitted (Test* with no --level): single-active default — resolves automatically
    ONLY if exactly one blueprint file is present; otherwise pp.pick_blueprint raises
    PickError and Claude HARD STOPS with its actionable message (does not guess).
    MockCreate M[N] always sets level='mock' implicitly — --level is never needed
    (and is ignored if given) on the Mock* alias.

  ExamCode: read from exam_config.json in project knowledge; must match blueprint + registry.
  [N]: integer ≥ 1 (P[N] for TestCreate, M[N] for the MockCreate alias — same meaning: the
       paper number within the selected blueprint's series); must ≤ that blueprint's
       total_mocks/n_papers. Identity is paper_id (= blueprint.mocks[N].paper_id): it must
       not already be in registry.papers_completed[] (legacy registries fall back to
       mocks_completed[] for the mock tier only).

## S2-2 — Universal Absolute Rules table

  R1:  Never copy PYQ verbatim or near-verbatim.
  R2:  No question repeated across mocks (registry dedup L1-L18).
  R3:  No image reused across any 2 questions (dHash + MD5).
  R4:  Every question has exactly 4 unique options (unless options_count≠4).
       — v4.7 NAT EXEMPTION: a NAT question (answer_type=='numerical') has ZERO options.
         R4 does not apply to it; option-count is governed by G-NAT-NOOPT instead.
  R5:  No answer key, correct marker, or hint anywhere in the paper.
       — INCLUDES: no answer key page at end of docx
       — INCLUDES: no asterisk, no bold correct option, no "correct" annotation
       — DETECTION: scan docx for "Answer Key", "Answers:", "Key:", "Q\.\d+.*→.*[1-4]"
       — HARD STOP if found: do not deliver until removed.
  R6:  Match blueprint allocations exactly.
  R7:  Q1 through QN continuous, no gaps, monotonic in document order.
  R8:  No section headings inside the paper body.
       — BANNED (KEYWORD form): "SECTION: ...", "Section I:", "Part A:", any divider lines.
       — BANNED (SECTION-NAME form, v4.8): a standalone body paragraph that IS a declared
         section NAME (e.g. "Reasoning", "Technical", or any name from blueprint
         sections[].section_name for the exam being generated)
         — the realistic section-header shape, which the keyword list does not cover. A
         questions-only paper (Q.N-first) has no standalone non-Q/non-option paragraph, so any
         body line equal to a section name (blueprint sections[].section_name) is a leaked
         header. Detection is PROVENANCE-BASED (matched against this paper's own section names),
         never a generic word list — exam-agnostic.
       — HARD STOP. Detection: scan all body paragraphs (a header may sit before the first Q
         or between sections), before and during assembly. Independently re-verified by
         Step 8 A-SECHDR.
  R8b: No title / info / scoring / cover / instruction block before Q.1 (v5.18).
       — The generated paper is questions-only at the DOCUMENT level (not merely per-block):
         the FIRST non-blank body paragraph of the docx MUST be the bold "Q.1" stem. No title
         ("... Mock Test [N] ..."), no "Total Questions / Maximum Marks / Time" line, no
         "Each question carries ... Negative marking ..." instruction, and no cover/preamble
         may precede Q.1.
       — CATEGORY-C values (marks_per_q, time_per_q_sec, negative_marking, options_count,
         total_questions) are STRUCTURED METADATA carried in section_rules.md / blueprint.json
         and the registry — they are NEVER rendered as printed paragraphs in the paper. A
         downstream platform may display them from that metadata; the .docx never prints them.
       — Blank separator paragraphs before Q.1 are NOT a violation (they carry no text); only
         a non-blank, non-Q.N, non-option paragraph before Q.1 is.
       — EXEMPTION (dormant, exam-agnostic): if — and only if — section_rules.md EXAM_STRUCTURE
         explicitly declares `paper_header_block` (a deliberate per-exam opt-in), a printed
         header matching that declaration is permitted and gate G-PREQ1 is dormant. No current
         section_rules.md declares it, so the ban is absolute for every present exam.
       — HARD STOP. Detection: scan every paragraph before the first "Q.<N>" stem, before and
         during assembly. Enforced by gate G-PREQ1; independently re-verified by Step 8
         A-HEADER (which strips the block, not merely validates it). Distinct from R8
         (section-name headers inside the body) and R9 (docx page header/footer region).
  R9:  No header, no footer (unless EXAM_STRUCTURE in section_rules.md says otherwise).
  R10: Option labels per exam — read option_label_format from exam_config.json
       or blueprint (S3-2). Default: "{i}.  {text}" (number, dot, two spaces).
       The configured format drives both generation (add_text_options) and gate
       G-OPTLABEL (OPTION_LABEL_RE built from the format at S3-2).
  R11: Wait for "continue" trigger before each batch. NEVER auto-advance. (= MANDATE 1)
  R12: No answer key sidecar or figural manifest in deliverable docx.
  R13: Every Q-stem bold. 4 option paragraphs follow. Blank separator after.
       — v4.7 NAT EXEMPTION: a NAT question (answer_type=='numerical') has ZERO option
         paragraphs — only the bold Q.<N> stem (carrying the nat_instruction per R14) and
         the blank separator. Enforced by G-NAT-NOOPT (no options) + G-NAT-INSTR (instruction).
  R14: Exactly one bold Q.<N> stem paragraph per question, and it MUST be the
       FIRST non-empty paragraph of the question's block (v3.7 Q.N-FIRST). No
       stimulus/table/chart/passage/preamble may precede "Q.<N>". For linked
       members the Q.<N> attaches to the shared context line (§9 SC-3). Enforced
       by gate G-QNUM-FIRST.
       — v4.7 NAT: for a NAT question the candidate-facing nat_instruction (blueprint
         nat_contract; e.g. "Enter your answer as a numerical value.") is appended INSIDE
         the bold Q.<N> stem paragraph (never a separate paragraph, never an option), exactly
         as the MSQ multi-select instruction is. Enforced by G-NAT-INSTR.
  R15: present_files FORBIDDEN until gate checks pass.
  R16: present_files MANDATORY immediately after gate checks pass (per batch).
  R17: Options grammatically and logically consistent with stem.
  R18: Every Q number within its section's q_range (blueprint.sections[]).
  R19: No 2+ consecutive questions from same subtopic. (v3.8 extension) Also:
       (a) no two questions sharing a CONCEPT_GROUP may be adjacent;
       (b) no contiguous run > 2 questions from the same PRESENTATION_FAMILY
           (a coarse surface-look grouping, e.g. "vocab_single_word_pick" =
           {antonym, synonym, spelling, homonym, one_word_substitution});
           where section composition makes a longer run unavoidable, maximise
           spread and never exceed run = 3;
       (c) a subtopic's N questions are DISTRIBUTED across its section, not
           clustered. Checked in the S4-11 manual checklist (G-CLUSTER item).
       Rationale: even presentation-varied questions read as repetitive when the
       same family is stacked back-to-back (M1 Q.77–Q.80 were four vocab-single-
       word questions in a row). Complements RULE C (which fixes look) with
       distribution (which fixes adjacency).
  R20: Print gate check results in chat after every batch, before present_files.
  R21: At least one statement/option must be TRUE in multi-statement Qs.
  R22: Output as .docx only — NEVER print questions in chat. (= MANDATE 0)
  R23: Final Assembly runs automatically after the last batch. (= MANDATE 1 exception)
  R24: FONT AND SIZE per exam — read from exam_config.json (keys: font_name,
       font_size_pt). Defaults: Calibri, 11. Arial BANNED (unless it IS the
       configured font). Apply the configured font/size uniformly:
       — Stems: configured font, configured size, bold.
       — Options: configured font, configured size, normal weight.
       — Verify: scan all runs; if run.font.name not in [configured_font, None]: fix.
  R-DELIVER (v3.5, HARD STOP): Step 7 delivers EXACTLY two files at Final
       Assembly — [ExamCode]_Mock[N]_Create.docx and [ExamCode]_registry.json —
       and NOTHING else. Producing a standalone answer-key file (any format:
       .docx/.pdf/.json/.txt) as a deliverable is forbidden with the same force
       as R5 (no answer key in the paper). Internal sidecars (answer_key.json,
       fig_manifest.json, batch_state.json, progress.json) are NEVER delivered.
       The learner-facing answer key is a Step-4 (MockExplain) artefact, not
       a Step-7 one. Enforced by S13-6, S13-7, and gate G-DELIVERY-SET.
  R-LINKED (v3.6, HARD STOP): Every question must be SELF-CONTAINED for
       one-question-at-a-time online rendering. For any linked-stimulus group
       (CLASS 4 — RC passage→Qs, DI table/graph→Qs, Cloze passage→blanks, puzzle
       set→Qs, or any shared dataset backing ≥2 questions), the shared stimulus
       MUST be physically present inside EACH member question's own block — not
       placed once as a loose lead-in before the first question.
       — DEFAULT = MODEL A (stimulus-per-member): duplicate the full stimulus
         (passage text / Word-table object / chart image / cloze paragraph) into
         every member question's stem block, so each question is answerable in
         total isolation.
       — MODEL B (engine-native passage-group) is permitted ONLY when the target
         test-series platform is CONFIRMED (S3) to support a comprehension/passage
         container that pins one stimulus across a tagged set. If unconfirmed,
         use Model A. Never rely on a loose lead-in paragraph (that is neither).
       — A "lead-in only" layout (stimulus before Q1 of the group, absent from
         Q2..Qn) is BANNED with the same force as R5/R8.
       — Q.N-FIRST (v3.7, HARD STOP): every question block — single OR linked —
         MUST OPEN with its "Q.<N>" paragraph. No paragraph, table, chart, or
         passage may precede the Q-number. For a linked group the Q-number
         attaches to the SHARED CONTEXT / INSTRUCTION line, e.g.
         "Q.74  Study the following table and answer the question. ...". The
         stimulus follows the Q.N line; the specific ask is a separate bold,
         non-numbered paragraph after the stimulus. Stimulus-first / preamble-
         first layouts are BANNED. Reference: §9 SC-3 ordered block.
       Enforced by §9 (SC-1..SC-7), S10-LINKED helper, R14, and gates
       G-STIMULUS-ORPHAN + G-QNUM-FIRST.
       — v4.7 LINKED-NAT (ND11): a linked/DI group MAY contain members whose subtopic is
         answer_type=='numerical' (a shared table/chart followed by numerical-answer
         questions — common in GATE/CAT DI). A NAT member is a 0-option member: the SHARED
         stimulus is still embedded per member (Model A self-containment, SC-1..SC-7 and
         G-STIMULUS-ORPHAN unchanged), the Q.N-first ordering holds, and the member simply
         emits no option paragraphs (R13 NAT exemption) and carries the nat_instruction
         (R14). Stimulus embedding, atomic-group batching, and self-containment are
         orthogonal to whether a member has options — so NAT members compose without any
         change to the linked machinery beyond permitting the 0-option member.
  R-FIGURAL (v4.0, HARD STOP): Every figural MCQ must be DECOMPOSED, not a
       composite panel. It is rendered as the problem/series figure(s) as their
       OWN image(s) PLUS one SEPARATE image per option, bound 1:1 to its "i."
       label and stacked SINGLE-COLUMN (exactly one option image per line — never
       two options on a line, never a table row of option images). A single image
       containing the problem and all options baked together is BANNED with the
       same force as R5/R-LINKED: the online engine renders one option region per
       screen and cannot slice a baked panel, and a fused panel decouples each
       figure from its answer label. No stem, caption, instruction, or option
       number may be baked into any raster — those are document text; only
       INTRINSIC figure annotations (mirror-line endpoints M/N, geometry vertices,
       axis labels) belong inside the image. Reference lines/axes are DRAWN as real
       geometry, never floating letters. Image quality is fixed by framework
       constants (FIGURAL_DPI=300, uniform option canvas, lossless PNG, vector-first
       geometry, FIG_MIN_STROKE_PT). The stem stays Q.N-first document text (R14).
       Enforced by §10-S10-7 (image-quality contract) + §10-S10-8
       (add_figural_question) + view-tool verification + gate G-FIGURAL-COMPOSITE.
       — v4.7 FIGURAL-NAT VARIANT (ND10): when a figural question's subtopic is
         answer_type=='numerical' (e.g. a GATE geometry/mensuration diagram with a typed
         answer), it has a PROBLEM image (or series images) but ZERO option images — there
         are no options to decompose. The "one image per option / ≥ n_options+1 images / 1:1
         option-label binding" requirement DOES NOT APPLY; G-FIGURAL-COMPOSITE must skip its
         per-option-image arm for a numerical figural question and require only that the
         problem image(s) obey the single-column / no-composite / 300-DPI / named-image
         (q{N}_problem[_k]) discipline. The answer obeys the NAT value+tolerance contract
         (R-ANSWER numerical branch) and the stem carries the nat_instruction (R14). Without
         this variant a valid figural-NAT would be hard-stopped for "missing option images".
  R-UNDERLINE (v4.1, HARD STOP): Every question that asks about an UNDERLINED
       span — vocabulary/grammar items presented as 'sentence_embedded_underlined'
       (antonym/synonym/of-the-underlined-word), sentence-improvement ("improve the
       underlined part of the sentence"), error-spotting on an underlined segment,
       or any stem that refers to "the underlined word/part/segment/phrase" — MUST
       render that target span as a GENUINE underlined run (python-docx
       run.underline = True; XML <w:u>) sitting inside the sentence at its natural
       position. BANNED with the same force as R5: emitting the target as a
       plain-text parenthetical annotation appended to the stem — "(underlined: X)",
       "(underline: X)", "(underlined word: X)" — or appending the target in any
       bracketed/quoted note in lieu of underlining the in-sentence span. Underlines
       are real character formatting, NEVER drawn with underscore characters
       ("____") or markdown. The instruction text itself ("improve the underlined
       part…") is NOT underlined; only the target span is. Enforced by §10-S10-2
       (add_stem_with_underline + UNDERLINE_TRIGGER), the tightened render-
       consistency contract (§7 G4 stem_matches_format), and gate G-UNDERLINE.
  R-OPTREF (v4.2, HARD STOP): A stem may not REFERENCE a terminal/escape option
       that the option set does not actually contain, and the instruction's promised
       option-structure must match the rendered options. Specifically:
       — If the stem instructs the candidate to choose a terminal escape option in
         the "no positive answer" case — e.g. "if there is no error, (select/mark)
         the last option", "select 'No improvement'", "None of these / None of the
         above", "All of the above", "Both … and …", "Neither … nor …" — then that
         option MUST be PRESENT in the option set, at the position the instruction
         names (a "last option" reference ⇒ it is option N).
       — A "pick the segment/part that contains the error" layout (every option is a
         sentence SEGMENT) may NOT carry a "no error → last option" escape
         instruction unless a real "No error" option is appended; conversely a
         "No error"-escape instruction REQUIRES the escape option and the matching
         3-segment (N−1) split. The instruction template and the option structure
         must be the SAME template.
       This is EXAM-AGNOSTIC: the permitted escape/terminal tokens and per-section
       option structures are read from section_rules.md (none_of_above_permitted at
       S3-12, wrong_option_structure / fixed_set at S3-13). The framework enforces
       coherence; it hardcodes no exam's wording. Carrier-sentence stems
       (error-spotting, sentence-improvement, fill-in-sentence) must also place the
       instruction and the sentence on SEPARATE paragraphs (§10-S10-2, generalised
       in v4.2 — no run-on). Enforced by §10-S10-2 layout + gate G-OPTREF.
  R-ANSWER (v4.5, HARD STOP at generation — generalises v4.2 R-UNIQUE; single source
       of truth, mirrored verbatim by Step 8 RA-12). The contract is parameterised by the
       subtopic's answer_cardinality (blueprint subtopic_list; default 'single'):

     ── answer_cardinality == 'single' (the v4.2 R-UNIQUE rule, UNCHANGED) ──
       Every question must have EXACTLY ONE
       defensible correct option; the other three must be indefensible under ANY
       reasonable reading. A question where a SECOND option is also defensible is a
       defect even though a "key" exists. This cannot be reduced to a regex — it is
       a generation-time reasoning check (the generator already knows the intended
       key and must confirm no other option survives a fair reading). Illustrative
       CLASSES of the failure (examples, NOT a hardcoded list — applies to every
       exam): (a) kinship/relational stems where an unqualified relation
       ("grandmother/grandfather/uncle/aunt") combined with "only son/daughter"
       admits a maternal AND a paternal reading that map to two DIFFERENT listed
       options; (b) any item whose answer depends on a CONTESTED convention (e.g.
       tense treatment of a universal truth in reported speech) while BOTH convention
       outputs sit in the option set; (c) series/analogy stems where two distinct
       rules each yield a listed option. The remedy is always to DISAMBIGUATE the
       stem (qualify the relation, fix the convention via section_rules, constrain the
       rule) or remove the colliding option — never to "pick one and hope".

     ── answer_cardinality == 'multi' (MSQ; v4.5, active only when blueprint multi_present) ──
       The intended key is a SET S of correct option positions. The generation-time
       reasoning obligation INVERTS to a set contract — equally not a regex:
         • EVERY option in S must be defensible (clearly correct) under EVERY fair reading;
         • EVERY option NOT in S must be indefensible (clearly wrong) under ANY fair reading
           — the dangerous failure is a BORDERLINE out-set option that should arguably be
           in S (the MSQ analogue of the two-defensible-answers single-mode defect);
         • S is a NON-EMPTY PROPER subset of {1..options_count}: 1 ≤ |S| ≤ options_count−1
           (k=0 "empty" and k=n "all-correct" are HARD-STOP defects by default);
         • when msq_k_mode == 'fixed', |S| == msq_k EXACTLY;
         • NEGATION composes: for a negated multi stem ("which are NOT correct"), S is the
           set of options satisfying the NEGATED predicate — derive S, then apply the rules
           above to S as derived.
       The remedy for an ambiguous out-set option is the same as single mode: DISAMBIGUATE
       the stem or move/remove the colliding option — never ship an arguable set.
       Escape options under multi obey R-MSQ-ESCAPE.

     ── answer_type == 'numerical' (NAT; v4.7, active only when blueprint nat_present) ──
       This branch is selected by the ORTHOGONAL answer_type axis and SUPERSEDES the
       option-based reasoning above: a NAT question has NO options at all, so there is no
       in-set/out-set to adjudicate. The intended answer is a single typed VALUE, and the
       generation-time obligation is WELL-POSEDNESS:
         • the stem must determine the value UNIQUELY — exactly one numerical answer follows
           from a fair reading (the NAT analogue of "exactly one defensible option"); a stem
           admitting two defensible values (ambiguous rounding convention, under-specified
           figure, missing unit) is a HARD-STOP defect — DISAMBIGUATE the stem;
         • the value's form must match nat_answer_type (blueprint nat_contract): 'integer' ⇒
           an exact integer, no decimals; 'real' ⇒ a decimal carried to the exam's stated
           precision;
         • tolerance: 'integer' ⇒ exact match (no band); 'real' ⇒ the accepted band is
           [value − nat_tolerance, value + nat_tolerance] (or the % form), recorded as
           ca_range = (lo, hi) with lo ≤ hi — this is the SAME ca_range Step 4 renders and
           Step 8 A-NAT-ANSWER re-derives. A '0' tolerance means exact-to-displayed-precision;
         • a zero, negative, or fractional value is valid — the value is stored as data, never
           tested for truthiness, and a fractional value renders as OMML (§11), never inline;
         • the value MUST NOT appear as a GIVEN anywhere else in the paper (no cross-question
           leak) — the same self-containment R-ANSWER demands of any key, here keyed on the
           derived VALUE (enforced by G-NAT-ANSWER + the value-leak arm of S11-4).
         • v5.25 — PORTAL GRADING VALUE (locked, DJ rules; see S7-NEW-C): the typed value above
           is the MATH answer, used for well-posedness/ca_range/OMML display. It is a SEPARATE
           concern from the exact string the delivery portal ingests to auto-grade the question
           — that string must derive from `derive_nat_grading()` (S7-NEW-C), never from ad-hoc
           formatting, and is stored alongside the math value in the sidecar (nat_grading_type,
           nat_grading_value), never inferred later by a downstream step.
       There are no distractors to make indefensible; correctness is the value + its band.

## S7-NEW-C — NAT portal grading value derivation (v5.25, locked DJ rules)

  MOTIVATION: the delivery portal auto-grades a NAT question by exact/tolerant string match
  against ONE field, and that field accepts ONLY the character set `0123456789.-` — no
  scientific notation, no units, no words, no en-dash, no parentheses, no spaces (confirmed
  against the portal's own answer-entry configuration screen). The math VALUE computed above
  (and its ca_range) is exam-content-correct but is NOT automatically portal-safe: a value that
  is legitimately tiny (e.g. a rate stated "in units of 10⁻⁹") or that carries a tolerance band
  must be TRANSFORMED into a portal-safe string before it ever reaches a sidecar, a docx, or an
  audit gate. This transformation is a PURE FUNCTION of (value, ca_range, stem_precision) — it
  is computed ONCE, here, at generation time, and carried forward verbatim by every downstream
  step (Step 8 re-derives it independently; Steps 9-11 render/pass it through, never reformat
  it). EXAM-AGNOSTIC — zero hardcoded exam values; the function reads only its three arguments.

  INPUTS:
    value          : the computed math answer (already expressed in whatever units the stem
                     states — a "units of 10⁻⁹" stem means `value` here is the SMALL number,
                     e.g. 3, not the raw 3×10⁻⁹; that pre-scaling is the author's job when
                     computing `value` in the first place, upstream of this function).
    ca_range       : the SAME (lo, hi) tuple computed above for R-ANSWER/G-NAT-ANSWER, or None.
    stem_precision : int N if the stem contains an explicit rounding instruction ("round off
                     to N decimal places" / "correct to N decimal places"), else None.

  DECISION TREE (zero-halt except the one explicit NOT-SUPPORTED gate below):
  ```python
  from decimal import Decimal, ROUND_HALF_UP
  import re

  _NAT_GRADE_CHARSET = frozenset('0123456789.-')
  _NAT_INTEGRAL_EPS = Decimal('1e-9')   # float-arithmetic-residue guard, NOT a domain judgement

  def _fmt_portal_number(value, precision=None):
      """One bound/value -> a portal-safe string. precision=None -> minimal
      representation (bare integer if integral, else unpadded decimal — this
      is what makes 'Decimal' point-optional / 'decimal-capable' per the
      portal's numeric-tolerance matching, no forced trailing zeros).
      precision=int N -> exactly N digits after the point, zero-padded,
      ROUND_HALF_UP (locked rule — never banker's rounding, never truncation)."""
      d = Decimal(str(value))
      if precision is not None:
          q = Decimal(1).scaleb(-precision)
          d = d.quantize(q, rounding=ROUND_HALF_UP)
          s = format(d, 'f')
      else:
          if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
              s = str(int(d.to_integral_value()))
          else:
              s = format(d.normalize(), 'f')
      if re.fullmatch(r'-0(\.0+)?', s):        # never emit negative zero
          s = s.lstrip('-')
      return s

  def _fmt_portal_range(lo, hi, precision=None):
      lo_s = _fmt_portal_number(lo, precision)
      hi_s = _fmt_portal_number(hi, precision)
      if lo_s.startswith('-') or hi_s.startswith('-'):
          # LOCKED, NOT an inferred default: '-' is both the range delimiter and a
          # possible bound sign, so a negative-bounded range is structurally
          # ambiguous with no confirmed portal-side escape convention. Escalate
          # rather than guess — same halt-on-genuine-ambiguity posture as
          # G-NAT-ANSWER/A-NAT-ANSWER elsewhere in this spec.
          raise ValueError(
              f"NAT range has a negative bound (lo={lo_s!r}, hi={hi_s!r}) — NOT "
              f"SUPPORTED. Rework the question so both bounds are non-negative, "
              f"or get an explicit portal-side range convention confirmed before "
              f"this gate is ever lifted.")
      if Decimal(lo_s) > Decimal(hi_s):
          raise ValueError(f"NAT range lo>hi ({lo_s!r} > {hi_s!r})")
      return f'{lo_s}-{hi_s}'

  def derive_nat_grading(value, ca_range=None, stem_precision=None):
      """Returns (grading_type, grading_value). grading_type is one of
      'positive_integer'|'integer'|'decimal'|'decimal_fixed'|'range'.
      grading_value is the final 0-9.- only string, ready for the sidecar,
      the docx Correct-Answer line, and the portal upload — identical string
      used in all three, never reformatted downstream."""
      # 1. Stem-stated rounding instruction wins outright (overrides both the
      #    range/no-range and the integral/non-integral branches below).
      if stem_precision is not None:
          if ca_range is not None:
              lo, hi = ca_range
              return ('range', _fmt_portal_range(lo, hi, precision=stem_precision))
          return ('decimal_fixed', _fmt_portal_number(value, precision=stem_precision))
      # 2. No stated precision, but a tolerance band exists -> Range type.
      #    (nat_tolerance != 0 for this question, i.e. ca_range is not None,
      #    is the ONLY signal for Range typing — no separate judgement call.)
      if ca_range is not None:
          lo, hi = ca_range
          return ('range', _fmt_portal_range(lo, hi, precision=None))
      # 3. Single exact value: Positive Integer / Integer / Decimal by sign
      #    and integrality, epsilon-tolerant against float noise.
      d = Decimal(str(value))
      if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
          v_int = int(d.to_integral_value())
          return (('positive_integer', str(v_int)) if v_int >= 0
                  else ('integer', str(v_int)))
      return ('decimal', _fmt_portal_number(value, precision=None))
  ```

  CALL SITE (v5.25): computed IMMEDIATELY after the math value + ca_range are finalized for a
  NAT question, BEFORE `write_q_to_sidecar` is called — the two new sidecar fields
  (`nat_grading_type`, `nat_grading_value`) are populated FROM this function's output, never
  independently derived by the sidecar writer itself (single source of truth; see S7-NEW-A).
  A `ValueError` from `derive_nat_grading` (the NOT-SUPPORTED negative-range case) is a
  HARD-STOP defect on the QUESTION, not a formatting bug — DISAMBIGUATE/rework the stem's
  numbers so both bounds are non-negative, exactly as any other well-posedness failure in this
  section is handled; never suppress or work around it.

  Enforced by gate G-NAT-GRADE (S12-NEW-29) at generation time and independently re-derived by
  Step 8's A-NAT-GRADE.

       Enforced by §7 CHECK 3 verify_answer (persisted as answer_verified in the
       S7-NEW-A sidecar) and gates G-UNIQUE (record backstop, both modes) + G-MSQ-SET /
       G-MSQ-CARD (multi only) + G-NAT-NOOPT / G-NAT-ANSWER / G-NAT-INSTR (numerical only).
  R-MSQ-ESCAPE (v4.5, applies only when answer_cardinality == 'multi'): "All of the above" is
       a self-contradictory option under multi-select (it cannot coexist with individually
       selectable correct options) and is REJECTED unless section_rules sets
       msq_allow_aota=true (default false), in which case the gate stands down. "None of
       these" is permitted only as an ordinary selectable option (it is the sole member of
       S when correct, i.e. |S|=1 — never an empty set). Enforced inside G-MSQ-SET.
  R-MATH-OMML (v4.3, HARD STOP): Every algebraic/symbolic expression that
       contains a STACKED FRACTION, an EXPONENT/SUPERSCRIPT, a RADICAL, or any
       built-up structure (per the §10-S10-4 decision tree rules 3-6) MUST render
       as native OMML (python-docx <m:oMath>) inline in the document text. Three
       forms are BANNED with the same force as R5:
       — a RASTER IMAGE of the expression (a <w:drawing> PNG/JPEG of "x + 1/x = 5",
         "x²+1/x²", a surd, a built-up fraction, etc.). The matplotlib/figural/
         image pipeline is for GEOMETRIC FIGURES ONLY (mensuration & coordinate
         diagrams, figural-reasoning panels); it may NEVER be handed an algebraic
         expression. This is the M1 Q.55 defect (two expressions shipped as 300-DPI
         matplotlib PNGs q55_e1/q55_e2 instead of OMML).
       — a SLASH/CARET ASCII fallback ("a/b" stacked fractions, "x^2") in the text
         stream (the long-standing G-FRAC ban).
       — RAW LaTeX (\frac, \sqrt) left unconverted.
       Single Unicode symbols (², ³, √n, ×, ÷, ≤, ≥, ±, π, °, θ) and unit labels
       (km/h, cm²) stay plain text/Unicode per the decision tree rules 1-2 — they
       are NOT built-up structures and do NOT require OMML. The executable home is
       §10-S10-4 (MATH_TRIGGER detector + add_math_stem/emit_math_inline +
       assert_not_math guard); the figural boundary is enforced in §10-S10-7
       (render_figural_image calls assert_not_math). Enforced by gate
       G-MATH-RASTER (image name-contract) and the existing G-FRAC (slash text).
# All checks mandatory. Q1 FORBIDDEN until every check passes.

# ════════════════════════════════════════════════════════════════════════
# §3 — PRE-GENERATION CHECKS (all must pass before Q1)
# ════════════════════════════════════════════════════════════════════════

## S3-1 — File path management and copy protocol

  /mnt/project/ (read-only) → /home/claude/ (working dir)
  /mnt/user-data/outputs/ (delivery)

  ```python
  import shutil, os, json, re, glob
  from pathlib import Path
  EXAM = "[ExamCode]"  # from trigger

  # MANDATORY COPIES (non-blueprint) — HARD STOP if any missing:
  required = [
      f'{EXAM}_registry.json',
      f'{EXAM}_section_rules.md',
      f'{EXAM}_subtopic_manifest.json',   # v3.4 — cross-step contract (REQUIRED)
  ]
  for f in required:
      src = f'/mnt/project/{f}'
      if not os.path.exists(src):
          raise SystemExit(f"HARD STOP: {f} not found in project knowledge. "
                           f"Upload it to [{EXAM}] project Files, then retry.")
      shutil.copy(src, f'/home/claude/{f}')

  # BLUEPRINT DISCOVERY (v5.28, paper_pipeline.py): copy EVERY [ExamCode]*_blueprint.json
  # present in project knowledge — the mock blueprint ([ExamCode]_blueprint.json) AND any
  # scoped blueprints ([ExamCode]_[SCOPETAG]_blueprint.json from ScopedBlueprint). §3 S3-2
  # (pp.pick_blueprint) decides which ONE of these this trigger actually generates from.
  blueprint_srcs = sorted(glob.glob(f'/mnt/project/{EXAM}*_blueprint.json'))
  if not blueprint_srcs:
      raise SystemExit(f"HARD STOP: no {EXAM}*_blueprint.json found in project knowledge. "
                       f"Run MockBlueprint or ScopedBlueprint first, then retry.")
  BLUEPRINT_PATHS = []
  for src in blueprint_srcs:
      fname = os.path.basename(src)
      shutil.copy(src, f'/home/claude/{fname}')
      BLUEPRINT_PATHS.append(f'/home/claude/{fname}')

  # OPTIONAL — audit script (Layer 2 guard — not required for Layer 1):
  audit_py = f'/mnt/project/{EXAM}_mock_test_audit.py'
  AUDIT_AVAILABLE = os.path.exists(audit_py)
  if AUDIT_AVAILABLE:
      shutil.copy(audit_py, f'/home/claude/{EXAM}_mock_test_audit.py')
  else:
      print(f"NOTE: {EXAM}_mock_test_audit.py not found in project. "
            f"This file is auto-generated by Step 6 (MockBlueprint) v1.20+. "
            f"Verify Step 6 outputs were uploaded to project Files. "
            f"Layer 1 batch enforcement (spec-level STOP) will be used. "
            f"Manual gate checklist (S4-11) will replace script gates.")

  # OPTIONAL — figural manifest from prior session:
  fig_src = f'/mnt/project/{EXAM}_fig_manifest.json'
  if os.path.exists(fig_src):
      shutil.copy(fig_src, f'/home/claude/{EXAM}_fig_manifest.json')

  # OPTIONAL — ExplainLearnings (v2.0 GAP-07 fix):
  for learn_file in [f'{EXAM}_ExplainLearnings.md',
                     f'{EXAM}_ExplainAuditLearnings.md']:
      src = f'/mnt/project/{learn_file}'
      if os.path.exists(src):
          shutil.copy(src, f'/home/claude/{learn_file}')
  ```

## S3-2 — Select and load the blueprint — read ALL fields (v2.0 GAP-02 fix; v5.28 pp.pick_blueprint)

  CRITICAL FIX: blueprint.json stores per-mock allocations under
  `mocks[i]['sections'][j]['subtopic_allocations']` — NOT under a
  top-level `allocations` key. The v1.0 spec had `mock_data['allocations']`
  which would raise KeyError on the actual file. This is fixed below.

  ```python
  import paper_pipeline as pp

  # LEVEL / SCOPE_SUBJECT / SCOPE_TOPIC come from the trigger (§2 S2-1):
  #   MockCreate M[N] alias        -> LEVEL='mock', SCOPE_SUBJECT=None, SCOPE_TOPIC=None
  #   TestCreate P[N] --level mock -> same as above
  #   TestCreate P[N] --level subject --scope Physics
  #                                 -> LEVEL='subject', SCOPE_SUBJECT='Physics', SCOPE_TOPIC=None
  #   TestCreate P[N] --level topic --scope Physics::Mechanics
  #                                 -> LEVEL='topic', SCOPE_SUBJECT='Physics', SCOPE_TOPIC='Mechanics'
  #   TestCreate P[N] (no --level)  -> LEVEL=None, SCOPE_SUBJECT=None, SCOPE_TOPIC=None
  #                                    (single-active default; requires exactly one blueprint file)

  blueprints = [json.load(open(p)) for p in BLUEPRINT_PATHS]
  try:
      bp = pp.pick_blueprint(blueprints, level=LEVEL, scope_subject=SCOPE_SUBJECT,
                              scope_topic=SCOPE_TOPIC)
  except pp.PickError as e:
      raise SystemExit(f"HARD STOP: {e}")

  # v5.29 SAFETY CHECK: the {EXAM}*_blueprint.json glob (S3-1) is a PREFIX match — if a
  # different ExamCode's files were ever uploaded into this same project (e.g. "SSC_CGL"
  # vs "SSC_CGL_TIER1"), the glob could sweep in a blueprint that isn't this exam's. The
  # exact-filename match this replaced made that structurally impossible; the glob does
  # not, so it must be checked explicitly rather than trusted implicitly.
  if bp['exam_code'] != EXAM:
      raise SystemExit(
          f"HARD STOP: selected blueprint's exam_code {bp['exam_code']!r} does not "
          f"match the trigger's ExamCode {EXAM!r}. A blueprint file from a different "
          f"ExamCode may have been picked up by the {EXAM}*_blueprint.json glob (S3-1) "
          f"— check this project for a similarly-prefixed ExamCode's files.")

  sr_text = open(f'/home/claude/{EXAM}_section_rules.md',
                 encoding='utf-8').read()

  exam_code         = bp['exam_code']
  exam_name         = bp['exam_name']
  blueprint_version = bp.get('blueprint_version', 'unknown')
  total_mocks       = bp['total_mocks']
  total_questions   = bp['total_questions']
  passage_present   = bp.get('passage_present', False)
  figural_present   = bp.get('figural_present', False)
  di_present        = bp.get('di_present', False)
  multi_present       = bp.get('multi_present', bp.get('msq_present', False))   # v4.6 (Phase-0 back-compat)
  nat_present         = bp.get('nat_present', False)          # v4.7 (default false ⇒ dormant)
  sections          = bp['sections']      # [{name, q_range, total_qs, max_attempt}, ...]
  subtopic_list     = bp.get('subtopic_list', [])
  # v5.10: new fields from Step 6 v1.19 (Step 2a v2.5 exam_config contract).
  # marking_scheme: per-range scoring rules. Each entry has q_range, question_type,
  # correct_marks, negative_marks. Used for per-Q-position marks/type lookup.
  # level: academic level for question complexity calibration.
  # medium: authoritative exam language.
  bp_marking_scheme = bp.get('marking_scheme', [])
  bp_level          = bp.get('level', 'unknown')
  bp_medium         = bp.get('medium', 'unknown')

  # v5.10: Per-Q-position lookup helpers from marking_scheme.
  # These enable exact marks/type for any Q number (e.g., CSIR NET Q.72 → 4 marks, MCQ).
  # When marking_scheme is empty (legacy blueprint), helpers return safe defaults.
  def _marks_for_q(qnum):
      """Return correct_marks for a given Q number from marking_scheme."""
      for ms in bp_marking_scheme:
          if ms['q_range'][0] <= qnum <= ms['q_range'][1]:
              return ms['correct_marks']
      return 1  # default when marking_scheme absent or Q not in any range

  def _type_for_q(qnum):
      """Return question_type ('MCQ'/'MSQ'/'NAT') for a given Q number."""
      for ms in bp_marking_scheme:
          if ms['q_range'][0] <= qnum <= ms['q_range'][1]:
              return ms['question_type']
      return 'MCQ'  # default

  def _neg_for_q(qnum):
      """Return negative_marks for a given Q number."""
      for ms in bp_marking_scheme:
          if ms['q_range'][0] <= qnum <= ms['q_range'][1]:
              return ms['negative_marks']
      return 0  # default
  # v4.5: answer_cardinality lookup by subtopic_id (whole-subtopic mode). Used to set each
  # subtopic_data['answer_cardinality'] at S6-3 classify time and to compute msq_positions
  # for the answer budget. Defaults 'single' for any subtopic (legacy blueprint safe).
  # v4.6 Phase-0 back-compat: accept the pre-unification 'answer_mode' key too.
  answer_cardinality_by_id = {s.get('subtopic_id'): s.get('answer_cardinality',
                                                           s.get('answer_mode', 'single'))
                       for s in subtopic_list}
  # v4.7: answer_type lookup by subtopic_id (the NAT dispatch axis, orthogonal to
  # cardinality). Defaults 'option' for any subtopic ⇒ legacy/non-NAT blueprints are inert.
  answer_type_by_id = {s.get('subtopic_id'): s.get('answer_type', 'option')
                       for s in subtopic_list}

  # v5.X POSITION-BASED QUESTION TYPE (GAP-2026-07-22-001 §6 FIX):
  # For question-type sections (e.g. IIT JAM: Section A=MCQ, B=MSQ, C=NAT), the same
  # subtopic can appear in different sections with different question types. The per-subtopic
  # answer_cardinality/answer_type from section_rules is unreliable — it reflects PYQ
  # observation majority, not the section's authoritative type.
  # DUAL-MODE DISPATCH (mirrors Framework_MockDeliver.md v1.7 FIX):
  #   > 1 distinct question_type in marking_scheme → POSITION-BASED: answer_cardinality and
  #     answer_type derived from the Q position's marking_scheme entry via _type_for_q().
  #   0 or 1 distinct type → SUBTOPIC-BASED: unchanged, uses per-subtopic values from
  #     blueprint subtopic_list (current behavior). Also covers legacy blueprints with no
  #     marking_scheme (empty → 0 types → subtopic-based, byte-identical to pre-v5.X).
  _distinct_q_types = {ms.get('question_type') for ms in bp_marking_scheme
                       if ms.get('question_type')}
  _position_based_typing = len(_distinct_q_types) > 1

  def _resolve_answer_axes(qnum, subtopic_id):
      """Return (answer_cardinality, answer_type) for a question at position qnum.
      Position-based mode: derives from marking_scheme (authoritative for question-type
      sections). Subtopic-based mode: from blueprint subtopic_list (current behavior)."""
      if _position_based_typing:
          qt = _type_for_q(qnum)
          if qt == 'MSQ':
              return ('multi', 'option')
          elif qt == 'NAT':
              return ('single', 'numerical')
          else:  # MCQ or unknown
              return ('single', 'option')
      else:
          return (answer_cardinality_by_id.get(subtopic_id, 'single'),
                  answer_type_by_id.get(subtopic_id, 'option'))
  difficulty_schedule = bp.get('difficulty_schedule', [])
  # v5.14 THREE-AXIS: per-section format-distribution target (Step 6 v1.23 axis_schedule).
  # Absent-safe: pre-v1.23 blueprint → {} → the whole Axis-2 steering path stays inert and
  # generation behaves exactly as v5.13.
  axis_schedule = bp.get('axis_schedule', {})
  zero_pyq_rotation = bp.get('zero_pyq_rotation', {})

  # v5.6 EXAM-AGNOSTIC CONFIG — font, option labels, styling. PRIMARY source is
  # section_rules.md (matching Step 8's cat_c reads: font_family, option_label_format).
  # exam_config.json is an OPTIONAL OVERRIDE. Defaults match the SSC CGL reference
  # implementation. Zero hardcoded exam values — every constant has a config path.
  _ecfg_path = f'/home/claude/{EXAM}_exam_config.json'
  _ecfg = {}
  if os.path.exists(_ecfg_path):
      _ecfg = json.load(open(_ecfg_path, encoding='utf-8'))
  elif os.path.exists(f'/mnt/project/exam_config.json'):
      _ecfg = json.load(open(f'/mnt/project/exam_config.json', encoding='utf-8'))

  def _sr_field(field, default):
      """Read a CATEGORY-A field from section_rules.md (same source as Step 8 cat_c)."""
      m = re.search(rf'^\s*{re.escape(field)}\s*[:=]\s*(.+?)\s*$', sr_text, re.M)
      return m.group(1).strip() if m else default

  # Priority: exam_config OVERRIDE > section_rules PRIMARY > blueprint fallback > default
  FONT_NAME        = _ecfg.get('font_name',
                       _sr_field('font_family', bp.get('font_name', 'Calibri')))
  FONT_SIZE_PT     = int(_ecfg.get('font_size_pt',
                       _sr_field('font_size_pt', bp.get('font_size_pt', 11))))
  _sr_label        = _sr_field('option_label_format', None)
  # section_rules uses '1/2/3/4' notation; convert to '{i}.  {text}' template if needed.
  if _sr_label and '/' in _sr_label and '{' not in _sr_label:
      _token = _sr_label.split('/')[0].strip()  # '1' or 'A' or 'a' or 'i'
      if _token.isdigit():
          _sr_label = '{i}.  {text}'
      elif _token.isupper():
          _sr_label = '({alpha_upper})  {text}'
      elif _token.islower():
          _sr_label = '({alpha_lower})  {text}'
  OPTION_LABEL_FMT = _ecfg.get('option_label_format',
                       _sr_label or bp.get('option_label_format', '{i}.  {text}'))
  # Regex for gate G-OPTLABEL built from the configured format:
  import re as _re_cfg
  _opt_prefix = OPTION_LABEL_FMT.split('{text}')[0].replace('{i}', r'\d+')
  _opt_prefix = _opt_prefix.replace('{alpha_upper}', r'[A-Z]').replace('{alpha_lower}', r'[a-z]')
  OPTION_LABEL_RE  = _re_cfg.compile(r'^\s*' + _re_cfg.escape(_opt_prefix).replace(
                         _re_cfg.escape(r'\d+'), r'\d+').replace(
                         _re_cfg.escape(r'[A-Z]'), r'[A-Z]').replace(
                         _re_cfg.escape(r'[a-z]'), r'[a-z]'))
  DI_HEADER_COLOR  = _ecfg.get('di_header_color',
                       _sr_field('di_header_color', bp.get('di_header_color', '1F4E79')))
  # FONT_BANNED: fonts that are never acceptable UNLESS they ARE the configured font.
  FONT_BANNED      = {f.lower() for f in _ecfg.get('font_banned', ['Arial'])} - {FONT_NAME.lower()}

  mock_entry = next((m for m in bp['mocks'] if m['mock'] == N), None)
  if not mock_entry:
      raise SystemExit(f"HARD STOP: Mock {N} not found in blueprint.json mocks[].")

  # BUILD allocations dict from actual blueprint schema:
  # blueprint stores: mocks[i].sections[j].subtopic_allocations
  # We build: allocations = {section_name: {subtopic_name: q_count}}
  # AND alloc_ids = {section_name: {subtopic_id: {q_count, display_name}}}  (v3.4)
  allocations = {}
  alloc_ids = {}
  for sec in mock_entry.get('sections', []):
      sec_name = sec['section_name']
      allocations[sec_name] = {}
      alloc_ids[sec_name] = {}
      for sa in sec.get('subtopic_allocations', []):
          allocations[sec_name][sa['subtopic']] = sa['q_count']
          # subtopic_id is the JOIN KEY (v3.4 contract). Blueprint v1.7+ always
          # carries it. If absent (legacy blueprint) → contract gate S3-CONTRACT
          # will HARD STOP; do not silently fall back to name matching.
          sid = sa.get('subtopic_id')
          alloc_ids[sec_name][sid] = {'q_count': sa['q_count'],
                                      'display_name': sa['subtopic']}

  # ALSO build batch_ranges from sections[]:
  # batch_ranges = {section_name: [q_start, q_end]}
  batch_ranges = {}
  for s in sections:
      batch_ranges[s['name']] = s['q_range']

  # Optional per-mock fields (present only in some blueprint versions):
  english_structure = mock_entry.get('english_structure', {})
  image_subtopics   = mock_entry.get('image_subtopics', {})

  # dedup_partition: may be at mock level or absent (use defaults if missing):
  dedup_partition = mock_entry.get('dedup_partition', {
      'rc_narrative_topic': None,
      'rc_report_topics': [],
      'cloze_topic': None,
      'math_seed_base': N * 100,
      'reasoning_seed_base': N * 50
  })

  diff_entry = next((d for d in difficulty_schedule if d['mock'] == N), {})
  n_simple = diff_entry.get('simple', total_questions // 4)
  n_medium = diff_entry.get('medium', total_questions // 2)
  n_hard   = diff_entry.get('hard',   total_questions // 4)

  # v5.2 SCHEDULE-FIRST difficulty assignment + capture (Contract_QuestionMetadataIndex v1.0).
  # n_simple/n_medium/n_hard are the QUOTA for this mock. Difficulty is assigned SCHEDULE-FIRST:
  # every question is placed into one band to fill the quota EXACTLY; PYQ calibration (S7 CHECK)
  # chooses WHICH questions take Simple vs Hard, and difficulty is also a generation lever
  # (number size / step count / directness). Each question's band is recorded as the CANONICAL
  # label from blueprint.difficulty_labels and passed to write_q_to_sidecar(difficulty=...) per
  # question — NEVER written to the docx. At Final Assembly the labels roll up into
  # registry.question_index (S13-4); G-QINDEX (S12-NEW-26) then requires their distribution to
  # EQUAL {n_simple, n_medium, n_hard} exactly — satisfiable by construction under this rule.
  # v5.14: difficulty stays SCHEDULE-FIRST and untouched. The Option-3 JOINT solve adds a
  # near-ORTHOGONAL second axis (Axis-2 stem structure, S7-AXIS): a MATCH/A-R/… question can be
  # any difficulty band, so both the difficulty quota AND the Axis-2 window target are met
  # together. On a genuine conflict the tie-break bends AXIS-2, never difficulty (which G-QINDEX
  # still enforces exactly). See S7-AXIS for the full contract.
  difficulty_labels = bp.get('difficulty_labels', ['Easy', 'Medium', 'Hard'])
  def canonical_difficulty(sched_key):
      # sched_key in {'simple','medium','hard'} -> canonical label. Honours an exam-overridden
      # 3-band difficulty_labels positionally; falls back to the fixed alias otherwise. (A non-
      # 3-band label set also needs an adapted schedule -- out of scope; 3-band fully supported.)
      _alias = {'simple': 'Easy', 'medium': 'Medium', 'hard': 'Hard'}
      if len(difficulty_labels) == 3:
          return {'simple': difficulty_labels[0], 'medium': difficulty_labels[1],
                  'hard': difficulty_labels[2]}.get(sched_key, _alias.get(sched_key, sched_key))
      return _alias.get(sched_key, sched_key)
  ```

  LOAD ExplainLearnings for quality constraints (GAP-07 fix):
  ```python
  learnings_bans = []  # Extra banned patterns from prior Explain sessions
  for learn_file in [f'/home/claude/{EXAM}_ExplainLearnings.md',
                     f'/home/claude/{EXAM}_ExplainAuditLearnings.md']:
      if os.path.exists(learn_file):
          content = open(learn_file, encoding='utf-8').read()
          # Extract BANNED/VERIFIED DEFECT entries and add to generation bans
          bans = re.findall(r'(?:BANNED|VERIFIED DEFECT):\s*(.+)', content)
          learnings_bans.extend(bans)
  # learnings_bans added to quality gate checks during generation
  ```

## S3-3 — Load section_rules.md — read ALL fields

  (Unchanged from v1.0 — see §3 S3-3 in v1.0 spec for full field list)

  Parse EXAM_STRUCTURE header block; per-section blocks; per-subtopic blocks.
  Regex: locate '--- Subtopic: [re.escape(S)] ---', stop at next '--- Subtopic:'
  or '=== SECTION:'.

  ALSO EXTRACT (used by S7-20, S7-21):
    Per-section content-ban directives (e.g. easy-ban types for a fact-recall section)
    Per-section mandatory-area/topic directives (ALL declared — count is data, never fixed)
    Per-section cluster-ban directives (adjacency constraints for a language section)
    All read by section name from section_rules.md; empty ⇒ vacuous no-op.

## S3-4 — Load registry.json — integrity check (non-blocking)

  ```python
  import re as _re_pid
  reg = json.load(open(f'/home/claude/{EXAM}_registry.json'))

  # C2 (v5.21): UNIVERSAL paper identity. paper_id comes from THIS paper's blueprint.mocks[]
  # entry (C1/Blueprint v1.29 added it); fallback "MOCK:M{N:02d}" for pre-C1 blueprints.
  # paper_index = its numeric suffix (mock → == N; scoped "SUBJ:Physics:03" → 3), used only for
  # the window index. For a mock, paper_id == "MOCK:M{N:02d}" and paper_index == N, so EVERY
  # downstream value (window, filename, registry integers) is bit-identical to pre-C2.
  _this_paper = next((mk for mk in bp.get('mocks', []) if mk.get('mock') == N), None)
  paper_id    = (_this_paper or {}).get('paper_id', f"MOCK:M{N:02d}")
  paper_index = int(_re_pid.sub(r'\D', '', paper_id.rsplit(':', 1)[-1]) or N)

  # papers_completed is the generalised paper-identity ledger (C1); mocks_completed retained
  # for backward-compatibility (a legacy registry falls back to it).
  mocks_done   = reg.get('mocks_completed', [])
  papers_done  = reg.get('papers_completed', mocks_done)
  q_hashes     = reg.get('question_hashes', [])
  expected_cnt = len(papers_done) * total_questions

  # v5.14 THREE-AXIS: the WINDOW-level Axis-2 counts live in the registry (cross-mock;
  # batch_state.json is per-mock and cannot span a 10-mock window). Read the current
  # window's running counts; RESET when this paper opens a new window.
  _win = bp.get('batch_size_qs', 10)
  _cur_window = (paper_index - 1) // max(1, _win)   # C2: paper_index (== N for a mock)
  _reg_axis = reg.get('axis2_window', {})            # {'window': int, 'sections': {sec: {counts,...}}}
  if _reg_axis.get('window') != _cur_window:
      axis2_window_counts = {}                        # new window → fresh counts
  else:
      axis2_window_counts = dict(_reg_axis.get('sections', {}))
  # axis2_window_counts[section] = {'counts': {...}, 'neg_count': int, 'total': int}
  # Trackers are built per section from this + blueprint axis_schedule (see S7-AXIS), mutated
  # during generation, and committed back to reg['axis2_window'] at Final Assembly (S13-4).

  # NON-BLOCKING — inconsistent registry → WARN, proceed with dedup_partition:
  if len(q_hashes) != expected_cnt:
      print(f"WARN: Registry inconsistent ({len(q_hashes)} hashes, "
            f"expected {expected_cnt}). G-DUP will be environment-WARN only.")

  # INITIALISE pending_registry (v2.0 GAP-19 fix — explicit init here):
  pending_registry = {
      'question_hashes': [],
      'stem_texts': [],
      'semantic_tuples': [],
      'semantic_usage': [],
      'image_phashes': [],
      'image_sources_used': [],
      'ga_facts_used': [],
      'passage_topics': [],
      'cloze_topics': [],
      'vocab_words_used': [],
      'idioms_used': [],
      'grammar_rules_used': [],
      'computer_facts': [],
      'numeric_seeds': [],
      'analogy_schemes': [],
      'cause_effect_domains': [],
      'syllogism_domains': [],
      'option_sets': [],
  }
  # pending_registry commits to registry ONLY at Final Assembly (S13-4).
  # All dedup additions during generation go here, NEVER to registry directly.
  ```

## S3-5 — Registry snapshot

  ```python
  shutil.copy(f'/home/claude/{EXAM}_registry.json',
              f'/home/claude/{EXAM}_registry_snapshot.json')
  registry_snapshot = json.load(open(f'/home/claude/{EXAM}_registry_snapshot.json'))

  # D (v5.23): build an IN-MEMORY dedup index PARTITIONED by subtopic_id, so a lookup for a
  # subtopic scans only that subtopic's prior entries — O(shard) instead of O(all) — which
  # bounds cost for large exams (100k+ questions). CORRECTNESS-NEUTRAL: the stored registry is
  # UNCHANGED (flat lists), and only the naturally subtopic-keyed fields are indexed
  # (semantic_usage keyed by 'subtopic_id'; semantic_tuples keyed by their first element,
  # [subtopic, approach, values]). L1 (question_hashes / stem_texts) stays GLOBAL — a verbatim
  # duplicate must be caught across subtopics, so it is deliberately NOT sharded.
  def _build_subtopic_index(snap):
      idx = {'semantic_usage': {}, 'semantic_tuples': {}}
      for u in snap.get('semantic_usage', []):
          idx['semantic_usage'].setdefault(u.get('subtopic_id'), []).append(u)
      for t in snap.get('semantic_tuples', []):
          sid = (t[0] if isinstance(t, (list, tuple)) and t else
                 (t.get('subtopic') if isinstance(t, dict) else None))
          idx['semantic_tuples'].setdefault(sid, []).append(t)
      return idx

  SUBTOPIC_INDEX = _build_subtopic_index(registry_snapshot)

  def subtopic_usage(snap, sid):
      """D: prior semantic_usage for ONE subtopic, from the index when available (built from
      this same snap), else an O(n) filter — identical membership either way."""
      if snap is registry_snapshot:
          return SUBTOPIC_INDEX['semantic_usage'].get(sid, [])
      return [u for u in snap.get('semantic_usage', []) if u.get('subtopic_id') == sid]
  ```
  Guard script uses snapshot. Live registry never modified during generation.

## S3-6 — ExamCode cross-verification

  ```python
  bp_code  = bp['exam_code']
  reg_code = reg.get('exam_code', bp_code)
  assert bp_code == EXAM, \
      f"HARD STOP: trigger ExamCode '{EXAM}' != blueprint '{bp_code}'"
  assert bp_code == reg_code, \
      f"HARD STOP: blueprint exam_code '{bp_code}' != registry '{reg_code}'"
  ```

## S3-7 — Blueprint version compatibility check

  ```python
  # v5.6: minimum-version check uses TUPLE comparison (not string) so "1.10" > "1.7"
  # is correct. v1.7 is the floor (subtopic_id contract); any version >= 1.7 is accepted.
  MIN_BLUEPRINT_VERSION = (1, 7)
  def _ver_tuple(v):
      """Parse a version string like '1.7' or '1.14' into a comparable tuple."""
      try:
          return tuple(int(x) for x in str(v).split('.'))
      except (ValueError, AttributeError):
          return (0,)
  if _ver_tuple(blueprint_version) < MIN_BLUEPRINT_VERSION:
      raise SystemExit(
          f"HARD STOP: blueprint_version '{blueprint_version}' < minimum "
          f"'{'.'.join(str(x) for x in MIN_BLUEPRINT_VERSION)}'. "
          f"Regenerate the blueprint with Framework_Blueprint v1.7+ (subtopic_id contract required).")
  ```

## S3-8 — Subtopic join via subtopic_id (v3.4 — CONTRACT GATE, replaces string-match)

  v3.4 CHANGE: Step 7 no longer matches subtopics by display-name string. It
  joins blueprint ↔ section_rules ON subtopic_id, the stable key minted by Step 0.
  This permanently fixes the ~70% name-mismatch that caused false "subtopic
  unrecognised" and false "mandatory subtopic absent" hard stops.

  ```python
  # Load the Step 0 manifest (authoritative id registry). REQUIRED.
  manifest_path = f'/home/claude/{EXAM}_subtopic_manifest.json'
  if not os.path.exists(manifest_path):
      # Try project dir as a fallback location
      alt = f'/mnt/project/{EXAM}_subtopic_manifest.json'
      if os.path.exists(alt):
          shutil.copy(alt, manifest_path)
  if not os.path.exists(manifest_path):
      raise SystemExit(
          f"HARD STOP (S3-8 contract): {EXAM}_subtopic_manifest.json not found. "
          f"Step 0 publishes it and the user uploads it to the {EXAM} project "
          f"Files section alongside section_rules.md. Upload it, then retry.")
  manifest = json.load(open(manifest_path, encoding='utf-8'))
  MANIFEST_IDS = manifest['subtopics']           # id -> {display_name, section, ...}

  # Build the section_rules id index: parse subtopic_id: from each block.
  # (Step 0 v2.4+ writes 'subtopic_id:' as the first field of every block.)
  sr_block_ids = set(re.findall(r'^subtopic_id:\s*(\S+)\s*$', sr_text, re.MULTILINE))

  # CONTRACT GATE — every blueprint id must exist in BOTH the manifest AND
  # section_rules. A missing id = HARD STOP naming the exact id (no silent fallback).
  contract_failures = []
  legacy_blueprint = False
  for sec_name, id_map in alloc_ids.items():
      for sid in id_map:
          if sid is None:
              legacy_blueprint = True
              continue
          if sid not in MANIFEST_IDS:
              contract_failures.append(f"{sid}  (not in manifest)")
          elif sid not in sr_block_ids:
              contract_failures.append(f"{sid}  (in manifest, missing from section_rules)")

  if legacy_blueprint:
      raise SystemExit(
          "HARD STOP (S3-8 contract): this blueprint has subtopic_allocations "
          "without 'subtopic_id'. It predates the v1.7 contract. Regenerate the "
          "blueprint with Framework_Blueprint v1.7+ (which reads the Step 0 "
          "manifest and emits subtopic_id), OR run the one-time migration to add "
          "ids. Step 7 will not string-match — it requires ids.")
  if contract_failures:
      raise SystemExit(
          "HARD STOP (S3-8 contract): these blueprint subtopic_ids are not "
          "joinable. Re-run Step 0 (manifest+section_rules) and/or Step 1 so all "
          "three agree:\n  - " + "\n  - ".join(sorted(set(contract_failures))))

  # Past the gate: every id joins cleanly. Resolve each id to its section_rules
  # block for pattern guidance (the join itself — no string matching anywhere).
  def sr_block_for_id(sid):
      # Split section_rules into subtopic blocks; return the block whose
      # 'subtopic_id:' line equals sid. This is the join (id → pattern block).
      blocks = re.split(r'\n--- Subtopic:', sr_text)
      for b in blocks:
          if re.search(r'^\s*subtopic_id:\s*' + re.escape(sid) + r'\s*$', b, re.MULTILINE):
              return b
      return None
  ```

  NOTE: sr_block_ids (built above via re.findall) and sr_block_for_id() both key
  on the SAME 'subtopic_id:' line that Step 0 emits as the first field of every
  block. The contract gate guarantees every blueprint id is in sr_block_ids
  before any sr_block_for_id() lookup runs, so a None return is impossible here.

  RESULT: alloc_ids[section][subtopic_id] is the authoritative allocation; each id
  resolves to exactly one section_rules block via sr_block_for_id(). The old
  name-based mismatch list is gone — joins are exact by construction.

## S3-9 — Section allocation sum verification

  ```python
  for section in sections:
      sec_name = section['name']
      expected = section['total_qs']
      actual   = sum(allocations.get(sec_name, {}).values())
      if actual != expected:
          raise SystemExit(
              f"HARD STOP: Section '{sec_name}' allocations sum={actual}, "
              f"expected={expected}. Blueprint may be corrupt or wrong mock.")
  ```

## S3-10 — Audit script self-test (Layer 2 — when audit.py exists)

  ```python
  if AUDIT_AVAILABLE:
      import subprocess
      result = subprocess.run(
          ['python3', f'/home/claude/{EXAM}_mock_test_audit.py', '--self-test'],
          capture_output=True, text=True
      )
      if result.returncode != 0:
          raise SystemExit(
              f"HARD STOP: Audit script self-test failed.\n{result.stdout}\n{result.stderr}")
      print(f"Audit script self-test: {result.stdout.strip()}")
  else:
      print("Audit script not available. Manual gate checklist (S4-11) will be used.")
  ```

## S3-11 — Read structural changes and deprecated formats

  From STRUCTURAL_CHANGES_BY_YEAR and DEPRECATED_FORMAT flags in section_rules.md.
  Build `deprecated_formats = {subtopic: [format_types]}` dict.
  Store ALL FIGURAL_BANNED flags (per-section and per-subtopic).

  v5.13 — FIGURAL_BANNED ↔ REPLACEMENT_RULE consistency (HS-16):
  After storing FIGURAL_BANNED flags, for each subtopic allocated in this
  mock where FIGURAL_BANNED is True, verify that section_rules contains a
  REPLACEMENT_RULE entry for it, pointing to a valid format=TEXT
  subtopic_id (in the same section, or in any section if the entire
  section is FIGURAL_BANNED). If REPLACEMENT_RULE is missing, empty, or
  points to a nonexistent subtopic_id → HS-16 HARD STOP:
  "FIGURAL_BANNED subtopic [id] has no valid REPLACEMENT_RULE. S7-NEW-B
  OPTION B replacement will fail. Add REPLACEMENT_RULE to section_rules
  before proceeding."
  If no subtopic in this mock has FIGURAL_BANNED: skip silently.

## S3-12 — Read none_of_above_permitted per section

  `none_of_above_map = {section_name: bool}` — default False if not found.
  v4.2 — this map is no longer read-only: gate G-OPTREF (S12-NEW-15) and rule
  R-OPTREF use it to ENFORCE that any stem referencing a terminal/escape option
  ("None of these", "No error → last option", "No improvement", "All/Both/Neither")
  actually contains that option, and only where the section permits it. Also read
  any per-section/per-subtopic escape-token wording from section_rules (exam-
  agnostic) so G-OPTREF matches the exam's own phrasing.

## S3-13 — Build answer position budget (PRE-Q1 — v2.0 GAP-08 fix)

  CRITICAL: Budget MUST be built before Q1, not post-generation.
  Assign answer positions for ALL N questions before generating any content.

  ```python
  import random

  def build_answer_budget(total_questions, sections, options_count=4,
                          msq_positions=None, nat_positions=None):
      """
      Build K-BAL balanced, K-PAT compliant answer sequence.
      K-BAL: 20-30% per option globally, 15-35% per section.
      K-PAT: max run of 2 consecutive identical answers GLOBALLY
             (including cross-section boundaries).
      v4.5: MSQ (answer_cardinality=='multi') Q positions are EXCLUDED from the single-position
      pool exactly like fixed_set positions — their answer is a SET, so single-position
      K-BAL share and K-PAT "run of identical answers" are undefined for them. The MSQ
      builder picks each set independently (subject to G-MSQ-SET/CARD); the budget leaves
      those positions as None. msq_positions = set of 1-based Q numbers whose subtopic
      answer_cardinality=='multi' (empty/None ⇒ fully dormant, identical to v4.4).
      v4.7 (ND8): NAT (answer_type=='numerical') Q positions are EXCLUDED on the SAME basis —
      a NAT answer is a typed VALUE, not an option position, so K-BAL share / K-PAT run are
      equally undefined. nat_positions = set of 1-based Q numbers whose subtopic
      answer_type=='numerical' (empty/None ⇒ dormant). excluded = fixed ∪ msq ∪ nat.
      v4.7 (ND12): under heavy exclusion (e.g. a 30-40% NAT+MSQ GATE paper) n_free can be
      small enough that an exact 20-30% per-option band is INFEASIBLE. In that regime the
      K-BAL band DEGRADES TO A WARNING (best-effort balance) instead of an assert-crash; the
      K-PAT run-cap still applies. Single-answer exams (n_free == total_questions) are
      unaffected — the band is trivially satisfiable exactly as in v4.4.
      """
      # Identify fixed-set Q positions (excluded from balance pool)
      # (detect from section_rules.md wrong_option_structure.type == fixed_set)
      fixed_positions = set()  # populated from subtopic analysis
      msq_positions   = set(msq_positions or ())   # v4.5: multi-answer Q positions
      nat_positions   = set(nat_positions or ())   # v4.7: numerical-answer Q positions
      excluded        = fixed_positions | msq_positions | nat_positions

      n_free = total_questions - len(excluded)
      target = n_free // options_count

      # Build balanced sequence with K-PAT max-run=2:
      sequence = []
      option_counts = {i: 0 for i in range(1, options_count+1)}
      last_two = []

      for _ in range(n_free):
          # Available options: not creating a run of 3
          available = list(range(1, options_count+1))
          if len(last_two) == 2 and last_two[0] == last_two[1]:
              forbidden = last_two[0]
              available = [x for x in available if x != forbidden]

          # Prefer under-represented options (for K-BAL):
          min_count = min(option_counts[o] for o in available)
          preferred = [o for o in available if option_counts[o] == min_count]
          choice = random.choice(preferred)

          sequence.append(choice)
          option_counts[choice] += 1
          last_two = (last_two + [choice])[-2:]

      # Validate K-BAL (only over the single-answer free pool):
      # v4.7 ND12: the exact band is only ENFORCEABLE when the free pool is large enough to
      # hold it — the tightest option share is 1/n_free, so a band floor of 20% needs
      # n_free ≥ ~ 4·options_count for every option to be placeable inside 20-30%. Below that
      # threshold (heavy NAT+MSQ exclusion) we WARN and keep the best-effort balance instead
      # of asserting. At/above it we assert exactly as before (no behaviour change for the
      # single-answer case, where n_free == total_questions).
      KBAL_MIN_FREE = 4 * options_count
      if n_free >= KBAL_MIN_FREE:
          for opt, cnt in option_counts.items():
              pct = cnt / n_free * 100
              assert 20 <= pct <= 30, \
                  f"K-BAL failed: option {opt} at {pct:.1f}% (need 20-30%)"
      elif n_free:
          for opt, cnt in option_counts.items():
              pct = cnt / n_free * 100
              if not (20 <= pct <= 30):
                  print(f"K-BAL degraded (n_free={n_free} < {KBAL_MIN_FREE} after "
                       f"fixed/MSQ/NAT exclusion): option {opt} at {pct:.1f}% — best-effort "
                       f"balance kept (band un-enforceable on a small free pool; K-PAT holds).")

      # Assign to Q positions (skip excluded = fixed_set ∪ MSQ ∪ NAT):
      budget = {}
      seq_idx = 0
      for q in range(1, total_questions + 1):
          if q in excluded:
              budget[str(q)] = None  # fixed: from option content; MSQ: set; NAT: typed value
          else:
              budget[str(q)] = sequence[seq_idx]
              seq_idx += 1

      return budget

  # v4.5: msq_positions = the set of Q numbers whose placed subtopic has
  # answer_cardinality=='multi'. Populated from the SAME subtopic→Q placement plan that
  # populates fixed_positions (whole-subtopic mode). Empty when blueprint multi_present is
  # false ⇒ build_answer_budget behaves exactly as v4.4. Defensive: if the placement plan
  # is not yet materialised at budget-build time, msq_positions stays empty and the MSQ
  # builder simply does not consume its budget slot (it self-assigns the set), so K-BAL/
  # K-PAT are never corrupted by a multi Q either way.
  msq_positions = set()
  if multi_present:
      if _position_based_typing:
          # v5.X: for position-based exams, MSQ positions come from marking_scheme Q-ranges,
          # not from per-subtopic answer_cardinality. Every Q in an MSQ range is MSQ regardless
          # of which subtopic is placed there.
          msq_positions = {q for q in range(1, total_questions + 1) if _type_for_q(q) == 'MSQ'}
      else:
          multi_ids = {sid for sid, am in answer_cardinality_by_id.items() if am == 'multi'}
          try:
              # subtopic_by_qnum[q] = subtopic_id assigned to Q q (same map fixed_positions uses)
              msq_positions = {q for q, sid in subtopic_by_qnum.items() if sid in multi_ids}
          except NameError:
              msq_positions = set()   # plan not materialised yet → MSQ Qs self-skip the budget
  # v4.7: nat_positions = the set of Q numbers whose placed subtopic has
  # answer_type=='numerical'. Same placement plan, same dormancy/defensive semantics as MSQ.
  # Empty when blueprint nat_present is false ⇒ budget identical to v4.6.
  nat_positions = set()
  if nat_present:
      if _position_based_typing:
          # v5.X: for position-based exams, NAT positions come from marking_scheme Q-ranges.
          nat_positions = {q for q in range(1, total_questions + 1) if _type_for_q(q) == 'NAT'}
      else:
          nat_ids = {sid for sid, at in answer_type_by_id.items() if at == 'numerical'}
          try:
              nat_positions = {q for q, sid in subtopic_by_qnum.items() if sid in nat_ids}
          except NameError:
              nat_positions = set()   # plan not materialised yet → NAT Qs self-skip the budget
  answer_budget = build_answer_budget(total_questions, sections,
                                      msq_positions=msq_positions,
                                      nat_positions=nat_positions)
  budget_path = f'/home/claude/{EXAM}_M{N}_answer_budget.json'
  json.dump({'positions': answer_budget}, open(budget_path, 'w'))
  # All SINGLE-answer questions read their correct-answer position from this budget.
  # Content generation fills the PRE-ASSIGNED slot with the correct answer.
  # v4.5: MULTI (MSQ) questions have budget[str(q)]==None — they SELF-ASSIGN the correct
  # set S (subject to R-ANSWER multi + G-MSQ-SET/CARD) and never read a single position.
  ```

## S3-14 — Initialise answer key sidecar (v2.0 GAP-18 fix)

  ```python
  answer_key_path = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  if not os.path.exists(answer_key_path):
      # v4.5: msq_meta carries the MSQ config (from blueprint) so the gate sweep can
      # validate MSQ keys with NO blueprint dependency at audit time. All values are
      # inert when multi_select_allowed is false. _mc = blueprint['msq_contract'] (v1.8).
      # msq_allow_aota (D5) is a generation-time policy read directly from section_rules
      # EXAM_STRUCTURE (a Step 7 input); default false. (Cleaner long-term: carry it in
      # blueprint['msq_contract'] from Step 0/Step 1 — a one-line addition each.)
      # v5.4 FIX: removed all 'bp' in dir() guards — bp is ALWAYS loaded at S3-2 before
      # S3-14 runs. The 'in dir()' idiom was a cosmetic guard that would silently activate
      # wrong defaults if the code were ever refactored into a function. Direct access is safe.
      _mc = bp.get('msq_contract', {})
      _nc = bp.get('nat_contract', {})                             # v4.7 NAT contract
      # v5.4 FIX: was 'section_rules_text' (undefined) — silently defaulted False via
      # NameError catch, so msq_allow_aota was ALWAYS ignored. Now reads sr_text (S3-2).
      _aota = bool(re.search(r'^\s*msq_allow_aota\s*:\s*true\s*$', sr_text, re.M | re.I))
      json.dump({
          "answers": {}, "sources": {},
          "msq_meta": {
              "multi_select_allowed": bool(bp.get('multi_select_allowed', False)),
              "total_options"       : int(bp.get('total_options', 4)),
              "msq_k_mode"          : _mc.get('msq_k_mode', 'n/a'),
              "msq_k"               : _mc.get('msq_k', None),
              "msq_allow_aota"      : _aota,
          },
          # v4.7 NAT meta — the answer model for the gate sweep (G-NAT-ANSWER) and Step 4.
          # Inert when nat_allowed=false (nat_present false ⇒ no NAT Qs reference it).
          "nat_meta": {
              "nat_allowed"     : bool(bp.get('nat_allowed', False)),
              "nat_answer_type" : _nc.get('nat_answer_type', 'real'),
              "nat_tolerance"   : _nc.get('nat_tolerance', '0'),
              "nat_instruction" : _nc.get('nat_instruction', 'Enter your answer as a numerical value.'),
          }
      }, open(answer_key_path, 'w'))
  # Written per-question during generation (S7 after each Q accepted)
  # NEVER at end — incremental, per-question writes only
  ```

## S3-15 — Build SC manifest

  Build from subtopic_list[] and dedup_partition. Register all linked groups.

## S3-16 — Build batch plan → write batch_state.json

  ```python
  batch_plan = []
  batch_id = 1
  for sec in sections:
      sec_name = sec['name']
      q_start = sec['q_range'][0]
      q_end   = sec['q_range'][1]
      q = q_start
      while q <= q_end:
          batch_q_end = min(q + 9, q_end)  # max 10Q per batch
          batch_plan.append({
              'batch_id': batch_id,
              'section': sec_name,
              'q_start': q,
              'q_end': batch_q_end,
              'q_count': batch_q_end - q + 1,
              'is_final': False
          })
          batch_id += 1
          q = batch_q_end + 1

  if batch_plan:
      batch_plan[-1]['is_final'] = True

  batch_state = {
      'exam_code': EXAM,
      'mock_n': N,
      'paper_id': paper_id,          # C2: universal identity (mock == "MOCK:M{N:02d}")
      'total_questions': total_questions,
      'batch_plan': batch_plan,
      'batches_completed': [],
      'current_batch': 1,
      'mechanics_used': {},
      'templates_used': {},
      'rotation_state': {},
      'passage_linked_qs': [],
      'cloze_linked_qs': [],
      'concept_ledger': [],          # v5.4 FIX: was missing from init (present in S4-3 schema)
      'presentation_ledger': [],     # v5.4 FIX: was missing from init (present in S4-3 schema)
      'figural_qs': {}               # v5.13: {qnum_str: {subtopic_id, image_role, rendered: bool}}
                                      # Populated at S3-18 from the figural manifest scan.
                                      # At generation time: set rendered=true after
                                      # add_figural_question() or add_figural_stem_question()
                                      # succeeds for that Q.
                                      # At gate check: any entry with rendered=false → HARD FAIL.
                                      # Empty {} when figural_present is False or no FIGURAL
                                      # subtopics exist in this mock.
  }
  json.dump(batch_state, open(f'/home/claude/{EXAM}_M{N}_batch_state.json', 'w'))
  ```

## S3-17 — Mandatory subtopic + alternation pre-check (v3.4 — manifest-driven)

  v3.4 CHANGE: This check no longer uses hardcoded literal strings like
  'Mensuration 3D' / 'Direction Sense'. Those caused false hard stops because the
  blueprint used different (granular) display names. It now reads the STRUCTURED
  mandate data from the Step 0 manifest and checks by subtopic_id. Fully
  exam-agnostic — zero subtopic names hardcoded.

  ```python
  MANDATORY_IDS = set(manifest.get('mandatory_every_mock', []))
  ALT_GROUPS    = manifest.get('alternation_groups', {})   # group -> [ids]
  MANDATORY_GROUPS = manifest.get('mandatory_groups', {})  # v5.0 group -> {members:[ids], min}
  MIN_COUNTS       = manifest.get('min_counts', {})        # v5.0 id -> k
  # manifest.cadence_windows is INTENTIONALLY NOT checked here. Cadence is a CROSS-mock
  # constraint (>=1 every N mocks) and is unobservable from a single mock; it is enforced
  # solely by Step 1 RULE M5 (full-series pass). A Step 7 cadence gate would be a category
  # error and would false-stop every legitimately-skipped mock. Do not add one.

  # Flatten ids AND total q_counts allocated in THIS mock (across sections):
  mock_ids = set()
  mock_counts = {}
  for sec_name, id_map in alloc_ids.items():
      mock_ids |= set(id_map.keys())
      for sid, info in id_map.items():
          mock_counts[sid] = mock_counts.get(sid, 0) + info['q_count']

  problems = []

  # CHECK 1 — mandatory_every_mock: every mandated id must be present this mock.
  for mid in MANDATORY_IDS:
      if mid not in mock_ids:
          disp = MANIFEST_IDS.get(mid, {}).get('display_name', mid)
          problems.append(f"MANDATORY subtopic absent: {mid} ('{disp}')")

  # CHECK 2 — alternation groups: at most ONE member per mock.
  for group, members in ALT_GROUPS.items():
      present = [m for m in members if m in mock_ids]
      if len(present) > 1:
          disps = [MANIFEST_IDS.get(m, {}).get('display_name', m) for m in present]
          problems.append(
              f"ALTERNATION violated: group '{group}' has {len(present)} members "
              f"in this mock ({', '.join(disps)}); at most 1 allowed.")

  # CHECK 3 — mandatory_groups (GROUP-PRESENCE, v5.0/Issue 2b): >=min members present.
  for group, spec in MANDATORY_GROUPS.items():
      members = spec.get('members', [])
      need    = spec.get('min', 1)
      have    = sum(1 for m in members if mock_counts.get(m, 0) > 0)
      if have < need:
          disps = [MANIFEST_IDS.get(m, {}).get('display_name', m) for m in members]
          problems.append(
              f"GROUP-PRESENCE violated: group '{group}' needs >={need} of "
              f"[{', '.join(disps)}] present, but only {have} in this mock.")

  # CHECK 4 — min_counts (MIN-COUNT, v5.0/Issue 2b): id must have >=k questions.
  for mid, k in MIN_COUNTS.items():
      c = mock_counts.get(mid, 0)
      if c < k:
          disp = MANIFEST_IDS.get(mid, {}).get('display_name', mid)
          problems.append(
              f"MIN-COUNT violated: {mid} ('{disp}') has {c}Q allocated, needs >={k}.")

  if problems:
      raise SystemExit(
          "HARD STOP (S3-17): blueprint mandate/alternation violations for Mock "
          f"{N}:\n  - " + "\n  - ".join(problems) +
          "\n\nThese are BLUEPRINT defects (Step 1 should prevent them at build "
          "time under Framework_Blueprint v1.11 RULE M1/M2/M4/M5/M6). Fix: "
          "regenerate the blueprint with v1.11 (enforces mandates by construction), "
          "or correct this mock's allocation, then retry. Step 7 does not auto-edit "
          "the blueprint.")
  ```

  NOTE ON THE OLD FALSE ALARMS: under the manifest contract, "Mensuration 3D
  absent" can only fire if the manifest actually flags a 3D-mensuration id as
  mandatory_every_mock AND no such id is in the mock. Granular names like
  "Right Circular Cone" now resolve through ids, so a present-but-differently-
  named mandatory subtopic is correctly recognised and does NOT false-stop.

## S3-18 — Display session start summary + batch plan

  Print in chat after all checks pass:

  ```
  === MockCreate — Session Start ===
  Exam     : [exam_name] ([ExamCode])
  Mock     : M[N] of [total_mocks]
  Questions: [total_questions]
  Sections : [count] | Difficulty: S=[n_simple] M=[n_medium] H=[n_hard]
  Formats  : PASSAGE=[T/F] FIGURAL=[T/F] DI=[T/F]
  Guard    : [Audit script available / Manual checklist mode]
  Registry : [len(mocks_done)] mocks completed
  ──────────────────────────────────────────────────
  BATCH PLAN:
  Batch | Section          | Q-Range  | Qs
  ──────────────────────────────────────────────────
  1     | [Section 1]      | Q1–Q10   | 10
  2     | [Section 1]      | Q11–Q20  | 10
  ...
  N     | [Last Section]   | Qx–Qy    |  z   ← FINAL BATCH
  ──────────────────────────────────────────────────

  FIGURAL MANIFEST (v5.13 — when figural_present is True):
  ──────────────────────────────────────────────────
  Scan all subtopic_allocations for this mock and list every subtopic
  whose section_rules format == FIGURAL. For each, read image_role from
  PYQ_IMAGE_ANALYSIS (default 'stem_and_options' if absent):

  FIGURAL Qs (matplotlib rendering required — S7-NEW-B OPTION A):
  Batch | Q#   | Subtopic ID          | image_role       | Rendering
  ──────────────────────────────────────────────────────────────────────
  [b]   | Q[n] | [subtopic_id]        | stem_and_options | problem PNG(s) + [k] option PNGs
  [b]   | Q[m] | [subtopic_id]        | stem_only        | problem PNG(s) + TEXT options
  [b]   | Q[p] | [subtopic_id]        | options_only     | TEXT stem + [k] option PNGs
  ...
  ──────────────────────────────────────────────────────────────────────
  Total: [count] figural Qs across [b_count] batches.
  Helper dispatch: stem_and_options/options_only → add_figural_question()
                   stem_only                     → add_figural_stem_question()
  Text descriptions are BANNED (S7-NEW-B OPTION C).

  Also populate batch_state.figural_qs with one entry per Q listed above:
    figural_qs[str(qnum)] = {subtopic_id, image_role, rendered: false}

  If figural_present is False: omit this table entirely.
  The Q# assignment is determined by the subtopic's position within the
  section's Q-range (subtopics assigned to Q positions in blueprint order).
  This manifest is INFORMATIONAL — the authoritative format source remains
  section_rules format field per subtopic_id.
  ──────────────────────────────────────────────────

  Answer budget: built and written to [EXAM]_M[N]_answer_budget.json
  All checks passed. Type 'continue' to begin Batch 1.
  ```
  STOP HERE. Wait for "continue".

## S3-19 — HARD STOP conditions

  HS-1: Any mandatory file missing from /mnt/project/
  HS-2: Section allocation sums mismatch
  HS-3: ExamCode mismatch between trigger/blueprint/registry
  HS-4: paper_id already in registry.papers_completed (legacy: Mock N in mocks_completed)
  HS-5: Audit script self-test fails (if audit.py present)
  HS-6: blueprint.json invalid JSON
  HS-7: section_rules.md empty
  HS-8: Mandatory subtopic absent from blueprint — detected by id via manifest
        mandatory_every_mock (S3-17), NOT by hardcoded name.
  HS-9: subtopic_manifest.json missing (S3-8 contract gate).
  HS-10: A blueprint subtopic_id not found in manifest or section_rules
        (S3-8 contract gate) — names drifted; re-run Step 0/Step 1.
  HS-11: Legacy blueprint without subtopic_id fields (S3-8) — regenerate with
        Framework_Blueprint v1.7+ or run the one-time id migration.
  HS-12: Alternation group has 2+ members in one mock (S3-17).
  HS-13: mandatory_groups group has <min members present in one mock (S3-17 CHECK 3,
        Issue 2b). Blueprint defect — Step 1 RULE M4 should prevent by construction.
  HS-14: min_counts id has <k questions in one mock (S3-17 CHECK 4, Issue 2b).
        Blueprint defect — Step 1 RULE M6 should prevent by construction.
  HS-15: (v5.13) figural_present is True but zero subtopics in this mock have
        section_rules format==FIGURAL. Either the blueprint flag is wrong
        (should be False) or section_rules format fields are stale.
        Non-blocking WARN (not HARD STOP): figural_present may be series-level
        — this specific mock simply has no figural Qs while others in the series do.
  HS-15a: (v5.13 REVERSE) figural_present is False but ≥1 subtopic in this mock
        has section_rules format==FIGURAL. The blueprint flag is wrong — should be
        True. Non-blocking WARN: the FORMAT DISPATCH (S4-7) and G-FIGTEXT (S12-NEW-5)
        still operate independently of figural_present and will attempt image
        generation. But the FIGURAL MANIFEST (S3-18) and CHECK 5 (S4-5) will be
        skipped, reducing early warning. Fix blueprint.json for the next series.
  HS-16: (v5.13) FIGURAL_BANNED subtopic has no valid REPLACEMENT_RULE. See S3-11.
        HARD STOP — S7-NEW-B OPTION B replacement will fail silently without it.


# ════════════════════════════════════════════════════════════════════════
# §4 — BATCH ARCHITECTURE (v3.0 — DEFINITIVE REWRITE)
# This is the single most critical section. Read every rule.
# ════════════════════════════════════════════════════════════════════════
#
# WHY THIS SECTION EXISTS:
#   In the M1 production failure, Claude generated all 100 questions in ONE
#   response instead of stopping after each 10-question batch. This section
#   makes that failure mechanically impossible by removing every ambiguity
#   and adding a self-check Claude must perform before ending each response.
#
# THE GOVERNING PRINCIPLE:
#   ONE BATCH = ONE RESPONSE. NO EXCEPTIONS EXCEPT THE FINAL BATCH.
#   A "batch" is at most 10 questions from a single section.
#   After delivering a batch, Claude's response ENDS. The next batch begins
#   only when the user sends "continue" / "go" / "next".

## S4-1 — What a batch is (precise definition)

  A batch is a unit of generation with these exact properties:
    - Contains AT MOST 10 questions (MAX_BATCH_SIZE = 10)
    - All questions come from ONE section (never spans two sections)
    - Has a fixed q_start and q_end read from batch_state.json
    - Is generated, gate-checked, delivered, then the response ENDS

  A batch is NEVER:
    - More than 10 questions
    - Questions from two different sections
    - Generated in the same response as another batch
    - Started without an explicit user "continue" (except Batch 1, which
      starts after the user types "continue" following session start)

## S4-2 — Batch plan computation (the ONLY source of batch boundaries)

  Built once at session start (S3-16). Written to batch_state.json.
  NEVER recomputed mid-session. NEVER derived from memory or "the last Q + 1".

  ALGORITHM (deterministic):
    MAX_BATCH_SIZE = 10
    batch_id = 1
    FOR each section in sections[] (ordered by q_range start ascending):
        q = section.q_range[0]
        WHILE q <= section.q_range[1]:
            batch_q_end = MIN(q + 9, section.q_range[1])
            record batch {batch_id, section, q_start=q, q_end=batch_q_end,
                          q_count = batch_q_end - q + 1, is_final=False}
            batch_id += 1
            q = batch_q_end + 1
    MARK the last batch in the list: is_final = True

  KEY PROPERTIES:
    - A section with 25 questions → batches of 10, 10, 5
    - The 5-question batch is the section remainder (always ≤ 10)
    - Sections never share a batch
    - Exactly one batch in the whole plan has is_final = True

## S4-3 — batch_state.json schema (the batch processing brain)

  ```json
  {
    "exam_code": "[ExamCode]",
    "mock_n": N,
    "paper_id": "MOCK:M0N",
    "total_questions": 100,
    "batch_plan": [
      {"batch_id": 1, "section": "Section_A", "q_start": 1, "q_end": 10,
       "q_count": 10, "is_final": false},
      {"batch_id": 2, "section": "Section_A", "q_start": 11, "q_end": 20,
       "q_count": 10, "is_final": false},
      ...
      {"batch_id": 10, "section": "Section_D", "q_start": 91, "q_end": 100,
       "q_count": 10, "is_final": true}
    ],
    "batches_completed": [],
    "current_batch": 1,
    "mechanics_used": {},
    "templates_used": {},
    "rotation_state": {},
    "passage_linked_qs": [],
    "cloze_linked_qs": [],
    "concept_ledger": [],
    "presentation_ledger": [],
    "figural_qs": {}
  }
  ```

  current_batch: the batch_id to generate next. Starts at 1.
  batches_completed: list of batch_ids whose questions are in the docx AND
                     passed gate checks AND were delivered. Updated ONLY
                     after present_files succeeds for that batch.
  concept_ledger: list of scenario_key strings already used in THIS mock
                  (DOUBT-3 / S6-3b RULE B). Checked before every new Q and
                  persisted across batches so no scenario repeats anywhere in
                  the paper. Each subtopic still produces EXACTLY its blueprint
                  q_count (RULE A) — distinct scenarios fill those N slots.
  presentation_ledger: list of "concept_group||presentation_key" strings already
                  used in THIS mock for CLASS-2/3 questions (DOUBT-4 / §6-3c
                  RULE C, v3.9). Checked at CHECK 1b and persisted/rehydrated like
                  concept_ledger so no two same-group questions LOOK alike across
                  batches or across a resume.

## S4-4 — The Batch Stop Law (B-1 through B-8 — ARCHITECTURAL, NON-NEGOTIABLE)

  These are not guidelines. They are the same class of rule as MANDATE 0.

  B-1: batch_state.json MUST exist and be valid before Q1 of any batch.
       If missing → rebuild from blueprint + existing docx (S4-12), then proceed.

  B-2: The q_start and q_end for the batch being generated come ONLY from
       batch_state.json batch_plan[current_batch - 1]. NEVER from memory.
       NEVER computed as "previous batch end + 1" without reading the file.

  B-3: Generate EXACTLY q_count questions for the current batch. Not one more.
       If current batch q_count is 5, generate 5 — even if it "feels" like
       there is room for 10. The plan is authoritative.

  B-4: AUTO-ADVANCE IS PERMANENTLY BANNED.
       After delivering a batch (present_files called), the response ENDS.
       FORBIDDEN in the same response after a batch delivery:
         - Generating the next batch's questions
         - "Let me now continue with Batch N+1..."
         - "I'll go ahead and generate the next section..."
         - A "preview" or "head start" on the next batch
         - ANY question content beyond the current batch
       The ONLY thing after present_files is the STOP line (S4-7 STEP E)
       and then the response ENDS.

  B-5: The next batch begins ONLY when the user's NEW message is a continue
       trigger ("continue" / "go" / "next", case-insensitive).
       Claude NEVER self-issues a continue. Claude NEVER assumes continue.

  B-6: batches_completed is updated (append current_batch's batch_id) and
       current_batch is incremented ONLY after present_files succeeds.
       This update is written to batch_state.json before the response ends.

  B-7: present_files is FORBIDDEN until the batch passes gate checks
       (Layer 2 audit script exit 0, OR Layer 1 manual checklist all-pass).

  B-8: The FINAL batch (is_final=True) is the ONLY batch that does NOT end
       with a continue prompt. It auto-triggers Final Assembly (§13) in the
       SAME response. See S4-9.

## S4-5 — Pre-batch self-check (MANDATORY before generating any batch)

  Before generating questions for a batch, Claude MUST silently verify:

    CHECK 1: Read batch_state.json. Confirm current_batch value.
    CHECK 2: Read batch_plan[current_batch - 1]. Get section, q_start, q_end, q_count.
    CHECK 3: Confirm this batch_id is NOT already in batches_completed.
             (If it is → the user re-triggered; advance to the true next batch.)
    CHECK 4: Confirm the user's last message was a continue trigger
             (or, for Batch 1, the continue following session start).
             If NOT a continue trigger → do NOT generate. Answer the user
             and re-show the continue prompt.
    CHECK 5: (v5.13) If any subtopic in this batch has section_rules
             format==FIGURAL (read by subtopic_id):
               Scan batch_state.figural_qs for Q numbers in this batch's range.
               For each found, read its image_role and print in chat:
                 "⚠ FIGURAL Qs in this batch:
                    Q.[x] ([subtopic_id]) — image_role=[role] → [helper name]
                    Q.[y] ([subtopic_id]) — image_role=[role] → [helper name]
                  matplotlib rendering required. Text descriptions BANNED (S7-NEW-B)."
               If FIGURAL_BANNED for any subtopic in this batch:
                 "Q.[z] ([subtopic_id]) — FIGURAL_BANNED → OPTION B replacement
                  using REPLACEMENT_RULE subtopic."
             If no FIGURAL subtopics in this batch: skip CHECK 5 silently.
             If figural_present is False: skip CHECK 5 silently.

  Only after all 5 checks pass does generation begin.

## S4-6 — The continue contract (exact behaviour)

  ACCEPTED CONTINUE TRIGGERS (case-insensitive, trimmed):
    "continue", "go", "next", "continue.", "go ahead", "next batch", "proceed"

  IF the user message IS a continue trigger:
    → Run S4-5 pre-batch self-check.
    → Generate the next batch.

  IF the user message is NOT a continue trigger (a question, a correction,
  a new instruction):
    → Do NOT generate a batch.
    → Address the user's message fully.
    → End the response with the standing continue prompt:
      "Ready for Batch [current_batch] → [section] Q[start]–Q[end] ([count]Q).
       Type 'continue' when ready."

  IF the user message is a correction to an already-delivered batch:
    → Apply the fix to that batch in the cumulative docx.
    → Re-run gate checks. Re-deliver via present_files.
    → Do NOT advance current_batch.
    → End with the continue prompt for the SAME next batch.

## S4-7 — Per-batch delivery protocol (the 6 steps — execute in order)

  STEP A — GENERATE: Produce exactly q_count questions for current_batch.
           Write them to the cumulative docx (append to prior batches' Qs).
           Write each question's answer to the sidecar immediately (S11-2).
           Apply ALL generation rules (§7), format rules (§8, §10),
           dedup (§6), self-containment (§9).

           FORMAT DISPATCH (v5.13 — per question, mandatory decision point):
             Read the subtopic's format from section_rules (by subtopic_id).
             IF format == FIGURAL:
               Read image_role from section_rules PYQ_IMAGE_ANALYSIS
               (default 'stem_and_options' if PYQ_IMAGE_ANALYSIS absent).

               ── FIGURE CONTENT PROFILE (v5.31, GAP-2026-07-26-003) ──────────
               Before generating, read the SEMANTIC half of PYQ_IMAGE_ANALYSIS —
               object_types, transformation_types, arrangement_types,
               complexity_dist — via bc.figural_generation_profile(). Until v5.31
               Step 7 read ONLY image_role, so Step 5 measured what the real
               figures CONTAIN and no step ever looked: the fields were written
               into section_rules and read by nothing. A generated figure could
               be a bar chart where every PYQ in that subtopic is a micrograph,
               and no gate would notice.

               profile = bc.figural_generation_profile(pyq_image_analysis)

               profile['mode'] decides how hard the constraint binds:
                 'dominant'  → 70% of generated figures use a type from
                               profile['dominant']; the remaining 30% draw from
                               profile['observed']. Never introduce a type that
                               appears in NEITHER list.
                 'observed'  → no type recurs often enough to be called dominant
                               (flat distribution, or too few observations).
                               Generate ACROSS profile['observed']; do not
                               fixate on any one type.
                 'unconstrained' → the profile is empty. Generate as before
                               v5.31, using subtopic semantics alone.

               EC-V18 — LEGACY TOLERANCE, NON-NEGOTIABLE. Roughly 200 exams hold
               section_rules written before v2.37 whose object_types are empty,
               and every one of them must keep working untouched. An absent or
               empty PYQ_IMAGE_ANALYSIS, an absent vision_status, and a
               vision_status of 'unavailable' ALL resolve to 'unconstrained'.
               This branch NEVER raises and NEVER blocks generation.

               vision_status == 'unavailable' deserves its own note: it means
               Step 5 queued figures and observed none, so an empty object_types
               there is a MEASUREMENT GAP, not evidence that the subtopic has no
               typical figure. Treating it as a constraint would generate against
               a fact nobody established. It is therefore 'unconstrained', and
               Step 5's QV-14 is what reports the gap.
               ────────────────────────────────────────────────────────────────

               IF image_role in ('stem_and_options', 'options_only'):
                 → Generate images via matplotlib (S7-NEW-B OPTION A):
                   stem_and_options: problem image(s) + option images
                   options_only: option images only (stem is text)
                 → Place via add_figural_question() (§10-S10-8)
                   (pass empty problem_pngs=[] for options_only)
               ELIF image_role == 'stem_only':
                 → Generate problem image(s) via matplotlib (S7-NEW-B OPTION A)
                 → Place via add_figural_stem_question() (§10-S10-8A)
                 → Options are TEXT — place via add_text_options() inside the helper
               ELSE (unknown role):
                 → Default to add_figural_question() (safest — forces all images)
                 → Log: "image_role unknown for [subtopic_id], defaulting to full"
               → Mark figural_qs[str(qnum)].rendered = true in batch_state
               → Record figural_qs[str(qnum)].object_type = the type this figure was
                 generated AS, drawn from profile['dominant'] / profile['observed']
                 (omit when mode == 'unconstrained'). Step 8 A-FIGPROFILE audits this
                 recorded intent against the same profile via the SAME engine function,
                 bc.check_figural_conformance — one rule, so the generator and its
                 auditor cannot drift apart.
               → Verify via view tool (9-item visual checklist, §10-S10-7)
               Text stem with add_question_stem() alone is BANNED for format=FIGURAL.
             IF stem_format_variant == 'match_the_following' (any TEXT/PASSAGE format):
               → Render via add_match_table() (§10-S10-3M): the Q.N-first bold instruction
                 paragraph, THEN a REAL Word table (List-I | List-II | … columns; unequal
                 columns blank-padded), THEN the pairing-quad options. Pass the List columns +
                 options as DATA — NEVER embed the lists as stem text.
               → add_standard_question() with the lists in the stem is BANNED for match: it
                 renders the grid as plain text (G-MATCH-TABLE; re-verified by Step 8
                 A-MATCH-TABLE). Keep the 'Match …' instruction in the Q.N paragraph so the
                 audit re-detects the MATCH axis.
             IF format == TEXT/PASSAGE/DI:
               → Generate via add_standard_question() (§10-S10-3)
               → add_figural_question() / add_figural_stem_question() NOT called.
             This dispatch is NOT optional. Every Q passes through it.
             Skipping it (using add_question_stem for all Qs regardless of format)
             is the root cause of the production figural defect.

  STEP B — GATE CHECK:
           If AUDIT_AVAILABLE: run audit script on cumulative docx → capture STDOUT.
           If NOT: run the Manual Gate Checklist (S4-11).
           If any fixable WARN/FAIL: fix it, re-run. Iterate to clean.
           present_files is FORBIDDEN until clean (B-7).

  STEP C — PERSIST STATE:
           If this batch contained PASSAGE questions: write progress.json (S4-8b).
           Update figural manifest if figural Qs present.
           (Do NOT yet update batches_completed — that's STEP F, after delivery.)

  STEP D — REPORT IN CHAT (no question content — MANDATE 0):
           ```
           === BATCH [N] COMPLETE ===
           Section: [section] | Q[start]–Q[end] | [count]Q generated
           Cumulative: Q1–Q[last] now in docx

           Gate checks:
             R8  (no section headers)    : PASS
             R24 (configured font)        : PASS
             R5  (no answer key in docx) : PASS
             G-OPTLABEL (1.  format)     : PASS
             K-BAL (option spread)       : PASS [show running %]
             K-PAT (max run=2)           : PASS
             MANDATE 0 (no chat content) : PASS (self-check)
             [audit script STDOUT if available]
           =========================
           ```

  STEP E — DELIVER + STOP LINE:
           Call present_files with cumulative docx.
           Then update batches_completed and current_batch in batch_state.json.
           Then print the STOP line:
           ```
           Batch [N] delivered. [X] of [total] batches done. [Y] remain.
           Next: Batch [N+1] → [next_section] Q[start]–Q[end] ([count]Q)
           Type 'continue' to proceed.
           ```

  STEP F — END THE RESPONSE.
           *** Write nothing more. Generate nothing more. ***
           This is the M1 failure point. The response is OVER here.
           (EXCEPTION: if the batch just delivered was is_final=True, do NOT
            print a continue prompt — instead proceed to Final Assembly per S4-9.)

## S4-8 — Cross-batch persistence

  S4-8a — batch_state.json update (every batch, after delivery):
    ```python
    bs = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json'))
    bs['batches_completed'].append(bs['current_batch'])
    bs['current_batch'] += 1
    # v3.3 — persist the scenario ledger so a resumed session (S4-12) cannot
    # reuse a scenario from an earlier batch. Write the FULL set every time.
    bs['concept_ledger'] = sorted(list(mock_scenario_ledger))
    # v3.9 (G3) — persist the presentation ledger too. Tuples (cg, pk) are stored
    # as "cg||pk" strings (JSON has no tuple/set); rebuilt to tuples on resume.
    bs['presentation_ledger'] = sorted(f"{cg}||{pk}"
                                       for (cg, pk) in mock_presentation_ledger)
    json.dump(bs, open(f'/home/claude/{EXAM}_M{N}_batch_state.json', 'w'))
    ```
    ORDERING: the answer_key sidecar concept_map (S7-NEW-A) is written
    per-question DURING generation, before the gate check and before
    present_files — so it is durable even if the run is interrupted after
    delivery. batch_state.concept_ledger + presentation_ledger are the cross-batch
    mirrors, refreshed here. On resume (S4-12):
        mock_scenario_ledger     = set(bs['concept_ledger'])
        mock_presentation_ledger = {tuple(s.split('||', 1))
                                    for s in bs.get('presentation_ledger', [])}
    so neither a scenario NOR a presentation can repeat across the resume boundary.

  S4-8b — progress.json (only after a batch containing PASSAGE questions):
    ```python
    progress_path = f'/home/claude/{EXAM}_M{N}_progress.json'
    progress = json.load(open(progress_path)) if os.path.exists(progress_path) else {}
    progress['passage_linked_qs'] = sorted(list(passage_linked_qs))
    progress['cloze_linked_qs']   = sorted(list(cloze_linked_qs))
    json.dump(progress, open(progress_path, 'w'))
    ```
    This is a GATED step: do not proceed to present_files until written.

## S4-9 — Final batch → Final Assembly (the ONE auto-advance that IS allowed)

  When the batch just completed has is_final = True:
    - Do NOT print a continue prompt.
    - Do NOT end the response yet.
    - Print: "=== Final batch complete. Running Final Assembly... ==="
    - Proceed directly to §13 Final Assembly in the SAME response.
    - Final Assembly: full gate sweep, registry commit, final docx, handoff.
    - THEN end the response.

  This is the only place auto-advance is permitted, and it is explicitly
  mandated by R23 / MANDATE 1 Final Batch Exception. It is NOT a violation
  of B-4 because Final Assembly is not "the next batch" — it is the closing
  step of the last batch.

## S4-10 — File naming convention

  All deliverable names use pp.paper_slug(paper_id) (v5.28 — the single shared
  implementation in paper_pipeline.py, replacing the old inline C2 v5.21 version):
  "Mock[N]" ZERO-PADDED to 2 digits for a mock (e.g. Mock01, Mock07, Mock12), else the
  scoped paper_id with "::" collapsed to a single "_" first, then remaining ":" to "_"
  (e.g. TOPIC:Physics::Mechanics:01 → TOPIC_Physics_Mechanics_01 — single underscore).
  BEHAVIOUR CHANGE from pre-v5.28: single-digit mock filenames were unpadded (Mock1);
  they are now zero-padded (Mock01) — confirmed with Radheshyam (v5.28 changelog).

  Per-batch cumulative: [ExamCode]_[paper_slug]_Q1to[last_q].docx
    (mock e.g. SSC_CGL_TIER1_Mock07_Q1to30.docx; scoped e.g. NEET_SUBJ_Physics_03_Q1to30.docx)
  Final:                [ExamCode]_[paper_slug]_Create.docx
  Answer key (internal): [ExamCode]_M[N]_answer_key.json
  Figural (internal):    [ExamCode]_fig_manifest.json
  Batch state (internal):[ExamCode]_M[N]_batch_state.json
  Progress (internal):   [ExamCode]_M[N]_progress.json
  Registry (delivered):  [ExamCode]_registry.json

## S4-11 — Manual Gate Checklist (Layer 1 — used when audit.py absent)

  When AUDIT_AVAILABLE is False, Claude runs these checks itself before
  each batch delivery. All must PASS before present_files.

  ```
  MANUAL GATE CHECKLIST — Batch [N] (cumulative docx):

  [ ] G-COUNT:    Cumulative docx has exactly the expected number of Qs
                  (sum of q_count for all batches in batches_completed + this one).
  [ ] G-RANGE:    Every Q number falls within its section's blueprint q_range.
  [ ] G-SECTIONHDR: No "SECTION:", "Part A", divider headers in body, AND (v4.8) no standalone body paragraph equal to a declared section NAME (provenance-based, reg['section_names']). (R8)
  [ ] G-PREQ1:    No title/info/scoring/cover/instruction paragraph before Q.1; the first
                  non-blank body paragraph is the bold "Q.1" stem. CATEGORY-C values
                  (marks/time/negative/options/total) are metadata, never printed. Dormant
                  only if section_rules EXAM_STRUCTURE declares paper_header_block (no current
                  exam does). (R8b) HARD FAIL.
  [ ] G-ANSWERKEY:  No answer key / "Answers:" / "Key:" in docx. (R5)
  [ ] G-FONTCHECK:  All runs use FONT_NAME / FONT_SIZE_PT (no banned fonts). (R24)
  [ ] G-OPTLABEL:   Option labels match OPTION_LABEL_FMT (configured format). (R10)
  [ ] G-BLANK:    Blank separator paragraph after every Q's last option.
  [ ] G-BOLD:     Every Q stem bold; options normal weight. (R13)
  [ ] G-FRAC:     No "a/b" slash fractions in math — OMML only (python-docx).
  [ ] G-MATH-RASTER: No algebraic/built-up expression shipped as an IMAGE. Every
                  inline <w:drawing> name matches q{N}_problem/opt{i}/stim — any
                  other name (e.g. q{N}_e1) is a rasterised expression. Built-up
                  math = OMML only (S10-4 add_math_stem). (R-MATH-OMML) HARD FAIL.
  [ ] G-KBAL:     Each option 1/2/3/4 is 20-30% of Qs so far.
  [ ] G-KPAT:     No run of 3+ identical consecutive answers.
  [ ] G-CONT:     No question content visible in this chat response. (MANDATE 0)
  [ ] G-KEY:      answer_key.json has an entry for every Q in this batch.
  [ ] G-PROG:     progress.json written if this batch had PASSAGE Qs.
  [ ] G-DEDUP:    Each new stem checked against registry_snapshot (L1/L2).
  [ ] G-CONCEPTDUP: No scenario_key repeats anywhere in this mock (DOUBT-3 RULE B).
                  Same scenario twice = HARD FAIL, even with different
                  values/names/wording, even across subtopics. Check concept_ledger.
  [ ] G-ALLOC:    Each subtopic in this batch has exactly its blueprint q_count
                  so far (DOUBT-3 RULE A). Never short, never over.
  [ ] G-GROUPMANDATE: (Issue 2b) every manifest.mandatory_groups group has ≥ its
                  min members generated in this mock. Dormant if no groups declared.
  [ ] G-MINCOUNT: (Issue 2b) every manifest.min_counts id has ≥ its k questions
                  generated in this mock. Dormant if no min_counts declared.
                  (Cadence is NOT checked here — cross-mock, owned by Step 1 RULE M5.)
  [ ] G-STIMULUS-ORPHAN: Every linked-group question in this batch physically
                  carries its shared stimulus (passage/table/chart/cloze) inside
                  its OWN block (R-LINKED / §9 Model A). No "lead-in only" layout;
                  no "Q.X and Q.Y" cross-reference text in any stem. HARD FAIL.
  [ ] G-QNUM-FIRST: Every question block (single AND linked) OPENS with its
                  "Q.<N>" paragraph — no table/passage/preamble before it; the
                  linked specific-ask paragraph is NON-numbered. (R14) HARD FAIL.
  [ ] G-FORMATDUP: No two CLASS-2/3 questions sharing a CONCEPT_GROUP have the
                  same presentation_key (stem_format_variant | distractor_strategy).
                  Different word/fact does NOT excuse an identical look. If a
                  CONCEPT_GROUP has ≥3 Qs, ≥2 stem formats appear. (RULE C) HARD FAIL.
  [ ] G-CLUSTER:  No two same-CONCEPT_GROUP Qs adjacent; no contiguous run > 2
                  from one PRESENTATION_FAMILY; each subtopic's N Qs spread across
                  its section, not stacked. (R19 v3.8)
  [ ] G-FIGURAL-COMPOSITE: Every figural Q is correctly structured per its
                  image_role variant (v5.13). stem_and_options: problem image +
                  one separate image per option, single-column, 1:1 label binding.
                  stem_only: ≥1 problem image + text options (option images NOT
                  required). options_only: ≥n option images, no problem image
                  required. No composite panel, no two images on a line, no
                  "1. Figure 1" dummy text, no question chrome baked into any raster;
                  all option images 300 DPI on a uniform square canvas.
                  (R-FIGURAL / §10-S10-7/S10-8/S10-8A) HARD FAIL.

  [ ] G-UNDERLINE: Every underline-class question (asks about "the underlined
                  word/part", or stem_format_variant 'sentence_embedded_underlined')
                  renders its target span as a REAL underlined run inside the
                  sentence — never a "(underlined: X)" text annotation, never an
                  underscore/markdown fake. (R-UNDERLINE / §10-S10-2) HARD FAIL.

  [ ] G-OPTREF: No stem references a terminal/escape option the option set lacks.
                  If a stem says "if no error → last option" / "select 'No
                  improvement'" / "None of these" / "Both…and…" / "Neither…nor…",
                  that option is PRESENT and at the named position; a "pick the
                  segment" layout carries no "no error" escape unless a real "No
                  error" option exists. (R-OPTREF / §10-S10-2) HARD FAIL.

  [ ] G-UNIQUE: Every question has EXACTLY ONE defensible answer — CHECK 3
                  verify_answer ran and answer_verified==true
                  is recorded in the sidecar. No kinship maternal/paternal split, no
                  contested-convention double-answer, no multi-rule series collision.
                  (R-ANSWER / §7 CHECK 3) HARD FAIL.

  [ ] G-ALTGROUP: No alternation group (manifest.alternation_groups) has 2+
                  members present in this mock. Dormant if no groups declared. (S3-17)
  [ ] G-ALLOC-SUBTOPIC: Each subtopic_id has EXACTLY its blueprint q_count
                  (DOUBT-3 RULE A). Distinct from G-COUNT which checks section totals.
  [ ] G-COUNT-X-UNIQUE: RULE A (exact per-subtopic count) AND RULE B (all
                  scenario_keys pairwise distinct) both hold mock-wide. (DOUBT-3)
  [ ] G-FIGTEXT: No figural questions delivered as text descriptions. Three-tier
                  check (v5.13): (1) every format=FIGURAL block has ≥ minimum images
                  for its image_role, (2) no bracketed placeholders anywhere, (3) no
                  figure-reference prose in zero-image blocks. HARD FAIL. (S7-NEW-B)
  [ ] G-MSQ-SET: (multi only, dormant if multi_present=false) MSQ key is a
                  non-empty proper subset of 1..total_options; no banned AOTA option
                  under multi (R-MSQ-ESCAPE). HARD FAIL.
  [ ] G-MSQ-CARD: (multi + fixed-k only, dormant otherwise) |S| == msq_k.
  [ ] G-MSQ-INSTR: (multi only, dormant if multi_present=false) the select-
                  instruction is present INSIDE the Q.N stem line (R14). HARD FAIL.
  [ ] G-NAT-NOOPT: (numerical only, dormant if nat_present=false) NAT question
                  renders ZERO option paragraphs. HARD FAIL.
  [ ] G-NAT-ANSWER: (numerical only) NAT value well-formed for nat_answer_type;
                  ca_range lo<=hi. HARD FAIL.
  [ ] G-NAT-GRADE: (numerical only) portal grading value/type well-formed
                  (0-9.- only charset) and deterministically re-derivable. HARD FAIL.
  [ ] G-NAT-INSTR: (numerical only) numerical-entry instruction present in
                  Q.N stem line (R14). HARD FAIL.
  [ ] G-MATCH-TABLE: Every match question (stem_format_variant == 'match_the_following')
                  renders its List columns as a REAL Word table, not plain text. Executable
                  enforcement is the Step-8 audit A-MATCH-TABLE (STEP B); this item is the
                  no-audit fallback. HARD FAIL — re-emit via add_match_table().

  All 41 items must PASS. If any FAIL: fix in this batch, re-check, then deliver.
  ```

## S4-12 — Session recovery / resume (v3.0)

  TRIGGER: MockCreate M[N] resume
  OR: batch_state.json indicates an incomplete mock (batches_completed not full).

  RECOVERY PROCEDURE:
    1. Load batch_state.json. Read current_batch and batches_completed.
    2. If batch_state.json is missing:
         - Load the most recent cumulative docx for Mock N.
         - Count Q paragraphs to find last completed Q number.
         - Map last Q to its batch using the freshly-rebuilt batch_plan.
         - Set current_batch = that batch + 1; batches_completed accordingly.
         - Rewrite batch_state.json.
    3. Load the existing cumulative docx as the base (do NOT regenerate prior Qs).
    4. Load answer_key.json (has all prior answers).
    4b. REHYDRATE THE LEDGERS (v3.9 G3 — mandatory, else resume can clone):
        mock_scenario_ledger     = set(bs.get('concept_ledger', []))
        mock_presentation_ledger = {tuple(s.split('||', 1))
                                    for s in bs.get('presentation_ledger', [])}
        If batch_state.json was missing (step 2), rebuild BOTH ledgers from the
        answer_key concept_map instead (scenario_key values, and (concept_group,
        presentation_key) pairs for every CLASS-2/3 question). Without this, RULE B
        and RULE C are blind to everything generated before the interruption.
    5. Print resume summary:
       "Resuming Mock [N]: [done] batches complete (Q1–Q[last]).
        Next: Batch [current_batch] → [section] Q[start]–Q[end].
        Type 'continue' to proceed."
    6. STOP. Wait for continue.

## S4-13 — Batch processing failure modes and their fixes (reference table)

  | Failure mode (what M1 did)                  | v3.0 rule that prevents it     |
  |---------------------------------------------|--------------------------------|
  | Generated all 100Q in one response          | B-4 + S4-7 STEP F + MANDATE 1  |
  | Auto-advanced to next batch without continue| B-5 + S4-6                     |
  | Computed Q-range from memory                | B-2 + S4-5 CHECK 2             |
  | Generated >10Q in a batch                   | B-3 + S4-1                     |
  | Spanned two sections in one batch           | S4-1 + S4-2 algorithm          |
  | Never stopped to let user review            | S4-7 STEP E + STEP F           |
  | Delivered without gate check                | B-7 + S4-7 STEP B              |
  | Lost track of which batch was next          | batch_state.json + S4-8a       |
  | Couldn't resume an interrupted mock         | S4-12                          |
  | Printed question content in chat            | MANDATE 0 + G-CONT             |


# ════════════════════════════════════════════════════════════════════════
# §5 — ANSWER POSITION BUDGET (see S3-13 for pre-build algorithm)
# ════════════════════════════════════════════════════════════════════════

## S5-1 — Pre-allocation (built at S3-13, before Q1)

  Budget built in S3-13. All Qs read correct-answer position from budget.
  Generation fills the pre-assigned slot with factually correct content.
  This is the ONLY source of answer positions. Never assign ad-hoc.

## S5-2 — K-BAL targets

  Global: 20-30% per option of total non-fixed Qs.
  Per-section: 15-35% per option.
  Fixed-set Qs (type=fixed_set in section_rules) excluded from pool.

## S5-3 — Fixed-set exclusion

  wrong_option_structure.type == "fixed_set" → excluded from K-BAL pool.
  These Qs' answer is determined by WHICH fixed option text is factually true.

## S5-4 — Difficulty interleaving

  Max 3 consecutive Hard. Max 4 consecutive Easy+Medium. Distribute evenly.

## S5-5 — Running monitor

  After each Q: check projected final % for each option.
  >32% for any option → WARN. >35% → switch to greedy assignment.

## S5-6 — K-BAL fix protocol (v2.0 — only for fixable WARN)

  Swap option TEXT positions in docx (not answer identity).
  Update answer_key sidecar: key[Q_num] = new position.
  Re-check K-PAT after every swap.
  Fixed-set Q positions excluded from any swap.

# ════════════════════════════════════════════════════════════════════════
# §6 — DEDUP ARCHITECTURE
# ════════════════════════════════════════════════════════════════════════

## S6-0 — dedup_partition priority rule

  HONOUR dedup_partition (blueprint) FIRST, then verify against registry.
  dedup_partition = mock-specific seeds/topic assignments.

## S6-1 through S6-12 — (identical to v1.0 — see full v1.0 text)

  L1: MD5 hash + near-verbatim (Jaccard ≥0.75 → HARD FAIL; 0.60-0.74 → WARN)
  L2: Semantic tuple [subtopic, approach, sorted_values] — CROSS-MOCK only
      (B v5.22: unchanged; a SEPARATE semantic_usage log tags each use with paper_index
       for the narrow-factual controlled-reuse spacing gap — L2 matching is untouched)
      (D v5.23: the L2 lookup is PARTITIONED by subtopic via SUBTOPIC_INDEX['semantic_tuples']
       (S3-5) — a candidate's tuple carries its subtopic, so only that subtopic's shard can
       match; the result is identical, just O(shard). L1 below stays GLOBAL — deliberately
       NOT sharded, so a verbatim duplicate is caught across subtopics.)
  L3: Per-subtopic exact count (blueprint q_count) + intra-mock scenario_key
      uniqueness + intra-mock presentation_key uniqueness (CLASS 2/3, RULE C,
      v3.8). SEE S6-3b/S6-3c for the authoritative rules. NOTE: CONCEPT_GROUP is
      NOT the uniqueness unit — it may repeat N times per mock; scenario_key is
      the CONTENT unit and presentation_key is the LOOK unit, and both must be
      unique within a CONCEPT_GROUP mock-wide.
  L4: Content tracking (ga_facts, passage topics, etc.)
  L5/L6: Image dHash (within-Q >20; cross-mock >25) + MD5
  L7-L18: All remaining dedup layers (grammar rules, vocab, idioms, etc.)

  KEY v2.0 FIX (GAP-19): ALL new dedup data accumulates in pending_registry
  (initialised at S3-4). NOTHING written to registry.json during generation.
  pending_registry committed ONLY at Final Assembly after all gate checks pass.

## S6-3b — ALLOCATION COUNT + INTRA-MOCK SCENARIO UNIQUENESS (DOUBT-3, v3.3)
#  ─────────────────────────────────────────────────────────────────────
#  TWO HARD RULES THAT BOTH ALWAYS HOLD — they never conflict:
#
#  RULE A (EXACT COUNT — from blueprint.json, authoritative):
#    Each subtopic produces EXACTLY the number of questions its blueprint
#    allocation specifies (subtopic_allocations[].q_count = N).
#    N is BOTH the floor AND the ceiling. Never generate N-1 or N+1.
#    This rule is NEVER weakened by the uniqueness rule below.
#
#  RULE B (SCENARIO UNIQUENESS — strict, zero tolerance):
#    No two questions ANYWHERE in the same mock may share a scenario_key.
#    A concept/scenario may appear EXACTLY ONCE per mock. Duplicating it by
#    changing values, names, numbers, or wording is STRICTLY BANNED.
#    There is no "near-duplicate" tolerance band: it is a HARD ZERO.
#
#  HOW THEY COMBINE (the resolution of DOUBT-3):
#    When a subtopic is allocated N>1 questions, the answer is NEVER to drop
#    the count. It is to generate N questions that are EACH a genuinely
#    different scenario (distinct scenario_key) within that subtopic — so a
#    student never perceives a repeat. A subtopic is "done" ONLY when N
#    distinct-scenario questions exist — never because "a scenario was used."
#  ─────────────────────────────────────────────────────────────────────

  VOCABULARY (single clear set of terms):
    CONCEPT_GROUP : the coarse subtopic-level tag from section_rules.md
                    (e.g. "compound_interest", "blood_relations", "syllogism",
                     "idiom_meaning", "mensuration_3d"). May legitimately repeat
                     up to N times in a mock (once per allocated question).
    scenario_key  : the FINE uniqueness unit. A canonical string naming the
                    specific cognitive OPERATION + structural SHAPE of one
                    question, independent of all surface values/names/wording.
                    THIS is the unit that must be unique mock-wide.
    concept_id    : (CONCEPT_GROUP, scenario_key) — used only for reporting.

  THE UNIQUENESS UNIT IS scenario_key (not CONCEPT_GROUP):
    - CONCEPT_GROUP MAY repeat exactly N times (= the allocation count).
    - But each of those N questions MUST carry a DISTINCT scenario_key.
    - Two questions with the same scenario_key anywhere in the mock = BANNED,
      even across two different subtopics (mock-global uniqueness).

  scenario_key DERIVATION (open-ended, value-independent):
    scenario_key = canonical(cognitive_operation + "|" + structural_shape)
      cognitive_operation = what the student DOES
                            (e.g. "find_time_given_CI_amount_and_rate")
      structural_shape    = the scenario structure
                            (e.g. "two_pipes_one_drain_net_fill")
    RULES:
      - Built ONLY from operation + structure. NEVER from numbers, names, or words.
      - A value-swap or reword yields the SAME scenario_key → correctly BANNED.
      - A genuinely different operation OR structure yields a NEW scenario_key
        → correctly ALLOWED.

    Examples of SAME scenario_key (BANNED as a 2nd Q in the mock):
      - "CI on ₹5000 at 10% for 2 yrs" and "CI on ₹8000 at 5% for 3 yrs"
        → both: find_CI_amount | principal_over_n_years_annual → SAME → banned.
      - "A is brother of B, B is daughter of C" vs same chain with new names
        → both: resolve_relation | linear_chain_3_people → SAME → banned.

    Examples of DIFFERENT scenario_key (each allowed once):
      - find_CI_amount | annual_compounding   vs
        find_CI_amount | half_yearly_compounding   → different shape → allowed.
      - find_CI_amount | given_P_R_T          vs
        find_principal  | given_CI_R_T (reverse)    → different operation → allowed.
      - mensuration_3d volume_of_cylinder     vs
        mensuration_3d surface_area_of_cone         → different op+shape → allowed.

  ───────────────────────────────────────────────────────────────────────
  SUBTOPIC CLASS — WHAT "SAME SCENARIO" MEANS DEPENDS ON THE SUBTOPIC TYPE
  (critical: without this, the rule mis-fires on vocabulary/fact subtopics)
  ───────────────────────────────────────────────────────────────────────
    The student-facing intent is: "a student must never FEEL a concept was
    repeated." What feels repeated differs by subtopic class. Classify each
    subtopic (from section_rules.md CONCEPT_GROUP / format) into ONE class and
    derive scenario_key accordingly:

    CLASS 1 — COMPUTATION / REASONING (e.g. CI, SI, Time-Work, Speed, Syllogism,
              Blood Relations, Seating, Mensuration, Series, Coding-Decoding):
        The UNIT is the OPERATION + STRUCTURE. Two questions doing the same
        calculation/deduction with different numbers/names FEEL repeated → BANNED.
        scenario_key = cognitive_operation | structural_shape (as above).
        To make N>1 distinct: change the operation (forward vs reverse), the
        structure (1 train vs 2 trains; linear vs circular seating), or the
        concept facet (volume vs surface area). NOT just the numbers.

    CLASS 2 — VOCABULARY / ITEM-RECALL (e.g. Synonyms, Antonyms, Idioms,
              One-Word-Substitution, Spelling, Homonyms):
        The cognitive operation is format-fixed ("pick the synonym"), so the
        TARGET ITEM is the CONTENT-uniqueness unit:
        scenario_key = subtopic | normalized_target_item
          (e.g. "synonyms|abstruse", "idioms|spill_the_beans").
        Two questions on the SAME item (even reworded) = SAME scenario_key →
        banned. Different items = different scenario_key. The item must ALSO be
        unique cross-mock via L8 vocab tracking.
        *** v3.8 CORRECTION (DOUBT-4) — a different word is NOT enough. ***
        A distinct scenario_key (different word) is NECESSARY but NOT SUFFICIENT.
        Because the operation is fixed, two CLASS-2 questions in the same
        CONCEPT_GROUP can be PRESENTATION-CLONES — identical stem template,
        identical distractor strategy, identical difficulty — and still pass the
        scenario_key check, which is exactly the M1 Q.77/Q.79 (Antonym) and
        Q.78/Q.80 (Synonym) defect. CLASS-2 subtopics with q_count > 1 MUST
        therefore ALSO satisfy RULE C (presentation uniqueness, §6-3c): every
        pair sharing a CONCEPT_GROUP must differ on
        presentation_key = (stem_format_variant | distractor_strategy).
        So two Antonym questions may NOT both be "isolated-word stem + 3-near-
        synonyms-of-headword distractors"; at least one must change format (e.g.
        sentence-embedded) or distractor strategy (e.g. same-semantic-field). See
        §6-3c for the enumerated variation menus and the ≥2-formats rule for N≥3.
        *** v4.5 — CLASS-2 under answer_cardinality=='multi' (MSQ vocabulary, dormant unless
        multi_present). The fixed operation INVERTS: a "select all synonyms of X" item
        has a correct SET of |S| true synonyms (1 ≤ |S| ≤ options_count−1, or =msq_k for
        fixed-k) plus (options_count−|S|) genuine non-synonyms as distractors — NOT the
        single-correct "1 synonym + 3 near-synonym distractors" menu. The distractor menu
        for a multi vocabulary item therefore supplies the OUT-SET pool (clearly-wrong
        items: opposites / unrelated-register / false-friends), and the IN-SET is the set
        of defensibly-correct items. scenario_key is unchanged (subtopic|target_item — the
        headword is still one item). vocab_words_used records the FULL correct set (every
        in-set word), not one word, so cross-mock vocab dedup (L8) cannot under-count.
        R-ANSWER (multi) + G-MSQ-SET/CARD govern the set; RULE C still applies.

    CLASS 3 — FACT-RECALL (e.g. single-fact questions in any knowledge/awareness
              section — GA, GK, static GK, current affairs, domain-specific facts):
        The UNIT is the FACT asserted. scenario_key = subtopic | normalized_fact
          (e.g. "polity|president_election_process").
        Two fact-recall questions on the SAME fact = banned; on different facts = allowed.
        (Cross-mock fact uniqueness already enforced by L4 ga_facts_used.)
        v3.8 (DOUBT-4): like CLASS 2, a different FACT is necessary but not
        sufficient. Two CLASS-3 questions in the same CONCEPT_GROUP must ALSO
        satisfy RULE C (§6-3c) — they may not share presentation_key
        (stem_format_variant | distractor_strategy). E.g. do not pose two polity
        facts as identical "Which of the following is correct?" stems with the
        same distractor pattern; rotate format (direct / fill-blank / assertion-
        reason / match / odd-one-out) and distractor type.

    CLASS 4 — LINKED-STIMULUS GROUPS (RC passage→5Q, DI table→2-3Q, Cloze→5
              blanks): the SHARED STIMULUS is allowed to back several questions
              (that is the format, not a repeat). The UNIT is the SUB-SKILL of
              each linked question.
        scenario_key = group_type | sub_skill
          RC examples:  "rc|direct_retrieval", "rc|inference", "rc|vocab_in_context",
                        "rc|tone_attitude", "rc|main_idea".
          DI examples:  "di|percentage_change", "di|ratio_compare", "di|average".
          Cloze:        each blank tests a distinct grammar/vocab point →
                        "cloze|collocation", "cloze|connector", "cloze|tense".
        WITHIN one linked group, no two questions may share a sub_skill
        scenario_key (no two pure inference RC Qs; no two identical DI operations).
        The shared stimulus itself is NOT counted as a repeat.
        This satisfies §8 RC minimums (≥1 inference, ≥1 vocab, ≥1 tone) AND the
        no-repeat rule simultaneously.
        DELIVERY NOTE (v3.6): CLASS 4 governs CONTENT uniqueness only. The DELIVERY
        of these groups (how the shared stimulus is physically placed so each
        member renders self-contained on a one-question screen) is governed
        separately by §9 SELF-CONTAINMENT (Model A default) + R-LINKED +
        G-STIMULUS-ORPHAN. Both must pass.

    CLASSIFICATION SOURCE: derive the class from the subtopic's format field and
    CONCEPT_GROUP in section_rules.md. If ambiguous, default to CLASS 1 (strictest).

  ───────────────────────────────────────────────────────────────────────
  §6-3c — RULE C: PRESENTATION UNIQUENESS (DOUBT-4, v3.8 — HARD, intra-mock)
  ───────────────────────────────────────────────────────────────────────
    WHY: scenario_key (RULE B) guarantees no two questions share the same
    CONTENT. It does NOT stop two questions LOOKING identical. For format-fixed
    subtopics (CLASS 2 vocabulary/item-recall, CLASS 3 fact-recall) the operation
    is constant by definition, so unless presentation is actively varied, every
    question in the CONCEPT_GROUP is a visual clone (the M1 Q.77/Q.79, Q.78/Q.80
    defect). RULE C adds the missing PRESENTATION axis.

    presentation_key = canonical(stem_format_variant + "|" + distractor_strategy)

    THE RULE (applies to CLASS 2 and CLASS 3; CLASS 1 and CLASS 4 are exempt —
    their variety is already carried by scenario_key / sub_skill). Let
    M = size of this family's stem_format_variant menu (resolve_presentation_family):
      (C1) DISTINCT VISIBLE FORMAT (primary, v3.9): for every PAIR of questions in
           the mock that share a CONCEPT_GROUP, stem_format_variant MUST differ,
           as long as the group's question count ≤ M (which it virtually always is
           — M is 3–6 and a CONCEPT_GROUP rarely holds >4 Qs). This guarantees two
           same-group questions never read with the same on-screen structure (the
           M1 complaint), not merely different distractors.
      (C2) DISTINCT presentation_key (always): every pair sharing a CONCEPT_GROUP
           MUST also differ on presentation_key = (stem_format_variant |
           distractor_strategy). When (and only when) a group's count EXCEEDS M, a
           stem_format_variant may repeat, but then the distractor_strategy must
           differ so presentation_key still differs. A distinct scenario_key
           (different word/fact) is NECESSARY but NOT SUFFICIENT.
      (C3) presentation_key AND stem_format_variant are persisted per question in
           the concept_map sidecar (§11) alongside scenario_key, and verified
           mock-wide by G-FORMATDUP (§12 S12-NEW-12).

    PRESENTATION_FAMILY (v3.9 — defined, not just exemplified): the coarse
    surface-look grouping a subtopic belongs to, resolved by
    resolve_presentation_family() below. Used by C1/C2 (to pick the right menu)
    AND by R19 anti-clustering (no contiguous run > 2 of one family). Default
    families: vocab_single_word {Antonym, Synonym, Spelling, Homonym},
    one_word_substitution {One-Word-Substitution}, idiom_phrase {Idioms},
    sentence_grammar {Error, Improvement, Voice, Narration, Tense}, fact_recall
    {GA/GK single-fact}.
    section_rules.md may override via a subtopic 'presentation_family' field.

    ENUMERATED VARIATION MENUS (the supply RULE C draws on; made executable in the
    helpers below; exam-agnostic — extend per section_rules.md if an exam adds a
    format):

      stem_format_variant
        · vocab_single_word (Antonym/Synonym/Spelling/Homonym):
            {isolated_word, sentence_embedded_underlined, fill_in_context_blank,
             odd_one_out_pair, definition_to_word}
        · one_word_substitution:
            {phrase_to_word, sentence_embedded_underlined, reverse_word_to_phrase}
        · idiom_phrase:
            {meaning_of_idiom, idiom_for_situation, sentence_substitution,
             odd_one_out}
        · fact_recall (CLASS 3):
            {direct_question, fill_blank, assertion_reason, match_the_following,
             odd_one_out, statement_correctness}

      distractor_strategy
        · vocab:
            {near_synonyms_of_headword, same_semantic_field,
             morphological_lookalike, register_or_collocation_trap,
             true_opposite_as_trap, commonly_confused_pair}
        · fact_recall:
            {plausible_same_category, swapped_attribute, close_date_or_number,
             common_misconception, adjacent_entity}

    EXECUTABLE HELPERS (v3.9 — close G1/G2; referenced by S7-CONCEPT):
    ```python
    PRESENTATION_FAMILIES = {
      'vocab_single_word'    : {'antonym','synonym','spelling','homonym'},
      'one_word_substitution': {'one_word_substitution'},
      'idiom_phrase'         : {'idiom_meaning','idiom','phrase'},
      'fact_recall'          : {'ga_fact','gk_fact','static_gk','current_affairs'},
    }
    STEM_FORMAT_MENU = {
      'vocab_single_word': ['isolated_word','sentence_embedded_underlined',
                            'fill_in_context_blank','odd_one_out_pair',
                            'definition_to_word'],
      'one_word_substitution': ['phrase_to_word','sentence_embedded_underlined',
                                'reverse_word_to_phrase'],
      'idiom_phrase'     : ['meaning_of_idiom','idiom_for_situation',
                            'sentence_substitution','odd_one_out'],
      'fact_recall'      : ['direct_question','fill_blank','assertion_reason',
                            'match_the_following','odd_one_out',
                            'statement_correctness'],
    }
    DISTRACTOR_MENU = {
      'vocab_single_word': ['near_synonyms_of_headword','same_semantic_field',
                            'morphological_lookalike','register_or_collocation_trap',
                            'true_opposite_as_trap','commonly_confused_pair'],
      'one_word_substitution': ['near_synonyms_of_headword','same_semantic_field',
                                'commonly_confused_pair','register_or_collocation_trap'],
      'idiom_phrase'     : ['near_synonyms_of_headword','same_semantic_field',
                            'commonly_confused_pair','register_or_collocation_trap'],
      'fact_recall'      : ['plausible_same_category','swapped_attribute',
                            'close_date_or_number','common_misconception',
                            'adjacent_entity'],
    }

    def resolve_presentation_family(subtopic_data):
        """G6: authoritative family resolver. Honour an explicit section_rules.md
        'presentation_family' field; else map by CONCEPT_GROUP; else by class."""
        fam = subtopic_data.get('presentation_family')
        if fam in STEM_FORMAT_MENU: return fam
        cg = (subtopic_data.get('CONCEPT_GROUP') or '').lower()
        for family, members in PRESENTATION_FAMILIES.items():
            if cg in members: return family
        # class-based fallback
        return 'fact_recall' if subtopic_data.get('SUBTOPIC_CLASS') == 'CLASS3' \
               else 'vocab_single_word'

    def format_menu_for(subtopic_data):       # G2
        return STEM_FORMAT_MENU[resolve_presentation_family(subtopic_data)]
    def distractor_menu_for(subtopic_data):   # G2
        return DISTRACTOR_MENU[resolve_presentation_family(subtopic_data)]

    def classify_subtopic(subtopic_data):
        """G1: derive the canonical SUBTOPIC_CLASS token. Tokens 'CLASS1'..'CLASS4'.
        v5.15 — LANGUAGE-AGNOSTIC + ROBUST (fixes the non-English RULE-C-disabled defect:
        an English-keyword-only classifier collapsed every non-English subtopic to CLASS1,
        silently switching OFF presentation-uniqueness so format-clone questions shipped).
        Order:
          (0) honour an explicit SUBTOPIC_CLASS from section_rules (forward-compat);
          (1) PASSAGE/DI/linked -> CLASS4;
          (2) map by CONCEPT_GROUP family — Step 5 v2.24 emits a canonical, TRANSLITERATED
              family even for Hindi/regional exams (पर्यायवाची -> 'synonym'), matched on the
              coarse base (strip any '__qualifier');
          (3) LANGUAGE-AGNOSTIC fallback: an EXPLICIT presentation_family (set by Step 5 from
              observed axis data, language-independent) → CLASS2/CLASS3, so RULE C stays ACTIVE.
              NOTE: we use only an EXPLICIT presentation_family here — never the resolver's
              vocab default — so reasoning subtopics are NOT misclassified as vocab;
          (4) else CLASS1 (computation/reasoning — strictest).
        Set once during S3-8 id-join and stored on subtopic_data."""
        explicit = str(subtopic_data.get('SUBTOPIC_CLASS') or '').upper()
        if explicit in ('CLASS1','CLASS2','CLASS3','CLASS4'):
            return explicit
        fmt = (subtopic_data.get('format') or 'TEXT').upper()
        if fmt in ('PASSAGE','DI') or subtopic_data.get('linked_group_id'):
            return 'CLASS4'                                  # linked-stimulus
        cg   = (subtopic_data.get('CONCEPT_GROUP') or '').strip().lower()
        base = cg.split('__', 1)[0]                          # coarse family (drop qualifier)
        VOCAB = {'antonym','synonym','spelling','homonym','one_word_substitution',
                 'idiom','idiom_meaning','idiom_phrase','phrase','phrasal_verb'}
        FACT  = {'ga_fact','gk_fact','static_gk','current_affairs','general_knowledge'}
        if cg in VOCAB or base in VOCAB:      return 'CLASS2'  # vocabulary/item-recall
        if cg in FACT  or base in FACT:       return 'CLASS3'  # fact-recall
        pf = str(subtopic_data.get('presentation_family') or '').strip().lower()
        if pf in ('vocab_single_word','idiom_phrase'):  return 'CLASS2'   # explicit family only
        if pf == 'fact_recall':                          return 'CLASS3'
        return 'CLASS1'                                       # computation/reasoning (strictest)
    ```

    ── v5.14 THREE-AXIS: OPTION-3 JOINT SOLVE — AXIS-2 STEERING (mirrors Step 5 classifier) ──
    ```python
    # Canonical stem_format_variant → Axis-2 class map. IDENTICAL semantics to Step 5's
    # STEM_FORMAT_TO_AXIS2 (AXIS CLASSIFIER v1.0). This is how a generated question's Axis-2
    # class is known from the variant it renders. Keep in sync with Step 5 if a variant is added.
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
    # One canonical variant per Axis-2 class (used to add a capable-but-non-family variant,
    # e.g. an OBSERVED SEQUENCE, to a subtopic's candidate set). LINKED has no stem variant
    # (stimulus-locked, allocation-enforced) so it is intentionally absent.
    AXIS2_TO_STEM_FORMAT = {
        'DIRECT': 'direct_question', 'FILL_BLANK': 'fill_blank',
        'ASSERTION_REASON': 'assertion_reason', 'MATCH': 'match_the_following',
        'STATEMENT': 'statement_correctness', 'SEQUENCE': 'sequence_ordering',
        'ODD_ONE_OUT': 'odd_one_out',
    }

    # ── WINDOW TRACKER (registry-resident; cross-mock). Plain dicts so it serializes into
    #    registry.json. One tracker per section for the CURRENT 10-mock window. ────────────
    def axis2_window_index(mock_n, mocks_per_window):
        return (int(mock_n) - 1) // max(1, int(mocks_per_window))

    def build_axis2_tracker(section_sched, window_counts):
        """section_sched = blueprint.axis_schedule[section] (or None); window_counts = the
        section's running counts for THIS window (from registry, {} if new window). Returns a
        tracker dict, or None when there is no usable target (feature inert)."""
        if not section_sched or section_sched.get('status') != 'ok':
            return None
        return {
            'window_target': dict(section_sched.get('axis2_window_target', {})),  # band-mode quotas
            'guarantee':     list(section_sched.get('axis2_guarantee', [])),      # >=1 per window
            'negative_rate': float(section_sched.get('negative_rate', 0.0)),
            'counts':        dict(window_counts.get('counts', {})),
            'neg_count':     int(window_counts.get('neg_count', 0)),
            'total':         int(window_counts.get('total', 0)),
        }

    def axis2_need(tr, cls):
        """How much the window still WANTS this Axis-2 class (higher = more). A pending
        guarantee dominates; else the remaining band gap; DIRECT/float and met/over = 0."""
        if tr is None or cls == 'DIRECT' or cls == 'LINKED':
            return 0.0
        have = tr['counts'].get(cls, 0)
        if cls in tr['guarantee']:
            return 1000.0 if have == 0 else 0.0     # only needed until its first appearance
        tgt = tr['window_target'].get(cls, 0)
        gap = tgt - have
        return float(gap) if (tgt > 0 and gap > 0) else 0.0

    def axis2_record(tr, cls, is_negative):
        if tr is None:
            return
        tr['counts'][cls] = tr['counts'].get(cls, 0) + 1
        tr['total'] += 1
        if is_negative:
            tr['neg_count'] += 1

    def axis2_want_negative(tr):
        """Soft nudge (decision 12): True when the window's running negative rate is below
        the section target. build_question honours this best-effort; never a hard gate."""
        if tr is None or tr['negative_rate'] <= 0:
            return False
        cur = (tr['neg_count'] / tr['total']) if tr['total'] else 0.0
        return cur < tr['negative_rate']

    def axis2_window_snapshot(tr):
        """Serialize the mutated counts back for the registry commit (S13-4)."""
        if tr is None:
            return None
        return {'counts': tr['counts'], 'neg_count': tr['neg_count'], 'total': tr['total']}

    # ── CAPABILITY-BOUNDED candidate variants (File 1 untouched; consistent with Step 6). ──
    def axis2_candidate_variants(subtopic_data, family_menu):
        """Faithful candidate stem_format_variants for target-aware selection, always
        INTERSECTED with the subtopic's axis2_capability (from section_rules, the File-1
        authority) — never offers a format the subtopic is not capable of (no fabrication,
        decision iii). DIRECT is always available (residual).
          • PYQ subtopics (CLASS 2/3): family-menu variants (correct for the family) PLUS a
            generic variant for each capable-but-non-family class (e.g. an OBSERVED SEQUENCE).
          • ZP subtopics: the CLASS1 default family menu is a VOCAB menu that is wrong for
            non-vocab content, so ZP draws GENERIC canonical variants (AXIS2_TO_STEM_FORMAT)
            straight from capability — neutral structures build_question can always render."""
        cap = set(subtopic_data.get('axis2_capability', ['DIRECT'])) or {'DIRECT'}
        variants, seen = [], set()
        if subtopic_data.get('is_zp'):
            for cls in cap:                         # generic canonical variant per capable class
                if cls in AXIS2_TO_STEM_FORMAT and cls not in seen:
                    variants.append(AXIS2_TO_STEM_FORMAT[cls]); seen.add(cls)
        else:
            for v in family_menu:                   # keep family order (RULE-C rotation stability)
                cls = STEM_FORMAT_TO_AXIS2.get(v, 'DIRECT')
                if cls in cap and cls not in seen:
                    variants.append(v); seen.add(cls)
            for cls in cap:                         # add capable-but-non-family (observed) classes
                if cls not in seen and cls in AXIS2_TO_STEM_FORMAT:
                    variants.append(AXIS2_TO_STEM_FORMAT[cls]); seen.add(cls)
        if 'DIRECT' not in seen:
            variants.append(AXIS2_TO_STEM_FORMAT['DIRECT'])
        return variants or [AXIS2_TO_STEM_FORMAT['DIRECT']]
    ```

    WHERE SUBTOPIC_CLASS IS SET (G1): during the S3-8 subtopic_id join, for every
    joined subtopic do `subtopic_data['SUBTOPIC_CLASS'] = classify_subtopic(...)`.
    S7-CONCEPT asserts it is present before generating; absence is a HARD STOP
    (generator bug, not a silent default).
    v4.5: at the SAME join, set `subtopic_data['answer_cardinality'] =
    answer_cardinality_by_id.get(subtopic_id, 'single')` (whole-subtopic mode from the
    blueprint subtopic_list). This is the value build_question / verify_answer /
    write_q_to_sidecar read. 'single' for every subtopic when multi_present is false.
    v5.X POSITION-BASED OVERRIDE (GAP-2026-07-22-001 §6): when the exam has >1 distinct
    question_type in marking_scheme (e.g. IIT JAM: MCQ/MSQ/NAT), answer_cardinality and
    answer_type are overridden PER Q POSITION during the generation loop (not at S3-8 join
    time) via _resolve_answer_axes(qnum, subtopic_id). The S3-8 join still sets the
    per-subtopic defaults; the per-Q override happens at generation dispatch (S7-CONCEPT).
    v5.14 (THREE-AXIS): at the SAME join, ALSO set from section_rules.md (File-1 CATEGORY B) +
    blueprint subtopic_list:
      • subtopic_data['axis2_capability'] = the parsed axis2_capability list (default ['DIRECT']).
        This bounds axis2_candidate_variants — the generator NEVER offers a format the subtopic
        is not capable of (no fabrication, decision (iii)); File 1 stays the authority.
      • subtopic_data['observed_axis2']  = the parsed observed_axis2 dict (default {}).
      • subtopic_data['is_zp'] = (r_avg == 0.0) from the blueprint subtopic_list — routes ZP
        subtopics through the target-aware selector as format-elastic fillers (decision 11).
      • v5.15: subtopic_data['form_key'] = read_field(S,'form_key') from section_rules.md
        (Step 5 v2.24), fallback question_mechanic → CONCEPT_GROUP. This is the FINE identity
        Step 6 BV-10a keys on; Step 7 carries it so intra-mock duplicate reasoning and the
        audit align on the SAME axis as the blueprint gate (no coarse/fine mismatch).
    All three are absent-safe: missing section_rules fields ⇒ capability=['DIRECT'], observed={},
    which reduces the Axis-2 steering to DIRECT-only (i.e., the v5.13 behaviour) for that subtopic.

    NORMALISATION: lowercase, snake_case, strip values. A presentation_key is a
    pair of menu tokens, never free text. If the generator cannot name a token
    for a candidate, it has not chosen a defined variant → treat as a RULE-C
    violation (G-FORMATDUP) and pick an explicit variant.

    INTERACTION WITH RULE A/B:
      - RULE A (exact count) is untouched — N is still floor AND ceiling.
      - RULE B (scenario_key) still holds — no repeated item/fact.
      - RULE C is ADDITIONAL: the N questions of a format-fixed CONCEPT_GROUP must
        be pairwise-distinct on scenario_key AND stem_format_variant (count ≤ M)
        AND presentation_key. "Done" = N questions, each a different item AND a
        visibly different format.
      All checked together at Final Assembly (G-COUNT-X-UNIQUE + G-CONCEPTDUP +
      G-FORMATDUP).

    v5.14 — RULE C × AXIS-2 TARGET RECONCILIATION (decision (b)): the Option-3 joint solve
      (S7-AXIS) makes pick_presentation TARGET-AWARE, but RULE C stays a HARD constraint and
      WINS. The tracker only STABLE-RE-ORDERS the RULE-C-VALID (unused-for-this-cg) variants by
      Axis-2 window need; it never selects a used/duplicate variant to hit a target. So RULE C's
      pairwise-distinct stem_format_variant guarantee (C1/C2) and presentation_key uniqueness
      (C3, G-FORMATDUP) hold UNCHANGED. When uniqueness and the target genuinely conflict (the
      only unique variant left is not the one the target wants), uniqueness wins and the target
      yields — audited within tolerance at Step 8, never fabricated.

    WORKED FIX (M1):
      Q.77 Antonym BENEVOLENT  → (isolated_word | near_synonyms_of_headword)
      Q.79 Antonym TRANSPARENT → also isolated_word → C1 COLLISION (same visible
      format) BEFORE even comparing distractors.
      Resolution: regenerate Q.79 with a DIFFERENT stem_format_variant, e.g.
      (sentence_embedded_underlined | same_semantic_field) — same subtopic, same
      "antonym" operation, but a visibly different question. scenario_key already
      differed; now format and presentation_key differ too.


  CROSS-MOCK vs INTRA-MOCK (do not confuse the two):
    The scenario_key rule here is INTRA-MOCK only — it bans repeats WITHIN one
    paper. The SAME scenario_key MAY appear in a DIFFERENT mock (that is a
    different paper and is expected). Cross-mock duplication of the actual
    question is separately prevented by L1/L2 against the registry. The two
    layers are complementary and must both pass (see enforcement loop CHECK 1
    and CHECK 2 below).

  ───────────────────────────────────────────────────────────────────────
  CONCEPT SOURCE ORDER — WHERE THE N DISTINCT SCENARIOS COME FROM
  (this is the crux of DOUBT-3; read carefully):
  ───────────────────────────────────────────────────────────────────────
    To fill N distinct scenario_keys for a subtopic, draw in this order:

      SOURCE 1 — OBSERVED PYQ patterns (PYQ_STEM_PATTERNS in section_rules.md):
        The SEED set. Frequency-weighted (most common patterns first, per S7-2).
        Each distinct observed pattern → one distinct scenario_key.

      SOURCE 2 — DOMAIN-GENERATED scenarios (Claude's own knowledge):
        When N exceeds the number of distinct observed PYQ patterns, INVENT
        additional genuinely-distinct scenarios from domain knowledge. Each
        must (a) fit the subtopic, (b) match the difficulty calibration for
        its slot, (c) obey ALL quality gates and banned-pattern rules.

    THE PYQ PATTERN LIST IS A SEED, NEVER A CEILING.
    "Ran out of patterns / not enough distinct concepts available" is NOT a
    valid state and is NOT a reason to reduce N or repeat a scenario. Subtopics
    like CI, Blood Relations, Syllogism, Mensuration, etc. have effectively
    UNLIMITED distinct scenarios — generate as many distinct ones as N requires.
    The generator is expected to create novel, exam-realistic scenarios beyond
    the observed PYQ set whenever N demands it.

  ───────────────────────────────────────────────────────────────────────
  THE ENFORCEMENT LOOP (per question, in order — all three must pass):
  ───────────────────────────────────────────────────────────────────────
    At session start, maintain in-memory (persisted to batch_state.json):
      mock_scenario_ledger     = set()   # scenario_key strings used in THIS mock
      mock_presentation_ledger = set()   # (concept_group, presentation_key) pairs
                                         # for CLASS 2/3 — RULE C (v3.8)

    For each question slot of a subtopic (looping exactly N times per subtopic):
      Build a candidate question, then check IN THIS ORDER:

      CHECK 1 — Intra-mock scenario uniqueness (RULE B):
        if candidate.scenario_key in mock_scenario_ledger:
            → REJECT. Regenerate on a DIFFERENT scenario (new operation/shape).
              Never reduce N. Never reuse a scenario_key.

      CHECK 1b — Intra-mock PRESENTATION uniqueness (RULE C, v3.8; CLASS 2/3 only):
        Let cg = candidate.concept_group. If the candidate is CLASS 2 or CLASS 3
        and (cg, candidate.presentation_key) already in mock_presentation_ledger:
            → REJECT. Regenerate with a DIFFERENT stem_format_variant OR
              distractor_strategy (draw a fresh pair from the §6-3c menus).
              Never reduce N. Never reuse a (cg, presentation_key) pair.
        Also enforce C2: if cg will reach q_count ≥ 3, ensure the chosen
        stem_format_variants for cg span ≥ 2 distinct values by the time the
        group is complete (track per-cg format set; if the last slot would leave
        only 1 distinct format, force a new format).

      CHECK 2 — Cross-mock dedup vs registry_snapshot (L1/L2):
        if candidate collides with a prior mock's question (Jaccard ≥0.75
        OR matching semantic tuple):
            → REJECT. Regenerate on a different scenario/values.

      CHECK 3 — Quality gates (§7): difficulty floor, banned patterns,
        3-pass verify, option quality, etc.
        if any fails → REJECT and regenerate.

      Only when CHECK 1, 1b, 2, 3 all PASS:
        ACCEPT the question.
        mock_scenario_ledger.add(candidate.scenario_key)
        if candidate is CLASS 2/3:
            mock_presentation_ledger.add((candidate.concept_group,
                                          candidate.presentation_key))
        subtopic_generated_count += 1

      Continue until subtopic_generated_count == N (RULE A satisfied).

  SAFE REGENERATION BOUND (prevents infinite code loops only):
    Bound regeneration attempts per slot at MAX_SCENARIO_TRIES = 12.
    Because scenario supply is effectively infinite, this bound is never
    expected to be reached. If it ever is, ESCALATE: deliberately broaden the
    scenario space (pick a structurally different sub-mechanic of the subtopic)
    and continue. EVEN THEN: never reduce N, never reuse a scenario_key.
    Hitting the bound is a generator-effort signal, NOT a licence to repeat.

  CROSS-SUBTOPIC COLLISIONS (mock-global uniqueness):
    scenario_key uniqueness is mock-GLOBAL, not per-subtopic. If two different
    subtopics would produce the same scenario_key (e.g. a percentage operation
    reachable from both "Percentage" and "Profit & Loss"), the second is a
    CHECK-1 collision → regenerate the second on a different scenario. A student
    must never meet effectively the same task under two different subtopic labels.

  RELATIONSHIP TO blueprint.json vs blueprint.xlsx:
    Per-subtopic counts are read from blueprint.json subtopic_allocations[].q_count
    (see S3-2). blueprint.xlsx is a human-readable companion only — Step 7 NEVER
    parses the .xlsx; blueprint.json is the single machine source for counts.

  THIS SUPERSEDES any softer "max_per_paper" reading:
    - count of questions for a subtopic in a mock = EXACTLY blueprint q_count (N).
    - count of any single scenario_key in a mock = EXACTLY 1 (hard zero for 2+).

## S6-9 — Cross-mock variant rotation (v4.4 — exam-agnostic; config-driven)

  v4.4 CHANGE: This section no longer hardcodes any subtopic name, pair, or
  parity table. It carries NO mutual-exclusion HARD STOP. It mirrors S3-17's
  contract: read structured policy from config (manifest + section_rules) by
  subtopic_id; if the config declares nothing, this is a no-op (never a stop).

  READ FROM batch_state.json rotation_state{} — not from memory.

  ── A. MUTUAL EXCLUSION (members must NOT co-occur in one mock) ──
    NOT enforced here. This invariant is owned SOLELY by S3-17, which reads
    manifest.alternation_groups by subtopic_id BEFORE generation and HARD STOPs
    if any group has >1 member allocated to the mock (HS-12). The post-generation
    audit backstop is G-ALTGROUP (S12-NEW-6). S6-9 holds no pair list and never
    re-checks this — duplicating it with hardcoded names is exactly the v3.4
    half-migration defect that v4.4 closes.
    NB: manifest.alternation_groups encodes mutual exclusion only; the parity
    ASSIGNMENT (which member appears in which mock) is a Step-1 blueprint
    ALLOCATION concern. Step 7 trusts the allocation it is handed and only
    verifies the invariant; it does not re-derive a parity schedule.

  ── B. CROSS-MOCK VARIANT ROTATION (no two consecutive mocks reuse a variant) ──
    For a subtopic that has interchangeable surface VARIANTS across mocks
    (e.g. cipher families for a coding subtopic, sub-types for a relations
    subtopic, series-variant for a number-series subtopic), Step 0 MAY author an
    OPTIONAL per-subtopic directive in section_rules.md inside that subtopic's
    block (parsed via S7-0):

        ROTATION: <variant_a> | <variant_b> | <variant_c> | ...
        ROTATION_BAN: <variant>            (optional; never permit this variant)

    Read these by subtopic_id into:
        rotation_cycles  = {subtopic_id: [variant, ...]}   # from ROTATION:
        rotation_bans    = {subtopic_id: {variant, ...}}    # from ROTATION_BAN:

    For each subtopic_id allocated in THIS mock that declares a cycle, pick the
    next variant (skipping any banned variant and the variant used in the
    previous mock), then persist it:

    ```python
    def rotation_pick(sid, rotation_cycles, rotation_bans, rotation_state):
        cycle = [v for v in rotation_cycles.get(sid, [])
                 if v not in rotation_bans.get(sid, set())]
        if not cycle:
            return None                      # no cycle declared → no constraint
        last = rotation_state.get(sid)
        choice = next((v for v in cycle if v != last), cycle[0])
        rotation_state[sid] = choice
        return choice
    ```

    A subtopic that declares NO ROTATION cycle has no rotation constraint (no-op).
    With section_rules carrying no ROTATION directives at all, S6-9 is a vacuous
    no-op and NEVER hard-stops — so an unconfigured policy can never block a run.
    (Intra-mock presentation variety remains owned by the §6-3c RULE C /
    presentation_key machinery; this section is the orthogonal CROSS-mock axis.)


# ════════════════════════════════════════════════════════════════════════
# §7 — QUESTION GENERATION ENGINE
# ════════════════════════════════════════════════════════════════════════

## S7-0 — section_rules.md parsing protocol (v1.0 — unchanged)

  Locate '--- Subtopic: [re.escape(S)] ---'
  Stop at next '--- Subtopic:' or '=== SECTION:'

## S7-1 through S7-31 — (see full v1.0 for all rules)

  Core additions/fixes in v2.0:

## S7-CONCEPT — Per-subtopic generation with scenario + presentation uniqueness (DOUBT-3 v3.3 / DOUBT-4 v3.8)

  This is the generation-time half of S6-3b/S6-3c. It runs for EVERY subtopic in
  EVERY section. It guarantees ALL rules simultaneously:
    RULE A: exactly N questions (blueprint q_count) per subtopic.
    RULE B: every question mock-wide has a distinct scenario_key.
    RULE C: CLASS 2/3 questions sharing a CONCEPT_GROUP have distinct
            presentation_key, with ≥2 stem_format_variants when N≥3 (v3.8).

  ```python
  # ledgers initialised at session start; persisted in batch_state.json across
  # batches (see S4-12 resume): mock_scenario_ledger, mock_presentation_ledger.
  MAX_SCENARIO_TRIES = 12   # safe bound only; supply is effectively infinite
  _WIDEN_EXHAUST     = 3     # B (v5.22): fruitless widenings for a narrow-FACTUAL subtopic
                            #   before its bounded (item × angle) universe is treated as drained
                            #   (decision c — empirical). Generative subtopics widen without limit.
  SPACING_GAP        = 8     # B: cumulative cross-tier spacing (papers) before an item may recur.

  def generate_subtopic(subtopic_data, N, section, registry_snapshot, axis2_tracker=None):
      """
      Produce EXACTLY N questions for this subtopic, each a distinct scenario AND
      (for CLASS 2/3) a distinct presentation. N is floor AND ceiling.
      v5.14: axis2_tracker (or None when inert) steers the flexible Axis-2 class toward the
      window target; ZP subtopics are routed as format-elastic fillers (decision 11).
      """
      cg     = subtopic_data['CONCEPT_GROUP']
      sclass = subtopic_data['SUBTOPIC_CLASS']     # CLASS1..CLASS4 (S6-3b classify)
      # v5.14: presentation (stem_format_variant) is chosen for CLASS 2/3 as before, AND for
      # ZP subtopics WHEN the Axis-2 feature is active (tracker present) — as format-elastic
      # fillers (decision 11). When the feature is inert (tracker None), ZP behaves EXACTLY as
      # v5.13 (no presentation). CLASS1 non-ZP and CLASS4 (LINKED) always keep their behaviour.
      do_presentation = (sclass in ('CLASS2', 'CLASS3')
                         or (subtopic_data.get('is_zp', False) and axis2_tracker is not None))
      produced = []
      used_formats_for_cg = set()                  # for RULE C2 (≥2 formats if N≥3)
      _widen_count = {}                            # B (v5.22): per-cg fruitless-widen counter

      scenario_source = scenario_iterator(subtopic_data)  # SOURCE 1 then SOURCE 2

      while len(produced) < N:                 # RULE A: loop until exactly N
          accepted = None
          for _try in range(MAX_SCENARIO_TRIES):
              op, shape = next(scenario_source)         # next distinct scenario
              scenario_key = canonical(op + "|" + shape)
              if scenario_key in mock_scenario_ledger:  # CHECK 1 (RULE B)
                  continue

              # v3.8 — choose a PRESENTATION for CLASS 2/3 (RULE C). Pick a
              # (stem_format_variant, distractor_strategy) pair from the §6-3c
              # menus that is NOT yet used for this concept_group, and that helps
              # satisfy C2 (force a new format if N≥3 and only 1 format so far).
              fmt = dstr = presentation_key = None
              if do_presentation:
                  # v5.14: target-aware among RULE-C-valid variants (RULE C WINS — only
                  # unique presentations are considered; the tracker only re-orders them).
                  fmt, dstr = pick_presentation(subtopic_data, cg,
                                                used_formats_for_cg,
                                                remaining=N - len(produced),
                                                tracker=axis2_tracker)
                  presentation_key = f"{fmt}|{dstr}"
                  if (cg, presentation_key) in mock_presentation_ledger:  # CHECK 1b
                      continue                          # try another presentation
                                                        # (or another scenario)

              # v4.5: resolve answer_cardinality for this subtopic from the blueprint
              # subtopic_list (whole-subtopic mode; default 'single'). Threaded into the
              # candidate so build_question renders the MSQ instruction line, verify_answer
              # runs the correct R-ANSWER branch, and write_q_to_sidecar stores the set +
              # flags. For 'multi', build_question must populate candidate.correct_set
              # (the intended set S) and candidate.has_aota_option, and obey the k-bound /
              # R-MSQ-ESCAPE. Inert ('single') when blueprint multi_present is false.
              # v5.X POSITION-BASED OVERRIDE (GAP-2026-07-22-001 §6): when the exam has
              # position-based typing (_position_based_typing True), derive answer_cardinality
              # and answer_type from the Q POSITION's marking_scheme entry, not from the
              # per-subtopic value. This ensures the same subtopic generates MCQ in Section A,
              # MSQ in Section B, NAT in Section C (e.g. IIT JAM).
              answer_cardinality, _answer_type = _resolve_answer_axes(
                  qnum, subtopic_data.get('subtopic_id'))
              if _position_based_typing:
                  subtopic_data['answer_type'] = _answer_type
              candidate = build_question(subtopic_data, op, shape, section,
                                         stem_format_variant=fmt,
                                         distractor_strategy=dstr,
                                         answer_cardinality=answer_cardinality,
                                         prefer_negative=axis2_want_negative(axis2_tracker))
              candidate.answer_cardinality = answer_cardinality

              if cross_mock_duplicate(candidate, registry_snapshot):   # CHECK 2 (L1+L2)
                  continue                                 # (B: same fn supports l1_only=True —
                                                           #  the reuse path uses it to keep L1
                                                           #  verbatim blocking while bypassing L2)
              if not passes_quality_gates(candidate, subtopic_data, section):  # CHECK 3
                  continue                                 # includes verify_answer (R-ANSWER)

              accepted = candidate
              accepted.scenario_key       = scenario_key
              accepted.subtopic_class     = sclass
              accepted.stem_format_variant= fmt
              accepted.distractor_strategy= dstr
              accepted.presentation_key   = presentation_key
              break

          if accepted is None:
              # B (v5.22): the bound was hit with no NEW distinct (item × angle). For a
              # GENERATIVE subtopic (supply effectively infinite) this is a generator-effort
              # signal → widen and keep trying (UNCHANGED behaviour; the mock path only ever
              # takes this branch). For a genuinely narrow-FACTUAL subtopic that has drained its
              # bounded (item × angle) universe (decision b: C-FACTUAL classification, gated by
              # decision c: repeated fruitless widening), take the CONTROLLED-REUSE valve.
              _widen_count[cg] = _widen_count.get(cg, 0) + 1
              if _is_narrow_factual(subtopic_data) and _widen_count[cg] >= _WIDEN_EXHAUST:
                  _pidx = globals().get('paper_index', N)          # C2 session identity (== N for a mock)
                  _pid  = globals().get('paper_id', f"MOCK:M{N:02d}")
                  reused = controlled_reuse(subtopic_data, registry_snapshot, _pidx,
                                            mock_scenario_ledger, do_presentation, cg,
                                            used_formats_for_cg, N - len(produced))
                  if reused is not None:
                      accepted = reused                            # fresh-surface, ≥8-back item;
                      mark_subtopic_exhausted(subtopic_data, _pid)  # sticky, cross-tier
                  else:
                      scenario_source = widen_scenario_space(subtopic_data, scenario_source)
                      continue
              else:
                  scenario_source = widen_scenario_space(subtopic_data, scenario_source)
                  continue                                  # never decrement N

          produced.append(accepted)
          mock_scenario_ledger.add(accepted.scenario_key)
          if do_presentation:
              mock_presentation_ledger.add((cg, accepted.presentation_key))
              used_formats_for_cg.add(accepted.stem_format_variant)
          # B (v5.22): record this (item × angle) usage in a SEPARATE additive field tagged with
          # the paper_index — so a later paper can measure the cross-tier spacing gap. The existing
          # semantic_tuples list (the L2 dedup unit) is left EXACTLY as-is (bare tuples), so L2
          # matching is byte-unchanged; semantic_usage is read only by B's controlled_reuse.
          pending_registry.setdefault('semantic_usage', []).append(
              {'subtopic_id': subtopic_data['subtopic_id'],
               'angle': accepted.scenario_key,
               'values': getattr(accepted, 'sorted_values', ''),
               'paper_index': globals().get('paper_index', N)})
          # v5.14: record this question's Axis-2 class + negativity into the WINDOW tracker.
          # LINKED for CLASS4 (stimulus-locked), the variant's class when one was chosen,
          # else DIRECT. axis2_need()==0 for DIRECT/LINKED so this never mis-steers; it keeps
          # the window counts (and the negative rate) accurate for Step 8's audit.
          _ax2 = (STEM_FORMAT_TO_AXIS2.get(accepted.stem_format_variant, 'DIRECT')
                  if accepted.stem_format_variant
                  else ('LINKED' if sclass == 'CLASS4' else 'DIRECT'))
          axis2_record(axis2_tracker, _ax2, bool(getattr(accepted, 'is_negative', False)))

      # RULE C2 final guard: if N≥3 and only one format was used, the loop above
      # should have forced variety via pick_presentation(); assert it held.
      if sclass in ('CLASS2','CLASS3') and N >= 3:
          assert len({q.stem_format_variant for q in produced}) >= 2, \
              "RULE C2 violated — diversify stem_format_variant"
      assert len(produced) == N, "RULE A violated — must never happen"
      return produced

  # ── B (v5.22): NARROW-FACTUAL EXHAUSTION + CONTROLLED REUSE ────────────────────
  # Dormant for generative subtopics and for mocks (which never drain a bounded universe);
  # the mock path is bit-identical. Active only for a C-FACTUAL subtopic whose finite
  # (item × angle) universe genuinely drains under a dense (e.g. scoped) series.
  def _is_narrow_factual(subtopic_data):
      """decision (b): questions are bounded FACTUAL recall → finite (item × angle) universe.
      From the Step-5 question_mechanic (C-FACTUAL family); never fabricated. Generative
      subtopics (CI, syllogism, …) return False and keep the strict never-reuse path."""
      mech = str(subtopic_data.get('question_mechanic', '')).lower()
      return any(k in mech for k in ('factual', 'recall', 'static_gk', 'current_affairs', 'fact'))

  def mark_subtopic_exhausted(subtopic_data, paper_id):
      """Sticky, cross-tier flag → pending_registry (committed at Final Assembly). Once set it
      NEVER clears: a subtopic drained in a mock stays drained for every scoped tier, and back."""
      ex = pending_registry.setdefault('exhausted_subtopics', {})
      ex.setdefault(subtopic_data['subtopic_id'], {'exhausted': True, 'since_paper': paper_id})

  # semantic_usage entries: {'subtopic_id': sid, 'angle': scenario_key, 'values': sorted_values,
  # 'paper_index': k}. A SEPARATE additive log (semantic_tuples/L2 stays bare + unchanged).
  def controlled_reuse(subtopic_data, registry_snapshot, paper_index,
                       scenario_ledger, do_presentation, cg, used_formats, remaining):
      """Build a fresh-SURFACE question reusing a prior (item × angle) for this exhausted
      narrow-factual subtopic, chosen so the reuse is safe:
        • spacing-{SPACING_GAP}: the item's LAST use is ≥ SPACING_GAP papers back (cross-tier).
          If none qualifies (dense series) → decision (b): least-recent + WARN (never hard-stop).
        • new angle: a scenario_key NOT already used THIS paper (CHECK 1 still holds).
        • never verbatim: the L1 (Jaccard/MD5) ban STILL applies; C-FACTUAL still web-verifies.
      Returns an accepted candidate, or None (→ caller widens again)."""
      sid  = subtopic_data['subtopic_id']
      uses = subtopic_usage(registry_snapshot, sid)   # D (v5.23): O(shard) via subtopic index
      if not uses:
          return None
      _pidx = lambda u: u.get('paper_index', -10**9)
      eligible = [u for u in uses if paper_index - _pidx(u) >= SPACING_GAP]
      if eligible:
          pool = sorted(eligible, key=_pidx)                    # oldest first
      else:
          pool = sorted(uses, key=_pidx)                        # decision (b): least-recent + WARN
          flag(f"B: subtopic {sid} exhausted and spacing-{SPACING_GAP} unsatisfiable in a dense "
               f"series — reusing the least-recent item with a fresh angle (never verbatim). WARN.")
      for u in pool:
          op, shape = u.get('angle', ''), u.get('values', '')
          scenario_key = canonical(op + "|" + shape)
          if scenario_key in scenario_ledger:                   # CHECK 1 (this paper) still holds
              continue
          fmt = dstr = presentation_key = None
          if do_presentation:
              fmt, dstr = pick_presentation(subtopic_data, cg, used_formats, remaining)
              presentation_key = f"{fmt}|{dstr}"
              if (cg, presentation_key) in mock_presentation_ledger:
                  continue
          cand = build_question(subtopic_data, op, shape, None,
                                stem_format_variant=fmt, distractor_strategy=dstr,
                                answer_cardinality=subtopic_data.get('answer_cardinality', 'single'),
                                reuse=True)                       # a FRESH surface of a known item
          if cross_mock_duplicate(cand, registry_snapshot, l1_only=True):   # L1 verbatim STILL blocks
              continue                                            # (L2 is bypassed BY DESIGN here)
          if not passes_quality_gates(cand, subtopic_data, None):
              continue
          cand.scenario_key        = scenario_key
          cand.stem_format_variant = fmt
          cand.distractor_strategy = dstr
          cand.presentation_key    = presentation_key
          cand.subtopic_class      = subtopic_data['SUBTOPIC_CLASS']
          return cand
      return None

  def pick_presentation(subtopic_data, cg, used_formats, remaining, tracker=None):
      """Return a (stem_format_variant, distractor_strategy) pair from the §6-3c
      menus for this subtopic's family. Prefer an UNUSED format for the cg; if
      remaining slots == 1 and only one format used so far, FORCE a second format
      (RULE C2). Distractor strategy is rotated so presentation_key stays unique.
      v5.14 THREE-AXIS: when `tracker` is provided, the candidate set is capability-bounded
      (axis2_candidate_variants), and among the RULE-C-valid (unused) variants the one whose
      Axis-2 class the WINDOW still needs is preferred. RULE C WINS — steering only re-orders
      the already-unique candidates; it never picks a used variant (decision (b))."""
      base = format_menu_for(subtopic_data)        # §6-3c stem_format_variant menu (family)
      fmts = axis2_candidate_variants(subtopic_data, base) if tracker is not None else base
      dstrs = distractor_menu_for(subtopic_data)   # §6-3c distractor_strategy menu
      # RULE C: valid = variants NOT yet used for this concept_group (uniqueness). Steering
      # (if any) is a STABLE re-ordering WITHIN this valid set, so a used variant is never chosen.
      unused = [f for f in fmts if f not in used_formats]
      if tracker is not None and unused:
          unused = sorted(unused,   # stable: equal-need keeps family/menu order (RULE-C rotation)
                          key=lambda f: -axis2_need(tracker, STEM_FORMAT_TO_AXIS2.get(f, 'DIRECT')))
      fmt = (unused[0] if unused else fmts[0])
      if remaining == 1 and len(used_formats) < 2:
          fmt = (unused[0] if unused else fmt)
      # rotate distractor strategy to keep (fmt|dstr) unique within the cg
      for d in dstrs:
          if (cg, f"{fmt}|{d}") not in mock_presentation_ledger:
              return fmt, d
      # all (fmt|*) taken → switch format. Search UNUSED-FIRST (target-ordered when steering),
      # then the remaining (used) formats, so a unique (format|distractor) pair is found if one
      # exists ANYWHERE — preserving v5.13 completeness (never emit a duplicate presentation_key).
      search_order = list(unused) + [f for f in fmts if f not in unused]
      for f in search_order:
          for d in dstrs:
              if (cg, f"{f}|{d}") not in mock_presentation_ledger:
                  return f, d
      return fmt, dstrs[0]   # menus large enough that this is never reached for real N

  def scenario_iterator(subtopic_data):
      for pk in weighted_patterns(subtopic_data['PYQ_STEM_PATTERNS']):
          yield (pk['operation'], pk['structural_shape'])
      while True:
          yield invent_distinct_scenario(subtopic_data)  # NO upper limit
  ```

  CALLER CONTRACT (hard rules — never violated):
    1. A scenario collision (CHECK 1) or presentation collision (CHECK 1b) NEVER
       ends a subtopic early. It triggers regeneration on a DIFFERENT scenario /
       presentation. The loop continues until exactly N questions exist, each
       distinct on scenario_key AND (CLASS 2/3) presentation_key.
    2. "Not enough observed patterns/formats for N" is NEVER a reason to stop.
       Invent additional distinct scenarios (SOURCE 2) and rotate the §6-3c
       presentation menus — supply is unlimited.
    3. NEVER change values/wording and re-submit the SAME scenario_key, and NEVER
       re-use a (concept_group, presentation_key) pair, to fill a slot.
    4. Persist mock_scenario_ledger AND mock_presentation_ledger to batch_state.json
       after each batch, so a resumed session (S4-12) cannot reuse an earlier
       scenario or presentation.

  RENDER-CONSISTENCY CONTRACT (v3.9 G4 — the label must match the question):
    build_question(subtopic_data, op, shape, section, stem_format_variant=fmt,
    distractor_strategy=dstr) MUST actually RENDER the requested presentation —
    not merely tag it. Specifically:
      · the produced STEM must structurally match stem_format_variant
        (e.g. 'sentence_embedded_underlined' → the target word appears underlined
         inside a sentence, NOT as an isolated headword, and — v4.1 — as a GENUINE
         underlined run, NOT a "(underlined: X)" parenthetical annotation);
      · the produced OPTIONS must be built by the requested distractor_strategy
        (e.g. 'same_semantic_field' → distractors drawn from the target's semantic
         field, NOT three near-synonyms of the headword).
    v5.14 SOFT PARAM — build_question also accepts prefer_negative=<bool> (default False,
    decision 12): a NUDGE toward a negative-polarity stem (NOT/EXCEPT/INCORRECT) when the
    section's window is below its negative_rate. BEST-EFFORT ONLY — honour it when the chosen
    stem_format_variant and content naturally support negation; otherwise ignore it. It NEVER
    forces an unnatural or invalid negative, never overrides correctness, and is never a gate.
    The actually-rendered is_negative (not the hint) is what the window tracker records.
    CHECK 3 (passes_quality_gates) therefore includes verify_presentation_match():
      def verify_presentation_match(candidate):
          # returns False if the rendered stem/options do not match the declared
          # stem_format_variant / distractor_strategy. A mismatch means the
          # presentation_key is cosmetic — REJECT and regenerate.
          ok = (stem_matches_format(candidate.stem, candidate.stem_format_variant)
                and options_match_strategy(candidate.options,
                                           candidate.distractor_strategy))
          # v4.1 — underline render must be REAL, not a text annotation:
          if candidate.stem_format_variant == 'sentence_embedded_underlined':
              ok = ok and has_underlined_span(candidate.block) \
                       and "(underlin" not in candidate.stem.lower()
          return ok
      # stem_matches_format() for 'sentence_embedded_underlined' now delegates the
      # underline check to has_underlined_span (S10-2 / S12-NEW-14): mere textual
      # presence of the target word — which the banned "(underlined: X)" annotation
      # satisfies — is NO LONGER sufficient. The candidate must carry a real <w:u>
      # run, or CHECK 3 fails and the question regenerates via add_stem_with_underline.

      # v4.5 — ANSWER CONTRACT (R-ANSWER, generalises v4.2 R-UNIQUE). CHECK 3 runs:
      def verify_answer(candidate):
          # v4.7: the answer_type axis is checked FIRST and SUPERSEDES cardinality — a NAT
          # question has no options, so the option-defensibility logic below does not apply.
          if candidate.get('answer_type', 'option') == 'numerical':
              # ── numerical mode (NAT; v4.7) ── R-ANSWER numerical branch. The generator
              # KNOWS candidate.nat_value. Confirm WELL-POSEDNESS by reasoning (not a regex):
              # is there a fair reading of the stem under which a DIFFERENT value follows
              # (ambiguous rounding, under-specified figure, missing unit)? If yes → return
              # False (disambiguate the stem, then regenerate). Also confirm the value's form
              # matches nat_answer_type (integer ⇒ integral) and that, for real NAT, the
              # accepted band ca_range=(lo,hi) is well-formed (lo<=hi). A 0/negative/fractional
              # value is valid (tested by presence, never truthiness). EXAM-AGNOSTIC.
              return value_uniquely_determined(candidate)       # generator-reasoned
          # answer_cardinality comes from the subtopic's blueprint entry (default 'single').
          mode = candidate.get('answer_cardinality', 'single')
          if mode != 'multi':
              # ── single mode (UNCHANGED v4.2 logic) ──
              # The generator KNOWS candidate.correct_pos. Confirm that under a FAIR
              # reading exactly ONE option is defensible. Reasoning check, not a regex:
              # for each other option, ask "is there a reasonable reading of the stem
              # under which THIS option is also correct?" If yes for any → ambiguous →
              # return False (disambiguate the stem or drop the colliding option, then
              # regenerate). Apply the R-ANSWER single-mode classes (kinship maternal/
              # paternal split; contested convention with both forms listed; multi-rule
              # series/analogy) plus any section_rules convention. EXAM-AGNOSTIC.
              return exactly_one_option_defensible(candidate)   # generator-reasoned
          # ── multi mode (MSQ; v4.5) ── candidate.correct_set is the intended set S.
          S = set(candidate.get('correct_set', []))
          n = candidate.get('options_count', 4)
          # (a) S well-formed: non-empty PROPER subset of {1..n}.
          if not S or not S.issubset(set(range(1, n + 1))) or len(S) == n:
              return False                                  # k=0 / out-of-range / k=n
          # (b) fixed-k cardinality (when configured).
          if candidate.get('msq_k_mode') == 'fixed' and len(S) != candidate.get('msq_k'):
              return False
          # (c) R-MSQ-ESCAPE: AOTA banned under multi unless msq_allow_aota.
          if not candidate.get('msq_allow_aota', False) and candidate.get('has_aota_option'):
              return False
          # (d) the SET reasoning obligation (generator-reasoned, not a regex):
          #     every option in S is defensible under EVERY fair reading, AND every
          #     option not in S is indefensible under ANY fair reading. The dangerous
          #     case is a BORDERLINE out-set option — treat exactly like the single-mode
          #     "second defensible option" defect: disambiguate or move/remove it.
          #     Negation already folded into S by the caller (S satisfies the predicate).
          return every_inset_defensible_and_every_outset_indefensible(candidate, S)
      # A passing candidate records answer_verified = True in the sidecar (S7-NEW-A);
      # G-UNIQUE (S12-NEW-16) later fails any Q missing that record; G-MSQ-SET / G-MSQ-CARD
      # (multi only) independently re-check (a)/(b)/(c).
    Without this, G-FORMATDUP could PASS on distinct labels while two questions
    still look identical — the v3.9 audit's most important closure. The sidecar
    stem_format_variant/distractor_strategy written by write_q_to_sidecar (§11)
    are taken from the ACCEPTED candidate's fields, so the gate reads what was
    actually rendered.



## S7-AXIS — Option-3 joint (difficulty × Axis-2) solve orchestration (v5.14)

  THE MOST CRITICAL RULE. A mock must replicate the exam's FORMAT MIX (Axis-2 stem
  structure), not just its syllabus and difficulty. Step 6 carries the per-section target in
  `blueprint.axis_schedule`; Step 7 steers the 7 flexible Axis-2 classes toward it WHILE
  difficulty stays SCHEDULE-FIRST.

  ```
  ORTHOGONALITY (why "joint" almost never actually trades):
    Difficulty (Easy/Medium/Hard) and Axis-2 (MATCH/ASSERTION_REASON/…) are near-INDEPENDENT
    — a MATCH question can be Easy, Medium, or Hard. So in the large majority of mocks BOTH
    the difficulty_schedule counts AND the Axis-2 window targets are satisfiable at once, and
    no trade happens. Difficulty is assigned schedule-first (unchanged, S3-2 / G-QINDEX); the
    Axis-2 class is chosen by the target-aware pick_presentation. They compose.

  TIE-BREAK (only when a genuine conflict is forced):
    1. Subtopic allocation is HARD #1 (fixed by the blueprint; never bent here).
    2. RULE C (presentation uniqueness, §6-3c) is a HARD intra-group constraint and WINS over
       the Axis-2 target: the tracker only re-orders the RULE-C-VALID (unique) variants, so a
       used variant is never chosen to hit a target (decision (b)).
    3. Between DIFFICULTY and AXIS-2, bend AXIS-2 first: difficulty guards the score signal and
       is already a hard gate (G-QINDEX). Because difficulty is assigned schedule-first and the
       Axis-2 arm only chooses among variants (which don't change a question's difficulty band),
       Axis-2 yields to difficulty automatically — the format target is met best-effort and
       AUDITED WITHIN TOLERANCE at Step 8, never forced at difficulty's expense.
    4. LINKED is allocation-enforced (Step 6, decision (a)); Step 7 does not steer it. DIRECT is
       the residual filler and is never steered toward (axis2_need==0).
  ```

  WINDOW TRACKER LIFECYCLE (registry-resident; see S3-4 read + S13-4 commit):
  ```python
  # Per MOCK, per SECTION — built once before generating that section's subtopics, then
  # threaded into every generate_subtopic() call and mutated as questions are accepted.
  axis2_trackers = {}
  for section in sections:                                  # section == mock section object
      sec_name  = section['name']
      sec_sched = axis_schedule.get(sec_name)               # blueprint.axis_schedule[section]
      win_counts = axis2_window_counts.get(sec_name, {})    # running counts for THIS window (S3-4)
      axis2_trackers[sec_name] = build_axis2_tracker(sec_sched, win_counts)  # None ⇒ inert

  # ... during generation, for each subtopic in this section:
  produced = generate_subtopic(subtopic_data, N_alloc, section, registry_snapshot,
                               axis2_tracker=axis2_trackers[section['name']])
  # generate_subtopic records each accepted question's Axis-2 class + negativity into the
  # tracker (axis2_record). When the mock's generation is complete, snapshot every tracker
  # back into axis2_window_counts for the S13-4 commit:
  for sec_name, tr in axis2_trackers.items():
      snap = axis2_window_snapshot(tr)
      if snap is not None:
          axis2_window_counts[sec_name] = snap
  ```
  Absent-safe end to end: no `axis_schedule` (pre-v1.23 blueprint) ⇒ every tracker is None ⇒
  pick_presentation falls back to the exact v5.13 family-menu rotation, and nothing is written
  to `reg['axis2_window']`. The feature turns itself off with zero behavioural drift.

  STEP 8 CONTRACT: Step 8 (MockCreateAudit) re-tags every generated question with the Step-5
  AXIS CLASSIFIER v1.0 and audits the realized per-window Axis-2 distribution against
  blueprint.axis_schedule (band = ±1/±15% whichever larger; guarantee = ≥1/window; DIRECT
  floats; negative rate = soft WARN). blueprint.json axis_schedule is the AUTHORITATIVE target.

## S7-NEW-A — Per-question answer key sidecar write (v2.0 GAP-18 fix; v3.3 concept map)

  IMMEDIATELY after each question is accepted and added to docx:
  ```python
  def write_q_to_sidecar(qnum, correct_pos, subtopic, concept_group, scenario_key,
                          subtopic_class=None, stem_format_variant=None,
                          distractor_strategy=None,
                          is_ga=False, fact_text=None, source_url=None,
                          event_date=None, answer_verified=False, answer_cardinality='single',
                          has_aota_option=False, msq_instr_in_stem=False,
                          answer_type='option', nat_value=None, ca_range=None,
                          nat_instr_in_stem=False,
                          nat_grading_type=None, nat_grading_value=None,
                          stem_precision=None,
                          subtopic_id=None, difficulty=None):
      # v4.5: correct_pos is an int for single-answer Qs and a SORTED list[int] (the
      # correct set S) for MSQ (answer_cardinality=='multi'). The sidecar stores it verbatim.
      # v4.7: for a NAT question (answer_type=='numerical') the stored answer is the typed
      # VALUE (nat_value: int|float — may be 0, negative, or fractional), NOT an option
      # position; correct_pos is ignored. ca_range=(lo,hi)|None is the accepted band (real
      # NAT) aligned to Step 4's answer_keys.json. The answer is written with `is not None`
      # semantics so a value of 0 is preserved.
      key_data = json.load(open(answer_key_path))
      if answer_type == 'numerical':
          key_data["answers"][str(qnum)] = nat_value
      else:
          key_data["answers"][str(qnum)] = (sorted(correct_pos)
                                            if answer_cardinality == 'multi' else correct_pos)

      # v3.3 — per-question concept record (DOUBT-3): lets the audit gate map
      # scenario_key → Q number for G-CONCEPTDUP / G-COUNT-X-UNIQUE, and verify
      # per-subtopic counts for G-ALLOC-SUBTOPIC. NOT placed in the docx (R5/R12).
      # v3.8 — adds presentation_key fields for RULE C / G-FORMATDUP (DOUBT-4).
      presentation_key = None
      if subtopic_class in ("CLASS2", "CLASS3") and stem_format_variant and distractor_strategy:
          presentation_key = f"{stem_format_variant}|{distractor_strategy}"
      # v4.7: qtype is the unified question-class label aligned to Step 4 (mcq|msq|nat),
      # derived from the two axes. nat supersedes cardinality.
      _qtype = ('nat' if answer_type == 'numerical'
                else 'msq' if answer_cardinality == 'multi'
                else 'mcq')
      key_data.setdefault("concept_map", {})[str(qnum)] = {
          "subtopic": subtopic,
          # v5.2 — the two fields that feed the certified per-question registry.question_index
          # (Contract_QuestionMetadataIndex v1.0). subtopic_id is the cross-step join key Step 6
          # expands into Subject/Topic/Subtopic/Question Type; difficulty is the canonical
          # Complexity label (schedule-first, from blueprint.difficulty_labels). NEVER in docx.
          "subtopic_id": subtopic_id,
          "difficulty": difficulty,
          "concept_group": concept_group,
          "scenario_key": scenario_key,
          "subtopic_class": subtopic_class,          # CLASS1..CLASS4
          "stem_format_variant": stem_format_variant, # §6-3c menu token or None
          "distractor_strategy": distractor_strategy, # §6-3c menu token or None
          "presentation_key": presentation_key,       # CLASS 2/3 only; else None
          "answer_cardinality": answer_cardinality,                 # v4.5: 'single' | 'multi'
          "answer_type": answer_type,                 # v4.7: 'option' | 'numerical'
          "qtype": _qtype,                            # v4.7: 'mcq' | 'msq' | 'nat'
          # v4.5 — MSQ structural flags (multi only; harmless defaults for single):
          "has_aota_option": bool(has_aota_option),   # an "All of the above" option exists
          "msq_instr_in_stem": bool(msq_instr_in_stem), # select-instruction is in Q.N line
          # v4.7 — NAT fields (numerical only; harmless defaults otherwise):
          "ca_range": (list(ca_range) if ca_range is not None else None),  # (lo,hi) | None
          # v5.25 — NAT fields (numerical only; harmless None otherwise): the PORTAL-safe
          # grading type/value, sourced FROM derive_nat_grading() (S7-NEW-C) at the call
          # site — never re-derived here. nat_grading_value is the exact string that
          # reaches the docx Correct-Answer line AND the portal upload, unmodified by any
          # downstream step.
          "nat_grading_type": nat_grading_type,       # 'positive_integer'|'integer'|
                                                       # 'decimal'|'decimal_fixed'|'range'|None
          "nat_grading_value": nat_grading_value,     # the 0-9.- only string, or None
          # v5.26 — the stem-stated rounding-instruction N (int) or None, EXACTLY the
          # third argument passed to derive_nat_grading() when nat_grading_type/value
          # were computed. Persisted so Step 8's A-NAT-GRADE self-consistency check can
          # re-run the SAME function call, not just guess the precision back out of the
          # already-formatted string.
          "stem_precision": stem_precision,
          "nat_instr_in_stem": bool(nat_instr_in_stem), # nat_instruction is in Q.N line
          # v4.5 — R-ANSWER: True iff CHECK 3 verify_answer passed for this Q (either
          # mode). G-UNIQUE (S12-NEW-16) Exit 1's if this is missing/False. (Renamed
          # from answer_uniqueness_verified; mode-agnostic.)
          "answer_verified": bool(answer_verified)
      }

      if is_ga and fact_text:
          key_data["sources"][str(qnum)] = {
              "fact": fact_text,
              "source_url": source_url or "",
              "event_date": event_date or "",
              "ca_window": True if event_date else False,
              "post_2020_changed": False  # update if applicable
          }
      json.dump(key_data, open(answer_key_path, 'w'), indent=2)
  ```
  Called ONCE per question. Not at end of batch. Not at end of mock.
  This ensures partial session recovery is always possible.
  The "concept_map" is an INTERNAL sidecar field — it is NEVER written to the
  docx (R5/R12). The audit gates read it directly instead of re-deriving.
  For CLASS 2/3 questions, stem_format_variant + distractor_strategy MUST be
  supplied (they are the RULE-C presentation_key inputs); omitting them for a
  CLASS-2/3 question is itself a G-FORMATDUP failure (the generator did not
  choose a defined variant — see §6-3c NORMALISATION).

## S7-NEW-B — Figural generation mandate (v2.0 GAP-12 fix)

  WHEN blueprint allocates a FIGURAL format question:

  OPTION A (generate real image — DECOMPOSED, v4.0):
    Render via matplotlib at FIGURAL_DPI=300 and place via §10-S10-7/S10-8.
    DECOMPOSITION MANDATE (R-FIGURAL — HARD STOP): a figural MCQ is rendered as
      • the problem/series figure(s) as their OWN image(s), AND
      • EACH option as its OWN separate image — one image per option,
        bound 1:1 to its "i." label, stacked SINGLE-COLUMN (one option per line).
    NEVER bake the problem + options + caption into one composite panel. NEVER
    bake the stem, caption, or option numbers into any raster (intrinsic figure
    annotations — e.g. a mirror line's M/N endpoints, geometry vertices, axis
    labels — are figure content and ARE allowed). Reference lines/axes (mirror
    line MN, number line, etc.) are drawn as REAL geometry, never floating
    letters. Build geometry vector-first (matplotlib patches / SVG paths) →
    rasterise to lossless PNG at 300 DPI (never JPEG, never upscale a small
    bitmap). All option images share one uniform SQUARE canvas size.
    Verify via view tool (9-item visual checklist). Log in figural manifest.

  OPTION B (replacement rule — if image generation fails or subtopic is banned):
    Check FIGURAL_BANNED in section_rules for this subtopic.
    If banned OR generation impossible:
      Replace with TEXT alternative from REPLACEMENT_RULE in section_rules.
      The replacement subtopic is read from that exam's REPLACEMENT_RULE
      (exam-agnostic — no subtopic name is hardcoded here). Prefer a replacement
      still missing from this mock's allocation, so the swap can also help satisfy a
      manifest.mandatory_every_mock subtopic where applicable.
      Log replacement: "FIGURAL slot Q.[N] replaced with TEXT [subtopic]."

  OPTION C (text placeholder) IS BANNED:
    NEVER deliver: "Q.19: [The figure shows a series of shapes...]"
    NEVER deliver: text descriptions of what an image would show.
    NEVER mark as "Image will be added later."
    A question is either a real image (Option A) or a real text replacement (Option B).
    Nothing in between. HARD STOP if a text placeholder is found before delivery.

## S7-24 — QA mandatory-topic tracking (v4.9 — exam-agnostic; names removed)

  v4.9 CHANGE: no QA subtopic name is hardcoded here. Every QA mandate is DATA,
  owned by the manifest + gates, mirroring the v4.4 alternation migration.

  ── MANDATORY-EVERY-MOCK presence ──
    NOT restated by name. A QA subtopic that must appear in every mock is declared
    once as DATA (Step 0 emits mandate_every_mock=true → manifest.mandatory_every_mock;
    Framework_MockTestAnalyse v2.10). Enforcement:
      • Step 1 RULE M1 force-places 1Q of each mandated id in every mock;
      • Step 7 S3-17 HARD STOPs pre-generation if a mandated id is absent (HS-8);
      • G-ALLOC-SUBTOPIC guarantees each allocated subtopic reaches its q_count, so a
        mandated subtopic is also present in the GENERATED questions (not just allocated).
    Empty config ⇒ vacuous no-op, never a false stop.

  ── ALTERNATION pairs (interest, partnership/mixture, any others) ──
    Declared once as DATA in manifest.alternation_groups (set alternation_group on
    both members in Step 0) and enforced exam-agnostically by S3-17 (pre-gen HARD
    STOP, HS-12) + G-ALTGROUP (audit backstop). No pair is hardcoded here. (v4.4)

  ── MATH CONVENTION (e.g. the π value) ──
    Read the exam's stated convention from section_rules (per-subtopic NOTE, e.g. a
    declared π value) and apply it in every affected stem. Exam-agnostic — no numeric
    convention is hardcoded in this file.

  ── ISSUE 2b MANDATES (v5.0 — now enforced) ──
    GROUP-PRESENCE ("≥1 of a subtopic GROUP per mock") and MIN-COUNT ("≥k Q per
    mock") are enforced via manifest.mandatory_groups and manifest.min_counts
    (Step 0 v2.11 + Step 1 v1.11 RULE M4/M6). Step 7 VERIFIES them at S3-17
    CHECK 3 / CHECK 4 (pre-gen) + G-GROUPMANDATE / G-MINCOUNT (post-gen
    backstops). PER-WINDOW CADENCE ("≥1 every N mocks") is a CROSS-mock
    constraint enforced solely by Step 1 RULE M5 — NOT gated in Step 7 (see
    S3-17 note). Zero subtopic names hardcoded; empty config ⇒ vacuous no-op.

## S7-31 — GIR mandatory-subtopic tracking (v4.9 — exam-agnostic; names removed)

  v4.9 CHANGE: no GIR subtopic name is hardcoded here. All GIR mandates are DATA,
  owned by the same manifest + gates as S7-24.

  ── MANDATORY-EVERY-MOCK presence ──
    A GIR subtopic that must appear in every mock is declared as DATA
    (mandate_every_mock=true → manifest.mandatory_every_mock) and enforced by Step 1
    RULE M1 + Step 7 S3-17 (HS-8) + G-ALLOC-SUBTOPIC — identical mechanism to S7-24.

  ── CROSS-MOCK VARIANT ROTATION (e.g. "a different cipher each mock") ──
    Owned by S6-9: read an OPTIONAL per-subtopic ROTATION: cycle (and ROTATION_BAN:
    for a permanently-banned variant) from section_rules by subtopic_id; rotation_pick
    selects a variant ≠ the previous mock's. A subtopic that declares no cycle has no
    constraint. No cipher family or banned variant is hardcoded here. (S6-9, v4.4)

  ── ISSUE 2b MANDATES (v5.0 — now enforced) ──
    MIN-COUNT mandates ("≥k Q per mock") and GROUP-PRESENCE mandates are enforced
    via manifest.min_counts and manifest.mandatory_groups (Step 0 v2.11 + Step 1
    v1.11 RULE M4/M6). Step 7 verifies at S3-17 CHECK 3/4 + G-GROUPMANDATE /
    G-MINCOUNT. PER-WINDOW CADENCE is cross-mock, owned by Step 1 RULE M5 — NOT
    gated here. No subtopic name or count is hardcoded; empty config ⇒ no-op.


# ════════════════════════════════════════════════════════════════════════
# §8 — FORMAT-SPECIFIC GENERATORS (v2.0 — DI TABLE FIX)
# ════════════════════════════════════════════════════════════════════════

## S8-1 — TEXT question generator (unchanged from v1.0)

## S8-2 — PASSAGE (RC) generator (unchanged from v1.0)
  Remember: after RC batch → write progress.json (S4-8).

## S8-3 — PASSAGE (Cloze) generator (unchanged from v1.0)
  Remember: after Cloze batch → write progress.json (S4-8).

## S8-4 — DI table question generator (v2.0 GAP-06 fix)

  HARD RULE: DI table MUST use build_word_table() / build_di_table_styled().
  BANNED: plain text pipe-delimited tables ("Quarter | Sales | ...")
  BANNED: text alignment with spaces ("Q1    100    200    300")
  DETECTION: before delivery, check docx for any paragraph containing
    "|" pipe characters within a non-table paragraph → C-TABLE gate FAIL.

  STRUCTURE (v5.32, GAP-2026-07-29-TBL): a DI table's GEOMETRY is part of its
  content. When the modelled PYQ carries a grouped header — one cell spanning
  several columns above a label cell spanning several rows — the generated table
  MUST carry the same spans. Squaring it into a rectangle padded with empty cells
  is BANNED: the values survive, the meaning does not.
  The geometry model is the TableSpec owned by corpus_io Cluster I
  (Framework_PYQPrepare S1-8a): ANCHOR CELLS ONLY, with 'cs' / 'rs' spans, and
  padding is not expressible. Authoring a two-tier header is therefore three
  keystrokes, not a workaround:
      {'grid': [[{'t': 'Days', 'rs': 2}, {'t': 'Printers', 'cs': 4}],
                [{'t': 'L'}, {'t': 'M'}, {'t': 'N'}, {'t': 'O'}],
                ['Friday', '10,230', '9580', '7560', '9600']],
       'header_rows': 2}
  corpus_io.place_cells() RAISES on a hole or an overlapping span, so a
  malformed table fails at generation rather than shipping as a squared grid.

  PYTHON-DOCX IMPLEMENTATION (mandatory for DI):
  v5.32 — GEOMETRY IS DELEGATED, PRESENTATION STAYS HERE. corpus_io.build_di_table
  places cells (spans included), writes text and stamps column widths; this function
  adds Step 7's own look. The previous local implementation owned BOTH and could
  express neither a colspan nor a rowspan.

  ```python
  import corpus_io      # routed to MockCreate / TestCreate in routes.json

  def build_di_table_styled(doc, spec, rows=None):
      """
      DI table: dark navy header row(s), bordered cells, span-aware.

      spec: a TableSpec (Framework_PYQPrepare S1-8a) — ANCHOR CELLS ONLY, with
            'cs' / 'rs' — or, for backward compatibility, the legacy positional
            call build_di_table_styled(doc, headers, rows).
      DO NOT use npm docx package for DI — cannot produce styled Word tables.
      """
      from docx.shared import Pt, RGBColor
      from docx.oxml import parse_xml
      from docx.oxml.ns import qn
      from docx.enum.text import WD_ALIGN_PARAGRAPH

      NAVY = DI_HEADER_COLOR  # v5.6: configurable (default "1F4E79")
      W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
      BORDER = (
          f'<w:tcBorders xmlns:w="{W}">'
          '<w:top    w:val="single" w:sz="6" w:color="000000"/>'
          '<w:left   w:val="single" w:sz="6" w:color="000000"/>'
          '<w:bottom w:val="single" w:sz="6" w:color="000000"/>'
          '<w:right  w:val="single" w:sz="6" w:color="000000"/>'
          '</w:tcBorders>'
      )
      if rows is not None:                      # legacy positional form
          spec = {'headers': spec, 'rows': rows}
      spec = corpus_io.normalise_table_spec(spec)
      header_rows = int(spec.get('header_rows', 1))

      # Data cells keep the v2.0 rule: numeric centred, text left. Header cells are
      # centred. Resolved BEFORE the build so the shared builder applies it.
      for ri, row in enumerate(spec['grid']):
          for cell in row:
              if cell.get('align'):
                  continue
              if ri < header_rows:
                  cell['align'] = 'center'
                  cell['bold'] = True
              else:
                  try:
                      float(str(cell.get('t', '')).replace(',', ''))
                      cell['align'] = 'center'
                  except ValueError:
                      cell['align'] = 'left'

      table = corpus_io.build_di_table(doc, spec, font_pt=FONT_SIZE_PT,
                                       default_align='center', font_name=FONT_NAME)

      # Header fill + white bold text, EVERY tier, merged anchors included. The
      # pre-v5.32 loop walked table.rows[0].cells, which under a merge returns one
      # entry per GRID COLUMN and repeats the anchor — it would have shaded the same
      # cell four times and never touched tier 2.
      # A raw <w:tr>/<w:tc> walk visits every cell EXACTLY ONCE: a horizontally
      # merged cell exists only as its anchor, and a vertically merged one has a
      # continuation tc that must be shaded too. Do NOT dedupe on id(tc) — lxml
      # creates a fresh proxy per findall() and Python reuses ids after GC, which
      # silently skips real cells.
      for tr in table._tbl.findall('{%s}tr' % W)[:header_rows]:
          for tc in tr.findall('{%s}tc' % W):
              tc.get_or_add_tcPr().append(parse_xml(
                  f'<w:shd xmlns:w="{W}" w:val="clear" w:color="auto" w:fill="{NAVY}"/>'))
      for ri, row in enumerate(table.rows):
          if ri >= header_rows:
              break
          for cell in row.cells:
              for para in cell.paragraphs:
                  para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                  for run in para.runs:
                      run.bold = True
                      run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                      run.font.size = Pt(FONT_SIZE_PT)

      # Borders on every cell (the raw walk visits each tc exactly once).
      for tr in table._tbl.findall('{%s}tr' % W):
          for tc in tr.findall('{%s}tc' % W):
              tc.get_or_add_tcPr().append(parse_xml(BORDER))
      return table
  ```

  Table structure in document:
    (1) Intro paragraph (bold): "Study the following table and answer the question."
    (2) build_di_table_styled(doc, spec)   # TableSpec, or legacy (headers, rows)
    (3) Question paragraph (bold): "Which of the following is correct?"
    (4) Options 1./2./3./4. (configured font, configured size, normal weight)
    (5) Blank separator paragraph

## S8-5 — DI chart generator (v5.33 — was an EMPTY TITLE from v1.0 to v5.32)

  D-8. This section carried a heading and no body for the life of the spec,
  while S8-5 was the documented home of the DI chart path and line 5576 called
  `insert_chart_image()` — a function defined nowhere in the corpus (D-7).
  A DI chart is a `data_series` or `data_single` figure under S10-6A and renders
  through `figural_core`, exactly like any other data figure.

  ```python
  import figural_core as fc

  def build_di_chart(doc, qnum, chart, *, role="stim"):
      """
      chart : {'kind': 'line'|'bar'|'scatter'|'pie',
               'series': [{'label':..., 'x':[...], 'y':[...]}, ...],
               'axes'  : {'x': {'title':..., 'units':...},
                          'y': {'title':..., 'units':...}}}
      Returns the FigureSpec, having emitted the image into `doc`.
      """
      n = len(chart["series"])
      cls = "data_series" if n >= 2 else "data_single"
      spec = fc.make_figure_spec(qnum, cls, fc.FIG_PROBLEM_DISPLAY_IN,
                                 series=fc.series_defaults(n),
                                 axes=chart.get("axes", {}),
                                 key_mode="legend" if n >= 2 else "none",
                                 role=role)
      for s, src in zip(spec["series"], chart["series"]):
          s["label"] = src["label"]

      def draw(ax, series, palette):
          for s, src in zip(series, chart["series"]):
              if chart["kind"] == "bar":
                  ax.bar(src["x"], src["y"], color=s["colour"],
                         edgecolor="black", linewidth=0.8, label=s["label"])
              elif chart["kind"] == "scatter":
                  ax.scatter(src["x"], src["y"], color=s["colour"],
                             marker=s["marker"], label=s["label"])
              elif chart["kind"] == "pie":
                  # Q7b.4 — direct on-mark labels; a legend alone is prohibited.
                  ax.pie(src["y"], labels=src["x"], colors=palette[:len(src["y"])],
                         wedgeprops={"edgecolor": "black", "linewidth": 0.8})
              else:
                  ax.plot(src["x"], src["y"], color=s["colour"],
                          linestyle=s["linestyle"], marker=s["marker"],
                          label=s["label"])
          if chart["kind"] != "pie":
              ax.set_xlabel(_axis_label(chart, "x"))     # Q9.2 — title + units
              ax.set_ylabel(_axis_label(chart, "y"))
              if len(series) >= 2:
                  ax.legend()

      png = f"q{qnum}_{role}.png"                        # Q8 canonical name
      fc.render_figure(draw, png, spec)
      fc.write_spec_sidecar(spec, png)
      insert_chart_image(doc, png, spec)
      return spec

  def _axis_label(chart, k):
      a = (chart.get("axes") or {}).get(k) or {}
      t, u = a.get("title", ""), a.get("units")
      return f"{t} ({u})" if t and u else t

  def insert_chart_image(doc, png_path, spec):
      """D-7: referenced at S10-6 since v1.0, defined nowhere until v5.33.
      Placement and alt text go through the ONE S10-8 path so the chart route
      cannot drift from the figural route — the drift between two uncontracted
      figure paths is what this gap was."""
      with open(png_path, "rb") as fh:
          _add_image_para(doc, fh.read(), spec["placed_in"], spec=spec)
  ```

## S8-6 — FIGURAL generator (v4.0 — decomposed; see S7-NEW-B + §10-S10-7/S10-8)

  A figural question is generated and emitted as DISCRETE images, never a
  composite panel. The generator:
    1. Builds geometry vector-first and renders each visual unit separately via
       render_figural_image() (§10-S10-7): one PNG for the problem/series
       figure(s); one PNG per option on a uniform square canvas; all at
       FIGURAL_DPI=300, lossless, no baked-in question text, reference lines drawn
       as real geometry.
    2. Places them via add_figural_question() (§10-S10-8): Q.N-first stem text,
       the problem image(s), then the N option images stacked SINGLE-COLUMN, each
       bound 1:1 to its "i." label (one option image per line; never two on a
       line, never a table row of options).
    3. Records the question in the figural manifest; the per-block image count
       (≥ n_options + 1) and one-image-per-option-line invariant are enforced by
       G-FIGURAL-COMPOSITE (S12-NEW-13). HARD STOP on a single-image (composite)
       figural block or any multi-image line.

## S8-7 through S8-9 — (unchanged from v1.0)

# ════════════════════════════════════════════════════════════════════════
# §9 — SELF-CONTAINMENT ARCHITECTURE (v3.6 — FULL REWRITE; was a v1.0 stub)
# ════════════════════════════════════════════════════════════════════════
#
# WHY THIS SECTION EXISTS (the M1 defect it prevents):
#   The mock docx is consumed by an ONLINE test-series engine that renders ONE
#   question per screen. The student never sees the surrounding page. Therefore a
#   question is only valid if EVERYTHING needed to answer it travels INSIDE that
#   question's own block. A shared stimulus placed once, before the first question
#   of a group, is invisible to every later question in that group → those
#   questions become unanswerable online. Mock 1 shipped exactly this defect for
#   Q74-75 (DI table), Q85-88 (Cloze), Q92-94 (RC). §9 makes it impossible.

## SC-1 — The self-containment invariant (applies to ALL questions)

  A question Q is SELF-CONTAINED iff a student shown ONLY Q's block (stem +
  options + any attached stimulus/figure/table) — with zero access to any other
  question or to any lead-in text — has everything required to select the answer.
  Single (non-linked) questions are self-contained by construction. Linked-group
  questions are the risk surface and are governed by SC-2..SC-7.

## SC-2 — What counts as a "shared stimulus" (CLASS 4 detection → §6)

  A shared stimulus is any block of content that ≥2 questions depend on:
    - RC / reading-comprehension PASSAGE (prose paragraph[s]).
    - CLOZE passage (a paragraph with numbered blanks (1),(2),(3)...).
    - DI dataset rendered as a Word TABLE, bar/pie/line CHART image, or caselet.
    - PUZZLE / arrangement clue-set (seating, scheduling, blood-relation chain).
    - Any "Study the following ... and answer Q.X to Q.Y" preamble.
  Detection is inherited from §6 CLASS 4 and the blueprint's linked_group_id /
  passage_linked_qs / cloze_linked_qs / di_linked_qs allocations. Every member
  question of a group carries the same linked_group_id in the answer_key sidecar
  and concept_map (already persisted per §11).

## SC-3 — DELIVERY CONTRACT: Model A (DEFAULT) — stimulus duplicated per member

  For every linked group, by default emit the stimulus INSIDE EACH member
  question's block. EACH member block opens with its Q-number (v3.7 Q.N-FIRST)
  and is laid out in this FIXED 5-line order:

    For each member q in group (in ascending Q-number order):
      1. Q.N CONTEXT LINE (bold) — the Q-number FUSED with the shared context /
         instruction, e.g.
           "Q.74  Study the following table and answer the question. The table
            shows the number of units (in thousands) of four products P, Q, R
            and S sold by a company in three years."
           "Q.85  In the following passage, some words have been deleted. Each
            blank is indicated by a number (1), (2), (3) and (4). Read the
            passage and select the most appropriate option for the indicated
            blank."
           "Q.92  Read the following passage and answer the question."
         Use the SINGULAR "question" — each screen shows one Q; NEVER write
         "questions Q.74 and Q.75" inside a per-member block (that re-introduces
         cross-question dependence and is banned by G-STIMULUS-ORPHAN).
         NOTHING may precede this line — no loose preamble, no table, no passage.
      2. THE EMBEDDED STIMULUS (immediately after the Q.N line):
         - PASSAGE / CLOZE → the complete passage paragraph(s) (identical text in
           every member; for Cloze, the SAME numbered-blank paragraph each time).
         - DI TABLE → a fresh Word-table object built by build_di_table_styled()
           (§8-S8-4) — re-emit the table in each member, WITH ITS SPANS (v5.32);
           never reference "the table above".
         - DI CHART → the same chart image (re-insert the image part per member;
           image-reuse ban R3 does NOT apply within a single linked group —
           see SC-6).
      3. THE SPECIFIC ASK (bold, NON-numbered paragraph) — the actual question
         for this member, e.g. "What is the total number of units (in thousands)
         of product R sold over the three years?" / "Select the most appropriate
         option for blank number (1)." / "The word 'industrious', as used in the
         passage, most nearly means:". This paragraph does NOT carry a Q-number
         (the block's single Q-number already opened it in line 1).
      4. OPTIONS (per OPTION_LABEL_FMT; default "1.  2.  3.  4.") (normal weight).
      5. BLANK SEPARATOR paragraph.

  RESULT (illustrative, using SSC CGL T1 reference Q numbers — actual Q numbers
  come from the blueprint for each exam): Q.74 opens with the context line +
  carries the table + asks the R-total;
  Q.75 opens with the SAME context line + the SAME table + asks the P-percentage;
  Q.85..Q.88 each open with the cloze instruction + the full cloze passage + one
  blank's ask; Q.92..Q.94 each open with the RC instruction + the full passage +
  one ask. Every block STARTS with "Q.<N>" and is answerable in isolation.

  This is the SAFE DEFAULT for ANY importer, because it assumes no group support
  in the engine. When in doubt, use Model A.

## SC-4 — DELIVERY CONTRACT: Model B (CONDITIONAL) — engine-native passage group

  Model B emits the stimulus ONCE and binds the member questions to it via the
  engine's comprehension/passage-group container, so the engine itself pins the
  stimulus on every member screen. Use Model B ONLY when ALL of these hold:
    (a) The target platform is CONFIRMED at S3 to support passage/comprehension
        groups on import (recorded as delivery.linked_mode = "group" in the
        session config). If unknown or unconfirmed → fall back to Model A.
    (b) The import format carries an explicit group binding (e.g. a shared
        passage_id / group_id column the importer maps). A loose lead-in
        paragraph is NOT a binding and never qualifies.
  When Model B is active, the docx still must make the grouping machine-evident:
  precede the group with one preamble paragraph tagged "[GROUP n: Q.X–Q.Y]" on
  its OWN line (this is the ONLY permitted shared-once layout, and only under
  confirmed Model B). Absent confirmation, this layout is BANNED by R-LINKED.

  DEFAULT RESOLUTION: delivery.linked_mode defaults to "embed" (Model A). It is
  set to "group" only by an explicit, recorded S3 confirmation. No silent Model B.

## SC-5 — Cloze-specific self-containment

  A Cloze passage has numbered blanks (1)..(k) and one question per blank. Under
  Model A each member question re-prints the WHOLE blanked paragraph and then asks
  for ONE specific blank ("Select the most appropriate option for blank number
  (n)."). The full paragraph (all blanks shown) must appear in every member so the
  student has full sentence context for the blank in view. Never strip the other
  blanks; never show only the target sentence.

## SC-6 — Image / table reuse exemption WITHIN a linked group

  R3 (no image reused across any two questions) and dedup of identical tables are
  CROSS-QUESTION integrity rules aimed at distinct questions. They DO NOT apply to
  the intentional re-emission of ONE group's shared stimulus across its OWN member
  questions — that re-emission is the format, not a duplicate. Implementation note:
  tag each re-emitted stimulus part with the group's linked_group_id so the dHash/
  MD5 dedup (§7) and G-DELIVERY checks skip intra-group repeats. Cross-group and
  cross-mock stimulus reuse remains banned (see Analyse §recycled_datasets).

## SC-7 — Self-containment self-check (run during S4-7 STEP A, per batch)

  For every question written in the batch:
    if q.linked_group_id is not None:
        assert stimulus_object_present_in_block(q), \
          f"R-LINKED: Q.{q.num} is a linked member with no embedded stimulus."
    # also catch accidental cross-references in single questions:
    assert not stem_references_absent_stimulus(q), \
          f"R-LINKED: Q.{q.num} references a stimulus not in its own block."
  stem_references_absent_stimulus() = stem matches any of
    {"the passage", "the table", "the graph", "the chart", "the given data",
     "blank (", "according to the passage", "Q\\.\\d+ (and|to) Q\\.\\d+"}
  AND no passage paragraph / Word table / chart image is attached to that
  question's block. Any failure is fixed IN THIS BATCH before gate check; it is
  also re-verified mock-wide at Final Assembly by gate G-STIMULUS-ORPHAN (§12).

  CONTEXT STORE / progress.json persistence (passage_linked_qs, cloze_linked_qs,
  di_linked_qs, and each group's stimulus text/table/image) is written per S4-8b
  so a resumed session re-embeds the IDENTICAL stimulus into later members.

# ════════════════════════════════════════════════════════════════════════
# §10 — OUTPUT FORMAT & DOCX CONSTRUCTION (v2.0 — FONT + OPTION FIXES)
# ════════════════════════════════════════════════════════════════════════

## S10-1 — Question format rules (v2.0 GAP-14 + GAP-15 fixes)

  FONT MANDATE (configured font — non-negotiable):
    ALL text in docx: FONT_NAME, FONT_SIZE_PT (read from exam_config / blueprint
    at S3-2; defaults Calibri 11 if not configured).
    Stem paragraphs: configured font, configured size, BOLD.
    Option paragraphs: configured font, configured size, normal weight.
    Continuation paragraphs (add_stem_ml): configured font, configured size.
    Fonts in FONT_BANNED are EXPLICITLY BANNED (default: Arial, unless Arial IS
    the configured font).

    PRE-DELIVERY FONT CHECK:
    ```python
    def verify_configured_font(docx_path):
        from docx import Document
        doc = Document(docx_path)
        for para in doc.paragraphs:
            for run in para.runs:
                if run.font.name and run.font.name.lower() not in [FONT_NAME.lower(), '']:
                    print(f"FONT FAIL: run '{run.text[:30]}' uses '{run.font.name}'"
                          f" (expected '{FONT_NAME}')")
                    return False
        return True
    ```

  OPTION LABEL FORMAT (configured — v5.6):
    All option labels rendered by OPTION_LABEL_FMT (S3-2; default "{i}.  {text}").
    Gate G-OPTLABEL matches OPTION_LABEL_RE (built from the configured format).
    Correct format: OPTION_LABEL_FMT.format(i=i, text=option_text)

  BLANK SEPARATOR: one blank paragraph (add_paragraph()) after every Q's options.
  Q-NUMBER FORMAT: Q.<N>  [stem text] — dot between Q and number, two spaces.

## S10-2 — UNDERLINE-SPAN CONTRACT (v4.1 — executable; replaces the v1.0 stub)

  A question that asks about an UNDERLINED span must render that span as a REAL
  underlined run inside the sentence — never as a parenthetical text annotation.
  This is the executable home of R-UNDERLINE. The v1.0 one-liner ("run.underline
  = True. NEVER underscores.") stated the goal but gave no trigger, no helper, and
  no ban; with only the single-run add_question_stem() available, the generator
  fell back to appending "(underlined: X)" as plain text and the underline rule
  never executed. Both gaps are closed here.

  WHEN UNDERLINE IS REQUIRED (UNDERLINE_TRIGGER):
    A block needs a real underlined span if EITHER holds:
      · stem_format_variant == 'sentence_embedded_underlined', OR
      · the stem/instruction refers to an underlined element — regex (case-insens.):
          r"underlin(e|ed)\s+(word|words|part|segment|phrase|portion|sentence)"
          OR r"the\s+underlined\b"
    Covers: Antonym/Synonym "of the underlined word", sentence IMPROVEMENT
    ("improve the underlined part of the sentence"), error-spotting on an
    underlined segment, and any future template that points at an underlined span.

    ```python
    import re
    UNDERLINE_TRIGGER_RE = re.compile(
        r"(?i)underlin(?:e|ed)\s+(?:word|words|part|segment|phrase|portion|sentence)"
        r"|the\s+underlined\b")   # single (?i) at start covers both alternatives

    def underline_required(stem_text, stem_format_variant=None):
        return (stem_format_variant == 'sentence_embedded_underlined'
                or bool(UNDERLINE_TRIGGER_RE.search(stem_text or "")))
    ```

  HOW TO RENDER (the helper the generator MUST call — never hand-roll the stem):
    Split the carrier sentence into THREE parts around the target span and underline
    ONLY the middle run. The instruction line and the carrier sentence are bold per
    R13; underline is layered on the target run on top of bold.

    ```python
    from docx.shared import Pt

    def add_stem_with_underline(doc, qnum, instruction, pre, target, post,
                                bold=True):
        """
        Renders an underline-class stem as:
          "Q.<qnum>  <instruction>"   (bold)            — e.g. the task line
          "<pre><TARGET underlined><post>"  (bold; TARGET also underlined)
        `pre`/`post` may be "" (target at start/end). NEVER pass the target as a
        bracketed note. Two paragraphs keep the instruction and the carrier
        sentence on separate lines, matching the reference exam layout.
        """
        assert target and target.strip(), "underline target span must be non-empty"
        # 1) instruction line (Q.N-first, R14)
        p1 = doc.add_paragraph()
        r1 = p1.add_run(f"Q.{qnum}  {instruction}")
        r1.bold = bold; r1.font.name = FONT_NAME; r1.font.size = Pt(FONT_SIZE_PT)
        # 2) carrier sentence with the underlined target span
        p2 = doc.add_paragraph()
        for chunk, is_target in ((pre, False), (target, True), (post, False)):
            if chunk == "":
                continue
            r = p2.add_run(chunk)
            r.bold = bold
            r.underline = is_target          # REAL <w:u> on the target run only
            r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
        return p1, p2
    ```

    For a single-line stem (no separate instruction, e.g. error-spotting where the
    whole sentence is the stem), pass instruction="" and the helper emits only the
    carrier paragraph as the Q.N-first line — fuse "Q.<qnum>  " into `pre`.

  BANNED (R-UNDERLINE; G-UNDERLINE will Exit 1 on any of these):
    · "(underlined: senior than me)"  · "(underline: benevolent)"
    · "(underlined word: X)"  · any bracketed/quoted note naming the target in
      place of underlining it
    · underscore runs ("____") or markdown "_x_" / "<u>" text as a fake underline
    Correct  →  the words "senior than me" appear with run.underline = True INSIDE
                the sentence "He is senior than me by three years."
    Incorrect → "He is senior than me by three years. (underlined: senior than me)"

  VERIFY (audit hook): has_underlined_span(block) returns True iff some run in the
  block carries w:u. G-UNDERLINE (S12-NEW-14) and the §7 render-consistency
  contract both call it; see S12-NEW-14 for the run-level XML check.

  CARRIER-SENTENCE LAYOUT (v4.2 — generalised from underline to all such stems):
  Any stem that contains a CARRIER SENTENCE the candidate must read — underline
  questions, error-spotting ("select the part that contains the error"),
  sentence-improvement ("improve the underlined/bracketed part"), fill-in-the-
  sentence — emits the INSTRUCTION line and the SENTENCE as SEPARATE paragraphs:
      (1) "Q.<N>  <instruction>"            (bold; Q.N-first, R14)
      (2) "<the carrier sentence>"          (bold; its own paragraph)
      then options. NEVER concatenate the instruction and the sentence into one
  run/paragraph (the M1 Q.100 run-on "…select the last option.Each of the
  students…"). add_stem_with_underline already does this; add_carrier_sentence_stem
  is the non-underline equivalent:
    ```python
    def add_carrier_sentence_stem(doc, qnum, instruction, sentence, bold=True):
        p1 = doc.add_paragraph(); r1 = p1.add_run(f"Q.{qnum}  {instruction}")
        r1.bold = bold; r1.font.name = FONT_NAME; r1.font.size = Pt(FONT_SIZE_PT)
        p2 = doc.add_paragraph(); r2 = p2.add_run(sentence)
        r2.bold = bold; r2.font.name = FONT_NAME; r2.font.size = Pt(FONT_SIZE_PT)
        return p1, p2
    ```

## S10-3 — Python helpers (v2.0 — Calibri enforced)

  ```python
  from docx import Document
  from docx.shared import Pt
  from docx.oxml import parse_xml

  def add_question_stem(doc, qnum, stem_text, bold=True, msq_instruction=None):
      # v4.5: for MSQ (answer_cardinality=='multi') the select-instruction is appended INSIDE
      # this single bold Q.N-first paragraph (R14 / G-QNUM-FIRST — there is NO paper-
      # level instructions page, and a separate instruction paragraph would break R14).
      # msq_instruction is the localized phrase from section_rules (msq_instruction_for);
      # None for single-answer questions ⇒ byte-identical to v4.4.
      text = f"Q.{qnum}  {stem_text}"
      if msq_instruction:
          text = f"{text}  {msq_instruction}"
      p = doc.add_paragraph()
      run = p.add_run(text)
      run.bold = bold
      run.font.name = FONT_NAME         # v5.6: configurable
      run.font.size = Pt(FONT_SIZE_PT)  # v5.6: configurable
      return p

  def msq_instruction_for(section_rules_text, language='english'):
      # EXAM-AGNOSTIC + localized: prefer the exam's own phrasing from section_rules
      # (field msq_instruction, optionally msq_instruction_hi for Hindi/bilingual); fall
      # back to a universal default. The phrase is parenthesised so it reads as an
      # instruction within the stem line.
      import re as _re
      key = 'msq_instruction_hi' if language in ('hindi', 'bilingual') else 'msq_instruction'
      m = _re.search(rf'^\s*{key}\s*:\s*(.+?)\s*$', section_rules_text or '', _re.M)
      phrase = m.group(1).strip() if m else None
      if not phrase:
          phrase = ('(एक या अधिक विकल्प सही हो सकते हैं)'
                    if language in ('hindi', 'bilingual')
                    else '(One or more options may be correct)')
      return phrase if phrase.startswith('(') else f'({phrase})'

  def _option_label(i, fmt=OPTION_LABEL_FMT):
      """Render the label for option i (1-based) using the configured format."""
      return fmt.format(
          i=i, text='{text}',
          alpha_upper=chr(ord('A') + i - 1),
          alpha_lower=chr(ord('a') + i - 1)
      ).replace('{text}', '').strip()

  def add_text_options(doc, options):
      for i, opt in enumerate(options, 1):
          p = doc.add_paragraph()
          lbl = _option_label(i)
          label = f"{lbl}  {opt}" if not lbl.endswith(' ') else f"{lbl}{opt}"
          run = p.add_run(label)
          run.bold = False
          run.font.name = FONT_NAME         # v5.6: configurable
          run.font.size = Pt(FONT_SIZE_PT)   # v5.6: configurable

  def add_blank_separator(doc):
      doc.add_paragraph()

  def add_stem_ml(doc, text, bold=False):
      p = doc.add_paragraph()
      run = p.add_run(text)
      run.bold = bold
      run.font.name = FONT_NAME
      run.font.size = Pt(FONT_SIZE_PT)
      return p

  def add_standard_question(doc, qnum, stem, options, answer_cardinality='single',
                            section_rules_text='', language='english'):
      # v4.5: dispatch on the subtopic's answer_cardinality (blueprint subtopic_list). For
      # 'multi', append the localized select-instruction to the Q.N stem line and record
      # msq_instr_in_stem=True for the sidecar (G-MSQ-INSTR). 'single' ⇒ unchanged.
      msq_instr = (msq_instruction_for(section_rules_text, language)
                   if answer_cardinality == 'multi' else None)
      add_question_stem(doc, qnum, stem, msq_instruction=msq_instr)
      add_text_options(doc, options)
      add_blank_separator(doc)
      return {'msq_instr_in_stem': bool(msq_instr)}   # caller forwards to write_q_to_sidecar

  def add_match_table(doc, qnum, instruction, columns, options,
                      answer_cardinality='single', section_rules_text='', language='english',
                      header_fill=None):
      """MANDATORY renderer for stem_format_variant == 'match_the_following' (§10-S10-3M).
      Renders a MATCH question as a REAL Word table grid — never plain text. Layout:
        (1) Q.N-first bold instruction paragraph (R14 / G-QNUM-FIRST; MSQ instruction in-stem);
        (2) a bordered Word table, one column per list (List-I | List-II | …): a header row
            plus one row per item. UNEQUAL columns are blank-padded (an extra List-II
            distractor renders as a row whose List-I cell is empty);
        (3) the pairing-quad options (e.g. 'A-I, B-III, …') via the standard option block;
        (4) blank separator (R13).
      columns : list of (header, [item, …]); each item already carries its own label
                ('(A) Collagen', 'I. triple helix', …). >=2 columns supported (List-III).
      options : the pairing-quad option texts.
      Exam-agnostic: headers, labels and the optional header_fill come from the caller — no
      hardcoded scheme. Emitting a match via add_standard_question() (lists as stem text) is
      BANNED — its grid renders as plain text: G-MATCH-TABLE, re-verified by Step 8
      A-MATCH-TABLE. Keeping the 'Match …' instruction in the Q.N paragraph (not inside the
      table) is what lets Step 8 re-detect the MATCH axis and confirm the table is present.
      """
      from docx.shared import Pt, RGBColor
      from docx.oxml import parse_xml
      from docx.enum.text import WD_ALIGN_PARAGRAPH
      msq_instr = (msq_instruction_for(section_rules_text, language)
                   if answer_cardinality == 'multi' else None)
      add_question_stem(doc, qnum, instruction, msq_instruction=msq_instr)
      headers   = [str(h) for h, _ in columns]
      col_items = [[str(x) for x in items] for _, items in columns]
      ncols = len(headers)
      nrows = max((len(c) for c in col_items), default=0)
      BORDER = (
          '<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:top    w:val="single" w:sz="6" w:color="000000"/>'
          '<w:left   w:val="single" w:sz="6" w:color="000000"/>'
          '<w:bottom w:val="single" w:sz="6" w:color="000000"/>'
          '<w:right  w:val="single" w:sz="6" w:color="000000"/>'
          '</w:tcBorders>')
      table = doc.add_table(rows=1 + nrows, cols=ncols)
      # header row (bold; optional fill for a styled header)
      for ci, h in enumerate(headers):
          cell = table.rows[0].cells[ci]
          run = cell.paragraphs[0].add_run(h)
          run.bold = True
          run.font.name = FONT_NAME
          run.font.size = Pt(FONT_SIZE_PT)
          if header_fill:
              run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
              cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
              cell._tc.get_or_add_tcPr().append(parse_xml(
                  f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
                  f' w:val="clear" w:color="auto" w:fill="{header_fill}"/>'))
      # data rows (blank-pad short columns so unequal lists render correctly)
      for ri in range(nrows):
          for ci in range(ncols):
              items = col_items[ci]
              cell = table.rows[ri + 1].cells[ci]
              run = cell.paragraphs[0].add_run(items[ri] if ri < len(items) else '')
              run.font.name = FONT_NAME
              run.font.size = Pt(FONT_SIZE_PT)
      # borders on every cell
      for row in table.rows:
          for cell in row.cells:
              cell._tc.get_or_add_tcPr().append(parse_xml(BORDER))
      add_text_options(doc, options)
      add_blank_separator(doc)
      return {'msq_instr_in_stem': bool(msq_instr), 'rendered_match_table': True}
  ```

## S10-4 — OMML library (complete — see v1.0 for full implementation)

  TECHNOLOGY MANDATE (GAP-05 fix):
  The OMML helpers below REQUIRE python-docx. They CANNOT run in npm docx.
  If exam has any mathematical content → MUST use Python + python-docx.

  ```python
  from docx.oxml import parse_xml
  M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
  def _r(t): return f'<m:r xmlns:m="{M}"><m:t xml:space="preserve">{t}</m:t></m:r>'
  def frac(n,d): return f'<m:f xmlns:m="{M}"><m:num>{n}</m:num><m:den>{d}</m:den></m:f>'
  def sup(b,e): return f'<m:sSup xmlns:m="{M}"><m:e>{b}</m:e><m:sup>{e}</m:sup></m:sSup>'
  def sqrt(x): return (f'<m:rad xmlns:m="{M}"><m:radPr>'
                       f'<m:degHide m:val="1"/></m:radPr><m:deg/>'
                       f'<m:e>{x}</m:e></m:rad>')
  def omath(*p): return f'<m:oMath xmlns:m="{M}">{"".join(p)}</m:oMath>'
  def add_math(paragraph, omath_xml): paragraph._p.append(parse_xml(omath_xml))
  ```

  Math rendering decision tree (in order — use FIRST applicable rule):
  0. ANY built-up expression (rules 3-6 below) is rendered as OMML and is NEVER
     rasterised. The matplotlib / figural / image pipeline is BANNED for
     algebraic/symbolic math — it is for GEOMETRIC FIGURES ONLY. (R-MATH-OMML.)
  1. Unit labels (km/h, m/s, cm²): plain text
  2. Single symbols (², ³, √n, ×, ÷, ≤, ≥, ±, π, °, θ): Unicode
  3. Fractions (a/b stacked): MANDATORY OMML frac()
  4. Nested radicals: MANDATORY OMML sqrt()
  5. Exponent+fraction: MANDATORY OMML
  6. Trig identities with fractions: MANDATORY OMML
  7. Raw LaTeX (\\frac, \\sqrt): NEVER — convert to OMML

  MATH-AS-OMML ROUTING CONTRACT (v4.3 — the executable home for rules 0/3-6).
  Before v4.3 the tree above stated the GOAL but there was no function to call:
  add_question_stem() writes the whole stem as one text run, so a generator with
  a built-up expression had no OMML entry point and could fall back to a raster
  (the M1 Q.55 defect: "x + 1/x = 5" and "x²+1/x²" shipped as 300-DPI matplotlib
  PNGs). These helpers close that hole. Any stem or option whose text matches
  MATH_TRIGGER_RE MUST be emitted through add_math_stem / emit_math_inline (OMML),
  NEVER through the figural raster path.

  ```python
  import re
  from docx.shared import Pt
  from docx.oxml import parse_xml

  # Detects a BUILT-UP expression (rules 3-6): a stacked fraction (token "/"
  # between operands, not a unit label), an exponent/superscript, or a radical.
  # Unit labels (km/h, m/s) and single Unicode symbols are deliberately NOT matched.
  MATH_TRIGGER_RE = re.compile(
      r"(?:[A-Za-z0-9\)\]]\s*/\s*[A-Za-z0-9\(\[])"      # stacked fraction a/b
      r"|(?:\^\s*[-+]?\d)"                               # caret exponent x^2
      r"|(?:[A-Za-z0-9]\s*[\u00b2\u00b3])"              # superscript ² ³ on a term
      r"|(?:\\frac|\\sqrt)"                              # raw LaTeX
      r"|(?:\u221a\s*[\(A-Za-z0-9])"                    # radical √(...)
  )
  # Allow-list so unit labels never trip the fraction branch.
  UNIT_LABEL_RE = re.compile(r"(?i)\b(km|m|cm|mm|kg|g|l|ml|s|hr|h)\s*/\s*(h|s|min|hr)\b")

  def needs_omml(text):
      if not text:
          return False
      if UNIT_LABEL_RE.search(text):
          # a unit label alone is plain text; only force OMML if ANOTHER built-up
          # token is also present.
          stripped = UNIT_LABEL_RE.sub(" ", text)
          return bool(MATH_TRIGGER_RE.search(stripped))
      return bool(MATH_TRIGGER_RE.search(text))

  def assert_not_math(label):
      """Guard called by the FIGURAL path (S10-7). A built-up expression must
      NEVER reach the raster pipeline. R-MATH-OMML HARD STOP."""
      if needs_omml(label):
          raise AssertionError(
              f"R-MATH-OMML: refusing to RASTERISE a math expression "
              f"({label!r}). Built-up math is OMML only (S10-4 add_math_stem); "
              f"the figural pipeline is for geometric figures only.")

  def emit_math_inline(paragraph, omath_xml):
      """Append one <m:oMath> block to an existing run-bearing paragraph,
      interleaved with surrounding text runs (alias of add_math, kept explicit
      so callers route built-up math here, not to a raster)."""
      paragraph._p.append(parse_xml(omath_xml))

  def add_math_stem(doc, qnum, segments, bold=True):
      """Build a Q.N-first stem (R14) that interleaves text and OMML.
      `segments` = ordered list of ('text', str) and ('omml', omath_xml) tuples.
      Example for Q.55 'If x+1/x=5, then ... value of x²+1/x² ?':
        add_math_stem(doc, 55, [
          ('text','If  '),
          ('omml', omath(_r('x + '), frac(_r('1'), _r('x')), _r(' = 5'))),
          ('text','  , then what is the value of  '),
          ('omml', omath(sup(_r('x'),_r('2')), _r(' + '),
                         frac(_r('1'), sup(_r('x'),_r('2'))))),
          ('text',' ?'),
        ])
      """
      p = doc.add_paragraph()
      first = p.add_run(f"Q.{qnum}  ")
      first.bold = bold; first.font.name = FONT_NAME; first.font.size = Pt(FONT_SIZE_PT)
      for kind, val in segments:
          if kind == 'text':
              r = p.add_run(val)
              r.bold = bold; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
          elif kind == 'omml':
              emit_math_inline(p, val)        # OMML run — never an image
          else:
              raise ValueError(f"add_math_stem: bad segment kind {kind!r}")
      return p
  ```

  GENERATION ROUTING (mandatory): when build_question() prepares a stem or an
  option, it FIRST tests needs_omml() on the rendered text. If true, the segment
  is emitted via add_math_stem / emit_math_inline (OMML). It is a HARD STOP to
  route such a segment to render_figural_image() — that function now calls
  assert_not_math() and will raise. Geometric figures (mensuration/coordinate
  diagrams, reasoning panels) are the ONLY content the figural raster path
  accepts, and they are emitted under the canonical image-naming convention
  (§10-S10-7/S10-8) so gate G-MATH-RASTER can tell a figure from a stray raster.

## S10-LINKED — linked-member emission (v3.7 — Q.N-FIRST ordered block)

  Called by S4-7 STEP A for every member of a CLASS-4 group. Emits the member as
  the §9 SC-3 ordered block: Q.N context line FIRST, then the embedded stimulus,
  then the specific ask, then options, then a blank separator. The stimulus
  content is read from the group's context-store entry so all members get
  byte-identical text/table/image (resume-safe per S4-8b).

  ```python
  def add_qn_context(doc, qnum, context):
      """Line 1 of the block: 'Q.<N>  <shared context/instruction>' (BOLD).
      This is the SINGLE Q-numbered paragraph for the whole block (R14)."""
      p = doc.add_paragraph()
      r = p.add_run(f"Q.{qnum}  {context}")     # Q.N FUSED with context
      r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
      return p

  def add_specific_ask(doc, ask_text):
      """Line 3 of the block: the actual question (BOLD, NON-numbered).
      Carries NO 'Q.N' — the block's Q-number already opened it in line 1."""
      p = doc.add_paragraph()
      r = p.add_run(ask_text)
      r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
      return p

  def add_linked_stimulus(doc, qnum, group):
      """
      Emit ONE linked member in §9 SC-3 order. Q.N comes FIRST (v3.7 Q.N-FIRST).
      group = {
        'linked_group_id': str,
        'mode'           : 'passage' | 'cloze' | 'di_table' | 'di_chart' | 'puzzle',
        'context'        : str,                 # shared instruction (singular Q)
        'passage_text'   : str | None,          # passage / cloze paragraph(s)
        'passage_bold'   : bool,                # True to match reference layout
        'table'          : TableSpec | {'headers': [...], 'rows': [[...]]} | None,
                           # v5.32: TableSpec (S1-8a) carries spans; the legacy
                           # {'headers','rows'} form still works unchanged.
        'chart_image'    : bytes | None,        # PNG, 300 DPI
        'ask'            : str,                  # this member's specific question
      }
      """
      # LINE 1 — Q.N + shared context (BOLD). Nothing may precede this.
      add_qn_context(doc, qnum, group['context'])

      # LINE 2 — the embedded stimulus (identical across members; SC-6 exempts
      #          intra-group repeats from R3/table-dedup).
      if group['mode'] in ('passage', 'cloze') and group.get('passage_text'):
          pp = doc.add_paragraph()
          rr = pp.add_run(group['passage_text'])   # full paragraph, all blanks
          rr.bold = bool(group.get('passage_bold', False))
          rr.font.name = FONT_NAME; rr.font.size = Pt(FONT_SIZE_PT)
      elif group['mode'] == 'di_table' and group.get('table'):
          build_di_table_styled(doc, group['table'])          # §8-S8-4 (v5.32)
      elif group['mode'] == 'di_chart' and group.get('chart_image'):
          insert_chart_image(doc, group['chart_image'])        # §8-S8-5
      elif group['mode'] == 'puzzle' and group.get('passage_text'):
          pp = doc.add_paragraph()
          rr = pp.add_run(group['passage_text'])
          rr.bold = bool(group.get('passage_bold', False))
          rr.font.name = FONT_NAME; rr.font.size = Pt(FONT_SIZE_PT)

      # LINE 3 — the specific ask (BOLD, non-numbered).
      add_specific_ask(doc, group['ask'])
  ```

  USAGE in S4-7 STEP A (per member, ascending Q order):
  ```python
  for q in batch_questions:
      if q.linked_group_id:
          g = dict(context_store[q.linked_group_id]); g['ask'] = q.ask
          add_linked_stimulus(doc, q.num, g)       # Q.N context → stimulus → ask
      else:
          add_question_stem(doc, q.num, q.stem)    # S10-3 (single Q — also Q.N first)
      add_text_options(doc, q.options)             # S10-3 (normal weight)
      doc.add_paragraph()                          # blank separator (R13)
  ```

  Q.N-FIRST INVARIANT: in BOTH branches the first paragraph of the block is a
  "Q.<N>" paragraph. No stimulus is ever emitted before it. Verified by
  G-QNUM-FIRST.

  MODEL B EXCEPTION: if delivery.linked_mode == "group" (confirmed at S3), emit
  one "Q.<X>  [GROUP: Q.X–Q.Y] <context>" line + stimulus once, then the members'
  asks bound by group_id. Default is ALWAYS "embed" (Model A).

## S10-5, S10-6, S10-9, S10-10 — (unchanged from v1.0 — see v1.0 for full spec)

## S10-6A — FIGURE CLASS TAXONOMY (v5.33 — new, GAP-2026-07-29-FIG-R2 §7.1)

  Every figure MUST declare exactly ONE class before it is drawn. Class selects
  the renderer, the palette policy, the sizing profile and which gates apply.

  | Class | Description | Renderer | Palette | Colour gate |
  | :--- | :--- | :--- | :--- | :--- |
  | `data_series` | ≥2 comparable series (line, scatter, grouped bar) | figural_core | Okabe-Ito, ≥2 hues | REQUIRED |
  | `data_single` | one series (single curve, single bar set) | figural_core | 1 accent hue permitted | not required |
  | `schematic` | pathway, apparatus, circuit, pedigree, structure | figural_core | ≥1 accent for the item under interrogation | not required |
  | `reasoning_glyph` | matrix / series / odd-one-out / figure-completion | S10-7 glyph path | MONOCHROME, mandatory | must be monochrome |
  | `option_canvas` | one MCQ option | inherits the parent question's class | inherits | inherits |

  CLASS INFERENCE PRECEDENCE: (1) declared in the FigureSpec, (2) measured from
  the draw call (series count), (3) keyword match on the stem. Declared always
  wins. If inference yields no class that is a HARD failure — NEVER a default.
  A defaulted class is how a scientific data figure ended up on the geometry
  path in the first place.

  `reasoning_glyph` MUST remain monochrome. Colour in an abstract-reasoning item
  can leak the answer: if the correct option carries any distinct colour
  treatment the item is void. The single permitted exception is a designated
  accent for a MISSING-ELEMENT marker (the "?" cell), which is identical across
  all options and therefore leaks nothing.

  TWO RENDERERS, ONE CONTRACT. `render_figural_image()` below is a geometry-glyph
  renderer — equal aspect, axes off, uniform square canvas. It is correct for
  `reasoning_glyph` and `option_canvas` and MUST NOT be used for the three data
  classes: it has no axis, tick, legend or font API and structurally cannot
  label a scientific figure. Those classes route to
  `figural_core.render_figure()`. Both obey S10-7 Q1–Q9 and S10-8.

## S10-7 — FIGURAL IMAGE-QUALITY CONTRACT (v5.33 — colour, labels, scale)

  Every figural raster must be reference-grade and online-renderable. This
  section is the executable home that S7-NEW-B Option A / S8-6 reference. The bar
  is PERFECT line-art quality: crisp at display size, uniform across options, no
  question chrome inside the pixels — AND, from v5.33, legible at the size it is
  actually printed and readable in greyscale and to a colour-blind reader.

  RUNTIME DEPENDENCIES (v5.33). This section needs more than Step 0's
  python-docx. figural_core.DEPENDENCIES declares the surface and
  figural_core.preflight() reports it; both are checked, never assumed.
    matplotlib  REQUIRED to render. render_figure() raises FiguralError
                G-FIGDEP carrying the pip command, not a bare ImportError from
                three frames down.
    pillow      required for the pixel gates (PNG size, DPI, colour presence)
    numpy       required for the pixel gates
    scipy       optional — advisory label estimate only
    fonttools   optional — tofu detection only
  ABSENCE NEVER HALTS AN AUDIT. Every gate degrades to DORMANT-but-reported and
  routes to AMBER: a gate that raises is worse than a gate that is absent,
  because it takes the whole audit down, and an audit that dies takes ~200
  projects with it. Guards import the module and catch failure rather than
  asking whether it is on the path — a package can be installed and still fail
  to load, and presence-checking leaves exactly the traceback the guard exists
  to prevent.

  FRAMEWORK CONSTANTS (do NOT read these from section_rules — they are universal;
  they are DEFINED in figural_core.py and mirrored here for reference only):
  ```python
  FIGURAL_DPI            = 300  # savefig dpi — minimum, never below
  FIG_COLUMN_IN          = 6.0  # usable text column, A4/Letter at 1in margins
  FIG_PROBLEM_DISPLAY_IN = 4.0  # on-page width of the problem/series figure
                                # (was 2.3 — too narrow to carry a labelled axis)
  FIG_OPT_DISPLAY_IN     = 1.3  # on-page side of EACH option (uniform square)
  FIG_NATIVE_HEADROOM    = 1.0  # RETIRED. Was 2.0 and was the whole of RC-2.
                                # MUST stay 1.0 and MUST NOT appear in placement
                                # arithmetic. At 300 dpi the supersample bought
                                # nothing and halved every label.
  FIG_MIN_STROKE_PT      = 1.4  # minimum line width
  ```

  QUALITY RULES (all mandatory — each is checked at view-tool verification):
    Q1. VECTOR-FIRST. Build every figure from geometry (matplotlib Rectangle /
        Circle / Polygon / Line, or an SVG path), then rasterise. NEVER screenshot,
        NEVER upscale a small bitmap, NEVER trace by hand in text.
    Q2. LOSSLESS PNG ONLY. Save as PNG. JPEG is BANNED for line art (ringing
        artefacts on edges). Background MUST be OPAQUE WHITE
        (facecolor="white", transparent=False) for every figure in every mock.
        v5.33: transparent RGBA is no longer permitted, and is no longer the
        stated preference. Transparent backgrounds render as invisible or
        near-invisible text in dark-mode and shaded-background viewers, and the
        alpha channel measured constant-255 on all 208 delivered drawings
        anyway — it was pure overhead. Prefer RGB over RGBA when alpha is
        constant.
    Q3. 300 DPI, NO HEADROOM, DETERMINISTIC CANVAS. Save at FIGURAL_DPI with
        figsize == the display size in inches, so
            saved_px == display_in × FIGURAL_DPI    (exactly)
        and the placement scale S is 1.0 by construction.
        v5.33 supersedes the old headroom rule, which said "render native pixels
        ≥ FIG_NATIVE_HEADROOM × the display pixel size" and then, in the same
        rule, gave two incompatible floors for the same 1.3 in option (780 px,
        then "≥ ~450 px and prefer ~600+"). The headroom was applied to the
        canvas and never compensated in the font size, so every label was
        printed at 1/headroom of its requested size — measured S = 0.500 exactly
        on 24 of 24 option canvases. At 300 dpi the supersample bought nothing
        that 300 dpi does not already provide, and Word's downsampling filter is
        unspecified. There is now ONE floor: 300 dpi at display size.
        `bbox_inches="tight"` is BANNED on every figure path. Tight trimming
        makes the saved width a function of the figure's own CONTENT — label
        length, legend overflow — so S becomes an uncontrolled variable: 27
        distinct canvas sizes across 31 delivered problem figures, S wandering
        0.495–0.666. Use `constrained_layout=True`, which gives the same good
        margins with a size that is known before the file is written.
    Q4. UNIFORM OPTION CANVAS. All N option images of a question share ONE square
        canvas size. Do NOT tight-crop options (tight crop yields non-uniform
        sizes). Fix the axes to [0,1]×[0,1], equal aspect, axis off, draw an
        explicit border box, and save with a fixed pad. (The problem figure MAY be
        a different, wider unit and MAY use a tight bbox.)
    Q5. NO QUESTION CHROME IN PIXELS. The stem, caption, instruction, and the
        option numbers (1/2/3/4) are DOCUMENT TEXT, never inside a raster.
        INTRINSIC figure annotations ARE allowed (mirror-line endpoints M/N,
        geometry vertices A/B/C, axis tick labels) — they label the figure itself.
    Q6. REAL REFERENCE GEOMETRY. A mirror line, fold line, number line, or axis is
        DRAWN as an actual line/curve. Never represent a line by two floating
        letters (the M1 "MN" defect).
    Q7. CONSISTENT STROKE + FILL. Line width ≥ FIG_MIN_STROKE_PT, antialiasing
        ON, and the SAME STROKE WEIGHT AND STYLE BUDGET across a question's
        option set so the options read as a matched set. A stroke or size
        difference between options is an answer cue; this clause is a
        correctness safeguard, not a cosmetic one, and must survive any future
        edit to this rule.
        v5.33: the words "solid black" are REMOVED. They were the whole of RC-1
        — the monochrome output measured across 55 delivered figures was
        CONFORMANT to this rule as previously written. Colour policy is now Q7b
        and is selected by the S10-6A class. `reasoning_glyph` and its option
        canvases remain monochrome under Q7b.7.
    Q7b. COLOUR AND REDUNDANT ENCODING (v5.33 — new).
        1. Palette MUST be Okabe-Ito unless overridden by
           `exam_config.figure_palette`:
           #0072B2 #D55E00 #009E73 #CC79A7 #E69F00 #56B4E9 #F0E442 #000000
           (colour-blind safe across deuteranopia/protanopia/tritanopia, print
           safe, 8 hues). Defined once in figural_core.OKABE_ITO.
        2. COLOUR MUST NEVER BE THE SOLE CARRIER OF MEANING. Every series MUST
           differ from every other series in at least ONE additional channel:
           line style, marker shape, or hatch pattern. This is what makes a
           figure survive greyscale printing and a colour-blind reader even if
           the palette is overridden. Gate G-FIGSERIES.
        3. Any two DECLARED series colours MUST remain separable after a
           deuteranope transform (≥ DEUT_MIN_SEP summed channel units).
           v5.33 NOTE — there is deliberately NO LUMINANCE CLAUSE. GAP-R2 §7.3.3
           demanded ≥20/255 luminance separation while §7.3.1 mandated
           Okabe-Ito, and the two are mutually unsatisfiable: over the 10 pairs
           of the first five Okabe-Ito hues the deuteranope clause passes 10/10
           and the luminance clause fails 3/10 (blue/bluish-green 18.6,
           vermillion/bluish-green 13.0, purple/orange 11.0). Okabe-Ito is
           CVD-safe by design; it was never greyscale-LUMINANCE-safe, and no
           8-hue palette can be both. GREYSCALE SURVIVAL IS DELIVERED BY Q7b.2
           REDUNDANT ENCODING, gated by G-FIGSERIES — not by a luminance
           threshold. Gating it twice made the check fire 569 times across 144
           conformant figures.
           The gate reads the DECLARED colours, never extracted pixels.
           Quantised onto a 32-step cube the mandated blue and bluish-green
           separate by 57 instead of their true 60.6 and the check fired on its
           own palette; that is measurement error reported as a defect. Gating
           the declaration is exact and reproducible, which also settles the
           method-sensitivity problem (the same exhibits measured two ways gave
           48 % and 70 % collapse). Whether the RENDER honoured the declaration
           is a separate question answered by G-FIGCOLOUR's hue COUNT.
        4. Pie, donut and area charts MUST label segments DIRECTLY ON THE MARK.
           A legend as the sole key is prohibited for these types.
        5. #F0E442 (yellow) MUST carry a dark edge when used as a fill.
        6. Colour MUST NOT correlate with correctness in an option set. All
           options in a set MUST use an identical style budget. (The delivered
           uniform 780×780 option canvases were CORRECT on this point and the
           property must be preserved.)
        7. Class `reasoning_glyph` MUST be monochrome apart from a declared
           missing-element accent. Gate G-FIGMONO.
    Q8. GEOMETRY ONLY + CANONICAL NAME (v4.3, R-MATH-OMML). The figural raster
        path renders GEOMETRIC FIGURES ONLY — never an algebraic/symbolic
        expression (those are OMML, §10-S10-4). Every emitted image MUST be named
        by the canonical convention so the audit can tell a figure from a stray
        raster:
          • problem/series figure : "q{N}_problem.png"  (or "q{N}_problem_{k}.png")
          • option figure         : "q{N}_opt{i}.png"   (i = 1..n_options)
          • linked-stimulus chart : "q{N}_stim.png"     (or "q{N}_stim_{tag}.png")
        Any other inline-image name (e.g. "q{N}_e1.png" for a rasterised
        expression) is an UNAUTHORISED raster and fails gate G-MATH-RASTER.
        render_figural_image() calls assert_not_math() on the figure's name/label
        and HARD-STOPS if handed a math expression.
    Q8b. SEVERITY — NO COLOUR CONDITION MAY EVER HALT A RUN (v5.33, owner
        directive). This is not a concession to convenience; it is this
        framework's own doctrine, stated in CLAUDE.md: "A CLASS T failure must
        be LOUD, and must NOT halt. These are separate properties and the corpus
        conflated them... Silence is the defect; a halt is not the remedy." A
        grey figure is a DEGRADED paper, never a void one. Three modes, defined
        in figural_core.SEVERITY:
          AMBER      — report at FAIL severity, force the amber delivery footer
                       (Framework_DeliveryFooter §5), ALWAYS complete. Every
                       colour and accessibility condition lives here:
                       G-FIGCOLOUR, G-FIGCVD, G-FIGSERIES, G-FIGGLYPH,
                       G-FIGALT, W-FIGLABELPX.
          VOID_ITEM  — the rendering leaks an ANSWER CUE, so this QUESTION is
                       invalid: G-FIGMONO (colour in a reasoning glyph),
                       G-FIGOPTUNIF (option canvases not uniform). Drop or
                       regenerate the single question. The paper continues.
                       Never halts the run.
          BLOCKING   — reserved for RENDERER-CONTRACT REGRESSION on v5.33+
                       output only: G-FIGSCALE, G-FIGLABEL, G-FIGDPI,
                       G-FIGDEGEN. These are safe to block ONLY because they are
                       unfireable by construction — verified 0 firings across
                       144 figures spanning 1.3–7.5 in, 2–8 series and four
                       label sets including full scientific notation. A firing
                       means someone reintroduced headroom or a tight bbox.
        EC-V18 LEGACY TOLERANCE, NON-NEGOTIABLE: output with no FigureSpec
        sidecar predates v5.33. Every BLOCKING gate downgrades to AMBER for it,
        so roughly 200 existing exams keep auditing and delivering untouched
        while still reporting the defect loudly. figural_core.triage() NEVER
        raises and NEVER halts.
    Q9. LABEL CONTRACT (v5.33 — new). The property the owner actually
        complained about, and the one no rule previously covered.
        1. ON-PAGE LABEL FLOORS, AT DISPLAY SIZE — not on the native canvas:
             data_series / data_single / schematic : 9 pt
             reasoning_glyph / option_canvas       : 8 pt
             target for all classes                : 10 pt
           axis titles ≥ tick labels. A floor declared on the native canvas is
           NOT this rule and does not satisfy it: under the pre-v5.33 contract a
           canvas-side floor was still halved at placement.
        2. Every axis MUST carry a title, including UNITS where the quantity is
           dimensional.
        3. Every series MUST be identified either by a direct label adjacent to
           the mark, or by a legend — and where a legend is the SOLE key, Q7b.2
           applies with no exception.
        4. The figure font MUST cover the exam's glyph set, at minimum:
           `µ ⁻² ₂ Å ° α β θ × ⇌ ≥ ≤ ‰ Δ λ`. A missing glyph renders as a tofu
           box and is a HARD failure. Gate G-FIGGLYPH.
        5. Every drawing MUST carry `wp:docPr/@descr` alt text naming the
           question number, the figure class and the quantities plotted.
           Measured 0 of 208 on the delivered exhibits. Emitted by S10-8 from
           `figural_core.alt_text()`. Gate A-FIGALT (AMBER — never halts).
        6. HOW THIS IS GATED. G-FIGLABEL is ARITHMETIC over the font sizes
           ACTUALLY USED at render time, recorded into the FigureSpec sidecar,
           multiplied by the recorded placement scale. It MUST NOT be gated on
           pixel connected components. Verified counter-example: three renders
           at an identical 10 pt request, identical 1304 px saved width and
           identical scale — the one whose axis titles carried
           "µmol photons m⁻² s⁻¹" and "Net CO₂ assimilation" measured 8.5 pt
           while short-label renders measured above the floor. Superscripts and
           subscripts are small connected components that drag the median down,
           so a pixel gate is biased against exactly the notation Q9.4
           mandates, and would fail conformant chemistry, biology and physics
           papers hardest. The pixel statistic is retained as a WARN-level
           cross-check only (`figural_core.g_figlabel_pixels`).

  RENDER HELPER — WHICH ONE (v5.33).
    Classes `data_series`, `data_single`, `schematic` route to
    `figural_core.render_figure()`. Classes `reasoning_glyph` and
    `option_canvas` (when the parent is a reasoning glyph) use
    `render_figural_image()` below.
    ```python
    import figural_core as fc

    spec = fc.make_figure_spec(qnum, "data_series", fc.FIG_PROBLEM_DISPLAY_IN,
                               series=fc.series_defaults(2),
                               axes={"x": {"title": ..., "units": ...},
                                     "y": {"title": ..., "units": ...}},
                               key_mode="legend")
    fc.render_figure(draw_fn, png_path, spec)   # MUTATES spec with png_px,
                                                # png_dpi, placed_in,
                                                # placement_scale, font_pt_native
    fc.write_spec_sidecar(spec, png_path)       # the audit reads this
    ```
    `render_figure()` reads the saved artefact back and records what actually
    happened. The audit then verifies the figure WITHOUT looking at it: colour
    presence, hue count, luminance and deuteranope separation, placement scale,
    on-page label size, DPI metadata and alt text are all deterministic
    arithmetic over the PNG and its sidecar. Only "does this render actually
    DEPICT a micrograph" needs eyes, and that alone remains CLASS T.

  GEOMETRY-GLYPH HELPER (returns lossless PNG bytes; one call per visual unit):
  ```python
  import io
  import matplotlib
  matplotlib.use("Agg")
  import matplotlib.pyplot as plt

  def render_figural_image(draw_fn, kind="option", *, name="", bg="transparent"):
      """
      draw_fn(ax) draws ONE visual unit using geometry only (no stem/option text).
      kind = "option"  -> uniform fixed square canvas (no tight crop); boxed.
      kind = "problem" -> single wider unit; tight bbox allowed.
      name = the canonical image name (Q8): q{N}_problem[_k] / q{N}_opt{i} /
             q{N}_stim[_tag]. REQUIRED so the audit name-contract is satisfiable.
      Returns PNG bytes at FIGURAL_DPI with headroom. Caller embeds at the
      display size below (so the on-page image is supersampled = crisp).
      """
      # v4.3 R-MATH-OMML HARD STOP: the figural path is geometry-only. A built-up
      # algebraic expression must NEVER be rasterised — route it to OMML (S10-4).
      assert_not_math(name)
      transparent = (bg == "transparent")
      if kind == "option":
          # v5.33: figsize == the display size, EXACTLY. The old line was
          #   side_in = max(FIG_OPT_DISPLAY_IN * FIG_NATIVE_HEADROOM, 2.0)
          # which, with headroom retired to 1.0, resolves to max(1.3, 2.0) = 2.0in
          # while placement is still 1.3in — S = 0.65 and gate A-FIGSCALE fires
          # BLOCKING on every option canvas. The 2.0 floor was a residue of the
          # old Q3, which gave two incompatible pixel floors in one rule.
          side_in = FIG_OPT_DISPLAY_IN
          fig, ax = plt.subplots(figsize=(side_in, side_in))
          ax.set_xlim(0, 1); ax.set_ylim(0, 1)
          ax.set_aspect("equal"); ax.axis("off")
          from matplotlib.patches import Rectangle
          ax.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, fill=False,
                                  lw=FIG_MIN_STROKE_PT, edgecolor="black"))
          draw_fn(ax)
          buf = io.BytesIO()
          # v5.33 Q2: opaque white, always. `transparent` is retained in the
          # signature for call compatibility and deliberately ignored.
          plt.savefig(buf, format="png", dpi=FIGURAL_DPI, transparent=False,
                      bbox_inches=None, pad_inches=0, facecolor="white")
      else:  # problem / series unit
          # v5.33: figsize == the display size and bbox_inches=None, so
          # saved_px == display_in x FIGURAL_DPI exactly and S == 1.0.
          # This branch previously multiplied by FIG_NATIVE_HEADROOM and saved
          # with bbox_inches="tight" — the two halves of RC-2 in three lines.
          # Tight trimming made the saved width a function of the drawing's own
          # content, which is why 31 delivered problem figures produced 27
          # distinct canvas sizes and S wandered 0.495-0.666.
          fig, ax = plt.subplots(figsize=(FIG_PROBLEM_DISPLAY_IN,
                                          FIG_PROBLEM_DISPLAY_IN * 0.8))
          ax.set_aspect("equal"); ax.axis("off")
          draw_fn(ax)
          buf = io.BytesIO()
          plt.savefig(buf, format="png", dpi=FIGURAL_DPI, transparent=False,
                      bbox_inches=None, pad_inches=0,
                      facecolor="white")
      plt.close(fig)
      buf.seek(0)
      return buf.read()

  def assert_uniform_options(option_pngs):
      """All option images MUST be the same native pixel size (Q4)."""
      from PIL import Image
      sizes = {Image.open(io.BytesIO(b)).size for b in option_pngs}
      if len(sizes) != 1:
          raise AssertionError(f"G-FIGURAL option canvases not uniform: {sizes}")
  ```

## S10-8 — FIGURAL PLACEMENT (v4.0 — single-column, label-bound; was a v1.0 stub)

  Lays a figural MCQ into the docx as DISCRETE images. Enforces R-FIGURAL: stem is
  Q.N-first document text (R14); problem image(s) next; then the option images
  stacked ONE PER LINE, each bound 1:1 to its "i." label. There is exactly one
  image per option line — never two options on a line, never a table row of
  options, never a composite panel.

  ```python
  from docx.shared import Inches, Pt
  import figural_core                     # v5.33 — alt_text() (S10-7 Q9.5)

  def _add_image_para(doc, png_bytes, width_in, spec=None):
      """Add a paragraph that holds EXACTLY ONE inline image (single-column).

      v5.33: width_in MUST come from the FigureSpec that rendered this PNG
      (spec['placed_in']), never from a bare configuration constant. Under
      v5.32 this function was called as _add_image_para(doc, pb,
      FIG_PROBLEM_DISPLAY_IN) — a fixed 2.3 in against a canvas that had been
      supersampled to 2x — which is what produced S = 0.500 on 24 of 24 option
      canvases. The width and the canvas MUST come from the same record.

      NOTE the direction of the fix. Display width stays a LAYOUT decision;
      Q3 makes the render match it. Deriving the width from the artefact
      instead (D := min(native, column)) was measured and REJECTED: it inflates
      figure area 1.84x and gives a four-option MCQ a 10.4 in option stack
      against a ~9.0 in page text height, breaking every such question across a
      page boundary with its options orphaned from the stem.
      """
      if spec is not None:
          width_in = spec["placed_in"]
      p = doc.add_paragraph()
      run = p.add_run()
      run.add_picture(io.BytesIO(png_bytes), width=Inches(width_in))
      if spec is not None:
          _set_last_drawing_alt(doc, figural_core.alt_text(spec))   # Q9.5
      return p

  def _set_last_drawing_alt(doc, descr):
      """Stamp wp:docPr/@descr on the most-recently added inline drawing (Q9.5).
      Measured 0 of 208 delivered drawings carried alt text."""
      from docx.oxml.ns import qn
      last = None
      for d in doc.element.body.iter(qn('w:drawing')):
          last = d
      if last is None:
          raise AssertionError("no inline drawing to describe")
      for dp in last.iter(qn('wp:docPr')):
          dp.set('descr', descr)

  def _name_last_drawing(doc, name):
      """Stamp the canonical figural name (S10-7 Q8) onto the most-recently added
      inline drawing — both wp:docPr and pic:cNvPr — so gate G-MATH-RASTER
      recognises it as a legitimate figure. python-docx's add_picture leaves a
      generic 'Picture N' name, which the name-contract would (correctly) reject."""
      from docx.oxml.ns import qn
      last = None
      for d in doc.element.body.iter(qn('w:drawing')):
          last = d
      if last is None:
          raise AssertionError("no inline drawing to name")
      for dp in last.iter(qn('wp:docPr')):
          dp.set('name', name)
      for cp in last.iter(qn('pic:cNvPr')):
          cp.set('name', name)

  def add_figural_question(doc, qnum, stem, problem_pngs, option_pngs,
                           problem_label="Problem Figure:",
                           problem_specs=None, option_specs=None):
      """
      qnum         : int
      stem         : str   — the question instruction (DOCUMENT text, Q.N-first)
      problem_pngs : [bytes] — 1+ problem/series images (geometry only)
      option_pngs  : [bytes] — EXACTLY n_options images, in option order, uniform
      Layout (R-FIGURAL / R14 / G-QNUM-FIRST):
        Q.N stem  →  "Problem Figure:"  →  problem image(s)
                  →  for i in 1..N:  "i."  then ONE option image (own line)
                  →  blank separator
      v4.3: every emitted image is stamped with its canonical name (S10-7 Q8) —
        q{N}_problem[_k] / q{N}_opt{i} — so it passes the G-MATH-RASTER name-
        contract; a rasterised expression (e.g. q{N}_e1) never carries such a name.
      """
      # 1:1 binding + uniform canvas are HARD invariants (G-FIGURAL-COMPOSITE).
      assert len(option_pngs) >= 2, "figural MCQ needs ≥2 option images"
      assert_uniform_options(option_pngs)

      # LINE 1 — Q.N stem (BOLD, configured font) — Q.N FIRST, no image precedes it.
      add_question_stem(doc, qnum, stem)            # S10-3

      # Problem figure(s): a text label (NOT baked into the image) + the image(s).
      if problem_pngs:
          lab = doc.add_paragraph(); r = lab.add_run(problem_label)
          r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
          for k, pb in enumerate(problem_pngs, 1):
              _add_image_para(doc, pb, FIG_PROBLEM_DISPLAY_IN,
                              spec=problem_specs[k - 1] if problem_specs else None)
              nm = f"q{qnum}_problem.png" if len(problem_pngs) == 1 \
                   else f"q{qnum}_problem_{k}.png"
              _name_last_drawing(doc, nm)           # canonical name (S10-7 Q8)

      # Options: SINGLE COLUMN — one option per line, label bound to its image.
      for i, opt_png in enumerate(option_pngs, 1):
          lp = doc.add_paragraph()                  # the "i." label line
          lr = lp.add_run(f"{_option_label(i)}.")     # option label (configured format)
          lr.bold = False; lr.font.name = FONT_NAME; lr.font.size = Pt(FONT_SIZE_PT)
          _add_image_para(doc, opt_png, FIG_OPT_DISPLAY_IN,
                          spec=option_specs[i - 1] if option_specs else None)
          _name_last_drawing(doc, f"q{qnum}_opt{i}.png")      # canonical name (Q8)

      add_blank_separator(doc)                       # R13

  # USAGE (per figural question, from S8-6):
  #   prob = render_figural_image(draw_problem, kind="problem")
  #   opts = [render_figural_image(lambda ax: draw_option(ax, k), kind="option")
  #           for k in range(n_options)]
  #   add_figural_question(doc, q.num, q.stem, [prob], opts)
  ```

  SINGLE-COLUMN INVARIANT: because every option image is added in its own
  paragraph and options are NEVER placed in a table row or shared paragraph, no
  line ever carries more than one option. Verified by G-FIGURAL-COMPOSITE.

  COMPOSITE BAN: a figural block that contains only ONE image (problem + options
  fused) is a hard defect — the online engine renders one option region per screen
  and cannot slice a baked panel, and the figures are decoupled from their labels.
  G-FIGURAL-COMPOSITE fails any figural block with < (n_options + 1) images.

## S10-8A — FIGURAL STEM placement helper (v5.13 — stem_only variant)

  Handles format=FIGURAL + image_role='stem_only' MCQ: the problem/series
  figure(s) are images, but the options are TEXT (numbers, words, phrases).
  E.g., "How many triangles are in the given figure?" with text options.

  ```python
  def add_figural_stem_question(doc, qnum, stem, problem_pngs, text_options,
                                problem_label="Problem Figure:"):
      """
      qnum         : int
      stem         : str   — the question instruction (DOCUMENT text, Q.N-first)
      problem_pngs : [bytes] — 1+ problem/series images (geometry only, 300 DPI)
      text_options : [str]  — text option strings (NOT images)
      Layout (R-FIGURAL stem_only / R14 / G-QNUM-FIRST):
        Q.N stem  →  "Problem Figure:"  →  problem image(s)
                  →  text options via add_text_options()
                  →  blank separator
      v5.13: new helper for the stem_only variant. Figural questions where only the
      stem has a visual element and options are text. Without this helper, the only
      path was add_figural_question() which HARD ASSERTs option images.
      """
      assert len(problem_pngs) >= 1, "stem_only figural MCQ needs ≥1 problem image"
      assert len(text_options) >= 2, "MCQ needs ≥2 text options"

      # LINE 1 — Q.N stem (BOLD, configured font) — Q.N FIRST, no image precedes it.
      add_question_stem(doc, qnum, stem)                # S10-3

      # Problem figure(s): a text label (NOT baked into the image) + the image(s).
      lab = doc.add_paragraph(); r = lab.add_run(problem_label)
      r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
      for k, pb in enumerate(problem_pngs, 1):
          _add_image_para(doc, pb, FIG_PROBLEM_DISPLAY_IN)
          nm = (f"q{qnum}_problem.png" if len(problem_pngs) == 1
                else f"q{qnum}_problem_{k}.png")
          _name_last_drawing(doc, nm)                   # canonical name (S10-7 Q8)

      # Options: TEXT, not images. Standard text option placement.
      add_text_options(doc, text_options)                # S10-3

      add_blank_separator(doc)                           # R13

  # USAGE (per stem_only figural question, from S8-6):
  #   prob = render_figural_image(draw_problem, kind="problem")
  #   add_figural_stem_question(doc, q.num, q.stem, [prob], text_options)
  ```

  WHEN TO USE THIS vs add_figural_question():
    add_figural_question()       → image_role in ('stem_and_options', 'options_only')
    add_figural_stem_question()  → image_role == 'stem_only'
  The FORMAT DISPATCH in S4-7 STEP A makes this decision per question.
  The dispatch reads image_role from section_rules PYQ_IMAGE_ANALYSIS.


# ════════════════════════════════════════════════════════════════════════
# §11 — ANSWER KEY SIDECAR (v2.0 — PER-QUESTION WRITE ENFORCED)
# ════════════════════════════════════════════════════════════════════════

## S11-1 — Format

  ```json
  {"answers": {"1": 2, "2": 4, ...}, "sources": {"Q_num": {...}}}
  ```
  File: [ExamCode]_M[N]_answer_key.json

## S11-2 — Incremental build (v2.0 GAP-18 fix — one write per question)

  Called from S7-NEW-A after EVERY question accepted.
  NEVER reconstructed from memory at batch end or mock end.
  NEVER embedded in docx body (R5 violation if so).

## S11-3 — Source logging for ALL GA facts (not just CA)

  All fact-recall questions: log source citation (authoritative academic,
  government, or official sources relevant to the exam's domain).
  CA questions: additionally log event_date and ca_window.

## S11-4 — Answer key NEVER in docx (v2.0 GAP-17 — detection added)

  PRE-DELIVERY DETECTION:
  ```python
  def check_no_answer_key_in_docx(docx_path):
      from docx import Document
      doc = Document(docx_path)
      answer_key_patterns = [
          r'(?i)answer\s*key',
          r'(?i)answers\s*:',
          r'(?i)^key\s*:',
          # v4.5: single-digit AND set-valued (comma/space list) keys. The v4.4 patterns
          # matched only one digit, so a leaked MSQ key "Q.1 → 1,2,4" slipped through.
          r'Q\.\d+\s*[→:]\s*[1-9](?:\s*[,\s]\s*[1-9])*',  # "Q.1 → 2" or "Q.1 → 1,2,4"
          r'\b\d+\.\s*[→:]\s*[1-9](?:\s*[,\s]\s*[1-9])*',  # "1. → 2" or "1. → 1,2,4"
          # v4.7: NAT numerical-value answer-key lines. The MSQ/MCQ patterns above only
          # match option digits 1-9, so a leaked NAT key "Q.5 → 47", "Q.5 → 0", "Q.5 → -3"
          # or "Q.5 → 3.14" would slip through. Match a signed integer or decimal value.
          r'Q\.\d+\s*[→:]\s*-?\d+(?:\.\d+)?\b',            # "Q.5 → 47" / "→ -3" / "→ 3.14"
          r'\b\d+\.\s*[→:]\s*-?\d+(?:\.\d+)?\b',           # "5. → 47" / "→ -3" / "→ 3.14"
      ]
      import re
      for i, para in enumerate(doc.paragraphs):
          text = para.text.strip()
          for pattern in answer_key_patterns:
              if re.search(pattern, text):
                  print(f"R5 VIOLATION: Answer key detected in docx para {i}: '{text[:60]}'")
                  return False
      return True
  ```
  If this returns False → HARD STOP. Remove answer key from docx before delivery.

## S11-5 — K-INT verification (v5.4 — MSQ/NAT-aware)

  ```python
  kd  = json.load(open(answer_key_path))
  key = kd["answers"]
  cm  = kd.get("concept_map", {})
  options_count = int(kd.get("msq_meta", {}).get("total_options", 4))   # v5.5 FIX: was undefined
  assert len(key) == total_questions, f"K-INT FAIL: {len(key)} vs {total_questions}"
  for qn, val in key.items():
      at = cm.get(str(qn), {}).get('answer_type', 'option')
      ac = cm.get(str(qn), {}).get('answer_cardinality', 'single')
      if at == 'numerical':
          # NAT: val is a number or numeric string; range-check not applicable
          assert val is not None, f"K-INT FAIL: Q.{qn} NAT answer is None"
      elif ac == 'multi':
          # MSQ: val is a list of ints; each must be in 1..options_count
          assert isinstance(val, list) and len(val) >= 1, \
              f"K-INT FAIL: Q.{qn} MSQ answer not a non-empty list: {val}"
          for v in val:
              assert 1 <= v <= options_count, \
                  f"K-INT FAIL: Q.{qn} MSQ answer element {v} out of range"
      else:
          # Single-answer MCQ: val is an int in 1..options_count
          assert isinstance(val, int) and 1 <= val <= options_count, \
              f"K-INT FAIL: Q.{qn} answer={val}"
  ```

## S11-6 — Answer key correspondence gate

  Q numbers in docx must exactly equal keys in answer_key.json.

# ════════════════════════════════════════════════════════════════════════
# §12 — GUARD SCRIPT (all 80 gates — 39 v1.0 baseline + 29 added since v1.0
#        + 12 FIGURE CONFORMANCE added in v5.33 / Audit v2.11)
# ════════════════════════════════════════════════════════════════════════

## S12-0 — Zero-Warning Policy (unchanged)

  Every fixable WARN = blocker = same as FAIL.

## GATE ADDITIONS / CHANGES (v2.0):

  S12-NEW-1 — G-FONTCHECK:
    Scan all text runs in docx. Any run with font.name not in [FONT_NAME, None]
    (None = inherits configured font from default style) → Exit 1.
    Fixable: re-run generation with corrected add_*() helpers.

  S12-NEW-2 — G-OPTLABEL:
    Scan all option paragraphs. Option labels must match "^\d+\.\s{2}" pattern.
    If "(1)", "1)", "1. " (one space) found → Exit WARN.
    Fixable: regenerate with corrected add_text_options().

  S12-NEW-3 — G-SECTIONHDR:
    Scan all paragraphs before first Q.N paragraph.
    If any paragraph matches "SECTION:", "Section I", "Part A" etc. → Exit 1.
    Fixable: remove the offending paragraphs from docx.

  S12-NEW-4 — G-ANSWERKEY:
    Call check_no_answer_key_in_docx() (S11-4).
    If answer key patterns found → Exit 1 (HARD FAIL).
    Fixable: remove answer key section from docx.

  S12-NEW-5 — G-FIGTEXT (v5.13 — 3-tier expanded detection):

    TIER 1 — IMAGE COUNT PER FORMAT=FIGURAL SUBTOPIC (primary):
      For every subtopic in this mock whose section_rules format==FIGURAL:
        Locate the Q-block by question number (from concept_map in sidecar).
        Read image_role from PYQ_IMAGE_ANALYSIS (default 'stem_and_options').
        COUNT the <w:drawing> inline images in the block.
        Expected minimum image count per image_role:
          stem_and_options : n_options + 1 (problem + options) — existing check
          stem_only        : 1 (problem image(s) only; options are text)
          options_only     : n_options (option images only; no problem image)
        IF image_count < expected minimum:
          → Exit 1: "G-FIGTEXT: Q.[n] is format=FIGURAL (image_role=[role])
             but contains [k] image(s), expected ≥[min]. Render via matplotlib
             (S7-NEW-B OPTION A) or replace subtopic (OPTION B).
             Text descriptions of figures are BANNED (OPTION C)."
      IF concept_map or section_rules is unavailable for Tier 1:
        → WARN: "G-FIGTEXT-DEPS: concept_map or section_rules missing —
           Tier 1 image-count check SKIPPED. Only Tier 2/3 active."
        → In --final mode: escalate to FAIL (Final Assembly must have full check).

    TIER 2 — LEGACY BRACKET-PATTERN REGEX (secondary, unchanged):
      Scan ALL paragraphs for bracketed placeholder patterns:
        "[The figure shows...", "[Image: ...", "[Figure will be added",
        "text description:", "[Diagram:", "[Picture:"
      Any match → Exit 1: "G-FIGTEXT: Figural placeholder detected."

    TIER 3 — VISUAL PROSE DETECTOR (tertiary, v5.13):
      For every Q-block in the docx:
        IF the block contains 0 <w:drawing> inline images:
          Scan the block's text for FIGURE REFERENCE patterns:
            r"(?i)\b(in the given figure|in the following figure|
              from the (given|following) (figure|diagram)|
              figure \(X\)|the figure (shows|below|above)|
              how many .{0,30}(triangles|squares|circles|lines|shapes|
              angles|sides|regions|parts)\s+(are|in|does|can))"
          IF any match found:
            → Exit 1: "G-FIGTEXT-PROSE: Q.[n] references a figure but block
               contains 0 images. Render the figure (S7-NEW-B OPTION A,
               use add_figural_stem_question for text-option variants) or
               replace the subtopic entirely (OPTION B)."
        IF the block contains ≥1 image: skip Tier 3 for this block (no false positive).

    WHY THREE TIERS: Tier 1 catches format=FIGURAL subtopics rendered as prose
    (the production defect class — unbracketed text that Tier 2's regex missed).
    Tier 2 catches bracketed placeholder annotations in any format block. Tier 3
    catches format=TEXT subtopics that are inherently visual but were misclassified
    — it operates on CONTENT, not on format metadata, and fires only when text
    references a figure AND zero images exist in the block.
    Together they cover the full failure space across all image_role variants.
    Fixable: generate real images (OPTION A) or replace the subtopic (OPTION B).

  S12-NEW-6 — G-ALTGROUP (v4.4 — manifest-driven; replaces hardcoded G-CISINCHECK):
    Exam-agnostic alternation backstop to S3-17. Reads the Step-0 manifest's
    alternation_groups {group: [subtopic_id, ...]} and the mock's allocated
    subtopic_ids (the same id set S3-17 uses). For each group, if ≥2 of its
    members are present in this mock → Exit 1 (alternation violated), naming the
    group and the offending members via manifest display_name.
    ```python
    groups   = manifest.get('alternation_groups', {})
    mock_ids = set().union(*[set(m.keys()) for m in alloc_ids.values()]) if alloc_ids else set()
    for group, members in groups.items():
        present = [m for m in members if m in mock_ids]
        if len(present) > 1:
            disp = [manifest['subtopics'].get(m, {}).get('display_name', m) for m in present]
            sys.exit(f"G-ALTGROUP: Mock {N} — alternation group '{group}' has "
                     f"{len(present)} members present ({', '.join(disp)}); ≤1 allowed.")
    ```
    Empty alternation_groups ⇒ nothing to enforce ⇒ pass (no false stop).
    Zero hardcoded subtopic names. Fixable: drop the member that the blueprint
    parity assigns to the other mock, then regenerate (Step 7 does not auto-edit
    the blueprint).

  S12-NEW-24 — G-GROUPMANDATE (v5.0 — group-presence backstop, Issue 2b):
    Exam-agnostic post-gen backstop to S3-17 CHECK 3, mirroring G-ALTGROUP. Reads
    manifest.mandatory_groups {group: {members:[ids], min}} and the per-subtopic_id
    counts computed from the mock's concept_map (the SAME generated-reality counts
    G-ALLOC-SUBTOPIC uses — not merely the blueprint). For each group, if the number
    of members with ≥1 GENERATED question is < min → Exit 1.
    ```python
    groups = manifest.get('mandatory_groups', {})
    # counts[sid] = generated questions of that subtopic_id in this mock (from concept_map)
    for group, spec in groups.items():
        members = spec.get('members', [])
        need    = spec.get('min', 1)
        have    = sum(1 for m in members if counts.get(m, 0) > 0)
        if have < need:
            disp = [manifest['subtopics'].get(m, {}).get('display_name', m) for m in members]
            sys.exit(f"G-GROUPMANDATE: Mock {N} — group '{group}' has {have} of "
                     f"[{', '.join(disp)}] present; needs >={need}.")
    ```
    Empty mandatory_groups ⇒ pass. Fixable: regenerate so ≥min members appear
    (Step 1 RULE M4 should have guaranteed this in the blueprint).

  S12-NEW-25 — G-MINCOUNT (v5.0 — min-count backstop, Issue 2b):
    Exam-agnostic post-gen backstop to S3-17 CHECK 4. Reads manifest.min_counts
    {id: k} and the same per-subtopic_id generated counts. If any id has < k
    GENERATED questions → Exit 1.
    ```python
    for mid, k in manifest.get('min_counts', {}).items():
        c = counts.get(mid, 0)
        if c < k:
            disp = manifest['subtopics'].get(mid, {}).get('display_name', mid)
            sys.exit(f"G-MINCOUNT: Mock {N} — {mid} ('{disp}') has {c}Q generated; "
                     f"needs >={k}.")
    ```
    Empty min_counts ⇒ pass. NOTE: manifest.cadence_windows is intentionally NOT
    gated in Step 7 — cadence is cross-mock (see S3-17 note + Step 1 RULE M5).

  S12-NEW-7 — G-CONCEPTDUP (DOUBT-3 — scenario uniqueness, v3.2; v3.3 concept_map):
    Read the per-question concept_map from the answer_key sidecar
    ({q: {subtopic, concept_group, scenario_key}}). Group questions by
    scenario_key. If ANY scenario_key maps to more than one Q → Exit 1.
    Strict zero: same scenario twice (even with changed values/names/wording,
    even across two different subtopics) is banned. No tolerance band.
    (If concept_map is missing for any Q → Exit 1: generation did not record it;
     fix the generator, do not silently re-derive.)
    Fixable: regenerate the duplicate on a DIFFERENT scenario (never reduce the
    subtopic count to "fix" it).
    Report (MANDATE 0 — no content): "G-CONCEPTDUP: Q.[a] and Q.[b] share
    scenario_key 'op|shape'. Regenerate Q.[b] on a different scenario."

  S12-NEW-8 — G-ALLOC-SUBTOPIC (DOUBT-3 RULE A — per-subtopic exact count, v3.2):
    From the concept_map, count questions per subtopic and compare to
    blueprint.json subtopic_allocations[].q_count (=N).
    If any subtopic count != N → Exit 1 (HARD FAIL).
      count < N → missing questions; generate the remainder (distinct scenarios).
      count > N → over-generated; remove extras.
    This is distinct from S3-9 (which only checks SECTION totals). G-ALLOC-SUBTOPIC
    checks every individual subtopic.

  S12-NEW-9 — G-COUNT-X-UNIQUE (DOUBT-3 combined check, v3.2):
    The two rules verified TOGETHER at Final Assembly, both from concept_map:
      (i)  every subtopic has EXACTLY its blueprint q_count (RULE A), AND
      (ii) all scenario_keys mock-wide are pairwise distinct (RULE B),
           with the CLASS-4 exception that a shared linked-stimulus is allowed
           but each linked Q's sub_skill scenario_key is still distinct.
    A subtopic with the right count but a repeated scenario → FAIL.
    A subtopic with distinct scenarios but the wrong count → FAIL.
    Both conditions must pass for the mock to ship.

  S12-NEW-10 — G-STIMULUS-ORPHAN (v3.6 — linked self-containment, HARD STOP):
    Enforces R-LINKED / §9. Scans EVERY question block in the cumulative docx and
    verifies that any question depending on a shared stimulus physically carries
    that stimulus in its OWN block.
    ALGORITHM:
      Parse the docx into per-question blocks (a block = the bold "Q.<N>" stem
      paragraph + its following paragraphs/tables/images up to the next "Q.<N>").
      For each block:
        refs_stimulus = stem matches ANY of:
          r"the passage", r"the table", r"the graph", r"the chart",
          r"the given (data|information)", r"blank \(\d+\)",
          r"according to the passage", r"in the passage",
          r"Q\.\d+\s*(and|to|–|-)\s*Q\.\d+"   # cross-question dependence text
        has_stimulus = block contains a passage paragraph (≥25 words of prose)
          OR a Word table OR an inline image, attached to THIS block.
        # Cross-reference language ("Q.X and Q.Y") is itself a violation even if
        # a stimulus is present, because it implies a multi-question screen.
        if re.search(r"Q\.\d+\s*(and|to|–|-)\s*Q\.\d+", stem):  → Exit 1
        if refs_stimulus and not has_stimulus:                  → Exit 1
      ALSO (group completeness): build groups from the answer_key sidecar
      linked_group_id. For each group, every member block must independently
      satisfy has_stimulus (Model A) — UNLESS delivery.linked_mode == "group"
      (Model B confirmed), in which case exactly one "[GROUP n: Q.X–Q.Y]" preamble
      must bind the set and members may share. Any member missing its stimulus
      under Model A → Exit 1.
    NOT FIXABLE BY DELETION: the fix is to EMBED the stimulus into each member
    (re-run S4-7 STEP A with add_linked_stimulus, §10-S10-LINKED). Never "fix" by
    dropping the linked questions.
    Report (MANDATE 0 — no content): "G-STIMULUS-ORPHAN: Q.[n] references a
    stimulus not present in its own block (linked_group_id=[gid]). Embed the
    shared stimulus into Q.[n] (Model A) and re-check."

  S12-NEW-11 — G-QNUM-FIRST (v3.7 — Q.N-FIRST block contract, HARD STOP):
    Enforces R14 / R-LINKED Q.N-FIRST clause. Segments the cumulative docx into
    question blocks (a block runs from one "Q.<N>" paragraph to the next). For
    EACH block, the FIRST non-empty body element must be the "Q.<N>" paragraph
    itself — NOT a table, chart image, passage, or unnumbered preamble.
    ALGORITHM:
      Walk the body in document order (paragraphs AND tables interleaved).
      Track the element immediately following each inter-question boundary.
      For each question's opening element:
        if it is a table / image / non-"Q.<N>" paragraph  → Exit 1
        if it is a paragraph but does NOT match r"^\s*Q\.\d+\b"  → Exit 1
      ALSO: assert exactly one r"^\s*Q\.\d+\b" paragraph per block (R14); the
      specific-ask paragraph in a linked block must be NON-numbered.
    This catches the v3.6-style "stimulus/preamble before Q.N" layout and any
    stray second Q-number inside a block.
    NOT FIXABLE BY REORDERING ALONE if the Q-number is missing: re-emit the block
    via S10-LINKED (add_qn_context first → stimulus → add_specific_ask).
    Report (MANDATE 0 — no content): "G-QNUM-FIRST: block for Q.[n] opens with
    [table/passage/preamble], not 'Q.[n]'. Re-emit Q.N context line first."

  S12-NEW-12 — G-FORMATDUP (v3.8; v3.9 hardened — RULE C, HARD STOP):
    Enforces §6-3c. Reads the per-question concept_map from the answer_key
    sidecar. SELECTS questions by subtopic_class ∈ {CLASS2, CLASS3} (v3.9 G5 fix —
    NOT by "presentation_key not None", which would let a missing-key question, the
    exact failure case, escape). Groups the selected questions by concept_group.
    Let M = len(STEM_FORMAT_MENU[resolve_presentation_family(subtopic_data)]).
    ALGORITHM:
      for cg, qs in group_by(selected, key=concept_group):
          # missing-key guard (now reachable, because selection is class-based)
          for q in qs:
              if q.presentation_key is None or q.stem_format_variant is None:
                  → Exit 1  "G-FORMATDUP: Q.[q] (CLASS 2/3) has no presentation_key
                             — generator did not pick a defined stem_format_variant
                             + distractor_strategy (§6-3c)."
          # (C1) distinct VISIBLE format while count ≤ M
          if len(qs) <= M and len({q.stem_format_variant for q in qs}) < len(qs):
              → Exit 1  "G-FORMATDUP/C1: CONCEPT_GROUP '[cg]' reuses a
                         stem_format_variant across [n] questions (count ≤ menu
                         size [M]); each must use a different visible format."
          # (C2) distinct presentation_key always
          seen = {}
          for q in qs:
              pk = q.presentation_key
              if pk in seen:
                  → Exit 1  "G-FORMATDUP/C2: Q.[seen[pk]] and Q.[q] share
                             CONCEPT_GROUP '[cg]' AND presentation_key '[pk]'.
                             Regenerate Q.[q] on a different format/distractor."
              seen[pk] = q
    Strict zero: distinct target item (scenario_key) does NOT excuse an identical
    look. This is the gate that catches M1 Q.77/Q.79 and Q.78/Q.80.
    NOT FIXABLE BY DROPPING N: regenerate the offending question on a new
    stem_format_variant / presentation_key (§6-3c menus). Never reduce the count.
    Report is MANDATE-0 safe (no stem content — only Q numbers, concept_group,
    and menu tokens).

  S12-NEW-13 — G-FIGURAL-COMPOSITE (v5.13 — image_role-aware, HARD STOP):
    Enforces R-FIGURAL / §10-S10-8 / §10-S10-8A. For every FIGURAL question, the
    rendered block must be correctly structured per its image_role variant.
    IDENTIFY figural blocks: use the figural manifest q-list when present; else a
    block is figural if its stem matches the figural cue set
      r"(?i)(select|choose|which) .*figure|mirror image|water image|paper.?fold(ing)?|
            complete the (figure|series|pattern)|embedded figure|odd one out.*figure|
            problem figure|find the missing (figure|term).*(figure|pattern)"
      AND the block contains ≥1 inline image AND no Word table (tables ⇒ DI, not
      figural — excluded to avoid false positives on DI charts).
    ALGORITHM (v5.13 — per figural block; n_opt = option count, default 4):
      imgs_total   = count of <w:drawing> inline images in the block
      imgs_per_line= max images in any single paragraph of the block

      Determine the image_role for this Q:
        Read from batch_state.figural_qs[qnum].image_role if available,
        else from section_rules PYQ_IMAGE_ANALYSIS via sidecar concept_map,
        else default 'stem_and_options'.
        SPECIAL CASE: if answer_type=='numerical' (FIGURAL-NAT, v4.7),
        treat as 'stem_only' regardless of PYQ_IMAGE_ANALYSIS — a NAT has
        a problem image but no option images (there are no options).

      BRANCH BY image_role:

        stem_and_options (DEFAULT — v4.0 behaviour):
          if imgs_total < n_opt + 1:      → Exit 1   # composite / missing options
          if imgs_per_line > 1:           → Exit 1   # ≥2 options on one line / row
          if <w:tbl> wraps option images: → Exit 1   # option grid/row
          if "1. Figure 1" dummy text:    → Exit 1   # placeholder option

        stem_only (v5.13 — problem image + text options; also covers FIGURAL-NAT):
          if imgs_total < 1:              → Exit 1   # no problem image at all
          # Option-image checks are SKIPPED — options are text (or absent for NAT).
          # Still check: no composite panel (problem should be separate from stem).
          if imgs_per_line > 1:           → Exit 1   # multiple images on one line

        options_only (v5.13 — text stem + option images):
          if imgs_total < n_opt:          → Exit 1   # missing option images
          # No problem image required — stem is text.
          if imgs_per_line > 1:           → Exit 1   # ≥2 options on one line
          if <w:tbl> wraps option images: → Exit 1   # option grid/row

    NOT FIXABLE BY EDITING TEXT: re-render via S10-7 and re-emit via the correct
    helper (S10-8 or S10-8A depending on image_role).
    Report (MANDATE 0 — no content): "G-FIGURAL-COMPOSITE: Q.[n] image_role=[role],
    holds [k] image(s) (expected ≥[min]). Re-render with the correct helper."

  S12-NEW-14 — G-UNDERLINE (v4.1 — underline-span rendering, HARD STOP):
    Catches the M1 defect where an underline-class question shipped its target span
    as a plain-text annotation ("(underlined: senior than me)") instead of a real
    underlined run. Parallel to G-FIGTEXT (figural-as-text), for underline-as-text.
    SELECT (underline-class blocks): a Q-block whose stem references an underlined
      element — UNDERLINE_TRIGGER_RE matches the stem text (see S10-2):
        r"(?i)underlin(?:e|ed)\s+(?:word|words|part|segment|phrase|portion|sentence)"
        r"|the\s+underlined\b"   # one (?i) at start applies to the whole pattern
      (the persisted stem_format_variant == 'sentence_embedded_underlined' also
       selects the block, even if the instruction wording differs.)
    ALGORITHM (per selected block):
      # (a) banned text annotation anywhere in the block:
      if re.search(r"(?i)\(\s*underlin(?:e|ed)\b", block_full_text):  → Exit 1
      # (b) no real underlined run present in the block:
      if not has_underlined_span(block):                              → Exit 1
    has_underlined_span(block) — run-level XML check (a run is underlined when its
      rPr carries <w:u> with a val other than "none"):
        from docx.oxml.ns import qn
        def has_underlined_span(block_elements):
            for el in block_elements:
                for r in el.iter(qn('w:r')):
                    rpr = r.find(qn('w:rPr'))
                    if rpr is None: continue
                    u = rpr.find(qn('w:u'))
                    if u is not None and u.get(qn('w:val')) not in ('none', '0'):
                        return True
            return False
    Test (a) catches the annotation fallback; test (b) catches a silently-dropped
    underline (target rendered as ordinary text). A correct block — target word as a
    real <w:u> run, no parenthetical — passes both.
    NOT FIXABLE BY EDITING TEXT: re-render via S10-2 add_stem_with_underline so the
    target span carries run.underline = True inside the sentence.
    Report (MANDATE 0 — no content): "G-UNDERLINE: Q.[n] references an underlined
    span but [renders it as a '(underlined: …)' annotation / has no underlined run].
    Re-render with add_stem_with_underline (target as a real underlined run)."

  S12-NEW-15 — G-OPTREF (v4.2 — stem↔option reference consistency, HARD STOP):
    Catches the M1 Q.100 mismatch (instruction promised a "no error → last option"
    escape the option set did not contain). EXAM-AGNOSTIC: escape tokens / option
    structures are read from section_rules (none_of_above_map S3-12,
    wrong_option_structure S3-13); the gate enforces coherence only.
    ESCAPE-REFERENCE PATTERNS (generic; extend from section_rules wording — single
    (?i) at the start, no embedded quote chars, so it compiles as written):
      ESCAPE_REF = re.compile(
          r"(?i)\\bif\\b[^.]*\\bno\\s+(?:error|improvement|mistake)\\b"
          r"|\\bselect\\b[^.]*\\bno\\s+(?:error|improvement)\\b"
          r"|none of (?:these|the above)|all of the above"
          r"|both\\b[^.]*\\band\\b[^.]*follow|neither\\b[^.]*\\bnor\\b")
      LASTOPT_REF = re.compile(r"(?i)(?:the\\s+)?last option")
    ALGORITHM (per Q block; opts = the 4 option strings):
      if ESCAPE_REF.search(stem):
          # the referenced terminal option must EXIST among opts
          want = canonical_escape_token(stem)   # "No error" / "No improvement" /
                                                # "None of these" / "Both I and II" …
          if not any(option_is(o, want) for o in opts):  → Exit 1
          # if the stem says "last option", the escape must be the LAST option
          if LASTOPT_REF.search(stem) and not option_is(opts[-1], want):  → Exit 1
      # converse: a "pick the segment with the error" layout (all four options are
      # sentence segments of the stem's carrier sentence) may NOT carry a
      # "no error → last option" instruction unless a real "No error" option exists:
      if is_segment_option_layout(stem, opts) and ESCAPE_REF.search(stem) \
         and not any(option_is(o, "No error") for o in opts):  → Exit 1
    option_is(o, token) does a normalised match (case/whitespace/quote-insensitive)
    against the exam's escape wording from section_rules.
    NOT FIXABLE BY EDITING THE KEY: either append the missing escape option in the
    position the instruction names (and re-balance K-BAL), or switch the stem to the
    matching template (a "select the segment with the error" instruction has NO "no
    error" escape). Carrier-sentence run-ons are fixed by §10-S10-2 layout.
    Report (MANDATE 0): "G-OPTREF: Q.[n] references a '[want]' option that is absent
    / mis-positioned. Add the escape option (or switch to the matching template)."

  S12-NEW-16 — G-UNIQUE (v4.5 — answer-contract record, HARD STOP; generalises v4.2):
    Enforces R-ANSWER (both modes). The answer contract is decided at GENERATION
    (CHECK 3 verify_answer, §7) because verbal ambiguity needs reasoning, not
    regex; this gate is the RECORD-PRESENCE backstop (same pattern as G-CONCEPTDUP
    requiring concept_map). EXAM-AGNOSTIC.
    ALGORITHM:
      read concept_map from the answer_key sidecar (S7-NEW-A).
      for each question q in 1..N:
          rec = concept_map.get(str(q))
          if rec is None or rec.get("answer_verified") is not True:
              → Exit 1
    A missing/False flag means generation SKIPPED the answer contract for that Q
    (e.g. the M1 Q.3 maternal/paternal Sister-vs-Cousin split, or Q.98 is-vs-was
    universal-truth convention would have been caught and disambiguated at CHECK 3;
    or, for an MSQ, a borderline out-set option would have been caught).
    NOT FIXABLE BY FLIPPING THE FLAG: re-run the question through CHECK 3
    verify_answer; if (single) a second option is defensible, or (multi) the set is
    ill-formed or an out-set option is arguable, disambiguate the stem (qualify the
    relation / pin the convention via section_rules / constrain the rule) or
    move/remove the colliding option, then regenerate.

  S12-NEW-18 — G-MSQ-SET (v4.5 — MSQ set well-formedness, HARD STOP; MULTI ONLY):
    Runs ONLY for questions whose concept_map answer_cardinality=='multi' (skipped entirely
    when blueprint multi_present is false — fully dormant). Enforces the structural half
    of R-ANSWER multi + R-MSQ-ESCAPE. EXAM-AGNOSTIC.
    ALGORITHM (read S = answers[q] as a set; n = total_options from blueprint):
      • S empty (k=0)                              → Exit 1
      • S not ⊆ {1..n}                             → Exit 1
      • |S| == n (all-correct, k=n)                → Exit 1
      • an "All of the above" option is present AND section_rules msq_allow_aota is
        false (R-MSQ-ESCAPE)                        → Exit 1
    NOT FIXABLE BY EDITING THE KEY: regenerate the question so the intended correct
    SET is a non-empty proper subset (drop the AOTA option / add a genuine wrong
    option / split an over-broad stem), then re-run CHECK 3.
    Report (MANDATE 0): "G-MSQ-SET: Q.[n] MSQ key is ill-formed ([reason])."

  S12-NEW-19 — G-MSQ-CARD (v4.5 — MSQ fixed-k cardinality, HARD STOP; MULTI + FIXED ONLY):
    Runs ONLY when answer_cardinality=='multi' AND section_rules msq_k_mode=='fixed'.
    ALGORITHM: if |answers[q]| != msq_k → Exit 1.
    For "Select TWO"/"Select THREE" exams this guarantees the rendered set matches the
    instructed count. Variable-k exams skip this gate (no fixed cardinality to check).
    Report: "G-MSQ-CARD: Q.[n] has |S|=[got], expected msq_k=[k]."

  S12-NEW-20 — G-MSQ-INSTR (v4.5 — MSQ instruction line present, HARD STOP; MULTI ONLY):
    Runs ONLY for answer_cardinality=='multi' questions. The multi instruction phrase
    ("(One or more options may be correct)" / "(Select TWO)" / localized equivalent
    from section_rules) MUST appear INSIDE the bold Q.<N>-first stem paragraph (R14 /
    G-QNUM-FIRST — there is no paper-level instructions page). EXAM-AGNOSTIC.
    ALGORITHM: locate the Q.<N> stem paragraph; if it contains no MSQ instruction
    phrase (matched case-insensitively against the section_rules msq_instruction set
    + the universal fallback set) → Exit 1.
    NOT FIXABLE BY ADDING A SEPARATE PARAGRAPH (that breaks R14): re-emit the stem with
    the instruction appended to the Q.<N> line.
    Report: "G-MSQ-INSTR: Q.[n] (MSQ) has no select-instruction in its Q.N stem line."
    Report (MANDATE 0): "G-UNIQUE: Q.[n] has no answer_verified record —
    generation did not run the R-ANSWER check. Re-verify and disambiguate if needed."

  S12-NEW-21 — G-NAT-NOOPT (v4.7 — NAT zero-option, HARD STOP; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. A NAT question is a typed-value
    question with NO options (R4 / R13 NAT exemption). AUTHORITATIVE: scans the rendered
    docx, locates the question's Q.<N> block, and counts option-label paragraphs (the R10
    "N.  " pattern). If a NAT question carries ANY option paragraph → Exit 1 (a generation
    routing bug — the NAT path must emit only the bold Q.<N> stem + blank separator).
    Fully dormant when nat_present=false. EXAM-AGNOSTIC.
    Report: "G-NAT-NOOPT: Q.[n] (NAT) has [k] option paragraph(s); must have none."

  S12-NEW-22 — G-NAT-ANSWER (v4.7 — NAT value well-formed, HARD STOP; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. Reads the stored answer VALUE
    (answers[q], tested 'is None' so 0/negative/fractional are valid) and the per-Q
    ca_range, against nat_meta.nat_answer_type. Exit 1 when: (a) no value recorded; (b)
    value is non-numeric; (c) nat_answer_type=='integer' but the value is not integral;
    (d) ca_range present but malformed (not exactly (lo,hi) with lo<=hi). This is the
    generation-side backstop for R-ANSWER's numerical branch; Step 8 A-NAT-ANSWER
    independently RE-DERIVES the value and checks it lies in the band. EXAM-AGNOSTIC.
    Report: "G-NAT-ANSWER: Q.[n] [value/ca_range problem]."

  S12-NEW-23 — G-NAT-INSTR (v4.7 — NAT instruction line present, HARD STOP; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. The nat_instruction (blueprint
    nat_contract; e.g. "Enter your answer as a numerical value.", localized) MUST appear
    INSIDE the bold Q.<N>-first stem paragraph (R14 / G-QNUM-FIRST — no paper-level
    instructions page). Record-presence backstop here (the per-Q nat_instr_in_stem flag);
    Step 8 A-NAT-INSTR re-checks the rendered docx. NOT FIXABLE by a separate paragraph
    (breaks R14): re-emit the stem with the instruction appended to the Q.<N> line.
    Fully dormant when nat_present=false. EXAM-AGNOSTIC.
    Report: "G-NAT-INSTR: Q.[n] (NAT) has no numerical-entry instruction in its Q.N stem line."

  S12-NEW-29 — G-NAT-GRADE (v5.25 — NAT portal grading value well-formed, HARD STOP;
    NUMERICAL ONLY): Runs ONLY for answer_type=='numerical' questions. Reads the sidecar's
    nat_grading_type/nat_grading_value (S7-NEW-C) and re-runs `derive_nat_grading()` against
    the SAME (value, ca_range, stem_precision) inputs. Exit 1 when: (a) nat_grading_value is
    missing/None while answer_type=='numerical'; (b) nat_grading_value contains any character
    outside `0123456789.-` (allowlist check — a blacklist of "known-bad" patterns like
    scientific notation is NOT sufficient, since it silently admits anything nobody thought to
    ban); (c) the re-derived (type, value) does not EXACTLY match the stored pair — this is a
    determinism check, not a re-judgement, since derive_nat_grading is a pure function of its
    three inputs; (d) a range-typed value's re-derivation raises the NOT-SUPPORTED
    negative-bound error — this Exit 1's as a WELL-POSEDNESS defect on the question (rework the
    numbers), never silently reformatted around. This is the generation-side backstop for the
    portal-grading contract (S7-NEW-C); Step 8 A-NAT-GRADE independently re-derives it again
    from scratch, exactly as A-NAT-ANSWER does for the math value. EXAM-AGNOSTIC.
    Report: "G-NAT-GRADE: Q.[n] [charset/type/determinism problem]."


  S12-NEW-17 — G-MATH-RASTER (v4.3 — math-as-OMML routing, HARD STOP):
    Enforces R-MATH-OMML / §10-S10-4. Catches the M1 Q.55 defect where two
    algebraic expressions ("x + 1/x = 5", "x²+1/x²") shipped as 300-DPI matplotlib
    PNGs (q55_e1.png, q55_e2.png) instead of native OMML. Parallel to G-FIGTEXT
    (figural-as-text) and G-UNDERLINE (underline-as-text); here it is math-as-raster.
    SIGNAL — the figural IMAGE NAME-CONTRACT (provenance-proof). The ONLY producers
    of inline rasters are the figural emitter (§10-S10-8, names q{N}_problem[_k] /
    q{N}_opt{i}) and the linked-stimulus path (§9, names q{N}_stim[_tag]). Any
    inline <w:drawing> whose pic name does NOT match the canonical pattern is an
    UNAUTHORISED raster — the prime case being a rasterised expression. This signal
    cannot be defeated by faking a figural-manifest entry (it reads the image, not a
    sidecar) and cannot false-positive on a genuine figure (which is named by the
    S10-8 convention).
    ```python
    import re
    from docx import Document
    from docx.oxml.ns import qn

    ALLOWED_IMG_NAME_RE = re.compile(
        r"(?i)^q\d+_(problem(_\d+)?|opt\d+|stim(_[a-z0-9]+)?)\.(png|jpg|jpeg)$")
    # corroborating diagnostics only (NOT the pass/fail signal):
    MATH_CONTEXT_RE = re.compile(
        r"(?i)value of|simplif|evaluate|solve for|find the value|"
        r"[=+\u00d7\u00f7\u221a\u00b2\u00b3]|\bx\s*\+|\b1\s*/\s*[a-z]|\^")
    MATH_IMG_NAME_RE = re.compile(
        r"(?i)(_e\d+|_eq\d*|_eqn|_expr|_frac|_math|_formula)")

    def _blocks(doc):
        cur, num, out = [], None, []
        for p in doc.paragraphs:
            m = re.match(r"\s*Q\.(\d+)", p.text or "")
            if m:
                if cur: out.append((num, cur))
                cur, num = [p], m.group(1)
            elif cur is not None:
                cur.append(p)
        if cur: out.append((num, cur))
        return out

    def _img_names(block):
        names = []
        for p in block:
            for dr in p._p.iter(qn('w:drawing')):
                nm = ""
                for c in dr.iter(qn('pic:cNvPr')): nm = c.get('name') or ""
                names.append(nm)
        return names

    def g_math_raster(docx_path):
        doc = Document(docx_path); offenders = []
        for qnum, block in _blocks(doc):
            for nm in _img_names(block):
                if ALLOWED_IMG_NAME_RE.match(nm or ""):
                    continue                         # legitimate figure / stimulus
                stem = " ".join(p.text for p in block)
                offenders.append((qnum, nm,
                                  bool(MATH_CONTEXT_RE.search(stem)),
                                  bool(MATH_IMG_NAME_RE.search(nm or ""))))
        if offenders:
            for q, nm, mc, mn in offenders:
                print(f"G-MATH-RASTER: Q.{q} carries unauthorised raster {nm!r} "
                      f"(math_context={mc}, math_name={mn}).")
            raise SystemExit(1)                      # Exit 1 — HARD STOP
    ```
    NOT FIXABLE BY EDITING TEXT: re-render the expression as OMML via §10-S10-4
    add_math_stem / emit_math_inline (interleave <m:oMath> with the stem text);
    delete the raster. If the flagged image is a GENUINE figure that was mis-named,
    re-emit it through add_figural_question (§10-S10-8) so it carries the canonical
    q{N}_problem / q{N}_opt{i} name.
    Report (MANDATE 0 — no content): "G-MATH-RASTER: Q.[n] ships a math expression
    as image [name] instead of OMML. Re-render via S10-4 add_math_stem; remove the
    raster."

  All 39 gates from v1.0 still apply (S12-1 through S12-39).
  v2.0 added 6 (S12-NEW-1..6). v3.1 added G-CONCEPTDUP. v3.2 added
  G-ALLOC-SUBTOPIC (S12-NEW-8) and G-COUNT-X-UNIQUE (S12-NEW-9). v3.5 added
  G-DELIVERY-SET. v3.6 added G-STIMULUS-ORPHAN (S12-NEW-10). v3.7 added
  G-QNUM-FIRST (S12-NEW-11). v3.8 added G-FORMATDUP (S12-NEW-12). v4.0 added
  G-FIGURAL-COMPOSITE (S12-NEW-13). v4.1 added G-UNDERLINE (S12-NEW-14). v4.2 added
  G-OPTREF (S12-NEW-15) and G-UNIQUE (S12-NEW-16). v4.3 adds G-MATH-RASTER
  (S12-NEW-17). v4.5 adds G-MSQ-SET (S12-NEW-18), G-MSQ-CARD (S12-NEW-19), and
  G-MSQ-INSTR (S12-NEW-20) — all MULTI-mode only, fully dormant when multi_present is false.
  G-NAT-NOOPT / G-NAT-ANSWER / G-NAT-INSTR (S12-NEW-21/22/23) — all NUMERICAL-mode only,
  fully dormant when nat_present is false (no concept_map entry has answer_type=='numerical').
  v5.25 adds G-NAT-GRADE (S12-NEW-29, numbered out of sequence — 24/25 were already taken by
  G-GROUPMANDATE/G-MINCOUNT — see that entry below) to the same NUMERICAL-mode-only family.
  v5.18 adds G-PREQ1 (S12-NEW-27) — the pre-Q.1 body-block ban. Total gates: 67.

  v5.19 adds G-MATCH-TABLE (S12-NEW-28) — match-grid rendering; executable enforcement
  delegated to the Step 8 audit A-MATCH-TABLE (no logic duplicated here). Total gates: 68.

  v5.25 adds G-NAT-GRADE (S12-NEW-29) — NAT portal grading value/type well-formedness
  (0-9.- charset, deterministic re-derivation via derive_nat_grading, S7-NEW-C). NUMERICAL-mode
  only, fully dormant when nat_present is false. Total gates: 69.

  S12-NEW-26 — G-QINDEX (v5.2 — question-index certification, HARD STOP; runs at Final
    Assembly; executable home S13-QINDEX, after S13-REGCHECK). Certifies the mock-N
    registry.question_index this session built (S13-4) — the per-question {subtopic_id,
    difficulty} record Step 6 renders as the five tags. Six checks, all HARD STOP:
      1  an index object exists for mock N;
      2  it has exactly total_questions question entries;
      3  its q set is exactly {1..total_questions} — sorted, no gaps, no duplicates;
      4  every subtopic_id exists in blueprint.subtopic_list[] (never a display name);
      5  every difficulty is in blueprint.difficulty_labels (the canonical set);
      6  the difficulty distribution EQUALS difficulty_schedule[N] exactly (simple->Easy,
         medium->Medium, hard->Hard alias) — satisfiable by construction under the SCHEDULE-FIRST
         assignment rule (§ difficulty budget).
    subtopic_id is Step-7's assignment here; Step 8 INDEPENDENTLY re-derives it from the fixed
    docx and cross-checks it (that is subtopic_id's certification). difficulty is
    authoritative-by-assignment (not re-derivable from the paper) + distribution-verified.
    Writes NOTHING to the docx. Governed by Contract_QuestionMetadataIndex v1.0; the six checks
    were proven in the Phase-1 harness before encoding.
    Report: "G-QINDEX: <failing check(s)>." 

  S12-NEW-27 — G-PREQ1 (v5.18 — pre-Q.1 body-block ban, HARD STOP; per-batch S4-11 AND the
    S13-2 Final-Assembly sweep):
    Scan every paragraph BEFORE the first Q.<N> stem paragraph in the docx body. A paragraph
    is a violation if it carries non-blank text (by construction nothing before Q.1 can be a
    Q.<N> stem or an option line). Any such paragraph → Exit 1:
      "G-PREQ1: non-Q paragraph before Q.1: '<text[:60]>'. The paper is questions-only (R8b);
       delete the pre-Q.1 title/info/scoring/cover block. CATEGORY-C values are metadata,
       never printed."
    Blank paragraphs before Q.1 are ignored (normal separators). DORMANT only if
    section_rules.md EXAM_STRUCTURE declares paper_header_block (a deliberate per-exam opt-in;
    no current exam declares it). Fixable: remove the offending paragraphs from the docx.
    Independently re-verified by Step 8 A-HEADER (strip, not validate).

  S12-NEW-28 — G-MATCH-TABLE (v5.19 — match-grid rendering; per-batch S4-11 + Step-8 audit):
    Every question rendered from stem_format_variant == 'match_the_following' MUST carry a real
    Word table (<w:tbl>) for its List columns. A match emitted via add_standard_question()
    (lists as plain text) is a format-fidelity defect: the MATCH format is counted present
    while the skill is left un-rehearsed. ENFORCEMENT: executable detection is DELEGATED to the
    Step 8 audit A-MATCH-TABLE, which already runs on the cumulative docx during S4-11 STEP B
    when AUDIT_AVAILABLE — the match-detection logic is NOT duplicated here (anti-drift). The
    S4-11 manual checklist item is the no-audit fallback. Fixable: re-emit the question via
    add_match_table() (§10-S10-3M).


# ════════════════════════════════════════════════════════════════════════
# §13 — FINAL ASSEMBLY (v2.0 — REGISTRY INIT FIX)
# ════════════════════════════════════════════════════════════════════════

## S13-1 — Final Assembly trigger (unchanged)

## S13-2 — Complete gate sweep (all 80 gates)

## S13-3 — Post-mock concept audit (unchanged)

## S13-4 — Registry update protocol (v2.0 GAP-03 + GAP-04 fix)

  FIRST-MOCK REGISTRY INITIALISATION (run only when mocks_completed=[]):
  If Mock 1 (registry.mocks_completed is empty), initialise ALL fields:
  ```python
  is_first_mock = len(reg.get('papers_completed', reg.get('mocks_completed', []))) == 0

  if is_first_mock:
      # Initialise fields that Step 1 registry template may not have:
      # (v2.0 GAP-03 fix: content_tracking L4-L18)
      if 'content_tracking' not in reg:
          reg['content_tracking'] = {
              '_schema': {
                  '_note': 'C2 (v5.21): every entry also carries paper_id (from batch_state) '
                           'for cross-tier dedup; mock_n retained. The generalised uniqueness '
                           'ledger (B phase) keys on paper_id.',
                  'ga_facts_used': 'list of {fact, source_url, mock_n}',
                  'passage_topics': 'list of {topic, type, mock_n}',
                  'cloze_topics': 'list of {topic, mock_n}',
                  'vocab_words_used': 'list of {word, correct_answer, mock_n, subtopic}'
                                      ' — v4.5: for a multi (MSQ) vocabulary item, append'
                                      ' one entry per word in the correct SET (correct_answer'
                                      ' may be a list of the in-set words), never just one,'
                                      ' so cross-mock dedup counts every used word.',
                  'idioms_used': 'list of {idiom, mock_n}',
                  'grammar_rules_used': 'list of {rule, mock_n, position}',
                  'computer_facts': 'list of {application, category, concept, mock_n}',
                  'numeric_seeds': 'list of {subtopic, seed_values, mock_n}',
                  'analogy_schemes': 'list of {scheme_type, mock_n}',
                  'cause_effect_domains': 'list of {domain, mock_n}',
                  'syllogism_domains': 'list of {domain, mock_n}',
                  'option_sets': 'list of {subtopic, sorted_options, mock_n}'
              },
              'ga_facts_used': [],
              'passage_topics': [],
              'cloze_topics': [],
              'vocab_words_used': [],
              'idioms_used': [],
              'grammar_rules_used': [],
              'computer_facts': [],
              'numeric_seeds': [],
              'analogy_schemes': [],
              'cause_effect_domains': [],
              'syllogism_domains': [],
              'option_sets': []
          }
      # (v2.0 GAP-04 fix: image_phashes, image_sources_used, session_log)
      for field in ['image_phashes', 'image_sources_used', 'session_log', 'question_index']:
          if field not in reg:
              reg[field] = []
  ```

  THEN commit pending_registry to registry:
  ```python
  # v5.34: bind EXPLICITLY rather than relying on a session-level import. The
  # whole GAP-2026-08-01 family began with a name that was read at three call
  # sites and bound at none, so a new read (glob, below) states its import here.
  import os, json, glob

  # Load registry from working dir (not /mnt/project/):
  registry = json.load(open(f'/home/claude/{EXAM}_registry.json'))

  # Apply first-mock initialisation above if needed.

  # Reload cross-batch data:
  prog = json.load(open(f'/home/claude/{EXAM}_M{N}_progress.json'))
  passage_linked_qs = set(prog.get('passage_linked_qs', []))
  cloze_linked_qs   = set(prog.get('cloze_linked_qs', []))

  # Commit pending_registry (the ONLY write to registry during this session):
  registry['question_hashes'].extend(pending_registry['question_hashes'])
  registry['stem_texts'].extend(pending_registry['stem_texts'])
  registry['semantic_tuples'].extend(pending_registry['semantic_tuples'])
  # B (v5.22): append this paper's (item × angle) usage log (for cross-paper spacing-8).
  registry.setdefault('semantic_usage', []).extend(pending_registry.get('semantic_usage', []))
  # B: merge the sticky, cross-tier exhaustion flags — set-once, NEVER clear (setdefault keeps
  # the earliest since_paper if a subtopic was already flagged in a prior paper).
  _ex = registry.setdefault('exhausted_subtopics', {})
  for _sid, _rec in pending_registry.get('exhausted_subtopics', {}).items():
      _ex.setdefault(_sid, _rec)
  registry.setdefault('image_phashes', []).extend(pending_registry.get('image_phashes', []))
  registry.setdefault('image_sources_used', []).extend(
      pending_registry.get('image_sources_used', []))

  # Update content_tracking (all L4-L18):
  ct = registry.setdefault('content_tracking', {})
  for field in ['ga_facts_used', 'passage_topics', 'cloze_topics',
                'vocab_words_used', 'idioms_used', 'grammar_rules_used',
                'computer_facts', 'numeric_seeds', 'analogy_schemes',
                'cause_effect_domains', 'syllogism_domains', 'option_sets']:
      ct.setdefault(field, []).extend(pending_registry.get(field, []))

  # RC manifests:
  if passage_present:
      registry.setdefault('rc_manifests', []).append({
          "mock": N,
          "passage_linked": sorted(list(passage_linked_qs)),
          "cloze_linked":   sorted(list(cloze_linked_qs))
      })

  # Figural manifests:
  if figural_present and os.path.exists(f'/home/claude/{EXAM}_fig_manifest.json'):
      fig = json.load(open(f'/home/claude/{EXAM}_fig_manifest.json'))
      registry.setdefault('figural_manifests', []).append({
          "mock": N,
          "figural_qs": list(fig['questions'].keys()),
          "image_hashes": [
              h for q in fig['questions'].values() for h in q.get('image_hashes', [])
          ],
          # v5.31 (GAP-2026-07-26-003 D2): the object_type each figure was generated
          # AS, plus its subtopic_id, so Step 8 A-FIGPROFILE can audit conformance
          # against the profile Step 5 measured. These live in the REGISTRY because
          # Step 8 receives it; the answer_key sidecar carrying concept_map is NOT
          # delivered (S0-1), so subtopic_id must travel here or the gate is blind.
          # Omitted per question when the profile mode was 'unconstrained' — an
          # absent entry makes the gate dormant rather than wrong.
          "object_types": {
              str(q): v['object_type'] for q, v in fig['questions'].items()
              if v.get('object_type')
          },
          "subtopic_ids": {
              str(q): v['subtopic_id'] for q, v in fig['questions'].items()
              if v.get('subtopic_id')
          },
          # v5.34 (GAP-2026-08-01-FIGSPEC-TRANSPORT D2): the FigureSpec records
          # themselves, keyed by the CANONICAL PNG name S10-8 stamps on the
          # drawing (_name_last_drawing -> "q{N}_problem.png"/"q{N}_opt{i}.png"),
          # which is the same base write_spec_sidecar() names the sidecar after.
          #
          # WHY THIS IS REQUIRED. The twelve v2.11 figure-conformance gates
          # (A-FIGSCALE / A-FIGLABEL / A-FIGDPI / A-FIGDEGEN / A-FIGMONO /
          # A-FIGOPTUNIF / A-FIGCOLOUR / A-FIGCVD / A-FIGSERIES / A-FIGGLYPH /
          # A-FIGALT / A-FIGLABELPX) are arithmetic over the saved PNG AND ITS
          # SIDECAR. render_figure() mutates the spec with png_px, png_dpi,
          # placed_in, placement_scale and font_pt_native — the record of what
          # actually happened — and write_spec_sidecar() drops it beside the PNG
          # in THIS session's working directory. That directory is internal and
          # is never delivered (S0-1 / R-DELIVER), so before v5.34 Step 8 saw
          # spec == {} on every figure, fc.is_legacy() read every v5.33+ render
          # as pre-v5.33 output, and EC-V18 downgraded every BLOCKING verdict on
          # a paper that was not in fact legacy. The registry is the sanctioned
          # channel for exactly this — the precedent object_types/subtopic_ids
          # set at v5.31, and for the identical reason: Step 8 receives the
          # registry and receives no sidecar.
          #
          # ABSENT-SAFE BOTH WAYS: a session that rendered no figure through
          # figural_core writes no sidecar and this is {}, which Step 8 reads as
          # legacy — i.e. exactly the pre-v5.34 behaviour, never a wrong verdict.
          # NOT delivered as a file and NOT written to the docx; it travels only
          # inside the registry that Step 8 already receives.
          "figure_specs": {
              os.path.basename(_fs)[:-len('.figspec.json')] + '.png':
                  json.load(open(_fs, encoding='utf-8'))
              for _fs in sorted(glob.glob('/home/claude/*.figspec.json'))
          }
      })

  # Question metadata index (v5.2 — Contract_QuestionMetadataIndex v1.0): build ONE mock object
  # {mock, questions:[{q, subtopic_id, difficulty}]} from the per-Q concept_map the sidecar
  # accumulated (S7-NEW-A). subtopic_id = cross-step join key; difficulty = canonical Complexity
  # label. NEVER written to the docx. Replace-by-key so a re-run of this mock is idempotent;
  # Step 8 later re-syncs this object by key from the fixed docx.
  _cm = json.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json')).get('concept_map', {})
  _qi = [{"q": int(qn),
          "subtopic_id": _cm[qn].get("subtopic_id"),
          "difficulty":  _cm[qn].get("difficulty")}
         for qn in sorted(_cm, key=int)]
  # C2: re-derive identity here (self-contained — bp + N are session-level, always in scope).
  import re as _re_wb
  _tp = next((mk for mk in bp.get('mocks', []) if mk.get('mock') == N), None)
  paper_id = (_tp or {}).get('paper_id', f"MOCK:M{N:02d}")
  registry.setdefault('question_index', [])
  registry['question_index'] = [e for e in registry['question_index']
                                if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") != paper_id]
  registry['question_index'].append({"mock": N, "paper_id": paper_id, "questions": _qi})

  # Append to BOTH ledgers: mocks_completed (legacy int) + papers_completed (generalised id).
  registry.setdefault('mocks_completed', []).append(N)
  registry.setdefault('papers_completed', []).append(paper_id)
  registry.setdefault('session_log', []).append({
      "mock": N, "paper_id": paper_id, "batches": len(batches_completed),
      "q_range": [1, total_questions], "questions_added": total_questions,
      "audit_result": "exit_0", "verdict": "SHIP",
      "timestamp": datetime.now(timezone.utc).isoformat(),
      "notes": "v2.0 session"
  })

  # v5.14 THREE-AXIS: commit this paper's contribution to the WINDOW-level Axis-2 counts.
  # Window index is recomputed here from paper_index + batch_size_qs (same formula as S3-4) so
  # the commit is self-consistent even if the read-side variables are out of scope at assembly.
  _win = bp.get('batch_size_qs', 10)
  _pidx = int(_re_wb.sub(r'\D', '', paper_id.rsplit(':', 1)[-1]) or N)   # == N for a mock
  _cur_window = (_pidx - 1) // max(1, _win)
  # axis2_window_counts holds the per-section snapshots accumulated during generation (S7-AXIS).
  if any(v is not None for v in axis2_window_counts.values()):
      registry['axis2_window'] = {'window': _cur_window,
                                  'sections': {s: c for s, c in axis2_window_counts.items()
                                               if c is not None}}
  # (Absent-safe: if the feature was inert this stays unset / carries the prior window verbatim.)

  json.dump(registry, open(f'/home/claude/{EXAM}_registry.json', 'w'),
            indent=2, ensure_ascii=False)
  ```

## S13-REGCHECK — Registry schema-completeness gate (v3.5 — runs after S13-4 commit)

  Runs immediately after the S13-4 commit writes registry.json, BEFORE S13-5.
  Sets REGCHECK_OK (read by S13-7). This gate does NOT trust the Step-1 template
  — it enforces the v2.0 schema regardless of what the template provided, so a
  drifted template can never silently ship an incomplete registry (the M1-D13
  failure mode). It is idempotent and safe to re-run.

  ```python
  reg = json.load(open(f'/home/claude/{EXAM}_registry.json'))

  REQUIRED_TOP = [
      'exam_code', 'schema_version', 'mocks_completed', 'papers_completed',
      'question_hashes', 'stem_texts', 'semantic_tuples', 'semantic_usage',
      'exhausted_subtopics',
      'question_index',
      'image_phashes', 'image_sources_used', 'session_log',
      'content_tracking',
      'section_names', 'rc_manifests', 'figural_manifests',
  ]
  REQUIRED_CT = [   # content_tracking L4-L18 subfields
      'ga_facts_used', 'passage_topics', 'cloze_topics', 'vocab_words_used',
      'idioms_used', 'grammar_rules_used', 'computer_facts', 'numeric_seeds',
      'analogy_schemes', 'cause_effect_domains', 'syllogism_domains',
      'option_sets',
  ]

  missing_top = [f for f in REQUIRED_TOP if f not in reg]
  missing_ct  = [f for f in REQUIRED_CT if f not in reg.get('content_tracking', {})]

  # SELF-HEAL (idempotent): schema is mandatory, so add any field the drifted
  # Step-1 template omitted, as an empty container. Same intent as the S13-4
  # first-mock init, but enforced as a GATE that ALWAYS runs.
  for f in missing_top:
      reg[f] = {} if f in ('content_tracking', 'exhausted_subtopics') else []
  ct = reg.setdefault('content_tracking', {})
  for f in missing_ct:
      ct[f] = []

  still_missing = ([f for f in REQUIRED_TOP if f not in reg]
                   + [f for f in REQUIRED_CT if f not in reg.get('content_tracking', {})])
  if still_missing:
      raise SystemExit(
          f"HARD STOP (S13-REGCHECK): registry still missing {still_missing} "
          f"after self-heal. Do NOT deliver. Inspect S13-4 commit logic.")

  # v4.7 (ND6 — MANDATORY): options_by_q — per-question EXPECTED option count for THIS mock,
  # written into the registry so Step 9 (Explain) resolves each question's TYPE. 0 marks a NAT
  # question (no options). Step 4's expected_options() READS this map and never counts rendered
  # options, so a NAT question is non-resolvable (mis-typed as MCQ, or count-invariant HALT)
  # WITHOUT it. Derived from the mock sidecar concept_map (answer_type per Q); total_options
  # from the persisted msq_meta. Harmless for non-NAT mocks (every value == total_options).
  _akp = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  try:
      _kd     = json.load(open(_akp))
      _km     = _kd.get("concept_map", {})
      _ocount = int(_kd.get("msq_meta", {}).get("total_options", 4))
  except Exception:
      _km, _ocount = {}, 4
  obq = {q: (0 if _km[q].get("answer_type") == "numerical" else _ocount) for q in _km}
  reg.setdefault('options_by_q', {})[str(N)] = obq

  # v4.8 — section_names: the declared section names for THIS exam, written so both the
  # embedded G-SECTIONHDR gate and Step 8 A-SECHDR can flag a stray body paragraph that IS a
  # section name (the realistic section-header form). Provenance-based, exam-agnostic.
  reg['section_names'] = [ (s.get('section_name') or s.get('name') or '').strip()
                           for s in bp.get('sections', [])
                           if (s.get('section_name') or s.get('name')) ]

  # Persist healed registry to BOTH working dir and outputs:
  json.dump(reg, open(f'/home/claude/{EXAM}_registry.json', 'w'),
            indent=2, ensure_ascii=False)
  os.makedirs('/mnt/user-data/outputs', exist_ok=True)
  json.dump(reg, open(f'/mnt/user-data/outputs/{EXAM}_registry.json', 'w'),
            indent=2, ensure_ascii=False)

  if missing_top or missing_ct:
      print(f"S13-REGCHECK: healed drifted template — added "
            f"{missing_top + missing_ct}. Registry now schema-complete.")
  REGCHECK_OK = True
  print("S13-REGCHECK: registry schema complete. OK.")
  ```

## S13-QINDEX — Question-index gate execution (v5.2 — G-QINDEX; runs after S13-REGCHECK)

  Runs immediately after S13-REGCHECK, BEFORE S13-5/S13-7. Certifies the mock-N
  question_index this session built (S13-4). Sets QINDEX_OK (read by S13-7). Executable
  home of gate G-QINDEX (definition in §12 S12-NEW-26). Governed by
  Contract_QuestionMetadataIndex v1.0; the six checks were proven in the Phase-1 harness.

  ```python
  from collections import Counter
  reg = json.load(open(f'/home/claude/{EXAM}_registry.json'))
  _canon   = bp.get('difficulty_labels', ['Easy', 'Medium', 'Hard'])
  _sub_ids = {sub.get('subtopic_id') for sub in bp.get('subtopic_list', [])}
  _sched   = next((d for d in bp.get('difficulty_schedule', []) if d.get('mock') == N), {})
  _entry   = next((e for e in reg.get('question_index', []) if e.get('mock') == N), None)
  _fails = []
  if _entry is None:
      _fails.append(f"G-QINDEX/1: no question_index object for mock {N}")
  else:
      _qs = _entry.get('questions', [])
      if len(_qs) != total_questions:                                              # check 2
          _fails.append(f"G-QINDEX/2: {len(_qs)} entries != total_questions {total_questions}")
      _qn = [x.get('q') for x in _qs]                                              # check 3
      if _qn != sorted(_qn) or len(set(_qn)) != len(_qn) \
         or set(_qn) != set(range(1, total_questions + 1)):
          _fails.append(f"G-QINDEX/3: q set != 1..{total_questions} (sorted/unique/complete)")
      _bad_id = sorted({x.get('subtopic_id') for x in _qs                          # check 4
                        if x.get('subtopic_id') not in _sub_ids})
      if _bad_id:
          _fails.append(f"G-QINDEX/4: subtopic_id(s) not in blueprint: {_bad_id}")
      _bad_d = sorted({x.get('difficulty') for x in _qs                            # check 5
                       if x.get('difficulty') not in _canon})
      if _bad_d:
          _fails.append(f"G-QINDEX/5: difficulty value(s) not in {_canon}: {_bad_d}")
      # check 6 — distribution EXACT vs difficulty_schedule[N] (simple/medium/hard -> label alias)
      _alias3 = ({'simple': _canon[0], 'medium': _canon[1], 'hard': _canon[2]}
                 if len(_canon) == 3 else {'simple': 'Easy', 'medium': 'Medium', 'hard': 'Hard'})
      _want = {}
      for _k, _v in _sched.items():
          if _k in ('mock', 'band') or not isinstance(_v, int):
              continue
          _lab = _alias3.get(_k, _k)
          _want[_lab] = _want.get(_lab, 0) + _v
      _want = {lab: _want.get(lab, 0) for lab in _canon}
      _got_all = Counter(x.get('difficulty') for x in _qs)
      _got = {lab: _got_all.get(lab, 0) for lab in _canon}
      if _got != _want:
          _fails.append(f"G-QINDEX/6: distribution {_got} != schedule {_want}")
  if _fails:
      raise SystemExit("HARD STOP (G-QINDEX): " + "; ".join(_fails)
                       + ". Fix the per-Q subtopic_id/difficulty capture (S7-NEW-A) or the "
                       + "schedule-first assignment, rebuild question_index (S13-4), re-run.")
  QINDEX_OK = True
  print(f"G-QINDEX: question_index certified for mock {N} — OK.")
  ```

## S13-5 — Registry integrity check (unchanged)

## S13-6 — THE DELIVERABLE SET IS CLOSED (v3.5 — read before delivering)

  At Final Assembly, Step 7 delivers EXACTLY TWO files to the user, and
  NOTHING ELSE. This is an exhaustive, closed list — not a minimum.

  DELIVER (both mandatory, both via the SAME present_files call):
    1. [ExamCode]_Mock[N]_Create.docx     — the final mock paper
    2. [ExamCode]_registry.json             — updated dedup/tracking registry

  DO NOT DELIVER (internal — never passed to present_files):
    ✗ [ExamCode]_M[N]_answer_key.json       — internal sidecar (S3-14)
    ✗ any standalone answer-key file in ANY format (.docx/.pdf/.json/.txt)
    ✗ [ExamCode]_fig_manifest.json          — internal
    ✗ [ExamCode]_M[N]_batch_state.json      — internal
    ✗ [ExamCode]_M[N]_progress.json         — internal
    ✗ any per-batch cumulative docx (Q1to[k]) — superseded by _Create.docx

  This is the inline anchor for R-DELIVER. The answers exist ONLY in the
  internal answer_key.json sidecar (S3-14), which is NEVER delivered. If the
  user wants a learner-facing answer key, that is a Step-4 (MockExplain)
  artefact, not a Step-7 one. Step 7 ships the paper + registry, full stop.

## S13-7 — Pre-delivery checklist (v3.5 — MANDATORY before present_files)

  Run this 7-point self-verification. If ANY item fails: fix, then re-run.
  present_files is FORBIDDEN until all 7 pass (extends B-7 to Final Assembly).

  ```python
  import os, json
  out = '/mnt/user-data/outputs'
  # v5.28: paper_slug is ALWAYS pp.paper_slug(paper_id) — the single shared implementation
  # (paper_pipeline.py), replacing the old inline C2 v5.21 version. Zero-pads mocks to 2
  # digits (Mock01, not Mock1) and correctly collapses scoped "::" before remaining ":".
  paper_slug = pp.paper_slug(paper_id)
  docx_name = f'{EXAM}_{paper_slug}_Create.docx'
  reg_name  = f'{EXAM}_registry.json'
  docx_path = f'{out}/{docx_name}'
  reg_path  = f'{out}/{reg_name}'

  checks = []
  # 1. Final docx staged in outputs.
  checks.append(("1 final docx in outputs", os.path.exists(docx_path)))
  # 2. registry.json staged in outputs (THE step missed in M1).
  checks.append(("2 registry.json in outputs", os.path.exists(reg_path)))
  # 3. registry passed schema gate (§13-REGCHECK ran OK).
  checks.append(("3 registry schema complete", bool(globals().get('REGCHECK_OK'))))
  # 4. NO standalone answer-key file staged.
  bad_ak = [f for f in os.listdir(out) if 'answer' in f.lower()]
  checks.append(("4 no answer-key file in outputs", len(bad_ak) == 0))
  # 5. NO internal sidecar staged.
  internal = ['_answer_key.json', '_fig_manifest.json',
              '_batch_state.json', '_progress.json']
  leaked = [f for f in os.listdir(out) if any(m in f for m in internal)]
  checks.append(("5 no internal sidecars in outputs", len(leaked) == 0))
  # 6. outputs == EXACTLY the 2 deliverables (closed set).
  staged = set(os.listdir(out))
  checks.append(("6 outputs == exactly the 2 deliverables",
                 staged == {docx_name, reg_name}))
  # 7. question_index certified for this mock (G-QINDEX / S13-QINDEX ran OK).
  checks.append(("7 question_index certified (G-QINDEX)", bool(globals().get('QINDEX_OK'))))

  fails = [name for name, ok in checks if not ok]
  if fails:
      raise SystemExit(
          "HARD STOP (S13-7): pre-delivery checklist failed: "
          + "; ".join(fails)
          + ". Fix each, then re-run S13-7. Do NOT call present_files yet. "
          + "If item 4 fails, DELETE the off-spec answer-key file from outputs. "
          + "If item 2/3 fails, re-run S13-4 + S13-REGCHECK. "
          + "If item 5/6 fails, move internal files back to /home/claude.")
  print("S13-7: all 7 pre-delivery checks PASS. Cleared to deliver.")
  ```

  Stage ONLY the two deliverables in /mnt/user-data/outputs; keep every
  internal file in /home/claude. Item 6 enforces the closed set.

## S13-8 — Deliver (v3.5 — the SINGLE present_files call)

  Call present_files ONCE, with BOTH files, docx first (most relevant):
    present_files([
        docx_path,        # C2: paper-scoped ({EXAM}_Mock{N}_Create.docx for a mock)
        reg_path
    ])

  This is the ONLY present_files call at Final Assembly. Do NOT call it once
  per file. Do NOT call it for any internal file. The per-batch habit of "one
  docx per present_files" does NOT apply here — Final Assembly ships TWO files.

## S13-9 — Handoff message (v3.5 — print after present_files, then END)

  Print exactly this block (no question content — MANDATE 0), filling brackets:

  ```
  === MOCK [N] COMPLETE — Step 7 done ===
  Delivered (2 files):
    • [ExamCode]_Mock[N]_Create.docx   — the mock paper
    • [ExamCode]_registry.json           — updated registry

  ⚠ REGISTRY HANDOFF — REQUIRED before generating the next mock:
    Replace registry.json in your [ExamCode] project knowledge with the one
    just delivered. The next mock's dedup depends on it. If you skip this,
    Mock [N+1] may repeat questions/scenarios from Mock [N].

  No separate answer-key file is produced by Step 7 (by design). Answers are
  surfaced later by Step 9 (MockExplain).

  Next step → Step 8 (MockCreateAudit): independent audit of this mock.
  Audit result this run: [exit_0 / SHIP].
  =========================================
  ```

  After printing the handoff: END THE RESPONSE. Write nothing more.

## S13-9A — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat delivery report or handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Upload / Replace / Use locally), and next-step reference.

Step 7 uses BOTH footer types:
  - F1 (amber) after each non-final batch (delivers cumulative Q1to[K].docx)
  - F2 (green) after Final Assembly (delivers Create.docx + registry.json)

NOTE: The footer renders AFTER the S13-9 handoff message. Sequence is:
  1. S13-7 pre-delivery checklist → 2. S13-8 present_files → 3. S13-9 handoff → 4. Footer
```

# ════════════════════════════════════════════════════════════════════════
# §14 — REGISTRY SCHEMA (v2.0 — fields added)
# ════════════════════════════════════════════════════════════════════════

## S14-1 — Universal fields (v2.0 GAP-04 fix — added fields)

  ```json
  {
    "exam_code"          : "[ExamCode]",
    "schema_version"     : "1.0",
    "mocks_completed"    : [],
    "question_hashes"    : [],
    "stem_texts"         : [],
    "semantic_tuples"    : [],
    "semantic_usage"     : [],
    "exhausted_subtopics": {},
    "question_index"     : [],
    "image_phashes"      : [],
    "image_sources_used" : [],
    "session_log"        : [],
    "content_tracking"   : { "_schema": {...}, ... }
  }
  ```

  question_index (v5.2): seeded [] by Step 1; Step 7 APPENDS one object per mock
  {mock, questions:[{q, subtopic_id, difficulty}]} at S13-4 (never in the docx), certified by
  G-QINDEX (S12-NEW-26 / S13-QINDEX). image_phashes, image_sources_used, session_log: MUST be
  present from Mock 1.
  options_by_q (v4.7): { "N": { "q": expected_option_count } } — per-mock, per-question
  expected option count. 0 marks a NAT question (no options). Written by S13-REGCHECK;
  consumed by Step 9 (Explain) to resolve each question's TYPE (mcq/msq/nat).
  section_names (v4.8): list of declared section names for this exam, from blueprint
  sections[].section_name. Written by S13-REGCHECK; consumed by the embedded G-SECTIONHDR
  gate and Step 8 A-SECHDR to flag stray section-name headers in the paper body.
  If registry from Step 1 is missing them: S13-4 first-mock init adds them, and
  S13-REGCHECK (v3.5) enforces the full schema as a gate before delivery —
  self-healing any field the drifted Step-1 template omitted, so an incomplete
  registry can never ship.

## S14-2 through S14-5 — (unchanged from v1.0 — see v1.0 for full spec)

# ════════════════════════════════════════════════════════════════════════
# §15 — AUTO-FIX PROTOCOL (unchanged from v1.0)
# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# §16 — STATUS DASHBOARD (unchanged from v1.0)
# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# §17 — DEFINITION OF DONE (v2.0 — additional items)
# ════════════════════════════════════════════════════════════════════════

## S17-1 — Complete DoD checklist (v2.0 additions marked *; v3.0 marked **)

  GENERATION (BATCH ENFORCEMENT — §4 v3.0):
  □ All batches completed (batches_completed == every batch_id in plan)  **
  □ ONE batch = ONE response throughout (no two batches in one response)  **
  □ Every batch generated EXACTLY q_count Qs from batch_state.json (B-3)  **
  □ No batch was auto-advanced (B-4); every next batch needed a "continue"  **
  □ Pre-batch self-check (S4-5) run before each batch  **
  □ batch_state.json updated after each delivery (S4-8a)  **
  □ Final batch auto-ran Final Assembly in same response (S4-9)  **
  □ Every batch: Layer 1 STOP executed (separate response per batch)  *
  □ Every batch: Manual gate checklist (S4-11) completed if no audit.py  *
  □ Final Assembly gate check passed (80 gates)  *
  □ (Issue 2b) group-presence (G-GROUPMANDATE) + min-count (G-MINCOUNT) verified for
    this mock; cadence left to Step 1 (cross-mock, not gated in Step 7)  *
  □ Audit STDOUT appended to every batch reply

  CONTENT QUALITY:
  □ All 80 gates: PASS or NON-FIX-WARN  *
    (the 12 v5.33 FIGURE CONFORMANCE gates report AMBER / VOID_ITEM / BLOCKING
     per S10-7 Q8b; NO colour condition may halt a run, and EC-V18 downgrades
     every BLOCKING gate to AMBER for output with no FigureSpec sidecar)  *
  □ Each subtopic has EXACTLY its blueprint q_count (RULE A, G-ALLOC-SUBTOPIC) — DOUBT-3  ***
  □ No scenario_key repeats anywhere in the mock (RULE B, G-CONCEPTDUP) — DOUBT-3  ***
  □ Subtopics with N>1 use N distinct scenarios; extra concepts invented as needed  ***
  □ OMML renders correctly (generated with python-docx if QA present); NO
    algebraic/built-up expression shipped as a raster image (R-MATH-OMML,
    G-MATH-RASTER) — every inline image is a named figure/stimulus, never math  *
  □ All images: visual_verified=True
  □ Font: configured font (FONT_NAME) and size (FONT_SIZE_PT) throughout  *
  □ Option labels: configured format (OPTION_LABEL_FMT)  *
  □ No section headings in paper body  *
  □ No title/info/scoring/cover block before Q.1 — paper is questions-only (R8b, G-PREQ1)  *
  □ No answer key embedded in docx  *
  □ All RC passages reprinted per linked Q
  □ All fact-recall questions: source citations logged (authoritative sources)
  □ All per-section mandatory areas/topics covered — the full set declared in
    section_rules (count read from data, not hardcoded)
  □ manifest.mandatory_every_mock — every mandated subtopic present in every mock
    (S3-17 pre-gen HS-8 + G-ALLOC-SUBTOPIC in generated Qs); exam-agnostic, no names  *
  □ manifest.alternation_groups — ≤1 member of each group per mock (S3-17 + G-ALTGROUP)  *
  □ Cross-mock variant rotation honored where section_rules declares a ROTATION cycle (S6-9)  *
  □ Difficulty: schedule satisfied

  REGISTRY:
  □ pending_registry committed at Final Assembly (not during generation)  *
  □ content_tracking L4-L18 fields populated  *
  □ image_phashes, image_sources_used, session_log present  *
  □ Registry integrity check passed

  DELIVERY:
  □ Complete docx delivered via present_files
  □ Updated registry.json delivered via present_files
  □ Handoff message with registry replacement instruction
  □ Audit report produced

  DELIVERY (v3.5 — closed contract):
  □ EXACTLY 2 files delivered: final .docx + registry.json (S13-6, R-DELIVER)  **
  □ registry.json staged in /mnt/user-data/outputs and present_files'd (S13-8)  **
  □ NO standalone answer-key file in any format delivered (R-DELIVER)  **
  □ NO internal sidecar (answer_key/fig/batch_state/progress) delivered  **
  □ S13-7 pre-delivery 7-point checklist passed before present_files  **
  □ S13-REGCHECK passed: registry schema-complete (top + content_tracking)  **
  □ G-DELIVERY-SET passed in the Final-Assembly gate sweep  **
  □ G-STIMULUS-ORPHAN passed: every linked-group question carries its shared
    stimulus inside its own block (R-LINKED / §9 Model A) — verified per batch
    AND mock-wide at Final Assembly  **
  □ G-QNUM-FIRST passed: every question block (single AND linked) opens with its
    "Q.<N>" paragraph; no stimulus/preamble precedes the Q-number; the linked
    specific-ask paragraph is non-numbered (R14)  **
  □ G-FORMATDUP passed: no two CLASS-2/3 questions sharing a CONCEPT_GROUP share
    presentation_key; ≥2 stem formats when a CONCEPT_GROUP has ≥3 Qs (RULE C);
    G-CLUSTER spacing/distribution satisfied (R19 v3.8)  **
  □ G-FIGURAL-COMPOSITE passed: every figural Q correctly structured per its
    image_role variant (v5.13 — stem_and_options / stem_only / options_only);
    no composite panel, no two images per line, no baked-in question chrome;
    option images (when present) 300 DPI on a uniform square canvas
    (R-FIGURAL / §10-S10-7/S10-8/S10-8A)  **
  □ G-UNDERLINE passed: every underline-class Q renders its target span as a real
    underlined run inside the sentence; no "(underlined: X)" annotation, no
    underscore/markdown fake (R-UNDERLINE / §10-S10-2)  **
  □ G-OPTREF passed: no stem references a terminal/escape option absent from the
    options; "no error/no improvement → last option" instructions have the escape
    option at the named position; carrier-sentence stems are two-paragraph, no
    run-on (R-OPTREF / §10-S10-2)  **
  □ G-UNIQUE passed: every Q satisfies R-ANSWER for its mode — single: exactly one
    defensible option; multi: the correct SET passes the set contract; CHECK 3
    verify_answer ran and answer_verified==true is recorded
    for all N (R-ANSWER / §7)  **
  □ G-MSQ-SET passed (multi only): every MSQ key is a non-empty proper subset of
    1..total_options; no banned AOTA option under multi (R-MSQ-ESCAPE). Dormant when
    multi_present=false  **
  □ G-MSQ-CARD passed (multi + fixed-k only): every MSQ key has |S|==msq_k  **
  □ G-MSQ-INSTR passed (multi only): every MSQ stem carries its select-instruction
    on the Q.N line (R14)  **
  □ G-NAT-NOOPT / G-NAT-ANSWER / G-NAT-GRADE / G-NAT-INSTR passed (numerical only): every NAT
    question renders zero options, carries a well-formed value (+ca_range lo<=hi for real NAT),
    a portal-safe grading value/type (0-9.- charset, S7-NEW-C), and its nat_instruction sits
    on the Q.N line (R4/R13/R14 NAT exemptions)  **
  □ options_by_q written to registry (per-question expected option count, 0 for NAT) so
    Step 4 resolves question type (ND6)  **
  □ G-MATH-RASTER passed: no algebraic/built-up expression ships as a raster
    image; every inline <w:drawing> is a canonically-named figure/stimulus
    (q{N}_problem/opt{i}/stim), and all built-up math is OMML (R-MATH-OMML /
    §10-S10-4)  **
  □ G-QINDEX passed (v5.2): registry.question_index has one {q, subtopic_id, difficulty}
    entry per question (q = 1..total_questions, sorted/unique/complete), every subtopic_id ∈
    blueprint.subtopic_list, every difficulty ∈ difficulty_labels, and the difficulty
    distribution == difficulty_schedule[N] exactly (S13-QINDEX / Contract v1.0)  **
  □ S13-9 handoff printed with the registry-replacement instruction  **

## S17-2 — Step 8 handoff (unchanged from v1.0)

# ════════════════════════════════════════════════════════════════════════
# §18 — AUDIT GATE GLOSSARY (80 gates total — 39 v1.0 baseline + 29 tabled below
#        + 12 FIGURE CONFORMANCE catalogued in Framework_MockTestCreateAudit v2.11)
# ════════════════════════════════════════════════════════════════════════

  v2.0 adds 6 new gates to the 39 from v1.0:

  | Gate Code    | Checks                                      | Fix?  | Fix                         |
  |--------------|---------------------------------------------|-------|-----------------------------|
  | G-FONTCHECK  | All runs use configured font (no banned fonts)  | YES   | Re-generate with configured font |
  | G-OPTLABEL   | Option labels match configured format           | YES   | Regenerate options          |
  | G-SECTIONHDR | No section headers in docx body — keyword form + (v4.8) section-NAME form (paragraph == a declared section name, from reg['section_names']) | YES   | Delete header paragraphs    |
  | G-ANSWERKEY  | No answer key embedded in docx              | YES   | Remove answer key section   |
  | G-FIGTEXT    | No figural text placeholders                | NO    | Generate real image or sub  |
  | G-ALTGROUP   | No alternation group has 2+ members in mock | YES   | Drop the off-parity member  |

  v3.2 added G-ALLOC-SUBTOPIC + G-COUNT-X-UNIQUE (with G-CONCEPTDUP from v3.1) → 48.
  These three DOUBT-3 gates (§12 S12-NEW-7/8/9) were defined but omitted from this table until
  v5.3; tabled here for glossary completeness:
  | G-CONCEPTDUP     | No scenario_key repeats in the mock (RULE B / DOUBT-3)      | YES | Regenerate the duplicate scenario         |
  | G-ALLOC-SUBTOPIC | Each subtopic_id has EXACTLY its blueprint q_count (RULE A) | YES | Add/drop questions to hit the exact count |
  | G-COUNT-X-UNIQUE | Per-subtopic generated counts match the concept_map        | YES | Reconcile concept_map vs generated Qs     |

  v3.5 adds 1 new gate (→ 49), enforced in the S13-2 Final-Assembly gate sweep:

  | Gate Code      | Checks                                          | Fix? | Fix                                  |
  |----------------|-------------------------------------------------|------|--------------------------------------|
  | G-DELIVERY-SET | Outputs dir holds EXACTLY the 2 deliverables    | YES  | Remove stray/internal files; add reg |

  G-DELIVERY-SET (definition): at Final Assembly, /mnt/user-data/outputs must
  contain exactly { [ExamCode]_Mock[N]_Create.docx, [ExamCode]_registry.json }
  — no more, no fewer. A standalone answer-key file, a leaked internal sidecar,
  or a missing registry → Exit 1. This is the machine-checkable form of the
  S13-6 closed contract (identical to S13-7 items 4–6) and runs inside the S13-2
  sweep so the off-spec set is caught even if S13-7 is skipped.

  v3.6 adds 1 new gate (→ 50), enforced both per-batch (S4-11) and in the S13-2
  Final-Assembly gate sweep:

  | Gate Code         | Checks                                              | Fix? | Fix                                       |
  |-------------------|-----------------------------------------------------|------|-------------------------------------------|
  | G-STIMULUS-ORPHAN | Every linked Q carries its stimulus in its own block| YES  | Embed stimulus per member (Model A, §9)   |

  G-STIMULUS-ORPHAN (definition): for one-question-at-a-time online rendering,
  any question depending on a shared passage / table / chart / cloze paragraph
  must physically contain that stimulus in its own block (§9 Model A), unless the
  platform is confirmed to support engine-native passage-groups (Model B). A
  "lead-in only" layout (stimulus before Q1, absent from Q2..Qn) or any
  "Q.X and Q.Y" cross-reference text in a stem → Exit 1. Not fixable by deleting
  the questions — fix by embedding the stimulus into each member.

  v3.7 adds 1 new gate (→ 51), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code     | Checks                                                  | Fix? | Fix                                       |
  |---------------|---------------------------------------------------------|------|-------------------------------------------|
  | G-QNUM-FIRST  | Every question block opens with its "Q.<N>" paragraph   | YES  | Re-emit block: Q.N context line first     |

  G-QNUM-FIRST (definition): enforces the v3.7 Q.N-FIRST contract / R14. Every
  question block — single OR linked — must OPEN with its "Q.<N>" paragraph; no
  table, chart, passage, or unnumbered preamble may precede the Q-number. In a
  linked block the Q-number fuses with the shared context line and the specific
  ask is a separate non-numbered bold paragraph. A block opening with a
  stimulus/preamble, or carrying a stray second Q-number, → Exit 1. Fix by
  re-emitting via S10-LINKED (add_qn_context → stimulus → add_specific_ask).

  v3.8 adds 1 new gate (→ 52), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code   | Checks                                                        | Fix? | Fix                                          |
  |-------------|---------------------------------------------------------------|------|----------------------------------------------|
  | G-FORMATDUP | No CLASS-2/3 CONCEPT_GROUP clones (same presentation_key)      | YES  | Regenerate on a new stem-format/distractor   |

  G-FORMATDUP (definition): enforces RULE C / §6-3c. For CLASS-2 (vocabulary/
  item-recall) and CLASS-3 (fact-recall) questions, two questions sharing a
  CONCEPT_GROUP may not share presentation_key = (stem_format_variant |
  distractor_strategy); a different target word/fact (distinct scenario_key) does
  NOT excuse an identical look. When a CONCEPT_GROUP has ≥3 questions, ≥2 distinct
  stem_format_variants must appear. A CLASS-2/3 question with no presentation_key
  (generator did not pick a defined variant) also fails. This is the gate that
  catches the M1 Q.77/Q.79 (Antonym) and Q.78/Q.80 (Synonym) clones. Fix by
  regenerating the offending question on a new presentation (§6-3c menus); never
  reduce N. The companion R19 v3.8 spacing (G-CLUSTER manual check) prevents
  same-family clustering.

  v4.0 adds 1 new gate (→ 53), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code            | Checks                                                         | Fix? | Fix                                     |
  |----------------------|---------------------------------------------------------------|------|-----------------------------------------|
  | G-FIGURAL-COMPOSITE  | Figural Q decomposed: problem img + 1 img/option, 1 per line   | YES  | Re-render discrete images (S10-7/S10-8)  |

  G-FIGURAL-COMPOSITE (definition): enforces R-FIGURAL / §10-S10-7/S10-8. A figural
  question must render as the problem figure(s) plus ONE separate image per option,
  stacked single-column (one option image per line) and bound 1:1 to its "i."
  label. A figural block with fewer than (n_options + 1) inline images — the
  canonical case being a SINGLE composite panel with the problem and all options
  baked together — or any line/table-row carrying more than one option image, or a
  "1. Figure 1" dummy-text option in place of an image → Exit 1. This is the gate
  that catches the M1-class composite (the SSC CGL T1 Q5 panel). Not fixable by
  editing text: re-render the figures discretely (S10-7) and re-emit via
  add_figural_question (S10-8). Image-quality (300 DPI, uniform option canvas, no
  baked-in chrome, real reference geometry) is enforced upstream at view-tool
  verification per S10-7.

  v4.1 adds 1 new gate (→ 54), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code   | Checks                                                          | Fix? | Fix                                       |
  |-------------|----------------------------------------------------------------|------|-------------------------------------------|
  | G-UNDERLINE | Underline-class Q renders a REAL underlined run, not "(underlined: X)" text | YES | Re-render via S10-2 add_stem_with_underline |

  G-UNDERLINE (definition): enforces R-UNDERLINE / §10-S10-2. Any question whose
  stem refers to an underlined element (UNDERLINE_TRIGGER_RE, or persisted
  stem_format_variant == 'sentence_embedded_underlined') must carry its target span
  as a genuine underlined run (<w:u>) inside the sentence. Exit 1 if the block
  contains a "(underlined: …)"/"(underline: …)" plain-text annotation, OR if no run
  in the block carries underline formatting. This is the gate that catches the M1
  Q.83 ("(underlined: senior than me)") and Q.78 ("(underlined: benevolent)")
  annotations and the document-wide absence of any <w:u> run. Parallel to G-FIGTEXT
  (figural-as-text); here it is underline-as-text. Not fixable by editing the note:
  re-render the carrier sentence via add_stem_with_underline so the target is a real
  underlined run, and drop the parenthetical.

  v4.2 adds 2 new gates (→ 56), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code | Checks                                                              | Fix? | Fix                                          |
  |-----------|--------------------------------------------------------------------|------|----------------------------------------------|
  | G-OPTREF  | Stem-referenced terminal/escape option exists & is positioned right| YES  | Add the escape option / switch template      |
  | G-UNIQUE  | Each Q has answer_verified==true (R-ANSWER ran)          | YES  | Re-run CHECK 3; disambiguate stem if needed  |
  | G-QINDEX  | question_index certified: one {q,subtopic_id,difficulty} per Q; ids ∈ blueprint; difficulty ∈ labels; distribution == schedule[N] (v5.2) | YES | Fix S7-NEW-A capture / schedule-first assign; rebuild index (S13-4) |

  G-OPTREF (definition): enforces R-OPTREF / §10-S10-2. If a stem REFERENCES a
  terminal/escape option — "if no error → (the) last option", "select 'No
  improvement'", "None of these / the above", "All of the above", "Both … and …",
  "Neither … nor …" — that option MUST be present in the option set, at the position
  the instruction names. A "pick the segment with the error" layout (all four options
  are sentence segments) may not carry a "no error → last option" escape unless a real
  "No error" option is appended. This is the gate that catches the M1 Q.100 mismatch
  (4 segments + a "no error → last option" instruction with no "No error" option).
  EXAM-AGNOSTIC: escape tokens and option structures come from section_rules
  (none_of_above_map S3-12, wrong_option_structure S3-13); the gate enforces coherence
  only, hardcoding no exam wording. Carrier-sentence run-ons (instruction + sentence on
  one line) are prevented by the §10-S10-2 two-paragraph layout. Fix by appending the
  escape option (re-balance K-BAL) or switching to the matching template.

  G-UNIQUE (definition): enforces R-ANSWER. Answer uniqueness is decided at GENERATION
  (§7 CHECK 3 verify_answer) because verbal ambiguity needs reasoning, not
  regex; G-UNIQUE is the record-presence backstop (same pattern as G-CONCEPTDUP reading
  concept_map). Any question whose sidecar lacks answer_verified == true →
  Exit 1: generation skipped the contract. This is the gate behind the M1 Q.3
  (Sister vs Cousin, paternal/maternal split) and Q.98 (is vs was, universal-truth
  convention) — each had a SECOND defensible option. EXAM-AGNOSTIC; the uniqueness
  classes are universal and any contested convention is pinned in section_rules, never
  hardcoded. Fix by re-running CHECK 3 and disambiguating the stem (qualify the
  relation / pin the convention / constrain the rule) or dropping the colliding option.

  v4.3 adds 1 new gate (→ 57), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code     | Checks                                                          | Fix? | Fix                                       |
  |---------------|----------------------------------------------------------------|------|-------------------------------------------|
  | G-MATH-RASTER | No built-up math shipped as an image; inline rasters are named figures/stimuli only | NO | Re-render expression as OMML (S10-4 add_math_stem); drop the raster |

  G-MATH-RASTER (definition): enforces R-MATH-OMML / §10-S10-4. Every algebraic or
  built-up expression (stacked fraction, exponent, radical, trig-with-fraction —
  S10-4 decision-tree rules 3-6) must render as native OMML (<m:oMath>) inline in
  the document text, NEVER as a raster image. The gate's authoritative signal is
  the figural image NAME-CONTRACT: the only legitimate producers of an inline
  raster are the figural emitter (§10-S10-8, names q{N}_problem[_k] / q{N}_opt{i})
  and the linked-stimulus path (§9, names q{N}_stim[_tag]); any inline <w:drawing>
  whose pic name falls OUTSIDE the pattern ^q\d+_(problem|opt\d+|stim) is an
  unauthorised raster → Exit 1. This is the gate that catches the M1 Q.55 defect
  (q55_e1.png / q55_e2.png — "x + 1/x = 5" and "x²+1/x²" rasterised at 300 DPI via
  matplotlib instead of OMML). The name-contract is provenance-proof: it reads the
  image, so a faked figural-manifest entry cannot smuggle a math raster past it, and
  it cannot false-positive on a genuine figure (named by the S10-8 convention) —
  validated in Python against the actual failing file (flags Q.55's two rasters,
  zero of the six genuine figural questions Q.3/10/12/16/19/22). Math-context stem
  detection and math image-name tokens (_e1, _eqn, _frac…) are reported as
  corroborating diagnostics only. Parallel to G-FIGTEXT (figural-as-text) and
  G-UNDERLINE (underline-as-text); here it is math-as-raster. NOT fixable by editing
  text: re-render the expression through §10-S10-4 add_math_stem / emit_math_inline
  (interleave <m:oMath> with the stem text) and delete the raster; if a flagged image
  is a genuine figure that was mis-named, re-emit via add_figural_question (§10-S10-8)
  so it carries the canonical q{N}_problem / q{N}_opt{i} name. The companion G-FRAC
  continues to catch the slash/caret ASCII fallback in the text stream.

  All 39 gates from v1.0 unchanged. See v1.0 §18 for full table.

  v4.5 adds 3 new gates (→ 60), MULTI-mode only (fully dormant when blueprint
  multi_present is false), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code   | Checks                                                            | Fix? | Fix                                          |
  |-------------|------------------------------------------------------------------|------|----------------------------------------------|
  | G-MSQ-SET   | MSQ key is a non-empty PROPER subset of 1..n; AOTA rule honored   | YES  | Regenerate so |S| is 1..n−1; drop AOTA if banned |
  | G-MSQ-CARD  | fixed-k exams: |S| == msq_k                                        | YES  | Regenerate the set to the instructed count   |
  | G-MSQ-INSTR | the multi instruction line is present in the Q.N stem (R14)       | YES  | Re-emit stem with instruction on the Q.N line |
  | G-NAT-NOOPT | NAT question renders ZERO option paragraphs (R4/R13 exempt)        | YES  | Re-emit as a 0-option NAT block (stem only)   |
  | G-NAT-ANSWER| NAT value well-formed for nat_answer_type; ca_range lo<=hi         | YES  | Regenerate value/band per nat_contract        |
  | G-NAT-GRADE  | portal grading value/type well-formed (0-9.- charset), deterministic | YES  | Re-run derive_nat_grading(); rework Q if NOT-SUPPORTED negative-range |
  | G-NAT-INSTR | the numerical-entry instruction is present in the Q.N stem (R14)   | YES  | Re-emit stem with nat_instruction on Q.N line |

  G-MSQ-SET (definition): enforces the structural half of R-ANSWER (multi) + R-MSQ-ESCAPE.
  Runs ONLY for sidecar concept_map entries with answer_cardinality=='multi' (skipped entirely
  when multi_present is false). The correct set S = answers[q] (a list[int]) must be a
  NON-EMPTY PROPER subset of {1..total_options}: k=0 (empty), out-of-range, and k=n
  (all-correct) are all defects. R-MSQ-ESCAPE: an "All of the above" option under multi is
  a defect unless section_rules msq_allow_aota=true (read into msq_meta). EXAM-AGNOSTIC —
  total_options/k-config come from msq_meta (blueprint/section_rules), no exam wording
  hardcoded. Validated in Python against real MSQ docx fixtures (catches k=0, k=n, and an
  AOTA option when the flag is false; passes a clean variable-k set). NOT fixable by
  editing the key — regenerate the question with a well-formed intended set.

  G-MSQ-CARD (definition): enforces the fixed-k cardinality of R-ANSWER (multi). Runs ONLY
  when answer_cardinality=='multi' AND msq_meta.msq_k_mode=='fixed'. For "Select TWO"/"Select
  THREE" exams it guarantees |S| matches the instructed k. Variable-k exams skip it (no
  fixed cardinality). Fix by regenerating the set to the configured count.

  G-MSQ-INSTR (definition): enforces R14 placement of the MSQ instruction. Runs ONLY for
  answer_cardinality=='multi'. The select-instruction ("(One or more options may be correct)" /
  "(Select TWO)" / localized equivalent from section_rules) MUST live INSIDE the bold
  Q.<N>-first stem paragraph — there is NO paper-level instructions page, and a separate
  instruction paragraph would break R14 / G-QNUM-FIRST. Step 7's gate is a record-presence
  backstop (msq_instr_in_stem flag in the sidecar, same pattern as G-UNIQUE); Step 8's
  independent audit (A-MSQ-INSTR) re-checks the docx Q.N line directly. Fix by re-emitting
  the stem with the instruction appended to the Q.<N> line (never as its own paragraph).

  v5.0 adds 2 new gates (→ 65), Issue 2b, enforced per-batch (S4-11) and in the
  S13-2 sweep. Both DORMANT when their manifest structure is empty (no false stop):

  | Gate Code      | Checks                                                         | Fix? | Fix                                              |
  |----------------|---------------------------------------------------------------|------|--------------------------------------------------|
  | G-GROUPMANDATE | ≥min members of each manifest.mandatory_groups group generated | YES  | Regenerate so ≥min members appear (Step 1 M4)    |
  | G-MINCOUNT     | ≥k generated questions for each manifest.min_counts id          | YES  | Regenerate to reach k (Step 1 M6)                |

  G-GROUPMANDATE (definition): exam-agnostic post-gen backstop to S3-17 CHECK 3, mirroring
  G-ALTGROUP. Reads manifest.mandatory_groups {group:{members:[ids],min}} and the per-
  subtopic_id counts from the mock's concept_map (the SAME generated-reality counts
  G-ALLOC-SUBTOPIC uses). A group with fewer than `min` members carrying ≥1 generated
  question fails. Expresses "≥1 of a subtopic GROUP per mock" (e.g. any one member of a
  solid-geometry group) — which mandatory_every_mock cannot, since it would force ALL
  members. No subtopic name hardcoded; empty mandatory_groups ⇒ pass.

  G-MINCOUNT (definition): exam-agnostic post-gen backstop to S3-17 CHECK 4. Reads
  manifest.min_counts {id:k} and the same per-subtopic_id generated counts; an id with
  fewer than k generated questions fails. Expresses "≥k Q of this subtopic per mock" —
  the generalisation of mandatory_every_mock from ≥1 to ≥k. No name hardcoded; empty
  min_counts ⇒ pass. DELIBERATELY there is NO companion cadence gate: manifest.
  cadence_windows ("≥1 every N mocks") is a CROSS-mock constraint, unobservable from one
  mock, and is enforced solely by Step 1 RULE M5 (full-series pass). Adding a Step 7
  cadence gate would false-stop every legitimately-skipped mock.

  v5.18 adds 1 new gate (→ 67), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code | Checks                                                        | Fix? | Fix                                     |
  |-----------|---------------------------------------------------------------|------|-----------------------------------------|
  | G-PREQ1   | No non-blank paragraph before Q.1 (title/info/scoring/cover)  | YES  | Delete the pre-Q.1 paragraphs from docx |

  v5.19 adds 1 new gate (→ 68), per-batch (S4-11 fallback) + Step-8 audit A-MATCH-TABLE:

  | Gate Code     | Checks                                                        | Fix? | Fix                                        |
  |---------------|---------------------------------------------------------------|------|--------------------------------------------|
  | G-MATCH-TABLE | Every match question renders its List columns as a real table | YES  | Re-emit via add_match_table() (§10-S10-3M) |

  G-PREQ1 (definition): the generated paper is questions-only at the DOCUMENT level — the
  first non-blank body paragraph must be the bold "Q.1" stem. Any title, "Total Questions /
  Maximum Marks / Time" line, "Each question carries ... Negative marking ..." instruction, or
  cover/preamble before Q.1 → Exit 1 (R8b). CATEGORY-C values (marks_per_q, time_per_q_sec,
  negative_marking, options_count, total_questions) are structured metadata in section_rules.md
  / blueprint.json / registry and are NEVER printed in the paper; a downstream platform may
  render them from that metadata. Blank separators before Q.1 are ignored. DORMANT only if
  section_rules.md EXAM_STRUCTURE declares paper_header_block (a deliberate per-exam opt-in; no
  current exam declares it). Independently re-verified by Step 8 A-HEADER (which strips the
  block rather than validating it).

# ════════════════════════════════════════════════════════════════════════
# §19 — EDGE-CASE CHECKLIST (v2.0 — additions marked *)
# ════════════════════════════════════════════════════════════════════════

  All items from v1.0 + these additions:

  BATCH ENFORCEMENT (§4 v3.0 — most critical):
  □ ONE batch = ONE response (never two batches in one response)  **
  □ Each non-final batch ends with "Type 'continue' to begin Batch [N+1]."  **
  □ Each non-final batch response ENDS after the continue prompt (S4-7 STEP F)  **
  □ No batch was auto-advanced within the same response (B-4)  **
  □ Every batch generated exactly q_count Qs from batch_state.json (B-3)  **
  □ No batch spanned two sections (S4-1)  **
  □ Q-range read from batch_state.json, never from memory (B-2)  **
  □ Pre-batch self-check (S4-5) performed before each batch  **
  □ Only the user's "continue" started each next batch (B-5)  **
  □ Final batch auto-ran Final Assembly, no continue prompt (S4-9)  **
  □ batch_state.json updated after each delivery (S4-8a)  **
  □ Manual gate checklist completed per batch (if no audit.py) (S4-11)  *

  FONT:
  □ All text uses configured font (FONT_NAME, FONT_SIZE_PT)  *
  □ Stems: configured font, configured size, bold  *
  □ Options: configured font, configured size, normal  *

  OPTIONS:
  □ Labels match OPTION_LABEL_FMT (configured format)  *

  STRUCTURE:
  □ No section headings in docx body  *
  □ No title/info/scoring/cover block before Q.1 — first non-blank paragraph is "Q.1" (R8b, G-PREQ1)  *
  □ No answer key page at end of docx  *
  □ No figural text placeholders  *

  FIGURAL (v5.13 — R-FIGURAL / §10-S10-7/S10-8/S10-8A):
  □ Each figural Q correctly structured per its image_role:
    stem_and_options → problem PNG(s) + option PNGs (add_figural_question)
    stem_only → problem PNG(s) + text options (add_figural_stem_question)
    options_only → text stem + option PNGs (add_figural_question, empty problem)  ****
  □ Options single-column — one option image per line, never two on a line  ****
  □ Each option image bound 1:1 to its "i." label; no "1. Figure 1" dummy text  ****
  □ No composite panel (problem + options fused into one image)  ****
  □ No stem/caption/option-number baked into any raster (intrinsic figure
    annotations like M/N, vertices, axis labels are allowed)  ****
  □ Reference lines (mirror line MN, number line, axis) drawn as real geometry  ****
  □ All option images 300 DPI, lossless PNG, uniform square canvas  ****
  □ G-FIGURAL-COMPOSITE passes at batch and Final Assembly  ****

  ALLOCATION COUNT + SCENARIO UNIQUENESS (DOUBT-3 — both rules, v3.2):
  □ Each subtopic has EXACTLY its blueprint q_count — floor and ceiling (RULE A)  ***
  □ No two questions in the mock share a scenario_key (RULE B)  ***
  □ No scenario duplicated by changed values, names, or reworded text  ***
  □ Subtopics allocated 2+ Q use a DISTINCT scenario for each question  ***
  □ N>distinct-PYQ-patterns handled by inventing new distinct scenarios (no cap)  ***
  □ scenario_key uniqueness is mock-global (also across different subtopics)  ***
  □ concept_ledger in batch_state.json reflects every accepted Q's scenario_key  ***
  □ G-CONCEPTDUP, G-ALLOC-SUBTOPIC, G-COUNT-X-UNIQUE all PASS at Final Assembly  ***

  MANDATE COMPLIANCE (exam-agnostic — v5.0; no subtopic names):
  □ Every manifest.mandatory_every_mock id present in this mock (S3-17 + G-ALLOC-SUBTOPIC)  *
  □ ≤1 member of each manifest.alternation_groups group in this mock (S3-17 + G-ALTGROUP)  *
  □ Cross-mock variant rotation honored where a ROTATION cycle is declared (S6-9)  *
  □ (Issue 2b) ≥min members of each manifest.mandatory_groups group present (S3-17 CHECK 3 + G-GROUPMANDATE)  *
  □ (Issue 2b) ≥k questions for each manifest.min_counts id (S3-17 CHECK 4 + G-MINCOUNT)  *
  □ (Issue 2b) cadence (≥1 every N mocks) enforced in Step 1 RULE M5 — NOT gated here (cross-mock)  *

  REGISTRY:
  □ pending_registry initialised at S3-4 session start  *
  □ content_tracking, image_phashes, session_log initialised at Mock 1  *
  □ No registry writes during generation (only pending_registry)  *

  TECH STACK:
  □ Python + python-docx used (not npm docx) for math-containing sections  *
  □ OMML used for all fractions/surds/exponents (not slash/caret notation)  *
  □ DI table uses Word table XML (not pipe-delimited plain text)  *


# ════════════════════════════════════════════════════════════════════════
# APPENDIX A — AUDIT SCRIPT BOOTSTRAP (GAP-01 permanent fix)
# ════════════════════════════════════════════════════════════════════════
#
# v5.11 NOTE: Step 6 (MockBlueprint) v1.20+ now AUTO-GENERATES this script
# as its 6th output file. Users no longer need to create it manually.
# See Framework_Blueprint.md §13-7A for generation rules, collision handling,
# upgrade path, and lifecycle.
#
# CANONICAL AUDITOR — SINGLE SOURCE OF TRUTH (v5.17)
# ────────────────────────────────────────────────────────────────────────
#   The Step-8 auditor is NO LONGER a separate "minimum-viable" script embedded here.
#   The ONE canonical, exam-agnostic auditor is the repo engine file
#       audit_canonical.py   (hash-tracked; formerly CreateAudit Appendix A)
#   and it is the ONLY auditor the pipeline generates or runs. It carries the full A-*
#   gate catalogue, the --audit-state COMPLETION GATE (S5-1A, C1-C7 + on-disk evidence
#   checks), and a FIXTURE-BASED self-test (builds tiny docx fixtures; asserts each gate
#   CATCHES a planted defect and PASSES a clean one; SELF-TEST: N/N with N >= 35 — the
#   canonical build self-tests 78/78).
#
#   RETIRED (do NOT generate, copy, or use): the old 13-gate "minimum-viable" embedded
#   script whose self_test() was a CONSTANT print ("SELF-TEST: 13/13 PASS") that executed
#   NO gate. That hollow stub is exactly what let a truncated/dead auditor pass the P1
#   self-test check and ship a false-clean paper (root cause documented in
#   Framework_MockTestCreateAudit.md v2.6). It is REMOVED here so it can never be copied
#   again. MVP_GATE_COUNT and the 13-vs-66 two-build split no longer exist.
#
#   HOW THE SCRIPT IS BORN (Step 6 B3 — Framework_Blueprint.md §13-7A):
#     B3 writes [ExamCode]_mock_test_audit.py by copying, VERBATIM, the repo engine
#     file audit_canonical.py (hash-tracked + bootstrap-verified; the single source of
#     truth since CreateAudit v2.11.2 — formerly the fenced python block in
#     Framework_MockTestCreateAudit.md Appendix A). No exam-specific edits are
#     needed — the script parameterises itself from blueprint.json / section_rules.md /
#     subtopic_manifest.json / registry.json at runtime. B3 then VALIDATES:
#         python3 [ExamCode]_mock_test_audit.py --self-test
#       → MUST print "SELF-TEST: N/N PASS" with N >= 35 AND be fixture-based.
#         A constant-print "N/N PASS" (no fixtures) is REJECTED → regenerate.
#
#   STEP 7 (this spec) still uses audit.py OPTIONALLY for its per-batch self-audit; it runs
#   the SAME canonical script (its --self-test and Part-A gates work standalone). If absent
#   → WARN + manual checklist (S4-11), unchanged.
#
#   The full ~1200-line script body is intentionally NOT duplicated here: a SINGLE canonical
#   copy is what prevents the three-way drift (13 / 35 / 66) that this fix eliminates.

# ════════════════════════════════════════════════════════════════════════
# APPENDIX B — M1 DEFECT LOG (permanent record for SSC_CGL_TIER1)
# ════════════════════════════════════════════════════════════════════════
#
# Mock 1 (SSC_CGL_TIER1) was generated in production before v2.0 framework.
# The following defects were confirmed and must be fixed in regeneration:
#
# M1-D01: All 100 questions generated in one response (batch enforcement violated)
# M1-D02: Section headings ("SECTION: General Intelligence...") in docx body — R8 violation
# M1-D03: Answer key page embedded at end of docx — R5/R12 violation
# M1-D04: Font is Arial (not Calibri 11pt)
# M1-D05: Option labels use "(1)" format (not "1.  text" format)
# M1-D06: DI table as plain text pipe-delimited (not Word table XML)
# M1-D07: OMML not used for math (npm docx package used — cannot produce OMML)
# M1-D08: Figural questions delivered as text descriptions
# M1-D09: Direction Sense absent from GIR (MANDATORY every mock)
# M1-D10: Address Matching absent from GIR (MANDATORY every mock, 2025)
# M1-D11: Mensuration 3D absent from QA (MANDATORY every mock)
# M1-D12: Both Simple Interest AND Compound Interest in M1 (alternation violated)
# M1-D13: pending_registry not used — registry written directly during generation
# M1-D14: content_tracking L4-L18 fields absent from registry
# M1-D15: progress.json never written (passage_linked_qs/cloze_linked_qs lost)
# M1-D16: answer_key sidecar JSON never created
# M1-D17: GIR pair rotation (A/B/C) not applied
# M1-D18: Question content visible in chat (print() debug statements — MANDATE 0 violation)
# M1-D19: MANDATE 0 violated (stem text visible in verification output)
# M1-D20: batch_state.json built but not consulted per-batch for gated stops
#
# STATUS: M1 is a known-defective mock. Recommend regenerating M1 with v2.0 spec.
# M2 onwards: follow v3.0 spec. All 20 defects addressed; batch logic hardened.

# ════════════════════════════════════════════════════════════════════════
# APPENDIX C — BATCH PROCESSING QUICK REFERENCE (v3.0)
# ════════════════════════════════════════════════════════════════════════
#
# The one-page summary every Step 7 session must internalise:
#
# 1. SESSION START: run all S3 checks → build batch_state.json →
#    show batch plan → print "Type 'continue' to begin Batch 1." → STOP.
#
# 2. EACH "continue": run S4-5 pre-batch self-check → generate EXACTLY
#    q_count Qs for current_batch (from batch_state.json) → gate check →
#    report → present_files → update batch_state → print continue prompt →
#    *** END RESPONSE ***.
#
# 3. ONE BATCH = ONE RESPONSE. Never two batches in one response.
#    Never auto-advance. Only the user's "continue" starts the next batch.
#
# 4. FINAL BATCH (is_final=True): no continue prompt — auto-run Final
#    Assembly in the same response, then end.
#
# 5. NEVER print question content in chat (MANDATE 0).
#
# 6. audit.py: OPTIONAL for Step 7 (manual checklist S4-11 substitutes).
#    MANDATORY for Step 8. If absent in Step 7 → WARN, use manual checklist.
#
# THE M1 FAILURE: all 100Q in one response. THE v3.0 FIX: §4 B-4 + S4-7
# STEP F + MANDATE 1 STEP 6 make that mechanically impossible.

# ════════════════════════════════════════════════════════════════════════
# END OF Framework_MockTestCreate v5.34.1
# Version: 5.8 | Date: 2026-07-04
# (Full per-version rationale was RELOCATED 2026-07-31 to CHANGELOG.md, section
#  'ARCHIVE — Framework_MockTestCreate' — that archive is authoritative for history.
#  The v1.0→v3.9 summary below is retained for continuity only.)
# v1.0 → v2.0: 20 production gaps fixed after M1 live failure
# v2.0 → v3.0: definitive batch-processing rewrite (§4); audit.py answer locked
# v3.0 → v3.1: DOUBT-3 intra-mock concept-uniqueness (first pass)
# v3.1 → v3.2: DOUBT-3 allocation-count (RULE A) + scenario-uniqueness (RULE B);
#              10 bugs fixed
# v3.2 → v3.3: DOUBT-3 final hardening — 7 issues fixed (L3 fix, per-Q concept_map
#              persistence, 4 subtopic CLASSES incl. linked-stimulus & vocabulary,
#              cross/intra-mock boundary, resume-safe ledger)
# v3.3 → v3.4: subtopic_id contract (join blueprint↔section_rules by id, §20)
# v3.4 → v3.5: delivery-contract hardening (§13 executable steps; closed 2-file
#              deliverable set; G-DELIVERY-SET; R-DELIVER)
# v3.5 → v3.6: linked-question self-containment (§9 full rewrite; Model A default
#              stimulus-per-member; R-LINKED; G-STIMULUS-ORPHAN; S10-LINKED helper)
# v3.6 → v3.7: Q.N-FIRST block contract — every block opens with "Q.<N>"; linked
#              order = Q.N context → stimulus → ask; R14 generalised; G-QNUM-FIRST
# v3.7 → v3.8: DOUBT-4 presentation-uniqueness — RULE C presentation_key (§6-3c)
#              for CLASS 2/3; CHECK 1b in the generation loop; G-FORMATDUP;
#              R19 anti-clustering. Fixes same-concept clones (Q.77/79, Q.78/80)
# v3.8 → v3.9: v3.8 hardening (deep audit) — 6 integration gaps closed:
#              classify_subtopic()+SUBTOPIC_CLASS populated; menu/family helpers
#              defined; presentation_ledger persisted+resumed; build_question
#              render-consistency + verify_presentation_match; G-FORMATDUP selects
#              by class (missing-key now caught); RULE C requires distinct visible
#              stem_format. No new gate/rule — pure closure.
# Total guard gates: 80 (see the §12 catalogue + §17 DoD, current through v5.33; the
#   per-batch/Final-Assembly gate set — MSQ gates dormant unless multi_present, NAT gates
#   dormant unless nat_present; G-GROUPMANDATE/G-MINCOUNT dormant unless their manifest
#   structure is non-empty; G-PREQ1 dormant only if EXAM_STRUCTURE declares paper_header_block)
# Total rules: R1-R24 (incl. R8b) + R-DELIVER + R-LINKED + R-FIGURAL + R-UNDERLINE + R-OPTREF
#   + R-ANSWER + R-MSQ-ESCAPE + R-MATH-OMML
# Batch enforcement: Layer 1 (spec STOP, no audit.py needed) + Layer 2 (audit.py)
# Zero hardcoded exam values
# ════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════
# §20 — SUBTOPIC_ID CONTRACT (v3.4 — joiner role)
# ════════════════════════════════════════════════════════════════════════
#
# Step 7's role in the cross-step contract (full contract authored in Step 0 §15):
#   Step 0 MINTS subtopic_id, publishes [ExamCode]_subtopic_manifest.json.
#   Step 1 CONSUMES it (assigns ids, enforces mandates at build time).
#   Step 7 (THIS step) JOINS blueprint ↔ section_rules ON subtopic_id.
#
# WHAT CHANGED IN v3.4 (and why your M1 hard-stopped before it):
#   The pre-v3.4 checks matched subtopics by display-name string. On SSC CGL T1,
#   ~70% of blueprint names did not match section_rules names (Step 0 and Step 1
#   each derived names independently). So:
#     - S3-8 flagged 144/208 subtopics as "unrecognised" (would generate them
#       with no PYQ guidance).
#     - S3-17 used hardcoded literals ('Mensuration 3D', 'Direction Sense', ...).
#       The blueprint had 3D mensuration under granular names ("Right Circular
#       Cone" etc.), so the literal check FALSELY reported it absent → HARD STOP.
#   v3.4 removes string-matching entirely. Joins are by subtopic_id, which all
#   three steps now share via the manifest. False "absent" alarms are impossible.
#
# THE THREE GUARANTEES (why this never breaks again, for 100 exams):
#   1. JOIN BY ID: S3-8 joins blueprint ↔ section_rules on subtopic_id. The
#      display name is decorative; nothing matches on it.
#   2. CONTRACT GATE: every blueprint id must exist in BOTH the manifest AND
#      section_rules, else HARD STOP naming the exact id (no silent Zero-PYQ
#      fallback that would quietly degrade quality).
#   3. MANDATES BY DATA: S3-17 reads manifest.mandatory_every_mock and
#      manifest.alternation_groups (structured data minted by Step 0). Zero
#      subtopic names are hardcoded anywhere in Step 7. Works for any exam.
#
# REQUIRED INPUT (S3-1): [ExamCode]_subtopic_manifest.json must be in the
#   project Files section alongside section_rules.md and blueprint.json. It is a
#   hard dependency; its absence is HS-9.
#
# RELATIONSHIP TO CONCEPT-UNIQUENESS (DOUBT-3, §6/§7): subtopic_id is the
#   cross-step JOIN key; concept_group/scenario_key are the intra-mock UNIQUENESS
#   keys. They are INDEPENDENT by design — a subtopic_id identifies WHICH subtopic;
#   scenario_key identifies WHICH concept within the generated questions. Do not
#   conflate them.
# ════════════════════════════════════════════════════════════════════════
