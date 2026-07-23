# Framework_PYQDeliver v1.2.1 — Universal PYQ Portal Tagger & Delivery Engine
# [ExamCode] project | PYQ-4 (PYQDeliver) | Exam-agnostic
#
# v1.2.1 — 2026-07-23 — Line-by-line adversarial audit fixes (3):
#   (1) exam_config.marks_default was read in §2-3b but declared nowhere —
#       now defined in §0 item 2 as an OPTIONAL positive number, fallback 1.
#   (2) Per-question JSON map keys (q_to_classification / options_by_q /
#       q_to_difficulty) — JSON keys are strings; explicit int-normalization
#       rule added to §0 item 3 so Tier-1 lookups can never silently miss.
#   (3) exam_config/difficulty_labels absent no longer collapses every Q to
#       Tier 3: §0 item 2 now defaults difficulty_labels to
#       ['Easy','Medium','Hard'] (MockDeliver parity), keeping Tier 2
#       functional; C10 therefore always has a vocabulary (degraded-check
#       clause removed); edge case 3 updated to match.
#
# v1.2 — 2026-07-23 — Complexity tag: hardcode → three-tier deterministic
#   resolver (§2-3, D11 supersedes D4). v1.1 tagged every question with
#   exam_config.difficulty_default ("Medium" fallback). v1.2 resolves per-Q
#   Complexity through a deterministic tier chain: Tier 1 = q_to_difficulty
#   from the progress JSON (future PYQ-1 assessment — activates automatically
#   when present); Tier 2 = E-9 score_difficulty on the stem via
#   blueprint_core.py (canonical shared copy of Step 5's 3-axis scorer,
#   extracted this session — Cluster E), levels mapped through the fixed
#   Blueprint §7 S7-6 ordinal alias into difficulty_labels; Tier 3 =
#   difficulty_default (v1.1 behavior, now the safety net only).
#   blueprint_core.py becomes a REQUIRED input (§0). Gate C10 extended:
#   Complexity values must be members of difficulty_labels, not merely
#   non-empty. §R3 now reports tier provenance + level distribution.
#   New edge cases 16-19.
#
# v1.1 — 2026-07-23 — Date/Session tag removal (§4A). The per-question
#   date/session tag paragraph (PYQSort date_label, e.g. "[12-Sep-2025 Shift 1]"
#   or "[15-Jun-2025]") that rides through PYQ-1/PYQ-2 above every Q-stem is
#   internal pipeline metadata, not portal content. v1.0 had no removal step,
#   so every question in _PYQ_Final.docx carried its date/session tag — and
#   S5-3's header-strip mis-fired on Q.1's label (false REGRESSION ALARM)
#   while leaving Q.2..Qn labels in place. v1.1 removes ALL date/session tag
#   paragraphs FIRST (before header stripping and tag insertion), mirroring
#   Framework_PYQFormat.md §4 (v1.1) exactly: same DATE_TAG_RE, same
#   media-safety gate, same tags_removed/tags_skipped accounting. Gate C4
#   extended to verify zero date/session tags remain. New decision D10.
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
#     D4. [SUPERSEDED BY D11 in v1.2] DIFFICULTY HARDCODED. All PYQ questions
#         got the same difficulty label (exam_config.difficulty_default,
#         fallback "Medium"). Retained as the Tier-3 safety net only.
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
#     D9. EXPLAIN ENGINE NOT REQUIRED. PYQ-4 reads the docx structurally
#         (Q-stems, tag insertion, render transforms). No explain_engine.py
#         needed. (v1.2 note: blueprint_core.py IS required — see D11/§0 —
#         but only for the pure Cluster E scoring functions, no allocation.)
#     D10. DATE/SESSION TAGS REMOVED (v1.1). The per-question date/session
#         tag paragraph (PYQSort date_label) is stripped from the delivered
#         document. It is internal pipeline metadata; the paper's identity is
#         already carried by the output filename and the PYQ registry entry.
#         Same decision as PYQFormat D8 — both PYQ-2 forks remove it.
#     D11. COMPLEXITY VIA DETERMINISTIC TIER CHAIN (v1.2, supersedes D4).
#         Per-question Complexity resolves through §2-3's three tiers:
#         (1) q_to_difficulty from the progress JSON, (2) E-9 3-axis scoring
#         via blueprint_core.py, (3) difficulty_default. Tiers 2-3 are pure
#         functions — same document always yields the same tags on every run
#         and every model instance. Tier 2 puts PYQ papers on the SAME
#         difficulty scale the blueprint/mock pipeline is calibrated on
#         (Step 5 runs the identical scorer on the PYQ corpus), so portal
#         Complexity is comparable across PYQ and mock papers. Known honest
#         limit: keyword-driven axes under-differentiate pure theory/recall
#         exams (most stems score 3 → labels[0]); Tier 1 is the designed
#         upgrade path for those exams and requires no PYQ-4 change.

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
- **Remove** the per-question date/session tag paragraphs (§4A) — the ONLY
  element ever deleted, matched by an anchored full-paragraph regex (v1.1)
- **Insert** 5-line tag blocks before each Q-stem (new content only)
- **Linearize** OMML → Unicode text on the render-source copy only
- **Re-font** non-ASCII spans to a safe font on the render-source copy only
- **Recolor** directly-underlined runs in question stems to red FF0000 on the
  render-source copy only

It **NEVER**:
- Changes any character in any question stem, option, table, image, or explanation
- Reorders questions
- Removes, rewrites, or paraphrases any content other than the date/session
  tag paragraphs sanctioned by §4A
- Modifies the integrity artifact in any way other than removing date/session
  tag paragraphs (§4A) and inserting tag blocks

Violation of this rule is a hard failure regardless of any other outcome.

---

# §0 — Input / output contract

**Inputs:**

1. `[ExamCode]_[date]_[session]_PYQ_Explanation_Complete.docx` — the PYQ-2 audited
   explanation document. Attached by user. This is the same input PYQ-3 uses (FORK).
   ALSO ACCEPTS: `_PYQ_Explanation.docx` (PYQ-1 output, if audit not yet run).
   The spec prefers the audited version.

2. `exam_config.json` — in project knowledge. Provides `exam_name`, `difficulty_default`
   (fallback "Medium"), and `difficulty_labels` (fallback ['Easy','Medium','Hard'] —
   MockDeliver parity — when the field or the whole file is absent/unusable; WARN).
   OPTIONAL field `marks_default` (v1.2): a positive number giving the exam's
   uniform per-question marks, used ONLY for E-9 threshold scaling in §2-3b
   Tier 2. Absent, non-numeric, or non-positive → 1. No other step reads it.

3. `q_to_classification` map — the per-question {subject, topic, subtopic,
   subtopic_id} mapping. KEY NORMALIZATION (v1.2, applies equally to
   `options_by_q` and `q_to_difficulty`): JSON object keys are always
   strings — on load, normalize every per-question map to int keys via
   `{int(k): v}` and perform all lookups with the int question number.
   A key that cannot int-parse → HARD STOP naming the map and the key. Loaded from ONE of these sources (in priority order):
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

6. `blueprint_core.py` — REQUIRED from v1.2. Loaded dual-path: the framework
   clone (`/tmp/fw`, GitHub model) FIRST, falling back to the project Files
   (`/mnt/project`, direct-upload model) — either location satisfies the
   mandate, so GitHub-connected projects need no per-project engine upload.
   Provides the Cluster E pure functions for Tier-2 Complexity resolution
   (§2-3): `score_difficulty`, `determine_strip_mode`, `map_difficulty_level`.
   If absent from BOTH locations → HARD STOP:
     "blueprint_core.py not found in the framework clone (/tmp/fw) or the
      project Files (/mnt/project). It is required for per-question Complexity
      resolution (v1.2). Reload the framework (Step 0) or upload it, then re-run."

7. `q_to_difficulty` map — OPTIONAL. Per-question {q: label} difficulty map
   from the same progress JSON as q_to_classification (§0 item 3 priority
   order). Present only if PYQ-1 has performed per-question difficulty
   assessment (future capability). When present and valid it is Tier 1 of
   §2-3; when absent PYQ-4 proceeds on Tier 2 with no WARN.

NOT REQUIRED (PYQ-4 does not use mock pipeline outputs):
  ✗ blueprint.json — does not exist for PYQ papers
  ✗ registry.json — does not exist for PYQ papers
  ✗ explain_engine.py — no explanations written or read
  ✗ explain_audit_gate.py — no audit performed
  ✗ paper_pipeline.py — filenames derived from the attached document
  (blueprint_core.py IS required from v1.2 — §0 item 6 — but only its pure
   Cluster E scoring functions; none of its allocation machinery runs.)

**Outputs:**

- `[ExamCode]_[date]_[session]_PYQ_Final.docx` — the tagged, render-safe document
  for portal upload. Every Q-stem preceded by 5 tag lines. Per-question
  date/session tag paragraphs removed (§4A). OMML linearized to Unicode.
  Non-ASCII safe-fonted. Underlined stems recolored red.
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
   Also load `q_to_difficulty` from the same JSON if present (§0 item 7,
   optional — Tier 1 of §2-3).

5a. **blueprint_core.py**: resolve it dual-path — the framework clone
   (`/tmp/fw/blueprint_core.py`) FIRST, else the project Files
   (`/mnt/project/blueprint_core.py`) — and verify it exposes
   `score_difficulty`, `determine_strip_mode`, `map_difficulty_level`
   (Cluster E). Absent from both, or missing a function → HARD STOP (§0 item 6).

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
| 5 | Complexity | §2-3 three-tier resolver | Tier 1 q_to_difficulty → Tier 2 E-9 scoring → Tier 3 difficulty_default (D11) |

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

## S2-3 — Complexity (difficulty) — three-tier deterministic resolver (D11, v1.2)

Complexity is resolved PER QUESTION through a deterministic tier chain.
For each question q (first tier that yields a value wins):

```text
TIER 1 — q_to_difficulty[q]         (progress JSON, if the map is present)
TIER 2 — E-9 score_difficulty(stem) (blueprint_core.py — always computable)
TIER 3 — difficulty_default          (exam_config, fallback "Medium")
```

### S2-3a — Tier 1: q_to_difficulty (upstream assessment)

If the progress JSON carries a `q_to_difficulty` map (§0 item 7):
- Accept `q_to_difficulty[q]` if and only if the value is a string AND a
  member of `difficulty_labels`. Record tier=1 for this q.
- Value absent for this q, wrong type, or not in `difficulty_labels` →
  WARN once per defect (with q number and offending value) and fall
  through to Tier 2. NEVER trust an unvalidated Tier-1 value.
- The whole map absent → silent (normal today); all questions use Tier 2.

### S2-3b — Tier 2: E-9 3-axis scoring (canonical path today)

Import `blueprint_core.py` (Cluster E — the canonical shared copy of Step 5's
E-9/E-10, under its CROSS-FILE SYNC RULE), resolved dual-path — the framework
clone (`/tmp/fw`) FIRST, else the project Files (`/mnt/project`):

```python
import os, shutil, sys
_engine_src = next((p for p in ('/tmp/fw/blueprint_core.py',
                                '/mnt/project/blueprint_core.py')
                    if os.path.exists(p)), None)
if _engine_src is None:
    raise SystemExit(
        "HARD STOP (ENGINE MANDATE): blueprint_core.py not found in the framework "
        "clone (/tmp/fw) or the project Files (/mnt/project). Reload the framework "
        "(Step 0) or upload the engine, then re-run.")
shutil.copy(_engine_src, '/home/claude/blueprint_core.py')
sys.path.insert(0, '/home/claude')
from blueprint_core import score_difficulty, determine_strip_mode, map_difficulty_level
```

```text
strip_mode = determine_strip_mode(subject, topic, subtopic)
               with subject/topic/subtopic from q_to_classification[q]
is_msq     = (resolved Question Type for q == 'MSQ')   # §2-2, already computed
marks      = exam_config.marks_default if it is a positive number, else 1
               (the PYQ pipeline does not track per-question marks — a
                uniform value is a documented, deterministic simplification;
                for uniform-marks exams it is also exactly correct)
result     = score_difficulty({'stem': stem_text, 'is_msq': is_msq},
                              marks=marks, strip_mode=strip_mode)
value      = map_difficulty_level(result['level'], difficulty_labels)
```

`stem_text` is the question's full stem: all `<w:t>` run text of the Q-stem
region concatenated in document order, `.strip()`ed — the SAME text layer
gates C2/C13 read. OMML content is not part of the text layer and therefore
not visible to the V axis; this matches Step 5's own extraction behavior
(parity by construction, documented, not a defect).

`map_difficulty_level` applies the fixed Blueprint §7 S7-6 ordinal alias
(Simple→labels[0], Medium→labels[1], Hard→labels[2]). It returns None —
forcing Tier 3 — when `difficulty_labels` is not an exactly-3-label list:
a 2- or 5-band custom vocabulary has no defensible correspondence to a
3-level scorer, and PYQ-4 must not guess.

`difficulty_labels` here is the §0 item 2 value INCLUDING its fallback:
when exam_config.json (or the field) is absent/unusable, the defaulted
['Easy','Medium','Hard'] keeps Tier 2 fully functional (MockDeliver
parity) — a missing config degrades vocabulary, never per-Q resolution.
Only a PRESENT custom non-3-label set forces Tier 3.

If `value` is not None → record tier=2 for this q. Else fall to Tier 3.

### S2-3c — Tier 3: difficulty_default (safety net — v1.1 behavior)

- Read `difficulty_default` from exam_config.json; if unset use "Medium".
- If the value is not in `difficulty_labels` → append it conceptually: the
  tag is still emitted (the portal accepts any string) but gate C10 will
  report the vocabulary violation as a HARD STOP — fix exam_config.
- Record tier=3 with a WARN naming the reason (empty stem / non-3-label
  set / other). On a normal run tier-3 count is ZERO.

### S2-3d — Determinism guarantee

Tiers 2 and 3 are pure functions of (document, project files). Tier 1 is a
pure lookup. Therefore the SAME inputs produce the SAME Complexity tags on
every run and every model instance — no model judgment participates in
tag resolution at PYQ-4 time.

### S2-3e — Provenance accounting

Track `tier_counts = {1: n1, 2: n2, 3: n3}` and the per-label distribution
of resolved values. Both are reported in §R3 and both feed gate C10.

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
2. bash_tool    → run it (parse → remove date/session tags (§4A) →
                  build tag lookup → insert tags →
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

Date/session tag removal (§4A) runs on the working body BEFORE the integrity
artifact is assembled — therefore NEITHER artifact contains date/session tags.

---

# §4A — Date/Session tag removal (v1.1)

The input document carries a per-question date/session tag paragraph — the
PYQSort `date_label` line that sits immediately above each Q-stem and rides
through PYQExplain/PYQExplainAudit unchanged:

```text
[12-Sep-2025 Shift 1]     (multi-session exam, keyword from exam_config)
[02-Feb-2025 Session 2]   (GATE-style keyword)
[15-Jun-2025]             (single-session exam — no keyword/number)
```

These tags are internal pipeline metadata, not portal content (D10). The
paper's identity is already carried by the output filename and the PYQ
registry entry. PYQ-4 removes every tag paragraph from the document body.

This section MIRRORS Framework_PYQFormat.md §4 (v1.1) — PYQ-3 and PYQ-4 are
independent forks of the PYQ-2 output, so each performs its own removal.
CROSS-FILE SYNC RULE: any change to DATE_TAG_RE or the removal algorithm in
either spec MUST be applied to both in the same session.

## S4A-1 — Tag matching regex

```python
import re

# Keyword-agnostic, anchored full-paragraph match.
# DELIBERATE DIVERGENCE from PYQSort's build_date_label_re(): PYQSort needs
# the exact session_keyword from exam_config.json because it PARSES the
# session number for sorting. PYQ-4 only needs to RECOGNIZE the tag for
# deletion, and must work even when exam_config.json is absent (§12 case 3
# WARN). [A-Za-z]+ therefore matches ANY session keyword (Shift, Slot,
# Phase, Paper, Session, Morning, Afternoon, or custom).
DATE_TAG_RE = re.compile(
    r'^\[\d{1,2}-[A-Za-z]{3}-\d{4}'   # [DD-Mon-YYYY
    r'(?:\s+[A-Za-z]+\s+\d+)?'        # optional: <keyword> <number>
    r'\]$'                            # ] — anchored: FULL paragraph only
)
```

A paragraph is a tag if and only if its FULL reconstructed text (all `<w:t>`
runs concatenated, then `.strip()`) matches DATE_TAG_RE. The anchors guarantee
PYQ-4 can never partially delete text: a stem or explanation that merely
CONTAINS a date label inline (e.g. "This question appeared in
[12-Sep-2025 Shift 1] and asks…") does not match and is never touched.

## S4A-2 — Removal algorithm

1. Walk every body-level `<w:p>` element of `word/document.xml`.
2. Reconstruct its full text from all `<w:t>` descendants; `.strip()`.
3. If the text matches DATE_TAG_RE:
   a. SAFETY GATE: if the paragraph contains any `<m:oMath>` or `<w:drawing>`
      descendant, SKIP removal for that paragraph and WARN (a real tag never
      contains media — this is defensive; deleting it would break gates C5/C6).
   b. Otherwise remove the `<w:p>` from its parent `<w:body>`.
4. Record `tags_removed` (count deleted) and `tags_skipped` (safety-gate skips).

Removal runs FIRST — before header stripping (S5-3) and tag insertion (S5-2) —
so all subsequent position arithmetic operates on the tag-free body, and S5-3
no longer mis-detects Q.1's date label as a stray header paragraph.

## S4A-3 — Removal outcomes

- `tags_removed ≥ 1` → normal. Reported in §R2.
- `tags_removed == 0` → WARN (not HALT): "No date/session tag paragraphs
  found — document may predate tagging or tags were already removed."
  Delivery proceeds.
- `tags_skipped ≥ 1` → WARN with position and reason for each skip. Delivery
  proceeds. Gate C4's date-tag check tolerates residuals ONLY in the exact
  count `tags_skipped` (same accounting as PYQFormat's residual-tag
  verification check) — any
  residual beyond that is a C4 failure.

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
Runs AFTER §4A removal — Q.1's date/session tag has already been removed by
then, so on a clean PYQ-2 output this finds ZERO (the tag-free document is
questions + explanations only). Any hits are stripped and a REGRESSION ALARM
is raised in the report. (v1.0 bug, fixed in v1.1: without §4A running first,
this step mis-fired on Q.1's date label — a legitimate pipeline artifact, not
a regression — while Q.2..Qn labels were left in the delivered document.)

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

**C4** Strip complete: zero header paragraphs remain before Q.1, AND
residual date/session tag paragraphs (full-paragraph DATE_TAG_RE matches,
§4A) anywhere in the body == `tags_skipped` (0 in the normal case).

**C5** OMML count unchanged: `<m:oMath>` count in integrity == source.

**C6** Drawing count unchanged: `<w:drawing>` count in integrity == source.

**C7** NAVY color (003366) count unchanged: Correct Answer line colors preserved.

**C8** DocPr IDs unique across the entire document.

**C9** No dangling references: every `*.rels` relationship resolves; every
`[Content_Types].xml` Override resolves.

**C10** No blank tag value: every Subject/Topic/Subtopic/Question Type/Complexity
non-empty for all tag blocks. ADDITIONALLY (v1.2): every Complexity value must
be a member of `difficulty_labels` — a non-member (e.g. a misconfigured
difficulty_default) is a HARD STOP naming the offending value and its tier.
The membership vocabulary is the §0 item 2 value including its
['Easy','Medium','Hard'] fallback, so C10 always has a vocabulary to
check against — there is no degraded mode.

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
  Date/session tag paragraphs removed (`tags_removed`, §4A); any safety-gate
  skips (`tags_skipped`) listed with position and reason.
- **§R3 — Complexity.** Tier provenance counts (Tier 1 / Tier 2 / Tier 3, §2-3e)
  and the per-label distribution of resolved Complexity values. Any Tier-1
  validation WARNs and any Tier-3 fallbacks listed with q number and reason.
  On a normal run today: Tier 2 = Q_TOTAL, Tiers 1/3 = 0.
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
5. ZERO content mutated (zero-mutation rule) — the ONLY deletions are the
   date/session tag paragraphs removed per §4A accounting.
5a. Every date/session tag paragraph removed (§4A) — residuals == tags_skipped
   (0 in the normal case), verified by gate C4.
6. Integrity artifact passes C1-C10.
7. Render-source artifact passes C11-C17.
8. No residual OMML in render-source. All non-ASCII safe-fonted.
9. PYQ registry updated with this paper.
10. Delivered via present_files with the delivery report and footer.
11. Opens clean in Microsoft Word with no "unreadable content" prompt.

**Hard invariants (never violated):**

- No text content is modified in the integrity artifact.
- The date/session tag paragraphs (§4A) are the ONLY elements ever removed —
  matched by anchored full-paragraph DATE_TAG_RE, protected by the media
  safety gate. Nothing else is ever deleted from either artifact.
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

3. **exam_config.json missing** → WARN. Use ExamCode as exam_name, "Medium"
   as difficulty_default, and ['Easy','Medium','Hard'] as difficulty_labels
   (§0 item 2 fallback — MockDeliver parity). Tier 2 stays fully
   functional; only the vocabulary is defaulted, never the per-Q resolver.

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

14. **No date/session tag paragraphs in the document** → WARN (not HALT,
    S4A-3): document may predate tagging or tags were already removed.
    Delivery proceeds; `tags_removed = 0` reported in §R2.

15. **Date-tag-shaped paragraph containing `<m:oMath>` or `<w:drawing>`** →
    S4A-2 safety gate SKIPs it, WARNs with position, counts it in
    `tags_skipped`. Gate C4 tolerates exactly `tags_skipped` residuals.
    An inline date label inside a stem/explanation is NEVER at risk — the
    anchored regex only matches full paragraphs.

16. **blueprint_core.py missing or lacking Cluster E functions** → HARD STOP
    (§0 item 6 / §1 step 5a). Absent from BOTH the framework clone (/tmp/fw)
    and the project Files (/mnt/project): the operator reloads the framework
    (Step 0) or uploads the current blueprint_core.py, then re-runs.

17. **q_to_difficulty present but defective** (value missing for some q,
    wrong type, or not in difficulty_labels) → per-q WARN + Tier-2
    fallthrough (S2-3a). A defective Tier-1 map can never block delivery
    and can never inject an out-of-vocabulary tag.

18. **Non-3-label difficulty_labels** (2-band or 5-band custom set) →
    `map_difficulty_level` returns None → Tier 3 for every question, each
    WARNed, difficulty_default used (must itself be in the label set or
    C10 HARD STOPs). Deterministic; never guesses an ordinal mapping.

19. **Theory/recall-heavy exam** (stems with no computation keywords,
    numbers, or indirection patterns) → most questions legitimately score
    C+I+V=3 → labels[0]; negative-phrasing and MSQ terms still
    differentiate. This is a documented signal limit of keyword axes, not
    a bug — the §R3 distribution makes it visible, and Tier 1 (PYQ-1
    assessment) is the designed upgrade path requiring no PYQ-4 change.

---

# §13 — Implementation notes

## S13-1 — Reused patterns from MockDeliver

The following MockDeliver patterns are reused identically:
- `remove_date_session_tags(root)` — §4A removal (from PYQFormat §4, not
  MockDeliver — mock papers carry no date labels; subject to the §4A
  CROSS-FILE SYNC RULE with Framework_PYQFormat.md)
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

EXCEPTION (v1.2): the Complexity Tier-2 functions (`score_difficulty`,
`determine_strip_mode`, `map_difficulty_level`) are NOT reproduced in the
pipeline script — they are IMPORTED from `blueprint_core.py`, resolved
dual-path (`/tmp/fw` first, else `/mnt/project` — §2-3b) (Cluster E, the
canonical shared copy). Reproducing them inline would create a fourth copy
of E-9 and is FORBIDDEN (anti-drift principle).

## S13-2 — PYQ-specific differences from MockDeliver

| Aspect | MockDeliver (Step 11) | PYQDeliver (PYQ-4) |
|---|---|---|
| Tag data source | registry.json + blueprint.json JOIN | q_to_classification direct lookup |
| Question Type | marking_scheme (position-based) or subtopic (subtopic-based) | options_by_q (structure-based) |
| Complexity | Per-Q from registry.difficulty | Per-Q three-tier resolver: q_to_difficulty → E-9 scoring (blueprint_core Cluster E) → difficulty_default (§2-3, D11) |
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

**End of Framework_PYQDeliver.md (v1.2.1)**
