# Framework_PYQDeliver v1.13 — Universal PYQ Portal Tagger & Delivery Engine
# v1.13 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE. Complexity Tier 2 (E-9 keyword
#   scoring) RETIRED with the scorer itself (MockTestAnalyse v2.55, blueprint_core): Tier 1
#   (assessed) → Tier 1.5 (structural) → Tier 3 (default). The §2-3e mixed-provenance WARN now
#   names Tier 3; R3 / EC-17 / EC-19 updated; the engine mandate requires only
#   structural_difficulty. Operator decision 2026-08-27. No tagging or delivery change.
# v1.12 — 2026-08-13 — TIER 0 ERA GUARD closes an era-blind Tier-1 defect surface
#   (PROJECT OVERRIDE for IIT_JAM_BIOTECHNOLOGY; proposed upstream for the repo).
#   ROOT CAUSE: S2-2a's Tier 1 is a literal, era-blind position lookup against
#   exam_config.marking_scheme whenever marking_scheme carries >1 distinct
#   question_type — with NO check that marking_scheme (which describes the
#   CURRENT pattern) actually describes the PAPER being delivered. Measured on
#   IIT JAM Biotechnology 07-May-2005: a 100-question, structurally all-MCQ
#   legacy paper (options_by_q == 4 for every Q, zero NAT-shaped questions;
#   PYQExplain's own qtype map already resolved all 100 as 'mcq') delivered
#   against the CURRENT 60-question MCQ/MSQ/NAT config. Literal Tier 1 would
#   have tagged Q31-40 MSQ and Q41-60 NAT on the delivered portal file — a
#   portal answer-format and scoring defect (the exact class of error Tier 1
#   was introduced in v1.8 to FIX, now reproduced by the same mechanism against
#   an off-era paper). This is the identical class of defect Framework_PYQCore
#   EC-P9/EC-P9b and Framework_MockTestAnalyse/PYQAnalyse Cluster F already
#   name and solve at the CORPUS level via blueprint_core.classify_paper_era —
#   PYQDeliver simply never called it. FIX: new S2-2 TIER 0 — before Tier 1 may
#   fire for ANY question, classify the WHOLE PAPER once via the EXISTING
#   canonical `classify_paper_era` (blueprint_core.py Cluster F — imported, per
#   the S13-1 anti-drift principle, never reproduced). era != 'current' (paper
#   is 'larger' / 'smaller' / 'renumbered' / 'retyped' relative to exam_config)
#   -> Tier 1 is skipped for the WHOLE paper and resolution proceeds straight
#   to Tier 2 (authoritative qtype). era == 'current' -> Tier 1 proceeds exactly
#   as v1.11 specified. Deterministic, exam-agnostic, no model judgment, no
#   operator prompt required for this class of paper ever again. PROVENANCE:
#   this exact paper was already used as EC-P9's own worked example ("a
#   100-question 2005 paper against a 60-question current pattern") before this
#   fix existed — this release wires that already-documented case into
#   PYQDeliver's own resolver instead of leaving it undetected there.
#   Touched: §0 item 6 (dual-path import list), new §S2-2 TIER 0 section
#   (before S2-2a), S2-2 diagram, S2-2e provenance, §10 §R1, END sentinel.
# [ExamCode] project | PYQ-4 (PYQDeliver) | Exam-agnostic
#
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take the audited PYQ explanation document, JOIN per-question metadata
#   from the classification map, INSERT portal tag blocks, and deliver a tagged,
#   upload-ready Word document for the distribution portal — WITH ALL ORIGINAL
#   CONTENT PRESERVED, including native OMML math (v1.9: no linearization, no
#   render transforms). This is the portal-facing counterpart to PYQ-3 (which
#   produces the student-facing download).
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_PYQDeliver.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

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
#     PYQ-3  PYQFormat       → _PYQ_Formatted.docx        (student)
#     PYQ-4  PYQDeliver      → _PYQ_Final.docx             (portal)  ← THIS STEP
#     (PYQ-2 PYQExplainAudit RETIRED in v1.6. PYQ-3 and PYQ-4 are INDEPENDENT —
#      both take PYQ-1's _PYQ_Explanation.docx directly.)

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

The content of every question block is SACRED. PYQ-4 may only (v1.9):
- **Remove** the per-question date/session tag paragraphs (§4A) — the ONLY
  element ever deleted, matched by an anchored full-paragraph regex (v1.1)
- **Insert** 5-line tag blocks before each Q-stem (new content only)

Those two edits are the ONLY changes PYQ-4 makes to the delivered file. Nothing
else in the body is touched.

It **NEVER** (v1.9 — this now holds for the DELIVERED file, not merely an
undelivered "integrity" copy):
- **Linearizes, converts, or otherwise rewrites OMML math.** Every `<m:oMath>`
  is preserved byte-for-byte; the delivered OMML count equals the source
  (gates C5 + C11). The v1.8-and-earlier OMML→Unicode linearization (Rule 19)
  is RETIRED from the delivery path.
- **Re-fonts or recolors** any run. Rule 21 (non-ASCII safe-font) and Rule 22
  (underline recolor) are no longer applied to the delivered file (§6 retired).
- Changes any character in any question stem, option, table, image, chart, or
  explanation
- Reorders questions
- Removes, rewrites, or paraphrases any content other than the date/session
  tag paragraphs sanctioned by §4A

Violation of this rule is a hard failure regardless of any other outcome.

DELIVERED FILE = INPUT + (§5 tag blocks) − (§4A date/session tags). Byte-identical
otherwise — math, options, images, tables, charts, fonts, and colours all
preserved exactly as the input carried them.

---

# §0 — Input / output contract

**Inputs:**

1. `[ExamCode]_[date]_[session]_PYQ_Explanation.docx` — the PYQ-1 explanation
   document. Attached by user. This is the same input PYQ-3 uses (FORK). STANDARD input
   (v1.6: PYQ-2 PYQExplainAudit is retired).
   ALSO ACCEPTS (legacy): `_PYQ_Explanation_Complete.docx` — a pre-v1.6 PYQ-2 audited
   document. Still a valid explanation doc; accepted unchanged. No longer produced.

2. `exam_config.json` — in project knowledge. Provides `exam_name`, `difficulty_default`
   (fallback "Medium"), `difficulty_labels` (fallback ['Easy','Medium','Hard'] —
   MockDeliver parity — when the field or the whole file is absent/unusable; WARN),
   and `sections` (each with a `q_range`, read for structural question-type resolution
   in §2-3a1; same field Step 2a writes).

   `marking_scheme[]` (v1.5) — OPTIONAL list of per-range scoring rules, each
   `{q_range:[lo,hi], question_type, correct_marks, negative_marks}`. This is the
   SAME field Step 2a writes and Steps 7/9/11 already consume; PYQ-4 does not
   introduce it and must not invent it. Used for THREE things and nothing else:
     * Tier 1 POSITION-BASED Question Type resolution (§2-2a) — reads
       `question_type` per q_range when marking_scheme carries >1 distinct type
     * Tier 1.5 structural resolution (§2-3a1)
     * per-question marks for E-9 threshold scaling (§2-3b)
   Absent, empty, or malformed → Tier 1.5 is skipped for every question and marks
   fall back as below. NEVER a HARD STOP: legacy projects have no marking_scheme.

   `marks_default` (v1.2, RETAINED as a fallback only) — a positive number giving
   a uniform per-question marks value. From v1.5 it is consulted ONLY when
   marking_scheme yields no marks for a question. Absent, non-numeric, or
   non-positive → 1. No other step reads or writes this field, so in practice it
   is usually absent; that is expected and silent.

   MARKS RESOLUTION ORDER (v1.5 — fixed, never improvised): for each question q,
     (a) `correct_marks` of the FIRST marking_scheme entry whose q_range contains q,
         when that value is a usable positive finite number;
     (b) else `marks_default` if it is a positive number;
     (c) else 1.
   "Usable" excludes non-numeric values, NaN, infinities, zero and negatives — a
   NaN marks value propagated into E-9's threshold arithmetic makes every
   comparison false and silently forces the hardest band. Such a value is treated
   as absent and resolution continues at (b).
   The executing instance MUST NOT derive marks by any other route (max of all
   ranges, modal value, most-frequent type, or similar). A uniform value silently
   substituted for a graded one changes E-9's thresholds for the whole paper.

3. `q_to_classification` map — the per-question {subject, topic, subtopic,
   subtopic_id} mapping. KEY NORMALIZATION (v1.2, applies equally to
   `options_by_q` and `q_to_difficulty`): JSON object keys are always
   strings — on load, normalize every per-question map to int keys via
   `{int(k): v}` and perform all lookups with the int question number.
   A key that cannot int-parse → HARD STOP naming the map and the key. Loaded from ONE of these sources (in priority order):
   a. `[ExamCode]_[date]_[session]_pyq_explain_progress.json` — PYQExplain (v2.2.1) delivers
      this under the SAME stem as the docx. DERIVE the expected name from the attached docx's
      parsed identity ({EXAM}_{DATE_SESSION}) and load THAT file, so the map provably belongs to
      this paper. If only a different-stem or a bare `pyq_explain_progress.json` is present →
      WARN that its paper-identity is unverifiable before using it (the standard source)
   b. `pyq_audit_progress.json` sidecar (LEGACY — only if a pre-v1.6 PYQ-2 run left one)
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
   Provides `structural_difficulty` (Cluster E2, Tier 1.5 — v1.5) for Complexity
   resolution (§2-3); the Cluster E Tier-2 functions are RETIRED (v1.13).
   ALSO PROVIDES (v1.12) the Cluster F pure functions for the Question Type
   TIER 0 era guard (§S2-2): `classify_paper_era`, `type_resolver_from_config`,
   `exam_config_bounds`. Reused, never reproduced (S13-1 anti-drift principle) —
   this is the SAME function Framework_PYQCore EC-P9/EC-P9b and Framework_
   MockTestAnalyse/PYQAnalyse Cluster F already use for the identical concept.
   If absent from BOTH locations → HARD STOP:
     "blueprint_core.py not found in the framework clone (/tmp/fw) or the
      project Files (/mnt/project). It is required for per-question Complexity
      resolution (v1.2) and the Question Type era guard (v1.12). Reload the
      framework (Step 0) or upload it, then re-run."

7. `q_to_difficulty` map — OPTIONAL. Per-question {q: label} difficulty map
   from the same progress JSON as q_to_classification (§0 item 3 priority
   order). Produced by PYQ-1 §7A. When present and valid it is Tier 1 of §2-3;
   when absent PYQ-4 proceeds on Tier 2 with no WARN. NOTE (v1.6): PYQ-2's
   independent validation of this map (§10A) is retired, so Tier 1 is now
   PRODUCER-ONLY — PYQ-4 consumes PYQ-1's assessed values directly, after the
   same membership check in S2-3a. A defective value still falls through safely.

8. `qtype` map — OPTIONAL. Per-question {q: 'mcq'/'msq'/'nat'} type map from the
   same progress JSON as q_to_classification (§0 item 3 priority order). Same KEY
   NORMALIZATION as item 3. DELIVERED by PYQExplain v2.3+ as a fourth sidecar map
   (§S7A-4); a pre-v2.3 sidecar has no qtype key and that is expected. When
   present and valid it is Tier 2 of the Question Type resolver (S2-2b) — used
   only for single-type / subtopic-based exams, where Tier 1 (position-based
   marking_scheme) does not apply. A defective per-q value or an absent map falls
   through safely to Tier 3 (S2-2c); it never blocks delivery and never injects
   an out-of-vocabulary tag. NOTE: qtype does NOT override Tier 1 — on a
   position-based exam the exam's official marking_scheme is authoritative, so
   Tier 1 wins and qtype is not consulted.

NOT REQUIRED (PYQ-4 does not use mock pipeline outputs):
  ✗ blueprint.json — does not exist for PYQ papers
  ✗ registry.json — does not exist for PYQ papers
  ✗ explain_engine.py — no explanations written or read
  ✗ (no audit is performed by PYQ-4; PYQ-2 PYQExplainAudit and its gate are retired)
  ✗ paper_pipeline.py — filenames derived from the attached document
  (blueprint_core.py IS required from v1.2 — §0 item 6 — but only its pure
   Cluster E scoring functions; none of its allocation machinery runs.)

**Outputs:**

- `[ExamCode]_[date]_[session]_PYQ_Final.docx` — the tagged document for portal
  upload. Every Q-stem preceded by 5 tag lines. Per-question date/session tag
  paragraphs removed (§4A). NATIVE OMML PRESERVED (v1.9) — no linearization, no
  safe-fonting, no underline recolor. The delivered file is the INTEGRITY
  artifact: byte-identical to the input except for §5 tag blocks and §4A date-tag
  removal.
- OPTIONAL `[ExamCode]_pyq_registry.json` — a LOCAL-ONLY, best-effort PYQ corpus
  progress tracker (§8). NOT a Project-Files deliverable and NOT required (v1.10):
  it is emitted only when a prior registry was attached as input, is badged
  📁 Use locally, and is never presented for upload/replace. Its absence never
  affects delivery (§12 case 11).

---

# §1 — Trigger and resolution

PYQ-4 begins on the instruction:

```text
PYQDeliver
```

Attach BOTH: the PYQ-1 output `_PYQ_Explanation.docx` AND its identity-matched sidecar
`[ExamCode]_[date]_[session]_pyq_explain_progress.json` — PYQExplain (v2.2.1) delivers both to
outputs under the SAME stem, so carry them together into this chat.
(A legacy PYQ-2 `_Complete.docx` is accepted in place of the docx.)

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
   If no matching file attached → HARD STOP: "Attach the PYQ Explanation document."

4. **exam_config.json**: load from project knowledge. Extract `exam_name`,
   `difficulty_default`, `difficulty_labels`.

5. **q_to_classification + options_by_q**: load from progress JSON (§0 priority).
   Also load, from the same JSON if present: `qtype` (§0 item 8 — Tier 2 of S2-2)
   and `q_to_difficulty` (§0 item 7, optional — Tier 1 of §2-3). Question Type
   Tier 1 (S2-2a) reads `exam_config.marking_scheme[].question_type`, already
   loaded at step 4.

5a. **blueprint_core.py**: resolve it dual-path — the framework clone
   (`/tmp/fw/blueprint_core.py`) FIRST, else the project Files
   (`/mnt/project/blueprint_core.py`) — and verify it exposes
   `structural_difficulty` (Cluster E2; v1.13 — the Tier-2 Cluster E names are
   retired and no longer required). Absent from both, or missing → HARD STOP (§0 item 6).

6. **PYQ registry check (OPTIONAL)**: load `[ExamCode]_pyq_registry.json` ONLY if
   the operator voluntarily attached one. It is NOT a Project-Files artifact, so on
   most runs there is none — that is the normal, expected state and is never a WARN
   or a nag. If a registry IS present and this paper (date + session) is already
   marked `completed` → WARN: "This paper has already been delivered. Proceed?
   (Continue to re-deliver, or stop.)" and proceed only on explicit confirmation.
   If no registry is attached, skip this check silently and continue — delivery
   never depends on it.

7. **Preflight checks**: same structural validations as MockDeliver S1-2:
   - Q-stems match q_re and count equals Q_TOTAL
   - Q-numbers are 1..Q_TOTAL continuous, no gaps
   - (v1.9: safe-fonting is retired, so no font-stack install is required for
     delivery; the delivered file keeps the input's fonts)
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
| 4 | Question Type | §2-2 three-tier resolver | Tier 1 position-based `marking_scheme[].question_type` (when >1 distinct type) → Tier 2 authoritative `qtype[q]` (PYQExplain v2.3+) → Tier 3 structural: `options_by_q` 0 → NAT; answer_cardinality 'multi' → MSQ; else → MCQ |
| 5 | Complexity | §2-3 four-tier resolver | Tier 1 q_to_difficulty → Tier 1.5 structural_difficulty → Tier 2 E-9 scoring → Tier 3 difficulty_default (D11) |

## S2-2 — Question Type resolution — era-guarded, position-first resolver (v1.12)

Question Type MUST be resolved from the exam's OFFICIAL structure, never from a
corpus statistic alone. For each question q, the first tier that yields a valid
value wins — but Tier 1 itself is now gated PAPER-WIDE by Tier 0:

```text
TIER 0 — ERA GUARD (v1.12)   classify_paper_era(...)          (blueprint_core.py)
TIER 1 — POSITION-BASED      marking_scheme[].question_type   (exam_config)
TIER 2 — AUTHORITATIVE       qtype[q]                          (sidecar, PYQExplain v2.3+)
TIER 3 — STRUCTURAL          options_by_q + answer_cardinality
```

### S2-2·T0 — Tier 0: paper era guard (v1.12 — NEW, closes an era-blind Tier-1 defect)

Before Tier 1 (S2-2a) may fire for ANY question in the paper, classify the
WHOLE PAPER once against exam_config's CURRENT pattern using the canonical
Cluster F function already shipped in `blueprint_core.py` for exactly this
concept (Framework_PYQCore EC-P9/EC-P9b; the same Pattern-Era logic that
backs Framework_MockTestAnalyse's and Framework_PYQAnalyse's corpus-era
classification). Reused via import, never reproduced (S13-1 anti-drift principle):

```python
from blueprint_core import (classify_paper_era, type_resolver_from_config,
                            exam_config_bounds)

cfg_total, min_cfg_q, max_cfg_q = exam_config_bounds(exam_config)
# raises ValueError if exam_config has no sections[] — a caller can never
# silently classify every paper against zeroes.

cfg_type_for_q = type_resolver_from_config(exam_config)
# None when exam_config carries no marking_scheme -> no type comparison is
# possible and classify_paper_era falls back to its size/range chain alone.

era = classify_paper_era(
    observed_q_numbers=range(1, Q_TOTAL + 1),
    cfg_total=cfg_total, min_cfg_q=min_cfg_q, max_cfg_q=max_cfg_q,
    observed_types=qtype_map,        # §0 item 8 — PYQExplain's authoritative map
    cfg_type_for_q=cfg_type_for_q,
)
# era is one of blueprint_core.PATTERN_ERAS:
#   'current' | 'larger' | 'smaller' | 'renumbered' | 'retyped'
```

RESOLUTION:

* **`era == 'current'`** — this paper's size AND (where observable) its
  per-position question types agree with exam_config's declared pattern.
  Tier 1 is trustworthy for this paper; proceed to S2-2a exactly as written.
* **`era != 'current'`** (`larger` / `smaller` / `renumbered` / `retyped`) —
  exam_config.marking_scheme describes a DIFFERENT pattern than this paper.
  Tier 1 is SKIPPED for EVERY question in the paper — not per-question,
  because an off-era marking_scheme cannot be trusted at any position, not
  just the ones a coincidence would flag. Resolution proceeds directly to
  Tier 2 (S2-2b) for every question. Record `era` in `qtype_tier_counts`
  provenance (S2-2e) and name it explicitly in §R1: "Tier 1 skipped — paper
  era='<era>' (exam_config's marking_scheme does not describe this paper's
  pattern)."

WHY THIS EXISTS. Tier 1 (v1.8) was introduced to fix section-determined MSQ
mis-tagging — but its literal position lookup carries an unstated assumption
that exam_config.marking_scheme describes the PAPER being delivered, not just
"the exam" in the abstract. Every exam whose pattern has changed over the
years (question count, type mix, or both) breaks that assumption for its own
older papers. Measured on IIT JAM Biotechnology 07-May-2005 (100 legacy
all-MCQ questions against the current 60-question MCQ/MSQ/NAT config): a
literal Tier 1 would have mistagged Q31-40 MSQ and Q41-60 NAT — reproducing,
via an off-era config, the exact class of portal defect Tier 1 exists to
prevent. `classify_paper_era` already existed for this precise concept
(EC-P9/EC-P9b) but PYQDeliver never called it before v1.12.

DETERMINISM: `classify_paper_era` is a pure function of (this paper's observed
Q-numbers, exam_config, PYQExplain's qtype map). Same inputs -> same era on
every run, every model instance. No model judgment participates, and no
operator confirmation is required for this class of paper again.

### S2-2a — Tier 1: position-based (v1.8 — closes the section-determined-MSQ defect; v1.12: reached only when Tier 0 returns era == 'current')

This mirrors the proven MockDeliver v1.7 precedent exactly. When
`exam_config.marking_scheme` carries MORE THAN ONE distinct `question_type`
value, Question Type is a property of the Q-NUMBER, not of the subtopic: resolve
q against `marking_scheme[].q_range` and emit that entry's `question_type`
(upper-cased MCQ/MSQ/NAT). The subtopic's `answer_cardinality` is IGNORED for
this tag.

```text
distinct = { e.question_type for e in marking_scheme }
if len(distinct) > 1:
    for e in marking_scheme:                    # first containing range wins
        lo, hi = e.q_range
        if lo <= q <= hi:  → e.question_type.upper()   (tier 1)
    # q covered by no range → fall through to Tier 2
```

When `marking_scheme` is absent, empty, or carries only ONE distinct type — every
subtopic-based exam (e.g. SSC CGL, all-MCQ) and every scoped blueprint — Tier 1
yields nothing and resolution falls through.

WHY THIS IS TIER 1. `answer_cardinality` (Tier 3) is SUBTOPIC-scoped. On exams
where MSQ is SECTION-determined — a whole section is MSQ but each of its
subtopics is predominantly single-answer across the corpus (IIT JAM, GATE, and
many others) — every subtopic's observed cardinality collapses to 'single' and
the structural rule silently mis-tags every MSQ in that section as MCQ. Measured
on IIT JAM Physics 15-Feb-2026: the structural rule returned 0 MSQ where the
exam's marking_scheme marks Q31-40 MSQ (10 questions) — a portal answer-format
and scoring error, not a cosmetic tag. `marking_scheme` is the exam's official,
section-scoped type-by-position and is the ONLY field that can express this
distinction; PYQ-4 already loads it (§0 item 2), so Tier 1 needs no new input.

### S2-2b — Tier 2: authoritative qtype (PYQExplain v2.3+)

Reached only where Tier 1 yielded nothing (single-type / subtopic-based exams).
PYQExplain (v2.3+) commits a per-question `qtype` ('mcq'/'msq'/'nat') at §5-1
and DELIVERS it in the sidecar (§S7A-4); it is the type each explanation block
was actually built as. Accept `qtype[q]` iff its value upper-cased is one of
MCQ / MSQ / NAT and emit that. Value absent/invalid for a q, or the whole map
absent (a pre-v2.3 sidecar) → fall through to Tier 3.

### S2-2c — Tier 3: structural fallback (the pre-v1.7 rule)

Reached only where Tiers 1 and 2 both yielded nothing. PYQ papers have no
`blueprint.marking_scheme`; resolve from structure:

```text
options_by_q[q] == 0                              → NAT
section_rules answer_cardinality == 'multi'        → MSQ
  (for this Q's subtopic, via q_to_classification[q].subtopic_id)
else                                              → MCQ
```

If answer_cardinality is not available for a subtopic, default 'single' (MCQ).

### S2-2d — Determinism (parity with §2-3d)

All three tiers are pure functions of (exam_config, sidecar, project files).
Tier 1 is a pure range lookup; Tier 2 a pure map lookup; Tier 3 a pure
structural computation. The SAME inputs produce the SAME Question Type on every
run and every model instance — no model judgment participates.

### S2-2e — Provenance (reported in §R1)

Track `qtype_tier_counts = {1: n1, 2: n2, 3: n3}` AND `paper_era` (v1.12, the
S2-2·T0 verdict). On a `current`-era, position-based exam (marking_scheme with
>1 distinct type) EXPECTED is Tier 1 = Q_TOTAL. Any Tier-3 questions on such an
exam mean a q fell outside every marking_scheme range — name them in §R1,
because they were resolved by the weakest instrument. On a NON-`current`-era
paper, EXPECTED is Tier 1 = 0 for the WHOLE paper (S2-2·T0 skipped it
paper-wide) and Tier 2 (or Tier 3, if qtype is also unavailable) carries every
question instead — this is normal and correct for that paper, not a defect;
§R1 must name the era so it reads as "by design" rather than "unexplained."

## S2-3 — Complexity (difficulty) — four-tier deterministic resolver (D11, v1.5)

Complexity is resolved PER QUESTION through a deterministic tier chain.
For each question q (first tier that yields a value wins):

```text
TIER 1   — q_to_difficulty[q]           (progress JSON — PYQ-1 §7A assessment)
TIER 1.5 — structural_difficulty(q)     (exam_config.marking_scheme[] structure)
TIER 2   — RETIRED (v1.13 — GAP-2026-08-27-DIFFICULTY-PROFILE): E-9 keyword scorer deleted; falls through
TIER 3   — difficulty_default            (exam_config, fallback "Medium")
```

WHY THE ORDER IS THIS AND NOT ANOTHER (v1.5 — do not reorder):
  Tier 1 is the only tier that reflects what SOLVING the question required. It is
  produced by the one step that reads and solves every question (PYQ-1), so it
  differentiates two questions that sit in the same marks band and use the same
  vocabulary. Nothing below it can do that.
  Tier 1.5 reflects the exam body's design intent for a whole Q-range. It is
  uniform within a band by construction — a floor, not an assessment.
  Tier 2 (E-9 keyword scoring) is RETIRED (v1.13): a vocabulary scorer is not an
  instrument (see item 19 below and MockTestAnalyse E-9). Nothing sits between
  the structural floor and the safety net any more.
  Tier 3 is a safety net that should never fire on a normal run.

### S2-3a — Tier 1: q_to_difficulty (upstream assessment)

If the progress JSON carries a `q_to_difficulty` map (§0 item 7):
- Accept `q_to_difficulty[q]` if and only if the value is a string AND a
  member of `difficulty_labels`. Record tier=1 for this q.
- Value absent for this q, wrong type, or not in `difficulty_labels` →
  WARN once per defect (with q number and offending value) and fall
  through to Tier 2. NEVER trust an unvalidated Tier-1 value.
- The whole map absent → silent (normal for a paper with no PYQ-1 pass);
  all questions fall through to Tier 1.5.

### S2-3a1 — Tier 1.5: structural difficulty from marking_scheme (v1.5)

Reached only when Tier 1 yielded nothing for this question.

```python
from blueprint_core import structural_difficulty   # Cluster E2 (import as in §2-3b)

value = structural_difficulty(q, marking_scheme, difficulty_labels)
```

`marking_scheme` is the §0 item 2 list, verbatim from exam_config.json.
`difficulty_labels` is the §0 item 2 value INCLUDING its ['Easy','Medium','Hard']
fallback — identical treatment to Tier 2.

`structural_difficulty` returns None — meaning FALL THROUGH TO TIER 2 — in every
one of these cases, and PYQ-4 must treat them all as ordinary, silent fall-through:
  * marking_scheme absent, empty, or not a list
  * the scheme carries no structural signal: uniform marks AND a single question
    type (a 200-question all-MCQ paper has nothing to read)
  * q falls outside every configured q_range (a legacy-pattern paper)
  * the question is an MCQ in an exam that mixes types but has uniform marks
  * `difficulty_labels` is not an exactly-3-label list
  * the matching entry's `correct_marks` is unusable — non-numeric, NaN, infinite,
    zero, or negative. Such an entry cannot occupy a position in a marks gradient,
    so its band is unknowable and Tier 1.5 declines rather than guessing one.

MALFORMED-ENTRY HANDLING (v1.5 — fixed, so two instances behave identically):
  * An entry that is not a dict is skipped.
  * `q_range` MUST be a two-element list/tuple of integers. Anything else — a
    string, a single value, three values, non-numeric members — is skipped. A
    two-CHARACTER string such as "15" also has length 2 and must NOT be accepted:
    indexing it per character yields the silently wrong range 1-5.
  * A reversed `q_range` such as [10, 1] is normalised to [1, 10] and still matches.
  * Entries with unusable `correct_marks` (as above) are excluded from the marks
    gradient entirely, so they never create a phantom tier.
  * q_ranges are scanned in the order given and the FIRST containing range wins.
    Overlapping ranges are therefore resolved by config order, deterministically.
  * None of these is a HARD STOP and none is a WARN in itself. exam_config is
    written upstream; PYQ-4's job here is to be unbreakable, not to validate it.
    A paper that then resolves degenerately is caught by the §2-3e WARN.

If `value` is not None → record tier=1.5 for this q. Else fall to Tier 2.

WHAT TIER 1.5 IS NOT — state this plainly in any report that surfaces it:
it assigns ONE label per (marks, question_type) band, so every question in a band
receives the same Complexity. It encodes the exam body's intent for that band, not
the demand of the individual question. On a paper where Tier 1.5 resolves every
question, the Complexity column carries exactly as much information as the marking
scheme already did. That is a floor worth having instead of a degenerate single
label — and it is a reason to run PYQ-1 so Tier 1 can supersede it, not a reason
to consider the paper assessed.

### S2-3b — Tier 2: RETIRED (v1.13 — GAP-2026-08-27-DIFFICULTY-PROFILE)

The E-9 keyword scorer (`blueprint_core.score_difficulty`) no longer exists in the
corpus; PYQ-4 imports only `structural_difficulty` (Cluster E2) and the Cluster F
Question-Type functions from `blueprint_core.py`. A question that Tier 1 (assessed,
PYQExplain §7A) and Tier 1.5 (structural) both leave unresolved falls DIRECTLY to
Tier 3. Difficulty on a delivered PYQ paper is therefore either MEASURED (Tier 1),
the exam body's DESIGN INTENT (Tier 1.5), or the disclosed DEFAULT (Tier 3) — never
a keyword guess presented as a label. `map_difficulty_level` / `determine_strip_mode`
stay in the engine for other consumers; PYQ-4 does not call them.

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

Track `tier_counts = {1: n1, 1.5: n15, 2: n2, 3: n3}` (v1.5 — four tiers) and the
per-label distribution of resolved values. Both are reported in §R3 and both feed
gate C10.

DEGENERATE-DISTRIBUTION WARN (v1.5 — MANDATORY, never silent). After resolution,
if EVERY question in the paper resolved to the SAME Complexity value and the paper
has more than one question, WARN:

  "All N questions resolved to Complexity '<value>'. A whole paper at one
   difficulty is almost always a resolution defect, not a property of the paper.
   Dominant tier: <tier>. If that tier is 2, the exam's stems are outside E-9's
   aptitude vocabulary and per-question difficulty was never actually measured —
   run PYQExplain (PYQ-1) so Tier 1 can supply assessed values, then re-run PYQ-4."

This is the check that would have surfaced the IIT JAM Biotechnology 60/60 "Easy"
delivery at the moment it was produced instead of after publication. It is a WARN,
not a HALT: a genuinely uniform paper is possible, and the operator decides.

MIXED-PROVENANCE WARN (v1.5 — MANDATORY, never silent). The degenerate check above
only fires when the WHOLE paper lands on one label, and that misses a real case.
An exam that mixes question types but has UNIFORM marks — MCQ and NAT both at the
same marks, the shape used by several major entrance exams — resolves its NAT/MSQ
questions at Tier 1.5 and drops every MCQ to Tier 3 (v1.13). The resulting distribution is
NOT uniform, so the degenerate WARN stays quiet, and the paper ships with a
Complexity column whose values came from two different instruments: one reading
the marking structure, the other a paper-wide default. Those are not the same
scale and must not be compared as though they were.

Therefore: if Tier 3 resolved at least one question AND Tiers 1/1.5 together
resolved at least one other, WARN:

  "Complexity on this paper has MIXED PROVENANCE: N question(s) were resolved by
   tier(s) <list> and M question(s) fell to Tier 3 (difficulty_default). These
   are different instruments — a 'Medium' from the marking structure and the
   paper-wide default are not comparable, and the Tier-3 questions were not
   measured at all. Run PYQExplain (PYQ-1) so Tier 1 resolves the whole paper on one
   instrument, then re-run PYQ-4."

Both WARNs can fire together, and both are reported in §R3.

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
                  build the DELIVERED artifact (native OMML, tag blocks, NO
                  render transforms) → validate all gates)
3. bash_tool    → final gate checks + OPTIONAL PYQ registry update (only if a
                  prior registry was attached; otherwise skipped silently — §8)
4. present_files → deliver [ExamCode]_[date]_[session]_PYQ_Final.docx
                  (the integrity artifact — native OMML preserved)
```

Uses the same `unzip → XML edit → zip` approach as MockDeliver — raw document.xml
editing that NEVER round-trips through python-docx, so OMML survives byte-perfect.
v1.9: a single delivered artifact (the integrity artifact). The former
render-source (OMML linearized) is RETIRED — not built, not delivered.

---

# §4 — Two-artifact model

Same architecture as MockDeliver, adapted for PYQ:

## S4-1 — Single delivered artifact (v1.9)

Earlier versions built TWO artifacts and delivered the linearized one. That was
the defect: it destroyed native math in the portal file. The reasoning behind it
does not survive scrutiny for PYQ-4:

1. The historical justification was that a naive python-docx ROUND-TRIP on a docx
   containing `<m:oMath>` can silently corrupt every math element. But PYQ-4 does
   NOT round-trip through python-docx — it edits raw `word/document.xml` and
   re-zips (§3). OMML therefore survives the pipeline byte-perfect, PROVEN by the
   integrity artifact every prior version already built and gated (C5: integrity
   OMML count == source). There is no corruption to defend against, so there is
   nothing to linearize.
2. Native OMML is standard Word math and renders in Word and any Word-based
   portal. The student-facing PYQ-3 (PYQFormat) already delivers native OMML to
   end users (its OMML-count-equality gate), so native math is a proven
   downstream contract, not a risk.

Therefore v1.9 delivers ONE artifact — the integrity artifact — and retires the
render-source and its transforms entirely.

## S4-2 — Artifact definition (v1.9)

- **Delivered artifact (the integrity artifact)**: byte-perfect content docx with
  NATIVE OMML untouched, tag blocks inserted, date/session tags removed, and NO
  render transforms. Validated by C1-C10, C16, C17, C18. THIS is the delivered
  file (`_PYQ_Final.docx`).
- **Render-source artifact**: RETIRED (v1.9). No OMML linearization, no
  safe-font, no underline recolor is performed, and no second artifact is built.

Date/session tag removal (§4A) runs on the working body BEFORE the delivered
artifact is assembled — so the delivered file contains no date/session tags.

---

# §4A — Date/Session tag removal (v1.1)

The input document carries a per-question date/session tag paragraph — the
PYQSort `date_label` line that sits immediately above each Q-stem and rides
through PYQExplain unchanged:

```text
[12-Sep-2025 Shift 1]     (multi-session exam, keyword from exam_config)
[02-Feb-2025 Session 2]   (GATE-style keyword)
[15-Jun-2025]             (single-session exam — no keyword/number)
```

These tags are internal pipeline metadata, not portal content (D10). The
paper's identity is already carried by the output filename and the PYQ
registry entry. PYQ-4 removes every tag paragraph from the document body.

This section MIRRORS Framework_PYQFormat.md §4 (v1.1) — PYQ-3 and PYQ-4 are
independent forks of the PYQ-1 output, so each performs its own removal.
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
then, so on a clean PYQ-1 output this finds ZERO (the tag-free document is
questions + explanations only). Any hits are stripped and a REGRESSION ALARM
is raised in the report. (v1.0 bug, fixed in v1.1: without §4A running first,
this step mis-fired on Q.1's date label — a legitimate pipeline artifact, not
a regression — while Q.2..Qn labels were left in the delivered document.)

---

# §6 — Render transforms — RETIRED (v1.9)

The entire §6 render-transform stage is RETIRED. None of these transforms is
applied to the delivered file. The delivered file is the integrity artifact,
carrying native OMML and the input's original fonts/colours (see §4). The
subsections are retained only so historical §6/S6-N and Rule 19/21/22 references
elsewhere in the corpus continue to resolve.

## S6-1 — Rule 19: OMML → Unicode text — RETIRED

NOT PERFORMED (v1.9). Every `<m:oMath>` is preserved byte-for-byte. This is the
single change that fixes the math-destruction defect: math is never linearized.

## S6-2 — Rule 22: Underlined stem recolor — RETIRED

NOT PERFORMED (v1.9). Underlined stem runs keep their input colour. (A portal
that wants red-underline emphasis can request the optional Option-B variant,
which reintroduces this transform while still preserving native OMML.)

## S6-3 — Rule 21: Non-ASCII safe-font — RETIRED

NOT PERFORMED (v1.9). Runs keep the input's original fonts. The input is an
already-valid, Word-openable PYQ-1 artifact whose glyphs render as-is; C18
re-proves package validity of the delivered file against the source.

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

**Delivered-file math/text gates (v1.9 — the delivered file is the integrity artifact):**

**C11** Math PRESERVATION (INVERTED, v1.9): the delivered file's `<m:oMath>`
count == source count (== C5). ZERO linearization; NO `<m:oMath>` was replaced
by text. This gate now guarantees native math is intact rather than eliminated.
A shortfall is a HARD STOP — it means math was lost.

**C12** Delivered docx valid ZIP; document.xml parses. (Covered for the delivered
integrity artifact; formerly the render-source check.)

**C13** Text conservation: Q.1..Q.{Q_TOTAL} present; tag label counts match;
`Correct Answer:` count matches source.

**C14** Symbol + math round-trip (v1.9): every non-ASCII codepoint present in the
source is present in the delivered file with the exact codepoint, AND native math
subtrees are byte-identical to the source (no `<m:t>` text altered). No Unicode
linearization is expected or permitted.

**C15** No stray recolor (v1.9, repurposed): the delivered file introduces NO
colour change vs source — no FF0000 recolor is applied; NAVY (003366) count
unchanged. (Rule 22 is retired; this gate now asserts colours were left alone.)

**Namespace/reference/order integrity:**

**C16** (a) mc:Ignorable coverage — every prefix declared. (b) Namespace superset
— no xmlns dropped vs source. (c) No dangling relationships. (d) Tag-block
pPr order: spacing before jc.

**Portal charset:**

**C17** NAT Correct-Answer portal charset: every NAT question's rendered value
matches `0123456789.-` exactly. Scoped by question_type (not pattern-matched).
Any violation → HARD STOP (last CONTENT gate in the pipeline; C18 follows as
the package gate).

**Package validity:**

**C18** OOXML package validity on the delivered artifact — HARD STOP.
(v1.9 retired the render-source; C18 validates the ONE delivered file. v1.11:
wording corrected from the stale "BOTH artifacts".)

⚠️ **C1–C17 verify CONTENT FIDELITY. None of them verifies PACKAGE VALIDITY.**
These are independent properties. C1 and C12 check that `document.xml` *parses*
— which a corrupt file does: undeclared `mc:Ignorable` prefixes and misordered
`pPr`/`tcPr` children leave the XML well-formed, so lxml and stdlib
ElementTree both read it happily. This is precisely what let PYQ-3 pass every
gate it had and deliver a file Word would not open, with its text stream,
drawings and paragraph counts all perfectly intact.

C18 runs last, after C17, on the artifacts as they will be delivered:

```python
import os
import subprocess

VALIDATOR = '/mnt/skills/public/docx/scripts/office/validate.py'


def gate_c18(source_docx, integrity_docx, render_source_docx=None):
    """C18 — OOXML package validity on the delivered artifact (v1.9).

    Returns 'validated' or 'degraded'; raises SystemExit on failure.

    v1.9: the render-source is retired, so the delivered file IS the integrity
    artifact and C18 validates that one file. render_source_docx is accepted but
    ignored when None (back-compat with pre-v1.9 callers). If a caller still
    passes a render-source path it is validated too, harmlessly.

    --original is REQUIRED: it reports only errors NEW relative to the source,
    so pre-existing quirks in a given exam's PYQ-1 output (frequent across ~200
    exams with heterogeneous provenance) do not block delivery, while anything
    PYQ-4 introduced does.
    """
    if not os.path.exists(VALIDATOR):
        # Validator absent. C16(a)/(b) remain in force as the namespace check,
        # but schema ordering is UNVERIFIED — report package validity as
        # UNVERIFIED in §R5, never as PASS.
        print('C18 DEGRADED — validator unavailable. Namespace integrity still '
              'covered by C16(a)/(b); schema ordering is UNVERIFIED. '
              'Report as UNVERIFIED in §R5.')
        return 'degraded'

    artifacts = [('delivered', integrity_docx)]
    if render_source_docx is not None:
        artifacts.append(('render-source', render_source_docx))
    failures = []
    for label, path in artifacts:
        result = subprocess.run(
            ['python3', VALIDATOR, path, '--original', source_docx],
            capture_output=True, text=True)
        if result.returncode != 0:
            failures.append('C18 FAIL [%s artifact] %s\n%s'
                            % (label, path, result.stdout + result.stderr))
    if failures:
        for f in failures:
            print(f)
        raise SystemExit('C18 HARD STOP — package is not valid OOXML. '
                         'Do not deliver.')
    return 'validated'
```

**The single delivered artifact (v1.9).** The integrity artifact IS the shipped
file (`_PYQ_Final.docx`), so its validity is non-negotiable — and it is also what
C1–C10 are evaluated against. A structural fault means those gates ran on a
damaged document and their PASS means less than it appears; a fault indicates the
pipeline is wrong. (Prior versions validated a second render-source artifact;
that artifact is retired, so C18 now validates the one delivered file against the
source.)

**Zero, not "fewer".** When a validator rejects an element at its own position
it does not descend into it, so that element's children's violations stay
hidden until the outer one is fixed. Measured on the PYQ-3 artefact: **812
errors reported, 991 elements actually requiring reorder.** An error count is a
LOWER BOUND until it reaches zero. If a fix lowers the count, re-run — newly
surfaced errors are expected behaviour, not a regression.

**Relationship to C16.** C16 is not superseded and must stay: it runs earlier,
is self-contained, and states the namespace invariant in PYQ-4's own terms.
But its coverage is narrower than it looks — C16(d) checks `pPr` order only for
the tag blocks this spec builds, and only that `spacing` precedes `jc`. Any
other misordering, in any other element, in any part, passes C16 untouched.
C18 is the general case.

**Fallback.** If the validator is unavailable in the runtime, C16(a)/(b) remain
in force as the namespace check and C18 degrades to that — report the
degradation explicitly in §R5. The fallback does NOT cover schema ordering;
treat a C18-degraded run as unverified for package validity rather than as a
pass.

**LibreOffice is not a substitute.** A successful `soffice` conversion is
necessary but not sufficient — it opens files Word rejects, confirmed on the
PYQ-3 artefact, which rendered acceptably while Word refused it. PYQ-4 performs
no `soffice` conversion in any case (§11 hard invariant); this is noted so the
absence of a rendering step is not mistaken for a missing validity check.

---

# §8 — PYQ registry

PYQ-4 can maintain `[ExamCode]_pyq_registry.json` — a corpus-level progress tracker
for PYQ paper delivery. It is OPTIONAL and LOCAL-ONLY (v1.10): it is NOT a
Project-Files deliverable, it is never required, and its absence is the normal state
on any run where the operator did not attach a prior copy. It exists purely as an
opt-in continuity aid for operators who want a running cross-paper tally; the portal
deliverable (`_PYQ_Final.docx`) never depends on it.

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

## S8-2 — Registry operations (all conditional on an attached registry, v1.10)

- **Before delivery**: ONLY when a prior registry was attached — check if this
  date_session is already in `papers_completed`. If yes → WARN and require explicit
  confirmation to re-deliver. With no registry attached this check is skipped
  silently.
- **After delivery**: ONLY when a prior registry was attached — add/update the entry
  in `papers_completed` with the current timestamp and increment
  `total_papers_delivered` / `total_questions_delivered`, then emit the updated file
  LOCAL-ONLY (📁 Use locally). With no registry attached, nothing is written and the
  §R6 report states current-paper-only totals.
- **No registry attached (the normal case)**: PYQ-4 does NOT create, deliver, badge,
  or present a registry, and does NOT treat its absence as a defect. This is the
  expected state and never blocks, warns, or renders amber.

## S8-3 — Registry storage (v1.10 — no Project-Files handoff)

The registry is NEVER uploaded to or replaced in the exam project's Files section,
and PYQ-4 never asks the operator to manage it there. This RETIRES the pre-v1.10
manual handoff, whose routinely-skipped upload was the root cause of the silent
cross-session reset across the ~200-exam corpus (see header v1.10). When PYQ-4 does
update a registry — which happens ONLY because one was attached — the updated copy
is written chat-scoped and badged 📁 Use locally: a convenience for an operator who
chooses to carry it into the next paper's chat by RE-ATTACHING it, NOT an
instruction and NOT a Project-Files deliverable. Cross-chat corpus tracking is
therefore OPT-IN by attachment; skipping it costs only the running tally and the
duplicate guard, never the portal file. Framework_DeliveryFooter v1.16 additionally
lists `*_pyq_registry.json` in the §2 LOCAL_ONLY set, so the badge engine cannot
route it to Project Files on any step or exam even if some future caller presents it.

---

# §9 — Delivery

PYQ-4 delivers in a single response:

1. All gates (§7 C1-C18) pass, C18 (package validity) included.
2. OPTIONAL PYQ registry update (§8) — performed ONLY when a prior registry was
   attached; skipped silently otherwise. Never gates delivery.
3. Present `[ExamCode]_[date]_[session]_PYQ_Final.docx` via present_files.
4. Upload to Google Drive (if Drive access is available; otherwise instruct the
   user to upload manually).
5. Print the delivery report (§10).
6. Render the post-delivery footer per Framework_DeliveryFooter.md:
   - F2 (step-complete, GREEN).
   - File badges: `📁 Use locally` for PYQ_Final.docx. The registry is NEVER badged
     for upload/replace and is NOT listed as a Project-Files deliverable (v1.10);
     if a LOCAL-ONLY updated registry was emitted (only when one was attached) it
     too carries `📁 Use locally`. On the normal run no registry line appears in the
     footer at all.
   - Next-step reference: "PYQ pipeline complete for [ExamCode] [date] [session].
     Next paper: run PYQ-1 (PYQExplain) for the next PYQ paper in a new chat."

---

# §10 — Delivery report

Printed in chat after present_files:

- **§R1 — Scope.** Exam, paper (date, session), Q_TOTAL, question types (MCQ/MSQ/NAT
  split), and Question Type provenance: `paper_era` (S2-2·T0, v1.12) plus Tier 1
  position-based / Tier 2 qtype / Tier 3 structural counts (S2-2e). EXPECTED on a
  `current`-era, position-based exam: Tier 1 = Q_TOTAL; any lower-tier questions are
  named. EXPECTED on a NON-`current`-era paper (`larger` / `smaller` / `renumbered` /
  `retyped`): Tier 1 = 0 for the whole paper by design (Tier 0 skipped it) — state the
  era explicitly so this reads as intentional, not a gap.
- **§R2 — Tag summary.** Total tag blocks inserted. Subject/Topic/Subtopic distribution.
  Date/session tag paragraphs removed (`tags_removed`, §4A); any safety-gate
  skips (`tags_skipped`) listed with position and reason.
- **§R3 — Complexity.** Tier provenance counts (Tier 1 / Tier 1.5 / Tier 2 /
  Tier 3, §2-3e) and the per-label distribution of resolved Complexity values.
  Any Tier-1 validation WARNs and any Tier-3 fallbacks listed with q number and
  reason. Both §2-3e WARNs — degenerate-distribution and mixed-provenance — are
  reported here when they fire, with the Q-numbers that fell to Tier 3.
  When Tier 1.5 resolved any question, state plainly that those values are the
  exam body's per-band design intent and are uniform within a band (§2-3a1).
  EXPECTED on a paper WITH a PYQ-1 pass: Tier 1 = Q_TOTAL, all others 0.
  EXPECTED on a paper WITHOUT one: Tier 1.5 and/or Tier 3 carry the paper, and
  the report should say so rather than presenting the column as assessed.
- **§R4 — Content fidelity (v1.9).** State the delivered `<m:oMath>` count and
  confirm it equals the source count (C5/C11) — i.e. native math preserved, zero
  linearization. Confirm no safe-font and no underline-recolor were applied
  (Rule 21/22 retired). Report the two — and only two — permitted edits:
  `tags_removed` (§4A) and tag blocks inserted (§5).
- **§R5 — Gate results.** C1-C18 all PASS (or list failures). Report C18
  explicitly for the delivered artifact — state the validator verdict, not merely
  "passed". If the validator was unavailable and C18 degraded to the C16(a)/(b)
  namespace fallback, say so here and mark package validity UNVERIFIED rather than
  PASS.
- **§R6 — PYQ registry (OPTIONAL).** Reported ONLY when a prior registry was
  attached: papers delivered to date, total questions, corpus progress. On the
  normal run (no registry attached) state plainly: "corpus tracking not active for
  this run (no registry attached); this paper delivered N questions." This is
  expected, not a defect, and never renders amber.
- **§R7 — Note.** "This is the portal-ready document with native math preserved.
  Open in Microsoft Word to verify equations render as native OMML. For student
  download, run PYQ-3 (PYQFormat) separately in a new chat — it takes PYQ-1 output
  directly."
- **§R8 — Regression alarms.** Any header paragraphs detected and stripped (should
  be zero on a clean PYQ-1 output).

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
6. The delivered (integrity) artifact passes C1-C10.
7. The delivered artifact passes C11-C17 (v1.9: C11 asserts OMML PRESERVED, not
   eliminated; C14 asserts native math byte-identical; C15 asserts no stray
   recolor).
7a. The delivered artifact passes C18 (package validity) against the source.
8. NATIVE OMML PRESERVED — delivered `<m:oMath>` count == source (C5/C11). No
   linearization, no safe-fonting, no recolor performed.
9. OPTIONAL: if (and only if) a prior registry was attached, it was updated with
   this paper and emitted LOCAL-ONLY. Absence of a registry is NOT a failure of this
   item — the item is vacuously satisfied when no registry was attached.
10. Delivered via present_files with the delivery report and footer.
11. Opens clean in Microsoft Word with no "unreadable content" prompt —
    machine-verified by C18 on the delivered artifact, not assumed. Items 1-10
    establish that the CONTENT is correct; only C18 establishes that the
    PACKAGE is valid. A file can satisfy every other item on this list and
    still fail to open.

**Hard invariants (never violated):**

- No text content is modified in the delivered artifact.
- The date/session tag paragraphs (§4A) are the ONLY elements ever removed —
  matched by anchored full-paragraph DATE_TAG_RE, protected by the media
  safety gate. Nothing else is ever deleted from the delivered file.
- OMML is NEVER linearized (v1.9). Native `<m:oMath>` is preserved byte-for-byte
  in the delivered file; delivered OMML count == source (C5/C11).
- The delivered file is the INTEGRITY artifact (native OMML); the render-source
  is retired and never built. No `soffice` conversion.
- No `cleanup_namespaces()` — ever (MockDeliver v1.3 lesson).
- `word/webSettings.xml` is never stripped (MockDeliver v1.3 lesson).
- Tag pPr: `<w:spacing>` before `<w:jc>` (OOXML schema order).
- The delivered artifact is a schema-valid OOXML package, proven by C18 against the
  source with `--original`. Parsing without error is NOT validity.
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

4. **Paper already delivered (registry attached)** → only reachable when a prior
   registry was attached and lists this paper: WARN + require confirmation. If
   confirmed, re-deliver and update the (local-only) registry entry. Unreachable on
   the normal run, where no registry is attached.

5. **Input is PYQ-1 output** → the NORMAL input (v1.6: PYQ-2 retired). Accepted
   with no WARN. A legacy `_PYQ_Explanation_Complete.docx` is equally accepted.

6. **NAT question with bad grading value** → C17 catches it as HARD STOP.

7. **Document with no OMML** → Fine. Preserved OMML count = 0 == source. C5/C11
   pass trivially (nothing to preserve, nothing linearized).

8. **Document with no images** → Fine. Drawing count = 0. Gates still pass.

9. **Non-ASCII codepoints not in safe font stack** → Kept in original font,
   logged in report. Not a HARD STOP (Word can substitute).

10. **Google Drive unavailable** → Deliver locally via present_files. Instruct
    user to upload manually. Not a HARD STOP.

11. **No registry attached (the normal case)** → PYQ-4 does not create, deliver,
    badge, or present one, and never treats the absence as an issue. Corpus tracking
    is simply inactive for the run. This is the expected state on the ~200-exam
    corpus (v1.10), not a first-paper special case, and never causes a WARN, a HALT,
    or an amber footer.

12. **Re-run on same paper** → if a prior registry was attached, it detects the
    duplicate, WARNs, and re-delivers on confirmation; with no registry attached
    there is no duplicate check and the re-run proceeds normally. Either way the
    output overwrites the previous _PYQ_Final.docx.

13. **Already-formatted doc attached by mistake (_PYQ_Formatted.docx)** → Detect
    from filename and HARD STOP: "This is the PYQ-3 formatted document. PYQ-4
    takes the PYQ-1 output (_PYQ_Explanation.docx) directly."

14. **No date/session tag paragraphs in the document** → WARN (not HALT,
    S4A-3): document may predate tagging or tags were already removed.
    Delivery proceeds; `tags_removed = 0` reported in §R2.

15. **Date-tag-shaped paragraph containing `<m:oMath>` or `<w:drawing>`** →
    S4A-2 safety gate SKIPs it, WARNs with position, counts it in
    `tags_skipped`. Gate C4 tolerates exactly `tags_skipped` residuals.
    An inline date label inside a stem/explanation is NEVER at risk — the
    anchored regex only matches full paragraphs.

16. **blueprint_core.py missing or lacking Cluster E / E2 functions** → HARD STOP
    (§0 item 6 / §1 step 5a). Absent from BOTH the framework clone (/tmp/fw)
    and the project Files (/mnt/project): the operator reloads the framework
    (Step 0) or uploads the current blueprint_core.py, then re-runs.

17. **q_to_difficulty present but defective** (value missing for some q,
    wrong type, or not in difficulty_labels) → per-q WARN + fallthrough to
    Tier 1.5 / Tier 3 (S2-3a; Tier 2 retired v1.13). A defective Tier-1 map can never block delivery
    and can never inject an out-of-vocabulary tag.

18. **Non-3-label difficulty_labels** (2-band or 5-band custom set) →
    `map_difficulty_level` returns None → Tier 3 for every question, each
    WARNed, difficulty_default used (must itself be in the label set or
    C10 HARD STOPs). Deterministic; never guesses an ordinal mapping.

19. **Exam whose stems are outside E-9's aptitude vocabulary** — RESOLVED by
    retirement (v1.13, GAP-2026-08-27-DIFFICULTY-PROFILE). The E-9 keyword scorer
    was measured on IIT JAM Biotechnology 15-Feb-2026 scoring C=1 for 60/60 and
    I=1 for 59/60, and on SSC CGL Tier-1 09-Sep-2024 disagreeing with the
    derivation rubric by 40 points. It is deleted. Correct handling is now, in
    order: (a) run PYQExplain (PYQ-1) so Tier 1 supplies assessed values — the
    resolution; (b) failing that, Tier 1.5 resolves any exam whose marking_scheme
    has a marks gradient or a type mix; (c) otherwise Tier 3 carries the paper,
    the §2-3e mixed-provenance / degenerate WARNs fire and R3 states plainly that
    the column is a default, not an assessment.

20. **exam_config.marking_scheme absent or uniform** (legacy project, or an
    exam like a 200-question all-MCQ paper at one mark) → structural_difficulty
    returns None for every question, Tier 1.5 contributes nothing, and
    resolution proceeds to Tier 2 exactly as in v1.4. Silent and expected —
    NOT a WARN in itself. If the paper then resolves degenerately, the §2-3e
    WARN is what fires, naming Tier 2 as the dominant tier.

21. **marking_scheme q_ranges do not cover every question** (legacy-pattern
    paper) → uncovered questions get Tier 1.5 = None and marks fall back per
    the §0 item 2 order; the existing v1.3 OUT-OF-PATTERN MARKS WARNING already
    reports them by Q-range and must still fire.

22. **Paper era != 'current' (v1.12 — S2-2·T0)** — the paper's size and/or
    per-position types disagree with exam_config's declared pattern (a
    shrunk/grown/renumbered/retyped exam, e.g. a legacy 100-Q all-MCQ paper
    against a current 60-Q MCQ/MSQ/NAT config). Tier 1 (S2-2a) is skipped for
    the WHOLE paper; every question resolves via Tier 2 (qtype) or Tier 3
    (structural). NOT a HARD STOP and NOT an operator prompt — deterministic,
    reported in §R1 by name (`paper_era`). If `qtype` (Tier 2) is ALSO
    unavailable for such a paper (pre-v2.3 sidecar), Tier 3 structural
    resolution carries it; report that combination plainly, since two
    weaker-than-Tier-1 instruments are then both in play.

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
- `gate_c16(src, out, labels)` — namespace/reference/order gate
- `gate_c17_natcharset(out, tag_lookup)` — NAT portal charset gate
- Single-artifact assembly (the integrity artifact ZIP construction, native OMML)
- All namespace preservation rules (no cleanup_namespaces, keep webSettings.xml)

RETIRED in v1.9 (no longer invoked — the delivered file carries native OMML and
the input's original fonts/colours):
- `replace_omath_with_text(root, font)` — Rule 19 OMML linearization (RETIRED)
- `recolor_underlined_stems(root, color)` — Rule 22 stem recolor (RETIRED)
- `apply_symbol_safe_font(root, default_font)` — Rule 21 safe-font (RETIRED)
- Second (render-source) artifact assembly (RETIRED)

These are NOT engine functions — they are standalone document-transform utilities
from MockDeliver, reproduced in PYQ-4's pipeline script.

EXCEPTION (v1.2; v1.13 — now `structural_difficulty` only, the Tier-2 functions
are retired): the engine function is NOT reproduced in the
pipeline script — it is IMPORTED from `blueprint_core.py`, resolved
dual-path (`/tmp/fw` first, else `/mnt/project` — §2-3b) (Cluster E, the
canonical shared copy). Reproducing them inline would create a fourth copy
of E-9 and is FORBIDDEN (anti-drift principle).

## S13-2 — PYQ-specific differences from MockDeliver

| Aspect | MockDeliver (Step 11) | PYQDeliver (PYQ-4) |
|---|---|---|
| Tag data source | registry.json + blueprint.json JOIN | q_to_classification direct lookup |
| Question Type | marking_scheme (position-based) or subtopic (subtopic-based) | marking_scheme position-based (Tier 1) → qtype (Tier 2) → structural (Tier 3) |
| Complexity | Per-Q from registry.difficulty | Per-Q four-tier resolver: q_to_difficulty (PYQ-1 §7A) → structural_difficulty (Cluster E2) → E-9 scoring (Cluster E) → difficulty_default (§2-3, D11) |
| Paper identity | pp.paper\_slug() via paper\_pipeline.py | Parsed from attached filename |
| Blueprint | Required | Not required (does not exist for PYQ) |
| Registry | Required | Not required (does not exist for PYQ) |
| PYQ registry | N/A | OPTIONAL, local-only, best-effort (§8) — never a Project-Files deliverable (v1.10) |
| Trigger | TestDeliver P[N] / MockDeliver M[N] | PYQDeliver (no arguments needed) |
| Package validity | C16(a)–(d) only | C16 **plus** C18 `gate_c18()` — full OOXML schema validation of the delivered artifact against the source (§7; v1.9: one delivered artifact, native OMML) |

`gate_c18()` is PYQ-4-specific and is NOT among the MockDeliver patterns reused
in S13-1 — MockDeliver has no equivalent. It is defined in full in §7 (C18).

## S13-3 — Namespace preservation (MockDeliver v1.3 lessons)

When assembling the delivered (integrity) docx:
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

RENDER-SAFE FONT STACK (RETIRED v1.9 — safe-fonting no longer applied; the
delivered file keeps the input's original fonts):
  Primary : DejaVu Sans (covers most Unicode, math symbols)
  Fallback: FreeSans (covers section markers ❌ ⬛ ✅ ⚡)
```

---

**End of Framework_PYQDeliver.md (v1.13)**
