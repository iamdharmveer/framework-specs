# Framework_PYQDeliver v1.5.1 — Universal PYQ Portal Tagger & Delivery Engine
# [ExamCode] project | PYQ-4 (PYQDeliver) | Exam-agnostic
#
# v1.5.1 — 2026-07-25 — END-OF-FILE VERSION MARKER CORRECTED. The trailing sentinel still
#   read v1.2.1, several versions behind the header, so the last line of the file
#   contradicted the first. Documentation only — not one line of behaviour changes. It went
#   unnoticed because BOTH integrity tools were structurally blind to it:
#   validate_framework_md.py Check C recognised only the '# END OF <name> vN' sentinel form
#   and skipped the comparison entirely for the '**End of <name>.md (vN)**' form used here,
#   while audit_specs_ext.py check_z_version reads the header from line 1 only. Check C now
#   recognises both forms (validate_framework_md.py v3.1), so this cannot drift silently
#   again.
# v1.5 — 2026-07-24 — TIER 1.5 (STRUCTURAL) + PER-QUESTION MARKS. Filed from the
#   IIT JAM Biotechnology 15-Feb-2026 delivery, which tagged 60 of 60 questions
#   "Easy" across a paper of 30 MCQ / 10 MSQ / 20 NAT.
#
#   MEASURED ROOT CAUSE (reproduced against the shipped engine on all 60 stems):
#   E-9's C axis scored 1 for 60/60 and its I axis 1 for 59/60. E-9's computation
#   keywords are gated to strip_mode=='quantitative' (BUG-B08) and E-10 maps every
#   science subject to 'reasoning', so the only stem-level signal that could lift a
#   science question is unreachable. Exactly ONE of the 60 stems contained any C-axis
#   keyword at all. This is not a calibration error to be tuned out: a keyword list is
#   inherently exam-SPECIFIC, and PYQ-4 serves ~200 exams. Tier 2 cannot be the answer.
#
#   THE ANSWER IS TIER 1, WHICH v1.2 ALREADY SPECIFIED (§0 item 7, §2-3a) and which
#   PYQ-1 v1.1 now supplies via its §7A assessment. PYQ-4 needs NO change to consume
#   it — that path was correct from the start and is untouched here. What v1.5 adds is
#   the FLOOR beneath it, for papers with no PYQ-1 derivation pass:
#
#   (1) TIER 1.5 — structural_difficulty (§2-3a1), a new PURE function in
#       blueprint_core.py Cluster E2. Reads the exam body's own marking_scheme:
#       question_type + position in the marks gradient. Returns None when the scheme
#       carries no structural signal (uniform marks AND one type — e.g. a 200-question
#       all-MCQ paper), so such exams fall through to Tier 2 exactly as before.
#       HONEST SCOPE: Tier 1.5 assigns one label per (marks, type) band. It reports the
#       exam body's design intent, NOT the difficulty of an individual question, and it
#       CANNOT separate a hard 2-mark MCQ from an easy one. It exists so that a paper
#       with no PYQ-1 pass is not degenerate; it is not a substitute for Tier 1.
#
#   (2) PER-QUESTION MARKS (§2-3b). v1.4 read one uniform exam_config.marks_default for
#       every question. Two independent defects: (a) marks_default is declared nowhere
#       outside this spec and no other step writes it, so the field is absent in practice
#       and the executing instance was left to improvise a value; (b) even when present,
#       a single value is wrong for any exam with a marks gradient. §2-3b now resolves
#       marks per question from exam_config.marking_scheme[] — the SAME field Tier 1.5
#       reads and the same one Steps 7/9/11 already consume — with marks_default and then
#       1 as ordered fallbacks. NOTE, recorded because it is counter-intuitive: raising
#       marks RAISES E-9's Simple threshold (simple = 4 + (marks-1)) while a science
#       stem's score does not rise with marks, so per-Q marks makes Tier 2 LESS
#       differentiating, not more. It is applied because it is CORRECT, not because it
#       helps the symptom; Tier 1/1.5 are what fix the symptom.
#
#   TIER CHAIN IS NOW 1 → 1.5 → 2 → 3. tier_counts (§2-3e) and §R3 extended to match.
#   Backward compatibility: an exam with no marking_scheme, or a uniform-marks
#   single-type scheme, skips Tier 1.5 entirely and resolves exactly as in v1.4.
#   E-9/E-10 are NOT modified — no CROSS-FILE SYNC obligation is created by v1.5.
#
# v1.4 — 2026-07-24 — PACKAGE VALIDITY GATE (C18). Preventive, adopted from
#   the PYQFormat v1.3 P0 incident. PYQ-4 has NOT produced a corrupt file;
#   this closes the blind spot that let PYQ-3 ship one silently.
#
#   What that incident established: CONTENT FIDELITY and PACKAGE VALIDITY are
#   independent properties, and every gate here verifies the first. A
#   document.xml with undeclared mc:Ignorable prefixes or misordered pPr/tcPr
#   children is still WELL-FORMED XML — it parses cleanly in lxml and stdlib
#   ElementTree alike. On the PYQ-3 artefact the text stream, all drawings and
#   every paragraph count were perfectly intact while Word refused to open the
#   file. C1 and C12 ("valid ZIP; document.xml parses") are exactly the checks
#   that gave false comfort there: parsing is not validating. §11 item 11
#   already required "opens clean in Microsoft Word with no unreadable content
#   prompt" with no machinery anywhere to verify it — C18 makes that real.
#
#   Why PYQ-4 has not hit this (recorded so the margin is not mistaken for
#   immunity): its ordering surface is tiny. make_tag_para builds exactly
#   [spacing, jc] — two elements, hardcoded in correct order, guarded by
#   C16(d). PYQ-3 inserted six pPr children plus tblPr/tcPr/tcMar plus two new
#   parts, and got five of those orders wrong. The safety here comes from a
#   small workload, not from a check — so any future widening of PYQ-4's
#   element workload removes the margin without any gate noticing. C18 is the
#   check that does not care how large the workload grows.
#
#   C18 gates BOTH artifacts (integrity and render-source) with --original, so
#   only errors NEW relative to the source block delivery. Zero, not "fewer" —
#   a rejected parent is not descended into, so nested faults stay masked until
#   the outer one is fixed (on the PYQ-3 artefact, 812 reported errors required
#   991 element reorders to clear).
#
#   SCOPE NOTE (deliberate, not an oversight): S13-3's library mandate remains
#   inherited by delegation — S13-1 states PYQ-4 reuses MockDeliver's patterns
#   identically, and MockDeliver mandates lxml explicitly. PYQ-4's own S13-3
#   text still warns against cleanup_namespaces() without naming a library.
#   C18 makes that inheritance verifiable at runtime rather than assumed, which
#   is the property that matters. Promoting the mandate into PYQ-4's own text
#   is a separate change, not made here.
#
# v1.3 — 2026-07-23 — OUT-OF-PATTERN MARKS WARNING (audit follow-up).
#   §2-3b fell back to exam_config.marks_default (or 1) for any question outside the
#   current marking_scheme, silently. For a PYQ paper from an earlier pattern that means a
#   legacy 4-mark question is delivered to students tagged 1 mark with no signal anywhere.
#   Now counts those questions and WARNs with their Q-range and the fallback value applied.
#   WARN, not HALT — publishing legacy PYQ papers is legitimate; only the silence was wrong.
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
#     D11. COMPLEXITY VIA DETERMINISTIC TIER CHAIN (v1.5, supersedes D4).
#         Per-question Complexity resolves through §2-3's FOUR tiers:
#         (1) q_to_difficulty from the progress JSON (PYQ-1 §7A assessment),
#         (1.5) structural_difficulty from exam_config.marking_scheme[],
#         (2) E-9 3-axis scoring via blueprint_core.py, (3) difficulty_default.
#         Every tier is a pure function or a pure lookup — the same document
#         always yields the same tags on every run and every model instance.
#         v1.5 CORRECTS the v1.2 rationale recorded here. That text claimed
#         Tier 2 put PYQ papers "on the SAME difficulty scale the blueprint/
#         mock pipeline is calibrated on". It does not. The mock pipeline does
#         not measure difficulty at all: Step 6 sets a difficulty_schedule
#         QUOTA, Step 7 assigns each generated question a band to fill that
#         quota exactly, and Step 11 tags by registry JOIN. E-9 is nowhere in
#         the mock tagging path, and Framework_Blueprint.md contains zero
#         references to PYQ_DIFFICULTY_CALIBRATION. The two pipelines were
#         never on one scale, so comparability was not a reason to prefer
#         Tier 2 — and Tier 2's measured behaviour on a non-aptitude exam is
#         60/60 questions at one label. Tier 1 is not an "upgrade path" for
#         unusual exams; it is the only tier that measures anything, and it is
#         the intended resolution for every exam. Tier 1.5 is the floor for
#         papers with no PYQ-1 pass. Tier 2 is retained solely because it is
#         always computable, and Tier 3 because a safety net must exist.

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
   (fallback "Medium"), `difficulty_labels` (fallback ['Easy','Medium','Hard'] —
   MockDeliver parity — when the field or the whole file is absent/unusable; WARN),
   and `sections` (each with a `q_range`, read for structural question-type resolution
   in §2-3a1; same field Step 2a writes).

   `marking_scheme[]` (v1.5) — OPTIONAL list of per-range scoring rules, each
   `{q_range:[lo,hi], question_type, correct_marks, negative_marks}`. This is the
   SAME field Step 2a writes and Steps 7/9/11 already consume; PYQ-4 does not
   introduce it and must not invent it. Used for TWO things and nothing else:
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
   (§2-3): `score_difficulty`, `determine_strip_mode`, `map_difficulty_level`
   (Cluster E, Tier 2) and `structural_difficulty` (Cluster E2, Tier 1.5 — v1.5).
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
   `score_difficulty`, `determine_strip_mode`, `map_difficulty_level`,
   `structural_difficulty`
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
| 5 | Complexity | §2-3 four-tier resolver | Tier 1 q_to_difficulty → Tier 1.5 structural_difficulty → Tier 2 E-9 scoring → Tier 3 difficulty_default (D11) |

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

## S2-3 — Complexity (difficulty) — four-tier deterministic resolver (D11, v1.5)

Complexity is resolved PER QUESTION through a deterministic tier chain.
For each question q (first tier that yields a value wins):

```text
TIER 1   — q_to_difficulty[q]           (progress JSON — PYQ-1 §7A assessment)
TIER 1.5 — structural_difficulty(q)     (exam_config.marking_scheme[] structure)
TIER 2   — E-9 score_difficulty(stem)   (blueprint_core.py — always computable)
TIER 3   — difficulty_default            (exam_config, fallback "Medium")
```

WHY THE ORDER IS THIS AND NOT ANOTHER (v1.5 — do not reorder):
  Tier 1 is the only tier that reflects what SOLVING the question required. It is
  produced by the one step that reads and solves every question (PYQ-1), so it
  differentiates two questions that sit in the same marks band and use the same
  vocabulary. Nothing below it can do that.
  Tier 1.5 reflects the exam body's design intent for a whole Q-range. It is
  uniform within a band by construction — a floor, not an assessment.
  Tier 2 reads stem keywords. Its vocabulary is aptitude-calibrated, so for exams
  outside that vocabulary it under-differentiates severely (measured: 60/60 at one
  label on IIT JAM BT). It is retained because it is always computable and because
  it is the scale Step 5's corpus statistics use — never because it is accurate.
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

### S2-3b — Tier 2: E-9 3-axis scoring (fallback path)

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
from blueprint_core import (score_difficulty, determine_strip_mode,
                            map_difficulty_level, structural_difficulty)
```

```text
strip_mode = determine_strip_mode(subject, topic, subtopic)
               with subject/topic/subtopic from q_to_classification[q]
is_msq     = (resolved Question Type for q == 'MSQ')   # §2-2, already computed
marks      = PER-QUESTION, resolved by the §0 item 2 MARKS RESOLUTION ORDER:
             (a) correct_marks of the marking_scheme entry whose q_range contains q;
             (b) else marks_default if it is a positive number;
             (c) else 1.
             (v1.5 — was a single uniform exam_config.marks_default for the whole
              paper. Never derive marks by any other route; see §0 item 2.)

           OUT-OF-PATTERN MARKS WARNING (v1.3 — MANDATORY, never silent):
           exam_config describes the CURRENT pattern. A PYQ paper from a previous era can
           carry Q-numbers beyond every configured range, and those questions may have been
           worth something quite different — a 4-mark legacy question silently delivered to
           students as 1 mark is a real scoring error, not a rounding detail.
           Before writing the tagged output, count the questions whose Q-number falls
           outside every exam_config.sections[].q_range (equivalently: those Framework_
           PYQSort v1.10 tagged with bc.OUT_OF_PATTERN). If that count is > 0, WARN:
             "N question(s) in this paper fall outside the current exam pattern's
              Q-number ranges (Q.x-Q.y). exam_config declares no marks for them, so each
              is being tagged [marks] mark(s) by fallback. If this paper is from an earlier
              pattern with different marks, correct them before publishing."
           This is a WARN, not a HALT: delivering a legacy PYQ paper is legitimate and
           common. Only the silence was wrong.
               (v1.5 SUPERSEDES the v1.2-v1.4 note that "the PYQ pipeline does not
                track per-question marks". It does: exam_config.marking_scheme[]
                carries correct_marks per q_range and Steps 7/9/11 already read it.
                The uniform value was a simplification, not a data limitation, and
                it is withdrawn. For a genuinely uniform-marks exam the resolved
                per-question value equals the old one, so nothing changes there.)
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
questions at Tier 1.5 and drops every MCQ to Tier 2. The resulting distribution is
NOT uniform, so the degenerate WARN stays quiet, and the paper ships with a
Complexity column whose values came from two different instruments: one reading
the marking structure, the other reading stem keywords. Those are not the same
scale and must not be compared as though they were.

Therefore: if Tier 2 resolved at least one question AND Tiers 1/1.5 together
resolved at least one other, WARN:

  "Complexity on this paper has MIXED PROVENANCE: N question(s) were resolved by
   tier(s) <list> and M question(s) fell to Tier 2 (E-9 keyword scoring). These
   are different instruments on different scales — a 'Medium' from the marking
   structure and an 'Easy' from stem keywords are not comparable, and the Tier-2
   questions were not measured at all unless this exam's stems use aptitude
   vocabulary. Run PYQExplain (PYQ-1) so Tier 1 resolves the whole paper on one
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
Any violation → HARD STOP (last CONTENT gate in the pipeline; C18 follows as
the package gate).

**Package validity:**

**C18** OOXML package validity on BOTH artifacts — HARD STOP.

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


def gate_c18(source_docx, integrity_docx, render_source_docx):
    """C18 — OOXML package validity on both artifacts.

    Returns 'validated' or 'degraded'; raises SystemExit on failure.

    --original is REQUIRED: it reports only errors NEW relative to the source,
    so pre-existing quirks in a given exam's PYQ-2 output (frequent across ~200
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

    failures = []
    for label, path in (('integrity', integrity_docx),
                        ('render-source', render_source_docx)):
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

**Both artifacts, not just the delivered one.** The render-source is what ships
(`_PYQ_Final.docx`) so its validity is non-negotiable. But the integrity
artifact is what C1–C10 are evaluated against — if it is structurally broken,
those ten gates are being run on a damaged document and their PASS means less
than it appears. A fault in either indicates the pipeline is wrong.

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

1. All gates (§7 C1-C18) pass, C18 (package validity) included.
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
- **§R3 — Complexity.** Tier provenance counts (Tier 1 / Tier 1.5 / Tier 2 /
  Tier 3, §2-3e) and the per-label distribution of resolved Complexity values.
  Any Tier-1 validation WARNs and any Tier-3 fallbacks listed with q number and
  reason. Both §2-3e WARNs — degenerate-distribution and mixed-provenance — are
  reported here when they fire, with the Q-numbers that fell to Tier 2.
  When Tier 1.5 resolved any question, state plainly that those values are the
  exam body's per-band design intent and are uniform within a band (§2-3a1).
  EXPECTED on a paper WITH a PYQ-1 pass: Tier 1 = Q_TOTAL, all others 0.
  EXPECTED on a paper WITHOUT one: Tier 1.5 and/or Tier 2 carry the paper, and
  the report should say so rather than presenting the column as assessed.
- **§R4 — Render transforms.** OMML linearized count, safe-font resolutions, underline recolor count.
  Any unresolved non-ASCII codepoints listed.
- **§R5 — Gate results.** C1-C18 all PASS (or list failures). Report C18
  explicitly for BOTH artifacts (integrity and render-source) — state the
  validator verdict, not merely "passed". If the validator was unavailable and
  C18 degraded to the C16(a)/(b) namespace fallback, say so here and mark
  package validity UNVERIFIED rather than PASS.
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
7a. BOTH artifacts pass C18 (package validity) against the source.
8. No residual OMML in render-source. All non-ASCII safe-fonted.
9. PYQ registry updated with this paper.
10. Delivered via present_files with the delivery report and footer.
11. Opens clean in Microsoft Word with no "unreadable content" prompt —
    machine-verified by C18 on both artifacts, not assumed. Items 1-10
    establish that the CONTENT is correct; only C18 establishes that the
    PACKAGE is valid. A file can satisfy every other item on this list and
    still fail to open.

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
- Both artifacts are schema-valid OOXML packages, proven by C18 against the
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

16. **blueprint_core.py missing or lacking Cluster E / E2 functions** → HARD STOP
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

19. **Exam whose stems are outside E-9's aptitude vocabulary** — science,
    engineering, medical, humanities, and every theory/recall paper — reaching
    Tier 2. v1.5 RECLASSIFIES this from "documented signal limit" to DEFECT
    SURFACE. Measured on IIT JAM Biotechnology 15-Feb-2026 (60 Q, 30 MCQ /
    10 MSQ / 20 NAT): E-9 scored C=1 for 60/60 and I=1 for 59/60, and the
    delivered paper carried one label for every question. Calling that a
    legitimate score was wrong — the negative-phrasing and MSQ terms do not
    rescue it, because they move a question by one point on an axis sum that
    never left its floor. Correct handling, in order:
      (a) run PYQExplain (PYQ-1) so Tier 1 supplies assessed values — this is
          the resolution, not a workaround, and it needs no PYQ-4 change;
      (b) failing that, Tier 1.5 (§2-3a1) resolves any exam whose marking_scheme
          has a marks gradient or a type mix, which covers most competitive
          exams that field MSQ/NAT alongside MCQ;
      (c) if the paper still resolves entirely on Tier 2, the §2-3e
          degenerate-distribution WARN fires and the §R3 report must state that
          per-question difficulty was not measured.
    Do NOT attempt to fix this by extending E-9's keyword sets or adding a
    strip_mode. Beyond the CROSS-FILE SYNC cost, `strip_variables` in
    Framework_MockTestAnalyse.md branches on a closed set of five modes with no
    else-branch: a sixth mode makes it a no-op passthrough, so Step 5's template
    skeletons silently become verbatim stems and its whole pattern layer
    collapses. A vocabulary list is also exam-SPECIFIC by nature and PYQ-4
    serves ~200 exams.

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
| Complexity | Per-Q from registry.difficulty | Per-Q four-tier resolver: q_to_difficulty (PYQ-1 §7A) → structural_difficulty (Cluster E2) → E-9 scoring (Cluster E) → difficulty_default (§2-3, D11) |
| Paper identity | pp.paper\_slug() via paper\_pipeline.py | Parsed from attached filename |
| Blueprint | Required | Not required (does not exist for PYQ) |
| Registry | Required | Not required (does not exist for PYQ) |
| PYQ registry | N/A | Maintained by PYQ-4 (§8) |
| Trigger | TestDeliver P[N] / MockDeliver M[N] | PYQDeliver (no arguments needed) |
| Package validity | C16(a)–(d) only | C16 **plus** C18 `gate_c18()` — full OOXML schema validation of BOTH artifacts against the source (§7, v1.4) |

`gate_c18()` is PYQ-4-specific and is NOT among the MockDeliver patterns reused
in S13-1 — MockDeliver has no equivalent. It is defined in full in §7 (C18).

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

**End of Framework_PYQDeliver.md (v1.5.1)**
