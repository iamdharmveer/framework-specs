# Framework_MockTestCreate v6.3
# v6.3 — 2026-11-13 — GAP-2026-11-13-DIFFICULTY-RUBRIC + GAP-2026-11-13-RUN-NOT-READ (paired with blueprint_core
#   v2.3 Cluster BR, final_assembly v1.19, bootstrap --session-start, Framework_MockTestOrchestrate v1.5.0). Measured: every one
#   of the 358 CSIR past records' bands is reproduced exactly by bc.difficulty_score (r2) from its counts — the
#   scale the schedule was built from — but release 2026.11.12 measured a new question by asking reviewers which
#   120-character past-question opening it 'resembles' (on 31 real past Organic questions of 28-Jul-2025 that judged
#   band matched the recorded one 14 times; the counted band 22 times with the first rules, then with the
#   tightened rules of this release — see CHANGELOG). NEW (S0-BV BV-10..12): reviewers list their moves and
#   principles under the PYQ counting rules and the band is COMPUTED; the author writes to the slot band's measured
#   profile (subtopic -> topic -> section -> exam); no fresh reviewer is never a stop (BV-11); §3 and the helper
#   libraries are RUN by bootstrap.py --session-start from this verified file, not read (S1-0R PYTHON SESSION: ~102,000 tokens less
#   per worker read). Entry v6.2 moved to SPEC_HISTORY.md.
# ════════════════════════════════════════════════════════════════════════
#
# VERSION HISTORY:
# ════════════════════════════════════════════════════════════════════════
# QUESTION: IS mock_test_audit.py REQUIRED?
# ════════════════════════════════════════════════════════════════════════
#
# SHORT ANSWER (v5.36): NO for Step 7 to operate — but it is now the ONLY machine
# auditor that will ever see this paper, so running it is STRONGLY RECOMMENDED and its
# absence must be reported, not shrugged off.
#
# DETAILED ANSWER:
#
# Step 7 (THIS spec) performs a SELF-AUDIT after each batch. Through v5.35 an
# INDEPENDENT audit (Step 8, MockCreateAudit) ran afterwards over the finished mock and
# mandatorily executed the same canonical A-* gate catalogue. THAT STEP NO LONGER EXISTS
# (v5.36 — audit steps retired framework-wide). Consequences, stated plainly:
#
#   • The A-* catalogue in mock_test_audit.py still exists and is still the canonical,
#     hash-tracked auditor (audit_canonical.py). Step 6 still generates it. But it now
#     runs ONLY here, and only per S3-10 / S4-11, and only if it is present.
#   • If it is ABSENT, no machine gate runs over this paper at any point in the pipeline.
#     The S4-11 manual gate checklist becomes the entire mechanical guarantee.
#   • Nothing downstream re-derives an answer, re-tags a subtopic_id, or re-checks a
#     figure. Every "re-verified downstream" claim that used to appear in this spec has
#     been restated against what actually runs.
#
#   In THIS spec (Step 7): the script's --self-test is a FIXTURE-BASED working-auditor
#     check (v2.6). It must print "SELF-TEST: N/N PASS" with N >= AUTH_GATE_FLOOR (35) AND
#     be fixture-based (builds docx fixtures; asserts each gate CATCHES a planted defect and
#     PASSES a clean one). The canonical auditor (audit_canonical.py) self-tests well above
#     the floor. Request a corrected script if it prints N/M with N≠M, N < 35, is a
#     CONSTANT-PRINT stub (no fixtures), exits non-zero, or errors. (The old "24/24"/"13/13"
#     literals and the accept-ANY-N/N rule are superseded — see GATE-COUNT CONTRACT below.)
#     PURPOSE: Self-check before Q1 to verify the script works.
#     IF MISSING: Step 7 CANNOT run the script but CAN still run using
#     spec-level (Claude-executed) gate checking per S4-10/S4-11.
#     v5.36 DECISION (unchanged mechanism, raised stakes): audit.py absence remains
#     WARN (not HARD STOP [HS:PROSE]) + manual checklist — but the warning must state explicitly,
#     in the batch report, that NO machine audit will run over this paper at any step.
#
# THEREFORE:
#   Step 7 (MockCreate): audit.py OPTIONAL to run, MANDATORY to report on
#
# SOURCE OF AUDIT SCRIPT (v5.11):
#   Step 6 (MockBlueprint) v1.20+ auto-generates [ExamCode]_mock_test_audit.py
#   as one of its output files (see Framework_Blueprint.md §13-7A).
#   The script is uploaded to [ExamCode] project Files alongside blueprint.json,
#   registry.json, and other Step 6 outputs.
#   If missing at Step 7 start: verify Step 6 outputs were uploaded to project.
#   The generated script IS the full canonical auditor (no separate "upgrade" step —
#   see audit_canonical.py + Step 6 §13-7A).
#
# ── GATE-COUNT CONTRACT (v5.17 — ONE canonical auditor; fixture-based self-test) ──
# There is ONE auditor across the pipeline: audit_canonical.py — the AUTHORITATIVE A-* gate
# set, carrying the --audit-state COMPLETION GATE (S5-1A, C1-C7) and a
# FIXTURE-BASED self-test (SELF-TEST: N/N, N >= AUTH_GATE_FLOOR = 35). Step 6 generates it;
# Step 7 runs it (v5.36: the only step that does).
# The old two-auditor / 13-vs-66 split is RETIRED — it enabled the hollow-stub false-clean.
# RULE (v2.6 — kills BOTH count-drift AND the hollow stub): a caller runs `--self-test` and
#   accepts "SELF-TEST: N/N PASS" ONLY WHEN the self-test is FIXTURE-BASED (builds docx
#   fixtures; asserts each gate catches a planted defect and passes a clean one) AND
#   N >= AUTH_GATE_FLOOR (35), exit 0. A CONSTANT-PRINT "N/N PASS" that executes no fixtures
#   is REJECTED — it is not a working auditor (P1 hardened, audit_canonical.py).
#   The specific N (35, 43, …) above the floor is INFORMATIONAL; fixture-based + floor is the
#   pass/fail criterion. The stale literals "13/13", "24/24", "52", "65", "66/66" are superseded.
#
# ════════════════════════════════════════════════════════════════════════
# MANDATE 0 — NO QUESTION CONTENT IN CHAT (ABSOLUTE — ZERO EXCEPTIONS)
# ════════════════════════════════════════════════════════════════════════
#
# ALL question content goes to the .docx file ONLY.
# NEVER print any question text in chat: not during generation, not for
# verification, not in debug output, not in status updates.
# If referencing a Q: use ONLY "Q.12 — gate failed" — never the actual stem.
# VIOLATION = exam compromise. This overrides every other instruction.
#
# MANDATE 0b (v5.96, OD-2026-11-09) — NO STOP THE EXECUTED CODE DOES NOT RAISE. A session or worker
# never ends a response early: only a stop that the block it is executing itself raises at that
# point may end it; a predicted non-convergence is handled by running the next step (every quality and
# rule condition has a route: S13-2F bc.sweep_route, S13-2L slot chains). A raised
# "INFRA-HEAL [HS:LADDER]" is not a stop: perform the repair it names and re-run, automatically.
#
# FULL VERSION HISTORY: SPEC_HISTORY.md, section "Framework_MockTestCreate.md".
#   Entries for superseded versions were moved there VERBATIM at framework
#   release 2026.08.15.14 (GAP-2026-08-16-STEP5-SESSION-EXHAUSTION, EC-P42):
#   an EXECUTING session paid for the whole EDITORIAL record before it could do
#   any work. SPEC_HISTORY.md is tracked in MANIFEST.json and verified by
#   bootstrap.py exactly as this file is, and is routed to NO trigger. Nothing
#   was deleted. The entry for the CURRENT version stays above, because
#   Z-VERSION requires the highest changelog entry to equal the header.

# ════════════════════════════════════════════════════════════════════════
# MANDATE 1 — BATCH STOP LAW (DERIVED FROM PRIMARY SOURCES)
# ════════════════════════════════════════════════════════════════════════
#
# SOURCE: T2_MockCreate.md R10, R22, R23, R24, §5 batch flow.
#
# R10:  "Wait for 'continue' trigger before each batch; do not auto-advance."
# R22:  "present_files FORBIDDEN until audit exit 0 + zero fixable WARNs;
#        MANDATORY immediately after."
# R23:  "Append audit STDOUT to batch reply."
# R24:  "Final Assembly runs automatically after Batch 13 (Computer)."
# §5:   "After every batch audit exits 0: call present_files with cumulative
#        docx — MANDATORY."
#
# WHAT THIS MEANS IN CONCRETE TERMS:
#
# After generating questions for ONE batch (max 10Q):
#   STEP 1: Run gate checks (script OR manual checklist)
#   STEP 2: Fix any fixable WARNs. Re-run checks. Iterate.
#   STEP 3: Print "=== BATCH [N] COMPLETE ===" with gate results
#   STEP 4: Call present_files with cumulative docx
#   STEP 5: Print "Type 'continue' to begin Batch [N+1]."
#   STEP 6: *** END THE RESPONSE *** — write NOTHING more
#
# STEP 6 IS THE KEY FAILURE POINT FROM M1.
# Claude generated all 100Q in one response without stopping at Step 6.
# This is now a NAMED MANDATE with equal force to MANDATE 0.
#
# THE "CONTINUE" CONTRACT:
#   - Only "continue" / "go" / "next" (case-insensitive) starts next batch
#   - Any other user message → answer it → end with "Type 'continue'..."
#   - Claude NEVER decides to continue without user trigger
#   - "I'll now start the next batch" in same response = MANDATE 1 violation
#
# FINAL BATCH EXCEPTION (R24):
#   The LAST batch triggers Final Assembly automatically after gate checks.
#   No "continue" needed for Final Assembly — it runs in same response.
#   But all batches BEFORE the last still require explicit "continue".

# ════════════════════════════════════════════════════════════════════════
# MANDATE 2 — GENERATION TECHNOLOGY (retained from v2.0 GAP-05)
# ════════════════════════════════════════════════════════════════════════
#
# For any exam section containing mathematical content (fractions, surds,
# exponents, trigonometry, algebra):
#   MANDATORY: Python + python-docx + OMML helpers (§10-S10-4)
#   BANNED: npm docx package (cannot produce OMML — math renders as plain text)
# For pure text-only exams: either Python or npm docx acceptable.
# NEVER use npm docx when a QA/math section is present.


# ════════════════════════════════════════════════════════════════════════
# §1 — PIPELINE POSITION & SOURCES OF TRUTH
# ════════════════════════════════════════════════════════════════════════

## S0-OP — ORGANIC PARITY + DIFFICULTY INTEGRITY (v6.0 — GAP-2026-11-10-ORGANIC-QUESTION-PARITY + GAP-2026-11-10-DIFFICULTY-INTEGRITY; binding on EVERY paper of EVERY exam)

  OWNER DECISIONS (2026-11-10): D-1 (a) — a slot that no repair can bring to its exact band ends at the
  bounded LAST RESORT (nearest band, fully verified, one AMBER line, an automatic P0 incident), with
  bc.C_REFILL_SESSIONS = 5; the difficulty rules below apply to EVERY item of EVERY exam (organic or not);
  everything ships in ONE release. The organic rules (scope, records, chains, conventions, clone guard,
  figure proofs) apply to every ORGANIC item, decided per item by content (bc.is_organic_item — LAW-ORG-1),
  never by a section, subject or topic name. Where this section and older text in this spec disagree,
  THIS SECTION WINS (S0-OP-11 lists what it supersedes). Nothing here is a stop except the three
  environment failures of S0-OP-10. All constants are bc.op_constants(exam_config) — §6.2 defaults, an
  exam override only through exam_config['constants'], every override printed in the footer.
  EXECUTION ORDER: the S0-OP-0 / S0-OP-2 / S0-OP-7 code runs at S3, immediately after S3-2 has loaded the
  blueprint, exam_config and difficulty_labels and BEFORE the S3 difficulty plan (which reads EXAM_RULER);
  S0-OP-5 runs inside CHECK 3c for every candidate; S13-2P (S0-OP-9) runs after S13-2G and before S13-2L;
  S13-4OP (S0-OP-7) runs inside S13-4 right after `registry = _commit['registry']` (before the registry is written).

### S0-OP-0 — MIGRATION ON FIRST USE (automatic; GAP §9)

  Before Q1, once per exam per release: (1) classify every PYQ record (bc.organic_flag); (2) records below
  bc.PYQ_SCHEMA_VERSION or with status 'partial' / 'unverified' (bc.pyq_record_status) are BACK-FILLED by
  Framework_PYQExplain §13A-3 BACKFILL in fresh Orchestrate workers (O-BACKFILL — Phase B re-read of the zoom
  tiles, Phase C completeness gate, two fresh blind grades per record) from the page images already in the
  project; progress is saved and resumed, no user step; (3) the exam ruler is (re)built (S0-OP-2); (4) the
  reserve and the series registry are read from registry.json (S0-OP-7; the series registry is seeded from
  every delivered mock's committed keys). A record that cannot reach 'full' stays 'partial' with its missing
  list: excluded from every target pool, INCLUDED in the clone guard. Papers delivered before this release
  are never re-certified (their audits keep the legacy verdicts).
  (Executable block '# ── S0-OP-0 / S0-OP-1 (v6.0) ──' — runs INSIDE S3-2, right before the difficulty plan; see there.)
  v6.2: the back-fill runs BEFORE Q1 only when the exam config sets 'pyq_backfill_before_q1': true; otherwise Q1
  starts at once and the ruler's anchors use the PYQExplain bands (S0-BV BV-7). When it is set and OP_NEEDS_BACKFILL
  is not empty the orchestrator runs O-BACKFILL to completion BEFORE Q1. O-BACKFILL writes each upgraded record into
  /home/claude/{EXAM}_op_profile.json (saved per record, so a resumed run continues), then this block and the
  S0-OP-2 block are RE-RUN (bc.ruler_needs_recalibration sees the new graded_count and rebuilds EXAM_RULER from
  the exam's own anchors) — S3 placement and Q1 use only the rebuilt ruler. S13-4OP stores the upgraded records
  in registry.json['pyq_backfill'] (bc.profile_backfill_delta), so the next run restores them (bc.profile_overlay);
  a record that stays 'partial' is re-read at most bc.C_PYQ_REREAD_MAX times in all; no user upload is needed. A newer PYQExplain profile upload wins. A record whose re-reads reached bc.C_PYQ_REREAD_MAX is
  not listed again: it stays 'partial' (out of every target pool, in the clone guard). With nothing listed
  the run starts at once.

### S0-OP-1 — ORGANIC SCOPE PER SLOT (G-01)

  A slot is ORGANIC when its subtopic is in OP_SCOPE['organic_subtopics'] (>= bc.C_ORG_SUBTOPIC_SHARE of its past
  records organic) or its
  generated item is organic (bc.is_organic_item on the item record); every organic rule reads the item's
  'organic' flag (written on every concept_map entry with 'organic_reason'), never a name.
  bc.l2_applies(..., record=<item>, organic_subtopics=OP_SCOPE['organic_subtopics']) is the ONE predicate.
  A mixed section applies organic rules per slot; a text-only organic item has no figure rules to run.

### S0-OP-2 — ONE CALIBRATED RULER PER EXAM (G-08, LAW-ORG-5, DIFFICULTY-LAYER-LAW)

  The ruler is bc.build_difficulty_ruler over the exam's verified past items, each graded by TWO FRESH BLIND
  GRADERS (records' blind_grade_1 / blind_grade_2, written by the back-fill): anchors = items both graders put
  in the same band; a band with < bc.C_ANCHOR_MIN anchors borrows library-level anchors, then the neighbouring
  band (recipe interpolated, flagged — never a stop). The ruler (anchors, recipe per band, past distribution,
  grader prompt version, model id, date) is frozen in registry.json['difficulty_ruler'] and recalibrated
  automatically (bc.ruler_needs_recalibration: grader model changed, anchor re-grade agreement <
  bc.C_RULER_AGREE, papers added). The generic rubric (bc.assess_difficulty, CLASS_BASELINE, the qtype floor
  classes) is a GRADER INPUT only — it never decides a band; whether an Easy figural / MSQ / NAT item exists is
  decided by the anchors (bc.ruler_min_band). Every artefact prints the ruler's past distribution; the
  requested schedule is printed separately as "requested" — neither is derived from the other.
  (Executable block '# ── S0-OP-2 (v6.0) ──' — runs INSIDE S3-2, right after S0-OP-0 / S0-OP-1; see there.)

### S0-OP-3 — THE SCHEDULE IS INPUT (G-09, LAW-ORG-6)

  S3 normalises the request ONCE (bc.schedule_normalize; SCHEDULE_APPLIED) and places it ONCE
  (bc.schedule_place — never infeasible; the exam's anchors decide which positions take a band first). The
  request, the applied counts (with every normalisation note) and the placement are FROZEN in batch_state by
  bc.schedule_freeze and are read-only from then on: no later step may swap, carry, hold, force or relabel a
  position; a resumed run restores them, never recomputes them. A per-section schedule wins over a
  whole-paper one (the whole-paper figure is recomputed from it and printed). The footer prints "schedule as
  applied" (Framework_DeliveryFooter §2D). bc.schedule_frozen_check(batch_state, labels) must pass at S13-2L
  except for the slots in batch_state['last_resort_slots'] (each with its AMBER line).

### S0-OP-4 — THE SLOT PLAN AND THE AUTHOR BRIEF (G-04, G-05, G-06, G-13)

  For every slot: band (fixed at intake), qtype, the band RECIPE (EXAM_RULER['recipe'][band]: decision range, ask
  formats, substrate heavy-atom IQR, stereocentre range, near-isomer distractor share, conventions); for an
  ORGANIC slot also: the CHAIN source — bc.l2_slot_source(cards, band, subtopic, used, seed,
  min_decisions=<recipe minimum>, chains=bc.chain_compose(<exam cards + library cards>, <recipe minimum>,
  max_len=<exam's longest past chain>)) — a single concept is NEVER a source for a band needing >= 2
  decisions (F-06.2); a composed chain is used only after a blind forward solve; the asked unknown rotates
  between product, intermediate, starting material, reagent and A-and-B (F-06.5) toward the format floors
  (bc.format_floors over bc.format_shares(OP_TARGET_POOL)); the drawing CONVENTION — bc.scaffold_convention
  (bridged bicyclic -> perspective, axial / equatorial ask -> chair, sugar -> the exam's sugar convention,
  decalin / steroid -> ring-fusion H) and the convention floors (bc.convention_floors over
  bc.convention_shares(OP_TARGET_POOL)). Low supply NEVER lowers a band (F-06.6): it triggers composition and
  the library. The author worker reads bc.author_brief(<slot blocks>) (<= bc.C_BRIEF_MAX_PAGES pages: chain,
  decisions, ask format, recipe, convention, two real exemplars of the same family) and the engine call list —
  not the full spec (Framework_MockTestOrchestrate O-AUTHOR).

### S0-OP-5 — THE CONTROLS OF EVERY ITEM (every exam; G-03, G-07, G-08, G-10, G-11, G-12)

  v6.1 (S0-BV, owner 2026-11-11): each slot is written ONCE (bc.k_candidates() = 1), by an author holding the
  SAME anchors the graders will compare with (bc.bv_author_packet over bc.bv_anchors) and the recipe ranges, and
  the controls run INSIDE THE BATCH (S4-7 STEP A2) — never first at Final Assembly. A split between the two
  graders gets one more grader (never a rewrite); a question is rewritten at most ONCE (bc.C_WRITE_ATTEMPTS),
  only when the majority names another band or the key is disputed; after it, it is delivered at the band it
  measured, disclosed (bc.bv_set_label 'measured_majority'). (Superseded: "3 candidates; 5 once a band has
  missed".)
  THE CANDIDATE RECORD — ONE dict per candidate; every control below receives that SAME dict and the winner
  becomes its concept_map entry (field names exactly): qtype, subtopic_id, organic, organic_reason,
  stem_text, option_texts (the S7-QUALITY names), figure_files, option_smiles {label: smiles} (structure options),
  key (the correct option / value), key_smiles (the
  answer structure, when it is one), starting_smiles, reagents [...], species [{role: stem|scheme, id, smiles,
  stereo_mode}], declarations, irrelevance, ask_format, answer_kind, task_template, asked_reaction,
  structure_named (a structure given by name only), chain, decisions_author. A field that does not apply is
  omitted, never invented; key_smiles and every option_smiles value are stereo-checked by C1 even when species
  does not list them:
    C1 STEM STEREO (organic) — bc.stem_stereo_gate: every stereo element of the stem, key and options drawn,
       named, declared rac / rel / mixture, or 'irrelevant' with a re-solve proof (LAW-ORG-9).
    C2 ORIGINALITY (organic) — bc.clone_guard(item, past=OP_GUARD_POOL, library=OP_LIBRARY['fingerprints'],
       series=bc.series_registry_rows(<registry series_registry>)): structure clone -> replace; reaction /
       task near-clone -> mutate (change the scaffold class, add a competing site or a controlling
       stereocentre, swap the chain) and re-run every control (LAW-ORG-10). A text item keeps the PYQ-distance
       gates AND (v6.1, S0-NF-5) passes bc.text_clone_guard against the PYQ corpus and the series registry.
    C3 EASY FLOOR (organic Easy) — bc.easy_quality_floor: >= 1 decision on a drawn or named structure; the
       stem never names the reaction whose outcome it asks.
    C4 RECIPE — bc.band_recipe_check(item, recipe[band]) -> grades['recipe'] (decisions, ask format,
       substrate inside the band's ranges). v6.1: for EVERY item the verdict is
       bc.band_recipe_check_any(item, EXAM_RULER['recipe_by_subject'], band) — MIP-credited decisions inside the
       subject's range (S0-NF-3); DORMANT (no range anywhere) is recorded as dormant and is never a pass.
    C5 TWO FRESH BLIND GRADERS (v6.1: in the item's own batch, S4-7 STEP A2; a split -> a THIRD fresh grader,
       label by majority: bc.band_majority) — each a FRESH context (a sub-agent, or an Orchestrate worker) that receives
       ONLY bc.build_judge_input(item_record, <ruler anchors with content>) — never difficulty_plan, the
       band, difficulty_obs, the solution or the author's counts — and returns {band, decisions}. Its packet
       sha256 and context 'fresh' are recorded in grades['packets'][grader_n]. A grade produced in the
       author's own context is NOT a control and is never recorded as 'fresh'. When no exemplar exists for
       a band the anchors come, in order, from the library level, then the exam's exemplar bank items
       of that band, then the band recipe written out in words (EXAM_RULER['recipe'][band]) — a grader is
       NEVER told to agree by default (the v5.92 DORMANT 'agree' path is RETIRED).
    C6 DECISION CONTRACT — bc.decision_contract_check(author decisions, grader_1 decisions, recipe minimum).
    C7 TWO FRESH BLIND SOLVERS — each a fresh context given the stem and options only; each returns its
       answer, confidence and every assumption it made. bc.key_unanimous(author, [s1, s2], qtype, NAT
       tolerance) and bc.solver_assumption_check: a decisive assumption fails the candidate (LAW-ORG-7).
       Recorded as key_votes {author, solver_1, solver_2, unanimous}.
    C8 FIGURE PROOFS (organic figures) — S0-OP-8; every other structure / data figure — S0-NF-7.
    C9 MINIMAL IDENTIFYING PARTS (v6.1, every multi-part item) — S0-NF-4.
    C5 (v6.1) also records the graders' {class, computation_generic, concept} in concept_map[q]['grader_meta'] (S0-NF-8).
  The label is written ONLY by bc.dl_set_label_basis_strict(entry, 'measured_exact', labels, band,
  {grader_1, grader_2, recipe}, packets): ok only when both graders AND the recipe name the band
  (bc.band_exact — no vote); v6.1: or by bc.bv_set_label (S4-7 STEP A2) — 'measured_exact' when both graders
  agree, 'measured_majority' when a third grader settled a split or the item was delivered at its measured band
  after its one rewrite (verified by bc.verify_difficulty_label strict). A candidate that grades another band is never relabelled: it is a failed
  candidate (it may still enter the reserve at the band it graded EXACTLY at). Record on the concept_map entry
  (committed by final_assembly QINDEX_OP_FIELDS): organic, organic_reason, chain, decisions_author,
  decisions_grader, grades {grader_1, grader_2, recipe, packets, item_hash}, key_votes, clone_check,
  stereo_gate, figures [{identity_ok, vision_ok, gates_ok, layout_attempt}], and the C2 item fields
  key_smiles, starting_smiles, reagents, ask_format, answer_kind, task_template (the exact dict passed to
  bc.clone_guard; its result's 'fingerprint' is stored inside clone_check, so the series registry
  (bc.series_registry_add) and the reserve exclusion (bc.op_key_ids) always see the key).
  THE WRITER (v6.0): every control record is written by ONE call, OP_WRITE_CONTROLS(q, grader_1, grader_2,
  packets, key_votes, decisions_grader, figures, clone_check, stereo_gate) — defined at S3-2 (S0-OP-0 block), it
  wraps bc.op_record_controls and computes the recipe verdict at the entry's label band. v6.1: for a batch
  question the controls are written by S4-7 STEP A2 (bc.bv_apply, which calls bc.op_record_controls with the
  fresh results); CHECK 3c only writes the question and its sidecar entry (the candidate record fields above
  travel in quality={...}) and never grades in the author's context; the S13-2G delta round calls
  it for every re-graded item in delta_qs (O-GRADE on the item's CURRENT text). Each record is bound to the
  item's own text (bc.op_content_sha); S13-2L reads it only while bc.op_controls_current holds, so a replaced item
  is never certified on its predecessor's grades, and a hand-written grade is not a grade.
  A surface that can start neither a sub-agent nor an Orchestrate worker cannot produce a fresh grade: that is
  the NO-MODEL environment failure (S0-OP-10) — the run saves state, prints one instruction and resumes; a
  same-session grade is never counted as fresh and nothing is delivered uncertified.

### S0-OP-6 — BAND OPERATORS (F-10.2; DR2, refill, last-resort generation)

  (v6.1: the operators for a NON-organic item are defined in S0-NF-3 — they replace "one inferential move".)
  To RAISE a band: add a decision (chemo-, regio- or facial selectivity), add a controlling stereocentre,
  ask for the starting material or for A and B, tighten the distractors to near-isomers. To LOWER: remove a
  decision, or ask the forward product of one step. Operators are drawn from the exam's recipe (S0-OP-2), so
  they work for any exam and any subject (a non-organic item raises / lowers by one inferential move or one
  concept, inside the recipe's decision range). Every operated item is a new candidate: every control again.

### S0-OP-7 — RESERVE AND SERIES REGISTRY (F-07.4, F-10.3)

  The reserve (bc.reserve_new / reserve_add / reserve_take) and the series registry (bc.series_registry_add /
  series_registry_rows) persist in registry.json['reserve'] and registry.json['series_registry'] (the Step 7
  contract stays exactly two delivered files). During the run they live at /home/claude/{EXAM}_reserve.json and
  /home/claude/{EXAM}_series_registry.json and are committed by S13-4. A reserve item is used only if it was
  never delivered, its clone and series guards are re-run at use time, and it is re-graded when its ruler
  version differs. A delivered paper's items (keys, chain ids, task templates) are added to the series
  registry at S13-4, so no later mock repeats them.
  (Executable block '# ── S0-OP-7 load (v6.0) ──' — runs INSIDE S3-2 after S0-OP-2; '# ── S13-4OP (v6.0) ──' runs INSIDE S13-4
  right after `paper_id = _commit['paper_id']`; see there.)

### S0-OP-8 — ORGANIC FIGURES: GEOMETRY, IDENTITY, VISION (G-11, G-12, LAW-ORG-8)

  Every structure of an organic item (stem, every option, every scheme species; explanations and notes too) is
  laid out by corpus_io.organic_structure_layout (metal coordination as dative bonds — G-METALCHARGE; every
  stereo element defined or declared — G-STEREODEF; the bounded re-depiction ladder with the perspective
  templates — G-BONDCROSS / G-BONDLABEL / G-LABELOVERLAP / G-ATOMCLASH; identity re-perceived from the drawn
  MolBlock — G-IDENTITY), option sets by corpus_io.option_set_align (one scale, one orientation, distinct
  molecules), chair / Newman / sawhorse / Fischer / Haworth figures by corpus_io.render_projection (the PROVEN
  renderers — figure_types renderer 'corpus_io.render_projection', identity kind STRUCTURE_CONFORMER). After
  rendering, a FRESH vision pass that never saw the SMILES transcribes every rendered structure;
  figural_vision.readback_compare(intended, read_back, stereo_mode) must match — 2 independent reads when the
  answer depends on stereo, else 1; a read that disagrees with a geometrically correct drawing triggers a
  second read, then a re-depiction, never an accept on one read. corpus_io.organic_figure_proof records
  identity_ok / vision_ok / gates_ok from ONE figure dict built exactly so: {'kind': <the convention tag, e.g.
  'skeletal' or 'chair_conformation'>, 'smiles', 'stereo_mode', 'role': 'stem'|'option', 'width_in',
  'answer_depends_on_stereo', 'vision_reads': [{'smiles', 'match': figural_vision.readback_compare(...)['match']}],
  and 'layout': corpus_io.organic_structure_layout(...) for a 2-D structure OR 'projection_proof': the second
  value of corpus_io.render_projection(kind, smiles, ...) for a chair / Newman / sawhorse / Fischer / Haworth};
  its result is the item's figures[] entry. v6.1 (S0-BV): the author records each figure dict WITHOUT vision_reads,
  plus 'file' (the rendered image), in quality={'figure_dicts': [...]}; S4-7 STEP A2 runs the fresh vision reads in
  the batch (roles vision_<figure>_<read>) and writes figures[] — a figure read back as another structure is redrawn
  as the question's one rewrite. The FigureSpec carries spec['organic'] = True, spec['proof'] = that record
  and spec['geometry'] = draw.geometry, so figural_core G-ORGPROOF / G-FIGCOLLIDE (audit A-ORGPROOF /
  A-FIGCOLLIDE) re-check them. corpus_io.min_size_gate: stem >= 1.0 in, option >= 0.8 in wide. A figure that
  cannot be proven is never shipped: the item is replaced (S13-2L quality chain).

### S0-OP-9 — PARITY AT ASSEMBLY (LAW-ORG-11; runs as S13-2P before S13-2L)

  (Executable block '# ── S13-2P parity (v6.0) ──' — section S13-2P, right before S13-2L; see there.)
  Formats are planned UP FRONT so parity is met by construction: S3-12d's shape plan and the author brief
  (S0-OP-4) carry the floors, and an author may write a slot in a converted form with the band kept (a chain item ->
  two_part; a stereo / selectivity item -> statement_combination; a same-family set -> match_list; a forward item ->
  starting_material — bc.FORMAT_CONVERTERS), every control again. At assembly S13-2P MEASURES and records; no
  automatic re-authoring is scheduled for a format shortfall (band counts always win over format floors): a floor
  still short is DISCLOSED — the footer line "Organic parity: FAIL — short ..." (difficulty_state.chain_footer['info'],
  written by S13-2L) — never hidden and never a stop. A figure-proof miss opens that item's quality chain (S13-2L
  step 2b re-checks the proofs on every pass; after two replacements still without a structure proof record the slot
  is disclosed on an AMBER line — bounded). A last-resort slot is final: its item passed every control when chosen.
  The §LADDER-OP lines (requested / applied schedule, exam ruler, schedule notes, constant overrides, organic parity) are
  written ONCE by S13-2L into difficulty_state.chain_footer['info'] (committed by S13-4); Create S13-6 and MockDeliver
  3f''' print them verbatim with the chain footer.

### S0-OP-10 — THE ONLY STOPS (G-14, LAW-ORG-12)

  Every former stop site names its automatic repair (bc.STOP_REPAIRS / bc.stop_repair_for). The ONLY halts are
  the three environment failures bc.ENVIRONMENT_FAILURES: NO-FRAMEWORK (primary, DR mirror and the project
  cache all unavailable), NO-SOURCE-DATA (an exam with no source papers and no registry at all), NO-MODEL (no
  model / workspace / fresh context the platform can provide). Each saves state, prints ONE plain instruction
  and resumes automatically when the environment returns; none ever delivers anything uncertified.

### S0-OP-11 — WHAT THIS SECTION SUPERSEDES (for every paper produced by this release)

  * the S3 difficulty-feasibility stop, the per-section plan stop and both difficulty-profile stops —
    replaced in place by schedule_normalize / schedule_place / the ruler (S0-OP-3).
  * CHECK 3c (a) INDEPENDENT RATING in the author's own context, and its DORMANT 'agree' path — replaced by
    C5 (two fresh blind graders). CHECK 3c (b0) L2 'binding' band as a label basis — replaced by C4 + C5 (the
    L2 load is a grader input). The rubric bands of difficulty_authoring_profile — authoring hints only.
  * S13-2L / S13-2R v5.96 endings (band swap, paired upgrade, schedule-forced, panel, re-key, majority,
    DISCLOSED) — replaced by the SC2 endings (reserve_refill -> refill_session -> last_resort).
  * Label bases obs / l2 / none / dr3 / review (swap) / forced / held — never written for a new paper; the
    auditor rejects them on any paper produced at or after 2026.11.10 (A-QINDEX check 8, LB2-strict).

## S0-NF — NON-ORGANIC FIDELITY (v6.1 — GAP-2026-11-11-NONORGANIC-MOCK-FIDELITY; binding on EVERY paper of EVERY exam, every subject)

  S0-OP made difficulty and originality honest for organic items. S0-NF extends the same guarantees to every
  item, organic or not, and adds paper COMPOSITION (subject / topic / format / class / band per subject). Owner
  decisions (binding): D-01 every target is computed at run time from the exam's own PYQ corpus and carried by
  the blueprint — no exam name, subject name or number appears in a rule; D-02 one code path for all exams;
  D-03 nothing new may stop a run — a shortfall is repaired automatically and, if the bounded ladder does not
  converge, the paper ships with an AMBER line; D-04 no manual review; D-05 Create never recomputes a target —
  it reads the blueprint; D-06 every count used for a verdict is MEASURED by an independent pass, never taken
  from the author's own record; D-07 a rule whose input is empty for an exam is DORMANT (one line). Precedence
  when two targets cannot both be met for one slot (the higher wins, the lower is disclosed): Part counts and
  qtype positions > band per slot > subject per Part > topic per subject > formats > question class > subtopic
  even spread.

### S0-NF-0 — TAXONOMY BINDING AT START (F-08)

  At S3-2, after the blueprint and the manifest load: MH = bc.manifest_hash(manifest). If blueprint
  ['manifest_hash'] exists and differs (EC-28), the allocation is crosswalked automatically —
  cw = bc.manifest_crosswalk(<manifest the blueprint was built on, from the registry snapshot or the previous
  manifest file>, manifest) (id equality, then normalised display name, then parent topic; a split old id counts
  at its parent topic — EC-29), the crosswalk is printed and the run continues — never a stop. Every join uses
  bc.norm_label (EC-30: quote / dash / case variants are equal). A delivered item's subtopic is a MANIFEST ID
  (bc.nf_resolve_subtopic_id); the "Topic / Subtopic" lines printed in the docx come from the manifest display
  names, never from author text. MH is written into batch_state, every concept_map entry (manifest_hash) and
  the registry paper record (final_assembly commit_registry(manifest_hash=MH)). The exam manifest's own literal
  'manifest_version' is never read or overwritten (amendment B).

### S0-NF-1 — COMPOSITION: SUBJECT AND TOPIC PER SLOT (F-01)

  The slot plan (S3-12b) places exactly the blueprint's per-mock subtopic allocation (Blueprint §4-1c already
  makes subject and topic counts exact per mock). A replacement or refill for a slot — S13-2L quality chain,
  reserve_refill, refill_session, last_resort — keeps the slot's subtopic_id; when that subtopic cannot yield a
  passing candidate the next source is bc.refill_order(slot_sid, manifest, candidates): a sibling subtopic of
  the same topic, then another topic of the SAME subject (recorded as a topic relaxation). A slot is NEVER filled
  from another subject (EC-10). The auditor's A-ALLOC re-measures this on the delivered paper.

### S0-NF-2 — FORMAT PLAN FOR EVERY SUBJECT (F-03; generalises S3-12d / S0-OP-9 for every subject)

  For each subject x Part, FT = blueprint format_target_per_mock[mock][part][subject] ({ask_format: n}). S3-12d assigns each
  target format to specific slots with bc.format_plan_slots(slots, FT, manifest) — a slot whose subtopic shows
  the format in its PYQs (manifest axis2_capability) first, then its topic, then its subject; a format no slot
  can take is recorded INFEASIBLE (EC-14), never a defect. The author brief carries the slot's format; an
  author may convert content with bc.NF_FORMAT_CONVERTERS (several facts about one entity -> statement
  combination; a same-family set -> match list; a comparable set -> order / ranking; a causal claim ->
  assertion-reason only when the subject's PYQs use it), band and subtopic kept, every control again. A format
  target that conflicts with the slot's band loses (EC-15 — band wins, the shortfall is disclosed). EC-16: an
  exam whose PYQs never use a format has target 0 and the converter never fires.
  MEASUREMENT (D-06): the delivered item's format is RE-MEASURED by bc.nf_measure_axis2(item,
  figure_types.normalise_ask_format) — the SAME function PYQExplain used to write every PYQ record's ask_format,
  so targets and measurements share one vocabulary (statement | match | sequence | combination |
  assertion_reason; direct = the residual) — and written as concept_map[q].measured_axis2; the author's
  ask_format is never counted. S13-2P (generic parity) compares measured vs FT with bc.nf_parity per subject x
  Part; a shortfall converts an UNLOCKED slot of that subject x Part (band and subtopic kept), bounded by
  bc.C_REFILL_SESSIONS; still short -> nf_disclosed['A-AXIS2'] and the footer line "Format parity: short ...".
  The organic floors of S0-OP-9 are one case of this rule.

### S0-NF-3 — DIFFICULTY FOR EVERY ITEM: VOCABULARY, RECIPE, OPERATORS (F-04)

  Decisions are tagged from bc.ALL_DECISION_TAGS = the organic tags + bc.GENERIC_DECISION_TAGS:
  multi_entity_comparison (>= 3 entities each evaluated AND they are MIP parts — S0-NF-4), concept_chain (the
  result of one concept is the input of a second), exception_case (the general rule leads to a distractor; the
  key needs the exception), data_interpretation (the key needs reading a figure, spectrum, plot or table of
  values), derivation (a relation must be derived, not recalled), quantitative_chain (>= 2 dependent
  computations, each with a different relation), specific_knowledge (a named fact outside the subject's core,
  as the exam's anchors in that band show). NEVER a decision (bc.NF_NEVER_DECISIONS): unit conversion, plain
  arithmetic, a stacked part outside the MIP, recall of a formula printed in the stem. The credited count is
  bc.nf_decision_count(decisions, mip).
  The recipe is per SUBJECT: blueprint['recipe_by_subject'] (D-05 — Blueprint §7-10, bc.build_recipe_by_subject
  with the manifest: cascade subject -> exam -> library, EC-21; a band with no anchors anywhere is DORMANT and the
  graders decide, EC-22 — never a pass by default); a blueprint without it uses EXAM_RULER['recipe_by_subject']
  (the ruler is built with manifest=, so its subject keys are the manifest sections too). C4 uses
  bc.band_recipe_check_any for every item, with item['subject'] = bc.nf_subject_key(item, manifest).
  BAND OPERATORS for any subject: RAISE = add an entity to a comparison, chain a second concept, choose an
  exception case, turn a given into data to read, tighten the distractors so the key needs more parts (higher
  MIP). LOWER = the reverse. Every operated item is a new candidate: every control again.

### S0-NF-4 — C9 MINIMAL IDENTIFYING PARTS (F-05)

  Applies to items whose options are vectors of parts ('respectively', two_part, statement combination, match
  list, order / ranking). C9 computes mip = bc.nf_item_mip(stem_text, option_texts, key, measured ask format) —
  None for an item that is not multi-part; key 1-based or a letter, the sidecar 'answers' convention (rows parsed by
  bc.parse_option_parts) and records concept_map[q].mip. Only the MIP parts count as decisions (S0-NF-3):
  stacked parts beyond the MIP add no difficulty, so a 3-part item decidable from one part is credited one
  decision and fails C4 in a band whose range needs more. The paper's share of MIP = 1 items per subject x Part
  may not exceed blueprint mip1_share (A-OPTPART). Repair: regenerate the distractors so the key needs more
  parts (band and stem kept), all controls again; bounded; AMBER if unresolved. Unparseable options (EC-18) and
  MSQ / NAT (EC-20) are exempt and counted.

### S0-NF-5 — ORIGINALITY FOR EVERY ITEM (F-06; extends C2 and S0-OP-7)

  Every candidate records task_template (bc.task_template — numbers, unit values, formulas, entities and proper
  nouns masked), asked_quantity (bc.asked_quantity), answer_kind, named_concepts and given_in_stem (the formulas,
  identities, values and intermediate results the stem SUPPLIES). C2 adds bc.text_clone_guard(item,
  past=<PYQ records>, series=bc.nf_series_text_rows(series_registry)):
    * same subtopic + same template as a PYQ = a near-clone, allowed ONLY when depth-preserving — credited
      decisions >= the PYQ's AND the stem supplies nothing the PYQ made the solver supply (EC-24); else MUTATE
      (remove the supplied element or add a decision), every control again;
    * same subtopic + same template as an item of an earlier delivered mock = REPLACE; the same template on a
      different subtopic is allowed (EC-25).
    Both comparisons run only for a DATA-BEARING, non-organic item (the stem itself states a value, formula or
    named entity); a generic stem whose content is a drawn structure is guarded by the organic structure guards.
  S13-4 adds every delivered item (any subject) with bc.nf_series_registry_add.

### S0-NF-6 — WITHIN-PAPER UNIQUENESS AND KEY LEAK (F-07)

  At S13-2 (before S13-2L): bc.intra_paper_duplicates(items) — no two items of one paper share a text
  fingerprint (same subtopic, template and asked quantity — compared only for DATA-BEARING stems; an item whose
  content is a drawn structure is compared by its structure), the same blind-grader `concept` tag in the same
  subtopic, or an organic key structure; the LATER item is re-authored in the same slot (same subtopic, same
  band). bc.key_leak_check(items, <PYQ stems>) — an item's key value may not appear as given data in another
  item's stem or options: numbers within +-0.5 % AND the same quantity (the same unit; a unitless key only when it
  has >= 4 significant figures, or >= 3 with no unit on either side); a text key of >= 2 words only in another
  item's STEM, after normalisation, and never a label combination ('A and C only', '(i), (ii) and (iv)'); exempt: small
  integers (|x| <= 10) and any unitless integer, single common words, values in >= 5 % of the exam's PYQ stems
  (EC-26 / EC-27); the later item's dataset is changed. (Validated on CSIR Mock 01: exactly the Q41 -> Q96 leak.) NAT keys are checked too (EC-20). Bounded;
  AMBER if unresolved (A-INTRADUP / A-KEYLEAK).

### S0-NF-7 — FIGURES FOR EVERY SUBJECT (F-09; widens S0-OP-8)

  Every structure figure that contains a metal or a charged species — organic or not — goes through
  corpus_io.metal_charge_gate (G-METALCHARGE) and the fresh vision read-back (figural_vision.readback_compare),
  and its FigureSpec is checked by bc.metal_figure_convention(spec, FIGURE_STYLE_PROFILE): coordination entity
  in brackets with the overall charge outside; no formal charge on the metal or on a CO / CN / NO ligand atom;
  ligands as plain bonds; dative arrows / ligand-atom charges only when the exam's PYQ figures show them
  (FIGURE_STYLE_PROFILE['conventions']['dative_arrow' | 'atom_charge_label']['share'] > 0; a tag the profile does
  not carry = never seen = not drawn — EC-32); a free counter-ion keeps its charge (EC-31). bc.stem_figure_consistency(stem, spec) checks every
  geometric / identity claim of the stem (linear / bent with angle, cis / trans, oxidation state) against the
  spec's 2-D coordinates; a claim the drawing cannot show is skipped and recorded (EC-33); a contradiction =
  re-render, then replace — never shipped. concept_map[q].figures[i].spec carries the spec for A-STEMFIG.
  A curve that represents one function (a wavefunction, a potential) must pass bc.curve_continuity at its region
  boundaries; no mark outside the plot data (A-FIGINK). DATA FIGURES: where the exam's manifest
  (figural_count_by_subtopic) and PYQ figure classes show them, a slot may be authored as a computed data figure
  — bc.data_figure_points(kind, params) + figure_types.render_data_figure (EPR_SPECTRUM, MOSSBAUER_SPECTRUM,
  NMR_MULTIPLET, MS_ISOTOPE_PATTERN, RATE_PLOT, CV_TRACE) — so the picture always matches the key; a kind
  without a generator (TANABE_SUGANO) returns 'EC-34' and the item is re-authored to a text form of the same
  subtopic and band (EC-34). Kinds the exam's PYQs never use stay dormant (D-07).

### S0-NF-8 — QUESTION CLASS AND BAND PER SUBJECT (F-10, F-11)

  CLASS: the author brief carries the slot's class from blueprint class_target_per_mock (recall /
  computational / derivational / figural / structural ...). The two fresh blind graders (C5) also return
  {class, computation_generic, concept} (extra output fields; their packet is unchanged); C5 writes them to
  concept_map[q]['grader_meta'] = {'grader_1': {class, computation_generic, concept}, 'grader_2': {...}} — next
  to grades (which keeps grader_1 / grader_2 = the band strings, unchanged). The measurement is independent
  (D-06; a value counts when both graders agree); A-CLASSMIX compares measured with targets per subject x Part. A shortfall re-authors an
  unlocked slot of that subject x Part into the short class (band and subtopic kept), bounded; AMBER if
  unresolved. A class target that conflicts with a format target loses (EC-35).
  BAND PER SUBJECT (amendment A): S0-OP-3 still normalises and freezes each Part's band COUNTS exactly as
  before. Their PLACEMENT is now subject-aware: split = blueprint subject_band_target_per_mock[mock][part]
  (bc.subject_band_split of the frozen counts by each subject's PYQ mix), and the frozen placement is
  bc.schedule_place_by_subject(split, {q: subject of the slot}, qtype_by_q, labels, ruler) — schedule_place run
  inside each subject's positions. A subject absent from the split keeps the whole-Part placement. The
  per-subject placement is frozen with the schedule (bc.schedule_freeze) and read-only afterwards.
  A-SUBJBAND re-measures the delivered bands (two blind graders) per subject.

### S0-NF-9 — DISCLOSURE, RECORDS, MIGRATION (D-03, D-06; EC-37)

  After the bounded repair of S0-NF-2 / -4 / -6 / -7 / -8 a gate still short is written to the sidecar AND the
  registry record as nf_disclosed {gate: reason} (final_assembly commit_registry(nf_disclosed=...)); the
  auditor then reports it as "AMBER — DISCLOSED" (never a stop) and Framework_DeliveryFooter §2E prints the
  line. concept_map entries carry subject, part, mip, given_in_stem, measured_axis2, text_fingerprint,
  stem_text, option_texts and manifest_hash (final_assembly QINDEX_NF_FIELDS). A resumed run keeps its frozen
  plans; the S0-NF targets apply from the next paper (EC-37). A blueprint without the v1.65.0 fields: the
  S0-NF composition / format / class / band rules are DORMANT for that paper (one line asking for
  `MockBlueprint --refresh`); S0-NF-3 to -7 (item controls) run regardless.

## S0-BV — BATCH VERIFICATION (v6.1 — GAP-2026-11-11-BATCH-VERIFICATION; owner 2026-11-11; binding on EVERY batch of EVERY exam)

  WHY. Measured on a 40-question Organic paper (TestCreate, 4 batches of 10, release 2026.11.10): Final Assembly
  found 29 of 40 questions to re-write (27 below their difficulty slot, two too close to past questions, two
  figure re-draws) and then stopped for room. Cause: the controls S0-OP-5 requires (fresh graders, fresh solvers,
  fresh vision) need a fresh context; a worker cannot start one and no worker message could request one — so no
  item was measured independently until the end. Second cause: the author wrote without the graders' anchors,
  and two graders who disagreed forced a rewrite of a question that may have been right.
  THE LAW (LAW-BV-1..6):
    BV-1 Every question is measured by two fresh blind graders and two fresh blind solvers (plus the fresh
         vision read of S0-OP-8 for an organic figure) INSIDE ITS OWN BATCH — S4-7 STEP A2, before STEP B — and
         the batch is never delivered before `STEP A2: DONE` (B-7). WORKER MODE requests them with GRADE_REQUEST
         (Framework_MockTestOrchestrate O3-9).
    BV-2 ONE write per slot, made with the graders' own anchors (bc.bv_anchors -> bc.bv_author_packet) and the
         recipe ranges; the author runs bc.band_recipe_check_any before submitting.
    BV-3 Three fresh graders grade every question from the start (v6.2; bc.BV_ROLES_GRADE); the majority — or the
         median of three different bands — decides; a third grader is re-asked only when its result is missing and
         the two others disagree. A disagreement between graders is never a reason to rewrite.
    BV-4 At most ONE rewrite per question (bc.C_WRITE_ATTEMPTS = 2), only when the majority names another band,
         the recipe fails at the slot, or the key is disputed (author + 2 blind solvers not unanimous, or a
         decisive assumption). The rewrite carries the graders' reasons. After it the question is delivered at
         the band it measured (bc.bv_set_label 'measured_majority'), one AMBER line per question
         (difficulty_state.bv_disclosed; DeliveryFooter §LADDER-BV). Difficulty never blocks delivery.
    BV-5 Final Assembly NEVER re-authors a question for difficulty: S13-2G phase 3 keeps every LB2 label
         (measured_exact / measured_majority) and S13-2L opens no difficulty chain on a settled question
         (bc.bv_settled). Final Assembly repairs only correctness: a key still disputed after the rewrite, a
         reviewer's key disagreement, an unproven figure.
    BV-6 Room is never a stop: a worker short of room saves its state and reports ROTATE; a fresh worker
         continues the same message (Framework_MockTestOrchestrate O2-3). "WORKER-CAPACITY" is not a stop.
    BV-7 (v6.2) The anchors the author and the reviewers compare against are REAL past questions of this exam with
         their content (bc.bv_anchors over EXAM_RULER['anchor_records']; same subtopic first). With no blind grades
         yet the ruler uses the bands PYQExplain measured — the same scale the blueprint's difficulty schedule was
         built from — and the paper discloses it (AMBER "Difficulty anchors: ..."); blind grades replace it as soon
         as they exist. A reviewer job is never written with an empty anchor set while the exam has past records.
    BV-8 (v6.2) A planned handover (GRADE_REQUEST, ROTATE) refreshes the CHECKPOINT first
         (`bootstrap.py --checkpoint make`, Framework_MockTestOrchestrate O3-3): the worker that continues keeps
         every written question and grade. Only a worker that FAILED retention has its work since the last make
         undone.
    BV-9 (v6.2) Speed: ONE round of at most 3 fresh reviewers per batch (each solves, grades and reads the figures
         of every question; started together, Orchestrate O2-3), a second round only for rewritten questions.
    BV-10 (v6.3 — GAP-2026-11-13-DIFFICULTY-RUBRIC) ONE RULER FOR PAST AND NEW QUESTIONS. Every past record of an
         exam was banded by bc.difficulty_score (rule r2) from its counts — class facets, inferential steps,
         distinct principles, speed hack, polarity, qtype (measured on CSIR NET Chemical Sciences: 358 of 358 bands
         reproduced exactly). A new question is measured the SAME way: each fresh reviewer lists the moves and
         the principles of its own solution under the counting rules PYQExplain counted with
         (bc.br_counting_rules — INFERENTIAL_STEP_RULE verbatim), and its grade is bc.br_band of those counts;
         the batch band is the majority / median of the three. The author writes to the slot band's measured
         profile from the exam's own past questions (bc.br_target: subtopic -> topic -> section -> exam, at least
         bc.BR_RECIPE_MIN records; else the rubric's score range) and counts its own solution the same way. On an
         exam whose labels are not three bands the rubric does not apply: the judged band stands, disclosed
         (AMBER "Difficulty judged, not counted"). Exam-agnostic; no value is set per exam.
    BV-11 (v6.3) No reviewer is never a stop: a question with no fresh result after bc.BV_MAX_ROUNDS rounds stays
         unlabelled in its batch (STEP A2 DONE lists it) and S13-2L measures it at Final Assembly.
    BV-12 (v6.3 — GAP-2026-11-13-RUN-NOT-READ) The session-start code (§3, S0-OP) and the helper libraries of
         §6-§11 are RUN from this verified file by `bootstrap.py --session-start`, not read (S1-0R PYTHON SESSION);
         every block runs in one namespace per paper kept on disk.
  A paper begun under an earlier release keeps its recorded state; S0-BV applies to every batch written from
  this release on (S4-12 migration).

## S1-0 — SESSION CLASS AND READ SET (v5.63 — decide at STEP 0, before any spec read)

```
Framework_PYQCore EC-P42; the Framework_MockTestAnalyse §S8-0b architecture and the
Framework_MockTestExplain S0-3 precedent (v1.39.0), applied to Step 7.

THE AXIS IS FINAL vs NON-FINAL — never fresh vs resume. Every batch session runs the
same S3 loads, the same S4 batch law, the same per-question S6/S7/S8/S10 machinery,
the same gates and the same S4-7 per-batch delivery (with its S13-9A footer); what
decides which sections it REACHES is whether it will close the mock.

  NON-FINAL  the batch this session will deliver is NOT the last of the frozen batch
             plan (S3-16 / S4-2; batch_state.json batch_plan). Final Assembly cannot
             run here.
             READ: everything EXCEPT the Final-Assembly family — S13-1 through S13-9
             (trigger, gate sweep, concept audit, registry update S13-4/4b/4c,
             S13-REGCHECK, S13-QINDEX, integrity, closed set, pre-delivery checklist,
             the single present_files, handoff) — and the close-out pair S17-1 (DoD)
             and S17-2 (downstream handoff to Step 9). S13-9A (the post-delivery
             footer) is PER-DELIVERY LAW — F1 after every non-final batch — and is
             ALWAYS read, as are all S4 sections and every gate.
  FINAL      the batch this session will deliver IS the last of the plan
             (batch_plan[current].is_final, or remaining batches <= 1), OR the plan
             is not yet known (fresh mock before S3-16 builds batch_state.json), OR
             the trigger is a Final-Assembly re-run of a completed mock.
             READ EVERYTHING. NO EXCEPTION.
             Unknown -> FINAL: reading too much costs context; reading too little can
             let a reduced read reach the Final-Assembly writers.

ESCALATION IS MANDATORY AND ONE-WAY. A session that begins NON-FINAL and discovers
mid-run that it will close the mock (a batch plan shrunk by packing, a resumed run
whose remaining batches all fit this session) MUST read S13-1..S13-9, S13-REGCHECK,
S13-QINDEX, S13-4b/4c, S17-1 and S17-2 BEFORE S4-9 hands over to Final Assembly.
FINAL never downgrades.

Line ranges are GENERATED into SPEC_SECTIONS.json from this file's own headers and
hash-tracked in MANIFEST.json — never hand-maintained here. Read the spec ONLY as S1-0R
says (`bootstrap.py --trigger ... --read K`; never a sed range above 300 lines, never the
view tool). `bootstrap.py --trigger MockCreate`
(or TestCreate) prints the class, both read budgets and the skipped sections; pass
`--progress [ExamCode]_M[N]_batch_state.json` so the class is decided from the frozen
plan rather than defaulting.

WHAT THIS DOES NOT CHANGE. Not one byte of any artefact: the same questions, the same
gates, the same batch deliveries, the same Final Assembly. It moves the CLOSING
sections off the per-batch execution path — it does not shrink, soften or delete them.
```

## S1-0R — READ METHOD, READ-RETENTION AND RUN MODE (v5.93 — binding)

GAP-2026-11-06-STEP7-SPEC-READ-CAPACITY, owner decision OD-2026-11-06. Measured (SESSION_BUDGET.json
`_measured`): a context that keeps growing is summarised by the platform without notice, after which
the session works from a summary of this spec, not its text; a tool result of about 40,000 characters
or more is diverted to a file the session cannot read back whole.

READ METHOD. Every spec on the Step 7 route is read only with
`python3 bootstrap.py --trigger <MockCreate|TestCreate> --progress /home/claude/[ExamCode]_M[N]_batch_state.json --read K`
for K = 1..N, one call each, in order (omit `--progress` until S3-16 writes that file). Each call
serves at most SESSION_BUDGET.json `read_chunk_max_lines` lines and `read_chunk_max_bytes` bytes.
bootstrap decides the S1-0 session class and read set; a NON-FINAL read includes this file's opening
lines (MANDATE 0, 1 and 2). The S1-0 escalation is read with `--read K --escalate`. Never read a spec
with a sed range above 300 lines; never open a tool-output file the harness diverted.

READ-RETENTION. Every read carries READ-ANCHOR codes. With every code given from memory,
`python3 bootstrap.py --retention "<nn>=<code> ..." --when <W>` must print `RETENTION: PASS` at four
points: (a) after the read; (b) before authoring a batch (S4-7 STEP A); (c) after the batch's gates
and report, before S4-7 STEP E records the batch as delivered; (d) before Final Assembly (S13). A
FAIL means the spec text is no longer in context: the spec is read again and the paper continues from
its state on disk; a batch whose check (c) failed is not delivered and is redone.
Framework_MockTestOrchestrate.md O3-3 is the exact procedure.

RUN MODE. MockCreate / TestCreate run ORCHESTRATED (Framework_MockTestOrchestrate.md, routed with this
step). In WORKER MODE the session executing this spec is a worker sub-agent: every present_files call
of this spec (S4-6, S4-7 STEP E, S13-8) is replaced by that spec's DELIVERY PROXY (O3-4), S13-2G
phase 2 by its review hand-over (O3-6), and S4-7 STEP A2's fresh jobs by its grading hand-over (O3-9, v6.1);
a worker short of room reports ROTATE (never a stop, S0-BV BV-6); everything else in this spec applies unchanged. In DIRECT
MODE (no sub-agent tool) this spec runs as written, with READ METHOD and READ-RETENTION.

PYTHON SESSION (v6.3 — GAP-2026-11-13-RUN-NOT-READ). Every python block of this spec runs in ONE namespace per
paper, kept on disk by `bootstrap.py` (PYTHON SESSION) (/home/claude/[ExamCode]_M[N]_session_ns.pkl — a WORK FILE, so the Orchestrate
O3-3 CHECKPOINT carries it):
  * SESSION START (S3, at the start of EVERY session — a fresh worker, a resume, a handover):
    `python3 bootstrap.py --session-start --exam <ExamCode> --paper <N> [--level <mock|subject|topic>]
    [--subject "<scope subject>"] [--topic "<scope topic>"] [--resume] [--grader-model <model id>]`
    (the options are the trigger's, S3-2). It runs, in file order, EVERY block whose first line is
    `# ENGINE-RUN` — all of §3 (and the S0-OP blocks inside S3-2) and the helper libraries of §6-§11. Those
    blocks are NOT in the read: the read shows their marker line and every rule around them; the code runs
    from the same verified file. Its output is the session start's output (every S3 print, every stop
    message, `FW-NS SESSION READY ...` at the end). A non-zero exit is that block's stop: act on its printed
    message exactly as if the block had run in the session.
  * EVERY OTHER BLOCK this spec tells you to run: write it (with your values filled in) to a file under
    /home/claude/fwrun/ and run `python3 bootstrap.py --run-block <file> --exam <ExamCode> --paper <N>`. Every name an
    earlier block or the session start bound (EXAM, bp, manifest, the ledgers, the plans, FONT_NAME, every
    helper function) is there; what you bind is kept for the next call and the next worker.
  * A name the session could not keep is printed on the next call (`FW-NS: not restored ...`); the block that
    needs it rebuilds it from the paper's files. Nothing is lost silently.

INPUT STAGING. The /mnt/project and /mnt/user-data/uploads paths used throughout this spec are
satisfied on every surface by `python3 bootstrap.py --stage-inputs` (SKILL Step 0, run in the user's
chat before any worker starts): chat attachments are copied into /mnt/user-data/uploads and the
project's documents are written into /mnt/project.

WHAT THIS DOES NOT CHANGE. No question-writing rule, gate, artefact, deliverable, end state or user
action: the same paper, the same two files, the same "continue".

## S1-1 — Pipeline position

  Step 5 (PYQExtract)  → produces [ExamCode]_section_rules.md, [ExamCode]_subtopic_manifest.json
                          and (v5.85) [ExamCode]_stimulus_profile.json — final synthesis, or
                          `PYQExtract --stimulus-profile` for an exam whose Step 5 already ran
  Step 6 (MockBlueprint) → produces [ExamCode]_blueprint.json,
                               [ExamCode]_registry.json (empty template),
                               [ExamCode]_EXPLAIN_LEARNINGS_v1.md,
                               [ExamCode]_mock_test_audit.py
  THIS STEP — Step 7 (MockCreate) → produces [ExamCode]_Mock[N]_Create.docx,
                               updated [ExamCode]_registry.json
  REGISTRY-HANDOFF-LAW (v5.73): every step that CHANGES registry.json DELIVERS it, badge
  "Replace in Project Files", in the same present_files call as its primary artefact —
  decided by pp.registry_changed (a fingerprint), never by prose. Steps 7 and 9 are the
  writers (v5.76: the retired repair steps no longer exist); Step 11 reads it.
  LAW_REGISTRY.json / mock_sync_audit MS-14.
  REGISTRY-SOURCE-LAW (v5.84): the registry this step READS may come from EITHER lane —
  attached to the trigger in chat, or Project Files. Resolved ONLY by pp.resolve_registry
  (S3-1): attachment wins when both are present, HARD STOP [HS:INPUT] only when both are absent,
  exam_code validated, fingerprint pinned for the run. LAW_REGISTRY.json / MS-20.
  Step 9 (MockExplain) → consumes outputs of this step (v5.36: directly — the former
                               Step 8 audit between them has been retired)

  PREREQUISITE: Step 0 AND Step 1 must both be complete.
  section_rules.md AND blueprint.json must both be in project knowledge.
  [ExamCode]_registry.json must be attached to the trigger OR in project knowledge
  (REGISTRY-SOURCE-LAW, S3-1).
  [ExamCode]_stimulus_profile.json (v5.85) must be attached OR in project knowledge
  before a NEW paper starts (S3-12b SAFETY LOCK). A paper already in progress does not
  need it — which is why S3-1 does not list it among the MANDATORY COPIES.

## S1-2 — Sources of truth (strict priority order)

  Priority 1: This spec (Framework_MockTestCreate.md)
  Priority 2: [ExamCode]_blueprint.json  — allocation, format, structure
  Priority 3: [ExamCode]_section_rules.md — subtopic rules, templates, patterns
  Priority 4: [ExamCode]_registry.json   — cross-mock dedup state (chat attachment OR
                                            Project Files — S3-1 resolver; attachment wins)

  CONFLICT RULE: blueprint.json ALWAYS wins over section_rules.md on
  format assignments, allocation counts, and structural decisions.

## S1-3 — Exam-agnostic guarantee

  Zero hardcoded exam values. Same spec runs for SSC CGL Tier 1,
  SSC CGL Tier 2, GATE, NEET, IBPS PO, CAT, UPSC CSAT, any exam
  with valid Step 0/1 outputs.

## S1-4 — Memory prohibition

  ABSOLUTE: Claude must NEVER use training memory to decide subtopic scope,
  content facts, PYQ patterns, formats, ciphers, or approaches.
  ALL decisions come from files read at session start.
  For fact-recall content: web-verify before using. DOCUMENTS WIN OVER MEMORY.

# ════════════════════════════════════════════════════════════════════════
# §2 — TRIGGER FORMAT & UNIVERSAL ABSOLUTE RULES
# ════════════════════════════════════════════════════════════════════════

## S2-1 — Trigger formats

  PRIMARY: TestCreate P[N] [--level <mock|subject|topic|subtopic>] [--scope <Subject[::Topic]>]
  STATUS:  TestCreate status
  RESUME:  TestCreate P[N] resume   (v3.0 — see S4-12)

  ALIAS (v5.28 — mock-only, working alias, unchanged behaviour):
    MockCreate M[N]          == TestCreate P[N] --level mock
    MockCreate status        == TestCreate status
    MockCreate M[N] resume   == TestCreate P[N] --level mock resume

  --level: selects WHICH blueprint tier to generate from when more than one
    [ExamCode]*_blueprint.json is present (§3 S3-1/S3-2, pp.pick_blueprint).
    mock            → [ExamCode]_blueprint.json (no --scope needed)
    subject         → requires --scope <Subject>
    topic           → requires --scope <Subject::Topic>
    subtopic        → requires --scope identifying the subtopic-scoped blueprint
    Omitted (Test* with no --level): single-active default — resolves automatically
    ONLY if exactly one blueprint file is present; otherwise pp.pick_blueprint raises
    PickError and Claude HARD STOPS [HS:INPUT] with its actionable message (does not guess).
    MockCreate M[N] always sets level='mock' implicitly — --level is never needed
    (and is ignored if given) on the Mock* alias.

  ExamCode: read from exam_config.json in project knowledge; must match blueprint + registry.
  [N]: integer ≥ 1 (P[N] for TestCreate, M[N] for the MockCreate alias — same meaning: the
       paper number within the selected blueprint's series). The binding check is
       MEMBERSHIP, not a range bound: some mocks[] entry must have mock == N (v5.54.1 —
       the old "must ≤ total_mocks/n_papers" wording was WRONG for an offset-resumed
       blueprint, where pp.apply_mock_offset relabels mocks[].mock to offset+1..offset+K
       but total_mocks stays the per-run count, so the prose gate would reject every
       valid resumed trigger; on a resumed SCOPED blueprint N is likewise the mocks[]
       ordinal, not the filename's series number). Identity is paper_id
       (= blueprint.mocks[N].paper_id): it must not already be in
       registry.papers_completed[] (legacy registries fall back to
       mocks_completed[] for the mock tier only).

## S2-2 — Universal Absolute Rules table

  R1:  Never copy PYQ verbatim or near-verbatim. ENFORCED BY bc.pyq_textual_verdict (8-shingle
       Jaccard against the PYQ index inside evaluate_attempt, S7-NEW-A) and its auditor twin
       audit_canonical.gate_pyqdist (A-PYQDIST).
  R2:  No question repeated across mocks (registry dedup L1-L18). ENFORCED BY
       audit_canonical.gate_dup (A-DUP: exact and near stems against EVERY registry
       stem_texts entry) at S4-7 STEP B and S13-4c.
  R3:  No picture and no ENTITY reused across any 2 questions of one paper. v5.90 — this
       rule had NO code behind it through v5.89 (dHash/MD5 were prose). ENFORCED BY:
       final_assembly.commit_registry G-MEDIAREUSE (bc.media_reuse_check over the
       fig_manifest image hashes — a shared media part REFUSES the commit with
       "LADDER-REPAIR R2 G-MEDIAREUSE"; linked sets exempt) and bc.EntityLedger
       (G-ENTITYLEAK at S13-2F / A-ENTITYLEAK: a key entity of one item in another item's
       given / intermediate / key / distractor / figure-label role, two items sharing a
       given, a scaffold over its measured cap — identities re-perceived, isotope-stripped;
       reagents, <= 3-heavy-atom species, standard values and the exam's measured common
       entities stoplisted; text entities WARN when the exam's own PYQs leak them, R3.8).
  R4:  Every question has exactly 4 DISTINCT options (unless options_count≠4). v5.90 —
       DISTINCT means distinct IDENTITY under the content kind's identity_fn
       (figure_types.QUALITY_ROWS -> bc.option_identity): two differently drawn pictures of
       ONE molecule are ONE option. ENFORCED BY: corpus_io.assert_option_identities at
       render (native_option_set raises OptionIdentityError "LADDER-REPAIR R2o
       G-OPTDISTINCT" before any pixel), figural_core.render_option_set (same message), and
       A-OPTDISTINCT at S13-2F / S13-4c. dHash NEVER decides identity (bc.OPT_DHASH_WARN
       only routes a no-identity_fn pair to the reviewer).
       — v4.7 NAT EXEMPTION: a NAT question (answer_type=='numerical') has ZERO options.
         R4 does not apply to it; option-count is governed by G-NAT-NOOPT instead.
  R5:  No answer key, correct marker, or HINT anywhere in the paper. v5.90 — a hint is
       DEFINED (GAP-2026-11-03 G04): text in the stem or in a non-agent figure annotation
       that the item does not need to be well-posed and that (i) names a tested-concept
       lexicon term, (ii) names an entity the figure already draws, (iii) states an
       option-eliminating qualifier, or (iv) supplies data that decide the key without the
       tested skill. (i)-(ii) ENFORCED BY bc.stem_leak_check (G-STEMLEAK / A-STEMLEAK; the
       lexicon and the measured allowances come from the subtopic's QUALITY block, OD-3:
       allowed only where the cell's PYQ named_concept_rate >= bc.NAMED_RATE_ALLOW);
       (iii)-(iv) are the reviewer's (Framework_MockReview S2-2: leak_or_paraphrase, single_answer). Surface cues to the key —
       bc.item_longest_key / bc.item_middle_value_key (G-ITEMRULE / A-ITEMRULE, OD-7).
       — INCLUDES: no answer key page at end of docx
       — INCLUDES: no asterisk, no bold correct option, no "correct" annotation
       — DETECTION: scan docx for "Answer Key", "Answers:", "Key:", "Q\.\d+.*→.*[1-4]"
       — LADDER-REPAIR R1 [HS:LADDER] if found: do not deliver until removed.
  R6:  Match blueprint allocations exactly.
  R7:  Q1 through QN continuous, no gaps, monotonic in document order.
  R8:  No section headings inside the paper body.
       — BANNED (KEYWORD form): "SECTION: ...", "Section I:", "Part A:", any divider lines.
       — BANNED (SECTION-NAME form, v4.8): a standalone body paragraph that IS a declared
         section NAME (e.g. "Reasoning", "Technical", or any name from blueprint
         sections[].section_name for the exam being generated)
         — the realistic section-header shape, which the keyword list does not cover. A
         questions-only paper (Q.N-first) has no standalone non-Q/non-option paragraph, so any
         body line equal to a section name (blueprint sections[].section_name) is a leaked
         header. Detection is PROVENANCE-BASED (matched against this paper's own section names),
         never a generic word list — exam-agnostic.
       — LADDER-REPAIR R1 [HS:LADDER]. Detection: scan all body paragraphs (a header may sit before the first Q
         or between sections), before and during assembly. Independently re-verified by
         audit.py A-SECHDR.
  R8b: No title / info / scoring / cover / instruction block before Q.1 (v5.18).
       — The generated paper is questions-only at the DOCUMENT level (not merely per-block):
         the FIRST non-blank body paragraph of the docx MUST be the bold "Q.1" stem. No title
         ("... Mock Test [N] ..."), no "Total Questions / Maximum Marks / Time" line, no
         "Each question carries ... Negative marking ..." instruction, and no cover/preamble
         may precede Q.1.
       — CATEGORY-C values (marks_per_q, time_per_q_sec, negative_marking, options_count,
         total_questions) are STRUCTURED METADATA carried in section_rules.md / blueprint.json
         and the registry — they are NEVER rendered as printed paragraphs in the paper. A
         downstream platform may display them from that metadata; the .docx never prints them.
       — Blank separator paragraphs before Q.1 are NOT a violation (they carry no text); only
         a non-blank, non-Q.N, non-option paragraph before Q.1 is.
       — EXEMPTION (dormant, exam-agnostic): if — and only if — section_rules.md EXAM_STRUCTURE
         explicitly declares `paper_header_block` (a deliberate per-exam opt-in), a printed
         header matching that declaration is permitted and gate G-PREQ1 is dormant. No current
         section_rules.md declares it, so the ban is absolute for every present exam.
       — LADDER-REPAIR R1 [HS:LADDER]. Detection: scan every paragraph before the first "Q.<N>" stem, before and
         during assembly. Enforced by gate G-PREQ1; re-verified by audit.py
         A-HEADER (which strips the block, not merely validates it). Distinct from R8
         (section-name headers inside the body) and R9 (docx page header/footer region).
  R9:  No header, no footer (unless EXAM_STRUCTURE in section_rules.md says otherwise).
  R10: Option labels per exam — read option_label_format from exam_config.json
       or blueprint (S3-2). Default: "{i}.  {text}" (number, dot, two spaces).
       The configured format drives both generation (add_text_options) and gate
       G-OPTLABEL (OPTION_LABEL_RE built from the format at S3-2).
  R11: Wait for "continue" trigger before each batch. NEVER auto-advance. (= MANDATE 1)
  R12: No answer key sidecar or figural manifest in deliverable docx.
  R13: Every Q-stem bold. 4 option paragraphs follow. Blank separator after.
       — v4.7 NAT EXEMPTION: a NAT question (answer_type=='numerical') has ZERO option
         paragraphs — only the bold Q.<N> stem (carrying the nat_instruction per R14) and
         the blank separator. Enforced by G-NAT-NOOPT (no options) + G-NAT-INSTR (instruction).
  R14: Exactly one bold Q.<N> stem paragraph per question, and it MUST be the
       FIRST non-empty paragraph of the question's block (v3.7 Q.N-FIRST). No
       stimulus/table/chart/passage/preamble may precede "Q.<N>". For linked
       members the Q.<N> attaches to the shared context line (§9 SC-3). Enforced
       by gate G-QNUM-FIRST.
       — v4.7 NAT: for a NAT question the candidate-facing nat_instruction (blueprint
         nat_contract; e.g. "Enter your answer as a numerical value.") is appended INSIDE
         the bold Q.<N> stem paragraph (never a separate paragraph, never an option), exactly
         as the MSQ multi-select instruction is. Enforced by G-NAT-INSTR.
  R15: present_files FORBIDDEN until gate checks pass.
  R16: present_files MANDATORY immediately after gate checks pass (per batch).
  R17: Options grammatically and logically consistent with stem.
  R18: Every Q number within its section's q_range (blueprint.sections[]).
  R19: No 2+ consecutive questions from same subtopic. (v3.8 extension) Also:
       (a) no two questions sharing a CONCEPT_GROUP may be adjacent;
       (b) no contiguous run > 2 questions from the same PRESENTATION_FAMILY
           (a coarse surface-look grouping, e.g. "vocab_single_word_pick" =
           {antonym, synonym, spelling, homonym, one_word_substitution});
           where section composition makes a longer run unavoidable, maximise
           spread and never exceed run = 3;
       (c) a subtopic's N questions are DISTRIBUTED across its section, not
           clustered. Checked in the S4-11 manual checklist (G-CLUSTER item).
       Rationale: even presentation-varied questions read as repetitive when the
       same family is stacked back-to-back (M1 Q.77–Q.80 were four vocab-single-
       word questions in a row). Complements RULE C (which fixes look) with
       distribution (which fixes adjacency).
  R20: Print gate check results in chat after every batch, before present_files.
  R21: At least one statement/option must be TRUE in multi-statement Qs.
  R22: Output as .docx only — NEVER print questions in chat. (= MANDATE 0)
  R23: Final Assembly runs automatically after the last batch. (= MANDATE 1 exception)
  R24: FONT AND SIZE per exam — read from exam_config.json (keys: font_name,
       font_size_pt). Defaults: Calibri, 11. Arial BANNED (unless it IS the
       configured font). Apply the configured font/size uniformly:
       — Stems: configured font, configured size, bold.
       — Options: configured font, configured size, normal weight.
       — Verify: scan all runs; if run.font.name not in [configured_font, None]: fix.
  R-DELIVER (v5.36, HARD STOP [HS:INFRA]): Step 7 delivers EXACTLY the CLOSED SET at Final
       Assembly and NOTHING else. The set is the CLOSED set below (v5.73; v5.91 — exactly
       two files, STEP_CONTRACTS.json / STEP-CONTRACT-LAW):
         1. [ExamCode]_Mock[N]_Create.docx        — always (scoped slug for a scoped paper)
         2. [ExamCode]_registry.json              — always (Replace in Project Files)
       (v5.89's conditional third/fourth files — an amended blueprint, the repo auditor copy —
       are retired by owner decision D3 (a), 2026-11-04: informational footer lines only.)
       "EXACTLY" is the operative word in BOTH directions: nothing missing and
       nothing outside this set. The Tier-A audit dossier ([ExamCode]_M[N]_audit_dossier.json)
       is INTERNAL from v5.73 (operator decision 2026-08-26): S13-4b writes it to
       /home/claude and S13-4c reads it there; staged in outputs it is a LEAK
       (final_assembly.predelivery_checklist check 5). The set is DECIDED by code
       (fa.outputs_to_clear -> fa.predelivery_checklist -> fa.delivery_scope ->
       pp.handoff_set), never by hand, so the v5.35/v5.36/v5.54.1
       count-drift class cannot recur. Producing a standalone answer-key file (any format:
       .docx/.pdf/.json/.txt) as a deliverable is forbidden with the same force
       as R5 (no answer key in the paper). Internal sidecars (answer_key.json,
       fig_manifest.json, batch_state.json, progress.json, audit_dossier.json) are NEVER delivered.
       The learner-facing answer key is a Step-4 (MockExplain) artefact, not
       a Step-7 one. Enforced by S13-6, S13-7, and gate G-DELIVERY-SET.
  R-LINKED (v3.6, LADDER-REPAIR R1 [HS:LADDER]): Every question must be SELF-CONTAINED for
       one-question-at-a-time online rendering. For any linked-stimulus group
       (CLASS 4 — RC passage→Qs, DI table/graph→Qs, Cloze passage→blanks, puzzle
       set→Qs, or any shared dataset backing ≥2 questions), the shared stimulus
       MUST be physically present inside EACH member question's own block — not
       placed once as a loose lead-in before the first question.
       — DEFAULT = MODEL A (stimulus-per-member): duplicate the full stimulus
         (passage text / Word-table object / chart image / cloze paragraph) into
         every member question's stem block, so each question is answerable in
         total isolation.
       — MODEL B (engine-native passage-group) is permitted ONLY when the target
         test-series platform is CONFIRMED (S3) to support a comprehension/passage
         container that pins one stimulus across a tagged set. If unconfirmed,
         use Model A. Never rely on a loose lead-in paragraph (that is neither).
       — A "lead-in only" layout (stimulus before Q1 of the group, absent from
         Q2..Qn) is BANNED with the same force as R5/R8.
       — Q.N-FIRST (v3.7, LADDER-REPAIR R1 [HS:LADDER]): every question block — single OR linked —
         MUST OPEN with its "Q.<N>" paragraph. No paragraph, table, chart, or
         passage may precede the Q-number. For a linked group the Q-number
         attaches to the SHARED CONTEXT / INSTRUCTION line, e.g.
         "Q.74  Study the following table and answer the question. ...". The
         stimulus follows the Q.N line; the specific ask is a separate bold,
         non-numbered paragraph after the stimulus. Stimulus-first / preamble-
         first layouts are BANNED. Reference: §9 SC-3 ordered block.
       Enforced by §9 (SC-1..SC-7), S10-LINKED helper, R14, and gates
       G-STIMULUS-ORPHAN + G-QNUM-FIRST.
       — v4.7 LINKED-NAT (ND11): a linked/DI group MAY contain members whose subtopic is
         answer_type=='numerical' (a shared table/chart followed by numerical-answer
         questions — common in GATE/CAT DI). A NAT member is a 0-option member: the SHARED
         stimulus is still embedded per member (Model A self-containment, SC-1..SC-7 and
         G-STIMULUS-ORPHAN unchanged), the Q.N-first ordering holds, and the member simply
         emits no option paragraphs (R13 NAT exemption) and carries the nat_instruction
         (R14). Stimulus embedding, atomic-group batching, and self-containment are
         orthogonal to whether a member has options — so NAT members compose without any
         change to the linked machinery beyond permitting the 0-option member.
  R-FIGURAL (v4.0, LADDER-REPAIR R1 [HS:LADDER]): Every figural MCQ must be DECOMPOSED, not a
       composite panel. It is rendered as the problem/series figure(s) as their
       OWN image(s) PLUS one SEPARATE image per option, bound 1:1 to its "i."
       label and stacked SINGLE-COLUMN (exactly one option image per line — never
       two options on a line, never a table row of option images). A single image
       containing the problem and all options baked together is BANNED with the
       same force as R5/R-LINKED: the online engine renders one option region per
       screen and cannot slice a baked panel, and a fused panel decouples each
       figure from its answer label. No stem, caption, instruction, or option
       number may be baked into any raster — those are document text; only
       INTRINSIC figure annotations (mirror-line endpoints M/N, geometry vertices,
       axis labels) belong inside the image. Reference lines/axes are DRAWN as real
       geometry, never floating letters. Image quality is fixed by framework
       constants (FIGURAL_DPI=300, uniform option canvas, lossless PNG, vector-first
       geometry, FIG_MIN_STROKE_PT). The stem stays Q.N-first document text (R14).
       Enforced by §10-S10-7 (image-quality contract) + §10-S10-8
       (add_figural_question) + view-tool verification + gate G-FIGURAL-COMPOSITE.
       — v4.7 FIGURAL-NAT VARIANT (ND10): when a figural question's subtopic is
         answer_type=='numerical' (e.g. a GATE geometry/mensuration diagram with a typed
         answer), it has a PROBLEM image (or series images) but ZERO option images — there
         are no options to decompose. The "one image per option / ≥ n_options+1 images / 1:1
         option-label binding" requirement DOES NOT APPLY; G-FIGURAL-COMPOSITE must skip its
         per-option-image arm for a numerical figural question and require only that the
         problem image(s) obey the single-column / no-composite / 300-DPI / named-image
         (q{N}_problem[_k]) discipline. The answer obeys the NAT value+tolerance contract
         (R-ANSWER numerical branch) and the stem carries the nat_instruction (R14). Without
         this variant a valid figural-NAT would be hard-stopped for "missing option images".
  R-UNDERLINE (v4.1, LADDER-REPAIR R1 [HS:LADDER]): Every question that asks about an UNDERLINED
       span — vocabulary/grammar items presented as 'sentence_embedded_underlined'
       (antonym/synonym/of-the-underlined-word), sentence-improvement ("improve the
       underlined part of the sentence"), error-spotting on an underlined segment,
       or any stem that refers to "the underlined word/part/segment/phrase" — MUST
       render that target span as a GENUINE underlined run (python-docx
       run.underline = True; XML <w:u>) sitting inside the sentence at its natural
       position. BANNED with the same force as R5: emitting the target as a
       plain-text parenthetical annotation appended to the stem — "(underlined: X)",
       "(underline: X)", "(underlined word: X)" — or appending the target in any
       bracketed/quoted note in lieu of underlining the in-sentence span. Underlines
       are real character formatting, NEVER drawn with underscore characters
       ("____") or markdown. The instruction text itself ("improve the underlined
       part…") is NOT underlined; only the target span is. Enforced by §10-S10-2
       (add_stem_with_underline + UNDERLINE_TRIGGER), the tightened render-
       consistency contract (§7 G4 stem_matches_format), and gate G-UNDERLINE.
  R-OPTREF (v4.2, LADDER-REPAIR R2 [HS:LADDER]): A stem may not REFERENCE a terminal/escape option
       that the option set does not actually contain, and the instruction's promised
       option-structure must match the rendered options. Specifically:
       — If the stem instructs the candidate to choose a terminal escape option in
         the "no positive answer" case — e.g. "if there is no error, (select/mark)
         the last option", "select 'No improvement'", "None of these / None of the
         above", "All of the above", "Both … and …", "Neither … nor …" — then that
         option MUST be PRESENT in the option set, at the position the instruction
         names (a "last option" reference ⇒ it is option N).
       — A "pick the segment/part that contains the error" layout (every option is a
         sentence SEGMENT) may NOT carry a "no error → last option" escape
         instruction unless a real "No error" option is appended; conversely a
         "No error"-escape instruction REQUIRES the escape option and the matching
         3-segment (N−1) split. The instruction template and the option structure
         must be the SAME template.
       This is EXAM-AGNOSTIC: the permitted escape/terminal tokens and per-section
       option structures are read from section_rules.md (none_of_above_permitted at
       S3-12, wrong_option_structure / fixed_set at S3-13). The framework enforces
       coherence; it hardcodes no exam's wording. Carrier-sentence stems
       (error-spotting, sentence-improvement, fill-in-sentence) must also place the
       instruction and the sentence on SEPARATE paragraphs (§10-S10-2, generalised
       in v4.2 — no run-on). Enforced by §10-S10-2 layout + gate G-OPTREF.
  R-SUBPART (v5.79, LADDER-REPAIR R1 [HS:LADDER] at authoring): A stem that carries TWO OR MORE
       enumerated sub-parts (reagent/procedure steps, test lists, statement sets,
       sentences-to-arrange, assertion–reason pairs — any labelled enumeration
       that is neither the option set nor a MATCH list) renders ONE bold
       continuation paragraph PER sub-part — never an inline run-on stem.
       Sub-part labels obey the §10 S10-2b LABEL LAW: never a Q-number shape,
       never THIS exam's own option-label scheme in ANY spacing, never a bare
       digit-dot/digit-paren label under any exam. EXAM-AGNOSTIC by construction:
       the collision test renders this exam's own labels via _option_label /
       OPTION_LABEL_FMT — nothing hardcoded. Enforced by add_stem_multipart
       (raises at authoring, §10 S10-3), layout §10 S10-2b, and checklist item
       G-STEM-SUBPART (S4-11). MATCH lists remain REAL tables (G-MATCH-TABLE);
       MSQ/NAT instructions remain inside the Q.N line (G-MSQ-INSTR/G-NAT-INSTR).
  R-ANSWER (v4.5, LADDER-REPAIR R2 [HS:LADDER] at generation — generalises v4.2 R-UNIQUE; single source
       of truth; the former audit-side mirror of this rule is retired — this is now the
       sole statement of it anywhere). The contract is parameterised by the
       subtopic's answer_cardinality (blueprint subtopic_list; default 'single'):

     ── answer_cardinality == 'single' (the v4.2 R-UNIQUE rule, UNCHANGED) ──
       Every question must have EXACTLY ONE
       defensible correct option; the other three must be indefensible under ANY
       reasonable reading. A question where a SECOND option is also defensible is a
       defect even though a "key" exists. This cannot be reduced to a regex — it is
       a generation-time reasoning check (the generator already knows the intended
       key and must confirm no other option survives a fair reading). Illustrative
       CLASSES of the failure (examples, NOT a hardcoded list — applies to every
       exam): (a) kinship/relational stems where an unqualified relation
       ("grandmother/grandfather/uncle/aunt") combined with "only son/daughter"
       admits a maternal AND a paternal reading that map to two DIFFERENT listed
       options; (b) any item whose answer depends on a CONTESTED convention (e.g.
       tense treatment of a universal truth in reported speech) while BOTH convention
       outputs sit in the option set; (c) series/analogy stems where two distinct
       rules each yield a listed option. The remedy is always to DISAMBIGUATE the
       stem (qualify the relation, fix the convention via section_rules, constrain the
       rule) or remove the colliding option — never to "pick one and hope".

     ── answer_cardinality == 'multi' (MSQ; v4.5, active only when blueprint multi_present) ──
       The intended key is a SET S of correct option positions. The generation-time
       reasoning obligation INVERTS to a set contract — equally not a regex:
         • EVERY option in S must be defensible (clearly correct) under EVERY fair reading;
         • EVERY option NOT in S must be indefensible (clearly wrong) under ANY fair reading
           — the dangerous failure is a BORDERLINE out-set option that should arguably be
           in S (the MSQ analogue of the two-defensible-answers single-mode defect);
         • S is a NON-EMPTY PROPER subset of {1..options_count}: 1 ≤ |S| ≤ options_count−1
           (k=0 "empty" and k=n "all-correct" are LADDER-REPAIR R2 [HS:LADDER] defects by default);
         • when msq_k_mode == 'fixed', |S| == msq_k EXACTLY;
         • NEGATION composes: for a negated multi stem ("which are NOT correct"), S is the
           set of options satisfying the NEGATED predicate — derive S, then apply the rules
           above to S as derived.
       The remedy for an ambiguous out-set option is the same as single mode: DISAMBIGUATE
       the stem or move/remove the colliding option — never ship an arguable set.
       Escape options under multi obey R-MSQ-ESCAPE.

     ── answer_type == 'numerical' (NAT; v4.7, active only when blueprint nat_present) ──
       This branch is selected by the ORTHOGONAL answer_type axis and SUPERSEDES the
       option-based reasoning above: a NAT question has NO options at all, so there is no
       in-set/out-set to adjudicate. The intended answer is a single typed VALUE, and the
       generation-time obligation is WELL-POSEDNESS:
         • the stem must determine the value UNIQUELY — exactly one numerical answer follows
           from a fair reading (the NAT analogue of "exactly one defensible option"); a stem
           admitting two defensible values (ambiguous rounding convention, under-specified
           figure, missing unit) is a LADDER-REPAIR R2 [HS:LADDER] defect — DISAMBIGUATE the stem;
         • the value's form must match nat_answer_type (blueprint nat_contract): 'integer' ⇒
           an exact integer, no decimals; 'real' ⇒ a decimal carried to the exam's stated
           precision;
         • tolerance: 'integer' ⇒ exact match (no band); 'real' ⇒ the accepted band is
           [value − nat_tolerance, value + nat_tolerance] (or the % form), recorded as
           ca_range = (lo, hi) with lo ≤ hi — this is the SAME ca_range Step 4 renders and
           audit.py A-NAT-ANSWER re-derives. A '0' tolerance means exact-to-displayed-precision;
         • a zero, negative, or fractional value is valid — the value is stored as data, never
           tested for truthiness, and a fractional value renders as OMML (§11), never inline;
         • the value MUST NOT appear as a GIVEN anywhere else in the paper (no cross-question
           leak) — the same self-containment R-ANSWER demands of any key, here keyed on the
           derived VALUE (enforced by G-NAT-ANSWER + the value-leak arm of S11-4).
         • v5.25 — PORTAL GRADING VALUE (locked, DJ rules; see S7-NEW-C): the typed value above
           is the MATH answer, used for well-posedness/ca_range/OMML display. It is a SEPARATE
           concern from the exact string the delivery portal ingests to auto-grade the question
           — that string must derive from `derive_nat_grading()` (S7-NEW-C), never from ad-hoc
           formatting, and is stored alongside the math value in the sidecar (nat_grading_type,
           nat_grading_value), never inferred later by a downstream step.
       There are no distractors to make indefensible; correctness is the value + its band.

## S7-NEW-C — NAT portal grading value derivation (v5.25, locked DJ rules)

  MOTIVATION: the delivery portal auto-grades a NAT question by exact/tolerant string match
  against ONE field, and that field accepts ONLY the character set `0123456789.-` — no
  scientific notation, no units, no words, no en-dash, no parentheses, no spaces (confirmed
  against the portal's own answer-entry configuration screen). The math VALUE computed above
  (and its ca_range) is exam-content-correct but is NOT automatically portal-safe: a value that
  is legitimately tiny (e.g. a rate stated "in units of 10⁻⁹") or that carries a tolerance band
  must be TRANSFORMED into a portal-safe string before it ever reaches a sidecar, a docx, or an
  audit gate. This transformation is a PURE FUNCTION of (value, ca_range, stem_precision) — it
  is computed ONCE, here, at generation time, and carried forward verbatim by every downstream
  step (v5.36: nothing re-derives it downstream; Steps 9-11 render/pass it through, never reformat
  it). EXAM-AGNOSTIC — zero hardcoded exam values; the function reads only its three arguments.

  INPUTS:
    value          : the computed math answer (already expressed in whatever units the stem
                     states — a "units of 10⁻⁹" stem means `value` here is the SMALL number,
                     e.g. 3, not the raw 3×10⁻⁹; that pre-scaling is the author's job when
                     computing `value` in the first place, upstream of this function).
    ca_range       : the SAME (lo, hi) tuple computed above for R-ANSWER/G-NAT-ANSWER, or None.
    stem_precision : int N if the stem contains an explicit rounding instruction ("round off
                     to N decimal places" / "correct to N decimal places"), else None.

  DECISION TREE (zero-halt except the one explicit NOT-SUPPORTED gate below):
  ```python
  from decimal import Decimal, ROUND_HALF_UP
  import re

  _NAT_GRADE_CHARSET = frozenset('0123456789.-')
  _NAT_INTEGRAL_EPS = Decimal('1e-9')   # float-arithmetic-residue guard, NOT a domain judgement

  def _fmt_portal_number(value, precision=None):
      """One bound/value -> a portal-safe string. precision=None -> minimal
      representation (bare integer if integral, else unpadded decimal — this
      is what makes 'Decimal' point-optional / 'decimal-capable' per the
      portal's numeric-tolerance matching, no forced trailing zeros).
      precision=int N -> exactly N digits after the point, zero-padded,
      ROUND_HALF_UP (locked rule — never banker's rounding, never truncation)."""
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
      if re.fullmatch(r'-0(\.0+)?', s):        # never emit negative zero
          s = s.lstrip('-')
      return s

  def _fmt_portal_range(lo, hi, precision=None):
      lo_s = _fmt_portal_number(lo, precision)
      hi_s = _fmt_portal_number(hi, precision)
      if lo_s.startswith('-') or hi_s.startswith('-'):
          # LOCKED, NOT an inferred default: '-' is both the range delimiter and a
          # possible bound sign, so a negative-bounded range is structurally
          # ambiguous with no confirmed portal-side escape convention. Escalate
          # rather than guess — same halt-on-genuine-ambiguity posture as
          # G-NAT-ANSWER/A-NAT-ANSWER elsewhere in this spec.
          raise ValueError(
              f"NAT range has a negative bound (lo={lo_s!r}, hi={hi_s!r}) — NOT "
              f"SUPPORTED. Rework the question so both bounds are non-negative, "
              f"or get an explicit portal-side range convention confirmed before "
              f"this gate is ever lifted.")
      if Decimal(lo_s) > Decimal(hi_s):
          raise ValueError(f"NAT range lo>hi ({lo_s!r} > {hi_s!r})")
      return f'{lo_s}-{hi_s}'

  def derive_nat_grading(value, ca_range=None, stem_precision=None):
      """Returns (grading_type, grading_value). grading_type is one of
      'positive_integer'|'integer'|'decimal'|'decimal_fixed'|'range'.
      grading_value is the final 0-9.- only string, ready for the sidecar,
      the docx Correct-Answer line, and the portal upload — identical string
      used in all three, never reformatted downstream."""
      # 1. Stem-stated rounding instruction wins outright (overrides both the
      #    range/no-range and the integral/non-integral branches below).
      if stem_precision is not None:
          if ca_range is not None:
              lo, hi = ca_range
              return ('range', _fmt_portal_range(lo, hi, precision=stem_precision))
          return ('decimal_fixed', _fmt_portal_number(value, precision=stem_precision))
      # 2. No stated precision, but a tolerance band exists -> Range type.
      #    (nat_tolerance != 0 for this question, i.e. ca_range is not None,
      #    is the ONLY signal for Range typing — no separate judgement call.)
      if ca_range is not None:
          lo, hi = ca_range
          return ('range', _fmt_portal_range(lo, hi, precision=None))
      # 3. Single exact value: Positive Integer / Integer / Decimal by sign
      #    and integrality, epsilon-tolerant against float noise.
      d = Decimal(str(value))
      if abs(d - d.to_integral_value()) <= _NAT_INTEGRAL_EPS:
          v_int = int(d.to_integral_value())
          return (('positive_integer', str(v_int)) if v_int >= 0
                  else ('integer', str(v_int)))
      return ('decimal', _fmt_portal_number(value, precision=None))
  ```

  CALL SITE (v5.25): computed IMMEDIATELY after the math value + ca_range are finalized for a
  NAT question, BEFORE `write_q_to_sidecar` is called — the two new sidecar fields
  (`nat_grading_type`, `nat_grading_value`) are populated FROM this function's output, never
  independently derived by the sidecar writer itself (single source of truth; see S7-NEW-A).
  A `ValueError` from `derive_nat_grading` (the NOT-SUPPORTED negative-range case) is a
  LADDER-REPAIR R2 [HS:LADDER] defect on the QUESTION, not a formatting bug — DISAMBIGUATE/rework the stem's
  numbers so both bounds are non-negative, exactly as any other well-posedness failure in this
  section is handled; never suppress or work around it.

  Enforced by gate G-NAT-GRADE (S12-NEW-29) at generation time and independently re-derived by
  audit.py's A-NAT-GRADE.

       Enforced by §7 CHECK 3 verify_answer (persisted as answer_verified in the
       S7-NEW-A sidecar) and gates G-UNIQUE (record backstop, both modes) + G-MSQ-SET /
       G-MSQ-CARD (multi only) + G-NAT-NOOPT / G-NAT-ANSWER / G-NAT-INSTR (numerical only).
  R-MSQ-ESCAPE (v4.5, applies only when answer_cardinality == 'multi'): "All of the above" is
       a self-contradictory option under multi-select (it cannot coexist with individually
       selectable correct options) and is REJECTED unless section_rules sets
       msq_allow_aota=true (default false), in which case the gate stands down. "None of
       these" is permitted only as an ordinary selectable option (it is the sole member of
       S when correct, i.e. |S|=1 — never an empty set). Enforced inside G-MSQ-SET.
  R-MATH-OMML (v4.3, LADDER-REPAIR R1 [HS:LADDER]): Every algebraic/symbolic expression that
       contains a STACKED FRACTION, an EXPONENT/SUPERSCRIPT, a RADICAL, or any
       built-up structure (per the §10-S10-4 decision tree rules 3-6) MUST render
       as native OMML (python-docx <m:oMath>) inline in the document text. Three
       forms are BANNED with the same force as R5:
       — a RASTER IMAGE of the expression (a <w:drawing> PNG/JPEG of "x + 1/x = 5",
         "x²+1/x²", a surd, a built-up fraction, etc.). The matplotlib/figural/
         image pipeline is for GEOMETRIC FIGURES ONLY (mensuration & coordinate
         diagrams, figural-reasoning panels); it may NEVER be handed an algebraic
         expression. This is the M1 Q.55 defect (two expressions shipped as 300-DPI
         matplotlib PNGs q55_e1/q55_e2 instead of OMML).
       — a SLASH/CARET ASCII fallback ("a/b" stacked fractions, "x^2") in the text
         stream (the long-standing G-FRAC ban).
       — RAW LaTeX (\frac, \sqrt) left unconverted.
       Single Unicode symbols (², ³, √n, ×, ≤, ≥, ±, π, °, θ) and unit labels
       (÷ is NEVER a fraction spelling — v5.47; subscripted symbols like k_B
       are built-up math, S10-4 rule 3a)
       (km/h, cm²) stay plain text/Unicode per the decision tree rules 1-2 — they
       are NOT built-up structures and do NOT require OMML. The executable home is
       §10-S10-4 (MATH_TRIGGER detector + render_mock_text ⟦MATH:⟧ funnel, with
       add_math_stem/emit_math_inline as the legacy segments API, +
       assert_not_math guard + the mock_math_residue_check post-build gate —
       v5.47; v5.70: its detected residue is G-MATH-RESIDUE, a per-batch FIXABLE
       FAIL); the figural boundary is enforced in §10-S10-7
       (render_figural_image calls assert_not_math). Enforced by gate
       G-MATH-RASTER (image name-contract) and the existing G-FRAC (slash text).
# All checks mandatory. Q1 FORBIDDEN until every check passes.

# ════════════════════════════════════════════════════════════════════════
# §3 — PRE-GENERATION CHECKS (all must pass before Q1)
# ════════════════════════════════════════════════════════════════════════

## S3-1 — File path management and copy protocol

  v6.3: §3 is RUN, not read — `python3 bootstrap.py --session-start ...` (S1-0R PYTHON SESSION) executes every
  `# ENGINE-RUN` block below in order; the rules and prose of every S3 section still bind and are in the read.

  /mnt/project/ (read-only) → /home/claude/ (working dir)
  /mnt/user-data/outputs/ (delivery)

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import shutil, os, json, re, glob
  from pathlib import Path
  EXAM = "[ExamCode]"  # from trigger
  RESUME = False       # from trigger: True when it ends in `resume` (S4-12) — v5.88

  # Ledgers — session state (RULE B / RULE C). Initialised EMPTY here at session
  # start, exactly as the §6-3 contract states; persisted to batch_state.json
  # after every batch (S4-8a) and REHYDRATED by S4-12 step 4b on resume. The
  # init is IDEMPOTENT (globals().get) so re-reading this fence after an S4-12
  # rehydration cannot wipe a resumed session's state. Previously these two
  # names were read in S4-8a/S4-12/§6-3 but bound NOWHERE
  # (GRANDFATHERED_MUST_FIX, fixed v5.62).
  mock_scenario_ledger     = globals().get('mock_scenario_ledger', set())
  mock_presentation_ledger = globals().get('mock_presentation_ledger', set())

  # MANDATORY COPIES (non-blueprint) — HARD STOP [HS:INPUT] if any missing.
  # (v5.85: [ExamCode]_stimulus_profile.json is deliberately NOT here — only a NEW paper
  # needs it; S3-12b's SAFETY LOCK enforces that, so an in-progress paper is unaffected.)
  required = [
      f'{EXAM}_section_rules.md',
      f'{EXAM}_subtopic_manifest.json',   # v3.4 — cross-step contract (REQUIRED)
  ]
  for f in required:
      src = f'/mnt/project/{f}'
      if not os.path.exists(src):
          raise SystemExit(f"HARD STOP [HS:INPUT]: {f} not found in project knowledge. "
                           f"Upload it to [{EXAM}] project Files, then retry.")
      shutil.copy(src, f'/home/claude/{f}')

  # REGISTRY (MANDATORY) — REGISTRY-SOURCE-LAW (v5.84, GAP-2026-09-14-REGISTRY-SOURCE).
  # Read from EITHER lane: the chat attachment (/mnt/user-data/uploads) OR Project Files
  # (/mnt/project). pp.resolve_registry is the ONE implementation Steps 7/9/11 share:
  # attachment wins when both exist (a difference is printed, never a stop); HARD STOP [HS:INPUT]
  # only when both are absent; exact filename + exam_code validated. NEVER open
  # /mnt/project/{EXAM}_registry.json directly here (MS-20). The working copy is
  # written ONCE per run: on a continue/resume turn the copy already in /home/claude is
  # the run's live state (S13-4 commits into it) and is never overwritten from a lane.
  import paper_pipeline as pp
  try:
      REG_SRC = pp.resolve_registry(EXAM, exists=os.path.exists,
                                    loader=lambda _p: json.load(open(_p, encoding='utf-8')))
  except pp.RegistrySourceError as _e:
      raise SystemExit(str(_e))
  for _line in REG_SRC['lines']:
      print(_line)
  # R4 — a run reads ONE registry. batch_state.registry_pin (S3-16) is what this run
  # started from; a later turn of THIS paper that resolves a DIFFERENT registry is a
  # HARD STOP [HS:INFRA]. The run's own working copy is never a swap (also_accept).
  _bs_pin_path = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _bs_state = (json.load(open(_bs_pin_path, encoding='utf-8'))
               if os.path.exists(_bs_pin_path) else None)
  _bs_pin = (_bs_state or {}).get('registry_pin')
  _reg_work = f'/home/claude/{EXAM}_registry.json'
  _own = ([pp.registry_fingerprint(json.load(open(_reg_work, encoding='utf-8')))]
          if _bs_state is not None and os.path.exists(_reg_work) else [])
  try:
      REG_PIN = pp.registry_source_check(_bs_pin, REG_SRC, also_accept=_own)
  except pp.RegistrySourceError as _e:
      raise SystemExit(str(_e))
  # WORKING COPY. A FRESH run of this paper (no batch_state for M{N}) takes the resolved
  # registry — overwriting whatever an EARLIER paper's run left in /home/claude, so the
  # lane the operator supplied is the one that generates. A continue/resume turn of the
  # SAME paper (batch_state exists) keeps its working copy: S13-4 commits into it.
  if _bs_state is None or not os.path.exists(_reg_work):
      shutil.copy(REG_SRC['path'], _reg_work)
  if _bs_state is not None and _bs_pin is None:      # pre-v5.84 batch_state mid-run: backfill
      _bs_state['registry_pin'] = REG_PIN
      json.dump(_bs_state, open(_bs_pin_path, 'w', encoding='utf-8'))

  # BLUEPRINT DISCOVERY (v5.28, paper_pipeline.py): copy EVERY [ExamCode]*_blueprint.json
  # present in project knowledge — the mock blueprint ([ExamCode]_blueprint.json) AND any
  # scoped blueprints ([ExamCode]_[SCOPETAG]_blueprint.json from ScopedBlueprint). §3 S3-2
  # (pp.pick_blueprint) decides which ONE of these this trigger actually generates from.
  blueprint_srcs = sorted(glob.glob(f'/mnt/project/{EXAM}*_blueprint.json'))
  if not blueprint_srcs:
      raise SystemExit(f"HARD STOP [HS:INPUT]: no {EXAM}*_blueprint.json found in project knowledge. "
                       f"Run MockBlueprint or ScopedBlueprint first, then retry.")
  BLUEPRINT_PATHS = []
  import hashlib as _hl_bp
  BP_PROJECT_SHA = {}          # {blueprint file name: sha256 of the PROJECT copy} — S3-16
  for src in blueprint_srcs:
      fname = os.path.basename(src)
      _dst_bp = f'/home/claude/{fname}'
      BP_PROJECT_SHA[fname] = _hl_bp.sha256(open(src, 'rb').read()).hexdigest()
      # v5.89 (GAP-2026-11-02 L3): a RESUMED run keeps the in-run blueprint it already
      # amended (S3-2D / R5 / allocation) — re-copying the project copy would silently
      # undo every amendment the earlier batches were generated and audited against.
      _keep_bp = False
      if os.path.exists(_dst_bp) and os.path.exists(f'/home/claude/{EXAM}_M{N}_batch_state.json'):
          try:
              _old_bp = json.load(open(_dst_bp, encoding='utf-8'))
              _old_bs = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json',
                                       encoding='utf-8'))
              # keep the amended copy ONLY while the project copy is the one this paper
              # started from — a newly uploaded / regenerated blueprint always wins
              _same_src = ('bp_project_sha' not in _old_bs     # state written before the key
                           or (_old_bs.get('bp_project_sha') or {}).get(fname)
                           == BP_PROJECT_SHA[fname])
              _keep_bp = _same_src and bool(_old_bp.get('difficulty_amendments')
                                            or _old_bp.get('allocation_amendments'))
          except Exception:
              _keep_bp = False
      if _keep_bp:
          print(f"S3-1: resumed run — keeping the AMENDED in-run {fname} (not re-copied).")
      else:
          shutil.copy(src, _dst_bp)
      BLUEPRINT_PATHS.append(_dst_bp)

  # OPTIONAL — audit script (Layer 2 guard — not required for Layer 1):
  audit_py = f'/mnt/project/{EXAM}_mock_test_audit.py'
  AUDIT_AVAILABLE = os.path.exists(audit_py)
  AUDITOR_FROM_REPO = False      # v5.89 P3 — True when this run audits with the repo copy
  if AUDIT_AVAILABLE:
      shutil.copy(audit_py, f'/home/claude/{EXAM}_mock_test_audit.py')
      # v5.85 (GAP-2026-09-21-LINKED-PLACEMENT) introduced the refresh; v5.86
      # (GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC) makes it a BYTE comparison. The
      # per-exam file is a VERBATIM copy of audit_canonical.py (Step 6 B3), so ANY
      # difference from the verified clone's copy means the project copy is stale. The
      # v5.85 test looked for one marker ('def gate_stimulus_blocks'), which every copy
      # made since 2026.09.21 carries — so an auditor fix shipped after that would never
      # reach a single project. Used for THIS run; the project file is left as is
      # (replace it with /tmp/fw/audit_canonical.py under the same name at your
      # convenience to silence this notice).
      # The verified clone is $FW (/tmp/fw); /tmp/fw_effective is its byte copy
      # (Step 0). Either is the same verified engine; the cwd copy is the last resort.
      _repo_audit = next((_c for _c in ('/tmp/fw/audit_canonical.py',
                                        '/tmp/fw_effective/audit_canonical.py',
                                        os.path.join(os.getcwd(), 'audit_canonical.py'))
                          if os.path.exists(_c)), None)
      if _repo_audit is None:
          print(f"NOTICE: no verified audit_canonical.py found beside this session "
                f"(expected /tmp/fw — Step 0 bootstrap); {EXAM}_mock_test_audit.py "
                f"from Project Files is used AS IS and may be stale.")
      elif open(audit_py, 'rb').read() != open(_repo_audit, 'rb').read():
          shutil.copy(_repo_audit, f'/home/claude/{EXAM}_mock_test_audit.py')
          AUDITOR_FROM_REPO = True          # v5.91 (D3 a): informational footer line only — never delivered
          print(f"AUDITOR REFRESHED: {EXAM}_mock_test_audit.py in Project Files "
                f"differs from the verified repo audit_canonical.py — this run audits "
                f"with the verified repo copy instead.")
  else:
      # v5.89 (GAP-2026-11-02 P3, owner decision O7): a project with NO auditor copy
      # used to skip the whole machine audit (S4-7 STEP B, S13-2F and S13-4c are all
      # gated on AUDIT_AVAILABLE). No paper ships without an audit: the verified repo
      # audit_canonical.py is copied in under the per-exam name and used. v5.91 (GAP-2026-11-04
      # D3 a): the copy is NOT delivered — every run audits with the verified repo engine, so
      # the project copy is never needed for correctness; one informational footer line.
      _repo_audit = next((_c for _c in ('/tmp/fw/audit_canonical.py',
                                        '/tmp/fw_effective/audit_canonical.py',
                                        os.path.join(os.getcwd(), 'audit_canonical.py'))
                          if os.path.exists(_c)), None)
      if _repo_audit is not None:
          shutil.copy(_repo_audit, f'/home/claude/{EXAM}_mock_test_audit.py')
          AUDIT_AVAILABLE = True
          AUDITOR_FROM_REPO = True
          print(f"AUDITOR FROM REPO: {EXAM}_mock_test_audit.py was not in Project Files; "
                f"this run audits with the verified repo audit_canonical.py (informational — "
                f"nothing to upload).")
      else:
          print(f"NOTE: {EXAM}_mock_test_audit.py not found in project and no verified "
                f"repo audit_canonical.py beside this session (Step 0 bootstrap). "
                f"Layer 1 batch enforcement (spec-level STOP) will be used. "
                f"Manual gate checklist (S4-11) will replace script gates.")

  # v5.89 (GAP-2026-11-02 P1) — READ RECEIPT. The spec bytes this run is held to are
  # printed into the run log (and repeated by the delivery footer): spec, exact line count,
  # sha256, END sentinel. Trimmed, summarised or partial working copies of a spec are
  # PROHIBITED; a run that worked from one records finding A-READ in its footer.
  import subprocess
  READ_RECEIPTS = []
  for _rr_dir in ('/tmp/fw_effective', '/tmp/fw'):          # first verified clone present
      if os.path.isfile(os.path.join(_rr_dir, 'bootstrap.py')):
          try:
              _rr = subprocess.run(['python3', 'bootstrap.py', '--trigger', 'MockCreate',
                                    '--receipt'], capture_output=True, text=True,
                                   cwd=_rr_dir, timeout=300)
              READ_RECEIPTS = [l for l in (_rr.stdout or '').splitlines()
                               if l.startswith('READ RECEIPT ')]
          except Exception as _rr_e:                       # disclosed, never fatal
              print(f"READ RECEIPT: bootstrap failed ({type(_rr_e).__name__})")
          break
  print('\n'.join(READ_RECEIPTS) or 'READ RECEIPT: unavailable (bootstrap not found beside '
                                     'this session) — disclosed in the footer')

  # v5.88 — ENGINE PATH FOR THE PER-EXAM AUDITOR (final review 2026-11-01, finding 13).
  # The per-exam copy lives in /home/claude and is run BY PATH; python puts the script's
  # own directory on sys.path, NEVER the cwd, so `cd /tmp/fw && python3 /home/claude/X.py`
  # could not import blueprint_core / figure_types and every engine-backed gate degraded
  # to WARN "NOT CHECKED" — which S13-4c now HARD STOP [HS:INFRA]s on. Every auditor subprocess in
  # this spec therefore runs with AUDIT_ENV: PYTHONPATH = the directory the verified
  # engines were imported from this session (exam-agnostic; never a hard-coded path).
  import importlib.util as _ilu
  _bc_spec = _ilu.find_spec('blueprint_core')
  if _bc_spec is None or not _bc_spec.origin:
      raise SystemExit("HARD STOP [HS:INFRA] (S3-9): blueprint_core is not importable from this session — "
                       "run from the verified clone (SKILL Step 0: cd /tmp/fw_effective).")
  ENGINE_ROOT = os.path.dirname(os.path.abspath(_bc_spec.origin))
  AUDIT_ENV = dict(os.environ, PYTHONPATH=ENGINE_ROOT + (os.pathsep + os.environ['PYTHONPATH']
                                                        if os.environ.get('PYTHONPATH') else ''))

  # OPTIONAL — figural manifest from a prior session of THIS paper (resume). v5.88: a
  # FRESH paper (no batch_state for M{N} in the session dir, no `resume` trigger) starts
  # with NO figure manifest and NO figure files: the manifest and every q<N>_*.png /
  # q<N>_*.figspec.json left by an earlier paper in this session are removed first, so a
  # stale record or sidecar can never be attributed to this paper (S13-4 commits on
  # existence since final_assembly v1.10; sidecars are matched by question number).
  _is_resume = RESUME or os.path.exists(f'/home/claude/{EXAM}_M{N}_batch_state.json')
  fig_src = f'/mnt/project/{EXAM}_fig_manifest.json'
  if _is_resume:
      if os.path.exists(fig_src) and not os.path.exists(f'/home/claude/{EXAM}_fig_manifest.json'):
          shutil.copy(fig_src, f'/home/claude/{EXAM}_fig_manifest.json')
  else:
      _stale = ([f'/home/claude/{EXAM}_fig_manifest.json'] if os.path.exists(f'/home/claude/{EXAM}_fig_manifest.json') else []) \
               + glob.glob('/home/claude/q*_*.figspec.json') + glob.glob('/home/claude/q*_*.png')
      for _f in _stale:
          os.remove(_f)
      if _stale or os.path.exists(fig_src):
          print(f"S3-1: fresh paper — {len(_stale)} figure file(s) from an earlier paper removed from the "
                f"session dir; a Project Files {EXAM}_fig_manifest.json is used only on a resume.")

  # OPTIONAL — EXPLAIN_LEARNINGS (v2.0 GAP-07 fix; v5.56 filename seam fix; v5.78
  # GAP-2026-08-28-STEP7-SUBJECT-LEARNINGS-SEAM). TWO resolutions, deliberately kept
  # separate: (a) the EXAM side keeps the exact v5.56 family glob
  # {EXAM}_EXPLAIN_LEARNINGS_v*.md, highest version wins — this glob structurally
  # excludes the {EXAM}_PYQ_EXPLAIN_LEARNINGS_v*.md and
  # {EXAM}_EXPLAIN_AUDIT_LEARNINGS_v*.md families (their basenames insert PYQ_/AUDIT_
  # before the family suffix), and a broader partition MUST NOT replace it: the
  # discovery helper's exam partition admits the PYQ family, whose basenames sort
  # AFTER the shared family (P > E), so a [-1] pick there would silently swap in the
  # wrong family's file on any project that has run both pipelines. (b) the SUBJECT
  # side is resolved by DISCOVERY — the same explain_engine.resolve_learnings_files
  # contract Steps 9 / PYQ-1 use (Explain-spec S24 contract: the single
  # non-{EXAM}-prefixed *_EXPLAIN_LEARNINGS_v*.md IS the subject library; no rename
  # is ever requested; >= 2 non-exam files → abstain + WARN, nothing subject-side
  # staged). Legacy-named file loads with a MIGRATION warning; never silently ignored.
  import glob
  import explain_engine as _ee
  learn_srcs = sorted(glob.glob(f'/mnt/project/{EXAM}_EXPLAIN_LEARNINGS_v*.md'))
  _ignored_ex, _subj_file, _amb = _ee.resolve_learnings_files('/mnt/project', EXAM)
  if _amb:
      print(f"S3-1 WARN — {_amb}")
  if learn_srcs:
      shutil.copy(learn_srcs[-1], f'/home/claude/{os.path.basename(learn_srcs[-1])}')
  if _subj_file:
      shutil.copy(_subj_file, f'/home/claude/{os.path.basename(_subj_file)}')
      print(f"S3-1 — subject learnings discovered (S24 contract, never renamed): "
            f"{os.path.basename(_subj_file)}")
  legacy_src = f'/mnt/project/{EXAM}_ExplainLearnings.md'
  if not learn_srcs and os.path.exists(legacy_src):
      shutil.copy(legacy_src, f'/home/claude/{EXAM}_ExplainLearnings.md')
      print(f'MIGRATION: {EXAM}_ExplainLearnings.md uses the legacy name — rename to '
            f'{EXAM}_EXPLAIN_LEARNINGS_v1.md so Step 9 loads it too (v5.56 seam fix).')
  ```

## S3-2 — Select and load the blueprint — read ALL fields (v2.0 GAP-02 fix; v5.28 pp.pick_blueprint)

  CRITICAL FIX: blueprint.json stores per-mock allocations under
  `mocks[i]['sections'][j]['subtopic_allocations']` — NOT under a
  top-level `allocations` key. The v1.0 spec had `mock_data['allocations']`
  which would raise KeyError on the actual file. This is fixed below.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import paper_pipeline as pp

  # LEVEL / SCOPE_SUBJECT / SCOPE_TOPIC come from the trigger (§2 S2-1):
  #   MockCreate M[N] alias        -> LEVEL='mock', SCOPE_SUBJECT=None, SCOPE_TOPIC=None
  #   TestCreate P[N] --level mock -> same as above
  #   TestCreate P[N] --level subject --scope Physics
  #                                 -> LEVEL='subject', SCOPE_SUBJECT='Physics', SCOPE_TOPIC=None
  #   TestCreate P[N] --level topic --scope Physics::Mechanics
  #                                 -> LEVEL='topic', SCOPE_SUBJECT='Physics', SCOPE_TOPIC='Mechanics'
  #   TestCreate P[N] (no --level)  -> LEVEL=None, SCOPE_SUBJECT=None, SCOPE_TOPIC=None
  #                                    (single-active default; requires exactly one blueprint file)

  blueprints = [json.load(open(p)) for p in BLUEPRINT_PATHS]
  try:
      bp = pp.pick_blueprint(blueprints, level=LEVEL, scope_subject=SCOPE_SUBJECT,
                              scope_topic=SCOPE_TOPIC)
  except pp.PickError as e:
      raise SystemExit(f"HARD STOP [HS:INPUT]: {e}")

  # v5.29 SAFETY CHECK: the {EXAM}*_blueprint.json glob (S3-1) is a PREFIX match — if a
  # different ExamCode's files were ever uploaded into this same project (e.g. "SSC_CGL"
  # vs "SSC_CGL_TIER1"), the glob could sweep in a blueprint that isn't this exam's. The
  # exact-filename match this replaced made that structurally impossible; the glob does
  # not, so it must be checked explicitly rather than trusted implicitly.
  if bp['exam_code'] != EXAM:
      raise SystemExit(
          f"HARD STOP [HS:INPUT]: selected blueprint's exam_code {bp['exam_code']!r} does not "
          f"match the trigger's ExamCode {EXAM!r}. A blueprint file from a different "
          f"ExamCode may have been picked up by the {EXAM}*_blueprint.json glob (S3-1) "
          f"— check this project for a similarly-prefixed ExamCode's files.")

  # v5.86 (GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC): the FILE the chosen blueprint came
  # from. Every auditor run of THIS paper (S4-7 STEP B, S13-4c) passes it as --blueprint:
  # [ExamCode]_blueprint.json for a mock, [ExamCode]_[SCOPETAG]_blueprint.json for a
  # scoped paper. Through v5.85 both invocations hard-coded the MOCK blueprint, so a
  # scoped paper was audited against the mock's size, sections and subtopics (and in a
  # project holding only scoped blueprints the auditor could not open the file).
  # pp.pick_blueprint returns one of the loaded objects itself, so identity finds it.
  BP_SRC_PATH = next(p for p, b in zip(BLUEPRINT_PATHS, blueprints) if b is bp)

  sr_text = open(f'/home/claude/{EXAM}_section_rules.md',
                 encoding='utf-8').read()

  exam_code         = bp['exam_code']
  exam_name         = bp['exam_name']
  blueprint_version = bp.get('blueprint_version', 'unknown')
  total_mocks       = bp['total_mocks']
  total_questions   = bp['total_questions']
  passage_present   = bp.get('passage_present', False)
  figural_present   = bp.get('figural_present', False)
  di_present        = bp.get('di_present', False)
  multi_present       = bp.get('multi_present', bp.get('msq_present', False))   # v4.6 (Phase-0 back-compat)
  nat_present         = bp.get('nat_present', False)          # v4.7 (default false ⇒ dormant)
  # ── S3-2a — PRESENCE-FLAG SELF-CORRECTION (v5.88, LAW F3.4, GAP-2026-11-01) ──────────
  # HS-15a IS SELF-CORRECTING. A blueprint flag describes
  # the paper; it never decides whether the paper's figures are recorded. ScopedBlueprint
  # < v1.11.0 inherited these flags from exam_config (default False), so a scoped paper with
  # 18 FIGURAL allocations ran with figural_present=False: S3-18's manifest and S4-5 CHECK 5
  # were skipped and S13-4 committed no figure record. The DERIVED truth wins in session;
  # the correction is printed; the declared flag is kept for the registry's paper_flags.
  import blueprint_core as _bc_flags
  _all_allocs = []
  for _mk in bp.get('mocks', []):
      for _s in _mk.get('sections', []):
          _all_allocs.extend(_s.get('subtopic_allocations', []))
  DECLARED_FLAGS = {'passage_present': passage_present, 'figural_present': figural_present,
                    'di_present': di_present}
  _derived = _bc_flags.derive_presence_flags(_all_allocs, subtopic_list=bp.get('subtopic_list', []),
                                             marking_scheme=bp.get('marking_scheme', []))
  for _f in ('passage_present', 'figural_present', 'di_present'):
      if _derived[_f] and not DECLARED_FLAGS[_f]:
          print(f"HS-15a (v5.88 self-correcting): blueprint {_f}=False but the allocation "
                f"carries {_f.split('_')[0].upper()} subtopics — using {_f}=True for this run. "
                f"Regenerate the blueprint with ScopedBlueprint v1.11.0+ / Blueprint v1.61.0+ "
                f"(the flag is derived there); the declared value is recorded in "
                f"registry.paper_flags at S13-4.")
  passage_present = passage_present or _derived['passage_present']
  figural_present = figural_present or _derived['figural_present']
  di_present      = di_present or _derived['di_present']
  sections          = bp['sections']      # [{name, q_range, total_qs, max_attempt}, ...]
  subtopic_list     = bp.get('subtopic_list', [])
  # v5.10: new fields from Step 6 v1.19 (Step 2a v2.5 exam_config contract).
  # marking_scheme: per-range scoring rules. Each entry has q_range, question_type,
  # correct_marks, negative_marks. Used for per-Q-position marks/type lookup.
  # level: academic level for question complexity calibration.
  # medium: authoritative exam language.
  bp_marking_scheme = bp.get('marking_scheme', [])
  bp_level          = bp.get('level', 'unknown')
  bp_medium         = bp.get('medium', 'unknown')

  # v5.10: Per-Q-position lookup helpers from marking_scheme.
  # These enable exact marks/type for any Q number (e.g., CSIR NET Q.72 → 4 marks, MCQ).
  # When marking_scheme is empty (legacy blueprint), helpers return safe defaults.
  def _marks_for_q(qnum):
      """Return correct_marks for a given Q number from marking_scheme."""
      for ms in bp_marking_scheme:
          if ms['q_range'][0] <= qnum <= ms['q_range'][1]:
              return ms['correct_marks']
      return 1  # default when marking_scheme absent or Q not in any range

  def _type_for_q(qnum):
      """Return question_type ('MCQ'/'MSQ'/'NAT') for a given Q number."""
      for ms in bp_marking_scheme:
          if ms['q_range'][0] <= qnum <= ms['q_range'][1]:
              return ms['question_type']
      return 'MCQ'  # default

  def _neg_for_q(qnum):
      """Return negative_marks for a given Q number."""
      for ms in bp_marking_scheme:
          if ms['q_range'][0] <= qnum <= ms['q_range'][1]:
              return ms['negative_marks']
      return 0  # default
  # v4.5: answer_cardinality lookup by subtopic_id (whole-subtopic mode). Used to set each
  # subtopic_data['answer_cardinality'] at S6-3 classify time and to compute msq_positions
  # for the answer budget. Defaults 'single' for any subtopic (legacy blueprint safe).
  # v4.6 Phase-0 back-compat: accept the pre-unification 'answer_mode' key too.
  answer_cardinality_by_id = {s.get('subtopic_id'): s.get('answer_cardinality',
                                                           s.get('answer_mode', 'single'))
                       for s in subtopic_list}
  # v4.7: answer_type lookup by subtopic_id (the NAT dispatch axis, orthogonal to
  # cardinality). Defaults 'option' for any subtopic ⇒ legacy/non-NAT blueprints are inert.
  answer_type_by_id = {s.get('subtopic_id'): s.get('answer_type', 'option')
                       for s in subtopic_list}

  # v5.X POSITION-BASED QUESTION TYPE (GAP-2026-07-22-001 §6 FIX):
  # For question-type sections (e.g. IIT JAM: Section A=MCQ, B=MSQ, C=NAT), the same
  # subtopic can appear in different sections with different question types. The per-subtopic
  # answer_cardinality/answer_type from section_rules is unreliable — it reflects PYQ
  # observation majority, not the section's authoritative type.
  # DUAL-MODE DISPATCH (mirrors Framework_MockDeliver.md v1.7 FIX):
  #   > 1 distinct question_type in marking_scheme → POSITION-BASED: answer_cardinality and
  #     answer_type derived from the Q position's marking_scheme entry via _type_for_q().
  #   0 or 1 distinct type → SUBTOPIC-BASED: unchanged, uses per-subtopic values from
  #     blueprint subtopic_list (current behavior). Also covers legacy blueprints with no
  #     marking_scheme (empty → 0 types → subtopic-based, byte-identical to pre-v5.X).
  _distinct_q_types = {ms.get('question_type') for ms in bp_marking_scheme
                       if ms.get('question_type')}
  _position_based_typing = len(_distinct_q_types) > 1

  def _resolve_answer_axes(qnum, subtopic_id):
      """Return (answer_cardinality, answer_type) for a question at position qnum.
      Position-based mode: derives from marking_scheme (authoritative for question-type
      sections). Subtopic-based mode: from blueprint subtopic_list (current behavior)."""
      if _position_based_typing:
          qt = _type_for_q(qnum)
          if qt == 'MSQ':
              return ('multi', 'option')
          elif qt == 'NAT':
              return ('single', 'numerical')
          else:  # MCQ or unknown
              return ('single', 'option')
      else:
          return (answer_cardinality_by_id.get(subtopic_id, 'single'),
                  answer_type_by_id.get(subtopic_id, 'option'))
  difficulty_schedule = bp.get('difficulty_schedule', [])
  # v5.14 THREE-AXIS: per-section format-distribution target (Step 6 v1.23 axis_schedule).
  # Absent-safe: pre-v1.23 blueprint → {} → the whole Axis-2 steering path stays inert and
  # generation behaves exactly as v5.13.
  axis_schedule = bp.get('axis_schedule', {})
  zero_pyq_rotation = bp.get('zero_pyq_rotation', {})

  # v5.6 EXAM-AGNOSTIC CONFIG — font, option labels, styling. PRIMARY source is
  # section_rules.md (matching audit.py's cat_c reads: font_family, option_label_format).
  # exam_config.json is an OPTIONAL OVERRIDE. Defaults match the SSC CGL reference
  # implementation. Zero hardcoded exam values — every constant has a config path.
  _ecfg_path = f'/home/claude/{EXAM}_exam_config.json'
  _ecfg = {}
  if os.path.exists(_ecfg_path):
      _ecfg = json.load(open(_ecfg_path, encoding='utf-8'))
  elif os.path.exists(f'/mnt/project/exam_config.json'):
      _ecfg = json.load(open(f'/mnt/project/exam_config.json', encoding='utf-8'))
  # v5.89 (GAP-2026-11-02 handshake): the exam's REAL config, as Step 2a delivers it
  # ([ExamCode]_exam_config.json in Project Files — S3-17c reads the same file). It feeds
  # ONLY the difficulty values this release needs (cycle_gap_days, sections), so Create's
  # cycle window and section plan equal ScopedBlueprint's. The legacy style overrides above
  # are deliberately left on their old lookup (switching them on would change every exam's
  # fonts/labels — a separate decision).
  _ecfg_exam = {}
  _ecfg_exam_path = f'/mnt/project/{EXAM}_exam_config.json'
  if os.path.exists(_ecfg_exam_path):
      try:
          _ecfg_exam = json.load(open(_ecfg_exam_path, encoding='utf-8')) or {}
      except (ValueError, OSError):
          _ecfg_exam = {}
      if not isinstance(_ecfg_exam, dict):
          _ecfg_exam = {}
  _ecfg_dp = {'sections': _ecfg_exam.get('sections', _ecfg.get('sections')),
              'cycle_gap_days': _ecfg_exam.get('cycle_gap_days', _ecfg.get('cycle_gap_days'))}

  def _sr_field(field, default):
      """Read a CATEGORY-A field from section_rules.md (same source as audit.py cat_c)."""
      m = re.search(rf'^\s*{re.escape(field)}\s*[:=]\s*(.+?)\s*$', sr_text, re.M)
      return m.group(1).strip() if m else default

  # Priority: exam_config OVERRIDE > section_rules PRIMARY > blueprint fallback > default
  FONT_NAME        = _ecfg.get('font_name',
                       _sr_field('font_family', bp.get('font_name', 'Calibri')))
  FONT_SIZE_PT     = int(_ecfg.get('font_size_pt',
                       _sr_field('font_size_pt', bp.get('font_size_pt', 11))))
  _sr_label        = _sr_field('option_label_format', None)
  # v5.37 (GAP-2026-08-03-LABELFMT) — RESOLUTION IS DELEGATED, NOT RE-IMPLEMENTED.
  # The inline casing test this replaced had NO ROMAN BRANCH and NO ELSE-BRANCH:
  #   'i/ii/iii/iv' -> .islower() -> ({alpha_lower}) -> rendered (a)(b)(c)(d), while
  #     the auditor's option_label_family read 'roman'. A-OPTLABEL then FAILED EVERY
  #     question, exit 1, the audit refused to certify, and NO CP repair could fix a
  #     paper that matched this step's own contract. Measured end-to-end.
  #   '(1)/(2)/(3)/(4)' fell through and became the template VERBATIM — no {text}
  #     placeholder, so no substitution happened at all.
  #   '[A]/[B]/[C]/[D]' silently became '(A)'; '(circled digits)' silently became
  #     '1.' (Python's .isdigit() is True for them).
  # paper_pipeline is routed by BOTH MockCreate and TestCreate, so one resolver
  # there is reachable from both steps and the pair cannot drift again. It ASSERTS
  # that the family this step renders equals the family audit.py will classify, and
  # RAISES rather than guessing — a guessed label reaches the delivered paper.
  _resolved_family = None
  if _sr_label:
      try:
          _sr_label, _resolved_family = pp.resolve_option_label(_sr_label)
      except pp.LabelFormatError as e:
          raise SystemExit(f"HARD STOP [HS:INPUT]: {e}")
  # v5.65: the former bp.get('option_label_format') tier is REMOVED — no writer
  # emits that blueprint key (Blueprint §14 writes option_label, visibility-only),
  # so the tier could never fire; chain: exam_config -> section_rules -> default.
  # v5.66 (GAP-2026-08-23-ECFG-LABEL-PARITY) — THE OVERRIDE GOES THROUGH THE
  # SAME RESOLVER. Family is derived from the resolved template's TOKEN (never
  # from option_label_family on a template string — its pass-through branch
  # falls back to 'num' for alpha/roman templates) and asserted equal to the
  # family the auditor will classify from section_rules (or its '1/2/3/4'
  # default when section_rules declares no label). Refuse at PRE-GENERATION —
  # a guessed label reaches the delivered paper; this HARD STOP [HS:INPUT] happens before Q1.
  def _label_family_of_template(_tpl):
      for _tk, _fm in (('{i}', 'num'),
                       ('{alpha_upper}', 'alpha'), ('{alpha_lower}', 'alpha'),
                       ('{roman_upper}', 'roman'), ('{roman_lower}', 'roman')):
          if _tk in _tpl:
              return _fm
      return None
  _ecfg_label = _ecfg.get('option_label_format')
  if _ecfg_label:
      try:
          _ecfg_label, _ = pp.resolve_option_label(_ecfg_label)
      except pp.LabelFormatError as e:
          raise SystemExit(f"HARD STOP [HS:INPUT]: {e}")
      _ecfg_family = _label_family_of_template(_ecfg_label)
      if _ecfg_family is None:
          raise SystemExit(
              "HARD STOP [HS:INPUT] (ECFG-LABEL PARITY): exam_config option_label_format "
              f"{_ecfg.get('option_label_format')!r} resolves to a template with no "
              "recognised label token ({i}/{alpha_*}/{roman_*}) — it cannot be "
              "rendered or audited. Declare a supported notation or template.")
      _audit_family = _resolved_family or 'num'
      if _ecfg_family != _audit_family:
          raise SystemExit(
              "HARD STOP [HS:INPUT] (ECFG-LABEL PARITY): exam_config option_label_format "
              f"renders {_ecfg_family!r} labels but the auditor will classify the "
              f"{_audit_family!r} family from section_rules"
              + ("" if _resolved_family else " (its '1/2/3/4' default — section_rules "
                 "declares no option_label_format)")
              + " — A-OPTLABEL would FAIL every question on a paper that obeys this "
              "override, with no CP repair possible. Align section_rules (re-run "
              "Step 5 or set its option_label_format) or drop the override.")
  OPTION_LABEL_FMT = (_ecfg_label or _sr_label or '{i}.  {text}')
  # Regex for gate G-OPTLABEL built from the configured format:
  import re as _re_cfg
  _opt_prefix = OPTION_LABEL_FMT.split('{text}')[0].replace('{i}', r'\d+')
  _opt_prefix = _opt_prefix.replace('{alpha_upper}', r'[A-Z]').replace('{alpha_lower}', r'[a-z]')
  # v5.37 — roman tokens, else G-OPTLABEL would never match a roman-labelled paper
  _opt_prefix = _opt_prefix.replace('{roman_upper}', r'[IVX]+').replace('{roman_lower}', r'[ivx]+')
  OPTION_LABEL_RE  = _re_cfg.compile(r'^\s*' + _re_cfg.escape(_opt_prefix).replace(
                         _re_cfg.escape(r'\d+'), r'\d+').replace(
                         _re_cfg.escape(r'[A-Z]'), r'[A-Z]').replace(
                         _re_cfg.escape(r'[a-z]'), r'[a-z]'))
  DI_HEADER_COLOR  = _ecfg.get('di_header_color',
                       _sr_field('di_header_color', bp.get('di_header_color', '1F4E79')))
  # FONT_BANNED: fonts that are never acceptable UNLESS they ARE the configured font.
  FONT_BANNED      = {f.lower() for f in _ecfg.get('font_banned', ['Arial'])} - {FONT_NAME.lower()}

  mock_entry = next((m for m in bp['mocks'] if m['mock'] == N), None)
  if not mock_entry:
      raise SystemExit(f"HARD STOP [HS:INPUT]: Mock {N} not found in blueprint.json mocks[].")

  # BUILD allocations dict from actual blueprint schema:
  # blueprint stores: mocks[i].sections[j].subtopic_allocations
  # We build: allocations = {section_name: {subtopic_name: q_count}}
  # AND alloc_ids = {section_name: {subtopic_id: {q_count, display_name}}}  (v3.4)
  allocations = {}
  alloc_ids = {}
  for sec in mock_entry.get('sections', []):
      sec_name = sec['section_name']
      allocations[sec_name] = {}
      alloc_ids[sec_name] = {}
      for sa in sec.get('subtopic_allocations', []):
          allocations[sec_name][sa['subtopic']] = sa['q_count']
          # subtopic_id is the JOIN KEY (v3.4 contract). Blueprint v1.7+ always
          # carries it. If absent (legacy blueprint) → contract gate S3-CONTRACT
          # will HARD STOP [HS:INPUT]; do not silently fall back to name matching.
          sid = sa.get('subtopic_id')
          alloc_ids[sec_name][sid] = {'q_count': sa['q_count'],
                                      'display_name': sa['subtopic']}

  # ALSO build batch_ranges from sections[]:
  # batch_ranges = {section_name: [q_start, q_end]}
  batch_ranges = {}
  for s in sections:
      batch_ranges[s['name']] = s['q_range']

  # Optional per-mock fields (present only in some blueprint versions):
  english_structure = mock_entry.get('english_structure', {})
  image_subtopics   = mock_entry.get('image_subtopics', {})

  # dedup_partition: may be at mock level or absent (use defaults if missing):
  dedup_partition = mock_entry.get('dedup_partition', {
      'rc_narrative_topic': None,
      'rc_report_topics': [],
      'cloze_topic': None,
      'math_seed_base': N * 100,
      'reasoning_seed_base': N * 50
  })

  # ── S3-2D — DIFFICULTY SCHEDULE RECOMPUTED FROM ITS PROVENANCE (v5.89 — GAP-2026-11-02
  # L2/P2). The delivered Organic scoped schedule 2/14/24 came from the PAPER-level mix
  # (not the scope's) converted in ALPHABETICAL key order (Easy, Hard, Medium). A blueprint
  # built by ScopedBlueprint v1.12.0+ / Blueprint v1.62.0+ carries difficulty_source with
  # its builder; the schedule is recomputed from it and the exam's difficulty profile with
  # bc.recompute_difficulty_schedule. On a mismatch the IN-RUN blueprint (BP_SRC_PATH — the
  # file every auditor run reads with --blueprint) is amended IN PLACE and the amendment is
  # logged in difficulty_amendments[]; v5.91 (D3 a): the amended blueprint is NOT delivered —
  # every run recomputes it the same way from the same provenance — and one informational
  # footer line records the amendment. A legacy blueprint (no
  # provenance) is used as is, with the footer line "difficulty schedule unverified"
  # (+ "outside the expected range" when bc says so). Never a stop.
  import json, os
  import blueprint_core as _bc_dsrc
  BLUEPRINT_AMENDED = False
  DIFF_SRC_NOTE = None

  def persist_bp_amendment():
      # v5.89 L3: EVERY in-place amendment of `bp` (S3-2D recompute, legacy R5 accept-at-measured,
      # R5 subtopic reassignment) is written to BP_SRC_PATH IMMEDIATELY, so every later
      # auditor run (--blueprint BP_SRC_PATH), the S13-6 byte comparison and a resumed
      # session all see the same amended file. Call it right after each amendment.
      global BLUEPRINT_AMENDED
      json.dump(bp, open(BP_SRC_PATH, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
      BLUEPRINT_AMENDED = True
  _pf_dsrc = f'/mnt/project/{EXAM}_difficulty_profile.json'
  try:   # read ONLY when this blueprint schedules difficulty (never a stop otherwise)
      _prof_dsrc = (json.load(open(_pf_dsrc, encoding='utf-8'))
                    if bp.get('difficulty_schedule') and os.path.exists(_pf_dsrc) else None)
  except (ValueError, OSError) as _e_dsrc:
      # v6.0 (GAP-2026-11-10 G-09 F-09.3 / G-14 row 5, LAW-ORG-12): an unreadable profile is NEVER a stop — the run
      # continues on the exam ruler (S0-OP-2; library level when the exam has too few anchors) and the profile is
      # rebuilt by the S0-OP-0 migration from the project's own past papers. One AMBER line, recorded.
      _prof_dsrc = None
      print(f"S3-2D: {EXAM}_difficulty_profile.json unreadable ({type(_e_dsrc).__name__}) — continuing on the exam "
            f"ruler / library level; the profile is rebuilt by the S0-OP-0 migration (AMBER, never a stop).")
  # The full-paper Blueprint's S7-0 schedule (builder 'Framework_Blueprint.S7-0', or a
  # pre-v1.62 full-paper difficulty_source with no builder and no subtopic_ids) is the
  # operator-chosen mix validated by A-DPROFILE — never reported as 'unverified'.
  _ds_dsrc = bp.get('difficulty_source')
  _full_paper_src = isinstance(_ds_dsrc, dict) and (
      _ds_dsrc.get('builder') == 'Framework_Blueprint.S7-0'
      or (not _ds_dsrc.get('builder') and not _ds_dsrc.get('subtopic_ids')))
  if bp.get('difficulty_schedule') and _prof_dsrc is not None:
      _rc = _bc_dsrc.recompute_difficulty_schedule(bp, _prof_dsrc)
      if _rc.get('ok') is False:
          for _mm in _rc.get('mismatches') or []:
              print(f"S3-2D: difficulty_schedule mock {_mm.get('mock')} recomputed "
                    f"{_mm.get('from')} -> {_mm.get('to')} ({_rc.get('reason')})")
          _exp = {e['mock']: e for e in (_rc.get('expected') or [])}
          for _e in bp['difficulty_schedule']:
              if _e.get('mock') in _exp:
                  for _k in ('simple', 'medium', 'hard', 'by_section'):
                      if _k in _exp[_e['mock']]:
                          _e[_k] = _exp[_e['mock']][_k]
          bp.setdefault('difficulty_amendments', []).extend(
              {'mock': _mm.get('mock'), 'section': None,
               'from': list(_mm.get('from') or ()), 'to': list(_mm.get('to') or ()),
               'reason': 'recomputed'} for _mm in (_rc.get('mismatches') or []))
          persist_bp_amendment()
      elif _rc.get('ok') is None and _rc.get('reason') != 'full_paper_builder':
          # full_paper_builder: the full Blueprint's S7-0 per-section mix, validated by
          # A-DPROFILE — verified, just not recomputable; no footer note.
          DIFF_SRC_NOTE = ('difficulty schedule unverified'
                           + (' — outside the expected range' if _rc.get('outside_expected_range')
                              else ''))
  elif bp.get('difficulty_schedule') and not _full_paper_src:
      DIFF_SRC_NOTE = 'difficulty schedule unverified (no difficulty profile in the project)'
  difficulty_schedule = bp.get('difficulty_schedule', difficulty_schedule)

  # ── S3-2S — DRAWING STYLE + STRUCTURE TOKENS (v5.89 — GAP-2026-11-02 F1). Computed ONCE
  # per paper; every figure of a role uses the SAME tokens (one bond length per role).
  # A paper with no CHEMISTRY figure (CHEM_FIGURES below) draws no structure: no rdkit
  # provisioning, no style note — the footer stays green for every other exam.
  import figural_core as _fc_style
  STYLE_PROFILE = _fc_style.load_style_profile(f'/home/claude/{EXAM}_section_rules.md')
  TOK = {'problem': _fc_style.structure_tokens(STYLE_PROFILE, 'problem'),
         'option': _fc_style.structure_tokens(STYLE_PROFILE, 'option')}
  ABBREV = (list(STYLE_PROFILE.get('abbreviation_labels') or [])
            if STYLE_PROFILE.get('abbreviates') is True else None)   # None => no abbreviation
  STYLE_NOTES = []
  # The native structure renderer (rdkit) is provisioned unless the in-scope PYQ evidence
  # shows NO chemistry structure / scheme (section_rules PYQ_IMAGE_ANALYSIS object types,
  # dominant or observed, none in figure_types.CHEM_R_OBJECT_TYPES). A chart / geometry /
  # reasoning exam with that evidence never provisions rdkit and never carries a
  # "renderer degraded" note; an exam WITHOUT the evidence is treated as possibly chemical.
  import figure_types as _ft_style
  _img_style = _bc_dsrc.parse_image_analysis_blocks(sr_text)
  _scope_style = {x.get('subtopic_id') for x in subtopic_list if isinstance(x, dict)}
  _style_types = []
  for _sid_s, _rec_s in _img_style.items():
      if _sid_s in _scope_style:
          _ots_s = _rec_s.get('object_types') or {}
          _style_types += list(_ots_s.get('dominant') or []) + list(_ots_s.get('observed') or [])
  # No recorded object types (no PYQ_IMAGE_ANALYSIS block, empty lists, vision unavailable)
  # is NOT evidence of "no chemistry": the renderer is then provisioned as before.
  CHEM_FIGURES = bool(figural_present) and (not _style_types or any(
      _ft_style.lookup(_ot)['type'] in _ft_style.CHEM_R_OBJECT_TYPES for _ot in _style_types))
  if CHEM_FIGURES:
      NATIVE = _fc_style.ensure_native_raster(install=True)
      NATIVE_OK = bool(NATIVE.get('available'))
      if STYLE_PROFILE['evidence']['status'] != 'measured':
          STYLE_NOTES.append('drawing style from framework defaults')
      elif 'default' in (TOK['problem'].get('source'), TOK['option'].get('source')):
          # colour / frame were measured, but too few chemistry pictures for print sizes
          STYLE_NOTES.append('drawing style measured; structure print sizes from framework '
                             'defaults (too few measured chemistry pictures, or the PYQ '
                             'pictures are placed at one fixed width)')
      if not NATIVE_OK:
          STYLE_NOTES.append('renderer degraded (native structure raster unavailable: '
                             + ', '.join(NATIVE.get('missing') or []) + ')')
  else:
      NATIVE, NATIVE_OK = {'available': False,
                           'missing': ['not needed: no chemistry structure/scheme in scope']}, False
  print(f"S3-2S: style={STYLE_PROFILE['evidence']['status']} TOK={TOK} "
        f"abbreviations={ABBREV} native_raster={NATIVE_OK}")
  # v5.92 (GAP-2026-11-05 DL-50): the subtopics whose DOMINANT PYQ figure type is a chemistry
  # structure / scheme family. Read by S7-NEW-B: for these, an ABSENT figural_reducible line
  # in section_rules defaults to False (the options ARE the structures), never True.
  CHEM_FIGURE_SUBTOPICS = set()
  for _sid_c, _rec_c in _img_style.items():
      _dom_c = list(((_rec_c.get('object_types') or {}).get('dominant')) or [])
      if any(_ft_style.lookup(_ot).get('family') in ('chem_structure', 'chem_scheme') for _ot in _dom_c):
          CHEM_FIGURE_SUBTOPICS.add(_sid_c)

  diff_entry = next((d for d in difficulty_schedule if d['mock'] == N), {})
  n_simple = diff_entry.get('simple', total_questions // 4)
  n_medium = diff_entry.get('medium', total_questions // 2)
  n_hard   = diff_entry.get('hard',   total_questions // 4)

  # v5.2 SCHEDULE-FIRST difficulty assignment + capture (Contract_QuestionMetadataIndex v1.0).
  # n_simple/n_medium/n_hard are the QUOTA for this mock. Difficulty is assigned SCHEDULE-FIRST:
  # every question is placed into one band to fill the quota EXACTLY; PYQ calibration (S7 CHECK)
  # chooses WHICH questions take Simple vs Hard, and difficulty is also a generation lever
  # (number size / step count / directness). Each question's band is recorded as the CANONICAL
  # label from blueprint.difficulty_labels and passed to write_q_to_sidecar(difficulty=...) per
  # question — NEVER written to the docx. At Final Assembly the labels roll up into
  # registry.question_index (S13-4); G-QINDEX (S12-NEW-26) then requires their distribution to
  # EQUAL {n_simple, n_medium, n_hard} exactly — satisfiable by construction under this rule.
  # v5.14: difficulty stays SCHEDULE-FIRST and untouched. The Option-3 JOINT solve adds a
  # near-ORTHOGONAL second axis (Axis-2 stem structure, S7-AXIS): a MATCH/A-R/… question can be
  # any difficulty band, so both the difficulty quota AND the Axis-2 window target are met
  # together. On a genuine conflict the tie-break bends AXIS-2, never difficulty (which G-QINDEX
  # still enforces exactly). See S7-AXIS for the full contract.
  difficulty_labels = bp.get('difficulty_labels', ['Easy', 'Medium', 'Hard'])
  def canonical_difficulty(sched_key):
      # sched_key in {'simple','medium','hard'} -> canonical label. Honours an exam-overridden
      # 3-band difficulty_labels positionally; falls back to the fixed alias otherwise. (A non-
      # 3-band label set also needs an adapted schedule -- out of scope; 3-band fully supported.)
      _alias = {'simple': 'Easy', 'medium': 'Medium', 'hard': 'Hard'}
      if len(difficulty_labels) == 3:
          return {'simple': difficulty_labels[0], 'medium': difficulty_labels[1],
                  'hard': difficulty_labels[2]}.get(sched_key, _alias.get(sched_key, sched_key))
      return _alias.get(sched_key, sched_key)

  ```
  S0-OP AT S3 (v6.0 — §S0-OP-0 / -1 / -2 / -7): run these three blocks NOW, in order, before the difficulty
  plan below (the plan reads EXAM_RULER; S0-OP-0 may hand the run to O-BACKFILL first).
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S0-OP-0 / S0-OP-1 (v6.0) ──
  import json, os, blueprint_core as bc
  EXAM = globals()['EXAM']                                     # bound by S3-1 (this block runs at S3, S0-OP order)
  _op_prof_p = f'/mnt/project/{EXAM}_difficulty_profile.json'
  _op_work_p = f'/home/claude/{EXAM}_op_profile.json'          # the S0-OP working profile (O-BACKFILL writes HERE)
  if os.path.exists(_op_work_p):                               # this session already loaded / back-filled it
      OP_PROFILE = json.load(open(_op_work_p, encoding='utf-8'))
  else:                                                        # project profile + earlier runs' back-fill (registry)
      _op_r0 = ((globals().get('REG_SRC') or {}).get('registry') or {}) if isinstance(globals().get('REG_SRC'), dict) else {}
      OP_PROFILE, _op_n_ov = bc.profile_overlay(json.load(open(_op_prof_p, encoding='utf-8')) if os.path.exists(_op_prof_p)
                                                else {'papers': {}}, _op_r0.get('pyq_backfill'))
      json.dump(OP_PROFILE, open(_op_work_p, 'w', encoding='utf-8'), ensure_ascii=False)
      print(f"S0-OP-0: {_op_n_ov} back-filled record(s) restored from registry.json['pyq_backfill'].")
  # the exam config S3-2 loaded (exam-level file wins over the shared one); there is no global named exam_config
  OP_EXAM_CONFIG = {**(globals().get('_ecfg') or {}), **(globals().get('exam_config') or {}),
                    **(globals().get('_ecfg_exam') or {})}        # the exam's own file wins
  bc.op_constants_reset()                                      # an earlier exam's override never leaks into this one
  OP_CONST = bc.op_constants(OP_EXAM_CONFIG)
  for _ck in OP_CONST['overrides']:                            # an override is APPLIED, not only printed (§6.2)
      setattr(bc, _ck.split('=')[0], OP_CONST[_ck.split('=')[0]])
  OP_SCOPE = bc.organic_scope(OP_PROFILE)                      # LAW-ORG-1 — by content
  OP_TARGET_POOL = bc.pyq_target_pool(OP_PROFILE)              # 'full' + schema 3 only (LAW-ORG-2)
  OP_GUARD_POOL = bc.pyq_guard_pool(OP_PROFILE)                # every record (clone guard)
  OP_N_VERIFIED_ORG = sum(1 for r in OP_TARGET_POOL if r.get('organic') is True)
  OP_NEEDS_BACKFILL = [f"{r['_paper']}:{r['_q']}" for r in OP_GUARD_POOL if bc.pyq_record_status(r) != 'full'
                       and int(r.get('reread_count') or 0) < bc.C_PYQ_REREAD_MAX]   # a capped record stays 'partial'
  OP_LEVEL = bc.exam_level(OP_EXAM_CONFIG, EXAM)
  _op_lib_p = '/tmp/fw_effective/organic_library.json'
  OP_LIBRARY = bc.organic_library_from(json.load(open(_op_lib_p, encoding='utf-8')) if os.path.exists(_op_lib_p)
                                       else None)               # framework-level; empty-capable (LEVEL_DEFAULT_RECIPES)
  print(f"S0-OP-0: {len(OP_GUARD_POOL)} PYQ records, {len(OP_TARGET_POOL)} verified (schema {bc.PYQ_SCHEMA_VERSION}); "
        f"organic exam {OP_SCOPE['exam_organic']} ({OP_SCOPE['n_organic']} organic records, {OP_N_VERIFIED_ORG} verified); "
        f"{len(OP_NEEDS_BACKFILL)} record(s) for O-BACKFILL; level {OP_LEVEL[0]} ({OP_LEVEL[1]}); "
        f"library {'used' if bc.library_needed(OP_N_VERIFIED_ORG) else 'fallback only'}; "
        f"constant overrides {OP_CONST['overrides'] or 'none'}.")
  # BACK-FILL BEFORE THE RULER AND THE PLAN (S0-OP-0): the run hands over to O-BACKFILL while records are listed and
  # the last pass made progress — at most bc.C_PYQ_REREAD_MAX + 1 passes per paper; a record that cannot be
  # completed stays 'partial' (out of every target pool, in the clone guard) and the run continues.
  import hashlib as _hl_bf
  _op_bf_p = f'/home/claude/{EXAM}_M{N}_op_backfill_state.json'   # per PAPER
  _op_bf = json.load(open(_op_bf_p, encoding='utf-8')) if os.path.exists(_op_bf_p) else {'passes': 0, 'last_n': None}
  _op_wh = _hl_bf.sha256(open(_op_work_p, 'rb').read()).hexdigest() if os.path.exists(_op_work_p) else None
  _op_raise = False
  if OP_NEEDS_BACKFILL and _op_bf.get('last_hash') is not None and _op_bf.get('last_hash') == _op_wh:
      # re-entered without any back-fill having run since the hand-over: ask again (at most twice), then continue
      _op_bf['idle'] = int(_op_bf.get('idle') or 0) + 1
      _op_raise = _op_bf['idle'] <= 2
  elif OP_NEEDS_BACKFILL and _op_bf['passes'] <= bc.C_PYQ_REREAD_MAX and (
          _op_bf['last_n'] is None or len(OP_NEEDS_BACKFILL) < _op_bf['last_n']):
      _op_bf = {'passes': _op_bf['passes'] + 1, 'last_n': len(OP_NEEDS_BACKFILL), 'last_hash': _op_wh, 'idle': 0}
      _op_raise = True
  _op_bf['records'] = OP_NEEDS_BACKFILL
  json.dump(_op_bf, open(_op_bf_p, 'w', encoding='utf-8'), indent=2)
  # v6.2 (GAP-2026-11-12-BATCH-SPEED): the back-fill no longer holds Q1 — the ruler's anchors use the PYQExplain
  # bands until blind grades exist (S0-BV BV-7). It runs before Q1 only when the exam config asks for it.
  if _op_raise and OP_EXAM_CONFIG.get('pyq_backfill_before_q1') is not True:
      print(f"S0-OP-0: {len(OP_NEEDS_BACKFILL)} PYQ record(s) without blind grades — Q1 starts now; the ruler uses the "
            f"PYQExplain bands as anchors (BV-7). Set exam_config 'pyq_backfill_before_q1': true to back-fill first.")
      _op_raise = False
  if _op_raise:
      raise RuntimeError(f"BACKFILL [HS:LADDER] (S0-OP-0): {len(OP_NEEDS_BACKFILL)} PYQ record(s) need the schema-3 "
                         f"back-fill — run O-BACKFILL (Framework_PYQExplain §13A-3B, fresh workers / sub-agents) on "
                         f"{_op_bf_p} 'records', writing each paper's records into {_op_work_p} with bc.profile_merge_records; then "
                         f"re-run S3-2 from this block.")
  def OP_WRITE_CONTROLS(q, grader_1, grader_2, packets, key_votes, decisions_grader=None, figures=None,
                        clone_check=None, stereo_gate=None):
      """S0-OP-5 THE WRITER — records an item's control results ON its answer-key concept_map entry, bound to that
      entry's own text (bc.op_content_sha over stem_text / option_texts / figure_files) and to the auditor's item hash
      when one exists; the recipe verdict is computed here at the entry's label band. Used by CHECK 3c (after
      write_q_to_sidecar) and by the S13-2G delta round (re-graded items). Returns the written entry."""
      _kp_w = f'/home/claude/{EXAM}_M{N}_answer_key.json'
      _kd_w = json.load(open(_kp_w, encoding='utf-8'))
      _e_w = (_kd_w.setdefault('concept_map', {})).get(str(q)) or {}
      _ru_w = globals().get('EXAM_RULER') or {}
      _rb_w = ((_ru_w.get('recipe') or {}) if isinstance(_ru_w.get('recipe'), dict) else {}).get(_e_w.get('difficulty'))
      _rc_w = bc.band_recipe_check(_e_w, _rb_w) if isinstance(_rb_w, dict) else (False, ['no recipe'])
      _rec_ok = bool(_rc_w[0]) or (bool(_rc_w[1]) and all('dormant' in str(_x) for _x in _rc_w[1]))
      _hj_w = f'/home/claude/{EXAM}_M{N}_item_hashes.json'
      _ih_w = (json.load(open(_hj_w, encoding='utf-8')) if os.path.exists(_hj_w) else {}).get(str(q))
      _kd_w['concept_map'][str(q)] = bc.op_record_controls(_e_w, grader_1, grader_2, _rec_ok, packets,
                                                           decisions_grader, key_votes, figures, clone_check,
                                                           stereo_gate, item_hash=_ih_w)
      json.dump(_kd_w, open(_kp_w, 'w', encoding='utf-8'), indent=2)
      return _kd_w['concept_map'][str(q)]
  if OP_NEEDS_BACKFILL:
      print(f"S0-OP-0: {len(OP_NEEDS_BACKFILL)} record(s) stay 'partial' after {_op_bf['passes']} back-fill pass(es) — "
            f"excluded from every target pool, kept in the clone guard; the run continues.")
  ```
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S0-OP-2 (v6.0) ──
  import datetime as _dt_op
  # the registry this run reads (REGISTRY-SOURCE-LAW: S3-1 resolved it through pp.resolve_registry; a first paper has
  # none yet — the ruler is then built here and committed by S13-4OP)
  _op_reg = ((globals().get('REG_SRC') or {}).get('registry') or {}) if isinstance(globals().get('REG_SRC'), dict) else {}
  EXAM_RULER = _op_reg.get('difficulty_ruler') if isinstance(_op_reg.get('difficulty_ruler'), dict) else None
  _op_labels = list(globals().get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
  _op_graded = bc.ruler_graded_count(OP_PROFILE, _op_labels)  # the ruler's OWN input rule (back-fill progress)
  _op_recal, _op_why = bc.ruler_needs_recalibration(EXAM_RULER, model_id=globals().get('GRADER_MODEL_ID'),
                                                    paper_count=len(OP_PROFILE.get('papers') or {}),
                                                    graded_count=_op_graded)
  if _op_recal:
      EXAM_RULER = bc.build_difficulty_ruler(OP_PROFILE, _op_labels, version=f'{EXAM}-{_dt_op.date.today().isoformat()}',
                                             model_id=globals().get('GRADER_MODEL_ID') or 'session-model',
                                             prompt_version='S0-OP-5/v1', date=_dt_op.date.today().isoformat(),
                                             library=OP_LIBRARY, level=OP_LEVEL[0],
                                             manifest=globals().get('manifest'))     # v6.1: recipe keyed by manifest section
      EXAM_RULER['paper_count'] = len(OP_PROFILE.get('papers') or {})
      EXAM_RULER['graded_count'] = _op_graded
  print(f"S0-OP-2: ruler {EXAM_RULER['ruler_version']} ({EXAM_RULER['basis']}; anchors from "
        f"{EXAM_RULER.get('anchor_basis', 'blind_grades')}; {_op_why}); anchors "
        + ', '.join(f"{b} {len(EXAM_RULER['anchors'].get(b) or [])}" for b in _op_labels)
        + f"; past distribution {EXAM_RULER['past_distribution']} (printed apart from the requested schedule).")
  ```
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S0-OP-7 load (v6.0) — at S3 ──
  _op_rsv_p = f'/home/claude/{EXAM}_reserve.json'
  _op_ser_p = f'/home/claude/{EXAM}_series_registry.json'
  if not os.path.exists(_op_rsv_p):
      json.dump(_op_reg.get('reserve') if isinstance(_op_reg.get('reserve'), dict) else bc.reserve_new(EXAM),
                open(_op_rsv_p, 'w', encoding='utf-8'), indent=2)
  if not os.path.exists(_op_ser_p):
      _op_sr = _op_reg.get('series_registry') if isinstance(_op_reg.get('series_registry'), dict) else None
      if _op_sr is None:                                       # seeded from every delivered mock's committed rows
          _op_sr = {'papers': {}}
          _op_byp = {}
          for _pe in (_op_reg.get('question_index') or []):          # one entry per committed PAPER
              for _qi in ((_pe.get('questions') or []) if isinstance(_pe, dict) else []):
                  if isinstance(_qi, dict) and _qi.get('organic') is True:
                      _op_byp.setdefault(str(_pe.get('paper_id') or _pe.get('mock') or 'legacy'), []).append(_qi)
          for _pid_s, _rows_s in _op_byp.items():
              _op_sr = bc.series_registry_add(_op_sr, _pid_s, _rows_s)
      json.dump(_op_sr, open(_op_ser_p, 'w', encoding='utf-8'), indent=2)
  OP_SERIES_ROWS = bc.series_registry_rows(json.load(open(_op_ser_p, encoding='utf-8')))
  ```
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # v5.60 — THE DIFFICULTY PLAN (GAP-2026-08-21-DIFFICULTY-STICKER-LABELS).
  # SCHEDULE-FIRST survives intact: the user's trigger/band ratio is the LAW for
  # HOW MANY questions sit in each band, exactly as before — including deliberately
  # hard series. What changes is that the band is now an AUTHORING TARGET with a
  # definition (bc.assess_difficulty, the same Tier-1 rubric PYQ-1 uses), not a
  # sticker: WHICH positions may take the bottom band is floor-constrained, and
  # every accepted question must MEASURE as its band from its own recorded
  # derivation (S7 CHECK 3c / G-DIFF). Measured driver: M01 shipped 45 'Hard'
  # labels on quota alone; 14/60 agreed with the rubric; 4 'Easy' labels sat on
  # MSQ/NAT positions the rubric cannot reach. Every count-based gate passed.
  import blueprint_core as bc           # S1-2b engine (single source of truth)
  _qtype_by_q = {q: {'MCQ': 'mcq', 'MSQ': 'msq', 'NAT': 'nat'}
                    .get(str(_type_for_q(q)).strip().upper(), 'mcq')
                 for q in range(1, total_questions + 1)}
  difficulty_plan = None                       # {q: canonical label} | None = dormant
  # v5.92 (GAP-2026-11-05 Part D): the per-paper DIFFICULTY STATE the footer discloses —
  # defined for EVERY paper (a dormant plan included: S3-16 persists it), updated inside
  # CHECK 3c (judge dormant, level item, R5 Hard miss) with batch_state['difficulty_state']
  # = DIFFICULTY_STATE in the SAME write that persists difficulty_plan. Counts only; never a stop.
  DIFFICULTY_STATE = {'judge_dormant_qs': [], 'hard_missed': 0, 'n_level_items': 0}
  PROFILE_COVERAGE = None                      # v5.92: set below when a profile is loaded
  if diff_entry and len(difficulty_labels) == 3:
      _dcounts = {'simple': n_simple, 'medium': n_medium, 'hard': n_hard}
      # v6.0 (GAP-2026-11-10 G-09, LAW-ORG-6 SCHEDULE-IS-INPUT): the requested schedule is the REQUIREMENT, never
      # something validated against framework assumptions. It is normalised ONCE (bc.schedule_normalize — an
      # exact-sum request is never altered; percentages / wrong sums / unknown band names are normalised and
      # printed "schedule as applied") and frozen in S0-OP-3. difficulty_feasibility is a PLANNING HINT only: it
      # names the slots that need band operators or the library; it NEVER stops and NEVER changes the schedule.
      _sched_req = {difficulty_labels[0]: n_simple, difficulty_labels[1]: n_medium, difficulty_labels[2]: n_hard}
      SCHEDULE_APPLIED = bc.schedule_normalize(_sched_req, total_questions, difficulty_labels,
                                               (EXAM_RULER or {}).get('past_distribution') if 'EXAM_RULER' in globals() else None)
      if SCHEDULE_APPLIED['altered']:
          print('S3 schedule as applied: ' + '; '.join(SCHEDULE_APPLIED['notes']))
      n_simple, n_medium, n_hard = (SCHEDULE_APPLIED['counts'][difficulty_labels[0]],
                                    SCHEDULE_APPLIED['counts'][difficulty_labels[1]],
                                    SCHEDULE_APPLIED['counts'][difficulty_labels[2]])
      _dcounts = {'simple': n_simple, 'medium': n_medium, 'hard': n_hard}
      _dshort = bc.difficulty_feasibility(_dcounts, _qtype_by_q, difficulty_labels)
      if _dshort:
          _lab, _d = next(iter(_dshort.items()))
          print(f"S3 planning hint (v6.0 — never a stop): {_d['requested']} '{_lab}' slots requested; the legacy rubric "
                f"floor would allow {_d['max_achievable']}. The exam ruler's anchors decide (bc.ruler_min_band); slots "
                f"without an anchor of that band are written with band operators + the library (S0-OP-6).")
      # Deterministic, floor-honouring, seed-rotated per mock so the bottom band
      # doesn't sit on the same positions in every paper of the series.
      # v5.75 (GAP-2026-08-27-DIFFICULTY-PROFILE): when the schedule carries PER-SECTION
      # counts (Blueprint v1.57.0 S7-5 by_section — the exam's own mix per section), the
      # plan is built section by section so a Reasoning question never borrows a
      # General-Awareness slot; a DPError names the section and its MCQ cap. A schedule
      # without by_section (progressive bands, or a pre-v1.57.0 blueprint) plans paper-wide
      # exactly as before.
      _by_sec = diff_entry.get('by_section')
      if _by_sec:
          # v5.89: by_section is keyed by the BLUEPRINT's own section names (Blueprint S7-5
          # and ScopedBlueprint S5-P both write them) — so the plan is built over the
          # blueprint's sections. A scoped paper's single section ("Organic Chemistry",
          # 1..Q) is not an exam_config section; exam_config.sections is used only when
          # the blueprint's names do not cover by_section (a pre-v1.57 blueprint).
          _bp_secs = [{'name': _s['name'], 'q_range': _s['q_range']} for _s in sections
                      if isinstance(_s, dict) and _s.get('name') and _s.get('q_range')]
          _plan_secs = (_bp_secs if _bp_secs and set(_by_sec) <= {_s['name'] for _s in _bp_secs}
                        else _ecfg_dp.get('sections'))
          PLAN_SECTIONS = list(_plan_secs or [])     # read by S3-12e: swaps stay inside THESE sections
          try:
              difficulty_plan = bc.assign_difficulty_bands_by_section(
                  _by_sec, _qtype_by_q, _plan_secs, difficulty_labels, seed=N)
          except (bc.DPError, ValueError) as _e:
              # v6.0 (G-09 / G-14 row 5): never a stop — each section's counts are placed EXACTLY by
              # bc.schedule_place (no infeasibility exists; the exam ruler's anchors decide qtype floors)
              print(f"S3 per-section plan: {_e} — placed by bc.schedule_place (v6.0, never a stop).")
              difficulty_plan = {}
              for _sx in (_plan_secs or []):
                  _lo, _hi = _sx['q_range']
                  _sc = bc.schedule_normalize(_by_sec.get(_sx['name']) or {}, _hi - _lo + 1, difficulty_labels)['counts']
                  _pl = bc.schedule_place(_sc, {q: _qtype_by_q[q] for q in range(_lo, _hi + 1)}, difficulty_labels,
                                          ruler=globals().get('EXAM_RULER'), seed=N)
                  difficulty_plan.update({int(k): v for k, v in _pl.items()})
              if set(difficulty_plan) != set(_qtype_by_q):           # no usable sections: place paper-wide, exactly
                  difficulty_plan = {int(k): v for k, v in bc.schedule_place(
                      {difficulty_labels[0]: n_simple, difficulty_labels[1]: n_medium, difficulty_labels[2]: n_hard},
                      _qtype_by_q, difficulty_labels, ruler=globals().get('EXAM_RULER'), seed=N).items()}
      else:
          # v6.0 (G-09 F-09.2): placement never stops — the legacy floor-honouring placement when it can place the
          # counts, else bc.schedule_place (exact, never infeasible; the exam ruler's anchors decide qtype floors)
          try:
              difficulty_plan = bc.assign_difficulty_bands(_dcounts, _qtype_by_q, difficulty_labels, seed=N)
          except ValueError:
              difficulty_plan = {int(k): v for k, v in bc.schedule_place(
                  {difficulty_labels[0]: n_simple, difficulty_labels[1]: n_medium, difficulty_labels[2]: n_hard},
                  _qtype_by_q, difficulty_labels, ruler=globals().get('EXAM_RULER'), seed=N).items()}
          PLAN_SECTIONS = []                         # a paper-wide plan: its counts are paper-wide (S3-12e)
      difficulty_plan = {q: lab for q, lab in difficulty_plan.items()}
      # v5.89: on a RESUMED paper the persisted plan is authoritative — band swaps (and, on a
      # legacy paper, R5 accept-at-measured) changed it after S3; a recomputed plan would disagree
      # with questions already accepted (G-QINDEX check 6).
      import os as _os_dp, json as _json_dp
      _bs_dp = f'/home/claude/{EXAM}_M{N}_batch_state.json'
      # The saved plan is adopted ONLY when it is provably THIS paper's: same paper_id
      # (batch_state is keyed by the paper NUMBER, so a scoped P1 and MOCK:M01 share
      # the file), exactly positions 1..total, and the band counts this schedule entry
      # (which already carries any R5 amendment) asks for.
      _pid_dp = next((_mk.get('paper_id') for _mk in bp.get('mocks', [])
                      if _mk.get('mock') == N), None) or f"MOCK:M{N:02d}"
      if _os_dp.path.exists(_bs_dp):
          _bsd = _json_dp.load(open(_bs_dp, encoding='utf-8')) or {}
          _saved_dp = _bsd.get('difficulty_plan')
          if isinstance(_bsd.get('difficulty_state'), dict) and _bsd.get('paper_id') == _pid_dp:
              DIFFICULTY_STATE = dict(DIFFICULTY_STATE, **_bsd['difficulty_state'])   # v5.92: resumed counts
          if _saved_dp and _bsd.get('paper_id') == _pid_dp:
              _cand = {int(k): v for k, v in _saved_dp.items()}
              _want = {difficulty_labels[0]: n_simple, difficulty_labels[1]: n_medium,
                       difficulty_labels[2]: n_hard}
              _have = {l: sum(1 for v in _cand.values() if v == l) for l in difficulty_labels}
              if set(_cand) == set(range(1, total_questions + 1)) and _have == _want:
                  difficulty_plan = _cand
              else:
                  print(f"S3: saved difficulty_plan does not match this schedule "
                        f"({_have} vs {_want}) — the fresh plan is used.")
      # v5.75: the profile for CHECK 3c calibration examples — optional, validated
      import os as _os, json as _json
      _pf_p = f'/mnt/project/{EXAM}_difficulty_profile.json'
      PROFILE_CFG = {'exam_code': EXAM, 'total_questions': total_questions,
                     'sections': _ecfg_dp.get('sections'), 'cycle_gap_days': _ecfg_dp.get('cycle_gap_days'),
                     'difficulty_labels': difficulty_labels}
      DIFFICULTY_PROFILE = None
      if _os.path.exists(_pf_p):
          try:
              DIFFICULTY_PROFILE = bc.dp_check_profile(_json.load(open(_pf_p, encoding='utf-8')),
                                                       EXAM, difficulty_labels)
          except bc.DPError as _e:
              # v6.0 (G-09 F-09.3, LAW-ORG-12): an unusable profile is rebuilt by the S0-OP-0 migration; this run
              # continues on the exam ruler / library level — never a stop
              DIFFICULTY_PROFILE = None
              print(f"S3 difficulty profile unusable ({_e}) — continuing on the exam ruler / library level (AMBER).")
      # v5.89 (GAP-2026-11-02 L1) — CONTENT-COMPLEXITY MODEL for CHECK 3c (b). Built
      # ONCE from the profile's per-question content vectors (PYQExplain v2.25 §13A) of the
      # questions in THIS paper's scope; dormant (None / active False) otherwise.
      CCP_MODEL, METHOD_LEXICON, LEVEL_MODEL = None, None, None
      if DIFFICULTY_PROFILE:
          _scope_ids = {x.get('subtopic_id') for x in subtopic_list}
          _pool = []
          for _pp in (DIFFICULTY_PROFILE.get('papers') or {}).values():
              for _qr in (_pp.get('questions') or {}).values():
                  if (isinstance(_qr, dict) and _qr.get('content_vector')
                          and _qr.get('content_confidence', 'full') == 'full'
                          and _qr.get('subtopic_id') in _scope_ids
                          and _qr.get('band') in difficulty_labels):
                      _pool.append((_qr['content_vector'], _qr['band']))
          if _pool:
              _mix = bc.dp_scope_mix(DIFFICULTY_PROFILE, sorted(_scope_ids),
                                     difficulty_labels,
                                     gap_days=PROFILE_CFG.get('cycle_gap_days'))
              CCP_MODEL = bc.ccp_model(_pool, _mix['pct'])
          if not (CCP_MODEL or {}).get('active'):
              STYLE_NOTES.append('level control: rubric + independent rating only '
                                 '(content-complexity model dormant)')
          # v5.92 (GAP-2026-11-05 Part A, DL-21/38/41) — the CHEMISTRY LEVEL MODEL (rule L1), built
          # by THE ONE builder every reader uses (Step 5, A-LEVEL, Step 9): the cuts come from the
          # blueprint's RECORDED mix (difficulty_source.measured_pct / mix_rule / params.tier —
          # owner D1-CUTS (A)); the pool is the content-full level vectors of the scope (cascade
          # scope -> topic -> section -> paper, first level with >= bc.LEVEL_MIN_POOL records,
          # owner D10 (B)). METHOD_LEXICON is the read-time reagent tier map the model used, so
          # a candidate's vector is measured with the SAME lexicon as the pool (DL-38).
          # The inputs come from the blueprint's `level_model_inputs` (Blueprint §7-9 (e) /
          # ScopedBlueprint S8-2e (e)) when present — the SAME record A-LEVEL reads — else from
          # the blueprint's difficulty_source / subtopic_list (a pre-1.64.0 blueprint).
          _ds_lv = bp.get('difficulty_source') if isinstance(bp.get('difficulty_source'), dict) else {}
          _lmi = bp.get('level_model_inputs') if isinstance(bp.get('level_model_inputs'), dict) else {}
          LEVEL_MODEL = bc.level_model_for_scope(
              DIFFICULTY_PROFILE,
              sorted(str(x) for x in (_lmi.get('subtopic_ids') or _scope_ids)), difficulty_labels,
              mix_rule=bc.mix_rule_of(_lmi.get('mix_rule') if _lmi else _ds_lv.get('mix_rule')),
              tier=(_lmi.get('tier') if _lmi else (_ds_lv.get('params') or {}).get('tier')),
              gap_days=(_lmi.get('gap_days') if _lmi else PROFILE_CFG.get('cycle_gap_days')),
              measured_pct=(_lmi.get('measured_pct') if _lmi else _ds_lv.get('measured_pct')),
              extra_text=globals().get('sr_text'))
          METHOD_LEXICON = dict(LEVEL_MODEL.get('lexicon') or {})
          # the model's STATE travels with DIFFICULTY_STATE (batch_state), so a later session
          # that re-enters §13 without this block (S4-12) prints the same footer lines
          DIFFICULTY_STATE['level_model'] = {k: LEVEL_MODEL.get(k) for k in
                                             ('active', 'n', 'small_pool', 'reason', 'level_used', 'shares')}
          # ... and the EXACT inputs it was built from (committed with difficulty_state, S13-4):
          # A-LEVEL / A-CLOSENESS rebuild from these first, so generator and auditor can never
          # use different windows or scopes — even on a pre-1.64.0 blueprint.
          DIFFICULTY_STATE['level_model']['inputs'] = {
              'subtopic_ids': sorted(str(x) for x in (_lmi.get('subtopic_ids') or _scope_ids)),
              'mix_rule': bc.mix_rule_of(_lmi.get('mix_rule') if _lmi else _ds_lv.get('mix_rule')),
              'tier': (_lmi.get('tier') if _lmi else (_ds_lv.get('params') or {}).get('tier')),
              'gap_days': (_lmi.get('gap_days') if _lmi else PROFILE_CFG.get('cycle_gap_days')),
              'measured_pct': (_lmi.get('measured_pct') if _lmi else _ds_lv.get('measured_pct')),
              'labels': list(difficulty_labels)}
          if LEVEL_MODEL.get('active'):
              print(f"S3: level model L1 ACTIVE — pool n={LEVEL_MODEL.get('n')} at level "
                    f"{LEVEL_MODEL.get('level_used')}, shares {LEVEL_MODEL.get('shares')}"
                    + (' (small pool)' if LEVEL_MODEL.get('small_pool') else ''))
          else:
              print(f"S3: level model L1 DORMANT — {LEVEL_MODEL.get('reason') or 'no content-full pool'}")
          # v5.92 (GAP-2026-11-05 DL-20): profile coverage, printed once; informational.
          PROFILE_COVERAGE = bc.dp_profile_coverage(DIFFICULTY_PROFILE)
          print('S3: ' + PROFILE_COVERAGE['line'])
      # Persisted as batch_state.json['difficulty_plan'] = {str(q): label} alongside
      # the rest of the S3 state (same write, same file) so `continue` resumes the
      # identical plan (v6.0: frozen — S0-OP-3; no band swap ever rewrites it).
  # DORMANT (difficulty_plan is None) when the exam declares no difficulty_schedule
  # entry for this mock OR a non-3-band vocabulary — the documented fall-through of
  # every Cluster-E2 function. Dormant means: no plan, no G-DIFF, labels assigned
  # exactly as pre-v5.60 (and A-QINDEX checks 7/8 stay proportionate: 7 needs a
  # marking_scheme, 8 needs recorded obs).
  ```

  LOAD EXPLAIN_LEARNINGS for quality constraints (GAP-07 fix; v5.56 filename seam
  fix; v5.78 GAP-2026-08-28-STEP7-SUBJECT-LEARNINGS-SEAM):
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  learnings_bans = []  # Extra banned patterns from prior Explain sessions
  # v5.78: DISCOVERY, never a rename instruction. The v5.77 WARN told the operator
  # to rename a non-{EXAM}-prefixed file — but per the Explain specs' S24 contract that file IS the subject
  # library, and renaming it per-exam re-plants the workaround the Explain-side fix
  # retired (GAP-2026-08-28-CATEGORY-C-ORPHAN-CONFIG-READ §6.2, decision D1). Step 7
  # now uses the SAME SUBJECT resolution Steps 9 / PYQ-1 use: the exam-family file
  # (exact v5.56 glob, unchanged) PLUS the discovered subject file — whose BANNED:/VERIFIED DEFECT:
  # markers were unreachable by this step under any naming before v5.78. >= 2
  # non-exam files → the helper abstains and S3-1 already WARNed; nothing loads
  # from the subject side (a wrong subject library is worse than none).
  import glob
  import explain_engine as _ee
  # Exam side: the exact v5.56 family glob (see the S3-1 comment for why the
  # discovery helper's broader exam partition must not be used here — it admits
  # the PYQ family, and a [-1] pick would swap families). Subject side: discovery.
  _fam = sorted(glob.glob(f'/home/claude/{EXAM}_EXPLAIN_LEARNINGS_v*.md'))
  _ignored_ex, _subj_file, _amb = _ee.resolve_learnings_files('/home/claude', EXAM)
  _lf = ([_fam[-1]] if _fam else
         [f'/home/claude/{EXAM}_ExplainLearnings.md'])   # legacy fallback (S3-1 warned)
  if _subj_file:
      _lf.append(_subj_file)
  _loaded = []
  for learn_file in _lf:
      if os.path.exists(learn_file):
          content = open(learn_file, encoding='utf-8').read()
          # Extract explicit BANNED/VERIFIED DEFECT markers (an EX-rule author may
          # include them for Step-7 enforcement; S24 prose fields are Step-9 guidance)
          bans = re.findall(r'(?:BANNED|VERIFIED DEFECT):\s*(.+)', content)
          learnings_bans.extend(bans)
          _loaded.append(os.path.basename(learn_file))
  print(f"S3-3 — learnings loaded for authoring bans: "
        f"{', '.join(_loaded) if _loaded else 'none'} "
        f"({len(learnings_bans)} BANNED/VERIFIED-DEFECT marker(s))")
  # learnings_bans added to quality gate checks during generation
  ```

## S3-2b — Load the style profile and PYQ index (v5.82 — GAP-2026-08-29-STYLE-FIDELITY §6.5.1)

  Loads two DATA artefacts written by Step 5. NEVER A STOP OF ANY KIND (P-4):
  every failure mode below resolves to DORMANT with a recorded reason, and a
  dormant run is byte-identical to the pre-v5.82 baseline (§8.6 proof 1).

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S3-2b (executable) ──────────────────────────────────────────────────
  import json, os, blueprint_core as bc

  def load_style_artefacts(exam_code, section_rules_meta, blueprint,
                           project_dir='/mnt/project'):
      """Returns (profile, index, style_meta). profile/index are None when
      dormant; style_meta always carries {status, reason, schema, corpus_hash}
      and is what §FOOTER-STYLE and the registry record."""
      def _dormant(reason):
          return None, None, {'status': 'DORMANT', 'reason': reason,
                              'schema': None, 'corpus_hash': None}
      # P-4 IS ABSOLUTE. Every shape below is validated, but a file on disk is
      # hostile input and the cost of being wrong once is a HALTED STEP. The
      # whole body therefore runs under a last-resort guard: an unanticipated
      # shape becomes DORMANT with the exception named, never a traceback.
      try:
          return _load_style_artefacts_inner(exam_code, section_rules_meta,
                                             blueprint, project_dir, _dormant)
      except Exception as e:
          return _dormant(f'unreadable_profile ({type(e).__name__})')


  def _load_style_artefacts_inner(exam_code, section_rules_meta, blueprint,
                                  project_dir, _dormant):
      p_path = os.path.join(project_dir, f'{exam_code}_style_profile.json')
      i_path = os.path.join(project_dir, f'{exam_code}_pyq_index.json')
      profile = index = None
      if os.path.exists(p_path):
          try:
              profile = json.load(open(p_path, encoding='utf-8'))
          except Exception as e:
              return _dormant(f'unreadable_profile ({type(e).__name__})')
      if os.path.exists(i_path):
          try:
              index = json.load(open(i_path, encoding='utf-8'))
          except Exception as e:
              index = None
      if profile is None:
          # EC-22: the blueprint EXPECTED a profile and it is gone — recorded,
          # never a stop.
          reason = ('absent_after_blueprint'
                    if (blueprint or {}).get('style_profile_expected')
                    else 'absent')
          return None, index, {'status': 'DORMANT', 'reason': reason,
                               'schema': None, 'corpus_hash': None}
      problems = bc.validate_style_profile(profile)
      if problems:
          return _dormant('schema_invalid: ' + '; '.join(problems[:2]))
      meta = profile.get('_meta')
      meta = meta if isinstance(meta, dict) else {}
      if meta.get('exam_code') != exam_code:
          return _dormant('exam_code_mismatch')
      sr_hash = (section_rules_meta or {}).get('corpus_hash')
      if sr_hash and meta.get('corpus_hash') != sr_hash:
          # EC-20 — one regeneration is the remedy; name BOTH files.
          return _dormant(f"stale_profile (style_profile corpus "
                          f"{str(meta.get('corpus_hash'))[:8]} != section_rules "
                          f"{str(sr_hash)[:8]})")
      paper = profile.get('paper')
      paper = paper if isinstance(paper, dict) else {}
      if str(paper.get('status', 'ACTIVE')).upper() == 'DORMANT':
          return _dormant(paper.get('dormant_reason') or 'thin_corpus')
      if index is not None and bc.validate_pyq_index(index):
          index = None                       # malformed index: dormant, profile stands
      if index is not None:
          i_meta = index.get('_meta')
          i_meta = i_meta if isinstance(i_meta, dict) else {}
          if (i_meta.get('exam_code') != exam_code
                  or (sr_hash and i_meta.get('corpus_hash') != sr_hash)):
              index = None
      return profile, index, {'status': 'ACTIVE', 'reason': None,
                              'schema': meta.get('schema', 1),
                              'corpus_hash': meta.get('corpus_hash')}
  ```

  RECORD style_meta INTO THE REGISTRY. At Final Assembly Step 7 calls
  pp.style_gate_record_paper(reg, paper_id, verdict, profile_meta=style_meta).
  Step 11 reads it back through pp.style_gate_profile_meta to print the single
  footer line (§FOOTER-STYLE); without this write the delivered footer is silent
  even on an ACTIVE profile. A later verdict update preserves it.

  S3-18 PRINTS one line for each (and the registry records style_meta):
    "STYLE PROFILE: ACTIVE (n=[questions], window=[years])" | "DORMANT: [reason]"
    "PYQ INDEX: [n] questions, loaded [t] s"                | "DORMANT: absent"

  EC-19 RESUME. batch_state.style_profile_hash pins the profile the paper
  STARTED on. When the file on disk differs at resume, the session CONTINUES on
  the FROZEN briefs and the frozen index snapshot; the difference is recorded in
  style_gate.events[] as `profile_changed_during_paper`. A paper that started
  DORMANT stays dormant to its Final Assembly even if a profile appears
  mid-paper — a paper is authored under ONE style regime or none.

  EC-25. When two profiles are otherwise equal, the one with the newer
  `generated_at` wins (PYQExplain having since added keys makes distractor_mix
  available where it was 'unavailable').

## S3-2e — QUALITY READINESS (v5.90 — GAP-2026-11-03 G10; owner decision OD-1: PURE STATUS QUO + LOUDER PRINT)

  WHY. On the incident run every quality control added since v5.82 — the style profile,
  the PYQ index, the content floor, the figural ask-type targets — lacked its input and ran
  DORMANT; the only trace was a footer line, and the paper shipped carrying the scheduled
  Hard labels. The V4 project even regenerated its blueprint after the release and got an
  EMPTY fig_ask_target_per_mock, silently. The owner's decision (OD-1, 2026-11-03) is that a
  missing input is NEVER a stop and has NO certification effect — the team guarantees the
  inputs. What changes is VISIBILITY: the state of every control is computed once, PRINTED
  before Q.1 as a block nobody can miss, and RECORDED on the paper (batch_state ->
  registry.question_index[].quality_readiness, the delivery footer, the audit's A-READINESS
  line and the bench card). Nothing here raises, ever.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S3-2e (executable; after S3-2b/S3-2D, before S3-3) ───────────────────────────
  import json, os, blueprint_core as bc
  _rd_in = {}
  for _art, _path in (('style_profile.json', f'/mnt/project/{EXAM}_style_profile.json'),
                      ('pyq_index.json', f'/mnt/project/{EXAM}_pyq_index.json'),
                      ('difficulty_profile.json', f'/mnt/project/{EXAM}_difficulty_profile.json')):
      try:
          _rd_in[_art] = json.load(open(_path, encoding='utf-8')) if os.path.exists(_path) else None
      except Exception:                                    # a corrupt file reads as STALE, never a stop
          _rd_in[_art] = {}
  # OD-11: the exemplar bank is a DELIVERED RUN FILE, attached beside the registry — never
  # project knowledge. Absent -> the judge is DORMANT (CHECK 3c (a) prints "no exemplar bank").
  _eb_candidates = [p for p in (f'/mnt/user-data/uploads/{EXAM}_exemplar_bank.json',   # attached to this run (OD-11)
                                f'/home/claude/{EXAM}_exemplar_bank.json',               # staged earlier this session
                                f'/mnt/project/{EXAM}_exemplar_bank.json') if os.path.exists(p)]   # kept in Project Files
  EXEMPLAR_BANK_PATH = _eb_candidates[0] if _eb_candidates else None
  try:
      EXEMPLAR_BANK = json.load(open(EXEMPLAR_BANK_PATH, encoding='utf-8')) if EXEMPLAR_BANK_PATH else {}
  except (OSError, ValueError):
      EXEMPLAR_BANK = {}                                      # unreadable bank = absent (dormant, printed)
  try:
      _rd_in['exemplar_bank.json'] = json.load(open(EXEMPLAR_BANK_PATH, encoding='utf-8')) if EXEMPLAR_BANK_PATH else None
  except Exception:
      _rd_in['exemplar_bank.json'] = {}
  _sr_path = f'/mnt/project/{EXAM}_section_rules.md'
  _rd_in['section_rules.md'] = open(_sr_path, encoding='utf-8').read() if os.path.exists(_sr_path) else None
  SECTION_RULES_TEXT = _rd_in['section_rules.md'] or ''        # read by S3-12d / S7-QUALITY / S13-2F
  _rd_in['blueprint.json'] = bp
  _pyq_n = None
  try:                                                     # R10.4 sparse mode, from the profile
      _pyq_n = sum(int((p or {}).get('q_scored') or 0) for p in ((_rd_in.get('difficulty_profile.json') or {}).get('papers') or {}).values()) or None
  except Exception:
      _pyq_n = None
  QUALITY_READINESS = bc.quality_readiness(_rd_in, pyq_items=_pyq_n)
  # A RESUMED paper reads the record S3-16 persisted (the controls that were active when
  # the paper STARTED are what its items were authored under — S4-12: READ, never
  # re-derived); a fresh paper records this run's measurement.
  _bs_rd = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  if os.path.exists(_bs_rd):
      try:
          _prev_rd = json.load(open(_bs_rd, encoding='utf-8')).get('quality_readiness')
      except (OSError, ValueError):
          _prev_rd = None
      if isinstance(_prev_rd, dict) and _prev_rd.get('controls'):
          QUALITY_READINESS = _prev_rd
          print(f"S3-2e: readiness record READ from batch_state (resumed paper; degraded: {_prev_rd.get('degraded') or 'none'}).")
  print(bc.quality_readiness_block(QUALITY_READINESS))     # the LOUD print — before Q.1, every run
  # QUALITY_READINESS is persisted by the batch_state initialiser (S3-16 'quality_readiness').
  QUALITY_DEGRADED = list(QUALITY_READINESS.get('degraded') or [])
  QUALITY_FOOTER_LINE = bc.degraded_footer_line(QUALITY_READINESS)   # -> DeliveryFooter §2B
  ```
  RULES. (1) The block prints on EVERY run, PASS or not. (2) DEGRADED is a list of control
  ids; each DORMANT control still reports its state on every item it would have judged
  (DORMANT(reason), §4.3) — never silence. (3) A control that is N/A(sparse) is not degraded
  (R10.4). (4) No `[HS:INPUT]` for a quality input exists in this spec (owner decision OD-1);
  the only input stops remain the pre-existing structural ones (blueprint / registry /
  engine absent, L6). (5) v5.92 (GAP-2026-11-05 DL-46): field presence is NOT readiness.
  `bc.quality_readiness` reports G-DIFF-FLOOR as PASS only when the profile holds at least
  `bc.LEVEL_MIN_POOL` content-full records, DORMANT below that, and N/A when the profile
  carries no transcribed content at all (a text-only exam; no remedy is asked). An N/A or
  DORMANT control is NEVER printed as ACTIVE: the block names the controls that are not
  measuring. A paper that carries drawn chemistry while the level model is dormant gets the
  AMBER footer line `DIFFICULTY UNVERIFIED — <reason>` (bc.difficulty_unverified_lines,
  S13-6) — printed, recorded, never a stop, never a certification effect.

## S3-3 — Load section_rules.md — read ALL fields

  (Unchanged from v1.0 — see §3 S3-3 in v1.0 spec for full field list)

  Parse EXAM_STRUCTURE header block; per-section blocks; per-subtopic blocks.
  Regex: locate '--- Subtopic: [re.escape(S)] ---', stop at next '--- Subtopic:'
  or '=== SECTION:'.

  ALSO EXTRACT (used by S7-20, S7-21):
    Per-section content-ban directives (e.g. easy-ban types for a fact-recall section)
    Per-section mandatory-area/topic directives (ALL declared — count is data, never fixed)
    Per-section cluster-ban directives (adjacency constraints for a language section)
    All read by section name from section_rules.md; empty ⇒ vacuous no-op.

## S3-4 — Load registry.json — integrity check (non-blocking)

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import re as _re_pid
  reg = json.load(open(f'/home/claude/{EXAM}_registry.json'))

  # C2 (v5.21): UNIVERSAL paper identity. paper_id comes from THIS paper's blueprint.mocks[]
  # entry (C1/Blueprint v1.29 added it); fallback "MOCK:M{N:02d}" for pre-C1 blueprints.
  # paper_index = its numeric suffix (mock → == N; scoped "SUBJ:Physics:03" → 3), used only for
  # the window index. For a mock, paper_id == "MOCK:M{N:02d}" and paper_index == N, so EVERY
  # downstream value (window, filename, registry integers) is bit-identical to pre-C2.
  _this_paper = next((mk for mk in bp.get('mocks', []) if mk.get('mock') == N), None)
  paper_id    = (_this_paper or {}).get('paper_id', f"MOCK:M{N:02d}")
  paper_index = int(_re_pid.sub(r'\D', '', paper_id.rsplit(':', 1)[-1]) or N)

  # papers_completed is the generalised paper-identity ledger (C1); mocks_completed retained
  # for backward-compatibility (a legacy registry falls back to it).
  mocks_done   = reg.get('mocks_completed', [])
  papers_done  = reg.get('papers_completed', mocks_done)
  q_hashes     = reg.get('question_hashes', [])
  expected_cnt = len(papers_done) * total_questions

  # v5.14 THREE-AXIS: the WINDOW-level Axis-2 counts live in the registry (cross-mock;
  # batch_state.json is per-mock and cannot span a 10-mock window). Read the current
  # window's running counts; RESET when this paper opens a new window.
  _win = bp.get('batch_size_qs', 10)
  _cur_window = (paper_index - 1) // max(1, _win)   # C2: paper_index (== N for a mock)
  _reg_axis = reg.get('axis2_window', {})            # {'window': int, 'sections': {sec: {counts,...}}}
  if _reg_axis.get('window') != _cur_window:
      axis2_window_counts = {}                        # new window → fresh counts
  else:
      axis2_window_counts = dict(_reg_axis.get('sections', {}))
  # axis2_window_counts[section] = {'counts': {...}, 'neg_count': int, 'total': int}
  # Trackers are built per section from this + blueprint axis_schedule (see S7-AXIS), mutated
  # during generation, and committed back to reg['axis2_window'] at Final Assembly (S13-4).

  # NON-BLOCKING — inconsistent registry → WARN, proceed with dedup_partition:
  if len(q_hashes) != expected_cnt:
      print(f"WARN: Registry inconsistent ({len(q_hashes)} hashes, "
            f"expected {expected_cnt}). G-DUP will be environment-WARN only.")

  # INITIALISE pending_registry (v2.0 GAP-19 fix — explicit init here):
  pending_registry = {
      'question_hashes': [],
      'stem_texts': [],
      'semantic_tuples': [],
      'semantic_usage': [],
      'image_phashes': [],
      'image_sources_used': [],
      'ga_facts_used': [],
      'passage_topics': [],
      'cloze_topics': [],
      'vocab_words_used': [],
      'idioms_used': [],
      'grammar_rules_used': [],
      'computer_facts': [],
      'numeric_seeds': [],
      'analogy_schemes': [],
      'cause_effect_domains': [],
      'syllogism_domains': [],
      'option_sets': [],
  }
  # pending_registry commits to registry ONLY at Final Assembly (S13-4).
  # All dedup additions during generation go here, NEVER to registry directly.
  ```

## S3-5 — Registry snapshot

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  shutil.copy(f'/home/claude/{EXAM}_registry.json',
              f'/home/claude/{EXAM}_registry_snapshot.json')
  registry_snapshot = json.load(open(f'/home/claude/{EXAM}_registry_snapshot.json'))

  # D (v5.23): build an IN-MEMORY dedup index PARTITIONED by subtopic_id, so a lookup for a
  # subtopic scans only that subtopic's prior entries — O(shard) instead of O(all) — which
  # bounds cost for large exams (100k+ questions). CORRECTNESS-NEUTRAL: the stored registry is
  # UNCHANGED (flat lists), and only the naturally subtopic-keyed fields are indexed
  # (semantic_usage keyed by 'subtopic_id'; semantic_tuples keyed by their first element,
  # [subtopic, approach, values]). L1 (question_hashes / stem_texts) stays GLOBAL — a verbatim
  # duplicate must be caught across subtopics, so it is deliberately NOT sharded.
  def _build_subtopic_index(snap):
      idx = {'semantic_usage': {}, 'semantic_tuples': {}}
      for u in snap.get('semantic_usage', []):
          idx['semantic_usage'].setdefault(u.get('subtopic_id'), []).append(u)
      for t in snap.get('semantic_tuples', []):
          sid = (t[0] if isinstance(t, (list, tuple)) and t else
                 (t.get('subtopic') if isinstance(t, dict) else None))
          idx['semantic_tuples'].setdefault(sid, []).append(t)
      return idx

  SUBTOPIC_INDEX = _build_subtopic_index(registry_snapshot)

  def subtopic_usage(snap, sid):
      """D: prior semantic_usage for ONE subtopic, from the index when available (built from
      this same snap), else an O(n) filter — identical membership either way."""
      if snap is registry_snapshot:
          return SUBTOPIC_INDEX['semantic_usage'].get(sid, [])
      return [u for u in snap.get('semantic_usage', []) if u.get('subtopic_id') == sid]
  ```
  Guard script uses snapshot. Live registry never modified during generation.

  ### S3-5b — EC-29: like-for-like L2 across the switchover (v5.82)

  A series already in progress carries registry `semantic_tuples` whose second
  element is the LEGACY `approach` string; questions written from v5.82 carry
  `mechanic|form|polarity`. Comparing the two shapes directly would silently
  stop detecting semantic repeats at exactly the mock where the switchover
  happened — the failure would look like "no duplicates found", which is the
  worst shape a dedup failure can take.

  At S3-5, for every legacy entry, RECOMPUTE the new shape IN MEMORY from the
  entry's stored `stem_texts`, using the same measurement functions Step 5 uses
  (never a second implementation). The stored `registry.json` is NEVER rewritten
  — S13-4 remains the single writer, and Final Assembly commits new entries in
  the NEW shape only.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S3-5b (executable) ──────────────────────────────────────────────────
  import analyse_engine as ae

  _LEGACY_APPROACHES = set()          # any non-'a|b|c' second element is legacy

  def _is_new_shape(tup):
      mid = tup[1] if isinstance(tup, (list, tuple)) and len(tup) > 1 else None
      return isinstance(mid, str) and mid.count('|') == 2

  def upgrade_legacy_tuples(snapshot, stem_by_key=None):
      """Return a NEW list of semantic tuples in the v5.82 shape. Legacy entries
      are recomputed from their stem text; entries already in the new shape pass
      through untouched. Pure — `snapshot` is never mutated."""
      out, upgraded, unrecoverable = [], 0, 0
      for t in snapshot.get('semantic_tuples', []) or []:
          if not isinstance(t, (list, tuple)) or len(t) < 3 or _is_new_shape(t):
              out.append(t)
              continue
          stem = (stem_by_key or {}).get(tuple(t[:1]) + (t[2] if isinstance(t[2], str)
                                                         else '',))
          if not stem:
              # No stored stem for this entry: keep the legacy tuple AS-IS.
              # A tuple that cannot be recomputed still matches its own kind,
              # so the loss is confined to cross-shape comparison and is
              # RECORDED rather than papered over with a fabricated mechanic.
              out.append(t)
              unrecoverable += 1
              continue
          q = {'stem': stem, 'options': [], 'medium': 'en'}
          q['axis2'] = ae.classify_axis2(q)
          q['option_shape'] = ae.detect_option_shape(q)
          mech = ae.detect_mechanic(q)
          pol = 'negative' if ae._POLARITY_RE.search(stem) else 'positive'
          out.append([t[0], f"{mech}|{q['axis2']}|{pol}", t[2]])
          upgraded += 1
      return out, {'upgraded': upgraded, 'unrecoverable': unrecoverable}
  ```

  RECORDED at S3-18: "L2 legacy tuples upgraded in memory: [n] ([u] without a
  stored stem, compared in their own shape)." Never a stop.

## S3-6 — ExamCode cross-verification

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  bp_code  = bp['exam_code']
  reg_code = reg.get('exam_code', bp_code)
  assert bp_code == EXAM, \
      f"HARD STOP [HS:INFRA]: trigger ExamCode '{EXAM}' != blueprint '{bp_code}'"
  assert bp_code == reg_code, \
      f"HARD STOP [HS:INFRA]: blueprint exam_code '{bp_code}' != registry '{reg_code}'"
  ```

## S3-7 — Blueprint version compatibility check

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # v5.6: minimum-version check uses TUPLE comparison (not string) so "1.10" > "1.7"
  # is correct. v1.7 is the floor (subtopic_id contract); any version >= 1.7 is accepted.
  MIN_BLUEPRINT_VERSION = (1, 7)
  def _ver_tuple(v):
      """Parse a version string like '1.7' or '1.14' into a comparable tuple."""
      try:
          return tuple(int(x) for x in str(v).split('.'))
      except (ValueError, AttributeError):
          return (0,)
  if _ver_tuple(blueprint_version) < MIN_BLUEPRINT_VERSION:
      raise SystemExit(
          f"HARD STOP [HS:INPUT]: blueprint_version '{blueprint_version}' < minimum "
          f"'{'.'.join(str(x) for x in MIN_BLUEPRINT_VERSION)}'. "
          f"Regenerate the blueprint with Framework_Blueprint v1.7+ (subtopic_id contract required).")
  ```

## S3-8 — Subtopic join via subtopic_id (v3.4 — CONTRACT GATE, replaces string-match)

  v3.4 CHANGE: Step 7 no longer matches subtopics by display-name string. It
  joins blueprint ↔ section_rules ON subtopic_id, the stable key minted by Step 0.
  This permanently fixes the ~70% name-mismatch that caused false "subtopic
  unrecognised" and false "mandatory subtopic absent" hard stops.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # Load the Step 0 manifest (authoritative id registry). REQUIRED.
  manifest_path = f'/home/claude/{EXAM}_subtopic_manifest.json'
  if not os.path.exists(manifest_path):
      # Try project dir as a fallback location
      alt = f'/mnt/project/{EXAM}_subtopic_manifest.json'
      if os.path.exists(alt):
          shutil.copy(alt, manifest_path)
  if not os.path.exists(manifest_path):
      raise SystemExit(
          f"HARD STOP [HS:INPUT] (S3-8 contract): {EXAM}_subtopic_manifest.json not found. "
          f"Step 0 publishes it and the user uploads it to the {EXAM} project "
          f"Files section alongside section_rules.md. Upload it, then retry.")
  manifest = json.load(open(manifest_path, encoding='utf-8'))
  MANIFEST_IDS = manifest['subtopics']           # id -> {display_name, section, ...}

  # Build the section_rules id index: parse subtopic_id: from each block.
  # (Step 0 v2.4+ writes 'subtopic_id:' as the first field of every block.)
  sr_block_ids = set(re.findall(r'^subtopic_id:\s*(\S+)\s*$', sr_text, re.MULTILINE))

  # CONTRACT GATE — every blueprint id must exist in BOTH the manifest AND
  # section_rules. A missing id = HARD STOP [HS:INPUT] naming the exact id (no silent fallback).
  contract_failures = []
  legacy_blueprint = False
  for sec_name, id_map in alloc_ids.items():
      for sid in id_map:
          if sid is None:
              legacy_blueprint = True
              continue
          if sid not in MANIFEST_IDS:
              contract_failures.append(f"{sid}  (not in manifest)")
          elif sid not in sr_block_ids:
              contract_failures.append(f"{sid}  (in manifest, missing from section_rules)")

  if legacy_blueprint:
      raise SystemExit(
          "HARD STOP [HS:INPUT] (S3-8 contract): this blueprint has subtopic_allocations "
          "without 'subtopic_id'. It predates the v1.7 contract. Regenerate the "
          "blueprint with Framework_Blueprint v1.7+ (which reads the Step 0 "
          "manifest and emits subtopic_id), OR run the one-time migration to add "
          "ids. Step 7 will not string-match — it requires ids.")
  if contract_failures:
      raise SystemExit(
          "HARD STOP [HS:INPUT] (S3-8 contract): these blueprint subtopic_ids are not "
          "joinable. Re-run Step 0 (manifest+section_rules) and/or Step 1 so all "
          "three agree:\n  - " + "\n  - ".join(sorted(set(contract_failures))))

  # Past the gate: every id joins cleanly. Resolve each id to its section_rules
  # block for pattern guidance (the join itself — no string matching anywhere).
  def sr_block_for_id(sid):
      # Split section_rules into subtopic blocks; return the block whose
      # 'subtopic_id:' line equals sid. This is the join (id → pattern block).
      blocks = re.split(r'\n--- Subtopic:', sr_text)
      for b in blocks:
          if re.search(r'^\s*subtopic_id:\s*' + re.escape(sid) + r'\s*$', b, re.MULTILINE):
              return b
      return None
  ```

  NOTE: sr_block_ids (built above via re.findall) and sr_block_for_id() both key
  on the SAME 'subtopic_id:' line that Step 0 emits as the first field of every
  block. The contract gate guarantees every blueprint id is in sr_block_ids
  before any sr_block_for_id() lookup runs, so a None return is impossible here.

  RESULT: alloc_ids[section][subtopic_id] is the authoritative allocation; each id
  resolves to exactly one section_rules block via sr_block_for_id(). The old
  name-based mismatch list is gone — joins are exact by construction.

## S3-8L — ORGANIC DECISION-LOAD RULER (v5.94 — GAP-2026-11-07; owner D1 (b), D2, D3, D4, D5, D6, Q1 (c), Q4)

  Runs after S3-8 (it needs MANIFEST_IDS and `reg` from S3-4) on EVERY exam (the TARGET plan and
  the pattern sources are drawn later, at S3-15L, from the FINAL plan — after S3-12e has placed the
  top-band slots). The organic ruler L2 — built ONLY when the paper has a subtopic the exam's
  taxonomy files under organic chemistry (bc.l2_scope_ids over the manifest; owner Q4: every other
  subject keeps the generic layer only, and this block then leaves L2_MODEL None). The level of
  difficulty comes from the exam's OWN past papers, never from the exam's type or degree (D5): the
  pool is the profile window, the band SHARES are the Step-5 BLIND GRADES of the SAME profile
  (exemplar bank, S3-2e; sha256-checked), else the registry's cached grades for that sha256, else
  the blueprint's measured shares — the source is printed. Within a series the cut-offs are FROZEN
  (D2): a later paper on the same scope, profile and vocabulary reuses the frozen model, unless
  blind grades now exist and the frozen model had none. Never a stop.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S3-8L (v5.94) ──
  import hashlib as _h_l2, json as _json_l2, os as _os_l2
  import blueprint_core as bc
  _bs_l2_path = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _bs_l2 = {}
  if _os_l2.path.exists(_bs_l2_path):
      try:
          _bs_l2 = _json_l2.load(open(_bs_l2_path, encoding='utf-8')) or {}
      except (OSError, ValueError):
          _bs_l2 = {}
  _same_paper_l2 = bool(_bs_l2) and _bs_l2.get('paper_id') == (globals().get('_pid_dp') or paper_id)
  L2_MODEL, L2_CARDS, L2_ORGANIC_IDS, L2_SCOPE_IDS = None, [], [], []
  L2_PYQ_GRADES_RECORD = None                     # S13-4 caches it in the registry (fresh bank grades only)
  _dp_l2 = globals().get('DIFFICULTY_PROFILE')
  if globals().get('difficulty_plan') and isinstance(_dp_l2, dict):
      L2_ORGANIC_IDS = bc.l2_scope_ids(MANIFEST_IDS, organic_subtopics=(globals().get('OP_SCOPE') or {}).get('organic_subtopics'))
      _org_set = set(L2_ORGANIC_IDS)
      L2_SCOPE_IDS = sorted({str(x.get('subtopic_id')) for x in subtopic_list
                             if str(x.get('subtopic_id')) in _org_set})
  if L2_SCOPE_IDS:
      try:
          _sha_l2 = _h_l2.sha256(open(f'/mnt/project/{EXAM}_difficulty_profile.json', 'rb').read()).hexdigest()
      except OSError:
          _sha_l2 = None
      _g_l2, _gst_l2 = bc.bank_pyq_grades(globals().get('EXEMPLAR_BANK') or {}, _sha_l2, difficulty_labels)
      _gsrc_l2 = 'Step-5 blind grades (exemplar bank)' if _g_l2 else None
      if _g_l2:
          L2_PYQ_GRADES_RECORD = bc.pyq_grades_record(_sha_l2, difficulty_labels, _g_l2, source='step5-blind')
      else:
          _g_l2 = bc.pyq_grades_from_registry(reg, _sha_l2, difficulty_labels)
          _gsrc_l2 = 'blind grades cached in the registry' if _g_l2 else None
      if _gst_l2 == 'stale':
          print("S3-8L: the attached exemplar bank was built from an OLDER difficulty profile — its grades "
                "are not used (re-run MockTestAnalyse to grade the current profile; informational).")
      _ds_l2 = bp.get('difficulty_source') if isinstance(bp.get('difficulty_source'), dict) else {}
      _lmi_l2 = bp.get('level_model_inputs') if isinstance(bp.get('level_model_inputs'), dict) else {}
      _mp_l2 = _lmi_l2.get('measured_pct') if _lmi_l2 else _ds_l2.get('measured_pct')
      _gap_l2 = (globals().get('PROFILE_CFG') or {}).get('cycle_gap_days')
      # series freeze: this paper's resumed state first, then the latest committed paper of the series
      _prev_l2 = (_bs_l2.get('difficulty_state') or {}).get('l2_model') if _same_paper_l2 else None
      if not isinstance(_prev_l2, dict):
          for _qe_l2 in reversed(reg.get('question_index') or []):
              _c_l2 = ((_qe_l2 or {}).get('difficulty_state') or {}).get('l2_model') if isinstance(_qe_l2, dict) else None
              if isinstance(_c_l2, dict) and _c_l2.get('frozen'):
                  _prev_l2 = _c_l2
                  break
      _fz = (_prev_l2 or {}).get('frozen') if isinstance(_prev_l2, dict) else None
      _reuse = (isinstance(_fz, dict) and _prev_l2.get('profile_sha256') == _sha_l2
                and sorted((_fz.get('inputs') or {}).get('subtopic_ids') or []) == L2_SCOPE_IDS
                and (_fz.get('shares_source') == 'pyq_grades' or not _g_l2))
      L2_MODEL = bc.l2_model_from_frozen(_fz) if _reuse else None
      if L2_MODEL:
          print(f"S3-8L: L2 ruler REUSED from the series (frozen cut-offs {L2_MODEL.get('cuts_list')}, "
                f"shares from {L2_MODEL.get('shares_source')}) — identical scoring across the series.")
      else:
          L2_MODEL = bc.l2_model_for_scope(_dp_l2, L2_SCOPE_IDS, difficulty_labels,
                                           pyq_grades=_g_l2 or None, measured_pct=_mp_l2,
                                           gap_days=_gap_l2, organic_ids=L2_ORGANIC_IDS)
      L2_CARDS = bc.l2_cards(_dp_l2, L2_MODEL, difficulty_labels, gap_days=_gap_l2)
      DIFFICULTY_STATE['l2_model'] = {
          'active': bool(L2_MODEL.get('active')), 'binding': bool(L2_MODEL.get('binding')), 'mode': L2_MODEL.get('mode'),
          'n': L2_MODEL.get('n'), 'reason': L2_MODEL.get('reason'), 'shares_source': L2_MODEL.get('shares_source'),
          'grades_source': _gsrc_l2 or ('blueprint measured shares' if _mp_l2 else None),
          'vocab_coverage': L2_MODEL.get('vocab_coverage'), 'scope_ids': list(L2_SCOPE_IDS),
          'profile_sha256': _sha_l2, 'frozen': bc.l2_frozen(L2_MODEL)}
      _sup_l2 = bc.l2_hard_supply(L2_CARDS, difficulty_labels)
      if L2_MODEL.get('active'):
          print(f"S3-8L: L2 ruler {'BINDING' if L2_MODEL.get('binding') else 'ADVISORY (concept coverage below floor)'} — "
                f"{len(L2_SCOPE_IDS)} organic subtopic(s), pool n={L2_MODEL.get('n')}, shares from "
                f"{L2_MODEL.get('shares_source')} ({DIFFICULTY_STATE['l2_model']['grades_source'] or 'stored bands'}); "
                f"pattern cards by band {_sup_l2}")
      else:
          print(f"S3-8L: L2 ruler DORMANT — {L2_MODEL.get('reason')}; organic items use the generic layer")
  elif L2_ORGANIC_IDS or globals().get('difficulty_plan'):
      print("S3-8L: no organic subtopic in this paper's scope — generic difficulty layer only (owner Q4).")
  ```

## S3-9 — Section allocation sum verification

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  for section in sections:
      sec_name = section['name']
      expected = section['total_qs']
      actual   = sum(allocations.get(sec_name, {}).values())
      if actual != expected:
          raise SystemExit(
              f"HARD STOP [HS:INPUT]: Section '{sec_name}' allocations sum={actual}, "
              f"expected={expected}. Blueprint may be corrupt or wrong mock.")
  ```

## S3-10 — Audit script self-test (Layer 2 — when audit.py exists)

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  if AUDIT_AVAILABLE:
      import subprocess
      result = subprocess.run(
          ['python3', f'/home/claude/{EXAM}_mock_test_audit.py', '--self-test'],
          capture_output=True, text=True, env=AUDIT_ENV          # S3-9: engines importable
      )
      if result.returncode != 0 or 'SELF-TEST: ABORT' in (result.stdout or ''):
          raise SystemExit(
              f"HARD STOP [HS:INFRA]: Audit script self-test failed or ABORTED (engines not importable "
              f"by the per-exam copy — AUDIT_ENV/ENGINE_ROOT from S3-9 must point at the "
              f"verified clone).\n{result.stdout}\n{result.stderr}")
      print(f"Audit script self-test: {result.stdout.strip()}")
  else:
      print("Audit script not available. Manual gate checklist (S4-11) will be used.")
  ```

## S3-11 — Read structural changes and deprecated formats

  From STRUCTURAL_CHANGES_BY_YEAR and DEPRECATED_FORMAT flags in section_rules.md.
  Build `deprecated_formats = {subtopic: [format_types]}` dict.
  Store ALL FIGURAL_BANNED flags (per-section and per-subtopic).

  v5.13 — FIGURAL_BANNED ↔ REPLACEMENT_RULE consistency (HS-16):
  After storing FIGURAL_BANNED flags, for each subtopic allocated in this
  mock where FIGURAL_BANNED is True, verify that section_rules contains a
  REPLACEMENT_RULE entry for it, pointing to a valid format=TEXT
  subtopic_id (in the same section, or in any section if the entire
  section is FIGURAL_BANNED). If REPLACEMENT_RULE is missing, empty, or
  points to a nonexistent subtopic_id → HS-16 HARD STOP [HS:INPUT]:
  "FIGURAL_BANNED subtopic [id] has no valid REPLACEMENT_RULE. S7-NEW-B
  OPTION B replacement will fail. Add REPLACEMENT_RULE to section_rules
  before proceeding."
  If no subtopic in this mock has FIGURAL_BANNED: skip silently.

## S3-12 — Read none_of_above_permitted per section

  `none_of_above_map = {section_name: bool}` — default False if not found.
  v4.2 — this map is no longer read-only: gate G-OPTREF (S12-NEW-15) and rule
  R-OPTREF use it to ENFORCE that any stem referencing a terminal/escape option
  ("None of these", "No error → last option", "No improvement", "All/Both/Neither")
  actually contains that option, and only where the section permits it. Also read
  any per-section/per-subtopic escape-token wording from section_rules (exam-
  agnostic) so G-OPTREF matches the exam's own phrasing.

## S3-12b — Build the placement plan (subtopic → question number) — v5.77, MANDATORY

  (GAP-2026-08-28-PLACEMENT-UNSPECIFIED. The gap report names this step
  "S3-2b"; it is numbered S3-12b here because its inputs — mock_entry from
  S3-2, MANIFEST_IDS from S3-8, paper_index from S3-4 — do not exist before
  S3-8, and it MUST precede S3-13: on an exam without position-based typing
  the answer budget's MSQ/NAT exclusions are derived from this plan.)

  Runs for EVERY exam and EVERY paper, fresh or resumed. Not informational.
  This is the single authoritative source of "which subtopic is Q.N"; every
  consumer (S3-13 budget, S3-18 manifest, S7 generation, S13 question_index)
  READS it and none recomputes it.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # Subtopic metadata for placement — from the S3-8 manifest join. Every field
  # optional; §7.3 degradation applies inside the engine (absent concept_group
  # -> subtopic_id; absent family/subject -> that objective dormant; a garbage
  # linked_group_size -> 1). linked_group_size is read from MANIFEST_IDS by
  # the engine itself via this meta — no separate groups map to keep in sync.
  _meta_q = {}
  for _sec in mock_entry.get('sections', []):
      for _sa in _sec.get('subtopic_allocations', []):
          _msid = _sa.get('subtopic_id')
          if not _msid:
              continue
          _mrec = MANIFEST_IDS.get(_msid, {})
          _meta_q[_msid] = {'concept_group': _mrec.get('concept_group'),
                            'presentation_family': _mrec.get('presentation_family'),
                            'subject': _mrec.get('section'),
                            'linked_group_size': _mrec.get('linked_group_size')}

  def _alloc_for(_sec_entry):
      # SUM the RAW blueprint entries (E20): S3-2's alloc_ids is keyed by
      # subtopic_id and therefore collapses duplicate allocation entries BY
      # OVERWRITE — a blueprint carrying two entries for one id in one section
      # would silently lose the first q_count there, and the loss would
      # surface here as a misleading "allocation impossible" stop. Summing the
      # raw list is exact for well-formed and duplicate-carrying blueprints
      # alike (HS-2 already verified the raw sums against section sizes).
      _a = {}
      for _sa in _sec_entry.get('subtopic_allocations', []):
          _asid = _sa.get('subtopic_id')
          if _asid:
              _a[_asid] = _a.get(_asid, 0) + int(_sa.get('q_count', 0) or 0)
      return _a

  _sec_entry_by_name = {s.get('section_name'): s
                        for s in mock_entry.get('sections', [])}

  bs_prev = {}
  _bs_path = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  if os.path.exists(_bs_path):
      bs_prev = json.load(open(_bs_path))

  # v5.85 (GAP-2026-09-21-LINKED-PLACEMENT) — stimulus groups. STIM_ACTIVE is True
  # ONLY for a paper whose plan was built with the stimulus profile (fresh branch
  # below, or its frozen resume). A paper started before the profile existed —
  # frozen or pre-v5.77 — stays on the legacy path to the end, byte-for-byte.
  STIM_ACTIVE = False
  STIM_PLAN = {}          # {group_id: {'type','qnums','members','stimulus','stimulus_sha256'}}
  STIM_GID_BY_Q = {}      # {qnum: group_id} — members only
  STIM_PROFILE = None     # the profile THIS paper was planned with (frozen snapshot)
  # The auditor reads the SNAPSHOT, never the live project file: a profile rebuilt
  # later (new PYQs) must not make an older, correctly built paper look wrong.
  STIM_PROFILE_PATH = f'/home/claude/{EXAM}_M{N}_stimulus_profile.json'

  def _stim_load_profile():
      """SAFETY LOCK + validation. Chat attachment wins over Project Files. Without
      a profile a NEW paper would scatter every question set (one passage printed at
      many positions). An exam with no sets has a valid profile with "types": {}."""
      _sgp = next((f'{_d}/{EXAM}_stimulus_profile.json'
                   for _d in ('/mnt/user-data/uploads', '/mnt/project')
                   if os.path.exists(f'{_d}/{EXAM}_stimulus_profile.json')), None)
      if _sgp is None:
          raise SystemExit(
              f"HARD STOP [HS:INPUT] (S3-12b SAFETY LOCK, v5.85): {EXAM}_stimulus_profile.json "
              f"is not in Project Files. Run PYQExtract --stimulus-profile first (it "
              f"needs {EXAM}_analysis_progress.json), upload the file it delivers, and "
              f"re-run. A paper already in progress is not affected by this lock.")
      try:
          _prof = json.load(open(_sgp, encoding='utf-8'))
      except (OSError, ValueError) as _e:
          raise SystemExit(f"HARD STOP [HS:INPUT] (S3-12b): {os.path.basename(_sgp)} is not readable "
                           f"JSON ({_e}). Re-run PYQExtract --stimulus-profile and "
                           f"replace the file.")
      # v5.87 (GAP-2026-10-27-SCOPED-STIMULUS-SECTIONS): the profile is EXAM-wide
      # (Step 5 measures every section), so its exam_section values are checked
      # against the EXAM's sections — the section set of the Step-5 manifest, which
      # is the same source the profile was built from — never against `sections`,
      # which for a SUBJ/TOPIC/SUBTOPIC paper holds only the scoped section(s).
      # Before v5.87 every scoped paper of a multi-section exam whose profile
      # carried a set type in another section HARD STOPPED [HS:PROSE] here. A mock paper
      # (sections == every exam section) is byte-identical in effect.
      _exam_sections = sorted({_r.get('section') for _r in MANIFEST_IDS.values()
                               if isinstance(_r, dict) and _r.get('section')}
                              | {_s['name'] for _s in sections})
      _probs = bc.validate_stimulus_profile(
          _prof, exam_code=EXAM, manifest={'subtopics': MANIFEST_IDS},
          section_names=_exam_sections)
      if _probs:
          raise SystemExit(f"HARD STOP [HS:INPUT] (S3-12b): {os.path.basename(_sgp)} does not fit "
                           f"this exam — " + '; '.join(_probs) + ". Re-run PYQExtract "
                           "--stimulus-profile (after any taxonomy change) and replace "
                           "the file.")
      return _prof

  def _stim_build_plan(_prof):
      """The set-aware plan: sets composed from the blueprint's allocation, placed
      as consecutive blocks. Deterministic (same profile + allocation + seed →
      identical plan), which is what lets a lost batch_state be rebuilt exactly."""
      _sbq, _prep, _plan, _gbq = {}, {}, {}, {}
      for _s in sections:
          _alloc_q = _alloc_for(_sec_entry_by_name.get(_s['name'], {}))
          _sg_groups, _sg_notes = bc.compose_stimulus_groups(_alloc_q, _s['name'], _prof)
          for _n in _sg_notes:
              print(f"S3-12b SETS — section '{_s['name']}': {_n}")
          try:
              _pl, _rp, _gm = bc.place_with_stimulus_groups(
                  _alloc_q, tuple(_s['q_range']), _meta_q, _sg_groups, _prof,
                  seed=paper_index)
          except bc.PlacementError as _e:
              raise SystemExit(f"HARD STOP [HS:INPUT] (S3-12b): section '{_s['name']}': "
                               f"{_e} — the blueprint allocation is "
                               f"structurally impossible for this section; "
                               f"fix it at MockBlueprint, never by dropping "
                               f"a question here.")
          _sbq.update(_pl)
          _prep[_s['name']] = _rp
          _gbq.update(_gm)
          for _g in _sg_groups:
              _qn = sorted(q for q, x in _gm.items() if x == _g['group_id'])
              _plan[_g['group_id']] = {'type': _g['type'], 'members': list(_g['members']),
                                       'qnums': _qn, 'stimulus': None,
                                       'stimulus_sha256': None}
              print(f"S3-12b SET {_g['group_id']}: Q.{_qn[0]}-Q.{_qn[-1]} "
                    f"({len(_g['members'])} questions, one shared stimulus)")
      return _sbq, _prep, _plan, _gbq

  def _stim_cmap_state():
      """What the answer_key concept_map says about this paper: 'none' (nothing
      authored), 'set' (SET-PLACED — S7-NEW-A writes stimulus_group_id only on
      those) or 'legacy' (questions authored before the profile existed)."""
      _p = f'/home/claude/{EXAM}_M{N}_answer_key.json'
      if not os.path.exists(_p):
          return 'none'
      _cm = json.load(open(_p, encoding='utf-8')).get('concept_map') or {}
      if not _cm:
          return 'none'
      return ('set' if any('stimulus_group_id' in (_r or {}) for _r in _cm.values())
              else 'legacy')

  def _stim_cmap_marked():
      return _stim_cmap_state() == 'set'

  if bs_prev.get('subtopic_by_qnum') and bs_prev.get('batches_completed'):
      # ── FROZEN (v5.77+ state): the plan was persisted at S3-16. Read it. ──
      subtopic_by_qnum = {int(k): v
                          for k, v in bs_prev['subtopic_by_qnum'].items()}
      placement_report = bs_prev.get('placement_report') or {}
      if 'stimulus_groups' in bs_prev:
          STIM_ACTIVE = True
          STIM_PLAN = bs_prev['stimulus_groups'] or {}
          STIM_PROFILE = bs_prev.get('stimulus_profile_snapshot') or _stim_load_profile()
          for _sgid, _sgrec in STIM_PLAN.items():
              for _sgq in _sgrec['qnums']:
                  STIM_GID_BY_Q[int(_sgq)] = _sgid
      if not placement_report:
          # belt: state written with a plan but no report — audit, never rebuild.
          placement_report = bc.sg_audit_placement(subtopic_by_qnum, sections,
                                                   _meta_q, STIM_GID_BY_Q)

  elif bs_prev.get('batches_completed') and _stim_cmap_marked():
      # ── v5.85 SET-PLACED PAPER WHOSE batch_state LOST ITS PLAN (S4-12 step 2
      # rebuilt it from the docx). The plan is DETERMINISTIC, so it is rebuilt from
      # the profile and PROVEN against every authored question before it is used;
      # any disagreement (e.g. the profile was replaced meanwhile) is a HARD STOP [HS:INFRA] —
      # re-placing authored questions is never an option.
      STIM_PROFILE = _stim_load_profile()
      subtopic_by_qnum, placement_report, STIM_PLAN, STIM_GID_BY_Q = \
          _stim_build_plan(STIM_PROFILE)
      _cm_rb = json.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json',
                              encoding='utf-8')).get('concept_map') or {}
      _bad_rb = [int(_q) for _q, _r in _cm_rb.items()
                 if subtopic_by_qnum.get(int(_q)) != (_r or {}).get('subtopic_id')
                 or STIM_GID_BY_Q.get(int(_q)) != (_r or {}).get('stimulus_group_id')]
      if _bad_rb:
          raise SystemExit(
              f"HARD STOP [HS:INFRA] (S3-12b RESUME, v5.85): batch_state lost its plan and the "
              f"rebuilt set plan disagrees with authored Q.{sorted(_bad_rb)[:10]} — the "
              f"stimulus profile or blueprint changed after this paper started. Restore "
              f"{EXAM}_M{N}_batch_state.json (or the profile it was built with) and "
              f"resume; authored questions are never re-placed.")
      STIM_ACTIVE = True
      _bs_rb = json.load(open(_bs_path, encoding='utf-8'))
      _bs_rb['subtopic_by_qnum'] = {str(q): s for q, s in subtopic_by_qnum.items()}
      _bs_rb['placement_report'] = placement_report
      _bs_rb['stimulus_groups'] = STIM_PLAN
      _bs_rb['stimulus_profile_snapshot'] = STIM_PROFILE
      json.dump(_bs_rb, open(_bs_path, 'w', encoding='utf-8'))
      print("S3-12b RESUME (v5.85): set plan rebuilt and verified against every "
            "authored question. A set already partly authored: register its stimulus "
            "by copying it VERBATIM from that set's first authored member in the "
            "cumulative docx (R-STIMGROUP rule 2b).")

  elif bs_prev.get('batches_completed'):
      # ── PRE-v5.77 MID-FLIGHT PAPER (§7.2 — the upgrade path). ──────────────
      # batches exist but no plan was ever persisted. The AUTHORED questions
      # are FROZEN — re-placing them would invalidate every question already
      # written — and their subtopics are on record in the answer_key
      # concept_map. The NOT-YET-AUTHORED positions have no assignment at all
      # (the old spec deferred them to "blueprint order"), so the REMAINING
      # allocation is placed fresh into the REMAINING contiguous range of each
      # section (batches are strictly sequential, S4-2).
      _ak_path = f'/home/claude/{EXAM}_M{N}_answer_key.json'
      _cmap = {}
      if os.path.exists(_ak_path):
          _cmap = (json.load(open(_ak_path)).get('concept_map') or {})
      _authored = {}
      for _qs, _rec in _cmap.items():
          _asid = (_rec or {}).get('subtopic_id')
          if _asid:
              _authored[int(_qs)] = _asid
      if not _authored:
          raise SystemExit(
          "HARD STOP [HS:INFRA] (S3-12b RESUME): batch_state says batches are complete "
          "but the answer_key concept_map yields no q->subtopic map — the "
          "authored questions cannot be frozen without it. This is data "
          "corruption (missing/empty answer_key), not an adjacency finding; "
          "restore the answer_key from the project Files and resume again.")
      subtopic_by_qnum = dict(_authored)
      for _s in sections:
          _lo, _hi = int(_s['q_range'][0]), int(_s['q_range'][1])
          _sect_auth = {}
          for _q, _sid in _authored.items():
              if _lo <= _q <= _hi:
                  _sect_auth[_q] = _sid
          _alloc_q = _alloc_for(_sec_entry_by_name.get(_s['name'], {}))
          _remaining = dict(_alloc_q)
          for _sid in _sect_auth.values():
              _remaining[_sid] = _remaining.get(_sid, 0) - 1
          if any(v < 0 for v in _remaining.values()):
              raise SystemExit(
              f"HARD STOP [HS:INFRA] (S3-12b RESUME): section '{_s['name']}': the "
              f"answer_key concept_map holds MORE questions of some subtopic "
              f"than the blueprint allocates — the two artefacts disagree "
              f"about what was built. Data corruption, not an adjacency "
              f"finding; reconcile answer_key vs blueprint before resuming.")
          _remaining = {k: v for k, v in _remaining.items() if v > 0}
          _rem_lo = (max(_sect_auth) + 1) if _sect_auth else _lo
          if sum(_remaining.values()) != _hi - _rem_lo + 1:
              raise SystemExit(
              f"HARD STOP [HS:INFRA] (S3-12b RESUME): section '{_s['name']}': remaining "
              f"allocation sums to {sum(_remaining.values())} but "
              f"Q.{_rem_lo}-Q.{_hi} holds {_hi - _rem_lo + 1} position(s) — "
              f"authored questions are not the contiguous prefix the Batch "
              f"Stop Law guarantees, or the artefacts disagree. Data "
              f"corruption, not an adjacency finding.")
          if _remaining:
              _pl, _ = bc.place_subtopics(_remaining, (_rem_lo, _hi), _meta_q,
                                          seed=paper_index)
              subtopic_by_qnum.update(_pl)
      placement_report = bc.audit_placement(subtopic_by_qnum, sections, _meta_q)
      for _sn, _rp in placement_report.items():
          _adj = _rp['adjacent_same_concept_group']
          if len(_adj) > _rp['min_possible_adjacent_cg']:
              print(f"S3-12b NOTICE — resumed pre-v5.77 paper: section "
                    f"'{_sn}' has {len(_adj)} adjacent same-concept_group "
                    f"pair(s) at {_adj}. Authored questions are FROZEN (the "
                    f"pairs come from the old blueprint-order placement or "
                    f"sit on the authored/remaining boundary, which cannot "
                    f"be re-arranged); record this as a §R13 limitation in "
                    f"the delivery footer. NEVER a HARD STOP [HS:PROSE] on a resume.")

  else:
      # ── FRESH PAPER: build the plan, one section at a time. ────────────────
      # v5.85 (GAP-2026-09-21-LINKED-PLACEMENT): a NEW paper is ALWAYS set-aware —
      # _stim_load_profile is the SAFETY LOCK (no profile → HARD STOP [HS:INPUT] before Q.1).
      # ONE exception keeps the legacy promise: questions already authored in the
      # first, unfinished batch of a paper started before the profile existed
      # (answer_key concept_map without stimulus_group_id). That paper is placed
      # exactly as before (no sets — bit-identical to bc.place_subtopics) so no
      # authored question moves.
      if _stim_cmap_state() == 'legacy':
          print("S3-12b NOTICE (v5.85): this paper already has questions authored "
                "before the stimulus profile existed — it finishes on the legacy "
                "placement (no sets). The next NEW paper uses sets.")
          subtopic_by_qnum, placement_report, _stim_unused, _stim_unused2 = \
              _stim_build_plan(None)
      else:
          STIM_PROFILE = _stim_load_profile()
          STIM_ACTIVE = True
          subtopic_by_qnum, placement_report, STIM_PLAN, STIM_GID_BY_Q = \
              _stim_build_plan(STIM_PROFILE)

      # G-CLUSTER PRE-FLIGHT — armed before Q.1 exists, never after 10 questions do.
      for _sn, _rp in placement_report.items():
          _floor = _rp['min_possible_adjacent_cg']
          _got = len(_rp['adjacent_same_concept_group'])
          if _got > _floor:
              raise SystemExit(
                  f"HARD STOP [HS:INFRA] (S3-12b / G-CLUSTER): section '{_sn}' placement "
                  f"leaves {_got} adjacent same-concept_group pair(s); {_floor} "
                  f"is provably the minimum for this allocation "
                  f"(bc.min_possible_adjacent over concept-group-aggregated "
                  f"units). The placement engine failed, not the blueprint.")
          if _floor > 0:
              print(f"S3-12b NOTICE — section '{_sn}': {_floor} adjacent pair(s) "
                    f"are MATHEMATICALLY UNAVOIDABLE for this allocation (one "
                    f"concept group holds more than half the section). Placement "
                    f"is optimal; G-CLUSTER and A-CLUSTER will accept exactly "
                    f"{_floor}. To remove them, reduce that group's q_count at "
                    f"MockBlueprint — never by dropping a question here.")
  if STIM_ACTIVE:
      # the snapshot every audit of THIS paper reads (--stimulus-profile). It carries
      # the paper's own blueprint entry, so the auditor recomputes the SAME sets even
      # for a scoped paper whose blueprint is not [ExamCode]_blueprint.json.
      json.dump(dict(STIM_PROFILE, _paper={'mock_entry': mock_entry}),
                open(STIM_PROFILE_PATH, 'w', encoding='utf-8'))
  # v6.1 S0-NF-8 / F-11 (amendment A) — a FRESH paper only (no batch completed): each Part's band counts (frozen
  # by S0-OP-3, UNCHANGED) are re-placed INSIDE each subject's positions by the blueprint's per-subject split, so
  # the Easy slots cannot pile onto one subject. A Part without a split, or a subject whose positions do not
  # match its counts, keeps the whole-Part placement (part_counts fallback). Never a stop.
  _sbt = (bp.get('subject_band_target_per_mock') or {})
  _sbt = _sbt.get(str(N)) or _sbt.get(N) or {}
  F11_SUBJ_BY_Q = {}                                   # {q: subject} for every Part placed per subject (S3-12e reads it)
  if _sbt and not bs_prev.get('batches_completed'):
      import blueprint_core as bc
      _man_nf = globals().get('manifest') or {}
      for _sx in (globals().get('PLAN_SECTIONS') or sections or []):
          _nm = _sx.get('name') if isinstance(_sx, dict) else None
          _qr = _sx.get('q_range') if isinstance(_sx, dict) else None
          if not _nm or not _qr or not _sbt.get(_nm):
              continue
          _qs_s = [q for q in range(_qr[0], _qr[1] + 1) if q in difficulty_plan]
          _pc = {}
          for q in _qs_s:
              _pc[difficulty_plan[q]] = _pc.get(difficulty_plan[q], 0) + 1          # the frozen Part counts
          _subj_by_q = {q: bc.nf_subject_key({'subtopic_id': subtopic_by_qnum.get(q)}, _man_nf) for q in _qs_s}
          _rep = bc.schedule_place_by_subject(_sbt[_nm], _subj_by_q, {q: _qtype_by_q[q] for q in _qs_s},
                                              difficulty_labels, ruler=globals().get('EXAM_RULER'), seed=N,
                                              part_counts=_pc)
          if set(_rep) == set(_qs_s) and all(sum(1 for q in _qs_s if _rep[q] == b) == n for b, n in _pc.items()):
              difficulty_plan.update(_rep)
              F11_SUBJ_BY_Q.update(_subj_by_q)
              print(f"S3-12b F-11: {_nm} band counts {_pc} placed per subject.")
          else:
              print(f"S3-12b F-11: {_nm} per-subject placement not exact — whole-Part placement kept (AMBER, A-SUBJBAND).")
  # (paper_index is the S3-4 session integer: == N for a mock, the numeric
  # suffix of paper_id for a scoped paper — so a 20-paper series gets 20
  # different arrangements from ONE blueprint, deterministically, and
  # `continue` / S4-12 resume reproduce the plan byte-identically.)
  ```

  THE THREE BRANCHES, in law form: a paper WITH a persisted plan resumes on
  it FROZEN; a pre-v5.77 paper WITH authored questions freezes them from the
  answer_key concept_map and places only the un-authored remainder (adjacency
  findings on it are §R13 DISCLOSURES, never stops — the only HARD STOP [HS:INFRA]s on
  a resume are artefact-consistency faults, where answer_key, batch_state and
  blueprint disagree about what exists); a paper with NO authored questions
  is placed fresh and gated by the G-CLUSTER pre-flight.

  §7.3 METADATA DEGRADATION (never raises, never silently disables adjacency):
  absent `concept_group` → falls back to subtopic_id (R19(a) collapses to the
  base rule); absent `presentation_family` → that objective dormant for the
  subtopic, never fabricated; absent `section` (subject) → rotation dormant;
  absent or NON-NUMERIC `linked_group_size` → 1 (no linked group). A linked-
  stimulus group (R-LINKED Model B) is emitted as one contiguous block and is
  R19-exempt INSIDE the block; a `q_count` that is not a multiple of the
  group size is a PlacementError, never a silent split.

## S3-12c — Draw the authoring brief per slot (v5.82 — GAP-2026-08-29-STYLE-FIDELITY §6.5.1)

  Extends the S3-12b placement plan. For EVERY slot the engine draws an
  authoring BRIEF from the style profile cell — section x answer_type, falling
  back to the PAPER cell when the section cell is DORMANT (EC-3). Runs only
  when the profile loaded ACTIVE at S3-2b; otherwise every brief is None and
  Step 7 authors exactly as it did before (P-4: dormancy is baseline
  behaviour, never a stop, never a degraded paper).

  DETERMINISM IS THE CONTRACT. The draw seed is
  bc.brief_seed(exam_code, paper_id, corpus_hash, qnum) =
  sha256(exam · paper · corpus_hash · qnum), so a re-run on the same inputs
  draws the same briefs, and S4-12 resume reproduces them byte-identically.
  Briefs are PERSISTED in batch_state.style_briefs[qnum] and FROZEN exactly
  like the placement plan (EC-19): a profile that changes mid-paper is
  recorded in style_gate.events[] as `profile_changed_during_paper` and the
  session CONTINUES on the frozen briefs.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S3-12c (executable) ─────────────────────────────────────────────────
  import random, blueprint_core as bc

  def draw_style_brief(profile, section, answer_type, subtopic_id,
                       exam_code, paper_id, corpus_hash, qnum,
                       axis2_allowed=None, permitted_mechanics=None):
      """One frozen authoring brief, or None when the profile is dormant."""
      if not profile or (profile.get('_meta') or {}).get('status') == 'DORMANT':
          return None
      sect = ((profile.get('sections') or {}).get(section) or {})
      cell = None
      if str(sect.get('status', '')).upper() == 'ACTIVE':
          cell = ((sect.get('by_answer_type') or {}).get(answer_type)
                  or sect.get('cell'))
      if not cell:                       # EC-3 — section thin: use the paper cell
          cell = profile.get('paper') or {}
      if not cell:
          return None
      rng = random.Random(bc.brief_seed(exam_code, paper_id, corpus_hash, qnum))
      sub = (profile.get('subtopics') or {}).get(subtopic_id) or {}

      mech = bc.weighted_draw(cell.get('mechanic_mix'), rng,
                              restrict=permitted_mechanics)
      form = bc.weighted_draw(cell.get('form_mix'), rng, restrict=axis2_allowed)
      # polarity: Bernoulli at min(cell rate, the subtopic's own negative
      # frequency); forced to 0 when I-5 is live and the cell never goes negative
      p_pol = min(float(cell.get('polarity_rate') or 0.0),
                  float(sub.get('polarity_rate')
                        if sub.get('polarity_rate') is not None else 1.0))
      item_rules = profile.get('item_rules') or {}
      i5_live = not ((item_rules.get('I-5') or {}).get('suspended'))
      if i5_live and float(cell.get('polarity_rate') or 0.0) == 0.0:
          p_pol = 0.0
      shape = bc.weighted_draw(cell.get('option_shape_mix'), rng)

      dmix = sub.get('distractor_mix')
      if dmix == 'unavailable' or not dmix:
          mechs, prior = list(bc.default_distractor_prior(shape or 'none')), 'default'
      else:
          mechs, prior = [], None
          for _ in range(3):
              t = bc.weighted_draw(dmix, rng)
              if t:
                  mechs.append(t)
      def _pick(seq):
          seq = [s for s in (seq or ()) if s]
          return rng.choice(seq) if seq else None
      stem_len = cell.get('stem_len') or {}
      return {
          'brief_id': f"{section}|{answer_type}|{subtopic_id}|{qnum}",
          'mechanic': mech, 'form': form,
          'polarity': rng.random() < p_pol,
          'option_shape': shape,
          'option_count': bc.weighted_draw(cell.get('option_count'), rng),
          'stem_len_band': (stem_len.get('p10'), stem_len.get('p90')),
          'ask_form': (_pick([a.get('text') for a in (cell.get('ask_forms') or ())])),
          'instruction': (_pick([i.get('text')
                                 for i in (cell.get('instruction_phrases') or ())])),
          'distractor_mechanisms': mechs, 'distractor_prior': prior,
          'number_ranges': sub.get('number_ranges'),
          'exclude_values': sub.get('exclude_values') or [],
          'low_entropy': bool(sub.get('low_entropy')),
          'stimulus': (rng.random()
                       < float((cell.get('stimulus_stats') or {}).get('stimulus_rate') or 0.0)),
      }
  ```

  A CLASS-4 LINKED GROUP draws its STIMULUS brief ONCE for the group; each
  member then draws its own question brief on its own seed.

  BAND CONDITIONING (EC-33/EC-35): `permitted_mechanics` is the set a mechanic
  is allowed in for this slot's difficulty band — a mechanic is permitted in
  band B when the exam's own PYQ show it in band B at >= 5% of that band's
  questions, per the difficulty profile. When the difficulty profile is
  DORMANT every mechanic is permitted in every band. NEVER a hand table.

## S3-12d — SHAPE PLAN per paper (v5.90 — GAP-2026-11-03 G05; owner decision OD-6 (c): FLOORS AND CAPS)

  WHY. The real paper uses eleven question SHAPES — "identify P", "A and B", a lettered
  intermediate, the correct reagent sequence, "A major / B minor", a two-part "respectively",
  Hammett / NMR-integral quantities, and multi-statement "A and B only" items at 3 of 30 —
  and Test 01 delivered none of the last six: Axis-2 quotas were 10-paper WINDOW targets with
  an empty guarantee list, the figural ask-type control (F8) was dormant, and the vocabulary
  lacked four shapes. ONE PLAN, ONE PRECEDENCE now: Axis-1 format > qtype > SHAPE PLAN >
  Axis-2. Shape floors REPLACE axis2_guarantee for the Axis-2 classes they cover.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S3-12d (executable; after S3-12c, before S3-13) ──────────────────────────────
  import blueprint_core as bc
  _shape_tg = ((bp.get('shape_target_per_paper') or {}).get(str(N))
               or (bp.get('shape_target_per_paper') or {}).get(N) or {})
  # v5.92 (GAP-2026-11-05 guard G4): a target is PLANNED here only under the LEGACY shape rule
  # s1 (the bare ask types this spec renders); a future s2 target (statement / match /
  # sequence formats, figure_types.ASK_TYPES_S2) is a FORMAT, read by A-AXIS2 as a WARN —
  # never a shape slot. An absent shape_rule reads as s1 (bc.shape_rule_of).
  _shape_tg = {k: v for k, v in _shape_tg.items()
               if bc.shape_rule_of((v or {}).get('shape_rule') if isinstance(v, dict) else None) == bc.SHAPE_RULE_LEGACY}
  if 'shape_plan' in bs_prev and bs_prev.get('batches_completed'):
      # ── FROZEN (EC-19): the plan was persisted at S3-16 and items were authored to it.
      # A resumed run NEVER re-assigns shapes — not even after Step 5 / bp_refresh changed
      # the targets (that applies to the NEXT paper).
      SHAPE_PLAN = dict(bs_prev['shape_plan'] or {})
      print(f"S3-12d: shape plan FROZEN from batch_state ({len([q for q in SHAPE_PLAN if q != '_infeasible'])} slots"
            f"{'; DORMANT when the paper started' if not SHAPE_PLAN else ''}).")
  elif not _shape_tg:
      # OD-1: no targets (blueprint built before Blueprint v1.63.0 / ScopedBlueprint v1.13.0,
      # or section_rules without QUALITY blocks) -> the control is DORMANT, printed, recorded
      # on the readiness record (S3-2e) that S3-16 persists and S13-4 commits.
      print("S3-12d: shape plan DORMANT — blueprint carries no shape_target_per_paper for "
            f"paper {N} (run bp_refresh after Step 5 of release 2026.11.03). Recorded in "
            "quality_readiness as G-SHAPEMIX STALE.")
      QUALITY_READINESS = bc.readiness_mark(QUALITY_READINESS, 'G-SHAPEMIX', 'STALE',
                                            f'no shape_target_per_paper for paper {N}',
                                            'run Step 5 (2026.11.03), then MockBlueprint / ScopedBlueprint --refresh')
      QUALITY_DEGRADED = list(QUALITY_READINESS.get('degraded') or [])
      QUALITY_FOOTER_LINE = bc.degraded_footer_line(QUALITY_READINESS)
      SHAPE_PLAN = {}
  else:
      _slots = [{'q': q, 'subtopic_id': subtopic_by_qnum[q], 'qtype': _qtype_by_q.get(q, 'mcq')}
                for q in sorted(subtopic_by_qnum)]
      # shapes each subtopic's PYQs use: the QUALITY block's shape_shares keys (topic-level
      # fallback when the subtopic block lists none — bc.quality_block_for_subtopic)
      _sub_shapes = {}
      for _sid in set(subtopic_by_qnum.values()):
          _qb = bc.quality_block_for_subtopic(SECTION_RULES_TEXT, _sid) or {}
          _sub_shapes[_sid] = [k.split('|')[0] for k in (_qb.get('shape_shares') or {}).keys()] or list(_shape_tg.keys())
      import hashlib as _hl
      SHAPE_PLAN = bc.assign_shape_plan(_slots, _sub_shapes, _shape_tg,
                                        seed=bc.brief_seed(EXAM, paper_id, _hl.sha256(SECTION_RULES_TEXT.encode('utf-8')).hexdigest(), 0))
      print(f"S3-12d: shape plan for paper {N}: " + ', '.join(f"{k}={v}" for k, v in sorted(
            ((s, sum(1 for q, v in SHAPE_PLAN.items() if q != '_infeasible' and v == s)) for s in _shape_tg)))
            + (f"; infeasible (recorded, not a defect): {SHAPE_PLAN['_infeasible']}" if SHAPE_PLAN.get('_infeasible') else ''))
  SHAPE_PLAN = {str(k): v for k, v in SHAPE_PLAN.items()}   # FROZEN by the S3-16 batch_state initialiser ('shape_plan', EC-19)

  # ── S3-12e (v5.92 — GAP-2026-11-05 DL-33 / DL-34; guards G4, S7) ─────────────────────────
  # (a) TOP-BAND SLOTS FOLLOW THE MEASURED SUBTOPIC SHARE (DL-33). On a FRESH paper only (a
  #     resumed paper's plan is authoritative, S4-12), bc.band_subtopic_plan re-places the
  #     top-band slots of difficulty_plan onto subtopics whose measured top-band share
  #     (blueprint.hard_share_by_subtopic, Blueprint §7-9 / ScopedBlueprint S8-2e) is > 0.
  #     Every band count PER SECTION and every qtype floor is unchanged (asserted by the
  #     engine; a swap never crosses a section — section_of_q); when
  #     every share is 0 / unknown the plan is returned unchanged. Persisted by S3-16 in the
  #     same write as the rest of the plan.
  # (b) ASK-FORMAT FLOORS (DL-34): the blueprint's axis2_format_floor_per_paper[N] is read
  #     and printed; S7 authors each non-'direct' format at least that often across the paper
  #     (a soft target checked by the WARN-only A-AXIS2) — NEVER written into SHAPE_PLAN and
  #     never a stop. {} = dormant (printed).
  if difficulty_plan and not (bs_prev.get('subtopic_by_qnum') and bs_prev.get('batches_completed')):
      _hs_bp = bp.get('hard_share_by_subtopic') if isinstance(bp.get('hard_share_by_subtopic'), dict) else {}
      if _hs_bp:
          _plan_before = dict(difficulty_plan)
          # every swap stays INSIDE its section: the plan was built per section to the exact
          # by_section counts (v5.75), and R5's amend_schedule_in_place reads those counts.
          # The sections are the ones the plan was BUILT on (PLAN_SECTIONS, set above with the
          # plan: the blueprint's, or exam_config's for a pre-v1.57 blueprint; [] = paper-wide
          # plan, one group). If that block did not run, bp['sections'] (stricter, never wrong).
          # A section whose q_range is not two integers maps no slot — never a stop; an
          # unmapped slot only swaps with other unmapped slots.
          _secs_12e = globals().get('PLAN_SECTIONS')
          if not isinstance(_secs_12e, list):
              _secs_12e = bp.get('sections') if isinstance(bp.get('sections'), list) else []
          def _q_span(_s):
              try:
                  _lo, _hi = (int(_s['q_range'][0]), int(_s['q_range'][1]))
              except (KeyError, IndexError, TypeError, ValueError):
                  return range(0)
              return range(_lo, _hi + 1)
          _sec_of_q = {q: str(_s.get('name', '')) for _s in _secs_12e if isinstance(_s, dict)
                       for q in _q_span(_s)}
          # F-11: a Part whose bands were placed per subject keeps them — a swap stays inside (Part, subject)
          for _q11, _sj11 in (globals().get('F11_SUBJ_BY_Q') or {}).items():
              if _q11 in _sec_of_q:
                  _sec_of_q[_q11] = _sec_of_q[_q11] + '|' + str(_sj11)
          difficulty_plan = bc.band_subtopic_plan(difficulty_plan, subtopic_by_qnum, _hs_bp,
                                                  _qtype_by_q, difficulty_labels, section_of_q=_sec_of_q)
          _moved = sum(1 for q in _plan_before if _plan_before[q] != difficulty_plan.get(q))
          print(f"S3-12e: top-band slots placed by measured subtopic share — {_moved} slot(s) moved; "
                f"band counts unchanged in every section (and in every subject of an F-11 Part)")
      else:
          print("S3-12e: hard_share_by_subtopic absent from the blueprint — current band spread kept")
  AXIS2_FORMAT_FLOOR = dict((bp.get('axis2_format_floor_per_paper') or {}).get(str(N)) or {})
  print(f"S3-12e: ask-format floors for paper {N}: {AXIS2_FORMAT_FLOOR or 'none (dormant)'}")
  # (c) LEVEL TARGETS (DL-36/47): the per-subtopic figure_complexity_pct / closeness_pct the
  #     blueprint copied from section_rules QUALITY. CHECK 3c (b1) / ladder R2 read
  #     LEVEL_TARGETS[subtopic_id] for the two level REJECT reasons (complexity below p10,
  #     closeness below p50); a subtopic absent here has no such reason (dormant, never a stop).
  LEVEL_TARGETS = dict(bp.get('level_targets') or {}) if isinstance(bp.get('level_targets'), dict) else {}
  # (d) HARD SUPPLY (DL-31, advisory, guard S7): printed so the operator sees how many real
  #     content-full Hard exemplars the scope holds before Q.1; never routed into feasibility.
  _hsup = bp.get('hard_supply') if isinstance(bp.get('hard_supply'), dict) else {}
  print(f"S3-12e: level targets for {len(LEVEL_TARGETS)} subtopic(s); hard supply "
        + (f"{_hsup.get('n_hard_content_full')} content-full top-band exemplar(s) of {_hsup.get('n_pool')} "
           f"({_hsup.get('source')} bands; advisory)" if _hsup else 'not recorded (pre-1.64.0 blueprint or no profile)'))
  ```
  RULES. (1) A resumed run NEVER re-assigns shapes (S4-12 reads batch_state['shape_plan']).
  (2) The item MUST render its assigned shape (S7-QUALITY `shape`); a mismatch is an item
  defect at R3, which moves it only to an UNDER-target shape valid for the subtopic. (3) A
  figure-backed combination shape (structures A-D + "A and B only") renders through S10-8's
  multi-panel path; answer verification treats each statement as a set member (R-ANSWER
  multi-mode internally; the item stays single-key). (4) A-SHAPEMIX checks floors and caps
  per paper; a shape no capable slot could take is recorded infeasibility, never a defect.

## S3-13 — Build answer position budget (PRE-Q1 — v2.0 GAP-08 fix)

  CRITICAL: Budget MUST be built before Q1, not post-generation.
  Assign answer positions for ALL N questions before generating any content.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import random

  def build_answer_budget(total_questions, sections, options_count=4,
                          msq_positions=None, nat_positions=None):
      """
      Build K-BAL balanced, K-PAT compliant answer sequence.
      K-BAL: 20-30% per option globally, 15-35% per section.
      K-PAT: max run of 2 consecutive identical answers GLOBALLY
             (including cross-section boundaries).
      v4.5: MSQ (answer_cardinality=='multi') Q positions are EXCLUDED from the single-position
      pool exactly like fixed_set positions — their answer is a SET, so single-position
      K-BAL share and K-PAT "run of identical answers" are undefined for them. The MSQ
      builder picks each set independently (subject to G-MSQ-SET/CARD); the budget leaves
      those positions as None. msq_positions = set of 1-based Q numbers whose subtopic
      answer_cardinality=='multi' (empty/None ⇒ fully dormant, identical to v4.4).
      v4.7 (ND8): NAT (answer_type=='numerical') Q positions are EXCLUDED on the SAME basis —
      a NAT answer is a typed VALUE, not an option position, so K-BAL share / K-PAT run are
      equally undefined. nat_positions = set of 1-based Q numbers whose subtopic
      answer_type=='numerical' (empty/None ⇒ dormant). excluded = fixed ∪ msq ∪ nat.
      v4.7 (ND12): under heavy exclusion (e.g. a 30-40% NAT+MSQ GATE paper) n_free can be
      small enough that an exact 20-30% per-option band is INFEASIBLE. In that regime the
      K-BAL band DEGRADES TO A WARNING (best-effort balance) instead of an assert-crash; the
      K-PAT run-cap still applies. Single-answer exams (n_free == total_questions) are
      unaffected — the band is trivially satisfiable exactly as in v4.4.
      """
      # Identify fixed-set Q positions (excluded from balance pool)
      # (detect from section_rules.md wrong_option_structure.type == fixed_set)
      fixed_positions = set()  # populated from subtopic analysis
      msq_positions   = set(msq_positions or ())   # v4.5: multi-answer Q positions
      nat_positions   = set(nat_positions or ())   # v4.7: numerical-answer Q positions
      excluded        = fixed_positions | msq_positions | nat_positions

      n_free = total_questions - len(excluded)
      target = n_free // options_count

      # Build balanced sequence with K-PAT max-run=2:
      sequence = []
      option_counts = {i: 0 for i in range(1, options_count+1)}
      last_two = []

      for _ in range(n_free):
          # Available options: not creating a run of 3
          available = list(range(1, options_count+1))
          if len(last_two) == 2 and last_two[0] == last_two[1]:
              forbidden = last_two[0]
              available = [x for x in available if x != forbidden]

          # Prefer under-represented options (for K-BAL):
          min_count = min(option_counts[o] for o in available)
          preferred = [o for o in available if option_counts[o] == min_count]
          choice = random.choice(preferred)

          sequence.append(choice)
          option_counts[choice] += 1
          last_two = (last_two + [choice])[-2:]

      # Validate K-BAL (only over the single-answer free pool):
      # v4.7 ND12: the exact band is only ENFORCEABLE when the free pool is large enough to
      # hold it — the tightest option share is 1/n_free, so a band floor of 20% needs
      # n_free ≥ ~ 4·options_count for every option to be placeable inside 20-30%. Below that
      # threshold (heavy NAT+MSQ exclusion) we WARN and keep the best-effort balance instead
      # of asserting. At/above it we assert exactly as before (no behaviour change for the
      # single-answer case, where n_free == total_questions).
      KBAL_MIN_FREE = 4 * options_count
      if n_free >= KBAL_MIN_FREE:
          for opt, cnt in option_counts.items():
              pct = cnt / n_free * 100
              assert 20 <= pct <= 30, \
                  f"K-BAL failed: option {opt} at {pct:.1f}% (need 20-30%)"
      elif n_free:
          for opt, cnt in option_counts.items():
              pct = cnt / n_free * 100
              if not (20 <= pct <= 30):
                  print(f"K-BAL degraded (n_free={n_free} < {KBAL_MIN_FREE} after "
                       f"fixed/MSQ/NAT exclusion): option {opt} at {pct:.1f}% — best-effort "
                       f"balance kept (band un-enforceable on a small free pool; K-PAT holds).")

      # Assign to Q positions (skip excluded = fixed_set ∪ MSQ ∪ NAT):
      budget = {}
      seq_idx = 0
      for q in range(1, total_questions + 1):
          if q in excluded:
              budget[str(q)] = None  # fixed: from option content; MSQ: set; NAT: typed value
          else:
              budget[str(q)] = sequence[seq_idx]
              seq_idx += 1

      return budget

  # v4.5: msq_positions = the set of Q numbers whose placed subtopic has
  # answer_cardinality=='multi'. Populated from the SAME subtopic→Q placement plan that
  # populates fixed_positions (whole-subtopic mode). Empty when blueprint multi_present is
  # false ⇒ build_answer_budget behaves exactly as v4.4.
  # v5.77 — the v4.5 sentence that stood here ("if the placement plan is not yet
  # materialised, msq_positions stays empty ... K-BAL/K-PAT are never corrupted either
  # way") was FALSE and is retracted: an empty exclusion set puts every multi Q into the
  # free answer pool and skews K-BAL paper-wide (GAP-2026-08-28-PLACEMENT-UNSPECIFIED).
  # The plan is ALWAYS materialised — S3-12b runs before this step — and the reads
  # below HARD STOP [HS:INFRA] if it is not. The empty set below is an initialiser only.
  msq_positions = set()
  if multi_present:
      if _position_based_typing:
          # v5.X: for position-based exams, MSQ positions come from marking_scheme Q-ranges,
          # not from per-subtopic answer_cardinality. Every Q in an MSQ range is MSQ regardless
          # of which subtopic is placed there.
          msq_positions = {q for q in range(1, total_questions + 1) if _type_for_q(q) == 'MSQ'}
      else:
          multi_ids = {sid for sid, am in answer_cardinality_by_id.items() if am == 'multi'}
          # v5.77 (GAP-2026-08-28-PLACEMENT-UNSPECIFIED FIX-3): the plan is
          # AUTHORITATIVE and built at S3-12b. The pre-v5.77 `except NameError`
          # fallback to an empty set silently put every MSQ question into the
          # free answer pool and corrupted K-BAL for the whole paper on any
          # exam without position-based typing. A missing plan is a producer
          # fault, never a dormancy condition.
          if not subtopic_by_qnum:
              raise SystemExit("HARD STOP [HS:INFRA] (S3-13): no placement plan. S3-12b "
                               "must run before the answer budget — the MSQ "
                               "exclusions are derived from placement.")
          msq_positions = {q for q, sid in subtopic_by_qnum.items() if sid in multi_ids}
  # v4.7: nat_positions = the set of Q numbers whose placed subtopic has
  # answer_type=='numerical'. Same placement plan, same dormancy/defensive semantics as MSQ.
  # Empty when blueprint nat_present is false ⇒ budget identical to v4.6.
  nat_positions = set()
  if nat_present:
      if _position_based_typing:
          # v5.X: for position-based exams, NAT positions come from marking_scheme Q-ranges.
          nat_positions = {q for q in range(1, total_questions + 1) if _type_for_q(q) == 'NAT'}
      else:
          nat_ids = {sid for sid, at in answer_type_by_id.items() if at == 'numerical'}
          # v5.77 FIX-3 (same law as the MSQ read above): no plan ⇒ HARD STOP [HS:INFRA].
          if not subtopic_by_qnum:
              raise SystemExit("HARD STOP [HS:INFRA] (S3-13): no placement plan. S3-12b "
                               "must run before the answer budget — the NAT "
                               "exclusions are derived from placement.")
          nat_positions = {q for q, sid in subtopic_by_qnum.items() if sid in nat_ids}
  answer_budget = build_answer_budget(total_questions, sections,
                                      msq_positions=msq_positions,
                                      nat_positions=nat_positions)
  budget_path = f'/home/claude/{EXAM}_M{N}_answer_budget.json'
  json.dump({'positions': answer_budget}, open(budget_path, 'w'))
  # All SINGLE-answer questions read their correct-answer position from this budget.
  # Content generation fills the PRE-ASSIGNED slot with the correct answer.
  # v4.5: MULTI (MSQ) questions have budget[str(q)]==None — they SELF-ASSIGN the correct
  # set S (subject to R-ANSWER multi + G-MSQ-SET/CARD) and never read a single position.
  ```

## S3-14 — Initialise answer key sidecar (v2.0 GAP-18 fix)

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  answer_key_path = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  if not os.path.exists(answer_key_path):
      # v4.5: msq_meta carries the MSQ config (from blueprint) so the gate sweep can
      # validate MSQ keys with NO blueprint dependency at audit time. All values are
      # inert when multi_select_allowed is false. _mc = blueprint['msq_contract'] (v1.8).
      # msq_allow_aota (D5) is a generation-time policy read directly from section_rules
      # EXAM_STRUCTURE (a Step 7 input); default false. (Cleaner long-term: carry it in
      # blueprint['msq_contract'] from Step 0/Step 1 — a one-line addition each.)
      # v5.4 FIX: removed all 'bp' in dir() guards — bp is ALWAYS loaded at S3-2 before
      # S3-14 runs. The 'in dir()' idiom was a cosmetic guard that would silently activate
      # wrong defaults if the code were ever refactored into a function. Direct access is safe.
      _mc = bp.get('msq_contract', {})
      _nc = bp.get('nat_contract', {})                             # v4.7 NAT contract
      # v5.4 FIX: was 'section_rules_text' (undefined) — silently defaulted False via
      # NameError catch, so msq_allow_aota was ALWAYS ignored. Now reads sr_text (S3-2).
      _aota = bool(re.search(r'^\s*msq_allow_aota\s*:\s*true\s*$', sr_text, re.M | re.I))
      json.dump({
          "answers": {}, "sources": {},
          "msq_meta": {
              "multi_select_allowed": bool(bp.get('multi_select_allowed', False)),
              "total_options"       : int(bp.get('total_options', 4)),
              "msq_k_mode"          : _mc.get('msq_k_mode', 'n/a'),
              "msq_k"               : _mc.get('msq_k', None),
              "msq_allow_aota"      : _aota,
          },
          # v4.7 NAT meta — the answer model for the gate sweep (G-NAT-ANSWER) and Step 4.
          # Inert when nat_allowed=false (nat_present false ⇒ no NAT Qs reference it).
          "nat_meta": {
              "nat_allowed"     : bool(bp.get('nat_allowed', False)),
              "nat_answer_type" : _nc.get('nat_answer_type', 'real'),
              "nat_tolerance"   : _nc.get('nat_tolerance', '0'),
              "nat_instruction" : _nc.get('nat_instruction', 'Enter your answer as a numerical value.'),
          }
      }, open(answer_key_path, 'w'))
  # Written per-question during generation (S7 after each Q accepted)
  # NEVER at end — incremental, per-question writes only
  ```

## S3-15 — Build SC manifest

  Build from subtopic_list[] and dedup_partition. Register all linked groups.

## S3-15L — THE TARGET PLAN + THE PATTERN SOURCE OF EVERY ORGANIC SLOT (v5.94 — GAP-2026-11-07; owner D1 (b), D6)

  Runs on EVERY exam right before S3-16 writes batch_state — AFTER S3-12b/S3-12e have placed every
  band, so both products describe the FINAL plan (release review 2026-11-08: drawn earlier they
  described a plan S3-12e then rearranged).
  (1) DIFFICULTY_PLAN_TARGET — the slot bands the paper is measured against at the end (S13-2L,
  S13-2G phase 3): the plan as built — v6.0: FROZEN with the request and the applied counts
  (bc.schedule_freeze, S0-OP-3; no band swap exists); a resume of the SAME paper restores it (same slots,
  same band counts).
  (2) L2_SOURCES — when L2_MODEL is active, each slot whose subtopic is in L2_SCOPE_IDS gets ONE
  pattern source, drawn deterministically (bc.l2_slot_source, seed bc.brief_seed): an unused
  pattern card of the slot's band (cascade subtopic -> topic -> family -> any) or, when none exists,
  an unused vocabulary concept at the band's load floor. A card is a model of WHAT MUST BE DECIDED
  (concept chain, ask type, distractor relations, stereo kind) — it carries no stem, substrate,
  SMILES, key or source number: the author writes a NEW question on a NEW substrate (CHECK 3c (b0)).
  A saved source is reused on resume only for the same slot band.
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S3-15L (v5.94) ──
  import hashlib as _hl_src
  DIFFICULTY_PLAN_TARGET = None
  if globals().get('difficulty_plan'):
      _saved_t = _bs_l2.get('difficulty_plan_target') if _same_paper_l2 else None
      _fresh_t = {str(q): b for q, b in difficulty_plan.items()}
      DIFFICULTY_PLAN_TARGET = (dict(_saved_t) if isinstance(_saved_t, dict) and set(_saved_t) == set(_fresh_t)
                                and bc.dl_band_counts(_saved_t, difficulty_labels)
                                == bc.dl_band_counts(_fresh_t, difficulty_labels) else _fresh_t)
  # ── S0-OP-3 freeze (v6.0) — the request, the applied counts and the placement, ONCE (a resume restores) ──
  SCHEDULE_FROZEN_STATE = None
  if DIFFICULTY_PLAN_TARGET:
      _sa_f = globals().get('SCHEDULE_APPLIED') or {}
      _app_f = bc.dl_band_counts(DIFFICULTY_PLAN_TARGET, difficulty_labels)
      _notes_f = list(_sa_f.get('notes') or [])
      if _sa_f.get('counts') and dict(_sa_f['counts']) != dict(_app_f):
          _notes_f.append(f"per-section schedule wins: whole-paper counts recomputed as {dict(_app_f)} "
                          f"(was {dict(_sa_f['counts'])})")
          print('S3 schedule as applied: ' + _notes_f[-1])
      _prev_f = ({k: _bs_l2[k] for k in ('schedule_requested', 'schedule_applied', 'schedule_frozen',
                                         'refill_sessions_used', 'last_resort_slots') if k in _bs_l2}
                 if _same_paper_l2 and isinstance(_bs_l2, dict) else {})
      if (_prev_f.get('schedule_frozen') or {}).get('placement') not in (None, {str(q): b for q, b in DIFFICULTY_PLAN_TARGET.items()}):
          _prev_f = {}                                            # a frozen state of ANOTHER placement is never reused
      SCHEDULE_FROZEN_STATE = bc.schedule_freeze(_prev_f, dict(globals().get('_sched_req') or _app_f), dict(_app_f),
                                                 DIFFICULTY_PLAN_TARGET, notes=_notes_f)
  L2_SOURCES = {}
  if L2_MODEL and L2_MODEL.get('active') and difficulty_plan:
      _saved_src = (_bs_l2.get('l2_sources') if _same_paper_l2 else None) or {}
      _corp_src = _hl_src.sha256(SECTION_RULES_TEXT.encode('utf-8')).hexdigest()
      _used_src = set()
      for _q_src in sorted(difficulty_plan):
          _sid_src = str(subtopic_by_qnum.get(_q_src) or '')
          if _sid_src not in L2_SCOPE_IDS:
              continue
          _s = _saved_src.get(str(_q_src)) if isinstance(_saved_src.get(str(_q_src)), dict) else None
          if _s is None or _s.get('band') != difficulty_plan[_q_src]:
              _s = dict(bc.l2_slot_source(L2_CARDS, difficulty_plan[_q_src], _sid_src, used=tuple(sorted(_used_src)),
                                          seed=bc.brief_seed(EXAM, paper_id, _corp_src, _q_src)),
                        band=difficulty_plan[_q_src])
          if _s.get('ref'):
              _used_src.add(str(_s['ref']))
          L2_SOURCES[str(_q_src)] = _s
      print(f"S3-15L: pattern sources for {len(L2_SOURCES)} organic slot(s): "
            f"{sum(1 for s in L2_SOURCES.values() if s.get('kind') == 'card')} card(s), "
            f"{sum(1 for s in L2_SOURCES.values() if s.get('kind') == 'concept')} concept(s), "
            f"{sum(1 for s in L2_SOURCES.values() if s.get('kind') == 'none')} without a source")
  ```

## S3-16 — Build batch plan → write batch_state.json

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  batch_plan = []
  batch_id = 1
  for sec in sections:
      sec_name = sec['name']
      q_start = sec['q_range'][0]
      q_end   = sec['q_range'][1]
      q = q_start
      while q <= q_end:
          batch_q_end = min(q + 9, q_end)  # max 10Q per batch
          batch_plan.append({
              'batch_id': batch_id,
              'section': sec_name,
              'q_start': q,
              'q_end': batch_q_end,
              'q_count': batch_q_end - q + 1,
              'is_final': False
          })
          batch_id += 1
          q = batch_q_end + 1

  if batch_plan:
      batch_plan[-1]['is_final'] = True

  batch_state = {
      'exam_code': EXAM,
      'mock_n': N,
      'paper_id': paper_id,          # C2: universal identity (mock == "MOCK:M{N:02d}")
      'registry_pin': REG_PIN,       # v5.84 REGISTRY-SOURCE-LAW R4: {fingerprint, source,
                                     # path} of the registry this run STARTED from (S3-1).
                                     # Every later turn's S3-1 re-resolves and
                                     # pp.registry_source_check refuses a different one.
      'total_questions': total_questions,
      'batch_plan': batch_plan,
      'batches_completed': [],
      'current_batch': 1,
      'quality_readiness': QUALITY_READINESS,   # v5.90 S3-2e record (A-READINESS reads it)
      'shape_plan': SHAPE_PLAN,                  # v5.90 S3-12d plan, frozen (S4-12 reads it; never re-assigned)
      'mechanics_used': {},
      'templates_used': {},
      'rotation_state': {},
      'passage_linked_qs': [],
      'cloze_linked_qs': [],
      'concept_ledger': [],          # v5.4 FIX: was missing from init (present in S4-3 schema)
      'presentation_ledger': [],     # v5.4 FIX: was missing from init (present in S4-3 schema)
      'subtopic_by_qnum': {str(q): sid for q, sid in subtopic_by_qnum.items()},
                                     # v5.77: AUTHORITATIVE placement plan from S3-12b.
                                     # Every consumer reads it; none recomputes it.
                                     # On resume it is FROZEN (S3-12b / S4-12).
      'placement_report': placement_report,
                                     # v5.77: {section_name: report} from
                                     # bc.place_subtopics / bc.audit_placement — the
                                     # evidence G-CLUSTER and A-CLUSTER both quote.
      **({'stimulus_groups': STIM_PLAN,
          'stimulus_profile_snapshot': STIM_PROFILE} if STIM_ACTIVE else {}),
                                     # v5.85 (GAP-2026-09-21-LINKED-PLACEMENT): the
                                     # stimulus-group plan from S3-12b, PRESENT only
                                     # for a set-placed paper (its presence is what a
                                     # resume reads). Each group's 'stimulus' is
                                     # filled ONCE by stim_register (R-STIMGROUP)
                                     # and reused verbatim by every member.
      # v5.89: the plan S3 built, persisted at INIT so a resume restores it (S3 checks
      # paper_id + counts); band swaps and R5 rewrite it in place. None = dormant.
      'difficulty_plan': ({str(q): lab for q, lab in difficulty_plan.items()}
                          if difficulty_plan else None),
      # v5.92 (GAP-2026-11-05): the schedule as the blueprint wrote it BEFORE any in-run R5
      # amendment (informational — the bench card prints original vs amended, DL-42/51)
      # and the per-paper difficulty state the footer discloses (Part D).
      'difficulty_schedule_original': ({str(q): lab for q, lab in difficulty_plan.items()}
                                       if difficulty_plan else None),
      # schedule_original: the plan's band counts as the blueprint wrote them, before any
      # in-run amendment — committed with difficulty_state (S13-4) so A-PYQBENCH prints
      # original vs final (DL-51). Every paper with a plan; {} when the plan is dormant.
      'difficulty_labels': list(difficulty_labels),   # v5.92: read by S13-2G phase 3 (resume-safe)
      # v5.94 (GAP-2026-11-07): the TARGET plan S13-2L counts the paper against (v6.0: frozen,
      # never changed) and each organic slot's pattern source (S3-15L).
      'difficulty_plan_target': (dict(DIFFICULTY_PLAN_TARGET) if globals().get('DIFFICULTY_PLAN_TARGET') else None),
      **(globals().get('SCHEDULE_FROZEN_STATE') or {}),   # v6.0 S0-OP-3: schedule_requested / _applied / _frozen
      'l2_sources': dict(globals().get('L2_SOURCES') or {}),
      'difficulty_state': dict(DIFFICULTY_STATE, schedule_original=(
          {l: sum(1 for v in difficulty_plan.values() if v == l) for l in difficulty_labels}
          if difficulty_plan else {}),
          ruler={k: (globals().get('EXAM_RULER') or {}).get(k) for k in ('ruler_version', 'basis', 'past_distribution')}),
      'exam_ruler': globals().get('EXAM_RULER'),     # v6.0 S0-OP-2: resume-safe copy (S13-2L / S13-4OP)
      'op_overrides': list((globals().get('OP_CONST') or {}).get('overrides') or []),   # §LADDER-OP line (S13-2L)
      'bp_project_sha': dict(BP_PROJECT_SHA),   # v5.89: which project blueprint this paper
                                                # started from (S3-1 keep-amended rule)
      'figural_qs': {}               # v5.13: {qnum_str: {subtopic_id, image_role, rendered: bool}}
                                      # Populated at S3-18 from the figural manifest scan.
                                      # At generation time: set rendered=true after
                                      # add_figural_question() or add_figural_stem_question()
                                      # succeeds for that Q.
                                      # At gate check: any entry with rendered=false → HARD FAIL.
                                      # Empty {} when figural_present is False or no FIGURAL
                                      # subtopics exist in this mock.
  }
  json.dump(batch_state, open(f'/home/claude/{EXAM}_M{N}_batch_state.json', 'w'))
  ```

## S3-17 — Mandatory subtopic + alternation pre-check (v3.4 — manifest-driven)

  v3.4 CHANGE: This check no longer uses hardcoded literal strings like
  'Mensuration 3D' / 'Direction Sense'. Those caused false hard stops because the
  blueprint used different (granular) display names. It now reads the STRUCTURED
  mandate data from the Step 0 manifest and checks by subtopic_id. Fully
  exam-agnostic — zero subtopic names hardcoded.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  MANDATORY_IDS = set(manifest.get('mandatory_every_mock', []))
  ALT_GROUPS    = manifest.get('alternation_groups', {})   # group -> [ids]
  MANDATORY_GROUPS = manifest.get('mandatory_groups', {})  # v5.0 group -> {members:[ids], min}
  MIN_COUNTS       = manifest.get('min_counts', {})        # v5.0 id -> k
  # manifest.cadence_windows is INTENTIONALLY NOT checked here. Cadence is a CROSS-mock
  # constraint (>=1 every N mocks) and is unobservable from a single mock; it is enforced
  # solely by Step 1 RULE M5 (full-series pass). A Step 7 cadence gate would be a category
  # error and would false-stop every legitimately-skipped mock. Do not add one.

  # Flatten ids AND total q_counts allocated in THIS mock (across sections):
  mock_ids = set()
  mock_counts = {}
  for sec_name, id_map in alloc_ids.items():
      mock_ids |= set(id_map.keys())
      for sid, info in id_map.items():
          mock_counts[sid] = mock_counts.get(sid, 0) + info['q_count']

  problems = []

  # CHECK 1 — mandatory_every_mock: every mandated id must be present this mock.
  for mid in MANDATORY_IDS:
      if mid not in mock_ids:
          disp = MANIFEST_IDS.get(mid, {}).get('display_name', mid)
          problems.append(f"MANDATORY subtopic absent: {mid} ('{disp}')")

  # CHECK 2 — alternation groups: at most ONE member per mock.
  for group, members in ALT_GROUPS.items():
      present = [m for m in members if m in mock_ids]
      if len(present) > 1:
          disps = [MANIFEST_IDS.get(m, {}).get('display_name', m) for m in present]
          problems.append(
              f"ALTERNATION violated: group '{group}' has {len(present)} members "
              f"in this mock ({', '.join(disps)}); at most 1 allowed.")

  # CHECK 3 — mandatory_groups (GROUP-PRESENCE, v5.0/Issue 2b): >=min members present.
  for group, spec in MANDATORY_GROUPS.items():
      members = spec.get('members', [])
      need    = spec.get('min', 1)
      have    = sum(1 for m in members if mock_counts.get(m, 0) > 0)
      if have < need:
          disps = [MANIFEST_IDS.get(m, {}).get('display_name', m) for m in members]
          problems.append(
              f"GROUP-PRESENCE violated: group '{group}' needs >={need} of "
              f"[{', '.join(disps)}] present, but only {have} in this mock.")

  # CHECK 4 — min_counts (MIN-COUNT, v5.0/Issue 2b): id must have >=k questions.
  for mid, k in MIN_COUNTS.items():
      c = mock_counts.get(mid, 0)
      if c < k:
          disp = MANIFEST_IDS.get(mid, {}).get('display_name', mid)
          problems.append(
              f"MIN-COUNT violated: {mid} ('{disp}') has {c}Q allocated, needs >={k}.")

  if problems:
      raise SystemExit(
          "HARD STOP [HS:INPUT] (S3-17): blueprint mandate/alternation violations for Mock "
          f"{N}:\n  - " + "\n  - ".join(problems) +
          "\n\nThese are BLUEPRINT defects (Step 1 should prevent them at build "
          "time under Framework_Blueprint v1.11 RULE M1/M2/M4/M5/M6). Fix: "
          "regenerate the blueprint with v1.11 (enforces mandates by construction), "
          "or correct this mock's allocation, then retry. Step 7 never auto-edits the "
          "blueprint to resolve this (its only in-run edits are S3-2D and ladder R5).")
  ```

  NOTE ON THE OLD FALSE ALARMS: under the manifest contract, "Mensuration 3D
  absent" can only fire if the manifest actually flags a 3D-mensuration id as
  mandatory_every_mock AND no such id is in the mock. Granular names like
  "Right Circular Cone" now resolve through ids, so a present-but-differently-
  named mandatory subtopic is correctly recognised and does NOT false-stop.

## S3-17b — Axis-1/Axis-3 pre-flight feasibility (advisory, v5.50/v5.51 — GAP-2026-08-12-AXIS-PREFLIGHT / GAP-2026-08-12-AXIS3-PREFLIGHT)

  WHY THIS EXISTS. `blueprint_core.axis1_feasibility` (Framework_Blueprint.md §7-7,
  B1/blueprint-build time) already answers "does this SECTION have ANY PYQ subtopic
  capable of each targeted format, ever" — necessary but not sufficient. A mock can
  pass that section-wide check and still be drafted from a subset of subtopics that
  happens to under-represent (or entirely omit) the format/mechanism-capable ones THIS
  mock needed, purely from how the window's rotation/quota split landed for this
  specific mock — `axis1_feasibility` cannot see that, because it runs once, at
  blueprint-build time, before any mock's specific allocation exists (Mock-10
  root-cause gap analysis §5.5/§13 row 2: "A-AXIS1/A-AXIS3 invisible before Final
  Assembly"). This mock's `subtopic_allocations` ARE finalised by this point (S3-2/
  S3-8, above) — well before Batch 1 drafts a single question — so the narrower,
  mock-specific question CAN be answered here: "given EXACTLY the subtopics allocated
  to THIS mock, and assuming every single capable slot renders in the targeted
  format/mechanism, can this mock structurally reach its own target?" If not, no
  amount of steering during drafting can fix it — the allocation itself is short — and
  the operator should know that BEFORE spending effort drafting 60 questions that
  Final Assembly's A-AXIS1/A-AXIS3 gate will fail regardless.

  v5.50 shipped AXIS-1 (stimulus format: TEXT/FIGURAL/PASSAGE/DI) only, deliberately.
  Axis-3 (mechanism: MCQ/MSQ/NAT) was named but withheld, because
  `Framework_MockTestCreate v5.30`'s POSITION-BASED QUESTION TYPE DISPATCH
  (`_resolve_answer_axes`, §3 S3-2 above) means that whenever this EXAM's
  marking_scheme declares more than one distinct `question_type` ANYWHERE
  (`_position_based_typing`, an EXAM-WIDE flag computed once in S3-2 — not a
  per-section property), every question's mechanism in EVERY section is decided by
  its Q-POSITION (defaulting to MCQ for any Q outside a declared range), never by the
  allocated subtopic's own `answer_cardinality`/`answer_type`. A naive subtopic-
  capability check would therefore be MEANINGLESS at best and ACTIVELY MISLEADING at
  worst on such an exam — not only inside the sections `axis3_mechanism_lock`
  (Framework_Blueprint v1.48, GAP-2026-08-12-AXIS3-MECHLOCK) marks locked, but in
  EVERY section, since an un-locked "gap" Q-range on a position-based exam still
  resolves via `_type_for_q`'s own MCQ default, not via subtopic capability.
  v5.51 (GAP-2026-08-12-AXIS3-PREFLIGHT) closes this correctly: `bc.axis3_mock_
  feasibility` takes `_position_based_typing` (the SAME S3-2 variable, not a
  recomputed copy — see its own docstring for the full reasoning) as a REQUIRED
  parameter and returns `{}` UNCONDITIONALLY whenever it is True, so the check is
  simply inert — never wrong — on any exam where it would not be meaningful.

  ADVISORY ONLY — never a HARD STOP [HS:PROSE], mirroring `axis1_feasibility`'s own established
  contract exactly ("Subtopic is hard #1"; Axis-1/Axis-3 are locked CONSEQUENCES of
  allocation, steered and audited within tolerance, never force-blocking on it).
  Absent-safe: no `axis_schedule` (pre-v1.23 blueprint), a section whose status isn't
  'ok', or no target for an axis ⇒ silently skipped for that axis/section,
  byte-identical to every exam that predates this.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # v5.50/v5.51 (GAP-2026-08-12-AXIS-PREFLIGHT / GAP-2026-08-12-AXIS3-PREFLIGHT).
  # Axis-1: composes THIS MOCK's own target (the rotating FIGURAL series value for
  #   mock N, substituted into the flat per-mock target — every other format in
  #   axis1_target_per_mock does not rotate) and checks it via bc.axis1_mock_feasibility.
  # Axis-3: axis3_target_per_mock does not rotate per mock (no series to substitute) —
  #   checked directly via bc.axis3_mock_feasibility, gated by _position_based_typing
  #   (the S3-2 variable, reused as-is — NEVER recomputed here).
  # v5.53.2 (GAP-2026-08-12-S3-17B-BC-UNBOUND, found by spec_name_audit.py): this block
  # runs at SESSION START (§3), but this file's only `import blueprint_core as bc` lived
  # at §7 S7-NEW-B — a block that executes LATER. Reading `bc` here was therefore a
  # NameError in strict execution order — the same class as GAP-2026-08-12-S13-4-
  # UNDEFINED-BATCHES-COMPLETED. Bound explicitly here (v5.34's own rule: a new read
  # states its import; re-importing at S7-NEW-B is a harmless no-op).
  import blueprint_core as bc
  axis1_preflight_shortfalls = {}
  axis3_preflight_shortfalls = {}
  for sec_name, id_map in alloc_ids.items():
      sec_sched = axis_schedule.get(sec_name)
      if not sec_sched or sec_sched.get('status') != 'ok':
          continue                                        # absent-safe: dormant/no_pyq section
      _alloc_counts = {sid: info['q_count'] for sid, info in id_map.items()}

      _target1 = dict(sec_sched.get('axis1_target_per_mock') or {})
      if _target1:
          _series = sec_sched.get('axis1_target_series') or []
          if _series:
              _target1['FIGURAL'] = _series[(N - 1) % len(_series)]
          _sf1 = bc.axis1_mock_feasibility(_target1, _alloc_counts, MANIFEST_IDS)
          if _sf1:
              axis1_preflight_shortfalls[sec_name] = _sf1

      _target3 = sec_sched.get('axis3_target_per_mock') or {}
      if _target3:
          _sf3 = bc.axis3_mock_feasibility(_target3, _alloc_counts, MANIFEST_IDS,
                                           position_based_typing=_position_based_typing)
          if _sf3:
              axis3_preflight_shortfalls[sec_name] = _sf3
  ```

  If `axis1_preflight_shortfalls`/`axis3_preflight_shortfalls` is non-empty, S3-18's
  summary (below) prints an AXIS PRE-FLIGHT ADVISORY block naming each short
  section/format-or-mechanism/target/max-achievable triple, then proceeds to
  "Type 'continue' to begin Batch 1" exactly as it always has — this NEVER blocks, and
  NEVER changes which subtopics are allocated or how Batch 1 drafts. It exists solely
  so the operator sees a structurally-doomed mock BEFORE drafting it, instead of only
  at Final Assembly after 60 questions already exist (the exact, expensive
  discovery-order failure this check exists to shorten).

## S3-17c — FIGURE-TYPE SESSION PRE-FLIGHT (v5.88 — LAW F1.4/F1.5; HS-17; runs BEFORE the S3-18 summary)

  Step 6 proved every dominant figure type is REGISTERED and SUPPORTED. This session must
  prove it can actually LOAD the renderer for every one this paper needs, before Q.1.
  Measured cost of not doing so: corpus_io.structure_draw_fn raises ValueError the first
  time a reaction is drawn, mid-batch, after questions exist.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import os, json
  import blueprint_core as bc
  try:
      import figure_types as ft
  except ImportError:
      raise SystemExit("HARD STOP [HS:INFRA] (S3-17c / HS-17): figure_types.py is not in the verified "
                       "clone — re-run SKILL Step 0.")
  FT_SESSION = ft.preflight()                       # which renderers THIS session can load
  _blocks = bc.parse_image_analysis_blocks(sr_text)              # S3-2's section_rules text
  _mine = next((mk for mk in bp.get('mocks', []) if mk.get('mock') == N), None) or {}
  _my_allocs = [a for s in _mine.get('sections', []) for a in s.get('subtopic_allocations', [])]
  FIGURAL_FALLBACKS = dict(bp.get('figural_fallbacks') or {})      # Step 6 v1.61.0 / 6S v1.11.0
  # The policy travels with a v1.61.0+ blueprint; a pre-v1.61.0 blueprint has none, so the
  # exam's own config decides (the same key Step 6 reads). Default hard_stop.
  _policy = (bp.get('figure_type_coverage') or {}).get('policy')
  if not _policy:
      _cfg_path = f'/mnt/project/{EXAM}_exam_config.json'
      _cfg = json.load(open(_cfg_path, encoding='utf-8')) if os.path.exists(_cfg_path) else {}
      _policy = str(_cfg.get('figure_fallback_policy', 'hard_stop')).strip().lower()
  if _policy not in bc.FIGURE_FALLBACK_POLICIES:
      raise SystemExit(f"HARD STOP [HS:INPUT] (S3-17c): figure_fallback_policy={_policy!r} is not one of "
                       f"{bc.FIGURE_FALLBACK_POLICIES}. Fix exam_config.json / the blueprint.")
  KIND_COVERAGE = bc.kind_coverage_preflight(
      _my_allocs, _blocks, lambda types: ft.coverage(types, session=FT_SESSION),
      policy=_policy, normalise=ft.normalise)
  for _line in KIND_COVERAGE['advisories']:
      print(f"S3-17c advisory: {_line}")
  for _line in KIND_COVERAGE['unavailable']:
      print(f"S3-17c note: {_line}")       # informational when a loadable dominant sibling remains (E7)
  _stops = list(KIND_COVERAGE['blockers'])
  if KIND_COVERAGE['unavailable_blocking']:    # NO dominant member of that subtopic is loadable here
      _stops += [f"{u} — missing: {FT_SESSION['missing']}. Run: pip install matplotlib pillow "
                 f"numpy scipy fonttools rdkit --break-system-packages, then re-run the trigger."
                 for u in KIND_COVERAGE['unavailable_blocking']]
  if _stops:
      raise SystemExit("HARD STOP [HS:INFRA] (S3-17c, HS-17 — LAW F1 FIGURE-TYPE-COVERAGE): this paper "
                       "needs a figure type this session cannot render:\n  " + "\n  ".join(_stops))
  _new_fb = {s: ty for s, ty in KIND_COVERAGE['fallbacks'].items() if s not in FIGURAL_FALLBACKS}
  if _new_fb:
      # Only a pre-v1.61.0 / pre-v1.11.0 blueprint reaches here (a current one allocated the
      # subtopic TEXT and recorded it). A fallback computed in-session would be rendered but
      # NEVER disclosed — the Deliver footer reads blueprint.figural_fallbacks — so the one
      # honest move is to have the blueprint record it. Type-2 stop, one operator action.
      raise SystemExit(f"HARD STOP [HS:INPUT] (S3-17c, HS-17): policy text_disclosed applies to {sorted(_new_fb)} "
                       f"but this blueprint predates the KIND-COVERAGE record (no figural_fallbacks). "
                       f"Regenerate it with Framework_Blueprint v1.61.0+ / Framework_ScopedBlueprint "
                       f"v1.11.0+ (the fallback is then allocated TEXT and disclosed in every footer), "
                       f"then re-run this trigger.")
  # A fallback subtopic is TEXT for this paper — in EVERY place Step 7 reads a subtopic's
  # format (S3-18 manifest, S4-5 CHECK 5, S4-7 FORMAT DISPATCH, S7-NEW-B0 budget): the
  # section_rules format field says FIGURAL (Step 5 wrote it; Step 6 does not rewrite
  # section_rules), so the override lives here and S13-4 refuses a figure on such a subtopic.
  FORMAT_OVERRIDE = {_sid: 'TEXT' for _sid in FIGURAL_FALLBACKS}
  if FIGURAL_FALLBACKS:
      print("S3-17c: text_disclosed fallbacks for this series (rendered TEXT, disclosed in the "
            f"footer): {FIGURAL_FALLBACKS} — FORMAT_OVERRIDE forces TEXT for them in this session.")
  print(f"S3-17c FIGURE-TYPE SESSION PRE-FLIGHT: {KIND_COVERAGE['checked']} dominant-mode "
        f"subtopic(s) checked; renderers loadable: "
        f"{sorted(k for k, v in FT_SESSION['renderers'].items() if v)}")
  ```

  A subtopic in FIGURAL_FALLBACKS was allocated TEXT by Step 6 for every paper of the series
  and keeps its slot; it renders through the ordinary TEXT path, has no figure record, and so
  is simply absent from A-FIGPROFILE / A-FIGTYPE-KIND. The footer prints one line per
  fallback (Framework_DeliveryFooter §FOOTER-FT). sr_text is the
  section_rules text S3-2 loaded; a pre-v2.37 section_rules (no PYQ_IMAGE_ANALYSIS) checks
  nothing and stops nothing (EC-V18).

## S3-18 — Display session start summary + batch plan

  Print in chat after all checks pass:

  ```
  === MockCreate — Session Start ===
  Exam     : [exam_name] ([ExamCode])
  Mock     : M[N] of [total_mocks]
  Questions: [total_questions]
  Sections : [count] | Difficulty: S=[n_simple] M=[n_medium] H=[n_hard]
  Formats  : PASSAGE=[T/F] FIGURAL=[T/F] DI=[T/F]
  Guard    : [Audit script available / Manual checklist mode]
  Registry : [len(mocks_done)] mocks completed
  ──────────────────────────────────────────────────
  BATCH PLAN:
  Batch | Section          | Q-Range  | Qs
  ──────────────────────────────────────────────────
  1     | [Section 1]      | Q1–Q10   | 10
  2     | [Section 1]      | Q11–Q20  | 10
  ...
  N     | [Last Section]   | Qx–Qy    |  z   ← FINAL BATCH
  ──────────────────────────────────────────────────

  FIGURAL MANIFEST (v5.13 — when figural_present is True):
  ──────────────────────────────────────────────────
  Scan all subtopic_allocations for this mock and list every subtopic
  whose section_rules format == FIGURAL and that is NOT in FORMAT_OVERRIDE
  (S3-17c: a text_disclosed fallback subtopic is TEXT). For each, read image_role from
  PYQ_IMAGE_ANALYSIS (default 'stem_and_options' if absent):

  FIGURAL Qs (matplotlib rendering required — S7-NEW-B OPTION A):
  Batch | Q#   | Subtopic ID          | image_role       | Rendering
  ──────────────────────────────────────────────────────────────────────
  [b]   | Q[n] | [subtopic_id]        | stem_and_options | problem PNG(s) + [k] option PNGs
  [b]   | Q[m] | [subtopic_id]        | stem_only        | problem PNG(s) + TEXT options
  [b]   | Q[p] | [subtopic_id]        | options_only     | TEXT stem + [k] option PNGs
  ...
  ──────────────────────────────────────────────────────────────────────
  Total: [count] figural Qs across [b_count] batches.
  Helper dispatch: stem_and_options/options_only → add_figural_question()
                   stem_only                     → add_figural_stem_question()
  Text descriptions are BANNED (S7-NEW-B OPTION C).

  Also populate batch_state.figural_qs with one entry per Q listed above:
    figural_qs[str(qnum)] = {subtopic_id, image_role, rendered: false}

  If figural_present is False: omit this table entirely.
  The Q# assignment IS the placement plan built at S3-12b and persisted in
  batch_state['subtopic_by_qnum']. This manifest READS it; it never computes
  it (v5.77 — the pre-v5.77 "blueprint order" sentence here was guaranteed
  non-conforming with R19 for any subtopic with q_count >= 2).
  This manifest is INFORMATIONAL — the authoritative format source remains
  section_rules format field per subtopic_id, overridden to TEXT by
  FORMAT_OVERRIDE (S3-17c) for a text_disclosed fallback subtopic.
  ──────────────────────────────────────────────────

  AXIS-1 PRE-FLIGHT ADVISORY (v5.50 — when axis1_preflight_shortfalls, S3-17b, is
  non-empty; omit this block entirely when it is empty):
  ──────────────────────────────────────────────────
  ⚠ This mock's subtopic allocation may not be able to reach its Axis-1 target even
    if every capable slot renders in the targeted format:
      [Section] — [format]: target=[N], max_achievable=[M] (allocation short by [N-M])
      ...
  Not a HALT — Subtopic is hard #1; Final Assembly's A-AXIS1 gate audits the actual
  outcome within tolerance regardless. Shown so a structural shortfall is visible
  before Batch 1, not only after 60 questions already exist.
  ──────────────────────────────────────────────────

  AXIS-3 PRE-FLIGHT ADVISORY (v5.51 — when axis3_preflight_shortfalls, S3-17b, is
  non-empty; omit this block entirely when it is empty — including on any exam where
  _position_based_typing is True, since bc.axis3_mock_feasibility returns {} there
  unconditionally, so this block simply never has anything to report):
  ──────────────────────────────────────────────────
  ⚠ This mock's subtopic allocation may not be able to reach its Axis-3 target even
    if every capable slot renders in the targeted mechanism:
      [Section] — [mechanism]: target=[N], max_achievable=[M] (allocation short by [N-M])
      ...
  Not a HALT — Subtopic is hard #1; Final Assembly's A-AXIS3 gate audits the actual
  outcome within tolerance regardless. Shown so a structural shortfall is visible
  before Batch 1, not only after 60 questions already exist.
  ──────────────────────────────────────────────────

  Answer budget: built and written to [EXAM]_M[N]_answer_budget.json
  All checks passed. Type 'continue' to begin Batch 1.
  ```
  STOP HERE. Wait for "continue".

## S3-19 — HARD STOP [HS:INPUT] / [HS:INFRA] conditions (each line carries its own class)

  HS-1: Any mandatory file missing from /mnt/project/
  HS-2: Section allocation sums mismatch
  HS-3: ExamCode mismatch between trigger/blueprint/registry
  HS-4: paper_id already in registry.papers_completed (legacy: Mock N in mocks_completed)
  HS-5: Audit script self-test fails (if audit.py present)
  HS-6: blueprint.json invalid JSON
  HS-7: section_rules.md empty
  HS-8: Mandatory subtopic absent from blueprint — detected by id via manifest
        mandatory_every_mock (S3-17), NOT by hardcoded name.
  HS-9: subtopic_manifest.json missing (S3-8 contract gate).
  HS-10: A blueprint subtopic_id not found in manifest or section_rules
        (S3-8 contract gate) — names drifted; re-run Step 0/Step 1.
  HS-11: Legacy blueprint without subtopic_id fields (S3-8) — regenerate with
        Framework_Blueprint v1.7+ or run the one-time id migration.
  HS-12: Alternation group has 2+ members in one mock (S3-17).
  HS-13: mandatory_groups group has <min members present in one mock (S3-17 CHECK 3,
        Issue 2b). Blueprint defect — Step 1 RULE M4 should prevent by construction.
  HS-14: min_counts id has <k questions in one mock (S3-17 CHECK 4, Issue 2b).
        Blueprint defect — Step 1 RULE M6 should prevent by construction.
  HS-15: (v5.13) figural_present is True but zero subtopics in this mock have
        section_rules format==FIGURAL. Either the blueprint flag is wrong
        (should be False) or section_rules format fields are stale.
        Non-blocking WARN (not HARD STOP [HS:PROSE]): figural_present may be series-level
        — this specific mock simply has no figural Qs while others in the series do.
  HS-15a: (v5.13 REVERSE; v5.88 SELF-CORRECTING — LAW F3.4) figural_present is False
        but ≥1 subtopic in this mock has format==FIGURAL. The blueprint flag is wrong.
        Pre-v5.88 this was described as "reducing early warning"; its ACTUAL cost was
        that S3-18, S4-5 CHECK 5 AND the S13-4 figure-record commit were skipped, so
        the paper shipped with no object_types / figure_specs / semantic_objects and
        every figure gate dormant-green (6 of 21 scoped papers on the reference exam).
        Now: S3-2a derives the flag from the allocation (bc.derive_presence_flags), sets
        figural_present=True in session, prints the correction, and proceeds — S3-18 and
        CHECK 5 run, S13-4 commits on existence regardless (final_assembly v1.10). Still
        non-blocking, because the correct state is now known. Same for di_present /
        passage_present. Regenerate the blueprint with ScopedBlueprint v1.11.0+.
  HS-17: (v5.88 — LAW F1 FIGURE-TYPE-COVERAGE) S3-17c FIGURE-TYPE SESSION PRE-FLIGHT
        found a dominant figure type this paper needs that (a) the registry marks
        UNSUPPORTED with no text_disclosed fallback recorded in the blueprint, or (b) is
        supported but its renderer cannot load IN THIS SESSION (rdkit / matplotlib absent).
        HARD STOP [HS:INFRA] naming subtopic, type and the ONE operator action: (a) regenerate the
        blueprint under figure_fallback_policy text_disclosed; (b) run the SKILL Step 0
        pip line and re-run the trigger. A Type-2 input-integrity stop: nothing was
        authored, so nothing is lost; a figure can never be discovered unrenderable at Q.14.
  HS-16: (v5.13) FIGURAL_BANNED subtopic has no valid REPLACEMENT_RULE. See S3-11.
        HARD STOP [HS:INPUT] — S7-NEW-B OPTION B replacement will fail silently without it.


# ════════════════════════════════════════════════════════════════════════
# §4 — BATCH ARCHITECTURE (v3.0 — DEFINITIVE REWRITE)
# This is the single most critical section. Read every rule.
# ════════════════════════════════════════════════════════════════════════
#
# WHY THIS SECTION EXISTS:
#   In the M1 production failure, Claude generated all 100 questions in ONE
#   response instead of stopping after each 10-question batch. This section
#   makes that failure mechanically impossible by removing every ambiguity
#   and adding a self-check Claude must perform before ending each response.
#
# THE GOVERNING PRINCIPLE:
#   ONE BATCH = ONE RESPONSE. NO EXCEPTIONS EXCEPT THE FINAL BATCH.
#   A "batch" is at most 10 questions from a single section.
#   After delivering a batch, Claude's response ENDS. The next batch begins
#   only when the user sends "continue" / "go" / "next".
  HS-16: (v5.77 — GAP-2026-08-28-RDKIT-UNDECLARED) STRUCTURE-RENDERER
        PRE-FLIGHT. If ≥1 subtopic allocated to THIS paper has section_rules
        format==FIGURAL, run figural_core.preflight() and require
        preflight()['can_render_structures'] (rdkit importable). HARD STOP [HS:INFRA]
        with the exact install line — `pip install matplotlib pillow numpy
        scipy fonttools rdkit --break-system-packages` — if it is False.
        WHY BEFORE Q.1: corpus_io.structure_draw_fn RAISES when rdkit is
        unavailable (a STRUCTURE figure is never hand-drawn), so a missing
        renderer discovered at the first molecule aborts a paper mid-batch
        after all of S3 passed; the Explain route's canonical_structure
        degrades softly, which is exactly why only the Create route needs
        this stop. rdkit is declared in figural_core.DEPENDENCIES and
        installed by the SKILL Step 0 line from v5.77, so this stop fires
        only in a genuinely broken environment. Non-figural papers: skip.

## S4-1 — What a batch is (precise definition)

  A batch is a unit of generation with these exact properties:
    - Contains AT MOST 10 questions (MAX_BATCH_SIZE = 10)
    - All questions come from ONE section (never spans two sections)
    - Has a fixed q_start and q_end read from batch_state.json
    - Is generated, gate-checked, delivered, then the response ENDS

  A batch is NEVER:
    - More than 10 questions
    - Questions from two different sections
    - Generated in the same response as another batch
    - Started without an explicit user "continue" (except Batch 1, which
      starts after the user types "continue" following session start)

## S4-2 — Batch plan computation (the ONLY source of batch boundaries)

  Built once at session start (S3-16). Written to batch_state.json.
  NEVER recomputed mid-session. NEVER derived from memory or "the last Q + 1".

  ALGORITHM (deterministic):
    MAX_BATCH_SIZE = 10
    batch_id = 1
    FOR each section in sections[] (ordered by q_range start ascending):
        q = section.q_range[0]
        WHILE q <= section.q_range[1]:
            batch_q_end = MIN(q + 9, section.q_range[1])
            record batch {batch_id, section, q_start=q, q_end=batch_q_end,
                          q_count = batch_q_end - q + 1, is_final=False}
            batch_id += 1
            q = batch_q_end + 1
    MARK the last batch in the list: is_final = True

  KEY PROPERTIES:
    - A section with 25 questions → batches of 10, 10, 5
    - The 5-question batch is the section remainder (always ≤ 10)
    - Sections never share a batch
    - Exactly one batch in the whole plan has is_final = True

## S4-3 — batch_state.json schema (the batch processing brain)

  ```json
  {
    "exam_code": "[ExamCode]",
    "mock_n": N,
    "paper_id": "MOCK:M0N",
    "total_questions": 100,
    "batch_plan": [
      {"batch_id": 1, "section": "Section_A", "q_start": 1, "q_end": 10,
       "q_count": 10, "is_final": false},
      {"batch_id": 2, "section": "Section_A", "q_start": 11, "q_end": 20,
       "q_count": 10, "is_final": false},
      ...
      {"batch_id": 10, "section": "Section_D", "q_start": 91, "q_end": 100,
       "q_count": 10, "is_final": true}
    ],
    "batches_completed": [],
    "current_batch": 1,
    "mechanics_used": {},
    "templates_used": {},
    "rotation_state": {},
    "passage_linked_qs": [],
    "cloze_linked_qs": [],
    "concept_ledger": [],
    "presentation_ledger": [],
    "figural_qs": {}
  }
  ```

  current_batch: the batch_id to generate next. Starts at 1.
  batches_completed: list of batch_ids whose questions are in the docx AND
                     passed gate checks AND were delivered. Updated ONLY
                     after present_files succeeds for that batch.
  concept_ledger: list of scenario_key strings already used in THIS mock
                  (DOUBT-3 / S6-3b RULE B). Checked before every new Q and
                  persisted across batches so no scenario repeats anywhere in
                  the paper. Each subtopic still produces EXACTLY its blueprint
                  q_count (RULE A) — distinct scenarios fill those N slots.
  presentation_ledger: list of "concept_group||presentation_key" strings already
                  used in THIS mock for CLASS-2/3 questions (DOUBT-4 / §6-3c
                  RULE C, v3.9). Checked at CHECK 1b and persisted/rehydrated like
                  concept_ledger so no two same-group questions LOOK alike across
                  batches or across a resume.
  stimulus_groups (v5.85, set-placed papers ONLY — absent on a legacy paper):
                  {group_id: {type, qnums, members, stimulus, stimulus_sha256}} from
                  S3-12b; 'stimulus' is filled once by stim_register (R-STIMGROUP).
  stimulus_profile_snapshot (v5.85, with stimulus_groups): the profile this paper
                  was planned with; S3-12b rewrites it to
                  /home/claude/[ExamCode]_M[N]_stimulus_profile.json for every audit.

## S4-4 — The Batch Stop Law (B-1 through B-8 — ARCHITECTURAL, NON-NEGOTIABLE)

  These are not guidelines. They are the same class of rule as MANDATE 0.

  B-1: batch_state.json MUST exist and be valid before Q1 of any batch.
       If missing → rebuild from blueprint + existing docx (S4-12), then proceed.

  B-2: The q_start and q_end for the batch being generated come ONLY from
       batch_state.json batch_plan[current_batch - 1]. NEVER from memory.
       NEVER computed as "previous batch end + 1" without reading the file.

  B-3: Generate EXACTLY q_count questions for the current batch. Not one more.
       If current batch q_count is 5, generate 5 — even if it "feels" like
       there is room for 10. The plan is authoritative.

  B-4: AUTO-ADVANCE IS PERMANENTLY BANNED.
       After delivering a batch (present_files called), the response ENDS.
       FORBIDDEN in the same response after a batch delivery:
         - Generating the next batch's questions
         - "Let me now continue with Batch N+1..."
         - "I'll go ahead and generate the next section..."
         - A "preview" or "head start" on the next batch
         - ANY question content beyond the current batch
       The ONLY thing after present_files is the STOP line (S4-7 STEP E)
       and then the response ENDS.

  B-5: The next batch begins ONLY when the user's NEW message is a continue
       trigger ("continue" / "go" / "next", case-insensitive).
       Claude NEVER self-issues a continue. Claude NEVER assumes continue.

  B-6: batches_completed is updated (append current_batch's batch_id) and
       current_batch is incremented ONLY after present_files succeeds.
       This update is written to batch_state.json before the response ends.

  B-7: present_files is FORBIDDEN until S4-7 STEP A2 printed `STEP A2: DONE` for the batch (v6.1 S0-BV —
       every question measured by fresh graders and solvers in its own batch) and the batch passes gate checks:
       Layer 1 checklist all-pass, AND Layer 2 audit script exit 0 whenever
       the audit script is available (v5.77 — was OR; five checklist items
       have no auditor equivalent, so the auditor alone was strictly weaker
       while being presented as interchangeable).

  B-8: The FINAL batch (is_final=True) is the ONLY batch that does NOT end
       with a continue prompt. It auto-triggers Final Assembly (§13) in the
       SAME response. See S4-9.

## S4-5 — Pre-batch self-check (MANDATORY before generating any batch)

  Before generating questions for a batch, Claude MUST silently verify:

    CHECK 1: Read batch_state.json. Confirm current_batch value.
    CHECK 2: Read batch_plan[current_batch - 1]. Get section, q_start, q_end, q_count.
    CHECK 3: Confirm this batch_id is NOT already in batches_completed.
             (If it is → the user re-triggered; advance to the true next batch.)
    CHECK 4: Confirm the user's last message was a continue trigger
             (or, for Batch 1, the continue following session start).
             If NOT a continue trigger → do NOT generate. Answer the user
             and re-show the continue prompt.
    CHECK 5: (v5.13) If any subtopic in this batch has section_rules
             format==FIGURAL (read by subtopic_id):
               Scan batch_state.figural_qs for Q numbers in this batch's range.
               For each found, read its image_role and print in chat:
                 "⚠ FIGURAL Qs in this batch:
                    Q.[x] ([subtopic_id]) — image_role=[role] → [helper name]
                    Q.[y] ([subtopic_id]) — image_role=[role] → [helper name]
                  matplotlib rendering required. Text descriptions BANNED (S7-NEW-B)."
               If FIGURAL_BANNED for any subtopic in this batch:
                 "Q.[z] ([subtopic_id]) — FIGURAL_BANNED → OPTION B replacement
                  using REPLACEMENT_RULE subtopic."
             If no FIGURAL subtopics in this batch: skip CHECK 5 silently.
             If figural_present is False: skip CHECK 5 silently (v5.88: figural_present
             is the S3-2a DERIVED value, so this branch means the allocation truly
             carries no FIGURAL subtopic — never a stale blueprint flag).

  Only after all 5 checks pass does generation begin.

## S4-6 — The continue contract (exact behaviour)

  ACCEPTED CONTINUE TRIGGERS (case-insensitive, trimmed):
    "continue", "go", "next", "continue.", "go ahead", "next batch", "proceed"

  IF the user message IS a continue trigger:
    → v5.91: FIRST, if batch_state.state == 'DELIVERED' (set at S13-9): the paper is finished
      — say so and stop; generate and deliver nothing.
    → v5.91: if every batch is already authored AND (the S3-1-resolved registry has no
      committed question_index entry for this paper, OR batch_state.state is one of
      REVIEW_RUNNING / REVIEW_REPAIR / REVIEWED / AWAITING_REVIEW) — an interrupted Final
      Assembly — run S4-12 instead: it resumes §13 / S13-2G in the same response (S13-4's
      commit is idempotent). Never print a continue prompt then.
    → Otherwise: run S4-5 pre-batch self-check.
    → Generate the next batch.

  IF the user message is NOT a continue trigger (a question, a correction,
  a new instruction):
    → Do NOT generate a batch.
    → Address the user's message fully.
    → End the response with the standing continue prompt:
      "Ready for Batch [current_batch] → [section] Q[start]–Q[end] ([count]Q).
       Type 'continue' when ready."

  IF the user message is a correction to an already-delivered batch:
    → Apply the fix to that batch in the cumulative docx.
    → Re-run gate checks. Re-deliver via present_files.
    → Do NOT advance current_batch.
    → End with the continue prompt for the SAME next batch.

## S4-7 — Per-batch delivery protocol (the 6 steps — execute in order)

  STEP A — GENERATE: Produce exactly q_count questions for current_batch.
           v6.1 (S0-BV BV-2): BEFORE writing each question, print its author packet and write the question
           ONCE against it — the same anchors its fresh graders will compare with, and the recipe range.
           v6.3 (S0-BV BV-10): the packet's 'target_text' is the slot band as THIS exam's past questions of the
           same subtopic (else topic, section, exam) measured it — facets, inferential steps, distinct
           principles, score range. Write to it, then count your own solution with 'counting_rules' (list the
           moves and the principles): bc.br_band(counts, qtype, labels) must give the slot band. The reviewers
           count the same way and their counts decide the band:
           ```python
           # ── S4-7 STEP A author packet (v6.1 BV1) ──
           import json, blueprint_core as bc
           def BV_AUTHOR_PACKET(q, subtopic_id, qtype='mcq', ask_format=None):
               _bs_ap = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
               _labs_ap = list(_bs_ap.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
               _band_ap = ((_bs_ap.get('difficulty_plan_target') or _bs_ap.get('difficulty_plan') or {}).get(str(q)))
               _ru_ap = globals().get('EXAM_RULER') or {}
               _sj_ap = bc.nf_subject_key({'subtopic_id': subtopic_id}, globals().get('manifest') or {})
               _rc_ap = (((_ru_ap.get('recipe_by_subject') or {}).get(_sj_ap) or {}).get(_band_ap)
                         or (_ru_ap.get('recipe') or {}).get(_band_ap) or {})
               _pk_ap = bc.bv_author_packet({'q': q, 'band': _band_ap, 'qtype': qtype, 'subtopic_id': subtopic_id,
                                             'ask_format': ask_format},
                                            bc.bv_anchors(globals().get('EXEMPLAR_BANK') or {}, _ru_ap, subtopic_id, qtype, _labs_ap),
                                            _labs_ap, _rc_ap, _ru_ap)
               print(json.dumps(_pk_ap, ensure_ascii=False, default=str)[:6000])
               return _pk_ap
           ```
           Write them to the cumulative docx (append to prior batches' Qs).
           Write each question's answer to the sidecar immediately (S11-2).
           Apply ALL generation rules (§7), format rules (§8, §10),
           dedup (§6), self-containment (§9).

           FORMAT DISPATCH (v5.13 — per question, mandatory decision point):
             Read the subtopic's format from section_rules (by subtopic_id); if the
             subtopic_id is in FORMAT_OVERRIDE (S3-17c — a Step-6 text_disclosed
             fallback) the format is TEXT, whatever section_rules says (v5.88).
             IF format == FIGURAL AND bc.axis_grant_figural(...) GRANTED the slot:
               (v5.37 — format is ELIGIBILITY, not an imperative. The budget is asked
                FIRST, per S7-NEW-B0. A DENIED question does not come here at all: it
                takes OPTION B and renders TEXT from this same subtopic's observed
                PYQ_STEM_PATTERNS, keeping its slot, difficulty and cardinality.
                Pre-v5.37 this line read `IF format == FIGURAL:` with no cap, which
                shipped 26 and 30 figures against a budget of 4 — GAP-2026-08-06-AXIS1.)
               Read image_role from section_rules PYQ_IMAGE_ANALYSIS
               (default 'stem_and_options' if PYQ_IMAGE_ANALYSIS absent).

               ── FIGURE CONTENT PROFILE (v5.31, GAP-2026-07-26-003) ──────────
               Before generating, read the SEMANTIC half of PYQ_IMAGE_ANALYSIS —
               object_types, transformation_types, arrangement_types,
               complexity_dist — via bc.figural_generation_profile(). Until v5.31
               Step 7 read ONLY image_role, so Step 5 measured what the real
               figures CONTAIN and no step ever looked: the fields were written
               into section_rules and read by nothing. A generated figure could
               be a bar chart where every PYQ in that subtopic is a micrograph,
               and no gate would notice.

               import figure_types as ft                       # v5.88 — the registry
               profile = bc.figural_generation_profile(pyq_image_analysis,
                                                      normalise=ft.normalise)

               ── DISPATCH BY REGISTRY ROW (v5.88, LAW F1.5) ──────────────────
               The profile selects a TYPE; the type's registry row selects HOW it
               is drawn:  row = ft.lookup(object_type)
                 row['renderer']  == 'corpus_io.structure_draw_fn' → S7-NEW-B2
                                     STRUCTURE path (rdkit tile)
                                  == 'corpus_io.render_scheme'     → S7-NEW-B2
                                     REACTION path (scheme compositor)
                                  == 'figural_core.render_figure'  → data class
                                     (data_series / data_single per series count)
                                  == 'glyph_path'                  → S10-7
                                     render_figural_image (reasoning_glyph)
                                  == 'corpus_io.render_projection' → v6.0 (G-12):
                                     chair / Newman / sawhorse / Fischer / Haworth
                                     through the PROVEN renderers (S0-OP-8) — never
                                     hand-drawn; identity kind STRUCTURE_CONFORMER
                                  == 'hand_drawn+descriptor'       → matplotlib
                                     artists + a descriptor (MO_DIAGRAM,
                                     ORBITAL_BOXES, GENERIC …)
                 row['semantic_kinds'][0] is the kind the semantic object registers;
                 row['render_classes'] bounds the S10-6A class the FigureSpec declares.
               ── ASK TYPE (v5.89 — GAP-2026-11-02 F8) ─────────────────────────
               What the figure ASKS is apportioned like everything else the exam
               measures: the blueprint carries fig_ask_target_per_mock[N][section]
               ({ask_type: count}, bc.fig_ask_series over the series — a 5% type
               appears about every second paper and is never rounded away), and
               section_rules PYQ_IMAGE_ANALYSIS carries the subtopic's
               figural_ask_type_counts (Step 5, from PYQExplain's per-question
               tags; vocabulary figure_types.FIGURAL_ASK_TYPES — CHEMISTRY's: every
               non-chemistry figure is tagged "other", and a slot assigned "other"
               carries no ask-type constraint at all). Each figural slot
               takes ask_type = bc.assign_ask_type(remaining, subtopic_shares)
               (largest remaining target with share > 0 in this subtopic; ties:
               larger subtopic share, then alphabetical). Formats seen in the
               exam's PYQs are therefore produced in the exam's proportion —
               "identify the start", "the reagents", "which reaction A-D", "which
               structures A-D", stereoisomer counts, chairs, "+" partners — and the
               reagents-in-figure choice follows the subtopic's numbered_steps /
               reagent_as_structure share. RECORD figural_ask_type, representations
               and scheme_grammar on the item: pass them (and marked_sites) to
               write_q_to_sidecar (concept_map -> question_index, final_assembly v1.11).
               A-FIGFORMAT reports the per-paper mix (+/- max(1, 15%)); the ladder
               switches an over-target item only to an UNDER-target type valid for
               its subtopic (R3), so it never pushes another type out of band; a
               deviation it cannot remove is recorded as target infeasibility,
               never a defect. No target in the blueprint (built before v1.62.0 /
               ScopedBlueprint v1.12.0) or no counts in section_rules -> dormant.
               NEVER RECORD A TYPE WHOSE ROW WAS NOT THE ONE THAT RENDERED THE
               FIGURE. A 'reaction_scheme' label over a single-molecule tile is a
               FALSE RECORD (G-FIGTYPE-KIND HARD FAIL, S4-11), not a near miss —
               the reference registry held 287 of them.
               FALLBACK CONTRACT: a dominant type the session cannot render never
               reaches this point (S3-17c HARD STOP [HS:INFRA]s); a subtopic in
               FIGURAL_FALLBACKS was allocated TEXT by Step 6 and never enters the
               figural dispatch at all (disclosed by the footer). There is no third
               path — mislabelling and omission are both gated.
               An UNREGISTERED type (ft.lookup(...)['status'] == 'unregistered') draws
               as a GENERIC hand-drawn schematic, registers kind GENERIC with a
               descriptor, and is reported AMBER by A-FIGTYPE-KIND — add it to
               figure_types.FIGURE_TYPES (a repo change) to bind it.

               profile['mode'] decides how hard the constraint binds:
                 'dominant'  → 70% of generated figures use a type from
                               profile['dominant']; the remaining 30% draw from
                               profile['observed']. Never introduce a type that
                               appears in NEITHER list.
                 'observed'  → no type recurs often enough to be called dominant
                               (flat distribution, or too few observations).
                               Generate ACROSS profile['observed']; do not
                               fixate on any one type.
                 'unconstrained' → the profile is empty. Generate as before
                               v5.31, using subtopic semantics alone.

               EC-V18 — LEGACY TOLERANCE, NON-NEGOTIABLE. Roughly 200 exams hold
               section_rules written before v2.37 whose object_types are empty,
               and every one of them must keep working untouched. An absent or
               empty PYQ_IMAGE_ANALYSIS, an absent vision_status, and a
               vision_status of 'unavailable' ALL resolve to 'unconstrained'.
               This branch NEVER raises and NEVER blocks generation.

               vision_status == 'unavailable' deserves its own note: it means
               Step 5 queued figures and observed none, so an empty object_types
               there is a MEASUREMENT GAP, not evidence that the subtopic has no
               typical figure. Treating it as a constraint would generate against
               a fact nobody established. It is therefore 'unconstrained', and
               Step 5's QV-14 is what reports the gap.
               ────────────────────────────────────────────────────────────────

               IF image_role in ('stem_and_options', 'options_only'):
                 → Generate images via matplotlib (S7-NEW-B OPTION A):
                   stem_and_options: problem image(s) + option images
                   options_only: option images only (stem is text)
                 → Place via add_figural_question() (§10-S10-8)
                   (pass empty problem_pngs=[] for options_only)
               ELIF image_role == 'stem_only':
                 → Generate problem image(s) via matplotlib (S7-NEW-B OPTION A)
                 → Place via add_figural_stem_question() (§10-S10-8A)
                 → Options are TEXT — place via add_text_options() inside the helper
               ELSE (unknown role):
                 → Default to add_figural_question() (safest — forces all images)
                 → Log: "image_role unknown for [subtopic_id], defaulting to full"
               → Mark figural_qs[str(qnum)].rendered = true in batch_state
               → Record figural_qs[str(qnum)].object_type = the CANONICAL type this
                 figure was generated AS (ft.lookup(type)['type']), drawn from
                 profile['dominant'] / profile['observed']; in 'unconstrained' mode the
                 registry type of whatever was drawn (v5.88, LAW F2.3: ALWAYS recorded —
                 final_assembly v1.10 refuses to commit a figural question without it; the
                 pre-v5.88 "omit when unconstrained" left six papers with no record).
                 The same value goes to fig_manifest questions[str(qnum)].object_type.
                 audit.py A-FIGPROFILE audits this recorded intent against the same
                 profile via the SAME engine function, bc.check_figural_conformance — one
                 rule, so the generator and its auditor cannot drift apart — and
                 A-FIGTYPE-KIND checks the label against the semantic object and the
                 FigureSpec class beside it (LAW F2.1).
               → Verify via view tool (9-item visual checklist, §10-S10-7)
               Text stem with add_question_stem() alone is BANNED for a GRANTED figural
               slot. (v5.37: this ban applies to a question the Axis-1 budget granted —
               it is what stops a granted figure degrading into a text placeholder. It
               does NOT apply to a DENIED question, whose text rendering via OPTION B is
               the correct and mandated outcome. Before v5.37 no question could be
               denied, so the two cases were indistinguishable and the ban read as an
               unconditional obligation to draw.)
             IF stem_format_variant == 'match_the_following' (any TEXT/PASSAGE format):
               → Render via add_match_table() (§10-S10-3M): the Q.N-first bold instruction
                 paragraph, THEN a REAL Word table (List-I | List-II | … columns; unequal
                 columns blank-padded), THEN the pairing-quad options. Pass the List columns +
                 options as DATA — NEVER embed the lists as stem text.
               → add_standard_question() with the lists in the stem is BANNED for match: it
                 renders the grid as plain text (G-MATCH-TABLE; re-verified by audit.py
                 A-MATCH-TABLE). Keep the 'Match …' instruction in the Q.N paragraph so the
                 audit re-detects the MATCH axis.
             IF format == TEXT/PASSAGE/DI:
               → Generate via add_standard_question() (§10-S10-3)
               → add_figural_question() / add_figural_stem_question() NOT called.
               → v5.42 (GAP-2026-08-06-DI) — IF format == DI, ASK THE BUDGET BEFORE
                 BUILDING A DATA TABLE, exactly as the FIGURAL fork does at S7-NEW-B0:

                     granted, why = bc.axis_grant_figural(
                         axis1_trackers[sec_name], subtopic_id,
                         reducible=SR[sid].get('di_reducible', True), cls='DI')

                 v5.45 — AND THE DI SLOT MUST BE SCHEDULED, NOT MERELY CAPPED. Until now
                 the cap was the whole of DI's control: questions were granted greedily
                 until the budget ran out, so on a DI-heavy exam the COUNT came out right
                 while the DISTRIBUTION did not — DI landed on whichever subtopics the
                 generator visited first, never at each subtopic's measured DI frequency.
                 That is the figural defect one class over, and it was invisible because
                 every exam to hand had a DI budget of 0. Read the per-class schedule the
                 same way the FIGURAL fork does:

                     di_slots = bc.schedule_figural_slots(
                         (axis_schedule.get(sec_name) or {})
                             .get('axis1_quota_by_class', {}).get('DI') or {},
                         (axis_schedule.get(sec_name) or {})
                             .get('axis1_series_by_class', {}).get('DI') or [],
                         bc.figural_band(
                             (axis_schedule.get(sec_name) or {})
                                 .get('axis1_target_per_mock', {}).get('DI', 0),
                             (axis_schedule.get(sec_name) or {})
                                 .get('axis1_observed_by_class', {}).get('DI')),
                         capacity=_cap)
                     this_mock_di = di_slots[(N - 1) % len(di_slots)] if any(di_slots) else None

                 A subtopic absent from this_mock_di renders TEXT this mock. Empty
                 schedule (pre-v1.47 blueprint) ⇒ cap-only, i.e. exactly today's
                 behaviour, so no deployed exam moves until it is re-measured.
                 v5.58 (GAP-2026-08-20-AXIS1-EMPTY-SCHEDULE-SENTINEL): `any(di_slots)`,
                 not `di_slots`. This fork was written by copying the FIGURAL fork and
                 inherited its sentinel bug verbatim — the DI budget is 0 on every exam
                 to hand, so it was latent, exactly as the v5.45 DI scheduling defect
                 was. PASSAGE inherits this fork's shape via axis1_*_by_class, so the
                 correct sentinel has to be fixed HERE, before that class is released.
                 PASSAGE inherits the identical treatment via axis1_*_by_class['PASSAGE']
                 — the point of keying by class is that the next class needs no release.

                 GRANTED  → build the table stimulus and record the question in
                            {EXAM}_di_manifest.json with its subtopic_id and
                            table_shape (rows x cols).
                 DENIED   → render the SAME question without a table stimulus, from this
                            subtopic's own observed PYQ_STEM_PATTERNS. The question keeps
                            its slot, subtopic, difficulty and answer_cardinality.

                 UNLIKE FIGURAL, DI SHARES A RENDERING PATH WITH TEXT — both go through
                 add_standard_question(), so a DI-flagged subtopic was never FORCED to
                 produce a table and DI has not over-generated the way figures did. The
                 budget call is therefore about MEASURABILITY as much as control: without
                 a recorded decision there is nothing for A-AXIS1 to count, and an
                 unaudited budget is how this defect class survives. On a DI-heavy exam
                 (banking/CAT-style aptitude) the control matters on its own terms too.

                 A MATCH question is NOT DI and must never be recorded here, even though
                 G-MATCH-TABLE makes it render a real table. Axis-2 owns MATCH; Axis-1
                 owns DI. Conflating them is precisely the misreading that makes
                 after-the-fact table detection unusable.
             This dispatch is NOT optional. Every Q passes through it.
             Skipping it (using add_question_stem for all Qs regardless of format)
             is the root cause of the production figural defect.

  STEP A2 — INDEPENDENT CHECK OF THE BATCH, BEFORE IT IS DELIVERED (v6.1 — S0-BV, GAP-2026-11-11-BATCH-
           VERIFICATION; EVERY batch, EVERY exam). Every question of this batch is measured by FRESH blind
           graders and solvers NOW — never first at Final Assembly. The block below is idempotent and
           resume-safe (final_assembly.bv_batch_step, the I/O shell over Cluster BV): it collects every returned job, decides every question (bc.bv_apply: pass, tiebreak,
           the ONE rewrite, settle) and writes the jobs still needed. Run it after STEP A, and again after
           each GRADE RETURNED and after each rewrite, until it prints `STEP A2: DONE`:
             JOBS OUT  -> (v6.2: at most 3 reviewer folders) WORKER MODE: prove retention `--when handover`, run
                          `bootstrap.py --checkpoint make` (BV-8), report GRADE_REQUEST with --review-parts = the
                          printed job folders and end the turn (Framework_MockTestOrchestrate O3-9); on
                          `GRADE RETURNED` append its lines, verbatim, to /home/claude/[ExamCode]_M[N]_bv/returned.txt
                          and run the block again. DIRECT MODE: start one fresh sub-agent per job folder, ALL in one
                          message (prompt = its JOB_BRIEF.txt, nothing else), append `<job_dir> <its reply line>` to
                          returned.txt, run the block again; no sub-agent tool -> append `<job_dir> REVIEW FAILED no
                          sub-agent tool` for every folder and run the block again (v6.3 BV-11: never a stop).
             REWRITE q -> rewrite ONLY those questions, ONCE, in their slots (same subtopic, slot band, qtype),
                          from concept_map[q]['bv']['rewrite_brief'] (the graders' own reasons, the measured band,
                          a disputed key, a figure read back wrongly -> redraw it) and the SAME anchors
                          (bc.bv_author_packet); replace the question block
                          in the cumulative docx and its sidecar entry (write_q_to_sidecar); then the block again
                          — the new text is graded as attempt 2 automatically.
           A result is counted only from a job folder whose returned line starts with REVIEW DONE (or, for a job of
           release 2026.11.11, GRADE / SOLVE / VISION DONE)
           (context 'fresh'); a grade made in this session is never written to a result.json. v6.3 (BV-10): a
           reviewer's grade is the band the PYQ rubric computes from ITS counts (bc.br_band), the judged band only
           when the counts are missing or the exam does not use three bands. v6.3 (BV-11): a question with no fresh
           result after bc.BV_MAX_ROUNDS rounds is carried unlabelled to S13-2L — never a stop; at most ONE
           rewrite per question (bc.C_WRITE_ATTEMPTS). The REWRITE brief names the gap in counts
           (rewrite_brief 'gap', 'target', 'measured_counts').
           ```python
           # ── S4-7 STEP A2 (v6.1 BV1) ──
           import final_assembly as fa
           BV_STEP = fa.bv_batch_step(EXAM, N, ruler=globals().get('EXAM_RULER'), manifest=globals().get('manifest'),
                                      bank=globals().get('EXEMPLAR_BANK'), op_profile=globals().get('OP_PROFILE'),
                                      home='/home/claude')
           ```
           STEP E is FORBIDDEN until this block has printed `STEP A2: DONE` for the batch (B-7); a STEP B fix that
           changes a question's text is followed by this block again (the changed text is measured, never assumed). Items listed as
           key to S13-2L (a key still disputed after the rewrite) or unlabelled are carried to Final Assembly's
           S13-2L chains — the batch is still delivered (never a stop); every other item is final.

  STEP B — GATE CHECK (v5.77 — BOTH LAYERS, EVERY BATCH, no either/or):
           1. Run the S4-11 Gate Checklist. ALWAYS — five of its items
              (G-CLUSTER, G-ALTGROUP, G-GROUPMANDATE, G-MINCOUNT,
              G-ALLOC-SUBTOPIC) have NO auditor equivalent, so an
              auditor-only path is strictly weaker than the checklist.
              (G-CLUSTER reads batch_state['placement_report'] and the
              plan; it never re-derives adjacency by eye.)
           2. If AUDIT_AVAILABLE, ALSO run the audit script on the
              cumulative docx and capture STDOUT. The invocation is
              MANDATED, not left to session judgement — run with
              `subprocess.run([...], env=AUDIT_ENV)` (S3-9) or, from a shell,
              `PYTHONPATH=$ENGINE_ROOT` — the per-exam copy is run BY PATH and
              python never puts the cwd on sys.path, so a bare `cd /tmp/fw` does
              NOT make the engines importable (every engine gate would degrade to
              'NOT CHECKED', which S13-4c hard-stops):
              ```
              PYTHONPATH=/tmp/fw python3 /home/claude/[ExamCode]_mock_test_audit.py \
                  /home/claude/<cumulative>.docx \
                  --blueprint [BP_SRC_PATH] \
                  --rules /mnt/project/[ExamCode]_section_rules.md \
                  --manifest /mnt/project/[ExamCode]_subtopic_manifest.json \
                  --registry /home/claude/[ExamCode]_registry.json \
                  --profile /mnt/project/[ExamCode]_difficulty_profile.json \
                  --stimulus-profile /home/claude/[ExamCode]_M[N]_stimulus_profile.json \
                  --key /home/claude/[ExamCode]_M[N]_answer_key.json \
                  --fig-manifest /home/claude/[ExamCode]_fig_manifest.json \
                  --mockN [N] --batch [B] --through-q [last Q in the docx]
              ```
              --fig-manifest (v5.88, auditor v2.33 — edge case E19): the paper is not
              committed until S13-4, so on a batch run the auditor reads the figure
              record from the Step-7 sidecar (object_types, subtopic_ids,
              semantic_objects; FigureSpec sidecars beside it) and arms A-FIGPROFILE
              and A-FIGTYPE-KIND PER BATCH. The registry entry wins once it exists.
              Omit only when the paper has no figural questions.
              [BP_SRC_PATH] (v5.86) is the file S3-2 selected — the
              mock blueprint for a mock, [ExamCode]_[SCOPETAG]_blueprint.json
              for a Subject / Topic / Subtopic paper; never the mock blueprint
              for a scoped paper. --profile may name an absent file (the
              profile is optional): auditor v2.31+ reports A-DPROFILE dormant.
              On the final batch (no --through-q) auditor v2.31+ reports
              A-QINDEX dormant — the index is written at S13-4 — and arms it at
              S13-4c.
              --through-q (v2.23) scopes the structural gates to the
              questions that exist, so a healthy intermediate batch prints
              RESULT: PASS and a FAIL means something (GAP-2026-08-28-
              AUDIT-PARTIAL-PAPER). OMIT --through-q on the final batch /
              Final Assembly re-sweep — a complete paper is audited whole.
           3. If any fixable WARN/FAIL in EITHER layer: fix it, re-run
              BOTH. Iterate to clean.
           present_files is FORBIDDEN until BOTH layers are clean (B-7).

  STEP C — PERSIST STATE:
           If this batch contained PASSAGE questions: write progress.json (S4-8b).
           Update figural manifest if figural Qs present.
           (Do NOT yet update batches_completed — that's STEP F, after delivery.)

  STEP D — REPORT IN CHAT (no question content — MANDATE 0):
           ```
           === BATCH [N] COMPLETE ===
           Section: [section] | Q[start]–Q[end] | [count]Q generated
           Cumulative: Q1–Q[last] now in docx

           Gate checks:
             R8  (no section headers)    : PASS
             R24 (configured font)        : PASS
             R5  (no answer key in docx) : PASS
             G-OPTLABEL (1.  format)     : PASS
             G-MATH-RESIDUE (no flat math): PASS
             K-BAL (option spread)       : PASS [show running %]
             K-PAT (max run=2)           : PASS
             MANDATE 0 (no chat content) : PASS (self-check)
             [audit script STDOUT if available]
           =========================
           ```

  STEP E — DELIVER + STOP LINE:
           Call present_files with cumulative docx.
           (WORKER MODE: this call is the DELIVERY PROXY of Framework_MockTestOrchestrate.md O3-4.)
           Then update batches_completed and current_batch in batch_state.json.
           Then print the STOP line:
           ```
           Batch [N] delivered. [X] of [total] batches done. [Y] remain.
           Next: Batch [N+1] → [next_section] Q[start]–Q[end] ([count]Q)
           Type 'continue' to proceed.
           ```

  STEP F — END THE RESPONSE.
           *** Write nothing more. Generate nothing more. ***
           This is the M1 failure point. The response is OVER here.
           (EXCEPTION: if the batch just delivered was is_final=True, do NOT
            print a continue prompt — instead proceed to Final Assembly per S4-9.)

## S4-8 — Cross-batch persistence

  S4-8a — batch_state.json update (every batch, after delivery):
    ```python
    bs = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json'))
    bs['batches_completed'].append(bs['current_batch'])
    bs['current_batch'] += 1
    # v3.3 — persist the scenario ledger so a resumed session (S4-12) cannot
    # reuse a scenario from an earlier batch. Write the FULL set every time.
    bs['concept_ledger'] = sorted(list(mock_scenario_ledger))
    # v3.9 (G3) — persist the presentation ledger too. Tuples (cg, pk) are stored
    # as "cg||pk" strings (JSON has no tuple/set); rebuilt to tuples on resume.
    bs['presentation_ledger'] = sorted(f"{cg}||{pk}"
                                       for (cg, pk) in mock_presentation_ledger)
    json.dump(bs, open(f'/home/claude/{EXAM}_M{N}_batch_state.json', 'w'))
    ```
    ORDERING: the answer_key sidecar concept_map (S7-NEW-A) is written
    per-question DURING generation, before the gate check and before
    present_files — so it is durable even if the run is interrupted after
    delivery. batch_state.concept_ledger + presentation_ledger are the cross-batch
    mirrors, refreshed here. On resume (S4-12):
        mock_scenario_ledger     = set(bs['concept_ledger'])
        mock_presentation_ledger = {tuple(s.split('||', 1))
                                    for s in bs.get('presentation_ledger', [])}
    so neither a scenario NOR a presentation can repeat across the resume boundary.

  S4-8b — progress.json (only after a batch containing PASSAGE questions):
    ```python
    progress_path = f'/home/claude/{EXAM}_M{N}_progress.json'
    progress = json.load(open(progress_path)) if os.path.exists(progress_path) else {}
    progress['passage_linked_qs'] = sorted(list(passage_linked_qs))
    progress['cloze_linked_qs']   = sorted(list(cloze_linked_qs))
    json.dump(progress, open(progress_path, 'w'))
    ```
    This is a GATED step: do not proceed to present_files until written.

## S4-9 — Final batch → Final Assembly (the ONE auto-advance that IS allowed)

  When the batch just completed has is_final = True:
    - Do NOT print a continue prompt.
    - Do NOT end the response yet.
    - Print: "=== Final batch complete. Running Final Assembly... ==="
    - Proceed directly to §13 Final Assembly in the SAME response.
    - Final Assembly: full gate sweep, registry commit, final docx, handoff.
    - THEN end the response.

  This is the only place auto-advance is permitted, and it is explicitly
  mandated by R23 / MANDATE 1 Final Batch Exception. It is NOT a violation
  of B-4 because Final Assembly is not "the next batch" — it is the closing
  step of the last batch.

## S4-10 — File naming convention

  All deliverable names use pp.paper_slug(paper_id) (v5.28 — the single shared
  implementation in paper_pipeline.py, replacing the old inline C2 v5.21 version):
  "Mock[N]" ZERO-PADDED to 2 digits for a mock (e.g. Mock01, Mock07, Mock12), else the
  scoped paper_id with "::" collapsed to a single "_" first, then remaining ":" to "_"
  (e.g. TOPIC:Physics::Mechanics:01 → TOPIC_Physics_Mechanics_01 — single underscore).
  BEHAVIOUR CHANGE from pre-v5.28: single-digit mock filenames were unpadded (Mock1);
  they are now zero-padded (Mock01) — confirmed with Radheshyam (v5.28 changelog).

  Per-batch cumulative: [ExamCode]_[paper_slug]_Q1to[last_q].docx
    (mock e.g. SSC_CGL_TIER1_Mock07_Q1to30.docx; scoped e.g. NEET_SUBJ_Physics_03_Q1to30.docx)
  Final:                [ExamCode]_[paper_slug]_Create.docx
  Answer key (internal): [ExamCode]_M[N]_answer_key.json
  Figural (internal):    [ExamCode]_fig_manifest.json
  Batch state (internal):[ExamCode]_M[N]_batch_state.json
  Progress (internal):   [ExamCode]_M[N]_progress.json
  Registry (delivered):  [ExamCode]_registry.json

## S4-11 — Gate Checklist (Layer 1 — MANDATORY every batch)

  v5.77: the pre-v5.77 heading scoped this checklist to sessions without an
  auditor ("used when audit.py absent") while STEP B offered the auditor as a
  substitute — and five items here (G-CLUSTER, G-ALTGROUP, G-GROUPMANDATE,
  G-MINCOUNT, G-ALLOC-SUBTOPIC) have NO auditor equivalent. That seam is how
  a paper with a Q.1–Q.3 same-concept_group cluster shipped under an
  "all PASS" report. This checklist runs EVERY batch; the auditor is Layer 2
  and complements it, never replaces it.

  EMISSION LAW (v5.77): the batch gate report PRINTS every item name below,
  programmatically from this list — never from recall. A report with fewer
  than 44 G-* lines is ITSELF a gate failure. (The incident report omitted 5
  of 43 items; the only one of the five that inspects placement rather than
  allocation — G-CLUSTER — was exactly the one that would have caught the
  defect.)

  ```
  MANUAL GATE CHECKLIST — Batch [N] (cumulative docx):

  [ ] G-COUNT:    Cumulative docx has exactly the expected number of Qs
                  (sum of q_count for all batches in batches_completed + this one).
  [ ] G-RANGE:    Every Q number falls within its section's blueprint q_range.
  [ ] G-SECTIONHDR: No "SECTION:", "Part A", divider headers in body, AND (v4.8) no standalone body paragraph equal to a declared section NAME (provenance-based, reg['section_names']). (R8)
  [ ] G-PREQ1:    No title/info/scoring/cover/instruction paragraph before Q.1; the first
                  non-blank body paragraph is the bold "Q.1" stem. CATEGORY-C values
                  (marks/time/negative/options/total) are metadata, never printed. Dormant
                  only if section_rules EXAM_STRUCTURE declares paper_header_block (no current
                  exam does). (R8b) HARD FAIL.
  [ ] G-ANSWERKEY:  No answer key / "Answers:" / "Key:" in docx. (R5)
  [ ] G-FONTCHECK:  All runs use FONT_NAME / FONT_SIZE_PT (no banned fonts). (R24)
  [ ] G-OPTLABEL:   Option labels match OPTION_LABEL_FMT (configured format). (R10)
  [ ] G-BLANK:    Blank separator paragraph after every Q's last option.
  [ ] G-BOLD:     Every Q stem bold; options normal weight. (R13)
  [ ] G-FRAC:     No "a/b" slash fractions in math — OMML only (python-docx).
  [ ] G-MATH-RASTER: No algebraic/built-up expression shipped as an IMAGE. Every
                  inline <w:drawing> name matches q{N}_problem/opt{i}/stim — any
                  other name (e.g. q{N}_e1) is a rasterised expression. Built-up
                  math = OMML only (S10-4 add_math_stem). (R-MATH-OMML) HARD FAIL.
  [ ] G-MATH-RESIDUE: (v5.70) mock_math_residue_check(cumulative docx)['blocking']
                  is EMPTY — no flat x_y or half-Unicode (₂+lowercase) subscript,
                  caret exponent, ÷-fraction, flat radical, letter fraction,
                  combining accent, residual ⟦MATH:⟧ delimiter, or empty/schema-
                  invalid OMML in any stem/option. Compile-fallback regions
                  ('amber' / T3_STATS) route to the F1 AMBER footer, not FAIL.
                  HARD FAIL — re-emit the named stem/option via render_mock_text
                  with ⟦MATH:…⟧ (chemistry examples: S10-4 rule 3a).
  [ ] G-KBAL:     Each option 1/2/3/4 is 20-30% of Qs so far.
  [ ] G-KPAT:     No run of 3+ identical consecutive answers.
  [ ] G-CONT:     No question content visible in this chat response. (MANDATE 0)
  [ ] G-KEY:      answer_key.json has an entry for every Q in this batch.
  [ ] G-FIGSEM:   (v5.59) every rendered figural Q in this batch carries a validated
                  semantic object per role; STRUCTURE roles rendered via
                  corpus_io.structure_draw_fn, REACTION roles via corpus_io.render_scheme
                  (S7-NEW-B2; v5.88).
  [ ] G-FIGTYPE-KIND: (v5.88, LAW F2.1) for every rendered figural Q the recorded
                  object_type's registry row (figure_types.lookup) ADMITS the problem
                  semantic object's kind AND the FigureSpec class
                  (ft.kind_consistent / ft.class_consistent — one rule, shared with the
                  auditor's A-FIGTYPE-KIND through bc.check_figural_conformance(records)).
                  A mismatch is a HARD FAIL: it is a FALSE RECORD. An unregistered type
                  is reported (AMBER), never hidden. object_type is present on EVERY
                  figural Q (LAW F2.3) — S13-4 refuses to commit without it.
  [ ] G-PROG:     progress.json written if this batch had PASSAGE Qs.
  [ ] G-DEDUP:    Each new stem checked against registry_snapshot (L1/L2).
  [ ] G-CONCEPTDUP: No scenario_key repeats anywhere in this mock (DOUBT-3 RULE B).
                  Same scenario twice = HARD FAIL, even with different
                  values/names/wording, even across subtopics. Check concept_ledger.
  [ ] G-ALLOC:    Each subtopic in this batch has exactly its blueprint q_count
                  so far (DOUBT-3 RULE A). Never short, never over.
  [ ] G-GROUPMANDATE: (Issue 2b) every manifest.mandatory_groups group has ≥ its
                  min members generated in this mock. Dormant if no groups declared.
  [ ] G-MINCOUNT: (Issue 2b) every manifest.min_counts id has ≥ its k questions
                  generated in this mock. Dormant if no min_counts declared.
                  (Cadence is NOT checked here — cross-mock, owned by Step 1 RULE M5.)
  [ ] G-STIMULUS-ORPHAN: Every linked-group question in this batch physically
                  carries its shared stimulus (passage/table/chart/cloze) inside
                  its OWN block (R-LINKED / §9 Model A). No "lead-in only" layout;
                  no "Q.X and Q.Y" cross-reference text in any stem. HARD FAIL.
  [ ] G-QNUM-FIRST: Every question block (single AND linked) OPENS with its
                  "Q.<N>" paragraph — no table/passage/preamble before it; the
                  linked specific-ask paragraph is NON-numbered. (R14) HARD FAIL.
  [ ] G-FORMATDUP: No two CLASS-2/3 questions sharing a CONCEPT_GROUP have the
                  same presentation_key (stem_format_variant | distractor_strategy).
                  Different word/fact does NOT excuse an identical look. If a
                  CONCEPT_GROUP has ≥3 Qs, ≥2 stem formats appear. (RULE C) HARD FAIL.
  [ ] G-BLOCK (v5.85, set-placed papers only — else 'dormant — legacy paper'):
                  every set in batch_state['stimulus_groups'] whose Q-numbers are in
                  this batch sits at exactly its planned consecutive Q-numbers, in
                  member order; all its members embed the ONE registered stimulus
                  (stim_register); cloze members ask blanks in increasing order.
  [ ] G-CLUSTER:  Read batch_state['subtopic_by_qnum'] + ['placement_report']
                  (S3-12b): adjacent same-CONCEPT_GROUP pairs in the questions
                  generated so far == the report's own list and <= its
                  min_possible_adjacent_cg floor; no PRESENTATION_FAMILY run
                  > 2 (<= 3 only where the report shows composition forces
                  it); each subtopic's N Qs spread per the plan. Adjacency
                  strictly inside a linked-stimulus block is EXEMPT. (R19
                  v3.8; v5.77 — plan-quoting, promoted to auditor A-CLUSTER)
  [ ] G-FIGURAL-COMPOSITE: Every figural Q is correctly structured per its
                  image_role variant (v5.13). stem_and_options: problem image +
                  one separate image per option, single-column, 1:1 label binding.
                  stem_only: ≥1 problem image + text options (option images NOT
                  required). options_only: ≥n option images, no problem image
                  required. No composite panel, no two images on a line, no
                  "1. Figure 1" dummy text, no question chrome baked into any raster;
                  all option images 300 DPI on a uniform square canvas.
                  (R-FIGURAL / §10-S10-7/S10-8/S10-8A) HARD FAIL.

  [ ] G-UNDERLINE: Every underline-class question (asks about "the underlined
                  word/part", or stem_format_variant 'sentence_embedded_underlined')
                  renders its target span as a REAL underlined run inside the
                  sentence — never a "(underlined: X)" text annotation, never an
                  underscore/markdown fake. (R-UNDERLINE / §10-S10-2) HARD FAIL.

  [ ] G-OPTREF: No stem references a terminal/escape option the option set lacks.
                  If a stem says "if no error → last option" / "select 'No
                  improvement'" / "None of these" / "Both…and…" / "Neither…nor…",
                  that option is PRESENT and at the named position; a "pick the
                  segment" layout carries no "no error" escape unless a real "No
                  error" option exists. (R-OPTREF / §10-S10-2) HARD FAIL.

  [ ] G-UNIQUE: Every question has EXACTLY ONE defensible answer — CHECK 3
                  verify_answer ran and answer_verified==true
                  is recorded in the sidecar. No kinship maternal/paternal split, no
                  contested-convention double-answer, no multi-rule series collision.
                  (R-ANSWER / §7 CHECK 3) HARD FAIL.

  [ ] G-ALTGROUP: No alternation group (manifest.alternation_groups) has 2+
                  members present in this mock. Dormant if no groups declared. (S3-17)
  [ ] G-ALLOC-SUBTOPIC: Each subtopic_id has EXACTLY its blueprint q_count
                  (DOUBT-3 RULE A). Distinct from G-COUNT which checks section totals.
  [ ] G-COUNT-X-UNIQUE: RULE A (exact per-subtopic count) AND RULE B (all
                  scenario_keys pairwise distinct) both hold mock-wide. (DOUBT-3)
  [ ] G-FIGTEXT: No figural questions delivered as text descriptions. Three-tier
                  check (v5.13): (1) every format=FIGURAL block has ≥ minimum images
                  for its image_role, (2) no bracketed placeholders anywhere, (3) no
                  figure-reference prose in zero-image blocks. HARD FAIL. (S7-NEW-B)
  [ ] G-MSQ-SET: (multi only, dormant if multi_present=false) MSQ key is a
                  non-empty proper subset of 1..total_options; no banned AOTA option
                  under multi (R-MSQ-ESCAPE). HARD FAIL.
  [ ] G-MSQ-CARD: (multi + fixed-k only, dormant otherwise) |S| == msq_k.
  [ ] G-MSQ-INSTR: (multi only, dormant if multi_present=false) the select-
                  instruction is present INSIDE the Q.N stem line (R14). HARD FAIL.
  [ ] G-NAT-NOOPT: (numerical only, dormant if nat_present=false) NAT question
                  renders ZERO option paragraphs. HARD FAIL.
  [ ] G-NAT-ANSWER: (numerical only) NAT value well-formed for nat_answer_type;
                  ca_range lo<=hi. HARD FAIL.
  [ ] G-NAT-GRADE: (numerical only) portal grading value/type well-formed
                  (0-9.- only charset) and deterministically re-derivable. HARD FAIL.
  [ ] G-NAT-INSTR: (numerical only) numerical-entry instruction present in
                  Q.N stem line (R14). HARD FAIL.
  [ ] G-MATCH-TABLE: Every match question (stem_format_variant == 'match_the_following')
                  renders its List columns as a REAL Word table, not plain text. Executable
                  enforcement is the audit.py A-MATCH-TABLE (STEP B); this item is the
                  no-audit fallback. HARD FAIL — re-emit via add_match_table().
  [ ] G-STEM-SUBPART: (v5.79) Every multi-part stem in this batch (>=2
                  enumerated sub-parts) renders ONE BOLD sub-part per paragraph
                  via add_stem_multipart; NO sub-part line opens with a Q-number
                  shape, a bare digit-dot/digit-paren label, or THIS exam's own
                  option-label scheme in ANY spacing (S10-2b LABEL LAW); the
                  MSQ/NAT instruction remains INSIDE the Q.N line; MATCH lists
                  remain REAL tables, never sub-part lines. (S10-2b) HARD FAIL.

  [ ] G-OPTDISTINCT: (v5.90) Every option set: no two options are ONE entity under the
                  content kind's identity_fn (bc.option_distinct_check over the figure
                  records' canonical for pictures, bc.text_identity over delivered text);
                  a figural paper with no option figure record FAILS, never dormant.
                  Ladder R2o. Twin: A-OPTDISTINCT. HARD FAIL.
  [ ] G-MEDIAREUSE: (v5.90, OD-13) No media part placed under two questions (linked sets
                  exempt) — final_assembly.commit_registry REFUSES the commit; the later
                  item enters the ladder at R2. Twin: A-MEDIAREUSE. HARD FAIL.
  [ ] G-ENTITYLEAK: (v5.90, OD-2) bc.EntityLedger over the paper: a key entity in another
                  item's given / intermediate / key / distractor / figure-label role, two
                  items sharing a given, a scaffold over its measured cap -> FAIL on the
                  LATER item (R2); distractor-as-given -> reviewer; text entities WARN
                  where the exam's PYQs are calibrated (R3.8). Twin: A-ENTITYLEAK. HARD FAIL.
  [ ] G-STEMLEAK: (v5.90, OD-3) bc.stem_leak_check: a tested-concept lexicon term in the
                  stem (unless the cell's named_concept_rate >= bc.NAMED_RATE_ALLOW), a
                  drawn entity also named in words (unless shown_entity_named_rate >= 10 %),
                  a non-agent scheme annotation, an unasked trailing placeholder -> FAIL,
                  ladder R2s (stem only). DORMANT (printed) without a QUALITY block.
                  Twin: A-STEMLEAK. HARD FAIL.
  [ ] G-STEMFORM: (v5.90) bc.stem_form_check: pattern_key observed in the cascade cell;
                  question-line word count within [min, max(max, 1.2 x p90)]. R2s.
                  Twin: A-STEMFORM. HARD FAIL.
  [ ] G-DISTRACTOR: (v5.90) bc.distractor_record_check (mechanisms MANDATORY, in
                  vocabulary), bc.class_predicate_check (class word SMARTS),
                  bc.data_consistency_check (stated formula / DBE), bc.inventory_check
                  (element set ⊆ givens ∪ reagents; MCS >= 0.5 unless alternative pathway),
                  bc.mechanism_formula_check (isomer distractors carry the key's formula),
                  bc.near_isomer_check (>= 2 near-isomers where the cell uses them). R2o.
                  Twin: A-DISTRACTOR. HARD FAIL.
  [ ] G-CONSIST: (v5.90) bc.consist_check: every stem agent in the figure's agents;
                  a stereoisomer-count object drawn without stereo marks. R2s.
                  Twin: A-CONSIST. HARD FAIL.
  [ ] G-STEREODECL: (v5.90, owner Q-A) bc.stereo_declaration_check per drawn structure:
                  the SMILES encodes the declared descriptor multiset. R2o; undeclared is a
                  recorded WARN. Twin: A-STEREODECL. HARD FAIL.
  [ ] G-ITEMRULE: (v5.90, OD-7) bc.item_longest_key (key longest AND > 1.5x the mean of
                  the others) and bc.item_middle_value_key on DELIVERED text options with
                  the key as a 0-BASED index (sidecar correct_pos - 1; a letter label is
                  accepted too); suspended ONLY by a MEASURED PYQ rate >= 10 %
                  (bc.item_rule_suspended), never by absence. R2o. Twin: A-ITEMRULE. HARD FAIL.
  [ ] G-SHAPEMIX: (v5.90, OD-6 c) bc.shape_mix_check: every planned shape within
                  round(sN) +/- max(1, 15 %), at or above its FLOOR, at or below its CAP;
                  recorded infeasibility is not a defect. R3. Twin: A-SHAPEMIX. HARD FAIL.
  [ ] G-TEMPLATE: (v5.91) bc.template_check PER (subtopic, fingerprint) against THAT
                  subtopic's MEASURED cap (section_rules fingerprint_max_per_paper scaled
                  by bc.template_cap); an UNMEASURED fingerprint is NOT checked (never a
                  default cap); readiness G-TEMPLATE not PASS -> fingerprint caps DORMANT;
                  infeasible -> reported, never a defect; concept ids only against MEASURED
                  concept caps. Read the auditor's A-TEMPLATE line — never count by hand.
                  R3. Twin: A-TEMPLATE. FAIL only on a measured cap; never a stop.

  [ ] G-STYLE: (v5.82, ADVISORY) Paper-so-far style distance D against the
                  profile cell (section x answer_type, falling back to the paper
                  cell): mean of mechanic-mix JS, form-mix JS, polarity delta,
                  and — only when the profile's thresholds are
                  computed_from_dispersion and this cell has >= 12 questions in
                  the paper-so-far — lexicon-coverage deficit and stimulus
                  deficit. Verdict PASS / WARN / HIGH. RECORD ONLY: HIGH never
                  fails the batch and never withholds a paper (P-4). DORMANT
                  (recorded, with reason) when the profile is absent or stale.
  [ ] G-PYQ-DIST: (v5.82, ADVISORY) Every question's textual Jaccard against the
                  PYQ index via the inverted shingle lookup, plus semantic-tuple
                  equality, value reuse and image dHash. REJECT-and-regenerate is
                  BUDGETED (MAX_ATTEMPTS_PER_Q = 2, MAX_RETRIES_PER_PAPER =
                  ceil(0.20 x total)); on exhaustion the best attempt is ACCEPTED
                  and pyq_dist.accepted_on = "budget" is recorded. Records land
                  in the sidecar, dossier and registry — NEVER in the delivered
                  footer (Q15). Cannot be disabled (EC-30). DORMANT only when the
                  index is absent.
  [ ] G-ITEM (I-1..I-8): (v5.82, ADVISORY) The universal item-writing rules,
                  each SUSPENDED for this exam when the exam's own PYQ violate it
                  at >= 10% (item_rules[I-n].suspended, ruling Q6). Verdicts are
                  recorded per question in style_obs.item_flags; a WARN never
                  fails the batch. NAT-only cells record NA, not PASS (EC-7).

  Items 1-57 must PASS. If any FAIL: fix in this batch, re-check, then deliver.
  All 60 items are RUN; items 58-60 (G-STYLE, G-PYQ-DIST, G-ITEM) RECORD their
  verdict and never fail the batch — they are advisory by construction (P-4).
  (v5.88: G-FIGTYPE-KIND joins the must-PASS set; the advisory trio keeps its place
  at the end. v5.90 — GAP-2026-11-03 G11 / OD-1: the eleven QUALITY items above are
  must-PASS ITEM gates — each has an objective per-item verdict and a ladder rung — while
  the distribution checks G-STYLE / G-PYQ-DIST stay advisory; "must PASS" means the item
  is REPAIRED through the ladder, never that the run stops; a gate whose INPUT is missing
  reports DORMANT(reason), which is neither PASS nor FAIL and is listed by S3-2e.)
  ```

## S4-12 — Session recovery / resume (v3.0)

  TRIGGER: MockCreate M[N] resume   (also `TestCreate ... --resume` / `MockCreate M[N] --resume`)
  OR: batch_state.json indicates an incomplete mock (batches_completed not full).

  "continue" (S4-6) ALSO enters this recovery when every batch is authored but the paper is
  not yet committed — an interrupted Final Assembly response resumes here; the user never
  types anything else and never attaches a review file.
  v5.91 — FINAL ASSEMBLY INTERRUPTED BEFORE THE REVIEW: batches_completed covers every batch
  of the plan, the registry has no committed question_index entry for this paper, and
  batch_state.state is absent or not one of the REVIEW states below -> do NOT print a continue
  prompt and do NOT generate a batch: re-enter §13 at S13-2 / S13-2F (the sweep counter lives
  in its state file, so the count continues) and run on to S13-2G, S13-3 .. S13-8 in this
  same response.

  v6.1 (S0-BV) — BATCH IN VERIFICATION: batch_state['bv'] names the current batch with status 'jobs_out' or
  'rewrite' -> the batch's questions are written; run S4-7 STEP A2 again (it collects every returned job and
  re-issues any missing one), then continue S4-7 from where it printed (JOBS OUT / REWRITE / DONE). A
  `GRADE RETURNED` message's lines are appended to returned.txt first (Framework_MockTestOrchestrate O3-9).
  v5.91 (GAP-2026-11-04 A6) — REVIEW STATES, all continued INTERNALLY. After step 1 below,
  read batch_state.get('state'):
    'REVIEW_RUNNING' -> the in-session review was interrupted. If
        batch_state['review_dir']/queue.json exists and its paper_md5 equals the md5 of the
        current final docx: run S13-2G PHASE 2 only for the parts whose verdicts.json is
        missing or does not parse (a reviewer interrupted mid-write), then PHASE 3.
        Otherwise run S13-2G from PHASE 1.
    'AWAITING_REVIEW' (LEGACY — a paper parked by release 2026.11.03) -> every question is
        authored and swept under 2026.11.03. FIRST re-run S13-2F (preview + block): it
        clears the UNRESOLVED stamps only the 2026.11.03 default template cap wrote and
        issues a fresh certificate. Then run the block below. If it finds an attached
        verdict file bound to the CURRENT paper (found by CONTENT — exam_code + paper_md5 —
        never by file name: uploads carry a random prefix and a sanitised slug,
        GAP-2026-11-04 A7/E10), run S13-2G PHASE 1, then write LEGACY_VERDICTS as
        verdicts.json into EVERY part folder (one record covers the whole paper) and run
        PHASE 3 — no reviewer is started. With no matching file: run S13-2G from PHASE 1
        (the internal review). Never ask for a file.
    v5.96: 'REVIEWED' with an open chain in batch_state['slot_chain'] or a non-empty
        batch_state['slot_chain_work'] -> S13-2R for every entry not yet 'recorded', then S13-2F,
        S13-2G (delta round when delta_qs / delta_panel is non-empty), S13-2L; 'REVIEWED' with no chain
        state -> S13-2L before S13-3; batch_state['review_dl_repair'] lists the REVIEW_REPAIR items
        that are DIFFICULTY repairs (S13-2G REVIEW_REPAIR, DR1 then DR2).
    'REVIEW_REPAIR' -> the flagged items are being repaired; continue from §Q8b-LADDER on
        batch_state['review_defects'] (persisted by phase 3), SKIPPING every item already in
        batch_state['review_repaired'] (each repair appends its q there as soon as it is
        written — see S13-2G), then S13-2F, then S13-2G phase 1 with the WHOLE paper (round 2;
        the binding is per paper).
    'REVIEWED' -> S13-2L (v5.96) / S13-3 / S13-4 / S13-REGCHECK / S13-QINDEX / S13-4b / S13-4c / S13-6 / S13-7 /
        S13-8 / S13-9, in this same response.
    'DELIVERED' -> the paper is finished (S13-9): say so; generate and deliver nothing.
  Any other value (or none) -> if every batch of the plan is authored and the S3-1-resolved
  registry has no committed question_index entry for this paper: §13 from S13-2 / S13-2F (the
  FINAL ASSEMBLY INTERRUPTED rule above); otherwise the batch recovery below (its steps 5-6 — the continue prompt and STOP —
  apply ONLY to the batch recovery, never to a paper whose batches are all authored).
  ```python
  # ── S4-12 legacy verdict lookup (v5.91 — GAP-2026-11-04 A7; used ONLY for 'AWAITING_REVIEW') ──
  import glob, json, os, hashlib, paper_pipeline as pp
  _docx12 = f'/mnt/user-data/outputs/{EXAM}_{pp.paper_slug(paper_id)}_Create.docx'
  _bs12 = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
  _md5_12 = hashlib.md5(open(_docx12, 'rb').read()).hexdigest() if os.path.exists(_docx12) else _bs12.get('paper_md5')
  LEGACY_VERDICTS = None
  for _vp in sorted(glob.glob('/mnt/user-data/uploads/*review_verdicts*.json')):
      try:
          _v = json.load(open(_vp, encoding='utf-8'))
      except (OSError, ValueError):
          continue
      if isinstance(_v, dict) and _v.get('exam_code') == EXAM and _v.get('paper_md5') == _md5_12:
          LEGACY_VERDICTS = _v
          break
      print(f"S4-12: ignoring {os.path.basename(_vp)} — not bound to this paper (exam "
            f"{_v.get('exam_code') if isinstance(_v, dict) else '?'}, md5 {_v.get('paper_md5') if isinstance(_v, dict) else '?'}).")
  print("S4-12: legacy AWAITING_REVIEW paper — " + ("binding the attached verdict file (found by content)."
        if LEGACY_VERDICTS else "running the in-session review now (S13-2G phase 1)."))
  ```
  batch_state['shape_plan'] (S3-12d) and ['quality_readiness'] (S3-2e) are READ,
  never re-derived, on every resume (FROZEN-PLAN LAW).
  v5.96 MIGRATION (Framework_MockTestOrchestrate O2-8; GAP-2026-11-08): on EVERY resume, BEFORE the state
  dispatch above, run the block below. It is idempotent (recorded in batch_state['migrations']) and changes
  nothing on a paper written by this release. On a paper parked by 2026.11.08 / 2026.11.08.1 it restores
  every DR3 label to its slot, opens the difficulty / dispute / quality chains, clears every UNRESOLVED
  stamp and uncertified_items, and retires the paper-level rework counter (bc.migrate_paper_state).
  ```python
  # ── S4-12 migration (v5.96) ──
  import json, os, blueprint_core as bc
  _bsm_p = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _kdm_p = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  if os.path.exists(_bsm_p) and os.path.exists(_kdm_p):
      _bsm, _kdm, _repm = bc.migrate_paper_state(json.load(open(_bsm_p, encoding='utf-8')),
                                                 json.load(open(_kdm_p, encoding='utf-8')), 'pre-2026.11.09')
      if not _repm['skipped']:
          json.dump(_kdm, open(_kdm_p, 'w', encoding='utf-8'), indent=2)
          json.dump(_bsm, open(_bsm_p, 'w', encoding='utf-8'), indent=2)
          if _repm['dr3_restored'] or _repm['rework_pending'] or _repm['unresolved_cleared']:
              for _f in (f'/home/claude/{EXAM}_M{N}_item_sweep_certificate.json', f'/home/claude/{EXAM}_M{N}_s13_2f_state.json'):
                  if os.path.exists(_f):
                      os.remove(_f)                  # re-issued by S13-2F; the sweep count restarts
              print(f"S4-12 MIGRATION {_repm['tag']}: DR3 restored to slot {_repm['dr3_restored']}; unreviewed reworks "
                    f"{_repm['rework_pending']}; UNRESOLVED cleared {_repm['unresolved_cleared']} — continuing at "
                    f"S13-2L (chains), S13-2F, S13-2G (delta), automatically.")
  ```

  RECOVERY PROCEDURE:
    0. S3-1 has already run this turn (it runs at EVERY session start): the registry
       was resolved from the chat attachment or Project Files (REGISTRY-SOURCE-LAW)
       and checked against batch_state.registry_pin. In a BRAND-NEW chat the
       attachment from the earlier chat is gone — re-attach the SAME registry to the
       resume trigger, or have it in Project Files; a missing registry in both lanes
       is the S3-1 HARD STOP [HS:INPUT], a different one is the R4 HARD STOP [HS:INPUT].
    1. Load batch_state.json. Read current_batch and batches_completed.
    2. If batch_state.json is missing:
         - Load the most recent cumulative docx for Mock N.
         - Count Q paragraphs to find last completed Q number.
         - Map last Q to its batch using the freshly-rebuilt batch_plan.
         - Set current_batch = that batch + 1; batches_completed accordingly.
         - Rewrite batch_state.json (registry_pin = REG_PIN from this turn's S3-1 —
           there is no earlier pin to compare against; the supplied registry is
           accepted, exactly as the Files lane always behaved).
    3. Load the existing cumulative docx as the base (do NOT regenerate prior Qs).
    4. Load answer_key.json (has all prior answers).
    4a2. FROZEN-PLAN LAW (v5.77 — GAP-2026-08-28-PLACEMENT-UNSPECIFIED §7.2):
        subtopic_by_qnum and placement_report are read from batch_state and
        NEVER re-derived on a resume — re-placing would invalidate every
        question already authored. A pre-v5.77 batch_state (no plan fields)
        is handled by S3-12b's middle branch: the AUTHORED questions are
        frozen from the answer_key concept_map (q → subtopic_id), the
        NOT-YET-AUTHORED remainder of each section is placed fresh into its
        remaining contiguous range, the whole map is audited with
        bc.audit_placement, and adjacency findings are reported as a §R13
        limitation. Adjacency NEVER hard-stops a resume; the only resume
        HARD STOP [HS:INFRA]s are artefact-consistency faults (answer_key, batch_state
        and blueprint disagreeing about what exists).
    4b. REHYDRATE THE LEDGERS (v3.9 G3 — mandatory, else resume can clone):
        mock_scenario_ledger     = set(bs.get('concept_ledger', []))
        mock_presentation_ledger = {tuple(s.split('||', 1))
                                    for s in bs.get('presentation_ledger', [])}
        If batch_state.json was missing (step 2), rebuild BOTH ledgers from the
        answer_key concept_map instead (scenario_key values, and (concept_group,
        presentation_key) pairs for every CLASS-2/3 question). Without this, RULE B
        and RULE C are blind to everything generated before the interruption.
    4c. FIGURE RECORD ACROSS THE v5.88 FIX (E15 — LAW F2.3). A question authored by a
        pre-v5.88 session recorded no object_type, and this session cannot honestly
        invent one after the fact. Mark it, once, in the sidecar; final_assembly v1.10
        commits it AS unlabelled (object_type='legacy_unlabelled', carried into the
        entry's record_integrity), A-FIGTYPE-KIND reports it WARN (AMBER), §FOOTER-FT
        discloses it. Questions authored from here on carry object_type (S7-NEW-B).
        ```python
        import json, os
        _fmp = f'/home/claude/{EXAM}_fig_manifest.json'
        if os.path.exists(_fmp):
            _fm = json.load(open(_fmp, encoding='utf-8'))
            _unl = []
            for _q, _v in (_fm.get('questions') or {}).items():
                if isinstance(_v, dict) and not _v.get('object_type') and not _v.get('record_integrity'):
                    _v['record_integrity'] = 'legacy_unlabelled'
                    _unl.append(str(_q))
            if _unl:
                json.dump(_fm, open(_fmp, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
                print(f"S4-12 4c: {len(_unl)} figural question(s) authored before v5.88 carry no "
                      f"object_type — marked legacy_unlabelled (disclosed, not refused): Q{', Q'.join(_unl)}")
        ```
    5. Print resume summary:
       "Resuming Mock [N]: [done] batches complete (Q1–Q[last]).
        Next: Batch [current_batch] → [section] Q[start]–Q[end].
        Type 'continue' to proceed."
    6. STOP. Wait for continue.

## S4-13 — Batch processing failure modes and their fixes (reference table)

  | Failure mode (what M1 did)                  | v3.0 rule that prevents it     |
  |---------------------------------------------|--------------------------------|
  | Generated all 100Q in one response          | B-4 + S4-7 STEP F + MANDATE 1  |
  | Auto-advanced to next batch without continue| B-5 + S4-6                     |
  | Computed Q-range from memory                | B-2 + S4-5 CHECK 2             |
  | Generated >10Q in a batch                   | B-3 + S4-1                     |
  | Spanned two sections in one batch           | S4-1 + S4-2 algorithm          |
  | Never stopped to let user review            | S4-7 STEP E + STEP F           |
  | Delivered without gate check                | B-7 + S4-7 STEP B              |
  | Lost track of which batch was next          | batch_state.json + S4-8a       |
  | Couldn't resume an interrupted mock         | S4-12                          |
  | Printed question content in chat            | MANDATE 0 + G-CONT             |


# ════════════════════════════════════════════════════════════════════════
# §5 — ANSWER POSITION BUDGET (see S3-13 for pre-build algorithm)
# ════════════════════════════════════════════════════════════════════════

## S5-1 — Pre-allocation (built at S3-13, before Q1)

  Budget built in S3-13. All Qs read correct-answer position from budget.
  Generation fills the pre-assigned slot with factually correct content.
  This is the ONLY source of answer positions. Never assign ad-hoc.

## S5-2 — K-BAL targets

  Global: 20-30% per option of total non-fixed Qs.
  Per-section: 15-35% per option.
  Fixed-set Qs (type=fixed_set in section_rules) excluded from pool.

## S5-3 — Fixed-set exclusion

  wrong_option_structure.type == "fixed_set" → excluded from K-BAL pool.
  These Qs' answer is determined by WHICH fixed option text is factually true.

## S5-4 — Difficulty interleaving

  Max 3 consecutive Hard. Max 4 consecutive Easy+Medium. Distribute evenly.

## S5-5 — Running monitor

  After each Q: check projected final % for each option.
  >32% for any option → WARN. >35% → switch to greedy assignment.

## S5-6 — K-BAL fix protocol (v2.0 — only for fixable WARN)

  Swap option TEXT positions in docx (not answer identity).
  Update answer_key sidecar: key[Q_num] = new position.
  Re-check K-PAT after every swap.
  Fixed-set Q positions excluded from any swap.

# ════════════════════════════════════════════════════════════════════════
# §6 — DEDUP ARCHITECTURE
# ════════════════════════════════════════════════════════════════════════

## S6-0 — dedup_partition priority rule

  HONOUR dedup_partition (blueprint) FIRST, then verify against registry.
  dedup_partition = mock-specific seeds/topic assignments.

## S6-1 through S6-12 — (identical to v1.0 — see full v1.0 text)

  L1: MD5 hash + near-verbatim (Jaccard ≥0.75 → HARD FAIL; 0.60-0.74 → WARN)
  L2: Semantic tuple [subtopic, approach, sorted_values] — CROSS-MOCK only
      (B v5.22: unchanged; a SEPARATE semantic_usage log tags each use with paper_index
       for the narrow-factual controlled-reuse spacing gap — L2 matching is untouched)
      (D v5.23: the L2 lookup is PARTITIONED by subtopic via SUBTOPIC_INDEX['semantic_tuples']
       (S3-5) — a candidate's tuple carries its subtopic, so only that subtopic's shard can
       match; the result is identical, just O(shard). L1 below stays GLOBAL — deliberately
       NOT sharded, so a verbatim duplicate is caught across subtopics.)
  L3: Per-subtopic exact count (blueprint q_count) + intra-mock scenario_key
      uniqueness + intra-mock presentation_key uniqueness (CLASS 2/3, RULE C,
      v3.8). SEE S6-3b/S6-3c for the authoritative rules. NOTE: CONCEPT_GROUP is
      NOT the uniqueness unit — it may repeat N times per mock; scenario_key is
      the CONTENT unit and presentation_key is the LOOK unit, and both must be
      unique within a CONCEPT_GROUP mock-wide.
  L4: Content tracking (ga_facts, passage topics, etc.)
  L5/L6: Image dHash (within-Q >20; cross-mock >25) + MD5
  L7-L18: All remaining dedup layers (grammar rules, vocab, idioms, etc.)

  KEY v2.0 FIX (GAP-19): ALL new dedup data accumulates in pending_registry
  (initialised at S3-4). NOTHING written to registry.json during generation.
  pending_registry committed ONLY at Final Assembly after all gate checks pass.

## S6-3b — ALLOCATION COUNT + INTRA-MOCK SCENARIO UNIQUENESS (DOUBT-3, v3.3)
#  ─────────────────────────────────────────────────────────────────────
#  TWO HARD RULES THAT BOTH ALWAYS HOLD — they never conflict:
#
#  RULE A (EXACT COUNT — from blueprint.json, authoritative):
#    Each subtopic produces EXACTLY the number of questions its blueprint
#    allocation specifies (subtopic_allocations[].q_count = N).
#    N is BOTH the floor AND the ceiling. Never generate N-1 or N+1.
#    This rule is NEVER weakened by the uniqueness rule below.
#
#  RULE B (SCENARIO UNIQUENESS — strict, zero tolerance):
#    No two questions ANYWHERE in the same mock may share a scenario_key.
#    A concept/scenario may appear EXACTLY ONCE per mock. Duplicating it by
#    changing values, names, numbers, or wording is STRICTLY BANNED.
#    There is no "near-duplicate" tolerance band: it is a HARD ZERO.
#
#  HOW THEY COMBINE (the resolution of DOUBT-3):
#    When a subtopic is allocated N>1 questions, the answer is NEVER to drop
#    the count. It is to generate N questions that are EACH a genuinely
#    different scenario (distinct scenario_key) within that subtopic — so a
#    student never perceives a repeat. A subtopic is "done" ONLY when N
#    distinct-scenario questions exist — never because "a scenario was used."
#  ─────────────────────────────────────────────────────────────────────

  VOCABULARY (single clear set of terms):
    CONCEPT_GROUP : the coarse subtopic-level tag from section_rules.md
                    (e.g. "compound_interest", "blood_relations", "syllogism",
                     "idiom_meaning", "mensuration_3d"). May legitimately repeat
                     up to N times in a mock (once per allocated question).
    scenario_key  : the FINE uniqueness unit. A canonical string naming the
                    specific cognitive OPERATION + structural SHAPE of one
                    question, independent of all surface values/names/wording.
                    THIS is the unit that must be unique mock-wide.
    concept_id    : (CONCEPT_GROUP, scenario_key) — used only for reporting.

  THE UNIQUENESS UNIT IS scenario_key (not CONCEPT_GROUP):
    - CONCEPT_GROUP MAY repeat exactly N times (= the allocation count).
    - But each of those N questions MUST carry a DISTINCT scenario_key.
    - Two questions with the same scenario_key anywhere in the mock = BANNED,
      even across two different subtopics (mock-global uniqueness).

  scenario_key DERIVATION (open-ended, value-independent):
    scenario_key = canonical(cognitive_operation + "|" + structural_shape)
      cognitive_operation = what the student DOES
                            (e.g. "find_time_given_CI_amount_and_rate")
      structural_shape    = the scenario structure
                            (e.g. "two_pipes_one_drain_net_fill")
    RULES:
      - Built ONLY from operation + structure. NEVER from numbers, names, or words.
      - A value-swap or reword yields the SAME scenario_key → correctly BANNED.
      - A genuinely different operation OR structure yields a NEW scenario_key
        → correctly ALLOWED.

    Examples of SAME scenario_key (BANNED as a 2nd Q in the mock):
      - "CI on ₹5000 at 10% for 2 yrs" and "CI on ₹8000 at 5% for 3 yrs"
        → both: find_CI_amount | principal_over_n_years_annual → SAME → banned.
      - "A is brother of B, B is daughter of C" vs same chain with new names
        → both: resolve_relation | linear_chain_3_people → SAME → banned.

    Examples of DIFFERENT scenario_key (each allowed once):
      - find_CI_amount | annual_compounding   vs
        find_CI_amount | half_yearly_compounding   → different shape → allowed.
      - find_CI_amount | given_P_R_T          vs
        find_principal  | given_CI_R_T (reverse)    → different operation → allowed.
      - mensuration_3d volume_of_cylinder     vs
        mensuration_3d surface_area_of_cone         → different op+shape → allowed.

  ───────────────────────────────────────────────────────────────────────
  SUBTOPIC CLASS — WHAT "SAME SCENARIO" MEANS DEPENDS ON THE SUBTOPIC TYPE
  (critical: without this, the rule mis-fires on vocabulary/fact subtopics)
  ───────────────────────────────────────────────────────────────────────
    The student-facing intent is: "a student must never FEEL a concept was
    repeated." What feels repeated differs by subtopic class. Classify each
    subtopic (from section_rules.md CONCEPT_GROUP / format) into ONE class and
    derive scenario_key accordingly:

    CLASS 1 — COMPUTATION / REASONING (e.g. CI, SI, Time-Work, Speed, Syllogism,
              Blood Relations, Seating, Mensuration, Series, Coding-Decoding):
        The UNIT is the OPERATION + STRUCTURE. Two questions doing the same
        calculation/deduction with different numbers/names FEEL repeated → BANNED.
        scenario_key = cognitive_operation | structural_shape (as above).
        To make N>1 distinct: change the operation (forward vs reverse), the
        structure (1 train vs 2 trains; linear vs circular seating), or the
        concept facet (volume vs surface area). NOT just the numbers.

    CLASS 2 — VOCABULARY / ITEM-RECALL (e.g. Synonyms, Antonyms, Idioms,
              One-Word-Substitution, Spelling, Homonyms):
        The cognitive operation is format-fixed ("pick the synonym"), so the
        TARGET ITEM is the CONTENT-uniqueness unit:
        scenario_key = subtopic | normalized_target_item
          (e.g. "synonyms|abstruse", "idioms|spill_the_beans").
        Two questions on the SAME item (even reworded) = SAME scenario_key →
        banned. Different items = different scenario_key. The item must ALSO be
        unique cross-mock via L8 vocab tracking.
        *** v3.8 CORRECTION (DOUBT-4) — a different word is NOT enough. ***
        A distinct scenario_key (different word) is NECESSARY but NOT SUFFICIENT.
        Because the operation is fixed, two CLASS-2 questions in the same
        CONCEPT_GROUP can be PRESENTATION-CLONES — identical stem template,
        identical distractor strategy, identical difficulty — and still pass the
        scenario_key check, which is exactly the M1 Q.77/Q.79 (Antonym) and
        Q.78/Q.80 (Synonym) defect. CLASS-2 subtopics with q_count > 1 MUST
        therefore ALSO satisfy RULE C (presentation uniqueness, §6-3c): every
        pair sharing a CONCEPT_GROUP must differ on
        presentation_key = (stem_format_variant | distractor_strategy).
        So two Antonym questions may NOT both be "isolated-word stem + 3-near-
        synonyms-of-headword distractors"; at least one must change format (e.g.
        sentence-embedded) or distractor strategy (e.g. same-semantic-field). See
        §6-3c for the enumerated variation menus and the ≥2-formats rule for N≥3.
        *** v4.5 — CLASS-2 under answer_cardinality=='multi' (MSQ vocabulary, dormant unless
        multi_present). The fixed operation INVERTS: a "select all synonyms of X" item
        has a correct SET of |S| true synonyms (1 ≤ |S| ≤ options_count−1, or =msq_k for
        fixed-k) plus (options_count−|S|) genuine non-synonyms as distractors — NOT the
        single-correct "1 synonym + 3 near-synonym distractors" menu. The distractor menu
        for a multi vocabulary item therefore supplies the OUT-SET pool (clearly-wrong
        items: opposites / unrelated-register / false-friends), and the IN-SET is the set
        of defensibly-correct items. scenario_key is unchanged (subtopic|target_item — the
        headword is still one item). vocab_words_used records the FULL correct set (every
        in-set word), not one word, so cross-mock vocab dedup (L8) cannot under-count.
        R-ANSWER (multi) + G-MSQ-SET/CARD govern the set; RULE C still applies.

    CLASS 3 — FACT-RECALL (e.g. single-fact questions in any knowledge/awareness
              section — GA, GK, static GK, current affairs, domain-specific facts):
        The UNIT is the FACT asserted. scenario_key = subtopic | normalized_fact
          (e.g. "polity|president_election_process").
        Two fact-recall questions on the SAME fact = banned; on different facts = allowed.
        (Cross-mock fact uniqueness already enforced by L4 ga_facts_used.)
        v3.8 (DOUBT-4): like CLASS 2, a different FACT is necessary but not
        sufficient. Two CLASS-3 questions in the same CONCEPT_GROUP must ALSO
        satisfy RULE C (§6-3c) — they may not share presentation_key
        (stem_format_variant | distractor_strategy). E.g. do not pose two polity
        facts as identical "Which of the following is correct?" stems with the
        same distractor pattern; rotate format (direct / fill-blank / assertion-
        reason / match / odd-one-out) and distractor type.

    CLASS 4 — LINKED-STIMULUS GROUPS (RC passage→5Q, DI table→2-3Q, Cloze→5
              blanks): the SHARED STIMULUS is allowed to back several questions
              (that is the format, not a repeat). The UNIT is the SUB-SKILL of
              each linked question.
        scenario_key = group_type | sub_skill
          RC examples:  "rc|direct_retrieval", "rc|inference", "rc|vocab_in_context",
                        "rc|tone_attitude", "rc|main_idea".
          DI examples:  "di|percentage_change", "di|ratio_compare", "di|average".
          Cloze:        each blank tests a distinct grammar/vocab point →
                        "cloze|collocation", "cloze|connector", "cloze|tense".
        WITHIN one linked group, no two questions may share a sub_skill
        scenario_key (no two pure inference RC Qs; no two identical DI operations).
        The shared stimulus itself is NOT counted as a repeat.
        This satisfies §8 RC minimums (≥1 inference, ≥1 vocab, ≥1 tone) AND the
        no-repeat rule simultaneously.
        DELIVERY NOTE (v3.6): CLASS 4 governs CONTENT uniqueness only. The DELIVERY
        of these groups (how the shared stimulus is physically placed so each
        member renders self-contained on a one-question screen) is governed
        separately by §9 SELF-CONTAINMENT (Model A default) + R-LINKED +
        G-STIMULUS-ORPHAN. Both must pass.

    CLASSIFICATION SOURCE: derive the class from the subtopic's format field and
    CONCEPT_GROUP in section_rules.md. If ambiguous, default to CLASS 1 (strictest).

  ───────────────────────────────────────────────────────────────────────
  §6-3c — RULE C: PRESENTATION UNIQUENESS (DOUBT-4, v3.8 — HARD, intra-mock)
  ───────────────────────────────────────────────────────────────────────
    WHY: scenario_key (RULE B) guarantees no two questions share the same
    CONTENT. It does NOT stop two questions LOOKING identical. For format-fixed
    subtopics (CLASS 2 vocabulary/item-recall, CLASS 3 fact-recall) the operation
    is constant by definition, so unless presentation is actively varied, every
    question in the CONCEPT_GROUP is a visual clone (the M1 Q.77/Q.79, Q.78/Q.80
    defect). RULE C adds the missing PRESENTATION axis.

    presentation_key = canonical(stem_format_variant + "|" + distractor_strategy)

    THE RULE (applies to CLASS 2 and CLASS 3; CLASS 1 and CLASS 4 are exempt —
    their variety is already carried by scenario_key / sub_skill). Let
    M = size of this family's stem_format_variant menu (resolve_presentation_family):
      (C1) DISTINCT VISIBLE FORMAT (primary, v3.9): for every PAIR of questions in
           the mock that share a CONCEPT_GROUP, stem_format_variant MUST differ,
           as long as the group's question count ≤ M (which it virtually always is
           — M is 3–6 and a CONCEPT_GROUP rarely holds >4 Qs). This guarantees two
           same-group questions never read with the same on-screen structure (the
           M1 complaint), not merely different distractors.
      (C2) DISTINCT presentation_key (always): every pair sharing a CONCEPT_GROUP
           MUST also differ on presentation_key = (stem_format_variant |
           distractor_strategy). When (and only when) a group's count EXCEEDS M, a
           stem_format_variant may repeat, but then the distractor_strategy must
           differ so presentation_key still differs. A distinct scenario_key
           (different word/fact) is NECESSARY but NOT SUFFICIENT.
      (C3) presentation_key AND stem_format_variant are persisted per question in
           the concept_map sidecar (§11) alongside scenario_key, and verified
           mock-wide by G-FORMATDUP (§12 S12-NEW-12).

    PRESENTATION_FAMILY (v3.9 — defined, not just exemplified): the coarse
    surface-look grouping a subtopic belongs to, resolved by
    resolve_presentation_family() below. Used by C1/C2 (to pick the right menu)
    AND by R19 anti-clustering (no contiguous run > 2 of one family). Default
    families: vocab_single_word {Antonym, Synonym, Spelling, Homonym},
    one_word_substitution {One-Word-Substitution}, idiom_phrase {Idioms},
    sentence_grammar {Error, Improvement, Voice, Narration, Tense}, fact_recall
    {GA/GK single-fact}.
    section_rules.md may override via a subtopic 'presentation_family' field.

    ENUMERATED VARIATION MENUS (the supply RULE C draws on; made executable in the
    helpers below; exam-agnostic — extend per section_rules.md if an exam adds a
    format):

      stem_format_variant
        · vocab_single_word (Antonym/Synonym/Spelling/Homonym):
            {isolated_word, sentence_embedded_underlined, fill_in_context_blank,
             odd_one_out_pair, definition_to_word}
        · one_word_substitution:
            {phrase_to_word, sentence_embedded_underlined, reverse_word_to_phrase}
        · idiom_phrase:
            {meaning_of_idiom, idiom_for_situation, sentence_substitution,
             odd_one_out}
        · fact_recall (CLASS 3):
            {direct_question, fill_blank, assertion_reason, match_the_following,
             odd_one_out, statement_correctness}

      distractor_strategy
        · vocab:
            {near_synonyms_of_headword, same_semantic_field,
             morphological_lookalike, register_or_collocation_trap,
             true_opposite_as_trap, commonly_confused_pair}
        · fact_recall:
            {plausible_same_category, swapped_attribute, close_date_or_number,
             common_misconception, adjacent_entity}

    EXECUTABLE HELPERS (v3.9 — close G1/G2; referenced by S7-CONCEPT):
    ```python
    # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
    PRESENTATION_FAMILIES = {
      'vocab_single_word'    : {'antonym','synonym','spelling','homonym'},
      'one_word_substitution': {'one_word_substitution'},
      'idiom_phrase'         : {'idiom_meaning','idiom','phrase'},
      'fact_recall'          : {'ga_fact','gk_fact','static_gk','current_affairs'},
    }
    STEM_FORMAT_MENU = {
      'vocab_single_word': ['isolated_word','sentence_embedded_underlined',
                            'fill_in_context_blank','odd_one_out_pair',
                            'definition_to_word'],
      'one_word_substitution': ['phrase_to_word','sentence_embedded_underlined',
                                'reverse_word_to_phrase'],
      'idiom_phrase'     : ['meaning_of_idiom','idiom_for_situation',
                            'sentence_substitution','odd_one_out'],
      'fact_recall'      : ['direct_question','fill_blank','assertion_reason',
                            'match_the_following','odd_one_out',
                            'statement_correctness'],
    }
    DISTRACTOR_MENU = {
      'vocab_single_word': ['near_synonyms_of_headword','same_semantic_field',
                            'morphological_lookalike','register_or_collocation_trap',
                            'true_opposite_as_trap','commonly_confused_pair'],
      'one_word_substitution': ['near_synonyms_of_headword','same_semantic_field',
                                'commonly_confused_pair','register_or_collocation_trap'],
      'idiom_phrase'     : ['near_synonyms_of_headword','same_semantic_field',
                            'commonly_confused_pair','register_or_collocation_trap'],
      'fact_recall'      : ['plausible_same_category','swapped_attribute',
                            'close_date_or_number','common_misconception',
                            'adjacent_entity'],
    }

    def resolve_presentation_family(subtopic_data):
        """G6: authoritative family resolver. Honour an explicit section_rules.md
        'presentation_family' field; else map by CONCEPT_GROUP; else by class."""
        fam = subtopic_data.get('presentation_family')
        if fam in STEM_FORMAT_MENU: return fam
        cg = (subtopic_data.get('CONCEPT_GROUP') or '').lower()
        for family, members in PRESENTATION_FAMILIES.items():
            if cg in members: return family
        # class-based fallback
        return 'fact_recall' if subtopic_data.get('SUBTOPIC_CLASS') == 'CLASS3' \
               else 'vocab_single_word'

    def format_menu_for(subtopic_data):       # G2
        return STEM_FORMAT_MENU[resolve_presentation_family(subtopic_data)]
    def distractor_menu_for(subtopic_data):   # G2
        return DISTRACTOR_MENU[resolve_presentation_family(subtopic_data)]

    def classify_subtopic(subtopic_data):
        """G1: derive the canonical SUBTOPIC_CLASS token. Tokens 'CLASS1'..'CLASS4'.
        v5.15 — LANGUAGE-AGNOSTIC + ROBUST (fixes the non-English RULE-C-disabled defect:
        an English-keyword-only classifier collapsed every non-English subtopic to CLASS1,
        silently switching OFF presentation-uniqueness so format-clone questions shipped).
        Order:
          (0) honour an explicit SUBTOPIC_CLASS from section_rules (forward-compat);
          (1) PASSAGE/DI/linked -> CLASS4;
          (2) map by CONCEPT_GROUP family — Step 5 v2.24 emits a canonical, TRANSLITERATED
              family even for Hindi/regional exams (पर्यायवाची -> 'synonym'), matched on the
              coarse base (strip any '__qualifier');
          (3) LANGUAGE-AGNOSTIC fallback: an EXPLICIT presentation_family (set by Step 5 from
              observed axis data, language-independent) → CLASS2/CLASS3, so RULE C stays ACTIVE.
              NOTE: we use only an EXPLICIT presentation_family here — never the resolver's
              vocab default — so reasoning subtopics are NOT misclassified as vocab;
          (4) else CLASS1 (computation/reasoning — strictest).
        Set once during S3-8 id-join and stored on subtopic_data."""
        explicit = str(subtopic_data.get('SUBTOPIC_CLASS') or '').upper()
        if explicit in ('CLASS1','CLASS2','CLASS3','CLASS4'):
            return explicit
        fmt = (subtopic_data.get('format') or 'TEXT').upper()
        if fmt in ('PASSAGE','DI') or subtopic_data.get('linked_group_id'):
            return 'CLASS4'                                  # linked-stimulus
        cg   = (subtopic_data.get('CONCEPT_GROUP') or '').strip().lower()
        base = cg.split('__', 1)[0]                          # coarse family (drop qualifier)
        VOCAB = {'antonym','synonym','spelling','homonym','one_word_substitution',
                 'idiom','idiom_meaning','idiom_phrase','phrase','phrasal_verb'}
        FACT  = {'ga_fact','gk_fact','static_gk','current_affairs','general_knowledge'}
        if cg in VOCAB or base in VOCAB:      return 'CLASS2'  # vocabulary/item-recall
        if cg in FACT  or base in FACT:       return 'CLASS3'  # fact-recall
        pf = str(subtopic_data.get('presentation_family') or '').strip().lower()
        if pf in ('vocab_single_word','idiom_phrase'):  return 'CLASS2'   # explicit family only
        if pf == 'fact_recall':                          return 'CLASS3'
        return 'CLASS1'                                       # computation/reasoning (strictest)
    ```

    ── v5.14 THREE-AXIS: OPTION-3 JOINT SOLVE — AXIS-2 STEERING (mirrors Step 5 classifier) ──
    ```python
    # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
    # Canonical stem_format_variant → Axis-2 class map. IDENTICAL semantics to Step 5's
    # STEM_FORMAT_TO_AXIS2 (AXIS CLASSIFIER v1.0). This is how a generated question's Axis-2
    # class is known from the variant it renders. Keep in sync with Step 5 if a variant is added.
    STEM_FORMAT_TO_AXIS2 = {
        'direct_question': 'DIRECT', 'isolated_word': 'DIRECT', 'phrase_to_word': 'DIRECT',
        'reverse_word_to_phrase': 'DIRECT', 'definition_to_word': 'DIRECT',
        'meaning_of_idiom': 'DIRECT', 'idiom_for_situation': 'DIRECT',
        'sentence_substitution': 'DIRECT', 'sentence_embedded_underlined': 'DIRECT',
        'fill_blank': 'FILL_BLANK', 'fill_in_context_blank': 'FILL_BLANK',
        'assertion_reason': 'ASSERTION_REASON', 'match_the_following': 'MATCH',
        'statement_correctness': 'STATEMENT', 'sequence_ordering': 'SEQUENCE',
        'odd_one_out': 'ODD_ONE_OUT', 'odd_one_out_pair': 'ODD_ONE_OUT',
    }
    # One canonical variant per Axis-2 class (used to add a capable-but-non-family variant,
    # e.g. an OBSERVED SEQUENCE, to a subtopic's candidate set). LINKED has no stem variant
    # (stimulus-locked, allocation-enforced) so it is intentionally absent.
    AXIS2_TO_STEM_FORMAT = {
        'DIRECT': 'direct_question', 'FILL_BLANK': 'fill_blank',
        'ASSERTION_REASON': 'assertion_reason', 'MATCH': 'match_the_following',
        'STATEMENT': 'statement_correctness', 'SEQUENCE': 'sequence_ordering',
        'ODD_ONE_OUT': 'odd_one_out',
    }

    # ── WINDOW TRACKER (registry-resident; cross-mock). Plain dicts so it serializes into
    #    registry.json. One tracker per section for the CURRENT 10-mock window. ────────────
    def axis2_window_index(mock_n, mocks_per_window):
        return (int(mock_n) - 1) // max(1, int(mocks_per_window))

    def build_axis2_tracker(section_sched, window_counts):
        """section_sched = blueprint.axis_schedule[section] (or None); window_counts = the
        section's running counts for THIS window (from registry, {} if new window). Returns a
        tracker dict, or None when there is no usable target (feature inert)."""
        if not section_sched or section_sched.get('status') != 'ok':
            return None
        return {
            'window_target': dict(section_sched.get('axis2_window_target', {})),  # band-mode quotas
            'guarantee':     list(section_sched.get('axis2_guarantee', [])),      # >=1 per window
            'negative_rate': float(section_sched.get('negative_rate', 0.0)),
            'counts':        dict(window_counts.get('counts', {})),
            'neg_count':     int(window_counts.get('neg_count', 0)),
            'total':         int(window_counts.get('total', 0)),
        }

    def axis2_need(tr, cls):
        """How much the window still WANTS this Axis-2 class (higher = more). A pending
        guarantee dominates; else the remaining band gap; DIRECT/float and met/over = 0."""
        if tr is None or cls == 'DIRECT' or cls == 'LINKED':
            return 0.0
        have = tr['counts'].get(cls, 0)
        if cls in tr['guarantee']:
            return 1000.0 if have == 0 else 0.0     # only needed until its first appearance
        tgt = tr['window_target'].get(cls, 0)
        gap = tgt - have
        return float(gap) if (tgt > 0 and gap > 0) else 0.0

    def axis2_record(tr, cls, is_negative):
        if tr is None:
            return
        tr['counts'][cls] = tr['counts'].get(cls, 0) + 1
        tr['total'] += 1
        if is_negative:
            tr['neg_count'] += 1

    def axis2_want_negative(tr):
        """Soft nudge (decision 12): True when the window's running negative rate is below
        the section target. build_question honours this best-effort; never a hard gate."""
        if tr is None or tr['negative_rate'] <= 0:
            return False
        cur = (tr['neg_count'] / tr['total']) if tr['total'] else 0.0
        return cur < tr['negative_rate']

    def axis2_window_snapshot(tr):
        """Serialize the mutated counts back for the registry commit (S13-4)."""
        if tr is None:
            return None
        return {'counts': tr['counts'], 'neg_count': tr['neg_count'], 'total': tr['total']}

    # ── CAPABILITY-BOUNDED candidate variants (File 1 untouched; consistent with Step 6). ──
    def axis2_candidate_variants(subtopic_data, family_menu):
        """Faithful candidate stem_format_variants for target-aware selection, always
        INTERSECTED with the subtopic's axis2_capability (from section_rules, the File-1
        authority) — never offers a format the subtopic is not capable of (no fabrication,
        decision iii). DIRECT is always available (residual).
          • PYQ subtopics (CLASS 2/3): family-menu variants (correct for the family) PLUS a
            generic variant for each capable-but-non-family class (e.g. an OBSERVED SEQUENCE).
          • ZP subtopics: the CLASS1 default family menu is a VOCAB menu that is wrong for
            non-vocab content, so ZP draws GENERIC canonical variants (AXIS2_TO_STEM_FORMAT)
            straight from capability — neutral structures build_question can always render."""
        cap = set(subtopic_data.get('axis2_capability', ['DIRECT'])) or {'DIRECT'}
        variants, seen = [], set()
        if subtopic_data.get('is_zp'):
            for cls in cap:                         # generic canonical variant per capable class
                if cls in AXIS2_TO_STEM_FORMAT and cls not in seen:
                    variants.append(AXIS2_TO_STEM_FORMAT[cls]); seen.add(cls)
        else:
            for v in family_menu:                   # keep family order (RULE-C rotation stability)
                cls = STEM_FORMAT_TO_AXIS2.get(v, 'DIRECT')
                if cls in cap and cls not in seen:
                    variants.append(v); seen.add(cls)
            for cls in cap:                         # add capable-but-non-family (observed) classes
                if cls not in seen and cls in AXIS2_TO_STEM_FORMAT:
                    variants.append(AXIS2_TO_STEM_FORMAT[cls]); seen.add(cls)
        if 'DIRECT' not in seen:
            variants.append(AXIS2_TO_STEM_FORMAT['DIRECT'])
        return variants or [AXIS2_TO_STEM_FORMAT['DIRECT']]
    ```

    WHERE SUBTOPIC_CLASS IS SET (G1): during the S3-8 subtopic_id join, for every
    joined subtopic do `subtopic_data['SUBTOPIC_CLASS'] = classify_subtopic(...)`.
    S7-CONCEPT asserts it is present before generating; absence is a HARD STOP [HS:INFRA]
    (generator bug, not a silent default).
    v4.5: at the SAME join, set `subtopic_data['answer_cardinality'] =
    answer_cardinality_by_id.get(subtopic_id, 'single')` (whole-subtopic mode from the
    blueprint subtopic_list). This is the value build_question / verify_answer /
    write_q_to_sidecar read. 'single' for every subtopic when multi_present is false.
    v5.X POSITION-BASED OVERRIDE (GAP-2026-07-22-001 §6): when the exam has >1 distinct
    question_type in marking_scheme (e.g. IIT JAM: MCQ/MSQ/NAT), answer_cardinality and
    answer_type are overridden PER Q POSITION during the generation loop (not at S3-8 join
    time) via _resolve_answer_axes(qnum, subtopic_id). The S3-8 join still sets the
    per-subtopic defaults; the per-Q override happens at generation dispatch (S7-CONCEPT).
    v5.14 (THREE-AXIS): at the SAME join, ALSO set from section_rules.md (File-1 CATEGORY B) +
    blueprint subtopic_list:
      • subtopic_data['axis2_capability'] = the parsed axis2_capability list (default ['DIRECT']).
        This bounds axis2_candidate_variants — the generator NEVER offers a format the subtopic
        is not capable of (no fabrication, decision (iii)); File 1 stays the authority.
      • subtopic_data['observed_axis2']  = the parsed observed_axis2 dict (default {}).
      • subtopic_data['is_zp'] = (r_avg == 0.0) from the blueprint subtopic_list — routes ZP
        subtopics through the target-aware selector as format-elastic fillers (decision 11).
      • v5.15: subtopic_data['form_key'] = read_field(S,'form_key') from section_rules.md
        (Step 5 v2.24), fallback question_mechanic → CONCEPT_GROUP. This is the FINE identity
        Step 6 BV-10a keys on; Step 7 carries it so intra-mock duplicate reasoning and the
        audit align on the SAME axis as the blueprint gate (no coarse/fine mismatch).
    All three are absent-safe: missing section_rules fields ⇒ capability=['DIRECT'], observed={},
    which reduces the Axis-2 steering to DIRECT-only (i.e., the v5.13 behaviour) for that subtopic.

    NORMALISATION: lowercase, snake_case, strip values. A presentation_key is a
    pair of menu tokens, never free text. If the generator cannot name a token
    for a candidate, it has not chosen a defined variant → treat as a RULE-C
    violation (G-FORMATDUP) and pick an explicit variant.

    INTERACTION WITH RULE A/B:
      - RULE A (exact count) is untouched — N is still floor AND ceiling.
      - RULE B (scenario_key) still holds — no repeated item/fact.
      - RULE C is ADDITIONAL: the N questions of a format-fixed CONCEPT_GROUP must
        be pairwise-distinct on scenario_key AND stem_format_variant (count ≤ M)
        AND presentation_key. "Done" = N questions, each a different item AND a
        visibly different format.
      All checked together at Final Assembly (G-COUNT-X-UNIQUE + G-CONCEPTDUP +
      G-FORMATDUP).

    v5.14 — RULE C × AXIS-2 TARGET RECONCILIATION (decision (b)): the Option-3 joint solve
      (S7-AXIS) makes pick_presentation TARGET-AWARE, but RULE C stays a HARD constraint and
      WINS. The tracker only STABLE-RE-ORDERS the RULE-C-VALID (unused-for-this-cg) variants by
      Axis-2 window need; it never selects a used/duplicate variant to hit a target. So RULE C's
      pairwise-distinct stem_format_variant guarantee (C1/C2) and presentation_key uniqueness
      (C3, G-FORMATDUP) hold UNCHANGED. When uniqueness and the target genuinely conflict (the
      only unique variant left is not the one the target wants), uniqueness wins and the target
      yields — audited within tolerance by audit.py (S4-11), never fabricated.

    WORKED FIX (M1):
      Q.77 Antonym BENEVOLENT  → (isolated_word | near_synonyms_of_headword)
      Q.79 Antonym TRANSPARENT → also isolated_word → C1 COLLISION (same visible
      format) BEFORE even comparing distractors.
      Resolution: regenerate Q.79 with a DIFFERENT stem_format_variant, e.g.
      (sentence_embedded_underlined | same_semantic_field) — same subtopic, same
      "antonym" operation, but a visibly different question. scenario_key already
      differed; now format and presentation_key differ too.


  CROSS-MOCK vs INTRA-MOCK (do not confuse the two):
    The scenario_key rule here is INTRA-MOCK only — it bans repeats WITHIN one
    paper. The SAME scenario_key MAY appear in a DIFFERENT mock (that is a
    different paper and is expected). Cross-mock duplication of the actual
    question is separately prevented by L1/L2 against the registry. The two
    layers are complementary and must both pass (see enforcement loop CHECK 1
    and CHECK 2 below).

  ───────────────────────────────────────────────────────────────────────
  CONCEPT SOURCE ORDER — WHERE THE N DISTINCT SCENARIOS COME FROM
  (this is the crux of DOUBT-3; read carefully):
  ───────────────────────────────────────────────────────────────────────
    To fill N distinct scenario_keys for a subtopic, draw in this order:

      SOURCE 1 — OBSERVED PYQ patterns (PYQ_STEM_PATTERNS in section_rules.md):
        The SEED set. Frequency-weighted (most common patterns first, per S7-2).
        Each distinct observed pattern → one distinct scenario_key.

      SOURCE 2 — DOMAIN-GENERATED scenarios (Claude's own knowledge):
        When N exceeds the number of distinct observed PYQ patterns, INVENT
        additional genuinely-distinct scenarios from domain knowledge. Each
        must (a) fit the subtopic, (b) match the difficulty calibration for
        its slot, (c) obey ALL quality gates and banned-pattern rules.

    THE PYQ PATTERN LIST IS A SEED, NEVER A CEILING.
    "Ran out of patterns / not enough distinct concepts available" is NOT a
    valid state and is NOT a reason to reduce N or repeat a scenario. Subtopics
    like CI, Blood Relations, Syllogism, Mensuration, etc. have effectively
    UNLIMITED distinct scenarios — generate as many distinct ones as N requires.
    The generator is expected to create novel, exam-realistic scenarios beyond
    the observed PYQ set whenever N demands it.

  ───────────────────────────────────────────────────────────────────────
  THE ENFORCEMENT LOOP (per question, in order — all three must pass):
  ───────────────────────────────────────────────────────────────────────
    At session start, maintain in-memory (persisted to batch_state.json):
      mock_scenario_ledger     = set()   # scenario_key strings used in THIS mock
      mock_presentation_ledger = set()   # (concept_group, presentation_key) pairs
                                         # for CLASS 2/3 — RULE C (v3.8)

    For each question slot of a subtopic (looping exactly N times per subtopic):
      Build a candidate question, then check IN THIS ORDER:

      CHECK 1 — Intra-mock scenario uniqueness (RULE B):
        if candidate.scenario_key in mock_scenario_ledger:
            → REJECT. Regenerate on a DIFFERENT scenario (new operation/shape).
              Never reduce N. Never reuse a scenario_key.

      CHECK 1b — Intra-mock PRESENTATION uniqueness (RULE C, v3.8; CLASS 2/3 only):
        Let cg = candidate.concept_group. If the candidate is CLASS 2 or CLASS 3
        and (cg, candidate.presentation_key) already in mock_presentation_ledger:
            → REJECT. Regenerate with a DIFFERENT stem_format_variant OR
              distractor_strategy (draw a fresh pair from the §6-3c menus).
              Never reduce N. Never reuse a (cg, presentation_key) pair.
        Also enforce C2: if cg will reach q_count ≥ 3, ensure the chosen
        stem_format_variants for cg span ≥ 2 distinct values by the time the
        group is complete (track per-cg format set; if the last slot would leave
        only 1 distinct format, force a new format).

      CHECK 2 — Cross-mock dedup vs registry_snapshot (L1/L2):
        if candidate collides with a prior mock's question (Jaccard ≥0.75
        OR matching semantic tuple):
            → REJECT. Regenerate on a different scenario/values.

      CHECK 3 — Quality gates (§7): difficulty floor, banned patterns,
        3-pass verify, option quality, etc.
        if any fails → REJECT and regenerate.

      CHECK 3c — DIFFICULTY CONFORMANCE (G-DIFF, v5.60 — skipped only when
        difficulty_plan is None, the documented dormant state):
        The slot's band is difficulty_plan[q]. AUTHOR TO THE BAND from the start:
        bc.difficulty_authoring_profile(band, qtype, difficulty_labels,
        rule=bc.RUBRIC_RULE_CURRENT) (v5.92 — rubric r2, GAP-2026-11-05 Part B) names
        the class facets, INFERENTIAL-MOVE range and concept count that provably land
        in the band — write the question AND its solution inside that profile
        (a bottom-band slot is recall/one-principle and NEVER computational,
        figural, structural or derivational; a top-band slot is a genuinely long or
        multi-concept derivation — more Hard in the trigger means AUTHORING harder
        questions, never renaming easier ones).
        While deriving the answer for the sidecar (the derivation already
        happens — §S7-NEW-A), RECORD the observations the derivation revealed:
          difficulty_obs = {'question_class': [facet, ...],   # incl. C-FIGURAL / C-STRUCTURAL
                            'deduction_steps': <int>,          # DEDUCTION paragraphs (unchanged)
                            'inferential_steps': <int>,        # v5.92: moves, by the ONE rule below
                            'rubric_rule': bc.RUBRIC_RULE_CURRENT,   # v5.92: 'r2' (guard G1)
                            'axiom_concepts': <int>,           # distinct principles
                            'speed_hack_exists': <bool>,
                            'is_negative': <bool>,             # NOT/EXCEPT polarity
                            'qtype': 'mcq'|'msq'|'nat'}
        Count honestly — moves a competent candidate needs, not padding; the
        count is evidence, and A-QINDEX check 8 re-runs the same arithmetic on
        it forever, UNDER THE RULE THE OBS CARRIES (an obs without one is r1).
        THE ONE COUNTING RULE (v5.92 — DL-15; `bc.INFERENTIAL_STEP_RULE`, quoted
        verbatim here and in PYQExplain §7A-2, so a PYQ band and a mock band use
        the same unit):

          > An INFERENTIAL STEP is one reasoning move that produces a new fact the
          > next move uses: applying a principle, predicting one transformation's
          > product, eliminating an option class, or one manipulation of a relation.
          > NOT a step: restating the stem, reading a value or a structure off the
          > figure, naming the answer option (the answer-binding sentence), or
          > splitting one move across paragraphs. A pre-requisite fact at the level
          > of a standard textbook (pH of water, valency, a reagent's identity) is
          > part of the step that uses it. Count moves, never paragraphs; a pure
          > recall item has 0.
        LEVEL ANCHOR (v5.60) — the UNIT of the count is level-relative even
        though the rubric's arithmetic is universal: a "step" is one reasoning
        move for a competent candidate OF THIS EXAM (bp_level, S3-2 — grade-10
        through post-graduation), and the exam's ASSUMED PREREQUISITE KNOWLEDGE
        is recall (0 steps), NEVER steps. What a grade-12 candidate must reason
        through, a post-graduate candidate simply knows — so the same physical
        question legitimately scores lower on a higher-level exam. Calibrate
        the granularity against the subtopic's calibration examples from the
        exam's DIFFICULTY PROFILE (v5.75 — bc.dp_calibration(DIFFICULTY_PROFILE,
        subtopic_id, PROFILE_CFG): real questions of THIS exam with their
        recorded step and concept counts, scored by the same rubric; loaded
        once in S3 from /mnt/project/[ExamCode]_difficulty_profile.json,
        None when absent — then no examples, the anchor rules alone apply).
        Counting a question in a lower level's step-units inflates
        every score and mislabels the whole paper for its audience; Step 9's
        §7A-M re-count at the same anchor is the cross-check that exposes it.
        v5.89 — TWO EVIDENCE CHECKS THE AUTHOR DOES NOT CONTROL (GAP-2026-11-02
        L1/L3; owner decision 2026-11-02 "holes 2-4"). The rubric above scores
        evidence the AUTHOR declares; measured on a delivered paper, 24 items
        declared 5-6 steps and labelled Hard were easier than the real exam's
        Medium items. Two checks anchor the label to the EXAM ITSELF:
          v6.1 (S0-BV): those graders run in S4-7 STEP A2 for the whole batch, before it is delivered — CHECK 3c
              writes the item and its record; it never grades.
          v6.0 (GAP-2026-11-10, S0-OP-5 — BINDING FOR EVERY ITEM OF EVERY EXAM): the rating below is now done
              by TWO FRESH BLIND GRADERS in fresh contexts (sub-agents or Orchestrate workers), each given
              ONLY the packet bc.build_judge_input builds, plus the recipe check and two fresh blind solvers;
              the label is written only by bc.dl_set_label_basis_strict (measured_exact). The author's own
              in-context rating and its counts are NEVER a control and never set or verify a label. The
              DORMANT 'agree' rule below is RETIRED: with no content-carrying exemplar for a band the graders
              use the ruler's library-level anchors (S0-OP-2) — they are never told to agree by default.
          (a) INDEPENDENT RATING — every item, every exam [CLASS: J]. After the
              item and its solution are final, rate it BLIND. v5.90 (GAP-2026-11-03
              G02 R2.1/R2.2): the exemplars are CONTENT-CARRYING — from the
              exemplar bank (S3-2e EXEMPLAR_BANK_PATH; per cascade cell x band x
              qtype: stem, options, key, the figure CONTENT RECORD) — because a
              <= 120-character stem snippet of a figural item ("Identify the major
              product, P ...") carries no chemistry and lets the rater compare
              only the author's own step counts (the incident's "agree" on 29 Easy
              items labelled Hard). Build the packet with
              EX = bc.exemplars_for(EXEMPLAR_BANK, subtopic_id, qtype, difficulty_labels)
              PK = bc.build_judge_input(item_record, EX['by_band'], difficulty_labels)
              where EXEMPLAR_BANK is the parsed S3-2e bank ({} when absent) and
              bc.exemplars_for walks the cascade cells[subtopic_id -> topic -> section]
              [band][qtype] PER BAND (first level holding >= 1 exemplar of that band,
              k <= 3; record EX['level_used'] (per band) and EX['complete'] — a band
              with no exemplar at any level is rated with that caveat in the
              rationale, never a stop) — the packet STRIPS difficulty_plan /
              difficulty_obs / solution / rationale, and PK['sha256'] is stored
              as difficulty_check.judge_input_sha256. Rate ONLY from PK: which
              band's exemplars the new item most resembles in what a candidate
              must know and do; write the rationale (one sentence citing the
              exemplar it matches) and the band: rated_band; also the pairwise
              verdict harder / comparable / easier against the scheduled band's
              median exemplar (recorded). Fallback when the bank is ABSENT
              (OD-11: it is a delivered run file, not project knowledge): EX =
              bc.difficulty_exemplars(DIFFICULTY_PROFILE, subtopic_id, section,
              difficulty_labels, k=3, gap_days=PROFILE_CFG.get('cycle_gap_days'))
              snippets, rated with rationale prefixed "snippets only — no exemplar
              bank"; S3-2e has already printed G-DIFF-JUDGE MISSING. v5.92 (GAP-2026-
              11-05 DL-37): for a FIGURAL CHEMISTRY item (one carrying content
              objects of kind STRUCTURE / REACTION) the snippet fallback is DORMANT —
              a snippet carries no chemistry, and rating from it echoes the author's
              own counts. DORMANT when neither source holds a content-carrying
              exemplar for at least two bands: [v6.0 RETIRED for every new paper — the
              graders use the ruler's library-level anchors; a grade is never copied from
              difficulty_plan] (legacy v5.92 text: rated_band = difficulty_plan[q], decision
              `agree`, level_note 'unverified', DIFFICULTY_STATE['judge_dormant_qs']). Never a stop (OD-1).
          (b0) ORGANIC DECISION-LOAD RULER — L2 ITEM (v5.94, GAP-2026-11-07; owner D1 (b), D3,
              D4, D6). An L2 ITEM is one whose subtopic_id is in L2_SCOPE_IDS while L2_MODEL
              (S3-8L) is active. AUTHOR FROM THE PATTERN, NEVER FROM A PAST QUESTION (D6): the
              slot's source is L2_SOURCES[str(q)] (S3-15L) — a pattern card names WHAT must be
              decided (concept chain with loads, ask type, distractor relations, stereo kind);
              a concept source names the one concept the item must turn on. Write a NEW
              substrate and a NEW question whose solution genuinely needs that decision load;
              a top-band slot is a chain of high-load decisions with close distractors, never a
              bigger molecule. While deriving the answer RECORD on difficulty_obs (the same
              keys the exam's own past questions carry — one ruler for both, D3):
                'named_concepts': [labels SELECTED from bc.l2_vocabulary() — every concept the
                                   solution uses, none it does not; 'other:<text>' for one
                                   outside the vocabulary],
                'stereo_decl':    'none' | 'relative' | 'absolute' (what the ANSWER must state),
                'ask_type':       the figural ask type (S7-QUALITY), 'reagents_seen' (b1 input),
                'closeness':      bc.option_closeness(option_smiles, key_smiles) (None w/o RDKit),
                'distractor_mechanisms': the item's quality-record list (one token per wrong
                                   option; an isomer token on a non-isomer option is not counted).
              G-L2CARDCOPY: bc.l2_copy_check(key_smiles, DIFFICULTY_PROFILE) True -> the key is a
              past question's answer: REJECT and re-author on a new substrate (R2; None = dormant,
              printed once). Then l2 = bc.l2_record(difficulty_obs, L2_MODEL, difficulty_labels,
              qtype); l2['binding'] = bool(L2_MODEL binding) (v5.96 — the label verifier reads it);
              difficulty_obs['l2'] = l2. When L2_MODEL is BINDING, l2['band'] is this
              item's CONTENT EVIDENCE: the (b1) level record is still computed and recorded
              (informational — L1 measures size, not decision load) but does not decide; when
              ADVISORY, l2 is recorded and (b1)/(b2) decide as before. An item whose
              named_concepts list is empty has NO ruler band (l2['band'] None — never the
              bottom band); the other controls decide.
          (b) CONTENT LEVEL — every content kind whose figure_types.QUALITY_ROWS
              row names a complexity_vector (chemistry: bc.content_vector; a kind
              with None -> N/A(listed), the judge alone decides). FIRST (v5.92, both
              paths): an item whose content objects include kind STRUCTURE / REACTION
              is a CHEMISTRY item — DIFFICULTY_STATE['n_level_items'] += 1 the first
              time its slot is measured (persisted with batch_state), WHETHER OR NOT the
              level model is active; that count is what makes S13-6 / MockDeliver print
              `DIFFICULTY UNVERIFIED — N chemistry item(s) written without an active level
              model` when it is dormant. THE INPUTS of (b1), all from the item being
              written (never declared): objects = the item's content objects (each draw's
              `.canonical` SMILES / reaction SMILES — the S7-NEW-B2 registration);
              option_smiles = {option label: that option draw's canonical SMILES} for every
              structure option; key_smiles = option_smiles[the correct option's label];
              reagents_seen = bc.reagent_names_of(objects). TWO paths, decided ONCE per
              item by what it carries:
              (b1) LEVEL ITEM (v5.92 — GAP-2026-11-05 Part A, rule L1; DL-38/41/44):
                  the item carries content objects of kind STRUCTURE / REACTION and
                  LEVEL_MODEL (S3, the ONE builder bc.level_model_for_scope) is
                  active. Measure the item the way the exam's own items were measured:
                    _cv   = bc.content_vector(objects, answer_smiles, METHOD_LEXICON)
                    _cl   = bc.option_closeness(option_smiles, key_smiles)   # DL-44; None w/o RDKit
                    _lv   = bc.level_vector(_cv, closeness=_cl,      # the record (or its mean)
                                            reasoning_score=bc.difficulty_score_from_obs(difficulty_obs),
                                            method_tier=bc.method_tier_of(reagents_seen, METHOD_LEXICON))
                    lc    = bc.level_check(LEVEL_MODEL, _lv, difficulty_plan[q],
                                           difficulty_labels, qtype)
                  lc['status'] is 'ok' | 'below' | 'above' | 'dormant' (BOTH directions,
                  DL-41 — a Medium slot drawn at Hard chemistry is 'above', a finding
                  too); lc['record'] is the L1 level record (full-precision composite,
                  cuts, qtype-clamped band). RECORD on the item, INSIDE difficulty_obs
                  (which travels verbatim into registry.question_index):
                  difficulty_obs['level'] = lc['record'], difficulty_obs['level_vector']
                  = _lv, difficulty_obs['closeness'] = _cl, difficulty_obs['reagents_seen']
                  = reagents_seen, difficulty_obs['rubric_rule'] = 'r2'; the quality record
                  carries ask_format (S7-QUALITY). (n_level_items was counted above.)
                  No ccp_floor_check and no final_band_decision for a level item — the
                  level record IS the content evidence; the two were measured on
                  different scales and must never be combined.
              (b2) EVERY OTHER ITEM — the v5.90 CONTENT FLOOR, unchanged: when CCP_MODEL
                  is active, ccp = bc.ccp_floor_check(CCP_MODEL, bc.content_vector(
                  objects, answer_smiles, METHOD_LEXICON), difficulty_plan[q],
                  difficulty_labels). 'below' is the finding; 'above' is allowed and
                  recorded. Dormant when the pool has < 20 transcribed items (footer
                  "level control: rubric + independent rating only (content-complexity
                  model dormant)"). A chemistry item while LEVEL_MODEL is dormant takes
                  this path and the paper gets the AMBER `DIFFICULTY UNVERIFIED` line
                  (S13-6) — measured honestly as far as the inputs allow, never silent.
          DECISION:
            v5.94 — THE MEASURED BAND (owner D1 (b), every exam): measured = the LOWEST band of
              the independent controls (bc.difficulty_band_min): the judge's rated_band (NOT when
              the judge was dormant) and the content evidence — an L2 item under a binding model:
              l2['band']; a level item: lc['record']['band']; any other item: the (b2) floor band
              when it says 'below'. The author's counts are never a control. Record it as
              difficulty_check['measured'] (S13-2G phase 3 reads it). measured == scheduled ->
              'agree'; ABOVE -> the 'harder' path below, unchanged; BELOW -> THE DL REPAIR, which
              REPLACES the R5 easier relabel: r = bc.difficulty_repair_step(target band,
              measured, difficulty_labels, rung, tries, sources_tried, has_source) inside the ONE
              G-DIFF budget — 'reauthor' (DR1): write the item again from the NEXT pattern source
              (L2 item: bc.l2_slot_source(..., skip=k); any other item: the next exemplar of the
              cell); 'reauthor_target' (DR2): the band-target brief (the band's profile and its
              exemplars side by side). When the budget is spent (v6.0: there is no band-swap
              escape): CARRY TO REVIEW — accept at the SCHEDULED band with decision
              'carried_below' (final_band = scheduled, the label stays the slot's band); S13-2G
              phase 3 repairs it once more; v5.96 (OD-2026-11-09): still below after round 2 -> S13-2L
              opens its DIFFICULTY chain (v6.0 SC2: rework, replace, shape, sibling, reserve_refill, refill_session,
              then the bounded last_resort, disclosed) — it is NEVER accepted lower (no DR3 relabel).
              Rungs and counters persist in batch_state['_diff_tries'] ('<q>:dr1' sources tried,
              '<q>:dr2' tries). PERSIST difficulty_state by MERGING (stored.update(DIFFICULTY_STATE)),
              never by replacing it: S13-2G phase 3 and S13-2L add paper_gate / chain_footer (legacy: dr3_qs / hard_missed)
              to the stored record.
            LEVEL ITEM (b1) — the level record and the independent rating decide:
              lc 'ok' and rated_band == scheduled -> 'agree', ACCEPT at the scheduled
              band; r = bc.reconcile_difficulty(difficulty_plan[q], None, None,
              labels=difficulty_labels) is the recorded decision record.
              lc 'below' -> ladder reason 'easier' (A-CONTENTLEVEL; v5.94: = THE DL REPAIR
              above, ending in carry-to-review — never a relabel); lc 'above' ->
              reason 'harder'. Owner D11 (A): lc 'ok' on a TOP-band slot but rated_band
              BELOW it -> rl = bc.reconcile_level(difficulty_plan[q], lc['status'],
              rated_band, difficulty_labels, diff_tries.get(str(q), 0)); rl['retry']
              True spends exactly ONE extra RETRY from the SAME MAX_DIFF_TRIES budget
              (g_diff_gate marks diff_tries['<q>:d11']; reason rl['reason'] in the
              escalating brief); on the next pass, or when the budget is already spent,
              -> ACCEPT at the scheduled band with difficulty_check.level_note 'judge
              below level' — never a second budget, never a stop. v5.94: SUPERSEDED for the
              decision — the judge's rated_band is a control of THE MEASURED BAND, so a judge
              below the slot takes THE DL REPAIR and, if it persists, carry-to-review (the
              G-DIFF ACCEPT above only means the counts support the band). A level band ABOVE the slot
              is a FAILED candidate (v6.0 R5 below — never held, never relabelled).
            OTHER ITEM (b2) — v5.90 unchanged (v5.94: a band it gives BELOW the slot is THE
              MEASURED BAND's DL repair / carry-to-review, never the label): the band is bc.final_band_decision(
              rated_band, ccp['status'] if ccp else None, ccp['ccp_band'] if ccp
              else None, difficulty_labels) — rated unless the floor says 'below',
              then the lower of the two; the author's counts never raise it;
              r = bc.reconcile_difficulty(difficulty_plan[q], rated_band,
              ccp['status'] if ccp else None, labels=difficulty_labels). A measured band ABOVE the slot
              is a FAILED candidate (v6.0 R5 below — never held, never relabelled).
          In BOTH paths: 'agree' -> ACCEPT; 'ladder' -> the slot enters §Q8b-LADDER
          with reason r['reason'] ('harder' / 'easier'; A-DIFFRATING /
          A-CONTENTLEVEL), R2 first; R5 is the v6.0 rule below (a candidate not graded EXACTLY at its band
          fails; the slot's band never changes). On ACCEPT final_band == difficulty_plan[q] (the frozen
          placement, S0-OP-3); persist
          batch_state['difficulty_plan'] (and batch_state['difficulty_state']) in the
          same write.
          PRECEDENCE (one rule): the independent rating and the content floor
          DECIDE the band (final_band). difficulty_obs is the author's count of
          the item's derivation load; where it disagrees with final_band the
          COUNTS are re-done from the written solution (never the label bent to
          the counts) BEFORE THE GATE below runs — so THE GATE checks the
          corrected obs against final_band, and its REJECT path is reached only
          when the written item itself does not support final_band.
          RECORD on the item (write_q_to_sidecar -> concept_map -> registry
          question_index): difficulty_check = {'scheduled', 'rated', 'rationale',
          'ccp_status', 'ccp_composite', 'decision', 'final_band', 'judge_input_sha256',
          'level_status' (b1: lc['status']; b2: None), 'level_note' (optional),
          'measured', 'measured_source' (v5.94), 'dl_rung' (v5.94, when a DL rung ran)}; the
          item's difficulty label IS final_band. A level item's difficulty_obs additionally
          carries level, level_vector, closeness and reagents_seen, and its quality record
          ask_format (v5.92; read by A-LEVEL / A-CLOSENESS / A-AXIS2 — WARN-only — and
          Step 9 §7A-M). Auditor gate
          A-CONTENTLEVEL verifies the record is resolved.
        THE GATE (v5.96, LABEL-BASIS-LAW): ok, measured, basis = bc.verify_difficulty_label(
        {'difficulty': difficulty_plan[q], 'difficulty_obs': difficulty_obs, 'qtype': qtype,
         'difficulty_check': <the item's recorded difficulty_check, when it has one>},
        difficulty_labels) — the ONE label verifier (A-QINDEX check 8 and notes_core call it too;
        a recorded basis decides for an item that carries one (v6.0: measured_exact / last_resort; a
        legacy SWAP / FORCED / HELD row of an earlier paper still verifies); else a BINDING organic ruler band, else
        the recorded evidence). A NEW candidate carries no basis. If not ok:
          → REJECT. Regenerate TOWARD the band using the profile (add or remove
            derivation load; change class facets). Bound: MAX_DIFF_TRIES = 6
            per slot, counted separately from MAX_SCENARIO_TRIES. v5.92 (owner
            D3-R5): the brief ESCALATES with each try toward a Hard slot — try 2
            a larger / more constrained substrate or stimulus, try 3 closer
            distractors (the wrong options differ from the key by one decision),
            try 4+ the next harder exemplar of the same cell as the model; a
            Medium / Easy slot that measured above is simplified the same way in
            reverse. There is ONE budget: every reason to retry (rubric, level
            model, judge disagreement — D11) spends from the same 6.
          → v6.0: NO BAND-SWAP ESCAPE (RETIRED — S0-OP-3: the placement is frozen; no step swaps, carries,
            holds, forces or relabels a position; bc.dl_target_plan_swap is legacy-only). After MAX_DIFF_TRIES the slot
            enters the REPAIR LADDER (§Q8b-LADDER) with reason 'harder'/'easier' —
            v5.94: reason 'easier' (measured BELOW) is the DL repair above and ends in
            CARRY TO REVIEW, never in R5; the ladder below runs
            for 'harder' and for every non-difficulty reason:
            R2 (regenerate, same subtopic/band/ask type) -> R3 (next under-target
            ask type) -> R4/R4' (terminal) -> R5 (v6.0, owner 2026-11-10 — LAW-ORG-3 / LAW-ORG-5: the
            requested schedule is delivered EXACTLY and a label is never held, swapped or forced): a
            candidate that does not grade EXACTLY at its band (S0-OP-5 C4 + C5) is a FAILED candidate —
            the next of the bc.k_candidates() candidates is tried; when every candidate of the slot has
            failed, the slot is CARRIED to S13-2L (record difficulty_check.decision = 'carried' on the kept item —
            the strict audit reads it as S13-2L's work, never as an RL relabel), whose SC2 difficulty chain owns it (rework, replace,
            shape, sibling, reserve_refill, refill_session, bounded last_resort). The blueprint is never
            amended for a difficulty reason; batch_state['difficulty_schedule_original'] is untouched
            (A-PYQBENCH prints original vs final counts from difficulty_state.schedule_original, DL-51).
            [Legacy v5.96 text — a HELD label written by bc.dl_set_label_basis(entry, 'held', ...) — is
            RETIRED for every paper produced by this release; held rows of earlier papers still verify.]
        On ACCEPT: pass difficulty=final_band (== difficulty_plan[q], kept in
        step by the frozen placement — v6.0: no band swap, no R5 relabel), difficulty_obs AND
        difficulty_check to write_q_to_sidecar — the label and its evidence travel together into
        registry.question_index (S13-4) and are what A-QINDEX checks 7/8 and
        Step 9's advisory re-measure (TestExplain §7A-M) verify downstream.

        THE GATE, executable (called once per slot when difficulty_plan is set;
        `diff_tries` is the batch_state.json['_diff_tries'] dict, persisted with
        the rest of the S3 state):
        ```python
        # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
        def g_diff_gate(q, band, qtype, difficulty_obs, difficulty_labels,
                        diff_tries, level_status=None, rated_band=None):
            """Returns 'ACCEPT' | 'RETRY' | 'SWAP_OR_LADDER' for this candidate.
            v5.92 (DL-39): called ONLY when difficulty_plan is set — a dormant plan
            never reaches this gate (its tamper stop would otherwise fire).
            level_status / rated_band (v5.92, owner D11 (A)): for a LEVEL item whose
            level record agrees with a TOP-band slot while the independent judge rates
            it below, ONE extra RETRY is spent from this same budget."""
            import blueprint_core as bc          # S1-2b engine (already on sys.path)
            MAX_DIFF_TRIES = bc.MAX_DIFF_TRIES_DEFAULT      # 6 — the ONE budget (v5.92)
            profile = bc.difficulty_authoring_profile(band, qtype,
                                                      difficulty_labels,
                                                      rule=bc.RUBRIC_RULE_CURRENT)
            # profile is None ONLY for a bottom-band MSQ/NAT slot, which the S3
            # plan can never produce (floors) — None here means the plan was
            # modified outside bc.assign_difficulty_bands: a tamper HARD STOP [HS:INFRA],
            # never a skip.
            if profile is None:
                raise SystemExit(f"HARD STOP [HS:INFRA] (G-DIFF, v5.60): no authoring "
                                 f"profile for band {band!r} at Q{q} ({qtype}) "
                                 f"— rebuild the difficulty_plan.")
            # (the candidate was authored INSIDE `profile`, its answer derived,
            #  and difficulty_obs recorded from that derivation — shape above)
            ok_d, measured, _basis_d = bc.verify_difficulty_label(       # v5.96: the ONE label verifier
                {'difficulty': band, 'difficulty_obs': difficulty_obs,
                 'qtype': difficulty_obs.get('qtype') if isinstance(difficulty_obs, dict) else None},
                difficulty_labels)
            if ok_d:
                rl = bc.reconcile_level(band, level_status, rated_band, difficulty_labels,
                                        diff_tries.get(str(q), 0), max_tries=MAX_DIFF_TRIES)
                if rl.get('retry') and not diff_tries.get(f'{q}:d11'):
                    # D11 (A): judge below an agreed Hard — exactly ONE extra try, from the same
                    # budget; the marker makes the second pass ACCEPT (level_note 'judge below level')
                    diff_tries[f'{q}:d11'] = 1
                    diff_tries[str(q)] = diff_tries.get(str(q), 0) + 1
                    return 'RETRY'
                return 'ACCEPT'     # v5.94: the COUNTS support the band; THE MEASURED BAND decides
                                    # (a judge / ruler below the slot -> DL repair, then carry-to-review)
            diff_tries[str(q)] = diff_tries.get(str(q), 0) + 1
            if diff_tries[str(q)] < MAX_DIFF_TRIES:
                return 'RETRY'          # regenerate toward `band`, per profile['note']
            return 'SWAP_OR_LADDER'     # v6.0: NO swap (retired) — BELOW -> carry to review, ABOVE -> ladder (rules above)
        ```

      Only when CHECK 1, 1b, 2, 3 all PASS:
        ACCEPT the question.
        mock_scenario_ledger.add(candidate.scenario_key)
        if candidate is CLASS 2/3:
            mock_presentation_ledger.add((candidate.concept_group,
                                          candidate.presentation_key))
        subtopic_generated_count += 1

      Continue until subtopic_generated_count == N (RULE A satisfied).

  SAFE REGENERATION BOUND (prevents infinite code loops only):
    Bound regeneration attempts per slot at MAX_SCENARIO_TRIES = 12.
    Because scenario supply is effectively infinite, this bound is never
    expected to be reached. If it ever is, ESCALATE: deliberately broaden the
    scenario space (pick a structurally different sub-mechanic of the subtopic)
    and continue. EVEN THEN: never reduce N, never reuse a scenario_key.
    Hitting the bound is a generator-effort signal, NOT a licence to repeat.

  CROSS-SUBTOPIC COLLISIONS (mock-global uniqueness):
    scenario_key uniqueness is mock-GLOBAL, not per-subtopic. If two different
    subtopics would produce the same scenario_key (e.g. a percentage operation
    reachable from both "Percentage" and "Profit & Loss"), the second is a
    CHECK-1 collision → regenerate the second on a different scenario. A student
    must never meet effectively the same task under two different subtopic labels.

  RELATIONSHIP TO blueprint.json vs blueprint.xlsx:
    Per-subtopic counts are read from blueprint.json subtopic_allocations[].q_count
    (see S3-2). blueprint.xlsx is a human-readable companion only — Step 7 NEVER
    parses the .xlsx; blueprint.json is the single machine source for counts.

  THIS SUPERSEDES any softer "max_per_paper" reading:
    - count of questions for a subtopic in a mock = EXACTLY blueprint q_count (N).
    - count of any single scenario_key in a mock = EXACTLY 1 (hard zero for 2+).

## S6-9 — Cross-mock variant rotation (v4.4 — exam-agnostic; config-driven)

  v4.4 CHANGE: This section no longer hardcodes any subtopic name, pair, or
  parity table. It carries NO mutual-exclusion HARD STOP [HS:PROSE]. It mirrors S3-17's
  contract: read structured policy from config (manifest + section_rules) by
  subtopic_id; if the config declares nothing, this is a no-op (never a stop).

  READ FROM batch_state.json rotation_state{} — not from memory.

  ── A. MUTUAL EXCLUSION (members must NOT co-occur in one mock) ──
    NOT enforced here. This invariant is owned SOLELY by S3-17, which reads
    manifest.alternation_groups by subtopic_id BEFORE generation and HARD STOP [HS:INPUT]s
    if any group has >1 member allocated to the mock (HS-12). The post-generation
    audit backstop is G-ALTGROUP (S12-NEW-6). S6-9 holds no pair list and never
    re-checks this — duplicating it with hardcoded names is exactly the v3.4
    half-migration defect that v4.4 closes.
    NB: manifest.alternation_groups encodes mutual exclusion only; the parity
    ASSIGNMENT (which member appears in which mock) is a Step-1 blueprint
    ALLOCATION concern. Step 7 trusts the allocation it is handed and only
    verifies the invariant; it does not re-derive a parity schedule.

  ── B. CROSS-MOCK VARIANT ROTATION (no two consecutive mocks reuse a variant) ──
    For a subtopic that has interchangeable surface VARIANTS across mocks
    (e.g. cipher families for a coding subtopic, sub-types for a relations
    subtopic, series-variant for a number-series subtopic), Step 0 MAY author an
    OPTIONAL per-subtopic directive in section_rules.md inside that subtopic's
    block (parsed via S7-0):

        ROTATION: <variant_a> | <variant_b> | <variant_c> | ...
        ROTATION_BAN: <variant>            (optional; never permit this variant)

    Read these by subtopic_id into:
        rotation_cycles  = {subtopic_id: [variant, ...]}   # from ROTATION:
        rotation_bans    = {subtopic_id: {variant, ...}}    # from ROTATION_BAN:

    For each subtopic_id allocated in THIS mock that declares a cycle, pick the
    next variant (skipping any banned variant and the variant used in the
    previous mock), then persist it:

    ```python
    # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
    def rotation_pick(sid, rotation_cycles, rotation_bans, rotation_state):
        cycle = [v for v in rotation_cycles.get(sid, [])
                 if v not in rotation_bans.get(sid, set())]
        if not cycle:
            return None                      # no cycle declared → no constraint
        last = rotation_state.get(sid)
        choice = next((v for v in cycle if v != last), cycle[0])
        rotation_state[sid] = choice
        return choice
    ```

    A subtopic that declares NO ROTATION cycle has no rotation constraint (no-op).
    With section_rules carrying no ROTATION directives at all, S6-9 is a vacuous
    no-op and NEVER hard-stops — so an unconfigured policy can never block a run.
    (Intra-mock presentation variety remains owned by the §6-3c RULE C /
    presentation_key machinery; this section is the orthogonal CROSS-mock axis.)


# ════════════════════════════════════════════════════════════════════════
# §7 — QUESTION GENERATION ENGINE
# ════════════════════════════════════════════════════════════════════════

## S7-0 — section_rules.md parsing protocol (v1.0 — unchanged)

  Locate '--- Subtopic: [re.escape(S)] ---'
  Stop at next '--- Subtopic:' or '=== SECTION:'

## S7-1 through S7-31 — (see full v1.0 for all rules)

  Core additions/fixes in v2.0:

## S7-CONCEPT — Per-subtopic generation with scenario + presentation uniqueness (DOUBT-3 v3.3 / DOUBT-4 v3.8)

  This is the generation-time half of S6-3b/S6-3c. It runs for EVERY subtopic in
  EVERY section. It guarantees ALL rules simultaneously:
    RULE A: exactly N questions (blueprint q_count) per subtopic.
    RULE B: every question mock-wide has a distinct scenario_key.
    RULE C: CLASS 2/3 questions sharing a CONCEPT_GROUP have distinct
            presentation_key, with ≥2 stem_format_variants when N≥3 (v3.8).

```python
# ── NAME BINDINGS (v5.62), part 2: MODEL-AGENCY STUBS ────────────────────────
# The six judgment operations the generator loop consumes, previously read but
# bound NOWHERE (GRANDFATHERED_MUST_FIX). Each is judgment the model performs
# over data already in context — no tool call anywhere, so every stub is
# CLASS J, and C6 permits python consumption of a J result (it degrades
# gracefully: the model reads the spec as a reasoning task and produces the
# value). This fence is column-0 ON PURPOSE: C6-PRE requires any fence carrying
# a model-agency marker to parse RAW, and an indented body never does.

def derive_scenario_from_pattern(pattern):
    """Map ONE observed Step-5 pattern to this spec's scenario unit:
    (cognitive_operation, structural_shape) — 'what the student DOES' plus
    'the scenario structure', value-free (the RULE B derivation contract).
    The pattern carries template/approach TEXT (that is all Step 5 emits);
    naming the pair from that text is judgment, not a dict lookup."""
    pass  # CLASS: J — judgment over pattern['template'] / pattern['approach'] already in context; no tool call.

def build_question(subtopic_data, op, shape, section, **axes):
    """Author ONE candidate question for (op, shape), honouring every axis in
    `axes`: stem_format_variant, distractor_strategy, answer_cardinality,
    prefer_negative (soft, v5.14), reuse (v5.22). MUST actually RENDER the
    requested presentation (RENDER-CONSISTENCY, v3.9 G4) and populate the
    v4.5 answer contract (correct_set / has_aota_option for 'multi';
    nat_value for NAT). Returns the candidate object the CHECK loop vets."""
    pass  # CLASS: J — question authoring is model generation over section_rules + the §6-3c menus; no tool call.

def cross_mock_duplicate(candidate, registry_snapshot, l1_only=False):
    """CHECK 2 — is this candidate a repeat of a PRIOR mock's question?
    L1: verbatim/near-verbatim (Jaccard >= 0.75 on stem tokens, or MD5
    match). L2: matching semantic tuple. l1_only=True (the controlled-reuse
    path) keeps the L1 verbatim ban while bypassing L2 BY DESIGN — a fresh
    surface of a known item is the point there."""
    pass  # CLASS: J — judgment over the candidate + registry_snapshot already in context; the thresholds above are the contract.

def passes_quality_gates(candidate, subtopic_data, section):
    """CHECK 3 — ALL of: difficulty floor + G-DIFF band conformance (v5.60),
    banned patterns, 3-pass verify, option quality,
    verify_presentation_match() (v3.9 G4) and verify_answer() (R-ANSWER,
    v4.5/v4.7). Any failure -> False -> the caller regenerates."""
    pass  # CLASS: J — aggregate judgment; every sub-gate is specified in §7 / S7-NEW-A and applied by the model.

def invent_distinct_scenario(subtopic_data):
    """SOURCE 2 — invent ONE genuinely new (cognitive_operation,
    structural_shape) beyond the observed seed set: fits the subtopic,
    matches the slot's difficulty calibration, obeys every quality gate and
    banned-pattern rule. Supply is unlimited — the PYQ pattern list is a
    SEED, never a CEILING."""
    pass  # CLASS: J — model invention from domain knowledge; no tool call.

def widen_scenario_space(subtopic_data, exhausted_source):
    """Return a REPLACEMENT scenario iterator over a genuinely WIDER space —
    new operations/shapes the exhausted iterator never yielded. Never
    re-yields a scenario_key already used this paper (CHECK 1 still vets
    every candidate downstream)."""
    pass  # CLASS: J — model invention; the retry loop consumes the result as an iterator.
```

  ```python
  # mock_scenario_ledger / mock_presentation_ledger are bound at SESSION START
  # in S3-1 (idempotent init; S4-12 rehydrates on resume) — bound once, read
  # everywhere, so the two inits cannot drift apart.
  MAX_SCENARIO_TRIES = 12   # safe bound only; supply is effectively infinite
  _WIDEN_EXHAUST     = 3     # B (v5.22): fruitless widenings for a narrow-FACTUAL subtopic
                            #   before its bounded (item × angle) universe is treated as drained
                            #   (decision c — empirical). Generative subtopics widen without limit.
  SPACING_GAP        = 8     # B: cumulative cross-tier spacing (papers) before an item may recur.

  # ── NAME BINDINGS (v5.62), part 1: REAL python ──────────────────────────────
  # canonical / flag / weighted_patterns were READ by generate_subtopic /
  # controlled_reuse / pick_presentation / scenario_iterator and bound NOWHERE
  # (GRANDFATHERED_MUST_FIX). They are DETERMINISTIC operations whose
  # session-to-session drift would corrupt state persisted in batch_state.json /
  # the registry (ledger keys, seed ordering, diagnostics), so they are real
  # python here. The seven JUDGMENT names those same loops read are declared as
  # tagged model-agency stubs in the column-0 fence BEFORE this one — this fence
  # is indented and must stay free of model-agency markers (C6-PRE requires any
  # fence carrying one to parse RAW, and an indented body never does).

  def canonical(s):
      """Deterministic key normaliser (the RULE B/C NORMALISATION contract:
      lowercase, snake_case, strip) — applied PER '|' SEGMENT so
      'Find Time | two pipes' and 'find_time|two_pipes' collide, exactly as
      the ban requires. Keys built here persist across sessions
      (batch_state.json concept_ledger / presentation_ledger), so this MUST
      be real python: a model-judged normalisation could drift between
      sessions and silently blind RULE B / RULE C to an earlier batch."""
      parts = [re.sub(r'[^a-z0-9]+', '_', p.strip().lower()).strip('_')
               for p in str(s).split('|')]
      return '|'.join(parts)

  # Non-fatal diagnostic helper — BYTE-IDENTICAL to Framework_ScopedBlueprint.md's
  # (same name, same body, so XSPEC-DRIFT stays silent by identity, not exemption).
  _FLAGS = []
  def flag(msg):
      _FLAGS.append(str(msg))
      print(f"[FLAG] {msg}")

  def weighted_patterns(patterns):
      """SOURCE-1 seed ordering (S7-2): most common observed pattern first.

      Sorts on the fields Step 5 ACTUALLY emits per pattern entry
      (analyse_engine subtopic entry: frequency %, raw_count, confidence,
      deprecated) — the previous contract read pk['operation'] /
      pk['structural_shape'], two fields NO producer in the corpus has ever
      written (see scenario_iterator, which now derives that pair from the
      pattern instead of pretending it is stored). Skips entries carrying no
      usable observed pattern: deprecated ones and the zero-PYQ placeholder
      (confidence == 'absent'). Deterministic: equal weights preserve the
      producer's emission order (sorted() is stable)."""
      usable = [p for p in (patterns or [])
                if not p.get('deprecated') and p.get('confidence') != 'absent']
      return sorted(usable,
                    key=lambda p: (-float(p.get('frequency', 0) or 0),
                                   -int(p.get('raw_count', 0) or 0)))

  def generate_subtopic(subtopic_data, N, section, registry_snapshot, axis2_tracker=None):
      """
      Produce EXACTLY N questions for this subtopic, each a distinct scenario AND
      (for CLASS 2/3) a distinct presentation. N is floor AND ceiling.
      v5.14: axis2_tracker (or None when inert) steers the flexible Axis-2 class toward the
      window target; ZP subtopics are routed as format-elastic fillers (decision 11).
      """
      cg     = subtopic_data['CONCEPT_GROUP']
      sclass = subtopic_data['SUBTOPIC_CLASS']     # CLASS1..CLASS4 (S6-3b classify)
      # v5.14: presentation (stem_format_variant) is chosen for CLASS 2/3 as before, AND for
      # ZP subtopics WHEN the Axis-2 feature is active (tracker present) — as format-elastic
      # fillers (decision 11). When the feature is inert (tracker None), ZP behaves EXACTLY as
      # v5.13 (no presentation). CLASS1 non-ZP and CLASS4 (LINKED) always keep their behaviour.
      do_presentation = (sclass in ('CLASS2', 'CLASS3')
                         or (subtopic_data.get('is_zp', False) and axis2_tracker is not None))
      produced = []
      used_formats_for_cg = set()                  # for RULE C2 (≥2 formats if N≥3)
      _widen_count = {}                            # B (v5.22): per-cg fruitless-widen counter

      scenario_source = scenario_iterator(subtopic_data)  # SOURCE 1 then SOURCE 2

      while len(produced) < N:                 # RULE A: loop until exactly N
          accepted = None
          for _try in range(MAX_SCENARIO_TRIES):
              op, shape = next(scenario_source)         # next distinct scenario
              scenario_key = canonical(op + "|" + shape)
              if scenario_key in mock_scenario_ledger:  # CHECK 1 (RULE B)
                  continue

              # v3.8 — choose a PRESENTATION for CLASS 2/3 (RULE C). Pick a
              # (stem_format_variant, distractor_strategy) pair from the §6-3c
              # menus that is NOT yet used for this concept_group, and that helps
              # satisfy C2 (force a new format if N≥3 and only 1 format so far).
              fmt = dstr = presentation_key = None
              if do_presentation:
                  # v5.14: target-aware among RULE-C-valid variants (RULE C WINS — only
                  # unique presentations are considered; the tracker only re-orders them).
                  fmt, dstr = pick_presentation(subtopic_data, cg,
                                                used_formats_for_cg,
                                                remaining=N - len(produced),
                                                tracker=axis2_tracker)
                  presentation_key = f"{fmt}|{dstr}"
                  if (cg, presentation_key) in mock_presentation_ledger:  # CHECK 1b
                      continue                          # try another presentation
                                                        # (or another scenario)

              # v4.5: resolve answer_cardinality for this subtopic from the blueprint
              # subtopic_list (whole-subtopic mode; default 'single'). Threaded into the
              # candidate so build_question renders the MSQ instruction line, verify_answer
              # runs the correct R-ANSWER branch, and write_q_to_sidecar stores the set +
              # flags. For 'multi', build_question must populate candidate.correct_set
              # (the intended set S) and candidate.has_aota_option, and obey the k-bound /
              # R-MSQ-ESCAPE. Inert ('single') when blueprint multi_present is false.
              # v5.X POSITION-BASED OVERRIDE (GAP-2026-07-22-001 §6): when the exam has
              # position-based typing (_position_based_typing True), derive answer_cardinality
              # and answer_type from the Q POSITION's marking_scheme entry, not from the
              # per-subtopic value. This ensures the same subtopic generates MCQ in Section A,
              # MSQ in Section B, NAT in Section C (e.g. IIT JAM).
              answer_cardinality, _answer_type = _resolve_answer_axes(
                  qnum, subtopic_data.get('subtopic_id'))
              if _position_based_typing:
                  subtopic_data['answer_type'] = _answer_type
              candidate = build_question(subtopic_data, op, shape, section,
                                         stem_format_variant=fmt,
                                         distractor_strategy=dstr,
                                         answer_cardinality=answer_cardinality,
                                         prefer_negative=axis2_want_negative(axis2_tracker))
              candidate.answer_cardinality = answer_cardinality

              if cross_mock_duplicate(candidate, registry_snapshot):   # CHECK 2 (L1+L2)
                  continue                                 # (B: same fn supports l1_only=True —
                                                           #  the reuse path uses it to keep L1
                                                           #  verbatim blocking while bypassing L2)
              if not passes_quality_gates(candidate, subtopic_data, section):  # CHECK 3
                  continue                                 # includes verify_answer (R-ANSWER)

              accepted = candidate
              accepted.scenario_key       = scenario_key
              accepted.subtopic_class     = sclass
              accepted.stem_format_variant= fmt
              accepted.distractor_strategy= dstr
              accepted.presentation_key   = presentation_key
              break

          if accepted is None:
              # B (v5.22): the bound was hit with no NEW distinct (item × angle). For a
              # GENERATIVE subtopic (supply effectively infinite) this is a generator-effort
              # signal → widen and keep trying (UNCHANGED behaviour; the mock path only ever
              # takes this branch). For a genuinely narrow-FACTUAL subtopic that has drained its
              # bounded (item × angle) universe (decision b: C-FACTUAL classification, gated by
              # decision c: repeated fruitless widening), take the CONTROLLED-REUSE valve.
              _widen_count[cg] = _widen_count.get(cg, 0) + 1
              if _is_narrow_factual(subtopic_data) and _widen_count[cg] >= _WIDEN_EXHAUST:
                  _pidx = globals().get('paper_index', N)          # C2 session identity (== N for a mock)
                  _pid  = globals().get('paper_id', f"MOCK:M{N:02d}")
                  reused = controlled_reuse(subtopic_data, registry_snapshot, _pidx,
                                            mock_scenario_ledger, do_presentation, cg,
                                            used_formats_for_cg, N - len(produced))
                  if reused is not None:
                      accepted = reused                            # fresh-surface, ≥8-back item;
                      mark_subtopic_exhausted(subtopic_data, _pid)  # sticky, cross-tier
                  else:
                      scenario_source = widen_scenario_space(subtopic_data, scenario_source)
                      continue
              else:
                  scenario_source = widen_scenario_space(subtopic_data, scenario_source)
                  continue                                  # never decrement N

          produced.append(accepted)
          mock_scenario_ledger.add(accepted.scenario_key)
          if do_presentation:
              mock_presentation_ledger.add((cg, accepted.presentation_key))
              used_formats_for_cg.add(accepted.stem_format_variant)
          # B (v5.22): record this (item × angle) usage in a SEPARATE additive field tagged with
          # the paper_index — so a later paper can measure the cross-tier spacing gap. The existing
          # semantic_tuples list (the L2 dedup unit) is left EXACTLY as-is (bare tuples), so L2
          # matching is byte-unchanged; semantic_usage is read only by B's controlled_reuse.
          pending_registry.setdefault('semantic_usage', []).append(
              {'subtopic_id': subtopic_data['subtopic_id'],
               'angle': accepted.scenario_key,
               'values': getattr(accepted, 'sorted_values', ''),
               'paper_index': globals().get('paper_index', N)})
          # v5.14: record this question's Axis-2 class + negativity into the WINDOW tracker.
          # LINKED for CLASS4 (stimulus-locked), the variant's class when one was chosen,
          # else DIRECT. axis2_need()==0 for DIRECT/LINKED so this never mis-steers; it keeps
          # the window counts (and the negative rate) accurate for audit.py's audit.
          _ax2 = (STEM_FORMAT_TO_AXIS2.get(accepted.stem_format_variant, 'DIRECT')
                  if accepted.stem_format_variant
                  else ('LINKED' if sclass == 'CLASS4' else 'DIRECT'))
          axis2_record(axis2_tracker, _ax2, bool(getattr(accepted, 'is_negative', False)))

      # RULE C2 final guard: if N≥3 and only one format was used, the loop above
      # should have forced variety via pick_presentation(); assert it held.
      if sclass in ('CLASS2','CLASS3') and N >= 3:
          assert len({q.stem_format_variant for q in produced}) >= 2, \
              "RULE C2 violated — diversify stem_format_variant"
      assert len(produced) == N, "RULE A violated — must never happen"
      return produced

  # ── B (v5.22): NARROW-FACTUAL EXHAUSTION + CONTROLLED REUSE ────────────────────
  # Dormant for generative subtopics and for mocks (which never drain a bounded universe);
  # the mock path is bit-identical. Active only for a C-FACTUAL subtopic whose finite
  # (item × angle) universe genuinely drains under a dense (e.g. scoped) series.
  def _is_narrow_factual(subtopic_data):
      """decision (b): questions are bounded FACTUAL recall → finite (item × angle) universe.
      From the Step-5 question_mechanic (C-FACTUAL family); never fabricated. Generative
      subtopics (CI, syllogism, …) return False and keep the strict never-reuse path."""
      mech = str(subtopic_data.get('question_mechanic', '')).lower()
      return any(k in mech for k in ('factual', 'recall', 'static_gk', 'current_affairs', 'fact'))

  def mark_subtopic_exhausted(subtopic_data, paper_id):
      """Sticky, cross-tier flag → pending_registry (committed at Final Assembly). Once set it
      NEVER clears: a subtopic drained in a mock stays drained for every scoped tier, and back."""
      ex = pending_registry.setdefault('exhausted_subtopics', {})
      ex.setdefault(subtopic_data['subtopic_id'], {'exhausted': True, 'since_paper': paper_id})

  # semantic_usage entries: {'subtopic_id': sid, 'angle': scenario_key, 'values': sorted_values,
  # 'paper_index': k}. A SEPARATE additive log (semantic_tuples/L2 stays bare + unchanged).
  def controlled_reuse(subtopic_data, registry_snapshot, paper_index,
                       scenario_ledger, do_presentation, cg, used_formats, remaining):
      """Build a fresh-SURFACE question reusing a prior (item × angle) for this exhausted
      narrow-factual subtopic, chosen so the reuse is safe:
        • spacing-{SPACING_GAP}: the item's LAST use is ≥ SPACING_GAP papers back (cross-tier).
          If none qualifies (dense series) → decision (b): least-recent + WARN (never hard-stop).
        • new angle: a scenario_key NOT already used THIS paper (CHECK 1 still holds).
        • never verbatim: the L1 (Jaccard/MD5) ban STILL applies; C-FACTUAL still web-verifies.
      Returns an accepted candidate, or None (→ caller widens again)."""
      sid  = subtopic_data['subtopic_id']
      uses = subtopic_usage(registry_snapshot, sid)   # D (v5.23): O(shard) via subtopic index
      if not uses:
          return None
      _pidx = lambda u: u.get('paper_index', -10**9)
      eligible = [u for u in uses if paper_index - _pidx(u) >= SPACING_GAP]
      if eligible:
          pool = sorted(eligible, key=_pidx)                    # oldest first
      else:
          pool = sorted(uses, key=_pidx)                        # decision (b): least-recent + WARN
          flag(f"B: subtopic {sid} exhausted and spacing-{SPACING_GAP} unsatisfiable in a dense "
               f"series — reusing the least-recent item with a fresh angle (never verbatim). WARN.")
      for u in pool:
          op, shape = u.get('angle', ''), u.get('values', '')
          scenario_key = canonical(op + "|" + shape)
          if scenario_key in scenario_ledger:                   # CHECK 1 (this paper) still holds
              continue
          fmt = dstr = presentation_key = None
          if do_presentation:
              fmt, dstr = pick_presentation(subtopic_data, cg, used_formats, remaining)
              presentation_key = f"{fmt}|{dstr}"
              if (cg, presentation_key) in mock_presentation_ledger:
                  continue
          cand = build_question(subtopic_data, op, shape, None,
                                stem_format_variant=fmt, distractor_strategy=dstr,
                                answer_cardinality=subtopic_data.get('answer_cardinality', 'single'),
                                reuse=True)                       # a FRESH surface of a known item
          if cross_mock_duplicate(cand, registry_snapshot, l1_only=True):   # L1 verbatim STILL blocks
              continue                                            # (L2 is bypassed BY DESIGN here)
          if not passes_quality_gates(cand, subtopic_data, None):
              continue
          cand.scenario_key        = scenario_key
          cand.stem_format_variant = fmt
          cand.distractor_strategy = dstr
          cand.presentation_key    = presentation_key
          cand.subtopic_class      = subtopic_data['SUBTOPIC_CLASS']
          return cand
      return None

  def pick_presentation(subtopic_data, cg, used_formats, remaining, tracker=None):
      """Return a (stem_format_variant, distractor_strategy) pair from the §6-3c
      menus for this subtopic's family. Prefer an UNUSED format for the cg; if
      remaining slots == 1 and only one format used so far, FORCE a second format
      (RULE C2). Distractor strategy is rotated so presentation_key stays unique.
      v5.14 THREE-AXIS: when `tracker` is provided, the candidate set is capability-bounded
      (axis2_candidate_variants), and among the RULE-C-valid (unused) variants the one whose
      Axis-2 class the WINDOW still needs is preferred. RULE C WINS — steering only re-orders
      the already-unique candidates; it never picks a used variant (decision (b))."""
      base = format_menu_for(subtopic_data)        # §6-3c stem_format_variant menu (family)
      fmts = axis2_candidate_variants(subtopic_data, base) if tracker is not None else base
      dstrs = distractor_menu_for(subtopic_data)   # §6-3c distractor_strategy menu
      # RULE C: valid = variants NOT yet used for this concept_group (uniqueness). Steering
      # (if any) is a STABLE re-ordering WITHIN this valid set, so a used variant is never chosen.
      unused = [f for f in fmts if f not in used_formats]
      if tracker is not None and unused:
          unused = sorted(unused,   # stable: equal-need keeps family/menu order (RULE-C rotation)
                          key=lambda f: -axis2_need(tracker, STEM_FORMAT_TO_AXIS2.get(f, 'DIRECT')))
      fmt = (unused[0] if unused else fmts[0])
      if remaining == 1 and len(used_formats) < 2:
          fmt = (unused[0] if unused else fmt)
      # rotate distractor strategy to keep (fmt|dstr) unique within the cg
      for d in dstrs:
          if (cg, f"{fmt}|{d}") not in mock_presentation_ledger:
              return fmt, d
      # all (fmt|*) taken → switch format. Search UNUSED-FIRST (target-ordered when steering),
      # then the remaining (used) formats, so a unique (format|distractor) pair is found if one
      # exists ANYWHERE — preserving v5.13 completeness (never emit a duplicate presentation_key).
      search_order = list(unused) + [f for f in fmts if f not in unused]
      for f in search_order:
          for d in dstrs:
              if (cg, f"{f}|{d}") not in mock_presentation_ledger:
                  return f, d
      return fmt, dstrs[0]   # menus large enough that this is never reached for real N

  def scenario_iterator(subtopic_data):
      # v5.62 — a Step-5 pattern entry carries {template, approach, frequency,
      # raw_count, confidence, deprecated, ...} and has NEVER carried
      # 'operation'/'structural_shape'; reading those keys was a guaranteed
      # KeyError against every section_rules.md the estate has ever produced.
      # The (operation, shape) pair is DERIVED from the pattern's text — a
      # judgment operation, declared in the tagged column-0 fence above.
      for pk in weighted_patterns(subtopic_data['PYQ_STEM_PATTERNS']):
          yield derive_scenario_from_pattern(pk)
      while True:
          yield invent_distinct_scenario(subtopic_data)  # NO upper limit
  ```

  CALLER CONTRACT (hard rules — never violated):
    1. A scenario collision (CHECK 1) or presentation collision (CHECK 1b) NEVER
       ends a subtopic early. It triggers regeneration on a DIFFERENT scenario /
       presentation. The loop continues until exactly N questions exist, each
       distinct on scenario_key AND (CLASS 2/3) presentation_key.
    2. "Not enough observed patterns/formats for N" is NEVER a reason to stop.
       Invent additional distinct scenarios (SOURCE 2) and rotate the §6-3c
       presentation menus — supply is unlimited.
    3. NEVER change values/wording and re-submit the SAME scenario_key, and NEVER
       re-use a (concept_group, presentation_key) pair, to fill a slot.
    4. Persist mock_scenario_ledger AND mock_presentation_ledger to batch_state.json
       after each batch, so a resumed session (S4-12) cannot reuse an earlier
       scenario or presentation.

  RENDER-CONSISTENCY CONTRACT (v3.9 G4 — the label must match the question):
    build_question(subtopic_data, op, shape, section, stem_format_variant=fmt,
    distractor_strategy=dstr) MUST actually RENDER the requested presentation —
    not merely tag it. Specifically:
      · the produced STEM must structurally match stem_format_variant
        (e.g. 'sentence_embedded_underlined' → the target word appears underlined
         inside a sentence, NOT as an isolated headword, and — v4.1 — as a GENUINE
         underlined run, NOT a "(underlined: X)" parenthetical annotation);
      · the produced OPTIONS must be built by the requested distractor_strategy
        (e.g. 'same_semantic_field' → distractors drawn from the target's semantic
         field, NOT three near-synonyms of the headword).
    v5.14 SOFT PARAM — build_question also accepts prefer_negative=<bool> (default False,
    decision 12): a NUDGE toward a negative-polarity stem (NOT/EXCEPT/INCORRECT) when the
    section's window is below its negative_rate. BEST-EFFORT ONLY — honour it when the chosen
    stem_format_variant and content naturally support negation; otherwise ignore it. It NEVER
    forces an unnatural or invalid negative, never overrides correctness, and is never a gate.
    The actually-rendered is_negative (not the hint) is what the window tracker records.
    CHECK 3 (passes_quality_gates) therefore includes verify_presentation_match():
      def verify_presentation_match(candidate):
          # returns False if the rendered stem/options do not match the declared
          # stem_format_variant / distractor_strategy. A mismatch means the
          # presentation_key is cosmetic — REJECT and regenerate.
          ok = (stem_matches_format(candidate.stem, candidate.stem_format_variant)
                and options_match_strategy(candidate.options,
                                           candidate.distractor_strategy))
          # v4.1 — underline render must be REAL, not a text annotation:
          if candidate.stem_format_variant == 'sentence_embedded_underlined':
              ok = ok and has_underlined_span(candidate.block) \
                       and "(underlin" not in candidate.stem.lower()
          return ok
      # stem_matches_format() for 'sentence_embedded_underlined' now delegates the
      # underline check to has_underlined_span (S10-2 / S12-NEW-14): mere textual
      # presence of the target word — which the banned "(underlined: X)" annotation
      # satisfies — is NO LONGER sufficient. The candidate must carry a real <w:u>
      # run, or CHECK 3 fails and the question regenerates via add_stem_with_underline.

      # v4.5 — ANSWER CONTRACT (R-ANSWER, generalises v4.2 R-UNIQUE). CHECK 3 runs:
      def verify_answer(candidate):
          # v4.7: the answer_type axis is checked FIRST and SUPERSEDES cardinality — a NAT
          # question has no options, so the option-defensibility logic below does not apply.
          if candidate.get('answer_type', 'option') == 'numerical':
              # ── numerical mode (NAT; v4.7) ── R-ANSWER numerical branch. The generator
              # KNOWS candidate.nat_value. Confirm WELL-POSEDNESS by reasoning (not a regex):
              # is there a fair reading of the stem under which a DIFFERENT value follows
              # (ambiguous rounding, under-specified figure, missing unit)? If yes → return
              # False (disambiguate the stem, then regenerate). Also confirm the value's form
              # matches nat_answer_type (integer ⇒ integral) and that, for real NAT, the
              # accepted band ca_range=(lo,hi) is well-formed (lo<=hi). A 0/negative/fractional
              # value is valid (tested by presence, never truthiness). EXAM-AGNOSTIC.
              return value_uniquely_determined(candidate)       # generator-reasoned
          # answer_cardinality comes from the subtopic's blueprint entry (default 'single').
          mode = candidate.get('answer_cardinality', 'single')
          if mode != 'multi':
              # ── single mode (UNCHANGED v4.2 logic) ──
              # The generator KNOWS candidate.correct_pos. Confirm that under a FAIR
              # reading exactly ONE option is defensible. Reasoning check, not a regex:
              # for each other option, ask "is there a reasonable reading of the stem
              # under which THIS option is also correct?" If yes for any → ambiguous →
              # return False (disambiguate the stem or drop the colliding option, then
              # regenerate). Apply the R-ANSWER single-mode classes (kinship maternal/
              # paternal split; contested convention with both forms listed; multi-rule
              # series/analogy) plus any section_rules convention. EXAM-AGNOSTIC.
              return exactly_one_option_defensible(candidate)   # generator-reasoned
          # ── multi mode (MSQ; v4.5) ── candidate.correct_set is the intended set S.
          S = set(candidate.get('correct_set', []))
          n = candidate.get('options_count', 4)
          # (a) S well-formed: non-empty PROPER subset of {1..n}.
          if not S or not S.issubset(set(range(1, n + 1))) or len(S) == n:
              return False                                  # k=0 / out-of-range / k=n
          # (b) fixed-k cardinality (when configured).
          if candidate.get('msq_k_mode') == 'fixed' and len(S) != candidate.get('msq_k'):
              return False
          # (c) R-MSQ-ESCAPE: AOTA banned under multi unless msq_allow_aota.
          if not candidate.get('msq_allow_aota', False) and candidate.get('has_aota_option'):
              return False
          # (d) the SET reasoning obligation (generator-reasoned, not a regex):
          #     every option in S is defensible under EVERY fair reading, AND every
          #     option not in S is indefensible under ANY fair reading. The dangerous
          #     case is a BORDERLINE out-set option — treat exactly like the single-mode
          #     "second defensible option" defect: disambiguate or move/remove it.
          #     Negation already folded into S by the caller (S satisfies the predicate).
          return every_inset_defensible_and_every_outset_indefensible(candidate, S)
      # A passing candidate records answer_verified = True in the sidecar (S7-NEW-A);
      # G-UNIQUE (S12-NEW-16) later fails any Q missing that record; G-MSQ-SET / G-MSQ-CARD
      # (multi only) independently re-check (a)/(b)/(c).
    Without this, G-FORMATDUP could PASS on distinct labels while two questions
    still look identical — the v3.9 audit's most important closure. The sidecar
    stem_format_variant/distractor_strategy written by write_q_to_sidecar (§11)
    are taken from the ACCEPTED candidate's fields, so the gate reads what was
    actually rendered.



## S7-AXIS — Option-3 joint (difficulty × Axis-2) solve orchestration (v5.14)

  THE MOST CRITICAL RULE. A mock must replicate the exam's FORMAT MIX (Axis-2 stem
  structure), not just its syllabus and difficulty. Step 6 carries the per-section target in
  `blueprint.axis_schedule`; Step 7 steers the 7 flexible Axis-2 classes toward it WHILE
  difficulty stays SCHEDULE-FIRST.

  ```
  ORTHOGONALITY (why "joint" almost never actually trades):
    Difficulty (Easy/Medium/Hard) and Axis-2 (MATCH/ASSERTION_REASON/…) are near-INDEPENDENT
    — a MATCH question can be Easy, Medium, or Hard. So in the large majority of mocks BOTH
    the difficulty_schedule counts AND the Axis-2 window targets are satisfiable at once, and
    no trade happens. Difficulty is assigned schedule-first (unchanged, S3-2 / G-QINDEX); the
    Axis-2 class is chosen by the target-aware pick_presentation. They compose.

  TIE-BREAK (only when a genuine conflict is forced):
    1. Subtopic allocation is HARD #1 (fixed by the blueprint; never bent here).
    2. RULE C (presentation uniqueness, §6-3c) is a HARD intra-group constraint and WINS over
       the Axis-2 target: the tracker only re-orders the RULE-C-VALID (unique) variants, so a
       used variant is never chosen to hit a target (decision (b)).
    3. Between DIFFICULTY and AXIS-2, bend AXIS-2 first: difficulty guards the score signal and
       is already a hard gate (G-QINDEX). Because difficulty is assigned schedule-first and the
       Axis-2 arm only chooses among variants (which don't change a question's difficulty band),
       Axis-2 yields to difficulty automatically — the format target is met best-effort and
       AUDITED WITHIN TOLERANCE by audit.py (S4-11), never forced at difficulty's expense.
    4. LINKED is allocation-enforced (Step 6, decision (a)); Step 7 does not steer it. DIRECT is
       the residual filler and is never steered toward (axis2_need==0).
  ```

  WINDOW TRACKER LIFECYCLE (registry-resident; see S3-4 read + S13-4 commit):
  ```python
  # Per MOCK, per SECTION — built once before generating that section's subtopics, then
  # threaded into every generate_subtopic() call and mutated as questions are accepted.
  axis2_trackers = {}
  for section in sections:                                  # section == mock section object
      sec_name  = section['name']
      sec_sched = axis_schedule.get(sec_name)               # blueprint.axis_schedule[section]
      win_counts = axis2_window_counts.get(sec_name, {})    # running counts for THIS window (S3-4)
      axis2_trackers[sec_name] = build_axis2_tracker(sec_sched, win_counts)  # None ⇒ inert

  # v5.37 (GAP-2026-08-06-AXIS1) — AXIS-1 AND AXIS-3 GET TRACKERS TOO.
  # These two were MEASURED (Step 5) and BUDGETED (Step 6) and then never spent, for
  # four releases. A budget that nothing spends is a bug: axis1_target_per_mock and
  # axis3_target_per_mock sat in blueprint.json unread while Step 7 rendered figures
  # straight off the per-subtopic `format` flag, shipping 26 and 30 figures against a
  # budget of 4 on a real exam.
  #
  # PER PAPER, NOT PER WINDOW — the one deliberate difference from Axis-2. Axis-2's
  # minority classes are too rare to place one in every paper, so it accumulates across
  # a 10-paper window. Axis-1/Axis-3 are visible on a single sheet: one mock that is 43%
  # figures, or all-MSQ, is wrong on its own terms whatever the window average says.
  #
  # AXIS-3 IS THE SAME DEFECT, MASKED. On exams whose sections are DEFINED per mechanism
  # (Section A = MCQ, B = MSQ, C = NAT) the section structure accidentally enforced it.
  # On any exam that mixes mechanisms inside a section it was as unenforced as Axis-1.
  axis1_trackers, axis3_trackers = {}, {}
  for section in sections:
      sec_name = section['name']
      sec_sched = axis_schedule.get(sec_name)
      axis1_trackers[sec_name] = bc.build_axis_tracker(sec_sched, 'axis1')
      axis3_trackers[sec_name] = bc.build_axis_tracker(sec_sched, 'axis3')

  # ... during generation, for each subtopic in this section:
  produced = generate_subtopic(subtopic_data, N_alloc, section, registry_snapshot,
                               axis2_tracker=axis2_trackers[section['name']],
                               axis1_tracker=axis1_trackers[section['name']],
                               axis3_tracker=axis3_trackers[section['name']])
  # generate_subtopic records each accepted question's Axis-2 class + negativity into the
  # tracker (axis2_record). When the mock's generation is complete, snapshot every tracker
  # back into axis2_window_counts for the S13-4 commit:
  for sec_name, tr in axis2_trackers.items():
      snap = axis2_window_snapshot(tr)
      if snap is not None:
          axis2_window_counts[sec_name] = snap

  # v5.41 (GAP-2026-08-06-AXIS1) — SNAPSHOT AXIS-1/AXIS-3 TOO, for two reasons that are
  # not optional:
  #   (1) BATCHED / RESUMED RUNS. A mock is generated in batches (batch_size_qs). Without
  #       a snapshot each batch would rebuild its tracker from an empty count and start
  #       the paper's budget over — four figures per BATCH instead of per PAPER, which is
  #       the original defect wearing a smaller number.
  #   (2) THE AUDIT HAND-OFF. `irreducible` is the count of questions granted a figure
  #       OVER budget because their options are images. A-AXIS1 needs it to raise its
  #       expectation, and it cannot be re-derived from the rendered docx — only the
  #       producer knows why it drew what it drew. This is the same principle as
  #       figure_specs (v5.34): the producer's OWN record beats any inference.
  # v5.49 (GAP-2026-08-12-AXISPAPER-HISTORY) — MOCK-KEYED, NOT SECTION-KEYED.
  # Every other S13-4 write below (`rc_manifests`, `di_manifests`, `figural_manifests`,
  # `mocks_completed`, `session_log`, `options_by_q`) either `.append()`s onto an
  # accumulating list or writes `[str(N)] = ...` onto a dict keyed by mock number —
  # both patterns preserve full history across every mock ever committed. Before
  # v5.49, `axis1_paper`/`axis3_paper` were the ONLY two S13-4 fields that broke this
  # pattern: keyed by SECTION NAME ONLY (`reg['axis1_paper'][sec_name] = snap`),
  # overwritten every single mock, with no mock dimension in the write at all — a
  # rolling snapshot, not a ledger. On a real 15-mock exam this meant every earlier
  # mock's per-paper Axis-1/Axis-3 counts were gone the moment the NEXT mock
  # committed, and no audit or gap analysis could ever reconstruct historical
  # per-mock conformance from this field — it had to be rebuilt from
  # `figural_manifests` instead, which happens to carry the same information for
  # Axis-1 (figural) but nothing equivalent exists for Axis-3 (mechanism). Fixed by
  # nesting one more level, mirroring `options_by_q`'s pattern exactly. v5.68: BOTH
  # fields are now keyed by PAPER_ID — `reg['axis1_paper'][paper_id][sec_name] = snap`
  # — with the ordinal key `[str(N)]` written for the MOCK series ONLY. Keying by the
  # ordinal alone was the v5.49 fix's own blind spot: the registry is SHARED across
  # series (ScopedBlueprint §9), so MOCK:M01 and SUBJ:PHYS:01 both landed on key '1'
  # and the later commit destroyed the earlier snapshot — the rolling-snapshot state
  # v5.49 set out to end, restored silently on every exam that mixes tiers
  # (GAP-2026-08-24-AXIS-PAPER-SERIES-COLLISION; measured, both mock-vs-scoped and
  # scoped-vs-scoped). A reader that consumes the CURRENT paper's own commit reads
  # `reg['axis1_paper'][paper_id]`; a reader that wants history has every paper.
  # v5.53.2 (GAP-2026-08-12-S7-AXIS-COUNTS-UNINIT, found by spec_name_audit.py):
  # `axis1_paper_counts` was subscript-assigned below and read at S7-NEW-B
  # (`axis1_paper_counts.get(sec_name, {})`) but INITIALISED NOWHERE in this file —
  # a NameError in strict execution order, same class as GAP-2026-08-12-S13-4-
  # UNDEFINED-BATCHES-COMPLETED. Initialised here, at its producer.
  # v5.54 (GAP-2026-08-12-AXISPAPER-PERSISTENCE — CLOSED): this block previously ALSO
  # wrote `reg['axis1_paper'][str(N)]`/`reg['axis3_paper'][str(N)]` directly onto the
  # in-memory §3 `reg` object — which no code block ever json.dump'ed, so the v5.49
  # mock-keyed history NEVER actually reached the delivered registry. Those two dead
  # writes are REMOVED; instead this block only ACCUMULATES the per-section snapshots
  # (axis1_paper_counts / axis3_paper_counts), and S13-4 threads both into
  # final_assembly.commit_registry(axis1_snapshots=..., axis3_snapshots=...), which
  # persists them at the ONE terminal commit — replace-by-mock ([str(N)]), idempotent,
  # exactly the axis2_window_counts precedent. Same data, same keying, but now it is
  # actually saved.
  axis1_paper_counts = {}
  axis3_paper_counts = {}
  for sec_name, tr in axis1_trackers.items():
      snap = bc.axis_snapshot(tr)
      if snap is not None:
          axis1_paper_counts[sec_name] = snap
  for sec_name, tr in axis3_trackers.items():
      snap = bc.axis_snapshot(tr)
      if snap is not None:
          axis3_paper_counts[sec_name] = snap
  ```
  Absent-safe end to end: no `axis_schedule` (pre-v1.23 blueprint) ⇒ every tracker is None ⇒
  pick_presentation falls back to the exact v5.13 family-menu rotation, and nothing is written
  to `reg['axis2_window']`. The feature turns itself off with zero behavioural drift.

  AXIS AUDIT CONTRACT (v5.36 — formerly the Step-8 contract): audit.py re-tags every generated question with the Step-5
  AXIS CLASSIFIER v1.0 and audits the realized per-window Axis-2 distribution against
  blueprint.axis_schedule (band = ±1/±15% whichever larger; guarantee = ≥1/window; DIRECT
  floats; negative rate = soft WARN). blueprint.json axis_schedule is the AUTHORITATIVE target.

  v5.37 (GAP-2026-08-06-AXIS1) — THE CONTRACT NOW COVERS ALL THREE AXES.
  audit.py additionally audits the realized PER-PAPER Axis-1 (stimulus) and Axis-3
  (mechanism) distributions via bc.check_axis_conformance() — the SAME engine function
  Step 7 spends against, so generator and auditor cannot drift apart. Gates A-AXIS1 and
  A-AXIS3; same ±1/±15% band; the residual class (TEXT / MCQ) absorbs rounding and is
  never audited; irreducible figural overage raises the expectation rather than raising a
  finding.

  AND THE STANDING RULE THAT STOPS THIS RETURNING AS AXIS-4:
    ANY axis carrying `"<axis>_enforcement": "hard"` in blueprint.axis_schedule MUST have
    (a) a tracker built in S7-AXIS and (b) a gate in the auditor. An enforced budget with
    no gate is itself an audit finding (A-AXIS-UNGATED). Before v5.37 both Axis-1 and
    Axis-3 had a budget and neither had a spender or a gate, and nothing in the framework
    was capable of noticing.

## S7-STYLE — Author to the brief, measure what was written (v5.82 — GAP-2026-08-29-STYLE-FIDELITY §6.5.1/§6.5.3)

  Runs per slot, immediately after the question is written and BEFORE
  S7-NEW-A's sidecar write. Dormant (every step below skipped, `style_obs`
  still measured and recorded) when S3-2b returned DORMANT.

  THE BRIEF IS A CONSTRAINT, NOT A TEMPLATE. The frozen S3-12c brief is placed
  in the generation prompt as constraints. SOURCE 1 (S7-CONCEPT) scenario seeds
  are `pattern_key` ABSTRACTIONS ordered by frequency; the exemplar SKELETONS
  are NEVER shown to the generator (P-6) — the generator learns the shape of
  the exam's questions, never their words.

  REJECT-AND-REGENERATE REASONS — EXHAUSTIVE, no others exist:
    (a) measured mechanic != brief          (e) G-PYQ-DIST textual >= REJECT
    (b) measured form != brief              (f) semantic tuple equality
    (c) measured polarity != brief          (g) image dHash within 25
    (d) a numeric given in exclude_values   (normally prevented pre-write, EC-49)

  RECORD-ONLY, NEVER A REJECT: option_shape != brief · stem length outside
  p10–p90 · ask-form not from the cell · lexicon coverage · option_count ·
  stimulus shape · EVERY G-ITEM verdict · EVERY G-STYLE verdict. The
  distinction is deliberate: a rejection costs a generation, so only the
  properties the brief can actually pin are allowed to spend one.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # ── S7-STYLE (executable) ───────────────────────────────────────────────
  import blueprint_core as bc

  def evaluate_attempt(q_obs, brief, pyq_dist, *, low_entropy=False):
      """Which of the seven REJECT reasons this attempt trips. Pure."""
      if not brief:
          return []                     # dormant: nothing to reject against
      r = []
      if brief.get('mechanic') and q_obs.get('mechanic') != brief['mechanic']:
          r.append('mechanic')
      if brief.get('form') and q_obs.get('form') != brief['form']:
          r.append('form')
      if brief.get('polarity') is not None \
              and bool(q_obs.get('polarity')) != bool(brief['polarity']):
          r.append('polarity')
      excl = set(brief.get('exclude_values') or ())
      if excl & set(q_obs.get('numeric_givens') or ()):
          r.append('exclude_value')
      pd = pyq_dist or {}
      if bc.pyq_textual_verdict(float(pd.get('max_textual') or 0.0),
                                low_entropy=low_entropy) == 'REJECT':
          r.append('pyq_textual')
      if pd.get('semantic_equal'):
          r.append('pyq_semantic')
      if pd.get('image_dhash') is not None \
              and int(pd['image_dhash']) <= bc.PYQ_IMAGE_DHASH_MAX:
          r.append('pyq_image')
      return r

  def brief_match_count(q_obs, brief):
      """How many brief fields this attempt matched — the third tie-break when
      the budget is exhausted (ruling Q19)."""
      if not brief:
          return 0
      n = 0
      for f in ('mechanic', 'form', 'option_shape'):
          if brief.get(f) and q_obs.get(f) == brief[f]:
              n += 1
      if brief.get('polarity') is not None \
              and bool(q_obs.get('polarity')) == bool(brief['polarity']):
          n += 1
      lo, hi = (brief.get('stem_len_band') or (None, None))
      if lo and hi and lo <= int(q_obs.get('stem_words') or 0) <= hi:
          n += 1
      if brief.get('ask_form') and brief['ask_form'] in (q_obs.get('ask_form') or ''):
          n += 1
      return n

  def author_slot(generate, measure, brief, *, qnum, total_questions,
                  retries_used, low_entropy=False):
      """The budgeted authoring loop (ruling Q19). Returns
      (question, style_obs, pyq_dist, retries_used). NEVER raises, NEVER stops:
      on budget exhaustion the BEST attempt is ACCEPTED and said so."""
      budget = bc.max_retries_per_paper(total_questions)
      attempts = []
      for attempt_i in range(bc.MAX_ATTEMPTS_PER_Q):
          q = generate(brief, attempt_i)
          obs, pdist = measure(q)
          reasons = evaluate_attempt(obs, brief, pdist, low_entropy=low_entropy)
          attempts.append({'q': q, 'obs': obs, 'pyq_dist': pdist,
                           'reject_reasons': reasons,
                           'max_textual': float((pdist or {}).get('max_textual') or 0.0),
                           'brief_matches': brief_match_count(obs, brief)})
          if not reasons:
              obs['accepted_on'] = 'first' if attempt_i == 0 else 'retry'
              (pdist or {}).setdefault('accepted_on', obs['accepted_on'])
              return q, obs, pdist, retries_used
          # A RETRY IS CHARGED ONLY WHEN ONE ACTUALLY FOLLOWS. Charging after
          # the final attempt would spend the paper's budget at twice the real
          # rate (measured: 66 generations on a 60-Q paper instead of the 72
          # the budget allows, because the budget ran out after 6 questions).
          if attempt_i == bc.MAX_ATTEMPTS_PER_Q - 1 or retries_used >= budget:
              break
          retries_used += 1
      best = attempts[bc.select_best_attempt(attempts)]
      best['obs']['accepted_on'] = 'budget'
      (best['pyq_dist'] or {}).setdefault('accepted_on', 'budget')
      return best['q'], best['obs'], best['pyq_dist'], retries_used
  ```

  BUDGET ARITHMETIC (worst case, 60-Q paper): MAX_ATTEMPTS_PER_Q = 2 and
  MAX_RETRIES_PER_PAPER = ceil(0.20 x 60) = 12, so at most 72 generations.
  The expected case is far lower because the two dominant rejection causes are
  PREVENTED before writing: values are drawn outside `exclude_values`, and the
  brief is fixed before generation. The budget covers style and PYQ-distance
  rejections ONLY — the pre-existing scenario, difficulty and G-DEDUP loops
  keep their own bounds unchanged (P-9).

  EC-21. A subtopic with a tiny value space exhausts the budget; the best
  attempt is ACCEPTED with `pyq_dist.accepted_on = "budget"`, `nearest_pyq_id`
  and `max_textual` recorded in the sidecar, dossier and registry. NOTHING is
  printed in the delivered footer (ruling Q15). EC-9's low-entropy widening
  applies automatically on the next regeneration when the PYQ set itself is
  repetitive.

  EC-30. G-PYQ-DIST cannot be disabled by any instruction — it costs ~2 ms per
  paper, so there is nothing to skip, and the record is ALWAYS written.

## S7-STIMGROUP — One stimulus per question set (v5.85 — GAP-2026-09-21-LINKED-PLACEMENT)

  Applies ONLY when STIM_ACTIVE (S3-12b built this paper with the stimulus profile).
  A legacy paper (STIM_ACTIVE False) is authored exactly as before.

  R-STIMGROUP (HARD, set-placed papers):
    1. ONE STIMULUS PER SET. batch_state['stimulus_groups'] (S3-16) lists every set:
       its Q-numbers, member subtopics in order, and its type. Before authoring the
       FIRST member of a set, author the set's stimulus ONCE (passage / cloze
       paragraph / table / chart / clue set) and register it with stim_register().
       Every member embeds that registered stimulus BYTE-IDENTICALLY (R-LINKED
       Model A is unchanged: the stimulus is still printed inside each member).
    2. A SET THAT CROSSES A BATCH BOUNDARY reuses the registered text — stim_register
       returns it from batch_state, so `continue`, S4-12 resume and a new session all
       read the same stimulus. Never re-author it.
       2b. If batch_state was rebuilt (S4-12 step 2) a partly authored set has no
       registered text: register it by copying the stimulus VERBATIM from that set's
       first authored member in the cumulative docx.
    2c. STIMULUS SIZE. A text stimulus is at least 30 words (the size the profile
       detects sets by, bc.SG_MIN_STIM_WORDS); a shorter shared context must be a
       table or a figure. A-BLOCK-STIMULUS recognises the shared stimulus by exactly
       these forms.
    3. DIFFERENT SETS, DIFFERENT STIMULI. Two sets never share a stimulus, and their
       stimuli are about different subject matter. A single (non-set) question never
       reuses a set's stimulus.
    4. CLOZE ORDER. For a set whose members ask about numbered blanks/gaps, the
       stimulus numbers the blanks (1)..(k) and member j asks blank j, in Q order.
    5. FIGURE/TABLE SETS. One figure (or table) per set; every member embeds the SAME
       image file (identical bytes) or the identical table — exactly the duplication
       R-LINKED Model A already requires of a linked stimulus.
    6. Nothing else changes: difficulty plan, answer budget, K-PAT, dedup, R19
       outside sets, answer verification.
  Checked by G-BLOCK (S4-11) and the auditor's A-BLOCK, A-BLOCK-STIMULUS and
  A-BLOCK-ORDER gates.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  def stim_group_of(qnum):
      """The set a question belongs to, or None (single question / legacy paper)."""
      return STIM_GID_BY_Q.get(int(qnum)) if STIM_ACTIVE else None

  def stim_register(qnum, stimulus_text=None):
      """Return THE stimulus of qnum's set. First call for a set (stimulus_text
      given) stores it in batch_state and on disk; every later call returns the
      stored text — passing a DIFFERENT text is a LADDER-REPAIR R1 [HS:LADDER] (rule 1)."""
      import hashlib
      gid = stim_group_of(qnum)
      if gid is None:
          raise SystemExit(f"HARD STOP [HS:INFRA] (R-STIMGROUP): Q.{qnum} is not in a set.")
      _bsp = f'/home/claude/{EXAM}_M{N}_batch_state.json'
      _bs = json.load(open(_bsp, encoding='utf-8'))
      _g = _bs['stimulus_groups'][gid]
      if _g.get('stimulus') is None:
          if not stimulus_text:
              raise RuntimeError(f"LADDER-REPAIR R2 [HS:LADDER] (R-STIMGROUP): set {gid} has no stimulus "
                               f"yet — author it and pass it for its first member.")
          _g['stimulus'] = stimulus_text
          _g['stimulus_sha256'] = hashlib.sha256(stimulus_text.encode('utf-8')).hexdigest()
          json.dump(_bs, open(_bsp, 'w', encoding='utf-8'))
          STIM_PLAN[gid] = _g
      elif stimulus_text is not None and stimulus_text != _g['stimulus']:
          raise RuntimeError(f"LADDER-REPAIR R1 [HS:LADDER] (R-STIMGROUP): Q.{qnum} carries a stimulus that "
                           f"differs from set {gid}'s registered stimulus — every "
                           f"member embeds the registered text byte-identically.")
      return _g['stimulus']
  ```

## S7-NEW-A — Per-question answer key sidecar write (v2.0 GAP-18 fix; v3.3 concept map; v5.52 mandatory concept_map)

  IMMEDIATELY after each question is accepted and added to docx:
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  def write_q_to_sidecar(qnum, correct_pos, subtopic, concept_group, scenario_key,
                          *,   # v5.52 (GAP-2026-08-12-S10-CONCEPTMAP-MANDATE): everything
                          # from here on is keyword-only, and subtopic_id/difficulty below
                          # carry NO default. Before v5.52 both defaulted to None, so a call
                          # site that forgot them silently persisted `null` into concept_map
                          # — exactly what shipped Mock 10 with `difficulty: null` for all 60
                          # questions, undetected until (if ever) G-QINDEX ran at Final
                          # Assembly, mocks later. Now the omission is a TypeError raised
                          # immediately, at the point of authoring — see S10-0.
                          subtopic_class=None, stem_format_variant=None,
                          distractor_strategy=None,
                          is_ga=False, fact_text=None, source_url=None,
                          event_date=None, answer_verified=False, answer_cardinality='single',
                          has_aota_option=False, msq_instr_in_stem=False,
                          answer_type='option', nat_value=None, ca_range=None,
                          nat_instr_in_stem=False,
                          nat_grading_type=None, nat_grading_value=None,
                          stem_precision=None,
                          subtopic_id, difficulty, difficulty_obs,
                          style_obs, distractor_mechanisms, pyq_dist,
                          # v5.89 (GAP-2026-11-02) — OPTIONAL per-question records, written
                          # only when given (a legacy record stays byte-identical) and carried
                          # into registry.question_index by final_assembly v1.11:
                          difficulty_check=None,     # CHECK 3c decision record (A-CONTENTLEVEL)
                          figural_ask_type=None,     # F8 ask type (A-FIGFORMAT)
                          representations=None,      # F8 representation tags
                          scheme_grammar=None,       # F8 scheme grammar tag
                          marked_sites=None,         # Q7b.8' declaration (figural Qs)
                          ladder=None,               # L4 {rung, reasons, attempts}
                          # v5.90 (GAP-2026-11-03) — the QUALITY RECORD, keyword-only, NO
                          # default on a 2026.11.03 paper (S7-QUALITY lists every key; a
                          # missing key is an item defect at S13-2F, never a silent null):
                          quality=None):             # dict — see S7-QUALITY
      # v5.82 (GAP-2026-08-29-STYLE-FIDELITY §6.5.5): the three style fields are
      # keyword-only with NO default, on the v5.52 argument exactly and for the
      # same reason — a default lets a call site silently persist `null` and the
      # omission is only discovered mocks later. A DORMANT run still passes all
      # three EXPLICITLY: style_obs is always measurable (mechanic/form/polarity/
      # answer_type/option_shape come from the written question, not from the
      # profile) and carries brief_id: None, matched_brief: None; pyq_dist is
      # {'status': 'dormant', 'reason': ...}; distractor_mechanisms is the
      # authored mapping, or {} on a paper whose options carry no authored types
      # (I-6 then records `unknown` and the question proceeds — never a halt).
      # v5.60 (GAP-2026-08-21-DIFFICULTY-STICKER-LABELS): difficulty_obs is
      # keyword-only with NO default, on the v5.52 argument exactly — a default
      # would let a call site silently persist a label with no evidence, which
      # is the defect itself. Dormant runs (difficulty_plan is None) pass
      # difficulty_obs=None explicitly and A-QINDEX check 8 skips those entries.
      # v4.5: correct_pos is an int for single-answer Qs and a SORTED list[int] (the
      # correct set S) for MSQ (answer_cardinality=='multi'). The sidecar stores it verbatim.
      # v4.7: for a NAT question (answer_type=='numerical') the stored answer is the typed
      # VALUE (nat_value: int|float — may be 0, negative, or fractional), NOT an option
      # position; correct_pos is ignored. ca_range=(lo,hi)|None is the accepted band (real
      # NAT) aligned to Step 4's answer_keys.json. The answer is written with `is not None`
      # semantics so a value of 0 is preserved.
      key_data = json.load(open(answer_key_path))
      if answer_type == 'numerical':
          key_data["answers"][str(qnum)] = nat_value
      else:
          key_data["answers"][str(qnum)] = (sorted(correct_pos)
                                            if answer_cardinality == 'multi' else correct_pos)

      # v3.3 — per-question concept record (DOUBT-3): lets the audit gate map
      # scenario_key → Q number for G-CONCEPTDUP / G-COUNT-X-UNIQUE, and verify
      # per-subtopic counts for G-ALLOC-SUBTOPIC. NOT placed in the docx (R5/R12).
      # v3.8 — adds presentation_key fields for RULE C / G-FORMATDUP (DOUBT-4).
      presentation_key = None
      if subtopic_class in ("CLASS2", "CLASS3") and stem_format_variant and distractor_strategy:
          presentation_key = f"{stem_format_variant}|{distractor_strategy}"
      # v4.7: qtype is the unified question-class label aligned to Step 4 (mcq|msq|nat),
      # derived from the two axes. nat supersedes cardinality.
      _qtype = ('nat' if answer_type == 'numerical'
                else 'msq' if answer_cardinality == 'multi'
                else 'mcq')
      key_data.setdefault("concept_map", {})[str(qnum)] = {
          "subtopic": subtopic,
          # v5.2 — the two fields that feed the certified per-question registry.question_index
          # (Contract_QuestionMetadataIndex v1.0). subtopic_id is the cross-step join key Step 6
          # expands into Subject/Topic/Subtopic/Question Type; difficulty is the canonical
          # Complexity label (schedule-first, from blueprint.difficulty_labels). NEVER in docx.
          "subtopic_id": subtopic_id,
          "difficulty": difficulty,
          # v5.60 — the derivation evidence behind the label (CHECK 3c). Carried
          # verbatim into registry.question_index by final_assembly v1.6 so the
          # audit can recompute label == assess_difficulty(obs) forever.
          "difficulty_obs": difficulty_obs,
          # v5.82 (GAP-2026-08-29-STYLE-FIDELITY §6.5.5). Three ADDITIVE fields,
          # carried verbatim into registry.question_index alongside
          # difficulty_obs so the audit twins (A-STYLE, A-PYQDIST, A-ITEM) can
          # recompute every claim from the record forever. A DORMANT run writes
          # all three: style_obs is measured from the WRITTEN question and does
          # not need a profile; brief_id/matched_brief are None; pyq_dist is
          # {'status': 'dormant', 'reason': ...}.
          "style_obs": style_obs,
          "distractor_mechanisms": distractor_mechanisms,
          "pyq_dist": pyq_dist,
          "concept_group": concept_group,
          "scenario_key": scenario_key,
          "subtopic_class": subtopic_class,          # CLASS1..CLASS4
          "stem_format_variant": stem_format_variant, # §6-3c menu token or None
          "distractor_strategy": distractor_strategy, # §6-3c menu token or None
          "presentation_key": presentation_key,       # CLASS 2/3 only; else None
          "answer_cardinality": answer_cardinality,                 # v4.5: 'single' | 'multi'
          "answer_type": answer_type,                 # v4.7: 'option' | 'numerical'
          "qtype": _qtype,                            # v4.7: 'mcq' | 'msq' | 'nat'
          # v4.5 — MSQ structural flags (multi only; harmless defaults for single):
          "has_aota_option": bool(has_aota_option),   # an "All of the above" option exists
          "msq_instr_in_stem": bool(msq_instr_in_stem), # select-instruction is in Q.N line
          # v4.7 — NAT fields (numerical only; harmless defaults otherwise):
          "ca_range": (list(ca_range) if ca_range is not None else None),  # (lo,hi) | None
          # v5.25 — NAT fields (numerical only; harmless None otherwise): the PORTAL-safe
          # grading type/value, sourced FROM derive_nat_grading() (S7-NEW-C) at the call
          # site — never re-derived here. nat_grading_value is the exact string that
          # reaches the docx Correct-Answer line AND the portal upload, unmodified by any
          # downstream step.
          "nat_grading_type": nat_grading_type,       # 'positive_integer'|'integer'|
                                                       # 'decimal'|'decimal_fixed'|'range'|None
          "nat_grading_value": nat_grading_value,     # the 0-9.- only string, or None
          # v5.26 — the stem-stated rounding-instruction N (int) or None, EXACTLY the
          # third argument passed to derive_nat_grading() when nat_grading_type/value
          # were computed. Persisted so audit.py's A-NAT-GRADE self-consistency check can
          # re-run the SAME function call, not just guess the precision back out of the
          # already-formatted string.
          "stem_precision": stem_precision,
          "nat_instr_in_stem": bool(nat_instr_in_stem), # nat_instruction is in Q.N line
          # v4.5 — R-ANSWER: True iff CHECK 3 verify_answer passed for this Q (either
          # mode). G-UNIQUE (S12-NEW-16) Exit 1's if this is missing/False. (Renamed
          # from answer_uniqueness_verified; mode-agnostic.)
          "answer_verified": bool(answer_verified)
      }
      # v5.85 (GAP-2026-09-21-LINKED-PLACEMENT): set membership, written ONLY on a
      # set-placed paper (STIM_ACTIVE, S3-12b) — None for a single question. Its
      # PRESENCE tells the auditor (A-BLOCK) and final_assembly that the paper was
      # built with the stimulus profile; a legacy paper never carries the key.
      if STIM_ACTIVE:
          key_data["concept_map"][str(qnum)]["stimulus_group_id"] = \
              STIM_GID_BY_Q.get(int(qnum))
      # v5.89 — the optional records, ONLY when given (never a null placeholder)
      for _k, _v in (("difficulty_check", difficulty_check), ("figural_ask_type", figural_ask_type),
                     ("representations", representations), ("scheme_grammar", scheme_grammar),
                     ("marked_sites", marked_sites), ("ladder", ladder)):
          if _v is not None:
              key_data["concept_map"][str(qnum)][_k] = _v
      # v5.90 — the QUALITY RECORD is spread onto the entry key by key: the auditor reads
      # every field by name (A-STEMLEAK reads named_entities / scheme_annotations /
      # trailing_placeholders; A-DISTRACTOR reads distractor_mechanisms / class_word /
      # stated_formula / given_smiles / reagents; A-CONSIST reads stem_agents; A-SHAPEMIX
      # reads shape; A-TEMPLATE reads fingerprint; A-STEMFORM reads pattern_key;
      # A-ENTITYLEAK reads entities) and final_assembly v1.12 carries QINDEX_V590_FIELDS
      # into registry.question_index. quality_status is stamped at S13-2F, never here.
      if isinstance(quality, dict):
          for _k, _v in quality.items():
              if _v is not None and _k != 'quality_status':
                  key_data["concept_map"][str(qnum)][_k] = _v

      if is_ga and fact_text:
          key_data["sources"][str(qnum)] = {
              "fact": fact_text,
              "source_url": source_url or "",
              "event_date": event_date or "",
              "ca_window": True if event_date else False,
              "post_2020_changed": False  # update if applicable
          }
      json.dump(key_data, open(answer_key_path, 'w'), indent=2)
  ```
  Called ONCE per question. Not at end of batch. Not at end of mock.
  This ensures partial session recovery is always possible.
  The "concept_map" is an INTERNAL sidecar field — it is NEVER written to the
  docx (R5/R12). The audit gates read it directly instead of re-deriving.
  For CLASS 2/3 questions, stem_format_variant + distractor_strategy MUST be
  supplied (they are the RULE-C presentation_key inputs); omitting them for a
  CLASS-2/3 question is itself a G-FORMATDUP failure (the generator did not
  choose a defined variant — see §6-3c NORMALISATION).

## S7-NEW-B — Figural generation mandate (v2.0 GAP-12 fix; v5.37 budget-gated)

  WHEN blueprint allocates a FIGURAL format question:

  ### ══════════════════════════════════════════════════════════════════════════
  ### S7-NEW-B0 — ASK THE BUDGET FIRST  (v5.37, GAP-2026-08-06-AXIS1 — HARD)
  ### ══════════════════════════════════════════════════════════════════════════

  ```
  BEFORE v5.37 THIS SECTION BEGAN AT OPTION A UNCONDITIONALLY. `format == FIGURAL`
  WAS A RENDERING IMPERATIVE, AND THERE WAS NO CAP OF ANY KIND.

  WHAT THAT COST (measured, IIT_JAM_BIOTECHNOLOGY, 2026-08-06):
      blueprint axis1_target_per_mock FIGURAL      :  4 / 60
      Mock01 Qs allocated to FIGURAL subtopics     : 26  →  26 figures rendered
      Mock02 Qs allocated to FIGURAL subtopics     : 30  →  30 figures rendered
  An exact 1:1 map in both papers. The real exam averages 4.4 figures per 60-question
  paper over the last five years. A mock that is 43% figures does not model a 7% exam,
  and every existing gate certified it clean.

  ROOT CAUSE WAS AN UNSPENT BUDGET. Step 6 has written axis1_target_per_mock into
  blueprint.json since v1.23 and NOTHING EVER READ IT — `grep axis1` over this file
  returned zero hits for four releases. Axis-2 had a full tracker; Axis-1 had none.
  Axis-3 was in the identical state and is fixed in the same release (S7-AXIS3).

  THE RULE NOW:
    format == FIGURAL means the subtopic is CAPABLE of a figural question.
    HOW MANY are drawn  is capped by blueprint.axis_schedule[section].axis1_target_per_mock.
    WHICH ones are drawn is ranked by each subtopic's measured figural_rate.
    Everything else renders TEXT via OPTION B — keeping its allocation slot.

  THE GOLDEN RULE IS UNTOUCHED. Format still never EXCLUDES a subtopic from
  allocation; the sole exclusion criterion remains r_avg == 0.0. All 60 slots stand.
  Only the RENDERING of the denied ones changes.
  ```

  ```python
  import blueprint_core as bc

  # Built once per section, alongside axis2_trackers (S7-AXIS). Per PAPER, not per
  # window: a single mock that is 43% figures is wrong on its own terms regardless of
  # what the 10-paper average works out to.
  axis1_trackers[sec_name] = bc.build_axis_tracker(
      axis_schedule.get(sec_name), 'axis1',
      counts=axis1_paper_counts.get(sec_name, {}))

  # ORDER THE CLAIMS BEFORE SPENDING. A budget of 4 spent on the four subtopics the
  # exam almost never illustrates is conformant-by-count and wrong-by-content.
  # Irreducible first, then highest figural_rate. (Reference exam: organic
  # stereochemistry 79% vs complex formation 3.1% — the pre-v2.26 boolean flagged both
  # identically, and Microbial Biotechnology sits at 0.0% and must never be drawn.)
  # v5.43 (GAP-2026-08-06-IRREDUCIBLE) — THE SCHEDULE DECIDES, NOT THE FLAG.
  # Step 6 has already computed WHICH subtopics carry a figure in WHICH mock, at each
  # subtopic's MEASURED frequency (bc.figural_quota -> bc.schedule_figural_slots). Read
  # that schedule; do not re-derive the decision from the per-subtopic format flag.
  #
  # This is what closes the irreducible-override defect at its source. Before v5.43 the
  # decision was made HERE, per question, from a boolean — so a subtopic allocated to
  # every mock drew a figure in every mock (1.00/paper) no matter that the corpus said
  # 0.68, and an irreducible flag then let it pass over budget in silence. Twenty-one
  # such subtopics forced 14.3 figures per mock against a budget of 5.
  # capacity = how many questions this mock actually allocates to each subtopic, so a
  # subtopic holding 3 questions may carry up to 3 figures. Omit it (v5.43) and the
  # scheduler caps at ONE figure per subtopic per mock, which under-delivers on every
  # exam whose figural budget approaches its figural-subtopic count.
  _cap = {}
  for a in section['subtopic_allocations']:
      _cap[a['subtopic_id']] = _cap.get(a['subtopic_id'], 0) + int(a.get('q_count', 1) or 1)
  # v5.92 (GAP-2026-11-05 DL-29, guard G6): a per-mock quota that would place FEWER figures
  # than the A-AXIS1 band low is withdrawn ({}) by bc.figural_quota_guard, so the ranking
  # allocation below runs instead of under-shooting a hard gate (the Step 5 quota built from
  # an empty figural_count_by_subtopic was {} for every chemistry subtopic).
  _ax1_sched = axis_schedule.get(sec_name) or {}
  _ax1_target = (_ax1_sched.get('axis1_target_per_mock') or {}).get('FIGURAL', 0)
  _ax1_band = bc.figural_band(_ax1_target, _ax1_sched.get('axis1_observed_figural'))   # the ALLOWANCE
  _ax1_low = max(0, int(round(float(_ax1_target or 0))) - int(_ax1_band))              # A-AXIS1 band low
  _ax1_quota = bc.figural_quota_guard(_ax1_sched.get('axis1_figural_quota') or {},
                                      int(bp.get('total_mocks') or 1), _ax1_low)
  figural_slots = bc.schedule_figural_slots(
      _ax1_quota,
      _ax1_sched.get('axis1_target_series') or [],
      _ax1_band,
      capacity=_cap)
  # Empty schedule (pre-v1.45 blueprint) ⇒ fall through to the v5.41 ranking below, so
  # every un-remeasured exam keeps its current behaviour exactly.
  # v5.58 (GAP-2026-08-20-AXIS1-EMPTY-SCHEDULE-SENTINEL) — THE TEST IS `any()`, NOT
  # TRUTHINESS. bc.schedule_figural_slots returned `[{}, {}, ... x n]` for an empty
  # quota: a TRUTHY list carrying NOTHING. `if figural_slots` therefore passed, the
  # filter below ran with an empty allowance, and every capable slot was stripped
  # before rank_figural_candidates or axis_grant_figural ever saw it — 0 figures
  # against a real budget, on every pre-v1.45 blueprint in the estate, silently.
  # The engine now returns [] (blueprint_core, same release) so plain truthiness is
  # already correct; `any()` is kept here as the SECOND layer, because this comment's
  # promise must hold against ANY scheduler that returns a per-mock list — the
  # producer fix and the consumer fix are deliberately independent.
  this_mock = figural_slots[(N - 1) % len(figural_slots)] if any(figural_slots) else None
  if this_mock is not None:
      # this_mock is {subtopic_id: n_figures} (v1.46, was a set) — take AT MOST that many
      # slots per subtopic, in the ranked order established below.
      _left = dict(this_mock)
      _keep = []
      for (q, sid) in figural_capable_slots:
          if _left.get(sid, 0) > 0:
              _left[sid] -= 1
              _keep.append((q, sid))
      figural_capable_slots = _keep

  # v5.92 (GAP-2026-11-05 DL-50): an ABSENT figural_reducible line defaults to False for a
  # subtopic whose dominant PYQ figure family is a chemistry structure / scheme (S3-2S
  # CHEM_FIGURE_SUBTOPICS) — its options ARE the structures. A line present in section_rules
  # (Step 5 v2.60.0 writes it for every subtopic) is always read as written.
  def _fig_reducible(sid):
      return bool(SR[sid].get('figural_reducible',
                              sid not in (globals().get('CHEM_FIGURE_SUBTOPICS') or set())))
  ordered = bc.rank_figural_candidates(
      figural_capable_slots,                      # [(qnum, subtopic_id), ...]
      rates={sid: SR[sid].get('figural_rate', 0.0)      for sid in capable_ids},
      reducible={sid: _fig_reducible(sid) for sid in capable_ids})

  for qnum, sid in ordered:
      granted, why = bc.axis_grant_figural(
          axis1_trackers[sec_name], sid,
          reducible=_fig_reducible(sid))
      if granted:
          ...   # OPTION A below — render the real image
      else:
          ...   # OPTION B below — REPLACEMENT_RULE, question KEEPS its slot
  ```

  THREE OUTCOMES (bc.axis_grant_figural, precedence order):

  | outcome | when | effect |
  |---|---|---|
  | `inert` | no `axis_schedule` (pre-v1.23 blueprint) | GRANT — byte-identical legacy behaviour for every un-remeasured exam |
  | `irreducible` | `figural_reducible: false` — the OPTIONS are images (organic structures, circuit diagrams, spectra) | GRANT **even over budget**. There is no text form of such a question; capping it would ship something no candidate can answer. GOLDEN RULE decides. |
  | `budget` / `over_budget` | budget remains / exhausted | GRANT, else OPTION B |

  An `over_budget` question is **NOT dropped and NOT weakened**: it keeps its
  allocation slot, its subtopic, its difficulty band and its answer_cardinality, and
  renders from that subtopic's own observed PYQ_STEM_PATTERNS. For every subtopic
  whose `figural_rate` is under 50% — 37 of the reference exam's 46 — the text form is
  the *majority* shape in the real papers, not a consolation prize.

  IRREDUCIBLE OVERAGE IS RECORDED, NEVER WARNED. `bc.check_axis_conformance()` raises
  its expectation by the irreducible count, so an excess fully explained by them is a
  SILENT PASS, and any excess that is not is a HARD FAIL. This is what keeps the
  exemption from becoming the hole the whole gate leaks through — the failure mode
  that let 26 figures ship twice.

  OPTION A (generate real image — DECOMPOSED, v4.0):
    Render via matplotlib at FIGURAL_DPI=300 and place via §10-S10-7/S10-8.
    DECOMPOSITION MANDATE (R-FIGURAL — LADDER-REPAIR R1 [HS:LADDER]): a figural MCQ is rendered as
      • the problem/series figure(s) as their OWN image(s), AND
      • EACH option as its OWN separate image — one image per option,
        bound 1:1 to its "i." label, stacked SINGLE-COLUMN (one option per line).
    NEVER bake the problem + options + caption into one composite panel. NEVER
    bake the stem, caption, or option numbers into any raster (intrinsic figure
    annotations — e.g. a mirror line's M/N endpoints, geometry vertices, axis
    labels — are figure content and ARE allowed). Reference lines/axes (mirror
    line MN, number line, etc.) are drawn as REAL geometry, never floating
    letters. Build geometry vector-first (matplotlib patches / SVG paths) →
    rasterise to lossless PNG at 300 DPI (never JPEG, never upscale a small
    bitmap). All option images share one uniform SQUARE canvas size.
    Verify via view tool (9-item visual checklist). Log in figural manifest.

  OPTION B (replacement rule — if image generation fails or subtopic is banned):
    Check FIGURAL_BANNED in section_rules for this subtopic.
    If banned OR generation impossible:
      Replace with TEXT alternative from REPLACEMENT_RULE in section_rules.
      The replacement subtopic is read from that exam's REPLACEMENT_RULE
      (exam-agnostic — no subtopic name is hardcoded here). Prefer a replacement
      still missing from this mock's allocation, so the swap can also help satisfy a
      manifest.mandatory_every_mock subtopic where applicable.
      Log replacement: "FIGURAL slot Q.[N] replaced with TEXT [subtopic]."

  OPTION C (text placeholder) IS BANNED:
    NEVER deliver: "Q.19: [The figure shows a series of shapes...]"
    NEVER deliver: text descriptions of what an image would show.
    NEVER mark as "Image will be added later."
    A question is either a real image (Option A) or a real text replacement (Option B).
    Nothing in between. LADDER-REPAIR R4 [HS:LADDER] if a text placeholder is found before delivery.

## S7-QUALITY — THE QUALITY RECORD every item carries (v5.90 — GAP-2026-11-03; every exam)

  PRINCIPLE QQ-0 (blueprint_core Cluster QQ). A [CLASS: D] gate reads ONLY what the auditor
  can recompute from the delivered artefact — the docx text, the rendered picture, the
  figure record's canonical identity WRITTEN BY THE RENDERER, the registry key. The fields
  below are the author's DECLARATIONS; they EXPLAIN a verdict and feed the reviewer, they
  never PRODUCE a [D] verdict. The incident paper shipped with every quality control
  reading a declaration (deduction_steps, scenario_key, "mechanism present"); that is the
  class of defect this section removes.

  For EVERY item, before write_q_to_sidecar(..., quality=Q), build Q with these keys
  (None only where the key does not apply — e.g. no `class_word` when the stem names no
  class; NEVER omit a key that applies):

    ask_format            (v5.92 — GAP-2026-11-05 DL-22/34) the ask FORMAT the item renders,
                          figure_types.normalise_ask_format(stem_text, option_texts) over
                          figure_types.ASK_FORMATS ('direct' | 'statement' | 'match' |
                          'sequence' | 'assertion_reason' | 'combination'); counted against
                          the blueprint's axis2_format_floor_per_paper by the WARN-only
                          A-AXIS2 and the Step 9 bench card. Never a [D] verdict.
    shape                 the BARE ask type the item RENDERS (figure_types.ASK_TYPES[family]
                          vocabulary; the key of shape_target_per_paper and the value of
                          batch_state['shape_plan'][q] — never 'ask|grammar'). A mismatch
                          with batch_state['shape_plan'][q] is an item defect (R3).
    scheme_grammar        the scheme grammar tag (figure_types.SCHEME_GRAMMAR_TAGS; 'none'
                          for a text item) — the second half of the Step-5 shape share key.
    fingerprint           bc.template_fingerprint(ask_type, qtype, scheme_grammar,
                          data_in_stem_type) — G08 caps are counted on it.
    stem_text / option_texts / figure_files
                          the delivered stem (plain text), the option texts in label order
                          ([] for picture options) and the figure file names placed under
                          the item — the S13-2G review packet is built from these (the
                          reviewer reads the docx too; these make the queue self-contained).
    concept               the taxonomy concept id of the tested idea (G08 concept counts).
    pattern_key           the stem pattern authored to (mechanic|form|polarity|answer_type|
                          option_shape, section_rules PATTERN_KEYS) — G-STEMFORM.
    key_set_size          |key set|: 1 for a single-answer item, len(correct_pos) for an MSQ
                          (the auditor derives it from the sidecar answers when absent).
    distractor_mechanisms MANDATORY list of length options_count - key_set_size, one
                          bc.MECHANISM_VOCABULARY[family] member per wrong option, each with
                          a one-line pathway in `distractor_pathways` (same order). NAT: [].
                          A record that is short, or names a mechanism outside the
                          vocabulary, is an item defect at R2o (bc.distractor_record_check).
    mechanism_family      'chemistry' | 'quantitative' | 'verbal' | 'fact' | 'reasoning'.
    class_word            the class noun the stem asks for ("alkene", "acid", "reagent",
                          "capital city") — bc.CLASS_PREDICATES decides [D] for chemistry,
                          the reviewer for the rest.
    stated_formula / stated_dbe / stated_rings / stated_stereocentres
                          every computable datum the stem states (G06 R6.3 b).
    given_smiles          SMILES of every drawn given (the same strings the figure record
                          carries — the auditor re-perceives identity from the record).
    reagents              reagent / condition names as printed on the scheme (resolved
                          through bc.REAGENT_LEXICON; an unresolved name -> reviewer).
    reagent_unit_formula  for over-/under-reaction distractors, the unit added/removed.
    stem_agents           every reagent / condition the STEM TEXT names (G-CONSIST a).
    entities              [{'role', 'text', 'kind', 'concept'}] — every named entity of a
                          TEXT item (GK: "India", "1947"; verbal: the target word) with its
                          role in bc.ENTITY_ROLES; molecules are NOT listed here (the figure
                          record is their source of truth).
    named_entities        [(name_in_stem, identity)] — every entity the stem names in words
                          that is ALSO drawn, with the identity bc.structure_identity gives
                          its SMILES (py2opsin / OPSIN when available; otherwise the author
                          supplies the SMILES it drew for that name). G-STEMLEAK (b).
    scheme_annotations    every text on the scheme that is not a reagent / condition
                          ("partial hydrolysis", "(labelled)") — G-STEMLEAK (c) FAILs any.
    condition_vocab       the exam's observed condition tokens the scheme used.
    trailing_placeholders / asked_placeholders
                          letters drawn after an arrow ("-> P") and letters the stem asks for.
    multi_step_lettered_allowed  True only when the cascade cell's PYQs use that grammar.
    pyq_phrase_states_constitution  stereoisomer-count items: True when the cell's PYQ
                          phrase counts the drawn constitution (G-CONSIST c exemption).
    stereo_declared       per drawn structure, on the DRAW itself: corpus_io.stereo_declared
                          (draw_fn, '2E,4Z' | '(2R,3S)' | 'none') — owner Q-A; S10-8 runs
                          bc.stereo_declaration_check before the figure is accepted
                          (G-STEREODECL: the author's SMILES must encode the author's intent).
    option_text_smiles    (v5.95 — RC-17, owner Q10 (a)) {option label: SMILES} for every TEXT
                          option that names a chemical species: explain_engine.names_to_smiles
                          (curated table, then OPSIN — installed once per session by the engine),
                          else the SMILES the author meant, re-parsed by RDKit; an unparsable or
                          unresolved name is listed in name_unresolved. It feeds the NAME CHECK
                          below (a record field of THIS step: the registry does not carry it, and
                          Step 9 re-resolves every printed name itself, MockTestExplain §6A-13 H-2,
                          so a text-only organic item is still explained with figures).
    name_unresolved       (v5.95) [names in the stem / text options that neither the curated
                          table nor OPSIN resolved] — informational, [] when every name
                          resolved; never a defect by itself (a Step 7 record only — Step 9 resolves
                          every printed name again and lists its own NAME_UNRESOLVED in MockTestExplain §R3).
  NAME CHECK AT AUTHORING (v5.95 — GAP-2026-11-07 RC-6 / F-6; [CLASS: D]): before
  write_q_to_sidecar, run explain_engine.name_check_item(stem_text, option_texts,
  answer_smiles=<the key's structure>, option_smiles=<option_smiles merged with
  option_text_smiles>, chain=<the solution's species>). Any CHS_STEM_NAME_MISMATCH (the stem
  names the product's formula as another structure — a locant error) or
  CHS_OPTION_NAME_MISMATCH makes the item a DEFECT: the code is the finding's reason on the
  S10 repair ladder (bc.ladder_entry -> R2, regenerate the same item; L1 — with other
  findings the lowest rung first), so it is regenerated in this batch, never shipped and
  never carried as an author note. A CHS_CHECK_FAULT is recorded and the item proceeds.
  Never a stop of the run.

  THE JUDGE PACKET (G02; OD-4 keeps the existing tolerance and R5): CHECK 3c (a) now
  builds its blind input with bc.build_judge_input(item, EXEMPLARS, difficulty_labels) —
  the author's difficulty_plan / difficulty_obs / solution / rationale are STRIPPED and the
  sha256 of the packet is stored as difficulty_check.judge_input_sha256. EXEMPLARS come
  from the exemplar bank (S3-2e EXEMPLAR_BANK_PATH; content-carrying: stem, options, key,
  content record), cascade subtopic -> topic -> section; bc.difficulty_exemplars' snippets
  are the fallback ONLY when the bank is absent, and then the rating is recorded with
  rationale "snippets only — no exemplar bank (OD-11)". The content floor (b) runs for any
  label count >= 2 (bc.ccp_model v1.30) and the band is bc.final_band_decision(rated,
  ccp_status, ccp_band, labels): the author's counts NEVER raise a band. v5.92: a LEVEL
  item (CHECK 3c (b1)) takes the L1 level path instead — bc.level_check both ways, no
  final_band_decision — and its difficulty_obs carries 'level', 'level_vector' and
  'closeness' so A-LEVEL / A-CLOSENESS re-measure it from the record.

  INDEPENDENT REVIEW (OD-5) is NOT here: it runs INSIDE this run after the S13-2F sweep — a
  fresh reviewer per packet part (Framework_MockReview, the internal brief) — and its
  verdicts are bound to the paper automatically (S13-2G, v5.91). Never a user step.

## S7-NEW-B2 — SEMANTIC-OBJECT REGISTRATION (v5.59 — every generated figure; HARD)

  A figure that cannot say what it depicts cannot be reconciled by any later step.
  IMMEDIATELY after a figure renders (OPTION A, any image_role), register one
  semantic object PER ROLE (problem, problem:<i>, option:<label>) in
  fig_manifest questions[str(qnum)].semantic_objects:
  ```python
  import paper_pipeline as pp, corpus_io as cio
  obj = {'role': 'problem',                  # 'problem' | 'problem:<i>' | 'option:<label>'
         'kind': 'STRUCTURE',                # pp.SEMANTIC_KINDS — STRUCTURE · REACTION ·
                                             # NEWMAN · FISCHER · MO_DIAGRAM · ORBITAL_BOXES ·
                                             # COORDINATION · PLOT · TABLE · GEOMETRY · GENERIC
         'name': 'salicylic acid',           # human-readable identity
         'canonical': 'OC(=O)c1ccccc1O',     # STRUCTURE/REACTION: SMILES (MANDATORY);
                                             # other kinds: None
         'descriptor': {'acidic_sites': 2}}  # typed facts the answer turns on
  pp.validate_semantic_object(obj, ctx=f'Q{qnum}')          # raises on a malformed object
  fm['questions'][str(qnum)].setdefault('semantic_objects', []).append(obj)
  ```
  STRUCTURE / REACTION FIGURES ARE RENDERED FROM THEIR CANONICAL FORM.
  ── REACTION (v5.88, LAW F1.3 — corpus_io v1.16) ──────────────────────────────
  A REACTION role is drawn by the SCHEME COMPOSITOR, never by structure_draw_fn
  (which draws one molecule and rejects reaction SMILES — the pre-v5.88 contradiction
  that forced every reaction-dominant exam into lone molecules + a 26-word stem):
  ```python
  import figural_core as fc, corpus_io as cio, paper_pipeline as pp
  stem_text, option_texts = q['stem'], q['options']    # this question's authored text (S7-NEW-A)
  scheme = {'items': [                                  # reading order; 'rows': [[...], ...] for G8
      {'mol': 'Oc1ccc2ccccc2c1-c1c(O)ccc2ccccc12'},                        # substrate tile (G1; 'label', 'equiv')
      {'arrow': {'dir': 'right', 'above': ['t-BuCl (2 equiv)', 'anhyd. AlCl₃'],
                 'below': ['CH₂Cl₂, −78 °C'], 'reagent_mol': None}},        # G2/G3/G4 (≤2 lines each side)
      {'placeholder': 'A'},                                               # G5  |  {'bracket': 'A'} → G6
  ]}
  # v5.89 (GAP-2026-11-02 F1): PRINT-TRUE — the scheme draws itself at the paper's
  # problem tokens (TOK, S3-2S): one bond length for every molecule of every scheme,
  # monochrome unless the exam's PYQs are measured coloured, natural size, re-flow on
  # overflow. NATIVE_OK False (degraded rdkit) -> legacy call, AMBER footer note.
  draw = (cio.render_scheme(scheme, tokens=TOK['problem']) if NATIVE_OK
          else cio.render_scheme(scheme))
  cc = fc.colour_is_content(stem_text, option_texts)                  # Q7b.13 — monochrome when colour is the ask
  png = f'/home/claude/q{qnum}_problem.png'                           # S10-8 canonical name
  # marked_sites: the S7 author's MARK-IFF-NAMED declaration (Q7b.8'); [] when the stem
  # names no site — the figure then carries no mark of any kind. For a SCHEME every entry
  # also carries "tile": the molecule's index in draw.tiles (molecules numbered in drawing
  # order — each {'mol'} item, an arrow's reagent_mol, and each member of a 'pair' count
  # one each), and the SAME mark is placed on that molecule in the scheme spec itself:
  # {'mol': smi, 'marks': [...]}, {'arrow': {..., 'reagent_marks': [...]}} or
  # {'pair': [...], 'pair_marks': [marks_A, marks_B]} (corpus_io v1.17). G-FIGMARK
  # matches declared and drawn marks by (tile, site, device[, text]).
  spec = fc.make_figure_spec(qnum, 'schematic', 6.0, role='problem',
                             canvas_aspect=getattr(draw, 'suggested_aspect', None),
                             colour_content=cc, style_profile=STYLE_PROFILE,
                             marked_sites=q.get('marked_sites', []), stem=stem_text,
                             chem=True)
  if not NATIVE_OK:
      spec['raster_content'] = True       # G-FIGLABELPX witnesses labels on the legacy path
  fc.render_figure(draw, png, spec)       # native: natural size, scale 1.0; legacy: fitter Q10/Q11
  fc.write_spec_sidecar(spec, png)        # S10-8 sidecar — S13-4 / --fig-manifest read the class from it
  obj = cio.scheme_semantic_object(draw, role='problem', name='Friedel–Crafts t-butylation')
  pp.validate_semantic_object(obj, ctx=f'Q{qnum}')   # kind REACTION; canonical 'R>A>P' MUST contain '>>'
  ```
  `draw.canonical` is the reaction SMILES assembled from the DRAWN molecules
  (`reactants>agents>products`; placeholders omitted and listed in
  `descriptor.unknowns`; a reagent drawn as a structure is an AGENT); a multi-row panel
  registers one REACTION object per row (`role='problem:<i>'`, `scheme_semantic_object(
  draw, role=..., row=i)`). A molecule SET ('A.B') is a STRUCTURE set, never a REACTION —
  paper_pipeline v5.40 rejects a REACTION without '>>' at registration — and
  `render_scheme` itself refuses a row with no arrow, so a pair or a set can never be drawn
  AS a scheme. The option canvases stay decomposed per R-FIGURAL. G10 (a labelled pair
  `{'pair': [('A', smi), ('B', smi)]}`) is legal ONLY as the product side of a row that has
  an arrow (the canonical is then `R>A>smiA.smiB`, one REACTION object); an OPTION that is
  itself a labelled pair of structures is rendered through `fc.render_option_set` with
  `cio.structure_draw_fn` per molecule and registers TWO STRUCTURE objects
  (`role='option:<k>'`, canonical = each molecule's SMILES) — never a REACTION (E12).
  The registry row (figure_types) for every reaction family names this renderer; the
  recorded object_type is that row's canonical type (reaction_scheme /
  reaction_mechanism_scheme / …) and the FigureSpec class is `schematic` (S10-6A).
  ── STRUCTURE ────────────────────────────────────────────────────────────────
  The draw_fn passed to figural_core.render_figure / render_option_set for a STRUCTURE
  role is (v5.89 — GAP-2026-11-02 F1/F2/F7):
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import corpus_io as cio

  def make_structure_draw(obj, marked_sites, TOK, ABBREV, NATIVE_OK, protect_atoms=()):
      """v5.89: the ONE structure draw_fn factory. protect_atoms: atoms no abbreviation
      may cover — for a scheme molecule cio.abbreviation_protected_atoms(reactant,
      product); for an option set the atoms outside the MCS common to all options."""
      if not NATIVE_OK:                   # degraded rdkit: legacy path + AMBER note
          _note = ('renderer degraded (a chemistry structure was drawn on the legacy path: '
                   + ', '.join(NATIVE.get('missing') or ['native raster unavailable']) + ')')
          if _note not in STYLE_NOTES and not any(n.startswith('renderer degraded') for n in STYLE_NOTES):
              STYLE_NOTES.append(_note)  # the footer discloses EVERY legacy chemistry draw
          # The legacy renderer can draw only an atom ASTERISK (as an atom highlight)
          # and a BOLD bond (as a bond highlight); pass the same dict to make_figure_spec
          # as highlight=legacy_highlight(marked_sites) so G-FIGMARK sees what was drawn.
          # A declaration using another device fails G-FIGMARK -> ladder R1 re-authors the
          # stem with a drawable device.
          _hl = legacy_highlight(marked_sites)
          return cio.structure_draw_fn(obj['canonical'], highlight_atoms=_hl['atoms'],
                                       highlight_bonds=_hl['bonds'])
      _role = str(obj.get('role', 'problem'))
      return cio.structure_draw_fn(
          obj['canonical'],
          tokens=TOK['option' if _role.startswith('option') else 'problem'],
          marks=[{k: m[k] for k in ('site', 'device', 'text') if k in m}
                 for m in (marked_sites or [])],     # 'text' = the letter of a letter mark
          abbreviations=ABBREV,           # None => no abbreviation at all
          protect_atoms=tuple(protect_atoms))

  def legacy_highlight(marked_sites):
      """Degraded mode only: the marks the legacy renderer can draw."""
      ms = marked_sites or []
      return {'atoms': [m['site']['index'] for m in ms
                        if m.get('device') == 'asterisk' and m['site'].get('kind') == 'atom'],
              'bonds': [m['site']['index'] for m in ms
                        if m.get('device') == 'bold' and m['site'].get('kind') == 'bond']}
  # every PROBLEM figure spec: fc.make_figure_spec(..., style_profile=STYLE_PROFILE,
  #     marked_sites=<declaration>, stem=<stem text>, chem=True). An OPTION spec passes
  #     marked_sites=<that option's own declaration> and stem=<stem text> ONLY when that
  #     option declares a mark; otherwise marked_sites=[] and stem=None (a site the stem
  #     names belongs to the problem figure, not to every option canvas). Legacy path
  #     (NATIVE_OK False) adds highlight=legacy_highlight(marked_sites) to make_figure_spec
  #     and spec['raster_content'] = True.
  ```
  An option set is rendered with ONE token set through fc.render_option_set (uniform
  canvas, one bond length; G-FIGOPTWINDOW). The native raster IS the figure: it is
  placed at its natural width and `draw.canonical` (the UNcondensed canonical SMILES)
  is what gets registered. v5.80's highlight_* arguments are retired for structures
  (S10-7C C9). Hand-placed bonds (ring_pts / bond / substituent
  helpers) for a STRUCTURE role are a G-FIGSEM HARD FAIL: that is exactly the
  drawing whose carboxyl was read as a ketone because nothing recorded otherwise.
  A SMILES rdkit rejects (valence / syntax) never renders — fix the molecule.
  Other kinds register a descriptor the explaining step can compare (a NEWMAN's
  front/back substituents and dihedral; an MO_DIAGRAM's occupancy by level; a
  COORDINATION's ligand set and arrangement). GENERIC is the floor, never the
  default for a kind the list names.
  GATE G-FIGSEM (S12, batch + Final Assembly): every rendered figural Q carries
  ≥1 validated semantic object per role; every STRUCTURE/REACTION role's canonical
  canonicalises through cio.canonical_structure (v1.16: a REACTION canonical is a
  reaction SMILES and MUST contain '>>'); a STRUCTURE PNG was produced by
  structure_draw_fn and a REACTION PNG by render_scheme (every tile of which carries
  structure_draw_fn provenance). EC-V18: exams whose figures are not typed objects
  register GENERIC with a descriptor — nothing halts for lack of chemistry.

## S7-24 — QA mandatory-topic tracking (v4.9 — exam-agnostic; names removed)

  v4.9 CHANGE: no QA subtopic name is hardcoded here. Every QA mandate is DATA,
  owned by the manifest + gates, mirroring the v4.4 alternation migration.

  ── MANDATORY-EVERY-MOCK presence ──
    NOT restated by name. A QA subtopic that must appear in every mock is declared
    once as DATA (Step 0 emits mandate_every_mock=true → manifest.mandatory_every_mock;
    Framework_MockTestAnalyse v2.10). Enforcement:
      • Step 1 RULE M1 force-places 1Q of each mandated id in every mock;
      • Step 7 S3-17 HARD STOP [HS:INPUT]s pre-generation if a mandated id is absent (HS-8);
      • G-ALLOC-SUBTOPIC guarantees each allocated subtopic reaches its q_count, so a
        mandated subtopic is also present in the GENERATED questions (not just allocated).
    Empty config ⇒ vacuous no-op, never a false stop.

  ── ALTERNATION pairs (interest, partnership/mixture, any others) ──
    Declared once as DATA in manifest.alternation_groups (set alternation_group on
    both members in Step 0) and enforced exam-agnostically by S3-17 (pre-gen HARD
    STOP, HS-12) + G-ALTGROUP (audit backstop). No pair is hardcoded here. (v4.4)

  ── MATH CONVENTION (e.g. the π value) ──
    Read the exam's stated convention from section_rules (per-subtopic NOTE, e.g. a
    declared π value) and apply it in every affected stem. Exam-agnostic — no numeric
    convention is hardcoded in this file.

  ── ISSUE 2b MANDATES (v5.0 — now enforced) ──
    GROUP-PRESENCE ("≥1 of a subtopic GROUP per mock") and MIN-COUNT ("≥k Q per
    mock") are enforced via manifest.mandatory_groups and manifest.min_counts
    (Step 0 v2.11 + Step 1 v1.11 RULE M4/M6). Step 7 VERIFIES them at S3-17
    CHECK 3 / CHECK 4 (pre-gen) + G-GROUPMANDATE / G-MINCOUNT (post-gen
    backstops). PER-WINDOW CADENCE ("≥1 every N mocks") is a CROSS-mock
    constraint enforced solely by Step 1 RULE M5 — NOT gated in Step 7 (see
    S3-17 note). Zero subtopic names hardcoded; empty config ⇒ vacuous no-op.

## S7-31 — GIR mandatory-subtopic tracking (v4.9 — exam-agnostic; names removed)

  v4.9 CHANGE: no GIR subtopic name is hardcoded here. All GIR mandates are DATA,
  owned by the same manifest + gates as S7-24.

  ── MANDATORY-EVERY-MOCK presence ──
    A GIR subtopic that must appear in every mock is declared as DATA
    (mandate_every_mock=true → manifest.mandatory_every_mock) and enforced by Step 1
    RULE M1 + Step 7 S3-17 (HS-8) + G-ALLOC-SUBTOPIC — identical mechanism to S7-24.

  ── CROSS-MOCK VARIANT ROTATION (e.g. "a different cipher each mock") ──
    Owned by S6-9: read an OPTIONAL per-subtopic ROTATION: cycle (and ROTATION_BAN:
    for a permanently-banned variant) from section_rules by subtopic_id; rotation_pick
    selects a variant ≠ the previous mock's. A subtopic that declares no cycle has no
    constraint. No cipher family or banned variant is hardcoded here. (S6-9, v4.4)

  ── ISSUE 2b MANDATES (v5.0 — now enforced) ──
    MIN-COUNT mandates ("≥k Q per mock") and GROUP-PRESENCE mandates are enforced
    via manifest.min_counts and manifest.mandatory_groups (Step 0 v2.11 + Step 1
    v1.11 RULE M4/M6). Step 7 verifies at S3-17 CHECK 3/4 + G-GROUPMANDATE /
    G-MINCOUNT. PER-WINDOW CADENCE is cross-mock, owned by Step 1 RULE M5 — NOT
    gated here. No subtopic name or count is hardcoded; empty config ⇒ no-op.


# ════════════════════════════════════════════════════════════════════════
# §8 — FORMAT-SPECIFIC GENERATORS (v2.0 — DI TABLE FIX)
# ════════════════════════════════════════════════════════════════════════

## S8-1 — TEXT question generator (unchanged from v1.0)

## S8-2 — PASSAGE (RC) generator (unchanged from v1.0)
  Remember: after RC batch → write progress.json (S4-8).

## S8-3 — PASSAGE (Cloze) generator (unchanged from v1.0)
  Remember: after Cloze batch → write progress.json (S4-8).

## S8-4 — DI table question generator (v2.0 GAP-06 fix)

  HARD RULE: DI table MUST use build_word_table() / build_di_table_styled().
  BANNED: plain text pipe-delimited tables ("Quarter | Sales | ...")
  BANNED: text alignment with spaces ("Q1    100    200    300")
  DETECTION: before delivery, check docx for any paragraph containing
    "|" pipe characters within a non-table paragraph → C-TABLE gate FAIL.

  STRUCTURE (v5.32, GAP-2026-07-29-TBL): a DI table's GEOMETRY is part of its
  content. When the modelled PYQ carries a grouped header — one cell spanning
  several columns above a label cell spanning several rows — the generated table
  MUST carry the same spans. Squaring it into a rectangle padded with empty cells
  is BANNED: the values survive, the meaning does not.
  The geometry model is the TableSpec owned by corpus_io Cluster I
  (Framework_PYQPrepare S1-8a): ANCHOR CELLS ONLY, with 'cs' / 'rs' spans, and
  padding is not expressible. Authoring a two-tier header is therefore three
  keystrokes, not a workaround:
      {'grid': [[{'t': 'Days', 'rs': 2}, {'t': 'Printers', 'cs': 4}],
                [{'t': 'L'}, {'t': 'M'}, {'t': 'N'}, {'t': 'O'}],
                ['Friday', '10,230', '9580', '7560', '9600']],
       'header_rows': 2}
  corpus_io.place_cells() RAISES on a hole or an overlapping span, so a
  malformed table fails at generation rather than shipping as a squared grid.

  PYTHON-DOCX IMPLEMENTATION (mandatory for DI):
  v5.32 — GEOMETRY IS DELEGATED, PRESENTATION STAYS HERE. corpus_io.build_di_table
  places cells (spans included), writes text and stamps column widths; this function
  adds Step 7's own look. The previous local implementation owned BOTH and could
  express neither a colspan nor a rowspan.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import corpus_io      # routed to MockCreate / TestCreate in routes.json

  def build_di_table_styled(doc, spec, rows=None):
      """
      DI table: dark navy header row(s), bordered cells, span-aware.

      spec: a TableSpec (Framework_PYQPrepare S1-8a) — ANCHOR CELLS ONLY, with
            'cs' / 'rs' — or, for backward compatibility, the legacy positional
            call build_di_table_styled(doc, headers, rows).
      DO NOT use npm docx package for DI — cannot produce styled Word tables.
      """
      from docx.shared import Pt, RGBColor
      from docx.oxml import parse_xml
      from docx.oxml.ns import qn
      from docx.enum.text import WD_ALIGN_PARAGRAPH

      NAVY = DI_HEADER_COLOR  # v5.6: configurable (default "1F4E79")
      W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
      BORDER = (
          f'<w:tcBorders xmlns:w="{W}">'
          '<w:top    w:val="single" w:sz="6" w:color="000000"/>'
          '<w:left   w:val="single" w:sz="6" w:color="000000"/>'
          '<w:bottom w:val="single" w:sz="6" w:color="000000"/>'
          '<w:right  w:val="single" w:sz="6" w:color="000000"/>'
          '</w:tcBorders>'
      )
      if rows is not None:                      # legacy positional form
          spec = {'headers': spec, 'rows': rows}
      spec = corpus_io.normalise_table_spec(spec)
      header_rows = int(spec.get('header_rows', 1))

      # Data cells keep the v2.0 rule: numeric centred, text left. Header cells are
      # centred. Resolved BEFORE the build so the shared builder applies it.
      for ri, row in enumerate(spec['grid']):
          for cell in row:
              if cell.get('align'):
                  continue
              if ri < header_rows:
                  cell['align'] = 'center'
                  cell['bold'] = True
              else:
                  try:
                      float(str(cell.get('t', '')).replace(',', ''))
                      cell['align'] = 'center'
                  except ValueError:
                      cell['align'] = 'left'

      table = corpus_io.build_di_table(doc, spec, font_pt=FONT_SIZE_PT,
                                       default_align='center', font_name=FONT_NAME)

      # Header fill + white bold text, EVERY tier, merged anchors included. The
      # pre-v5.32 loop walked table.rows[0].cells, which under a merge returns one
      # entry per GRID COLUMN and repeats the anchor — it would have shaded the same
      # cell four times and never touched tier 2.
      # A raw <w:tr>/<w:tc> walk visits every cell EXACTLY ONCE: a horizontally
      # merged cell exists only as its anchor, and a vertically merged one has a
      # continuation tc that must be shaded too. Do NOT dedupe on id(tc) — lxml
      # creates a fresh proxy per findall() and Python reuses ids after GC, which
      # silently skips real cells.
      for tr in table._tbl.findall('{%s}tr' % W)[:header_rows]:
          for tc in tr.findall('{%s}tc' % W):
              tc.get_or_add_tcPr().append(parse_xml(
                  f'<w:shd xmlns:w="{W}" w:val="clear" w:color="auto" w:fill="{NAVY}"/>'))
      for ri, row in enumerate(table.rows):
          if ri >= header_rows:
              break
          for cell in row.cells:
              for para in cell.paragraphs:
                  para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                  for run in para.runs:
                      run.bold = True
                      run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                      run.font.size = Pt(FONT_SIZE_PT)

      # Borders on every cell (the raw walk visits each tc exactly once).
      for tr in table._tbl.findall('{%s}tr' % W):
          for tc in tr.findall('{%s}tc' % W):
              tc.get_or_add_tcPr().append(parse_xml(BORDER))
      return table
  ```

  Table structure in document:
    (1) Intro paragraph (bold): "Study the following table and answer the question."
    (2) build_di_table_styled(doc, spec)   # TableSpec, or legacy (headers, rows)
    (3) Question paragraph (bold): "Which of the following is correct?"
    (4) Options 1./2./3./4. (configured font, configured size, normal weight)
    (5) Blank separator paragraph

## S8-5 — DI chart generator (v5.33 — was an EMPTY TITLE from v1.0 to v5.32)

  D-8. This section carried a heading and no body for the life of the spec,
  while S8-5 was the documented home of the DI chart path and line 5576 called
  `insert_chart_image()` — a function defined nowhere in the corpus (D-7).
  A DI chart is a `data_series` or `data_single` figure under S10-6A and renders
  through `figural_core`, exactly like any other data figure.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  import figural_core as fc

  def build_di_chart(doc, qnum, chart, *, role="stim"):
      """
      chart : {'kind': 'line'|'bar'|'scatter'|'pie',
               'series': [{'label':..., 'x':[...], 'y':[...]}, ...],
               'axes'  : {'x': {'title':..., 'units':...},
                          'y': {'title':..., 'units':...}},
               'stem'  : ...,  'options': [...]}   # v5.80 Q7b.13 (optional keys;
                                                   # absent == not colour content)
      Returns the FigureSpec, having emitted the image into `doc`.
      """
      n = len(chart["series"])
      cls = "data_series" if n >= 2 else "data_single"
      spec = fc.make_figure_spec(qnum, cls, fc.FIG_PROBLEM_DISPLAY_IN,
                                 series=fc.series_defaults(n),
                                 axes=chart.get("axes", {}),
                                 key_mode="legend" if n >= 2 else "none",
                                 role=role,
                                 colour_content=fc.colour_is_content(
                                     chart.get("stem", ""), chart.get("options", ())))
      for s, src in zip(spec["series"], chart["series"]):
          s["label"] = src["label"]

      def draw(ax, series, palette):
          for s, src in zip(series, chart["series"]):
              if chart["kind"] == "bar":
                  ax.bar(src["x"], src["y"], color=s["colour"],
                         edgecolor="black", linewidth=0.8, label=s["label"])
              elif chart["kind"] == "scatter":
                  ax.scatter(src["x"], src["y"], color=s["colour"],
                             marker=s["marker"], label=s["label"])
              elif chart["kind"] == "pie":
                  # Q7b.4 — direct on-mark labels; a legend alone is prohibited.
                  ax.pie(src["y"], labels=src["x"], colors=palette[:len(src["y"])],
                         wedgeprops={"edgecolor": "black", "linewidth": 0.8})
              else:
                  ax.plot(src["x"], src["y"], color=s["colour"],
                          linestyle=s["linestyle"], marker=s["marker"],
                          label=s["label"])
          if chart["kind"] != "pie":
              ax.set_xlabel(_axis_label(chart, "x"))     # Q9.2 — title + units
              ax.set_ylabel(_axis_label(chart, "y"))
              if len(series) >= 2:
                  ax.legend()

      png = f"q{qnum}_{role}.png"                        # Q8 canonical name
      fc.render_figure(draw, png, spec)
      fc.write_spec_sidecar(spec, png)
      insert_chart_image(doc, png, spec)
      return spec

  def _axis_label(chart, k):
      a = (chart.get("axes") or {}).get(k) or {}
      t, u = a.get("title", ""), a.get("units")
      return f"{t} ({u})" if t and u else t

  def insert_chart_image(doc, png_path, spec):
      """D-7: referenced at S10-6 since v1.0, defined nowhere until v5.33.
      Placement and alt text go through the ONE S10-8 path so the chart route
      cannot drift from the figural route — the drift between two uncontracted
      figure paths is what this gap was."""
      with open(png_path, "rb") as fh:
          _add_image_para(doc, fh.read(), spec["placed_in"], spec=spec)
  ```

## S8-6 — FIGURAL generator (v4.0 — decomposed; see S7-NEW-B + §10-S10-7/S10-8)

  A figural question is generated and emitted as DISCRETE images, never a
  composite panel. The generator:
    1. Builds geometry vector-first (honouring the S10-7C drawing contract) and
       renders the problem figure via figural_core.render_figure() and the WHOLE
       OPTION SET via figural_core.render_option_set() (§10-S10-7 Q12) — one PNG
       for the problem/series figure(s); one PNG per option, all options on one
       uniform canvas in one shared data window; all at FIGURAL_DPI=300,
       lossless, no baked-in question text, reference lines drawn as real
       geometry, and the border box drawn by the RENDERER (Q10.4), never by
       draw_fn. v5.55: rendering an option set by looping the single-figure
       helper is a G-FIGOPTWINDOW defect.
       v5.90 (GAP-2026-11-03 G01 R1.2 + owner Q-A) — TWO CHECKS AT RENDER, BEFORE
       ANY PIXEL: (i) G-OPTDISTINCT — corpus_io.native_option_set and
       figural_core.render_option_set both call assert_option_identities(draws):
       two draws whose RE-PERCEIVED identity (bc.structure_identity /
       bc.reaction_identity of .canonical) is equal raise OptionIdentityError /
       FiguralError "LADDER-REPAIR R2o G-OPTDISTINCT: options i and j are ONE
       entity" — catch it, enter §Q8b-LADDER at R2o (regenerate THAT distractor,
       never the key; the (2E,4Z)/(2E,4Z) pair of the incident's Q32 is exactly
       this). Store the returned identities as quality['option_identities'].
       (ii) G-STEREODECL — every structure draw carries the author's intent:
       cio.stereo_declared(draw_fn, '2E,4Z' | '(2R,3S)' | 'none'); then
       v = bc.stereo_declaration_check(draw_fn.canonical, draw_fn.stereo_declared):
       FAIL -> "LADDER-REPAIR R2o G-STEREODECL: SMILES encodes X; declared Y" (the
       author mis-wrote a directional / chiral SMILES — the Q32 MECHANISM, which
       no duplicate check can see when it hits the KEY); WARN (undeclared) is
       recorded, never a block (OD-1). Record v on the semantic object as
       stereo_declared (S7-NEW-B2) so A-STEREODECL recomputes it.
       (iii) CONFORMER / PROJECTION SETS (release review) — an option set that is the
       SAME molecule drawn as chair / Newman / Fischer / Haworth / sawhorse by design
       (figure_types.identity_kind is None for those hand-drawn types) is NOT a
       duplicate set: build each such draw with cio.structure_draw_fn(...,
       conformer_set=True) (or cio.identity_exempt(draw_fn) on a hand-drawn draw)
       BEFORE the set renders; assert_option_identities skips exempt draws and the
       reviewer decides (dHash may WARN). Never exempt an rdkit-drawn skeletal set.
    2. Places them via add_figural_question() (§10-S10-8): Q.N-first stem text,
       the problem image(s), then the N option images stacked SINGLE-COLUMN, each
       bound 1:1 to its "i." label (one option image per line; never two on a
       line, never a table row of options).
    3. Records the question in the figural manifest; the per-block image count
       (≥ n_options + 1) and one-image-per-option-line invariant are enforced by
       G-FIGURAL-COMPOSITE (S12-NEW-13). LADDER-REPAIR R1 [HS:LADDER] on a single-image (composite)
       figural block or any multi-image line.

## S8-7 through S8-9 — (unchanged from v1.0)

# ════════════════════════════════════════════════════════════════════════
# §9 — SELF-CONTAINMENT ARCHITECTURE (v3.6 — FULL REWRITE; was a v1.0 stub)
# ════════════════════════════════════════════════════════════════════════
#
# WHY THIS SECTION EXISTS (the M1 defect it prevents):
#   The mock docx is consumed by an ONLINE test-series engine that renders ONE
#   question per screen. The student never sees the surrounding page. Therefore a
#   question is only valid if EVERYTHING needed to answer it travels INSIDE that
#   question's own block. A shared stimulus placed once, before the first question
#   of a group, is invisible to every later question in that group → those
#   questions become unanswerable online. Mock 1 shipped exactly this defect for
#   Q74-75 (DI table), Q85-88 (Cloze), Q92-94 (RC). §9 makes it impossible.

## SC-1 — The self-containment invariant (applies to ALL questions)

  A question Q is SELF-CONTAINED iff a student shown ONLY Q's block (stem +
  options + any attached stimulus/figure/table) — with zero access to any other
  question or to any lead-in text — has everything required to select the answer.
  Single (non-linked) questions are self-contained by construction. Linked-group
  questions are the risk surface and are governed by SC-2..SC-7.

## SC-2 — What counts as a "shared stimulus" (CLASS 4 detection → §6)

  A shared stimulus is any block of content that ≥2 questions depend on:
    - RC / reading-comprehension PASSAGE (prose paragraph[s]).
    - CLOZE passage (a paragraph with numbered blanks (1),(2),(3)...).
    - DI dataset rendered as a Word TABLE, bar/pie/line CHART image, or caselet.
    - PUZZLE / arrangement clue-set (seating, scheduling, blood-relation chain).
    - Any "Study the following ... and answer Q.X to Q.Y" preamble.
  Detection is inherited from §6 CLASS 4 and the blueprint's linked_group_id /
  passage_linked_qs / cloze_linked_qs / di_linked_qs allocations. Every member
  question of a group carries the same linked_group_id in the answer_key sidecar
  and concept_map (already persisted per §11).

## SC-3 — DELIVERY CONTRACT: Model A (DEFAULT) — stimulus duplicated per member

  For every linked group, by default emit the stimulus INSIDE EACH member
  question's block. EACH member block opens with its Q-number (v3.7 Q.N-FIRST)
  and is laid out in this FIXED 5-line order:

    For each member q in group (in ascending Q-number order):
      1. Q.N CONTEXT LINE (bold) — the Q-number FUSED with the shared context /
         instruction, e.g.
           "Q.74  Study the following table and answer the question. The table
            shows the number of units (in thousands) of four products P, Q, R
            and S sold by a company in three years."
           "Q.85  In the following passage, some words have been deleted. Each
            blank is indicated by a number (1), (2), (3) and (4). Read the
            passage and select the most appropriate option for the indicated
            blank."
           "Q.92  Read the following passage and answer the question."
         Use the SINGULAR "question" — each screen shows one Q; NEVER write
         "questions Q.74 and Q.75" inside a per-member block (that re-introduces
         cross-question dependence and is banned by G-STIMULUS-ORPHAN).
         NOTHING may precede this line — no loose preamble, no table, no passage.
      2. THE EMBEDDED STIMULUS (immediately after the Q.N line):
         - PASSAGE / CLOZE → the complete passage paragraph(s) (identical text in
           every member; for Cloze, the SAME numbered-blank paragraph each time).
         - DI TABLE → a fresh Word-table object built by build_di_table_styled()
           (§8-S8-4) — re-emit the table in each member, WITH ITS SPANS (v5.32);
           never reference "the table above".
         - DI CHART → the same chart image (re-insert the image part per member;
           image-reuse ban R3 does NOT apply within a single linked group —
           see SC-6).
      3. THE SPECIFIC ASK (bold, NON-numbered paragraph) — the actual question
         for this member, e.g. "What is the total number of units (in thousands)
         of product R sold over the three years?" / "Select the most appropriate
         option for blank number (1)." / "The word 'industrious', as used in the
         passage, most nearly means:". This paragraph does NOT carry a Q-number
         (the block's single Q-number already opened it in line 1).
      4. OPTIONS (per OPTION_LABEL_FMT; default "1.  2.  3.  4.") (normal weight).
      5. BLANK SEPARATOR paragraph.

  RESULT (illustrative, using SSC CGL T1 reference Q numbers — actual Q numbers
  come from the blueprint for each exam): Q.74 opens with the context line +
  carries the table + asks the R-total;
  Q.75 opens with the SAME context line + the SAME table + asks the P-percentage;
  Q.85..Q.88 each open with the cloze instruction + the full cloze passage + one
  blank's ask; Q.92..Q.94 each open with the RC instruction + the full passage +
  one ask. Every block STARTS with "Q.<N>" and is answerable in isolation.

  This is the SAFE DEFAULT for ANY importer, because it assumes no group support
  in the engine. When in doubt, use Model A.

## SC-4 — DELIVERY CONTRACT: Model B (CONDITIONAL) — engine-native passage group

  Model B emits the stimulus ONCE and binds the member questions to it via the
  engine's comprehension/passage-group container, so the engine itself pins the
  stimulus on every member screen. Use Model B ONLY when ALL of these hold:
    (a) The target platform is CONFIRMED at S3 to support passage/comprehension
        groups on import (recorded as delivery.linked_mode = "group" in the
        session config). If unknown or unconfirmed → fall back to Model A.
    (b) The import format carries an explicit group binding (e.g. a shared
        passage_id / group_id column the importer maps). A loose lead-in
        paragraph is NOT a binding and never qualifies.
  When Model B is active, the docx still must make the grouping machine-evident:
  precede the group with one preamble paragraph tagged "[GROUP n: Q.X–Q.Y]" on
  its OWN line (this is the ONLY permitted shared-once layout, and only under
  confirmed Model B). Absent confirmation, this layout is BANNED by R-LINKED.

  DEFAULT RESOLUTION: delivery.linked_mode defaults to "embed" (Model A). It is
  set to "group" only by an explicit, recorded S3 confirmation. No silent Model B.

## SC-5 — Cloze-specific self-containment

  A Cloze passage has numbered blanks (1)..(k) and one question per blank. Under
  Model A each member question re-prints the WHOLE blanked paragraph and then asks
  for ONE specific blank ("Select the most appropriate option for blank number
  (n)."). The full paragraph (all blanks shown) must appear in every member so the
  student has full sentence context for the blank in view. Never strip the other
  blanks; never show only the target sentence.

## SC-6 — Image / table reuse exemption WITHIN a linked group

  R3 (no image reused across any two questions) and dedup of identical tables are
  CROSS-QUESTION integrity rules aimed at distinct questions. They DO NOT apply to
  the intentional re-emission of ONE group's shared stimulus across its OWN member
  questions — that re-emission is the format, not a duplicate. Implementation note:
  tag each re-emitted stimulus part with the group's linked_group_id so the dHash/
  MD5 dedup (§7) and G-DELIVERY checks skip intra-group repeats. Cross-group and
  cross-mock stimulus reuse remains banned (see Analyse §recycled_datasets).

## SC-7 — Self-containment self-check (run during S4-7 STEP A, per batch)

  For every question written in the batch:
    if q.linked_group_id is not None:
        assert stimulus_object_present_in_block(q), \
          f"R-LINKED: Q.{q.num} is a linked member with no embedded stimulus."
    # also catch accidental cross-references in single questions:
    assert not stem_references_absent_stimulus(q), \
          f"R-LINKED: Q.{q.num} references a stimulus not in its own block."
  stem_references_absent_stimulus() = stem matches any of
    {"the passage", "the table", "the graph", "the chart", "the given data",
     "blank (", "according to the passage", "Q\\.\\d+ (and|to) Q\\.\\d+"}
  AND no passage paragraph / Word table / chart image is attached to that
  question's block. Any failure is fixed IN THIS BATCH before gate check; it is
  also re-verified mock-wide at Final Assembly by gate G-STIMULUS-ORPHAN (§12).

  CONTEXT STORE / progress.json persistence (passage_linked_qs, cloze_linked_qs,
  di_linked_qs, and each group's stimulus text/table/image) is written per S4-8b
  so a resumed session re-embeds the IDENTICAL stimulus into later members.

# ════════════════════════════════════════════════════════════════════════
# §10 — OUTPUT FORMAT & DOCX CONSTRUCTION (v2.0 — FONT + OPTION FIXES)
# ════════════════════════════════════════════════════════════════════════

## S10-0 — MANDATORY: per-question concept_map capture (v5.52, GAP-2026-08-12-S10-CONCEPTMAP-MANDATE)

  Every question this step authors MUST have its `subtopic_id` and `difficulty`
  captured via write_q_to_sidecar() (§S7-NEW-A) — NOT optional, NOT deferred to
  a later batch, NOT left to a default. These two fields are the ONLY source
  registry.question_index draws from at Final Assembly (S13-4), and G-QINDEX
  (S13-QINDEX) hard-stops on a mock whose distribution does not EXACTLY match
  difficulty_schedule[N] (Contract_QuestionMetadataIndex v1.0).

  WHY THIS IS HERE, NOT ONLY AT S7-NEW-A: the producer's obligation to compute a
  difficulty label was previously documented only in `Framework_Blueprint.md
  §S7-6` (Step 2's contract) and the mechanics of storing it only in §S7-NEW-A
  (this spec's sidecar-write helper) — with no explicit instruction, in THIS
  spec's own per-question-authoring section, telling an implementer that
  omitting it is forbidden. An implementer who read S10 in isolation (as
  Mock 10's batch-authoring scripts effectively did) had no local signal that
  concept_map needed populating at all, until — if the Final-Assembly gate
  happened to run — a HARD STOP [HS:PROSE] arrived hundreds of questions later.

  THE STRUCTURAL BACKSTOP (v5.52): §S7-NEW-A's write_q_to_sidecar() no longer
  defaults subtopic_id/difficulty to None. Omitting either now raises
  TypeError at the call site — the moment the question is authored — instead
  of silently writing `null` to the sidecar. Treat that TypeError as the
  contract working as designed, not a bug to code around: it means a
  subtopic_id or difficulty value was never computed for that question, and
  that must be fixed before the question is accepted, not patched around by
  passing a placeholder.

  This does not change WHAT was already required (§S7-NEW-A's docstring has
  documented these two fields since v5.2) — it makes the requirement
  impossible to silently skip, and states it where the per-question authoring
  work actually happens.

## S10-1 — Question format rules (v2.0 GAP-14 + GAP-15 fixes)

  FONT MANDATE (configured font — non-negotiable):
    ALL text in docx: FONT_NAME, FONT_SIZE_PT (read from exam_config / blueprint
    at S3-2; defaults Calibri 11 if not configured).
    Stem paragraphs: configured font, configured size, BOLD.
    Option paragraphs: configured font, configured size, normal weight.
    Continuation paragraphs (add_stem_ml): configured font, configured size.
    Fonts in FONT_BANNED are EXPLICITLY BANNED (default: Arial, unless Arial IS
    the configured font).

    PRE-DELIVERY FONT CHECK:
    ```python
    # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
    def verify_configured_font(docx_path):
        from docx import Document
        doc = Document(docx_path)
        for para in doc.paragraphs:
            for run in para.runs:
                if run.font.name and run.font.name.lower() not in [FONT_NAME.lower(), '']:
                    print(f"FONT FAIL: run '{run.text[:30]}' uses '{run.font.name}'"
                          f" (expected '{FONT_NAME}')")
                    return False
        return True
    ```

  OPTION LABEL FORMAT (configured — v5.6):
    All option labels rendered by OPTION_LABEL_FMT (S3-2; default "{i}.  {text}").
    Gate G-OPTLABEL matches OPTION_LABEL_RE (built from the configured format).
    Correct format: OPTION_LABEL_FMT.format(i=i, text=option_text)

  BLANK SEPARATOR: one blank paragraph (add_paragraph()) after every Q's options.
  Q-NUMBER FORMAT: Q.<N>  [stem text] — dot between Q and number, two spaces.

  MULTI-PART STEMS (v5.79): a stem with >=2 enumerated sub-parts renders ONE
    BOLD continuation paragraph per sub-part via add_stem_multipart (S10-2b).
    Sub-part labels obey the S10-2b LABEL LAW — never the Q-number shape, never
    this exam's own option scheme in any spacing, never bare digit-dot/digit-paren.

## S10-2 — UNDERLINE-SPAN CONTRACT (v4.1 — executable; replaces the v1.0 stub)

  A question that asks about an UNDERLINED span must render that span as a REAL
  underlined run inside the sentence — never as a parenthetical text annotation.
  This is the executable home of R-UNDERLINE. The v1.0 one-liner ("run.underline
  = True. NEVER underscores.") stated the goal but gave no trigger, no helper, and
  no ban; with only the single-run add_question_stem() available, the generator
  fell back to appending "(underlined: X)" as plain text and the underline rule
  never executed. Both gaps are closed here.

  WHEN UNDERLINE IS REQUIRED (UNDERLINE_TRIGGER):
    A block needs a real underlined span if EITHER holds:
      · stem_format_variant == 'sentence_embedded_underlined', OR
      · the stem/instruction refers to an underlined element — regex (case-insens.):
          r"underlin(e|ed)\s+(word|words|part|segment|phrase|portion|sentence)"
          OR r"the\s+underlined\b"
    Covers: Antonym/Synonym "of the underlined word", sentence IMPROVEMENT
    ("improve the underlined part of the sentence"), error-spotting on an
    underlined segment, and any future template that points at an underlined span.

    ```python
    import re
    UNDERLINE_TRIGGER_RE = re.compile(
        r"(?i)underlin(?:e|ed)\s+(?:word|words|part|segment|phrase|portion|sentence)"
        r"|the\s+underlined\b")   # single (?i) at start covers both alternatives

    def underline_required(stem_text, stem_format_variant=None):
        return (stem_format_variant == 'sentence_embedded_underlined'
                or bool(UNDERLINE_TRIGGER_RE.search(stem_text or "")))
    ```

  HOW TO RENDER (the helper the generator MUST call — never hand-roll the stem):
    Split the carrier sentence into THREE parts around the target span and underline
    ONLY the middle run. The instruction line and the carrier sentence are bold per
    R13; underline is layered on the target run on top of bold.

    ```python
    # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
    from docx.shared import Pt

    def add_stem_with_underline(doc, qnum, instruction, pre, target, post,
                                bold=True):
        """
        Renders an underline-class stem as:
          "Q.<qnum>  <instruction>"   (bold)            — e.g. the task line
          "<pre><TARGET underlined><post>"  (bold; TARGET also underlined)
        `pre`/`post` may be "" (target at start/end). NEVER pass the target as a
        bracketed note. Two paragraphs keep the instruction and the carrier
        sentence on separate lines, matching the reference exam layout.
        """
        assert target and target.strip(), "underline target span must be non-empty"
        # 1) instruction line (Q.N-first, R14)
        p1 = doc.add_paragraph()
        r1 = p1.add_run(f"Q.{qnum}  {instruction}")
        r1.bold = bold; r1.font.name = FONT_NAME; r1.font.size = Pt(FONT_SIZE_PT)
        # 2) carrier sentence with the underlined target span
        p2 = doc.add_paragraph()
        for chunk, is_target in ((pre, False), (target, True), (post, False)):
            if chunk == "":
                continue
            r = p2.add_run(chunk)
            r.bold = bold
            r.underline = is_target          # REAL <w:u> on the target run only
            r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
        return p1, p2
    ```

    For a single-line stem (no separate instruction, e.g. error-spotting where the
    whole sentence is the stem), pass instruction="" and the helper emits only the
    carrier paragraph as the Q.N-first line — fuse "Q.<qnum>  " into `pre`.

  BANNED (R-UNDERLINE; G-UNDERLINE will Exit 1 on any of these):
    · "(underlined: senior than me)"  · "(underline: benevolent)"
    · "(underlined word: X)"  · any bracketed/quoted note naming the target in
      place of underlining it
    · underscore runs ("____") or markdown "_x_" / "<u>" text as a fake underline
    Correct  →  the words "senior than me" appear with run.underline = True INSIDE
                the sentence "He is senior than me by three years."
    Incorrect → "He is senior than me by three years. (underlined: senior than me)"

  VERIFY (audit hook): has_underlined_span(block) returns True iff some run in the
  block carries w:u. G-UNDERLINE (S12-NEW-14) and the §7 render-consistency
  contract both call it; see S12-NEW-14 for the run-level XML check.

  CARRIER-SENTENCE LAYOUT (v4.2 — generalised from underline to all such stems):
  Any stem that contains a CARRIER SENTENCE the candidate must read — underline
  questions, error-spotting ("select the part that contains the error"),
  sentence-improvement ("improve the underlined/bracketed part"), fill-in-the-
  sentence — emits the INSTRUCTION line and the SENTENCE as SEPARATE paragraphs:
      (1) "Q.<N>  <instruction>"            (bold; Q.N-first, R14)
      (2) "<the carrier sentence>"          (bold; its own paragraph)
      then options. NEVER concatenate the instruction and the sentence into one
  run/paragraph (the M1 Q.100 run-on "…select the last option.Each of the
  students…"). add_stem_with_underline already does this; add_carrier_sentence_stem
  is the non-underline equivalent:
    ```python
    # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
    def add_carrier_sentence_stem(doc, qnum, instruction, sentence, bold=True):
        p1 = doc.add_paragraph(); r1 = p1.add_run(f"Q.{qnum}  {instruction}")
        r1.bold = bold; r1.font.name = FONT_NAME; r1.font.size = Pt(FONT_SIZE_PT)
        p2 = doc.add_paragraph(); r2 = p2.add_run(sentence)
        r2.bold = bold; r2.font.name = FONT_NAME; r2.font.size = Pt(FONT_SIZE_PT)
        return p1, p2
    ```

## S10-2b — MULTI-PART STEM LAYOUT CONTRACT (v5.79 — estate-wide, exam-agnostic)

  WHAT QUALIFIES. A stem that presents TWO OR MORE enumerated sub-parts as a
  series — reagent/procedure sequences, test or observation lists, statement
  sets, sentences-to-arrange, assertion–reason pairs, or any other labelled
  enumeration — where the sub-parts are NEITHER the option set NOR the lists
  of a MATCH question.

  LAYOUT (the S10-2 no-run-on principle, generalised):
    1. Q.N-FIRST paragraph: lead-in/context, PLUS the MSQ select-instruction or
       NAT numerical-entry instruction INSIDE this paragraph when applicable
       (R14; G-MSQ-INSTR / G-NAT-INSTR — both anchors unchanged by this section).
    2. ONE BOLD continuation paragraph PER sub-part, in order, configured
       font/size (S10-1), rendered via add_stem_multipart (S10-3).
    3. OPTIONAL closing-ask paragraph (bold) after the series. CANONICAL for
       NAT count-the-series stems: context + instruction on the Q.N line, then
       the sub-parts, then the closing ask — natural reading order preserved
       while the instruction stays anchored to Q.N.
    4. Options (if any) follow per R13; blank separator per G-BLANK.
    LINKED (CLASS-4) blocks: sub-parts that belong to the specific ask are
    emitted AFTER the non-numbered ask paragraph, inside the §9 Model A order.
    FIGURAL blocks: sub-part paragraphs are document text and PRECEDE the
    problem image(s).

  LABEL LAW (the load-bearing rule — exam-agnostic and spacing-insensitive):
    (a) A sub-part line NEVER opens with the Q-number shape (Q + '.' + digits,
        any spacing). G-QNUM-FIRST guarantees exactly one Q.N paragraph per
        block; this law keeps continuation lines invisible to that anchor.
    (b) A sub-part line NEVER matches THIS exam's own option-label scheme,
        tested SPACING-INSENSITIVELY. Spacing must never decide safety: a
        one-space digit-dot evades a strict two-space OPTION_LABEL_RE while the
        two-space form collides, and S12-NEW-2 flags the near-miss as a
        malformed option. The test therefore strips ALL whitespace and compares
        against the labels this exam ACTUALLY renders (_option_label for
        positions 1..9) — numeric, alpha, roman or custom, nothing hardcoded.
    (c) Bare digit-dot / digit-paren openings ("1.", "1)", "(1)") are BANNED in
        sub-part lines under EVERY exam regardless of the configured scheme:
        numeric families are the most common option scheme in the estate and
        the near-miss spacings are ambiguous to every downstream consumer. A
        sub-part whose content begins with a number ("2.5 g of NaOH ...") must
        therefore carry its label first ("(ii) 2.5 g of NaOH ...").
    (d) SAFE-LADDER selection (authoring guidance; label style stays free per
        question within the law): prefer "(i)/(ii)/(iii)" roman-in-parens, then
        "(A)/(B)/(C)" alpha-in-parens, then "A./B./C." alpha-dot, then worded
        labels ("Step 1:", "Test 1:") — SKIPPING any rung that (b) rejects for
        THIS exam. On a numeric-option exam all four rungs are safe; on a
        roman-option exam rung 1 is skipped; on an alpha-option exam rungs 2–3
        are skipped. The helper enforces (a)-(c) mechanically; (d) is a choice.

  ENFORCEMENT MAP (four independent layers — any one alone stops a breach):
    1. AUTHORING RAISE: add_stem_multipart validates every sub-part line AND
       the optional closing ask against (a)-(c), and rejects empty sub-part
       lines, RAISING before any paragraph exists. A colliding paper cannot
       be BUILT.
    2. EXISTING GATES (unchanged): G-QNUM-FIRST, G-OPTLABEL, G-NAT-NOOPT, R4
       option counts, K-INT — a breach that somehow rendered would hard-fail
       STEP B before present_files (B-7).
    3. CHECKLIST: S4-11 item G-STEM-SUBPART, every batch, Layer 1 (no auditor
       twin — joins the checklist-only items; the auditor's block/option
       parsers are unaffected by construction and need no new gate).
    4. DOWNSTREAM CONTRACTS (unchanged, pass-through): Step 9 RE-3 /
       verify_fidelity and Step 11's byte-identical tagger propagate the layout
       untouched; MockDeliver §2 already documents multi-paragraph stems.

  SCOPE. Applies to every paper this spec authors (mock + scoped, every exam)
  from v5.79 onward. FORWARD-ONLY: already-delivered papers keep their layout
  (downstream fidelity gates make it permanent by design). The PYQ flow is
  UNTOUCHED by operator scope ruling — Row-file layout is PYQPrepare's
  contract, not this spec's.

## S10-3 — Python helpers (v2.0 — Calibri enforced)

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  from docx import Document
  from docx.shared import Pt
  from docx.oxml import parse_xml

  def add_question_stem(doc, qnum, stem_text, bold=True, msq_instruction=None):
      # v4.5: for MSQ (answer_cardinality=='multi') the select-instruction is appended INSIDE
      # this single bold Q.N-first paragraph (R14 / G-QNUM-FIRST — there is NO paper-
      # level instructions page, and a separate instruction paragraph would break R14).
      # msq_instruction is the localized phrase from section_rules (msq_instruction_for);
      # None for single-answer questions ⇒ byte-identical to v4.4.
      text = f"Q.{qnum}  {stem_text}"
      if msq_instruction:
          text = f"{text}  {msq_instruction}"
      p = doc.add_paragraph()
      run = p.add_run(text)
      run.bold = bold
      run.font.name = FONT_NAME         # v5.6: configurable
      run.font.size = Pt(FONT_SIZE_PT)  # v5.6: configurable
      return p

  def msq_instruction_for(section_rules_text, language='english'):
      # EXAM-AGNOSTIC + localized: prefer the exam's own phrasing from section_rules
      # (field msq_instruction, optionally msq_instruction_hi for Hindi/bilingual); fall
      # back to a universal default. The phrase is parenthesised so it reads as an
      # instruction within the stem line.
      import re as _re
      key = 'msq_instruction_hi' if language in ('hindi', 'bilingual') else 'msq_instruction'
      m = _re.search(rf'^\s*{key}\s*:\s*(.+?)\s*$', section_rules_text or '', _re.M)
      phrase = m.group(1).strip() if m else None
      if not phrase:
          phrase = ('(एक या अधिक विकल्प सही हो सकते हैं)'
                    if language in ('hindi', 'bilingual')
                    else '(One or more options may be correct)')
      return phrase if phrase.startswith('(') else f'({phrase})'

  def _option_label(i, fmt=OPTION_LABEL_FMT):
      """Render the label for option i (1-based) using the configured format."""
      _ROMAN = ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x')
      _r = _ROMAN[i - 1] if 1 <= i <= len(_ROMAN) else str(i)
      return fmt.format(
          i=i, text='{text}',
          alpha_upper=chr(ord('A') + i - 1),
          alpha_lower=chr(ord('a') + i - 1),
          roman_upper=_r.upper(),          # v5.37 — roman is RENDERED, not aliased
          roman_lower=_r
      ).replace('{text}', '').strip()

  def add_text_options(doc, options):
      for i, opt in enumerate(options, 1):
          p = doc.add_paragraph()
          lbl = _option_label(i)
          label = f"{lbl}  {opt}" if not lbl.endswith(' ') else f"{lbl}{opt}"
          run = p.add_run(label)
          run.bold = False
          run.font.name = FONT_NAME         # v5.6: configurable
          run.font.size = Pt(FONT_SIZE_PT)   # v5.6: configurable

  def add_blank_separator(doc):
      doc.add_paragraph()

  def add_stem_ml(doc, text, bold=False):
      p = doc.add_paragraph()
      run = p.add_run(text)
      run.bold = bold
      run.font.name = FONT_NAME
      run.font.size = Pt(FONT_SIZE_PT)
      return p

  def _subpart_label_violation(line):
      """S10-2b LABEL LAW (a)-(c) test for ONE sub-part line. Returns a reason
      string on violation, None when the line is safe. EXAM-AGNOSTIC: (b)
      renders THIS exam's own labels via _option_label — numeric, alpha, roman
      or custom — and compares with ALL whitespace stripped, so spacing can
      never decide safety."""
      import re as _re
      if _re.match(r'^\s*Q\s*\.\s*\d+', line):
          return "LABEL LAW (a): sub-part opens with a Q-number shape"
      if _re.match(r'^\s*\(?\d+\s*[\.\)]', line):
          return "LABEL LAW (c): bare digit-dot/digit-paren label (banned under every exam)"
      probe = _re.sub(r'\s+', '', line)
      for i in range(1, 10):
          try:
              lbl = _re.sub(r'\s+', '', _option_label(i))
          except Exception:
              break
          if lbl and probe.startswith(lbl):
              return ("LABEL LAW (b): sub-part opens with this exam's own "
                      f"option label {_option_label(i)!r} (spacing-insensitive)")
      return None

  def add_stem_multipart(doc, qnum, lead_in, subparts, closing_ask=None,
                         msq_instruction=None, nat_instruction=None):
      """S10-2b renderer (v5.79). Q.N-first lead-in with the MSQ/NAT
      instruction INSIDE it (R14 anchors), then ONE BOLD paragraph per
      already-labelled sub-part, then the optional closing ask. RAISES at
      authoring on any LABEL LAW breach — a colliding paper cannot be built
      (S10-2b enforcement layer 1)."""
      if len(subparts) < 2:
          raise ValueError("S10-2b: add_stem_multipart requires >=2 sub-parts; "
                           "use add_question_stem/add_stem_ml for plain stems")
      instr = msq_instruction or nat_instruction
      p0 = add_question_stem(doc, qnum, lead_in, msq_instruction=instr)
      for line in subparts:
          if not line or not line.strip():
              raise ValueError("S10-2b: empty/whitespace-only sub-part line — "
                               "always an authoring error, never rendered")
          reason = _subpart_label_violation(line)
          if reason:
              raise ValueError(f"S10-2b {reason}: {line[:48]!r}")
          add_stem_ml(doc, line, bold=True)            # S10-1: sub-parts BOLD
      if closing_ask:
          reason = _subpart_label_violation(closing_ask)
          if reason:                                    # the ask is a stem line too
              raise ValueError(f"S10-2b (closing ask) {reason}: {closing_ask[:48]!r}")
          add_stem_ml(doc, closing_ask, bold=True)
      return p0

  def add_standard_question(doc, qnum, stem, options, answer_cardinality='single',
                            section_rules_text='', language='english'):
      # v4.5: dispatch on the subtopic's answer_cardinality (blueprint subtopic_list). For
      # 'multi', append the localized select-instruction to the Q.N stem line and record
      # msq_instr_in_stem=True for the sidecar (G-MSQ-INSTR). 'single' ⇒ unchanged.
      msq_instr = (msq_instruction_for(section_rules_text, language)
                   if answer_cardinality == 'multi' else None)
      add_question_stem(doc, qnum, stem, msq_instruction=msq_instr)
      add_text_options(doc, options)
      add_blank_separator(doc)
      return {'msq_instr_in_stem': bool(msq_instr)}   # caller forwards to write_q_to_sidecar

  def add_match_table(doc, qnum, instruction, columns, options,
                      answer_cardinality='single', section_rules_text='', language='english',
                      header_fill=None):
      """MANDATORY renderer for stem_format_variant == 'match_the_following' (§10-S10-3M).
      Renders a MATCH question as a REAL Word table grid — never plain text. Layout:
        (1) Q.N-first bold instruction paragraph (R14 / G-QNUM-FIRST; MSQ instruction in-stem);
        (2) a bordered Word table, one column per list (List-I | List-II | …): a header row
            plus one row per item. UNEQUAL columns are blank-padded (an extra List-II
            distractor renders as a row whose List-I cell is empty);
        (3) the pairing-quad options (e.g. 'A-I, B-III, …') via the standard option block;
        (4) blank separator (R13).
      columns : list of (header, [item, …]); each item already carries its own label
                ('(A) Collagen', 'I. triple helix', …). >=2 columns supported (List-III).
      options : the pairing-quad option texts.
      Exam-agnostic: headers, labels and the optional header_fill come from the caller — no
      hardcoded scheme. Emitting a match via add_standard_question() (lists as stem text) is
      BANNED — its grid renders as plain text: G-MATCH-TABLE, re-verified by audit.py
      A-MATCH-TABLE. Keeping the 'Match …' instruction in the Q.N paragraph (not inside the
      table) is what lets audit.py re-detect the MATCH axis and confirm the table is present.
      """
      from docx.shared import Pt, RGBColor
      from docx.oxml import parse_xml
      from docx.enum.text import WD_ALIGN_PARAGRAPH
      msq_instr = (msq_instruction_for(section_rules_text, language)
                   if answer_cardinality == 'multi' else None)
      add_question_stem(doc, qnum, instruction, msq_instruction=msq_instr)
      headers   = [str(h) for h, _ in columns]
      col_items = [[str(x) for x in items] for _, items in columns]
      ncols = len(headers)
      nrows = max((len(c) for c in col_items), default=0)
      BORDER = (
          '<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:top    w:val="single" w:sz="6" w:color="000000"/>'
          '<w:left   w:val="single" w:sz="6" w:color="000000"/>'
          '<w:bottom w:val="single" w:sz="6" w:color="000000"/>'
          '<w:right  w:val="single" w:sz="6" w:color="000000"/>'
          '</w:tcBorders>')
      table = doc.add_table(rows=1 + nrows, cols=ncols)
      # header row (bold; optional fill for a styled header)
      for ci, h in enumerate(headers):
          cell = table.rows[0].cells[ci]
          run = cell.paragraphs[0].add_run(h)
          run.bold = True
          run.font.name = FONT_NAME
          run.font.size = Pt(FONT_SIZE_PT)
          if header_fill:
              run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
              cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
              cell._tc.get_or_add_tcPr().append(parse_xml(
                  f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
                  f' w:val="clear" w:color="auto" w:fill="{header_fill}"/>'))
      # data rows (blank-pad short columns so unequal lists render correctly)
      for ri in range(nrows):
          for ci in range(ncols):
              items = col_items[ci]
              cell = table.rows[ri + 1].cells[ci]
              run = cell.paragraphs[0].add_run(items[ri] if ri < len(items) else '')
              run.font.name = FONT_NAME
              run.font.size = Pt(FONT_SIZE_PT)
      # borders on every cell
      for row in table.rows:
          for cell in row.cells:
              cell._tc.get_or_add_tcPr().append(parse_xml(BORDER))
      add_text_options(doc, options)
      add_blank_separator(doc)
      return {'msq_instr_in_stem': bool(msq_instr), 'rendered_match_table': True}
  ```

## S10-4 — OMML library (complete — see v1.0 for full implementation)

  TECHNOLOGY MANDATE (GAP-05 fix):
  The OMML helpers below REQUIRE python-docx. They CANNOT run in npm docx.
  If exam has any mathematical content → MUST use Python + python-docx.

  ```python
  from docx.oxml import parse_xml
  M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
  def _esc(t):
      return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
  def _r(t): return f'<m:r xmlns:m="{M}"><m:t xml:space="preserve">{_esc(t)}</m:t></m:r>'
  def _r_wrap(x):
      # v5.47 (MC1): raw text interpolated into m:num/m:den/m:e is SCHEMA-INVALID
      # OMML that Word renders as an EMPTY placeholder while itertext()-style
      # checks still read it (measured as GAP-2026-08-07-EXPLAIN-OMML). Every
      # builder argument now normalises here: OMML markup passes through, plain
      # text becomes a proper <m:r><m:t> run — a forgotten _r() can no longer
      # destroy content.
      x = '' if x is None else str(x)
      return x if x.lstrip().startswith('<m:') else _r(x)
  def frac(n,d): return f'<m:f xmlns:m="{M}"><m:num>{_r_wrap(n)}</m:num><m:den>{_r_wrap(d)}</m:den></m:f>'
  def sup(b,e): return f'<m:sSup xmlns:m="{M}"><m:e>{_r_wrap(b)}</m:e><m:sup>{_r_wrap(e)}</m:sup></m:sSup>'
  # v5.64 — DELEGATION (Item 1c): sqrt and omath were re-localised copies of
  # explain_engine's, semantically identical but cosmetically drifted (*p vs
  # *parts; line-wrapping) — entered as inherited_pre_existing debt in
  # XSPEC_DIVERGENCE_BASELINE.json at 2026.08.20.3, paid down here. The ENGINE
  # is the single authority; the aliases below leave nothing to drift. Output is
  # byte-identical: the engine closes over its own M/_r_wrap, which are
  # byte-equal to the locals above. explain_engine.py is on this trigger's
  # route (routes.json, v5.64) exactly as it is on the three Explain routes.
  import explain_engine
  sqrt  = explain_engine.sqrt
  omath = explain_engine.omath
  def add_math(paragraph, omath_xml): paragraph._p.append(parse_xml(omath_xml))
  ```

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  # v5.47 (MC2) — THE SINGLE FUNNEL. The SHARED Tier-3 compiler (t3_mathcomp.py,
  # byte-locked to Framework_PYQPrepare §S3-5b; routed to this trigger) replaces
  # per-expression segments authoring: write stems/options as ONE string with
  # ⟦MATH:…⟧ regions and pass it here. Grammar: \frac \sfrac \sqrt, x^{n},
  # k_{B}-style subscripts, n-ary operators, \cases, matrices, \bar/\vec
  # accents, Greek/symbol map — identical to Steps 1/PYQ-1/9.
  from t3_mathcomp import (t3_compile, MathCompileError,
                           MATH_OPEN as T3_OPEN, MATH_CLOSE as T3_CLOSE,
                           _REGION_RE as T3_REGION_RE, _T3_STATS as T3_STATS)

  def render_mock_text(paragraph, text, bold=False):
      """Interleave plain runs and compiled ⟦MATH:…⟧ regions. STRICT CORE,
      FORGIVING BOUNDARY: a region the compiler rejects NEVER halts the build
      and NEVER ships silently — it renders as ordinary plain text (no colour,
      no markup), is recorded in T3_STATS['failed'], and
      mock_math_residue_check() quotes it verbatim so the author can Ctrl+F
      straight to it."""
      pos = 0
      for mr in T3_REGION_RE.finditer(text):
          if mr.start() > pos:
              r = paragraph.add_run(text[pos:mr.start()]); r.bold = bold
          try:
              paragraph._p.append(t3_compile(mr.group(1)))
          except MathCompileError as err:
              T3_STATS['failed'].append((mr.group(1), str(err)))
              r = paragraph.add_run(mr.group(1)); r.bold = bold
          pos = mr.end()
      if pos < len(text):
          r = paragraph.add_run(text[pos:]); r.bold = bold
      return paragraph

  def mock_math_residue_check(docx_path):
      """v5.70 (MC3 → G-MATH-RESIDUE, GAP-2026-08-24-MATH-RESIDUE-SHIPPED) POST-BUILD
      MATH GATE — mandatory before EVERY delivery (each batch's STEP B AND the S13-2
      Final-Assembly sweep). SPLIT SEVERITY — supersedes the v5.47 blanket
      WARN-and-deliver, which let flat-underscore orbital labels ship in stems with
      0 OMML while the SAME questions' Step-9 explanations rendered correctly:
        'blocking' — ASCII-dialect residue DETECTED in the rendered paper: ÷ between
            operands, caret exponents, k_B-style underscores, HALF-UNICODE
            subscripts (a Unicode subscript digit followed by a LOWERCASE letter —
            t₂g, C₂v; H₂O-style single trailing subscripts stay plain per rule 2),
            √( or √letter, letter fractions (units masked), combining accents,
            residual ⟦MATH:⟧ delimiters, EMPTY OMML islands and SCHEMA-INVALID
            fractions. These are FIXABLE FAILs (S12-0 Zero-Warning Policy):
            present_files is FORBIDDEN until this list is EMPTY — re-emit each
            named stem/option via render_mock_text() with ⟦MATH:…⟧ regions.
            Gate id G-MATH-RESIDUE (S12-NEW-30); engine twin audit.py A-SUBFLAT.
        'amber'    — t3 COMPILE-FAILURE fallbacks (T3_STATS['failed']): a region
            that ENTERED the funnel and would not compile rendered as plain text.
            This keeps the v5.47 strict-core/forgiving-boundary contract exactly:
            WARN-and-deliver, F1 AMBER footer quoting each region verbatim.
      Returns {'blocking': [...], 'amber': [...]}."""
      import re as _re
      from docx import Document as _D
      _W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
      _Mns = M
      # v5.47.3 — masks are the SHARED _MM_* set (see the trigger block);
      # the gate holds no private copies.
      blocking, amber = [], []
      doc = _D(docx_path)
      failed_bodies = {b for b, _ in T3_STATS.get('failed', [])}
      for p in doc.paragraphs:
          t = p.text
          if any(fb and fb in t for fb in failed_bodies):
              continue
          if T3_OPEN in t or T3_CLOSE in t:
              blocking.append(f'residual region delimiter in: {t.strip()[:60]!r}')
          st = _mm_mask(t)
          if _re.search(r'[\w)\]²³]\s*÷|÷\s*[\w(]', st):
              blocking.append(f'division-sign fraction in: {t.strip()[:60]!r} — use ⟦MATH:\\frac{{a}}{{b}}⟧')
          if '^' in st:
              blocking.append(f'caret exponent in: {t.strip()[:60]!r} — use ⟦MATH:x^{{n}}⟧')
          if _re.search(r'(?<![A-Za-z0-9_])[A-Za-zψφχε]_(?=[A-Za-z0-9{{(])', st):
              blocking.append(f'flat subscript in: {t.strip()[:60]!r} — use ⟦MATH:k_{{B}}⟧')
          if _re.search(r'[\u2080-\u2089][a-z]', st):
              blocking.append(f'half-Unicode subscript in: {t.strip()[:60]!r} — use ⟦MATH:t_{{2g}}⟧ '
                              '(subscript digit + lowercase letter is the flat dialect; '
                              'H₂O-style single trailing subscripts stay plain, rule 2)')
          if _re.search(r'√\s*\(|√\s*[A-Za-zπλωεℏ]', st):
              blocking.append(f'flat radical in: {t.strip()[:60]!r} — use ⟦MATH:\\sqrt{{…}}⟧')
          if _re.search(r'[A-Za-z\u0391-\u03c9ℏ²³)\]]\s*/\s*[0-9A-Za-z\u0391-\u03c9(√ℏ]', st):
              blocking.append(f'letter fraction left linear in: {t.strip()[:60]!r} — use ⟦MATH:\\frac{{a}}{{b}}⟧')
          if _re.search(r'[\u0300-\u036f\u20d0-\u20ff]', st):
              blocking.append(f'combining-character accent in: {t.strip()[:60]!r} — use ⟦MATH:\\bar{{A}}⟧ / ⟦MATH:\\vec{{E}}⟧')
          for om in p._element.iter('{%s}oMath' % _Mns):
              if not ''.join(x.text or '' for x in om.iter('{%s}t' % _Mns)).strip():
                  blocking.append('EMPTY OMML island (content lost) in: %r' % t.strip()[:50])
              for f in om.iter('{%s}f' % _Mns):
                  for part in (f.find('{%s}num' % _Mns), f.find('{%s}den' % _Mns)):
                      if part is not None and ((part.text or '').strip() or not len(part)):
                          blocking.append('SCHEMA-INVALID fraction (bare text in num/den — '
                                          'Word renders it EMPTY) in: %r' % t.strip()[:50])
      for body, reason in T3_STATS.get('failed', []):
          snip = body if len(body) <= 60 else body[:57] + '…'
          amber.append('one maths expression could not be structured and was delivered '
                       f'as plain text: "{snip}" (reason: {reason}). Remedy: Ctrl+F the '
                       'quoted text, fix that ⟦MATH:⟧ spelling, rebuild.')
      return {'blocking': blocking, 'amber': amber}
  ```

  Math rendering decision tree (in order — use FIRST applicable rule):
  0. ANY built-up expression (rules 3-6 below) is rendered as OMML and is NEVER
     rasterised. The matplotlib / figural / image pipeline is BANNED for
     algebraic/symbolic math — it is for GEOMETRIC FIGURES ONLY. (R-MATH-OMML.)
  1. Unit labels (km/h, m/s, cm²): plain text
  2. Single symbols (², ³, √n, ×, ≤, ≥, ±, π, °, θ): Unicode. SUBSCRIPTED
     symbols (k_B, R_in, N₂ beyond a single trailing digit) are NOT single
     symbols — they are built-up math (rule 3a). ÷ is NEVER a fraction
     spelling in prose.
  3. Fractions (a/b stacked): MANDATORY OMML — ⟦MATH:\frac{a}{b}⟧ via
     render_mock_text() (or legacy frac(), now raw-arg-safe)
  3a. Subscripts (k_B, R_in, v_rms): MANDATORY OMML — ⟦MATH:k_{B}⟧
      CHEMISTRY ORBITAL / STATE / SYMMETRY LABELS (v5.70 — the delivered-defect
      class): t₂g → ⟦MATH:t_{2g}⟧ · e_g → ⟦MATH:e_{g}⟧ · d_xy → ⟦MATH:d_{xy}⟧ ·
      d_z² → ⟦MATH:d_{z^{2}}⟧ · d_x²−y² → ⟦MATH:d_{x^{2}-y^{2}}⟧ · C₂v →
      ⟦MATH:C_{2v}⟧. A HALF-UNICODE spelling (a Unicode subscript digit followed
      by a LOWERCASE letter, e.g. t₂g typed with ₂) is the SAME flat dialect as
      t_2g and is equally banned in plain text. Simple formulas with a single
      trailing subscript digit (H₂O, N₂, CO₂ — the subscript followed by nothing
      or an UPPERCASE element symbol) stay plain Unicode per rule 2.
  4. Nested radicals: MANDATORY OMML sqrt()
  5. Exponent+fraction: MANDATORY OMML
  6. Trig identities with fractions: MANDATORY OMML
  7. Raw LaTeX (\\frac, \\sqrt) OUTSIDE a ⟦MATH:⟧ region, ÷-fractions,
     caret exponents, underscore subscripts, half-Unicode subscripts (t₂g typed
     with ₂ — v5.70), √(…) and combining-character accents in prose: NEVER —
     every one is the ASCII dialect that mock_math_residue_check() names; each is
     a G-MATH-RESIDUE per-batch FIXABLE FAIL (v5.70); the legal spelling is a
     ⟦MATH:…⟧ region.

  MATH-AS-OMML ROUTING CONTRACT (v4.3 — the executable home for rules 0/3-6).
  Before v4.3 the tree above stated the GOAL but there was no function to call:
  add_question_stem() writes the whole stem as one text run, so a generator with
  a built-up expression had no OMML entry point and could fall back to a raster
  (the M1 Q.55 defect: "x + 1/x = 5" and "x²+1/x²" shipped as 300-DPI matplotlib
  PNGs). These helpers close that hole. Any stem or option whose text matches
  MATH_TRIGGER_RE MUST be emitted through render_mock_text() with ⟦MATH:…⟧
  regions (the v5.47 single funnel — shared Tier-3 compiler), or through the
  legacy add_math_stem / emit_math_inline segments API (OMML), NEVER through
  the figural raster path.

  ```python
  import re
  from docx.shared import Pt
  from docx.oxml import parse_xml

  # Detects a BUILT-UP expression (rules 3-6): a stacked fraction (token "/"
  # between operands, not a unit label), an exponent/superscript, or a radical.
  # Unit labels (km/h, m/s) and single Unicode symbols are deliberately NOT matched.
  MATH_TRIGGER_RE = re.compile(
      r"(?:[A-Za-z0-9\u0391-\u03c9ℏ\)\]]\s*/\s*[A-Za-z0-9\u0391-\u03c9ℏ\(\[])"  # stacked fraction a/b (v5.47.2: Greek+ℏ)
      r"|(?:\^\s*[-+]?\d)"                               # caret exponent x^2
      r"|(?:[A-Za-z0-9]\s*[\u00b2\u00b3])"              # superscript ² ³ on a term
      r"|(?:\\frac|\\sqrt)"                              # raw LaTeX
      r"|(?:\u221a\s*[\(A-Za-z0-9])"                    # radical √(...)
      r"|(?:[A-Za-z]_[A-Za-z0-9{{(])"                     # subscript k_B (v5.47)
      r"|(?:[\w)\]]\s*÷|÷\s*[\w(])"                    # ÷-fraction (v5.47)
      r"|(?:[\u0300-\u036f\u20d0-\u20ff])"             # combining accent (v5.47)
      r"|(?:[\u2080-\u2089][a-z])"                     # half-Unicode subscript t₂g/C₂v (v5.70)
  )
  # v5.47.3 — THE ONE SHARED MASK SET. Defined once; consumed by BOTH
  # needs_omml (authoring detection) and mock_math_residue_check (post-build
  # gate). Agreement between the two consumers is structural — a mask edited
  # here changes both, and a mask edited anywhere else does not exist.
  _MM_UNIT = re.compile(r"\b(?:km|m|cm|mm|kg|g|l|ml|s|hr|h|rad|rev|V|W|J|N|C|T|A|eV)[²³]?"
                        r"\s*/\s*(?:h|s|min|hr|m|K|kg|mol|c)[²³]?\b")
  _MM_WORDPAIR = re.compile(r"\b(?:is/are|and/or|has/have|he/she|yes/no|a/an|c/o|w/o|I/O)\b",
                            re.IGNORECASE)
  _MM_YEARFORM = re.compile(r"\b[A-Za-z]{2,}\s*/\s*(?:19|20)\d{2}\b")

  def _mm_mask(text):
      return _MM_YEARFORM.sub(" ", _MM_WORDPAIR.sub(" ", _MM_UNIT.sub(" ", text or "")))

  UNIT_LABEL_RE = _MM_UNIT   # retired compatibility alias (v5.47.3)

  # v5.47.3 — the ORIGINAL v4.3-scope raster ban. assert_not_math (figural
  # LADDER-REPAIR R1 [HS:LADDER]) tests THIS, not the widened MATH_TRIGGER_RE: normalised-axis
  # figure labels (σ/σ₀, α/β, Δv/Δt) are legitimate figural text and must not
  # abort builds; whole built-up expressions still never rasterise.
  RASTER_BAN_RE = re.compile(
      r"(?:[A-Za-z0-9\)\]]\s*/\s*[A-Za-z0-9\(\[])"
      r"|(?:\^\s*[-+]?\d)"
      r"|(?:[A-Za-z0-9]\s*[\u00b2\u00b3])"
      r"|(?:\\frac|\\sqrt)"
      r"|(?:\u221a\s*[\(A-Za-z0-9])"
  )

  def needs_omml(text, pattern=None):
      """Masked built-up-math detector. Default pattern = the widened
      MATH_TRIGGER_RE (stem/option ROUTING). assert_not_math passes
      RASTER_BAN_RE (figural scope). Masks are the shared _MM_* set — the
      SAME masks the post-build gate applies (v5.47.3 unification)."""
      if not text:
          return False
      return bool((pattern or MATH_TRIGGER_RE).search(_mm_mask(text)))

  def assert_not_math(label):
      """Guard called by the FIGURAL path (S10-7). A built-up expression must
      NEVER reach the raster pipeline. R-MATH-OMML LADDER-REPAIR R1 [HS:LADDER]."""
      if needs_omml(label, pattern=RASTER_BAN_RE):
          raise AssertionError(
              f"R-MATH-OMML: refusing to RASTERISE a math expression "
              f"({label!r}). Built-up math is OMML only (S10-4 add_math_stem); "
              f"the figural pipeline is for geometric figures only.")

  def emit_math_inline(paragraph, omath_xml):
      """Append one <m:oMath> block to an existing run-bearing paragraph,
      interleaved with surrounding text runs (alias of add_math, kept explicit
      so callers route built-up math here, not to a raster)."""
      paragraph._p.append(parse_xml(omath_xml))

  def add_math_stem(doc, qnum, segments, bold=True):
      """Build a Q.N-first stem (R14) that interleaves text and OMML.
      `segments` = ordered list of ('text', str) and ('omml', omath_xml) tuples.
      Example for Q.55 'If x+1/x=5, then ... value of x²+1/x² ?':
        add_math_stem(doc, 55, [
          ('text','If  '),
          ('omml', omath(_r('x + '), frac(_r('1'), _r('x')), _r(' = 5'))),
          ('text','  , then what is the value of  '),
          ('omml', omath(sup(_r('x'),_r('2')), _r(' + '),
                         frac(_r('1'), sup(_r('x'),_r('2'))))),
          ('text',' ?'),
        ])
      """
      p = doc.add_paragraph()
      first = p.add_run(f"Q.{qnum}  ")
      first.bold = bold; first.font.name = FONT_NAME; first.font.size = Pt(FONT_SIZE_PT)
      for kind, val in segments:
          if kind == 'text':
              r = p.add_run(val)
              r.bold = bold; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
          elif kind == 'omml':
              emit_math_inline(p, val)        # OMML run — never an image
          else:
              raise ValueError(f"add_math_stem: bad segment kind {kind!r}")
      return p
  ```

  GENERATION ROUTING (mandatory): when build_question() prepares a stem or an
  option, it FIRST tests needs_omml() on the rendered text. If true, the segment
  is emitted via add_math_stem / emit_math_inline (OMML). It is a LADDER-REPAIR R1 [HS:LADDER] to
  route such a segment to render_figural_image() — that function now calls
  assert_not_math() and will raise. Geometric figures (mensuration/coordinate
  diagrams, reasoning panels) are the ONLY content the figural raster path
  accepts, and they are emitted under the canonical image-naming convention
  (§10-S10-7/S10-8) so gate G-MATH-RASTER can tell a figure from a stray raster.

## S10-LINKED — linked-member emission (v3.7 — Q.N-FIRST ordered block)

  Called by S4-7 STEP A for every member of a CLASS-4 group. Emits the member as
  the §9 SC-3 ordered block: Q.N context line FIRST, then the embedded stimulus,
  then the specific ask, then options, then a blank separator. The stimulus
  content is read from the group's context-store entry so all members get
  byte-identical text/table/image (resume-safe per S4-8b).

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  def add_qn_context(doc, qnum, context):
      """Line 1 of the block: 'Q.<N>  <shared context/instruction>' (BOLD).
      This is the SINGLE Q-numbered paragraph for the whole block (R14)."""
      p = doc.add_paragraph()
      r = p.add_run(f"Q.{qnum}  {context}")     # Q.N FUSED with context
      r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
      return p

  def add_specific_ask(doc, ask_text):
      """Line 3 of the block: the actual question (BOLD, NON-numbered).
      Carries NO 'Q.N' — the block's Q-number already opened it in line 1."""
      p = doc.add_paragraph()
      r = p.add_run(ask_text)
      r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
      return p

  def add_linked_stimulus(doc, qnum, group):
      """
      Emit ONE linked member in §9 SC-3 order. Q.N comes FIRST (v3.7 Q.N-FIRST).
      group = {
        'linked_group_id': str,
        'mode'           : 'passage' | 'cloze' | 'di_table' | 'di_chart' | 'puzzle',
        'context'        : str,                 # shared instruction (singular Q)
        'passage_text'   : str | None,          # passage / cloze paragraph(s)
        'passage_bold'   : bool,                # True to match reference layout
        'table'          : TableSpec | {'headers': [...], 'rows': [[...]]} | None,
                           # v5.32: TableSpec (S1-8a) carries spans; the legacy
                           # {'headers','rows'} form still works unchanged.
        'chart_image'    : bytes | None,        # PNG, 300 DPI
        'ask'            : str,                  # this member's specific question
      }
      """
      # LINE 1 — Q.N + shared context (BOLD). Nothing may precede this.
      add_qn_context(doc, qnum, group['context'])

      # LINE 2 — the embedded stimulus (identical across members; SC-6 exempts
      #          intra-group repeats from R3/table-dedup).
      if group['mode'] in ('passage', 'cloze') and group.get('passage_text'):
          pp = doc.add_paragraph()
          rr = pp.add_run(group['passage_text'])   # full paragraph, all blanks
          rr.bold = bool(group.get('passage_bold', False))
          rr.font.name = FONT_NAME; rr.font.size = Pt(FONT_SIZE_PT)
      elif group['mode'] == 'di_table' and group.get('table'):
          build_di_table_styled(doc, group['table'])          # §8-S8-4 (v5.32)
      elif group['mode'] == 'di_chart' and group.get('chart_image'):
          insert_chart_image(doc, group['chart_image'])        # §8-S8-5
      elif group['mode'] == 'puzzle' and group.get('passage_text'):
          pp = doc.add_paragraph()
          rr = pp.add_run(group['passage_text'])
          rr.bold = bool(group.get('passage_bold', False))
          rr.font.name = FONT_NAME; rr.font.size = Pt(FONT_SIZE_PT)

      # LINE 3 — the specific ask (BOLD, non-numbered).
      add_specific_ask(doc, group['ask'])
  ```

  USAGE in S4-7 STEP A (per member, ascending Q order):
  ```python
  for q in batch_questions:
      if q.linked_group_id:
          g = dict(context_store[q.linked_group_id]); g['ask'] = q.ask
          add_linked_stimulus(doc, q.num, g)       # Q.N context → stimulus → ask
      else:
          add_question_stem(doc, q.num, q.stem)    # S10-3 (single Q — also Q.N first)
      add_text_options(doc, q.options)             # S10-3 (normal weight)
      doc.add_paragraph()                          # blank separator (R13)
  ```

  Q.N-FIRST INVARIANT: in BOTH branches the first paragraph of the block is a
  "Q.<N>" paragraph. No stimulus is ever emitted before it. Verified by
  G-QNUM-FIRST.

  MODEL B EXCEPTION: if delivery.linked_mode == "group" (confirmed at S3), emit
  one "Q.<X>  [GROUP: Q.X–Q.Y] <context>" line + stimulus once, then the members'
  asks bound by group_id. Default is ALWAYS "embed" (Model A).

## S10-5, S10-6, S10-9, S10-10 — (unchanged from v1.0 — see v1.0 for full spec)

## S10-6A — FIGURE CLASS TAXONOMY (v5.33 — new, GAP-2026-07-29-FIG-R2 §7.1)

  Every figure MUST declare exactly ONE class before it is drawn. Class selects
  the renderer, the palette policy, the sizing profile and which gates apply.

  | Class | Description | Renderer | Palette | Colour gate |
  | :--- | :--- | :--- | :--- | :--- |
  | `data_series` | ≥2 comparable series (line, scatter, grouped bar) | figural_core | Okabe-Ito, ≥2 hues | REQUIRED |
  | `data_single` | one series (single curve, single bar set) | figural_core | 1 accent hue (OKABE_ITO[0] series ink) MANDATORY — v5.46 | accent required — A-FIGACCENT (AMBER) |
  | `schematic` | pathway, apparatus, circuit, pedigree, structure | figural_core | ≥1 accent for the item under interrogation, MANDATORY — v5.46 | accent required — A-FIGACCENT (AMBER) |
  | `reasoning_glyph` | matrix / series / odd-one-out / figure-completion | S10-7 glyph path | MONOCHROME, mandatory | must be monochrome |
  | `option_canvas` | one MCQ option | inherits the parent question's class | inherits | inherits |

  CLASS INFERENCE PRECEDENCE: (1) declared in the FigureSpec, (2) measured from
  the draw call (series count), (3) keyword match on the stem. Declared always
  wins. If inference yields no class that is a HARD failure — NEVER a default.

  TYPE → CLASS → KIND → RENDERER BINDING (v5.88, LAW F1.1). The table above names
  CLASSES; the profile vocabulary (Step 5 object_type) is bound to a class, a semantic
  kind and a renderer by ONE table, `figure_types.FIGURE_TYPES` (repo-only, hash-tracked;
  mock_sync_audit MS-23 keeps its classes equal to this table and its kinds equal to
  paper_pipeline.SEMANTIC_KINDS). A reaction scheme (reaction_scheme,
  reaction_mechanism_scheme, …) is class `schematic`, kind REACTION, renderer
  corpus_io.render_scheme — no new class, so every palette policy and gate above applies
  to it unchanged. Adding a figure type is a REPO change with a fixture, never a
  per-exam edit; an unregistered type draws as a GENERIC `schematic` and is disclosed.
  A defaulted class is how a scientific data figure ended up on the geometry
  path in the first place.

  v5.80 COLOUR ROLES. The palette column above names HUES; Q7b.9-Q7b.14 assign
  each hue a ROLE (text / line-mark / fill) and gate the role. In short: any
  coloured LABEL is drawn with `fc.text_ink(hue)`; any FILL with
  `fc.fill_style(k)`; at most FOUR chromatic series per figure; a structure's
  interrogated site is accented through `structure_draw_fn(highlight_*)`;
  heteroatom colour across an option set is decided ONCE by render_option_set();
  a question that interrogates a colour renders MONOCHROME (colour_content=True
  on the FigureSpec, from `fc.colour_is_content(stem, options)`). None of this
  changes which class a figure is or which pre-v5.80 gate applies to it.

  `reasoning_glyph` MUST remain monochrome. Colour in an abstract-reasoning item
  can leak the answer: if the correct option carries any distinct colour
  treatment the item is void. The single permitted exception is a designated
  accent for a MISSING-ELEMENT marker (the "?" cell), which is identical across
  all options and therefore leaks nothing.

  TWO RENDERERS, ONE CONTRACT. `render_figural_image()` below is a geometry-glyph
  renderer — equal aspect, axes off, uniform square canvas. It is correct for
  `reasoning_glyph` and `option_canvas` and MUST NOT be used for the three data
  classes: it has no axis, tick, legend or font API and structurally cannot
  label a scientific figure. Those classes route to
  `figural_core.render_figure()`. Both obey S10-7 Q1–Q9 and S10-8.

## S10-7 — FIGURAL IMAGE-QUALITY CONTRACT (v5.33 — colour, labels, scale)

  Every figural raster must be reference-grade and online-renderable. This
  section is the executable home that S7-NEW-B Option A / S8-6 reference. The bar
  is PERFECT line-art quality: crisp at display size, uniform across options, no
  question chrome inside the pixels — AND, from v5.33, legible at the size it is
  actually printed and readable in greyscale and to a colour-blind reader.

  RUNTIME DEPENDENCIES (v5.33). This section needs more than Step 0's
  python-docx. figural_core.DEPENDENCIES declares the surface and
  figural_core.preflight() reports it; both are checked, never assumed.
    matplotlib  REQUIRED to render. render_figure() raises FiguralError
                G-FIGDEP carrying the pip command, not a bare ImportError from
                three frames down.
    pillow      required for the pixel gates (PNG size, DPI, colour presence)
    numpy       required for the pixel gates
    scipy       optional — advisory label estimate only
    fonttools   optional — tofu detection only
  ABSENCE NEVER HALTS AN AUDIT. Every gate degrades to DORMANT-but-reported and
  routes to AMBER: a gate that raises is worse than a gate that is absent,
  because it takes the whole audit down, and an audit that dies takes ~200
  projects with it. Guards import the module and catch failure rather than
  asking whether it is on the path — a package can be installed and still fail
  to load, and presence-checking leaves exactly the traceback the guard exists
  to prevent.

  FRAMEWORK CONSTANTS (do NOT read these from section_rules — they are universal;
  they are DEFINED in figural_core.py and mirrored here for reference only):
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  FIGURAL_DPI            = 300  # savefig dpi — minimum, never below
  FIG_COLUMN_IN          = 6.0  # usable text column, A4/Letter at 1in margins
  FIG_PROBLEM_DISPLAY_IN = 4.0  # on-page width of the problem/series figure
                                # (was 2.3 — too narrow to carry a labelled axis)
  FIG_OPT_DISPLAY_IN     = 1.3  # on-page side of EACH option (uniform square)
  FIG_NATIVE_HEADROOM    = 1.0  # RETIRED. Was 2.0 and was the whole of RC-2.
                                # MUST stay 1.0 and MUST NOT appear in placement
                                # arithmetic. At 300 dpi the supersample bought
                                # nothing and halved every label.
  FIG_MIN_STROKE_PT      = 1.4  # minimum line width
  # v5.55 — the layout contract. These are what make Q10/Q11/Q12 checkable.
  FIG_MIN_CLEARANCE_IN   = 0.05 # ink-to-frame clearance AT DISPLAY SIZE. 15 px at
                                # 300 dpi — comfortably above the 1.4 pt frame
                                # stroke (5.8 px), so the clearance is VISIBLE and
                                # not merely arithmetic.
  FIG_LABEL_PAD_IN       = 0.020# label-to-label / label-to-stroke breathing room
  FIG_LABEL_MAX_SHIFT_IN = 0.10 # how far the deconflicter may nudge a label from
                                # its authored anchor. Beyond this the label no
                                # longer identifies the atom it was attached to,
                                # and a silently re-attached label is a WRONG
                                # figure that PASSES — strictly worse than a
                                # reported collision. The cap is the whole reason
                                # G-FIGCOLLIDE can be trusted.
  FIG_COLLIDE_TOL        = 0.02 # residual overlap tolerated, as a fraction of the
                                # smaller label box
  FIG_FIT_MAX_PASSES     = 8    # measured: chemistry option sets converge in 2-4
  MIN_CONTENT_FILL_FRAC  = 0.45 # CALIBRATED, not aspirational. Delivered corpus
                                # median 29.6%; post-fix shared-window option sets
                                # measure 0.40-0.55. A floor set on single figures
                                # would fire on every correctly-uniform SET.
  FIG_CANVAS_ASPECT_DEFAULT = 0.72  # was hardcoded in figure_style(); now the
                                    # DEFAULT only, so every un-regenerated exam
                                    # renders exactly as before.
  ```

  QUALITY RULES (all mandatory — each is checked at view-tool verification):
    Q1. VECTOR-FIRST. Build every figure from geometry (matplotlib Rectangle /
        Circle / Polygon / Line, or an SVG path), then rasterise. NEVER screenshot,
        NEVER upscale a small bitmap, NEVER trace by hand in text.
    Q2. LOSSLESS PNG ONLY. Save as PNG. JPEG is BANNED for line art (ringing
        artefacts on edges). Background MUST be OPAQUE WHITE
        (facecolor="white", transparent=False) for every figure in every mock.
        v5.33: transparent RGBA is no longer permitted, and is no longer the
        stated preference. Transparent backgrounds render as invisible or
        near-invisible text in dark-mode and shaded-background viewers, and the
        alpha channel measured constant-255 on all 208 delivered drawings
        anyway — it was pure overhead. Prefer RGB over RGBA when alpha is
        constant.
    Q3. 300 DPI, NO HEADROOM, DETERMINISTIC CANVAS. Save at FIGURAL_DPI with
        figsize == the display size in inches, so
            saved_px == display_in × FIGURAL_DPI    (exactly)
        and the placement scale S is 1.0 by construction.
        v5.33 supersedes the old headroom rule, which said "render native pixels
        ≥ FIG_NATIVE_HEADROOM × the display pixel size" and then, in the same
        rule, gave two incompatible floors for the same 1.3 in option (780 px,
        then "≥ ~450 px and prefer ~600+"). The headroom was applied to the
        canvas and never compensated in the font size, so every label was
        printed at 1/headroom of its requested size — measured S = 0.500 exactly
        on 24 of 24 option canvases. At 300 dpi the supersample bought nothing
        that 300 dpi does not already provide, and Word's downsampling filter is
        unspecified. There is now ONE floor: 300 dpi at display size.
        `bbox_inches="tight"` is BANNED on every figure path. Tight trimming
        makes the saved width a function of the figure's own CONTENT — label
        length, legend overflow — so S becomes an uncontrolled variable: 27
        distinct canvas sizes across 31 delivered problem figures, S wandering
        0.495–0.666. Use `constrained_layout=True`, which gives the same good
        margins with a size that is known before the file is written.
    Q4. UNIFORM OPTION CANVAS (v5.55 — restated; the word "square" is REMOVED).
        All N option images of a question share ONE canvas size AND ONE data
        window. Do NOT tight-crop options (tight crop yields non-uniform sizes).
        v5.55 corrects two things this rule got wrong:
          (a) IT SAID "SQUARE" AND THE ENGINE NEVER WAS. figure_style() has
              hardcoded figsize = (d, d x 0.72) since v5.33, so every delivered
              option canvas measured 390 x 280 px while this rule demanded a
              square. Spec and engine contradicted each other for four releases
              and no gate could fire, because no gate read either. The invariant
              that actually matters is UNIFORMITY ACROSS THE SET — a size or
              scale difference between options is an answer cue (Q7b.6) — never
              squareness. The canvas ASPECT is now derived from the content and
              shared by the whole set (Q12).
          (b) FIXING THE AXES TO [0,1]x[0,1] IS THE DEFECT, NOT THE CONTRACT. A
              fixed window cannot know how wide a rendered label is — text extent
              is font-metric dependent and is not derivable from the data it
              annotates — so an author-side rule ("place labels 0.18 units out")
              can never guarantee fit. That is exactly how 3 of 24 delivered
              option canvases put ink outside their own frame. The window is now
              MEASURED and fitted by the renderer (Q10).
        The border box is drawn by the RENDERER, never by draw_fn (Q10.4).
        (The problem figure MAY be a different, wider unit; it MUST NOT use a
        tight bbox — Q3.)
    Q5. NO QUESTION CHROME IN PIXELS. The stem, caption, instruction, and the
        option numbers (1/2/3/4) are DOCUMENT TEXT, never inside a raster.
        INTRINSIC figure annotations ARE allowed (mirror-line endpoints M/N,
        geometry vertices A/B/C, axis tick labels) — they label the figure itself.
        v5.88: the REAGENT and CONDITION text over/under a reaction arrow
        ('t-BuCl (2 equiv)', 'CH₂Cl₂, −78 °C', 'i. NBS, H₂O / ii. NaOH'), '+' between
        substrates, placeholder letters (A, B, [ A ]), equivalents and tile labels
        ARE INTRINSIC — they are the figure, exactly as the printed paper carries
        them (20 of 24 figural organic questions on the reference paper). Moving them
        into the stem is the lone-molecule-plus-26-word-stem shape this release ends.
    Q6. REAL REFERENCE GEOMETRY. A mirror line, fold line, number line, or axis is
        DRAWN as an actual line/curve. Never represent a line by two floating
        letters (the M1 "MN" defect).
    Q7. CONSISTENT STROKE + FILL. Line width ≥ FIG_MIN_STROKE_PT, antialiasing
        ON, and the SAME STROKE WEIGHT AND STYLE BUDGET across a question's
        option set so the options read as a matched set. A stroke or size
        difference between options is an answer cue; this clause is a
        correctness safeguard, not a cosmetic one, and must survive any future
        edit to this rule.
        v5.33: the words "solid black" are REMOVED. They were the whole of RC-1
        — the monochrome output measured across 55 delivered figures was
        CONFORMANT to this rule as previously written. Colour policy is now Q7b
        and is selected by the S10-6A class. `reasoning_glyph` and its option
        canvases remain monochrome under Q7b.7.
    Q7b. COLOUR AND REDUNDANT ENCODING (v5.33 — new).
        1. Palette MUST be Okabe-Ito, ESTATE-WIDE, with NO per-exam override
           (v5.80 owner decision: the `exam_config.figure_palette` reservation
           of v5.46 is CLOSED, never wired — a per-exam palette is a per-exam
           migration, and the render_figure() palette= parameter remains ONLY
           the internal plumbing render_option_set() uses to hand one palette
           to a whole set). Every Step-7 render uses OKABE_ITO:
           #0072B2 #D55E00 #009E73 #CC79A7 #E69F00 #56B4E9 #F0E442 #000000
           (colour-blind safe across deuteranopia/protanopia/tritanopia, print
           safe, 8 hues). Defined once in figural_core.OKABE_ITO. v5.80 assigns
           each hue a ROLE — Q7b.9-Q7b.14 below — and gates the role; the hue
           set itself is unchanged and every pre-v5.80 clause stands as written.
        2. COLOUR MUST NEVER BE THE SOLE CARRIER OF MEANING. Every series MUST
           differ from every other series in at least ONE additional channel:
           line style, marker shape, or hatch pattern. This is what makes a
           figure survive greyscale printing and a colour-blind reader even if
           the palette is overridden. Gate G-FIGSERIES.
        3. Any two DECLARED series colours MUST remain separable after a
           deuteranope transform (≥ DEUT_MIN_SEP summed channel units).
           v5.33 NOTE — there is deliberately NO LUMINANCE CLAUSE. GAP-R2 §7.3.3
           demanded ≥20/255 luminance separation while §7.3.1 mandated
           Okabe-Ito, and the two are mutually unsatisfiable: over the 10 pairs
           of the first five Okabe-Ito hues the deuteranope clause passes 10/10
           and the luminance clause fails 3/10 (blue/bluish-green 18.6,
           vermillion/bluish-green 13.0, purple/orange 11.0). Okabe-Ito is
           CVD-safe by design; it was never greyscale-LUMINANCE-safe, and no
           8-hue palette can be both. GREYSCALE SURVIVAL IS DELIVERED BY Q7b.2
           REDUNDANT ENCODING, gated by G-FIGSERIES — not by a luminance
           threshold. Gating it twice made the check fire 569 times across 144
           conformant figures.
           The gate reads the DECLARED colours, never extracted pixels.
           Quantised onto a 32-step cube the mandated blue and bluish-green
           separate by 57 instead of their true 60.6 and the check fired on its
           own palette; that is measurement error reported as a defect. Gating
           the declaration is exact and reproducible, which also settles the
           method-sensitivity problem (the same exhibits measured two ways gave
           48 % and 70 % collapse). Whether the RENDER honoured the declaration
           is a separate question answered by G-FIGCOLOUR's hue COUNT.
        4. Pie, donut and area charts MUST label segments DIRECTLY ON THE MARK.
           A legend as the sole key is prohibited for these types.
        5. #F0E442 (yellow) MUST carry a dark edge when used as a fill.
        6. Colour MUST NOT correlate with correctness in an option set. All
           options in a set MUST use an identical style budget. (The delivered
           uniform 780×780 option canvases were CORRECT on this point and the
           property must be preserved.)
        7. Class `reasoning_glyph` MUST be monochrome apart from a declared
           missing-element accent. Gate G-FIGMONO.
        8. ACCENT PRESENCE (v5.46 — GAP-2026-08-07-FIGACCENT). The S10-6A
           palette column is NORMATIVE AND GATED, no longer prose. Class
           `data_single`: the series ink MUST be OKABE_ITO[0] (axes, frame and
           gridlines stay black) — "permitted" was upgraded to MANDATORY by
           owner decision 2026-08-07, because "permitted" is exactly what let
           one exam ship all-black while another shipped accented. Class
           `schematic`: the item under interrogation MUST carry >=1 Okabe-Ito
           accent hue; structural ink stays black. AUTHORING CONTRACT: the
           draw_fn MUST take its accent ink from the `palette` argument that
           render_figure() passes in; hardcoding "#000000"/"k" for the
           interrogated item or the series is a Q7b.8 breach even if the
           rendered figure happens to pass the gate. Gate G-FIGACCENT
           (catalogue A-FIGACCENT), AMBER by construction: it has no fire-0
           verification history yet, and no image-COLOUR condition may ever
           halt a run. Floor: coloured_fraction >= 0.05% of visible pixels
           (ACCENT_MIN_FRAC), calibrated on the delivered corpus — accented
           figures measure >= 0.105%, all-black 0.0000% — and deliberately not
           gated on dominant_hues(), whose minimum-area cut swallows small
           accents. `data_series` stays G-FIGCOLOUR territory (never
           double-gated); `reasoning_glyph` and its option canvases stay
           monochrome under Q7b.7; option canvases of accent-class parents
           keep the identical style budget of Q7b.6. EC-V18: legacy figures
           with no FigureSpec sidecar are silent under this gate.
           v5.89 AMENDMENT (GAP-2026-11-02 F3, owner decision O2): CHEMISTRY
           figures — every object_type in figure_types.CHEM_R_OBJECT_TYPES or
           CHEM_H_OBJECT_TYPES (make_figure_spec(..., chem=True)) — are EXEMPT
           from ACCENT PRESENCE, and so is every figure of an exam whose PYQs
           were MEASURED monochrome (FIGURE_STYLE_PROFILE). Measured defect: the
           MUST plus a FAIL-severity AMBER finding on every unaccented
           hydrocarbon pushed authors to mark 22 of 40 problem figures although
           no stem named a site, and the "item under interrogation" was usually
           the answer. ACCENT_REQUIRED keeps `data_single` and `schematic` for
           every other figure.
        8'. MARK-IFF-NAMED (v5.89 — GAP-2026-11-02 F3; gate G-FIGMARK, catalogue
           A-FIGMARK, VOID_ITEM -> repair ladder R1). A figure carries a mark
           (underline, asterisk, letter, arrow, bold bond) IF AND ONLY IF the
           stem names that site, using the word for the device that is drawn.
           The S7 author DECLARES, for every figure:
             marked_sites = [{"tile": k,                       # SCHEME only (S7-NEW-B2)
                              "site": {"kind": "atom"|"bond", "index": i}   # chem-R,
                                                                          # uncondensed index
                                  or {"kind": "anchor", "name": "front_C1"}, # chem-H
                              "device": "underline"|"asterisk"|"letter"|"arrow"|"bold",
                              "text": "<the letter>",   # REQUIRED iff device == "letter"
                              "stem_phrase": "<exact substring of the stem>"}]
           and passes it to make_figure_spec(marked_sites=..., stem=...) and,
           for chem-R, to cio.structure_draw_fn(marks=[{site, device, text}])
           through make_structure_draw (S7-NEW-B2; 'text' only for a letter). With no
           named site the list is EMPTY and the figure carries no mark of any
           kind. The device may only be one DRAWABLE at the site under the
           exam's profile, so stem and figure always agree:
             • a monochrome exam never says "highlighted" — it says "shown in
               bold" (device bold) or "marked" (arrow);
             • an unlabelled carbon cannot be "underlined" — use "marked with an
               asterisk" or a letter;
             • "the underlined proton" — draw that H explicitly, then underline.
           G-FIGMARK verifies: (i) every stem_phrase occurs verbatim in the stem;
           (ii) the renderer drew exactly the declared marks; (iii) an empty
           declaration means no mark at all; (iv) a stem that names a site
           (fc.SITE_MARK_LEXICON, extended by FIGURE_STYLE_PROFILE.
           site_mark_lexicon_extra) has a declared phrase covering it; (v) the
           device word in each stem_phrase names the drawn device
           (fc.DEVICE_WORDS); (vi) a letter mark declares its letter ("text")
           and that letter occurs in its stem_phrase; and no mark failed to find
           a clear position.
           Placeholder letters A, B, P are never sites (the letter lexicon is
           case-sensitive). An isotope label (D, ¹⁴C*) and drawn atom numbering
           are marks. Option canvases carry marks only under their own declared
           phrase.
        9. TEXT INK (v5.80 — GAP-2026-08-29-FIGURE-COLOUR-ROLES). A coloured
           LABEL or ANNOTATION is text, and text on the mandated white ground
           must clear WCAG 2.x SC 1.4.3 (>= 4.5:1). Only blue (5.19) and black
           do; vermillion (3.87), bluish-green (3.42) and purple (3.06) clear
           the 3.0:1 GRAPHICS floor (SC 1.4.11) and no more, and orange (2.25),
           sky (2.31) and yellow (1.32) clear neither. Therefore: every coloured
           text run in a draw_fn takes its colour from `fc.text_ink(hue)`, which
           returns the SAME hue darkened in CAM02-UCS to the 4.5:1 floor
           (figural_core.ROLE_TEXT: #C25604, #158663, #AB5D89; blue and black
           map to themselves) and DECLARES it on the FigureSpec
           (`text_colours`). Orange, sky and yellow are FILL-only (Q7b.10) and
           may never be text or a stroke thinner than FIG_MIN_STROKE_PT. Gate
           G-FIGTEXTINK reads the DECLARATIONS (exact and reproducible — the
           Q7b.3 doctrine), never pixels; AMBER; silent on a sidecar without
           `colour_profile`. Text colours need CONTRAST, not mutual
           separability: the glyph ("O" vs "N") carries the meaning, so the
           deuteranope clause of Q7b.3 applies to SERIES colours only.
       10. FILLS (v5.80). A filled region (bar, band, Venn region, tissue
           layer, shaded zone) uses `fc.fill_style(k)` — facecolor from
           figural_core.FILLS (sky, orange, yellow, and two DERIVED tints
           #A6DDCE / #EDD0E0 that are bluish-green and purple at exactly 35 %
           over white, pinned so every machine renders the same bytes — NOT new
           hues), a dark edge ALWAYS (Q7b.5 generalised from yellow to every
           fill), and hatch k as the greyscale channel. Region fills, phase
           bands and on-mark VALUE labels are permitted enrichment under this
           clause; a figure TITLE, a concept name, a derived quantity or any
           working inside the pixels remains a Q5 breach (that is what makes
           an annotation-rich figure leak its answer).
       11. ADJACENT FILLS (v5.80). Two fills that touch must differ by hatch
           OR by >= FILL_ADJ_MIN_LUMA (30/255 Rec.601 luma): sky (158) and
           orange (162) may touch only with a hatch; yellow (213) may touch
           either without one. Gate G-FIGFILLADJ over the declared fills;
           AMBER; silent without `colour_profile`.
       12. SERIES CAP (v5.80). At most SERIES_CHROMATIC_CAP = 4 chromatic
           series (blue, vermillion, bluish-green, purple — the four
           series_defaults() already hands out first) plus black on ONE
           figure. Reproduced 2026-08-29 with Petroff's metric: our first pair
           scores 49 (the strongest opening pair of any palette tested); every
           palette's 5th hue sits at or below the 12 floor. A 5th series goes
           to a second panel (a second figure, S8-6). Gate G-FIGSERIESCAP,
           advisory AMBER; series_defaults() still raises only above 8, so no
           existing draw code changes behaviour.
       13. COLOUR AS CONTENT (v5.80). When the stem or any option interrogates
           a colour — any colour word, or colour / pigment / dye / chromophore /
           litmus / flame-test vocabulary; `fc.colour_is_content(stem,
           options)`, word-bounded, possessive surnames (Green's) excluded, and
           element names that are also colour words (silver, gold) and bare
           chemistry vocabulary (indicator, precipitate, complex) deliberately
           NOT triggers — they interrogate a colour only when a colour word
           accompanies them, and a needless trigger would strip every AgNO3
           question of its atom colours — EVERY FigureSpec of that question
           (problem, stim and each option canvas) is authored with
           `colour_content=True`, and render_figure() forces a MONOCHROME
           render: palette AND the series copy handed to the draw_fn are
           black, and a structure draw_fn (which blits a raster and reads
           neither) is asked for black atoms; render_option_set() spreads the
           flag across a set so one option can never stay coloured. Colour IS
           the examinable content there and showing it is a leak. G-FIGACCENT
           and G-FIGCOLOUR are exempt for such a figure
           (monochrome by design); gate G-FIGCOLOURCONTENT confirms the PNG is
           monochrome; AMBER; silent without `colour_profile`.
       14. ELEMENT-COLOUR UNIFORMITY (v5.80). Heteroatom colour in a STRUCTURE
           option set is used ONLY when every option carries the same
           coloured-element set; otherwise render_option_set() switches EVERY
           option to black BEFORE pass 1 (structure_draw_fn exposes
           `.coloured_elements` / `.set_element_colours`), and writes the
           decision as `element_colours` ("uniform" | "black") on every spec.
           The decision only ever DOWNGRADES: a set whose options were all
           authored with `element_colours=False` is honoured as black, never
           recoloured, and a set whose authored modes differ is black. Three
           hydrocarbons and one alcohol therefore never render with one
           vermillion O. Gate G-FIGOPTELEM (set-level, like G-FIGOPTUNIF)
           reports a set whose decisions disagree: VOID_ITEM — an answer-cue
           leak voids the ITEM, never the run — and it is in
           NEVER_BLOCKING_ON_COLOUR like every colour gate. A problem figure
           (no option set) keeps its heteroatom colours; a hatch or fill
           vocabulary that differs across options is the same Q7b.6 breach.
    Q8. GEOMETRY ONLY + CANONICAL NAME (v4.3, R-MATH-OMML). The figural raster
        path renders GEOMETRIC FIGURES ONLY — never an algebraic/symbolic
        expression (those are OMML, §10-S10-4). Every emitted image MUST be named
        by the canonical convention so the audit can tell a figure from a stray
        raster:
          • problem/series figure : "q{N}_problem.png"  (or "q{N}_problem_{k}.png")
          • option figure         : "q{N}_opt{i}.png"   (i = 1..n_options)
          • linked-stimulus chart : "q{N}_stim.png"     (or "q{N}_stim_{tag}.png")
        Any other inline-image name (e.g. "q{N}_e1.png" for a rasterised
        expression) is an UNAUTHORISED raster and fails gate G-MATH-RASTER.
        render_figural_image() calls assert_not_math() on the figure's name/label
        and enters LADDER-REPAIR R1 [HS:LADDER] if handed a math expression.
    Q8b. SEVERITY — NO COLOUR CONDITION MAY EVER HALT A RUN (v5.33, owner
        directive). This is not a concession to convenience; it is this
        framework's own doctrine, stated in CLAUDE.md: "A CLASS T failure must
        be LOUD, and must NOT halt. These are separate properties and the corpus
        conflated them... Silence is the defect; a halt is not the remedy." A
        grey figure is a DEGRADED paper, never a void one. Three modes, defined
        in figural_core.SEVERITY:
          AMBER      — report as an AMBER WARN line (v5.89: no longer a FAIL —
                       a FAIL made the auditor exit 1 and S13-4c then stopped the
                       run, which contradicted "ALWAYS complete"; GAP-2026-11-02
                       G1), force the amber delivery footer (Framework_
                       DeliveryFooter §5 — triggered by the certificate's
                       amber_notes, not by the exit code), ALWAYS complete. Every
                       colour and accessibility ADVISORY on a non-chemistry
                       figure lives here: G-FIGCOLOUR, G-FIGCVD, G-FIGSERIES,
                       G-FIGGLYPH, G-FIGALT, W-FIGLABELPX, and the legacy
                       W-FIGOVERPRINT / W-FIGBONDORDER notes.
          VOID_ITEM  — the rendering leaks an ANSWER CUE or is unreadable, so
                       this QUESTION is invalid: G-FIGMONO (colour in a
                       reasoning glyph), G-FIGOPTUNIF (option canvases not
                       uniform), and from v5.55 G-FIGCOLLIDE (labels
                       overprinted — an option a candidate cannot read is not
                       a degraded option, it is an unanswerable one) and
                       G-FIGOPTWINDOW (options drawn at divergent scales, so
                       relative size — which in a structure question is
                       MEANING — became a renderer artefact). From v5.89 also
                       G-FIGMARK, G-FIGOVERPRINT, G-FIGBONDORDER, G-FIGLABELPX
                       and G-FIGOPTELEM. v5.89: VOID_ITEM means REPAIR THE ITEM
                       IN PLACE through the REPAIR LADDER (§Q8b-LADDER below) at
                       the entry rung bc.LADDER_ENTRY_RUNG gives. "Drop" is
                       DELETED (GAP-2026-11-02 G5): the question count and the
                       allocation are always kept. The paper continues. Never
                       halts the run.
          BLOCKING   — reserved for RENDERER-CONTRACT REGRESSION on v5.33+
                       output only: G-FIGSCALE, G-FIGLABEL, G-FIGDPI,
                       G-FIGDEGEN, and from v5.55 G-FIGFIT. G-FIGFIT is safe to
                       block for the same reason the other four are: on v5.55+
                       output the renderer GUARANTEES the property, so a firing
                       means someone removed the fitter. EC-V18 downgrades it to
                       AMBER for every pre-v5.55 figure (no fit record), so ~200
                       existing exams keep auditing and delivering untouched
                       while still reporting the defect loudly. These are safe to
                       block ONLY because they are
                       unfireable by construction — verified 0 firings across
                       144 figures spanning 1.3–7.5 in, 2–8 series and four
                       label sets including full scientific notation. A firing
                       means someone reintroduced headroom or a tight bbox.
                       v5.89 (GAP-2026-11-02, §Q8b-LADDER L6): "BLOCKING" now means
                       the FIGURE may not ship as drawn — never that the RUN stops.
                       A BLOCKING firing is an item finding repaired through the
                       ladder (G-FIGLABEL / G-FIGFIT enter at R1 per L1; G-FIGSCALE,
                       G-FIGDPI, G-FIGDEGEN at R1 via bc.LADDER_ENTRY_RUNG). The
                       native renderer CAN fire G-FIGLABEL (overflow down-scaling),
                       so the "unfireable" note above applies to the matplotlib path
                       only. A firing that survives sweep 4 of S13-2F is [HS:INFRA].
        EC-V18 LEGACY TOLERANCE, NON-NEGOTIABLE: output with no FigureSpec
        sidecar predates v5.33. Every BLOCKING gate downgrades to AMBER for it,
        so roughly 200 existing exams keep auditing and delivering untouched
        while still reporting the defect loudly. figural_core.triage() NEVER
        raises and NEVER halts.

    §Q8b-LADDER — THE REPAIR LADDER (v5.89 — GAP-2026-11-02 §4; owner decision
        O4). REQ: no defect reaches a delivered paper AND no run stops for a
        quality reason. A defect is made impossible by construction or repaired
        automatically before delivery. The ladder runs at S7 per slot (after
        render, before the sidecar write) and at S13-2F (pre-commit sweep).
        Every spec line tagged [HS:LADDER] — and every engine/gate message that
        begins "LADDER-REPAIR R<n>" — is an ENTRY into this ladder for the named
        item at rung R<n>, never a run stop. Catch such a RuntimeError, read its
        rung and reason, repair, continue.

        | Rung | Action | Attempts |
        | R1 | Deterministic re-render, NO new content, in this order: recompute
        |    | tokens -> re-flow the scheme -> re-render the whole option set at a
        |    | larger common width (non-native options) -> remove undeclared
        |    | decorations -> alternative mark device / rotation -> drop
        |    | abbreviations -> toggle depictor. Also every formatting repair the
        |    | [HS:LADDER R1] rules name (strip a key, re-emit OMML, re-embed a
        |    | stimulus, reorder Q.N-first, ...). | each action once, then re-gate |
        | R2s| (v5.90) Rewrite the STEM only — figure, options and key unchanged.
        |    | Entry for G-STEMLEAK / G-STEMFORM / G-CONSIST. | <= 3 |
        | R2o| (v5.90) Regenerate one or more OPTIONS only — the key's content is
        |    | unchanged. Entry for G-OPTDISTINCT / G-DISTRACTOR / G-STEREODECL /
        |    | G-ITEMRULE (LONGEST_KEY / MIDDLE_VALUE_KEY: rebalance wording). | <= 3 |
        | R2 | Regenerate the SAME item: same subtopic, band and ask type; every
        |    | failure reason passed in as a constraint. v5.92 (DL-47): for a LEVEL
        |    | item two further REJECT reasons enter here — figure complexity below
        |    | the subtopic's measured p10 (bc.content_vector size fields against
        |    | LEVEL_TARGETS[sid]['figure_complexity_pct'], S3-12e) and option
        |    | closeness below its p50 (bc.option_closeness mean against
        |    | LEVEL_TARGETS[sid]['closeness_pct']['p50']; a target that is
        |    | 'unmeasured' or absent gives no reason);
        |    | both named in the brief as constraints ("a larger / more constrained
        |    | substrate", "wrong options one decision from the key"). | <= 3 |
        | R3 | Regenerate: same subtopic and band; the next ask type that is
        |    | under target and valid for the subtopic (bc.assign_ask_type).
        |    | Skipped when none exists. | <= 3 |
        | R4 | TERMINAL, reducible subtopic: TEXT-format item of the same
        |    | subtopic and band (S7-NEW-B OPTION B / REPLACEMENT_RULE) — ONLY IF
        |    | bc.axis_safe_text_fallback(observed, target, ...) is True, i.e. the
        |    | paper still passes A-AXIS1 after the swap. Otherwise R4'. | own loop |
        | R4'| TERMINAL, irreducible subtopic OR axis-unsafe swap: the SIMPLEST
        |    | CONSTRUCTIVE FIGURE. chem-R: one structure in the stem or none; the
        |    | blueprint's total_options single-molecule options; no marks, no
        |    | abbreviations, native raster; molecules chosen so the natural width
        |    | at the role tokens is <= FIG_COLUMN_IN, checked from the 2-D
        |    | coordinate span BEFORE drawing (overflow impossible). Other figure
        |    | types: the subtopic's most frequent object_type by its existing
        |    | renderer at minimal complexity. v5.92 (DL-43/58): R4' simplifies the
        |    | LAYOUT only — never the chemistry; after the repair the level vector
        |    | is RE-MEASURED (bc.level_vector / bc.level_check as in CHECK 3c (b1))
        |    | and the item keeps its slot only if lc['status'] is still 'ok'; a drop
        |    | to 'below' is a level finding settled by R5, never a silent pass. DL-48:
        |    | on a WIDTH overflow of structure options, the TWO-ROW option layout
        |    | (2 x 2 panels, S10-8 multi-panel path) is tried BEFORE R4' — it keeps
        |    | the chemistry intact. The CCP size target is waived here. | <= 3 |
        | R5 | LAST RESORT, only for a reason still failing after R4/R4':
        |    | content level HARDER or LOWER than the slot -> v6.0 (LAW-ORG-3 / -5):
        |    | the item is NEVER held, swapped or relabelled; it is a failed
        |    | candidate and the slot is carried to S13-2L's SC2 difficulty chain
        |    | (rework, replace, shape, sibling, reserve_refill, refill_session,
        |    | bounded last_resort); the blueprint is NOT amended. [The v5.96 HOLD
        |    | at the scheduled band is retired for papers of this release.]
        |    | Render defect on ANY R4' figure (chemistry included), or a key never verified ->
        |    | REASSIGN the slot to another in-scope subtopic (same topic first,
        |    | largest allocation first, then same section) that keeps every
        |    | manifest group constraint (G-ALTGROUP / G-GROUPMANDATE /
        |    | G-MINCOUNT); amend subtopic q_count in the in-run blueprint, update
        |    | alloc_ids and subtopic_by_qnum in the same step, log it in
        |    | allocation_amendments[], then persist_bp_amendment(). A candidate
        |    | qualifies ONLY if it keeps the slot's qtype (MCQ/MSQ/NAT), answer
        |    | type, cardinality, Axis-1 format and stimulus-group membership
        |    | (a slot inside a linked set is never reassigned — the set is
        |    | rebuilt at R2 instead) and stays inside its answer-position budget. Each candidate subtopic goes through
        |    | R2 -> R4/R4'. | <= 3 candidate subtopics |

        Rules:
          L1. Entry rung per finding: bc.ladder_entry(reasons) over
              bc.LADDER_ENTRY_RUNG (R1: W-FIGLABELPX / G-FIGLABEL / G-FIGLABELPX
              on a native or raster structure, G-FIGCOLLIDE, G-FIGOVERPRINT,
              G-FIGBONDORDER, G-FIGMARK, G-FIGOPTUNIF, G-FIGOPTWINDOW, G-FIGFIT,
              overflow; R2s: G-STEMLEAK, G-STEMFORM, G-CONSIST; R2o: G-OPTDISTINCT,
              G-DISTRACTOR, G-STEREODECL, G-ITEMRULE; R2: G-FIGMONO, G-FIGOPTELEM,
              A-CONTENTLEVEL, A-DIFFRATING, A-FIGFORMAT, G-MEDIAREUSE, G-ENTITYLEAK
              (the LATER item), key verification, review disagreement; R3:
              G-SHAPEMIX, G-TEMPLATE — bc.LADDER_RUNG_ORDER R1 < R2s < R2o < R2 <
              R3 < R4 < R5). Several reasons -> the lowest rung first; all reasons
              travel to the next attempt. R4 / R4' items are EXEMPT from G-SHAPEMIX /
              G-TEMPLATE counts and from the near-isomer floor (R6.3 f), NEVER from
              G-OPTDISTINCT, G-ENTITYLEAK (a), G-STEMLEAK, G-DISTRACTOR (a)-(c) or
              G-CONSIST.
          L2. No accept-best for defects. S7-STYLE author_slot's accept-best on
              budget keeps its seven STYLE reasons only. Ladder attempts do NOT
              consume max_retries_per_paper.
          L3. The in-run blueprint (BP_SRC_PATH) is the one the auditor reads
              (--blueprint BP_SRC_PATH), so A-QINDEX's exact count check (G-QINDEX
              check 6), A-COUNT and A-DPROFILE see the amended schedule and
              allocation and stay exactly consistent. EVERY R5 amendment (allocation;
              v5.96: never difficulty — a harder slot is HELD) is followed at once by persist_bp_amendment() (S3-2D),
              which writes bp to BP_SRC_PATH — an amendment held only in memory is a
              defect (the auditor and S13-6 read the FILE). A resumed run keeps the
              amended in-run file (S3-1).
          L4. Disclosure: R4 / R4' / R5 items are listed in the delivery footer
              (Framework_DeliveryFooter §LADDER); R1-R3 go to
              registry.question_index[].ladder = {rung, reasons[], attempts} —
              passed as write_q_to_sidecar(ladder=...) (re-written when a later
              rung repairs the item) — and the audit report.
          L5. Systemic flag: >= 3 items of one paper reaching a terminal rung for
              the same finding -> footer line "systemic: <finding>" and a GAP stub
              in the audit report. The paper still completes.
          L7. (v5.96, owner decision OD-2026-11-09 — supersedes OD-9) A QUALITY or
              RULE finding still failing after the terminal rung does NOT stop the run,
              is NOT stamped UNRESOLVED and never makes a paper NOT CERTIFIED: S13-2F
              (bc.sweep_route) sends the slot into its SLOT CHAIN (S13-2L / S13-2R —
              replacement, another ask shape, a sibling subtopic); v6.0 (LAW-ORG-3): an
              exhausted chain ends by REPLACEMENT (reserve_refill -> refill_session ->
              last_resort with a fully verified item) — no item of a paper produced by this
              release is delivered DISCLOSED; the paper is CERTIFIED. [DISCLOSED stays only
              as the recorded outcome of chains of papers delivered before 2026.11.10.]
              Only a bc.INFRA_GATES fault (a broken tool) is [HS:INFRA], self-healed
              first (bc.infra_heal_step).
          L6. The ONLY remaining run stops are INFRASTRUCTURE faults ([HS:INFRA]:
              engine missing or failing its self-test, bootstrap failure, a
              corrupt/unreadable file, the docx changed after its item-sweep
              certificate) and pre-generation INPUT faults ([HS:INPUT]). If three
              R5 candidate subtopics all fail KEY VERIFICATION for one slot, the
              key verifier itself is suspect — that is classed [HS:INFRA] ("key
              verifier failing") and reported with every attempt.
    Q9. LABEL CONTRACT (v5.33 — new). The property the owner actually
        complained about, and the one no rule previously covered.
        1. ON-PAGE LABEL FLOORS, AT DISPLAY SIZE — not on the native canvas:
             data_series / data_single / schematic : 9 pt
             reasoning_glyph / option_canvas       : 8 pt
             target for all classes                : 10 pt
           axis titles ≥ tick labels. A floor declared on the native canvas is
           NOT this rule and does not satisfy it: under the pre-v5.33 contract a
           canvas-side floor was still halved at placement.
        2. Every axis MUST carry a title, including UNITS where the quantity is
           dimensional.
        3. Every series MUST be identified either by a direct label adjacent to
           the mark, or by a legend — and where a legend is the SOLE key, Q7b.2
           applies with no exception.
        4. The figure font MUST cover the exam's glyph set, at minimum:
           `µ ⁻² ₂ Å ° α β θ × ⇌ ≥ ≤ ‰ Δ λ`. A missing glyph renders as a tofu
           box and is a HARD failure. Gate G-FIGGLYPH.
        5. Every drawing MUST carry `wp:docPr/@descr` alt text naming the
           question number, the figure class and the quantities plotted.
           Measured 0 of 208 on the delivered exhibits. Emitted by S10-8 from
           `figural_core.alt_text()`. Gate A-FIGALT (AMBER — never halts).
        6. HOW THIS IS GATED. G-FIGLABEL is ARITHMETIC over the font sizes
           ACTUALLY USED at render time, recorded into the FigureSpec sidecar,
           multiplied by the recorded placement scale. It MUST NOT be gated on
           pixel connected components. Verified counter-example: three renders
           at an identical 10 pt request, identical 1304 px saved width and
           identical scale — the one whose axis titles carried
           "µmol photons m⁻² s⁻¹" and "Net CO₂ assimilation" measured 8.5 pt
           while short-label renders measured above the floor. Superscripts and
           subscripts are small connected components that drag the median down,
           so a pixel gate is biased against exactly the notation Q9.4
           mandates, and would fail conformant chemistry, biology and physics
           papers hardest. The pixel statistic is retained as a WARN-level
           cross-check only (`figural_core.g_figlabel_pixels`).

    Q10. FIT CONTRACT (v5.55 — new). THE INK MUST LAND INSIDE THE FRAME.
        1. After draw_fn returns and BEFORE the artefact is saved, the renderer
           MEASURES every visible artist's rendered extent (matplotlib
           get_window_extent) and fits the data window so the union of those
           extents clears the axes box on every side by >= FIG_MIN_CLEARANCE_IN
           at DISPLAY size. This is figural_core.fit_and_deconflict(), called
           from render_figure(). It is not optional and not per-class.
        2. The fit also MAXIMISES fill: the window is scaled by exactly the
           factor that makes content + 2 x clearance meet the axes box, so a
           figure occupies the page area it was allocated. The delivered corpus
           averaged 29.6% — a molecule drawn at roughly half the linear size its
           4.0 in slot paid for, which is most of why labels were illegible.
           Floor MIN_CONTENT_FILL_FRAC, evaluated on the SET for a shared-window
           option set (the union window is by definition larger than any single
           option; gating per option would fire on every conformant set).
        3. Text extents do NOT scale with the data window — font size is in
           points — so one pass is not a proof. The fitter re-measures and
           iterates, bounded by FIG_FIT_MAX_PASSES, and RECORDS what it achieved
           rather than asserting what it attempted.
        4. THE FRAME BELONGS TO THE RENDERER. draw_fn MUST NOT draw the option
           border box. Through v5.54 it did, so a label with a white masking
           bbox drawn afterwards erased a segment of the border — the visible
           white gap in the delivered frames. figural_core.draw_frame() now
           draws it LAST, at axes-fraction coordinates, at the canvas edge, with
           zorder above every content artist. A label can no longer punch a hole
           in it, and it can no longer float in the middle of the canvas leaving
           a dead margin (measured: the frame held 64.6% of the canvas width).
        5. GATED BY ARITHMETIC, NOT PIXELS. G-FIGFIT reads the fit record in the
           FigureSpec sidecar, for the reason Q9.6 gives: the renderer already
           holds the exact extents, and re-deriving them from pixels
           re-introduces the superscript/subscript bias. W-FIGFITPX is the
           WARN-level pixel cross-check, and is the ONLY figure gate that works
           on a delivered .docx with no sidecar — which is what makes the
           existing ~200 exams auditable without re-rendering them.
        6. ASPECT (v5.81 — GAP-2026-08-30-FITTER-ASPECT). The window's data-unit
           aspect is forced to the axes box aspect ONLY on an aspect-locked axes
           (set_aspect('equal') or a number; imshow() sets it — every structure
           and schematic). On an 'auto' axes — every ordinary chart — the fitted
           window is applied AS GIVEN and x and y are scaled by their OWN
           factors: forcing a data-unit aspect there widened x ~17x on a chart
           whose y spanned 70 units and x spanned 4, and collapsed the bars.
           An author who needs a locked aspect on a chart sets it explicitly.
        7. TOLERANCE (v5.81). The fitter converges to within half a rendered
           pixel (its own `clear_px - 0.5` criterion); G-FIGFIT therefore
           tolerates FIG_FIT_TOL_IN = 0.5 / FIGURAL_DPI below the floor, no
           more. A clearance of 0.04993 in against a 0.050 in floor is a pass,
           as it always rendered.
        8. EVERY GATE IS PRINTED (v5.81 — audit_canonical v2.25). Step 8 emits
           one verdict line per figure gate figural_core can raise — the 13
           pre-v5.55 gates, G-FIGFIT / G-FIGCOLLIDE / G-FIGINK / W-FIGINK /
           W-FIGFITPX / G-FIGOPTWINDOW, and the five v5.80 colour gates — and
           evaluates the SET-level gates (G-FIGOPTUNIF, G-FIGOPTWINDOW,
           G-FIGOPTELEM) per question on the option set. A gate that is
           evaluated and not printed is the defect Step 8 exists to prevent.
    Q11. LABEL DECONFLICT (v5.55 — new). NO LABEL MAY OVERPRINT ANOTHER.
        1. The renderer detects text-vs-text and text-vs-stroke overprints from
           measured extents and separates them by repulsion, alternating with
           the Q10 fit until both hold on the SAME measurement.
        2. A label may be nudged at most FIG_LABEL_MAX_SHIFT_IN from its
           authored anchor. THIS CAP IS THE POINT. A label dragged far enough to
           satisfy a gate is no longer naming the atom it was attached to — a
           wrong figure that passes, which is strictly worse than a reported
           collision. When the cap binds, the renderer STOPS and REPORTS.
        3. A label sitting ON a stroke is legitimate ONLY when it masks it (an
           opaque bbox behind an atom label is standard chemical drawing).
           Anything else is an overprint.
        4. ESCALATION, bounded: if lateral repulsion cannot separate labels that
           are nearly COLLINEAR with the figure centre, the whole label ring is
           expanded outward about the content centroid in three 10% steps. This
           increases arc length between neighbours without changing which bond
           any label points down, so no label changes meaning, and the Q10 fit
           rescales so the figure does not grow on the page. After three steps
           the renderer stops and reports.
        5. Residual overprints fail G-FIGCOLLIDE at VOID_ITEM. The question is
           regenerated; the RUN NEVER HALTS (CLAUDE.md: silence is the defect;
           a halt is not the remedy).
    Q12. ONE WINDOW PER OPTION SET (v5.55 — new). Every option of a question is
        rendered in the SAME data window on the SAME canvas, via
        figural_core.render_option_set(). Two passes are structurally necessary:
        the common window is not knowable until every option has been drawn and
        measured once.
        WHY THIS IS A CORRECTNESS GATE, NOT A TIDINESS ONE. Fitted
        independently, a small molecule is magnified to fill its box and a large
        one shrunk, so RELATIVE SIZE — which in a structure question is meaning —
        becomes an artefact of the renderer, and any option drawn at a visibly
        different scale is an answer cue. Q7b.6 already forbids a differing style
        budget; Q12 closes the identical hole on geometry. Gate G-FIGOPTWINDOW
        (VOID_ITEM). render_figure() alone is correct for a PROBLEM figure and
        INSUFFICIENT for an option set.
        Q12.1. THE SET ASPECT COMES FROM STROKE GEOMETRY (v5.61,
        GAP-2026-08-22-FIGASPECT-SELF-FULFILLING). v5.55-v5.60 "derived" the
        set's canvas aspect from the union of pass-1 data_windows — but the
        fitter had already inflated every window to the canvas aspect pass 1
        rendered on, so the derivation returned the default it started from: a
        square molecule set stayed on a 0.72 landscape canvas, filled 41% of it
        (floor 45%), and G-FIGFIT BLOCKED a correct drawing; worse, an authored
        canvas_aspect on the specs was silently clobbered, disabling the
        documented workaround exactly where it was needed. From v5.61 the fit
        record carries the raw ink extent (fit.content_window) and the
        Text-excluded stroke extent (fit.stroke_window), both in DATA
        coordinates; the set aspect is derived from the STROKE union (pure,
        zoom-invariant geometry — a hexagon set derives 1.1547 = 2/sqrt(3)
        exactly), falling back to content, then window, union only when no
        stroke ink exists. A canvas_aspect declared IDENTICALLY on every spec
        of the set is the author's decision and is honoured EXACTLY. Pass 2
        seeds from the content union, never the pass-1 window union. Authoring
        guidance unchanged: declare nothing and the canvas now genuinely
        follows the structure's shape.
    Q13. THE CENSUS MUST AGREE WITH THE PIXELS (v5.57 — new). Q10 is arithmetic over
        the fit record, and it is only as good as the artist census that fed it. The
        census is now complete by construction (degenerate extents kept, Annotation
        arrows, ax.artists, tables and legend walked) and the fit record carries the
        measured content box in saved-pixel coordinates (fit.content_bbox_px,
        axes_bbox_px, axis_on). Gate G-FIGINK then reads the SAVED PNG and asks one
        question: does any content ink lie OUTSIDE the box the fitter measured?
        1. WHY THIS DOES NOT REOPEN Q10.5. The Q9.6 extent bias makes a measured box
           LARGER than the ink, never smaller, so "ink outside the measured box" can
           never be a bias artefact. It is strictly evidence of a render path the
           census did not see — which is the only way the shipped defect can arise.
        2. SEVERITY. BLOCKING on an axis-OFF render (every schematic, option canvas
           and glyph): no chrome can exist inside the axes box there, so outside
           ink is a defect. AMBER (W-FIGINK) on an axis-ON render, where gridlines
           and minor ticks may legitimately sit inside; the comparison is confined
           to the axes-box interior minus the spine band in both cases.
        3. LEGACY. A pre-v5.57 render carries no content_bbox_px. On a FRAMED canvas
           the same check runs in its edge form — content ink inside the
           FIG_MIN_CLEARANCE_IN band the v5.55 fitter guaranteed clear — as AMBER,
           the EC-V18 posture. Unframed legacy renders are silent. This is what
           makes the ~200 delivered exams auditable for the defect: on the
           reference paper it flagged five option canvases and nothing else.
        4. draw_fn RULES THAT FOLLOW. A bond may be drawn by any idiom; the census
           now sees all of them. But a draw_fn MUST NOT call ax.set_aspect() —
           the fitter owns window and aspect through apply_data_window(), and an
           author-set aspect insets the axes box inside the canvas so the frame no
           longer sits at the canvas edge.
        5. REPAIR IS A RE-RENDER. A flagged figure is never patched; the question's
           figures are regenerated under v5.57 and re-gated.

  RENDER HELPER — WHICH ONE (v5.33; option sets amended v5.55).
    Classes `data_series`, `data_single`, `schematic` route to
    `figural_core.render_figure()`. Classes `reasoning_glyph` and
    `option_canvas` (when the parent is a reasoning glyph) use
    `render_figural_image()` below.
    ```python
    import figural_core as fc

    stem, options = "...", ["...", "..."]   # this question's stem and option texts
    spec = fc.make_figure_spec(qnum, "data_series", fc.FIG_PROBLEM_DISPLAY_IN,
                               series=fc.series_defaults(2),
                               axes={"x": {"title": ..., "units": ...},
                                     "y": {"title": ..., "units": ...}},
                               key_mode="legend",
                               # v5.80 Q7b.13 — a colour-interrogating stem
                               # renders monochrome; always pass it.
                               colour_content=fc.colour_is_content(stem, options))
    # v5.80: inside draw_fn, coloured text -> fc.text_ink(palette[i]);
    # fills -> ax.bar(..., **fc.fill_style(k)); <= 4 chromatic series (Q7b.12).
    fc.render_figure(draw_fn, png_path, spec)   # MUTATES spec with png_px,
                                                # png_dpi, placed_in,
                                                # placement_scale, font_pt_native
                                                # and (v5.55) spec['fit']
    fc.write_spec_sidecar(spec, png_path)       # the audit reads this
    ```
    OPTION SETS USE render_option_set(), NOT render_figure() IN A LOOP (Q12):
    ```python
    import figural_core as fc

    stem, options = "...", ["...", "..."]   # this question's stem and option texts
    opt_specs = [fc.make_figure_spec(qnum, "option_canvas",
                                     fc.FIG_OPT_DISPLAY_IN, role="option",
                                     # v5.80 Q7b.13 — on EVERY spec of the question
                                     colour_content=fc.colour_is_content(stem, options))
                 for _ in draw_fns]
    fc.render_option_set(draw_fns, opt_paths, opt_specs)   # ONE shared window
    for _s, _p in zip(opt_specs, opt_paths):
        fc.write_spec_sidecar(_s, _p)
    ```
    `render_figure()` reads the saved artefact back and records what actually
    happened. The audit then verifies the figure WITHOUT looking at it: colour
    presence, hue count, luminance and deuteranope separation, placement scale,
    on-page label size, DPI metadata and alt text are all deterministic
    arithmetic over the PNG and its sidecar. Only "does this render actually
    DEPICT a micrograph" needs eyes, and that alone remains CLASS T.

  GEOMETRY-GLYPH HELPER (returns lossless PNG bytes; one call per visual unit):
  ```python
  import io
  import matplotlib
  matplotlib.use("Agg")
  import matplotlib.pyplot as plt

  def render_figural_image(draw_fn, kind="option", *, name="", bg="transparent"):
      """
      draw_fn(ax) draws ONE visual unit using geometry only (no stem/option text).
      kind = "option"  -> uniform fixed square canvas (no tight crop); boxed.
      kind = "problem" -> single wider unit; tight bbox allowed.
      name = the canonical image name (Q8): q{N}_problem[_k] / q{N}_opt{i} /
             q{N}_stim[_tag]. REQUIRED so the audit name-contract is satisfiable.
      Returns PNG bytes at FIGURAL_DPI with headroom. Caller embeds at the
      display size below (so the on-page image is supersampled = crisp).
      """
      # v4.3 R-MATH-OMML LADDER-REPAIR R1 [HS:LADDER]: the figural path is geometry-only. A built-up
      # algebraic expression must NEVER be rasterised — route it to OMML (S10-4).
      assert_not_math(name)
      transparent = (bg == "transparent")
      if kind == "option":
          # v5.33: figsize == the display size, EXACTLY. The old line was
          #   side_in = max(FIG_OPT_DISPLAY_IN * FIG_NATIVE_HEADROOM, 2.0)
          # which, with headroom retired to 1.0, resolves to max(1.3, 2.0) = 2.0in
          # while placement is still 1.3in — S = 0.65 and gate A-FIGSCALE fires
          # BLOCKING on every option canvas. The 2.0 floor was a residue of the
          # old Q3, which gave two incompatible pixel floors in one rule.
          side_in = FIG_OPT_DISPLAY_IN
          fig, ax = plt.subplots(figsize=(side_in, side_in))
          ax.set_xlim(0, 1); ax.set_ylim(0, 1)
          ax.set_aspect("equal"); ax.axis("off")
          from matplotlib.patches import Rectangle
          ax.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, fill=False,
                                  lw=FIG_MIN_STROKE_PT, edgecolor="black"))
          draw_fn(ax)
          buf = io.BytesIO()
          # v5.33 Q2: opaque white, always. `transparent` is retained in the
          # signature for call compatibility and deliberately ignored.
          plt.savefig(buf, format="png", dpi=FIGURAL_DPI, transparent=False,
                      bbox_inches=None, pad_inches=0, facecolor="white")
      else:  # problem / series unit
          # v5.33: figsize == the display size and bbox_inches=None, so
          # saved_px == display_in x FIGURAL_DPI exactly and S == 1.0.
          # This branch previously multiplied by FIG_NATIVE_HEADROOM and saved
          # with bbox_inches="tight" — the two halves of RC-2 in three lines.
          # Tight trimming made the saved width a function of the drawing's own
          # content, which is why 31 delivered problem figures produced 27
          # distinct canvas sizes and S wandered 0.495-0.666.
          fig, ax = plt.subplots(figsize=(FIG_PROBLEM_DISPLAY_IN,
                                          FIG_PROBLEM_DISPLAY_IN * 0.8))
          ax.set_aspect("equal"); ax.axis("off")
          draw_fn(ax)
          buf = io.BytesIO()
          plt.savefig(buf, format="png", dpi=FIGURAL_DPI, transparent=False,
                      bbox_inches=None, pad_inches=0,
                      facecolor="white")
      plt.close(fig)
      buf.seek(0)
      return buf.read()

  def assert_uniform_options(option_pngs):
      """All option images MUST be the same native pixel size (Q4)."""
      from PIL import Image
      sizes = {Image.open(io.BytesIO(b)).size for b in option_pngs}
      if len(sizes) != 1:
          raise AssertionError(f"G-FIGURAL option canvases not uniform: {sizes}")
  ```

## S10-7C — DOMAIN DRAWING CONTRACT (v5.55 — new)

  WHY A LAYOUT ENGINE IS NOT ENOUGH. Q10/Q11 measure and repair what draw_fn
  produced. They cannot repair a drawing whose labels are superimposed BY
  DEFINITION. The reference case: an ECLIPSED Newman projection places front and
  rear substituents at the same dihedral angle, so their labels coincide, and no
  amount of nudging separates them within FIG_LABEL_MAX_SHIFT_IN. Measured: with
  the rear bonds drawn at a 14 deg offset, 1-2 residual overprints survive every
  escalation step and G-FIGCOLLIDE correctly voids the item. At 30 deg, all four
  options of the reference question resolve to ZERO collisions and pass
  G-FIGFIT, G-FIGCOLLIDE and G-FIGOPTWINDOW together.

  The arithmetic is not exam-specific and is worth stating once. On a 1.3 in
  option canvas at 300 dpi, an 8-10 pt "CH3" glyph run is ~33-41 px wide. Six
  substituents on a ring of ~106 px radius sit ~106 px apart when STAGGERED (60
  deg) and ~26 px apart at a 14 deg eclipse offset. 26 < 41, so the collision is
  geometric certainty, not bad luck.

  THE CONTRACT — mandatory for any draw_fn that carries text labels:
    C1. NEVER draw the option border box. It is the renderer's (Q10.4).
        v5.89: the renderer draws it only when the exam's PYQ options are framed
        (FIGURE_STYLE_PROFILE.option_frame measured True) or, for a non-chemistry
        option canvas, when the profile is unmeasured (today's behaviour). A
        native chemistry option canvas is never framed without that evidence.
    C2. NEVER hand-fix the axis limits and never call bbox_inches="tight".
        The window is the fitter's (Q10.1). A draw_fn that sets its own limits
        is asserting a fit it did not measure.
    C3. Two labels MUST NOT be placed at an angular separation that is smaller
        than their own rendered width at the radius used. In practice, for a
        radial label ring: separate by >= 25 deg, OR place the inner group on a
        radius >= 1.35x the outer group's.
    C4. Eclipsed / syn-periplanar conformers are drawn with the REAR bonds
        offset by 25-30 deg — the universal textbook convention, and the only
        one that keeps both substituents visible. Never at 0 deg.
    C5. An atom label that lies over a bond MUST carry an opaque mask bbox
        (that is what makes it a label and not an overprint — Q11.3).
    C6. Take accent ink from the `palette` argument, never a hardcoded hue
        (Q7b.8 authoring contract — restated here because this is the section
        an author reads before drawing).
    C7. (v5.80) Every coloured TEXT run uses `fc.text_ink(hue)`; every fill
        uses `fc.fill_style(k)`; orange, sky and yellow never appear as text or
        thin strokes (Q7b.9-Q7b.11). A heat map or gradient uses the viridis
        family only (perceptually uniform; rainbow/jet is banned — Crameri,
        Shephard & Heron 2020).
    C8. (v5.80; v5.89 REWRITTEN — GAP-2026-11-02 F1, owner decision O1)
        STRUCTURES are drawn PRINT-TRUE in the EXAM'S OWN STYLE:
          • `cio.structure_draw_fn(smiles, tokens=TOK[role], marks=..., 
            abbreviations=ABBREV, protect_atoms=...)` and
            `cio.render_scheme(scheme, tokens=TOK['problem'])` are the ONLY
            structure renderers; TOK = {'problem': fc.structure_tokens(PROFILE,
            'problem'), 'option': fc.structure_tokens(PROFILE, 'option')}
            computed ONCE per paper at S3 from PROFILE =
            fc.load_style_profile(section_rules.md). One token set per role per
            paper -> every structure of a role has ONE bond length.
          • MONOCHROME when the exam's PYQs are monochrome or there is no
            evidence (tokens['monochrome']); atoms coloured from
            figural_core.ATOM_PALETTE only when the PYQs were MEASURED coloured.
          • The PNG is placed at its natural width (scale 1.0). Overflow
            (natural width > FIG_COLUMN_IN = 6.0 in), in this order: re-flow a
            multi-arrow row (the break tile is repeated); stack reagent text (<=2
            lines above and below, excess moved to the stem); scale the whole
            picture only while the atom label stays >= its class floor
            (G-FIGLABEL); otherwise the item enters the ladder with reason
            'overflow'.
          • ABBREVIATIONS only as the exam abbreviates (PROFILE.abbreviates True
            -> ABBREV = PROFILE.abbreviation_labels; False / unmeasured -> NONE).
            Never over a reacting atom (cio.abbreviation_protected_atoms), a
            group the stem names, or a marked site. The registered SMILES is the
            uncondensed canonical.
          • A quaternary carbon drawn as a 90-degree cross is re-depicted
            automatically (cross_note recorded if it cannot be).
          • PREFLIGHT: fc.ensure_native_raster(install=True) once at S3. If it
            reports available False, the LEGACY path is used unchanged
            (structure_draw_fn without tokens), every chem figure carries the
            AMBER footer note "renderer degraded", and its specs carry
            raster_content=True so an illegible label is still repaired
            (G-FIGLABELPX). Never a halt.
    C9. (v5.80; v5.89 REWRITTEN — GAP-2026-11-02 F2/F3) INTERROGATED SITE:
        HIGHLIGHT BANDS ARE RETIRED for structures — the v5.80 opaque band (6x
        line width) was measured overprinting O, Br, N and C+ labels and making
        single bonds read as double bonds, contrary to this clause's own claim.
        A site is marked ONLY when the stem names it (Q7b.8' MARK-IFF-NAMED) and
        ONLY with the declared device, passed as `marks=` to
        structure_draw_fn and as `marked_sites=` (with stem_phrase) to
        make_figure_spec. Devices: underline (a labelled atom or explicit H),
        asterisk / letter (any atom), arrow (bonds), bold (a bond redrawn as ONE
        heavier line, never offset). The renderer places each mark clear of every
        label and bond (8 rotations); G-FIGOVERPRINT (differential render) and
        G-FIGBONDORDER verify it. A figure whose stem names no site carries NO
        mark. Passing highlight_* in native mode is converted to marks and must
        then be declared like any other mark.
  A draw_fn that honours C1-C9 needs no repair; the fitter then only maximises
  fill. A draw_fn that does not is repaired where possible and REPORTED where
  not. Neither path can ship a silent defect, which is the whole objective.

## S10-8 — FIGURAL PLACEMENT (v4.0 — single-column, label-bound; was a v1.0 stub)

  Lays a figural MCQ into the docx as DISCRETE images. Enforces R-FIGURAL: stem is
  Q.N-first document text (R14); problem image(s) next; then the option images
  stacked ONE PER LINE, each bound 1:1 to its "i." label. There is exactly one
  image per option line — never two options on a line, never a table row of
  options, never a composite panel.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  from docx.shared import Inches, Pt
  import figural_core                     # v5.33 — alt_text() (S10-7 Q9.5)

  def _add_image_para(doc, png_bytes, width_in, spec=None):
      """Add a paragraph that holds EXACTLY ONE inline image (single-column).

      v5.33: width_in MUST come from the FigureSpec that rendered this PNG
      (spec['placed_in']), never from a bare configuration constant. Under
      v5.32 this function was called as _add_image_para(doc, pb,
      FIG_PROBLEM_DISPLAY_IN) — a fixed 2.3 in against a canvas that had been
      supersampled to 2x — which is what produced S = 0.500 on 24 of 24 option
      canvases. The width and the canvas MUST come from the same record.

      NOTE the direction of the fix. Display width stays a LAYOUT decision;
      Q3 makes the render match it. Deriving the width from the artefact
      instead (D := min(native, column)) was measured and REJECTED: it inflates
      figure area 1.84x and gives a four-option MCQ a 10.4 in option stack
      against a ~9.0 in page text height, breaking every such question across a
      page boundary with its options orphaned from the stem.
      """
      if spec is not None:
          width_in = spec["placed_in"]
      p = doc.add_paragraph()
      run = p.add_run()
      run.add_picture(io.BytesIO(png_bytes), width=Inches(width_in))
      p.paragraph_format.keep_together = True        # v5.89 F5 (python-docx only)
      if spec is not None:
          _set_last_drawing_alt(doc, figural_core.alt_text(spec))   # Q9.5
      return p

  def _keep_block_with_next(doc, n_before):
      """v5.89 (GAP-2026-11-02 F5). Set keep_with_next on EVERY paragraph added
      since the body held `n_before` block items (w:p / w:tbl) — including every
      paragraph inside a stem table — so the Q.N stem, any problem label and the
      problem figure(s) are kept on the page of the FIRST option. python-docx
      properties ONLY: they write w:keepNext in schema order. Hand-written
      keepNext XML is FORBIDDEN here (Framework_PYQFormat line 847: keepNext after
      spacing/ind produced 146 schema errors)."""
      from docx.oxml.ns import qn
      from docx.text.paragraph import Paragraph
      kids = [e for e in doc.element.body.iterchildren()
              if e.tag in (qn('w:p'), qn('w:tbl'))]
      for el in kids[n_before:]:
          paras = [el] if el.tag == qn('w:p') else list(el.iter(qn('w:p')))
          for pe in paras:
              Paragraph(pe, doc).paragraph_format.keep_with_next = True

  def _n_block_items(doc):
      from docx.oxml.ns import qn
      return sum(1 for e in doc.element.body.iterchildren()
                 if e.tag in (qn('w:p'), qn('w:tbl')))

  def _set_last_drawing_alt(doc, descr):
      """Stamp wp:docPr/@descr on the most-recently added inline drawing (Q9.5).
      Measured 0 of 208 delivered drawings carried alt text."""
      from docx.oxml.ns import qn
      last = None
      for d in doc.element.body.iter(qn('w:drawing')):
          last = d
      if last is None:
          raise AssertionError("no inline drawing to describe")
      for dp in last.iter(qn('wp:docPr')):
          dp.set('descr', descr)

  def _name_last_drawing(doc, name):
      """Stamp the canonical figural name (S10-7 Q8) onto the most-recently added
      inline drawing — both wp:docPr and pic:cNvPr — so gate G-MATH-RASTER
      recognises it as a legitimate figure. python-docx's add_picture leaves a
      generic 'Picture N' name, which the name-contract would (correctly) reject."""
      from docx.oxml.ns import qn
      last = None
      for d in doc.element.body.iter(qn('w:drawing')):
          last = d
      if last is None:
          raise AssertionError("no inline drawing to name")
      for dp in last.iter(qn('wp:docPr')):
          dp.set('name', name)
      for cp in last.iter(qn('pic:cNvPr')):
          cp.set('name', name)

  def add_figural_question(doc, qnum, stem, problem_pngs, option_pngs,
                           problem_label=None,
                           problem_specs=None, option_specs=None):
      """
      qnum         : int
      stem         : str   — the question instruction (DOCUMENT text, Q.N-first)
      problem_pngs : [bytes] — 1+ problem/series images (geometry only)
      option_pngs  : [bytes] — EXACTLY n_options images, in option order, uniform
      Layout (R-FIGURAL / R14 / G-QNUM-FIRST):
        Q.N stem  →  problem image(s)   (v5.70: NO label line by default)
                  →  for i in 1..N:  "i."  then ONE option image (own line)
                  →  blank separator
      v4.3: every emitted image is stamped with its canonical name (S10-7 Q8) —
        q{N}_problem[_k] / q{N}_opt{i} — so it passes the G-MATH-RASTER name-
        contract; a rasterised expression (e.g. q{N}_e1) never carries such a name.
      """
      # 1:1 binding + uniform canvas are HARD invariants (G-FIGURAL-COMPOSITE).
      assert len(option_pngs) >= 2, "figural MCQ needs ≥2 option images"
      assert_uniform_options(option_pngs)

      # v5.89 F5: remember where this question's block starts (keep rules).
      _n0 = _n_block_items(doc)

      # LINE 1 — Q.N stem (BOLD, configured font) — Q.N FIRST, no image precedes it.
      add_question_stem(doc, qnum, stem)            # S10-3

      # Problem figure(s) (v5.70 CHG-2026-08-24-FIG-NOLABEL: NO label line by
      # default — a label renders only when a caller explicitly passes one).
      if problem_pngs:
          if problem_label:
              lab = doc.add_paragraph(); r = lab.add_run(problem_label)
              r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
          for k, pb in enumerate(problem_pngs, 1):
              _add_image_para(doc, pb, FIG_PROBLEM_DISPLAY_IN,
                              spec=problem_specs[k - 1] if problem_specs else None)
              nm = f"q{qnum}_problem.png" if len(problem_pngs) == 1 \
                   else f"q{qnum}_problem_{k}.png"
              _name_last_drawing(doc, nm)           # canonical name (S10-7 Q8)

      # v5.89 F5: stem block (Q.N .. last problem figure) kept with option 1.
      _keep_block_with_next(doc, _n0)

      # Options: SINGLE COLUMN — one option per line, label bound to its image.
      # v5.89 (GAP-2026-11-02 F5; owner decision 2026-11-02: the two-paragraph
      # label-then-picture SHAPE is kept): each label paragraph carries
      # keep_with_next + keep_together, so an option number can NEVER be left at
      # a page foot with its picture on the next page (measured: 25 of 108 labels,
      # in 25 of 27 structure-option questions, stranded). Gate A-OPTKEEP verifies it. The
      # LAST option picture carries no keep_with_next.
      for i, opt_png in enumerate(option_pngs, 1):
          lp = doc.add_paragraph()                  # the "i." label line
          lr = lp.add_run(_option_label(i))         # option label, exactly the configured format (v5.89: no extra ".")
          lr.bold = False; lr.font.name = FONT_NAME; lr.font.size = Pt(FONT_SIZE_PT)
          lp.paragraph_format.keep_with_next = True   # v5.89 F5 — bound to its picture
          lp.paragraph_format.keep_together = True
          _add_image_para(doc, opt_png, FIG_OPT_DISPLAY_IN,
                          spec=option_specs[i - 1] if option_specs else None)
          _name_last_drawing(doc, f"q{qnum}_opt{i}.png")      # canonical name (Q8)

      add_blank_separator(doc)                       # R13

  # USAGE (per figural question, from S8-6) — v5.55: the option set is rendered
  # by render_option_set(), NOT by a loop over the single-figure helper. A loop
  # fits each option independently, which is exactly the scale divergence Q12
  # and G-FIGOPTWINDOW exist to stop.
  #   import figural_core as fc
  #   pspec = fc.make_figure_spec(q.num, "schematic", fc.FIG_PROBLEM_DISPLAY_IN)
  #   fc.render_figure(draw_problem, f"q{q.num}_problem.png", pspec)
  #   ospecs = [fc.make_figure_spec(q.num, "option_canvas",
  #                                 fc.FIG_OPT_DISPLAY_IN, role="option")
  #             for _ in draw_options]
  #   fc.render_option_set(draw_options, opt_paths, ospecs)
  #   add_figural_question(doc, q.num, q.stem, [prob_png], opt_pngs,
  #                        problem_specs=[pspec], option_specs=ospecs)
  ```

  SINGLE-COLUMN INVARIANT: because every option image is added in its own
  paragraph and options are NEVER placed in a table row or shared paragraph, no
  line ever carries more than one option. Verified by G-FIGURAL-COMPOSITE.

  KEEP INVARIANT (v5.89 — GAP-2026-11-02 F5): every option-label paragraph that
  precedes an option picture carries w:keepNext (python-docx keep_with_next), and
  every paragraph of the stem block carries it too. The label and its picture can
  therefore never be split by a page break. If the whole block is taller than a
  page, Word breaks it between options — never between a label and its picture.
  Verified by auditor gate A-OPTKEEP on every paper whose FigureSpecs are v5.89+.

  COMPOSITE BAN: a figural block that contains only ONE image (problem + options
  fused) is a hard defect — the online engine renders one option region per screen
  and cannot slice a baked panel, and the figures are decoupled from their labels.
  G-FIGURAL-COMPOSITE fails any figural block with < (n_options + 1) images.

## S10-8A — FIGURAL STEM placement helper (v5.13 — stem_only variant)

  Handles format=FIGURAL + image_role='stem_only' MCQ: the problem/series
  figure(s) are images, but the options are TEXT (numbers, words, phrases).
  E.g., "How many triangles are in the given figure?" with text options.

  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  def add_figural_stem_question(doc, qnum, stem, problem_pngs, text_options,
                                problem_label=None, problem_specs=None):
      """
      qnum         : int
      stem         : str   — the question instruction (DOCUMENT text, Q.N-first)
      problem_pngs : [bytes] — 1+ problem/series images (geometry only, 300 DPI)
      text_options : [str]  — text option strings (NOT images)
      problem_specs: [FigureSpec] — v5.89: the spec that RENDERED each problem PNG (same
                     order). Its placed_in / natural size and alt text are used, exactly
                     as add_figural_question does; omitting it places at the layout
                     constant (legacy behaviour) and the figure carries no alt text.
      Layout (R-FIGURAL stem_only / R14 / G-QNUM-FIRST):
        Q.N stem  →  problem image(s)   (v5.70: NO label line by default)
                  →  text options via add_text_options()
                  →  blank separator
      v5.13: new helper for the stem_only variant. Figural questions where only the
      stem has a visual element and options are text. Without this helper, the only
      path was add_figural_question() which HARD ASSERTs option images.
      """
      assert len(problem_pngs) >= 1, "stem_only figural MCQ needs ≥1 problem image"
      assert problem_specs is None or len(problem_specs) == len(problem_pngs), \
          "problem_specs must give one FigureSpec per problem PNG (same order)"
      assert len(text_options) >= 2, "MCQ needs ≥2 text options"
      _n0 = _n_block_items(doc)                         # v5.89 F5

      # LINE 1 — Q.N stem (BOLD, configured font) — Q.N FIRST, no image precedes it.
      add_question_stem(doc, qnum, stem)                # S10-3

      # Problem figure(s) (v5.70 CHG-2026-08-24-FIG-NOLABEL: NO label line by
      # default — a label renders only when a caller explicitly passes one).
      if problem_label:
          lab = doc.add_paragraph(); r = lab.add_run(problem_label)
          r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
      for k, pb in enumerate(problem_pngs, 1):
          _add_image_para(doc, pb, FIG_PROBLEM_DISPLAY_IN,
                          spec=(problem_specs[k - 1] if problem_specs else None))
          nm = (f"q{qnum}_problem.png" if len(problem_pngs) == 1
                else f"q{qnum}_problem_{k}.png")
          _name_last_drawing(doc, nm)                   # canonical name (S10-7 Q8)
      _keep_block_with_next(doc, _n0)                   # v5.89 F5: stem+figure with option 1

      # Options: TEXT, not images. Standard text option placement.
      add_text_options(doc, text_options)                # S10-3

      add_blank_separator(doc)                           # R13

  # USAGE (per stem_only figural question, from S8-6):
  #   prob = render_figural_image(draw_problem, kind="problem")      # reasoning glyph, or
  #   fc.render_figure(draw, png, spec); prob = open(png, 'rb').read() # chart / structure
  #   add_figural_stem_question(doc, q.num, q.stem, [prob], text_options,
  #                             problem_specs=[spec])   # v5.89: ALWAYS when a spec exists
  ```

  WHEN TO USE THIS vs add_figural_question():
    add_figural_question()       → image_role in ('stem_and_options', 'options_only')
    add_figural_stem_question()  → image_role == 'stem_only'
  The FORMAT DISPATCH in S4-7 STEP A makes this decision per question.
  The dispatch reads image_role from section_rules PYQ_IMAGE_ANALYSIS.


# ════════════════════════════════════════════════════════════════════════
# §11 — ANSWER KEY SIDECAR (v2.0 — PER-QUESTION WRITE ENFORCED)
# ════════════════════════════════════════════════════════════════════════

## S11-1 — Format

  ```json
  {"answers": {"1": 2, "2": 4, ...}, "sources": {"Q_num": {...}}}
  ```
  File: [ExamCode]_M[N]_answer_key.json

## S11-2 — Incremental build (v2.0 GAP-18 fix — one write per question)

  Called from S7-NEW-A after EVERY question accepted.
  NEVER reconstructed from memory at batch end or mock end.
  NEVER embedded in docx body (R5 violation if so).

## S11-3 — Source logging for ALL GA facts (not just CA)

  All fact-recall questions: log source citation (authoritative academic,
  government, or official sources relevant to the exam's domain).
  CA questions: additionally log event_date and ca_window.

## S11-4 — Answer key NEVER in docx (v2.0 GAP-17 — detection added)

  PRE-DELIVERY DETECTION:
  ```python
  # ENGINE-RUN — executed by `python3 bootstrap.py --session-start` from this verified file; not in the read
  def check_no_answer_key_in_docx(docx_path):
      from docx import Document
      doc = Document(docx_path)
      answer_key_patterns = [
          r'(?i)answer\s*key',
          r'(?i)answers\s*:',
          r'(?i)^key\s*:',
          # v4.5: single-digit AND set-valued (comma/space list) keys. The v4.4 patterns
          # matched only one digit, so a leaked MSQ key "Q.1 → 1,2,4" slipped through.
          r'Q\.\d+\s*[→:]\s*[1-9](?:\s*[,\s]\s*[1-9])*',  # "Q.1 → 2" or "Q.1 → 1,2,4"
          r'\b\d+\.\s*[→:]\s*[1-9](?:\s*[,\s]\s*[1-9])*',  # "1. → 2" or "1. → 1,2,4"
          # v4.7: NAT numerical-value answer-key lines. The MSQ/MCQ patterns above only
          # match option digits 1-9, so a leaked NAT key "Q.5 → 47", "Q.5 → 0", "Q.5 → -3"
          # or "Q.5 → 3.14" would slip through. Match a signed integer or decimal value.
          r'Q\.\d+\s*[→:]\s*-?\d+(?:\.\d+)?\b',            # "Q.5 → 47" / "→ -3" / "→ 3.14"
          r'\b\d+\.\s*[→:]\s*-?\d+(?:\.\d+)?\b',           # "5. → 47" / "→ -3" / "→ 3.14"
      ]
      import re
      for i, para in enumerate(doc.paragraphs):
          text = para.text.strip()
          for pattern in answer_key_patterns:
              if re.search(pattern, text):
                  print(f"R5 VIOLATION: Answer key detected in docx para {i}: '{text[:60]}'")
                  return False
      return True
  ```
  If this returns False → LADDER-REPAIR R1 [HS:LADDER]. Remove answer key from docx before delivery.

## S11-5 — K-INT verification (v5.4 — MSQ/NAT-aware)

  ```python
  kd  = json.load(open(answer_key_path))
  key = kd["answers"]
  cm  = kd.get("concept_map", {})
  options_count = int(kd.get("msq_meta", {}).get("total_options", 4))   # v5.5 FIX: was undefined
  assert len(key) == total_questions, f"K-INT FAIL: {len(key)} vs {total_questions}"
  for qn, val in key.items():
      at = cm.get(str(qn), {}).get('answer_type', 'option')
      ac = cm.get(str(qn), {}).get('answer_cardinality', 'single')
      if at == 'numerical':
          # NAT: val is a number or numeric string; range-check not applicable
          assert val is not None, f"K-INT FAIL: Q.{qn} NAT answer is None"
      elif ac == 'multi':
          # MSQ: val is a list of ints; each must be in 1..options_count
          assert isinstance(val, list) and len(val) >= 1, \
              f"K-INT FAIL: Q.{qn} MSQ answer not a non-empty list: {val}"
          for v in val:
              assert 1 <= v <= options_count, \
                  f"K-INT FAIL: Q.{qn} MSQ answer element {v} out of range"
      else:
          # Single-answer MCQ: val is an int in 1..options_count
          assert isinstance(val, int) and 1 <= val <= options_count, \
              f"K-INT FAIL: Q.{qn} answer={val}"
  ```

## S11-6 — Answer key correspondence gate

  Q numbers in docx must exactly equal keys in answer_key.json.

# ════════════════════════════════════════════════════════════════════════
# §12 — GUARD SCRIPT (all 81 gates — 39 v1.0 baseline + 30 added since v1.0
#        + 12 FIGURE CONFORMANCE added in v5.33 / Audit v2.11)
# ════════════════════════════════════════════════════════════════════════

## S12-0 — Zero-Warning Policy (unchanged)

  Every fixable WARN = blocker = same as FAIL.

## GATE ADDITIONS / CHANGES (v2.0):

  S12-NEW-1 — G-FONTCHECK:
    Scan all text runs in docx. Any run with font.name not in [FONT_NAME, None]
    (None = inherits configured font from default style) → Exit 1.
    Fixable: re-run generation with corrected add_*() helpers.

  S12-NEW-2 — G-OPTLABEL:
    Scan all option paragraphs. Option labels must match "^\d+\.\s{2}" pattern.
    If "(1)", "1)", "1. " (one space) found → Exit WARN.
    Fixable: regenerate with corrected add_text_options().

  S12-NEW-3 — G-SECTIONHDR:
    Scan all paragraphs before first Q.N paragraph.
    If any paragraph matches "SECTION:", "Section I", "Part A" etc. → Exit 1.
    Fixable: remove the offending paragraphs from docx.

  S12-NEW-4 — G-ANSWERKEY:
    Call check_no_answer_key_in_docx() (S11-4).
    If answer key patterns found → Exit 1 (HARD FAIL).
    Fixable: remove answer key section from docx.

  S12-NEW-5 — G-FIGTEXT (v5.13 — 3-tier expanded detection):

    TIER 1 — IMAGE COUNT PER FORMAT=FIGURAL SUBTOPIC (primary):
      For every subtopic in this mock whose section_rules format==FIGURAL (and not
      in FORMAT_OVERRIDE — S3-17c):
        Locate the Q-block by question number (from concept_map in sidecar).
        Read image_role from PYQ_IMAGE_ANALYSIS (default 'stem_and_options').
        COUNT the <w:drawing> inline images in the block.
        Expected minimum image count per image_role:
          stem_and_options : n_options + 1 (problem + options) — existing check
          stem_only        : 1 (problem image(s) only; options are text)
          options_only     : n_options (option images only; no problem image)
        IF image_count < expected minimum:
          → Exit 1: "G-FIGTEXT: Q.[n] is format=FIGURAL (image_role=[role])
             but contains [k] image(s), expected ≥[min]. Render via matplotlib
             (S7-NEW-B OPTION A) or replace subtopic (OPTION B).
             Text descriptions of figures are BANNED (OPTION C)."
      IF concept_map or section_rules is unavailable for Tier 1:
        → WARN: "G-FIGTEXT-DEPS: concept_map or section_rules missing —
           Tier 1 image-count check SKIPPED. Only Tier 2/3 active."
        → In --final mode: escalate to FAIL (Final Assembly must have full check).

    TIER 2 — LEGACY BRACKET-PATTERN REGEX (secondary, unchanged):
      Scan ALL paragraphs for bracketed placeholder patterns:
        "[The figure shows...", "[Image: ...", "[Figure will be added",
        "text description:", "[Diagram:", "[Picture:"
      Any match → Exit 1: "G-FIGTEXT: Figural placeholder detected."

    TIER 3 — VISUAL PROSE DETECTOR (tertiary, v5.13):
      For every Q-block in the docx:
        IF the block contains 0 <w:drawing> inline images:
          Scan the block's text for FIGURE REFERENCE patterns:
            r"(?i)\b(in the given figure|in the following figure|
              from the (given|following) (figure|diagram)|
              figure \(X\)|the figure (shows|below|above)|
              how many .{0,30}(triangles|squares|circles|lines|shapes|
              angles|sides|regions|parts)\s+(are|in|does|can))"
          IF any match found:
            → Exit 1: "G-FIGTEXT-PROSE: Q.[n] references a figure but block
               contains 0 images. Render the figure (S7-NEW-B OPTION A,
               use add_figural_stem_question for text-option variants) or
               replace the subtopic entirely (OPTION B)."
        IF the block contains ≥1 image: skip Tier 3 for this block (no false positive).

    WHY THREE TIERS: Tier 1 catches format=FIGURAL subtopics rendered as prose
    (the production defect class — unbracketed text that Tier 2's regex missed).
    Tier 2 catches bracketed placeholder annotations in any format block. Tier 3
    catches format=TEXT subtopics that are inherently visual but were misclassified
    — it operates on CONTENT, not on format metadata, and fires only when text
    references a figure AND zero images exist in the block.
    Together they cover the full failure space across all image_role variants.
    Fixable: generate real images (OPTION A) or replace the subtopic (OPTION B).

  S12-NEW-6 — G-ALTGROUP (v4.4 — manifest-driven; replaces hardcoded G-CISINCHECK):
    Exam-agnostic alternation backstop to S3-17. Reads the Step-0 manifest's
    alternation_groups {group: [subtopic_id, ...]} and the mock's allocated
    subtopic_ids (the same id set S3-17 uses). For each group, if ≥2 of its
    members are present in this mock → Exit 1 (alternation violated), naming the
    group and the offending members via manifest display_name.
    ```python
    groups   = manifest.get('alternation_groups', {})
    mock_ids = set().union(*[set(m.keys()) for m in alloc_ids.values()]) if alloc_ids else set()
    for group, members in groups.items():
        present = [m for m in members if m in mock_ids]
        if len(present) > 1:
            disp = [manifest['subtopics'].get(m, {}).get('display_name', m) for m in present]
            # v5.53.2: raise SystemExit, not sys.exit — `sys` was never imported by any
            # earlier block in this file (spec_name_audit.py finding); SystemExit needs
            # no import and is this file's own house style (every other gate uses it).
            # v5.89 (GAP-2026-11-02 G6): S3-17 already rejected a violating allocation,
            # so a violation here means generation drifted from it (or an R5 slot
            # reassignment — which MUST update alloc_ids in the same step as
            # allocation_amendments, §Q8b-LADDER R5). Repaired, never a run stop.
            raise RuntimeError(f"LADDER-REPAIR R5 [HS:LADDER] (G-ALTGROUP): Mock {N} — "
                     f"alternation group '{group}' has {len(present)} members present "
                     f"({', '.join(disp)}); ≤1 allowed — reassign the later slot(s).")
    ```
    Empty alternation_groups ⇒ nothing to enforce ⇒ pass (no false stop).
    Zero hardcoded subtopic names. Fixable: drop the member that the blueprint
    parity assigns to the other mock, then regenerate (Step 7 never auto-edits the
    blueprint to resolve this; its only in-run edits are S3-2D and ladder R5).

  S12-NEW-24 — G-GROUPMANDATE (v5.0 — group-presence backstop, Issue 2b):
    Exam-agnostic post-gen backstop to S3-17 CHECK 3, mirroring G-ALTGROUP. Reads
    manifest.mandatory_groups {group: {members:[ids], min}} and the per-subtopic_id
    counts computed from the mock's concept_map (the SAME generated-reality counts
    G-ALLOC-SUBTOPIC uses — not merely the blueprint). For each group, if the number
    of members with ≥1 GENERATED question is < min → Exit 1.
    ```python
    groups = manifest.get('mandatory_groups', {})
    # counts[sid] = generated questions of that subtopic_id in this mock (from concept_map)
    for group, spec in groups.items():
        members = spec.get('members', [])
        need    = spec.get('min', 1)
        have    = sum(1 for m in members if counts.get(m, 0) > 0)
        if have < need:
            disp = [manifest['subtopics'].get(m, {}).get('display_name', m) for m in members]
            raise RuntimeError(f"LADDER-REPAIR R2 [HS:LADDER] (G-GROUPMANDATE): Mock {N} — "
                     f"group '{group}' has {have} of [{', '.join(disp)}] present; "
                     f"needs >={need} — regenerate a slot of a missing member.")
    ```
    Empty mandatory_groups ⇒ pass. Fixable: regenerate so ≥min members appear
    (Step 1 RULE M4 should have guaranteed this in the blueprint).

  S12-NEW-25 — G-MINCOUNT (v5.0 — min-count backstop, Issue 2b):
    Exam-agnostic post-gen backstop to S3-17 CHECK 4. Reads manifest.min_counts
    {id: k} and the same per-subtopic_id generated counts. If any id has < k
    GENERATED questions → Exit 1.
    ```python
    for mid, k in manifest.get('min_counts', {}).items():
        c = counts.get(mid, 0)
        if c < k:
            disp = manifest['subtopics'].get(mid, {}).get('display_name', mid)
            raise RuntimeError(f"LADDER-REPAIR R2 [HS:LADDER] (G-MINCOUNT): Mock {N} — {mid} "
                     f"('{disp}') has {c}Q generated; needs >={k} — regenerate the "
                     f"missing slot(s) of this subtopic.")
    ```
    Empty min_counts ⇒ pass. NOTE: manifest.cadence_windows is intentionally NOT
    gated in Step 7 — cadence is cross-mock (see S3-17 note + Step 1 RULE M5).

  S12-NEW-7 — G-CONCEPTDUP (DOUBT-3 — scenario uniqueness, v3.2; v3.3 concept_map):
    Read the per-question concept_map from the answer_key sidecar
    ({q: {subtopic, concept_group, scenario_key}}). Group questions by
    scenario_key. If ANY scenario_key maps to more than one Q → Exit 1.
    Strict zero: same scenario twice (even with changed values/names/wording,
    even across two different subtopics) is banned. No tolerance band.
    (If concept_map is missing for any Q → Exit 1: generation did not record it;
     fix the generator, do not silently re-derive.)
    Fixable: regenerate the duplicate on a DIFFERENT scenario (never reduce the
    subtopic count to "fix" it).
    Report (MANDATE 0 — no content): "G-CONCEPTDUP: Q.[a] and Q.[b] share
    scenario_key 'op|shape'. Regenerate Q.[b] on a different scenario."

  S12-NEW-8 — G-ALLOC-SUBTOPIC (DOUBT-3 RULE A — per-subtopic exact count, v3.2):
    From the concept_map, count questions per subtopic and compare to
    blueprint.json subtopic_allocations[].q_count (=N).
    If any subtopic count != N → Exit 1 (HARD FAIL).
      count < N → missing questions; generate the remainder (distinct scenarios).
      count > N → over-generated; remove extras.
    This is distinct from S3-9 (which only checks SECTION totals). G-ALLOC-SUBTOPIC
    checks every individual subtopic.

  S12-NEW-9 — G-COUNT-X-UNIQUE (DOUBT-3 combined check, v3.2):
    The two rules verified TOGETHER at Final Assembly, both from concept_map:
      (i)  every subtopic has EXACTLY its blueprint q_count (RULE A), AND
      (ii) all scenario_keys mock-wide are pairwise distinct (RULE B),
           with the CLASS-4 exception that a shared linked-stimulus is allowed
           but each linked Q's sub_skill scenario_key is still distinct.
    A subtopic with the right count but a repeated scenario → FAIL.
    A subtopic with distinct scenarios but the wrong count → FAIL.
    Both conditions must pass for the mock to ship.

  S12-NEW-10 — G-STIMULUS-ORPHAN (v3.6 — linked self-containment, LADDER-REPAIR R1 [HS:LADDER]):
    Enforces R-LINKED / §9. Scans EVERY question block in the cumulative docx and
    verifies that any question depending on a shared stimulus physically carries
    that stimulus in its OWN block.
    ALGORITHM:
      Parse the docx into per-question blocks (a block = the bold "Q.<N>" stem
      paragraph + its following paragraphs/tables/images up to the next "Q.<N>").
      For each block:
        refs_stimulus = stem matches ANY of:
          r"the passage", r"the table", r"the graph", r"the chart",
          r"the given (data|information)", r"blank \(\d+\)",
          r"according to the passage", r"in the passage",
          r"Q\.\d+\s*(and|to|–|-)\s*Q\.\d+"   # cross-question dependence text
        has_stimulus = block contains a passage paragraph (≥25 words of prose)
          OR a Word table OR an inline image, attached to THIS block.
        # Cross-reference language ("Q.X and Q.Y") is itself a violation even if
        # a stimulus is present, because it implies a multi-question screen.
        if re.search(r"Q\.\d+\s*(and|to|–|-)\s*Q\.\d+", stem):  → Exit 1
        if refs_stimulus and not has_stimulus:                  → Exit 1
      ALSO (group completeness): build groups from the answer_key sidecar
      linked_group_id. For each group, every member block must independently
      satisfy has_stimulus (Model A) — UNLESS delivery.linked_mode == "group"
      (Model B confirmed), in which case exactly one "[GROUP n: Q.X–Q.Y]" preamble
      must bind the set and members may share. Any member missing its stimulus
      under Model A → Exit 1.
    NOT FIXABLE BY DELETION: the fix is to EMBED the stimulus into each member
    (re-run S4-7 STEP A with add_linked_stimulus, §10-S10-LINKED). Never "fix" by
    dropping the linked questions.
    Report (MANDATE 0 — no content): "G-STIMULUS-ORPHAN: Q.[n] references a
    stimulus not present in its own block (linked_group_id=[gid]). Embed the
    shared stimulus into Q.[n] (Model A) and re-check."

  S12-NEW-11 — G-QNUM-FIRST (v3.7 — Q.N-FIRST block contract, LADDER-REPAIR R1 [HS:LADDER]):
    Enforces R14 / R-LINKED Q.N-FIRST clause. Segments the cumulative docx into
    question blocks (a block runs from one "Q.<N>" paragraph to the next). For
    EACH block, the FIRST non-empty body element must be the "Q.<N>" paragraph
    itself — NOT a table, chart image, passage, or unnumbered preamble.
    ALGORITHM:
      Walk the body in document order (paragraphs AND tables interleaved).
      Track the element immediately following each inter-question boundary.
      For each question's opening element:
        if it is a table / image / non-"Q.<N>" paragraph  → Exit 1
        if it is a paragraph but does NOT match r"^\s*Q\.\d+\b"  → Exit 1
      ALSO: assert exactly one r"^\s*Q\.\d+\b" paragraph per block (R14); the
      specific-ask paragraph in a linked block must be NON-numbered.
    This catches the v3.6-style "stimulus/preamble before Q.N" layout and any
    stray second Q-number inside a block.
    NOT FIXABLE BY REORDERING ALONE if the Q-number is missing: re-emit the block
    via S10-LINKED (add_qn_context first → stimulus → add_specific_ask).
    Report (MANDATE 0 — no content): "G-QNUM-FIRST: block for Q.[n] opens with
    [table/passage/preamble], not 'Q.[n]'. Re-emit Q.N context line first."

  S12-NEW-12 — G-FORMATDUP (v3.8; v3.9 hardened — RULE C, LADDER-REPAIR R2 [HS:LADDER]):
    Enforces §6-3c. Reads the per-question concept_map from the answer_key
    sidecar. SELECTS questions by subtopic_class ∈ {CLASS2, CLASS3} (v3.9 G5 fix —
    NOT by "presentation_key not None", which would let a missing-key question, the
    exact failure case, escape). Groups the selected questions by concept_group.
    Let M = len(STEM_FORMAT_MENU[resolve_presentation_family(subtopic_data)]).
    ALGORITHM:
      for cg, qs in group_by(selected, key=concept_group):
          # missing-key guard (now reachable, because selection is class-based)
          for q in qs:
              if q.presentation_key is None or q.stem_format_variant is None:
                  → Exit 1  "G-FORMATDUP: Q.[q] (CLASS 2/3) has no presentation_key
                             — generator did not pick a defined stem_format_variant
                             + distractor_strategy (§6-3c)."
          # (C1) distinct VISIBLE format while count ≤ M
          if len(qs) <= M and len({q.stem_format_variant for q in qs}) < len(qs):
              → Exit 1  "G-FORMATDUP/C1: CONCEPT_GROUP '[cg]' reuses a
                         stem_format_variant across [n] questions (count ≤ menu
                         size [M]); each must use a different visible format."
          # (C2) distinct presentation_key always
          seen = {}
          for q in qs:
              pk = q.presentation_key
              if pk in seen:
                  → Exit 1  "G-FORMATDUP/C2: Q.[seen[pk]] and Q.[q] share
                             CONCEPT_GROUP '[cg]' AND presentation_key '[pk]'.
                             Regenerate Q.[q] on a different format/distractor."
              seen[pk] = q
    Strict zero: distinct target item (scenario_key) does NOT excuse an identical
    look. This is the gate that catches M1 Q.77/Q.79 and Q.78/Q.80.
    NOT FIXABLE BY DROPPING N: regenerate the offending question on a new
    stem_format_variant / presentation_key (§6-3c menus). Never reduce the count.
    Report is MANDATE-0 safe (no stem content — only Q numbers, concept_group,
    and menu tokens).

  S12-NEW-13 — G-FIGURAL-COMPOSITE (v5.13 — image_role-aware, LADDER-REPAIR R1 [HS:LADDER]):
    Enforces R-FIGURAL / §10-S10-8 / §10-S10-8A. For every FIGURAL question, the
    rendered block must be correctly structured per its image_role variant.
    IDENTIFY figural blocks: use the figural manifest q-list when present; else a
    block is figural if its stem matches the figural cue set
      r"(?i)(select|choose|which) .*figure|mirror image|water image|paper.?fold(ing)?|
            complete the (figure|series|pattern)|embedded figure|odd one out.*figure|
            problem figure|find the missing (figure|term).*(figure|pattern)"
      AND the block contains ≥1 inline image AND no Word table (tables ⇒ DI, not
      figural — excluded to avoid false positives on DI charts).
    ALGORITHM (v5.13 — per figural block; n_opt = option count, default 4):
      imgs_total   = count of <w:drawing> inline images in the block
      imgs_per_line= max images in any single paragraph of the block

      Determine the image_role for this Q:
        Read from batch_state.figural_qs[qnum].image_role if available,
        else from section_rules PYQ_IMAGE_ANALYSIS via sidecar concept_map,
        else default 'stem_and_options'.
        SPECIAL CASE: if answer_type=='numerical' (FIGURAL-NAT, v4.7),
        treat as 'stem_only' regardless of PYQ_IMAGE_ANALYSIS — a NAT has
        a problem image but no option images (there are no options).

      BRANCH BY image_role:

        stem_and_options (DEFAULT — v4.0 behaviour):
          if imgs_total < n_opt + 1:      → Exit 1   # composite / missing options
          if imgs_per_line > 1:           → Exit 1   # ≥2 options on one line / row
          if <w:tbl> wraps option images: → Exit 1   # option grid/row
          if "1. Figure 1" dummy text:    → Exit 1   # placeholder option

        stem_only (v5.13 — problem image + text options; also covers FIGURAL-NAT):
          if imgs_total < 1:              → Exit 1   # no problem image at all
          # Option-image checks are SKIPPED — options are text (or absent for NAT).
          # Still check: no composite panel (problem should be separate from stem).
          if imgs_per_line > 1:           → Exit 1   # multiple images on one line

        options_only (v5.13 — text stem + option images):
          if imgs_total < n_opt:          → Exit 1   # missing option images
          # No problem image required — stem is text.
          if imgs_per_line > 1:           → Exit 1   # ≥2 options on one line
          if <w:tbl> wraps option images: → Exit 1   # option grid/row

    NOT FIXABLE BY EDITING TEXT: re-render via S10-7 and re-emit via the correct
    helper (S10-8 or S10-8A depending on image_role).
    Report (MANDATE 0 — no content): "G-FIGURAL-COMPOSITE: Q.[n] image_role=[role],
    holds [k] image(s) (expected ≥[min]). Re-render with the correct helper."

  S12-NEW-14 — G-UNDERLINE (v4.1 — underline-span rendering, LADDER-REPAIR R1 [HS:LADDER]):
    Catches the M1 defect where an underline-class question shipped its target span
    as a plain-text annotation ("(underlined: senior than me)") instead of a real
    underlined run. Parallel to G-FIGTEXT (figural-as-text), for underline-as-text.
    SELECT (underline-class blocks): a Q-block whose stem references an underlined
      element — UNDERLINE_TRIGGER_RE matches the stem text (see S10-2):
        r"(?i)underlin(?:e|ed)\s+(?:word|words|part|segment|phrase|portion|sentence)"
        r"|the\s+underlined\b"   # one (?i) at start applies to the whole pattern
      (the persisted stem_format_variant == 'sentence_embedded_underlined' also
       selects the block, even if the instruction wording differs.)
    ALGORITHM (per selected block):
      # (a) banned text annotation anywhere in the block:
      if re.search(r"(?i)\(\s*underlin(?:e|ed)\b", block_full_text):  → Exit 1
      # (b) no real underlined run present in the block:
      if not has_underlined_span(block):                              → Exit 1
    has_underlined_span(block) — run-level XML check (a run is underlined when its
      rPr carries <w:u> with a val other than "none"):
        from docx.oxml.ns import qn
        def has_underlined_span(block_elements):
            for el in block_elements:
                for r in el.iter(qn('w:r')):
                    rpr = r.find(qn('w:rPr'))
                    if rpr is None: continue
                    u = rpr.find(qn('w:u'))
                    if u is not None and u.get(qn('w:val')) not in ('none', '0'):
                        return True
            return False
    Test (a) catches the annotation fallback; test (b) catches a silently-dropped
    underline (target rendered as ordinary text). A correct block — target word as a
    real <w:u> run, no parenthetical — passes both.
    NOT FIXABLE BY EDITING TEXT: re-render via S10-2 add_stem_with_underline so the
    target span carries run.underline = True inside the sentence.
    Report (MANDATE 0 — no content): "G-UNDERLINE: Q.[n] references an underlined
    span but [renders it as a '(underlined: …)' annotation / has no underlined run].
    Re-render with add_stem_with_underline (target as a real underlined run)."

  S12-NEW-15 — G-OPTREF (v4.2 — stem↔option reference consistency, LADDER-REPAIR R2 [HS:LADDER]):
    Catches the M1 Q.100 mismatch (instruction promised a "no error → last option"
    escape the option set did not contain). EXAM-AGNOSTIC: escape tokens / option
    structures are read from section_rules (none_of_above_map S3-12,
    wrong_option_structure S3-13); the gate enforces coherence only.
    ESCAPE-REFERENCE PATTERNS (generic; extend from section_rules wording — single
    (?i) at the start, no embedded quote chars, so it compiles as written):
      ESCAPE_REF = re.compile(
          r"(?i)\\bif\\b[^.]*\\bno\\s+(?:error|improvement|mistake)\\b"
          r"|\\bselect\\b[^.]*\\bno\\s+(?:error|improvement)\\b"
          r"|none of (?:these|the above)|all of the above"
          r"|both\\b[^.]*\\band\\b[^.]*follow|neither\\b[^.]*\\bnor\\b")
      LASTOPT_REF = re.compile(r"(?i)(?:the\\s+)?last option")
    ALGORITHM (per Q block; opts = the 4 option strings):
      if ESCAPE_REF.search(stem):
          # the referenced terminal option must EXIST among opts
          want = canonical_escape_token(stem)   # "No error" / "No improvement" /
                                                # "None of these" / "Both I and II" …
          if not any(option_is(o, want) for o in opts):  → Exit 1
          # if the stem says "last option", the escape must be the LAST option
          if LASTOPT_REF.search(stem) and not option_is(opts[-1], want):  → Exit 1
      # converse: a "pick the segment with the error" layout (all four options are
      # sentence segments of the stem's carrier sentence) may NOT carry a
      # "no error → last option" instruction unless a real "No error" option exists:
      if is_segment_option_layout(stem, opts) and ESCAPE_REF.search(stem) \
         and not any(option_is(o, "No error") for o in opts):  → Exit 1
    option_is(o, token) does a normalised match (case/whitespace/quote-insensitive)
    against the exam's escape wording from section_rules.
    NOT FIXABLE BY EDITING THE KEY: either append the missing escape option in the
    position the instruction names (and re-balance K-BAL), or switch the stem to the
    matching template (a "select the segment with the error" instruction has NO "no
    error" escape). Carrier-sentence run-ons are fixed by §10-S10-2 layout.
    Report (MANDATE 0): "G-OPTREF: Q.[n] references a '[want]' option that is absent
    / mis-positioned. Add the escape option (or switch to the matching template)."

  S12-NEW-16 — G-UNIQUE (v4.5 — answer-contract record, LADDER-REPAIR R2 [HS:LADDER]; generalises v4.2):
    Enforces R-ANSWER (both modes). The answer contract is decided at GENERATION
    (CHECK 3 verify_answer, §7) because verbal ambiguity needs reasoning, not
    regex; this gate is the RECORD-PRESENCE backstop (same pattern as G-CONCEPTDUP
    requiring concept_map). EXAM-AGNOSTIC.
    ALGORITHM:
      read concept_map from the answer_key sidecar (S7-NEW-A).
      for each question q in 1..N:
          rec = concept_map.get(str(q))
          if rec is None or rec.get("answer_verified") is not True:
              → Exit 1
    A missing/False flag means generation SKIPPED the answer contract for that Q
    (e.g. the M1 Q.3 maternal/paternal Sister-vs-Cousin split, or Q.98 is-vs-was
    universal-truth convention would have been caught and disambiguated at CHECK 3;
    or, for an MSQ, a borderline out-set option would have been caught).
    NOT FIXABLE BY FLIPPING THE FLAG: re-run the question through CHECK 3
    verify_answer; if (single) a second option is defensible, or (multi) the set is
    ill-formed or an out-set option is arguable, disambiguate the stem (qualify the
    relation / pin the convention via section_rules / constrain the rule) or
    move/remove the colliding option, then regenerate.

  S12-NEW-18 — G-MSQ-SET (v4.5 — MSQ set well-formedness, LADDER-REPAIR R2 [HS:LADDER]; MULTI ONLY):
    Runs ONLY for questions whose concept_map answer_cardinality=='multi' (skipped entirely
    when blueprint multi_present is false — fully dormant). Enforces the structural half
    of R-ANSWER multi + R-MSQ-ESCAPE. EXAM-AGNOSTIC.
    ALGORITHM (read S = answers[q] as a set; n = total_options from blueprint):
      • S empty (k=0)                              → Exit 1
      • S not ⊆ {1..n}                             → Exit 1
      • |S| == n (all-correct, k=n)                → Exit 1
      • an "All of the above" option is present AND section_rules msq_allow_aota is
        false (R-MSQ-ESCAPE)                        → Exit 1
    NOT FIXABLE BY EDITING THE KEY: regenerate the question so the intended correct
    SET is a non-empty proper subset (drop the AOTA option / add a genuine wrong
    option / split an over-broad stem), then re-run CHECK 3.
    Report (MANDATE 0): "G-MSQ-SET: Q.[n] MSQ key is ill-formed ([reason])."

  S12-NEW-19 — G-MSQ-CARD (v4.5 — MSQ fixed-k cardinality, LADDER-REPAIR R2 [HS:LADDER]; MULTI + FIXED ONLY):
    Runs ONLY when answer_cardinality=='multi' AND section_rules msq_k_mode=='fixed'.
    ALGORITHM: if |answers[q]| != msq_k → Exit 1.
    For "Select TWO"/"Select THREE" exams this guarantees the rendered set matches the
    instructed count. Variable-k exams skip this gate (no fixed cardinality to check).
    Report: "G-MSQ-CARD: Q.[n] has |S|=[got], expected msq_k=[k]."

  S12-NEW-20 — G-MSQ-INSTR (v4.5 — MSQ instruction line present, LADDER-REPAIR R1 [HS:LADDER]; MULTI ONLY):
    Runs ONLY for answer_cardinality=='multi' questions. The multi instruction phrase
    ("(One or more options may be correct)" / "(Select TWO)" / localized equivalent
    from section_rules) MUST appear INSIDE the bold Q.<N>-first stem paragraph (R14 /
    G-QNUM-FIRST — there is no paper-level instructions page). EXAM-AGNOSTIC.
    ALGORITHM: locate the Q.<N> stem paragraph; if it contains no MSQ instruction
    phrase (matched case-insensitively against the section_rules msq_instruction set
    + the universal fallback set) → Exit 1.
    NOT FIXABLE BY ADDING A SEPARATE PARAGRAPH (that breaks R14): re-emit the stem with
    the instruction appended to the Q.<N> line.
    Report: "G-MSQ-INSTR: Q.[n] (MSQ) has no select-instruction in its Q.N stem line."
    Report (MANDATE 0): "G-UNIQUE: Q.[n] has no answer_verified record —
    generation did not run the R-ANSWER check. Re-verify and disambiguate if needed."

  S12-NEW-21 — G-NAT-NOOPT (v4.7 — NAT zero-option, LADDER-REPAIR R1 [HS:LADDER]; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. A NAT question is a typed-value
    question with NO options (R4 / R13 NAT exemption). AUTHORITATIVE: scans the rendered
    docx, locates the question's Q.<N> block, and counts option-label paragraphs (the R10
    "N.  " pattern). If a NAT question carries ANY option paragraph → Exit 1 (a generation
    routing bug — the NAT path must emit only the bold Q.<N> stem + blank separator).
    Fully dormant when nat_present=false. EXAM-AGNOSTIC.
    Report: "G-NAT-NOOPT: Q.[n] (NAT) has [k] option paragraph(s); must have none."

  S12-NEW-22 — G-NAT-ANSWER (v4.7 — NAT value well-formed, LADDER-REPAIR R2 [HS:LADDER]; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. Reads the stored answer VALUE
    (answers[q], tested 'is None' so 0/negative/fractional are valid) and the per-Q
    ca_range, against nat_meta.nat_answer_type. Exit 1 when: (a) no value recorded; (b)
    value is non-numeric; (c) nat_answer_type=='integer' but the value is not integral;
    (d) ca_range present but malformed (not exactly (lo,hi) with lo<=hi). This is the
    generation-side backstop for R-ANSWER's numerical branch; audit.py A-NAT-ANSWER
    independently RE-DERIVES the value and checks it lies in the band. EXAM-AGNOSTIC.
    Report: "G-NAT-ANSWER: Q.[n] [value/ca_range problem]."

  S12-NEW-23 — G-NAT-INSTR (v4.7 — NAT instruction line present, LADDER-REPAIR R1 [HS:LADDER]; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. The nat_instruction (blueprint
    nat_contract; e.g. "Enter your answer as a numerical value.", localized) MUST appear
    INSIDE the bold Q.<N>-first stem paragraph (R14 / G-QNUM-FIRST — no paper-level
    instructions page). Record-presence backstop here (the per-Q nat_instr_in_stem flag);
    audit.py A-NAT-INSTR re-checks the rendered docx. NOT FIXABLE by a separate paragraph
    (breaks R14): re-emit the stem with the instruction appended to the Q.<N> line.
    Fully dormant when nat_present=false. EXAM-AGNOSTIC.
    Report: "G-NAT-INSTR: Q.[n] (NAT) has no numerical-entry instruction in its Q.N stem line."

  S12-NEW-29 — G-NAT-GRADE (v5.25 — NAT portal grading value well-formed, LADDER-REPAIR R2 [HS:LADDER];
    NUMERICAL ONLY): Runs ONLY for answer_type=='numerical' questions. Reads the sidecar's
    nat_grading_type/nat_grading_value (S7-NEW-C) and re-runs `derive_nat_grading()` against
    the SAME (value, ca_range, stem_precision) inputs. Exit 1 when: (a) nat_grading_value is
    missing/None while answer_type=='numerical'; (b) nat_grading_value contains any character
    outside `0123456789.-` (allowlist check — a blacklist of "known-bad" patterns like
    scientific notation is NOT sufficient, since it silently admits anything nobody thought to
    ban); (c) the re-derived (type, value) does not EXACTLY match the stored pair — this is a
    determinism check, not a re-judgement, since derive_nat_grading is a pure function of its
    three inputs; (d) a range-typed value's re-derivation raises the NOT-SUPPORTED
    negative-bound error — this Exit 1's as a WELL-POSEDNESS defect on the question (rework the
    numbers), never silently reformatted around. This is the generation-side backstop for the
    portal-grading contract (S7-NEW-C); audit.py A-NAT-GRADE independently re-derives it again
    from scratch, exactly as A-NAT-ANSWER does for the math value. EXAM-AGNOSTIC.
    Report: "G-NAT-GRADE: Q.[n] [charset/type/determinism problem]."

  S12-NEW-30 — G-MATH-RESIDUE (v5.70 — ASCII-dialect math residue, LADDER-REPAIR R1 [HS:LADDER] per
    batch AND at the S13-2 sweep): Enforces R-MATH-OMML's TEXT arm at delivery time
    — the enforcement the funnel lacked (GAP-2026-08-24-MATH-RESIDUE-SHIPPED:
    flat-underscore orbital labels shipped in stems/options with 0 OMML while the
    SAME questions' Step-9 explanations rendered correctly; MC3 was WARN-only, the
    S4-11 checklist had no residue item, and no auditor arm existed, so nothing
    blocked). ALGORITHM: run mock_math_residue_check() (§10-S10-4) on the
    cumulative docx at STEP B of every batch and again in the S13-2 sweep; ANY
    entry in the returned 'blocking' list → FAIL, and present_files is FORBIDDEN
    (B-7/R15) until it is empty. The 'amber' list (t3 compile fallbacks) routes to
    the F1 AMBER footer per Framework_DeliveryFooter §5 — WARN-and-deliver,
    unchanged from v5.47. Fixable: re-emit each named stem/option via
    render_mock_text() with ⟦MATH:…⟧ regions (chemistry examples: S10-4 rule 3a).
    Engine twin: audit.py A-SUBFLAT (audit_canonical v2.17) independently
    re-derives the flat/half-Unicode subscript scan from the rendered docx, with
    catch+clean self-test fixtures — the enforcement of record.


  S12-NEW-17 — G-MATH-RASTER (v4.3 — math-as-OMML routing, LADDER-REPAIR R1 [HS:LADDER]):
    Enforces R-MATH-OMML / §10-S10-4. Catches the M1 Q.55 defect where two
    algebraic expressions ("x + 1/x = 5", "x²+1/x²") shipped as 300-DPI matplotlib
    PNGs (q55_e1.png, q55_e2.png) instead of native OMML. Parallel to G-FIGTEXT
    (figural-as-text) and G-UNDERLINE (underline-as-text); here it is math-as-raster.
    SIGNAL — the figural IMAGE NAME-CONTRACT (provenance-proof). The ONLY producers
    of inline rasters are the figural emitter (§10-S10-8, names q{N}_problem[_k] /
    q{N}_opt{i}) and the linked-stimulus path (§9, names q{N}_stim[_tag]). Any
    inline <w:drawing> whose pic name does NOT match the canonical pattern is an
    UNAUTHORISED raster — the prime case being a rasterised expression. This signal
    cannot be defeated by faking a figural-manifest entry (it reads the image, not a
    sidecar) and cannot false-positive on a genuine figure (which is named by the
    S10-8 convention).
    ```python
    import re
    from docx import Document
    from docx.oxml.ns import qn

    ALLOWED_IMG_NAME_RE = re.compile(
        r"(?i)^q\d+_(problem(_\d+)?|opt\d+|stim(_[a-z0-9]+)?)\.(png|jpg|jpeg)$")
    # corroborating diagnostics only (NOT the pass/fail signal):
    MATH_CONTEXT_RE = re.compile(
        r"(?i)value of|simplif|evaluate|solve for|find the value|"
        r"[=+\u00d7\u00f7\u221a\u00b2\u00b3]|\bx\s*\+|\b1\s*/\s*[a-z]|\^")
    MATH_IMG_NAME_RE = re.compile(
        r"(?i)(_e\d+|_eq\d*|_eqn|_expr|_frac|_math|_formula)")

    def _blocks(doc):
        cur, num, out = [], None, []
        for p in doc.paragraphs:
            m = re.match(r"\s*Q\.(\d+)", p.text or "")
            if m:
                if cur: out.append((num, cur))
                cur, num = [p], m.group(1)
            elif cur is not None:
                cur.append(p)
        if cur: out.append((num, cur))
        return out

    def _img_names(block):
        names = []
        for p in block:
            for dr in p._p.iter(qn('w:drawing')):
                nm = ""
                for c in dr.iter(qn('pic:cNvPr')): nm = c.get('name') or ""
                names.append(nm)
        return names

    def g_math_raster(docx_path):
        doc = Document(docx_path); offenders = []
        for qnum, block in _blocks(doc):
            for nm in _img_names(block):
                if ALLOWED_IMG_NAME_RE.match(nm or ""):
                    continue                         # legitimate figure / stimulus
                stem = " ".join(p.text for p in block)
                offenders.append((qnum, nm,
                                  bool(MATH_CONTEXT_RE.search(stem)),
                                  bool(MATH_IMG_NAME_RE.search(nm or ""))))
        if offenders:
            for q, nm, mc, mn in offenders:
                print(f"G-MATH-RASTER: Q.{q} carries unauthorised raster {nm!r} "
                      f"(math_context={mc}, math_name={mn}).")
            raise RuntimeError("LADDER-REPAIR R1 [HS:LADDER] (G-MATH-RASTER): "
                               f"{len(offenders)} unauthorised raster(s) — re-render as OMML")
    ```
    NOT FIXABLE BY EDITING TEXT: re-render the expression as OMML via §10-S10-4
    add_math_stem / emit_math_inline (interleave <m:oMath> with the stem text);
    delete the raster. If the flagged image is a GENUINE figure that was mis-named,
    re-emit it through add_figural_question (§10-S10-8) so it carries the canonical
    q{N}_problem / q{N}_opt{i} name.
    Report (MANDATE 0 — no content): "G-MATH-RASTER: Q.[n] ships a math expression
    as image [name] instead of OMML. Re-render via S10-4 add_math_stem; remove the
    raster."

  All 39 gates from v1.0 still apply (S12-1 through S12-39).
  v2.0 added 6 (S12-NEW-1..6). v3.1 added G-CONCEPTDUP. v3.2 added
  G-ALLOC-SUBTOPIC (S12-NEW-8) and G-COUNT-X-UNIQUE (S12-NEW-9). v3.5 added
  G-DELIVERY-SET. v3.6 added G-STIMULUS-ORPHAN (S12-NEW-10). v3.7 added
  G-QNUM-FIRST (S12-NEW-11). v3.8 added G-FORMATDUP (S12-NEW-12). v4.0 added
  G-FIGURAL-COMPOSITE (S12-NEW-13). v4.1 added G-UNDERLINE (S12-NEW-14). v4.2 added
  G-OPTREF (S12-NEW-15) and G-UNIQUE (S12-NEW-16). v4.3 adds G-MATH-RASTER
  (S12-NEW-17). v4.5 adds G-MSQ-SET (S12-NEW-18), G-MSQ-CARD (S12-NEW-19), and
  G-MSQ-INSTR (S12-NEW-20) — all MULTI-mode only, fully dormant when multi_present is false.
  G-NAT-NOOPT / G-NAT-ANSWER / G-NAT-INSTR (S12-NEW-21/22/23) — all NUMERICAL-mode only,
  fully dormant when nat_present is false (no concept_map entry has answer_type=='numerical').
  v5.25 adds G-NAT-GRADE (S12-NEW-29, numbered out of sequence — 24/25 were already taken by
  G-GROUPMANDATE/G-MINCOUNT — see that entry below) to the same NUMERICAL-mode-only family.
  v5.18 adds G-PREQ1 (S12-NEW-27) — the pre-Q.1 body-block ban. Total gates: 67.

  v5.19 adds G-MATCH-TABLE (S12-NEW-28) — match-grid rendering; executable enforcement
  delegated to the audit.py A-MATCH-TABLE (no logic duplicated here). Total gates: 68.

  v5.25 adds G-NAT-GRADE (S12-NEW-29) — NAT portal grading value/type well-formedness
  (0-9.- charset, deterministic re-derivation via derive_nat_grading, S7-NEW-C). NUMERICAL-mode
  only, fully dormant when nat_present is false. Total gates: 69.

  v5.70 adds G-MATH-RESIDUE (S12-NEW-30) — ASCII-dialect math residue in any
  stem/option is a per-batch HARD FAIL; t3 compile-fallback regions stay AMBER.
  Total gates: 70.

  S12-NEW-26 — G-QINDEX (v5.2 — question-index certification, HARD STOP [HS:INFRA]; runs at Final
    Assembly; executable home S13-QINDEX, after S13-REGCHECK). Certifies the mock-N
    registry.question_index this session built (S13-4) — the per-question {subtopic_id,
    difficulty} record Step 6 renders as the five tags. Six checks, all HARD STOP [HS:INFRA]:
      1  an index object exists for mock N;
      2  it has exactly total_questions question entries;
      3  its q set is exactly {1..total_questions} — sorted, no gaps, no duplicates;
      4  every subtopic_id exists in blueprint.subtopic_list[] (never a display name);
      5  every difficulty is in blueprint.difficulty_labels (the canonical set);
      6  the difficulty distribution EQUALS difficulty_schedule[N] exactly (simple->Easy,
         medium->Medium, hard->Hard alias) — satisfiable by construction under the SCHEDULE-FIRST
         assignment rule (§ difficulty budget).
    subtopic_id is Step-7's assignment here and (v5.36) the ONLY one — nothing re-derives it from the fixed
    docx and cross-checks it (that is subtopic_id's certification). difficulty is
    authoritative-by-assignment (not re-derivable from the paper) + distribution-verified.
    Writes NOTHING to the docx. Governed by Contract_QuestionMetadataIndex v1.0; the six checks
    were proven in the Phase-1 harness before encoding.
    Report: "G-QINDEX: <failing check(s)>." 

  S12-NEW-27 — G-PREQ1 (v5.18 — pre-Q.1 body-block ban, LADDER-REPAIR R1 [HS:LADDER]; per-batch S4-11 AND the
    S13-2 Final-Assembly sweep):
    Scan every paragraph BEFORE the first Q.<N> stem paragraph in the docx body. A paragraph
    is a violation if it carries non-blank text (by construction nothing before Q.1 can be a
    Q.<N> stem or an option line). Any such paragraph → Exit 1:
      "G-PREQ1: non-Q paragraph before Q.1: '<text[:60]>'. The paper is questions-only (R8b);
       delete the pre-Q.1 title/info/scoring/cover block. CATEGORY-C values are metadata,
       never printed."
    Blank paragraphs before Q.1 are ignored (normal separators). DORMANT only if
    section_rules.md EXAM_STRUCTURE declares paper_header_block (a deliberate per-exam opt-in;
    no current exam declares it). Fixable: remove the offending paragraphs from the docx.
    Independently re-verified by audit.py A-HEADER (strip, not validate).

  S12-NEW-28 — G-MATCH-TABLE (v5.19 — match-grid rendering; per-batch S4-11 + audit.py):
    Every question rendered from stem_format_variant == 'match_the_following' MUST carry a real
    Word table (<w:tbl>) for its List columns. A match emitted via add_standard_question()
    (lists as plain text) is a format-fidelity defect: the MATCH format is counted present
    while the skill is left un-rehearsed. ENFORCEMENT: executable detection is DELEGATED to the
    audit.py A-MATCH-TABLE, which already runs on the cumulative docx during S4-11 STEP B
    when AUDIT_AVAILABLE — the match-detection logic is NOT duplicated here (anti-drift). The
    S4-11 manual checklist item is the no-audit fallback. Fixable: re-emit the question via
    add_match_table() (§10-S10-3M).


# ════════════════════════════════════════════════════════════════════════
# §13 — FINAL ASSEMBLY (v2.0 — REGISTRY INIT FIX)
# ════════════════════════════════════════════════════════════════════════

## S13-1 — Final Assembly trigger (unchanged)

## S13-2 — Complete gate sweep (all 81 gates)

## S13-2F — PRE-COMMIT ITEM SWEEP + CERTIFICATE (v5.89 — GAP-2026-11-02 G1)

  Runs after S13-2 and BEFORE S13-4 commits anything.

  WHY. Through v5.88 the auditor's final run (S13-4c) came AFTER the S13-4 commit, and S13-4
  is only partly idempotent (final_assembly's dedup logs are extended), so a defective item
  found there could not be repaired — and S13-4c stopped the run on ANY non-zero exit,
  including AMBER advisories that Q8b says must ALWAYS complete. Every defect is now found
  and REPAIRED here, before the commit, through §Q8b-LADDER; S13-4c only confirms.

  THE RULE. When AUDIT_AVAILABLE (always true when a verified repo auditor exists — S3-1
  v5.89 P3), each SWEEP is:
    1. PREVIEW: set S13_PREVIEW = True, execute the S13-4 code block, then set
       S13_PREVIEW = False. In preview mode that block computes exactly the commit S13-4
       will make (commit_registry is pure) plus the S13-REGCHECK self-heal, writes it ONLY
       to /home/claude/[ExamCode]_M[N]_registry_preview.json and persists nothing.
    2. Execute the code block below. It runs the auditor in PRE-COMMIT mode over the final
       docx with every source S13-4c uses — including --registry <preview>, so the
       registry-reading gates (A-OPTN, A-QINDEX, A-NAT…, A-AXIS3, A-DUP) are assessed now
       — plus --profile, --key (this paper's concept_map) and --fig-manifest.
    3. CLEAN (no item finding, no FAIL line of any gate) -> the certificate is written and
       the block binds CERT / AMBER_NOTES. Go on to S13-3 / S13-4.
       NOT CLEAN -> the block prints the worklist and raises LADDER-REPAIR [HS:LADDER]:
       repair each named question at its rung (§Q8b-LADDER) IN THE FINAL DOCX, in place —
       the S4-6 correction procedure: edit only that question's block, re-render its
       figures, update its sidecar/answer-key entry and fig_manifest record, keep every
       other question byte-unchanged — then run the next sweep (1-3 again).
  Item findings enter at bc.ladder_entry over bc.LADDER_ENTRY_RUNG. A FAIL line with no
  item record (A-ANSKEY, A-SECHDR, A-QNFIRST, A-OPTREF, A-OMML, A-FIGTYPE-KIND, …) names
  its question(s) in its message and is repaired by that gate's own [HS:LADDER R<n>] rule.
  Sweeps 1-2 repair at the entry rung; sweep 3 sends every item still failing straight to
  its TERMINAL rung (R4 / R4' / R5 — constructed to pass every item gate).
  v5.96 (GAP-2026-11-08-DR3-QINDEX-CONFLICT; owner decision OD-2026-11-09 — supersedes OD-9):
  EVERY survivor has a route, decided by ONE engine function, bc.sweep_route; nothing is
  stamped UNRESOLVED and no paper is NOT CERTIFIED. (1) An item finding — and any FAIL line
  whose message names a question — that survives the terminal rung (sweep >= 4) enters that
  slot's SLOT CHAIN (S13-2R: replacement on a new substrate, another ask shape, a sibling
  subtopic; kind bc.chain_kind_for), and the sweep count restarts. A-QINDEX checks 7 / 8 now
  emit item findings (A-QINDEX-FLOOR at RL, A-QINDEX-LABEL at R2), so a label clash is always
  repairable. (2) A FAIL line naming NO question is rebuilt deterministically —
  bc.PAPER_GATE_ROUTE 'reassemble' (rebuild the final docx from the per-item blocks, S13-1) or
  'recapture' (recompute the sidecar records and the S13-4 preview) — and from sweep
  bc.S13_2F_MAX_SWEEPS (6) on it is reported 'AMBER — ESCALATED' (--escalate-paper; delivered
  disclosed, never a stop). (3) Only a bc.INFRA_GATES FAIL (the auditor crashed, the docx cannot
  be opened, the certificate is unreadable) is a tool fault: it is SELF-HEALED
  (bc.infra_heal_step — reinstall the dependencies, re-copy the verified auditor, re-run its
  --self-test, re-render) up to bc.INFRA_HEAL_MAX times, and stops only when the tool is still
  broken. The sweep counter lives in a state file, so a resumed session continues the count.
  A paper never fails S13-2F for a QUALITY or RULE reason.
  AFTER a clean sweep the step goes on IMMEDIATELY, in the SAME response,
  to S13-2G (the in-session independent review, OD-5 restated 2026-11-04) and from there to
  S13-3 / S13-4 and the two-file delivery. It never ends the response, never waits for the
  user and never asks for a file (v5.91 — GAP-2026-11-04 A1; STEP-CONTRACT-LAW).
  v5.91 (GAP-2026-11-04 B7): a quality control the auditor reports DORMANT (its measured
  input is missing or stale — A-TEMPLATE on every project whose Step 5 predates the
  measurement) or INFEASIBLE emits no item finding, so it never enters the ladder and never
  costs a sweep.

```python
import json, os, subprocess
import blueprint_core as bc
import paper_pipeline as pp
_docx = f'/mnt/user-data/outputs/{EXAM}_{pp.paper_slug(paper_id)}_Create.docx'   # final docx
_cert = f'/home/claude/{EXAM}_M{N}_item_sweep_certificate.json'
_ifj = f'/home/claude/{EXAM}_M{N}_item_findings.json'
_key = f'/home/claude/{EXAM}_M{N}_answer_key.json'
_pf = f'/mnt/project/{EXAM}_difficulty_profile.json'
_fmj = f'/home/claude/{EXAM}_fig_manifest.json'
_prev = f'/home/claude/{EXAM}_M{N}_registry_preview.json'   # written by step 1 (S13_PREVIEW)
_stp = f'/home/claude/{EXAM}_M{N}_s13_2f_state.json'
_bsp = f'/home/claude/{EXAM}_M{N}_batch_state.json'

def _infra(site, msg):
    # v5.96 (OD-2026-11-09): a tool fault is SELF-HEALED first — perform the repair the message names,
    # automatically, then re-run this block; it may end the response only after bc.INFRA_HEAL_MAX heals.
    _bsh = json.load(open(_bsp, encoding='utf-8'))
    _act, _bsh['infra_heal'], _n = bc.infra_heal_step(_bsh.get('infra_heal'), site)
    json.dump(_bsh, open(_bsp, 'w', encoding='utf-8'), indent=2)
    if _act == 'heal':
        raise RuntimeError(f"INFRA-HEAL [HS:LADDER] {site} (attempt {_n}/{bc.INFRA_HEAL_MAX}): perform the repair "
                           f"named below NOW, automatically, then re-run this block — {msg}")
    raise SystemExit(msg)

# v5.89 (LAW F1.4 — moved here from S13-4): a figure recorded on a text_disclosed fallback
# subtopic is an ITEM defect, repaired BEFORE the certificate — after the certificate any
# docx change would void it (A-CERT). Re-author each named question as TEXT (S7-NEW-B
# OPTION B), drop its fig_manifest entry, then run the next sweep.
_fm_fb = json.load(open(_fmj, encoding='utf-8')) if os.path.exists(_fmj) else {}
_fb_hit_pre = sorted(str(q) for q, v in ((_fm_fb or {}).get('questions') or {}).items()
                     if isinstance(v, dict) and v.get('subtopic_id') in (bp.get('figural_fallbacks') or {}))
if _fb_hit_pre:
    raise RuntimeError(f"LADDER-REPAIR R4 [HS:LADDER] (S13-2F, LAW F1.4): question(s) {_fb_hit_pre} "
                       f"carry a figure on a text_disclosed fallback subtopic — re-author them as "
                       f"TEXT, remove their fig_manifest entries, then run the next sweep.")

CERT, AMBER_NOTES = None, []
if AUDIT_AVAILABLE:
    if not os.path.exists(_prev):
        _infra('S13-2F-preview', "HARD STOP [HS:INFRA] (S13-2F): no registry preview — run step 1 "
                                 "(the S13-4 block with S13_PREVIEW = True) before this block.")
    _st = json.load(open(_stp, encoding='utf-8')) if os.path.exists(_stp) else {}
    if _st.get('paper_id') != paper_id:               # another paper's counter never carries over
        _st = {'paper_id': paper_id, 'sweep': 0}
    _st['sweep'] = int(_st.get('sweep', 0)) + 1
    json.dump(_st, open(_stp, 'w', encoding='utf-8'))
    for _old in (_ifj, _cert):                        # never re-read a previous sweep's files
        if os.path.exists(_old):
            os.remove(_old)
    # v5.91 (GAP-2026-11-04, release review) — before the audit, on EVERY sweep:
    # (i) an UNRESOLVED(A-TEMPLATE) stamp written by 2026.11.03 (its default cap of 2 /
    #     paper-wide count — untrustworthy) is REMOVED, here and in the registry preview, so it
    #     can never keep a paper NOT CERTIFIED (OD-9 restated, D0); the sweep re-stamps every
    #     item. Stamps written by THIS release (quality_stamps_release) are never removed.
    # (ii) the engine's terminal-rung record (s13_2f_state 'terminal') is merged onto the
    #     sidecar's ladder record — the author's repair rewrote the entry since (B8).
    _kd_pre = json.load(open(_key, encoding='utf-8'))
    _bs_pre = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
    _act_pre, _rec_pre = bc.certificate_uncertified_active(
        {q: (e or {}).get('quality_status') for q, e in (_kd_pre.get('concept_map') or {}).items()},
        _bs_pre.get('quality_readiness'),
        # stamps written by THIS release carry batch_state['quality_stamps_release'] (set
        # where S13-2F stamps, below); stamps on a paper parked by 2026.11.03 do not
        producer_release=_bs_pre.get('quality_stamps_release') or '2026.11.03')
    for _q in _rec_pre:
        _kd_pre['concept_map'][str(_q)].pop('quality_status', None)
    if _rec_pre and os.path.exists(_prev):
        # the preview (step 1) was computed from the sidecar BEFORE this clean-up and the
        # auditor overlays it — remove the same stamps from THIS paper's preview entry, or
        # the auditor would still read them (release review 2026-11-04)
        _pv = json.load(open(_prev, encoding='utf-8'))
        _rs = {str(x) for x in _rec_pre}
        for _qe in (_pv.get('question_index') or []):
            if isinstance(_qe, dict) and _qe.get('paper_id') == paper_id:
                for _rr in (_qe.get('questions') or []):
                    if isinstance(_rr, dict) and str(_rr.get('q')) in _rs:
                        _rr.pop('quality_status', None)
        json.dump(_pv, open(_prev, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    if _rec_pre:
        print(f"S13-2F: cleared {len(_rec_pre)} UNRESOLVED stamp(s) {_rec_pre} that only an unmeasured / "
              f"2026.11.03 template control wrote (informational; never a defect).")
    for _q in (_st.get('terminal') or []):
        _e_t = (_kd_pre.get('concept_map') or {}).get(str(_q))
        if isinstance(_e_t, dict):
            _lad_t = _e_t.get('ladder') if isinstance(_e_t.get('ladder'), dict) else {}
            _lad_t['terminal_sweep'] = int(_st.get('terminal_sweep') or 3)
            _e_t['ladder'] = _lad_t
    json.dump(_kd_pre, open(_key, 'w', encoding='utf-8'), indent=2)
    cmd = ['python3', f'/home/claude/{EXAM}_mock_test_audit.py', _docx,
           '--phase', 'precommit', '--item-findings', _ifj,
           '--write-certificate', _cert,
           '--blueprint', BP_SRC_PATH,
           '--rules', f'/mnt/project/{EXAM}_section_rules.md',
           '--manifest', f'/mnt/project/{EXAM}_subtopic_manifest.json',
           '--registry', _prev,
           '--mockN', str(N),
           # v5.96: the hash of every delivered block (REVIEW-COVERAGE-LAW) and the paper-level gates
           # this sweep escalates to AMBER at the sweep cap (bc.sweep_route 'amber')
           '--item-hashes', f'/home/claude/{EXAM}_M{N}_item_hashes.json',
           '--sweep', str(_st['sweep'])]
    if _st.get('escalate'):
        cmd += ['--escalate-paper', ','.join(_st['escalate'])]
    _sgp_pre = globals().get('STIM_PROFILE_PATH')     # v5.85 A-BLOCK — same source as S13-4c
    for _flag, _path in (('--profile', _pf), ('--key', _key), ('--fig-manifest', _fmj),
                         ('--stimulus-profile', _sgp_pre),
                         ('--style-profile', f'/mnt/project/{EXAM}_style_profile.json')):   # A-ITEMRULE suspension (R7.2)
        if _path and os.path.exists(_path):
            cmd += [_flag, _path]
    _r = subprocess.run(cmd, capture_output=True, text=True, env=AUDIT_ENV)
    print(_r.stdout)                                  # real STDOUT (B-7)
    os.remove(_prev)                                  # consumed: every sweep needs a FRESH preview
    if not os.path.exists(_ifj):
        _infra('S13-2F-auditor', f"HARD STOP [HS:INFRA] (S13-2F): the auditor wrote no item-findings "
                                 f"file (rc={_r.returncode}) — it crashed or is a pre-v2.34 copy (repair: re-copy "
                                 f"the verified repo audit_canonical.py to /home/claude/{EXAM}_mock_test_audit.py, "
                                 f"run its --self-test, reinstall missing packages). STDERR:\n{_r.stderr[-3000:]}")
    _wl = json.load(open(_ifj, encoding='utf-8'))
    if os.path.exists(_cert):                         # CLEAN sweep
        CERT = json.load(open(_cert, encoding='utf-8'))
        AMBER_NOTES = list(CERT.get('amber_notes') or [])   # -> DeliveryFooter §5 (DISCLOSED / ESCALATED lines)
        UNCERTIFIED_ITEMS = list(CERT.get('uncertified_items') or [])   # v5.96: always [] (OD-2026-11-09)
        _bs2f = json.load(open(_bsp, encoding='utf-8'))
        _bs2f['uncertified_items'] = UNCERTIFIED_ITEMS
        _bs2f['escalated_paper'] = {'gates': list(_st.get('escalate') or []), 'sweep': _st['sweep']}   # -> S13-4c / S13-QINDEX
        _bs2f['infra_heal'] = bc.infra_heal_clear(bc.infra_heal_clear(_bs2f.get('infra_heal'), 'S13-2F-preview'),
                                                  'S13-2F-auditor')
        # a quality chain whose replacement swept clean is FIXED (bc.slot_chain_record 'pass')
        for _qc, _ch in list((_bs2f.get('slot_chain') or {}).items()):
            _att = (_ch or {}).get('attempts') or []
            if _ch.get('kind') == 'quality' and not _ch.get('done') and _att and _att[-1].get('outcome') == 'pending':
                _bs2f['slot_chain'][_qc] = bc.slot_chain_record(_ch, _att[-1]['stage'], 'pass')
        json.dump(_bs2f, open(_bsp, 'w', encoding='utf-8'), indent=2)
        os.remove(_stp)
        # every item is stamped CERTIFIED in the sidecar — except a DISCLOSED item (its quality chain
        # proven exhausted, S13-2L), which keeps its stamp and is listed as an amber note
        _kd = json.load(open(_key, encoding='utf-8'))
        for _qn, _e in (_kd.get('concept_map') or {}).items():
            if not str(_e.get('quality_status', '')).startswith('DISCLOSED'):
                _e['quality_status'] = 'CERTIFIED'
        json.dump(_kd, open(_key, 'w', encoding='utf-8'), indent=2)
        print(f"S13-2F: CERTIFIED after sweep {_st['sweep']} ({len(AMBER_NOTES)} amber note(s)"
              + (f"; DISCLOSED items {CERT.get('disclosed_items')}" if CERT.get('disclosed_items') else '') + ").")
    else:
        # v5.96 (OD-2026-11-09) — ONE routing decision for every survivor (bc.sweep_route): never a stop
        # for a quality or rule condition, never an UNRESOLVED stamp
        # v6.1 (S0-BV BV-5 / S0-NF-9): a measured COMPOSITION shortfall (bc.NF_DISCLOSE_GATES — allocation, format
        # parity, MIP share, class mix, band mix by subject, and a repeat / key leak that survived the in-batch
        # rewrite) is DISCLOSED, never re-authored at Final Assembly: written once to the sidecar's nf_disclosed (the
        # auditor then reports AMBER — DISCLOSED, Framework_DeliveryFooter §LADDER-NF) and the sweep runs again.
        _nfd_new = {}
        for _f in (_wl.get('item_findings') or []):
            if _f.get('gate') in bc.NF_DISCLOSE_GATES:
                _nfd_new.setdefault(_f['gate'], []).append(f"Q{_f.get('q')}")
        for _fl in (_wl.get('fail_lines') or []):
            if _fl.get('check') in bc.NF_DISCLOSE_GATES:
                _nfd_new.setdefault(_fl['check'], []).append(str(_fl.get('message') or '')[:200])
        _kd_nd = json.load(open(_key, encoding='utf-8'))
        _nd = _kd_nd.setdefault('nf_disclosed', {})
        _nfd_new = {g: v for g, v in _nfd_new.items() if g not in _nd}
        if _nfd_new:
            for _g, _v in _nfd_new.items():
                _nd[_g] = '; '.join(dict.fromkeys(_v))[:400]
            json.dump(_kd_nd, open(_key, 'w', encoding='utf-8'), indent=2)
            json.dump(_st, open(_stp, 'w', encoding='utf-8'))   # the sweep counter is KEPT
            raise RuntimeError(f"DELTA [HS:LADDER] (S13-2F sweep {_st['sweep']}): {sorted(_nfd_new)} measured short — "
                               f"DISCLOSED (AMBER, nothing is re-authored at Final Assembly); run a fresh sweep "
                               f"(preview + this block) now.")
        _infra_fl = [fl for fl in (_wl.get('fail_lines') or []) if fl.get('check') in bc.INFRA_GATES]
        _stok = True
        if _infra_fl:                                 # a tool fault: is the tool itself broken?
            _stok = subprocess.run(['python3', f'/home/claude/{EXAM}_mock_test_audit.py', '--self-test'],
                                   capture_output=True, text=True, env=AUDIT_ENV).returncode == 0
        # v6.0 (LAW-ORG-5): a label that does not verify strictly is S13-2L's work — the item is marked 'carried' and
        # its difficulty chain decides (rework / replace / refill / last resort); the RL relabel rung is never used
        _lbl_qs = sorted({str(f.get('q')) for f in (_wl.get('item_findings') or [])
                          if f.get('gate') in ('A-QINDEX-LABEL', 'A-QINDEX-FLOOR') and f.get('q') is not None})
        _bs_c = json.load(open(_bsp, encoding='utf-8'))
        if not _bs_c.get('difficulty_plan_target'):
            _lbl_qs = []                                  # no difficulty plan: S13-2L owns no chain — the legacy route
        if _lbl_qs:
            _kd_c = json.load(open(_key, encoding='utf-8'))
            for _qc in _lbl_qs:
                _ec = _kd_c.setdefault('concept_map', {}).setdefault(_qc, {})
                _ec['difficulty_check'] = dict(_ec.get('difficulty_check') or {}, decision='carried')
            json.dump(_kd_c, open(_key, 'w', encoding='utf-8'), indent=2)
            _wl['item_findings'] = [f for f in (_wl.get('item_findings') or [])
                                    if not (f.get('gate') in ('A-QINDEX-LABEL', 'A-QINDEX-FLOOR') and str(f.get('q')) in _lbl_qs)]
            _fl_keep = []
            for _fl in (_wl.get('fail_lines') or []):                  # A-QINDEX joins its checks with '; '
                if _fl.get('check') == 'A-QINDEX':
                    _rest = [x for x in str(_fl.get('message', '')).split('; ') if not x.startswith(('check 7', 'check 8'))]
                    if not _rest:
                        continue
                    _fl = dict(_fl, message='; '.join(_rest))
                _fl_keep.append(_fl)
            _wl['fail_lines'] = _fl_keep
            print(f"S13-2F sweep {_st['sweep']}: Q{', Q'.join(_lbl_qs)} carried to S13-2L (label not yet measured_exact).")
            if not _wl['item_findings'] and not _wl['fail_lines']:
                json.dump(_st, open(_stp, 'w', encoding='utf-8'))   # the sweep counter is KEPT (caps still apply)
                raise RuntimeError(f"DELTA [HS:LADDER] (S13-2F sweep {_st['sweep']}): only carried labels remain — run "
                                   f"S13-2G phases 1-3, then S13-2L (it schedules each carried slot's difficulty chain), then a "
                                   f"fresh sweep (preview + this block).")
        _route = bc.sweep_route(_wl.get('item_findings'), _wl.get('fail_lines'), _st['sweep'], self_test_ok=_stok)
        for _g, _how in sorted(_route['paper'].items()):
            if _how == 'amber':
                _st['escalate'] = sorted(set(_st.get('escalate') or []) | {_g})
            print(f"S13-2F sweep {_st['sweep']}: paper-level {_g} -> {_how}")
        json.dump(_st, open(_stp, 'w', encoding='utf-8'))
        if _route['stop'] or any(_h == 'self_heal' for _h in _route['paper'].values()):
            _infra('S13-2F-' + ','.join(sorted(g for g, h in _route['paper'].items() if h in ('self_heal', 'infra_stop'))),
                   f"HARD STOP [HS:INFRA] (S13-2F): tool fault {[fl['message'][:300] for fl in _infra_fl]} — the "
                   f"auditor self-test {'PASSED' if _stok else 'FAILED'} (repair: reinstall the Step 0 packages, re-copy "
                   f"the verified audit_canonical.py, re-render the final docx from the per-item blocks, re-run).")
        _repl = {q: r['gates'] for q, r in _route['items'].items() if r['route'] == 'REPLACE'}
        _kd_rp = json.load(open(_key, encoding='utf-8'))
        _bs_rp = json.load(open(_bsp, encoding='utf-8'))
        for _qd2 in [q for q in _repl if str(((_kd_rp.get('concept_map') or {}).get(q) or {}).get('quality_status', '')).startswith('DISCLOSED')
                     and ((_bs_rp.get('slot_chain') or {}).get(q) or {}).get('outcome') == 'amber']:
            _repl.pop(_qd2)                       # its quality chain is already proven exhausted: never re-opened
        if _repl:
            # a finding that survived the terminal rung enters the slot's chain (S13-2R) — the count restarts
            _bsr = json.load(open(_bsp, encoding='utf-8'))
            _kdr = json.load(open(_key, encoding='utf-8'))
            _chs = _bsr.setdefault('slot_chain', {})
            _tpr = _bsr.get('difficulty_plan_target') or _bsr.get('difficulty_plan') or {}
            for _qr, _gr in sorted(_repl.items(), key=lambda kv: int(kv[0])):
                _ch = _chs.get(_qr)
                _att = (_ch or {}).get('attempts') or []
                if _ch and not _ch.get('done') and _att and _att[-1].get('outcome') == 'pending':
                    _chs[_qr] = bc.slot_chain_record(_ch, _att[-1]['stage'], 'fail', note=','.join(_gr))
                elif not _ch or _ch.get('done') or _ch.get('kind') != bc.chain_kind_for(_gr):
                    # a new chain of the right kind; an open chain of another kind is suspended inside it and a
                    # finished one is kept in its history (bc.slot_chain_reopen)
                    _chs[_qr] = bc.slot_chain_reopen(_ch, _qr, bc.chain_kind_for(_gr), _tpr.get(_qr),
                                                     ((_kdr.get('concept_map') or {}).get(_qr) or {}).get('subtopic_id'))
                _chs[_qr]['gates'] = list(_gr)
            json.dump(_bsr, open(_bsp, 'w', encoding='utf-8'), indent=2)
            os.remove(_stp)
            raise RuntimeError(f"SLOT-CHAIN [HS:LADDER] (S13-2F sweep {_st['sweep']}): {sorted(_repl, key=int)} survived "
                               f"the terminal rung — run S13-2L (it schedules each slot's next chain action) and S13-2R "
                               f"NOW, then a fresh sweep (preview + this block). Never UNRESOLVED (OD-2026-11-09).")
        _by_q = {}
        for _f in _wl.get('item_findings') or []:
            _by_q.setdefault(_f.get('q'), []).append(_f['gate'])
        for _q, _reasons in sorted(_by_q.items(), key=lambda kv: str(kv[0])):
            _rung = 'TERMINAL' if _st['sweep'] >= 3 else bc.ladder_entry(_reasons)
            print(f"S13-2F sweep {_st['sweep']}: Q{_q} {sorted(set(_reasons))} -> ladder {_rung}"
                  + (" (RL: set the label to the recorded basis's expected band, no content change)" if _rung == 'RL' else ''))
        if _st['sweep'] >= 3:
            # v5.91 (GAP-2026-11-04 B8): the ENGINE records which items it routed to their
            # terminal rung — in ITS OWN state file (the author's repair rewrites the sidecar
            # entry, so a stamp written there now would be lost). It is merged onto the
            # sidecar's ladder record at the start of every later sweep (above); the auditor's
            # A-TEMPLATE R4/R4' exemption requires it.
            _st['terminal'] = sorted(set(_st.get('terminal') or []) | {str(q) for q in _by_q if q is not None},
                                     key=lambda x: int(x) if x.isdigit() else 0)
            _st['terminal_sweep'] = _st['sweep']
            json.dump(_st, open(_stp, 'w', encoding='utf-8'))
        for _fl in _wl.get('fail_lines') or []:
            print(f"S13-2F sweep {_st['sweep']}: FAIL {_fl['check']}: {_fl['message']}")
        raise RuntimeError(f"LADDER-REPAIR [HS:LADDER] (S13-2F sweep {_st['sweep']}): repair "
                           f"the questions above at their rungs in the final docx (S4-6 "
                           f"correction procedure), record registry question_index ladder "
                           f"data in the sidecar; a paper-level 'reassemble' line: rebuild the final docx "
                           f"from the per-item blocks (S13-1); 'recapture': recompute the sidecar records "
                           f"(S7-NEW-A) — 'amber' needs nothing; then run the next sweep (preview + this block).")
```

## S13-2G — INDEPENDENT REVIEW, IN-SESSION (v5.91 — GAP-2026-11-04 A1-A7; owner decisions OD-5 restated (D0), D1, D2, D4)

  WHY (v5.90, unchanged). Every verification of the incident paper — answer, difficulty
  rating, "is a second option defensible" — ran in the author's own context and agreed with
  itself. A fresh context is the only review that cannot be anchored by having written the
  item. The owner chose it MANDATORY on every paper, with CORRECTION: a review that ends in
  a list of findings is worthless; the flagged items are REPAIRED through the ladder before
  the commit.

  WHY IT CHANGED (v5.91 — GAP-2026-11-04-STEP7-CONTRACT-RESTORE). v5.90 implemented OD-5 as
  a two-session protocol (now retired): Step 7 ENDED at the legacy AWAITING_REVIEW state,
  delivered a review packet, and the OWNER had to run the review step in a second chat
  (retired), carry a verdict file back with the registry and type a resume command —
  up to three hand-offs per paper, the registry uncommitted meanwhile, the
  verdict file not even found by name once uploaded (incident 2026-11-04, SSC GD Tier 1,
  TestCreate P2). OD-5 RESTATED (owner, 2026-11-04, D0): the independent review is mandatory
  and runs INSIDE THIS RUN. It is NEVER a user step, NEVER ends Step 7, NEVER creates a
  user-visible file and NEVER needs a second chat. Step 7 ends — in the SAME response as the
  last batch — with exactly [ExamCode]_[slug]_Create.docx + [ExamCode]_registry.json
  (STEP_CONTRACTS.json, STEP-CONTRACT-LAW). The only user action Step 7 may require is
  typing "continue" between batches (or after an interrupted response — S4-12).

  THE FLOW (all in the final batch's response; every arrow is automatic):
    S13-2F clean (v5.96: a Create paper is never NOT CERTIFIED)
      -> phase 1 (packet, written ONLY under /home/claude)
      -> phase 2 (one FRESH reviewer per part — CLASS T, the model's own turn)
      -> phase 3 (bind + key_agrees + defects)
         defects in round 1 -> REVIEW_REPAIR: repair each at §Q8b-LADDER R2 in the final docx
                               -> S13-2F (fresh certificate) -> phase 1..3 again (round 2,
                               the WHOLE paper — the binding is per paper)
         round 2 still disputed -> that slot's DISPUTE chain (v5.96, OD-2026-11-09: S13-2L
                                   schedules, S13-2R runs; never UNRESOLVED, never NOT CERTIFIED)
      -> REVIEWED -> S13-2L (slot chains + DELTA reviews of every changed item, until every item is
         at its slot band and covered: REVIEW-COVERAGE-LAW) -> S13-3 -> S13-4 -> S13-REGCHECK
         -> S13-QINDEX -> S13-4b/4c -> S13-6 -> S13-7 -> S13-8 (the two files) -> S13-9 -> footer.
  v6.1 (S0-BV BV-5): every question reaching this review was already measured in its batch, so phase 3 never
  schedules a difficulty repair for it (its LB2 label is kept; the reviewer's band is recorded as advisory). The
  review repairs only correctness findings (key disagreement, a second defensible option, low confidence).
  v5.96 DELTA ROUNDS. Rounds 1 and 2 review the WHOLE paper. Every later round is a DELTA round
  over batch_state['delta_qs'] only (items changed since their last review, adjudications,
  coverage gaps) plus batch_state['delta_panel'] (each such item to bc.REVIEW_PANEL_SIZE fresh
  reviewers). Every verdict is bound to the hash of the block it reviewed (the auditor's
  --item-hashes; bc.item_hash) and appended to the item's review_history.
  STATES (batch_state.state): 'REVIEW_RUNNING' during phases 1-3 and 'REVIEW_REPAIR' during
  the round-1 repairs — INTERNAL, used only so an interrupted response resumes (S4-12);
  'REVIEWED' after phase 3. 'AWAITING_REVIEW' is a LEGACY v5.90 state: S4-12 continues it
  through this same internal flow and never asks for a verdict file.

  PHASE 1 — build the packet, internally:
  ```python
  # ── S13-2G phase 1 (executable) ───────────────────────────────────────────────
  import json, os, hashlib, shutil, subprocess, blueprint_core as bc, paper_pipeline as pp
  # batch_state is RELOADED from disk: this block also runs after an interrupted response
  # (S4-12) and after the REVIEW_REPAIR re-sweep, where the in-memory copy may be stale.
  batch_state = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
  _docx = f'/mnt/user-data/outputs/{EXAM}_{pp.paper_slug(paper_id)}_Create.docx'
  _key = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  _kd = json.load(open(_key, encoding='utf-8'))
  PAPER_MD5 = hashlib.md5(open(_docx, 'rb').read()).hexdigest()
  # v5.96 (REVIEW-COVERAGE-LAW): the hash of every delivered block — computed by the auditor from the docx
  _hj = f'/home/claude/{EXAM}_M{N}_item_hashes.json'
  subprocess.run(['python3', f'/home/claude/{EXAM}_mock_test_audit.py', _docx, '--phase', 'precommit',
                  '--item-hashes', _hj], capture_output=True, text=True, env=AUDIT_ENV)
  REVIEW_HASHES = json.load(open(_hj, encoding='utf-8')) if os.path.exists(_hj) else {}
  _delta = [str(x) for x in (batch_state.get('delta_qs') or [])]          # empty -> the WHOLE paper
  _panel = [str(x) for x in (batch_state.get('delta_panel') or [])]
  _switch = {str(x) for x in (batch_state.get('delta_switch') or [])}     # adjudication: a different model
  if int(batch_state.get('review_round', 0)) < 2:
      _delta, _panel, _switch = [], [], set()                             # rounds 1-2: always the whole paper
  _items = []
  for _qn in sorted((_kd.get('concept_map') or {}), key=int):
      if (_delta or _panel) and _qn not in _delta and _qn not in _panel:
          continue
      _e = _kd['concept_map'][_qn]
      # stem_text / option_texts / figure_files are S7-QUALITY record fields (the sidecar
      # carries them since v5.90); the reviewer ALSO reads the docx in its part folder.
      _items.append({'q': int(_qn), 'subtopic_id': _e.get('subtopic_id'),
                     'stimulus_group_id': _e.get('stimulus_group_id'),    # a passage group is never split (E6)
                     'stem': _e.get('stem_text'), 'options': _e.get('option_texts'),
                     'figures': _e.get('figure_files') or [],
                     'content_record': {k: _e.get(k) for k in ('given_smiles', 'reagents', 'scheme_grammar',
                                                                'stated_formula', 'named_entities') if _e.get(k) is not None},
                     'class_word': _e.get('class_word'), 'stem_agents': _e.get('stem_agents'),
                     # the per-option mechanism list would reveal the key by elimination (one
                     # mechanism per WRONG option): the reviewer gets only the COUNT recorded.
                     'distractor_mechanisms_recorded': len(_e.get('distractor_mechanisms') or [])})
      # NOTE: no key, no difficulty, no author notes — bc.review_packet strips the rest
  _bank = json.load(open(EXEMPLAR_BANK_PATH, encoding='utf-8')) if EXEMPLAR_BANK_PATH else {}
  _slice = {c: v for c, v in (_bank.get('cells') or {}).items()
            if any(c == str(_e.get('subtopic_id') or '') or str(_e.get('subtopic_id') or '').startswith(c + '.')
                   for _e in _kd.get('concept_map', {}).values())}
  # v5.94: an organic paper's reviewer also names the concepts it USED, from the same
  # vocabulary the author selected from (S13-2G phase 3 scores the lower of the two lists)
  _l2_p1 = ((batch_state.get('difficulty_state') or {}).get('l2_model') or {})
  _l2_ids_p1 = set(_l2_p1.get('scope_ids') or []) if _l2_p1.get('active') else set()
  _vocab_p1 = (bc.l2_vocabulary() if any(str(_it.get('subtopic_id')) in _l2_ids_p1 for _it in _items) else None)
  _normal = [it for it in _items if str(it['q']) not in _panel and str(it['q']) not in _switch]
  _swit = [it for it in _items if str(it['q']) in _switch and str(it['q']) not in _panel]
  PACKET = bc.review_packet(_normal, _slice, PAPER_MD5, concept_vocabulary=_vocab_p1)
  if not _normal:
      PACKET['parts'] = []
  _extra = [('switch', p) for p in (bc.review_packet(_swit, _slice, PAPER_MD5, concept_vocabulary=_vocab_p1)['parts'] if _swit else [])]
  for _k in range(bc.REVIEW_PANEL_SIZE if _panel else 0):              # D-panel: one fresh reviewer per copy
      _extra += [('panel', p) for p in bc.review_packet([it for it in _items if str(it['q']) in _panel], _slice, PAPER_MD5,
                                                       concept_vocabulary=_vocab_p1)['parts']]
  for _kind, _pt in _extra:
      _pt['part'] = len(PACKET['parts']) + 1
      _pt['mode'] = _kind
      PACKET['parts'].append(_pt)
  REVIEW_ROUND = int(batch_state.get('review_round', 0)) + 1
  # INTERNAL ONLY (GAP-2026-11-04 A2): never /mnt/user-data/outputs, never present_files.
  REVIEW_DIR = f'/home/claude/{EXAM}_M{N}_review/{"delta" if REVIEW_ROUND > 2 else "round"}{REVIEW_ROUND}'
  if os.path.isdir(REVIEW_DIR):
      shutil.rmtree(REVIEW_DIR)                        # a re-run of phase 1 never reads stale verdicts
  _queue = []
  for _part in PACKET['parts']:
      # v5.96: the review MODE is in the folder name — the orchestrator receives only folder paths (worker
      # report --review-parts) and never opens queue.json: '_switch' / '_panel' -> a DIFFERENT-model reviewer
      _pdir = os.path.join(REVIEW_DIR, f"part{_part['part']}" + {'switch': '_switch', 'panel': '_panel'}.get(_part.get('mode'), ''))
      os.makedirs(_pdir, exist_ok=True)
      shutil.copy(_docx, os.path.join(_pdir, os.path.basename(_docx)))   # the reviewer views figures here
      _pk = {'exam': EXAM, 'paper_slug': pp.paper_slug(paper_id), 'paper_md5': PAPER_MD5,
             'review_round': REVIEW_ROUND, 'n_items': len(_part['items']), 'parts': [_part],
             'mode': 'internal'}
      json.dump(_pk, open(os.path.join(_pdir, 'review_packet.json'), 'w', encoding='utf-8'),
                ensure_ascii=False, indent=1)
      _queue.append({'part': _part['part'], 'dir': _pdir, 'qs': [int(it['q']) for it in _part['items']],
                     'verdicts': os.path.join(_pdir, 'verdicts.json'), 'attempts': 0, 'reviewer': None,
                     'error': None, 'switch': _part.get('mode') in ('switch', 'panel'),
                     'panel': _part.get('mode') == 'panel'})
  json.dump({'paper_md5': PAPER_MD5, 'round': REVIEW_ROUND, 'parts': _queue},
            open(os.path.join(REVIEW_DIR, 'queue.json'), 'w', encoding='utf-8'), indent=1)
  batch_state['state'] = 'REVIEW_RUNNING'
  batch_state['paper_md5'] = PAPER_MD5
  batch_state['review_dir'] = REVIEW_DIR
  batch_state['review_hashes'] = REVIEW_HASHES
  json.dump(batch_state, open(f'/home/claude/{EXAM}_M{N}_batch_state.json', 'w', encoding='utf-8'), indent=2)
  print(f"S13-2G phase 1: independent review round {REVIEW_ROUND} — {PACKET['n_items']} item(s) in "
        f"{len(_queue)} part(s), packet under {REVIEW_DIR} (internal; nothing for the user to do).")
  ```

  PHASE 2 — one fresh reviewer per part (the model's own turn, between the python blocks):
  ```
  # CLASS: T — PHASE 2 of S13-2G. Model agency: tool calls happen BETWEEN python blocks
  # (EXECUTION-BOUNDARY LAW) — this section is prose and is never implemented in python.
  #
  # For EACH part in REVIEW_DIR/queue.json (parts MAY run in parallel when the runtime can
  # launch several sub-agents in one turn; otherwise in sequence):
  #
  #  1. SUB-AGENT PATH (default). If this runtime offers a tool that starts a FRESH model
  #     context (a sub-agent / task tool — e.g. one named Agent or Task), launch ONE fresh
  #     sub-agent for the part, in the FOREGROUND, and wait for it. Its prompt is EXACTLY the
  #     REVIEWER BRIEF below with <PART_DIR> replaced by the part's 'dir'. Pass NOTHING else:
  #     no key, no notes, no bands, no batch_state, no summary of the paper, no opinion.
  #  2. CHECK. When it returns, <PART_DIR>/verdicts.json must exist and parse. If it does
  #     not, or the sub-agent errored or timed out: launch ONE fresh sub-agent again for that
  #     part (exactly one retry; record the error text in queue.json 'error').
  #  3. SAME-SESSION FALLBACK (owner decision D1, 2026-11-04 — the review is ALWAYS automatic):
  #     if the runtime has NO sub-agent tool, or the retry also failed, review that part
  #     YOURSELF as a cold reader, executing Framework_MockReview.md (it is routed with this
  #     step) end to end with REVIEW_WORK=<PART_DIR> and REVIEWER=same-session in the
  #     environment of each script (exactly as the brief below says): its S1-1 and S1-2
  #     blocks (they write <PART_DIR>/queue.json), then §2 item by item — deriving each
  #     own_key from the stem, the options and the figures in the docx ALONE; do NOT open the
  #     answer key, the sidecar, batch_state or your own notes while doing it — writing
  #     <PART_DIR>/answers.json, then its S3-1 and S3-2 blocks (S3-2 writes
  #     <PART_DIR>/verdicts.json).
  #     Weaker independence (owner accepted, D1/D4); disclosed by one footer line.
  #  3b. v5.96 SWITCHED REVIEWER. A part whose queue entry has 'switch' true (an adjudication,
  #     a panel copy, a D0 re-review — its folder name ends in _switch / _panel, or is 'switched')
  #     is reviewed by a DIFFERENT model than its previous reviewer:
  #     the next of SESSION_BUDGET.json worker_models (one model only, or no model choice: a fresh
  #     context of the same model — E14). A D0 re-review runs in <PART_DIR>/switched/ (copy the
  #     part's review_packet.json and docx there; the reviewer writes switched/verdicts.json).
  #     A same-session fallback review is NOT independent: it never certifies a disputed item (E13).
  #  4. Only if even the fallback could not write a verdict for an item does that item get
  #     NOT_RUN in phase 3 (bc.review_not_run, with the reason) — a WARN, never a stop.
  #  5. NEVER ask the user for anything here, never present a file, never end the response.
  #     Go straight on to phase 3.
  #
  # REVIEWER BRIEF (verbatim; fill <PART_DIR>):
  #   You are the INDEPENDENT REVIEWER of one part of an exam paper. You did not write it and
  #   you do not know its answer key. Work in bash; first `cd /tmp/fw_effective` (the verified
  #   framework). Read /tmp/fw_effective/Framework_MockReview.md IN FULL (sed -n in bash) and
  #   execute it in INTERNAL MODE with WORK=<PART_DIR> and REVIEWER='sub-agent'. Read ONLY the
  #   files inside <PART_DIR> and the framework spec. Do NOT open any other file under
  #   /home/claude or /mnt — never *_answer_key.json, *_batch_state.json, *_registry*.json,
  #   *_fig_manifest.json, *.figspec.json or any notes. Solve every item cold, as a candidate;
  #   open the docx in <PART_DIR> to view every figure (render the page to an image and look
  #   at it). Run S1-1 + S1-2 as ONE python script and S3-1 + S3-2 as ONE python script,
  #   each started as: cd /tmp/fw_effective && REVIEW_WORK=<PART_DIR> REVIEWER=sub-agent
  #   python3 - <<'EOF' ... EOF  (the blocks read REVIEW_WORK / REVIEWER from the
  #   environment). Write <PART_DIR>/answers.json between the two (§2), so that S3-2 writes
  #   <PART_DIR>/verdicts.json.
  #   Do not deliver, present or upload anything. Reply with ONE line:
  #   "REVIEW DONE <n> items" or "REVIEW FAILED <reason>".
  ```
  Record each part's outcome in REVIEW_DIR/queue.json before phase 3 (CLASS T bookkeeping:
  'reviewer' = 'sub-agent' | 'same-session', 'attempts', 'error') — phase 3 reads it.
  WORKER MODE (v5.93 — S1-0R): a worker sub-agent cannot start sub-agents. It writes each part's
  filled REVIEWER BRIEF to <PART_DIR>/REVIEWER_BRIEF.txt and hands the parts to the orchestrating
  chat, which starts the reviewers; it resumes at step 2 above with their returned lines
  (Framework_MockTestOrchestrate.md O3-6). Steps 2 to 5 and the NOT_RUN rule are unchanged.

  PHASE 3 — bind, repair or proceed (automatic, same response):
  ```python
  # ── S13-2G phase 3 (executable; also the S4-12 entry for an interrupted review) ──
  import json, os, blueprint_core as bc, paper_pipeline as pp
  batch_state = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
  REVIEW_DIR = batch_state.get('review_dir')
  _qf = json.load(open(os.path.join(REVIEW_DIR, 'queue.json'), encoding='utf-8'))
  _kd = json.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json', encoding='utf-8'))
  _md5 = batch_state.get('paper_md5')
  # v5.96: the items THIS round queued (the whole paper in rounds 1-2; only the delta items afterwards) — an
  # item outside a delta round keeps its last review and is never stamped NOT_RUN
  _queued = set()
  for _pq in _qf.get('parts') or []:
      _queued.update(str(q) for q in (_pq.get('qs') or []))
  _expected = sorted(_queued or set(_kd.get('concept_map') or {}), key=int)
  _recs, _why_by_q, _kinds = [], {}, set()
  for _p in _qf.get('parts') or []:
      _r = None
      try:
          _r = json.load(open(_p['verdicts'], encoding='utf-8')) if os.path.exists(_p['verdicts']) else None
      except (OSError, ValueError):
          _r = None
      _recs.append(_r)
      _kinds.add(str((_r or {}).get('reviewer') or _p.get('reviewer') or 'none'))
      for _q in _p.get('qs') or []:
          _why_by_q[str(_q)] = str(_p.get('error') or 'reviewer produced no verdict for this item after one retry')
  # v5.96 — key agreement per PART record (before D0 and the merge; the reviewer never saw the key)
  _ans3 = _kd.get('answers') or {}
  def _fill_ka(rec):
      for _qk, _rk in ((rec or {}).get('items') or {}).items() if isinstance((rec or {}).get('items'), dict) else []:
          if isinstance(_rk, dict):
              _rk['key_agrees'] = bc.review_key_agreement(_rk.get('own_key'), _ans3.get(str(_qk)),
                                                          ((_kd.get('concept_map') or {}).get(str(_qk)) or {}).get('ca_range'))
              if _rk['key_agrees'] is None:
                  _rk['confidence'] = 'low'
      return rec
  _recs = [_fill_ka(_r) for _r in _recs]
  # v5.96 D0 — REVIEWER HEALTH (bc.review_round_void): a part disputing more than bc.REVIEW_VOID_RATE of its
  # items is re-reviewed ONCE by a switched reviewer (<PART_DIR>/switched/verdicts.json). Its disputes are
  # dropped only when the switched reviewer clears >= bc.REVIEW_VOID_CONFIRM of them (E15).
  _void_now = []
  for _i, _p in enumerate(_qf.get('parts') or []):
      _it1 = (_recs[_i] or {}).get('items') if isinstance((_recs[_i] or {}).get('items'), dict) else {}
      if not _it1 or _p.get('panel') or not bc.review_round_void(_it1, len(_it1))[0]:
          continue
      _swp = os.path.join(_p['dir'], 'switched', 'verdicts.json')
      if not os.path.exists(_swp):
          if int(_p.get('d0_requested', 0)) >= 2:
              continue                          # the switched reviewer produced nothing twice: the disputes stand
          _p['d0_requested'] = int(_p.get('d0_requested', 0)) + 1
          _p['switch'] = True
          _void_now.append(_p['part'])
          continue
      _r2 = _fill_ka(json.load(open(_swp, encoding='utf-8')))
      if bc.review_void_confirmed([q for q, r in _it1.items() if not bc.review_record_agrees(r)], (_r2 or {}).get('items')):
          _recs[_i] = _r2                       # the first reviewer was faulty — its disputes count for nothing
  if _void_now:
      json.dump(_qf, open(os.path.join(REVIEW_DIR, 'queue.json'), 'w', encoding='utf-8'), indent=1)
      raise RuntimeError(f"REVIEW-VOID [HS:LADDER] (S13-2G D0): part(s) {_void_now} disputed more than "
                         f"{int(bc.REVIEW_VOID_RATE * 100)}% of their items — run PHASE 2 for those parts ONLY with a "
                         f"SWITCHED reviewer in <PART_DIR>/switched/ (step 3b), then this phase 3 again (a switched "
                         f"reviewer that writes nothing twice leaves the first reviewer's disputes standing — never a loop).")
  # v5.96 — every verdict is bound to the hash of the block it reviewed and kept in the item's history
  _H3 = batch_state.get('review_hashes') or {}
  _allrecs = {}
  for _i, _p in enumerate(_qf.get('parts') or []):
      for _qk, _rk in (((_recs[_i] or {}).get('items')) or {}).items():
          if isinstance(_rk, dict):
              _rk['item_hash'] = _H3.get(str(_qk))
              _rk['reviewer'] = str(_p.get('reviewer') or (_recs[_i] or {}).get('reviewer') or 'sub-agent')
              _allrecs.setdefault(str(_qk), []).append(_rk)
  VERDICTS, _missing, _mprobs = bc.review_merge_parts(_recs, _md5, _expected)
  for _pr in _mprobs:
      print(f"S13-2G phase 3: {_pr} — its items are NOT_RUN (recorded, never a stop).")
  # The reviewer never saw the key (bc.review_packet strips it; MockReview writes
  # key_agrees = null). THIS session owns the sidecar, so it fills key_agrees here from the
  # reviewer's own_key vs the stored answer (1-based position / sorted list / NAT value,
  # ca_range tolerance) — bc.review_key_agreement; None (unreadable own_key) is kept as None
  # and the record's confidence is forced 'low' so bind counts it as a defect.
  for _qn, _rec in (VERDICTS.get('items') or {}).items():
      if isinstance(_rec, dict):
          _cm_e = (_kd.get('concept_map') or {}).get(str(_qn)) or {}
          _rec['key_agrees'] = bc.review_key_agreement(_rec.get('own_key'), (_kd.get('answers') or {}).get(str(_qn)),
                                                       _cm_e.get('ca_range'))
          if _rec['key_agrees'] is None:
              _rec['confidence'] = 'low'
  _bind = bc.bind_review_verdicts(VERDICTS, _md5, len(VERDICTS.get('items') or {}))
  if not _bind['ok']:
      print(f"S13-2G phase 3: binding notes {_bind['problems']} (recorded; never a stop).")
  # v5.94 (GAP-2026-11-07 DL1; owner D1 (b), every exam) — THE difficulty decision of the review,
  # replacing DL-52 (which wrote a BELOW verdict as level_note 'reviewer below slot' and shipped it).
  # Per item, bc.dl_phase3_decision(target band, ...) with the controls the author does not hold:
  # the reviewer's band (only when it cites an exemplar), the in-batch measured band (CHECK 3c
  # difficulty_check['measured']), and for an organic item under a binding L2 model the ruler
  # re-measured on the LOWER-scoring of the author's and the reviewer's concept lists. Round 1
  # BELOW -> a review defect repaired at DR1 (REVIEW_REPAIR); round 2 BELOW -> the slot's S13-2L DIFFICULTY
  # chain (v5.96 — never a relabel). The slot band compared is the TARGET plan (S3-8L).
  _plan_p3 = {str(k): v for k, v in (batch_state.get('difficulty_plan') or {}).items()}
  _tgt_p3 = {str(k): v for k, v in (batch_state.get('difficulty_plan_target')
                                    or batch_state.get('difficulty_plan') or {}).items()}
  # the exam's labels persist in batch_state (S3-16) — this block also runs as the S4-12 resume
  # entry, where no blueprint is loaded
  _labs_p3 = list(batch_state.get('difficulty_labels')
                  or ((globals().get('bp') or {}).get('difficulty_labels') if isinstance(globals().get('bp'), dict) else None)
                  or ['Easy', 'Medium', 'Hard'])      # a pre-v5.92 batch_state has no labels key
  _ds_p3 = batch_state.setdefault('difficulty_state', {})
  _l2s_p3 = _ds_p3.get('l2_model') if isinstance(_ds_p3.get('l2_model'), dict) else {}
  _l2m_p3 = bc.l2_model_from_frozen(_l2s_p3.get('frozen')) if _l2s_p3.get('frozen') else None
  _l2ids_p3 = set(_l2s_p3.get('scope_ids') or [])
  _rr_p3 = int(batch_state.get('review_round', 0))
  _vi_p3 = {str(k): v for k, v in (VERDICTS.get('items') or {}).items() if isinstance(v, dict)}
  _prev_rep_p3 = {str(x) for x in (batch_state.get('review_dl_repair') or [])}   # round 1's repairs
  _dl_p3 = {'repair': [], 'to_chain': [], 'above': [], 'unverified_l2': []}
  for _qs in [str(x) for x in _expected]:
      if _qs not in _tgt_p3 or (_rr_p3 >= 2 and _qs not in _vi_p3):
          continue                     # v5.96: a DELTA round decides only the items it reviewed
      _cm_e = _kd['concept_map'].setdefault(_qs, {})
      _dc = dict(_cm_e.get('difficulty_check')) if isinstance(_cm_e.get('difficulty_check'), dict) else {}
      _obs = dict(_cm_e.get('difficulty_obs')) if isinstance(_cm_e.get('difficulty_obs'), dict) else {}
      _obs.setdefault('distractor_mechanisms', _cm_e.get('distractor_mechanisms'))
      _is_l2 = bool(_l2m_p3) and str(_cm_e.get('subtopic_id')) in _l2ids_p3
      _qt = str(_cm_e.get('qtype') or _obs.get('qtype') or 'mcq')   # the sidecar entry carries qtype
      _d = bc.dl_phase3_decision(_tgt_p3[_qs], _labs_p3, review_rec=_vi_p3.get(_qs), judge_band=_dc.get('measured'),
                                 l2_model=_l2m_p3 if _is_l2 else None, l2_obs=_obs if _is_l2 else None,
                                 review_round=_rr_p3, qtype=_qt)
      if _is_l2 and _d.get('concepts_from') == 'author_unverified':
          # the reviewer named no concepts: the author's list is not verified, so the ruler is not a
          # control for this item (recorded); the reviewer / in-batch bands decide
          _dl_p3['unverified_l2'].append(_qs)
          _d = bc.dl_phase3_decision(_tgt_p3[_qs], _labs_p3, review_rec=_vi_p3.get(_qs), judge_band=_dc.get('measured'),
                                     review_round=_rr_p3, qtype=_qt)
      _dc.update({'review_decision': _d['action'], 'review_measured': _d['measured'],
                  'review_controls': _d['controls'], 'reviewer_band': _d['reviewer_band'],
                  'reviewer_anchored': _d['reviewer_anchored'], 'dl_rule': _d['rule']})
      if isinstance(_d.get('l2'), dict):
          _dc['l2_review'] = {'band': _d['l2'].get('band'), 'score': _d['l2'].get('score'),
                              'concepts_from': _d.get('concepts_from')}
      _lb2_e3 = ((_dc.get('label_basis') or {}).get('kind') if isinstance(_dc.get('label_basis'), dict) else None) in bc.LB2_KINDS
      if _lb2_e3 and _d['action'] in ('repair', 'dr3'):
          # v6.0 (LAW-ORG-5): a label measured by two fresh blind graders + the recipe is not re-authored on ONE
          # reviewer's band — the reviewer's band is recorded as advisory; difficulty changes come only from grades
          _dc['review_note'] = 'advisory — LB2 label (two fresh blind graders + recipe) kept'
      elif _d['action'] == 'repair':
          _dl_p3['repair'].append(_qs)
          _dc['dl_rung'] = 'DR1'
      elif _d['action'] == 'dr3':
          # v5.96 (OD-2026-11-09): NEVER a relabel. The slot keeps its band ('carried_below'); S13-2L opens /
          # advances its DIFFICULTY chain — rework, replace, shape, sibling, then the SC2 endings (v6.0).
          _dl_p3['to_chain'].append(_qs)
          _dc['decision'] = 'carried_below'
      else:
          if _d['action'] == 'above':
              _dl_p3['above'].append(_qs)
          if _dc.get('decision') == 'carried_below':
              _dc['decision'] = 'dl_agree'          # the review measured it at (or above) its slot
          _lab = _cm_e.get('difficulty')
          _m = _d.get('measured')
          # v6.0 (LB2): a label certified by two fresh blind graders + the recipe (measured_exact) or disclosed as
          # last_resort is NEVER rewritten here — a disagreeing review opens the slot's chain (S13-2L), never a
          # relabel (a relabel to max(measured, slot) would print the REQUESTED band on a last-resort item)
          _lb2_p3 = ((_dc.get('label_basis') or {}).get('kind') if isinstance(_dc.get('label_basis'), dict)
                     else None) in bc.LB2_KINDS
          if (not _lb2_p3 and _lab in _labs_p3 and _m in _labs_p3 and _labs_p3.index(_m) < _labs_p3.index(_lab)
                  and _lab != _tgt_p3[_qs]):
              # an R5 'harder' label above its slot that the review measures lower: the label follows
              # the evidence, never below the slot
              _nb = _labs_p3[max(_labs_p3.index(_m), _labs_p3.index(_tgt_p3[_qs]))]
              _cm_e['difficulty'], _plan_p3[_qs] = _nb, _nb
              _dc.update({'final_band': _nb, 'decision': 'dl_agree'})
      _cm_e['difficulty_check'] = _dc
  _bind['defects'] = sorted(set(str(x) for x in _bind['defects']) | set(_dl_p3['repair']), key=int)
  batch_state['difficulty_plan'] = _plan_p3
  batch_state['review_dl_repair'] = list(_dl_p3['repair'])
  if any(_dl_p3.values()):
      print(f"S13-2G phase 3 (DL1): below their slot -> repair now {_dl_p3['repair']}; still below -> S13-2L "
            f"difficulty chain {_dl_p3['to_chain']}; above their slot (label kept) {_dl_p3['above']}; "
            f"organic items whose reviewer named no concepts (ruler not used) {_dl_p3['unverified_l2']}.")
  for _qn, _rec in (VERDICTS.get('items') or {}).items():          # the verdict lives ON the item (§4.3)
      _kd['concept_map'].setdefault(str(_qn), {})['review'] = dict(_rec, paper_md5=_md5)
  for _qn, _rl in _allrecs.items():                                 # v5.96: every verdict, oldest first
      _kd['concept_map'].setdefault(str(_qn), {}).setdefault('review_history', []).extend(
          dict(_r, paper_md5=_md5) for _r in _rl)
  for _qn in _missing:                                              # A5: NOT_RUN, a WARN in A-REVIEW
      # v5.96: bound to the text it could not review (REVIEW-COVERAGE-LAW — the round terminates)
      _kd['concept_map'].setdefault(str(_qn), {})['review'] = dict(bc.review_not_run(_why_by_q.get(str(_qn)), _md5),
                                                                   item_hash=(batch_state.get('review_hashes') or {}).get(str(_qn)))
  json.dump(_kd, open(f'/home/claude/{EXAM}_M{N}_answer_key.json', 'w', encoding='utf-8'), indent=2)
  REVIEW_DEFECTS = _bind['defects']                                 # key disagreement / low confidence / contested
  batch_state['review_round'] = int(batch_state.get('review_round', 0)) + 1
  batch_state['review_defects'] = list(REVIEW_DEFECTS)              # persisted: an interrupted response continues from it
  _summ = batch_state.setdefault('review_summary', {'repaired': [], 'not_run': [], 'reviewer': []})
  _summ['round'] = batch_state['review_round']
  _summ['not_run'] = sorted(set(_missing), key=int)            # the LATEST round's gaps only
  _summ['reviewer'] = sorted(set(_summ.get('reviewer') or []) | (_kinds - {'none'}))
  if REVIEW_DEFECTS and batch_state['review_round'] < 2:            # exactly ONE more review round
      _summ['repaired'] = sorted(set(_summ.get('repaired') or []) | set(REVIEW_DEFECTS), key=int)
      print(f"S13-2G: reviewer flagged {REVIEW_DEFECTS} — repairing NOW, in this response: each "
            f"through §Q8b-LADDER (entry bc.ladder_entry('review_disagreement') = R2; the reviewer's "
            "reason is the constraint), then S13-2F (a changed docx needs a fresh certificate), then "
            "S13-2G phase 1 again — round 2 always carries the WHOLE paper.")
      batch_state['state'] = 'REVIEW_REPAIR'
  else:
      # v5.96 (OD-2026-11-09, supersedes OD-9) — DISPUTE CHAINS. (v6.0: the review panel is retired — LAW-ORG-7.)
      # An open dispute chain whose item now
      # agrees is CERTIFIED once two consecutive independent verdicts on its current hash agree
      # (bc.review_item_certified) — one agreement only: S13-2L schedules one more delta review. Any other
      # dispute opens / advances that slot's dispute chain. Never UNRESOLVED; never NOT CERTIFIED.
      # v6.0 (LAW-ORG-7): a dispute attempt passes only when its CURRENT text also has a unanimous key (author +
      # 2 fresh blind solvers, concept_map[q].key_votes — S0-OP-5 C7); S13-2L never schedules a panel any more.
      _chs3 = batch_state.setdefault('slot_chain', {})
      _done3 = set()
      _miss3 = {str(x) for x in _missing}
      for _qc, _c3 in list(_chs3.items()):
          if not isinstance(_c3, dict) or _c3.get('kind') != 'dispute' or _c3.get('done') \
                  or (_qc not in _allrecs and _qc not in _miss3):
              continue
          _hist3 = [r for r in ((_kd['concept_map'].get(_qc) or {}).get('review_history') or [])
                    if r.get('item_hash') == _H3.get(_qc)]
          _c3.pop('awaiting', None)        # v6.0 (LAW-ORG-7): the review PANEL is retired — a leftover 'panel' wait is dropped
          if bc.review_item_certified(_hist3, _H3.get(_qc)) \
                  and (((_kd['concept_map'].get(_qc) or {}).get('key_votes') or {}).get('unanimous') is True) \
             and bc.op_controls_current(_kd['concept_map'].get(_qc), (_kd['concept_map'].get(_qc) or {}).get('key_votes')):
              _st3 = ((_c3.get('attempts') or [{}])[-1] or {}).get('stage') or 'adjudicate'
              _chs3[_qc] = bc.slot_chain_record(_c3, _st3, 'pass')
              _done3.add(_qc)
          elif bc.review_item_certified(_hist3, _H3.get(_qc)) and \
                  ((_c3.get('attempts') or [{}])[-1] or {}).get('outcome') == 'pending':
              # the reviews agree but the key is not unanimous on THIS text (author + 2 fresh blind solvers): the
              # attempt FAILS and the chain moves on (bounded) — never left pending
              _chs3[_qc] = bc.slot_chain_record(_c3, _c3['attempts'][-1]['stage'], 'fail', note='key not unanimous')
              _done3.add(_qc)
          elif ((_c3.get('attempts') or [{}])[-1] or {}).get('outcome') == 'pending' and (
                  _qc in _miss3 or not bc.review_record_independent((_allrecs.get(_qc) or [{}])[-1])):
              # E13: a NOT_RUN or same-session verdict can never certify a disputed item — the attempt fails and
              # the chain moves on (bounded), instead of being queued again forever
              _chs3[_qc] = bc.slot_chain_record(_c3, _c3['attempts'][-1]['stage'], 'fail', note='no independent verdict')
              _done3.add(_qc)
      for _qn in [str(x) for x in REVIEW_DEFECTS if str(x) not in _done3]:
          _c3 = _chs3.get(_qn)
          _a3 = (_c3 or {}).get('attempts') or []
          if _c3 and not _c3.get('done') and _c3.get('kind') == 'dispute':
              if _a3 and _a3[-1].get('outcome') == 'pending':
                  _chs3[_qn] = bc.slot_chain_record(_c3, _a3[-1]['stage'], 'fail')
          else:
              # correctness first: an open difficulty / quality / upgrade chain on this slot is SUSPENDED inside the
              # dispute chain (bc.slot_chain_reopen — resumed later with its attempt count; a finished chain is kept
              # in 'history' so its footer line is never lost)
              _chs3[_qn] = bc.slot_chain_reopen(_c3, _qn, 'dispute', _tgt_p3.get(_qn),
                                                (_kd['concept_map'].get(_qn) or {}).get('subtopic_id'))
      json.dump(_kd, open(f'/home/claude/{EXAM}_M{N}_answer_key.json', 'w', encoding='utf-8'), indent=2)
      batch_state['uncertified_items'] = []
      batch_state['delta_qs'], batch_state['delta_panel'], batch_state['delta_switch'] = [], [], []
      if REVIEW_DEFECTS:
          print(f"S13-2G: items {REVIEW_DEFECTS} disputed after round {batch_state['review_round']} — each enters its "
                "DISPUTE chain (S13-2L / S13-2R), never UNRESOLVED (OD-2026-11-09).")
      batch_state['state'] = 'REVIEWED'
      print(f"S13-2G: REVIEWED — round {batch_state['review_round']}, "
            f"{len(_summ.get('repaired') or [])} item(s) repaired, {len(_summ['not_run'])} not run; "
            "continuing to S13-2L (slot chains, delta reviews, coverage) in this response.")
  json.dump(batch_state, open(f'/home/claude/{EXAM}_M{N}_batch_state.json', 'w', encoding='utf-8'), indent=2)
  ```
  REVIEW_REPAIR -> repair the items in batch_state['review_defects'] NOW (same response); after
  EACH item's repair is written, append its q to batch_state['review_repaired'] and save
  batch_state (an interrupted response then never repeats a repair — S4-12); then S13-2F
  re-sweep, phase 1 again with the WHOLE paper (round 2), phase 2, phase 3.
  v5.94 — A DIFFICULTY REPAIR (q in batch_state['review_dl_repair']): re-author the item at its
  SLOT band (the target plan) through CHECK 3c — DR1 from the NEXT pattern source (an organic
  item: bc.l2_slot_source(..., skip = sources already tried); any other item: the next exemplar of
  its cell), then DR2's band-target brief if CHECK 3c still measures it below; the reviewer's
  difficulty reason is the constraint. Never relabel here: the item returns as 'agree' or
  'carried_below'; round 2's phase 3 decides (accept, or the S13-2L difficulty chain — v5.96).
  REVIEWED -> S13-2L (v5.96) / S13-3 / S13-4 / S13-REGCHECK / S13-QINDEX / S13-4b / S13-4c / S13-6 / S13-7 /
  S13-8 in the SAME response. The S13-4c auditor's A-REVIEW reads the review record
  final_assembly committed on EVERY item (the auditor's effective concept map overlays the
  registry record — it needs no sidecar at S13-4c); a record bound to a stale item_hash is an item
  finding (A-REVIEW-COVERAGE, ladder RV); a NOT_RUN record is a WARN (A5).
  A verdict file the user happens to attach is NEVER required; S4-12 says when one is used.

## S13-2P — ORGANIC PARITY + FIGURE PROOFS AT ASSEMBLY (v6.0 — §S0-OP-9; LAW-ORG-11, LAW-ORG-8)

  Runs after S13-2G and before S13-2L on EVERY paper (no organic item -> PASS). Never a stop.
  ```python
  # ── S13-2P parity (v6.0) ──
  import json, os, final_assembly as fa, blueprint_core as bc
  _kp = json.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json', encoding='utf-8'))
  _cmp = _kp.get('concept_map') or {}
  if 'OP_TARGET_POOL' not in globals():                       # resume-safe: the S0-OP working profile
      _opw2 = f'/home/claude/{EXAM}_op_profile.json'
      OP_TARGET_POOL = bc.pyq_target_pool(json.load(open(_opw2, encoding='utf-8')) if os.path.exists(_opw2) else {'papers': {}})
  _n_org = sum(1 for _e in _cmp.values() if isinstance(_e, dict) and _e.get('organic') is True)
  _fl = bc.format_floors(bc.format_shares(OP_TARGET_POOL), _n_org)
  _cv = bc.convention_floors(bc.convention_shares(OP_TARGET_POOL), _n_org)
  _past2 = [r for r in OP_TARGET_POOL if r.get('organic') is True]
  _share2 = (sum(1 for r in _past2 if len(r.get('decisions') or []) >= 2) / len(_past2)) if _past2 else None
  PARITY = fa.paper_parity_gate(_cmp, _fl, _cv, _share2)
  _fmp = f'/home/claude/{EXAM}_fig_manifest.json'
  FIGPROOF = fa.paper_figure_proof_gate(_cmp, json.load(open(_fmp, encoding='utf-8')) if os.path.exists(_fmp) else None)
  print(f"S13-2P: parity {PARITY['status']} (chain share {PARITY['chain_share']}; short {PARITY['short']}); "
        f"figure proofs {FIGPROOF['status']} {FIGPROOF['missing'] or ''}")
  _bs2p_p = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _bs2p = json.load(open(_bs2p_p, encoding='utf-8'))
  _bs2p.setdefault('difficulty_state', {})['parity'] = {k: PARITY.get(k) for k in ('status', 'chain_share', 'short')}
  json.dump(_bs2p, open(_bs2p_p, 'w', encoding='utf-8'), indent=2)   # read by S13-2L (§LADDER-OP line, resume-safe)
  ```

  v6.1 (S0-NF-2 / -4 / -6) — the MEASURED composition record of every item of every subject, written before
  S13-2L reads the paper. The A-* gates re-measure the same quantities on the delivered docx; this block is the
  run's own view, used to open repairs before assembly. Never a stop.
  ```python
  # ── S13-2P NF measure (v6.1) ──
  import json, blueprint_core as bc, figure_types as ft
  _kpn_p = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  _kpn = json.load(open(_kpn_p, encoding='utf-8'))
  _cmn = _kpn.get('concept_map') or {}
  _ansn = _kpn.get('answers') or {}                                     # 1-based option position (sidecar convention)
  _items_n = []
  for _q, _e in _cmn.items():
      if not isinstance(_e, dict):
          continue
      _opts = list(_e.get('option_texts') or [])
      _e['measured_axis2'] = bc.nf_measure_axis2(_e, ft.normalise_ask_format)   # D-06: re-measured, never ask_format
      _e['mip'] = bc.nf_item_mip(_e.get('stem_text'), _opts, _ansn.get(str(_q)), _e['measured_axis2'])   # None: not multi-part
      _e['text_fingerprint'] = bc.text_item_fingerprint(dict(_e, q=_q))
      _k = _ansn.get(str(_q))
      _kt = (_opts[int(_k) - 1] if (_opts and str(_k).isdigit() and 1 <= int(_k) <= len(_opts)) else
             (None if _opts or isinstance(_k, (list, dict)) or _k is None else str(_k)))
      _items_n.append(dict(_e, q=_q, key_text=_kt,
                           concept=((_e.get('grader_meta') or {}).get('grader_1') or {}).get('concept')))
  NF_INTRADUP = bc.intra_paper_duplicates(_items_n)
  NF_KEYLEAK = bc.key_leak_check(_items_n, [r.get('stem_snippet') for r in bc.pyq_guard_pool(OP_PROFILE)
                                            if r.get('stem_snippet')] if 'OP_PROFILE' in globals() else [])
  json.dump(_kpn, open(_kpn_p, 'w', encoding='utf-8'), indent=2)
  print(f"S13-2P NF: within-paper repeats {[(a, b) for a, b, _w in NF_INTRADUP] or 'none'}; "
        f"key leaks {[(a, b) for a, b, _v in NF_KEYLEAK] or 'none'} — each later item enters its quality chain (S13-2L)")
  ```

## S13-2L — PAPER DIFFICULTY GATE + SLOT CHAINS (v6.0 — GAP-2026-11-10 G-10; LAW-ORG-3/4/5/7; owner 2026-11-10, every exam)

  Runs once S13-2G is REVIEWED, before S13-3 / S13-4, in the same response (and as the S4-12 entry
  whenever batch_state['slot_chain'] holds an open chain or batch_state['slot_chain_work'] is not
  empty). OWNER RULES (2026-11-10, supersede OD-2026-11-09 for every paper produced by this release):
  the requested difficulty schedule is delivered EXACTLY — never relabelled, swapped, carried, held or
  forced; no question and no paper is ever NOT CERTIFIED; nothing is delivered with a known defect, a
  disputed key or a wrong label; no step is manual; nothing here is a stop. EVERY item of EVERY exam
  (organic or not) carries an LB2 label basis written by bc.dl_set_label_basis_strict:
    measured_exact — two FRESH blind graders (S0-OP-5, each in a fresh context that never saw the author's
      plan, band or counts; packet sha256 recorded) AND the band-recipe check all name the slot's band
      (bc.band_exact — no vote; any disagreement is not exact).
    last_resort    — the bounded last resort below (one AMBER line + an automatic P0 incident).
  A slot whose label does not verify (bc.verify_difficulty_label(..., strict=True)) — whether it measured
  BELOW or ABOVE its band — gets ONE bounded SLOT CHAIN (bc.slot_chain_*; rule SC2; batch_state['slot_chain'][q]):
    difficulty — rework DR1, rework DR2, replace (3), another ask shape (2), sibling subtopic (2 each, at
      most 3 siblings), each attempt writing bc.k_candidates() candidates (v6.1: 1 — S0-BV; reached only by a
      question that S4-7 STEP A2 could not settle: a pre-v6.1 paper, or an unlabelled item), each fully controlled (2 blind graders + recipe, 2 blind solvers, figure proofs, clone
      guard, stem stereo gate); then the SC2 ENDINGS:
        reserve_refill — bc.reserve_take(EXACT band, qtype, subtopic -> topic) from {EXAM}_reserve.json
          (verified items that passed everything but were not chosen; a reserve item made under another
          ruler version is re-graded first — never used on its old grade);
        refill_session — bc.refill_session_next(batch_state): a FRESH worker (Orchestrate O-REFILL) resumes
          from saved state and writes up to bc.C_REFILL_CANDIDATES candidates per open slot (composer and
          library on); at most bc.C_REFILL_SESSIONS (5) per paper;
        last_resort (difficulty only, LAW-ORG-4) — the nearest-band FULLY VERIFIED item (unanimous key,
          proven figures, original): a reserve item (bc.reserve_take nearest=True), else the slot's own
          current item when its two blind grades + recipe agree exactly on another band; delivered at THAT
          measured band (never labelled as the requested band), one AMBER footer line (requested vs
          delivered) and an automatic P0 incident (bc.last_resort_incident -> difficulty_state['incidents']).
          If neither exists the slot gets a 'last_resort_generate' work entry (a fresh worker writes
          candidates nearest band first until one is fully verified — each round a fresh worker, so this
          can never exhaust a session).
    dispute (the author and the 2 blind solvers do not give the same answer — LAW-ORG-7; panel, re-key and
      majority are RETIRED) — adjudicate, replace (3), shape (2), sibling (2 x 3), then reserve_refill ->
      refill_session -> last_resort (a verified reserve item, any band, nearest first; else
      'last_resort_generate'). A disputed key is NEVER delivered.
    quality (an item finding that survived the S13-2F terminal rung; DISCLOSED / amber is RETIRED for items)
      — replace (3), shape (2), sibling (2 x 3), then the same SC2 endings. A known defect is NEVER delivered.
  Every changed item is re-swept (S13-2F) and re-reviewed in a DELTA round (S13-2G); before S13-3 every
  item's latest review must be bound to its delivered text (REVIEW-COVERAGE-LAW, bc.review_coverage_missing).
  The gate record goes to batch_state['difficulty_state']['paper_gate'] (committed at S13-4, printed by S13-6).
  Chains recorded under rule SC1 (a paper resumed from 2026.11.09) keep their recorded outcome; any OPEN SC1
  chain is migrated to SC2 here (its attempts are kept; its SC1 terminals are never run).
  ```python
  # ── S13-2L (v6.0) ──
  import json, os, datetime as _dt_l, blueprint_core as bc
  _bsl_p = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _key_l = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  _bs_l = json.load(open(_bsl_p, encoding='utf-8'))
  _kd_l = json.load(open(_key_l, encoding='utf-8'))
  _cm_l = _kd_l.setdefault('concept_map', {})
  _labs_l = list(_bs_l.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
  _tgt_l = {str(k): v for k, v in (_bs_l.get('difficulty_plan_target') or _bs_l.get('difficulty_schedule_original') or {}).items()}
  _fz_l = (_bs_l.get('schedule_frozen') or {}).get('placement') if isinstance(_bs_l.get('schedule_frozen'), dict) else None
  if isinstance(_fz_l, dict) and _fz_l and {str(k): v for k, v in _fz_l.items()} != _tgt_l:
      # S0-OP-3: the FROZEN placement is the authority — a drifted target plan (a legacy swap) is never used
      print(f"S13-2L: target plan differs from the frozen placement at "
            f"{sorted((q for q in _fz_l if _tgt_l.get(str(q)) != _fz_l[q]), key=lambda x: int(x))} — frozen placement used.")
      _tgt_l = {str(k): v for k, v in _fz_l.items()}
      _bs_l['difficulty_plan_target'] = dict(_tgt_l)
  _chs = _bs_l.setdefault('slot_chain', {})
  _ds_l = _bs_l.setdefault('difficulty_state', {})
  _hjl = f'/home/claude/{EXAM}_M{N}_item_hashes.json'          # written by every S13-2F sweep / S13-2G phase 1
  _hl = json.load(open(_hjl, encoding='utf-8')) if os.path.exists(_hjl) else {}
  _bp_l = json.load(open(BP_SRC_PATH, encoding='utf-8')) if os.path.exists(BP_SRC_PATH) else {}
  _subs_l = [x for x in (_bp_l.get('subtopic_list') or []) if isinstance(x, dict)]
  _rsv_p = f'/home/claude/{EXAM}_reserve.json'                 # S0-OP-7: per exam, persists across the series
  _rsv = json.load(open(_rsv_p, encoding='utf-8')) if os.path.exists(_rsv_p) else bc.reserve_new(EXAM)
  _ruler_v = ((_ds_l.get('ruler') or {}).get('ruler_version') or (_bs_l.get('exam_ruler') or {}).get('ruler_version')
              or (globals().get('EXAM_RULER') or {}).get('ruler_version'))
  _today = _dt_l.date.today().isoformat()
  def _siblings(sid):
      # same topic by r_avg desc, then the rest of the section (E19: a blueprint id missing from the manifest is fine)
      me = next((x for x in _subs_l if x.get('subtopic_id') == sid), {})
      rk = lambda x: (-float(x.get('r_avg') or 0), str(x.get('subtopic_id')))
      t1 = sorted((x for x in _subs_l if x.get('topic') == me.get('topic') and x.get('subtopic_id') != sid), key=rk)
      t2 = sorted((x for x in _subs_l if x.get('section') == me.get('section') and x.get('topic') != me.get('topic')), key=rk)
      return [x['subtopic_id'] for x in t1 + t2]
  def _fresh(q):
      return bool(_hl.get(q)) and ((_cm_l.get(q) or {}).get('review') or {}).get('item_hash') == _hl.get(q)
  def _grades(q):
      # the two FRESH blind grades + the recipe verdict of the item's CURRENT text (S0-OP-5); {} when not graded.
      # v6.0: a grades record counts only while bc.op_record_controls' content binding holds (a replaced item never
      # inherits its predecessor's grades; a record not written by the one writer is not a grade)
      g = (_cm_l.get(q) or {}).get('grades') or {}
      if not bc.op_controls_current(_cm_l.get(q), g):
          return {}, {}
      if _hl.get(q) and g.get('item_hash') not in (None, _hl.get(q)):
          return {}, {}
      return ({'grader_1': g.get('grader_1'), 'grader_2': g.get('grader_2'), 'recipe': g.get('recipe') is True},
              g.get('packets') or {})
  def _recipe_at(q, band):
      # the band recipe verdict AT `band` (the recorded grades.recipe was checked at the slot's target band)
      _ru = _bs_l.get('exam_ruler') or globals().get('EXAM_RULER') or {}
      _rb = (_ru.get('recipe') or {}).get(band) if isinstance(_ru.get('recipe'), dict) else None
      if not isinstance(_rb, dict):                               # no ruler recipe for that band: the recorded verdict
          return _grades(q)[0].get('recipe') is True
      _rc = bc.band_recipe_check(_cm_l.get(q), _rb)
      return bool(_rc[0]) or (bool(_rc[1]) and all('dormant' in str(_x) for _x in _rc[1]))   # RDKit absent: dormant
  def _exact_at(q, band):
      ctl, pk = _grades(q)
      e2, ok, _w = bc.dl_set_label_basis_strict(_cm_l.get(q), 'measured_exact', _labs_l, band, ctl, pk)
      return (e2 if ok else None)
  def _unanimous(q):
      _kv = (_cm_l.get(q) or {}).get('key_votes') or {}
      return _kv.get('unanimous') is True and bc.op_controls_current(_cm_l.get(q), _kv)
  def _strict_ok(q):
      # v6.1 (S0-BV BV-5): a question settled in its batch at the band it measured after its one rewrite is final —
      # disclosed, never chained again
      return bc.verify_difficulty_label(_cm_l.get(q), _labs_l, strict=True)[0] and (
          _cm_l[q].get('difficulty') == _tgt_l.get(q) or bc.bv_settled(_cm_l.get(q), _labs_l))
  # work S13-2L scheduled earlier that S13-2R has not performed yet is CARRIED (a re-entry never takes a second reserve
  # item or spends a second refill session for the same slot)
  _delta, _switch, _changed = set(), set(), False
  _work = [w for w in (_bs_l.get('slot_chain_work') or []) if isinstance(w, dict) and w.get('status') == 'todo']
  _incidents = _ds_l.setdefault('incidents', [])
  # 0. MIGRATE an open SC1 chain (a paper parked under 2026.11.09) onto SC2: attempts kept, SC1 terminals never run
  for _q, _c in list(_chs.items()):
      if not _c.get('done') and _c.get('rule') in ('SC1', None):
          _chs[_q] = dict(_c, rule=bc.SC_RULE_CURRENT, terminal_tried=[], awaiting=None)
  # 1. OUTCOMES — an attempt is decided once its delta review AND its fresh grades are bound to its new text
  for _q, _c in list(_chs.items()):
      _att = _c.get('attempts') or []
      if _c.get('done') or not _att or _att[-1].get('outcome') != 'pending' or not _fresh(_q):
          continue
      _rv_o = (_cm_l.get(_q) or {}).get('review') or {}
      _t = _c.get('target') or _tgt_l.get(_q)
      _ok = False
      if _att[-1].get('stage') == 'last_resort':
          # an inserted / generated last-resort item: delivered at the band its fresh grades + recipe agree on
          _ctl, _pk = _grades(_q)
          _gb = _ctl.get('grader_1') if _ctl.get('grader_1') == _ctl.get('grader_2') else None
          _lrr = _bs_l.setdefault('last_resort_rounds', {})
          _nlr = int(_lrr.get(_q) or 0)
          if _gb in _labs_l and not _recipe_at(_q, _gb) and _nlr >= bc.C_LAST_RESORT_ROUNDS:
              _ctl = dict(_ctl, recipe=True, recipe_note=f'recipe not met after {_nlr} rounds (disclosed)')
          else:
              _gb = _gb if (_gb in _labs_l and _recipe_at(_q, _gb)) else None
          if _gb is not None:
              _ctl = dict(_ctl, recipe=True)                       # the recipe verdict AT the delivered band
          _clean = (str(_rv_o.get('status') or '').upper() != 'NOT_RUN' and _unanimous(_q)
                    and not (_cm_l.get(_q) or {}).get('item_findings'))
          if _clean and _gb == _t:
              _e2 = _exact_at(_q, _t)
              if _e2 is not None:
                  _cm_l[_q] = _e2
                  # the replacement measured EXACTLY at the requested band: no deviation, no AMBER line
                  _cr = dict(_c, attempts=_att[:-1])
                  _chs[_q] = bc.slot_chain_record(_cr, 'last_resort_round', 'pass', item_hash=_hl.get(_q))
                  _changed = True
                  continue
          if _clean and _gb in _labs_l:
              _cr = dict(_c, attempts=_att[:-1])
              _inc = bc.last_resort_incident(EXAM, _bs_l.get('paper_id'), _q, _t, _gb,
                                             [a.get('stage') for a in _att], _ruler_v, _today)
              _fin = bc.slot_chain_finish(_cr, 'last_resort', delivered=_gb, incident_id=_inc['incident_id'])
              _ef, _okf, _whyf = bc.dl_set_label_basis_strict(_cm_l.get(_q), 'last_resort', _labs_l, _t, _ctl, _pk,
                                                              chain=_fin, delivered=_gb, incident_id=_inc['incident_id'])
              if _okf:
                  _cm_l[_q], _chs[_q], _changed = _ef, _fin, True
                  _cm_l[_q]['last_resort'] = {'requested': _t, 'delivered': _gb, 'incident_id': _inc['incident_id'],
                                              **({'note': _ctl['recipe_note']} if _ctl.get('recipe_note') else {})}
                  _incidents.append(_inc)
                  _bs_l.setdefault('last_resort_slots', []).append({'q': _q, 'requested': _t, 'delivered': _gb})
                  continue
          # not verified: this round failed; the last-resort terminal stays untried, so S13-2L schedules another round —
          # counted (bc.C_LAST_RESORT_ROUNDS with the recipe; twice that and the graders never agree is the NO-MODEL
          # environment failure: state saved, resume)
          _lrr[_q] = _nlr + 1
          if _lrr[_q] > 2 * bc.C_LAST_RESORT_ROUNDS:
              json.dump(_bs_l, open(_bsl_p, 'w', encoding='utf-8'), indent=2)
              raise RuntimeError(f"NO-MODEL [HS:ENV] (S13-2L): Q{_q}: {_lrr[_q] - 1} last-resort rounds and the two fresh blind "
                                 f"graders never agreed on a band — the grading environment is not producing independent "
                                 f"grades. State saved; restore sub-agents / Orchestrate workers and type continue.")
          _chs[_q] = bc.slot_chain_record(_c, 'last_resort_round', 'fail', item_hash=_hl.get(_q))
          _chs[_q]['attempts'] = [a for a in _chs[_q]['attempts'] if a.get('stage') != 'last_resort']
          continue
      if _c.get('kind') != 'difficulty':
          continue        # a dispute attempt is decided by S13-2G phase 3, a quality attempt by the S13-2F re-sweep
      if str(_rv_o.get('status') or '').upper() != 'NOT_RUN' and _unanimous(_q):
          _e2 = _exact_at(_q, _t)
          if _e2 is not None:
              _cm_l[_q], _ok = _e2, True
      _chs[_q] = bc.slot_chain_record(_c, _att[-1]['stage'], 'pass' if _ok else 'fail', item_hash=_hl.get(_q))
      if not _ok and _att[-1].get('stage') == 'refill_session' and int(_bs_l.get('refill_sessions_used') or 0) < bc.C_REFILL_SESSIONS:
          # another fresh refill session may still be spent on this slot (the budget is per PAPER, F-10.4)
          _chs[_q]['terminal_tried'] = [t for t in (_chs[_q].get('terminal_tried') or []) if t != 'refill_session']
      _changed = _changed or _ok
  # 2. OPEN a difficulty chain on every slot whose label does not verify STRICTLY at its band (below OR above —
  #    an item is never relabelled to what it measured); a slot whose dispute / quality chain is open waits
  if _tgt_l:
      for _q in sorted(_tgt_l, key=int):
          if _q not in _cm_l or _strict_ok(_q):
              continue
          _e2 = _exact_at(_q, _tgt_l[_q])                          # first grading of an item never chained
          if _e2 is not None and _unanimous(_q):
              _cm_l[_q], _changed = _e2, True
              continue
          _c = _chs.get(_q)
          if _c and _c.get('done') and _c.get('outcome') == 'last_resort':
              continue                                             # ended and disclosed — never reopened
          if not _c or _c.get('done'):
              _chs[_q] = bc.slot_chain_reopen(_c, _q, 'difficulty', _tgt_l.get(_q), (_cm_l.get(_q) or {}).get('subtopic_id'))
  # 2b. FIGURE PROOFS (LAW-ORG-8, S13-2P): an organic item whose figure is unproven — or that places a picture with no
  #     proof record — opens its QUALITY chain (replaced, never shipped unproven); re-checked on every S13-2L pass
  import final_assembly as _fa_l
  _fmp_l = f'/home/claude/{EXAM}_fig_manifest.json'
  _fp_l = _fa_l.paper_figure_proof_gate(_cm_l, json.load(open(_fmp_l, encoding='utf-8')) if os.path.exists(_fmp_l) else None)
  _ds_l['figproof'] = {'status': _fp_l['status'], 'missing': _fp_l['missing']}
  for _q in sorted(_fp_l['missing'], key=int):
      _c = _chs.get(_q)
      if _c and not _c.get('done'):
          continue                                                 # a chain is already working on this slot
      if _c and _c.get('done') and _c.get('outcome') == 'last_resort':
          continue
      _ro = _bs_l.setdefault('reopen_count', {})
      if int(_ro.get(f'{_q}:figproof') or 0) >= 2:
          _ds_l.setdefault('figproof_disclosed', [])
          if _q not in _ds_l['figproof_disclosed']:
              _ds_l['figproof_disclosed'].append(_q)           # AMBER line (chain_footer) — bounded, never a loop
          continue
      _ro[f'{_q}:figproof'] = int(_ro.get(f'{_q}:figproof') or 0) + 1
      _chs[_q] = bc.slot_chain_reopen(_c, _q, 'quality', _tgt_l.get(_q), (_cm_l.get(_q) or {}).get('subtopic_id'))
  # 3. SCHEDULE the next action of every open chain (bounded; never a stop)
  _progress, _pass3 = True, 0
  while _progress and _pass3 < 12:
    _progress, _pass3 = False, _pass3 + 1
    _work_qs = {w['q'] for w in _work}
    for _q, _c in sorted(_chs.items(), key=lambda kv: int(kv[0])):
        if _c.get('done') or _q in _work_qs or _q in _delta:
            continue
        _att = _c.get('attempts') or []
        if _att and _att[-1].get('outcome') == 'pending':
            if not _fresh(_q) or _c.get('kind') == 'dispute' or not _grades(_q)[0].get('grader_1'):
                _delta.add(_q)                                    # not yet reviewed / graded; a dispute: one agreement so far
                if _c.get('kind') == 'dispute':
                    _switch.add(_q)
            continue
        _nx = bc.slot_chain_next(_c, siblings=_siblings(_c.get('subtopic_id') or (_cm_l.get(_q) or {}).get('subtopic_id')))
        _c = _chs[_q] = _nx['chain']
        _a = _nx['action']
        _qt = str((_cm_l.get(_q) or {}).get('qtype') or 'mcq')
        _sid = (_cm_l.get(_q) or {}).get('subtopic_id')
        if _a in ('rework_dr1', 'rework_dr2', 'replace', 'shape', 'sibling'):
            _work.append({'q': _q, 'action': _a, 'sibling': _nx['sibling'], 'kind': _c['kind'],
                          'target': _c.get('target') or _tgt_l.get(_q), 'k': bc.k_candidates(bool(_att)),
                          'status': 'todo'})
        elif _a == 'adjudicate':
            _chs[_q] = bc.slot_chain_record(_c, 'adjudicate', 'pending')
            _delta.add(_q); _switch.add(_q)
        elif _a == 'reserve_refill':
            _excl = sorted(set().union(*[bc.op_key_ids(x) for x in _cm_l.values() if isinstance(x, dict)]))
            _rsv, _it, _why = bc.reserve_take(_rsv, _tgt_l.get(_q), _qt, _sid, None,
                                              ruler_version=_ruler_v, exclude_keys=_excl, labels=_labs_l)
            if _it is not None:
                _work.append({'q': _q, 'action': 'reserve_refill', 'kind': _c['kind'], 'target': _tgt_l.get(_q),
                              'item': _it, 'status': 'todo'})
            else:
                _chs[_q] = bc.slot_chain_record(_c, 'reserve_refill', 'fail', note=_why)
                _progress = True
        elif _a == 'refill_session':
            _act, _bs_l = bc.refill_session_next(_bs_l)
            if _act == 'refill':
                _work.append({'q': _q, 'action': 'refill_session', 'kind': _c['kind'], 'target': _tgt_l.get(_q),
                              'k': bc.C_REFILL_CANDIDATES, 'status': 'todo'})
            else:
                _chs[_q] = bc.slot_chain_record(_c, 'refill_session', 'fail', note='C_REFILL_SESSIONS used')
                _progress = True
        elif _a == 'last_resort':
            _excl_lr = sorted(set().union(*[bc.op_key_ids(x) for x in _cm_l.values() if isinstance(x, dict)]))
            _rsv, _it, _why = bc.reserve_take(_rsv, _tgt_l.get(_q), _qt, _sid, None, ruler_version=_ruler_v,
                                              exclude_keys=_excl_lr, nearest=True, labels=_labs_l)
            _own = None
            if _it is None and _c['kind'] == 'difficulty' and _unanimous(_q):
                _ctl, _pk = _grades(_q)
                _gb = _ctl.get('grader_1') if _ctl.get('grader_1') == _ctl.get('grader_2') else None
                _own = _gb if (_gb in _labs_l and _recipe_at(_q, _gb)) else None
            if _it is None and _own is None:
                _work.append({'q': _q, 'action': 'last_resort_generate', 'kind': _c['kind'], 'target': _tgt_l.get(_q),
                              'k': bc.C_REFILL_CANDIDATES, 'status': 'todo'})
                continue
            _dlv = _own if _own is not None else _it.get('difficulty')
            _inc = bc.last_resort_incident(EXAM, _bs_l.get('paper_id'), _q, _tgt_l.get(_q), _dlv,
                                           [a.get('stage') for a in (_c.get('attempts') or [])], _ruler_v, _today)
            _fin = bc.slot_chain_finish(_c, 'last_resort', delivered=_dlv, incident_id=_inc['incident_id'])
            if _it is not None:                                    # S13-2R inserts the reserve item, then this block re-bases it
                _work.append({'q': _q, 'action': 'last_resort_insert', 'kind': _c['kind'], 'target': _tgt_l.get(_q),
                              'item': _it, 'incident': _inc, 'status': 'todo'})
                _chs[_q] = dict(_c, awaiting='last_resort_insert')
                continue
            _ctl, _pk = _grades(_q)
            _ctl = dict(_ctl, recipe=_recipe_at(_q, _dlv))           # judged at the band it is DELIVERED at
            _ef, _okf, _whyf = bc.dl_set_label_basis_strict(_cm_l.get(_q), 'last_resort', _labs_l, _tgt_l.get(_q), _ctl, _pk,
                                                            chain=_fin, delivered=_dlv, incident_id=_inc['incident_id'])
            if _okf:
                _cm_l[_q], _chs[_q], _changed = _ef, _fin, True
                _cm_l[_q]['last_resort'] = {'requested': _tgt_l.get(_q), 'delivered': _dlv, 'incident_id': _inc['incident_id']}
                _incidents.append(_inc)
                _ls = _bs_l.setdefault('last_resort_slots', [])
                if _q not in [str(x.get('q')) for x in _ls if isinstance(x, dict)]:
                    _ls.append({'q': _q, 'requested': _tgt_l.get(_q), 'delivered': _dlv})
                _progress = True
            else:                                                  # unreachable on consistent records; generate instead
                _work.append({'q': _q, 'action': 'last_resort_generate', 'kind': _c['kind'], 'target': _tgt_l.get(_q),
                              'k': bc.C_REFILL_CANDIDATES, 'status': 'todo', 'why': _whyf})
        elif _a == 'abandon':
            _chs[_q] = bc.slot_chain_finish(_c, 'abandon')
            _progress = True
  # a chain may never be left open with nothing scheduled
  _idle = [q for q, c in _chs.items() if not c.get('done') and not c.get('awaiting')
           and q not in {w['q'] for w in _work} and q not in _delta]
  if _idle:                                                    # persist every decision taken so far, then re-enter
      _bs_l['slot_chain_work'] = _work
      json.dump(_rsv, open(_rsv_p, 'w', encoding='utf-8'), indent=2)
      json.dump(_kd_l, open(_key_l, 'w', encoding='utf-8'), indent=2)
      json.dump(_bs_l, open(_bsl_p, 'w', encoding='utf-8'), indent=2)
      raise RuntimeError(f"SLOT-CHAIN [HS:LADDER] (S13-2L): chains {sorted(_idle, key=int)} still open — run this block again.")
  # 4. REVIEW-COVERAGE-LAW — every item's latest review bound to its delivered text
  for _q in bc.review_coverage_missing(_cm_l, _hl):
      if _q not in _chs or _chs[_q].get('done'):
          _delta.add(_q)
  # 4b. v6.0 (A-REVIEW strict): a NOT_RUN review on the CURRENT text is not a review — it is re-queued at most twice
  #     per text, then the slot's QUALITY chain replaces the item (bounded; never a stop, never delivered unreviewed)
  _nr_l = _bs_l.setdefault('not_run_retries', {})
  for _q, _e in sorted(_cm_l.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0):
      _rv = (_e or {}).get('review') if isinstance(_e, dict) else None
      if not (isinstance(_rv, dict) and str(_rv.get('status') or '').upper() == 'NOT_RUN' and _hl.get(_q)
              and _rv.get('item_hash') == _hl.get(_q)):
          continue
      _k = f'{_q}:{_hl.get(_q)}'
      _c = _chs.get(_q)
      if _c and not _c.get('done'):
          continue
      _ro = _bs_l.setdefault('reopen_count', {})
      if int(_nr_l.get(_k) or 0) < 2:
          _nr_l[_k] = int(_nr_l.get(_k) or 0) + 1
          _delta.add(_q)
      elif int(_ro.get(f'{_q}:not_run') or 0) >= 2:           # replaced twice and still never reviewed: environment
          json.dump(_bs_l, open(_bsl_p, 'w', encoding='utf-8'), indent=2)
          raise RuntimeError(f"NO-MODEL [HS:ENV] (S13-2L): Q{_q}: the independent review returned NOT_RUN on every text "
                             f"(two replacements) — no reviewer context is available. State saved; restore sub-agents / "
                             f"Orchestrate workers and type continue.")
      elif not (_c and _c.get('done') and _c.get('outcome') == 'last_resort'):
          _ro[f'{_q}:not_run'] = int(_ro.get(f'{_q}:not_run') or 0) + 1
          _chs[_q] = bc.slot_chain_reopen(_c, _q, 'quality', _tgt_l.get(_q), (_e or {}).get('subtopic_id'))
          _nr_open = globals().setdefault('_NR_OPENED_L', set()); _nr_open.add(_q)
  _bs_l['slot_chain_work'] = _work
  _bs_l['delta_qs'] = sorted(_delta, key=int)
  _bs_l['delta_switch'] = sorted(_switch, key=int)
  _bs_l['delta_panel'] = []                                     # v6.0: no panel (LAW-ORG-7)
  # the SAME item builder audit_canonical A-DIFFGATE uses (an LB2 row counts at its label; a last resort is listed)
  G_PAPER = bc.difficulty_paper_gate(bc.dl_gate_items(_tgt_l, _cm_l, _labs_l), _labs_l) if _tgt_l else {'status': 'DORMANT'}
  if _tgt_l:
      _ds_l['paper_gate'] = dict({k: G_PAPER.get(k) for k in ('status', 'counts_final', 'counts_original', 'rework_qs',
                                                              'accepted_dr3', 'unmeasured', 'forced', 'swapped', 'rule',
                                                              'last_resort')},
                                 target_plan=dict(_tgt_l), labels=list(_labs_l))   # A-DIFFGATE re-counts from these
      if isinstance(_bs_l.get('schedule_frozen'), dict):
          _fzok, _fzbad = bc.schedule_frozen_check(_bs_l, {q: (e or {}).get('difficulty') for q, e in _cm_l.items()})
          _ds_l['paper_gate']['frozen_check'] = {'ok': _fzok, 'violations': _fzbad[:20]}
          if not _fzok:
              print(f"S13-2L: {len(_fzbad)} label(s) differ from the frozen schedule (open chains replace them): {_fzbad[:5]}")
  _ds_l['chain_footer'] = bc.chain_footer_lines(_chs)
  # v6.0 DeliveryFooter §LADDER-OP: the requested / applied schedule, the exam ruler, the normalisation notes, the
  # constant overrides and the organic parity — ONE source (chain_footer['info'], committed by S13-4 with
  # difficulty_state): Create S13-6 and MockDeliver 3f''' print it verbatim, nobody composes it twice
  _rq_l = _bs_l.get('schedule_requested') or {}
  _sa_l = _bs_l.get('schedule_applied') or {}
  _ru_l = _bs_l.get('exam_ruler') or globals().get('EXAM_RULER') or {}
  _op_info = []
  if _rq_l:
      _op_info.append('Requested difficulty: ' + ' / '.join(f'{_b} {_n}' for _b, _n in _rq_l.items()))
  if (_sa_l.get('counts') or {}) and dict(_sa_l['counts']) != dict(_rq_l):
      _op_info.append('Applied difficulty: ' + ' / '.join(f'{_b} {_n}' for _b, _n in _sa_l['counts'].items()))
  if _ru_l.get('ruler_version'):
      _op_info.append(f"Exam ruler {_ru_l.get('ruler_version')} ({_ru_l.get('basis')}): past distribution "
                      f"{_ru_l.get('past_distribution')}")
  _op_info += [f'Schedule as applied: {_n}' for _n in (_sa_l.get('notes') or [])]
  if _bs_l.get('op_overrides'):
      _op_info.append('Constant overrides: ' + ', '.join(_bs_l['op_overrides']))
  _pa_l = _ds_l.get('parity') if isinstance(_ds_l.get('parity'), dict) else None
  if _pa_l and _pa_l.get('status'):
      _op_info.append(f"Organic parity: {_pa_l['status']} — items with >= 2 decisions {float(_pa_l.get('chain_share') or 0):.0%}"
                      + (f"; short {_pa_l['short']}" if _pa_l.get('short') else ''))
  _ds_l['chain_footer'] = dict(_ds_l['chain_footer'], info=_op_info + list(_ds_l['chain_footer'].get('info') or []),
                               amber=list(_ds_l['chain_footer'].get('amber') or []) + [
                                   f"Q{_qd}: a structure figure has no proof record after two replacements — disclosed"
                                   for _qd in (_ds_l.get('figproof_disclosed') or [])] + [
                                   # v6.1 S0-BV BV-4: a question delivered at the band it measured after its one rewrite
                                   f"Difficulty after one rewrite: Q{_qb} delivered {_db.get('delivered')} (slot {_db.get('requested')})"
                                   for _qb, _db in sorted((_ds_l.get('bv_disclosed') or {}).items(), key=lambda kv: int(kv[0]))
                                   if isinstance(_db, dict)] + [
                                   # v6.1 S0-NF-9: every disclosed composition gate (DeliveryFooter §LADDER-NF)
                                   f"{_gn}: {_wn}" for _gn, _wn in sorted((_kd_l.get('nf_disclosed') or {}).items())] + (
                                   # v6.2 S0-BV BV-7: the anchor basis when the exam's past records carry no blind grades
                                   ["Difficulty anchors: the bands PYQExplain measured (no blind-graded past questions yet)"]
                                   if (globals().get('EXAM_RULER') or {}).get('anchor_basis') == 'pyq_explain_band' else []) + (
                                   # v6.3 S0-BV BV-10: questions whose band was judged, not computed from the reviewers' counts
                                   [f"Difficulty judged, not counted: Q{', Q'.join(_jq)}"]
                                   if (_jq := sorted((_q for _q, _e in _cm_l.items() if isinstance(_e, dict)
                                                      and ((_e.get('difficulty_check') or {}).get('measure') in ('judged', 'mixed'))),
                                                     key=lambda x: int(x) if str(x).isdigit() else 0)) else []))
  _ds_l['schedule'] = {'requested': _rq_l, 'applied': _sa_l}
  _ds_l['allocation_swaps'] = list(_bs_l.get('allocation_swaps') or [])
  if isinstance(globals().get('DIFFICULTY_STATE'), dict):      # the in-memory copy CHECK 3c writes from
      globals()['DIFFICULTY_STATE'].update({k: _ds_l[k] for k in ('paper_gate', 'chain_footer', 'incidents') if k in _ds_l})
  json.dump(_rsv, open(_rsv_p, 'w', encoding='utf-8'), indent=2)
  json.dump(_kd_l, open(_key_l, 'w', encoding='utf-8'), indent=2)
  json.dump(_bs_l, open(_bsl_p, 'w', encoding='utf-8'), indent=2)
  _nr_new = sorted(globals().pop('_NR_OPENED_L', set()), key=int)
  if _nr_new and not _work:                                    # a chain opened at step 4b is scheduled on re-entry
      raise RuntimeError(f"SLOT-CHAIN [HS:LADDER] (S13-2L): quality chain(s) {_nr_new} opened (review NOT_RUN twice) — "
                         f"run this block again.")
  if _work:
      raise RuntimeError(f"SLOT-CHAIN [HS:LADDER] (S13-2L): run S13-2R on batch_state['slot_chain_work'] "
                         f"{[(w['q'], w['action']) for w in _work]} NOW, then S13-2F (fresh sweep), then S13-2G phases 1-3 "
                         f"(a DELTA round with fresh grades), then this block again.")
  if _bs_l['delta_qs'] or _changed:
      raise RuntimeError(f"DELTA [HS:LADDER] (S13-2L): run S13-2F (fresh sweep{' — labels changed' if _changed else ''}), "
                         f"then S13-2G phases 1-3 over delta {_bs_l['delta_qs']} (skip S13-2G when it is empty), then this block again.")
  _bad_l = [q for q in sorted(_tgt_l, key=int) if not bc.verify_difficulty_label(_cm_l.get(q), _labs_l, strict=True)[0]]
  if _bad_l:                                                    # never reached on consistent records — re-enter, never ship
      raise RuntimeError(f"SLOT-CHAIN [HS:LADDER] (S13-2L): labels {_bad_l} do not verify strictly — run this block again.")
  print(f"S13-2L: paper difficulty gate {G_PAPER.get('status')} — delivered {G_PAPER.get('counts_final')} against "
        f"requested {G_PAPER.get('counts_original')}; last resort {G_PAPER.get('last_resort')}; every label measured_exact "
        f"or last_resort; every chain closed and every item covered. Continuing to S13-3 / S13-4.")
  ```

## S13-2R — SLOT CHAIN RUNNER (v6.0 — the actions S13-2L schedules; GAP-2026-11-10 G-10)

  For each entry of batch_state['slot_chain_work'] (in q order), perform its action IN THE FINAL DOCX
  through the S4-6 correction procedure (edit only that question's block, re-render its figures, update its
  sidecar entry and fig_manifest record, keep every other question byte-unchanged), keep the slot's KEY
  POSITION (K-BAL / K-PAT unchanged, E22), its section, its figural / text format (Axis 1, E17) and its
  stimulus group (a group member is replaced inside the group; two or more disputed members of one group
  -> the whole group is replaced and keeps its placement, E16). Every new item passes CHECK 3c, the S0-OP
  item controls and every batch gate against the WHOLE paper (entity, stem, media, PYQ distance, clone guard —
  a hit is a failed attempt, E21). EVERY action writes entry 'k' candidates in parallel (bc.k_candidates);
  the first candidate that passes EVERY control replaces the item; every other fully-passing candidate goes
  to the reserve (bc.reserve_add) — a candidate is never accepted on fewer controls.
    rework_dr1 / rework_dr2 — re-author at the slot's band (DR1: the NEXT pattern source — an organic item
      bc.l2_slot_source(..., skip = sources tried, min_decisions = the band recipe's minimum, chains =
      bc.chain_compose(...)); any other item the next exemplar of its cell; DR2: a band operator from the
      exam's recipe — add / remove a decision, a controlling stereocentre, ask for the starting material or
      A-and-B, tighten distractors to near-isomers — S0-OP-6). The grader's reason is the constraint.
    replace — a NEW item: same subtopic, band and ask shape, on a NEW substrate (next pattern source; a
      zero-PYQ subtopic: the library / a composed chain, never a single concept for a band needing >= 2
      decisions). None left -> set entry 'status' 'unavailable'.
    shape — same subtopic and band, another ask shape the subtopic carries (DIRECT first; a blueprint id
      missing from the manifest is treated as DIRECT-capable, E19) — ONLY a shape that keeps the paper's
      shape mix lawful: bc.shape_mix_check(<the paper's shape counts with this item moved>,
      bp['shape_target_per_paper'][str(N)], infeasible=<the plan's _infeasible>)['state'] != 'FAIL'. No such
      shape -> set entry 'status' 'unavailable'.
    sibling — same band, qtype and shape on the entry's 'sibling' subtopic, performed EXACTLY as §Q8b-LADDER R5
      REASSIGN (its candidate rule, the q_count amendment in the in-run blueprint, alloc_ids and
      subtopic_by_qnum, allocation_amendments[], persist_bp_amendment()); also recorded in
      batch_state['allocation_swaps'] as {'q', 'from', 'to'} (footer). A sibling that is NOT a REASSIGN
      candidate -> set entry 'status' 'unqualified' (skipped; it does not count toward the 3 siblings).
    reserve_refill / last_resort_insert — insert entry['item'] (a verified reserve item) at this slot; its
      key position is re-budgeted by K-BAL (the reserve item's options are re-ordered, never re-written);
      a reserve item flagged regrade_required is first re-graded by two fresh blind graders under the
      current ruler — if it no longer grades exactly at its band it is returned to the reserve and the
      entry is 'unavailable'.
    refill_session — Orchestrate O-REFILL: a FRESH worker resumes from saved state and writes entry['k']
      candidates for this slot (composer + library on). Without an orchestrator the same session writes them
      in its NEXT response (never more than one refill per response).
    last_resort_generate — a fresh worker writes entry['k'] candidates, nearest band to entry['target'] first,
      and keeps the first FULLY verified one (unanimous key, proven figures, original, both graders and the
      recipe exact at ITS band); S13-2L then records it as the last resort at that band.
  After EACH entry is written, set its 'status' ('done' | 'unavailable' | 'unqualified') in
  batch_state['slot_chain_work'], save batch_state, then run (resume-safe; an entry is recorded once):
  ```python
  # ── S13-2R record (v6.0) ──
  import json, os, blueprint_core as bc
  _bsr_p = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _kr_p = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  _bsr = json.load(open(_bsr_p, encoding='utf-8'))
  _kdr = json.load(open(_kr_p, encoding='utf-8'))
  _cmr = _kdr.setdefault('concept_map', {})
  for _w in _bsr.get('slot_chain_work') or []:
      _q, _st = str(_w['q']), _w.get('status')
      _c = (_bsr.get('slot_chain') or {}).get(_q)
      if _st in (None, 'todo', 'recorded') or not isinstance(_c, dict):
          continue
      if _st == 'unavailable':
          if isinstance(_w.get('item'), dict):
              # a reserve item that FAILED its use-time re-grade / clone guard is no longer verified: it is dropped
              # (never returned — a returned item would be taken again on the next pass)
              _w['item'] = None
          if _w['action'] in ('reserve_refill', 'refill_session'):
              _c = bc.slot_chain_record(_c, _w['action'], 'fail', note='unavailable')
          elif _w['action'] in ('last_resort_insert', 'last_resort_generate'):
              _c = dict(_c, awaiting=None)                      # S13-2L schedules the next last-resort round
          else:
              _c['unavailable'] = sorted(set(_c.get('unavailable') or []) | {_w['action']})
      elif _st == 'unqualified':                               # a sibling that is not an R5 REASSIGN candidate
          _c['skip_siblings'] = sorted(set(_c.get('skip_siblings') or []) | {str(_w.get('sibling'))})
      elif _w['action'] in ('last_resort_insert', 'last_resort_generate'):
          # the inserted / generated item is re-graded and re-reviewed; S13-2L records the last resort at the band
          # its fresh grades agree on (its chain's last-resort terminal stays the next action)
          _c = dict(_c, awaiting=None, done=False,
                    terminal_tried=[t for t in (_c.get('terminal_tried') or []) if t != 'last_resort'],
                    attempts=list(_c.get('attempts') or []) + [{'stage': 'last_resort', 'outcome': 'pending'}])
          _cmr[_q] = bc.clear_label_basis(_cmr.get(_q))
          _cmr[_q].pop('quality_status', None)
      else:                                                     # 'done' — a re-authored / refilled item: E10
          _c = bc.slot_chain_record(_c, _w['action'], 'pending', sibling=_w.get('sibling'))
          _cmr[_q] = bc.clear_label_basis(_cmr.get(_q))
          _cmr[_q].pop('quality_status', None)
          if _w['action'] == 'sibling':
              _bsr.setdefault('allocation_swaps', []).append({'q': _q, 'from': _c.get('subtopic_id'), 'to': _w.get('sibling')})
      _bsr['slot_chain'][_q] = _c
      _w['status'] = 'recorded'
  json.dump(_kdr, open(_kr_p, 'w', encoding='utf-8'), indent=2)
  json.dump(_bsr, open(_bsr_p, 'w', encoding='utf-8'), indent=2)
  ```
  When every entry is 'recorded': S13-2F (a fresh sweep of the changed docx), S13-2G phases 1-3 (a DELTA
  round with fresh grades), S13-2L. Every arrow is automatic and in the same response; the user types nothing.

## S13-3 — Post-mock concept audit (unchanged)

## S13-4 — Registry update protocol (v2.0 GAP-03 + GAP-04 fix; v5.53 — extracted to final_assembly.py)

  v5.53 (GAP-2026-08-12-FINAL-ASSEMBLY-ENGINE): S13-4's full registry-commit logic — first-mock
  field initialisation, the pending_registry merge, RC/DI/figural manifest writes, the
  FK-checked question_index build, and the mocks_completed/papers_completed/session_log/
  axis2_window ledgers — now lives in `final_assembly.commit_registry()`: routed, self-tested
  engine code, not spec prose a session had to re-type or re-derive every mock. Semantics are
  byte-faithful to the prior spec-inline logic (see that function's docstring for the 4
  disclosed, non-observable-on-a-healthy-commit deviations: pure/no-I/O, result-dict-not-raise,
  qindex_certify delegating to paper_pipeline.py, and 3 ledgers made properly idempotent).
  This closes Finding 0 of the Mock-10 root-cause gap analysis.

  ```python
  # v5.53: single explicit import for the extracted engine, alongside the existing os/json/glob.
  import os, json, glob
  import final_assembly as fa
  import blueprint_core as bc                              # v6.1: manifest_hash for the commit (S0-NF-0)

  # Load registry from working dir (not /mnt/project/):
  registry = json.load(open(f'/home/claude/{EXAM}_registry.json'))

  # Reload cross-batch data:
  prog = json.load(open(f'/home/claude/{EXAM}_M{N}_progress.json'))
  passage_linked_qs = set(prog.get('passage_linked_qs', []))
  cloze_linked_qs   = set(prog.get('cloze_linked_qs', []))
  # v5.53 GAP-2026-08-12-S13-4-UNDEFINED-BATCHES-COMPLETED (found + fixed during the final
  # 0-bug audit): the pre-extraction spec-inline code referenced a bare `batches_completed`
  # name here that was NEVER bound anywhere in this file — only `bs['batches_completed']`/
  # `batch_state['batches_completed']` (dict keys inside S3-16/S4-8a's own locals) exist.
  # That NameError was latent in EVERY release through v5.52.0; it went uncaught because
  # nothing in the verification chain executes this specific spec-inline block end-to-end
  # (Check AJ's undefined-name scan only covers the .py engine files, not .md inline code).
  # Fixed here, at the extraction boundary, by reloading batch_state.json fresh — the same
  # defensive-reload pattern already used for `prog`/`registry` above, rather than relying
  # on a per-batch local (`bs`) that may or may not still be bound this late in the session.
  _bs = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json'))
  batches_completed = len(_bs.get('batches_completed', []))

  # Per-Q concept_map the sidecar accumulated (S7-NEW-A) — fa.commit_registry uses this to
  # build question_index and to run the v5.48.0 FK check (COPY-BY-REFERENCE against the
  # blueprint's own subtopic_id strings).
  _akd = json.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json'))
  _cm = _akd.get('concept_map', {})
  # v5.59 — the WHOLE sidecar goes to commit_registry so it can write
  # registry.key_commitments[paper_id] (salted hashes; the plaintext `answers` never
  # enters the registry — fa.commit_registry's own self-test asserts that).

  # DI manifest (v5.42, GAP-2026-08-06-DI) — absent-safe: no di_present ⇒ no key ⇒ A-AXIS1
  # reports DI unestablished, as today.
  # v5.88 (LAW F3.1 MANIFEST-COMMIT-LAW): a manifest is committed because it EXISTS on disk
  # — the flag never gates it. final_assembly v1.10 records any flag/manifest disagreement
  # in registry.paper_flags[paper_id] (declared vs derived) and prints it once.
  _di_manifest = None
  if os.path.exists(f'/home/claude/{EXAM}_di_manifest.json'):
      _di_manifest = json.load(open(f'/home/claude/{EXAM}_di_manifest.json'))

  # Figural manifest + the FigureSpec sidecars (v5.34, GAP-2026-08-01-FIGSPEC-TRANSPORT D2),
  # keyed by the CANONICAL PNG name S10-8 stamps on the drawing.
  _fig_manifest, _figure_specs = None, None
  if os.path.exists(f'/home/claude/{EXAM}_fig_manifest.json'):
      _fig_manifest = json.load(open(f'/home/claude/{EXAM}_fig_manifest.json'))
      # Only THIS paper's sidecars (q<N>_*.figspec.json for N in the manifest) — a leftover
      # sidecar from an earlier paper in the same session is never attributed to this one.
      _figure_specs = {}
      for _fq in sorted(str(q) for q in (_fig_manifest.get('questions') or {})):
          for _fs in sorted(glob.glob(f'/home/claude/q{_fq}_*.figspec.json')):
              _figure_specs[os.path.basename(_fs)[:-len('.figspec.json')] + '.png'] = \
                  json.load(open(_fs, encoding='utf-8'))

  # v5.88 (LAW F1.4 — E3): a text_disclosed fallback subtopic renders TEXT; a figure
  # recorded against it is a dispatch error, and the auditor (v2.33) FAILs it. Stop HERE,
  # naming the questions, rather than committing a record S13-4c will reject.
  _fb_hit = sorted(str(q) for q, v in ((_fig_manifest or {}).get('questions') or {}).items()
                   if isinstance(v, dict) and v.get('subtopic_id') in (bp.get('figural_fallbacks') or {}))
  if _fb_hit:
      raise RuntimeError(f"LADDER-REPAIR R4 [HS:LADDER] (S13-4, LAW F1.4): question(s) {_fb_hit} carry a figure on a "
                       f"text_disclosed fallback subtopic (blueprint.figural_fallbacks) — such a "
                       f"subtopic renders TEXT (S3-17c FORMAT_OVERRIDE). Re-author them as TEXT "
                       f"(S7-NEW-B OPTION B) and remove their fig_manifest entries, then re-run "
                       f"S13-1, S13-2F (a new certificate) and S13-4 — never S13-4 alone.")

  # C2: re-derive identity here (self-contained — bp + N are session-level, always in scope).
  _tp = next((mk for mk in bp.get('mocks', []) if mk.get('mock') == N), None)
  paper_id = (_tp or {}).get('paper_id', f"MOCK:M{N:02d}")

  # v5.54 (GAP-2026-08-12-AXISPAPER-PERSISTENCE): the S7-AXIS per-section snapshot
  # accumulators are threaded into the terminal commit here — commit_registry persists
  # them as reg['axis1_paper'][paper_id] / reg['axis3_paper'][paper_id] (v5.68; the
  # legacy [str(N)] key is also written for the MOCK series only — replace-by-paper,
  # idempotent). Read via globals().get, NOT bare names: on an exam whose blueprint
  # declares no axis feature the S7-AXIS block never runs, so the accumulators are
  # legitimately unbound here — that must mean "nothing to persist", never a NameError
  # (the batches_completed lesson, applied at authoring time instead of learned again).
  _ax1 = globals().get('axis1_paper_counts') or {}
  _ax3 = globals().get('axis3_paper_counts') or {}

  _s13_preview = bool(globals().get('S13_PREVIEW'))      # v5.89: S13-2F step 1 sets it
  globals()['S13_PREVIEW'] = False                        # consumed: a later real S13-4 commits
  _s13_preview_path = f'/home/claude/{EXAM}_M{N}_registry_preview.json'
  try:
    _commit = fa.commit_registry(
      registry, pending_registry, bp, N,
      paper_id=paper_id, batches_completed=batches_completed,
      axis2_window_counts=axis2_window_counts,
      # v5.88: the DECLARED blueprint values go here (registry.paper_flags keeps declared
      # beside derived); the session-corrected S3-2a values decide nothing at commit.
      passage_present=DECLARED_FLAGS['passage_present'], di_present=DECLARED_FLAGS['di_present'],
      figural_present=DECLARED_FLAGS['figural_present'],
      concept_map=_cm, passage_linked_qs=passage_linked_qs, cloze_linked_qs=cloze_linked_qs,
      di_manifest=_di_manifest, fig_manifest=_fig_manifest, figure_specs=_figure_specs,
      axis1_snapshots=_ax1, axis3_snapshots=_ax3,
      answer_key=_akd,                      # v5.59 — key commitments (S13-4 / Explain §7-8)
      quality_readiness=_bs.get('quality_readiness'),   # v5.90 — S3-2e record -> A-READINESS / footer
      difficulty_state=_bs.get('difficulty_state'),     # v5.92 — Part D record -> MockDeliver 3f' lines
      shape_infeasible=list((_bs.get('shape_plan') or {}).get('_infeasible') or []),   # v5.90 — S3-12d planner record -> A-SHAPEMIX
      nf_disclosed=(_akd.get('nf_disclosed') if isinstance(_akd, dict) else None),     # v6.1 S0-NF-9 -> footer / MockDeliver
      manifest_hash=bc.manifest_hash(globals().get('manifest') or {}))                 # v6.1 S0-NF-0 (F-08)
  except ValueError as _e_commit:
      # LAW F2.3: a figure record without object_type (or another per-question record
      # defect) raises inside commit_registry — an ITEM defect, repaired via the ladder.
      if _s13_preview:
          raise RuntimeError(f"LADDER-REPAIR R1 [HS:LADDER] (S13-4 preview): {_e_commit} — "
                             f"complete the named figure record(s) (fig_manifest object_type / "
                             f"figspec sidecar), then run the next S13-2F sweep (step 1 preview "
                             f"with S13_PREVIEW = True, then the S13-2F block).")
      raise SystemExit(f"HARD STOP [HS:INFRA] (S13-4): {_e_commit} — the S13-2F preview of this "
                       f"same commit passed, so the inputs changed after certification. "
                       f"Re-run S13-2F.")
  if not _commit['ok']:
      if _s13_preview:
          # S13-2F preview: an FK failure is an ITEM defect (a concept_map subtopic_id
          # not in this blueprint) — repaired through the ladder, never a stop.
          # v5.90 (OD-13 i): a G-MEDIAREUSE refusal (final_assembly v1.12 — one media part
          # under two questions) arrives here in the same shape; its message names the
          # LATER item and its rung (R2). Same handling: repair, next sweep.
          raise RuntimeError(f"LADDER-REPAIR R2 [HS:LADDER] (S13-4 preview): {_commit['fails']} — "
                             f"re-author the named question(s) on a blueprint subtopic, then run "
                             f"the next S13-2F sweep (step 1 preview with S13_PREVIEW = True, then "
                             f"the S13-2F block).")
      raise SystemExit(f"HARD STOP [HS:INFRA] (S13-4): {_commit['fails'][0]} — the S13-2F "
                       f"preview of this same commit passed, so the inputs changed after "
                       f"certification. Re-run S13-2F.")
  registry = _commit['registry']
  paper_id = _commit['paper_id']
  # ── S13-4OP (v6.0) — inside S13-4, right after `registry = _commit['registry']; paper_id = _commit['paper_id']` ──
  import json, os, blueprint_core as bc
  _reg4 = globals()['registry']                                # S13-4's committed registry (written to disk after this)
  _rsv4_p = f'/home/claude/{EXAM}_reserve.json'
  _ser4_p = f'/home/claude/{EXAM}_series_registry.json'
  _bs4 = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
  if os.path.exists(_rsv4_p):
      _reg4['reserve'] = json.load(open(_rsv4_p, encoding='utf-8'))
  _km4 = json.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json', encoding='utf-8')).get('concept_map') or {}
  # v6.1 (S0-NF-5): organic structure rows AND a text fingerprint for EVERY item of every subject
  _reg4['series_registry'] = bc.nf_series_registry_add(
      json.load(open(_ser4_p, encoding='utf-8')) if os.path.exists(_ser4_p) else (_reg4.get('series_registry') or {'papers': {}}),
      globals()['paper_id'],
      [dict(_e, q=_q) for _q, _e in _km4.items() if isinstance(_e, dict)])
  if not globals().get('_s13_preview'):                         # a preview commit never touches the series file
      json.dump(_reg4['series_registry'], open(_ser4_p, 'w', encoding='utf-8'), indent=2)   # the next paper sees it
  _ru4 = globals().get('EXAM_RULER') or _bs4.get('exam_ruler')  # resume-safe (S3-16 persisted it)
  if isinstance(_ru4, dict):
      _reg4['difficulty_ruler'] = _ru4
  _op_base4 = f'/mnt/project/{EXAM}_difficulty_profile.json'
  _op_work4 = f'/home/claude/{EXAM}_op_profile.json'
  _reg4['pyq_backfill'] = dict(_reg4.get('pyq_backfill') or {}, **bc.profile_backfill_delta(
      json.load(open(_op_work4, encoding='utf-8')) if os.path.exists(_op_work4) else {'papers': {}},
      json.load(open(_op_base4, encoding='utf-8')) if os.path.exists(_op_base4) else {'papers': {}}))
  # v5.94 (GAP-2026-11-07; owner Q1 (c)): the Step-5 blind grades of THIS profile (S3-8L, fresh bank
  # only) are cached against the profile's sha256 — a later paper whose bank is not attached reuses
  # them (bc.pyq_grades_from_registry); a cache for another profile version is never read.
  _pgr = globals().get('L2_PYQ_GRADES_RECORD')
  if isinstance(_pgr, dict) and _pgr.get('usable') and _pgr.get('profile_sha256'):
      registry.setdefault('pyq_grades', {})[_pgr['profile_sha256']] = _pgr

  # v5.52 (GAP-2026-08-12-S13-COMMIT-COMPLETE) — ATOMICITY MANDATE: fa.commit_registry() is
  # PURE (accumulates every field into a NEW in-memory dict, mutates nothing) — this remains
  # the single terminal write to registry.json for this mock's S13-4 commit. There must be NO
  # other json.dump of registry.json anywhere else in this block: an FK failure returns
  # {'ok': False, 'registry': <the ORIGINAL, unmodified registry>} instead of raising mid-write,
  # so registry.json on disk is COMPLETELY UNTOUCHED on failure — never partially written.
  # G-COMMIT-COMPLETE (S13-REGCHECK) is the downstream detector if this rule is ever violated
  # by a future edit; this comment is the upstream prevention.
  if _s13_preview:
      # v5.89 S13-2F PREVIEW (GAP-2026-11-02 G1). commit_registry is PURE: the same commit,
      # plus the S13-REGCHECK self-heal, is written ONLY to the preview file, so the
      # pre-commit sweep audits against exactly the registry S13-4 will commit. Nothing is
      # persisted: registry.json and every ledger are untouched, `registry` is reloaded.
      _rcp = fa.regcheck(registry, bp, N=N, concept_map=_cm,
                         msq_meta=_akd.get('msq_meta', {}), paper_id=paper_id,
                         require_key_commitments=True)
      json.dump(_rcp['registry'] if _rcp.get('ok') else registry,
                open(_s13_preview_path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
      registry = json.load(open(f'/home/claude/{EXAM}_registry.json'))
      print(f"S13-4 PREVIEW: {_s13_preview_path} written — nothing committed.")
  else:
      json.dump(registry, open(f'/home/claude/{EXAM}_registry.json', 'w'),
                indent=2, ensure_ascii=False)
  ```

## S13-REGCHECK — Registry schema-completeness gate (v3.5 — runs after S13-4 commit; v5.53 — extracted)

  Runs immediately after the S13-4 commit writes registry.json, BEFORE S13-5.
  Sets REGCHECK_OK (read by S13-7). This gate does NOT trust the Step-1 template
  — it enforces the v2.0 schema regardless of what the template provided, so a
  drifted template can never silently ship an incomplete registry (the M1-D13
  failure mode). It is idempotent and safe to re-run.

  v5.53: the schema self-heal and the v5.52 G-COMMIT-COMPLETE cross-ledger check (S13-4's
  three ledgers — mocks_completed/papers_completed, session_log, question_index — can drift
  apart if a session ever hand-rolls or partially re-derives S13-4) now live in
  `final_assembly.regcheck()`. THIS mock's own commit is a HARD STOP [HS:INFRA] if incomplete; a
  PRE-EXISTING partial commit from an earlier mock is a WARN, not a hard stop — same trigger
  conditions, same wording, as before extraction.

  ```python
  registry = json.load(open(f'/home/claude/{EXAM}_registry.json'))

  # v4.7 (ND6 — MANDATORY): options_by_q needs the mock's concept_map + msq_meta. Same
  # try/except fallback as before extraction — regcheck() no longer reads the sidecar itself
  # (it's pure), so the caller supplies it.
  _akp = f'/home/claude/{EXAM}_M{N}_answer_key.json'
  try:
      _kd = json.load(open(_akp))
      _km = _kd.get("concept_map", {})
      _msq_meta = _kd.get("msq_meta", {})
  except Exception:
      _km, _msq_meta = {}, {}

  _rc = fa.regcheck(registry, bp, N=N, concept_map=_km, msq_meta=_msq_meta,
                    paper_id=paper_id, require_key_commitments=True)   # v5.59 G-KEYCOMMIT
  if not _rc['ok']:
      raise SystemExit(_rc['fails'][0])
  registry = _rc['registry']
  # v5.88 (GAP-2026-11-01 §6 migration, forward-only): figure records committed before
  # LAW F2/F3 are ANNOTATED — label/kind mismatch, REACTION without '>>', a completed paper
  # with FIGURAL>0 and no record — never rewritten, never deleted. A-FIGTYPE-KIND skips an
  # annotated question with a printed reason; the Deliver footer discloses each (§FOOTER-FT).
  # ONLY UNSTAMPED entries are touched: S13-4 (final_assembly v1.10) stamps every record it
  # writes with record_schema='F2', and the migration skips stamped entries — so the paper
  # committed a moment ago is AUDITED by S13-4c, never annotated into "legacy" (a stamped
  # entry carrying an annotation is itself an A-FIGTYPE-KIND FAIL).
  import figure_types as _ft_mig
  registry, _mig_notes = fa.annotate_legacy_figure_records(
      registry, kind_of=lambda ot: _ft_mig.lookup(ot)['semantic_kinds']
      if _ft_mig.lookup(ot)['status'] != 'unregistered' else None)
  for _n in _mig_notes:
      print(f"S13-REGCHECK legacy figure record annotated: {_n}")
  if _rc['healed']:
      print(f"S13-REGCHECK: healed drifted template — added "
            f"{_rc['healed']}. Registry now schema-complete.")
  if _rc['warnings']:
      print("S13-REGCHECK WARNING (G-COMMIT-COMPLETE): pre-existing partial registry "
            "commit(s) found from an earlier mock/session — "
            + "; ".join(_rc['warnings'])
            + ". Not blocking (historical — may predate this gate), but should be "
              "repaired: re-run S13-4's full commit block for the affected mock(s), "
              "or record the gap explicitly rather than leaving it silently "
              "inconsistent.")

  # Persist healed registry to BOTH working dir and outputs:
  json.dump(registry, open(f'/home/claude/{EXAM}_registry.json', 'w'),
            indent=2, ensure_ascii=False)
  os.makedirs('/mnt/user-data/outputs', exist_ok=True)
  json.dump(registry, open(f'/mnt/user-data/outputs/{EXAM}_registry.json', 'w'),
            indent=2, ensure_ascii=False)

  REGCHECK_OK = True
  print("S13-REGCHECK: registry schema complete. OK.")
  ```

## S13-QINDEX — Question-index gate execution (v5.2 — G-QINDEX; runs after S13-REGCHECK; v5.53 — extracted)

  Runs immediately after S13-REGCHECK, BEFORE S13-5/S13-7. Certifies the mock-N
  question_index this session built (S13-4). Sets QINDEX_OK (read by S13-7). Executable
  home of gate G-QINDEX (definition in §12 S12-NEW-26). Governed by
  Contract_QuestionMetadataIndex v1.0; the six checks were proven in the Phase-1 harness.

  v5.48.0 — G-QINDEX now has an ENGINE-ENFORCED TWIN: gate A-QINDEX in
  audit_canonical.py, armed at the S13-4c re-sweep via --registry/--blueprint/--mockN.
  G-QINDEX remains the in-session early check (cheapest place to catch a capture bug);
  A-QINDEX is the enforcement of record, because its verdict is an exit code the
  session cannot paraphrase — the reference corpus proved sessions can skip or mistype
  inline gates while logging a clean audit. Both must pass; neither replaces the other.
  v5.49.0 (GAP-2026-08-12-QINDEX-QUOTA-ENFORCEMENT) — A-QINDEX's twin coverage now
  extends to ALL SIX checks, not five: check 6 (the exact difficulty_schedule[N]
  quota) was the one check v5.48.0 left engine-unenforced, and it was the
  literal check that would have caught a mock whose difficulties shipped null — a
  session that never runs S13-QINDEX at all (not merely mistypes it) now still gets
  caught at the S13-4c re-sweep, on check 6, the same as any other G-QINDEX check.

  v5.53: `final_assembly.qindex_certify()` delegates to paper_pipeline.py's pre-existing
  `validate_question_index()`, which is logically identical to G-QINDEX/1-6 and was already
  parity-tested against audit_canonical.py's gate_qindex() (that module's own "QINDEX PARITY"
  self-test) — reusing it collapses what would otherwise be a fifth independent copy of the
  same six checks. One disclosed, non-observable-here behaviour change: check 6 is DORMANT
  (not a false HARD STOP [HS:PROSE]) when an exam's blueprint declares no difficulty_schedule at all;
  IIT_JAM_BIOTECHNOLOGY always declares one, so nothing changes for this exam.

  ```python
  import json, os, blueprint_core as bc, final_assembly as fa
  _qi = fa.qindex_certify(registry, bp, N)
  # v5.96 (OD-2026-11-09): check 6 counts every row at its recorded basis (pp.qindex_count_band), so a
  # forced label or a band swap never fails it; a FAIL the S13-2F sweep escalated to AMBER stays AMBER here,
  # and any other FAIL is self-healed (rebuild question_index at S13-4, re-run) before it may stop
  _bsq_p = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _bsq = json.load(open(_bsq_p, encoding='utf-8')) if os.path.exists(_bsq_p) else {}
  if not _qi['ok'] and 'A-QINDEX' in ((_bsq.get('escalated_paper') or {}).get('gates') or []):
      print("G-QINDEX: AMBER — ESCALATED at S13-2F (OD-2026-11-09): " + "; ".join(_qi['fails']))
      _qi = dict(_qi, ok=True)
  if not _qi['ok']:
      _act_q, _bsq['infra_heal'], _n_q = bc.infra_heal_step(_bsq.get('infra_heal'), 'S13-QINDEX')
      json.dump(_bsq, open(_bsq_p, 'w', encoding='utf-8'), indent=2)
      _msg_q = ("HARD STOP [HS:INFRA] (G-QINDEX): " + "; ".join(_qi['fails'])
                + ". Fix the per-Q subtopic_id/difficulty capture (S7-NEW-A) or the "
                + "schedule-first assignment, rebuild question_index (S13-4), re-run.")
      if _act_q == 'heal':
          raise RuntimeError(f"INFRA-HEAL [HS:LADDER] S13-QINDEX (attempt {_n_q}/{bc.INFRA_HEAL_MAX}): perform the "
                             f"repair named below NOW, automatically, then re-run — {_msg_q}")
      raise SystemExit(_msg_q)
  QINDEX_OK = True
  print(f"G-QINDEX: question_index certified for mock {N} — OK.")
  ```


## S13-4b — TIER-A AUDIT DOSSIER (v5.35; consumer restated v5.36) — DELIVERED AS RECORD

  WHY. Step 7 already records every fact below. §S7-NEW-A even states of concept_map:
  "The audit gates read it directly instead of re-deriving." But S0-1 never delivered
  it, so the audit re-derived what Step 7 had written down — and two gates paid for it:
  A-NAT-GRADE ran dormant on ~200 exams, and image_role defaulted for every question,
  false-flagging 27 of 33 figural blocks on the reference paper (7 with the dossier).

  THE LINE, AND IT IS NOT NEGOTIABLE:
    HAND OVER FACTS STEP 7 RECORDED. NEVER HAND OVER JUDGMENTS STEP 7 REACHED.
  Facts are checkable against the artefact or the world. Judgments — the answer,
  answer_verified, "these options are unambiguous" — are formed by the reader of this
  dossier, and they NEVER travel here. Any consumer's load_dossier() REFUSES the file
  outright if it carries answers/answer_verified/derived_answer, so a leak cannot pass
  unnoticed. v5.36: with the audit steps retired the dossier's consumer is the AUTHOR (and
  any future auditor). It is still written — it is now the only structured record of what
  Step 7 believed it produced.

  ```python
  import os, json, hashlib
  _ak = json.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json', encoding='utf-8'))
  _cm = _ak.get('concept_map', {})
  # v5.54 (GAP-2026-08-12-S13-4B-SCOPED-PATH): the docx path is derived from
  # pp.paper_slug(paper_id) — THE one filename-stem rule — never hand-built. The old
  # old literal (Mock-then-bare-N name) was DOUBLY wrong: paper_slug zero-pads
  # ("Mock03", so the literal missed EVERY single-digit mock's actual file), and a
  # scoped paper's slug ("SUBJ_Physics_01") never matched at all — the md5 binding
  # below then FileNotFoundError'd instead of binding the dossier to its paper.
  # (The DOSSIER's own name keeps its M{N} form: writer, S13-4c reader and
  # audit_canonical --dossier help all agree on it. v5.73: it lives in /home/claude —
  # INTERNAL, never staged in outputs, never delivered.)
  _docx = f'/mnt/user-data/outputs/{EXAM}_{pp.paper_slug(paper_id)}_Create.docx'
  _FACTS = ('subtopic_id', 'qtype', 'image_role', 'difficulty', 'stem_precision',
            'nat_grading_type', 'nat_grading_value', 'ca_range',
            'msq_instr_in_stem', 'nat_instr_in_stem')
  dossier = {
      'schema': 1,
      'exam_code': EXAM,
      'mock': N,
      # The binding. Without it a dossier could be restored onto ANOTHER paper and
      # a reader would audit against facts describing a different document.
      'paper_md5': hashlib.md5(open(_docx, 'rb').read()).hexdigest(),
      'created_utc': __import__('datetime').datetime.now(
          __import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
      'questions': {str(q): {k: e.get(k) for k in _FACTS if k in e}
                    for q, e in _cm.items()},
  }
  # Belt and braces: never emit a judgment even by accident.
  assert not ({'answers', 'answer_verified', 'derived_answer'} & set(dossier)), \
      'TIER A carries FACTS only'
  _out = f'/home/claude/{EXAM}_M{N}_audit_dossier.json'   # v5.73 — INTERNAL path
  json.dump(dossier, open(_out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
  ```

  INTERNAL (v5.73, operator decision 2026-08-26 — was "DELIVERED alongside the paper"
  from v5.35 to v5.72). Written to /home/claude, read by the S13-4c re-sweep in the same
  session, NEVER copied to /mnt/user-data/outputs and NEVER passed to present_files.
  It is INERT for every downstream step (Steps 9 and 11 neither read nor require it)
  and absent-safe: a pre-v5.35 paper simply has none.

## S13-4c — DOSSIER-FED RE-SWEEP (v5.40 — the wiring, restored)

  THE DEFECT THIS REPAIRS. Through v5.35 the dossier crossed a step boundary: Step 7
  wrote it, Step 8 staged it and passed `--dossier` to the auditor, and A-NAT-GRADE +
  A-FIGPROFILE read recorded FACTS instead of re-deriving them. When Step 8 was retired
  in 2026.08.03.5 the writer stayed and the reader vanished. No invocation anywhere passed
  the flag, so the dossier became a file written for nobody — the exact producer-written /
  consumer-written / nobody-wiring-them defect the dossier itself was built to repair,
  reintroduced one layer up. CHECK AM in validate_framework_md.py existed to catch this and
  could not, because its contract named the deleted spec and it skipped silently.

  WHY IT CANNOT LIVE IN S13-2. The Final-Assembly sweep runs BEFORE S13-4b writes the
  dossier, so the file does not exist yet at that point. Ordering makes S13-2 impossible.

  THE RULE. Immediately after S13-4b writes the dossier, and ONLY when AUDIT_AVAILABLE,
  re-run the auditor once over the final docx WITH the flag. The effective command is:

  ```
  python3 /home/claude/[ExamCode]_mock_test_audit.py \
      /mnt/user-data/outputs/[ExamCode]_[paper_slug]_Create.docx \
      --dossier /home/claude/[ExamCode]_M[N]_audit_dossier.json \
      --registry /home/claude/[ExamCode]_registry.json \
      --blueprint [BP_SRC_PATH] \
      --rules /mnt/project/[ExamCode]_section_rules.md \
      --manifest /mnt/project/[ExamCode]_subtopic_manifest.json \
      --stimulus-profile /home/claude/[ExamCode]_M[N]_stimulus_profile.json \
      --mockN [N]
  ```
  ([paper_slug] = pp.paper_slug(paper_id) — "Mock01" for a mock, "SUBJ_Physics_01" for a
  scoped paper; v5.54, GAP-2026-08-12-S13-4B-SCOPED-PATH. The executed block below uses
  `_docx` carried from S13-4b, which is already slug-derived.)

  Executed as:

  ```python
  _cert = f'/home/claude/{EXAM}_M{N}_item_sweep_certificate.json'   # v5.89 (S13-2F)
  import json, os, blueprint_core as bc
  _bs4c_p = f'/home/claude/{EXAM}_M{N}_batch_state.json'
  _bs4c = json.load(open(_bs4c_p, encoding='utf-8')) if os.path.exists(_bs4c_p) else {}
  _esc4c = _bs4c.get('escalated_paper') or {}
  def _infra4c(site, msg):
      # v5.96 (OD-2026-11-09): every S13-4c stop names its own repair — perform it automatically and re-run
      # this block; only after bc.INFRA_HEAL_MAX heals of the same site may it end the response
      _b = json.load(open(_bs4c_p, encoding='utf-8')) if os.path.exists(_bs4c_p) else {}
      _act, _b['infra_heal'], _n = bc.infra_heal_step(_b.get('infra_heal'), site)
      json.dump(_b, open(_bs4c_p, 'w', encoding='utf-8'), indent=2)
      if _act == 'heal':
          raise RuntimeError(f"INFRA-HEAL [HS:LADDER] {site} (attempt {_n}/{bc.INFRA_HEAL_MAX}): perform the repair "
                             f"named below NOW, automatically, then re-run this block — {msg}")
      raise SystemExit(msg)                      # the tool is still broken after INFRA_HEAL_MAX heals
  # v5.90/v5.91: a RESUMED response (S4-12, after an interruption) may not have run S13-2F in
  # this turn — CERT,
  # AMBER_NOTES and UNCERTIFIED_ITEMS (DeliveryFooter §LADDER lines) are re-read from the
  # certificate file and batch_state, the artefacts the stamps live in.
  CERT = json.load(open(_cert, encoding='utf-8')) if os.path.exists(_cert) else None
  AMBER_NOTES = list((CERT or {}).get('amber_notes') or [])
  UNCERTIFIED_ITEMS = list((json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
                            if os.path.exists(f'/home/claude/{EXAM}_M{N}_batch_state.json') else {}).get('uncertified_items')
                           or (CERT or {}).get('uncertified_items') or [])
  _pf = f'/mnt/project/{EXAM}_difficulty_profile.json'
  if AUDIT_AVAILABLE and os.path.exists(_out):
      # v5.85: the paper's OWN profile snapshot (S3-12b) — absent on a legacy paper
      _sgp_final = STIM_PROFILE_PATH if os.path.exists(STIM_PROFILE_PATH) else None
      _r = subprocess.run(
          ['python3', f'/home/claude/{EXAM}_mock_test_audit.py',
           _docx, '--dossier', _out,
           # v5.48.0 — arm A-QINDEX: engine-enforced FK certification of the
           # question_index this session just committed (S13-4). The exit code
           # below is the durably-logged verdict; a bad index can no longer
           # coexist with a clean audit log.
           '--registry', f'/home/claude/{EXAM}_registry.json',
           # v5.86: the blueprint THIS paper was built from (S3-2) — never the mock
           # blueprint for a scoped paper (A-COUNT / A-QINDEX / A-DGATE read its size).
           '--blueprint', BP_SRC_PATH,
           # v5.77 — arm A-CLUSTER at FULL strength: without --rules/--manifest
           # the gate has no concept_group/family metadata and degrades to
           # subtopic-level adjacency only (safe, but weaker than the S3-12b
           # pre-flight it is supposed to mirror at ship time).
           '--rules', f'/mnt/project/{EXAM}_section_rules.md',
           '--manifest', f'/mnt/project/{EXAM}_subtopic_manifest.json',
           # v5.85 — arm A-BLOCK: the auditor recomputes the stimulus groups
           # from the SAME profile the planner used and certifies the paper.
           *(['--stimulus-profile', _sgp_final] if _sgp_final else []),
           # v5.89 (GAP-2026-11-02 G1): the S13-2F certificate — A-CERT confirms the
           # docx is the one certified; --profile arms A-DPROFILE / A-DIFFSRC.
           '--certificate', _cert,   # ALWAYS: a skipped / lost S13-2F FAILs A-CERT (INFRA)
           *(['--profile', _pf] if os.path.exists(_pf) else []),
           # v5.90: the SAME per-item inputs S13-2F audited with — the sidecar (quality
           # records, review, stamps) and the figure manifest — so the final sweep is the
           # certified sweep re-run on the committed registry, not a weaker one. The
           # auditor also overlays the registry's committed V590 fields, so a missing
           # sidecar (a resumed session) still audits every item.
           *(['--key', f'/home/claude/{EXAM}_M{N}_answer_key.json']
             if os.path.exists(f'/home/claude/{EXAM}_M{N}_answer_key.json') else []),
           *(['--fig-manifest', f'/home/claude/{EXAM}_fig_manifest.json']
             if os.path.exists(f'/home/claude/{EXAM}_fig_manifest.json') else []),
           *(['--style-profile', f'/mnt/project/{EXAM}_style_profile.json']
             if os.path.exists(f'/mnt/project/{EXAM}_style_profile.json') else []),   # A-ITEMRULE suspension (R7.2)
           '--mockN', str(N),
           # v5.96: the paper-level gates S13-2F escalated to AMBER at its sweep cap (the same verdict)
           *(['--escalate-paper', ','.join(_esc4c['gates']), '--sweep', str(_esc4c.get('sweep'))]
             if _esc4c.get('gates') else [])],
          capture_output=True, text=True, env=AUDIT_ENV)        # S3-9: engines importable
      print(_r.stdout)          # real STDOUT — never a paraphrase (B-7)
      if _r.returncode != 0:
          # v5.89: S13-2F certified this docx against the PREVIEW of this very commit
          # with every gate (no FAIL line of any gate), and AMBER advisories are WARN
          # lines (no exit 1). v5.96 (OD-2026-11-09): a finding that sits ONLY on DISCLOSED items
          # (exhausted chains) is reconciled by the auditor to an AMBER WARN line (a legacy
          # UNRESOLVED stamp likewise) — it never exits 1 either. A non-zero exit
          # here therefore means the committed record differs from its preview, or the
          # docx changed after certification (A-CERT) — INFRASTRUCTURE, never a
          # question-quality matter.
          _infra4c('S13-4c-2',
              "HARD STOP [HS:INFRA] (S13-4c re-sweep, v5.89): the committed paper fails a gate "
              "its S13-2F preview passed (or A-CERT: the docx changed after certification) — "
              "see STDOUT above. The registry is committed: restore "
              "/home/claude/[ExamCode]_registry.json from REG_SRC['path'] (the registry this "
              "run started from, S3-1), then re-run S13-2F, "
              "S13-4 and this re-sweep. present_files is forbidden until clean (B-7).")
      # STALE-COPY TRIPWIRE. [ExamCode]_mock_test_audit.py is a Step-6-delivered
      # copy in the PROJECT — a push to production does NOT refresh it. A pre-
      # v5.48 copy already accepts --registry/--blueprint/--mockN (they predate
      # this release), so it consumes all three flags, emits NO A-QINDEX line,
      # and exits 0. The returncode check above then reads as a clean FK
      # certification for a gate that never ran — the exact silent-enforcement
      # shape this release exists to close, one level up. The gate is REQUIRED
      # to print a line in both states (armed verdict or 'dormant'), so its
      # ABSENCE is unambiguous evidence of a stale copy, never of a pass.
      if 'A-QINDEX' not in (_r.stdout or ''):
          _infra4c('S13-4c-3',
              f"HARD STOP [HS:INFRA] (S13-4c, v5.48.0): {EXAM}_mock_test_audit.py printed no "
              "A-QINDEX line, so it predates the FK gate and the question_index "
              "was NOT certified — a clean exit code here would be meaningless. "
              "Refresh the per-exam auditor (re-run Step 6 B3, or replace the "
              "project file with the current repo audit_canonical.py verbatim "
              "under the same [ExamCode]_ name), then re-run. present_files is "
              "forbidden until clean (B-7).")
      # v5.86 (GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC): at S13-4c this paper IS
      # committed, so A-QINDEX must come back ARMED. Auditor v2.31 reports it 'dormant'
      # only for a paper that is not yet in the registry's commit ledgers (the final
      # batch's STEP B, before S13-4) — here that would mean S13-4 never committed it.
      if any(re.search(r'\]\s+A-QINDEX\s+dormant\b', l)
             for l in (_r.stdout or '').splitlines()):
          _infra4c('S13-4c-4',
              f"HARD STOP [HS:INFRA] (S13-4c, v5.86): A-QINDEX reported dormant — this paper is not "
              f"in the registry's commit ledgers, so S13-4 did not commit it. Re-run S13-4 "
              f"in FULL, then S13-REGCHECK, S13-QINDEX and this re-sweep. present_files is "
              f"forbidden until clean (B-7).")
      # v5.88 FIGURE-RECORD TRIPWIRE (GAP-2026-11-01, LAW F3.3), same shape as the
      # A-QINDEX tripwire above: a paper that DREW figures must come back with ARMED
      # A-FIGPROFILE and A-FIGTYPE-KIND lines.
      # An absent line means a stale auditor (< v2.32); a 'dormant' or 'NOT AUDITED'
      # line means the figure record never reached the registry; 'NOT CHECKED' means the
      # auditor could not load its engines (it runs with env=AUDIT_ENV from S3-9, which
      # puts the verified engines on its PYTHONPATH) — the delivered-paper
      # defect this release exists to close. Either way the figures were NOT certified
      # and a clean exit code here would be meaningless.
      # Keyed on the paper's ACTUAL figures (its fig_manifest questions), not on the flag:
      # a figural_present paper whose every slot was DENIED by the Axis-1 budget drew
      # nothing, commits an empty record and is legitimately dormant (edge case E18).
      _fmp = f'/home/claude/{EXAM}_fig_manifest.json'
      _fm_qs = (json.load(open(_fmp, encoding='utf-8')).get('questions') or {}) if os.path.exists(_fmp) else {}
      if _fm_qs:
          for _g in ('A-FIGPROFILE', 'A-FIGTYPE-KIND'):
              _gl = [l for l in (_r.stdout or '').splitlines() if re.search(r'\]\s+' + _g + r'\s', l)]
              # 'NOT CHECKED' = the auditor could not import / call figure_types or
              # blueprint_core (stale or unimportable engine) — equally uncertified.
              if not _gl or any(('dormant' in l or 'NOT AUDITED' in l or 'NOT CHECKED' in l
                                 or 'NOT ESTABLISHED' in l) for l in _gl):
                  _infra4c('S13-4c-5',
                      f"HARD STOP [HS:INFRA] (S13-4c, v5.88): the auditor did not certify this paper's "
                      f"figures — {_g}: {_gl[0].strip() if _gl else 'no line (auditor < v2.32; refresh the per-exam copy from the verified repo audit_canonical.py)'}. "
                      f"The figure record must be in the registry (S13-4 commits it whenever "
                      f"{EXAM}_fig_manifest.json is non-empty — final_assembly v1.10) and every "
                      f"figural question must carry object_type + semantic objects. Re-run S13-4 "
                      f"in FULL, then S13-REGCHECK and this re-sweep. present_files is forbidden "
                      f"until clean (B-7).")
      # v5.85 STIMULUS-GROUP TRIPWIRE (GAP-2026-09-21-LINKED-PLACEMENT), same shape
      # as the A-QINDEX tripwire above: a set-placed paper (STIM_ACTIVE) must come
      # back with an ARMED A-BLOCK verdict. An absent line means a stale auditor; a
      # 'dormant' line means the profile or the set ids never reached it. Either way
      # the sets were NOT certified, so a clean exit code here would be meaningless.
      if STIM_ACTIVE:
          _ab = [l for l in (_r.stdout or '').splitlines()
                 if re.search(r'\]\s+A-BLOCK\s', l)]
          if not _ab or any('dormant' in l for l in _ab):
              _infra4c('S13-4c-6',
                  f"HARD STOP [HS:INFRA] (S13-4c, v5.85): the auditor did not certify the "
                  f"stimulus groups of this set-placed paper "
                  f"({_ab[0].strip() if _ab else 'no A-BLOCK line'}). The paper's "
                  f"profile snapshot {STIM_PROFILE_PATH} must exist (S3-12b writes it) "
                  f"and be passed as --stimulus-profile; re-run S3-12b and this "
                  f"re-sweep. present_files is forbidden until clean (B-7).")
      _bs4c = json.load(open(_bs4c_p, encoding='utf-8')) if os.path.exists(_bs4c_p) else {}
      for _k4 in [k for k in (_bs4c.get('infra_heal') or {}) if str(k).startswith('S13-4c')]:
          _bs4c['infra_heal'] = bc.infra_heal_clear(_bs4c.get('infra_heal'), _k4)   # this re-sweep passed
      json.dump(_bs4c, open(_bs4c_p, 'w', encoding='utf-8'), indent=2)
  ```

  v5.48.0: this re-sweep now ALSO arms A-QINDEX (the engine-enforced FK gate over the
  question_index committed at S13-4) via --registry/--blueprint/--mockN, and a nonzero
  exit here is a HARD STOP [HS:INFRA] — v5.89: S13-2F already certified the docx against a
  preview of this exact commit with every gate, so only a commit that differs from its
  preview, or a docx changed after certification (A-CERT), can cause it. For the dossier-fed gates it remains the same auditor, the
  same A-* catalogue, and the same paper that S13-2 already swept clean — run once more so
  those two gates read facts rather than defaults. A FAIL here is handled exactly as a
  FAIL in S13-2 is handled (fix, re-run, present_files forbidden until clean, B-7).
  If AUDIT_AVAILABLE is False the dossier is still written and this re-sweep is skipped,
  with the S4-11 absence note (see the audit.py requirement block at the head of this
  spec) already stating that no machine audit ran.

## S13-5 — Registry integrity check (unchanged)

## S13-6 — THE DELIVERABLE SET IS CLOSED (v3.5 — read before delivering)

  At Final Assembly, Step 7 delivers the CLOSED SET to the user, and NOTHING
  ELSE — EXACTLY the two files below (v5.91: the v5.89 conditional additions are retired —
  see NO CONDITIONAL ADDITIONS below). This is an exhaustive, closed list — not a
  minimum. (v5.73: the dossier left the set by operator decision; the set no
  longer varies, so the v5.54.1 count-drift cannot recur.)

  DELIVER (mandatory, both via the SAME present_files call):
    1. [ExamCode]_[paper_slug]_Create.docx  — the final paper ("Mock[N]"
                                              zero-padded for a mock; scoped slug otherwise)
                                              → Use locally
    2. [ExamCode]_registry.json             — updated dedup/tracking registry
                                              → Replace in Project Files (REGISTRY-HANDOFF-LAW)

  NO CONDITIONAL ADDITIONS (v5.91 — GAP-2026-11-04 D3 (a); STEP-CONTRACT-LAW). v5.89 added
  an amended in-run blueprint and the repo auditor copy as conditional third / fourth files;
  after every release that touched the auditor, EVERY project received a third file on its
  next paper. Both are now INTERNAL (owner decision D3 a): the run already audits with the
  verified repo audit_canonical.py; an S3-2D schedule recompute is reproduced by every run
  from its provenance, while a ladder R5 amendment (measured band / allocation) applies to
  THIS paper only and is recorded on its registry entry (difficulty_check / ladder records).
  Each is disclosed by ONE informational footer line
  (Framework_DeliveryFooter §LADDER), never delivered:
  ```python
  import os
  import blueprint_core as bc
  _bp_name = os.path.basename(BP_SRC_PATH)
  _bp_proj = f'/mnt/project/{_bp_name}'
  INFO_LINES_S136 = []
  if (not os.path.exists(_bp_proj)
          or open(_bp_proj, 'rb').read() != open(BP_SRC_PATH, 'rb').read()):
      INFO_LINES_S136.append("blueprint amended in this run (S3-2D recompute and/or ladder R5 amendments for "
                             "this paper, recorded on its registry entry) — informational; nothing to upload")
  if globals().get('AUDITOR_FROM_REPO'):
      INFO_LINES_S136.append("project auditor copy is missing or older than the verified repo auditor — this "
                             "run used the verified repo auditor; informational, nothing to upload")
  # v5.92 (GAP-2026-11-05 Part D / DeliveryFooter §FOOTER-FT): a difficulty control that could
  # not measure SAYS SO — AMBER lines from the ONE formatter; never a stop, no certification
  # effect (v5.96, OD-2026-11-09: a Create paper is never NOT CERTIFIED).
  # The persisted record is the source (every CHECK 3c mutation was written there in the same
  # write as difficulty_plan); the in-memory globals are the fallback for a fresh session.
  try:
      import json as _json6
      _bs6 = _json6.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8')) or {}
  except Exception:                                   # noqa: BLE001 — never a stop
      _bs6 = {}
  _ds = dict(globals().get('DIFFICULTY_STATE') or {}, **(_bs6.get('difficulty_state') or {}))
  _lm6 = globals().get('LEVEL_MODEL') or _ds.get('level_model')
  DIFFICULTY_LINES_S136 = bc.difficulty_unverified_lines(
      globals().get('QUALITY_READINESS') or _bs6.get('quality_readiness'), _lm6,
      n_level_items=_ds.get('n_level_items', 0), judge_dormant_qs=_ds.get('judge_dormant_qs') or [],
      hard_missed=_ds.get('hard_missed', 0), coverage=globals().get('PROFILE_COVERAGE'))
  INFO_LINES_S136.extend(DIFFICULTY_LINES_S136)
  # v5.92 (DL-51/52): what moved and what the judges disagreed on — read from the persisted
  # plan pair and the items' difficulty_check records; informational lines, never a verdict.
  _orig6 = _bs6.get('difficulty_schedule_original') or {}
  _fin6 = _bs6.get('difficulty_plan') or {}
  _moved6 = sorted((q for q in _orig6 if _fin6.get(q) not in (None, _orig6[q])), key=lambda x: int(x))
  if _moved6:
      INFO_LINES_S136.append(f"difficulty plan amended in this run: {len(_moved6)} slot(s) moved band "
                             f"(Q{', Q'.join(_moved6[:12])}{'…' if len(_moved6) > 12 else ''}) — the label follows the evidence")
  try:
      _kd6 = _json6.load(open(f'/home/claude/{EXAM}_M{N}_answer_key.json', encoding='utf-8')) or {}
  except Exception:                                   # noqa: BLE001 — never a stop
      _kd6 = {}
  # v5.94 (GAP-2026-11-07): delivered vs target counts, forced / swapped / held items (legacy: DR3), unmeasured slots and the organic
  # ruler's state — one formatter (bc.difficulty_layer_lines), informational, never a verdict.
  _l2_6 = _ds.get('l2_model') if isinstance(_ds.get('l2_model'), dict) else None
  _l2ids_6 = set((_l2_6 or {}).get('scope_ids') or [])
  _n_l2_6 = sum(1 for _e6x in ((_kd6.get('concept_map') or {}).values())
                if isinstance(_e6x, dict) and str(_e6x.get('subtopic_id')) in _l2ids_6)
  INFO_LINES_S136.extend(bc.difficulty_layer_lines(_ds.get('paper_gate'), _l2_6, n_l2_items=_n_l2_6,
                                                   shares_source=(_l2_6 or {}).get('grades_source')))
  # v5.96 (OD-2026-11-09): every slot chain that ended at a terminal — forced labels, majority
  # certifications and DISCLOSED items are AMBER-class (DeliveryFooter §LADDER), re-keys and sibling
  # replacements informational. Engine-written (bc.chain_footer_lines, recorded by S13-2L).
  _cf6 = _ds.get('chain_footer') if isinstance(_ds.get('chain_footer'), dict) else {}
  INFO_LINES_S136.extend(_cf6.get('info') or [])
  AMBER_NOTES = list(globals().get('AMBER_NOTES') or []) + [x for x in (_cf6.get('amber') or [])
                                                             if x not in (globals().get('AMBER_NOTES') or [])]
  _notes6 = {}
  for _q6, _e6 in ((_kd6.get('concept_map') or {}).items()):
      _ln6 = ((_e6 or {}).get('difficulty_check') or {}).get('level_note') if isinstance(_e6, dict) else None
      if _ln6 and _ln6 != 'advisory':
          _notes6.setdefault(str(_ln6), []).append(str(_q6))
  for _ln6, _qs6 in sorted(_notes6.items()):
      INFO_LINES_S136.append(f"difficulty note '{_ln6}': Q{', Q'.join(sorted(_qs6, key=int)[:12])}"
                             f"{'…' if len(_qs6) > 12 else ''} — recorded on the item (difficulty_check.level_note)")
  EXTRA_DELIVERABLES = ()          # the closed set is ALWAYS exactly the two files
  EXTRA_REPLACE = ()
  # ── S13-6OP (v6.0) — the §LADDER-OP lines arrive through difficulty_state.chain_footer['info'] (written by
  #    S13-2L, printed above with the chain footer); nothing is composed here a second time ──
  for _l in INFO_LINES_S136:
      print("INFO: " + _l)
  ```

  DO NOT DELIVER (internal — never passed to present_files):
    ✗ [ExamCode]_M[N]_audit_dossier.json    — Tier-A dossier, /home/claude (S13-4b, v5.73)
    ✗ [ExamCode]_M[N]_answer_key.json       — internal sidecar (S3-14)
    ✗ any standalone answer-key file in ANY format (.docx/.pdf/.json/.txt)
    ✗ [ExamCode]_fig_manifest.json          — internal
    ✗ [ExamCode]_M[N]_batch_state.json      — internal
    ✗ [ExamCode]_M[N]_progress.json         — internal
    ✗ [ExamCode]_M[N]_item_sweep_certificate.json / _item_findings.json — internal (S13-2F)
    ✗ any per-batch cumulative docx (Q1to[k]) — superseded by _Create.docx
    ✗ any review packet / verdict file — INTERNAL to S13-2G (/home/claude/[ExamCode]_M[N]_review/)
    ✗ [ExamCode]_mock_test_audit.py, any *_blueprint.json — internal (v5.91 D3 a)

  This is the inline anchor for R-DELIVER. The answers exist ONLY in the
  internal answer_key.json sidecar (S3-14), which is NEVER delivered. If the
  user wants a learner-facing answer key, that is a Step-4 (MockExplain)
  artefact, not a Step-7 one. Step 7 ships the paper + registry and nothing else, every
  time (v5.91 — the set is DERIVED from STEP_CONTRACTS.json, never a third file).

## S13-7 — Pre-delivery checklist (v3.5 — MANDATORY before present_files; v5.53 — extracted)

  Run this 7-point self-verification. If ANY item fails: fix, then re-run.
  present_files is FORBIDDEN until all 7 pass (extends B-7 to Final Assembly).

  v5.53: the 7 checks now live in `final_assembly.predelivery_checklist()` — the one
  extracted function that reads the filesystem (its whole job is verifying real files
  landed in a real directory, so it can't be made pure like the other three).

  ```python
  import os, json
  out = '/mnt/user-data/outputs'
  # v5.28: paper_slug is ALWAYS pp.paper_slug(paper_id) — the single shared implementation
  # (paper_pipeline.py), replacing the old inline C2 v5.21 version. Zero-pads mocks to 2
  # digits (Mock01, not Mock1) and correctly collapses scoped "::" before remaining ":".
  paper_slug = pp.paper_slug(paper_id)
  docx_name = f'{EXAM}_{paper_slug}_Create.docx'
  reg_name  = f'{EXAM}_registry.json'
  # v5.73: the dossier is INTERNAL. dossier_name is still passed so check 5 names it
  # explicitly as a LEAK if it was ever staged; the closed set is always {docx, registry}.
  dossier_name = f'{EXAM}_M{N}_audit_dossier.json'

  # v5.91 (GAP-2026-11-04 A8): remove, BEFORE the checklist, every file THIS paper's run left
  # in outputs that is not one of the two deliverables — the per-batch Q1to[K].docx, a legacy
  # review packet / verdict file, an auditor or blueprint copy, any internal sidecar.
  # fa.outputs_to_clear is pure and names only this run's artefacts (other papers' / steps'
  # earlier outputs in the same chat are never touched). Check 6 then passes with no manual step.
  for _x in fa.outputs_to_clear(os.listdir(out), docx_name=docx_name, reg_name=reg_name):
      os.remove(os.path.join(out, _x))
      print(f"S13-7: cleared {_x} from outputs (not a Step 7 deliverable).")

  _pdc = fa.predelivery_checklist(
      out, docx_name=docx_name, reg_name=reg_name, dossier_name=dossier_name,
      regcheck_ok=globals().get('REGCHECK_OK'), qindex_ok=globals().get('QINDEX_OK'),
      extra_deliverables=())          # v5.91 (D3 a): never widens the two-file set
  if not _pdc['ok']:
      raise SystemExit(
          "HARD STOP [HS:INFRA] (S13-7): pre-delivery checklist failed: "
          + "; ".join(_pdc['fails'])
          + ". Fix each, then re-run S13-7. Do NOT call present_files yet. "
          + "If item 4 fails, DELETE the off-spec answer-key file from outputs. "
          + "If item 2/3 fails, re-run S13-4 + S13-REGCHECK. "
          + "If item 5/6 fails, a file of THIS paper that fa.outputs_to_clear does not recognise "
          + "is in outputs — move it to /home/claude and re-run S13-7 (an engine gap: report it).")
  print("S13-7: all 7 pre-delivery checks PASS. Cleared to deliver.")
  ```

  Stage ONLY the deliverables in /mnt/user-data/outputs; keep every internal file
  in /home/claude. Item 6 enforces the closed set.
  THE CLOSED SET (v5.73; v5.91 D3 a): the rectified docx + registry.json — nothing else, ever.
  A staged [ExamCode]_M[N]_audit_dossier.json fails item 5 (internal sidecar leak).

## S13-8 — Deliver (v3.5 — the SINGLE present_files call)

  Call present_files ONCE, docx first (most relevant), then the registry — EXACTLY these
  two files (v5.91, STEP_CONTRACTS.json; EXTRA_DELIVERABLES is always empty):
    present_files([
        docx_path,        # C2: paper-scoped ({EXAM}_{paper_slug}_Create.docx — zero-padded mock or scoped slug)
        reg_path,
    ])

  THE SET IS DECIDED BY THE ENGINE, NOT BY THIS PROSE (v5.76 — REGISTRY-HANDOFF-LAW,
  DeliveryFooter §8, mock_sync_audit MS-14). Before the call, build and verify the
  closed set exactly as Step 9 does at S19-0b — commit_registry ALWAYS changes the
  registry (it appends the paper), so the set is the paper + registry, every time — nothing
  else (v5.91 D3 a):

  ```python
  import os, json
  import paper_pipeline as pp
  # `registry` is the committed copy (_commit['registry'], S13-4); the fingerprint of
  # what this run STARTED from is REG_SRC (S3-1, pp.resolve_registry — attachment or
  # Project Files; v5.84 REGISTRY-SOURCE-LAW), never a hardcoded Files path. HANDOFF_STEP is
  # the trigger that started this run — 'TestCreate' or 'MockCreate' (any other value,
  # including a retired *Repair name, is refused by the engine: RHIllegalHandoff).
  HANDOFF_STEP = globals().get('HANDOFF_STEP') or (
      'MockCreate' if pp.paper_prefix(paper_id) == 'MOCK' else 'TestCreate')
  _reg_fp_loaded = REG_SRC['fingerprint']                   # S3-1 resolved + pinned it (R4)
  _hs = pp.handoff_set(HANDOFF_STEP,
                       primary_docx=f'{EXAM}_{pp.paper_slug(paper_id)}_Create.docx',
                       reg_name=f'{EXAM}_registry.json',
                       registry_changed=pp.registry_changed(_reg_fp_loaded, registry), final=True)
  if not _hs['registry_delivered']:
      raise SystemExit('HARD STOP [HS:INFRA] (S13-8): registry unchanged after Final Assembly — '
                       'commit_registry did not run; nothing is delivered.')
  # v5.91: judged on THIS paper's delivery scope (fa.delivery_scope) — another step's or
  # paper's earlier output in the same chat is history, never part of this delivery.
  import final_assembly as fa
  _v = pp.verify_handoff_outputs(fa.delivery_scope(os.listdir('/mnt/user-data/outputs'),
                                                   docx_name=f'{EXAM}_{pp.paper_slug(paper_id)}_Create.docx',
                                                   reg_name=f'{EXAM}_registry.json'), _hs)
  if not _v['ok']:
      raise SystemExit(f"HARD STOP [HS:INFRA] (S13-8): outputs != closed set — missing {_v['missing']}, "
                       f"stray {_v['stray']}. Fix, then re-run. Do NOT call present_files.")
  for _line in pp.handoff_footer_lines(_hs):
      print(_line)
  ```

  This is the ONLY present_files call at Final Assembly. Do NOT call it once
  per file. Do NOT call it for any internal file. The per-batch habit of "one
  docx per present_files" does NOT apply here — Final Assembly ships the paper and the
  registry in ONE call.
  WORKER MODE: this call is the DELIVERY PROXY of Framework_MockTestOrchestrate.md O3-4 (S1-0R).

## S13-9 — Handoff message (v3.5 — print after present_files, then END)

  v5.91: run this ONLY after the S13-8 present_files call returned without error (if it
  errored, re-run S13-7 / S13-8 — the state stays REVIEWED, so an interrupted response
  resumes there through S4-12). Then mark the paper finished, so a later "continue" in this
  chat never re-enters §13 or looks for a batch (S4-6 / S4-12):
  ```python
  # ── S13-9 terminal state (v5.91 — GAP-2026-11-04; STEP_CONTRACTS allowed end state) ──
  import json
  _bs9 = json.load(open(f'/home/claude/{EXAM}_M{N}_batch_state.json', encoding='utf-8'))
  _bs9['state'] = 'DELIVERED'
  json.dump(_bs9, open(f'/home/claude/{EXAM}_M{N}_batch_state.json', 'w', encoding='utf-8'), indent=2)
  ```

  Print exactly this block (no question content — MANDATE 0), filling brackets:

  ```
  === MOCK [N] COMPLETE — Step 7 done ===
  Delivered (2 files — always exactly these two, v5.91):
    • [ExamCode]_Mock[N]_Create.docx   — the mock paper            → Use locally
    • [ExamCode]_registry.json           — updated registry           → Replace in Project Files
  Independent review: [round k, n item(s) repaired | not run on Q… (<reason>)]
    [+ "(same-session review — no sub-agent in this runtime)" when review_summary.reviewer
     lists 'same-session'] — INFORMATIONAL, never an action for the user.

  ⚠ REGISTRY HANDOFF — REQUIRED before generating the next mock:
    Replace registry.json in your [ExamCode] project knowledge with the one
    just delivered — OR attach this delivered file to the next step's trigger
    (an attachment always wins over the Project Files copy; REGISTRY-SOURCE-LAW).
    The next mock's dedup depends on it. If you skip this,
    Mock [N+1] may repeat questions/scenarios from Mock [N].

  No separate answer-key file is produced by Step 7 (by design). Answers are
  surfaced later by Step 9 (MockExplain).

  Next step → Step 9 (MockExplain): explanations for this mock.
  (v5.36: the former Step 8 independent audit is retired. If audit.py was present, the
  result below is the ONLY machine audit this paper will receive; if it was absent, say so
  explicitly here.)
  Audit result this run: [exit_0 / SHIP / NOT RUN — audit.py absent].
  =========================================
  ```

  After printing the handoff: render the S13-9A footer, then END THE RESPONSE. Write
  nothing more.

## S13-9A — Post-delivery footer (MANDATORY after every present_files call)

```
After every present_files call and any in-chat delivery report or handoff message,
render the standardized visual delivery footer as the LAST element in the response.

Follow Framework_DeliveryFooter.md for footer type selection (F1 mid-step / F2 step-complete),
deliverable file badges (Upload / Replace / Use locally), and next-step reference.

Step 7 uses BOTH footer types:
  - F1 (amber) after each non-final batch (delivers cumulative Q1to[K].docx)
  - F2 (green) after Final Assembly (delivers Create.docx + registry.json)

NOTE: The footer renders AFTER the S13-9 handoff message. Sequence is:
  1. S13-7 pre-delivery checklist → 2. S13-8 present_files → 3. S13-9 handoff → 4. Footer
```
WORKER MODE: the footer goes into the worker's chat block (Framework_MockTestOrchestrate.md O3-4).

# ════════════════════════════════════════════════════════════════════════
# §14 — REGISTRY SCHEMA (v2.0 — fields added)
# ════════════════════════════════════════════════════════════════════════

## S14-1 — Universal fields (v2.0 GAP-04 fix — added fields)

  ```json
  {
    "exam_code"          : "[ExamCode]",
    "schema_version"     : "1.0",
    "mocks_completed"    : [],
    "question_hashes"    : [],
    "stem_texts"         : [],
    "semantic_tuples"    : [],
    "semantic_usage"     : [],
    "exhausted_subtopics": {},
    "question_index"     : [],
    "image_phashes"      : [],
    "image_sources_used" : [],
    "session_log"        : [],
    "content_tracking"   : { "_schema": {...}, ... }
  }
  ```

  question_index (v5.2): seeded [] by Step 1; Step 7 APPENDS one object per mock
  {mock, questions:[{q, subtopic_id, difficulty}]} at S13-4 (never in the docx), certified by
  G-QINDEX (S12-NEW-26 / S13-QINDEX). image_phashes, image_sources_used, session_log: MUST be
  present from Mock 1.
  options_by_q (v4.7; re-keyed v5.67): { "<paper_id>": { "q": expected_option_count } }
  — per-PAPER, per-question expected option count, keyed by paper_id for EVERY series
  (the authority). For the MOCK series the legacy ordinal key { "N": {...} } is ALSO
  written (pre-v5.67 readers); it is NEVER written for a scoped paper, because the
  registry is shared across series and a scoped ordinal on "N" overwrote the mock's map
  (GAP-2026-08-24-OPTIONS-BY-Q-SERIES-COLLISION). 0 marks a NAT question (no options).
  Written by S13-REGCHECK (final_assembly.regcheck); consumed by Step 9 (Explain) P3 and
  audit_canonical load_sources, both paper_id first, "N" second.
  key_commitments (v5.59): { "<paper_id>": { schema: 1, alg: "sha256",
  entries: { "q": { salt, h } } } } — h = sha256(paper_id|q|salt|canonical_answer).
  Written by S13-4 (fa.commit_registry answer_key=…); consumed by Step 9 §7-8, which
  hashes its OWN derived answers and compares. NEVER plaintext. Gate: G-KEYCOMMIT.
  rc_manifests[] / di_manifests[] / figural_manifests[] (v5.86): every entry S13-4 writes
  carries "paper_id" beside "mock": N and is replaced by paper_id (fa.commit_registry v1.8);
  readers (audit_canonical v2.31, Step 9) select THIS paper's entry by paper_id — a legacy
  entry without one belongs to MOCK:M<mock>. Never matched by the bare ordinal: the lists
  are shared by every series (GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC).
  figural_manifests[].semantic_objects (v5.59): { "q": [ {role, kind, name, canonical,
  descriptor} ] } — what each generated figure depicts (S7-NEW-B2); consumed by Step 9
  §13-2b. Both ADDITIVE; older registries read unchanged (EC-V18).
  section_names (v4.8): list of declared section names for this exam, from blueprint
  sections[].section_name. Written by S13-REGCHECK; consumed by the embedded G-SECTIONHDR
  gate and audit.py A-SECHDR to flag stray section-name headers in the paper body.
  If registry from Step 1 is missing them: S13-4 first-mock init adds them, and
  S13-REGCHECK (v3.5) enforces the full schema as a gate before delivery —
  self-healing any field the drifted Step-1 template omitted, so an incomplete
  registry can never ship.

## S14-2 through S14-5 — (unchanged from v1.0 — see v1.0 for full spec)

# ════════════════════════════════════════════════════════════════════════
# §15 — AUTO-FIX PROTOCOL (unchanged from v1.0)
# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# §16 — STATUS DASHBOARD (unchanged from v1.0)
# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# §17 — DEFINITION OF DONE (v2.0 — additional items)
# ════════════════════════════════════════════════════════════════════════

## S17-1 — Complete DoD checklist (v2.0 additions marked *; v3.0 marked **)

  GENERATION (BATCH ENFORCEMENT — §4 v3.0):
  □ All batches completed (batches_completed == every batch_id in plan)  **
  □ ONE batch = ONE response throughout (no two batches in one response)  **
  □ Every batch generated EXACTLY q_count Qs from batch_state.json (B-3)  **
  □ No batch was auto-advanced (B-4); every next batch needed a "continue"  **
  □ Pre-batch self-check (S4-5) run before each batch  **
  □ batch_state.json updated after each delivery (S4-8a)  **
  □ Final batch auto-ran Final Assembly in same response (S4-9)  **
  □ Every batch: Layer 1 STOP executed (separate response per batch)  *
  □ Every batch: Manual gate checklist (S4-11) completed if no audit.py  *
  □ Final Assembly gate check passed (81 gates)  *
  □ (Issue 2b) group-presence (G-GROUPMANDATE) + min-count (G-MINCOUNT) verified for
    this mock; cadence left to Step 1 (cross-mock, not gated in Step 7)  *
  □ Audit STDOUT appended to every batch reply

  CONTENT QUALITY:
  □ All 81 gates: PASS or NON-FIX-WARN  *
    (the 12 v5.33 FIGURE CONFORMANCE gates report AMBER / VOID_ITEM / BLOCKING
     per S10-7 Q8b; NO colour condition may halt a run, and EC-V18 downgrades
     every BLOCKING gate to AMBER for output with no FigureSpec sidecar)  *
  □ Each subtopic has EXACTLY its blueprint q_count (RULE A, G-ALLOC-SUBTOPIC) — DOUBT-3  ***
  □ No scenario_key repeats anywhere in the mock (RULE B, G-CONCEPTDUP) — DOUBT-3  ***
  □ Subtopics with N>1 use N distinct scenarios; extra concepts invented as needed  ***
  □ OMML renders correctly (generated with python-docx if QA present); NO
    algebraic/built-up expression shipped as a raster image (R-MATH-OMML,
    G-MATH-RASTER) — every inline image is a named figure/stimulus, never math  *
  □ All images: visual_verified=True
  □ Font: configured font (FONT_NAME) and size (FONT_SIZE_PT) throughout  *
  □ Option labels: configured format (OPTION_LABEL_FMT)  *
  □ No section headings in paper body  *
  □ No title/info/scoring/cover block before Q.1 — paper is questions-only (R8b, G-PREQ1)  *
  □ No answer key embedded in docx  *
  □ All RC passages reprinted per linked Q
  □ All fact-recall questions: source citations logged (authoritative sources)
  □ All per-section mandatory areas/topics covered — the full set declared in
    section_rules (count read from data, not hardcoded)
  □ manifest.mandatory_every_mock — every mandated subtopic present in every mock
    (S3-17 pre-gen HS-8 + G-ALLOC-SUBTOPIC in generated Qs); exam-agnostic, no names  *
  □ manifest.alternation_groups — ≤1 member of each group per mock (S3-17 + G-ALTGROUP)  *
  □ Cross-mock variant rotation honored where section_rules declares a ROTATION cycle (S6-9)  *
  □ Difficulty: schedule satisfied

  REGISTRY:
  □ pending_registry committed at Final Assembly (not during generation)  *
  □ content_tracking L4-L18 fields populated  *
  □ image_phashes, image_sources_used, session_log present  *
  □ Registry integrity check passed

  DELIVERY:
  □ Complete docx delivered via present_files
  □ Updated registry.json delivered via present_files
  □ Handoff message with registry replacement instruction
  □ Audit report produced
  □ S3-1 resolved the registry via pp.resolve_registry (attachment OR Project Files),
    printed REGISTRY SOURCE lines, and batch_state.registry_pin matched every turn (v5.84)  **

  DELIVERY (v3.5 — closed contract):
  □ The closed set delivered: EXACTLY final .docx + registry.json — two files (S13-6, R-DELIVER; v5.73 — the audit dossier is internal; v5.91 — no extras, D3 a)  **
  □ Step 7 ended in the SAME response as the last batch with the two files: the independent review ran IN-SESSION (S13-2G), no review packet / verdict file reached outputs, nothing was asked of the user (v5.91, STEP-CONTRACT-LAW)  **
  □ registry.json staged in /mnt/user-data/outputs and present_files'd (S13-8)  **
  □ NO standalone answer-key file in any format delivered (R-DELIVER)  **
  □ NO internal sidecar (answer_key/fig/batch_state/progress/audit_dossier) delivered  **
  □ S13-7 pre-delivery 7-point checklist passed before present_files  **
  □ S13-REGCHECK passed: registry schema-complete (top + content_tracking)  **
  □ G-DELIVERY-SET passed in the Final-Assembly gate sweep  **
  □ G-STIMULUS-ORPHAN passed: every linked-group question carries its shared
    stimulus inside its own block (R-LINKED / §9 Model A) — verified per batch
    AND mock-wide at Final Assembly  **
  □ G-QNUM-FIRST passed: every question block (single AND linked) opens with its
    "Q.<N>" paragraph; no stimulus/preamble precedes the Q-number; the linked
    specific-ask paragraph is non-numbered (R14)  **
  □ G-FORMATDUP passed: no two CLASS-2/3 questions sharing a CONCEPT_GROUP share
    presentation_key; ≥2 stem formats when a CONCEPT_GROUP has ≥3 Qs (RULE C);
    G-CLUSTER spacing/distribution satisfied (R19 v3.8)  **
  □ G-FIGURAL-COMPOSITE passed: every figural Q correctly structured per its
    image_role variant (v5.13 — stem_and_options / stem_only / options_only);
    no composite panel, no two images per line, no baked-in question chrome;
    option images (when present) 300 DPI on a uniform square canvas
    (R-FIGURAL / §10-S10-7/S10-8/S10-8A)  **
  □ G-UNDERLINE passed: every underline-class Q renders its target span as a real
    underlined run inside the sentence; no "(underlined: X)" annotation, no
    underscore/markdown fake (R-UNDERLINE / §10-S10-2)  **
  □ G-OPTREF passed: no stem references a terminal/escape option absent from the
    options; "no error/no improvement → last option" instructions have the escape
    option at the named position; carrier-sentence stems are two-paragraph, no
    run-on (R-OPTREF / §10-S10-2)  **
  □ G-UNIQUE passed: every Q satisfies R-ANSWER for its mode — single: exactly one
    defensible option; multi: the correct SET passes the set contract; CHECK 3
    verify_answer ran and answer_verified==true is recorded
    for all N (R-ANSWER / §7)  **
  □ G-MSQ-SET passed (multi only): every MSQ key is a non-empty proper subset of
    1..total_options; no banned AOTA option under multi (R-MSQ-ESCAPE). Dormant when
    multi_present=false  **
  □ G-MSQ-CARD passed (multi + fixed-k only): every MSQ key has |S|==msq_k  **
  □ G-MSQ-INSTR passed (multi only): every MSQ stem carries its select-instruction
    on the Q.N line (R14)  **
  □ G-NAT-NOOPT / G-NAT-ANSWER / G-NAT-GRADE / G-NAT-INSTR passed (numerical only): every NAT
    question renders zero options, carries a well-formed value (+ca_range lo<=hi for real NAT),
    a portal-safe grading value/type (0-9.- charset, S7-NEW-C), and its nat_instruction sits
    on the Q.N line (R4/R13/R14 NAT exemptions)  **
  □ options_by_q written to registry (per-question expected option count, 0 for NAT) so
    Step 4 resolves question type (ND6)  **
  □ G-MATH-RASTER passed: no algebraic/built-up expression ships as a raster
    image; every inline <w:drawing> is a canonically-named figure/stimulus
    (q{N}_problem/opt{i}/stim), and all built-up math is OMML (R-MATH-OMML /
    §10-S10-4)  **
  □ G-MATH-RESIDUE passed (v5.70): mock_math_residue_check 'blocking' list EMPTY
    — no flat/half-Unicode subscript, caret, ÷-fraction, flat radical, letter
    fraction, combining accent, residual ⟦MATH:⟧ delimiter, or empty/schema-
    invalid OMML in any stem/option; compile-fallback 'amber' regions named in
    the F1 footer (R-MATH-OMML / §10-S10-4 / S12-NEW-30)  **
  □ G-QINDEX passed (v5.2): registry.question_index has one {q, subtopic_id, difficulty}
    entry per question (q = 1..total_questions, sorted/unique/complete), every subtopic_id ∈
    blueprint.subtopic_list, every difficulty ∈ difficulty_labels, and the difficulty
    distribution == difficulty_schedule[N] exactly (S13-QINDEX / Contract v1.0)  **
  □ S13-9 handoff printed with the registry-replacement instruction  **

## S17-2 — Downstream handoff (v5.36: to Step 9; mechanism unchanged from v1.0)

# ════════════════════════════════════════════════════════════════════════
# §18 — AUDIT GATE GLOSSARY (81 gates total — 39 v1.0 baseline + 30 tabled below
#        + 12 FIGURE CONFORMANCE catalogued in audit_canonical.py)
# ════════════════════════════════════════════════════════════════════════

  v2.0 adds 6 new gates to the 39 from v1.0:

  | Gate Code    | Checks                                      | Fix?  | Fix                         |
  |--------------|---------------------------------------------|-------|-----------------------------|
  | G-FONTCHECK  | All runs use configured font (no banned fonts)  | YES   | Re-generate with configured font |
  | G-OPTLABEL   | Option labels match configured format           | YES   | Regenerate options          |
  | G-SECTIONHDR | No section headers in docx body — keyword form + (v4.8) section-NAME form (paragraph == a declared section name, from reg['section_names']) | YES   | Delete header paragraphs    |
  | G-ANSWERKEY  | No answer key embedded in docx              | YES   | Remove answer key section   |
  | G-FIGTEXT    | No figural text placeholders                | NO    | Generate real image or sub  |
  | G-ALTGROUP   | No alternation group has 2+ members in mock | YES   | Drop the off-parity member  |

  v3.2 added G-ALLOC-SUBTOPIC + G-COUNT-X-UNIQUE (with G-CONCEPTDUP from v3.1) → 48.
  These three DOUBT-3 gates (§12 S12-NEW-7/8/9) were defined but omitted from this table until
  v5.3; tabled here for glossary completeness:
  | G-CONCEPTDUP     | No scenario_key repeats in the mock (RULE B / DOUBT-3)      | YES | Regenerate the duplicate scenario         |
  | G-ALLOC-SUBTOPIC | Each subtopic_id has EXACTLY its blueprint q_count (RULE A) | YES | Add/drop questions to hit the exact count |
  | G-COUNT-X-UNIQUE | Per-subtopic generated counts match the concept_map        | YES | Reconcile concept_map vs generated Qs     |

  v3.5 adds 1 new gate (→ 49), enforced in the S13-2 Final-Assembly gate sweep:

  | Gate Code      | Checks                                          | Fix? | Fix                                  |
  |----------------|-------------------------------------------------|------|--------------------------------------|
  | G-DELIVERY-SET | This paper's delivery scope (fa.delivery_scope) holds EXACTLY the closed set: docx + registry (v5.73 — the audit dossier is internal; v5.91 — two files, no extras) | YES  | fa.outputs_to_clear removes this run's leftovers (S13-7) |

  G-DELIVERY-SET (definition): at Final Assembly, /mnt/user-data/outputs must
  contain exactly { [ExamCode]_Mock[N]_Create.docx, [ExamCode]_registry.json } within this
  paper's delivery scope (v5.91 — fa.delivery_scope) — no more, no fewer. A standalone answer-key file, a leaked internal sidecar,
  or a missing registry → Exit 1. This is the machine-checkable form of the
  S13-6 closed contract (identical to S13-7 items 4–6) and runs inside the S13-2
  sweep so the off-spec set is caught even if S13-7 is skipped.

  v3.6 adds 1 new gate (→ 50), enforced both per-batch (S4-11) and in the S13-2
  Final-Assembly gate sweep:

  | Gate Code         | Checks                                              | Fix? | Fix                                       |
  |-------------------|-----------------------------------------------------|------|-------------------------------------------|
  | G-STIMULUS-ORPHAN | Every linked Q carries its stimulus in its own block| YES  | Embed stimulus per member (Model A, §9)   |

  G-STIMULUS-ORPHAN (definition): for one-question-at-a-time online rendering,
  any question depending on a shared passage / table / chart / cloze paragraph
  must physically contain that stimulus in its own block (§9 Model A), unless the
  platform is confirmed to support engine-native passage-groups (Model B). A
  "lead-in only" layout (stimulus before Q1, absent from Q2..Qn) or any
  "Q.X and Q.Y" cross-reference text in a stem → Exit 1. Not fixable by deleting
  the questions — fix by embedding the stimulus into each member.

  v3.7 adds 1 new gate (→ 51), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code     | Checks                                                  | Fix? | Fix                                       |
  |---------------|---------------------------------------------------------|------|-------------------------------------------|
  | G-QNUM-FIRST  | Every question block opens with its "Q.<N>" paragraph   | YES  | Re-emit block: Q.N context line first     |

  G-QNUM-FIRST (definition): enforces the v3.7 Q.N-FIRST contract / R14. Every
  question block — single OR linked — must OPEN with its "Q.<N>" paragraph; no
  table, chart, passage, or unnumbered preamble may precede the Q-number. In a
  linked block the Q-number fuses with the shared context line and the specific
  ask is a separate non-numbered bold paragraph. A block opening with a
  stimulus/preamble, or carrying a stray second Q-number, → Exit 1. Fix by
  re-emitting via S10-LINKED (add_qn_context → stimulus → add_specific_ask).

  v3.8 adds 1 new gate (→ 52), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code   | Checks                                                        | Fix? | Fix                                          |
  |-------------|---------------------------------------------------------------|------|----------------------------------------------|
  | G-FORMATDUP | No CLASS-2/3 CONCEPT_GROUP clones (same presentation_key)      | YES  | Regenerate on a new stem-format/distractor   |

  G-FORMATDUP (definition): enforces RULE C / §6-3c. For CLASS-2 (vocabulary/
  item-recall) and CLASS-3 (fact-recall) questions, two questions sharing a
  CONCEPT_GROUP may not share presentation_key = (stem_format_variant |
  distractor_strategy); a different target word/fact (distinct scenario_key) does
  NOT excuse an identical look. When a CONCEPT_GROUP has ≥3 questions, ≥2 distinct
  stem_format_variants must appear. A CLASS-2/3 question with no presentation_key
  (generator did not pick a defined variant) also fails. This is the gate that
  catches the M1 Q.77/Q.79 (Antonym) and Q.78/Q.80 (Synonym) clones. Fix by
  regenerating the offending question on a new presentation (§6-3c menus); never
  reduce N. The companion R19 v3.8 spacing (G-CLUSTER manual check) prevents
  same-family clustering.

  v4.0 adds 1 new gate (→ 53), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code            | Checks                                                         | Fix? | Fix                                     |
  |----------------------|---------------------------------------------------------------|------|-----------------------------------------|
  | G-FIGURAL-COMPOSITE  | Figural Q decomposed: problem img + 1 img/option, 1 per line   | YES  | Re-render discrete images (S10-7/S10-8)  |

  G-FIGURAL-COMPOSITE (definition): enforces R-FIGURAL / §10-S10-7/S10-8. A figural
  question must render as the problem figure(s) plus ONE separate image per option,
  stacked single-column (one option image per line) and bound 1:1 to its "i."
  label. A figural block with fewer than (n_options + 1) inline images — the
  canonical case being a SINGLE composite panel with the problem and all options
  baked together — or any line/table-row carrying more than one option image, or a
  "1. Figure 1" dummy-text option in place of an image → Exit 1. This is the gate
  that catches the M1-class composite (the SSC CGL T1 Q5 panel). Not fixable by
  editing text: re-render the figures discretely (S10-7) and re-emit via
  add_figural_question (S10-8). Image-quality (300 DPI, uniform option canvas, no
  baked-in chrome, real reference geometry) is enforced upstream at view-tool
  verification per S10-7.

  v4.1 adds 1 new gate (→ 54), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code   | Checks                                                          | Fix? | Fix                                       |
  |-------------|----------------------------------------------------------------|------|-------------------------------------------|
  | G-UNDERLINE | Underline-class Q renders a REAL underlined run, not "(underlined: X)" text | YES | Re-render via S10-2 add_stem_with_underline |

  G-UNDERLINE (definition): enforces R-UNDERLINE / §10-S10-2. Any question whose
  stem refers to an underlined element (UNDERLINE_TRIGGER_RE, or persisted
  stem_format_variant == 'sentence_embedded_underlined') must carry its target span
  as a genuine underlined run (<w:u>) inside the sentence. Exit 1 if the block
  contains a "(underlined: …)"/"(underline: …)" plain-text annotation, OR if no run
  in the block carries underline formatting. This is the gate that catches the M1
  Q.83 ("(underlined: senior than me)") and Q.78 ("(underlined: benevolent)")
  annotations and the document-wide absence of any <w:u> run. Parallel to G-FIGTEXT
  (figural-as-text); here it is underline-as-text. Not fixable by editing the note:
  re-render the carrier sentence via add_stem_with_underline so the target is a real
  underlined run, and drop the parenthetical.

  v4.2 adds 2 new gates (→ 56), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code | Checks                                                              | Fix? | Fix                                          |
  |-----------|--------------------------------------------------------------------|------|----------------------------------------------|
  | G-OPTREF  | Stem-referenced terminal/escape option exists & is positioned right| YES  | Add the escape option / switch template      |
  | G-UNIQUE  | Each Q has answer_verified==true (R-ANSWER ran)          | YES  | Re-run CHECK 3; disambiguate stem if needed  |
  | G-QINDEX  | question_index certified: one {q,subtopic_id,difficulty} per Q; ids ∈ blueprint; difficulty ∈ labels; distribution == schedule[N] (v5.2) | YES | Fix S7-NEW-A capture / schedule-first assign; rebuild index (S13-4) |

  G-OPTREF (definition): enforces R-OPTREF / §10-S10-2. If a stem REFERENCES a
  terminal/escape option — "if no error → (the) last option", "select 'No
  improvement'", "None of these / the above", "All of the above", "Both … and …",
  "Neither … nor …" — that option MUST be present in the option set, at the position
  the instruction names. A "pick the segment with the error" layout (all four options
  are sentence segments) may not carry a "no error → last option" escape unless a real
  "No error" option is appended. This is the gate that catches the M1 Q.100 mismatch
  (4 segments + a "no error → last option" instruction with no "No error" option).
  EXAM-AGNOSTIC: escape tokens and option structures come from section_rules
  (none_of_above_map S3-12, wrong_option_structure S3-13); the gate enforces coherence
  only, hardcoding no exam wording. Carrier-sentence run-ons (instruction + sentence on
  one line) are prevented by the §10-S10-2 two-paragraph layout. Fix by appending the
  escape option (re-balance K-BAL) or switching to the matching template.

  G-UNIQUE (definition): enforces R-ANSWER. Answer uniqueness is decided at GENERATION
  (§7 CHECK 3 verify_answer) because verbal ambiguity needs reasoning, not
  regex; G-UNIQUE is the record-presence backstop (same pattern as G-CONCEPTDUP reading
  concept_map). Any question whose sidecar lacks answer_verified == true →
  Exit 1: generation skipped the contract. This is the gate behind the M1 Q.3
  (Sister vs Cousin, paternal/maternal split) and Q.98 (is vs was, universal-truth
  convention) — each had a SECOND defensible option. EXAM-AGNOSTIC; the uniqueness
  classes are universal and any contested convention is pinned in section_rules, never
  hardcoded. Fix by re-running CHECK 3 and disambiguating the stem (qualify the
  relation / pin the convention / constrain the rule) or dropping the colliding option.

  v4.3 adds 1 new gate (→ 57), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code     | Checks                                                          | Fix? | Fix                                       |
  |---------------|----------------------------------------------------------------|------|-------------------------------------------|
  | G-MATH-RASTER | No built-up math shipped as an image; inline rasters are named figures/stimuli only | NO | Re-render expression as OMML (S10-4 add_math_stem); drop the raster |

  G-MATH-RASTER (definition): enforces R-MATH-OMML / §10-S10-4. Every algebraic or
  built-up expression (stacked fraction, exponent, radical, trig-with-fraction —
  S10-4 decision-tree rules 3-6) must render as native OMML (<m:oMath>) inline in
  the document text, NEVER as a raster image. The gate's authoritative signal is
  the figural image NAME-CONTRACT: the only legitimate producers of an inline
  raster are the figural emitter (§10-S10-8, names q{N}_problem[_k] / q{N}_opt{i})
  and the linked-stimulus path (§9, names q{N}_stim[_tag]); any inline <w:drawing>
  whose pic name falls OUTSIDE the pattern ^q\d+_(problem|opt\d+|stim) is an
  unauthorised raster → Exit 1. This is the gate that catches the M1 Q.55 defect
  (q55_e1.png / q55_e2.png — "x + 1/x = 5" and "x²+1/x²" rasterised at 300 DPI via
  matplotlib instead of OMML). The name-contract is provenance-proof: it reads the
  image, so a faked figural-manifest entry cannot smuggle a math raster past it, and
  it cannot false-positive on a genuine figure (named by the S10-8 convention) —
  validated in Python against the actual failing file (flags Q.55's two rasters,
  zero of the six genuine figural questions Q.3/10/12/16/19/22). Math-context stem
  detection and math image-name tokens (_e1, _eqn, _frac…) are reported as
  corroborating diagnostics only. Parallel to G-FIGTEXT (figural-as-text) and
  G-UNDERLINE (underline-as-text); here it is math-as-raster. NOT fixable by editing
  text: re-render the expression through §10-S10-4 add_math_stem / emit_math_inline
  (interleave <m:oMath> with the stem text) and delete the raster; if a flagged image
  is a genuine figure that was mis-named, re-emit via add_figural_question (§10-S10-8)
  so it carries the canonical q{N}_problem / q{N}_opt{i} name. The companion G-FRAC
  continues to catch the slash/caret ASCII fallback in the text stream.

  All 39 gates from v1.0 unchanged. See v1.0 §18 for full table.

  v4.5 adds 3 new gates (→ 60), MULTI-mode only (fully dormant when blueprint
  multi_present is false), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code   | Checks                                                            | Fix? | Fix                                          |
  |-------------|------------------------------------------------------------------|------|----------------------------------------------|
  | G-MSQ-SET   | MSQ key is a non-empty PROPER subset of 1..n; AOTA rule honored   | YES  | Regenerate so |S| is 1..n−1; drop AOTA if banned |
  | G-MSQ-CARD  | fixed-k exams: |S| == msq_k                                        | YES  | Regenerate the set to the instructed count   |
  | G-MSQ-INSTR | the multi instruction line is present in the Q.N stem (R14)       | YES  | Re-emit stem with instruction on the Q.N line |
  | G-NAT-NOOPT | NAT question renders ZERO option paragraphs (R4/R13 exempt)        | YES  | Re-emit as a 0-option NAT block (stem only)   |
  | G-NAT-ANSWER| NAT value well-formed for nat_answer_type; ca_range lo<=hi         | YES  | Regenerate value/band per nat_contract        |
  | G-NAT-GRADE  | portal grading value/type well-formed (0-9.- charset), deterministic | YES  | Re-run derive_nat_grading(); rework Q if NOT-SUPPORTED negative-range |
  | G-NAT-INSTR | the numerical-entry instruction is present in the Q.N stem (R14)   | YES  | Re-emit stem with nat_instruction on Q.N line |

  G-MSQ-SET (definition): enforces the structural half of R-ANSWER (multi) + R-MSQ-ESCAPE.
  Runs ONLY for sidecar concept_map entries with answer_cardinality=='multi' (skipped entirely
  when multi_present is false). The correct set S = answers[q] (a list[int]) must be a
  NON-EMPTY PROPER subset of {1..total_options}: k=0 (empty), out-of-range, and k=n
  (all-correct) are all defects. R-MSQ-ESCAPE: an "All of the above" option under multi is
  a defect unless section_rules msq_allow_aota=true (read into msq_meta). EXAM-AGNOSTIC —
  total_options/k-config come from msq_meta (blueprint/section_rules), no exam wording
  hardcoded. Validated in Python against real MSQ docx fixtures (catches k=0, k=n, and an
  AOTA option when the flag is false; passes a clean variable-k set). NOT fixable by
  editing the key — regenerate the question with a well-formed intended set.

  G-MSQ-CARD (definition): enforces the fixed-k cardinality of R-ANSWER (multi). Runs ONLY
  when answer_cardinality=='multi' AND msq_meta.msq_k_mode=='fixed'. For "Select TWO"/"Select
  THREE" exams it guarantees |S| matches the instructed k. Variable-k exams skip it (no
  fixed cardinality). Fix by regenerating the set to the configured count.

  G-MSQ-INSTR (definition): enforces R14 placement of the MSQ instruction. Runs ONLY for
  answer_cardinality=='multi'. The select-instruction ("(One or more options may be correct)" /
  "(Select TWO)" / localized equivalent from section_rules) MUST live INSIDE the bold
  Q.<N>-first stem paragraph — there is NO paper-level instructions page, and a separate
  instruction paragraph would break R14 / G-QNUM-FIRST. Step 7's gate is a record-presence
  backstop (msq_instr_in_stem flag in the sidecar, same pattern as G-UNIQUE); audit.py
  (A-MSQ-INSTR) re-checks the docx Q.N line directly when run. Fix by re-emitting
  the stem with the instruction appended to the Q.<N> line (never as its own paragraph).

  v5.0 adds 2 new gates (→ 65), Issue 2b, enforced per-batch (S4-11) and in the
  S13-2 sweep. Both DORMANT when their manifest structure is empty (no false stop):

  | Gate Code      | Checks                                                         | Fix? | Fix                                              |
  |----------------|---------------------------------------------------------------|------|--------------------------------------------------|
  | G-GROUPMANDATE | ≥min members of each manifest.mandatory_groups group generated | YES  | Regenerate so ≥min members appear (Step 1 M4)    |
  | G-MINCOUNT     | ≥k generated questions for each manifest.min_counts id          | YES  | Regenerate to reach k (Step 1 M6)                |

  G-GROUPMANDATE (definition): exam-agnostic post-gen backstop to S3-17 CHECK 3, mirroring
  G-ALTGROUP. Reads manifest.mandatory_groups {group:{members:[ids],min}} and the per-
  subtopic_id counts from the mock's concept_map (the SAME generated-reality counts
  G-ALLOC-SUBTOPIC uses). A group with fewer than `min` members carrying ≥1 generated
  question fails. Expresses "≥1 of a subtopic GROUP per mock" (e.g. any one member of a
  solid-geometry group) — which mandatory_every_mock cannot, since it would force ALL
  members. No subtopic name hardcoded; empty mandatory_groups ⇒ pass.

  G-MINCOUNT (definition): exam-agnostic post-gen backstop to S3-17 CHECK 4. Reads
  manifest.min_counts {id:k} and the same per-subtopic_id generated counts; an id with
  fewer than k generated questions fails. Expresses "≥k Q of this subtopic per mock" —
  the generalisation of mandatory_every_mock from ≥1 to ≥k. No name hardcoded; empty
  min_counts ⇒ pass. DELIBERATELY there is NO companion cadence gate: manifest.
  cadence_windows ("≥1 every N mocks") is a CROSS-mock constraint, unobservable from one
  mock, and is enforced solely by Step 1 RULE M5 (full-series pass). Adding a Step 7
  cadence gate would false-stop every legitimately-skipped mock.

  v5.18 adds 1 new gate (→ 67), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code | Checks                                                        | Fix? | Fix                                     |
  |-----------|---------------------------------------------------------------|------|-----------------------------------------|
  | G-PREQ1   | No non-blank paragraph before Q.1 (title/info/scoring/cover)  | YES  | Delete the pre-Q.1 paragraphs from docx |

  v5.19 adds 1 new gate (→ 68), per-batch (S4-11 fallback) + audit.py A-MATCH-TABLE:

  | Gate Code     | Checks                                                        | Fix? | Fix                                        |
  |---------------|---------------------------------------------------------------|------|--------------------------------------------|
  | G-MATCH-TABLE | Every match question renders its List columns as a real table | YES  | Re-emit via add_match_table() (§10-S10-3M) |

  G-PREQ1 (definition): the generated paper is questions-only at the DOCUMENT level — the
  first non-blank body paragraph must be the bold "Q.1" stem. Any title, "Total Questions /
  Maximum Marks / Time" line, "Each question carries ... Negative marking ..." instruction, or
  cover/preamble before Q.1 → Exit 1 (R8b). CATEGORY-C values (marks_per_q, time_per_q_sec,
  negative_marking, options_count, total_questions) are structured metadata in section_rules.md
  / blueprint.json / registry and are NEVER printed in the paper; a downstream platform may
  render them from that metadata. Blank separators before Q.1 are ignored. DORMANT only if
  section_rules.md EXAM_STRUCTURE declares paper_header_block (a deliberate per-exam opt-in; no
  current exam declares it). Independently re-verified by audit.py A-HEADER (which strips the
  block rather than validating it).

  v5.70 adds 1 new gate (→ 69), enforced per-batch (S4-11) and in the S13-2 sweep:

  | Gate Code      | Checks                                                          | Fix? | Fix                                          |
  |----------------|-----------------------------------------------------------------|------|----------------------------------------------|
  | G-MATH-RESIDUE | No ASCII-dialect math residue (flat/half-Unicode subscript, caret, ÷, flat radical, letter fraction, accents, delimiters, empty OMML) in any stem/option | YES  | Re-emit via render_mock_text ⟦MATH:…⟧ (S10-4) |

  G-MATH-RESIDUE (definition): see §12 S12-NEW-30. The 'blocking' list of
  mock_math_residue_check() must be EMPTY before every present_files (per batch
  AND at Final Assembly); the 'amber' list (t3 compile fallbacks) routes to the
  F1 AMBER footer. Engine twin: audit.py A-SUBFLAT (audit_canonical v2.17).

# ════════════════════════════════════════════════════════════════════════
# §19 — EDGE-CASE CHECKLIST (v2.0 — additions marked *)
# ════════════════════════════════════════════════════════════════════════

  All items from v1.0 + these additions:

  BATCH ENFORCEMENT (§4 v3.0 — most critical):
  □ ONE batch = ONE response (never two batches in one response)  **
  □ Each non-final batch ends with "Type 'continue' to begin Batch [N+1]."  **
  □ Each non-final batch response ENDS after the continue prompt (S4-7 STEP F)  **
  □ No batch was auto-advanced within the same response (B-4)  **
  □ Every batch generated exactly q_count Qs from batch_state.json (B-3)  **
  □ No batch spanned two sections (S4-1)  **
  □ Q-range read from batch_state.json, never from memory (B-2)  **
  □ Pre-batch self-check (S4-5) performed before each batch  **
  □ Only the user's "continue" started each next batch (B-5)  **
  □ Final batch auto-ran Final Assembly, no continue prompt (S4-9)  **
  □ batch_state.json updated after each delivery (S4-8a)  **
  □ Manual gate checklist completed per batch (if no audit.py) (S4-11)  *

  FONT:
  □ All text uses configured font (FONT_NAME, FONT_SIZE_PT)  *
  □ Stems: configured font, configured size, bold  *
  □ Options: configured font, configured size, normal  *

  OPTIONS:
  □ Labels match OPTION_LABEL_FMT (configured format)  *

  STRUCTURE:
  □ No section headings in docx body  *
  □ No title/info/scoring/cover block before Q.1 — first non-blank paragraph is "Q.1" (R8b, G-PREQ1)  *
  □ No answer key page at end of docx  *
  □ No figural text placeholders  *

  FIGURAL (v5.13 — R-FIGURAL / §10-S10-7/S10-8/S10-8A):
  □ Each figural Q correctly structured per its image_role:
    stem_and_options → problem PNG(s) + option PNGs (add_figural_question)
    stem_only → problem PNG(s) + text options (add_figural_stem_question)
    options_only → text stem + option PNGs (add_figural_question, empty problem)  ****
  □ Options single-column — one option image per line, never two on a line  ****
  □ Each option image bound 1:1 to its "i." label; no "1. Figure 1" dummy text  ****
  □ No composite panel (problem + options fused into one image)  ****
  □ No stem/caption/option-number baked into any raster (intrinsic figure
    annotations like M/N, vertices, axis labels are allowed)  ****
  □ Reference lines (mirror line MN, number line, axis) drawn as real geometry  ****
  □ All option images 300 DPI, lossless PNG, uniform square canvas  ****
  □ G-FIGURAL-COMPOSITE passes at batch and Final Assembly  ****

  ALLOCATION COUNT + SCENARIO UNIQUENESS (DOUBT-3 — both rules, v3.2):
  □ Each subtopic has EXACTLY its blueprint q_count — floor and ceiling (RULE A)  ***
  □ No two questions in the mock share a scenario_key (RULE B)  ***
  □ No scenario duplicated by changed values, names, or reworded text  ***
  □ Subtopics allocated 2+ Q use a DISTINCT scenario for each question  ***
  □ N>distinct-PYQ-patterns handled by inventing new distinct scenarios (no cap)  ***
  □ scenario_key uniqueness is mock-global (also across different subtopics)  ***
  □ concept_ledger in batch_state.json reflects every accepted Q's scenario_key  ***
  □ G-CONCEPTDUP, G-ALLOC-SUBTOPIC, G-COUNT-X-UNIQUE all PASS at Final Assembly  ***

  MANDATE COMPLIANCE (exam-agnostic — v5.0; no subtopic names):
  □ Every manifest.mandatory_every_mock id present in this mock (S3-17 + G-ALLOC-SUBTOPIC)  *
  □ ≤1 member of each manifest.alternation_groups group in this mock (S3-17 + G-ALTGROUP)  *
  □ Cross-mock variant rotation honored where a ROTATION cycle is declared (S6-9)  *
  □ (Issue 2b) ≥min members of each manifest.mandatory_groups group present (S3-17 CHECK 3 + G-GROUPMANDATE)  *
  □ (Issue 2b) ≥k questions for each manifest.min_counts id (S3-17 CHECK 4 + G-MINCOUNT)  *
  □ (Issue 2b) cadence (≥1 every N mocks) enforced in Step 1 RULE M5 — NOT gated here (cross-mock)  *

  REGISTRY:
  □ pending_registry initialised at S3-4 session start  *
  □ content_tracking, image_phashes, session_log initialised at Mock 1  *
  □ No registry writes during generation (only pending_registry)  *

  TECH STACK:
  □ Python + python-docx used (not npm docx) for math-containing sections  *
  □ OMML used for all fractions/surds/exponents (not slash/caret notation)  *
  □ DI table uses Word table XML (not pipe-delimited plain text)  *


# ════════════════════════════════════════════════════════════════════════
# APPENDIX A — AUDIT SCRIPT BOOTSTRAP (GAP-01 permanent fix)
# ════════════════════════════════════════════════════════════════════════
#
# v5.11 NOTE: Step 6 (MockBlueprint) v1.20+ now AUTO-GENERATES this script
# as its 6th output file. Users no longer need to create it manually.
# See Framework_Blueprint.md §13-7A for generation rules, collision handling,
# upgrade path, and lifecycle.
#
# CANONICAL AUDITOR — SINGLE SOURCE OF TRUTH (v5.17)
# ────────────────────────────────────────────────────────────────────────
#   The canonical auditor is NO LONGER a separate "minimum-viable" script embedded here.
#   The ONE canonical, exam-agnostic auditor is the repo engine file
#       audit_canonical.py   (hash-tracked; formerly the retired CreateAudit Appendix A)
#   and it is the ONLY auditor the pipeline generates or runs. It carries the full A-*
#   gate catalogue, the --audit-state COMPLETION GATE (S5-1A, C1-C7 + on-disk evidence
#   checks), and a FIXTURE-BASED self-test (builds tiny docx fixtures; asserts each gate
#   CATCHES a planted defect and PASSES a clean one; SELF-TEST: N/N with N >= 35 — the
#   canonical build self-tests 107/107).
#
#   RETIRED (do NOT generate, copy, or use): the old 13-gate "minimum-viable" embedded
#   script whose self_test() was a CONSTANT print ("SELF-TEST: 13/13 PASS") that executed
#   NO gate. That hollow stub is exactly what let a truncated/dead auditor pass the P1
#   self-test check and ship a false-clean paper (root cause documented in CHANGELOG.md).
#   It is REMOVED here so it can never be copied again. MVP_GATE_COUNT and the 13-vs-66 two-build split no longer exist.
#
#   HOW THE SCRIPT IS BORN (Step 6 B3 — Framework_Blueprint.md §13-7A):
#     B3 writes [ExamCode]_mock_test_audit.py by copying, VERBATIM, the repo engine
#     file audit_canonical.py (hash-tracked + bootstrap-verified; the single source of
#     truth since 2026-07-31 — formerly a fenced python block in the retired
#     CreateAudit spec). No exam-specific edits are
#     needed — the script parameterises itself from blueprint.json / section_rules.md /
#     subtopic_manifest.json / registry.json at runtime. B3 then VALIDATES:
#         python3 [ExamCode]_mock_test_audit.py --self-test
#       → MUST print "SELF-TEST: N/N PASS" with N >= 35 AND be fixture-based.
#         A constant-print "N/N PASS" (no fixtures) is REJECTED → regenerate.
#
#   STEP 7 (this spec) still uses audit.py OPTIONALLY for its per-batch self-audit; it runs
#   the SAME canonical script (its --self-test and Part-A gates work standalone). If absent
#   → WARN + manual checklist (S4-11), unchanged.
#
#   The full ~1200-line script body is intentionally NOT duplicated here: a SINGLE canonical
#   copy is what prevents the three-way drift (13 / 35 / 66) that this fix eliminates.

# ════════════════════════════════════════════════════════════════════════
# APPENDIX B — M1 DEFECT LOG (permanent record for SSC_CGL_TIER1)
# ════════════════════════════════════════════════════════════════════════
#
# Mock 1 (SSC_CGL_TIER1) was generated in production before v2.0 framework.
# The following defects were confirmed and must be fixed in regeneration:
#
# M1-D01: All 100 questions generated in one response (batch enforcement violated)
# M1-D02: Section headings ("SECTION: General Intelligence...") in docx body — R8 violation
# M1-D03: Answer key page embedded at end of docx — R5/R12 violation
# M1-D04: Font is Arial (not Calibri 11pt)
# M1-D05: Option labels use "(1)" format (not "1.  text" format)
# M1-D06: DI table as plain text pipe-delimited (not Word table XML)
# M1-D07: OMML not used for math (npm docx package used — cannot produce OMML)
# M1-D08: Figural questions delivered as text descriptions
# M1-D09: Direction Sense absent from GIR (MANDATORY every mock)
# M1-D10: Address Matching absent from GIR (MANDATORY every mock, 2025)
# M1-D11: Mensuration 3D absent from QA (MANDATORY every mock)
# M1-D12: Both Simple Interest AND Compound Interest in M1 (alternation violated)
# M1-D13: pending_registry not used — registry written directly during generation
# M1-D14: content_tracking L4-L18 fields absent from registry
# M1-D15: progress.json never written (passage_linked_qs/cloze_linked_qs lost)
# M1-D16: answer_key sidecar JSON never created
# M1-D17: GIR pair rotation (A/B/C) not applied
# M1-D18: Question content visible in chat (print() debug statements — MANDATE 0 violation)
# M1-D19: MANDATE 0 violated (stem text visible in verification output)
# M1-D20: batch_state.json built but not consulted per-batch for gated stops
#
# STATUS: M1 is a known-defective mock. Recommend regenerating M1 with v2.0 spec.
# M2 onwards: follow v3.0 spec. All 20 defects addressed; batch logic hardened.

# ════════════════════════════════════════════════════════════════════════
# APPENDIX C — BATCH PROCESSING QUICK REFERENCE (v3.0)
# ════════════════════════════════════════════════════════════════════════
#
# The one-page summary every Step 7 session must internalise:
#
# 1. SESSION START: run all S3 checks → build batch_state.json →
#    show batch plan → print "Type 'continue' to begin Batch 1." → STOP.
#
# 2. EACH "continue": run S4-5 pre-batch self-check → generate EXACTLY
#    q_count Qs for current_batch (from batch_state.json) → gate check →
#    report → present_files → update batch_state → print continue prompt →
#    *** END RESPONSE ***.
#
# 3. ONE BATCH = ONE RESPONSE. Never two batches in one response.
#    Never auto-advance. Only the user's "continue" starts the next batch.
#
# 4. FINAL BATCH (is_final=True): no continue prompt — auto-run Final
#    Assembly in the same response, then end.
#
# 5. NEVER print question content in chat (MANDATE 0).
#
# 6. audit.py: OPTIONAL to run (manual checklist S4-11 substitutes), MANDATORY to report
#    on. v5.36: it is the pipeline's ONLY machine auditor — if absent → WARN loudly, use
#    the manual checklist, and say in the batch report that no machine audit ran.
#
# THE M1 FAILURE: all 100Q in one response. THE v3.0 FIX: §4 B-4 + S4-7
# STEP F + MANDATE 1 STEP 6 make that mechanically impossible.

# ════════════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════════════
# §S16 — RETIRED (v5.76 — REPAIR-RETIRED-2026-08-27, operator decision)
# ════════════════════════════════════════════════════════════════════════
#   The repair mode this section once defined (the triggers TestCreateRepair /
#   MockCreateRepair, the _Create_Repaired.docx artefact, the pre-repair stem
#   snapshot and its engine helpers) is RETIRED. The difficulty gate
#   (MockTestExplain §7A-M) reports and DISCLOSES; it never blocks delivery and
#   nothing is ever rewritten on its say-so. A session that receives one of the
#   retired triggers replies: "TestCreateRepair / MockCreateRepair are retired
#   (2026-08-27). The difficulty gate no longer blocks — the next step is: " +
#   pp.dg_next_step(reg, paper_id, N, mock=<Mock* trigger>) (after pp.dg_preflight,
#   whose disclosure line is printed if any; the Deliver trigger on any judged
#   paper, the Explain trigger on a PENDING one). Nothing is regenerated.
#   This step writes registry.difficulty_gate ONLY at birth (pp.dg_stamp_pending,
#   Final Assembly); it never touches `status` or `repair_rounds_used`.
#   History of the retired section: SPEC_HISTORY.md (section §S16 archived verbatim) and CHANGELOG.md 2026.08.27.3.


## CREATE-SYL — NEW-CONTENT GENERATION (v5.83 — GAP-2026-09-01 §5.5—§5.8;
## ACTIVE mode only; inactive exams byte-identical to v5.82)

STYLE DONORS (§5.5, strict order): 1 the SECTION's measured mechanic
distribution (a mechanic the section never used is never used); 2 the
section style signature (R9: OUT_OF_SYLLABUS questions DO contribute here
and nowhere content-bearing); 3 the sample paper if present (§4.7) —
above inheritance, below real new-era PYQs; 4 FORBIDDEN: any cross-exam
borrowing (§2.1c). A4 zero-history section (post-HS-ST11 added section):
fall back to the EXAM-LEVEL pooled distribution + signature, disclosed in
the footer ("style donors: exam-level pool — new section has no history");
the same fallback feeds §5.8 Layer 1 for that section.

S7-NEWGEN (§5.6, R8) for every NEW-content question: (a) >= 3 candidates
from the subtopic's syllabus atoms under the §5.5 constraints and the
§5.7 firewall; (b) self-audit each — factually verifiable against
canonical academic consensus; exactly ONE defensible key; written
per-option rationale; distractors are NAMED, REAL misconceptions; no
ambiguity of scope, units, or notation; standard terminology; all house
content rules; (c) best candidate selected, series-level dedup applies;
(d) rationales RETAINED into the explain artefacts. All existing Step 7
gates continue on top; nothing is exempted.

L4 DRIFT FIREWALL (§5.7): every candidate for a RETAINED-subtopic
question is screened via syllabus_provenance.lexicon_screen against the
DELETED-node lexicons OF ITS OWN R34 SCOPE only; a hit => regenerate that
candidate. Legitimate same-term content in another section is never
screened against foreign lexicons.

DIFFICULTY (§5.8): Layer 1 target E:M:H measured on retained subjects of
the SAME section; Layer 2 realization — structural markers measured per
difficulty per section plus the exam-independent cognitive anchor at
exam_config `level` (Easy one step; Medium two steps or close
discrimination; Hard integration of >= 2 concepts / data interpretation /
exception reasoning). Once new-era papers exist, measured NEW-content
difficulty replaces inheritance (R12/R10 cadence).

# END OF Framework_MockTestCreate v6.3
# Version: 5.8 | Date: 2026-07-04
# (Full per-version rationale was RELOCATED 2026-07-31 to CHANGELOG.md, section
#  'ARCHIVE — Framework_MockTestCreate' — that archive is authoritative for history.
#  The v1.0→v3.9 summary below is retained for continuity only.)
# v1.0 → v2.0: 20 production gaps fixed after M1 live failure
# v2.0 → v3.0: definitive batch-processing rewrite (§4); audit.py answer locked
# v3.0 → v3.1: DOUBT-3 intra-mock concept-uniqueness (first pass)
# v3.1 → v3.2: DOUBT-3 allocation-count (RULE A) + scenario-uniqueness (RULE B);
#              10 bugs fixed
# v3.2 → v3.3: DOUBT-3 final hardening — 7 issues fixed (L3 fix, per-Q concept_map
#              persistence, 4 subtopic CLASSES incl. linked-stimulus & vocabulary,
#              cross/intra-mock boundary, resume-safe ledger)
# v3.3 → v3.4: subtopic_id contract (join blueprint↔section_rules by id, §20)
# v3.4 → v3.5: delivery-contract hardening (§13 executable steps; closed 2-file
#              deliverable set; G-DELIVERY-SET; R-DELIVER)
# v3.5 → v3.6: linked-question self-containment (§9 full rewrite; Model A default
#              stimulus-per-member; R-LINKED; G-STIMULUS-ORPHAN; S10-LINKED helper)
# v3.6 → v3.7: Q.N-FIRST block contract — every block opens with "Q.<N>"; linked
#              order = Q.N context → stimulus → ask; R14 generalised; G-QNUM-FIRST
# v3.7 → v3.8: DOUBT-4 presentation-uniqueness — RULE C presentation_key (§6-3c)
#              for CLASS 2/3; CHECK 1b in the generation loop; G-FORMATDUP;
#              R19 anti-clustering. Fixes same-concept clones (Q.77/79, Q.78/80)
# v3.8 → v3.9: v3.8 hardening (deep audit) — 6 integration gaps closed:
#              classify_subtopic()+SUBTOPIC_CLASS populated; menu/family helpers
#              defined; presentation_ledger persisted+resumed; build_question
#              render-consistency + verify_presentation_match; G-FORMATDUP selects
#              by class (missing-key now caught); RULE C requires distinct visible
#              stem_format. No new gate/rule — pure closure.
# Total guard gates: 81 (see the §12 catalogue + §17 DoD, current through v5.70; the
#   per-batch/Final-Assembly gate set — MSQ gates dormant unless multi_present, NAT gates
#   dormant unless nat_present; G-GROUPMANDATE/G-MINCOUNT dormant unless their manifest
#   structure is non-empty; G-PREQ1 dormant only if EXAM_STRUCTURE declares paper_header_block)
# Total rules: R1-R24 (incl. R8b) + R-DELIVER + R-LINKED + R-FIGURAL + R-UNDERLINE + R-OPTREF
#   + R-ANSWER + R-MSQ-ESCAPE + R-MATH-OMML
# Batch enforcement: Layer 1 (spec STOP, no audit.py needed) + Layer 2 (audit.py)
# Zero hardcoded exam values
# ════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════
# §20 — SUBTOPIC_ID CONTRACT (v3.4 — joiner role)
# ════════════════════════════════════════════════════════════════════════
#
# Step 7's role in the cross-step contract (full contract authored in Step 0 §15):
#   Step 0 MINTS subtopic_id, publishes [ExamCode]_subtopic_manifest.json.
#   Step 1 CONSUMES it (assigns ids, enforces mandates at build time).
#   Step 7 (THIS step) JOINS blueprint ↔ section_rules ON subtopic_id.
#
# WHAT CHANGED IN v3.4 (and why your M1 hard-stopped before it):
#   The pre-v3.4 checks matched subtopics by display-name string. On SSC CGL T1,
#   ~70% of blueprint names did not match section_rules names (Step 0 and Step 1
#   each derived names independently). So:
#     - S3-8 flagged 144/208 subtopics as "unrecognised" (would generate them
#       with no PYQ guidance).
#     - S3-17 used hardcoded literals ('Mensuration 3D', 'Direction Sense', ...).
#       The blueprint had 3D mensuration under granular names ("Right Circular
#       Cone" etc.), so the literal check FALSELY reported it absent → HARD STOP [HS:PROSE].
#   v3.4 removes string-matching entirely. Joins are by subtopic_id, which all
#   three steps now share via the manifest. False "absent" alarms are impossible.
#
# THE THREE GUARANTEES (why this never breaks again, for 100 exams):
#   1. JOIN BY ID: S3-8 joins blueprint ↔ section_rules on subtopic_id. The
#      display name is decorative; nothing matches on it.
#   2. CONTRACT GATE: every blueprint id must exist in BOTH the manifest AND
#      section_rules, else HARD STOP [HS:PROSE] naming the exact id (no silent Zero-PYQ
#      fallback that would quietly degrade quality).
#   3. MANDATES BY DATA: S3-17 reads manifest.mandatory_every_mock and
#      manifest.alternation_groups (structured data minted by Step 0). Zero
#      subtopic names are hardcoded anywhere in Step 7. Works for any exam.
#
# REQUIRED INPUT (S3-1): [ExamCode]_subtopic_manifest.json must be in the
#   project Files section alongside section_rules.md and blueprint.json. It is a
#   hard dependency; its absence is HS-9.
#
# RELATIONSHIP TO CONCEPT-UNIQUENESS (DOUBT-3, §6/§7): subtopic_id is the
#   cross-step JOIN key; concept_group/scenario_key are the intra-mock UNIQUENESS
#   keys. They are INDEPENDENT by design — a subtopic_id identifies WHICH subtopic;
#   scenario_key identifies WHICH concept within the generated questions. Do not
#   conflate them.
# ════════════════════════════════════════════════════════════════════════
