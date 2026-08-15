# Framework_PYQCore v1.4 — PYQ Analysis Shared Core (§1, S2-3, §6–§12)
# v1.4 — 2026-08-15 — GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION. §9 gains EC-P37
#   (inline channel in a batched, multi-session step — the budget is per SESSION, a
#   fresh chat resets it, halve it because an inline payload is charged twice, and
#   partition only AFTER the recency sort), EC-P38 (channel transition on resume —
#   persist and reuse the verdict, re-probe once on a first-acquisition failure, never
#   flip silently) and EC-P39 (an empty listing is a TRANSPORT diagnosis, never a
#   zero-PYQ exam — the one transport defect in the framework that produced a wrong
#   ANSWER rather than a stall). EC-P35/EC-P36 now say explicitly that their
#   single-session resolution does not apply to a batched step.
# v1.3 — 2026-08-15 — GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION. §9 gains EC-P35 (the
#   Drive channel cannot reach the container) and EC-P36 (an inline channel exceeds the
#   context budget). Neither condition is visible to size-based partitioning: measured
#   on IIT_JAM_MATHEMATICS, partition_by_transport returned auto:22 / upload:0 for a
#   corpus of which ZERO papers were actually fetchable, so plan_transport() printed
#   nothing and the operator learned the transport shape of the run AFTER the
#   acquisition loop — the exact discovery EC-P31 and S5-1 exist to prevent. MINIMUM
#   COMPANION VERSIONS now require the engines carrying stage_drive_payload(),
#   bare-base64 decode and channel-aware partitioning.
# v1.2 — 2026-08-15 — GAP-2026-08-15-BAREQ (R-3). Phase-B checklist TASK 1 no longer
#   names a local regex: Q-counting uses bc.detect_question_start(), the same detector
#   Steps 3 and 5 parse with. A checklist that tells the operator to reproduce a private
#   pattern is how a third Q-detection dialect stayed in production.
# v1.1 — 2026-08-05 — GAP-2026-08-05-001. §6 DISCRIMINATOR rewritten: "next non-empty
#   paragraph" -> "next CONTENT-BEARING BLOCK" with the four textless classes enumerated
#   (image, equation, embedded object, TABLE) plus auto-numbering; the false invariant "a
#   stem continuation NEVER is [followed by a date label]" corrected; DISCRIMINATOR 2
#   (colour, per-FILE gate) added; the NAT impossibility stated explicitly. MINIMUM
#   COMPANION VERSIONS now require the GAP-2026-08-05-001 engine and python-docx >= 1.1.0.
# v1.0.2 — 2026-07-31 — HOST-NOTE HEADER DISAMBIGUATED (sync audit, ownership check).
#   The scaffolding header '## §2-HOSTED — ...' matched the '^## §N' section-header
#   pattern, so a tool locating §2 by header could resolve to this file's host note
#   instead of Framework_PYQDraft.md, which owns §2. Renamed to 'HOSTED SECTION S2-3
#   (from §2 ...)' so §-ownership is unique per file: §2 -> Draft; hosted S2-3 content
#   here, unchanged and still byte-identical to v2.29. Scaffolding-only; zero rule change.
# v1.0.1 — 2026-07-31 — ERA-SYNC SOURCING LINE (audit_sync). The split placed S2-3's
#   prose mentions of OUT_OF_PATTERN in this file while the executable bc.OUT_OF_PATTERN
#   call sites landed in Framework_PYQScan.md; audit_sync's per-file rule (any spec naming
#   OUT_OF_PATTERN must source it from the engine) then fired on this file. Added an
#   engine-sourcing comment to the S2-3 host note — scaffolding only, the hosted v2.29
#   content remains byte-identical. Zero rule/functionality change.
# v1.0 — 2026-07-31 — SPLIT FROM Framework_PYQAnalyse v2.29 (content byte-identical).
#   Zero rule/functionality change. All §/S/EC IDs preserved verbatim. The
#   pre-split changelog (v2.0-v2.29) lives in CHANGELOG.md; the superseded
#   monolith remains as a stub section map at Framework_PYQAnalyse.md (v3.0).
## CROSS-FILE SECTION DIRECTORY — all §/S/EC IDs unchanged from Framework_PYQAnalyse v2.29
#### §1 — SESSION START → Framework_PYQCore.md
#### §2 — PHASE 0a: TAXONOMY BUILDING (PYQDraft) → Framework_PYQDraft.md
####      (S2-3 Draft taxonomy generation is HOSTED in Framework_PYQCore.md — universal
####       machinery per §11, executed by both S2-3 [PYQDraft] and S3-6 Refinement [PYQScan])
#### §3 — PHASE 0b: SMART SCAN (PYQScan) → Framework_PYQScan.md
#### §4 — PHASE 0c: ANALYSIS DOC & APPROVAL (PYQApprove) → Framework_PYQApprove.md
#### §5 — PHASE B: COUNT FILLING (PYQCount) → Framework_PYQCount.md
#### §6 — HEADING FORMAT CONTRACT → Framework_PYQCore.md
#### §7 — NAME CONSISTENCY CONTRACT → Framework_PYQCore.md
#### §8 — CLASSIFICATION RULES → Framework_PYQCore.md
#### §9 — EDGE CASES → Framework_PYQCore.md
#### §10 — DELIVERABLE SET CONTRACT → Framework_PYQCore.md
#### §11 — EXAM-AGNOSTIC GUARANTEE → Framework_PYQCore.md
#### §12 — DEFINITION OF DONE → Framework_PYQCore.md
#### Every trigger loads its step file + Framework_PYQCore.md (routes.json). History: CHANGELOG.md

---

# MINIMUM COMPANION VERSIONS (carried from Framework_PYQAnalyse v2.28 — FUNCTIONAL):
# MINIMUM COMPANION VERSIONS (v2.28):
#   corpus_io.py          >= the GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION build —
#                                     stage_drive_payload() is the verified route from
#                                     an ALREADY-MATERIALISED Drive payload to disk
#                                     with no download_fn to fabricate, and
#                                     decode_drive_payload() accepts bare base64.
#                                     Older builds raise AttributeError at the first
#                                     paper — loud, never a silent miscount.
#   blueprint_core.py     >= the GAP-2026-08-15-PYQCOUNT-DRIVE-ACQUISITION build —
#                                     partition_by_transport(..., channel=) and
#                                     INLINE_BUDGET_CHARS. Older builds raise
#                                     TypeError on the channel keyword at S5-0, before
#                                     any paper is fetched — loud, and before Task 1.
#   corpus_io.py          >= v1.4   — load_taxonomy() IS Task 2.5's loader and gate;
#                                     Cluster K write_analysis_doc() IS S4-2,
#                                     read_analysis_doc() IS Task 2.5's reader and
#                                     assert_taxonomy_lock() IS its identity gate, and
#                                     read_analysis_doc() IS Task 2.5's reader. v1.2
#                                     adds INGEST FORMS: the Analysis doc is stored in
#                                     project Files as extracted TEXT, so under v1.1
#                                     Phase B cannot read it at all (GAP-2026-07-25-003).
#   reconcile_taxonomy.py >= v1.3   — S4-0 passes final_taxonomy=, and v1.3 RECORDS it
#                                     so Steps 3-6 need no Word document at all; older
#                                     builds accept
#                                     no such argument and raise TypeError.
#   blueprint_core.py     — MAX_HEADING_LEN for the S4-0 name gate; and the
#                           GAP-2026-07-26-001 build carrying next_nonempty_texts()
#                           and is_taxonomy_heading(para, is_option, next_text).
#                           S5-2 PASSES next_text; on an older engine that raises
#                           TypeError rather than silently miscounting.
#                           GAP-2026-08-05-001 build REQUIRED, carrying
#                           paragraph_is_content_bearing(), CONTENT_SENTINEL,
#                           VISUAL_CONTENT_TAGS, sorted_body_lookahead(),
#                           HEADING_NAVY, first_run_colour() and
#                           heading_colour_available(). A walker calling
#                           sorted_body_lookahead() against an older engine raises
#                           AttributeError at the FIRST paper — loud, never a silent
#                           miscount. A NEW engine under an OLD walker still gets the
#                           textless-content fix (it is inside next_nonempty_texts)
#                           but not the table fix: strictly better, never worse.
#   python-docx           >= 1.1.0 — Paragraph.text includes hyperlink run text only
#                                    from 1.1.0. On 0.8.x a hyperlink-only paragraph
#                                    reports no text and carries none of the
#                                    VISUAL_CONTENT_TAGS, so it is read as an empty
#                                    spacer — a latent instance of the same
#                                    "textless is not empty" class.

---

## §1 — SESSION START

### S1-1 — Trigger parsing

```
Trigger formats:
  Step 2a: PYQDraft [ExamCode]
  Step 2b: PYQScan
  Step 2b: PYQScan PYQ: <<Drive link>>
  Step 2c: PYQApprove
  Step 4:  PYQCount PYQ: <<Drive link>>

Trigger matching is case-insensitive.

Parse:
  PYQDraft → Step 2a (--taxonomy mode)
    ExamCode : alphanumeric + underscore only.
               Invalid chars → flag and ask to correct.
               Saved in exam_config.json for all future steps.
  PYQScan  → Step 2b (--scan mode)
    ExamCode : read from exam_config.json in project knowledge.
               If exam_config not found → "Run PYQDraft [ExamCode] first."
    PYQ:     : Google Drive folder link (REQUIRED — v2.16, standardized with Step 4)
               Extract folder ID: r'drive\.google\.com/drive/folders/([A-Za-z0-9_-]+)'
               If absent → HARD STOP: "PYQScan requires PYQ: <<Google Drive folder
               link>>. Row files must be in Google Drive — the local upload fallback
               was removed (v2.16) to match Step 4 (PYQCount)."
  PYQApprove → Step 2c (--approve mode)
    ExamCode : read from exam_config.json.
  PYQCount → Step 4 (--counts mode)
    ExamCode : read from exam_config.json.
    PYQ:     : Google Drive folder link (required)
               Extract folder ID: r'drive\.google\.com/drive/folders/([A-Za-z0-9_-]+)'

Mode validation:
  PYQDraft   → requires: Exam Syllabus + Exam Pattern in uploads or chat
  PYQScan    → requires: PYQ: Drive link to Row files + taxonomy_draft.json in project
  PYQApprove → requires: scan_progress.json in project or uploads
  PYQCount   → requires: PYQ: Drive link to sorted PYQ folder
```

### S1-2 — File inventory

```
List ALL received files immediately after trigger.

For --taxonomy mode:
  ✓ Exam Syllabus  : image (JPG/PNG), PDF, .docx, or plain text in chat
  ✓ Exam Pattern   : .xlsx (PREFERRED) or image/PDF/.docx/plain text (legacy)
      XLSX detection: file extension is .xlsx AND contains sheets
      named "Overview", "Sections", "Range" → use xlsx parser (S2-2a).
      Any other format → use legacy AI extraction (S2-2b).
  If either missing → ask user to provide.

For --scan mode:
  ✓ Row files (.docx) : from PYQ: Drive link (REQUIRED — v2.16, no local fallback)
  ✓ taxonomy_draft.json : from project knowledge or uploads
  Use Google Drive MCP to list files recursively.
  If PYQ: absent → HARD STOP: "PYQScan requires PYQ: <<Google Drive folder link>>.
  Row files must be in Google Drive — the local upload fallback was removed (v2.16)
  to match Step 4 (PYQCount)."
  If taxonomy_draft.json missing → "Run --taxonomy mode first."

For --approve mode:
  ✓ scan_progress.json : from project knowledge or uploads
  If missing → "Run --scan mode first until convergence or full coverage."

For --counts mode:
  ✓ Drive folder with sorted PYQ files
  ✓ Approved Analysis doc in project knowledge (to update with counts)
  If Analysis doc missing → "Run --approve mode first."
```

---


---

## HOSTED SECTION S2-3 (from §2 — Draft taxonomy generation) — hosted here per §11
# Executed by PYQDraft (Step 2a) as part of §2, AND by PYQScan S3-6 Refinement
# (Domain Check, per-entry decision tree, 6 Pattern Dimensions Appendix).
# ID, content and internal numbering unchanged from Framework_PYQAnalyse v2.29 §2.
# ENGINE SOURCING: the OUT_OF_PATTERN sentinel named in this hosted section IS the
# engine literal bc.OUT_OF_PATTERN (blueprint_core Cluster F — PATTERN ERA; same
# constant as Framework_PYQSort v1.9 S2-2). Executable call sites live in
# Framework_PYQScan.md S3-2a/S3-3b (RULE 4 OUT-OF-RANGE branch).

### S2-3 — Draft taxonomy generation

```
═══════════════════════════════════════════════════════════════════════
TAXONOMY CORE PRINCIPLE — THE UNIQUE DOMAIN PROPERTY:

  Every subtopic must UNIQUELY CLAIM a set of concepts that no other
  subtopic also claims. Given any PYQ question from this exam, EXACTLY
  ONE subtopic must be the unambiguous best match.

  When this holds  → classification is unambiguous → 100% question mapping.
  When this breaks → classification is ambiguous → questions vanish.

  DEFAULT BIAS: MERGE over SPLIT. An over-merged taxonomy loses some
  granularity but classifies 100% of questions. An over-split taxonomy
  creates near-duplicate bins that confuse the classifier and cause
  questions to disappear from the output entirely.

  CRITICAL SCOPE OF MERGE BIAS:
    The merge-over-split bias applies ONLY to AI-INVENTED subtopics —
    splits that Claude proposes from domain knowledge beyond what the
    syllabus explicitly states. It does NOT apply to items the syllabus
    itself explicitly enumerates. If the syllabus lists "Triangles,
    Circles, Polygons" under Geometry, those are syllabus-given items
    and MUST become subtopics regardless of the merge bias. Suppressing
    syllabus-enumerated items is data loss, not conservative merging.

  EVIDENCE: MPPSC Botany — 81 syllabus entries faithfully used as
  subtopics → 150/150 Qs mapped (100%). Same exam with 336 AI-generated
  micro-subtopics → 93/150 Qs mapped (62%). The 4.1× inflation created
  75 near-duplicate subtopic pairs that broke classification.

  COUNTER-EVIDENCE: SSC CGL Tier 1 — framework produced 68 subtopics
  from a syllabus that explicitly lists ~100 items. The 1:1 Topic=Subtopic
  mapping (e.g., "Geometry" → 1 subtopic "Geometry" despite syllabus
  listing Triangles + Circles + Polygons) lost syllabus-given items.
  The merge bias must never suppress what the syllabus explicitly names.
═══════════════════════════════════════════════════════════════════════

For each subject in the syllabus:

  ─── STEP 1: TOPIC DERIVATION (unchanged from v1.5) ───

  Each INDIVIDUALLY LISTED syllabus item that represents a DISTINCT
  QUESTION TYPE = one Topic.

  DO NOT merge syllabus items into super-categories like "Vocabulary",
  "Grammar", "Non-Verbal Reasoning". Those are SUBJECT-level or
  SECTION-level labels, NOT Topic-level labels.

  TOPIC INTEGRITY TEST — apply these 3 questions to every proposed Topic:
    Q1. Would a coaching institute teach this as a SEPARATE chapter?
    Q2. Would a student study for this INDEPENDENTLY of other Topics?
    Q3. Does the exam present this as a DISTINCT question type with its
        own recognisable format?
    If ANY answer is YES for a syllabus item → it is its OWN Topic.

  MERGE ONLY when two syllabus items are genuinely synonymous — i.e., they
  describe the SAME question type with different words.

  GROUPING is allowed ONLY for syllabus items that are sub-operations of
  a single concept where the exam never tests them independently:
    Example: "Percentage, Ratio, Average, Interest, P&L, Discount,
             Partnership, Mixture, SDT, Time & Work, Pipes & Cisterns"
             → Topic "Arithmetic" with each item as a subtopic.
    Example: "Triangle centres, Congruence, Similarity, Circles,
             Quadrilaterals" → Topic "Geometry" with each item as a subtopic.
    Counter-example: "Spot the Error" and "Sentence Improvement" must be
             SEPARATE Topics — distinct question types.

  ═══════════════════════════════════════════════════════════════════
  GROUPED ITEMS ARE SUBTOPICS (MANDATORY):

    When multiple syllabus items are GROUPED into one Topic, EVERY
    grouped item MUST become a named Subtopic under that Topic. The
    Topic name is the umbrella label; the individual items are the
    subtopics. A grouped Topic with only 1 subtopic (same name as
    the Topic) is ALWAYS WRONG — it means the grouped items were lost.

    EXAMPLE — Geometry:
      Syllabus says: "Triangle and its various kinds of centres,
      Congruence and similarity of triangles, Circle and its chords,
      tangents, Regular Polygons"
      ✗ WRONG: Topic "Geometry" → 1 subtopic "Geometry"
      ✓ RIGHT: Topic "Geometry" → subtopics:
          "Triangles — Centres, Congruence, Similarity"
          "Circles — Chords, Tangents, Common Tangents"
          "Regular Polygons"

    EXAMPLE — Trigonometry:
      Syllabus says: "Trigonometric ratio, Degree and Radian Measures,
      Standard Identities, Complementary angles, Heights and Distances"
      ✗ WRONG: Topic "Trigonometry" → 1 subtopic "Trigonometry"
      ✓ RIGHT: Topic "Trigonometry" → subtopics:
          "Trigonometric Ratios & Standard Identities"
          "Heights & Distances"
      (Heights & Distances is a different question type — applied word
      problems vs algebraic simplification. Different solving approach,
      separate textbook chapter, unambiguous classification.)

    EXAMPLE — Polity (GK):
      Syllabus says: "Constitution, Parliament, Judiciary, Executive,
      Fundamental Rights, Elections, etc."
      ✗ WRONG: Topic "Polity" → 1 subtopic "Indian Polity & Governance"
      ✓ RIGHT: Topic "Polity" → subtopics per distinct area

    SELF-CHECK — 1:1 TOPIC=SUBTOPIC DETECTOR:
      After completing subtopic derivation, scan for any Topic where:
        (a) the Topic has exactly 1 subtopic, AND
        (b) the subtopic name is identical or near-identical to the Topic name
      For each match: check if the syllabus listed multiple items under
      that heading. If YES → the items were silently dropped. Re-derive.
      A 1:1 mapping is valid ONLY when the syllabus genuinely lists that
      item as a single atomic concept with no sub-items (e.g., "Venn
      Diagrams" — one concept, one subtopic, no sub-items in syllabus).
  ═══════════════════════════════════════════════════════════════════

  PROOF OF CORRECT TOPIC COUNT (self-check):
    After Topic derivation, count the Topics per section.
    If a section has ≤ 4 Topics but the syllabus listed 10+ items → Topics
    are over-aggregated. Re-derive. The syllabus items ARE the Topics.

  ═══════════════════════════════════════════════════════════════════
  CATCH-ALL / RESIDUAL TOPIC PROHIBITION (MANDATORY):

    Claude MUST NEVER create a Topic or Subtopic named "Other",
    "Other Sub-topics", "Others", "Miscellaneous", "General",
    "Additional Topics", "Remaining Topics", or ANY label that serves
    as a catch-all / residual bin for items that "didn't fit elsewhere".

    EVERY syllabus item that passes the Topic Integrity Test (Q1/Q2/Q3
    = ANY YES) MUST become its own Topic. Items must NOT be grouped
    into a residual bucket.

    FAILURE EXAMPLE (SSC CGL Tier 2 Reasoning):
      ✗ "Topic 17: Other Sub-topics" containing Blood Relations,
        Seating Arrangement, Syllogism, Dice and Cubes, Ranking and
        Ordering, Logical Sequence.
      Each of these is a distinct question type taught as a separate
      chapter by every coaching institute. They MUST be separate Topics:
        ✓ Topic 17: Blood Relations
        ✓ Topic 18: Logical Sequence
        ✓ Topic 19: Seating Arrangement
        ✓ Topic 20: Dice and Cubes
        ✓ Topic 21: Ranking and Ordering
        ✓ Topic 22: Syllogism

    ROOT CAUSE: Claude runs out of patience while processing a long
    syllabus and dumps remaining items into a residual bin. The
    prohibition is unconditional — if a Topic name matches ANY of the
    banned patterns, it is a spec violation and must be re-derived.

    BANNED PATTERNS (case-insensitive, substring match):
      "other", "miscellaneous", "misc", "remaining", "additional",
      "general topics", "catch-all", "residual"

    SELF-CHECK: after completing Topic derivation for a section,
    scan all Topic names against the banned patterns. If ANY match
    → HARD STOP. Re-derive those items as individual Topics.
  ═══════════════════════════════════════════════════════════════════

  ═══════════════════════════════════════════════════════════════════
  NAME-SHAPE VALIDATION (v2.12 — D6-1/D6-2: reject question-strings; canonicalise)

    D6-1 — A raw PYQ QUESTION captured as a subtopic (an extraction defect) must
    NEVER enter the taxonomy. In the SSC CGL run a manifest contained a subtopic
    literally named "What is the average number of pages printed by printer Z during
    the 3 days?" — it was PYQ-based, so Step 6 ALLOCATED it and Step 7 was asked to
    "generate questions for" a question. This gate stops that at the source.

    HARD STOP if any Topic/Subtopic name is QUESTION-SHAPED: ends with '?', is
    > 80 chars, or begins with an interrogative (what / which / how many / …).
    WARN (review, not block) on softer signals (stem phrasing, > 12 words). The gate
    is HIGH-PRECISION — real syllabus labels ("Time, Speed and Distance", "Direct and
    Indirect Speech", "Assertion and Reason") never trip it (verified against 31 real
    labels + 4 question-strings, 0 false positives).

    D6-2 — CANONICALISE names before COMPARING / COUNTING with canon_name(): NFC
    (Unicode), dash variants (– — ‐ − → -), doubled / non-breaking whitespace, and
    case are folded, so trivial drift never splits one subtopic into a phantom pair.
    Display keeps the ORIGINAL name; only comparison/counting uses canon_name().
    This complements the Task 2.5 phantom-triple check (which DETECTS drift) by
    PREVENTING it at the point counts are aggregated.

```python
# Steps 1-3 name-quality gates (v-bump). Pure, deterministic, high-precision.
import re, unicodedata

def canon_name(s):
    """D6-2/D5-6: canonical form for COMPARING/COUNTING subtopic names so trivial drift
    (NFC/NFD, dash variants, doubled/〈nbsp〉whitespace, trailing spaces, case) never splits
    one subtopic into a phantom pair. NOT for display — display keeps the original."""
    s = unicodedata.normalize('NFC', s or '')
    s = s.replace(' ', ' ')                       # nbsp -> space
    for d in ('‐','‑','‒','–','—','−'):  # hyphen/dash variants
        s = s.replace(d, '-')
    s = re.sub(r'\s+', ' ', s).strip()
    return s.casefold()

_INTERROGATIVE = re.compile(
    r'^\s*(what|which|who|whom|whose|when|where|why|how\s+many|how\s+much|how\s+long|how\b)\b',
    re.I)
# stem phrases that only appear inside a question, never in a taxonomy label
_STEM_PHRASE = re.compile(
    r'\b(the average (number|value|of)|the value of x\b|is equal to\b|how many|of the following (is|are)\b'
    r'|printed by|find the value)\b', re.I)

def question_shape_verdict(name):
    """D6-1: is this 'subtopic' actually a raw question string? Returns (verdict, reason).
    verdict ∈ {'OK','HARD','WARN'}. HIGH-PRECISION: HARD only on signals a real syllabus
    label never has, so legitimate names are never blocked."""
    n = (name or '').strip()
    if not n:
        return ('HARD', 'empty name')
    if n.endswith('?'):
        return ('HARD', "ends with '?' — a question stem, not a label")
    if len(n) > 80:
        return ('HARD', f'{len(n)} chars — far longer than any taxonomy label')
    if _INTERROGATIVE.match(n):
        return ('HARD', 'begins with an interrogative — a question stem')
    if _STEM_PHRASE.search(n) and len(n.split()) >= 6:
        return ('WARN', 'contains question-stem phrasing; review that this is a label')
    if len(n.split()) > 12:
        return ('WARN', f'{len(n.split())} words — unusually long for a label; review')
    return ('OK', '')
```

    SELF-CHECK (runs after subtopic derivation, before S-QV / DoD):
      for name in all Topic names + all Subtopic names:
          verdict, reason = question_shape_verdict(name)
          if verdict == 'HARD':
              HARD STOP: f"Name-shape violation: '{name[:60]}' — {reason}. "
                         f"Re-extract this item as a proper taxonomy label, not a question."
          elif verdict == 'WARN':
              review_list.append((name, reason))     # surfaced at S-QV, non-blocking
      # counting/comparison of subtopic triples uses canon_name() on each of
      # (section, topic, subtopic) so NFC/dash/whitespace/case drift cannot phantom-split.
  ═══════════════════════════════════════════════════════════════════

  ─── STEP 2: SUBTOPIC DERIVATION (PER-ENTRY DECISION TREE) ───

  ═══════════════════════════════════════════════════════════════════
  EXCLUSION RULES — apply BEFORE the decision tree:

    ✗ VOCABULARY / GLOSSARY LISTS: Individual terms, named reactions,
      specific organisms, historical terms, concept glossaries
      (e.g., UGC NET History's 80+ terms like "Iqta, Jaziya, Mansab")
      → these define content SCOPE, not taxonomy structure.
      They are CONTENT WITHIN a subtopic, not subtopics themselves.

    ✗ ENUMERATED SCOPE ITEMS within a colon-descriptor:
      (e.g., "mitochondria, lysosomes, peroxisomes" within
      "Structural organization of intracellular organelles:")
      → these are scope markers listing what CAN be tested,
      not separate subtopics. All items share the same question
      type (factual recall of organelle biology).

    ✗ FORMAT QUALIFIERS (TEXT/FIGURAL/PASSAGE/DI):
      → tracked separately in the Format column. NOT taxonomy.

    ✗ CATCH-ALL / RESIDUAL SUBTOPICS:
      → Same prohibition as Topics (see above). Claude MUST NEVER create
      a Subtopic named "Other", "Others", "Miscellaneous", "General",
      or any residual bin. Every distinct concept = its own named Subtopic.
  ═══════════════════════════════════════════════════════════════════

  For each syllabus entry within a Topic, apply this decision tree:

  ┌─────────────────────────────────────────────────────────────┐
  │ Q1: Does this entry have an EXPLICIT IDENTIFIER?            │
  │     (Letter: A/B/C, Number: 1/2/3, bullet with titled      │
  │      header followed by colon + descriptor, or textbook     │
  │      chapter number)                                        │
  │                                                             │
  │   YES → This entry IS a subtopic candidate. Go to Q2.      │
  │                                                             │
  │   NO  → This is an UNDIVIDED BLOCK (paragraph without       │
  │          internal structure, e.g., GATE CS "Section 5:       │
  │          Algorithms" or IIT JAM "Section 2: Mechanics").    │
  │          → Apply DOMAIN KNOWLEDGE to identify 2–5 natural   │
  │            sub-domains within it (e.g., "Theory of           │
  │            Computation" → Regular Languages & FA, CFG & PDA, │
  │            Turing Machines & Undecidability).                │
  │          → Each proposed sub-domain MUST pass Q3.           │
  │          → If no natural sub-domains exist → the entire     │
  │            block = ONE subtopic.                             │
  │          → The 6 PATTERN DIMENSIONS (Format, Direction,     │
  │            Task, Content, Structural, Medium — see Appendix)│
  │            MAY be used as a tool for identifying sub-domains│
  │            in undivided blocks. They are NOT mandatory for  │
  │            entries that already have explicit identifiers.   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │ Q2: Does this entry contain INTERNAL SUB-STRUCTURE?         │
  │                                                             │
  │     Internal sub-structure means ANY of:                    │
  │     • Internal headers with colons (e.g., "Wave optics:     │
  │       wavefront and Huygens' principle" within a larger     │
  │       "Optics" unit)                                        │
  │     • Paragraph breaks with new titled sections             │
  │     • Nested bullets listing distinct domains               │
  │     • An UMBRELLA LABEL covering 2+ genuinely different     │
  │       academic sub-fields (e.g., "Algebra" covering both    │
  │       Abstract Algebra AND Linear Algebra — different       │
  │       university courses taught in different semesters)     │
  │                                                             │
  │   NO  → This entry = ONE subtopic. Use VERBATIM syllabus   │
  │          text (title portion before the colon). DONE.       │
  │          Example: "7K. Recombination: Homologous and        │
  │          non-homologous recombination including              │
  │          transposition" → subtopic "Recombination"          │
  │                                                             │
  │   YES → Each internal sub-section = potential subtopic.     │
  │          Go to Q3 for each proposed split.                  │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │ Q3: UNIQUE DOMAIN CHECK (for each proposed split):          │
  │                                                             │
  │   ALL THREE must be TRUE to justify the split:              │
  │                                                             │
  │   (a) DIFFERENT SOLVING APPROACH:                           │
  │       Would a student use a fundamentally different         │
  │       method/strategy for this vs the other split?          │
  │       "Group Theory" vs "Linear Algebra" → YES (different   │
  │        math). "Lysosomes" vs "Peroxisomes" → NO (same      │
  │        memorization approach for both).                     │
  │                                                             │
  │   (b) SEPARATE STUDY UNIT:                                  │
  │       Would a coaching institute or textbook teach this     │
  │       as a SEPARATE chapter or practice set?                │
  │       "Regular Languages" vs "Turing Machines" → YES.       │
  │       "Nitrate Assimilation" vs "Ammonium Assimilation" → NO│
  │       (same chapter: Nitrogen Metabolism).                  │
  │                                                             │
  │   (c) UNAMBIGUOUS CLASSIFICATION:                           │
  │       Given any question about concept X, could it ONLY     │
  │       belong to THIS split and not the other?               │
  │       If a question could plausibly go either way → the     │
  │       split creates classification ambiguity → DON'T SPLIT. │
  │       "BFS on adjacency list" → could be "Graph Algorithms" │
  │       OR "Graph Data Structures" → ambiguous → DON'T create │
  │       both as separate subtopics.                           │
  │                                                             │
  │   ALL THREE TRUE → Create the split.                        │
  │   ANY FALSE      → Keep the entry as ONE subtopic.          │
  └─────────────────────────────────────────────────────────────┘

  WORKED EXAMPLES ACROSS EXAM TYPES:

    SSC CGL T1 Reasoning: "Semantic Analogy, Figural Classification,
    Coding & Decoding, Venn Diagrams, Number Series..."
    → Each comma-separated label is a short label with implicit
      identifier. Q1=YES. Q2: each is already atomic (no internal
      sub-structure). → Each label = one subtopic. No splitting needed.
    → For Topics like "Analogy" grouped from multiple labels:
      "Semantic Analogy" + "Number Analogy" + "Figural Analogy"
      each becomes a subtopic under Topic "Analogy".

    MPPSC Botany: "2B. Structural organization of intracellular
    organelles: Cell wall, nucleus, mitochondria, Golgi bodies,
    lysosomes, ER, peroxisomes, plastids, vacuoles, chloroplast..."
    → Q1=YES (letter ID "2B"). Q2: the enumerated items (mitochondria,
      lysosomes...) are SCOPE MARKERS, not internal sub-structure.
      No internal headers, no paragraph breaks with new titles.
      Q2=NO. → ONE subtopic: "Structural organization of intracellular
      organelles." DONE.

    GATE CS: "Section 6: Theory of Computation — Regular expressions
    and finite automata. Context-free grammars and push-down automata.
    Regular and context-free languages, pumping lemma. Turing machines
    and undecidability."
    → Q1=NO (undivided block, no letter IDs within). Apply domain
      knowledge: 3 natural sub-domains (Regular/FA, CFG/PDA, TM).
      Q3 check for each: (a) Different approaches? YES — DFA
      minimization ≠ PDA stack operations ≠ TM halting proofs.
      (b) Separate textbook chapters? YES. (c) Unambiguous
      classification? YES — "pumping lemma for CFL" can ONLY be
      CFG/PDA. → Split into 3 subtopics. ✓

    CUET PG Math: "Algebra: Groups, subgroups, Abelian groups, cyclic
    groups, permutation groups; Normal subgroups, Lagrange's Theorem;
    Rings, Subrings, Ideal, Prime ideal; Maximal ideals; Fields;
    Vector spaces, Linear dependence, basis, dimension, linear
    transformations, matrix representation, eigenvalues..."
    → Q1=YES (header "Algebra" with colon). Q2: Does it contain
      internal sub-structure? YES — "Algebra" is an UMBRELLA LABEL
      covering Abstract Algebra (Groups/Rings/Fields) AND Linear
      Algebra (vector spaces/eigenvalues) — different university
      courses. Q3: (a) Different approaches? YES. (b) Separate
      chapters? YES. (c) Unambiguous? YES — "find eigenvalues" is
      always Linear Algebra, "prove Lagrange's Theorem" is always
      Abstract Algebra. → Split into 2 subtopics. ✓

    NEET Biology Unit 7: "Genetics and Evolution" with bullets:
    "• Heredity and variation: Mendelian Inheritance..."
    "• Molecular basis of Inheritance: DNA structure, RNA..."
    "• Evolution: Origin of life, Darwin's contribution..."
    → Q1=YES (bullets with titled headers). Q2: each bullet has a
      distinct titled header → YES, internal sub-structure. Q3 for
      each: Mendelian genetics ≠ molecular biology ≠ evolution —
      all three pass. → 3 subtopics under this Topic. ✓

    CTET Math Content: "• Geometry • Numbers • Addition and Subtraction
    • Multiplication • Division • Measurement • Weight • Time..."
    → Q1=YES (bullet labels). Q2: each is a short label (≤3 words)
      = atomic. No internal sub-structure. → Each bullet = one
      subtopic. 12 subtopics total. ✓

    UGC NET History Unit I: "Negotiating the Sources: Archaeological
    sources: Exploration, Excavation..." + "Indus/Harappa Civilization:
    Origin, extent, major sites..." + "Vedic and later Vedic periods..."
    → Q1=YES (named paragraphs with colon-titles within the unit).
      Each named paragraph = one subtopic. The separate "Concepts,
      Ideas and Terms" list (80+ items) → EXCLUDED by vocabulary
      exclusion rule. → ~5 subtopics for Unit I. ✓

  WHEN SYLLABUS ASSIGNS QUESTION COUNTS:
    If the syllabus itself assigns explicit question counts to a
    level (e.g., CTET: "a) Child Development — 15 Questions"),
    that level IS a meaningful taxonomy boundary. Do not split
    below it UNLESS internal items are clearly distinct question
    types (as with CTET Math Content's 12 labels under "15 Qs").

  ─── STEP 3: RECORD TAXONOMY ───

  taxonomy = {
    section_name: {
      topic_name: [subtopic_1, subtopic_2, ...],
      ...
    },
    ...
  }

  QUALITY GATE — RATIO-BASED GUARDRAIL (before saving):
    Count:
      total_subtopics = sum of all subtopics across all sections
      total_syllabus_entries = count of explicitly identified entries
        in the original syllabus (letters, numbers, bullets, named
        paragraphs — NOT individual enumerated scope items)
      ratio = total_subtopics / total_syllabus_entries

    Guardrails:
      ratio ≤ 2.0  → PASS. Proceed normally.
      2.0 < ratio ≤ 3.0 → FLAG. Print warning:
        "Taxonomy inflation ratio = [X]×. Review all splits for
         Unique Domain Property compliance. Proceed only if each
         split passes Q3 (Unique Domain Check)."
      ratio > 3.0  → HARD STOP. Print:
        "Taxonomy inflation ratio = [X]× exceeds 3.0× guardrail.
         Over-fragmentation will cause classification failures.
         Re-derive taxonomy with fewer splits."

    NEAR-DUPLICATE CHECK (mandatory):
      For every pair of subtopics (S_i, S_j) within the same Topic:
        If name similarity > 75% (by SequenceMatcher or equivalent):
          FLAG: "Subtopics '[S_i]' and '[S_j]' have >75% name similarity.
                 Merge or rename to disambiguate."
      Fix ALL flagged pairs before proceeding.

    COVERAGE CHECK (mandatory):
      Every concept explicitly named in the syllabus must map to
      EXACTLY ONE subtopic. No orphaned concepts (mentioned in syllabus
      but not covered by any subtopic). No duplicated concepts (claimed
      by 2+ subtopics).

    CATCH-ALL NAME CHECK (mandatory):
      Scan ALL Topic and Subtopic names against the banned patterns
      from the CATCH-ALL PROHIBITION rule (above). If ANY match →
      HARD STOP. Re-derive those items as individual named Topics/Subtopics.
      This check runs AFTER all other quality gates.

  ─── APPENDIX: 6 PATTERN DIMENSIONS (optional tool) ───

  The 6 pattern dimensions below are an OPTIONAL analytical tool for
  identifying sub-domains within UNDIVIDED BLOCK entries (Q1=NO path).
  They are NOT mandatory for entries with explicit identifiers.

  They remain useful for aptitude/reasoning exams (SSC, CAT, CTET)
  where a single Topic like "Series" genuinely produces distinct
  question types along format/medium dimensions.

  DIMENSION 1 — FORMAT VARIANT:
    Standalone vs In-context. Single-word vs Phrase vs Passage-embedded.
  DIMENSION 2 — DIRECTION VARIANT:
    A→B or B→A (Active→Passive, Direct→Indirect, Encode→Decode).
  DIMENSION 3 — TASK VARIANT:
    Identify error vs Correct vs Select vs Fill vs Find next vs Find wrong.
  DIMENSION 4 — CONTENT/THEMATIC DOMAIN:
    Same format but different knowledge areas tested.
  DIMENSION 5 — STRUCTURAL VARIANT:
    Single-statement vs Multi-statement. 2-pair vs Matrix. Individual vs Set-based.
  DIMENSION 6 — MEDIUM VARIANT:
    Text-based vs Figure/Image-based vs Mixed.

  WHEN USING DIMENSIONS: every proposed subtopic from dimensional
  analysis MUST pass Q3 (Unique Domain Check) before being accepted.
  If Q3(c) fails (ambiguous classification between two proposed
  subtopics) → merge them into one subtopic.
```



---

## §6 — HEADING FORMAT CONTRACT

```
═══════════════════════════════════════════════════════════════════════
HEADING FORMAT CONTRACT — PYQSort ↔ Step 5 (PYQExtract) E-1 PARSER
═══════════════════════════════════════════════════════════════════════

PYQSort produces sorted PYQ files with headings in THIS EXACT format.
Step 5's parse_taxonomy_level() parses THIS EXACT format.
Phase B's count parser uses THIS EXACT format.

ANY deviation breaks the entire downstream pipeline.

LEVEL 1 (Subject — the taxonomy top-level, from syllabus):
  Text format: "Subject: <Subject Name>"
  Example:     "Subject: General Intelligence & Reasoning"
  Styling:     14pt, Bold, Navy #003366
  Parser:      re.match(r'Subject:|Domain:', text) → level 1
               content = text.split(':', 1)[1].strip()
  Result:      "General Intelligence & Reasoning"

LEVEL 2 (Topic):
  Text format: "Topic <N>: <Topic Name>"
  Example:     "Topic 1: Analogy"
  Styling:     12pt, Bold, Black #000000
  Parser:      re.match(r'Topic\s+\d+:', text) → level 2
               content = re.sub(r'Topic\s+\d+:\s*', '', text).strip()
  Result:      "Analogy"

LEVEL 3 (Subtopic):
  Text format: "<Subtopic Name>"  (no prefix — just the name)
  Example:     "Mixed Number-Letter Analogy"
  Styling:     11pt, Bold, Navy #003366
  Parser:      default → level 3, content = text.strip()
  Result:      "Mixed Number-Letter Analogy"

DATE LABEL:
  Text format: "[DD-Mon-YYYY Shift X]"
  Example:     "[12-Sep-2025 Shift 1]"
  Styling:     11pt, Bold, Navy #003366, Right-aligned
  NOT a heading → skipped by is_taxonomy_heading() via shift-tag detection

QUESTION (first paragraph):
  Text format: "Q.<N>  <stem text>"
  NOT a heading → skipped by is_taxonomy_heading() via Q-pattern detection

QUESTION (second and subsequent paragraphs — STEM CONTINUATION):
  GAP-2026-07-26-001. This entry did not exist, and its absence WAS the defect.
  §6 described a question as a SINGLE paragraph while PYQSort EC-S8 explicitly emits
  multi-paragraph stems — two specs in one repository disagreeing about whether a
  question can span paragraphs. Everything downstream inherited the wrong one.

  Text format: free text — a Statement I/II block, a line following a figure, scheme
               or table, a NAT ask-line, or a bare option label ("1.") whose content
               is an image. PYQSort EC-S8 emits these BOLD, by design.
  Detection (EC-S8): bold + not-date + not-option + not-next-Q.
  WARNING: that is CHARACTER FOR CHARACTER the level-3 heading predicate. A stem
    continuation is therefore INDISTINGUISHABLE from a subtopic heading on styling
    alone. Bold is not an identity; it is a style attribute shared by both classes.

  DISCRIMINATOR 1 — POSITIONAL (the FALLBACK; it is NOT the only one the document
  carries — see DISCRIMINATOR 2):
    A genuine BARE (level-3) heading is ALWAYS followed, as the next CONTENT-BEARING
    BLOCK, by a DATE LABEL. A stem continuation is never followed by a date label as
    the next content-bearing block — the options, figures, equations or tables that
    belong to its own question always intervene.
    "CONTENT-BEARING BLOCK" IS THE LOAD-BEARING PHRASE (GAP-2026-08-05-001). It was
    written as "next non-empty paragraph", and the engine implemented exactly that:
    the next paragraph with TEXT. Four classes of block carry content but no text —
      (1) image-only paragraphs   <w:drawing> / <w:pict> / <v:imagedata>
      (2) equation-only paragraphs <m:oMath> / <m:oMathPara>
      (3) embedded objects        <w:object>  (Equation Editor 3.0)
      (4) TABLES <w:tbl> — which are not paragraphs at all and never appear in
          doc.paragraphs, so NO paragraph-scoped rule can ever see one
    plus auto-numbered paragraphs whose visible "1." is rendered by Word and stored
    nowhere in the XML. When every block between a continuation and the next date
    label is of those classes, the continuation satisfies this test and becomes a
    phantom subtopic. Use bc.sorted_body_lookahead(doc), never doc.paragraphs +
    bc.next_nonempty_texts(), in any sorted-PYQ walker.
    A WARNING TO THE NEXT IMPLEMENTER: in a printed copy, a PDF export or a
    screenshot, those four textless option labels look identical to text ones. The
    difference is visible only in the XML. Do not diagnose this class from an image.
    EXPOSURE IS DECIDED BY STEP 1's RENDERING, so two papers of the SAME exam can
    differ: a multi-line stem emitted as one paragraph with <w:br> line breaks
    produces no continuation candidate at all, while the same stem split into
    separate paragraphs produces one per break. Likewise an option labelled with a
    literal "1." text run is safe where the same option auto-numbered is not. A
    corpus that looks clean today is one rendering change from exposed.

  THIS RULE CANNOT DISCRIMINATE A NAT QUESTION AND NOTHING WILL MAKE IT.
    A NAT question has no options. Its last stem paragraph is therefore followed by
    the next question's date label DIRECTLY — no textless content required, nothing
    for D1/D2 to detect. A genuine subtopic heading occupies that identical slot.
    The two objects yield byte-identical lookahead values, so no positional rule,
    forward or backward, can separate them. For NAT, DISCRIMINATOR 2 is the only
    consumer-side rule that works, and it is not optional.

  DISCRIMINATOR 2 — COLOUR, the DIRECT signal (GAP-2026-08-05-001 / SG-9):
    PYQSort S6-2 mandates 11pt Bold Navy #003366 for every level-3 heading and
    make_heading_para() stamps <w:color> UNCONDITIONALLY, so any file PYQSort emitted
    carries it by construction, not by luck. Consult it via
    bc.heading_colour_available(paras) -> bool, computed ONCE PER FILE and passed to
    is_taxonomy_heading(..., colour_available=). The probe reads the DATE LABELS, not
    the headings, because S6-2 mandates their colour too, CHECK 3 enforces it and
    EC-S10 guarantees one above every question.
    THE GATE MUST BE PER FILE, NOT PER PARAGRAPH. "Require navy, fall back when
    colour is absent on that paragraph" fixes NOTHING (measured: phantoms 1 -> 1) —
    a misread continuation has no <w:color> element at all, so it takes the fallback
    straight back into the blind spot. If ANY date label in the file is not
    explicitly navy, colour is unavailable for that whole file and DISCRIMINATOR 1
    applies. w:themeColor counts as UNAVAILABLE, not as "not navy": the alternative
    turns an unusual styling choice into total heading loss for that file.
    NOTE: level 2 (Topic N:) is BLACK #000000 per S6-2 and is self-identifying by its
    prefix, so it returns True before the colour gate is ever reached. Do not "fix"
    that by requiring navy of it.
    BOTH DISCRIMINATORS SHIP. Their blind spots do not overlap: colour cannot see a
    continuation deep-copied from a navy-styled source; position cannot see a heading
    whose colour was stripped, and cannot see NAT at all.
  GUARANTEED BY (exam-agnostic; names no exam, section or subtopic):
    PYQSort S6-2    — date label "always emitted immediately above Q.N stem, zero
                      paragraphs between"
    PYQSort CHECK 3 — HARD FAIL if date-label count != Q-count, or the position slips
    PYQSort EC-S10  — ValueError when a Q.N has no preceding date label
  ENFORCED BY: blueprint_core.is_taxonomy_heading(para, is_option, next_text), with
    next_text from blueprint_core.next_nonempty_texts(). Levels 1 and 2 are exempt —
    they carry an explicit prefix and are self-identifying.
  NOT a heading → skipped by is_taxonomy_heading() via the positional gate.
```

---

## §7 — NAME CONSISTENCY CONTRACT

```
═══════════════════════════════════════════════════════════════════════
NAME CONSISTENCY — SINGLE SOURCE OF TRUTH
═══════════════════════════════════════════════════════════════════════

The APPROVED Analysis doc is the SINGLE SOURCE OF TRUTH for all
display names (Section, Topic, Subtopic). Every downstream consumer
reads names from the Analysis doc or from files derived from it.

CHAIN:
  Phase 0c (Analysis doc) → PYQSort (reads taxonomy) → Sorted PYQ headings
  → Step 5 E-1 parser → section_rules.md → manifest.json
  → Step 6 (Blueprint) → Step 7 (Create)

RULES:
  1. ALL names MUST be .strip()-ed at WRITE time. No trailing/leading whitespace.
  2. PYQSort MUST copy subtopic names EXACTLY from the Analysis doc — no rewording,
     no punctuation changes, no case changes.
  3. Phase B MUST use the SAME heading parser as Step 5 (§5-2).
  4. If a name needs correction: update the Analysis doc, re-approve, re-sort
     ALL affected papers. Never fix downstream only.

KNOWN RISK — COSMETIC VARIATIONS:
  "Triangles — Centres, Congruence, Similarity" (em-dash)
  "Triangles - Centres, Congruence, Similarity"  (hyphen)
  These are DIFFERENT strings. The subtopic_id contract (Step 5 slugify)
  handles this: both produce the same slug. But for cleanliness, Phase 0c
  MUST use consistent punctuation throughout.

VERIFICATION:
  After Phase B --counts, compare subtopic names in the updated Analysis doc
  against names in Step 5's section_rules.md. If ANY mismatch → flag as error.
  The slugify-based subtopic_id contract tolerates cosmetic differences, but
  zero mismatches is the standard.
```

---

## §8 — CLASSIFICATION RULES (Universal)

```
═══════════════════════════════════════════════════════════════════════
UNIVERSAL CLASSIFICATION RULES — APPLY TO ALL EXAMS
═══════════════════════════════════════════════════════════════════════

These rules are embedded in the framework and apply to every PYQAnalyse
scan and every PYQSort invocation. Exam-specific precedents are loaded
from the Analysis doc or a companion config file.

RULE 1 — TOPICAL HOME WINS OVER SOLVE METHOD
  Pick the subtopic whose DOMAIN matches what the question is ABOUT,
  not what technique is USED to solve it.
  Example: Bank deposits earning interest → Simple Interest (not Percentage)
  Example: Two trains crossing → Trains/Boats (not Speed/Distance/Time)
  Example: Discount on marked price + resulting profit → Discount (not P&L)

RULE 2 — THE VERB AT THE END OF THE STEM DECIDES
  "find the ratio" → Ratio & Proportion
  "find the percentage" → Percentage
  "find the value of [trig expression]" → Trigonometry
  "find the average" → Average

RULE 3 — OMML-AWARE CLASSIFICATION IS MANDATORY
  When a question stem contains <m:oMath> math expressions, RENDER the math
  before classifying. Walk <m:t>, <m:r>, <m:f>, <m:sSup>, <m:sSub>, <m:rad>.
  "OMML obscured" is NEVER an acceptable reason to guess.
  PHASE 0b EXCEPTION: During lightweight scan via Drive read_file_content,
  OMML formulas may be stripped. Use fallback classification (S3-2 OMML
  HANDLING: Q-position + option content + context). Log "OMML-obscured"
  in question_format. This exception does NOT apply to PYQSort (Phase A)
  which MUST render OMML fully via python-docx.

RULE 4 — SECTION DETERMINED BY STRUCTURE, NOT CONTENT
  If marker_mode = true: section from module separator (=== Subject ===)
  If marker_mode = false: section from Q-number range in exam_config
  NEVER classify section from question content alone (a maths question in
  the Reasoning section stays in Reasoning — it might be Mathematical Operations).

  OUT-OF-RANGE Q-NUMBERS (v2.18 — marker_mode = false only):
    exam_config describes the CURRENT exam pattern. A PYQ corpus routinely spans
    SEVERAL patterns, so a Q-number can fall outside every configured range — a
    100-question paper from a previous era scanned against a 60-question current
    config leaves Q.61-Q.100 matching nothing.
    Such a question is NOT dropped, NOT guessed into the nearest section, and NOT
    assigned section=None. It takes the OUT_OF_PATTERN sentinel (see
    Framework_PYQSort v1.9 S2-2, same constant) and is then classified against the
    FULL taxonomy rather than one section's slice.
    This is the ONE case where the "not content" half of this rule is relaxed, and
    only because its premise fails: the rule presupposes the question HAS a
    structural section, and this one has none. The relaxation is gated on the
    sentinel, never on a failed match, so a question that does have a section can
    never reach it. Everything else about RULE 4 is unchanged.
    Record pattern_era='out_of_pattern' on the classification so Phase B and the
    batch report can distinguish era-mixing from a classification failure.

RULE 5 — CLOSEST FIT FOR UNCLASSIFIABLE QUESTIONS
  If no subtopic fits perfectly, classify under the closest match.
  No flagging, no halting. Decide and move on.
  The closest match is determined by: topical home (Rule 1) > stem keywords >
  option structure > question format.

RULE 6 — IMAGE/FIGURAL QUESTIONS
  If question has image in stem with no meaningful text:
  Classify under the section's spatial/figural subtopic if one exists.
  If no figural subtopic in taxonomy: classify under the most general subtopic
  in the section.

RULE 7 — PATTERN METADATA RECORDING (Phase 0b scan ONLY)
  During Phase 0b scan, EVERY classification MUST include 4 pattern
  metadata fields in addition to (section, topic, subtopic):

  question_task: what the student is asked to DO
    Values: find_match, find_next, find_wrong, select_correct,
            select_incorrect, identify_error, correct_error,
            fill_blank, rearrange, calculate, determine, classify,
            match_pair, complete_figure, decode, interpret_data,
            find_answer (for RC), or other descriptive string.

  question_format: how the content is presented
    Values: standalone_word, standalone_number, word_pair, number_pair,
            in_sentence, in_passage, word_list, number_set, number_letter_mixed,
            figure, table_based, matrix, code_string, statement_based,
            dialogue_based, or other descriptive string.

  question_direction: transformation direction if applicable
    Values: a_to_b, b_to_a, null (if not a transformation question)
    Example: Active→Passive = a_to_b, Passive→Active = b_to_a

  thematic_domain: knowledge area if classifiable
    Values: use snake_case descriptors relevant to the Topic.
    Example for OWS: actions_behaviour, persons_professionals,
      government_legal, animals_nature, literary_arts, medical_phobias,
      branches_of_study, places_structures
    Example for Spotting Errors: subject_verb_agreement, tense_errors,
      pronoun_errors, article_errors, preposition_errors
    Value: null if the question is generic / domain-independent

  These fields are NOT used during PYQSort (Phase A) — they exist solely
  to enable the Subtopic Refinement Pass (§3-6). They are stored in
  scan_progress.json classifications and discarded after approval.

  The metadata does NOT need to be perfect — it needs to be CONSISTENT
  enough to detect clusters. If two questions with the same metadata
  pattern belong to different subtopics, the refinement pass will split.
```

---

## §9 — EDGE CASES

```
EC-P1: EXAM WITH 0 PYQ PAPERS
  Phase 0b has nothing to scan. Run PYQScan anyway — it detects 0 papers,
  runs refinement pass (with 0 classifications → no splits), saves
  scan_progress.json, and prints "Run: PYQApprove".
  Taxonomy = 100% from Step 2a's per-entry decision tree (S2-3 Step 2),
  which produces syllabus-faithful subtopics even without any PYQ papers.
  --approve generates the Analysis doc with all counts = "—" (filled by Phase B).
  PYQSort never runs (no Row files). Phase B never runs.
  Step 5: section_rules with all confidence='absent'.
  Step 6: handles zero-PYQ exam via §5 ZP rotation.

EC-P2: EXAM WITH 1-2 PYQ PAPERS ONLY
  Falls under Gate 0 (SMALL_CORPUS_THRESHOLD = 20): all papers scanned.
  Gate 4 (refinement pass) still applies after all papers are scanned.
  Taxonomy depth relies primarily on Step 2a's syllabus-faithful derivation;
  scanning 1-2 papers provides minimal discovery but validates coverage.
  Taxonomy may be incomplete but Step 2a's domain knowledge compensates.

EC-P3: CROSS-SHIFT DUPLICATE QUESTIONS
  Same question in Shift 1 and Shift 2 of same date.
  Both are scanned and classified. Convergence tracks NEW SUBTOPICS
  (not question volume), so duplicates don't inflate discovery count
  or falsely trigger early exit.

EC-P4: RC / CLOZE LINKED QUESTIONS (5 Qs per passage)
  Each sub-question counted as 1 PYQ. 5 passage questions = 5 PYQs.
  Classify each sub-question by its individual task/pattern:
    - Q asks for a word's meaning → "Vocabulary in Context" subtopic
    - Q asks for factual detail → "Direct/Factual Retrieval" subtopic
    - Q asks for main idea → "Main Idea/Theme/Purpose" subtopic
  Each sub-Q may belong to a DIFFERENT subtopic under the same Topic.
  Passage text preserved per question in sorted output (per PYQSort design).

EC-P5: FIGURAL-ONLY QUESTIONS DURING SCAN
  Question has image in stem, no meaningful text.
  Phase 0b: classify under section's figural/spatial subtopic.
  Phase A (PYQSort): has image access for better classification.
  The subtopic must exist in taxonomy from Phase 0a/0b.

EC-P6: SECTION DETECTION — MARKERS vs Q-RANGE
  Framework auto-detects:
    Check first few paragraphs for === separators.
    If found → marker_mode = true (read module names from separators)
    If not → marker_mode = false (use Q-range from exam_config)
  Both modes can coexist across exams. exam_config.marker_mode is authoritative.

EC-P7: SAME SUBTOPIC NAME IN MULTIPLE TOPICS
  Example: "Subject-Verb Agreement" under both Spotting Errors AND Sentence Improvement.
  The (Section, Topic, Subtopic) TRIPLE is unique. Both are valid taxonomy entries.
  Classification uses the full triple, not just the subtopic name.

EC-P8: YEAR EXTRACTION FROM FILENAME FAILS
  Filename doesn't contain a recognisable year pattern.
  Resolution: skip this file from year-wise counts in Phase B.
  Log a warning. The file still contributes to total PYQ count.

EC-P9: VARIABLE Q COUNT PER PAPER
  Some exams have papers with different Q counts (e.g., 96Q vs 100Q).
  Framework handles any Q count — no hardcoded total.
  Q-range mode: if paper has fewer Qs than expected, later sections may have
  0 questions. This is valid (partial paper).

  PAPER LARGER THAN THE CURRENT PATTERN (v2.18 — the missing mirror of the above):
  The clause above covers only the SHORTER direction. The LONGER direction —
  a paper with MORE questions than exam_config.total_questions — was undocumented
  everywhere in the corpus, and it is the dangerous one: the surplus Q-numbers match
  no section range at all, whereas a short paper merely leaves ranges empty.
  This happens whenever an exam's pattern SHRINKS and the corpus retains the older,
  larger papers (e.g. a 100-question 2005 paper against a 60-question current
  pattern). It is a normal, expected state — legacy papers are retained precisely
  because the variety of concepts, phrasings, difficulties and question formats they
  contain is what makes generated questions good. Only the handling was missing.
  Resolution: RULE 4's OUT-OF-RANGE branch. The surplus questions take the
  OUT_OF_PATTERN sentinel (never None), are classified against the full taxonomy so
  their concepts still enter the corpus, and carry pattern_era='out_of_pattern'.
  S3-2a's pre-scan gate reports the size difference per paper BEFORE the scan starts.
  CONSEQUENCE — counts are safe, mix is not. Framework_Blueprint §4-2 consumes r_avg
  as a PROPORTION against a sec_qs budget taken from exam_config, so a different-size
  paper can neither inflate nor shrink allocation. Subject/subtopic MIX, however, is
  inherited from whichever eras the corpus contains; §3 recency weighting dampens but
  does not remove this. Reported, never silently absorbed.
  Related: Framework_PYQSort EC-S1b, Framework_Blueprint v1.36 §2 S2-3.

EC-P9b: SAME Q COUNT, DIFFERENT QUESTION TYPES (v2.19)
  An exam keeps 50 questions but converts Q.41-50 from MCQ to NAT. Counts match, all
  Q-numbers are in range, so a size-only era test calls every legacy paper 'current' and
  blends its mix and its axis-3 (mechanism) distribution into today's targets.
  Resolution: bc.classify_paper_era compares each position's OBSERVED type against
  exam_config.marking_scheme and returns era='retyped'. Requires marking_scheme to be
  present and question types to have been detected; with either absent no type comparison
  is attempted and the size/numbering chain applies unchanged.
  For ~200 exams this is expected to be the MOST COMMON kind of pattern change.

EC-P9c: MARKER-MODE PATTERN CHANGE (v2.19)
  marker_mode exams carry no Q-ranges, so era cannot be read from Q-numbers. A retired
  SUBJECT/module is the signal instead. S3-2a step 3b compares observed module names to
  exam_config.sections[].name and reports any unknown module rather than letting EC-S2
  fuzzy matching absorb it into a surviving section.

EC-P10: BILINGUAL QUESTIONS (Hindi + English)
  Preserve non-Latin scripts in sorted output.
  Classification uses English portion of stem.
  Font fallback for Devanagari/regional scripts (Nirmala UI, Mangal, etc.).

EC-P11: DI TABLES IN QUESTIONS
  Full multi-row DI table → classify as Statistics / Data Tables (DI).
  Small 2-4 row reference table → classify by the arithmetic operation.
  Tables preserved verbatim in sorted output (original font size kept).

EC-P12: OMML FORMULAS IN STEMS
  Render OMML before classification. MANDATORY in both Phase 0b and Phase A.
  "OMML obscured" is never acceptable.

EC-P13: TAXONOMY APPROVED BUT USER FINDS ERROR LATER
  After approval, taxonomy is LOCKED. If error found after sorting has started:
  1. Correct the Analysis doc
  2. Re-upload to [ExamCode] project
  3. Re-sort ALL papers processed so far
  This is the cost of a taxonomy error. Framework documents this prominently
  in the approval gate message.

EC-P14: PHASE B AND STEP 5 COUNT MISMATCH
  Both parse sorted PYQ headings. Both use parse_taxonomy_level().
  If counts diverge: Step 6's BV-0A cross-check catches it.
  Root cause: one parser diverged from the heading format contract (§6).
  Fix: ensure both use IDENTICAL parser code.

EC-P15: VERY LARGE TAXONOMY (500+ subtopics)
  Some exams have many subtopics. Classification rules scale linearly.
  Context window may need BATCH_SIZE reduced to 2 for Phase 0b scan
  to fit the full taxonomy + 2 papers + classification output.
  Phase A (PYQSort) always processes 1 paper — unaffected by taxonomy size.
  Refinement pass (§3-6) also scales linearly — processes per-subtopic.

EC-P16: EXAM PATTERN CHANGES BETWEEN YEARS
  2024 exam has Figural questions, 2025 removes them.
  Taxonomy includes ALL subtopics from ALL years.
  Phase B counts will show 0 for 2025 on Figural subtopics.
  Step 6 handles year-specific patterns via recency weighting.

EC-P17: SUBTOPIC WITH 0 PYQS AFTER REFINEMENT SPLIT
  Refinement splits "Analogy" subtopic "Number Analogy" into 3 new subtopics.
  Some new subtopics may have 0 classified questions (if no questions in
  the scanned set matched that pattern). This is VALID — the subtopic
  exists because domain knowledge says it's a real exam pattern.
  Phase B will fill actual counts later. A 0-count subtopic is harmless;
  a missing subtopic is a taxonomy failure.

EC-P18: REFINEMENT CREATES DUPLICATE SUBTOPIC NAME ACROSS TOPICS
  Refinement splits create "Subject-Verb Agreement" under Topic "Spotting
  Errors" — but the same name already exists under Topic "Sentence
  Improvement". This is VALID per EC-P7: the (Section, Topic, Subtopic)
  TRIPLE is unique. Both are legitimate taxonomy entries because they
  represent different question types (finding the error vs improving
  the sentence) that happen to test the same grammar concept.

EC-P19: SCAN RESUME AFTER REFINEMENT PASS
  Refinement found splits → consecutive_empty_batches reset to 0.
  Scan must continue to verify stability of the expanded taxonomy.
  The refinement_pass_done flag stays True (refinement runs only once).
  Gate 3 must be re-satisfied: 7 more consecutive empty batches needed.
  Gate 2 does NOT need to be re-satisfied — it was already met before
  refinement triggered. The additional papers push total above 30%.
  Gate 4 stays True (refinement runs only once).
  Worst case: 60 (Gate 2) + 21 (post-refinement Gate 3) = 81 papers.
  If scan resumes and finds MORE new subtopics (from the freshly split
  taxonomy revealing finer patterns), consecutive_empty resets again.
  This is correct — it means the taxonomy is still evolving.

EC-P20: SYLLABUS WITH PRE-GROUPED ITEMS vs INDIVIDUALLY-LISTED ITEMS
  Some syllabi present items in groups:
    "Vocabulary: Synonyms, Antonyms, Spelling, OWS, Idioms"
  Others list items individually:
    "Synonyms/Homonyms, Antonyms, Spellings, Idioms & Phrases, OWS"

  For grouped syllabi: the GROUP NAME (e.g., "Vocabulary") is NOT a Topic.
    The ITEMS within the group are the Topics. Apply the Topic Integrity
    Test (S2-3 Step 1) to each item individually.
  For individually-listed syllabi: each item is already at Topic level.
    Apply the Topic Integrity Test to confirm.

  In BOTH cases, the result should be the same: each distinct question
  type = one Topic. The syllabus presentation format does not change
  the taxonomy structure.

EC-P21: DRIVE FOLDER CONTAINS NON-DOCX FILES
  Filter: only process files with mimeType =
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  Skip PDFs, images, Google Docs, folders. Log skipped files.
  Only .docx files count toward total_available for convergence gates.

EC-P22: DUPLICATE OR NEAR-DUPLICATE FILENAMES
  If two files have the same date + shift (ignoring trailing " 1", " 2"
  suffixes), they are duplicates. Process the LARGER file (more likely
  to have images). Skip the smaller. Log the skip.
  Both count as 1 paper for total_available (not 2).
  See deduplicate_files() in S3-2.

EC-P23: DRIVE FOLDER STRUCTURE VARIANTS
  The spec handles:
    a) Flat folder (all .docx directly inside) — collect all
    b) Year subfolders (2019/, 2020/, ...) — scan recursively
    c) Any nesting depth — walk full tree
  Year is extracted from FILENAME, not folder name. Folder names are
  used only for navigation, not year attribution.

EC-P24: FIGURAL QUESTION MISCLASSIFICATION DURING SCAN
  Scan-level classification of figural questions relies on text clues
  when images are unavailable via Drive read_file_content.
  If the stem says "Select the figure" with no further context, classify
  under Figure / Pattern Completion (default figural subtopic).
  PYQSort (Phase A) uses python-docx with full image access and will
  reclassify more accurately. Scan misclassification of figural questions
  is acceptable — it does not affect taxonomy structure (figural subtopics
  are created by Step 2a's syllabus-faithful derivation, not by scan discovery).

EC-P25: OMML-OBSCURED QUESTIONS DURING SCAN
  Drive read_file_content may strip OMML formulas, leaving blank stems.
  Classify using Q-position (section), option content analysis, and
  surrounding question context. Log "OMML-obscured" in question_format.
  Accuracy is lower (~70-80%) but acceptable for scan-level classification.
  PYQSort performs full OMML rendering for final classification.

EC-P26: PARTIAL BATCH ON CONTEXT LIMIT
  If context fills before completing BATCH_SIZE papers in a batch:
    1. The partial batch does NOT increment/reset consecutive_empty counter
    2. Save scan_progress.json + classifications.json with partial results
    3. Print session handoff message (see S3-7)
    4. New session resumes the incomplete batch — re-processes any papers
       from the partial batch that weren't fully classified

EC-P27: PHANTOM TRIPLE — NAME MISMATCH BETWEEN SORTED FILE AND ANALYSIS DOC
  A counted (section, topic, subtopic) triple does not exist in the Analysis
  doc taxonomy. Common causes:
    - Trailing/leading whitespace in sorted file heading (PYQSort bug)
    - Dash variant: em-dash (—) vs hyphen (-) vs en-dash (–)
    - Case difference: "DI" vs "di" vs "Di"
    - Punctuation: "Time & Work" vs "Time and Work"
  Task 2.5 (S5-4b) catches this with fuzzy matching to suggest the
  closest taxonomy triple. Resolution requires either re-sorting the
  affected papers or correcting the Analysis doc. Phase B cannot
  auto-fix because the correct name is ambiguous.

EC-P28: ORPHAN QUESTION IN SORTED FILE
  A question appears in a sorted PYQ file before any Subject or Subtopic
  heading. This means PYQSort emitted a question without taxonomy context.
  This is a PYQSort bug, not a Phase B issue. Phase B logs the orphan
  (file + Q number + reason) and HARD STOPs. Resolution: re-sort the
  affected paper in Step 3.

EC-P29: NON-SORTED FILE IN DRIVE FOLDER
  Drive folder contains .docx files that are NOT sorted PYQ outputs (e.g.,
  original Row files, the Analysis doc, exam_config docs, or other documents).
  S5-1 filters by sorted filename pattern (*_Sorted_Q*-Q*.docx).
  Non-matching .docx files are skipped with a warning log.
  If ALL .docx files are non-matching → error: "No sorted files found."

EC-P30: DUPLICATE SORTED FILE IN DRIVE FOLDER (v2.21 — now a HARD STOP)
  Drive folder contains two sorted files for the same date+session (e.g.,
  paper was re-sorted after a correction and both copies remain).
  Resolution: HARD STOP naming both files with their sizes (S5-1
  assert_no_session_duplicates). The operator deletes the superseded copy.
  BEFORE v2.21 this kept the LARGER file, on the reasoning that it was more
  likely to have images intact. That rule became wrong in two independent ways:
    1. it selects by ACCIDENT. The two files differ in content — that is why
       one replaced the other — so choosing between them changes the counts,
       and S5-4a tolerates no error at all. Size is not evidence of currency;
       a superseded file can easily be the larger one.
    2. under the 10 MiB connector cap it picks precisely the copy least likely
       to be fetchable, turning a cosmetic duplicate into a blocked paper.
  The image-integrity reasoning is also obsolete: PYQSort v1.12 CHECK 10 gates
  image survival where the sorted file is produced, so a file that lost a
  figure cannot be delivered at all.

EC-P31: PAPER ABOVE THE DRIVE DOWNLOAD CAP (v2.21)
  A sorted file exceeds blueprint_core.DRIVE_CAP and the connector refuses the
  download. Detected TWICE, by design: predicted at S5-1 by
  bc.partition_by_transport from the fileSize the listing already carried, and
  caught at fetch time by corpus_io.fetch_drive_docx raising TransportFallback.
  Resolution: the paper is routed to the UPLOAD LANE and requested by name.
  It is never skipped and never counted as done. NOT a hard stop — a large
  paper must not stop a 200-paper run.
  The prediction is deliberately non-binding: if the connector's cap changes,
  the partition is simply wrong and the runtime fallback still routes correctly.
  Permanent fix: PYQCompress the paper once and replace it in Drive.

EC-P32: UPLOAD LANE EXCEEDS ONE CHAT (v2.21)
  More than bc.CHAT_FILE_LIMIT papers need uploading. At BATCH_SIZE_COUNTS = 5
  that is 4 batches / 20 papers per chat (bc.upload_batch_plan).
  Resolution: S5-1 prints chats_needed BEFORE Task 1 so the operator can plan.
  Per-file saves (S5-4) make the session boundary safe: work already counted is
  already persisted, and _transport.upload_lane tells the resumed session which
  papers still need supplying.

EC-P33: UNEXPECTED OR MISNAMED UPLOAD (v2.21)
  The operator uploads a file that was not requested, or the browser renames the
  requested file to "X (1).docx" because the original was already in Downloads.
  Resolution: corpus_io.resolve_uploaded_papers matches by CANONICAL identity —
  never by exact filename, and never by recency, because uploads accumulate
  across turns and "the newest five files" would silently recount earlier
  batches. An unrecognised upload is REPORTED and never processed.

EC-P34: TRUNCATED DOWNLOAD (v2.21)
  A download returns fewer bytes than the listing reported. This is the most
  dangerous transport failure because it does not look like one: a .docx
  truncated at a ZIP member boundary still opens as a valid archive, python-docx
  parses it without complaint, and the paper simply contains fewer questions.
  The count comes out low and nothing reports an error.
  Resolution: corpus_io.fetch_drive_docx asserts len(bytes) == fileSize and the
  PK\x03\x04 magic before the file is used, and raises TransportFallback on
  mismatch — the paper then takes the upload lane like any other fetch failure.
  This is why DEFECT A (capturing fileSize) is a correctness fix and not merely
  a planning convenience: without the reported size there is nothing to compare.

EC-P35: DRIVE CHANNEL CANNOT REACH THE CONTAINER (2026-08-15)
  The connector cannot put bytes where python-docx must read them: it returns
  payloads INLINE with no spill file, or the deployment blocks Google egress from
  the container, or the connector is not connected at all.
  This is NOT EC-P31. The file is UNDER DRIVE_CAP and the connector does not
  refuse it, so size-based partitioning cannot see the condition at all —
  measured on IIT_JAM_MATHEMATICS, bc.partition_by_transport returned auto:22 /
  upload:0 for a corpus of which zero papers were fetchable.
  Detection: the S5-0 CHANNEL PROBE. ONE paper, the smallest, before Task 1.
  Resolution: route the WHOLE corpus to the upload lane at S5-1 and print the
  bc.upload_batch_plan arithmetic before Task 1. NOT a hard stop. PYQCompress
  does NOT help — the constraint is the channel, not the file size.
  NEVER diagnose this per paper inside the acquisition loop: the condition is a
  property of the DEPLOYMENT and is identical for every paper in the corpus.
  NEVER diagnose it by listing a directory to see whether a spill file appeared.
  Which directory a deployment spills to — or whether it spills at all — differs
  between deployments of the SAME connector; measured 2026-08-15, one 40,488-byte
  paper spilled to a file in one deployment and returned inline in another, and
  the two spill directories were different directories. A probe that hardcodes a
  path reports 'inline' on a working spill channel and sends an entirely
  fetchable corpus to manual upload on every exam — a worse failure than the one
  the probe was added to catch, because it is silent and permanent.

EC-P36: INLINE CHANNEL EXCEEDS THE CONTEXT BUDGET (2026-08-15)
  channel == 'inline' and the corpus is large. Each paper costs
  bc.base64_cost_chars(fileSize) = ceil(bytes/3)*4 characters of context inbound,
  and again to persist it, so the Drive lane is bounded by CONTEXT, not by
  DRIVE_CAP. Measured: 22 papers / 986,230 bytes = 1,315,000 base64 characters
  (~329k tokens inbound, ~658k with persistence).
  Detection: the same S5-0 probe; the arithmetic is bc.base64_cost_chars summed
  over the drive lane, compared against bc.INLINE_BUDGET_CHARS.
  Resolution: bc.partition_by_transport(..., channel='inline') admits papers in
  listing order until the budget would be exceeded and routes the remainder to
  the upload lane, reporting them as deferred FOR CONTEXT, not for size.
  Papers already counted are unaffected — the per-file save in S5-4 makes the
  boundary safe — and _transport.channel recorded in count_progress.json
  prevents a resumed session from re-deciding the lane mid-corpus.
  Never restate the budget as a literal. INLINE_BUDGET_CHARS has one definition
  in blueprint_core, exactly as DRIVE_CAP and CHAT_FILE_LIMIT do.

  IN A MULTI-SESSION STEP (Step 5 PYQExtract) the resolution above is WRONG.
  See EC-P37: the budget is per SESSION, a fresh chat resets it, and the overflow
  is CARRIED to the next session rather than demanded as manual uploads.

EC-P37: INLINE CHANNEL IN A BATCHED, MULTI-SESSION STEP (2026-08-15)
  channel == 'inline' in a step that already stops at a batch boundary and resumes
  in a fresh chat — Step 5 (PYQExtract), BATCH_SIZE 3, mandatory BATCH STOP, and a
  documented Option B (download analysis_progress.json, open a fresh chat).
  EC-P35/EC-P36's resolution — route the corpus to the upload lane — is correct for
  a step that must complete in ONE session (Step 4) and wrong here, because A FRESH
  CHAT RESETS THE CONTEXT BUDGET. Applying the single-session rule to Step 5 turns a
  fully automatic multi-session run into 19 manual uploads on a 22-paper corpus.
  Resolution: apply the budget PER SESSION.
    admitted = bc.partition_by_transport(pending_recency_sorted, channel='inline',
                                         inline_budget=SESSION_INLINE_BUDGET)['auto']
  Process the admitted set, take the normal BATCH STOP, and instruct Option B. The
  upload lane remains the fallback for a paper that cannot fit even ONE session's
  budget, or that exceeds DRIVE_CAP — never the default for the corpus.
  The budget is HALVED for an inline channel in such a step: INLINE_BUDGET_CHARS
  prices INBOUND characters only, and the model pays that cost a SECOND time when it
  re-emits the payload into a python block for stage_drive_payload to decode. There
  is no third route — the container's egress allowlist contains no Google domain.
  Halve it at the CALL SITE (bc.INLINE_BUDGET_CHARS // 2), never by editing the
  shared constant: that constant is also Step 4's, and mutating it would silently
  re-partition a step this rule does not govern.
  A CONSEQUENCE THAT MUST NOT BE "FIXED": with the halved budget a session may admit
  FEWER papers than BATCH_SIZE — measured on IIT_JAM_MATHEMATICS, one 45-50 KB paper
  costs ~63,500 characters, so a session admits ONE paper. BATCH_SIZE is a pacing
  CEILING, not a floor, and the run simply takes more sessions. Widening the budget to
  reach BATCH_SIZE trades a longer run for a mid-batch context stall that the per-paper
  save survives but the operator cannot interpret. On a SPILL channel this clause is
  inert: context cost is zero, every pending paper is admitted, and pacing returns to
  BATCH_SIZE alone.
  ORDER IS LOAD-BEARING: partition only AFTER the recency sort. partition_by_transport
  admits papers in the order it receives them, and corpus_io.collect_corpus_files
  returns DRIVE LISTING order. Measured on IIT_JAM_MATHEMATICS — same 22 papers, same
  budget, only the order changed: listing order admitted 2017/2021/2014 (185,892
  chars), recency order admitted 2026/2025/2024 (189,156 chars). Partitioning the raw
  listing order can leave the §1-6 required years permanently unreached while the
  operator watches papers arrive successfully.

EC-P38: CHANNEL TRANSITION ON RESUME (2026-08-15)
  A step that spans sessions must not re-decide transport in each one. Persist the
  verdict — Step 4 in count_progress.json._transport.channel, Step 5 in
  analysis_progress.json._meta._transport — and REUSE it on resume. Re-probing costs
  one paper's context every session for a fact that is a property of the deployment.
  Exception: if the FIRST Drive-lane acquisition of a resumed session raises
  TransportFallback, re-probe exactly ONCE and overwrite the record. A resumed session
  may legitimately be running on a different deployment.
  Every transition MUST print and MUST be recorded. A silent mid-corpus lane change
  produces a run half of which was fetched under rules the other half was not.
  A progress file written before the transport key existed is VALID INPUT: the absent
  key means "probe as if fresh, then record". Never discard or invalidate it.

EC-P39: AN EMPTY LISTING IS NOT A ZERO-PYQ EXAM (2026-08-15)
  A step that has a legitimate zero-PYQ path — Step 5's Scenario B / '--synthesise
  ALL' — must NEVER reach it by inference from an empty listing. An empty listing and
  a PYQ-less exam are indistinguishable at that point, and the listing is exactly what
  a transport defect empties.
  Measured: Framework_MockTestAnalyse v2.49.1 read the wrong envelope key, got zero
  papers from a 22-paper folder, rewrote mode to '--synthesise ALL', and shipped a
  complete, green, F2-footered deliverable in which every subtopic was a zero-PYQ
  scaffold. Step 6 blueprinted it and Step 7 generated every question from training
  knowledge, for an exam with 22 years of papers in the folder the operator had just
  supplied. This is the ONE transport defect in the framework that can produce a wrong
  ANSWER rather than a stall — the "the failure is LOUD" mitigation does not hold here.
  Detection: zero usable papers from an operator-supplied corpus link.
  Resolution: HARD STOP with the transport diagnosis — report the entry count, the
  reject list with reasons, and the PHASE A cache check. A genuinely PYQ-less exam is
  requested EXPLICITLY by the operator; it is never inferred from an empty container.
```

---

## §10 — DELIVERABLE SET CONTRACT

### S10-1 — Closed deliverable set (per mode)

```
═══════════════════════════════════════════════════════════════════════
DELIVERABLE SET CONTRACT — EXHAUSTIVE AND CLOSED
═══════════════════════════════════════════════════════════════════════

Each mode delivers EXACTLY the files listed below and NOTHING ELSE.
This is an exhaustive, closed list — not a minimum. Creating or
delivering any file not on this list is a spec violation with the
same force as an anti-editorializing violation.

LIVE FAILURE (SSC CGL Tier 2, July 2026):
  Claude delivered an unauthorized taxonomy_draft_v2.json alongside
  the spec-defined scan outputs. The file was redundant (taxonomy
  lives inside scan_progress.json per v1.7 D2) and unauthorized
  (not in the output contract). Root cause: no "NOTHING ELSE"
  qualifier, no DO-NOT-DELIVER list, no pre-delivery checklist.

────────────────────────────────────────────────────────────────────
MODE: --taxonomy (Step 2a: PYQDraft)
────────────────────────────────────────────────────────────────────
DELIVER (both mandatory, single present_files call):
  1. [ExamCode]_taxonomy_draft.json
  2. [ExamCode]_exam_config.json

DO NOT DELIVER:
  ✗ Exam Syllabus source files (these are INPUTS, not outputs)
  ✗ Exam Pattern source files (these are INPUTS, not outputs)
  ✗ Any intermediate parsing or extraction files
  ✗ Any renamed or versioned variants of the above 2 files

DESTINATION: User downloads → uploads to [ExamCode] project knowledge.

────────────────────────────────────────────────────────────────────
MODE: --scan (Step 2b: PYQScan)
────────────────────────────────────────────────────────────────────
DELIVER (both mandatory, single present_files call after each batch
         AND at scan completion):
  1. [ExamCode]_scan_progress.json
  2. [ExamCode]_classifications.json

DO NOT DELIVER:
  ✗ [ExamCode]_taxonomy_draft.json (INPUT — already in project)
  ✗ [ExamCode]_taxonomy_draft_v2.json or any versioned taxonomy file
     (the evolved taxonomy lives INSIDE scan_progress.json['taxonomy']
      per v1.7 D2 — a standalone copy is redundant and unauthorized)
  ✗ [ExamCode]_exam_config.json (INPUT — already in project)
  ✗ Any per-batch intermediate files
  ✗ Any summary, analysis, or report files not listed above
  ✗ Any file with "taxonomy" in its name (taxonomy is INSIDE
     scan_progress.json, never a separate deliverable in --scan mode)

DESTINATION: User downloads → uploads to [ExamCode] project knowledge.
             Replaces prior versions on each batch delivery.

NOTE: scan_progress.json MUST contain the COMPLETE evolved taxonomy
in its ['taxonomy'] field (v1.7 D2). This is the ONLY place the
scan-discovered taxonomy is stored. If Claude needs to work with
the taxonomy internally, it reads from scan_progress.json — it
does NOT create a separate file.

────────────────────────────────────────────────────────────────────
MODE: --approve (Step 2c: PYQApprove)
────────────────────────────────────────────────────────────────────
DELIVER (all three mandatory, single present_files call):
  1. [ExamCode]_PYQ_Analysis.docx  (single merged doc, all subjects)
  2. [ExamCode]_exam_config.json   (may be updated with OTS boundaries)
  3. [ExamCode]_approval_record.json  (v2.17 — S4-0 reconciliation verdict,
     adjudication ledger, conservation proof. REQUIRED: later PYQApprove runs
     replay its verdicts per INV-6. Not a report — a load-bearing artifact.)

DO NOT DELIVER:
  ✗ [ExamCode]_scan_progress.json (INPUT — consumed, not forwarded)
  ✗ [ExamCode]_classifications.json (INPUT — consumed, not forwarded)
  ✗ [ExamCode]_taxonomy_draft.json (INPUT — consumed, not forwarded)
  ✗ Per-subject Analysis docs (merged format replaced per-file in v2.6)
  ✗ Any intermediate generation files

DESTINATION: User downloads → uploads to [ExamCode] project knowledge.
             Taxonomy is LOCKED after upload — no further changes.

────────────────────────────────────────────────────────────────────
MODE: --counts (Step 4: PYQCount)
────────────────────────────────────────────────────────────────────
DELIVER (single file, single present_files call at completion):
  1. [ExamCode]_PYQ_Analysis.docx  (UPDATED with PYQ counts)

DO NOT DELIVER:
  ✗ [ExamCode]_count_progress.json (internal session persistence —
     saved to /home/claude for resume, never delivered to user)
  ✗ Any intermediate counting files or scripts
  ✗ count_pipeline.py or count_finalize.py (execution scripts)

INTERIM SESSION DELIVERY (session handoff only):
  When context limit forces session break during counting:
    Deliver [ExamCode]_count_progress.json via present_files
    for the user to upload to project knowledge for resume.
    This is a SESSION PERSISTENCE deliverable, not a final output.
    It is NOT delivered at completion — only at session breaks.

DESTINATION: User downloads → replaces prior Analysis doc in
             [ExamCode] project knowledge.
═══════════════════════════════════════════════════════════════════════
```

### S10-2 — Pre-delivery checklist (MANDATORY before every present_files call)

```python
import os

# ── MODE-SPECIFIC EXPECTED SET ──────────────────────────────
# Set `expected` based on current mode before running checks.

# --taxonomy mode:
expected_taxonomy = {
    f'{exam_code}_taxonomy_draft.json',
    f'{exam_code}_exam_config.json'
}

# --scan mode:
expected_scan = {
    f'{exam_code}_scan_progress.json',
    f'{exam_code}_classifications.json'
}

# --approve mode:
expected_approve = {
    f'{exam_code}_PYQ_Analysis.docx',
    f'{exam_code}_exam_config.json',
    f'{exam_code}_approval_record.json'      # v2.17 (S4-0)
}

# --counts mode (completion):
expected_counts = {
    f'{exam_code}_PYQ_Analysis.docx'
}

# --counts mode (session break):
expected_counts_interim = {
    f'{exam_code}_count_progress.json'
}

# ── UNIVERSAL CHECKS ───────────────────────────────────────
expected = expected_scan  # ← set to current mode's expected set

# NOTE: Checks validate the present_files ARGUMENT LIST, not the
# full outputs directory (which may contain files from prior modes).

# files_for_present: the list of paths about to be passed to present_files
delivering = set(os.path.basename(f) for f in files_for_present)

# Check 1: All expected files present in the delivery list
missing = expected - delivering
assert not missing, f"MISSING deliverables: {missing}"

# Check 2: No unexpected files in the delivery list (CLOSED SET)
extra = delivering - expected
assert not extra, f"UNAUTHORIZED files in present_files call: {extra}. " \
                  f"Remove before calling present_files."

# Check 3: No internal/intermediate files leaked into the delivery
banned_patterns = [
    'taxonomy_draft_v2', 'taxonomy_draft_v3',  # versioned taxonomy
    'taxonomy_evolved', 'taxonomy_updated',     # renamed taxonomy
    'batch_', 'temp_', 'intermediate_',         # working files
    'pipeline', 'script',                       # execution scripts
]
leaked = [f for f in delivering
          if any(p in f.lower() for p in banned_patterns)]
assert not leaked, f"INTERNAL files leaked to delivery: {leaked}"

# Check 4: For --scan mode, verify taxonomy is INSIDE scan_progress
if mode == 'scan':
    import json
    sp_path = f'/mnt/user-data/outputs/{exam_code}_scan_progress.json'
    with open(sp_path) as f:
        sp = json.load(f)
    assert 'taxonomy' in sp, \
        "scan_progress.json missing ['taxonomy'] field (v1.7 D2)"
    assert isinstance(sp['taxonomy'], dict) and len(sp['taxonomy']) > 0, \
        "scan_progress.json['taxonomy'] is empty — must be COMPLETE"

print("Pre-delivery checklist: ALL PASS")
# Only after all checks pass → call present_files
```

### S10-3 — Delivery destinations (quick reference)

```
--taxonomy : User downloads → uploads to [ExamCode] project knowledge
             Next: PYQScan
--scan     : User downloads → uploads to [ExamCode] project knowledge
             (replaces prior version on each batch)
             Next: continue scanning OR PYQApprove
--approve  : User downloads → uploads to [ExamCode] project Files section
             Next: PYQSort (one Row file at a time, same project)
--counts   : User downloads → uploads to [ExamCode] project Files section
             (replaces the no-counts version)
             Next: Step 5 (PYQExtract) + Step 6 (MockBlueprint)
```

### S10-4 — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat delivery report or handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Upload / Replace / Use locally), and next-step reference.
```

---

## §11 — EXAM-AGNOSTIC GUARANTEE

```
UNIVERSAL IN THIS SPEC (identical every exam):
  Trigger parsing and mode detection
  Topic Integrity Test (3 questions — S2-3 Step 1)
  Per-entry decision tree for subtopic derivation (S2-3 Step 2: Q1/Q2/Q3)
  Unique Domain Property enforcement (no overlapping concept claims)
  6 Pattern Dimensions as optional tool for undivided blocks (S2-3 Appendix)
  Ratio-based guardrail (flag 2.0×, hard-stop 3.0×) and near-duplicate check
  Smart scan algorithm with 4-gate convergence
  Anti-editorializing rules (chat + JSON)
  Batch integrity rule (partial batches don't count)
  Session management protocol (S3-7)
  Drive reading method with OMML/figural fallback
  New discovery validation (3-question gate)
  Subtopic Refinement Pass (§3-6) with per-subtopic execution model
  Round-robin year sampling (newest-first, date-asc within year)
  Classification storage (separate file for large corpora)
  Analysis doc format (.docx with tables)
  Heading format contract (§6)
  Name consistency contract (§7)
  Universal classification rules 1-7 (§8)
  All 34 edge cases (§9)
  Progress JSON schemas (schema_version 2.0)
  Batch processing model (3/batch scan, 5/batch counts)
  Task 1 pre-count confirmation gate (S5-1a)
  Task 2 post-count accuracy gate (S5-4a)
  Task 2.5 taxonomy name cross-check (S5-4b)
  Task 3 doc-writing arithmetic verification (S5-5)
  Phase B execution model — Python script (S5-8)


EXAM-DISCOVERED (zero hardcoding):
  Section names, topic names, subtopic names → from syllabus + PYQ + refinement
  OTS section count, Q count per section, Q ranges → from exam pattern xlsx / doc
  Subject order → from exam pattern
  marker_mode → from PYQ structure detection
  Medium, question types, level → from exam pattern xlsx Overview tab
  Marking scheme (per-range type, marks, penalty) → from exam pattern xlsx Range tab
  Max attempt per section → from exam pattern xlsx Sections tab
  Classification precedents → from PYQ content discovery
  Refinement splits → from classified question pattern metadata

PROOF (validated against 13 exams — all produce ratio ≤ 2.6×):
  SSC CGL Tier 1:        ~30 entries → ~30 subtopics  (1.0×, short labels)
  SSC CGL Tier 2:        ~35 entries → ~35 subtopics  (1.0×, short labels)
  CAT:                   ~25 entries → ~25 subtopics  (1.0×, short labels)
  MPPSC Botany:           81 entries →  81 subtopics  (1.0×, lettered descriptors)
  CSIR NET Life Sci:    ~120 entries → ~120 subtopics (1.0×, lettered descriptors)
  GATE Biotech:          ~35 entries →  ~35 subtopics (1.0×, colon-headed topics)
  GATE CS:                10 sections → ~20 subtopics (2.0×, undivided blocks)
  IIT JAM Physics:         7 sections → ~14 subtopics (2.0×, undivided blocks)
  UGC NET History:       ~40 paras   →  ~40 subtopics (1.0×, named paragraphs)
  CUET PG Mathematics:     7 headers →   ~9 subtopics (1.3×, umbrella label split)
  CUET UG Political Sci:  16 chapters →  16 subtopics (1.0×, textbook chapters)
  NEET (3 subjects):     ~50 units   →  ~70 subtopics (1.4×, units with bullets)
  CTET Paper 1:          ~12 sub-sec →  ~31 subtopics (2.6×, content labels)
  Same spec handles all — zero exam-specific code.
```

---

## §12 — DEFINITION OF DONE

```
Phase 0a:
  ☐ Syllabus fully extracted (all subjects, all items)
  ☐ Exam pattern fully extracted — xlsx (preferred) or legacy format
  ☐ If xlsx: 3 tabs parsed (Overview, Sections, Range)
  ☐ If xlsx: all 10 structural validations passed (V1-V10):
    ☐ V1: Σ(Total Question) == Total Questions
    ☐ V2: Q_Ends − Q_Starts + 1 == Total Question (per section)
    ☐ V3: Section Q-ranges contiguous, non-overlapping
    ☐ V4: Range tab tiles Q.1 through Total Questions completely
    ☐ V5: All Negative Marks ≤ 0
    ☐ V6: Σ(Max Attempt × correct_marks) == Total Marks
    ☐ V7: 0 < Max Attempt ≤ Total Question (per section)
    ☐ V8: Overview Question Type set == Range tab distinct types
    ☐ V9: All Correct Marks > 0
    ☐ V10: Total Questions > 0, Duration > 0
  ☐ New fields populated: medium, question_types, level, marking_scheme[], max_attempt
  ☐ Section ≠ Subject principle applied (section names = OTS labels, not taxonomy)
  ☐ Topic Integrity Test applied — each distinct question type = one Topic
  ☐ Per-entry decision tree (Q1/Q2/Q3) applied to every syllabus entry
  ☐ Exclusion rules applied (vocabulary lists, scope markers, format qualifiers)
  ☐ Unique Domain Property verified — no two subtopics claim overlapping concepts
  ☐ Ratio guardrail passed: total_subtopics / syllabus_entries ≤ 3.0×
  ☐ Near-duplicate check passed: no pair with >75% name similarity
  ☐ Coverage check passed: every syllabus concept maps to exactly 1 subtopic
  ☐ Catch-all name check passed: zero Topics/Subtopics match banned patterns
  ☐ 1:1 Topic=Subtopic check passed: no Topic has a single subtopic with the
    same name UNLESS the syllabus genuinely lists it as a single atomic concept
  ☐ taxonomy_draft.json generated with correct structure
  ☐ exam_config.json generated with correct metadata (v2.5 schema)
  ☐ Both files delivered via present_files
  ☐ Deliverable set closed: EXACTLY 2 files delivered (S10-1 --taxonomy)
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call

Phase 0b:
  ☐ PRE-SCAN GATE: Year-wise paper inventory displayed with per-paper Q counts
  ☐ PRE-SCAN GATE: Pattern Era column present; era computed from exam_config +
    observed Q-numbers only (S3-2a step 3b) — never from filename or year
  ☐ PRE-SCAN GATE: Pattern-era notice printed when the corpus spans >1 era
    (and suppressed entirely when it does not)
  ☐ PRE-SCAN GATE: User confirmation received before scanning begins
  ☐ Round-robin year sampling applied (newest-first, date-asc within year)
  ☐ Drive file inventory cached in scan_progress.json (no re-listing on resume)
  ☐ File deduplication applied (EC-P22)
  ☐ Drive reading method used with OMML/figural fallback (S3-2)
  ☐ Pattern metadata (RULE 7) recorded for every classification
  ☐ Per-question classifications stored in [ExamCode]_classifications.json
  ☐ New discovery validation (3-question gate) applied before taxonomy changes
  ☐ Post-paper Q-count validation logged (informational)
  ☐ All new subtopics added to taxonomy (in scan_progress.json — FULL, not delta)
  ☐ 4-gate convergence enforced:
    ☐ Gate 0: small corpus (≤20 papers) → all papers scanned
    ☐ Gate 1: all available years covered
    ☐ Gate 2: ≥30% of total papers scanned (PROSE MANDATE enforced)
    ☐ Gate 3: ≥7 consecutive empty batches (after gates 0-2 pass)
    ☐ Gate 4: refinement pass completed
  ☐ Anti-editorializing enforced (no banned phrases in chat, no banned fields in JSON)
  ☐ Batch integrity enforced (partial batches don't affect counter)
  ☐ Subtopic Refinement Pass (§3-6) executed with per-subtopic model
  ☐ Orphan classification check passed after refinement
  ☐ Session management protocol followed (4-5 batches/session target)
  ☐ scan_progress.json saved after each batch (schema_version 2.0)
  ☐ classifications.json saved after each batch (separate file)
  ☐ Batch Stop Law enforced (S3-4a): each batch = one response;
    next batch starts ONLY after user's continue trigger;
    auto-advance is permanently banned including small corpora
  ☐ Batch-end message includes per-section Q-count distribution
  ☐ Batch-end message includes classification quality (normal/OMML/figural)
  ☐ Post-convergence summary displayed before "Run: PYQApprove"
  ☐ Resume sessions re-list Drive files and re-run S3-2a pre-scan gate
  ☐ Deliverable set closed: EXACTLY 2 files per batch (S10-1 --scan)
  ☐ Taxonomy stored INSIDE scan_progress.json (no separate taxonomy file)
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call

Phase 0c:
  ☐ Single merged Analysis .docx generated with all subjects (page-break separated)
  ☐ All topics and subtopics present in doc
  ☐ PYQ Count columns show "—" (not filled)
  ☐ Format matches IFAS reference (tables, headings, footer)
  ☐ All names .strip()-ed (no trailing whitespace)
  ☐ exam_config.json included in delivery
  ☐ S4-4 verdict printed from a COMPLETED S4-0 record (Branch A / B / C)
  ☐ Deliverable set closed: EXACTLY 3 files delivered (S10-1 --approve)
  ☐ S4-0 ran BEFORE S4-4 and its approval_record.json exists
  ☐ approval_record.checks.missing is empty  (INV-7)
  ☐ approval_record.checks.vacuous is empty  (INV-8)
  ☐ approval_record.unmaterialisable is empty (INV-9 / INV-10)
  ☐ approval_record.mode matches the R1 mode actually taken
  ☐ Every C7 anchoring line in the gate matches taxonomy_draft.json
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call

Phase B:
  ☐ TASK 1: Year-wise paper inventory displayed with per-paper Q counts
  ☐ TASK 1: Q-counting uses bc.detect_question_start() — never a local regex
         (GAP-2026-08-15-BAREQ R-3; count_sorted_file delegates to the same engine call)
  ☐ TASK 1: Per-file Q counts stored in task1_per_file for Task 2 diagnostic
  ☐ TASK 1: User confirmation received before counting begins
  ☐ Sorted file filtering applied (*_Sorted_*.docx pattern)
  ☐ Duplicate sorted file detection applied (same date+session dedup)
  ☐ Multi-date files excluded from dedup
  ☐ Non-sorted files skipped with warning log
  ☐ All sorted PYQ files from Drive processed (5 per batch max)
  ☐ Heading parser matches Step 5's parse_taxonomy_level() exactly
  ☐ Child pointer reset on new parent heading (cur_sub reset on new Topic)
  ☐ Year extracted from each filename
  ☐ Counts aggregated correctly (per subtopic, per year)
  ☐ Per-file attributed counts tracked for Task 2 diagnostic
  ☐ Orphan questions tracked per file (zero orphans required)
  ☐ TASK 2: Full Subject > Topic > Subtopic breakdown displayed
  ☐ TASK 2: Grand total == Task 1 confirmed total (zero tolerance)
  ☐ TASK 2: Per-file diagnostic available on failure
  ☐ TASK 2.5: Taxonomy extracted from the Analysis doc using parse_taxonomy_level rules
  ☐ TASK 2.5: Every counted triple exists in the Analysis doc taxonomy
  ☐ TASK 2.5: Phantom triples = 0 (hard stop if any found)
  ☐ TASK 2.5: Uncounted subtopics listed (informational)
  ☐ TASK 3: Subtopic cells filled with exact verified counts
  ☐ TASK 3: Zero-count subtopics written as "0" (no "—" remains)
  ☐ TASK 3: Per-topic TOTAL rows == sum of subtopic cells
  ☐ TASK 3: Master summary topic PYQs == topic TOTAL rows
  ☐ TASK 3: GRAND TOTAL == sum of all topic totals
  ☐ TASK 3: Header total == GRAND TOTAL
  ☐ TASK 3: Cross-check: header == grand == sum(topics) == sum(subtopics)
  ☐ TASK 3: Sum of all section header totals == Task 1 confirmed total
  ☐ TASK 4: Batch size = 5 papers per batch (BATCH_SIZE_COUNTS = 5)
  ☐ Enumeration captured fileSize + mimeType for every entry (S5-1)
  ☐ Every rejected entry printed with its reason — nothing dropped silently
  ☐ Both duplicate classes clear: canonical identity and date+session (S5-1)
  ☐ Transport plan printed BEFORE Task 1, including chats_needed for the
     upload lane (S5-1 plan_transport / S5-7)
  ☐ Every Drive fetch guarded — TransportFallback routed to the upload lane,
     never fatal (S5-4)
  ☐ count_progress.json saved after EVERY FILE, not merely after each batch
     (S5-4 — DEFECT C; the batch save is a redundant flush only)
  ☐ Uploads matched by canonical identity, unexpected uploads reported
  ☐ Execution model: Python script (count_pipeline.py / count_finalize.py)
  ☐ Session management: count_progress.json saved with files_processed_list
  ☐ Updated Analysis doc delivered via present_files
  ☐ Deliverable set closed: EXACTLY 1 file at completion (S10-1 --counts)
  ☐ count_progress.json NOT delivered at completion (internal)
  ☐ Pre-delivery checklist (S10-2) passed
  ☐ No unauthorized files in present_files call
```

---

# END OF Framework_PYQCore v1.4
