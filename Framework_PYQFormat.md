# Framework_PYQFormat v1.0 — Universal PYQ Student Document Formatter
# [ExamCode] project | PYQ-3 (PYQFormat) | Exam-agnostic
#
# v1.0 — 2026-07-22 — Initial release. Takes the audited PYQ explanation
#   document from PYQ-2 (PYQExplainAudit) and transforms it into a beautiful,
#   student-facing Word document: exam header, IFAS branding footer, per-
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
- **Insert** the exam header as the first element (new content only)
- **Insert** colored pill tables before each Q-stem (new content only)
- **Insert** the IFAS branding footer as the last element (new content only)
- **Apply** visual styling (font, spacing, page margins) to existing elements

It **NEVER**:
- Changes any character in any question stem, option, table, image, or explanation
- Reorders questions
- Removes, rewrites, or paraphrases any content
- Modifies any OMML fraction or math element
- Alters any image, drawing, or media part
- Changes the correct-answer line, axiom, deduction, speed hack, or why-wrong text

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
  Contains: exam header + (pill + question + explanation) × Q_TOTAL + IFAS footer.
  Every question/explanation byte-identical to the input; only visual elements added.

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
2. bash_tool    → run it (open input → insert header → insert pills → insert
                  footer → apply styling → save output)
3. bash_tool    → verify output (Q-count, pill-count, content integrity)
4. present_files → deliver [ExamCode]_[date]_[session]_PYQ_Formatted.docx
```

This step uses the `unzip → edit XML → zip` approach for editing the existing
docx (python-docx for reading structure, direct XML manipulation for insertions
that must preserve all existing formatting, OMML, images, and drawings intact).

---

# §3 — Exam header

The exam header is the FIRST visible element in the formatted document, inserted
before Q.1 (before Q.1's pill, before Q.1's stem — the very top of the document).

## S3-1 — Header content

```text
[exam_name]   ·   [DD-Mon-YYYY]   ·   [Shift/Session N]   ·   IFAS
```

Example:
```text
SSC CGL Tier 1   ·   12-Sep-2025   ·   Shift 1   ·   IFAS
```

- `exam_name`: from exam_config.json `exam_name` field (or ExamCode as fallback)
- `DD-Mon-YYYY`: from the trigger DATE
- `Shift/Session N`: from the trigger SESSION (omit the session part if no session)
- `IFAS`: hardcoded (D5)
- Separator: ` · ` (space · middle-dot · space)

## S3-2 — Header styling

```text
Font        : Arial, 14pt, Bold
Alignment   : Center
Color       : Dark blue (#1F3864)
Spacing     : 6pt before, 12pt after (visual separation from first question)
Border      : Thin bottom border, dark blue (#1F3864), 0.5pt
```

The header is a SINGLE paragraph with the four elements separated by middle-dot
spacers. No table, no multi-line — one clean centered line.

---

# §4 — Colored pills (Option C)

Per-question Subject/Topic/Subtopic classification displayed as three colored
pill cells inserted BEFORE each Q-stem. This is the visual signature of PYQ-3
and must look professional and beautiful in the downloaded Word document.

## S4-1 — Pill structure (per question)

For each question Q.n, insert a 1-row, 3-cell Word table immediately before
the Q-stem paragraph. Each cell displays one classification level:

```text
┌─────────────────┬─────────────────┬─────────────────┐
│    [Subject]    │     [Topic]     │   [Subtopic]    │
└─────────────────┴─────────────────┴─────────────────┘
```

The table is inserted as a NEW element — it does not modify or displace the
Q-stem or any other existing content.

## S4-2 — Pill styling

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

## S4-3 — Pill table properties

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

## S4-4 — Pill data resolution

For each question Q.n, look up `q_to_classification[n]`:
- `subject` → Cell 1 text
- `topic` → Cell 2 text
- `subtopic` → Cell 3 text

If Q.n is missing from the classification map → SKIP the pill for that question
(WARN in the delivery report, do not HALT). The question and its explanation are
still included — only the pill is omitted.

## S4-5 — Pill insertion position

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

For Q.1, the order is:
```text
[exam header]          ← NEW (§3)
[pill table for Q.1]   ← NEW (§4)
Q.1 stem paragraph     ← EXISTING
...
```

---

# §5 — IFAS branding footer

The IFAS branding footer is the LAST visible element in the formatted document,
inserted after the last question's explanation block — the very bottom of the
document.

## S5-1 — Footer content

```text
ifasonline.com   ·   IFAS: India's No. 1 Sarkari Exam Preparation   ·   +91-9172266888
```

All three elements on ONE line, separated by ` · ` (middle-dot spacers).

## S5-2 — Footer styling

```text
Font        : Arial, 10pt, Bold
Alignment   : Center
Color       : Dark blue (#1F3864)
Spacing     : 18pt before (visual separation from last explanation), 6pt after
Border      : Thin top border, dark blue (#1F3864), 0.5pt
```

## S5-3 — Footer hardcoded values (D5)

These are COMPANY branding constants, not exam-specific values:
- Website: `ifasonline.com`
- Tagline: `IFAS: India's No. 1 Sarkari Exam Preparation`
- Phone: `+91-9172266888`

Same across all exams, all papers, all sessions. Hardcoded by design.

---

# §6 — Visual polish

Optional visual improvements applied to the EXISTING content elements. These
changes affect STYLING ONLY — never text content, never OMML math, never images.

## S6-1 — Page margins (if not already set)

```text
Top     : 1.27 cm (0.5 in)
Bottom  : 1.27 cm (0.5 in)
Left    : 1.91 cm (0.75 in)
Right   : 1.91 cm (0.75 in)
```

Compact margins maximize content per page for a student printout.

## S6-2 — Consistent spacing

Ensure paragraph spacing between questions is uniform:
- Before each Q-stem (after the pill table): 8pt
- After the last explanation element of each Q: 12pt
- Between explanation sub-sections (AXIOM → DEDUCTION → etc.): unchanged
  (preserve the spacing PYQ-1/PYQ-2 set through the engine)

## S6-3 — What is NOT changed

- Font face of question/option/explanation text → NEVER changed (preserve
  whatever font the Row file and engine used)
- Bold/italic/underline formatting on any text → NEVER changed
- OMML fractions and math elements → NEVER touched
- Images, drawings, charts, tables → NEVER modified
- Paragraph content → NEVER modified (zero-mutation rule)

---

# §7 — Content integrity verification

After all visual elements are inserted and styling is applied, PYQ-3 verifies
that the content is intact. This is the LAST check before delivery.

## S7-1 — Question count match

Count the Q-stems in the output document and verify it equals Q_TOTAL from the
input document. A mismatch means PYQ-3 accidentally displaced or deleted a
question paragraph — HARD STOP.

## S7-2 — Pill count match

Count the pill tables in the output document. Expected: one per question that
has a classification entry (may be fewer than Q_TOTAL if some Qs are missing
from the map). Verify: pill_count == len(q_to_classification ∩ {1..Q_TOTAL}).

## S7-3 — Header and footer presence

Verify the exam header paragraph is the first element (before Q.1's pill).
Verify the IFAS footer paragraph is the last element (after the last Q's
explanation).

## S7-4 — Content byte-identity spot-check

For a sample of questions (first 3, last 3, and 3 random), extract the Q-stem
text from both the input and output documents and confirm they are byte-identical.
This is a spot-check, not a full fidelity verification (PYQ-2 already certified
the content — PYQ-3 only adds around it).

## S7-5 — OMML survival check

Count the `<m:oMath>` elements in the input and output. They must be equal —
PYQ-3 never creates, modifies, or removes OMML. A mismatch means the XML
manipulation accidentally corrupted a math element — HARD STOP.

## S7-6 — Image survival check

Count the `<w:drawing>` elements in the input and output. They must be equal.
A mismatch means an image was lost or duplicated — HARD STOP.

---

# §8 — Delivery

PYQ-3 delivers in a single response (no batching):

1. All integrity checks (§7) pass.
2. Present `[ExamCode]_[date]_[session]_PYQ_Formatted.docx` via present_files.
3. Print the delivery report (§9).
4. Render the post-delivery footer per Framework_DeliveryFooter.md:
   - F2 (step-complete, GREEN) — PYQ-3 delivers once, always complete.
   - File badge: `📁 Use locally` for PYQ_Formatted.docx.
   - Next-step reference: "This is the student-facing document — ready for
     distribution. For portal delivery, run PYQ-4 (PYQDeliver) separately
     in a new chat (PYQ-4 takes PYQ-2 output directly, not this file)."

---

# §9 — Delivery report

Printed in chat after present_files. Brief and skimmable:

- **§R1 — Scope.** Exam, paper (date, session), Q_TOTAL.
- **§R2 — Header.** Exam header text as rendered.
- **§R3 — Pills.** pill_count of Q_TOTAL questions have pills. Any missing
  classifications listed by Q number.
- **§R4 — Footer.** IFAS branding footer text as rendered.
- **§R5 — Integrity.** Q-count match, OMML count match, image count match,
  spot-check results. All must show PASS.
- **§R6 — Note.** "This is the student-facing document. Review in Microsoft
  Word (OMML renders correctly only in Word). For portal delivery, run PYQ-4
  (PYQDeliver) in a new chat — it takes PYQ-2 output directly."

---

# §10 — Definition of done

PYQ-3 is done when **all** hold:

1. The input document opened successfully and Q_TOTAL was determined.
2. The q_to_classification map was loaded with coverage for the paper.
3. The exam header is the first element, correctly formatted (§3).
4. Every question with a classification entry has a colored pill table
   immediately before its Q-stem (§4).
5. The IFAS branding footer is the last element, correctly formatted (§5).
6. ZERO content was changed — no question, option, explanation, OMML, or
   image was modified (zero-mutation rule).
7. All integrity checks (§7) pass: Q-count, pill-count, header/footer
   presence, content spot-check, OMML count, image count.
8. The output is a valid .docx that opens clean in Microsoft Word.
9. Delivered via present_files with the delivery report and footer.

**Hard invariants (never violated):**

- No text content is modified (zero-mutation rule).
- No OMML element is created, modified, or removed.
- No image or drawing is modified, moved, or removed.
- The pill table is the ONLY new element between questions.
- The exam header is the ONLY new element before Q.1.
- The IFAS footer is the ONLY new element after the last explanation.
- No exam-specific value is hardcoded (exam-agnostic guarantee).
  The only hardcoded values are IFAS branding constants (D5).

---

# §11 — Edge cases

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
   elements only; existing elements are untouched (§6-3, §7-5, §7-6).

8. **Multi-session exam (same date, 3 shifts)** → Each session is a
   separate PYQFormat run. The filename includes the session identifier.

9. **Document already formatted (re-run)** → The output filename differs
   from the input filename, so re-running produces a fresh formatted doc
   from the original input. If someone attaches the _PYQ_Formatted.docx
   by mistake, the spec detects it (filename check) and warns: "This
   appears to already be a formatted document. Attach the
   _PYQ_Explanation_Complete.docx instead."

---

# §12 — Implementation notes

## S12-1 — Pill table XML structure

The pill table is built as a `<w:tbl>` element in the document XML with:
- `<w:tblPr>`: table width 100%, layout fixed, no borders
- `<w:tblGrid>`: 3 `<w:gridCol>` of equal width
- `<w:tr>`: single row with 3 `<w:tc>` cells
- Each `<w:tc>`: cell properties (shading with fill color, vertical alignment
  center, cell margins) + a single `<w:p>` with the classification text

Cell shading uses `<w:shd w:val="clear" w:fill="[HEX]"/>` — the `clear` val
is critical (Word renders `solid` as opaque black).

## S12-2 — Insertion strategy

The document is processed via `unzip → XML edit → zip`:

1. Unzip the input .docx to a working directory
2. Parse `word/document.xml` as XML
3. Find each Q-stem `<w:p>` by matching the question regex pattern
4. For each Q-stem found (in reverse order to preserve positions):
   - Build the pill `<w:tbl>` element
   - Insert it BEFORE the Q-stem `<w:p>` in the parent `<w:body>`
5. Insert the exam header `<w:p>` as the first child of `<w:body>`
6. Insert the IFAS footer `<w:p>` as the last child of `<w:body>`
7. Re-zip to the output .docx

Processing in REVERSE ORDER (Q.N → Q.1) ensures that inserting elements
for Q.5 doesn't shift the positions of Q.6-Q.N (which were already processed).

## S12-3 — Namespace preservation

When editing the XML, ALL existing namespace declarations on the root element
must be preserved exactly. No `cleanup_namespaces()` — this strips xmlns
declarations that `mc:Ignorable` and drawing content reference, causing Word
to show "unreadable content" errors (learned from MockDeliver v1.3).

## S12-4 — Why not python-docx for insertion

python-docx can READ the document structure but has limitations for INSERTING
tables at arbitrary positions in an existing document while preserving all
existing OMML, drawings, and complex formatting. Direct XML manipulation gives
full control over insertion position and guarantees zero mutation of existing
elements. The `unzip → edit → zip` approach is the same one MockDeliver uses
for tag insertion.

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

These are design tokens, not exam-specific values. They are the same
across all exams and all papers.
```

---

**End of Framework_PYQFormat.md (v1.0)**
