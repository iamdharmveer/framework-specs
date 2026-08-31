# Framework_MockDeliver v1.20.0 — Universal Mock Test Tagger & Delivery Engine
# v1.20.0 — 2026-08-31 — GAP-2026-08-29-STYLE-FIDELITY: step 3d prints the ONE style-profile status line from
#   pp.style_footer_line (§FOOTER-STYLE). No per-question detail, no similarity figure and
#   no G-* verdict ever reaches the delivered document (P-11 / ruling Q15); an absent
#   record is a legacy paper and prints nothing.
# v1.19.0 — 2026-08-29 — GAP-2026-08-29-DIFFICULTY-HARDER-PRESET (paired with Blueprint
#   v1.58.0 S7-0, blueprint_core Cluster DP, audit_canonical v2.24). §FOOTER-DS item 3c
#   gains the mode 'profile_harder' → "Difficulty mix: measured from [k] sittings
#   ([labels]), raised 30% by framework preset." — the framework's own default is
#   named as such, so it can never read as a measured mix nor as an operator
#   deviation. One prose line; no gate change (still 17); no engine change.
# v1.18.0 — 2026-08-27 — REPAIR-RETIRED-2026-08-27 (operator decision; paired with
#   paper_pipeline v5.76, MockTestCreate v5.76, MockTestExplain v1.47.0, DeliveryFooter
#   v1.29). The four *Repair triggers are RETIRED and the difficulty gate DISCLOSES instead
#   of blocking. S1-2 3b: the FAILED branch is GONE — 'FAILED' is a retired status that
#   pp.dg_preflight heals to DISCLOSED/0 (disclosed, footer line from rec['migrations']);
#   ('DISCLOSED', 0) PROCEEDS with the §FOOTER-DG measured-difficulty line; PENDING is the
#   ONLY gate state this step refuses, and its remedy (pp.dg_next_step) is the Explain
#   trigger. ('PASSED', 1) / ('DISCLOSED', 1) stay as LEGACY repaired papers. S1-2 item 3:
#   the writer list is Step 7 and Step 9. No tagging or delivery rule changed.
# v1.17.0 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE (paired with Blueprint v1.57.0). S1-2
#   item 3c / §FOOTER-DS: one delivery-footer line from blueprint.json['difficulty_source']
#   (measured from k sittings | measured + operator-confirmed deviations | set by operator, no
#   PYQ profile | set on the trigger); absent key → nothing (legacy). Defined HERE, not in
#   DeliveryFooter, to keep the PYQPrepare route under its SPEC-BUDGET. No gate-count change.
# v1.16.0 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (paired with MockTestExplain
#   v1.46.0, MockTestCreate v5.73, DeliveryFooter v1.27, paper_pipeline v5.74 Cluster RH).
#   Two seam fixes, no gate change (still 17): (1) S1-2 3b said a HEALED registry "is
#   re-presented with the deliverables" while §8 said "No other files are presented" —
#   §8 now states the closed set as pp.handoff_set('TestDeliver', …): Final.docx always,
#   plus registry.json (Replace in Project Files) ONLY when pp.registry_changed shows the
#   preflight healed it — the one case this step changes the registry. (2) S1-2 item 3
#   states the REGISTRY-HANDOFF-LAW precondition explicitly: the project copy IS the
#   verdict; a PENDING/FAILED stop here on a paper whose Step 9 verdict box said PASSED
#   means the operator did not REPLACE the registry Step 9 delivered — the stop message
#   names that remedy before the re-run command. S1-2 also ignores a
#   [ExamCode]_[slug]_Explain_Report.docx attached alongside the Solutions docx (Step 9
#   v1.46.0 delivers one; it is inert here and never mistaken for the input).
# v1.15.0 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS (paired with MockTestExplain
#   v1.45.0, MockTestCreate v5.72, DeliveryFooter v1.26, paper_pipeline v5.72, blueprint_core
#   Cluster E2d). S1-2 3b: the FAILED branch documents pp.dg_next_step's two outcomes — the
#   repair pair for a windowed record, the Explain trigger for a FAILED record written under
#   the retired band-equality rule (re-judged, never repaired); the DISCLOSED footer example
#   shows the windowed shape ("(not gated)" / "in window"). No gate-count change (still 17);
#   the single-writer contract of v1.14.0 unchanged.
# v1.14.0 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER (paired with
#   paper_pipeline v5.71 Cluster DG, MockTestExplain v1.44.0, MockTestCreate v5.71,
#   DeliveryFooter v1.25). P0. S1-2 3b branched on `status` alone and ignored
#   repair_rounds_used; §7A-R R1 branched on the counter alone and ignored status.
#   On a corrupt (FAILED, 1) record each sent the operator to the other — no exit.
#   3b now opens with pp.dg_preflight (heals a corrupt pair per DG-INVARIANT with a
#   mandatory chat + footer disclosure; hard-stops on an unknown status), then acts
#   on pp.dg_deliver_decision — the branch table is encoded once in the engine and
#   every next-step command is pp.dg_next_step, the function Step 9 prints from.
#   NEW branch ('DORMANT', 0) → deliver with a dormancy footer line: a dormant gate
#   previously wrote nothing, the record stayed PENDING and every scoped paper /
#   non-3-band exam was undeliverable. §FOOTER-DG (referenced since v1.13.0, defined
#   nowhere) is now defined in DeliveryFooter v1.25 as pp.dg_footer_lines. Superseded
#   v1.12.1 entry moved verbatim to SPEC_HISTORY.md (EC-P42).
# v1.13.0 — 2026-08-24 — GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING (paired with MockTestExplain v1.42.0,
#   MockTestCreate v5.69). S1-2 gains item 3b: delivery reads
#   registry.difficulty_gate — PENDING/FAILED hard-stop with the exact next
#   command; PASSED delivers clean; DISCLOSED delivers with one measured-
#   difficulty footer line; ABSENT = legacy, delivers as before.
# v1.12.2 — 2026-08-19 — GAP-2026-08-19-UNCHECKED-END-MARKER-DRIFT. PATCH: prose-only,
#   no gate, no logic, no artefact change. This file is the ONLY spec in the corpus
#   carrying TWO end-of-document markers: the canonical `# END OF ...` sentinel that
#   MANIFEST.json pins and bootstrap.py verifies, AND a prose marker
#   `*End of Framework_MockDeliver vX (body)*` closing the body section. At the
#   v1.12.1 bump the SENTINEL was updated and the PROSE marker was not, leaving the file
#   declaring two different versions of itself.
#   ROOT CAUSE, worth naming: the marker that is CHECKED cannot drift, so only the
#   UNCHECKED one did. A corpus sweep confirms this is a single instance and not a
#   class — 21 end-markers across 21 specs, 20 correct, and every other spec carries
#   exactly one marker, which is the checked one. The durable fix is therefore not a
#   new rule but the removal of the redundant second version string: the prose marker
#   now closes the body WITHOUT restating a version, so there is no second version
#   string left to drift. The canonical sentinel remains the single source.
# [ExamCode] project | Step 11 (MockDeliver) | Exam-agnostic
#
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_MockDeliver.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.
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
- (v1.10.0) The former Step 8 independent re-derivation of `subtopic_id` no longer runs;
  Step 7's write is the single authority. `difficulty` is carried forward as before
  (not rendered in the paper).
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
    (subtopic-based mode only — see below)

registry.question_index[mock_N].questions[q].difficulty
  → canonical label from blueprint.difficulty_labels  = Complexity
```

**Zero AI classification. Zero hardcoded exam values. Fully deterministic.**
A tag value is wrong only if the registry or blueprint is wrong. v1.10.0: those
artifacts are Step-7 / Step-6 outputs that no audit step re-derives, so the JOIN is
exactly as correct as its inputs — deterministic, but no longer independently certified.

**Position-based vs. subtopic-based typing (v1.7).** The JOIN path above assumes
Question Type is a property of the subtopic. This is correct for subtopic-based
exams (e.g. SSC CGL, where every marking_scheme range is MCQ). For position-based
exams (e.g. GATE, where Q25-31 is always MSQ and Q48-65 is always NAT regardless
of which subtopic Step 6 assigns there in a given mock), Question Type depends on
the Q-NUMBER, not on subtopic identity — the same subtopic can be MCQ in one mock's
Q11-24 and NAT in another mock's Q48-65 (see EC-13). `blueprint.marking_scheme[]`
already carries this per-Q-range type (Step 2a v2.5+ contract, the same field Step 7
already uses via `_type_for_q()` to GENERATE the question). Step 11 now reads it too:
when `marking_scheme` carries more than one distinct `question_type` value, Question
Type is resolved from the Q-number against `marking_scheme`, and the subtopic's
`answer_type` / `answer_cardinality` are ignored for this tag. When `marking_scheme`
is absent, empty, or carries only one distinct type — including every scoped
blueprint, whose §7 marking_scheme is deliberately collapsed to one modal-type range
regardless of how many real types are in scope — resolution falls back to the
subtopic-based JOIN above, byte-identical to v1.6. See §3 S3-2a for the full
mode-selection rule.

---

# ★ ZERO-MUTATION RULE — NON-NEGOTIABLE

The content of every question block is SACRED. This step may only (v1.11.0):
- **Strip** any residual pre-Q.1 header paragraphs (SAFETY-NET only — the input is
  questions-only per Step 7 R8b / G-PREQ1, so this normally strips nothing; a non-zero
  strip is an upstream regression, flagged in the delivery report. v1.10.0: with the
  Step-8 A-HEADER backstop gone this is the ONLY header strip in the pipeline)
- **Insert** 5-line tag blocks above each Q-stem (new content only)

Those two edits are the ONLY changes to the delivered file. Nothing else is touched.

It **NEVER** (v1.11.0 — this now holds for the DELIVERED file, not merely an
undelivered "integrity" copy):
- **Linearizes, converts, or otherwise rewrites OMML math.** Every `<m:oMath>` is
  preserved byte-for-byte; the delivered OMML count equals the source (gates
  C5 + C11). The v1.10.0-and-earlier OMML→Unicode linearization (Rule 19) is
  RETIRED from the delivery path.
- **Re-fonts or recolors** any run. Rule 21 (non-ASCII safe-font) and Rule 22
  (underline recolor) are no longer applied to the delivered file (Phase 4 retired).
- Changes any character in any question stem, option, table, image, chart, or explanation
- Reorders questions
- Removes, rewrites, or paraphrases any content
- Drops or reorders the document root's namespace declarations, or lets mc:Ignorable
  name a prefix that is not declared (v1.3 — see the FOURTH hard invariant)

Violation of this rule is a hard failure regardless of any other outcome.

DELIVERED FILE = STEP-9 SOLUTIONS INPUT + (tag blocks). Byte-identical otherwise —
math, options, images, tables, charts, fonts, and colours all preserved exactly.

---

# ★ THE DELIVERED FILE IS THE INTEGRITY ARTIFACT (NATIVE OMML) — v1.11.0

Earlier versions built TWO artifacts and delivered the linearized one. That was
the math-destruction defect. The reasoning behind it does not survive scrutiny:

**Fact 1 (historical):** A naive python-docx ROUND-TRIP on a docx containing
`<m:oMath>` can silently corrupt every math element. **But Step 11 does NOT
round-trip through python-docx** — it edits raw `word/document.xml` and re-zips
(Phases 3/5). OMML therefore survives the pipeline byte-perfect, PROVEN by the
integrity artifact every prior version already built and gated (C5: integrity
OMML count == source). There is no corruption to defend against, so there is
nothing to linearize.

**Fact 2:** Native OMML is standard Word math and renders in Word and any
Word-based portal. The student-facing PYQ pipeline (PYQFormat) already delivers
native OMML to end users, so native math is a proven downstream contract.

Therefore v1.11.0 delivers ONE artifact — the **integrity artifact** — carrying
native OMML untouched, with tag blocks inserted and the safety-net header strip
applied. Phase 4's render transforms (Rule 19 linearization, Rule 22 recolor,
Rule 21 safe-font) are RETIRED; no render-source docx is built or delivered.

**The integrity artifact IS the final delivered file (`_Final.docx`). No
`soffice`, no `pdftotext`, no `pypdf`, and no OMML linearization.**

---

# ★ DEFINITION OF DONE

The output Word document is NOT finished until ALL hold:

1. **Output is questions-only before Q.1** — the input should be questions-only
   (Step 7 R8b / G-PREQ1), so `detect_header_paras()` should find ZERO. Any non-blank,
   non-Q-stem paragraph before Q.1 is stripped (output stays questions-only) AND, if the
   count is non-zero, a REGRESSION ALARM is raised in the delivery report (a Step 7 leak
   to fix). v1.10.0: no upstream gate strips these any more — this net is load-bearing.
2. **All tag blocks inserted** — every Q-stem preceded by exactly 5 tag
   paragraphs in order (total_questions tag blocks, count read from blueprint).
3. **Zero content mutation** — no character changed in any question, option, image,
   table, or explanation.
4. **All 17 audit gates pass** (§6) — run before docx delivery. (v1.12.1: said 16; §6 runs C1–C17.)
5. **Math preserved as native OMML** — the delivered docx's `<m:oMath>` count
   equals the source (C5/C11). ZERO linearization (v1.11.0).
6. **Symbols preserved** — every non-ASCII codepoint in the source survives in the
   delivered file with the exact codepoint (no safe-fonting applied; C14).
7. **Tag values are JOIN-verified** — every Subject/Topic/Subtopic/Question Type/
   Complexity value traces to a registry + blueprint JOIN, not to content inference.
8. **Output is a .docx file** — the integrity docx assembled per §5 Phase 5.
9. **`present_files` called** immediately after docx verified — before any other output.
10. **In-chat delivery report** printed after `present_files` (§8).
11. **Opens clean in Microsoft Word** — the delivered docx opens with NO "unreadable
    content / recover?" prompt (v1.3 — final acceptance check, §10 step 13). python-docx
    and LibreOffice are lenient readers and do NOT prove this.

---

# §1 — SESSION START

## S1-1 — Trigger parsing

```
Trigger: TestDeliver P[N] [--level <mock|subject|topic|subtopic>] [--scope <Subject[::Topic]>]
Trigger matching is case-insensitive.

ALIAS (v1.9 — mock-only, working alias, unchanged behaviour):
  MockDeliver M[N]   ==   TestDeliver P[N] --level mock

Parse:
  N        : positive integer — mock/paper number
  LEVEL    : from --level, or 'mock' if the MockDeliver alias was used, else None
             (single-active-default / docx-driven resolution — §5 Phase 1).
  ExamCode : derived from the *_blueprint.json file(s) found in project knowledge
             (v1.9: every [ExamCode]*_blueprint.json, not just one — §5 Phase 1).
             If none found → HARD STOP:
               "No *_blueprint.json found in project knowledge.
                Run MockBlueprint or ScopedBlueprint first and upload
                its blueprint.json to this project."
```

## S1-2 — Preflight (HARD STOP on any failure)

```
1. Verify Solutions docx attached. Accept either:
     [ExamCode]_[paper_slug]_Explanation.docx           (Step 9 output — the input)
     [ExamCode]_[paper_slug]_Explanation_Complete.docx  (LEGACY — pre-v1.10.0 papers
                                                         produced by the retired Step 10;
                                                         still accepted, never produced)
   (v1.9: paper_slug is pp.paper_slug(paper_id) — "Mock[N]" zero-padded for a mock, else
   the scoped slug; parsed from the uploaded filename itself, §5 Phase 1.)
   If neither attached → HARD STOP: "Attach the Solutions docx for [N]."
   (v1.16.0) A [ExamCode]_[paper_slug]_Explain_Report.docx attached alongside is the
   Step-9 report (MockTestExplain S20-R) — IGNORE it; it is never the input and its
   suffix can never match the two accepted names above.

2. Verify the resolved blueprint (§5 Phase 1 — pp.pick_blueprint over every
   [ExamCode]*_blueprint.json in project knowledge, driven by the uploaded docx).
   Read: exam_code, total_questions, sections[], subtopic_list[],
         difficulty_labels, q_types, marking_scheme[] (v1.7 — optional; absent/empty
         is valid and means subtopic-based Question Type resolution, see §3 S3-2a).
   If exam_code missing → HARD STOP.

3. Verify registry.json in project knowledge.
   REGISTRY-HANDOFF-LAW precondition (v1.16.0): this step reads ONLY the project copy.
   Every upstream step that changed the registry delivered it with the "Replace in
   Project Files" badge (Step 7 Final Assembly, Step 9 §7A-M — v1.18.0: the retired
   repair steps no longer write it). If 3b below stops on PENDING although Step 9's
   verdict box said PASSED or DISCLOSED, the operator has NOT replaced the registry
   Step 9 delivered — say so FIRST, in these words, before the re-run command:
     "The project registry does not carry the verdict Step 9 wrote. Replace
      [ExamCode]_registry.json in Project Files with the copy Step 9 delivered,
      then re-run TestDeliver P[N]. If you no longer have it, run: <d['next_step']>."
   Also take the fingerprint BEFORE 3b (pp.registry_fingerprint) — §8 decides from it
   whether a healed registry must be delivered.
   Read: question_index — find the mock N entry.
   v1.12.0 — FIRST run the ledger↔index agreement check over the WHOLE registry:
     claimed = papers_completed ∪ {f"MOCK:M{m:02d}" for m in mocks_completed}
     have    = {entry.paper_id for entry in question_index}
     For every paper in claimed − have, print a named Class-A finding:
       "REGISTRY DATA LOSS: [paper] is recorded complete in the ledger but has
        NO question_index entry — the entry was dropped by a later registry
        write. Its delivery will hard-stop until the paper is recreated via
        Step 7 (the per-question data cannot be recovered)."
   THEN, if no mock N entry in question_index → HARD STOP with the Class-A
   finding above when mock N is in the ledger (data loss — remedy: re-run
   Step 7 for Mock [N]); otherwise:
   3b. DIFFICULTY GATE VERDICT (v1.13.0 — GAP-2026-08-24-DIFFICULTY-GATE-
       BLOCKING; v1.14.0 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER:
       validate first, then branch on the STATE PAIR, all via paper_pipeline
       Cluster DG — never a hand-written branch on one field).
       FIRST:
         rec, disclosure = pp.dg_preflight(reg, paper_id, where='S1-2 3b')
       An illegal (status, repair_rounds_used) pair is healed per DG-INVARIANT
       and disclosure['line'] is printed VERBATIM in chat; the healed registry
       is DELIVERED with the Final docx — Replace in Project Files — per §8 /
       REGISTRY-HANDOFF-LAW (§FOOTER-DG also prints it from rec['migrations']). A DGIllegalState (unknown status) HARD-STOPS with
       its message verbatim. An illegal record must NEVER be silently read as
       one of the branches below.
       THEN:
         d = pp.dg_deliver_decision(reg, paper_id, N, mock=<Mock* trigger>)
       and act on it — d is the verdict, this table is what it encodes:
         absent            → LEGACY paper (pre-gate). Deliver exactly as
                             before — operator decision 2026-08-24.
         ('PENDING',   0)  → HARD STOP: "This paper has not passed the
                             difficulty check. Run: " + d['next_step'] + "
                             then return here."
         ('DISCLOSED', 0)  → PROCEED (v1.18.0 — REPAIR-RETIRED-2026-08-27:
                             the gate was not met and the paper is delivered
                             with disclosure); §FOOTER-DG prints
                             d['footer_lines']: "Measured difficulty: [bottom]
                             n (not gated) · [middle] b/m in window · [top]
                             c/h in window — the difficulty gate was not met;
                             labels are as planned at Step 7." A record still
                             carrying the RETIRED status 'FAILED' never
                             reaches this table: pp.dg_preflight above healed
                             it to this pair and its disclosure line was
                             printed; §FOOTER-DG adds the healed-record line.
         ('PASSED',    0)  → proceed; no extra footer text.
         ('PASSED',    1)  → proceed (LEGACY repaired paper); no extra footer text.
         ('DISCLOSED', 1)  → proceed (LEGACY repaired paper); §FOOTER-DG prints
                             d['footer_lines']: "Measured difficulty: … confirmed
                             after 1 repair round (legacy repair — the repair
                             steps are retired)." (a pre-window record prints
                             plain a/n fractions — DeliveryFooter §FOOTER-DG).
         ('DORMANT',   0)  → PROCEED; §FOOTER-DG prints d['footer_lines']:
                             "Difficulty gate: not applicable to this paper
                              ([dormant_reason]) — labels are as planned at
                              Step 7." NEW in v1.14.0: before this, a dormant
                             gate wrote nothing, the record stayed PENDING and
                             the paper could never be delivered (every scoped
                             paper, every non-3-band exam, every session
                             without blueprint_core).
       These six pairs (plus absent) are the ONLY states pp.DG_LEGAL_STATES
       admits; the
       preflight guarantees no other reaches this table. `bands` is read ONLY
       on DISCLOSED (a PENDING or DORMANT record legitimately carries none —
       schema 2 makes the shape a function of status); dg_footer_lines already
       honours that. d['next_step'] is pp.dg_next_step — the same function
       Step 9 prints from — so the command printed here is one the named step
       accepts.
       The gate reads ONLY the registry — never the chat transcript — so a
       skipped or re-ordered session cannot out-talk the record.

    3c. DIFFICULTY SOURCE LINE (v1.19.0 — GAP-2026-08-29-DIFFICULTY-HARDER-PRESET; §FOOTER-DS).
       Read blueprint.json['difficulty_source'] (Blueprint v1.58.0 S7-0). ONE line,
       printed as the last body line of the delivery footer, so a framework preset, a
       measured mix and an operator choice can never be mistaken for one another:
         mode 'profile_harder'     → "Difficulty mix: measured from [k] sittings
                                      ([cycle labels]), raised 30% by framework preset."
         mode 'profile'            → "Difficulty mix: measured from [k] sittings of
                                      this exam ([cycle labels])."
         mode 'profile_confirmed'  → "Difficulty mix: measured from [k] sittings;
                                      operator-confirmed deviations in [sections]."
                                     ([k] = len(difficulty_source['cycles_used']);
                                      [sections] = the distinct 'section' values of
                                      difficulty_source['overrides_confirmed'], in
                                      paper order.)
         mode 'operator_no_pyq'    → "Difficulty mix: set by operator — no PYQ
                                      profile available for this exam."
         mode 'flag' / 'progressive' → "Difficulty mix: set by operator on the
                                      trigger ([E:M:H | progressive bands])."
         key absent (pre-v1.57.0 blueprint) → print nothing (legacy series).
         (The 30% in the 'profile_harder' line is bc.DP_HARDER_FRAC, printed as a
          whole percentage; the sentence never carries an exam value.)
       Never invent a mode; a value outside this set is a data defect → HARD STOP
       naming blueprint.json.

    3d. STYLE-PROFILE STATUS LINE (v1.20.0 — GAP-2026-08-29-STYLE-FIDELITY §6.7;
       §FOOTER-STYLE). Read the Step-7 style record from the registry
       via pp.style_gate_profile_meta(reg, paper_id) — the ONE reader-side
       accessor, so this step never reaches into the container shape by hand —
       and print EVERY string returned by pp.style_footer_line(style_meta),
       one per line,
       after the §FOOTER-DG lines. The engine is the ONLY source of this line:
         ACTIVE  → "STYLE PROFILE: ACTIVE (schema 1, corpus [hash8])"
         DORMANT → "STYLE PROFILE: DORMANT — [reason]"
         no record (pre-v5.82 paper) → print nothing (legacy series)
       EXACTLY ONE LINE (P-11 / ruling Q15). The per-question style, PYQ-distance
       and item-rule records are internal: they live in the audit dossier and the
       registry `style_gate` container, never in the delivered document. An
       absent record is a legacy paper, NEVER a defect and NEVER a stop — the
       style layer cannot withhold a paper in any state (P-4).

     "registry.json has no question_index entry for Mock [N].
      Run MockCreate for Mock [N] first."

4. Verify question_index[mock_N] has exactly total_questions entries
   with q = 1..total_questions (sorted, unique, complete).
   If mismatch → HARD STOP: report the gap.

5. Verify every question in question_index[mock_N] resolves to an entry in
   blueprint.subtopic_list[] — by subtopic_id when present, else by
   (section, subtopic). If any unresolved → HARD STOP: list the unresolved keys.

6. Defensive-copy the uploaded docx to /home/claude/deliver_work/inputs_safe/.
   (Gate C16(b) needs this pristine pre-edit source to prove the delivered file
   dropped no root namespaces.)

7. (v1.11.0: safe-fonting is RETIRED, so no render-safe font stack is required
   for delivery — the delivered file keeps the input's original fonts. This step
   is now advisory only: if you separately render a preview you may want DejaVu
   Sans / FreeSans installed, but delivery does not depend on it, and soffice,
   pdftotext, pypdf are NOT required.)

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
    # 1. Find THIS paper in question_index. C3: key on paper_id (mock == "MOCK:M{mock_n:02d}",
    #    so this is bit-identical for a mock); tolerant of legacy entries that carry only 'mock'.
    _tp  = next((mk for mk in blueprint.get('mocks', []) if mk.get('mock') == mock_n), None)
    _pid = (_tp or {}).get('paper_id', f"MOCK:M{int(mock_n):02d}")
    qi_entry = next(
        (e for e in registry.get('question_index', [])
         if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") == _pid),
        None
    )
    if qi_entry is None:
        raise SystemExit(
            f"HARD STOP: No question_index entry for paper {_pid} in registry.json.")

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

    # 4. Resolve Question Type — DUAL MODE (v1.7 FIX).
    #
    #    blueprint.marking_scheme[] (Step 2a v2.5+, carried by Step 6 v1.19+; ALSO
    #    inherited by every scoped blueprint per Framework_ScopedBlueprint.md §7) is
    #    exam-wide config, not mock-specific, so this classification is identical and
    #    stable across every mock/paper generated for the same exam.
    #
    #    MODE SELECTION — count of DISTINCT question_type values across marking_scheme:
    #      > 1 distinct type  → POSITION-BASED (e.g. GATE: Q1-24/36-43=MCQ, Q25-31/44-47=
    #                           MSQ, Q32-35/48-65=NAT — the SAME subtopic can legitimately
    #                           land in an MCQ range in one mock and a NAT range in another;
    #                           see EC-13). Question Type is resolved from the Q-NUMBER via
    #                           marking_scheme — EXACTLY the source Step 7's _type_for_q()
    #                           already uses to generate the question. The subtopic's
    #                           answer_type / answer_cardinality are NOT consulted for this
    #                           tag in this mode.
    #      0 or 1 distinct type → SUBTOPIC-BASED (e.g. SSC CGL: every range is MCQ). Also
    #                           covers EVERY scoped blueprint unconditionally: Framework_
    #                           ScopedBlueprint.md §7 deliberately collapses marking_scheme
    #                           to a single [1,Q] MODAL-type range even when the scope
    #                           contains a heterogeneous mix of MCQ/MSQ/NAT subtopics — that
    #                           single range must NOT be treated as authoritative per-Q
    #                           typing, or every scoped-test question would be mistagged
    #                           with the one modal type. Scoped subtopics carry their own
    #                           answer_type/answer_cardinality specifically for this tag
    #                           (Framework_ScopedBlueprint.md S8-1: "Step 11 tagging (mock
    #                           parity)" / "NAT/MSQ fidelity for scoped"). Question Type is
    #                           resolved per-subtopic — BYTE-IDENTICAL to v1.6 output.
    #      Also covers legacy blueprints where marking_scheme is absent (pre-v1.19):
    #      empty list → 0 distinct types → subtopic-based, byte-identical to v1.6.
    bp_marking_scheme = blueprint.get('marking_scheme', [])
    _distinct_q_types = {ms.get('question_type') for ms in bp_marking_scheme
                          if ms.get('question_type')}
    _position_based_typing = len(_distinct_q_types) > 1

    def resolve_question_type_by_subtopic(answer_type, answer_cardinality):
        if answer_type == 'numerical':
            return 'NAT'
        elif answer_cardinality == 'multi':
            return 'MSQ'
        else:
            return 'MCQ'

    def resolve_question_type_by_position(qnum):
        for ms in bp_marking_scheme:
            qr = ms.get('q_range')
            if qr and qr[0] <= qnum <= qr[1]:
                qt = ms.get('question_type')
                if qt:
                    return qt
                break
        raise SystemExit(
            f"HARD STOP: Q{qnum} — Question Type resolution is position_based "
            f"(blueprint.marking_scheme has {sorted(_distinct_q_types)} across its "
            f"ranges) but Q{qnum} does not resolve to a usable question_type from any "
            f"marking_scheme q_range. blueprint.marking_scheme is corrupt, stale, or "
            f"does not cover the full paper — fix marking_scheme (or the upstream "
            f"exam_config.json) before re-running Step 11. Step 11 never guesses a "
            f"Question Type tag.")

    def resolve_question_type(qnum, answer_type, answer_cardinality):
        if _position_based_typing:
            return resolve_question_type_by_position(qnum)
        return resolve_question_type_by_subtopic(answer_type, answer_cardinality)

    # 5. Build the per-question lookup
    lookup = {}
    _unresolved = {}   # v1.12.0: q -> stale id, classified after the loop
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
                # v1.12.0: COLLECT, don't fail-fast — the operator needs the full
                # remediation picture in one report, and the old "ensure both are
                # from the same run" message was proven misleading (reference
                # corpus: both files WERE from the same run; the ids were
                # invented at Step-7 write time).
                _unresolved[q] = sid if sid else f"(no id; name_key={name_key})"
                continue

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
                q, st_info['answer_type'], st_info['answer_cardinality']),
            'complexity': difficulty,
        }

    # v1.12.0 — REMEDIATION CLASSIFIER: one hard stop carrying every unresolved
    # question, classified, with the exact remedy per class. W1 output is a
    # ready-to-apply registry patch line; W2/D are NEVER auto-applied.
    if _unresolved:
        import difflib as _dl
        _by_leaf, _all_ids = {}, []
        for _st in blueprint.get('subtopic_list', []):
            _sid2 = _st.get('subtopic_id') or ''
            _all_ids.append(_sid2)
            _by_leaf.setdefault(_sid2.rsplit('.', 1)[-1], []).append(_sid2)
        _lines = []
        for _q in sorted(_unresolved):
            _stale = _unresolved[_q]
            _leaf = str(_stale).rsplit('.', 1)[-1]
            _tg = _by_leaf.get(_leaf, [])
            if len(_tg) == 1:
                _lines.append(f"Q{_q} [W1 — deterministic]: {_stale!r}\n"
                              f"     PATCH registry -> {_tg[0]!r}")
            elif len(_tg) > 1:
                _lines.append(f"Q{_q} [D — AMBIGUOUS, human decision]: {_stale!r}\n"
                              f"     candidates: {sorted(_tg)}")
            else:
                _cand = _dl.get_close_matches(str(_stale), _all_ids, n=3, cutoff=0.5)
                _lines.append(f"Q{_q} [W2 — leaf reworded, HUMAN CONFIRM]: {_stale!r}\n"
                              f"     candidates: {_cand or '(none ≥0.5 — check taxonomy)'}")
        raise SystemExit(
            "HARD STOP (S1-3 JOIN, v1.12.0): " + str(len(_unresolved)) + " question(s) "
            "carry a subtopic_id that is not in blueprint.subtopic_list. Per-question "
            "classification and remedy:\n  " + "\n  ".join(_lines) + "\n"
            "W1 patches are safe to apply mechanically to the registry (then replace the "
            "project registry and re-run this step). W2/D require a human decision — "
            "never auto-apply. If the paper's data is wrong beyond the id, recreate via "
            "Step 7. Root-cause fix: MockTestCreate v5.48.0 S13-4/A-QINDEX prevents these "
            "ids from ever being committed.")
    return lookup
```

---

# §2 — INPUT DOCX STRUCTURE (Solutions document from Step 9)

Understanding the exact structure is mandatory for correct processing.

## S2-1 — Document-level layout

```
[Q.1 first] NO pre-Q.1 header paragraphs — the paper is questions-only from Step 7
           (R8b / G-PREQ1). The FIRST non-blank
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
option clones. All are PRESERVED byte-for-byte in the delivered file (v1.11.0 —
never linearized).

**Section-marker glyphs** (❌ ⬛ ✅ ⚡ and similar) live in the explanation blocks.
They are non-ASCII and are PRESERVED in their original font (v1.11.0 — Rule 21
safe-fonting retired; the input already carries them in a Word-openable file).

---

# §3 — TAG VALUE RESOLUTION (the JOIN engine)

## S3-1 — Tag field definitions

| # | Field | Source | Resolution |
|---|---|---|---|
| 1 | Subject | `blueprint.subtopic_list[].section` | JOIN on subtopic_id or (section, subtopic) |
| 2 | Topic | `blueprint.subtopic_list[].topic` | JOIN on subtopic_id or (section, subtopic) |
| 3 | Subtopic | `blueprint.subtopic_list[].subtopic` | JOIN on subtopic_id or (section, subtopic) |
| 4 | Question Type | Conditional (v1.7) — (a) `blueprint.marking_scheme[]` when it carries >1 distinct `question_type`, resolved by Q-number; (b) otherwise `blueprint.subtopic_list[].answer_type` + `.answer_cardinality`, resolved per subtopic | See S3-2a |
| 5 | Complexity | `registry.question_index[mock_N].questions[q].difficulty` | Canonical label from `difficulty_labels` |

## S3-2 — Question Type resolution

### S3-2a — Resolution mode selection (v1.7)

Question Type resolution is CONDITIONAL on `blueprint.marking_scheme[]`, evaluated
ONCE per paper (marking_scheme is exam-wide, not mock-specific):

| Distinct `question_type` values in `marking_scheme` | Mode | Source |
|---|---|---|
| > 1 (e.g. MCQ + MSQ + NAT) | Position-based | `blueprint.marking_scheme[]` — Q-number looked up against each entry's `q_range` |
| 0 or 1 (absent, empty, or every range the same type — includes ALL scoped blueprints per Framework_ScopedBlueprint.md §7) | Subtopic-based | `blueprint.subtopic_list[].answer_type` + `.answer_cardinality`, per S3-2b |

When position-based: for question number `q`, scan `marking_scheme[]` for the
entry whose `q_range = [start, end]` satisfies `start <= q <= end`, and return
that entry's `question_type`. The subtopic's `answer_type` / `answer_cardinality`
are IGNORED for this tag in this mode. If no entry covers `q` (or the matching
entry has no usable `question_type`) → HARD STOP (marking_scheme does not fully
cover the paper — a data-integrity fault, never silently guessed).

When subtopic-based: use S3-2b, unchanged from v1.6.

### S3-2b — Subtopic-based resolution table (used when NOT position-based)

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
    # v1.8: retired-format legacy marker. Pre-explain_engine.py-v1.16 documents rendered a
    # SEPARATE 'Accepted Range: lo-hi' paragraph for a NAT tolerance band; that format was
    # replaced by folding the range directly into the SAME 'Correct Answer: lo-hi' line
    # (explain_engine.py v1.16 — see C17 above), so this pattern will never match a
    # freshly-generated document and is kept only for any older mid-pipeline document that
    # predates the fix. 'Correct Answer' above already covers the current format.
    r'^Accepted\s+Range',
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

Retained UNCHANGED from v1.0. Since Step 7 (R8b / G-PREQ1)
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
import paper_pipeline as pp

# ── Session variables (set from trigger and uploaded file) ──
N = MOCK_NUMBER                 # integer from "MockDeliver M[N]" / "TestDeliver P[N]"
src_path = UPLOADED_FILE_PATH   # path to the attached Solutions docx

os.makedirs('/home/claude/deliver_work/inputs_safe', exist_ok=True)
os.makedirs('/home/claude/deliver_work/out', exist_ok=True)

# Load registry.json from project knowledge (still exactly ONE per ExamCode/project —
# the registry is the single shared ledger across mock AND every scoped tier).
reg_matches = [f'/mnt/project/{f}' for f in os.listdir('/mnt/project/')
               if f.endswith('_registry.json')]
if not reg_matches:
    raise SystemExit("HARD STOP: No *_registry.json in project knowledge.")
if len(reg_matches) > 1:
    raise SystemExit(
        f"HARD STOP: Multiple registry files found: {reg_matches}\n"
        f"Only one [ExamCode]_registry.json should exist per project.")
registry = json.load(open(reg_matches[0], encoding='utf-8'))
# v1.16.0 (REGISTRY-HANDOFF-LAW): fingerprint the PROJECT copy before any preflight can
# heal it; §8 decides from this whether a healed registry must be delivered (Replace).
_reg_fp_loaded = pp.registry_fingerprint(registry)

# BLUEPRINT DISCOVERY (v1.9, paper_pipeline.py): load EVERY *_blueprint.json present — the
# mock blueprint AND any scoped ([ExamCode]_[SCOPETAG]_blueprint.json) blueprints. No
# collision HARD STOP here: multiple blueprint files is the NORMAL state once any scoped
# tier has been generated alongside the mock series. pp.pick_blueprint (below) selects
# the ONE this delivery is actually for, driven by the uploaded docx.
bp_matches = [f'/mnt/project/{f}' for f in os.listdir('/mnt/project/')
              if f.endswith('_blueprint.json')]
if not bp_matches:
    raise SystemExit("HARD STOP: No *_blueprint.json in project knowledge. "
                     "Run MockBlueprint or ScopedBlueprint first.")
blueprints = [json.load(open(p, encoding='utf-8')) for p in bp_matches]
_exam_codes = {b['exam_code'] for b in blueprints}
if len(_exam_codes) > 1:
    raise SystemExit(
        f"HARD STOP: blueprint files disagree on exam_code: {_exam_codes}\n"
        f"Only one ExamCode's files should exist per project.")
EXAM = next(iter(_exam_codes))

# v1.9: derive paper_slug from the UPLOADED filename itself (accepts the Step-9 name and
# the legacy _Complete name), then let pp.pick_blueprint identify WHICH blueprint (mock or
# scoped) produced it — cross-checked against --level if given.
_uploaded_name = os.path.basename(src_path)
_slug_m = re.match(rf'^{re.escape(EXAM)}_(.+)_Explanation(?:_Complete)?\.docx$', _uploaded_name)
if not _slug_m:
    raise SystemExit(f"HARD STOP: could not parse a paper_slug from the uploaded filename "
                     f"{_uploaded_name!r}. Expected [ExamCode]_[paper_slug]_Explanation.docx "
                     f"or [ExamCode]_[paper_slug]_Explanation_Complete.docx.")
docx_slug = _slug_m.group(1)

try:
    blueprint = pp.pick_blueprint(blueprints, level=LEVEL, docx_slug=docx_slug)
except pp.PickError as e:
    raise SystemExit(f"HARD STOP: {e}")

safe_path = f'/home/claude/deliver_work/inputs_safe/{docx_slug}_src.docx'
shutil.copy(src_path, safe_path)
src_path = safe_path

# C3 (v1.9): paper identity for deliverable naming. paper_slug is ALWAYS pp.paper_slug —
# "Mock[N]" ZERO-PADDED for a mock, else the scoped slug. Fallback "MOCK:M{N:02d}" for pre-C1.
_tp = next((mk for mk in blueprint.get('mocks', []) if mk.get('mock') == N), None)
paper_id   = (_tp or {}).get('paper_id', f"MOCK:M{N:02d}")
paper_slug = pp.paper_slug(paper_id)
if paper_slug != docx_slug:
    raise SystemExit(f"HARD STOP: uploaded docx paper_slug {docx_slug!r} does not match "
                     f"blueprint mock/paper {N}'s paper_slug {paper_slug!r}.")
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
integrity_path = f'/home/claude/deliver_work/out/{EXAM}_{paper_slug}_integrity.docx'  # C3

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

## Phase 4 — Prepare the delivered tree (v1.11.0 — render transforms RETIRED)

```python
import copy

_M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

# v1.11.0: the delivered file is the INTEGRITY artifact with NATIVE OMML.
# No linearization (Rule 19), no underline recolor (Rule 22), no safe-font
# (Rule 21). render_root is an UNTRANSFORMED copy of the integrity tree, so
# Phase 5's existing assembly delivers native math unchanged.
render_root = copy.deepcopy(root)

# OMML is PRESERVED, not linearized. Counts below are for the delivery report
# and gate C11 (which now asserts preservation, not elimination).
omml_count = len(render_root.findall(f'.//{{{_M_NS}}}oMath'))   # == source (C5/C11)
linearized_strings = []   # nothing linearized
recolored_count = 0       # Rule 22 retired
runs_split, unresolved = 0, []   # Rule 21 retired
```

## Phase 5 — Assemble and deliver the docx (native OMML preserved)

⚠️ **v1.3 / FIX 1 + FIX 3 applied below** (same as Phase 3). This is the
DELIVERED file. v1.11.0: `render_root` is the untransformed integrity tree, so
this assembly ships native OMML.

```python
render_out_path = f'/home/claude/deliver_work/out/{EXAM}_{paper_slug}_Final.docx'  # C3
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
            f'/mnt/user-data/outputs/{EXAM}_{paper_slug}_Final.docx')  # C3
```

**The integrity artifact (native OMML) IS the final delivered file. No `soffice`
conversion is performed.**

---

# §6 — VALIDATION CHECKLIST (all 17 must PASS)

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

**Docx math/symbol gate — delivered docx (after Phase 5 assembly; v1.11.0):**

**C11** Math PRESERVATION (INVERTED, v1.11.0): the delivered `document.xml`
`<m:oMath>` count == `<m:oMath>` count from C5 (== source). `omml_count` from
Phase 4 equals that count and `linearized_strings` is empty. ZERO linearization;
NO `<m:oMath>` was replaced by text. A shortfall is a HARD STOP — it means math
was lost.

**C12** Delivered docx opens as a valid ZIP; `document.xml` parses without error.

**C13** Text conservation in the delivered docx: every `Q.N` (N=1..total_questions)
present; total_questions occurrences each of `Subject:`, `Topic:`, `Subtopic:`,
`Question Type:`, `Complexity:`; `Correct Answer:` count matches source; zero
header paragraphs.

**C14** Symbol + math round-trip (v1.11.0): every non-ASCII codepoint present in
the source body appears in the delivered file with the **exact codepoint**, AND
native math subtrees are byte-identical to the source (no `<m:t>` math text
altered, no OMML replaced by `<w:t>` runs). No Unicode linearization is expected
or permitted.

**C15** No stray recolor (v1.11.0, repurposed): the delivered docx introduces NO
colour change vs source — no FF0000 recolor is applied to any run; NAVY `003366`
Correct Answer colour count unchanged. (Rule 22 is retired; this gate now asserts
colours were left alone.)

**Docx namespace/reference/order integrity gate — delivered docx (v1.3):**

**C16** Namespace + reference + tag-order integrity (FIX 5). Run on the DELIVERED
docx. Needs the pristine pre-edit source from `inputs_safe/` for C16(b).

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

**Portal grading-value charset gate — delivered docx (v1.8, last-mile defense-in-depth):**

**C17** NAT Correct-Answer portal charset (part of the same defect chain as
Framework_MockTestCreate.md v5.25/v5.26 and explain_engine.py v1.16/v1.17). Runs on the
FINAL DELIVERED docx, immediately before `present_files` — the last possible check before
the artifact reaches the upload-ready state. For every question whose `tag_lookup[q]
['question_type'] == 'NAT'` (the SAME resolved type already used for that question's
Question Type tag — never re-derived a second time), the rendered `Correct Answer:` value
MUST match the delivery portal's grading charset exactly: `0123456789.-` and nothing
else, either a plain number (`-?\d+(\.\d+)?`) or a `lo-hi` range with both bounds
non-negative. A numeric-labeled MCQ's `Correct Answer: 3` is legitimately
charset-identical to a NAT value and is correctly NOT checked here (scoped by
`question_type`, not by pattern-matching the value, which would be ambiguous); an MSQ's
`Correct Answer: 2, 4` is a different field entirely and is also correctly out of scope.
Any violation → HARD STOP (this is the LAST gate; there is no later step to catch it).

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


_NAT_CHARSET_ALLOWED = frozenset('0123456789.-')
_NAT_POINT_RE = re.compile(r'^-?\d+(?:\.\d+)?$')
_NAT_RANGE_RE = re.compile(r'^\d+(?:\.\d+)?-\d+(?:\.\d+)?$')

def gate_c17_natcharset(out_docx, tag_lookup):
    """C17 — NAT portal grading-value charset (v1.8, last-mile defense-in-depth).
    Independently re-validates every NAT question's rendered Correct-Answer VALUE
    against the delivery portal's grading charset ('0123456789.-' only), reading
    the FINAL DELIVERED docx directly — the last check before present_files.
    Uses tag_lookup's ALREADY-RESOLVED question_type (never re-derived a second
    time — anti-drift, single source of truth) to scope the check to NAT
    questions only: a numeric-labeled MCQ's 'Correct Answer: 3' is legitimately
    charset-identical to a NAT point value, and an MSQ's 'Correct Answer: 2, 4'
    is a different field entirely — pattern-matching the value alone cannot
    distinguish these, only question_type can."""
    with zipfile.ZipFile(out_docx) as z:
        root = etree.fromstring(z.read('word/document.xml'))
    cur_q = None
    bad = []
    for p in root.iter(f'{{{W}}}p'):
        txt = ''.join(t.text or '' for t in p.iter(f'{{{W}}}t')).strip()
        qm = Q_STEM_RE.match(txt)
        if qm:
            cur_q = int(qm.group(1))
            continue
        if cur_q is None or not txt.startswith('Correct Answer:'):
            continue
        if tag_lookup.get(cur_q, {}).get('question_type') != 'NAT':
            continue
        val = txt[len('Correct Answer:'):].strip()
        bad_chars = sorted(set(val) - _NAT_CHARSET_ALLOWED)
        if bad_chars:
            bad.append(f'Q{cur_q}: {val!r} has banned character(s) {bad_chars}')
        elif not (_NAT_POINT_RE.match(val) or _NAT_RANGE_RE.match(val)):
            bad.append(f'Q{cur_q}: {val!r} is not a well-formed plain number or lo-hi range')
    return (len(bad) == 0, {'bad': bad})
```

Any C16 or C17 FAIL → HARD STOP (fix and re-run).

**Optional stronger gate — OOXML XSD validation (recommended for a 200-exam guarantee):**
If the OOXML `wml.xsd` schema set is available in the environment, validate the
delivered `word/document.xml` against it with `lxml.etree.XMLSchema`. A schema
failure is a HARD STOP. This catches element-order and structural violations that the
targeted gates above may not enumerate. If the XSD is not present, skip (do not block),
and rely on C16 + the mandatory Word open (§10 step 13).

---

# §7 — RULE IMPLEMENTATIONS (RETIRED v1.11.0 — kept for reference only)

**RETIRED (v1.11.0).** Rules 19, 22, and 21 are NO LONGER APPLIED to the delivered
file. The delivered file is the integrity artifact with native OMML and the
input's original fonts/colours (Phase 4). These helper definitions are retained
only so historical references to `replace_omath_with_text`, `recolor_underlined_stems`,
`apply_symbol_safe_font`, and Rule 19/21/22 continue to resolve, and so an operator
who wants the optional "Option B" variant (native OMML + red-underline emphasis)
can reinstate Rule 22 selectively. Do NOT call them in the standard delivery path.

## Rule 19 — OMML → Selectable Unicode Text — RETIRED

RETIRED (v1.11.0). Operated on the render-source deepcopy only. Never applied now.

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

Output file: `[ExamCode]_Mock[N]_Final.docx`
Output path: `/mnt/user-data/outputs/[ExamCode]_Mock[N]_Final.docx`

`present_files` is called immediately after all 17 checklist gates pass, with the
CLOSED SET (v1.16.0 — REGISTRY-HANDOFF-LAW, paper_pipeline Cluster RH):

```python
import os, json, shutil
import paper_pipeline as pp
# _reg_fp_loaded was taken in Phase 1 immediately after `registry` was loaded, BEFORE
# S1-2 3b's pp.dg_preflight could heal the record.
_final_name = f'{EXAM}_{paper_slug}_Final.docx'
_reg_name   = f'{EXAM}_registry.json'
HANDOFF = pp.handoff_set('TestDeliver', primary_docx=_final_name, reg_name=_reg_name,
                         registry_changed=pp.registry_changed(_reg_fp_loaded, registry), final=True)
if HANDOFF['registry_delivered']:          # the ONE case Step 11 changes the registry: a heal
    json.dump(registry, open(f'/home/claude/{_reg_name}', 'w', encoding='utf-8'),
              indent=2, ensure_ascii=False)
    shutil.copy(f'/home/claude/{_reg_name}', f'/mnt/user-data/outputs/{_reg_name}')
_v = pp.verify_handoff_outputs(os.listdir('/mnt/user-data/outputs'), HANDOFF)
if not _v['ok']:
    raise SystemExit(f"HARD STOP (§8): outputs != closed set — missing {_v['missing']}, "
                     f"stray {_v['stray']}. Do NOT call present_files.")
for _line in pp.handoff_footer_lines(HANDOFF):
    print(_line)
```
Then present_files([f'/mnt/user-data/outputs/{n}' for n in HANDOFF['files']]) — ONE
call: the Final docx, plus registry.json ONLY when the preflight healed it. No other
file is ever presented.

**In-chat delivery report (printed after `present_files`):**

```
MockDeliver M[N] — Delivery Report
=====================================
Exam         : [ExamCode] ([exam_name])
Mock         : [N]
Checklist    : C1–C17 all PASS

Questions tagged  : [total_questions] / [total_questions]
Headers stripped  : [count]  (expected 0 — input is questions-only per Step 7)
Header regression : none      (or: ⚠ REGRESSION ALARM — [count] pre-Q.1 paragraph(s)
                               were present and stripped. The Complete/Solutions docx
                               should be questions-only (Step 7 R8b/G-PREQ1).
                               Re-run Step 7 on the upstream paper.)

OMML preserved (native)  : [count]  (== source; ZERO linearized — v1.11.0)
Non-ASCII codepoints     : [count] unique; all preserved with exact codepoint
Runs re-fonted (R21)     : 0  (Rule 21 retired — safe-fonting not applied)
Stem-underline recolor (R22): 0  (Rule 22 retired — no recolor applied)
Content edits            : tag blocks inserted + safety-net header strip ONLY

Namespace/reference (C16): superset OK · mc:Ignorable covered · 0 dangling refs · tag order OK

Tag summary:
  Complexity distribution:
    [label1]: [count] Q
    [label2]: [count] Q
    [label3]: [count] Q

  Question Type distribution:
    [type1]: [count] Q
    [type2]: [count] Q  (if multiple types exist)
  Type resolution mode (v1.7): [position_based | subtopic_based]
    (position_based: marking_scheme has >1 distinct type — subtopic_based: 0 or 1,
     always true for scoped tests)

  Subject distribution:
    [Section1] ([count]): [Subtopic1: N, Subtopic2: N, ...]
    [Section2] ([count]): [Subtopic1: N, Subtopic2: N, ...]
    ...

Output: [ExamCode]_Mock[N]_Final.docx
```

**Post-delivery footer (MANDATORY after present_files):**
After the present_files call and in-chat delivery report above, render the standardized
visual delivery footer as the LAST element in the response. Follow Framework_DeliveryFooter.md
for footer type (F2 step-complete — always for Step 11), file badges
(pp.handoff_footer_lines(HANDOFF) verbatim: Use locally for Final.docx; Replace in Project
Files for registry.json when a heal delivered it), and next-step reference. Step 11 uses the special bottom text:
"Pipeline complete for [ExamCode] Mock [N]. Thank you!" (last step — no next step).
For the next mock: "Step 7: MockCreate M[N+1]".

---

# §9 — EDGE CASES

## EC-1 — Solutions docx is questions-only (the guaranteed, normal case)

Since Step 7 (R8b / G-PREQ1) never emits a pre-Q.1 block, the Solutions docx starts
directly with Q.1. `detect_header_paras()`
returns an empty list, nothing is stripped, and C4 passes (zero detected, zero remain).
This is the expected case for every mock produced by the current pipeline; the delivery
report reads "Headers stripped: 0" and "Header regression: none".

## EC-2 — Solutions docx has pre-Q.1 header paragraphs (UPSTREAM REGRESSION — safety-net)

This should NOT occur: Step 7 R8b / G-PREQ1 guarantees a questions-only paper. If a
title/info/scoring block nonetheless appears before Q.1, it is an upstream regression (a
Step 7 generator leak). v1.10.0: the Step-8 A-HEADER backstop that used to catch such a
leak before it reached here no longer exists, so this net is the only one left. The
safety-net `detect_header_paras()` still removes it (the delivered Final.docx stays
questions-only) and C4 verifies removal, but the delivery report raises a REGRESSION ALARM
naming the count so the upstream Step 7 run can be fixed. Never silently absorb it as if
it were normal — Step 11 delivers correctly AND surfaces the leak.

## EC-3 — Exam with MSQ questions

Some questions may have `Question Type: MSQ`. Resolution depends on mode (S3-2a):
  - **Position-based** (marking_scheme has >1 distinct type, e.g. GATE): a question
    is `MSQ` if its Q-number falls inside an MSQ `q_range` in `marking_scheme`,
    regardless of the subtopic's `answer_cardinality`.
  - **Subtopic-based** (everything else, including scoped tests): resolved from
    `blueprint.subtopic_list[].answer_cardinality == 'multi'`, as in v1.6.
No special handling elsewhere in the tagging pipeline — the tag value is simply
`MSQ` instead of `MCQ`.

## EC-4 — Exam with NAT questions

Some questions may have `Question Type: NAT`. Resolution depends on mode (S3-2a):
  - **Position-based**: a question is `NAT` if its Q-number falls inside a NAT
    `q_range` in `marking_scheme`, regardless of the subtopic's `answer_type`.
  - **Subtopic-based**: resolved from `blueprint.subtopic_list[].answer_type ==
    'numerical'`, as in v1.6.
NAT questions may have different option structures (no option lines, or a single
answer field). The tagging pipeline does not inspect option structure — it only
inserts tags.

## EC-5 — Zero OMML in source docx

If the Solutions docx has no `<m:oMath>` elements (pure text exam), `omml_count`
(Phase 4) is 0. C5 passes (0 == 0). C11 passes (0 preserved == 0 source; nothing
linearized). C14 is trivially satisfied. (v1.11.0: no linearization is performed
in any case.)

## EC-6 — Missing question_index for mock N

If `registry.question_index` has no entry for mock N, Step 11 halts at S1-2
step 3. The user must run Step 7 for mock N first. Step 11 never
guesses or infers tag values from content.

## EC-7 — Subtopic mismatch between registry and blueprint

If a question cannot be JOINed to `blueprint.subtopic_list[]` by subtopic_id OR by
(section, subtopic), Step 11 halts at S1-3 (`build_tag_lookup`). This indicates a
registry/blueprint version mismatch. The user must ensure both files are from the
same pipeline run.

## EC-8 — Difficulty label not in canonical set

If any question's `difficulty` value is not in `blueprint.difficulty_labels`,
Step 11 halts at S1-3. This indicates a registry corruption. The user must
re-run Step 7.

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

## EC-13 — Position-based exam where subtopic-level type disagrees with position-level type (v1.7)

When `blueprint.marking_scheme[]` carries >1 distinct `question_type` (position-based
mode, S3-2a), the same subtopic may have `answer_type='numerical'` or
`answer_cardinality='multi'` (from Step 5 PYQ whole-subtopic majority voting) while
being assigned by Step 6 to an MCQ Q-range in this particular mock — or the reverse.
This is NORMAL and EXPECTED, not an error: `marking_scheme` is authoritative for the
Question Type tag in position-based mode, and the subtopic-level `answer_type` /
`answer_cardinality` fields are statistical artifacts of PYQ observation (used
elsewhere for allocation and axis scheduling) that do not constrain, and are not
constrained by, which Q-position a subtopic lands on in any given mock. Step 11 never
uses subtopic-level `answer_type` / `answer_cardinality` for the Question Type tag
when in position-based mode. No warning is logged; this is not a data-quality signal.

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
8. ☐ Phase 4 (v1.11.0): deepcopy integrity tree → render_root UNTRANSFORMED.
     Rules 19/22/21 RETIRED — NOT applied. Compute omml_count (== source) for the
     report; linearized_strings=[], recolored_count=0.
9. ☐ Phase 5: assemble the docx ZIP from render_root (native OMML) (KEEP
     webSettings.xml — FIX 3; NO cleanup_namespaces — FIX 1). Copy to
     `/mnt/user-data/outputs/[ExamCode]_Mock[N]_Final.docx`.
10. ☐ Run docx gate C11–C17 on the DELIVERED docx (C11 = OMML PRESERVED: delivered
     count == source, v1.11.0; C16 = namespace + reference + tag-order integrity,
     needs the inputs_safe/ source for C16(b); C17 = NAT portal grading-value
     charset, needs `tag_lookup` — already built at Preflight, never re-derived).
     Optionally validate document.xml against the OOXML wml.xsd if present. Any
     FAIL → HARD STOP, fix and re-run.
11. ☐ `present_files([output_path])`.
12. ☐ Print delivery report (§8).
13. ☐ FINAL ACCEPTANCE (mandatory, at least for the FIRST mock of each exam): open
     the delivered docx in Microsoft Word ONCE. It MUST open with NO "unreadable
     content / recover?" prompt. python-docx and LibreOffice are lenient readers that
     accept namespace-broken files Word rejects — they do NOT substitute for this check.

---

*End of Framework_MockDeliver (body) — version is declared once, in the header and the closing sentinel.*

*Four hard invariants: (1) NEVER linearize OMML — deliver native `<m:oMath>`
byte-for-byte; the delivered docx's OMML count MUST equal the source (gates
C5/C11), and no `<m:oMath>` is ever replaced by a `<w:t>` run (v1.11.0); (2)
every equation in the delivered docx is the source's own native OMML, unchanged —
verified by the C11 count-equality and C14 math-subtree check; (3) every tag value
must trace to a registry + blueprint JOIN — Step 11 never infers Subject/Topic/
Subtopic/Question Type/Complexity from question content; (4) never drop or reorder
the document root's namespace declarations, and never let mc:Ignorable name a
prefix that is not declared — do NOT run etree.cleanup_namespaces() on a Word
document; validate with gate C16 and confirm in Microsoft Word itself (python-docx
/ LibreOffice accept namespace-broken files that Word rejects).*

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

# END OF Framework_MockDeliver v1.20.0
