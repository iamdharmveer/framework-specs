# Framework_PYQPrepare v2.1 — Universal PYQ Row File Generator
# v2.1 — 2026-08-15 — GAP-2026-08-15-BAREQ (producer side). S1-4 contract rewritten: a
#   bare "Q.N" stem — OMML-only, figure-only, or empty/corrupt — is a LAWFUL normalised
#   form with a named reason, and "repairing" it by injecting filler ("Solve:") is now
#   PROHIBITED: filler is not in the source, survives into Step 5's extraction and into
#   every mock derived from the item, and corrupts the corpus it appears to fix.
#   CHECK 1/2/12/15/21 delegate to bc.detect_question_start() — they carried a PRIVATE
#   regex r'^Q\.\d+' that needed no trailing content, so Step 1 certified "Q-count = 60,
#   sequential OK" on a file Step 3 read as 56 and delivered it green. CHECK 13 calls
#   bc.is_bare_q_label(): it already had the right regex gated on the wrong payload test
#   (NEXT paragraph for a drawing, never the SAME paragraph for an equation) and now
#   reports OMML-only, figure-only and truly-empty stems separately. S2-4 sanitise() and
#   CHECK 7 widen to the zero-width class (U+200B/200C/200D/2060/FEFF), which str.strip()
#   does not remove and \s does not match, so "Q.4<ZWSP>" defeats every table entry while
#   looking correct on screen. NEW CHECK 22 (WARN, 21 -> 22): producer/consumer
#   Q-detection agreement — the <w:t>-only view vs the <w:t>+<m:t> view of the SAME
#   document, the one construction a shared blind spot cannot satisfy.
# v2.0 — 2026-08-07 — TIER-3 STRUCTURED MATH (GAP-2026-08-07-OMML, remedies M1/M2/M4/M5).
#   Root cause (measured on IIT_JAM_MATHEMATICS 15-Feb-2026, 60 questions): S1-13
#   emitted FLAT Unicode transcription, destroying 2-D math structure at capture
#   time; Tier-2 regex reconstruction then recovered only digit fractions and √N.
#   Result classes: letter-fraction flattening, ^/_ artefacts, inline big-operator
#   limits, cases/matrix structures PARAPHRASED into prose (Q.11/14/17/33/34/36/
#   37/49/52/56), hybrid-font islands, and the bare-label OMML option conflict.
#   Fix: (M1) S1-13 now REQUIRES ⟦MATH:…⟧ LaTeX-lite regions for all structural
#   math and BANS paraphrasing matrices/vectors/cases into prose, with declared
#   STRUCT_FLAGS; (M2) new S3-5b deterministic LaTeX-lite→OMML compiler (fractions,
#   radicals, scripts, n-ary with true operands, limLow, cases, matrices, sPre,
#   stretchy delimiters, accents, \binom, Greek/symbol map; STRICT CORE with a
#   FORGIVING BOUNDARY — a region the compiler rejects never halts the run and
#   never ships silently: it is delivered as ordinary plain text — no colour,
#   no highlight — and CHECK 20 quotes it verbatim for Ctrl+F, with the remedy
#   in plain operator words, under an F1 AMBER footer);
#   render_text_with_math() v2.0 dispatches Tier-3 regions first and
#   keeps the v1.5 legacy path byte-compatible for plain segments; (M3, in
#   corpus_io Cluster I) text_of() = w:t + m:t canonical accessor; CHECK 9 v2
#   accepts bare "N." labels whose payload is <m:oMath> (producer mirror of S-1);
#   (M4) CHECK 19 structure-residue, CHECK 20 region round-trip, CHECK 21 declared-
#   structure fidelity — 18 -> 21 checks; (M5) S4-1: OMML runs keep the Word math
#   font (Cambria Math italic), EXEMPT from the Arial rule.
#   Verified: 60-question rebuild, 142/142 regions compiled, 21/21 checks, page-
#   for-page structural render match against the source PDF.
# v1.14.1 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   317 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQPrepare'. The current companion block, the
#   v1.14 entry, and all structural notes remain in-file. Body byte-untouched.
# [ExamCode] project | Step 1 (PYQPrepare) | Exam-agnostic
#
# PURPOSE:
#   Convert one raw PYQ (Previous Year Question) exam paper from any source
#   format into a standardised Row file (.docx). The Row file is the universal
#   input that Steps 2–11 consume. Step 1 is the normalisation layer — it
#   absorbs ALL source-format complexity so that every downstream step sees
#   an identical, predictable document structure regardless of exam or source.
#
# REPLACES:
#   TestSeriesRow Tier 1 v17 (SSC CGL Tier 1 specific)
#   TestSeriesRow Tier 2 v3  (SSC CGL Tier 2 specific)
#   This framework is exam-agnostic — same spec for ALL exams.
#
# PIPELINE POSITION:
#   Step 1 PYQ Prepare  → THIS SPEC (raw exam dump → Row file .docx)
#   Step 2a PYQ Draft   → syllabus + taxonomy_draft.json + exam_config.json
#   Step 2b PYQ Scan    → discover subtopics from PYQ content
#   Step 2c PYQ Approve → approved Analysis docs + exam_config.json
#   Step 3 PYQ Sort     → 1 Row file → 1 Sorted PYQ
#   Step 4 PYQ Count    → fill PYQ counts in Analysis docs
#   Step 5 PYQ Extract  → Sorted PYQ → section_rules.md + manifest + Frequency xlsx
#   Step 6 Mock Blueprint → Analysis docs + Frequency xlsx → blueprint.json
#   Steps 7–11          → Mock test creation pipeline
#
# PREREQUISITE:
#   None. Step 1 is the first step in the pipeline. The exam project may be
#   completely empty — Step 1 is fully self-contained from two inputs:
#     1. Trigger text (ExamCode + date + optional session)
#     2. Attached raw exam paper (PDF or other format)
#   No exam_config.json, no project knowledge files required.
#
# INPUTS:
#   1. One raw exam paper — attached to chat (PDF, ZIP, docx, or any format)
#   2. Trigger text with ExamCode, date, and optional session keyword+number
#   (1 exam paper per trigger. Never bundled multi-session files.)
#
# OUTPUT:
#   One Row file (.docx) — delivered via present_files.
#   (1 file, nothing else. Deliverable set is CLOSED.)
#   User downloads → uploads to [ExamCode] project Files or Google Drive PYQ folder.
#
#   DO NOT DELIVER:
#     ✗ pipeline.py (execution script — stays in /home/claude/)
#     ✗ Any intermediate or working files
#     ✗ Any JSON, log, or image files generated during extraction
#     ✗ The input raw exam paper
#     ✗ Answer key in any form (JSON, text, or embedded in Row file)
#
# TRIGGER FORMAT:
#   Step 1: PYQPrepare [ExamCode] [DD-Mon-YYYY] [<session_keyword> <N>]
#   Trigger matching is case-insensitive for the keyword.
#   ExamCode: alphanumeric + underscore (e.g. SSC_CGL_T1, GATE_CS, IBPS_PO)
#   Date: DD-Mon-YYYY (e.g. 18-Jan-2025). Mon = 3-char English abbreviation.
#   Session: OPTIONAL. Keyword + number (e.g. Shift 1, Slot 2, Session 1).
#            If omitted, date label in output contains date only — no session.
#
#   Examples:
#     Step 1: PYQPrepare SSC_CGL_T1 [18-Jan-2025 Shift 1]
#     Step 1: PYQPrepare GATE_CS [09-Feb-2025 Session 1]
#     Step 1: PYQPrepare UPSC_CSE [02-Jun-2024]
#     Step 1: PYQPrepare IBPS_PO [14-Oct-2023 Slot 3]
#
# RUNS IN: [ExamCode] project (exam-specific). Project may be empty on first run.
#
# EXECUTION MODEL:
#   Two-phase: Inspect → Build.
#   Phase A (Inspect): Claude reads/inspects the source file using bash_tool
#     and/or view to understand source format, layout, question count, sections,
#     edge cases. 1–3 exploratory tool calls.
#   Phase A-IMAGE (v1.6): If source has embedded images, Claude extracts them,
#     views each using the view tool, and classifies/transcribes content.
#     1–8 additional view calls depending on image count.
#   Phase B (Build): Claude writes a complete pipeline.py (including
#     IMAGE_CLASSIFICATIONS dict from Phase A-IMAGE), runs it, validates,
#     and delivers. 3–4 tool calls (create_file → bash run → bash verify →
#     present_files).
#   Total: 5–15 tool calls (image-count-dependent). No user "Continue" needed.
#   Claude self-fixes on failure — iterate until validation passes.
#
# EXAM-AGNOSTIC GUARANTEE:
#   Zero hardcoded exam values in this spec. All exam-varying information
#   comes from the trigger (ExamCode, date, session) and from the source
#   file content (questions, options, sections). Same spec runs for SSC CGL,
#   GATE, NEET, UPSC, CAT, Banking, RRB, state PSC, or any exam.
#
# VERSION HISTORY:
#   v1.14 — 2026-07-29 — DI TABLE STRUCTURE, BLOCK COMPOSITION AND CELL CONTENT
#           (GAP-2026-07-29-TBL). This spec could say what a table CONTAINS and never
#           what a table IS. S1-12 CATEGORY 2 transcribed "a list of rows" and S4-3
#           wrote cell.text into a rectangular add_table(), so a grouped header had
#           exactly one representable form: squared into a grid and padded with empty
#           strings. Measured on SSC_CGL_Tier1 09-Sep-2024 Shift 1 — Q.52 and Q.61 each
#           lost a 4-column header span and a 2-row label span and gained 4 stray empty
#           cells, while Q.74 passed because ITS header is flat. That is why the gap
#           survived to v1.13: the worked example in S1-12 and in EC-P20b is flat too,
#           so a model that cannot express a span was never once exercised against one.
#           The delivered Row file carried 0 gridSpan and 0 vMerge elements and passed
#           16/16 checks with a green F2 footer, because no check in this framework has
#           ever compared a built table with its source.
#           SECOND DEFECT, SAME FAMILY: S1-7 and S4-2 emitted one table PER OPTION, and
#           two adjacent w:tbl siblings are FUSED into a single table by every Word
#           engine. Measured: 19 tables as written came back from a Word-engine
#           round-trip as 7. It is invisible in the emitted file — python-docx reports
#           19 — which is why it went unnoticed for the life of the spec.
#           Fix: (1) new S1-8a TABLE STRUCTURE CONTRACT — the TableSpec model, anchor
#           cells with cs/rs, padding BANNED; a blank cell is now distinguishable from
#           padding STRUCTURALLY rather than by heuristic.
#           (2) S4-3 build_di_table DELEGATED to corpus_io (Cluster I) — HTML-style
#           occupancy placement, cell.merge() strictly AFTER text placement (merge
#           CONCATENATES: 'A'+'B' -> 'A\nB'), per-cell column widths, centred default.
#           Two builders modelled one concept and both were flat; one model, one owner.
#           (3) S1-6 and S1-11 scope EXTENDED to table cells — cells now render through
#           render_text_with_math, so a fraction, a superscript or an underlined term
#           inside a DI table is no longer silently flattened. That is the v1.3-v1.6
#           math defect, relocated into tables and unaddressed until now.
#           (4) new S1-8b BLOCK COMPOSITION — no two adjacent block tables; a figure-
#           option SET is ONE table with one row per option, which is also the better
#           match for the ALL-or-NONE rule in S1-7.
#           (5) new S2-2 CALL A2b — text-layer tables are DETECTED and transcribed
#           instead of being parsed as stem prose. S1-12 fires only on embedded images,
#           so a vector-drawn DI table in a FORMAT A source never entered the table
#           protocol at all.
#           (6) new CHECK 17 (geometry equality, declared vs built), CHECK 17b (padding
#           signature, legacy path only), CHECK 18 (no adjacent block tables).
#           16 -> 18 checks.
#           (7) new EC-P24 (table structure, 8 sub-scenarios) and EC-P25 (adjacent
#           block tables). EC-P14 and EC-P20b rewritten; "preserve source data exactly"
#           governed VALUES and was silently read as covering STRUCTURE.
#           (8) an unrepresentable structure is REPORTED, never silently normalised —
#           the EC-V8 / EC-P22 principle extended from images to tables.
#           REQUIRES corpus_io with Cluster I table structure (normalise_table_spec,
#           place_cells, build_di_table, read_table_spec, adjacent_table_pairs) AND the
#           anchor-only _table_rows. Shipping the writer without the reader turns lost
#           geometry into DUPLICATED header text in every consumer: python-docx
#           row.cells returns one entry per GRID COLUMN and repeats the anchor for every
#           covered position. The two halves ship together.
---

## §1 — OUTPUT CONTRACT (immutable — all downstream steps depend on this)

The Row file is the universal exchange format between Step 1 and Steps 2–11.
Every rule in this section is a HARD CONTRACT — violating any rule breaks
downstream steps. PYQSort, PYQAnalyse, and MockTestAnalyse all reference
this contract and raise errors pointing to Step 1 if violations are detected.

### S1-1 — Document-level properties

```
Page size   : A4 (8.27 × 11.69 inches = 595 × 842 points)
Margins     : 1 inch (914400 EMU) all four sides
Font        : Arial 11pt throughout (body, stems, options, date labels)
              Exception: DI table cells may use source font size (typically 9pt)
space_before: 0 on all paragraphs (Pt(0))
space_after : 0 on all paragraphs (Pt(0))
```

### S1-2 — Per-question block structure

Every question in the Row file follows this exact sequence:

```
┌─────────────────────────────────────────────────────────────┐
│  1. DATE LABEL         (right-aligned, bold, navy #003366)  │
│  2. STEM               (left, bold, "Q.N  <stem text>")     │
│     [2a. INSTRUCTION]  (plain — passage instruction line)   │
│     [2b. PASSAGE]      (plain — passage body paragraphs)    │
│     [2c. STEM IMAGE]   (red placeholder — IF figure stem)   │
│  3. OPTIONS            (indented 18pt, not bold, "N. text") │
│     [3a. OPTION IMAGES](placeholder table — IF figure opts) │
│  4. BLANK LINE         (empty paragraph separator)          │
└─────────────────────────────────────────────────────────────┘

For NAT questions (no options): block 3 is absent.

Q.N-FIRST (MANDATORY — aligns with MockTestCreate v3.7 R-LINKED):
  Every question block — single OR passage-linked — MUST OPEN with
  its "Q.<N>" paragraph (line 2). NOTHING may precede the Q-number
  except the date label. No passage, instruction line, table, chart,
  or preamble may appear before Q.N.

For passage questions: the Q.N stem line comes FIRST (bold), then
the instruction line (e.g. "Read the given passage and answer the
questions that follow.") as a plain paragraph, then the passage body
paragraph(s) as plain text, then options. Regardless of how the
SOURCE ordered these elements, the OUTPUT always uses Q.N-FIRST.

Example (RC):
  [18-Jan-2025 Shift 1]                                  ← date label
  Q.97  How did Subhas Chandra Bose view India's...      ← Q.N stem (bold)
  Read the given passage and answer the questions...     ← instruction (plain)
  Subhas Chandra Bose, a prominent Indian ...            ← passage body (plain)
  1. Through political negotiations                       ← options
  2. Through economic sanctions
  ...

Example (Cloze):
  [18-Jan-2025 Shift 1]                                  ← date label
  Q.90  Select the most appropriate option for blank 1.  ← Q.N stem (bold)
  In the following passage, some words have been...      ← instruction (plain)
  The economy of a country depends on ...                ← passage body (plain)
  1. option text                                          ← options
  ...
```

### S1-3 — Date label format

```
WITH session:    [DD-Mon-YYYY <session_keyword> <N>]
WITHOUT session: [DD-Mon-YYYY]

Properties:
  Alignment  : RIGHT
  Font       : Arial 11pt Bold, Navy #003366
  Italic     : NEVER
  Brackets   : included in text (literal [ and ])
  Month      : 3-char English abbreviation (Jan, Feb, Mar, ...)
  Day        : 1 or 2 digits (no zero-padding required, but accepted)

Examples:
  [18-Jan-2025 Shift 1]
  [09-Feb-2025 Session 1]
  [2-Jun-2024]

One date label per question — MANDATORY. No question may exist without
a preceding date label. PYQSort EC-S10 raises ValueError if violated.
```

### S1-4 — Question numbering

```
Format    : Q.<N>  (Q dot number, two spaces before stem text)
Numbering : Continuous Q.1 → Q.N across entire paper
Sections  : MERGED — if source has per-section numbering (e.g. Math Q.1–30,
            Reasoning Q.1–30), Step 1 renumbers continuously (Q.1–Q.60).
Separators: NONE — no === module separators === in output.
            Section information is not preserved in the Row file.
            Step 2b (PYQScan) classifies each question into taxonomy.
Gaps      : FORBIDDEN — every integer from 1 to N must appear exactly once.
Duplicates: FORBIDDEN — no Q.N may appear more than once.

The stem paragraph is BOLD. Format: "Q.N  <stem text>" where N is the
continuous number. Two spaces separate Q.N from stem text.

Empty/corrupt questions (no stem, no image), and questions whose ENTIRE
stem is a single OMML equation or a single figure, are emitted as a bare
"Q.N" paragraph whose <w:t> text layer holds only the label.

This is a LAWFUL normalised form, not a defect to be repaired.
blueprint_core.Q_PATTERNS entries 3 and 4 exist for it
(GAP-2026-08-15-BAREQ), and CHECK 22 proves the producer and the consumer
agree about it on every delivered file.

It must NEVER be "repaired" by injecting filler text such as "Solve:" or
"Find the value of". Filler is not in the source. It survives into Step 5's
extracted stem, into section_rules.md, into PYQ_STEM_PATTERNS and into every
mock question derived from the item — it corrupts the corpus it appears to
fix, permanently and invisibly. If a Row file was hand-edited this way while
the defect was open, revert the edit and re-run Step 3; the Row file was
never wrong, only the reading was.
```

### S1-5 — Option format (canonical)

```
ALL source option formats are normalised to this single canonical format:

  N. <option text>

Where N is 1, 2, 3, 4, 5 (or however many options the source has).

Source formats that get normalised:
  (a) text  → 1. text
  (A) text  → 1. text
  A. text   → 1. text
  a) text   → 1. text
  1) text   → 1. text
  (1) text  → 1. text

Properties:
  Alignment   : LEFT (no explicit alignment set)
  Indent      : 18pt (228600 EMU) left indent
  Font        : Arial 11pt, NOT bold
  Spacing     : "N. " (number, dot, space, then text)
  Line layout : Each option on its OWN paragraph — NEVER two options on same line

Option count is NOT hardcoded. Extract ALL options found per question.
Could be 2, 3, 4, 5, or more. Downstream steps validate against
exam_config.options_count.

NAT questions: ZERO options. Stem only. This is valid.
MSQ questions: Normal options, same format. Multiple-correct marking
is a downstream concern (Step 7), not a Step 1 concern.

CROSS-STEP CONTRACT:
  This canonical format matches OPT_PATTERNS[0] in Steps 3/5:
    r'^([1-5])\.\s+(.+)'
  Steps 3, 5, and 2b all use the 5-pattern OPT_PATTERNS list which
  includes this format as the FIRST pattern — guaranteed match.
```

### S1-6 — Math rendering (OMML — mandatory)

```
All mathematical content in stems, options AND TABLE CELLS MUST be rendered
using OMML (Office MathML) or Unicode math symbols. No red-box substitution
for math.

v1.14 — TABLE CELLS ARE IN SCOPE. Before v1.14 this clause said "stems AND
options" and S1-8 said nothing about math at all, so the intersection was
governed by neither: S4-3 wrote cell.text directly and a fraction, a
superscript or a ₹ figure inside a DI table was silently flattened to plain
text. That is the v1.3-v1.6 math defect relocated into tables. Cell content
now goes through render_text_with_math() like every other string (S1-8a).

OMML required for:
  Fractions     : 7/12, 1/4, x/2 → <m:f> fraction element
  Mixed numbers : 12⅓, 3(2/3) → <m:f> with integer prefix
  Superscripts  : cm², m³, x², cos²θ → <m:sSup>
  Subscripts    : CO₂, H₂O, a₁ → <m:sSub>
  Square roots  : √15, √(x²−9) → <m:rad> with degHide=1
  Nth roots     : ³√8, ⁴√16 → <m:rad> with visible <m:deg> (v1.4)
  Complex       : combinations of the above

  COMPOUND EXPRESSIONS (v1.3 — mandatory nested OMML):
    1/√3      → <m:f> with <m:rad> in denominator
    √3/2      → <m:f> with <m:rad> in numerator
    1/(2√3)   → <m:f> with compound denominator [text "2" + <m:rad>3]
    3√5/7     → <m:f> with compound numerator [text "3" + <m:rad>5]
    These MUST render as nested OMML elements. Leaving √ or SQRT markers
    as literal text inside <m:t> is a HARD BUG — see build_compound_content()
    in §3 S3-4.

FOUR-TIER MATH HANDLING ARCHITECTURE (v2.0):

  TIER 3 — STRUCTURED ⟦MATH:…⟧ REGIONS (PRIMARY for vision-transcribed and
    any structurally rich source — v2.0, S3-5b):
    The transcription buffer wraps every non-trivial expression in
    ⟦MATH: LaTeX-lite ⟧. render_text_with_math() compiles each region into
    ONE homogeneous <m:oMath> via the deterministic S3-5b compiler:
      \frac \sfrac \sqrt \root  →  <m:f> / <m:rad>
      base^{…} base_{…}            →  <m:sSup>/<m:sSub>/<m:sSubSup>
      \int \iint \oint \sum \prod \sumi \prodi  →  <m:nary> whose
        <m:e> is the TRUE OPERAND (rest of the enclosing scope — correct
        nesting, no placeholder box in any engine)
      \lim \max \min _{…}        →  <m:limLow>
      \cases{…&…\\…}              →  <m:d begChr="{"> + <m:eqArr>
      \pmatrix \bmatrix \vmatrix \matrix  →  <m:d> + <m:m>
      \pre{sub}{sup}{base}         →  <m:sPre>   (ⁿCᵣ prescripts)
      \paren \brack \set \abs     →  stretchy <m:d>
      \sin \cos … \log \text{…}   →  roman (m:sty="p") runs
    STRICT CORE, FORGIVING BOUNDARY: an unknown command or malformed
    region raises MathCompileError inside the compiler, and the RENDERER
    catches it — the region is DELIVERED as ordinary plain text (no colour,
    no highlight), quoted verbatim in the CHECK 20 report so the operator
    can Ctrl+F straight to it, and explained in plain words. The run
    never halts; the defect never ships invisibly. The grammar also maps
    common LaTeX habits (\alpha…\Omega, \le \ge \in \to \infty …,
    \hat \bar \vec accents, \binom) so degradation is rare in practice.
    Regex reconstruction of structure is inherently lossy; structure is
    captured at the source instead (GAP-2026-08-07-OMML root cause).

  TIER 1 — PIPELINE-LEVEL DETECTION (deterministic text sources):
    During Phase B, Claude's pipeline.py detects math expressions in the
    source text and calls OMML helpers directly. This handles ALL patterns
    including complex ones that no regex safety net can parse:
      - Trig fractions: (secθ − tanθ)/(secθ + tanθ)
      - Expressions with operators: (a⁷ × b⁸)/(a⁹ × b⁵)
      - Nth roots: ³√6859, ⁴√1296
      - Multi-OMML compounds: option with 2+ separate OMML elements
      - Negative fractions with sign: −13/27
      - Any source-format-specific math detection
    This tier is written fresh by Claude for each exam's source format.
    The OMML helpers (omml_frac, omml_sqrt, omml_nthroot, omml_sup,
    omml_sub) are the building blocks used at this tier. Prefer emitting
    ⟦MATH:…⟧ regions (Tier 3) over hand-built helper calls wherever the
    expression has any structure.

  TIER 2 — render_text_with_math() SAFETY NET (plain segments only):
    When the pipeline passes text to add_stem() or add_option(), the
    render_text_with_math() function scans for RESIDUAL math patterns
    that the pipeline missed. It handles:
      - Simple numeric fractions: 1/2, 7/12
      - Fractions with √: 1/√3, √3/2, 2√3/5, 1/2√3
      - Mixed numbers: 3(1/3), 12(2/5)
      - Standalone √N: √3, √15
      - Residual ⟦SQRT:N⟧ or [SQRT:N] pipeline markers
    It does NOT handle complex expressions (trig, operators, variables) —
    those are Tier 3's (or, for deterministic sources, Tier 1's) job.
    Tier 2 runs ONLY on text outside ⟦MATH:…⟧ regions.

  TIER 4 — VALIDATION (CHECK 11 + CHECK 19/20/21, v2.0):
    After the document is built, CHECK 11 scans for residual markers,
    CHECK 19 scans plain <w:t> runs for structure that should have been a
    ⟦MATH:⟧ region (carets, _x subscript artefacts, √(expr), letter
    fractions), CHECK 20 proves the region→<m:oMath> round-trip count, and
    CHECK 21 proves every DECLARED matrix/cases structure was built. Any
    occurrence is a WARN requiring investigation.

Unicode (NOT OMML) for:
  Polynomial superscripts in bold stem runs: x³ − 4x² − 8x + 11
    Use Unicode: \u00b2 (²), \u00b3 (³), \u2212 (−)
    Reason: OMML inside bold runs creates x□² rendering artifact
  Standalone math symbols: ° θ π ∆ ≤ ≥ ≠ √ ₹ ∠ ∞
    Preserve verbatim from source when OCR/text extraction captures them

DO NOT flag as OMML-required:
  km/h, m/s, ₹X/kg, and/or — these are plain text ratios/units

Image-rendered math (source has math as embedded image):
  If the source renders a math expression as an embedded image and the
  text extraction produces NO usable text for that expression, DO NOT
  automatically assign a red placeholder. Instead, follow the IMAGE
  INSPECTION PROTOCOL (S1-12):
    1. Extract the image to disk during Phase A
    2. Claude views the image using the view tool
    3. If the image contains math/text/table content → Claude transcribes
       the content and the pipeline writes it as text + OMML
    4. If the image is genuinely unreadable (corrupt, blank, too low
       resolution) → red placeholder + WARN in delivery
       v1.11: permitted ONLY when THIS IMAGE'S cell was OBSERVED in Phase B.
       With vision unavailable every image looks unreadable, so this branch
       would placeholder ALL math — the exact failure the rule below forbids.
       image_clarity=='vision_unavailable' → leave the image untouched and
       complete the run, never placeholder. The run does NOT halt.

  Red placeholders for math content are BANNED. The ONLY legitimate
  placeholder for a math question is when the image is physically
  unreadable after Claude has viewed it. "No extractable text" is NOT
  sufficient reason — Claude's vision capability is the fallback.
  v1.9 corollary: if Claude CANNOT view, the fallback is unavailable and the
  correct action is to stop, not to guess. A placeholder assigned without a
  passing probe is indistinguishable from a placeholder assigned to real math.

  See S1-12 for the complete image classification and transcription
  protocol, and EC-P20 for the 8-scenario edge case taxonomy.
```

### S1-7 — Visual content handling (red placeholders)

```
PREREQUISITE (v1.6): Every embedded image in the source MUST be
classified via the Image Inspection Protocol (S1-12) BEFORE any
placeholder is assigned. Assigning a red placeholder to an
unclassified image is a HARD BUG. Only images classified as
VISUAL-IMAGE get red placeholders. Images classified as MATH-IMAGE,
TEXT-IMAGE, or TABLE-IMAGE get transcribed content instead.

PREREQUISITE (v1.11): THIS IMAGE'S CELL must have been OBSERVED in Phase B
(S1-12) before a red placeholder may be assigned to it. A classification is a
claim about what an image contains; a session that did not look at it is not
entitled to make one. The gate is now PER IMAGE rather than per session,
which is strictly stronger: a session whose vision worked for 40 images and
lapsed for 3 may placeholder none of those 3.
  image_clarity == 'unclear'            -> placeholder PERMITTED (earned)
  image_clarity == 'vision_unavailable' -> placeholder FORBIDDEN; leave the
                                           image untouched, complete the run,
                                           report it, render F1 amber.
A red placeholder assigned to an unobserved image is a HARD BUG of the same
rank as an unclassified image, because on the page the two are
indistinguishable from a placeholder that was genuinely earned.

Non-math visual content (geometric figures, dice patterns, Venn diagrams,
mirror images, bar charts, map-based questions, pattern grids, embedded
photographs) → RED SUBSTITUTE IMAGE.

Red placeholder specification:
  Size  : 300 × 200 pixels
  Color : RGB (220, 30, 30) — solid red
  Format: PNG

Generation (once at script start):
```

```python
from PIL import Image
RED_PNG = f"{WORK_DIR}/placeholder_red.png"
Image.new("RGB", (300, 200), (220, 30, 30)).save(RED_PNG)
```

```
Placement rules:

  FIGURE STEM (question with image-only or image-supplemented stem):
    Render as: Q.N paragraph (bold) + red placeholder inline image
    If stem has text + figure: keep stem text, add placeholder after it
    If stem is image-only (no text): Q.N paragraph only, placeholder follows

  FIGURE OPTIONS (any option is blank / image-only):
    Detection: option line matches ^\s*[1-5]\.\s*$ (empty after number)
    When ANY option is blank: ALL options get red placeholders
    Render as: ONE 2-column borderless table for the WHOLE option set —
      one ROW per option (label | image). NOT one table per option.
    Keep the text stem above the option placeholder table

    v1.14 (GAP-2026-07-29-TBL): "one table per option" emitted four adjacent
    w:tbl siblings, and two adjacent block tables are FUSED into a single table
    by every Word engine (S1-8b). Measured: a Row file written with 19 tables
    came back from a Word-engine round-trip with 7. One table for the set is
    fusion-proof AND the better match for the ALL-or-NONE rule above — the set
    is one unit, so it is one element.

  TEXT OPTIONS with figure stem:
    Keep options as plain text. Only stem gets placeholder.

  PURE TEXT question (no figures):
    No placeholder.

Team manually replaces all red placeholders with actual images after
delivery. Step 1 only positions placeholders correctly.
```

### S1-8 — DI / Statistics tables

```
Every data interpretation table, frequency table, statistics table, or
any structured tabular data in the source → NATIVE WORD TABLE.

STRUCTURE (mandatory, v1.14): the built table MUST reproduce the source's
CELL GEOMETRY — horizontally merged (colspan) and vertically merged (rowspan)
cells, at every header tier and in the body. A merged cell in the source MUST
be a merged cell in the output. Squaring a merged table into a rectangle padded
with empty cells is a HARD BUG of the same rank as placeholdering readable
math: the values survive, the meaning does not, and no downstream step can
reconstruct what was discarded.
  "Preserve source data exactly" (below) governs VALUES. It was silently read
  as covering STRUCTURE for thirteen versions, which is how a two-tier header
  came out flat with four stray empty cells and passed 16/16 checks.

DATA MODEL: tables are transcribed and carried as a TableSpec (S1-8a).
ANCHOR CELLS ONLY — padding a row with '' to square the grid is BANNED.

CONTENT: cell text renders through render_text_with_math() exactly as stems and
options do (S1-6, S1-11) — OMML math and {{u}} underline markers are honoured
INSIDE cells.

PRESENTATION: 'Table Grid' style. Preserve source data exactly. Font size in
table cells may differ from body font (typically 9pt) — this is acceptable.
Cells are CENTRE-aligned by default; per-table and per-cell overrides are
permitted. Column widths follow TableSpec.col_widths when present, else equal
distribution. Width MUST be stamped on EVERY CELL of a column — tblGrid alone
is advisory and several renderers ignore it.

BLOCK COMPOSITION: see S1-8b.

Never render tables as images or placeholders.
```

### S1-8a — Table structure contract (v1.14 — TableSpec)

```
The TableSpec is the ONE model for tabular data across the pipeline. Step 1
writes it, Step 7 rebuilds from it, Steps 3/4/5 read it back. It is OWNED BY
corpus_io (Cluster I) and is never re-implemented in a spec — two builders
modelled one concept before v1.14 (S4-3 here, S8-4 in Framework_MockTestCreate)
and BOTH were flat, which is exactly the drift the delegation rule exists to
prevent.

  TableSpec := {
    'grid'        : [[Cell, ...], ...],   # REQUIRED, row-major, ANCHOR CELLS ONLY
    'header_rows' : int,                  # OPTIONAL, default 1
    'col_widths'  : [float, ...] | None,  # OPTIONAL, relative weights
    'align'       : 'left'|'center'|'right',   # OPTIONAL, default 'center'
    'note'        : str | None,           # OPTIONAL, footnote rendered below
  }

  Cell := str                             # == {'t': str, 'cs': 1, 'rs': 1}
        | {'t': str, 'cs': int, 'rs': int, 'align': str|None, 'bold': bool}

THE RULE THAT REMOVES THE AMBIGUITY — ANCHOR CELLS ONLY. A row declares only
the cells that START in it. A position covered by a span from above or from the
left is NOT declared. Padding is therefore impossible to express, and a
genuinely blank cell ({'t': ''} — the classic empty top-left corner) is
distinguishable from padding STRUCTURALLY rather than by heuristic.

GRID WIDTH IS COMPUTED, NEVER DECLARED, by corpus_io.place_cells(), which runs
the standard HTML occupancy algorithm. A row that under-declares produces a
'hole'; a row that over-declares produces an 'overlap'. Both are TRANSCRIPTION
ERRORS and both are REPORTED (ValueError) — never silently normalised. Silent
normalisation is the defect this contract exists to end.

BACK-COMPATIBILITY: a bare list of lists of strings is a valid 'grid'. Every
pre-v1.14 call site keeps working unchanged; a flat table has no spans to lose.

WORKED EXAMPLE — a two-tier header, as the source renders it:

  {'grid': [
     [{'t': 'Days', 'rs': 2},  {'t': 'Printers', 'cs': 4}],
     [{'t': 'L'}, {'t': 'M'}, {'t': 'N'}, {'t': 'O'}],
     ['Friday',   '10,230', '9580',  '7560', '9600'],
     ['Saturday', '8540',   '11,230','6580', '7890'],
     ['Sunday',   '9235',   '8264',  '7546', '10,325'],
   ],
   'header_rows': 2,
   'col_widths': [2.0, 1.0, 1.0, 1.0, 1.0]}

  Row 0 has TWO entries because the source shows two cells. Row 1 has FOUR,
  because its first position is covered by the 'Days' rowspan. That is the whole
  model.

UNREPRESENTABLE STRUCTURE IS REPORTED, NEVER NORMALISED. A diagonally split
corner cell, a nested table, a rotated header, or meaning carried by shading
alone cannot be expressed here. Transcribe the closest faithful structure, set
spec['note'] or record a transcription warning naming the question, and surface
it in the delivery report. This is EC-V8 ("queued, flagged, counted; never
dropped") and EC-P22 ("leave it and report it") extended from images to tables:
once the source is out of view, a silent normalisation is indistinguishable
from a faithful transcription.
```

### S1-8b — Block composition (v1.14 — adjacent tables fuse)

```
Two consecutive <w:tbl> siblings with NO <w:p> between them are rendered as a
SINGLE table by every Word engine. This is an OOXML block rule, not a renderer
quirk, and it is INVISIBLE in the emitted file: python-docx reports N tables
where Word shows one. Measured on the SSC_CGL_Tier1 09-Sep-2024 Shift 1 Row
file — 19 tables as written, 7 after a Word-engine round-trip, four clusters of
four option-placeholder tables fused into four 4-row tables.

RULE B1: no two block-level tables may be emitted as adjacent siblings. A
builder that appends a table MUST guarantee that the preceding body sibling is
a paragraph.

RULE B2 (preferred): a figure-option SET is ONE table with one row per option
(S1-7), not one table per option.

RULE B3 (fallback where B2 is impractical, e.g. two DI tables in one question):
emit an empty separator paragraph (space_before = space_after = 0) between them.

RULE B4: a question block that ENDS with a table must still be followed by the
S1-2 block-4 blank paragraph before the next date label. This is already true of
the block contract and must not regress — it is what keeps a trailing DI table
from fusing with the pill table Framework_PYQFormat S5-1 inserts before the next
Q-stem.

CHECK 18 enforces B1 mechanically.
```

### S1-9 — Passage handling (comprehension / cloze / DI / case study)

```
RULE 1 — REPETITION: Repeat the full passage text for EVERY sub-question
that depends on that passage. This applies to ALL passage-dependent
question types across ALL exam subjects:
  - English RC (Reading Comprehension)
  - English Cloze (fill-in-the-blanks)
  - Data Interpretation passages (scenario + questions)
  - Case study passages (MBA/law exams)
  - Statement-based grouped questions
  - Any other shared-context question group

RULE 2 — Q.N-FIRST LAYOUT (MANDATORY): Regardless of source ordering,
the output ALWAYS places Q.N BEFORE the passage. The fixed block order
for every passage-linked question is:

  Date label  →  Q.N stem (bold)  →  instruction line (plain)
  →  passage body (plain)  →  options  →  blank line

BANNED: placing instruction line or passage paragraphs BEFORE Q.N.
Even if the source has passage-first layout, Step 1 REORDERS to
Q.N-first in the output. This aligns with MockTestCreate v3.7
Q.N-FIRST rule (R-LINKED, G-QNUM-FIRST).

The Q.N stem line contains the SPECIFIC QUESTION text (e.g.
"Q.97  How did Subhas Chandra Bose view India's fight for
independence?"). The instruction line ("Read the given passage and
answer the questions that follow." / "In the following passage, some
words have been deleted...") is a SEPARATE plain paragraph that
follows the Q.N stem and precedes the passage body.

Passage rendering:
  Font      : Arial 11pt, NOT bold (plain text)
  Alignment : LEFT (no explicit alignment set)
  Position  : ALWAYS after Q.N stem, before options (see RULE 2)

Strip instruction labels: "Comprehension:", "SubQuestion No : N",
and similar metadata labels. Keep the passage body and instruction
line ("Read the given passage and answer..." / "In the following
passage, some words have been deleted...").
```

### S1-10 — Multi-paragraph stems

```
Questions with structured blocks (assertion-reason, statement I/II,
cause-effect, multi-premise) often span multiple paragraphs in source.

RULE: Merge into a SINGLE paragraph with \n line breaks within the
bold stem run. Each labelled line gets its own line within the paragraph.

Example source:
  Q.5  Read the statements and select the correct answer.
  Statement I: The Earth revolves around the Sun.
  Statement II: The Moon revolves around the Earth.

Output (single paragraph, bold):
  Q.5  Read the statements and select the correct answer.\n
  Statement I: The Earth revolves around the Sun.\n
  Statement II: The Moon revolves around the Earth.

This preserves readability while keeping the stem as one parseable unit.
PYQSort EC-S8 handles multi-paragraph stems but single-paragraph is cleaner.
```

### S1-11 — Inline formatting preservation (v1.5 — underline)

```
RULE: Semantically significant inline formatting in stems and passage
sentences MUST be preserved in the Row file output. The primary case
is UNDERLINE — used in vocabulary, error detection, and sentence
improvement questions where the question explicitly references
"the underlined word/part/phrase."

Without the underline, the question is NONSENSICAL. This is a HARD BUG
with the same severity as missing a figure placeholder.

MARKER CONVENTION:
  Underlined text is wrapped in {{u}}...{{/u}} markers during extraction.
  These markers are processed by render_text_with_math() and converted
  to Word underline formatting (run.underline = True) in the output.

  Example source: "He walked leisurely towards the entrance."
                              ──────────  (underlined in source)
  Extracted text:  "He walked {{u}}leisurely{{/u}} towards the entrance."
  Output docx:     "He walked leisurely towards the entrance."
                              ───────── (Word underline run)

DETECTION:
  FORMAT D (docx): Check run.underline for each run in the source.
  FORMAT A/B (PDF): Use pdfplumber char-level properties (char['underline'])
    or detect underline annotations. If text extraction tool cannot detect
    underlines, flag during Phase A and use visual inspection.

SCOPE:
  Underline is the ONLY inline formatting preserved by Step 1. Other
  inline styles (italic, color, strikethrough) are stripped — they are
  decorative in exam papers, not semantically significant.
  Exception: bold is always applied to the entire stem (not per-word).
  v1.14: this applies INSIDE TABLE CELLS as well. Cell text renders through
  render_text_with_math(), so {{u}} markers in a cell become a Word underline
  run exactly as they do in a stem (S1-8, S1-8a).

CROSS-STEP:
  PYQSort (Step 3) must preserve underline runs during re-sorting.
  MockTestCreate (Step 7) must carry underlines from PYQ stems into
  mock test questions.
```

### S1-12 — Image Inspection Protocol (v1.6 — mandatory)

```
PURPOSE:
  Source files frequently render math, tables, and text content as
  embedded images (especially docx files from coaching platforms,
  response sheet exports, and scanned-then-OCR'd papers). The Python
  pipeline cannot read image content — but Claude CAN. This protocol
  ensures every embedded image is classified and, when it contains
  non-visual content, transcribed into text + OMML.

WHEN THIS PROTOCOL APPLIES:
  Whenever Phase A inspection reveals embedded images in the source
  (drawings, blips, inline shapes in docx; embedded images in PDF;
  JPEG files in ZIP-of-images format). If the source has ZERO embedded
  images, this protocol is skipped entirely.

═══════════════════════════════════════════════════════════════════════
PHASE A-PROBE — VISION LIVENESS GATE (v1.9, MANDATORY, RUNS FIRST)
═══════════════════════════════════════════════════════════════════════
WHY. Every decision in this protocol is made BY VISION. S1-6 states the rule
plainly — red placeholders for math are BANNED, and the only legitimate
placeholder for a math question is an image that is physically unreadable
AFTER Claude has viewed it. But if the session's vision path has stopped
working, EVERY image is "physically unreadable", every one falls through to a
red placeholder, and nothing in the protocol can tell the two cases apart.

That is not a theoretical risk. It is the precise defect v1.6 was written to
eliminate, and the v1.6 changelog records the damage: SSC CGL T2 18-Jan-2025
Shift 1 — Q.6, Q.14, Q.15, Q.17, Q.19-Q.22, Q.28-Q.30, eleven math questions,
about 35% of the Quant section, delivered as red placeholders instead of
transcribed math. Under the current workflow it compounds: the graphics team
receives placeholders for equations and tables, draws pictures of them, and
those questions are FIGURAL rather than TEXT for the rest of the pipeline.

Vision can degrade MID-SESSION as context grows. Demonstrated: a freshly
generated control PNG failed to render in a session where real figures had
rendered correctly earlier. The files were never the problem.

HOW (v1.11 — THREE-PHASE, GAP-2026-07-26-003):

  run_img6_probe(read_probe) IS GONE. It took a CALLBACK that was supposed to
  perform a view(). A callback cannot make a tool call from inside a running python
  process — a tool call happens only BETWEEN model turns — so the parameter
  defaulted to a function returning '', score_vision_probe raised
  ProbeObservationMissing on all three attempts, and the probe reported EVERY
  session blind. Step 1 INHERITED that defect from Step 5 by importing it.

  Step 1 now uses the SAME three-phase bridge as Framework_MockTestAnalyse S4-2,
  against the images this step has already extracted. There is no separate probe:
  the images ARE the probe. If any of them comes back observed, vision works.

    PHASE A (python)  corpus_io.build_vision_queue(items, VISION_WORKDIR, fresh=True)
                      — items are the extracted images, keyed (source_id, img_idx).

                      VISION_WORKDIR = '/home/claude/pyq_vision_prep'   (v1.13)

                      DEFINED HERE, and DISTINCT from Step 5's /home/claude/pyq_vision.
                      Before v1.13 this spec used the name without defining it, so
                      every session inherited Step 5's directory — invisible under
                      corpus_io <= v1.8, whose builder overwrote the workdir, but the
                      v1.9 union made the queue ACCUMULATE across runs and steps:
                      a second PYQPrepare run saw the first paper's cells re-queued
                      (measured: queued=3 for a 1-image paper), Phase B re-viewed
                      them, Phase C counted them unobserved, and the footer went
                      amber with wrong counts. fresh=True (corpus_io >= v1.10)
                      restores per-run semantics EXPLICITLY: Step 1 completes
                      Phase A->B->C inside one trigger, so a prior queue is never
                      resume state here — it is contamination. Step 5 keeps the
                      union; its workdir spans a batch and resumed sessions must
                      not orphan prior sheets.
    PHASE B (model)   view() each contact sheet; record one observation per
                      labelled cell. THIS IS PROSE, NEVER A PYTHON FUNCTION.
                      Protocol verbatim as Framework_MockTestAnalyse S4-2b, except
                      that what is recorded is the CLASSIFICATION this protocol
                      needs (math / table / text / figure) plus figure_readable.
    PHASE C (python)  bc.merge_vision_observations(queue['items'], observations)
                      — the only writer of image_clarity.

ON `observed` — proceed to Phase A-IMAGE. Behaviour is exactly as v1.6 specified.
          Nothing below changes when vision is working.

ON `unavailable` or `partial` — v1.11 REPLACES THE HALT.

  The halt was protecting the right thing for the wrong reason. What must never
  happen is a red placeholder assigned to an image nobody looked at: that is
  permanent, it converts a math question into a FIGURAL one for the rest of the
  pipeline, and no later step can undo it. What does NOT need to happen is
  stopping the run — an image LEFT IN PLACE is safe, reversible and costs nothing.

  So Step 1 COMPLETES and DELIVERS, under these rules:

  1. Do NOT classify any unobserved image.
  2. Do NOT assign a red placeholder to ANY unobserved image. Assigning one under
     an unobserved cell is a HARD BUG, ranking with the "unclassified image" hard
     bug below. This rule is UNCHANGED and is the whole point.
  3. LEAVE the unobserved image exactly as it is, in place, untouched. An image
     that is still an image can be transcribed later; a placeholder cannot be
     un-baked. This is what makes completing the run safe.
  4. Record image_clarity='vision_unavailable' for those images via
     bc.merge_vision_observations() (Phase C is the only writer).
  5. DELIVER the Row file, and state plainly in the delivery footer which images
     are pending. The footer renders F1 AMBER, never F2 green, because a FAIL or
     an unobserved-image count is present (Framework_DeliveryFooter §5).
  6. Tell the user in plain terms:
       "N image(s) could not be read in this session. NO placeholders were
        assigned and those images are preserved untouched in the Row file.
        The contact sheets are already on disk at <VISION_WORKDIR>.
        To complete them, re-run PHASE B ONLY in a fresh chat — Phases A and C
        need not repeat, and re-running Phase B is idempotent."

  NOTHING HALTS, AND THE ARTEFACT IS STILL PROTECTED. The two goals were never in
  conflict; the old design conflated "do not corrupt the Row file" with "do not
  finish the run".

COST: ceil(N_images / 6) view() calls per session instead of N_images + 1. The
liveness check itself is free — it is derived from whether observations came back.

THREE-STATE OUTCOME (bc.merge_vision_observations / bc.image_clarity_state) — the
two-state form conflated two failures with different causes and opposite remedies:
  clear              the image was read and classified.
  unclear            the FIGURE is genuinely illegible — corrupt, blank, too low
                     resolution. Requires that the cell WAS observed. This is the
                     only state that may lead to a placeholder for math-like
                     content, and it is reported in delivery.
  vision_unavailable the cell was NOT observed. Never a statement about the image.
                     Never a placeholder. The image is left untouched and the run
                     completes; QV-style reporting and an amber footer carry it.

The distinction is load-bearing here in a way it is not in Step 5: 'unclear' MAY
become a placeholder, and 'vision_unavailable' MUST NOT. Collapsing them is how
eleven SSC CGL math questions became red placeholders.

RESUMING: re-run PHASE B whenever classification resumes after a context break.
An observation is evidence about the session at the moment it was made, not a
permanent fact — and because merges are keyed by tag, a second Phase B pass fills
only the gaps and cannot corrupt work already done (idempotent, EC-V4/EC-V12).

NO GOVERNOR IN STEP 1 (v1.9, stated so the omission reads as a decision).
Steps 3, 4 and 5 govern document size against the Drive transport cap. Step 1
does not, and must not: the only images it EMITS are 300x200 red placeholder
PNGs. There is nothing to compress. Size governance begins at Step 3
(PYQSort S7-6), the first step to hold real image bytes.
═══════════════════════════════════════════════════════════════════════

PHASE A — IMAGE EXTRACTION (part of Phase A inspection):

  Step 1: Extract all embedded images from the source to numbered files.

  FORMAT D (docx):
    DELEGATED to corpus_io (Cluster I) — v1.9. Do NOT re-implement.
```

```python
import corpus_io      # routed to PYQPrepare in routes.json

def extract_source_images(docx_path, output_dir):
    """Extract every embedded image and map each one to its question.

    v1.9 — REPLACES a local extract_images() that walked doc.paragraphs and
    matched only <a:blip>. That implementation had two silent failures, both of
    which removed an image from the protocol entirely — it was never extracted,
    never viewed, never classified, and did not even reach the "unclassified
    image" HARD BUG below, because the walk never saw it:

      * TABLE IMAGES. In python-docx, doc.paragraphs returns ONLY paragraphs
        that are direct children of the body; paragraphs inside table cells are
        excluded. Measured on a two-image document with one figure in a table:
        2 images present, 1 found. Table layout is the NORMAL arrangement for
        match-the-following items, multi-panel figures and option grids — and a
        math table rendered as an image inside a table is exactly the content
        this protocol exists to rescue.
      * VML IMAGES. Only <a:blip> was resolved. Legacy <v:imagedata r:id>,
        emitted by older Word, several PDF converters and pasted OLE/equation
        objects, was never mapped to its part.

    corpus_io.map_images_to_questions walks doc.element.body.iter(), which
    descends into tables, and matches BOTH mechanisms. corpus_io.extract_images
    writes every media part as ORIGINAL BYTES and labels vector parts (EMF/WMF)
    which must be rasterised before view().

    Returns (extracted, mapping):
      extracted {basename: {path, bytes, kind, format, size, mode, note}}
      mapping   {q_num or 'preamble': [media part names in document order]}
    """
    extracted = corpus_io.extract_images(docx_path, output_dir)
    mapping   = corpus_io.map_images_to_questions(docx_path)
    return extracted, mapping
```

```
    ACCOUNTING (v1.9): corpus_io.count_image_refs(docx_path) gives the number of
    image references the package actually contains. Every one of them must end
    up either in the mapping or in the 'preamble' bucket. A shortfall means an
    image exists that this protocol will never classify — investigate before
    building, because the pipeline's fall-through would silently placeholder it.

    Vector parts (kind == 'vector') cannot be viewed directly. PHASE A handles this:
    corpus_io.build_vision_queue() normalises every source internally (CMYK -> RGB,
    bounded, PNG) before tiling, and a part it cannot rasterise is queued and labelled
    [UNRENDERABLE] rather than dropped (EC-V8). Never view a raw source directly, or a
    vector/CMYK part reads as unreadable and is misclassified as VISUAL.
```

```
  FORMAT A (text PDF):
    Extract via PyMuPDF (fitz):
      import fitz
      doc = fitz.open(pdf_path)
      for page in doc:
          for img_info in page.get_images():
              xref = img_info[0]
              pix = fitz.Pixmap(doc, xref)
              pix.save(f"{output_dir}/img_{xref}.png")

  FORMAT B (ZIP-of-images):
    Images are already separate JPEG files in the extracted ZIP.
    Use them directly.

  Step 2: Build a paragraph-to-image mapping.
    For each image, record which question (paragraph index or Q-number)
    it belongs to. Use surrounding text context:
      - Look backwards from the image paragraph for the nearest Q.N
      - Look forwards for options or the next Q.N
    This mapping tells the pipeline which question each image belongs to.

PHASE A-IMAGE — CLAUDE VISUAL INSPECTION:

  Step 3: Claude views each extracted image using the view tool and
  classifies it into exactly one of four categories:

  CATEGORY 1 — MATH-IMAGE:
    Content: Mathematical expressions, equations, formulas, algebraic
    expressions, trigonometric expressions, coordinate geometry figures
    with equations, number series patterns expressed symbolically.
    Action: Claude transcribes the math as text. OMML helpers convert
    fractions/roots/superscripts during Phase B pipeline build.
    Examples:
      - "If x²+1/x² = 7, find x³+1/x³"
      - "³√6859 × ⁴√1296"
      - "sin²θ + cos²θ = 1, find tanθ"
      - A stem with a complex fraction expression
      - Options showing "1. 7/12  2. 5/12  3. 11/12  4. 1/12"

  CATEGORY 2 — TABLE-IMAGE:
    Content: Tabular data — frequency tables, DI data tables, statistics
    tables, comparison tables rendered as images.
    Action: Claude transcribes the table into a TableSpec (S1-8a) —
    ANCHOR CELLS ONLY, WITH cs/rs SPANS. Pipeline builds a native Word
    table using build_di_table() (S4-3 → corpus_io Cluster I).
      v1.14: this said "transcribes the table data as a list of rows". A list
      of rows has no vocabulary for a span, so the geometry of a grouped header
      was destroyed AT THE MOMENT OF OBSERVATION, before any builder was
      reached, and the only way to keep the grid rectangular was to pad with
      empty strings. TRANSCRIBE THE SPANS: if the source shows one cell
      covering four columns, that is ONE Cell with 'cs': 4, not four cells.
    Examples:
      - Class interval frequency table
      - Year-wise revenue/production data
      - Student marks distribution table

  CATEGORY 3 — TEXT-IMAGE:
    Content: Plain text rendered as an image (no math, no table, no
    visual). Sometimes coaching platforms render entire question stems
    as images for copy-protection.
    Action: Claude transcribes the text verbatim. Pipeline writes it
    as a normal text stem/option.
    Examples:
      - Full question stem rendered as image
      - Instructions rendered as image
      - Option text rendered as image

  CATEGORY 4 — VISUAL-IMAGE:
    Content: Genuine visual content that CANNOT be transcribed as text.
    Geometric figures, dice faces, Venn diagrams, mirror images, bar
    charts, pie charts, line graphs, pattern grids, map-based content,
    photographs, embedded diagrams.
    Action: Red placeholder (existing S1-7 behavior). This is the ONLY
    category that gets a red placeholder.
    Examples:
      - Geometry figure showing triangle with angle marks
      - Dice showing letter positions
      - Pattern completion figures (4 option figures)
      - Mirror image question figures
      - Bar chart / pie chart (note: underlying DATA tables are
        TABLE-IMAGE; the visual chart itself is VISUAL-IMAGE)

  HYBRID CASE — Image contains BOTH visual and text/math:
    Example: A geometry figure with labeled sides "AB = 5cm, BC = 12cm"
    Classification: VISUAL-IMAGE (the visual is the primary content).
    BUT: if the stem text already mentions these labels, nothing is lost.
    If the image contains math expressions that are NOT in the stem text,
    Claude transcribes the math portion and notes it in the classification.
    Pipeline adds the transcribed math to the stem text, followed by the
    red placeholder for the visual portion.

  UNREADABLE IMAGE:
    If an image is corrupt, blank, too small to read, or too low
    resolution for Claude to determine content → classify as VISUAL-IMAGE
    (red placeholder) + add WARN to delivery message. This is the ONLY
    case where math MIGHT get a placeholder — and it's flagged explicitly.

    v1.11 GATE — this verdict REQUIRES THAT THIS IMAGE'S CELL WAS OBSERVED.
    "Unreadable" is a claim about the IMAGE. With vision unavailable every
    image looks unreadable, so recording this verdict for an unobserved cell
    states something the session is in no position to know — and it is the
    exact path by which eleven math questions were destroyed in the incident
    recorded in the v1.6 changelog. For an unobserved cell the verdict is
    vision_unavailable, the image is LEFT UNTOUCHED, and the run COMPLETES.
    Sequence, non-negotiable:
      observed   → viewed → genuinely unreadable → VISUAL + WARN  (permitted)
      unobserved → no view verdict at all        → leave in place (mandatory)
                                                   report + F1 amber; NO halt
    Vector parts (EMF/WMF) are NOT unreadable — PHASE A rasterises what it can and
    marks the rest [UNRENDERABLE] on the sheet (EC-V8); judge the sheet cell, never
    the raw source file.

  Step 4: Record all classifications in a structured dict.
```

```python
# IMAGE_CLASSIFICATIONS dict — baked into pipeline.py during Phase B.
# Keys: paragraph index (or Q-number) from the source.
# Values: (category, transcription_or_None)
#
# The pipeline uses this dict when processing image-only paragraphs
# to decide whether to transcribe or placeholder.

IMAGE_CLASSIFICATIONS = {
    # Q.6 stem — math expression rendered as image
    37: ("MATH", "If the ratio of the cost price to selling price is 5:7, "
         "and the discount offered is 20%, then the ratio of cost price "
         "to the marked price is:"),
    # Q.14 — table image, FLAT header (a bare list of lists is a valid grid)
    86: ("TABLE", [
        ["Class Interval", "0-10", "10-20", "20-30", "30-40", "40-50"],
        ["Frequency", "5", "8", "15", "12", "10"],
    ]),
    # Q.15 — table image, TWO-TIER header (v1.14). The worked example above is
    # flat, and a flat example is why a model that could not express a span was
    # never exercised against one. This is the shape that broke: 'Days' covers
    # two rows, 'Printers' covers four columns, and row 1 declares FOUR cells
    # because its first position is already covered.
    91: ("TABLE", {
        'grid': [
            [{'t': 'Days', 'rs': 2}, {'t': 'Printers', 'cs': 4}],
            [{'t': 'L'}, {'t': 'M'}, {'t': 'N'}, {'t': 'O'}],
            ['Friday', '10,230', '9580', '7560', '9600'],
        ],
        'header_rows': 2,
        'col_widths': [2.0, 1.0, 1.0, 1.0, 1.0],
    }),
    # Q.33 — geometric figure (genuine visual)
    209: ("VISUAL", None),
    # Q.36 — mirror image figure
    227: ("VISUAL", None),
    # Q.37 — pattern figure
    231: ("VISUAL", None),
}
```

```
PIPELINE USAGE:
  In Phase B, the pipeline checks IMAGE_CLASSIFICATIONS when it
  encounters a paragraph with an embedded image but no extractable text:

  if para_idx in IMAGE_CLASSIFICATIONS:
      cat, content = IMAGE_CLASSIFICATIONS[para_idx]
      if cat == "MATH" or cat == "TEXT":
          # Write transcribed text as stem (with OMML rendering)
          add_stem(doc, q_num, content)
      elif cat == "TABLE":
          # Write as native Word table. `content` is a TableSpec (S1-8a) — or a
          # bare list of lists for a flat table, which normalise_table_spec()
          # accepts unchanged.
          add_stem(doc, q_num, "")  # Q.N header
          build_di_table(doc, content)
      elif cat == "VISUAL":
          # Red placeholder (existing behavior)
          add_stem_figure_only(doc, q_num)
          add_placeholder_stem(doc, RED_PNG)
  else:
      # UNCLASSIFIED IMAGE — this is a HARD BUG.
      # Every image MUST be classified. If we reach here, Phase A-IMAGE
      # was incomplete. Treat as VISUAL + WARN.
      #
      # v1.9 — TWO WAYS TO REACH HERE, and they need different responses:
      #   (a) the image was extracted but not classified — the original hard
      #       bug; the fall-through below applies.
      #   (b) the image was never extracted at all, because it sat inside a
      #       table cell and the old doc.paragraphs walk could not see it
      #       (DEFECT I). Delegating discovery to corpus_io closes that route;
      #       cross-check the mapping against corpus_io.count_image_refs so a
      #       shortfall is caught BEFORE the build rather than becoming a
      #       silent placeholder here.
      # v1.11: if THIS image's cell was not observed, do NOT reach this branch.
      # An unobserved image is left exactly as it is — never placeholdered —
      # and the run completes with the gap reported (S1-12).
      add_stem_figure_only(doc, q_num)
      add_placeholder_stem(doc, RED_PNG)
      warnings.append(f"UNCLASSIFIED IMAGE at para {para_idx} — "
                       f"image inspection incomplete")

OPTION IMAGES:
  The same protocol applies to option images. If options are rendered
  as images:
    - Extract and view each option image
    - If MATH/TEXT: transcribe and write as text options
    - If VISUAL: red placeholder option table (existing S1-7 behavior)
    - Mixed (some text, some visual): transcribe text options, placeholder
      visual options — but maintain ALL-or-NONE placeholder rule for
      visual option sets (if ANY option is visual, ALL get placeholders)

  For options, the IMAGE_CLASSIFICATIONS key format is:
    (para_idx, "opt", opt_num) — e.g. (37, "opt", 1) for Q.6 option 1

TOOL CALL BUDGET:
  Image inspection adds view calls to Phase A. Each image requires one
  view call. For a source with N images:
    - 0 images:  Phase A unchanged (1–3 calls), total 4–7
    - 1–5 images: +1–2 view calls (batch review), total 5–9
    - 6–15 images: +3–5 view calls, total 7–12
    - 16+ images: +5–8 view calls (batch where possible), total 9–15
  The view tool shows one image per call. To minimize calls, Claude can
  extract all images first, then view them in sequence, recording
  classifications as it goes.

CLASSIFICATION ACCURACY:
  Claude's classification determines whether math content is preserved
  or destroyed. OVER-CLASSIFY as MATH when in doubt:
    - If unsure whether an image is math or text → classify as MATH
    - If unsure whether a chart shows data or is decorative → VISUAL
    - If an image has ANY mathematical notation → MATH (not VISUAL)
    - If a table image is partially readable → TABLE (transcribe what's
      readable, note gaps)
  The cost of over-classifying as MATH (extra transcription work) is
  trivially small. The cost of under-classifying (math question gets
  red placeholder, entire question is DESTROYED for downstream use)
  is catastrophic.
```

### S1-13 — Scanned-Source Vision Transcription (v1.7 — FORMAT C1)

```
PURPOSE:
  Reconcile the FORMAT C halt with the S1-6/S1-12 principle that Claude's
  vision is a first-class transcription mechanism. A scanned page is just a
  very large TEXT/MATH/TABLE/VISUAL image; S1-12 already transcribes those
  when embedded. S1-13 extends the same capability to WHOLE PAGES, behind a
  MECHANICAL tier decision and a mandatory provenance marker — so the halt is
  relaxed for LEGIBLE scans without re-introducing silent OCR-error risk.

WHEN THIS PROTOCOL APPLIES:
  Whenever classify_source_pdf() (below) returns C1, C-HYBRID, or C0_OR_C1.
  C0_OR_C1 (a zero-text scan — the COMMON case, e.g. a bare scanned paper) is
  NOT a halt: it ENTERS this protocol at steps 1-2 (rasterise + legibility
  gate), which RESOLVE it to C1 (legible -> proceed) or C0 (illegible ->
  HALT). The legibility gate (step 2) is the ONLY producer of C0. FORMAT A
  (clean text) and FORMAT B/D/E paths are untouched.

DECISION IS COMPUTED, NEVER INTERPRETED:
  The A / C1 / C-HYBRID / C0_OR_C1 routing is returned by a runnable
  function, so the same source yields the same result on every run and in
  every project. For a zero-text scan the function emits C0_OR_C1; the ONLY
  human-like judgment retained is then a single bounded legibility check
  (one rendered page: readable? yes -> C1, no -> C0), whose default on doubt
  is the SAFE one (C0 -> HALT).
```

```python
def _text_is_sane(t):
    """Conservative poisoned-OCR-layer detector. Returns False only when the
    extracted text is mostly garbage (mojibake / replacement / C0 controls).
    Tuned high so clean FORMAT A papers are NEVER misrouted to vision."""
    if not t:
        return True
    bad = sum(1 for c in t
              if c == '\ufffd' or (ord(c) < 32 and c not in '\t\n\r'))
    return (bad / max(len(t), 1)) < 0.30   # <30% garbage -> treat as sane text


def classify_source_pdf(pdf_path, k_chars=20):
    """Deterministic FORMAT tier for a PDF source. Returns one of:
      'A'         clean text layer (existing FORMAT A path)
      'C1'        image-only OR poisoned-text scan -> S1-13 vision path
      'C-HYBRID'  some text pages + some image pages -> per-page routing
      'C0_OR_C1'  zero text everywhere -> legibility gate decides C0 vs C1
    Never returns a bare 'HALT'; C0 is resolved by the legibility gate so the
    decision that used to be interpretive prose is now executed code."""
    import fitz  # PyMuPDF
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        return 'C0_OR_C1'          # unreadable container -> legibility gate -> C0
    if getattr(doc, 'needs_pass', False) or getattr(doc, 'is_encrypted', False):
        return 'C0_OR_C1'          # encrypted -> cannot extract/rasterise -> C0
    n = doc.page_count or 1
    text_pages = 0
    sane_pages = 0
    for pg in doc:
        try:
            t = pg.get_text().strip()
        except Exception:
            t = ''                 # a single unreadable page counts as image page
        if len(t) >= k_chars:
            text_pages += 1
            if _text_is_sane(t):
                sane_pages += 1
    coverage = text_pages / n
    if coverage == 0:
        return 'C0_OR_C1'
    if coverage == 1 and sane_pages == text_pages:
        return 'A'
    if coverage == 1 and sane_pages < text_pages:
        return 'C1'                 # poisoned layer -> prefer vision over garbage
    return 'C-HYBRID'               # 0 < coverage < 1
```

```
MANDATORY ORDERED STEPS (C1 / C-HYBRID image pages):

  1. RASTERISE each image page to a viewable PNG at >=150 dpi
     (PyMuPDF page.get_pixmap(dpi=150).save(...)). This is the step that did
     not exist before v1.7 — without it the JBIG2/CCITT stream is not
     viewable in-context. If rasterisation raises (exotic codec, corrupt,
     encrypted) -> C0 -> HALT with that specific reason.

  2. LEGIBILITY GATE. View one representative rasterised page. If it is
     unreadable (too low resolution, heavy noise, illegible) -> downgrade the
     whole source to C0 -> HALT. Default on doubt: HALT. Otherwise proceed.

  3. PAGE CLASSIFICATION (extends EC-P2 to page granularity). Label every
     page and SKIP all but question pages:
       COVER / INSTRUCTION  -> skip (EC-P2)
       ROUGH-WORK / BLANK   -> skip (EC-P2)
       SAMPLE / SPECIMEN    -> skip (EC-P21 — the "Q.201" trap)
       ANSWER-KEY           -> skip (EC-P17 — NEVER transcribe answers)
       QUESTION-CONTENT     -> transcribe (step 4)
     Bilingual policy: reuse EC-P13 — transcribe the ENGLISH question text,
     drop pure other-language instruction/cover chrome. (Configurable per
     exam, but English-only is the default, identical to EC-P13.)

  4. REGION-LEVEL CONTENT CLASSIFICATION (extends S1-12's four categories to
     sub-page regions, because one scanned page may hold several questions of
     mixed type):
       TEXT   -> transcribe verbatim (S1-11: underline preserved via {{u}};
                 italic dropped as decorative)
       MATH   -> transcribe as ⟦MATH:…⟧ LaTeX-lite regions (S1-6 Tier 3,
                 S3-5b compiler). v2.0 MANDATORY RULES:
                 (a) WRAP THE WHOLE EXPRESSION, not fragments — one region
                     per displayed expression/equation, so the entire
                     expression renders as one math object in one font.
                     Trivial single tokens (ℝ, ∈, π, x², aₙ, S₃) may stay
                     as bare Unicode in prose.
                 (b) NEVER PARAPHRASE STRUCTURE INTO PROSE. A bracketed
                     matrix is transcribed as \bmatrix/\pmatrix, a column
                     vector as \pmatrix{a\\ b\\ c}, a piecewise
                     definition as \cases — never as "the matrix whose
                     rows are (…)", never as (…)ᵀ tuples. Rewording is a
                     transcription DEFECT even when mathematically
                     equivalent (measured: Q.37/Q.56, JAM MA 2026).
                 (c) DECLARE structures: build STRUCT_FLAGS =
                     {q_num: {'matrix'} | {'cases'} | both} for every
                     question whose source shows a matrix/vector or a
                     cases brace, and pass it to the validator (CHECK 21).
                 (d) Regions are single-line; multi-line stems keep \n in
                     the PLAIN text between regions.
                 (e) Inside regions, √N literal is auto-converted; any
                     other literal √ is rejected by the compiler (the
                     region then degrades per S3-5) — use \sqrt{…}.
                 (f) {{u}} underline spans must not cross a region
                     boundary — underline plain text only, or none.
       TABLE  -> transcribe into a TableSpec, SPANS INCLUDED (S1-8a)
                 -> native Word table (S1-8). A scanned two-tier header is
                 a two-tier header; page rasterisation changes the
                 acquisition path, never the structure contract.
       VISUAL -> red placeholder for THAT region only (S1-7)

  5. CROSS-PAGE CONCATENATION (extends EC-P1). Build ONE continuous question
     buffer across page images BEFORE numbering. Never number page-by-page.

  6. BUILD VIA THE STANDARD TEXT PATH. The transcription becomes the content
     source (exactly like a FORMAT E raw-text source). It feeds the SAME
     add_stem / add_option / render_text_with_math / build_di_table builders.
     S1-13 does NOT use the paragraph-keyed IMAGE_CLASSIFICATIONS dict (there
     are no source paragraphs in a bare scan) — that dict remains S1-12-only.

  7. EMIT the standard Row file (§1 output contract UNCHANGED) PLUS the
     provenance marker (below). Continuous Q.1..Q.N, canonical options, one
     date label per question — all identical to any other Row file.

C-HYBRID PER-PAGE ROUTING (v1.7):
  For a C-HYBRID source, route EACH page independently: a page whose extracted
  text PASSES _text_is_sane() uses normal text extraction; a page with NO text
  OR whose text FAILS _text_is_sane() (poisoned OCR) is treated as an image
  page and vision-transcribed via steps 1-6. This prevents a garbage OCR page
  from being extracted verbatim. All pages merge into the single continuous
  buffer (step 5) before numbering.

PROVENANCE MARKER (mandatory, set at BUILD time — the key new control):
  Every C1 / C-HYBRID Row file MUST carry a machine-readable trust flag so a
  vision-transcribed file is distinguishable from a deterministically
  extracted one. Set BOTH, in the C1 build path, before delivery:
```

```python
def mark_vision_transcribed(doc, mixed=False):
    """Set the mandatory VISION provenance marker on a C1/C-HYBRID Row file.
    Called unconditionally by the S1-13 build path -> the marker cannot be
    forgotten. CHECK 14 is only a post-build safety net."""
    trust = 'MIXED' if mixed else 'VISION-TRANSCRIBED'
    doc.core_properties.category = 'PYQPrepare-Source-Trust:' + trust
    return trust
```

```
  Plus a filename suffix: insert "__vision-unverified" before ".docx"
  (see §6). Human reviewers see the suffix; downstream steps may read the
  core-property (see §10). No in-document banner paragraph is added, so no
  downstream text parser can trip over an unexpected leading paragraph.

DELIVERY (see §7): C1/C-HYBRID uses the F2 step-complete footer PLUS a
  prominent "VISION-TRANSCRIBED — human verification required" note listing
  any low-confidence Q-numbers. The Row file is still delivered (the S5
  contract is warn-and-deliver).

BUDGET / BATCH MODEL:
  FORMAT C1 tool-call budget is PAGE-COUNT-DEPENDENT: roughly one view call
  per QUESTION-CONTENT page + ~7 overhead calls (inspect + rasterise + build
  + validate + deliver). For papers with <= ~40 question-content pages, run
  in one session (a typical 150-question paper is ~20-25 question pages). For
  larger scans, transcribe in batches, delivering an interim file per batch
  under the EXISTING DeliveryFooter F1 amber "continue" variant (and the F1
  session-break variant on a forced context-limit break). No DeliveryFooter
  change is required — those variants already exist.

  OUT OF SCOPE (v1.7 — documented limitation):
    A ZIP-of-images source with no per-page .txt (a "FORMAT C inside a ZIP")
    is NOT handled here — S1-13 is PDF-scan-only. Such a source stays on the
    FORMAT B path and is a known limitation to be addressed separately.

DECISION POLICY (the one governance dial):
  DEFAULT = AUTO-PROCEED for a legible, pure-text C1 scan within budget (the
  common Indian-exam paper): transcribe, mark, deliver with the verification
  note — reproducing a clean first-trigger success while keeping the marker
  as the safety floor. Confirm-first is used only for the harder cases
  (figures present, or page count over the batch threshold). C0 always halts.
  This default is what makes the GitHub (strict-skill) path succeed
  deterministically instead of halting.
```

---

## §2 — SOURCE PARSING LAYER (adaptive — varies by source format)

Step 1 uses a two-layer architecture:
  Layer 1: Output Contract (§1) — immutable, identical for every exam
  Layer 2: Source Parsing (§2) — adaptive, varies by source format

Claude inspects the source file during Phase A (exploratory calls) and
selects the appropriate parsing strategy. The output is always identical
regardless of which parsing path was used.

### S2-1 — Known source format families

```
FORMAT A — TEXT PDF
  Description: Standard PDF with extractable text layers.
  Detection  : file command shows "PDF document", text extraction yields content.
  Tools      : pdftotext, pdfplumber, PyMuPDF (fitz), or native PDF text extraction.
  Examples   : Official exam body releases, some coaching site PDFs.
  Underline  : pdftotext CANNOT detect underlines. Use pdfplumber with
               char-level properties (char['fontname'], text annotations)
               or PyMuPDF span flags to detect underlined text. If the
               extraction tool cannot detect underlines, flag during
               Phase A and try alternative tools. Wrap in {{u}}...{{/u}}.

FORMAT B — ZIP-OF-IMAGES (mislabelled PDF)
  Description: ZIP archive containing per-page JPEG + TXT + manifest.json.
               File extension may be .pdf but is actually a ZIP.
  Detection  : file command shows "Zip archive", or unzip succeeds.
  Tools      : unzip → read *.txt in page order → concatenate into buffer.
  Examples   : Adda247/Oliveboard response sheet PDFs.
  Special    : manifest.json has_visual_content flag is USELESS (always true).
               Decide figure presence from TEXT CONTENT only.

FORMAT C — SCANNED / IMAGE-ONLY PDF (three mechanical tiers — v1.7)
  Description: Pages are rasterised images; text extraction yields little or
               no text, OR the extracted text is garbage (poisoned OCR layer).
  Detection  : MECHANICAL — call classify_source_pdf() (S1-13). Do NOT decide
               by interpretation. The function returns a tier from measured
               text coverage + a sanity gate:
                 C0_OR_C1  — zero extractable text (the common bare scan) →
                             ENTERS S1-13; its legibility gate resolves it to
                             C1 (legible) or C0 (illegible)
                 C1        — legible / poisoned-text scan → vision-transcribe (S1-13)
                 C-HYBRID  — some text pages, some image pages → per-page route
                 C0        — produced ONLY by the S1-13 legibility gate → HALT
  Strategy   : C0 → HALT with a specific reason (rasterisation failed, encrypted,
               or the legibility gate judged the rendered page unreadable). This
               is the ONLY terminal FORMAT C state. Inform the user OCR/a
               text-layer PDF is needed.
               C1 / C-HYBRID / C0_OR_C1 → run the S1-13 Scanned-Source Vision
               Transcription protocol (C0_OR_C1 is resolved to C1 or C0 by the
               legibility gate). Output is a standard Row file (§1 contract
               unchanged) PLUS a mandatory VISION-TRANSCRIBED marker (S1-13).
  NOTE       : "image-only PDF" is NO LONGER an automatic halt. Claude's vision
               is a first-class transcription mechanism (S1-6/S1-12 principle);
               S1-13 extends it to full pages. HALT is reserved for illegible
               scans only.

FORMAT D — DOCX SOURCE
  Description: Question paper already in Word format.
  Detection  : file command shows "Microsoft Word" or "Office Open XML".
  Tools      : python-docx to read paragraphs, tables, images directly.
  Examples   : Coaching institute internal papers, self-made compilations.
  Underline  : MUST detect run.underline on each run during extraction
               and wrap underlined text in {{u}}...{{/u}} markers (S1-11).
               Example: for run in para.runs:
                 if run.underline: text += f'{{{{u}}}}{run.text}{{{{/u}}}}'
                 else: text += run.text
  Images     : MUST extract all embedded images (paragraphs with
               <w:drawing> elements) using extract_images() from S1-12.
               Docx sources from coaching platforms frequently render
               math content as images — these MUST be classified and
               transcribed per the Image Inspection Protocol (S1-12).

FORMAT E — RAW TEXT / HTML / COPY-PASTE
  Description: Plain text or HTML dump of questions.
  Detection  : file shows "ASCII text", "UTF-8 text", or "HTML document".
  Tools      : Direct string parsing. BeautifulSoup for HTML.
  Examples   : Questions copied from websites, text file compilations.

FORMAT F — UNKNOWN
  Description: Format not matching any known family.
  Strategy   : Claude applies best-effort extraction. If extraction quality
               is uncertain, warn user in delivery message.
```

### S2-2 — Source inspection (Phase A)

```
Claude performs 1–3 exploratory tool calls to understand the source:

CALL 1: Determine file type
  bash_tool: file /mnt/user-data/uploads/<filename>
  → Identifies PDF, ZIP, DOCX, text, HTML, etc.

CALL 2: Attempt text extraction (format-dependent)
  PDF:  bash_tool: pdftotext <file> - | head -200
  ZIP:  bash_tool: unzip -l <file> (list contents)
  DOCX: view or bash_tool: python3 -c "from docx import ..."
  TEXT: view the file directly

CALL 3 (if needed): Deeper inspection
  ZIP:  bash_tool: unzip <file> -d /home/claude/work/source && cat *.txt
  PDF:  Check for images, page count, section headers
  DOCX: Check paragraph structure, formatting

CALL A2b — TEXT-LAYER TABLE DETECTION (v1.14, FORMAT A / FORMAT C-HYBRID text
pages, and FORMAT D):
  S1-12 fires only on EMBEDDED IMAGES. A DI table drawn as vector rules plus a
  real text layer therefore never entered the table protocol at all: its cell
  text was consumed by the ordinary line parser and appended into the stem as
  running prose. S1-8 has always said "any structured tabular data in the
  source → NATIVE WORD TABLE" while no clause anywhere said how such data is
  DETECTED outside the image path.
    1. Run a table finder over every text page (e.g. pdfplumber
       page.find_tables(); python-docx doc.tables for FORMAT D).
    2. DISCARD page furniture: the exam-header block (CATEGORY 2 metadata) and
       the question-block separator rules, both of which present as low-row-count
       grids spanning the full text width. On the reference corpus this filter
       discards exactly one header table and three separator false positives, so
       it is exercised by real data.
    3. A surviving candidate overlapping a question's y-range IS a DI table:
       transcribe it into a TableSpec (S1-8a) and render per S1-8. Do NOT let
       its text reach the stem parser.
  The acquisition mechanism differs from S1-12; the structure contract does not.

CALL 3/4 — IMAGE EXTRACTION (v1.6 — mandatory when images detected):
  If CALL 2/3 reveals embedded images (drawings, blips, inline shapes):
    1. Extract ALL images to /home/claude/work/images/ using the
       extract_images() function from S1-12.
    2. Record paragraph-to-image mapping.
    3. Identify which images correspond to which questions by checking
       surrounding paragraph text context.

CALLS A-IMAGE — IMAGE CLASSIFICATION (v1.6 — mandatory):
  After image extraction, Claude views each extracted image using the
  view tool and classifies per S1-12 categories (MATH / TABLE / TEXT /
  VISUAL). Claude records the IMAGE_CLASSIFICATIONS dict for use in
  Phase B pipeline.py.
  For efficiency:
    - View images in question-number order
    - Record classification + transcription for each image immediately
    - If image is MATH/TEXT/TABLE: transcribe content fully
    - If image is VISUAL: note "VISUAL" and move on
  This sub-phase may require 1–8 view calls depending on image count.

After inspection, Claude identifies:
  - Total question count (approximate)
  - Section/module structure (if any)
  - Option format used in source
  - Presence of figures/images
  - IMAGE CLASSIFICATIONS for all embedded images (v1.6)
  - Metadata vocabulary to strip
  - Math content requiring OMML
  - Passage/comprehension blocks
  - Any edge cases specific to this source
```

### S2-3 — Metadata stripping (universal vocabulary)

```
Step 1 strips ALL of the following from the source. This list is
comprehensive but not exhaustive — Claude adds source-specific patterns
as discovered during inspection.

CATEGORY 1 — Answer/status metadata:
  Question ID : <digits>
  Option N ID : <digits>          (N = 1–5)
  Status : Answered
  Status : Not Answered
  Status : Marked For Review
  Chosen Option : <N>
  Chosen Option : --
  Correct Answer : <N>
  Answer: <text>
  Answer : (a) / (b) / (c) / (d)
  Solution: / Explanation: / Hint:

CATEGORY 2 — Exam header metadata:
  Roll Number / Candidate Name / Venue Name
  Exam Date / Exam Time / Subject line
  Exam title lines (e.g. "Combined Graduate Level Examination 2024 Tier II")
  Section headers (e.g. "Section : Module I Mathematical Abilities")

CATEGORY 3 — Sub-question metadata:
  SubQuestion No : <N>
  Comprehension: (label only — keep the passage text below it)

CATEGORY 4 — Third-party branding:
  Any line containing: Oliveboard, Adda247, Testbook, Unacademy,
  BYJU'S, Gradeup, Cracku, or other coaching brand names
  Any line containing: Mock Test, Test Series, Practice Set
  Any line containing: URLs (http, https, www., .com, .in, .org)
  Any line containing: social/app handles (Telegram, YouTube, WhatsApp,
  Google Play, App Store, Download the App)
  Watermark text, promotional footers, advertisement lines

CATEGORY 5 — Answer markers:
  ✓ ✔ (correct answer checkmarks) — STRIP
  ✗ ✘ (wrong answer crossmarks) — STRIP
  Green/red colouring on options — IGNORE (colour not preserved anyway)
  Bold/highlight on correct option — normalise to plain text

CATEGORY 6 — Source formatting noise:
  "Ans" / "Ans." before option 1 — STRIP (options rendered as clean 1./2./3./4.)
  Page headers / page footers repeated on every page
  Page numbers
  "Continued on next page" type markers

EDGE CASE — Run-on metadata:
  "Chosen Option : -- Q.4 Find the..." — metadata runs directly into next
  question with no newline. Strip at "Chosen Option : (--|\d+)" and treat
  the following Q.\d+ as a fresh question boundary.
```

### S2-4 — String sanitisation

```python
import re

def sanitise(s):
    """
    Remove OCR control-character corruption AND zero-width contamination.
    Delete C0 control bytes EXCEPT tab (\t) and newline (\n, \r), and delete the
    zero-width class U+200B ZWSP / U+200C ZWNJ / U+200D ZWJ / U+2060 WJ /
    U+FEFF BOM-ZWNBSP.
    Preserve ALL legitimate Unicode: curly quotes, em/en dashes, ₹, °, θ, π, etc.

    GAP-2026-08-15-BAREQ (R-8). Zero-width characters are NOT whitespace to Python:
    str.strip() does not remove them and regex \s does not match them. So a stem
    label written "Q.4<ZWSP>" is invisible to EVERY entry of Q_PATTERNS — the same
    silent question loss as the bare-label defect, by a second route, and invisible
    on screen because the operator sees "Q.4". PDF-to-DOCX converters emit these
    routinely. The class is deleted here at the PRODUCER; blueprint_core's
    detect_question_start() strips the same class at the CONSUMER so that Row files
    already delivered still parse without a Step 1 rebuild.
    """
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\u200b-\u200d\u2060\ufeff]', '', s)
```

```
Apply sanitise() to EVERY extracted string: stems, options, passages.
Do NOT normalise typographic Unicode — preserve curly quotes " " ' ',
em dashes —, en dashes –, rupee sign ₹, and all special symbols verbatim.
```

### S2-5 — Section merging and renumbering

```
Source papers often have per-section numbering:
  Math:      Q.1 – Q.30
  Reasoning: Q.1 – Q.30
  English:   Q.1 – Q.45
  GA:        Q.1 – Q.25

Step 1 MERGES all sections and RENUMBERS continuously:
  Q.1 – Q.30   (was Math Q.1–30)
  Q.31 – Q.60  (was Reasoning Q.1–30)
  Q.61 – Q.105 (was English Q.1–45)
  Q.106 – Q.130 (was GA Q.1–25)

Algorithm:
  1. Detect section boundaries (from section headers, or Q.1 resets)
  2. Collect all questions in source order
  3. Assign continuous Q.1 → Q.N
  4. Strip all section headers / module separators from output

Section headers in the source are treated as metadata (CATEGORY 2)
and stripped. No === separators === appear in the Row file.
```

### S2-6 — Passage detection and repetition

```
Passage-dependent questions share a common passage/context block.
Step 1 must detect these groups and repeat the passage for each
sub-question in the output, using Q.N-FIRST layout (S1-9 RULE 2).

Detection signals:
  - "Comprehension:" label followed by passage text
  - "Read the given passage and answer the questions that follow."
  - "In the following passage, some words have been deleted..."
  - "Directions (Q.N–Q.M): Read the following passage..."
  - "Study the following table/chart/graph and answer..."
  - Source repeats passage for each sub-question (1:1 mapping)
  - Source shows passage once followed by multiple sub-questions
    (1:many — replicate passage for each sub-question in output)

OUTPUT LAYOUT (Q.N-FIRST — mandatory for all passage questions):
  For each sub-question, emit in this order:
    1. Date label
    2. Q.N  <specific question text>     (bold)
    3. Instruction line                   (plain)
    4. Passage body paragraph(s)          (plain)
    5. Options
    6. Blank line

  Even if the source places the passage BEFORE the question number,
  the output REORDERS so Q.N always comes first. This is not optional.

The passage text is rendered as plain (NOT bold) Arial 11pt paragraph(s).
Strip the "Comprehension:" label but keep the instruction line and body.
```

---

## §3 — EXTRACTION PIPELINE

### S3-1 — Question detection

```python
# Q-number detection — ALIGNED WITH Step 5 E-2 and PYQSort S3-1
# These patterns detect question boundaries in the source.
# After detection, Step 1 RENUMBERS to continuous Q.1 → Q.N.

SOURCE_Q_PATTERNS = [
    r'^Q\.\s*(\d+)\s+',            # Q.1  Q.25  Q. 1
    r'^Q(\d+)\.\s+',               # Q1.  Q25.
    r'^Question\s+(\d+)\s*[:.]',   # Question 1:
    r'^(\d+)\.\s+(?!\d)',           # 1.   25.   (negative lookahead: not 1.5)
    r'^\((\d+)\)\s+',              # (1)  (25)
]

import blueprint_core as bc   # ENGINE (routed)
# SOURCE_Q_PATTERNS (renamed 2026-07-25) detects question boundaries in the RAW source,
# where "Question 1:", bare "1." and "(1)" are all genuine numbering and options are not yet
# canonical. It is Step 1's own table, deliberately WIDER than the engine's, and it is named
# SOURCE_* for the same reason SOURCE_OPT_PATTERNS is — to keep it out of the normalised-
# document contract that Steps 3, 4 and 5 share.
#
# The engine detector below is the NORMALISED-document one and implements only "Q.N" / "QN.".
# It must never be widened to match the table above: after Step 1 renumbers, options read
# "N. text", so the bare-number pattern would match every option line — a 100-question paper
# would parse as 500 questions (verified by execution).
# Step 1 VALIDATES its own normalised output with this detector — §5 CHECK 1, CHECK 2,
# CHECK 12, CHECK 15, CHECK 21 and CHECK 22 all call bc.detect_question_start(), never a
# local regex (GAP-2026-08-15-BAREQ, R-2). Until 2026-08-15 this binding existed but
# nothing used it: the checks carried a private r'^Q\.\d+' that matched strings the
# engine did not, so Step 1 certified "Q-count = 60, sequential OK" on a file Step 3
# read as 56 and delivered it green. A producer must count with the detector its
# consumers parse with. If a future check needs a Q-number, call this — never re-write it.
detect_question_start = bc.detect_question_start
```

### S3-2 — Option detection and normalisation

```python
# Source option patterns — detect ANY format the source uses.
# These are for DETECTION only. Output is ALWAYS canonical "N. text".

SOURCE_OPT_PATTERNS = [
    r'^([1-5])\.\s+(.+)',           # 1. 2. 3. 4. 5.
    r'^([A-Ea-e])\.\s+(.+)',        # A. B. C. D. E. / a. b. c. d. e.
    r'^\(([1-5])\)\s+(.+)',         # (1) (2) (3) (4) (5)
    r'^\(([A-Ea-e])\)\s+(.+)',      # (A) (B) (C) (D) (E) / (a)(b)(c)(d)(e)
    r'^([1-5])\)\s+(.+)',           # 1) 2) 3) 4) 5)
    r'^([A-Ea-e])\)\s+(.+)',        # A) B) C) D) E) / a) b) c) d) e)
]

# Letter-to-number mapping for normalisation
LETTER_TO_NUM = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5,
}

def parse_option(text):
    """
    Parse a source option line. Returns (option_number, option_text) or None.
    Option number is always an integer (1-5), regardless of source format.
    """
    for pat in SOURCE_OPT_PATTERNS:
        m = re.match(pat, text.strip())
        if m:
            label = m.group(1)
            opt_text = m.group(2).strip()
            if label.isdigit():
                return (int(label), opt_text)
            else:
                return (LETTER_TO_NUM.get(label, 0), opt_text)
    return None

def is_blank_option(text):
    """
    Detect blank/image-only option line (figure-option trigger).
    Matches: "1. " / "2." / "(a)" with nothing after the label.
    """
    blank_patterns = [
        r'^\s*[1-5]\.\s*$',
        r'^\s*[A-Ea-e]\.\s*$',
        r'^\s*\([1-5]\)\s*$',
        r'^\s*\([A-Ea-e]\)\s*$',
        r'^\s*[1-5]\)\s*$',
        r'^\s*[A-Ea-e]\)\s*$',
    ]
    return any(re.match(p, text.strip()) for p in blank_patterns)
```

### S3-3 — Figure detection

```
Figure presence is determined from TEXT CONTENT, never from metadata
flags (e.g. has_visual_content which may be unreliable).

PREREQUISITE (v1.6): Before classifying any image-bearing paragraph as
"figure-only," check IMAGE_CLASSIFICATIONS (S1-12). If the image was
classified as MATH-IMAGE, TABLE-IMAGE, or TEXT-IMAGE, it is NOT a
figure — it is transcribed content. Only VISUAL-IMAGE classifications
trigger figure handling (red placeholders).

Figure-only stem signals (AFTER image classification):
  - Q.N followed immediately by options/Ans with no stem text between
    AND the associated image is classified as VISUAL-IMAGE
  - Stem text is empty or whitespace-only after Q.N AND no image exists
    (truly empty — see EC-P15)

Image-only stem with MATH/TEXT/TABLE classification (v1.6):
  - Q.N has no extractable text BUT the image is classified as
    MATH-IMAGE, TEXT-IMAGE, or TABLE-IMAGE
  - This is NOT a figure-only stem — it is a TRANSCRIBED stem
  - Pipeline uses the transcription from IMAGE_CLASSIFICATIONS

Figure-option signals:
  - Any option line is blank after its label (is_blank_option() returns True)
    AND the option images are classified as VISUAL-IMAGE
  - When ANY option is blank AND visual, treat ALL options as figure-options
  - If option images are MATH/TEXT: transcribe them as text options

Stem-references-figure signals (stem has text but also needs a figure):
  - Stem text references visual content: "given figure", "shown below",
    "the diagram", "mirror image", "select the option figure",
    "study the pattern", "embedded figure"
  - These get: text stem + red placeholder after stem
  - Note: a stem may reference a figure AND contain math. The figure
    reference triggers a placeholder; the math in the text stem still
    gets OMML rendering.
```

### S3-4 — OMML rendering

```
OMML helpers and templates are inherited from the established pipeline.
Step 1 actively converts text-based math to OMML during extraction.

OMML SCAN (mandatory, during Phase A inspection):
  Identify questions/options requiring OMML:
    - Numeric fractions: \d+/\d+, 1/x, x/2
    - Mixed numbers: 2 4/5, 3(1/3), 12⅓
    - Trig powers: cos²θ, sin²x
    - Chemical subscripts: CO₂, H₂O
    - Unit superscripts: cm², cm³, m²
    - Roots: √15, √(x²−9), ³√8, ⁴√16
  DO NOT flag as OMML:
    - Rates: km/h, m/s, ₹X/kg
    - Logical: and/or
    - Dates: DD/MM/YYYY

POLYNOMIAL STEMS — use Unicode superscripts in the bold stem run (NOT OMML):
  x³ − 4x² − 8x + 11  →  "x\u00b3 \u2212 4x\u00b2 \u2212 8x + 11"
  Reason: OMML inside bold runs creates x□² rendering artifact.
```

```python
# OMML helper functions (v1.3 — compound-content-aware)

OMML_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"

def build_math_run(text):
    """Build an atomic OMML text run: <m:r><m:t>text</m:t></m:r>."""
    r = OxmlElement('m:r')
    t = OxmlElement('m:t')
    t.text = text
    r.append(t)
    return r

def build_compound_content(text):
    """
    Decompose a compound math string into a list of OMML elements.
    Handles text+sqrt combinations recursively.

    Examples:
      "3"    → [build_math_run("3")]
      "√3"   → [omml_sqrt("3")]
      "2√3"  → [build_math_run("2"), omml_sqrt("3")]
      "3√5"  → [build_math_run("3"), omml_sqrt("5")]
      "√3x"  → [omml_sqrt("3"), build_math_run("x")]

    Also cleans residual pipeline markers: ⟦SQRT:N⟧ → omml_sqrt(N).
    """
    import re
    # Normalise residual markers: ⟦SQRT:3⟧ or [SQRT:3] → √3
    text = re.sub(r'[⟦\[]SQRT:(\d+)[⟧\]]', lambda m: '√' + m.group(1), text)

    elements = []
    sqrt_pat = re.compile(r'√(\d+)')
    pos = 0
    while pos < len(text):
        m = sqrt_pat.search(text, pos)
        if m:
            before = text[pos:m.start()]
            if before:
                elements.append(build_math_run(before))
            elements.append(omml_sqrt(m.group(1)))
            pos = m.end()
        else:
            rest = text[pos:]
            if rest:
                elements.append(build_math_run(rest))
            break
    return elements if elements else [build_math_run(text)]

def omml_frac(num_text, den_text):
    """
    Build OMML fraction <m:f>. Numerator and denominator strings are
    processed through build_compound_content() — so "2√3" in either
    position decomposes into [text("2"), rad("3")] automatically.
    This handles: 1/2, 1/√3, √3/2, 1/(2√3), 3√5/7, etc.
    """
    f = OxmlElement('m:f')
    fPr = OxmlElement('m:fPr')
    f.append(fPr)
    num = OxmlElement('m:num')
    for el in build_compound_content(num_text):
        num.append(el)
    f.append(num)
    den = OxmlElement('m:den')
    for el in build_compound_content(den_text):
        den.append(el)
    f.append(den)
    return f

def omml_sup(base_text, sup_text):
    """Build OMML superscript element <m:sSup>."""
    ss = OxmlElement('m:sSup')
    e = OxmlElement('m:e')
    e_r = OxmlElement('m:r')
    e_t = OxmlElement('m:t')
    e_t.text = base_text
    e_r.append(e_t)
    e.append(e_r)
    ss.append(e)
    sup = OxmlElement('m:sup')
    sup_r = OxmlElement('m:r')
    sup_t = OxmlElement('m:t')
    sup_t.text = sup_text
    sup_r.append(sup_t)
    sup.append(sup_r)
    ss.append(sup)
    return ss

def omml_sub(base_text, sub_text):
    """Build OMML subscript element <m:sSub>."""
    ss = OxmlElement('m:sSub')
    e = OxmlElement('m:e')
    e_r = OxmlElement('m:r')
    e_t = OxmlElement('m:t')
    e_t.text = base_text
    e_r.append(e_t)
    e.append(e_r)
    ss.append(e)
    sub = OxmlElement('m:sub')
    sub_r = OxmlElement('m:r')
    sub_t = OxmlElement('m:t')
    sub_t.text = sub_text
    sub_r.append(sub_t)
    sub.append(sub_r)
    ss.append(sub)
    return ss

def omml_sqrt(content_text):
    """Build OMML square root element <m:rad> (degree hidden)."""
    rad = OxmlElement('m:rad')
    radPr = OxmlElement('m:radPr')
    degHide = OxmlElement('m:degHide')
    degHide.set(qn('m:val'), '1')
    radPr.append(degHide)
    rad.append(radPr)
    deg = OxmlElement('m:deg')
    rad.append(deg)
    e = OxmlElement('m:e')
    e_r = OxmlElement('m:r')
    e_t = OxmlElement('m:t')
    e_t.text = content_text
    e_r.append(e_t)
    e.append(e_r)
    rad.append(e)
    return rad

def omml_nthroot(degree_text, content_text):
    """Build OMML nth-root element <m:rad> with visible degree.
    degree_text: "3" for cube root, "4" for fourth root, etc.
    content_text: radicand, e.g. "8" for ³√8.
    For square root (degree hidden), use omml_sqrt() instead.
    """
    rad = OxmlElement('m:rad')
    radPr = OxmlElement('m:radPr')
    # degHide=0 (default) — degree IS visible for nth roots
    rad.append(radPr)
    deg = OxmlElement('m:deg')
    deg_r = OxmlElement('m:r')
    deg_t = OxmlElement('m:t')
    deg_t.text = degree_text
    deg_r.append(deg_t)
    deg.append(deg_r)
    rad.append(deg)
    e = OxmlElement('m:e')
    e_r = OxmlElement('m:r')
    e_t = OxmlElement('m:t')
    e_t.text = content_text
    e_r.append(e_t)
    e.append(e_r)
    rad.append(e)
    return rad

def add_omml_inline(paragraph, omml_element):
    """Append an OMML element inline in a paragraph (wrapped in <m:oMath>)."""
    omath = OxmlElement('m:oMath')
    omath.append(omml_element)
    paragraph._element.append(omath)
```

### S3-5 — Inline math renderer (v1.3; v1.4 hardened; v2.0 Tier-3 dispatch)

```python
# render_text_with_math() — TIER 2 SAFETY NET.
# Replaces p.add_run(text) in add_stem() and add_option().
# Catches RESIDUAL math patterns that the pipeline's Tier 1 detection missed.
# Does NOT handle complex expressions (trig fractions, operator expressions,
# nth roots) — those are Tier 1 (pipeline-level) responsibility.

import re

# False-positive exclusions: NOT math fractions
_UNIT_RATIO_RE = re.compile(
    r'(?:km|m|cm|mm|ft|mi|g|kg|mg|ml|rad|rev|₹\d*)'
    r'/(?:h|hr|s|sec|min|m|cm|l|ml|kg)',
    re.IGNORECASE
)
_DATE_RE = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4}')
_LOGICAL_RE = re.compile(r'\band/or\b', re.IGNORECASE)

def _find_math_spans(text):
    """
    Scan text for math expressions. Return list of
    (start, end, type, g1, g2, g3) sorted by position, non-overlapping.

    ASSUMES: residual ⟦SQRT:N⟧/[SQRT:N] markers have already been
    normalized to √N by the caller (render_text_with_math step 0).
    """
    spans = []

    # Pattern 1: Mixed number — 3(1/3), 12(2/5)
    for m in re.finditer(r'(\d+)\s*\(\s*(\d+)\s*/\s*(\d+)\s*\)', text):
        matched = m.group()
        if _UNIT_RATIO_RE.search(matched) or _DATE_RE.search(matched):
            continue
        spans.append((m.start(), m.end(), 'mixed',
                       m.group(1), m.group(2), m.group(3)))

    # Pattern 2: Fraction — digits (optionally with √) on each side of /
    # v1.4 FIX: clean regex — no false-positive letter characters.
    # \d* = optional leading digits, √? = optional √, \d+ = required digits.
    # Matches: 1/2, 7/12, 1/√3, √3/2, 2√3/5, 1/2√3.
    for m in re.finditer(r'(\d*√?\d+)\s*/\s*(\d*√?\d+)', text):
        matched = m.group()
        # Exclude unit ratios
        if _UNIT_RATIO_RE.search(matched):
            continue
        # Exclude and/or
        if _LOGICAL_RE.search(text[max(0, m.start()-4):m.end()+4]):
            continue
        # v1.4 DATE FIX: check surrounding context for DD/MM/YYYY pattern.
        # If the fraction match is part of a date, skip it.
        window_start = max(0, m.start() - 3)
        window_end = min(len(text), m.end() + 6)
        if _DATE_RE.search(text[window_start:window_end]):
            continue
        spans.append((m.start(), m.end(), 'frac',
                       m.group(1), m.group(2), None))

    # Pattern 3: Standalone √N (not inside a fraction — caught by Pattern 2)
    for m in re.finditer(r'√(\d+)', text):
        spans.append((m.start(), m.end(), 'sqrt', m.group(1), None, None))

    # (Pattern 4 removed in v1.4 — residual markers pre-normalized by caller)

    # Sort by position, resolve overlaps (keep longest/earliest match)
    spans.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    result = []
    last_end = 0
    for span in spans:
        if span[0] >= last_end:
            result.append(span)
            last_end = span[1]
    return result

def _t3_degrade(paragraph, body, err, bold=False, color=None):
    """GRACEFUL DEGRADATION (v2.0 — never halt, never silent, NO markup).

    A region the compiler rejects is DELIVERED as ORDINARY plain text —
    same Arial, same bold/colour as the surrounding run, no highlight, no
    colour flag of any kind — recorded in _T3_STATS['failed'], and surfaced
    by CHECK 20 in plain operator language. Findability lives in the
    REPORT, not in the document: CHECK 20 quotes the text verbatim, so the
    operator presses Ctrl+F in Word, pastes the quote, lands on the spot,
    fixes that ⟦MATH:⟧ spelling in the buffer, rebuilds. The compiler's
    strictness is preserved (the defect can never ship UNREPORTED); the
    run is preserved too (no condition halts a delivery — the
    framework-wide rule); the document stays visually clean.
    """
    _T3_STATS['failed'].append((body, str(err)))
    r = paragraph.add_run(body)
    set_font(r, bold=bold, color=color)

def render_text_with_math(paragraph, text, bold=False, color=None):
    """v2.0 DISPATCHER — Tier 3 first, then the v1.5 legacy path.

    ⟦MATH:…⟧ regions compile through the S3-5b compiler into ONE <m:oMath>
    each, appended inline at their position; every plain segment between
    regions goes through the byte-compatible v1.5 legacy path
    (_render_legacy: {{u}} underline split + Tier-2 safety net).

    A region that fails to compile — unknown command, unmatched brace,
    ragged matrix — NEVER halts the build and NEVER ships silently: it is
    rendered via _t3_degrade() (ordinary plain text, quoted verbatim in the
    CHECK 20 report for Ctrl+F). Damage is LOCALISED: every well-formed region still compiles;
    only the failing region — or, for a stray unpaired delimiter, only the
    plain segment carrying it (delimiters stripped) — degrades.
    """
    if MATH_OPEN in text or MATH_CLOSE in text:
        pos = 0
        for m in _REGION_RE.finditer(text):
            if m.start() > pos:
                _t3_plain_or_degrade(paragraph, text[pos:m.start()],
                                     bold=bold, color=color)
            try:
                paragraph._element.append(t3_compile(m.group(1)))
            except MathCompileError as err:
                _t3_degrade(paragraph, m.group(1), err, bold=bold, color=color)
            pos = m.end()
        if pos < len(text):
            _t3_plain_or_degrade(paragraph, text[pos:], bold=bold, color=color)
        return
    _render_legacy(paragraph, text, bold=bold, color=color)

def _t3_plain_or_degrade(paragraph, seg, bold=False, color=None):
    """Plain segment between regions. A stray unpaired ⟦MATH: or ⟧ marks the
    segment as a broken region: degrade JUST this segment (delimiters
    stripped so no ⟦ ⟧ residue reaches the document); neighbouring
    well-formed regions are unaffected."""
    if MATH_OPEN in seg or MATH_CLOSE in seg:
        _t3_degrade(paragraph,
                    seg.replace(MATH_OPEN, '').replace(MATH_CLOSE, ''),
                    'unbalanced ⟦MATH:⟧ delimiters', bold=bold, color=color)
    else:
        _render_legacy(paragraph, seg, bold=bold, color=color)

def _render_legacy(paragraph, text, bold=False, color=None):
    """
    TIER 2 SAFETY NET (the v1.5 render_text_with_math body, verbatim) —
    render PLAIN text with inline OMML and underline formatting.

    Processing order:
      Step 0a: Pre-normalize residual SQRT markers → clean √N
      Step 0b: Split on {{u}}...{{/u}} underline markers (v1.5)
      Step 1:  For each segment, find math spans and emit runs/OMML

    Handles compound expressions: 1/(2√3) → fraction with nested sqrt.
    Handles underlined text: {{u}}word{{/u}} → run with underline=True.
    Excludes false positives: km/h, m/s, dates, and/or.
    """
    # Step 0a: Pre-normalize ALL residual pipeline markers to clean √N
    text = re.sub(r'[⟦\[]SQRT:(\d+)[⟧\]]', lambda m: '√' + m.group(1), text)

    # Step 0b: Split on underline markers, process each part (v1.5)
    if '{{u}}' in text:
        parts = re.split(r'(\{\{u\}\}.*?\{\{/u\}\})', text)
        for part in parts:
            if part.startswith('{{u}}') and part.endswith('{{/u}}'):
                inner = part[5:-6]  # Strip {{u}} and {{/u}}
                _emit_text_with_math(paragraph, inner,
                                     bold=bold, color=color, underline=True)
            elif part:
                _emit_text_with_math(paragraph, part,
                                     bold=bold, color=color, underline=False)
        return

    # No underline markers — standard path
    _emit_text_with_math(paragraph, text, bold=bold, color=color, underline=False)

def _emit_text_with_math(paragraph, text, bold=False, color=None, underline=False):
    """
    Core renderer for a single text segment (may or may not be underlined).
    Finds math spans and emits alternating text-runs + OMML elements.
    All text runs in this segment share the same bold/color/underline state.
    """
    spans = _find_math_spans(text)

    if not spans:
        if text:
            r = paragraph.add_run(text)
            set_font(r, bold=bold, color=color, underline=underline)
        return

    pos = 0
    for start, end, mtype, g1, g2, g3 in spans:
        if pos < start:
            before = text[pos:start]
            if before:
                r = paragraph.add_run(before)
                set_font(r, bold=bold, color=color, underline=underline)

        if mtype == 'frac':
            omml_el = omml_frac(g1, g2)
        elif mtype == 'mixed':
            r = paragraph.add_run(g1)
            set_font(r, bold=bold, color=color, underline=underline)
            omml_el = omml_frac(g2, g3)
        elif mtype == 'sqrt':
            omml_el = omml_sqrt(g1)
        else:
            r = paragraph.add_run(text[start:end])
            set_font(r, bold=bold, color=color, underline=underline)
            pos = end
            continue

        add_omml_inline(paragraph, omml_el)
        pos = end

    if pos < len(text):
        after = text[pos:]
        if after:
            r = paragraph.add_run(after)
            set_font(r, bold=bold, color=color, underline=underline)
```

### S3-5b — Tier-3 structured math compiler (v2.0)

```
The deterministic LaTeX-lite → OMML compiler behind Tier 3 (S1-6). One
⟦MATH:…⟧ region → one <m:oMath>. Grammar, commands and failure semantics
are documented in the code header below; the load-bearing properties are:

  DETERMINISTIC   the same region always compiles to the same XML — no
                  regex guessing, no context sensitivity.
  STRICT CORE     MathCompileError on any unknown command, unmatched
                  brace, ragged matrix, script without base, or literal √
                  before a non-digit — deterministically, with the failing
                  region named.
  FORGIVING       …but the failure NEVER halts a run and NEVER ships
  BOUNDARY        silently: render_text_with_math() catches it and
                  delivers the region as ORDINARY plain text — no colour,
                  no highlight — recorded in _T3_STATS['failed'] and
                  quoted VERBATIM by CHECK 20 so Ctrl+F finds it, with the
                  remedy in plain operator language. (Silent fallback is what
                  produced GAP-2026-08-07-OMML; a halt is what the
                  framework-wide no-halt rule forbids. This is the third
                  road.)
  WIDE GRAMMAR    common LaTeX habits compile instead of degrading:
                  Greek names, relation/arrow/set symbols, \hat \bar
                  \tilde \vec \dot \ddot accents, \binom.
  TRUE OPERANDS   \int/\sum/… consume the rest of their scope as <m:e>,
                  so nesting is semantically correct and NO engine renders
                  a placeholder box. Scope a big operator with \paren{…}
                  or a {…} group when it must not swallow trailing text.
  ENGINE-PROOF    empty required slots are filled with a preserved space:
                  Word shows no dotted box, LibreOffice shows no ❑.
  COUNTABLE       _T3_STATS['compiled'] and count_math_regions() feed the
                  CHECK 20 round-trip proof.

Script arguments SHOULD be braced (x^{2}, not x^2); an unbraced argument
takes exactly one atom. A base ending in ")" attaches its whole balanced
(…) group — (1 + x)^{2} superscripts the group, not the parenthesis.
```

```python
# ── S3-5b — TIER 3 STRUCTURED MATH COMPILER (v2.0) ──────────────────────────────
# Deterministic LaTeX-lite → OMML compiler. Replaces regex reconstruction for all
# structural math. A transcription buffer wraps each non-trivial expression in
# ⟦MATH: ... ⟧; the compiler emits ONE homogeneous <m:oMath> per region.
#
# STRICT CORE, FORGIVING BOUNDARY (v2.0): the compiler itself is strict — an
# unknown command or malformed region raises MathCompileError, deterministically.
# The RENDERER (S3-5 render_text_with_math) catches it: the run NEVER halts and
# the defect NEVER ships silently — the region is delivered as ORDINARY plain
# text (no colour, no highlight — it blends with the surrounding run styling),
# recorded in _T3_STATS['failed'], and reported by CHECK 20 in plain operator
# language, quoting the exact text so the operator can Ctrl+F straight to it.
# That is the GAP-2026-08-07-OMML remedy M2 contract.
#
# Grammar (region body):
#   literal text            any chars except { } ^ _ \   (√N auto-→ <m:rad>)
#   {...}                   grouping (inlined; use as ^/_ argument)
#   base^{sup}  base_{sub}  scripts — attach to preceding atom; both orders
#                           merge into <m:sSubSup>; base "...)"-terminated
#                           literals attach to the balanced (...) group
#   \frac{a}{b}             stacked fraction        <m:f>
#   \sfrac{a}{b}            skewed fraction         <m:f m:type="skw">
#   \sqrt{a}  \root{n}{a}   radicals                <m:rad>
#   \int \iint \oint        n-ary, limits subSup    <m:nary>  (scripts optional)
#   \sum \prod              n-ary, limits undOvr    <m:nary>
#   \sumi \prodi            n-ary, limits subSup (inline running-text style)
#   \lim_{...}              limit-below             <m:limLow>
#   \cases{a, & c1\\ b, & c2}   cases brace         <m:d "{"> + <m:eqArr>
#   \pmatrix{a & b\\ c & d}     ( ) matrix          <m:d> + <m:m>   (also
#   \bmatrix [ ]   \vmatrix | |   \matrix (bare)     — rows \\, cells &)
#   \pre{sub}{sup}{base}    prescripts (ⁿCᵣ)        <m:sPre>
#   \paren{a} \brack{a} \set{a} \abs{a}   stretchy ( ) [ ] { } | | <m:d>
#   \text{...}              roman (upright) text run
#   \sin \cos \tan \sec \csc \cot \log \ln \exp \det \max \min  roman functions
#   \{ \} \& \\ \^ \_ \(space)   escaped literal characters
#
# Empty required slots (e.g. \pre{}{13}{C}) are filled with U+200B so Word never
# shows a dotted placeholder box.

import re as _t3_re

MATH_OPEN = '\u27e6MATH:'      # ⟦MATH:
MATH_CLOSE = '\u27e7'          # ⟧
_REGION_RE = _t3_re.compile(_t3_re.escape(MATH_OPEN) + '(.*?)'
                            + _t3_re.escape(MATH_CLOSE), _t3_re.S)
_T3_STATS = {'compiled': 0, 'failed': []}   # CHECK 20 round-trip + degrade ledger


class MathCompileError(ValueError):
    """Tier-3 compile failure — the region cannot be structured. The S3-5
    renderer catches this and degrades the region to ordinary plain text
    (quoted verbatim in the CHECK 20 report so it can be found with Ctrl+F);
    the build CONTINUES (never halt, never silent)."""


_T3_NARY = {
    'int':  ('\u222b', 'subSup'), 'iint': ('\u222c', 'subSup'),
    'oint': ('\u222e', 'subSup'),
    'sum':  ('\u2211', 'undOvr'), 'prod': ('\u220f', 'undOvr'),
    'sumi': ('\u2211', 'subSup'), 'prodi': ('\u220f', 'subSup'),
}
_T3_MATRIX = {'pmatrix': ('(', ')'), 'bmatrix': ('[', ']'),
              'vmatrix': ('|', '|'), 'matrix': ('', '')}
_T3_DELIM = {'paren': ('(', ')'), 'brack': ('[', ']'),
             'set': ('{', '}'), 'abs': ('|', '|')}
_T3_FUNCS = {'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'ln', 'exp',
             'det', 'sinh', 'cosh', 'tanh', 'gcd', 'arg'}
_T3_LIMWORDS = {'lim', 'max', 'min'}
_T3_ACCENTS = {'hat': '\u0302', 'tilde': '\u0303', 'bar': '\u0305',
               'vec': '\u20d7', 'dot': '\u0307', 'ddot': '\u0308'}
_T3_SYMBOLS = {
    # Greek
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
    'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'iota': 'ι', 'kappa': 'κ',
    'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'pi': 'π', 'rho': 'ρ',
    'sigma': 'σ', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ', 'chi': 'χ',
    'psi': 'ψ', 'omega': 'ω', 'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ',
    'Lambda': 'Λ', 'Xi': 'Ξ', 'Pi': 'Π', 'Sigma': 'Σ', 'Phi': 'Φ',
    'Psi': 'Ψ', 'Omega': 'Ω',
    # relations / operators / arrows / sets
    'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥', 'ne': '≠', 'neq': '≠',
    'pm': '±', 'mp': '∓', 'times': '×', 'cdot': '·', 'div': '÷',
    'in': '∈', 'notin': '∉', 'subset': '⊂', 'subseteq': '⊆',
    'supset': '⊃', 'supseteq': '⊇', 'cup': '∪', 'cap': '∩',
    'infty': '∞', 'partial': '∂', 'nabla': '∇', 'forall': '∀',
    'exists': '∃', 'to': '→', 'rightarrow': '→', 'leftarrow': '←',
    'Rightarrow': '⇒', 'Leftarrow': '⇐', 'mapsto': '↦', 'approx': '≈',
    'equiv': '≡', 'propto': '∝', 'sim': '~', 'emptyset': '∅',
    'setminus': '∖', 'mid': '|', 'circ': '∘', 'star': '⋆', 'cdots': '⋯',
    'ldots': '…', 'because': '∵', 'therefore': '∴', 'angle': '∠',
    'perp': '⊥', 'parallel': '∥', 'cong': '≅', 'oplus': '⊕',
    'otimes': '⊗', 'wedge': '∧', 'vee': '∨', 'neg': '¬', 'prime': '′',
    'degree': '°',
}


def _t3_run(text):
    r = OxmlElement('m:r')
    t = OxmlElement('m:t')
    t.text = text
    if text != text.strip():
        t.set(qn('xml:space'), 'preserve')
    r.append(t)
    return r


def _t3_run_roman(text):
    r = OxmlElement('m:r')
    rPr = OxmlElement('m:rPr')
    sty = OxmlElement('m:sty')
    sty.set(qn('m:val'), 'p')
    rPr.append(sty)
    r.append(rPr)
    t = OxmlElement('m:t')
    t.text = text
    if text != text.strip():
        t.set(qn('xml:space'), 'preserve')
    r.append(t)
    return r


def _t3_wrap(tag, children):
    el = OxmlElement(tag)
    for c in children:
        el.append(c)
    return el


def _t3_content(elems):
    """Non-empty content list — empty slots get a preserved-space run so neither
    Word (dotted box) nor LibreOffice (\u274f placeholder) shows an artefact."""
    return elems if elems else [_t3_run(' ')]


def _t3_e(elems):
    return _t3_wrap('m:e', _t3_content(elems))


def _t3_delim(beg, end, elems):
    d = OxmlElement('m:d')
    if beg != '(' or end != ')':
        dPr = OxmlElement('m:dPr')
        b = OxmlElement('m:begChr'); b.set(qn('m:val'), beg); dPr.append(b)
        en = OxmlElement('m:endChr'); en.set(qn('m:val'), end); dPr.append(en)
        d.append(dPr)
    d.append(_t3_e(elems))
    return d


def _t3_frac(num_elems, den_elems, skewed=False, nobar=False):
    f = OxmlElement('m:f')
    if skewed or nobar:
        fPr = OxmlElement('m:fPr')
        ty = OxmlElement('m:type')
        ty.set(qn('m:val'), 'skw' if skewed else 'noBar')
        fPr.append(ty)
        f.append(fPr)
    f.append(_t3_wrap('m:num', _t3_content(num_elems)))
    f.append(_t3_wrap('m:den', _t3_content(den_elems)))
    return f


def _t3_rad(deg_elems, content_elems):
    rad = OxmlElement('m:rad')
    radPr = OxmlElement('m:radPr')
    if deg_elems is None:
        dh = OxmlElement('m:degHide'); dh.set(qn('m:val'), '1'); radPr.append(dh)
    rad.append(radPr)
    deg = OxmlElement('m:deg')
    if deg_elems is not None:
        for el in _t3_content(deg_elems):
            deg.append(el)
    rad.append(deg)
    rad.append(_t3_e(content_elems))
    return rad


def _t3_nary(chr_, limloc, sub_elems, sup_elems, operand_elems):
    n = OxmlElement('m:nary')
    pr = OxmlElement('m:naryPr')
    c = OxmlElement('m:chr'); c.set(qn('m:val'), chr_); pr.append(c)
    ll = OxmlElement('m:limLoc'); ll.set(qn('m:val'), limloc); pr.append(ll)
    if sub_elems is None:
        sh = OxmlElement('m:subHide'); sh.set(qn('m:val'), '1'); pr.append(sh)
    if sup_elems is None:
        sh = OxmlElement('m:supHide'); sh.set(qn('m:val'), '1'); pr.append(sh)
    n.append(pr)
    if sub_elems is not None:
        n.append(_t3_wrap('m:sub', _t3_content(sub_elems)))
    if sup_elems is not None:
        n.append(_t3_wrap('m:sup', _t3_content(sup_elems)))
    n.append(_t3_e(operand_elems))             # true operand — rest of scope
    return n


def _t3_limlow(word, sub_elems):
    ll = OxmlElement('m:limLow')
    ll.append(_t3_e([_t3_run_roman(word)]))
    ll.append(_t3_wrap('m:lim', _t3_content(sub_elems)))
    return ll


def _t3_acc(chr_, base_elems):
    acc = OxmlElement('m:acc')
    pr = OxmlElement('m:accPr')
    c = OxmlElement('m:chr'); c.set(qn('m:val'), chr_); pr.append(c)
    acc.append(pr)
    acc.append(_t3_e(base_elems))
    return acc


def _t3_spre(sub_elems, sup_elems, base_elems):
    sp = OxmlElement('m:sPre')
    sp.append(_t3_wrap('m:sub', _t3_content(sub_elems)))
    sp.append(_t3_wrap('m:sup', _t3_content(sup_elems)))
    sp.append(_t3_e(base_elems))
    return sp


def _t3_group_raw(s, i):
    """s[i] == '{' → (raw_body, index_after_close), escape- and nest-aware."""
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise MathCompileError("unclosed '{' in %r" % s)


def _t3_req_group_raw(s, j, cmd):
    while j < len(s) and s[j] == ' ':
        j += 1
    if j >= len(s) or s[j] != '{':
        raise MathCompileError("\\%s expects a {…} argument in %r" % (cmd, s))
    return _t3_group_raw(s, j)


def _t3_compile_group(raw):
    elems, _ = _t3_seq(raw, 0, top=True)
    return elems


def _t3_rows(raw):
    rows, buf, depth, i = [], [], 0, 0
    while i < len(raw):
        c = raw[i]
        if c == '\\':
            if i + 1 < len(raw) and raw[i + 1] == '\\' and depth == 0:
                rows.append(''.join(buf)); buf = []; i += 2; continue
            buf.append(raw[i:i + 2]); i += 2; continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        buf.append(c); i += 1
    rows.append(''.join(buf))
    return rows


def _t3_cells(row):
    cells, buf, depth, i = [], [], 0, 0
    while i < len(row):
        c = row[i]
        if c == '\\':
            buf.append(row[i:i + 2]); i += 2; continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        if c == '&' and depth == 0:
            cells.append(''.join(buf)); buf = []; i += 1; continue
        buf.append(c); i += 1
    cells.append(''.join(buf))
    return cells


def _t3_cases(raw):
    rows = _t3_rows(raw)
    if len(rows) < 2:
        raise MathCompileError("\\cases needs ≥2 rows (\\\\-separated): %r" % raw)
    eq = OxmlElement('m:eqArr')
    for row in rows:
        content = []
        for k, cell in enumerate(_t3_cells(row)):
            if k:
                content.append(_t3_run('  '))
            content.extend(_t3_compile_group(cell.strip()))
        eq.append(_t3_e(content))
    return _t3_delim('{', '', [eq])


def _t3_matrix(raw, beg, end):
    rows = _t3_rows(raw)
    mm = OxmlElement('m:m')
    width = None
    for row in rows:
        cells = _t3_cells(row)
        if width is None:
            width = len(cells)
        elif len(cells) != width:
            raise MathCompileError(
                "ragged matrix — row widths %d vs %d in %r" % (width, len(cells), raw))
        mr = OxmlElement('m:mr')
        for cell in cells:
            mr.append(_t3_e(_t3_compile_group(cell.strip())))
        mm.append(mr)
    if beg == '' and end == '':
        return mm
    return _t3_delim(beg, end, [mm])


def _t3_literal(out, chunk):
    pos = 0
    for m in _t3_re.finditer('\u221a(\\d+)', chunk):
        if m.start() > pos:
            out.append(_t3_run(chunk[pos:m.start()]))
        out.append(_t3_rad(None, [_t3_run(m.group(1))]))
        pos = m.end()
    rest = chunk[pos:]
    if '\u221a' in rest:
        raise MathCompileError(
            "literal \u221a before non-digit in %r — use \\sqrt{…}" % chunk)
    if rest:
        out.append(_t3_run(rest))


def _t3_pop_base(out, kind):
    if not out:
        raise MathCompileError("script '%s' has no base" % kind)
    base = out.pop()
    if base.tag == qn('m:r') and base.find(qn('m:rPr')) is None:
        t_el = base.find(qn('m:t'))
        txt = (t_el.text or '').rstrip()
        if not txt:
            raise MathCompileError("script '%s' base is empty text" % kind)
        if len(txt) > 1:
            if txt.endswith(')'):
                depth, k = 0, len(txt) - 1
                while k >= 0:
                    if txt[k] == ')':
                        depth += 1
                    elif txt[k] == '(':
                        depth -= 1
                        if depth == 0:
                            break
                    k -= 1
                split = k if (k >= 0 and depth == 0) else len(txt) - 1
            else:
                split = len(txt) - 1
            if split > 0:
                out.append(_t3_run(txt[:split]))
                base = _t3_run(txt[split:])
            else:
                base = _t3_run(txt)
        else:
            base = _t3_run(txt)
    return base


def _t3_children(el, *tags):
    return [el.find(qn(t)) for t in tags]


def _t3_script(s, i, out):
    kind = s[i]
    atoms, j = _t3_atom(s, i + 1)
    prev = out[-1] if out else None
    # merge x_a^b / x^b_a into m:sSubSup
    if prev is not None and prev.tag == qn('m:sSub') and kind == '^':
        e_el, sub_el = _t3_children(prev, 'm:e', 'm:sub')
        out.pop()
        ss = OxmlElement('m:sSubSup')
        ss.append(e_el); ss.append(sub_el)
        ss.append(_t3_wrap('m:sup', _t3_content(atoms)))
        out.append(ss)
        return j
    if prev is not None and prev.tag == qn('m:sSup') and kind == '_':
        e_el, sup_el = _t3_children(prev, 'm:e', 'm:sup')
        out.pop()
        ss = OxmlElement('m:sSubSup')
        ss.append(e_el)
        ss.append(_t3_wrap('m:sub', _t3_content(atoms)))
        ss.append(sup_el)
        out.append(ss)
        return j
    base = _t3_pop_base(out, kind)
    tag = 'm:sSup' if kind == '^' else 'm:sSub'
    arg = 'm:sup' if kind == '^' else 'm:sub'
    ss = OxmlElement(tag)
    ss.append(_t3_e([base]))
    ss.append(_t3_wrap(arg, _t3_content(atoms)))
    out.append(ss)
    return j


def _t3_atom(s, i):
    if i >= len(s):
        raise MathCompileError("script or command runs off end of region %r" % s)
    c = s[i]
    if c == '{':
        raw, j = _t3_group_raw(s, i)
        return _t3_compile_group(raw), j
    if c == '\\':
        out = []
        j = _t3_command(s, i, out)
        return out, j
    if c == '\u221a':
        m = _t3_re.match('\u221a(\\d+)', s[i:])
        if m:
            return [_t3_rad(None, [_t3_run(m.group(1))])], i + m.end()
        raise MathCompileError("literal \u221a before non-digit — use \\sqrt{…}")
    return [_t3_run(c)], i + 1


def _t3_command(s, i, out):
    m = _t3_re.match(r'\\([A-Za-z]+)', s[i:])
    if not m:
        nc = s[i + 1] if i + 1 < len(s) else ''
        if nc in '{}&\\^_ ':
            out.append(_t3_run(nc))
            return i + 2
        raise MathCompileError("bad escape '\\%s' in %r" % (nc, s))
    name = m.group(1)
    j = i + m.end()
    if name in ('frac', 'sfrac'):
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_frac(_t3_compile_group(a), _t3_compile_group(b),
                            skewed=(name == 'sfrac')))
        return j
    if name == 'sqrt':
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_rad(None, _t3_compile_group(a)))
        return j
    if name == 'root':
        d, j = _t3_req_group_raw(s, j, name)
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_rad(_t3_compile_group(d), _t3_compile_group(a)))
        return j
    if name in _T3_DELIM:
        a, j = _t3_req_group_raw(s, j, name)
        beg, end = _T3_DELIM[name]
        out.append(_t3_delim(beg, end, _t3_compile_group(a)))
        return j
    if name == 'text':
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_run_roman(a))
        return j
    if name in _T3_NARY:
        ch, loc = _T3_NARY[name]
        sub = sup = None
        while j < len(s) and s[j] in '^_':
            k = s[j]
            atoms, j = _t3_atom(s, j + 1)
            if k == '_':
                sub = atoms
            else:
                sup = atoms
        rest, _ = _t3_seq(s, j, top=True)   # operand = remainder of this scope
        out.append(_t3_nary(ch, loc, sub, sup, rest))
        return len(s)
    if name in _T3_LIMWORDS:
        if j < len(s) and s[j] == '_':
            atoms, j = _t3_atom(s, j + 1)
            out.append(_t3_limlow(name, atoms))
            return j
        out.append(_t3_run_roman(name))
        return j
    if name in _T3_FUNCS:
        out.append(_t3_run_roman(name))
        return j
    if name == 'cases':
        raw, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_cases(raw))
        return j
    if name in _T3_MATRIX:
        raw, j = _t3_req_group_raw(s, j, name)
        beg, end = _T3_MATRIX[name]
        out.append(_t3_matrix(raw, beg, end))
        return j
    if name in _T3_ACCENTS:
        a, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_acc(_T3_ACCENTS[name], _t3_compile_group(a)))
        return j
    if name == 'binom':
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        f = _t3_frac(_t3_compile_group(a), _t3_compile_group(b), nobar=True)
        out.append(_t3_delim('(', ')', [f]))
        return j
    if name in _T3_SYMBOLS:
        out.append(_t3_run(_T3_SYMBOLS[name]))
        return j
    if name == 'pre':
        a, j = _t3_req_group_raw(s, j, name)
        b, j = _t3_req_group_raw(s, j, name)
        c, j = _t3_req_group_raw(s, j, name)
        out.append(_t3_spre(_t3_compile_group(a), _t3_compile_group(b),
                            _t3_compile_group(c)))
        return j
    raise MathCompileError(
        "unknown command \\%s — not in the Tier-3 grammar (S3-5b). The renderer "
        "delivers this region as plain text and CHECK 20 quotes it; fix the "
        "⟦MATH:⟧ spelling in the buffer and rebuild" % name)


def _t3_seq(s, i, top=False):
    out = []
    while i < len(s):
        c = s[i]
        if c == '}':
            if top:
                raise MathCompileError("unmatched '}' at %d in %r" % (i, s))
            return out, i + 1
        if c == '{':
            raw, i = _t3_group_raw(s, i)
            out.extend(_t3_compile_group(raw))
        elif c in '^_':
            i = _t3_script(s, i, out)
        elif c == '\\':
            i = _t3_command(s, i, out)
        else:
            jj = i
            while jj < len(s) and s[jj] not in '{}^_\\':
                jj += 1
            _t3_literal(out, s[i:jj])
            i = jj
    if top:
        return out, i
    raise MathCompileError("missing '}' in %r" % s)


def t3_compile(body):
    """Compile one ⟦MATH:…⟧ region body → a single <m:oMath> element."""
    if MATH_OPEN in body or MATH_CLOSE in body:
        raise MathCompileError("nested/unbalanced region delimiters in %r" % body)
    if '\n' in body or '\t' in body:
        raise MathCompileError("⟦MATH:⟧ region must be single-line: %r" % body)
    elems, _ = _t3_seq(body, 0, top=True)
    if not elems:
        raise MathCompileError("empty ⟦MATH:⟧ region")
    om = OxmlElement('m:oMath')
    for e in elems:
        om.append(e)
    _T3_STATS['compiled'] += 1
    return om


def count_math_regions(*texts):
    """Region count across buffer strings (CHECK 20 producer side)."""
    n = 0
    for t in texts:
        if not t:
            continue
        n += len(_t3_re.findall(_t3_re.escape(MATH_OPEN), t))
    return n
```

---

## §4 — DOCUMENT BUILDER

### S4-1 — Document setup

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

NAVY = RGBColor(0x00, 0x33, 0x66)

def set_font(run, bold=False, color=None, underline=False):
    """Standard font setter — Arial 11pt. Supports underline (v1.5)."""
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.bold = bold
    if color:
        run.font.color.rgb = color
    if underline:
        run.underline = True

def create_document():
    """Create a new Row file document with standard page setup."""
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Inches(8.27)    # A4
    sec.page_height = Inches(11.69)  # A4
    sec.left_margin = Inches(1)
    sec.right_margin = Inches(1)
    sec.top_margin = Inches(1)
    sec.bottom_margin = Inches(1)
    return doc

# MATH RUNS ARE EXEMPT FROM THE ARIAL RULE (v2.0 — M5).
# <m:oMath> content takes Word's math default (Cambria Math, math italic),
# matching source-PDF typography. set_font() is for <w:r> prose runs ONLY —
# never inject w:rPr fonts into m:r runs; \text{…}/function names carry
# m:sty="p" (roman) and nothing else.
```

### S4-2 — Element builders

```python
def add_blank(doc):
    """Add a blank separator paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    return p

def add_date_label(doc, date_text):
    """
    Add date label paragraph.
    date_text: "[DD-Mon-YYYY]" or "[DD-Mon-YYYY Shift 1]" — full string.
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run(date_text)
    set_font(r, bold=True, color=NAVY)
    r.italic = False
    return p

def add_stem(doc, n, text):
    """Add question stem paragraph. n=continuous number, text=stem content.
    Uses render_text_with_math() for inline OMML (v1.3)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    render_text_with_math(p, f"Q.{n}  {text}".rstrip(), bold=True)
    return p

def add_stem_figure_only(doc, n):
    """Add Q.N for figure-only stem (no text — placeholder follows)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(f"Q.{n}")
    set_font(r, bold=True)
    return p

def add_option(doc, n, text):
    """Add option paragraph with canonical format.
    Uses render_text_with_math() for inline OMML (v1.3)."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(18)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    render_text_with_math(p, f"{n}. {text}")
    return p

def add_passage(doc, text):
    """Add passage paragraph (plain, not bold)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(text)
    set_font(r)
    return p

def add_placeholder_stem(doc, red_png_path):
    """Add red placeholder image for figure stem."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run()
    r.add_picture(red_png_path, width=Inches(3.0))
    return p

def add_placeholder_opt_set(doc, n_options, red_png_path):
    """
    Add red placeholders for a WHOLE figure-option set (v1.14, S1-8b RULE B2).

    ONE borderless table, one ROW per option: [label | image].

    Replaces add_placeholder_opt(), which built one table PER OPTION and so
    emitted four adjacent w:tbl siblings. Two adjacent block tables are FUSED
    into a single table by every Word engine (S1-8b), so the four option blocks
    silently became one — invisible in the emitted file, visible the moment Word
    opened it. Measured: 19 tables written, 7 after a Word-engine round-trip.
    One table for the set is fusion-proof and matches the ALL-or-NONE rule.
    """
    tbl = doc.add_table(rows=n_options, cols=2)
    tbl.autofit = False
    # Remove borders
    tbl_pr = tbl._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'none')
        e.set(qn('w:sz'), '0')
        e.set(qn('w:space'), '0')
        e.set(qn('w:color'), 'auto')
        borders.append(e)
    tbl_pr.append(borders)
    for i in range(n_options):
        # Label cell
        cell_label = tbl.cell(i, 0)
        cell_label.text = f"{i + 1}."
        for r in cell_label.paragraphs[0].runs:
            set_font(r)
        # Image cell
        cell_img = tbl.cell(i, 1)
        p = cell_img.paragraphs[0]
        r = p.add_run()
        r.add_picture(red_png_path, width=Inches(2.5))
    return tbl
```

### S4-3 — DI table builder (v1.14 — DELEGATED to corpus_io Cluster I)

```
The implementation is OWNED BY corpus_io and is NOT restated here. Two builders
modelled one concept before v1.14 — this one and build_di_table_styled() in
Framework_MockTestCreate S8-4 — and BOTH modelled a table as a rectangle of
strings, so neither could express a merged cell. Two implementations under one
concept emit zero drift signal until they disagree, which is precisely how a
grouped header stayed unrepresentable through thirteen versions of this spec.

corpus_io provides:
  normalise_table_spec(spec)   legacy list-of-lists OR TableSpec -> TableSpec
  place_cells(grid)            HTML occupancy placement -> (placements, width,
                               nrows, errors); 'hole' / 'overlap' are reported
  build_di_table(doc, spec, font_pt=9, default_align='center', render=None)
  read_table_spec(tbl, doc)    a built table -> TableSpec, spans included
  table_spec_spans(spec)       a TableSpec -> its spans (CHECK 17, both sides)
  adjacent_table_pairs(doc)    fused-block counter    (CHECK 18 input)

ORDERING INSIDE THE BUILDER IS LOAD-BEARING and is the easiest thing to get
wrong on a re-implementation:
  1. write text into ANCHOR cells
  2. THEN merge
  3. THEN stamp per-cell column widths
cell.merge() CONCATENATES the text of both cells ('A' + 'B' -> 'A\nB', verified
on python-docx 1.2.0), so text must never be written into a covered position and
merging must never precede text placement.

Pass render=render_text_with_math so cell content gets the SAME OMML and {{u}}
underline treatment as stems and options (S1-6, S1-11).
```

```python
import corpus_io      # routed to PYQPrepare in routes.json

def build_di_table(doc, spec, font_pt=9):
    """Thin forwarding adapter — implementation owned by corpus_io (Cluster I).

    spec: a TableSpec (S1-8a) or a legacy list of lists.
    """
    return corpus_io.build_di_table(doc, spec, font_pt=font_pt,
                                    render=render_text_with_math)
```

---

## §5 — VALIDATION (warn on failure, deliver anyway)

### S5-1 — Validation checks

```
Step 1 validation runs AFTER document generation and BEFORE delivery.
If any check FAILS, Claude logs a WARNING but still delivers the file.
Source data quality varies widely — some issues are inherent to the source,
not Step 1 bugs.

CHECK 1 — Q-COUNT
  Count Q.N paragraphs in output. Report total.
  Warn if count seems low for the exam type (heuristic, not hard-fail).

CHECK 2 — SEQUENTIAL NUMBERING
  Q-numbers must be Q.1, Q.2, ..., Q.N with no gaps and no duplicates.
  WARN if any gap or duplicate found.

CHECK 3 — DATE LABEL COUNT
  Count date label paragraphs. Must equal Q-count.
  WARN if mismatch.

CHECK 4 — DATE LABEL FORMAT
  Every date label must match:
    WITH session:    ^\[(\d{1,2})-([A-Za-z]{3})-(\d{4})\s+.+\s+\d+\]$
    WITHOUT session: ^\[(\d{1,2})-([A-Za-z]{3})-(\d{4})\]$
  WARN if any label doesn't match.

CHECK 5 — DATE LABEL STYLING
  All date labels: RIGHT aligned, bold, navy #003366, non-italic.
  WARN if any style mismatch.

CHECK 6 — NO METADATA LEAKAGE
  Scan all paragraphs for leaked metadata patterns:
    Question ID, Option N ID, Status :, Chosen Option, SubQuestion No,
    Roll Number, Candidate Name, Venue Name, Exam Date, Exam Time,
    Section :, Comprehension: (as standalone label), ===.*===
  Also: third-party brands, URLs, app handles.
  WARN on any match.

CHECK 7 — NO CONTROL OR ZERO-WIDTH CHARACTERS (v2.1, GAP-2026-08-15-BAREQ)
  Scan all paragraph text for C0 control bytes AND the zero-width class:
    [\x00-\x08\x0b\x0c\x0e-\x1f\u200b-\u200d\u2060\ufeff]
  Zero-width characters are not matched by \s and not removed by str.strip(),
  so "Q.4<ZWSP>" defeats every Q_PATTERNS entry and the question disappears at
  Step 3 with nothing on screen to show why. WARN if any found (S2-4 sanitise()
  missed something) and NAME the affected Q-numbers.

CHECK 8 — NO ANSWER MARKERS
  Scan for ✓ ✔ ✗ ✘ characters and "Ans" / "Ans." text.
  WARN if any found.

CHECK 9 — OPTIONS FORMAT (v2.0)
  Every option paragraph should match r'^[1-5]\.\s+'  OR  be a bare label
  r'^[1-5]\.\s*$' whose paragraph carries an <m:oMath> payload — an
  OMML-only option (e.g. a fraction or a column vector) is CANONICAL, the
  producer-side mirror of corpus_io's S-1 consumer rule (is_option with
  para). Downstream text audits read corpus_io.text_of(), which
  concatenates <w:t> AND <m:t> (M3). WARN on anything else.

CHECK 10 — OMML STRUCTURAL INTEGRITY
  Traverse OMML XML for broken <m:sSup> / <m:sSub> elements.
  WARN if structural issues found.

CHECK 11 — RESIDUAL MATH MARKERS (v1.3)
  Scan ALL <m:t> elements AND all paragraph text for unresolved math
  markers that should have been converted to OMML. Detect:
    - ⟦SQRT:N⟧ or [SQRT:N] tags (pipeline residuals)
    - Literal √ followed by digits inside <m:t> (should be <m:rad>)
    - Any text matching r'SQRT:\d+' in the document
  WARN for each occurrence. These indicate build_compound_content()
  or render_text_with_math() failed to process a math expression.

CHECK 12 — SEMANTIC UNDERLINE VALIDATION (v1.5)
  Scan all stem paragraphs (bold, starting with Q.\d+). For each stem
  that contains the word "underlined" (case-insensitive), check if ANY
  run in the question block (stem + the sentence paragraph following it)
  has run.underline = True. If stem says "underlined" but no underline
  formatting exists → WARN. This catches extraction failures where
  underlines were not detected from the source.
  Also WARN if {{u}} or {{/u}} markers appear as literal text in any
  paragraph (they should have been processed by render_text_with_math).

CHECK 13 — IMAGE CLASSIFICATION VERIFICATION (v1.6)
  Cross-reference the IMAGE_CLASSIFICATIONS log against the built
  document. For every image classified as MATH-IMAGE, TABLE-IMAGE,
  or TEXT-IMAGE, verify that the corresponding question in the output
  contains TRANSCRIBED CONTENT (not a red-box substitute). Detect
  red-box images in the output (inline images with width=3.0 inches)
  and check if any correspond to non-VISUAL classified images.
  Also check for UNCLASSIFIED images — any image paragraph that was
  not in IMAGE_CLASSIFICATIONS at all.
  WARN for:
    - Any MATH/TABLE/TEXT classified image that has a red box in the
      output (transcription was not applied)
    - Any unclassified image paragraph (Phase A-IMAGE was incomplete)
  This check catches the exact production defect that v1.6 was
  designed to prevent: math questions delivered with red boxes
  instead of transcribed content.

CHECK 14 — VISION PROVENANCE CONSISTENCY (v1.7)
  For vision-transcribed Row files (FORMAT C1 / C-HYBRID): the trust
  marker must be coherent. If EITHER the doc core-property category
  carries "PYQPrepare-Source-Trust:" OR the filename ends with
  "__vision-unverified", then BOTH must be present. WARN on any
  half-marked file. (The marker itself is set at build time in the
  S1-13 path — this check is the safety net.)

CHECK 15 — SPECIMEN / OUT-OF-RANGE EXCLUSION (v1.7)
  Scanned papers often carry a demonstration "sample question" with an
  out-of-range number (e.g. "Q.201", नमुना प्रश्न / "sample question" /
  "specimen"). It must NOT appear in the Row file. WARN if any stem text
  contains a specimen marker, or if any Q-number exceeds the built count
  (a specimen leaking through).

CHECK 16 — Q-COUNT vs STATED-TOTAL (v1.7)
  If the source cover states a total ("Total Questions: N" / "एकूण प्रश्न")
  and that number is passed as stated_total, compare it to the built
  Q-count. WARN on mismatch (dropped, duplicated, or specimen questions).
  Skipped silently when stated_total is not available.

CHECK 17 — TABLE GEOMETRY FIDELITY (v1.14)
  For every transcribed table, compare the spans DECLARED in its TableSpec
  against the spans actually BUILT in the document:
    table_spec_spans(spec)  vs  table_spec_spans(read_table_spec(tbl))
  The built table is read BACK into a TableSpec and both sides are then measured
  by the SAME placement function, so this is a round-trip EQUALITY
  test, not an estimate, and it cannot false-positive on a legitimately blank
  cell — a blank cell is declared {'t': ''} and occupies exactly one grid
  position. WARN on any difference, naming the question.
  This is the check whose absence let a two-tier header ship flat under a
  green footer: CHECK 13 asserts only that a TABLE-classified image produced
  TRANSCRIBED CONTENT rather than a red box, and says nothing about shape.
  Requires table_specs {q_num: TableSpec} to be passed in. Skipped silently
  when it is not available (legacy flat path) — CHECK 17b then applies.

CHECK 17b — PADDING SIGNATURE (v1.14, advisory, legacy path only)
  When no TableSpec is available: WARN if a HEADER row contains TWO OR MORE
  trailing empty cells while the table declares NO spans anywhere. That is the
  padding signature and cannot arise from the S1-8a anchor-only model; it
  exists to catch legacy artefacts and third-party inputs.
  A SINGLE empty cell is NEVER flagged — a blank top-left corner is a
  legitimate and common table shape.

CHECK 18 — NO FUSED BLOCKS (v1.14)
  corpus_io.adjacent_table_pairs(doc) must be 0. Two adjacent block-level
  <w:tbl> siblings are FUSED into one table by every Word engine (S1-8b),
  and the fusion is INVISIBLE in the emitted file — python-docx reports N
  tables where Word shows one. WARN with the pair count.
  Cheap, no false positives, and it belongs in the shared validation layer:
  every step that inserts or copies a table inherits the hazard.

CHECK 19 — STRUCTURE RESIDUE IN PLAIN TEXT (v2.0)
  Scan every <w:t> run. HARD residue (WARN, marked HARD): region delimiters
  ⟦ ⟧, caret ^, subscript artefacts _x/_{/_( , √ before a non-digit.
  SOFT residue (WARN): probable letter fractions (x/2, π/4, dy/dx…) after
  masking is/are-style word pairs, unit ratios and dates. Any hit means an
  expression that should have been a ⟦MATH:⟧ region was left flat.

CHECK 20 — TIER-3 ROUND-TRIP + DEGRADE REPORT (v2.0)
  count_math_regions(buffer) must EQUAL _T3_STATS['compiled'], and no
  ⟦MATH: / ⟧ delimiter may survive in any <w:t> or <m:t>. Every degraded
  region (math_failed) is reported IN PLAIN WORDS: the affected text
  QUOTED VERBATIM (so Ctrl+F in Word lands on it — the document itself
  carries no colour or highlight), why it failed, and the remedy ("search
  for the quoted text, fix that ⟦MATH:⟧ spelling in the buffer, rebuild").
  ANY degraded region ⇒ deliver under an F1 AMBER footer that
  repeats the same plain-language remedy (Framework_DeliveryFooter §5) —
  the file still ships; nothing halts. Skipped silently when
  math_regions/math_compiled are not passed (legacy pipelines).

CHECK 21 — DECLARED-STRUCTURE FIDELITY (v2.0)
  For every q_num in struct_flags (S1-13 rule c): 'matrix' requires an
  <m:m> and 'cases' requires an <m:eqArr> somewhere in that question's
  paragraphs. This mechanically prevents the Q.37/Q.56 defect class — a
  source matrix or cases brace flattened or paraphrased into prose under a
  green footer. Skipped silently when struct_flags is not passed.

CHECK 22 — PRODUCER/CONSUMER Q-DETECTION AGREEMENT (v1.0, GAP-2026-08-15-BAREQ)
  THE check that cannot be satisfied by a blind spot shared between producer and
  consumer, because it compares two DIFFERENT VIEWS of the same document:
    - p.text            — the <w:t>-only view, which is what Steps 3 and 5 walk
    - corpus_io.text_of — the <w:t> + <m:t> view, i.e. what a reader actually sees
  For every paragraph, assert:
      (bc.detect_question_start(p.text) is not None)
      == (bc.detect_question_start(corpus_io.text_of(p)) is not None)
  and assert the two views yield the SAME Q-count and the SAME Q-numbers.
  A disagreement means a question exists in the visible document that the
  downstream parser cannot see (or the reverse). That is silent data loss, and it
  is the exact shape that cost IIT_JAM_MATHEMATICS 12-Feb-2017 four questions with
  all ten PYQSort checks passing.
  Also assert that no paragraph's Q-label is only reachable after zero-width
  stripping — if it is, S2-4 sanitise() did not run or ran on the wrong buffer.
  SEVERITY: WARN, consistent with §5's "warn on failure, deliver anyway" doctrine.
  The warning text MUST name GAP-2026-08-15-BAREQ, list every divergent Q-number,
  and state plainly that Step 3 will lose those questions — a warning that does
  not say what will be lost is not actionable.

```

### S5-2 — Validation implementation

```python
def validate_row_file(doc_path, date_label_text, source_trust=None, stated_total=None,
                      table_specs=None, math_regions=None, math_compiled=None,
                      math_failed=None, struct_flags=None):
    """
    Run all 22 validation checks. Return (pass_count, warn_count, messages).

    table_specs: {q_num: TableSpec} as transcribed in Phase B (S1-12 / S1-8a).
    Optional — when absent, CHECK 17 is skipped and CHECK 17b applies instead.
    math_regions / math_compiled: count_math_regions(buffer strings) and
    _T3_STATS['compiled'] (v2.0). Optional — when absent, CHECK 20 is skipped.
    math_failed: _T3_STATS['failed'] — [(region_body, reason), …] for every
    region delivered as unmarked plain text (graceful degradation) — CHECK 20
    quotes each one verbatim for Ctrl+F.
    struct_flags: {q_num: {'matrix','cases'}} declared per S1-13 rule (c).
    Optional — when absent, CHECK 21 is skipped.
    """
    from docx import Document
    import re
    import blueprint_core as bc   # ENGINE (routed) — THE Q-detector
    import corpus_io              # ENGINE (routed) — text_of(): <w:t> AND <m:t>

    doc = Document(doc_path)
    paras = doc.paragraphs
    warnings = []

    # ── GAP-2026-08-15-BAREQ (R-2). CHECK 1/2 used a PRIVATE regex r'^Q\.\d+' that
    # required no trailing content, while Steps 3 and 5 parsed with Q_PATTERNS, which
    # required whitespace AFTER the digits. On IIT_JAM_MATHEMATICS 12-Feb-2017 that
    # divergence is the whole defect: Step 1 certified "Q-count = 60, sequential OK"
    # on a file Step 3 could only read as 56, and delivered it green. A producer that
    # validates with a different detector than its consumer parses with is not
    # validating anything. Both checks now delegate to the engine — the SAME table,
    # the SAME zero-width normalisation, no second copy to drift.
    def _q(p):
        return bc.detect_question_start(p.text)

    # CHECK 1 — Q-count
    q_paras = [p for p in paras if _q(p) is not None]
    q_count = len(q_paras)
    print(f"CHECK 1: Q-count = {q_count}")

    # CHECK 2 — Sequential numbering
    q_nums = [_q(p) for p in paras if _q(p) is not None]
    expected = list(range(1, q_count + 1))
    if q_nums != expected:
        warnings.append(f"CHECK 2 WARN: Q-sequence not continuous. Got {q_nums[:5]}...{q_nums[-3:]}")
    else:
        print("CHECK 2: Sequential numbering OK")

    # CHECK 3 — Date label count
    date_re_any = re.compile(r'^\[\d{1,2}-[A-Za-z]{3}-\d{4}(\s+.+\s+\d+)?\]$')
    date_paras = [p for p in paras if date_re_any.match(p.text.strip())]
    if len(date_paras) != q_count:
        warnings.append(f"CHECK 3 WARN: Date labels={len(date_paras)} != Q-count={q_count}")
    else:
        print(f"CHECK 3: Date label count = {len(date_paras)} OK")

    # CHECK 4 — Date label format
    date_re_session = re.compile(r'^\[\d{1,2}-[A-Za-z]{3}-\d{4}\s+.+\s+\d+\]$')
    date_re_no_session = re.compile(r'^\[\d{1,2}-[A-Za-z]{3}-\d{4}\]$')
    bad_dates = 0
    for p in date_paras:
        t = p.text.strip()
        if not (date_re_session.match(t) or date_re_no_session.match(t)):
            bad_dates += 1
    if bad_dates:
        warnings.append(f"CHECK 4 WARN: {bad_dates} date labels with bad format")
    else:
        print("CHECK 4: Date label format OK")

    # CHECK 5 — Date label styling
    style_issues = 0
    for p in date_paras:
        if p.alignment != WD_ALIGN_PARAGRAPH.RIGHT:
            style_issues += 1
        for r in p.runs:
            if not r.bold:
                style_issues += 1
    if style_issues:
        warnings.append(f"CHECK 5 WARN: {style_issues} date label style issues")
    else:
        print("CHECK 5: Date label styling OK")

    # CHECK 6 — Metadata leakage
    META_RE = re.compile(
        r'(Question ID|Option \d ID|Status\s*:|Chosen Option|SubQuestion No|'
        r'Roll Number|Candidate Name|Venue Name|Exam Date|Exam Time|'
        r'Section\s*:)',
        re.IGNORECASE
    )
    leaked = 0
    for p in paras:
        t = p.text.strip()
        if META_RE.search(t):
            leaked += 1
        elif t == 'Comprehension:':
            leaked += 1
        elif re.match(r'^===.+===$', t):
            leaked += 1
    if leaked:
        warnings.append(f"CHECK 6 WARN: {leaked} paragraphs with leaked metadata")
    else:
        print("CHECK 6: No metadata leakage OK")

    # CHECK 7 — Control OR zero-width characters (v2.1, GAP-2026-08-15-BAREQ)
    CTRL_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\u200b-\u200d\u2060\ufeff]')
    ctrl_paras = [p for p in paras if CTRL_RE.search(p.text)]
    if ctrl_paras:
        _zw = [p.text.strip()[:24] for p in ctrl_paras
               if re.search(r'[\u200b-\u200d\u2060\ufeff]', p.text)]
        warnings.append(
            f"CHECK 7 WARN: {len(ctrl_paras)} paragraphs with control or zero-width "
            f"characters" + (f" — zero-width in: {_zw[:5]}" if _zw else ""))
    else:
        print("CHECK 7: No control or zero-width characters OK")

    # CHECK 8 — Answer markers
    ans_markers = sum(1 for p in paras if re.search(r'[✓✔✗✘]', p.text) or re.search(r'\bAns\b', p.text))
    if ans_markers:
        warnings.append(f"CHECK 8 WARN: {ans_markers} answer markers found")
    else:
        print("CHECK 8: No answer markers OK")

    # CHECK 9 — Option format (v2.0 — OMML-bearing bare labels are canonical)
    OMML_NS_V = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    opt_re = re.compile(r'^[1-5]\.\s+')
    opt_bare_re = re.compile(r'^[1-5]\.\s*$')
    bad_opts = 0
    for p in paras:
        t = p.text.strip()
        if p.paragraph_format.left_indent and p.paragraph_format.left_indent > 0:
            if not t:
                continue
            if opt_re.match(t):
                continue
            if opt_bare_re.match(t) and p._p.find(f'.//{{{OMML_NS_V}}}oMath') is not None:
                continue
            bad_opts += 1
    if bad_opts:
        warnings.append(f"CHECK 9 WARN: {bad_opts} non-canonical option lines")
    else:
        print("CHECK 9: Option format OK")

    # CHECK 10 — OMML structural integrity
    from lxml import etree
    omml_ns = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    body = doc.element.body
    broken = 0
    for tag in ('sSup', 'sSub'):
        for el in body.findall(f'.//{{{omml_ns}}}{tag}'):
            e = el.find(f'{{{omml_ns}}}e')
            s = el.find(f'{{{omml_ns}}}{"sup" if tag == "sSup" else "sub"}')
            if e is None or s is None:
                broken += 1
    # v2.0 — Tier-3 element classes
    for el in body.findall(f'.//{{{omml_ns}}}sSubSup'):
        if (el.find(f'{{{omml_ns}}}e') is None or el.find(f'{{{omml_ns}}}sub') is None
                or el.find(f'{{{omml_ns}}}sup') is None):
            broken += 1
    for el in body.findall(f'.//{{{omml_ns}}}f'):
        if el.find(f'{{{omml_ns}}}num') is None or el.find(f'{{{omml_ns}}}den') is None:
            broken += 1
    for tag in ('rad', 'nary', 'limLow'):
        for el in body.findall(f'.//{{{omml_ns}}}{tag}'):
            if el.find(f'{{{omml_ns}}}e') is None:
                broken += 1
    for el in body.findall(f'.//{{{omml_ns}}}m'):
        widths = {len(mr.findall(f'{{{omml_ns}}}e'))
                  for mr in el.findall(f'{{{omml_ns}}}mr')}
        if len(widths) != 1:
            broken += 1
    if broken:
        warnings.append(f"CHECK 10 WARN: {broken} broken OMML elements")
    else:
        print("CHECK 10: OMML integrity OK")

    # CHECK 11 — Residual math markers (v1.3)
    residual_count = 0
    for p in paras:
        t = p.text
        if 'SQRT:' in t or '⟦' in t or '⟧' in t:
            residual_count += 1
        for mt in p._element.iter(f'{{{omml_ns}}}t'):
            if mt.text and ('SQRT' in mt.text or '⟦' in mt.text or '√' in mt.text):
                residual_count += 1
    if residual_count:
        warnings.append(f"CHECK 11 WARN: {residual_count} residual math markers found")
    else:
        print("CHECK 11: No residual math markers")

    # CHECK 12 — Semantic underline validation (v1.5)
    underline_issues = 0
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    for p in paras:
        t = p.text.strip()
        # Check for unprocessed {{u}} markers
        if '{{u}}' in t or '{{/u}}' in t:
            underline_issues += 1
        # Check: stem says "underlined" but no underline formatting exists
        if bc.detect_question_start(t) is not None and 'underlined' in t.lower():
            has_underline = any(
                r.underline for r in p.runs if r.underline
            )
            if not has_underline:
                underline_issues += 1
    if underline_issues:
        warnings.append(f"CHECK 12 WARN: {underline_issues} underline issues")
    else:
        print("CHECK 12: Underline validation OK")

    # CHECK 13 — Image classification verification (v1.6)
    # Cross-reference IMAGE_CLASSIFICATIONS against output.
    # This check uses the image_classifications dict passed to the
    # pipeline (or reconstructed from the build log).
    # Detect: figure-only stems (Q.N with no text, followed by image)
    # that should have been transcribed.
    placeholder_issues = 0
    figure_only_qnums = []
    omml_only_qnums   = []   # GAP-2026-08-15-BAREQ (G-5)
    bare_empty_qnums  = []   # S1-4 "empty/corrupt" — no stem, no image, no equation
    for idx, p in enumerate(paras):
        t = p.text.strip()
        # Detect bare-label stems: the paragraph is nothing but "Q.N".
        # GAP-2026-08-15-BAREQ (G-5). This check already had the RIGHT regex and
        # gated it on the WRONG payload test: it looked only at the NEXT paragraph
        # for <w:drawing>/<w:pict> and never at the SAME paragraph for <m:oMath>.
        # An OMML-only stem — the discovery shape, and the shape v2.0's M1/M2
        # transcription rules make COMMON — was therefore silent here while being
        # invisible to Step 3. Both payload positions are now inspected.
        qnum = bc.is_bare_q_label(t)   # ENGINE predicate — no private copy (R-6)
        if qnum is not None:
            own    = p._element.xml
            nxt    = paras[idx + 1]._element.xml if idx + 1 < len(paras) else ''
            if '<m:oMath' in own:
                omml_only_qnums.append(qnum)
            elif ('<w:drawing' in own or '<w:pict' in own
                  or '<w:drawing' in nxt or '<w:pict' in nxt):
                figure_only_qnums.append(qnum)
            else:
                bare_empty_qnums.append(qnum)
    # Report figure-only stems for manual verification against
    # IMAGE_CLASSIFICATIONS. In automated mode, cross-check with
    # the classifications dict. In validation-only mode, report count.
    if figure_only_qnums:
        print(f"CHECK 13: {len(figure_only_qnums)} figure-only stems "
              f"detected: Q.{figure_only_qnums}. Verify these are all "
              f"VISUAL-IMAGE classified (not MATH/TABLE/TEXT).")
    if omml_only_qnums:
        print(f"CHECK 13: {len(omml_only_qnums)} OMML-only stems detected: "
              f"Q.{omml_only_qnums}. This is a LAWFUL normalised form (S1-4) and "
              f"needs NO repair — do NOT inject filler text. Q_PATTERNS entries 3/4 "
              f"read it and CHECK 22 proves Step 3 will see it.")
    if bare_empty_qnums:
        print(f"CHECK 13: {len(bare_empty_qnums)} bare Q.N stems with no stem, no "
              f"image and no equation: Q.{bare_empty_qnums}. These are S1-4 "
              f"empty/corrupt carriers — confirm against the source that content "
              f"was genuinely absent rather than lost in transcription.")
    if not (figure_only_qnums or omml_only_qnums or bare_empty_qnums):
        print("CHECK 13: No figure-only stems — all content transcribed OK")

    # CHECK 14 — Vision provenance consistency (v1.7)
    import os as _os
    cat = (doc.core_properties.category or '')
    has_prop = 'PYQPrepare-Source-Trust:' in cat
    has_suffix = _os.path.basename(doc_path).endswith('__vision-unverified.docx')
    if has_prop != has_suffix:
        warnings.append(
            f"CHECK 14 WARN: half-marked vision file "
            f"(property={has_prop}, filename_suffix={has_suffix}) — both or neither")
    else:
        print(f"CHECK 14: Vision provenance consistent (marked={has_prop})")

    # CHECK 15 — Specimen / out-of-range exclusion (v1.7)
    SPECIMEN_RE = re.compile(
        r'(sample\s+question|specimen|\u0928\u092e\u0941\u0928\u093e)', re.IGNORECASE)
    specimen_hits = 0
    for p in paras:
        t = p.text.strip()
        if bc.detect_question_start(t) is not None and SPECIMEN_RE.search(t):
            specimen_hits += 1
    out_of_range = sum(1 for qn in q_nums if qn > q_count)
    if specimen_hits or out_of_range:
        warnings.append(
            f"CHECK 15 WARN: {specimen_hits} specimen-marked stems, "
            f"{out_of_range} out-of-range Q-numbers (possible specimen leak)")
    else:
        print("CHECK 15: No specimen / out-of-range questions OK")

    # CHECK 16 — Q-count vs stated-total reconciliation (v1.7)
    if stated_total is not None:
        try:
            st = int(stated_total)
            if st != q_count:
                warnings.append(
                    f"CHECK 16 WARN: built Q-count={q_count} != cover stated total={st}")
            else:
                print(f"CHECK 16: Q-count matches stated total ({st}) OK")
        except (TypeError, ValueError):
            print("CHECK 16: stated_total not numeric — skipped")
    else:
        print("CHECK 16: stated_total not provided — skipped")

    # CHECK 17 — table geometry fidelity (v1.14)
    import corpus_io
    di_tables = [t for t in doc.tables if len(t.columns) > 2]
    if table_specs:
        for (qn_, spec), tbl in zip(sorted(table_specs.items()), di_tables):
            want = corpus_io.table_spec_spans(spec)
            got = corpus_io.table_spec_spans(corpus_io.read_table_spec(tbl._tbl))
            if want != got:
                warnings.append(
                    f"CHECK 17 WARN: Q.{qn_} table spans differ — "
                    f"declared {want}, built {got}")
        if not any(w.startswith('CHECK 17 WARN') for w in warnings):
            print(f"CHECK 17: {len(di_tables)} table(s), geometry matches transcription OK")
    else:
        print("CHECK 17: no table_specs supplied — skipped (CHECK 17b applies)")

    # CHECK 17b — padding signature (advisory, legacy path only)
    pad_hits = 0
    if not table_specs:
        for tbl in di_tables:
            x = tbl._tbl.xml
            if 'w:gridSpan' in x or 'w:vMerge' in x:
                continue
            head = [c.text.strip() for c in tbl.rows[0].cells]
            trailing = 0
            for cell_text in reversed(head):
                if cell_text:
                    break
                trailing += 1
            if len(head) > 2 and trailing >= 2:
                pad_hits += 1
    if pad_hits:
        warnings.append(
            f"CHECK 17b WARN: {pad_hits} table(s) show the padding signature "
            f"(>=2 trailing empty header cells, no spans) — a merged header was "
            f"probably squared into a grid (S1-8a)")
    else:
        print("CHECK 17b: No padding signature OK")

    # CHECK 18 — no fused blocks (v1.14)
    pairs = corpus_io.adjacent_table_pairs(doc)
    if pairs:
        warnings.append(
            f"CHECK 18 WARN: {pairs} pair(s) of adjacent block tables — Word will "
            f"fuse them into one table (S1-8b RULE B1)")
    else:
        print("CHECK 18: No adjacent block tables OK")

    # CHECK 19 — Structure residue in plain text (v2.0)
    W_NS_V = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    _WL_RE = re.compile(
        r'\b(?:is/are|and/or|has/have|have/has|he/she|s/he|yes/no'
        r'|c/o|w/o|24/7|I/O|a/c)\b', re.IGNORECASE)
    hard_res = soft_res = 0
    _degraded_bodies = {body for body, _ in (math_failed or [])}
    for p in paras:
        for wt in p._element.iter(f'{{{W_NS_V}}}t'):
            if (wt.text or '') in _degraded_bodies:
                continue    # degraded region — already reported by CHECK 20
            s = wt.text or ''
            if ('⟦' in s or '⟧' in s or '^' in s
                    or re.search(r'_[A-Za-z{(]', s)
                    or re.search(r'√(?![0-9])', s) or s.endswith('√')):
                hard_res += 1
            masked = _WL_RE.sub(' ', s)
            masked = _UNIT_RATIO_RE.sub(' ', masked)
            masked = _DATE_RE.sub(' ', masked)
            if (re.search(r'[A-Za-zπθφ)\]!²³ⁿᵏ]\s*/', masked)
                    or re.search(r'/\s*[A-Za-z(π√]', masked)):
                soft_res += 1
    if hard_res:
        warnings.append(f"CHECK 19 WARN (HARD): {hard_res} structural artefacts "
                        f"in plain text — should be ⟦MATH:⟧ regions")
    if soft_res:
        warnings.append(f"CHECK 19 WARN: {soft_res} probable letter-fractions left linear")
    if not hard_res and not soft_res:
        print("CHECK 19: No structure residue in plain text OK")

    # CHECK 20 — Tier-3 round-trip (v2.0)
    if math_regions is None or math_compiled is None:
        print("CHECK 20: math region counts not supplied — skipped (legacy path)")
    else:
        delim_res = 0
        for p in paras:
            for node in p._element.iter():
                if node.tag in (f'{{{W_NS_V}}}t', f'{{{omml_ns}}}t'):
                    if node.text and ('⟦MATH:' in node.text or '⟧' in node.text):
                        delim_res += 1
        for body, reason in (math_failed or []):
            snippet = body if len(body) <= 60 else body[:57] + '…'
            warnings.append(
                "CHECK 20 WARN: one maths expression could not be structured and "
                f"was delivered as plain text: \"{snippet}\" "
                f"(reason: {reason}). Remedy: in Word press Ctrl+F, search for "
                "the quoted text to locate it, fix that ⟦MATH:⟧ spelling in the "
                "buffer, rebuild. Deliver under an F1 AMBER footer.")
        n_failed = len(math_failed or [])
        ledger_ok = (math_regions == math_compiled + n_failed)
        if not ledger_ok:
            warnings.append(
                f"CHECK 20 WARN: region ledger mismatch — {math_regions} in buffer "
                f"vs {math_compiled} compiled + {n_failed} degraded (a stray "
                f"unpaired ⟧ can cause this; see the quoted text above)")
        elif delim_res:
            warnings.append(f"CHECK 20 WARN: {delim_res} residual region delimiters")
        elif not n_failed:
            print(f"CHECK 20: Tier-3 round-trip {math_compiled}/{math_regions} regions OK")

    # CHECK 21 — Declared-structure fidelity (v2.0)
    if not struct_flags:
        print("CHECK 21: no struct_flags supplied — skipped")
    else:
        need_tag = {'matrix': f'{{{omml_ns}}}m', 'cases': f'{{{omml_ns}}}eqArr'}
        cur_q = None
        q_spans = {}
        for p in paras:
            _n = bc.detect_question_start(p.text)   # R-2: engine detector, not a copy
            if _n is not None:
                cur_q = _n
                q_spans[cur_q] = []
            if cur_q:
                q_spans[cur_q].append(p)
        missing = []
        for q_num, kinds in struct_flags.items():
            for kind in kinds:
                found = any(p._element.find(f'.//{need_tag[kind]}') is not None
                            for p in q_spans.get(q_num, []))
                if not found:
                    missing.append(f"Q.{q_num}:{kind}")
        if missing:
            warnings.append("CHECK 21 WARN: declared structures missing — "
                            + ", ".join(missing))
        else:
            print(f"CHECK 21: Declared structures present ({len(struct_flags)} questions) OK")

    # CHECK 22 — Producer/consumer Q-detection agreement (v1.0, GAP-2026-08-15-BAREQ)
    #
    # Every other check in this file reads the document ONE way. This one reads it TWO
    # ways and compares them, which is the only construction a shared blind spot cannot
    # satisfy. p.text is <w:t>-only — exactly what Steps 3 and 5 walk. corpus_io.text_of()
    # concatenates <w:t> AND <m:t> — what a human reading the page actually sees. If a
    # paragraph opens a question in one view and not the other, a question that exists on
    # the page does not exist for the parser, and it will be absorbed into the preceding
    # question's body with every count still reconciling. That is what happened to
    # IIT_JAM_MATHEMATICS 12-Feb-2017 Q.4/Q.6/Q.25/Q.27.
    #
    # It also catches the INVERSE — a paragraph the visible text makes look like a
    # question start when the text layer does not — and the zero-width route (R-8), where
    # the label parses only after the ZW class is stripped.
    wt_nums, vis_nums, divergent, zw_only = [], [], [], []
    for p in paras:
        _wt  = p.text or ''
        _vis = corpus_io.text_of(p)
        a = bc.detect_question_start(_wt)
        b = bc.detect_question_start(_vis)
        if a is not None:  wt_nums.append(a)
        if b is not None:  vis_nums.append(b)
        if (a is None) != (b is None):
            divergent.append({'q': a if a is not None else b,
                              'seen_by_step3': a is not None,
                              'text': repr(_wt.strip()[:40])})
        # zero-width route: the label is only reachable after stripping the ZW class
        if a is not None and re.search(r'[\u200b-\u200d\u2060\ufeff]', _wt):
            zw_only.append(a)

    if divergent:
        _lost = [d['q'] for d in divergent if not d['seen_by_step3']]
        _ghost = [d['q'] for d in divergent if d['seen_by_step3']]
        _msg = ("CHECK 22 WARN: GAP-2026-08-15-BAREQ — the <w:t> view and the "
                "<w:t>+<m:t> view of this file DISAGREE about which paragraphs open a "
                "question. ")
        if _lost:
            _msg += (f"Step 3 (PYQSort) and Step 5 (PYQExtract) WILL LOSE Q.{_lost} — "
                     f"each stem, its options and its date label will be absorbed into "
                     f"the body of the preceding question, and every PYQSort check will "
                     f"still pass because input and output are counted with the same "
                     f"detector. ")
        if _ghost:
            _msg += (f"Q.{_ghost} open a question in the text layer but not in the "
                     f"visible text — investigate before delivering. ")
        _msg += ("Do NOT repair by injecting filler text into the stem (S1-4). Verify "
                 "the framework carrying this file is >= 2026.08.15.5.")
        warnings.append(_msg)
    elif zw_only:
        warnings.append(
            f"CHECK 22 WARN: Q.{sorted(set(zw_only))} carry zero-width characters in the "
            f"Q-label. They parse only because the engine strips them defensively — S2-4 "
            f"sanitise() should have removed them at the producer (GAP-2026-08-15-BAREQ "
            f"R-8). Re-run S2-4 over the buffers.")
    else:
        print(f"CHECK 22: Producer/consumer Q-detection agrees "
              f"({len(wt_nums)} questions, both views) OK")

    # Summary
    pass_count = 22 - len(warnings)
    for w in warnings:
        print(f"  ⚠️ {w}")
    print(f"\n{'✅' if not warnings else '⚠️'} {pass_count}/22 checks passed, {len(warnings)} warnings")

    return pass_count, len(warnings), warnings
```

---

## §6 — OUTPUT FILENAME

```
WITH session:
  [ExamCode]_DD-Mon-YYYY_<session_keyword>-<N>.docx

WITHOUT session:
  [ExamCode]_DD-Mon-YYYY.docx

Examples:
  SSC_CGL_T1_18-Jan-2025_Shift-1.docx
  GATE_CS_09-Feb-2025_Session-1.docx
  UPSC_CSE_02-Jun-2024.docx

ExamCode, date, and session all come from the trigger text.

VISION-TRANSCRIBED (FORMAT C1 / C-HYBRID — v1.7):
  Append "__vision-unverified" before ".docx":
    [ExamCode]_DD-Mon-YYYY[_session]__vision-unverified.docx
  This is the human-visible half of the S1-13 provenance marker (the
  machine-readable half is core_properties.category). Only C1/C-HYBRID
  outputs carry the suffix; all other formats are unchanged.
```

---

## §7 — DELIVERY

```
1. Save completed Row file to /mnt/user-data/outputs/ with exact filename.
2. Run validation (§5). Log all check results.
3. Deliver via present_files — even if warnings exist.
4. Render delivery footer per Framework_DeliveryFooter.md.

Footer type: F2 (step-complete) — Step 1 has no batches.
File badge: "Use locally" — Row files go to Google Drive PYQ folder
            or are uploaded to project Files by the user manually.
Next step: "Step 2a: PYQDraft — provide Exam Syllabus + Exam Pattern
            to build taxonomy and exam_config.json"

VISION PROBE PROVENANCE (v1.9 — MANDATORY whenever the source had images):
  The delivery message MUST state the S1-12 probe result and the placeholder
  count together:
    "Vision probe: PASS. N image(s) classified — M red placeholder(s)
     (VISUAL-IMAGE), K transcribed as math/table/text."
  A placeholder is a permanent, downstream-visible decision: the graphics team
  draws a figure for it, and the question is FIGURAL from then on. Recording the
  probe alongside the count makes that decision auditable after the fact —
  without it, a placeholder assigned by a blind session is indistinguishable
  from one that was genuinely earned.
  v1.11: a Row file IS delivered when some cells were unobserved — with those
  images LEFT UNTOUCHED, never placeholdered, the count stated, and the footer
  rendered F1 amber. Delivering the file is safe; placeholdering is what is not.
  Recording per-image observation state alongside the count is what keeps that
  distinction auditable after the fact (S1-12).

FORMAT C1 / C-HYBRID (v1.7 — vision-transcribed):
  Deliver the Row file (still EXACTLY 1 file, closed set) with the
  __vision-unverified suffix. The delivery message MUST carry a prominent
  "VISION-TRANSCRIBED — human verification required" note listing any
  low-confidence Q-numbers. Large scans that were batched use the F1 amber
  "continue" footer per batch and F2 on the final batch. The S5
  warn-and-deliver contract is unchanged.

DELIVERABLE SET CONTRACT (CLOSED):
  present_files MUST contain EXACTLY 1 file:
    /mnt/user-data/outputs/[ExamCode]_DD-Mon-YYYY[_session].docx
  and NOTHING ELSE.

  DO NOT include in present_files:
    ✗ pipeline.py or any Python script
    ✗ placeholder_red.png
    ✗ Any extracted images, text files, or intermediates
    ✗ The source exam paper
    ✗ Any answer key file
```

---

## §8 — EDGE CASES

```
EC-P1: QUESTIONS SPLIT ACROSS PAGES
  Source text may split a question across page boundaries.
  Resolution: concatenate all source text/pages into one buffer BEFORE
  parsing. Never parse page-by-page independently.

EC-P2: BLANK PAGES / INSTRUCTION PAGES
  Source may contain cover pages, instruction pages, or blank pages with
  no questions. Skip silently — never treat as a question.

EC-P3: METADATA RUN-ON
  "Chosen Option : -- Q.4 Find the..." — metadata runs into next question
  with no line break. Cut at metadata pattern boundary, treat subsequent
  Q.\d+ as new question start.

EC-P4: FIGURE-ONLY STEMS
  Q.N followed immediately by options with no stem text between.
  PREREQUISITE (v1.6): before assigning a red placeholder, check
  IMAGE_CLASSIFICATIONS for this question's image. If classified as
  MATH/TABLE/TEXT → transcribe, not placeholder. Only VISUAL → placeholder.
  Render (VISUAL): Q.N paragraph (bold) + red placeholder image.
  Render (MATH/TEXT): Q.N paragraph (bold) + transcribed stem text.
  Render (TABLE): Q.N paragraph (bold) + native Word table.
  Never leave stem empty without EITHER a placeholder OR transcription.

EC-P5: FIGURE OPTIONS
  Any option line is blank after its label number → ALL options get
  red placeholder tables. Keep text stem above placeholders.

EC-P6: OCR CONTROL CHARACTER CORRUPTION
  OCR may inject \x02 or other C0 bytes into words. Apply sanitise()
  to every extracted string. Do NOT invent hyphens — just delete the
  control byte (e.g. "problem\x02solving" → "problemsolving").

EC-P7: MULTI-STATEMENT STEMS
  Assertion-reason, statement I/II, cause-effect blocks: merge into
  single bold paragraph with \n line breaks. Preserve all labelled lines.

EC-P8: PASSAGE REPETITION + Q.N-FIRST
  All passage-dependent sub-questions must have the passage repeated
  for each sub-question in output — with Q.N-FIRST layout (S1-9 RULE 2).
  If source shows passage once with multiple sub-questions, replicate
  passage for each sub-question. Regardless of source ordering, output
  always places Q.N stem BEFORE instruction line and passage body.

EC-P9: PER-MODULE Q-NUMBER RESTART
  Source has Math Q.1-30, Reasoning Q.1-30, etc. Step 1 merges and
  renumbers continuously: Q.1-Q.60. No section info preserved in output.

EC-P10: TYPOGRAPHIC UNICODE
  Curly quotes " " ' ', em dashes —, en dashes –, rupee sign ₹, and
  all special Unicode symbols: preserve verbatim. NEVER normalise to
  straight quotes or ASCII hyphens.

EC-P11: NAT QUESTIONS (NO OPTIONS)
  Some exams (GATE, banking) have Numerical Answer Type questions with
  zero selectable options — only a stem, possibly with an answer-entry
  instruction. These are valid questions. Render: date label → Q.N stem
  → blank line. No options block.

EC-P12: MSQ QUESTIONS (MULTIPLE SELECT)
  Multiple-correct questions have standard options. Render identically
  to MCQ. The multiple-select marking is a downstream concern (Step 7).

EC-P13: BILINGUAL PAPERS
  Some exams provide Hindi+English bilingual papers. Extract ENGLISH
  version only. Skip Hindi/other language content.

EC-P14: DI TABLES
  Data interpretation tables → native Word tables. Never render as
  images or placeholders. Preserve source data exactly — and, from v1.14,
  preserve source STRUCTURE exactly: merged header and body cells are
  reproduced as merged cells (S1-8, S1-8a). "Preserve source data exactly"
  governs VALUES; for thirteen versions it was silently read as covering
  geometry too, which is how a grouped header shipped flat with four stray
  empty cells and every value correct. See EC-P24.

EC-P15: EMPTY/CORRUPT QUESTIONS
  If a question has no stem text AND no image (completely empty), include
  it as Q.N with no content. Let downstream steps handle it.

EC-P16: THIRD-PARTY BRANDING
  Strip ALL coaching brand watermarks, logos, promotional text, URLs,
  and social media handles. These are never part of the question content.

EC-P17: ANSWER/EXPLANATION STRIPPING
  Strip ALL answer markers (✓/✗), correct answer indicators, explanations,
  solutions, and hints. The Row file contains ONLY questions and options.
  Answer keys are completely discarded — not preserved in any form.

EC-P18: SINGLE-SESSION EXAMS
  GATE, UPSC, state PSC exams typically have one session per date.
  If session is not provided in trigger, date label omits session entirely:
  [DD-Mon-YYYY]. No default session=1 is added.

EC-P19: UNDERLINE PRESERVATION (v1.5)
  Vocabulary, error detection, and sentence improvement questions
  reference "the underlined word/part/phrase." The underline MUST be
  preserved in the output or the question is nonsensical.
  During extraction, wrap underlined text in {{u}}...{{/u}} markers.
  render_text_with_math() processes these into Word underline runs.
  If the extraction tool cannot detect underlines (e.g. pdftotext),
  try alternative tools (pdfplumber, PyMuPDF). If detection fails
  entirely, WARN in the delivery message so the team can manually
  add underlines. CHECK 12 validates: if stem says "underlined" but
  no underline formatting exists → WARN.

EC-P20: MATH-AS-IMAGE (v1.6)
  Source renders math content as embedded images (common in coaching
  platform exports, response sheet docx files). Eight sub-scenarios:

  EC-P20a: FULL STEM AS MATH IMAGE
    Entire question stem is an image containing a math expression.
    No extractable text. Claude views → MATH-IMAGE → transcribe.
    Example: Q.6 image shows "If x²+1/x² = 7, find x⁴+1/x⁴"
    Pipeline writes: add_stem(doc, 6, "If x²+1/x² = 7, find x⁴+1/x⁴")
    with OMML rendering for fractions/superscripts.

  EC-P20b: FULL STEM AS TABLE IMAGE
    Question stem is an image of a data table.
    Claude views → TABLE-IMAGE → transcribe into a TableSpec, SPANS INCLUDED
    (S1-8a). Pipeline writes: add_stem(doc, N, ""), then build_di_table().
    If the image also carries the intro sentence and/or the question sentence
    (common in response-sheet exports), the intro becomes the Q.N stem, the
    table follows, and the question sentence follows the table as a plain
    paragraph — Q.N-FIRST is unaffected.

  EC-P20c: OPTIONS AS MATH IMAGES
    Option lines are blank (image-only) but images contain math text.
    Claude views each option image → MATH-IMAGE → transcribe.
    Pipeline writes: add_option(doc, 1, "7/12") with OMML.
    Note: if ALL options are math-images, transcribe ALL. If some are
    math and some are visual → this is unusual; transcribe the math
    options and placeholder the visual ones. BUT if any option is
    genuinely visual, apply the ALL-or-NONE rule from S1-7 for that
    specific set.

  EC-P20d: STEM HAS TEXT + IMAGE IS SUPPLEMENTARY MATH
    Stem has extractable text but the image adds math content not in
    the text (e.g., a formula referenced by the stem text).
    Claude views → MATH-IMAGE → transcribe.
    Pipeline appends transcribed math to the existing stem text.

  EC-P20e: STEM HAS TEXT + IMAGE IS SUPPLEMENTARY VISUAL
    Stem has extractable text and the image is a genuine figure.
    Claude views → VISUAL-IMAGE → red placeholder after stem text.
    This is the standard text+figure case (no change from v1.5).

  EC-P20f: IMAGE CONTAINS BOTH MATH AND VISUAL
    A single image has both mathematical notation AND a geometric
    figure (e.g., a triangle with angle expressions inside it).
    Classification: VISUAL-IMAGE (the visual content cannot be
    transcribed as text). Claude transcribes any math/labels that
    are present in the image as supplementary text BEFORE the
    red-box substitute. Example: "In triangle PQR, ∠P = 60°, PQ = 5 cm"
    followed by red box for the figure.

  EC-P20g: UNREADABLE IMAGE
    Image is corrupt, blank, very low resolution, or rendered in a
    format Claude cannot parse visually. Classification: VISUAL-IMAGE
    + explicit WARN in delivery message listing the affected Q-numbers.
    "Q.N: image unreadable — red box used, manual review needed."

  EC-P20h: MIXED QUESTION SET (SOME OMML, SOME IMAGE)
    Same paper has some questions with OMML math (text-extractable)
    and others with math as images. Both paths coexist in the same
    pipeline run. OMML math → Tier 1/2 rendering. Image math →
    S1-12 inspection + transcription. No conflict.

EC-P21: SCANNED-SOURCE SPECIMEN / SAMPLE QUESTION (v1.7)
  Scanned papers frequently print a DEMONSTRATION question on an
  instruction page — a "sample question" shown only to explain how to
  mark the answer sheet, carrying an OUT-OF-RANGE number (e.g. "Q.201",
  नमुना प्रश्न). It is NOT part of the real Q.1..N set and MUST be
  excluded. During S1-13 page classification (step 3) the SAMPLE/SPECIMEN
  page is skipped entirely. CHECK 15 verifies no specimen marker or
  out-of-range Q-number leaked into the Row file. Also applies to text
  sources: a specimen block on an instruction page is dropped like any
  other instruction chrome (EC-P2).

EC-P22: VISION UNAVAILABLE DURING IMAGE INSPECTION (v1.9)
  The S1-12 liveness probe fails: Claude cannot read back the token from a
  freshly generated control image. This is a property of the SESSION, not of
  any source image, and it can appear mid-run as context grows.
  Resolution: record vision_unavailable, assign NO placeholders, HALT with the
  extracted images preserved, and ask for a fresh session.
  What makes this a named edge case rather than a footnote: without the probe
  the failure is INVISIBLE. Every image reads as unreadable, every one takes
  the "genuinely unreadable" branch, and the run completes successfully with a
  Row file full of red placeholders where the math used to be. It looks like a
  bad source. It is not. This is the SSC CGL T2 18-Jan-2025 failure recorded in
  the v1.6 changelog — eleven math questions, ~35% of the Quant section.
  Do NOT "work around" an unobserved cell by classifying from filenames, from
  surrounding text, or from the extraction order. A classification is a claim
  about image content and there is no evidence for it. Leave the image in place
  and report it; that costs one re-run of Phase B, whereas a wrong placeholder
  costs the question permanently.

EC-P23: IMAGE INSIDE A TABLE CELL (v1.9)
  The source lays a figure out inside a table — the normal arrangement for
  match-the-following items, multi-panel figures and option grids.
  Before v1.9 the local extract_images() walked doc.paragraphs, which in
  python-docx does NOT descend into table cells, so the image was never
  extracted, never viewed and never classified. It did not even reach the
  "unclassified image" HARD BUG, because that branch fires on an image the
  pipeline KNOWS about. Proven: 2 images present, 1 found.
  Resolution: discovery is delegated to corpus_io.map_images_to_questions,
  which walks doc.element.body.iter() and descends into tables, and to
  corpus_io.extract_images, which reads the package directly.
  Cross-check the count against corpus_io.count_image_refs — a mapping that
  is short by one is an image that will be silently placeholdered.

EC-P24: MERGED / GROUPED TABLE STRUCTURE (v1.14)
  The source table has cells that span columns or rows — the NORM for DI sets
  in SSC, banking and railway papers. Eight sub-scenarios:

  EC-P24a: HEADER CELL SPANNING N COLUMNS ("Printers" over L/M/N/O)
    -> ONE Cell with 'cs': N. Not N cells, and never N-1 padded blanks.

  EC-P24b: LABEL CELL SPANNING N ROWS ("Days" beside a two-tier header)
    -> ONE Cell with 'rs': N in the row where it STARTS. The covered rows do
       not declare it.

  EC-P24c: BOTH IN ONE TABLE (the reported case)
    -> both, independently. Row 0 declares two cells; row 1 declares four.

  EC-P24d: THREE-OR-MORE-TIER HEADER
    -> full nesting; header_rows = number of tiers.

  EC-P24e: MERGE IN THE BODY (a category label spanning several data rows)
    -> identical treatment; 'rs' is not a header-only property.

  EC-P24f: GENUINELY BLANK CELL vs PADDING
    -> a blank cell is {'t': ''} and occupies one grid position. Padding cannot
       be expressed at all (S1-8a anchor-only rule), so the two can never be
       confused. A blank TOP-LEFT CORNER is legitimate and common and is NEVER
       flagged by CHECK 17b.

  EC-P24g: RAGGED OR OVERLAPPING DECLARATION
    -> place_cells() reports 'hole at (r,c)' or 'overlapping span at (r,c)' and
       build_di_table raises. FIX THE TRANSCRIPTION. Never auto-pad: auto-padding
       is the original defect wearing a different hat.

  EC-P24h: UNREPRESENTABLE STRUCTURE (diagonal split corner, nested table,
    rotated header, meaning carried by shading alone)
    -> transcribe the closest faithful structure, set spec['note'] or record a
       transcription warning naming the question, and surface it in the delivery
       report. NEVER normalise silently (S1-8a).

EC-P25: ADJACENT BLOCK TABLES (v1.14)
  A question emits two or more block-level tables with nothing between them —
  a figure-option set built one-table-per-option, or two DI tables in one
  question. Every Word engine FUSES adjacent w:tbl siblings into a single
  table, and the emitted file gives no sign of it: python-docx counts N, Word
  shows one. Measured: 19 tables written, 7 after a Word-engine round-trip.
  Resolution: S1-8b — one table for an option SET (B2), or a separator
  paragraph (B3). CHECK 18 enforces it. Because the defect is only observable
  through a rendering engine, a round-trip belongs in CI; static inspection of
  the .docx will never see it.
```

---

## §9 — EXECUTION WALKTHROUGH

```
Complete execution flow for a typical Step 1 run:

USER provides:
  Trigger: "Step 1: PYQPrepare SSC_CGL_T1 [18-Jan-2025 Shift 1]"
  Attachment: 18-Jan-2025-Paper-I-EN.pdf

PHASE A — INSPECT (1–3 tool calls):

  CALL A1: Determine file type
    bash_tool: file /mnt/user-data/uploads/18-Jan-2025-Paper-I-EN.pdf
    → "PDF document" or "Zip archive" or ...

  CALL A2: Extract sample content + check for embedded images
    bash_tool: pdftotext /mnt/user-data/uploads/18-Jan-2025-Paper-I-EN.pdf - | head -300
    → Reveals question format, option format, metadata vocabulary, sections
    Also: detect embedded images (drawings, blips) and their count.
    For DOCX: count paragraphs with <w:drawing> elements.
    For PDF: check page.get_images() via PyMuPDF.

  CALL A3 (if images detected): Extract all embedded images
    bash_tool: python3 -c "... extract_source_images() from S1-12 ..."
    → corpus_io.extract_images + corpus_io.map_images_to_questions
    → Saves every media part (including images inside TABLE CELLS, which the
      pre-v1.9 doc.paragraphs walk could not see) and maps each to its Q-number.
    → Cross-check the mapping total against corpus_io.count_image_refs.

  CALL A3b (v1.11, MANDATORY before any classification): PHASE A + PHASE B
    bash_tool: queue = corpus_io.build_vision_queue(items, VISION_WORKDIR, fresh=True)
      # VISION_WORKDIR = '/home/claude/pyq_vision_prep' — Step 1's own, NOT Step 5's
      # (v1.13; fresh=True needs corpus_io >= v1.10 — per-run scope, see S1-12)
      where items = [{'paper_id','q_num','srcs':[extracted image paths]}, ...]
    THEN, IN THIS TURN (PHASE B — prose protocol, S1-12; never a python call):
      view(<VISION_WORKDIR>/<sheet>) for each sheet in queue['sheets']
      record ONE observation per labelled cell, then
      corpus_io.write_vision_observations(VISION_WORKDIR, observations)
    bash_tool: bc.merge_vision_observations(queue['items'], observations)  (PHASE C)
    → OBSERVED cells: classify exactly as v1.6 specified.
    → UNOBSERVED cells: leave the image untouched, assign NO placeholder, complete
      the run, state the count, render F1 amber. NO HALT.
    The separate token probe is GONE (corpus_io v1.8): Phase B looks at the REAL
    figures, so liveness arrives free — any observation returned proves vision works.
    Skipping Phase B is how eleven math questions became red placeholders in the
    SSC CGL T2 18-Jan-2025 incident (v1.6 changelog); the difference now is that
    skipping it is VISIBLE (amber footer + stated count) rather than silent.

PHASE A-IMAGE — IMAGE CLASSIFICATION (1–8 view calls, v1.6):
  Only when embedded images exist. Claude views each extracted image
  and classifies per S1-12 (MATH / TABLE / TEXT / VISUAL).

  CALL A-IMG-1: view /home/claude/work/images/img_000.png
    → Q.6 image: MATH expression "If the ratio..." → transcribe
  CALL A-IMG-2: view /home/claude/work/images/img_001.png
    → Q.14 image: frequency table → transcribe as TABLE
  ...
  CALL A-IMG-N: view /home/claude/work/images/img_NNN.png
    → Q.33 image: geometric figure → VISUAL (placeholder)

  After all images classified, build IMAGE_CLASSIFICATIONS dict.

  MENTAL PLANNING (no tool call):
    - Source has 100 questions across 4 sections (Math, GI, English, GK)
    - Options use "1. text" format in source
    - Has figure-only stems in Reasoning section
    - Has comprehension passages in English section
    - Math fractions need OMML: Q.15 has "7/12", Q.23 has "3(1/3)"
    - IMAGE CLASSIFICATIONS: 11 images classified (6 MATH, 1 TABLE,
      0 TEXT, 4 VISUAL) — transcriptions ready for pipeline
    - Metadata: Question ID, Option IDs, Status, Chosen Option to strip
    - Source has Adda247 branding to strip

PHASE B — BUILD (3–4 tool calls):

  CALL B1: Write complete pipeline.py
    create_file: /home/claude/work/pipeline.py
    Contains:
      - Trigger parsing (ExamCode, date, session from trigger)
      - Source reader (format-appropriate extraction)
      - IMAGE_CLASSIFICATIONS dict (v1.6 — from Phase A-IMAGE)
      - Metadata stripper (all categories)
      - Sanitiser (control character removal)
      - Section merger + renumberer (Q.1 → Q.N continuous)
      - Passage detector + replicator
      - OMML converter (fractions, roots, superscripts)
      - Image-aware figure detector (v1.6 — checks classification
        before placeholder; transcribes MATH/TABLE/TEXT images)
      - DI table builder (v1.14 — TableSpec + corpus_io.build_di_table;
        spans preserved, cells rendered through render_text_with_math)
      - Document builder (date labels, stems, options, blanks)
      - Validator (22 checks)
      - File saver + copier

  CALL B2: Run pipeline
    bash_tool: cd /home/claude/work && python3 pipeline.py
    → Extracts, transforms, validates, saves

  CALL B3 (if needed): Fix and re-run
    bash_tool: (fix script and re-execute if validation issues)

  CALL B4: Deliver
    present_files: /mnt/user-data/outputs/SSC_CGL_T1_18-Jan-2025_Shift-1.docx

FORMAT C1 VARIANT (scanned source — v1.7):
  After CALL A2, run classify_source_pdf(). If C1 / C-HYBRID / C0_OR_C1:
  rasterise each page (page.get_pixmap), pass the legibility gate (which
  resolves C0_OR_C1 to C1 -> proceed or C0 -> HALT), classify + skip
  non-question pages (EC-P2/P13/P17/P21), view question pages in order,
  transcribe into a continuous buffer, then build via the standard text
  path (S1-13). Call mark_vision_transcribed() and add the filename suffix
  before delivery. View-call budget scales with question-page count; batch
  beyond ~40 pages using the F1 continue footer.

POST-DELIVERY:
  Render delivery footer per Framework_DeliveryFooter.md.
```

---

## §10 — CROSS-STEP SYNC CONTRACT

```
Step 1's output is consumed by multiple downstream steps. These are the
contracts that MUST be maintained. Any change to Step 1 output format
requires updating ALL consuming steps.

MODULE DEPENDENCY (v1.9): image discovery is delegated to corpus_io
(Cluster I) — the same implementation Steps 3, 4 and 5 use. It must be
routed to PYQPrepare in routes.json. A local re-implementation of any
corpus_io function is forbidden: this file carried DEFECT I and DEFECT J
for exactly as long as it kept its own copy of extract_images, while both
had already been fixed elsewhere. Two copies produce no drift signal until
they disagree, and by then the images are already gone.

MODULE DEPENDENCY (v1.14): TABLE STRUCTURE is delegated to corpus_io
(Cluster I) for the same reason and after the same kind of failure —
normalise_table_spec, place_cells, build_di_table, read_table_spec,
table_spec_spans, read_table_spans, adjacent_table_pairs. This spec keeps only
a thin forwarding adapter (S4-3). Framework_MockTestCreate S8-4 currently holds
the SECOND flat implementation (build_di_table_styled(doc, headers, rows),
single header row) and must adopt the same model before a mock paper can
reproduce a two-tier DI header — until it does, a structure Step 1 preserves is
lost at Step 7. Tracked as the second half of GAP-2026-07-29-TBL; it also needs
corpus_io added to the MockCreate/TestCreate routes in routes.json.

TABLE CONTRACT (v1.14): Row files may now contain merged cells. Consumers that
read tables MUST use corpus_io._table_rows (anchor cells, no repeats) or
corpus_io.read_table_spec (full geometry). Reading python-docx row.cells
directly returns one entry per GRID COLUMN and repeats the anchor for every
covered position, so a 4-column merged header reads as four identical strings
and a vertically merged label reappears in every row it spans.
  CONSUMER STATUS AT v1.14:
    Step 3 PYQSort        — SAFE, no change. Question bodies are carried as
                            body_elems [<w:p> or <w:tbl>] and DEEP-COPIED, so
                            merges survive byte-identically.
    Step 4 / Step 2c      — SAFE. corpus_io._table_rows is the only reader and
                            is anchor-only from v1.14; output on a flat table is
                            byte-identical to before.
    Step 8 PYQFormat      — SAFE. TCPR_ORDER already lists gridSpan/hMerge/vMerge,
                            so merged cells survive its XML normalisation.
    Step 5 PYQExtract     — table-blind by design (no w:tbl handling at all);
                            unaffected either way. Documented so the silence
                            reads as a decision rather than an omission.
    Step 7 MockCreate     — NOT YET COMPLIANT. See MODULE DEPENDENCY (v1.14).

CONSUMER: Step 2b PYQScan (Framework_PYQAnalyse.md)
  READS: Row file Q.N stems for subtopic classification
  EXPECTS: Q.N format, date labels, no metadata, no answers

CONSUMER: Step 3 PYQSort (Framework_PYQSort.md)
  READS: Row file for re-sorting by taxonomy
  EXPECTS:
    - Date labels matching: ^\[(\d{1,2})-([A-Za-z]{3})-(\d{4})(?:\s+.+\s+(\d+))?\]$
      (session part is OPTIONAL — PYQSort v1.8 handles both forms)
    - Q.N continuous numbering (Step 1 always outputs continuous)
    - Options in OPT_PATTERNS format (canonical "1. text" always matches)
    - NAT questions: valid with zero options
    - No metadata, no answers, no section separators

CONSUMER: Step 5 PYQExtract (Framework_MockTestAnalyse.md)
  READS: Sorted PYQ (output of Step 3, which reads Step 1's Row file)
  EXPECTS: Same Q_PATTERNS, OPT_PATTERNS contracts

PYQSort SYNC STATUS: COMPLETE (v1.8)
  PYQSort v1.8 build_date_label_re() uses optional group for session:
    ^\[(\d{1,2})-([A-Za-z]{3})-(\d{4})(?:\s+<keyword>\s+(\d+))?\]$
  parse_date_label() defaults session to 1 when not present.
  No further updates needed.

PROVENANCE RIPPLE (v1.7 — additive, non-breaking):
  FORMAT C1/C-HYBRID Row files carry core_properties.category =
  "PYQPrepare-Source-Trust:VISION-TRANSCRIBED". This is ADDITIVE metadata;
  Steps 2b/3/4/5/7 need NO change to keep working. Optionally, a consuming
  step MAY read this property and surface a "source unverified" flag so the
  verification burden travels with the data. No consumer is REQUIRED to.
```

---

## §11 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL IN THIS SPEC (identical every exam):
  Output contract (§1) — all formatting, numbering, styling rules
  Q detection patterns (§3 Q_PATTERNS, aligned with Steps 3/5)
  Option detection and normalisation (§3 SOURCE_OPT_PATTERNS)
  String sanitisation (§2 S2-4)
  Metadata stripping vocabulary (§2 S2-3, all 6 categories)
  Red placeholder specification (§1 S1-7)
  Image Inspection Protocol (§1 S1-12, v1.6)
  Scanned-source vision transcription (§1 S1-13, v1.7 — deterministic
    C0/C1/C-HYBRID tiers, provenance marker)
  OMML helper functions (§3 S3-4)
  DI table builder (§4 S4-3)
  Document builder functions (§4)
  Validation checks (§5)
  Delivery contract (§7)
  All edge cases (§8, 25 total — EC-P1 through EC-P25)
  Table structure contract (§1 S1-8a) and block composition (§1 S1-8b)

EXAM-SPECIFIC (from trigger + source content at runtime):
  ExamCode (from trigger)
  Date and session (from trigger)
  Source file format (auto-detected from source)
  Question count (from source content)
  Option count per question (from source content)
  Section structure (from source content — merged in output)
  Math content requiring OMML (from source content)
  Figure presence (from source content)
  Passage structure (from source content)
  Metadata vocabulary extensions (from source content)
  Third-party branding to strip (from source content)

PROOF:
  SSC CGL Tier 1: 4 sections, 100 Q, Shift, all MCQ, 4 options
  SSC CGL Tier 2: 5 sections, 150 Q, Shift, all MCQ, 4 options
  GATE CS:        1 section,  65 Q, Session, MCQ+NAT, 4 options
  IBPS PO:        5 sections, 100 Q, Slot, all MCQ, 5 options
  UPSC CSE:       1 section,  100 Q, no session, all MCQ, 4 options
  NEET:           1 section,  200 Q, no session, all MCQ, 4 options
  CAT:            3 sections, 66 Q, Session, MCQ+NAT, 4 options
  Same spec handles all — zero exam-specific code in framework.
```

---

## §12 — DEFINITION OF DONE

```
☐ 1.  Trigger parsed: ExamCode, date, optional session extracted
☐ 2.  Source file inspected: format identified, structure understood
☐ 3.  Source text extracted: all questions and options captured
☐ 3a. Embedded images extracted via corpus_io — including images inside TABLE
       CELLS and legacy VML — and every one classified (v1.6/v1.9 — S1-12)
☐ 3a1. Mapping total cross-checked against corpus_io.count_image_refs — no
       image reaches the build unclassified (v1.9)
☐ 3a2. Every image that received a CLASSIFICATION had its cell OBSERVED in
       Phase B (v1.11 — S1-12). Unobserved ⇒ image left untouched, no
       placeholder, run completes, count stated, footer F1 amber
☐ 3b. Math/table/text images transcribed (v1.6 — zero math placeholders)
☐ 4.  Metadata stripped: all 6 categories removed, zero leakage
☐ 5.  Strings sanitised: no C0 control characters remain
☐ 6.  Sections merged: continuous Q.1 → Q.N numbering applied
☐ 7.  Options normalised: all converted to canonical "N. text" format
☐ 8.  Each option on its own line: no multi-option rows
☐ 9.  Math converted to OMML: fractions, roots, superscripts rendered
☐ 10. Figures handled: red placeholders ONLY for VISUAL-IMAGE classified,
       and ONLY under a passing probe (v1.9)
☐ 10b. Probe result stated in the delivery message alongside the placeholder
       count, so every placeholder's provenance is auditable (v1.9 — §7)
☐ 10a. Scanned source (C1/C-HYBRID): legibility-gated vision transcription
       with mandatory VISION provenance marker (v1.7 — S1-13)
☐ 11. DI tables rendered: native Word tables, not images
☐ 11a. Table STRUCTURE preserved: every merged cell in the source is a merged
       cell in the output; no padded empty cells (v1.14 — S1-8, S1-8a)
☐ 11b. Table cells rendered through render_text_with_math: OMML math and
       {{u}} underlines work inside cells (v1.14 — S1-6, S1-11)
☐ 11c. No two adjacent block-level tables anywhere in the document; figure-option
       sets are ONE table with one row per option (v1.14 — S1-8b, CHECK 18)
☐ 11d. Text-layer tables detected and built as tables, not parsed as stem prose
       (v1.14 — S2-2 CALL A2b)
☐ 12. Passages repeated: every sub-question has passage, Q.N-FIRST layout
☐ 13. Date labels present: one per question, correct format and style
☐ 14. Answer markers stripped: no ✓/✗, no correct answer indicators
☐ 15. Document formatting: Arial 11pt, A4, 1" margins, proper spacing
☐ 16. Validation run: all 22 checks executed, results logged
☐ 17. Row file delivered via present_files (1 file, closed set)
☐ 18. Delivery footer rendered per Framework_DeliveryFooter.md

POST-DELIVERY:
  User downloads Row file.
  User uploads to [ExamCode] project Files or Google Drive PYQ folder.
  Next: Step 2a PYQDraft — provide Exam Syllabus + Exam Pattern.
```

---

# END OF Framework_PYQPrepare v2.1
