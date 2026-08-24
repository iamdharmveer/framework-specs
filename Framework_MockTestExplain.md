# Framework_MockTestExplain v1.40.0
# v1.40.0 — 2026-08-24 — GAP-2026-08-24-STEP9-AUDIT-R1 (spec-only; no engine, gate-count,
#   schema or artefact-shape change; zero exam values). Full-line audit of v1.39.0 against
#   the routed engines, Step 7, Step 11 and PYQExplain. THREE run-breaking defects:
#   (1) S19-1 check 4 scanned the Solutions docx ITSELF for the BANNED substrings, so any
#   scoped slug or exam code containing 'state'/'answer'/'key'/'source'/'progress' (e.g.
#   TOPIC_…_SOLID_STATE_01) HARD-STOPPED every delivery — PYQExplain already excluded its
#   expected files; Step 9 now scans present − {sol}. (2) §17-3(b) told Step 9 to write a
#   PLAINTEXT key_corrections.json "which MockDeliver reads": MockDeliver has no reader
#   (it preserves the docx 'Correct Answer:' line verbatim, C17 charset only), the file is
#   banned by S19-1 checks 4 and 5, and it re-created the plaintext key the v1.37.0 hashing
#   design removed. Dropped; RESOLVED_SOURCE now lives in progress.json + §R10 with an
#   operator EX-rule prompt. (3) P3 typed mcq/msq/nat from per-subtopic section_rules only,
#   while Step 7 v5.30 / Step 11 v1.7 / audit_canonical v2.9 switch to POSITION-BASED
#   typing from marking_scheme when it declares >1 question_type — on such an exam every
#   MSQ-range question was typed mcq. P3 now applies the same mode rule.
#   DRIFT (each verified against the live engine): §13-2b named paper_pipeline.
#   canonical_structure (lives in explain_engine; 'rdkit_unavailable' path now specified);
#   MANDATE A / P1 / S0-1 allowed explain_engine.py from /mnt/project (engines are REPO-ONLY,
#   sha256-verified — fallback removed); §16-2 still asserted a live Step 10 (retired
#   v1.21.0); S7-4 claimed byte-identity with two copies that differ in docstrings (logic
#   verified identical on 19 edge inputs — reworded to logic-identical); S0-2 / MANDATE 0 /
#   P2 named the output Mock[N] where S19 uses [paper_slug]; §18-1 cited 'Step8_source' and
#   '(§13)' for the §11 degrade ledger; §6A-3 / §R3 omitted CONFORMER from the visual
#   verdicts the engine enforces; §6A-6 sent renderer preflight to 'P0' (trigger detection)
#   — now an explicit P1 sub-step with its dashboard line, plus the §7A-M line P2 lacked;
#   S19-1 gated on SELF_AUDIT_CLEAN / COVERAGE_OK that nothing set — S4-4 D now sets them;
#   §21 items 16/19/17/18 renumbered. Superseded v1.38.0 entry moved verbatim to
#   SPEC_HISTORY.md (EC-P42).
# v1.39.0 — 2026-08-22 — GAP-2026-08-22-STEP9-READ-SET (EC-P42; deploy follow-up #2
#   of 2026.08.21.2). New S0-3: FINAL vs NON-FINAL session class with a GENERATED
#   read set — a NON-FINAL batch session skips §20 (end-of-mock report), §22 (its
#   §R9 disclosure input) and APPENDIX A; escalation to a full read is mandatory and
#   one-way before §20 runs. §20–§24, APPENDIX A and FOOTER banners promoted from
#   '# ' to '## ' so spec_sections.py can address their spans (IDs unchanged; no
#   consumer reads header levels — verified by corpus grep). Ranges live in
#   SPEC_SECTIONS.json (has_read_set), hash-tracked, never hand-copied. The
#   MockExplain/TestExplain route is now budget-covered by design, not by headroom.
# ════════════════════════════════════════════════════════════════════════
# §0 — INPUT / OUTPUT CONTRACT (read before anything else)
# ════════════════════════════════════════════════════════════════════════

## S0-1 — INPUTS (what Step 9 is given)

  DELIVERED BY STEP 7 (the closed set; both already in the [ExamCode] project):
    1. [ExamCode]_Mock[N]_Create.docx     — the paper to explain, exactly as Step 7
                                            assembled and self-audited it
    2. [ExamCode]_registry.json           — FROZEN; read for figural_manifests[] /
                                            rc_manifests[] cross-checks + dedup context +
                                            options_by_q[str(N)] (v1.3: per-question expected
                                            option count, 0=NAT — the mandatory question-type
                                            wiring; see P3) + v1.37.0: key_commitments[paper_id]
                                            (salted HASHES of Step 7's canonical answers — §7-8;
                                            never a plaintext key) + figural_manifests[]
                                            .semantic_objects (what each generated figure
                                            DEPICTS, machine-readable — §13-2b)

  ALREADY IN PROJECT KNOWLEDGE (from the PYQ-phase steps; required):
    3. [ExamCode]_section_rules.md        — per-subtopic rules + CATEGORY-C exam params
    4. [ExamCode]_blueprint.json          — sections[], q_range[], options-count, difficulty
    5. [ExamCode]_subtopic_manifest.json  — subtopic_id ↔ name + mandate/alternation data
    6. explain_engine.py                  — the universal explanation engine, taken ONLY
                                            from the Step-0 verified clone (MANDATORY —
                                            MANDATE A; never from project Files)

  NOT DELIVERED (Step 9 must do without these — by design):
    ✗ any answer key. Step 7 holds a key internally and never delivers it.
       Step 9 re-derives all answers independently (§7), THEN reconciles its
       derived answers against Step 7's hash commitments (§7-8, v1.37.0).
    ✗ internal Step-7 sidecars (answer_key.json, concept_map, audit ledger).
       The figural/RC maps Step 9 needs are in registry.json and re-extracted at P3.

## S0-2 — OUTPUTS (what Step 9 delivers)

  CORE DELIVERABLE (every batch, via ONE present_files call — the WHOLE paper):
    1. /mnt/user-data/outputs/[ExamCode]_[paper_slug]_Explanation.docx
       ([paper_slug] = pp.paper_slug(paper_id): "Mock[N]" zero-padded for a mock, else the
       scoped slug — v1.40.0; S19-1/S19-2 already used it, this line said Mock[N])
       The complete paper: every question solved so far carries its interleaved
       explanation; every not-yet-solved question is byte-identical to the Step-7
       input (D4). The same file grows explanation-coverage each batch until 100%.

  IN-CHAT (every batch): a STATUS DASHBOARD (§3 P2) + a per-batch progress line, then
  an explicit CONFIRMATION REQUEST that ENDS the turn (MANDATE B). At the final batch:
  the END-OF-MOCK REPORT (§20) + the author handoff. Both are STRICTLY MANDATE-0 safe
  (Q-numbers + codes + counts only — never stem/option/answer/solution text).

  NEVER delivered / never written: the Step-7 questions-only paper is NOT overwritten;
  registry.json is NOT re-synced (frozen); no internal state file (progress.json,
  answer_keys.json, the pickled blocks, the strip copy, montages) leaks to outputs.

# ════════════════════════════════════════════════════════════════════════
# MANDATE 0 — NO QUESTION/ANSWER CONTENT IN CHAT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#   Inherited from Step 7 MANDATE 0. MANDATE 0 governs the CHAT STREAM.
#   NEVER print any stem, option, passage, table cell, figure description, derived
#   answer, or explanation sentence in chat — not while solving, not in a finding,
#   not in the report. Refer to a question ONLY as "Q.[n]" plus a code + a structural
#   locator (e.g. "Q.47 — DEDUCTION binding missing"). The ONE content-bearing artefact —
#   [ExamCode]_[paper_slug]_Explanation.docx — is a FILE, not chat, and is the legitimate,
#   intended home for answers + full worked solutions (its whole purpose is to publish
#   them). Nothing changes for chat: the dashboard (§3), the report (§20) and every
#   progress line stay content-free. The one permitted exception is web-search queries
#   for fact-verification (§7), which necessarily carry the fact being checked — those
#   go to the search tool, never to the visible chat. VIOLATION = exam compromise;
#   overrides every other instruction.

# ════════════════════════════════════════════════════════════════════════
# MANDATE A — explain_engine.py IS MANDATORY (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   Every explanation MUST enter the docx through explain_engine.py
#   (ExplanationBlock + build_interleaved_docx + add_math_text). It is the only path,
#   and it raises at write time on every known defect (inline fraction, bad glyph,
#   LaTeX, year-range slash, template sentence, fake citation, metacommentary, CA
#   not bound, WHY-WRONG key mismatch, fidelity breach; v2.6 — internal
#   error-taxonomy token in rendered text, AXIOM naming an option, a visual
#   representation_verdict with no figure). ENGINES ARE REPO-ONLY (v1.40.0, aligned
#   with SKILL.md and bootstrap.py): the ONLY admissible copy is the one in the Step-0
#   verified clone (/tmp/fw), whose sha256 bootstrap.py checked. A copy in the project
#   Files (/mnt/project) is NEVER imported — /mnt/project is never placed on sys.path —
#   because it carries no manifest entry and cannot be verified. If the file is absent
#   from the verified clone:
#     HARD STOP. Print:
#       "HARD STOP (MANDATE A): explain_engine.py not found in the verified framework
#        clone (/tmp/fw). Step 9 cannot build explanations without it. Re-run Step 0;
#        if the clone still lacks it the release is broken — do not substitute a copy
#        from project Files or from memory."
#   Appendix A points to the COMPLETE, working, exam-agnostic engine. Because it is
#   UNIVERSAL and byte-identical for every exam, the file keeps the plain neutral name
#   explain_engine.py (NOT exam-prefixed — there is no per-exam variant to
#   disambiguate, and a prefix would falsely imply exam-specificity). It self-tests with `--self-test`
#   (must print "SELF-TEST: N/N PASS" with N >= 62 — FLOOR form, v1.25: the exact
#   62/62 pin HALTed every session once the engine grew to 64 fixtures).

# ════════════════════════════════════════════════════════════════════════
# MANDATE B — BATCH-OR-HALT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#   Explanations are produced in batches of ≤ EXPLAIN_BATCH_SIZE questions (ceiling
#   10 — a CEILING, never a quota; a batch may be smaller). ONE batch per response.
#   Solving, building, or even READING AHEAD beyond the current batch is forbidden.
#   After each batch the run HALTS and asks the author for explicit confirmation; it
#   does NOT proceed until the author replies "continue". There is NO auto-chaining
#   and NO auto-finalise — the final batch also stops and asks before the report.
#   "It is more efficient to finish in one go" is a MALFUNCTION SIGNAL, not a reason:
#   front-loading the whole mock into one context window measurably degrades
#   derivation quality on later questions (the documented decay) — so all-at-once is
#   not merely a process breach, it produces worse answers. The ceiling is enforced
#   four ways, none of which weakens as the mock gets longer (§4, §16): the frozen
#   batch plan, the engine's stage guard (≤ ceiling, no look-ahead), the pre-deliver
#   coverage assertion, and the hard turn boundary. ONE exception, and only one: an
#   ATOMIC LINKED GROUP (RC / cloze / DI / puzzle) is never split — if it would cross
#   the ceiling the batch closes early; a single linked group larger than the ceiling
#   becomes its own batch and may exceed it (atomicity wins — §4).
#   AUTONOMOUS MODE (v1.12 — PACING WAIVER ONLY, RE-0): when the author / a project-
#   memory preference requests non-interactive / "don't pause" execution, the
#   inter-batch HALT is waived and batches run SEQUENTIALLY in one session — but each
#   batch is STILL processed one at a time internally (solve → build → §18 self-audit →
#   coverage assertion → deliver), the per-question derive-twice/web-verify/view review
#   is NEVER collapsed, and the whole-paper coverage assertion still fires per batch. A
#   run that finishes "fast" by skipping the per-question solve/verify is a MANDATE B
#   violation, not a valid autonomous run. Autonomy waives the PAUSE, never the WORK
#   (RE-0). NOTE (v1.21.0): no downstream completion gate re-checks coverage any more —
#   the per-batch coverage assertion here is the ONLY coverage check that will ever run.

# ════════════════════════════════════════════════════════════════════════
# MANDATE D — WHOLE-PAPER EACH BATCH, ONLY AFTER SELF-AUDIT CLEAN (HARD STOP)
# ════════════════════════════════════════════════════════════════════════
#   present_files is FORBIDDEN until the current batch's self-audit (§18) is clean:
#   engine validate() on every block + verify_fidelity (whole paper byte-identical to
#   the Step-7 source) + verify_structure (coverage == exactly this batch's questions,
#   no look-ahead) + math-render check. The delivered file is ALWAYS the complete
#   paper (D4): explained-so-far interleaved + remainder identical to the Step-7
#   input. A fragment containing only the batch's questions must NEVER be presented.
#   /mnt/user-data/outputs holds ONLY the single Solutions docx; the WIP state lives
#   in /home/claude across "continue" turns so nothing is lost.

# ════════════════════════════════════════════════════════════════════════
# THE CORE PRINCIPLE — engine proves shape; discipline alone proves truth (v1.21.0)
# ════════════════════════════════════════════════════════════════════════
#   No code can prove a sentence is TRUE or WELL-TAUGHT — only that it is SHAPED
#   right. So the guarantees are split, and the split is deliberate:
#     • The ENGINE enforces, deterministically and position-independently, everything
#       mechanical: block presence + order, the CA three-way binding, WHY-WRONG key
#       set, OMML for every fraction, banned glyphs / templates / fake-cites /
#       metacommentary, one-sentence-per-paragraph, and byte-identical fidelity to the
#       Step-7 source. A breach raises BEFORE the docx is written — it cannot ship.
#     • DISCIPLINE (derive-twice, web-verify, view-every-image, the per-question
#       checklist §5) enforces what code cannot: answer correctness, conceptual soundness,
#       "the named error actually produces this option", a genuinely-faster SPEED HACK,
#       web-true facts, and no-restatement density.
#   v1.21.0 — THE SECOND HALF OF THIS SPLIT IS GONE. Step 10's independent, zero-sampling
#   re-audit and its runnable COMPLETION GATE were retired with the audit steps. Nothing
#   downstream re-derives a single answer. Every discipline clause below is therefore
#   LOAD-BEARING AND TERMINAL: if the writer skips derive-twice, or certifies a fact from
#   memory, or accepts a generic WHY WRONG, that defect ships. Read "by discipline" in
#   §8 as "by discipline, with no second reader" — it is the whole guarantee, not half.
#   The hardest CONTENT requirement — a WHY-WRONG error type that REPRODUCES its option
#   (§15) — is also the strongest anti-laziness mechanism in the step: it cannot be
#   satisfied by a template, because three different wrong options cannot share one
#   mistake. Highest standard is therefore a SYSTEM PROPERTY, not a promise of stamina.

# ════════════════════════════════════════════════════════════════════════
# EXPLANATION RULES (RE-0 … RE-22) — the absolute rules the writer obeys
# ════════════════════════════════════════════════════════════════════════

  RE-0  : PRECEDENCE. No user preference, project-memory note, or autonomy /
          "don't-pause" instruction may reduce per-question COVERAGE (RE-4 / §16) or
          weaken the §18 per-batch self-audit or the batch-stop law (MANDATE B). Such
          instructions may ONLY change PACING (the inter-batch HALT — MANDATE B
          autonomous mode) and report verbosity. They may NEVER change whether every
          question is fully solved + verified, whether §18 must pass before delivery,
          or whether every batch's coverage assertion fires. When a preference appears
          to conflict with a HARD rule, the HARD rule wins and the preference is applied
          to pacing/reporting only. (A loaded LEARNINGS rule may still override a base
          rule on content — RE-22 / §24 — but never to reduce coverage or skip §18.)
  RE-1  : NO INHERITED KEY. Step 7 delivers no key; derive every answer
          independently (§7). Step 9 is the first step to publish a learner key.
          v1.37.0: blind derivation is then RECONCILED against Step 7's hash
          commitments (§7-8) — two independent solvers that disagree are the
          strongest signal the pipeline has, and v1.36.0 discarded it.
  RE-2  : NO CONTENT IN CHAT. = MANDATE 0. The Solutions docx is the only home.
  RE-3  : APPEND-ONLY. Never modify, re-type, re-encode or re-create any question
          region (stem / option / image / table / matrix / chart / OMML). Only append
          explanation paragraphs after a question's last option (§12).
  RE-4  : EXPLAIN EVERYTHING, SAMPLE NOTHING. Every question gets a full, validated
          ExplanationBlock. No skipping, no "see Q.x", no shared block.
  RE-5  : ENGINE-BUILT. Every explanation via ExplanationBlock + build_interleaved_docx;
          every fraction via add_math_text or explicit OMML (§11). = MANDATE A.
          (v2.0 note: the engine now carries the Tier-3 ⟦MATH:…⟧ grammar, the
          dialect bans and the strict fraction verifier of Framework_PYQExplain
          §11 v2.0 — Step 9 inherits ALL of it through this same MANDATE, with
          zero change to this spec's own rules.)
  RE-6  : DERIVE-TWICE, NEVER GUESS. First principles + a second independent method;
          disagreement → third → 2-of-3 + DERIVATION-CONFIDENCE (§7).
  RE-7  : BATCH-OR-HALT. = MANDATE B. ≤ ceiling, one batch/response, confirm before next
          (interactively; autonomous mode waives the pause only — MANDATE B).
  RE-8  : WHOLE-PAPER INCREMENTAL DELIVERY. = MANDATE D. Each batch ships the full paper
          (explained-so-far + untouched remainder), never a fragment.
  RE-9  : EXAM-AGNOSTIC. Read every exam value from the source files; hardcode nothing.
  RE-10 : LANGUAGE / LABEL / FORMAT-AWARE. Question/option regex, option count (uniform
          OR per-section), option LABEL SCHEME (numeric/alpha/roman/custom), sentence
          TERMINATORS, block labels and markers all come from EngineConfig (section_rules
          CATEGORY C / blueprint), never from this spec. The CA line and "Option" refs
          print the paper's OWN labels (A/B/C, i/ii/iii, …), never a mismatched number.
  RE-11 : VIEW EVERY IMAGE. A figural answer is derived from the VIEWED extracted images,
          never from a manifest (the manifest is a cross-check, not a key — §13).
  RE-12 : ONE DEFENSIBLE ANSWER ASSUMED. Step 7 built one defensible answer; expect
          exactly one defensible answer. A suspicion otherwise is most likely an
          incomplete solve — raise the bar before concluding a defect (§17).
  RE-13 : WHY WRONG DIAGNOSES, NEVER DISMISSES — AND NEVER INVENTS (v1.37.0). Each
          wrong option carries a §9 diagnosis (internal; rendered in natural language,
          never the raw token) in ONE of two modes: a VERIFIED path the engine has
          RECOMPUTED and that reproduces the option, or a DIRECT CONTRADICTION that
          claims no path (§15-2). Hedged provenance is engine-banned. No guess, ever.
  RE-11b: FIGURAL FAMILY IS DECIDED, NOT ASSUMED (v1.29.0). Every figural question is
          classed TRANSFORMATION-PUZZLE or SCIENTIFIC-DIAGRAM before solving (§13-1), and
          read by that family's protocol (§13-4a / §13-4b). A scientific figure read as a
          pose puzzle loses the domain content entirely; when mixed or unclear, read it
          as SCIENTIFIC-DIAGRAM (the stricter reading never damages a puzzle).
  RE-13b: REPRESENTATION IS ROUTED, NOT ASSUMED (v1.27.0). Every question runs the
          §6A router after derivation and before writing. PROSE is the default and a
          visual must EARN its place on the §14 two-part test; the verdict is recorded
          per question and reported (§20). Quantitative steps render as ⟦MATH:⟧ math,
          never as verbalised arithmetic (§11 S11-1c).
  RE-6b : CONDITIONS BEFORE RECALL (v1.32.0). Every condition a remembered result depends
          on is read back from the stem and checked before the result is applied (§7-0a);
          material assumptions are ledgered (§7-0b). A stated condition the DEDUCTION
          never uses is a misread signal, not a spare part.
  RE-6c : NUMERICAL VERIFICATION (v1.32.0). Every quantitative answer passes the §7-5
          checks — units, conversions/kelvin, magnitude, log base, sign, stoichiometry,
          precision — which derive-twice cannot catch because both routes can share one
          silent slip.
  RE-6d : CLAIMS CONSISTENT; ENUMERATE BEFORE FORMULA (v1.35.0). Decisive
          intermediate claims are listed and mutually consistent before writing (§7-6)
          — a right answer with contradictory reasoning is invalid; and a counting
          question is derived inventory-first, a closed-form only after the
          independence it assumes is verified (§7-0c).
  RE-14b: SHORTCUTS ARE SCOPED (v1.32.0). Every SPEED HACK states the conditions under
          which it is safe, inside the shortcut (§14-3b). Unscopable in one clause → OMIT.
  RE-9b : SUPPORTED VALUES ONLY (v1.31.0). Every number traces to the stem, a syllabus
          constant, or a shown derivation (§8-0a). No invented yields, ratios, constants,
          angles or conditions.
  RE-9c : CALIBRATED LANGUAGE (v1.31.0). Absolutes only for claims absolute in the
          subject's own terms; tendencies take calibrated terms (§8-0b). Applies to
          WHY WRONG as much as to AXIOM.
  RE-14 : SPEED HACK ONLY WHEN GENUINELY FASTER. Emit iff a structurally-different route
          reaches the same CA with materially less work; otherwise OMIT — never pad (§14).
  RE-15 : NO TEMPLATES / GLYPHS / FAKE-CITES / METACOMMENTARY / BANNED BLOCKS. Engine-
          enforced at write time; the writer must not even attempt them.
  RE-16 : RESOLVE IN-RUN, NEVER FIX CONTENT, NEVER HALT THE PAPER (v1.37.0). A key
          conflict or figure/object disagreement runs §17-3 INSIDE the session; the paper
          always completes; no key ships that did not survive §17-3; only a PROVEN
          defect (§17-4) is reported for targeted regeneration; the operator never
          adjudicates.
  RE-17 : FIDELITY EVERY BATCH. The whole question region must be byte-identical to the
          Step-7 source, verified after every batch — not once at the end (§12, §18).
  RE-18 : WEB-VERIFY FACTS. Every current-affairs / general-knowledge fact and every factual
          option is web-verified with a recorded source; never certified from memory.
  RE-19 : RESUME-SAFE. All cross-batch state lives in files; "continue" reloads and
          re-verifies the on-disk doc before solving the next batch (§4).
  RE-20 : KINDNESS TO THE READER OF RECORD. The handoff states plainly what was derived,
          what was web-verified, what carries a DERIVATION-CONFIDENCE flag, and what is
          model-derived — so a human reviewer knows where to look hardest. With no audit
          step downstream (v1.21.0) this handoff is the ONLY surviving record of where the
          run was least certain: it is MANDATORY, never abbreviated, never skipped.
  RE-21 : QUESTION-TYPE-AWARE. Resolve each question as mcq / msq / nat from config (§6,
          §3 P3) and shape the block accordingly: mcq binds one option, msq binds the full
          correct set with WHY WRONG over the non-selected, nat binds a value (+ optional
          range) with COMMON PITFALLS in place of WHY WRONG. Never force one type's shape
          onto another. Descriptive/essay questions are out of scope and flagged (§22).
  RE-23 : KEY RECONCILIATION (v1.37.0). Every derived answer is hashed and compared with
          Step 7's commitment (§7-8) before its block ships; a mismatch enters §17-3; the
          outcome is recorded per question (§R10).
  RE-24 : FORMULA TYPOGRAPHY IS ENGINE-APPLIED (v1.37.0, §8-0c): notation in student prose
          is normalised to Unicode sub/superscripts at construction; residue raises.
  RE-22 : LOAD & APPLY LEARNINGS. At P1, load the accumulated learnings —
          [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md (v1.21.0: legacy/manually-authored — its
          Step-10 producer no longer exists; still READ when present),
          [ExamCode]_EXPLAIN_LEARNINGS_v*.md (human guardrails) and, v1.36.0,
          [Subject]_EXPLAIN_LEARNINGS_v*.md (subject-level guardrails shared by every
          exam in the subject — the curated neighbour library §7-7 tests against) — via
          parse_learnings, and OBEY every applicable rule while authoring (§24).
          Learnings OVERRIDE this spec on conflict (content only — never coverage/§18,
          RE-0; exam file > subject file > spec); they accumulate across mocks (never
          deleted, superseded only by an explicit annotation). Absent on mock 1 by
          design — proceed without them.

# ════════════════════════════════════════════════════════════════════════
# §1 — PIPELINE POSITION & SOURCES OF TRUTH
# ════════════════════════════════════════════════════════════════════════

## S0-3 — SESSION CLASS AND READ SET (v1.39.0 — decide at STEP 0, before any spec read)

```
Framework_PYQCore EC-P42; the Framework_MockTestAnalyse §S8-0b architecture, applied to
Step 9. Deploy follow-up #2 of release 2026.08.21.2.

THE AXIS IS FINAL vs NON-FINAL — never fresh vs resume. Every batch session runs the
same per-question machinery, the same §21 invariants and the same S18/S19 per-batch
delivery; what decides which sections it REACHES is whether it will close the mock.

  NON-FINAL  the batch this session will deliver is NOT the last of the frozen batch
             plan (S4-2). The end-of-mock report cannot run here.
             READ: everything EXCEPT §20 (END-OF-MOCK REPORT), §22 (KNOWN
             LIMITATIONS — disclosed in §20's §R9, nowhere else) and APPENDIX A
             (engine provenance; editorial). §21, §23 and §24 are per-session law
             and are ALWAYS read.
  FINAL      the batch this session will deliver IS the last of the plan, OR the plan
             is not yet known (fresh mock before P4 builds it), OR the trigger is a
             re-run of a completed paper. READ EVERYTHING. NO EXCEPTION.
             Unknown -> FINAL: reading too much costs context; reading too little can
             let a reduced read reach the end-of-mock writer.

ESCALATION IS MANDATORY AND ONE-WAY. A session that begins NON-FINAL and discovers
mid-run that it will close the mock (a batch plan shrunk by atomic-group packing, a
resumed run whose remaining batches all fit this session) MUST read §20, §22 and
APPENDIX A BEFORE the end-of-mock report is entered. FINAL never downgrades.

Line ranges are GENERATED into SPEC_SECTIONS.json from this file's own headers and
hash-tracked in MANIFEST.json — never hand-maintained here. Read ranges with
`sed -n 'START,ENDp'` in bash (the view tool truncates ~16,000 chars per call;
SPEC_SECTIONS.json records both stride constants). `bootstrap.py --trigger MockExplain`
prints the class, both read budgets and the exact ranges.

WHAT THIS DOES NOT CHANGE. Not one byte of any artefact: the same explanations, the
same gates, the same deliveries. It moves the CLOSING sections off the per-batch
execution path — it does not shrink, soften or delete them.
```


## S1-1 — Sources of truth (strict priority order)

  1. THE PAPER ITSELF — [ExamCode]_Mock[N]_Create.docx. The rendered stem +
     options + attached artefacts are the ground truth for what must be explained.
  2. section_rules.md — CATEGORY C (option count, language, labels, escape tokens,
     figural types) + per-subtopic patterns (what the AXIOM must state per class).
  3. blueprint.json — sections[], q_range[] (the batch-plan source), difficulty.
  4. subtopic_manifest.json — subtopic_id join (class detection support — §6).
  5. registry.json — figural_manifests[] / rc_manifests[] as CROSS-CHECKS only.
     (v1.5) registry.question_index is a FROZEN, read-only field (Step 7 -> Step 11): Step 9
     neither consumes it as a source nor modifies it; see S2-2 for the defensive alignment check.
  When the paper and a manifest disagree, the PAPER wins (a manifest records intent;
  a render bug is exactly what Step 9 must catch — §13).

## S1-2 — Memory prohibition

  No answer, fact, figural reading or label is certified from memory. Answers are
  derived (§7); facts are web-verified (§7 / RE-18); figures are viewed (§13);
  labels/regex/counts are read from config (RE-9/RE-10).

# ════════════════════════════════════════════════════════════════════════
# §2 — TRIGGER FORMAT & MOCK-NUMBER RESOLUTION
# ════════════════════════════════════════════════════════════════════════

## S2-1 — Trigger formats

```text
  FRESH  : TestExplain P[N] [--level <mock|subject|topic|subtopic>] [--scope <Subject[::Topic]>]
           (+ [ExamCode]_[paper_slug]_Create.docx already in project)
  RESUME : TestExplain P[N] resume  (re-enter mid-paper; reload state, §4)
  STATUS : TestExplain P[N] --status (dashboard only, then WAIT)
  CONT   : continue | next | go                     (proceed to the next batch — §4)

  ALIAS (v1.19 — mock-only, working alias, unchanged behaviour):
    MockExplain M[N]          == TestExplain P[N] --level mock
    MockExplain M[N] resume   == TestExplain P[N] --level mock resume
    MockExplain M[N] --status == TestExplain P[N] --level mock --status
```

  Unclear trigger → ask ONE clarifying question. Never solve on ambiguous input.
  Trigger WITHOUT the matching [ExamCode]_[paper_slug]_Create.docx present → HALT, request
  the upload. (v1.24: this and the FRESH line above said "Create_Complete" — a filename
  RETIRED at v1.21.0 that no step produces (see the header note); a session following the
  old wording literally would refuse the valid _Create.docx upload forever. The operative
  P1 discovery always used _Create.docx; the trigger contract now says the same thing.)
  --level, when given, is cross-checked (not required) against the blueprint
  pp.pick_blueprint resolves via the uploaded docx (P1) — a mismatch is a HARD STOP.
  MockExplain M[N] always implies level='mock'.

## S2-2 — Mock/paper-number resolution (do this BEFORE loading questions)

  Resolve N from the trigger. Confirm registry.papers_completed CONTAINS this paper's
  paper_id (Step 7 appends it at Final Assembly) — falling back to legacy
  registry.mocks_completed containing N for a mock on an older registry. If neither holds:
    HARD STOP: "registry.papers_completed = [...] does not contain paper_id [paper_id].
    Step 9 explains a paper Step 7 has completed; run Step 7 on it first."
  registry is FROZEN here — this is a read-only alignment check, never a re-sync.

  DEFENSIVE INDEX ALIGNMENT (v1.5 — read-only; Contract_QuestionMetadataIndex v1.0):
  registry.question_index is a Step-7-written, FROZEN field that feeds Step 11's tags. Step 9
  NEVER reads it as a source and NEVER modifies it. As a cheap corruption tripwire ONLY: if the
  field is present it should carry exactly one object for mock N whose questions cover
  1..total_questions; a mismatch is reported as a WARNING (Step 9 derives its own question TYPE
  from the paper + registry.options_by_q and does NOT consume the index, so this never blocks or
  alters Step 9's output — it flags a registry that Step 7 should rebuild). If the field is
  absent, Step 9 proceeds silently (older registries predate it).

# ════════════════════════════════════════════════════════════════════════
# §3 — SESSION START: PRE-FLIGHT (P0 … P9) — run ALL before any solving
# ════════════════════════════════════════════════════════════════════════

  P0  TRIGGER DETECTION (§2). Resolve N; pick FRESH / RESUME / STATUS / CONT.
  P1  AUTO-LOAD (exact order): this spec → section_rules.md → BLUEPRINT (v1.19,
      docx-driven pp.pick_blueprint — twin of Step 7's resolver): discover the uploaded
      [ExamCode]_[paper_slug]_Create.docx, parse its paper_slug from the
      filename, load every [ExamCode]*_blueprint.json present (mock + any scoped),
      import paper_pipeline as pp, and call
      pp.pick_blueprint(blueprints, level=LEVEL, docx_slug=paper_slug) to select the
      ONE blueprint that produced this paper (cross-checked against --level if given;
      PickError → HARD STOP, never a guess). SAFETY CHECK: the [ExamCode]*_blueprint.json
      glob is a PREFIX match — verify the selected blueprint's exam_code equals
      [ExamCode] exactly; a mismatch is a HARD STOP (a different ExamCode's file may
      have been swept in by the glob) → subtopic_manifest.json → registry.json →
      explain_engine.py (from the Step-0 verified clone /tmp/fw ONLY — v1.40.0; a
      project-Files copy is never imported, MANDATE A). Copy the engine to /home/claude and run
      `python3 explain_engine.py --self-test` → MUST print
      "SELF-TEST: N/N PASS" with N == total (all pass) AND N >= 62 before any
      solving (v1.25, GAP-2026-08-13-STALE-SELFTEST-PIN: the FLOOR form, the
      same AUTH_GATE_FLOOR pattern Steps 6/7 use for the audit copy — the
      previous exact "62/62" pin made every session HALT on a HEALTHY engine
      the moment it grew fixtures, and the fixture count has risen repeatedly
      since. NO EXACT COUNT IS WRITTEN INTO PRESCRIPTIVE TEXT ANYWHERE IN THIS
      SPEC (§21-0 — the historical record may still quote one):
      bootstrap.py's sha256 verification is what proves engine integrity, not
      the count). THEN LOAD LEARNINGS (§24): via
      explain_engine.parse_learnings, parse the highest-version
      [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md (legacy/manual — v1.21.0) and
      [ExamCode]_EXPLAIN_LEARNINGS_v*.md (human guardrails) IF PRESENT — and, v1.36.0,
      the SUBJECT-level [Subject]_EXPLAIN_LEARNINGS_v*.md (subject code from
      section_rules CATEGORY C `subject_code`, upper-cased) IF PRESENT — and index every
      AL/EX rule by defect_code (precedence exam > subject > spec). Record in the
      dashboard whether the subject file was found: §7-7 neighbours come from it.
      v1.37.0 — triggers = explain_engine.triggers_from_learnings([all parsed files]) →
      EngineConfig(learnings_triggers=triggers) at P3 (§7-7 step 3, §24-1b). These OVERRIDE this spec on conflict (§24). When a
      learnings file is present, also run `--self-test-audit` (N/N PASS with N >= 10) to
      confirm the cross-step readers. Absent on mock 1 by design — proceed. Any load/self-test
      failure → HALT.
      THEN RENDERER PREFLIGHT (v1.40.0 — the §6A-6 dependency install, given its P-step):
      read section_rules CATEGORY C `representation_renderers`; for each declared
      requirement pip-install its library (--break-system-packages, the Step-0 pattern),
      import-test it, and record the result on the dashboard "Renderer preflight" line.
      An install that fails does NOT halt: that requirement degrades per §6A-4 for the
      WHOLE run, disclosed up front. No block declared → PROSE/EQUATION only, said so.
  P2  STATUS DASHBOARD (print every turn, before any solving):
```text
      === MockExplain [spec version from this file's header] — Session Status ===
      Spec / section_rules / blueprint / manifest / registry : [loaded]
      explain_engine.py --self-test                          : [the N/N PASS line
                                                               the engine printed]
      Exam config (CATEGORY C)  : options=[k or per-section map] · labels=[scheme] ·
                                  q_re=[..] · opt_re=[..] · lang=[..] · terminators=[..]
      Level / Medium             : [level] · [medium]  (from exam_config via CATEGORY C)
      Marking ranges             : [N] range(s) · marks=[list] · neg=[list]  (from marking_scheme)
      Question types present     : [mcq C · msq M · nat T]  (per blueprint/section_rules)
      Answer key                 : NONE by design — Step 9 derives all [Q_TOTAL]
      Key commitments / semantic objects / triggers : [k entries] · [m Qs] · [t families]
                                   (each OR absent — §7-8 / §13-2b / §7-7)
      Learnings loaded           : [k AL-rules · m EX-rules · v_j] OR [none — mock 1 by design]
      Paper (Mock N)             : [X bytes · Q_TOTAL questions · K images · T tables]
      Figural manifest / RC manifest : [found in registry] OR [absent — derive visually]
      Batch plan                 : [K batches · ceiling 10 · linked groups atomic]
      Mode                       : [interactive — halt per batch] OR [autonomous — no pause, §MANDATE B]
      Output                     : /mnt/user-data/outputs/[ExamCode]_[paper_slug]_Explanation.docx
      Renderer preflight (P1)    : [requirement → library → installed/absent → degrade?] per declared renderer, OR [none declared — PROSE/EQUATION only]
      §7A-M difficulty re-measure: [k/n agree] OR [DORMANT — reason]  (advisory, §7A-M)
      State                      : /home/claude (chat-scoped)
      Status                     : [Ready — Batch 1] OR [Resume — Batch k] OR [Halted — reason]
```
  P3  VERIFY INPUT DOCX — build EngineConfig from CATEGORY C + blueprint, then run
      parse_paper(). EngineConfig carries: q_re, opt_re, the option count (uniform OR a
      per-question/per-section map via options_by_q, with 0 marking NAT questions), the
      option LABEL SCHEME (numeric/alpha/roman/custom), the language SENTENCE TERMINATORS
      (e.g. add the Devanagari danda), and labels/markers. Resolve each question's TYPE
      (mcq/msq/nat) by the SAME mode rule Step 7 (v5.30), Step 11 (v1.7) and
      audit_canonical (v2.9) apply — v1.40.0, GAP-2026-08-24-STEP9-AUDIT-R1:
        POSITION-BASED  — blueprint.marking_scheme[] declares > 1 distinct question_type
                          → each question's type is the question_type of the marking_scheme
                          range containing its number (MCQ→mcq, MSQ→msq, NAT/integer/
                          numerical→nat). On such an exam the per-subtopic fields are
                          UNRELIABLE by construction (a subtopic sits in both an MCQ and an
                          MSQ range) and are NOT consulted for the type.
        SUBTOPIC-BASED  — 0 or 1 distinct question_type (or no marking_scheme) → the
                          pre-v1.40.0 rule: section_rules answer_type=='numerical' → nat;
                          answer_cardinality=='multi' → msq; else mcq.
      In BOTH modes options_by_q (below) remains the per-question NAT authority and must
      agree with the resolved type; a disagreement is a config drift → P5 HALT. parse_paper checks: questions ascending + contiguous
      from 1; every question carries its EXPECTED option count (per-question, 0 for NAT);
      Q_TOTAL matches blueprint. Re-extract figural_manifests[] / rc_manifests[] from
      registry. Any fail → HALT with the specific check.
      v1.3 — options_by_q SOURCE (the mandatory NAT wiring, Step-7 ND6 contract): load the
      per-question expected-option-count map from registry.json['options_by_q'][str(N)]
      (Step 7 writes it at Final Assembly — 0 marks a NAT question, OPTIONS_COUNT marks an
      option question) and pass it to EngineConfig(options_by_q=...). This is REQUIRED, not
      optional: EngineConfig.expected_options(q) reads this map and NEVER counts the rendered
      option paragraphs, so WITHOUT it a NAT question inherits the uniform count and is
      mis-resolved as mcq (or trips the count-invariant HALT). v1.3.1 — the registry's inner
      keys round-trip through JSON as STRINGS ("3") while expected_options() is queried with
      an INT q; EngineConfig now normalises options_by_q keys to int on construction, so the
      map may be passed straight from registry.json with no key conversion (a str/int miss
      would otherwise silently mis-type every NAT question as mcq — the NAT-STRKEY self-test
      locks this). v1.37.0: the SAME EngineConfig carries learnings_triggers (P1) and
      formula_typography (CATEGORY C, default true); provenance_gates is NEVER set — a
      session passing provenance_gates=False is NON-CONFORMING. The registry map is the
      per-question AUTHORITY; the section_rules answer_type is the per-subtopic EXPLICIT hint
      the PYQ-phase config now specifies — they must agree (a NAT subtopic's questions are exactly the
      options_by_q==0 questions). If the registry lacks options_by_q (a pre-v4.7 paper),
      fall back to the section_rules per-question/per-section type resolution and WARN that
      the paper predates the ND6 contract.
  P4  BUILD THE FROZEN BATCH PLAN (§4) from blueprint q_range[] + the linked-group
      manifests; write it to progress.json. This plan is the AUTHORITY for batching.
  P5  CONFLICT CHECK: if section_rules / blueprint disagree on a section's option count,
      its question type, or Q_TOTAL → HALT (a drifted config corrupts every block).
      Also verify opt_re and label_scheme DESCRIBE THE SAME LABELS — both digits, or both
      A–D, or both i–iv, etc.; a digit opt_re paired with an alpha label_scheme is a config
      drift that mis-parses every option → HALT. Surface, do not guess.
      OPTION-LABEL FORMAT COHERENCE (v1.34.0 — GAP-2026-08-19-SILENT-LABEL-FORMAT-CONFLICT).
      section_rules declares `option_label_format` in TWO PLACES: once in the CATEGORY C
      header, and once per SECTION block. COMPARE THEM ALL. If the header disagrees with
      ANY section, or two sections disagree with each other → HALT, printing every
      declared value with its location. DO NOT resolve it by precedence, and above all do
      not silently prefer the header — that is exactly the guess this step forbids.
      WHY THIS IS ITS OWN CHECK. The option count and question type were already compared
      above; the LABEL FORMAT was not, and it is generated from a different source: the
      header is written from OBSERVED PYQ papers, while the per-section values come from
      per-section synthesis. Re-running the PYQ analysis can therefore change the header
      alone and leave every section untouched, producing a file that contradicts itself
      with no other symptom. The failure is silent and total: every option in the paper
      carries the wrong label, every explanation binds against it, and NOTHING else in the
      run looks wrong — the counts match, the types match, the paper renders.
      SCOPE, stated honestly: the labels are PRINTED by the generation step, and this step
      only reads them. Halting here does not un-print a paper already generated — it stops
      an explanation run from cementing the wrong labels and tells the author to fix the
      config and regenerate. The same comparison belongs in the generation step; that this
      one is downstream is a reason to surface loudly, not a reason to guess.
  P6  RESUME (only on `resume` / `continue`): reload progress.json + answer_keys.json
      + the pickled blocks, rebuild the Solutions docx from the clean source + all
      blocks so far, run §18 self-audit on it, THEN proceed to the next batch (RE-19).
  P7  MALFUNCTION GUARD: if about to ask "per-batch or all-at-once?", STOP — the
      answer is fixed (per-batch, MANDATE B; autonomous mode waives only the pause,
      never the per-batch review). If about to solve beyond the current batch, STOP (no
      look-ahead). If about to declare a paper defect, go to §17 first.
  P8  PRINT the batch plan summary (batch → q-range → count) and announce Batch 1.
  P9  EXECUTE the current batch (§4). One batch, then HALT for confirmation (interactive)
      or proceed to the next batch (autonomous — §MANDATE B).

# ════════════════════════════════════════════════════════════════════════
## P10 — REGISTRY-FK TRIPWIRE (v1.23 — MANDATORY, runs after P9, before any solving)

  Validates the registry↔blueprint contract for THIS mock so a defective
  question_index is caught before a single question is explained, not at Step 11.
  Self-contained on purpose (no engine import needed at this point in the session).

  ```python
  import json as _p10_json
  import glob as _p10_glob
  import paper_pipeline as pp   # v1.24: explicit in-block bind (P10 is self-contained;
                                # a re-import after P1 is a harmless no-op)
  # v1.25 (GAP-2026-08-13-P10-SCOPED-BLUEPRINT): select the blueprint the SAME
  # docx-driven way P1 does, never the hardcoded mock filename. The old literal
  # f'{EXAM}_blueprint.json' load meant every SCOPED Explain either compared the
  # uploaded scoped docx against the MOCK blueprint (unconditional false P10/0
  # HARD STOP) or FileNotFoundError'd if no mock blueprint existed — the v1.24
  # gate could never pass for the resumed-scoped papers it was written about.
  # Selection key: the blueprint that CONTAINS a paper whose slug matches the
  # uploaded docx (PAPER_SLUG, parsed at P1) — P1's own semantics, restated
  # self-contained.
  _p10_bps = [_p10_json.load(open(_f, encoding='utf-8'))
              for _f in sorted(_p10_glob.glob(f'/mnt/project/{EXAM}*_blueprint.json'))]
  _p10_bp = next((b for b in _p10_bps if any(
      pp.paper_slug(mk.get('paper_id', f"MOCK:M{int(mk.get('mock', 0) or 0):02d}")) == PAPER_SLUG
      for mk in b.get('mocks', []))), None)
  if _p10_bp is None:
      raise SystemExit(
          f"HARD STOP (P10/0): no blueprint under /mnt/project/{EXAM}*_blueprint.json "
          f"contains a paper whose slug matches the uploaded docx {PAPER_SLUG!r}. "
          f"The blueprint that produced this paper is missing from the project — "
          f"restore it (or re-run Step 6/6S), then re-trigger.")
  _p10_reg = _p10_json.load(open(f'/mnt/project/{EXAM}_registry.json', encoding='utf-8'))
  _p10_tp  = next((mk for mk in _p10_bp.get('mocks', []) if mk.get('mock') == N), None)
  _p10_pid = (_p10_tp or {}).get('paper_id', f"MOCK:M{int(N):02d}")
  # P10/0 (v1.24 — GAP-2026-08-13-EXPLAIN-N-SLUG-GATE): trigger-N ↔ uploaded-docx
  # identity gate, the SAME assertion Step 11 (Framework_MockDeliver S1-2) already
  # makes and Step 9 previously did NOT. P1 selects the BLUEPRINT by the uploaded
  # docx's slug, but N comes from the trigger — and on a RESUMED SCOPED SERIES the
  # blueprint's `mock` field is an ORDINAL (1..count) while the paper_id carries the
  # OFFSET series number (ScopedBlueprint S2-4 paper_start), so a mistyped P[N] can
  # silently bind a DIFFERENT paper's options_by_q/question_index to the uploaded
  # paper and publish a mislabeled Explanation. PAPER_SLUG here is the slug parsed
  # from the uploaded _Create.docx filename at P1.
  if pp.paper_slug(_p10_pid) != PAPER_SLUG:
      raise SystemExit(
          f"HARD STOP (P10/0): trigger paper N={N} resolves to paper_slug "
          f"{pp.paper_slug(_p10_pid)!r}, but the uploaded docx carries "
          f"{PAPER_SLUG!r}. Wrong P[N] for this upload (on a resumed scoped "
          f"series remember N is the blueprint ORDINAL, not the filename's series "
          f"number). Re-trigger with the N whose paper produced this docx.")
  _p10_entry = next((e for e in _p10_reg.get('question_index', [])
                     if e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}") == _p10_pid), None)
  _p10_fails = []
  if _p10_entry is None:
      _p10_fails.append(f"P10/1: no question_index entry for {_p10_pid} — registry data "
                        f"for this paper is missing (lost by a later write, or Step 7 "
                        f"never committed). Remedy: re-run Step 7 for mock {N}.")
  else:
      _p10_qs = _p10_entry.get('questions', [])
      _p10_tq = _p10_bp.get('total_questions')
      if _p10_tq and len(_p10_qs) != _p10_tq:
          _p10_fails.append(f"P10/2: {len(_p10_qs)} entries != total_questions {_p10_tq}")
      # P10/2b COVERAGE + UNIQUENESS. The count test above is NOT sufficient: an
      # index carrying q=[1,1] has the right LENGTH and passes it, so P10 would
      # certify a paper whose q=2 has no entry at all — and Step 11's JOIN then
      # fails after the whole Explain effort was spent, which is the one outcome
      # P10 exists to prevent. Both engine implementations (A-QINDEX/3 and
      # paper_pipeline.validate_question_index) already assert the q set is
      # exactly 1..total_questions, sorted and unique; this preflight must agree
      # with them or the three copies of this rule disagree on a real registry.
      _p10_qn = [x.get('q') for x in _p10_qs]
      if _p10_tq and (_p10_qn != sorted(_p10_qn) or len(set(_p10_qn)) != len(_p10_qn)
                      or set(_p10_qn) != set(range(1, _p10_tq + 1))):
          _p10_fails.append(f"P10/2b: q set != 1..{_p10_tq} (sorted/unique/complete) — "
                            f"got {sorted(_p10_qn)!r}; a duplicate or missing q number "
                            f"leaves a question with no index entry for Step 11's JOIN.")
      _p10_ids = {s.get('subtopic_id') for s in _p10_bp.get('subtopic_list', [])}
      _p10_bad = {int(x.get('q', -1)): x.get('subtopic_id')
                  for x in _p10_qs if x.get('subtopic_id') not in _p10_ids}
      if _p10_bad:
          _p10_fails.append("P10/3: subtopic_id(s) not in blueprint.subtopic_list "
                            "(invented/re-typed at Step 7 — Step 11's JOIN will hard-stop): "
                            + "; ".join(f"Q{q}={_p10_bad[q]!r}" for q in sorted(_p10_bad)))
      _p10_canon = _p10_bp.get('difficulty_labels', ['Easy', 'Medium', 'Hard'])
      _p10_badd = sorted({x.get('difficulty') for x in _p10_qs
                          if x.get('difficulty') not in _p10_canon})
      if _p10_badd:
          _p10_fails.append(f"P10/4: difficulty value(s) not in {_p10_canon}: {_p10_badd}")
  if _p10_fails:
      raise SystemExit("HARD STOP (P10 registry-FK tripwire, v1.23):\n  "
                       + "\n  ".join(_p10_fails)
                       + "\nFix upstream (Step 7 / registry patch) and re-trigger Step 9. "
                         "Explaining a paper whose index cannot JOIN wastes the whole "
                         "Explain effort — Step 11 will refuse it.")
  # Ledger↔index agreement for the WHOLE registry (other papers): WARN, never block.
  _p10_claimed = set(_p10_reg.get('papers_completed') or [])
  for _m in _p10_reg.get('mocks_completed') or []:
      try: _p10_claimed.add(f"MOCK:M{int(_m):02d}")
      except (TypeError, ValueError): pass
  _p10_have = {e.get('paper_id', f"MOCK:M{e.get('mock', -1):02d}")
               for e in _p10_reg.get('question_index', [])}
  _p10_missing = sorted(_p10_claimed - _p10_have)
  if _p10_missing:
      print(f"P10 WARN: registry ledger claims complete but question_index is MISSING for "
            f"{_p10_missing} — those papers' data was lost and their deliveries WILL "
            f"hard-stop. Surface this to the operator now; it does not block mock {N}.")
  print(f"P10: registry-FK tripwire PASS for {_p10_pid}.")
  ```

# §4 — BATCH ARCHITECTURE (the continue contract; whole-paper incremental delivery)
# ════════════════════════════════════════════════════════════════════════

## S4-1 — EXPLAIN_BATCH_SIZE

  EXPLAIN_BATCH_SIZE = 10. This is a CEILING, never a quota (RE-7). A batch may hold
  fewer (an early close for an atomic group). It is NEVER raised above 10 by choice;
  the ONLY over-10 batch is a single atomic linked group larger than 10 (S4-3).

## S4-2 — The frozen batch plan (built once at P4, the authority for the whole run)

  Walk blueprint q_range[] in order, accumulating questions into the current batch
  until adding the next unit would exceed the ceiling, then start a new batch. A
  "unit" is a single standalone question OR a whole atomic linked group (S4-3). The
  plan is written to progress.json and is the SOLE source for which questions a turn
  may touch — not in-the-moment judgement. The dashboard prints "Batch k of K" every
  turn so position is always visible.

## S4-3 — Atomic linked groups (the one flexibility)

  A linked group (RC passage set / cloze / DI cluster / puzzle) — identified from
  registry rc_manifests[] + the paper's shared-stimulus structure — is NEVER split
  across a batch boundary (so every member is solved with the full stimulus in view).
  Packing rule: if adding the next group would cross the ceiling, CLOSE the batch
  early. If a single group is ITSELF larger than the ceiling, it becomes its own
  batch and may exceed 10 (atomicity wins — MANDATE B). EXPLAIN_BATCH_SIZE can only
  ever shrink a batch, never grow one by choice.

## S4-4 — One batch = one response (the continue contract)

  Each batch response does EXACTLY this, in order, then ENDS:
    A. Read batch_plan[k] from progress.json. Solve ONLY those questions (§7 derive +
       second-method verify; §13 view images; §6A ROUTE THE REPRESENTATION; §6
       class-adaptive write). No look-ahead.
    B. Build each ExplanationBlock and call .validate() immediately (fail-at-construction).
    C. CUMULATIVE WHOLE-PAPER BUILD: build_interleaved_docx(CLEAN_SOURCE, ALL_BLOCKS_1..k,
       out, cfg). ALL blocks from batch 1 through k — never batch-k-only (this is why the
       remainder stays the source's bytes and prior batches are never dropped). The clean
       Step-7 source is kept read-only in /home/claude and seeded WHOLE every time.
    D. §18 SELF-AUDIT on the whole doc: validate() all blocks + verify_fidelity (byte-
       identical to source) + verify_structure (coverage == Q1..last(batch k), NO look-
       ahead) + math-render check. Any fail → fix, re-build, re-audit. Never deliver dirty.
       When and only when every §18-1 item holds, set SELF_AUDIT_CLEAN = True and (for the
       S4-5 guard-3 coverage assertion) COVERAGE_OK = True in the session — these are the
       two flags S19-1 reads (v1.40.0; they were gated on but never assigned anywhere).
       They are reset to False at the start of every batch.
    E. Flush state to /home/claude: progress.json (mark batch k done) + answer_keys.json
       (append this batch's CAs) + the pickled blocks. Stage NOTHING else to outputs.
    F. present_files(the single Solutions docx) — the whole paper (MANDATE D).
    G. Print the MANDATE-0-safe progress line + ASK for explicit confirmation, then END
       THE RESPONSE. Do NOT begin batch k+1. (RE-7) — INTERACTIVE mode. In AUTONOMOUS mode
       (MANDATE B) the pause is waived: proceed to batch k+1 in the same session, still
       running A..F for one batch at a time (the review is never collapsed, RE-0).
  The run resumes only on the author's "continue" (P6 reloads + re-verifies first) in
  interactive mode. The FINAL batch (k == K) also stops and asks (interactive); on the
  next "continue" it prints the §20 report + author handoff (no auto-finalise —
  MANDATE B). In autonomous mode the report + handoff print after batch K in the same run.

## S4-5 — The four anti-overrun guards (why all-at-once cannot happen)

  1. FROZEN PLAN (S4-2): the turn may only touch batch_plan[k]; the plan is fixed at P4.
  2. ENGINE STAGE GUARD: build_interleaved_docx + verify_structure assert coverage is
     EXACTLY the expected set — a batch that solved beyond its slice fails verify_structure
     ("look-ahead") and cannot be delivered.
  3. PRE-DELIVER COVERAGE ASSERTION (§18): the whole doc must carry explanations for
     exactly Q1..last(batch k) — no fewer (broken cumulative build) and no more (silent
     look-ahead). For a non-final batch, Q(last+1) MUST NOT be explained.
  4. HARD TURN BOUNDARY (S4-4 G): the response ends at the confirmation request with
     nothing after it (interactive). The batch reset is also the quality reset (§16) — it
     keeps the last question as sharp as the first. In autonomous mode the boundary is the
     per-batch build+§18 cycle rather than a turn end; the coverage assertion (guard 3)
     still fires per batch, so a collapsed run is caught the same way.

# ════════════════════════════════════════════════════════════════════════
# §5 — THE BLOCK MODEL (ExplanationBlock) + the per-question checklist
# ════════════════════════════════════════════════════════════════════════

## S5-1 — Fields (shaped by the question type: mcq · msq · nat)

  | Field           | Type                 | Constraint                                          |
  |-----------------|----------------------|-----------------------------------------------------|
  | q               | int                  | the question number                                 |
  | qtype           | 'mcq'/'msq'/'nat'    | auto-inferred (0 expected options → nat; ca is a set → msq; else mcq) or set explicitly |
  | ca              | int / set[int] / val | MCQ: 1-based index. MSQ: a non-empty set of indices. NAT: the PORTAL GRADING VALUE string from `derive_nat_grading()` (S7-4) — never the raw derived number directly; a bare `str()` of a float can differ from the certified string (e.g. "3.0" vs "3") |
  | ca_range        | (lo,hi) / None       | NAT only; when grading_type=='range' (S7-4), `(_fmt_portal_number(lo, stem_precision), _fmt_portal_number(hi, stem_precision))` — the SAME S7-4 helper, called directly on the two bounds; never raw floats (lose stated precision) and never a string split apart from `grading_value` (an unnecessary extra step with its own failure modes) |
  | axiom           | list[str]            | ≥1 DENSE sentence (content floor, not length floor — §8) |
  | deduction       | list[str]            | ≥2 steps. MCQ: last binds "Option L(ca)". MSQ: last binds EVERY selected option. NAT: last contains the value |
  | speed_hack      | list[str]/None       | present IFF a genuinely faster route exists (§14); else None |
  | why_wrong       | dict{int:list}       | MCQ/MSQ only: keys == exactly the NON-selected options; each names an error type that reproduces the option (§15) |
  | common_pitfalls | dict{val:list}       | NAT only: ≥1 wrong-VALUE entry; each names the slip that yields that value (the NAT analogue of WHY WRONG) |
  | anomaly         | str/None             | INTERNAL escalation flag only — NEVER rendered to a student (§17) |
  | figures         | list[RepresentationFigure] | v2.3, may be empty. Each carries the §6A-5 validation record (renderer/intended/derived/match) and fails validate() on any breach; rendered as text-free centred picture paragraphs interleaved into DEDUCTION at after_step (§6A-6) |
  | representation_verdict | str/None      | v2.6, optional. The §6A router verdict (PROSE / EQUATION / TABLE / STRUCTURE_GRAPH / LEVEL_DIAGRAM / DATA_PLOT / CONFORMER v2.7). When set, a VISUAL verdict with zero figures raises at validate() — verdict↔emission coherence (§6A-3); after a §6A-4 degrade the block carries the DEGRADED requirement |

  | absolutes_justified | dict{str:str}  | v2.7. {sentence: reason} for each absolute KEPT in AXIOM / SPEED HACK / WHY WRONG / COMMON PITFALLS; an undeclared universal there raises at validate() (§8-0b). Reason = why it is absolute in the subject's own terms |
  | transfer_record | list[dict]/None  | v2.7, REQUIRED by this spec on every block (§7-7). One entry per claim {section, claim, epistemic_type, scope, neighbour_tested, outcome}; shape-validated: AXIOM needs an AXIOM entry, SPEED HACK a SPEED_HACK entry, no QUESTION_SPECIFIC in AXIOM, no OPTION_SET_SHORTCUT outside SPEED_HACK |

  Option index → displayed label is via cfg.option_label() (numeric / alpha / roman /
  custom — read from CATEGORY C), so a paper labelled A·B·C·D shows "Correct Answer: A"
  and "Option B", never a 1-based number that mismatches the paper (RE-10).

## S5-2 — Hard structural guards (engine, write-time — position-independent)

  Correct Answer line = INDEX/VALUE ONLY (no option text): MCQ shows the one label, MSQ
  the label set ("A, C"), NAT the S7-4 grading value (a plain value, or a lo-hi range when
  the exam publishes a tolerance). The CA line, the DEDUCTION's
  binding, and the stored answer_keys.json value must agree (three-way CA binding).
  DEDUCTION ≥2 steps; last binds the answer (every selected option for MSQ; the value for
  NAT). WHY WRONG keys == exactly the non-selected options (MCQ/MSQ); NAT uses
  common_pitfalls (≥1) and MUST NOT carry why_wrong (and vice-versa). ≥1 dense sentence
  each. OMML for every fraction (§11) — including a fractional NAT value. One sentence per
  paragraph (terminator set is language-configurable — §11). Zero ✓/✗ glyphs, zero LaTeX,
  zero metacommentary, zero template sentences, zero fake citations, zero REMEMBER /
  EXAM-CONNECTION blocks, zero year-range slashes, zero internal error-taxonomy
  tokens in any rendered sentence (§9, v2.6), and no AXIOM naming an option label
  (§8-2, v2.6). A breach raises in
  ExplanationBlock.validate() / add_math_text BEFORE the doc is written. As of
  2026.08.10.3, validate() also COMPILES any ⟦MATH:…⟧ Tier-3 region (t3_compile) and
  RAISES at construction on a grammar reject, so such a region can never degrade to
  raw text at render; this pipeline normally builds math with the explicit helpers
  (§11), so regions are rare here, but the gate applies to the shared engine. (v1.36.0) Engine v2.7 adds three write-time gates: an
  UNDECLARED UNIVERSAL in AXIOM / SPEED HACK / WHY WRONG / COMMON PITFALLS raises
  (§8-0b; keep one by declaring it in absolutes_justified); a LEARNER-PSYCHOLOGY
  template raises (§15-3); a supplied transfer_record is shape-validated (§7-7).
  DEDUCTION is not absolute-gated — item-specific working, governed by §7-7.

## S5-3 — PER-QUESTION CHECKLIST (tick every item before constructing the block)

```text
  [ ] Full stem + ALL options read to the end; OMML merged with text in document order
  [ ] Question TYPE resolved: mcq (one option) · msq (a set) · nat (a value, no options)
  [ ] Negative phrasing scanned (config triggers; default NOT/EXCEPT/INCORRECT/FALSE) → §10a
  [ ] Composite options scanned (Both/Only/All of the above/None of the above)   → §10b
  [ ] Figural? → every image extracted, role-bound, and VIEWED before solving     (§13)
  [ ] Figural? → FAMILY decided (transformation-puzzle / scientific-diagram) and the
      matching protocol used; for scientific-diagram, decisive features TRANSCRIBED
      before solving and NONE inferred from what would make an option work  (§13-1/4b)
  [ ] Answer derived from first principles AND a second independent method        (§7)
  [ ] Methods agree (else DERIVATION-CONFIDENCE) and land on exactly the answer:
      one option (mcq) · the full correct set (msq) · the single value/range (nat) (§7)
  [ ] Factual content web-verified with a recorded source                         (RE-18)
  [ ] Class identified (§6); the right section LEADS; the rest compressed to one dense line
  [ ] Conditions the stem supplies READ BACK and checked before applying any
      remembered result; every stated condition actually used or re-read       (§7-0a)
  [ ] Material assumptions ledgered; any that changes the answer is STATED     (§7-0b)
  [ ] Quantitative? → §7-5 checks pass (units · kelvin · magnitude · log base ·
      sign · stoichiometry · precision)                                        (§7-5)
  [ ] Counting question? → inventory → independence → generate → de-duplicate →
      count; a closed-form only after independence is verified                 (§7-0c)
  [ ] Decisive intermediate claims LISTED and mutually consistent               (§7-6)
  [ ] SPEED HACK, if present, states the conditions under which it is safe    (§14-3b)
  [ ] Every number traces to stem / syllabus constant / shown derivation      (§8-0a)
  [ ] No absolute used for a tendency; no tendency used for a real absolute;
      every KEPT absolute declared with its reason (engine gate, v2.7)         (§8-0b)
  [ ] TRANSFER SAFETY: every AXIOM claim and every SPEED HACK typed, scoped,
      tested on its nearest neighbour at this exam's level, repaired by
      MECHANISM where it failed; transfer_record built and passed to the block (§7-7)
  [ ] AXIOM epistemic type recorded; a MODEL_DEPENDENT or EXAM_CONVENTION rule
      carries its qualifier INSIDE the sentence; item-specific facts are in
      DEDUCTION, not AXIOM                                                     (§8-2)
  [ ] Topic MINIMUM-CONCEPT components (loaded subject learnings, §24) present
      in the DEDUCTION for every archetype the question belongs to             (§8-3)
  [ ] REPRESENTATION ALIGNMENT: the chosen representation, or the prose, shows
      the deciding relation; a spatial / occupancy / topology / handedness
      decision in PROSE carries its explicit inventory                        (§6A-1c)
  [ ] WHY WRONG / COMMON PITFALLS refute the CONTENT; zero learner-psychology
      narration (engine gate, v2.7)                                            (§15-3)
  [ ] AXIOM states a TRUTH, not the task; no restatement of the question
  [ ] DEDUCTION last step binds the answer: "Option L(ca)" (mcq) · every selected
      "Option L(i)" (msq) · the value string (nat); each step shows its value
  [ ] §6A representation router RUN; verdict recorded AND passed into the block
      (engine coherence — a visual verdict requires its figure); PROSE unless the
      two-part test passed; §6A-1b structure-answer questions either emit
      STRUCTURE_GRAPH or record the PROSE justification; any degrade disclosed    (§6A)
  [ ] every quantitative step rendered as ⟦MATH:⟧ math, NOT verbalised arithmetic (§11 S11-1c)
  [ ] every ⟦MATH:⟧ body uses braced scripts and backslash names (\Delta, \sqrt)  (§11 S11-1b)
  [ ] SPEED HACK present IFF a genuinely shorter route was found; else omitted     (§14)
  [ ] WHY WRONG covers exactly the non-selected options, each first sentence
      delivering its §9 diagnosis in natural language (token recorded internally,
      never rendered) and ACTUALLY producing it (mcq/msq); NAT uses COMMON PITFALLS —
      ≥1 wrong VALUE, each with the slip that yields it                            (§15)
  [ ] applicable learnings routed (§24): AL/EX rules whose defect_code this question's
      class can exhibit are loaded and obeyed; any >=2-occurrence AL-rule for a present
      class is honored
  [ ] block.validate() called immediately after construction
```

# ════════════════════════════════════════════════════════════════════════
# §6 — UNIVERSAL QUESTION CLASSES & CLASS-ADAPTIVE SOLVING
# ════════════════════════════════════════════════════════════════════════
#   Solving protocols are keyed to the SAME universal question CLASSES that Step 7's
#   generation model uses — derived at runtime from section_rules format +
#   wrong_option_structure + stem cues, NEVER from exam-specific section ranges. One
#   shared class model across Steps 7 and 9. A question may carry more than one facet.

## S6-1 — The classes and what each makes the explanation LEAD with

  | Class            | Detection (section_rules)                  | Lead section / shape |
  |------------------|--------------------------------------------|----------------------|
  | C-COMPUTATIONAL  | numeric/quantitative answer; TEXT/DI        | DEDUCTION leads (the working); AXIOM = formula+units in one line; each WHY WRONG = one arithmetic slip that yields that value |
  | C-FORMAL-LOGIC   | fixed formal procedure; wrong_option_structure.type == fixed_set (syllogism, data-sufficiency, assertion-reason, cause-effect, inequality, statement-conclusion) | DEDUCTION = a tight one-line-per-statement verdict chain |
  | C-FACTUAL        | answer is a fact (general-knowledge / science / current-affairs / domain) | AXIOM = the fact + its scope in one line; DEDUCTION = answer + crisp reason; WHY WRONG = what each option ACTUALLY is; SPEED HACK OMITTED (a fact cannot be shortcut) |
  | C-VOCAB-ITEM     | synonym/antonym/idiom/one-word/spelling     | AXIOM = the sense/register under test; WHY WRONG = the one nuance each near-miss gets wrong; 2–3 lines total |
  | C-GRAMMAR        | error-spotting/improvement/voice/narration/jumble | DEDUCTION = re-derive the correct form; each WHY WRONG = the one rule violated |
  | C-LINKED         | member of a shared-stimulus group (RC/cloze/DI/puzzle) | POINT to the licensing line in the stimulus ("the passage states … → answer"); do NOT re-argue it |
  | C-FIGURAL        | answer is/depends on a figure (§13)          | Family-dependent (§13-1). TRANSFORMATION-PUZZLE: AXIOM = the visual rule, DEDUCTION traces the VISIBLE transformation, WHY WRONG = the visual difference (§13-4a). SCIENTIFIC-DIAGRAM: AXIOM = the domain principle, DEDUCTION reads the figure as notation then solves, WHY WRONG = the domain error (§13-4b) |
  | C-STRUCTURAL     | v1.29.0 — the answer turns on CONNECTIVITY, a site of reaction, spatial/stereochemical arrangement, symmetry or an enumeration over structures (products, isomers, environments), whether or not a figure is present | DEDUCTION leads and is a TRANSFORMATION CHAIN: starting arrangement → the change and WHERE it happens → resulting arrangement → why that one. AXIOM = the selectivity or structural principle governing the change. Enumerations state the generating rule, then the de-duplication (symmetry, equivalence), then the count — never a bare number. Pairs naturally with a §6A STRUCTURE_GRAPH verdict, but the class holds even when the router says PROSE |
  | C-DERIVATIONAL   | v1.29.0 — a MULTI-STEP chain where each step feeds the next (a relation is manipulated before use, several relations compose, or a limit/boundary case is taken) — distinct from C-COMPUTATIONAL, which substitutes into ONE known relation | DEDUCTION leads and shows the CHAIN: governing relation → what is eliminated or substituted at each step → the result, every step rendered as ⟦MATH:⟧ math (§11 S11-1c). AXIOM = the relation the chain starts from, plus the condition that licenses it. Each WHY WRONG names the ONE step at which that option's route diverges |
  | C-MATRIX/MATCH   | match-the-column / matrix                    | DEDUCTION = re-derive every pair; isolate the one fully-correct option |
  | C-MULTI-SELECT   | MSQ — more than one correct option (section_rules answer_cardinality == 'multi') | DEDUCTION = a truth-verdict line per option, then state the full correct SET; WHY WRONG = why each NON-selected option fails; CA line lists the set |
  | C-NUMERICAL-INPUT| NAT — typed numerical answer, NO options (section_rules answer_type == 'numerical') | DEDUCTION leads to the VALUE (last step contains it); AXIOM = formula+units; COMMON PITFALLS replace WHY WRONG (the wrong VALUES students compute + the slip for each); CA line shows the value (+ tolerance range if the exam allows one) |

  Class detection reads section_rules; an unknown format defaults to the closest class
  by wrong_option_structure.type, and the generic standards (§8) still apply. The
  question TYPE (mcq/msq/nat) is orthogonal to these content classes: a NAT question is
  usually also C-COMPUTATIONAL, an MSQ usually C-FORMAL-LOGIC or C-FACTUAL — the type
  shapes the block skeleton (§5), the class shapes which section leads (§6-2).

## S6-2 — Class-adaptive leading (the "to the point" principle)

  "To the point" is class-dependent: give the ONE section doing the real work the room
  it needs, and compress the rest to a single dense line each. A factual answer must
  not read like a maths proof; a maths answer must not read like an essay; an RC answer
  cites the line rather than re-deriving the passage. The lead section is chosen by the
  question's class (S6-1), not by its position in the paper.

# ════════════════════════════════════════════════════════════════════════
# §6A — REPRESENTATION ROUTER (v1.27.0 — exam-agnostic, domain-configured; §6A-1c / §6A-3b v1.36.0)
# ════════════════════════════════════════════════════════════════════════
#   Representation selection is now an EXPLICIT pipeline stage, run once per
#   question AFTER the answer is derived and verified (§7) and BEFORE any
#   explanation prose is written. Before v1.27.0 it was not a stage at all, so
#   every explanation defaulted to prose regardless of what the question was
#   about — a structural transformation could only be DESCRIBED, never shown.
#   The router is EXAM-AGNOSTIC: it names no exam and no subject. It emits a
#   REQUIREMENT; which renderer satisfies that requirement is read at runtime
#   from the exam's own section_rules.md (CATEGORY C), exactly as option labels
#   and language already are. An exam whose section_rules declares no renderer
#   gets PROSE and EQUATION only and behaves EXACTLY as it did before this
#   version — deploying the router cannot regress an exam that does not opt in.

## S6A-1 — PROSE IS THE DEFAULT. A VISUAL IS EARNED, NEVER ISSUED.
  This is the load-bearing rule; read it before the table. The router's default
  verdict is PROSE, and every richer representation must EARN its place by the
  same two-part test §14 already applies to SPEED HACK ("omit, never fake"):
    1. DECISIVE — the answer turns on a relationship that prose states less
       clearly than the representation would (connectivity, spatial arrangement,
       occupancy, a computed chain, a data shape).
    2. NOT REDUNDANT — the representation carries information the surrounding
       sentences do not already carry. Re-drawing what the stem already shows,
       or illustrating a recall fact, fails this half.
  BOTH must pass, else PROSE. A recall question ("which metal catalyses this
  industrial process") takes PROSE and stops — manufacturing a diagram for it is
  the failure mode this rule exists to prevent, and across 200 exams it is the
  difference between a clearer document and a bloated one.
  MINIMUM SUFFICIENT REPRESENTATION: where two representations both pass, take
  the simpler. Never draw a mechanism where a transformation arrow suffices;
  never draw every intermediate when one selectivity-determining step decides it.

## S6A-1b — STRUCTURE-ANSWER PRESUMPTION (v1.35.0)
  §6A-1's default is inverted for ONE narrow shape: the question whose verified
  ANSWER IS a structure — the CA option is itself a drawn figure
  (IMAGE-AS-OPTIONS, §13-1), or the question is C-STRUCTURAL and the answer is
  the identity of a transformed arrangement. For that shape the decisive
  relationship is BY CONSTRUCTION one that prose states less clearly than the
  representation, so the two-part test is PRESUMED PASSED for STRUCTURE_GRAPH.
  Routing such a question to PROSE anyway is permitted ONLY with a RECORDED
  justification (in progress state, next to the verdict) stating where the
  DEDUCTION prose itself carries each decisive feature — the change, the
  position at which it happens, and the resulting arrangement. A terminal
  identification that only POINTS ("the structure drawn in Option N") carries
  none of them and never satisfies this.
  REFERENCE INCIDENT: a structure-heavy paper shipped 46 question-region images
  and 2 explanation figures, its structure-decisive DEDUCTIONs ending at the
  pointer sentence — the §6A-1 default won everywhere this presumption should
  have. The presumption is still not a quota: a question whose deciding feature
  is fully stated in one prose clause records that justification and ships
  prose legitimately.


## S6A-1b-ii — COUNT-OF-VISUAL-OBJECTS PRESUMPTION (v1.37.0)
  When the ANSWER IS A COUNT OF VISUAL OBJECTS (resonance contributors, isomers, fac/mer,
  bridging bonds, orbital occupancies, competing products, distinct sites) §6A-1b
  applies AND the figure must SHOW THE ENUMERATED OBJECTS, not the starting structure
  alone. PROSE stays legal with a recorded justification.

## S6A-1c — ALIGNMENT: THE REPRESENTATION MUST SHOW THE DECIDING RELATION (v1.36.0)
  §6A-1 tests DECISIVE and NOT REDUNDANT. Both can pass while the learner never
  SEES what the answer turned on: the product drawn, the selectivity-deciding
  intermediate in prose; a terminal/bridging count with no picture of which is
  which; a projection argued without saying which carbon is in front. So a
  THIRD question is asked of every verdict, PROSE included, once the DEDUCTION
  is drafted: does the representation — or the prose — make the ANSWER-DECIDING
  relation visible? A present-but-misaligned representation fails
  (REP_PRESENT_BUT_NOT_ALIGNED) and is re-routed, never captioned over.
  WHEN THE DECISION IS SPATIAL, PROSE NEEDS AN EXPLICIT INVENTORY. If the answer
  turns on arrangement in space, occupancy, topology (which elements bridge) or
  handedness, PROSE is valid ONLY when the DEDUCTION carries what a drawing would:
    • a projection → the viewing direction and the front/rear identity stated
      before any staggered/eclipsed or anti/gauche claim is made;
    • an occupancy-decided answer → the occupancy stated level by level ("the
      lower set holds six, the upper set none"), not only the conclusion;
    • a topology count → the elements listed by role ("four bridge, six are
      terminal: two on each outer centre, one on each inner one");
    • a handedness-decided count → each geometric form named and tested for a
      mirror plane separately, the chiral one stated as a pair.
  Absent that inventory the verdict is a visual one the router under-fired on,
  and it is re-routed (§6A-2). Not a quota: a deciding relation fully stated in
  one prose clause keeps PROSE and records that it did.

## S6A-2 — The requirement vocabulary (what the router emits)
  | Requirement          | Emit when the answer turns on …                        |
  |----------------------|--------------------------------------------------------|
  | PROSE                | a fact, a definition, or a short causal chain (DEFAULT) |
  | EQUATION             | a calculation — governing relation, substitution, value |
  | TABLE                | independent criteria tested across several candidates   |
  | STRUCTURE_GRAPH      | connectivity / stereochemistry / a transformation       |
  | LEVEL_DIAGRAM        | occupancy, energy ordering, or state splitting          |
  | DATA_PLOT            | the shape of a graph, spectrum, or titration curve      |
  | CONFORMER            | (v1.36.0) HOW atoms are arranged at a given rotation — a projection (Newman / sawhorse / chair), which a constitution renderer cannot express; visual, requires its figure (run-report F3) |
  EQUATION is satisfied by §11's ⟦MATH:⟧ regions and is ALWAYS available — it
  needs no renderer and no configuration. TABLE is native docx. The last four
  require a renderer declared in section_rules (CONFORMER is drawn with the
  LEVEL_DIAGRAM library — a projection is a 2-D template with labelled bonds —
  and its §6A-5 identifier is the dihedral/occupant string restated from the
  drawn data); absent one, the router degrades (§6A-4).

## S6A-3 — Record the verdict on every question
  The router's verdict is recorded per question in progress.json as
  representation_verdict, with the two-part test's outcome. This is what makes
  the choice auditable rather than implicit: a paper whose every question
  demanded a figure, or whose every question refused one, is visible as a
  pattern instead of discovered by reading. The §20 report states the
  distribution. (v1.35.0) The verdict is ALSO passed into the ExplanationBlock
  (engine v2.6 representation_verdict), which enforces verdict↔emission
  coherence at construction: a STRUCTURE_GRAPH / LEVEL_DIAGRAM / DATA_PLOT /
  CONFORMER (v1.40.0 — the engine's _VISUAL_VERDICTS has carried CONFORMER since v2.7)
  verdict with zero figures raises; after a §6A-4 degrade the block carries the
  DEGRADED requirement, never the original. HISTORY: v1.27.0 shipped this router RECORD-ONLY so routing
  decisions could be reviewed before any figure shipped; v1.28.0 (paired with
  engine v2.3) turns EMISSION ON — a STRUCTURE_GRAPH / LEVEL_DIAGRAM / DATA_PLOT
  verdict now renders through §6A-6 and ships inside the explanation region.


## S6A-3b — THE DISTRIBUTION IS A TRIPWIRE, AS §14-5 IS FOR SPEED HACK (v1.36.0)
  The reference paper routed ZERO TABLE on four candidate-comparison questions
  and ZERO LEVEL_DIAGRAM on three occupancy-decided ones, renderer live: each
  verdict defensible, the aggregate an under-firing router. So, per batch,
  before §18: if every candidate-comparison or every occupancy-/arrangement-
  decided question routed PROSE, re-run §6A-1 / §6A-1c on each. Survivors ship
  as they stood; failures are re-routed. No target rate; a paper with no such
  questions trips nothing.

## S6A-4 — Degrade LOUDLY, never silently, and never HALT
  If a required renderer is unavailable, or a rendered artefact fails its
  validation gate (§6A-5), the router steps DOWN one requirement — toward
  EQUATION, then PROSE — and the explanation still ships. A missing renderer
  must never halt a paper mid-run. (v1.35.0) The RECORDED verdict — in progress
  state AND on the block — becomes the DEGRADED requirement, with the reason,
  never the original: engine v2.6 raises on a visual verdict with no figure, so
  an un-updated verdict cannot even construct. But the degrade is DISCLOSED: recorded in
  progress.json, listed in the §20 report, and named in the delivery footer.
  Silent degradation is the worse failure: it makes quality vary invisibly
  between runs of the same spec, which is undiagnosable from the artefact.

## S6A-5 — A rendered artefact must be PROVED, not trusted
  Any generated figure carries a validation record, and a figure that fails its
  gate is never shipped (it degrades per §6A-4). The gate is renderer-specific
  and declared with the renderer in section_rules, but the CONTRACT is fixed:
  the artefact must be re-derived from the rendered output and compared against
  what was intended, not merely inspected. A structural renderer, for example,
  re-parses the drawn structure and compares a canonical identifier — molecular
  formula alone is insufficient, since two different answers commonly share one
  formula and a formula check would pass a swapped structure. Renderers must be
  DETERMINISTIC: the same question re-rendered must produce identical bytes, or
  no byte-level audit downstream can mean anything.
  WHAT THE GATE DOES NOT PROVE — state this plainly rather than over-claim. The
  gate proves the drawn artefact matches what was requested. It cannot prove the
  request was right; that judgement stays with the derive-twice protocol (§7).

## S6A-6 — Renderer execution contract (v1.28.0 — emission is LIVE)
  WHO RENDERS: the executing session, at solve time, inside this step — the same
  model Step 7 uses for its figural questions. There is NO renderer engine file
  and no routes.json change: rendering is spec-directed session work, and the
  ENGINE's job is confined to what an engine can guarantee (emission mechanics,
  the §6A-5 record check at construction, and the landing check at verify time).

  WHAT IS DECLARED WHERE. The exam's section_rules.md CATEGORY C may carry a
  `representation_renderers` block naming, per requirement, the library and the
  §6A-5 identifier discipline, e.g.:
      STRUCTURE_GRAPH : rdkit    — identifier = CANONICAL SMILES round-trip
                                   (render from SMILES; re-parse the intended
                                   SMILES; compare canonical forms — formula
                                   comparison alone is a §6A-5 violation)
      LEVEL_DIAGRAM   : matplotlib — identifier = the computed occupancy /
                                   ordering string, restated from the drawn data
      DATA_PLOT       : matplotlib — identifier = the plotted series' defining
                                   parameters
  ABSENT the block, the router degrades those verdicts to EQUATION/PROSE per
  §6A-4 — loudly, in the report — and the exam behaves exactly as pre-v1.27.0.

  DEPENDENCIES ARE PREFLIGHT WORK, NEVER MID-BATCH DISCOVERIES. P1 (its RENDERER
  PREFLIGHT sub-step — v1.40.0; this sentence said "P0", which is trigger detection and
  installs nothing) installs any library the exam's declared renderers name (pip, --break-system-packages, same
  pattern as matplotlib in Step 0) and RECORDS the preflight result in the §3
  dashboard. An install that fails does not halt: the affected requirement
  degrades per §6A-4 for the WHOLE run, disclosed up front, so quality never
  varies silently between batches.

  MECHANICS (engine v2.3, for the session's use):
    RepresentationFigure(path, width_in, validation, after_step)
      — validation is the §6A-5 record: renderer, intended, derived, match.
      — after_step: 0-based count of DEDUCTION sentences before the figure;
        default 1, so the sentence ABOVE the figure names what it shows.
    ExplanationBlock(..., figures=[...]) — validate() raises on any §6A-5 breach.
  RENDERING RULES the session must hold to:
    • DETERMINISM — same question, same bytes on re-render (§6A-5); seed or
      canonicalise anything stochastic.
    • ONE figure carries ONE decisive relationship. Two relationships = either
      two figures or (better) the simpler §6A-1 representation.
    • The figure paragraph carries NO text (engine-enforced invariant); every
      label the reader needs is drawn INSIDE the figure; the adjacent DEDUCTION
      sentence states what the figure decides.
    • Width 0.5..7.0 in; default 6.0 for a full-column scheme, ~4.0 for a
      single-panel diagram.
  FAILURE PATHS, all loud: a failed render or failed §6A-5 comparison → drop the
  figure, degrade the verdict per §6A-4, record it; a declared-but-unrendered
  figure at verify time → BLOCKING figure-landing FAIL (§18). No path ships an
  unproved image, and no path hides a skipped one.

# ════════════════════════════════════════════════════════════════════════
# §7 — ANSWER DERIVATION & VERIFICATION (no key delivered — derive it)
# ════════════════════════════════════════════════════════════════════════

## S7-0a — CAPTURE THE CONDITIONS BEFORE APPLYING ANY REMEMBERED RESULT (v1.32.0)
  A named reaction, standard formula or remembered result is a CONDITIONAL claim. Before
  applying one, read back from the stem every condition it depends on, and check the stem
  actually supplies them. NEVER apply a remembered name while ignoring its conditions —
  that is how a confident, fluent, WRONG answer gets produced, because the recalled name
  is right and only the conditions differ.
  CAPTURE every qualifier the stem attaches to the situation. WHICH qualifiers exist is
  DOMAIN-DEPENDENT and is read from the exam's own material (section_rules CATEGORY C
  cues + the subtopic), never assumed from this list. TYPICAL, NOT EXHAUSTIVE, and NOT a
  requirement that any of these appear: the ORDER in which things are applied · what is
  held constant · the stated regime or range of validity · the environment or medium ·
  any explicitly given rate, level, setting or state · the post-process or clean-up step.
  A paper in a domain where none of these apply simply captures nothing here and the rule
  costs it nothing.
  REFERENCE CASE (one domain, illustrating the shape — the failure is universal): an
  ozonolysis question turns entirely on the WORK-UP. The same
  substrate and the same ozone give an aldehyde under a reductive work-up and a carboxylic
  acid under an oxidative one. A solver who recalls "ozonolysis cleaves the double bond"
  and stops has recalled a true statement and will still answer wrongly half the time.
  A condition the stem supplies but the DEDUCTION never uses is a warning sign: examiners
  supply conditions because they DISCRIMINATE. If a stated condition changed nothing in
  the reasoning, re-read the question before proceeding.
  CROSS-STEP: §9's `wrong_condition` names this failure in a DISTRACTOR. This rule governs
  the SOLVER. They are different obligations and neither substitutes for the other.

## S7-0b — ASSUMPTION LEDGER (v1.32.0)
  Record every approximation the derivation leans on, at the moment it is used. WHICH
  approximations are conventional is DOMAIN- AND LEVEL-DEPENDENT; the exam's own material
  establishes them. ILLUSTRATIVE ONLY, across domains, and no item here is expected of any
  particular paper: an idealised model substituted for the real one · a small quantity
  neglected · a limiting or standard condition assumed · a second-order effect ignored ·
  a value taken at its reference state.
  THREE CASES, and only the third reaches the reader:
    1. The STEM supplies the assumption -> use it, no comment needed.
    2. It is the settled convention at this exam's level and does NOT change the answer
       -> use it silently.
    3. It MATERIALLY affects the answer -> STATE IT in the explanation, in the step that
       relies on it. A number that would differ under a different, equally defensible
       assumption is not a fact; presenting it as one hides the choice from the learner.
  An assumption may never CONTRADICT something the stem supplies. If it must, the stem
  wins and the conflict is an ambiguity signal (§17).

## S7-0c — ENUMERATION BEFORE FORMULA (v1.35.0)
  A counting question is never OPENED from a closed-form ceiling. The order is
  fixed: 1. INVENTORY the generating elements the count runs over; 2. CLASSIFY
  each element; 3. TEST INDEPENDENCE — whether every element genuinely varies
  freely of the others; 4. GENERATE the possibilities under the constraints
  actually present; 5. DE-DUPLICATE under every equivalence that applies
  (symmetry, relabelling, indistinguishability); 6. COUNT. A closed-form
  (a k^n or factorial shape) is legitimate ONLY AFTER step 3 verified the
  independence it assumes — and the DEDUCTION then shows the inventory and the
  de-duplication, never just the formula (the C-STRUCTURAL enumeration shape,
  §6-1, is this rule's rendered form).
  WHY. A ceiling formula applied first FEELS like a derivation and is the single
  most common wrong path in enumeration: it silently asserts an independence
  that step 3 would have refuted. ILLUSTRATIVE, one domain showing the
  universal shape: stereoisomer counting — the 2-to-the-n ceiling holds only
  for independent stereogenic elements, and dependent elements, internal
  compensation and symmetry each defeat it; the same failure shape appears in
  arrangement counting under symmetry and in state counting over
  indistinguishable members. The rule is the ORDER, not the domain.

## S7-1 — Derive-twice, never guess (every question, no exception — RE-6)

  1. FIRST PRINCIPLES: derive the answer using the correct method for the class.
  2. SECOND INDEPENDENT METHOD: re-solve by a genuinely different route — back-
     substitute the derived option, a different formula, elimination, SymPy for
     algebra, enumeration for arrangements. Not the same steps repeated.
  3. AGREE → proceed. DISAGREE → a THIRD independent derivation; take the 2-of-3 result
     and set DERIVATION-CONFIDENCE in progress.json + the §20 report.
  4. The second method is the natural SPEED HACK candidate: if it turned out to be a
     faster, structurally-different route, it becomes the SPEED HACK (§14); if it was
     mere back-substitution, there is no shortcut and the block omits SPEED HACK.
  5. NO DEFENSIBLE SINGLE ANSWER after all of the above → HALT-AND-ESCALATE (§17). Never
     guess: a wrong published key teaches thousands of students a wrong fact.

## S7-2 — Facts are web-verified, never recalled (RE-18)

  For C-FACTUAL content (and any factual option in any class), web-verify the keyed
  fact AND every option with a recorded source (date-stamped). The query carries the
  fact (the one MANDATE-0 exception, §0); the source goes in the §20 report, never in
  chat. An item that cannot be verified is flagged DERIVATION-CONFIDENCE, never
  certified from memory.

## S7-3 — Uniqueness expectation (RE-12)

  Step 7 builds exactly one defensible answer per question. The derivation must land
  on a single defensible answer: one option (mcq), one correct SET (msq), or one value /
  accepted range (nat). If an MCQ appears to land on two options, or an MSQ set is
  ambiguous, or a NAT value is not pinned, that is almost certainly an incomplete solve
  (a misread stem, an unmerged OMML stem, an unviewed figure) — go to §17 before
  concluding a defect.

## S7-4 — NAT portal grading value (v1.16, S7-NEW-C parity; NUMERICAL only)

  MOTIVATION: the derive-twice VALUE (S7-1) is the MATH answer — content-correct, but not
  automatically the exact string the delivery portal's auto-grader accepts (charset
  exactly "0123456789.-", no scientific notation, no units, no en-dash, no parentheses;
  confirmed against the portal's own answer-entry configuration). A value that is
  legitimately tiny (a stem stating "in units of 10⁻⁹") or that carries a tolerance band
  must be run through the SAME PURE, DETERMINISTIC transform Step 7 used when the question
  was created (`derive_nat_grading()`, Framework_MockTestCreate.md §S7-NEW-C) — never
  hand-formatted, never a naive `str()` of the derived value (a Python float `3.0` renders
  as `"3.0"`, not the portal-correct `"3"` — a real, distinct defect class from getting the
  math wrong). Because the function is pure, running it on the SAME (value, ca_range,
  stem_precision) triple Step 7 used is GUARANTEED to reproduce the SAME certified string —
  no sidecar read is needed; this is a determinism guarantee, not a lookup.

  PROCEDURE (every NAT question, after S7-1's value is pinned):
  1. `ca_range` (the numeric tuple, unchanged from existing practice): the tolerance band
     if the exam publishes one (nat_tolerance != 0), else None.
  2. `stem_precision`: detect mechanically from the STEM TEXT itself (the same text S7-1
     already reads) — an explicit "round off to N decimal places" / "correct to N decimal
     places" instruction gives int N; its absence gives None. This is a literal-phrase
     read, not a judgement call.
  3. Call `derive_nat_grading(value, ca_range, stem_precision)` below to get
     `(grading_type, grading_value)`. Populate the ExplanationBlock EXACTLY as follows —
     never any other construction:
       - `grading_type != 'range'`: `ca = grading_value` (the string, used as-is);
         `ca_range = None`.
       - `grading_type == 'range'`: `ca = _fmt_portal_number(value, precision=None)` (the
         central point value, charset-valid, used ONLY for the DEDUCTION-binding check —
         never displayed, since `ca_range` takes over CA-line rendering); `ca_range =
         (_fmt_portal_number(lo, stem_precision), _fmt_portal_number(hi, stem_precision))`
         — the SAME helper called directly on the two bounds (S5-1). This reproduces
         `grading_value` exactly by construction (it's literally how `_fmt_portal_range`
         builds it) without ever needing to parse a string back apart.
  4. If step 3's call to `derive_nat_grading` raises (the NOT-SUPPORTED negative-bound-
     range case), that is a well-posedness defect on the QUESTION, not a formatting bug —
     go to §17 HALT-AND-ESCALATE exactly as an unpinned value would (S7-3), never
     hand-work around it.

  ```python
  from decimal import Decimal, ROUND_HALF_UP
  import re

  _NAT_GRADE_CHARSET = frozenset('0123456789.-')
  _NAT_INTEGRAL_EPS = Decimal('1e-9')   # float-arithmetic-residue guard, NOT a domain call

  def _fmt_portal_number(value, precision=None):
      d = Decimal(str(value))
      if precision is not None:
          q = Decimal(1).scaleb(-precision)
          d = d.quantize(q, rounding=ROUND_HALF_UP)
          s = format(d, 'f')
      else:
          if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
              s = str(int(d.to_integral_value()))
          else:
              s = format(d.normalize(), 'f')
      if re.fullmatch(r'-0(\.0+)?', s):
          s = s.lstrip('-')
      return s

  def _fmt_portal_range(lo, hi, precision=None):
      lo_s = _fmt_portal_number(lo, precision); hi_s = _fmt_portal_number(hi, precision)
      if lo_s.startswith('-') or hi_s.startswith('-'):
          raise ValueError(f'NOT SUPPORTED negative-bound range lo={lo_s} hi={hi_s}')
      if Decimal(lo_s) > Decimal(hi_s):
          raise ValueError(f'lo>hi {lo_s} {hi_s}')
      return f'{lo_s}-{hi_s}'

  def derive_nat_grading(value, ca_range=None, stem_precision=None):
      if stem_precision is not None:
          if ca_range is not None:
              lo, hi = ca_range
              return ('range', _fmt_portal_range(lo, hi, precision=stem_precision))
          return ('decimal_fixed', _fmt_portal_number(value, precision=stem_precision))
      if ca_range is not None:
          lo, hi = ca_range
          return ('range', _fmt_portal_range(lo, hi, precision=None))
      d = Decimal(str(value))
      if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
          v_int = int(d.to_integral_value())
          return (('positive_integer', str(v_int)) if v_int >= 0 else ('integer', str(v_int)))
      return ('decimal', _fmt_portal_number(value, precision=None))
  ```

  PINNED: this function body MUST stay LOGIC-IDENTICAL to Framework_MockTestCreate.md
  §S7-NEW-C and audit_canonical.py's A-NAT-GRADE implementation (there named
  _derive_nat_grading) — never re-implemented independently (anti-drift by design).
  v1.40.0: "byte-identical" was the previous wording and was false — the three copies
  differ in docstrings, error-message text and line wrapping; the LOGIC was verified
  identical on 19 edge inputs (integral floats, -0.0, 1e-9 residue, ROUND_HALF_UP at a 5,
  negative bound, lo>hi). Any change to the logic is made in all three copies in one
  release and re-verified the same way. Three independent copies computing the SAME
  deterministic function on the SAME true inputs is the intended redundancy (matches Step
  8's own pinned-copy pattern); three DIFFERENT implementations would not be.

## S7-5 — NUMERICAL VERIFICATION (every quantitative answer, v1.32.0)
  Derive-twice (§7-1) catches a DIFFERENT-ANSWER error. It does NOT catch a CONSISTENT
  error: both routes can share one unit slip, one log base, one power of ten. These checks
  are orthogonal to it and are run on the final value before the block is written.
  EACH CHECK IS CONDITIONAL ON APPLICABILITY. A check whose subject the question does not
  contain is NOT APPLICABLE and is not a failure — a pure-arithmetic item has no units to
  verify, a word problem no conversion. Never manufacture a check to satisfy the list, and
  never treat a non-applicable check as a defect. The parenthetical examples span domains
  and are ILLUSTRATIVE ONLY.
    [ ] UNITS (if the answer carries one) — the result carries the unit the question asked
        for, and the working is dimensionally consistent throughout, not merely at the end.
    [ ] CONVERSIONS (if any quantity is expressed in more than one unit) — every quantity
        converted where the relation demands it, including any ABSOLUTE-SCALE requirement
        the relation imposes on a scaled quantity.
    [ ] MAGNITUDE — the order of magnitude is sane for what the quantity IS. A bounded
        quantity outside its bounds, or a length in the wrong power of ten, is an
        arithmetic slip, not a result.
    [ ] LOG / EXPONENT BASE (if a logarithm or exponential appears) — the base matches the
        constant used alongside it; a mismatched base silently rescales the whole answer.
    [ ] SIGN / DIRECTION (if the quantity is signed or directional) — the sign matches the
        direction the question defines (gain vs loss, forward vs reverse, in vs out).
    [ ] DEFINING RATIO (if the domain fixes one) — any conserved or defining ratio comes
        from the relation that DEFINES it, and that relation was balanced, normalised or
        otherwise completed BEFORE it was used.
    [ ] PRECISION — the answer is rounded exactly as the question asked, and no further.
        Rounding is applied ONCE, at the end, never to an intermediate that is then reused.
  A check that FAILS sends the question back to §7-1, never to a patched number.

## S7-6 — DECISIVE-CLAIM CONSISTENCY (every question, v1.35.0)
  Derive-twice (§7-1) compares final ANSWERS; the §7-5 checks audit the final
  VALUE. Neither reads the reasoning. This check does: before any prose is
  written, LIST the decisive intermediate claims the DEDUCTION will assert —
  the claims the answer actually turns on — and check them against each other:
    [ ] LOGICAL — no claim asserts what another denies.
    [ ] COUNT / NUMERIC — an element one claim excludes is not counted by a
        later one; totals equal their stated parts.
    [ ] SIGN / DIRECTION — a direction argued qualitatively is the direction
        the arithmetic then applies.
    [ ] CONSERVATION / BALANCE — whatever the domain conserves is conserved
        across the chain, not merely in the final line.
    [ ] IDENTITY — the object one claim establishes is the object later claims
        use, not a silently substituted variant.
  AN EXPLANATION WHOSE DECISIVE CLAIMS CANNOT ALL BE TRUE IS INVALID EVEN WHEN
  ITS FINAL ANSWER MATCHES the derived one: answer agreement can HIDE invalid
  reasoning, and a learner re-walking the chain inherits the contradiction.
  ILLUSTRATIVE, one domain showing the shape: "this centre is not an
  independent stereogenic element" followed by a count that treats it as one —
  the keyed answer can still come out right, and the explanation is still
  wrong. A failed check returns to §7-1 — the SOLVER re-derives; the
  contradiction is never patched in the prose (patching the sentence that
  exposed it leaves the reasoning it exposed).

## S7-7 — TRANSFER-SAFETY PROTOCOL (every AXIOM and every SPEED HACK, v1.36.0)
  An explanation is read twice: to check THIS answer, and later, on a
  DIFFERENT question, as a remembered rule. §7-1 to §7-6 prove the first
  reading; nothing proved the second. A statement can be correct for the item
  and a FALSE GENERAL RULE — true for the stem's substrate, false for its
  nearest neighbour — and every answer-level gate is blind to it because the
  answer was right. This protocol runs BEFORE AXIOM / SPEED HACK prose is
  written and its result is RECORDED, as §7-6 and §14-5 record theirs.
  FOR EVERY TRANSFERABLE CLAIM — each AXIOM sentence, each SPEED HACK, and any
  WHY WRONG / COMMON PITFALLS line phrased as a general rule:
    1. STATE THE INTENDED SCOPE. What class of situations is this claim meant to
       cover? A claim with no statable scope is not yet a claim (GEN_SCOPE_UNDEFINED).
    2. TYPE IT (§8-2): SCIENTIFIC_GENERAL_RULE · MODEL_DEPENDENT_RULE ·
       EXAM_CONVENTION · QUESTION_SPECIFIC_INFERENCE · OPTION_SET_SHORTCUT.
    3. NAME THE NEAREST LEGITIMATE NEIGHBOUR — the closest member of the same
       apparent class, AT THE TARGET EXAM'S LEVEL, that a learner would meet next.
       v1.37.0 — THE LOOKUP IS MECHANICAL. Each curated rule carries **Triggers:**
       (§24-1b). A trigger firing on the claim's sentence makes that rule's canonical
       counterexamples THE neighbour; the record cites neighbour_source
       CURATED:<rule-code>, and the engine refuses an AXIOM / SPEED HACK that matches a
       family it did not cite (GEN_CANONICAL_EXCEPTION_MISSED). GENERATED is admissible
       ONLY where no trigger fires.
    4. TEST the claim on that neighbour. Still true → SAFE.
    5. FALSE on the neighbour → REPAIR BY RETURNING TO THE MECHANISM, never by
       hedging: name the actual effect, class or condition that makes the claim
       true where it is true (NARROWED); or, if the fact is really about THIS
       item only, move it into the DEDUCTION (MOVED_TO_DEDUCTION); or, for a
       SPEED HACK, omit it (OMITTED, §14-1 part 3). Inserting "usually" is NOT a
       repair (it satisfies §8-0b and still teaches nothing about WHEN); listing
       every exception is NOT a repair either (§8-2 — the AXIOM does not get
       longer as the fix).
  THE RECORD (progress state + engine v2.7 `transfer_record`, shape-validated):
  one entry per claim {section, claim, epistemic_type, scope, neighbour_tested,
  outcome}; an AXIOM without an AXIOM entry or a SPEED HACK without a SPEED_HACK
  entry cannot construct; no QUESTION_SPECIFIC in AXIOM, no OPTION_SET_SHORTCUT
  outside SPEED HACK. The engine proves the protocol RAN; judging the neighbour
  stays with discipline, as §6A-5 proves the artefact and not the request.
  ILLUSTRATIVE, one domain, the PROCEDURE is the rule: AXIOM "an electron-
  withdrawing substituent directs meta"; neighbour at this level, chlorobenzene
  (withdrawing, ortho/para); claim fails; repair by mechanism — "a substituent
  that withdraws by resonance destabilises the ortho and para intermediates
  more than the meta one, so it directs meta" — true for item and neighbour,
  the halogen case excluded for a stated reason. Same shape in the reference
  paper: "one carbon richer" (non-methyl Grignards), "stable carbonylate = 18
  electrons" (stable 16e/17e), "identical halves always give a meso form".
  CROSS-STEP: §9's `overgeneralised_rule` names this failure in a DISTRACTOR;
  this rule governs the SOLVER'S OWN AXIOM (the §7-0a / `wrong_condition` pair).
  TRIPWIRE (v1.37.0): explain_engine.transfer_tripwire fires when ≥20 AXIOM claims carry
  0 NARROWED / MOVED_TO_DEDUCTION (the reference shape: 60 "SAFE on first try", seven
  unsafe); it obliges a recorded SECOND PASS over every AXIOM before §18 (§R12).

## S7-8 — KEY RECONCILIATION (every question, v1.37.0 — RE-23)
  Two independent solvers disagreeing is the most valuable check this pipeline can
  run; until v1.37.0 it never ran. MECHANISM (paper_pipeline v5.39): Step 7 writes
  registry.key_commitments[paper_id].entries[q] = {salt, h = sha256(paper_id|q|salt|
  canonical)}, canonical = '2' (mcq) · '2,3' (msq) · the NAT grading string. No
  plaintext exists anywhere Step 9 reads.
  THE PROTOCOL (per batch, after §7-1..§7-7, before §18): rec = explain_engine.
  reconcile_key_commitments(blocks, registry, paper_id). MATCHED → key_status MATCH.
  MISMATCHED → §17-3 for that question (rec.candidates[q] names the canonical the
  commitment accepts; mcq probed over all labels, msq/nat over the resolver's own
  alternatives). UNCOMMITTED (pre-v5.59 registry) → key_status UNAVAILABLE, proceed,
  say so in the dashboard and §R10 — never refused. RESOLVED_SOURCE writes NO file
  (§17-3b, v1.40.0). key_status per question ∈ MATCH ·
  RESOLVED_SELF · RESOLVED_SOURCE · UNAVAILABLE · DEFECT; unset cannot ship (§18).

## §7A-M — ADVISORY DIFFICULTY RE-MEASURE (MOCK-ONLY, v1.38.0 — REPORT, NEVER BLOCK)

  Counterpart of PYQExplain §7A under the adopted contract: both pipelines share
  the RUBRIC (blueprint_core.assess_difficulty) with different MECHANISMS. Mock
  difficulty is a SPECIFICATION enforced at authoring (MockTestCreate v5.60
  CHECK 3c / G-DIFF; audited by A-QINDEX 7/8), so Step 9 never re-decides a
  label — THE STICKER WINS. But only Step 9 re-derives every question
  INDEPENDENTLY, so it is the one honest cross-check of Step 7's evidence.

  MECHANISM (per question, zero extra solving): after §7-8, record what §7-1's
  derive-twice pass revealed, in the SAME observation shape Step 7 stores as
  difficulty_obs (CHECK 3c is the single source for the shape); compute _lab9 =
  blueprint_core.assess_difficulty(..., derivation_confidence per §7-1
  agreement); compare to question_index[q].difficulty. LEVEL ANCHOR: count
  steps/concepts for a competent candidate OF THIS EXAM (blueprint `level` +
  the subtopic's PYQ_DIFFICULTY_CALIBRATION); assumed prerequisite knowledge is
  recall (0 steps), never steps — Step 9's count stays commensurable with
  Step 7's rather than a granularity artefact.

  REPORT (the whole output): dashboard "§7A-M: k/n agree"; §R10 "DIFFICULTY
  RE-MEASURE (advisory): agree X/[total]; disagreements: Q[n] label=[L]
  re-measured=[M], ...". Disagreements NEVER block, edit the registry, or
  change an explanation; a large count is OPERATOR signal (§24 learnings —
  suspect Step 7's obs capture or a drifted regeneration). DORMANT (one §R10
  line) when the entry has no difficulty labels, the vocabulary is not 3-band,
  or blueprint_core is unavailable.
# ════════════════════════════════════════════════════════════════════════
# §8 — SECTION QUALITY STANDARDS (the highest-standard contract per section)
# ════════════════════════════════════════════════════════════════════════
#   Governing rule across ALL sections — the DENSITY FLOOR (not a length floor):
#   every line must add a NEW number, fact, or reason; NO sentence may restate another.
#   Brevity is allowed only when the line is dense; a line carrying none of its required
#   facts fails the content floor (v1.21.0: the no-restatement rule is enforced by the
#   writer alone — no audit step re-reads it).

## S8-0 — TWO CONTENT DISCIPLINES THAT BIND EVERY SECTION (vv1.31.0)
  These govern AXIOM, DEDUCTION, SPEED HACK and WHY WRONG / COMMON PITFALLS alike.
  Both were found in a delivered chemistry paper and both had NO rule against them.

### S8-0a — SUPPORTED VALUES ONLY (no invented precision)
  EVERY number an explanation asserts must come from ONE of exactly three places:
    1. the STEM (or its figure/table), 2. a constant the syllabus establishes, or
    3. a value DERIVED in the explanation itself, with the derivation shown.
  A number from none of those is INVENTED and must not be written. The reference
  defect: an elimination explanation asserted the major product forms "in about 70
  percent yield" — a figure the stem never gave, the syllabus never fixes, and no step
  derived. It reads as authoritative and is unfalsifiable by the learner.
  BANNED unless supplied or derived — stated as a SHAPE, since the specific quantities
  are domain-dependent: any efficiency, yield or success rate; any ratio between competing
  outcomes; any tabulated constant; any exact measured magnitude, position or setting; any
  real-world operating figure. ILLUSTRATIVE ACROSS DOMAINS, not a checklist to match
  against: a reaction yield, a market share, a population figure, a material property, a
  historical date, a device rating. If the paper's domain has no such quantities, the rule
  simply never fires.
  THE TEST — ask of every number: "where would a student LOOK to check this?" If the
  answer is not the stem, the syllabus, or a line above it, delete it. Deleting costs
  nothing: "the terminal alkene predominates" carries the entire teaching point that
  "forms in about 70 percent yield" was pretending to add.
  QUALITATIVE CLAIMS ARE NOT EXEMPT. "Much faster", "far more stable" are comparative
  claims; state the comparison's BASIS (the structural or energetic reason), not a
  magnitude the explanation cannot support.

### S8-0b — CALIBRATED LANGUAGE (a tendency is not an impossibility)
  Real systems express TENDENCIES. Stating a tendency as an absolute teaches a false
  rule that fails the student the first time they meet the exception.
  Reserve ABSOLUTES — impossible, forbidden, never, always, cannot — for claims that
  are absolute in the subject's own terms: a conservation law, a symmetry-forbidden
  process, a definition, a mathematical impossibility.
  Use CALIBRATED terms for everything else: predominates, is favoured, is disfavoured,
  is the minor pathway, is sterically hindered, is slower under these conditions.
  The reference defect: "a bulky base CANNOT approach the shielded hydrogens" — it
  demonstrably can, it is simply disfavoured, and the whole question turns on a
  competition between two accessible pathways. Writing it as impossible destroys the
  very reasoning the question tests.
  WHY WRONG IS NOT EXEMPT — arguably it matters more there. A distractor is usually
  wrong because it is DISFAVOURED or MISAPPLIED, not because it is impossible; saying
  a plausible option "cannot" happen leaves the student unable to see why anyone chose
  it. Name the condition under which it WOULD be right, then why it is not right here.
  A GENUINE absolute must still be stated absolutely — hedging a real impossibility is
  the same failure in the other direction.
  (v1.36.0) NOW A GATE, NOT ADVICE. "cannot be titrated directly at all", "gives no
  turbidity at all", "always collapses into a meso form" passed every check
  because nothing read the sentence's modality. Engine v2.7 raises on an
  undeclared universal (always · never · cannot · impossible · at all ·
  regardless of · irrespective of · no matter · whatever the · universally ·
  without exception · in all cases) in AXIOM, SPEED HACK, WHY WRONG, COMMON
  PITFALLS. To KEEP one, declare the sentence in absolutes_justified with why it
  is absolute in the subject's own terms — a declaration, not a ban. Plain
  quantifiers ("only two ions", "every formula unit", "exactly 208") are NOT
  gated: measured four-fifths false positives, and declaration spam is worse
  than no gate. Per-language pattern: EngineConfig(absolute_terms_re=...).

## S8-0c — FORMULA TYPOGRAPHY (v1.37.0 — RE-24; engine-applied)
  Reference paper: 71 pages, zero sub/superscript runs in explanations. Engine v2.8
  normalises every student sentence at construction (normalise_formula_text: element
  subscripts, ion charges, orbital / hybrid labels, π/σ; ⟦MATH:⟧ untouched; LOCANTS
  such as C2–C3 left alone) and raises FMT_UNFORMATTED_FORMULA on the residue. Write
  what it will not rewrite (η⁵-C₅H₅, ²³²Th) in Unicode or ⟦MATH:⟧. Per-exam switch:
  section_rules CATEGORY C `formula_typography: false`.

## S8-1 — Correct Answer
  Role: the one line the student trusts absolutely; the most dangerous line in the
  pipeline. Standard: INDEX/VALUE ONLY, in the paper's own label scheme, no option text —
  MCQ "Correct Answer: 3" (or "C" for a lettered paper); MSQ the full set "Correct
  Answer: 1, 3"; NAT the portal grading value from S7-4 — a plain value ("Correct Answer:
  47") or, when the exam publishes a tolerance band, the lo-hi range with NO parentheses,
  words, or en-dash ("Correct Answer: 46.50-47.50"). The retired
  "47 (accepted range 46.5–47.5)" wording is banned outright — it fails the delivery
  portal's grading charset on five separate counts (space, parens, letters, en-dash) and
  must never appear in a rendered document. Equals the independently
  derived answer; bound three ways (line = DEDUCTION binding = answer_keys.json). For a
  negative stem it is the option the stem asks to IDENTIFY, polarity-correct (§10a).
  Enforced: three-way binding asserted at write time; truth by derive-twice + web-verify
  + the §19 pre-delivery checklist (no second reader — v1.21.0).

## S8-2 — AXIOM
  Role: the transferable concept — the rule/formula/theorem/definition that makes this
  CLASS solvable; a student who reads only the AXIOM learns the principle. Standard: ≥1
  dense sentence; sentence one states the core principle as a TRUTH ("the sum equals the
  average times the count"), never as a task ("we need to find the sum"); never restates
  the question. TEACH THE WHY, NOT JUST THE WHAT: where the rule has a reason, state the
  MECHANISM that makes it true, because the mechanism is what transfers to the next
  question — "a train clears a platform only when its rear passes the far edge, so the
  distance is train + platform" beats the bare "speed = total length ÷ time"; "6 = 2 × 3
  with 2 and 3 coprime, so a multiple of 6 must pass both tests" beats "even with digit
  sum divisible by 3" (the coprime reason generalises to 12, 15, 35). A bare formula with
  no reason is the weakest acceptable AXIOM; prefer the one-sentence statement that also
  carries its why. Content is class-conditional and PYQ-grounded — what it must state per
  subtopic is read from section_rules (RE-9). A forced second sentence is how restatement
  creeps in; one dense sentence is preferred when it fully states the rule AND its reason.
  THE AXIOM NEVER NAMES AN OPTION LABEL (v1.35.0) — binding the answer is the
  DEDUCTION last step's job (§8-3); an AXIOM naming one has leaked the conclusion
  into the principle. Enforced: ≥1 sentence, one-per-paragraph, banned-phrase scan,
  no option reference in the AXIOM (engine v2.6); "truth not task",
  "why not just what", correctness by discipline alone (v1.21.0).
  EPISTEMIC TYPE AND SCOPE-IN-SENTENCE (v1.36.0). Every AXIOM carries one recorded
  type (§7-7): SCIENTIFIC_GENERAL_RULE — stands once scoped; MODEL_DEPENDENT_RULE —
  names its model INSIDE the sentence ("spin-only", "using the radius-ratio rule",
  "for an ideal gas"); EXAM_CONVENTION — usable, phrased so the learner can tell
  ("under standard Lucas-test conditions"); QUESTION_SPECIFIC_INFERENCE — DEDUCTION
  only; OPTION_SET_SHORTCUT — SPEED HACK only. The qualifier is part of the rule,
  not a caveat after it (the §14-3b posture).
  Which conventions the exam expects is read from the subject learnings (§24)
  and section_rules CATEGORY C `exam_conventions`, never assumed. PRESERVE THE
  EXAM'S NOTATION: an older-convention option is still the keyed option; the
  DEDUCTION teaches the cleaner form without an answer conflict.
  THE AXIOM DOES NOT GET LONGER AS THE FIX: a failed claim is repaired by a
  narrower MECHANISM, never by an appended exception list ("… usually … except").

## S8-3 — DEDUCTION
  Role: the reproducible spine — AXIOM → answer with every intermediate value shown, so
  the student re-walks it and gets the same result. Standard: ≥2 steps, one sentence
  each, each showing its actual value ("235 ÷ 5 = 47", not "simplifying we get 47"); no
  "clearly", no skipped algebra; every fraction in OMML; the LAST step contains "Option
  N" (N = ca). Load-bearing tokens (decisive numbers, the final value) are bolded so a
  strong student reads only the bolded path (fast lane) and a weaker one reads the full
  line (full lane) — both served by one block. Enforced: ≥2 steps + last-binds-Option-N
  + OMML + one-per-paragraph + zero glyphs (engine); chain completeness + arithmetic
  truth by derive-twice + back-substitution (no second reader — v1.21.0).
  TOPIC MINIMUM-CONCEPT COMPONENTS (v1.36.0). Compression also teaches false rules:
  a ligand-field geometry reduced to "a strong ligand pairs the electrons"; alkyl
  activation explained as lone-pair resonance; a capacity maximum without its
  fixed-total-concentration condition. For each archetype the subject learnings
  file (§24) lists the SEMANTIC COMPONENTS a DEDUCTION must state before its
  conclusion — a minimum, not a template. §5-3 ticks every component for every
  archetype present. WHICH archetypes exist is SUBJECT DATA; this spec only
  requires that a loaded list is satisfied.

## S8-4 — SPEED HACK
  Role: exam-craft — a genuinely shorter route to the SAME answer, for time pressure;
  optional by design. Standard: a structurally DIFFERENT, faster path (not the same
  steps reworded); same CA; one or two dense lines; names the actual lever ("test
  divisibility by 3 first", "back-solve from the options", "only 39 fits"). Vague
  encouragement ("do it mentally", "obvious with practice") is banned — that is a
  platitude, not a hack. Inclusion is decided per question by §14; if no honest shortcut
  exists the block is OMITTED, never padded. Enforced: if present, binds the same CA
  (engine); "genuinely faster, not cosmetic" by discipline alone (v1.21.0). (v1.36.0) A third requirement joins the
  two: the shortcut is TRANSFER-SAFE (§14-1 part 3) — it passed the §7-7 neighbour
  test, it is not weaker than a one-line exact method, and an option-dependent
  trick is phrased as ELIMINATION ("strike every option whose sign is negative"),
  never as a law of the subject. A hack that works only because of the options
  shown is OPTION_SET_SHORTCUT and says so in its own wording.

## S8-5 — WHY WRONG (mcq / msq) · COMMON PITFALLS (nat)
  Role: where most learning happens — the SPECIFIC error a student commits to land on a
  wrong choice, inoculating against that exact mistake. Standard (the anti-template
  contract, §15): keys = exactly the NON-selected options (for MSQ, every option not in
  the correct set; never a selected one, never skipping one); 1–2 DENSE lines each; the
  first line DELIVERS its §9 diagnosis in natural language — the type itself is
  recorded internally (§9), never rendered — and must ACTUALLY produce that
  option's value/content
  (back-derive the distractor — "if a student did X they get exactly this option"); the
  line also carries the corrected value ("13 × 3 = 39, not 36"). No two wrong options
  share an explanation. For negative stems the true options are "a TRUE statement,
  therefore NOT the answer" — never "incorrect" (§10a). For factual classes every reason
  is a web-confirmed fact.
  NAT analogue — COMMON PITFALLS: a NAT question has no options to reject, so this section
  lists the wrong VALUES a student most commonly computes, ≥1, each headed by the value
  and naming the slip that yields it in natural language ("forgetting to divide leaves
  235 unchanged"; "dividing by the wrong count gives 9.4 instead"), the §9 type
  recorded internally. Same anti-template discipline:
  each pitfall must reproduce a real wrong value, none generic. Enforced: key set (mcq/msq)
  or ≥1 value-keyed pitfall (nat) + ≥1 sentence + ZERO internal taxonomy tokens in
  rendered text (engine v2.6) + banned templates/glyphs (engine); diagnosis recorded
  internally + reproduces-the-wrong-answer + factual truth by discipline
  alone (v1.21.0).

# NOTE (v1.13): the former S8-6 (figure_note, rendered under ⬛ FIGURE) is REMOVED.
#   Figural questions no longer emit any FIGURE section; the rendered order for EVERY
#   question type is Correct Answer → ⬛ AXIOM → ⬛ DEDUCTION → (⚡ SPEED HACK) →
#   ❌ WHY WRONG? / ❌ COMMON PITFALLS. The figure itself stays in the question region
#   (byte-identical, §12); how a figural AXIOM / DEDUCTION / WHY WRONG is written is
#   governed by C-FIGURAL (§6-1) and the image-viewing protocol (§13), both unchanged.

# ════════════════════════════════════════════════════════════════════════
# §9 — ERROR-TYPE TAXONOMY (name one in each WHY WRONG first line)
# ════════════════════════════════════════════════════════════════════════
#   Exam-agnostic. The named type must ACTUALLY produce the option (§15).

  | Error type            | When it applies                                              |
  |-----------------------|--------------------------------------------------------------|
  | value_swap            | a correct value used for the wrong quantity                  |
  | sign_error            | wrong arithmetic sign (added vs subtracted)                  |
  | unit_error            | wrong units (km vs m; minutes vs hours)                      |
  | off_by_one            | result of n instead of n±1 (counting, sequencing, inclusive count) |
  | partial_truth         | correct for part of the question but misses a condition      |
  | process_confusion     | right values, wrong process (multiplied instead of divided)  |
  | reversed_relationship | a relationship inverted (A→B read as B→A)                    |
  | name_swap             | correct fact attributed to the wrong entity/person/place     |
  | formula_error         | wrong formula applied (CI used as SI)                        |
  | rounding_trap         | correct calculation, wrong rounding                          |
  | polarity_flip         | a true statement called false / false called true (neg. stem)|

  SCIENTIFIC / STRUCTURAL TYPES (v1.27.0). The eleven types above are shaped for
  aptitude papers and force a science distractor into an ill-fitting label — a
  regiochemistry slip logged as "off_by_one" tells the learner nothing. These are
  additive; the ban on writing a WHY WRONG line with NO type is unchanged.

  | Error type            | When it applies                                              |
  |-----------------------|--------------------------------------------------------------|
  | wrong_condition       | right transformation, wrong stated condition (work-up, solvent, pH, temperature, order of addition) |
  | regiochemistry_error  | correct reaction at the wrong position / site                |
  | stereochemistry_error | wrong configuration, or some stereocentres inverted not all  |
  | mechanism_confusion   | a different mechanism's product (substitution for elimination, etc.) |
  | electron_count_error  | miscounted electrons / occupancy / oxidation state           |
  | symmetry_error        | equivalence or a mirror plane wrongly asserted or missed     |
  | overgeneralised_rule  | a valid rule applied outside its stated validity domain      |
  | concept_reversal      | the governing relationship applied in reverse                |

  Unknown patterns default to the closest type; never write a WHY WRONG line without one.

  INTERNAL DIAGNOSIS, NATURAL RENDERING (v1.35.0). The error type is METADATA.
  It is still MANDATORY — every wrong option / pitfall is diagnosed with exactly
  one §9 type, recorded per option in progress state (alongside the derived
  answer in answer_keys.json / progress.json) — but the snake_case token NEVER
  appears in student-facing text. The visible first line DELIVERS the diagnosis
  in the subject's own natural language ("this is the para product, formed only
  when both ortho positions are blocked"), never as a machine label
  ("regiochemistry_error: ..."). REFERENCE INCIDENT: a delivered 60-question
  paper opened all 40 WHY WRONG entries and all 20 NAT pitfalls with the raw
  token — obeying the old "first line names an error type" literally. ENFORCED:
  engine v2.6 raises at write time on any §9 token in a rendered sentence and
  re-scans the rendered bytes at verify time; the reproduce check (§15-2) is
  unchanged and still binds in full.

# ════════════════════════════════════════════════════════════════════════
# §10 — SPECIAL-CASE PROTOCOLS
# ════════════════════════════════════════════════════════════════════════

## S10a — Negative stem (the deadliest content trap)
  Trigger: the stem contains a negation cue. The cue LIST is language-configurable (read
  from section_rules CATEGORY C; the English default is NOT / EXCEPT / INCORRECT / FALSE /
  "does not" / "cannot be"), so the protocol works for any-language papers (scanned BEFORE
  writing). CA = the option the stem asks to identify (usually the FALSE one). DEDUCTION
  gives one truth-verdict line for EVERY option, then isolates the target. Each WHY WRONG
  entry's first line states the option is a TRUE statement (hence NOT the answer),
  polarity_flip recorded internally (§9) — NEVER calls a true statement "incorrect"
  (that teaches false information), and never renders the token. This cannot be machine-proven; the §5-3 checklist tick is why this
  protocol exists.

## S10b — Composite options
  Trigger: options combine items ("Both 1 and 2", "Only 1 and 3", "All of the above",
  "None of the above"; trigger phrases configurable per CATEGORY C). Establish the truth
  value of EVERY underlying statement first (one DEDUCTION line each), THEN map the
  combination to the option. WHY WRONG for a composite names the exact component that
  breaks it ("Statement 2 is false, so the pair fails" — the §9 type recorded
  internally), never a blanket rejection.

## S10c — MSQ (multiple-select) and NAT (numerical-answer) protocols
  MSQ: treat like a composite spread across options — DEDUCTION gives a truth-verdict line
  per option, then the LAST step states the full correct SET (binding every selected
  "Option L(i)"); ca is that set; WHY WRONG covers every NON-selected option (why each is
  excluded). The CA line lists the set. Never collapse an MSQ to a single option, and
  never leave a selected option unexplained in the DEDUCTION verdict chain.
  NAT: there are NO options — derive the VALUE (derive-twice, §7), bind it in the last
  DEDUCTION step (the DERIVED VALUE, in natural form — the DEDUCTION prose is not held to
  the portal charset, only the CA line is), run it through `derive_nat_grading()` (S7-4)
  to get the portal-safe grading value/type, and set ca/ca_range from THAT output (never
  the raw derived number) exactly as S5-1 specifies. Write COMMON PITFALLS (the wrong
  values students compute + the slip for each) in place of WHY WRONG — pitfall labels are
  explanation prose, not graded, so they are unaffected by the portal charset and may use
  natural notation (including fractions). A fractional NAT value renders as OMML (§11) IN
  THE DEDUCTION/PITFALL prose; the CA line itself is always the plain grading-value string
  from S7-4, never a fraction or OMML — a NAT answer that is naturally a fraction is
  converted to its decimal equivalent by `derive_nat_grading()` before it ever reaches the
  CA line. Carrying why_wrong on a NAT block (or common_pitfalls on an option block) is a
  write-time error.

# ════════════════════════════════════════════════════════════════════════
# §11 — MATH / OMML RENDERING DISCIPLINE
# ════════════════════════════════════════════════════════════════════════
#   Every piece of math in an explanation is real OMML built through one validated
#   funnel — never inline text, glyph, or LaTeX. Same OMML standard Step 7 generates
#   under: one math standard across the whole document.

## S11-1 — The single funnel (write-time enforced)
  All prose enters via add_math_text(), which auto-converts every digit/digit fraction
  to stacked OMML and RAISES ValueError on: an inline fraction it cannot convert —
  including non-numeric forms (1/x, 1/(x+1), 1/√2, x²/2, (a+b)/c), which must be built
  explicitly with the helpers — an end-of-sentence fraction ("= 3/4." — add a trailing
  word), a consecutive-year slash ("2025/26" → use en-dash "2025–26"; a genuine n/(n+1)
  fraction whose denominator is NOT year+1 is left alone), a vulgar glyph (½ ¾ ⅓ … ⅒) or
  the Unicode fraction slash (U+2044), or bare LaTeX written directly INTO PROSE
  ("\frac", "\sqrt", "$…$"). Units km/h, m/s are letter/letter and are left as text.
  Exponents, surds, trig, n-ary and stacked formulae use the explicit helpers (frac, sup,
  sqrt, nary, omath) → true OMML nodes, not Unicode approximations.

  SCOPE OF THE LaTeX BAN — READ THIS BEFORE CONCLUDING MATH IS FORBIDDEN (v1.27.0).
  The ban above applies to RAW PROSE ONLY. It does NOT apply inside a ⟦MATH:…⟧ region,
  where backslash notation is the CORRECT and REQUIRED spelling. Reading the ban as
  global is the documented cause of GAP-2026-08-19-EXPLAIN-MATH-NOTATION: sessions
  concluded that notation was unsafe and VERBALISED arithmetic instead ("0.0591 divided
  by 2", "the square root of 32 divided by 4", "2 raised to the power 2"). That is a
  DEFECT, not a house style. Quantitative work is written as MATH.

## S11-1b — The ⟦MATH:…⟧ Tier-3 grammar (authoritative; what actually compiles)
  A ⟦MATH:…⟧ region is compiled by t3_mathcomp.t3_compile and becomes ONE <m:oMath>.
  Regions may sit inline mid-sentence or stand as their own display line. The grammar
  below is VERIFIED against the shipped compiler — use it verbatim.

  | Need               | WRITE THIS              | NEVER THIS   | Because                    |
  |--------------------|-------------------------|--------------|----------------------------|
  | fraction           | \frac{0.05912}{2}       | 0.05912/2    | / stays flat text          |
  | radical            | \sqrt{3RT/M}            | sqrt(3RT/M)  | compiles to literal text   |
  | subscript          | K_{sp}                  | K_sp         | binds ONE char → "Kₛp"     |
  | superscript        | x^{10}                  | x^10         | binds ONE char             |
  | both               | E_{cell}^{0}            | E_cell^0     | → "E_c el l^0"             |
  | Greek              | \Delta_{o} · \theta     | Delta_o      | → "Delt aₒ"                |
  | n-ary              | \int_{0}^{\infty}       | int_0^infty  | → "in t₀^i nfty"           |
  | over/vector        | \bar{A} · \vec{E}       | bar(A)       | literal text               |

  THE ONE RULE THAT REMOVES ALL AMBIGUITY: **every sub/superscript is BRACED, always.**
  An unbraced script cannot be judged mechanically — "_2SO" in H_{2}SO_{4} is a correct
  one-character subscript while "_2g" in t_{2g} is a wrong two-character one, and the two
  are indistinguishable. Bracing everything removes the guess. Unicode symbols (Δ, θ, ℏ)
  may be used DIRECTLY and need no backslash; it is the ASCII NAME that must be escaped.

  ENFORCEMENT (engine v2.2). guard_sentence now runs t3_notation_guard over every
  ⟦MATH:⟧ body and RAISES at AUTHORING time — at block construction, not at render —
  naming the exact remedy. Before v2.2 the compiler checked GRAMMAR but never NOTATION,
  so all four wrong spellings above shipped SILENTLY with every gate green. Note the
  division of responsibility: t3_mathcomp.py is byte-locked to Framework_PYQPrepare
  §S3-5b by the engine self-test drift lock and is NEVER edited from this side — the
  guard lives in explain_engine.py, which is the consumer.

## S11-1c — When quantitative work MUST be rendered as math (not prose)
  If a step performs a calculation, it is written as a ⟦MATH:⟧ region. Verbalised
  arithmetic is a DEFECT. Concretely, any DEDUCTION step that states a governing
  relation, substitutes values, or reports a computed result carries the relation, the
  substitution and the result as math — the reader must be able to CHECK the arithmetic,
  which prose denies them.
    WRITE : the governing relation, then the substitution, then the value, each its own
            ⟦MATH:⟧ line — e.g. ⟦MATH:E = E^{0} - \frac{0.05912}{n}\log Q⟧
    NEVER : "the coefficient is 0.0591 volts divided by 2, that is 0.02955 volts"
  A purely qualitative explanation (a recall fact, a mechanism in words) needs no math
  and must not manufacture any — S11-1c is a floor on quantitative work, never a quota.

## S11-2 — Post-write verification (every batch)
  After writing, verify_explanations() re-parses the RENDERED docx and re-confirms every
  <m:f> fraction has a non-empty numerator AND denominator and that none is a year-range
  artefact, and re-scans the rendered prose for any inline or vulgar fraction that slipped
  the funnel. This is viewer-independent and read back from the FILE, not the in-memory
  blocks — it proves the math is present and well-formed in the delivered bytes (§18).

## S11-3 — The Word-native limit (disclosed, never misdiagnosed)
  OMML is Microsoft Word's native math format and renders perfectly in Word (the
  delivery target). LibreOffice / pandoc / many docx→PDF/HTML pipelines silently drop or
  mangle OMML — so a previewer may show broken math on a CORRECT file. This is a
  rendering-environment artefact, never a document defect. The deliverable and the §20
  report state plainly: FINAL VISUAL REVIEW MUST BE DONE IN MICROSOFT WORD, so a
  LibreOffice preview is never mistaken for a bug.

# ════════════════════════════════════════════════════════════════════════
# §12 — CONTENT-FIDELITY PRESERVATION (append-only; byte-identity)
# ════════════════════════════════════════════════════════════════════════
#   Step 9 never COPIES question content — it PRESERVES the original in place and only
#   APPENDS (RE-3). There is no code path in Step 9 that writes question content; only
#   paths that write explanation content and move existing content unchanged.

## S12-1 — What is guaranteed byte-identical to the Step-7 source (verified EVERY batch)
  • Stem + option TEXT (paragraph lines), and <w:u> underline / bold runs.
  • OMML: the <m:t> math-text sequence + node count per question (a math-bearing or
    pure-OMML stem is read math+text MERGED in document order, never judged "empty").
  • Images / figures / charts: every drawing's rId resolves to the SAME media part;
    per-paragraph drawing counts identical; every media part MD5-identical (a
    recompressed or dropped image fails).
  • Tables / matrices / DI grids: table count + row/column counts + the full cell-text
    grid compared cell-by-cell.

## S12-2 — How (the architecture, not a promise)
  build_interleaved_docx seeds the CLEAN Step-7 source WHOLE and inserts explanation
  paragraphs only AFTER a question's last option — never inside a region, never touching
  a question paragraph, never re-creating an image or re-typing OMML. verify_fidelity
  compares the output's every question region to the immutable source (kept read-only in
  /home/claude) after every batch (§18). Corruption cannot accumulate unseen because the
  comparison is always against the pristine original.

## S12-3 — Two independent confirmations (beyond the fidelity diff)
  • STRIP-AND-RE-AUDIT: strip_solutions() produces a questions-only copy; the Step-7
    paper auditor runs on THAT (never the combined doc — running it raw scans
    explanation prose as paper content and false-alarms). It must pass identically to
    the Step-7 input. INVOKE IT WITH THE FULL CONTRACT — --registry --blueprint
    --rules --manifest --mockN — or A-OPTN fails NOT ASSESSABLE on every NAT Q (F4).
  • COUNT INVARIANTS: output question count, options/question, image count, table count
    and OMML count == the Step-7 input exactly. v1.21.0: nothing re-verifies these
    counts downstream — this per-batch check is the only one that runs.

## S12-4 — INTERIM COVERAGE BANNER (vv1.31.0 — the artefact declares its own state)
  EVERY delivered .docx carries a DOCUMENT-LEVEL coverage banner as its first line,
  written via explain_engine.set_coverage_banner() (engine v2.4).
  WHY THIS EXISTS. Coverage was announced only in the chat progress line, so the FILE
  said nothing about itself. A partially-explained paper — a legitimate mid-run
  artefact under the batch law — is byte-for-byte indistinguishable from a finished
  one the moment it leaves the conversation. In the reference incident a Batch-1 file
  carrying 10 of 60 explanations was reviewed by a third party as a completed
  document, and the review's central complaint was simply the 50 questions the batch
  had not reached yet. The chat line was correct and did not travel with the file.
  CONTENT — MANDATE-0 SAFE, counts and ranges ONLY, never stem or answer text:
    interim : "Batch k of K - Q[a]..Q[b] explained of [Q_TOTAL]. NOT FINAL - further
               batches pending."
    final   : "Complete - all [Q_TOTAL] questions explained."
  The banner is REPLACED each batch, never stacked (set_coverage_banner is
  idempotent), and the final batch overwrites the interim wording.
  WHY IT NEEDED ENGINE SUPPORT, not spec text alone: a banner is framework-added
  content, not paper content, so strip_solutions() MUST remove it — otherwise the
  questions-only copy differs from the Step-7 source and the §12-3 re-audit fails.
  That was verified empirically before this rule was written: with the banner present
  and unstripped, verify_fidelity still PASSES (the banner sits outside every question
  region) while the strip comparison FAILS. Engine v2.4 strips it; the self-test
  BANNER-STRIPPED-CLEAN locks that, and BANNER-GATES-UNAFFECTED locks that fidelity,
  structure and explanation verification are all undisturbed by its presence.

# ════════════════════════════════════════════════════════════════════════
# §13 — FIGURAL DEEP-ANALYSIS PROTOCOL (view every image — no exception)
# ════════════════════════════════════════════════════════════════════════
#   No ExplanationBlock for a figural question may be built until every image in that
#   question has been extracted, role-bound, and VIEWED. Reasoning around the picture
#   from surrounding text alone is forbidden (RE-11).

## S13-1 — Detect figural questions structurally
  A question is figural if its region contains a <w:drawing> in the STEM or in any
  OPTION (read from the docx XML) — plus section_rules figural cues and registry
  figural_manifests[]. Two PLACEMENTS, handled distinctly: IMAGE-IN-STEM (a figure to
  reason about) and IMAGE-AS-OPTIONS (each option is itself a figure).

  AND — v1.29.0 — TWO FAMILIES, which decide HOW the figure is READ. Placement and
  family are independent: either family can appear in either placement.
    • TRANSFORMATION-PUZZLE — the figure carries no domain meaning; the answer lies in
      a geometric or set operation on abstract marks. Series, analogy, odd-one-out,
      mirror/water image, paper folding, cube net, embedded/counting figures, space
      orientation. (Typical of reasoning sections: SSC, CAT, IBPS, police/defence.)
    • SCIENTIFIC-DIAGRAM — the figure DENOTES something, and the answer depends on what
      it denotes, never on its pose on the page. Molecular structures and reaction
      schemes, stereochemical projections (Fischer/Newman/chair/wedge-dash), orbital and
      energy-level diagrams, circuits, ray diagrams, free-body and vector diagrams,
      graphs, spectra, titration curves, maps, anatomical and biological diagrams,
      apparatus schematics. (Typical of subject papers: JAM, GATE, NEET, JEE, boards.)
  DECIDING THE FAMILY: read section_rules figural cues and the subtopic; if the marks
  in the figure have NAMES in the syllabus (an element symbol, a bond, an axis label, an
  orbital, a component), it is SCIENTIFIC-DIAGRAM. Abstract shapes with no such naming
  are TRANSFORMATION-PUZZLE. When genuinely mixed, read it as SCIENTIFIC-DIAGRAM: the
  stricter reading (§13-4b) never damages a puzzle, whereas reading a structure as a
  puzzle loses the chemistry entirely — the failure this split exists to prevent.

## S13-2 — Extract, role-bind, view (the gate before solving)
  Extract the actual image bytes from the docx media parts, render them, and bind each
  to its exact role (which is the problem figure, which is option 1, option 2, …) using
  the 1:1 image↔label binding Step 7 built. VIEW each labelled image
  before deriving. The binding matters: an unbound view can derive the right shape but
  key the wrong index.

## S13-2b — SEMANTIC-OBJECT RECONCILIATION (v1.37.0 — BEFORE solving)
  Never reason from pixels directly. For every viewed image FIRST transcribe what it
  depicts in the machine-readable form of its kind (paper_pipeline.SEMANTIC_KINDS:
  STRUCTURE as SMILES, REACTION as reaction SMILES, others as typed descriptors) with
  parse_confidence HIGH / MEDIUM / LOW, persisted in progress state. THEN:
    • registry.figural_manifests[].semantic_objects[q] present (Step 7 v5.59+) →
      paper_pipeline.semantic_objects_agree(mine, theirs) per role. AGREE → solve
      from the object. DISAGREE → re-view and re-transcribe ONCE with the registered
      name known; still DISAGREE → §17-3. The registered object is a CROSS-CHECK as
      the manifest always was; pixels still win when §17-3's proof says so.
    • absent (older paper, PYQ) → the transcription stands alone; rdkit sanitisation
      (explain_engine.canonical_structure — v1.40.0: it lives in the ENGINE, not in
      paper_pipeline; it never raises and returns (canonical|None, reason)) still runs on
      every STRUCTURE — a 'parse_error' reason is a misread. A reason of
      'rdkit_unavailable' (the P1 renderer preflight did not install it) is NOT a misread:
      the transcription stands at its own parse_confidence, the omission is recorded once
      in the dashboard and §R12, and an answer-critical STRUCTURE then carries
      DERIVATION-CONFIDENCE (§R5). Only kinds the exam actually emits invoke this; an exam
      with no STRUCTURE objects never touches rdkit. LOW confidence on an answer-critical figure →
      re-view; still LOW → DERIVATION-CONFIDENCE (§R5).

## S13-3 — Derive from the images, NOT the manifest
  figural_manifests[].answer_position records what Step 7 INTENDED to draw — a render
  bug is exactly what produces a wrong figure, so the manifest is a CROSS-CHECK, never a
  key. VIEW → derive → compare. Agreement → proceed. Disagreement → re-derive; if the
  pixels still win, trust the image, flag DERIVATION-CONFIDENCE, and HALT-AND-ESCALATE
  the possible render defect to the author (§17). v1.21.0: no audit step ran the A-FIG*
  pixel gates over this paper unless Step 7 ran audit.py, so a render defect reaching
  here is more likely than it was — escalate it, never explain around it. Manifest
  absent (it is chat-scoped) → derive without it; the strip re-audit waives the manifest
  requirement (§12-3).

## S13-4 — Write what is visible; never anomaly-for-figural (BOTH families)
  Common to both: DEDUCTION cites CONCRETE features actually visible, never a generic
  gesture at "the figure". WHY WRONG names, per wrong option-figure, the specific
  difference that makes it wrong. (v1.13: no separate figure-description line is
  rendered — the figure sits in the question region above; images are still VIEWED
  before solving, §13-2 / RE-11.) anomaly is NEVER used merely because options are
  images — a figural question always has a derivable answer once viewed.

## S13-4a — TRANSFORMATION-PUZZLE family (unchanged behaviour)
  AXIOM = the visual rule (rotation / reflection / element add-remove / count /
  net-folding). DEDUCTION traces the VISIBLE transformation step by step to the chosen
  option. This is the pre-v1.29.0 protocol, preserved: for a genuine reasoning puzzle
  it was correct and stays correct.

## S13-4b — SCIENTIFIC-DIAGRAM family (v1.29.0)
  AXIOM = the DOMAIN PRINCIPLE the figure is testing — never "the visual rule". The
  figure is notation for a fact, so the governing fact is the axiom.
  READ THE FIGURE AS NOTATION, IN THIS ORDER, BEFORE SOLVING:
    1. IDENTIFY what is drawn, in the domain's own terms (which compound, which circuit,
       which quantity on which axis, which orbital set).
    2. TRANSCRIBE the decisive features EXACTLY: bonds and bond orders, charges, wedge/
       dash direction, ring size, substituent identity and position, atom numbering,
       stereo-descriptors, reagent ORDER above/below the arrow, axis labels and units,
       component values, arrow directions, occupancy.
    3. Only then SOLVE, from that transcription.
  THE PROHIBITION THAT MATTERS MOST: never infer an unreadable feature from whatever
  would make an option work. A figure read backwards from a plausible answer produces a
  confident, wrong, unfalsifiable explanation. If a decisive feature cannot be read,
  re-view at higher resolution; if it still cannot be read, HALT-AND-ESCALATE (§17) —
  this is exactly the §13-3 render-defect path, not a case for judgement.
  POSE IS NOT MEANING. A scientific figure means the same thing rotated, reflected or
  redrawn. Two structures drawn differently may be the SAME compound; two drawn
  identically apart from one wedge may be DIFFERENT compounds. Never reason from
  page-orientation, and never treat a redrawing as a transformation — that is the
  §13-4a reflex misapplied, and it is wrong here.
  PRESERVE THE QUESTION'S OWN REPRESENTATION. If the stem poses a Fischer projection,
  reason in Fischer; a Newman stays Newman; a chair stays chair. Translating between
  representations adds a conversion step the question never asked for and imports its
  own error. Convert ONLY when the conversion IS the thing being tested.
  WHY WRONG for this family names the DOMAIN error (§9's scientific types —
  regiochemistry_error, stereochemistry_error, electron_count_error, symmetry_error,
  wrong_condition, … — INTERNAL names, recorded per §9 and never rendered), never a
  merely visual difference: "the double bond is at C3
  rather than C2" is the explanation; "the shape differs" is not.

# ════════════════════════════════════════════════════════════════════════
# §14 — SPEED HACK INCLUSION GATE (derivation-driven; omit, never fake)
# ════════════════════════════════════════════════════════════════════════
#   SPEED HACK earns its place ONLY when a path reaches the answer with materially less
#   work than the DEDUCTION — fewer/cheaper operations, not the same operations in fewer
#   words. If the fastest honest route IS the DEDUCTION, there is no SPEED HACK; OMIT.

## S14-1 — The two-part test (BOTH must pass, else omit)
  1. DISTINCT METHOD: the shortcut uses a different operation than the DEDUCTION —
     elimination by the most-discriminating feature, a divisibility/parity/unit-digit
     check, back-solving from options, a ratio/approximation, a known pattern. Same
     steps as the DEDUCTION → fails part 1.
  2. GENUINELY FASTER: it removes at least one full computation, or reaches the answer by
     checking one feature instead of resolving all, or lets the student stop before the
     formal solve completes. A one-step saving on a five-step solve does not qualify.
  3. TRANSFER-SAFE (v1.36.0): read alone, stripped of the question, the shortcut survives
     the §7-7 neighbour test at this exam's level; it does not replace a one-line
     exact method with a weaker heuristic (SPD_SHORTCUT_WEAKER_THAN_EXACT_METHOD);
     it does not work merely by accident of the options shown — and where it IS
     option-dependent, it is phrased as option ELIMINATION, never as a rule of the
     subject; and no common, examinable, answer-reversing exception stands
     unqualified (SPD_COMMON_EXCEPTION_UNQUALIFIED). "No aromatic ring → least
     acidic", "stable carbonylate = 18 electrons", "identical halves → meso" each
     passed parts 1–2 and fail part 3. ALL THREE must pass (title kept for
     cross-reference; the test is three-part).

## S14-2 — The operational proxy (applied per question at solve time)
  "Could a trained student pick the correct option WITHOUT performing the full DEDUCTION
  — by exploiting structure, the options, or a property?" YES → write it (must land on
  the same CA). NO → omit. The second derivation (§7) is the natural candidate.

## S14-3 — Where shortcuts live vs do not
  C-COMPUTATIONAL / C-FORMAL-LOGIC frequently admit real shortcuts (divisibility, unit-
  digit, alligation, ratio-jump, back-solve, parity, discriminating-feature filter).
  C-FACTUAL has none (you know a fact or you do not) → omit as a rule. C-LINKED (RC): the
  fast move is pointing to the licensing line, already in the DEDUCTION → omit. C-VOCAB
  is usually recall → omit unless an elimination trick genuinely exists.
  NAT (C-NUMERICAL-INPUT) is usually C-COMPUTATIONAL → actively look for a cleaner route
  (a different scaling, a unit shortcut, a property), since NAT solves are often the most
  shortcut-rich; do NOT default to omitting it just because there are no options. MSQ
  (C-MULTI-SELECT): the classic shortcut is eliminate-by-the-most-discriminating-property
  (strike every option failing one cheap test before doing the full per-option check) —
  include it when that cheap test genuinely removes options for free. This falls out of
  the TEST (§14-1/§14-2), never from hardcoded section ranges.

## S14-3b — EVERY SHORTCUT CARRIES ITS VALIDITY DOMAIN (v1.32.0)
  A SPEED HACK is the line a student memorises. That is what makes it useful and what
  makes an unscoped one the most damaging sentence in the block: it is recalled verbatim,
  under time pressure, in a question where its conditions do not hold.
  So every SPEED HACK states — in the shortcut itself, not in a caveat afterwards — the
  CONDITIONS under which it is safe. The scope is part of the shortcut, not an apology
  attached to it.
  The example below is from one domain; the SHAPE is what transfers — an unscoped rule
  states an outcome, a scoped one states the outcome AND the situation that triggers it.
    NEVER : "a bulky base always gives the less substituted alkene"
    WRITE : "when two beta-sites compete and the base is hindered, check the less
             substituted alkene FIRST"
  Note the difference from §8-0b. That rule bans stating a tendency as an absolute; this
  one requires the SCOPE to be present at all. "A bulky base usually gives the less
  substituted alkene" satisfies §8-0b and still fails here — it is calibrated but
  unscoped, so it never tells the student WHEN to reach for it.
  A SHORTCUT THAT CANNOT BE SCOPED IN ONE CLAUSE IS NOT A SHORTCUT. If stating the
  conditions takes longer than the DEDUCTION, the honest outcome is to OMIT (§14-1) —
  the §14 default has always been omit, never fake, and an over-broad shortcut is a
  species of fake.
  THE TEST: read the shortcut alone, stripped of the question. Could a student apply it
  to a question where it is WRONG and never notice? If yes, it is unscoped — fix or omit.

## S14-4 — The honesty guard
  If you cannot state the SPECIFIC lever that saves SPECIFIC work, there is no SPEED HACK
  — omit it. An empty or generic SPEED HACK is a DEFECT, treated like a wrong
  answer. The pressure runs toward omission, never fabrication.

## S14-5 — ELIGIBILITY IS RECORDED; THE DISTRIBUTION IS A TRIPWIRE (v1.35.0)
  For EVERY question, record the §14-1 outcome in progress state next to the
  representation verdict: {distinct_method, genuinely_faster, scoped} and the
  include/omit decision. §R3 reports the inclusion RATE alongside the count.
  WHY. The two-part test binds per question and nothing measured the aggregate,
  so inclusion pressure compounded invisibly: the reference paper carried a
  SPEED HACK on 56 of 60 questions — 93 percent — several of them restating the
  DEDUCTION in fewer words, a §14-1 part-1 failure each. A per-question rule
  with no distribution check is how a paper drifts to hack-everywhere while
  every individual decision felt defensible.
  THE TRIPWIRE, never a quota: if EVERY question in a batch carries a SPEED
  HACK, re-run the §14-1 test on each of them before §18. A hack that fails its
  re-audit is REMOVED (omit, never fake); a genuinely shortcut-rich batch —
  they exist — survives its re-audit unchanged and ships as it stood. No target
  rate exists in either direction; §16-1's pattern-matching cause is what an
  all-hack batch signals, and a re-test is the proportionate response. (v1.36.0) The record carries FOUR fields {distinct_method,
  genuinely_faster, scoped, transfer_safe}; §R3 reports hacks OMITTED on part 3.

# ════════════════════════════════════════════════════════════════════════
# §15 — WHY WRONG / COMMON PITFALLS ANTI-TEMPLATE STANDARD (the diagnosis contract)
# ════════════════════════════════════════════════════════════════════════
#   Templating happens because, when the writer does not truly know why a distractor (or
#   a wrong VALUE) is wrong, a generic line ("this option is incorrect") is sayable for
#   ANY of them. The fix is a CONTENT requirement no template can satisfy. The contract is
#   identical for an option-keyed WHY WRONG (mcq/msq) and a value-keyed COMMON PITFALLS
#   (nat) — "option" below means "option or wrong value" throughout.

## S15-1 — The rule that kills templating
  Every WHY WRONG / COMMON PITFALLS line must contain the specific WRONG PATH that
  produces THAT option's value — what mistake a student makes and what wrong number/fact
  it yields, traced to this exact option or value. Different wrong answers cannot come
  from one mistake, so if two of them share an explanation, the rule is violated by
  definition.

## S15-2 — Four hard requirements per wrong option / value
  1. DIAGNOSE with exactly one §9 error type — recorded internally (§9) while the
     first line delivers that diagnosis in natural language: a diagnosis, not a
     dismissal, and never the raw token (engine v2.6 raises on one).
  2. PROVENANCE BEFORE EXPLANATION (v1.37.0 — REWRITTEN; engine v2.8 gate). Two modes,
     recorded per wrong option / value in ExplanationBlock(error_provenance=…):
       MODE A — VERIFIED_ERROR_PATH: name the wrong operation AND give the engine an
         arithmetic expression (`recompute`) with the `target`; the block is REFUSED
         unless the result reproduces the target at its own precision (DST_UNVERIFIED_
         NUMERICAL_ORIGIN). A non-numeric target records the wrong CONTENT produced and
         `matches_target: true` after checking it IS this option. Only MODE A may say
         "doing X gives Y".
       MODE B — DIRECT_CONTRADICTION: no path claimed; the line states why the option /
         value contradicts the correct relation ("uses n = 1, but two electrons are
         transferred, so the correction is twice too large"). DEFAULT when no path
         verifies.
     THE PREVIOUS WORDING — "a real path always exists … go solve it" — IS WITHDRAWN:
     obeyed literally it produced "2.2 + 9.4 without halving gives 7.2" (11.6), "693 is
     1/k" (144), "rms/average near 1.414" (1.085) and 24 hedged lines ("or otherwise /
     perhaps by / or a similar") — now engine-banned here (DST_HEDGED_PROVENANCE). When
     a path does not verify, MODE B is the correct line, not a better-sounding MODE A.
  3. CARRY the corrected value — what the right step gives instead ("13 × 3 = 39, not 36";
     for NAT, "…, not 90"). The explicit contrast to the correct answer is mandatory, not
     optional.
  4. NO two wrong options/values share wording; NO banned template sentences (engine-scanned).

## S15-3 — Class- and type-specific shape (never generic across types)
  Computational → the arithmetic slip + the wrong number. Factual → what the option
  ACTUALLY is (the corrected fact). Negative stem → "TRUE, therefore not the answer"
  (never "incorrect"). Composite → the exact component that breaks it. Vocab → the
  precise nuance missed. RC → the passage line that REFUTES the option.
  MSQ → OPTION → the WRONG FEATURE or ASSUMPTION → the DECISIVE CORRECTION (v1.36.0): name
  the test the statement passes and the test it fails, as CONTENT — "it shares the
  metal and the d count, and differs in the ligand field, which pairs every electron
  in one complex and leaves two unpaired in the other" — so the line teaches the trap
  as a property of the subject, not of the learner. Two distractors that fail "the
  same way" must still differ in WHICH test they pass. THE PREVIOUS WORDING ("lead
  with the SEDUCTIVE HALF … a hasty solver") is WITHDRAWN: obeyed literally it opened
  10 of 10 MSQ blocks with "The seductive half is …", narration that proves nothing.
  A distractor is refuted by the subject; a thought process may be named only where
  the §9 diagnosis IS a known misconception, stated as the mechanism producing the
  option. Engine v2.7 raises on the phrases (DST_UNSUPPORTED_LEARNER_PSYCHOLOGY).
  NAT (COMMON PITFALLS) → head each entry with the wrong VALUE a student computes, name the
  slip that yields exactly it (MODE A, recomputed) or the contradiction (MODE B), and
  carry the contrast to the correct value. NO QUOTA (v1.37.0): ≥1 entry; a second only
  when a second VERIFIED path exists, never for symmetry.
  Density without thinness: 1–2 lines, each carrying a required fact; one informative line
  beats two padded ones, but a line carrying none of the required facts fails the content
  floor.

# ════════════════════════════════════════════════════════════════════════
# §16 — QUALITY-CONSISTENCY (ANTI-DECAY) ARCHITECTURE
# ════════════════════════════════════════════════════════════════════════
#   Quality decay over a long run is a PREDICTABLE property, not a moral failing, so the
#   defence is structural, not "try harder". Four named causes, each blocked.

## S16-1 — The causes
  (1) context dilution (by Q60 the window crowds out the current question); (2) pattern-
  matching auto-fill (remembered shape instead of solving THIS question — the source of
  templated WHY WRONG); (3) floor-gaming (writing to the minimum that passes); (4) no
  fresh checkpoint (the bar quietly lowers).

## S16-2 — The defences (none weakens as the mock lengthens)
  • BATCHING IS THE LEVER (cause 1): ≤ ceiling per batch with a HALT for confirmation
    means the context never fills with 60 prior solves; each batch starts fresh with the
    full standard re-loaded. This is why all-at-once is a MANDATE-level breach (MANDATE B).
    Autonomous mode waives the HALT but NOT the per-batch fresh-context processing (RE-0).
  • STANDARD RE-ASSERTED EACH BATCH (cause 4): the §5-3 checklist + §8 floors are
    actively re-applied each turn, not remembered from batch 1.
  • CONTENT FLOORS, NOT LENGTH FLOORS (cause 3): §8 / §15 demand option-specific facts a
    template cannot supply — laziness FAILS the check instead of passing it padded.
  • PER-BATCH WHOLE-DOC SELF-AUDIT (§18): a thin or malformed block cannot hide mid-mock;
    every batch ships the full cumulative doc so any drop is visible in context.
  • UNIFORM MECHANICAL GUARANTEES: every engine guard fires identically on Q1 and Q97 —
    a write-time ValueError does not get lenient because the run is long.
  • DERIVE-TWICE HAS NO EXCEPTIONS (§7): no "confident by now, skip the check" path.
  • THERE IS NO INDEPENDENT NET (v1.40.0 — this bullet previously described a live Step
    10 re-reading every explanation with a CA1–CA7 gate; Step 10 was RETIRED at v1.21.0
    and §18-2 says so). The §18 per-batch read-back of the WRITTEN document is the last
    mechanical check this paper receives, and the §R8 handoff is the only record a human
    reviewer gets. Neither may be softened on any batch (RE-0).
  The guarantee is not "I never write a weaker line" — it is "a weaker line CANNOT REACH
  THE STUDENT", caught at four independent layers that do not weaken with length.

# ════════════════════════════════════════════════════════════════════════
# §17 — DEFECT HANDLING (halt-and-escalate, never fix)
# ════════════════════════════════════════════════════════════════════════
#   v1.21.0 — THE PRIOR IS WEAKER THAN IT WAS. The paper carries Step 7's own generation
#   gates and its per-batch self-audit, but NO independent audit layer has re-derived a
#   single answer. If a question looks wrong, an INCOMPLETE SOLVE on Step 9's part is
#   still the likelier explanation and §17-1/§17-2 still bind — but a real Step-7 defect
#   is now materially more plausible than it was under a certified paper, so a claim that
#   survives §17-1/§17-2 is to be escalated promptly rather than assumed self-inflicted.

## S17-1 — The burden of proof is inverted (RE-12)
  "This question/option is wrong" is a conclusion of LAST RESORT, never a reaction to
  difficulty or surprise. Before a defect may even be SUSPECTED, all of these must hold:
  solved from first principles AND a second method that DISAGREE or land on no option;
  full stem + all options re-read to the end (most "it's wrong" reflexes are a misread or
  a missed "NOT"); OMML merged with text (a pure-OMML stem reads blank — not "missing
  data"); for figural, the images actually VIEWED (§13); and no wrong-convention-on-my-
  part. Only then is "possible defect" a legitimate hypothesis.

## S17-2 — "Wrong" must be specific and reproducible
  A defect claim must state PRECISELY what is defective and prove it with a concrete
  derivation ("two options both satisfy the stem as printed — here are both", or
  "computed value 47 matches no option under any stated rounding"). A claim that cannot
  be reproduced is not a defect — it is a Step-9 error; go solve the question.

## S17-3 — RESOLUTION PROTOCOL (v1.37.0 — in-run; the paper never halts)
  Entered on a §7-8 mismatch, a §13-2b disagreement, or a §17-1 suspicion; run
  INSIDE the session, each step recorded in progress.json:
    1. RE-READ stem and every option to the end; re-merge OMML.
    2. Figural → re-extract, re-VIEW, re-transcribe with the registered NAME known
       (§13-2b); rdkit sanitisation.
    3. A THIRD and a FOURTH independent derivation, one being back-substitution of
       EVERY option / the committed candidate (§7-8).
    4. Web-verify any fact the disagreement turns on (§7-2), source recorded.
  OUTCOMES (exactly one, recorded as key_status — §7-8):
    (a) RESOLVED_SELF — Step 9 was wrong (the usual case): correct the block,
        continue. No operator action.
    (b) RESOLVED_SOURCE — a reproduced derivation that ALSO agrees with the registered
        semantic object and web-verified facts proves Step 7's key wrong while the
        question is sound: publish the proven answer in the docx, record key_status =
        RESOLVED_SOURCE with the proving §17-3 step and source reference in progress.json,
        and report it in §R10. No file is written (v1.40.0 — the former key_corrections.json
        had no consumer: MockDeliver preserves the docx 'Correct Answer:' line verbatim, and
        a plaintext corrections file is exactly the artefact the §7-8 hashing design and
        S19-1 checks 4/5 forbid). The registry commitment stays as written — it is frozen
        here and no downstream step reads it as a key. No operator action for delivery;
        the §R10 line is the operator's cue to add an EX-rule (§24) so Step 7 does not
        repeat the error.
    (c) DEFECT — §17-4.
  Step 9 never edits content (RE-3) and never publishes a key that did not survive
  steps 1–4.

## S17-4 — A PROVEN QUESTION DEFECT (v1.37.0 — reported, never adjudicated by the operator)
  When steps 1–4 show the QUESTION is defective — the figure contradicts its own
  registered object, or two answers are provably defensible as printed — that block
  carries the INTERNAL anomaly flag (never rendered), the paper COMPLETES for every
  other question, and §R7 lists the defect with its evidence plus ONE copy-paste
  regeneration line for that question. The operator runs it; nothing is judged by
  hand. v5.59's creation-time gate (structure drawn FROM its SMILES) makes (c) rare.

## S17-5 — Why this cannot become lazy defect-calling
  The escalation path is deliberately EXPENSIVE (reproduced derivation + halt + bounce to
  the author for a Step 7 re-run), while solving is the path of least resistance. The
  cheap escape that drove the bad reflex no longer exists. v1.21.0: no downstream step
  catches a wrongly-flagged clean question or a waved-through misread, so §17-1's
  preconditions must be met in full before any claim is raised.

# ════════════════════════════════════════════════════════════════════════
# §18 — PER-BATCH SELF-AUDIT (the Audit-A analogue; producer self-certification)
# ════════════════════════════════════════════════════════════════════════
#   Runs after EVERY batch over the WHOLE cumulative doc (not just the new batch), so a
#   fix in one batch cannot silently break an earlier one. v1.21.0: this is Step 9's own
#   gate AND the last gate — no independent re-audit follows it.

## S18-1 — The checklist (all must hold before present_files — MANDATE D)
```text
  [ ] every block this run: ExplanationBlock.validate() clean (engine)
  [ ] verify_fidelity(out, Step7_source): whole question region byte-identical, every
      image rId resolves to a relationship (no dangling embed) (§12)
  [ ] verify_structure(out, blocks, expected = Q1..last(batch k)): coverage exact,
      NO look-ahead, header order + CA binding intact (§4 / §5)
  [ ] verify_explanations(out, blocks) -> (ok, problems): INDEPENDENT post-render re-audit
      of the rendered docx — re-reads the written bytes (not the in-memory blocks) and
      re-checks header order, the type-aware CA binding read back from the document,
      WHY-WRONG / COMMON-PITFALLS coverage, zero banned glyphs / metacommentary / templates
      / inline or vulgar fractions in rendered prose, one sentence per rendered paragraph,
      every OMML fraction well-formed with no year-range artefact, AND the Tier-3 degrade
      ledger (§11 S11-2). BLOCKING CONTRACT — the verifiers RETURN status, they do NOT raise:
      assert ok is True AND problems == [] AND explain_engine.T3_STATS['failed'] is empty.
      A non-empty degrade ledger (a ⟦MATH:⟧ region that fell back to raw plain text) is a
      BLOCKING FAIL — present_files FORBIDDEN. A run that checks only "did the call raise"
      is NON-CONFORMING. (As of 2026.08.10.3 ExplanationBlock.validate() also compiles any
      ⟦MATH:⟧ region and RAISES at construction, so this ledger is normally empty; the
      assertion is the second gate. v1.27.0 CORRECTION: the parenthetical that stood here
      previously — "so ⟦MATH:⟧ regions are rare here" — was itself the defect. It read as
      licence to avoid math, and sessions duly verbalised arithmetic instead. ⟦MATH:⟧
      regions are NORMAL and EXPECTED wherever a question is quantitative (§11 S11-1c),
      and engine v2.2's t3_notation_guard rejects mis-compiling notation at construction.)
  [ ] §6A router verdict present for EVERY question in this batch AND carried on
      each block (engine coherence — a visual verdict requires its figure, a §6A-4
      degrade carries the degraded requirement); every §6A-1b structure-answer
      question either emits STRUCTURE_GRAPH or its PROSE justification is recorded;
      every degrade disclosed in the report; zero verbalised-arithmetic steps in a
      quantitative DEDUCTION (§11 S11-1c). A missing verdict is a BLOCKING FAIL — an
      unrouted question silently reverts to the pre-v1.27.0 prose-only default,
      which is the defect this router exists to remove.
  [ ] SPEED-HACK ELIGIBILITY recorded per question (§14-5); if every question in
      this batch carries a SPEED HACK, the §14-1 re-audit was run and any hack
      failing it removed BEFORE this checklist                              (§14-5)
  [ ] REPRESENTATION DISTRIBUTION + DEGRADE LEDGER captured for this batch's questions,
      ready for §R3; an empty ledger recorded AS empty, never omitted            (§20 R3)
  [ ] FIGURE LANDING (v1.28.0): verify_explanations confirms every block's declared
      figures rendered — declared N, landed N, per question. A mismatch is a BLOCKING
      FAIL; a figure dropped by §6A-4 degrade is REMOVED from the block (so declared
      == landed == the degraded count) AND disclosed in the report, never left
      declared-but-missing.
  [ ] COVERAGE BANNER set for this batch via set_coverage_banner(); wording states
      batch k of K and the explained range; strip_solutions still yields a copy
      byte-equal to the Step-7 source (§12-4 / §12-3)
  [ ] count invariants: image / table / OMML / question / option counts == Step-7 input
  [ ] strip-and-re-audit: questions-only copy passes the Step-7 auditor identically (§12-3)
  [ ] every CA fact web-verified with a recorded source (§7 / RE-18)
  [ ] derived answers flushed to answer_keys.json; CA three-way binding holds
  [ ] coverage assertion (S4-5 guard 3): the whole doc carries explanations for EXACTLY
      Q1..last(batch k) — no fewer, no more; a collapsed or look-ahead run fails HERE
      (this is the producer-side mechanical scope check; RE-0 forbids waiving it)
  [ ] learnings coverage (§24): every question's applicable AL/EX rules were routed; no
      loaded rule for a present class was silently skipped; the SUBJECT-level file, when
      present in the project, was loaded and its neighbour library used by §7-7
  [ ] TRANSFER-SAFETY RECORD (v1.36.0) present for EVERY question (§7-7) and
      passed into its block; every AXIOM typed; zero QUESTION_SPECIFIC claims
      in an AXIOM; zero kept absolutes undeclared
  [ ] REPRESENTATION ALIGNMENT (§6A-1c) recorded; §6A-3b tripwire evaluated
  [ ] SPEED HACK part-3 outcomes recorded (§14-5 four-field record)
  [ ] (v1.37.0) KEY RECONCILIATION run (§7-8): every Q carries key_status, zero
      MISMATCHED unresolved · SEMANTIC OBJECTS (§13-2b): every transcription persisted
      and compared · ERROR PROVENANCE mode counts captured (§15-2) · transfer_tripwire
      evaluated, second pass recorded if fired (§7-7) · §6A-1b-ii Qs emit the
      enumerated objects or carry a recorded justification
```
  Any item open → fix, re-build, re-audit. present_files is FORBIDDEN until ALL hold.
  All hold → SELF_AUDIT_CLEAN = True; coverage assertion passed → COVERAGE_OK = True
  (S4-4 D; read by S19-1).
  Why verify_explanations exists alongside verify_structure: the latter re-validates the
  in-memory block OBJECTS, the former re-parses the RENDERED ARTIFACT. Trusting the build
  is not the same as verifying the output — a future renderer change or a build bug
  could write something the construction-time guards never saw, and only an
  independent read-back of the document catches it.

## S18-2 — THERE IS NO INDEPENDENT GATE (v1.21.0 — stated, not hidden)
  Step 9's §18 above is PRODUCER self-certification, and with Step 10 retired it is the
  ONLY certification this document will ever receive. The former independent half —
  `explain_audit_gate.py --audit-progress ...` asserting CA1–CA7 over an evidence-bound
  ledger — is no longer run for mock/scoped papers by any step. (v1.21.1: the module
  explain_audit_gate.py has been REMOVED from the framework — its sole remaining
  consumer, PYQExplainAudit, was retired.)
  CONSEQUENCES, binding:
  • The per-question evidence Step 9 records (derived answers, web-verified facts,
    viewed-image confirmations, DERIVATION-CONFIDENCE flags) is still recorded IN FULL and
    still handed off (RE-20). Its consumer is now a human reviewer, not a gate. Recording
    it is NOT optional merely because nothing machine-reads it.
  • Producer↔auditor drift is no longer a risk because there is no auditor; the risk that
    replaces it is PRODUCER SELF-DECEPTION, which §18-1's read-back-the-written-document
    checks (not self-report) are the only defence against. Run them literally.
  • RE-0 forbids any preference from weakening §18. That prohibition is now the single
    load-bearing guarantee of this step and admits no exception.

# ════════════════════════════════════════════════════════════════════════
# §19 — DELIVERY (incremental whole-paper; one present_files per batch)
# ════════════════════════════════════════════════════════════════════════

## S19-1 — Pre-delivery checklist (MANDATORY before present_files)
```python
import os
out = '/mnt/user-data/outputs'
# PAPER_SLUG = pp.paper_slug(paper_id) of the blueprint mock/paper resolved at P1 (v1.19).
# "Mock[N]" zero-padded for a mock, else the scoped slug — same value the input
# _Create.docx filename carries (v1.24: previously named the retired "_Complete" form).
sol = f'{EXAMCODE}_{PAPER_SLUG}_Explanation.docx'
present = set(os.listdir(out))
BANNED = ('answer', 'key', 'ledger', 'progress', 'state', 'pickle', 'stripped', 'source')
# v1.40.0: scan every file EXCEPT the Solutions docx. A scoped slug or exam code can
# legitimately contain a banned substring (TOPIC_…_SOLID_STATE_01, …_STATE_PSC_…);
# check 5 already asserts outputs == {sol}. PYQExplain S19-1 has the same exclusion.
leaked = [f for f in present - {sol} if any(b in f.lower() for b in BANNED)]
checks = [
    ('1 solutions docx in outputs',      os.path.exists(f'{out}/{sol}')),
    ('2 self-audit (S18) all clean',     bool(globals().get('SELF_AUDIT_CLEAN'))),
    ('3 whole-paper coverage asserted',  bool(globals().get('COVERAGE_OK'))),
    ('4 no internal sidecar leaked',     not leaked),
    ('5 outputs == exactly the solutions docx', present == {sol}),
]
fails = [n for n, ok in checks if not ok]
if fails:
    raise SystemExit('HARD STOP (S19-1): ' + '; '.join(fails) +
                     '. Fix, then re-run S19-1. Do NOT call present_files yet.')
```
  Stage ONLY the Solutions docx in outputs; keep the clean source + all state in
  /home/claude. registry.json is NOT delivered (frozen; it already lives in the project).

## S19-2 — The single present_files call (per batch)
```python
def present_files(paths):
    """CLASS: T — the chat file-delivery tool. NOT executable python.

    GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), DEFECT-CLASS SWEEP.
    This spec CALLED present_files() from compiling python while DEFINING it
    nowhere — a guaranteed NameError the moment the path executes as python. Five
    such call sites stood across four specs (Framework_MockTestAnalyse.md twice,
    Framework_PYQScan.md, Framework_PYQExplain.md, Framework_MockTestExplain.md).
    It reached production because spec_name_audit_baseline.json accepted
    `present_files` as a known-unbound name in all four.

    SAME SHAPE as D2 of GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, where
    collect_drive_docx_recursive() called the CLASS T marker gdrive_search() from
    python. That gap fixed the INSTANCE; the CLASS stood eleven days longer.

    Declared per-spec, matching this corpus's CLASS T house pattern (gdrive_search
    is declared in both Framework_MockTestAnalyse.md and Framework_PYQCount.md).
    The F1/F2 footer contract is owned by Framework_DeliveryFooter.md.

    The model performs the call in its own turn, after python returns. Nothing is
    returned to python and NO call site may consume a result (C6).
    """
    pass  # CLASS: T — performed by the model between turns, never from python
present_files([f'/mnt/user-data/outputs/{EXAMCODE}_{PAPER_SLUG}_Explanation.docx'])
```

## S19-3 — Progress line + confirmation request (ENDS the turn — MANDATE B)
  Print a MANDATE-0-safe line: "Batch k of K delivered — Q[a]..Q[b] explained; Q1..Q[b]
  now carry solutions, Q[b+1]..Q[end] unchanged. SPEED HACK on m of these; DERIVATION-
  CONFIDENCE on j (listed by Q-number)." Then ask: "Reply 'continue' for Batch k+1." END
  THE RESPONSE — do not begin the next batch. (Interactive mode; autonomous mode prints
  the progress line and proceeds without the confirmation request — MANDATE B / RE-0.)

## S19-4 — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat progress line (S19-3),
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Use locally — always for Explanation.docx), and next-step reference.

Step 9 uses BOTH footer types:
  - F1 (amber) after each non-final batch (same Explanation.docx, incrementally filled)
  - F2 (green) after the final batch (same Explanation.docx, now fully explained)
```

# ════════════════════════════════════════════════════════════════════════
## §20 — END-OF-MOCK REPORT (after the FINAL batch's confirmation; MANDATE-0 safe)
# ════════════════════════════════════════════════════════════════════════
  §R1 PROVENANCE: mock N · registry state · blueprint reference · THIS spec's version
      as read from its own header · the engine self-test line EXACTLY as the engine
      printed it · timestamp · EngineConfig (option count(s), label scheme, language,
      terminators) actually used.
      v1.29.0 — BOTH VERSIONS ARE READ, NEVER PINNED. This line previously carried the
      literal "spec v1.13 · engine 62/62" and was still carrying it at spec v1.28.0 /
      engine 78/78, misreporting the very thing provenance exists to record. Any exact
      count written here goes stale the moment a fixture is added — the same failure
      mode as GAP-2026-08-13-STALE-SELFTEST-PIN, which is why the GATES are floor-form
      (§18, "N/N PASS with N >= 62"). A report line is not a gate and must not become
      one: report what ran, assert nothing.
  §R2 VERDICT: SHIP (delivered) / HALTED (escalation) — first line, unambiguous.
  §R3 COVERAGE: Q_TOTAL/Q_TOTAL explained · question-type split (mcq/msq/nat counts) ·
      SPEED HACK count AND inclusion rate (Q-numbers; §14-5 — a near-total rate on a
      mixed-class paper is the §16-1 pattern-matching signal; report it, do not
      editorialise) · OMML object count in explanations · per-class
      derived-answer distribution (counts only).
      REPRESENTATION (v1.29.0 — the §6A-3 distribution this line was promised to carry):
        • verdict counts across PROSE / EQUATION / TABLE / STRUCTURE_GRAPH /
          LEVEL_DIAGRAM / DATA_PLOT / CONFORMER, plus the Q-numbers for every non-PROSE
          verdict.
        • figures declared vs figures landed (must be equal — §18 blocks otherwise).
        • DEGRADE LEDGER: every §6A-4 step-down, with the Q-number, the requirement
          asked for, what it degraded to, and WHY (renderer absent / preflight failed /
          §6A-5 validation mismatch). An EMPTY ledger is stated explicitly as empty —
          a silent absence and a clean run must not look identical.
        • §6A-1b structure-answer questions routed to PROSE, each with its recorded
          justification (Q-numbers; an empty list stated as empty).
      A distribution that is 100% PROSE on a diagram-heavy paper, or one that emits a
      figure for nearly every question, is the signal this line exists to surface: both
      mean the §6A-1 two-part test is not being applied. Report the counts; do not
      editorialise.
      TRANSFER SAFETY (v1.36.0 — the §7-7 distribution): AXIOM epistemic-type counts ·
        claims NARROWED / MOVED_TO_DEDUCTION · SPEED HACKs OMITTED on §14-1 part 3 ·
        kept absolutes (count of declared sentences) · neighbours drawn from the
        curated library vs session-generated (counts; a library-absent run says so).
      ALIGNMENT (§6A-1c): questions re-routed by the §6A-3b tripwire (Q-numbers;
        an empty list stated as empty).
  §R4 SELF-AUDIT (§18): verify_fidelity / verify_structure / math-render / count
      invariants / strip-re-audit / coverage assertion — all clean (real engine STDOUT,
      content-free).
  §R5 DERIVATION-CONFIDENCE: every Q where methods disagreed initially or a figural
      reading diverged from the manifest, with the resolution (Q-numbers + reason class).
  §R6 FACT SOURCES: every web-verified fact with source URL + verification date
      (author-facing; never echoed to chat).
  §R7 DEFECTS (§17-4, v1.37.0): every Q proven defective, with the reproduced evidence
      and the ONE regeneration line the operator runs — the paper still SHIPS for
      every other question; §R2 reads SHIP WITH DEFECTS [Q-numbers].
  §R8 AUTHOR HANDOFF (RE-20): what was derived, what was web-verified, what is model-
      derived, where to look hardest — the record a human reviewer needs, since no gate
      reads it (§18-2). State: review the docx IN MICROSOFT WORD (§11-3).
  §R9 LIMITATIONS (§22).
  §R10 KEY RECONCILIATION (§7-8): commitments available y/n · key_status counts ·
      Q-numbers for every non-MATCH with the §17-3 step that resolved it · for every
      RESOLVED_SOURCE: Q-number, the proving step, the web-source reference, and ONE fixed
      sentence: "Step 7's committed key for this question was proven wrong — consider an
      EX-rule in [ExamCode]_EXPLAIN_LEARNINGS_v*.md (§24)". Never the answer value.
  §R11 ERROR PROVENANCE (§15-2): lines by mode (VERIFIED_ERROR_PATH · DIRECT_
      CONTRADICTION) · hedge-ban hits at construction · pitfalls per NAT Q.
  §R12 SEMANTIC OBJECTS (§13-2b): registered · agreed first / after re-transcription ·
      LOW confidence · §7-7 tripwire fired y/n and second-pass outcome.

# ════════════════════════════════════════════════════════════════════════
## §21 — DEFINITION OF DONE / HARD INVARIANTS (ANY violation = do NOT deliver)
# ════════════════════════════════════════════════════════════════════════
  0.  (v1.30.0) NO EXACT SELF-TEST OR VERSION COUNT IS EVER WRITTEN INTO PRESCRIPTIVE
      TEXT IN THIS SPEC — not in a gate, not in a dashboard template, not in a report
      field, not in a checklist. Every such reference is EITHER floor form
      ("N/N PASS with N >= 62")
      where it gates, OR read from what actually ran where it reports. RATIONALE: an
      exact count is correct only until the next fixture is added, and this shape has
      now been fixed three times one instance at a time — GAP-2026-08-13-STALE-SELFTEST-
      PIN (the P1 gate, v1.25.0), v1.29.0 (the §R1 report line), and v1.30.0 (§21, the
      dashboard, an explanatory aside). Fixing the instance and leaving the class is
      what let it recur. Engine INTEGRITY is proved by bootstrap.py's sha256, never by
      a count; a count only ever proves how many fixtures exist today.
      SCOPE — PRESCRIPTIVE TEXT ONLY. This governs text that INSTRUCTS: gates,
      dashboard and report templates, checklists, definition-of-done items. It does
      NOT govern the HISTORICAL RECORD. A changelog entry, or an explanatory note
      describing a defect that was fixed, MUST be able to quote the stale value it is
      about — "this line carried 62/62 while the engine printed 78/78" is the evidence
      that makes the fix reviewable, and stripping it would leave a rule with no
      account of why it exists. The test is not whether a number appears; it is
      whether the number TELLS A SESSION WHAT TO DO. If it does, it is floor form or
      read-what-ran. If it merely records what once was, it stays.
  1.  Pre-flight P0–P9 passed; engine --self-test printed "N/N PASS" with N == total
      and N >= 62 (floor form, §21-0); N in mocks_completed; config built.
  2.  Every question explained (zero sampling); every ExplanationBlock.validate() clean.
  2b. (v1.29.0) Every figural question carries a decided FAMILY (§13-1); every question
      carries a §6A representation verdict; §R1 reports the spec version and engine
      self-test line AS READ, pinning neither.
  3.  Every answer independently derived two ways; disagreements resolved 2-of-3 +
      DERIVATION-CONFIDENCE; zero guesses. Each block typed correctly (mcq/msq/nat) and
      the answer bound accordingly (one option / the full set / the value+range).
  3b. (v1.35.0) Decisive intermediate claims mutually consistent on every question
      (§7-6); every counting answer derived inventory-first, closed-form only after
      verified independence (§7-0c).
  3c. (v1.36.0) Every AXIOM and every SPEED HACK transfer-tested and recorded (§7-7);
      a claim that fails its neighbour test never ships unrepaired; every kept
      absolute declared (§8-0b); every representation aligned to the deciding
      relation (§6A-1c); zero learner-psychology narration (§15-3).
  4.  Every figural question's images extracted, role-bound, VIEWED; answer from the
      images, not the manifest (no FIGURE section is rendered — v1.13).
  5.  Every CA/factual option web-verified with a recorded source.
  6.  WHY WRONG (mcq/msq): keys == exactly the non-selected options, each carrying a
      §9 diagnosis (recorded internally, rendered in natural language — never the raw
      token, v1.35.0) that REPRODUCES its option; COMMON PITFALLS (nat): ≥1 wrong value, each with the
      slip that yields it; no two share wording; no template/glyph/fake-cite; the wrong
      container matches the type (no why_wrong on nat, no common_pitfalls on mcq/msq).
  7.  SPEED HACK present IFF a genuinely faster route exists; never padded.
  7b. (v1.35.0) SPEED HACK eligibility recorded per question; any all-hack batch
      re-audited per §14-5 before delivery.
  8.  Every fraction OMML; explanation OMML well-formed; no year-range artefact.
  9.  FIDELITY: whole question region byte-identical to the Step-7 source (text, OMML,
      drawings, media MD5, tables); strip-re-audit passes; count invariants hold.
  10. Delivery: each batch shipped the COMPLETE paper (explained-so-far + untouched
      remainder); never a fragment; never the secure paper overwritten.
  11. Batched ≤ ceiling, one batch/response, HALT-for-confirmation each batch (interactive;
      autonomous waives the pause only); no look-ahead; the coverage assertion (§18) passed
      each batch; final batch also stopped before the report (MANDATE B).
  12. registry.json NOT re-synced (frozen); no internal sidecar leaked to outputs.
  13. present_files called exactly once per batch, only after §18 clean (MANDATE D).
  14. Report (§20) built from real STDOUT + findings; MANDATE-0 safe; author handoff printed.
  15. No question/answer/solution content ever printed in chat (MANDATE 0).
  16. (v1.37.0) Any conflict RESOLVED IN-RUN per §17-3 with its steps recorded; the paper
      never halted; content never edited; a proven defect reported per §17-4 with its
      regeneration line; no published key that failed §17-3; no key_corrections.json or
      any other plaintext-key artefact written (v1.40.0).
  17. (v1.37.0) key_status recorded per Q (§7-8); every figural transcription persisted
      and compared (§13-2b); error_provenance engine-validated (§15-2); curated families
      cited (§7-7); typography engine-applied (§8-0c).
  18. Learnings loaded at P1 (EXPLAIN_AUDIT_LEARNINGS + EXPLAIN_LEARNINGS, if present) and
      every question's applicable AL/EX rules routed and obeyed (§24); on mock 1 their
      absence is recorded, not an error.
  19. No preference reduced coverage or waived §18 / the coverage assertion (RE-0); any
      autonomous run waived the inter-batch PAUSE only, never the per-question review.

# ════════════════════════════════════════════════════════════════════════
## §22 — KNOWN LIMITATIONS & SCOPE (disclose in §R9 of every report)
# ════════════════════════════════════════════════════════════════════════
  • SCOPE: Step 9 explains OBJECTIVE papers — MCQ (single correct), MSQ (multiple
    correct), and NAT (typed numerical answer, no options), in any language/script and
    any option-label scheme, with uniform OR per-section option counts. PURELY
    DESCRIPTIVE / essay papers (e.g. UPSC Mains) are OUT OF SCOPE by nature: they have no
    options and no single keyed answer, so the block model (CA, WHY WRONG / COMMON
    PITFALLS) does not apply. A paper that mixes objective and descriptive questions is
    explained for its objective questions only; descriptive items are flagged, not faked.
  • The engine self-parameterises from the source files. If section_rules omits a needed
    value (label scheme, sentence terminators, per-section counts, a question's type), the
    structural default is used (numeric labels, Latin terminators, the uniform count, mcq)
    and logged — never silently wrong, but only as good as the config supplied.
  • The metacommentary/template guards are English-text patterns; for another-language
    explanation they will not catch language-specific metacommentary (the one-sentence,
    glyph, LaTeX, fraction, and structural guards remain language-independent). Negative-
    stem / composite trigger lists are config-supplied (§10) so those protocols stay
    language-correct.
  • No external key existed — correctness rests on first-principles derivation + a second
    independent method (+ web-verification for facts). v1.21.0: nothing re-derives them
    afterwards — this is the only derivation the answer will receive.
  • Difficulty/section labels are model-estimated; not independently provable here.
  • Figural answers rest on reviewer reasoning over the VIEWED images (no machine proof) —
    but viewing is mandatory and un-sampled.
  • Web-verified facts are correct as of the verification timestamp; later real-world
    changes are outside Step 9's window.
  • "Genuinely faster" (SPEED HACK) and "the named error reproduces the option / value"
    (WHY WRONG / COMMON PITFALLS) are writer-discipline judgements with no second reader
    (v1.21.0); the engine proves shape, not pedagogy.

# ════════════════════════════════════════════════════════════════════════
## §23 — SUBTOPIC_ID CONTRACT (consumer role — v2.4 cross-step authority)
# ════════════════════════════════════════════════════════════════════════
#   Step 9 is a pure CONSUMER of the subtopic_id contract (the PYQ-phase steps mint; Step 5 enforces;
#   Step 7 joins and is the last writer). Step 9 reads subtopic_manifest.json only to support
#   CLASS detection (§6) and to label the per-class coverage rollup (§20 §R3) — mapping a
#   question to its subtopic_id by matching rendered content to section_rules patterns
#   keyed by id, NEVER by display-name string-match. Step 9 NEVER mints an id, NEVER joins
#   on a display name, and NEVER edits the manifest. The id recipe carries zero exam-
#   specific values (PYQ-phase §15).

# ════════════════════════════════════════════════════════════════════════
## §24 — LEARNINGS CONSUMPTION CONTRACT (consumer-only since v1.21.0)
# ════════════════════════════════════════════════════════════════════════
#   v1.21.0 — NO AUTOMATIC PRODUCER (Step 10 retired): this section is the CONSUMER
#   half only. Accumulated AL-rule files stay valid, loaded and obeyed; new rules are
#   added BY HAND. Schema below frozen so existing files keep parsing. (Retirement
#   narrative: SPEC_HISTORY.md, this spec's section — EC-P42.)
#
#   TWO learnings files, both loaded at P1, both exam-agnostic, both OVERRIDE this spec:
#     • [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md — AL-rules ("Audit Learning"). Formerly
#       auto-generated by Step 10; now legacy + manually authored.
#     • [ExamCode]_EXPLAIN_LEARNINGS_v*.md — EX-rules, human-authored guardrails (the
#       hard-won manual fixes). Same mechanism, same precedence.
#     • [Subject]_EXPLAIN_LEARNINGS_v*.md (v1.36.0) — SUBJECT-LEVEL guardrails, same
#       schema, same parser, one file copied unchanged into every exam project of that
#       subject (e.g. CHEMISTRY_EXPLAIN_LEARNINGS_v1.md). It carries the §7-7 curated
#       neighbour library, the exam-convention classes and the §8-3 minimum-concept
#       components: subject knowledge fixed once per subject, never once per exam.
#       Subject code from section_rules CATEGORY C `subject_code` (fallback
#       blueprint.subject), upper-cased. Absent file → nothing loaded, nothing
#       lost. Precedence: exam file > subject file > this spec.
#   Neither exists on mock 1 by design (nothing has been reviewed yet). Their ABSENCE is
#   normal and never a HALT; their PRESENCE is loaded and obeyed.
#
# ── S24-1 — WHAT A RULE CARRIES (frozen schema; no automatic producer — v1.21.0) ─────
#   Each rule is a markdown block headed `## AL-<id> — TITLE` (or `## EX-<id> — TITLE`)
#   with these fields (parse_learnings extracts them verbatim):
```text
  Defect code    : the universal-taxonomy code the rule addresses (e.g. FAKE-SPEED-HACK,
                   WHY-NOT-WHAT, AXIOM-RESTATE). THIS is the routing key — never a section.
  First seen     : Mock N, Q# (provenance)
  Occurrences    : "k of m" in the mock that promoted it (why it earned a rule)
  Pattern        : what went wrong and why it recurs
  Prevention rule: exactly what to do differently while authoring (the obeyable part)
  Verification   : the one-line self-check to confirm the rule was honored
```
#   parse_learnings(path) (explain_engine.py) returns {'rules':[...], 'by_defect':
#   {defect_code:[rule_code,...]}} — rules indexed by defect_code, NEVER by exam section
#   (the human file may GROUP rules under section headings for readability; the machine
#   index ignores those and keys off defect_code, so the loop is exam-agnostic).
#
# ── S24-2 — HOW A RULE IS APPLIED (per question, at solve time) ──────────────────────
#   1. Resolve the question's CLASS(es) (§6). Each class can exhibit a known set of
#      defect codes (the §15 / error-taxonomy mapping shared across Steps 8/9/10).
#   2. The APPLICABLE rules for the question are the loaded AL/EX rules whose defect_code
#      is in that class's defect set (via by_defect). Obey each one's Prevention rule
#      while authoring the block, and run its Verification before validate().
#   3. A rule promoted with HIGH occurrence (the >= 2-occurrence threshold, S24-4) for a
#      class PRESENT in this mock becomes an explicit per-question checklist item (§5
#      S5-3) — it is not merely advisory, it is ticked.
#   4. The §18 self-audit asserts, whole-paper, that every question's applicable rules
#      were routed and none for a present class was silently skipped (S18-1).
#   This does NOT duplicate §15: §15 is the always-on content contract (a named error must
#   reproduce its option); §24 ROUTES the accumulated, exam-tested specifics of HOW that
#   contract failed before to the exact questions at risk, so a known slip is not re-made.
#
# ── S24-3 — PRECEDENCE & ACCUMULATION ───────────────────────────────────────────────
#   • A loaded learnings rule OVERRIDES this base spec on any CONTENT conflict (it carries
#     a realised, exam-tested fix this spec was written before). It may NEVER override the
#     coverage/exhaustiveness rules or the §18 gate (RE-0) — a learnings rule tightens
#     quality, it never licenses skipping work.
#   • Rules ACCUMULATE across mocks — never delete a rule. A rule is retired only by an
#     explicit `Supersedes: AL-<id>` annotation on a newer rule (parse_learnings marks the
#     superseded flag); silent removal is forbidden (it would reopen a closed defect).
#   • On conflict BETWEEN two loaded rules, the one bearing the explicit Supersedes wins;
#     absent that, the more specific (narrower defect_code / class) wins; surface, never
#     guess.
#
# ── S24-4 — THE PRODUCER CONTRACT (RETIRED — kept for files already written) ──────────
#   HISTORICAL (through v1.20.1): Step 10, at the end of a mock's audit, updated
#   [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v1.md:
#   for EVERY defect code it fixed >= 2 times in that mock (the promotion threshold), it
#   writes or updates an AL-rule in the schema above, appends the mock to the file's
#   coverage line, and re-uploads the file (accumulate, never overwrite history). A single
#   occurrence is logged in the audit defect log but does not yet earn a standing rule —
#   the threshold keeps the learnings file signal, not noise. The filename version (_v1,
#   _v2, …) advances only on an incompatible schema change; the consumer loads the highest
#   version present. v1.21.0: no step performs this promotion any more. An author adding a
#   rule by hand SHOULD follow the same threshold and schema so the consumer keeps parsing
#   the file, but nothing enforces it.
#
# ── S24-1b — THE **Triggers:** FIELD (v1.37.0 — additive; the frozen schema still parses) ──
#   A rule MAY carry `**Triggers:** term, term, re:<regex>` — comma-separated phrases
#   (case-insensitive, whole-word) or raw regexes. parse_learnings reads it into
#   rules[].triggers; triggers_from_learnings compiles the table; the engine uses it
#   for §7-7 step 3. A rule without Triggers is loaded and obeyed exactly as before but
#   is NOT mechanically enforced — every NEIGHBOUR-LIBRARY rule SHOULD carry one.
#
# ── S24-6 — DEFECT CODES INTRODUCED BY v1.37.0 ─────────────────────────────────────────
#   KEY-CONFLICT · SEMANTIC-MISREAD · UNVERIFIED-PROVENANCE · HEDGED-PROVENANCE ·
#   LIBRARY-NOT-CITED · FORMULA-TYPOGRAPHY · MINIMUM-SPECIFICITY · FORMULA-OXIDATION-
#   STATE · SITE-SET-CONFLATION · CAUSAL-CONFLATION (definitions: subject library).
#
# ── S24-5 — DEFECT CODES INTRODUCED BY v1.36.0 (routing keys for new rules) ─────────────
#   §24 ROUTING KEYS for the transfer-safety family: OVERGENERALISED-AXIOM ·
#   UNSAFE-SPEED-HACK (§14-1 part 3) · UNJUSTIFIED-ABSOLUTE (§8-0b) ·
#   EXAM-CONVENTION-AS-LAW · CONCEPT-MINIMUM-MISSING (§8-3) ·
#   REPRESENTATION-MISALIGNED (§6A-1c) · LEARNER-PSYCHOLOGY (§15-3) ·
#   NEIGHBOUR-LIBRARY (a curated neighbour family: Pattern = the unsafe
#   generalisation, Prevention rule = the safe scope, Verification = the canonical
#   counterexamples — the §7-7 library in the frozen schema, no new parser).
#
# ════════════════════════════════════════════════════════════════════════
## APPENDIX A — UNIVERSAL EXAM-AGNOSTIC explain_engine.py (MANDATE A) — SINGLE SOURCE
# ════════════════════════════════════════════════════════════════════════
#   v1.12 — the ~1000-line engine listing is NO LONGER re-embedded here. The engine has
#   ONE canonical, runnable home:
#       explain_engine.py   (delivered alongside this spec; uploaded to each [ExamCode] project)
#   It is COMPLETE, working, universal, and byte-identical across exams — the same file
#   PYQExplain reads. It carries EngineConfig, ExplanationBlock,
#   add_math_text, parse_paper, build_interleaved_docx, verify_fidelity, verify_structure,
#   verify_explanations, strip_solutions, the reader parse_solution_blocks, and
#   parse_learnings. Self-tests: `python3 explain_engine.py --self-test` →
#   "SELF-TEST: N/N PASS", N >= 62 (core, required at P1) and `--self-test-audit` →
#   "AUDIT-SELF-TEST: N/N PASS", N >= 10 (reader round-trip; v1.25 floor form).
#
#   The framework linter (validate_framework_md.py) runs explain_engine.py's
#   `--self-test` directly. (v1.12 removal rationale — the embedded-copy desync
#   history: SPEC_HISTORY.md, this spec's section — EC-P42.)
#
#   COMPANION GATE (v1.21.1 — REMOVED): explain_audit_gate.py has been deleted from the
#   framework. Its sole remaining consumer, PYQExplainAudit (PYQ-2), was retired, so no
#   step runs a CA1–CA7 completion gate over any audit_progress.json ledger or Solutions
#   doc. Step 9's §18 self-audit is
#   the whole mechanical certification this document gets.

# ════════════════════════════════════════════════════════════════════════
## FOOTER — this file is the canonical Step-9 spec. On any CONTENT conflict with a loaded
# learnings file — [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md (legacy/manual, §24)
# or [ExamCode]_EXPLAIN_LEARNINGS_v*.md (human guardrails) — that learnings
# file WINS (it carries hard-won, exam-tested fixes); both are loaded at P1 via
# parse_learnings and applied per §24. A learnings rule NEVER overrides coverage/§18/the
# batch law (RE-0). Deliver the full merged spec on every edit — never a patch.
# END OF Framework_MockTestExplain v1.40.0
# ════════════════════════════════════════════════════════════════════════
