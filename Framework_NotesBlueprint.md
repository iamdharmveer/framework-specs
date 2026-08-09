# Framework_NotesBlueprint v1.1.0 — Notes Pipeline Step NB (Blueprint + SourceMap)
# v1.1.0 — 2026-08-08 — REFINEMENT SUPPORT. The blueprint now carries (a)
#   allowed_question_types, the ordered unique type set read from the Exam
#   Pattern Range tab — HARD STOP if empty — consumed by NC for example/recall
#   typing and by NA gate G-5; (b) explicit unit ordering: units are listed in
#   syllabus order and each unit carries seq_in_topic, the 1-based sequence
#   within its parent Topic, which becomes the document's top-level outline
#   number; (c) optional per-unit prose_ban_exemptions for subjects whose own
#   content requires otherwise-banned tokens (e.g. years in History units).
#   Registry schema advances to notes-registry/1.1 with in-place migration of
#   1.0 files (new fields defaulted; nothing deleted).
# v1.0.0 — 2026-08-08 — INITIAL RELEASE. Codifies the design locked in the
#   2026-08-08 design session and validated end-to-end on the IIT JAM BT
#   Enzyme Kinetics proof-of-concept (37/37 PYQ solvability, 1 convergence
#   iteration). SourceMap is FOLDED INTO this step (no separate trigger).
# [ExamCode] project | Notes Step NB | Exam-agnostic
#
# MINIMUM COMPANION VERSIONS:
#   notes_core.py      >= v1.1 — registry create/load/save + 1.0→1.1
#                                migration, syllabus hashing, unit-code naming,
#                                role/tier assignment tables
#   notes_blueprint.py >= v1.0 — input parsing helpers + blueprint writer
#
# PURPOSE:
#   Build notes_blueprint.json (the complete unit list for one exam, with role
#   tags and depth tiers) and initialise notes_registry.json. This is the ONLY
#   step that reads the syllabus, Exam Pattern xlsx and PYQ Analysis directly;
#   every later step consumes the blueprint.
#
# PIPELINE POSITION (Notes pipeline — independent of the Mock pipeline):
#   Notes Step NB (NotesBlueprint) → THIS SPEC
#   Notes Step NC (NotesCreate)    → 1 subtopic → 1 notes .docx (draft)
#   Notes Step NA (NotesAudit)     → closed-book solvability audit + loop
#   Notes Step ND (NotesDeliver)   → delivery + registry DELIVERED
#
# PREREQUISITE:
#   [ExamCode] project Files MUST contain: (a) official syllabus (pdf/docx —
#   ANY official layout; §2 parsing rules), (b) Exam Pattern xlsx (Overview /
#   Sections / Range tabs; Overview MUST carry a Level field), (c) PYQ Analysis
#   doc with subtopic-wise counts. Sorted PYQ papers are located via §3.

## §1 — SCOPE RULES (locked)
1. CURRENT syllabus is the MASTER FILTER. Out-of-syllabus PYQ subtopics are
   excluded and listed in the blueprint's exclusion report.
2. EVIDENCE EXPANSION (Option B): a PYQ-analysis subtopic absent from the
   syllabus is folded in with role EVIDENCE_ADDED iff it has >= 2 PYQs within
   the LATEST 3 exam years. Otherwise excluded (reported).
3. PYQ subtopic assignment in the sorted-PYQ Subject→Topic→Subtopic headers is
   AUTHORITATIVE. NotesBlueprint never reclassifies a question.

## §2 — INPUT PARSING
S-1 Syllabus: accept pdf or docx in any official layout. Extract the
    Subject→Topic→Subtopic hierarchy; where a syllabus lists prose topics
    without explicit subtopics, the PYQ Analysis subtopic list for that topic
    is adopted as the unit set (provenance recorded per unit as
    "syllabus" | "analysis-adopted").
S-2 Exam Pattern xlsx: read Overview (Total Questions, Types, Marks, Duration,
    Level), Sections (question ranges) and Range (per-range type + marking).
    Level drives depth calibration (§5). Missing Level = HARD STOP.
S-3 PYQ Analysis: read subtopic-wise counts; retain per-subtopic totals and,
    where present, per-year distributions.
S-4 syllabus_sha256 is computed over the raw syllabus file bytes and written
    to the registry. Any later change of hash marks all units STALE for
    incremental re-run (§7).

## §3 — SORTED-PYQ SOURCE RESOLUTION (SourceMap, folded in)
Priority order:
  1. A Drive folder link given in the triggering chat message (chat wins).
  2. A Sources tab in the Exam Pattern xlsx (columns: label, url).
  3. Sorted PYQ .docx files present directly in project Files.
The resolved source list is written into notes_blueprint.json.sources with
per-paper ids/urls so NC and NA never re-resolve.

## §4 — ROLE TAGS (locked vocabulary)
  PYQ_WEIGHTED   — in-syllabus, pyq_count >= 3.
  BRIDGE         — prerequisite unit; full notes even at 0 PYQs. BRIDGE units
                   are declared by the blueprint author (Claude-as-SME) with a
                   one-line justification stored per unit.
  EVIDENCE_ADDED — folded in via §1.2.
  COVERAGE       — in-syllabus, pyq_count 0–2, not BRIDGE; leaner treatment.

## §5 — DEPTH TIERS
  TIER-1: PYQ_WEIGHTED with pyq_count >= 15 ......... full anatomy, 6–15 pp.
  TIER-2: PYQ_WEIGHTED 3–14, or EVIDENCE_ADDED ...... full anatomy, 4–8 pp;
          blocks 5–7 only where PYQ evidence warrants.
  TIER-3: BRIDGE or COVERAGE ........................ blocks 1–4 + 8–10, 2–5 pp.
Level (from S-2) calibrates the register and assumed prerequisites inside a
tier; it never changes the tier boundaries above.

## §6 — OUTPUTS
O-1 notes_blueprint.json — schema in notes_core.py BLUEPRINT_SCHEMA; contains
    exam_code, level, allowed_question_types (ordered unique set from the
    Range tab; HARD STOP if empty), sources, exclusion report, and the full
    unit table (unit_code, names, role, pyq_count, tier, provenance,
    seq_in_topic, optional prose_ban_exemptions).
O-2 notes_registry.json — initialised via notes_core.registry_init(); every
    unit enters state BLUEPRINTED.
O-3 Chat summary — unit counts by role/tier + the exclusion report. Version
    numbers are displayed in CHAT ONLY, never inside delivered documents.

## §7 — INCREMENTAL RE-RUNS
Re-running NotesBlueprint with an unchanged syllabus_sha256 is a no-op merge:
existing unit states are preserved; new units (e.g. new PYQ year added) enter
BLUEPRINTED. A changed hash marks every unit STALE=true (state preserved) and
the chat summary lists the diff. Nothing is deleted automatically.

## §8 — HARD RULES CARRIED FROM THE FRAMEWORK CORE
1. NEVER work from memory for exam-varying values: counts, ranges, marks and
   Level come from the parsed inputs of §2 only.
2. Specs are PROJECT-FIRST; engines are REPO-ONLY (bootstrap-verified).
3. The memory ban is ABSOLUTE for question generation and answer keys. Notes
   CONTENT is SME-generated (see Framework_NotesCreate §3) — that carve-out
   does not extend to this step, which generates no content.

---

# END OF Framework_NotesBlueprint v1.1.0
