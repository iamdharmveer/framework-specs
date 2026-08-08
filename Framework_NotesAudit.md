# Framework_NotesAudit v1.0.0 — Notes Pipeline Step NA (Closed-Book Solvability Audit)
# v1.0.0 — 2026-08-08 — INITIAL RELEASE. Encodes the audit protocol proven on
#   Enzyme Kinetics (35 SOLVABLE + 2 PARTIAL at v0.1; both patched; 37/37 at
#   v0.2 in one convergence iteration) plus the two environment rules that run
#   discovered: OMML structural verification and docx line-rule clipping.
# [ExamCode] project | Notes Step NA | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py  >= v1.0 — density-gate constants, OMML assertion,
#                            registry transitions
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
  G-2 OMML STRUCTURAL VERIFICATION: equations are verified by XML assertion
      (m:oMath presence + expected content tokens). NEVER verify equations via
      a LibreOffice-rendered preview: LibreOffice DOCX→PDF drops OMML
      SILENTLY (verified 2026-08-08 with a minimal fixture). Visual page
      checks remain valid for layout, images and tables.
  G-3 ANATOMY GATE: required blocks for the unit's tier are present (B1–B10
      per NotesCreate §4).

## §6 — REPORT AND STATE
The audit report artifact (schema notes_audit.REPORT_SCHEMA) carries: per-id
verdict table with notes locations and answers, the convergence log, the
FIGURE_PENDING and KEY_FLAG queues, and gate results. On 100% SOLVABLE (with
FIGURE_PENDING permitted per §1) the unit moves DRAFTED → AUDITED_PASS and
the report is stored beside the notes artifact. PARTIAL/NOT never persists
past the loop of §4 — the loop exits only at pass or at the §4 L-3 diagnostic.

---

# END OF Framework_NotesAudit v1.0.0
