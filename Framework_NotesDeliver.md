# Framework_NotesDeliver v1.0.0 — Notes Pipeline Step ND (Delivery)
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
     (n/n SOLVABLE), open queues (FIGURE_PENDING / KEY_FLAG counts).

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
On delivery the unit moves AUDITED_PASS → DELIVERED (timestamped). Open
FIGURE_PENDING or KEY_FLAG queues survive delivery and keep their standing
re-audit triggers (Framework_NotesAudit gate rules: figure pass and mode M-2); a re-audit that changes any
verdict re-opens the unit to AUDITED_PASS pending redelivery.

---

# END OF Framework_NotesDeliver v1.0.0
