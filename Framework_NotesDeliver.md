# Framework_NotesDeliver v1.1.0 — Notes Pipeline Step ND (Delivery)
# v1.1.0 — 2026-08-10 — POST-DEPLOY REVIEW. (1) ND is the delivery step but never
#   said to present_files its artifacts and rendered no footer — so on mobile the
#   delivered files were unreachable and the Framework_DeliveryFooter contract was
#   unmet. §1 now present_files the notes .docx + audit report and renders the F2
#   step-complete footer (4-cell NOTES bar "4 of 4"; Framework_DeliveryFooter
#   v1.18 §3 ND entry). (2) Removed stale references the NA v2.0.0 changes left
#   behind: KEY_FLAG is retired (NA owner decision 4a) and answer-mode "M-2" is
#   gone (NA runs permanent ground-truth mode). Companion: notes_core >= v1.0.
# v1.0.0 — 2026-08-08 — INITIAL RELEASE.
# [ExamCode] project | Notes Step ND | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py >= v1.0 — registry transitions, naming assertion
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

## §1 — DELIVERABLES
  1. The notes .docx, filename per rule F-1 in Framework_NotesCreate, byte-identical to the
     audited artifact (delivery never edits content).
  2. The audit report for that unit (markdown), same basename + _Audit.
  3. A chat delivery line per unit: unit code, notes_version, verdict summary
     (n/n SOLVABLE), open FIGURE_PENDING count (KEY_FLAG is retired — NotesAudit
     owner decision 4a).
  4. present_files BOTH artifacts (the .docx and the _Audit.md) so the operator
     can download them, then RENDER THE F2 STEP-COMPLETE FOOTER as the LAST element
     of the response (Framework_DeliveryFooter §4-1, the 4-cell NOTES pipeline bar
     "4 of 4", header "Step ND · NotesDeliver"). The footer is obligatory after a
     present_files call (§4-0 R1) and NEVER omitted. Next callout: NC — NotesCreate
     for the next subtopic, or "Notes pipeline complete" when every blueprinted
     unit is DELIVERED.

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
On delivery the unit moves AUDITED_PASS → DELIVERED (timestamped). An open
FIGURE_PENDING item survives delivery and keeps its standing re-audit trigger
(Framework_NotesAudit §1 figure handling; NA runs permanent ground-truth mode,
§3); a re-audit that changes any verdict re-opens the unit to AUDITED_PASS pending
redelivery. (There is no KEY_FLAG queue — retired, NA owner decision 4a.)

---

# END OF Framework_NotesDeliver v1.1.0
