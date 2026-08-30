# Framework_PYQExplain v2.21 — Universal PYQ Explanation Generator
# v2.21 — 2026-08-30 — GAP-2026-08-30-EXPLAIN-COLOUR-BINDING (explain_engine v2.11,
#   MockTestExplain v1.49.0, routes.json +figural_core/+corpus_io; SHARED_RULES 1.5 → 1.6).
#   S6A-6 COLOUR: explanation figures draw with figural_core's constants via
#   explain_engine.structure_draw / fc.text_ink / fc.fill_style. Additive; no re-render.
# v2.20 — 2026-08-29 — GAP-2026-08-29-PROFILE-UNSCORED-QUESTIONS (paired with blueprint_core
#   Cluster DP dp_add_paper paper_positions/unscored_reasons, Blueprint v1.58.0 S7-0,
#   audit_canonical v2.24). Two explained 60-question papers were EXCLUDED from an exam's
#   difficulty profile because 1–2 questions carried no derived answer (a VOID_ITEM figure,
#   a defective Row-file option set): the writer counted OBSERVATIONS against
#   total_questions and read the shortfall as a pattern change. It was not — the paper had
#   every position. S7A-6 now passes the handoff's `qtype` map keys as the paper's
#   POSITIONS (the pattern test runs on those) and the new S7A-4 `difficulty_unscored`
#   map {q: reason} for every position without an observation; such a question is
#   recorded UNSCORED in the profile with its reason and left out of the arithmetic — it
#   never excludes its paper and can never bias a mix (a gap shrinks the sample). Only a
#   paper whose positions differ from the current pattern is excluded. §R13 states
#   "added (scored/held; unscored Q list)". Exam-agnostic; no per-exam change.
# v2.19 — 2026-08-28 — GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ (paired with
#   explain_engine v2.10, Framework_MockTestExplain v1.48.0, audit_seam v1.3,
#   validate_framework_md v3.2). Three CATEGORY-C config keys this spec read were
#   produced by NOTHING anywhere in the framework, so their absent-paths ran on every
#   exam forever: representation_renderers (every STRUCTURE_GRAPH / LEVEL_DIAGRAM /
#   DATA_PLOT / CONFORMER verdict degraded per §6A-4), subject_code (the
#   [Subject]_EXPLAIN_LEARNINGS_v*.md subject library was unlocatable and had never
#   loaded on any exam — worsened here by P1's load list never naming the subject
#   file at all), and exam_conventions (§S8-2's EXAM_CONVENTION machinery had no
#   configured input). FIX, exam-independent, zero regeneration: (A) the requirement →
#   library → §6A-5 identifier binding is FRAMEWORK-OWNED in
#   explain_engine.REPRESENTATION_RENDERERS (§6A-6); WHETHER a question uses a
#   renderer stays a per-question §6A-1 decision, so non-scientific exams are
#   byte-unchanged. (B) subject_code RETIRED; the subject library is found by
#   DISCOVERY (explain_engine.resolve_learnings_files; >= 2 non-exam files → abstain +
#   WARN) and P1 now loads it. (C) exam_conventions RETIRED; §S8-2 reads conventions
#   from the subject library only, "never assumed" preserved. Also corrects §S6A-2's
#   stale "last three" (CONFORMER made it four, v2.14). P7 dashboard gains a
#   "Renderer preflight" line and names the loaded subject file. No section_rules.md
#   schema change, no analyse_engine change, no exam regenerated. Gate for the class:
#   validate_framework_md Check V + audit_seam v1.3.
# v2.18 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE (paired with blueprint_core Cluster DP,
#   Blueprint §S7-0, MockTestAnalyse E-9 retirement, PYQDeliver Tier-2 retirement, ScopedBlueprint
#   §1-3/§5). §7A-3 records the raw rubric SCORE (bc.difficulty_score) and the observation
#   record; S7A-4 writes q_to_difficulty_score + difficulty_obs beside q_to_difficulty; NEW
#   S7A-6 writes [ExamCode]_difficulty_profile.json on the final batch through the single
#   writer bc.dp_add_paper (pattern-changed papers recorded as excluded, never a stop);
#   S19-1 check 8, S19-2 deliverable, §R13 report line. PYQ-side rule unchanged (measurement,
#   no target); SHARED_RULES_VERSION unchanged (no RE-*/MANDATE/§4-§18 rule changed).
# v2.17 — 2026-08-24 — CHG-2026-08-24-NO-COVERAGE-BANNER (operator decision; paired with
#   MockTestExplain v1.43.0; SHARED_RULES_VERSION 1.4 → 1.5; NO engine change). The
#   S12-4 document-level coverage banner ("COVERAGE: …") is RETIRED from every delivered
#   _PYQ_Explanation.docx — interim AND final. PYQ-1 no longer calls
#   explain_engine.set_coverage_banner(); the delivered file's first non-blank body
#   paragraph is Q.1. Same reasons as the mock side: the operator does not want a
#   coverage line in the delivered document, and the downstream deliver step
#   (Framework_PYQDeliver, detect_header_paras — same as MockDeliver S4-2) strips any
#   non-blank pre-Q.1 paragraph and raises a regression alarm on it. A new §18-1 item
#   asserts zero banner paragraphs before present_files. Coverage is still stated in
#   chat (S19-3, F1/F2 footer) and asserted per batch (S4-5 guard 3) — only the in-file
#   announcement is gone. Engine untouched (BANNER-* fixtures retained, function unused).
# v2.16 — 2026-08-21 — GAP-2026-08-21-DIFFICULTY-STICKER-LABELS (note-only; §7A
#   itself unchanged). The v1.1 DELIBERATE DIVERGENCE note's deferred mock-side
#   difficulty treatment is RESOLVED under the adopted contract: both pipelines
#   share the rubric (bc.assess_difficulty); mock side enforces it at authoring
#   (MockTestCreate v5.60 G-DIFF), audits it mechanically (audit_canonical v2.15),
#   and re-measures advisorily at Step 9 (TestExplain §7A-M). No shared §4-§18
#   rule changed; SHARED_RULES_VERSION stays 1.4.
# v2.15 — 2026-08-21 — GAP-2026-08-21-EXPLANATION-PROVENANCE (paired with
#   MockTestExplain v1.37.0, engine v2.8). Same defect class, same fixes, so both
#   explanation paths hold one standard; see MockTestExplain v1.37.0 for the
#   incident record (a delivered paper with a wrong published key on a misread
#   structure, 24 hedged / nine arithmetically false WHY WRONG lines, a curated
#   library loaded and never consulted, ASCII formulae throughout). PYQ-side: §13-2b
#   SEMANTIC-OBJECT transcription folds into the §13A pre-transcription pass (a
#   STRUCTURE is transcribed to SMILES and rdkit-sanitised; no registered object
#   exists for a PYQ, so the transcription stands alone); §15-2 REWRITTEN (two
#   provenance modes, engine RECOMPUTES, hedges banned, old wording WITHDRAWN, no
#   pitfall quota); §7-7 step 3 MECHANICAL (Triggers + tripwire); §8-0c FORMULA
#   TYPOGRAPHY; §6A-1b-ii; RE-13 amended, RE-24 new; §18/§21/§24 hooks. §7-8 KEY
#   RECONCILIATION is MOCK-ONLY (a PYQ has no Step-7 commitment; D4 unchanged).
#   SHARED_RULES_VERSION 1.3 → 1.4.
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_PYQExplain.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42), and
#   v2.14 at 2026.08.21.2:
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
#   Self-tests: `python3 explain_engine.py --self-test` → "SELF-TEST: N/N PASS", N >= 62 (v2.5 floor form; §21-0 — no exact count is written here)

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
  RE-11b: FIGURAL FAMILY IS DECIDED, NOT ASSUMED (v2.7). Every figural question is
          classed TRANSFORMATION-PUZZLE or SCIENTIFIC-DIAGRAM before solving (§13-1) and
          read by that family's protocol (§13-4a / §13-4b), from the §13A transcription.
          When mixed or unclear, read it as SCIENTIFIC-DIAGRAM.
  RE-13a: REPRESENTATION IS ROUTED, NOT ASSUMED (v2.7). Every question runs the §6A
          router after derivation and before writing. PROSE is the default; a visual is
          EARNED on the §14 two-part test. A VOID_ITEM figure can never produce a
          generated figure (§6A-2b). Verdicts are recorded and reported (§R3).
  RE-6b : CONDITIONS BEFORE RECALL (v2.10). Every condition a remembered result depends
          on is read back from the stem and checked before the result is applied (§7-0a);
          material assumptions are ledgered (§7-0b). A stated condition the DEDUCTION
          never uses is a misread signal, not a spare part.
  RE-6c : NUMERICAL VERIFICATION (v2.10). Every quantitative answer passes the §7-5
          checks — units, conversions/kelvin, magnitude, log base, sign, stoichiometry,
          precision — which derive-twice cannot catch because both routes can share one
          silent slip.
  RE-6d : CLAIMS CONSISTENT; ENUMERATE BEFORE FORMULA (v2.13). Decisive
          intermediate claims are listed and mutually consistent before writing (§7-6)
          — a right answer with contradictory reasoning is invalid; and a counting
          question is derived inventory-first, a closed-form only after the
          independence it assumes is verified (§7-0c).
  RE-14b: SHORTCUTS ARE SCOPED (v2.10). Every SPEED HACK states the conditions under
          which it is safe, inside the shortcut (§14-3b). Unscopable in one clause → OMIT.
  RE-9b : SUPPORTED VALUES ONLY (v2.9). Every number traces to the stem, a syllabus
          constant, or a shown derivation (§8-0a).
  RE-9c : CALIBRATED LANGUAGE (v2.9). Absolutes only for claims absolute in the
          subject's own terms; tendencies take calibrated terms (§8-0b).
  RE-13 : WHY WRONG DIAGNOSES, NEVER DISMISSES — AND NEVER INVENTS (v2.15). Each
          wrong option carries a §9 diagnosis (internal; rendered in natural language,
          never the raw token) in ONE of two modes: a VERIFIED path the engine has
          RECOMPUTED and that reproduces the option, or a DIRECT CONTRADICTION that
          claims no path (§15-2). Hedged provenance is engine-banned. No guess, ever.
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
  RE-24 : FORMULA TYPOGRAPHY IS ENGINE-APPLIED (v2.15, §8-0c): notation in student prose
          is normalised to Unicode sub/superscripts at construction; residue raises.
  RE-22 : LOAD & APPLY LEARNINGS. At P1, load accumulated learnings files — the
          exam's files AND, v2.14, the subject-level [Subject]_EXPLAIN_LEARNINGS_v*.md
          shared by every exam in the subject (the curated neighbour library §7-7
          tests against) — via parse_learnings and OBEY every applicable rule while
          authoring (§24; precedence exam file > subject file > spec).
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
      v2.19 — RENDERER PREFLIGHT (§6A-6, GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ).
      For each requirement in explain_engine.REPRESENTATION_RENDERERS, import-test its
      library HERE and RECORD the outcome for the P7 dashboard. Step 0 already installs
      the full set (SKILL Step 0: matplotlib pillow numpy scipy fonttools rdkit), so
      this is normally a confirmation; pip (--break-system-packages) only where an
      import fails. An unavailable library NEVER halts: the affected requirement
      degrades for the WHOLE run per §6A-4, disclosed up front as a plain note, so
      quality never varies silently between batches. Nothing is read from
      section_rules for this.

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
        • the SUBJECT-level [Subject]_EXPLAIN_LEARNINGS_v*.md (v2.19,
          GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ) — found by DISCOVERY, never
          by a derived or configured subject code: explain_engine.
          resolve_learnings_files('/mnt/project', ExamCode) returns the single
          non-{ExamCode}-prefixed *_EXPLAIN_LEARNINGS_v*.md as the subject file;
          >= 2 such files → abstain and WARN naming every candidate (load none);
          zero → nothing loaded, nothing lost. The P7 dashboard names the loaded
          subject file and its rule count. Precedence: exam files > subject file
          > this spec (§24).

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
      OPTION-LABEL FORMAT COHERENCE (v2.12 — GAP-2026-08-19-SILENT-LABEL-FORMAT-CONFLICT).
      section_rules declares `option_label_format` in TWO PLACES: once in the CATEGORY C
      header, and once per SECTION block. COMPARE THEM ALL. If the header disagrees with
      ANY section, or two sections disagree with each other → HALT, printing every
      declared value with its location. DO NOT resolve it by precedence, and above all do
      not silently prefer the header — that is exactly the guess this step forbids.
      WHY THIS IS ITS OWN CHECK. The option count and question type were already compared
      above; the LABEL FORMAT was not, and it is generated from a different source: the
      header is written from OBSERVED PYQ papers, while the per-section values come from
      per-section synthesis. Re-running the PYQ analysis can therefore change the header
      alone and leave every section untouched, producing a file that contradicts itself
      with no other symptom. The failure is silent and total: every option in the paper
      carries the wrong label, every explanation binds against it, and NOTHING else in the
      run looks wrong — the counts match, the types match, the paper renders.
      SCOPE, stated honestly: the labels are PRINTED by the generation step, and this step
      only reads them. Halting here does not un-print a paper already generated — it stops
      an explanation run from cementing the wrong labels and tells the author to fix the
      config and regenerate. The same comparison belongs in the generation step; that this
      one is downstream is a reason to surface loudly, not a reason to guess.

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
Learnings loaded   : [k AL-rules · m EX-rules · subject=[filename · r rules] OR subject=none OR subject=AMBIGUOUS(n)] OR [none — first paper]
Renderer preflight : [requirement → library → available/absent → degrade?] per explain_engine.REPRESENTATION_RENDERERS entry (framework-owned, v2.19)
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
  | figures         | list[RepresentationFigure] | v2.7, may be empty. Each carries the §6A-5 validation record (renderer/intended/derived/match) and fails validate() on any breach; rendered as text-free centred picture paragraphs interleaved into DEDUCTION at after_step (§6A-6) |
  | representation_verdict | str/None      | v2.6, optional. The §6A router verdict (PROSE / EQUATION / TABLE / STRUCTURE_GRAPH / LEVEL_DIAGRAM / DATA_PLOT / CONFORMER v2.7). When set, a VISUAL verdict with zero figures raises at validate() — verdict↔emission coherence (§6A-3); after a §6A-4 degrade the block carries the DEGRADED requirement |
  | absolutes_justified | dict{str:str}  | v2.7. {sentence: reason} for each absolute KEPT in AXIOM / SPEED HACK / WHY WRONG / COMMON PITFALLS; an undeclared universal there raises at validate() (§8-0b). Reason = why it is absolute in the subject's own terms |
  | transfer_record | list[dict]/None  | v2.7, REQUIRED by this spec on every block (§7-7). One entry per claim {section, claim, epistemic_type, scope, neighbour_tested, outcome}; shape-validated: AXIOM needs an AXIOM entry, SPEED HACK a SPEED_HACK entry, no QUESTION_SPECIFIC in AXIOM, no OPTION_SET_SHORTCUT outside SPEED_HACK |

  Option index → displayed label is via cfg.option_label() (RE-10).

## S5-2 — Hard structural guards (engine, write-time — position-independent)

  Correct Answer line = INDEX/VALUE ONLY (no option text). DEDUCTION ≥2 steps;
  last binds the answer. WHY WRONG keys == exactly the non-selected options
  (MCQ/MSQ); NAT uses common_pitfalls (≥1) and MUST NOT carry why_wrong.
  OMML for every fraction. One sentence per paragraph. Zero banned content, zero
  internal error-taxonomy tokens in any rendered sentence (§9, v2.6), and no AXIOM
  naming an option label (§8-2, v2.6).
  Every ⟦MATH:…⟧ region COMPILES at validate() time (t3_compile) — a region the
  Tier-3 grammar rejects RAISES at construction, so it can never degrade to raw
  text at render (§S11-1a; 2026.08.10.3). A breach raises in
  ExplanationBlock.validate() / add_math_text.

 (v2.14) Engine v2.7 adds three write-time gates: an
  UNDECLARED UNIVERSAL in AXIOM / SPEED HACK / WHY WRONG / COMMON PITFALLS raises
  (§8-0b; keep one by declaring it in absolutes_justified); a LEARNER-PSYCHOLOGY
  template raises (§15-3); a supplied transfer_record is shape-validated (§7-7).
  DEDUCTION is not absolute-gated — item-specific working, governed by §7-7.

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
  [ ] Figural? → FAMILY decided (transformation-puzzle / scientific-diagram); for
      scientific-diagram, decisive features taken from the transcription and NONE
      inferred from what would make an option work                    (§13-1 / §13-4b)
  [ ] §6A representation router RUN; verdict recorded AND passed into the block
      (engine coherence — a visual verdict requires its figure); PROSE unless the
      two-part test passed; §6A-1b structure-answer questions either emit
      STRUCTURE_GRAPH or record the PROSE justification; VOID_ITEM → never a
      generated figure; any degrade disclosed                                     (§6A)
  [ ] Class identified (§6); the right section LEADS
  [ ] Conditions READ BACK and checked before applying a remembered result (§7-0a)
  [ ] Material assumptions ledgered; any that changes the answer is STATED (§7-0b)
  [ ] Quantitative? → §7-5 checks pass (units · kelvin · magnitude · log base ·
      sign · stoichiometry · precision)                                     (§7-5)
  [ ] Counting question? → inventory → independence → generate → de-duplicate →
      count; a closed-form only after independence is verified              (§7-0c)
  [ ] Decisive intermediate claims LISTED and mutually consistent            (§7-6)
  [ ] SPEED HACK, if present, states when it is safe                       (§14-3b)
  [ ] Every number traces to stem / syllabus constant / shown derivation   (§8-0a)
  [ ] No absolute used for a tendency; no tendency for a real absolute;
      every KEPT absolute declared with its reason (engine gate, v2.7)      (§8-0b)
  [ ] TRANSFER SAFETY: every AXIOM claim and every SPEED HACK typed, scoped,
      tested on its nearest neighbour at this exam's level, repaired by
      MECHANISM where it failed; transfer_record passed to the block        (§7-7)
  [ ] AXIOM epistemic type recorded; MODEL_DEPENDENT / EXAM_CONVENTION rules
      carry their qualifier INSIDE the sentence                             (§8-2)
  [ ] Topic MINIMUM-CONCEPT components (subject learnings, §24) present     (§8-3)
  [ ] REPRESENTATION ALIGNMENT: representation or prose shows the deciding
      relation; spatial / occupancy / topology decisions in PROSE carry
      their explicit inventory                                              (§6A-1c)
  [ ] WHY WRONG / COMMON PITFALLS refute the CONTENT; zero learner-psychology
      narration (engine gate, v2.7)                                         (§15-3)
  [ ] AXIOM states a TRUTH, not the task; no restatement
  [ ] DEDUCTION last step binds the answer
  [ ] SPEED HACK present IFF genuinely shorter route found           (§14)
  [ ] WHY WRONG covers exactly the non-selected options, each first sentence
      delivering its §9 diagnosis in natural language (token internal)       (§15)
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
  | C-FIGURAL        | image-based stem or options                | Family-dependent (§13-1). TRANSFORMATION-PUZZLE: AXIOM = the visual rule (§13-4a). SCIENTIFIC-DIAGRAM: AXIOM = the domain principle; DEDUCTION reads the figure as notation, then solves (§13-4b) |
  | C-STRUCTURAL     | v2.7 — answer turns on CONNECTIVITY, reaction site, spatial/stereochemical arrangement, symmetry, or an enumeration over structures | DEDUCTION leads as a TRANSFORMATION CHAIN: starting arrangement → the change and WHERE → resulting arrangement → why that one. AXIOM = the governing selectivity/structural principle. Enumerations state the generating rule, then the de-duplication, then the count — never a bare number |
  | C-DERIVATIONAL   | v2.7 — a MULTI-STEP chain where each step feeds the next (relations composed, manipulated before use, or a limit taken) — distinct from C-COMPUTATIONAL, which substitutes into ONE relation | DEDUCTION leads and shows the CHAIN, every step as ⟦MATH:⟧ math (§11). AXIOM = the relation the chain starts from plus the condition licensing it. Each WHY WRONG names the ONE step where that option diverges |
  | C-MULTI-SELECT   | answer_cardinality == 'multi'              | DEDUCTION = per-option verdict |
  | C-NUMERICAL-INPUT| NAT — typed numerical answer               | DEDUCTION = computation chain |

  A question may carry more than one facet (e.g. C-FIGURAL + C-COMPUTATIONAL).

# ════════════════════════════════════════════════════════════════════════
# §6A — REPRESENTATION ROUTER (v2.7 — exam-agnostic, domain-configured)
# ════════════════════════════════════════════════════════════════════════
#   Representation selection is an EXPLICIT stage, run once per question AFTER the
#   answer is derived and verified (§7) and BEFORE any explanation prose is written.
#   Same contract as TestExplain §6A — one router across both explanation steps, so a
#   learner sees the same standard whether a question came from a mock or a past paper.
#   ADAPTED, NOT COPIED. Three things differ in PYQ and are stated here, not inherited:
#     • There is NO registry and NO figural_manifest. Nothing recorded what a source
#       figure was SUPPOSED to be, so there is nothing to cross-check a reading against.
#     • Figures are transcribed ONCE per paper at P2a (§13A) into
#       pyq_figural_vision.json. The router therefore runs AFTER that transcription and
#       is fed by it (§6A-2b).
#     • A paper may contain VOID_ITEM figures — untranscribable ones, for which §13A-5
#       already forbids publishing any answer. §6A-2b makes the matching figure rule
#       explicit.
#   The router is EXAM-AGNOSTIC: it names no exam and no subject. It emits a
#   REQUIREMENT; which renderer satisfies it is bound framework-side in
#   explain_engine.REPRESENTATION_RENDERERS (v2.19, GAP-2026-08-28-CATEGORY-C-
#   ORPHAN-CONFIG-READ — formerly specified as a section_rules CATEGORY C read that
#   no producer ever emitted). The binding is identical for every exam; WHETHER any
#   question uses a renderer is decided per question by §6A-1, so an exam whose
#   router never reaches a visual verdict behaves EXACTLY as before and deploying
#   the router cannot regress it.

## S6A-1 — PROSE IS THE DEFAULT. A VISUAL IS EARNED, NEVER ISSUED.
  The load-bearing rule; read it before the table. The default verdict is PROSE, and a
  richer representation must EARN its place on the same two-part test §14 applies to
  SPEED HACK ("omit, never fake"):
    1. DECISIVE — the answer turns on a relationship prose states less clearly than the
       representation would (connectivity, spatial arrangement, occupancy, a computed
       chain, a data shape).
    2. NOT REDUNDANT — it carries information the surrounding sentences do not. Re-drawing
       what the stem already shows, or illustrating a recall fact, fails this half.
  BOTH must pass, else PROSE. A recall question takes PROSE and stops.
  PYQ SHARPENS THE REDUNDANCY HALF. The source figure is a REAL exam figure and it sits
  in the question region above the explanation, byte-identical (§12). Re-drawing it is
  redundant BY CONSTRUCTION. A generated figure earns its place here only by showing
  something the exam's own figure does NOT: the transformation it undergoes, the
  electron occupancy it implies, the comparison that decides between options.
  MINIMUM SUFFICIENT REPRESENTATION: where two representations both pass, take the
  simpler. Never draw a mechanism where a transformation arrow suffices.

## S6A-1b — STRUCTURE-ANSWER PRESUMPTION (v2.13)
  §6A-1's default is inverted for ONE narrow shape: the question whose verified
  ANSWER IS a structure — the CA option is itself a drawn figure
  (IMAGE-AS-OPTIONS, §13-1), or the question is C-STRUCTURAL and the answer is
  the identity of a transformed arrangement. For that shape the decisive
  relationship is BY CONSTRUCTION one that prose states less clearly than the
  representation, so the two-part test is PRESUMED PASSED for STRUCTURE_GRAPH.
  Routing such a question to PROSE anyway is permitted ONLY with a RECORDED
  justification (in progress state, next to the verdict) stating where the
  DEDUCTION prose itself carries each decisive feature — the change, the
  position at which it happens, and the resulting arrangement. A terminal
  identification that only POINTS ("the structure drawn in Option N") carries
  none of them and never satisfies this.
  VOID_ITEM WINS (§6A-2b): a VOID_ITEM question never generates a figure — no
  answer is published for it at all (§13A-5) — so this presumption is void for
  a VOID_ITEM by construction; its verdict stays PROSE with reason VOID_ITEM.
  REFERENCE INCIDENT (mock path, same engine and same router): a structure-heavy
  paper shipped 46 question-region images and 2 explanation figures, its
  structure-decisive DEDUCTIONs ending at the pointer sentence. On a REAL past
  paper the stakes are higher still: the exam body drew the answer, and an
  explanation that only points at it teaches nothing the paper did not already
  show. The presumption is still not a quota: a question whose deciding feature
  is fully stated in one prose clause records that justification and ships
  prose legitimately.


## S6A-1b-ii — COUNT-OF-VISUAL-OBJECTS PRESUMPTION (v2.15)
  When the ANSWER IS A COUNT OF VISUAL OBJECTS (resonance contributors, isomers, fac/mer,
  bridging bonds, orbital occupancies, competing products, distinct sites) §6A-1b
  applies AND the figure must SHOW THE ENUMERATED OBJECTS, not the starting structure
  alone. PROSE stays legal with a recorded justification.

## S6A-1c — ALIGNMENT: THE REPRESENTATION MUST SHOW THE DECIDING RELATION (v2.14)
  §6A-1 tests DECISIVE and NOT REDUNDANT. Both can pass while the learner never
  SEES what the answer turned on: the product drawn, the selectivity-deciding
  intermediate in prose; a terminal/bridging count with no picture of which is
  which; a projection argued without saying which carbon is in front. So a
  THIRD question is asked of every verdict, PROSE included, once the DEDUCTION
  is drafted: does the representation — or the prose — make the ANSWER-DECIDING
  relation visible? A present-but-misaligned representation fails
  (REP_PRESENT_BUT_NOT_ALIGNED) and is re-routed, never captioned over.
  WHEN THE DECISION IS SPATIAL, PROSE NEEDS AN EXPLICIT INVENTORY. If the answer
  turns on arrangement in space, occupancy, topology (which elements bridge) or
  handedness, PROSE is valid ONLY when the DEDUCTION carries what a drawing would:
    • a projection → the viewing direction and the front/rear identity stated
      before any staggered/eclipsed or anti/gauche claim is made;
    • an occupancy-decided answer → the occupancy stated level by level ("the
      lower set holds six, the upper set none"), not only the conclusion;
    • a topology count → the elements listed by role ("four bridge, six are
      terminal: two on each outer centre, one on each inner one");
    • a handedness-decided count → each geometric form named and tested for a
      mirror plane separately, the chiral one stated as a pair.
  Absent that inventory the verdict is a visual one the router under-fired on,
  and it is re-routed (§6A-2). Not a quota: a deciding relation fully stated in
  one prose clause keeps PROSE and records that it did.

## S6A-2 — The requirement vocabulary (what the router emits)
  | Requirement          | Emit when the answer turns on …                        |
  |----------------------|--------------------------------------------------------|
  | PROSE                | a fact, a definition, or a short causal chain (DEFAULT) |
  | EQUATION             | a calculation — governing relation, substitution, value |
  | TABLE                | independent criteria tested across several candidates   |
  | STRUCTURE_GRAPH      | connectivity / stereochemistry / a transformation       |
  | LEVEL_DIAGRAM        | occupancy, energy ordering, or state splitting          |
  | DATA_PLOT            | the shape of a graph, spectrum, or titration curve      |
  | CONFORMER            | (v2.14) HOW atoms are arranged at a given rotation — a projection (Newman / sawhorse / chair), which a constitution renderer cannot express; visual, requires its figure (run-report F3) |
  EQUATION is satisfied by §11's ⟦MATH:…⟧ regions and is ALWAYS available — it needs no
  renderer and no configuration; §11 already governs its spelling and is unchanged by
  this version. TABLE is native docx. The last four (v2.19 — CONFORMER, added v2.14,
  made the pre-v2.19 "three" stale) need a renderer bound in
  explain_engine.REPRESENTATION_RENDERERS (§6A-6); a library its preflight found
  unavailable degrades the requirement (§6A-4).

## S6A-2b — PYQ ORDERING AND THE VOID_ITEM PROHIBITION (v2.7, PYQ-only)
  ORDER: for a figural question the router runs AFTER the §13A transcription is read,
  never before. Routing from stem text alone would decide what to draw without knowing
  what the exam actually drew — RE-11's failure in a new costume.
  VOID_ITEM: if the question's §13A record is VOID_ITEM (MISSING / EMPTY / THIN /
  STALE), the router MUST NOT emit STRUCTURE_GRAPH, LEVEL_DIAGRAM or DATA_PLOT for it.
  §13A-5 already forbids publishing an ANSWER for such a question; generating a figure
  from an untranscribable source would manufacture content from nothing — exactly what
  RE-11 forbids — and would look authoritative while resting on no observation. Record
  the verdict as PROSE with reason VOID_ITEM, and let §R12 carry it as it already does.

## S6A-3 — Record the verdict on every question
  Recorded per question in progress state as representation_verdict, with the two-part
  test's outcome, so the choice is auditable rather than implicit: a paper whose every
  question demanded a figure, or whose every question refused one, becomes visible as a
  pattern instead of discovered by reading. §R3 states the distribution. (v2.13) The
  verdict is ALSO passed into the ExplanationBlock (engine v2.6
  representation_verdict), which enforces verdict↔emission coherence at construction:
  a STRUCTURE_GRAPH / LEVEL_DIAGRAM / DATA_PLOT verdict with zero figures raises;
  after a §6A-4 degrade the block carries the DEGRADED requirement, never the
  original.


## S6A-3b — THE DISTRIBUTION IS A TRIPWIRE, AS §14-5 IS FOR SPEED HACK (v2.14)
  The reference paper routed ZERO TABLE on four candidate-comparison questions
  and ZERO LEVEL_DIAGRAM on three occupancy-decided ones, renderer live: each
  verdict defensible, the aggregate an under-firing router. So, per batch,
  before §18: if every candidate-comparison or every occupancy-/arrangement-
  decided question routed PROSE, re-run §6A-1 / §6A-1c on each. Survivors ship
  as they stood; failures are re-routed. No target rate; a paper with no such
  questions trips nothing.

## S6A-4 — Degrade LOUDLY, never silently, and never HALT
  If a required renderer is unavailable, or a rendered artefact fails its validation
  gate (§6A-5), step DOWN one requirement — toward EQUATION, then PROSE — and ship the
  explanation anyway. A missing renderer must never halt a paper mid-run. (v2.13) The
  RECORDED verdict — in progress state AND on the block — becomes the DEGRADED
  requirement, with the reason, never the original: engine v2.6 raises on a visual
  verdict with no figure, so an un-updated verdict cannot even construct. But the
  degrade is DISCLOSED: recorded in progress state, listed in §R3, named in the delivery
  footer. Silent degradation is the worse failure — it makes quality vary invisibly
  between runs of the same spec, which is undiagnosable from the artefact.

## S6A-5 — A rendered artefact must be PROVED, not trusted
  Every generated figure carries a validation record; one that fails its gate is never
  shipped (it degrades per §6A-4). The gate is renderer-specific and bound with the
  renderer in explain_engine.REPRESENTATION_RENDERERS (v2.19), but the CONTRACT is fixed: re-derive the artefact from the rendered output
  and compare it against what was intended — do not merely inspect it. A structural
  renderer re-parses the drawn structure and compares a CANONICAL identifier; molecular
  formula alone is insufficient, since two different answers commonly share one formula
  and a formula check would pass a swapped structure. Renderers must be DETERMINISTIC:
  the same question re-rendered must produce identical bytes.
  NOTE THE ASYMMETRY WITH §13-3. The source figure has no manifest to check against —
  that is why §13-3 says VIEW and derive, with no cross-check. This gate is the
  opposite case and is fully checkable: WE generated the artefact, so we know exactly
  what was intended and can prove the output matches it. The absence of a source
  cross-check is no reason to relax an output gate that is available.
  WHAT THE GATE DOES NOT PROVE: it proves the drawn artefact matches what was requested.
  It cannot prove the request was right; that stays with derive-twice (§7).

## S6A-6 — Renderer execution contract
  WHO RENDERS: the executing session, at solve time. No renderer engine file — rendering
  is spec-directed session work (v2.21: figural_core and corpus_io, Step 7's engines,
  are routed here as the palette owner and structure renderer), and the ENGINE's job
  stays confined to emission mechanics, the §6A-5 record check at construction, and the
  figure-landing check at verify time (explain_engine v2.3, shared with TestExplain).
  DECLARED WHERE (v2.19 — GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ): the
  requirement → library → §6A-5 identifier binding is FRAMEWORK-OWNED and lives in
  explain_engine.REPRESENTATION_RENDERERS (STRUCTURE_GRAPH : rdkit — canonical SMILES
  round-trip; LEVEL_DIAGRAM / DATA_PLOT / CONFORMER : matplotlib). It is NOT an exam
  property and is NOT read from section_rules: it states what this framework can draw
  and how each artefact is proved, identical for every exam; WHETHER any question uses
  a renderer is decided per question by §6A-1, which no declaration can override.
  HISTORY: v2.7–v2.18 specified this block as section_rules CATEGORY C
  representation_renderers. No producer ever emitted that key — not
  analyse_engine.write_section_rules(), not Framework_MockTestAnalyse §14, not any
  engine — so EVERY exam took the absent-path and every visual verdict degraded per
  §6A-4, permanently. A per-exam override is deliberately NOT built (operator
  decision D1); if ever needed, an optional exam_config key layers on with
  precedence exam_config → constant.
  DEPENDENCIES ARE PREFLIGHT WORK. P0 import-tests the library of every
  REPRESENTATION_RENDERERS requirement — and, v2.21, `import figural_core, corpus_io`,
  recording explain_engine.colour_contract()['available'] (S6A-6 COLOUR) — (Step 0 already installs the full set; pip only
  on import failure) and RECORDS the result in the P7 dashboard. An unavailable
  library does not halt: the affected requirement degrades for the WHOLE run,
  disclosed up front as a plain note, so quality never varies silently between
  batches. After v2.19 there is no "block absent" state — the only remaining degrade
  cause is a genuinely unavailable library.
  MECHANICS: RepresentationFigure(path, width_in, validation, after_step) and
  ExplanationBlock(..., figures=[...]); validate() raises on any §6A-5 breach. Figure
  paragraphs carry NO text (engine-enforced) — every label the reader needs is drawn
  INSIDE the figure, and the adjacent DEDUCTION sentence states what it decides. Width
  0.5..7.0 in; ~6.0 for a full-column scheme, ~4.0 for a single panel.
  FAILURE PATHS, all loud: failed render or failed §6A-5 comparison → drop the figure,
  degrade, record it; declared-but-unrendered at verify time → BLOCKING figure-landing
  FAIL. No path ships an unproved image, and no path hides a skipped one.

  COLOUR (v2.21 — GAP-2026-08-30-EXPLAIN-COLOUR-BINDING; shared rule, mirrored in
  MockTestExplain S6A-6). An explanation figure draws with EXACTLY the constants a Step 7
  question figure draws with — figural_core is the palette owner and is routed to
  this trigger together with corpus_io (routes.json v2026.08.30.1). No library
  default palette is ever used. Per requirement (the CONSTANT
  explain_engine.REPRESENTATION_RENDERERS[...]['colour'] is the authority;
  explain_engine.colour_contract() returns the live values):
      STRUCTURE_GRAPH : draw = explain_engine.structure_draw(canonical_smiles,
                        highlight_bonds=[...] / highlight_atoms=[...]) — the ONE
                        call for structures: it loads figural_core FIRST and then
                        runs corpus_io.structure_draw_fn (which reads the palette
                        from the already-loaded module and never imports it, so a
                        process that imported corpus_io alone would draw black-
                        and-white with only draw.palette_note to say so); atoms from
                        figural_core.ATOM_PALETTE (O #C25604, N #0072B2, halogens
                        #158663, all else black), the DECISIVE site the adjacent
                        DEDUCTION sentence names accented in
                        figural_core.HIGHLIGHT_COLOUR; rasterise into a matplotlib axes
                        (ax.axis('off')) and save at explain_engine.RENDER_DPI
                        (300) for width_in. The §6A-5 identifier is draw.canonical;
                        a non-None draw.palette_note is a §6A-4 degrade to RECORD.
      LEVEL_DIAGRAM / DATA_PLOT / CONFORMER : series and accent ink from
                        fc.OKABE_ITO[:4] + black, at most fc.SERIES_CHROMATIC_CAP
                        chromatic series, each with its own linestyle/marker
                        (fc.LINESTYLES / fc.MARKERS); every coloured LABEL through
                        fc.text_ink(hue); every FILL through fc.fill_style(k);
                        continuous data viridis only; opaque white background;
                        300 dpi at width_in.
  WHAT DOES NOT TRANSFER FROM STEP 7: an explanation EXPLAINS the answer, so the
  Step-7 answer-leak rules (Q7b.13 colour-as-content monochrome, Q7b.14 option-set
  element uniformity, S10-7 Q5 no-chrome) do NOT apply here — a solution may show
  the colour it is explaining, and labels inside the figure remain REQUIRED by the
  MECHANICS above. Determinism (§6A-5) is unchanged: the palette is a constant, so
  the bytes are the same on every machine. figural_core.audit_figure() is NOT run on
  explanation figures (they carry no FigureSpec); the §6A-5 record is their proof.
  DEGRADE: if `import figural_core` or `import corpus_io` fails at P0 (impossible
  on a verified clone; recorded anyway), figures render black-and-white with the
  reason on the dashboard — never a library default, never a halt.


# ════════════════════════════════════════════════════════════════════════
# §7 — DERIVATION PROTOCOL (derive-twice, never guess)
# ════════════════════════════════════════════════════════════════════════
#   Same derive-twice contract as the mock pipeline. DERIVATION-CONFIDENCE for
#   disagreements. NAT portal grading value via derive_nat_grading().

## S7-0a — CAPTURE THE CONDITIONS BEFORE APPLYING ANY REMEMBERED RESULT (v2.10)
  A named reaction, standard formula or remembered result is a CONDITIONAL claim. Before
  applying one, read back from the stem every condition it depends on, and check the stem
  actually supplies them. NEVER apply a remembered name while ignoring its conditions —
  that is how a confident, fluent, WRONG answer gets produced, because the recalled name
  is right and only the conditions differ.
  CAPTURE every qualifier the stem attaches to the situation. WHICH qualifiers exist is
  DOMAIN-DEPENDENT and is read from the exam's own material (section_rules CATEGORY C
  cues + the subtopic), never assumed from this list. TYPICAL, NOT EXHAUSTIVE, and NOT a
  requirement that any of these appear: the ORDER in which things are applied · what is
  held constant · the stated regime or range of validity · the environment or medium ·
  any explicitly given rate, level, setting or state · the post-process or clean-up step.
  A paper in a domain where none of these apply simply captures nothing here and the rule
  costs it nothing.
  REFERENCE CASE (one domain, illustrating the shape — the failure is universal): an
  ozonolysis question turns entirely on the WORK-UP. The same
  substrate and the same ozone give an aldehyde under a reductive work-up and a carboxylic
  acid under an oxidative one. A solver who recalls "ozonolysis cleaves the double bond"
  and stops has recalled a true statement and will still answer wrongly half the time.
  A condition the stem supplies but the DEDUCTION never uses is a warning sign: examiners
  supply conditions because they DISCRIMINATE. If a stated condition changed nothing in
  the reasoning, re-read the question before proceeding.
  CROSS-STEP: §9's `wrong_condition` names this failure in a DISTRACTOR. This rule governs
  the SOLVER. They are different obligations and neither substitutes for the other.

## S7-0b — ASSUMPTION LEDGER (v2.10)
  Record every approximation the derivation leans on, at the moment it is used. WHICH
  approximations are conventional is DOMAIN- AND LEVEL-DEPENDENT; the exam's own material
  establishes them. ILLUSTRATIVE ONLY, across domains, and no item here is expected of any
  particular paper: an idealised model substituted for the real one · a small quantity
  neglected · a limiting or standard condition assumed · a second-order effect ignored ·
  a value taken at its reference state.
  THREE CASES, and only the third reaches the reader:
    1. The STEM supplies the assumption -> use it, no comment needed.
    2. It is the settled convention at this exam's level and does NOT change the answer
       -> use it silently.
    3. It MATERIALLY affects the answer -> STATE IT in the explanation, in the step that
       relies on it. A number that would differ under a different, equally defensible
       assumption is not a fact; presenting it as one hides the choice from the learner.
  An assumption may never CONTRADICT something the stem supplies. If it must, the stem
  wins and the conflict is an ambiguity signal (§17).

## S7-0c — ENUMERATION BEFORE FORMULA (v2.13)
  A counting question is never OPENED from a closed-form ceiling. The order is
  fixed: 1. INVENTORY the generating elements the count runs over; 2. CLASSIFY
  each element; 3. TEST INDEPENDENCE — whether every element genuinely varies
  freely of the others; 4. GENERATE the possibilities under the constraints
  actually present; 5. DE-DUPLICATE under every equivalence that applies
  (symmetry, relabelling, indistinguishability); 6. COUNT. A closed-form
  (a k^n or factorial shape) is legitimate ONLY AFTER step 3 verified the
  independence it assumes — and the DEDUCTION then shows the inventory and the
  de-duplication, never just the formula (the C-STRUCTURAL enumeration shape,
  §6-1, is this rule's rendered form).
  WHY. A ceiling formula applied first FEELS like a derivation and is the single
  most common wrong path in enumeration: it silently asserts an independence
  that step 3 would have refuted. ILLUSTRATIVE, one domain showing the
  universal shape: stereoisomer counting — the 2-to-the-n ceiling holds only
  for independent stereogenic elements, and dependent elements, internal
  compensation and symmetry each defeat it; the same failure shape appears in
  arrangement counting under symmetry and in state counting over
  indistinguishable members. The rule is the ORDER, not the domain.

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

## S7-5 — NUMERICAL VERIFICATION (every quantitative answer, v2.10)
  Derive-twice (§7-1) catches a DIFFERENT-ANSWER error. It does NOT catch a CONSISTENT
  error: both routes can share one unit slip, one log base, one power of ten. These checks
  are orthogonal to it and are run on the final value before the block is written.
  EACH CHECK IS CONDITIONAL ON APPLICABILITY. A check whose subject the question does not
  contain is NOT APPLICABLE and is not a failure — a pure-arithmetic item has no units to
  verify, a word problem no conversion. Never manufacture a check to satisfy the list, and
  never treat a non-applicable check as a defect. The parenthetical examples span domains
  and are ILLUSTRATIVE ONLY.
    [ ] UNITS (if the answer carries one) — the result carries the unit the question asked
        for, and the working is dimensionally consistent throughout, not merely at the end.
    [ ] CONVERSIONS (if any quantity is expressed in more than one unit) — every quantity
        converted where the relation demands it, including any ABSOLUTE-SCALE requirement
        the relation imposes on a scaled quantity.
    [ ] MAGNITUDE — the order of magnitude is sane for what the quantity IS. A bounded
        quantity outside its bounds, or a length in the wrong power of ten, is an
        arithmetic slip, not a result.
    [ ] LOG / EXPONENT BASE (if a logarithm or exponential appears) — the base matches the
        constant used alongside it; a mismatched base silently rescales the whole answer.
    [ ] SIGN / DIRECTION (if the quantity is signed or directional) — the sign matches the
        direction the question defines (gain vs loss, forward vs reverse, in vs out).
    [ ] DEFINING RATIO (if the domain fixes one) — any conserved or defining ratio comes
        from the relation that DEFINES it, and that relation was balanced, normalised or
        otherwise completed BEFORE it was used.
    [ ] PRECISION — the answer is rounded exactly as the question asked, and no further.
        Rounding is applied ONCE, at the end, never to an intermediate that is then reused.
  A check that FAILS sends the question back to §7-1, never to a patched number.

## S7-6 — DECISIVE-CLAIM CONSISTENCY (every question, v2.13)
  Derive-twice (§7-1) compares final ANSWERS; the §7-5 checks audit the final
  VALUE. Neither reads the reasoning. This check does: before any prose is
  written, LIST the decisive intermediate claims the DEDUCTION will assert —
  the claims the answer actually turns on — and check them against each other:
    [ ] LOGICAL — no claim asserts what another denies.
    [ ] COUNT / NUMERIC — an element one claim excludes is not counted by a
        later one; totals equal their stated parts.
    [ ] SIGN / DIRECTION — a direction argued qualitatively is the direction
        the arithmetic then applies.
    [ ] CONSERVATION / BALANCE — whatever the domain conserves is conserved
        across the chain, not merely in the final line.
    [ ] IDENTITY — the object one claim establishes is the object later claims
        use, not a silently substituted variant.
  AN EXPLANATION WHOSE DECISIVE CLAIMS CANNOT ALL BE TRUE IS INVALID EVEN WHEN
  ITS FINAL ANSWER MATCHES the derived one: answer agreement can HIDE invalid
  reasoning, and a learner re-walking the chain inherits the contradiction — on
  a REAL past paper it also misstates the reasoning the exam actually tested.
  ILLUSTRATIVE, one domain showing the shape: "this centre is not an
  independent stereogenic element" followed by a count that treats it as one —
  the keyed answer can still come out right, and the explanation is still
  wrong. A failed check returns to §7-1 — the SOLVER re-derives; the
  contradiction is never patched in the prose (patching the sentence that
  exposed it leaves the reasoning it exposed).

## S7-7 — TRANSFER-SAFETY PROTOCOL (every AXIOM and every SPEED HACK, v2.14)
  An explanation is read twice: to check THIS answer, and later, on a
  DIFFERENT question, as a remembered rule. §7-1 to §7-6 prove the first
  reading; nothing proved the second. A statement can be correct for the item
  and a FALSE GENERAL RULE — true for the stem's substrate, false for its
  nearest neighbour — and every answer-level gate is blind to it because the
  answer was right. This protocol runs BEFORE AXIOM / SPEED HACK prose is
  written and its result is RECORDED, as §7-6 and §14-5 record theirs.
  FOR EVERY TRANSFERABLE CLAIM — each AXIOM sentence, each SPEED HACK, and any
  WHY WRONG / COMMON PITFALLS line phrased as a general rule:
    1. STATE THE INTENDED SCOPE. What class of situations is this claim meant to
       cover? A claim with no statable scope is not yet a claim (GEN_SCOPE_UNDEFINED).
    2. TYPE IT (§8-2): SCIENTIFIC_GENERAL_RULE · MODEL_DEPENDENT_RULE ·
       EXAM_CONVENTION · QUESTION_SPECIFIC_INFERENCE · OPTION_SET_SHORTCUT.
    3. NAME THE NEAREST LEGITIMATE NEIGHBOUR — the closest member of the same
       apparent class, AT THE TARGET EXAM'S LEVEL, that a learner would meet next.
       v2.15 — THE LOOKUP IS MECHANICAL. Each curated rule carries **Triggers:**
       (§24-1b). A trigger firing on the claim's sentence makes that rule's canonical
       counterexamples THE neighbour; the record cites neighbour_source
       CURATED:<rule-code>, and the engine refuses an AXIOM / SPEED HACK that matches a
       family it did not cite (GEN_CANONICAL_EXCEPTION_MISSED). GENERATED is admissible
       ONLY where no trigger fires. P1 builds the table: explain_engine.
       triggers_from_learnings([all parsed files]) → EngineConfig(learnings_triggers=…).
    4. TEST the claim on that neighbour. Still true → SAFE.
    5. FALSE on the neighbour → REPAIR BY RETURNING TO THE MECHANISM, never by
       hedging: name the actual effect, class or condition that makes the claim
       true where it is true (NARROWED); or, if the fact is really about THIS
       item only, move it into the DEDUCTION (MOVED_TO_DEDUCTION); or, for a
       SPEED HACK, omit it (OMITTED, §14-1 part 3). Inserting "usually" is NOT a
       repair (it satisfies §8-0b and still teaches nothing about WHEN); listing
       every exception is NOT a repair either (§8-2 — the AXIOM does not get
       longer as the fix).
  THE RECORD (progress state + engine v2.7 `transfer_record`, shape-validated):
  one entry per claim {section, claim, epistemic_type, scope, neighbour_tested,
  outcome}; an AXIOM without an AXIOM entry or a SPEED HACK without a SPEED_HACK
  entry cannot construct; no QUESTION_SPECIFIC in AXIOM, no OPTION_SET_SHORTCUT
  outside SPEED HACK. The engine proves the protocol RAN; judging the neighbour
  stays with discipline, as §6A-5 proves the artefact and not the request.
  ILLUSTRATIVE, one domain, the PROCEDURE is the rule: AXIOM "an electron-
  withdrawing substituent directs meta"; neighbour at this level, chlorobenzene
  (withdrawing, ortho/para); claim fails; repair by mechanism — "a substituent
  that withdraws by resonance destabilises the ortho and para intermediates
  more than the meta one, so it directs meta" — true for item and neighbour,
  the halogen case excluded for a stated reason. Same shape in the reference
  paper: "one carbon richer" (non-methyl Grignards), "stable carbonylate = 18
  electrons" (stable 16e/17e), "identical halves always give a meso form".
  CROSS-STEP: §9's `overgeneralised_rule` names this failure in a DISTRACTOR;
  this rule governs the SOLVER'S OWN AXIOM (the §7-0a / `wrong_condition` pair).
  TRIPWIRE (v2.15): explain_engine.transfer_tripwire fires when ≥20 AXIOM claims carry
  0 NARROWED / MOVED_TO_DEDUCTION; it obliges a recorded SECOND PASS over every AXIOM
  before §18 (§R3).

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
from blueprint_core import difficulty_score, band_for_score   # Cluster E2 — PURE, no I/O

obs = {                                   # v2.18 — the observation record is KEPT (S7A-4)
    'question_class'        : <§6 class facet(s)>,
    'deduction_steps'       : <§8-3 step count>,
    'axiom_concepts'        : <§8-2 principle count>,
    'speed_hack_exists'     : <§14 gate verdict>,
    'derivation_confidence' : 'flagged' if methods initially disagreed else 'full',
    'is_negative'           : <§10a scan result>,
    'qtype'                 : <'mcq' | 'msq' | 'nat'>,
    'subtopic_id'           : <§6 subtopic_id — the same value q_to_classification carries>,
    'stem_snippet'          : <first 120 characters of the stem, plain text>,
}
score = difficulty_score(obs['question_class'], obs['deduction_steps'], obs['axiom_concepts'],
                         obs['speed_hack_exists'], obs['derivation_confidence'],
                         obs['is_negative'], obs['qtype'])          # int 0..12
label = band_for_score(score, <exam_config.difficulty_labels, default Easy/Medium/Hard>)
```

  `difficulty_score` / `band_for_score` are pure functions (`assess_difficulty` is
  exactly their composition): identical observations always return the identical
  score and label, on every run and every model instance. The SCORE is recorded
  beside the label (v2.18 — GAP-2026-08-27-DIFFICULTY-PROFILE): it is what the
  exam's difficulty profile (S7A-6) pools across papers, and it lets a later band-
  edge change be applied without re-explaining a single paper. PYQ-1 MUST NOT override,
  round, smooth, or "balance" its output — there is no target distribution here.
  A paper legitimately skewed toward recall SHOULD come out skewed.

  `band_for_score` returns `None` when `difficulty_labels` is not an exactly-3-label
  list (the same contract as `assess_difficulty`). On `None`: omit that question
  from `q_to_difficulty` and `q_to_difficulty_score` entirely — never write a
  `None` or a guessed value — and note it once in §R11. PYQ-4 then resolves those
  questions on its own lower tiers. The observation record (`difficulty_obs`) is
  still written for every question: the profile is DORMANT for such an exam, but
  the evidence is kept.

## S7A-4 — Recording

  After the batch's questions are assessed, write into
  `pyq_explain_progress.json` alongside `q_to_classification`:

```json
{
  "_meta": { "exam_code": "...", "phase": "pyq_explain", "...": "..." },
  "q_to_classification": { "1": { "...": "..." } },
  "options_by_q": { "1": 4, "41": 0 },
  "qtype": { "1": "mcq", "31": "msq", "41": "nat" },

  "q_to_difficulty": { "1": "Easy", "42": "Medium", "54": "Hard" },

  "q_to_difficulty_score": { "1": 1, "42": 4, "54": 7 },
  "difficulty_unscored": { "22": "Row-file defect: options 1 and 2 bind the same image",
                           "35": "VOID_ITEM: figure not transcribable to publication confidence" },
  "difficulty_obs": { "1": { "question_class": ["C-FACTUAL"], "deduction_steps": 0,
                             "axiom_concepts": 1, "speed_hack_exists": false,
                             "derivation_confidence": "full", "is_negative": false,
                             "qtype": "mcq", "subtopic_id": "…", "stem_snippet": "…" } }
}
```

  * `q_to_difficulty_score` and `difficulty_obs` (v2.18) are written by the SAME
    batch write as `q_to_difficulty`, so the three maps can never disagree on
    coverage. `difficulty_obs` is the exact input S7A-3 scored — the profile
    writer (S7A-6) re-scores it with the engine, so a hand-edited score can never
    enter the profile.

  * `difficulty_unscored` (v2.20 — GAP-2026-08-29-PROFILE-UNSCORED-QUESTIONS): one
    entry {q: reason} for EVERY position of the paper that has NO `difficulty_obs`
    record — a VOID_ITEM figure (§13A-5), a Row-file defect (§R7), an exam-body
    cancelled or defective question, or any other question with no derived answer.
    The reason is the same sentence §R11 prints for the omission. Written in the
    same batch write; a position may appear in `difficulty_obs` OR
    `difficulty_unscored`, never both, and every `qtype` position is in exactly
    one of them by the final batch. S7A-6 stores these under the profile paper's
    `unscored` map so Blueprint can list them; they never enter the arithmetic.

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

## S7A-6 — The exam's difficulty profile (v2.18 — GAP-2026-08-27-DIFFICULTY-PROFILE)

  PYQ-1 is the SINGLE PRODUCER of `[ExamCode]_difficulty_profile.json` — the
  measured difficulty mix of this exam, pooled over its explained papers, from which
  MockBlueprint derives its DEFAULT Easy:Medium:Hard split per section (Blueprint
  §S7-0) and Step 7 / ScopedBlueprint read per-subtopic calibration examples. It
  replaced the silent 25:25:50 Blueprint default and the retired keyword scorer
  (Step 5 E-9). One file per exam; written ONLY through `bc.dp_add_paper`; every
  recommendation is recomputed by the reader from the raw records, never stored
  as a decision. The engine contract (window of the latest 3 sittings, 60-day
  cycle clustering, equal weight per sitting, exact-fraction rounding) is
  blueprint_core Cluster DP — never re-tuned inline.

  WHEN: on the FINAL batch only (100% coverage), inside S19-1 before the checklist.
  INPUT: the project's current `[ExamCode]_difficulty_profile.json` if present
         (the operator keeps ONE copy in the project Files section and replaces it
         after every PYQExplain run, before the next one); absent → a new profile
         is started. Re-explaining a paper REPLACES its record (idempotent), so a
         paper dropped by a missed upload is recovered by re-running it.
  POSITIONS vs SCORED (v2.20 — GAP-2026-08-29-PROFILE-UNSCORED-QUESTIONS): the
         paper's POSITIONS are the handoff `qtype` map keys (every question the
         paper has — S19-1 check 7 proves the map complete); the SCORED questions
         are `difficulty_obs`. The pattern test (positions == 1..total_questions)
         runs on POSITIONS. A position without an observation is passed as
         UNSCORED with its `difficulty_unscored` reason and is recorded, listed,
         and left out of the mix — it NEVER excludes the paper. A profile
         written before v2.20 (no `q_scored`/`unscored` keys) reads unchanged.
  WRITE: `/mnt/user-data/outputs/[ExamCode]_difficulty_profile.json` — a deliverable
         alongside the explanation docx and the handoff json (S19-2).

```python
import os, json, datetime as _dt
import blueprint_core as bc
_pf_name = f'{EXAM}_difficulty_profile.json'
_pf_in   = f'/mnt/project/{_pf_name}'
_profile = None
if os.path.exists(_pf_in):
    _profile = json.load(open(_pf_in, encoding='utf-8'))       # bc.dp_add_paper validates it
_ec  = json.load(open(f'/mnt/project/{EXAM}_exam_config.json', encoding='utf-8'))
_ec  = {'exam_code': EXAM, 'total_questions': _ec.get('total_questions'),
        'sections': _ec.get('sections'), 'cycle_gap_days': _ec.get('cycle_gap_days'),
        'difficulty_labels': _ec.get('difficulty_labels') or ['Easy', 'Medium', 'Hard']}
_h   = json.load(open('/home/claude/pyq_explain_progress.json', encoding='utf-8'))
_obs = _h.get('difficulty_obs') or {}
if not _obs:
    raise SystemExit('HARD STOP (S7A-6): difficulty_obs missing from the handoff — S7A-4 did not run')
_positions = sorted(int(k) for k in (_h.get('qtype') or {}))     # v2.20: the paper's positions
if not _positions:
    raise SystemExit('HARD STOP (S7A-6): qtype map missing from the handoff — S7A-4 did not run')
_unscored_reasons = _h.get('difficulty_unscored') or {}            # v2.20: {q: reason}, may be empty
if len(_ec['difficulty_labels']) != 3:
    # DORMANT exam (non-3-band vocabulary): the profile contract is 3-band; nothing is written,
    # nothing is delivered, §R13 says DORMANT. The observations stay in the handoff json.
    PROFILE_STATUS, PROFILE_REASON, PROFILE_SUMMARY = 'dormant', 'difficulty vocabulary is not 3-band', {}
else:
    try:
        _profile, PROFILE_STATUS, PROFILE_REASON = bc.dp_add_paper(
            _profile, source_file=os.path.basename(CLEAN_ROW_FILE), exam_config=_ec, questions=_obs,
            paper_positions=_positions, unscored_reasons=_unscored_reasons,
            written_by='PYQExplain v2.20 / blueprint_core Cluster DP',
            now=_dt.datetime.now(_dt.timezone.utc).isoformat(timespec='seconds'))
    except bc.DPError as _e:
        raise SystemExit(f'HARD STOP (S7A-6): {_e}')       # a contract violation, never a silent skip
    json.dump(_profile, open(f'/mnt/user-data/outputs/{_pf_name}', 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    PROFILE_SUMMARY = _profile.get('summary_at_write', {})
```

  * `PROFILE_STATUS == 'excluded'` is NOT a stop: the paper's POSITIONS do not
    match the CURRENT exam_config (pattern changed), or no question at all carries a
    derived answer. The profile is still written (the paper is recorded under
    `excluded_papers` with the reason) and §R13 says so. A pattern change is a fact
    about the exam, not a defect. A question WITHOUT a derived answer on a paper
    whose positions DO match is never a reason to exclude (v2.20): it is stored under
    the paper's `unscored` map and the paper is `added`.
  * A DORMANT exam (non-3-band `difficulty_labels`) writes and delivers NO profile
    (`PROFILE_STATUS == 'dormant'`); S19-1 check 8 and the S19-2 deliverable are
    conditional on that status. The observations stay in the handoff json.
  * The bare filename of the attached Row file is the paper identity
    (`[ExamCode]_[DD-Mon-YYYY][_session]`); an unparsable name is the S1 HARD STOP
    already in force, so it can never reach this block.

# ════════════════════════════════════════════════════════════════════════
# §8 — SECTION QUALITY STANDARDS (highest-standard contract per section)
# ════════════════════════════════════════════════════════════════════════
#   Governing rule across ALL sections — the DENSITY FLOOR (not a length floor):
#   every line must add a NEW number, fact, or reason; NO sentence may restate
#   another. Brevity is allowed only when the line is dense; a line carrying none
#   of its required facts fails the content floor (producer discipline enforces the
#   no-restatement rule code cannot).

## S8-0 — TWO CONTENT DISCIPLINES THAT BIND EVERY SECTION (vv2.9)
  These govern AXIOM, DEDUCTION, SPEED HACK and WHY WRONG / COMMON PITFALLS alike.
  Both were found in a delivered chemistry paper and both had NO rule against them.

### S8-0a — SUPPORTED VALUES ONLY (no invented precision)
  EVERY number an explanation asserts must come from ONE of exactly three places:
    1. the STEM (or its figure/table), 2. a constant the syllabus establishes, or
    3. a value DERIVED in the explanation itself, with the derivation shown.
  A number from none of those is INVENTED and must not be written. The reference
  defect: an elimination explanation asserted the major product forms "in about 70
  percent yield" — a figure the stem never gave, the syllabus never fixes, and no step
  derived. It reads as authoritative and is unfalsifiable by the learner.
  BANNED unless supplied or derived — stated as a SHAPE, since the specific quantities
  are domain-dependent: any efficiency, yield or success rate; any ratio between competing
  outcomes; any tabulated constant; any exact measured magnitude, position or setting; any
  real-world operating figure. ILLUSTRATIVE ACROSS DOMAINS, not a checklist to match
  against: a reaction yield, a market share, a population figure, a material property, a
  historical date, a device rating. If the paper's domain has no such quantities, the rule
  simply never fires.
  THE TEST — ask of every number: "where would a student LOOK to check this?" If the
  answer is not the stem, the syllabus, or a line above it, delete it. Deleting costs
  nothing: "the terminal alkene predominates" carries the entire teaching point that
  "forms in about 70 percent yield" was pretending to add.
  QUALITATIVE CLAIMS ARE NOT EXEMPT. "Much faster", "far more stable" are comparative
  claims; state the comparison's BASIS (the structural or energetic reason), not a
  magnitude the explanation cannot support.

### S8-0b — CALIBRATED LANGUAGE (a tendency is not an impossibility)
  Real systems express TENDENCIES. Stating a tendency as an absolute teaches a false
  rule that fails the student the first time they meet the exception.
  Reserve ABSOLUTES — impossible, forbidden, never, always, cannot — for claims that
  are absolute in the subject's own terms: a conservation law, a symmetry-forbidden
  process, a definition, a mathematical impossibility.
  Use CALIBRATED terms for everything else: predominates, is favoured, is disfavoured,
  is the minor pathway, is sterically hindered, is slower under these conditions.
  The reference defect: "a bulky base CANNOT approach the shielded hydrogens" — it
  demonstrably can, it is simply disfavoured, and the whole question turns on a
  competition between two accessible pathways. Writing it as impossible destroys the
  very reasoning the question tests.
  WHY WRONG IS NOT EXEMPT — arguably it matters more there. A distractor is usually
  wrong because it is DISFAVOURED or MISAPPLIED, not because it is impossible; saying
  a plausible option "cannot" happen leaves the student unable to see why anyone chose
  it. Name the condition under which it WOULD be right, then why it is not right here.
  A GENUINE absolute must still be stated absolutely — hedging a real impossibility is
  the same failure in the other direction.

  (v2.14) NOW A GATE, NOT ADVICE. "cannot be titrated directly at all", "gives no
  turbidity at all", "always collapses into a meso form" passed every check
  because nothing read the sentence's modality. Engine v2.7 raises on an
  undeclared universal (always · never · cannot · impossible · at all ·
  regardless of · irrespective of · no matter · whatever the · universally ·
  without exception · in all cases) in AXIOM, SPEED HACK, WHY WRONG, COMMON
  PITFALLS. To KEEP one, declare the sentence in absolutes_justified with why it
  is absolute in the subject's own terms — a declaration, not a ban. Plain
  quantifiers ("only two ions", "every formula unit", "exactly 208") are NOT
  gated: measured four-fifths false positives, and declaration spam is worse
  than no gate. Per-language pattern: EngineConfig(absolute_terms_re=...).

## S8-0c — FORMULA TYPOGRAPHY (v2.15 — RE-24; engine-applied)
  Engine v2.8 normalises every student sentence at construction (normalise_formula_
  text: element subscripts, ion charges, orbital / hybrid labels, π/σ; ⟦MATH:⟧
  untouched; LOCANTS such as C2–C3 left alone) and raises FMT_UNFORMATTED_FORMULA on
  the residue. Write what it will not rewrite (η⁵-C₅H₅, ²³²Th) in Unicode or ⟦MATH:⟧.
  Per-exam switch: section_rules CATEGORY C `formula_typography: false`.

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
  THE AXIOM NEVER NAMES AN OPTION LABEL (v2.13) — binding the answer is the
  DEDUCTION last step's job (§8-3); an AXIOM naming one has leaked the conclusion
  into the principle. Enforced: ≥1 sentence, one-per-paragraph, banned-phrase
  scan, no option reference in the AXIOM (engine v2.6); "truth
  not task", "why not just what", correctness by discipline (§18 self-audit).

  EPISTEMIC TYPE AND SCOPE-IN-SENTENCE (v2.14). Every AXIOM carries one recorded
  type (§7-7): SCIENTIFIC_GENERAL_RULE — stands once scoped; MODEL_DEPENDENT_RULE —
  names its model INSIDE the sentence ("spin-only", "using the radius-ratio rule",
  "for an ideal gas"); EXAM_CONVENTION — usable, phrased so the learner can tell
  ("under standard Lucas-test conditions"); QUESTION_SPECIFIC_INFERENCE — DEDUCTION
  only; OPTION_SET_SHORTCUT — SPEED HACK only. The qualifier is part of the rule,
  not a caveat after it (the §14-3b posture).
  Which conventions the exam expects is read from the subject learnings library
  (§24) — its exam-convention classes are subject knowledge, fixed once per
  subject (v2.19, GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ: the former
  second source, section_rules CATEGORY C exam_conventions, was produced by
  nothing and is retired) — never assumed. PRESERVE THE
  EXAM'S NOTATION: an older-convention option is still the keyed option; the
  DEDUCTION teaches the cleaner form without an answer conflict.
  THE AXIOM DOES NOT GET LONGER AS THE FIX: a failed claim is repaired by a
  narrower MECHANISM, never by an appended exception list ("… usually … except").

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

  TOPIC MINIMUM-CONCEPT COMPONENTS (v2.14). Compression also teaches false rules:
  a ligand-field geometry reduced to "a strong ligand pairs the electrons"; alkyl
  activation explained as lone-pair resonance; a capacity maximum without its
  fixed-total-concentration condition. For each archetype the subject learnings
  file (§24) lists the SEMANTIC COMPONENTS a DEDUCTION must state before its
  conclusion — a minimum, not a template. §5-3 ticks every component for every
  archetype present. WHICH archetypes exist is SUBJECT DATA; this spec only
  requires that a loaded list is satisfied.

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
  (v2.14) A third requirement joins the
  two: the shortcut is TRANSFER-SAFE (§14-1 part 3) — it passed the §7-7 neighbour
  test, it is not weaker than a one-line exact method, and an option-dependent
  trick is phrased as ELIMINATION ("strike every option whose sign is negative"),
  never as a law of the subject. A hack that works only because of the options
  shown is OPTION_SET_SHORTCUT and says so in its own wording.

## S8-5 — WHY WRONG (mcq / msq) · COMMON PITFALLS (nat)
  Role: where most learning happens — the SPECIFIC error a student commits to land
  on a wrong choice, inoculating against that exact mistake. Standard (the anti-
  template contract, §15): keys = exactly the NON-selected options (for MSQ, every
  option not in the correct set); 1–2 DENSE lines each; the first line DELIVERS its §9 diagnosis in natural
  language — the type itself is recorded internally (§9), never rendered — and
  must ACTUALLY produce that option's value/content (back-derive
  the distractor — "if a student did X they get exactly this option"); the line
  also carries the corrected value ("13 × 3 = 39, not 36"). No two wrong options
  share an explanation. For negative stems the true options are "a TRUE statement,
  therefore NOT the answer" — never "incorrect" (§10a). For factual classes every
  reason is a web-confirmed fact.
  NAT analogue — COMMON PITFALLS: a NAT question has no options to reject, so this
  section lists the wrong VALUES a student most commonly computes, ≥1, each headed
  by the value and naming the slip that yields it in natural language ("forgetting
  to divide leaves 235 unchanged"; "dividing by the wrong count gives 9.4
  instead"), the §9 type recorded internally.
  Same anti-template discipline: each pitfall must reproduce a real wrong value.
  Enforced: key set (mcq/msq) or ≥1 value-keyed pitfall (nat) + ≥1 sentence +
  ZERO internal taxonomy tokens in rendered text (engine v2.6) + banned
  templates/glyphs (engine); diagnosis recorded internally +
  reproduces-the-wrong-answer + factual truth by discipline (§18 self-audit).

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

  SCIENTIFIC / STRUCTURAL TYPES (v2.7). The eleven above are aptitude-shaped and force a
  science distractor into an ill-fitting label — a regiochemistry slip logged as
  "off_by_one" teaches the learner nothing. Additive; the ban on a WHY WRONG line with
  NO type is unchanged.

  | Error type            | When it applies                                   |
  |-----------------------|---------------------------------------------------|
  | wrong_condition       | right transformation, wrong stated condition (work-up, solvent, pH, temperature, order of addition) |
  | regiochemistry_error  | correct reaction at the wrong position/site       |
  | stereochemistry_error | wrong configuration, or some stereocentres inverted not all |
  | mechanism_confusion   | a different mechanism's product                   |
  | electron_count_error  | miscounted electrons / occupancy / oxidation state |
  | symmetry_error        | equivalence or a mirror plane wrongly asserted or missed |
  | overgeneralised_rule  | a valid rule applied outside its validity domain  |
  | concept_reversal      | the governing relationship applied in reverse     |

  INTERNAL DIAGNOSIS, NATURAL RENDERING (v2.13). The error type is METADATA.
  It is still MANDATORY — every wrong option / pitfall is diagnosed with exactly
  one §9 type, recorded per option in progress state (alongside the derived
  answer in pyq_answer_keys.json / pyq_explain_progress state) — but the
  snake_case token NEVER appears in student-facing text. The visible first line
  DELIVERS the diagnosis in the subject's own natural language ("this is the
  para product, formed only when both ortho positions are blocked"), never as a
  machine label ("regiochemistry_error: ..."). REFERENCE INCIDENT: a delivered
  60-question paper opened all 40 WHY WRONG entries and all 20 NAT pitfalls with
  the raw token — obeying the old "first line names an error type" literally.
  ENFORCED: engine v2.6 raises at write time on any §9 token in a rendered
  sentence and re-scans the rendered bytes at verify time; the reproduce check
  (§15-2) is unchanged and still binds in full.

# ════════════════════════════════════════════════════════════════════════
# §10 — SPECIAL-CASE PROTOCOLS
# ════════════════════════════════════════════════════════════════════════
#   Protocols for negative stems, composite options, and MSQ/NAT questions.

## S10a — Negative stem
  Trigger: stem contains NOT / EXCEPT / INCORRECT / FALSE (configurable).
  DEDUCTION gives a truth-verdict for EVERY option, then isolates the target.
  WHY WRONG states each option is TRUE (hence NOT the answer); polarity_flip is
  recorded internally (§9), never rendered.

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

## S12-4 — NO COVERAGE BANNER (v2.17 — RETIRED; operator decision)
  The delivered _PYQ_Explanation.docx carries NO document-level coverage banner — not
  on an interim batch, not on the final one. PYQ-1 NEVER calls
  explain_engine.set_coverage_banner(); the delivered file's first non-blank body
  paragraph is Q.1 (blank separators before it are fine). Because build_interleaved_docx
  seeds the clean Row-file source WHOLE every batch (S4-4 C), no banner can exist unless
  a session writes one — §18-1 asserts that none does.
  WHERE COVERAGE IS STATED INSTEAD (unchanged): the chat progress line (S19-3), the F1/F2
  delivery footer (Framework_DeliveryFooter — "batch X of Y"), and the per-batch coverage
  assertion (S4-5 guard 3 / §18). Only the in-file announcement is gone.
  HISTORY (record, not instruction). v2.9 introduced the banner for
  GAP-2026-08-19-INTERIM-ARTEFACT-UNLABELLED: a Batch-1 file carrying 10 of 60
  explanations was reviewed by a third party as a finished document. The operator has
  accepted that trade-off (2026-08-24): a partially-explained file forwarded outside the
  chat is no longer self-labelled. The retirement also removes a cross-step conflict —
  Framework_PYQDeliver's detect_header_paras() (same net as MockDeliver S4-2) strips
  every non-blank pre-Q.1 paragraph as an upstream regression and alarms on it, so the
  mandated final banner was itself a deliver-step finding. Engine v2.4's
  set_coverage_banner() / strip_solutions() banner handling and the BANNER-* self-test
  fixtures are retained untouched (no engine change; the function is simply unused).

# ════════════════════════════════════════════════════════════════════════
# §13 — FIGURAL DEEP-ANALYSIS PROTOCOL (view every image — no exception)
# ════════════════════════════════════════════════════════════════════════
#   No ExplanationBlock for a figural question may be built until every image in
#   that question has been extracted, role-bound, and VIEWED. For PYQ, there are
#   no figural_manifests from a registry — detect figural questions structurally
#   from the Row file only (any question with <w:drawing> in stem or options).

## S13-1 — Detect figural questions structurally
  A question is figural if its region contains a <w:drawing> in the STEM or in
  any OPTION. Two PLACEMENTS: IMAGE-IN-STEM and IMAGE-AS-OPTIONS.

  AND — v2.7 — TWO FAMILIES, which decide HOW the figure is READ. Placement and family
  are independent; either family can appear in either placement.
    • TRANSFORMATION-PUZZLE — the figure carries no domain meaning; the answer lies in a
      geometric or set operation on abstract marks. Series, analogy, odd-one-out,
      mirror/water image, paper folding, cube net, embedded/counting figures, space
      orientation. (Reasoning sections: SSC, CAT, IBPS, police/defence.)
    • SCIENTIFIC-DIAGRAM — the figure DENOTES something, and the answer depends on what
      it denotes, never on its pose on the page. Molecular structures and reaction
      schemes, stereochemical projections (Fischer/Newman/chair/wedge-dash), orbital and
      energy-level diagrams, circuits, ray diagrams, free-body and vector diagrams,
      graphs, spectra, titration curves, maps, anatomical diagrams, apparatus schematics.
      (Subject papers: JAM, GATE, NEET, JEE, boards.)
  DECIDING THE FAMILY: read section_rules figural cues and the subtopic; if the marks in
  the figure have NAMES in the syllabus (an element symbol, a bond, an axis label, an
  orbital, a component), it is SCIENTIFIC-DIAGRAM. Abstract shapes with no such naming
  are TRANSFORMATION-PUZZLE. When genuinely mixed, read it as SCIENTIFIC-DIAGRAM: the
  stricter reading never damages a puzzle, whereas reading a structure as a puzzle loses
  the domain content entirely.
  PYQ NOTE: these are REAL past papers, so in a subject paper the scientific family is
  the overwhelming default — and the §13A transcription (not the raw stem) is what the
  family judgement and the reading are made from.

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

## S13-4 — Write what is visible (BOTH families)
  Common to both: DEDUCTION cites CONCRETE features actually present in the §13A
  transcription, never a generic gesture at "the figure". WHY WRONG names, per wrong
  option-figure, the specific difference that makes it wrong.

## S13-4a — TRANSFORMATION-PUZZLE family (unchanged behaviour)
  AXIOM = the visual rule (rotation / reflection / element add-remove / count /
  net-folding). DEDUCTION traces the VISIBLE transformation step by step to the chosen
  option. This is the pre-v2.7 protocol, preserved: for a genuine reasoning puzzle it
  was correct and stays correct.

## S13-4b — SCIENTIFIC-DIAGRAM family (v2.7)
  AXIOM = the DOMAIN PRINCIPLE the figure is testing — never "the visual rule". The
  figure is notation for a fact, so the governing fact is the axiom.
  READ THE FIGURE AS NOTATION, IN THIS ORDER, BEFORE SOLVING:
    1. IDENTIFY what is drawn, in the domain's own terms.
    2. TRANSCRIBE the decisive features EXACTLY: bonds and bond orders, charges,
       wedge/dash direction, ring size, substituent identity and position, atom
       numbering, stereo-descriptors, reagent ORDER above/below the arrow, axis labels
       and units, component values, arrow directions, occupancy.
    3. Only then SOLVE, from that transcription.
  For PYQ these features come from pyq_figural_vision.json (§13A-4); if a decisive
  feature is absent from the transcription it was NOT SEEN, and the question is a
  VOID_ITEM (§13A-5) — not a case for judgement.
  THE PROHIBITION THAT MATTERS MOST: never infer an unreadable feature from whatever
  would make an option work. A figure read backwards from a plausible answer produces a
  confident, wrong, unfalsifiable explanation — and on a REAL past paper it also
  misrepresents what the exam actually asked.
  POSE IS NOT MEANING. A scientific figure means the same thing rotated, reflected or
  redrawn. Two structures drawn differently may be the SAME compound; two drawn
  identically apart from one wedge may be DIFFERENT compounds. Never reason from
  page-orientation, and never treat a redrawing as a transformation — that is the
  §13-4a reflex misapplied, and it is wrong here.
  PRESERVE THE QUESTION'S OWN REPRESENTATION. Fischer stays Fischer; Newman stays
  Newman; chair stays chair. Convert ONLY when the conversion IS what is being tested.
  WHY WRONG for this family names the DOMAIN error (§9's scientific types —
  INTERNAL names, recorded per §9 and never rendered), never a
  merely visual difference: "the double bond is at C3 rather than C2" is the
  explanation; "the shape differs" is not.

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
       v2.15 — §13-2b SEMANTIC OBJECT. Where the figure is a typed object
       (paper_pipeline.SEMANTIC_KINDS) ALSO write its machine-readable form:
       a STRUCTURE as SMILES, a REACTION as reaction SMILES, a NEWMAN / FISCHER /
       MO_DIAGRAM / COORDINATION as its descriptor, with parse_confidence
       HIGH / MEDIUM / LOW. At solve time every STRUCTURE is passed through
       explain_engine.canonical_structure: a SMILES rdkit rejects is a MISREAD
       (re-view once; still rejected → VOID_ITEM per §13A-5). LOW confidence on
       an answer-critical figure → re-view; still LOW → DERIVATION-CONFIDENCE.
       Never reason from pixels directly; reason from the object.
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
  3. TRANSFER-SAFE (v2.14): read alone, stripped of the question, the shortcut
     survives the §7-7 neighbour test at this exam's level; it is not weaker than
     a one-line exact method; an option-dependent trick is phrased as option
     ELIMINATION, never as a rule of the subject; and no common, examinable,
     answer-reversing exception stands unqualified. ALL THREE must pass (the
     rule's title is kept for cross-reference; the test is three-part).

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

## S14-3b — EVERY SHORTCUT CARRIES ITS VALIDITY DOMAIN (v2.10)
  A SPEED HACK is the line a student memorises. That is what makes it useful and what
  makes an unscoped one the most damaging sentence in the block: it is recalled verbatim,
  under time pressure, in a question where its conditions do not hold.
  So every SPEED HACK states — in the shortcut itself, not in a caveat afterwards — the
  CONDITIONS under which it is safe. The scope is part of the shortcut, not an apology
  attached to it.
  The example below is from one domain; the SHAPE is what transfers — an unscoped rule
  states an outcome, a scoped one states the outcome AND the situation that triggers it.
    NEVER : "a bulky base always gives the less substituted alkene"
    WRITE : "when two beta-sites compete and the base is hindered, check the less
             substituted alkene FIRST"
  Note the difference from §8-0b. That rule bans stating a tendency as an absolute; this
  one requires the SCOPE to be present at all. "A bulky base usually gives the less
  substituted alkene" satisfies §8-0b and still fails here — it is calibrated but
  unscoped, so it never tells the student WHEN to reach for it.
  A SHORTCUT THAT CANNOT BE SCOPED IN ONE CLAUSE IS NOT A SHORTCUT. If stating the
  conditions takes longer than the DEDUCTION, the honest outcome is to OMIT (§14-1) —
  the §14 default has always been omit, never fake, and an over-broad shortcut is a
  species of fake.
  THE TEST: read the shortcut alone, stripped of the question. Could a student apply it
  to a question where it is WRONG and never notice? If yes, it is unscoped — fix or omit.

## S14-4 — The honesty guard
  If you cannot state the SPECIFIC lever that saves SPECIFIC work, there is no
  SPEED HACK — omit it. An empty or generic SPEED HACK is a defect — caught by
  producer discipline (§18), since (v2.1) no downstream audit follows.

## S14-5 — ELIGIBILITY IS RECORDED; THE DISTRIBUTION IS A TRIPWIRE (v2.13)
  For EVERY question, record the §14-1 outcome in progress state next to the
  representation verdict: {distinct_method, genuinely_faster, scoped} and the
  include/omit decision. §R3 reports the inclusion RATE alongside the count.
  WHY. The two-part test binds per question and nothing measured the aggregate,
  so inclusion pressure compounded invisibly: the reference paper carried a
  SPEED HACK on 56 of 60 questions — 93 percent — several of them restating the
  DEDUCTION in fewer words, a §14-1 part-1 failure each. A per-question rule
  with no distribution check is how a paper drifts to hack-everywhere while
  every individual decision felt defensible.
  THE TRIPWIRE, never a quota: if EVERY question in a batch carries a SPEED
  HACK, re-run the §14-1 test on each of them before §18. A hack that fails its
  re-audit is REMOVED (omit, never fake); a genuinely shortcut-rich batch —
  they exist — survives its re-audit unchanged and ships as it stood. No target
  rate exists in either direction; §16-1's pattern-matching cause is what an
  all-hack batch signals, and a re-test is the proportionate response.
  (v2.14) The record carries FOUR fields {distinct_method,
  genuinely_faster, scoped, transfer_safe}; §R3 reports hacks OMITTED on part 3.

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
  1. DIAGNOSE with exactly one §9 error type — recorded internally (§9) while the
     first line delivers that diagnosis in natural language: a diagnosis, not a
     dismissal, and never the raw token (engine v2.6 raises on one).
  2. PROVENANCE BEFORE EXPLANATION (v2.15 — REWRITTEN; engine v2.8 gate). Two modes,
     recorded per wrong option / value in ExplanationBlock(error_provenance=…):
       MODE A — VERIFIED_ERROR_PATH: name the wrong operation AND give the engine an
         arithmetic expression (`recompute`) with the `target`; the block is REFUSED
         unless the result reproduces the target at its own precision (DST_UNVERIFIED_
         NUMERICAL_ORIGIN). A non-numeric target records the wrong CONTENT produced and
         `matches_target: true` after checking it IS this option. Only MODE A may say
         "doing X gives Y".
       MODE B — DIRECT_CONTRADICTION: no path claimed; the line states why the option /
         value contradicts the correct relation. DEFAULT when no path verifies.
     THE PREVIOUS WORDING — "a real path always exists … go solve it" — IS WITHDRAWN
     (see MockTestExplain §15-2 for the incident). Hedged provenance ("or otherwise /
     perhaps by / or a similar") is engine-banned here (DST_HEDGED_PROVENANCE).
  3. CARRY the corrected value — what the right step gives instead ("13 × 3 = 39,
     not 36"; for NAT, "…, not 90"). The explicit contrast is mandatory.
  4. NO two wrong options/values share wording; NO banned template sentences.

## S15-3 — Class- and type-specific shape
  Computational → the arithmetic slip + the wrong number. Factual → what the option
  ACTUALLY is (the corrected fact). Negative stem → "TRUE, therefore not the answer"
  (never "incorrect"). Composite → the exact component that breaks it. Vocab → the
  precise nuance missed. RC → the passage line that REFUTES the option.
  MSQ → OPTION → the WRONG FEATURE or ASSUMPTION → the DECISIVE CORRECTION (v2.14):
  name the test the statement passes and the test it fails, as CONTENT of the
  subject, never as a story about the learner. The previous wording ("lead with
  the SEDUCTIVE HALF … a hasty solver") is WITHDRAWN — see MockTestExplain §15-3
  for the incident; engine v2.7 raises on learner-psychology boilerplate
  (DST_UNSUPPORTED_LEARNER_PSYCHOLOGY).
  NAT (COMMON PITFALLS) → head each entry with the wrong VALUE, name the slip that
  yields exactly it (MODE A, recomputed) or the contradiction (MODE B), and carry the
  contrast to the correct value. NO QUOTA (v2.15): ≥1 entry; a second only when a
  second VERIFIED path exists, never for symmetry.
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
  [ ] §6A router verdict present for EVERY question in this batch AND carried on
      each block (engine coherence — a visual verdict requires its figure, a §6A-4
      degrade carries the degraded requirement); every §6A-1b structure-answer
      question either emits STRUCTURE_GRAPH or its PROSE justification is
      recorded; every degrade disclosed for §R3                             (§6A)
  [ ] SPEED-HACK ELIGIBILITY recorded per question (§14-5); if every question in
      this batch carries a SPEED HACK, the §14-1 re-audit was run and any hack
      failing it removed BEFORE this checklist                            (§14-5)
  [ ] count invariants: image / table / OMML / question / option counts == Row file
  [ ] strip-and-re-audit: questions-only copy passes (§12-3)
  [ ] NO COVERAGE BANNER (v2.17 — §12-4): zero body paragraphs begin with
      cfg.labels['coverage_banner']; the first non-blank body paragraph of the delivered
      docx matches cfg.q_re (Q.1). A banner found → remove it (set_coverage_banner(out,
      cfg, None)), re-build, re-audit — never ship it (the deliver step alarms on it)
  [ ] every CA fact web-verified with a recorded source (§7 / RE-18)
  [ ] derived answers flushed to pyq_answer_keys.json; CA three-way binding holds
  [ ] coverage assertion (S4-5 guard 3): exactly Q1..last(batch k)
  [ ] learnings coverage (§24): every applicable rule routed; the SUBJECT-level
      file, when present, loaded and its neighbour library used by §7-7
  [ ] TRANSFER-SAFETY RECORD (v2.14) present for EVERY question (§7-7) and passed
      into its block; every AXIOM typed; zero kept absolutes undeclared
  [ ] REPRESENTATION ALIGNMENT (§6A-1c) recorded; §6A-3b tripwire evaluated
  [ ] SPEED HACK part-3 outcomes recorded (§14-5 four-field record)
  [ ] (v2.15) SEMANTIC OBJECTS (§13-2b / §13A-3): every typed figure's transcription
      persisted, every STRUCTURE rdkit-sanitised · ERROR PROVENANCE mode counts captured
      (§15-2) · transfer_tripwire evaluated, second pass recorded if fired (§7-7) ·
      §6A-1b-ii Qs emit the enumerated objects or carry a recorded justification
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
pfile = f'{EXAM}_difficulty_profile.json'                  # v2.18 — S7A-6 profile, final batch only
_pf_due = FINAL_BATCH and globals().get('PROFILE_STATUS') != 'dormant'
expected = ({sol, prog, pfile} if _pf_due else {sol, prog}) if FINAL_BATCH else {sol}
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
    ('8 difficulty profile written on final batch (S7A-6)',
                                                (not _pf_due) or os.path.exists(f'{out}/{pfile}')),
]
fails = [n for n, ok in checks if not ok]
if fails:
    raise SystemExit('HARD STOP (S19-1): ' + '; '.join(fails))
```
  (S7A-6 runs immediately BEFORE this checklist on the final batch; the `pfile`
  name above is the one it wrote.)

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
    if globals().get('PROFILE_STATUS') != 'dormant':                                 # v2.18 — S7A-6
        deliverables.append(f'/mnt/user-data/outputs/{EXAM}_difficulty_profile.json')
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
  §R1 PROVENANCE: paper [date] [session] · THIS spec's version as read from its own
      header · the engine self-test line EXACTLY as the engine printed it · timestamp ·
      EngineConfig (option count(s), label scheme, language, terminators).
      v2.7 — BOTH VERSIONS ARE READ, NEVER PINNED. This line carried the literal
      "spec v1.1 · engine 62/62" while the spec stood at v2.6 and the engine printed
      78/78, misreporting the very thing provenance exists to record. Any exact count
      written here goes stale the moment a fixture is added — the same failure mode as
      GAP-2026-08-13-STALE-SELFTEST-PIN, which is why the GATE at P0 is floor form
      (N >= 62). A report line is not a gate and must not become one: report what ran,
      assert nothing.
  §R2 VERDICT: SHIP (delivered) / HALTED.
  §R3 COVERAGE: Q_TOTAL/Q_TOTAL explained · question-type split (mcq/msq/nat) ·
      SPEED HACK count AND inclusion rate (Q-numbers; §14-5 — a near-total rate on
      a mixed-class paper is the §16-1 pattern-matching signal; report it, do not
      editorialise) · OMML count · per-class distribution.
      REPRESENTATION (v2.7 — the §6A-3 distribution):
        • verdict counts across PROSE / EQUATION / TABLE / STRUCTURE_GRAPH /
          LEVEL_DIAGRAM / DATA_PLOT, plus Q-numbers for every non-PROSE verdict.
        • figures declared vs figures landed (must be equal — §18 blocks otherwise).
        • DEGRADE LEDGER: every §6A-4 step-down with the Q-number, the requirement
          asked for, what it degraded to, and WHY (renderer absent / preflight failed /
          §6A-5 validation mismatch / VOID_ITEM per §6A-2b). An EMPTY ledger is stated
          explicitly as empty — a silent absence and a clean run must not look identical.
        • §6A-1b structure-answer questions routed to PROSE, each with its recorded
          justification (Q-numbers; an empty list stated as empty).
      A distribution that is 100% PROSE on a diagram-heavy paper, or one emitting a
      figure for nearly every question, is the signal this line exists to surface: both
      mean the §6A-1 two-part test is not being applied. Report counts; do not editorialise.
      TRANSFER SAFETY (v2.14 — the §7-7 distribution): AXIOM epistemic-type counts ·
        claims NARROWED / MOVED_TO_DEDUCTION · SPEED HACKs OMITTED on §14-1 part 3 ·
        kept absolutes (count of declared sentences) · neighbours drawn from the
        curated library vs session-generated (counts; a library-absent run says so).
      ALIGNMENT (§6A-1c): questions re-routed by the §6A-3b tripwire (Q-numbers;
        an empty list stated as empty).
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

  §R13 DIFFICULTY PROFILE (S7A-6, v2.20 — final batch only): PROFILE_STATUS
       ('added' | 'excluded' | 'dormant', + PROFILE_REASON verbatim); on 'added' the
       paper's scored/held counts and every UNSCORED question with its reason (e.g.
       "added — 58/60 scored; unscored: Q.22 Row-file defect…, Q.35 VOID_ITEM…");
       the sittings the profile now covers and its summary_at_write per section; and ONE operator line:
       "Upload [ExamCode]_difficulty_profile.json to this project's Files section
       (replace the old one) BEFORE the next PYQExplain run — each run starts from
       the uploaded copy, so a run started on an older copy drops the papers
       explained since (Blueprint will flag them as absent; re-run PYQExplain on
       them to recover). MockBlueprint reads the profile from there."
  §R12 FIGURAL VISION (§13A, v1.2): artefacts extracted · artefacts transcribed
       OK · every VOID_ITEM question with its status (MISSING/EMPTY/THIN/STALE)
       and the stated remedy. Reported here and NOT in §R7 — a vision shortfall
       is a session defect, not an exam-body error. If any VOID_ITEM exists the
       verdict is SHIP-AMBER, never SHIP.

# ════════════════════════════════════════════════════════════════════════
# §21 — DEFINITION OF DONE / HARD INVARIANTS
# ════════════════════════════════════════════════════════════════════════
  0.  (v2.8) NO EXACT SELF-TEST OR VERSION COUNT IS EVER WRITTEN INTO PRESCRIPTIVE
      TEXT IN THIS SPEC — not in a gate, not in a dashboard template, not in a report
      field, not in a checklist. Every such reference is EITHER floor form
      ("N/N PASS with N >= 62")
      where it gates, OR read from what actually ran where it reports. RATIONALE: an
      exact count is correct only until the next fixture is added, and this shape has
      been fixed repeatedly one instance at a time — GAP-2026-08-13-STALE-SELFTEST-PIN
      (the P0 gate, v2.5), v2.7 (the §R1 report line), and v2.8 (§21 and the
      engine-capability reference). Fixing the instance and leaving the class is what
      let it recur. Engine INTEGRITY is proved by bootstrap.py's sha256, never by a
      count. Identical in substance to MockTestExplain §21-0: one rule across both
      explanation specs, which share the engine this rule is about.
      SCOPE — PRESCRIPTIVE TEXT ONLY. This governs text that INSTRUCTS: gates,
      dashboard and report templates, checklists, definition-of-done items. It does
      NOT govern the HISTORICAL RECORD. A changelog entry, or an explanatory note
      describing a defect that was fixed, MUST be able to quote the stale value it is
      about — "this line carried 62/62 while the engine printed 78/78" is the evidence
      that makes the fix reviewable, and stripping it would leave a rule with no
      account of why it exists. The test is not whether a number appears; it is
      whether the number TELLS A SESSION WHAT TO DO. If it does, it is floor form or
      read-what-ran. If it merely records what once was, it stays.
  1.  Pre-flight P0-P10 passed; engine --self-test printed "N/N PASS" with N == total
      and N >= 62 (floor form, §21-0); config built from section_rules.
  2.  Every question explained (zero sampling); every validate() clean.
  3.  Every answer derived two ways; disagreements resolved 2-of-3 +
      DERIVATION-CONFIDENCE. Zero guesses. Typed correctly (mcq/msq/nat).
  3c. (v2.14) Every AXIOM and SPEED HACK transfer-tested and recorded (§7-7); every
      kept absolute declared (§8-0b); representations aligned (§6A-1c); zero
      learner-psychology narration (§15-3).
  3d. (v2.15) Every typed figure transcribed to its semantic object and sanitised
      (§13-2b); error_provenance engine-validated on every wrong option / value
      (§15-2); curated families cited (§7-7); typography engine-applied (§8-0c).
  3b. (v2.13) Decisive intermediate claims mutually consistent on every question
      (§7-6); every counting answer derived inventory-first, closed-form only
      after verified independence (§7-0c).
  4.  Every figural question's images extracted, role-bound, VIEWED ONCE at
      P2a (§13A) and persisted; every figural answer traceable to an OK
      transcription, or the question recorded as VOID_ITEM.
  5.  Every CA/factual option web-verified with a recorded source.
  6.  WHY WRONG keys == exactly non-selected; the §9 diagnosis (recorded
      internally, rendered in natural language — never the raw token, v2.13)
      REPRODUCES the option. NAT: ≥1 pitfall. No template/glyph/fake-cite.
  7.  SPEED HACK present IFF genuinely faster; never padded.
  7b. (v2.13) SPEED HACK eligibility recorded per question; any all-hack batch
      re-audited per §14-5 before delivery.
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
#     • [Subject]_EXPLAIN_LEARNINGS_v*.md (v2.14) — SUBJECT-LEVEL guardrails, same
#       schema, same parser, one file copied unchanged into every exam project of that
#       subject (e.g. CHEMISTRY_EXPLAIN_LEARNINGS_v1.md). It carries the §7-7 curated
#       neighbour library, the exam-convention classes and the §8-3 minimum-concept
#       components. RESOLVED BY DISCOVERY (v2.19, GAP-2026-08-28-CATEGORY-C-ORPHAN-
#       CONFIG-READ): explain_engine.resolve_learnings_files(project_dir, ExamCode)
#       partitions *_EXPLAIN_LEARNINGS_v*.md by the {ExamCode}_ prefix — the single
#       non-exam-prefixed file IS the subject file (no subject code is derived,
#       configured or read from anywhere; the former source, section_rules CATEGORY C
#       subject_code, was produced by nothing, so this library had never loaded on
#       any exam). >= 2 non-exam files → abstain + WARN naming all candidates (none
#       loaded). Precedence on conflict: exam files > subject file > this spec.
#   None exist on the first PYQ paper by design. Absence is normal, never a HALT.

# ── S24-1b — THE **Triggers:** FIELD (v2.15 — additive; the frozen schema still parses) ──
#   A rule MAY carry `**Triggers:** term, term, re:<regex>` — comma-separated phrases
#   (case-insensitive, whole-word) or raw regexes. parse_learnings reads it into
#   rules[].triggers; triggers_from_learnings compiles the table; the engine uses it
#   for §7-7 step 3. Every NEIGHBOUR-LIBRARY rule SHOULD carry one.
#
# ── S24-6 — DEFECT CODES INTRODUCED BY v2.15 ─────────────────────────────────────────
#   SEMANTIC-MISREAD · UNVERIFIED-PROVENANCE · HEDGED-PROVENANCE · LIBRARY-NOT-CITED ·
#   FORMULA-TYPOGRAPHY · MINIMUM-SPECIFICITY · FORMULA-OXIDATION-STATE ·
#   SITE-SET-CONFLATION · CAUSAL-CONFLATION (definitions: subject library).
#
# ── S24-5 — DEFECT CODES INTRODUCED BY v2.14 (routing keys for new rules) ─────────────
#   §24 ROUTING KEYS for the transfer-safety family: OVERGENERALISED-AXIOM ·
#   UNSAFE-SPEED-HACK (§14-1 part 3) · UNJUSTIFIED-ABSOLUTE (§8-0b) ·
#   EXAM-CONVENTION-AS-LAW · CONCEPT-MINIMUM-MISSING (§8-3) ·
#   REPRESENTATION-MISALIGNED (§6A-1c) · LEARNER-PSYCHOLOGY (§15-3) ·
#   NEIGHBOUR-LIBRARY (a curated neighbour family: Pattern = the unsafe
#   generalisation, Prevention rule = the safe scope, Verification = the canonical
#   counterexamples — the §7-7 library in the frozen schema, no new parser).
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
#     --self-test       → "SELF-TEST: N/N PASS", N == total and N >= 62 (core, required
#                          at P0; v2.8 floor form — §21-0, no exact count)
#     --self-test-audit → "AUDIT-SELF-TEST: N/N PASS", N >= 10 (reader round-trip; v2.5 floor form)
#   (v2.1: the companion gate explain_audit_gate.py and PYQExplainAudit (PYQ-2) were
#    RETIRED and removed from the framework; PYQ-1 does not use them.)

# ════════════════════════════════════════════════════════════════════════
# SHARED_RULES_VERSION: 1.6 (2026-08-30)
#
# SHARED-RULES BUMP (v1.6, 2026-08-30): GAP-2026-08-30-EXPLAIN-COLOUR-BINDING added the
# S6A-6 COLOUR clause (a §4-§18 rule) to BOTH files — MockTestExplain v1.49.0 and
# PYQExplain v2.21 — binding every explanation figure to figural_core's constants.
#
# (previous) SHARED_RULES_VERSION: 1.5 (2026-08-24)
#
# SHARED-RULES BUMP (v1.5, 2026-08-24): CHG-2026-08-24-NO-COVERAGE-BANNER changed one
#   shared §4–§18 section in BOTH files — §12 (S12-4 retired: no document-level coverage
#   banner, interim or final) — and added the matching §18-1 "NO COVERAGE BANNER" item
#   in both. No RE-* rule and no MANDATE changed; no engine change.
#   MockTestExplain v1.43.0 == PYQExplain v2.17 on every shared rule.
#
# SHARED-RULES BUMP (v1.4, 2026-08-21): GAP-2026-08-21-EXPLANATION-PROVENANCE changed
#   shared §4–§18 sections in BOTH files — §6A (S6A-1b-ii), §7 (S7-7 step 3 mechanical
#   + tripwire), §8 (S8-0c), §13 (S13-2b; PYQ-side folded into §13A-3), §15 (S15-2
#   rewritten, S15-3 NAT quota), §18, §21 and §24 (S24-1b Triggers, S24-6) — amended
#   RE-13 and added RE-24 in both. MOCK-ONLY: §7-8 KEY RECONCILIATION, §17-3/§17-4
#   in-run resolution, RE-23 (a PYQ has no Step-7 commitment; its RE-16 is unchanged).
#   MockTestExplain v1.37.0 == PYQExplain v2.15 on every shared rule.
#
# SHARED-RULES BUMP (v1.3, 2026-08-20): GAP-2026-08-20-TRANSFER-SAFE-EXPLANATIONS
#   changed shared §4–§18 sections in BOTH files — §5-1/§5-2/§5-3, §6A (S6A-1c,
#   S6A-2 CONFORMER, S6A-3b), §7 (S7-7), §8 (S8-0b gate, S8-2 epistemic type, S8-3
#   minimum components, S8-4 part 3), §14 (S14-1 part 3, S14-5 four fields), §15
#   (S15-3 MSQ rewritten, old wording withdrawn), §18, §21 and §24 (subject-level
#   file, S24-5) — and restated RE-22 in both. MockTestExplain v1.36.0 ==
#   PYQExplain v2.14 on every shared rule.
#
# SHARED-RULES BUMP (v1.2, 2026-08-19): GAP-2026-08-19-EXPLANATION-EXECUTION-
#   INTEGRITY changed shared §4–§18 sections in BOTH files — §6A (S6A-1b + verdict
#   coherence), §7 (S7-0c, S7-6), §9 (internal diagnosis, natural rendering),
#   §14 (S14-5), §15 (S15-2 item 1), §18 and §21 — and added RE-6d / restated
#   RE-13 in both. MockTestExplain v1.35.0 == PYQExplain v2.13 on every shared
#   rule; the §6A-1b VOID_ITEM precedence is the one recorded PYQ-side sharpening.
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
#   chore.
#
#   RESOLVED (2026-08-21, GAP-2026-08-21-DIFFICULTY-STICKER-LABELS) — the adopted
#   contract, exactly as this note asked: the two pipelines SHARE THE RUBRIC
#   (blueprint_core.assess_difficulty, Cluster E2) while keeping different
#   mechanisms, and §7A was NOT copied across.
#     · PYQ side (this file, §7A): difficulty is a MEASUREMENT — unchanged.
#     · Mock side: difficulty is a SPECIFICATION enforced AT AUTHORING —
#       MockTestCreate v5.60 builds a floor-honouring band plan
#       (bc.assign_difficulty_bands), authors each question TO its band
#       (bc.difficulty_authoring_profile), and accepts it only when the recorded
#       derivation evidence measures as the band (CHECK 3c / G-DIFF via
#       bc.verify_difficulty_obs). Blueprint v1.51.0 validates every requested
#       mix against the exam shape's rubric floors (S7-3 V5). audit_canonical
#       v2.15 re-verifies label-vs-evidence mechanically forever (A-QINDEX 7/8).
#     · Which wins: the STICKER WINS ON THE PAPER — because from v5.60 the
#       sticker is a conclusion from evidence, not a slot name. TestExplain
#       §7A-M (v1.38.0) re-measures ADVISORILY from Step 9's independent
#       derivation and reports agreement; it never re-labels.
#   No RE-* rule, no MANDATE and no shared §4-§18 rule changed on either side,
#   so SHARED_RULES_VERSION is not bumped — the same reasoning this note has
#   always recorded.
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
# END OF Framework_PYQExplain v2.21
# ════════════════════════════════════════════════════════════════════════
