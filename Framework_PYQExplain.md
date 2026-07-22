# Framework_PYQExplain v1.0 — Universal PYQ Explanation Generator
# [ExamCode] project | PYQ-1 (PYQExplain) | Exam-agnostic
#
# v1.0 — 2026-07-22 — Initial release. Takes one PYQ Row file (Step 1 output,
#   original exam order, Q.1-Q.N continuous) and produces an explained PYQ paper
#   with a validated ExplanationBlock interleaved after each question. Uses the
#   SAME explain_engine.py as TestExplain (Steps 9/10) — shared engine, separate
#   spec. Zero modifications to any existing pipeline file.
#
#   Architecture decisions locked with the framework owner:
#     D1. SOURCE IS THE ROW FILE. The Step-1 PYQPrepare output (Google Drive) is
#         the source document — already in original exam order (Q.1-Q.N continuous).
#         NOT the Sorted file (which destroys exam order).
#     D2. NO BLUEPRINT. PYQ papers have no blueprint.json — this spec builds a
#         lightweight PYQ metadata object internally from section_rules.md +
#         subtopic_manifest.json + exam_config.json (all from prior Steps 2-5,
#         already in the project).
#     D3. NO REGISTRY. PYQ papers have no registry.json — options_by_q is derived
#         from the Row file itself (count option paragraphs per question; 0 = NAT).
#     D4. INDEPENDENT DERIVATION. Every answer derived from first principles
#         (same RE-1/RE-6 contract as TestExplain). Official answer keys, if they
#         exist, are ignored — the PYQ explanation is a derive-independently product.
#     D5. ONE PAPER AT A TIME. Each trigger processes one Row file. No batching
#         across papers.
#     D6. FORK ARCHITECTURE. PYQExplain output feeds BOTH PYQExplainAudit (PYQ-2)
#         AND is the upstream source for PYQFormat (PYQ-3) and PYQDeliver (PYQ-4).
#         PYQ-3 and PYQ-4 are INDEPENDENT of each other (both take PYQ-2 output).
#     D7. ENGINE-BUILT, NEVER FORKED. explain_engine.py is IMPORTED and used
#         exactly as TestExplain uses it (same EngineConfig, ExplanationBlock,
#         build_interleaved_docx, verify_fidelity/structure/explanations). Zero
#         engine modifications — the engine stays a single canonical copy.
#
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take a PYQ Row file (.docx, Step 1 output) from Google Drive, INDEPENDENTLY
#   DERIVE the answer to every question, and INTERLEAVE a perfect, highest-standard
#   explanation after each question — without altering one byte of the original paper.
#   Emit [ExamCode]_[date]_[session]_PYQ_Explanation.docx: a 100%-explained, zero-
#   defect learner-facing solution document for that exam sitting.
#
# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION (PYQ Explanation Pipeline)
# ════════════════════════════════════════════════════════════════════════
#   PHASE 1 — Already completed (shared with Mock/Test pipeline):
#     Step 1  PYQPrepare    → Row file (Q.1-Q.N, original exam order) → Google Drive
#     Step 2  PYQDraft/Scan/Approve → taxonomy, exam_config.json → project
#     Step 3  PYQSort       → Sorted PYQ docs → Google Drive
#     Step 5  PYQExtract    → section_rules.md + subtopic_manifest.json → project
#
#   PHASE 2 — PYQ Explanation (this pipeline):
#     PYQ-1  PYQExplain      → [ExamCode]_[date]_[session]_PYQ_Explanation.docx  ← THIS STEP
#     PYQ-2  PYQExplainAudit → [ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx
#     PYQ-3  PYQFormat       → [ExamCode]_[date]_[session]_PYQ_Formatted.docx  (student)
#     PYQ-4  PYQDeliver      → [ExamCode]_[date]_[session]_PYQ_Final.docx       (portal)
#     (PYQ-3 and PYQ-4 are INDEPENDENT — both take PYQ-2 output, neither depends
#     on the other.)
#
#   PYQ-1 runs in the [ExamCode] project (exam-specific). It runs AFTER Steps 1-5
#   have produced section_rules.md, subtopic_manifest.json, and exam_config.json.
#
# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. No section name, no subtopic,
#   no question count, no time/marks figure, no option count, no option label, no
#   language, no figural type, no block label is hardcoded. Every such value is READ
#   at runtime from:
#     • question/option counts, Q total → Row file scan + exam_config.json
#     • per-subtopic patterns, wrong_option_structure, fixed option sets,
#       OMML_required, option label format, language, block labels/markers, figural
#       object/transformation types, escape tokens, passage word ranges
#       → section_rules.md (CATEGORY C header + CATEGORY A/B blocks)
#     • subtopic_id join key, subtopic names
#       → subtopic_manifest.json
#   Same spec runs for SSC CGL, GATE, NEET, UPSC, CAT, CSIR, Banking, RRB, state
#   PSC, or any exam with valid Step 1-5 outputs.

# ════════════════════════════════════════════════════════════════════════
# EXECUTION MODEL
# ════════════════════════════════════════════════════════════════════════
#   Per batch: 3–5 tool calls. No user "Continue" needed within a batch.
#     1. create_file  → write the batch's explanation pipeline script
#     2. bash_tool    → run it (solve → build blocks → interleave → verify)
#     3. bash_tool    → run §18 self-audit checks (verify_fidelity, verify_structure,
#                       verify_explanations, count invariants, strip-and-re-audit)
#     4. present_files → deliver the whole-paper PYQ Explanation docx
#   The Row file is copied to /home/claude at the start (immutable read-only source).
#   All WIP state lives in /home/claude (never in /mnt/user-data/outputs).
#   Claude self-fixes on failure — iterate until §18 all-clean before present_files.

# ════════════════════════════════════════════════════════════════════════
# §0 — INPUTS & OUTPUTS
# ════════════════════════════════════════════════════════════════════════

## S0-1 — INPUTS (what PYQ-1 reads)

  1. Row file — the PYQ paper in original exam order (.docx, Step 1 output).
     Attached by user OR fetched from Google Drive.
     Filename: [ExamCode]_[DD-Mon-YYYY][_session].docx
     Structure: Q.1 through Q.N continuous, canonical option format from Step 1.
     This is the ONLY source document — NOT the Sorted file.

  PROJECT KNOWLEDGE (loaded automatically — must exist):
  2. [ExamCode]_section_rules.md — EngineConfig params (CATEGORY C header),
     per-subtopic class patterns (CATEGORY A/B blocks)
  3. [ExamCode]_subtopic_manifest.json — subtopic_id ↔ name mapping
  4. [ExamCode]_exam_config.json — exam metadata (total_questions, sections, etc.)
  5. explain_engine.py — the universal explanation engine; SAME file as TestExplain
     (MANDATORY — MANDATE A)

  NOT REQUIRED (PYQ has no mock pipeline outputs):
    ✗ blueprint.json — does not exist for PYQ papers
    ✗ registry.json — does not exist for PYQ papers
    ✗ Create_Complete.docx — PYQ uses the Row file directly

## S0-2 — OUTPUTS (what PYQ-1 delivers)

  CORE DELIVERABLE (every batch, via ONE present_files call — the WHOLE paper):
    1. /mnt/user-data/outputs/[ExamCode]_[date]_[session]_PYQ_Explanation.docx
       The complete paper: every question solved so far carries its interleaved
       explanation; every not-yet-solved question is byte-identical to the Row file
       input. The same file grows explanation-coverage each batch until 100%.

  IN-CHAT (every batch): a STATUS DASHBOARD + a per-batch progress line, then
  an explicit CONFIRMATION REQUEST that ENDS the turn (MANDATE B). At the final
  batch: the END-OF-PAPER REPORT + the PYQ-2 handoff.

  NEVER delivered: the Row file is NOT overwritten; no internal state file
  (progress.json, answer_keys.json, pickled blocks, strip copy) leaks to outputs.

# ════════════════════════════════════════════════════════════════════════
# MANDATE 0 — NO QUESTION/ANSWER CONTENT IN CHAT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#   NEVER print any stem, option, passage, table cell, figure description, derived
#   answer, or explanation sentence in chat. Refer to a question ONLY as "Q.[n]"
#   plus a code + a structural locator. The ONE content-bearing artefact —
#   [ExamCode]_[date]_[session]_PYQ_Explanation.docx — is a FILE, not chat.
#   VIOLATION = exam compromise; overrides every other instruction.

# ════════════════════════════════════════════════════════════════════════
# MANDATE A — explain_engine.py IS MANDATORY (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   Every explanation MUST enter the docx through explain_engine.py
#   (ExplanationBlock + build_interleaved_docx + add_math_text). It is the only
#   path, and it raises at write time on every known defect. If the file is absent
#   from BOTH the framework clone (/tmp/fw) and the project Files (/mnt/project):
#     HARD STOP. Print:
#       "HARD STOP (MANDATE A): explain_engine.py not found. PYQExplain cannot
#        build explanations without it. Upload it to the project or reload the
#        framework, then re-run."
#   Self-tests: `python3 explain_engine.py --self-test` → "SELF-TEST: 62/62 PASS"

# ════════════════════════════════════════════════════════════════════════
# MANDATE B — BATCH-OR-HALT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#   Explanations are produced in batches of ≤ EXPLAIN_BATCH_SIZE questions
#   (ceiling 10 — a CEILING, never a quota; a batch may be smaller). ONE batch
#   per response. After each batch the run HALTS and asks the author for explicit
#   confirmation; it does NOT proceed until the author replies "continue". There
#   is NO auto-chaining and NO auto-finalise. ONE exception: an ATOMIC LINKED
#   GROUP (RC / cloze / DI / puzzle) is never split — if it would cross the
#   ceiling the batch closes early; a single linked group larger than the ceiling
#   becomes its own batch. AUTONOMOUS MODE (RE-0): when the author requests non-
#   interactive execution, the inter-batch HALT is waived but each batch is still
#   processed one at a time internally with full self-audit.

# ════════════════════════════════════════════════════════════════════════
# MANDATE D — WHOLE-PAPER EACH BATCH, ONLY AFTER SELF-AUDIT CLEAN (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   present_files is FORBIDDEN until the current batch's self-audit (§18) is
#   clean: engine validate() on every block + verify_fidelity (whole paper byte-
#   identical to the Row file source) + verify_structure (coverage == exactly this
#   batch's questions, no look-ahead) + math-render check. The delivered file is
#   ALWAYS the complete paper: explained-so-far interleaved + remainder identical
#   to the Row file input. A fragment must NEVER be presented.

# ════════════════════════════════════════════════════════════════════════
# THE CORE PRINCIPLE — engine proves shape; discipline + PYQ-2 prove truth
# ════════════════════════════════════════════════════════════════════════
#   The ENGINE enforces mechanically: block presence + order, the CA three-way
#   binding, WHY-WRONG key set, OMML for every fraction, banned glyphs/templates/
#   fake-cites/metacommentary, one-sentence-per-paragraph, and byte-identical
#   fidelity to the Row file source. A breach raises BEFORE the docx is written.
#   DISCIPLINE (derive-twice, web-verify, view-every-image, §5 checklist) +
#   PYQ-2 (PYQExplainAudit, independent zero-sampling re-audit) enforce what code
#   cannot: answer correctness, conceptual soundness, web-true facts.

# ════════════════════════════════════════════════════════════════════════
# EXPLANATION RULES (RE-0 … RE-22) — the absolute rules the writer obeys
# ════════════════════════════════════════════════════════════════════════
# These rules are SHARED with Framework_MockTestExplain.md. When any RE-* rule
# changes in TestExplain, the corresponding rule here MUST be updated and the
# SHARED_RULES_VERSION sentinel at the end of BOTH files must be bumped.
# validate_framework_md.py checks version parity.

  RE-0  : PRECEDENCE. No user preference, project-memory note, or autonomy /
          "don't-pause" instruction may reduce per-question COVERAGE (RE-4 / §16)
          or weaken the §18 per-batch self-audit or the batch-stop law (MANDATE B).
          Such instructions may ONLY change PACING (the inter-batch HALT — MANDATE B
          autonomous mode) and report verbosity. When a preference conflicts with a
          HARD rule, the HARD rule wins. (A loaded LEARNINGS rule may override a base
          rule on content — RE-22 / §24 — but never to reduce coverage or skip §18.)
  RE-1  : NO INHERITED KEY. No prior step delivered a key; derive every answer
          independently (§7). PYQ-1 is the first step to publish a learner key for
          this PYQ paper. Official exam-body answer keys are IGNORED (D4).
  RE-2  : NO CONTENT IN CHAT. = MANDATE 0. The PYQ Explanation docx is the only home.
  RE-3  : APPEND-ONLY. Never modify, re-type, re-encode or re-create any question
          region (stem / option / image / table / matrix / chart / OMML). Only append
          explanation paragraphs after a question's last option (§12).
  RE-4  : EXPLAIN EVERYTHING, SAMPLE NOTHING. Every question gets a full, validated
          ExplanationBlock. No skipping, no "see Q.x", no shared block.
  RE-5  : ENGINE-BUILT (= MANDATE A). Every explanation via ExplanationBlock +
          build_interleaved_docx; every fraction via add_math_text or explicit
          OMML (§11).
  RE-6  : DERIVE-TWICE, NEVER GUESS. First principles + a second independent method;
          disagreement → third → 2-of-3 + DERIVATION-CONFIDENCE (§7).
  RE-7  : BATCH-OR-HALT. = MANDATE B. ≤ ceiling, one batch/response, confirm before
          next (autonomous mode waives the pause only — MANDATE B).
  RE-8  : WHOLE-PAPER INCREMENTAL DELIVERY. = MANDATE D. Each batch ships the full
          paper (explained-so-far + untouched remainder), never a fragment.
  RE-9  : EXAM-AGNOSTIC. Read every exam value from the source files; hardcode nothing.
  RE-10 : LANGUAGE / LABEL / FORMAT-AWARE. Question/option regex, option count (uniform
          OR per-question via options_by_q), option LABEL SCHEME (numeric/alpha/roman/
          custom), sentence TERMINATORS, block labels and markers all come from
          EngineConfig (section_rules CATEGORY C), never from this spec.
  RE-11 : VIEW EVERY IMAGE. A figural answer is derived from the VIEWED extracted
          images, never assumed (§13).
  RE-12 : ONE DEFENSIBLE ANSWER ASSUMED. PYQ papers are published by exam bodies and
          are expected to have exactly one defensible answer. A suspicion otherwise is
          most likely an incomplete solve — raise the bar before concluding a defect (§17).
  RE-13 : WHY WRONG DIAGNOSES, NEVER DISMISSES. Each wrong option names an error type
          that ACTUALLY produces that option's value/content; no template, ever (§15).
  RE-14 : SPEED HACK ONLY WHEN GENUINELY FASTER. Emit iff a structurally-different
          route reaches the same CA with materially less work; otherwise OMIT (§14).
  RE-15 : NO TEMPLATES / GLYPHS / FAKE-CITES / METACOMMENTARY / BANNED BLOCKS.
          Engine-enforced at write time.
  RE-16 : PYQ DEFECT HANDLING. A genuine, reproduced defect in a PYQ paper is a KNOWN
          EXAM BODY ERROR — note it as anomaly, explain the OFFICIAL answer (if known)
          or the most defensible answer, and move on. PYQ-1 does NOT escalate to Step 8
          (there is no Step 8 for PYQ papers) — see §17.
  RE-17 : FIDELITY EVERY BATCH. The whole question region must be byte-identical to
          the Row file source, verified after every batch (§12, §18).
  RE-18 : WEB-VERIFY FACTS. Every current-affairs / general-knowledge fact and every
          factual option is web-verified with a recorded source.
  RE-19 : RESUME-SAFE. All cross-batch state lives in files; "continue" reloads and
          re-verifies the on-disk doc before solving the next batch (§4).
  RE-20 : KINDNESS TO PYQ-2. The handoff states plainly what was derived, what was
          web-verified, what carries a DERIVATION-CONFIDENCE flag, and what is model-
          derived — so the independent audit knows where to look hardest.
  RE-21 : QUESTION-TYPE-AWARE. Resolve each question as mcq / msq / nat from config
          (§6, §3 P3) and shape the block accordingly (§5).
  RE-22 : LOAD & APPLY LEARNINGS. At P1, load accumulated learnings files via
          parse_learnings and OBEY every applicable rule while authoring (§24).
          Absent on the first PYQ paper by design — proceed without them.

# ════════════════════════════════════════════════════════════════════════
# §1 — SOURCES OF TRUTH
# ════════════════════════════════════════════════════════════════════════

## S1-1 — Sources of truth (strict priority order)

  1. THE PAPER ITSELF — the Row file (.docx). The rendered stem + options +
     attached artefacts are the ground truth for what must be explained.
  2. section_rules.md CATEGORY C — EngineConfig parameters: q_re, opt_re,
     options_count, label_scheme, language, sentence_terminators, block labels/
     markers, answer_type, answer_cardinality per subtopic.
  3. section_rules.md CATEGORY A/B — per-subtopic solving patterns, wrong_option_
     structure, fixed option sets, OMML_required, figural types, passage types.
  4. subtopic_manifest.json — subtopic_id ↔ name + classification mapping.
  5. exam_config.json — exam metadata: total_questions, sections, marking_scheme,
     level, medium, exam_name.

  NOT a source:
    ✗ blueprint.json — does not exist for PYQ
    ✗ registry.json — does not exist for PYQ
    ✗ Official answer keys — ignored (D4, RE-1)

# ════════════════════════════════════════════════════════════════════════
# §2 — TRIGGER
# ════════════════════════════════════════════════════════════════════════

## S2-1 — Trigger format

```
PYQExplain
```

  Attach: the Row file (.docx, Step 1 output) OR provide a Google Drive link.

  Everything is derived from the attachment and project knowledge:

  1. **ExamCode**: derived from project knowledge files (any `[ExamCode]_*` file
     in `/mnt/project/` — e.g. `SSC_CGL_T1_section_rules.md`). If ambiguous →
     HARD STOP.

  2. **Date + Session**: parsed from the attached Row file's filename. The
     filename follows the pattern `[ExamCode]_[DD-Mon-YYYY][_session].docx`
     (e.g. `SSC_CGL_T1_12-Sep-2025_Shift_1.docx`). If the filename cannot be
     parsed → HARD STOP: "Cannot parse date/session from the attached filename."

  3. **Input document**: the attached Row file. If no matching file attached →
     HARD STOP: "Attach the PYQ Row file."

  Resume triggers (when resuming after a session break):
    PYQExplain resume
    PYQExplain --status

  Derived values (used for filenames and state):
    EXAM     = ExamCode (parsed from project knowledge)
    DATE     = DD-Mon-YYYY (parsed from attached filename)
    SESSION  = session keyword + number (parsed from attached filename, if present)
    DATE_SESSION = DATE[_SESSION] (e.g. 12-Sep-2025_Shift_1)

# ════════════════════════════════════════════════════════════════════════
# §3 — PREFLIGHT (P0 … P10)
# ════════════════════════════════════════════════════════════════════════

  P0  ENGINE PRESENT AND HONEST.
      explain_engine.py must be importable and its self-test must print
      "SELF-TEST: 62/62 PASS" (MANDATE A). If absent or stale → HARD STOP.

  P1  LOAD PROJECT KNOWLEDGE.
      Load from /mnt/project (project knowledge):
        • [ExamCode]_section_rules.md → parse CATEGORY C header for EngineConfig
        • [ExamCode]_subtopic_manifest.json → subtopic_id ↔ name mapping
        • [ExamCode]_exam_config.json → exam metadata
      If section_rules.md missing → HARD STOP:
        "section_rules.md not found. Run PYQExtract (Step 5) first."
      If subtopic_manifest.json missing → HARD STOP:
        "subtopic_manifest.json not found. Run PYQExtract (Step 5) first."
      If exam_config.json missing → WARN (use Row file scan for Q total).
      Load learnings files if present (RE-22, §24):
        • [ExamCode]_PYQ_EXPLAIN_AUDIT_LEARNINGS_v*.md
        • [ExamCode]_PYQ_EXPLAIN_LEARNINGS_v*.md
        • [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md (shared with mock pipeline)
        • [ExamCode]_EXPLAIN_LEARNINGS_v*.md (shared with mock pipeline)

  P2  BUILD EngineConfig AND PARSE ROW FILE.

      BUILD EngineConfig from CATEGORY C:
        q_re, opt_re, options_count, label_scheme, language, sentence_terminators
        → from section_rules CATEGORY C header.
        labels, markers, colors → from CATEGORY C (or engine defaults).
        banned_blocks, banned_templates, banned_fakecites, metacommentary_re
        → from CATEGORY C (or engine English defaults).

      DERIVE options_by_q FROM THE ROW FILE (replaces registry.json):
        Scan the Row file: for each question Q.n, count the option paragraphs
        that match opt_re. Build {q_num: option_count} map. 0 = NAT question.
        Pass to EngineConfig(options_by_q=...). This is the per-question AUTHORITY.

      parse_paper(row_file_path, cfg): checks questions ascending + contiguous
        from 1; every question carries its EXPECTED option count; Q_TOTAL derived.
        Any fail → HALT with the specific check.

  P3  BUILD THE SUBTOPIC CLASSIFICATION MAP.
      For each question Q.n, determine its (subject, topic, subtopic, subtopic_id).
      Sources (in priority order):
        a. Sorted PYQ file for the same date/session (if available on Drive) —
           the classification table PYQSort built maps every original Q number to
           its subtopic. Load this mapping.
        b. Taxonomy matching — classify each question against the subtopic_manifest
           + section_rules patterns by matching question content.
      Store the map as q_to_classification = {q: {subject, topic, subtopic,
      subtopic_id}} in pyq_explain_progress.json.
      This map is used by PYQ-3 (PYQFormat) for colored pills and PYQ-4
      (PYQDeliver) for portal tagging.

  P4  RESOLVE QUESTION TYPES (depends on P2 + P3).
      Using the options_by_q map (P2) AND the subtopic classification (P3):
        - options_by_q[q] == 0 → nat
        - section_rules answer_cardinality == 'multi' for this Q's subtopic → msq
          (requires the subtopic from P3 to look up answer_cardinality)
        - else → mcq

  P5  BUILD THE FROZEN BATCH PLAN (§4).
      Walk Q.1 through Q.N in order, accumulating questions into batches.
      No blueprint q_range[] needed — PYQ papers are a single continuous sequence.
      Linked groups detected structurally from the Row file (shared-stimulus
      questions: multiple questions referencing the same passage/DI/figure above).
      Write the batch plan to pyq_explain_progress.json.

  P6  CONFLICT CHECK: if section_rules and exam_config disagree on Q_TOTAL,
      option count, or question type → HALT (a drifted config corrupts every block).
      Also verify opt_re and label_scheme describe the SAME LABELS.

  P7  PRINT THE SESSION STATUS DASHBOARD (all data now available from P2-P6):
```
PYQExplain — Session Status
=====================================
Exam               : [ExamCode] ([exam_name])
Paper              : [date] [session]
Config             : q_re=[..] · opt_re=[..] · lang=[..] · terminators=[..]
Level / Medium     : [level] · [medium]  (from exam_config)
Question types     : [mcq C · msq M · nat T]  (from P4 resolution)
Answer key         : NONE by design — PYQ-1 derives all [Q_TOTAL]
Learnings loaded   : [k AL-rules · m EX-rules] OR [none — first paper]
Paper (Row file)   : [X bytes · Q_TOTAL questions · K images · T tables]
Subtopic map       : [Q_TOTAL] questions classified · source: [Sorted file / taxonomy]
Batch plan         : [K batches · ceiling 10 · linked groups atomic]
Mode               : [interactive — halt per batch] OR [autonomous]
Output             : [ExamCode]_[date]_[session]_PYQ_Explanation.docx
State              : /home/claude (chat-scoped)
Status             : [Ready — Batch 1] OR [Resume — Batch k] OR [Halted]
```

  P8  RESUME (only on `resume` / `continue`): reload pyq_explain_progress.json +
      pyq_answer_keys.json + the pickled blocks, rebuild the PYQ Explanation docx
      from the clean source + all blocks so far, run §18 self-audit on it, THEN
      proceed to the next batch (RE-19).

  P9  MALFUNCTION GUARD: if about to ask "per-batch or all-at-once?", STOP — the
      answer is fixed (per-batch, MANDATE B). If about to solve beyond the current
      batch, STOP. If about to declare a paper defect, go to §17 first.

  P10 PRINT the batch plan summary (batch → q-range → count) and announce Batch 1.
      EXECUTE the current batch (§4).

# ════════════════════════════════════════════════════════════════════════
# §4 — BATCH ARCHITECTURE (the continue contract; whole-paper incremental delivery)
# ════════════════════════════════════════════════════════════════════════
#   Same batch architecture as the mock pipeline. EXPLAIN_BATCH_SIZE (ceiling 10),
#   frozen batch plan, atomic linked-group handling, and four anti-overrun guards.

## S4-1 — EXPLAIN_BATCH_SIZE

  EXPLAIN_BATCH_SIZE = 10. CEILING, never a quota (RE-7). NEVER raised above 10.

## S4-2 — The frozen batch plan (built once at P4, the authority for the whole run)

  Walk Q.1 through Q.N in order, accumulating questions into the current batch
  until adding the next unit would exceed the ceiling, then start a new batch. A
  "unit" is a single standalone question OR a whole atomic linked group (S4-3). The
  plan is written to pyq_explain_progress.json and is the SOLE source for which
  questions a turn may touch. No blueprint q_range needed — PYQ papers have a
  single continuous Q.1-Q.N sequence, so the batch plan is simple sequential
  partitioning.

## S4-3 — Atomic linked groups

  A linked group (RC passage set / cloze / DI cluster / puzzle) — identified from
  the Row file's shared-stimulus structure (multiple questions following a common
  passage/table/figure) — is NEVER split across a batch boundary. Packing rule:
  if adding the next group would cross the ceiling, CLOSE the batch early. If a
  single group is ITSELF larger than the ceiling, it becomes its own batch and may
  exceed 10 (atomicity wins — MANDATE B).

## S4-4 — One batch = one response (the continue contract)

  Each batch response does EXACTLY this, in order, then ENDS:
    A. Read batch_plan[k] from pyq_explain_progress.json. Solve ONLY those
       questions (§7 derive + second-method verify; §13 view images; §6 class-
       adaptive write). No look-ahead.
    B. Build each ExplanationBlock and call .validate() immediately.
    C. CUMULATIVE WHOLE-PAPER BUILD: build_interleaved_docx(CLEAN_ROW_FILE,
       ALL_BLOCKS_1..k, out, cfg). ALL blocks from batch 1 through k.
    D. §18 SELF-AUDIT on the whole doc.
    E. Flush state to /home/claude: pyq_explain_progress.json (mark batch k done)
       + pyq_answer_keys.json (append this batch's CAs) + pickled blocks.
    F. present_files(the single PYQ Explanation docx) — the whole paper (MANDATE D).
    G. Print MANDATE-0-safe progress line + ASK for confirmation, then END.
       (AUTONOMOUS mode: proceed to batch k+1 without pause.)

## S4-5 — The four anti-overrun guards

  1. FROZEN PLAN (S4-2): the turn may only touch batch_plan[k].
  2. ENGINE STAGE GUARD: verify_structure asserts coverage == expected set.
  3. PRE-DELIVER COVERAGE ASSERTION (§18): exactly Q1..last(batch k).
  4. HARD TURN BOUNDARY (S4-4 G): response ends at confirmation request.

# ════════════════════════════════════════════════════════════════════════
# §5 — THE BLOCK MODEL (ExplanationBlock) + the per-question checklist
# ════════════════════════════════════════════════════════════════════════
#   Same block model as TestExplain §5. Fields, structural guards, and per-
#   question checklist are reproduced below (self-contained — no cross-file
#   dependency).

## S5-1 — Fields (shaped by the question type: mcq · msq · nat)

  | Field           | Type                 | Constraint                            |
  |-----------------|----------------------|---------------------------------------|
  | q               | int                  | the question number                   |
  | qtype           | 'mcq'/'msq'/'nat'   | auto-inferred or set explicitly       |
  | ca              | int / set / val      | MCQ: 1-based index. MSQ: set. NAT: portal grading value from derive_nat_grading() |
  | ca_range        | (lo,hi) / None       | NAT only, when grading_type=='range'  |
  | axiom           | list[str]            | ≥1 DENSE sentence                     |
  | deduction       | list[str]            | ≥2 steps. Last binds the answer       |
  | speed_hack      | list[str]/None       | present IFF genuinely faster           |
  | why_wrong       | dict{int:list}       | MCQ/MSQ: keys == non-selected options  |
  | common_pitfalls | dict{val:list}       | NAT only: ≥1 wrong-VALUE entry        |
  | anomaly         | str/None             | INTERNAL escalation flag               |

  Option index → displayed label is via cfg.option_label() (RE-10).

## S5-2 — Hard structural guards (engine, write-time — position-independent)

  Correct Answer line = INDEX/VALUE ONLY (no option text). DEDUCTION ≥2 steps;
  last binds the answer. WHY WRONG keys == exactly the non-selected options
  (MCQ/MSQ); NAT uses common_pitfalls (≥1) and MUST NOT carry why_wrong.
  OMML for every fraction. One sentence per paragraph. Zero banned content.
  A breach raises in ExplanationBlock.validate() / add_math_text.

## S5-3 — PER-QUESTION CHECKLIST (tick every item before constructing the block)

```text
  [ ] Full stem + ALL options read to the end; OMML merged with text
  [ ] Question TYPE resolved: mcq · msq · nat
  [ ] Negative phrasing scanned (NOT/EXCEPT/INCORRECT/FALSE)        → §10a
  [ ] Composite options scanned (Both/Only/All/None of the above)   → §10b
  [ ] Figural? → every image extracted, role-bound, and VIEWED       (§13)
  [ ] Answer derived from first principles AND a second method       (§7)
  [ ] Methods agree (else DERIVATION-CONFIDENCE)                     (§7)
  [ ] Factual content web-verified with a recorded source            (RE-18)
  [ ] Class identified (§6); the right section LEADS
  [ ] AXIOM states a TRUTH, not the task; no restatement
  [ ] DEDUCTION last step binds the answer
  [ ] SPEED HACK present IFF genuinely shorter route found           (§14)
  [ ] WHY WRONG covers exactly the non-selected options (§15)
  [ ] Applicable learnings routed (§24)
  [ ] block.validate() called immediately after construction
```

# ════════════════════════════════════════════════════════════════════════
# §6 — UNIVERSAL QUESTION CLASSES & CLASS-ADAPTIVE SOLVING
# ════════════════════════════════════════════════════════════════════════
#   Same classes as TestExplain §6. Detection from section_rules, same
#   lead-section shapes. Reproduced below (self-contained).

## S6-1 — The classes and what each makes the explanation LEAD with

  | Class            | Detection (section_rules)                  | Lead section / shape |
  |------------------|--------------------------------------------|----------------------|
  | C-COMPUTATIONAL  | numeric/quantitative answer                | DEDUCTION leads      |
  | C-FORMAL-LOGIC   | fixed formal procedure; fixed_set          | DEDUCTION = tight verdict chain |
  | C-FACTUAL        | factual-recall / encyclopedic              | AXIOM leads (the fact) |
  | C-VOCAB-ITEM     | word/term meaning; grammar                 | AXIOM defines the term |
  | C-LINKED         | RC / cloze / DI passage-dependent          | DEDUCTION = stimulus → answer |
  | C-FIGURAL        | image-based stem or options                | AXIOM = visual rule   |
  | C-MULTI-SELECT   | answer_cardinality == 'multi'              | DEDUCTION = per-option verdict |
  | C-NUMERICAL-INPUT| NAT — typed numerical answer               | DEDUCTION = computation chain |

  A question may carry more than one facet (e.g. C-FIGURAL + C-COMPUTATIONAL).

# ════════════════════════════════════════════════════════════════════════
# §7 — DERIVATION PROTOCOL (derive-twice, never guess)
# ════════════════════════════════════════════════════════════════════════
#   Same derive-twice contract as the mock pipeline. DERIVATION-CONFIDENCE for
#   disagreements. NAT portal grading value via derive_nat_grading().

## S7-1 — Derive-twice (RE-6)

  For every question: derive the answer from first principles (Method 1), then
  verify by a second INDEPENDENT method (Method 2). The two methods MUST be
  meaningfully different — not the same calculation twice with different variable
  names. If they agree → high confidence. If they disagree → derive a third
  method → 2-of-3 consensus + DERIVATION-CONFIDENCE flag. If no consensus →
  HALT and report (§17).

## S7-2 — Web-verify facts (RE-18)

  Every current-affairs / general-knowledge fact, every factual option, and every
  date/name/place claim is web-verified against an authoritative, current source
  and the source URL recorded. Never certified from memory alone.

## S7-3 — Uniqueness expectation (RE-12)

  PYQ papers are published by exam bodies and are expected to have exactly one
  defensible answer per question. If a question appears to have zero or multiple
  defensible answers, that is almost certainly an incomplete solve — go to §17.

## S7-4 — NAT portal grading value

  Same derive_nat_grading() function as TestExplain §S7-4 (pinned, byte-identical
  copy). After the derive-twice value is pinned, run it through derive_nat_grading()
  to get the portal-safe grading value. Set ExplanationBlock ca/ca_range from
  that output, never the raw derived number.

  ```python
  from decimal import Decimal, ROUND_HALF_UP
  import re

  _NAT_GRADE_CHARSET = frozenset('0123456789.-')
  _NAT_INTEGRAL_EPS = Decimal('1e-9')

  def _fmt_portal_number(value, precision=None):
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
      if re.fullmatch(r'-0(\.0+)?', s):
          s = s.lstrip('-')
      return s

  def _fmt_portal_range(lo, hi, precision=None):
      lo_s = _fmt_portal_number(lo, precision)
      hi_s = _fmt_portal_number(hi, precision)
      if lo_s.startswith('-') or hi_s.startswith('-'):
          raise ValueError(f'NOT SUPPORTED negative-bound range lo={lo_s} hi={hi_s}')
      if Decimal(lo_s) > Decimal(hi_s):
          raise ValueError(f'lo>hi {lo_s} {hi_s}')
      return f'{lo_s}-{hi_s}'

  def derive_nat_grading(value, ca_range=None, stem_precision=None):
      if stem_precision is not None:
          if ca_range is not None:
              lo, hi = ca_range
              return ('range', _fmt_portal_range(lo, hi, precision=stem_precision))
          return ('decimal_fixed', _fmt_portal_number(value, precision=stem_precision))
      if ca_range is not None:
          lo, hi = ca_range
          return ('range', _fmt_portal_range(lo, hi, precision=None))
      d = Decimal(str(value))
      if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
          v_int = int(d.to_integral_value())
          return (('positive_integer', str(v_int)) if v_int >= 0 else ('integer', str(v_int)))
      return ('decimal', _fmt_portal_number(value, precision=None))
  ```

  PINNED: byte-identical to Framework_MockTestCreate.md §S7-NEW-C and
  Framework_MockTestCreateAudit.md's A-NAT-GRADE copy.

# ════════════════════════════════════════════════════════════════════════
# §8 — SECTION QUALITY STANDARDS (highest-standard contract per section)
# ════════════════════════════════════════════════════════════════════════
#   Governing rule across ALL sections — the DENSITY FLOOR (not a length floor):
#   every line must add a NEW number, fact, or reason; NO sentence may restate
#   another. Brevity is allowed only when the line is dense; a line carrying none
#   of its required facts fails the content floor (PYQ-2 enforces the no-
#   restatement rule code cannot).

## S8-1 — Correct Answer
  Role: the one line the student trusts absolutely; the most dangerous line in the
  pipeline. Standard: INDEX/VALUE ONLY, in the paper's own label scheme, no option
  text — MCQ "Correct Answer: 3" (or "C" for a lettered paper); MSQ the full set
  "Correct Answer: 1, 3"; NAT the portal grading value from S7-4 — a plain value
  ("Correct Answer: 47") or, when the exam publishes a tolerance band, the lo-hi
  range with NO parentheses, words, or en-dash ("Correct Answer: 46.50-47.50").
  The retired "47 (accepted range 46.5–47.5)" wording is banned outright — it fails
  the delivery portal's grading charset on five separate counts (space, parens,
  letters, en-dash) and must never appear in a rendered document. Equals the
  independently derived answer; bound three ways (line = DEDUCTION binding =
  pyq_answer_keys.json). For a negative stem it is the option the stem asks to
  IDENTIFY, polarity-correct (§10a).
  Enforced: three-way binding at write time; truth by derive-twice + web-verify +
  PYQ-2.

## S8-2 — AXIOM
  Role: the transferable concept — the rule/formula/theorem/definition that makes
  this CLASS solvable; a student who reads only the AXIOM learns the principle.
  Standard: ≥1 dense sentence; sentence one states the core principle as a TRUTH
  ("the sum equals the average times the count"), never as a task ("we need to find
  the sum"); never restates the question. TEACH THE WHY, NOT JUST THE WHAT: where
  the rule has a reason, state the MECHANISM that makes it true, because the
  mechanism is what transfers to the next question — "a train clears a platform
  only when its rear passes the far edge, so the distance is train + platform"
  beats the bare "speed = total length ÷ time"; "6 = 2 × 3 with 2 and 3 coprime,
  so a multiple of 6 must pass both tests" beats "even with digit sum divisible
  by 3" (the coprime reason generalises to 12, 15, 35). A bare formula with no
  reason is the weakest acceptable AXIOM; prefer the one-sentence statement that
  also carries its why. Content is class-conditional — what it must state per
  subtopic is read from section_rules (RE-9). A forced second sentence is how
  restatement creeps in; one dense sentence is preferred when it fully states the
  rule AND its reason.
  Enforced: ≥1 sentence, one-per-paragraph, banned-phrase scan (engine); "truth
  not task", "why not just what", correctness by discipline + PYQ-2.

## S8-3 — DEDUCTION
  Role: the reproducible spine — AXIOM → answer with every intermediate value
  shown, so the student re-walks it and gets the same result. Standard: ≥2 steps,
  one sentence each, each showing its actual value ("235 ÷ 5 = 47", not
  "simplifying we get 47"); no "clearly", no skipped algebra; every fraction in
  OMML; the LAST step contains "Option N" (N = ca). Load-bearing tokens (decisive
  numbers, the final value) are bolded so a strong student reads only the bolded
  path (fast lane) and a weaker one reads the full line (full lane) — both served
  by one block.
  Enforced: ≥2 steps + last-binds-Option-N + OMML + one-per-paragraph + zero
  glyphs (engine); chain completeness + arithmetic truth by derive-twice + back-
  substitution + PYQ-2.

## S8-4 — SPEED HACK
  Role: exam-craft — a genuinely shorter route to the SAME answer, for time
  pressure; optional by design. Standard: a structurally DIFFERENT, faster path
  (not the same steps reworded); same CA; one or two dense lines; names the actual
  lever ("test divisibility by 3 first", "back-solve from the options", "only 39
  fits"). Vague encouragement ("do it mentally", "obvious with practice") is
  banned — that is a platitude, not a hack. Inclusion is decided per question by
  §14; if no honest shortcut exists the block is OMITTED, never padded.
  Enforced: if present, binds the same CA (engine); "genuinely faster, not
  cosmetic" by discipline + PYQ-2.

## S8-5 — WHY WRONG (mcq / msq) · COMMON PITFALLS (nat)
  Role: where most learning happens — the SPECIFIC error a student commits to land
  on a wrong choice, inoculating against that exact mistake. Standard (the anti-
  template contract, §15): keys = exactly the NON-selected options (for MSQ, every
  option not in the correct set); 1–2 DENSE lines each; the first line names an
  error type (§9) that ACTUALLY produces that option's value/content (back-derive
  the distractor — "if a student did X they get exactly this option"); the line
  also carries the corrected value ("13 × 3 = 39, not 36"). No two wrong options
  share an explanation. For negative stems the true options are "a TRUE statement,
  therefore NOT the answer" — never "incorrect" (§10a). For factual classes every
  reason is a web-confirmed fact.
  NAT analogue — COMMON PITFALLS: a NAT question has no options to reject, so this
  section lists the wrong VALUES a student most commonly computes, ≥1, each headed
  by the value and naming the slip that yields it ("forgetting to divide leaves
  235 — process_confusion"; "dividing by the wrong count gives 9.4 — value_swap").
  Same anti-template discipline: each pitfall must reproduce a real wrong value.
  Enforced: key set (mcq/msq) or ≥1 value-keyed pitfall (nat) + ≥1 sentence +
  error-type token + banned templates/glyphs (engine); reproduces-the-wrong-answer
  + factual truth by discipline + PYQ-2.

# NOTE: Figural questions no longer emit any FIGURE section; the rendered order
#   for EVERY question type is Correct Answer → ⬛ AXIOM → ⬛ DEDUCTION →
#   (⚡ SPEED HACK) → ❌ WHY WRONG? / ❌ COMMON PITFALLS. The figure itself stays
#   in the question region (byte-identical, §12); how a figural AXIOM / DEDUCTION /
#   WHY WRONG is written is governed by C-FIGURAL (§6-1) and the image-viewing
#   protocol (§13).

# ════════════════════════════════════════════════════════════════════════
# §9 — ERROR-TYPE TAXONOMY
# ════════════════════════════════════════════════════════════════════════
#   Exam-agnostic error types. The named type must ACTUALLY produce the option (§15).

  | Error type            | When it applies                                   |
  |-----------------------|---------------------------------------------------|
  | value_swap            | correct value for the wrong quantity               |
  | sign_error            | wrong arithmetic sign                             |
  | unit_error            | wrong units                                       |
  | off_by_one            | n instead of n±1                                  |
  | partial_truth         | correct for part, misses a condition              |
  | process_confusion     | right values, wrong process                       |
  | reversed_relationship | relationship inverted                             |
  | name_swap             | correct fact, wrong entity                        |
  | formula_error         | wrong formula applied                             |
  | rounding_trap         | correct calculation, wrong rounding               |
  | polarity_flip         | true↔false (negative stem)                        |

# ════════════════════════════════════════════════════════════════════════
# §10 — SPECIAL-CASE PROTOCOLS
# ════════════════════════════════════════════════════════════════════════
#   Protocols for negative stems, composite options, and MSQ/NAT questions.

## S10a — Negative stem
  Trigger: stem contains NOT / EXCEPT / INCORRECT / FALSE (configurable).
  DEDUCTION gives a truth-verdict for EVERY option, then isolates the target.
  WHY WRONG states each option is TRUE (hence NOT the answer) — polarity_flip.

## S10b — Composite options
  Trigger: "Both 1 and 2", "All of the above", "None of the above" (configurable).
  Establish truth of EVERY underlying statement, THEN map to the option.

## S10c — MSQ and NAT protocols
  MSQ: DEDUCTION = truth-verdict per option; last step binds the full set.
  NAT: derive the VALUE, run through derive_nat_grading() (S7-4), set
  ca/ca_range, write COMMON PITFALLS in place of WHY WRONG.

# ════════════════════════════════════════════════════════════════════════
# §11 — MATH / OMML RENDERING DISCIPLINE
# ════════════════════════════════════════════════════════════════════════
#   Every piece of math in an explanation is real OMML — never inline text, glyph,
#   or LaTeX. Same OMML standard across the whole document.

## S11-1 — The single funnel (write-time enforced)
  All prose enters via add_math_text(). Auto-converts digit/digit fractions to
  OMML. Raises on: unconvertible inline fraction, year-range slash, vulgar glyph,
  LaTeX. Units km/h, m/s are left as text.

## S11-2 — Post-write verification (every batch)
  verify_explanations() re-parses the RENDERED docx and re-confirms every OMML
  fraction is well-formed and no inline fraction slipped the funnel.

## S11-3 — The Word-native limit
  OMML renders perfectly in Word. LibreOffice may mangle it — that is a rendering-
  environment artefact, never a document defect. FINAL VISUAL REVIEW IN WORD.

# ════════════════════════════════════════════════════════════════════════
# §12 — CONTENT-FIDELITY PRESERVATION (append-only; byte-identity)
# ════════════════════════════════════════════════════════════════════════
#   Same as TestExplain §12 except the source is the Row file (not the mock
#   pipeline's Create_Complete paper).

## S12-1 — What is guaranteed byte-identical to the Row file source
  • Stem + option TEXT (paragraph lines), and underline/bold runs.
  • OMML: the <m:t> math-text sequence + node count per question.
  • Images/figures/charts: every drawing's rId resolves; per-paragraph drawing
    counts identical; every media part MD5-identical.
  • Tables/matrices/DI grids: table count + row/column counts + cell-text grid.

## S12-2 — How
  build_interleaved_docx seeds the CLEAN Row file WHOLE and inserts explanation
  paragraphs only AFTER a question's last option. verify_fidelity compares the
  output's every question region to the immutable source after every batch.

## S12-3 — Two independent confirmations (beyond the fidelity diff)
  • STRIP-AND-RE-AUDIT: strip_solutions() produces a questions-only copy; it
    must match the Row file source identically (never run the auditor on the
    combined doc — it scans explanation prose as paper content and false-alarms).
  • COUNT INVARIANTS: output question count, options/question, image count,
    table count and OMML count == the Row file input exactly.

# ════════════════════════════════════════════════════════════════════════
# §13 — FIGURAL DEEP-ANALYSIS PROTOCOL (view every image — no exception)
# ════════════════════════════════════════════════════════════════════════
#   No ExplanationBlock for a figural question may be built until every image in
#   that question has been extracted, role-bound, and VIEWED. For PYQ, there are
#   no figural_manifests from a registry — detect figural questions structurally
#   from the Row file only (any question with <w:drawing> in stem or options).

## S13-1 — Detect figural questions structurally
  A question is figural if its region contains a <w:drawing> in the STEM or in
  any OPTION. Two shapes: IMAGE-IN-STEM and IMAGE-AS-OPTIONS.

## S13-2 — Extract, role-bind, view
  Extract image bytes, render them, bind each to its role, VIEW each before
  deriving. The binding matters: an unbound view can key the wrong index.

## S13-3 — Derive from the images
  VIEW → derive → proceed. No manifest cross-check for PYQ (no registry).

## S13-4 — Write what is visible
  AXIOM = the visual rule. DEDUCTION traces the VISIBLE transformation.
  WHY WRONG names, per wrong option-figure, the specific visual difference.

# ════════════════════════════════════════════════════════════════════════
# §14 — SPEED HACK INCLUSION GATE (derivation-driven; omit, never fake)
# ════════════════════════════════════════════════════════════════════════
#   SPEED HACK earns its place ONLY when a path reaches the answer with materially
#   less work than the DEDUCTION — fewer/cheaper operations, not the same operations
#   in fewer words. If the fastest honest route IS the DEDUCTION, there is no SPEED
#   HACK; OMIT.

## S14-1 — The two-part test (BOTH must pass, else omit)
  1. DISTINCT METHOD: the shortcut uses a different operation than the DEDUCTION —
     elimination by the most-discriminating feature, a divisibility/parity/unit-digit
     check, back-solving from options, a ratio/approximation, a known pattern. Same
     steps as the DEDUCTION → fails part 1.
  2. GENUINELY FASTER: it removes at least one full computation, or reaches the
     answer by checking one feature instead of resolving all, or lets the student
     stop before the formal solve completes.

## S14-2 — The operational proxy (applied per question at solve time)
  "Could a trained student pick the correct option WITHOUT performing the full
  DEDUCTION — by exploiting structure, the options, or a property?" YES → write it
  (must land on the same CA). NO → omit. The second derivation (§7) is the natural
  candidate.

## S14-3 — Where shortcuts live vs do not
  C-COMPUTATIONAL / C-FORMAL-LOGIC frequently admit real shortcuts (divisibility,
  unit-digit, alligation, ratio-jump, back-solve, parity, discriminating-feature).
  C-FACTUAL has none (you know a fact or you do not) → omit as a rule. C-LINKED
  (RC): the fast move is pointing to the licensing line, already in the DEDUCTION →
  omit. C-VOCAB is usually recall → omit unless elimination trick exists.
  NAT (C-NUMERICAL-INPUT) is usually C-COMPUTATIONAL → actively look for a cleaner
  route (a different scaling, a unit shortcut, a property), since NAT solves are
  often the most shortcut-rich. MSQ (C-MULTI-SELECT): the classic shortcut is
  eliminate-by-the-most-discriminating-property.

## S14-4 — The honesty guard
  If you cannot state the SPECIFIC lever that saves SPECIFIC work, there is no
  SPEED HACK — omit it. An empty or generic SPEED HACK is a PYQ-2 defect, treated
  like a wrong answer.

# ════════════════════════════════════════════════════════════════════════
# §15 — WHY WRONG / COMMON PITFALLS ANTI-TEMPLATE STANDARD (the diagnosis contract)
# ════════════════════════════════════════════════════════════════════════
#   Templating happens because, when the writer does not truly know why a
#   distractor is wrong, a generic line ("this option is incorrect") is sayable
#   for ANY of them. The fix is a CONTENT requirement no template can satisfy.

## S15-1 — The rule that kills templating
  Every WHY WRONG / COMMON PITFALLS line must contain the specific WRONG PATH that
  produces THAT option's value — what mistake a student makes and what wrong
  number/fact it yields, traced to this exact option or value. Different wrong
  answers cannot come from one mistake, so if two of them share an explanation,
  the rule is violated by definition.

## S15-2 — Four hard requirements per wrong option / value
  1. NAME the error type (§9) in the first line — a diagnosis, not a dismissal.
  2. The named error must ACTUALLY produce that option/value (the reproduce check):
     back-derive the distractor — "if a student did X they get exactly this
     option/value." If no such mistake can be found, the question is not yet
     understood → go solve it; a generic line is forbidden.
  3. CARRY the corrected value — what the right step gives instead ("13 × 3 = 39,
     not 36"; for NAT, "…, not 90"). The explicit contrast is mandatory.
  4. NO two wrong options/values share wording; NO banned template sentences.

## S15-3 — Class- and type-specific shape
  Computational → the arithmetic slip + the wrong number. Factual → what the option
  ACTUALLY is (the corrected fact). Negative stem → "TRUE, therefore not the answer"
  (never "incorrect"). Composite → the exact component that breaks it. Vocab → the
  precise nuance missed. RC → the passage line that REFUTES the option.
  MSQ → lead with the SEDUCTIVE HALF (the cheap test the distractor passes, which
  makes a hasty solver select it), then the test it fails.
  NAT (COMMON PITFALLS) → head each entry with the wrong VALUE, name the slip that
  yields exactly it, and carry the contrast to the correct value.
  Density without thinness: 1–2 lines, each carrying a required fact.

# ════════════════════════════════════════════════════════════════════════
# §16 — QUALITY-CONSISTENCY (ANTI-DECAY) ARCHITECTURE
# ════════════════════════════════════════════════════════════════════════
#   Quality decay over a long run is a PREDICTABLE property, not a moral failing,
#   so the defence is structural, not "try harder". Four named causes, each blocked.

## S16-1 — The causes
  (1) context dilution (by Q60 the window crowds out the current question);
  (2) pattern-matching auto-fill (remembered shape instead of solving THIS question
  — the source of templated WHY WRONG); (3) floor-gaming (writing to the minimum
  that passes); (4) no fresh checkpoint (the bar quietly lowers).

## S16-2 — The defences (none weakens as the paper lengthens)
  • BATCHING IS THE LEVER (cause 1): ≤ ceiling per batch with a HALT for
    confirmation means the context never fills with 60 prior solves; each batch
    starts fresh with the full standard re-loaded. This is why all-at-once is a
    MANDATE-level breach (MANDATE B). Autonomous mode waives the HALT but NOT the
    per-batch fresh-context processing (RE-0).
  • STANDARD RE-ASSERTED EACH BATCH (cause 4): the §5-3 checklist + §8 floors are
    actively re-applied each turn, not remembered from batch 1.
  • CONTENT FLOORS, NOT LENGTH FLOORS (cause 3): §8 / §15 demand option-specific
    facts a template cannot supply — laziness FAILS the check instead of passing.
  • PER-BATCH WHOLE-DOC SELF-AUDIT (§18): a thin or malformed block cannot hide
    mid-paper; every batch ships the full cumulative doc.
  • UNIFORM MECHANICAL GUARANTEES: every engine guard fires identically on Q1 and
    Q97 — a write-time ValueError does not get lenient because the run is long.
  • DERIVE-TWICE HAS NO EXCEPTIONS (§7): no "confident by now, skip" path.
  • PYQ-2 IS THE INDEPENDENT NET: it re-reads EVERY explanation, zero sampling,
    not trusting PYQ-1; it certifies with a runnable completion gate (CA1–CA7).
  The guarantee: "a weaker line CANNOT REACH THE STUDENT", caught at four
  independent layers that do not weaken with length.

# ════════════════════════════════════════════════════════════════════════
# §17 — PYQ DEFECT HANDLING (exam body paper; note, never fix)
# ════════════════════════════════════════════════════════════════════════
#   DIFFERS FROM TestExplain §17. PYQ papers are published by exam bodies —
#   they are NOT generated mock papers. A defect in a PYQ is a KNOWN EXAM
#   BODY ERROR, not a Step-8 certification failure.

## S17-1 — The burden of proof is STILL inverted (RE-12)
  "This question/option is wrong" is a conclusion of LAST RESORT. Before a
  defect may be suspected: solve from first principles AND a second method,
  full stem + all options re-read, OMML merged with text, figural images VIEWED.

## S17-2 — "Wrong" must be specific and reproducible
  A defect claim must state PRECISELY what is defective with a concrete derivation.

## S17-3 — PYQ-1 does NOT fix (RE-16, adapted for PYQ)
  PYQ-1 NEVER edits question content (RE-3). Three outcomes:
  • COMMON: what looked wrong was an incomplete solve → solve it and write the
    explanation. No defect.
  • RARE: there is provably no single defensible answer (two options both valid,
    or the stated answer is demonstrably wrong). PYQ-1 picks the MOST DEFENSIBLE
    answer (or the answer an exam-body key would select), writes a normal
    ExplanationBlock for that answer, and sets a DERIVATION-CONFIDENCE flag with
    a PYQ-AMBIGUITY note recording the reproduced evidence. The question is
    explained, not skipped — the student still gets a full explanation.
    IMPORTANT: PYQ-1 does NOT set the anomaly flag here (the engine forbids
    anomaly + content on the same block). Instead, the DERIVATION-CONFIDENCE +
    PYQ-AMBIGUITY note in pyq_answer_keys.json signals PYQ-2 to review.
    Unlike TestExplain (which halts and escalates to Step 8), PYQ-1 CONTINUES
    because there is no upstream step to fix the paper — it IS the actual exam.
    The ambiguity is noted in the END-OF-PAPER REPORT (§20) for PYQ-2 review.
  • VERY RARE: the question is genuinely unanswerable (corrupt image, missing
    data, truncated stem from scan defect) → set the anomaly flag (no content),
    skip explanation for this question, note in report. PYQ-2 will review.
    The anomaly flag is reserved for THIS case only — a question so broken that
    no answer can be defended at all.

## S17-4 — Why this is different from mock pipeline defect handling
  Mock papers were GENERATED by the pipeline — a defect is a pipeline bug that
  can be fixed by re-running Step 7/8. PYQ papers were published by an exam body —
  a defect is a FACT about the exam, not a fixable bug. The correct response is
  to note the defect and explain the most defensible answer, not to halt the
  pipeline waiting for a fix that cannot happen.

# ════════════════════════════════════════════════════════════════════════
# §18 — PER-BATCH SELF-AUDIT (producer self-certification)
# ════════════════════════════════════════════════════════════════════════
#   Same checklist as TestExplain §18, adapted for Row file source.

## S18-1 — The checklist (all must hold before present_files — MANDATE D)
```text
  [ ] every block this run: ExplanationBlock.validate() clean (engine)
  [ ] verify_fidelity(out, Row_file_source): whole question region byte-identical
      to the Row file, every image rId resolves (§12)
  [ ] verify_structure(out, blocks, expected = Q1..last(batch k)): coverage exact,
      NO look-ahead (§4 / §5)
  [ ] verify_explanations(out, blocks): INDEPENDENT post-render re-audit (§11)
  [ ] count invariants: image / table / OMML / question / option counts == Row file
  [ ] strip-and-re-audit: questions-only copy passes (§12-3)
  [ ] every CA fact web-verified with a recorded source (§7 / RE-18)
  [ ] derived answers flushed to pyq_answer_keys.json; CA three-way binding holds
  [ ] coverage assertion (S4-5 guard 3): exactly Q1..last(batch k)
  [ ] learnings coverage (§24): every applicable rule routed
```
  Any item open → fix, re-build, re-audit. present_files FORBIDDEN until ALL hold.

## S18-2 — The independent gate is PYQ-2's completion gate (the loop's other half)
  PYQ-1's §18 is PRODUCER self-certification. The INDEPENDENT certification is
  PYQ-2 (PYQExplainAudit), which runs the same explain_audit_gate.py completion
  gate (CA1-CA7). PYQ-1's per-question handoff data (derived answers, web-verified
  facts, viewed-image confirmations, DERIVATION-CONFIDENCE flags) populates that
  ledger — one shared evidence contract.

# ════════════════════════════════════════════════════════════════════════
# §19 — DELIVERY (incremental whole-paper; one present_files per batch)
# ════════════════════════════════════════════════════════════════════════

## S19-1 — Pre-delivery checklist (MANDATORY before present_files)
```python
import os
out = '/mnt/user-data/outputs'
sol = f'{EXAM}_{DATE_SESSION}_PYQ_Explanation.docx'
present = set(os.listdir(out))
BANNED = ('answer', 'key', 'ledger', 'progress', 'state', 'pickle', 'stripped', 'source')
leaked = [f for f in present if any(b in f.lower() for b in BANNED)]
checks = [
    ('1 PYQ explanation docx in outputs',  os.path.exists(f'{out}/{sol}')),
    ('2 self-audit (S18) all clean',       bool(globals().get('SELF_AUDIT_CLEAN'))),
    ('3 whole-paper coverage asserted',    bool(globals().get('COVERAGE_OK'))),
    ('4 no internal sidecar leaked',       not leaked),
    ('5 outputs == exactly the PYQ docx',  present == {sol}),
]
fails = [n for n, ok in checks if not ok]
if fails:
    raise SystemExit('HARD STOP (S19-1): ' + '; '.join(fails))
```

## S19-2 — The single present_files call (per batch)
```python
present_files([f'/mnt/user-data/outputs/{EXAM}_{DATE_SESSION}_PYQ_Explanation.docx'])
```

## S19-3 — Progress line + confirmation request
  Print: "Batch k of K — Q[a]..Q[b] explained; Q1..Q[b] now carry solutions,
  Q[b+1]..Q[end] unchanged. SPEED HACK on m; DERIVATION-CONFIDENCE on j."
  Then: "Reply 'continue' for Batch k+1." END THE RESPONSE.
  (Autonomous mode: proceed without the confirmation request.)

## S19-4 — Post-delivery footer (MANDATORY after every present_files call)
  Follow Framework_DeliveryFooter.md for footer type:
    - F1 (amber) after each non-final batch
    - F2 (green) after the final batch

# ════════════════════════════════════════════════════════════════════════
# §20 — END-OF-PAPER REPORT (after the FINAL batch; MANDATE-0 safe)
# ════════════════════════════════════════════════════════════════════════
  §R1 PROVENANCE: paper [date] [session] · spec v1.0 · engine 62/62 · timestamp ·
      EngineConfig (option count(s), label scheme, language, terminators).
  §R2 VERDICT: SHIP (delivered) / HALTED.
  §R3 COVERAGE: Q_TOTAL/Q_TOTAL explained · question-type split (mcq/msq/nat) ·
      SPEED HACK count · OMML count · per-class distribution.
  §R4 SELF-AUDIT (§18): verify_fidelity / verify_structure / math-render /
      count invariants / strip-re-audit / coverage — all clean.
  §R5 DERIVATION-CONFIDENCE: every Q where methods initially disagreed.
  §R6 FACT SOURCES: every web-verified fact with source URL.
  §R7 ANOMALIES (§17): every Q where no defensible answer was found, with
      the reproduced evidence. For PYQ, these are exam body errors, not pipeline
      bugs — noted, not escalated.
  §R8 PYQ-2 HANDOFF (RE-20): what was derived, what was web-verified, what is
      model-derived, where to look hardest. State: review IN MICROSOFT WORD.
  §R9 SUBTOPIC CLASSIFICATION MAP: summary of q_to_classification (Q→subtopic
      mapping) for PYQ-3 (PYQFormat pills) and PYQ-4 (PYQDeliver tags).
  §R10 LIMITATIONS (§22).

# ════════════════════════════════════════════════════════════════════════
# §21 — DEFINITION OF DONE / HARD INVARIANTS
# ════════════════════════════════════════════════════════════════════════
  1.  Pre-flight P0-P10 passed; engine 62/62; config built from section_rules.
  2.  Every question explained (zero sampling); every validate() clean.
  3.  Every answer derived two ways; disagreements resolved 2-of-3 +
      DERIVATION-CONFIDENCE. Zero guesses. Typed correctly (mcq/msq/nat).
  4.  Every figural question's images extracted, role-bound, VIEWED.
  5.  Every CA/factual option web-verified with a recorded source.
  6.  WHY WRONG keys == exactly non-selected; error type REPRODUCES option.
      NAT: ≥1 pitfall. No template/glyph/fake-cite.
  7.  SPEED HACK present IFF genuinely faster; never padded.
  8.  Every fraction OMML; well-formed; no year-range artefact.
  9.  FIDELITY: whole question region byte-identical to Row file source.
  10. Self-audit (§18) clean every batch; coverage assertion holds.
  11. Subtopic classification map complete for PYQ-3/PYQ-4 consumption.

# ════════════════════════════════════════════════════════════════════════
# §22 — LIMITATIONS & SCOPE
# ════════════════════════════════════════════════════════════════════════
  • Descriptive/essay questions are out of scope — flag and skip.
  • Language comprehension questions in non-English scripts may require
    language-specific EngineConfig customisation (sentence terminators, banned
    patterns).
  • A vision-transcribed Row file (__vision-unverified suffix) may have
    transcription errors — explanations proceed but flag low-confidence Qs.
  • OMML renders correctly only in Microsoft Word.

# ════════════════════════════════════════════════════════════════════════
# §23 — SUBTOPIC ID RESOLUTION
# ════════════════════════════════════════════════════════════════════════
#   When PYQ-1 maps each question to its subtopic (P3), it resolves the subtopic_id
#   by matching rendered content to section_rules patterns keyed by id, NEVER by
#   display-name string-match. PYQ-1 NEVER mints a new id, NEVER joins on a display
#   name, and NEVER edits the manifest. The id recipe carries zero exam-specific
#   values. subtopic_manifest.json is the single source for id ↔ name mapping.

# ════════════════════════════════════════════════════════════════════════
# §24 — LEARNINGS CONSUMPTION CONTRACT (the PYQ-2 → PYQ-1 feedback loop)
# ════════════════════════════════════════════════════════════════════════
#   PYQ-2 (PYQExplainAudit) is the independent auditor. Every paper it audits, it
#   distils the defects it fixed into reusable rules so the SAME mistake is not
#   authored again. This section is the consumer half; PYQ-2 §24 is the producer.
#
#   FOUR learnings files, all loaded at P1, all OVERRIDE this spec on content:
#     • [ExamCode]_PYQ_EXPLAIN_AUDIT_LEARNINGS_v*.md — PYQ-specific AL-rules,
#       auto-generated by PYQ-2. The PYQ feedback loop proper.
#     • [ExamCode]_PYQ_EXPLAIN_LEARNINGS_v*.md — PYQ-specific human guardrails.
#     • [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md — mock pipeline AL-rules (shared
#       exam, shared subtopics, shared defect patterns — reusable).
#     • [ExamCode]_EXPLAIN_LEARNINGS_v*.md — mock pipeline human guardrails.
#   None exist on the first PYQ paper by design. Absence is normal, never a HALT.
#
## S24-1 — What a rule carries (the pinned schema)
  Each rule: defect_code (routing key), first seen, occurrences, pattern,
  prevention rule (the obeyable part), verification (the self-check).
  parse_learnings(path) returns {rules, by_defect} indexed by defect_code.
#
## S24-2 — How a rule is applied (per question, at solve time)
  1. Resolve the question's CLASS(es) (§6). Each class has a known defect set.
  2. Applicable rules = loaded AL/EX rules whose defect_code is in that set.
  3. Obey each Prevention rule while authoring; run each Verification before
     validate(). The §18 self-audit asserts all applicable rules were routed.
#
## S24-3 — Precedence & accumulation
  A loaded learnings rule OVERRIDES this base spec on any CONTENT conflict. It may
  NEVER override coverage/§18/the batch law (RE-0). Rules ACCUMULATE across papers
  (never deleted, superseded only by explicit annotation).

# ════════════════════════════════════════════════════════════════════════
# APPENDIX A — UNIVERSAL explain_engine.py (MANDATE A) — SINGLE SOURCE
# ════════════════════════════════════════════════════════════════════════
#   The engine listing is NOT embedded here. The canonical, runnable home:
#       explain_engine.py   (delivered alongside this spec)
#   It is COMPLETE, working, universal, and byte-identical across all exams
#   and across both the mock and PYQ pipelines. Self-tests:
#     --self-test       → "SELF-TEST: 62/62 PASS" (core, required at P0)
#     --self-test-audit → "AUDIT-SELF-TEST: 10/10 PASS" (reader round-trip)
#   The companion gate (explain_audit_gate.py) is used by PYQ-2, not PYQ-1.

# ════════════════════════════════════════════════════════════════════════
# SHARED_RULES_VERSION: 1.0 (2026-07-22)
# Shared with: Framework_MockTestExplain.md
# Counterpart file: Framework_MockTestExplain.md (mock/test pipeline)
# If any RE-* rule, MANDATE, or §4-§18 section changes in EITHER file,
# update BOTH files and bump this version.
# validate_framework_md.py checks version parity between
# Framework_PYQExplain.md and Framework_MockTestExplain.md.
# ════════════════════════════════════════════════════════════════════════

# FOOTER — this file is the canonical PYQ-1 spec. On any CONTENT conflict with a
# loaded learnings file, that learnings file WINS (§24). A learnings rule NEVER
# overrides coverage/§18/the batch law (RE-0). Deliver the full merged spec on
# every edit — never a patch.
# END OF Framework_PYQExplain v1.0
# ════════════════════════════════════════════════════════════════════════
