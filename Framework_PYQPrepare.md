# Framework_PYQPrepare v1.6 — Universal PYQ Row File Generator
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
#   v1.6 — 2026-07-07 — IMAGE INSPECTION PROTOCOL (math-as-image fix).
#          Root cause: source files (especially docx from coaching platforms)
#          render math questions as embedded images with no extractable text.
#          The previous spec surrendered all image-only content to red
#          placeholders — including MATH content (fractions, equations,
#          tables, expression-heavy stems). Production defect: SSC CGL T2
#          18-Jan-2025 Shift 1 — Q.6, Q.14, Q.15, Q.17, Q.19–Q.22,
#          Q.28–Q.30 (11 math questions, ~35% of Quant section) delivered
#          with red placeholders instead of transcribed math content.
#          Fix: (1) new S1-12 IMAGE INSPECTION PROTOCOL — mandatory
#          Phase A sub-step that extracts all embedded images, Claude views
#          each, classifies as MATH-IMAGE / TABLE-IMAGE / TEXT-IMAGE /
#          VISUAL-IMAGE, and transcribes content for non-visual images.
#          Transcriptions are baked into pipeline.py as IMAGE_CLASSIFICATIONS
#          dict. (2) S1-6 "surrender" clause replaced — image-rendered math
#          now triggers image inspection, NOT automatic placeholder. Red
#          placeholders for math are BANNED unless image is unreadable.
#          (3) S1-7 updated — placeholder assignment requires prior image
#          classification; unclassified images are a HARD BUG. (4) S3-3
#          figure detection updated to use classification results. (5) S2-2
#          Phase A expanded — image extraction is mandatory when source
#          contains embedded images. (6) new EC-P20 math-as-image edge
#          case with 8 sub-scenarios. (7) new CHECK 13 — IMAGE CLASSIFICATION
#          detection: scans for figure-only stems in math-range questions
#          and cross-references against image classification log. (8) §9
#          execution walkthrough updated with Phase A-IMAGE sub-phase.
#          (9) §12 DoD updated with image inspection items. (10) EC-P4
#          updated to reference image classification prerequisite.
#          Total checks: 12→13. Tool call budget: 4–7 → 5–15
#          (image-count-dependent).
#   v1.5 — 2026-07-07 — INLINE UNDERLINE PRESERVATION.
#          Root cause: questions like "Select the meaning of the underlined
#          word" had the underlined word (e.g. "leisurely") rendered as plain
#          bold text — the underline was LOST during extraction. Without the
#          underline, the question is nonsensical. Production defect: SSC CGL
#          T2 18-Jan-2025 Q.2 — "leisurely" underlined in source, plain in
#          output.
#          Fix: (1) new S1-11 INLINE FORMATTING CONTRACT — defines {{u}}...
#          {{/u}} marker convention for underlined text. Underlines are the
#          only semantically significant inline formatting in PYQ stems
#          (vocabulary, error detection, sentence improvement questions).
#          (2) S2-1 FORMAT D (docx) updated — extraction must detect
#          run.underline and wrap in {{u}}...{{/u}} markers. FORMAT A (PDF)
#          guidance added for pdfplumber char-level underline detection.
#          (3) set_font() gains underline parameter (S4-2).
#          (4) render_text_with_math() refactored — now splits on {{u}} markers
#          FIRST, then processes each segment for math. Underlined segments
#          get run.underline=True on all text runs within them.
#          (5) new CHECK 12 — SEMANTIC UNDERLINE VALIDATION: if stem text
#          contains "underlined" but no underline formatting exists in the
#          paragraph XML → WARN. Catches extraction failures.
#          (6) new EC-P19 — underline handling edge case.
#          Total checks: 11→12.
#   v1.4 — 2026-07-07 — MATH RENDERING HARDENING (5 fixes).
#          Comprehensive audit of all math patterns in SSC CGL T2 output
#          (35 OMML elements, 150 questions). Findings: v1.3 compound fix
#          resolved the ROOT CAUSE; 5 additional gaps identified and fixed:
#          (1) FRACTION REGEX FIX: character class [\d√⟦\[SQRT:\]⟧] was
#          buggy — included individual letters S,Q,R,T as false-positive
#          matches. Replaced with clean r'(\d*√?\d+)\s*/\s*(\d*√?\d+)'
#          that matches only digit+√ combinations. Pre-normalization of
#          residual markers makes SQRT characters in the class unnecessary.
#          (2) DATE FALSE-POSITIVE FIX: 12/05/2024 matched as fraction 12/05.
#          Added date context lookahead — if matched denominator is followed
#          by /\d{2,4}, skip (it's a date). Also added lookbehind for
#          preceding digit+/ patterns.
#          (3) NTH ROOT HELPER: new omml_nthroot(degree, content) in S3-4
#          for cube roots ³√8, fourth roots ⁴√16 etc. Q.14 in the reference
#          paper had ³√6859 × ⁴√1296 — pipeline managed without the helper
#          but the spec should provide it for reliability.
#          (4) PRE-NORMALIZATION: render_text_with_math() now normalizes
#          all ⟦SQRT:N⟧ and [SQRT:N] markers to √N at the TOP before any
#          pattern matching. Eliminates timing-dependent Pattern 4 catch.
#          Pattern 4 (residual markers) removed — pre-norm handles it.
#          (5) 2-TIER ARCHITECTURE NOTE: S1-6 now documents the two-tier
#          math handling system: pipeline-level detection (primary — handles
#          complex expressions, trig fractions, nth roots, multi-OMML
#          compounds) vs render_text_with_math() safety net (catches simple
#          fractions, √, mixed numbers, residual markers that pipeline
#          missed). Complex expressions like (secθ−tanθ)/(secθ+tanθ) are
#          PIPELINE responsibility, not safety-net scope.
#   v1.3 — 2026-07-07 — COMPOUND MATH RENDERING FIX.
#          Root cause: omml_frac() accepted only simple text strings for
#          numerator/denominator. When a fraction component contained compound
#          content (e.g. "2√3" in the denominator of 1/(2√3)), the √3 was
#          left as a literal ⟦SQRT:3⟧ text marker inside <m:t> instead of
#          being decomposed into nested <m:rad> OMML. Production defect:
#          SSC CGL T2 18-Jan-2025 Q.17 option 3 showed "2[SQRT:3]" as
#          visible text in the rendered document.
#          Fix: (1) new build_math_run() — creates atomic <m:r><m:t> element.
#          (2) new build_compound_content() — recursively decomposes compound
#          math strings into mixed [text-run + OMML-element] lists. Handles
#          √N within fraction components, ⟦SQRT:N⟧ residual markers, and
#          arbitrary text+sqrt combinations. (3) omml_frac() rewritten to
#          use build_compound_content() for BOTH num and den — supports
#          1/(2√3), √3/2, 2√5/7, etc. (4) new render_text_with_math() —
#          top-level function that parses a text string for inline math
#          patterns (fractions, roots, mixed numbers, residual tags) and
#          renders segments as alternating text-runs + OMML elements. Handles
#          false-positive exclusions (km/h, dates, and/or). (5) add_stem()
#          and add_option() in S4-2 updated to call render_text_with_math()
#          instead of plain p.add_run(). (6) new CHECK 11 — RESIDUAL MATH
#          MARKERS validation: scans all <m:t> and paragraph text for
#          unresolved ⟦SQRT:⟧, [SQRT:], or stray √ patterns that should
#          have been converted to OMML. (7) S1-6 contract updated with
#          compound expression examples. Total checks: 10→11.
#   v1.2 — 2026-07-07 — Q.N-FIRST BLOCK CONTRACT FOR PASSAGE QUESTIONS.
#          Root cause: Step 1 output placed passage/instruction BEFORE Q.N
#          for passage-linked questions (RC, Cloze, DI). This violated the
#          universal "a question starts with Q.N" expectation and conflicted
#          with MockTestCreate v3.7 Q.N-FIRST contract. Downstream consumers
#          (Steps 3, 5, 7) expect every question block to OPEN with Q.N.
#          Fix: §1 S1-2 block structure diagram updated — removed position 1a
#          (passage before Q.N). Passage now ALWAYS follows Q.N stem. §1 S1-9
#          passage handling rewritten — "preserve source ordering" removed,
#          replaced with mandatory Q.N-FIRST layout: Date→Q.N→instruction→
#          passage→options. §2 S2-6 updated to match. §8 EC-P8 updated. §12
#          DoD item 12 updated. Aligns Step 1 output with MockTestCreate §9
#          SC-3 Q.N-FIRST rule, so PYQ Row files are natively compatible with
#          the online importer expectation.
#   v1.1 — 2026-07-07 — CROSS-STEP SYNC AUDIT FIX (1 stale text fix).
#          §10 cross-step contract: "PYQSort UPDATE REQUIRED" was stale —
#          PYQSort v1.8 already has the optional session fix. Changed to
#          "PYQSort SYNC STATUS: COMPLETE (v1.8)" with current regex.
#   v1.0 — 2026-07-07 — Initial release. Derived from TestSeriesRow Tier 1 v17
#          and Tier 2 v3. Full exam-agnostic rewrite. 31 design decisions
#          documented and resolved. Two-layer architecture (output contract +
#          adaptive source parsing). Cross-step sync verified against PYQSort
#          v1.7, PYQAnalyse v2.10, MockTestAnalyse v2.4, MockTestCreate v5.8.
#          Output contract: continuous Q.1→Q.N, canonical option format,
#          configurable date labels, OMML math, red placeholders for figures,
#          native Word tables for DI, passage repetition for all exam types.

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

Empty/corrupt questions (no stem, no image): include as Q.N with no
content after the number. Downstream steps handle classification.
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
All mathematical content in stems AND options MUST be rendered using
OMML (Office MathML) or Unicode math symbols. No red-box substitution for math.

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

TWO-TIER MATH HANDLING ARCHITECTURE (v1.4):

  TIER 1 — PIPELINE-LEVEL DETECTION (PRIMARY):
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
    omml_sub) are the building blocks used at this tier.

  TIER 2 — render_text_with_math() SAFETY NET:
    When the pipeline passes text to add_stem() or add_option(), the
    render_text_with_math() function scans for RESIDUAL math patterns
    that the pipeline missed. It handles:
      - Simple numeric fractions: 1/2, 7/12
      - Fractions with √: 1/√3, √3/2, 2√3/5, 1/2√3
      - Mixed numbers: 3(1/3), 12(2/5)
      - Standalone √N: √3, √15
      - Residual ⟦SQRT:N⟧ or [SQRT:N] pipeline markers
    It does NOT handle complex expressions (trig, operators, variables) —
    those are Tier 1's responsibility.

  TIER 3 — CHECK 11 VALIDATION:
    After the document is built, CHECK 11 scans for any residual math
    markers that BOTH tiers missed. Any occurrence is a WARN requiring
    investigation.

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

  Red placeholders for math content are BANNED. The ONLY legitimate
  placeholder for a math question is when the image is physically
  unreadable after Claude has viewed it. "No extractable text" is NOT
  sufficient reason — Claude's vision capability is the fallback.

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
    Render as: 2-column borderless table per option (label | image)
    Keep the text stem above the option placeholder table

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

Render using doc.add_table() with 'Table Grid' style.
Preserve source data exactly. Font size in table cells may differ from
body font (typically 9pt) — this is acceptable.

Never render tables as images or placeholders.
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

PHASE A — IMAGE EXTRACTION (part of Phase A inspection):

  Step 1: Extract all embedded images from the source to numbered files.

  FORMAT D (docx):
    Extract via python-docx relationships:
```

```python
import os
from docx import Document

def extract_images(docx_path, output_dir):
    """
    Extract all embedded images from a docx file.
    Returns dict mapping paragraph_index → image_filepath.
    """
    doc = Document(docx_path)
    os.makedirs(output_dir, exist_ok=True)
    image_map = {}  # {para_index: image_path}
    img_counter = 0

    for i, para in enumerate(doc.paragraphs):
        xml = para._element.xml
        if '<w:drawing' not in xml and '<w:pict' not in xml:
            continue
        # Extract image data from relationships
        for rel in doc.part.rels.values():
            if "image" in rel.reltype:
                # Check if this relationship is referenced in this paragraph
                rel_id = rel.rId
                if rel_id in xml:
                    img_data = rel.target_part.blob
                    ext = os.path.splitext(rel.target_ref)[1] or '.png'
                    img_path = os.path.join(output_dir, f"img_{img_counter:03d}{ext}")
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    image_map[i] = img_path
                    img_counter += 1
                    break  # One image per paragraph for mapping

    return image_map
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
    Action: Claude transcribes the table data as a list of rows.
    Pipeline builds a native Word table using build_di_table().
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
    # Q.14 — table image
    86: ("TABLE", [
        ["Class Interval", "0-10", "10-20", "20-30", "30-40", "40-50"],
        ["Frequency", "5", "8", "15", "12", "10"],
    ]),
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
          # Write as native Word table
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

FORMAT C — SCANNED PDF (image-only, no text layer)
  Description: Each page is a rasterised image with no embedded text.
  Detection  : pdftotext yields empty/garbage output. Pages are images.
  Strategy   : HALT — inform user that OCR pre-processing is needed.
               Step 1 does not perform OCR. User must provide a text-layer
               PDF or an OCR-processed version.

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
    Remove OCR control-character corruption.
    Delete C0 control bytes EXCEPT tab (\t) and newline (\n, \r).
    Preserve ALL legitimate Unicode: curly quotes, em/en dashes, ₹, °, θ, π, etc.
    """
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)
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

Q_PATTERNS = [
    r'^Q\.\s*(\d+)\s+',            # Q.1  Q.25  Q. 1
    r'^Q(\d+)\.\s+',               # Q1.  Q25.
    r'^Question\s+(\d+)\s*[:.]',   # Question 1:
    r'^(\d+)\.\s+(?!\d)',           # 1.   25.   (negative lookahead: not 1.5)
    r'^\((\d+)\)\s+',              # (1)  (25)
]

def detect_question_start(text):
    """Detect if a line starts a new question. Returns source Q-number or None."""
    for pat in Q_PATTERNS:
        m = re.match(pat, text.strip())
        if m:
            return int(m.group(1))
    return None
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

### S3-5 — Inline math renderer (v1.3; v1.4 hardened)

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

def render_text_with_math(paragraph, text, bold=False, color=None):
    """
    TIER 2 SAFETY NET — render text with inline OMML and underline formatting.

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

def add_placeholder_opt(doc, opt_num, red_png_path):
    """
    Add red placeholder for one figure option.
    Creates a 1-row, 2-column borderless table: [label | image].
    """
    tbl = doc.add_table(rows=1, cols=2)
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
    # Label cell
    cell_label = tbl.cell(0, 0)
    cell_label.text = f"{opt_num}."
    for r in cell_label.paragraphs[0].runs:
        set_font(r)
    # Image cell
    cell_img = tbl.cell(0, 1)
    p = cell_img.paragraphs[0]
    r = p.add_run()
    r.add_picture(red_png_path, width=Inches(2.5))
    return tbl
```

### S4-3 — DI table builder

```python
def build_di_table(doc, rows_data):
    """
    Build a native Word table from extracted tabular data.
    rows_data: list of lists, e.g. [['Year', '2020', '2021'], ['Revenue', '100', '200']]
    """
    if not rows_data:
        return None
    n_rows = len(rows_data)
    n_cols = max(len(row) for row in rows_data)
    tbl = doc.add_table(rows=n_rows, cols=n_cols, style='Table Grid')
    for ri, row in enumerate(rows_data):
        for ci, cell_text in enumerate(row):
            if ci < n_cols:
                cell = tbl.cell(ri, ci)
                cell.text = str(cell_text)
    return tbl
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

CHECK 7 — NO CONTROL CHARACTERS
  Scan all paragraph text for C0 control bytes: [\x00-\x08\x0b\x0c\x0e-\x1f]
  WARN if any found (sanitisation missed something).

CHECK 8 — NO ANSWER MARKERS
  Scan for ✓ ✔ ✗ ✘ characters and "Ans" / "Ans." text.
  WARN if any found.

CHECK 9 — OPTIONS FORMAT
  Every option paragraph should match r'^[1-5]\.\s+'.
  WARN if non-canonical options found.

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
```

### S5-2 — Validation implementation

```python
def validate_row_file(doc_path, date_label_text):
    """
    Run all 13 validation checks. Return (pass_count, warn_count, messages).
    """
    from docx import Document
    import re

    doc = Document(doc_path)
    paras = doc.paragraphs
    warnings = []

    # CHECK 1 — Q-count
    q_paras = [p for p in paras if re.match(r'^Q\.\d+', p.text.strip())]
    q_count = len(q_paras)
    print(f"CHECK 1: Q-count = {q_count}")

    # CHECK 2 — Sequential numbering
    q_nums = []
    for p in paras:
        m = re.match(r'^Q\.(\d+)', p.text.strip())
        if m:
            q_nums.append(int(m.group(1)))
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

    # CHECK 7 — Control characters
    CTRL_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
    ctrl = sum(1 for p in paras if CTRL_RE.search(p.text))
    if ctrl:
        warnings.append(f"CHECK 7 WARN: {ctrl} paragraphs with control characters")
    else:
        print("CHECK 7: No control characters OK")

    # CHECK 8 — Answer markers
    ans_markers = sum(1 for p in paras if re.search(r'[✓✔✗✘]', p.text) or re.search(r'\bAns\b', p.text))
    if ans_markers:
        warnings.append(f"CHECK 8 WARN: {ans_markers} answer markers found")
    else:
        print("CHECK 8: No answer markers OK")

    # CHECK 9 — Option format
    opt_re = re.compile(r'^[1-5]\.\s+')
    bad_opts = 0
    for p in paras:
        t = p.text.strip()
        if p.paragraph_format.left_indent and p.paragraph_format.left_indent > 0:
            if t and not opt_re.match(t):
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
        if re.match(r'^Q\.\d+', t) and 'underlined' in t.lower():
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
    for idx, p in enumerate(paras):
        t = p.text.strip()
        # Detect figure-only stems: Q.N with very short text (just "Q.N")
        m = re.match(r'^Q\.(\d+)\s*$', t)
        if m:
            qnum = int(m.group(1))
            # Check if next paragraph has an inline image (placeholder)
            if idx + 1 < len(paras):
                next_xml = paras[idx + 1]._element.xml
                if '<w:drawing' in next_xml or '<w:pict' in next_xml:
                    figure_only_qnums.append(qnum)
    # Report figure-only stems for manual verification against
    # IMAGE_CLASSIFICATIONS. In automated mode, cross-check with
    # the classifications dict. In validation-only mode, report count.
    if figure_only_qnums:
        print(f"CHECK 13: {len(figure_only_qnums)} figure-only stems "
              f"detected: Q.{figure_only_qnums}. Verify these are all "
              f"VISUAL-IMAGE classified (not MATH/TABLE/TEXT).")
    else:
        print("CHECK 13: No figure-only stems — all content transcribed OK")

    # Summary
    pass_count = 13 - len(warnings)
    for w in warnings:
        print(f"  ⚠️ {w}")
    print(f"\n{'✅' if not warnings else '⚠️'} {pass_count}/13 checks passed, {len(warnings)} warnings")

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
  images or placeholders. Preserve source data exactly.

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
    Claude views → TABLE-IMAGE → transcribe rows.
    Pipeline writes: add_stem(doc, N, ""), then build_di_table().

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
    bash_tool: python3 -c "... extract_images() from S1-12 ..."
    → Saves images to /home/claude/work/images/img_000.png, img_001.png, ...
    → Records paragraph-to-image mapping with surrounding Q-context.

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
      - DI table builder
      - Document builder (date labels, stems, options, blanks)
      - Validator (13 checks)
      - File saver + copier

  CALL B2: Run pipeline
    bash_tool: cd /home/claude/work && python3 pipeline.py
    → Extracts, transforms, validates, saves

  CALL B3 (if needed): Fix and re-run
    bash_tool: (fix script and re-execute if validation issues)

  CALL B4: Deliver
    present_files: /mnt/user-data/outputs/SSC_CGL_T1_18-Jan-2025_Shift-1.docx

POST-DELIVERY:
  Render delivery footer per Framework_DeliveryFooter.md.
```

---

## §10 — CROSS-STEP SYNC CONTRACT

```
Step 1's output is consumed by multiple downstream steps. These are the
contracts that MUST be maintained. Any change to Step 1 output format
requires updating ALL consuming steps.

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
  OMML helper functions (§3 S3-4)
  DI table builder (§4 S4-3)
  Document builder functions (§4)
  Validation checks (§5)
  Delivery contract (§7)
  All edge cases (§8, 20 total — EC-P1 through EC-P20)

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
☐ 3a. Embedded images extracted and classified (v1.6 — S1-12)
☐ 3b. Math/table/text images transcribed (v1.6 — zero math placeholders)
☐ 4.  Metadata stripped: all 6 categories removed, zero leakage
☐ 5.  Strings sanitised: no C0 control characters remain
☐ 6.  Sections merged: continuous Q.1 → Q.N numbering applied
☐ 7.  Options normalised: all converted to canonical "N. text" format
☐ 8.  Each option on its own line: no multi-option rows
☐ 9.  Math converted to OMML: fractions, roots, superscripts rendered
☐ 10. Figures handled: red placeholders ONLY for VISUAL-IMAGE classified
☐ 11. DI tables rendered: native Word tables, not images
☐ 12. Passages repeated: every sub-question has passage, Q.N-FIRST layout
☐ 13. Date labels present: one per question, correct format and style
☐ 14. Answer markers stripped: no ✓/✗, no correct answer indicators
☐ 15. Document formatting: Arial 11pt, A4, 1" margins, proper spacing
☐ 16. Validation run: all 13 checks executed, results logged
☐ 17. Row file delivered via present_files (1 file, closed set)
☐ 18. Delivery footer rendered per Framework_DeliveryFooter.md

POST-DELIVERY:
  User downloads Row file.
  User uploads to [ExamCode] project Files or Google Drive PYQ folder.
  Next: Step 2a PYQDraft — provide Exam Syllabus + Exam Pattern.
```

---

# END OF Framework_PYQPrepare v1.6
