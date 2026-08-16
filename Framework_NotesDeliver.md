# Framework_NotesDeliver v1.2.0 — Notes Pipeline Step ND (Portal Formatting + Delivery)
# v1.2.0 — 2026-08-12 — CONSUMES NA's _Final (GAP-2026-08-12-NADOCX patch P2 of
#   2; pairs with Framework_NotesAudit v3.0.0).
#     (1) ND's input is now the unit's _Final.docx from NA
#         (notes_core.notes_final_filename), attached or filed per section 1.0,
#         and its output is notes_core.notes_deliver_filename —
#         {unit_code}_{Slug}_Deliver.docx. Three filename authorities now
#         exist (draft / _Final / _Deliver) and each is an ENGINE CALL; no step
#         spells a pattern.
#     (2) THE AUDIT REPORT IS GONE. NA no longer writes [ExamCode]_<unit>_
#         Audit.md; the evidence lives in notes_registry.json as the unit's
#         audit_summary (schema notes-registry/2.1). ND's delivery line reads
#         its verdict counts from there.
#     (3) PORTAL FORMATTING IS DEFERRED (owner decision, 2026-08-12). ND
#         currently ships the audited bytes UNCHANGED. When portal formatting
#         is specified it will make ND a SECOND WRITER downstream of the
#         certified bytes, so it will need its own terminal re-gate — and any
#         LibreOffice-based conversion will silently destroy every equation
#         (section 3). Recorded here so the requirement is not rediscovered
#         late.
#   Companions: notes_core >= v2.3.
# [ExamCode] project | Notes Step ND | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py >= v2.4 — notes_deliver_filename (the _Deliver authority),
#                           verify_docx_ref (the section 1.0 preflight against
#                           final_ref), registry schema notes-registry/2.1
#                           (audit_summary, final_ref), registry transitions,
#                           resolve_unit
#
# PURPOSE:
#   Deliver AUDITED_PASS notes to the operator (one .docx per subtopic, plus
#   its audit report) and advance the registry to DELIVERED.
#
# PIPELINE POSITION:
#   Notes Step NA (NotesAudit)   → AUDITED_PASS units
#   Notes Step ND (NotesDeliver) → THIS SPEC
#
# PREREQUISITE:
#   Unit state AUDITED_PASS. Units in any other state are refused with the
#   state named (never silently skipped).
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_NotesDeliver.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

## §1 — DELIVERABLES
  0. INPUTS (fresh chat): the unit's _Final.docx from NA
     (notes_core.notes_final_filename) — ATTACHED to the trigger, the same
     convention NA uses — plus notes_registry.json from Project Files. There is
     no _Audit.md: NA's evidence is the unit's audit_summary inside the
     registry (Framework_NotesAudit section 6). ND performs the preflight
     checks of Framework_NotesAudit section 0B against the unit's final_ref
     (filename identity, exam-code cross-check, sha256), and HARD STOPS the
     same way — a delivery step that ships an unverified file is the one thing
     this pipeline must not do.
  1. The delivered .docx, named by
     notes_core.notes_deliver_filename(exam_code, s, t, st, slug) — the ENGINE
     is the single authority for the recipe. v1.2.0 ships the audited bytes
     UNCHANGED (portal formatting deferred), so its content is byte-identical
     to NA's _Final.docx.
  2. A chat delivery line per unit: <Sub Topic Name> (<sid>), unit code,
     notes_version, verdict summary read from audit_summary (n/n solvable,
     including any SOLVABLE_KEY_CORRECTED), the JUDGEMENT-tier key corrections
     named individually, the quarantine list, and the open FIGURE_PENDING
     count.
  3. present_files the _Deliver.docx AND the updated notes_registry.json
     (unit -> DELIVERED, section 4), then RENDER THE F2 STEP-COMPLETE FOOTER as
     the LAST element of the response (Framework_DeliveryFooter section 4-1,
     the 4-cell NOTES pipeline bar "4 of 4", header "Step ND · NotesDeliver").
     The footer is obligatory after a present_files call (section 4-0 R1) and
     NEVER omitted. Next callout: NC — NotesCreate for the next subtopic, or
     "Notes pipeline complete" when every blueprinted unit is DELIVERED.

## §2 — DOCUMENT/VERSION SEPARATION
No version footer, draft marker or pipeline metadata appears INSIDE the
document (rule F-6 in Framework_NotesCreate). All versioning is chat-and-registry only.

## §3 — PORTAL PATH NOTE
Delivery format is Word (.docx) for the IFAS portal. Because equations are
OMML, any downstream conversion of these files through LibreOffice will drop
every equation silently (gate G-2 in Framework_NotesAudit). The delivery chat line MUST
repeat this warning the FIRST time a given exam project delivers notes, so
the portal team confirms a Word-native path once per exam.

## §4 — STATE AND QUEUES
On delivery the unit moves AUDITED_PASS -> DELIVERED (timestamped).

THREE QUEUES SURVIVE DELIVERY, all read from the unit's audit_summary:
  1. FIGURE_PENDING — an unresolved stem figure keeps its standing re-audit
     trigger (Framework_NotesAudit section 1).
  2. QUARANTINED (v1.2.0) — a question NA could not make solvable from
     in-syllabus notes (Framework_NotesAudit section 4 L-4). It indicates the
     question does not belong to this subtopic or its stem is corrupt, so it
     is checked against Step 5; it is NOT a defect in the delivered notes and
     never appears inside the document.
  3. KEY CORRECTIONS (v1.2.0) — the JUDGEMENT-tier entries of
     audit_summary["key_corrections"], where NA disagreed with a bank key that
     was internally consistent (Framework_NotesAudit section 3A TIER 2). These
     are for human review of the SOURCE data, not of the notes. TIER 1
     corrections are provable from the bank itself and need no review.
A bank refresh (an NB re-run) is a standing trigger to re-audit the affected
units; a re-audit that changes any verdict re-opens the unit to AUDITED_PASS
pending redelivery.

There is no KEY_FLAG queue: owner decision 4a retired it, and
Framework_NotesAudit v3.0.0 section 3A replaced it with the two-tier key
CORRECTION mechanism above — NA now fixes a wrong key rather than queueing it.

---

# END OF Framework_NotesDeliver v1.2.0
