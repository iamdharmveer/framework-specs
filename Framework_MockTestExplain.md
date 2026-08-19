# Framework_MockTestExplain v1.27.0
# v1.27.0 — 2026-08-19 — GAP-2026-08-19-EXPLAIN-MATH-NOTATION + REPRESENTATION ROUTER.
#   MINOR bump: §11 grammar is DOCUMENTED and §9 gains scientific error types; no
#   existing artefact shape changes. TWO defects, one root cause.
#   D1 — §11 BANNED THE SYNTAX ITS OWN COMPILER REQUIRES. S11-1 listed "\\frac",
#   "\\sqrt" and "$…$" as banned LaTeX while t3_compile handles \\frac{}{},
#   \\sqrt{}, K_{sp}, E_{cell}^{0} and \\Delta_{o} CORRECTLY, and S18 recorded the
#   consequence in its own words: "bans LaTeX in prose (§11), so ⟦MATH:⟧ regions
#   are rare here". An executing session therefore read §11, concluded that math
#   notation was forbidden, and VERBALISED arithmetic instead — measured on a
#   60-question chemistry paper: 105 verbalised phrases ("divided by" x18,
#   "square root of" x9, "raised to the power" x3) against 6 OMML nodes in the
#   whole document, every one of them in the two pure-mathematics questions and
#   NONE in any science question. The prose-only texture was the spec working as
#   written, not a generation failure. S11-1 now documents the grammar that
#   actually compiles and confines the LaTeX ban to PROSE, where it belongs.
#   D2 — THE COMPILER VALIDATES GRAMMAR, NEVER NOTATION. guard_sentence exempts
#   ⟦MATH:⟧ bodies from every prose guard on the stated grounds that the compiler
#   checks them. It does not: a bare _ / ^ binds exactly ONE preceding character
#   and unknown words pass through as literal text, so Delta_o rendered "Delt aₒ",
#   K_sp rendered "Kₛp" and sqrt(x) rendered as flat text — SILENTLY, with every
#   gate green. explain_engine v2.2 adds t3_notation_guard (authoring-time, fail-
#   at-construction, remedy named in the message) and the self-test locks it in
#   BOTH directions. t3_mathcomp.py is deliberately NOT touched — it is byte-
#   locked to Framework_PYQPrepare §S3-5b by the self-test drift lock.
#   D3 — REPRESENTATION SELECTION WAS NOT A PIPELINE STAGE. §6 classed questions
#   by exam-shape (vocab/grammar/formal-logic) with no class for structural or
#   derivational reasoning, and ExplanationBlock has no field able to carry a
#   figure, so a structural explanation could only DESCRIBE what a scheme would
#   show. New §6A REPRESENTATION ROUTER makes the choice explicit and — critically
#   — makes PROSE the default that visuals must EARN, on the proven §14 SPEED HACK
#   "omit, never fake" pattern. Emission is staged for the engine work; the router
#   verdict is recorded and reported from this version.
# v1.26.0 — 2026-08-16 — GAP-2026-08-16-STEP5-SYNTHESIS-UNRUNNABLE (D3), CLASS SWEEP.
#   MINOR bump: a name is added to this file's executable surface. NO ARTEFACT CHANGES.
#   This spec CALLED present_files() from compiling python while DEFINING it nowhere —
#   a guaranteed NameError the moment that path executes as python. Five such call
#   sites stood across four specs; spec_name_audit_baseline.json had accepted
#   `present_files` as a known-unbound name in all four, which is why the ratchet
#   reported OK for weeks. SAME SHAPE as D2 of
#   GAP-2026-08-15-PYQEXTRACT-DRIVE-ACQUISITION, which fixed the instance and left the
#   class standing. FIX: a CLASS: T stub is declared in this file, matching the
#   corpus's per-file house pattern for CLASS T markers.
# v1.25.0 — 2026-08-13 — SYNC AUDIT ROUND 2 (fresh-lens re-audit of Steps 5→11)
#   1. GAP-2026-08-13-STALE-SELFTEST-PIN (HALT-class). P1 pinned the engine gate at the
#      literal "SELF-TEST: 62/62 PASS" (3 sites; + "10/10" for --self-test-audit, 2 sites)
#      while explain_engine.py actually prints 64/64 (26/26 audit) — so EVERY Explain
#      session following P1 literally HALTed on a healthy engine. All 5 sites converted to
#      the FLOOR form ("N/N PASS with N >= 62 / >= 10"), the same AUTH_GATE_FLOOR pattern
#      Steps 6/7 already use — integrity is bootstrap.py's sha256 job, not a count pin's.
#   2. GAP-2026-08-13-P10-SCOPED-BLUEPRINT (behavioral). P10 loaded the hardcoded
#      f'{EXAM}_blueprint.json' (the MOCK blueprint) though P1 selects among ALL
#      {EXAM}*_blueprint.json by the uploaded docx's slug — so for a SCOPED paper the
#      v1.24 P10/0 gate compared the scoped docx against the mock blueprint (unconditional
#      false HARD STOP), or crashed if no mock blueprint existed: the gate could never
#      pass for the resumed-scoped papers it was written about. P10 now selects the
#      blueprint containing the paper whose slug matches PAPER_SLUG (P1's own semantics,
#      restated self-contained), and every downstream P10 check (FK, count, difficulty)
#      now validates against the CORRECT blueprint for scoped papers too.
# ════════════════════════════════════════════════════════════════════════
#
# VERSION HISTORY:
# ════════════════════════════════════════════════════════════════════════
# PURPOSE
# ════════════════════════════════════════════════════════════════════════
#   Take the .docx produced by Step 7 and the frozen registry.json,
#   INDEPENDENTLY DERIVE the answer to every Question, and INTERLEAVE a perfect,
#   highest-standard explanation after each question — without altering one byte of
#   the paper. Emit [ExamCode]_Mock[N]_Explanation.docx: a 100%-explained, zero-defect
#   learner-facing solution document, plus an author handoff report.
#
# ════════════════════════════════════════════════════════════════════════
# PIPELINE POSITION
# ════════════════════════════════════════════════════════════════════════
#   Step 5 (PYQExtract)   → [ExamCode]_section_rules.md + _subtopic_manifest.json
#   Step 6 (MockBlueprint) → [ExamCode]_blueprint.json + _registry.json (template)
#   Step 7 (MockCreate)    → [ExamCode]_Mock[N]_Create.docx
#                                  [ExamCode]_registry.json (written at Final Assembly —
#                                  FROZEN for every step after Step 7)
#   THIS STEP — Step 9 (MockExplain) → [ExamCode]_Mock[N]_Explanation.docx (interleaved explanations)
#   C3 (v1.15): in every [ExamCode]_Mock[N]_*.docx name above, "Mock[N]" is the paper_slug of the
#   paper being processed — "Mock[N]" for a mock (byte-identical), else the scoped paper_id with
#   ":"→"_" (e.g. SUBJ_Physics_03), derived from blueprint.mocks[N].paper_id (fallback MOCK:M{N:02d}).
#   Read the input under, and write the output under, that same paper_slug. No registry writes here.
#   Step 11 (MockDeliver)
#
#   Steps 5–11 all run in the [ExamCode] project (exam-specific). Step 9 runs directly
#   after Step 7 and directly before Step 11. There is no audit step on either side:
#   nothing re-derives these answers after this step, so §12 and §19 are terminal.
#
# ════════════════════════════════════════════════════════════════════════
# EXAM-AGNOSTIC GUARANTEE
# ════════════════════════════════════════════════════════════════════════
#   This spec contains ZERO hardcoded exam values. It names no section, no subtopic,
#   no question count, no time/marks figure, no option count, no section family, no
#   language, no figural type, no block label. Every such value is READ at runtime:
#     • question/section counts, q_ranges, options-count, difficulty schedule
#       → blueprint.json
#     • per-subtopic patterns, wrong_option_structure, fixed option sets, OMML_required,
#       option label format, language, block labels/markers, figural object/transformation
#       types, escape tokens, passage word ranges
#       → section_rules.md (CATEGORY C header + CATEGORY A/B blocks)
#     • subtopic_id join key, mandatory-every-mock list, alternation groups
#       → subtopic_manifest.json
#     • per-mock figural_manifests[] + rc_manifests[] (cross-checks only, never keys)
#       → registry.json
#   SCOPE — what "exam-independent" means here, stated precisely (no over-claim):
#   Step 9 explains OBJECTIVE papers and supports, per question, all three objective
#   answer formats found across these exams:
#     • MCQ — single correct option (the common case; e.g. SSC, IBPS, NEET, CLAT).
#     • MSQ — multiple correct options, scored as a set (e.g. GATE multi-select).
#     • NAT — numerical-answer-type with NO options, optionally with a tolerance
#       range (e.g. GATE / JEE numerical-input questions).
#   It also handles, from config (never hardcoded): per-SECTION option counts (a paper
#   that is 4-option in one section and 5-option in another), alphabetic / roman /
#   custom option labels (A·B·C·D, i·ii·iii, …) as well as numeric, and language-
#   specific sentence terminators (e.g. the Devanagari danda '।'). With valid
#   upstream outputs (Steps 5–7) it therefore covers SSC CGL, GATE (incl. NAT/MSQ), NEET, IBPS,
#   UPSC CSAT, CAT and regional/other-language exams. OUT OF SCOPE by nature: purely
#   DESCRIPTIVE / essay papers (e.g. UPSC Mains), which have no options and no single
#   keyed answer — the objective block model does not apply (see §22). If a value an
#   explanation needs is absent from the source files, the engine falls back to a
#   STRUCTURAL default (English labels, numeric scheme, Latin terminators, the uniform
#   option count) and logs it — it is NEVER hardcoded as an exam fact.
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_MockTestExplain.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

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
                                            wiring; see P3)

  ALREADY IN PROJECT KNOWLEDGE (from the PYQ-phase steps; required):
    3. [ExamCode]_section_rules.md        — per-subtopic rules + CATEGORY-C exam params
    4. [ExamCode]_blueprint.json          — sections[], q_range[], options-count, difficulty
    5. [ExamCode]_subtopic_manifest.json  — subtopic_id ↔ name + mandate/alternation data
    6. explain_engine.py                  — the universal explanation engine; SAME file
                                            in every exam project (MANDATORY — MANDATE A)

  NOT DELIVERED (Step 9 must do without these — by design):
    ✗ any answer key. Step 7 holds a key internally and never delivers it.
       Step 9 re-derives all answers independently (§7).
    ✗ internal Step-7 sidecars (answer_key.json, concept_map, audit ledger).
       The figural/RC maps Step 9 needs are in registry.json and re-extracted at P3.

## S0-2 — OUTPUTS (what Step 9 delivers)

  CORE DELIVERABLE (every batch, via ONE present_files call — the WHOLE paper):
    1. /mnt/user-data/outputs/[ExamCode]_Mock[N]_Explanation.docx
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
#   [ExamCode]_Mock[N]_Explanation.docx — is a FILE, not chat, and is the legitimate,
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
#   not bound, WHY-WRONG key mismatch, fidelity breach). If the file is absent from
#   BOTH the framework clone (/tmp/fw) and the project Files (/mnt/project):
#     HARD STOP. Print:
#       "HARD STOP (MANDATE A): explain_engine.py not found in the framework clone
#        (/tmp/fw) or the [ExamCode] project Files (/mnt/project). Step 9 cannot build
#        explanations without it. It ships with the framework repo (GitHub projects get
#        it from the clone) — reload the framework (Step 0); or for a direct-upload
#        project obtain it from Appendix A (the canonical runnable copy) and upload it,
#        then re-run."
#   Appendix A points to the COMPLETE, working, exam-agnostic engine. Because it is
#   UNIVERSAL and byte-identical for every exam, the file keeps the plain neutral name
#   explain_engine.py in every project (NOT exam-prefixed — there is no per-exam
#   variant to disambiguate, and a prefix would falsely imply exam-specificity). It
#   ships with the framework repo, so a GitHub project finds it in the /tmp/fw clone
#   (no upload needed); a direct-upload project uploads it once to /mnt/project and
#   reuses the SAME file in every exam project. It self-tests with `--self-test`
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
  RE-13 : WHY WRONG DIAGNOSES, NEVER DISMISSES. Each wrong option names an error type
          that ACTUALLY produces that option's value/content; no template, ever (§15).
  RE-13b: REPRESENTATION IS ROUTED, NOT ASSUMED (v1.27.0). Every question runs the
          §6A router after derivation and before writing. PROSE is the default and a
          visual must EARN its place on the §14 two-part test; the verdict is recorded
          per question and reported (§20). Quantitative steps render as ⟦MATH:⟧ math,
          never as verbalised arithmetic (§11 S11-1c).
  RE-14 : SPEED HACK ONLY WHEN GENUINELY FASTER. Emit iff a structurally-different route
          reaches the same CA with materially less work; otherwise OMIT — never pad (§14).
  RE-15 : NO TEMPLATES / GLYPHS / FAKE-CITES / METACOMMENTARY / BANNED BLOCKS. Engine-
          enforced at write time; the writer must not even attempt them.
  RE-16 : HALT-AND-ESCALATE, NEVER FIX. A genuine, reproduced defect HALTS the run and is
          escalated to the author for a Step 7 re-run of that question; Step 9 never edits
          question content and never publishes a guessed key (§17).
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
  RE-22 : LOAD & APPLY LEARNINGS. At P1, load the accumulated learnings —
          [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md (v1.21.0: legacy/manually-authored — its
          Step-10 producer no longer exists; still READ when present) and
          [ExamCode]_EXPLAIN_LEARNINGS_v*.md (human guardrails) — via parse_learnings, and
          OBEY every applicable rule while authoring (§24). Learnings OVERRIDE this spec on
          conflict (content only — never coverage/§18, RE-0); they accumulate across mocks
          (never deleted, superseded only by an explicit annotation). Absent on mock 1 by
          design — proceed without them.

# ════════════════════════════════════════════════════════════════════════
# §1 — PIPELINE POSITION & SOURCES OF TRUTH
# ════════════════════════════════════════════════════════════════════════

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
      explain_engine.py (from the framework clone /tmp/fw, else the project Files
      /mnt/project). Copy the engine to /home/claude and run
      `python3 explain_engine.py --self-test` → MUST print
      "SELF-TEST: N/N PASS" with N == total (all pass) AND N >= 62 before any
      solving (v1.25, GAP-2026-08-13-STALE-SELFTEST-PIN: the FLOOR form, the
      same AUTH_GATE_FLOOR pattern Steps 6/7 use for the audit copy — the
      previous exact "62/62" pin made every session HALT on a HEALTHY engine
      the moment it grew fixtures; it prints 64/64 today. bootstrap.py's
      sha256 verification is what proves engine integrity, not the count). THEN LOAD LEARNINGS (§24): via
      explain_engine.parse_learnings, parse the highest-version
      [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md (legacy/manual — v1.21.0) and
      [ExamCode]_EXPLAIN_LEARNINGS_v*.md (human guardrails) IF PRESENT, and index every
      AL/EX rule by defect_code. These OVERRIDE this spec on conflict (§24). When a
      learnings file is present, also run `--self-test-audit` (N/N PASS with N >= 10; currently 26/26) to
      confirm the cross-step readers. Absent on mock 1 by design — proceed. Any load/self-test
      failure → HALT.
  P2  STATUS DASHBOARD (print every turn, before any solving):
```text
      === MockExplain v1.20 — Session Status ===
      Spec / section_rules / blueprint / manifest / registry : [loaded]
      explain_engine.py --self-test                          : [62/62 PASS]
      Exam config (CATEGORY C)  : options=[k or per-section map] · labels=[scheme] ·
                                  q_re=[..] · opt_re=[..] · lang=[..] · terminators=[..]
      Level / Medium             : [level] · [medium]  (from exam_config via CATEGORY C)
      Marking ranges             : [N] range(s) · marks=[list] · neg=[list]  (from marking_scheme)
      Question types present     : [mcq C · msq M · nat T]  (per blueprint/section_rules)
      Answer key                 : NONE by design — Step 9 derives all [Q_TOTAL]
      Learnings loaded           : [k AL-rules · m EX-rules · v_j] OR [none — mock 1 by design]
      Paper (Mock N)             : [X bytes · Q_TOTAL questions · K images · T tables]
      Figural manifest / RC manifest : [found in registry] OR [absent — derive visually]
      Batch plan                 : [K batches · ceiling 10 · linked groups atomic]
      Mode                       : [interactive — halt per batch] OR [autonomous — no pause, §MANDATE B]
      Output                     : /mnt/user-data/outputs/[ExamCode]_Mock[N]_Explanation.docx
      State                      : /home/claude (chat-scoped)
      Status                     : [Ready — Batch 1] OR [Resume — Batch k] OR [Halted — reason]
```
  P3  VERIFY INPUT DOCX — build EngineConfig from CATEGORY C + blueprint, then run
      parse_paper(). EngineConfig carries: q_re, opt_re, the option count (uniform OR a
      per-question/per-section map via options_by_q, with 0 marking NAT questions), the
      option LABEL SCHEME (numeric/alpha/roman/custom), the language SENTENCE TERMINATORS
      (e.g. add the Devanagari danda), and labels/markers. Resolve each question's TYPE
      (mcq/msq/nat) from section_rules (answer_type=='numerical' → nat; answer_cardinality
      =='multi' → msq; else mcq). parse_paper checks: questions ascending + contiguous
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
      locks this). The registry map is the
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
  EXAM-CONNECTION blocks, zero year-range slashes. A breach raises in
  ExplanationBlock.validate() / add_math_text BEFORE the doc is written. As of
  2026.08.10.3, validate() also COMPILES any ⟦MATH:…⟧ Tier-3 region (t3_compile) and
  RAISES at construction on a grammar reject, so such a region can never degrade to
  raw text at render; this pipeline normally builds math with the explicit helpers
  (§11), so regions are rare here, but the gate applies to the shared engine.

## S5-3 — PER-QUESTION CHECKLIST (tick every item before constructing the block)

```text
  [ ] Full stem + ALL options read to the end; OMML merged with text in document order
  [ ] Question TYPE resolved: mcq (one option) · msq (a set) · nat (a value, no options)
  [ ] Negative phrasing scanned (config triggers; default NOT/EXCEPT/INCORRECT/FALSE) → §10a
  [ ] Composite options scanned (Both/Only/All of the above/None of the above)   → §10b
  [ ] Figural? → every image extracted, role-bound, and VIEWED before solving     (§13)
  [ ] Answer derived from first principles AND a second independent method        (§7)
  [ ] Methods agree (else DERIVATION-CONFIDENCE) and land on exactly the answer:
      one option (mcq) · the full correct set (msq) · the single value/range (nat) (§7)
  [ ] Factual content web-verified with a recorded source                         (RE-18)
  [ ] Class identified (§6); the right section LEADS; the rest compressed to one dense line
  [ ] AXIOM states a TRUTH, not the task; no restatement of the question
  [ ] DEDUCTION last step binds the answer: "Option L(ca)" (mcq) · every selected
      "Option L(i)" (msq) · the value string (nat); each step shows its value
  [ ] §6A representation router RUN; verdict recorded; PROSE unless the two-part
      test passed; any degrade disclosed                                          (§6A)
  [ ] every quantitative step rendered as ⟦MATH:⟧ math, NOT verbalised arithmetic (§11 S11-1c)
  [ ] every ⟦MATH:⟧ body uses braced scripts and backslash names (\Delta, \sqrt)  (§11 S11-1b)
  [ ] SPEED HACK present IFF a genuinely shorter route was found; else omitted     (§14)
  [ ] WHY WRONG covers exactly the non-selected options, each first sentence naming an
      error type (§9) that ACTUALLY produces it (mcq/msq); NAT uses COMMON PITFALLS —
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
  | C-FIGURAL        | answer is/depends on a figure (§13)          | AXIOM = the visual rule; DEDUCTION traces the VISIBLE transformation; WHY WRONG = the visual difference per wrong figure |
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
# §6A — REPRESENTATION ROUTER (v1.27.0 — exam-agnostic, domain-configured)
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

## S6A-2 — The requirement vocabulary (what the router emits)
  | Requirement          | Emit when the answer turns on …                        |
  |----------------------|--------------------------------------------------------|
  | PROSE                | a fact, a definition, or a short causal chain (DEFAULT) |
  | EQUATION             | a calculation — governing relation, substitution, value |
  | TABLE                | independent criteria tested across several candidates   |
  | STRUCTURE_GRAPH      | connectivity / stereochemistry / a transformation       |
  | LEVEL_DIAGRAM        | occupancy, energy ordering, or state splitting          |
  | DATA_PLOT            | the shape of a graph, spectrum, or titration curve      |
  EQUATION is satisfied by §11's ⟦MATH:⟧ regions and is ALWAYS available — it
  needs no renderer and no configuration. TABLE is native docx. The last three
  require a renderer declared in section_rules; absent one, the router degrades
  (§6A-4).

## S6A-3 — Record the verdict on every question
  The router's verdict is recorded per question in progress.json as
  representation_verdict, with the two-part test's outcome. This is what makes
  the choice auditable rather than implicit: a paper whose every question
  demanded a figure, or whose every question refused one, is visible as a
  pattern instead of discovered by reading. The §20 report states the
  distribution. NOTE (v1.27.0): the router RECORDS and REPORTS from this
  version; figure EMISSION lands with the ExplanationBlock representation field
  in the paired engine release. Recording first is deliberate — it lets the
  routing decisions be reviewed against real papers before any figure ships.

## S6A-4 — Degrade LOUDLY, never silently, and never HALT
  If a required renderer is unavailable, or a rendered artefact fails its
  validation gate (§6A-5), the router steps DOWN one requirement — toward
  EQUATION, then PROSE — and the explanation still ships. A missing renderer
  must never halt a paper mid-run. But the degrade is DISCLOSED: recorded in
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

# ════════════════════════════════════════════════════════════════════════
# §7 — ANSWER DERIVATION & VERIFICATION (no key delivered — derive it)
# ════════════════════════════════════════════════════════════════════════

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

  PINNED: this function body MUST stay byte-identical to Framework_MockTestCreate.md
  §S7-NEW-C and audit_canonical.py's A-NAT-GRADE implementation — never re-implemented
  independently (anti-drift by design). Three independent copies computing the SAME
  deterministic function on the SAME true inputs is the intended redundancy (matches Step
  8's own pinned-copy pattern); three DIFFERENT implementations would not be.

# ════════════════════════════════════════════════════════════════════════
# §8 — SECTION QUALITY STANDARDS (the highest-standard contract per section)
# ════════════════════════════════════════════════════════════════════════
#   Governing rule across ALL sections — the DENSITY FLOOR (not a length floor):
#   every line must add a NEW number, fact, or reason; NO sentence may restate another.
#   Brevity is allowed only when the line is dense; a line carrying none of its required
#   facts fails the content floor (v1.21.0: the no-restatement rule is enforced by the
#   writer alone — no audit step re-reads it).

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
  Enforced: ≥1 sentence, one-per-paragraph, banned-phrase scan (engine); "truth not task",
  "why not just what", correctness by discipline alone (v1.21.0).

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

## S8-4 — SPEED HACK
  Role: exam-craft — a genuinely shorter route to the SAME answer, for time pressure;
  optional by design. Standard: a structurally DIFFERENT, faster path (not the same
  steps reworded); same CA; one or two dense lines; names the actual lever ("test
  divisibility by 3 first", "back-solve from the options", "only 39 fits"). Vague
  encouragement ("do it mentally", "obvious with practice") is banned — that is a
  platitude, not a hack. Inclusion is decided per question by §14; if no honest shortcut
  exists the block is OMITTED, never padded. Enforced: if present, binds the same CA
  (engine); "genuinely faster, not cosmetic" by discipline alone (v1.21.0).

## S8-5 — WHY WRONG (mcq / msq) · COMMON PITFALLS (nat)
  Role: where most learning happens — the SPECIFIC error a student commits to land on a
  wrong choice, inoculating against that exact mistake. Standard (the anti-template
  contract, §15): keys = exactly the NON-selected options (for MSQ, every option not in
  the correct set; never a selected one, never skipping one); 1–2 DENSE lines each; the
  first line names an error type (§9) that ACTUALLY produces that option's value/content
  (back-derive the distractor — "if a student did X they get exactly this option"); the
  line also carries the corrected value ("13 × 3 = 39, not 36"). No two wrong options
  share an explanation. For negative stems the true options are "a TRUE statement,
  therefore NOT the answer" — never "incorrect" (§10a). For factual classes every reason
  is a web-confirmed fact.
  NAT analogue — COMMON PITFALLS: a NAT question has no options to reject, so this section
  lists the wrong VALUES a student most commonly computes, ≥1, each headed by the value
  and naming the slip that yields it ("forgetting to divide leaves 235 — process_confusion";
  "dividing by the wrong count gives 9.4 — value_swap"). Same anti-template discipline:
  each pitfall must reproduce a real wrong value, none generic. Enforced: key set (mcq/msq)
  or ≥1 value-keyed pitfall (nat) + ≥1 sentence + error-type token + banned
  templates/glyphs (engine); reproduces-the-wrong-answer + factual truth by discipline
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

# ════════════════════════════════════════════════════════════════════════
# §10 — SPECIAL-CASE PROTOCOLS
# ════════════════════════════════════════════════════════════════════════

## S10a — Negative stem (the deadliest content trap)
  Trigger: the stem contains a negation cue. The cue LIST is language-configurable (read
  from section_rules CATEGORY C; the English default is NOT / EXCEPT / INCORRECT / FALSE /
  "does not" / "cannot be"), so the protocol works for any-language papers (scanned BEFORE
  writing). CA = the option the stem asks to identify (usually the FALSE one). DEDUCTION
  gives one truth-verdict line for EVERY option, then isolates the target. Each WHY WRONG
  entry's first line states the option is a TRUE statement (hence NOT the answer) and
  names polarity_flip — NEVER calls a true statement "incorrect" (that teaches false
  information). This cannot be machine-proven; the §5-3 checklist tick is why this
  protocol exists.

## S10b — Composite options
  Trigger: options combine items ("Both 1 and 2", "Only 1 and 3", "All of the above",
  "None of the above"; trigger phrases configurable per CATEGORY C). Establish the truth
  value of EVERY underlying statement first (one DEDUCTION line each), THEN map the
  combination to the option. WHY WRONG for a composite names the exact component that
  breaks it ("Statement 2 is false, so the pair fails — partial_truth"), never a blanket
  rejection.

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
    the Step-7 input.
  • COUNT INVARIANTS: output question count, options/question, image count, table count
    and OMML count == the Step-7 input exactly. v1.21.0: nothing re-verifies these
    counts downstream — this per-batch check is the only one that runs.

# ════════════════════════════════════════════════════════════════════════
# §13 — FIGURAL DEEP-ANALYSIS PROTOCOL (view every image — no exception)
# ════════════════════════════════════════════════════════════════════════
#   No ExplanationBlock for a figural question may be built until every image in that
#   question has been extracted, role-bound, and VIEWED. Reasoning around the picture
#   from surrounding text alone is forbidden (RE-11).

## S13-1 — Detect figural questions structurally
  A question is figural if its region contains a <w:drawing> in the STEM or in any
  OPTION (read from the docx XML) — plus section_rules figural cues and registry
  figural_manifests[]. Two shapes, handled distinctly: IMAGE-IN-STEM (a diagram to
  reason about) and IMAGE-AS-OPTIONS (each option is itself a figure — series, analogy,
  odd-one-out, mirror/water image, paper folding, embedded figures, counting figures,
  cube net, space orientation).

## S13-2 — Extract, role-bind, view (the gate before solving)
  Extract the actual image bytes from the docx media parts, render them, and bind each
  to its exact role (which is the problem figure, which is option 1, option 2, …) using
  the 1:1 image↔label binding Step 7 built. VIEW each labelled image
  before deriving. The binding matters: an unbound view can derive the right shape but
  key the wrong index.

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

## S13-4 — Write what is visible; never anomaly-for-figural
  AXIOM = the visual rule (rotation / reflection / element add-remove / count /
  net-folding). DEDUCTION traces the VISIBLE transformation step by step to the chosen
  option, citing concrete features. WHY WRONG names, per wrong option-figure, the
  specific visual difference. (v1.13: no separate figure-description line is rendered —
  the figure itself sits in the question region above; the images are still VIEWED
  before solving, §13-2 / RE-11.) anomaly is NEVER used merely because options are
  images — a figural question always has a derivable answer once viewed.

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

## S14-4 — The honesty guard
  If you cannot state the SPECIFIC lever that saves SPECIFIC work, there is no SPEED HACK
  — omit it. An empty or generic SPEED HACK is a DEFECT, treated like a wrong
  answer. The pressure runs toward omission, never fabrication.

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
  1. NAME the error type (§9) in the first line — a diagnosis, not a dismissal.
  2. The named error must ACTUALLY produce that option/value (the reproduce check):
     back-derive the distractor — "if a student did X they get exactly this option/value."
     If no such mistake can be found, the question is not yet understood → go solve it; a
     generic line is forbidden. (Distractors are not random — Step 7 built each from a
     specific error path; for NAT, the common wrong values come from specific slips, so a
     real path always exists.)
  3. CARRY the corrected value — what the right step gives instead ("13 × 3 = 39, not 36";
     for NAT, "…, not 90"). The explicit contrast to the correct answer is mandatory, not
     optional.
  4. NO two wrong options/values share wording; NO banned template sentences (engine-scanned).

## S15-3 — Class- and type-specific shape (never generic across types)
  Computational → the arithmetic slip + the wrong number. Factual → what the option
  ACTUALLY is (the corrected fact). Negative stem → "TRUE, therefore not the answer"
  (never "incorrect"). Composite → the exact component that breaks it. Vocab → the
  precise nuance missed. RC → the passage line that REFUTES the option.
  MSQ → lead with the SEDUCTIVE HALF (the cheap test the distractor passes, which makes a
  hasty solver select it), then the test it fails — so the line teaches the trap, not just
  the verdict; two distractors that fail "the same way" must still differ in WHICH half
  seduces ("passes the 3 test, fails the 2 test" vs "passes the 2 test, fails the 3 test").
  NAT (COMMON PITFALLS) → head each entry with the wrong VALUE a student computes, name the
  slip that yields exactly it, and carry the contrast to the correct value.
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
  • STEP 10 IS THE INDEPENDENT NET: it re-reads EVERY explanation, zero sampling, not
    trusting Step 9 — and runs batched too, so it cannot get lazy at Q60 either; v1.12,
    it certifies with a runnable completion gate (CA1–CA7) so its own exhaustiveness is a
    command result, not a self-report.
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

## S17-3 — Step 9 does NOT fix, and almost never declares
  Per RE-16, Step 9 NEVER edits question content (that is Step 7's job) and NEVER
  publishes a guessed key. The two outcomes:
  • COMMON (still the usual case): what looked wrong was an incomplete solve → solve it
    properly and write the explanation. No defect.
  • RARE: after §17-1/§17-2, there is provably no single defensible answer → set the
    INTERNAL anomaly flag (never rendered, §5-1), HALT the run, and ESCALATE TO THE AUTHOR
    with the reproduced evidence, naming the question and the derivation. The author
    re-runs Step 7 for that question. Step 9 never overrides unilaterally.

## S17-4 — Why this cannot become lazy defect-calling
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
  [ ] verify_fidelity(out, Step8_source): whole question region byte-identical, every
      image rId resolves to a relationship (no dangling embed) (§12)
  [ ] verify_structure(out, blocks, expected = Q1..last(batch k)): coverage exact,
      NO look-ahead, header order + CA binding intact (§4 / §5)
  [ ] verify_explanations(out, blocks) -> (ok, problems): INDEPENDENT post-render re-audit
      of the rendered docx — re-reads the written bytes (not the in-memory blocks) and
      re-checks header order, the type-aware CA binding read back from the document,
      WHY-WRONG / COMMON-PITFALLS coverage, zero banned glyphs / metacommentary / templates
      / inline or vulgar fractions in rendered prose, one sentence per rendered paragraph,
      every OMML fraction well-formed with no year-range artefact, AND the Tier-3 degrade
      ledger (§13). BLOCKING CONTRACT — the verifiers RETURN status, they do NOT raise:
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
  [ ] §6A router verdict present for EVERY question in this batch; every degrade
      disclosed in the report; zero verbalised-arithmetic steps in a quantitative
      DEDUCTION (§11 S11-1c). A missing verdict is a BLOCKING FAIL — an unrouted
      question silently reverts to the pre-v1.27.0 prose-only default, which is the
      defect this router exists to remove.
  [ ] count invariants: image / table / OMML / question / option counts == Step-7 input
  [ ] strip-and-re-audit: questions-only copy passes the Step-7 auditor identically (§12-3)
  [ ] every CA fact web-verified with a recorded source (§7 / RE-18)
  [ ] derived answers flushed to answer_keys.json; CA three-way binding holds
  [ ] coverage assertion (S4-5 guard 3): the whole doc carries explanations for EXACTLY
      Q1..last(batch k) — no fewer, no more; a collapsed or look-ahead run fails HERE
      (this is the producer-side mechanical scope check; RE-0 forbids waiving it)
  [ ] learnings coverage (§24): every question's applicable AL/EX rules were routed; no
      loaded rule for a present class was silently skipped
```
  Any item open → fix, re-build, re-audit. present_files is FORBIDDEN until ALL hold.
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
leaked = [f for f in present if any(b in f.lower() for b in BANNED)]
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
# §20 — END-OF-MOCK REPORT (after the FINAL batch's confirmation; MANDATE-0 safe)
# ════════════════════════════════════════════════════════════════════════
  §R1 PROVENANCE: mock N · registry state · blueprint reference · spec v1.13 · engine
      62/62 · timestamp · EngineConfig (option count(s), label scheme, language,
      terminators) actually used.
  §R2 VERDICT: SHIP (delivered) / HALTED (escalation) — first line, unambiguous.
  §R3 COVERAGE: Q_TOTAL/Q_TOTAL explained · question-type split (mcq/msq/nat counts) ·
      SPEED HACK count (Q-numbers) · OMML object count in explanations · per-class
      derived-answer distribution (counts only).
  §R4 SELF-AUDIT (§18): verify_fidelity / verify_structure / math-render / count
      invariants / strip-re-audit / coverage assertion — all clean (real engine STDOUT,
      content-free).
  §R5 DERIVATION-CONFIDENCE: every Q where methods disagreed initially or a figural
      reading diverged from the manifest, with the resolution (Q-numbers + reason class).
  §R6 FACT SOURCES: every web-verified fact with source URL + verification date
      (author-facing; never echoed to chat).
  §R7 ESCALATIONS (§17): every Q where no single defensible answer was found, with the
      reproduced evidence — these block SHIP and bounce to the author for a Step 7 re-run.
  §R8 AUTHOR HANDOFF (RE-20): what was derived, what was web-verified, what is model-
      derived, where to look hardest — the record a human reviewer needs, since no gate
      reads it (§18-2). State: review the docx IN MICROSOFT WORD (§11-3).
  §R9 LIMITATIONS (§22).

# ════════════════════════════════════════════════════════════════════════
# §21 — DEFINITION OF DONE / HARD INVARIANTS (ANY violation = do NOT deliver)
# ════════════════════════════════════════════════════════════════════════
  1.  Pre-flight P0–P9 passed; engine --self-test 62/62; N in mocks_completed; config built.
  2.  Every question explained (zero sampling); every ExplanationBlock.validate() clean.
  3.  Every answer independently derived two ways; disagreements resolved 2-of-3 +
      DERIVATION-CONFIDENCE; zero guesses. Each block typed correctly (mcq/msq/nat) and
      the answer bound accordingly (one option / the full set / the value+range).
  4.  Every figural question's images extracted, role-bound, VIEWED; answer from the
      images, not the manifest (no FIGURE section is rendered — v1.13).
  5.  Every CA/factual option web-verified with a recorded source.
  6.  WHY WRONG (mcq/msq): keys == exactly the non-selected options, each naming an error
      type that REPRODUCES its option; COMMON PITFALLS (nat): ≥1 wrong value, each with the
      slip that yields it; no two share wording; no template/glyph/fake-cite; the wrong
      container matches the type (no why_wrong on nat, no common_pitfalls on mcq/msq).
  7.  SPEED HACK present IFF a genuinely faster route exists; never padded.
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
  16. Any genuine, reproduced defect HALTED-and-ESCALATED to the author; content never edited.
  17. Learnings loaded at P1 (EXPLAIN_AUDIT_LEARNINGS + EXPLAIN_LEARNINGS, if present) and
      every question's applicable AL/EX rules routed and obeyed (§24); on mock 1 their
      absence is recorded, not an error.
  18. No preference reduced coverage or waived §18 / the coverage assertion (RE-0); any
      autonomous run waived the inter-batch PAUSE only, never the per-question review.

# ════════════════════════════════════════════════════════════════════════
# §22 — KNOWN LIMITATIONS & SCOPE (disclose in §R9 of every report)
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
# §23 — SUBTOPIC_ID CONTRACT (consumer role — v2.4 cross-step authority)
# ════════════════════════════════════════════════════════════════════════
#   Step 9 is a pure CONSUMER of the subtopic_id contract (the PYQ-phase steps mint; Step 5 enforces;
#   Step 7 joins and is the last writer). Step 9 reads subtopic_manifest.json only to support
#   CLASS detection (§6) and to label the per-class coverage rollup (§20 §R3) — mapping a
#   question to its subtopic_id by matching rendered content to section_rules patterns
#   keyed by id, NEVER by display-name string-match. Step 9 NEVER mints an id, NEVER joins
#   on a display name, and NEVER edits the manifest. The id recipe carries zero exam-
#   specific values (PYQ-phase §15).

# ════════════════════════════════════════════════════════════════════════
# §24 — LEARNINGS CONSUMPTION CONTRACT (consumer-only since v1.21.0)
# ════════════════════════════════════════════════════════════════════════
#   v1.21.0 — THE AUTOMATIC PRODUCER IS GONE. Step 10 was this loop's producer: it distilled
#   the defects it had to FIX into reusable AL-rules so the same mistake was not authored
#   again. With Step 10 retired, NOTHING generates AL-rules automatically any more. This
#   section remains as the CONSUMER half only: any AL-rule file already accumulated stays
#   valid and is still loaded and obeyed, and new rules may be added BY HAND by the author.
#   The schema below is frozen so existing files keep parsing; there is no producer half to
#   keep pinned to it.
#
#   TWO learnings files, both loaded at P1, both exam-agnostic, both OVERRIDE this spec:
#     • [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md — AL-rules ("Audit Learning"). Formerly
#       auto-generated by Step 10; now legacy + manually authored.
#     • [ExamCode]_EXPLAIN_LEARNINGS_v*.md — EX-rules, human-authored guardrails (the
#       hard-won manual fixes). Same mechanism, same precedence.
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
# ════════════════════════════════════════════════════════════════════════
# APPENDIX A — UNIVERSAL EXAM-AGNOSTIC explain_engine.py (MANDATE A) — SINGLE SOURCE
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
#   WHY THE LISTING WAS REMOVED (v1.12): through v1.11 the full engine was reproduced
#   verbatim in this Appendix AND in the (now retired) ExplainAudit spec's Appendix A "for
#   self-containment" — but a reproduced copy and the standalone can silently DESYNC, and
#   the v1.8/v1.9 changelog records that this ALREADY happened once (the embedded copy
#   lagged the standalone's step-number + code fixes). A single canonical copy removes
#   that failure mode — the same multi-copy-drift fix the retired audit steps applied
#   to their auditors. The framework linter (validate_framework_md.py) runs
#   explain_engine.py's `--self-test` directly.
#
#   COMPANION GATE (v1.21.1 — REMOVED): explain_audit_gate.py has been deleted from the
#   framework. Its sole remaining consumer, PYQExplainAudit (PYQ-2), was retired, so no
#   step runs a CA1–CA7 completion gate over any audit_progress.json ledger or Solutions
#   doc. Step 9's §18 self-audit is
#   the whole mechanical certification this document gets.

# ════════════════════════════════════════════════════════════════════════
# FOOTER — this file is the canonical Step-9 spec. On any CONTENT conflict with a loaded
# learnings file — [ExamCode]_EXPLAIN_AUDIT_LEARNINGS_v*.md (legacy/manual, §24)
# or [ExamCode]_EXPLAIN_LEARNINGS_v*.md (human guardrails) — that learnings
# file WINS (it carries hard-won, exam-tested fixes); both are loaded at P1 via
# parse_learnings and applied per §24. A learnings rule NEVER overrides coverage/§18/the
# batch law (RE-0). Deliver the full merged spec on every edit — never a patch.
# END OF Framework_MockTestExplain v1.27.0
# ════════════════════════════════════════════════════════════════════════
