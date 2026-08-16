# Framework_PYQScan v1.2 — PYQ Step 2b — Smart Scan for Subtopic Discovery (§3)
# v1.2 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION (D5).
#   collect_row_files() was `files = []` … `pass  # Drive MCP calls` … `return files`:
#   it returned an EMPTY LIST unconditionally, on every run of every exam, and its own
#   comment cited "the same pattern as Step 5's S1-2 Drive path" — inheriting a pattern
#   that was itself dead. Invisible to C6 twice over: the `pass` shares its body with
#   other statements so it is not a pass-bodied stub, and it carried no CLASS tag. The
#   listing now delegates to corpus_io.collect_corpus_files over a PHASE A cache keyed
#   by folder id, and an empty result HARD STOPS with a transport diagnosis (EC-P39)
#   instead of silently reporting a Row-file-less exam.
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
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_PYQScan.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

---

## §3 — PHASE 0b: SMART SCAN FOR SUBTOPIC DISCOVERY

### S3-1 — Scan initialisation

```python
import json, os, re
from collections import Counter

BATCH_SIZE = 3  # papers per batch — default, same as Step 5
                # May be reduced to 2 for very large taxonomies (EC-P15: 500+ subtopics)
                # to fit classification context within Claude's context window.
CONVERGENCE_CONSECUTIVE = 7    # raised from 3 (v1.4) — 21 papers, not 9
MIN_COVERAGE_RATIO = 0.30      # 30% of total papers — ABSOLUTE MINIMUM
SMALL_CORPUS_THRESHOLD = 20    # below this: scan ALL papers, no convergence shortcut

def load_taxonomy_draft(exam_code):
    """Load taxonomy draft from project knowledge or uploads."""
    for base in ['/mnt/project/', '/mnt/user-data/uploads/']:
        path = f'{base}{exam_code}_taxonomy_draft.json'
        if os.path.exists(path):
            return json.load(open(path, encoding='utf-8'))
    return None

def load_scan_progress(exam_code):
    """Load scan progress for resume across sessions."""
    for base in ['/mnt/project/', '/mnt/user-data/uploads/']:
        path = f'{base}{exam_code}_scan_progress.json'
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            # v1.7: Schema version enforcement (Issue 20)
            sv = data.get('_meta', {}).get('schema_version')
            if sv != '2.0':
                raise ValueError(
                    f"scan_progress.json schema_version is {sv}, expected 2.0. "
                    f"Re-run PYQScan from scratch."
                )
            return data
    return None

def load_count_progress(exam_code):
    """Load count progress for resume across sessions.
    Restores counts_by_year keys from string repr back to tuples."""
    for base in ['/mnt/project/', '/mnt/user-data/uploads/']:
        path = f'{base}{exam_code}_count_progress.json'
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            # v1.1 FIX: restore tuple keys from JSON string representation.
            # JSON serialises tuple keys as their repr string, e.g.
            # "('Section', 'Topic', 'Subtopic')". Restore to actual tuples
            # so Counter lookups work with (section, topic, subtopic) keys.
            if 'counts_by_year' in data:
                import ast
                restored = {}
                for k, v in data['counts_by_year'].items():
                    try:
                        restored[ast.literal_eval(k)] = v
                    except (ValueError, SyntaxError):
                        restored[k] = v  # keep as-is if not a tuple repr
                data['counts_by_year'] = restored
            return data
    return None

def init_scan_progress(exam_code, taxonomy_draft):
    """Initialize scan_progress.json from taxonomy_draft.json.
    TAXONOMY AUTHORITY CHAIN (v1.7):
      Step 2a creates taxonomy_draft.json → uploaded to project knowledge.
      Step 2b modifies taxonomy IN scan_progress.json (not taxonomy_draft.json).
      Step 2c (PYQApprove) reads taxonomy FROM scan_progress.json.
      taxonomy_draft.json is NEVER modified after Step 2a.
      The authoritative taxonomy after scanning = scan_progress.json['taxonomy'].
    """
    total_subtopics = sum(
        len(subs) for topics in taxonomy_draft['sections'].values()
        for subs in topics.values()
    )
    return {
        '_meta': {
            'exam_code': exam_code,
            'phase': '0b_scan',
            'schema_version': '2.0',
            'source_taxonomy': 'taxonomy_draft.json',
            'source_taxonomy_subtopics': total_subtopics,
            'papers_scanned': 0,
            'total_available': 0,
            'years_covered': [],
            'convergence_status': 'in_progress',
            'consecutive_empty_batches': 0,
            'refinement_pass_done': False,
            'last_updated': None
        },
        'taxonomy': taxonomy_draft['sections'],  # FULL COPY — not delta
        'exam_config': taxonomy_draft['exam_config'],
        'papers_scanned_list': [],
        'discovery_log': [],
        'drive_file_inventory': []
        # v1.7: Per-question classifications stored in SEPARATE FILE
        # [ExamCode]_classifications.json — NOT in this file.
        # See S3-8 CLASSIFICATION STORAGE STRATEGY for details.
    }
```

```
TAXONOMY AUTHORITY CHAIN:
  taxonomy_draft.json (Step 2a) → FULL COPY into scan_progress.json['taxonomy']
  Step 2b modifies ONLY scan_progress.json['taxonomy'] (adds discoveries).
  taxonomy_draft.json is NEVER modified after Step 2a.
  Step 2c (PYQApprove) reads taxonomy FROM scan_progress.json['taxonomy'].
  scan_progress.json['taxonomy'] MUST contain the COMPLETE taxonomy —
  original from taxonomy_draft.json PLUS all scan discoveries. It is NOT
  a delta/additions-only field.

CLASSIFICATION STORAGE STRATEGY (v1.7):
  Per-question classifications are stored in a SEPARATE file:
    [ExamCode]_classifications.json
  NOT in scan_progress.json (which would grow to 6000+ records for large corpora).
  scan_progress.json contains: _meta, taxonomy, discovery_log, papers_scanned_list,
    drive_file_inventory.
  classifications.json contains: { paper_id: [ {q_num, section, topic, subtopic,
    question_task, question_format, question_direction, thematic_domain}, ... ] }
  Classifications file is cumulative — appended per batch, saved alongside
  scan_progress.json.
  Refinement pass reads the classifications file.
```

### S3-2 — Paper collection and round-robin ordering

```
═══════════════════════════════════════════════════════════════════════
BY DESIGN — THE SCAN DOES NOT SEE IMAGES OR OMML, AND THAT IS CORRECT
(v2.21 banner. S3-2 behaviour, EC-P24 and EC-P25 are UNCHANGED.)
═══════════════════════════════════════════════════════════════════════
Framework_MockTestAnalyse v2.29, Framework_PYQSort v1.12 and corpus_io made
image loss a HARD STOP everywhere images MATTER. A reader arriving from that
work will notice that Step 2b reads text only — no image extraction, no
image-count gate, OMML often reduced to placeholders — and could reasonably
conclude Step 2b has the same defect and "fix" it. It does not. Do not add
image extraction or an image gate here.

WHY IT IS CORRECT:
  * The scan's ONLY job is discovering SUBTOPIC NAMES to extend the draft
    taxonomy. It is explicitly lightweight — 80%+ accuracy is sufficient.
  * Figural subtopics do NOT come from the scan. They come from Step 2a's
    syllabus-faithful derivation, so a figural question the scan misreads
    cannot remove a subtopic that already exists (EC-P24).
  * PYQSort (Step 3) reclassifies every question with FULL python-docx image
    and OMML access, and Step 5 extracts the format distribution from that.
    Nothing downstream inherits a scan-level format judgement.
  * The scan never counts. Counts come from Phase B (§5) against sorted files.

WHERE IMAGE INTEGRITY IS ENFORCED, AND WHY NOT HERE:
  Step 3 PYQSort  S7-5/S7-6/S7-7 + CHECK 10 — images are re-embedded there,
                  so that is where loss can occur and where it is gated.
  Step 5 PYQExtract IMG-1..IMG-6 — the format distribution that drives Step 7
                  generation is derived there, so a missed figure corrupts it.
  Step 2b (here)  neither produces nor consumes a figure. There is nothing to
                  gate. A gate here would fail every text-extracted paper for
                  a condition that is the intended operating mode.

WHAT WOULD MAKE THIS WRONG: if the scan ever began deriving question FORMAT,
counting questions, or feeding anything other than subtopic names forward.
None of those is true today. Revisit this banner if any of them changes.
```

```
FILE READING METHOD (v1.7):
  For Drive-sourced papers, use Google Drive:read_file_content for text extraction.
  This provides question stems and options but OMML formulas may render as
  placeholders and images will be absent.

  OMML HANDLING DURING SCAN:
    If a question stem is blank or contains only option numbers after
    read_file_content extraction, classify using:
      (a) Q-number position (which section it falls in)
      (b) Option content to infer section:
          - Mathematical expressions / numbers → quantitative / numerical section
          - Verbal / textual content → language / comprehension section
          - Domain-specific terminology → relevant domain section
          Use exam_config.sections to match inferred section type to actual names.
      (c) Surrounding question context
    Log: "OMML-obscured" in question_format field of classification.

  FIGURAL QUESTION HANDLING DURING SCAN:
    If question references a figure but no image is visible in text:
      (a) Classify under the section's figural/spatial subtopic (RULE 6)
      (b) Use stem text clues: "mirror image", "paper folding", "Venn diagram",
          "count triangles", "embedded figure", "dice" → map to known subtopic
    Log: "figure-inferred" in question_format field.

  FULL OMML/IMAGE PARSING IS NOT REQUIRED FOR SCAN.
  Scan classification is LIGHTWEIGHT — 80%+ accuracy is sufficient.
  PYQSort (Phase A) performs FULL parsing with python-docx for final classification.

DRIVE RATE LIMIT HANDLING:
  If Drive read_file_content fails with a rate-limit or timeout:
    Wait 5 seconds and retry once.
    If second attempt fails: save progress, end session, resume later.
    Log the failure in discovery_log for debugging.

DRIVE FILE INVENTORY CACHING (v1.7, updated v2.3):
  On first session: list all files from Drive → store in
  scan_progress.json['drive_file_inventory'] as:
    [{"name": "filename.docx", "id": "driveId", "year": 2025, "size": 50629,
      "q_count": 100, "q_count_method": "parsed"}, ...]

  q_count / q_count_method are MANDATORY (GAP-2026-08-15-BAREQ, R-5).
    q_count        : the per-file question count this gate just computed
    q_count_method : "parsed"   — counted by bc.detect_question_start over the docx
                     "filename" — inferred from a Q-range in the filename because the
                                  file could not be read; NOT usable for reconciliation
  Until 2026-08-15 this gate computed a ✓-verified per-file count, DISPLAYED it, and
  threw it away. The one number that would have caught GAP-2026-08-15-BAREQ in two
  seconds — 56 parsed against 60 classified on IIT_JAM_MATHEMATICS 12-Feb-2017 —
  existed, was correct, and was discarded before anything could compare it. A count
  that is not persisted cannot reconcile anything, and "MANDATORY GATE" in the heading
  above does not make it so. Persist it.
  On RESUME sessions: RE-LIST from Drive (do NOT rely on cached inventory).
  See S3-7 RESUME PROTOCOL for full details. Files may have been added or
  removed between sessions — cached inventory could be stale.
  The fresh listing replaces drive_file_inventory in scan_progress.json.
```

### S3-3b — FORMAT AUTHORITY RECONCILIATION (v2.14 — register D6-11)

```
The scan (S3-3) is LIGHTWEIGHT (~80% accurate) and, on OMML math / figural questions,
records PROVISIONAL question_format tokens like "OMML-obscured" and "figure-inferred".
PYQSort Phase A does the FULL python-docx parse and is the AUTHORITY. Without reconciling
the two, a provisional/wrong scan format can silently drive the wrong Format column →
wrong CONCEPT_GROUP / SUBTOPIC_CLASS / passage_present / figural_present / di_present
downstream (Steps 5–7), so a math or figural item can be generated in the wrong form.

RULE (D6-11): before the Format column is finalised, reconcile every question's scan
question_format against its authoritative full-parse format with reconcile_format():
  • the authoritative (clean) full-parse format ALWAYS wins when present;
  • a differing scan value is 'corrected' (logged for review), not silently kept;
  • if the authority is absent, a clean scan value is used ('scan-only'); a provisional
    placeholder with no authority is 'unresolved' → defaults to TEXT and is flagged.
Aggregate with reconcile_stats(): if > 20% of questions were corrected/unresolved, the
scan or the parse has a quality problem — surface it at S-QV rather than shipping silently.
```

```python
# D6-11: reconcile the LIGHTWEIGHT scan question_format against the AUTHORITATIVE
# full python-docx parse (PYQSort Phase A). Scan is ~80% accurate on OMML/figural;
# the full parse wins, and disagreements are surfaced (not silently propagated to
# CONCEPT_GROUP / SUBTOPIC_CLASS / format flags downstream). Pure & deterministic.

_CLEAN = {'TEXT','FIGURAL','PASSAGE','DI'}
# map provisional/scan tokens -> a clean format (best-guess for when the authority is absent)
_SCAN_MAP = {
    'figure':'FIGURAL', 'figure-inferred':'FIGURAL', 'figural':'FIGURAL',
    'omml-obscured':'TEXT',            # math with obscured stem — text unless authority says else
    'word_list':'TEXT', 'number_set':'TEXT', 'text':'TEXT',
    'passage':'PASSAGE', 'rc':'PASSAGE',
    'di':'DI', 'data_interpretation':'DI', 'table':'DI',
}
_PLACEHOLDER = {'omml-obscured','figure-inferred','','none', None}

def _norm(f):
    if f is None: return None
    f=str(f).strip()
    return f.upper() if f.upper() in _CLEAN else f.lower()

def reconcile_format(scan_fmt, authoritative_fmt):
    """Return (final_format, status). status ∈
       {'confirmed','corrected','scan-only','unresolved'}.
       - authoritative (clean full-parse) format ALWAYS wins when present.
       - 'corrected' when it overrides a differing scan value → log for review.
       - 'scan-only' when authority absent but scan gave a usable value.
       - 'unresolved' when neither yields a clean format (WARN; default TEXT)."""
    a = _norm(authoritative_fmt)
    s = _norm(scan_fmt)
    scan_clean = s if s in _CLEAN else _SCAN_MAP.get(s)
    if a in _CLEAN:
        return (a, 'confirmed' if scan_clean == a else 'corrected')
    # authority absent / non-clean
    if scan_clean in _CLEAN:
        was_placeholder = (scan_fmt in _PLACEHOLDER) or (s in _PLACEHOLDER)
        return (scan_clean, 'scan-only' if not was_placeholder else 'unresolved')
    return ('TEXT', 'unresolved')

def reconcile_stats(pairs):
    """pairs: list of (scan_fmt, authoritative_fmt). Returns per-status counts +
    a WARN flag if the corrected/unresolved rate is high (scan quality problem)."""
    from collections import Counter
    st = Counter()
    for scan,auth in pairs:
        st[reconcile_format(scan,auth)[1]] += 1
    total = sum(st.values()) or 1
    bad = st['corrected'] + st['unresolved']
    return {'counts': dict(st), 'total': total,
            'corrected_pct': round(100*bad/total, 1),
            'flag': bad/total > 0.20}   # >20% mismatch → scan/parse quality review
```

```python
import json
import corpus_io                 # I/O shell — Drive listing, screening, pagination

ROW_LISTING_CACHE = '/home/claude/row_drive_listing.json'


def collect_row_files(drive_folder_id, cached_inventory=None):
    """
    Collect all Row file paths, grouped by year, from Google Drive.
    v2.16: DRIVE-ONLY — the local /mnt/user-data/uploads/ fallback was REMOVED to
    standardize with Step 4 (PYQCount), which has always required Drive with no
    fallback (see S1-1's PYQCount PYQ: parameter). Row files via chat upload are
    no longer accepted for --scan mode; PYQ: <<Drive link>> is a required trigger
    parameter.
    cached_inventory: from scan_progress.json['drive_file_inventory']
                      Used ONLY on first session if already cached.
                      Resume sessions re-list from Drive (v2.3 — see S3-7).
    Returns: list of {name, path_or_id, source, year} sorted for round-robin.
    """
    # v2.3: On resume, caller passes cached_inventory=None to force re-listing.
    # On first session, caller may pass cached_inventory if available.
    if cached_inventory and len(cached_inventory) > 0:
        return cached_inventory

    if not drive_folder_id:
        raise SystemExit(
            "HARD STOP: PYQScan requires PYQ: <<Google Drive folder link>>. Row "
            "files must be in Google Drive — the local upload fallback was removed "
            "(v2.16) to match Step 4 (PYQCount). Provide the Drive link and retry.")

    # v1.2 (GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION). This block used to read:
    #     files = []
    #     pass  # Drive MCP calls
    # `files` was initialised empty, the `pass` performed nothing, and the function
    # returned [] UNCONDITIONALLY on every run of every exam. It carried the comment
    # "same pattern as Step 5's S1-2 Drive path" — an explicit inheritance of a
    # pattern that was itself defective. No auditor could see it: the `pass` sits in a
    # body with other statements, so it is not a pass-bodied stub and C6 cannot anchor
    # on it, and it carried no CLASS tag so C6's tagging case could not fire either.
    #
    # Fixed in the same wave as Step 5, deliberately. The gap report recommended a
    # separate ticket; deferring a known-dead listing to a later ticket is precisely
    # the partial remediation that produced this GAP in the first place.
    #
    # PHASE A (model, in its own turns, BEFORE this runs): call
    # Google Drive:search_files(query="parentId = '<folder_id>'", pageSize=100),
    # paginate to exhaustion, recurse into every sub-folder, merge each folder's pages
    # into one {"files": [...]} and cache it under that folder's OWN id — a flat cache
    # that ignores folder_id makes the recursive walk re-enter the sub-folder and raise
    # a spurious DuplicatePaperError. Write it to ROW_LISTING_CACHE.
    #
    # PHASE B (python): a plain lookup over that cache. No tool call happens here.
    with open(ROW_LISTING_CACHE, encoding='utf-8') as _fh:
        _cached = json.load(_fh)
    if isinstance(_cached, dict) and 'files' in _cached:
        _cached = {drive_folder_id: _cached}          # flat cache: root folder only
    def _list_fn(fid, page_token=None):
        if page_token:
            return {'files': []}                 # PHASE A merged every page already
        return _cached.get(fid, {'files': []})

    # corpus_io owns the walk: pagination to exhaustion, newest-first recursion,
    # bc.screen_drive_entry on every entry, DuplicatePaperError on canonical-identity
    # collisions, and the 'files'/'items'/bare-list plus 'title'/'name' normalisation
    # this function used to have no answer for. Never re-implement it here.
    files, _rejects = corpus_io.collect_corpus_files(_list_fn, drive_folder_id)
    for _r in _rejects:
        print(f"  REJECTED: {_r.get('name')} — {_r.get('reason')}")

    if not files:
        raise SystemExit(
            "HARD STOP — the Row-file Drive folder yielded ZERO usable files "
            "(EC-P39).\n"
            f"  folder id    : {drive_folder_id}\n"
            f"  rejected     : {len(_rejects)}\n"
            "Check that PHASE A ran and ROW_LISTING_CACHE holds every page of every "
            "folder, that the link points at the Row files, and the rejects above. An "
            "empty listing is a TRANSPORT diagnosis, never a corpus fact.")

    # Extract year from filename
    for f in files:
        f['year'] = extract_year_from_filename(f['name'])

    # v1.7: Deduplicate (EC-P22): same date+shift → keep larger file
    files = deduplicate_files(files)

    return files

# v2.20 — DELEGATED (Cluster G). The local copy searched the WHOLE path for any 4-digit run,
# so a digit-bearing folder could supply the year instead of the file.
extract_year_from_filename = bc.extract_year_from_filename

def deduplicate_files(files):
    """EC-P22: If two files have the same date+shift (ignoring trailing
    ' 1', ' 2' suffixes), keep the LARGER file. Skip the smaller."""
    # Group by normalized name (strip trailing ' N' suffixes)
    groups = {}
    for f in files:
        norm = re.sub(r'\s+\d+\.docx$', '.docx', f['name'])
        groups.setdefault(norm, []).append(f)
    result = []
    for norm, group in groups.items():
        if len(group) == 1:
            result.append(group[0])
        else:
            # Keep largest file (most likely to have images)
            result.append(max(group, key=lambda x: x.get('size', 0)))
    return result

def round_robin_by_year(files):
    """
    Order files round-robin by year to ensure early coverage of all years.
    E.g.: 2025-paper1, 2024-paper1, 2023-paper1, ..., 2025-paper2, ...
    Files with no extractable year (year=None) are appended at the end.

    DESIGN NOTE (v1.7): Round-robin uses newest-year-first ordering. This is
    intentional — if the exam introduced new question types in recent years,
    they are discovered early. Front-loading newest content is
    compatible with the 30% gate because the gate ensures adequate coverage
    of older years too.

    WITHIN EACH YEAR (v1.7): files are ordered by date ascending, then shift
    ascending. Claude MUST NOT reorder by file size. Smaller files may be
    text-only Row files; larger files contain embedded images for figural
    questions. Cherry-picking small files biases toward text-only types.
    """
    by_year = {}
    no_year = []  # EC-P8: files where year extraction failed
    for f in files:
        if f['year'] is None:
            no_year.append(f)
        else:
            by_year.setdefault(f['year'], []).append(f)

    # Sort years descending (newest first within each round)
    sorted_years = sorted(by_year.keys(), reverse=True)

    # v1.7: Within each year, sort by filename (date-asc, shift-asc)
    for year in sorted_years:
        by_year[year].sort(key=lambda x: x['name'])

    # Round-robin: take 1 from each year per round
    ordered = []
    max_per_year = max(len(v) for v in by_year.values()) if by_year else 0
    for round_idx in range(max_per_year):
        for year in sorted_years:
            year_files = by_year[year]
            if round_idx < len(year_files):
                ordered.append(year_files[round_idx])

    # Append no-year files at the end (still scanned, just not year-prioritised)
    ordered.extend(no_year)
    return ordered
```

### S3-2a — PRE-SCAN CONFIRMATION GATE

```
═══════════════════════════════════════════════════════════════════════
MANDATORY GATE — must pass before ANY scan classification begins.
═══════════════════════════════════════════════════════════════════════

After collecting and ordering all Row files (S3-2), but BEFORE running
any batch scanning (S3-5):

  1. Read EVERY Row file from the collected list.
     For Drive-sourced files: use Google Drive:read_file_content.
     For uploaded files: use python-docx or text read.
  2. For each file: count total questions using Q_PATTERNS from Step 5's E-2:
       Q_PATTERNS = [
         r'^Q\.\s*(\d+)\s+',        r'^Q(\d+)\.\s+',
         r'^Q\.\s*(\d+)\s*$',       r'^Q(\d+)\.\s*$'
       ]
     FOUR patterns, matching blueprint_core exactly — never five. Row files are
     NORMALISED (questions "Q.N", options "N. text"), so a bare-number pattern
     would count every OPTION as a question: 100 questions would count as 500.
     Entries 3-4 are the BARE-LABEL forms (GAP-2026-08-15-BAREQ): a stem whose whole
     payload is <m:oMath>, a drawing, or nothing (PYQPrepare S1-4 "empty/corrupt")
     reads through p.text as just "Q.N", and entries 1-2 require whitespace AFTER
     the digits, so they never matched it. The $ anchor admits ONLY a paragraph that
     is nothing but the label, so no option, cross-reference or heading can match.
     PREFER bc.detect_question_start(text) over a local copy of this table — the
     table is reproduced here for reading only, and audit_deep TABLE-PARITY proves
     it identical to the engine's.
     Mark each count as:
       ✓ = verified by parsing (file content was readable, Q-patterns matched)
       * = from filename pattern (file unreadable but filename has Q range like Q1-Q150)
     RECORD the count — do not merely display it. Per-file q_count and
     q_count_method are PERSISTED to scan_progress.json (S3-2, R-5), because a
     number that is computed, printed and discarded cannot reconcile anything.
  3. Extract year from filename (reuse extract_year_from_filename from S3-2)

  3b. DETERMINE PATTERN ERA per paper (v2.19 — ENGINE-BACKED, exam-agnostic).

      Call the ENGINE. Do NOT re-implement this logic here:

        import blueprint_core as bc     # routed for PYQScan in routes.json

        cfg_total, min_cfg_q, max_cfg_q = bc.exam_config_bounds(exam_config)
        cfg_type = bc.type_resolver_from_config(exam_config)   # None if no marking_scheme
        era = bc.classify_paper_era(
                  observed_q_numbers,          # Q-numbers parsed from THIS file
                  cfg_total, min_cfg_q, max_cfg_q,
                  observed_types=observed_types,   # {q_num: 'MCQ'|'MSQ'|'NAT'} if detected
                  cfg_type_for_q=cfg_type)

      Returns exactly one of bc.PATTERN_ERAS:
        'current'    — same count, all Q-numbers in range, types agree with marking_scheme
        'larger'     — more questions than the current pattern
        'smaller'    — fewer questions than the current pattern
        'renumbered' — right count, but Q-numbers outside every configured range
        'retyped'    — right count and numbering, but question TYPES disagree
      Papers whose count could not be verified by parsing (marked * ) are era='unverified'
      and are never guessed — 'unverified' is a pre-scan display value, not an engine era.

      v2.19 REPLACED A TRANSCRIBED COPY. v2.18 spelled this chain out in prose here while
      blueprint_core carried its own implementation, and routes.json gave PYQScan no engine
      to call — two independent definitions of "current era" that could drift apart silently.
      They are now one. The engine is also where the 'retyped' era was added: an exam that
      keeps its question COUNT but changes its question TYPES (all-MCQ becoming MCQ/MSQ/NAT
      is the textbook case) used to classify as 'current' and blend straight in. Across ~200
      exams a type or marking change is at least as common as a count change.

      Record out_of_range for era in ('larger', 'renumbered'): these are exactly the
      questions RULE 4's OUT-OF-RANGE branch routes through bc.OUT_OF_PATTERN. Note that
      era='smaller' produces NO out-of-range questions — a short paper merely leaves later
      ranges empty (EC-P9 first clause), which is why the shorter direction was never a
      data-loss risk and the longer one always was.

      MARKER-MODE EXAMS (v2.19 — previously had NO era detection at all).
      When marker_mode = true, questions are grouped by === Module === separators and
      Q-ranges are unused, so the Q-number chain above cannot run. A pattern change still
      shows up, in a different place: a RETIRED MODULE. Compare each paper's observed module
      names against exam_config.sections[].name:
        unknown_modules = [m for m in observed_modules
                           if m not in {s['name'] for s in exam_config['sections']}]
      Any unknown module means the paper predates (or postdates) the current pattern; label
      the paper era='larger' when it carries modules the current pattern does not have.
      Report them by name. Do NOT let EC-S2 fuzzy matching silently absorb a retired module
      into a surviving section — that is a mis-assignment, not a match, and it is exactly the
      marker-mode analogue of the out-of-range data loss fixed in Framework_PYQSort v1.9.

  4. Display a YEAR-WISE PAPER INVENTORY table:

     TASK 1 — PRE-SCAN CONFIRMATION

     | Year | Paper File | Q Count | Pattern Era |
     |------|-----------|---------|-------------|
     | 2025 | [ExamCode]_12-Sep-2025_Shift-1_Q1-Q100.docx | 100 ✓ | current |
     | 2025 | [ExamCode]_13-Sep-2025_Shift-2_Q1-Q100.docx | 100 * | unverified |
     | ...  | ...       | ...     | ...         |
     | TOTAL | [N] papers | [T] questions | [C] current / [L] larger / [S] smaller |

     ✓ = verified by parsing, * = from filename pattern (same structure as verified files)

  5. Print summary:
     "Papers found: [N]
      Total questions across all papers: [T]
      Years covered: [year1] ([count1] papers), [year2] ([count2] papers), ...
      Duplicates detected: [D]
      Non-docx files skipped: [S]

      ★ CONFIRMATION REQUIRED ★
      Verify these numbers match your expectation.
      Once confirmed, I will proceed with subtopic-level scanning
      ([BATCH_SIZE] papers per batch).
      If anything looks wrong, tell me and I will re-scan."

  5b. PATTERN-ERA NOTICE (v2.18 — print ONLY when some paper is not era='current';
      the single-era corpus, which is the common case across the ~200 exams, sees
      no extra output at all and this gate is unchanged for it):

     "PATTERN ERA: this corpus spans more than one exam pattern.
        current-pattern papers : [C]  ([total] Q each)
        larger-pattern papers  : [L]  (e.g. [file]: [n] Q — [k] Q above the
                                       current pattern's last question)
        smaller-pattern papers : [S]

      Both eras are SCANNED and both feed the taxonomy. That is deliberate: the
      reason older papers are retained is the variety of concepts, phrasings,
      difficulties and question formats they expose, and a subtopic seen across
      many eras yields better generated questions than one seen twice. Questions
      beyond the current pattern's last Q-number are NOT dropped — RULE 4 routes
      them through the OUT_OF_PATTERN sentinel and classifies them against the full
      taxonomy.

      What this does and does not affect:
        SAFE   — question COUNTS. Framework_Blueprint §4-2 uses r_avg only as a
                 proportion; the absolute budget always comes from exam_config's
                 sec_qs. A 100-Q historical paper cannot produce a 100-Q mock when
                 the pattern says 60.
        AT RISK— subject/subtopic MIX and format mix, which are inherited from
                 whichever eras dominate the corpus. §3 recency weighting (last 2
                 valid years x2) dampens this but does not remove it: an exam with
                 many old-era years still lets the retired pattern outweigh the
                 live one in r_avg.

      No action is required to proceed — this is a report, not an error. If the mix
      matters more to you than the variety for this exam, restrict the corpus to
      current-pattern papers and re-run. That is an operator decision and the
      framework will not make it silently in either direction."

  6. WAIT for explicit user confirmation. Do NOT proceed to S3-5 until
     confirmed. The confirmed paper count and total questions become the
     reference for scan progress tracking.

  7. On RESUME sessions (scan_progress.json exists): still display the
     inventory but also show progress:
       "Previously scanned: [M] papers. Remaining: [N-M] papers."
     User re-confirms before scanning resumes.

PURPOSE: proves that Claude can see every Row file and every question
inside each file without fail — BEFORE classification effort begins.
Catches Drive access issues, missing files, corrupt docs, or Q-pattern
parsing failures upfront. Consistent with Step 4's Task 1 (S5-1a).
```

### S3-3 — Scan classification (lightweight, OMML-aware, pattern-tracked)

```
For each paper in the batch:
  1. Read the Row file .docx (or Drive text via read_file_content — see S3-2)

  1b. RECONCILE AGAINST THE INVENTORY (GAP-2026-08-15-BAREQ, R-5 — HARD STOP).
      After classifying this paper, assert:

        len(classifications[paper]) == inventory[paper]['q_count']

      when inventory[paper]['q_count_method'] == "parsed". A mismatch means the
      mechanical parse and the classification pass disagree about how many questions
      this paper HAS — which is this defect class observed at the earliest possible
      point, before a single downstream artefact is built on it. HARD STOP and name
      the Q-numbers present in one and absent from the other.

      Measured precedent: IIT_JAM_MATHEMATICS_classifications.json held 60 rows for
      12-Feb-2017 — four of them tagged "OMML-obscured", this step's own term for a
      stem that extracted blank — while the Row file mechanically parsed to 56. Two
      artefacts of the same project, in the same folder, disagreeing by four, and
      nothing in the framework compared them.

      q_count_method == "filename" → WARN and continue; an inferred count is not
      evidence. Field absent (a pre-remedy project) → WARN and continue, never halt.

  2. For each question (detected via bc.detect_question_start — Q_PATTERNS, Step 5 E-2):
     a. Extract stem text
     b. If OMML formula present and rendered → use rendered text
        If OMML-obscured (blank stem after extraction) → classify by
        Q-position + option content + context (see S3-2 OMML HANDLING)
     c. Determine SECTION:
        - If marker_mode=true: use module separator (=== Subject ===)
        - If marker_mode=false: use Q-number range from exam_config.sections
        - If marker_mode=false AND the Q-number is outside every configured range
          (a previous-era paper larger than the current pattern): assign the
          OUT_OF_PATTERN sentinel and classify against the FULL taxonomy in (d).
          NEVER None, NEVER dropped, NEVER guessed into the nearest section.
          See RULE 4 OUT-OF-RANGE branch (§8) and EC-P9.
     d. Classify into (Topic, Subtopic) within that section:
        - Match against current taxonomy
        - Use universal classification rules (§8)
        - If figure-referenced but no image → use text clues for
          figural subtopic (S3-2 FIGURAL HANDLING)
        - If no subtopic fits → record as NEW DISCOVERY candidate
     e. Record PATTERN METADATA (RULE 7 — mandatory for refinement pass):
        - question_task: what the student is asked to DO
          (identify, select, correct, find, calculate, match, arrange,
           select_incorrect, select_correct, fill_blank, rearrange, etc.)
        - question_format: how content is presented
          (standalone_word, standalone_number, in_sentence, in_passage,
           word_list, number_set, figure, figure-inferred, OMML-obscured,
           mixed, table_based, etc.)
        - question_direction: transformation direction if applicable
          (a_to_b, b_to_a, null if not a transformation question)
        - thematic_domain: knowledge area if classifiable
          (e.g., "actions_behaviour", "persons_professionals",
           "subject_verb_agreement", "tense_errors", null if generic)
     f. Store classification in [ExamCode]_classifications.json:
        {q_num, section, topic, subtopic, is_new_discovery,
         question_task, question_format, question_direction, thematic_domain}

  3. NEW DISCOVERY VALIDATION (v1.7 — before adding to taxonomy):
     For each NEW DISCOVERY candidate, Claude MUST answer these 3 questions:
       Q1. Does ANY existing subtopic in this section cover this question type?
           If yes → classify there, NOT a new discovery.
       Q2. Would the existing subtopic's name mislead a student studying for
           this question type? If no → classify there, NOT a new discovery.
       Q3. Would a coaching institute create a SEPARATE practice set for this
           question type vs the closest existing subtopic?
           If no → classify there, NOT a new discovery.
     Only if all 3 answers confirm separation → add as new discovery.

  4. After all questions in paper classified:
     - Apply new discovery validation (step 3 above)
     - Genuinely new subtopics: add to taxonomy under appropriate section/topic
     - Record paper_id in papers_scanned_list

  5. POST-PAPER VALIDATION (v1.7 — informational, does not halt scanning):
     After classifying all questions in a paper:
       a. Count questions per section (using Q-range from exam_config)
       b. If any section has fewer questions than expected: log warning
          "Paper X: Section Y has N questions, expected M"
       c. If total questions ≠ exam_config.total_questions: log warning
       d. Warnings are informational only (EC-P9 handles variable Q counts)
```

### S3-4 — Convergence check (4 HARD GATES)

```
═══════════════════════════════════════════════════════════════════════
MANDATE: MINIMUM PAPER COVERAGE (v1.7 — PROSE-LEVEL, outside code block)
═══════════════════════════════════════════════════════════════════════

For any corpus > 20 papers, Claude MUST scan at least 30% of total
papers before convergence is possible. For a 200-paper corpus this
means MINIMUM 60 papers. This is not a recommendation. It is a hard
numerical floor. Scanning 59 papers and declaring convergence is a
spec violation regardless of discovery rates or empty-batch counts.

ANTI-EDITORIALIZING RULE (v1.7, updated v2.3):
  When ANY gate returns 'continue', Claude's batch-end message MUST contain:
    1. New subtopics count for this batch
    2. Current taxonomy size (total subtopics)
    3. Papers scanned / total, remaining count
    4. Per-section Q distribution for this batch (v2.2)
    5. Classification quality breakdown if any degraded (v2.2)
    6. Gate status (PASS/FAIL per gate)
    7. "Say 'continue' to process next batch."
    8. NOTHING ELSE — no editorial commentary beyond items 1-7.
       After printing items 1-7, the response ENDS (S3-4a Batch Stop Law).
       Claude MUST NOT process the next batch in the same response.
       Claude MUST NOT run the refinement pass in the same response
       (unless this is the final batch — see S3-4a FINAL BATCH EXCEPTION).

  Claude MUST NOT:
    - Describe taxonomy as "stable", "functionally complete", or "converged"
    - Use phrases like "low discovery rate", "diminishing returns",
      "near-zero value", "scanning more papers would yield..."
    - Recommend skipping to refinement/approve before all gates pass
    - Frame any gate as a "structural constraint" or "numerical threshold"
    - Suggest the user trigger PYQApprove early
    - Add any analysis, recommendation, or editorial commentary about
      whether scanning should continue — the GATES decide, not Claude

  This rule applies to BOTH chat output AND JSON content.
  scan_progress.json MUST contain ONLY schema-defined fields. Claude
  MUST NOT add editorial fields (convergence_recommendation, scan_analysis,
  recommendation, justification, assessment, or ANY field arguing for/against
  convergence). The JSON is a progress tracker, not an opinion document.

  consecutive_empty_batches accumulates from Batch 1 onward but is ONLY
  EVALUATED after Gate 2 passes. Claude MUST NOT cite the counter's value
  as evidence of stability before Gate 2 passes. Before Gate 2, the counter
  is informational noise — it has zero bearing on convergence.
```

```python
def check_convergence(progress, total_available, all_years):
    """
    ═══════════════════════════════════════════════════════════════
    CONVERGENCE HARD GATES — NON-NEGOTIABLE, NON-BYPASSABLE.

    Claude CANNOT declare convergence unless ALL 4 gates pass.
    There is NO override. NO shortcut. NO exception. NO early exit.
    There is NO "close enough". There is NO "probably sufficient".
    Treat these gates like physical locks that cannot be picked.

    If ANY gate returns 'continue' or 'refinement_needed':
      - DO NOT print "★ CONVERGENCE REACHED ★"
      - DO NOT offer early exit options
      - DO NOT ask user if they want to stop
      - Return 'continue' status in the batch-end summary, then
        STOP THE RESPONSE and wait for user's "continue" trigger
        (see S3-4a Batch Stop Law). "Without discussion" means
        do not editorialize — it does NOT mean auto-advance.
    ═══════════════════════════════════════════════════════════════

    all_years: set of all distinct years in the full paper pool
               (derived from round_robin_by_year's input).
    """
    meta = progress['_meta']
    scanned = meta['papers_scanned']
    years = meta['years_covered']
    consecutive_empty = meta['consecutive_empty_batches']

    # ── GATE 0: SMALL CORPUS — scan ALL papers, no convergence shortcut ──
    if total_available <= SMALL_CORPUS_THRESHOLD:
        if scanned < total_available:
            return 'continue', (
                f'GATE 0 LOCKED: Small corpus ({total_available} papers). '
                f'ALL papers must be scanned. No convergence shortcut allowed. '
                f'{scanned}/{total_available} done.'
            )
        # If scanned >= total_available in small corpus → skip gates 1-3,
        # but Gate 4 (refinement) still applies.

    # ── GATE 1: YEAR COVERAGE — every available year must appear ──
    if total_available > SMALL_CORPUS_THRESHOLD:
        min_year_coverage = len(all_years) > 0 and set(years) >= all_years
        if not min_year_coverage:
            covered = len(set(years))
            needed = len(all_years)
            return 'continue', (
                f'GATE 1 LOCKED: Year coverage incomplete. '
                f'Have {covered}/{needed} years. '
                f'Convergence is IMPOSSIBLE until ALL {needed} years are covered.'
            )

    # ── GATE 2: PAPER COVERAGE — minimum 30% of total papers ──
    if total_available > SMALL_CORPUS_THRESHOLD:
        min_papers = max(1, int(MIN_COVERAGE_RATIO * total_available))
        if scanned < min_papers:
            return 'continue', (
                f'GATE 2 LOCKED: {scanned}/{min_papers} papers scanned '
                f'({MIN_COVERAGE_RATIO*100:.0f}% minimum = {min_papers}). '
                f'Convergence is IMPOSSIBLE until {min_papers} papers are scanned.'
            )

    # ── GATE 3: CONSECUTIVE EMPTY BATCHES — stability signal ──
    #    Only checked AFTER gates 0-2 have all passed.
    #    SKIP when all papers have been scanned — stability is irrelevant
    #    because there are no more papers to test against.
    all_papers_scanned = (scanned >= total_available)
    if not all_papers_scanned and consecutive_empty < CONVERGENCE_CONSECUTIVE:
        return 'continue', (
            f'Gates 0-2 passed. Gate 3: Stability check — '
            f'{consecutive_empty}/{CONVERGENCE_CONSECUTIVE} consecutive empty batches. '
            f'Need {CONVERGENCE_CONSECUTIVE - consecutive_empty} more.'
        )

    # ── GATE 4: REFINEMENT PASS — mandatory before convergence ──
    #    Only checked AFTER gates 0-3 have all passed.
    if not progress['_meta'].get('refinement_pass_done', False):
        return 'refinement_needed', (
            f'Gates 0-3 passed. Gate 4: MANDATORY refinement pass required. '
            f'Run §3-6 Subtopic Refinement Pass before convergence can be declared.'
        )

    # ── ALL 4 GATES PASSED — convergence is legitimate ──
    return 'converged', (
        f'Taxonomy stable. {scanned}/{total_available} papers scanned. '
        f'All {len(all_years)} years covered. '
        f'Last {CONVERGENCE_CONSECUTIVE * BATCH_SIZE} papers added 0 new subtopics. '
        f'Refinement pass completed.'
    )

def report_gate_status(progress, total_available, all_years):
    status, msg = check_convergence(progress, total_available, all_years)
    if status == 'converged':
        print(f"\n★ CONVERGENCE REACHED ★")
        print(f"  {msg}")
        print(f"\n  Options:")
        print(f"    A) Stop scanning — proceed to --approve (recommended)")
        print(f"    B) Continue scanning remaining papers")
        return 'converged'
    elif status == 'refinement_needed':
        print(f"\n⚙ REFINEMENT PASS REQUIRED ⚙")
        print(f"  {msg}")
        return 'refinement_needed'
    else:
        # Gates not met — print status but DO NOT offer any exit option
        print(f"  Convergence: {msg}")
        return 'continue'

def print_convergence_summary(progress, classifications, exam_code):
    """
    v2.2: Comprehensive summary displayed BEFORE "Run: PYQApprove".
    The user is about to LOCK the taxonomy — they need full visibility.
    """
    meta = progress['_meta']
    taxonomy = progress['taxonomy']

    # ── TAXONOMY SIZE ──
    original_count = meta.get('source_taxonomy_subtopics', '?')
    final_sections = len(taxonomy)
    final_topics = sum(len(topics) for topics in taxonomy.values())
    final_subtopics = sum(
        len(subs) for topics in taxonomy.values() for subs in topics.values()
    )

    # ── DISCOVERY STATS ──
    scan_discoveries = 0
    refinement_new = 0
    refinement_removed = 0
    for entry in progress.get('discovery_log', []):
        if entry.get('batch') == 'refinement_pass':
            refinement_new += entry.get('count', 0)
            refinement_removed += len(entry.get('removed_subtopics', []))
        else:
            scan_discoveries += entry.get('count', 0)

    # ── CLASSIFICATION QUALITY ──
    total_qs = 0
    quality = Counter()  # normal / omml_obscured / figure_inferred
    sec_dist = Counter()
    for paper_id, paper_classifs in classifications.items():
        for c in paper_classifs:
            total_qs += 1
            sec_dist[c['section']] += 1
            fmt = c.get('question_format', '')
            if 'OMML-obscured' in str(fmt):
                quality['omml_obscured'] += 1
            elif 'figure-inferred' in str(fmt):
                quality['figure_inferred'] += 1
            else:
                quality['normal'] += 1

    normal_pct = (quality['normal'] / total_qs * 100) if total_qs else 0
    omml_pct = (quality['omml_obscured'] / total_qs * 100) if total_qs else 0
    fig_pct = (quality['figure_inferred'] / total_qs * 100) if total_qs else 0

    # ── PAPERS PER YEAR ──
    year_counts = Counter()
    for entry in progress.get('discovery_log', []):
        if entry.get('batch') != 'refinement_pass':
            for p in entry.get('papers', []):
                yr = extract_year_from_filename(p)
                if yr:
                    year_counts[yr] += 1

    # ── PRINT SUMMARY ──
    print(f"\n{'═' * 60}")
    print(f"  POST-CONVERGENCE SUMMARY — REVIEW BEFORE LOCKING TAXONOMY")
    print(f"{'═' * 60}")
    print(f"\n  TAXONOMY GROWTH:")
    print(f"    Step 2a original : {original_count} subtopics")
    print(f"    Final            : {final_subtopics} subtopics "
          f"({final_sections} sections, {final_topics} topics)")
    print(f"    Scan discoveries : +{scan_discoveries} new subtopics")
    print(f"    Refinement splits: +{refinement_new} new, "
          f"-{refinement_removed} removed")
    print(f"\n  PAPERS SCANNED: {meta['papers_scanned']}/{meta.get('total_available', '?')}")
    if year_counts:
        yr_str = ', '.join(f"{yr} ({cnt})" for yr, cnt
                           in sorted(year_counts.items(), reverse=True))
        print(f"    Per year: {yr_str}")
    print(f"\n  CLASSIFICATION QUALITY ({total_qs} total questions):")
    print(f"    Normal          : {quality['normal']} ({normal_pct:.1f}%)")
    print(f"    OMML-obscured   : {quality['omml_obscured']} ({omml_pct:.1f}%)")
    print(f"    Figure-inferred : {quality['figure_inferred']} ({fig_pct:.1f}%)")
    if omml_pct > 30:
        print(f"    ⚠ WARNING: {omml_pct:.0f}% OMML-obscured — scan may have "
              f"missed math-heavy patterns. Consider this before locking.")
    print(f"\n  PER-SECTION SNAPSHOT:")
    for sec_name in sorted(taxonomy.keys()):
        topics = taxonomy[sec_name]
        n_topics = len(topics)
        n_subs = sum(len(subs) for subs in topics.values())
        n_qs = sec_dist.get(sec_name, 0)
        print(f"    {sec_name}: {n_topics} topics, {n_subs} subtopics, "
              f"{n_qs} Qs classified")
    print(f"\n{'═' * 60}")
    print(f"  Run: PYQApprove")
    print(f"{'═' * 60}")
```

### S3-4a — BATCH STOP LAW (MANDATORY — same architectural class as convergence gates)

```
═══════════════════════════════════════════════════════════════════════
BATCH STOP LAW — AUTO-ADVANCE BETWEEN BATCHES IS PERMANENTLY BANNED
═══════════════════════════════════════════════════════════════════════

This rule has the same force as convergence gates and anti-editorializing.
It applies to EVERY batch in EVERY mode that processes batches:
  Phase 0b (--scan): scanning batches
  Phase B  (--counts): counting batches (when run interactively, not via script)

LIVE FAILURE (SSC CGL Tier 2, July 2026):
  Claude processed Batch 1 (3 papers, 35 new subtopics discovered) and
  immediately processed Batch 2 (2 papers) in the SAME response without
  waiting for user confirmation. The batch gate was not enforced because
  the spec buried it as item 7 in the Anti-Editorializing Rule (a section
  about banned phrases, not about response flow control). This failure
  will repeat across all 200+ exams unless enforced at mandate level.

THE BATCH STOP CONTRACT:

  After completing ANY scan batch (including the very first):
    STEP 1: Print the batch-end summary (items 1-6 from S3-4)
    STEP 2: Save scan_progress.json + classifications.json
    STEP 3: Call present_files with scan_progress.json + classifications.json
            (user needs a download link for session resume)
    STEP 4: Print: "Say 'continue' to process next batch."
    STEP 5: *** END THE RESPONSE. Write NOTHING more. ***

  The next batch begins ONLY when the user's NEW message is a
  continue trigger.

  ACCEPTED CONTINUE TRIGGERS (case-insensitive, trimmed):
    "continue", "continue.", "go", "next", "proceed", "go ahead",
    "next batch"

  IF the user message IS a continue trigger:
    → Process the next batch.

  IF the user message is NOT a continue trigger (a question,
  correction, or other instruction):
    → Answer the user's message.
    → Do NOT process the next batch.
    → End with: "Say 'continue' to process next batch."

  NOTE ON RESUME SESSIONS:
    Resume sessions (S3-7) use their own gate (re-list Drive files,
    re-run S3-2a pre-scan gate) and are NOT governed by the intra-session
    continue trigger contract. The Batch Stop Law applies to batch
    boundaries within a session, not to the session-start gate.

  APPLIES TO ALL CORPUS SIZES:
    "Scan ALL papers" (small corpus mode, < SMALL_CORPUS_THRESHOLD)
    means every paper WILL be scanned eventually. It does NOT mean
    they are scanned in one response without stopping. Even for a
    5-paper corpus, Claude MUST stop between batches.

  WHY THIS MATTERS:
    Between batches, the user may want to:
    - Review discovered subtopics for accuracy
    - Correct misclassifications before they propagate
    - Upload additional papers to the Drive folder
    - Pause and resume in a new session
    - Ask questions about the scan results so far
    Auto-advance removes all these checkpoints silently.

  FORBIDDEN IN THE SAME RESPONSE AFTER A BATCH SUMMARY:
    - Processing the next batch's papers
    - "I'll now continue with Batch N+1..."
    - "Proceeding to scan the remaining papers..."
    - Running the refinement pass (unless it's the final batch
      AND all papers are scanned — see S3-4a FINAL BATCH below)
    - ANY classification work beyond the current batch

  FINAL BATCH EXCEPTION:
    The LAST batch (all papers scanned, no pending papers) does NOT
    end with a continue prompt. Instead, it auto-runs:
      1. Refinement pass (if not already done)
      2. Post-convergence summary
      3. File delivery (scan_progress.json + classifications.json)
      4. "Run: PYQApprove"
    This matches MockCreate's final-batch exception (B-8).
═══════════════════════════════════════════════════════════════════════
```

### S3-5 — Batch processing loop

```
BATCH INTEGRITY RULE (v1.7):
  A batch counts toward consecutive_empty_batches ONLY if it contains
  exactly BATCH_SIZE papers (or remaining papers if fewer than BATCH_SIZE
  are left in the queue). A partial batch (context limit reached mid-batch)
  does NOT increment or reset the counter.

  If context fills before completing BATCH_SIZE:
    1. Save scan_progress.json and classifications.json with partial results
    2. Print: "Context limit. Download scan_progress.json → upload to
       project knowledge → new chat → Step 2b: PYQScan PYQ: <<link>>"
    3. New session resumes the incomplete batch (not a new batch)

RESPONSE BUDGET (v1.7):
  A single response reads BATCH_SIZE papers via Drive, classifies all
  questions, and saves progress. If context is insufficient for 3 papers:
    - Reduce to 2 papers per batch (EC-P15 allows this)
    - If even 2 papers won't fit: save progress, end session, resume
  Claude should note reduced batch size in the batch summary.

PER-QUESTION CLASSIFICATION STORAGE (v1.7):
  Every classified question MUST be stored with its full metadata in
  [ExamCode]_classifications.json. Storing only paper-level summaries
  (e.g., "5 new subtopics found") is a spec violation. The refinement
  pass REQUIRES per-question data to detect patterns.
```

```python
def run_scan(exam_code, progress, paper_queue, total_available):
    """Main scan loop — processes papers in batches."""

    # v2.3: Write total_available to _meta so saved JSON has correct value.
    # Without this, _meta.total_available stays 0 (the init default) and
    # convergence gates break on resume if they read from _meta.
    progress['_meta']['total_available'] = total_available

    # Derive all_years from the FULL paper queue (not just pending)
    all_years = set(p['year'] for p in paper_queue if p.get('year') is not None)

    done_ids = set(progress.get('papers_scanned_list', []))
    pending = [p for p in paper_queue if p['name'] not in done_ids]

    # v1.7: Load or init classifications file (separate from progress)
    classif_path = f'/mnt/user-data/outputs/{exam_code}_classifications.json'
    if os.path.exists(classif_path):
        with open(classif_path, encoding='utf-8') as f:
            classifications = json.load(f)
    else:
        classifications = {}

    if not pending:
        # All papers scanned (or 0 papers available).
        # Force refinement if not already done
        if not progress['_meta'].get('refinement_pass_done', False):
            run_refinement_pass(progress, classifications, exam_code)
        from datetime import datetime, timezone
        progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
        save_scan_progress(progress, exam_code)
        conv_status = report_gate_status(progress, total_available, all_years)
        print_convergence_summary(progress, classifications, exam_code)
        return

    print(f"Papers: {len(done_ids)} done / {total_available} total. "
          f"Pending: {len(pending)}")

    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch = pending[batch_start : batch_start + BATCH_SIZE]
        batch_num = (len(done_ids) // BATCH_SIZE) + (batch_start // BATCH_SIZE) + 1
        is_complete_batch = (len(batch) == BATCH_SIZE or
                             batch_start + BATCH_SIZE >= len(pending))

        print(f"\n=== Scan Batch {batch_num}: {len(batch)} paper(s) ===")

        new_subtopics_this_batch = []
        for paper_ref in batch:
            # Read and classify (lightweight scan with pattern metadata)
            paper_classifications, new_discoveries = scan_paper(
                paper_ref, progress['taxonomy'], progress['exam_config']
            )
            # v1.7: Store per-Q classifications in separate file
            paper_id = paper_ref['name']
            classifications[paper_id] = paper_classifications

            # Add validated new discoveries to taxonomy
            for disc in new_discoveries:
                add_to_taxonomy(progress['taxonomy'], disc)
                new_subtopics_this_batch.append(disc)

            # Update metadata
            progress['papers_scanned_list'].append(paper_id)
            progress['_meta']['papers_scanned'] += 1
            year = paper_ref.get('year')
            if year and year not in progress['_meta']['years_covered']:
                progress['_meta']['years_covered'].append(year)

            # v2.22 — PERSIST AFTER EVERY PAPER (DEFECT C, third instance; found by
            # validate_framework_md Check X, not by reading). scan_paper() mutates
            # progress in memory — the scanned list, the paper count, the years covered
            # and any newly discovered subtopics already added to the taxonomy above.
            # Until v2.22 the only save was after the batch, so an exception on paper 3
            # discarded papers 1 and 2 along with every subtopic they discovered, and the
            # progress file showed them as never scanned.
            # This does NOT disturb convergence. consecutive_empty_batches is updated
            # below, per BATCH and only for complete batches, and EC-P26 already
            # establishes that a partial batch persists its papers WITHOUT touching that
            # counter. Saving per paper produces exactly the state EC-P26 describes; it
            # simply reaches it on an exception as well as on a context limit.
            # BATCH_SIZE is unchanged — batching remains the pacing unit, not the
            # durability unit.
            save_scan_progress(progress, exam_code)
            save_classifications(classifications, exam_code)

        # v1.7: Update convergence tracking — ONLY for complete batches
        # A batch with 2 empty papers + 1 discovery = RESET (not increment)
        if is_complete_batch:
            if len(new_subtopics_this_batch) == 0:
                progress['_meta']['consecutive_empty_batches'] += 1
            else:
                progress['_meta']['consecutive_empty_batches'] = 0  # HARD RESET
        # Partial batches (context limit) do NOT affect the counter

        # Log discovery
        progress['discovery_log'].append({
            'batch': batch_num,
            'papers': [p['name'] for p in batch],
            'complete_batch': is_complete_batch,
            'new_subtopics': [f"{d['section']}/{d['topic']}/{d['subtopic']}"
                              for d in new_subtopics_this_batch],
            'count': len(new_subtopics_this_batch)
        })

        # Save progress + classifications
        from datetime import datetime, timezone
        progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
        save_scan_progress(progress, exam_code)
        save_classifications(classifications, exam_code)

        # Print batch summary
        total_subtopics = sum(
            len(subs) for topics in progress['taxonomy'].values()
            for subs in topics.values()
        )
        scanned = progress['_meta']['papers_scanned']
        remaining = total_available - scanned

        # v1.7: MANDATORY BATCH-END MESSAGE FORMAT
        # Claude MUST print EXACTLY this and NOTHING ELSE after it.
        # v2.2: Added per-section Q-count and classification quality.
        print(f"  New subtopics: {len(new_subtopics_this_batch)}")
        print(f"  Taxonomy: {total_subtopics} subtopics")
        print(f"  Papers: {scanned}/{total_available} ({remaining} remaining)")

        # v2.2: Per-section Q-count from this batch — catches section detection
        # failures early (e.g., all Qs going to 1 section in a 4-section exam).
        sec_counts = Counter()
        quality_counts = Counter()  # normal / OMML-obscured / figure-inferred
        for paper_ref in batch:
            paper_id = paper_ref['name']
            for c in classifications.get(paper_id, []):
                sec_counts[c['section']] += 1
                fmt = c.get('question_format', '')
                if 'OMML-obscured' in str(fmt):
                    quality_counts['omml_obscured'] += 1
                elif 'figure-inferred' in str(fmt):
                    quality_counts['figure_inferred'] += 1
                else:
                    quality_counts['normal'] += 1
        total_batch_qs = sum(sec_counts.values())
        print(f"  Batch Q distribution: {dict(sec_counts)}")
        if quality_counts['omml_obscured'] + quality_counts['figure_inferred'] > 0:
            print(f"  Quality: {quality_counts['normal']} normal, "
                  f"{quality_counts['omml_obscured']} OMML-obscured, "
                  f"{quality_counts['figure_inferred']} figure-inferred")

        # Gate status
        status, msg = check_convergence(progress, total_available, all_years)
        print(f"  Gates: {msg}")

        # Check convergence
        if status == 'refinement_needed':
            run_refinement_pass(progress, classifications, exam_code)
            status, msg = check_convergence(progress, total_available, all_years)
            if status == 'converged':
                save_scan_progress(progress, exam_code)
                print_convergence_summary(progress, classifications, exam_code)
                return
        elif status == 'converged':
            save_scan_progress(progress, exam_code)
            print_convergence_summary(progress, classifications, exam_code)
            return

        # ══ BATCH STOP LAW (S3-4a) — HARD STOP ══════════════
        # After printing batch summary: END THE RESPONSE.
        # *** Write nothing more. Generate nothing more. ***
        # This is the PYQScan equivalent of MockCreate's MANDATE 1 STEP 6.
        # Claude's response ENDS here. The next batch begins ONLY when
        # the user sends a new message with a continue trigger.
        # Auto-advancing to the next batch = S3-4a violation.

        # Deliver via present_files: EXACTLY 2 files (S10-1 --scan closed set).
        #   1. [ExamCode]_scan_progress.json
        #   2. [ExamCode]_classifications.json
        # No other files. The evolved taxonomy is INSIDE scan_progress.json.
        # DO NOT create separate taxonomy files (taxonomy_draft_v2, etc.).
        # Run S10-2 pre-delivery checklist before present_files.
        progress_path = f'/mnt/user-data/outputs/{exam_code}_scan_progress.json'
        classif_path  = f'/mnt/user-data/outputs/{exam_code}_classifications.json'
        present_files([progress_path, classif_path])

        print(f"\n  Say 'continue' to process next batch.")
        return  # EXIT — response ENDS here

def save_scan_progress(progress, exam_code):
    """Save scan progress JSON. Called after each batch.
    v1.7: BANNED JSON FIELDS — Claude MUST NOT add any of these:
      convergence_recommendation, scan_analysis, recommendation,
      justification, assessment, analysis, suggestion, or ANY field
      arguing for/against convergence. Only schema-defined fields."""
    path = f'/mnt/user-data/outputs/{exam_code}_scan_progress.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
    return path

def save_classifications(classifications, exam_code):
    """Save per-question classifications to SEPARATE file (v1.7).
    This file is cumulative — grows with each batch.
    Used by refinement pass and for audit."""
    path = f'/mnt/user-data/outputs/{exam_code}_classifications.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(classifications, f, indent=2, ensure_ascii=False)
    return path

def scan_paper(paper_ref, taxonomy, exam_config):
    """
    Lightweight classification of one Row file against current taxonomy.
    Returns: (classifications, new_discoveries)
      classifications: list of {q_num, section, topic, subtopic,
                                 question_task, question_format,
                                 question_direction, thematic_domain}
      new_discoveries: list of {section, topic, subtopic} for genuinely new subtopics
                       (AFTER passing new discovery validation — S3-3 step 3)
    Claude performs this classification using domain knowledge + universal rules (§8).
    Pattern metadata (RULE 7) is MANDATORY — every classification must include
    the 4 metadata fields. These enable the refinement pass (§3-6).
    """
    pass  # CLASS: J — Judgment over the paper text already in context: the model reads the stem and names a subtopic. No tool call, so it degrades gracefully — the model treats the spec as a reasoning task and produces the value directly.

def add_to_taxonomy(taxonomy, discovery):
    """
    Add a newly discovered subtopic to the taxonomy dict.
    discovery: {section, topic, subtopic}
    taxonomy[section][topic] is a list of subtopic strings.
    """
    sec = discovery['section']
    top = discovery['topic']
    sub = discovery['subtopic'].strip()  # §7 NAME CONTRACT: always .strip()
    if sec not in taxonomy:
        taxonomy[sec] = {}
    if top not in taxonomy[sec]:
        taxonomy[sec][top] = []
    if sub not in taxonomy[sec][top]:
        taxonomy[sec][top].append(sub)
```

### S3-6 — Subtopic Refinement Pass (MANDATORY before convergence)

```
═══════════════════════════════════════════════════════════════════════
SUBTOPIC REFINEMENT PASS — GATE 4 PREREQUISITE
═══════════════════════════════════════════════════════════════════════

WHEN:
  Triggered automatically when Gates 0-3 all pass (check_convergence
  returns 'refinement_needed'). This pass runs ONCE. After completion,
  it sets refinement_pass_done = True, which unlocks Gate 4.

PURPOSE (v2.4 — revised default bias):
  Two goals, applied in this priority order:

  1. MERGE confused subtopics: If the classifier consistently assigns
     questions to subtopic A with low confidence because subtopic B is
     equally plausible (confidence < 70%), MERGE A and B into one.
     Over-splitting is worse than over-merging (ref: MPPSC Botany proof —
     4.1× inflation caused 38% data loss).

  2. SPLIT genuinely broad subtopics: If a subtopic accumulates ≥15
     classified questions AND contains 2+ genuinely distinct question
     patterns, propose a split — but ONLY if it passes the Q3 Unique
     Domain Check from S2-3 (different solving approach + separate coaching
     chapter + unambiguous classification).

  The refinement pass may use the 6 pattern dimensions from S2-3 Appendix
  as an analytical tool, but every proposed split MUST pass Q3 (Unique
  Domain Check) before being accepted. The default bias is MERGE over SPLIT.

ALGORITHM:
```

```python
def run_refinement_pass(progress, classifications, exam_code):
    """
    Mandatory refinement pass — reviews all classified questions per subtopic,
    detects broad subtopics, and splits them based on observed patterns.

    EXECUTION MODEL (v1.7):
      Processes one (section, topic, subtopic) at a time — NOT the entire
      classification set at once. Context holds one subtopic's data at a time.
      For subtopics with > 50 classified questions: sample 50 random questions
      for dimension analysis (sufficient to detect clusters).
    """
    taxonomy = progress['taxonomy']
    refinement_splits = []

    # 1. Aggregate all classified questions by (section, topic, subtopic)
    subtopic_questions = {}  # key: (sec, top, sub) → list of classification dicts
    for paper_id, paper_classifs in classifications.items():
        for c in paper_classifs:
            key = (c['section'], c['topic'], c['subtopic'])
            subtopic_questions.setdefault(key, []).append(c)

    # 2. For each subtopic with enough data, check for splittable patterns
    MIN_QUESTIONS_FOR_SPLIT = 15  # v2.4: raised from 5. Need substantial evidence before splitting.
    MIN_PATTERN_SIZE = 3          # v2.4: raised from 2. A pattern needs ≥3 Qs to justify a new subtopic.

    for (sec, top, sub), questions in subtopic_questions.items():
        if len(questions) < MIN_QUESTIONS_FOR_SPLIT:
            continue  # not enough data to split reliably

        # 3. Cluster by pattern metadata dimensions
        #    Check each dimension for distinct clusters
        splits_found = check_dimensional_splits(questions, sec, top, sub)

        if splits_found:
            refinement_splits.extend(splits_found)

    # 4. Apply splits to taxonomy
    for split in refinement_splits:
        old_sub = split['old_subtopic']
        sec = split['section']
        top = split['topic']
        new_subs = split['new_subtopics']

        # Remove old subtopic
        if old_sub in taxonomy.get(sec, {}).get(top, []):
            taxonomy[sec][top].remove(old_sub)

        # Add new subtopics
        for ns in new_subs:
            ns_clean = ns.strip()
            if ns_clean not in taxonomy[sec][top]:
                taxonomy[sec][top].append(ns_clean)

    # 5. Reclassify affected questions under new subtopics
    if refinement_splits:
        reclassify_after_refinement(classifications, refinement_splits)

    # 5b. Verify no orphaned classifications (v1.7)
    for paper_id, paper_classifs in classifications.items():
        for c in paper_classifs:
            sub = c['subtopic']
            sec = c['section']
            top = c['topic']
            if sub not in taxonomy.get(sec, {}).get(top, []):
                # Orphaned classification — reclassify missed this question
                # Force-assign to first new subtopic as fallback
                available = taxonomy.get(sec, {}).get(top, [])
                if available:
                    c['subtopic'] = available[0]  # fallback assignment

    # 6. Log refinement results
    progress['discovery_log'].append({
        'batch': 'refinement_pass',
        'papers': [],
        'new_subtopics': [
            f"{s['section']}/{s['topic']}/{ns}"
            for s in refinement_splits
            for ns in s['new_subtopics']
        ],
        'removed_subtopics': [
            f"{s['section']}/{s['topic']}/{s['old_subtopic']}"
            for s in refinement_splits
        ],
        'count': sum(len(s['new_subtopics']) for s in refinement_splits)
    })

    # 7. Update metadata
    progress['_meta']['refinement_pass_done'] = True

    # If refinement found new subtopics, reset consecutive_empty counter
    # because the taxonomy just changed — need to verify stability again
    if refinement_splits:
        progress['_meta']['consecutive_empty_batches'] = 0
        print(f"\n  Refinement pass: {len(refinement_splits)} subtopics split into "
              f"{sum(len(s['new_subtopics']) for s in refinement_splits)} new subtopics.")
        print(f"  consecutive_empty_batches reset to 0 — resume scanning to verify stability.")
    else:
        print(f"\n  Refinement pass: no splits needed. Taxonomy depth is adequate.")

    from datetime import datetime, timezone
    progress['_meta']['last_updated'] = datetime.now(timezone.utc).isoformat()
    save_scan_progress(progress, exam_code)

def check_dimensional_splits(questions, sec, top, sub):
    """
    v2.4 REFINEMENT ANALYSIS — check if a subtopic should be split or merged.

    TWO-PHASE CHECK (v2.4 — merge-first, then split):

      PHASE A — MERGE CHECK (priority):
        If this subtopic frequently confuses with another subtopic during
        classification (tracked via confidence scores), recommend MERGE
        rather than split. Over-splitting causes data loss (MPPSC proof).

      PHASE B — SPLIT CHECK (only if no merge needed):
        For each of the 4 recorded metadata dimensions:
          1. Collect distinct values: Counter(q[dimension] for q in questions)
          2. Remove null values from consideration
          3. If >= 2 distinct values AND each has >= MIN_PATTERN_SIZE:
             → candidate split, BUT must pass Q3 Unique Domain Check:
               (a) Different solving approach?
               (b) Separate coaching chapter?
               (c) Unambiguous classification between proposed splits?

      CONCRETE EXAMPLE:
        Subtopic "Spotting Errors" with 30 classified questions:
          question_task: {identify_error: 30}  → NO split (1 value)
          question_format: {in_sentence: 30}   → NO split (1 value)
          question_direction: {null: 30}        → skip (all null)
          thematic_domain: {subject_verb: 8, tense: 7, pronoun: 5,
                           preposition: 4, article: 3, conjunction: 3}
                           → CANDIDATE split. Q3 check:
                             (a) Different approach? Debatable.
                             (b) Separate coaching chapter? Not usually.
                             (c) Unambiguous? A question about subject-verb
                                 agreement in a complex tense → ambiguous
                                 between "subject_verb" and "tense".
                           → Q3(c) FAILS → DON'T SPLIT.

    DIMENSION CHECK ORDER AND MERGE RULE:
      Check all 4 metadata dimensions. For each dimension that yields
      2+ clusters with >= MIN_PATTERN_SIZE:
        Record the candidate split.

      After checking all dimensions:
        - If 0 dimensions yielded splits → return empty (no split needed)
        - If 1+ dimensions yielded splits → select the MOST NATURAL split
          (the one whose clusters most clearly pass Q3 Unique Domain Check).
        - Do NOT blindly merge multiple dimension splits into a cross-product.
          Apply Q3(c) to every proposed subtopic pair — if any pair has
          ambiguous classification, merge those two back together.

    SPLIT DECISION CRITERIA (v2.4 — Q3 Unique Domain Check required):
      A split is warranted ONLY when ALL of:
        (a) ≥15 classified questions in the subtopic (MIN_QUESTIONS_FOR_SPLIT)
        (b) 2+ distinct values exist for a dimension with ≥3 each (MIN_PATTERN_SIZE)
        (c) The distinction passes Q3: different solving approach + separate
            coaching chapter + unambiguous classification
      If ANY condition fails → no split.

    Returns: list of {section, topic, old_subtopic, new_subtopics: [str]}
             or empty list if no split needed.
    """
    from collections import Counter as Ctr
    splits = []
    dims = ['question_task', 'question_format', 'question_direction', 'thematic_domain']
    for dim in dims:
        values = [q.get(dim) for q in questions if q.get(dim) is not None]
        counts = Ctr(values)
        valid = {k: v for k, v in counts.items() if v >= MIN_PATTERN_SIZE}
        if len(valid) >= 2:
            splits.append({'dimension': dim, 'clusters': valid})
    # Claude merges and names the subtopics using domain knowledge
    # Returns structured split recommendations
    pass
    # NOTE (v2.13): Claude produces the named `new_subtopics` at runtime, then MUST validate
    # them with the deterministic guards below before applying (D6-4/D6-5).
```

# ── v2.13 SPLIT GOVERNANCE GUARDS (register D6-4 over-split / D6-5 under-split) ──
# D6-4: after Claude proposes `new_subtopics` for a split, run split_children_valid();
#       any near-duplicate pair returned MUST be merged back (enforces Q3(c) — over-split
#       otherwise produces two subtopics that later collapse to one mechanic → false BV-10;
#       QV-13 (Step 5) + §4-1b (Step 6) are the downstream backstops).
# D6-5: when distinct forms are MERGED into one subtopic (len(questions) < 15, or Q3
#       ambiguous), call merge_record() and keep the record so Step 7's scenario_key can
#       still separate the merged forms (no silent loss of a distinct question form).

```python
# D6-4 / D6-5 split governance guards. Pure, deterministic.
import re, unicodedata

def _canon(s):
    s=unicodedata.normalize('NFC', s or '')
    for d in ('‐','‑','‒','–','—','−'): s=s.replace(d,'-')
    s=re.sub(r'\s+',' ',s).strip().casefold()
    return s

def _tokens(name):
    # tokenize; normalize trivial plural (trailing s/es) so "relations"=="relation"
    toks=[t for t in re.split(r'[^a-z0-9]+', _canon(name)) if t and t not in
          ('and','of','the','a','an','in','to','for','with','on','&')]
    return {re.sub(r'(es|s)$','',t) for t in toks}

def _jaccard(a,b):
    A,B=_tokens(a),_tokens(b)
    if not A or not B: return 0.0
    return len(A&B)/len(A|B)

def split_children_valid(children, sim_threshold=0.6):
    """D6-4 OVER-SPLIT guard. children = proposed split subtopic names. Returns list of
    (a, b, jaccard) pairs that are near-duplicates (ambiguous split) → the caller MUST
    merge those pairs back (enforces check_dimensional_splits Q3(c)). Empty = all distinct."""
    viol=[]
    for i in range(len(children)):
        for j in range(i+1, len(children)):
            if _canon(children[i])==_canon(children[j]):
                viol.append((children[i],children[j],1.0)); continue
            s=_jaccard(children[i],children[j])
            if s>=sim_threshold:
                viol.append((children[i],children[j],round(s,2)))
    return viol

def merge_record(kept_name, merged_forms, reason):
    """D6-5 UNDER-SPLIT record. When distinct forms are merged into one subtopic (below
    MIN_QUESTIONS_FOR_SPLIT or Q3-ambiguous), record the constituent forms so Step 7's
    scenario_key can still separate them. Returns a structured, serialisable record."""
    forms=sorted({f.strip() for f in merged_forms if f and f.strip()})
    return {'subtopic': kept_name.strip(), 'merged_forms': forms,
            'reason': reason, 'separate_by': 'scenario_key'}

# ── WIRING ──
# In check_dimensional_splits Q3(c) / the apply-splits loop:
#     viol = split_children_valid(split['new_subtopics'])
#     if viol:
#         # merge each near-duplicate pair back into one child, then re-name; do NOT emit
#         # two subtopics that a downstream mechanic would treat as identical.
#         ...  # collapse pairs in viol; record with merge_record(kept, [a,b], "Q3(c) near-dup")
# In the MERGE branch (subtopic kept whole because distinct forms are ambiguous/thin):
#     records.append(merge_record(sub, [f for f in distinct_forms], "below MIN_QUESTIONS_FOR_SPLIT"))
# These records travel with the taxonomy so Step 7 keeps the forms distinct at scenario_key.
```

```python
def reclassify_after_refinement(classifications, refinement_splits):
    """
    After refinement splits, update all existing classifications to use
    the new subtopic names instead of the old broad ones.

    For each split:
      - Find all classifications using old_subtopic
      - Re-examine each question's pattern metadata
      - Assign to the correct new subtopic
      - Update the classification dict in place
    """
    for split in refinement_splits:
        sec = split['section']
        top = split['topic']
        old_sub = split['old_subtopic']
        new_subs = split['new_subtopics']

        for paper_id, paper_classifs in classifications.items():
            for c in paper_classifs:
                if (c['section'] == sec and c['topic'] == top
                        and c['subtopic'] == old_sub):
                    # Claude re-examines the question's metadata and assigns
                    # to the best-fit new subtopic
                    c['subtopic'] = assign_to_refined_subtopic(
                        c, new_subs
                    )

def assign_to_refined_subtopic(classification, new_subtopics):
    """
    Given a classification dict with pattern metadata and a list of new
    subtopic names (from a refinement split), determine which new subtopic
    this question belongs to.

    Uses question_task, question_format, question_direction, thematic_domain
    to match against the new subtopic names.

    Claude performs this mapping using domain knowledge.
    Returns: the best-fit new subtopic name (str).
    """
    pass  # CLASS: J — Judgment over data already in context: maps a question to a refined subtopic. No tool call required.
```

### S3-7 — Session management for large corpora

```
EXPECTED THROUGHPUT (v1.7):
  Each chat session should process 4-5 complete batches (12-15 papers).
  If a session processes fewer than 3 complete batches, Claude MUST note
  this as below-target throughput in the batch-end message.

  Expected sessions: ~ceil(total_papers × MIN_COVERAGE_RATIO / 12) minimum.
    50 papers  → ~2 sessions
    100 papers → ~3 sessions
    200 papers → ~5-6 sessions

SESSION HANDOFF PROTOCOL:
  When context approaches capacity (after completing the current batch):
    1. Complete the current batch (never leave partial — EC-P26)
    2. Save scan_progress.json + classifications.json via present_files
       (EXACTLY these 2 files — S10-1 closed set. No other files.
        Run S10-2 pre-delivery checklist before present_files.)
    3. Print: "Session limit. [X]/[Y] papers scanned.
       Download scan_progress.json + classifications.json →
       upload to project knowledge.
       New chat → Step 2b: PYQScan PYQ: <<Drive link>>"
    4. END response. Do NOT process another batch.

RESUME PROTOCOL:
  New session loads:
    1. scan_progress.json from project knowledge (schema version checked)
    2. classifications.json from project knowledge
    3. RE-LIST Drive files (do NOT rely on cached inventory — files may
       have been added or removed between sessions). Update
       drive_file_inventory in scan_progress.json with fresh listing.
    4. RE-RUN S3-2a pre-scan gate: display full inventory with progress.
       Show "Previously scanned: [M] papers. Remaining: [N-M] papers."
       If total files differ from cached inventory → warn user:
         "Drive folder changed since last session: was [X] files, now [Y].
          [added/removed] files detected."
       User re-confirms before scanning resumes.
    5. Resume from first unscanned paper in round-robin queue
```

### S3-8 — Scan progress JSON schema

```json
{
  "_meta": {
    "exam_code": "[ExamCode]",
    "phase": "0b_scan",
    "schema_version": "2.0",
    "source_taxonomy": "taxonomy_draft.json",
    "source_taxonomy_subtopics": 209,
    "papers_scanned": 65,
    "total_available": 200,
    "years_covered": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "convergence_status": "converged",
    "consecutive_empty_batches": 7,
    "refinement_pass_done": true,
    "last_updated": "2026-07-02T10:30:00Z"
  },
  "taxonomy": {
    "Section 1 Name": {
      "Topic A": ["Subtopic A1", "Subtopic A2", "Subtopic A3"],
      "Topic B": ["Subtopic B1", "Subtopic B2"]
    }
  },
  "exam_config": { },
  "papers_scanned_list": ["Paper_12-Sep-2025_Shift-1_Q1-Q100", "..."],
  "drive_file_inventory": [
    {"name": "Paper_12-Sep-2025_Shift-1_Q1-Q100.docx",
     "id": "1jD5lA67...", "year": 2025, "size": 50629,
     "q_count": 100, "q_count_method": "parsed"}
  ],
  "discovery_log": [
    {
      "batch": 1,
      "papers": ["Paper_12-Sep-2025_Shift-1_Q1-Q100", "..."],
      "complete_batch": true,
      "new_subtopics": ["Section1/TopicA/NewSubtopic", "..."],
      "count": 3
    },
    {
      "batch": "refinement_pass",
      "papers": [],
      "new_subtopics": ["Section1/TopicA/SplitSubtopic1", "..."],
      "removed_subtopics": ["Section1/TopicA/OldBroadSubtopic"],
      "count": 5
    }
  ]
}
```

```
SEPARATE FILE — [ExamCode]_classifications.json:
{
  "Paper_12-Sep-2025_Shift-1_Q1-Q100": [
    {"q_num": 1, "section": "Section 1 Name",
     "topic": "Topic A", "subtopic": "Subtopic A1",
     "question_task": "find_match", "question_format": "word_pair",
     "question_direction": null, "thematic_domain": "profession_workplace"},
    {"q_num": 2, "section": "Section 1 Name",
     "topic": "Topic A", "subtopic": "Subtopic A2",
     "question_task": "find_match", "question_format": "mixed_alphanumeric",
     "question_direction": null, "thematic_domain": null}
  ]
}

scan_progress.json REQUIRED FIELDS (v1.7 — PYQApprove reads these):
  _meta.exam_code          (string)
  _meta.papers_scanned     (int, informational)
  _meta.refinement_pass_done (bool, must be True for approve)
  _meta.schema_version     (string, must be "2.0")
  taxonomy                 (dict — COMPLETE Section > Topic > [Subtopics])
  exam_config              (dict — from taxonomy_draft)

BANNED JSON FIELDS (v1.7 — Claude MUST NOT add any of these):
  convergence_recommendation, scan_analysis, recommendation,
  justification, assessment, analysis, suggestion, editorial,
  or ANY field not listed in the schema above.
```

---


---

# END OF Framework_PYQScan v1.2
