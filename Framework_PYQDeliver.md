# Framework_PYQDeliver v1.0 — Universal PYQ Portal Tagger & Delivery Engine
# [ExamCode] project | PYQ-4 (PYQDeliver) | Exam-agnostic
#
# v1.0 — 2026-07-22 — Initial release. Takes the audited PYQ explanation
#   document from PYQ-2 (PYQExplainAudit), inserts a 5-line portal tag block
#   (Subject / Topic / Subtopic / Question Type / Complexity) before every
#   Q-stem, applies render-safe transforms (OMML linearization, non-ASCII
#   safe-font, underlined-stem recolor), maintains the PYQ registry, and
#   delivers a tagged, portal-ready Word document to Google Drive.
#
#   Adapted from MockDeliver (Step 11) for the PYQ pipeline. Uses the same
#   tag block format, render transforms, and two-artifact model (integrity +
#   render-source). Key difference: tag values come from q_to_classification
#   (PYQ-1 P3) instead of a registry.json + blueprint.json JOIN, and
#   difficulty is HARDCODED for PYQ papers.
#
#   Architecture decisions locked with the framework owner:
#     D1. FORK INPUT. PYQ-4 takes PYQ-2 output directly
#         ([ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx).
#         PYQ-3 and PYQ-4 are INDEPENDENT — neither depends on the other.
#     D2. SAME PORTAL FORMAT. The output uses the same 5-line tag block as
#         MockDeliver (Step 11) so the portal ingests PYQ papers identically
#         to mock papers. No portal-side changes needed.
#     D3. TAG DATA FROM q_to_classification. Subject/Topic/Subtopic resolved
#         from the classification map built by PYQ-1 P3. No registry.json or
#         blueprint.json JOIN — those do not exist for PYQ papers.
#     D4. DIFFICULTY HARDCODED. All PYQ questions get the same difficulty
#         label (configurable per exam via exam_config.json difficulty_default,
#         fallback "Medium"). PYQ papers are past exams — assigning per-Q
#         difficulty would require subjective classification.
#     D5. QUESTION TYPE DERIVED. MCQ/MSQ/NAT derived from options_by_q (Row
#         file scan, same as PYQ-1 P2). Not from blueprint marking_scheme
#         (which does not exist for PYQ).
#     D6. PYQ REGISTRY. [ExamCode]_pyq_registry.json tracks which PYQ papers
#         have been delivered, preventing re-delivery and providing a corpus
#         progress dashboard.
#     D7. DRIVE DELIVERY. The final doc is uploaded to Google Drive.
#     D8. TWO-ARTIFACT MODEL. Same as MockDeliver: integrity artifact (OMML
#         intact) + render-source artifact (OMML linearized, safe-font,
#         underline recolor). The render-source is the delivered file.
#     D9. ENGINE NOT REQUIRED. PYQ-4 reads the docx structurally (Q-stems,
#         tag insertion, render transforms). No explain_engine.py needed.

# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take the audited PYQ explanation document, JOIN per-question metadata
#   from the classification map, INSERT portal tag blocks, apply render-safe
#   transforms, and deliver a tagged, upload-ready Word document for the
#   distribution portal. This is the portal-facing counterpart to PYQ-3
#   (which produces the student-facing download).

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
#     PYQ-3  PYQFormat       → _PYQ_Formatted.docx        (student)
#     PYQ-4  PYQDeliver      → _PYQ_Final.docx             (portal)  ← THIS STEP
#     (PYQ-3 and PYQ-4 are INDEPENDENT — both take PYQ-2 output.)

# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. Subject names, topic
#   names, subtopic names, question counts, option counts, question types —
#   all read at runtime from the classification map, exam_config.json, and
#   the document itself. Same spec runs for SSC CGL, GATE, NEET, UPSC, CAT,
#   CSIR, Banking, RRB, state PSC, or any exam.

---

# ★ ZERO-MUTATION RULE — NON-NEGOTIABLE

The content of every question block is SACRED. PYQ-4 may only:
- **Insert** 5-line tag blocks before each Q-stem (new content only)
- **Linearize** OMML → Unicode text on the render-source copy only
- **Re-font** non-ASCII spans to a safe font on the render-source copy only
- **Recolor** directly-underlined runs in question stems to red FF0000 on the
  render-source copy only

It **NEVER**:
- Changes any character in any question stem, option, table, image, or explanation
- Reorders questions
- Removes, rewrites, or paraphrases any content
- Modifies the integrity artifact in any way other than inserting tag blocks

Violation of this rule is a hard failure regardless of any other outcome.

---

# §0 — Input / output contract

**Inputs:**

1. `[ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx` — the PYQ-2 audited
   explanation document. Attached by user. This is the same input PYQ-3 uses (FORK).
   ALSO ACCEPTS: `_PYQ_Explanation.docx` (PYQ-1 output, if audit not yet run).
   The spec prefers the audited version.

2. `exam_config.json` — in project knowledge. Provides `exam_name`, `difficulty_default`
   (fallback "Medium"), and `difficulty_labels`.

3. `q_to_classification` map — the per-question {subject, topic, subtopic,
   subtopic_id} mapping. Loaded from ONE of these sources (in priority order):
   a. `pyq_audit_progress.json` sidecar (if PYQ-2 was run)
   b. `pyq_explain_progress.json` sidecar (PYQ-1's progress file)
   c. Attached by user as a separate JSON file
   If no classification map is found → HARD STOP:
     "q_to_classification map not found. Run PYQExplain first, or attach
      pyq_explain_progress.json / pyq_audit_progress.json."

4. `options_by_q` — the per-question option count map (for question type resolution).
   Loaded from the same progress JSON as q_to_classification, or derived from
   the Row file if attached. If unavailable → HARD STOP:
     "options_by_q not found. Attach the progress JSON or the Row file."

5. `section_rules.md` — in project knowledge. Provides q_re (question regex) for
   Q-stem detection in the document.

NOT REQUIRED (PYQ-4 does not use mock pipeline outputs):
  ✗ blueprint.json — does not exist for PYQ papers
  ✗ registry.json — does not exist for PYQ papers
  ✗ explain_engine.py — no explanations written or read
  ✗ explain_audit_gate.py — no audit performed
  ✗ paper_pipeline.py — filenames derived from the attached document

**Outputs:**

- `[ExamCode]_[date]_[session]_PYQ_Final.docx` — the tagged, render-safe document
  for portal upload. Every Q-stem preceded by 5 tag lines. OMML linearized to
  Unicode. Non-ASCII safe-fonted. Underlined stems recolored red.
- Updated `[ExamCode]_pyq_registry.json` — PYQ corpus progress tracker (§8).

---

# §1 — Trigger and resolution

PYQ-4 begins on the instruction:

```text
PYQDeliver
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
   If no matching file attached → HARD STOP: "Attach the PYQ Explanation document."

4. **exam_config.json**: load from project knowledge. Extract `exam_name`,
   `difficulty_default`, `difficulty_labels`.

5. **q_to_classification + options_by_q**: load from progress JSON (§0 priority).

6. **PYQ registry check**: load `[ExamCode]_pyq_registry.json` if it exists.
   If this paper (date + session) is already marked `completed` → WARN:
   "This paper has already been delivered. Proceed? (Continue to re-deliver,
   or stop.)" Proceed only on explicit confirmation.

7. **Preflight checks**: same structural validations as MockDeliver S1-2:
   - Q-stems match q_re and count equals Q_TOTAL
   - Q-numbers are 1..Q_TOTAL continuous, no gaps
   - Render-safe font stack installed (DejaVu Sans, FreeSans)
   - document.xml parses cleanly

---

# §2 — Tag value resolution

PYQ-4 resolves tag values differently from MockDeliver. MockDeliver JOINs
registry.json + blueprint.json. PYQ-4 reads from the classification map
directly — no JOIN needed.

## S2-1 — Tag fields and sources

| # | Field | Source | Resolution |
|---|---|---|---|
| 1 | Subject | `q_to_classification[q].subject` | Direct lookup |
| 2 | Topic | `q_to_classification[q].topic` | Direct lookup |
| 3 | Subtopic | `q_to_classification[q].subtopic` | Direct lookup |
| 4 | Question Type | `options_by_q[q]` | 0 → NAT; answer_cardinality 'multi' → MSQ; else → MCQ |
| 5 | Complexity | `exam_config.difficulty_default` | HARDCODED for all PYQ Qs (D4) |

## S2-2 — Question Type resolution

PYQ papers have no `blueprint.marking_scheme` — Question Type is resolved from
the question's structure, not from a position-based scheme:

```text
options_by_q[q] == 0                              → NAT
section_rules answer_cardinality == 'multi'        → MSQ
  (for this Q's subtopic, looked up via
   q_to_classification[q].subtopic_id)
else                                              → MCQ
```

This is the same resolution PYQ-1 uses at P4 — the types are consistent across
the pipeline. If answer_cardinality is not available for a subtopic, default to
'single' (MCQ) — the vast majority of PYQ questions are MCQ.

## S2-3 — Complexity (difficulty) — HARDCODED (D4)

All PYQ questions receive the same Complexity tag value:
- Read `difficulty_default` from `exam_config.json` (e.g. "Medium")
- If `difficulty_default` is not set → use "Medium" as fallback
- Validate the value is in `difficulty_labels` from exam_config

This is a deliberate design decision: PYQ papers are past exams — per-question
difficulty would require subjective classification that no upstream step has
performed. A uniform label is accurate (it means "not classified") and does
not mislead the portal.

## S2-4 — Tag field order (fixed — portal contract)

```text
Subject: <value>
Topic: <value>
Subtopic: <value>
Question Type: <value>
Complexity: <value>
```

Same order as MockDeliver §3-3. The portal expects this exact label sequence.

## S2-5 — Pre-tagging validation

Before inserting any tag blocks, verify the complete tag lookup:
- Every Q from 1..Q_TOTAL has all 5 fields non-empty
- If any Q is missing from q_to_classification → HARD STOP (unlike PYQ-3
  which WARNs on missing pills, PYQ-4 requires complete coverage because
  the portal requires every question to be tagged)

---

# §3 — Execution model

PYQ-4 is a SINGLE-PASS transformation. No batching, no multi-turn:

```text
1. create_file  → write complete pyq_deliver_pipeline.py
2. bash_tool    → run it (parse → build tag lookup → insert tags →
                  build integrity artifact → render transforms →
                  build render-source → validate all gates)
3. bash_tool    → final gate checks + PYQ registry update
4. present_files → deliver [ExamCode]_[date]_[session]_PYQ_Final.docx
```

Uses the same `unzip → XML edit → zip` approach as MockDeliver. The two-artifact
model (integrity + render-source) is identical.

---

# §4 — Two-artifact model

Same architecture as MockDeliver, adapted for PYQ:

## S4-1 — Why two artifacts

Three empirically verified facts drive the two-artifact design:

1. A naive python-docx round-trip on a docx containing `<m:oMath>` can SILENTLY
   CORRUPT every math element. OMML must be linearized to Unicode text in the
   render-source before delivery. The integrity artifact keeps OMML untouched.
2. Plain Unicode text runs survive all downstream tooling perfectly.
3. A non-ASCII glyph in a run tagged with Arial/Times can corrupt the text layer.
   Re-tagging to a safe font fixes this.

## S4-2 — Artifact definitions

- **Integrity artifact**: byte-perfect content docx with native OMML, tag blocks
  inserted but no render transforms applied. Used for validation (gates C1-C10).
  NOT delivered.
- **Render-source artifact**: tag blocks + OMML linearized + safe-font + underline
  recolor. THIS is the delivered file (`_PYQ_Final.docx`).

---

# §5 — Tag insertion

Tag blocks are inserted the same way as MockDeliver Phase 2:

## S5-1 — Tag block structure

For each question Q.n, 5 tag paragraphs are inserted BEFORE the Q-stem:

```text
Subject: <value>
Topic: <value>
Subtopic: <value>
Question Type: <value>
Complexity: <value>
Q.n  [stem]    ← existing, unchanged
```

Each tag paragraph: Arial 11pt, left-aligned, zero spacing, built from scratch
(NEVER cloned from existing paragraphs — MockDeliver lesson). `<w:spacing>`
BEFORE `<w:jc>` in pPr (OOXML schema order — MockDeliver v1.3 fix).

## S5-2 — Insertion mechanics

Walk the document body. For each Q-stem found:
1. Look up tag values from the tag lookup (§2)
2. Build 5 tag paragraphs using `make_tag_para(label, value)`
3. Insert at `idx + i` for i in 0..4, where idx is the Q-stem's position
   (computed once BEFORE any insertion for this Q)

After all insertions, `reassign_docpr_ids(root)`.

## S5-3 — Header stripping (safety-net)

Same as MockDeliver: detect_header_paras() scans for any non-blank, non-Q-stem paragraphs before Q.1.
On the PYQ-2 output, this should find ZERO (the document is questions + explanations
only). Any hits are stripped and a REGRESSION ALARM is raised in the report.

---

# §6 — Render transforms

Applied to the render-source artifact only. Same transforms as MockDeliver:

## S6-1 — Rule 19: OMML → Unicode text

Replace every `<m:oMath>` with a Unicode text run. Each linearized string is
copy-paste–correct. Font: DejaVu Sans.

## S6-2 — Rule 22: Underlined stem recolor

Directly-underlined runs in Q-stem regions → red FF0000. Only stem regions —
options, explanations, tag blocks are not touched.

## S6-3 — Rule 21: Non-ASCII safe-font

Per-codepoint font selection from the safe font stack (DejaVu Sans + FreeSans).
Section markers (❌ ⬛ ✅ ⚡) are covered by FreeSans. Codepoints no stacked font
covers keep their original font (Word substitutes) and are logged.

---

# §7 — Validation checklist (all gates must PASS)

Same gate structure as MockDeliver, adapted for PYQ:

**Content-integrity gates (integrity artifact):**

**C1** Valid ZIP; `document.xml` parses without error.

**C2** Q-count = Q_TOTAL; stems Q.1..Q.{Q_TOTAL} in document order, no gaps.

**C3** Every Q-stem preceded by exactly 5 tag paragraphs in correct label
order: Subject / Topic / Subtopic / Question Type / Complexity.

**C4** Strip complete: zero header paragraphs remain before Q.1.

**C5** OMML count unchanged: `<m:oMath>` count in integrity == source.

**C6** Drawing count unchanged: `<w:drawing>` count in integrity == source.

**C7** NAVY color (003366) count unchanged: Correct Answer line colors preserved.

**C8** DocPr IDs unique across the entire document.

**C9** No dangling references: every `*.rels` relationship resolves; every
`[Content_Types].xml` Override resolves.

**C10** No blank tag value: every Subject/Topic/Subtopic/Question Type/Complexity
non-empty for all tag blocks.

**Render-source gates:**

**C11** Math conservation: OMML count from C5 == linearized count; zero residual
`<m:oMath>` in render-source.

**C12** Render-source docx valid ZIP; document.xml parses.

**C13** Text conservation: Q.1..Q.{Q_TOTAL} present; tag label counts match;
`Correct Answer:` count matches source.

**C14** Math + symbol round-trip: linearized strings appear verbatim in
extracted text; non-ASCII codepoints exact.

**C15** Stem-underline recolor: underlined stem runs carry FF0000; no color
changes on options/explanations/tags; NAVY count unchanged.

**Namespace/reference/order integrity:**

**C16** (a) mc:Ignorable coverage — every prefix declared. (b) Namespace superset
— no xmlns dropped vs source. (c) No dangling relationships. (d) Tag-block
pPr order: spacing before jc.

**Portal charset:**

**C17** NAT Correct-Answer portal charset: every NAT question's rendered value
matches `0123456789.-` exactly. Scoped by question_type (not pattern-matched).
Any violation → HARD STOP (last gate in the pipeline).

---

# §8 — PYQ registry

PYQ-4 maintains `[ExamCode]_pyq_registry.json` — a corpus-level progress tracker
for PYQ paper delivery.

## S8-1 — Registry schema

```json
{
  "exam_code": "[ExamCode]",
  "papers_completed": [
    {
      "date_session": "12-Sep-2025_Shift_1",
      "questions": 100,
      "delivered_at": "2026-07-22T14:30:00Z",
      "output_file": "[ExamCode]_12-Sep-2025_Shift_1_PYQ_Final.docx"
    }
  ],
  "papers_in_progress": [],
  "total_papers_delivered": 1,
  "total_questions_delivered": 100
}
```

## S8-2 — Registry operations

- **Before delivery**: check if this date_session is already in `papers_completed`.
  If yes → WARN and require explicit confirmation to re-deliver.
- **After delivery**: add/update the entry in `papers_completed` with the current
  timestamp. Increment `total_papers_delivered` and `total_questions_delivered`.
- **First run**: if the registry file does not exist, create it with empty arrays.

## S8-3 — Registry storage

The registry is saved to `/home/claude/` (chat-scoped) and presented for the user
to upload to project knowledge for persistence across sessions. The user manages
the registry file in their project — PYQ-4 reads it if present and writes the
updated version.

---

# §9 — Delivery

PYQ-4 delivers in a single response:

1. All gates (§7 C1-C17) pass.
2. PYQ registry updated (§8).
3. Present `[ExamCode]_[date]_[session]_PYQ_Final.docx` via present_files.
4. Upload to Google Drive (if Drive access is available; otherwise instruct the
   user to upload manually).
5. Print the delivery report (§10).
6. Render the post-delivery footer per Framework_DeliveryFooter.md:
   - F2 (step-complete, GREEN).
   - File badges: `📁 Use locally` for PYQ_Final.docx,
     `📤 Upload to Project Files` for pyq_registry.json (if new) or
     `🔁 Replace in Project Files` (if updating existing registry).
   - Next-step reference: "PYQ pipeline complete for [ExamCode] [date] [session].
     Next paper: run PYQ-1 (PYQExplain) for the next PYQ paper in a new chat."

---

# §10 — Delivery report

Printed in chat after present_files:

- **§R1 — Scope.** Exam, paper (date, session), Q_TOTAL, question types (MCQ/MSQ/NAT split).
- **§R2 — Tag summary.** Total tag blocks inserted. Subject/Topic/Subtopic distribution.
- **§R3 — Complexity.** All questions tagged with "[difficulty_default]" (hardcoded per D4).
- **§R4 — Render transforms.** OMML linearized count, safe-font resolutions, underline recolor count.
  Any unresolved non-ASCII codepoints listed.
- **§R5 — Gate results.** C1-C17 all PASS (or list failures).
- **§R6 — PYQ registry.** Papers delivered to date, total questions, corpus progress.
- **§R7 — Note.** "This is the portal-ready document. Open in Microsoft Word to
  verify. For student download, run PYQ-3 (PYQFormat) separately in a new chat —
  it takes PYQ-2 output directly."
- **§R8 — Regression alarms.** Any header paragraphs detected and stripped (should
  be zero on a clean PYQ-2 output).

---

# §11 — Definition of done

PYQ-4 is done when **all** hold:

1. The input document opened and Q_TOTAL was determined.
2. The q_to_classification map was loaded with COMPLETE coverage (1..Q_TOTAL).
3. All 5 tag values resolved for every question (§2).
4. Every Q-stem preceded by exactly 5 correctly ordered tag paragraphs.
5. ZERO content mutated (zero-mutation rule).
6. Integrity artifact passes C1-C10.
7. Render-source artifact passes C11-C17.
8. No residual OMML in render-source. All non-ASCII safe-fonted.
9. PYQ registry updated with this paper.
10. Delivered via present_files with the delivery report and footer.
11. Opens clean in Microsoft Word with no "unreadable content" prompt.

**Hard invariants (never violated):**

- No text content is modified in the integrity artifact.
- OMML is linearized ONLY in the render-source (never in the integrity artifact).
- The render-source is the ONLY delivered file. No `soffice` conversion.
- No `cleanup_namespaces()` — ever (MockDeliver v1.3 lesson).
- `word/webSettings.xml` is never stripped (MockDeliver v1.3 lesson).
- Tag pPr: `<w:spacing>` before `<w:jc>` (OOXML schema order).
- Tag paragraphs built from scratch, never cloned from body paragraphs.
- No exam-specific value hardcoded (exam-agnostic guarantee).

---

# §12 — Edge cases

1. **q_to_classification map missing** → HARD STOP with message (§0).

2. **Partial map (covers 90 of 100 Qs)** → HARD STOP. Unlike PYQ-3 (which WARNs
   and omits pills), PYQ-4 requires COMPLETE coverage because the portal requires
   every question to be tagged.

3. **exam_config.json missing** → WARN. Use ExamCode as exam_name. Use "Medium"
   as difficulty_default.

4. **Paper already delivered (registry)** → WARN + require confirmation. If
   confirmed, re-deliver and update the registry entry.

5. **Input is PYQ-1 output (not PYQ-2)** → ACCEPTED with WARN noting the
   document has not been audited.

6. **NAT question with bad grading value** → C17 catches it as HARD STOP.

7. **Document with no OMML** → Fine. Linearization count = 0. Gates still pass.

8. **Document with no images** → Fine. Drawing count = 0. Gates still pass.

9. **Non-ASCII codepoints not in safe font stack** → Kept in original font,
   logged in report. Not a HARD STOP (Word can substitute).

10. **Google Drive unavailable** → Deliver locally via present_files. Instruct
    user to upload manually. Not a HARD STOP.

11. **Registry file does not exist** → Create new one. Normal on first PYQ paper.

12. **Re-run on same paper** → Registry detects duplicate, WARNs, re-delivers on
    confirmation. Output overwrites the previous _PYQ_Final.docx.

13. **Already-formatted doc attached by mistake (_PYQ_Formatted.docx)** → Detect
    from filename and HARD STOP: "This is the PYQ-3 formatted document. PYQ-4
    takes the PYQ-2 output (_PYQ_Explanation_Complete.docx) directly."

---

# §13 — Implementation notes

## S13-1 — Reused patterns from MockDeliver

The following MockDeliver patterns are reused identically:
- `make_tag_para(label, value)` — tag paragraph builder (§4-3 from MockDeliver)
- `detect_header_paras(body_children)` — safety-net header strip
- `reassign_docpr_ids(root)` — DocPr ID dedup
- `replace_omath_with_text(root, font)` — Rule 19 OMML linearization
- `recolor_underlined_stems(root, color)` — Rule 22 stem recolor
- `apply_symbol_safe_font(root, default_font)` — Rule 21 safe-font
- `gate_c16(src, out, labels)` — namespace/reference/order gate
- `gate_c17_natcharset(out, tag_lookup)` — NAT portal charset gate
- Two-artifact assembly (integrity + render-source ZIP construction)
- All namespace preservation rules (no cleanup_namespaces, keep webSettings.xml)

These are NOT engine functions — they are standalone document-transform utilities
from MockDeliver, reproduced in PYQ-4's pipeline script.

## S13-2 — PYQ-specific differences from MockDeliver

| Aspect | MockDeliver (Step 11) | PYQDeliver (PYQ-4) |
|---|---|---|
| Tag data source | registry.json + blueprint.json JOIN | q_to_classification direct lookup |
| Question Type | marking_scheme (position-based) or subtopic (subtopic-based) | options_by_q (structure-based) |
| Complexity | Per-Q from registry.difficulty | HARDCODED from exam_config.difficulty_default |
| Paper identity | pp.paper\_slug() via paper\_pipeline.py | Parsed from attached filename |
| Blueprint | Required | Not required (does not exist for PYQ) |
| Registry | Required | Not required (does not exist for PYQ) |
| PYQ registry | N/A | Maintained by PYQ-4 (§8) |
| Trigger | TestDeliver P[N] / MockDeliver M[N] | PYQDeliver (no arguments needed) |

## S13-3 — Namespace preservation (MockDeliver v1.3 lessons)

When assembling both the integrity and render-source docx:
- Do NOT call `etree.cleanup_namespaces()` — this strips xmlns declarations
  that `mc:Ignorable` and drawing content reference, causing Word to show
  "unreadable content" errors.
- Do NOT strip `word/webSettings.xml` — this causes dangling relationships
  and dangling Overrides.
- DO preserve all existing namespace declarations on the root element exactly.
- DO use `zipfile.ZIP_STORED` for `[Content_Types].xml`, `_rels/.rels`, and
  `word/_rels/document.xml.rels`; `ZIP_DEFLATED` for everything else.

---

# APPENDIX A — Tag constants

```text
TAG_LABELS = ['Subject', 'Topic', 'Subtopic', 'Question Type', 'Complexity']

TAG PARAGRAPH STYLE:
  Font    : Arial, 11pt
  Align   : Left
  Spacing : 0pt before, 0pt after, 240 twips line
  Color   : Default (auto)

PORTAL GRADING CHARSET (NAT only):
  Allowed : 0123456789.-
  Format  : plain number (-?\d+(\.\d+)?) or lo-hi range (\d+(\.\d+)?-\d+(\.\d+)?)

RENDER-SAFE FONT STACK:
  Primary : DejaVu Sans (covers most Unicode, math symbols)
  Fallback: FreeSans (covers section markers ❌ ⬛ ✅ ⚡)
```

---

**End of Framework_PYQDeliver.md (v1.0)**
