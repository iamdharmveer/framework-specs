# Framework_MockDeliver v1.4 — Universal Mock Test Tagger & Delivery Engine
# [ExamCode] project | Step 11 (MockDeliver) | Exam-agnostic
#
# PURPOSE:
#   Take the audited Solutions document from Step 10 (MockExplainAudit),
#   JOIN per-question metadata from registry.json + blueprint.json,
#   INSERT a 5-line tag block (Subject / Topic / Subtopic / Question Type /
#   Complexity) before every Q-stem, apply render-safe transforms (OMML
#   linearization, non-ASCII safe-font, underlined-stem recolor), and
#   deliver a tagged, upload-ready Word document (.docx).
#
#   This is the LAST step in the mock test pipeline. Its output is the
#   final learner-facing artifact uploaded to the distribution platform.
#
# PIPELINE POSITION:
#   Step 5  PYQExtract       → section_rules.md, subtopic_manifest.json
#   Step 6  MockBlueprint    → blueprint.json, registry.json (template)
#   Step 7  MockCreate       → [ExamCode]_Mock[N]_Complete.docx, registry.json
#   Step 8  MockCreateAudit  → rectified paper, re-synced registry
#   Step 9  MockExplain      → [ExamCode]_Mock[N]_Solutions.docx
#   Step 10 MockExplainAudit → [ExamCode]_Mock[N]_Solutions_Audited.docx
#   Step 11 MockDeliver      → [ExamCode]_Mock[N]_Tagged.docx   ← THIS STEP
#
#   Step 11 runs in the [ExamCode] project (exam-specific).
#   Step 11 runs AFTER Step 10 has completed and the audited Solutions docx is available.
#
# INPUTS:
#   1. Solutions docx — attached by user (output of Step 10 or Step 9)
#      Accepted filenames: [ExamCode]_Mock[N]_Solutions_Audited.docx
#                          [ExamCode]_Mock[N]_Solutions.docx
#   2. [ExamCode]_blueprint.json   — in project knowledge (loaded automatically)
#   3. [ExamCode]_registry.json    — in project knowledge (loaded automatically)
#
# OUTPUT:
#   One tagged Word document (.docx) — delivered via present_files.
#   Filename: [ExamCode]_Mock[N]_Tagged.docx
#
# TRIGGER FORMAT:
#   Step 11: MockDeliver M[N]
#   Trigger matching is case-insensitive.
#   [N] = mock number (positive integer).
#   ExamCode read from blueprint.json in project knowledge.
#   The Solutions docx must be attached to the trigger message.
#
# RUNS IN: [ExamCode] project (exam-specific, where blueprint.json and
#          registry.json are in project knowledge)
#
# EXECUTION MODEL: Single script, 4 tool calls maximum. No "Continue" needed.
#   1. create_file  → write complete deliver_pipeline.py
#   2. bash_tool    → run it (parse + join + tag + integrity + render-source + validate)
#   3. bash_tool    → verify Q-count, tag counts, render-source checks
#   4. present_files → deliver
#
# EXAM-AGNOSTIC GUARANTEE:
#   This spec contains ZERO hardcoded exam values. No section name, no topic name,
#   no subtopic name, no question count, no Q-number range, no option label, no
#   difficulty label, no question type string is hardcoded.
#   All tag values are JOIN-derived from blueprint.json and registry.json at runtime.
#   Same spec runs for SSC CGL (4 sections, 100Q), GATE (1 section, 65Q),
#   UPSC (variable), or any MCQ/MSQ/NAT exam.
#
# VERSION HISTORY:
#   v1.4 — 2026-07-11 — FIGURE SECTION REMOVED FROM SOLUTIONS LAYOUT LEGEND
#          (parallel to Step 9 v1.13 / Step 10 v1.8). Step 9 no longer renders the
#          ⬛ FIGURE / figure-description block, so the §S2-2 per-question interleaved-
#          Solutions layout legend drops those two lines. The per-question block is now
#          Correct Answer → ⬛ AXIOM → ⬛ DEDUCTION → (⚡ SPEED HACK) → ❌ WHY WRONG? /
#          ❌ COMMON PITFALLS for every question type. Documentation-only; MockDeliver
#          reads and delivers the finished docx and never rendered or checked the FIGURE
#          header, so there is zero logic change.
#   v1.3 — 2026-07-09 — DOCX VALIDITY HARDENING (fixes Word "unreadable content —
#          recover?" on the delivered Tagged.docx). Roots out an OOXML-corruption class
#          that python-docx and LibreOffice opened SILENTLY while Microsoft Word — the
#          only strict consumer — rejected. SIX exam-agnostic fixes:
#          (1) ROOT CAUSE — removed etree.cleanup_namespaces() from BOTH the integrity
#              assembly (§5 Phase 3) AND the render-source assembly (§5 Phase 5). It
#              stripped root xmlns declarations (w14/wp14/o/v/w10 + drawing namespaces)
#              that mc:Ignorable and drawing/VML content still reference, which Word
#              treats as corrupt. NOTE: Phase 3 mutated the SHARED tree in place and
#              Phase 4 deepcopied it, so removing only one call site was insufficient —
#              BOTH had to go.
#          (2) §4-3 make_tag_para now emits <w:spacing> BEFORE <w:jc> (OOXML CT_PPr
#              child-order; jc-first was schema-invalid).
#          (3) §5 Phase 3/5 — stopped stripping word/webSettings.xml (retired Rule 14).
#              The part is benign; keeping it removes the dangling relationship (in
#              document.xml.rels) and dangling Override (in [Content_Types].xml) that a
#              strip-without-cleanup leaves behind — a second corruption trigger. Gate
#              C9 repurposed from "webSettings absent" to a dangling-reference check.
#          (4) §1 S1-3 build_tag_lookup — JOIN now accepts subtopic_id when present and
#              falls back to (section, subtopic) with a duplicate-key guard; tolerant of
#              both registry schemas so a clean run never hard-stops on the key name.
#          (5) §6 + §10 — NEW gate C16 (namespace + reference + tag-order integrity),
#              optional OOXML-XSD validation, a 4th hard invariant, and a MANDATORY
#              single Microsoft Word open as the final human acceptance check.
#          (6) §7 Rule 21 — multi-font fallback: _SAFE_STACK extended with FreeSans;
#              font is chosen PER non-ASCII codepoint (first stacked font that covers
#              it) so section markers ❌ ⬛ ✅ ⚡ no longer render as tofu; codepoints no
#              stacked font covers KEEP their original font (so Word can substitute) and
#              are logged in the delivery report. Preflight (§1 S1-2) now verifies the
#              fallback font is installed.
#          PROPAGATION: this is the exam-agnostic MASTER. Every exam project MUST re-sync
#          its Step-11 spec from this file — a per-project copy left at v1.1/v1.2 will
#          reproduce the corruption. This v1.3 supersedes BOTH earlier "v1.2" documents
#          (the header-strip demotion below AND the standalone docx-validity amendment).
#   v1.2 — 2026-07-09 — HEADER-STRIP DEMOTED TO SAFETY-NET (pairs with Step 7 v5.18 /
#          Step 8 v2.7). The input Solutions docx is now questions-only BY CONSTRUCTION:
#          Step 7 R8b / G-PREQ1 never emits a pre-Q.1 title/info/scoring/cover block, and
#          Step 8 A-HEADER strips any residual. So detect_header_paras() should ALWAYS find
#          zero. It is retained UNCHANGED as a defensive safety-net; if it ever strips a
#          paragraph, that is an UPSTREAM REGRESSION (Step 7/8) and is now flagged as a
#          REGRESSION ALARM in the delivery report. DoD #1, §2 S2-1, EC-1, EC-2, the
#          ZERO-MUTATION note, the §8 delivery report, and the §10 checklist reworded
#          accordingly. Zero logic change to the strip / tag / render code.
#   v1.1 — 2026-07-07 — DELIVERY FOOTER CROSS-REFERENCE.
#          Added post-delivery footer rendering reference to Framework_DeliveryFooter.md
#          v1.3 in §8 (File Naming & Delivery). F2 (step-complete) footer rendered after
#          present_files and delivery report. Step 11 uses the special "Pipeline complete"
#          bottom text (last step in pipeline). Zero logic change.
#   v1.0 — Initial release. JOIN-derived tag architecture (replaces AI classification).
#          Tag values resolved from registry.question_index + blueprint.subtopic_list.
#          Render-source transforms (Rules 19, 21, 22) inherited from proven T2 pipeline.
#          Two-artifact model (integrity + render-source). 15-gate validation.
#          Zero-mutation rule. Exam-agnostic throughout.

---

# ★ ARCHITECTURAL DECISION — JOIN, NOT CLASSIFY

The SSC CGL Tier 2 pipeline (T2_MockTestSort) determined Subject/Topic/Subtopic
by reading question content and classifying it against a hardcoded taxonomy. This
approach has two fatal flaws for a universal framework:

1. **Accuracy risk**: AI classification can misassign questions, especially for
   ambiguous subtopics that span multiple topics.
2. **Exam-specificity**: The classification engine requires a hardcoded taxonomy
   per exam — the opposite of exam-agnostic.

Step 11 uses a fundamentally different architecture: **JOIN-derived tags**.

The pipeline has already determined and certified every tag value upstream:
- Step 7 (MockCreate) assigns `subtopic_id` and `difficulty` per question and writes
  them to `registry.question_index`.
- Step 8 (MockCreateAudit) independently re-derives `subtopic_id` and certifies it;
  `difficulty` is carried forward (not rendered in the paper).
- `blueprint.subtopic_list[]` maps every `subtopic_id` to its `section` (Subject),
  `topic` (Topic), `subtopic` display name (Subtopic), `answer_type`, and
  `answer_cardinality`.

Step 11 performs a deterministic JOIN:

```
registry.question_index[mock_N].questions[q].subtopic_id
  → blueprint.subtopic_list[].section           = Subject
  → blueprint.subtopic_list[].topic             = Topic
  → blueprint.subtopic_list[].subtopic          = Subtopic

blueprint.subtopic_list[].answer_type + answer_cardinality
  → MCQ (option + single)
  → MSQ (option + multi)
  → NAT (numerical + single or multi)           = Question Type

registry.question_index[mock_N].questions[q].difficulty
  → canonical label from blueprint.difficulty_labels  = Complexity
```

**Zero AI classification. Zero hardcoded exam values. Fully deterministic.
Already certified by Step 8.** A tag value is wrong only if the registry or
blueprint is wrong — and those are certified artifacts.

---

# ★ ZERO-MUTATION RULE — NON-NEGOTIABLE

The content of every question block is SACRED. This step may only:
- **Strip** any residual pre-Q.1 header paragraphs (SAFETY-NET only — the input is
  questions-only per Step 7 R8b / G-PREQ1 + Step 8 A-HEADER, so this normally strips
  nothing; a non-zero strip is an upstream regression, flagged in the delivery report)
- **Insert** 5-line tag blocks above each Q-stem (new content only)
- **Linearize** OMML → Unicode text on the render-source copy only
- **Re-font** non-ASCII spans to a safe font on the render-source copy only
- **Recolor** directly-underlined runs in question stems to red FF0000 on the
  render-source copy only

It **NEVER**:
- Changes any character in any question stem, option, table, image, or explanation
- Reorders questions
- Removes, rewrites, or paraphrases any content
- Modifies the integrity artifact in any way other than stripping residual headers
  (safety-net) and inserting tag blocks
- Drops or reorders the document root's namespace declarations, or lets mc:Ignorable
  name a prefix that is not declared (v1.3 — see the FOURTH hard invariant)

Violation of this rule is a hard failure regardless of any other outcome.

---

# ★ WHY THE RENDER-SOURCE DOCX IS SEPARATE FROM THE INTEGRITY ARTIFACT

Three empirically verified facts drive the two-artifact design (inherited from
the verified Tier-1 and Tier-2 pipelines):

**Fact 1:** A naive python-docx round-trip on a docx containing `<m:oMath>` can
SILENTLY CORRUPT EVERY MATH ELEMENT. Raw OMML must therefore be linearized to
Unicode text in the render-source copy before delivery. The integrity artifact
keeps OMML untouched for archival fidelity.

**Fact 2:** Plain Unicode text runs survive all downstream tooling perfectly —
visually and as extractable, copyable text.

**Fact 3:** A non-ASCII glyph in a run tagged with Arial/Times/Courier can corrupt
the text layer even though it displays correctly. Re-tagging the non-ASCII span to
a glyph-verified safe font makes the text extract byte-identical.

Therefore Step 11 uses a **two-artifact model**: build a byte-perfect content docx
(the *integrity artifact*, carrying native OMML untouched), then build a separate
*render-source docx* in which every OMML zone is linearized to a Unicode text run
and every non-ASCII span is re-fonted to a glyph-verified safe font. **The
render-source docx is the final delivered file.**

**No `soffice`, no `pdftotext`, no `pypdf` required.**

---

# ★ DEFINITION OF DONE

The output Word document is NOT finished until ALL hold:

1. **Output is questions-only before Q.1** — the input is already questions-only
   (Step 7 R8b / G-PREQ1 + Step 8 A-HEADER), so `detect_header_paras()` is a SAFETY-NET
   that should find ZERO. Any non-blank, non-Q-stem paragraph before Q.1 is stripped
   (output stays questions-only) AND, if the count is non-zero, a REGRESSION ALARM is
   raised in the delivery report (an upstream Step 7/8 leak to fix).
2. **All tag blocks inserted** — every Q-stem preceded by exactly 5 tag
   paragraphs in order (total_questions tag blocks, count read from blueprint).
3. **Zero content mutation** — no character changed in any question, option, image,
   table, or explanation.
4. **All 16 audit gates pass** (§6) — run before docx delivery.
5. **Math as Unicode text** — zero `<m:oMath>` in render-source docx; every
   linearized string is copy-paste–correct.
6. **Symbols as Unicode text** — every non-ASCII codepoint in the source survives
   copy-paste with exact codepoint.
7. **Tag values are JOIN-verified** — every Subject/Topic/Subtopic/Question Type/
   Complexity value traces to a registry + blueprint JOIN, not to content inference.
8. **Output is a .docx file** — the render-source docx assembled per §5 pipeline.
9. **`present_files` called** immediately after docx verified — before any other output.
10. **In-chat delivery report** printed after `present_files` (§8).
11. **Opens clean in Microsoft Word** — the delivered docx opens with NO "unreadable
    content / recover?" prompt (v1.3 — final acceptance check, §10 step 13). python-docx
    and LibreOffice are lenient readers and do NOT prove this.

---

# §1 — SESSION START

## S1-1 — Trigger parsing

```
Trigger: MockDeliver M[N]
Trigger matching is case-insensitive.

Parse:
  N        : positive integer — mock number
  ExamCode : read from blueprint.json in project knowledge.
             If no blueprint.json found → HARD STOP:
               "No blueprint.json found in project knowledge.
                Run MockBlueprint first and upload blueprint.json
                to this project."
```

## S1-2 — Preflight (HARD STOP on any failure)

```
1. Verify Solutions docx attached. Accept either:
     [ExamCode]_Mock[N]_Solutions_Audited.docx  (Step 10 output — preferred)
     [ExamCode]_Mock[N]_Solutions.docx           (Step 9 output — acceptable)
   If neither attached → HARD STOP: "Attach the Solutions docx for Mock [N]."

2. Verify blueprint.json in project knowledge.
   Read: exam_code, total_questions, sections[], subtopic_list[],
         difficulty_labels, q_types.
   If exam_code missing → HARD STOP.

3. Verify registry.json in project knowledge.
   Read: question_index — find the mock N entry.
   If no mock N entry in question_index → HARD STOP:
     "registry.json has no question_index entry for Mock [N].
      Run MockCreate + MockCreateAudit for Mock [N] first."

4. Verify question_index[mock_N] has exactly total_questions entries
   with q = 1..total_questions (sorted, unique, complete).
   If mismatch → HARD STOP: report the gap.

5. Verify every question in question_index[mock_N] resolves to an entry in
   blueprint.subtopic_list[] — by subtopic_id when present, else by
   (section, subtopic). If any unresolved → HARD STOP: list the unresolved keys.

6. Defensive-copy the uploaded docx to /home/claude/deliver_work/inputs_safe/.
   (Gate C16(b) needs this pristine pre-edit source to prove the delivered file
   dropped no root namespaces.)

7. Verify the render-safe font stack is installed:
     DejaVu Sans  /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
     FreeSans     /usr/share/fonts/truetype/freefont/FreeSans.ttf
   FreeSans covers section markers absent from DejaVu Sans (❌ U+274C, ⬛ U+2B1B,
   ✅ U+2705, and similar). If FreeSans is missing, INSTALL it before proceeding
   (e.g. `apt-get install -y fonts-freefont-ttf`) — otherwise those glyphs render
   as tofu (Rule 21 / v1.3 fix 6). Verify fontTools importable for the Rule 21
   coverage probe. (soffice, pdftotext, pypdf are NOT required.)

8. Parse the docx with lxml via zipfile. Confirm document.xml parses cleanly.

9. Detect Q-stems matching Q_STEM_RE. Confirm count == total_questions.
   Confirm Q-numbers are 1..total_questions continuous, no gaps, no restarts.
```

## S1-3 — Build the tag-value lookup table

```python
import json

def build_tag_lookup(blueprint, registry, mock_n):
    """
    JOIN registry.question_index + blueprint.subtopic_list to produce
    a complete tag-value lookup table for every question in mock N.

    Returns: {q_num: {subject, topic, subtopic, question_type, complexity}}

    JOIN key (v1.3 / FIX 4): prefer registry subtopic_id; fall back to the
    (section, subtopic) display-name pair when the registry has no subtopic_id.
    Tolerant of BOTH registry schemas so a clean run never hard-stops merely on
    the key name.
    """
    # 1. Find mock N in question_index
    qi_entry = next(
        (e for e in registry.get('question_index', []) if e.get('mock') == mock_n),
        None
    )
    if qi_entry is None:
        raise SystemExit(
            f"HARD STOP: No question_index entry for Mock {mock_n} in registry.json.")

    # 2. Build TWO lookup maps from blueprint.subtopic_list so the JOIN works
    #    whether the registry stores subtopic_id (preferred) or only the
    #    (section, subtopic) display names.
    st_by_id = {}                 # subtopic_id -> metadata
    st_by_name = {}               # (section, subtopic) -> metadata
    for st in blueprint.get('subtopic_list', []):
        meta = {
            'section': st['section'],
            'topic': st['topic'],
            'subtopic': st['subtopic'],
            'answer_type': st.get('answer_type', 'option'),
            'answer_cardinality': st.get('answer_cardinality', 'single'),
        }
        sid = st.get('subtopic_id')
        if sid:
            st_by_id[sid] = meta
        name_key = (st['section'], st['subtopic'])
        if name_key in st_by_name:
            raise SystemExit(
                f"HARD STOP: blueprint.subtopic_list has two rows sharing "
                f"(section, subtopic) = {name_key}. The (section, subtopic) JOIN "
                f"fallback would be ambiguous. Give these subtopics distinct "
                f"subtopic_id values AND ensure the registry carries subtopic_id.")
        st_by_name[name_key] = meta

    # 3. Read difficulty_labels for canonical Complexity vocabulary
    difficulty_labels = blueprint.get('difficulty_labels', ['Easy', 'Medium', 'Hard'])

    # 4. Resolve Question Type from answer_type + answer_cardinality
    def resolve_question_type(answer_type, answer_cardinality):
        if answer_type == 'numerical':
            return 'NAT'
        elif answer_cardinality == 'multi':
            return 'MSQ'
        else:
            return 'MCQ'

    # 5. Build the per-question lookup
    lookup = {}
    for q_entry in qi_entry.get('questions', []):
        q = int(q_entry['q'])
        difficulty = q_entry.get('difficulty')

        if not difficulty:
            raise SystemExit(
                f"HARD STOP: Q{q} has no 'difficulty' field in "
                f"registry.question_index. Registry may be corrupt or pre-v1.12.")

        # Resolve subtopic metadata: prefer subtopic_id; fall back to
        # (section, subtopic) display-name JOIN (FIX 4).
        sid = q_entry.get('subtopic_id')
        st_info = None
        if sid and sid in st_by_id:
            st_info = st_by_id[sid]
        else:
            name_key = (q_entry.get('section'), q_entry.get('subtopic'))
            if name_key[0] is not None and name_key[1] is not None:
                st_info = st_by_name.get(name_key)
            if st_info is None:
                raise SystemExit(
                    f"HARD STOP: Q{q} could not be JOINed to blueprint.subtopic_list. "
                    f"Tried subtopic_id='{sid}' and (section, subtopic)={name_key}. "
                    f"Registry/blueprint mismatch — ensure both are from the same run.")

        # Validate difficulty is in the canonical set
        if difficulty not in difficulty_labels:
            raise SystemExit(
                f"HARD STOP: Q{q} difficulty '{difficulty}' not in "
                f"difficulty_labels {difficulty_labels}.")

        lookup[q] = {
            'subject': st_info['section'],
            'topic': st_info['topic'],
            'subtopic': st_info['subtopic'],
            'question_type': resolve_question_type(
                st_info['answer_type'], st_info['answer_cardinality']),
            'complexity': difficulty,
        }

    return lookup
```

---

# §2 — INPUT DOCX STRUCTURE (Solutions document from Step 10)

Understanding the exact structure is mandatory for correct processing.

## S2-1 — Document-level layout

```
[Q.1 first] NO pre-Q.1 header paragraphs — the paper is questions-only from Step 7
           (R8b / G-PREQ1) and Step 8 (A-HEADER strips any residual). The FIRST non-blank
           body paragraph is the bold "Q.1" stem. detect_header_paras() runs as a
           safety-net and normally finds zero; any hit is an upstream Step 7/8 regression.
[Q blocks] Q.1 body ... Q.N body (interleaved with explanations)
[sectPr]   ALWAYS preserved
```

## S2-2 — Per-question block structure (interleaved Solutions format)

```
[blank para]                     ← visual separator (absent before Q.1)
Q.N  [bold stem text]            ← may span multiple paragraphs
[option lines]                   ← numbered or lettered per exam
[blank para]                     ← separator between options and explanation
Correct Answer: K                ← bold, color NAVY 003366
⬛ AXIOM                         ← bold header
[axiom sentences]
⬛ DEDUCTION                     ← bold header
[deduction steps]
⚡ SPEED HACK                   ← bold header (optional)
[speed hack steps]
❌ WHY WRONG?                   ← bold header (MCQ/MSQ) or
❌ COMMON PITFALLS              ← bold header (NAT)
[wrong-option notes or pitfalls]
```

**Colors present in Solutions docx:**
- `003366` (NAVY): `Correct Answer: K` line — preserved in output docx
- Other colors may be present per exam — all preserved byte-identical

**OMML locations:** question stems, options, explanation sentences, WHY WRONG
option clones. All must be linearized in the render-source.

**Section-marker glyphs** (❌ ⬛ ✅ ⚡ and similar) live in the explanation blocks.
They are non-ASCII and are handled by Rule 21's per-codepoint safe-font selection —
see §7 Rule 21 (v1.3 fix 6).

---

# §3 — TAG VALUE RESOLUTION (the JOIN engine)

## S3-1 — Tag field definitions

| # | Field | Source | Resolution |
|---|---|---|---|
| 1 | Subject | `blueprint.subtopic_list[].section` | JOIN on subtopic_id or (section, subtopic) |
| 2 | Topic | `blueprint.subtopic_list[].topic` | JOIN on subtopic_id or (section, subtopic) |
| 3 | Subtopic | `blueprint.subtopic_list[].subtopic` | JOIN on subtopic_id or (section, subtopic) |
| 4 | Question Type | `blueprint.subtopic_list[].answer_type` + `.answer_cardinality` | Resolved per subtopic |
| 5 | Complexity | `registry.question_index[mock_N].questions[q].difficulty` | Canonical label from `difficulty_labels` |

## S3-2 — Question Type resolution table

| answer_type | answer_cardinality | Question Type |
|---|---|---|
| option | single | MCQ |
| option | multi | MSQ |
| numerical | single | NAT |
| numerical | multi | NAT |

## S3-3 — Tag field order (fixed — never changes)

```
Subject: <value>
Topic: <value>
Subtopic: <value>
Question Type: <value>
Complexity: <value>
```

This order is the pipeline contract. Downstream consumers (upload platforms,
analytics dashboards) expect this exact label sequence. The labels themselves
(`Subject`, `Topic`, `Subtopic`, `Question Type`, `Complexity`) are fixed
English strings — not exam-dependent.

## S3-4 — Pre-tagging validation

Before inserting any tag blocks, verify the complete lookup table:

```python
def validate_tag_lookup(lookup, total_questions):
    """
    Verify the lookup table covers all questions and has no empty values.
    Returns list of issues (empty = all clean).
    """
    issues = []

    # Coverage check: every q from 1..total_questions must be present
    for q in range(1, total_questions + 1):
        if q not in lookup:
            issues.append(f"Q{q}: missing from tag lookup")
            continue
        tags = lookup[q]
        for field in ('subject', 'topic', 'subtopic', 'question_type', 'complexity'):
            if not tags.get(field):
                issues.append(f"Q{q}: empty '{field}' tag value")

    return issues
```

If any issues → HARD STOP. Never insert partial or empty tags.

---

# §4 — CONSTANTS AND HELPERS

## S4-1 — Paragraph classification

⚠️ **Namespace alias note:** This section defines `W` and `M` as namespace
strings. §7 (Rule implementations) defines `W_NS` and `M_NS` for the same
values. In the final script, use a single consistent alias throughout (either
`W` / `M` everywhere, or `W_NS` / `M_NS` everywhere). Both sections' code
uses their own alias — unify before running.

```python
import re, copy, zipfile
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
P_TAG    = f'{{{W}}}p'
TBL_TAG  = f'{{{W}}}tbl'
SECPR_TAG= f'{{{W}}}sectPr'
OMATH_TAG= f'{{{M}}}oMath'
DOCPR_TAG= f'{{{WP}}}docPr'

# Q-stem detection (exam-agnostic: matches Q.1, Q.100, Q.200, etc.)
Q_STEM_RE = re.compile(r'^\s*Q\.?\s*(\d+)[.):]?\s*')

# Option line detection (exam-agnostic: matches numbered or lettered options)
# Numeric: 1. / 2. / 3. / 4. / 5. — any count
# Alpha upper: A. / B. / C. / D. / E. — any count
# Alpha lower: a. / b. / c. / d. / e. — any count
# Parenthesized: (1) / (a) / (A) — any count
# Lower roman: (i) / (ii) / (iii) / (iv) — used by engineering/civil service exams
OPT_RE = re.compile(r'^\s*(?:\d+\.|[a-zA-Z]\.|\(\d+\)|\([a-zA-Z]+\))\s')

# Explanation markers (end stem region for Rule 22)
EXPL_MARKERS = [
    r'^⬛', r'^⚡', r'^❌',
    r'^Correct\s+Answer',
    r'^Accepted\s+Range',          # NAT answer line
    r'^Option\s+\d+',              # WHY WRONG sub-headers (with or without dash)
    r'^STRUCTURAL_ANOMALY',
]

def get_para_text(el):
    """MUST walk both <w:t> and <m:t> — OMML-heavy paragraphs return empty
    string if only <w:t> is walked."""
    return ''.join(c.text for c in el.iter()
                   if c.tag in (f'{{{W}}}t', f'{{{M}}}t') and c.text)

def classify_para(el):
    """Returns: 'q_stem' | 'body_content'"""
    if el.tag != P_TAG:
        return 'body_content'
    text = get_para_text(el).strip()
    if Q_STEM_RE.match(text):
        return 'q_stem'
    return 'body_content'

def is_expl_marker(text):
    return any(re.match(p, text) for p in EXPL_MARKERS)
```

## S4-2 — Header detection (exam-agnostic — SAFETY-NET, v1.2)

Retained UNCHANGED from v1.0. Since Step 7 (R8b / G-PREQ1) and Step 8 (A-HEADER)
guarantee a questions-only input, `detect_header_paras()` is now a defensive
safety-net that should return an EMPTY list on every mock produced by the current
pipeline. A non-empty return is an upstream Step 7/8 regression — the paragraphs are
still stripped (output stays questions-only), and the delivery report raises a
REGRESSION ALARM (§8).

```python
def detect_header_paras(body_children):
    """
    Detect document header paragraphs that appear before Q.1.
    Headers are non-blank, non-Q-stem paragraphs before the first Q-stem.
    Blank paragraphs before Q.1 are NOT headers (they are normal separators).

    Returns: list of indices into body_children to strip.
    """
    header_indices = []
    for idx, el in enumerate(body_children):
        if el.tag == SECPR_TAG:
            continue
        if el.tag == P_TAG:
            text = get_para_text(el).strip()
            if Q_STEM_RE.match(text):
                break  # reached Q.1 — stop scanning
            if text:
                header_indices.append(idx)  # non-blank, non-Q-stem = header
            # blank paragraphs before Q.1 are skipped (not headers)
        elif el.tag == TBL_TAG:
            break  # table before Q.1 is unusual; stop scanning
    return header_indices
```

## S4-3 — Tag block paragraph builder

⚠️ **LEARNT DEFECT (verified T2 M1):** NEVER clone `pPr` from existing body
paragraphs. The first body paragraphs may carry `<w:jc val="center"/>`. Cloning
their `pPr` propagates center-alignment AND paragraph spacing into every tag
block. The fix is to build `pPr` from scratch with explicit `jc=left` and
`spacing before=0 after=0`.

⚠️ **SCHEMA ORDER (v1.3 / FIX 2):** OOXML `CT_PPr` is an ordered sequence —
`<w:spacing>` MUST be emitted BEFORE `<w:jc>`. Emitting `jc` first is
schema-invalid and can trip Word's "unreadable content" repair. The builder
below emits them in the correct order. Gate C16(d) guards against regressions.

```python
def make_tag_para(label, value):
    """Build a minimal left-aligned Arial 11pt tag paragraph: '<label>: <value>'.
    pPr is built from scratch — NEVER cloned from body paragraphs.
    pPr child order is schema-correct: <w:spacing> before <w:jc> (FIX 2).
    One run per paragraph. Returns an lxml element.
    CALLER must ensure value is a non-empty string — never pass None."""
    if not value:
        raise ValueError(f"make_tag_para: value for '{label}' is empty/None — "
                         f"tag resolution must be completed before calling this function")
    p = etree.Element(P_TAG)
    # Minimal pPr: explicit left alignment, zero spacing, single line.
    # CT_PPr schema order: <w:spacing> MUST precede <w:jc> (FIX 2).
    ppr = etree.SubElement(p, f'{{{W}}}pPr')
    spacing = etree.SubElement(ppr, f'{{{W}}}spacing')
    spacing.set(f'{{{W}}}before', '0')
    spacing.set(f'{{{W}}}after', '0')
    spacing.set(f'{{{W}}}line', '240')
    spacing.set(f'{{{W}}}lineRule', 'auto')
    jc = etree.SubElement(ppr, f'{{{W}}}jc')
    jc.set(f'{{{W}}}val', 'left')
    # Build run
    r = etree.SubElement(p, f'{{{W}}}r')
    rpr = etree.SubElement(r, f'{{{W}}}rPr')
    rf = etree.SubElement(rpr, f'{{{W}}}rFonts')
    rf.set(f'{{{W}}}ascii', 'Arial'); rf.set(f'{{{W}}}hAnsi', 'Arial')
    sz = etree.SubElement(rpr, f'{{{W}}}sz'); sz.set(f'{{{W}}}val', '22')
    szCs = etree.SubElement(rpr, f'{{{W}}}szCs'); szCs.set(f'{{{W}}}val', '22')
    t = etree.SubElement(r, f'{{{W}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = f'{label}: {value}'
    return p

TAG_LABELS = ['Subject', 'Topic', 'Subtopic', 'Question Type', 'Complexity']
# Usage per Q-stem:
#   tags = tag_lookup[q_num]
#   values = [tags['subject'], tags['topic'], tags['subtopic'],
#             tags['question_type'], tags['complexity']]
#   tag_paras = [make_tag_para(label, val)
#                for label, val in zip(TAG_LABELS, values)]
```

## S4-4 — DocPr ID reassignment

```python
def reassign_docpr_ids(root):
    counter = 1
    for el in root.iter(DOCPR_TAG):
        el.set('id', str(counter)); counter += 1
```

---

# §5 — BUILD PIPELINE

## Phase 1 — Parse input docx and build tag lookup

```python
import os, re, copy, zipfile, shutil, json
from lxml import etree

# ── Session variables (set from trigger and uploaded file) ──
N = MOCK_NUMBER                 # integer from "MockDeliver M[N]"
src_path = UPLOADED_FILE_PATH   # path to the attached Solutions docx

os.makedirs('/home/claude/deliver_work/inputs_safe', exist_ok=True)
os.makedirs('/home/claude/deliver_work/out', exist_ok=True)
safe_path = f'/home/claude/deliver_work/inputs_safe/Mock{N}_src.docx'
shutil.copy(src_path, safe_path)
src_path = safe_path

# Load blueprint.json and registry.json from project knowledge
# COLLISION CHECK: if multiple *_blueprint.json files exist, HARD STOP
bp_matches = [f'/mnt/project/{f}' for f in os.listdir('/mnt/project/')
              if f.endswith('_blueprint.json')]
reg_matches = [f'/mnt/project/{f}' for f in os.listdir('/mnt/project/')
               if f.endswith('_registry.json')]
if not bp_matches:
    raise SystemExit("HARD STOP: No *_blueprint.json in project knowledge.")
if len(bp_matches) > 1:
    raise SystemExit(
        f"HARD STOP: Multiple blueprint files found: {bp_matches}\n"
        f"Only one [ExamCode]_blueprint.json should exist per project.")
if not reg_matches:
    raise SystemExit("HARD STOP: No *_registry.json in project knowledge.")
if len(reg_matches) > 1:
    raise SystemExit(
        f"HARD STOP: Multiple registry files found: {reg_matches}\n"
        f"Only one [ExamCode]_registry.json should exist per project.")
bp_path = bp_matches[0]
reg_path = reg_matches[0]

blueprint = json.load(open(bp_path, encoding='utf-8'))
registry = json.load(open(reg_path, encoding='utf-8'))

EXAM = blueprint['exam_code']
total_questions = blueprint['total_questions']

# Build the tag-value lookup table (§3)
tag_lookup = build_tag_lookup(blueprint, registry, N)
issues = validate_tag_lookup(tag_lookup, total_questions)
if issues:
    raise SystemExit("HARD STOP: Tag lookup validation failed:\n" +
                     "\n".join(issues))

# Open source docx as ZIP; extract document.xml as lxml tree
with zipfile.ZipFile(src_path) as z:
    doc_xml_bytes = z.read('word/document.xml')
root = etree.fromstring(doc_xml_bytes)
body = root.find(f'{{{W}}}body')

body_children = list(body)  # snapshot before modification
```

## Phase 2 — Build integrity body

1. Walk `body_children` in document order.
2. Detect header paragraphs (§4-2) and mark for removal. SAFETY-NET: on a
   questions-only input (the guaranteed case) this list is EMPTY. Record its
   length as `headers_stripped` for the delivery report; a non-zero value is an
   upstream Step 7/8 regression to be alarmed (§8), not a normal outcome.
3. Identify each `q_stem` paragraph; extract Q-number from `Q_STEM_RE`.
4. Look up tag values from `tag_lookup[q_num]`.
5. Build 5 tag paragraphs using `make_tag_para(label, value)`.
6. Insert them into the body using `parent.insert(idx + i, tag_para_i)` for
   i in 0..4, where `idx = list(body).index(stem_para)` is computed **once
   before any insertion for this Q**. Inserting TAG1 at `idx` pushes the stem
   to `idx+1`; inserting TAG2 at `idx+1` pushes the stem to `idx+2`; and so
   on. After all 5 insertions the stem is at `idx+5`.
7. Remove any detected header paragraphs from the body **after** all tag blocks are
   inserted. Store references to the header ELEMENTS before insertions begin (not
   indices), then remove each element by reference: `body.remove(header_el)`. Index-based
   removal would be wrong because tag insertions shift all indices. (On the guaranteed
   questions-only input there is nothing to remove.)
8. `reassign_docpr_ids(root)` after all insertions.

**Insertion order verification:** after insertion, the sequence immediately
before each Q.N stem must be:

```
[blank separator para — from previous Q's explanation, if not Q.1]
Subject: <value>
Topic: <value>
Subtopic: <value>
Question Type: <value>
Complexity: <value>
Q.N  [stem]
```

## Phase 3 — Assemble integrity docx

⚠️ **v1.3 / FIX 1 + FIX 3 applied below.** Do NOT reintroduce
`etree.cleanup_namespaces()` and do NOT strip `word/webSettings.xml`. Both
changes are load-bearing for Word validity — see the notes in the code.

```python
os.makedirs('/home/claude/deliver_work/out', exist_ok=True)
integrity_path = f'/home/claude/deliver_work/out/{EXAM}_Mock{N}_integrity.docx'

STRUCTURAL_STORED = {
    '[Content_Types].xml', '_rels/.rels', 'word/_rels/document.xml.rels'
}
with zipfile.ZipFile(src_path) as src_zip:
    with zipfile.ZipFile(integrity_path, 'w') as out_zip:
        for name in src_zip.namelist():
            # FIX 3: do NOT strip word/webSettings.xml. It is benign, and copying it
            # through avoids a dangling relationship (in word/_rels/document.xml.rels)
            # and a dangling Override (in [Content_Types].xml) — a Word-corruption
            # trigger. (Rule 14 retired; gate C9 now checks for dangling references.)
            if name == 'word/document.xml':
                # FIX 1 (ROOT CAUSE): do NOT call etree.cleanup_namespaces(root).
                # It removes root xmlns declarations (w14/wp14/o/v/w10 + drawing
                # namespaces) that mc:Ignorable and drawing/VML content still
                # reference, which makes Word report "unreadable content — recover?".
                # lxml preserves every namespace declared on the parsed root when we
                # skip cleanup. Redundant local xmlns on injected runs are legal.
                data = etree.tostring(root, xml_declaration=True,
                                      encoding='UTF-8', standalone=True)
                # etree emits a single-quoted XML decl; normalize to double quotes.
                # (Cosmetic — Word accepts both — kept for byte-consistency.)
                data = data.replace(
                    b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>",
                    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                )
            else:
                data = src_zip.read(name)
            compress = (zipfile.ZIP_STORED if name in STRUCTURAL_STORED
                        else zipfile.ZIP_DEFLATED)
            out_zip.writestr(name, data, compress_type=compress)
```

## Phase 3.5 — Content-integrity gate (all must PASS before rendering)

Run on the integrity docx. All 10 gates must pass. See §6 (C1–C10).

Any FAIL → fix and re-run. Never proceed to Phase 4 with a failing integrity
artifact.

## Phase 4 — Build render-source docx

```python
# Deepcopy the integrity document.xml tree. Because FIX 1 removed the Phase 3
# cleanup_namespaces() call, `root` still carries ALL of its original root xmlns
# declarations here, so render_root inherits a complete, valid namespace set.
render_root = copy.deepcopy(root)

# Step 4a — Rule 19: OMML → Unicode text (math-as-text)
omml_count, linearized_strings = replace_omath_with_text(render_root,
                                                          font='DejaVu Sans')

# Step 4b — Rule 22: Underlined stem text → red FF0000
recolored_count = recolor_underlined_stems(render_root, color='FF0000')

# Step 4c — Rule 21: Non-ASCII spans → per-codepoint safe font (FIX 6)
runs_split, unresolved = apply_symbol_safe_font(render_root,
                                                 default_font='DejaVu Sans')
if unresolved:
    # These codepoints are covered by NO font in _SAFE_STACK. Rule 21 (v1.3)
    # LEAVES them in their original font so Word can font-substitute rather than
    # forcing a font known to lack the glyph. Surface them in the delivery report;
    # not a HARD STOP (the codepoint survives in the text layer), but the font may
    # not render it visually. If a marker is affected, install a covering font
    # (e.g. add Noto Sans Symbols to the preflight font set) and re-run.
    print(f"WARNING: {len(unresolved)} non-ASCII codepoints covered by no safe font:")
    for c in sorted(unresolved, key=ord):
        print(f"  U+{ord(c):04X} '{c}'")
```

## Phase 5 — Assemble and deliver render-source docx

⚠️ **v1.3 / FIX 1 + FIX 3 applied below** (same as Phase 3). This is the
DELIVERED file — the corruption the learner saw came from this assembly.

```python
render_out_path = f'/home/claude/deliver_work/out/{EXAM}_Mock{N}_Tagged.docx'
reassign_docpr_ids(render_root)
with zipfile.ZipFile(src_path) as src_zip:
    with zipfile.ZipFile(render_out_path, 'w') as out_zip:
        for name in src_zip.namelist():
            # FIX 3: keep word/webSettings.xml (do not strip) — no dangling refs.
            if name == 'word/document.xml':
                # FIX 1 (ROOT CAUSE): do NOT call etree.cleanup_namespaces(render_root).
                data = etree.tostring(render_root, xml_declaration=True,
                                      encoding='UTF-8', standalone=True)
                data = data.replace(
                    b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>",
                    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                )
            else:
                data = src_zip.read(name)
            compress = (zipfile.ZIP_STORED if name in STRUCTURAL_STORED
                        else zipfile.ZIP_DEFLATED)
            out_zip.writestr(name, data, compress_type=compress)
shutil.copy(render_out_path,
            f'/mnt/user-data/outputs/{EXAM}_Mock{N}_Tagged.docx')
```

**The render-source docx IS the final delivered file. No `soffice` conversion
is performed.**

---

# §6 — VALIDATION CHECKLIST (all 16 must PASS)

**Content-integrity gate — integrity docx (Phase 3.5):**

**C1** Valid ZIP; `document.xml` parses without error.

**C2** Q-count = total_questions (from blueprint); stems read Q.1, Q.2, …
Q.{total_questions} in document order, no gaps, no restarts.

**C3** Every Q-stem preceded by exactly 5 tag paragraphs in correct label
order: Subject / Topic / Subtopic / Question Type / Complexity.

**C4** Strip complete: zero header paragraphs remain before Q.1 (the safety-net
result — on the guaranteed questions-only input, zero were detected AND zero remain;
if any were detected the delivery report carries a REGRESSION ALARM).

**C5** OMML count unchanged: `<m:oMath>` count in integrity docx ==
`<m:oMath>` count in source docx.

**C6** Drawing count unchanged: total `<w:drawing>` elements in integrity
docx == source docx.

**C7** `003366` (NAVY) color count unchanged: Correct Answer line colors
preserved.

**C8** DocPr IDs are unique across the entire document.

**C9** No dangling references in the integrity docx (v1.3 — repurposed from the old
"webSettings.xml absent" check, since FIX 3 now KEEPS webSettings.xml): for every
`*.rels` part, every relationship whose `TargetMode` is not `External` resolves to a
part present in the ZIP, AND every `[Content_Types].xml` `Override` `PartName` exists
in the ZIP. Zero dangling relationships and zero dangling Overrides.

**C10** No blank Subject/Topic/Subtopic/Question Type/Complexity tag value
(every field non-empty for all tag blocks).

**Docx math/symbol-text gate — render-source docx (after Phase 5 assembly):**

**C11** Math conservation: `omml_count` returned by `replace_omath_with_text`
== `<m:oMath>` count from C5; render-source `document.xml` contains **zero**
residual `<m:oMath>` elements after linearization.

**C12** Render-source docx opens as a valid ZIP; `document.xml` in
render-source parses without error.

**C13** Text conservation in render-source: every `Q.N` (N=1..total_questions)
present; total_questions occurrences each of `Subject:`, `Topic:`, `Subtopic:`,
`Question Type:`, `Complexity:`; `Correct Answer:` count matches source; zero
header paragraphs.

**C14** Math + symbol round-trip: read all `<w:t>` text from render-source
`document.xml`; collapse runs of whitespace; assert both:
  - **(a)** Every linearized math string from `linearized_strings` appears
    **verbatim** in the normalized extracted text. Codepoints exact: `³`=U+00B3,
    `²`=U+00B2, `−`=U+2212, never `a 3` or hyphen `-`.
  - **(b)** Every non-ASCII codepoint present in the source body appears in the
    render-source with the **exact codepoint**.

**C15** Stem-underline recolor (Rule 22): in the render-source, every
directly-underlined run inside a stem region carries `w:color="FF0000"`;
zero color changes on options, explanation blocks, tag headers, or table
contents; NAVY `003366` Correct Answer color count unchanged.

**Docx namespace/reference/order integrity gate — render-source docx (v1.3):**

**C16** Namespace + reference + tag-order integrity (FIX 5). Run on the DELIVERED
render-source docx. Needs the pristine pre-edit source from `inputs_safe/` for
C16(b).

  - **C16(a) — mc:Ignorable coverage:** every prefix token in the output root's
    `mc:Ignorable` MUST be declared as `xmlns:<prefix>` on that root.
  - **C16(b) — namespace superset:** the output root's `xmlns:` prefix set MUST be a
    superset of the SOURCE `document.xml` root's set (nothing dropped). This is the
    direct guard against the FIX 1 root cause.
  - **C16(c) — no dangling relationships:** for every `*.rels` part, every
    relationship whose `TargetMode` is not `External` MUST resolve to a part that
    exists in the ZIP (guards FIX 3).
  - **C16(d) — tag-block order:** for every inserted tag paragraph, `pPr` children
    must be `[spacing, jc]` in that order (guards FIX 2, which C16(a–c) cannot see).

```python
import re, posixpath, zipfile
from lxml import etree
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def gate_c16(src_docx, out_docx,
             tag_labels=('Subject','Topic','Subtopic','Question Type','Complexity')):
    def root_ns_and_ignorable(zf):
        data = zf.read('word/document.xml').decode('utf-8', 'replace')
        tag = re.search(r'<w:document\b[^>]*>', data).group(0)
        ns = set(re.findall(r'xmlns:([A-Za-z0-9]+)=', tag))
        ig = re.search(r'mc:Ignorable="([^"]*)"', tag)
        return ns, set((ig.group(1).split() if ig else []))
    with zipfile.ZipFile(src_docx) as sz, zipfile.ZipFile(out_docx) as oz:
        src_ns, _ = root_ns_and_ignorable(sz)
        out_ns, out_ign = root_ns_and_ignorable(oz)
        names = set(oz.namelist())
        a = out_ign.issubset(out_ns)                     # C16(a)
        b = src_ns.issubset(out_ns)                      # C16(b)
        dangling = []
        for n in names:
            if not n.endswith('.rels'): continue
            base = '/'.join(n.split('/')[:-2])
            for rel in etree.fromstring(oz.read(n)):
                if rel.get('TargetMode') == 'External': continue
                resolved = posixpath.normpath(
                    posixpath.join(base, rel.get('Target'))).lstrip('/')
                if resolved not in names:
                    dangling.append((n, rel.get('Target')))
        c = (len(dangling) == 0)                         # C16(c)
        root = etree.fromstring(oz.read('word/document.xml'))
        order_ok = True
        for p in root.iter(f'{{{W}}}p'):
            txt = ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))
            if any(txt.startswith(l + ':') for l in tag_labels):
                ppr = p.find(f'{{{W}}}pPr')
                kids = [etree.QName(x).localname for x in ppr] if ppr is not None else []
                if 'spacing' in kids and 'jc' in kids and \
                   kids.index('spacing') > kids.index('jc'):
                    order_ok = False; break
        d = order_ok                                     # C16(d)
    return (a and b and c and d,
            {'ignorable_ok': a, 'ns_superset': b, 'no_dangling': c,
             'tag_order_ok': d, 'dangling': dangling})
```

Any C16 FAIL → HARD STOP (fix and re-run).

**Optional stronger gate — OOXML XSD validation (recommended for a 200-exam guarantee):**
If the OOXML `wml.xsd` schema set is available in the environment, validate
render-source `word/document.xml` against it with `lxml.etree.XMLSchema`. A schema
failure is a HARD STOP. This catches element-order and structural violations that the
targeted gates above may not enumerate. If the XSD is not present, skip (do not block),
and rely on C16 + the mandatory Word open (§10 step 13).

---

# §7 — RULE IMPLEMENTATIONS (verified helpers from Tier-1/Tier-2 pipeline)

## Rule 19 — OMML → Selectable Unicode Text

Operates on the render-source deepcopy only. Never the integrity artifact.

```python
M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def _m(t): return f'{{{M_NS}}}{t}'
def _w(t): return f'{{{W_NS}}}{t}'
def _loc(el): return etree.QName(el).localname

SUP = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵',
 '6':'⁶','7':'⁷','8':'⁸','9':'⁹','+':'⁺','-':'⁻',
 '−':'⁻','=':'⁼','(':'⁽',')':'⁾','a':'ᵃ','b':'ᵇ',
 'c':'ᶜ','d':'ᵈ','e':'ᵉ','f':'ᶠ','g':'ᵍ','h':'ʰ',
 'i':'ⁱ','j':'ʲ','k':'ᵏ','l':'ˡ','m':'ᵐ','n':'ⁿ',
 'o':'ᵒ','p':'ᵖ','r':'ʳ','s':'ˢ','t':'ᵗ','u':'ᵘ',
 'v':'ᵛ','w':'ʷ','x':'ˣ','y':'ʸ','z':'ᶻ'}
SUB = {'0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅',
 '6':'₆','7':'₇','8':'₈','9':'₉','+':'₊','-':'₋',
 '−':'₋','=':'₌','(':'₍',')':'₎','a':'ₐ','e':'ₑ',
 'h':'ₕ','i':'ᵢ','j':'ⱼ','k':'ₖ','l':'ₗ','m':'ₘ',
 'n':'ₙ','o':'ₒ','p':'ₚ','r':'ᵣ','s':'ₛ','t':'ₜ',
 'u':'ᵤ','v':'ᵥ','x':'ₓ'}
RAD = {'2':'√','3':'∛','4':'∜'}
DASHES = '-‐‑–—−'
OPS = '+−±×÷=≤≥≠≈'

def _map(s, table):
    out = ''
    for ch in s:
        if ch in table: out += table[ch]
        else: return None
    return out

def _has_op(s):   return bool(re.search(r'[+\-−*/ ]', s.strip()))
def _compound(s): return _has_op(s) or len(s.strip()) > 1

def _norm(s):
    s = ''.join('−' if ch in DASHES else ch for ch in s)
    return s.replace('*', '×')

def _lin(el):
    tag = _loc(el)
    if tag in ('oMath','oMathPara','e','num','den','sup','sub','deg','lim','fName','box'):
        return ''.join(_lin(c) for c in el)
    if tag == 'r':
        return _norm(''.join((t.text or '') for t in el.iter(_m('t'))))
    if tag == 'f':
        n = _lin(el.find(_m('num'))); d = _lin(el.find(_m('den')))
        if _compound(n): n = f'({n})'
        if _compound(d): d = f'({d})'
        return f'{n}/{d}'
    if tag == 'sSup':
        b = _lin(el.find(_m('e'))); s = _lin(el.find(_m('sup'))); u = _map(s, SUP)
        return b + u if u is not None else (f'{b}^({s})' if _compound(s) else f'{b}^{s}')
    if tag == 'sSub':
        b = _lin(el.find(_m('e'))); s = _lin(el.find(_m('sub'))); u = _map(s, SUB)
        return b + u if u is not None else (f'{b}_({s})' if _compound(s) else f'{b}_{s}')
    if tag == 'sSubSup':
        b = _lin(el.find(_m('e'))); sb = _lin(el.find(_m('sub'))); sp = _lin(el.find(_m('sup')))
        ub = _map(sb, SUB); up = _map(sp, SUP)
        return b + (ub if ub is not None else f'_({sb})') + (up if up is not None else f'^({sp})')
    if tag == 'sPre':
        sb = _lin(el.find(_m('sub'))); sp = _lin(el.find(_m('sup'))); e = _lin(el.find(_m('e')))
        ub = _map(sb, SUB); up = _map(sp, SUP)
        return (ub if ub is not None else f'_({sb})') + (up if up is not None else f'^({sp})') + e
    if tag == 'rad':
        e = _lin(el.find(_m('e'))); deg = el.find(_m('deg'))
        dt = _lin(deg).strip() if (deg is not None and len(deg)) else ''
        body = f'({e})' if _has_op(e) else e
        if dt and dt in RAD: return RAD[dt] + body
        if dt:
            ud = _map(dt, SUP); return (ud if ud else f'[{dt}]') + '√' + body
        return '√' + body
    if tag == 'd':
        beg, end = '(', ')'; dpr = el.find(_m('dPr'))
        if dpr is not None:
            bc = dpr.find(_m('begChr')); ec = dpr.find(_m('endChr'))
            if bc is not None and bc.get(_m('val')) is not None: beg = bc.get(_m('val'))
            if ec is not None and ec.get(_m('val')) is not None: end = ec.get(_m('val'))
        inner = ''.join(_lin(c) for c in el if _loc(c) == 'e')
        return f'{beg}{inner}{end}'
    if tag == 'nary':
        op = '∫'; np_ = el.find(_m('naryPr'))
        if np_ is not None:
            c = np_.find(_m('chr'))
            if c is not None and c.get(_m('val')): op = c.get(_m('val'))
        sb = el.find(_m('sub')); sp = el.find(_m('sup')); e = el.find(_m('e')); s = op
        if sb is not None and len(sb):
            t = _lin(sb); u = _map(t, SUB); s += u if u is not None else f'[{t}]'
        if sp is not None and len(sp):
            t = _lin(sp); u = _map(t, SUP); s += u if u is not None else f'^({t})'
        if e is not None: s += ' ' + _lin(e)
        return s
    if tag == 'func':
        fn = el.find(_m('fName')); e = el.find(_m('e'))
        return f"{_lin(fn).strip()}({_lin(e)})"
    if tag in ('acc', 'bar'):
        return _lin(el.find(_m('e')))
    if tag in ('limLow', 'limUpp'):
        return f"{_lin(el.find(_m('e')))}[{_lin(el.find(_m('lim')))}]"
    if tag == 'm':
        rows = ['; '.join(_lin(c) for c in mr.findall(_m('e')))
                for mr in el.findall(_m('mr'))]
        return '[' + ' | '.join(rows) + ']'
    return ''.join(_lin(c) for c in el)

def _space_ops(s):
    for op in OPS:
        s = s.replace(op, f' {op} ')
    s = re.sub(r'[ \t]+', ' ', s).strip()
    s = (s.replace('( ', '(').replace(' )', ')').replace('[ ', '[')
          .replace(' ]', ']').replace('{ ', '{').replace(' }', '}'))
    s = re.sub(r'(^|[\(\[\{])\s*([+−±])\s+', r'\1\2', s)
    return s

def linearize_omml(el):
    return _space_ops(_lin(el))

def replace_omath_with_text(doc_root, font='DejaVu Sans'):
    """Render-source ONLY. Replaces each <m:oMath> (or its parent <m:oMathPara>)
    with a single Unicode text run tagged with `font`.
    Returns (count_replaced, list_of_linearized_strings)."""
    maths = [e for e in doc_root.iter() if _loc(e) == 'oMath']
    linearized = []
    for math_el in maths:
        text = linearize_omml(math_el)
        linearized.append(text)
        run = etree.fromstring(
            f'<w:r xmlns:w="{W_NS}"><w:rPr>'
            f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/></w:rPr>'
            f'<w:t xml:space="preserve"></w:t></w:r>')
        run.find(_w('t')).text = text
        target = math_el
        if target.getparent() is not None and _loc(target.getparent()) == 'oMathPara':
            target = target.getparent()
        parent = target.getparent()
        if parent is None:
            continue
        parent.replace(target, run)
    return len(maths), linearized
```

## Rule 22 — Question-Stem Underline → Red FF0000

Operates on render-source AFTER Rule 19, BEFORE Rule 21. Never the integrity
artifact.

```python
def recolor_underlined_stems(root, color='FF0000'):
    """RENDER-SOURCE ONLY. In the question stem region only, set the font color
    of every directly-underlined run to FF0000. Preserves underline, bold, size,
    font, text, and run boundaries — only <w:color> changes.

    Stem region: from the Q.<n> stem paragraph up to but NOT including the first
    option line or explanation marker. Stem continuation paragraphs (passages,
    Statements:, Conclusions:) are included.

    NEVER touches: options, explanation blocks, tag headers, or table contents.
    Returns count of runs recolored."""
    body = root.find(f'{{{W_NS}}}body')
    if body is None: return 0
    recolored = 0
    in_stem = False
    for el in list(body):
        tag = el.tag
        if tag == f'{{{W_NS}}}tbl':
            continue
        if tag == f'{{{W_NS}}}sectPr':
            in_stem = False; continue
        if tag != P_TAG:
            continue
        text = get_para_text(el).strip()
        if Q_STEM_RE.match(text):
            in_stem = True
        elif in_stem:
            if OPT_RE.match(text) or is_expl_marker(text):
                in_stem = False
        if not in_stem:
            continue
        for r in el.findall(f'{{{W_NS}}}r'):
            rpr = r.find(f'{{{W_NS}}}rPr')
            if rpr is None: continue
            u = rpr.find(f'{{{W_NS}}}u')
            if u is None: continue
            if u.get(f'{{{W_NS}}}val') == 'none': continue
            col = rpr.find(f'{{{W_NS}}}color')
            if col is None:
                col = etree.SubElement(rpr, f'{{{W_NS}}}color')
            col.set(f'{{{W_NS}}}val', color)
            recolored += 1
    return recolored
```

## Rule 21 — Symbol-Safe Re-Font (v1.3 — multi-font, per-codepoint)

Operates on render-source AFTER Rules 19 and 22. Never the integrity artifact.

⚠️ **v1.3 / FIX 6.** The old implementation forced EVERY non-ASCII segment to a
single `default_font` (DejaVu Sans). Section markers ❌ (U+274C), ⬛ (U+2B1B),
✅ (U+2705) are NOT in DejaVu Sans, so that forced them to render as tofu even
though the text layer was intact. This version:
  1. extends `_SAFE_STACK` with FreeSans (which covers ❌ ⬛ ✅ ⚡);
  2. selects the safe font PER non-ASCII codepoint — the first stacked font that
     covers it — and splits runs on font boundaries;
  3. leaves any codepoint that NO stacked font covers in its ORIGINAL font (so Word
     can font-substitute rather than showing tofu from a font we KNOW lacks the
     glyph) and records it in `unresolved` for the delivery report.
Preflight (§1 S1-2 step 7) verifies FreeSans is installed. The coverage probe below
is empirical — it never assumes a glyph is present.

```python
from fontTools.ttLib import TTFont

_SAFE_STACK = [
    ("DejaVu Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ("FreeSans",    "/usr/share/fonts/truetype/freefont/FreeSans.ttf"),
]

def _coverage(path):
    f = TTFont(path, fontNumber=0); s = set()
    for t in f['cmap'].tables: s |= set(t.cmap.keys())
    return s

_COV = {name: _coverage(path) for name, path in _SAFE_STACK}

def _font_for(cp):
    """First stacked safe font whose cmap covers codepoint cp, else None."""
    for name, _ in _SAFE_STACK:
        if cp in _COV[name]: return name
    return None

def _set_rfonts(rpr, font):
    rf = rpr.find(_w('rFonts'))
    if rf is None:
        rf = etree.Element(_w('rFonts')); rpr.insert(0, rf)
    for a in ('ascii', 'hAnsi', 'cs'): rf.set(_w(a), font)

def _seg_key(ch):
    """Segment key for a character:
       '__ascii__'  -> ASCII (keep original font)
       <font name>  -> non-ASCII covered by this safe font
       None         -> non-ASCII covered by NO safe font (keep original, log)."""
    if ord(ch) < 128:
        return '__ascii__'
    return _font_for(ord(ch))

def apply_symbol_safe_font(root, default_font='DejaVu Sans'):
    """RENDER-SOURCE ONLY (Rule 21, v1.3). Split each single-<w:t> run into maximal
    same-key spans (ASCII / per-covering-safe-font / uncovered) and re-font only the
    covered non-ASCII spans to their covering safe font. Preserves rPr on every
    fragment via deepcopy. Uncovered non-ASCII codepoints keep their original font
    and are returned in `unresolved`. `default_font` is retained for API
    compatibility; the per-codepoint stack governs actual font choice.
    Returns (runs_split, unresolved_codepoints)."""
    runs_split = 0; unresolved = set()
    for r in list(root.iter(_w('r'))):
        ts = r.findall(_w('t'))
        if len(ts) != 1: continue
        txt = ts[0].text or ''
        if not txt or all(ord(c) < 128 for c in txt): continue
        # Segment by key: consecutive chars sharing the same _seg_key.
        segs = []; cur = ''; key = None
        for ch in txt:
            k = _seg_key(ch)
            if not cur:
                cur = ch; key = k
            elif k == key:
                cur += ch
            else:
                segs.append((cur, key)); cur = ch; key = k
        if cur:
            segs.append((cur, key))
        if len(segs) == 1 and segs[0][1] == '__ascii__':
            continue
        rpr = r.find(_w('rPr')); parent = r.getparent()
        idx = list(parent).index(r); out = []
        for seg, key in segs:
            nr = etree.Element(_w('r'))
            if rpr is not None: nr.append(copy.deepcopy(rpr))
            if key not in ('__ascii__', None):
                # Non-ASCII covered by a specific safe font -> pin that font.
                npr = nr.find(_w('rPr'))
                if npr is None:
                    npr = etree.SubElement(nr, _w('rPr')); nr.insert(0, npr)
                _set_rfonts(npr, key)
            elif key is None:
                # Non-ASCII covered by NO stacked font: leave the original rPr/font
                # so Word can font-substitute (better than known-tofu). Log it.
                unresolved |= {c for c in seg}
            # ASCII segment ('__ascii__'): keep the original rPr untouched.
            t = etree.SubElement(nr, _w('t'))
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            t.text = seg
            out.append(nr)
        for off, nr in enumerate(out): parent.insert(idx + off, nr)
        parent.remove(r); runs_split += 1
    return runs_split, unresolved
```

**Rule interaction order:** Rule 19 first (OMML → text), then Rule 22
(underline recolor — skips linearized math runs since they carry no `<w:u>`),
then Rule 21 (safe-font — deepcopies each run's `<w:rPr>` onto fragments,
so Rule 22's `<w:color>` propagates automatically).

---

# §8 — FILE NAMING & DELIVERY

Output file: `[ExamCode]_Mock[N]_Tagged.docx`
Output path: `/mnt/user-data/outputs/[ExamCode]_Mock[N]_Tagged.docx`

`present_files` is called immediately after all 16 checklist gates pass.
No other files are presented.

**In-chat delivery report (printed after `present_files`):**

```
MockDeliver M[N] — Delivery Report
=====================================
Exam         : [ExamCode] ([exam_name])
Mock         : [N]
Checklist    : C1–C16 all PASS

Questions tagged  : [total_questions] / [total_questions]
Headers stripped  : [count]  (expected 0 — input is questions-only per Step 7/8)
Header regression : none      (or: ⚠ REGRESSION ALARM — [count] pre-Q.1 paragraph(s)
                               were present and stripped. The Complete/Solutions docx
                               should be questions-only (Step 7 R8b/G-PREQ1 + Step 8
                               A-HEADER). Re-run Step 8 on the upstream paper.)

OMML zones linearized : [count]
Non-ASCII codepoints  : [count] unique; all survived docx text-layer check
Runs re-fonted (R21)  : [count]
Stem-underline recolor (R22): [count] runs recolored red
Unresolved glyph defects: none  (or: list of U+XXXX codepoints covered by no safe
                               font — left in original font for Word substitution;
                               install a covering font and re-run if a marker shows)

Namespace/reference (C16): superset OK · mc:Ignorable covered · 0 dangling refs · tag order OK

Tag summary:
  Complexity distribution:
    [label1]: [count] Q
    [label2]: [count] Q
    [label3]: [count] Q

  Question Type distribution:
    [type1]: [count] Q
    [type2]: [count] Q  (if multiple types exist)

  Subject distribution:
    [Section1] ([count]): [Subtopic1: N, Subtopic2: N, ...]
    [Section2] ([count]): [Subtopic1: N, Subtopic2: N, ...]
    ...

Output: [ExamCode]_Mock[N]_Tagged.docx
```

**Post-delivery footer (MANDATORY after present_files):**
After the present_files call and in-chat delivery report above, render the standardized
visual delivery footer as the LAST element in the response. Follow Framework_DeliveryFooter.md
for footer type (F2 step-complete — always for Step 11), file badge (Use locally for
Tagged.docx), and next-step reference. Step 11 uses the special bottom text:
"Pipeline complete for [ExamCode] Mock [N]. Thank you!" (last step — no next step).
For the next mock: "Step 7: MockCreate M[N+1]".

---

# §9 — EDGE CASES

## EC-1 — Solutions docx is questions-only (the guaranteed, normal case)

Since Step 7 (R8b / G-PREQ1) never emits a pre-Q.1 block and Step 8 (A-HEADER) strips
any residual, the Solutions docx starts directly with Q.1. `detect_header_paras()`
returns an empty list, nothing is stripped, and C4 passes (zero detected, zero remain).
This is the expected case for every mock produced by the current pipeline; the delivery
report reads "Headers stripped: 0" and "Header regression: none".

## EC-2 — Solutions docx has pre-Q.1 header paragraphs (UPSTREAM REGRESSION — safety-net)

This should NOT occur: Step 7 R8b / G-PREQ1 and Step 8 A-HEADER together guarantee a
questions-only paper. If a title/info/scoring block nonetheless appears before Q.1, it is
an upstream regression (a Step 7 generator leak that Step 8 failed to strip). The
safety-net `detect_header_paras()` still removes it (the delivered Tagged.docx stays
questions-only) and C4 verifies removal, but the delivery report raises a REGRESSION ALARM
naming the count so the upstream Step 7/8 run can be fixed. Never silently absorb it as if
it were normal — Step 11 delivers correctly AND surfaces the leak.

## EC-3 — Exam with MSQ questions

Some questions may have `Question Type: MSQ`. This is resolved entirely from
`blueprint.subtopic_list[].answer_cardinality == 'multi'`. No special handling
in the tagging pipeline — the tag value is simply `MSQ` instead of `MCQ`.

## EC-4 — Exam with NAT questions

Some questions may have `Question Type: NAT`. Resolved from
`blueprint.subtopic_list[].answer_type == 'numerical'`. NAT questions may have
different option structures (no option lines, or a single answer field). The
tagging pipeline does not inspect option structure — it only inserts tags.

## EC-5 — Zero OMML in source docx

If the Solutions docx has no `<m:oMath>` elements (pure text exam),
`replace_omath_with_text` returns `(0, [])`. C5 passes (0 == 0). C11 passes
(0 replaced, 0 residual). C14(a) is trivially satisfied (empty list).

## EC-6 — Missing question_index for mock N

If `registry.question_index` has no entry for mock N, Step 11 halts at S1-2
step 3. The user must run Step 7 + Step 8 for mock N first. Step 11 never
guesses or infers tag values from content.

## EC-7 — Subtopic mismatch between registry and blueprint

If a question cannot be JOINed to `blueprint.subtopic_list[]` by subtopic_id OR by
(section, subtopic), Step 11 halts at S1-3 (`build_tag_lookup`). This indicates a
registry/blueprint version mismatch. The user must ensure both files are from the
same pipeline run.

## EC-8 — Difficulty label not in canonical set

If any question's `difficulty` value is not in `blueprint.difficulty_labels`,
Step 11 halts at S1-3. This indicates a registry corruption. The user must
re-run Step 7 + Step 8.

## EC-9 — Table or drawing element before Q.1

If a table or drawing appears before Q.1 in the document body,
`detect_header_paras()` stops scanning (conservative — tables are unusual
before Q.1 and may be part of content). This prevents accidental stripping
of content elements.

## EC-10 — Blank separator paragraph between header and Q.1

Blank paragraphs before Q.1 are NOT stripped (they are normal visual
separators). Only non-blank, non-Q-stem paragraphs before Q.1 are considered
headers. This prevents loss of intended spacing.

## EC-11 — Namespace preservation (v1.3 — the root-cause guard)

The document root declares many namespaces (w14/wp14/o/v/w10 + drawing) and an
`mc:Ignorable` list that references some of them. Step 11 must NEVER drop or reorder
these. `etree.cleanup_namespaces()` is BANNED (FIX 1) because it strips declarations it
considers "unused" without understanding that `mc:Ignorable` references them by name —
which makes Word treat the file as corrupt. C16(a)/(b) verify this on the delivered
file. If C16(b) fails (source namespace not a subset of output), a banned cleanup call
has crept back in — remove it.

## EC-12 — Non-ASCII codepoint covered by no installed font (v1.3)

If a source codepoint is covered by neither DejaVu Sans nor FreeSans, Rule 21 leaves it
in its original font (so Word can font-substitute) and lists it under
"Unresolved glyph defects" in the delivery report. The text layer is intact (copy-paste
correct); only the visual glyph is at risk. If a learner-visible marker is affected,
add a covering font (e.g. Noto Sans Symbols) to the preflight font set and `_SAFE_STACK`,
then re-run. Not a HARD STOP.

---

# §10 — EXECUTION CHECKLIST (every invocation)

1. ☐ Read this spec — this file wins over memory, chat history, and older code.
2. ☐ Defensive-copy upload to `/home/claude/deliver_work/inputs_safe/` — done
     in Phase 1 (also needed by gate C16(b)).
3. ☐ Preflight: load blueprint.json + registry.json; build tag lookup table;
     verify BOTH DejaVu Sans AND FreeSans fonts (install FreeSans if missing);
     verify fontTools importable. HARD STOP if any missing. (`soffice`,
     `pdftotext`, `pypdf` NOT needed.)
4. ☐ Phase 1: parse source docx via lxml + zipfile. `get_para_text()` walks
     both `<w:t>` and `<m:t>`.
5. ☐ Phase 2: detect headers (SAFETY-NET — normally zero on the questions-only
     input; a non-zero count is an upstream Step 7/8 regression, alarmed in §8) →
     build tag blocks from lookup table → insert into integrity body. Strip any
     detected headers after all insertions.
6. ☐ Phase 3: assemble integrity docx (ZIP; KEEP webSettings.xml — FIX 3; NO
     cleanup_namespaces — FIX 1; double-quoted XML decl; ZIP_STORED structural parts).
7. ☐ Phase 3.5: run content-integrity gate C1–C10 (C9 now checks for dangling
     references). All must PASS. Fix and re-run if any FAIL.
8. ☐ Phase 4: deepcopy integrity tree → render-source. Apply Rule 19
     (OMML→Unicode). Apply Rule 22 (stem underline → red). Apply Rule 21
     (non-ASCII → per-codepoint safe font — FIX 6).
9. ☐ Phase 5: assemble render-source docx ZIP (KEEP webSettings.xml — FIX 3; NO
     cleanup_namespaces — FIX 1). Copy to
     `/mnt/user-data/outputs/[ExamCode]_Mock[N]_Tagged.docx`.
10. ☐ Run docx gate C11–C16 on the DELIVERED render-source docx (C16 = namespace +
     reference + tag-order integrity; needs the inputs_safe/ source for C16(b)).
     Optionally validate document.xml against the OOXML wml.xsd if present. Any
     FAIL → HARD STOP, fix and re-run.
11. ☐ `present_files([output_path])`.
12. ☐ Print delivery report (§8).
13. ☐ FINAL ACCEPTANCE (mandatory, at least for the FIRST mock of each exam): open
     the delivered docx in Microsoft Word ONCE. It MUST open with NO "unreadable
     content / recover?" prompt. python-docx and LibreOffice are lenient readers that
     accept namespace-broken files Word rejects — they do NOT substitute for this check.

---

*End of Framework_MockDeliver v1.3*

*Four hard invariants: (1) never deliver a render-source docx that still
contains raw OMML — linearize ALL `<m:oMath>` via Rule 19 before assembling
the render-source ZIP; (2) every equation in the delivered docx must survive
copy-paste as proper Unicode (a³, never `a 3`) — verified by reading `<w:t>`
text from render-source document.xml; (3) every tag value must trace to a
registry + blueprint JOIN — Step 11 never infers Subject/Topic/Subtopic/
Question Type/Complexity from question content; (4) never drop or reorder the
document root's namespace declarations, and never let mc:Ignorable name a prefix
that is not declared — do NOT run etree.cleanup_namespaces() on a Word document;
validate with gate C16 and confirm in Microsoft Word itself (python-docx /
LibreOffice accept namespace-broken files that Word rejects).*

---

# APPENDIX — other Word "unreadable content" triggers (guard when editing docx)

These are the usual suspects when surgically editing a docx. Keep them in mind for any
future edit to this step:

  1. Undeclared namespace referenced by mc:Ignorable  -> FIXED (FIX 1); C16(a)/(b).
  2. Dangling relationship / content-type Override to a removed part
     -> avoided by keeping webSettings.xml (FIX 3); C9 and C16(c) guard it.
  3. Schema element-ORDER violations (pPr/rPr child order) -> FIX 2; C16(d).
  4. Duplicate wp:docPr @id values across drawings -> reassign_docpr_ids reassigns
     them uniquely after every insertion (Phase 2 and Phase 5). Keep those calls.
  5. Duplicate bookmark @id (w:bookmarkStart) -> do not clone paragraphs that
     contain bookmarks; the tag builder creates fresh paragraphs, so this is safe.
  6. Broken media relationships (r:embed / a:blip -> missing image part) -> do NOT
     renumber or drop rIds on runs that carry drawings; copy media parts through
     untouched (the spec does).
  7. mc:AlternateContent requiring a drawing namespace (Requires="wps" etc.) that
     got stripped -> avoided by NOT calling cleanup_namespaces (FIX 1).

# END OF Framework_MockDeliver v1.4
