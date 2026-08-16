# Framework_PYQExplain v2.6 — Universal PYQ Explanation Generator
# v2.6 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: a name is added to this file's executable surface. NO ARTEFACT CHANGES.
#   This spec CALLED present_files() from compiling python while DEFINING it nowhere —
#   a guaranteed NameError the moment that path executes as python. Five such call
#   sites stood across four specs; spec_name_audit_baseline.json had accepted
#   `present_files` as a known-unbound name in all four, which is why the ratchet
#   reported OK for weeks. SAME SHAPE as D2 of
#   GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, which fixed the instance and left the
#   class standing. FIX: a CLASS: T stub is declared in this file, matching the
#   corpus's per-file house pattern for CLASS T markers.
# v2.5 — 2026-08-13 — GAP-2026-08-13-STALE-SELFTEST-PIN: the MANDATE-A engine gate pinned
#   the literal "SELF-TEST: 62/62 PASS" while explain_engine.py prints 64/64 — a HALT on
#   every session with a healthy engine. Converted to the FLOOR form (N/N PASS, N >= 62),
#   the AUTH_GATE_FLOOR pattern; same for the --self-test-audit reader pin (>= 10).
# [ExamCode] project | PYQ-1 (PYQExplain) | Exam-agnostic
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
#     PYQ-3  PYQFormat       → [ExamCode]_[date]_[session]_PYQ_Formatted.docx  (student)
#     PYQ-4  PYQDeliver      → [ExamCode]_[date]_[session]_PYQ_Final.docx       (portal)
#     (PYQ-2 PYQExplainAudit was RETIRED in v2.1. PYQ-3 and PYQ-4 are INDEPENDENT —
#     both take PYQ-1's _PYQ_Explanation.docx directly, neither depends on the other.)
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
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_PYQExplain.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

# ════════════════════════════════════════════════════════════════════════
# EXECUTION MODEL
# ════════════════════════════════════════════════════════════════════════
#   Per batch: 3–5 tool calls. No user "Continue" needed within a batch.
#     1. create_file  → write the batch's explanation pipeline script
#     2. bash_tool    → run it (solve → build blocks → interleave → verify)
#     3. bash_tool    → run §18 self-audit checks (verify_fidelity, verify_structure,
#                       verify_explanations, count invariants, strip-and-re-audit)
#     4. present_files → deliver the whole-paper PYQ Explanation docx
#   Before Batch 1 only: the §13A figural pre-transcription pass (P2a) adds one
  Phase A call, one in-turn view per figure artefact, and one Phase C call.
  The Row file is copied to /home/claude at the start (immutable read-only source).
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
  4. [ExamCode]_exam_config.json — exam metadata (total_questions, sections,
     difficulty_labels [default Easy/Medium/Hard], etc.). `exam_config.marking_scheme`
     (OPTIONAL field) — list of `{q_range, question_type, correct_marks, ...}` —
     is READ at P4 for POSITION-BASED Question Type resolution (its `question_type`
     per q_range) when it carries more than one distinct question_type; absent,
     empty, or single-type → P4 falls back to the structural rule.
  5. explain_engine.py — the universal explanation engine; SAME file as TestExplain
     (MANDATORY — MANDATE A)

  NOT REQUIRED (PYQ has no mock pipeline outputs):
    ✗ blueprint.json — does not exist for PYQ papers
    ✗ registry.json — does not exist for PYQ papers
    ✗ Create_Complete.docx — PYQ uses the Row file directly

## S0-2 — OUTPUTS (what PYQ-1 delivers)

  CORE DELIVERABLES (via present_files — the WHOLE paper):
    1. /mnt/user-data/outputs/[ExamCode]_[date]_[session]_PYQ_Explanation.docx
       — delivered EVERY batch. The complete paper: every question solved so far
       carries its interleaved explanation; every not-yet-solved question is
       byte-identical to the Row file input. The same file grows explanation-
       coverage each batch until 100%.
    2. /mnt/user-data/outputs/[ExamCode]_[date]_[session]_pyq_explain_progress.json
       (v2.3 — PIPELINE HANDOFF) — delivered on the FINAL batch only (100% coverage),
       when all four of its maps are complete. It is delivered under the SAME
       [ExamCode]_[date]_[session] stem as the docx so two papers' sidecars never collide
       by filename, and PYQ-3/PYQ-4 can prove it belongs to the attached paper. It carries q_to_classification, options_by_q, qtype, and
       q_to_difficulty. Since PYQExplainAudit (PYQ-2) retired (v2.1), this JSON is the
       SOLE metadata source for PYQ-3 (PYQFormat pills) and PYQ-4 (PYQDeliver tags),
       and those steps normally run in a FRESH chat where /home/claude is gone. It is
       therefore promoted from internal state to a first-class deliverable the user
       carries forward and attaches to PYQ-3/PYQ-4. It contains NO answer keys or
       correct-answer data — only classification, option counts, and difficulty — so it
       is MANDATE-0-safe to hand over.

  IN-CHAT (every batch): a STATUS DASHBOARD + a per-batch progress line, then
  an explicit CONFIRMATION REQUEST that ENDS the turn (MANDATE B). At the final
  batch: the END-OF-PAPER REPORT + the human-review handoff.

  NEVER delivered: the Row file is NOT overwritten; no TRUE internal state file
  (answer_keys.json, pickled blocks, strip copy, figural queues) leaks to outputs.
  The ONLY state file promoted to a deliverable is the identity-prefixed
  [ExamCode]_[date]_[session]_pyq_explain_progress.json (final batch), because PYQ-3/PYQ-4
  require it as a cross-chat handoff.

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
#   Self-tests: `python3 explain_engine.py --self-test` → "SELF-TEST: N/N PASS", N >= 62 (v2.5 floor form; currently 64/64)

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
# THE CORE PRINCIPLE — engine proves shape; discipline proves truth
# ════════════════════════════════════════════════════════════════════════
#   The ENGINE enforces mechanically: block presence + order, the CA three-way
#   binding, WHY-WRONG key set, OMML for every fraction, banned glyphs/templates/
#   fake-cites/metacommentary, one-sentence-per-paragraph, and byte-identical
#   fidelity to the Row file source. A breach raises BEFORE the docx is written.
#   DISCIPLINE (derive-twice, web-verify, view-every-image, §5 checklist) enforces what
#   code cannot: answer correctness, conceptual soundness, web-true facts.
#   NOTE (v2.1): PYQExplainAudit (PYQ-2) has been RETIRED — no independent re-audit runs
#   downstream. This §18 self-audit is the final certification (§18-2); the risk it must
#   now guard against is PRODUCER SELF-DECEPTION, which the read-back-the-written-document
#   checks (not self-report) exist to catch. Run them literally.

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
  RE-20 : KINDNESS TO THE READER OF RECORD. The handoff states plainly what was
          derived, what was web-verified, what carries a DERIVATION-CONFIDENCE flag, and
          what is model-derived — so a HUMAN reviewer knows where to look hardest. With
          no audit step downstream (v2.1) this handoff is the ONLY surviving record of
          where the run was least certain: MANDATORY, never abbreviated, never skipped.
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
      "SELF-TEST: N/N PASS" with N == total AND N >= 62 (MANDATE A; v2.5 —
      GAP-2026-08-13-STALE-SELFTEST-PIN: floor form, the exact 62/62 pin HALTed
      every session once the engine grew to 64). If absent or stale → HARD STOP.

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

  P2a FIGURAL PRE-TRANSCRIPTION PASS (v1.2, §13A). Runs HERE — the earliest
      point at which the Row file is parsed and the figural set is known, and
      before any project-knowledge load, batch plan, or solve. Execute §13A in
      full: extract + role-bind every figure (Phase A), VIEW each one in-turn
      and record what is visible (Phase B), verify and persist (Phase C).
      Produces pyq_figural_vision.json. NEVER HALTS: a shortfall marks the
      affected questions VOID_ITEM and sets the run AMBER (§13A-5).
      A paper with zero figural questions skips P2a and records that fact.

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

      pyq_explain_progress.json ALSO carries `q_to_difficulty` (v1.1) — the
      per-question {q: label} map produced by §7A. Written incrementally as each
      batch completes, alongside q_to_classification, under the same int-key
      convention. PYQ-4 reads it as Tier 1 of its §2-3 resolver. (v2.1: PYQ-2's
      independent validation of this map is retired — it is now producer-only.)
      See §7A for the contract.

  P4  RESOLVE QUESTION TYPES (depends on P2 + P3).
      TIER 1 — POSITION-BASED (v2.3). When exam_config.marking_scheme (§0 item 5)
      carries MORE THAN ONE distinct question_type value, Question Type is a
      property of the Q-NUMBER, not the subtopic: resolve q against
      marking_scheme[].q_range and take that entry's question_type
      (lower-cased mcq/msq/nat); answer_cardinality is IGNORED for this q.
        distinct = { e.question_type for e in marking_scheme }
        if len(distinct) > 1 and some range contains q → e.question_type.lower()
      This mirrors MockDeliver v1.7 / PYQDeliver S2-2a and is the "set explicitly"
      mechanism named in §5-1: it is what makes qtype AUTHORITATIVE for
      section-determined-MSQ exams (IIT JAM, GATE, …) — where a whole section is
      MSQ but each of its subtopics reads answer_cardinality 'single' across the
      corpus — rather than a copy of that subtopic statistic.
      TIER 2 — STRUCTURAL (fallback; single-type / subtopic-based exams). Using
      the options_by_q map (P2) AND the subtopic classification (P3):
        - options_by_q[q] == 0 → nat
        - section_rules answer_cardinality == 'multi' for this Q's subtopic → msq
          (requires the subtopic from P3 to look up answer_cardinality)
        - else → mcq
      The resolved per-question type is the ExplanationBlock.qtype (§5-1) and is
      recorded in the delivered sidecar as the fourth map (§S7A-4).

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
Figural vision     : [n/n artefact(s) transcribed across k question(s)]
                     OR [no figural questions] OR [AMBER — v VOID_ITEM]
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
      If about to HALT because a figure cannot be seen, STOP — that is a
      VOID_ITEM + AMBER, never a halt (§13A-5). If about to derive a figural
      answer with no OK transcription behind it, STOP — that is RE-11.

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
    F. Set FINAL_BATCH = (k == K), then run §19 (S19-1 gate → S19-2 present_files): the
       whole paper every batch, plus pyq_explain_progress.json on the final batch (MANDATE D).
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
  Every ⟦MATH:…⟧ region COMPILES at validate() time (t3_compile) — a region the
  Tier-3 grammar rejects RAISES at construction, so it can never degrade to raw
  text at render (§S11-1a; 2026.08.10.3). A breach raises in
  ExplanationBlock.validate() / add_math_text.

## S5-3 — PER-QUESTION CHECKLIST (tick every item before constructing the block)

```text
  [ ] Full stem + ALL options read to the end; OMML merged with text
  [ ] Question TYPE resolved: mcq · msq · nat
  [ ] Negative phrasing scanned (NOT/EXCEPT/INCORRECT/FALSE)        → §10a
  [ ] Composite options scanned (Both/Only/All/None of the above)   → §10b
  [ ] Figural? → transcription read from pyq_figural_vision.json    (§13A)
      (VOID_ITEM there → no answer is published for this Q; §13A-5)
  [ ] Answer derived from first principles AND a second method       (§7)
  [ ] Methods agree (else DERIVATION-CONFIDENCE)                     (§7)
  [ ] Factual content web-verified with a recorded source            (RE-18)
  [ ] Class identified (§6); the right section LEADS
  [ ] AXIOM states a TRUTH, not the task; no restatement
  [ ] DEDUCTION last step binds the answer
  [ ] SPEED HACK present IFF genuinely shorter route found           (§14)
  [ ] WHY WRONG covers exactly the non-selected options (§15)
  [ ] DIFFICULTY assessed from this question's own derivation      → §7A
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
  audit_canonical.py's A-NAT-GRADE implementation.

# ════════════════════════════════════════════════════════════════════════
# §7A — PER-QUESTION DIFFICULTY ASSESSMENT (v1.1)
# ════════════════════════════════════════════════════════════════════════
#   PYQ-1 is the SINGLE PRODUCER of per-question difficulty for the PYQ pipeline.
#   This section records what the derivation just revealed. It introduces no new
#   analysis, re-reads nothing, and never touches the delivered document.

## S7A-1 — Exact position in the per-question flow

  Within a batch (§4-4), for each question:

```text
   1. Read stem + ALL options                        ← question loaded
   2. Classify (§6)                                  ← class facet(s) known
   3. Derive via Method 1 (§7)                       ← reasoning path walked
   4. Derive via Method 2 (§7)                       ← agreement / DERIVATION-CONFIDENCE known
   5. Build AXIOM (§8-2)                             ← principle count known
   6. Build DEDUCTION (§8-3)                         ← step count known
   7. Test SPEED HACK gate (§14)                     ← alternative route known
   8. Build WHY WRONG / COMMON PITFALLS (§15)        ← option analysis done
   9. ★ ASSESS DIFFICULTY (this section)             ← record the observations
  10. block.validate()                               ← block verified
```

  Step 9 runs AFTER all derivation and BEFORE block finalisation, so every
  observation is fresh and first-hand. Running it earlier is a defect: the step
  count and the speed-hack verdict do not exist yet.

## S7A-2 — The six observations (all already made — do not re-derive)

| Observation | Type | Source | Meaning |
|---|---|---|---|
| `question_class` | str or list[str] | §6 | class facet(s), e.g. `C-FACTUAL`, `C-NUMERICAL-INPUT` |
| `deduction_steps` | int | §8-3 | number of steps in the DEDUCTION just built (engine minimum 2) |
| `axiom_concepts` | int | §8-2 | distinct principles the AXIOM had to state (1 = single concept) |
| `speed_hack_exists` | bool | §14 | the two-part gate passed and a SPEED HACK was written |
| `derivation_confidence` | `'full'` or `'flagged'` | §7 | `'flagged'` iff the two methods initially disagreed |
| `is_negative` | bool | §10a | NOT / INCORRECT / EXCEPT / FALSE polarity in the stem |

  Plus `qtype` (`mcq` / `msq` / `nat`, from §5-1) and the exam's
  `difficulty_labels` (from exam_config.json; default `['Easy','Medium','Hard']`).

  COUNTING RULES — fixed, so two instances counting the same block agree:
  * `deduction_steps` = the number of discrete inferential moves in the DEDUCTION,
    which is the number of DEDUCTION paragraphs the block carries. Do not count
    the answer-binding sentence separately when it shares a paragraph with the
    final move.
  * `axiom_concepts` = the number of DISTINCT named principles, laws, formulae, or
    definitions the AXIOM states. Two applications of one principle count once;
    a principle plus an independent definition it does not follow from count twice.

## S7A-3 — The assessment call

```text
from blueprint_core import assess_difficulty   # Cluster E2 — PURE, no I/O

label = assess_difficulty(
    question_class        = <§6 class facet(s)>,
    deduction_steps       = <§8-3 step count>,
    axiom_concepts        = <§8-2 principle count>,
    speed_hack_exists     = <§14 gate verdict>,
    derivation_confidence = 'flagged' if methods initially disagreed else 'full',
    is_negative           = <§10a scan result>,
    qtype                 = <'mcq' | 'msq' | 'nat'>,
    difficulty_labels     = <exam_config.difficulty_labels, default Easy/Medium/Hard>,
)
```

  `assess_difficulty` is a pure function: identical observations always return the
  identical label, on every run and every model instance. PYQ-1 MUST NOT override,
  round, smooth, or "balance" its output — there is no target distribution here.
  A paper legitimately skewed toward recall SHOULD come out skewed.

  It returns `None` when `difficulty_labels` is not an exactly-3-label list (the
  same contract as `map_difficulty_level`). On `None`: omit that question from
  `q_to_difficulty` entirely — never write a `None` or a guessed value — and note
  it once in §R11. PYQ-4 then resolves those questions on its own lower tiers.

## S7A-4 — Recording

  After the batch's questions are assessed, write into
  `pyq_explain_progress.json` alongside `q_to_classification`:

```json
{
  "_meta": { "exam_code": "...", "phase": "pyq_explain", "...": "..." },
  "q_to_classification": { "1": { "...": "..." } },
  "options_by_q": { "1": 4, "41": 0 },
  "qtype": { "1": "mcq", "31": "msq", "41": "nat" },

  "q_to_difficulty": { "1": "Easy", "42": "Medium", "54": "Hard" }
}
```

  * Keys follow the SAME convention as every other per-question map: JSON object
    keys are strings; readers normalise to int.
  * `qtype` values (v2.3) are members of {'mcq','msq','nat'}, resolved at P4
    (position-based first, structural fallback). qtype is a STRUCTURAL TYPE, not
    answer content — MANDATE-0-safe — and covers every question 1..Q_TOTAL.
  * Values are members of `difficulty_labels`, nothing else.
  * Written incrementally per batch, so a resumed run (§4 P8) keeps the labels
    already produced and never re-assesses a completed batch.
  * NEVER rendered into the document. This is metadata for PYQ-4 only (v2.1: PYQ-2
    retired, so the difficulty map is no longer independently validated).

## S7A-5 — What this measures, and what it does not

  MEASURES: what solving the question actually required — how many inferential
  moves, how many distinct principles, whether every option had to be evaluated
  independently, whether an exact value had to be produced with no options to
  check against, whether two independent methods agreed.

  DOES NOT MEASURE: student-relative difficulty. A question that is routine for a
  well-prepared candidate and brutal for an average one receives one label. No
  step in this pipeline has response data, and none should pretend to.

  EXAM-AGNOSTIC BY CONSTRUCTION: every input is an observation about the act of
  solving. None of them names an exam, a subject, a topic, or a language, and
  none of them is a word list. This is the property that makes one function
  correct for ~200 exams, and it is the property that E-9's keyword axes — where
  the vocabulary IS the instrument — can never have. Do not add subject-aware or
  vocabulary-aware terms to this assessment.

# ════════════════════════════════════════════════════════════════════════
# §8 — SECTION QUALITY STANDARDS (highest-standard contract per section)
# ════════════════════════════════════════════════════════════════════════
#   Governing rule across ALL sections — the DENSITY FLOOR (not a length floor):
#   every line must add a NEW number, fact, or reason; NO sentence may restate
#   another. Brevity is allowed only when the line is dense; a line carrying none
#   of its required facts fails the content floor (producer discipline enforces the
#   no-restatement rule code cannot).

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
  Enforced: three-way binding at write time; truth by derive-twice + web-verify
  + producer discipline (§18 self-audit).

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
  not task", "why not just what", correctness by discipline (§18 self-audit).

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
  substitution + producer discipline (§18 self-audit).

## S8-4 — SPEED HACK
  Role: exam-craft — a genuinely shorter route to the SAME answer, for time
  pressure; optional by design. Standard: a structurally DIFFERENT, faster path
  (not the same steps reworded); same CA; one or two dense lines; names the actual
  lever ("test divisibility by 3 first", "back-solve from the options", "only 39
  fits"). Vague encouragement ("do it mentally", "obvious with practice") is
  banned — that is a platitude, not a hack. Inclusion is decided per question by
  §14; if no honest shortcut exists the block is OMITTED, never padded.
  Enforced: if present, binds the same CA (engine); "genuinely faster, not
  cosmetic" by discipline (§18 self-audit).

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
  + factual truth by discipline (§18 self-audit).

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
# §11 — MATH / OMML RENDERING DISCIPLINE (v2.0 — Tier-3)
# ════════════════════════════════════════════════════════════════════════
#   Every piece of math in an explanation is real OMML — never inline text, glyph,
#   LaTeX, or ASCII dialect. Same OMML standard as PYQPrepare v2.0, via the SAME
#   compiler: t3_mathcomp.py (byte-identical to Framework_PYQPrepare §S3-5b; the
#   engine self-test drift-locks the two — one grammar, no divergence possible).

## S11-1 — The single funnel (write-time enforced; v2.0)
  All prose enters via add_math_text(). Any non-trivial math is written as a
  ⟦MATH:…⟧ LaTeX-lite region and compiles to ONE homogeneous <m:oMath> through
  the shared Tier-3 compiler — fractions \frac/\sfrac, scripts x^{n}/V_{B},
  radicals \sqrt/\root, n-ary operators with true operands, \lim, \cases,
  matrices, \pre prescripts, stretchy delimiters, \bar/\vec/\hat accents
  (Boolean negation and vectors are ACCENTS, never combining characters), roman
  functions, and the Greek/relation symbol map. Plain segments keep the v1
  digit/digit auto-fraction path byte-compatibly; units km/h, m/s stay text.
  THE DIALECT IS BANNED: guard_sentence() raises — at authoring time, invisible
  to the operator — on ÷ between operands, caret exponents, V_B-style
  underscores, √( or √letter, and any combining accent character, each naming
  the ⟦MATH:…⟧ spelling as the remedy. Guards are region-aware: \frac inside a
  region is legal; the _BANNED_LATEX list applies to prose outside regions only.
  A region the compiler rejects at RENDER time degrades to ordinary plain text
  (no colour, no markup), is recorded in T3_STATS['failed'], and is quoted
  VERBATIM by verify_explanations() — the strict-core/forgiving-boundary contract
  shared with PYQPrepare S3-5. That render path is now DEFENCE-IN-DEPTH, not the
  primary gate.

## S11-1a — AUTHORING-TIME COMPILE GATE (BLOCKING; 2026.08.10.3)
  ExplanationBlock.validate() COMPILES every ⟦MATH:…⟧ region through t3_compile
  and RAISES a ValueError on any MathCompileError, so a region that cannot compile
  fails at CONSTRUCTION — before any docx exists and before it can ever reach the
  renderer. validate() is the ONE universal chokepoint (called on every block, in
  every step, in BOTH pipelines, for all exams, driving the SAME explain_engine.py
  under MANDATE A) and it RAISES, so this gate cannot be bypassed by a producer's
  §18 harness. It mirrors the NAT grading-value posture ("Fail-at-construction:
  the primary gate; render() re-checks as defense-in-depth", §S5-2 / S7-4).
  WHY THIS EXISTS. Before 2026.08.10.3 a ⟦MATH:…⟧ region was compiled ONLY at
  render. A rejected region did not raise there — by the no-halt render contract
  it degraded to raw text and shipped as literal LaTeX unless the producer
  separately consumed verify_explanations()'s RETURNED (ok, problems) ledger. That
  returned-not-raised signal was dropped by a harness that checked only whether the
  call raised, and a whole paper shipped with un-rendered LaTeX under green audits.
  The authoring gate removes the window entirely: the region never renders at all.
  The gate is exam-agnostic — it names no exam, subject, or value; it is pure
  Tier-3 grammar. Only ⟦MATH:…⟧ (Tier-3) is compiled; ⟦M:<b64>⟧ preserve tokens
  are never matched by T3_REGION_RE and are untouched.

## S11-2 — Post-write verification (every batch; v2.0)
  verify_explanations() re-parses the RENDERED docx and re-confirms: every OMML
  fraction is well-formed WITH run-level children — bare text directly inside
  m:num/m:den is SCHEMA-INVALID and named as such (Word renders it as an empty
  ▯/▯ placeholder; itertext()-style readers that accept it are the defect, not
  the proof); Tier-3 structural integrity (sSubSup/rad/nary/limLow complete,
  matrices rectangular); zero ASCII-dialect residue in rendered prose; and the
  region ledger — every ⟦MATH:⟧ region in the blocks either compiled or is
  quoted verbatim in a plain-language degrade report.

## S11-2a — Input health (before generating; v2.0)
  source_math_health() scans the SOURCE paper's question regions for upstream
  math loss — gap signatures where a symbol vanished, empty OMML islands, and
  dialect already present in stems — and prints plain-word warnings ending with
  the remedy: re-run PYQPrepare v2.0 on the source PDF FIRST, then regenerate.
  Advisory, never a halt: PYQ-1 must never silently launder inherited damage.

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
  v1.2: this happens ONCE per paper, at P2a, via §13A — not per batch. Role
  binding is READ FROM THE DOCUMENT (a drawing in a paragraph whose text opens
  with an option label binds to that option), never inferred from extraction
  order.

## S13-3 — Derive from the images
  VIEW → derive → proceed. No manifest cross-check for PYQ (no registry).
  v1.2: at solve time the observation is read from pyq_figural_vision.json
  (§13A-4). That file IS the record of the view — reading it is not "deriving
  from a manifest" in the §13-3 sense that TestExplain forbids, because no
  registry stated what the figure was SUPPOSED to contain; the transcription
  records only what was actually seen.

## S13-4 — Write what is visible
  AXIOM = the visual rule. DEDUCTION traces the VISIBLE transformation.
  WHY WRONG names, per wrong option-figure, the specific visual difference.

# ════════════════════════════════════════════════════════════════════════
# §13A — FIGURAL PRE-TRANSCRIPTION PASS (v1.2; MATERIALISE-THEN-INJECT)
# ════════════════════════════════════════════════════════════════════════
#   View every figure ONCE, at P2a, and persist what was seen as TEXT. Every
#   batch afterwards reads the text. Governed by the EXECUTION-BOUNDARY LAW
#   (CLAUDE.md): `view` is CLASS T, so it happens only BETWEEN model turns and
#   is NEVER modelled as a Python function, callback, or parameter.
#
#   WHY ONCE, AND WHY EARLY. An image in context is volatile; text on disk is
#   not. Viewing lazily meant the last figural batch asked the image channel for
#   a fresh render at the point of greatest context pressure — after the clone,
#   the bootstrap, two specs read in full, and every earlier batch. Viewing once
#   at P2a spends vision when it is cheapest and converts it into an artefact
#   that survives every later batch, every resume, and every session break.

## S13A-1 — Applicability
  Runs at P2a for every paper with ≥1 figural question (§13-1 detection: a
  <w:drawing> in the STEM or any OPTION). Zero figural questions → skip and
  record "no figural questions" in the P7 dashboard. Never skipped for any
  other reason, and never deferred into a batch.

## S13A-2 — PHASE A (python — deterministic)
```python
import figural_vision as fv, os
FIGDIR = '/home/claude/figures'
items = fv.extract_figures(CLEAN_ROW_FILE, FIGDIR, cfg.q_re, cfg.opt_re)
fv.write_queue(items, '/home/claude/pyq_figural_queue.json')
print(fv.vision_report_line({'clean': True, 'ok_items': 0,
                             'total_items': len(items)}))
for it in items:
    print(fv.item_key(it), it['path'])
```
  q_re / opt_re come from EngineConfig (section_rules CATEGORY C) — no exam
  value is hardcoded (RE-9). Media bytes are written out UNCHANGED: nothing is
  re-encoded, so §12 byte-identity is untouched and this pass never writes to
  the delivered document.

## S13A-3 — PHASE B (model — IN-TURN tool calls; NOT a code block)

  Phase B is prose by law. Do not implement it, do not wrap it in a ```python
  fence, and do not name a function for it. The urge to "implement" Phase B is
  the bug, not the fix.

```
  For each item printed by Phase A, in order:
    1. Call the view tool on item.path.
    2. Record, in your own words, EVERY visible element: labels, axis names and
       scales, arrows and their direction, shapes and their relative position,
       printed values, shading, counts. Transcribe what is THERE; do not solve
       the question and do not interpret it — interpretation happens at solve
       time, from this text.
    3. If the payload comes back blank or unreadable, retry that item ONCE. If
       it is still blank, write an EMPTY string for it and move on. Do not
       guess, do not infer the figure from the surrounding stem text, and do
       not halt.
  Then write every transcription to /home/claude/pyq_figural_transcripts.json
  as {item_key: {"text": "...", "sha256": "<item sha256>"}}.
```

  MANDATE 0 STILL BINDS. The transcriptions go to a FILE. No stem, option,
  figure description, or derived answer is ever printed in chat — the only
  chat output from this pass is the MANDATE-0-safe count line of §13A-5.

## S13A-4 — PHASE C (python — deterministic; NEVER raises)
```python
import figural_vision as fv, json
items = fv.load_queue('/home/claude/pyq_figural_queue.json')
transcripts = json.load(open('/home/claude/pyq_figural_transcripts.json'))
report = fv.verify_transcripts(items, transcripts)
fv.write_manifest(items, transcripts, report,
                  '/home/claude/pyq_figural_vision.json')
print(fv.vision_report_line(report))
```
  verify_transcripts classifies each artefact OK / MISSING / EMPTY / THIN /
  STALE. THIN catches the payload that arrived but says too little to derive
  from; STALE catches a transcription written against a different image. It
  returns a report — it does not raise, and Phase C never halts the run.

  At solve time (§4-4 A) a figural question reads its observation with
  `fv.transcript_for(manifest, q, role)`. That returns None for any artefact
  that is not OK, so an unusable transcription can never reach a derivation.

## S13A-5 — SEVERITY: AMBER and VOID_ITEM only; BLOCKING never
  A vision shortfall NEVER stops the paper. Three-tier model:

  | Condition | Severity | Effect |
  |---|---|---|
  | every artefact OK | — | normal run |
  | ≥1 artefact not OK | AMBER | run completes; footer is amber (F1) |
  | a question with ≥1 not-OK artefact | VOID_ITEM | that Q publishes no answer |
  | any vision condition | never BLOCKING | a paper is never halted by vision |

  A VOID_ITEM question takes the §17-3 VERY-RARE shape mechanically — an
  ExplanationBlock carrying the anomaly flag and NO content (the engine forbids
  anomaly + content on one block) — so batch COVERAGE stays exact and the
  S4-5 guard 3 assertion still holds with no gaps. It is reported SEPARATELY
  from exam-body defects (§20 §R12, not §R7): an untranscribable figure is a
  SESSION defect with a known remedy, not a fact about the exam paper.

  WHY VOID AND NOT GUESS. RE-11 forbids deriving a figural answer from anything
  but the image. With no legible image there is no honest derivation, and this
  document is a learner-facing answer key — a fabricated figural answer is the
  single most damaging output this pipeline can produce. Publishing nothing for
  that question is recoverable; publishing a guess is not.

  REMEDY, stated in the footer and the report: re-run PYQExplain in a session
  with a working view tool. The pass is cheap and idempotent — a re-run that
  transcribes cleanly clears the VOID_ITEM and the amber.

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
  SPEED HACK — omit it. An empty or generic SPEED HACK is a defect — caught by
  producer discipline (§18), since (v2.1) no downstream audit follows.

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
  (v2.1: the former fourth layer — "PYQ-2 IS THE INDEPENDENT NET" — is GONE.
  PYQExplainAudit is retired, so no independent re-read follows this step. The
  defences above are producer-side only; the risk they must now carry alone is
  PRODUCER SELF-DECEPTION, blocked by §18's read-back-the-document checks.)
  The guarantee: "a weaker line CANNOT REACH THE STUDENT", caught at three
  producer-side layers that do not weaken with length.

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
    PYQ-AMBIGUITY note in pyq_answer_keys.json is surfaced in the END-OF-PAPER
    REPORT for HUMAN review (v2.1: PYQ-2 retired — no auditor consumes it).
    Unlike TestExplain (which halts and escalates to Step 8), PYQ-1 CONTINUES
    because there is no upstream step to fix the paper — it IS the actual exam.
    The ambiguity is noted in the END-OF-PAPER REPORT (§20) for human review.
  • VERY RARE: the question is genuinely unanswerable (corrupt image, missing
    data, truncated stem from scan defect) → set the anomaly flag (no content),
    skip explanation for this question, note in report for human review.
    The anomaly flag is reserved for THIS case only — a question so broken that
    no answer can be defended at all.
  • VISION-UNAVAILABLE (v1.2, §13A-5): a figural question whose image could not
    be legibly transcribed at P2a. Mechanically identical to the VERY RARE case
    (anomaly flag, no content, coverage preserved), but it is NOT an exam-body
    defect and MUST NOT be reported as one — the paper is fine and the session's
    view tool was not. Report it in §R12, never §R7, with the remedy. Do not
    convert it into a derived answer by reasoning from the surrounding stem
    text; that is precisely what RE-11 forbids.

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
  [ ] verify_explanations(out, blocks) -> (ok, problems): INDEPENDENT post-render
      re-audit (§11). BLOCKING CONTRACT — the verifiers RETURN status, they do NOT
      raise: assert ok is True AND problems == [] AND explain_engine.T3_STATS
      ['failed'] is empty. A non-empty degrade ledger (a ⟦MATH:⟧ region that fell
      back to plain text) is a BLOCKING FAIL — present_files is FORBIDDEN. A run
      that checks only "did the call raise" is NON-CONFORMING and will ship raw
      LaTeX. (As of 2026.08.10.3 validate() also compiles regions and RAISES at
      construction, §S11-1a, so this ledger should always be empty; the assertion
      is the second gate that guarantees it.)
  [ ] count invariants: image / table / OMML / question / option counts == Row file
  [ ] strip-and-re-audit: questions-only copy passes (§12-3)
  [ ] every CA fact web-verified with a recorded source (§7 / RE-18)
  [ ] derived answers flushed to pyq_answer_keys.json; CA three-way binding holds
  [ ] coverage assertion (S4-5 guard 3): exactly Q1..last(batch k)
  [ ] learnings coverage (§24): every applicable rule routed
  [ ] figural coverage (§13A): every figural Q in this batch either
      carries an OK transcription or is a recorded VOID_ITEM — never
      a figural answer with no transcription behind it
```
  Any item open → fix, re-build, re-audit. present_files FORBIDDEN until ALL hold.

## S18-1a — MATH-INTEGRITY GATE (literal, MANDATORY before present_files; 2026.08.10.3)
  The verify_explanations line above is enforced by this exact HARD STOP, run every
  batch after the cumulative build and BEFORE the S19-1 delivery gate. It exists
  because verify_explanations RETURNS its verdict rather than raising, and a run
  must consume that return — not merely call it.
```python
import explain_engine as _ee
_ok, _problems = _ee.verify_explanations(out, blocks, cfg, expected_qs=EXPECTED)
_degraded = list(_ee.T3_STATS.get('failed', []))
if (not _ok) or _problems or _degraded:
    # A ⟦MATH:⟧ region degraded to raw text, or another render check failed.
    # Every such region is quoted verbatim in _problems (§11-2). Fix the Tier-3
    # syntax (§11 / §S11-1a) and rebuild — do NOT deliver.
    raise SystemExit('HARD STOP (§18-1a): verify_explanations not clean — '
                     f'ok={_ok}; problems={_problems[:3]}; '
                     f'degraded_regions={[b for b,_ in _degraded][:3]}')
```
  Note: as of 2026.08.10.3 a malformed region cannot reach the renderer at all —
  ExplanationBlock.validate() raises on it at construction (§S11-1a) — so in a
  conforming run _degraded is always empty here. This gate is the belt to that
  braces: it converts the engine's RETURNED ledger into a delivery-blocking
  condition, closing the returned-not-raised gap permanently. Exam-agnostic.

## S18-2 — THIS IS THE ONLY GATE (v2.1 — PYQ-2 retired; stated, not hidden)
  PYQ-1's §18 is PRODUCER self-certification, and as of v2.1 it is the ONLY
  certification this document will ever receive. The former independent half —
  PYQ-2 (PYQExplainAudit) re-deriving every answer and running the
  explain_audit_gate.py completion gate (CA1-CA7) — is RETIRED and is no longer
  run by any step. ACCEPTED LOSS, stated once: no independent re-derivation of any
  answer, no independent completion gate, and no official-answer-key cross-check
  (former PYQ-2 D4) exist after this step. Correctness rests on producer discipline
  (§7 derive-twice, RE-18 web-verify, §13/§13A view-every-image) plus the engine's
  write-time shape guarantees. The per-question handoff data (derived answers,
  web-verified facts, viewed-image confirmations, DERIVATION-CONFIDENCE flags) is
  still recorded IN FULL and handed off (RE-20) — its consumer is now a HUMAN
  reviewer, not a gate. The risk that replaces producer<->auditor drift is PRODUCER
  SELF-DECEPTION, which §18-1's read-back-the-written-document checks (never
  self-report) are the only defence against. Run them literally.

# ════════════════════════════════════════════════════════════════════════
# §19 — DELIVERY (incremental whole-paper; one present_files per batch)
# ════════════════════════════════════════════════════════════════════════

## S19-1 — Pre-delivery checklist (MANDATORY before present_files)
```python
import os, shutil
out  = '/mnt/user-data/outputs'
sol  = f'{EXAM}_{DATE_SESSION}_PYQ_Explanation.docx'
prog = f'{EXAM}_{DATE_SESSION}_pyq_explain_progress.json'  # v2.2.1 — identity-prefixed handoff
src  = '/home/claude/pyq_explain_progress.json'            # bare internal working file
FINAL_BATCH = bool(globals().get('FINAL_BATCH'))          # True only on the last batch (k == K)
# On the final batch, promote the COMPLETE handoff into outputs under the paper-identity name.
# GUARDED (v2.2.1): a missing source is reported by check 6 as a clean HARD STOP, never a crash.
if FINAL_BATCH and os.path.exists(src):
    shutil.copy(src, f'{out}/{prog}')
expected = {sol, prog} if FINAL_BATCH else {sol}          # handoff ships ONLY at 100% coverage
present = set(os.listdir(out))
# TRUE internal state must never leak; the one delivered handoff (in `expected`) is exempt.
BANNED = ('answer', 'key', 'ledger', 'progress', 'state', 'pickle', 'stripped', 'source')
leaked = [f for f in present if f not in expected and any(b in f.lower() for b in BANNED)]
# v2.3: the fourth map (qtype) must be complete before the handoff ships — coverage
# is tied to q_to_classification so an incomplete qtype cannot pass as complete.
_qtype_complete = True
if FINAL_BATCH:
    try:
        import json as _j
        _h = _j.load(open(f'{out}/{prog}'))
        _exp = {int(k) for k in _h.get('q_to_classification', {})}
        _qt  = {int(k) for k in _h.get('qtype', {})}
        _qtype_complete = bool(_exp) and _qt == _exp
    except Exception:
        _qtype_complete = False
checks = [
    ('1 PYQ explanation docx in outputs',       os.path.exists(f'{out}/{sol}')),
    ('2 self-audit (S18) all clean',            bool(globals().get('SELF_AUDIT_CLEAN'))),
    ('3 whole-paper coverage asserted',         bool(globals().get('COVERAGE_OK'))),
    ('4 no internal sidecar leaked',            not leaked),
    ('5 outputs == exactly the deliverables',   present == expected),
    ('6 handoff json present on final batch',   (not FINAL_BATCH) or os.path.exists(f'{out}/{prog}')),
    ('7 qtype map complete on final batch',     (not FINAL_BATCH) or _qtype_complete),
]
fails = [n for n, ok in checks if not ok]
if fails:
    raise SystemExit('HARD STOP (S19-1): ' + '; '.join(fails))
```

## S19-2 — The present_files call (per batch; +handoff json on the FINAL batch)
```python
def present_files(paths):
    """CLASS: T — the chat file-delivery tool. NOT executable python.

    GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), DEFECT-CLASS SWEEP.
    This spec CALLED present_files() from compiling python while DEFINING it
    nowhere — a guaranteed NameError the moment the path executes as python. Five
    such call sites stood across four specs (Framework_MockTestAnalyse.md twice,
    Framework_PYQScan.md, Framework_PYQExplain.md, Framework_MockTestExplain.md).
    It reached production because spec_name_audit_baseline.json accepted
    `present_files` as a known-unbound name in all four.

    SAME SHAPE as D2 of GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, where
    collect_drive_docx_recursive() called the CLASS T marker gdrive_search() from
    python. That gap fixed the INSTANCE; the CLASS stood eleven days longer.

    Declared per-spec, matching this corpus's CLASS T house pattern (gdrive_search
    is declared in both Framework_MockTestAnalyse.md and Framework_PYQCount.md).
    The F1/F2 footer contract is owned by Framework_DeliveryFooter.md.

    The model performs the call in its own turn, after python returns. Nothing is
    returned to python and NO call site may consume a result (C6).
    """
    pass  # CLASS: T — performed by the model between turns, never from python
deliverables = [f'/mnt/user-data/outputs/{EXAM}_{DATE_SESSION}_PYQ_Explanation.docx']
if FINAL_BATCH:                       # v2.2.1 — ship the identity-prefixed handoff at 100% coverage
    deliverables.append(f'/mnt/user-data/outputs/{EXAM}_{DATE_SESSION}_pyq_explain_progress.json')
present_files(deliverables)
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
  §R1 PROVENANCE: paper [date] [session] · spec v1.1 · engine 62/62 · timestamp ·
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
  §R8 HANDOFF (RE-20): what was derived, what was web-verified, what is
      model-derived, where to look hardest — for the HUMAN reviewer (v2.1: PYQ-2
      retired, so this handoff is the ONLY surviving record of where the run was
      least certain; it is MANDATORY, never abbreviated). Next: PYQ-3 (PYQFormat,
      student doc) OR PYQ-4 (PYQDeliver, portal) — both take THIS
      _PYQ_Explanation.docx directly. State: review IN MICROSOFT WORD.
  §R9 SUBTOPIC CLASSIFICATION MAP: summary of q_to_classification (Q→subtopic
      mapping) for PYQ-3 (PYQFormat pills) and PYQ-4 (PYQDeliver tags).
  §R10 LIMITATIONS (§22).
  §R11 DIFFICULTY ASSESSMENT (§7A, v1.1): the resolved label distribution across
       the paper; every Q omitted from q_to_difficulty with its reason; and the
       count of Qs whose derivation_confidence was 'flagged'. If EVERY question
       resolved to the SAME label and the paper has more than one question, say so
       explicitly — a whole paper at one difficulty is a signal worth checking
       before delivery, not a result to pass along silently.

  §R12 FIGURAL VISION (§13A, v1.2): artefacts extracted · artefacts transcribed
       OK · every VOID_ITEM question with its status (MISSING/EMPTY/THIN/STALE)
       and the stated remedy. Reported here and NOT in §R7 — a vision shortfall
       is a session defect, not an exam-body error. If any VOID_ITEM exists the
       verdict is SHIP-AMBER, never SHIP.

# ════════════════════════════════════════════════════════════════════════
# §21 — DEFINITION OF DONE / HARD INVARIANTS
# ════════════════════════════════════════════════════════════════════════
  1.  Pre-flight P0-P10 passed; engine 62/62; config built from section_rules.
  2.  Every question explained (zero sampling); every validate() clean.
  3.  Every answer derived two ways; disagreements resolved 2-of-3 +
      DERIVATION-CONFIDENCE. Zero guesses. Typed correctly (mcq/msq/nat).
  4.  Every figural question's images extracted, role-bound, VIEWED ONCE at
      P2a (§13A) and persisted; every figural answer traceable to an OK
      transcription, or the question recorded as VOID_ITEM.
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
# §24 — LEARNINGS CONSUMPTION CONTRACT (human-authored guardrails; v2.1)
# ════════════════════════════════════════════════════════════════════════
#   PYQExplainAudit (PYQ-2) — which used to AUTO-GENERATE PYQ audit learnings — has
#   been RETIRED (v2.1). No step now produces PYQ_EXPLAIN_AUDIT_LEARNINGS or
#   EXPLAIN_AUDIT_LEARNINGS automatically, so the automatic feedback loop is OPEN.
#   PYQ-1 remains the CONSUMER: it still LOADS and OBEYS every learnings file present,
#   so human-authored guardrail rules (and any AL-rules already written before
#   retirement) keep working exactly as before. Nothing here HALTS on absence.
#
#   FOUR learnings files, all loaded at P1, all OVERRIDE this spec on content:
#     • [ExamCode]_PYQ_EXPLAIN_AUDIT_LEARNINGS_v*.md — PYQ-specific AL-rules.
#       Formerly auto-generated by PYQ-2; now LEGACY + manually authored only.
#     • [ExamCode]_PYQ_EXPLAIN_LEARNINGS_v*.md — PYQ-specific human guardrails.
#     • [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md — shared exam AL-rules. Formerly
#       auto-generated by the mock audit step (also retired); now legacy + manual.
#     • [ExamCode]_EXPLAIN_LEARNINGS_v*.md — shared human guardrails.
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
#     --self-test-audit → "AUDIT-SELF-TEST: N/N PASS", N >= 10 (reader round-trip; v2.5 floor form)
#   (v2.1: the companion gate explain_audit_gate.py and PYQExplainAudit (PYQ-2) were
#    RETIRED and removed from the framework; PYQ-1 does not use them.)

# ════════════════════════════════════════════════════════════════════════
# SHARED_RULES_VERSION: 1.1 (2026-08-10)
#
# DELIBERATE PYQ-ONLY DIVERGENCE (v1.2, 2026-08-03) — RECORDED, NOT DRIFT.
#   §13A (figural pre-transcription pass) is NEW and is NOT mirrored in
#   Framework_MockTestExplain.md. No RE-* rule, no MANDATE, and no existing
#   §4-§18 rule was MODIFIED: §13-2 / §13-3 gained pointer lines only, exactly
#   as §5-3 did for §7A. SHARED_RULES_VERSION is therefore NOT bumped, on the
#   same reasoning recorded for v1.1 below.
#
#   WHY THE MOCK SIDE IS NOT MIRRORED. The two pipelines do not face the same
#   risk. A mock paper's figures are GENERATED by figural_core from a spec
#   sidecar, and registry.json carries figural_manifests[] recording what Step 7
#   intended to draw — so TestExplain §13-3 already has an independent semantic
#   cross-check when the pixels are unreadable, and Step 8 already has its own
#   measured vision route (COMPLETION-GATE: DEGRADED (vision), Audit v2.16 / D2).
#   A PYQ paper has NEITHER: §13 states plainly that for PYQ there are no
#   figural_manifests and no registry. The image is the ONLY record of what the
#   figure contains, which is exactly why PYQ-1 needs a durable transcription
#   and the mock side does not.
#
#   WHAT A FUTURE SESSION MUST DO. If TestExplain is ever given a pre-
#   transcription pass, it should REUSE figural_vision.py rather than copy §13A:
#   the engine is exam-agnostic and pipeline-agnostic by construction. The mock
#   side would additionally have to specify how a transcription and a
#   figural_manifest that DISAGREE are reconciled — a design decision §13A does
#   not make, because PYQ has no manifest to disagree with. Do NOT resolve it by
#   blindly copying §13A across.
#
# DELIBERATE PYQ-ONLY DIVERGENCE (v1.1, 2026-07-24) — RECORDED, NOT DRIFT.
#   Two additions in this file are NOT mirrored in Framework_MockTestExplain.md:
#     * §7A (per-question difficulty assessment) — a NEW section, added between
#       §7 and §8. No existing §4-§18 rule was modified to accommodate it.
#     * one line in the §5-3 per-question checklist pointing at §7A.
#   No RE-* rule and no MANDATE changed, so SHARED_RULES_VERSION is NOT bumped:
#   bumping it would assert a parity that does not exist, and the counterpart file
#   carries no sentinel to bump against.
#
#   WHY THE MOCK SIDE IS NOT MIRRORED. Difficulty means something structurally
#   different in the two pipelines. Here it is a MEASUREMENT: the exam body wrote
#   the questions, so the label must follow the content, and PYQ-1 is the only
#   step that reads and solves them. In the mock pipeline it is a SPECIFICATION:
#   Step 6 sets a difficulty_schedule quota, Step 7 assigns each generated question
#   a band to fill that quota exactly (enforced by G-QINDEX), and Step 11 tags by
#   registry JOIN — content follows the label. Copying §7A into TestExplain would
#   have Step 9 measure a value that Step 7 already fixed, with no specified rule
#   for which wins; that reconciliation is a design decision, not a mirroring
#   chore. The mock-side treatment is DEFERRED pending that decision.
#
#   WHAT A FUTURE SESSION MUST DO. When the mock side is designed, revisit this
#   note. If it adopts assess_difficulty (blueprint_core Cluster E2), the two
#   pipelines will share the RUBRIC while keeping different mechanisms, and this
#   divergence note should be replaced by whatever contract that design defines.
#   Do NOT resolve it by blindly copying §7A across.
#
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
# END OF Framework_PYQExplain v2.6
# ════════════════════════════════════════════════════════════════════════
