# Framework_PYQDraft v1.0 — PYQ Step 2a — Taxonomy Building from Syllabus (§2)
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
## CROSS-FILE SECTION DIRECTORY — all §/S/EC IDs unchanged from Framework_PYQAnalyse v2.29
#### §1 — SESSION START → Framework_PYQCore.md
#### §2 — PHASE 0a: TAXONOMY BUILDING (PYQDraft) → Framework_PYQDraft.md
####      (S2-3 Draft taxonomy generation is HOSTED in Framework_PYQCore.md — universal
####       machinery per §11, executed by both S2-3 [PYQDraft] and S3-6 Refinement [PYQScan])
#### §3 — PHASE 0b: SMART SCAN (PYQScan) → Framework_PYQScan.md
#### §4 — PHASE 0c: ANALYSIS DOC & APPROVAL (PYQApprove) → Framework_PYQApprove.md
#### §5 — PHASE B: COUNT FILLING (PYQCount) → Framework_PYQCount.md
#### §6 — HEADING FORMAT CONTRACT → Framework_PYQCore.md
#### §7 — NAME CONSISTENCY CONTRACT → Framework_PYQCore.md
#### §8 — CLASSIFICATION RULES → Framework_PYQCore.md
#### §9 — EDGE CASES → Framework_PYQCore.md
#### §10 — DELIVERABLE SET CONTRACT → Framework_PYQCore.md
#### §11 — EXAM-AGNOSTIC GUARANTEE → Framework_PYQCore.md
#### §12 — DEFINITION OF DONE → Framework_PYQCore.md
#### Every trigger loads its step file + Framework_PYQCore.md (routes.json). History: CHANGELOG.md

---

## §2 — PHASE 0a: TAXONOMY BUILDING FROM SYLLABUS

### S2-1 — Syllabus extraction

```
Claude reads the Exam Syllabus (any format — image, PDF, .docx, or text).
Extract ALL subject/topic items mentioned.

For each subject listed in the syllabus:
  1. Record subject name EXACTLY as syllabus states it
  2. List every individual topic/item mentioned under that subject
  3. Preserve each item as-is — do NOT merge or group items at this stage
     (S2-3's Topic Integrity Test determines final Topic structure)
  4. v2.17 — PRESERVE THE SYLLABUS'S OWN HIERARCHY. If the syllabus places
     items under intermediate headings, RECORD THOSE HEADINGS. Do NOT flatten
     them away.

GRANULARITY — WHAT COUNTS AS ONE ITEM (v2.17, MANDATORY):

  The old wording ("list every individual topic/item") did not define the unit.
  For CSIR Life Sciences that spans 85 (lettered subsections) to ~700
  (individual concepts) — a ~10x swing that FLIPS the S2-3 ratio guardrail
  between WARN and pass on an IDENTICAL taxonomy. Six of eleven real syllabi
  tested are prose-dense, so the ambiguity governs the majority of items.

  TWO LEVELS ARE RECORDED. Do not pick one and discard the other:

    ENTRY  — the smallest unit carrying its OWN heading, bullet, or
             letter/number label. THIS is a syllabus_item.
             CSIR "A. Photosynthesis" = 1 entry.
             CTET bullet "Remedial Teaching" = 1 entry.
    ATOMIC — a delimiter-separated concept INSIDE an entry (';' preferred,
             else ','). Recorded as a COUNT ONLY, never as separate items.
             "Light harvesting complexes, mechanisms of electron transport,
              photoprotective mechanisms, CO2 fixation" = 1 entry, 4 atomic.

  Never split an entry into multiple items on a delimiter. Splitting inflates
  the item count, breaks 1:1 coverage checking, and makes counts irreproducible
  across sessions — the exact non-determinism the provenance record exists to
  remove.

  WHY BOTH: the inflation guardrail means different things per syllabus style.
    ENUMERATED (entries ARE concepts — CTET, CAT, UGC glossary):
      measure subtopics / ENTRIES, thresholds 2.0x warn / 3.0x hard stop.
      Preserves the MPPSC Botany calibration (336/81 = 4.1x) the thresholds
      were originally set against — verified still HARD STOPs.
    PROSE (a whole section is one entry — JAM Physics, CUET PG Math, GATE, NEET):
      measure subtopics / ATOMIC, thresholds 0.85x warn / 1.0x hard stop.
      Measured against entries instead, 7 of 11 real syllabi HARD STOP as FALSE
      POSITIVES. For prose the failure is INVERTED: a ratio at or above 1.0 means
      one subtopic per concept, i.e. NO grouping happened — MPPSC restated.

  Style is DETECTED, not chosen: median atomic-per-entry <= 1.5 => ENUMERATED,
  else PROSE. Computed per SUBJECT (a syllabus may mix both). Depends only on
  delimiters present in the text, so it is reproducible across sessions.
  See classify_style() / ratio_verdict() in syllabus_provenance.py.

HIERARCHY PRESERVATION (v2.17 — MANDATORY):

  WHY: a syllabus that reads
        Chemistry > Physical Chemistry > Thermodynamics
  already STATES which group the item belongs to. Flattening it to
  (Chemistry, Thermodynamics) discards that fact and forces S2-3 to
  RE-DERIVE by judgment something the source document supplied as data.
  Re-derived facts cannot be verified against anything; recorded facts can.
  This is the same defect class as discarding the subject would be.

  For every item record:
    syllabus_path  : ordered list of headings ABOVE the item, outermost
                     first, verbatim. e.g. ["Chemistry","Physical Chemistry"]
                     For a flat syllabus this is just ["Chemistry"].
    syllabus_group : the IMMEDIATE parent heading below the subject —
                     syllabus_path[1] if it exists, else None.
                     None means the syllabus supplied NO grouping.

  DO NOT INVENT A GROUP. If the syllabus lists items directly under the
  subject with no intermediate heading, syllabus_group is None. Inventing
  one manufactures false ground truth — strictly worse than recording none,
  because downstream checks would then verify against fiction.

  DEEP HIERARCHIES (Subject > Unit > Chapter > item): record the FULL
  path in syllabus_path. syllabus_group is always the immediate child of
  the subject (syllabus_path[1]). Deeper levels are preserved for audit
  but are NOT used for anchoring — which level maps to a taxonomy Topic
  is exam-specific and cannot be assumed.

  ENUMERATIVE HEADINGS ("Unit I", "Part A", "Module 2") are recorded like
  any other heading. Anchoring never compares heading NAMES to topic names,
  only consistency of mapping, so semantically empty labels work fine.

TERMINOLOGY NOTE — "Subject" vs "Section":
  The SYLLABUS defines Subject names (the top-level taxonomy grouping).
  The EXAM PATTERN defines Section names (the OTS paper structure).
  These are independent — see S2-2a "SECTION ≠ SUBJECT" note.
  The taxonomy uses Subject > Topic > Subtopic throughout.
  In the framework code and JSON, the taxonomy key 'section' historically
  refers to the SUBJECT (from syllabus), not the OTS section (from exam
  pattern). This naming is preserved for backward compatibility with all
  downstream steps (PYQSort, PYQExtract, Blueprint, MockCreate, etc.).

S2-3 determines which items become Topics vs Subtopics using the
Topic Integrity Test and 6 Pattern Dimensions.
```

### S2-2 — Exam Pattern extraction

Two paths: S2-2a (xlsx — preferred) and S2-2b (legacy — fallback).

#### S2-2a — XLSX parser (deterministic, preferred)

```python
import pandas as pd
from openpyxl import load_workbook

def parse_exam_pattern_xlsx(xlsx_path, exam_code):
    """
    Parse the standardized 3-tab Exam Pattern xlsx.
    Returns exam_config dict ready for save_exam_config().
    Raises SystemExit on any validation failure.
    """
    wb = load_workbook(xlsx_path)
    required_sheets = {'Overview', 'Sections', 'Range'}
    if not required_sheets.issubset(set(wb.sheetnames)):
        missing = required_sheets - set(wb.sheetnames)
        raise SystemExit(
            f"HARD STOP: Exam Pattern xlsx missing required tab(s): {missing}. "
            f"Expected 3 tabs: Overview, Sections, Range.")

    # ── TAB 1: Overview (key-value, no header row) ────────────────────
    df_ov = pd.read_excel(xlsx_path, sheet_name='Overview', header=None)
    ov = dict(zip(df_ov[0].str.strip(), df_ov[1]))
    # Required fields
    for field in ['Total Questions', 'Medium', 'Question Type',
                  'Total Marks', 'Duration', 'Level']:
        if field not in ov:
            raise SystemExit(
                f"HARD STOP: Overview tab missing required field: '{field}'.")
    total_questions = int(ov['Total Questions'])
    total_marks     = float(ov['Total Marks'])
    medium          = str(ov['Medium']).strip()
    # question_types: comma-separated string → sorted list
    question_types  = sorted(set(
        t.strip() for t in str(ov['Question Type']).split(',')
    ))
    # duration: "180 Min" → 180 (expected format: "<number> Min")
    # Extracts all digits from the string. If duration is in hours,
    # the xlsx must convert to minutes before saving (e.g., "180 Min" not "3 Hours").
    dur_str = str(ov['Duration']).strip()
    time_minutes = int(''.join(c for c in dur_str if c.isdigit()))
    level = str(ov['Level']).strip()

    # ── TAB 2: Sections (table with header row) ──────────────────────
    df_sec = pd.read_excel(xlsx_path, sheet_name='Sections')
    required_cols = {'Section', 'Total Question', 'Question Starts',
                     'Question Ends', 'Max Attempt'}
    if not required_cols.issubset(set(df_sec.columns)):
        missing = required_cols - set(df_sec.columns)
        raise SystemExit(
            f"HARD STOP: Sections tab missing required column(s): {missing}.")
    sections = []
    for idx, row in df_sec.iterrows():
        sections.append({
            'name':        str(row['Section']).strip(),
            'q_count':     int(row['Total Question']),
            'q_range':     [int(row['Question Starts']),
                            int(row['Question Ends'])],
            'max_attempt': int(row['Max Attempt']),
            'subject_order': idx
        })

    # ── TAB 3: Range (table with header row) ─────────────────────────
    df_rng = pd.read_excel(xlsx_path, sheet_name='Range')
    required_cols_r = {'Question Range', 'Question Type',
                       'Correct Marks', 'Negative Marks'}
    if not required_cols_r.issubset(set(df_rng.columns)):
        missing = required_cols_r - set(df_rng.columns)
        raise SystemExit(
            f"HARD STOP: Range tab missing required column(s): {missing}.")
    marking_scheme = []
    for _, row in df_rng.iterrows():
        parts = str(row['Question Range']).split('-')
        rs, re_ = int(parts[0].strip()), int(parts[1].strip())
        marking_scheme.append({
            'q_range':        [rs, re_],
            'question_type':  str(row['Question Type']).strip(),
            'correct_marks':  float(row['Correct Marks']),
            'negative_marks': float(row['Negative Marks'])
        })

    # ── 10 STRUCTURAL VALIDATIONS ────────────────────────────────────
    issues = []

    # V1: Section sum = Total Questions
    sec_sum = sum(s['q_count'] for s in sections)
    if sec_sum != total_questions:
        issues.append(
            f"V1: Sum of section Total Question ({sec_sum}) ≠ "
            f"Overview Total Questions ({total_questions}).")

    # V2: Q_Ends − Q_Starts + 1 == Total Question per section
    for s in sections:
        computed = s['q_range'][1] - s['q_range'][0] + 1
        if computed != s['q_count']:
            issues.append(
                f"V2: Section '{s['name']}': Q{s['q_range'][0]}-"
                f"Q{s['q_range'][1]} = {computed} Qs but "
                f"Total Question = {s['q_count']}.")

    # V3: Section Q-ranges contiguous and non-overlapping
    prev_end = 0
    for s in sections:
        if s['q_range'][0] != prev_end + 1:
            issues.append(
                f"V3: Section '{s['name']}' starts at Q{s['q_range'][0]} "
                f"but previous section ended at Q{prev_end}. "
                f"Expected Q{prev_end + 1}.")
        prev_end = s['q_range'][1]
    if prev_end != total_questions:
        issues.append(
            f"V3: Last section ends at Q{prev_end}, not Q{total_questions}.")

    # V4: Range tab tiles Q.1 through Total Questions completely
    prev_end_r = 0
    for ms in marking_scheme:
        if ms['q_range'][0] != prev_end_r + 1:
            issues.append(
                f"V4: Range {ms['q_range']} starts at Q{ms['q_range'][0]} "
                f"but previous range ended at Q{prev_end_r}.")
        prev_end_r = ms['q_range'][1]
    if prev_end_r != total_questions:
        issues.append(
            f"V4: Last range ends at Q{prev_end_r}, not Q{total_questions}.")

    # V5: All Negative Marks ≤ 0
    for ms in marking_scheme:
        if ms['negative_marks'] > 0:
            issues.append(
                f"V5: Range {ms['q_range']} has positive Negative Marks "
                f"({ms['negative_marks']}). Must be ≤ 0.")

    # V6: Σ(Max Attempt × correct_marks) == Total Marks
    # Build per-Q marks lookup, then compute per-section attempt marks
    marks_by_q = {}
    for ms in marking_scheme:
        for q in range(ms['q_range'][0], ms['q_range'][1] + 1):
            marks_by_q[q] = ms['correct_marks']
    attempt_marks_total = 0.0
    for s in sections:
        sec_total = sum(
            marks_by_q.get(q, 0)
            for q in range(s['q_range'][0], s['q_range'][1] + 1)
        )
        if s['q_count'] == s['max_attempt']:
            attempt_marks_total += sec_total
        else:
            # Proportional (uniform marks within section assumed for
            # attempt-limited sections; exact when all ranges within
            # section have the same correct_marks)
            attempt_marks_total += sec_total * s['max_attempt'] / s['q_count']
    if abs(attempt_marks_total - total_marks) > 0.01:
        issues.append(
            f"V6: Attempt marks ({attempt_marks_total:.2f}) ≠ "
            f"Total Marks ({total_marks}). Check Max Attempt values.")

    # V7: max_attempt must be > 0 and ≤ q_count for every section
    for s in sections:
        if s['max_attempt'] <= 0:
            issues.append(
                f"V7: Section '{s['name']}' has max_attempt={s['max_attempt']}. "
                f"Must be > 0.")
        if s['max_attempt'] > s['q_count']:
            issues.append(
                f"V7: Section '{s['name']}' has max_attempt={s['max_attempt']} > "
                f"q_count={s['q_count']}. Cannot attempt more than total.")

    # V8: question_types from Overview must match distinct types in Range tab
    range_types = sorted(set(ms['question_type'] for ms in marking_scheme))
    if question_types != range_types:
        issues.append(
            f"V8: Overview Question Type {question_types} does not match "
            f"Range tab types {range_types}. Both must list the same set.")

    # V9: correct_marks must be > 0 for every range
    for ms in marking_scheme:
        if ms['correct_marks'] <= 0:
            issues.append(
                f"V9: Range {ms['q_range']} has correct_marks="
                f"{ms['correct_marks']}. Must be > 0.")

    # V10: total_questions and time_minutes must be > 0
    if total_questions <= 0:
        issues.append(f"V10: total_questions={total_questions}. Must be > 0.")
    if time_minutes <= 0:
        issues.append(f"V10: time_minutes={time_minutes}. Must be > 0.")

    if issues:
        msg = "HARD STOP: Exam Pattern xlsx failed validation:\n"
        for i, issue in enumerate(issues, 1):
            msg += f"  {i}. {issue}\n"
        msg += "Fix the xlsx and re-upload."
        raise SystemExit(msg)

    # ── BUILD EXAM_CONFIG ─────────────────────────────────────────────
    exam_config = {
        'exam_code':       exam_code,
        'exam_name':       '',    # filled by Claude from pattern/syllabus context
        'total_questions':  total_questions,
        'total_marks':      total_marks,
        'time_minutes':     time_minutes,
        'medium':           medium,
        'question_types':   question_types,
        'level':            level,
        'marker_mode':      False,   # determined from PYQ structure, not xlsx
        'session_keyword':  'Shift', # default; user may override
        'page_size':        'A4',
        'options_count':    4,       # auto-detected from PYQ at Step 5
        'sections':         sections,
        'marking_scheme':   marking_scheme
    }
    return exam_config
```

```
SECTION ≠ SUBJECT — CRITICAL ARCHITECTURAL NOTE:

  Section names from the Sections tab (e.g., "Part A", "Part B", "Part C" for
  CSIR NET; "General Aptitude", "Biotechnology" for GATE) are ONLINE TEST SERIES
  (OTS) display labels. They define how the test platform presents and organizes
  sections to the student during the exam.

  Section names are NOT Subject names for the taxonomy. The syllabus (provided
  separately in S2-1) defines Subjects, Topics, and Subtopics.

  A single Subject from the syllabus can have questions spanning MULTIPLE sections.
  Example: CSIR NET Life Science — "Cell Biology" questions appear in both Part B
  (Q.21-70, 2 marks) and Part C (Q.71-145, 4 marks).

  Conversely, for exams like SSC CGL, section names happen to align closely with
  subject areas, but the framework still derives subjects from the syllabus — never
  from section names.

  The framework uses section names ONLY for:
    1. Q-range boundaries (which question numbers belong to which section)
    2. Marking scheme linkage (which scoring rules apply to which questions)
    3. Max attempt enforcement (OTS platform concern, not paper generation)
    4. OTS display labels (passed through to the platform as metadata)
```

#### S2-2b — Legacy extraction (AI-interpreted, fallback)

```
Used when exam pattern is provided as image, PDF, .docx, or plain text
(not the standardized xlsx). Claude reads the document and extracts:

  exam_code           : from trigger
  sections            : list of {name, q_count, q_range: [start, end],
                         max_attempt (= q_count if not stated)}
  total_questions     : sum of all section q_counts
  total_marks         : from pattern
  time_minutes        : from pattern
  medium              : from pattern (default: "English")
  question_types      : from pattern (default: ["MCQ"])
  level               : from pattern (default: "Graduation")
  marking_scheme      : inferred from pattern — if a single marks value is stated
                         (e.g., "each question carries 2 marks"), produce one entry
                         covering Q.1 through total_questions. If per-section marks
                         are stated, produce one entry per section. If unclear,
                         ask user.
  marker_mode         : true if exam uses section separators in paper,
                        false if sections determined by Q-number range.
                        If unclear → ask user.

  After extraction, run the same 10 validations (V1-V10) as the xlsx path.
  Any failure → flag to user with specific issue and ask to correct.

  The legacy path produces the SAME exam_config schema as the xlsx path.
  All downstream steps consume exam_config.json identically regardless
  of which input path was used.
```


### S2-3 — Draft taxonomy generation  →  HOSTED IN Framework_PYQCore.md
# The full S2-3 section (Topic Integrity Test, per-entry decision tree Q1/Q2/Q3,
# Unique Domain Property, ratio guardrails, 6 Pattern Dimensions Appendix) is
# hosted in Framework_PYQCore.md because PYQScan S3-6 executes the same machinery
# (§11 EXAM-AGNOSTIC GUARANTEE declares it universal). Read it there and execute
# it HERE, at this position, as part of --taxonomy mode. Content unchanged.


### S2-3e — SYLLABUS MAPPING EMISSION (v2.17, MANDATORY — closes S2-3)

```
S2-3 derives the taxonomy from the syllabus. This step RECORDS HOW.

WHY MANDATORY: Step 2c (PYQApprove) reconciles the taxonomy against the
syllabus (S4-0). It can only do that if the derivation recorded which
taxonomy path(s) each syllabus item became. Without this record, PYQApprove
has no ground truth and must fall back to asking a human an academic
question — the exact defect v2.17 exists to remove.

The mapping is a BY-PRODUCT OF DERIVATION, not a reconstruction after the
fact. Claude MUST record each item's destination AT THE MOMENT it places
that item into the taxonomy. Reconstructing the mapping afterwards by
name-matching re-introduces the guesswork this record exists to eliminate.

EMIT, for every syllabus item identified in S2-1:

  {
    "id":             "SYL-001",          # stable, assigned in S2-1 order
    "subject":        "<verbatim S2-1 subject name>",
    "syllabus_path":  ["Chemistry","Physical Chemistry"],   # S2-1, verbatim
    "syllabus_group": "Physical Chemistry",                 # or null if flat
    "raw_text":       "<verbatim syllabus item text>",
    "enumerated":     true,               # explicitly listed in syllabus
    "source_ref":     "<locator: page/line/bullet, best effort>",
    "mapped_paths":   ["Subject/Topic/Subtopic", ...],
    "deviation":      null                # or {"rule": ..., "reason": ...}
  }

ALSO EMIT the group -> topic mapping (one entry per non-null syllabus group):

  group_topic_map: [
    {"subject": "Chemistry",
     "group":   "Physical Chemistry",
     "mapped_topics": ["Chemistry/Physical Chemistry"]}    # 1..N topics
  ]

  This declares, ONCE per group, which taxonomy Topic(s) that syllabus group
  legitimately became. Items are then anchored THROUGH this declaration.

─────────────────────────────────────────────────────────────────────
CONFORM-OR-DECLARE (v2.17 — the topic-placement anchor)
─────────────────────────────────────────────────────────────────────
S2-3 is EXPECTED to override syllabus grouping — the Topic Integrity Test
exists precisely to split badly-grouped syllabus entries (e.g. a single
"Grammar" heading MUST become separate Topics for distinct question types).
So deviation from the syllabus grouping is NORMAL AND OFTEN CORRECT. It is
NOT an error signal, and MUST NOT be auto-flagged as one — doing so would
fire on exactly the cases the framework is designed to produce.

The rule is therefore CONFORM OR DECLARE, never CONFORM OR FAIL:

  CONFORM  — every mapped_path's Topic appears in group_topic_map for that
             item's (subject, group). Nothing further required.

  DECLARE  — the item lands in a Topic outside its group's declared map.
             LEGAL, but the item MUST carry:
               "deviation": {
                 "rule":   "TOPIC_INTEGRITY_TEST" | "SPLIT" | "MERGE" | "OTHER",
                 "reason": "<one line: why this item left its syllabus group>"
               }

  UNDECLARED DEVIATION → HARD ERROR. This is the only failure mode, and it
  is purely structural: no judgment about whether the placement is CORRECT,
  only whether it was DECLARED. Zero false positives by construction.

WHAT THIS DOES AND DOES NOT ACHIEVE (do not overstate):
  DOES     — makes every departure from the syllabus's own structure
             explicit, recorded, and reviewable. Silent misplacement becomes
             impossible: an item cannot quietly drift to another Topic.
  DOES NOT — verify that a declared deviation is CORRECT. A wrong placement
             with a plausible reason still passes. Declaration converts an
             invisible unbounded risk into a small named list; it does not
             eliminate the risk.

FLAT SYLLABI (syllabus_group is null):
  No grouping was supplied, so there is NOTHING to anchor against. The
  correct Topic is not present in ANY input — not the syllabus, not the exam
  pattern, and not the PYQs (the scan classifies by SUBTOPIC, inheriting the
  parent Topic, so a wrong parent produces no classification error). This is
  an INFORMATION limit, not an engineering gap.
  Handling: skip anchoring for that subject and RECORD it as unanchorable in
  the approval record, so the gap is named rather than silent.

MAPPING RULES:
  1. An item that became its OWN Topic maps to EVERY subtopic under that
     Topic (a Topic is realized by its subtopics — the Topic itself is a
     label, not a leaf).
  2. An item GROUPED under a shared Topic maps to the ONE subtopic that
     represents it (per S2-3 GROUPED ITEMS ARE SUBTOPICS).
  3. An item SPLIT across multiple subtopics maps to ALL of them.
  4. Two items MERGED as genuinely synonymous both map to the SAME single
     path. This is legal and is NOT a duplicate.
  5. mapped_paths MUST be [] if the item genuinely has no taxonomy
     representation. NEVER invent a path to make the list non-empty —
     an empty list is a truthful signal that S4-0 will surface as
     ITEM_UNMAPPED. A fabricated mapping hides data loss permanently.
  6. Path strings MUST be byte-identical to the taxonomy keys/values
     (§7 NAME CONSISTENCY CONTRACT). No re-typing; copy from the taxonomy.

Pass syllabus_subjects and syllabus_items to save_taxonomy_draft() (S2-4).
Run syllabus_provenance.validate_provenance() BEFORE saving. HARD STOP on failure.
It is the ONLY implementation of these checks — do not re-implement it here.
```

```python
# ─────────────────────────────────────────────────────────────────
# S2-3e VALIDATION — SINGLE IMPLEMENTATION (v2.17)
# ─────────────────────────────────────────────────────────────────
# There is exactly ONE implementation of these checks:
#     syllabus_provenance.validate_provenance()
#
# Two spec-embedded duplicates (verify_syllabus_mapping,
# verify_topic_anchoring) were REMOVED here. They parsed paths as
# '/'-delimited STRINGS while build_items() emits LIST paths, so a
# perfectly valid mapping was reported as an UNDECLARED DEVIATION on
# EVERY item of EVERY exam. Two call sites were live simultaneously,
# each using a different implementation.
#
# ANTI-DRIFT (same force as the §D6 detection-logic rule): validation
# logic MUST NOT exist in two places. A second copy does not stay in
# sync — it silently diverges and then contradicts the first.
#
# All path handling is LIST-based end to end. Nothing splits or joins
# a path for comparison; see norm_path() in syllabus_provenance.py.
# ─────────────────────────────────────────────────────────────────
```



### S2-3e-1 — MINIMAL EMISSION FORMAT (v2.17, Issue C — supersedes hand-built records)

```
DO NOT hand-emit the 9-field item records. Emit FOUR fields per item and let
syllabus_provenance.build_items() derive the rest. A field that is DERIVED
cannot be emitted wrong; a field that is TYPED can be.

PER ITEM emit exactly:
  path : ["Chemistry","Physical Chemistry"]      headings ABOVE the item,
                                                 outermost first, verbatim.
                                                 ["Chemistry"] if flat.
  text : "Thermodynamics"                        verbatim item text
  to   : [["Chemistry","Physical Chemistry","Thermodynamics"]]
                                                 destination(s), each a LIST of
                                                 exactly 3 components
  why  : "one line"                              ONLY when a destination leaves
                                                 the item's syllabus group
  rule : TOPIC_INTEGRITY_TEST | SPLIT | MERGE | OTHER   (optional, with `why`)

DERIVED AUTOMATICALLY (never emit these):
  id, subject, syllabus_group, enumerated, deviation{rule,reason}

PATHS ARE LISTS, NEVER STRINGS. This is not stylistic. Real subject names
contain '/' — IIT JAM Biotechnology has "Microbial/Plant/Animal Biotech".
Any '/'-joined path is unparseable in general and produced FALSE ANCHOR
FAILURES on live data. A joined string is REJECTED at build time.

group_topic_map MUST BE DECLARED FROM THE SYLLABUS STRUCTURE — i.e. what each
heading SHOULD become — NOT derived from where items were actually sent.
A DERIVED map makes conform-or-declare CIRCULAR: every item conforms by
construction and the check silently passes any misplacement. This was found by
testing 11 real syllabi: all 11 initially passed anchoring for this reason, not
because the mappings were correct. derive_group_topic_map() therefore refuses to
run without _authorized=True and is for bootstrapping an editable draft ONLY;
validate_provenance(map_is_declared=False) hard-errors.

ALSO emit ONCE (not per item):
  syllabus_style   : classify_style(items) output, per subject. Drives the
                     style-aware C4 inflation check at S4-0. Omitting it makes
                     C4 fall back to the legacy whole-corpus ratio, which
                     false-hard-stops prose syllabi.
  syllabus_total   : integer count of ENTRIES you are about to emit.
                     Compared against what actually arrives — catches silent
                     truncation on long syllabi, the dominant failure mode.
  group_topic_map  : one entry per syllabus group:
                     {"subject":..., "group":..., "mapped_topics":[[subj,topic]]}
                     ~1 line per group (tens), not per item (hundreds).

BATCHING (long syllabi): process in bounded chunks, emitting the running count
after each. Never emit a partial set as if complete — syllabus_total is the
contract that makes truncation detectable rather than silent.
```

```python
# S2-3e EXECUTION (replaces hand-built records)
from syllabus_provenance import (build_items, canonicalize_paths,
                                 validate_provenance, derive_group_topic_map)

items, build_errors = build_items(emissions, group_topic_map)
if build_errors:
    raise AnchoringGateFailure(build_errors)          # S2-3f self-correction

# §7: snap destinations to the taxonomy's exact spelling BEFORE validation
name_fixes = canonicalize_paths(taxonomy, items)

ok, errors, warnings, unanchorable = validate_provenance(
    taxonomy, items, syllabus_subjects, group_topic_map,
    declared_total=syllabus_total)
if not ok:
    raise AnchoringGateFailure(errors)                # S2-3f self-correction

# name_fixes must be PASSED to save_taxonomy_draft — it is not a global:
#   save_taxonomy_draft(taxonomy, exam_config, exam_code, syllabus_subjects,
#                       items, group_topic_map, name_fixes=name_fixes)
```

### S2-3f — GATE FAILURE HANDLING (v2.17, B-FIX — operator never sees a traceback)

```
The S2-3e gate fires on CLAUDE'S OWN output during Step 2a. The operator did
nothing wrong and can do nothing about it. A Python traceback reaching them is
a spec violation of the same class as asking them an academic question: it
puts an unanswerable artifact in front of someone with no means to act.

ON AnchoringGateFailure — SELF-CORRECT, DO NOT ESCALATE:

  ATTEMPT 1 — read each error and fix the CAUSE, not the symptom:
    "UNDECLARED DEVIATION"      -> the item left its syllabus group. Decide:
                                   is the placement CORRECT?
                                     YES -> add deviation {rule, reason}
                                     NO  -> correct mapped_paths instead
                                   Do NOT reflexively add a declaration to
                                   silence the gate — a declaration on a WRONG
                                   placement launders an error into a record
                                   that looks reviewed. Fix the mapping first.
    "no group_topic_map entry"  -> add the missing group -> topic declaration
    "deviation.rule not in..."  -> use TOPIC_INTEGRITY_TEST | SPLIT | MERGE | OTHER
    "empty reason"              -> write a real one-line reason
    "mapped_path not present"   -> the path is a typo or the taxonomy lacks it
    "hierarchy ... inconsistent"-> re-run S2-1 extraction for that subject:
                                   some items got a group, some did not
    Re-run the gate.

  ATTEMPT 2 — if it still fails, re-derive that subject's mapping from S2-3.

  AFTER 2 FAILED ATTEMPTS — stop. Do NOT loop, do NOT save a partial draft,
  and do NOT surface the exception. Print the operator message below.

OPERATOR MESSAGE (plain language, closed set — this is the ONLY form in which
this failure may reach the operator):

  "Step 2a could not complete. The syllabus mapping has an issue I could not
   resolve automatically.

   WHAT HAPPENED:
     [one plain line per error, max 5, jargon removed]

   This is a taxonomy build issue, not something you did, and not something
   you need to evaluate.

   YOUR NEXT ACTION (1 step):
   1. Re-run: PYQDraft [ExamCode]
      If it fails again, report the WHAT HAPPENED lines above."

  No traceback. No field names. No stack. No request to judge anything.

TRANSLATION TABLE (error -> plain line):
  UNDECLARED DEVIATION        -> "A syllabus item was placed under a different
                                  topic than the syllabus lists it under."
  no group_topic_map entry    -> "A syllabus heading has no matching topic."
  mapped_path not present     -> "An item points to a topic that doesn't exist."
  hierarchy ... inconsistent  -> "The syllabus headings were read inconsistently
                                  for one subject."
  deviation rule/reason bad   -> "A recorded change is missing its explanation."
  COUNT MISMATCH              -> "Part of the syllabus was not read — the number
                                  of items does not match what was expected."
  must be a list / joined str -> "A topic location was written in the wrong
                                  format."
  exactly 3 components        -> "A topic location is incomplete."
```

### S2-4 — Taxonomy draft output

```python
import json

class AnchoringGateFailure(Exception):
    """S2-3e gate failure. Caught and self-corrected by Claude (S2-3f).
    Reaches the operator ONLY as the plain-language S2-3f message."""
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__(f"{len(self.errors)} undeclared/invalid mapping(s)")


def save_taxonomy_draft(taxonomy, exam_config, exam_code,
                        syllabus_subjects=None, syllabus_items=None,
                        group_topic_map=None, name_fixes=None):
    """
    v2.17: persists the SYLLABUS PROVENANCE RECORD alongside the derived
    taxonomy. Without it, Step 2c (PYQApprove) has no machine-readable ground
    truth and its reconciliation cannot run (S4-0).

    syllabus_subjects: [str] verbatim subject names exactly as S2-1 recorded.
    syllabus_items:    [{'id','subject','raw_text','enumerated',
                         'source_ref','mapped_paths':[...]}]
      mapped_paths = taxonomy paths ('Section/Topic/Subtopic') realizing this
      item. EMPTY list means the item was dropped -> S4-0 flags ITEM_UNMAPPED.
      Every item S2-3 places into the taxonomy MUST record its path(s) here.
    name_fixes:       output of canonicalize_paths() (§7 spelling corrections).
                      Passed in, NOT a free variable — it is produced by the
                      S2-3e block that runs BEFORE this function.
    group_topic_map:  [{'subject','group','mapped_topics':[...]}] — declares
      which taxonomy Topic(s) each syllabus group legitimately became.
      Required for CONFORM-OR-DECLARE anchoring (S2-3e). Omit ONLY when the
      syllabus supplies no grouping at all (fully flat).
    """
    draft = {
        'exam_code': exam_code,
        'version': 'draft',
        'source': 'syllabus + exam pattern',
        'syllabus_subjects': syllabus_subjects or [],
        'syllabus_items': syllabus_items or [],
        'group_topic_map': group_topic_map or [],
        'sections': {},
        'exam_config': exam_config
    }
    for section, topics in taxonomy.items():
        draft['sections'][section] = {}
        for topic, subtopics in topics.items():
            draft['sections'][section][topic] = subtopics

    # Count totals
    total_subtopics = sum(
        len(subs) for topics in taxonomy.values()
        for subs in topics.values()
    )
    draft['total_subtopics'] = total_subtopics

    # v2.17 provenance gate — surfaces a broken S2-3 mapping immediately
    # rather than 3 steps later at PYQApprove.
    if syllabus_items:
        unmapped = [i['raw_text'] for i in syllabus_items if not i.get('mapped_paths')]
        if unmapped:
            print(f"WARNING: {len(unmapped)} syllabus item(s) have no mapped_paths "
                  f"— these will be flagged ITEM_UNMAPPED at PYQApprove: {unmapped[:5]}")

        # v2.17 CONFORM-OR-DECLARE gate. Runs HERE so an undeclared topic
        # deviation is caught at Step 2a, not discovered at Step 2c or later.
        ok_a, err_a, warn_a, unanchorable = validate_provenance(
            taxonomy, syllabus_items, syllabus_subjects, group_topic_map,
            declared_total=len(syllabus_items))
        if not ok_a:
            # v2.17 (B-FIX): this gate fires during CLAUDE'S OWN Step 2a work,
            # never as a result of anything the operator did. Claude MUST
            # self-correct per S2-3f and re-run. A raw traceback must NEVER be
            # the operator's first contact with this failure — they cannot act
            # on it, and surfacing it recreates the exact "unanswerable prompt"
            # problem v2.17 exists to remove.
            raise AnchoringGateFailure(err_a)
        draft['unanchorable_subjects'] = unanchorable
        draft['name_canonicalizations'] = list(name_fixes or [])
        draft['syllabus_style'] = classify_style(syllabus_items)
        draft['declared_deviations'] = [
            {'id': i['id'], 'subject': i.get('subject'),
             'group': i.get('syllabus_group'), 'deviation': i['deviation']}
            for i in syllabus_items if i.get('deviation')]
        if unanchorable:
            print(f"NOTE: {len(unanchorable)} subject(s) have a FLAT syllabus — "
                  f"topic placement cannot be anchored for: {unanchorable}")

    path = f'/mnt/user-data/outputs/{exam_code}_taxonomy_draft.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(draft, f, indent=2, ensure_ascii=False)
    return path

# Also save exam_config separately (PYQSort needs this)
def save_exam_config(exam_config, exam_code):
    path = f'/mnt/user-data/outputs/{exam_code}_exam_config.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(exam_config, f, indent=2, ensure_ascii=False)
    return path
```

### S2-5 — Exam config schema

```json
{
  "exam_code": "[ExamCode]",
  "exam_name": "[Exam Full Name]",
  "total_questions": 145,
  "total_marks": 200,
  "time_minutes": 180,
  "medium": "English",
  "question_types": ["MCQ"],
  "level": "Post Graduation",
  "marker_mode": false,
  "session_keyword": "Shift",
  "page_size": "A4",
  "options_count": 4,
  "sections": [
    {
      "name": "[Section 1 Name]",
      "q_count": 20,
      "q_range": [1, 20],
      "max_attempt": 15,
      "subject_order": 0
    },
    {
      "name": "[Section 2 Name]",
      "q_count": 50,
      "q_range": [21, 70],
      "max_attempt": 35,
      "subject_order": 1
    },
    {
      "name": "[Section 3 Name]",
      "q_count": 75,
      "q_range": [71, 145],
      "max_attempt": 25,
      "subject_order": 2
    }
  ],
  "marking_scheme": [
    {
      "q_range": [1, 20],
      "question_type": "MCQ",
      "correct_marks": 2,
      "negative_marks": -0.5
    },
    {
      "q_range": [21, 70],
      "question_type": "MCQ",
      "correct_marks": 2,
      "negative_marks": -0.5
    },
    {
      "q_range": [71, 145],
      "question_type": "MCQ",
      "correct_marks": 4,
      "negative_marks": -1.0
    }
  ]
}
```

Field definitions:
  exam_code          : alphanumeric + underscore (from trigger).
  exam_name          : human-readable exam name (from Exam Pattern doc or syllabus).
  total_questions    : sum of all section q_counts.
  total_marks        : maximum marks achievable (accounts for attempt limits).
  time_minutes       : total exam duration in minutes.
  medium             : exam language — "English", "Hindi", "Bilingual", etc.
                       From Overview tab. Step 5 auto-detection validates against this;
                       xlsx value takes priority on conflict.
  question_types     : sorted list of distinct question types across all ranges.
                       e.g., ["MCQ"] or ["MCQ", "MSQ", "NAT"]. Derived from Range tab's
                       Question Type column. Controls which Step 5 extensions activate:
                         ["MCQ"] only → MSQ/NAT dormant.
                         includes "MSQ" → multi_select_allowed = true.
                         includes "NAT" → nat_present = true.
  level              : academic level — "Graduation", "Post Graduation",
                       "Under Graduation", "School". From Overview tab.
                       Step 7 uses for question complexity calibration.
                       Step 9 uses for explanation depth.
  marker_mode        : true if exam uses === separators in PYQ papers, false if
                       sections determined by Q-number range. NOT in xlsx — determined
                       from PYQ structure at scan time; default false.
  session_keyword    : the keyword used in date labels (Shift/Slot/Phase/Paper/Session).
                       NOT in xlsx — read from Exam Pattern context or default "Shift".
                       Step 1 uses this when producing Row files; PYQSort reads it for
                       date parsing.
  page_size          : "A4" (default, Indian standard) or "Letter" (US). PYQSort reads
                       this for output .docx page setup.
  options_count      : default number of options per question (typically 4 or 5).
                       PYQSort reads this for option-count validation. Auto-detected
                       from PYQ at Step 5 (PARAMETER 7).
  sections[]         : per-section structural definitions.
    name             : OTS display label (NOT a Subject name for taxonomy — see S2-2a).
    q_count          : total questions in this section.
    q_range          : [start_inclusive, end_inclusive] Q-number boundaries.
    max_attempt      : max questions student may attempt in this section. The framework
                       generates ALL q_count questions; max_attempt is OTS platform
                       metadata. When max_attempt == q_count, there is no attempt limit.
                       Used ONLY for V6 marks validation:
                       Σ(max_attempt × correct_marks) must equal total_marks.
    subject_order    : 0-based display order.
  marking_scheme[]   : per-range scoring rules. Ordered by q_range start ascending.
    q_range          : [start_inclusive, end_inclusive] — must tile Q.1 through
                       total_questions with no gaps or overlaps (validated by V4).
                       A single section can contain multiple marking_scheme ranges
                       (e.g., GATE Biotechnology: section Q.11-65 has 6 ranges with
                       mixed MCQ/MSQ/NAT and mixed 1-mark/2-mark).
    question_type    : "MCQ", "MSQ", or "NAT" for this range.
    correct_marks    : marks awarded per correct answer. Float (supports 4.75 etc.).
    negative_marks   : penalty per wrong answer. Must be ≤ 0. Float.
                       0 = no negative marking for this range.

  HELPER — get marks/type for a specific question number:
    To find correct_marks for Q.72: scan marking_scheme[] for the entry where
    q_range[0] ≤ 72 ≤ q_range[1] → returns that entry's correct_marks.
    Same for question_type and negative_marks.
    Step 5, 6, 7, 8, 9 use this lookup pattern.

### S2-6 — Delivery and next step

```
TAXONOMY MODE DELIVERY (S10-1 closed set):
  Deliver via present_files: EXACTLY 2 files.
    1. [ExamCode]_taxonomy_draft.json
    2. [ExamCode]_exam_config.json
  No other files. Run S10-2 pre-delivery checklist before present_files.

Deliver taxonomy_draft.json and exam_config.json via present_files.

Print:
  "Phase 0a complete.
   Draft taxonomy: [N] sections, [M] topics, [K] subtopics.
   Syllabus entries: [E]. Ratio: [K/E]× (guardrail: ≤ 3.0×).
   Near-duplicate pairs: [D] (must be 0).

   Exam config:
     Total questions : [total_questions]
     Total marks     : [total_marks]
     Duration        : [time_minutes] min
     Medium          : [medium]
     Question types  : [question_types]
     Level           : [level]
     Sections        : [sections_count] ([section_names])
     Marking ranges  : [marking_scheme_count] range(s)
     Attempt limits  : [Yes/No] ([max_attempt per section if Yes])
     Validations     : V1-V10 PASSED

   NEXT: Upload both files to [ExamCode] project knowledge.
         Then run: PYQScan
         (with Row files uploaded or Drive link provided)"
```

---


---

# END OF Framework_PYQDraft v1.0
