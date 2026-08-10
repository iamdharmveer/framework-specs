# Framework_NotesAudit v2.0.6 — Notes Pipeline Step NA (Closed-Book Solvability Audit)
# v2.0.6 — 2026-08-10 — DEFECT-CLASS SWEEP (single-authority contracts). §7's
#   informal "[ExamCode]_<unit>.docx" now reads "the unit's F-1 filename" —
#   Framework_NotesCreate F-1 (notes_core.notes_filename) is the single
#   authority for notes filenames. Pairs with Framework_NotesCreate v2.2.1.
#   Nothing else changed.
# v2.0.5 — 2026-08-10 — TAXONOMY SYNC (Framework_NotesBlueprint v3.0.0). The
#   registry is KEYED BY the Step-5 manifest sid (notes-registry/2.0) and the
#   operator's unit reference is resolved exactly as in Framework_NotesCreate section 0
#   (notes_core.resolve_unit: Sub Topic Id -> Subject::Topic::Sub Topic Name ->
#   bare Sub Topic Name; ambiguous/zero hits STOP, never auto-pick). The audit
#   report's unit_code field carries the REGISTRY KEY (the sid); the chat line
#   names the unit as <Sub Topic Name> (<sid>). Bank joins are unchanged
#   (bank_questions_for on the unit's stored manifest triple). Companion:
#   notes_core >= v2.0. No gate logic changed; notes_audit.py is UNCHANGED.
# v2.0.4 — 2026-08-10 — CROSS-CHAT HANDOFF + STALE-REF FIX. (1) NA runs in its own
#   chat; on AUDITED_PASS it now present_files the audited .docx + audit report +
#   the updated registry and renders the footer (F2 on pass, F1 amber at the §4
#   L-3 diagnostic), so ND (a fresh chat) can deliver a byte-identical file (new
#   §7). (2) Corrected the stale claim that the PYQ bank is "NC's artifact from
#   §1" — since NB v2.0.0 the bank is NB's artifact and NC/NA are consumers; the
#   PIPELINE POSITION and PREREQUISITE lines now say so. Pairs with
#   Framework_DeliveryFooter v1.19.
# v2.0.3 — 2026-08-10 — POST-DEPLOY REVIEW. bank_questions_for joins by
#   RECOMPUTING the subtopic key from stored fields (drift class closed).
#   Companion: notes_core >= v1.8.
# v2.0.2 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 3 (subtopic-join normalization).
#   bank_questions_for joins via the hardened notes_core.subtopic_key
#   (syllabus_provenance.norm). Companion: notes_core >= v1.7,
#   +syllabus_provenance.py on the route.
# v2.0.1 — 2026-08-10 — DEPLOYMENT-REVIEW FIX 2 (vacuous-pass floor wired). A
#   unit pass is now certified ONLY through notes_audit.pass_for_unit(report,
#   unit_questions), which derives expected_count = len(unit_questions) from the
#   bank (notes_core.bank_questions_for) — so an audit that covered fewer than the
#   unit's bank questions can never certify AUDITED_PASS. §2/§6 name the source of
#   the count. Companion bump to notes_core >= v1.6, notes_audit >= v1.3.
# v2.0.0 — 2026-08-10 — GROUND-TRUTH + BANK FIGURES (Framework_NotesBlueprint
#   v2.0.0). NB now ingests the corpus and stores, per question, the verbatim
#   correct_answer, the explanation, and the stem/solution figure split. So NA:
#     (1) reads figures from the BANK (notes_audit.figures_for) — no re-download,
#         no bind_figures; extract_media/bind_figures are removed from the engine.
#     (2) runs PERMANENTLY in ground-truth mode: it solves from the notes and
#         matches the bank's answer with notes_audit.verdict_against_key
#         (MCQ token; MSQ unordered set; NAT rounding-precision tolerance from the
#         stem — owner decision 4b). Self-answer (question-only) mode is retired.
#     (3) DROPS KEY_FLAG (owner decision 4a): the doc key is authoritative and
#         never re-derived; a notes-derived answer that disagrees with the key is
#         a NOTES defect and enters the §4 convergence loop, not a key queue.
#   FIGURE_PENDING survives only as a rare safety path (§1) for an unresolved bank
#   figure; it is not the normal run (NB reads every image — owner decision 6).
#   Gates G-1..G-6 are unchanged.
# v1.1.0 — 2026-08-08 — REFINEMENT GATES (G-4 ban scan, G-5 type/template,
#   G-6 outline integrity; G-2 dual math scans; G-3 v2 anatomy).
# v1.0.0 — 2026-08-08 — INITIAL RELEASE. Audit protocol proven on Enzyme Kinetics
#   (37/37 at v0.2 in one convergence iteration).
# [ExamCode] project | Notes Step NA | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py  >= v2.0 — resolve_unit + sid-keyed registry; density-gate
#                            constants, math gates, PROSE_BAN
#                            lexicon, registry transitions, ground-truth match
#                            helpers (msq_match / nat_within_tolerance /
#                            nat_precision_from_stem / normalize_answer),
#                            bank_questions_for
#   notes_audit.py >= v1.3 — verdict/report schema (no key_flags), convergence
#                            loop, ground-truth verdict_against_key, bank figures,
#                            pass_for_unit (bank-derived vacuous-pass floor)
#
# PURPOSE:
#   Machine-verify the NotesCreate guarantee: after reading ONE subtopic's
#   notes, every in-syllabus PYQ of that subtopic is solvable. NA is the ONLY
#   quality gate in the Notes pipeline (no human review exists).
#
# PIPELINE POSITION:
#   Notes Step NB (NotesBlueprint) → notes_pyq_bank.json (the PYQ bank)
#   Notes Step NC (NotesCreate)    → the unit's draft .docx
#   Notes Step NA (NotesAudit)     → THIS SPEC
#   Notes Step ND (NotesDeliver)   → delivery of AUDITED_PASS units only
#
# PREREQUISITE:
#   Unit state DRAFTED; the draft .docx from NC and notes_pyq_bank.json from NB
#   (the bank is NB's artifact — NA is a read-only consumer) are in Project Files.

## §1 — FIGURES (read from the bank; no re-extraction)
NB already extracted every image from Drive and bound it to its question,
splitting stem figures from solution figures at the "Correct Answer:" line
(NB §3B B-5). NA does NOT open any .docx. For each bank question it reads the
solve-critical images with notes_audit.figures_for (stem figures only; solution
figures are part of the key, not the prompt) and views them alongside the stem.
DEGENERATE CASE ONLY: if a stem figure is recorded "UNRESOLVED:..."
(notes_audit.missing_figures is non-empty — rare, since NB reads every image),
that question is parked in report['figure_pending'] and re-audits when the bank
is refreshed; it never hard-stops the run (owner decision 6). There is no
binary-transport / stem-only fallback in the normal path.

## §2 — CLOSED-BOOK SOLVE PROTOCOL (ground-truth)
For each bank question, in order:
  P-1 Extract the tested concept(s).
  P-2 PRESENCE: locate where the notes teach each concept (block reference).
  P-3 SOLVE the question using ONLY the notes text (plus the stem figures from
      §1) — no outside knowledge beyond the Level-assumed prerequisites declared
      in the blueprint.
  P-4 MATCH the produced answer against the bank's verbatim correct_answer via
      notes_audit.verdict_against_key: MCQ option token; MSQ unordered set; NAT
      equal after rounding BOTH to the stem's stated precision
      (notes_core.nat_precision_from_stem, owner decision 4b).
  P-5 VERDICT: SOLVABLE (produced answer matches the key) | PARTIAL (notes teach
      the concept but the notes-derived answer misses the key) | NOT (notes do
      not teach the concept). The notes location and the produced answer are
      recorded (notes_audit.record).
KEY_FLAG IS RETIRED (owner decision 4a). The doc key is authoritative and never
re-derived. If a stem is genuinely ambiguous under the notes' rules, the notes —
not the key — are at fault: that is a PARTIAL that enters the §4 loop and is
fixed by tightening the notes, never by re-opening the key.

COVERAGE + PASS: NA audits EVERY one of the unit's bank questions —
unit_questions = notes_core.bank_questions_for(bank, subject, topic, subtopic) —
and certifies a pass ONLY through notes_audit.pass_for_unit(report,
unit_questions). That helper derives expected_count = len(unit_questions) from the
bank, so a run that recorded fewer verdicts than the unit has questions can never
vacuously certify AUDITED_PASS (fix 2).

## §3 — ANSWER MODE (ground-truth, permanent)
There is ONE mode. NB read the correct_answer and the explanation from every
sorted paper and stored them VERBATIM in the bank, so a ground-truth key always
exists. NA solves from the notes (§2 P-3) and matches that answer against the
bank key (§2 P-4). NA NEVER self-generates a key and NEVER re-derives the doc's
answer. new_report is opened with mode="ground_truth" (notes_audit rejects any
other mode). A refreshed bank (NB re-run) is a STANDING TRIGGER to re-audit the
affected units.

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
verdict table with notes locations and produced answers, the convergence log, the
FIGURE_PENDING queue (normally empty), and gate results (G-1 through G-6). There
is no KEY_FLAG queue (owner decision 4a). A unit passes ONLY when
notes_audit.pass_for_unit(report, unit_questions) is True — i.e. 100% SOLVABLE
across ALL of the bank's questions for this unit (expected_count =
len(unit_questions); the rare FIGURE_PENDING permitted per §1) — at which point
the unit moves DRAFTED → AUDITED_PASS and
the report is stored beside the notes artifact. PARTIAL/NOT never persists
past the loop of §4 — the loop exits only at pass or at the §4 L-3 diagnostic.

## §7 — DELIVERY / CROSS-CHAT HANDOFF
NA runs in its own chat, so the audited unit must reach ND (a fresh chat). On
AUDITED_PASS: present_files the audited notes .docx under the unit's F-1
filename (the SAME file ND
ships — delivery never edits content), the [ExamCode]_<unit>_Audit.md report, and
the updated notes_registry.json (unit → AUDITED_PASS); then RENDER THE F2
STEP-COMPLETE FOOTER as the LAST element (Framework_DeliveryFooter §4-1; 4-cell
NOTES bar "3 of 4"; header "Step NA · NotesAudit"; Next → ND: NotesDeliver in a
new chat). If the §4 loop instead exits at the L-3 non-convergence diagnostic,
render F1 AMBER with the quality-gate variant (the step ran, the unit is not
AUDITED_PASS, the diagnostic names the suspect stage) — still after a present_files
call, still the last element. The footer is obligatory after present_files
(Framework_DeliveryFooter §4-0 R1) and never omitted.

---

# END OF Framework_NotesAudit v2.0.6
