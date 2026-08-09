# Framework_NotesAudit v1.1.0 — Notes Pipeline Step NA (Closed-Book Solvability Audit)
# v1.1.0 — 2026-08-08 — REFINEMENT GATES. Adds the machine gates that enforce
#   the v2 document standard of Framework_NotesCreate: content-style ban scan
#   (G-4), question-type-set and template gate (G-5), outline-number integrity
#   (G-6); G-2 extended with the dual zero-issue math scans (no textual
#   exponents or unicode scripts inside oMath; no flat math tokens in any
#   text run); G-3 re-pointed at the v2 anatomy. Gate helpers live in
#   notes_core >= v1.1 and were regression-locked against the approved
#   Enzyme Kinetics golden sample.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE. Encodes the audit protocol proven on
#   Enzyme Kinetics (35 SOLVABLE + 2 PARTIAL at v0.1; both patched; 37/37 at
#   v0.2 in one convergence iteration) plus the two environment rules that run
#   discovered: OMML structural verification and docx line-rule clipping.
# [ExamCode] project | Notes Step NA | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py  >= v1.1 — density-gate constants, math gates, PROSE_BAN
#                            lexicon, registry transitions
#   notes_audit.py >= v1.0 — verdict/report schema, convergence-loop state,
#                            figure extraction + binding
#
# PURPOSE:
#   Machine-verify the NotesCreate guarantee: after reading ONE subtopic's
#   notes, every in-syllabus PYQ of that subtopic is solvable. NA is the ONLY
#   quality gate in the Notes pipeline (no human review exists).
#
# PIPELINE POSITION:
#   Notes Step NC (NotesCreate) → draft .docx + PYQ bank
#   Notes Step NA (NotesAudit)  → THIS SPEC
#   Notes Step ND (NotesDeliver)→ delivery of AUDITED_PASS units only
#
# PREREQUISITE:
#   Unit state DRAFTED; the unit's PYQ bank artifact from NC §1 is present.

## §1 — FIGURE EXTRACTION (prerequisite pass)
Before auditing, every bank question flagged FIGURE gets its images bound:
download the source .docx, unzip, walk word/media, and bind images to bank
ids by document position (notes_audit.bind_figures). If a source .docx cannot
be obtained in the run environment (e.g. binary transport unavailable), the
affected questions are audited on their TEXT STEMS and tagged FIGURE_PENDING;
they re-audit automatically when the file arrives. FIGURE_PENDING does not
block a pass verdict when concept coverage is complete on the stem.

## §2 — CLOSED-BOOK SOLVE PROTOCOL
For each bank question, in order:
  P-1 Extract the tested concept(s).
  P-2 PRESENCE: locate where the notes teach each concept (block reference).
  P-3 SOLVE the question using ONLY the notes text — no outside knowledge
      beyond the Level-assumed prerequisites declared in the blueprint.
  P-4 VERDICT: SOLVABLE | PARTIAL | NOT, with the notes location and the
      produced answer recorded.
Ambiguous stems that admit two defensible answers under the notes' correct
rules (e.g. a both-valid-options MCQ) are verdicted SOLVABLE with a KEY_FLAG
and queued for official-key resolution.

## §3 — ANSWER MODES
  M-1 QUESTION-ONLY MODE (default until the operator supplies solved PYQs):
      the audit SELF-GENERATES answers; the report labels them self-answers.
  M-2 GROUND-TRUTH MODE: when solved PYQs with explanations arrive in project
      Files, all self-answers are replaced, every unit auto re-audits, and
      KEY_FLAG items resolve. This re-audit is a STANDING TRIGGER.

## §4 — CONVERGENCE LOOP (no delivery block; loop until pass)
  L-1 Any PARTIAL/NOT verdict produces a targeted PATCH to the notes; the
      affected questions re-audit; the notes minor version bumps.
  L-2 After 3 FAILED patches on the same question: FULL REGENERATION of the
      unit's notes (back to NC), then full re-audit.
  L-3 After ~3 full regenerations without convergence: STOP and emit a
      DIAGNOSTIC REPORT — persistent non-convergence signals a data problem
      (bank extraction, blueprint scoping, or source quality), not a drafting
      problem. The diagnostic names the suspect stage.
  L-4 Every patch is logged in the audit report (id, gap, patch text ref).

## §5 — MACHINE GATES RUN ALONGSIDE THE SOLVE
  G-1 DENSITY GATE (constants in notes_core.py, spec in NotesCreate §5):
      bullet word counts, table-first violations, page count within tier band.
  G-2 MATH GATES (all three must report ZERO findings):
      (a) OMML presence verified by XML assertion (m:oMath count + expected
          content tokens). NEVER verify equations via a LibreOffice-rendered
          preview: LibreOffice DOCX→PDF drops OMML SILENTLY (verified
          2026-08-08 with a minimal fixture). Visual page checks remain valid
          for layout, images and tables.
      (b) STRUCTURAL-OMML SCAN: no textual exponent ("^(") and no unicode
          super/subscript character inside any oMath region.
      (c) FLAT-TOKEN SCAN: no un-styled math token (the notes_core token
          lexicon) in any plain text run anywhere in the document.
  G-3 ANATOMY GATE: required blocks for the unit's tier are present and in
      order per the v2 anatomy in Framework_NotesCreate, including: no EXAM
      LENS block; RECALL CHECK items follow the Example template minus
      Explanation and speed hack; adjacent boxes separated by spacers.
  G-4 CONTENT-STYLE BAN SCAN: zero occurrences of the PROSE_BAN lexicon
      (type names, PYQ token, star glyphs, year references, "Q:" prefixes,
      editorial lead-ins) in document text, honouring any per-unit
      exemptions declared in the blueprint.
  G-5 QUESTION-FORMAT GATE: every Example and Recall item matches the fixed
      template (options as numbered lines for choice types; bold Answer
      before Explanation; NAT stems carry unit + rounding) and its type is a
      member of the blueprint's allowed_question_types; across the unit all
      allowed types are represented where evidence permits.
  G-6 OUTLINE-NUMBER INTEGRITY: level numbering is gapless and sequential;
      every in-text cross-reference resolves to an existing outline number.

## §6 — REPORT AND STATE
The audit report artifact (schema notes_audit.REPORT_SCHEMA) carries: per-id
verdict table with notes locations and answers, the convergence log, the
FIGURE_PENDING and KEY_FLAG queues, and gate results (G-1 through G-6). On 100% SOLVABLE (with
FIGURE_PENDING permitted per §1) the unit moves DRAFTED → AUDITED_PASS and
the report is stored beside the notes artifact. PARTIAL/NOT never persists
past the loop of §4 — the loop exits only at pass or at the §4 L-3 diagnostic.

---

# END OF Framework_NotesAudit v1.1.0
