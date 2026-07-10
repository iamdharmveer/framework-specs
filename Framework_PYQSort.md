# Framework_PYQSort v1.8 — Universal PYQ Sorter
# [ExamCode] project | Step 3 (PYQSort) | Exam-agnostic
#
# PURPOSE:
#   Take one Row file (.docx, output of Step 1 PYQ Prepare) and re-sort every
#   question into a new .docx grouped hierarchically by Subject → Topic →
#   Subtopic, ordered within each subtopic by date descending, session ascending.
#   The sorted output is the input format that Step 5 (PYQExtract) expects.
#
# REPLACES:
#   TestSeriesSort Tier 1 v10 (SSC CGL Tier 1 specific)
#   TestSeriesSort Tier 2 v3  (SSC CGL Tier 2 specific)
#   This framework is exam-agnostic — same spec for ALL exams.
#
# PIPELINE POSITION:
#   Step 1 PYQ Prepare  → raw exam dump to Row file (.docx)
#   Step 2a PYQ Draft   → syllabus + taxonomy_draft.json + exam_config.json
#   Step 2b PYQ Scan    → discover subtopics from PYQ content
#   Step 2c PYQ Approve → approved Analysis docs + exam_config.json
#   Step 3 PYQ Sort     → THIS SPEC (1 Row file → 1 Sorted PYQ)
#   Step 4 PYQ Count    → fill PYQ counts in Analysis docs (Phase B of PYQAnalyse)
#   Step 5 PYQ Extract  → Sorted PYQ → section_rules.md + manifest + Frequency xlsx
#   Step 6 Mock Blueprint → Analysis docs + Frequency xlsx → blueprint.json
#   Steps 7–11          → Mock test creation pipeline
#
# PREREQUISITE:
#   1. Step 1 must have produced the Row file from raw exam dump.
#   2. Step 2c PYQApprove must have produced approved Analysis docs + exam_config.json.
#   3. Both Analysis docs and exam_config.json must be in [ExamCode] project Files.
#
# INPUTS:
#   1. One Row file (.docx) — uploaded to chat
#   2. Approved Analysis docs — in project knowledge (loaded automatically)
#   3. [ExamCode]_exam_config.json — in project knowledge (loaded automatically)
#
# OUTPUT:
#   One Sorted PYQ .docx file — delivered via present_files.
#   (1 file, nothing else. Deliverable set is CLOSED — see §9 delivery contract.)
#   User downloads → uploads to Google Drive PYQ folder.
#
#   DO NOT DELIVER:
#     ✗ sort_pipeline.py (execution script — stays in /home/claude/)
#     ✗ Any intermediate or working .docx files
#     ✗ Any JSON, .txt, or log files generated during sorting
#     ✗ Input Row file (this is an INPUT, not an output)
#
# TRIGGER FORMAT:
#   Step 3: PYQSort
#   Trigger matching is case-insensitive.
#   ExamCode read from exam_config.json in project knowledge (set during Step 2a PYQDraft).
#
# RUNS IN: [ExamCode] project (exam-specific, where Analysis docs are uploaded)
#
# EXECUTION MODEL: Single script, 4 tool calls maximum. No "Continue" needed.
#   1. create_file  → write complete sort_pipeline.py
#   2. bash_tool    → run it (parse + classify + sort + emit + validate)
#   3. bash_tool    → verify Q-count, heading counts, date-label count
#   4. present_files → deliver
#
# EXAM-AGNOSTIC GUARANTEE:
#   Zero hardcoded exam values. All section names, topic names, subtopic names,
#   subject order, section boundaries, session keyword, page size, question types
#   → read from Analysis docs + exam_config.json.
#   Same spec runs for SSC CGL (4 sections, Q-range, Shift), SSC Tier 2 (5 sections,
#   markers, Shift), GATE (1 section, no session, NAT questions), Banking (Slot),
#   UPSC (Paper), RRB (Phase), or any exam.
#
# STEP 1 FORMAT CONTRACT:
#   PYQSort assumes Row files are produced by Step 1 (PYQ Prepare) in a
#   STANDARDISED format. Step 1 is the normalisation layer — it converts
#   exam-specific raw dumps into this universal format:
#     Date labels:  [DD-Mon-YYYY <session_keyword> <N>] (with session)
#                   [DD-Mon-YYYY] (without session — single-session exams)
#                   session_keyword comes from exam_config.json
#                   Session part is OPTIONAL — Step 1 omits it when not provided
#                   Month abbreviations: always 3-char English (Jan, Feb, ...)
#     Q-numbering:  Q.<N> format (continuous or per-module)
#     Options:      one of the 5 OPT_PATTERNS formats, or none for NAT questions
#   If a Row file violates this contract, PYQSort raises a clear error pointing
#   to Step 1 as the fix location — not a PYQSort bug.
#
# VERSION HISTORY:
#   v1.8 — 2026-07-07 — OPTIONAL SESSION IN DATE LABELS (Step 1 sync).
#           Framework_PYQPrepare v1.0 allows session to be omitted from date labels.
#           (1) build_date_label_re(): session_keyword+number now optional in regex.
#               Old: ^\[DD-Mon-YYYY\s+<keyword>\s+\d+\]$
#               New: ^\[DD-Mon-YYYY(?:\s+<keyword>\s+(\d+))?\]$
#           (2) parse_date_label(): session defaults to 1 when not present in label.
#           (3) CHECK 3: accepts both [DD-Mon-YYYY] and [DD-Mon-YYYY <keyword> N].
#           (4) EC-S10: error message updated to show both date label formats.
#           (5) EC-S15: updated — Step 1 now omits session entirely for single-session
#               exams (no default session=1). parse_date_label defaults to 1.
#           (6) Header + bottom STEP 1 FORMAT CONTRACT updated for optional session.
#           (7) make_output_filename(): handles session-less date labels.
#           Cross-step sync: Framework_PYQPrepare v1.0 §1 S1-3 (date label contract).
#   v1.7 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#           Added post-delivery footer rendering reference to
#           Framework_DeliveryFooter.md v1.3 in §12 DoD POST-DELIVERY block.
#           Zero logic change.
#   v1.6 — 2026-07-06 — CLOSED DELIVERABLE SET CONTRACT.
#           Added closed-set delivery contract to match cross-framework standard
#           (PYQAnalyse §10, MockCreate S13-6). Header OUTPUT now says "(1 file,
#           nothing else)" with explicit DO-NOT-DELIVER list. §9 execution model
#           has a DELIVERABLE SET CONTRACT block with pre-delivery check (exactly
#           1 file, correct path, all validations passed). §12 DoD item 18 added.
#           Low structural risk (single-file deterministic script output), but
#           formalised for consistency after SSC CGL Tier 2 PYQAnalyse failure
#           (unauthorized taxonomy_draft_v2.json delivery) exposed the gap pattern.
#
#   v1.5 — 2026-07-06 — EXAM_CONFIG V2.5 SCHEMA COMPATIBILITY.
#           Step 2a v2.5 expanded exam_config.json with marking_scheme[], level, medium,
#           max_attempt, and question_types. PYQSort does NOT consume these new fields
#           (sorting depends on taxonomy + Q-ranges + session_keyword, not marks or level).
#           Change: S1-3 file inventory printout updated to reflect new schema fields
#           for transparency (shows marking ranges count, level, medium if present).
#           sections[] now includes max_attempt in the loaded schema — PYQSort ignores it
#           (sorting is independent of attempt limits). Zero code logic changes.
#
#   v1.4 — 2026-07-03 — EXAM-AGNOSTIC AUDIT (6 rigidity fixes).
#          (1) DATE_LABEL_RE: replaced hardcoded "Shift" with session_keyword
#              read from exam_config.json. Supports Shift/Slot/Phase/Paper/
#              Session/Morning/Afternoon or any custom keyword. parse_date_label()
#              and Check 3 validation both use the configurable pattern.
#          (2) Check 4 NAT-awareness: exams with NAT questions (answer_type=
#              numerical) have questions with ZERO options. Check 4 now counts
#              only MCQ questions (total − NAT count) for the options threshold.
#              NAT questions are identified by having 0 option paragraphs in
#              their body_elems.
#          (3) Page size: replaced hardcoded US Letter (8.5×11") with page_size
#              from exam_config.json. Default is A4 (8.27×11.69") — the standard
#              for Indian competitive exams. US Letter available via config.
#          (4) EC-S10 softened: missing date label still raises ValueError (it IS
#              a parse failure), but the error message now names Step 1 as the
#              fix location and documents the Step 1 format contract.
#          (5) Sort key shift field documented: for single-session exams, Step 1
#              synthesises session=1, making field 7 a no-op tiebreak. This is
#              correct behaviour, not dead weight.
#          (6) PROOF section expanded: added GATE (1 section, NAT, no session),
#              Banking (multi-slot), UPSC (multi-paper) as covered exam patterns.
#              Added Step 1 format contract as explicit prerequisite.
#   v1.3 — 2026-07-03 — DEEP-RESEARCH AUDIT (14 fixes).
#          (1) Q_PATTERNS drift: patterns 1-2 used `\s` instead of `\s+`,
#              misaligned with Step 5 E-2. Fixed to `\s+` for contract parity.
#          (2) OPT_RE replaced: single `r'^[1-5]\.\s'` replaced with full
#              5-pattern OPT_PATTERNS matching Step 5 E-3 / PYQAnalyse exactly.
#              is_option() function aligned.
#          (3) Taxonomy table parser rewritten: cur_topic_for_table was declared
#              but never used — all subtopics were attributed to the LAST topic.
#              Fixed: table rows now properly track their parent topic via
#              section-topic detection within each table.
#          (4) load_exam_config circular dependency: function required exam_code
#              to find the file containing exam_code. Fixed: glob search for
#              any *_exam_config.json in /mnt/project/.
#          (5) Pipeline position updated: "TestSeriesRow" → "Step 1 PYQ Prepare",
#              Step 4 PYQCount added between PYQSort and PYQExtract, full 11-step
#              pipeline listed.
#          (6) make_output_filename: multi-date case now computes actual earliest
#              and latest dates instead of generic "Multi" placeholder.
#          (7) renumber_stem: extended to handle all Q_PATTERNS formats (Q.N,
#              QN., Question N:, N., (N)) not just Q.N.
#          (8) Month regex aligned: DATE_LABEL_RE changed from `{3,}` to `{3}`
#              to match Check 3 validation exactly.
#          (9) subtopic_idx reset per topic in taxonomy table parser.
#          (10) Check 4 options count: changed from hardcoded 4 to exam_config.
#          (11) Footer version marker added.
#          (12) Section detection fallback: marker_mode mismatch changed from
#               warn-and-fallback to HARD STOP.
#          (13) S3-1 comment corrected.
#          (14) §11 Exam-Agnostic Guarantee updated.
#   v1.2 — 2026-07-03 — DEEP-AUDIT-2 (1 fix). S6-2 sub-section heading still
#          said "STEP 0 E-1 COMPATIBLE" — missed by v1.1 audit. Corrected to
#          "STEP 5 E-1 COMPATIBLE". No code logic changed.
#   v1.1 — 2026-07-03 — DEEP-AUDIT (1 fix). 4 "Step 0" references corrected
#          to "Step 5" (PYQExtract). Step 0 was the old internal name; the
#          canonical pipeline position is Step 5. No code logic changed.
#   v1.0 — Initial release. Derived from TestSeriesSort Tier 1 v10 + Tier 2 v3.
#          Exam-agnostic taxonomy loading. Dual section-detection mode (markers + Q-range).
#          Heading format contract with Step 5 E-1 parser. 13 edge cases.
#          All pipeline mechanics inherited: insert_para, image re-embedding,
#          OMML walker, date label iron rule, 9-check validator.

---

## §1 — SESSION START

### S1-1 — Trigger parsing

```
Trigger: PYQSort
Trigger matching is case-insensitive.

Parse:
  ExamCode : read from exam_config.json in project knowledge.
             The file is discovered by glob (*_exam_config.json), NOT by
             constructing a filename from an already-known exam code.
             If no exam_config found → HARD STOP:
               "No exam_config.json found.
                Run PYQDraft [ExamCode] first, then upload
                Analysis docs + exam_config.json to this project."
```

### S1-2 — Load taxonomy from Analysis docs

```python
import json, os, re, copy, glob
from collections import Counter
from docx import Document

def load_exam_config():
    """
    Load exam_config.json from project knowledge via glob search.
    No exam_code needed — discovers any *_exam_config.json file.
    Returns (exam_code, config_dict) or raises SystemExit.
    """
    matches = sorted(glob.glob('/mnt/project/*_exam_config.json'))
    if not matches:
        raise SystemExit(
            "HARD STOP: No *_exam_config.json found in project knowledge.\n"
            "Run PYQDraft [ExamCode] first, then upload\n"
            "Analysis docs + exam_config.json to this project.")
    if len(matches) > 1:
        raise SystemExit(
            f"HARD STOP: Multiple exam_config.json files found: {matches}\n"
            "Only one exam should be configured per project.")
    config = json.load(open(matches[0], encoding='utf-8'))
    exam_code = config.get('exam_code', os.path.basename(matches[0]).split('_exam_config')[0])
    return exam_code, config

def load_taxonomy_from_analysis_docs():
    """
    Load the COMPLETE taxonomy from ALL Analysis docs in project knowledge.
    Returns: {
      section_name: {
        'subject_order': int,
        'topics': {
          topic_name: {
            'topic_idx': int,
            'subtopics': {
              subtopic_name: {'subtopic_idx': int}
            }
          }
        }
      }
    }
    Also returns: ordered list of (subject, topic, subtopic) triples.
    """
    taxonomy = {}
    triples = []

    # Find all Analysis docs in project
    analysis_files = sorted(glob.glob('/mnt/project/*_PYQ_Analysis_*.docx'))
    if not analysis_files:
        raise SystemExit(
            "HARD STOP: No PYQ Analysis docs found in project knowledge.\n"
            "Upload the approved Analysis docs from PYQApprove.")

    for doc_path in analysis_files:
        doc = Document(doc_path)
        section_name = None
        topics = {}
        cur_topic = None
        topic_idx = -1

        # PASS 1: Parse paragraphs for section name and topic headers
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue

            # Detect section name from header
            if not section_name and 'Subject:' in text:
                section_name = text.split('Subject:')[1].strip()
                continue

            # Detect topic headers: "Topic N: <Name>"
            topic_match = re.match(r'Topic\s+(\d+):\s*(.+)', text)
            if topic_match:
                topic_idx = int(topic_match.group(1)) - 1
                cur_topic = topic_match.group(2).strip()
                topics[cur_topic] = {'topic_idx': topic_idx, 'subtopics': {}}
                continue

        # PASS 2: Parse tables for subtopic extraction
        # Tables follow their parent topic in document order.
        # Track which topic each table belongs to by re-scanning
        # the document structure (paragraphs + tables interleaved).
        cur_topic_for_tables = None
        for child in doc.element.body:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'p':
                # Check if this paragraph is a topic header
                ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
                p_text = ''.join(
                    t.text for t in child.iter(f'{{{ns}}}t') if t.text
                ).strip()
                topic_match = re.match(r'Topic\s+(\d+):\s*(.+)', p_text)
                if topic_match:
                    cur_topic_for_tables = topic_match.group(2).strip()
            elif tag == 'tbl' and cur_topic_for_tables and cur_topic_for_tables in topics:
                # This table belongs to cur_topic_for_tables
                subtopic_idx = len(topics[cur_topic_for_tables]['subtopics'])
                from docx.table import Table as DocxTable
                tbl_obj = DocxTable(child, doc)
                for row in tbl_obj.rows:
                    cells = [c.text.strip() for c in row.cells]
                    if len(cells) >= 2:
                        name = cells[0]
                        # Skip header rows and total rows
                        if name in ('Subtopic', 'Topic', 'GRAND TOTAL', 'TOTAL', ''):
                            continue
                        if name.startswith('Topic '):
                            continue
                        # This is a subtopic row
                        if name not in topics[cur_topic_for_tables]['subtopics']:
                            topics[cur_topic_for_tables]['subtopics'][name] = {
                                'subtopic_idx': subtopic_idx
                            }
                            triples.append((section_name, cur_topic_for_tables, name))
                            subtopic_idx += 1

        if section_name:
            taxonomy[section_name] = {
                'subject_order': len(taxonomy),  # order by file discovery
                'topics': topics
            }

    return taxonomy, triples
```

### S1-3 — File inventory

```
List ALL received files:
  "Received files:
   • [filename].docx  (Row file, [size])

   Project knowledge loaded:
   • [N] Analysis docs ([total] subtopics across [M] subjects)
   • exam_config.json ([ExamCode], [total_questions] questions, [sections] sections)

   Section detection mode: [marker_mode / Q-range]
   Session keyword: [session_keyword] (from exam_config)
   Page size: [page_size] (from exam_config)
   Level: [level] (from exam_config, if present)
   Medium: [medium] (from exam_config, if present)
   Marking ranges: [N] range(s) (from exam_config, if present)"

If Row file missing → "Upload 1 Row file (.docx) and re-trigger PYQSort."
If Analysis docs missing → HARD STOP (see S1-2).
If exam_config missing → HARD STOP (see S1-1).
```

---

## §2 — SECTION DETECTION

### S2-1 — Auto-detect mode

```python
def detect_section_mode(doc, exam_config):
    """
    Auto-detect whether the Row file uses module separators or Q-number ranges.
    Check first 20 paragraphs for === separators.
    """
    for i, para in enumerate(doc.paragraphs[:20]):
        text = para.text.strip()
        if re.match(r'^===\s+.+\s+===$', text):
            return 'marker'

    # No markers found — use Q-range from exam_config
    if exam_config.get('marker_mode', False):
        # Config says markers expected but none found — HARD STOP
        raise SystemExit(
            "HARD STOP: exam_config says marker_mode=true but no === separators\n"
            "found in the first 20 paragraphs of the Row file.\n"
            "Either the wrong file was uploaded, or the Row file format is corrupted.\n"
            "Check the file and re-upload.")
    return 'q_range'
```

### S2-2 — Q-range section assignment

```python
def get_section_by_q_range(q_num, exam_config):
    """
    Determine section from Q-number using exam_config section boundaries.
    Returns section name or None if out of range.
    """
    for sec in exam_config['sections']:
        q_start, q_end = sec['q_range']
        if q_start <= q_num <= q_end:
            return sec['name']
    return None
```

### S2-3 — Marker section assignment

```python
def parse_module_separator(text):
    """
    Parse === Subject Name === separator.
    Returns subject name or None.
    """
    m = re.match(r'^===\s+(.+?)\s+===$', text.strip())
    return m.group(1).strip() if m else None
```

---

## §3 — PARSER (Row File Reading)

### S3-1 — Question extraction

```python
# Q-number detection patterns — ALIGNED WITH Step 5 E-2 (MUST stay in sync)
Q_PATTERNS = [
    r'^Q\.\s*(\d+)\s+',            # Q.1  Q.25  Q. 1  (one or more trailing space)
    r'^Q(\d+)\.\s+',               # Q1.  Q25.  (one or more trailing space)
    r'^Question\s+(\d+)\s*[:.]',   # Question 1:
    r'^(\d+)\.\s+(?!\d)',           # 1.   25.   (negative lookahead: not 1.5)
    r'^\((\d+)\)\s+',              # (1)  (25)
]

def detect_question_start(text):
    for pat in Q_PATTERNS:
        m = re.match(pat, text.strip())
        if m: return int(m.group(1))
    return None

# ═══════════════════════════════════════════════════════════════════
# DATE LABEL DETECTION — CONFIGURABLE SESSION KEYWORD
# ═══════════════════════════════════════════════════════════════════
#
# The session keyword (Shift, Slot, Phase, Paper, Session, etc.) is read
# from exam_config.json at runtime. Step 1 (PYQ Prepare) produces date labels
# using the SAME keyword. The regex is built dynamically.
#
# exam_config.json field:
#   "session_keyword": "Shift"      (SSC CGL, SSC CHSL, SSC MTS)
#   "session_keyword": "Slot"       (IBPS PO, IBPS Clerk, SBI PO)
#   "session_keyword": "Phase"      (RRB NTPC, RRB Group D)
#   "session_keyword": "Paper"      (UPSC CSE, UPSC CAPF)
#   "session_keyword": "Session"    (GATE, CAT)
#   "session_keyword": "Shift"      (default if not specified)
#
# For single-session exams (GATE, UPSC single-paper):
#   Step 1 omits session entirely: [DD-Mon-YYYY]
#   parse_date_label() defaults session to 1 — sort key field 7 is a no-op.
# ═══════════════════════════════════════════════════════════════════

def build_date_label_re(session_keyword):
    """
    Build date label regex dynamically from exam_config session_keyword.
    Session part is OPTIONAL — matches both [DD-Mon-YYYY] and
    [DD-Mon-YYYY <keyword> N] formats.
    """
    return re.compile(
        r'^\[(\d{1,2})-([A-Za-z]{3})-(\d{4})'
        r'(?:\s+' + re.escape(session_keyword) + r'\s+(\d+))?'
        r'\]$'
    )

MONTH_MAP = {
    'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
    'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12
}

def parse_date_label(text, date_label_re):
    """
    Parse [DD-Mon-YYYY <session_keyword> X] or [DD-Mon-YYYY] →
    (year, month, day, session) or None.
    Session defaults to 1 when not present in the label.
    """
    m = date_label_re.match(text.strip())
    if not m: return None
    day = int(m.group(1))
    month = MONTH_MAP.get(m.group(2)[:3].lower(), 0)
    year = int(m.group(3))
    session = int(m.group(4)) if m.group(4) else 1
    return (year, month, day, session)

# Option detection — ALIGNED WITH Step 5 E-3 / PYQAnalyse (MUST stay in sync)
# The (.+) suffix requires actual option text after the label, preventing bare
# labels like "1. " from being treated as options.
OPT_PATTERNS = [
    r'^([1-5])\.\s+(.+)',           # 1. 2. 3. 4. 5.  (up to 5 options)
    r'^([A-Ea-e])\.\s+(.+)',        # A. B. C. D. E.
    r'^\(([1-5])\)\s+(.+)',         # (1) (2) (3) (4) (5)
    r'^\(([A-Ea-e])\)\s+(.+)',      # (A) (B) (C) (D) (E) / (a)(b)(c)(d)(e)
    r'^([A-Ea-e])\)\s+(.+)',        # A) B) C) D) E) / a) b) c) d) e)
]

def is_option(text):
    """Aligned with Step 5's is_option() — same 5 patterns."""
    return any(re.match(p, text.strip()) for p in OPT_PATTERNS)
```

### S3-2 — Full extraction algorithm

```python
def extract_questions(doc, section_mode, exam_config, date_label_re):
    """
    Walk the Row file, extract question blocks.
    Each question = {
      'q_num': int (original),
      'section': str,
      'date_label': str,   # e.g. '[12-Sep-2025 Shift 1]'
      'date_parsed': (year, month, day, session),
      'stem_elem': <w:p> element (deep-copyable),
      'body_elems': [<w:p> or <w:tbl> elements],
      'module': str or None (for marker mode),
      'has_options': bool   # False for NAT questions
    }
    """
    session_keyword = exam_config.get('session_keyword', 'Shift')
    questions = []
    current_module = None
    current_date_label = None
    current_q = None
    body = doc.element.body

    for child in body:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'p':
            text = child.text or ''
            # Reconstruct full text from all <w:t> elements
            NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            runs_text = ''.join(
                t.text for t in child.iter(f'{{{NS}}}t') if t.text
            )
            text = runs_text.strip()

            # Check for module separator (marker mode)
            if section_mode == 'marker':
                mod = parse_module_separator(text)
                if mod:
                    current_module = mod
                    continue

            # Check for date label
            dl = parse_date_label(text, date_label_re)
            if dl:
                current_date_label = text.strip()
                continue

            # Check for question start
            q_num = detect_question_start(text)
            if q_num is not None:
                # Save previous question (and compute has_options)
                if current_q:
                    current_q['has_options'] = _count_options_in_body(current_q['body_elems']) > 0
                    questions.append(current_q)

                # Determine section
                if section_mode == 'marker':
                    section = current_module
                else:
                    section = get_section_by_q_range(q_num, exam_config)

                current_q = {
                    'q_num': q_num,
                    'section': section,
                    'date_label': current_date_label or '',
                    'date_parsed': parse_date_label(current_date_label, date_label_re) if current_date_label else None,
                    'stem_elem': child,
                    'body_elems': [],
                    'module': current_module,
                    'has_options': True  # default, recomputed when next Q starts
                }

                if not current_date_label:
                    raise ValueError(
                        f"Q.{q_num} has no date label. "
                        f"Step 1 (PYQ Prepare) must emit a date label before every "
                        f"question in format: [DD-Mon-YYYY] or [DD-Mon-YYYY {session_keyword} N]. "
                        f"Fix the Row file in Step 1, then re-upload."
                    )
                continue

            # Not a separator, not a date, not a Q start → body element
            if current_q is not None:
                current_q['body_elems'].append(child)

        elif tag == 'tbl':
            # Table element → part of current question body
            if current_q is not None:
                current_q['body_elems'].append(child)

    # Save last question
    if current_q:
        current_q['has_options'] = _count_options_in_body(current_q['body_elems']) > 0
        questions.append(current_q)

    return questions

def _count_options_in_body(body_elems):
    """Count option paragraphs in a question's body elements."""
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    count = 0
    for elem in body_elems:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag != 'p':
            continue
        text = ''.join(t.text for t in elem.iter(f'{{{NS}}}t') if t.text)
        if is_option(text.strip()):
            count += 1
    return count
```

### S3-3 — OMML text extraction (for classification)

```python
MATH_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

def omml_to_text(omath_elem):
    """
    Recursive OMML → linear text renderer for classification.
    Walks <m:f>, <m:sSup>, <m:sSub>, <m:rad>, <m:d>, <m:nary>, <m:eqArr>, <m:r>, <m:t>.
    """
    def recurse(el):
        tag = el.tag.split('}')[-1] if '}' in el.tag else el.tag
        if tag == 'r':
            t = el.find(f'{{{MATH_NS}}}t')
            return (t.text or '') if t is not None else ''
        elif tag == 'f':
            n = el.find(f'{{{MATH_NS}}}num')
            d = el.find(f'{{{MATH_NS}}}den')
            return f'({recurse(n)})/({recurse(d)})' if n is not None and d is not None else '?/?'
        elif tag == 'sSup':
            b = el.find(f'{{{MATH_NS}}}e')
            s = el.find(f'{{{MATH_NS}}}sup')
            return f'{recurse(b)}^{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'sSub':
            b = el.find(f'{{{MATH_NS}}}e')
            s = el.find(f'{{{MATH_NS}}}sub')
            return f'{recurse(b)}_{recurse(s)}' if b is not None and s is not None else '?'
        elif tag == 'rad':
            deg = el.find(f'{{{MATH_NS}}}deg')
            e = el.find(f'{{{MATH_NS}}}e')
            return f'√({recurse(e)})' if e is not None else '√?'
        elif tag == 'd':
            e = el.find(f'{{{MATH_NS}}}e')
            return f'({recurse(e)})' if e is not None else '(?)'
        else:
            return ''.join(recurse(c) for c in el)
    return recurse(omath_elem)

def get_full_stem_text(stem_elem, body_elems):
    """
    Extract complete stem text including OMML formulas.
    Used for classification — not for output (output preserves original XML).
    """
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    parts = []

    for elem in [stem_elem] + body_elems[:3]:  # stem + first 3 body elems
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag != 'p':
            continue
        for child in elem:
            ctag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if ctag == 'r':
                t = child.find(f'{{{NS}}}t')
                if t is not None and t.text:
                    parts.append(t.text)
            elif 'oMath' in child.tag:
                parts.append(omml_to_text(child))

    return ' '.join(parts).strip()
```

---

## §4 — CLASSIFICATION PROTOCOL

### S4-1 — Pre-build classification table

```
Before writing sort_pipeline.py, Claude builds a complete classification table
for ALL questions in the Row file:

  Q.N | Stem summary | Section | Topic | Subtopic

This table is the SINGLE SOURCE OF TRUTH. The CLASSIF dictionary in code
must be copied from this table exactly — never rewritten from memory.

Classification uses:
  1. Universal rules from §4-2 (Rule 1–6)
  2. Taxonomy from approved Analysis docs (loaded in §1-2)
  3. OMML-rendered stem text (from §3-3)
  4. Section assignment (from §2)
```

### S4-2 — Universal classification rules

```
RULE 1 — TOPICAL HOME WINS OVER SOLVE METHOD
  Pick the subtopic whose DOMAIN matches what the question is ABOUT,
  not what technique is USED to solve it.

  Canonical precedents (apply to ALL exams):
    Bank deposits earning interest       → Interest subtopic (not Percentage)
    Discount on marked price + profit    → Discount subtopic (not Profit & Loss)
    Two trains crossing                  → Trains/Speed subtopic (not generic SDT)
    Pipes filling a tank                 → Pipes subtopic (not Time & Work)
    Mixture at different prices          → Mixture subtopic (not Ratio)
    Compound interest multi-period       → CI subtopic (not Percentage)
    Polynomial remainder via factor      → Algebra subtopic (not Number System)
    Full multi-row DI table              → DI/Statistics subtopic
    Small 2-4 row reference table        → classify by arithmetic operation

RULE 2 — THE VERB AT THE END OF THE STEM DECIDES
    "find the ratio"       → Ratio subtopic
    "find the percentage"  → Percentage subtopic
    "find the average"     → Average subtopic
    "find the value of [trig]" → Trigonometry subtopic

RULE 3 — OMML-AWARE CLASSIFICATION IS MANDATORY
    Render OMML math before classifying. Never guess from garbled text.

RULE 4 — SECTION FROM STRUCTURE, NOT CONTENT
    marker_mode → section from === separator
    Q-range mode → section from Q-number range in exam_config
    A maths question in the Reasoning section STAYS in Reasoning.

RULE 5 — CLOSEST FIT FOR UNCLASSIFIABLE QUESTIONS
    If no subtopic fits perfectly → closest match. No flag. Decide and move on.

RULE 6 — IMAGE/FIGURAL QUESTIONS
    Image-only stem → section's spatial/figural subtopic.
    If no figural subtopic exists → most general subtopic in section.
```

### S4-3 — Taxonomy matching algorithm

```python
def classify_question(stem_text, section, taxonomy, options_text=''):
    """
    Classify a question into (topic, subtopic) within its section.
    Uses stem_text (OMML-rendered), section (from structure), and taxonomy.

    Returns: (topic_name, subtopic_name)

    Classification approach:
    1. Get all topics + subtopics for this section from taxonomy
    2. Match stem keywords against subtopic names and known patterns
    3. Apply Rules 1-6 for disambiguation
    4. If no match → closest fit (Rule 5)
    """
    section_taxonomy = taxonomy.get(section, {}).get('topics', {})

    # Build a flat list of (topic, subtopic) candidates
    candidates = []
    for topic, topic_data in section_taxonomy.items():
        for subtopic in topic_data['subtopics']:
            candidates.append((topic, subtopic))

    # Claude classifies the question against these candidates
    # using stem analysis + Rules 1-6
    # Returns the best (topic, subtopic) match
    pass  # Claude's classification judgment applied here
```

### S4-4 — CLASSIF dictionary format

```python
# For Q-range mode (single Q-number namespace):
CLASSIF = {
    1:  ('General Intelligence & Reasoning', 'Analogy', 'General Word Analogy'),
    2:  ('General Intelligence & Reasoning', 'Analogy', 'General Word Analogy'),
    3:  ('General Intelligence & Reasoning', 'Series', 'Letter Group / Cluster Series'),
    # ...
    100: ('English Comprehension', 'Cloze Test', 'Vocabulary-Based Cloze (Appropriate Word)'),
}

# For marker mode (Q-numbers restart per module):
# Key = (module_name, q_num) — 2-tuple for single-paper inputs
# Key = (module_name, date_label, q_num) — 3-tuple for multi-paper inputs
CLASSIF = {
    ('Mathematical Abilities', 1): ('Mathematical Abilities', 'Number Systems', 'Simplification (BODMAS)'),
    ('Mathematical Abilities', 2): ('Mathematical Abilities', 'Fundamental Arithmetical Operations', 'Percentage'),
    # ...
}
```

---

## §5 — SORT ORDER

```
Every question has a sort key composed of 8 fields, compared left-to-right:

  (subject_idx, topic_idx, subtopic_idx, −year, −month, −day, +session, +orig_q_num)

Field definitions:
  subject_idx   : from exam_config.sections[].subject_order (or taxonomy load order)
  topic_idx     : position of topic within its section's Analysis doc
  subtopic_idx  : position of subtopic within its topic's table in Analysis doc
  −year         : from date label                              DESC (newest first)
  −month        : parsed month (Jan=1 … Dec=12)                DESC
  −day          : parsed day-of-month                          DESC
  +session      : parsed session number (Shift/Slot/Phase/etc) ASC (Session 1 before 2)
  +orig_q_num   : original Q-number from Row file              ASC (deterministic tiebreak)

For marker mode: orig_q_num is the per-module Q-number.
For single-session exams: session is always 1 (no-op tiebreak, correct by design).
```

```python
def make_sort_key(q, taxonomy, exam_config):
    """Build 8-field sort key for a classified question."""
    section = q['classified_section']
    topic = q['classified_topic']
    subtopic = q['classified_subtopic']

    sec_data = taxonomy.get(section, {})
    subject_idx = sec_data.get('subject_order', 99)

    topic_data = sec_data.get('topics', {}).get(topic, {})
    topic_idx = topic_data.get('topic_idx', 99)

    subtopic_data = topic_data.get('subtopics', {}).get(subtopic, {})
    subtopic_idx = subtopic_data.get('subtopic_idx', 99)

    dp = q.get('date_parsed')
    if dp:
        year, month, day, session = dp
    else:
        year, month, day, session = 0, 0, 0, 0

    return (
        subject_idx,
        topic_idx,
        subtopic_idx,
        -year,      # DESC
        -month,     # DESC
        -day,       # DESC
        session,    # ASC
        q['q_num']  # ASC
    )
```

---

## §6 — OUTPUT FILE STRUCTURE

### S6-1 — Filename pattern

```python
def make_output_filename(exam_code, questions, session_keyword):
    """
    Build output filename from exam code and date range in questions.
    Single date: [ExamCode]_DD-Mon-YYYY_<session_keyword>-N_Sorted_Q1-QN.docx
    Multi date:  [ExamCode]_DD-Mon-YYYY_to_DD-Mon-YYYY_Sorted_Q1-QN.docx
    """
    dates = set()
    date_label_re = build_date_label_re(session_keyword)
    for q in questions:
        if q.get('date_label'):
            dates.add(q['date_label'])

    total = len(questions)
    if len(dates) == 1:
        dl = list(dates)[0].strip('[]')
        parts = dl.split()
        date_str = parts[0]
        if len(parts) >= 3 and session_keyword in dl:
            session_num = parts[-1]
            return f'{exam_code}_{date_str}_{session_keyword}-{session_num}_Sorted_Q1-Q{total}.docx'
        else:
            return f'{exam_code}_{date_str}_Sorted_Q1-Q{total}.docx'
    else:
        # Multi-date: compute earliest and latest from parsed dates
        parsed = []
        for d in dates:
            p = parse_date_label(d, date_label_re)
            if p:
                parsed.append((p, d.strip('[]')))
        if parsed:
            parsed.sort()
            earliest_str = parsed[0][1].split()[0]   # DD-Mon-YYYY portion
            latest_str = parsed[-1][1].split()[0]
            return f'{exam_code}_{earliest_str}_to_{latest_str}_Sorted_Q1-Q{total}.docx'
        return f'{exam_code}_Multi_Sorted_Q1-Q{total}.docx'
```

### S6-2 — Heading format (STEP 5 E-1 COMPATIBLE — NON-NEGOTIABLE)

```
══════════════════════════════════════════════════════════════════
HEADING FORMAT — EXACT CONTRACT WITH Step 5 parse_taxonomy_level()
══════════════════════════════════════════════════════════════════

LEVEL 1 (Section/Subject):
  Text:    "Subject: <Section Name>"
  Styling: 14pt Bold Navy #003366
  Parser:  re.match(r'Subject:|Domain:', text) → level 1

LEVEL 2 (Topic):
  Text:    "Topic <N>: <Topic Name>"
  N:       1-indexed ABSOLUTE position from Analysis doc (gaps OK, no renumber)
  Styling: 12pt Bold Black #000000
  Parser:  re.match(r'Topic\s+\d+:', text) → level 2

LEVEL 3 (Subtopic):
  Text:    "<Subtopic Name>"  (no prefix)
  Name:    EXACT string from Analysis doc, .strip()-ed
  Styling: 11pt Bold Navy #003366
  Parser:  default → level 3

NOTE: Step 5's parser also supports "Chapter N" as a level 2 heading for
non-SSC exams. PYQSort always EMITS "Topic N:" format. The "Chapter N"
path exists only for backwards compatibility in downstream parsers.

DATE LABEL:
  Text:    "[DD-Mon-YYYY <session_keyword> X]"
  Examples: "[12-Sep-2025 Shift 1]"   (SSC)
            "[15-Jan-2025 Slot 2]"    (Banking)
            "[02-Feb-2025 Session 1]" (GATE)
  Styling: 11pt Bold Navy #003366, Right-aligned
  Always REBUILT from scratch (never cloned from source)
  Always emitted immediately above Q.N stem — zero paragraphs between

ALL headings built as raw OOXML via make_heading_para() + insert_para().
NEVER use doc.add_paragraph() — it breaks when mixed with insert_para().
NEVER set explicit LEFT alignment on headings — leave as None (unset).
```

### S6-3 — OOXML helper functions

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ═══════════════════════════════════════════════════════════════════
# PAGE SIZE — CONFIGURABLE VIA EXAM_CONFIG
# ═══════════════════════════════════════════════════════════════════
#
# exam_config.json field:
#   "page_size": "A4"           (default — 210mm × 297mm — Indian standard)
#   "page_size": "Letter"       (8.5" × 11" — US standard)
#
# All Indian competitive exams default to A4. Override via exam_config only.
# ═══════════════════════════════════════════════════════════════════

PAGE_SIZES = {
    'A4':     (8.27, 11.69),    # 210mm × 297mm — Indian standard
    'Letter': (8.5,  11.0),     # US Letter
}

def get_page_dimensions(exam_config):
    """Return (width_inches, height_inches) from exam_config page_size."""
    size_name = exam_config.get('page_size', 'A4')
    return PAGE_SIZES.get(size_name, PAGE_SIZES['A4'])

def insert_para(doc, elem):
    """Insert element into body BEFORE sectPr so it stays in document flow."""
    body = doc.element.body
    sectPr = body.find(qn('w:sectPr'))
    if sectPr is not None:
        body.insert(list(body).index(sectPr), elem)
    else:
        body.append(elem)

def make_heading_para(text, size_pt, bold, color_hex, space_before_pt, space_after_pt):
    """Build heading as raw OOXML — never use doc.add_paragraph()."""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before_pt * 20)))
    spacing.set(qn('w:after'),  str(int(space_after_pt  * 20)))
    pPr.append(spacing)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Arial'); rFonts.set(qn('w:hAnsi'), 'Arial')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz');   sz.set(qn('w:val'), str(int(size_pt * 2)))
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), str(int(size_pt * 2)))
    rPr.append(sz); rPr.append(szCs)
    if bold:
        rPr.append(OxmlElement('w:b')); rPr.append(OxmlElement('w:bCs'))
    clr = OxmlElement('w:color'); clr.set(qn('w:val'), color_hex)
    rPr.append(clr)
    r.append(rPr)
    t = OxmlElement('w:t'); t.text = text; r.append(t)
    p.append(r)
    return p

def make_date_label_para(date_str):
    """Build date label as raw OOXML — always rebuilt, never cloned."""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'right')
    pPr.append(jc)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Arial'); rFonts.set(qn('w:hAnsi'), 'Arial')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz');   sz.set(qn('w:val'), '22')
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), '22')
    rPr.append(sz); rPr.append(szCs)
    rPr.append(OxmlElement('w:b')); rPr.append(OxmlElement('w:bCs'))
    clr = OxmlElement('w:color'); clr.set(qn('w:val'), '003366')
    rPr.append(clr)
    r.append(rPr)
    t = OxmlElement('w:t'); t.text = date_str; r.append(t)
    p.append(r)
    return p

def make_blank_para():
    """One empty paragraph for inter-question spacing."""
    return OxmlElement('w:p')

def renumber_stem(stem_elem, new_q_num):
    """
    Replace the original Q-number with new_q_num in the stem's first <w:t>.
    Handles all Q_PATTERNS formats:
      Q.N, QN., Question N:, N., (N)
    """
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    RENUMBER_PATTERNS = [
        (r'^(Q\.?\s*)\d+',        r'\g<1>' + str(new_q_num)),    # Q.N / QN
        (r'^(Question\s+)\d+',    r'\g<1>' + str(new_q_num)),    # Question N
        (r'^(\()\d+(\))',         r'\g<1>' + str(new_q_num) + r'\2'),  # (N)
        (r'^(\d+)(\.\s)',         str(new_q_num) + r'\2'),        # N.
    ]
    for t in stem_elem.iter(f'{{{NS}}}t'):
        if not t.text:
            continue
        for pat, repl in RENUMBER_PATTERNS:
            if re.match(pat, t.text):
                t.text = re.sub(pat, repl, t.text, count=1)
                return
```

### S6-4 — Emit loop (IRON RULE — non-negotiable order)

```python
def emit_sorted(out_doc, sorted_questions, taxonomy, src_doc, exam_config):
    """
    Emit all questions in sorted order with Subject/Topic/Subtopic headings.
    """
    from docx.shared import Inches

    # Set page dimensions from exam_config (default A4)
    page_w, page_h = get_page_dimensions(exam_config)
    sec = out_doc.sections[0]
    sec.page_width  = Inches(page_w)
    sec.page_height = Inches(page_h)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1)

    prev_section = prev_topic = prev_subtopic = None
    new_q_num = 0

    for q in sorted_questions:
        section = q['classified_section']
        topic = q['classified_topic']
        subtopic = q['classified_subtopic']

        # Emit Subject heading on section change
        if section != prev_section:
            h = make_heading_para(f'Subject: {section}', 14, True, '003366', 24, 6)
            insert_para(out_doc, h)
            prev_section = section
            prev_topic = None
            prev_subtopic = None

        # Emit Topic heading on topic change
        if topic != prev_topic:
            topic_idx = taxonomy[section]['topics'][topic]['topic_idx'] + 1
            h = make_heading_para(f'Topic {topic_idx}: {topic}', 12, True, '000000', 12, 4)
            insert_para(out_doc, h)
            prev_topic = topic
            prev_subtopic = None

        # Emit Subtopic heading on subtopic change
        if subtopic != prev_subtopic:
            h = make_heading_para(subtopic, 11, True, '003366', 8, 2)
            insert_para(out_doc, h)
            prev_subtopic = subtopic

        # ⛔ IRON RULE — EMIT ORDER IS MANDATORY, NO DEVIATION
        new_q_num += 1

        # Step A — Date label (MANDATORY, always first)
        dl = make_date_label_para(q['date_label'])
        insert_para(out_doc, dl)

        # Step B — Cloned stem (renumbered Q.N)
        stem = copy.deepcopy(q['stem_elem'])
        renumber_stem(stem, new_q_num)
        re_embed_images(stem, src_doc, out_doc)
        insert_para(out_doc, stem)

        # Step C — Cloned body elements (options, tables, images)
        # Strip trailing blank paragraphs first
        body = list(q['body_elems'])
        while body and not (body[-1].text or '').strip():
            ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            has_content = any(True for _ in body[-1].iter(f'{{{ns}}}t'))
            has_table = body[-1].tag.endswith('}tbl') if '}' in body[-1].tag else body[-1].tag == 'tbl'
            if not has_content and not has_table:
                body.pop()
            else:
                break

        for elem in body:
            cloned = copy.deepcopy(elem)
            re_embed_images(cloned, src_doc, out_doc)
            insert_para(out_doc, cloned)

        # Step D — Exactly one blank line
        insert_para(out_doc, make_blank_para())
```

---

## §7 — PIPELINE MECHANICS

### S7-1 — Image re-embedding

```python
def re_embed_images(elem, src_doc, out_doc):
    """
    Re-embed all images in an element with fresh relationship IDs.
    Without this, images silently vanish in the output document.
    """
    DRAW_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    for blip in elem.iter(f'{{{DRAW_NS}}}blip'):
        old_rid = blip.get(f'{{{REL_NS}}}embed')
        if old_rid and old_rid in src_doc.part.rels:
            src_rel = src_doc.part.rels[old_rid]
            new_rid = out_doc.part.relate_to(
                src_rel.target_part, src_rel.reltype
            )
            blip.set(f'{{{REL_NS}}}embed', new_rid)
```

### S7-2 — Orphan option auto-repair

```python
def repair_orphan_options(body_elems):
    """
    At emit time: if an option paragraph has no indent, force Pt(18) left indent.
    Accepts 4 forms: (a) Pt(18) indent, (b) table cell, (c) inline drawing,
    (d) OMML formula.
    Uses is_option() (5-pattern, aligned with Step 5) for detection.
    """
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    for elem in body_elems:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag != 'p':
            continue
        text = ''.join(t.text for t in elem.iter(f'{{{NS}}}t') if t.text)
        if not is_option(text.strip()):
            continue
        # Check if already indented
        pPr = elem.find(f'{{{NS}}}pPr')
        if pPr is not None:
            ind = pPr.find(f'{{{NS}}}ind')
            if ind is not None and ind.get(qn('w:left')):
                continue
        # Force indent
        if pPr is None:
            pPr = OxmlElement('w:pPr')
            elem.insert(0, pPr)
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), '360')  # Pt(18) = 360 twips (1 pt = 20 twips)
        pPr.append(ind)
```

### S7-3 — Non-Latin script preservation

```
Non-Latin text (Hindi/Devanagari, regional scripts) is preserved by
copy.deepcopy() of source XML elements. No font forcing on non-Latin runs.

Acceptable non-Latin fonts:
  Nirmala UI, Mangal, Devanagari Sangam MN, SimSun, SimHei,
  Microsoft YaHei, MS Mincho, MS Gothic, Malgun Gothic, Yu Gothic

Check 1 (validation) accepts these fonts on runs where ord(c) > 0x024F.
```

### S7-4 — Comprehension passage handling

```
RC and Cloze passages: the Row file repeats the full passage above each
sub-question. Preserve this structure exactly — do not deduplicate.
After sorting, sub-questions from the same passage remain consecutive
(same date+session → same sort key cluster).
```

---

## §8 — VALIDATION (9 checks — iterate until ALL PASSED)

```
Every Sorted file must pass all 9 checks before delivery.
session_keyword is read from exam_config.json for Check 3.

CHECK 1 — BODY FONT & TIER SIZES
  All body runs effectively Arial 11pt (with font-inheritance and non-Latin fallback).
  Subject 14pt. Topic 12pt. Subtopic 11pt.
  DI table cells exempted (preserve source font size, typically 9pt).

CHECK 2 — Q-COUNT PARITY
  Input Q-count == Output Q-count strictly. Every question exactly once.
  For marker mode: count per module (Q.1 appears once per module), sum modules.

CHECK 3 — DATE LABEL: PRESENCE, POSITION, FORMAT & STYLING
  HARD FAIL if date-label count ≠ Q-count.
  Every label matches the DYNAMIC pattern built from session_keyword.
  Session part is OPTIONAL — both formats are valid:
    WITH session:    ^\[\d{1,2}-[A-Za-z]{3}-\d{4}\s+<session_keyword>\s+\d+\]$
    WITHOUT session: ^\[\d{1,2}-[A-Za-z]{3}-\d{4}\]$
  The build_date_label_re() regex handles both via optional group.
  Examples:
    SSC:     [18-Jan-2025 Shift 1]
    Banking: [14-Oct-2023 Slot 3]
    GATE:    [09-Feb-2025]          (no session — single-session exam)
    UPSC:    [02-Jun-2024]          (no session)
  Styling: Arial 11pt bold navy #003366, non-italic, right-aligned.
  Position: each label immediately precedes its Q.N stem — zero paragraphs between.

CHECK 4 — OPTIONS INDENTED (NAT-aware)
  For MCQ questions (has_options=True):
    ≥ options_count × mcq_count option paragraphs
    (options_count from exam_config, typically 4 or 5)
  For NAT questions (has_options=False):
    0 option paragraphs expected — exempted from this check.
  mcq_count = total Q-count − nat_count.
  Uses is_option() with all 5 OPT_PATTERNS for detection.
  Accept: (a) Pt(18) indent, (b) table cell, (c) inline drawing, (d) OMML formula.

CHECK 5 — SEQUENTIAL NUMBERING
  Q-lines read Q.1, Q.2 … Q.N in body order. No gaps, no duplicates.

CHECK 6 — SUBTOPIC GROUPING
  Subtopic heading count == number of distinct (Subject, Topic, Subtopic) triples used.
  Every heading under correct parent Topic and Subject.
  Same subtopic name under different Topics is valid (not a violation).

CHECK 7 — TAXONOMY MEMBERSHIP
  Every Subject, Topic, Subtopic heading text exists verbatim in the Analysis docs.

CHECK 8 — SORT ORDER
  Sequence matches (subject_idx ASC, topic_idx ASC, subtopic_idx ASC,
  year DESC, month DESC, day DESC, session ASC, orig_q_num ASC).

CHECK 9 — NO METADATA LEAKAGE
  No paragraphs matching Answer:, Explanation:, Solution:, Question ID,
  Chosen Option, Correct Answer, Section:, === (module separators).
```

---

## §9 — EXECUTION MODEL

```
SINGLE SCRIPT, 4 TOOL CALLS, NO "CONTINUE":

  CALL 1 — create_file: Write complete sort_pipeline.py containing:
    1. Taxonomy dictionary (loaded from Analysis docs)
    2. CLASSIF dictionary (from pre-build classification table)
    3. Parser (Row file → question blocks)
    4. Sorter (8-field sort key)
    5. Emitter (headings + questions via insert_para)
    6. Validator (all 9 checks)
    7. Delivery (shutil.copy2 to /mnt/user-data/outputs/)

  CALL 2 — bash_tool: Run sort_pipeline.py
    → Parse + classify + sort + emit + validate + deliver

  CALL 3 — bash_tool: Verify output
    → Q-count, heading counts, date-label count

  CALL 4 — present_files: Deliver sorted .docx

DELIVERABLE SET CONTRACT (CLOSED):
  The present_files call MUST contain EXACTLY 1 file:
    [ExamCode]_<date-range>_Sorted_Q1-Q<N>.docx
  and NOTHING ELSE. This is an exhaustive, closed list.

  DO NOT include in present_files:
    ✗ sort_pipeline.py (execution script)
    ✗ Any working .docx from /home/claude/work/
    ✗ Any JSON, log, or intermediate files
    ✗ The input Row file

  PRE-DELIVERY CHECK: Before calling present_files, verify:
    1. Exactly 1 file path in the argument list
    2. File is the FINAL_OUT path (/mnt/user-data/outputs/...)
    3. All 9 validation checks PASSED on this file

If script fails: fix and re-run within the 4-call budget.
If validation fails: iterate until PASSED, then deliver.

MANDATORY CLASSIF CROSS-CHECK:
  After writing the CLASSIF dict in sort_pipeline.py, verify every entry
  against the pre-build classification table before executing. Any mismatch →
  fix the code before running. Never rewrite from memory — copy exactly.

INPUT/OUTPUT PATHS:
  INPUT_DOC  = "/mnt/user-data/uploads/<Row-filename>.docx"
  OUT_FILE   = "/home/claude/work/<Sorted-filename>.docx"
  FINAL_OUT  = "/mnt/user-data/outputs/<Sorted-filename>.docx"
```

---

## §10 — EDGE CASES

```
EC-S1: ROW FILE WITH FEWER QUESTIONS THAN EXPECTED
  Some papers may have <100 questions (partial paper, missing section).
  Process whatever is present. Q-count validation targets the actual count,
  not the expected count from exam_config.

EC-S2: MODULE SEPARATOR NOT MATCHING SECTION NAME
  Marker mode: === Subject === text might not exactly match Analysis doc section name.
  Resolution: fuzzy match against taxonomy section names. If ambiguous → classify
  based on question content within that module.

EC-S3: DUPLICATE Q-NUMBERS (marker mode)
  Tier 2 style: Q.1 appears once per module. Parser tracks current_module to
  disambiguate. CLASSIF key = (module_name, q_num).

EC-S4: MULTI-PAPER ROW FILES
  Row file combines questions from multiple dates. Filename uses date range.
  CLASSIF key = (module_name, date_label, q_num) to avoid collisions.
  Detect: if all date labels identical → 2-tuple key; else → 3-tuple key.

EC-S5: IMAGE-ONLY QUESTIONS
  Question stem is an image with no text. Classification uses figural fallback
  subtopic for the section. Image re-embedded via re_embed_images().

EC-S6: OMML FORMULA IN OPTIONS
  Options contain <m:oMath> elements. Accept as valid option form (Check 4 form d).
  Preserve verbatim via deep-copy.

EC-S7: ASSERTION-REASON LONG OPTIONS
  Options like "Both A and R are true and R is the correct explanation of A"
  are valid plain-text options despite length. Do not treat as stem continuation.

EC-S8: MULTI-PARAGRAPH STEMS
  Statement I / Statement II blocks span multiple bold paragraphs after Q.N.
  Detection: bold + not-date + not-option + not-next-Q → stem continuation.
  Include in body_elems in source order.

EC-S9: DI TABLE PRESERVATION
  Tables preserved with original font size (typically 9pt). Do NOT upscale.
  Check 1 exempts table cells from the Arial 11pt requirement.

EC-S10: MISSING DATE LABEL
  If parser finds Q.N without a preceding date label → raise ValueError.
  Error message names Step 1 (PYQ Prepare) as the fix location:
    "Q.{N} has no date label. Step 1 must emit a date label before every
     question in format: [DD-Mon-YYYY] or [DD-Mon-YYYY {session_keyword} N]."
  Step 1 FORMAT CONTRACT: every Row file must have a date label above every
  question. Session part is optional — omitted for single-session exams.

EC-S11: NON-LATIN SCRIPTS (Hindi/Devanagari)
  Preserved by deep-copy. Font fallback accepted in Check 1.
  Classification uses English portion of bilingual stems.

EC-S12: TOPIC NUMBER GAPS
  If paper has questions from Topic 1 and Topic 3 but not Topic 2, headings read
  "Topic 1: ..." and "Topic 3: ..." — gaps in numbering are CORRECT. Do NOT
  renumber topics to close gaps. Topic N uses ABSOLUTE 1-indexed position from
  Analysis doc.

EC-S13: BLANK LINES BETWEEN QUESTIONS
  Strip trailing blank paragraphs from source question block. Emit exactly ONE
  fresh blank paragraph after each question via make_blank_para() + insert_para().
  Do NOT clone source blank — always emit fresh.

EC-S14: NAT QUESTIONS (NO OPTIONS)
  GATE, banking, and some other exams have Numerical Answer Type questions with
  ZERO selectable options — only a stem. These are valid questions.
  Parser sets has_options=False. Check 4 exempts them from options count.
  Classification, sorting, heading emission, and date labels are identical to MCQ.
  The body_elems for NAT questions may include an answer-entry instruction
  paragraph (e.g. "Enter your answer as an integer") — preserve verbatim.

EC-S15: SINGLE-SESSION EXAMS
  GATE, UPSC, state PSC exams have one session per date.
  Step 1 omits session from date label entirely: [DD-Mon-YYYY].
  parse_date_label() defaults session to 1. Sort key field 7 becomes
  a no-op tiebreak. This is correct by design — no special handling
  needed in PYQSort.
```

---

## §11 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL IN THIS SPEC (identical every exam):
  Trigger parsing and file inventory
  Section detection (auto: markers vs Q-range)
  Question extraction (Q patterns, date label patterns, option patterns)
  Date label parsing (dynamic regex from session_keyword)
  Option detection (5-pattern OPT_PATTERNS aligned with Step 5 E-3)
  NAT question handling (has_options flag, Check 4 exemption)
  OMML renderer
  Classification rules 1-6
  Sort key (8 fields)
  Heading format (Step 5 E-1 contract)
  Page size selection (from exam_config, default A4)
  All OOXML helpers (insert_para, make_heading_para, make_date_label_para, etc.)
  Image re-embedding
  Orphan option repair (using 5-pattern is_option)
  Non-Latin script preservation
  9-check validator (with configurable session_keyword and NAT-awareness)
  4-call execution model
  All 15 edge cases

EXAM-SPECIFIC (loaded at runtime from project files):
  Taxonomy (from Analysis docs)
  Section names, topic names, subtopic names (from Analysis docs)
  Subject order (from exam_config.json)
  Section boundaries / marker mode (from exam_config.json)
  Session keyword: Shift/Slot/Phase/Paper/Session (from exam_config.json)
  Page size: A4/Letter (from exam_config.json)
  Options count per question (from exam_config.json)
  Question types: MCQ/NAT/MSQ (from exam_config.json)
  Classification precedents (from question content + universal rules)

PROOF:
  SSC CGL Tier 1: 4 sections, Q-range mode, Shift, 100 Q/paper, all MCQ
  SSC CGL Tier 2: 5 sections, marker mode, Shift, 150 Q/paper, all MCQ
  GATE CS:        1 section,  Q-range mode, Session, 65 Q/paper, MCQ+NAT
  IBPS PO:        5 sections, marker mode, Slot, 100 Q/paper, all MCQ
  UPSC CSE:       2 papers,   Q-range mode, Paper, 100 Q/paper, all MCQ
  Same spec handles all — zero exam-specific code in framework.

STEP 1 FORMAT CONTRACT (prerequisite):
  Step 1 (PYQ Prepare) normalises all exam-specific raw formats into:
    Date labels:  [DD-Mon-YYYY <session_keyword> <N>] (with session)
                  [DD-Mon-YYYY] (without session — single-session exams)
                  Session part is OPTIONAL. PYQSort handles both forms.
    Q-numbering:  Q.<N> (continuous — Step 1 always renumbers continuously)
    Options:      Canonical "N. text" format, or none for NAT
    Month names:  3-char English abbreviations (Jan, Feb, ...)
  PYQSort trusts this contract. Violations are Step 1 bugs, not PYQSort bugs.
```

---

## §12 — DEFINITION OF DONE

```
☐ 1.  All Analysis docs loaded from project knowledge
☐ 2.  exam_config.json loaded and validated
☐ 3.  Session keyword and page size read from exam_config
☐ 4.  Section detection mode determined (markers or Q-range)
☐ 5.  Row file parsed — all questions extracted with date labels
☐ 6.  NAT questions identified (has_options=False)
☐ 7.  OMML rendered for all math-containing stems
☐ 8.  Pre-build classification table completed for all questions
☐ 9.  CLASSIF dictionary matches pre-build table exactly
☐ 10. sort_pipeline.py written with all 7 components
☐ 11. Script executed successfully
☐ 12. All 9 validation checks PASSED
☐ 13. Output Q-count == Input Q-count
☐ 14. All headings present in taxonomy (Check 7)
☐ 15. Sort order verified (Check 8)
☐ 16. No metadata leakage (Check 9)
☐ 17. Sorted .docx delivered via present_files
☐ 18. Deliverable set closed: EXACTLY 1 file in present_files call
       (no scripts, no intermediates, no input files)

POST-DELIVERY:
  User downloads sorted .docx → uploads to Google Drive PYQ folder.
  After ALL papers sorted: run Step 4 PYQCount PYQ: <<Drive link>> to fill
  PYQ counts into Analysis docs.

POST-DELIVERY FOOTER (MANDATORY after present_files):
  Render the standardized visual delivery footer as the LAST element in the response.
  Follow Framework_DeliveryFooter.md for footer type (F2 step-complete — always for
  PYQSort since it has no batches), file badge (Use locally), and next-step reference.
```

---

## §13 — CRITICAL WARNINGS

```
⚠️ NEVER use body.append() — ALWAYS use insert_para()
   body.append() places content after <w:sectPr>, making it invisible.
   This is the #1 most dangerous bug. Every element (headings, date labels,
   stems, options, tables, blanks) MUST use insert_para().

⚠️ NEVER use doc.add_paragraph() for any content
   It conflicts with insert_para() when mixed. Build ALL elements as raw
   OOXML via OxmlElement.

⚠️ ALWAYS use Inches() for page dimensions
   Raw integers (12240, 15840) are DXA values, not EMU. They produce
   a corrupt document with hundreds of micro-pages.

⚠️ ALWAYS re-embed images with fresh rIds
   Without re_embed_images(), images silently vanish. No error, just empty
   space where the image should be.

⚠️ NEVER set explicit LEFT alignment on headings
   Leave alignment as None (unset). Explicit LEFT adds a <w:jc> element
   that should not be there.

⚠️ ALWAYS rebuild date labels from scratch
   Never clone source date label paragraphs. Always use make_date_label_para()
   to ensure consistent styling regardless of source formatting.

⚠️ NEVER skip the date label emit
   If q['date_label'] is empty → raise ValueError. Fix Step 1.
   A missing date label is a Step 1 format violation, not a valid state to skip.

⚠️ Q_PATTERNS and OPT_PATTERNS MUST stay aligned with Step 5 E-2 / E-3
   Any change to pattern lists here MUST be mirrored in Framework_MockTestAnalyse.md
   and Framework_PYQAnalyse.md. Contract violation breaks the entire pipeline.

⚠️ NEVER hardcode exam-specific values (Shift, US Letter, 4 options, etc.)
   ALL exam-varying values come from exam_config.json. If you find yourself
   writing a literal "Shift" or "4" in the code, you are violating the
   exam-agnostic guarantee.
```

---

# END OF Framework_PYQSort v1.8
