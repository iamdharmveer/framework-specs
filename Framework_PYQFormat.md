# Framework_PYQFormat v1.5 — Universal PYQ Student Document Formatter
# v1.5 — 2026-08-09 — PYQExplainAudit (PYQ-2) RETIRED. PYQ-3 now takes PYQ-1's
#   _PYQ_Explanation.docx as its STANDARD input (a legacy _Complete.docx is still
#   accepted, unchanged, but is no longer produced). q_to_classification is read from
#   pyq_explain_progress.json as the primary sidecar. No runtime behaviour changes —
#   PYQ-3 never audited; it formats whatever it is given. Edits retire the "certified by
#   PYQ-2" framing (the input is now producer-certified by PYQ-1's self-audit, not independently
#   audited) and the PYQ-2 cross-references. Touched: PURPOSE, ZERO-MUTATION rationale,
#   §0/§1 input contract + map priority, §4, S7-2, §9/§10 notes, §12 edge cases.
# v1.4.2 — 2026-07-31 — CHANGELOG RELOCATED (history-only; zero rule change).
#   173 lines of version history and superseded companion blocks moved
#   verbatim to CHANGELOG.md 'ARCHIVE — Framework_PYQFormat'. The current companion block, the
#   v1.4.1 entry, and all structural notes remain in-file. Body byte-untouched.
# [ExamCode] project | PYQ-3 (PYQFormat) | Exam-agnostic
#
# v1.4.1 — 2026-07-25 — END-OF-FILE VERSION MARKER CORRECTED. The trailing sentinel still
#   read v1.3, several versions behind the header, so the last line of the file contradicted
#   the first. Documentation only — not one line of behaviour changes. It went unnoticed
#   because BOTH integrity tools were structurally blind to it: validate_framework_md.py
#   Check C recognised only the '# END OF <name> vN' sentinel form and skipped the
#   comparison entirely for the '**End of <name>.md (vN)**' form used here, while
#   audit_specs_ext.py check_z_version reads the header from line 1 only. Check C now
#   recognises both forms (validate_framework_md.py v3.1), so this cannot drift silently
#   again.
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Transform a content-complete PYQ explanation document into a polished
#   student-facing download. The input is PYQ-1's _PYQ_Explanation.docx
#   (v1.5: PYQ-2 PYQExplainAudit is retired, so PYQ-1's output is the final
#   explanation document; a legacy _Complete.docx is also accepted). PYQ-3's
#   job is purely visual: make it look beautiful for the student who downloads
#   it. No content judgement, no re-derivation, no quality gate — PYQ-3 never
#   audits; it presents whatever it is given.

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
#     PYQ-3  PYQFormat       → _PYQ_Formatted.docx   ← THIS STEP
#     PYQ-4  PYQDeliver      → _PYQ_Final.docx        (portal)
#     (PYQ-2 PYQExplainAudit RETIRED in v1.5. PYQ-3 and PYQ-4 are INDEPENDENT —
#      both take PYQ-1's _PYQ_Explanation.docx directly.)

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
input is PYQ-1's explanation content — producer-certified by PYQ-1's own self-audit
(v1.5: PYQ-2 is retired, so there is no independent completion gate). PYQ-3
preserves that content byte-for-byte by touching NOTHING but the visual elements
named above.

---

# §0 — Input / output contract

**Inputs:**

1. `[ExamCode]_[date]_[session]_PYQ_Explanation.docx` — the PYQ-1 explanation
   document. Attached by user. This is the STANDARD input (v1.5: PYQ-2 PYQExplainAudit
   is retired, so PYQ-1's output is the pipeline's final explanation document).
   ALSO ACCEPTS (legacy): `_PYQ_Explanation_Complete.docx` — a pre-v1.5 PYQ-2 audited
   document. Still a valid explanation doc; accepted unchanged. This format is no longer
   produced. If both are attached, use whichever the user names; absent that, prefer
   `_PYQ_Explanation.docx`.

2. `exam_config.json` — in project knowledge. Provides `exam_name` for the header.

3. `q_to_classification` map — the per-question {subject, topic, subtopic,
   subtopic_id} mapping. Loaded from ONE of these sources (in priority order):
   a. `pyq_explain_progress.json` sidecar (PYQ-1's progress file — the standard source)
   b. `pyq_audit_progress.json` sidecar (LEGACY — only if a pre-v1.5 PYQ-2 run left one)
   c. Attached by user as a separate JSON file
   If no classification map is found → HARD STOP:
     "q_to_classification map not found. Run PYQExplain first, or attach
      pyq_explain_progress.json / pyq_audit_progress.json."

NOT REQUIRED (PYQ-3 adds no content):
  ✗ explain_engine.py — no explanations written or read by this step
  ✗ (no audit performed by this step; PYQ-2 PYQExplainAudit and its gate are retired)
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

Attach: the PYQ-1 output `_PYQ_Explanation.docx` (a legacy PYQ-2 `_Complete.docx` is also accepted).

Everything is derived from the attachment and project knowledge:

1. **ExamCode**: derived from project knowledge files (any `[ExamCode]_*` file
   in `/mnt/project/`). If ambiguous → HARD STOP.

2. **Date + Session**: parsed from the attached filename. The filename follows
   the pattern `[ExamCode]_[DD-Mon-YYYY]_[session]_PYQ_Explanation[_Complete].docx`.
   If the filename cannot be parsed → HARD STOP: "Cannot parse date/session from
   the attached filename."

3. **Input document**: the attached file. Accept either:
   - `_PYQ_Explanation.docx` (PYQ-1 — standard)
   - `_PYQ_Explanation_Complete.docx` (legacy PYQ-2 audited doc — accepted, no WARN)
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
through PYQExplain unchanged:

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
  (preserve the spacing PYQ-1 set through the engine)

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

## S8-9 — Package validity gate (v1.4) — HARD STOP

⚠️ **S8-1..S8-8 verify CONTENT FIDELITY. None of them verifies PACKAGE
VALIDITY.** These are independent properties, and the v1.3 failure lived
entirely in the second one. A `document.xml` whose `mc:Ignorable` names
undeclared prefixes is still well-formed XML: it parses cleanly in both stdlib
ET and lxml, so the Q-count, the OMML and drawing counts, and even S8-8's
full text-stream comparison all PASS — on a file Word refuses to open. §11
item 10 requires "a valid .docx that opens clean in Microsoft Word"; S8-9 is
the check that makes that requirement real instead of asserted.

This gate is the layer that generalises. S13-3 and S13-7 fix two known defect
classes; S8-9 catches those **and** any serialization defect not yet
encountered, which is what a permanent guarantee across ~200 exams requires.

Run on the DELIVERED file, after every other check:

```python
import os
import subprocess

VALIDATOR = '/mnt/skills/public/docx/scripts/office/validate.py'


def gate_s8_9(input_docx, output_docx, input_document_xml, output_document_xml):
    """S8-9 — package validity. Returns 'validated' or 'degraded'; else raises.

    The two *_document_xml arguments are the raw bytes of word/document.xml
    from each package, used only by the fallback path.
    """
    if os.path.exists(VALIDATOR):
        result = subprocess.run(
            ['python3', VALIDATOR, output_docx, '--original', input_docx],
            capture_output=True, text=True)
        if result.returncode != 0:
            print('S8-9 FAIL — output package is not valid OOXML:')
            print(result.stdout)
            print(result.stderr)
            raise SystemExit('S8-9 HARD STOP — do not deliver this file.')
        return 'validated'

    # Validator absent: fall back to the namespace rules only. This does NOT
    # cover schema ordering, so the run is UNVERIFIED for package validity —
    # report it as such in §R7 rather than as a pass.
    failures = namespace_selfcheck(input_document_xml, output_document_xml)
    if failures:
        print('S8-9 FAIL (fallback path) — namespace integrity broken:')
        for f in failures:
            print('  ' + f)
        raise SystemExit('S8-9 HARD STOP — do not deliver this file.')
    print('S8-9 DEGRADED — validator unavailable; namespace rules pass but '
          'schema ordering is UNVERIFIED. Report this in §R7.')
    return 'degraded'
```

`--original` is REQUIRED. It reports only errors that are **new** relative to
the input, so pre-existing quirks in a given exam's source document (a
frequent occurrence across 200 exams with heterogeneous provenance) do not
block delivery, while anything PYQFormat introduced does.

What it catches, **measured on the failing v1.3 artefact** (input: 0 errors;
output: 812 reported errors + 4 undeclared namespaces, all introduced by
PYQFormat):

| Defect | Reported as | Count |
|---|---|---|
| Namespace loss / undeclared `mc:Ignorable` prefix | `Namespace 'w14' in Ignorable but not declared` | 4 |
| `pPr` order — `pBdr` after `ind`/`spacing` | `Element '…pBdr': This element is not expected` | 244 + 2 |
| `tcPr` order — `tcMar` after `vAlign` | `Element '…tcMar': This element is not expected` | 180 |
| `pPr` order — `spacing` after `jc` | `Element '…spacing': This element is not expected` | 180 |
| `pPr` order — `keepNext` after `spacing`/`ind` | `Element '…keepNext': This element is not expected` | 146 |
| `tblPr` order — `tblBorders` after `tblLayout` | `Element '…tblBorders': This element is not expected` | 60 |

⚠️ **Validate EVERY part, and require ZERO — not "fewer".** The two errors
above marked `+ 2` were in `header1.xml` and `footer1.xml`, not the body. And
because a rejected parent is not descended into, a passing-looking count can
conceal nested faults: repairing this artefact required reordering **991**
elements although only **812** errors were reported. Re-run the gate after
every fix until it reports zero; newly surfaced errors are expected.

**Fallback.** If the validator is unavailable in the runtime, run
`namespace_selfcheck()` (S13-3) on input vs output `document.xml` and treat a
non-empty result as the same HARD STOP. The fallback covers the namespace
class only — it does not replace the schema check, and its use must be
reported in §R7.

**LibreOffice is not a substitute.** A successful `soffice` conversion is
necessary but NOT sufficient: LibreOffice opens files Word rejects. Confirmed
on this artefact — it rendered acceptably while Word refused it. Rendering is
a visual check, not a validity check.

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
     in a new chat (PYQ-4 takes PYQ-1 output directly, not this file)."

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
  tag absence (S8-7), text-stream integrity (S8-8), spot-check results,
  and **package validity (S8-9)** — report the validator verdict explicitly,
  plus the input→output namespace prefix delta (expected: none lost). If the
  S13-3 fallback self-check was used instead of the validator, say so here.
  All must show PASS.
- **§R8 — Note.** "This is the student-facing document. Review in Microsoft
  Word (OMML renders correctly only in Word). For portal delivery, run PYQ-4
  (PYQDeliver) in a new chat — it takes PYQ-1 output directly."

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
   text-stream integrity, and package validity (S8-9).
10. The output is a valid .docx that opens clean in Microsoft Word —
    machine-verified by S8-9, not assumed. Items 1–9 establish that the
    CONTENT is intact; only S8-9 establishes that the PACKAGE is valid.
    A file can satisfy every other item on this list and still fail to open.
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

4. **Input is PYQ-1 output** → the NORMAL input (v1.5: PYQ-2 retired). PYQ-3 does
   not require any audit — it formats whatever it receives, with no WARN. A legacy
   `_PYQ_Explanation_Complete.docx` is equally accepted.

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
   _PYQ_Explanation.docx instead."

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

⚠️ **SCHEMA ORDER (v1.4).** `tblPr`, `tcPr` and `tcMar` are `xsd:sequence`
types — child order is enforced and a violation triggers Word's "unreadable
content" error. Build every one of them through `set_child()` (S13-7):

- `tblPr`: `tblW` → `tblBorders` → `tblLayout` (NOT `tblW` → `tblLayout` →
  `tblBorders`, which is the natural writing order and is invalid).
- `tcPr`: `tcW` → `shd` → `tcMar` → `vAlign`.
- `tcMar`: `top` → `start` → `left` → `bottom` → `end` → `right`.

Note on `tcMar` naming: **both** `<w:start>/<w:end>` and `<w:left>/<w:right>`
are valid — the ISO-IEC29500-4:2016 schema declares all six children, and
`left`/`right` are what Word itself writes. Do NOT "modernise" existing
`left`/`right` elements to `start`/`end`, and do NOT drop them from the order
table: an order table missing them relocates them and corrupts a document that
was valid on input. When creating new cell margins, either pair is acceptable;
only the sequence matters. The same applies to `<w:tblCellMar>`.

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

## S13-3 — Namespace preservation (v1.4 — MANDATORY MECHANISM)

⚠️ **This section is a hard requirement, not guidance.** The v1.3 defect
occurred because the previous text warned against `cleanup_namespaces()` — an
**lxml-only** function — without mandating lxml. The run used stdlib
`xml.etree.ElementTree`, where that function does not exist, so the warning
was satisfied while the file was being corrupted.

**RULE 1 — lxml is MANDATORY.** All reading and writing of existing OOXML
parts (`word/document.xml`, `headerN.xml`, `footerN.xml`,
`word/_rels/document.xml.rels`, `[Content_Types].xml`) uses `lxml.etree`.

**RULE 2 — `xml.etree.ElementTree` is FORBIDDEN** for editing existing parts.
It cannot preserve the namespace set even when used carefully. Measured on a
Word-realistic root carrying 20 prefixes with
`mc:Ignorable="w14 w15 w16se wp14"`:

| Approach | Prefixes preserved | Lost |
|---|---|---|
| stdlib ET, naive | 0 (all rewritten to `ns0`…`ns5`) | **20** |
| stdlib ET + `register_namespace()` for every prefix | 6 | **14** — incl. `w15`, `w16se`, `wp14` |
| **lxml, no `cleanup_namespaces()`** | **20** | **0** |

`register_namespace()` is NOT a fix: stdlib ET emits a declaration only for a
prefix used as an element/attribute *tag* prefix, and drops those referenced
only inside attribute values — which is exactly what `mc:Ignorable` is.

**RULE 3 — `etree.cleanup_namespaces()` is FORBIDDEN** (the MockDeliver v1.3
lesson). lxml preserves every declaration on the parsed root as long as this
is never called.

**RULE 4 — the namespace set is DISCOVERED, never hardcoded.** It varies by
exam: documents without drawings lack `a`/`a14`/`pic`; older templates carry
VML (`v`, `o`, `w10`); newer Word versions add `w16cid`, `w16cex`. Any
hardcoded list fails on the next exam.

**RULE 5 — new parts must declare every prefix they actually use.** `headerN.xml`
/ `footerN.xml` created by S13-6 must declare each prefix appearing in their
own content, and — if they carry an `mc:Ignorable` attribute — every token in
it. They do NOT need the document root's full prefix set; over-declaring is
harmless but unnecessary. (Verified on a real artefact: header/footer parts
declaring only `w`, `r`, `m` and carrying no `mc:Ignorable` validate cleanly.)
Build them with lxml like every other part.

⚠️ **RULE 6 — every part written is in scope, not just `document.xml`.** On the
failing artefact, `header1.xml` and `footer1.xml` each carried their own schema
violation. Apply S13-3 and S13-7 to every part the step creates or edits, and
validate all of them (S8-9).

### Why Word rejects what Python accepts

`mc:Ignorable` (ECMA-376 Part 3, Markup Compatibility) holds a whitespace-
delimited list of namespace **prefixes** that the MCE processor must resolve.
An XML parser has no reason to interpret an attribute's *value*, so a file
whose `mc:Ignorable` names undeclared prefixes is still well-formed XML and
parses cleanly in both stdlib ET and lxml. Word's MCE preprocessor resolves
it, fails, and reports unreadable content. This is precisely why the defect is
invisible to every content check in §8 and why S8-9 exists.

### Mandated read/write pattern

```python
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def w(tag):
    """Qualify a bare WordprocessingML tag name."""
    return '{%s}%s' % (W, tag)


def ln(el):
    """Local name of an element, namespace stripped."""
    t = el.tag
    return t.split('}')[-1] if isinstance(t, str) and '}' in t else t


def parse_part(path):
    """Parse an existing OOXML part. lxml keeps every root xmlns declaration."""
    return etree.parse(path)


def write_part(tree_or_root, path):
    """Serialize a part with all namespace declarations intact.

    NEVER call etree.cleanup_namespaces() anywhere in this pipeline.
    """
    root = tree_or_root.getroot() if hasattr(tree_or_root, 'getroot') else tree_or_root
    data = etree.tostring(root, xml_declaration=True, encoding='UTF-8',
                          standalone=True)
    data = data.replace(
        b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>",
        b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    with open(path, 'wb') as fh:
        fh.write(data)
```

### In-spec namespace self-check (runs before S8-9)

Reproduces the two rules the external validator enforces, so the pipeline
fails loudly even if the validator is unavailable:

```python
import re


def namespace_selfcheck(input_xml_bytes, output_xml_bytes):
    """Return a list of failures; empty list means the namespace set is safe.

    (a) every prefix named in mc:Ignorable must be declared as xmlns:<prefix>
    (b) the output prefix set must be a superset of the input prefix set
    """
    failures = []
    src = input_xml_bytes.decode('utf-8', 'replace')
    out = output_xml_bytes.decode('utf-8', 'replace')

    out_prefixes = set(re.findall(r'xmlns:([A-Za-z0-9_.-]+)=', out))
    in_prefixes = set(re.findall(r'xmlns:([A-Za-z0-9_.-]+)=', src))

    for ig in re.findall(r'mc:Ignorable="([^"]*)"', out):
        for token in ig.split():
            if token and token not in out_prefixes:
                failures.append(
                    "mc:Ignorable names '%s' but xmlns:%s is not declared"
                    % (token, token))

    missing = sorted(in_prefixes - out_prefixes)
    if missing:
        failures.append('namespace prefixes lost during edit: %s'
                        % ', '.join(missing))

    if re.search(r'<ns\d+:', out):
        failures.append('invented ns<N>: prefixes present — stdlib '
                        'ElementTree was used; S13-3 RULE 2 violated')
    return failures
```

Any non-empty result — HARD STOP, do not deliver.

## S13-4 — Why not python-docx for insertion

python-docx can READ the document structure but has limitations for INSERTING
tables at arbitrary positions in an existing document while preserving all
existing OMML, drawings, and complex formatting. Direct XML manipulation gives
full control over insertion position and guarantees zero mutation of existing
elements. The `unzip → edit → zip` approach is the same one MockDeliver uses
for tag insertion.

## S13-5 — Restyle mechanics (v1.2)

Restyling modifies elements IN PLACE — no paragraph is recreated:

⚠️ **v1.4 — every insertion below goes through `set_child()` (S13-7).** The
element lists here are NOT a writing order. Appending them in the order
written produces `keepNext`/`keepLines` after `spacing`/`ind`, which violates
the `CT_PPr` sequence and is independently sufficient to make Word reject the
document. `set_child()` places each element at its schema-correct position
regardless of the order the caller inserts in.

- pPr: create it if absent; add/replace `<w:pBdr>` (left bar), `<w:shd>`
  (w:val="clear" — S13-1 warning applies), `<w:ind>`, `<w:spacing>`,
  `<w:keepNext>`, `<w:keepLines>` — each via
  `set_child(pPr, name, PPR_ORDER, attrs)`. Existing pPr children not listed
  in S7-5 are preserved, in place.
- rPr on each affected run: add/replace `<w:b>`, `<w:color>`, `<w:sz>`/
  `<w:szCs>`, `<w:spacing>` (letter-spacing) — each via
  `set_child(rPr, name, RPR_ORDER, attrs)`. NEVER add or modify
  `<w:rFonts>` — font face preservation is a hard invariant (S7-3).
- ⚠️ **Use the right table.** A run's properties (`<w:r><w:rPr>`) are
  `CT_RPr` → `RPR_ORDER`. A paragraph-MARK's properties (`<w:pPr><w:rPr>`)
  are `CT_ParaRPr` → `PARA_RPR_ORDER`, which admits `ins`/`del`/`moveFrom`/
  `moveTo` ahead of everything else. Using `RPR_ORDER` on a paragraph-mark
  rPr that carries `<w:del>` relocates it and corrupts the document.
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

⚠️ **v1.4 — sectPr reference insertion.** `CT_SectPr` is an ordered sequence
beginning `headerReference`, `footerReference`, `footnotePr`, `endnotePr`,
`type`, `pgSz`, `pgMar`, … Rule 4's "insert at the head of sectPr" is correct,
but implement it with `set_child()` semantics rather than a raw `insert(0, …)`,
so that a sectPr already carrying other leading children stays valid. Because a
sectPr holds THREE `headerReference` and THREE `footerReference` elements (one
per `w:type`, D10), these two are in `REPEATABLE` — `set_child()` refuses them
and `set_child_multi()` (S13-7) must be used:

```python
set_child_multi(sectPr, 'headerReference', SECTPR_ORDER, [
    {'type': 'default', 'r:id': hdr_rid},
    {'type': 'even',    'r:id': hdr_rid},
    {'type': 'first',   'r:id': hdr_rid},
])
set_child_multi(sectPr, 'footerReference', SECTPR_ORDER, [
    {'type': 'default', 'r:id': ftr_rid},
    {'type': 'even',    'r:id': ftr_rid},
    {'type': 'first',   'r:id': ftr_rid},
])
```

Note `'r:id'`, not `'id'`: the relationship id lives in the relationships
namespace, while `w:ins`/`w:del` use `w:id`. `qattr()` (S13-7) resolves the
prefix explicitly so neither can be written by accident.

## S13-7 — OOXML schema ordering discipline (v1.4)

OOXML composite types are XML Schema `xsd:sequence` — children MUST appear in
the declared order. This is not a strict-vs-transitional distinction; both
enforce it. `SubElement()`/`append()` add at the END, which is correct only if
the caller happens to insert in schema order. Any violation triggers Word's
"unreadable content" prompt.

### The tables

Extracted programmatically from
`/mnt/skills/public/docx/scripts/office/schemas/ISO-IEC29500-4_2016/wml.xsd` —
never hand-written, never recalled from memory.

⚠️ **A naive XSD walk produces SHORT tables, and a short table is the exact
failure mode `set_child()` exists to prevent.** An extractor must resolve BOTH
`xsd:extension` bases AND `xsd:group` references. Skipping group refs silently
drops `cellIns`/`cellDel`/`cellMerge` from `CT_TcPr` (they arrive via
`EG_CellMarkupElements` through `CT_TcPrInner`) and the whole of `CT_RPr` and
`CT_SectPr`, which are group-composed. To regenerate or re-verify:

```python
def xsd_order(complex_type_name, xsd_path):
    """Authoritative child order for an OOXML complexType.

    Resolves xsd:extension bases and xsd:group references — both are required.
    """
    XS = '{http://www.w3.org/2001/XMLSchema}'
    root = etree.parse(xsd_path).getroot()
    types = dict((c.get('name'), c) for c in root.iter(XS + 'complexType')
                 if c.get('name'))
    groups = dict((g.get('name'), g) for g in root.iter(XS + 'group')
                  if g.get('name'))

    def walk(node, out, seen):
        for ch in node:
            if ch.tag == XS + 'element':
                nm = ch.get('name')
                if nm and nm not in out:
                    out.append(nm)
            elif ch.tag == XS + 'group':
                ref = ch.get('ref')
                if ref:
                    ref = ref.split(':')[-1]
                    if ref in groups and ref not in seen:
                        seen.add(ref)
                        walk(groups[ref], out, seen)
                else:
                    walk(ch, out, seen)
            elif ch.tag in (XS + 'sequence', XS + 'choice', XS + 'all',
                            XS + 'complexContent', XS + 'extension'):
                if ch.tag == XS + 'extension':
                    base = ch.get('base', '').split(':')[-1]
                    if base in types and base not in seen:
                        seen.add(base)
                        walk(types[base], out, seen)
                walk(ch, out, seen)
        return out

    return walk(types[complex_type_name], [], set())
```

Expected lengths, for a fast sanity check after regeneration:
`CT_PPr` 36 · `CT_RPr` 40 · `CT_ParaRPr` 44 · `CT_TblPr` 18 · `CT_TcPr` 18 ·
`CT_TcMar` 6 · `CT_SectPr` 22. A shorter result means the walk is incomplete —
fix the extractor, do NOT ship the table.

```python
# ---------------------------------------------------------------------------
# OOXML child-element orders — ISO-IEC29500-4:2016 wml.xsd
# ---------------------------------------------------------------------------

PPR_ORDER = [
    'pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr',
    'widowControl', 'numPr', 'suppressLineNumbers', 'pBdr', 'shd', 'tabs',
    'suppressAutoHyphens', 'kinsoku', 'wordWrap', 'overflowPunct',
    'topLinePunct', 'autoSpaceDE', 'autoSpaceDN', 'bidi', 'adjustRightInd',
    'snapToGrid', 'spacing', 'ind', 'contextualSpacing', 'mirrorIndents',
    'suppressOverlap', 'jc', 'textDirection', 'textAlignment',
    'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr',
    'pPrChange',
]

# CT_RPr — properties of a RUN: <w:r><w:rPr>
RPR_ORDER = [
    'rStyle', 'rFonts', 'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike',
    'dstrike', 'outline', 'shadow', 'emboss', 'imprint', 'noProof',
    'snapToGrid', 'vanish', 'webHidden', 'color', 'spacing', 'w', 'kern',
    'position', 'sz', 'szCs', 'highlight', 'u', 'effect', 'bdr', 'shd',
    'fitText', 'vertAlign', 'rtl', 'cs', 'em', 'lang', 'eastAsianLayout',
    'specVanish', 'oMath', 'rPrChange',
]

# CT_ParaRPr — properties of a PARAGRAPH MARK: <w:pPr><w:rPr>
# Distinct from CT_RPr: four revision children precede everything else.
PARA_RPR_ORDER = ['ins', 'del', 'moveFrom', 'moveTo'] + RPR_ORDER

TBLPR_ORDER = [
    'tblStyle', 'tblpPr', 'tblOverlap', 'bidiVisual', 'tblStyleRowBandSize',
    'tblStyleColBandSize', 'tblW', 'jc', 'tblCellSpacing', 'tblInd',
    'tblBorders', 'shd', 'tblLayout', 'tblCellMar', 'tblLook', 'tblCaption',
    'tblDescription', 'tblPrChange',
]

# CT_TcPr = CT_TcPrBase (14) + EG_CellMarkupElements (cellIns/cellDel/
# cellMerge, via CT_TcPrInner) + tcPrChange. The three markup elements are
# easy to miss — they arrive through a group reference, not a direct element
# declaration — and omitting them would relocate them in any cell that has
# tracked changes.
TCPR_ORDER = [
    'cnfStyle', 'tcW', 'gridSpan', 'hMerge', 'vMerge', 'tcBorders', 'shd',
    'noWrap', 'tcMar', 'textDirection', 'tcFitText', 'vAlign', 'hideMark',
    'headers', 'cellIns', 'cellDel', 'cellMerge', 'tcPrChange',
]

# CT_TcMar and CT_TblCellMar share this order. BOTH naming pairs are valid —
# start/end AND left/right. All six must stay in the table (see S13-1).
TCMAR_ORDER = ['top', 'start', 'left', 'bottom', 'end', 'right']

SECTPR_ORDER = [
    'headerReference', 'footerReference', 'footnotePr', 'endnotePr', 'type',
    'pgSz', 'pgMar', 'paperSrc', 'pgBorders', 'lnNumType', 'pgNumType',
    'cols', 'formProt', 'vAlign', 'noEndnote', 'titlePg', 'textDirection',
    'bidi', 'rtlGutter', 'docGrid', 'printerSettings', 'sectPrChange',
]
```

### The insertion function

⚠️ **Do NOT sort the parent's children.** A whole-parent sort relocates every
element missing from the table, and no hardcoded table can enumerate what a
real Word document contains (extension-namespace children, revision markers,
future additions). Two verified corruptions caused by sorting:

| Parent | Valid input | After a whole-parent sort | Validator |
|---|---|---|---|
| `tcMar` (Word-native) | `top, left, bottom, right` | `top, bottom, left, right` | **`left`: This element is not expected** |
| `<w:pPr><w:rPr>` with a deleted paragraph mark | `del, b` | `b, del` | **`del`: This element is not expected** |

`set_child()` inserts at the correct position **relative to elements already
present** and never moves an existing child:

```python
# Attribute namespaces. A bare key means the w: namespace; a key written
# "prefix:name" is resolved through ATTR_NS. This is explicit on purpose:
# <w:headerReference> needs r:id while <w:ins>/<w:del> need w:id, so no
# blanket rule for a key called "id" can be correct.
ATTR_NS = {
    'w': W,
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'xml': 'http://www.w3.org/XML/1998/namespace',
}

# Elements that may legitimately occur MORE THAN ONCE in one parent, per the
# ISO-IEC29500-4:2016 schema. D10 requires three of each in every sectPr
# (default / even / first), so set_child's replace-one semantics would destroy
# two of them — it refuses, and set_child_multi must be used instead.
REPEATABLE = {'headerReference', 'footerReference'}


def qattr(key):
    """Resolve an attribute key to a Clark-notation qualified name."""
    if ':' in key:
        prefix, local = key.split(':', 1)
        if prefix not in ATTR_NS:
            raise ValueError('unknown attribute namespace prefix: %s' % prefix)
        return '{%s}%s' % (ATTR_NS[prefix], local)
    return '{%s}%s' % (W, key)


def _insert_index(parent, order, name):
    """Index at which `name` belongs, relative to the children already present."""
    rank = dict((n, i) for i, n in enumerate(order))
    mine = rank[name]
    for i, child in enumerate(parent):
        r = rank.get(ln(child))
        if r is not None and r > mine:
            return i
    return len(parent)


def set_child(parent, name, order, attrs=None):
    """Insert-or-replace <w:name> at its schema-correct position.

    NEVER reorders existing children — unknown/extension elements stay put.
    Raises on an unknown name so a missing table entry fails loudly rather
    than corrupting silently, and on a repeatable element so the caller is
    sent to set_child_multi instead of silently losing siblings.
    """
    if name not in order:
        raise ValueError('%s is not in the supplied schema order table' % name)
    if name in REPEATABLE:
        raise ValueError('%s may occur more than once — use set_child_multi() '
                         'or its siblings will be destroyed' % name)
    for existing in [c for c in parent if ln(c) == name]:
        parent.remove(existing)
    el = etree.Element(w(name))
    for key, val in (attrs or {}).items():
        el.set(qattr(key), val)
    parent.insert(_insert_index(parent, order, name), el)
    return el


def set_child_multi(parent, name, order, attrs_list):
    """Same placement rule, for elements legitimately repeated in one parent.

    Used for <w:headerReference>/<w:footerReference>, which appear once per
    w:type (default/even/first). Removes all existing instances of `name`,
    then inserts the new set together at the schema-correct position.

    Attribute keys follow qattr(): write 'r:id' for the relationship id and
    'type' for w:type.
    """
    if name not in order:
        raise ValueError('%s is not in the supplied schema order table' % name)
    if not attrs_list:
        raise ValueError('set_child_multi(%s) called with an empty attrs_list — '
                         'this would delete the existing elements and add '
                         'nothing; pass the replacement set explicitly' % name)
    for existing in [c for c in parent if ln(c) == name]:
        parent.remove(existing)
    idx = _insert_index(parent, order, name)
    made = []
    for offset, attrs in enumerate(attrs_list):
        el = etree.Element(w(name))
        for key, val in (attrs or {}).items():
            el.set(qattr(key), val)
        parent.insert(idx + offset, el)
        made.append(el)
    return made


def get_or_make(parent, name, order):
    """Return the existing child `name`, creating it in position if absent."""
    for child in parent:
        if ln(child) == name:
            return child
    return set_child(parent, name, order)
```

### When it is required

MANDATORY after/for any insertion into: `pPr` (`PPR_ORDER`), run `rPr`
(`RPR_ORDER`), paragraph-mark `rPr` (`PARA_RPR_ORDER`), `tblPr`
(`TBLPR_ORDER`), `tcPr` (`TCPR_ORDER`), `tcMar` / `tblCellMar`
(`TCMAR_ORDER`), `sectPr` (`SECTPR_ORDER`).

**In EVERY part the step writes** — `word/document.xml`, `word/headerN.xml`,
`word/footerN.xml`. On the failing artefact the header and footer parts each
carried their own `pBdr` violation; a body-only discipline would not have
caught them.

NOT required when only modifying the *attributes* of an element that already
exists, or when reading.

⚠️ **`set_child()` places elements; it does not know their required
attributes.** Schema validity needs both. `<w:shd>` requires `w:val` and
`w:fill`, `<w:sz>` requires `w:val`, `<w:pgMar>` requires all eight of
top/right/bottom/left/header/footer/gutter, `<w:tblW>` requires `w:w` and
`w:type`, and each `<w:pBdr>`/`<w:tblBorders>` side element requires
`w:val`/`w:sz`/`w:space`/`w:color`. Correct order with missing attributes is
still an invalid document — S8-9 reports these as
`The attribute '…' is required but missing`.

### ⚠️ Nested defects are masked — an error count is a LOWER BOUND

When a validator rejects an element at its own position it does not descend
into that element, so its children's violations stay hidden until the outer
one is fixed. Measured on the failing artefact: **812 errors reported, but 991
elements actually required reordering.** `tcMar`'s internal
`[top, bottom, left, right]` was invisible behind `tcMar`'s own misplacement
inside `tcPr`.

Consequence: **never treat a reduced error count as success.** S8-9 passes only
at zero. If a fix lowers the count, re-run — new errors surfacing is expected
behaviour, not a regression.

This is also why the correct remedy for that `tcMar` was to REORDER to
`[top, left, bottom, right]`, not to rename `left`/`right` to `start`/`end`.
Renaming would have masked the real fault while leaving `TCMAR_ORDER`
incomplete for every Word-authored table (S13-1).

### Inline order assertion (cheap, runs before S8-9)

```python
def assert_schema_order(parent, order, where=''):
    """Raise if `parent`'s known children are not in schema order.

    Unknown/extension children are ignored — they are not the caller's to
    order. Use as a cheap inline guard right after building an element, so a
    fault is caught at its source rather than at the S8-9 gate.
    """
    rank = dict((n, i) for i, n in enumerate(order))
    seen = [rank[ln(c)] for c in parent if ln(c) in rank]
    for i in range(len(seen) - 1):
        if seen[i] > seen[i + 1]:
            names = [ln(c) for c in parent]
            raise AssertionError('schema order violation in %s%s: %s'
                                 % (ln(parent), (' (' + where + ')') if where else '',
                                    names))
    return True
```

### Self-test (run before first use on a new exam)

```python
def selftest_set_child():
    """Assert every regression case that caused, or would cause, corruption."""
    def mk(xml):
        return etree.fromstring(xml.replace('@W@', W))

    R_NS = ATTR_NS['r']

    # 1. Word-native tcMar must survive untouched.
    tc = mk('<w:tcMar xmlns:w="@W@">'
            '<w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
            '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
            '</w:tcMar>')
    set_child(tc, 'top', TCMAR_ORDER, {'w': '40', 'type': 'dxa'})
    assert [ln(c) for c in tc] == ['top', 'left', 'bottom', 'right']

    # 2. A deleted paragraph mark must stay first.
    rpr = mk('<w:rPr xmlns:w="@W@"><w:del w:id="1"/><w:i/></w:rPr>')
    for nm in ['b', 'color', 'sz']:
        set_child(rpr, nm, PARA_RPR_ORDER)
    assert ln(list(rpr)[0]) == 'del'

    # 3. The S13-5 workload, inserted in deliberately wrong order.
    ppr = mk('<w:pPr xmlns:w="@W@"><w:jc w:val="both"/></w:pPr>')
    for nm in ['spacing', 'ind', 'keepNext', 'keepLines', 'shd', 'pBdr']:
        set_child(ppr, nm, PPR_ORDER)
    names = [ln(c) for c in ppr]
    rank = dict((n, i) for i, n in enumerate(PPR_ORDER))
    assert all(rank[names[i]] < rank[names[i + 1]]
               for i in range(len(names) - 1)), names

    # 4. Extension-namespace children are never relocated.
    px = mk('<w:pPr xmlns:w="@W@" xmlns:w14="urn:x"><w14:collapsed/>'
            '<w:jc w:val="both"/></w:pPr>')
    set_child(px, 'spacing', PPR_ORDER)
    assert ln(list(px)[0]) == 'collapsed'

    # 5. All three header/footer references survive, in schema position,
    #    with the relationship id in the r: namespace (D10).
    sect = mk('<w:sectPr xmlns:w="@W@"><w:pgSz w:w="11906"/></w:sectPr>')
    set_child_multi(sect, 'headerReference', SECTPR_ORDER,
                    [{'type': t, 'r:id': 'rId7'}
                     for t in ('default', 'even', 'first')])
    set_child_multi(sect, 'footerReference', SECTPR_ORDER,
                    [{'type': t, 'r:id': 'rId8'}
                     for t in ('default', 'even', 'first')])
    assert [ln(c) for c in sect] == (['headerReference'] * 3
                                     + ['footerReference'] * 3 + ['pgSz'])
    assert all(c.get('{%s}id' % R_NS) == 'rId7'
               for c in sect if ln(c) == 'headerReference')

    # 6. set_child REFUSES repeatable elements rather than collapsing them.
    try:
        set_child(sect, 'headerReference', SECTPR_ORDER, {'type': 'default'})
        raise AssertionError('set_child accepted a repeatable element')
    except ValueError:
        pass
    assert len([c for c in sect if ln(c) == 'headerReference']) == 3

    # 7. set_child_multi refuses an empty replacement set.
    try:
        set_child_multi(sect, 'headerReference', SECTPR_ORDER, [])
        raise AssertionError('set_child_multi accepted an empty attrs_list')
    except ValueError:
        pass

    # 8. Unknown element name and unknown attribute prefix both fail loudly.
    try:
        set_child(mk('<w:pPr xmlns:w="@W@"/>'), 'nosuch', PPR_ORDER)
        raise AssertionError('unknown element name accepted')
    except ValueError:
        pass
    try:
        qattr('zz:id')
        raise AssertionError('unknown attribute prefix accepted')
    except ValueError:
        pass

    # 9. get_or_make returns the existing child, never a duplicate.
    p2 = mk('<w:pPr xmlns:w="@W@"><w:jc w:val="both"/></w:pPr>')
    a = get_or_make(p2, 'spacing', PPR_ORDER)
    a.set(w('before'), '120')
    b = get_or_make(p2, 'spacing', PPR_ORDER)
    assert a is b and b.get(w('before')) == '120'
    assert [ln(c) for c in p2] == ['spacing', 'jc']
    return True
```

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

**End of Framework_PYQFormat.md (v1.5)**
