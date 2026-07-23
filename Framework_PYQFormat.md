# Framework_PYQFormat v1.3 — Universal PYQ Student Document Formatter
# [ExamCode] project | PYQ-3 (PYQFormat) | Exam-agnostic
#
# v1.3 — 2026-07-23 — Page-level header and footer (every page). The exam
#   header (§3) and IFAS footer (§6) are no longer one-time body paragraphs;
#   they are real Word page header/footer PARTS (header1.xml / footer1.xml
#   wired via sectPr references) that repeat automatically on every page.
#   Header layout: exam name LEFT, date · session CENTER, IFAS RIGHT.
#   Footer layout: website LEFT, tagline CENTER, phone RIGHT. Tagline (D5)
#   changed to "IFAS – India's No. 1 Exam Preparation Platform". No page
#   numbers; first page identical to all others. Body insertions are now
#   pills ONLY, simplifying S8-3/S8-8. New decision D10; new S13-6
#   part-wiring mechanics.
#
# v1.2 — 2026-07-23 — Explanation tag restyle (§7-4..§7-6). The explanation
#   tag headers (AXIOM, DEDUCTION, SPEED HACK, WHY WRONG?, COMMON PITFALLS),
#   the Correct Answer line, and the Option/pitfall sub-heads are restyled
#   into colored tint bands with 3pt left accent bars, per-tag colors from
#   the document-wide design palette (Appendix A). Marker glyphs upgraded
#   in tag headers only: ⬛→📘 (AXIOM), ⬛→🧮 (DEDUCTION), ❌→⚠️ (COMMON
#   PITFALLS); ⚡ and ❌ WHY WRONG? unchanged. The glyph substitution is the
#   ONLY text change PYQFormat ever performs (D9) — verified by a new
#   full-document text-stream integrity check (S8-8). Delivery report gains
#   §R6 (Tag styling). New architecture decision D9.
#
# v1.1 — 2026-07-23 — Date/Session tag removal (§4). The per-question
#   date/session tag paragraph (PYQSort date_label, e.g. "[12-Sep-2025 Shift 1]"
#   or "[02-Feb-2025]") that rides through PYQExplain/PYQExplainAudit above
#   each question is now REMOVED from the student-facing document. This is the
#   ONLY sanctioned deletion — the zero-mutation rule is amended accordingly.
#   Removal uses a keyword-agnostic anchored regex (works even when
#   exam_config.json is absent), verifies each removed paragraph is media-free
#   (no OMML, no drawings), and a new integrity check (S8-7) confirms zero tag
#   paragraphs remain in the output. Delivery report gains §R4 (Tags removed).
#   New architecture decision D8.
#
# v1.0 — 2026-07-22 — Initial release. Takes the audited PYQ explanation
#   document from PYQ-2 (PYQExplainAudit) and transforms it into a beautiful,
#   student-facing Word document: page header/footer on every page, per-
#   question colored Subject/Topic/Subtopic pills, and visual polish.
#   ZERO content changes — every question, option, explanation sentence, and
#   OMML fraction is byte-identical to the input. This is purely a VISUAL
#   transformation step.
#
#   Architecture decisions locked with the framework owner:
#     D1. ZERO CONTENT CHANGES. Not one character of any question, option,
#         explanation, or answer is modified. PYQFormat adds visual elements
#         AROUND the certified content — never inside it.
#     D2. FORK INPUT. PYQ-3 takes PYQ-2 output directly
#         ([ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx).
#         PYQ-3 and PYQ-4 are INDEPENDENT — neither depends on the other.
#     D3. COLORED PILLS (Option C). Per-question Subject/Topic/Subtopic
#         displayed as three colored pill cells (1-row, 3-cell table) inserted
#         BEFORE each Q stem. Subject = blue tint, Topic = green tint,
#         Subtopic = amber/orange tint. Pills are inserted HERE (PYQFormat),
#         NOT in PYQExplain/PYQExplainAudit — keeping the explanation doc
#         clean for engine verification.
#     D4. PILL DATA SOURCE. The q_to_classification map built by PYQ-1 at P3
#         (stored in pyq_explain_progress.json or pyq_audit_progress.json)
#         provides {subject, topic, subtopic, subtopic_id} per question.
#     D5. IFAS BRANDING HARDCODED. Same branding across all exams — no
#         per-exam customization needed.
#     D6. EXAM HEADER FROM CONFIG. Exam name from exam_config.json; date and
#         session from the trigger/filename.
#     D7. STUDENT-FACING OUTPUT. This file is the final download artifact
#         students receive. It must look professional and beautiful.
#     D8. DATE/SESSION TAGS REMOVED (v1.1). The per-question date/session tag
#         paragraphs (PYQSort date_label lines) are internal pipeline metadata,
#         not student content. PYQFormat removes them. The paper's date and
#         session already appear ONCE in the exam header (§3) — repeating them
#         above every question adds noise. This is the ONLY deletion PYQFormat
#         ever performs.
#     D9. EXPLANATION TAG RESTYLE (v1.2). The engine (explain_engine.py)
#         deliberately writes plain headers (black text, no shading) so the
#         explanation document stays clean for engine/audit verification —
#         same rationale as D3. PYQFormat restyles them for students: tint
#         band + accent bar per tag, one palette shared with the pills.
#         Marker glyph substitution (⬛→📘/🧮, ❌→⚠️ on COMMON PITFALLS) is
#         the ONLY text change in the whole spec, allowed in exact-match tag
#         header paragraphs only, and verified by S8-8.
#     D10. PAGE-LEVEL HEADER/FOOTER (v1.3). The exam header and IFAS footer
#         are Word page header/footer parts, not body paragraphs — Word
#         repeats them on every page automatically, surviving any reflow.
#         References are registered for default, even, AND first page types
#         pointing to the same parts, so every page is identical regardless
#         of the document's evenAndOddHeaders / titlePg settings. No page
#         numbers. Tagline (D5 constant) is
#         "IFAS – India's No. 1 Exam Preparation Platform".

# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Transform a certified, content-complete PYQ explanation document into
#   a polished student-facing download. The input has been through PYQ-1
#   (explanation) and PYQ-2 (audit) — every answer is correct, every
#   explanation is validated, the completion gate has passed. PYQ-3's job
#   is purely visual: make it look beautiful for the student who downloads
#   it. No content judgement, no re-derivation, no quality gate — those
#   are done. This is presentation.

# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION (PYQ Explanation Pipeline)
# ════════════════════════════════════════════════════════════════════════
#   PHASE 1 — Already completed (shared with Mock/Test pipeline):
#     Step 1  PYQPrepare    → Row file → Google Drive
#     Step 2  PYQDraft/Scan/Approve → taxonomy, exam_config.json → project
#     Step 3  PYQSort       → Sorted PYQ docs → Google Drive
#     Step 5  PYQExtract    → section_rules.md + subtopic_manifest.json → project
#
#   PHASE 2 — PYQ Explanation:
#     PYQ-1  PYQExplain      → _PYQ_Explanation.docx
#     PYQ-2  PYQExplainAudit → _PYQ_Explanation_Complete.docx
#     PYQ-3  PYQFormat       → _PYQ_Formatted.docx   ← THIS STEP
#     PYQ-4  PYQDeliver      → _PYQ_Final.docx        (portal)
#     (PYQ-3 and PYQ-4 are INDEPENDENT — both take PYQ-2 output.)

# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. Exam name, section
#   names, topic names, subtopic names, question counts — all read at
#   runtime from exam_config.json, the q_to_classification map, and the
#   document itself. Same spec runs for SSC CGL, GATE, NEET, UPSC, CAT,
#   CSIR, Banking, RRB, state PSC, or any exam.
#   The ONLY hardcoded values are IFAS branding strings (D5) — these are
#   company-wide constants, not exam-specific values.

---

# ★ ZERO-MUTATION RULE — NON-NEGOTIABLE

The content of every question block is SACRED. PYQ-3 may only:
- **Add** the exam page header and IFAS page footer as document PARTS
  (header1.xml / footer1.xml + sectPr references, §3/§6/S13-6) — these
  never enter the body
- **Insert** colored pill tables before each Q-stem — the ONLY body
  insertion (new content only)
- **Remove** the per-question date/session tag paragraphs (§4) — the ONLY
  sanctioned deletion. A tag is a standalone paragraph whose FULL text matches
  DATE_TAG_RE and which contains no OMML and no drawings. Nothing else is
  ever deleted.
- **Restyle** the explanation tag header paragraphs, the Correct Answer line,
  and the Option/pitfall sub-heads (§7-4..§7-5) — pPr/rPr styling only
  (shading, borders, color, size, letter-spacing, keep-with-next).
- **Substitute** the leading marker glyph in exact-match tag header
  paragraphs (§7-6): ⬛→📘 (AXIOM), ⬛→🧮 (DEDUCTION), ❌→⚠️ (COMMON
  PITFALLS). This is the ONLY text change PYQFormat ever performs (D9),
  verified by S8-8. No other character anywhere is ever altered.
- **Apply** visual styling (font, spacing, page margins) to existing elements

It **NEVER**:
- Changes any character in any question stem, option, table, image, or
  explanation sentence (the sole exception being the §7-6 marker glyph in
  tag HEADER paragraphs — never in body content)
- Reorders questions
- Removes, rewrites, or paraphrases any content
- Modifies any OMML fraction or math element
- Alters any image, drawing, or media part
- Changes the TEXT of the correct-answer line, or of any axiom, deduction,
  speed-hack, why-wrong, or pitfall sentence (their STYLING changes per
  §7-4..§7-5; the §7-6 marker glyph is the sole text exception, in tag
  header paragraphs only)

Violation of this rule is a hard failure regardless of any other outcome. The
input was certified by PYQ-2's completion gate (CA1–CA7) — PYQ-3 preserves that
certification by touching NOTHING the gate validated.

---

# §0 — Input / output contract

**Inputs:**

1. `[ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx` — the PYQ-2 audited
   explanation document. Attached by user. This is the certified, content-complete
   document that has passed the completion gate.
   ALSO ACCEPTS: `_PYQ_Explanation.docx` (PYQ-1 output, if audit not yet run).
   The spec prefers the audited version; if both are attached, use the
   `_Complete` version.

2. `exam_config.json` — in project knowledge. Provides `exam_name` for the header.

3. `q_to_classification` map — the per-question {subject, topic, subtopic,
   subtopic_id} mapping. Loaded from ONE of these sources (in priority order):
   a. `pyq_audit_progress.json` sidecar (if PYQ-2 was run, this carries the map)
   b. `pyq_explain_progress.json` sidecar (PYQ-1's progress file)
   c. Attached by user as a separate JSON file
   If no classification map is found → HARD STOP:
     "q_to_classification map not found. Run PYQExplain first, or attach
      pyq_explain_progress.json / pyq_audit_progress.json."

NOT REQUIRED (PYQ-3 adds no content):
  ✗ explain_engine.py — no explanations written or read by this step
  ✗ explain_audit_gate.py — no audit performed by this step
  ✗ section_rules.md — no engine configuration needed
  ✗ blueprint.json — PYQ has no mock pipeline outputs
  ✗ registry.json — PYQ has no mock pipeline outputs

**Output:**

- `[ExamCode]_[date]_[session]_PYQ_Formatted.docx` — the student-facing document.
  Body: (pill + question + explanation) × Q_TOTAL. Exam header and IFAS
  footer repeat on EVERY page as page header/footer parts (§3/§6).
  Every question/explanation byte-identical to the input; only visual elements
  added, and the per-question date/session tag paragraphs removed (§4).

---

# §1 — Trigger and resolution

PYQ-3 begins on the instruction:

```text
PYQFormat
```

Attach: the PYQ-2 output (or PYQ-1 output if audit not yet run).

Everything is derived from the attachment and project knowledge:

1. **ExamCode**: derived from project knowledge files (any `[ExamCode]_*` file
   in `/mnt/project/`). If ambiguous → HARD STOP.

2. **Date + Session**: parsed from the attached filename. The filename follows
   the pattern `[ExamCode]_[DD-Mon-YYYY]_[session]_PYQ_Explanation[_Complete].docx`.
   If the filename cannot be parsed → HARD STOP: "Cannot parse date/session from
   the attached filename."

3. **Input document**: the attached file. Accept either:
   - `_PYQ_Explanation_Complete.docx` (PYQ-2, preferred)
   - `_PYQ_Explanation.docx` (PYQ-1, acceptable with WARN)
   If neither attached → HARD STOP: "Attach the PYQ Explanation document."

Derived values (used for filenames and header):
  EXAM         = ExamCode (parsed from project knowledge)
  DATE         = DD-Mon-YYYY (parsed from attached filename)
  SESSION      = session keyword + number (parsed from attached filename, if present)
  DATE_SESSION = DATE[_SESSION] (e.g. 12-Sep-2025_Shift_1)

Resolution sequence (after trigger parsing):

1. Load `exam_config.json` from project knowledge. Extract `exam_name`
   (e.g. "SSC CGL Tier 1", "GATE Life Sciences").
   If exam_config.json is missing → use ExamCode as the display name (WARN, not HALT).

2. Load the `q_to_classification` map (§0 priority order). Parse Q_TOTAL from the
   document (count Q-stems). Verify the map covers Q.1 through Q_TOTAL — a missing
   question in the map means a pill cannot be generated for that question.
   Missing entries → WARN per question (pill omitted for that Q), not HALT.

---

# §2 — Execution model

PYQ-3 is a SINGLE-PASS transformation. No batching, no multi-turn, no "continue"
needed. The entire document is processed in one response:

```text
1. create_file  → write the complete format_pipeline.py script
2. bash_tool    → run it (open input → remove date/session tags → restyle
                  explanation tags → insert pills → wire page header/footer
                  parts → apply styling → save output)
3. bash_tool    → verify output (Q-count, pill-count, tag absence, header/
                  footer parts, text-stream integrity, content integrity)
4. present_files → deliver [ExamCode]_[date]_[session]_PYQ_Formatted.docx
```

This step uses the `unzip → edit XML → zip` approach for editing the existing
docx (python-docx for reading structure, direct XML manipulation for insertions
that must preserve all existing formatting, OMML, images, and drawings intact).

---

# §3 — Exam page header (every page, v1.3)

The exam header is a Word PAGE HEADER part — it appears at the top of EVERY
page of the formatted document, including the first (D10, no titlePg). It is
NOT a body paragraph.

## S3-1 — Header content and layout

One paragraph, three zones via tab stops:

```text
LEFT                      CENTER                      RIGHT
[exam_name]               [DD-Mon-YYYY] · [Session]   IFAS
```

Example:
```text
SSC CGL Tier 1            18-Jan-2025 · Shift 1       IFAS
```

- `exam_name`: from exam_config.json `exam_name` field (or ExamCode as fallback)
- `DD-Mon-YYYY`: from the trigger DATE
- `Session`: from the trigger SESSION, joined to the date with ` · `
  (omit the ` · Session` part entirely if no session)
- `IFAS`: hardcoded (D5)
- Zones: left-aligned run at margin, `<w:tab w:val="center">` at the page
  center, `<w:tab w:val="right">` at the right margin. Tab positions are
  computed from the section's page width and margins at runtime — never
  hardcoded twips (page size varies per exam).

## S3-2 — Header styling

```text
Exam name (LEFT)    : Bold, 9pt, dark blue (#1F3864)
Date · Session (CTR): Regular, 9pt, muted slate (#5A6B85)
IFAS (RIGHT)        : Bold, 10pt, dark blue (#1F3864), letter-spacing 40
                      (2pt tracking — wordmark treatment)
Font face           : Arial (header/footer parts are NEW content, so a font
                      face is set here — S7-3 applies to existing content)
Border              : Thin bottom border, dark blue (#1F3864), sz=6 (0.75pt),
                      space=4 — separates header from body
Spacing             : after=120 (6pt)
```

## S3-3 — Repetition guarantee

The header repeats on every page because it is wired as header parts
referenced from every sectPr for ALL THREE reference types (default, even,
first) — see S13-6. First page is identical to all others; no page numbers
anywhere (D10).

---

# §4 — Date/Session tag removal (v1.1)

The input document carries a per-question date/session tag paragraph — the
PYQSort `date_label` line that sits immediately above each Q-stem and rides
through PYQExplain/PYQExplainAudit unchanged:

```text
[12-Sep-2025 Shift 1]     (multi-session exam, keyword from exam_config)
[02-Feb-2025 Session 2]   (GATE-style keyword)
[15-Jun-2025]             (single-session exam — no keyword/number)
```

These tags are internal pipeline metadata, not student content (D8). The
paper's date and session already appear once in the exam header (§3).
PYQFormat removes every tag paragraph from the document body.

## S4-1 — Tag matching regex

```python
import re

# Keyword-agnostic, anchored full-paragraph match.
# DELIBERATE DIVERGENCE from PYQSort's build_date_label_re(): PYQSort needs
# the exact session_keyword from exam_config.json because it PARSES the
# session number for sorting. PYQFormat only needs to RECOGNIZE the tag for
# deletion, and must work even when exam_config.json is absent (§1 WARN
# case). [A-Za-z]+ therefore matches ANY session keyword (Shift, Slot,
# Phase, Paper, Session, Morning, Afternoon, or custom).
DATE_TAG_RE = re.compile(
    r'^\[\d{1,2}-[A-Za-z]{3}-\d{4}'   # [DD-Mon-YYYY
    r'(?:\s+[A-Za-z]+\s+\d+)?'        # optional: <keyword> <number>
    r'\]$'                            # ] — anchored: FULL paragraph only
)
```

A paragraph is a tag if and only if its FULL reconstructed text (all `<w:t>`
runs concatenated, then `.strip()`) matches DATE_TAG_RE. The anchors guarantee
PYQFormat can never partially delete text: a stem or explanation that merely
CONTAINS a date label inline (e.g. "This question appeared in
[12-Sep-2025 Shift 1] and asks…") does not match and is never touched.

## S4-2 — Removal algorithm

1. Walk every body-level `<w:p>` element of `word/document.xml`.
2. Reconstruct its full text from all `<w:t>` descendants; `.strip()`.
3. If the text matches DATE_TAG_RE:
   a. SAFETY GATE: if the paragraph contains any `<m:oMath>` or `<w:drawing>`
      descendant, SKIP removal for that paragraph and WARN (a real tag never
      contains media — this is defensive; deleting it would break S8-5/S8-6).
   b. Otherwise remove the `<w:p>` from its parent `<w:body>`.
4. Record `tags_removed` (count deleted) and `tags_skipped` (safety-gate skips).

Removal runs FIRST — before header/pill/footer insertion (§13-2) — so all
subsequent position arithmetic operates on the tag-free body.

## S4-3 — Removal outcomes

- `tags_removed ≥ 1` → normal. Reported in §R4.
- `tags_removed == 0` → WARN (not HALT): "No date/session tag paragraphs
  found — document may predate tagging or tags were already removed."
  Formatting proceeds.
- `tags_skipped ≥ 1` → WARN per paragraph with its position, listed in §R4.
- Tags are removed WHEREVER they match — count does not need to equal
  Q_TOTAL (some sources tag only on date change; some tag every question).

---

# §5 — Colored pills (Option C)

Per-question Subject/Topic/Subtopic classification displayed as three colored
pill cells inserted BEFORE each Q-stem. This is the visual signature of PYQ-3
and must look professional and beautiful in the downloaded Word document.

## S5-1 — Pill structure (per question)

For each question Q.n, insert a 1-row, 3-cell Word table immediately before
the Q-stem paragraph. Each cell displays one classification level:

```text
┌─────────────────┬─────────────────┬─────────────────┐
│    [Subject]    │     [Topic]     │   [Subtopic]    │
└─────────────────┴─────────────────┴─────────────────┘
```

The table is inserted as a NEW element — it does not modify or displace the
Q-stem or any other existing content.

## S5-2 — Pill styling

```text
CELL 1 — Subject:
  Background    : Light blue (#D6E4F0)
  Text color    : Dark blue (#1F3864)
  Font          : Arial, 9pt, Bold
  Alignment     : Center
  Padding       : 2pt top/bottom, 4pt left/right

CELL 2 — Topic:
  Background    : Light green (#E2EFDA)
  Text color    : Dark green (#375623)
  Font          : Arial, 9pt, Bold
  Alignment     : Center
  Padding       : 2pt top/bottom, 4pt left/right

CELL 3 — Subtopic:
  Background    : Light amber (#FFF2CC)
  Text color    : Dark amber (#7F6000)
  Font          : Arial, 9pt, Bold
  Alignment     : Center
  Padding       : 2pt top/bottom, 4pt left/right
```

## S5-3 — Pill table properties

```text
Table width     : 100% of page width (between margins)
Cell borders    : NONE (no visible borders — the colored background IS the pill)
Row height      : Auto (fits one line of 9pt text)
Table spacing   : 0pt before the table, 4pt after (tight gap between pill and Q-stem)
Column widths   : Equal thirds (each cell = 33.33% of table width)
Cell shading    : ShadingType.CLEAR with the fill color (NOT ShadingType.SOLID —
                  SOLID renders black in Word)
Vertical align  : Center
```

## S5-4 — Pill data resolution

For each question Q.n, look up `q_to_classification[n]`:
- `subject` → Cell 1 text
- `topic` → Cell 2 text
- `subtopic` → Cell 3 text

If Q.n is missing from the classification map → SKIP the pill for that question
(WARN in the delivery report, do not HALT). The question and its explanation are
still included — only the pill is omitted.

## S5-5 — Pill insertion position

The pill table is inserted IMMEDIATELY BEFORE the Q-stem paragraph. In the
document's XML, this means: find the `<w:p>` element that starts with the
question number pattern (from the document's q_re), and insert the pill table's
`<w:tbl>` element BEFORE that `<w:p>` in the document body.

Order in the formatted document for each question:
```text
[pill table]           ← NEW (PYQ-3 inserts this)
Q.n stem paragraph     ← EXISTING (unchanged)
option paragraphs      ← EXISTING (unchanged)
explanation block      ← EXISTING (unchanged)
```

For Q.1, the pill table is the very first BODY element (v1.3 — the exam
header lives in the page header part, §3, not in the body):
```text
[pill table for Q.1]   ← NEW (§5) — first child of <w:body>
Q.1 stem paragraph     ← EXISTING
...
```

---

# §6 — IFAS page footer (every page, v1.3)

The IFAS branding footer is a Word PAGE FOOTER part — it appears at the
bottom of EVERY page, including the first (D10). It is NOT a body paragraph.

## S6-1 — Footer content and layout

One paragraph, three zones via tab stops (same tab mechanics as S3-1):

```text
LEFT                CENTER                                        RIGHT
ifasonline.com      IFAS – India's No. 1 Exam Preparation Platform  +91-9172266888
```

## S6-2 — Footer styling

```text
Website (LEFT)   : Bold, 9pt, dark blue (#1F3864)
Tagline (CENTER) : Regular, 9pt, dark blue (#1F3864)
Phone (RIGHT)    : Bold, 9pt, dark blue (#1F3864)
Font face        : Arial (new content — same note as S3-2)
Border           : Thin top border, dark blue (#1F3864), sz=6 (0.75pt),
                   space=4 — separates footer from body
Spacing          : before=120 (6pt)
```

No page numbers (D10).

## S6-3 — Footer hardcoded values (D5)

These are COMPANY branding constants, not exam-specific values:
- Website: `ifasonline.com`
- Tagline: `IFAS – India's No. 1 Exam Preparation Platform`
  (v1.3 — en dash `–` U+2013 after IFAS; replaces the former
  "IFAS: India's No. 1 Sarkari Exam Preparation")
- Phone: `+91-9172266888`

Same across all exams, all papers, all sessions. Hardcoded by design.

---

# §7 — Visual polish

Visual improvements applied to the EXISTING content elements. These changes
affect STYLING ONLY — never text content (sole exception: the §7-6 marker
glyph), never OMML math, never images.

## S7-1 — Page margins (if not already set)

```text
Top     : 1.27 cm (0.5 in)
Bottom  : 1.27 cm (0.5 in)
Left    : 1.91 cm (0.75 in)
Right   : 1.91 cm (0.75 in)
```

Compact margins maximize content per page for a student printout.

## S7-2 — Consistent spacing

Ensure paragraph spacing between questions is uniform:
- Before each Q-stem (after the pill table): 8pt
- After the last explanation element of each Q: 12pt
- Between explanation sub-sections (AXIOM → DEDUCTION → etc.): the tag
  header spacing is set by S7-5; sentence spacing stays unchanged
  (preserve the spacing PYQ-1/PYQ-2 set through the engine)

## S7-3 — What is NOT changed

- Font face of ANY text → NEVER changed (preserve whatever font the Row
  file and engine used — including on restyled tag headers: S7-5 sets
  size/color/bold/spacing but never rFonts)
- Bold/italic/underline on question stems, options, and explanation
  SENTENCES → NEVER changed (tag headers, the Correct Answer line, and
  Option/pitfall sub-heads are restyled per S7-4..S7-5 — those paragraphs
  only)
- OMML fractions and math elements → NEVER touched
- Images, drawings, charts, tables → NEVER modified
- Paragraph content → NEVER modified (zero-mutation rule; sole exception:
  the §7-6 marker glyph in tag header paragraphs)

## S7-4 — Explanation tag restyle (v1.2): detection

The engine writes plain explanation blocks (D9). PYQFormat identifies four
classes of paragraph to restyle. Labels and markers are read from
exam_config.json key `explain_labels` / `explain_markers` when present
(non-English exams), else the engine defaults below — matching
explain_engine.py's cfg.labels / cfg.markers. NEVER hardcode beyond these
config-backed defaults.

```text
ENGINE DEFAULT LABELS (cfg.labels):
  correct_answer   → "Correct Answer"
  axiom            → "AXIOM"
  deduction        → "DEDUCTION"
  speed_hack       → "SPEED HACK"
  why_wrong        → "WHY WRONG?"
  common_pitfalls  → "COMMON PITFALLS"
ENGINE DEFAULT MARKERS (cfg.markers):
  axiom ⬛   deduction ⬛   speed_hack ⚡   why_wrong ❌   common_pitfalls ❌
```

CLASS 1 — Tag header paragraph: full stripped text equals
`"<marker> <LABEL>"` or `"<LABEL>"` for one of axiom / deduction /
speed_hack / why_wrong / common_pitfalls. Exact full-paragraph match —
a sentence merely CONTAINING the word "AXIOM" is never touched.

CLASS 2 — Correct Answer line: full stripped text starts with
`"<correct_answer label>:"` (e.g. "Correct Answer: 3"). Prefix match
because the paragraph carries the answer value (possibly OMML for NAT —
the OMML is left untouched; only pPr/run styling is applied).

CLASS 3 — Option / pitfall sub-heads: paragraphs strictly BETWEEN a
why_wrong or common_pitfalls header (CLASS 1) and the next CLASS-1 header,
next Q-stem, or document end, that the engine wrote as sub-headers. Detect
structurally, exactly as explain_engine.py's _is_subheader(): a sub-header
has spacing before > after; sentences have before < after. Fall back to
the engine's textual heuristic only when spacing is absent; when still
uncertain → leave the paragraph unstyled (WARN). Never guess-style a body
sentence.

CLASS 4 — Everything else: never restyled.

## S7-5 — Explanation tag style table (v1.2)

All colors are document-wide design tokens (Appendix A). Font FACE is never
set — existing rFonts preserved. sz values are half-points; w:spacing in
rPr is letter-spacing in twentieths of a point; pBdr left sz=24 is a 3pt
bar; w:ind left=120 twips clears the bar; shd uses w:val="clear" (S13-1
warning: "solid" renders black).

```text
TAG HEADERS (CLASS 1) — common: bold, sz 24 (12pt), letter-spacing 20,
  left bar sz=24 space=8 (color = FG), shd clear fill = BG, ind left 120,
  spacing before=280 after=120, keepNext + keepLines.

  axiom            📘 AXIOM            BG #D6E4F0   FG/bar #1F3864  (blue)
  deduction        🧮 DEDUCTION        BG #E8E2F4   FG/bar #4C3D8F  (purple)
  speed_hack       ⚡ SPEED HACK       BG #FFF2CC   FG/bar #7F6000  (amber)
  why_wrong        ❌ WHY WRONG?       BG #FDECEC   FG/bar #991B1B  (red)
  common_pitfalls  ⚠️ COMMON PITFALLS  BG #FBE5D6   FG/bar #843C0C  (orange)

CORRECT ANSWER (CLASS 2): bold, sz 22 (11pt), letter-spacing 10,
  left bar sz=24 space=8 #375623, shd clear fill #E2EFDA, ind left 120,
  spacing before=240 after=180, keepNext.
  Run color #375623 applied to TEXT runs only — OMML answer values (NAT)
  keep their own math run properties untouched.

SUB-HEADS (CLASS 3): bold, sz 22 (11pt), keepNext + keepLines. Run color:
  #7F1D1D under a why_wrong header, #7A3708 under a common_pitfalls header.
  SPACING PRESERVED AS-IS — the engine's before>after relation on
  sub-heads is a structural invariant (_is_subheader) and must survive.
  No shading, no bar — sub-heads stay lighter than section headers.

BODY SENTENCES (CLASS 4): untouched — color, size, spacing, everything.
```

## S7-6 — Marker glyph substitution (v1.2, D9)

The ONLY text change in this spec. Applied ONLY to CLASS-1 tag header
paragraphs whose full text exactly equals `"<old_marker> <LABEL>"`:

```text
⬛ AXIOM            →  📘 AXIOM
⬛ DEDUCTION        →  🧮 DEDUCTION
❌ COMMON PITFALLS  →  ⚠️ COMMON PITFALLS
⚡ SPEED HACK       →  (unchanged)
❌ WHY WRONG?       →  (unchanged)
```

Rules:
1. Substitution replaces the single leading marker glyph in the header's
   run text; the label word(s) and everything else are untouched.
2. If a header carries no marker, an unexpected marker, or already carries
   the new glyph (engine re-run with updated markers) → NO substitution;
   restyle still applies. WARN only when the marker is unexpected.
3. Word renders emoji via the platform color-emoji font regardless of run
   color — the header's color identity is carried by the label text and
   the band/bar, so glyph color variance across platforms is acceptable.
4. Every substitution performed is recorded as
   (paragraph position, old_text, new_text) for S8-8 verification and the
   §R6 report.

---

# §8 — Content integrity verification

After all visual elements are inserted and styling is applied, PYQ-3 verifies
that the content is intact. This is the LAST check before delivery.

## S8-1 — Question count match

Count the Q-stems in the output document and verify it equals Q_TOTAL from the
input document. A mismatch means PYQ-3 accidentally displaced or deleted a
question paragraph — HARD STOP.

## S8-2 — Pill count match

Count the pill tables in the output document. Expected: one per question that
has a classification entry (may be fewer than Q_TOTAL if some Qs are missing
from the map). Verify: pill_count == len(q_to_classification ∩ {1..Q_TOTAL}).

## S8-3 — Header and footer parts check (v1.3)

Verify in the output package:
1. The header and footer parts exist (e.g. word/header1.xml,
   word/footer1.xml) and contain the exact expected texts: exam name,
   date · session, "IFAS"; and "ifasonline.com", the D5 tagline,
   "+91-9172266888".
2. word/_rels/document.xml.rels contains relationships to both parts, and
   [Content_Types].xml declares their content types.
3. EVERY `<w:sectPr>` in word/document.xml carries `<w:headerReference>`
   and `<w:footerReference>` for ALL THREE types (default, even, first)
   pointing to those relationships (S13-6).
4. The BODY's first element is Q.1's pill table and its last element is
   the final explanation paragraph — no header/footer paragraphs in the
   body.
Any failure — HARD STOP.

## S8-4 — Content byte-identity spot-check

For a sample of questions (first 3, last 3, and 3 random), extract the Q-stem
text from both the input and output documents and confirm they are byte-identical.
This is a fast early-fail check; S8-8 performs the full-document text-stream
verification.

## S8-5 — OMML survival check

Count the `<m:oMath>` elements in the input and output. They must be equal —
PYQ-3 never creates, modifies, or removes OMML. A mismatch means the XML
manipulation accidentally corrupted a math element — HARD STOP.

## S8-6 — Image survival check

Count the `<w:drawing>` elements in the input and output. They must be equal.
A mismatch means an image was lost or duplicated — HARD STOP.

NOTE (v1.1): S8-5 and S8-6 remain exact input==output equality checks. Tag
removal (§4) cannot affect them because the S4-2 safety gate refuses to delete
any paragraph containing OMML or drawings.

## S8-7 — Date/session tag absence check (v1.1)

Count the body-level paragraphs in the OUTPUT whose full text matches
DATE_TAG_RE (§4). Expected: exactly `tags_skipped` (0 in the normal case).
Additionally verify: `input_tag_count == tags_removed + tags_skipped`.
Any other result means removal missed a tag or the accounting is wrong —
HARD STOP.

## S8-8 — Full text-stream integrity check (v1.2)

The strongest check in the spec — full-document, not a spot-check:

1. Extract the ordered list of paragraph texts from the INPUT, minus the
   date/session tag paragraphs removed per §4 accounting.
2. Extract the ordered list of paragraph texts from the OUTPUT body, minus
   the pill tables PYQFormat inserted (v1.3: pills are the only body
   insertion — header/footer live in separate parts and never enter this
   comparison).
3. The two lists must be identical in length and content, where the ONLY
   permitted differences are the exact (position, old_text, new_text)
   marker substitutions recorded in S7-6.

Any other difference — one character, anywhere — means text was mutated:
HARD STOP. This check makes the D9 guarantee ("the marker glyph is the
only text change") machine-verified rather than asserted.

---

# §9 — Delivery

PYQ-3 delivers in a single response (no batching):

1. All integrity checks (§8) pass.
2. Present `[ExamCode]_[date]_[session]_PYQ_Formatted.docx` via present_files.
3. Print the delivery report (§10).
4. Render the post-delivery footer per Framework_DeliveryFooter.md:
   - F2 (step-complete, GREEN) — PYQ-3 delivers once, always complete.
   - File badge: `📁 Use locally` for PYQ_Formatted.docx.
   - Next-step reference: "This is the student-facing document — ready for
     distribution. For portal delivery, run PYQ-4 (PYQDeliver) separately
     in a new chat (PYQ-4 takes PYQ-2 output directly, not this file)."

---

# §10 — Delivery report

Printed in chat after present_files. Brief and skimmable:

- **§R1 — Scope.** Exam, paper (date, session), Q_TOTAL.
- **§R2 — Header.** Page header as rendered (left / center / right zones),
  confirmed on every page via the S8-3 parts check.
- **§R3 — Pills.** pill_count of Q_TOTAL questions have pills. Any missing
  classifications listed by Q number.
- **§R4 — Tags removed.** tags_removed date/session tag paragraphs removed
  (§4). Any safety-gate skips (tags_skipped) listed with position and reason.
  "0 removed" shown with the S4-3 WARN when no tags were found.
- **§R5 — Tag styling.** Counts of restyled paragraphs per class: tag
  headers by tag, Correct Answer lines, sub-heads. Marker substitutions
  performed (S7-6). Any detection WARNs (unstyled uncertain sub-heads,
  unexpected markers) listed.
- **§R6 — Footer.** Page footer as rendered (website / tagline / phone),
  confirmed on every page via the S8-3 parts check.
- **§R7 — Integrity.** Q-count match, OMML count match, image count match,
  tag absence (S8-7), text-stream integrity (S8-8), spot-check results.
  All must show PASS.
- **§R8 — Note.** "This is the student-facing document. Review in Microsoft
  Word (OMML renders correctly only in Word). For portal delivery, run PYQ-4
  (PYQDeliver) in a new chat — it takes PYQ-2 output directly."

---

# §11 — Definition of done

PYQ-3 is done when **all** hold:

1. The input document opened successfully and Q_TOTAL was determined.
2. The q_to_classification map was loaded with coverage for the paper.
3. The exam page header appears on every page, correctly formatted with
   its three zones (§3, S8-3).
4. Every question with a classification entry has a colored pill table
   immediately before its Q-stem (§5).
5. The IFAS page footer appears on every page with the D5 tagline
   "IFAS – India's No. 1 Exam Preparation Platform" (§6, S8-3).
6. Every date/session tag paragraph has been removed (§4) — none remain in
   the output (S8-7), barring reported safety-gate skips.
7. Explanation tags are restyled per S7-4..S7-5 and marker glyphs
   substituted per S7-6, with counts reported in §R5.
8. ZERO content was changed — no question, option, explanation, OMML, or
   image was modified (zero-mutation rule); the tag paragraphs are the ONLY
   removed elements and the S7-6 marker glyphs the ONLY changed characters.
9. All integrity checks (§8) pass: Q-count, pill-count, header/footer
   parts, content spot-check, OMML count, image count, tag absence,
   text-stream integrity.
10. The output is a valid .docx that opens clean in Microsoft Word.
11. Delivered via present_files with the delivery report and footer.

**Hard invariants (never violated):**

- No text content is modified (zero-mutation rule) — sole exception: the
  S7-6 marker glyph in exact-match tag header paragraphs, machine-verified
  by S8-8's full text-stream comparison.
- The date/session tag paragraphs (§4) are the ONLY elements ever removed —
  each verified media-free before deletion. Nothing else is deleted.
- Restyling (S7-4..S7-5) touches ONLY the four detected classes; body
  sentences are never restyled, and font FACE is never changed anywhere.
- No OMML element is created, modified, or removed.
- No image or drawing is modified, moved, or removed.
- The pill table is the ONLY new element between questions.
- The pill tables are the ONLY new elements in the body; the exam header
  and IFAS footer live exclusively in page header/footer parts (D10) and
  never appear as body paragraphs.
- No exam-specific value is hardcoded (exam-agnostic guarantee).
  The only hardcoded values are IFAS branding constants (D5).

---

# §12 — Edge cases

1. **q_to_classification map missing entirely** → HARD STOP with message
   (§0). Cannot generate pills without classification data.

2. **Partial map (covers 90 of 100 Qs)** → WARN per missing Q. Pills
   inserted for the 90 covered questions; the 10 uncovered questions
   appear without pills (question and explanation still present). Report
   lists the missing Q numbers.

3. **exam_config.json missing** → WARN (not HALT). Use ExamCode as the
   display name in the header. Everything else works.

4. **Input is PYQ-1 output (not PYQ-2)** → ACCEPTED (§0). PYQ-3 does not
   require the audit — it formats whatever it receives. A WARN is printed
   noting the document has not been audited.

5. **Document has 0 questions** → HARD STOP. Nothing to format.

6. **Very long subtopic names (>50 chars)** → The pill cell auto-wraps.
   The table row height increases to fit. No truncation — the full name
   is always shown.

7. **Document with images/OMML** → All preserved. PYQ-3 inserts new
   elements only; existing elements are untouched (§7-3, §8-5, §8-6).

8. **Multi-session exam (same date, 3 shifts)** → Each session is a
   separate PYQFormat run. The filename includes the session identifier.

9. **Document already formatted (re-run)** → The output filename differs
   from the input filename, so re-running produces a fresh formatted doc
   from the original input. If someone attaches the _PYQ_Formatted.docx
   by mistake, the spec detects it (filename check) and warns: "This
   appears to already be a formatted document. Attach the
   _PYQ_Explanation_Complete.docx instead."

10. **No date/session tags in the document** → WARN (not HALT, S4-3).
    The document may predate tagging or use a non-standard label the
    anchored regex does not match. Formatting proceeds; §R4 reports
    "0 removed" with the WARN.

11. **Date-label text inline inside a stem or explanation** → NOT removed.
    DATE_TAG_RE is anchored to the full paragraph text (§4-1) — partial
    deletion is structurally impossible. Only standalone tag paragraphs
    are removed.

12. **Tag paragraph containing OMML or a drawing** → removal SKIPPED for
    that paragraph, WARN with position (S4-2 safety gate). S8-7 accounts
    for it via tags_skipped; S8-5/S8-6 equality checks stay intact.

13. **Non-English exam (custom labels/markers)** → labels and markers read
    from exam_config.json `explain_labels` / `explain_markers` (S7-4). If
    absent and the English defaults match nothing → WARN "no explanation
    tag headers detected — restyle skipped"; formatting proceeds without
    the tag restyle. Never HALT over styling.

14. **Header already carries the new glyph** (engine re-run with updated
    markers, or PYQFormat re-run) → no substitution (S7-6 rule 2), restyle
    applies normally, no WARN.

15. **SPEED HACK absent** → normal; the block is optional in the engine.
    Restyle whatever headers exist — no completeness requirement on tags.

16. **Sub-head detection uncertain** (spacing absent AND textual heuristic
    inconclusive) → paragraph left unstyled, WARN in §R5 (S7-4 CLASS 3).
    An unstyled sub-head is cosmetically imperfect; a mis-styled body
    sentence is a defect. Choose the former.

17. **NAT Correct Answer with OMML value** → the paragraph band/bar/bold
    is applied via pPr; run color applies to TEXT runs only, OMML math
    runs untouched (S7-5). S8-5 still requires exact OMML count equality.

18. **A body sentence that happens to start with "Correct Answer:"** →
    styled as CLASS 2 only if the paragraph is positioned as the engine
    writes it (immediately after the option block / before the first tag
    header). Elsewhere → left alone, WARN. Positional context guards the
    prefix match.

19. **Input already has header/footer parts** (rare — engine output is
    plain, but python-docx templates can carry empty defaults) → existing
    header/footer parts and their sectPr references are REPLACED by
    PYQFormat's (S13-6). The replaced parts are document chrome, not
    certified content — the zero-mutation rule protects the body, and
    S8-8 proves the body text stream is intact.

20. **Multiple `<w:sectPr>` elements** (multi-section body) → the
    header/footer references are added to EVERY sectPr, including the
    body-level trailing sectPr and any paragraph-level ones. S8-3 rule 3
    verifies all of them.

21. **`evenAndOddHeaders` or `titlePg` present in the input** → harmless
    by construction: references are registered for default, even, and
    first types pointing to the same parts (D10), so every page renders
    identically without editing settings.xml.

---

# §13 — Implementation notes

## S13-1 — Pill table XML structure

The pill table is built as a `<w:tbl>` element in the document XML with:
- `<w:tblPr>`: table width 100%, layout fixed, no borders
- `<w:tblGrid>`: 3 `<w:gridCol>` of equal width
- `<w:tr>`: single row with 3 `<w:tc>` cells
- Each `<w:tc>`: cell properties (shading with fill color, vertical alignment
  center, cell margins) + a single `<w:p>` with the classification text

Cell shading uses `<w:shd w:val="clear" w:fill="[HEX]"/>` — the `clear` val
is critical (Word renders `solid` as opaque black).

## S13-2 — Insertion strategy

The document is processed via `unzip → XML edit → zip`:

1. Unzip the input .docx to a working directory
2. Parse `word/document.xml` as XML
3. REMOVE date/session tag paragraphs (§4) — every body-level `<w:p>` whose
   full text matches DATE_TAG_RE and passes the media-free safety gate.
   This runs FIRST so all subsequent position arithmetic is tag-free.
4. RESTYLE explanation tags (S7-4..S7-6) — detect the four classes, apply
   pPr/rPr styling in place, substitute marker glyphs, record every
   substitution for S8-8.
5. Find each Q-stem `<w:p>` by matching the question regex pattern
6. For each Q-stem found (in reverse order to preserve positions):
   - Build the pill `<w:tbl>` element
   - Insert it BEFORE the Q-stem `<w:p>` in the parent `<w:body>`
7. WIRE the page header/footer parts (S13-6) — create header1.xml /
   footer1.xml, register relationships and content types, add references
   to every sectPr.
8. Re-zip to the output .docx

Processing in REVERSE ORDER (Q.N → Q.1) ensures that inserting elements
for Q.5 doesn't shift the positions of Q.6-Q.N (which were already processed).

## S13-3 — Namespace preservation

When editing the XML, ALL existing namespace declarations on the root element
must be preserved exactly. No `cleanup_namespaces()` — this strips xmlns
declarations that `mc:Ignorable` and drawing content reference, causing Word
to show "unreadable content" errors (learned from MockDeliver v1.3).

## S13-4 — Why not python-docx for insertion

python-docx can READ the document structure but has limitations for INSERTING
tables at arbitrary positions in an existing document while preserving all
existing OMML, drawings, and complex formatting. Direct XML manipulation gives
full control over insertion position and guarantees zero mutation of existing
elements. The `unzip → edit → zip` approach is the same one MockDeliver uses
for tag insertion.

## S13-5 — Restyle mechanics (v1.2)

Restyling modifies elements IN PLACE — no paragraph is recreated:

- pPr: create it if absent; add/replace `<w:pBdr>` (left bar), `<w:shd>`
  (w:val="clear" — S13-1 warning applies), `<w:ind>`, `<w:spacing>`,
  `<w:keepNext>`, `<w:keepLines>`. Existing pPr children not listed in
  S7-5 are preserved.
- rPr on each affected run: add/replace `<w:b>`, `<w:color>`, `<w:sz>`/
  `<w:szCs>`, `<w:spacing>` (letter-spacing). NEVER add or modify
  `<w:rFonts>` — font face preservation is a hard invariant (S7-3).
- CLASS-2 (Correct Answer) paragraphs: iterate runs; style `<w:r>` runs
  containing `<w:t>`; skip `<m:oMath>` children entirely.
- Marker substitution (S7-6): edit the text of the first `<w:t>` in the
  header paragraph — replace the single leading glyph, preserving any
  `xml:space="preserve"` attribute and all following characters.
- Sub-head spacing (CLASS 3) is read but never written (S7-5).

## S13-6 — Page header/footer part wiring (v1.3)

The mechanism the reference documents use, made exam-agnostic:

1. **Parts.** Create `word/headerN.xml` (`<w:hdr>`) and `word/footerN.xml`
   (`<w:ftr>`) where N is the lowest positive integer not already used by
   an existing part (collision-safe). Each contains the single three-zone
   paragraph of S3-1 / S6-1: left run, `<w:r><w:tab/></w:r>`, center run,
   `<w:r><w:tab/></w:r>`, right run, with `<w:tabs>` defining a center tab
   at (page_width − left_margin − right_margin) / 2 and a right tab at
   (page_width − left_margin − right_margin), both computed from the
   section's `<w:pgSz>` / `<w:pgMar>` at runtime. `xml:space="preserve"`
   on every `<w:t>`.
2. **Relationships.** Append to `word/_rels/document.xml.rels` two new
   `<Relationship>` entries (next free rIds) with types
   `.../header` and `.../footer` targeting the parts.
3. **Content types.** Add `<Override>` entries to `[Content_Types].xml`
   for both parts (wordprocessingml header/footer content types).
4. **References.** In EVERY `<w:sectPr>`: remove any existing
   `<w:headerReference>`/`<w:footerReference>` (edge case 19), then add
   references for ALL THREE `w:type` values — `default`, `even`, `first`
   — all pointing to the new parts (D10). Insert them at the head of
   sectPr (schema order: header/footer references precede pgSz).
5. **Namespaces.** The parts declare the full namespace set the document
   root uses (S13-3 discipline applies to new parts too).

Header/footer parts contain no OMML and no drawings, so S8-5/S8-6 input==
output equality is unaffected by construction.

---

# APPENDIX A — Color reference

```text
PILL COLORS (named for easy reference in code):
  PILL_SUBJECT_BG   = "#D6E4F0"  (light blue)
  PILL_SUBJECT_FG   = "#1F3864"  (dark blue)
  PILL_TOPIC_BG     = "#E2EFDA"  (light green)
  PILL_TOPIC_FG     = "#375623"  (dark green)
  PILL_SUBTOPIC_BG  = "#FFF2CC"  (light amber)
  PILL_SUBTOPIC_FG  = "#7F6000"  (dark amber)

HEADER/FOOTER ACCENT = "#1F3864" (dark blue — matches Subject pill foreground)

EXPLANATION TAG COLORS (v1.2 — named for easy reference in code):
  TAG_CA_BG        = "#E2EFDA"  TAG_CA_FG        = "#375623"  (green — success)
  TAG_AXIOM_BG     = "#D6E4F0"  TAG_AXIOM_FG     = "#1F3864"  (blue)
  TAG_DEDUCTION_BG = "#E8E2F4"  TAG_DEDUCTION_FG = "#4C3D8F"  (purple)
  TAG_SPEED_BG     = "#FFF2CC"  TAG_SPEED_FG     = "#7F6000"  (amber)
  TAG_WRONG_BG     = "#FDECEC"  TAG_WRONG_FG     = "#991B1B"  (red)
  TAG_PITFALL_BG   = "#FBE5D6"  TAG_PITFALL_FG   = "#843C0C"  (orange)
  SUBHEAD_WRONG_FG   = "#7F1D1D"  (Option sub-heads under WHY WRONG?)
  SUBHEAD_PITFALL_FG = "#7A3708"  (value sub-heads under COMMON PITFALLS)

MARKER GLYPHS (v1.2): axiom 📘  deduction 🧮  speed_hack ⚡
                      why_wrong ❌  common_pitfalls ⚠️

These are design tokens, not exam-specific values. They are the same
across all exams and all papers. Note the deliberate reuse: AXIOM shares
the Subject pill family, SPEED HACK the Subtopic pill family, and the
Correct Answer band the Topic pill family — one palette document-wide.
```

---

**End of Framework_PYQFormat.md (v1.3)**
