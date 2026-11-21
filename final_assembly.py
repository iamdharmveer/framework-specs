"""
final_assembly.py — Registry commit / schema-completeness / question-index
certification / pre-delivery checklist for Step 7 (MockCreate/TestCreate)
Final Assembly.

PROVENANCE
    Extracted VERBATIM (semantics-identical, with the explicit deviations
    listed below) from Framework_MockTestCreate.md §13. This closes Finding 0
    of the Mock-10 root-cause gap analysis ("§13 Final Assembly has zero
    engine-file backing, anywhere in the framework") — GAP-2026-08-12-
    FINAL-ASSEMBLY-ENGINE. Follows the precedent already proven out by
    blueprint_core.py / paper_pipeline.py / audit_canonical.py: this was spec
    prose a session had to re-type or faithfully re-derive every single mock;
    it is now importable, routed, self-tested code.

    PRODUCTION HOTFIXES v1.22 / v1.22.1 (eaf40a9, GAP-2026-11-14-FINAL-ROUND-CAP-DEADLOCK — a per-text round budget at
    S13-1B) are superseded by S0-BC: S13-1B / S13-2L chains / S13-2R never run on the normal path, and a paper stranded
    by the old global cap is measured by its settlement batch 'S', which keeps its own round count (self-test
    bv_final_stranded_slot_migrates_and_is_measured — the live SSC_CGL_TIER1 P1 state).

    v1.28.0 — GAP-2026-11-21-MATH-TYPESET + GAP-2026-11-21-FIGURE-NEED (release 2026.11.27; owner decisions OD-P1..
      OD-P5 of 2026-11-21). bv_s3_plans freezes batch_state['math_typeset'] (bc.math_typeset_plan — per SUBJECT, the
      chemistry boundary per item) on a fresh paper; the pre-review gate context gains bc.mt_gate_context (G-MATH-TYPESET
      for a strict item, G-FIG-NEED for every non-inert item — both SOFT); a settled question whose delivered text still
      trips one carries bc.p1_amber_lines; a reviewer job with a non-chemistry problem figure of a non-inert item gets
      bc.BV_BRIEF_REVIEWER_R3_FIG, every other job BV_BRIEF_REVIEWER_R3 byte for byte. A paper begun earlier has no
      'math_typeset' and finishes exactly as it began. No new stop, loop or round.
    v1.27.0 — GAP-2026-11-20-RUNG3-BIND-DEADLOCK (release 2026.11.26; owner decision OD-2026-11-20). bc_bind_batch
    (STEP A3) refuses a figure only on the rung-3 TEXT fallback (bc.bc_is_text_fallback, F1) — a text / figure rebuild
    and an R5b figure version bind; its refusal names STEP A2 as the repair. bv_batch_step (STEP A2) treats a decided
    fallback that still carries a figure as OPEN (bc.bc_fallback_figure_open — an earlier batch's question too) and
    decides it again in the same step, so the bounded repair of bc.bc_apply (F9: REWRITE without the figure, then R5b,
    else kept + disclosed with its figure record put back) is always issued before STEP A3. Self-test gap1120_* (5).
    v1.26.0 — GAP-2026-11-19-S13-2F-LOOP + GAP-2026-11-19-FIGURE-LOSS (release 2026.11.25). bv_batch_step: in a
    count-free mode the ENGINE writes difficulty_obs (bc.difficulty_obs_engine_record; the worker's record archived as
    difficulty_obs_author, its moves kept as author_moves); the gate context carries the slot's planned shape
    (G-SHAPEPLAN) and the question's FigureSpec records (G-FIG-SCALE); a granted figure slot that settles as the TEXT
    fallback re-grants its figure to the first capable unwritten slot (bc.figure_regrant; NEW bv_figure_capable_qs for a
    plan frozen earlier). NEW bc_last_batch_route / bc_last_batch_apply — the last batch's whole-paper decision
    (disclose a composition shortfall, re-open drift and item gates; LAW-BC-6 amended). QINDEX_V589_FIELDS carry
    difficulty_mode and shape_drift (A-QINDEX check 9 reads the mode).

    v1.24.1 — GAP-2026-11-15-RUN-ANALYSIS second pass (release 2026.11.20). NEW bc_stimulus_fill: a stimulus-set
    member's reviewers and adjudicator read the set's registered stimulus; the pre-review 'shown' cue needs a picture
    noun; pre-review skips a text that already has reviewer results (NEW bc_text_has_results); only offsets a paper
    measured itself seed the next paper.

    v1.24 — GAP-2026-11-15-RUN-ANALYSIS (release 2026.11.19; owner go-ahead 2026-11-15). bv_batch_step: STEP A2
    PRE-REVIEW (NEW bc_prereview_gaps — figure proof, List-I / 'shown' packet gaps, the auditor's item and AMBER findings
    from <exam>_M<n>_batch_findings.json) holds the jobs and sends the gaps back, at most bc.BC_PREREVIEW_TRIES per rung;
    the batch figure proof is the S13-2P rule (NEW bc_figure_with_layout computes the 2-D layout); author offsets start
    from earlier papers (NEW bc_registry_author_offsets); reviewer jobs use review_qs_per_job_fallback when the run
    recorded no lean sub-agents (NEW bv_review_qs_per_job).

    v1.23 — GAP-2026-11-14-SPEED-AND-FIDELITY (release 2026.11.17; owner go-ahead 2026-11-14). bv_batch_step sizes
    each round's reviewer jobs so they and the round's adjudicator jobs fit in ONE wave (P1, bc.bv_round_job_caps);
    before a text's first review round the author's own counts must give the slot band (P3, bc.bc_selfcount — a miss is
    sent back with no job written, at most bc.BC_SELFCOUNT_TRIES times per rung); difficulty_state.author_offset is
    written every step (P4, bc.bc_author_offsets). NEW bc_fallback_clear_figure (C3): the rung-3 TEXT fallback loses
    its fig_manifest record at REWRITE (kept; NEW bc_fallback_restore_figure puts it back when R5b restores an earlier
    figure version; an R10 family-engine item keeps its figure); bc_bind_batch refuses a fallback that carries a picture
    and clears a leftover record. C4: a step that asks for text work (rewrite / permute / restore / self-count) writes no
    job — the next step issues the whole round together (before 1.23 a rewrite asked beside JOBS OUT could be skipped).

    v1.22 — GAP-2026-11-14-BATCH-COMPLETE (release 2026.11.16; OD-2026-11-14 R1–R13). bv_batch_step drives
    blueprint_core.bc_apply: every question of the batch is settled or disclosed IN its batch — adjudicator jobs
    ('<q>_adj' folders), re-key / option swap / R5b restore actions, a round budget (R11), NO-MODEL with saved state
    instead of INFRA-CARRY (LAW-BC-9); earlier unsettled questions (migration, bc_reopen) join the batch; final=True is the
    settlement batch 'S' of a migrating paper. NEW bc_bind_batch (STEP A3), assemble_final_docx + bc_check_bound (S13-1),
    bc_reopen, bc_figure_intrinsic. QINDEX_OP_FIELDS carry bc_fallback.

    v1.21 — GAP-2026-11-13-STEP7-SPEED (release 2026.11.15). bv_batch_step settles every question INSIDE ITS OWN BATCH
    (defer=False: a rewrite, an edge re-count or a missing role gets its next round at once; the only carry is
    INFRA-CARRY after bc.BV_MAX_ROUNDS); reviewer jobs split per SESSION_BUDGET.json review_qs_per_job; a re-ask goes to
    a '_switch' folder (another model); paper_in_progress (Create S3-13 / S3-16 RESUME); bv_budget_value.

    v1.20 — GAP-2026-11-14-CARRY + FINAL-COUNT (release 2026.11.14). bv_batch_step carries a question rewritten (or
    held for its edge re-count) in its batch to the NEXT batch's first reviewer round (batch_state['bv_carry']; no
    extra round inside a batch); final=True (Create S13-1B) measures every unsettled question before the review.

    v1.19 — GAP-2026-11-13-DIFFICULTY-RUBRIC (release 2026.11.13). No fresh reviewer is never a stop (S0-BV BV-11):
    the question is carried unlabelled; each reviewer's grade is the band blueprint_core v2.3 computes from its counts.

    v1.18 — GAP-2026-11-12-BATCH-SPEED + RULER-ANCHORS (release 2026.11.12). bv_batch_step writes at most 3
    REVIEWER jobs per round for the whole batch (blueprint_core.bv_reviewer_jobs), each packet carrying every
    question's own past-question anchors and the band guide; a reviewer's result is split per question
    (bv_split_reviewer_result); asked-twice roles are not re-asked (a rewrite clears the count: it is per content); the mis-written 'bc.manifest_hash' key is fixed.

    v1.17 — GAP-2026-11-11-NONORGANIC-MOCK-FIDELITY (release 2026.11.11). QINDEX_NF_FIELDS (subject, part, mip,
    given_in_stem, measured_axis2, text_fingerprint, stem_text, option_texts, manifest_hash) carried when present;
    the question_index entry records nf_disclosed {gate: reason} and manifest_hash.

    v1.16 — GAP-2026-11-10-ORGANIC-QUESTION-PARITY + DIFFICULTY-INTEGRITY (release 2026.11.10). qindex_cert
    gains framework_release (bc.OP_RELEASE) — every audit of a paper at or after FRAMEWORK_RELEASE_STRICT judges its
    labels LB2-strict; QINDEX_OP_FIELDS carries the generated-item records (organic flag, chain, decisions,
    grades, key votes, clone check, stereo elements, figure proofs, last resort) when present;
    paper_parity_gate (LAW-ORG-11) and paper_figure_proof_gate (LAW-ORG-8) are the assembly checks S13-2L runs.

    v1.15 — GAP-2026-11-08-DR3-QINDEX-CONFLICT (release 2026.11.09, OD-2026-11-09). QINDEX_V589_FIELDS
    carries 'slot_chain' — present ONLY on an item delivered DISCLOSED (its quality chain proven exhausted,
    Create S13-2L) — so the final S13-4c audit re-derives the disclosure from the REGISTRY alone (a resumed
    session without the sidecar) instead of failing that item. Additive; an item without it is unchanged.

    v1.14 — GAP-2026-11-05-DIFFICULTY-FIDELITY Part D. commit_registry accepts
    difficulty_state=None and, when a dict, commits it on the question_index entry beside
    quality_readiness (Create S3 / S13-6 record it; MockDeliver 3f' reprints the AMBER
    difficulty disclosure lines from it). Additive; an older caller is byte-identical.

    v1.13 — GAP-2026-11-04-STEP7-CONTRACT-RESTORE (owner decisions D0, D3 (a), D6).
    THE STEP 7 USER CONTRACT IS EXACTLY TWO FILES (STEP_CONTRACTS.json). (a)
    predelivery_checklist check 6: the closed set is ALWAYS {Create.docx, registry.json};
    `extra_deliverables` is still ACCEPTED as a keyword (every call site compiles) but no
    longer widens the set — the repo auditor / an amended blueprint are never delivered to
    the exam user (D3 a; disclosed by an informational footer line). (b) NEW pure
    outputs_to_clear(staged, ...): the files THIS paper's run staged in outputs that are
    not deliverables (per-batch Q1to[K].docx, a legacy review packet / verdict file, an
    auditor or blueprint copy, any internal sidecar) — S13-7 removes them BEFORE the
    checklist, so check 6 passes with no manual step (GAP A8; the 2026.11.03 packet left in
    outputs made S13-7 HARD STOP "move internal files back"). Files of OTHER papers/steps
    in the same chat are not this run's and are never touched.

    v1.12 — GAP-2026-11-03-QUESTION-AND-OPTION-QUALITY (OD-13 (i), OD-10 (a), G12).
    (a) G-MEDIAREUSE at commit: the incident docx embedded ONE media part under Q12 and
    Q36 and one under Q24 and Q38 (byte-identical PNGs for two different questions).
    commit_registry now runs bc.media_reuse_check over fig_manifest image_hashes per
    question (linked sets exempt) and REFUSES the commit with the ladder message
    ("LADDER-REPAIR R2 G-MEDIAREUSE ...") in the same {'ok': False, 'fails': [...]}
    shape as the FK gate — the S13-4 caller repairs the later item and re-commits; the
    run never stops. (b) qindex_cert carries producer_release = bc.QQ_RELEASE (OD-10:
    new gates apply only to papers whose entry carries >= the new release; older
    entries audit AMBER). (c) QINDEX_V590_FIELDS — option_identities, entities, shape,
    fingerprint, distractor_mechanisms, stem_leak, consist, stereo_decl, review,
    quality_status — carried concept_map -> question_index when present, so Explain /
    Deliver / the auditor READ verdicts and never recompute them differently (§4.3).
    v1.11 — GAP-2026-11-02-QUESTION-AND-FIGURE-FIDELITY P2/P3. predelivery_checklist
    accepts `extra_deliverables`: a CONDITIONAL addition to the closed set, used only for
    the in-run blueprint when it differs from the project copy (S3-2D recomputation / R5
    amendment — "UPLOAD THIS BLUEPRINT TO THE PROJECT BEFORE THE NEXT PAPER") and the
    per-exam auditor when the run audited with the verified repo copy ("UPLOAD THIS
    AUDITOR TO THE PROJECT"). An extra must be a blueprint or the per-exam auditor by
    NAME; anything else is refused (closed set unchanged otherwise).
    v1.10 — GAP-2026-11-01 final review (same release). (a) Every figure record commit_registry
    writes is STAMPED record_schema='F2'; annotate_legacy_figure_records() annotates only
    UNSTAMPED entries, so a current paper's false record can never be laundered into
    "legacy" by the S13-REGCHECK migration that runs right after its own commit — it
    FAILS A-FIGTYPE-KIND. (b) E15: a question authored pre-v5.88 and resumed across the fix
    carries record_integrity='legacy_unlabelled' (set by MockTestCreate S4-12); it commits
    with object_type='legacy_unlabelled', carried into the entry's record_integrity, and is
    disclosed rather than refused. (c) figural_present_derived is the manifest's truth
    alone (declared True + empty manifest now reads derived False). (d) migration: roles
    'problem:N' checked, string FIGURAL counts tolerated, mocks_completed-only registries
    (axis1_paper keyed by ordinal) get absent_legacy too.

    v1.9 — GAP-2026-11-01-FIGURE-TYPE-COVERAGE-AND-RECORD-INTEGRITY, LAW F3 MANIFEST-
    COMMIT-LAW + F2.3 (paired with MockTestCreate v5.88, ScopedBlueprint v1.11.0,
    audit_canonical v2.32, blueprint_core v1.28, corpus_io v1.16, paper_pipeline
    v5.40, figure_types v1.0). commit_registry gated the rc / di / figural manifest
    blocks on the blueprint's passage_present / di_present / figural_present flags.
    ScopedBlueprint inherited those flags from exam_config with default False (no step
    writes them), so every scoped paper of the reference exam — 18 FIGURAL allocations
    per paper — committed NO figure record: no object_types (A-FIGPROFILE dormant), no
    figure_specs (every v5.33+ figure gate downgraded to legacy AMBER), no
    semantic_objects (Step 9 §13-2b blind). Six of 21 scoped papers; all audited green.
    (1) COMMIT ON EXISTENCE: a manifest block is written whenever its manifest is
        non-empty, REGARDLESS of the flag. The flags stay informational. When a flag is
        False while its manifest is non-empty, the disagreement is RECORDED in
        registry.paper_flags[paper_id] (the derived truth beside the declared flag),
        printed once, never hidden. A legacy registry (flag True, manifest given)
        commits byte-identically to v1.8.
    (2) F2.3 object_types MANDATORY on a paper with figures: a fig_manifest question
        without object_type raises at commit (closes the label-omitted variant V3 — 6
        papers audited green with no record of what their figures were).
    (3) annotate_legacy_figure_records(registry): the forward-only migration run by
        S13-REGCHECK — a figure record whose object_type kind disagrees with its
        semantic object is annotated record_integrity='legacy_label_mismatch'; a REACTION
        object without '>>' is 'legacy_degenerate_reaction'; a completed paper with
        FIGURAL>0 in axis1_paper and no figure record gets paper_flags[pid]
        figure_record='absent_legacy'. Nothing is rewritten or deleted; the Deliver
        footer discloses each annotation (DeliveryFooter §FOOTER-DG precedent).

    v1.8 — GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC (paired with MockTestCreate
    v5.86, MockTestExplain v1.51.1, audit_canonical v2.31). The registry is SHARED by
    every series (MOCK, SUBJ, TOPIC, SUBTOPIC), and two writes here still keyed a
    paper by its run ORDINAL N. (1) rc/di/figural manifests were replaced by
    `mock != N` and carried no paper_id: committing SUBJ:X:01 deleted MOCK:M01's
    manifest (and vice versa). Now replace-by-paper_id with `paper_id` on every new
    entry; a legacy entry without one belongs to MOCK:M<mock>. (2) The same-slot
    rule (_stale_sibling, the papers_completed filter, _commit_problems,
    _duplicate_commit_problems) compared the ordinal N, but on a RESUMED scoped
    series mocks[].mock restarts at 1 while paper_id carries paper_start+k:
    committing SUBJ:U:11 (ordinal 1) erased SUBJ:U:01 from papers_completed,
    question_index and session_log (measured). Now the slot is the PAPER NUMBER
    parsed from paper_id (_entry_number); the ordinal is used only for a legacy or
    unparseable id, so the renamed-paper_id case behaves exactly as before. MOCK
    series: number == ordinal, so a mock-only registry commits exactly as before
    except that new rc/di/figural manifest entries also carry "paper_id".
    v1.7 — GAP-2026-09-21-LINKED-PLACEMENT (paired with MockTestCreate v5.85,
    audit_canonical v2.30, blueprint_core Cluster SG). commit_registry's
    question_index entry carries `stimulus_group_id` ONLY when the concept_map entry
    has the key (a set-placed paper) — a legacy paper's entry is byte-identical.
    v5.60 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (paired with MockTestCreate v5.73,
    MockTestExplain v1.46.0, MockDeliver v1.16.0, DeliveryFooter v1.27,
    paper_pipeline v5.74 Cluster RH, explain_engine v2.9). Operator decision
    2026-08-26: the Tier-A audit dossier is NOT a deliverable. predelivery_checklist
    now treats `_audit_dossier.json` as an internal sidecar (check 5) and the closed
    set is ALWAYS {Create.docx, registry.json} (check 6). Additive; no commit,
    regcheck or qindex logic touched.
    v5.58 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER (paired with paper_pipeline
    v5.71 Cluster DG, MockTestCreate v5.71, MockTestExplain v1.44.0, MockDeliver
    v1.14.0, DeliveryFooter v1.25, audit_canonical v2.18 A-DGATE). The v5.56 PENDING
    stamp was an inline dict literal — one of THREE hand-writers of
    registry.difficulty_gate across two specs and this engine, with no legal-state
    table and no write guard. Its own comment ("never edited elsewhere") was false:
    the (since retired) repair step added rework_stem_hashes, and one of its sessions
    also set repair_rounds_used=1 on a still-FAILED record, deadlocking four triggers.
    FIX: the stamp is now pp.dg_stamp_pending — the single CREATE path. Second
    defect closed here (gap G-4): the stamp had no mock-vs-scoped condition, so
    EVERY scoped paper was born PENDING while §7A-M is MOCK-ONLY and could never be
    delivered. A scoped paper_id is now born DORMANT/scoped_paper (a legal, terminal,
    deliverable state) and a mock is born PENDING exactly as before. Fixtures pin
    both births, the legal-state check and the shape (schema 2, no bands on birth).
    Also hosts the fleet scanner/healer CLI (--dg-fleet-scan ROOT [--apply]): the
    thin core may not perform file I/O (CHECK AB), and this engine already imports
    paper_pipeline and is routed only where paper_pipeline is (CHECK AI).

    v5.57 — GAP-2026-08-24-AXIS-PAPER-SERIES-COLLISION (paired with MockTestCreate
    v5.68, audit_seam v1.2). THE SECOND INSTANCE OF THE v5.56 CLASS, found by the
    cross-step field-contract sweep and confirmed by execution: axis1_paper /
    axis3_paper were written as reg['axis1_paper'][str(N)] — the paper ORDINAL — on a
    registry SHARED across series. Measured: Mock 1 commits {'1': {...TEXT 8}}, then
    SUBJ:PHYS:01 commits and the mock's snapshot is GONE; two SCOPED series collide
    with each other the same way (SUBJ:PHYS:01 then SUBJ:CHEM:01 leaves only the
    second). Nothing reads these snapshots back today, so no run breaks and no wrong
    paper ships — but the field's WHOLE PURPOSE (v5.49, GAP-2026-08-12-AXISPAPER-
    HISTORY) is to be a historical LEDGER; that release's own note says the pre-v5.49
    field "was a rolling snapshot, not a ledger", and on any exam mixing mocks and
    scoped papers it silently became one again. FIX: identical to v5.56 —
    [paper_id] is the AUTHORITY for every series; the legacy [str(N)] key is written
    for the MOCK series ONLY (pre-v5.57 readers of a mock registry see exactly what
    they always saw) and NEVER for a scoped paper. GATE: audit_seam v1.2's KEY-SHAPE
    check now fails the build on any ordinal-only per-paper container, so the class is
    machine-checked rather than swept for.

    v5.56 — GAP-2026-08-24-OPTIONS-BY-Q-SERIES-COLLISION (paired with MockTestCreate
    v5.67, MockTestExplain v1.41.0, audit_canonical v2.16). regcheck() wrote
    registry['options_by_q'][str(N)] — keyed by the paper ORDINAL. The registry is
    SHARED across series (ScopedBlueprint §9), so MOCK:M01 and SUBJ:PHYS:01 both
    landed on key '1' and the later commit silently overwrote the earlier map;
    Step 9 on the overwritten paper then hard-stopped at parse_paper ('Q1 has 4
    options, expected 0') or, on an overlapping shape, mistyped NAT questions with
    NO error. MEASURED by the Step-9 dry-run harness (scenario S9/S9b). Every other
    per-paper field (key_commitments, question_index, papers_completed) had been
    re-keyed by paper_id at v5.54/v5.55; options_by_q was the one left behind.
    FIX: options_by_q[paper_id] is now the AUTHORITY, written for every series; the
    legacy options_by_q[str(N)] is still written for the MOCK series only (so a
    pre-v5.56 reader of a mock registry sees exactly what it always saw) and is
    NEVER written for a scoped paper (the collision path). Readers (Step 9 P3,
    audit_canonical load_sources) look up paper_id first, str(N) second.

    v5.55 — GAP-2026-08-21-EXPLANATION-PROVENANCE (paired with MockTestCreate v5.59,
    paper_pipeline v5.39, explain_engine v2.8). commit_registry() now also writes
      * registry['key_commitments'][paper_id]  — salted sha256 of every canonical
        answer (paper_pipeline.seal_key_commitments), built from the answer_key
        sidecar passed as `answer_key`; the plaintext never enters the registry.
        Step 9 re-derives, hashes its OWN answers and compares — the Q47 class
        (Step 7 key 2, Step 9 published 1, nobody compared) cannot recur silently.
      * figural_manifests[].semantic_objects {q: [obj, ...]} — what each figure
        DEPICTS in machine-readable form (fig_manifest questions[q].semantic_objects),
        shape-validated through paper_pipeline.validate_semantic_object.
    Both are ADDITIVE registry fields; an older registry without them is read
    unchanged by every consumer (EC-V18). regcheck() requires key_commitments for
    the paper being committed when an answer_key was supplied.

    Source anchors (Framework_MockTestCreate.md, pre-extraction v5.52.0):
      commit_registry ......... §13 S13-4  (registry update protocol)
      regcheck ................ §13 S13-REGCHECK (schema completeness + G-COMMIT-COMPLETE)
      qindex_certify ........... §13 S13-QINDEX (G-QINDEX, delegates to
                                  paper_pipeline.validate_question_index — see
                                  DEVIATION 3 below)
      predelivery_checklist .... §13 S13-7 (the 7-point pre-delivery gate)

WHAT IS DELIBERATELY NOT HERE (scoping — GAP-2026-08-12-FINAL-ASSEMBLY-ENGINE
scoping document, §1): S13-1/S13-2/S13-3/S13-5 are stub headers in the spec
with no body — nothing to extract. S13-4b (Tier-A dossier)/S13-4c
(dossier-fed re-sweep) are about invoking an external subprocess (the
per-exam audit_canonical.py copy), a different concern from registry/gate
logic — left spec-inline. S13-6/S13-8/S13-9 are narrative/delivery mechanics
with no executable logic. §14 (registry schema documentation) is untouched;
Check U in validate_framework_md.py reads it as prose/JSON documentation,
independent of where the producer code lives.

DELIBERATE DEVIATIONS from the spec-inline code (each one is a design
decision recorded in the scoping document, not an accident):

  1. EVERY function here is PURE — no file I/O, no mutation of its inputs
     (registry/pending are deep-copied before any write). The spec-inline
     code did its own json.load/json.dump inline; callers now do that, and
     pass data in. This is what makes every function trivially unit-testable
     without touching disk, and is why this module does NOT claim THIN-CORE
     purity in validate_framework_md.py's Check AB — predelivery_checklist's
     entire job is checking a real directory, which cannot be made pure, so
     honestly classifying this module as "does real I/O, like
     audit_canonical.py" (not like blueprint_core.py) is the correct
     boundary, not a compromise.

  2. ALL FOUR functions return a result dict shaped
     {'ok': bool, 'fails': [...], ...}; none of them raise SystemExit. The
     spec-inline code raised directly. The CALLER (Framework_MockTestCreate.md
     §13, post-extraction) does `raise SystemExit(...)` on `not result['ok']`
     — same hard-stop trigger conditions, equivalent wording, but the
     decision logic is now testable without catching SystemExit, and
     commit_registry's FK-check failure has somewhere to attach (an earlier
     draft of the design that let commit_registry return a bare registry
     dict was caught, by adversarial review, as a real defect: there would
     have been no way to represent "the FK check failed" at all).

  3. qindex_certify() DELEGATES to the pre-existing
     paper_pipeline.validate_question_index() rather than re-implementing
     G-QINDEX's 6 checks a fifth time. That function is already logically
     identical to G-QINDEX/1-6 (confirmed by direct comparison) and is
     already parity-tested against audit_canonical.py's gate_qindex() in
     that module's own self-test ("QINDEX PARITY"). Reusing it here is the
     repo's own established pattern for collapsing duplicate copies rather
     than adding a new one. ONE observable, deliberate, disclosed behavior
     change results: paper_pipeline's check 6 (the difficulty_schedule
     quota) is DORMANT (not evaluated) when an exam's blueprint declares no
     difficulty_schedule at all, whereas the spec-inline check 6 has no such
     guard and would compare a real (non-zero) distribution against an
     all-zero target derived from an empty schedule dict — an unconditional
     HARD STOP on every mock of any exam that omits difficulty_schedule.
     This exam (IIT_JAM_BIOTECHNOLOGY) always declares difficulty_schedule,
     so this changes nothing observable here; for any other exam that
     doesn't, this is a bug fix (a false-positive hard stop removed), not a
     behavior loosening of anything difficulty_schedule actually governs.

  4. commit_registry() makes THREE of its writes properly idempotent
     (replace by an identifying key before append, mirroring the pattern
     question_index already used) where the spec-inline code was NOT
     idempotent: session_log (replace-by-paper_id), mocks_completed /
     papers_completed (append-only-if-absent), and rc_manifests /
     di_manifests / figural_manifests (replace-by-paper_id since v1.8 —
     every new entry carries "paper_id" beside "mock": N; a legacy entry
     without one belongs to MOCK:M<mock>). This directly
     strengthens G-COMMIT-COMPLETE (a retry of the SAME mock can no longer
     itself create a duplicate-but-differently-shaped partial state). The
     remaining ledgers (question_hashes / stem_texts / semantic_tuples /
     semantic_usage / image_phashes / image_sources_used / content_tracking's
     twelve subfields) are cross-mock DEDUP LOGS whose individual entries
     carry no per-mock tag in the current schema — making THOSE idempotent
     would require a schema change, which is out of scope here (per the
     scoping document, §3 item 4). They remain .extend()-based, exactly as
     today: re-running commit_registry for the same mock still duplicates
     THESE specific lists. This is an explicitly named, not a silently
     inherited, limitation.

FIELD-SET FIDELITY: every field name and shape (including options_by_q's
string-keyed {"N": {...}} JSON round-trip shape) is unchanged from the
current schema documented at Framework_MockTestCreate.md §14. No schema
change is bundled into this extraction — Framework_MockDeliver.md,
Framework_MockTestExplain.md, Framework_ScopedBlueprint.md, and
audit_canonical.py all depend on this exact shape.

NOTE ON `framework_repo_commit`/`spec_source_report` (commit_registry's two
provenance kwargs): these are optional, additive-only fields — when supplied,
they're stamped onto the new question_index entry's qindex_cert and the new
session_log entry (per the original Finding-0 scoping recommendation); when
omitted (the current reality — no §13 call site passes them yet), nothing
changes. Forward-compatible surface, not yet wired to a live value.

v5.54 — TWO DEFERRED DESIGN GAPS CLOSED (each was flagged, documented and
deliberately left out of the earlier hardening releases; each now gets its
own scoped fix):

  A. GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING. question_index/
     session_log deduped by exact paper_id while G-COMMIT-COMPLETE looked
     entries up by mock number — so a paper_id corrected mid-session and
     re-committed left a stale sibling entry (same mock number, old id)
     that no gate could ever see. Fixed on BOTH sides: (prevention)
     commit_registry's dedupe key is widened to SAME-SERIES + SAME-NUMBER
     (`_series_prefix()` — one series holds exactly one paper per number,
     so a same-series entry with this number is by definition the stale
     version of this commit; a same-number entry in a DIFFERENT series,
     e.g. MOCK:M01 alongside SUBJ:Physics:01, legitimately coexists and is
     never touched), and papers_completed drops the renamed predecessor
     (same series, same parsed number, different id — unparseable numbers
     are left alone rather than guessed at); (detection) regcheck() gains
     `_duplicate_commit_problems()` — ≥2 same-series entries for one number
     is a HARD STOP when it is THIS mock's slot, a warning for historical
     mocks, mirroring G-COMMIT-COMPLETE's own fails/warns split exactly.

  B. GAP-2026-08-12-AXISPAPER-PERSISTENCE. The spec's S7-AXIS block wrote
     per-paper Axis-1/Axis-3 snapshots onto an in-memory registry object
     nothing ever dumped, so the v5.49 mock-keyed history never actually
     reached disk. commit_registry() now takes optional `axis1_snapshots`/
     `axis3_snapshots` dicts ({section: snapshot}) and persists them as
     reg['axis1_paper'][paper_id] / reg['axis3_paper'][paper_id] (v5.57;
     plus the legacy [str(N)] key for the MOCK series only) — replace-by-
     mock, idempotent, deep-copied (purity), exactly the axis2_window_counts
     precedent. Absent/empty ⇒ no write ⇒ byte-identical behaviour for
     every exam without the axis feature. No engine consumes these fields
     yet; this makes the write real so history accrues from now on.
"""

import copy
import hashlib
import re as _re
from collections import Counter
from datetime import datetime, timezone

import paper_pipeline as pp
import blueprint_core as bc      # v1.12 — G-MEDIAREUSE (GAP-2026-11-03 OD-13) + producer_release

__all__ = [
    "commit_registry",
    "regcheck",
    "qindex_certify",
    "predelivery_checklist",
    "outputs_to_clear",
    "delivery_scope",
]


# ══════════════════════════════════════════════════════════════════════════
# S13-4 — commit_registry()
# ══════════════════════════════════════════════════════════════════════════
def _series_prefix(paper_id):
    """Series identity of a paper_id ('MOCK', 'SUBJ:Physics', ...). A null /
    absent paper_id maps to 'MOCK' — the same assumption the historical
    default slug f"MOCK:M{mock:02d}" always encoded. Never raises."""
    if not paper_id:
        return 'MOCK'
    try:
        return pp.paper_prefix(paper_id)
    except Exception:
        return str(paper_id)


def _paper_number_or_none(paper_id):
    """pp.paper_number(), degraded to None on any unparseable id."""
    try:
        return pp.paper_number(paper_id)
    except Exception:
        return None


def _entry_paper_id(e):
    """v1.8 — the paper a registry ledger/manifest entry belongs to. An entry
    without a paper_id is a LEGACY entry and maps to f"MOCK:M{mock:02d}" — the
    same convention _stale_sibling and A-QINDEX already use. Never raises
    (a malformed 'mock' value yields None)."""
    pid = e.get('paper_id') if isinstance(e, dict) else None
    if pid:
        return pid
    try:
        return f"MOCK:M{int(e.get('mock')):02d}"
    except (AttributeError, TypeError, ValueError):
        return None


def _entry_number(e):
    """v1.8 — the PAPER NUMBER an entry occupies within its series: parsed from
    its paper_id when parseable, else its 'mock' ordinal (legacy / unparseable
    ids — the pre-v1.8 rule). On a MOCK series the two are always equal
    (pp.apply_mock_offset moves both); on a RESUMED SCOPED series they differ
    (mocks[].mock is the run-local ordinal 1..K, paper_id carries paper_start+k),
    which is exactly why the ordinal can never be the slot key."""
    n = _paper_number_or_none(e.get('paper_id')) if e.get('paper_id') else None
    return n if n is not None else e.get('mock')


# v1.11 — optional per-question fields carried concept_map -> registry.question_index.
# v1.16 (GAP-2026-11-10, GAP §6.1 generated item record): the per-item organic-parity / difficulty-integrity
# records — carried ONLY when the concept_map entry has them (a legacy entry stays byte-identical)
QINDEX_OP_FIELDS = ('organic', 'organic_reason', 'chain', 'decisions_author', 'decisions_grader', 'grades',
                    'key_votes', 'clone_check', 'stereo_elements', 'stereo_gate', 'figures', 'last_resort',
                    # the C2 item fields (S0-OP-5 CANDIDATE RECORD) — the series registry is seeded from them
                    'key_smiles', 'starting_smiles', 'reagents', 'answer_kind', 'task_template',
                    # v1.22 (GAP-2026-11-14-BATCH-COMPLETE): the rung-3 fallback record (A-AXIS1 reads it)
                    'bc_fallback')
# v1.17 (GAP-2026-11-11-NONORGANIC-MOCK-FIDELITY): the per-item non-organic fidelity records
QINDEX_NF_FIELDS = ('subject', 'part', 'mip', 'given_in_stem', 'measured_axis2', 'text_fingerprint', 'stem_text',
                    'option_texts', 'manifest_hash')
QINDEX_V589_FIELDS = ('difficulty_check', 'figural_ask_type', 'representations',
                      'scheme_grammar', 'marked_sites', 'ladder',
                      'slot_chain',            # v1.15: a DISCLOSED item's exhausted chain (S13-4c re-derives it)
                      # release 2026.11.25 (GAP-2026-11-19-S13-2F-LOOP P1): the mode the label was decided under, so
                      # A-QINDEX check 9 can tell a count-free row (modes ladder / counted) from author-counted evidence
                      'difficulty_mode', 'shape_drift',
                      's13_2f_cap')            # release 2026.11.25 (LAW-FA-TERM-1): S13-4c re-reads a cap-stamped item
# v1.12 — GAP-2026-11-03 §4.3: every quality verdict lives ON the item and is READ
# downstream, never recomputed differently.
QINDEX_V590_FIELDS = (
    # every S7-QUALITY record field a quality gate reads (a SUBSET of audit_canonical
    # _QQ_V590_FIELDS, which adds identity / key fields the registry never carries;
    # handshake_audit.py asserts the subset — final_assembly never imports the auditor): the final S13-4c sweep audits the registry
    # record, not the sidecar, so a field absent here is invisible to its gate at S13-4c.
    'ask_format',                                             # v1.14 (GAP-2026-11-05 DL-22)
    'option_identities', 'entities', 'shape', 'scheme_grammar', 'fingerprint',
    'concept', 'pattern_key', 'distractor_mechanisms', 'distractor_pathways', 'mechanism_family',
    'class_word', 'stated_formula', 'stated_dbe', 'stated_rings', 'stated_stereocentres',
    'given_smiles', 'reagents', 'reagent_unit_formula', 'stem_agents', 'named_entities',
    'scheme_annotations', 'condition_vocab', 'trailing_placeholders', 'asked_placeholders', 'multi_step_lettered_allowed',
    'pyq_phrase_states_constitution', 'key_set_size', 'ladder', 'stem_leak', 'consist',
    'stereo_decl', 'review', 'quality_status', 'judge_input_sha256')


def commit_registry(registry, pending, bp, N, *, paper_id, batches_completed,
                     axis2_window_counts, passage_present, di_present,
                     figural_present, concept_map,
                     passage_linked_qs=(), cloze_linked_qs=(),
                     di_manifest=None, fig_manifest=None, figure_specs=None,
                     axis1_snapshots=None, axis3_snapshots=None,
                     framework_repo_commit=None, spec_source_report=None,
                     timestamp=None, answer_key=None, quality_readiness=None, shape_infeasible=None,
                     difficulty_state=None, nf_disclosed=None, manifest_hash=None):
    """Registry update protocol (v2.0 GAP-03 + GAP-04 fix; v5.48.0 QINDEX-FK
    enforcement; v5.52 idempotency — see module docstring deviation 4;
    v5.54 same-series dedupe + axis snapshot persistence — see the module
    docstring's v5.54 section).

    Pure: does not mutate `registry`/`pending`; returns a NEW dict. On the
    FK check failing (a concept_map subtopic_id not present in
    bp['subtopic_list']), returns {'ok': False, 'fails': [...],
    'registry': <the ORIGINAL, unmodified registry>} — the caller must NOT
    persist that 'registry' value; nothing was committed.

    FIRST-MOCK REGISTRY INITIALISATION runs automatically whenever
    registry has no papers_completed/mocks_completed yet (mirrors the
    spec-inline `is_first_mock` gate exactly).

    Returns {'ok': True, 'fails': [], 'registry': <new dict>, 'paper_id': paper_id}
    on success.
    """
    reg = copy.deepcopy(registry)
    pending = pending or {}

    # ── FIRST-MOCK REGISTRY INITIALISATION (unchanged logic) ────────────────
    is_first_mock = len(reg.get('papers_completed', reg.get('mocks_completed', []))) == 0
    if is_first_mock:
        if 'content_tracking' not in reg:
            reg['content_tracking'] = {
                '_schema': {
                    '_note': 'C2 (v5.21): every entry also carries paper_id (from batch_state) '
                             'for cross-tier dedup; mock_n retained. The generalised uniqueness '
                             'ledger (B phase) keys on paper_id.',
                    'ga_facts_used': 'list of {fact, source_url, mock_n}',
                    'passage_topics': 'list of {topic, type, mock_n}',
                    'cloze_topics': 'list of {topic, mock_n}',
                    'vocab_words_used': 'list of {word, correct_answer, mock_n, subtopic}'
                                        ' — v4.5: for a multi (MSQ) vocabulary item, append'
                                        ' one entry per word in the correct SET (correct_answer'
                                        ' may be a list of the in-set words), never just one,'
                                        ' so cross-mock dedup counts every used word.',
                    'idioms_used': 'list of {idiom, mock_n}',
                    'grammar_rules_used': 'list of {rule, mock_n, position}',
                    'computer_facts': 'list of {application, category, concept, mock_n}',
                    'numeric_seeds': 'list of {subtopic, seed_values, mock_n}',
                    'analogy_schemes': 'list of {scheme_type, mock_n}',
                    'cause_effect_domains': 'list of {domain, mock_n}',
                    'syllogism_domains': 'list of {domain, mock_n}',
                    'option_sets': 'list of {subtopic, sorted_options, mock_n}',
                },
                'ga_facts_used': [], 'passage_topics': [], 'cloze_topics': [],
                'vocab_words_used': [], 'idioms_used': [], 'grammar_rules_used': [],
                'computer_facts': [], 'numeric_seeds': [], 'analogy_schemes': [],
                'cause_effect_domains': [], 'syllogism_domains': [], 'option_sets': [],
            }
        for field in ['image_phashes', 'image_sources_used', 'session_log', 'question_index']:
            if field not in reg:
                reg[field] = []

    # ── COMMIT pending_registry (bare-indexed to match spec exactly — these
    #    three fields are guaranteed present by the Step-1 template, §14
    #    S14-1, unlike the setdefault-guarded ones below) ────────────────────
    reg['question_hashes'].extend(pending.get('question_hashes', []))
    reg['stem_texts'].extend(pending.get('stem_texts', []))
    reg['semantic_tuples'].extend(pending.get('semantic_tuples', []))
    reg.setdefault('semantic_usage', []).extend(pending.get('semantic_usage', []))
    _ex = reg.setdefault('exhausted_subtopics', {})
    for _sid, _rec in pending.get('exhausted_subtopics', {}).items():
        _ex.setdefault(_sid, _rec)
    reg.setdefault('image_phashes', []).extend(pending.get('image_phashes', []))
    reg.setdefault('image_sources_used', []).extend(pending.get('image_sources_used', []))

    ct = reg.setdefault('content_tracking', {})
    for field in ['ga_facts_used', 'passage_topics', 'cloze_topics',
                  'vocab_words_used', 'idioms_used', 'grammar_rules_used',
                  'computer_facts', 'numeric_seeds', 'analogy_schemes',
                  'cause_effect_domains', 'syllogism_domains', 'option_sets']:
        ct.setdefault(field, []).extend(pending.get(field, []))

    # ── Slot identity of THIS commit (v1.8 — GAP-2026-10-09-PAPER-SIZE-SERIES-
    #    AGNOSTIC). One series holds ONE paper per paper NUMBER; the number comes
    #    from paper_id, never from the run ordinal N (on a resumed scoped series
    #    N=1 is paper :11, and keying on N erased paper :01 from papers_completed,
    #    question_index and session_log — measured). Unparseable ids fall back to
    #    N, the pre-v1.8 rule, so the renamed-paper_id case is handled as before.
    _new_prefix = _series_prefix(paper_id)
    _new_num = _paper_number_or_none(paper_id)
    _slot_num = _new_num if _new_num is not None else N
    _this_pid = paper_id or f"MOCK:M{int(N):02d}"

    def _stale_sibling(e):
        if _entry_paper_id(e) == _this_pid:
            return True                      # the exact-id rule
        if _series_prefix(e.get('paper_id')) != _new_prefix:
            return False                     # a different series never collides
        _en = _entry_number(e)
        if _new_num is not None and _paper_number_or_none(e.get('paper_id')) is not None:
            return _en == _new_num           # both ids parse: compare paper numbers
        return e.get('mock') == N            # an unparseable id: the pre-v1.8 rule

    # ── RC / DI / figural manifests — replace-by-PAPER_ID (deviation 4; v1.8) ──
    # Pre-v1.8 these were replaced by the ordinal (`e.get('mock') != N`) and carried
    # no paper_id, on a registry SHARED across series: committing SUBJ:X:01 deleted
    # MOCK:M01's manifest and vice versa, and the auditor read whichever entry came
    # first. Same class as options_by_q (v5.56) and axis1_paper (v5.57). Every entry
    # now carries paper_id (the authority); "mock" is kept for legacy readers.
    # ── v1.9 MANIFEST-COMMIT-LAW (GAP-2026-11-01 LAW F3.1): COMMIT ON EXISTENCE. ──
    # A producer flag may DESCRIBE a paper; it may never SUPPRESS the record the
    # producer wrote. The declared flags and the derived truth are both kept:
    # registry.paper_flags[paper_id] = {flag: declared, flag_derived: from the manifest}.
    _has_rc = bool(passage_linked_qs) or bool(cloze_linked_qs)
    _has_di = bool(di_manifest) and bool(di_manifest.get('questions'))
    _has_fig = bool(fig_manifest) and bool(fig_manifest.get('questions'))
    _pf = reg.setdefault('paper_flags', {})
    _pf[_this_pid] = {
        'passage_present': bool(passage_present), 'passage_present_derived': bool(passage_present) or _has_rc,
        'di_present': bool(di_present), 'di_present_derived': bool(di_present) or _has_di,
        'figural_present': bool(figural_present), 'figural_present_derived': _has_fig,
    }
    # *_derived is the manifest's truth alone (passage/di keep their v1.9 shape; the
    # figural flag is derived from the figure manifest only — v1.10, so declared True over
    # an empty manifest reads as the disagreement it is).
    for _flag, _declared, _has in (('passage_present', passage_present, _has_rc),
                                   ('di_present', di_present, _has_di),
                                   ('figural_present', figural_present, _has_fig)):
        if _has and not _declared:
            print(f"S13-4 (final_assembly v1.10, MANIFEST-COMMIT-LAW): blueprint says "
                  f"{_flag}=False but this paper's manifest is non-empty — the record is "
                  f"COMMITTED and registry.paper_flags[{_this_pid!r}].{_flag}_derived=True "
                  f"records the disagreement. Fix the blueprint flag (ScopedBlueprint "
                  f"v1.11.0 derives it); the record was never optional.")

    if passage_present or _has_rc:
        rc = [e for e in reg.setdefault('rc_manifests', []) if not _stale_sibling(e)]
        rc.append({
            "mock": N, "paper_id": _this_pid,
            "passage_linked": sorted(set(passage_linked_qs)),
            "cloze_linked": sorted(set(cloze_linked_qs)),
        })
        reg['rc_manifests'] = rc

    if di_manifest is not None and (di_present or _has_di):
        di = [e for e in reg.setdefault('di_manifests', []) if not _stale_sibling(e)]
        di.append({
            "mock": N, "paper_id": _this_pid,
            "di_qs": sorted(int(q) for q in di_manifest.get('questions', {})),
            "subtopic_ids": {str(q): v.get('subtopic_id')
                             for q, v in di_manifest.get('questions', {}).items()
                             if v.get('subtopic_id')},
            "table_shapes": {str(q): v.get('table_shape')
                             for q, v in di_manifest.get('questions', {}).items()
                             if v.get('table_shape')},
        })
        reg['di_manifests'] = di

    if fig_manifest is not None and (figural_present or _has_fig):
        # v1.9 F2.3 — a figure with no recorded type cannot be audited against the
        # measured profile; the gate would go dormant and report green (variant V3).
        # E15 — a question authored by a pre-v5.88 session and RESUMED across the fix has
        # no object_type and never can have one honestly; S4-12 marks it
        # record_integrity='legacy_unlabelled' and it is committed AS unlabelled, disclosed.
        fig_manifest = copy.deepcopy(fig_manifest)       # v1.10: never mutate the caller's sidecar
        _ri_in = {str(q): (v or {}).get('record_integrity')
                  for q, v in fig_manifest.get('questions', {}).items()
                  if (v or {}).get('record_integrity')}
        for _q, _v in fig_manifest.get('questions', {}).items():
            if _v and not _v.get('object_type') and _ri_in.get(str(_q)) == 'legacy_unlabelled':
                _v['object_type'] = 'legacy_unlabelled'
        _no_type = sorted((str(q) for q, v in fig_manifest.get('questions', {}).items()
                           if not (v or {}).get('object_type')),
                          key=lambda s: (not s.isdigit(), int(s) if s.isdigit() else s))
        if _no_type:
            raise ValueError(
                f"S13-4 (final_assembly v1.10, LAW F2.3): fig_manifest question(s) "
                f"{_no_type} carry no object_type — every rendered figural question must "
                f"record the figure type it was generated AS (MockTestCreate S7-NEW-B; "
                f"figure_types.FIGURE_TYPES vocabulary). A figure whose type is not "
                f"recorded cannot be audited and is not committed.")
        # v1.12 — G-MEDIAREUSE (GAP-2026-11-03 OD-13 (i)): no two questions share a
        # picture (MD5 of the media part) unless both belong to ONE linked set. Refused in
        # the FK gate's shape; the S13-4 caller sends the LATER item to the ladder (R2).
        _linked = []
        for _grp in (passage_linked_qs or ()), (cloze_linked_qs or ()):
            if _grp:
                _linked.append([str(q) for q in _grp])
        _sg = {}
        for _qn, _cm in (concept_map or {}).items():
            if isinstance(_cm, dict) and _cm.get('stimulus_group_id') not in (None, ''):
                _sg.setdefault(str(_cm['stimulus_group_id']), []).append(str(_qn))
        _linked += list(_sg.values())
        _mr = bc.media_reuse_check({str(q): list(v.get('image_hashes', []))
                                    for q, v in fig_manifest.get('questions', {}).items()
                                    if isinstance(v, dict)}, linked_sets=_linked)
        if _mr['state'] == 'FAIL':
            fail_msg = ("LADDER-REPAIR R2 G-MEDIAREUSE (final_assembly v1.12, GAP-2026-11-03): the same "
                        "picture is placed under two questions — "
                        + "; ".join(f"Q{f['q']} reuses Q{f['other_q']}'s media ({f['md5'][:10]})" for f in _mr['findings'])
                        + ". Regenerate the LATER item (new given entity, new picture), rebuild the "
                          "sidecar, re-run S13-4. Never hand-patch the manifest.")
            return {'ok': False, 'fails': [fail_msg], 'registry': registry, 'paper_id': paper_id}
        fg = [e for e in reg.setdefault('figural_manifests', []) if not _stale_sibling(e)]
        fg.append({
            "mock": N, "paper_id": _this_pid,
            "figural_qs": list(fig_manifest.get('questions', {}).keys()),
            "image_hashes": [h for q in fig_manifest.get('questions', {}).values()
                             for h in q.get('image_hashes', [])],
            "object_types": {str(q): v['object_type']
                             for q, v in fig_manifest.get('questions', {}).items()
                             if v.get('object_type')},
            "subtopic_ids": {str(q): v['subtopic_id']
                             for q, v in fig_manifest.get('questions', {}).items()
                             if v.get('subtopic_id')},
            "figure_specs": figure_specs or {},
            # v5.55 — machine-readable identity of every generated figure.
            "semantic_objects": _validated_semantic_objects(
                fig_manifest, unvalidated=[q for q, r in _ri_in.items() if r == 'legacy_unlabelled']),
            # v1.10 — LAW F2 record stamp. annotate_legacy_figure_records() annotates ONLY
            # entries without it, so a CURRENT paper's false record can never be laundered
            # into "legacy" (it FAILS A-FIGTYPE-KIND instead).
            "record_schema": FIGURE_RECORD_SCHEMA,
            **({"record_integrity": _ri_in} if _ri_in else {}),
            # release 2026.11.24 (FG-2): the paper's figure plan (target, granted, recorded shortfalls) — A-AXIS1 reads it
            **({"plan": fig_manifest['plan']} if isinstance(fig_manifest.get('plan'), dict) else {}),
        })
        reg['figural_manifests'] = fg

    # ── v5.55 KEY COMMITMENTS (additive; replace-by-paper_id) ───────────────
    if answer_key is not None:
        import paper_pipeline as _pp
        _ans = (answer_key or {}).get('answers', answer_key) or {}
        _cm = concept_map or (answer_key or {}).get('concept_map', {}) or {}
        _canon = {}
        for _q, _v in _ans.items():
            _qt = (_cm.get(str(_q)) or {}).get('qtype') or (
                'nat' if isinstance(_v, float) or
                ((_cm.get(str(_q)) or {}).get('answer_type') == 'numerical') else
                'msq' if isinstance(_v, (list, tuple, set)) else 'mcq')
            if _qt == 'nat':
                # the committed string is the PORTAL GRADING VALUE Step 9 re-derives
                # (S7-NEW-C), never a float repr
                _gv = (_cm.get(str(_q)) or {}).get('nat_grading_value')
                _v = _gv if _gv not in (None, '') else _v
            _canon[int(_q)] = _pp.canonical_answer(_qt, _v)
        reg.setdefault('key_commitments', {})[paper_id] = _pp.seal_key_commitments(paper_id, _canon)
        # ── difficulty_gate birth stamp — SINGLE WRITER (v5.57,
        #    GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER; was GAP-2026-08-24-
        #    DIFFICULTY-GATE-BLOCKING's inline dict) ────────────────────────────
        # OWNERSHIP: this is the ONLY place a record is CREATED, and it is created
        # through paper_pipeline Cluster DG — never as a hand-built dict. A MOCK
        # paper is born PENDING (Step 11 refuses it until Step 9's gate runs). A
        # SCOPED paper is born DORMANT/scoped_paper: §7A-M is MOCK-ONLY, so a
        # scoped paper stamped PENDING could never be resolved and was
        # undeliverable in every project (gap defect G-4). After birth `status`
        # and `repair_rounds_used` are written ONLY by Step 9 via
        # pp.dg_write_verdict (together, atomically). (v5.76 / REPAIR-RETIRED-
        # 2026-08-27: the repair steps and their snapshot writer are gone.) A registry entry
        # with NO difficulty_gate key is a LEGACY paper and delivers as before
        # (operator decision 2026-08-24: old papers untouched).
        _pp.dg_stamp_pending(reg, paper_id)


    # ── Question metadata index (v5.2, Contract_QuestionMetadataIndex v1.0) ─
    concept_map = concept_map or {}
    _bp_by_id = {s.get('subtopic_id'): s for s in bp.get('subtopic_list', [])}
    _fk_bad = {qn: concept_map[qn].get('subtopic_id') for qn in concept_map
               if concept_map[qn].get('subtopic_id') not in _bp_by_id}
    if _fk_bad:
        fail_msg = (
            "HARD STOP (S13-4 FK, v5.48.0): concept_map subtopic_id(s) are NOT in "
            "blueprint.subtopic_list — the capture re-typed an id instead of copying the "
            "blueprint string: "
            + "; ".join(f"Q{q}={_fk_bad[q]!r}" for q in sorted(_fk_bad, key=int))
            + ". Fix the S7-NEW-A capture for these questions (assign from the blueprint "
              "row object), rebuild concept_map, re-run S13-4. Never hand-patch the "
              "registry to bypass this.")
        return {'ok': False, 'fails': [fail_msg], 'registry': registry, 'paper_id': paper_id}

    _qi = [{"q": int(qn),
            "subtopic_id": _bp_by_id[concept_map[qn]["subtopic_id"]]["subtopic_id"],
            "section": _bp_by_id[concept_map[qn]["subtopic_id"]].get("section"),
            "subtopic": _bp_by_id[concept_map[qn]["subtopic_id"]].get("subtopic"),
            "difficulty": concept_map[qn].get("difficulty"),
            # v1.6 (GAP-2026-08-21-DIFFICULTY-STICKER-LABELS): the derivation
            # observations behind the label — deduction_steps / axiom_concepts /
            # question_class / speed_hack_exists / is_negative / qtype — recorded
            # at authoring (S7 CHECK 3c) and carried verbatim so the audit can
            # recompute label == assess_difficulty(obs) forever. None for a
            # legacy concept_map: the audit's check 8 then skips, never false-
            # fails, while its structural-floor check 7 still runs on the label.
            "difficulty_obs": concept_map[qn].get("difficulty_obs"),
            # v1.7 (GAP-2026-09-21-LINKED-PLACEMENT): set membership, carried ONLY
            # when the concept_map entry has the key (a set-placed paper) — a legacy
            # paper's question_index entry is byte-identical to v1.6.
            **({"stimulus_group_id": concept_map[qn]["stimulus_group_id"]}
               if "stimulus_group_id" in concept_map[qn] else {}),
            # v1.11 (GAP-2026-11-02): the per-question v5.89 records — difficulty decision
            # (CHECK 3c), ask type / representations / scheme grammar (F8), declared marks
            # (MARK-IFF-NAMED) and the repair-ladder trace (L4) — carried ONLY when the
            # concept_map entry has them, so a legacy entry stays byte-identical.
            **{_k: copy.deepcopy(concept_map[qn][_k]) for _k in QINDEX_V589_FIELDS if _k in concept_map[qn]},
            # v1.12 (GAP-2026-11-03): the quality verdicts, carried only when present.
            **{_k: copy.deepcopy(concept_map[qn][_k]) for _k in QINDEX_V590_FIELDS if _k in concept_map[qn]},
            # v1.16 (GAP-2026-11-10): organic parity / difficulty integrity records
            **{_k: copy.deepcopy(concept_map[qn][_k]) for _k in QINDEX_OP_FIELDS if _k in concept_map[qn]},
            # v1.17 (GAP-2026-11-11): non-organic fidelity records (subject / Part, MIP, given_in_stem, measured
            # format, text fingerprint) — carried only when present
            **{_k: copy.deepcopy(concept_map[qn][_k]) for _k in QINDEX_NF_FIELDS if _k in concept_map[qn]}}
           for qn in sorted(concept_map, key=int)]
    _qindex_cert = {"blueprint_version": bp.get("blueprint_version"),
                    "subtopic_set_hash": hashlib.sha256("\n".join(sorted(
                        s.get("subtopic_id") or "" for s in bp.get("subtopic_list", [])
                    )).encode("utf-8")).hexdigest()[:16],
                    # v1.12 (OD-10 a): the release that produced this paper
                    "producer_release": bc.QQ_RELEASE,
                    # v1.13 (GAP-2026-11-04 D5): the release whose quality gates wrote this
                    # paper's quality_status stamps — Deliver re-certifies A-TEMPLATE-only
                    # stamps ONLY when they were written by 2026.11.03 (no stamps_release)
                    "stamps_release": bc.STAMPS_RELEASE,
                    # v1.16 (GAP-2026-11-10): the release that produced this paper — a paper at or after
                    # bc.FRAMEWORK_RELEASE_STRICT is LB2-strict in every later audit (LAW-ORG-5)
                    "framework_release": bc.OP_RELEASE}
    if framework_repo_commit is not None:
        _qindex_cert["framework_repo_commit"] = framework_repo_commit
    if spec_source_report is not None:
        _qindex_cert["spec_source_report"] = spec_source_report

    # v5.54 (GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING): the dedupe key
    # for question_index/session_log is widened from exact-paper_id to
    # SAME SERIES + SAME MOCK NUMBER. Rationale: one series can hold exactly
    # one paper per number, so an existing entry with this mock's number in
    # this paper's OWN series is by definition the stale version of THIS
    # commit (the historical trigger: a paper_id corrected mid-session, then
    # re-committed — the old key never matched the renamed entry, so the
    # stale sibling survived forever and no gate could see it). An entry with
    # the same number in a DIFFERENT series (MOCK:M01 vs SUBJ:Physics:01) is
    # a legitimately coexisting paper and is never touched.
    # v1.8: _stale_sibling is defined once, above the manifest writes, and keys on
    # the paper NUMBER parsed from paper_id (the ordinal only for unparseable ids).
    reg.setdefault('question_index', [])
    reg['question_index'] = [e for e in reg['question_index'] if not _stale_sibling(e)]
    reg['question_index'].append({"mock": N, "paper_id": paper_id,
                                  "qindex_cert": _qindex_cert, "questions": _qi,
                                  # v1.12 — S3-2e readiness record (A-READINESS reads it; a
                                  # DEGRADED paper is visible in the audit, not only in a footer)
                                  **({"quality_readiness": copy.deepcopy(quality_readiness)}
                                     if isinstance(quality_readiness, dict) else {}),
                                  # v1.12 — S3-12d planner record: shapes whose floor no capable
                                  # slot could take (A-SHAPEMIX reads it; recorded, never a defect)
                                  **({"shape_infeasible": [str(x) for x in shape_infeasible]}
                                     if isinstance(shape_infeasible, (list, tuple)) else {}),
                                  # v1.14 (GAP-2026-11-05 Part D) — the paper's recorded difficulty
                                  # state (level items, judge-dormant items, Hard misses): Step 11
                                  # reprints the AMBER disclosure lines from it. Absent -> nothing.
                                  **({"difficulty_state": copy.deepcopy(difficulty_state)}
                                     if isinstance(difficulty_state, dict) else {}),
                                  # v1.17 (GAP-2026-11-11): the gates disclosed after the bounded repair (A-* reads
                                  # them as AMBER) and the taxonomy the paper was built on (F-08). Absent -> nothing.
                                  **({"nf_disclosed": dict(nf_disclosed)} if isinstance(nf_disclosed, dict) and nf_disclosed else {}),
                                  **({"manifest_hash": str(manifest_hash)} if manifest_hash else {})})

    # ── Ledgers — idempotent (deviation 4) ───────────────────────────────────
    # v5.55 (GAP-2026-08-13-SCOPED-MOCKS-COMPLETED): mocks_completed is the
    # LEGACY MOCK-SERIES ledger — appending a SCOPED paper's bare ordinal here
    # fabricated a phantom mock (ScopedBlueprint S9-1: scoped papers are
    # "tagged with paper_id, NOT a bare mock number"): committing only
    # SUBJ:Physics:03 yielded mocks_completed=[3], and every integrity check
    # that converts those ints to MOCK:M03 (paper_pipeline.registry_integrity_
    # check; Step 11 S1-2; Step 9 P10's WARN) then reported false "REGISTRY
    # DATA LOSS: MOCK:M03" with a wrong remedy, forever. papers_completed is
    # the universal ledger and gets EVERY paper; mocks_completed only mocks.
    mocks_completed = reg.setdefault('mocks_completed', [])
    if _new_prefix == 'MOCK' and N not in mocks_completed:
        mocks_completed.append(N)
    papers_completed = reg.setdefault('papers_completed', [])
    # v5.54: a stale same-series entry whose parsed paper NUMBER equals N is
    # the renamed predecessor of THIS paper — remove it, or the ledger holds
    # two ids for one paper forever. Unparseable numbers are left alone
    # (can't attribute them safely); different series are never touched.
    # v1.8: compared against THIS paper's NUMBER (_slot_num), not the run ordinal N —
    # on a resumed scoped series they differ, and comparing to N deleted paper :01
    # when paper :11 committed.
    papers_completed[:] = [p for p in papers_completed
                           if p == paper_id
                           or _series_prefix(p) != _new_prefix
                           or _paper_number_or_none(p) != _slot_num]
    if paper_id not in papers_completed:
        papers_completed.append(paper_id)

    session_log = [e for e in reg.setdefault('session_log', [])
                   if not _stale_sibling(e)]
    _ts = timestamp if timestamp is not None else datetime.now(timezone.utc).isoformat()
    _sl_entry = {
        "mock": N, "paper_id": paper_id, "batches": batches_completed,
        "q_range": [1, bp.get('total_questions')],
        "questions_added": bp.get('total_questions'),
        "audit_result": "exit_0", "verdict": "SHIP",
        "timestamp": _ts, "notes": "v2.0 session",
    }
    if framework_repo_commit is not None:
        _sl_entry["framework_repo_commit"] = framework_repo_commit
    if spec_source_report is not None:
        _sl_entry["spec_source_report"] = spec_source_report
    session_log.append(_sl_entry)
    reg['session_log'] = session_log

    # ── Axis-2 window snapshot (unchanged) ───────────────────────────────────
    _win = bp.get('batch_size_qs', 10)
    _pidx = int(_re.sub(r'\D', '', paper_id.rsplit(':', 1)[-1]) or N)
    _cur_window = (_pidx - 1) // max(1, _win)
    axis2_window_counts = axis2_window_counts or {}
    if any(v is not None for v in axis2_window_counts.values()):
        reg['axis2_window'] = {'window': _cur_window,
                               'sections': {s: c for s, c in axis2_window_counts.items()
                                            if c is not None}}

    # ── Axis-1/Axis-3 per-paper snapshots (v5.54 — GAP-2026-08-12-AXISPAPER-
    # PERSISTENCE). The spec's S7-AXIS block accumulated these per section and
    # wrote them onto an in-memory registry object that nothing ever dumped —
    # so the v5.49 mock-keyed history the spec promised never reached disk.
    # Persisted here, at the ONE terminal commit, exactly like every other
    # per-mock field: [str(N)] keying = replace-by-mock = idempotent
    # (deviation 4's pattern; axis2_window_counts is the signature precedent).
    # Absent-safe: an exam with no axis feature passes nothing, writes nothing.
    # v5.57 (GAP-2026-08-24-AXIS-PAPER-SERIES-COLLISION): paper_id-keyed AUTHORITY for
    # every series; the ordinal key is MOCK-only (legacy readers) and is never written
    # for a scoped paper — an ordinal key on a shared registry is exactly the write
    # that destroyed the earlier paper's snapshot. Same shape as options_by_q (v5.56).
    _axpid = paper_id or f"MOCK:M{int(N):02d}"
    _ax_is_mock = _series_prefix(_axpid) == 'MOCK'
    if axis1_snapshots:
        _a1 = reg.setdefault('axis1_paper', {})
        _a1[_axpid] = copy.deepcopy(dict(axis1_snapshots))
        if _ax_is_mock:
            _a1[str(N)] = copy.deepcopy(dict(axis1_snapshots))
    if axis3_snapshots:
        _a3 = reg.setdefault('axis3_paper', {})
        _a3[_axpid] = copy.deepcopy(dict(axis3_snapshots))
        if _ax_is_mock:
            _a3[str(N)] = copy.deepcopy(dict(axis3_snapshots))

    return {'ok': True, 'fails': [], 'registry': reg, 'paper_id': paper_id}


def _validated_semantic_objects(fig_manifest, unvalidated=()):
    """v5.55 — {q: [semantic objects]} from fig_manifest questions[q].semantic_objects,
    each shape-validated (paper_pipeline.validate_semantic_object) and, for a
    STRUCTURE/REACTION, canonicalised through rdkit when available so the
    registry carries the canonical form. Raises ValueError on a malformed object
    — a figure whose identity cannot be stated is not committed.
    unvalidated (v1.10, E15): question keys marked record_integrity='legacy_unlabelled'
    — authored by a pre-v5.88 session, so a REACTION object there may carry a molecule
    canonical (the pre-fix shape). They are committed AS IS (disclosed, skipped by the
    auditor), never validated against a rule that did not exist when they were written."""
    import paper_pipeline as _pp
    out = {}
    unvalidated = {str(q) for q in (unvalidated or ())}
    for q, v in (fig_manifest or {}).get('questions', {}).items():
        objs = (v or {}).get('semantic_objects') or []
        if not objs:
            continue
        if str(q) in unvalidated:
            out[str(q)] = [dict(o) for o in objs if isinstance(o, dict)]
            continue
        clean = []
        for i, o in enumerate(objs):
            _pp.validate_semantic_object(o, ctx=f'Q{q} semantic_objects[{i}]')
            o = dict(o)
            if o['kind'] in ('STRUCTURE', 'REACTION'):
                import corpus_io as _cio                 # Create-route rdkit home
                canon, reason = _cio.canonical_structure(o['canonical'])
                if canon is None and reason != 'rdkit_unavailable':
                    raise ValueError(f'Q{q} semantic_objects[{i}]: canonical {o["canonical"]!r} '
                                     f'rejected — {reason}')
                if canon is not None:
                    o['canonical'] = canon
            clean.append(o)
        out[str(q)] = clean
    return out


FIGURE_RECORD_SCHEMA = 'F2'      # stamp written by commit_registry v1.10 on every figure record
LEGACY_RECORD_INTEGRITY = ('legacy_label_mismatch', 'legacy_degenerate_reaction', 'legacy_unlabelled')


def annotate_legacy_figure_records(registry, kind_of=None):
    """v1.9 — forward-only MIGRATION for registries committed before LAW F2/F3
    (GAP-2026-11-01 §6 Migration). Delivered papers are never re-rendered (S10-7 Q13
    posture); the record is ANNOTATED so a healed registry never looks identical to a
    clean one. Pure: returns (new_registry, annotations) and mutates nothing.

    kind_of : INJECTED figure_types.default_kind-like callable
              (object_type) -> (kinds tuple | None). None => the TYPE↔KIND pass is
              skipped (thin posture; only the '>>' and absent-record passes run).
    Annotations written (idempotent; an existing annotation is left as it is):
      figural_manifests[].record_integrity[q] = 'legacy_label_mismatch' |
                                                'legacy_degenerate_reaction'
      paper_flags[pid].figure_record          = 'absent_legacy'
    """
    reg = copy.deepcopy(registry or {})
    notes = []
    for e in reg.get('figural_manifests', []) or []:
        if e.get('record_schema'):
            continue            # committed under LAW F2 — audited, never annotated (v1.10)
        pid = _entry_paper_id(e)
        ri = e.setdefault('record_integrity', {})
        so = e.get('semantic_objects') or {}
        for q, ot in (e.get('object_types') or {}).items():
            objs = [o for o in so.get(str(q), []) if str((o or {}).get('role', '')).startswith('problem')]
            if kind_of is not None and objs and ot:
                kinds = kind_of(ot)
                if kinds and objs[0].get('kind') not in kinds and str(q) not in ri:
                    ri[str(q)] = 'legacy_label_mismatch'
                    notes.append(f'{pid} Q{q}: {ot!r} over {objs[0].get("kind")} — legacy_label_mismatch')
        for q, objs in so.items():
            for o in objs or []:
                if (o or {}).get('kind') == 'REACTION' and '>' not in str(o.get('canonical', '')) \
                        and str(q) not in ri:
                    ri[str(q)] = 'legacy_degenerate_reaction'
                    notes.append(f'{pid} Q{q}: REACTION without ">>" — legacy_degenerate_reaction')
        if not ri:
            e.pop('record_integrity', None)
    have = {_entry_paper_id(e) for e in reg.get('figural_manifests', []) or []}
    pf = reg.setdefault('paper_flags', {})
    def _n(x):
        try:
            return int(x or 0)
        except (TypeError, ValueError):
            return 0
    _a1_all = reg.get('axis1_paper') or {}
    _done = [(str(p), str(p)) for p in (reg.get('papers_completed', []) or [])]
    if not _done:                                   # pre-paper_id registries (mock numbers only;
        for m in (reg.get('mocks_completed', []) or []):   # axis1_paper keyed by ORDINAL pre-v5.57)
            _pid = f"MOCK:M{int(m):02d}" if str(m).isdigit() else str(m)
            _done.append((_pid, str(m) if str(m) in _a1_all else _pid))
    for pid, _a1_key in _done:
        a1 = _a1_all.get(_a1_key) or _a1_all.get(pid) or {}
        n_fig = 0
        for _sec, _counts in (a1.items() if isinstance(a1, dict) else []):
            if isinstance(_counts, dict):
                n_fig += _n(_counts.get('FIGURAL', 0))
            elif _sec == 'FIGURAL':
                n_fig += _n(_counts)
        if n_fig > 0 and pid not in have and 'figure_record' not in pf.get(pid, {}):
            pf.setdefault(pid, {})['figure_record'] = 'absent_legacy'
            notes.append(f'{pid}: {n_fig} FIGURAL question(s) in axis1_paper, no figure record — absent_legacy')
    if not pf:
        reg.pop('paper_flags', None)
    return reg, notes


# ══════════════════════════════════════════════════════════════════════════
# S13-REGCHECK — regcheck()
# ══════════════════════════════════════════════════════════════════════════
_REQUIRED_TOP = [
    'exam_code', 'schema_version', 'mocks_completed', 'papers_completed',
    'question_hashes', 'stem_texts', 'semantic_tuples', 'semantic_usage',
    'exhausted_subtopics', 'question_index', 'image_phashes',
    'image_sources_used', 'session_log', 'content_tracking',
    'section_names', 'rc_manifests', 'figural_manifests', 'di_manifests',
]
_REQUIRED_CT = [
    'ga_facts_used', 'passage_topics', 'cloze_topics', 'vocab_words_used',
    'idioms_used', 'grammar_rules_used', 'computer_facts', 'numeric_seeds',
    'analogy_schemes', 'cause_effect_domains', 'syllogism_domains',
    'option_sets',
]


def _commit_problems(reg, m, series_prefix='MOCK'):
    """G-COMMIT-COMPLETE per-mock cross-ledger check (GAP-2026-08-12-
    S13-COMMIT-COMPLETE). A paper is complete iff it has a session_log entry
    AND a question_index entry carrying a non-null paper_id.

    v5.55 (GAP-2026-08-13-SCOPED-MOCKS-COMPLETED): entries are filtered to
    the requested SERIES before matching by number. Without this, a SCOPED
    paper's entry (mock=3, paper_id='SUBJ:Physics:03') could satisfy — and
    therefore MASK — a check for MOCK number 3 whose own MOCK:M03 entry was
    genuinely lost. Null/absent paper_id maps to 'MOCK', matching the
    historical default-slug assumption everywhere else in this module."""
    # v1.8: matched by PAPER NUMBER (_entry_number: parsed from paper_id, the
    # ordinal only for legacy/unparseable ids) — on a resumed scoped series the
    # ordinal 1 is shared by paper :01 and paper :11. MOCK series: unchanged
    # (number == ordinal there).
    sl_mocks = {_entry_number(e) for e in reg.get('session_log', [])
                if _series_prefix(e.get('paper_id')) == series_prefix}
    qi_by_mock = {_entry_number(e): e for e in reg.get('question_index', [])
                  if _series_prefix(e.get('paper_id')) == series_prefix}
    problems = []
    if m not in sl_mocks:
        problems.append('no session_log entry')
    qie = qi_by_mock.get(m)
    if qie is None:
        problems.append('no question_index entry')
    elif not qie.get('paper_id'):
        problems.append('question_index entry has no paper_id')
    return problems


def _duplicate_commit_problems(reg, m, series_prefix=None):
    """v5.54 (GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING) — detect the
    stale-sibling state the old gate was blind to: TWO OR MORE
    question_index/session_log entries carrying the same mock number WITHIN
    THE SAME SERIES. One series holds exactly one paper per number, so ≥2
    same-series entries for one number always means a stale duplicate (the
    historical trigger: a paper_id corrected mid-session, re-committed under
    the new id, old entry never cleaned). Entries with the same number in
    DIFFERENT series (MOCK:M01 alongside SUBJ:Physics:01) are legitimately
    coexisting papers and never flagged. Keyed by series PREFIX, not full
    paper_id, deliberately — the whole point is catching two different ids
    that claim the same slot.

    v1.8: `m` is a PAPER NUMBER and entries are matched by _entry_number (the
    ordinal only for legacy/unparseable ids), so paper :01 and paper :11 of a
    resumed scoped series — both ordinal 1 — are two slots, not a duplicate.
    series_prefix (optional) restricts the check to one series: THIS paper's
    own slot check passes it; the historical sweep leaves it None (all series)."""
    problems = []
    for ledger in ('question_index', 'session_log'):
        by_prefix = Counter(_series_prefix(e.get('paper_id'))
                            for e in reg.get(ledger, []) if _entry_number(e) == m
                            and (series_prefix is None
                                 or _series_prefix(e.get('paper_id')) == series_prefix))
        dups = {pfx: c for pfx, c in by_prefix.items() if c > 1}
        for pfx, c in sorted(dups.items()):
            problems.append(f"{ledger} holds {c} entries for number {m} in "
                            f"series '{pfx}' (one series holds ONE paper per "
                            f"number — a stale duplicate from a paper_id "
                            f"change)")
    return problems


def regcheck(registry, bp, *, N, concept_map=None, msq_meta=None, paper_id=None,
             require_key_commitments=False):
    """Registry schema-completeness gate (v3.5) + G-COMMIT-COMPLETE
    (v5.52, GAP-2026-08-12-S13-COMMIT-COMPLETE). Pure — does not mutate
    `registry`; caller does I/O (see Framework_MockTestCreate.md §13 for the
    exact json.load/answer_key.json try-except/json.dump/os.makedirs
    sequence this replaces).

    Returns {'ok': bool, 'fails': [...], 'healed': [...], 'warnings': [...],
    'registry': <healed dict>}. 'ok' is False only if THIS mock's own commit
    (mock N) is incomplete or the schema self-heal somehow still leaves
    fields missing (should be unreachable). A pre-existing incomplete commit
    from a DIFFERENT mock produces a warning, not a failure — see module
    docstring deviation 4 for why full retroactive repair is out of scope.
    """
    reg = copy.deepcopy(registry)
    concept_map = concept_map or {}
    msq_meta = msq_meta or {}

    missing_top = [f for f in _REQUIRED_TOP if f not in reg]
    missing_ct = [f for f in _REQUIRED_CT if f not in reg.get('content_tracking', {})]

    for f in missing_top:
        reg[f] = {} if f in ('content_tracking', 'exhausted_subtopics') else []
    ct = reg.setdefault('content_tracking', {})
    for f in missing_ct:
        ct[f] = []

    still_missing = ([f for f in _REQUIRED_TOP if f not in reg]
                     + [f for f in _REQUIRED_CT if f not in reg.get('content_tracking', {})])
    if still_missing:
        return {'ok': False, 'registry': reg, 'healed': missing_top + missing_ct,
                'warnings': [],
                'fails': [f"HARD STOP (S13-REGCHECK): registry still missing "
                          f"{still_missing} after self-heal. Do NOT deliver. Inspect "
                          f"S13-4 commit logic."]}

    # v5.55: the current paper's series prefix, derived from bp exactly the
    # way S13-4 derives paper identity (C2). For a SCOPED run this makes the
    # this-commit completeness check look for the SCOPED entry (previously it
    # looked for a MOCK-series entry with the scoped ordinal — a guaranteed
    # false HARD STOP once _commit_problems became series-aware); the
    # historical warnings loop below stays MOCK-series (mocks_completed is
    # the mock ledger, and now only ever contains mocks).
    _this_pid = next((mk.get('paper_id') for mk in bp.get('mocks', [])
                      if mk.get('mock') == N), None) or f"MOCK:M{int(N):02d}"
    _this_prefix = _series_prefix(_this_pid)
    # v1.8: THIS paper's slot is its paper NUMBER within its series (from paper_id);
    # the run ordinal N only when the id does not parse (pre-v1.8 rule).
    _this_num = _paper_number_or_none(_this_pid)
    if _this_num is None:
        _this_num = N

    this_mock_problems = _commit_problems(reg, _this_num, series_prefix=_this_prefix)
    if this_mock_problems:
        return {'ok': False, 'registry': reg, 'healed': missing_top + missing_ct,
                'warnings': [],
                'fails': [f"HARD STOP (G-COMMIT-COMPLETE): THIS mock's own S13-4 "
                          f"commit is incomplete — mock {N}: "
                          f"{', '.join(this_mock_problems)}. A freshly committed mock MUST "
                          "have a session_log entry AND a question_index entry with a "
                          "non-null paper_id from the SAME S13-4 run. Re-run S13-4 in FULL "
                          "(never a hand-rolled subset of its writes), then re-run "
                          "S13-REGCHECK. Do NOT deliver."]}

    # v5.54 (GAP-2026-08-12-S13-COMMIT-COMPLETE-PAPERID-KEYING) — the
    # stale-sibling detector. Same THIS-mock-fails / other-mocks-warn split
    # as the incompleteness check above, for the same reason: a fresh commit
    # that left its own ledger slot ambiguous must never ship, while
    # historical duplicates get surfaced on every run, never silently.
    this_mock_dups = _duplicate_commit_problems(reg, _this_num, series_prefix=_this_prefix)
    if this_mock_dups:
        return {'ok': False, 'registry': reg, 'healed': missing_top + missing_ct,
                'warnings': [],
                'fails': [f"HARD STOP (G-COMMIT-COMPLETE/DUP): THIS mock's ledger slot "
                          f"is ambiguous — {'; '.join(this_mock_dups)}. This is the "
                          "renamed-paper_id stale-duplicate state: S13-4's v5.54 "
                          "same-series dedupe prevents CREATING it, so its presence "
                          "means an older/hand-rolled commit left it behind. Remove "
                          "the stale entry (the one whose paper_id no longer matches "
                          "the blueprint's mocks[] declaration for this number), "
                          "re-run S13-4 in FULL, then re-run S13-REGCHECK. "
                          "Do NOT deliver."]}

    # v5.55 (GAP-2026-08-21-EXPLANATION-PROVENANCE) — a paper committed with an
    # answer key must carry its key commitments, or Step 9 has nothing to
    # reconcile against and the wrong-published-key class is open again.
    if require_key_commitments:
        _pid = paper_id or f"MOCK:M{int(N):02d}"
        _kc = (reg.get('key_commitments') or {}).get(_pid) or {}
        _nq = len(((concept_map or {}) if isinstance(concept_map, dict) else {}) or {})
        if not _kc.get('entries') or (_nq and len(_kc['entries']) != _nq):
            return {'ok': False, 'registry': reg, 'healed': missing_top + missing_ct,
                    'warnings': [],
                    'fails': [f"HARD STOP (G-KEYCOMMIT): registry.key_commitments[{_pid!r}] "
                              f"carries {len(_kc.get('entries', {}))} entries, expected "
                              f"{_nq or '>=1'}. S13-4 must be run with answer_key=<the "
                              f"answer_key sidecar> so every question's canonical answer is "
                              f"committed (paper_pipeline.seal_key_commitments). Step 9 "
                              f"reconciles its derived answers against these; without them "
                              f"a wrong published key is undetectable. Do NOT deliver."]}

    # v1.8: the historical sweep skips THIS paper only when this paper IS that mock
    # (a scoped run used to skip MOCK m == N — its own ordinal — and so never warned
    # about that mock's incomplete commit).
    def _is_this(m):
        return _this_prefix == 'MOCK' and m == _this_num
    warnings = [f"mock {m}: {', '.join(_commit_problems(reg, m))}"
               for m in reg.get('mocks_completed', [])
               if not _is_this(m) and _commit_problems(reg, m)]
    warnings += [f"mock {m}: {', '.join(_duplicate_commit_problems(reg, m))}"
                 for m in reg.get('mocks_completed', [])
                 if not _is_this(m) and _duplicate_commit_problems(reg, m)]

    # options_by_q (v4.7, ND6) — derived from concept_map/msq_meta the caller
    # already read (with the SAME try/except fallback the spec-inline code
    # has around the answer_key.json load — see §13 in the spec).
    #
    # v5.53 hardening (found in the final 0-bug audit): the spec-inline code's
    # try/except around the answer_key.json load ALSO wrapped its int(total_
    # options) coercion, so a syntactically-valid file with a non-numeric
    # total_options fell back to 4 rather than crashing. Splitting the file
    # load (caller) from the schema gate (here, pure) moved that coercion
    # outside the caller's try/except — an extraction-introduced regression,
    # fixed by giving it its own guard, which is the more correct home for it
    # anyway: this function's docstring promises it never raises.
    try:
        ocount = int(msq_meta.get("total_options", 4))
    except (TypeError, ValueError):
        ocount = 4
    # Guard against a malformed (non-dict) concept_map entry — e.g. a hand-
    # edited or corrupted answer_key.json — degrading to "not numerical"
    # (the ocount default) rather than raising AttributeError on `.get()`.
    obq = {q: (0 if isinstance(concept_map.get(q), dict)
                  and concept_map[q].get("answer_type") == "numerical"
               else ocount)
           for q in concept_map}
    # Guard against a pre-existing options_by_q of the WRONG TYPE (e.g. a
    # hand-patched registry carrying a list) — force it to the correct
    # container type rather than crashing on `[...][str(N)] = obq`, the same
    # self-heal spirit already applied to the _REQUIRED_TOP fields above.
    if not isinstance(reg.get('options_by_q'), dict):
        reg['options_by_q'] = {}
    # v5.56 (GAP-2026-08-24-OPTIONS-BY-Q-SERIES-COLLISION): paper_id-keyed AUTHORITY
    # for every series; the ordinal key survives for the MOCK series only (legacy
    # readers), never for a scoped paper — a scoped ordinal on key str(N) is exactly
    # the write that destroyed the mock's map.
    _pid = paper_id or f"MOCK:M{int(N):02d}"
    reg['options_by_q'][_pid] = obq
    if _series_prefix(_pid) == 'MOCK':
        reg['options_by_q'][str(N)] = obq

    reg['section_names'] = [(s.get('section_name') or s.get('name') or '').strip()
                            for s in bp.get('sections', [])
                            if (s.get('section_name') or s.get('name'))]

    return {'ok': True, 'fails': [], 'healed': missing_top + missing_ct,
           'warnings': warnings, 'registry': reg}


# ══════════════════════════════════════════════════════════════════════════
# S13-QINDEX — qindex_certify()
# ══════════════════════════════════════════════════════════════════════════
def qindex_certify(registry, bp, N):
    """G-QINDEX (v5.2/v5.49.0) — certifies mock N's question_index entry.
    Delegates to paper_pipeline.validate_question_index() (see module
    docstring deviation 3 for exactly what that changes and why it's safe).
    Pure; never raises. Returns {'ok': bool, 'fails': [...]}."""
    ok, report = pp.validate_question_index(registry, bp, mock_n=N)
    return {'ok': ok, 'fails': list(report.get('fails', []))}



# ══════════════════════════════════════════════════════════════════════════
# S13-7 pre-step — outputs_to_clear() (v1.13, GAP-2026-11-04 A8 / D3)
# ══════════════════════════════════════════════════════════════════════════
_INTERNAL_MARKERS = ('_answer_key.json', '_fig_manifest.json', '_batch_state.json',
                     '_progress.json', '_audit_dossier.json', '_item_sweep_certificate.json',
                     '_item_findings.json', '_registry_preview.json')
# release review (2026-11-04): THIS run's internal files, ANCHORED to the names Step 7 writes
# (<EXAM>_M<N>_<kind>.json, <EXAM>_fig_manifest.json) — a substring match deleted other steps'
# deliverables (e.g. PYQScan's <EXAM>_scan_progress.json).
_RUN_INTERNAL_KINDS = ('answer_key', 'batch_state', 'progress', 'audit_dossier', 'item_sweep_certificate',
                       'item_findings', 'registry_preview', 's13_2f_state', 'stimulus_profile', 'repair_state')


def _is_run_internal(name, exam):
    import re as _re
    return bool(exam) and (name == f'{exam}_fig_manifest.json' or _re.fullmatch(
        _re.escape(exam) + r'_M\d+_(?:' + '|'.join(_RUN_INTERNAL_KINDS) + r')\.json', name) is not None)


def _exam_and_slug(docx_name, reg_name):
    """('EXAM', 'slug') from the two deliverable names: reg = '<EXAM>_registry.json',
    docx = '<EXAM>_<slug>_Create.docx' (an exam code may contain '_', so the registry
    name — never a split — gives the exam)."""
    exam = str(reg_name or '')[:-len('_registry.json')] if str(reg_name or '').endswith('_registry.json') else ''
    d = str(docx_name or '')
    slug = d[len(exam) + 1:-len('_Create.docx')] if exam and d.startswith(exam + '_') and d.endswith('_Create.docx') else ''
    return exam, slug


def _is_other_paper_deliverable(name, docx_name, reg_name):
    """A previous paper's Create.docx of the same exam, delivered earlier in the same chat:
    history, not this run's artefact — never deleted, never a check-6 failure."""
    exam, _slug = _exam_and_slug(docx_name, reg_name)
    return bool(exam) and name != docx_name and name.startswith(exam + '_') and name.endswith('_Create.docx')


def delivery_scope(staged, *, docx_name, reg_name):
    """PURE. The names in `staged` that THIS paper's Step 7 delivery is judged on: the two
    deliverables, every file outputs_to_clear recognises as this run's artefact, and any
    other file carrying this paper's prefix <EXAM>_<slug>_ (an unrecognised file of THIS
    paper is still a closed-set breach). Another exam's, step's or paper's earlier output
    in the same chat is NOT in scope — present_files names its two paths explicitly, so
    such history is never delivered and never blocks the delivery (GAP-2026-11-04).
    S13-7 check 6 requires scope == {docx, registry}; S13-8 passes the scope, not the raw
    listing, to pp.verify_handoff_outputs."""
    exam, slug = _exam_and_slug(docx_name, reg_name)
    pfx = f'{exam}_{slug}_' if exam and slug else None
    st = set(staged or ())
    out = {f for f in st if f in (docx_name, reg_name)}
    out |= set(outputs_to_clear(st, docx_name=docx_name, reg_name=reg_name))
    out |= {f for f in st if (pfx is None or f.startswith(pfx)) and not _is_other_paper_deliverable(f, docx_name, reg_name)
            and (pfx is not None or f not in (docx_name, reg_name))}
    out |= {f for f in st if _is_run_internal(f, exam)}
    return sorted(out)


def outputs_to_clear(staged, *, docx_name, reg_name):
    """PURE. The names in `staged` (the outputs folder listing) that THIS paper's Step 7 run
    put there and that are NOT one of the two deliverables — S13-7 removes each before
    predelivery_checklist, so the delivery is exactly {Create.docx, registry.json} with no
    manual step:
      - per-batch cumulative docx  <EXAM>_<slug>_Q1to<k>.docx
      - a legacy (2026.11.03) review packet / verdict file  <EXAM>_<slug>_review_packet.zip,
        *_review_verdicts.json of this paper
      - any internal sidecar of this exam (answer key, batch state, certificate, …)
      - an answer-key file of THIS paper in any format
    Files of other exams, other steps or other papers are never returned."""
    import re as _re
    exam, slug = _exam_and_slug(docx_name, reg_name)
    if not exam:
        return []
    keep = {docx_name, reg_name}
    out = []
    for f in sorted(staged or ()):
        if f in keep or not f.startswith(exam + '_'):
            continue
        rest = f[len(exam) + 1:]
        # release review (2026-11-04): ONLY names this paper's Create run produces. A
        # blueprint (ScopedBlueprint / MockBlueprint deliverable) or the Step-6 auditor copy
        # presented earlier in the same chat is ANOTHER step's output — never deleted here
        # (it is outside delivery_scope, so it never blocks the delivery either).
        hit = (
            (slug and _re.fullmatch(_re.escape(slug) + r'_Q1to\d+\.docx', rest) is not None)
            or (slug and rest in (slug + '_review_packet.zip', slug + '_review_verdicts.json'))
            or _is_run_internal(f, exam)
            or (slug and rest.startswith(slug + '_') and 'answer' in rest.lower())
        )
        if hit:
            out.append(f)
    return out


# ══════════════════════════════════════════════════════════════════════════
# S13-7 — predelivery_checklist()
# ══════════════════════════════════════════════════════════════════════════
def paper_parity_gate(concept_map, format_floors=None, convention_floors=None, chain_share_floor=None):
    """v1.16 — LAW-ORG-11 PARITY-FLOORS at assembly (G-04 / G-05 / G-06): {'status': 'PASS'|'FAIL', 'formats',
    'conventions', 'chain_share', 'short': [...]} over the paper's ORGANIC items: every ask-format floor and
    convention floor met, and the share of items with >= 2 decisions >= chain_share_floor (the exam's past
    share). A FAIL names what is short; Create S13-2L converts / generates to fill it (never a stop)."""
    items = [dict(v, q=k) for k, v in (concept_map or {}).items() if isinstance(v, dict)]
    org = [i for i in items if i.get('organic') is True]
    fm = bc.parity_floor_check(org, format_floors or {}, key='ask_format')
    cv = bc.parity_floor_check(org, convention_floors or {}, key='representations')
    n2 = sum(1 for i in org if len([d for d in (i.get('decisions_author') or []) if d in bc.DECISION_TAGS]) >= 2)
    share = (n2 / len(org)) if org else 1.0
    short = [f'ask format {k}: {v} short' for k, v in fm['short'].items()] + \
            [f'convention {k}: {v} short' for k, v in cv['short'].items()]
    if isinstance(chain_share_floor, (int, float)) and share + 1e-9 < chain_share_floor:
        short.append(f'items with >= 2 decisions {share:.0%} < past share {chain_share_floor:.0%}')
    return {'status': 'FAIL' if short else 'PASS', 'formats': fm, 'conventions': cv,
            'chain_share': round(share, 4), 'short': short}


def paper_figure_proof_gate(concept_map, fig_manifest=None):
    """v1.16 — LAW-ORG-8 at assembly: {'status', 'missing': {q: [proof names]}} — every figure record of every
    ORGANIC item carries identity_ok, vision_ok and gates_ok True (the certificate requires all three).
    fig_manifest (the paper's {EXAM}_fig_manifest.json, when given): an organic item that places a picture
    (questions[q].image_hashes non-empty) with FEWER figures[] records than distinct pictures is missing
    'figure_proof_record' —
    a picture is never certified by the absence of its proof."""
    miss = {}
    fq = (fig_manifest or {}).get('questions') if isinstance(fig_manifest, dict) else None
    fq = fq if isinstance(fq, dict) else {}
    for q, v in (concept_map or {}).items():
        if not isinstance(v, dict) or v.get('organic') is not True:
            continue
        _fqe = fq.get(str(q)) if isinstance(fq.get(str(q)), dict) else {}
        _ot = str(_fqe.get('object_type') or '').lower()
        # only a STRUCTURE picture needs a structure proof record (a spectrum / graph / photo picture does not)
        _pics = _fqe.get("image_hashes") if _re.search(
            r'struct|reaction|scheme|molecule|chair|newman|fischer|haworth|sawhorse|conform|projection', _ot) else None
        _recs = [f for f in (v.get('figures') or []) if isinstance(f, dict)]
        if _pics and len(_recs) < len(set(_pics)):                 # every picture holds >= 1 proven structure
            miss[str(q)] = ['figure_proof_record']
            continue
        for f in (v.get('figures') or []):
            if not isinstance(f, dict):
                continue
            m = [k for k in ('identity_ok', 'vision_ok', 'gates_ok') if f.get(k) is not True]
            if m:
                miss.setdefault(str(q), sorted(set(miss.get(str(q), []) + m)))
    return {'status': 'FAIL' if miss else 'PASS', 'missing': miss}


def predelivery_checklist(outputs_dir, *, docx_name, reg_name, dossier_name=None,
                          regcheck_ok, qindex_ok, listdir=None, exists=None,
                          extra_deliverables=()):
    """7-point pre-delivery checklist (v3.5). The one function in this module
    that reads the filesystem (os.path.exists/os.listdir) — inherently can't
    be pure, since its entire job is verifying real files landed in a real
    directory. `listdir`/`exists` are injectable for self-testing without
    touching disk; default to the real os functions.

    Returns {'ok': bool, 'checks': [(name, bool), ...], 'fails': [...]}."""
    import os as _os
    _listdir = listdir if listdir is not None else _os.listdir
    _exists = exists if exists is not None else _os.path.exists

    docx_path = f'{outputs_dir}/{docx_name}'
    reg_path = f'{outputs_dir}/{reg_name}'

    try:
        staged = set(_listdir(outputs_dir))
    except OSError:
        # v5.53 hardening (found in the final 0-bug audit): broadened from
        # FileNotFoundError-only. outputs_dir can also fail to list with
        # NotADirectoryError (a file sits where the directory should be) or
        # PermissionError (restricted ACL) — both real OSError subclasses a
        # real filesystem can raise, and this function's whole contract is
        # "never crashes, report what's actually there." An unreadable
        # directory correctly reads as "nothing staged" (checks 1/2/4/5/6
        # then fail honestly on their own terms), never a raised exception.
        staged = set()

    checks = []
    checks.append(("1 final docx in outputs", _exists(docx_path)))
    checks.append(("2 registry.json in outputs", _exists(reg_path)))
    checks.append(("3 registry schema complete", bool(regcheck_ok)))
    bad_ak = [f for f in staged if 'answer' in f.lower()]
    checks.append(("4 no answer-key file in outputs", len(bad_ak) == 0))
    # v5.60 (GAP-2026-08-26-REGISTRY-HANDOFF-SEAM, operator decision 2026-08-26): the
    # Tier-A audit dossier is INTERNAL — written to /home/claude, consumed by the
    # S13-4c re-sweep, never delivered. It joins the sidecar list, so a dossier in
    # outputs is a LEAK (check 5) and the closed set is ALWAYS {docx, registry}
    # (check 6). `dossier_name` is kept as an accepted keyword so every existing
    # call site still compiles; it now names the file check 5 must NOT see.
    internal = ['_answer_key.json', '_fig_manifest.json', '_batch_state.json',
                '_progress.json', '_audit_dossier.json']
    # v1.13 (release review): judged on THIS paper's delivery scope — another step's file that
    # merely contains a marker (PYQScan's <EXAM>_scan_progress.json) is not this run's leak
    _scope5 = set(delivery_scope(staged, docx_name=docx_name, reg_name=reg_name))
    leaked = [f for f in staged if any(m in f for m in internal) and (f in _scope5 or not _exam_and_slug(docx_name, reg_name)[0])]
    if dossier_name and dossier_name in staged and dossier_name not in leaked:
        leaked.append(dossier_name)
    checks.append(("5 no internal sidecars in outputs", len(leaked) == 0))
    # v1.11 (GAP-2026-11-02 P2/P3): conditional extras — ONLY a blueprint json or the
    # per-exam auditor, by name. Anything else passed here is ignored (never widens
    # the set), so a caller cannot launder a sidecar into the delivery.
    # v1.13 (GAP-2026-11-04 D3 a): extras NEVER widen the set — the Step 7 contract is
    # exactly two files. `extra_deliverables` is accepted and ignored (call-site compat).
    # Check 6 judges the files THIS run stages: the two deliverables plus anything
    # outputs_to_clear recognises as this paper's run artefact; files of other papers /
    # steps of the same chat are not part of this delivery (present_files names its two
    # paths explicitly) and never block it.
    expected_set = {docx_name, reg_name}
    checks.append((f"6 outputs == exactly the {len(expected_set)} deliverables",
                  set(delivery_scope(staged, docx_name=docx_name, reg_name=reg_name)) == expected_set))
    checks.append(("7 question_index certified (G-QINDEX)", bool(qindex_ok)))

    fails = [name for name, ok in checks if not ok]
    return {'ok': not fails, 'checks': checks, 'fails': fails}



# ══ v1.17 (GAP-2026-11-11-BATCH-VERIFICATION) — Create S4-7 STEP A2, the I/O shell over blueprint_core Cluster BV ══

def paper_in_progress(home, exam, n):
    """v2.5 (GAP-2026-11-13-STEP7-SPEED G-10): the saved batch_state of paper <exam> M<n> when that paper is IN PROGRESS —
    the file exists, parses to a dict with a non-empty batch_plan and its state is not 'DELIVERED' — else None. A session
    start that finds one runs in RESUME mode and regenerates nothing (Create S3-13 / S3-16; bootstrap ns_session_start
    applies the same test, bootstrap.ns_paper_in_progress). In the I/O shell (final_assembly), never in the thin core."""
    import json as _j, os as _o
    p = _o.path.join(str(home), f'{exam}_M{int(n)}_batch_state.json')
    try:
        d = _j.load(open(p, encoding='utf-8'))
    except (OSError, ValueError, TypeError):
        return None
    if not isinstance(d, dict) or not d.get('batch_plan') or str(d.get('state') or '') == 'DELIVERED':
        return None
    return d


def bv_budget_value(key, default):
    """v1.21 (GAP-2026-11-13-STEP7-SPEED): one SESSION_BUDGET.json value (the verified copy beside this engine, i.e.
    /tmp/fw_effective), else default. A budget is never a constant in the engine (OR-4); never raises."""
    import json, os
    try:
        v = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SESSION_BUDGET.json'),
                           encoding='utf-8')).get(key)
    except (OSError, ValueError):
        v = None
    return default if v is None else v


BV_IN_BATCH_ASKS = 3     # v1.21: a reviewer role is asked at most 3 times in its batch (the 3rd on a switched model);
                         # v1.22 = bc.BC_ROLE_ASKS (LAW-BC-9) — kept as a name for the 2026.11.15 callers
BC_INTRINSIC_RENDERERS = ('glyph_path',)   # v1.22 R10: a figure drawn by these renderers IS the question (no text form)


def bc_figure_intrinsic(batch_state, q):
    """v1.22 (R10) — (intrinsic, family_engine) for question q: True when its recorded figure type is drawn by a
    renderer in BC_INTRINSIC_RENDERERS (figure_types registry — reasoning / geometry glyph families: the figure IS the
    question, so no rung-3 text fallback exists); family_engine when bc.BC_FAMILY_ANSWER_ENGINES names an engine for
    that family. Never raises (no record -> (False, False))."""
    try:
        import figure_types as _ft
        ot = (((batch_state or {}).get('figural_qs') or {}).get(str(q)) or {}).get('object_type')
        if not ot:
            return False, False
        row = _ft.lookup(ot) or {}
        intr = str(row.get('renderer') or '') in BC_INTRINSIC_RENDERERS
        fam = row.get('family') or row.get('type')
        return bool(intr), bool(intr and (fam in bc.BC_FAMILY_ANSWER_ENGINES or row.get('type') in bc.BC_FAMILY_ANSWER_ENGINES))
    except Exception:                                   # noqa: BLE001
        return False, False


def _bc_entry_sha(entry):
    """The question's CURRENT text binding exactly as bc.bc_apply computes it (op_content_sha + the render sha of every
    recorded figure)."""
    e = entry if isinstance(entry, dict) else {}
    sha = bc.op_content_sha(e)
    _fdl = [(f.get('file'), f.get('render_sha')) for f in (e.get('figure_dicts') or []) if isinstance(f, dict)]
    return bc._bv_sha([sha, _fdl]) if _fdl else sha


def _bc_render_shas(entry):
    import os as _o
    e = dict(entry) if isinstance(entry, dict) else {}
    if isinstance(e.get('figure_dicts'), list):
        e['figure_dicts'] = [dict(_fd, render_sha=(hashlib.sha256(open(str(_fd['file']), 'rb').read()).hexdigest()
                                                   if _fd.get('file') and _o.path.exists(str(_fd['file'])) else None))
                             if isinstance(_fd, dict) else _fd for _fd in e['figure_dicts']]
    return e


def bc_reopen(exam, n, qs, reason, home='/home/claude'):
    """v1.22 (GAP §6.6 step 2, P2) — the LAST batch's whole-paper sweep named a question of an EARLIER batch: re-open it
    inside the current batch. It joins this batch's work and climbs one rung there with `reason` as its brief (a gate
    finding), with reviewers — never repaired at Final Assembly. Returns the re-opened questions. Never raises."""
    import json, os
    try:
        p = os.path.join(home, f'{exam}_M{n}_batch_state.json')
        bs = json.load(open(p, encoding='utf-8'))
        st = bs.setdefault('bv', {})
        ro = st.setdefault('reopen', {})
        out = []
        for q in [str(x) for x in (qs or [])]:
            ro.setdefault(q, [])
            if str(reason) not in ro[q]:
                ro[q].append(str(reason))
            out.append(q)
        json.dump(bs, open(p, 'w', encoding='utf-8'), indent=2)
        return out
    except (OSError, ValueError):
        return []


def bc_last_batch_route(findings, shape_plan=None, concept_map=None, current_batch_qs=None):
    """release 2026.11.25 (GAP-2026-11-19-S13-2F-LOOP P13 / G9 / G21, amended LAW-BC-6) — THE decision for the LAST
    batch's whole-paper pre-commit sweep, so no worker judgment decides it. `findings` = the auditor's item findings
    (and/or FAIL lines with 'qs'). Returns {'disclose': {gate: [q]}, 'reopen': {q: [reasons]}, 'accepted': [q]}:
      * a composition gate (bc.NF_DISCLOSE_GATES) is DISCLOSED — never a re-open — EXCEPT an A-SHAPEMIX item that
        DRIFTED from its planned shape (concept_map shape != shape_plan[q], no recorded shape_drift): that item is
        re-opened in this batch (the drift is the writer's, the plan is not the cause);
      * any other item gate on a question of an EARLIER batch re-opens it (fa.bc_reopen); a question of the CURRENT
        batch (current_batch_qs) is listed in 'current' — it is already in this batch's own STEP B / STEP A2 flow;
      * a composition gate's paper-level FAIL line (no question) is disclosed too;
      * an item already settled (ESCALATED / DISCLOSED) is accepted, never re-opened.
    Pure; never raises."""
    sp = shape_plan if isinstance(shape_plan, dict) else {}
    cm = concept_map if isinstance(concept_map, dict) else {}
    cur = {str(x) for x in (current_batch_qs or [])} if isinstance(current_batch_qs, (list, tuple, set)) else set()
    out = {'disclose': {}, 'reopen': {}, 'accepted': [], 'current': []}
    rows = []
    for f in (findings or []) if isinstance(findings, (list, tuple)) else []:
        if not isinstance(f, dict):
            continue
        g = str(f.get('gate') or f.get('check') or '')
        if f.get('q') is not None:
            rows.append((str(f.get('q')), g, str(f.get('finding') or f.get('message') or g)))
        _fqs = f.get('qs') if isinstance(f.get('qs'), (list, tuple)) else None
        for q in (_fqs or []):
            rows.append((str(q), g, str(f.get('message') or g)))
        if f.get('q') is None and not _fqs and g in bc.NF_DISCLOSE_GATES:
            out['disclose'].setdefault(g, [])              # a paper-level composition FAIL: disclosed, no question
    for q, g, why in rows:
        e = cm.get(q) if isinstance(cm.get(q), dict) else {}
        if str(e.get('quality_status') or '').startswith(('ESCALATED', 'DISCLOSED')):
            if q not in out['accepted']:
                out['accepted'].append(q)
            continue
        if g in bc.NF_DISCLOSE_GATES:
            drift = (g == 'A-SHAPEMIX' and e.get('shape') and isinstance(sp.get(q), str)
                     and bc.canonical_shape(e.get('shape')) != bc.canonical_shape(sp.get(q))
                     and not isinstance(e.get('shape_drift'), dict))
            if drift:
                out['reopen'].setdefault(q, [])
                _r = f"G-SHAPEPLAN: planned {bc.canonical_shape(sp.get(q))!r}, written {bc.canonical_shape(e.get('shape'))!r}"
                if _r not in out['reopen'][q]:
                    out['reopen'][q].append(_r)
            else:
                out['disclose'].setdefault(g, [])
                if q not in out['disclose'][g]:
                    out['disclose'][g].append(q)
            continue
        if q in cur:
            if q not in out['current']:
                out['current'].append(q)
            continue
        out['reopen'].setdefault(q, [])
        if f'{g}: {why}'[:300] not in out['reopen'][q]:
            out['reopen'][q].append(f'{g}: {why}'[:300])
    return out


def bc_last_batch_apply(exam, n, worklist, home='/home/claude'):
    """The I/O shell of bc_last_batch_route for Create S4-7 STEP B (LAST batch): reads the batch_state shape plan and
    the sidecar, writes each NEW composition disclosure once to the sidecar's nf_disclosed (AMBER, the same record
    S13-2F writes) and re-opens each 'reopen' question with fa.bc_reopen. Returns the route. Never raises."""
    import json, os
    try:
        bsp = os.path.join(home, f'{exam}_M{n}_batch_state.json')
        kp = os.path.join(home, f'{exam}_M{n}_answer_key.json')
        bs = json.load(open(bsp, encoding='utf-8')) if os.path.exists(bsp) else {}
        kd = json.load(open(kp, encoding='utf-8')) if os.path.exists(kp) else {}
        wl = worklist if isinstance(worklist, dict) else {}
        _cb = next((b for b in (bs.get('batch_plan') or []) if isinstance(b, dict)
                    and str(b.get('batch_id')) == str(bs.get('current_batch'))), None)
        _cur = [str(q) for q in range(int(_cb['q_start']), int(_cb['q_end']) + 1)] if _cb else []
        _fl_nf = [x for x in (wl.get('fail_lines') or []) if isinstance(x, dict)
                  and (x.get('qs') or str(x.get('check') or '') in bc.NF_DISCLOSE_GATES)]
        r = bc_last_batch_route(list(wl.get('item_findings') or []) + _fl_nf,
                                bs.get('shape_plan'), kd.get('concept_map'), current_batch_qs=_cur)
        if r['disclose'] and kd:
            nd = kd.setdefault('nf_disclosed', {})
            for g, qs in r['disclose'].items():
                if g not in nd:
                    nd[g] = ('last batch: ' + ', '.join(f'Q{q}' for q in qs))[:380] if qs else \
                        'last batch: paper-level composition shortfall'
            json.dump(kd, open(kp, 'w', encoding='utf-8'), indent=2)
        for q, why in r['reopen'].items():
            bc_reopen(exam, n, [q], '; '.join(why)[:500], home=home)
        return r
    except (OSError, ValueError, TypeError):
        return {'disclose': {}, 'reopen': {}, 'accepted': [], 'current': []}


def bv_paper_blueprint(exam, n, home, batch_state):
    """release 2026.11.25 — THE blueprint a paper was built on, when only its state is at hand: the first
    <exam>*_blueprint.json (staged copy first, then the project) whose paper-n allocation holds EVERY subtopic of the
    paper's slot map (batch_state['subtopic_by_qnum']) — the rule bv_figure_plan_fallback uses, so a project holding a
    mock blueprint AND scoped blueprints never takes another series' paper n. {} when none fits. Never raises."""
    try:
        import glob as _gl
        import json
        import os
        bs = batch_state if isinstance(batch_state, dict) else {}
        sbq = bs.get('subtopic_by_qnum') if isinstance(bs.get('subtopic_by_qnum'), dict) else {}
        need = {str(v) for v in sbq.values() if v}
        if not need:
            return {}
        for c in sorted(set(_gl.glob(os.path.join(home, f'{exam}*_blueprint.json')))) + \
                sorted(set(_gl.glob(f'/mnt/project/{exam}*_blueprint.json'))):
            try:
                b = json.load(open(c, encoding='utf-8'))
            except (OSError, ValueError):
                continue
            if not isinstance(b, dict):
                continue
            m = next((m for m in (b.get('mocks') or []) if isinstance(m, dict) and str(m.get('mock')) == str(n)), None)
            have = {str(a.get('subtopic_id')) for sec in ((m or {}).get('sections') or []) if isinstance(sec, dict)
                    for a in (sec.get('subtopic_allocations') or []) if isinstance(a, dict)}
            if have and need <= have:
                return b
        return {}
    except Exception:                                   # noqa: BLE001 — never a stop
        return {}


def bv_figure_capable_qs(exam, n, home, batch_state, section):
    """release 2026.11.25 (F5) — the figure-capable slots of one section for a figure plan frozen before this release
    (no 'capable_qs'): the questions whose subtopic the PAPER'S blueprint (bv_paper_blueprint) allocates in FIGURAL
    format in that section. [] when unknown (the re-grant is then recorded as not possible — disclosed). Never raises."""
    try:
        bs = batch_state if isinstance(batch_state, dict) else {}
        sbq = bs.get('subtopic_by_qnum') if isinstance(bs.get('subtopic_by_qnum'), dict) else {}
        b = bv_paper_blueprint(exam, n, home, bs)
        m = next((m for m in (b.get('mocks') or []) if isinstance(m, dict) and str(m.get('mock')) == str(n)), None)
        fig = set()
        for sec in ((m or {}).get('sections') or []):
            if isinstance(sec, dict) and str(sec.get('section_name')) == str(section):
                fig |= {str(a.get('subtopic_id')) for a in (sec.get('subtopic_allocations') or [])
                        if isinstance(a, dict) and str(a.get('format') or '').upper() == 'FIGURAL'}
        return sorted((str(q) for q, s_ in sbq.items() if str(s_) in fig), key=lambda x: int(x) if x.isdigit() else 0)
    except Exception:                                   # noqa: BLE001 — never a stop
        return []


def bv_load_ladder(exam, home='/home/claude', fresh_first=False):
    """Cluster R3: the exam's difficulty ladder ([ExamCode]_difficulty_ladder.json, written by Step 5). A paper in
    progress reads the session's STAGED copy first (the ladder is frozen per paper); a NEW paper (fresh_first) reads
    the attachments, then the project files, then the staged copy — a re-built ladder that was attached wins over a
    stale staged one. None when absent or unreadable (the paper then runs mode 'counted', disclosed). Never raises."""
    import json, os
    _home = [os.path.join(home, f'{exam}_difficulty_ladder.json')]
    _fresh = [f'/mnt/user-data/uploads/{exam}_difficulty_ladder.json', f'/mnt/project/{exam}_difficulty_ladder.json']
    for _p in (_fresh + _home if fresh_first else _home + _fresh):
        try:
            if os.path.exists(_p):
                _d = json.load(open(_p, encoding='utf-8'))
                if isinstance(_d, dict):
                    return _d
        except (OSError, ValueError):
            continue
    return None


def bv_difficulty_mode(batch_state, ladder=None):
    """Cluster R3: THE difficulty mode of a paper, frozen in batch_state['difficulty_mode'] the first time it is
    asked. A paper whose batch_state already holds review records but no mode was begun on an earlier release and
    stays on that release's rule ('br1') — a paper never changes rule mid-way. Mutates batch_state; never raises."""
    bs = batch_state if isinstance(batch_state, dict) else {}
    if str(bs.get('difficulty_mode') or '') not in bc.R3_MODES:
        begun = bool(((bs.get('bv') or {}).get('items')) if isinstance(bs.get('bv'), dict) else False)
        bs['difficulty_mode'] = bc.R3_MODE_LEGACY if begun else bc.r3_mode({}, ladder,
                                                                           {'difficulty_mode': bs.get('blueprint_difficulty_mode')})
    return bs['difficulty_mode']


def bv_r3_gaps(entry, key, top_band, ladder=None, mode=None, context=None):
    """Cluster R3 pre-review gaps of one text (§7.7 steps 1 and 3): the deterministic item gates
    (bc.qg_item_gates, with the release-2026.11.24 context — figure plan, ask form, planned statement count) and,
    for a top-band slot on the ladder, the content floor (bc.ld_floor_for / bc.r3_floor_gaps against the entry's
    content_record). [gap strings]. Never raises."""
    e = entry if isinstance(entry, dict) else {}
    out = list(bc.qg_item_gates(e, key, top_band, context=context))
    if top_band and mode == bc.R3_MODE_LADDER and isinstance(ladder, dict):
        _sc = bc.ld_scope_for(ladder, e.get('subject'), e.get('subtopic_id'))
        _fl = bc.ld_floor_for(ladder, _sc, e.get('subtopic_id'))
        if _fl:
            out += [f'CONTENT FLOOR (top band): {x} — use a larger / more constrained setting'
                    for x in bc.r3_floor_gaps(bc.r3_content_measures(e), _fl)]
    return out


def bv_figure_plan_fallback(exam, n, home, batch_state, blueprint=None):
    """FG-1 safety net (release 2026.11.24): when Create S3 recorded no batch_state['figure_plan'], build it here
    with bc.figure_grant_plan from the paper's blueprint (home, else /mnt/project) and batch_state['subtopic_by_qnum'],
    per section ({section: plan}; a section with no FIGURAL target is left out). Ranking without measured rates
    (subtopic order). {} when the blueprint or the slot map is unavailable. `blueprint` = the blueprint the paper was
    built on (Create S3-16 passes it); without it, the first candidate whose paper-n allocation holds EVERY subtopic of
    the paper's slot map (a scoped paper never takes the mock blueprint's target). Never raises."""
    try:
        import glob as _gl
        import json
        import os
        bs = batch_state if isinstance(batch_state, dict) else {}
        sbq = bs.get('subtopic_by_qnum') if isinstance(bs.get('subtopic_by_qnum'), dict) else {}
        if not sbq:
            return {}
        _need = {str(s) for s in sbq.values() if s}

        def _fits(b):
            m = next((m for m in (b.get('mocks') or []) if isinstance(m, dict) and str(m.get('mock')) == str(n)), None)
            have = {str(a.get('subtopic_id')) for s in ((m or {}).get('sections') or []) if isinstance(s, dict)
                    for a in (s.get('subtopic_allocations') or []) if isinstance(a, dict)}
            return bool(have) and _need <= have
        bp = blueprint if isinstance(blueprint, dict) else None
        if bp is None:
            cands = sorted(set(_gl.glob(os.path.join(home, f'{exam}*_blueprint.json'))
                               + _gl.glob(f'/mnt/project/{exam}*_blueprint.json')))
            for c in cands:
                try:
                    _b = json.load(open(c, encoding='utf-8'))
                except (OSError, ValueError):
                    continue
                if isinstance(_b, dict) and _fits(_b):
                    bp = _b
                    break
        if not isinstance(bp, dict):
            return {}
        mk = next((m for m in (bp.get('mocks') or []) if isinstance(m, dict) and str(m.get('mock')) == str(n)), None)
        sched = bp.get('axis_schedule') if isinstance(bp.get('axis_schedule'), dict) else {}
        out = {}
        for sec in (mk or {}).get('sections') or []:
            if not isinstance(sec, dict):
                continue
            nm = sec.get('section_name') or sec.get('name')
            ss = sched.get(nm)
            figs = {a.get('subtopic_id') for a in (sec.get('subtopic_allocations') or [])
                    if isinstance(a, dict) and a.get('format') == 'FIGURAL'}
            qr = sec.get('q_range') if isinstance(sec.get('q_range'), (list, tuple)) and len(sec.get('q_range')) == 2 else None
            cap = [(str(q), s) for q, s in sorted(sbq.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 0)
                   if s in figs and (qr is None or int(qr[0]) <= int(q) <= int(qr[1]))]
            if not isinstance(ss, dict):
                continue
            pl = bc.figure_grant_plan(cap, ss, bp.get('total_mocks') or 1, n)
            if pl.get('target', 0) > 0:
                out[str(nm)] = dict(pl, source='engine fallback (no Create S3 figure plan)')
        return out
    except Exception:                                   # noqa: BLE001 — a safety net never raises
        return {}


def bv_p1_chem_types():
    """release 2026.11.27 (GAP-2026-11-21 §2.5): every chemistry figure object type and its aliases — a figure_types
    row whose family is one of bc.CHEM_FAMILIES, or a member of CHEM_R/H/P_OBJECT_TYPES. Supplied to
    bc.math_typeset_plan (the thin core imports nothing) and frozen in the paper plan. figure_types is routed with
    every trigger that routes this engine. Sorted list; [] when figure_types is unavailable. Never raises."""
    try:
        import figure_types as _ft
        base = set(getattr(_ft, 'CHEM_R_OBJECT_TYPES', ())) | set(getattr(_ft, 'CHEM_H_OBJECT_TYPES', ())) \
            | set(getattr(_ft, 'CHEM_P_OBJECT_TYPES', ()))
        for t in getattr(_ft, 'FIGURE_TYPES', {}) or {}:
            if (_ft.lookup(t) or {}).get('family') in bc.CHEM_FAMILIES:
                base.add(t)
        for a, t in (getattr(_ft, 'ALIASES', {}) or {}).items():
            if t in base or (_ft.lookup(a) or {}).get('type') in base:
                base.add(a)
        return sorted(str(x) for x in base)
    except Exception:                                   # noqa: BLE001
        return []


R31_STATEMENT_SHAPES = ('statement', 'statements', 'combination', 'statement_combination', 'multi_statement',
                        'assertion_reason')


def bv_s3_plans(exam, n, home, batch_state, ladder=None, section_rules_text=None, blueprint=None):
    """Create S3-16 (release 2026.11.24) — the paper's per-slot plans, computed ONCE on a fresh paper and frozen in
    batch_state: (1) 'figure_plan' (FG-1, owner ruling RL-3: the blueprint's figure target per section, filled from
    the figure-capable slots in rank order — bv_figure_plan_fallback's chain); (2) 'stem_form' = {'ask_form':
    {section: measure}, 'statement_forms': {...}, 'n_statements': {q: n}} (D1 / RP-2: Step 5's measures; n per
    statement-shape slot by bc.statement_n_plan, rotated by the paper number); (3) 'r3_notes' += the E1 notice when
    the requested band mix is easier than the real exam on its ladder (owner ruling RL-1b: the mix is FINAL — notice
    only). Returns {key: value} for batch_state.update(); a key whose input is missing is left out (dormant). Never
    raises."""
    out = {}
    bs = batch_state if isinstance(batch_state, dict) else {}
    try:
        # release 2026.11.27 (GAP-2026-11-21 C-S8): the maths-typesetting / figure-purpose plan per SUBJECT, frozen once.
        # Always recorded on a fresh paper (all 'off' when section_rules carries no MATH_TYPESET_PROFILE line and no
        # owner line): its PRESENCE marks a paper built on this release; a resumed earlier paper has none (dormant)
        _sids = sorted({str(s) for s in (bs.get('subtopic_by_qnum') or {}).values() if s}) or None
        out['math_typeset'] = bc.math_typeset_plan(section_rules_text or '', blueprint, _sids,
                                                   chem_types=bv_p1_chem_types())
    except Exception:                                   # noqa: BLE001
        pass
    try:
        fp = bv_figure_plan_fallback(exam, n, home, bs, blueprint)
        # always recorded on a fresh paper ({} = no figure target): bv_batch_step falls back only when the key is absent
        out['figure_plan'] = {k: dict(v, source='Create S3-16') for k, v in fp.items()}
    except Exception:                                   # noqa: BLE001
        pass
    try:
        sf = bc.parse_stem_form(section_rules_text or '')
        sp = bs.get('shape_plan') if isinstance(bs.get('shape_plan'), dict) else {}
        stq = sorted((q for q, v in sp.items() if q != '_infeasible' and str(v).lower() in R31_STATEMENT_SHAPES),
                     key=lambda q: int(q) if str(q).isdigit() else 0)
        nd = {}
        for m in (sf.get('statement_forms') or {}).values():
            for k, v in ((m or {}).get('n_dist') or {}).items() if isinstance(m, dict) else []:
                if isinstance(v, (int, float)):
                    nd[k] = nd.get(k, 0.0) + float(v)
        ns = bc.statement_n_plan(nd, len(stq), offset=bc._qf_int(n, 1) - 1) if stq else []
        if sf.get('ask_form') or sf.get('statement_forms') or ns:
            out['stem_form'] = dict(sf, n_statements={q: k for q, k in zip(stq, ns)})
    except Exception:                                   # noqa: BLE001
        pass
    try:
        labs = list(bs.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
        dp = bs.get('difficulty_plan_target') or bs.get('difficulty_plan') or {}
        sids = sorted({str(s) for s in (bs.get('subtopic_by_qnum') or {}).values() if s}) or None
        real = bc.ld_real_shares(ladder, labs, sids)
        easier = bc.difficulty_vs_real({b: sum(1 for v in dp.values() if v == b) for b in labs}, real, labs)
        if easier:
            note = ('DIFFICULTY: the requested mix is easier than the real exam on its own ladder — '
                    + '; '.join(f"{e['band']} or harder {round(100 * e['requested'])}% requested vs "
                                f"{round(100 * e['real'])}% real" for e in easier)
                    + ' (blueprint mix kept as given — owner ruling RL-1b)')
            out['r3_notes'] = [x for x in (bs.get('r3_notes') or []) if not str(x).startswith('DIFFICULTY: the requested mix')] + [note]
        if real:
            out['difficulty_state'] = dict(bs.get('difficulty_state') or {}, real_shares=real)
    except Exception:                                   # noqa: BLE001
        pass
    return out

def bv_r3_report(batch_state, concept_map, ladder=None):
    """Cluster R3 paper report for the footer (S13-2L.0): the mode note, the count rule (cumulative minimums from
    the top), the paper rule (median placement per band vs the real exam) and the void-placement rate. Returns
    {'info': [...], 'amber': [...], 'count_rule', 'paper_rule'}; writes nothing. Never raises."""
    bs = batch_state if isinstance(batch_state, dict) else {}
    cm = concept_map if isinstance(concept_map, dict) else {}
    labs = list(bs.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
    mode = str(bs.get('difficulty_mode') or bc.R3_MODE_LEGACY)
    if mode == bc.R3_MODE_LEGACY:
        return {'info': [], 'amber': [], 'count_rule': None, 'paper_rule': None}
    req = bs.get('schedule_requested') or {}
    if not req:
        _tg = bs.get('difficulty_plan_target') or bs.get('difficulty_plan') or {}
        for _b in _tg.values():
            req[_b] = req.get(_b, 0) + 1
    dlv = {str(q): e.get('difficulty') for q, e in cm.items() if isinstance(e, dict) and str(q).isdigit()}
    cr = bc.r3_count_rule(dlv, req, labs) if req else None
    pnew, scope = {}, {}
    void = tot = 0
    for q, e in cm.items():
        if not isinstance(e, dict):
            continue
        dc = e.get('difficulty_check') if isinstance(e.get('difficulty_check'), dict) else {}
        if isinstance(dc.get('p_new'), (int, float)):
            pnew[str(q)] = dc['p_new']
            scope[str(q)] = bc.ld_scope_for(ladder, e.get('subject'), e.get('subtopic_id')) if isinstance(ladder, dict) else None
        for _m in ((e.get('grader_meta') or {}).values() if isinstance(e.get('grader_meta'), dict) else []):
            if isinstance(_m, dict) and isinstance(_m.get('placement'), dict):
                tot += 1
                void += 0 if _m['placement'].get('valid') else 1
    pr = bc.r3_paper_rule(pnew, dlv, ladder, scope, labs) if mode == bc.R3_MODE_LADDER else None
    fs = []
    if isinstance(ladder, dict) and isinstance(ladder.get('figure_share'), dict):
        _byf = {}
        for q, e in cm.items():
            if isinstance(e, dict) and str(q).isdigit():
                _s = bc.ld_scope_for(ladder, e.get('subject'), e.get('subtopic_id'))
                if _s:
                    _byf.setdefault(_s, []).append(bool(e.get('figure_files') or e.get('figure_dicts')))
        fs = bc.qg_figure_share(_byf, ladder.get('figure_share'))
    lines = bc.r3_footer_lines(mode, ladder, cr, pr, (void / tot) if tot else None, fs) + \
        [str(x) for x in (bs.get('r3_notes') or [])]
    lines += bv_r31_lines(bs, cm, ladder, labs)
    amber = [x for x in lines if '(AMBER)' in x or '(RED)' in x]
    return {'info': [x for x in lines if x not in amber], 'amber': amber, 'count_rule': cr, 'paper_rule': pr}


def bv_r31_lines(batch_state, concept_map, ladder=None, labels=None):
    """Release 2026.11.24 footer lines (Framework_DeliveryFooter §2R): (1) the SLOT LEDGER per band — planned,
    delivered at or above, swapped (S1), named misses (RL-1: every slot at its planned band, swapped, or named); (2) E3
    — the paper's mean ladder position per scope against its real past questions' ('harder' / 'equal' within
    bc.E3_EQUAL_BAND / 'easier' (AMBER)); (3) the FIGURE PLAN — planned against target per section and every recorded
    shortfall (FG-3). Print only — never a stop. Never raises."""
    try:
        bs = batch_state if isinstance(batch_state, dict) else {}
        cm = concept_map if isinstance(concept_map, dict) else {}
        labs = list(labels or bs.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
        tg = {str(k): v for k, v in (bs.get('difficulty_plan_target') or bs.get('difficulty_plan') or {}).items()}
        out = []
        if tg:
            rows, misses = [], []
            _swl = [s for s in ((bs.get('difficulty_state') or {}).get('band_swaps') or []) if isinstance(s, dict)]
            sw = {s.get('up') for s in _swl}
            pairs = {str(s.get('pair')): s for s in _swl}
            for b in labs:
                qs = [q for q, t in tg.items() if t == b]
                if not qs:
                    continue
                ok = [q for q in qs if (cm.get(q) or {}).get('difficulty') in labs
                      and labs.index((cm.get(q) or {}).get('difficulty')) >= labs.index(b)]
                up = [q for q, e in cm.items() if q in sw and isinstance(e, dict) and e.get('difficulty') == b]
                rows.append(f"{b} {len(ok) + len(up)}/{len(qs)}" + (f" ({len(up)} swapped)" if up else ''))
                misses += [f"Q{q} planned {b}, delivered {(cm.get(q) or {}).get('difficulty')}" for q in qs
                           if q not in ok and q not in pairs]
            out.append('DIFFICULTY SLOTS: ' + '; '.join(rows) + (' — every slot at or above its planned band'
                                                               if not misses else ''))
            for _pq, _s in sorted(pairs.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 0):
                out.append(f"DIFFICULTY: Q{_s.get('up')} (planned {_s.get('from')}) measured {_s.get('to')}; Q{_pq} "
                           f"(planned {_s.get('to')}) delivered {(cm.get(_pq) or {}).get('difficulty')} — labels swapped (S1)")
            if misses:
                out.append('DIFFICULTY (AMBER): below the planned band — ' + '; '.join(sorted(misses, key=lambda x: int(
                    x.split(' ')[0][1:]) if x.split(' ')[0][1:].isdigit() else 0)))
        if isinstance(ladder, dict) and ladder.get('status') == 'ok':
            by = {}
            for q, e in cm.items():
                dc = (e or {}).get('difficulty_check') if isinstance(e, dict) else None
                if isinstance(dc, dict) and isinstance(dc.get('p_new'), (int, float)):
                    by.setdefault(bc.ld_scope_for(ladder, e.get('subject'), e.get('subtopic_id')), []).append(float(dc['p_new']))
            for sc, ps in sorted((k, v) for k, v in by.items() if k):
                sids = [str(x) for x in ((ladder.get('scopes') or {}).get(sc) or {}).get('subtopic_of', {}).values()] or None
                rl = bc.ld_real_shares(ladder, labs, sids)
                if not rl:
                    continue
                mn = sum(ps) / len(ps)
                d = mn - rl['mean']
                word = 'equal' if abs(d) <= bc.E3_EQUAL_BAND else ('harder' if d > 0 else 'easier')
                out.append(f"PAPER LEVEL {sc}: mean ladder position {mn:.2f} vs the real exam {rl['mean']:.2f} — {word}"
                           + (' (AMBER)' if word == 'easier' else ''))
        fp = bs.get('figure_plan') if isinstance(bs.get('figure_plan'), dict) else {}
        for sec, pl in sorted(fp.items()):
            if not isinstance(pl, dict) or not pl.get('target'):
                continue
            drawn = [q for q in (pl.get('granted') or []) if isinstance(cm.get(str(q)), dict)
                     and (cm[str(q)].get('figure_dicts') or cm[str(q)].get('figure_files'))]
            short = [f"Q{q} text ({(cm.get(str(q)) or {}).get('fig_short', {}).get('reason', 'no record')})"
                     for q in (pl.get('granted') or []) if str(q) not in [str(x) for x in drawn]]
            cap = sum(int(s.get('n') or 0) for s in (pl.get('short') or []) if isinstance(s, dict) and s.get('reason') == 'capacity')
            line = f"FIGURES {sec}: target {pl.get('target')}, delivered {len(drawn)}"
            if short or cap:
                line += ' — ' + '; '.join(short + ([f'{cap} slot(s) short: fewer figure-capable slots than the target']
                                                   if cap else [])) + ' (AMBER)'
            out.append(line)
        return out
    except Exception as _e:                             # noqa: BLE001 — a footer line never stops a paper
        return [f'DIFFICULTY: release 2026.11.24 footer lines unavailable ({type(_e).__name__})']


def bv_batch_step(exam, n, ruler=None, manifest=None, bank=None, op_profile=None, home='/home/claude', echo=True,
                  final=False, defer=False, terminal=None, ladder=None):
    """THE in-batch step of Create S4-7 STEP A2 (S0-BC, GAP-2026-11-14-BATCH-COMPLETE), for the CURRENT batch of paper
    <exam> M<n>. v1.22: every question of the batch is SETTLED or DISCLOSED here (LAW-BC-1) through one bounded ladder
    (bc.bc_apply): three reviewers count as solvers, a disputed answer goes to ONE fresh adjudicator (job folder
    '<q>_adj'), a re-key keeps the question, rung 1 FIX -> rung 2 REPLACE -> rung 3 FALLBACK -> R5b / the terminal.
    Idempotent and resume-safe: (1) collects every outstanding job whose sub-agent returned REVIEW DONE / ADJUDICATE
    DONE (lines in <home>/<exam>_M<n>_bv/returned.txt: '<job_dir> <reply line>'); (2) runs the within-paper checks
    (bc.intra_paper_duplicates / bc.key_leak_check over every question up to this batch); (3) decides every question
    (bc.bc_apply) and keeps the state in batch_state['bv']['items']; (4) writes the jobs still needed (reviewer jobs
    split per SESSION_BUDGET.json review_qs_per_job; one adjudicator job per disputed question; a re-ask goes to a
    '_switch' folder — another model). A question of an EARLIER batch that is not settled (a paper begun on an earlier
    release — key_chain, unlabelled, carried — or one bc_reopen named) joins this batch's work. Nothing is carried:
    INFRA-CARRY, unmeasured and key_chain do not exist after DONE. final=True: the SETTLEMENT BATCH 'S' of a migrating
    paper (S4-12) — every question of the paper not yet settled. Returns {'status': 'jobs_out' | 'rewrite' | 'no_model'
    | 'stop' | 'done', 'jobs', 'rewrite', 'permute', 'restore', 'settled', 'disclosed', 'no_model', 'key_chain' ([]),
    'open' ([]), 'pending' ([]), 'lines'} and prints the lines (echo)."""
    import json, os, shutil
    _lines = []

    def _say(x):
        _lines.append(str(x))
        if echo:
            print(x)
    _bsp_bv = os.path.join(home, f'{exam}_M{n}_batch_state.json')
    _kp_bv = os.path.join(home, f'{exam}_M{n}_answer_key.json')
    _bs_bv = json.load(open(_bsp_bv, encoding='utf-8'))
    _kd_bv = json.load(open(_kp_bv, encoding='utf-8'))
    _cm_bv = _kd_bv.setdefault('concept_map', {})
    _ans_bv = _kd_bv.setdefault('answers', {})
    _labs_bv = list(_bs_bv.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
    _term = terminal if terminal in bc.BC_TERMINALS else bc.BC_TERMINAL
    _st_bv = _bs_bv.setdefault('bv', {})
    _items0 = _st_bv.get('items') or {}
    # Cluster R3 (release 2026.11.21): the paper's difficulty mode, frozen once (bv_difficulty_mode)
    _lad_bv = ladder if isinstance(ladder, dict) else bv_load_ladder(exam, home)
    _mode_bv = bv_difficulty_mode(_bs_bv, _lad_bv)
    _r3_bv = _mode_bv != bc.R3_MODE_LEGACY
    if _mode_bv == bc.R3_MODE_LADDER and _bs_bv.get('ladder_fingerprint') \
            and bc.ld_fingerprint(_lad_bv) != _bs_bv.get('ladder_fingerprint'):
        # the ladder the paper started on is not the one loaded now (a lost staged copy, a re-built file attached):
        # the paper continues on the loaded one and the footer says so — never a stop
        _nt = (f"DIFFICULTY (AMBER): the difficulty ladder changed during this paper (started on "
               f"{_bs_bv.get('ladder_fingerprint')}, batch {_bs_bv.get('current_batch')} used "
               f"{bc.ld_fingerprint(_lad_bv) or 'none'}) — later questions were placed on the ladder loaded then.")
        if _nt not in (_bs_bv.get('r3_notes') or []):
            _bs_bv.setdefault('r3_notes', []).append(_nt)

    def _open_q(q):
        """A question that still needs work: not settled / disclosed under BC1 on its current text; under BV1 (an
        earlier release) a question in key_chain / unlabelled / open / a pending attempt, or with no unanimous key."""
        e = _cm_bv.get(q) if isinstance(_cm_bv.get(q), dict) else None
        if e is None:
            return False
        it0 = _items0.get(q) if isinstance(_items0.get(q), dict) else {}
        if it0.get('rule') == bc.BC_RULE:
            # GAP-2026-11-20 F9: a decided TEXT fallback that still carries a figure is open — STEP A2 owns its repair
            # (bounded by bc.BC_FALLBACK_FIGURE_ORDERS, then R5b / kept + disclosed), so STEP A3 never waits on it
            return not (it0.get('state') in bc.BC_STATES and e.get('bv_state') in bc.BC_STATES
                        and it0.get('content_sha') == _bc_entry_sha(_bc_render_shas(e))) \
                or bc.bc_fallback_figure_open(dict(e, bv=it0), bc_figure_intrinsic(_bs_bv, q)[1])
        if e.get('bv_state') in ('key_chain', 'unlabelled', 'open'):
            return True
        kv = e.get('key_votes') if isinstance(e.get('key_votes'), dict) else {}
        if kv.get('content_sha') and kv.get('content_sha') != bc.op_content_sha(e):
            return True                                 # rewritten after its key votes (a legacy chain): measured again
        if it0:
            return it0.get('state') != 'settled'
        return kv.get('unanimous') is not True
    _plan = _bs_bv.get('batch_plan') or []
    if final:
        _qall = sorted((q for q in _cm_bv if str(q).isdigit()), key=int)
        _bp_bv = {'batch_id': 'S', 'q_start': int(_qall[0]) if _qall else 1, 'q_end': int(_qall[-1]) if _qall else 0}
        _qs_bv = [q for q in _qall if _open_q(q)]
    else:
        _bp_bv = _plan[int(_bs_bv.get('current_batch', 1)) - 1]
        _qs_bv = [str(q) for q in range(int(_bp_bv['q_start']), int(_bp_bv['q_end']) + 1) if str(q) in _cm_bv]
        # migration (S4-12) and the last batch's re-open rule (P2): an earlier question that is not settled joins this
        # batch's work; it is named in the batch report
        _early = [q for q in sorted((q for q in _cm_bv if str(q).isdigit() and int(q) < int(_bp_bv['q_start'])), key=int)
                  if q in (_st_bv.get('reopen') or {}) or q in set(str(x) for x in (_bs_bv.get('bv_carry') or []))
                  or (q in _items0 and _open_q(q)) or ((_cm_bv.get(q) or {}).get('bv_state') in ('key_chain', 'unlabelled', 'open'))]
        _qs_bv = _early + [q for q in _qs_bv if q not in _early]
    _tgt_bv = {str(k): v for k, v in (_bs_bv.get('difficulty_plan_target') or _bs_bv.get('difficulty_plan') or {}).items()}
    _ru_bv = ruler or {}
    _man_bv = manifest or {}
    _bank_bv = bank or {}
    # release 2026.11.24 — the per-question gate context: the paper's figure plan (FG-1 / FG-5, written by Create S3;
    # built here from the blueprint when absent), the exam's measured ask form (D1) and the planned statement counts
    # (RP-2), both written by Create S3 into batch_state['stem_form'] (absent = dormant)
    _fp_bv = _bs_bv.get('figure_plan') if isinstance(_bs_bv.get('figure_plan'), dict) else {}
    if 'figure_plan' not in _bs_bv:                     # a paper begun before 2026.11.24 (S3-16 records it, {} included)
        _fp_bv = bv_figure_plan_fallback(exam, n, home, _bs_bv)
        if _fp_bv:
            _bs_bv['figure_plan'] = _fp_bv
    _granted_bv = {str(q) for _sp in _fp_bv.values() if isinstance(_sp, dict) for q in (_sp.get('granted') or [])}
    _sf_bv = _bs_bv.get('stem_form') if isinstance(_bs_bv.get('stem_form'), dict) else {}

    def _fig_specs_of(_q):
        import glob as _glf
        _out = []
        for _fs in sorted(_glf.glob(os.path.join(home, f'q{_q}_*.figspec.json'))):
            try:
                _d = json.load(open(_fs, encoding='utf-8'))
            except (OSError, ValueError):
                continue
            if isinstance(_d, dict):
                _out.append(dict(_d, file=os.path.basename(_fs)[:-len('.figspec.json')] + '.png'))
        return _out

    def _gctx(_q, _e):
        _afm = _sf_bv.get('ask_form') if isinstance(_sf_bv.get('ask_form'), dict) else {}
        _nsm = _sf_bv.get('n_statements') if isinstance(_sf_bv.get('n_statements'), dict) else {}
        _nst = _nsm.get(str(_q))
        _psp = (_bs_bv.get('shape_plan') or {}).get(str(_q)) if isinstance(_bs_bv.get('shape_plan'), dict) else None
        return {'figure_granted': str(_q) in _granted_bv,
                'ask_form': _afm.get(str((_e or {}).get('section') or '')) or _afm.get('*'),
                'n_statements': _nst if isinstance(_nst, int) and not isinstance(_nst, bool) else None,
                # release 2026.11.25 (P6): the slot's frozen S3-12d shape — pre-review G-SHAPEPLAN (non-blocking)
                'planned_shape': _psp if isinstance(_psp, str) else None,
                # release 2026.11.25 (GAP-2026-11-19-FIGURE-LOSS F4): this question's FigureSpec records (the native
                # renderer's on-page scale) — pre-review G-FIG-SCALE (non-blocking)
                'figure_specs': _fig_specs_of(_q),
                # release 2026.11.27 (GAP-2026-11-21): G-MATH-TYPESET (strict item) / G-FIG-NEED (non-inert item), both
                # soft; {} for an inert (chemistry) item or a paper without batch_state['math_typeset'] (dormant)
                **bc.mt_gate_context(_bs_bv.get('math_typeset'), (_e or {}).get('subject')
                                     or bc.nf_subject_key(_e or {}, _man_bv), (_e or {}).get('subtopic_id'))}
    _root_bv = os.path.join(home, f'{exam}_M{n}_bv')
    os.makedirs(_root_bv, exist_ok=True)
    if _st_bv.get('batch') != _bp_bv['batch_id']:
        _keep_items = dict(_st_bv.get('items') or {})          # every earlier batch's record
        _keep_reopen = dict(_st_bv.get('reopen') or {})
        _st_bv.clear()
        _st_bv.update({'batch': _bp_bv['batch_id'], 'round': 0, 'jobs': [], 'status': 'open', 'items': _keep_items,
                       'rule': bc.BC_RULE, 'reopen': _keep_reopen})
    _st_bv['rule'] = bc.BC_RULE
    _ret_bv = {}
    if os.path.exists(os.path.join(_root_bv, 'returned.txt')):
        for _ln in open(os.path.join(_root_bv, 'returned.txt'), encoding='utf-8'):
            _pp = _ln.strip().split(' ', 1)
            if len(_pp) == 2:
                _ret_bv[_pp[0]] = _pp[1]
    try:
        import figural_vision as _fv_bv
        import corpus_io as _ci_bv
        _vcmp_bv = _fv_bv.readback_compare
        _vprf_bv = lambda _fd: _ci_bv.organic_figure_proof(bc_figure_with_layout(_fd))   # v1.24 D1: same rule as S13-2P
    except Exception:                                   # noqa: BLE001 — dormant: G-FIGRECORD / S3-17c cover it
        _vcmp_bv, _vprf_bv = None, None
    # 1. COLLECT every outstanding job whose fresh sub-agent returned DONE
    _res_bv = {}
    for _j in _st_bv.get('jobs') or []:
        _rp = os.path.join(_j['dir'], 'result.json')
        _line = str(_ret_bv.get(_j['dir'], ''))
        _role_j = str(_j.get('role', ''))
        if _role_j.startswith('reviewer_'):
            if _line.startswith('REVIEW DONE') and os.path.exists(_rp):
                try:
                    _rv = json.load(open(_rp, encoding='utf-8'))
                except (OSError, ValueError):
                    _rv = None
                _k = int(_role_j.rsplit('_', 1)[-1])
                _split = bc.bv_split_reviewer_result(_k, _rv, _labs_bv, _j.get('qs'), _j['sha256'],
                                                     {q: (_cm_bv.get(q) or {}).get('figure_dicts') for q in (_j.get('qs') or [])},
                                                     tasks_by_q=(_j.get('tasks') or {}) if _j.get('r3') else None)
                for _q2, _rr in _split.items():
                    _res_bv.setdefault(_q2, {}).update(_rr)
            continue
        if _role_j == 'adjudicator':
            if _line.startswith('ADJUDICATE DONE') and os.path.exists(_rp):
                try:
                    _ra = json.load(open(_rp, encoding='utf-8'))
                except (OSError, ValueError):
                    _ra = None
                if isinstance(_ra, dict) and bc.bc_read_adjudication(_ra) is not None:
                    _res_bv.setdefault(str(_j['q']), {})['adjudicator'] = {'result': _ra, 'sha256': _j['sha256'],
                                                                         'context': 'fresh'}
            continue
        _ok_j = _line.startswith(('GRADE DONE', 'SOLVE DONE', 'VISION DONE'))   # a per-role job of release 2026.11.11
        _r = None
        if _ok_j and os.path.exists(_rp):
            try:
                _r = bc.bv_read_result(_j['role'], json.load(open(_rp, encoding='utf-8')), _labs_bv)
            except (OSError, ValueError):
                _r = None
        if _r is not None:
            _res_bv.setdefault(_j['q'], {})[_j['role']] = {'result': _r, 'sha256': _j['sha256'], 'context': 'fresh'}
    # S0-NF-6 IN THE BATCH: a repeat of an earlier question's template / an answer leak (the later of the two)
    _all_bv = []
    _qmax = max([int(_bp_bv['q_end'])] + [int(q) for q in _qs_bv])
    for _qa, _ea in _cm_bv.items():
        if not isinstance(_ea, dict) or not str(_qa).isdigit() or int(_qa) > _qmax:
            continue
        _oa = list(_ea.get('option_texts') or [])
        _ka = _ans_bv.get(str(_qa))
        _kt = (_oa[int(_ka) - 1] if (_oa and str(_ka).isdigit() and 1 <= int(_ka) <= len(_oa))
               else (None if _oa or isinstance(_ka, (list, dict)) or _ka is None else str(_ka)))
        _all_bv.append(dict(_ea, q=str(_qa), key_text=_kt,
                            concept=((_ea.get('grader_meta') or {}).get('grader_1') or {}).get('concept')))
    _all_bv.sort(key=lambda x: int(x['q']))
    _fnd_bv = {}
    for _a, _b, _w in bc.intra_paper_duplicates(_all_bv):
        if str(_b) in _qs_bv:
            _fnd_bv.setdefault(str(_b), []).append(f'repeats Q{_a} ({_w}) — write another task / dataset')
    if _r3_bv:
        # G-INTRAPAPER-FACT (Cluster R3): the same tested fact, whatever the subtopic or concept wording
        _facts = []
        for _x in _all_bv:
            _bvx = (_st_bv.get('items') or {}).get(_x['q']) or {}
            _df = next((_s.get('decisive_fact') for _s in ((_bvx.get('solvers') or {}).values()
                                                            if isinstance(_bvx.get('solvers'), dict) else [])
                        if isinstance(_s, dict) and _s.get('decisive_fact')), None)
            _facts.append(dict(_x, decisive_fact=_df))
        for _a, _b, _w in bc.qg_fact_overlap(_facts):
            if str(_b) in _qs_bv:
                _fnd_bv.setdefault(str(_b), []).append(f'repeats the fact tested by Q{_a} ({_w}) — test another fact')
    _pyq_bv = ([r.get('stem_snippet') for r in bc.pyq_guard_pool(op_profile)
                if isinstance(r, dict) and r.get('stem_snippet')] if op_profile else [])
    for _a, _b, _v in bc.key_leak_check(_all_bv, _pyq_bv):
        _cand = [x for x in (str(_a), str(_b)) if x in _qs_bv]
        if _cand:
            _x = max(_cand, key=int)
            _o = str(_b) if _x == str(_a) else str(_a)
            _fnd_bv.setdefault(_x, []).append(f'answer leak with Q{_o} ({_v}) — change the data so the value is not given')
    # a re-opened earlier question (P2): its gate finding is a hard finding for the ladder
    for _q, _rs in (_st_bv.get('reopen') or {}).items():
        if _q in _qs_bv:
            _fnd_bv.setdefault(_q, []).extend('GATE: ' + str(x) for x in _rs)
    # 2. DECIDE every question (bc.bc_apply) and 3. WRITE the jobs still needed
    _acts_bv, _new_jobs, _needs_bv, _adj_q = {}, [], {}, []
    _perm, _rest, _nm = {}, {}, {}
    _sc_back, _sc_missing = {}, []                      # v1.23 P3: author self-count misses / missing counts
    _pre_back = {}                                      # v1.24 D1-D3: pre-review gaps
    try:                                                # STEP B wrote the per-batch auditor's item findings here
        _pre_doc = json.load(open(os.path.join(home, f'{exam}_M{n}_batch_findings.json'), encoding='utf-8'))
    except (OSError, ValueError):
        _pre_doc = None
    _jr_bv = int(_st_bv.get('round', 0))               # job rounds issued so far for this batch
    _left = max(0, int(bc.BV_MAX_ROUNDS) - _jr_bv)
    _asked_all = _st_bv.setdefault('asked', {})
    # LAW-BC-9 RESUME: the step after a NO-MODEL re-asks the missing results even when the quality round budget is spent
    # (an infrastructure round is not a quality round — it never starts a rung: bc_apply still sees rounds_left); without
    # this a NO-MODEL at the cap could never be resumed (found by the 600-paper property fuzz, invariant I8)
    _resume_infra = str(_st_bv.get('status') or '') == 'no_model'

    def _decide(_q, _e, _mx):
        _cr = _e.get('ca_range') if isinstance(_e.get('ca_range'), (list, tuple)) and len(_e.get('ca_range')) == 2 else None
        try:
            _tol = (abs(float(_cr[1]) - float(_cr[0])) / 2.0) if _cr else None
        except (TypeError, ValueError):
            _tol = None
        _fi, _fe = bc_figure_intrinsic(_bs_bv, _q)
        return bc.bc_apply(_e, _tgt_bv.get(_q), _labs_bv, _ru_bv, _ans_bv.get(_q), str(_e.get('qtype') or 'mcq'), _tol,
                           results=_res_bv.get(_q) or {}, findings=_fnd_bv.get(_q), vision_compare=_vcmp_bv,
                           figure_proof=_vprf_bv, asked=_asked_all.get(_q), max_asks=_mx, rounds_left=_left,
                           figure_intrinsic=_fi, family_engine=_fe, terminal=_term)
    for _q in _qs_bv:
        _e = dict(_cm_bv[_q])
        if isinstance((_st_bv.get('items') or {}).get(_q), dict):
            _e['bv'] = _st_bv['items'][_q]
        if _r3_bv:
            _e['difficulty_mode'] = _mode_bv
            # release 2026.11.25 (P13, LAW-RECORD-READER-1): in a count-free mode the ENGINE writes difficulty_obs —
            # {'qtype', 'mode'} — whatever the worker passed; anything else the worker recorded is archived, never read
            # by a decision (A-QINDEX check 9 then gives the same answer for every worker on the same paper)
            _rec_obs, _arch_obs = bc.difficulty_obs_engine_record(_e, _mode_bv)
            if _arch_obs:
                if _arch_obs.get('moves') and not _e.get('author_moves'):
                    _e['author_moves'] = _arch_obs.get('moves')        # the adjudicator packet reads it
                _e.setdefault('difficulty_obs_author', _arch_obs)
            _e['difficulty_obs'] = _rec_obs
            # a HARD gate still failing after the pre-review tries of this rung enters the rung ladder (bounded)
            _rk0 = str(((_e.get('bv') or {}).get('rung')) or 0)
            if int((((_st_bv.get('prereview') or {}).get(_q) or {}).get(_rk0)) or 0) >= int(bc.BC_PREREVIEW_TRIES):
                _top0 = bool(_labs_bv) and _tgt_bv.get(_q) == _labs_bv[-1]
                for _hx in [x for x in bc.qg_item_gates(_e, _ans_bv.get(_q), _top0) if bc.r3_hard_gate(x)]:
                    if 'GATE: ' + _hx not in (_fnd_bv.get(_q) or []):
                        _fnd_bv.setdefault(_q, []).append('GATE: ' + _hx)
        _e.setdefault('subject', bc.nf_subject_key(_e, _man_bv))
        _e.setdefault('manifest_hash', bc.manifest_hash(_man_bv))
        _e.pop('bc.manifest_hash', None)                # a key mis-written by release 2026.11.11
        if _q in (_st_bv.get('reopen') or {}) and (_e.get('bv') or {}).get('state') in bc.BC_STATES:
            # re-opened: decided again on its current text with the gate finding as a hard finding
            _e['bv'] = dict(_e['bv'], state='grading', reopened_in_last_batch=True)
            _e.pop('bv_state', None)
        _e = _bc_render_shas(_e)
        _e = bc_stimulus_fill(_e, _q, _bs_bv)           # v1.24: a set member's reviewers read the set's stimulus
        _r = _decide(_q, _e, bc.BC_ROLE_ASKS)
        if _r['action'] == 'grade' and _left < 1 and not _resume_infra:
            # R11 at the round cap: decide with the results that exist (minimum results / R5b / terminal / NO-MODEL)
            _r = _decide(_q, _r['entry'], 0)
        if _r['action'] == 'adjudicate' and _left < 1:
            _r = _decide(_q, _r['entry'], 0)
        if _r['action'] in bc.BC_STATES and bc.bc_fallback_figure_open(_r['entry'], bc_figure_intrinsic(_bs_bv, _q)[1]):
            # GAP-2026-11-20 F9: settled as the TEXT fallback with a figure still on it — the repair is decided in THIS
            # step (order to drop it / R5b / kept + disclosed), never left for STEP A3 to refuse
            _r = _decide(_q, _r['entry'], bc.BC_ROLE_ASKS)
        if _r['action'] == 'grade' and not _asked_all.get(_q) and not _res_bv.get(_q):
            # v1.23 P3 (G-SELFCOUNT): before the FIRST reviewer round of a text, the author's own count must give the
            # slot band — a miss goes back to the author (no reviewer is paid), at most bc.BC_SELFCOUNT_TRIES times per
            # rung, then the text is reviewed anyway (never a loop, never a stop); missing counts are only reported
            _sc = (bc.bc_selfcount(_r['entry'], _tgt_bv.get(_q), _labs_bv) if not _r3_bv
                   else {'status': 'n/a', 'why': 'Cluster R3: the writer is never measured against a count'})
            _rk = str((_r['entry'].get('bv') or {}).get('rung') or 0)
            _scs = _st_bv.setdefault('selfcount', {}).setdefault(_q, {})
            if _sc['status'] == 'fail' and int(_scs.get(_rk) or 0) < int(bc.BC_SELFCOUNT_TRIES):
                _scs[_rk] = int(_scs.get(_rk) or 0) + 1
                _sc_back[_q] = dict(_sc, try_no=_scs[_rk])
            elif _sc['status'] == 'missing':
                _sc_missing.append(_q)
            # v1.24 (GAP-2026-11-15-RUN-ANALYSIS D1-D3): PRE-REVIEW — the figure proof (identity + gates, computed by
            # the engine), the packet the reviewers will get (lists / figure present) and the per-batch auditor's item
            # findings for this text; a gap goes back to the author with no reviewer started, at most
            # bc.BC_PREREVIEW_TRIES times per rung, then the text is reviewed as it stands (never a loop)
            if _q not in _sc_back and not bc_text_has_results(_r['entry']):
                _pg = bc_prereview_gaps(_r['entry'], _q, _pre_doc) + (
                    bv_r3_gaps(_r['entry'], _ans_bv.get(_q), bool(_labs_bv) and _tgt_bv.get(_q) == _labs_bv[-1],
                               _lad_bv, _mode_bv, context=_gctx(_q, _r['entry'])) if _r3_bv else [])
                _pgs = _st_bv.setdefault('prereview', {}).setdefault(_q, {})
                if _pg and int(_pgs.get(_rk) or 0) < int(bc.BC_PREREVIEW_TRIES):
                    _pgs[_rk] = int(_pgs.get(_rk) or 0) + 1
                    _pre_back[_q] = {'gaps': _pg, 'try_no': _pgs[_rk]}
        _cm_bv[_q] = _r['entry']
        _st_bv.setdefault('items', {})[_q] = _r['entry'].get('bv')
        _acts_bv.setdefault(_r['action'], []).append(_q)
        if _r['action'] in ('settled', 'disclosed') and _q in (_st_bv.get('reopen') or {}):
            _st_bv['reopen'].pop(_q, None)
        if _r['action'] in ('rewrite', 'permute', 'restore'):
            _asked_all.pop(_q, None)                    # the next text is new content: its roles have not been asked
        if _r['action'] == 'rewrite' and ((_r['entry'].get('bv') or {}).get('climb_brief') or {}).get('kind') == 'fallback' \
                and not bc_figure_intrinsic(_bs_bv, _q)[1]:
            # C3: the rung-3 text question has no figure record (an R10 family-engine item is a figure: kept)
            if bc_fallback_clear_figure(exam, n, _q, home, bs=_bs_bv):
                _say(f"STEP A2: Q{_q} goes to the rung-3 TEXT fallback — its figure record was removed (fig_manifest).")
        if _r['action'] == 'restore' and isinstance(_r.get('restore'), dict) and (
                ((_r['restore'].get('entry') or {}).get('figure_files')) or ((_r['restore'].get('entry') or {}).get('figure_dicts'))):
            # C3: R5b puts back an earlier FIGURE version — its figure record comes back with it
            if bc_fallback_restore_figure(exam, n, _q, home, bs=_bs_bv):
                _say(f"STEP A2: Q{_q} — the restored version has a figure: its figure record was put back (fig_manifest).")
        if _r['action'] in bc.BC_STATES and ((_r['entry'].get('bv') or {}).get('fallback_figure_kept')):
            # GAP-2026-11-20 F9: delivered WITH its figure (disclosed) — the figure record removed at the fallback order
            # comes back, so the per-batch auditor counts the slot as the figure question it is
            if bc_fallback_restore_figure(exam, n, _q, home, bs=_bs_bv):
                _say(f"STEP A2: Q{_q} — the text fallback kept its figure (F9, disclosed): its figure record was put "
                     f"back (fig_manifest).")
        if _r.get('reset_asks'):
            _ak0 = _asked_all.setdefault(_q, {})
            for _rl in _r['reset_asks']:
                _ak0.pop(_rl, None)
        if _r.get('answer') is not None and _r['action'] in ('settled', 'disclosed'):
            # a re-key that keeps its position, R5b or the terminal: the delivered key changes (the docx never shows it)
            _ans_bv[_q] = _r['answer']
        if _r['action'] == 'permute':
            _perm[_q] = {'swap': _r['swap'], 'answer': _r['answer']}
        if _r['action'] == 'restore':
            _rp_f = os.path.join(_root_bv, f'restore_q{_q}.json')
            json.dump(_r['restore'], open(_rp_f, 'w', encoding='utf-8'), indent=1, default=str, ensure_ascii=False)
            _rest[_q] = _rp_f
        if _r['action'] == 'no_model':
            _nm[_q] = _r.get('why')
            _asked_all.pop(_q, None)                    # LAW-BC-9: the resume re-asks from a clean count
        if _r['action'] == 'adjudicate':
            _adj_q.append(_q)
        elif _r['roles']:
            _needs_bv[_q] = list(_r['roles'])
            if _r.get('also_adjudicate'):
                # release 2026.11.24 (B4 + C1): the one re-measure and the adjudicator run in the SAME round (one wave)
                _adj_q.append(_q)
        if _r['action'] in ('disclosed',) and 'terminal' in ((_r['entry'].get('bv') or {}).get('amber') or []):
            _p0 = _bs_bv.setdefault('p0_incidents', [])
            if not any(x.get('q') == _q and x.get('kind') == 'bc_terminal' for x in _p0 if isinstance(x, dict)):
                _p0.append({'q': _q, 'kind': 'bc_terminal', 'why': (_r['entry'].get('bv') or {}).get('terminal'),
                            'rule': 'LAW-BC-2 / BC_TERMINAL adjudicated_disclosed'})
    # release 2026.11.24 (FG-3): a slot the figure plan granted that settled with no figure (G-FIG-MISSING after its
    # pre-review tries) is RECORDED on its entry — the auditor (A-AXIS1) counts it at its planned format, disclosed
    for _q in _qs_bv:
        _ef = _cm_bv.get(_q) if isinstance(_cm_bv.get(_q), dict) else {}
        if _q in _granted_bv and _ef.get('bv_state') in bc.BC_STATES and not (_ef.get('figure_dicts') or _ef.get('figure_files')) \
                and not isinstance(_ef.get('bc_fallback'), dict):
            _ef['fig_short'] = {'reason': 'not_drawn', 'rule': 'FG-3'}
        elif isinstance(_ef.get('fig_short'), dict) and (_ef.get('figure_dicts') or _ef.get('figure_files')):
            _ef.pop('fig_short', None)
    for _q in _sc_back:
        _acts_bv.setdefault('selfcount', []).append(_q)
        if _q in (_acts_bv.get('grade') or []):
            _acts_bv['grade'].remove(_q)
    for _q in _pre_back:
        _acts_bv.setdefault('prereview', []).append(_q)
        if _q in (_acts_bv.get('grade') or []):
            _acts_bv['grade'].remove(_q)
    if _sc_back or _pre_back or _acts_bv.get('rewrite') or _perm or _rest:
        # v1.23 (P3, C4): the TEXT WORK comes first — a step that asks for a rewrite, a permutation, a restore or a
        # self-count fix writes no job (no round is spent); the next run of this block issues every job of the round
        # together (the rewritten texts' reviewers with the others' adjudicators — one wave). Before 1.23 a rewrite
        # asked in a step that also wrote jobs was printed only as JOBS OUT, so the worker handed the jobs over, the
        # text was never rewritten and the ladder moved on from the same text (a rung lost — found by the fuzz).
        _needs_bv, _adj_q = {}, []
    # the round folder: a quality round r<k>; a LAW-BC-9 resume beyond the budget r<k>i<j> (never reuses a folder)
    _rlabel = (f"r{_jr_bv}i{int(_st_bv.get('infra_rounds') or 0) + 1}" if (_left < 1 and _resume_infra)
               else f"r{_jr_bv + 1}")
    # 3. WRITE the fresh jobs: reviewer jobs (k = 1..3, split per review_qs_per_job) and one adjudicator per question
    def _copy_into(_d, _f):
        if _f and os.path.exists(str(_f)):
            _dst = os.path.join(_d, os.path.basename(str(_f)))
            shutil.copy(str(_f), _dst)
            return _dst
        return None
    if _needs_bv:
        _bg_bv = bc.bv_band_guide(_ru_bv, _labs_bv) if not _r3_bv else {}
        _anc_bv = {q: bc.bv_anchors(_bank_bv, _ru_bv, (_cm_bv[q] or {}).get('subtopic_id'),
                                    str((_cm_bv[q] or {}).get('qtype') or 'mcq'), _labs_bv) for q in _needs_bv} if not _r3_bv else {}
        _tasks_bv = {}
        if _mode_bv == bc.R3_MODE_LADDER and isinstance(_lad_bv, dict):
            # Cluster R3 §6.3 / release 2026.11.24 rule r3.1 (B1, S1): each item's placement task PER REVIEWER — its own
            # seeded draw of complete anchors around its band's cut (plus the upper probe of a middle band), shuffled
            # with the item under opaque labels; the one re-measure (B4) draws again; an item with no anchor set is
            # measured with the r2.1 counts
            for _q4 in _needs_bv:
                if not any(str(_r4).startswith('grader_') for _r4 in (_needs_bv.get(_q4) or [])) or _tgt_bv.get(_q4) is None:
                    continue
                _e4 = _cm_bv.get(_q4) or {}
                _rc4 = ((_e4.get('bv') or {}).get('recount')) if isinstance(_e4.get('bv'), dict) else None
                _rm4 = ':rc' if isinstance(_rc4, dict) and _rc4.get('kind') == 'placement' else ''
                _sc4 = bc.ld_scope_for(_lad_bv, _e4.get('subject') or bc.nf_subject_key(_e4, _man_bv), _e4.get('subtopic_id'))
                for _k4 in range(1, len(bc.BV_ROLES_GRADE) + 1):
                    _salt4 = f"{exam}:{n}:{_q4}:{bc.op_content_sha(_e4)[:12]}:k{_k4}{_rm4}"
                    _as4 = bc.ld_anchor_set(_lad_bv, _sc4, _tgt_bv.get(_q4), _labs_bv, _e4.get('subtopic_id'),
                                            _e4.get('ask_format'), salt=_salt4, upper=True)
                    _tk4 = bc.ld_placement_task(_as4, bc.r3_item_text(_e4), salt=_salt4)
                    if _tk4:
                        _tasks_bv[(_q4, _k4)] = _tk4
        _qpj = bv_review_qs_per_job(home)
        # v1.23 (P1): the round's reviewer jobs + adjudicator jobs fit in ONE wave of parallel_jobs_max
        _mjr = bc.bv_round_job_caps(bv_budget_value('parallel_jobs_max', 6), len(_adj_q))
        for _jb in bc.bv_reviewer_jobs(_needs_bv, _cm_bv, _anc_bv, _labs_bv, _bg_bv, qs_per_job=_qpj,
                                       max_jobs_per_reviewer=_mjr):
            _kk0 = _jb['role'].rsplit('_', 1)[-1]
            _tk_k = {q: t for (q, k), t in _tasks_bv.items() if str(k) == str(_kk0)}   # this reviewer's own tasks
            if _r3_bv:
                # Cluster R3: rank / count task per item, enumerated defect codes, no band-labelled exemplars
                _jb['packet'] = dict({k: v for k, v in _jb['packet'].items() if k != 'band_guide'},
                                     items=bc.rp_attach_prior(bc.r3_reviewer_rows(_jb['packet']['items'], _tk_k), _cm_bv),
                                     counting_rules=bc.r3_counting_rules(), decision_rule=bc.R3_DECISION_RULE)
                # release 2026.11.27 (GAP-2026-11-21 C-E5): D-FIG-DECORATIVE is described only to a job carrying a
                # non-chemistry problem figure of a non-inert item; every other job keeps the default brief byte for byte
                _jb['brief'] = (bc.BV_BRIEF_REVIEWER_R3_FIG if bc.bv_brief_needs_fig(
                    {str(_q5): _cm_bv.get(_q5) for _q5 in _jb['qs']}, {str(_q5): _fig_specs_of(_q5) for _q5 in _jb['qs']},
                    _bs_bv.get('math_typeset'), _man_bv) else bc.BV_BRIEF_REVIEWER_R3)
            _reask = any(int((_asked_all.get(_q3) or {}).get(_rl) or 0) >= 1
                         for _q3 in _jb['qs'] for _rl in (_needs_bv.get(_q3) or []) if _rl.endswith('_' + _kk0))
            _d = os.path.join(_root_bv, f"b{_bp_bv['batch_id']}", _rlabel,
                              _jb.get('name') or _jb['role']) + ('_switch' if _reask else '')
            os.makedirs(_d, exist_ok=True)
            _pk = json.loads(json.dumps(_jb['packet'], default=str))
            for _row in _pk['items']:
                if isinstance(_row.get('item'), dict) and _row['item'].get('figure_files'):
                    _row['item']['figure_files'] = [x for x in (_copy_into(_d, f) for f in _row['item']['figure_files']) if x]
                _row['figures_to_read'] = [x for x in (_copy_into(_d, f) for f in (_row.get('figures_to_read') or [])) if x]
            _sha = hashlib.sha256(json.dumps(_pk, sort_keys=True, default=str, ensure_ascii=False).encode('utf-8')).hexdigest()
            json.dump(_pk, open(os.path.join(_d, 'packet.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            open(os.path.join(_d, 'JOB_BRIEF.txt'), 'w', encoding='utf-8').write(_jb['brief'].replace('<JOB_DIR>', _d))
            _new_jobs.append(dict({'role': _jb['role'], 'qs': _jb['qs'], 'dir': _d, 'sha256': _sha},
                                  **({'r3': True, 'tasks': {q: {k: _tk_k[q].get(k) for k in ('map', 'meta', 'band', 'probe', 'cuts')}
                                                            for q in _jb['qs'] if q in _tk_k}}
                                     if _r3_bv else {})))
            for _q3 in _jb['qs']:
                for _rl in _needs_bv.get(_q3) or []:
                    if _rl.endswith('_' + _kk0):
                        _ak = _asked_all.setdefault(_q3, {})
                        _ak[_rl] = int(_ak.get(_rl) or 0) + 1
    for _q in _adj_q:
        _bvq = _st_bv['items'].get(_q) or {}
        _sv = [(_bvq.get('solvers') or {}).get(r) for r in bc.BV_ROLES_SOLVE if isinstance((_bvq.get('solvers') or {}).get(r), dict)]
        _aj = bc.bc_adjudicator_job(_q, _cm_bv[_q], _ans_bv.get(_q), _sv, _labs_bv,
                                    claims=_bvq.get('claims_pending'))   # release 2026.11.24 (C1)
        _reask = int((_asked_all.get(_q) or {}).get('adjudicator') or 0) >= 1
        _d = os.path.join(_root_bv, f"b{_bp_bv['batch_id']}", _rlabel, f'q{_q}_adj') + ('_switch' if _reask else '')
        os.makedirs(_d, exist_ok=True)
        _pk = json.loads(json.dumps(_aj['packet'], default=str))
        if _pk.get('item', {}).get('figure_files'):
            _pk['item']['figure_files'] = [x for x in (_copy_into(_d, f) for f in _pk['item']['figure_files']) if x]
        _sha = hashlib.sha256(json.dumps(_pk, sort_keys=True, default=str, ensure_ascii=False).encode('utf-8')).hexdigest()
        json.dump(_pk, open(os.path.join(_d, 'packet.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        open(os.path.join(_d, 'JOB_BRIEF.txt'), 'w', encoding='utf-8').write(_aj['brief'].replace('<JOB_DIR>', _d))
        _new_jobs.append({'role': 'adjudicator', 'q': _q, 'qs': [_q], 'dir': _d, 'sha256': _sha})
        _ak = _asked_all.setdefault(_q, {})
        _ak['adjudicator'] = int(_ak.get('adjudicator') or 0) + 1
    for _j in _st_bv.get('jobs') or []:
        _j['done'] = True
    _st_bv['jobs'] = _new_jobs
    _infra_round = bool(_new_jobs) and _left < 1 and _resume_infra
    if _new_jobs and not _infra_round:
        _st_bv['round'] = _jr_bv + 1
    elif _infra_round:
        _st_bv['infra_rounds'] = int(_st_bv.get('infra_rounds') or 0) + 1   # LAW-BC-9 re-asks beyond the quality budget
    if not _infra_round and _jr_bv + (1 if _new_jobs else 0) > int(bc.BV_MAX_ROUNDS):
        # impossible by construction (R11 decides at the cap); an engine defect is recorded, never a carry
        _bs_bv.setdefault('p0_incidents', []).append({'kind': 'bc_round_cap', 'round': _jr_bv + 1,
                                                      'rule': 'LAW-BC-2 round budget'})
    _ds_bv = _bs_bv.setdefault('difficulty_state', {})
    _disc = _ds_bv.setdefault('bv_disclosed', {})
    _bst = bc.bc_batch_status(_cm_bv, _qs_bv)
    _foot = _bs_bv.setdefault('bc_footer', {})
    # release 2026.11.25 (GAP-2026-11-19-FIGURE-LOSS F5): a GRANTED figure slot that settled as the TEXT fallback hands
    # its grant to the first capable, not-yet-written slot of the same section (recorded; disclosed in the footer).
    # In the last batch nothing is left to take it: recorded as a shortfall (FE7) — never a stop.
    if isinstance(_bs_bv.get('figure_plan'), dict):
        _unauth = [str(_x) for _x in (_bs_bv.get('subtopic_by_qnum') or {}) if str(_x) not in _cm_bv]
        for _q in _bst['settled']:
            _fbk = _cm_bv[_q].get('bc_fallback') if isinstance(_cm_bv[_q].get('bc_fallback'), dict) else None
            if not _fbk or _fbk.get('regranted_to') is not None or 'regrant_checked' in _fbk \
                    or _cm_bv[_q].get('figure_files') or _cm_bv[_q].get('figure_dicts'):
                continue                                # delivered WITH a figure (R5b / R10): its grant is kept
            for _sec, _spf in list(_bs_bv['figure_plan'].items()):
                if isinstance(_spf, dict) and _q in [str(_x) for _x in (_spf.get('granted') or [])]:
                    if not _spf.get('capable_qs'):
                        _spf = dict(_spf, capable_qs=bv_figure_capable_qs(exam, n, home, _bs_bv, _sec))
                    _spn, _to = bc.figure_regrant(_spf, _q, _unauth)
                    _bs_bv['figure_plan'][_sec] = _spn
                    _cm_bv[_q]['bc_fallback'] = dict(_fbk, regranted_to=_to, regrant_checked=True)
                    _say(f"STEP A2: Q{_q} ended as text — its figure grant " + (f"moves to Q{_to} (F5)." if _to else
                         "could not move (no capable slot left in a later batch) — disclosed."))
                    _granted_bv.discard(_q)
                    if _to:
                        _granted_bv.add(_to)
                    break
    for _q in _bst['settled']:
        _foot[_q] = bc.bc_amber_lines(_q, _cm_bv[_q])
        if _r3_bv and isinstance(_bs_bv.get('math_typeset'), dict):
            # release 2026.11.27 (GAP-2026-11-21 C-S6 / C-S15): the delivered text still trips a soft Phase 1 gate after
            # the pre-review tries — delivered as it stands (figure kept), one AMBER line each
            _foot[_q] = list(_foot[_q] or []) + bc.p1_amber_lines(_q, _cm_bv[_q], _gctx(_q, _cm_bv[_q]))
        _rgt = (_cm_bv[_q].get('bc_fallback') or {}) if isinstance(_cm_bv[_q].get('bc_fallback'), dict) else {}
        if 'regrant_checked' in _rgt:
            # the S13-2L.0 footer reader unpacks every line as (class, text) — bc.bc_amber_lines' shape
            _foot[_q] = list(_foot[_q] or []) + [('INFORMATIONAL', f"Q{_q}: figure grant " + (
                f"moved to Q{_rgt['regranted_to']}" if _rgt.get('regranted_to') else 'could not move to a later slot')
                + ' after the text fallback')]
        _lb = ((_cm_bv[_q].get('difficulty_check') or {}).get('label_basis') or {}) if isinstance(_cm_bv[_q].get('difficulty_check'), dict) else {}
        if _lb.get('disclosed') and _tgt_bv.get(_q) is not None:
            _disc[_q] = {'requested': _tgt_bv.get(_q), 'delivered': _cm_bv[_q].get('difficulty')}
            if _lb.get('recipe_note'):
                _disc[_q]['recipe_note'] = _lb.get('recipe_note')
    _bs_bv['bv_carry'] = []                            # LAW-BC-1: nothing is carried (a 2026.11.14 carry was migrated)
    _st_bv['infra_carry'] = []
    _st_bv['unmeasured'] = []
    _rw = list(_acts_bv.get('rewrite') or [])
    if _new_jobs:
        _status = 'jobs_out'
    elif _rw or _perm or _rest or _sc_back or _pre_back:
        _status = 'rewrite'
    elif _acts_bv.get('stop'):
        _status = 'stop'
    elif _nm:
        _status = 'no_model'
    else:
        _status = 'done'
    if _status == 'done' and _bst['other']:
        # LAW-BC-1 — impossible by construction; never delivered in this state
        _status = 'no_model'
        _nm.update({q: 'not settled at DONE (engine defect, P0)' for q in _bst['other']})
        _bs_bv.setdefault('p0_incidents', []).append({'kind': 'bc_not_settled_at_done', 'qs': list(_bst['other'])})
    if final and _status == 'done':
        # LEGACY MIGRATION (S4-12): every question is settled by the settlement batch — an open S13-2L chain of the
        # earlier release is closed, never run
        for _qc, _ch in list((_bs_bv.get('slot_chain') or {}).items()):
            if isinstance(_ch, dict) and not _ch.get('done'):
                _ch.update({'done': True, 'outcome': 'migrated'})
        _bs_bv['slot_chain_work'] = []
    _st_bv['status'] = _status
    _st_bv['selfcount_missing'] = sorted(set(_sc_missing), key=int)
    # P4: the author/reviewer count offset per (subject, band), from every question measured so far (resume-safe)
    _bs_bv.setdefault('difficulty_state', {})['author_offset'] = bc.bc_author_offsets(
        _cm_bv, _st_bv.get('items') or {}, _tgt_bv, _labs_bv,
        seed=bc_registry_author_offsets(os.path.join(home, f'{exam}_registry.json'), _bs_bv.get('paper_id')))
    _st_bv['open'] = []
    _st_bv['pending'] = []
    _st_bv['key_chain'] = []
    _st_bv['permute'] = _perm
    _st_bv['restore'] = _rest
    _st_bv['no_model'] = _nm
    # release 2026.11.25 (F5 / F7): the figure manifest carries the CURRENT figure plan (re-grants included) from the
    # first batch on — S13-2F's pre-commit sweep (A-AXIS1: floor, moved grants) reads it through the registry preview,
    # which S13-2L.0 (that also writes it) only follows. Idempotent; written only when it differs.
    if any(isinstance(_v, dict) and _v.get('target') for _v in (_bs_bv.get('figure_plan') or {}).values()) \
            if isinstance(_bs_bv.get('figure_plan'), dict) else False:
        _fmp_bv = os.path.join(home, f'{exam}_fig_manifest.json')
        try:
            _fm_bv = json.load(open(_fmp_bv, encoding='utf-8')) if os.path.exists(_fmp_bv) else {'questions': {}}
        except (OSError, ValueError):
            _fm_bv = None                                # an unreadable manifest is never overwritten here
        if isinstance(_fm_bv, dict) and _fm_bv.get('plan') != _bs_bv['figure_plan']:
            _fm_bv['plan'] = _bs_bv['figure_plan']
            json.dump(_fm_bv, open(_fmp_bv, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    json.dump(_kd_bv, open(_kp_bv, 'w', encoding='utf-8'), indent=2)
    json.dump(_bs_bv, open(_bsp_bv, 'w', encoding='utf-8'), indent=2)
    _early_s = [q for q in _qs_bv if int(q) < int(_bp_bv['q_start'])] if not final else []
    _say(f"STEP A2 (job round {_st_bv['round']} of at most {bc.BV_MAX_ROUNDS}): "
         + '; '.join(f"{k} {v}" for k, v in sorted(_acts_bv.items()) if v)
         + (f"; earlier questions in this batch {_early_s}" if _early_s else '')
         + (f"; author_counts not recorded for {sorted(set(_sc_missing), key=int)} (G-SELFCOUNT, STEP B)"
            if _sc_missing else ''))
    if _status == 'jobs_out':
        _say("STEP A2: JOBS OUT " + ','.join(j['dir'] for j in _new_jobs))
    elif _status == 'rewrite':
        for _q, _pb in sorted(_pre_back.items(), key=lambda x: int(x[0])):
            _say(f"STEP A2: PRE-REVIEW Q{_q} (try {_pb['try_no']} of {bc.BC_PREREVIEW_TRIES}) — "
                 + '; '.join(_pb['gaps'])[:900] + " — fix it (re-render / record / correct), then STEP B for it "
                 "(it rewrites the findings file), then this block again (no reviewer was started)")
        for _q, _sc in sorted(_sc_back.items(), key=lambda x: int(x[0])):
            _say(f"STEP A2: SELF-COUNT Q{_q} (try {_sc['try_no']} of {bc.BC_SELFCOUNT_TRIES}) — {_sc['why']}: fix the "
                 f"question (or its author_counts, if they were miscounted), then STEP B for it, then this block again "
                 f"(no reviewer was started)")
        if _rw:
            _say(f"STEP A2: REWRITE {_rw} — each from concept_map[q]['bv']['climb_brief'] (rung 1 FIX / 2 REPLACE / "
                 f"3 FALLBACK), then STEP B for the new text, then this block again")
        for _q, _p in sorted(_perm.items(), key=lambda x: int(x[0])):
            _say(f"STEP A2: PERMUTE Q{_q} — exchange options {_p['swap'][0]} and {_p['swap'][1]} in the docx block and the "
                 f"sidecar (content unchanged, key = {_p['answer']}), then this block again (no new review)")
        for _q, _p in sorted(_rest.items(), key=lambda x: int(x[0])):
            _say(f"STEP A2: RESTORE Q{_q} — put back the version in {_p} (its sidecar entry and key; re-render its block), "
                 f"then this block again (no new review; R5b)")
    elif _status == 'stop':
        _say(f"STEP A2: STOP (BC_TERMINAL 'stop') — {_acts_bv.get('stop')}: no version meets R5b; state saved.")
    elif _status == 'no_model':
        _say(f"NO-MODEL [HS:ENV] — no fresh result for {sorted(_nm, key=int)} after {bc.BC_ROLE_ASKS} asks "
             f"({'; '.join(f'Q{q}: {w}' for q, w in sorted(_nm.items(), key=lambda x: int(x[0])))}). State saved; the next "
             f"message re-runs this block and asks again (LAW-BC-9 — never a carry).")
    else:
        _say(f"STEP A2: DONE — settled {len(_bst['settled'])}/{len(_qs_bv)} (disclosed {_bst['disclosed'] or 'none'}); "
             f"next: STEP A3 (bind the review records)")
    return {'status': _status, 'jobs': [j['dir'] for j in _new_jobs], 'rewrite': _rw, 'permute': _perm,
            'restore': _rest, 'settled': _bst['settled'], 'disclosed': _bst['disclosed'], 'no_model': _nm,
            'key_chain': [], 'open': [], 'pending': [], 'lines': _lines}


def _bc_norm_tokens(x):
    import unicodedata as _ud
    return _re.findall(r'[a-z0-9]+', _ud.normalize('NFKC', str(x or '')).lower())


def _bc_block_contains(block_text, entry):
    """True when the delivered block and the sidecar describe the same question (STEP A3 R2 guard). Tolerant of
    rendering (NFKC, case, punctuation, math / subscript runs): at least 80% of the stem's word tokens appear in the
    block; for a TEXT-option question every option's tokens appear in the block IN ORDER (a re-key swap done in one
    place only is caught). Drawn options (figure files / option structures) carry no text in the docx — only the stem
    is checked for them. An entry with no stem text cannot be checked: True. Never a false refusal on formatting."""
    e = entry if isinstance(entry, dict) else {}
    bt = _bc_norm_tokens(block_text)
    st = _bc_norm_tokens(e.get('stem_text'))
    if not st:
        return True
    bset = set(bt)
    if sum(1 for t in st if t in bset) < 0.8 * len(st):
        return False
    if e.get('figure_files') or e.get('figure_dicts') or e.get('option_smiles'):
        return True
    ops = e.get('option_texts') if isinstance(e.get('option_texts'), list) else []
    seq = ' ' + ' '.join(bt) + ' '
    pos = 0
    for o in ops:
        ot = _bc_norm_tokens(o)
        if not ot:
            continue
        needle = ' ' + ' '.join(ot) + ' '
        nxt = seq.find(needle, pos)
        if nxt < 0:
            return False
        pos = nxt + 1
    return True


def bv_review_qs_per_job(home='/home/claude'):
    """v1.24 (owner decision 2026-11-15) — questions per reviewer job: SESSION_BUDGET.json review_qs_per_job, or
    review_qs_per_job_fallback when this run's orchestrator recorded that lean sub-agents are NOT available
    (<home>/fw_lean_agents.json {'available': false} — bootstrap --lean-agents no): with ~65k of start-up per sub-agent,
    fewer, larger jobs halve the start-up tokens. Unknown -> review_qs_per_job. Never raises."""
    import json, os
    base = bv_budget_value('review_qs_per_job', bc.BV_REVIEW_QS_PER_JOB)
    try:
        rec = json.load(open(os.path.join(home, 'fw_lean_agents.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return base
    if isinstance(rec, dict) and rec.get('available') is False:
        return bv_budget_value('review_qs_per_job_fallback', base)
    return base


def bc_figure_with_layout(fd):
    """v1.24 (GAP-2026-11-15-RUN-ANALYSIS D1) — one organic figure dict with its 2-D layout proof: when the author did
    not record 'layout' (or 'projection_proof' for a chair / Newman / sawhorse / Fischer / Haworth), the engine computes
    corpus_io.organic_structure_layout(smiles, stereo_mode) itself, so corpus_io.organic_figure_proof applies EXACTLY
    the rule S13-2P applies (identity_ok, vision_ok, gates_ok). A projection kind without its projection_proof stays
    unproven (it must be recorded). Never raises; returns a new dict."""
    f = dict(fd) if isinstance(fd, dict) else {}
    if isinstance(f.get('layout'), dict) or isinstance(f.get('projection_proof'), dict):
        return f
    try:
        import corpus_io as _ci
        if str(f.get('kind') or '') in getattr(_ci, 'ORG_PROJECTION_KINDS', ()):
            return f
        if f.get('smiles'):
            _lay = _ci.organic_structure_layout(f.get('smiles'), f.get('stereo_mode') or 'abs')
            f['layout'] = {k: _lay.get(k) for k in ('identity_ok', 'gates_ok', 'findings', 'layout_attempt', 'smiles')}
    except Exception:                                   # noqa: BLE001 — unproven, reported by the caller
        pass
    return f


_BC_LIST_REF = None
_BC_SHOWN_REF = None
BC_PREREVIEW_AMBER_GATES = ('A-FIGLABELPX', 'A-FIGLABEL', 'A-FIGLABELRASTER', 'A-FIGCOLLIDE', 'A-FIGOVERPRINT',
                            'A-OPTDISTINCT')


def bc_prereview_gaps(entry, q, findings_doc=None):
    """v1.24 (GAP-2026-11-15-RUN-ANALYSIS D1-D3) — what must be fixed in question q BEFORE its reviewers are paid:
    (1) an organic structure figure whose proof fails identity / gates (computed by bc_figure_with_layout — the
        S13-2P rule); (2) a packet the reviewers could not solve: the stem refers to List-I / List-II / Column-I but
        list_columns is not recorded, or to a figure 'shown' with no figure_files, list_columns or stimulus_text;
    (3) the per-batch auditor's item findings for q (findings_doc = the --item-findings JSON STEP B wrote): every
        item finding, and the AMBER findings of BC_PREREVIEW_AMBER_GATES (small labels, collisions, stereo-ambiguous
        option pairs). [] when nothing is found. Never raises."""
    import re as _re
    global _BC_LIST_REF, _BC_SHOWN_REF
    if _BC_LIST_REF is None:
        _BC_LIST_REF = _re.compile(r'\b(list|column)[\s-]*(i{1,2}|1|2)\b', _re.I)
        # a picture noun with a showing verb ('the compound shown', 'the graph drawn below') or 'the figure / diagram
        # below / above', 'the following figure' — never 'statements given below' or 'it has been shown that'
        _BC_SHOWN_REF = _re.compile(
            r'\b(?:(?:figure|structure|reaction|scheme|graph|plot|diagram|compound|molecule|spectrum|spectra|circuit|'
            r'curve|image|picture|mechanism|apparatus|map|chart|pedigree|gel|blot|cladogram|tree)s?\s+'
            r'(?:shown|depicted|drawn|illustrated)'
            r'|(?:figure|diagram|graph|plot|scheme|chart)s?\s+(?:below|above)'
            r'|following\s+(?:figure|diagram|graph|plot|scheme|chart|structure)s?)\b', _re.I)
    e = entry if isinstance(entry, dict) else {}
    out = []
    if e.get('organic') is True:
        try:
            import corpus_io as _ci
            for i, fd in enumerate([f for f in (e.get('figure_dicts') or []) if isinstance(f, dict)], 1):
                pr = _ci.organic_figure_proof(dict(bc_figure_with_layout(fd), vision_reads=[{'match': True}] * 2))
                miss = [k for k in ('identity_ok', 'gates_ok') if not pr.get(k)]
                if miss:
                    why = ', '.join(f'{a}: {b}' for a, b in ((bc_figure_with_layout(fd).get('layout') or {}).get('findings')
                                                           or [])[:3]) or 'no layout / projection proof'
                    out.append(f"figure {i} ({fd.get('file')}) not proven ({'/'.join(miss)}: {why}) — correct the SMILES "
                               f"or stereo_mode, or redraw")
        except Exception:                               # noqa: BLE001 — engine unavailable: the batch proof decides
            pass
    stem = ' '.join(str(e.get(k) or '') for k in ('stem_text', 'stem'))
    if _BC_LIST_REF.search(stem) and not e.get('list_columns'):
        out.append("the stem refers to List-I / List-II but list_columns is not recorded — the reviewers would see no "
                   "lists: record list_columns in the sidecar entry")
    if _BC_SHOWN_REF.search(stem) and not any(e.get(k) for k in ('figure_files', 'figure_dicts', 'list_columns',
                                                                 'stimulus_text', 'content_record', 'given_smiles')):
        out.append("the stem refers to something shown but the entry carries no figure_files — the reviewers would see "
                   "no picture: record figure_files")
    doc = findings_doc if isinstance(findings_doc, dict) else {}
    for r in (doc.get('item_findings') or []):
        if isinstance(r, dict) and str(r.get('q')) == str(q):
            out.append(f"{r.get('gate')}: {str(r.get('finding'))[:200]}")
    for r in (doc.get('amber_findings') or []):
        if isinstance(r, dict) and str(r.get('q')) == str(q) and r.get('gate') in BC_PREREVIEW_AMBER_GATES:
            out.append(f"{r.get('gate')} (AMBER): {str(r.get('finding'))[:200]}")
    return out


def bc_stimulus_fill(entry, q, bs):
    """v1.24 (GAP-2026-11-15-RUN-ANALYSIS D2) — a member of a stimulus set (passage / data / cloze — Create S7 R-LINKED,
    batch_state['stimulus_groups'][gid] = {'qnums', 'stimulus'}) is printed under its set's stimulus, which its own
    stem_text does not repeat: the reviewers and the adjudicator must read it too. Returns a copy of entry with
    'stimulus_text' = the registered stimulus when the entry has none; an existing value is never replaced. The text
    binding (op_content_sha / item_hash) does not include it, so no review record changes. Never raises."""
    e = entry if isinstance(entry, dict) else {}
    if e.get('stimulus_text'):
        return e
    try:
        qi = int(q)
        for g in ((bs or {}).get('stimulus_groups') or {}).values():
            if isinstance(g, dict) and g.get('stimulus') and qi in {int(x) for x in (g.get('qnums') or [])}:
                return dict(e, stimulus_text=str(g['stimulus']))
    except (TypeError, ValueError, AttributeError):
        pass
    return e


def bc_text_has_results(entry):
    """v1.24 — True when the entry's CURRENT text already carries reviewer results (bv 'grades' / 'solvers' / 'meta'
    recorded for this content_sha — e.g. a question migrated from an earlier release with its grades kept). Pre-review
    is for a text no reviewer has seen; such a text is never sent back by it. Never raises."""
    e = entry if isinstance(entry, dict) else {}
    bvs = e.get('bv') if isinstance(e.get('bv'), dict) else {}
    if not any(bvs.get(k) for k in ('grades', 'solvers', 'meta')):
        return False
    try:
        return not bvs.get('content_sha') or bvs.get('content_sha') == bc.op_content_sha(e)
    except Exception:                                   # noqa: BLE001
        return True


def bc_registry_author_offsets(registry_path, paper_id=None):
    """v1.24 (D6) — the author/reviewer count offsets earlier papers of this exam recorded (registry question_index[].
    difficulty_state.author_offset), newest paper first, this paper excluded: [{key: {'n', 'steps', 'concepts'}}].
    [] when there is none. Never raises."""
    import json, os
    try:
        reg = json.load(open(registry_path, encoding='utf-8')) if os.path.exists(registry_path) else {}
    except (OSError, ValueError):
        return []
    out = []
    for qe in reversed(list((reg or {}).get('question_index') or [])):
        if not isinstance(qe, dict) or (paper_id and qe.get('paper_id') == paper_id):
            continue
        ao = ((qe.get('difficulty_state') or {}).get('author_offset')) if isinstance(qe.get('difficulty_state'), dict) else None
        if isinstance(ao, dict) and ao:
            # only what that paper MEASURED itself — an offset it carried from an even earlier paper ('from') is skipped,
            # so a newer measurement is never shadowed by an old one handed down
            _own = {k: v for k, v in ao.items() if isinstance(v, dict) and not str(k).startswith('_') and not v.get('from')}
            if _own:
                out.append(_own)
    return out


def bc_fallback_clear_figure(exam, n, q, home='/home/claude', bs=None):
    """v1.23 (GAP-2026-11-14-SPEED-AND-FIDELITY C3) — the rung-3 FALLBACK of S0-BC LAW-BC-2 is a TEXT question: remove
    question q from the paper's figure record (<home>/<exam>_fig_manifest.json questions[q]) so the per-batch auditor
    does not count the slot as a figure question with no picture (A-FIGCOMP 'figural:0img'). The slot's planned format
    is kept by concept_map[q].bc_fallback.from_figure (A-AXIS1 counts it as the disclosed fallback). Idempotent; records
    the removal in batch_state['bv']['fallback_cleared']. Returns True when a record was removed. Never raises."""
    import json, os
    q = str(q)
    removed = False
    fmp = os.path.join(home, f'{exam}_fig_manifest.json')
    try:
        fm = json.load(open(fmp, encoding='utf-8')) if os.path.exists(fmp) else None
    except (OSError, ValueError):
        fm = None
    rec = None
    if isinstance(fm, dict) and isinstance(fm.get('questions'), dict) and q in fm['questions']:
        rec = fm['questions'].pop(q, None)
        try:
            json.dump(fm, open(fmp, 'w', encoding='utf-8'), indent=2)
            removed = True
        except OSError:
            return False

    def _keep(_bs):
        _bv = _bs.setdefault('bv', {})
        fc = _bv.setdefault('fallback_cleared', [])
        if q not in fc:
            fc.append(q)
        if rec is not None:                      # kept so an R5b restore of the earlier figure version puts it back
            _bv.setdefault('fallback_fig_records', {})[q] = rec
    if isinstance(bs, dict):                  # the caller holds batch_state in memory and writes it itself
        _keep(bs)
        return removed
    bsp = os.path.join(home, f'{exam}_M{n}_batch_state.json')
    try:
        bs = json.load(open(bsp, encoding='utf-8'))
        _keep(bs)
        json.dump(bs, open(bsp, 'w', encoding='utf-8'), indent=2)
    except (OSError, ValueError, AttributeError):
        pass
    return removed


def bc_fallback_restore_figure(exam, n, q, home='/home/claude', bs=None):
    """v1.23 (C3) — an R5b RESTORE put back an earlier FIGURE version of a question whose figure record the rung-3
    fallback removed: re-insert the kept record (batch_state['bv']['fallback_fig_records'][q]) into
    <home>/<exam>_fig_manifest.json. Idempotent; True when a record was put back. Never raises."""
    import json, os
    q = str(q)
    own = not isinstance(bs, dict)
    bsp = os.path.join(home, f'{exam}_M{n}_batch_state.json')
    try:
        if own:
            bs = json.load(open(bsp, encoding='utf-8'))
        rec = ((bs.get('bv') or {}).get('fallback_fig_records') or {}).get(q)
    except (OSError, ValueError, AttributeError):
        return False
    if not isinstance(rec, dict):
        return False
    fmp = os.path.join(home, f'{exam}_fig_manifest.json')
    try:
        fm = json.load(open(fmp, encoding='utf-8')) if os.path.exists(fmp) else {'questions': {}}
        if not isinstance(fm, dict) or not isinstance(fm.get('questions'), dict):
            return False
        if q in fm['questions']:
            return False
        fm['questions'][q] = rec
        json.dump(fm, open(fmp, 'w', encoding='utf-8'), indent=2)
    except (OSError, ValueError):
        return False
    return True


def _qf_rung(bvs):
    try:
        return int((bvs or {}).get('rung') or 0)
    except (TypeError, ValueError):
        return 0


def bc_bind_batch(exam, n, item_hashes_path, item_texts_path=None, home='/home/claude', echo=True, upto=None):
    """v1.22 STEP A3 (LAW-BC-7) — bind every settled / disclosed question up to this batch to the auditor's item_hash
    of its block in the cumulative docx: concept_map[q]['review'] = bc.bc_review_record (reviewer 'batch') and one
    review_history entry; key_votes are already bound to the question's content by bc_apply. REFUSES (names the
    question, binds nothing for it) when: the question is not settled / disclosed; its current text is not the text
    its reviewers judged (it was edited after review without re-review — R2); its block is missing from the item
    hashes; or (with item_texts_path) the block does not show the sidecar's stem and options in order. M-BIND: a question
    settled under BV1 (an earlier release) gets a two-solver 'unanimous' record with key_votes.rule 'BV1'. Returns
    {'status': 'bound' | 'refused', 'bound': [q], 'refused': {q: why}, 'lines'}. Never raises on a refusal."""
    import json, os
    _lines = []

    def _say(x):
        _lines.append(str(x))
        if echo:
            print(x)
    bsp = os.path.join(home, f'{exam}_M{n}_batch_state.json')
    kp = os.path.join(home, f'{exam}_M{n}_answer_key.json')
    bs = json.load(open(bsp, encoding='utf-8'))
    kd = json.load(open(kp, encoding='utf-8'))
    cm = kd.setdefault('concept_map', {})
    labs = list(bs.get('difficulty_labels') or ['Easy', 'Medium', 'Hard'])
    try:
        hashes = {str(k): v for k, v in json.load(open(item_hashes_path, encoding='utf-8')).items()}
    except (OSError, ValueError, TypeError, AttributeError):
        hashes = {}
    texts = {}
    if item_texts_path:
        try:
            texts = {str(k): v for k, v in json.load(open(item_texts_path, encoding='utf-8')).items()}
        except (OSError, ValueError, TypeError, AttributeError):
            texts = {}
    items = (bs.get('bv') or {}).get('items') or {}
    plan = bs.get('batch_plan') or []
    if upto is None:
        try:
            upto = int(plan[min(len(plan), int(bs.get('current_batch', 1))) - 1]['q_end'])
        except (IndexError, KeyError, ValueError, TypeError):
            upto = max([int(q) for q in cm if str(q).isdigit()] or [0])
    bound, refused = [], {}
    rnd = (bs.get('bv') or {}).get('round')
    for q in sorted((q for q in cm if str(q).isdigit() and int(q) <= int(upto)), key=int):
        e = cm[q] if isinstance(cm[q], dict) else {}
        bvs = items.get(q) if isinstance(items.get(q), dict) else e.get('bv')
        h = hashes.get(q)
        if not h:
            refused[q] = 'no item_hash for its block (the auditor did not find it in the docx)'
            continue
        if texts and q in texts and not _bc_block_contains(texts[q], e):
            refused[q] = 'the docx block does not show the sidecar stem / options in order (edited in one place only)'
            continue
        if isinstance(bvs, dict) and bvs.get('rule') == bc.BC_RULE:
            if bvs.get('state') not in bc.BC_STATES or e.get('bv_state') not in bc.BC_STATES:
                refused[q] = f"not settled (state {bvs.get('state')}) — STEP A2 is not DONE for it"
                continue
            if bvs.get('content_sha') != _bc_entry_sha(_bc_render_shas(e)):
                refused[q] = 'its text changed after its review (R2) — run STEP A2 again so the new text is reviewed'
                continue
            if bc.bc_is_text_fallback(bvs) and not bc_figure_intrinsic(bs, q)[1]:
                # C3: the rung-3 FALLBACK is a TEXT question (LAW-BC-2) — a picture on it is a defect; a figure record
                # left behind by the replaced question is removed here (no text change, no new review).
                # GAP-2026-11-20 F1: only the TEXT fallback (bc.bc_is_text_fallback) — a text / figure rebuild or an R5b
                # version keeps its figure and binds. F9: STEP A2 owns the repair of a fallback that still carries a
                # figure (bounded; it treats the question as open), so this refusal only names the step to run.
                if bc.bc_fallback_figure_open(dict(e, bv=bvs), bc_figure_intrinsic(bs, q)[1]):
                    refused[q] = ('it is the rung-3 TEXT fallback but carries a figure — run STEP A2 again: it orders the '
                                  'repair (REWRITE without the figure, at most '
                                  f'{bc.BC_FALLBACK_FIGURE_ORDERS} times, then R5b or kept + disclosed — F9), then '
                                  'STEP B, STEP A2 and STEP A3')
                    continue
                if bc_fallback_clear_figure(exam, n, q, home):
                    _say(f"STEP A3: Q{q} is the rung-3 TEXT fallback — its leftover figure record was removed "
                         f"(fig_manifest; A-AXIS1 counts the slot as the disclosed fallback).")
            _old = e.get('review') if isinstance(e.get('review'), dict) else {}
            if _old.get('rule') == bc.BC_RULE and _old.get('item_hash') and _old.get('item_hash') != h \
                    and _old.get('content_sha') == bvs.get('content_sha'):
                # measured on the incident paper: a block's hash does not change when later batches are appended, so a
                # new hash on an unchanged text means the docx block alone was edited (e.g. a picture swapped) — R2
                refused[q] = 'its docx block changed after it was bound while its text did not (edited outside the ladder)'
                continue
            rec = bc.bc_review_record(dict(e, bv=bvs), h, rnd)
            if rec is None:
                refused[q] = 'no review record could be built'
                continue
        else:
            # M-BIND (GAP §9.1): settled under BV1 — two solvers, unanimous, label verified
            kv = e.get('key_votes') if isinstance(e.get('key_votes'), dict) else {}
            rv0 = e.get('review') if isinstance(e.get('review'), dict) else {}
            if rv0.get('item_hash') == h:
                bound.append(q)                         # an S13-2G record bound to this text stays as it is
                continue
            if kv.get('unanimous') is not True or (kv.get('content_sha') and kv.get('content_sha') != bc.op_content_sha(e)) \
                    or (e.get('difficulty_check') and not bc.verify_difficulty_label(e, labs, strict=True)[0]):
                refused[q] = 'settled under an earlier release without a unanimous key / verified label — STEP A2 migrates it'
                continue
            e['key_votes'] = dict(kv, rule='BV1')
            rec = {'item_hash': h, 'reviewer': 'batch', 'rule': 'BV1', 'certified_by': 'unanimous', 'key_agrees': True,
                   'own_key': kd.get('answers', {}).get(q), 'confidence': 'medium', 'single_answer': 'yes',
                   'leak_or_paraphrase': 'none', 'distractor_existence_and_class': '', 'consistency_and_names': 'ok',
                   'selectivity_basis': 'clean', 'verdict': 'PASS', 'round': None, 'rung': None, 'migrated': True}
        e['review'] = rec
        e.setdefault('review_history', []).append(dict(rec))
        cm[q] = e
        bound.append(q)
    json.dump(kd, open(kp, 'w', encoding='utf-8'), indent=2)
    if refused:
        _say(f"STEP A3: REFUSED — {len(refused)} question(s) not bound: "
             + '; '.join(f'Q{q}: {w}' for q, w in sorted(refused.items(), key=lambda x: int(x[0])))
             + ' — fix as named, then STEP A3 again (STEP E is forbidden until this prints BOUND).')
    else:
        _say(f"STEP A3: BOUND — {len(bound)} question(s) carry a batch review record bound to their delivered block.")
    return {'status': 'refused' if refused else 'bound', 'bound': bound, 'refused': refused, 'lines': _lines}


def assemble_final_docx(src_docx, dst_docx):
    """v1.22 Create S13-1 ASSEMBLE (GAP §6.6 step 1, E-03): copy the last cumulative docx BYTE FOR BYTE to the final
    name — no re-render, no renumbering, no reformatting — and prove it (sha256 of both). Returns {'ok', 'sha256',
    'why'}. Never raises."""
    import os, shutil
    try:
        if os.path.abspath(src_docx) != os.path.abspath(dst_docx):
            shutil.copyfile(src_docx, dst_docx)
        a = hashlib.sha256(open(src_docx, 'rb').read()).hexdigest()
        b = hashlib.sha256(open(dst_docx, 'rb').read()).hexdigest()
        return {'ok': a == b, 'sha256': b, 'why': 'byte copy' if a == b else 'copy differs from the cumulative docx'}
    except OSError as ex:
        return {'ok': False, 'sha256': None, 'why': f'{type(ex).__name__}: {ex}'}


def bc_check_bound(exam, n, item_hashes_path, home='/home/claude'):
    """v1.22 Create S13-1 — every question's batch-bound review.item_hash equals the hash the auditor computes from the
    FINAL docx. Returns {'ok', 'mismatch': [q], 'missing': [q]}. A mismatch is an INFRA fault (re-copy; still different
    -> P0) — never a re-review. Never raises."""
    import json, os
    try:
        kd = json.load(open(os.path.join(home, f'{exam}_M{n}_answer_key.json'), encoding='utf-8'))
        hs = {str(k): v for k, v in json.load(open(item_hashes_path, encoding='utf-8')).items()}
    except (OSError, ValueError, TypeError, AttributeError):
        return {'ok': False, 'mismatch': [], 'missing': ['(unreadable)']}
    cm = kd.get('concept_map') or {}
    ans = kd.get('answers') or {}
    mis, miss, keyx = [], [], []
    for q in sorted((q for q in cm if str(q).isdigit()), key=int):
        rv = (cm[q] or {}).get('review') if isinstance(cm[q], dict) else None
        if not isinstance(rv, dict) or not rv.get('item_hash'):
            miss.append(q)
        elif hs.get(q) != rv.get('item_hash'):
            mis.append(q)
        kv = (cm[q] or {}).get('key_votes') if isinstance(cm[q], dict) else None
        _qt = str((cm[q] or {}).get('qtype') or 'mcq') if isinstance(cm[q], dict) else 'mcq'
        if isinstance(kv, dict) and kv.get('rule') == bc.BC_RULE and kv.get('decided_key') is not None \
                and not bc.bc_same_answer(kv.get('decided_key'), ans.get(q), _qt, 1e-9):
            keyx.append(q)                              # the committed key must be the decided key (GAP §7.4)
    return {'ok': not mis and not miss and not keyx, 'mismatch': mis, 'missing': miss, 'key_mismatch': keyx}



# ══════════════════════════════════════════════════════════════════════════
# Self-test
# ══════════════════════════════════════════════════════════════════════════
def self_test():
    passed = 0
    total = 0
    fails = []

    def check(name, cond):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
        else:
            fails.append(name)

    def check_raises_never(name, fn):
        """Mirrors paper_pipeline.py's ck_call — a fixture that raises counts
        as a failure instead of aborting the whole self-test."""
        nonlocal passed, total
        total += 1
        try:
            if fn():
                passed += 1
            else:
                fails.append(name)
        except Exception as exc:
            fails.append(f"{name} [raised {type(exc).__name__}: {exc}]")

    def mini_bp(**over):
        bp = {
            'blueprint_version': 'test-1.0',
            'total_questions': 3,
            'batch_size_qs': 10,
            'subtopic_list': [
                {'subtopic_id': 'ex.a', 'section': 'Section A', 'subtopic': 'Alpha'},
                {'subtopic_id': 'ex.b', 'section': 'Section A', 'subtopic': 'Beta'},
            ],
            'difficulty_labels': ['Easy', 'Medium', 'Hard'],
            'difficulty_schedule': [{'mock': 1, 'simple': 1, 'medium': 1, 'hard': 1}],
            'sections': [{'section_name': 'Section A'}],
            'mocks': [{'mock': 1, 'paper_id': 'MOCK:M01'}],
        }
        bp.update(over)
        return bp

    def mini_registry(**over):
        reg = {
            'exam_code': 'EX', 'schema_version': '1.0',
            'mocks_completed': [], 'papers_completed': [],
            'question_hashes': [], 'stem_texts': [], 'semantic_tuples': [],
            'semantic_usage': [], 'exhausted_subtopics': {}, 'question_index': [],
            'image_phashes': [], 'image_sources_used': [], 'session_log': [],
            'content_tracking': {k: [] for k in _REQUIRED_CT},
            'section_names': [], 'rc_manifests': [], 'figural_manifests': [],
            'di_manifests': [],
        }
        reg.update(over)
        return reg

    def mini_registry_no_ct(**over):
        """Same as mini_registry() but WITHOUT a pre-seeded content_tracking
        key — models a registry that has never had Step-1's template init
        run (or a template that omitted it entirely), so S13-4's first-mock
        `if 'content_tracking' not in reg` branch actually fires. A registry
        that already carries a (possibly schema-less) content_tracking dict,
        as mini_registry() does, correctly does NOT get re-seeded — that's
        the drifted-but-present case regcheck's self-heal handles instead."""
        reg = mini_registry(**over)
        del reg['content_tracking']
        return reg

    def mini_pending():
        return {'question_hashes': ['h1'], 'stem_texts': ['s1'], 'semantic_tuples': ['t1']}

    def mini_cm():
        return {
            '1': {'subtopic_id': 'ex.a', 'difficulty': 'Easy'},
            '2': {'subtopic_id': 'ex.b', 'difficulty': 'Medium'},
            '3': {'subtopic_id': 'ex.a', 'difficulty': 'Hard'},
        }

    # ── commit_registry ──────────────────────────────────────────────────
    bp1 = mini_bp()
    r1 = commit_registry(mini_registry(), mini_pending(), bp1, 1,
                         paper_id='MOCK:M01', batches_completed=3,
                         axis2_window_counts={}, passage_present=False,
                         di_present=False, figural_present=False,
                         concept_map=mini_cm(), timestamp='2026-01-01T00:00:00+00:00')
    check('commit_first_mock_ok', r1['ok'] is True)
    # release 2026.11.25 (P1): the decision mode reaches the registry row (A-QINDEX check 9 reads it); legacy rows unchanged
    _cm25 = mini_cm(); _cm25['1']['difficulty_mode'] = 'ladder'
    _cm25['2']['s13_2f_cap'] = {'sweep': 12, 'gates': ['A-X']}
    _r25 = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01', batches_completed=3,
                           axis2_window_counts={}, passage_present=False, di_present=False, figural_present=False,
                           concept_map=_cm25, timestamp='2026-01-01T00:00:00+00:00')
    _qi25 = {str(x['q']): x for x in _r25['registry']['question_index'][0]['questions']}
    check('s13loop_P1_difficulty_mode_committed', _r25['ok'] and _qi25['1'].get('difficulty_mode') == 'ladder'
          and 'difficulty_mode' not in _qi25['2'] and _qi25['2'].get('s13_2f_cap') == {'sweep': 12, 'gates': ['A-X']}
          and 's13_2f_cap' not in _qi25['1'])
    # release 2026.11.25: a project holding a MOCK blueprint and a SCOPED blueprint, both with a paper 1 — the paper's
    # own blueprint is the one whose paper-1 allocation holds its slot map (never the first file found)
    import tempfile as _tf25, json as _js25, os as _os25
    with _tf25.TemporaryDirectory() as _h25:
        def _bpx(sids, fig):
            return {'mocks': [{'mock': 1, 'sections': [{'section_name': 'S', 'subtopic_allocations': [
                {'subtopic_id': x, 'format': 'FIGURAL' if x in fig else 'TEXT'} for x in sids]}]}]}
        _js25.dump(_bpx(['a', 'b'], ['a']), open(_os25.path.join(_h25, 'ZZEX_blueprint.json'), 'w'))
        _js25.dump(_bpx(['c', 'd'], ['d']), open(_os25.path.join(_h25, 'ZZEX_SUBJ_X_blueprint.json'), 'w'))
        _bs25 = {'subtopic_by_qnum': {'1': 'c', '2': 'd', '3': 'd'}}
        _pb25 = bv_paper_blueprint('ZZEX', 1, _h25, _bs25)
        check('s13loop_paper_blueprint_is_the_papers_own',
              [a['subtopic_id'] for a in _pb25['mocks'][0]['sections'][0]['subtopic_allocations']] == ['c', 'd']
              and bv_figure_capable_qs('ZZEX', 1, _h25, _bs25, 'S') == ['2', '3']
              and bv_paper_blueprint('ZZEX', 1, _h25, {'subtopic_by_qnum': {'1': 'q'}}) == {}
              and bv_paper_blueprint('ZZEX', 1, _h25, None) == {})
    # release 2026.11.25 (F5 / F7): one batch step writes the CURRENT figure plan into the figure manifest
    with _tf25.TemporaryDirectory() as _h27:
        _js25.dump({'concept_map': {'1': {'stem_text': 'Identify the product', 'option_texts': ['A', 'B', 'C', 'D'],
                                          'subtopic_id': 'A.b', 'qtype': 'mcq'}}, 'answers': {'1': 1}},
                   open(_os25.path.join(_h27, 'EX_M1_answer_key.json'), 'w'))
        _fp27 = {'S': {'target': 1, 'granted': ['1'], 'capable': 1, 'capable_qs': ['1'], 'short': []}}
        _js25.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1,
                    'difficulty_labels': ['Easy', 'Medium', 'Hard'], 'difficulty_plan_target': {'1': 'Medium'},
                    'difficulty_mode': bc.R3_MODE_LEGACY, 'figure_plan': _fp27},
                   open(_os25.path.join(_h27, 'EX_M1_batch_state.json'), 'w'))
        bv_batch_step('EX', 1, home=_h27, echo=False)
        _fm27 = _js25.load(open(_os25.path.join(_h27, 'EX_fig_manifest.json')))
        check('figloss_figure_plan_reaches_manifest_every_batch', _fm27.get('plan') == _fp27)
    # release 2026.11.25 (F5): a granted slot settled as the TEXT fallback hands its grant to the unwritten capable slot;
    # the footer line has the (class, text) shape the S13-2L.0 reader unpacks
    with _tf25.TemporaryDirectory() as _h28:
        _e28 = {'stem_text': 'Identify X', 'option_texts': ['A', 'B', 'C', 'D'], 'subtopic_id': 'A.b', 'qtype': 'mcq',
                'bv_state': 'settled', 'bc_fallback': {'rung': 3, 'from_figure': True},
                'bv': {'state': 'settled', 'rung': 3, 'rung3_kind': 'fallback'}}
        _js25.dump({'concept_map': {'1': _e28}, 'answers': {'1': 1}}, open(_os25.path.join(_h28, 'EX_M1_answer_key.json'), 'w'))
        _js25.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}, {'batch_id': 2, 'q_start': 2, 'q_end': 2}],
                    'current_batch': 1, 'difficulty_labels': ['Easy', 'Medium', 'Hard'], 'difficulty_mode': 'br1',
                    'subtopic_by_qnum': {'1': 'A.b', '2': 'A.c'},
                    'figure_plan': {'S': {'target': 1, 'granted': ['1'], 'capable': 2, 'capable_qs': ['1', '2'], 'short': []}},
                    'bv': {'batch': 1, 'round': 1, 'items': {'1': _e28['bv']}, 'status': 'open'}},
                   open(_os25.path.join(_h28, 'EX_M1_batch_state.json'), 'w'))
        bv_batch_step('EX', 1, home=_h28, echo=False)
        _b28 = _js25.load(open(_os25.path.join(_h28, 'EX_M1_batch_state.json')))
        _k28 = _js25.load(open(_os25.path.join(_h28, 'EX_M1_answer_key.json')))
        _ok28 = True
        try:
            for _qf28, _ln28 in (_b28.get('bc_footer') or {}).items():
                for _c28, _t28 in (_ln28 or []):
                    pass
        except ValueError:
            _ok28 = False
        check('figloss_F5_regrant_in_batch_step_and_footer_shape',
              _b28['figure_plan']['S']['granted'] == ['2'] and _b28['figure_plan']['S']['regrants'] == [{'from': '1', 'to': '2'}]
              and _k28['concept_map']['1']['bc_fallback'].get('regranted_to') == '2' and _ok28
              and any('moved to Q2' in t for _c, t in _b28['bc_footer']['1']))
    # release 2026.11.25: the I/O shell end to end — disclosure written once to the sidecar, an EARLIER-batch item
    # re-opened through bc_reopen, a CURRENT-batch item left to its own flow, a second call idempotent
    with _tf25.TemporaryDirectory() as _h26:
        _js25.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 10}, {'batch_id': 2, 'q_start': 11, 'q_end': 20}],
                    'current_batch': 2, 'shape_plan': {'3': 'direct'}}, open(_os25.path.join(_h26, 'EX_M1_batch_state.json'), 'w'))
        _js25.dump({'concept_map': {'3': {'shape': 'direct'}, '15': {}}, 'answers': {}},
                   open(_os25.path.join(_h26, 'EX_M1_answer_key.json'), 'w'))
        _wl26 = {'item_findings': [{'q': '3', 'gate': 'A-SHAPEMIX'}, {'q': '4', 'gate': 'A-STEMLEAK', 'finding': 'x'},
                                   {'q': '15', 'gate': 'A-STEMLEAK', 'finding': 'y'}],
                 'fail_lines': [{'check': 'A-AXIS2', 'message': 'short', 'qs': []}]}
        _a26 = bc_last_batch_apply('EX', 1, _wl26, home=_h26)
        _a26b = bc_last_batch_apply('EX', 1, _wl26, home=_h26)
        _k26 = _js25.load(open(_os25.path.join(_h26, 'EX_M1_answer_key.json')))
        _b26 = _js25.load(open(_os25.path.join(_h26, 'EX_M1_batch_state.json')))
        check('s13loop_last_batch_apply_io',
              sorted(_k26['nf_disclosed']) == ['A-AXIS2', 'A-SHAPEMIX'] and list(_a26['reopen']) == ['4']
              and _a26['current'] == ['15'] and sorted(_b26['bv']['reopen']) == ['4']
              and len(_b26['bv']['reopen']['4']) == 1 and _a26b['reopen'] == _a26['reopen'])
    # release 2026.11.25 (P13 / G9 / G21, T-U12): THE last-batch decision — composition disclosed, drift re-opened,
    # another item gate re-opened, a settled item accepted
    _lbr = bc_last_batch_route(
        [{'q': '23', 'gate': 'A-SHAPEMIX'}, {'q': '9', 'gate': 'A-SHAPEMIX'}, {'q': '5', 'gate': 'A-STEMLEAK', 'finding': 'leak'},
         {'q': '7', 'gate': 'A-REVIEW'}, {'q': '11', 'gate': 'A-INTRADUP'}, {'check': 'A-ANSKEY', 'qs': ['12'], 'message': 'x'}],
        {'23': 'statement', '9': 'matching', '5': 'direct', '12': 'direct'},
        {'23': {'shape': 'statement'}, '9': {'shape': 'spectrum_to_structure'}, '5': {'shape': 'direct'},
         '7': {'quality_status': 'ESCALATED(A-REVIEW)'}, '11': {}, '12': {}})
    check('s13loop_TU12_last_batch_route_is_engine_owned',
          _lbr['disclose'] == {'A-SHAPEMIX': ['23'], 'A-INTRADUP': ['11']}
          and sorted(_lbr['reopen']) == ['12', '5', '9'] and _lbr['reopen']['9'][0].startswith('G-SHAPEPLAN')
          and _lbr['accepted'] == ['7']
          and bc_last_batch_route([{'q': '5', 'gate': 'A-STEMLEAK'}, {'check': 'A-CLASSMIX', 'qs': [], 'message': 'm'}],
                                  {}, {}, current_batch_qs=['5'])
          == {'disclose': {'A-CLASSMIX': []}, 'reopen': {}, 'accepted': [], 'current': ['5']}
          and bc_last_batch_route([{'q': '9', 'gate': 'A-SHAPEMIX'}], {'9': 'match'},
                                  {'9': {'shape': 'direct', 'shape_drift': {'planned': 'match', 'delivered': 'direct',
                                                                            'reason': 'fallback'}}})['disclose'] == {'A-SHAPEMIX': ['9']}
          and bc_last_batch_route(None, None, None) == {'disclose': {}, 'reopen': {}, 'accepted': [], 'current': []})
    # content_tracking is pre-seeded (no _schema) by mini_registry(), which
    # models a Step-1 template that already ran — so the S13-4 "not in reg"
    # seeding branch correctly does NOT fire here (see mini_registry_no_ct).
    check('commit_first_mock_content_tracking_not_reseeded_when_already_present',
         '_schema' not in r1['registry']['content_tracking'])
    r1_noct = commit_registry(mini_registry_no_ct(), mini_pending(), bp1, 1,
                              paper_id='MOCK:M01', batches_completed=3,
                              axis2_window_counts={}, passage_present=False,
                              di_present=False, figural_present=False,
                              concept_map=mini_cm(), timestamp='2026-01-01T00:00:00+00:00')
    check('commit_first_mock_content_tracking_seeded_when_absent',
         '_schema' in r1_noct['registry']['content_tracking'])
    check('commit_first_mock_qindex_written',
         r1['registry']['question_index'][0]['questions'][0]['subtopic_id'] == 'ex.a')
    check('commit_first_mock_mocks_completed', r1['registry']['mocks_completed'] == [1])
    check('commit_first_mock_session_log_stamped',
         r1['registry']['session_log'][0]['timestamp'] == '2026-01-01T00:00:00+00:00')
    check('commit_does_not_mutate_input_registry',
         mini_registry() == mini_registry())  # sanity: literal fixture unaffected by prior call
    _orig = mini_registry()
    commit_registry(_orig, mini_pending(), bp1, 1, paper_id='MOCK:M01',
                    batches_completed=1, axis2_window_counts={}, passage_present=False,
                    di_present=False, figural_present=False, concept_map=mini_cm())
    check('commit_pure_original_untouched', _orig == mini_registry())

    # v1.7 (GAP-2026-09-21-LINKED-PLACEMENT): set membership passthrough
    check('commit_qindex_legacy_has_no_stimulus_key',
          all('stimulus_group_id' not in q
              for q in r1['registry']['question_index'][0]['questions']))
    _sg_cm = mini_cm()
    _sg_cm['1']['stimulus_group_id'] = 'ex.rc#1'
    _sg_cm['2']['stimulus_group_id'] = 'ex.rc#1'
    _sg_cm['3']['stimulus_group_id'] = None
    _r_sg = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                            batches_completed=1, axis2_window_counts={},
                            passage_present=False, di_present=False,
                            figural_present=False, concept_map=_sg_cm)
    check('commit_qindex_carries_stimulus_group_id',
          [q.get('stimulus_group_id', 'ABSENT') for q in
           _r_sg['registry']['question_index'][0]['questions']]
          == ['ex.rc#1', 'ex.rc#1', None])

    # v1.11 (GAP-2026-11-02): v5.89 per-question records carried only when present
    _v9_cm = mini_cm()
    _v9_cm['1'].update({'difficulty_check': {'decision': 'agree', 'final_band': 'Hard'},
                        'figural_ask_type': 'product_prediction', 'marked_sites': [],
                        'ladder': {'rung': 'R1', 'reasons': ['G-FIGMARK'], 'attempts': 1}})
    _r_v9 = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                            batches_completed=1, axis2_window_counts={},
                            passage_present=False, di_present=False,
                            figural_present=False, concept_map=_v9_cm)
    _q_v9 = _r_v9['registry']['question_index'][0]['questions']
    check('commit_qindex_carries_v589_fields_only_when_present',
          _q_v9[0]['figural_ask_type'] == 'product_prediction'
          and _q_v9[0]['ladder']['rung'] == 'R1' and _q_v9[0]['marked_sites'] == []
          and _q_v9[0]['difficulty_check']['final_band'] == 'Hard'
          and not any(k in _q_v9[1] for k in QINDEX_V589_FIELDS))
    _v9_cm['1']['ladder']['rung'] = 'R4'                 # the caller edits its record later
    check('commit_qindex_v589_fields_are_copies_not_aliases',
          _q_v9[0]['ladder']['rung'] == 'R1')

    # non-first-mock: existing fields preserved + extended
    reg2 = copy.deepcopy(r1['registry'])
    r2 = commit_registry(reg2, {'question_hashes': ['h2']}, mini_bp(total_questions=3,
                         mocks=[{'mock': 2, 'paper_id': 'MOCK:M02'}]), 2,
                         paper_id='MOCK:M02', batches_completed=3, axis2_window_counts={},
                         passage_present=False, di_present=False, figural_present=False,
                         concept_map=mini_cm())
    check('commit_second_mock_preserves_first',
         set(r2['registry']['mocks_completed']) == {1, 2})
    check('commit_second_mock_extends_hashes',
         r2['registry']['question_hashes'] == ['h1', 'h2'])

    # FK hard-stop surfaces as a result flag, never raises
    bad_cm = {'1': {'subtopic_id': 'NOT.REAL', 'difficulty': 'Easy'}}
    check_raises_never('commit_fk_failure_is_a_flag_not_an_exception',
                       lambda: commit_registry(mini_registry(), mini_pending(), bp1, 1,
                           paper_id='MOCK:M01', batches_completed=1, axis2_window_counts={},
                           passage_present=False, di_present=False, figural_present=False,
                           concept_map=bad_cm)['ok'] is False)
    _fk = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=1, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=False, concept_map=bad_cm)
    check('commit_fk_failure_names_offender', 'Q1=' in _fk['fails'][0])
    check('commit_fk_failure_registry_is_original_unmodified',
         _fk['registry'] == mini_registry())

    # RC/DI/figural manifest conditional writes
    r_rc = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                           batches_completed=1, axis2_window_counts={}, passage_present=True,
                           di_present=False, figural_present=False, concept_map=mini_cm(),
                           passage_linked_qs=[1, 2], cloze_linked_qs=[3])
    check('commit_rc_manifest_written_when_present',
         r_rc['registry']['rc_manifests'][0]['passage_linked'] == [1, 2])
    r_norc = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                             batches_completed=1, axis2_window_counts={}, passage_present=False,
                             di_present=False, figural_present=False, concept_map=mini_cm())
    check('commit_rc_manifest_absent_when_not_present',
         r_norc['registry']['rc_manifests'] == [])

    # idempotent re-run of the SAME mock produces IDENTICAL output
    base = mini_registry()
    once = commit_registry(base, mini_pending(), bp1, 1, paper_id='MOCK:M01',
                           batches_completed=1, axis2_window_counts={}, passage_present=True,
                           di_present=False, figural_present=False, concept_map=mini_cm(),
                           passage_linked_qs=[1], cloze_linked_qs=[],
                           timestamp='2026-01-01T00:00:00+00:00')['registry']
    twice = commit_registry(once, mini_pending(), bp1, 1, paper_id='MOCK:M01',
                            batches_completed=1, axis2_window_counts={}, passage_present=True,
                            di_present=False, figural_present=False, concept_map=mini_cm(),
                            passage_linked_qs=[1], cloze_linked_qs=[],
                            timestamp='2026-01-01T00:00:00+00:00')['registry']
    check('commit_idempotent_mocks_completed_no_dup', twice['mocks_completed'] == [1])
    check('commit_idempotent_papers_completed_no_dup', twice['papers_completed'] == ['MOCK:M01'])
    check('commit_idempotent_session_log_no_dup', len(twice['session_log']) == 1)
    check('commit_idempotent_rc_manifests_no_dup', len(twice['rc_manifests']) == 1)
    check('commit_idempotent_question_index_no_dup', len(twice['question_index']) == 1)
    # Full-dict equality only holds on the fields deviation 4 actually makes
    # idempotent (replace-by-key). The dedup ledgers (question_hashes etc.)
    # are DELIBERATELY still append-only — see the very next check — so they
    # are excluded here rather than asserting whole-registry equality.
    _idem_fields = ['mocks_completed', 'papers_completed', 'session_log',
                    'rc_manifests', 'di_manifests', 'figural_manifests',
                    'question_index']
    check('commit_idempotent_full_rerun_stable_output',
         all(twice[f] == once[f] for f in _idem_fields))
    # non-idempotent-by-design fields DO still duplicate on re-run (named limitation)
    check('commit_dedup_lists_intentionally_not_idempotent',
         len(twice['question_hashes']) == 2 * len(once_input_hashes := ['h1']))

    # provenance stamp present when supplied, absent-safe when not
    r_prov = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                             batches_completed=1, axis2_window_counts={}, passage_present=False,
                             di_present=False, figural_present=False, concept_map=mini_cm(),
                             framework_repo_commit='abc123', spec_source_report={'ok': True})
    check('commit_provenance_stamped',
         r_prov['registry']['session_log'][0]['framework_repo_commit'] == 'abc123')
    r_noprov = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                               batches_completed=1, axis2_window_counts={}, passage_present=False,
                               di_present=False, figural_present=False, concept_map=mini_cm())
    check('commit_provenance_absent_safe',
         'framework_repo_commit' not in r_noprov['registry']['session_log'][0])

    # exhausted_subtopics read via .get(), not bare-indexed (a mock with zero
    # exhausted subtopics must not crash — §3 item 7 of the scoping doc)
    check_raises_never('commit_pending_without_exhausted_subtopics_key_does_not_crash',
                       lambda: commit_registry(mini_registry(), {'question_hashes': []},
                           bp1, 1, paper_id='MOCK:M01', batches_completed=1,
                           axis2_window_counts={}, passage_present=False, di_present=False,
                           figural_present=False, concept_map=mini_cm())['ok'] is True)

    # ── v5.54 A: same-series dedupe (PAPERID-KEYING) ─────────────────────
    def _commit(reg_in, n, pid):
        return commit_registry(reg_in, mini_pending(), bp1, n, paper_id=pid,
                               batches_completed=1, axis2_window_counts={},
                               passage_present=False, di_present=False,
                               figural_present=False, concept_map=mini_cm())['registry']
    # the historical trigger: paper_id corrected mid-session, same mock
    # re-committed — the stale sibling must be REPLACED, not accumulated
    _r1 = _commit(mini_registry(), 1, 'MOCK:M01')
    _r2 = _commit(_r1, 1, 'MOCK:M01-CORRECTED')
    check('rename_recommit_question_index_single_entry',
         len([e for e in _r2['question_index'] if e.get('mock') == 1]) == 1)
    check('rename_recommit_question_index_carries_new_id',
         _r2['question_index'][0]['paper_id'] == 'MOCK:M01-CORRECTED')
    check('rename_recommit_session_log_single_entry',
         len([e for e in _r2['session_log'] if e.get('mock') == 1]) == 1)
    check('rename_recommit_papers_completed_stale_id_removed',
         _r2['papers_completed'] == ['MOCK:M01-CORRECTED'])
    check('rename_recommit_mocks_completed_no_dup', _r2['mocks_completed'] == [1])
    # a DIFFERENT series with the same number legitimately coexists —
    # the widened dedupe must NEVER touch it
    _m1 = _commit(mini_registry(), 1, 'MOCK:M01')
    _mixed = _commit(_m1, 1, 'SUBJ:Physics:01')
    check('mixed_series_same_number_coexist_qindex',
         len(_mixed['question_index']) == 2)
    check('mixed_series_same_number_coexist_papers',
         set(_mixed['papers_completed']) == {'MOCK:M01', 'SUBJ:Physics:01'})
    check('mixed_series_mock_entry_untouched',
         any(e.get('paper_id') == 'MOCK:M01' for e in _mixed['question_index']))
    # unparseable stale number in papers_completed is left alone, not guessed at
    _odd = _commit(mini_registry(), 1, 'MOCK:M01')
    _odd['papers_completed'].insert(0, 'MOCK:MBROKEN')
    _odd2 = _commit(_odd, 1, 'MOCK:M01')
    check('unparseable_stale_paper_id_left_alone',
         'MOCK:MBROKEN' in _odd2['papers_completed'])

    # ── v5.55: SCOPED papers never pollute the mock ledger ───────────────
    # (GAP-2026-08-13-SCOPED-MOCKS-COMPLETED) A scoped commit records its
    # paper_id in papers_completed but must NOT append its bare ordinal to
    # mocks_completed — that fabricated a phantom MOCK:M03 that
    # registry_integrity_check / Step 11 / Step 9's P10 WARN then reported
    # as "REGISTRY DATA LOSS" forever.
    _sc = _commit(mini_registry(), 3, 'SUBJ:Physics:03')
    check('scoped_commit_leaves_mocks_completed_empty',
         _sc['mocks_completed'] == [])
    check('scoped_commit_records_paper_id',
         _sc['papers_completed'] == ['SUBJ:Physics:03'])
    check('scoped_then_mock_ledgers_independent',
         _commit(_sc, 3, 'MOCK:M03')['mocks_completed'] == [3])
    # registry_integrity_check no longer sees a phantom mock
    _ok_ic, _rep_ic = pp.registry_integrity_check(_sc)
    check('scoped_commit_passes_registry_integrity_check', _ok_ic is True)
    # a SCOPED entry must not MASK a genuinely missing MOCK entry of the
    # same number, and a scoped commit's own completeness must be checked
    # against the SCOPED series (not falsely against MOCK)
    check('scoped_entry_does_not_mask_missing_mock_entry',
         'no question_index entry' in ' '.join(_commit_problems(_sc, 3)))
    check('scoped_own_series_completeness_clean',
         _commit_problems(_sc, 3, series_prefix='SUBJ:Physics') == [])
    _sc_bp = mini_bp(mocks=[{'mock': 3, 'paper_id': 'SUBJ:Physics:03'}],
                     total_questions=3)
    _rc_sc = regcheck(_sc, _sc_bp, N=3, concept_map=mini_cm())
    check('regcheck_scoped_commit_ok_not_false_hard_stop', _rc_sc['ok'] is True)

    # regcheck detection side: a hand-left stale sibling for THIS mock's
    # slot is a HARD STOP; the same state on a historical mock is a warning
    _dup_reg = _commit(mini_registry(), 1, 'MOCK:M01')
    _dup_reg['question_index'].append(
        {'mock': 1, 'paper_id': 'MOCK:M01-OLD', 'questions': []})
    _rc_dup = regcheck(_dup_reg, bp1, N=1, concept_map=mini_cm())
    check('regcheck_this_mock_stale_sibling_hard_stops',
         _rc_dup['ok'] is False and 'DUP' in _rc_dup['fails'][0])
    _hist = _commit(_dup_reg, 2, 'MOCK:M02')  # mock 2 committed cleanly on top
    _rc_hist = regcheck(_hist, bp1, N=2, concept_map=mini_cm())
    check('regcheck_historical_stale_sibling_warns_not_fails',
         _rc_hist['ok'] is True and any('mock 1' in w and 'series' in w
                                        for w in _rc_hist['warnings']))
    # mixed series must NOT trip the duplicate detector
    _rc_mixed = regcheck(_mixed, bp1, N=1, concept_map=mini_cm())
    check('regcheck_mixed_series_not_flagged_as_duplicate',
         _rc_mixed['ok'] is True
         and not any('series' in w for w in _rc_mixed['warnings']))

    # ── v5.54 B: axis snapshot persistence (AXISPAPER-PERSISTENCE) ──────
    _snap1 = {'Section A': {'TEXT': 8, 'FIGURAL': 2, 'irreducible': 1}}
    _snap3 = {'Section A': {'MCQ': 7, 'MSQ': 2, 'NAT': 1}}
    r_ax = commit_registry(mini_registry(), mini_pending(), bp1, 1,
                           paper_id='MOCK:M01', batches_completed=1,
                           axis2_window_counts={}, passage_present=False,
                           di_present=False, figural_present=False,
                           concept_map=mini_cm(),
                           axis1_snapshots=_snap1, axis3_snapshots=_snap3)
    check('axis1_snapshot_persisted_mock_keyed',
         r_ax['registry']['axis1_paper']['1'] == _snap1)
    # v5.57 — paper_id key is the authority; a scoped paper of the SAME ordinal must
    # not touch the mock's snapshot, and two scoped series must not touch each other.
    check('axis_paper_id_keyed',
         r_ax['registry']['axis1_paper'].get('MOCK:M01') == _snap1
         and r_ax['registry']['axis3_paper'].get('MOCK:M01') == _snap3)
    _ax_bpx = dict(bp1); _ax_bpx['mocks'] = [{'mock': 1, 'paper_id': 'SUBJ:PHYS:01'}]
    _ax_reg = commit_registry(r_ax['registry'], mini_pending(), _ax_bpx, 1,
                              paper_id='SUBJ:PHYS:01', batches_completed=1,
                              axis2_window_counts={}, passage_present=False,
                              di_present=False, figural_present=False,
                              concept_map=mini_cm(),
                              axis1_snapshots={'Section A': {'TEXT': 1}})['registry']
    check('axis_scoped_does_not_clobber_mock',
         _ax_reg['axis1_paper'].get('MOCK:M01') == _snap1
         and _ax_reg['axis1_paper'].get('SUBJ:PHYS:01') == {'Section A': {'TEXT': 1}}
         and _ax_reg['axis1_paper'].get('1') == _snap1)
    _ax_bpy = dict(bp1); _ax_bpy['mocks'] = [{'mock': 1, 'paper_id': 'SUBJ:CHEM:01'}]
    _ax_reg2 = commit_registry(_ax_reg, mini_pending(), _ax_bpy, 1,
                               paper_id='SUBJ:CHEM:01', batches_completed=1,
                               axis2_window_counts={}, passage_present=False,
                               di_present=False, figural_present=False,
                               concept_map=mini_cm(),
                               axis1_snapshots={'Section A': {'TEXT': 2}})['registry']
    check('axis_two_scoped_series_coexist',
         _ax_reg2['axis1_paper'].get('SUBJ:PHYS:01') == {'Section A': {'TEXT': 1}}
         and _ax_reg2['axis1_paper'].get('SUBJ:CHEM:01') == {'Section A': {'TEXT': 2}})
    check('axis3_snapshot_persisted_mock_keyed',
         r_ax['registry']['axis3_paper']['1'] == _snap3)
    # deep-copied, not aliased (purity)
    _snap1['Section A']['TEXT'] = 999
    check('axis_snapshot_deep_copied_not_aliased',
         r_ax['registry']['axis1_paper']['1']['Section A']['TEXT'] == 8)
    # absent/empty ⇒ no write ⇒ feature-inert exams byte-identical
    r_noax = commit_registry(mini_registry(), mini_pending(), bp1, 1,
                             paper_id='MOCK:M01', batches_completed=1,
                             axis2_window_counts={}, passage_present=False,
                             di_present=False, figural_present=False,
                             concept_map=mini_cm(),
                             axis1_snapshots={}, axis3_snapshots=None)
    check('axis_snapshot_absent_safe_no_keys',
         'axis1_paper' not in r_noax['registry']
         and 'axis3_paper' not in r_noax['registry'])
    # idempotent: re-commit of the same mock REPLACES its [str(N)] slot
    r_ax2 = commit_registry(r_ax['registry'], mini_pending(), bp1, 1,
                            paper_id='MOCK:M01', batches_completed=1,
                            axis2_window_counts={}, passage_present=False,
                            di_present=False, figural_present=False,
                            concept_map=mini_cm(),
                            axis1_snapshots={'Section A': {'TEXT': 9}},
                            axis3_snapshots=_snap3)
    check('axis_snapshot_replace_by_mock_idempotent',
         r_ax2['registry']['axis1_paper'] == {'MOCK:M01': {'Section A': {'TEXT': 9}},
                                              '1': {'Section A': {'TEXT': 9}}})

    # ── regcheck ─────────────────────────────────────────────────────────
    clean_reg = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                                batches_completed=1, axis2_window_counts={},
                                passage_present=False, di_present=False, figural_present=False,
                                concept_map=mini_cm())['registry']
    rc_clean = regcheck(clean_reg, bp1, N=1, concept_map=mini_cm(), msq_meta={'total_options': 4})
    check('regcheck_clean_ok', rc_clean['ok'] is True)
    check('regcheck_clean_no_warnings', rc_clean['warnings'] == [])
    check('regcheck_options_by_q_written',
         rc_clean['registry']['options_by_q']['1']['1'] == 4)
    # ── v1.8 (GAP-2026-10-09-PAPER-SIZE-SERIES-AGNOSTIC) ─────────────────
    # (a) RESUMED SCOPED SERIES. mocks[].mock is the run-local ordinal (1..K) while
    #     paper_id carries paper_start+k (ScopedBlueprint S8), so paper :11 is
    #     ordinal 1 again. Measured on v1.7: committing SUBJ:U:11 erased SUBJ:U:01
    #     from papers_completed, question_index AND session_log. Each check below
    #     FAILS on v1.7.
    _rs1 = _commit(mini_registry(), 1, 'SUBJ:U:01')
    _rs2 = _commit(_rs1, 1, 'SUBJ:U:11')
    check('v18_resumed_scoped_papers_completed_keeps_earlier',
         _rs2['papers_completed'] == ['SUBJ:U:01', 'SUBJ:U:11'])
    check('v18_resumed_scoped_question_index_keeps_earlier',
         [e['paper_id'] for e in _rs2['question_index']] == ['SUBJ:U:01', 'SUBJ:U:11'])
    check('v18_resumed_scoped_session_log_keeps_earlier',
         [e['paper_id'] for e in _rs2['session_log']] == ['SUBJ:U:01', 'SUBJ:U:11'])
    _rs_bp = mini_bp(mocks=[{'mock': 1, 'paper_id': 'SUBJ:U:11'}])
    _rc_rs = regcheck(_rs2, _rs_bp, N=1, concept_map=mini_cm(), paper_id='SUBJ:U:11')
    check('v18_resumed_scoped_regcheck_ok_no_false_dup',
         _rc_rs['ok'] is True and _rc_rs['fails'] == [])
    _rs3 = _commit(_rs2, 1, 'SUBJ:U:11')          # same paper again: replaced, not added
    check('v18_resumed_scoped_recommit_idempotent',
         [e['paper_id'] for e in _rs3['question_index']] == ['SUBJ:U:01', 'SUBJ:U:11']
         and _rs3['papers_completed'] == ['SUBJ:U:01', 'SUBJ:U:11']
         and len(_rs3['session_log']) == 2)
    # a GENUINE stale sibling (same series, same paper NUMBER, different id) still stops
    _rs_dup = copy.deepcopy(_rs2)
    _rs_dup['question_index'].append({'mock': 1, 'paper_id': 'SUBJ:U:011', 'questions': []})
    _rc_rsd = regcheck(_rs_dup, _rs_bp, N=1, concept_map=mini_cm(), paper_id='SUBJ:U:11')
    check('v18_same_number_stale_sibling_still_hard_stops',
         _rc_rsd['ok'] is False and 'DUP' in _rc_rsd['fails'][0])
    # a SCOPED run no longer skips MOCK m == its own ordinal in the historical sweep
    _hw = _commit(mini_registry(), 1, 'MOCK:M01')
    _hw['question_index'] = []                    # MOCK:M01's commit is incomplete
    _hw = _commit(_hw, 1, 'SUBJ:U:01')
    _rc_hw = regcheck(_hw, mini_bp(mocks=[{'mock': 1, 'paper_id': 'SUBJ:U:01'}]), N=1,
                      concept_map=mini_cm(), paper_id='SUBJ:U:01')
    check('v18_scoped_run_still_warns_incomplete_mock_same_ordinal',
         _rc_hw['ok'] is True and any(w.startswith('mock 1:') for w in _rc_hw['warnings']))
    # (b) RC / DI / FIGURAL MANIFESTS keyed by paper_id. v1.7 replaced them by the
    #     ordinal on a registry shared across series: SUBJ:X:01 deleted MOCK:M01's.
    def _commit_fig(reg_in, n, pid, qs):
        return commit_registry(reg_in, mini_pending(), bp1, n, paper_id=pid,
                               batches_completed=1, axis2_window_counts={},
                               passage_present=True, di_present=True, figural_present=True,
                               concept_map=mini_cm(), passage_linked_qs=qs, cloze_linked_qs=[],
                               di_manifest={'questions': {str(q): {} for q in qs}},
                               fig_manifest={'questions': {str(q): {'object_type': 'line_graph'} for q in qs}})['registry']
    _mf = _commit_fig(_commit_fig(mini_registry(), 1, 'MOCK:M01', [1, 2]), 1, 'SUBJ:X:01', [3])
    for _key in ('rc_manifests', 'di_manifests', 'figural_manifests'):
        check(f'v18_{_key}_mock_and_scoped_coexist',
             sorted(e.get('paper_id') for e in _mf[_key]) == ['MOCK:M01', 'SUBJ:X:01'])
    def _fqs(reg_in, pid):
        return next((e.get('figural_qs') for e in reg_in.get('figural_manifests', [])
                     if e.get('paper_id') == pid), None)
    check('v18_figural_manifest_mock_content_intact', _fqs(_mf, 'MOCK:M01') == ['1', '2'])
    _mf2 = _commit_fig(_mf, 1, 'MOCK:M01', [2])
    check('v18_manifest_recommit_replaces_only_own_entry',
         len(_mf2['figural_manifests']) == 2
         and _fqs(_mf2, 'MOCK:M01') == ['2'] and _fqs(_mf2, 'SUBJ:X:01') == ['3'])
    # a LEGACY entry (no paper_id) belongs to MOCK:M<mock>: a scoped commit keeps it,
    # the mock's own commit replaces it
    _lg = mini_registry(figural_manifests=[{'mock': 1, 'figural_qs': ['9']}])
    _lg_sc = _commit_fig(_lg, 1, 'SUBJ:X:01', [3])
    check('v18_legacy_manifest_survives_scoped_commit',
         any(e.get('figural_qs') == ['9'] and 'paper_id' not in e
             for e in _lg_sc['figural_manifests']))
    _lg_mk = _commit_fig(_lg_sc, 1, 'MOCK:M01', [1])
    check('v18_legacy_manifest_replaced_by_its_mock',
         sorted(e.get('paper_id') for e in _lg_mk['figural_manifests'])
         == ['MOCK:M01', 'SUBJ:X:01']
         and not any(e.get('figural_qs') == ['9'] for e in _lg_mk['figural_manifests']))
    check('v18_entry_paper_id_helper',
         _entry_paper_id({'mock': 3}) == 'MOCK:M03'
         and _entry_paper_id({'mock': 3, 'paper_id': 'SUBJ:X:03'}) == 'SUBJ:X:03'
         and _entry_paper_id({'mock': 'x'}) is None and _entry_paper_id({}) is None
         and _entry_number({'mock': 1, 'paper_id': 'SUBJ:U:11'}) == 11
         and _entry_number({'mock': 1, 'paper_id': 'MOCK:M01-OLD'}) == 1
         and _entry_number({'mock': 4}) == 4)

    # v5.56 — options_by_q is paper_id-keyed; the ordinal key is MOCK-only and a
    # scoped paper with the same ordinal must NOT touch the mock's map.
    check('regcheck_options_by_q_paper_id_key',
         rc_clean['registry']['options_by_q'].get('MOCK:M01', {}).get('1') == 4)
    _sc_bpx = dict(bp1); _sc_bpx['mocks'] = [{'mock': 1, 'paper_id': 'SUBJ:PHYS:01'}]
    _sc_cm = {'1': {'subtopic_id': 'ex.a', 'difficulty': 'Easy', 'answer_type': 'numerical'}}
    _sc_reg = commit_registry(rc_clean['registry'], mini_pending(), _sc_bpx, 1,
                              paper_id='SUBJ:PHYS:01', batches_completed=1,
                              axis2_window_counts={}, passage_present=False,
                              di_present=False, figural_present=False,
                              concept_map=_sc_cm)['registry']
    rc_scoped = regcheck(_sc_reg, _sc_bpx, N=1, concept_map=_sc_cm,
                         msq_meta={'total_options': 4}, paper_id='SUBJ:PHYS:01')
    _obq = rc_scoped['registry']['options_by_q']
    check('regcheck_scoped_options_by_q_no_collision',
         _obq.get('SUBJ:PHYS:01') == {'1': 0} and _obq.get('1', {}).get('1') == 4
         and _obq.get('MOCK:M01', {}).get('1') == 4)
    check('regcheck_section_names_written',
         rc_clean['registry']['section_names'] == ['Section A'])
    check('regcheck_does_not_mutate_input', clean_reg['section_names'] == [])

    # v5.53 hardening fixtures (found in the final 0-bug audit): three
    # malformed-input shapes that used to crash regcheck() outright, in
    # violation of its own "never raises" docstring promise. All three are
    # degrade-gracefully, not silently-wrong: a non-numeric total_options
    # falls back to the documented default (4, matching the old spec-inline
    # try/except's fallback); a non-dict concept_map entry is treated as
    # "not numerical" (never crashes, never mis-detects a WELL-FORMED entry);
    # a wrong-typed options_by_q is reset to a dict, not indexed into.
    check_raises_never('regcheck_nonnumeric_total_options_does_not_crash',
                       lambda: regcheck(clean_reg, bp1, N=1, concept_map=mini_cm(),
                           msq_meta={'total_options': 'four'})['ok'] is True)
    check('regcheck_nonnumeric_total_options_falls_back_to_4',
         regcheck(clean_reg, bp1, N=1, concept_map=mini_cm(),
                  msq_meta={'total_options': 'four'})['registry']['options_by_q']['1']['1'] == 4)
    check_raises_never('regcheck_malformed_concept_map_entry_does_not_crash',
                       lambda: regcheck(clean_reg, bp1, N=1,
                           concept_map={'1': 'not-a-dict'})['ok'] is True)
    check('regcheck_malformed_concept_map_entry_treated_as_not_numerical',
         regcheck(clean_reg, bp1, N=1, concept_map={'1': 'not-a-dict'},
                  msq_meta={'total_options': 4})['registry']['options_by_q']['1']['1'] == 4)
    _wrongtype_reg = copy.deepcopy(clean_reg)
    _wrongtype_reg['options_by_q'] = ['not', 'a', 'dict']
    check_raises_never('regcheck_wrong_type_options_by_q_does_not_crash',
                       lambda: regcheck(_wrongtype_reg, bp1, N=1,
                           concept_map=mini_cm())['ok'] is True)
    check('regcheck_wrong_type_options_by_q_reset_to_dict',
         isinstance(regcheck(_wrongtype_reg, bp1, N=1,
                             concept_map=mini_cm())['registry']['options_by_q'], dict))

    # session_log / question_index are G-COMMIT-COMPLETE's own evidence for
    # THIS mock's commit — deleting either one doesn't just mean "drifted
    # template", it means mock N's own S13-4 write is gone. Self-heal still
    # recreates the field as an empty container (schema-complete), but
    # G-COMMIT-COMPLETE must then correctly HARD STOP (ok False), exactly as
    # the spec-inline code does — silently healing these two into an empty
    # list and reporting ok True would defeat the whole point of the gate.
    _commit_evidence_fields = {'session_log', 'question_index'}
    for _f in _REQUIRED_TOP:
        _broken = copy.deepcopy(clean_reg)
        del _broken[_f]
        _r = regcheck(_broken, bp1, N=1, concept_map=mini_cm())
        if _f in _commit_evidence_fields:
            check(f'regcheck_heals_missing_{_f}_but_gcommit_hardstops',
                 _f in _r['registry'] and _r['registry'][_f] == []
                 and _r['ok'] is False
                 and 'mock 1' in _r['fails'][0])
        else:
            check(f'regcheck_heals_missing_{_f}', _f in _r['registry'] and _r['ok'] is True)

    # G-COMMIT-COMPLETE: THIS mock broken -> ok False
    broken_this = copy.deepcopy(clean_reg)
    broken_this['session_log'] = []
    r_broken_this = regcheck(broken_this, bp1, N=1, concept_map=mini_cm())
    check('regcheck_this_mock_incomplete_fails', r_broken_this['ok'] is False)
    check('regcheck_this_mock_incomplete_names_mock',
         'mock 1' in r_broken_this['fails'][0])

    # G-COMMIT-COMPLETE: a DIFFERENT (earlier) mock broken -> ok True + warning
    # (this is the exact Mock-4 historical shape)
    reg_m4 = mini_registry(
        mocks_completed=[1, 2, 3, 4, 5],
        session_log=[{'mock': i, 'paper_id': f'MOCK:M0{i}'} for i in (1, 2, 3, 5)],
        question_index=[{'mock': i, 'paper_id': f'MOCK:M0{i}', 'questions': []}
                        for i in (1, 2, 3)]
        + [{'mock': 4, 'paper_id': None, 'questions': []}]
        + [{'mock': 5, 'paper_id': 'MOCK:M05', 'questions': []}],
    )
    r_m4 = regcheck(reg_m4, bp1, N=5, concept_map={})
    check('regcheck_legacy_mock4_shape_warns_not_fails', r_m4['ok'] is True)
    check('regcheck_legacy_mock4_shape_names_mock4',
         len(r_m4['warnings']) == 1 and 'mock 4' in r_m4['warnings'][0])

    # mutation check: prove the THIS-mock branch's raise-equivalent is
    # load-bearing, not incidental — a variant with it removed lets a
    # broken current-mock commit through as a mere warning
    def _regcheck_neutered_this_mock_gate(reg, bp, N):
        problems = {m: _commit_problems(reg, m) for m in reg.get('mocks_completed', [])}
        return {'ok': True, 'warnings': [f"mock {m}: {p}" for m, p in problems.items() if p]}
    _neutered = _regcheck_neutered_this_mock_gate(broken_this, bp1, 1)
    check('regcheck_mutation_neutered_gate_lets_broken_current_mock_through_silently',
         _neutered['ok'] is True and any('mock 1' in w for w in _neutered['warnings']))

    # ── qindex_certify ───────────────────────────────────────────────────
    qi_clean = qindex_certify(clean_reg, bp1, 1)
    check('qindex_clean_ok', qi_clean['ok'] is True)

    no_entry_reg = mini_registry()
    check('qindex_check1_no_entry', qindex_certify(no_entry_reg, bp1, 1)['ok'] is False)

    short_reg = copy.deepcopy(clean_reg)
    short_reg['question_index'][0]['questions'] = short_reg['question_index'][0]['questions'][:1]
    check('qindex_check2_wrong_count', qindex_certify(short_reg, bp1, 1)['ok'] is False)

    dup_reg = copy.deepcopy(clean_reg)
    dup_reg['question_index'][0]['questions'][1]['q'] = 1
    check('qindex_check3_dup_q', qindex_certify(dup_reg, bp1, 1)['ok'] is False)

    badid_reg = copy.deepcopy(clean_reg)
    badid_reg['question_index'][0]['questions'][0]['subtopic_id'] = 'NOT.REAL'
    check('qindex_check4_bad_subtopic', qindex_certify(badid_reg, bp1, 1)['ok'] is False)

    badd_reg = copy.deepcopy(clean_reg)
    badd_reg['question_index'][0]['questions'][0]['difficulty'] = 'Impossible'
    check('qindex_check5_bad_difficulty', qindex_certify(badd_reg, bp1, 1)['ok'] is False)

    wrongdist_reg = copy.deepcopy(clean_reg)
    for q in wrongdist_reg['question_index'][0]['questions']:
        q['difficulty'] = 'Easy'
    check('qindex_check6_wrong_distribution', qindex_certify(wrongdist_reg, bp1, 1)['ok'] is False)

    # NOTE: earlier drafts of this suite also cross-checked qindex_certify()
    # against audit_canonical.gate_qindex() directly (`import audit_canonical`)
    # as a belt-and-braces parity fixture. Deliberately removed: (1) it is
    # redundant — qindex_certify() delegates to paper_pipeline.validate_
    # question_index(), which is ALREADY parity-tested against audit_
    # canonical.gate_qindex() in paper_pipeline.py's own self-test ("QINDEX
    # PARITY"); testing it again here would just be re-deriving a guarantee
    # that already exists one level down. (2) audit_canonical.py is, by this
    # repo's own convention (see routes.json / the mock-test-framework skill),
    # one of the tracked-but-NEVER-ROUTED scripts — copied per-exam and
    # invoked via subprocess (S13-4c), never imported as a module dependency
    # of a routed engine. An `import audit_canonical` anywhere in this file,
    # even self-test-only, trips validate_framework_md.py's Check AI (ENGINE
    # DEPENDENCY PARITY): it would demand audit_canonical.py be added to
    # routes.json's MockCreate/TestCreate entries, which is exactly the
    # never-routed convention this module deliberately does not break.

    check('qindex_shares_paper_pipeline_implementation',
         qindex_certify.__doc__ is not None and 'validate_question_index' in
         qindex_certify.__doc__)

    # ── predelivery_checklist ────────────────────────────────────────────
    def fake_fs(files):
        return (lambda d: sorted(files)), (lambda p: p.rsplit('/', 1)[-1] in files)

    files_ok = {'EX_Mock01_Create.docx', 'EX_registry.json'}
    ld, ex = fake_fs(files_ok)
    chk_ok = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                   reg_name='EX_registry.json', regcheck_ok=True,
                                   qindex_ok=True, listdir=ld, exists=ex)
    check('predelivery_all_pass', chk_ok['ok'] is True)

    ld2, ex2 = fake_fs(set())
    chk_1 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=True,
                                  qindex_ok=True, listdir=ld2, exists=ex2)
    check('predelivery_check1_missing_docx', chk_1['checks'][0] == ('1 final docx in outputs', False))
    check('predelivery_check2_missing_registry', chk_1['checks'][1][1] is False)

    ld3, ex3 = fake_fs(files_ok)
    chk_3 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=False,
                                  qindex_ok=True, listdir=ld3, exists=ex3)
    check('predelivery_check3_regcheck_not_ok', chk_3['checks'][2] == ('3 registry schema complete', False))

    files_ak = files_ok | {'EX_M1_answer_key.json'}
    ld4, ex4 = fake_fs(files_ak)
    chk_4 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=True,
                                  qindex_ok=True, listdir=ld4, exists=ex4)
    check('predelivery_check4_answer_key_leaked', chk_4['checks'][3][1] is False)

    files_bs = files_ok | {'EX_M1_batch_state.json'}
    ld5, ex5 = fake_fs(files_bs)
    chk_5 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=True,
                                  qindex_ok=True, listdir=ld5, exists=ex5)
    check('predelivery_check5_internal_sidecar_leaked', chk_5['checks'][4][1] is False)

    files_extra = files_ok | {'EX_Mock01_scratch.txt'}
    ld6, ex6 = fake_fs(files_extra)
    chk_6 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=True,
                                  qindex_ok=True, listdir=ld6, exists=ex6)
    check('predelivery_check6_extra_file', chk_6['checks'][5][1] is False)
    # v1.13 (GAP-2026-11-04): another step's / exam's / paper's earlier output in the same
    # chat is not this delivery and never blocks it; this run's leftovers are cleared first
    _hist = files_ok | {'stray_file.txt', 'OTHER_registry.json', 'EX_Mock00_Create.docx', 'EX_Mock00_Explain.docx'}
    ld6b, ex6b = fake_fs(_hist)
    check('predelivery_v113_unrelated_history_never_blocks', predelivery_checklist(
        '/out', docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json', regcheck_ok=True,
        qindex_ok=True, listdir=ld6b, exists=ex6b)['ok'] is True)
    _run = {'EX_Mock01_Q1to25.docx', 'EX_Mock01_Q1to50.docx', 'EX_Mock01_review_packet.zip',
            'EX_Mock01_review_verdicts.json', 'EX_M1_batch_state.json', 'EX_mock_test_audit.py',
            'EX_SUBJ_X_blueprint.json', 'EX_Mock00_Create.docx', 'stray_file.txt', 'EXAMPLE_Mock01_Q1to5.docx',
            'EX_Mock00_answer_sheet.docx', 'EX_Mock01_answers.pdf'}
    _clr = outputs_to_clear(files_ok | _run, docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json')
    check('outputs_to_clear_this_run_only', _clr == sorted(_run - {'EX_Mock00_Create.docx', 'stray_file.txt', 'EXAMPLE_Mock01_Q1to5.docx',
                                                                    'EX_mock_test_audit.py', 'EX_SUBJ_X_blueprint.json',
                                                                    'EX_Mock00_answer_sheet.docx'})
          and outputs_to_clear(files_ok, docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json') == []
          and outputs_to_clear(_run, docx_name='x.docx', reg_name='nope.json') == [])
    check('internal_markers_anchored_to_this_run',
          outputs_to_clear(files_ok | {'EX_scan_progress.json', 'EX_M2_stimulus_profile.json', 'EX_M1_s13_2f_state.json', 'EX_fig_manifest.json'},
                           docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json')
          == ['EX_M1_s13_2f_state.json', 'EX_M2_stimulus_profile.json', 'EX_fig_manifest.json']
          and predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json', regcheck_ok=True,
                                    qindex_ok=True, listdir=fake_fs(files_ok | {'EX_scan_progress.json'})[0],
                                    exists=fake_fs(files_ok | {'EX_scan_progress.json'})[1])['ok'] is True
          and predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json', regcheck_ok=True,
                                    qindex_ok=True, listdir=fake_fs(files_ok | {'EX_M1_s13_2f_state.json'})[0],
                                    exists=fake_fs(files_ok | {'EX_M1_s13_2f_state.json'})[1])['ok'] is False)
    check('delivery_scope_this_paper_only', delivery_scope(_hist | {'EX_Mock01_Q1to5.docx'}, docx_name='EX_Mock01_Create.docx',
                                                           reg_name='EX_registry.json')
          == ['EX_Mock01_Create.docx', 'EX_Mock01_Q1to5.docx', 'EX_registry.json'])
    ld6c, ex6c = fake_fs(files_ok | {'EX_Mock01_Q1to50.docx', 'EX_Mock01_review_packet.zip'})
    check('predelivery_v113_leftover_packet_breaks_until_cleared', predelivery_checklist(
        '/out', docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json', regcheck_ok=True,
        qindex_ok=True, listdir=ld6c, exists=ex6c)['ok'] is False)

    ld7, ex7 = fake_fs(files_ok)
    chk_7 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=True,
                                  qindex_ok=False, listdir=ld7, exists=ex7)
    check('predelivery_check7_qindex_not_ok', chk_7['checks'][6][1] is False)

    # v5.60 — the dossier is INTERNAL: staged in outputs it is a LEAK (check 5) and
    # breaks the closed set (check 6); absent, the 2-file set is clean.
    files_dossier = files_ok | {'EX_M1_audit_dossier.json'}
    ld8, ex8 = fake_fs(files_dossier)
    chk_8 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json',
                                  dossier_name='EX_M1_audit_dossier.json',
                                  regcheck_ok=True, qindex_ok=True, listdir=ld8, exists=ex8)
    check('predelivery_check5_dossier_in_outputs_is_a_leak', chk_8['checks'][4][1] is False)
    check('predelivery_check6_dossier_breaks_closed_set', chk_8['checks'][5][1] is False
          and chk_8['ok'] is False)
    ld8b, ex8b = fake_fs(files_ok)
    chk_8b = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                   reg_name='EX_registry.json',
                                   dossier_name='EX_M1_audit_dossier.json',
                                   regcheck_ok=True, qindex_ok=True, listdir=ld8b, exists=ex8b)
    check('predelivery_two_file_closed_set_clean', chk_8b['ok'] is True
          and '2 deliverables' in chk_8b['checks'][5][0])

    # v1.11 — conditional extras (P2/P3): a recomputed blueprint and a repo auditor
    # copy join the closed set only when named; a sidecar can never be laundered in.
    _x = files_ok | {'EX_SUBJ_ORG_blueprint.json', 'EX_mock_test_audit.py'}
    ld9, ex9 = fake_fs(_x)
    chk_9 = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                  reg_name='EX_registry.json', regcheck_ok=True,
                                  qindex_ok=True, listdir=ld9, exists=ex9,
                                  extra_deliverables=('EX_SUBJ_ORG_blueprint.json',
                                                      'EX_mock_test_audit.py'))
    # v1.13 (D3 a): extras are NEVER delivered — named or not, they break the 2-file set,
    # and outputs_to_clear names them so S13-7 removes them before the checklist
    # another step's blueprint / auditor copy presented earlier in the chat is outside this
    # paper's delivery scope: never deleted, never delivered, never blocking (release review)
    check('predelivery_v113_extras_never_widen_the_set', chk_9['ok'] is True
          and outputs_to_clear(_x, docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json') == []
          and delivery_scope(_x, docx_name='EX_Mock01_Create.docx', reg_name='EX_registry.json')
          == ['EX_Mock01_Create.docx', 'EX_registry.json'])
    ld9b, ex9b = fake_fs(_x)
    chk_9b = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                   reg_name='EX_registry.json', regcheck_ok=True,
                                   qindex_ok=True, listdir=ld9b, exists=ex9b)
    check('predelivery_v113_other_step_outputs_not_in_scope', chk_9b['ok'] is True)
    _x2 = files_ok | {'EX_M1_answer_key.json'}
    ld9c, ex9c = fake_fs(_x2)
    chk_9c = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                   reg_name='EX_registry.json', regcheck_ok=True,
                                   qindex_ok=True, listdir=ld9c, exists=ex9c,
                                   extra_deliverables=('EX_M1_answer_key.json',))
    check('predelivery_v111_sidecar_cannot_be_laundered_as_extra', chk_9c['ok'] is False)
    # a name that trips NO other check (not an answer key, not a known internal sidecar):
    # only the extras filter (*_blueprint.json / *_mock_test_audit.py) can reject it
    _x3 = files_ok | {'EX_Mock01_notes.json'}
    ld9d, ex9d = fake_fs(_x3)
    chk_9d = predelivery_checklist('/out', docx_name='EX_Mock01_Create.docx',
                                   reg_name='EX_registry.json', regcheck_ok=True,
                                   qindex_ok=True, listdir=ld9d, exists=ex9d,
                                   extra_deliverables=('EX_Mock01_notes.json',))
    check('predelivery_v111_only_blueprint_or_auditor_names_are_extras', chk_9d['ok'] is False)

    # missing outputs_dir entirely does not crash (§ Angle 6 of the design's
    # adversarial review — first-run-before-makedirs case)
    def raising_listdir(_d):
        raise FileNotFoundError()
    check_raises_never('predelivery_missing_outputs_dir_does_not_crash',
                       lambda: predelivery_checklist('/does/not/exist',
                           docx_name='x', reg_name='y', regcheck_ok=True, qindex_ok=True,
                           listdir=raising_listdir, exists=lambda p: False)['ok'] is False)

    # v5.53 hardening fixtures (found in the final 0-bug audit): the guard
    # above only ever exercised FileNotFoundError. A real outputs_dir can
    # also fail to list with NotADirectoryError (a file occupies where the
    # directory should be) or PermissionError (restricted ACL) — both real
    # OSError subclasses, both now caught by the same broadened `except
    # OSError` this function uses.
    def notadir_listdir(_d):
        raise NotADirectoryError()
    check_raises_never('predelivery_not_a_directory_does_not_crash',
                       lambda: predelivery_checklist('/some/file/path',
                           docx_name='x', reg_name='y', regcheck_ok=True, qindex_ok=True,
                           listdir=notadir_listdir, exists=lambda p: False)['ok'] is False)

    def permission_listdir(_d):
        raise PermissionError()
    check_raises_never('predelivery_permission_error_does_not_crash',
                       lambda: predelivery_checklist('/restricted',
                           docx_name='x', reg_name='y', regcheck_ok=True, qindex_ok=True,
                           listdir=permission_listdir, exists=lambda p: False)['ok'] is False)

    # ── v5.55 key commitments + semantic objects ──────────────────────────
    _ak = {'answers': {'1': 2, '2': [1, 3], '3': 3.09},
           'concept_map': {'1': {'qtype': 'mcq'}, '2': {'qtype': 'msq'},
                           '3': {'qtype': 'nat', 'nat_grading_value': '3.09'}}}
    r_k = commit_registry(mini_registry(), mini_pending(), bp1, 1,
                          paper_id='MOCK:M01', batches_completed=3,
                          axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=False,
                          concept_map=mini_cm(), answer_key=_ak)
    _kc = r_k['registry'].get('key_commitments', {}).get('MOCK:M01')
    check('commit_key_commitments_written', bool(_kc) and set(_kc['entries']) == {'1', '2', '3'})
    import paper_pipeline as _ppt
    check('commit_key_commitments_verify_roundtrip',
          _ppt.verify_key_commitments(_kc, {1: '2', 2: '1,3', 3: '3.09'}, 'MOCK:M01')['matched'] == [1, 2, 3])
    check('commit_key_commitments_no_plaintext',
          '"answers"' not in __import__('json').dumps(r_k['registry']) and
          all(len(e['h']) == 64 for e in _kc['entries'].values()))
    check('commit_key_commitments_absent_without_key',
          'key_commitments' not in r1['registry'])
    _fm = {'questions': {'47': {'image_hashes': ['h'], 'object_type': 'structure',
                                'subtopic_id': 'ex.a', 'object_type': 'chemical_structure',
                                'semantic_objects': [{'role': 'problem', 'kind': 'STRUCTURE',
                                                      'name': 'salicylic acid',
                                                      'canonical': 'Oc1ccccc1C(O)=O',
                                                      'descriptor': {}}]}}}
    r_f = commit_registry(mini_registry(), mini_pending(), bp1, 1,
                          paper_id='MOCK:M01', batches_completed=3,
                          axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=True,
                          concept_map=mini_cm(), fig_manifest=_fm)
    _so = r_f['registry']['figural_manifests'][0].get('semantic_objects', {})
    check('commit_semantic_objects_written', '47' in _so and _so['47'][0]['kind'] == 'STRUCTURE')
    import corpus_io as _ciot
    _canon_ok = _ciot.canonical_structure('OC(=O)c1ccccc1O')[1] == 'ok'
    check('commit_semantic_objects_canonicalised',
          (not _canon_ok) or _so['47'][0]['canonical'] == _ciot.canonical_structure('OC(=O)c1ccccc1O')[0])
    def _bad_sem():
        _fm2 = {'questions': {'47': {'image_hashes': ['h'], 'subtopic_id': 'ex.a',
                                     'object_type': 'chemical_structure',
                                     'semantic_objects': [{'role': 'problem', 'kind': 'STRUCTURE',
                                                           'name': 'x', 'canonical': '',
                                                           'descriptor': {}}]}}}
        commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                        batches_completed=3, axis2_window_counts={}, passage_present=False,
                        di_present=False, figural_present=True, concept_map=mini_cm(),
                        fig_manifest=_fm2)
        return True
    try:
        _bad_sem(); check('commit_semantic_objects_malformed_raises', False)
    except ValueError:
        check('commit_semantic_objects_malformed_raises', True)

    # ── v1.9 — GAP-2026-11-01 MANIFEST-COMMIT-LAW (F3.1) + F2.3 + migration ───────
    # Each fixture FAILS on v1.8 (the record was suppressed / accepted / unannotated).
    _fm9 = {'questions': {'1': {'image_hashes': ['h1'], 'subtopic_id': 'ex.a',
                                'object_type': 'reaction_scheme',
                                'semantic_objects': [{'role': 'problem', 'kind': 'REACTION', 'name': 'r',
                                                      'canonical': 'CCBr>>CCO', 'descriptor': {}}]}}}
    r9 = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='SUBJ:X:01',
                         batches_completed=3, axis2_window_counts={}, passage_present=False,
                         di_present=False, figural_present=False, concept_map=mini_cm(), fig_manifest=_fm9)
    _fg9 = [e for e in r9['registry']['figural_manifests'] if e.get('paper_id') == 'SUBJ:X:01']
    check('v19_flag_false_manifest_nonempty_STILL_COMMITS', len(_fg9) == 1 and _fg9[0]['object_types'] == {'1': 'reaction_scheme'})
    _pf9 = r9['registry'].get('paper_flags', {}).get('SUBJ:X:01', {})
    check('v19_flag_disagreement_recorded', _pf9.get('figural_present') is False and _pf9.get('figural_present_derived') is True)
    check('v19_reaction_object_commits_end_to_end',
          _fg9 and _fg9[0]['semantic_objects']['1'][0]['canonical'].count('>') == 2)
    r9b = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=3, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=False, concept_map=mini_cm(), fig_manifest=None)
    check('v19_no_manifest_no_record_no_disagreement',
          not r9b['registry'].get('figural_manifests')
          and r9b['registry']['paper_flags']['MOCK:M01']['figural_present_derived'] is False)
    r9c = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=3, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=True, concept_map=mini_cm(),
                          fig_manifest={'questions': {}})
    check('v19_empty_manifest_with_true_flag_commits_as_v1_8',
          len(r9c['registry'].get('figural_manifests', [])) == 1
          and r9c['registry']['paper_flags']['MOCK:M01']['figural_present'] is True
          and r9c['registry']['paper_flags']['MOCK:M01']['figural_present_derived'] is False)   # v1.10: derived = manifest truth only
    check('v110_record_schema_stamped', r9c['registry']['figural_manifests'][0].get('record_schema') == FIGURE_RECORD_SCHEMA)
    # E15 — resumed pre-v5.88 question: committed only when S4-12 marked it legacy_unlabelled
    r9e = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=3, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=True, concept_map=mini_cm(),
                          fig_manifest={'questions': {'7': {'image_hashes': ['h7'], 'subtopic_id': 'ex.a',
                                                            'record_integrity': 'legacy_unlabelled'}}})
    _e9e = r9e['registry']['figural_manifests'][0]
    check('v110_legacy_unlabelled_resume_commits_disclosed',
          _e9e['object_types'] == {'7': 'legacy_unlabelled'} and _e9e['record_integrity'] == {'7': 'legacy_unlabelled'})
    # E15 second variant: a pre-v5.88 REACTION object with a MOLECULE canonical commits unvalidated
    _fm9f = {'questions': {'7': {'image_hashes': ['h7'], 'subtopic_id': 'ex.a', 'record_integrity': 'legacy_unlabelled',
                                 'semantic_objects': [{'role': 'problem', 'kind': 'REACTION', 'name': 'r', 'canonical': 'CCO', 'descriptor': {}}]}}}
    r9f = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=3, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=True, concept_map=mini_cm(), fig_manifest=_fm9f)
    check('v110_legacy_unlabelled_degenerate_reaction_commits_unvalidated',
          r9f['registry']['figural_manifests'][0]['semantic_objects']['7'][0]['canonical'] == 'CCO')
    check('v110_commit_does_not_mutate_caller_manifest', 'object_type' not in _fm9f['questions']['7'])
    # v1.12 — G-MEDIAREUSE (GAP-2026-11-03 OD-13 (i)): the incident shape — one media part
    # under two questions — is REFUSED at commit with the ladder message; a linked set
    # (stimulus_group_id) sharing its stimulus picture commits; distinct pictures commit.
    _cm12 = mini_cm()
    _fm12 = {'questions': {'7': {'image_hashes': ['same-md5'], 'subtopic_id': 'ex.a', 'object_type': 'line_graph'},
                           '8': {'image_hashes': ['same-md5'], 'subtopic_id': 'ex.a', 'object_type': 'line_graph'}}}
    r12 = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=3, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=True, concept_map=_cm12, fig_manifest=_fm12)
    check('v112_media_reuse_refused_at_commit',
          r12['ok'] is False and 'LADDER-REPAIR R2 G-MEDIAREUSE' in r12['fails'][0] and 'Q8 reuses Q7' in r12['fails'][0]
          and r12['registry'] is mini_registry() or r12['registry'].get('figural_manifests', []) == [])
    _cm12l = copy.deepcopy(_cm12)
    for _k in list(_cm12l)[:2]:
        _cm12l[_k]['stimulus_group_id'] = 'SG1'
    _fm12l = {'questions': {str(_k): {'image_hashes': ['same-md5'], 'subtopic_id': 'ex.a', 'object_type': 'line_graph'}
                            for _k in list(_cm12l)[:2]}}
    r12l = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                           batches_completed=3, axis2_window_counts={}, passage_present=False,
                           di_present=False, figural_present=True, concept_map=_cm12l, fig_manifest=_fm12l)
    _fm12d = {'questions': {'7': {'image_hashes': ['a'], 'subtopic_id': 'ex.a', 'object_type': 'line_graph'},
                            '8': {'image_hashes': ['b'], 'subtopic_id': 'ex.a', 'object_type': 'line_graph'}}}
    r12d = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                           batches_completed=3, axis2_window_counts={}, passage_present=False,
                           di_present=False, figural_present=True, concept_map=_cm12, fig_manifest=_fm12d)
    check('v112_media_reuse_linked_set_and_distinct_commit', r12l['ok'] is True and r12d['ok'] is True)
    # v1.12 — producer_release on the certificate; V590 verdict fields carried only when present
    _cm12v = mini_cm()
    _k0 = sorted(_cm12v, key=int)[0]
    _cm12v[_k0].update({'quality_status': 'UNRESOLVED(A-STEMLEAK)', 'shape': 'product_prediction|none',
                        'option_identities': ['a', 'b'], 'review': {'key_agrees': True}})
    r12v = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                           batches_completed=1, axis2_window_counts={}, passage_present=False,
                           di_present=False, figural_present=False, concept_map=_cm12v)
    _e12v = r12v['registry']['question_index'][0]
    _e12r = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01', batches_completed=1,
                            axis2_window_counts={}, passage_present=False, di_present=False, figural_present=False,
                            concept_map=mini_cm(), quality_readiness={'degraded': ['G-X'], 'controls': {}})
    _e12rv = _e12r['registry']['question_index'][0]
    check('v112_quality_readiness_committed', _e12rv.get('quality_readiness', {}).get('degraded') == ['G-X']
          and 'quality_readiness' not in _e12v)
    _e12ds = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01', batches_completed=1,
                             axis2_window_counts={}, passage_present=False, di_present=False, figural_present=False,
                             concept_map=mini_cm(), difficulty_state={'hard_missed': 2, 'judge_dormant_qs': [3]})
    check('v114_difficulty_state_committed',
          _e12ds['registry']['question_index'][0].get('difficulty_state') == {'hard_missed': 2, 'judge_dormant_qs': [3]}
          and 'difficulty_state' not in _e12v)
    _e12s = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01', batches_completed=1,
                            axis2_window_counts={}, passage_present=False, di_present=False, figural_present=False,
                            concept_map=mini_cm(), shape_infeasible=['two_part'])
    check('v112_shape_infeasible_committed', _e12s['registry']['question_index'][0].get('shape_infeasible') == ['two_part']
          and 'shape_infeasible' not in _e12rv)
    _e12n = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01', batches_completed=1,
                            axis2_window_counts={}, passage_present=False, di_present=False, figural_present=True,
                            concept_map=None, fig_manifest={'questions': {}})
    check('v112_none_concept_map_tolerated', isinstance(_e12n, dict) and 'registry' in _e12n)
    check('v112_producer_release_and_v590_fields',
          _e12v['qindex_cert']['producer_release'] == bc.QQ_RELEASE
          and _e12v['qindex_cert']['stamps_release'] == bc.STAMPS_RELEASE == '2026.11.04'
          and _e12v['questions'][0]['quality_status'] == 'UNRESOLVED(A-STEMLEAK)'
          and _e12v['questions'][0]['shape'] == 'product_prediction|none'
          and not any(k in _e12v['questions'][1] for k in QINDEX_V590_FIELDS))
    # v1.10 — a CURRENT (stamped) false record is never annotated into "legacy"
    _cur = copy.deepcopy(r9e['registry'])
    _cur['figural_manifests'][0].update({'object_types': {'1': 'reaction_scheme'},
                                         'semantic_objects': {'1': [{'role': 'problem', 'kind': 'STRUCTURE', 'canonical': 'CCO'}]},
                                         'record_integrity': {}})
    _m2, _n2 = annotate_legacy_figure_records(_cur, kind_of=lambda ot: ('REACTION',) if ot == 'reaction_scheme' else None)
    check('v110_migration_skips_stamped_current_records', not _n2 and not _m2['figural_manifests'][0].get('record_integrity'))
    # legacy shapes: problem:1 roles, string counts, mocks_completed-only registries
    _lg = {'mocks_completed': [1], 'papers_completed': [], 'figural_manifests': [
               {'mock': 1, 'paper_id': 'MOCK:M01', 'object_types': {'3': 'reaction_scheme'},
                'semantic_objects': {'3': [{'role': 'problem:1', 'kind': 'STRUCTURE', 'canonical': 'CCO'}]}}],
           'mocks_completed': [1, 2]}
    _a1k = 'axis1_paper'          # READ-side fixture key: never a dict literal (audit_seam)
    _lg[_a1k] = {'MOCK:M02': {'S1': {'FIGURAL': '4'}}}
    _m3, _n3 = annotate_legacy_figure_records(_lg, kind_of=lambda ot: ('REACTION',) if ot == 'reaction_scheme' else None)
    check('v110_migration_multirow_role_and_string_counts',
          _m3['figural_manifests'][0]['record_integrity'] == {'3': 'legacy_label_mismatch'}
          and _m3['paper_flags']['MOCK:M02']['figure_record'] == 'absent_legacy')
    _lg2 = {'mocks_completed': [1], 'figural_manifests': [], _a1k: {'1': {'S1': {'FIGURAL': 5}}}}
    check('v110_migration_ordinal_keyed_axis1', annotate_legacy_figure_records(_lg2)[0]['paper_flags']['MOCK:M01']['figure_record'] == 'absent_legacy')
    r9d = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=3, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=False, concept_map=mini_cm(),
                          di_manifest={'questions': {'5': {'subtopic_id': 'ex.b', 'table_shape': [2, 2]}}})
    check('v19_di_manifest_commits_without_flag', [e for e in r9d['registry']['di_manifests'] if e.get('di_qs') == [5]])
    r9e = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                          batches_completed=3, axis2_window_counts={}, passage_present=False,
                          di_present=False, figural_present=False, concept_map=mini_cm(),
                          passage_linked_qs=[1, 2])
    check('v19_rc_manifest_commits_without_flag', [e for e in r9e['registry']['rc_manifests'] if e.get('passage_linked') == [1, 2]])
    def _no_type():
        commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                        batches_completed=3, axis2_window_counts={}, passage_present=False,
                        di_present=False, figural_present=True, concept_map=mini_cm(),
                        fig_manifest={'questions': {'3': {'image_hashes': ['h'], 'subtopic_id': 'ex.a'}}})
    try:
        _no_type(); check('v19_missing_object_type_raises', False)
    except ValueError as _e9:
        check('v19_missing_object_type_raises', 'object_type' in str(_e9) and "['3']" in str(_e9))
    # migration annotator
    _legacy = mini_registry(papers_completed=['MOCK:M01', 'SUBJ:X:01', 'SUBJ:X:02'],
                            axis1_paper={'SUBJ:X:01': {'S': {'FIGURAL': 36, 'TEXT': 4}},
                                         'SUBJ:X:02': {'S': {'FIGURAL': 0, 'TEXT': 40}}},
                            figural_manifests=[{'mock': 1, 'paper_id': 'MOCK:M01',
                                                'object_types': {'1': 'reaction_scheme', '2': 'reaction_scheme', '3': 'chemical_structure'},
                                                'semantic_objects': {'1': [{'role': 'problem', 'kind': 'STRUCTURE', 'canonical': 'CCO'}],
                                                                     '2': [{'role': 'problem', 'kind': 'REACTION', 'canonical': 'BrBr.CCC#CCC'}],
                                                                     '3': [{'role': 'problem', 'kind': 'STRUCTURE', 'canonical': 'CCO'}]}}])
    _kind_of = lambda ot: {'reaction_scheme': ('REACTION',), 'chemical_structure': ('STRUCTURE', 'COORDINATION')}.get(ot)
    _mig, _notes = annotate_legacy_figure_records(_legacy, kind_of=_kind_of)
    _ri = _mig['figural_manifests'][0].get('record_integrity', {})
    check('v19_migration_label_mismatch_annotated', _ri.get('1') == 'legacy_label_mismatch')
    check('v19_migration_degenerate_reaction_annotated', _ri.get('2') == 'legacy_degenerate_reaction')
    check('v19_migration_consistent_record_untouched', '3' not in _ri)
    check('v19_migration_absent_record_flagged',
          _mig['paper_flags']['SUBJ:X:01']['figure_record'] == 'absent_legacy' and 'SUBJ:X:02' not in _mig['paper_flags'])
    check('v19_migration_pure', 'paper_flags' not in _legacy and 'record_integrity' not in _legacy['figural_manifests'][0])
    _mig2, _notes2 = annotate_legacy_figure_records(_mig, kind_of=_kind_of)
    check('v19_migration_idempotent', _mig2 == _mig and _notes2 == [])
    check('v19_migration_notes_name_each', len(_notes) == 3 and any('absent_legacy' in n for n in _notes))
    _mig3, _ = annotate_legacy_figure_records(_legacy)      # no kind_of: '>>' + absent passes only
    check('v19_migration_without_kind_of', _mig3['figural_manifests'][0]['record_integrity'] == {'2': 'legacy_degenerate_reaction'})

    _rc_bad = regcheck(r1['registry'], bp1, N=1, concept_map=mini_cm(), paper_id='MOCK:M01',
                       require_key_commitments=True)
    check('regcheck_keycommit_gate_fails_without_commitments', _rc_bad['ok'] is False
          and 'G-KEYCOMMIT' in _rc_bad['fails'][0])
    _ak3 = {'answers': {'1': 1, '2': 2, '3': 3},
            'concept_map': {k: {'qtype': 'mcq'} for k in ('1', '2', '3')}}
    r_k3 = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='MOCK:M01',
                           batches_completed=3, axis2_window_counts={}, passage_present=False,
                           di_present=False, figural_present=False, concept_map=mini_cm(),
                           answer_key=_ak3)
    _rc_ok = regcheck(r_k3['registry'], bp1, N=1, concept_map=mini_cm(), paper_id='MOCK:M01',
                      require_key_commitments=True)
    check('regcheck_keycommit_gate_passes_with_commitments',
          not any('G-KEYCOMMIT' in f for f in _rc_ok.get('fails', [])))

    # ── v5.58 GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER — birth stamp via the
    #    single writer. A mock is born PENDING/0; a scoped paper is born
    #    DORMANT/scoped_paper (deliverable — gap defect G-4); both are LEGAL states
    #    by pp.DG_LEGAL_STATES; birth carries no bands (schema 2 shape).
    _dg_m = r_k3['registry'].get('difficulty_gate', {}).get('MOCK:M01')
    check('commit_difficulty_gate_mock_born_PENDING',
          bool(_dg_m) and _ppt.dg_state(_dg_m) == ('PENDING', 0) and _ppt.dg_is_legal(_dg_m)
          and _dg_m.get('schema') == _ppt.DG_SCHEMA and 'bands' not in _dg_m)
    r_sc = commit_registry(mini_registry(), mini_pending(), bp1, 1, paper_id='SUBJ:PHYS:01',
                           batches_completed=3, axis2_window_counts={}, passage_present=False,
                           di_present=False, figural_present=False, concept_map=mini_cm(),
                           answer_key=_ak3)
    _dg_s = r_sc['registry'].get('difficulty_gate', {}).get('SUBJ:PHYS:01')
    check('commit_difficulty_gate_scoped_born_DORMANT_deliverable',
          bool(_dg_s) and _ppt.dg_state(_dg_s) == ('DORMANT', 0)
          and _dg_s.get('dormant_reason') == 'scoped_paper'
          and _ppt.dg_deliver_decision(r_sc['registry'], 'SUBJ:PHYS:01', 1, mock=False)['deliver'])
    check('commit_difficulty_gate_absent_without_key',
          'difficulty_gate' not in r1['registry'])

    # ── v1.16 (GAP-2026-11-10) — parity floors, figure proofs, release stamp ────────────────────
    _cmp = {'1': {'organic': True, 'ask_format': 'two_part', 'decisions_author': ['chemoselectivity', 'facial_selectivity'],
                  'representations': ['chair_conformation'],
                  'figures': [{'identity_ok': True, 'vision_ok': True, 'gates_ok': True}]},
            '2': {'organic': True, 'ask_format': 'forward_product', 'decisions_author': ['regioselectivity'],
                  'representations': ['skeletal'], 'figures': [{'identity_ok': True, 'vision_ok': False, 'gates_ok': True}]},
            '3': {'organic': False, 'ask_format': 'forward_product'}}
    _pg = paper_parity_gate(_cmp, {'two_part': 1, 'statement_combination': 1}, {'chair_conformation': 1}, 0.66)
    check('v116_parity_gate_names_shortfalls', _pg['status'] == 'FAIL' and _pg['chain_share'] == 0.5
          and any('statement_combination' in x for x in _pg['short']) and any('decisions' in x for x in _pg['short'])
          and paper_parity_gate(_cmp, {'two_part': 1}, {'chair_conformation': 1}, 0.5)['status'] == 'PASS')
    _fp = paper_figure_proof_gate(_cmp)
    check('v116_figure_proof_gate', _fp['status'] == 'FAIL' and _fp['missing'] == {'2': ['vision_ok']}
          and paper_figure_proof_gate({})['status'] == 'PASS')
    _fm2 = {'questions': {'5': {'image_hashes': ['h5'], 'object_type': 'chemical_structure'}, '6': {'image_hashes': []},
                          '7': {'image_hashes': ['h7'], 'object_type': 'spectrum'}}}
    _cm2 = {'5': {'organic': True}, '6': {'organic': True}, '7': {'organic': False}}
    check('v116_picture_without_proof_record_fails',
          paper_figure_proof_gate(_cm2, _fm2) == {'status': 'FAIL', 'missing': {'5': ['figure_proof_record']}}
          and paper_figure_proof_gate(_cm2)['status'] == 'PASS'
          and paper_figure_proof_gate(_cm2, {'questions': 'bad'})['status'] == 'PASS'
          and paper_figure_proof_gate({'5': {'organic': True, 'figures': [
              {'identity_ok': True, 'vision_ok': True, 'gates_ok': True}]}}, _fm2)['status'] == 'PASS'
          and paper_figure_proof_gate({'5': {'organic': True, 'figures': [
              {'identity_ok': True, 'vision_ok': True, 'gates_ok': True}]}},
              {'questions': {'5': {'image_hashes': ['a', 'b'], 'object_type': 'reaction_scheme'}}})['status'] == 'FAIL'
          and paper_figure_proof_gate({'7': {'organic': True}}, _fm2)['status'] == 'PASS')
    check('v117_nf_fields_carried', set(QINDEX_NF_FIELDS) >= {'mip', 'given_in_stem', 'text_fingerprint'}
          and not (set(QINDEX_NF_FIELDS) & (set(QINDEX_OP_FIELDS) | set(QINDEX_V589_FIELDS))))
    check('v116_op_fields_carried', set(QINDEX_OP_FIELDS) >= {'organic', 'figures', 'key_votes', 'clone_check', 'grades'}
          and not (set(QINDEX_OP_FIELDS) & set(QINDEX_V589_FIELDS)) and bc.OP_RELEASE >= bc.FRAMEWORK_RELEASE_STRICT)
    L = ['Easy', 'Medium', 'Hard']
    import tempfile as _bv_tf, os as _bv_os, json as _bv_js
    # release 2026.11.24 — FG-1 fallback plan, FG-5 pre-review, RP-1 prior skills to reviewers
    with _bv_tf.TemporaryDirectory() as _h:
        _cmf = {'1': {'stem_text': 'The phase diagram of the binary system shows the eutectic point clearly', 'option_texts':
                      ['A only', 'B only', 'both', 'neither'], 'subtopic_id': 'pc.ph', 'qtype': 'mcq', 'concept_note': 'eutectic'},
                '2': {'stem_text': 'Which statement about the lever rule for the same binary system holds', 'option_texts':
                      ['w', 'x', 'y', 'z'], 'subtopic_id': 'pc.ph', 'qtype': 'mcq'}}
        _bv_js.dump({'concept_map': _cmf, 'answers': {'1': 1, '2': 2}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 2}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Medium', '2': 'Medium'}, 'subtopic_by_qnum': {'1': 'pc.ph', '2': 'pc.ph'}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _bv_js.dump({'total_mocks': 2, 'mocks': [{'mock': 1, 'sections': [{'section_name': 'PC', 'q_range': [1, 2],
                     'subtopic_allocations': [{'subtopic_id': 'pc.ph', 'q_count': 2, 'format': 'FIGURAL'}]}]}],
                     'axis_schedule': {'PC': {'status': 'ok', 'axis1_target_per_mock': {'TEXT': 1, 'FIGURAL': 1},
                                              'axis1_target_series': [1, 1], 'axis1_observed_figural': []}}},
                    open(_bv_os.path.join(_h, 'EX_blueprint.json'), 'w'))
        _fp0 = bv_figure_plan_fallback('EX', 1, _h, _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'))))
        _sf1 = bv_batch_step('EX', 1, home=_h, echo=False)
        _bsf = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        check('v124_figure_plan_fallback_and_granted_slot_must_draw',
              _fp0.get('PC', {}).get('granted') == ['1'] and _fp0['PC']['target'] == 1
              and _bsf.get('figure_plan', {}).get('PC', {}).get('granted') == ['1']
              and _sf1['status'] == 'rewrite' and any('G-FIG-MISSING' in x for x in _sf1['lines'])
              and (_bsf['bv'].get('prereview') or {}).get('1') and not (_bsf['bv'].get('prereview') or {}).get('2')
              and bv_figure_plan_fallback('EX', 1, '/nonexistent', {}) == {})
        _cmL = {'1': {'difficulty': 'Medium'}, '2': {'difficulty': 'Hard'}, '3': {'difficulty': 'Medium'}, '4': {'difficulty': 'Easy'}}
        _bsL = {'difficulty_plan_target': {'1': 'Hard', '2': 'Medium', '3': 'Hard', '4': 'Easy'},
                'difficulty_state': {'band_swaps': [{'up': '2', 'from': 'Medium', 'to': 'Hard', 'pair': '1'}]},
                'figure_plan': {'PC': {'target': 2, 'granted': ['4'], 'short': [{'q': None, 'reason': 'capacity', 'n': 1}]}}}
        _ln = bv_r31_lines(_bsL, _cmL)
        check('v124_slot_ledger_swap_and_figure_lines', _ln[0] == 'DIFFICULTY SLOTS: Easy 1/1; Medium 1/1; Hard 1/2 (1 swapped)'
              and 'labels swapped (S1)' in _ln[1] and _ln[2] == 'DIFFICULTY (AMBER): below the planned band — Q3 planned Hard, '
                                                                 'delivered Medium'
              and _ln[3].startswith('FIGURES PC: target 2, delivered 0') and _ln[3].endswith('(AMBER)')
              and bv_r31_lines(None, None) == [])
        _bsS = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        _bsS['shape_plan'] = {'1': 'statement', '2': 'direct', '3': 'statement_combination'}
        _srS = ('=== SECTION: PC ===\nask_form: {"ask_words_p10": 6, "headline_share": 0.0}\n'
                'statement_forms: {"n_dist": {"3": 0.5, "4": 0.5}, "label_style": "A."}\n')
        _pS = bv_s3_plans('EX', 1, _h, _bsS, None, _srS)
        check('v124_s3_plans_figure_stem_form', _pS.get('figure_plan', {}).get('PC', {}).get('granted') == ['1']
              and _pS['stem_form']['ask_form']['PC']['ask_words_p10'] == 6
              and sorted(_pS['stem_form']['n_statements']) == ['1', '3']
              and sorted(_pS['stem_form']['n_statements'].values()) == [3, 4]
              and 'r3_notes' not in _pS and {k: v for k, v in bv_s3_plans(None, None, None, None).items()
                                             if k != 'math_typeset'} == {'figure_plan': {}}
              and bv_s3_plans(None, None, None, None)['math_typeset']['subjects'] == {}
              and bv_s3_plans('EX', 1, _h, _bsS, None, '', blueprint={'mocks': []})['figure_plan'] == {}
              and bv_figure_plan_fallback('EX', 1, _h, dict(_bsS, subtopic_by_qnum={'1': 'other.sub'})) == {})
        check('v124_prior_skills_reach_reviewers', bc.rp_attach_prior([{'q': '2'}, {'q': '1'}], _cmf)
              == [{'q': '2', 'prior_skills': [{'q': '1', 'skill': 'eutectic'}]}, {'q': '1'}]
              and bc.rp_prior_skills(_cmf, '9') == [] and bc.rp_attach_prior(None, None) == [])
    with _bv_tf.TemporaryDirectory() as _h:
        _cmt = {'1': {'stem_text': 'Find the dipole moment of molecule one', 'option_texts': ['1', '2', '3', '4'], 'subtopic_id': 'A.b',
                      'qtype': 'mcq'},
                '2': {'stem_text': 'Name the point group of the second molecule', 'option_texts': ['C2v', 'D3h', 'Td', 'Oh'],
                      'subtopic_id': 'C.d', 'qtype': 'mcq'}}
        _bv_js.dump({'concept_map': _cmt, 'answers': {'1': 2, '2': 3}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 2}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Hard', '2': 'Easy'}}, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        s1 = bv_batch_step('EX', 1, home=_h, echo=False)
        _ret = []
        for _d in s1['jobs']:
            _pk = _bv_js.load(open(_bv_os.path.join(_d, 'packet.json')))
            _items = {r['q']: {'band': {'1': 'Hard', '2': 'Easy'}[r['q']], 'decisions': 2, 'rationale': 'r',
                               'answer': {'1': 2, '2': 3}[r['q']], 'confidence': 'high', 'assumptions': []}
                      for r in _pk['items']}
            _bv_js.dump({'items': _items}, open(_bv_os.path.join(_d, 'result.json'), 'w'))
            _ret.append(_d + ' REVIEW DONE')
        open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'w').write('\n'.join(_ret) + '\n')
        _pk1 = _bv_js.load(open(_bv_os.path.join(s1['jobs'][0], 'packet.json')))
        s2 = bv_batch_step('EX', 1, home=_h, echo=False)
        _kdt = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
        check('bv_batch_step_end_to_end', s1['status'] == 'jobs_out' and len(s1['jobs']) == 3
              and [p.rsplit('/', 1)[-1] for p in s1['jobs']] == ['reviewer_1', 'reviewer_2', 'reviewer_3']
              and [r['q'] for r in _pk1['items']] == ['1', '2'] and 'Hard' not in str([r['item'] for r in _pk1['items']])
              and s2['status'] == 'done' and s2['settled'] == ['1', '2'] and s2['open'] == [] and s2['jobs'] == []
              and bc.verify_difficulty_label(_kdt['concept_map']['1'], L, strict=True) == (True, 'Hard', 'measured_majority')
              and _kdt['concept_map']['2']['difficulty'] == 'Easy' and 'bc.manifest_hash' not in _kdt['concept_map']['1']
              and all(_bv_os.path.exists(_bv_os.path.join(d, 'JOB_BRIEF.txt')) for d in s1['jobs']))
        s3 = bv_batch_step('EX', 1, home=_h, echo=False)
        check('bv_batch_step_idempotent_when_done', s3['status'] == 'done' and s3['jobs'] == [] and s3['settled'] == ['1', '2'])
    # release 2026.11.27 (GAP-2026-11-21) — end to end through bv_batch_step: (A) a job carrying a non-chemistry problem
    # figure of a strict-subject item gets BV_BRIEF_REVIEWER_R3_FIG, the same paper WITHOUT the plan (a paper begun earlier)
    # gets BV_BRIEF_REVIEWER_R3 byte for byte; (B) maths written as text is sent back BC_PREREVIEW_TRIES times, then the
    # item is reviewed as it stands, settles and carries the AMBER line (never a stop, never a loop)
    _p1_plan = bc.math_typeset_plan(
        'MATH_TYPESET_PROFILE: {"schema":1,"section":"Mathematical Sciences","n":300,"omml_q_share":0.84,'
        '"omml_per_q":3.7,"display_per_q":0.33,"arms":["A1","A2","A3","A4","A5","A6"],"mode":"strict"}\n',
        {'subtopic_list': [{'subtopic_id': 'ms.a', 'section': 'Mathematical Sciences'}]})

    def _p1_paper(_h, _cm, with_plan):
        _bv_js.dump({'concept_map': _cm, 'answers': {q: 1 for q in _cm}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bs = {'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': len(_cm)}], 'current_batch': 1, 'difficulty_labels': L,
               'difficulty_plan_target': {q: 'Easy' for q in _cm}}
        if with_plan:
            _bs['math_typeset'] = _p1_plan
        _bv_js.dump(_bs, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))

    def _p1_answer(_h, s, ans):
        _ret = []
        for _d in s['jobs']:
            _pk = _bv_js.load(open(_bv_os.path.join(_d, 'packet.json')))
            _bv_js.dump({'items': {r['q']: {'band': 'Easy', 'decisions': 1, 'rationale': 'r', 'answer': ans,
                                            'confidence': 'high', 'assumptions': []} for r in _pk['items']}},
                        open(_bv_os.path.join(_d, 'result.json'), 'w'))
            _ret.append(_d + ' REVIEW DONE')
        open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'w').write('\n'.join(_ret) + '\n')
    _cmF = {'1': {'stem_text': 'A bead of mass m moves on the wire as shown. Find the period.', 'option_texts': ['1', '2', '3', '4'],
                  'subtopic_id': 'ms.a', 'qtype': 'mcq', 'figure_files': ['q1_problem.png']}}
    _briefs = {}
    for _wp in (True, False):
        with _bv_tf.TemporaryDirectory() as _h:
            _p1_paper(_h, _cmF, _wp)
            _bv_js.dump({'class': 'schematic', 'role': 'problem', 'text_labels': ['m', '$\\theta$']},
                        open(_bv_os.path.join(_h, 'q1_problem.figspec.json'), 'w'))
            _sF = bv_batch_step('EX', 1, home=_h, echo=False)
            _briefs[_wp] = [open(_bv_os.path.join(d, 'JOB_BRIEF.txt')).read().replace(d, '<JOB_DIR>') for d in _sF['jobs']]
    check('p1_brief_fig_variant_end_to_end', _briefs[True] and _briefs[False]
          and all(b == bc.BV_BRIEF_REVIEWER_R3_FIG for b in _briefs[True])
          and all(b == bc.BV_BRIEF_REVIEWER_R3 for b in _briefs[False]))
    with _bv_tf.TemporaryDirectory() as _h:
        _p1_paper(_h, {'1': {'stem_text': 'If ω² > g a⁻¹, which value of x holds?', 'option_texts': ['1', '2', '3', '4'],
                             'subtopic_id': 'ms.a', 'qtype': 'mcq'}}, True)
        _sT = [bv_batch_step('EX', 1, home=_h, echo=False) for _ in range(3)]
        _p1_answer(_h, _sT[-1], 1)
        _sD = bv_batch_step('EX', 1, home=_h, echo=False)
        _bsT = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        check('p1_math_typeset_soft_send_back_then_amber', [x['status'] for x in _sT] == ['rewrite', 'rewrite', 'jobs_out']
              and any('G-MATH-TYPESET' in ln for ln in (_sT[0].get('lines') or []))
              and _sD['status'] == 'done' and _sD['settled'] == ['1']
              and ['AMBER', 'Q1: maths written as text (G-MATH-TYPESET A1)'] in [list(x) for x in
                                                                                   (_bsT.get('bc_footer') or {}).get('1') or []])
    # the thin core's embedded copies of the compiler's delimiters / tables never drift from t3_mathcomp (byte-locked
    # §S3-5b), and the chemistry types the plan freezes come from figure_types (both routed with this engine)
    try:
        import t3_mathcomp as _t3k
        _t3ok = (bc.P1_MATH_OPEN == _t3k.MATH_OPEN and bc.P1_MATH_CLOSE == _t3k.MATH_CLOSE
                 and bc.P1_SYMBOLS == dict(_t3k._T3_SYMBOLS)
                 and bc.P1_NARY == {k: v[0] for k, v in _t3k._T3_NARY.items()}
                 and set(bc.P1_MATRIX_ENVS) == set(_t3k._T3_MATRIX) and set(bc.P1_NOOP) == set(_t3k._T3_NOOP)
                 and set(bc.P1_STYLED) == set(_t3k._T3_STYLED))
    except Exception:                                   # noqa: BLE001
        _t3ok = False
    check('p1_t3_drift_lock', _t3ok)
    _ctk = bv_p1_chem_types()
    check('p1_chem_types_from_figure_types', {'chemical_structure', 'reaction_scheme', 'newman_projection',
                                              'nmr_spectrum', 'molecular_orbital_diagram'} <= set(_ctk)
          and not {'bar_chart', 'line_graph', 'pie_chart'} & set(_ctk) and _ctk == sorted(_ctk)
          and bc.fig_need('x', [], {'object_type': 'nmr_spectrum', 'class': 'data_series', 'text_labels': ['a']},
                          _ctk)[0] == 'N/A')
    # v1.23 (C3) — the rung-3 TEXT fallback has no figure record; a picture on it is refused at STEP A3
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'questions': {'4': {'object_type': 'chemical_structure'}, '5': {'object_type': 'spectrum'}}},
                    open(_bv_os.path.join(_h, 'EX_fig_manifest.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 5}], 'current_batch': 1},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _c1 = bc_fallback_clear_figure('EX', 1, 4, home=_h)
        _c2 = bc_fallback_clear_figure('EX', 1, '4', home=_h)
        _fmx = _bv_js.load(open(_bv_os.path.join(_h, 'EX_fig_manifest.json')))
        _bsx = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        _mem = {}
        _c3 = bc_fallback_clear_figure('EX', 1, '5', home=_h, bs=_mem)
        _bsx2 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        check('c3_fallback_clear_figure', _c1 is True and _c2 is False and list(_fmx['questions']) == ['5']
              and _bsx['bv']['fallback_cleared'] == ['4'] and _c3 is True and _mem['bv']['fallback_cleared'] == ['5']
              and _bsx2['bv']['fallback_cleared'] == ['4']
              and bc_fallback_clear_figure('EX', 1, '9', home=_bv_os.path.join(_h, 'missing')) is False)
        # STEP A3: a settled rung-3 question with a picture is refused; without one it binds and its record is cleared
        _bv_js.dump({'questions': {'1': {'object_type': 'chemical_structure'}, '2': {'object_type': 'chemical_structure'}}},
                    open(_bv_os.path.join(_h, 'EX_fig_manifest.json'), 'w'))
        _sv3 = {r: {'answer': 2, 'confidence': 'high', 'single_answer': 'yes', 'leak_or_paraphrase': 'none',
                    'distractor_existence_and_class': 'ok', 'consistency_and_names': 'ok', 'selectivity_basis': 'clean'}
                for r in bc.BV_ROLES_SOLVE}
        _ents = {}
        for _qq, _ff in (('1', []), ('2', ['/x/q2.png'])):
            _e3 = {'stem_text': f'Text fallback question {_qq} about acidity order', 'option_texts': ['a', 'b', 'c', 'd'],
                   'qtype': 'mcq', 'figure_files': _ff}
            _e3 = _bc_render_shas(_e3)
            _e3['bv'] = {'rule': bc.BC_RULE, 'state': 'settled', 'rung': 3, 'solvers': _sv3,
                         'key': {'certified_by': 'unanimous', 'decided_key': 2},
                         'content_sha': _bc_entry_sha(_bc_render_shas(_e3))}
            _e3['bv_state'] = 'settled'
            _ents[_qq] = _e3
        _bv_js.dump({'concept_map': _ents, 'answers': {'1': 2, '2': 2}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 2}], 'current_batch': 1,
                     'bv': {'items': {q: v['bv'] for q, v in _ents.items()}}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _bv_js.dump({'1': 'h1', '2': 'h2'}, open(_bv_os.path.join(_h, 'ih.json'), 'w'))
        _bb = bc_bind_batch('EX', 1, _bv_os.path.join(_h, 'ih.json'), home=_h, echo=False)
        _fmy = _bv_js.load(open(_bv_os.path.join(_h, 'EX_fig_manifest.json')))
        check('c3_bind_refuses_picture_on_fallback_and_clears_record', _bb['bound'] == ['1']
              and 'rung-3 TEXT fallback' in _bb['refused'].get('2', '') and list(_fmy['questions']) == ['2']
              and any('leftover figure record was removed' in x for x in _bb['lines']))
        # an R10 family-engine rung-3 item IS a figure: never refused, its record never cleared
        _bv_js.dump({'questions': {'2': {'object_type': 'dice'}}}, open(_bv_os.path.join(_h, 'EX_fig_manifest.json'), 'w'))
        _orig_fi = globals()['bc_figure_intrinsic']
        globals()['bc_figure_intrinsic'] = lambda _b, _q: (True, True)
        try:
            _bb2 = bc_bind_batch('EX', 1, _bv_os.path.join(_h, 'ih.json'), home=_h, echo=False)
        finally:
            globals()['bc_figure_intrinsic'] = _orig_fi
        check('c3_family_engine_item_keeps_its_figure', sorted(_bb2['bound'], key=int) == ['1', '2']
              and list(_bv_js.load(open(_bv_os.path.join(_h, 'EX_fig_manifest.json')))['questions']) == ['2'])
        # the kept record comes back when R5b restores an earlier figure version
        _bv_js.dump({'questions': {'3': {'object_type': 'chemical_structure', 'image_hashes': ['h3']}}},
                    open(_bv_os.path.join(_h, 'EX_fig_manifest.json'), 'w'))
        _memr = {}
        _cl = bc_fallback_clear_figure('EX', 1, '3', home=_h, bs=_memr)
        _after_clear = list(_bv_js.load(open(_bv_os.path.join(_h, 'EX_fig_manifest.json')))['questions'])
        _rb1 = bc_fallback_restore_figure('EX', 1, '3', home=_h, bs=_memr)
        _rb2 = bc_fallback_restore_figure('EX', 1, '3', home=_h, bs=_memr)
        _fmr = _bv_js.load(open(_bv_os.path.join(_h, 'EX_fig_manifest.json')))
        check('c3_restore_puts_the_figure_record_back', _cl and _after_clear == [] and _rb1 is True and _rb2 is False
              and _fmr['questions'] == {'3': {'object_type': 'chemical_structure', 'image_hashes': ['h3']}}
              and _memr['bv']['fallback_fig_records']['3']['image_hashes'] == ['h3']
              and bc_fallback_restore_figure('EX', 1, '8', home=_h, bs=_memr) is False)
    # v1.18 — the ask count is per content: a rewrite clears it, so the regrade of the new text can be re-asked
    with _bv_tf.TemporaryDirectory() as _h:
        _cmt = {'1': {'stem_text': 'Find the dipole moment of molecule one', 'option_texts': ['1', '2', '3', '4'],
                      'subtopic_id': 'A.b', 'qtype': 'mcq'}}
        _bv_js.dump({'concept_map': _cmt, 'answers': {'1': 2}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Hard'}}, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))

        def _answer_all(_jobs, _band):
            _ret = []
            for _d in _jobs:
                _pk = _bv_js.load(open(_bv_os.path.join(_d, 'packet.json')))
                _bv_js.dump({'items': {r['q']: {'band': _band, 'decisions': 1, 'rationale': 'r', 'answer': 2,
                                                'confidence': 'high', 'assumptions': []} for r in _pk['items']}},
                            open(_bv_os.path.join(_d, 'result.json'), 'w'))
                _ret.append(_d + ' REVIEW DONE')
            open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'w').write('\n'.join(_ret) + '\n')
        r1 = bv_batch_step('EX', 1, home=_h, echo=False)
        _answer_all(r1['jobs'], 'Easy')
        r2 = bv_batch_step('EX', 1, home=_h, echo=False)
        _bsr = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        _asked_after_rw = ((_bsr.get('difficulty_state') or {}).get('bv') or _bsr.get('bv') or {}).get('asked') or {}
        _kdr = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
        _kdr['concept_map']['1']['stem_text'] = 'Find the dipole moment of molecule one after a ring flip and a reduction'
        _bv_js.dump(_kdr, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        r3 = bv_batch_step('EX', 1, home=_h, echo=False)
        _bs3 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        check('bv_rewrite_clears_ask_count', len(r1['jobs']) == 3 and r2['status'] == 'rewrite' and r2['rewrite'] == ['1']
              and '1' not in _asked_after_rw)
        # v1.21 (G-06, t_carry_empty): the rewritten text is re-graded IN ITS OWN BATCH — its next round is issued at
        # once with only that question; nothing is carried to the next batch or to Final Assembly
        check('bv_rewrite_is_measured_in_its_own_batch', r3['status'] == 'jobs_out' and len(r3['jobs']) == 3
              and all('/b1/r2/' in d for d in r3['jobs']) and r3['pending'] == [] and _bs3['bv_carry'] == [])
        _answer_all(r3['jobs'], 'Hard')
        r4 = bv_batch_step('EX', 1, home=_h, echo=False)
        check('t_carry_empty_at_done', r4['status'] == 'done' and r4['settled'] == ['1'] and r4['pending'] == []
              and _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))['bv_carry'] == [])
        # GAP-2026-11-14-FINAL-COUNT-INDEX (hotfix 48c6502, kept): by Final Assembly S4-8a has moved current_batch PAST
        # the plan — the final round must not index batch_plan with it (the pre-fix engine raised IndexError here)
        _bs4 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        _bs4['current_batch'] = len(_bs4.get('batch_plan') or []) + 1
        _bv_js.dump(_bs4, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        r5 = bv_batch_step('EX', 1, home=_h, echo=False, final=True)
        # v1.22 (BATCH-COMPLETE): the settlement batch 'S' of a migrating paper has nothing to do on a settled paper
        check('bv_final_round_is_a_check_when_every_batch_settled', r5['status'] == 'done' and r5['jobs'] == []
              and r5['settled'] == [] and 'DONE' in r5['lines'][-1] and not _bv_os.path.isdir(_bv_os.path.join(_h, 'EX_M1_bv', 'bS')))
        # v1.22 STEP A3 guard (measured on the CSIR NET Chemical Sciences incident paper, 40 real blocks: 40 matched, 40
        # unrelated stems refused): tolerant of rendering, drawn options checked on the stem only, text options in order
        _blk_t = 'Q.6 The number of optically active stereoisomers possible for the constitution shown is 1. 0 2. 1 3. 2 4. 4'
        _blk_f = 'Q.1 Identify the major product P of the following two-step sequence. 1. 2. 3. 4.'
        _blk_o = 'Q.2 Which reagent reduces the ketone 1. NaBH4 2. KMnO4 3. PCC 4. O3'
        check('bc_block_contains_tolerant_and_ordered',
              _bc_block_contains(_blk_t, {'stem_text': 'The number of optically-active stereoisomers possible for the '
                                                       'constitution shown is', 'option_texts': ['0', '1', '2', '4']})
              and _bc_block_contains(_blk_f, {'stem_text': 'Identify the major product P of the following two-step sequence.',
                                              'option_texts': ['CC(O)C', 'CCO', 'C=C', 'CC'], 'figure_files': ['q1.png']})
              and not _bc_block_contains(_blk_f, {'stem_text': 'Calculate the boiling point elevation of a sucrose solution',
                                                  'figure_files': ['q1.png']})
              and _bc_block_contains(_blk_o, {'stem_text': 'Which reagent reduces the ketone',
                                              'option_texts': ['NaBH4', 'KMnO4', 'PCC', 'O3']})
              and not _bc_block_contains(_blk_o, {'stem_text': 'Which reagent reduces the ketone',
                                                  'option_texts': ['KMnO4', 'NaBH4', 'PCC', 'O3']})
              and _bc_block_contains('anything', {'stem_text': ''}))
        # v1.22 S13-1 ASSEMBLE: the final docx is PROVEN a byte copy — a copy that differs is never reported ok
        import shutil as _bv_sh
        _src_a, _dst_a = _bv_os.path.join(_h, 'cum.docx'), _bv_os.path.join(_h, 'final.docx')
        open(_src_a, 'wb').write(b'PK cumulative')
        _ok_copy = assemble_final_docx(_src_a, _dst_a)
        _real_cf = _bv_sh.copyfile
        try:
            _bv_sh.copyfile = lambda a, b: open(b, 'wb').write(b'PK re-rendered')
            _bad_copy = assemble_final_docx(_src_a, _dst_a)
        finally:
            _bv_sh.copyfile = _real_cf
        check('assemble_final_docx_proves_the_byte_copy', _ok_copy['ok'] and not _bad_copy['ok']
              and 'differs' in _bad_copy['why'] and not assemble_final_docx(_bv_os.path.join(_h, 'missing.docx'), _dst_a)['ok'])
        # v1.22: 'defer' (the 2026.11.14 carry) is accepted for old callers and ignored — nothing is ever carried
        import inspect as _bv_insp
        _sig = _bv_insp.signature(bv_batch_step).parameters
        check('bv_defer_is_opt_in_only', _sig['defer'].default is False and _sig['final'].default is False
              and _sig['terminal'].default is None)
    # GAP-2026-11-14-FINAL-COUNT-INDEX x v1.21 INFRA-CARRY: the last batch's INFRA-CARRY question is measured by the final
    # round (S13-1B) while current_batch is already past the plan — jobs go out at once, never an IndexError
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'concept_map': {'1': {'stem_text': 'Find the dipole moment of molecule one', 'option_texts': ['1', '2'],
                                           'subtopic_id': 'A.b', 'qtype': 'mcq'}}, 'answers': {'1': 2}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 2, 'bv_carry': ['1'],
                     'difficulty_labels': L, 'difficulty_plan_target': {'1': 'Hard'}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        try:
            _ri = bv_batch_step('EX', 1, home=_h, echo=False, final=True)
        except IndexError:
            _ri = {'status': 'IndexError', 'jobs': []}
        check('gap_2026_11_14_final_count_index_infra_carry', _ri['status'] == 'jobs_out' and len(_ri['jobs']) == 3
              and all('/bS/' in d for d in _ri['jobs']))
    # v1.20 (S0-BV BV-13) — a question carried from batch 1 rides in batch 2's FIRST reviewer round (no extra round)
    with _bv_tf.TemporaryDirectory() as _h:
        _cm2 = {'1': {'stem_text': 'Find the dipole moment of molecule one', 'option_texts': ['1', '2'], 'subtopic_id': 'A.b', 'qtype': 'mcq'},
                '2': {'stem_text': 'Name the point group of the second molecule here', 'option_texts': ['C2v', 'D3h'],
                      'subtopic_id': 'C.d', 'qtype': 'mcq'}}
        _bv_js.dump({'concept_map': _cm2, 'answers': {'1': 2, '2': 1}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}, {'batch_id': 2, 'q_start': 2, 'q_end': 2}],
                     'current_batch': 2, 'difficulty_labels': L, 'difficulty_plan_target': {'1': 'Hard', '2': 'Easy'},
                     'bv_carry': ['1']}, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _b2 = bv_batch_step('EX', 1, home=_h, echo=False)
        _p2 = _bv_js.load(open(_bv_os.path.join(_b2['jobs'][0], 'packet.json')))
        check('bv_carried_question_rides_in_the_next_batch_first_round', _b2['status'] == 'jobs_out' and len(_b2['jobs']) == 3
              and [r['q'] for r in _p2['items']] == ['1', '2'])
    # v1.20 — at FINAL a failed reviewer role is asked again up to the round limit (nothing can be carried any more)
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'concept_map': {'1': {'stem_text': 'Find the dipole moment of molecule one', 'option_texts': ['1', '2'],
                                           'subtopic_id': 'A.b', 'qtype': 'mcq'}}, 'answers': {'1': 2}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Hard'}, 'bv_carry': ['1']}, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _fs = []
        for _i in range(3):
            _fr = bv_batch_step('EX', 1, home=_h, echo=False, final=True)
            _fs.append(_fr['status'])
            if _fr['jobs']:
                open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'a').write(
                    '\n'.join(d + ' REVIEW FAILED x' for d in _fr['jobs']) + '\n')
        check('bv_final_reasks_a_failed_role_beyond_two', _fs == ['jobs_out', 'jobs_out', 'jobs_out'])
    # v1.22 (LAW-BC-9): a reviewer that returns nothing is re-asked (the 2nd and 3rd ask on a switched model); after
    # bc.BC_ROLE_ASKS asks the batch reports NO-MODEL with its state saved — never a carry, never an exception — and
    # the next run (the resume) asks again from a clean count
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'concept_map': {'1': {'stem_text': 'Find the dipole moment of molecule one', 'option_texts': ['1', '2'],
                                           'subtopic_id': 'A.b', 'qtype': 'mcq'}}, 'answers': {'1': 2}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Hard'}}, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _seen, _raised, _last, _dirs = [], None, None, []
        try:
            for _i in range(bc.BC_ROLE_ASKS + 2):
                _last = bv_batch_step('EX', 1, home=_h, echo=False)
                _seen.append(_last['status'])
                _dirs.append(list(_last['jobs']))
                if _last['jobs']:
                    open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'a').write(
                        '\n'.join(d + ' REVIEW FAILED x' for d in _last['jobs']) + '\n')
                if _last['status'] != 'jobs_out':
                    break
        except Exception as _ex:                                   # noqa: BLE001
            _raised = _ex
        _bsn = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        check('bv_no_reviewer_never_a_stop', _raised is None and _last is not None and _last['status'] == 'no_model'
              and _seen.count('jobs_out') == bc.BC_ROLE_ASKS and _last['pending'] == [] and _bsn['bv_carry'] == []
              and not any('_switch' in d for d in _dirs[0]) and all(d.endswith('_switch') for d in _dirs[1] + _dirs[2])
              and 'NO-MODEL [HS:ENV]' in _last['lines'][-1] and '1' in _last['no_model'])
        _res = bv_batch_step('EX', 1, home=_h, echo=False)
        check('bv_max_rounds_carries_to_the_next_batch', _res['status'] == 'jobs_out' and _res['pending'] == []
              and len(_res['jobs']) == 3)
        # at the round cap the question is decided with what exists (R11) — NO-MODEL here (no result at all), not a carry
        _bsx = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        _bsx['bv'].update({'round': bc.BV_MAX_ROUNDS, 'asked': {}, 'status': 'jobs_out', 'jobs': []})
        _bv_js.dump(_bsx, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        try:
            _mf = bv_batch_step('EX', 1, home=_h, echo=False)
        except Exception as _ex:                                   # noqa: BLE001
            _mf = {'status': f'raised {_ex}', 'jobs': ['x']}
        check('bv_no_model_is_the_role_asks_not_an_engine_defect', 'after 3 asks' in _last['lines'][-1]
              and not any(isinstance(_x, dict) and _x.get('kind') == 'bc_not_settled_at_done' for _x in (_bsn.get('p0_incidents') or [])))
        check('bv_final_max_rounds_carries_unlabelled_never_a_stop', _mf['status'] == 'no_model' and _mf['jobs'] == []
              and _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))['bv'].get('unmeasured') == [])
        # LAW-BC-9 RESUME at the cap (600-paper fuzz, invariant I8): the next step re-asks in an infrastructure round
        # (folder r<k>i<j>, the quality budget untouched) and the batch completes — a NO-MODEL is never a dead end
        _rz = bv_batch_step('EX', 1, home=_h, echo=False)
        for _d in _rz['jobs']:
            _pkz = _bv_js.load(open(_bv_os.path.join(_d, 'packet.json')))
            _bv_js.dump({'items': {r['q']: {'band': 'Hard', 'decisions': 2, 'rationale': 'r', 'answer': 2,
                                            'confidence': 'high', 'assumptions': []} for r in _pkz['items']}},
                        open(_bv_os.path.join(_d, 'result.json'), 'w'))
        open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'a').write('\n'.join(d + ' REVIEW DONE' for d in _rz['jobs']) + '\n')
        _rz2 = bv_batch_step('EX', 1, home=_h, echo=False)
        _bsz = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
        check('bv_no_model_at_the_cap_resumes_and_completes', _rz['status'] == 'jobs_out' and all('/r' + str(bc.BV_MAX_ROUNDS) + 'i1/' in d for d in _rz['jobs'])
              and _rz2['status'] == 'done' and _bsz['bv']['round'] == bc.BV_MAX_ROUNDS and _bsz['bv'].get('infra_rounds') == 1)
    # v1.21 (G-11, t_reviewer_jobs_split): 10 questions at 5 per job -> 6 jobs; every question in exactly 3 distinct
    # reviewer contexts (k = 1..3); a linked group is never split; a re-ask goes to a '_switch' folder (another model)
    with _bv_tf.TemporaryDirectory() as _h:
        _cms = {str(q): {'stem_text': f'Compute quantity number {q} of the sample system here', 'option_texts': ['1', '2', '3', '4'],
                         'subtopic_id': 'A.b', 'qtype': 'mcq'} for q in range(1, 11)}
        for _q in ('4', '5', '6'):
            _cms[_q]['stimulus_group_id'] = 'G1'
        _bv_js.dump({'concept_map': _cms, 'answers': {str(q): 1 for q in range(1, 11)}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 10}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {str(q): 'Medium' for q in range(1, 11)}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _sj = bv_batch_step('EX', 1, home=_h, echo=False)
        _jq = {}
        for _d in _sj['jobs']:
            for _r in _bv_js.load(open(_bv_os.path.join(_d, 'packet.json')))['items']:
                _jq.setdefault(_r['q'], []).append(_d.rsplit('/', 1)[-1].split('_p')[0])
        _grp = [[_r['q'] for _r in _bv_js.load(open(_bv_os.path.join(_d, 'packet.json')))['items']] for _d in _sj['jobs']]
        # v1.23 (P1): the 3 chunks today's split makes (9 jobs) are rebalanced to 2 per reviewer — one wave of 6
        check('t_reviewer_jobs_split', len(_sj['jobs']) == 3 * len(bc.bv_job_chunks_n([str(q) for q in range(1, 11)], _cms, 5,
                                                                                   bc.bv_round_job_caps(6, 0)))
              and len(_sj['jobs']) == 6 and len(bc.bv_job_chunks([str(q) for q in range(1, 11)], _cms, 5)) == 3
              and len(bc.bv_job_chunks([str(q) for q in range(1, 11)], {}, 5)) == 2
              and all(sorted(v) == ['reviewer_1', 'reviewer_2', 'reviewer_3'] for v in _jq.values()) and len(_jq) == 10
              and all(({'4', '5', '6'} <= set(g)) or not ({'4', '5', '6'} & set(g)) for g in _grp))
        open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'w').write(
            '\n'.join(d + ' REVIEW FAILED quota' for d in _sj['jobs']) + '\n')
        _sw = bv_batch_step('EX', 1, home=_h, echo=False)
        check('bv_reask_goes_to_a_switched_model', _sw['status'] == 'jobs_out' and _sw['jobs']
              and all(d.endswith('_switch') for d in _sw['jobs']) and all('/b1/r2/' in d for d in _sw['jobs']))
    # v1.23 (P3) G-SELFCOUNT: a self-count miss goes back to the author before any reviewer is paid — at most
    # bc.BC_SELFCOUNT_TRIES times per rung, then the text is reviewed anyway; missing counts are only reported
    _HARD = {'facets': ['C-COMPUTATIONAL'], 'moves': ['m1', 'm2', 'm3', 'm4'], 'principles': ['p1', 'p2']}
    _EASY = {'facets': ['C-FACTUAL'], 'moves': ['m1'], 'principles': ['p1']}
    for _fix in (False, True):
        with _bv_tf.TemporaryDirectory() as _h:
            _cmc = {'1': {'stem_text': 'Compute the first quantity of the sample', 'option_texts': ['1', '2', '3', '4'],
                          'subtopic_id': 'A.b', 'qtype': 'mcq', 'author_counts': _HARD},
                    '2': {'stem_text': 'Compute the second quantity of the sample', 'option_texts': ['1', '2', '3', '4'],
                          'subtopic_id': 'A.b', 'qtype': 'mcq', 'author_counts': _EASY},
                    '3': {'stem_text': 'Compute the third quantity of the sample', 'option_texts': ['1', '2', '3', '4'],
                          'subtopic_id': 'A.b', 'qtype': 'mcq'}}
            _bv_js.dump({'concept_map': _cmc, 'answers': {'1': 1, '2': 1, '3': 1}},
                        open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
            _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 3}], 'current_batch': 1,
                         'difficulty_labels': L, 'difficulty_plan_target': {'1': 'Hard', '2': 'Hard', '3': 'Hard'},
                         'difficulty_mode': bc.R3_MODE_LEGACY},       # release 2026.11.20 rule: the self-count applies
                        open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
            _c1 = bv_batch_step('EX', 1, home=_h, echo=False)
            _bsc = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
            _first = (_c1['status'] == 'rewrite' and _c1['jobs'] == [] and _bsc['bv']['round'] == 0
                      and any('SELF-COUNT Q2 (try 1 of 2)' in x for x in _c1['lines'])
                      and any("author_counts not recorded for ['3']" in x for x in _c1['lines'])
                      and not any('SELF-COUNT Q1' in x or 'SELF-COUNT Q3' in x for x in _c1['lines']))
            if _fix:
                _kdc = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
                _kdc['concept_map']['2']['author_counts'] = _HARD
                _bv_js.dump(_kdc, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
                _c2 = bv_batch_step('EX', 1, home=_h, echo=False)
                check('p3_selfcount_fixed_then_reviewed_in_round_1', _first and _c2['status'] == 'jobs_out'
                      and all('/b1/r1/' in d for d in _c2['jobs'])
                      and {r['q'] for d in _c2['jobs'] for r in _bv_js.load(open(_bv_os.path.join(d, 'packet.json')))['items']}
                      == {'1', '2', '3'}
                      and not any('author_counts' in str(r['item']) for d in _c2['jobs']
                                  for r in _bv_js.load(open(_bv_os.path.join(d, 'packet.json')))['items']))
            else:
                _c2 = bv_batch_step('EX', 1, home=_h, echo=False)
                _c3 = bv_batch_step('EX', 1, home=_h, echo=False)
                check('p3_selfcount_two_tries_then_reviewed_never_a_loop', _first and _c2['status'] == 'rewrite'
                      and any('SELF-COUNT Q2 (try 2 of 2)' in x for x in _c2['lines'])
                      and _c3['status'] == 'jobs_out' and all('/b1/r1/' in d for d in _c3['jobs'])
                      and '2' in {r['q'] for d in _c3['jobs']
                                  for r in _bv_js.load(open(_bv_os.path.join(d, 'packet.json')))['items']})
    # v1.24 (D1-D3) STEP A2 PRE-REVIEW: a packet gap / auditor finding goes back to the author before any reviewer is
    # paid — at most bc.BC_PREREVIEW_TRIES times per rung, then the text is reviewed anyway (never a loop)
    for _fixp in (False, True):
        with _bv_tf.TemporaryDirectory() as _h:
            _cmp = {'1': {'stem_text': 'Match List-I with List-II for the sample', 'option_texts': ['1', '2', '3', '4'],
                          'subtopic_id': 'A.b', 'qtype': 'mcq', 'author_counts': _HARD},
                    '2': {'stem_text': 'Compute the second quantity of the sample', 'option_texts': ['1', '2', '3', '4'],
                          'subtopic_id': 'A.b', 'qtype': 'mcq', 'author_counts': _HARD}}
            _bv_js.dump({'concept_map': _cmp, 'answers': {'1': 1, '2': 1}},
                        open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
            _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 2}], 'current_batch': 1,
                         'difficulty_labels': L, 'difficulty_plan_target': {'1': 'Hard', '2': 'Hard'},
                         'stimulus_groups': {'g1': {'qnums': [2], 'stimulus': 'SHARED PASSAGE TEXT'}}},
                        open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
            _bv_js.dump({'item_findings': [{'q': '2', 'gate': 'G-STEM', 'finding': 'stem cue gives the answer'}],
                         'amber_findings': []}, open(_bv_os.path.join(_h, 'EX_M1_batch_findings.json'), 'w'))
            _p1 = bv_batch_step('EX', 1, home=_h, echo=False)
            _firstp = (_p1['status'] == 'rewrite' and _p1['jobs'] == []
                       and any('PRE-REVIEW Q1 (try 1 of 2)' in x and 'list_columns' in x for x in _p1['lines'])
                       and any('PRE-REVIEW Q2 (try 1 of 2)' in x and 'G-STEM' in x for x in _p1['lines'])
                       and not _bv_os.path.isdir(_bv_os.path.join(_h, 'EX_M1_bv', 'b1', 'r1')))
            if _fixp:
                _kdp = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
                _kdp['concept_map']['1']['list_columns'] = [['a', 'b', 'c', 'd'], ['p', 'q', 'r', 's']]
                _bv_js.dump(_kdp, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
                _bv_js.dump({'item_findings': [], 'amber_findings': []},
                            open(_bv_os.path.join(_h, 'EX_M1_batch_findings.json'), 'w'))
                _p2 = bv_batch_step('EX', 1, home=_h, echo=False)
                _rows_p = [r for d in _p2['jobs'] for r in _bv_js.load(open(_bv_os.path.join(d, 'packet.json')))['items']]
                check('v124_set_member_packet_carries_its_stimulus',
                      _rows_p and all(r['item'].get('stimulus_text') == 'SHARED PASSAGE TEXT' for r in _rows_p if r['q'] == '2')
                      and any(r['q'] == '2' for r in _rows_p)
                      and all('stimulus_text' not in r['item'] for r in _rows_p if r['q'] == '1'))
                check('v124_prereview_fixed_then_reviewed', _firstp and _p2['status'] == 'jobs_out' and _p2['jobs']
                      and all('/b1/r1/' in d for d in _p2['jobs'])
                      and not any('PRE-REVIEW' in x for x in _p2['lines']))
            else:
                _p2 = bv_batch_step('EX', 1, home=_h, echo=False)
                _p3 = bv_batch_step('EX', 1, home=_h, echo=False)
                check('v124_prereview_two_tries_then_reviewed_never_a_loop', _firstp and _p2['status'] == 'rewrite'
                      and any('PRE-REVIEW Q1 (try 2 of 2)' in x for x in _p2['lines'])
                      and _p3['status'] == 'jobs_out' and all('/b1/r1/' in d for d in _p3['jobs'])
                      and {r['q'] for d in _p3['jobs'] for r in _bv_js.load(open(_bv_os.path.join(d, 'packet.json')))['items']}
                      == {'1', '2'})
    # v1.23 (C3): driven through job folders to rung 3 — the fallback REWRITE removes the slot's fig_manifest record
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'concept_map': {'1': {'stem_text': 'Compute the yield of the reaction here',
                                           'option_texts': ['1', '2', '3', '4'], 'subtopic_id': 'A.b', 'qtype': 'mcq'}},
                     'answers': {'1': 1}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1,
                     'difficulty_labels': L, 'difficulty_plan_target': {'1': 'Medium'}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _bv_js.dump({'questions': {'1': {'object_type': 'chemical_structure'}, '7': {'object_type': 'x'}}},
                    open(_bv_os.path.join(_h, 'EX_fig_manifest.json'), 'w'))
        _seen3, _rec_at3, _line3 = False, None, False
        for _st3 in range(30):
            _r3 = bv_batch_step('EX', 1, home=_h, echo=False)
            _b3 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
            _k3 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
            _cb3 = ((_b3['bv']['items'].get('1') or {}).get('climb_brief') or {}).get('kind')
            if _r3['status'] == 'rewrite' and _cb3 == 'fallback' and not _seen3:
                _seen3 = True
                _rec_at3 = list(_bv_js.load(open(_bv_os.path.join(_h, 'EX_fig_manifest.json')))['questions'])
                _line3 = any('rung-3 TEXT fallback' in x for x in _r3['lines'])
            if _r3['status'] == 'done':
                break
            if _r3['status'] == 'jobs_out':
                _ln3 = []
                for _jb in _b3['bv']['jobs']:
                    if _jb['role'] == 'adjudicator':
                        _bv_js.dump({'verdict': 'question_defective', 'correct_answer': None, 'single_answer': 'no: two',
                                     'missing_condition': '', 'reason': 'r', 'confidence': 'high'},
                                    open(_bv_os.path.join(_jb['dir'], 'result.json'), 'w'))
                        _ln3.append(_jb['dir'] + ' ADJUDICATE DONE')
                        continue
                    _pk3 = _bv_js.load(open(_bv_os.path.join(_jb['dir'], 'packet.json')))
                    _bv_js.dump({'items': {_x['q']: {'band': 'Medium', 'answer': 2 if _jb['role'].endswith('1') else 3,
                                                     'confidence': 'high', 'assumptions': [], 'single_answer': 'no: 2',
                                                     'leak_or_paraphrase': 'none',
                                                     'distractor_existence_and_class': 'ok',
                                                     'consistency_and_names': 'ok', 'selectivity_basis': 'clean',
                                                     'moves': ['m']} for _x in _pk3['items']}},
                                open(_bv_os.path.join(_jb['dir'], 'result.json'), 'w'))
                    _ln3.append(_jb['dir'] + ' REVIEW DONE')
                open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'a').write('\n'.join(_ln3) + '\n')
            elif _r3['status'] == 'rewrite':
                for _q3 in _r3['rewrite']:
                    _k3['concept_map'][_q3]['stem_text'] += ' x'
                _bv_js.dump(_k3, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        check('c3_fallback_rewrite_removes_the_figure_record', _seen3 and _rec_at3 == ['7'] and _line3
              and _r3['status'] == 'done'
              and _b3['bv'].get('fallback_cleared') == ['1'])
    # production hotfixes v1.22 / v1.22.1 (GAP-2026-11-14-FINAL-ROUND-CAP-DEADLOCK) under S0-BC: the live stranded state
    # (final round at the cap, the slot carried unmeasured, never asked, an open slot chain) is measured by the
    # settlement batch 'S' — its own round count, never the old global one
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'concept_map': {'1': {'stem_text': 'A replacement question on new data about the sample table',
                                           'option_texts': ['3', '4'], 'subtopic_id': 'A.b', 'qtype': 'mcq'}},
                     'answers': {'1': 1}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Medium'}, 'slot_chain': {'1': {'done': False}},
                     'bv': {'batch': 'final', 'round': bc.BV_MAX_ROUNDS, 'status': 'done', 'jobs': [], 'asked': {},
                            'unmeasured': ['1'], 'items': {'1': {'state': 'grading', 'attempt': 2}}}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _mm = bv_batch_step('EX', 1, home=_h, echo=False, final=True)
        _bmm = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))['bv']
        check('bv_final_stranded_slot_migrates_and_is_measured', _mm['status'] == 'jobs_out' and len(_mm['jobs']) == 3
              and not _bmm.get('unmeasured') and _bmm['batch'] == 'S' and _bmm['round'] == 1)
    # v1.23 (C4): a step that asks for a rewrite writes no job; after the rewrite ONE round carries the other question's
    # adjudicator and the rewritten question's reviewers together
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'concept_map': {'1': {'stem_text': 'Compute the yield of the first reaction here',
                                           'option_texts': ['1', '2', '3', '4'], 'subtopic_id': 'A.b', 'qtype': 'mcq'},
                                     '2': {'stem_text': 'Compute the yield of the second reaction here',
                                           'option_texts': ['1', '2', '3', '4'], 'subtopic_id': 'A.b', 'qtype': 'mcq'}},
                     'answers': {'1': 1, '2': 1}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 2}], 'current_batch': 1, 'difficulty_labels': L,
                     'difficulty_plan_target': {'1': 'Medium', '2': 'Hard'}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _r41 = bv_batch_step('EX', 1, home=_h, echo=False)
        _ln4 = []
        for _d in _r41['jobs']:
            _it4 = {}
            for _x in _bv_js.load(open(_bv_os.path.join(_d, 'packet.json')))['items']:
                _it4[_x['q']] = dict({'band': 'Medium', 'answer': 2} if _x['q'] == '1' else {'band': 'Easy', 'answer': 1},
                                     confidence='high', assumptions=[], single_answer='yes', leak_or_paraphrase='none',
                                     distractor_existence_and_class='ok', consistency_and_names='ok',
                                     selectivity_basis='clean', moves=['m'], decisions=1, rationale='r')
            _bv_js.dump({'items': _it4}, open(_bv_os.path.join(_d, 'result.json'), 'w'))
            _ln4.append(_d + ' REVIEW DONE')
        open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'a').write('\n'.join(_ln4) + '\n')
        _r42 = bv_batch_step('EX', 1, home=_h, echo=False)
        _k4 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
        _k4['concept_map']['2']['stem_text'] = 'Compute the yield of the second reaction after two coupled equilibria here'
        _bv_js.dump(_k4, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        _r43 = bv_batch_step('EX', 1, home=_h, echo=False)
        _names4 = sorted(_d.rsplit('/', 1)[-1] for _d in _r43['jobs'])
        check('c4_rewrite_step_writes_no_job_then_one_round', _r42['status'] == 'rewrite' and _r42['jobs'] == []
              and _r42['rewrite'] == ['2'] and _r43['status'] == 'jobs_out'
              and all('/b1/r2/' in _d for _d in _r43['jobs'])
              and _names4 == ['q1_adj', 'reviewer_1', 'reviewer_2', 'reviewer_3'])
    # v1.23 (C3): rung 3 fails, R5b restores the earlier FIGURE version — its figure record comes back with it.
    # Release 2026.11.22: that climb is mode 'br1' only — under the new modes a finding alone stops at rung 2 and
    # the question keeps its figure (bc.R3_FINDING_MAX_RUNG); the same scenario is run in both modes
    for _mode5 in (bc.R3_MODE_LEGACY, bc.R3_MODE_COUNTED):
        with _bv_tf.TemporaryDirectory() as _h:
            open(_bv_os.path.join(_h, 'q1.png'), 'wb').write(b'png')
            _bv_js.dump({'concept_map': {'1': {'stem_text': 'Identify the major product of the reaction shown',
                                               'option_texts': ['A', 'B', 'C', 'D'], 'subtopic_id': 'A.b', 'qtype': 'mcq',
                                               'figure_files': [_bv_os.path.join(_h, 'q1.png')]}}, 'answers': {'1': 1}},
                        open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
            _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 1}], 'current_batch': 1,
                         'difficulty_labels': L, 'difficulty_plan_target': {'1': 'Medium'}, 'difficulty_mode': _mode5},
                        open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
            _bv_js.dump({'questions': {'1': {'object_type': 'chemical_structure'}}},
                        open(_bv_os.path.join(_h, 'EX_fig_manifest.json'), 'w'))
            _seq5 = []
            for _st5 in range(40):
                _r5 = bv_batch_step('EX', 1, home=_h, echo=False)
                _b5 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
                _k5 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
                _rg5 = (_b5['bv']['items'].get('1') or {}).get('rung', 0)
                _seq5.append((_r5['status'], _rg5, '1' in _bv_js.load(open(_bv_os.path.join(_h, 'EX_fig_manifest.json')))['questions'],
                              bool(_r5['restore'])))
                if _r5['status'] == 'done':
                    break
                if _r5['status'] == 'jobs_out':
                    _ln5 = []
                    for _jb in _b5['bv']['jobs']:
                        if _jb['role'] == 'adjudicator':
                            _v5 = ({'verdict': 'author_correct', 'correct_answer': 1, 'single_answer': 'yes'} if _rg5 < 3 else
                                   {'verdict': 'question_defective', 'correct_answer': None, 'single_answer': 'no: x'})
                            _v5.update({'missing_condition': '', 'reason': 'r', 'confidence': 'high'})
                            _bv_js.dump(_v5, open(_bv_os.path.join(_jb['dir'], 'result.json'), 'w'))
                            _ln5.append(_jb['dir'] + ' ADJUDICATE DONE')
                            continue
                        _kk5 = int(_jb['role'].split('_')[1])
                        _a5 = ([1, 1, 3] if _rg5 < 3 else [2, 3, 4])[_kk5 - 1]
                        _bv_js.dump({'items': {_x['q']: {'band': 'Medium', 'answer': _a5, 'confidence': 'high', 'assumptions': [],
                                                         'single_answer': 'yes',
                                                         'leak_or_paraphrase': 'leaks' if (_rg5 < 3 and _kk5 < 3) else 'none',
                                                         'distractor_existence_and_class': 'ok', 'consistency_and_names': 'ok',
                                                         'selectivity_basis': 'clean', 'moves': ['m']}
                                               for _x in _bv_js.load(open(_bv_os.path.join(_jb['dir'], 'packet.json')))['items']}},
                                    open(_bv_os.path.join(_jb['dir'], 'result.json'), 'w'))
                        _ln5.append(_jb['dir'] + ' REVIEW DONE')
                    open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'a').write('\n'.join(_ln5) + '\n')
                elif _r5['status'] == 'rewrite':
                    for _q5 in _r5['rewrite']:
                        _k5['concept_map'][_q5]['stem_text'] += ' v' + str(_rg5)
                        # the author follows the rung-3 KIND the engine chose (release 2026.11.25 F1): only the TEXT
                        # fallback drops the figure
                        _kd5 = ((_b5['bv']['items'].get(_q5) or {}).get('climb_brief') or {}).get('kind')
                        if _rg5 == 3 and _kd5 == 'fallback':
                            _k5['concept_map'][_q5].pop('figure_files', None)
                    for _q5, _p5 in _r5['restore'].items():
                        _rs5 = _bv_js.load(open(_p5))
                        _k5['concept_map'][_q5] = dict(_rs5['entry'])
                        _k5['answers'][_q5] = _rs5['answer']
                    _bv_js.dump(_k5, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
            if _mode5 == bc.R3_MODE_LEGACY:
                # release 2026.11.25 (GAP-2026-11-19-FIGURE-LOSS F1): the defect here is in the WORDING (a leak) — rung 3
                # is a TEXT REBUILD, so the figure record is never removed and the paper ends with its figure
                _cm5l = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))['concept_map']['1']
                check('c3_restore_brings_back_the_figure_record',
                      any(st == 'rewrite' and rg == 3 and fig for st, rg, fig, _rs in _seq5)
                      and all(fig for st, rg, fig, _rs in _seq5)
                      and _seq5[-1][0] == 'done' and _seq5[-1][2] is True and bool(_cm5l.get('figure_files'))
                      and not isinstance(_cm5l.get('bc_fallback'), dict))
            else:
                _cm5 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))['concept_map']['1']
                check('r3_finding_never_reaches_text_fallback_figure_kept', _seq5[-1][0] == 'done'
                      and max(rg for _x, rg, _f, _r in _seq5) == 2 and all(fig for _x, _r, fig, _rr in _seq5)
                      and bool(_cm5.get('figure_files')) and 'finding_open' in (_cm5.get('bv') or {}).get('amber', []))
    # v1.23 (P4): the author/reviewer offset per (subject, band), written to difficulty_state, shown in the packet
    _meta = {f'grader_{k}': {'rubric': {'facets': ['C-COMPUTATIONAL'], 'inferential_steps': 1, 'concepts': 2,
                                        'speed_hack': False, 'negative': False}} for k in (1, 2, 3)}
    _cmo = {str(q): {'stem_text': f's{q}', 'option_texts': ['a', 'b'], 'subject': 'org', 'author_counts': _HARD}
            for q in range(1, 5)}
    _ito = {str(q): {'meta': _meta} for q in range(1, 5)}
    _off = bc.bc_author_offsets(_cmo, _ito, {str(q): 'Hard' for q in range(1, 5)}, L)
    _off2 = bc.bc_author_offsets({k: v for k, v in _cmo.items() if k in ('1', '2')}, _ito, {'1': 'Hard', '2': 'Hard'}, L)
    _apk = bc.bv_author_packet({'q': '9', 'band': 'Hard', 'subject': 'org', 'subtopic_id': 'A.b'}, {}, L, offsets=_off)
    check('p4_offset_measured_capped_and_shown', _off == {'org|Hard': {'n': 4, 'steps': 2, 'concepts': 0}}
          and _off2 == {} and _apk['author_offset'] == {'n': 4, 'steps': 2, 'concepts': 0}
          and any('+2 move(s)' in x for x in _apk['self_check'])
          and not any('move(s)' in x for x in bc.bv_author_packet({'q': '9', 'band': 'Hard', 'subject': 'inorg'}, {}, L,
                                                                     offsets=_off)['self_check']))
    # v1.21 (G-10): the in-progress test used by Create S3-13 / S3-16 (bootstrap.ns_paper_in_progress applies the same)
    with _bv_tf.TemporaryDirectory() as _h:
        _bv_js.dump({'batch_plan': [{'batch_id': 1}]}, open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _bv_js.dump({'batch_plan': [{'batch_id': 1}], 'state': 'DELIVERED'}, open(_bv_os.path.join(_h, 'EX_M2_batch_state.json'), 'w'))
        _bv_js.dump({'batch_plan': []}, open(_bv_os.path.join(_h, 'EX_M3_batch_state.json'), 'w'))
        open(_bv_os.path.join(_h, 'EX_M4_batch_state.json'), 'w').write('{bad')
        check('t_paper_in_progress', isinstance(paper_in_progress(_h, 'EX', 1), dict)
              and all(paper_in_progress(_h, 'EX', k) is None for k in (2, 3, 4, 5)))
    check('bv_job_chunks_shapes', bc.bv_job_chunks(['1', '2'], {}, None) == [['1', '2']] and bc.bv_job_chunks([], {}, 5) == []
          and bc.bv_job_chunks(['1', '2', '3'], {'1': {'figure_dicts': [{}]}}, 2) == [['1'], ['2', '3']])
    # v1.24 (GAP-2026-11-15-RUN-ANALYSIS D1-D3, D6, S3): pre-review gaps, layout proof, earlier-paper offsets, lean fallback
    _fl = bc_figure_with_layout({'file': 'f1.png', 'smiles': 'C[C@H](O)CC', 'stereo_mode': 'abs'})
    _fp = bc_figure_with_layout({'file': 'f2.png', 'kind': 'newman_projection', 'smiles': 'CC'})
    check('v124_figure_with_layout', isinstance(_fl.get('layout'), dict) and _fl['layout'].get('identity_ok') is True
          and 'layout' not in _fp and bc_figure_with_layout({'layout': {'x': 1}}) == {'layout': {'x': 1}}
          and bc_figure_with_layout(None) == {})
    _fdoc = {'item_findings': [{'q': '4', 'gate': 'G-STEM', 'finding': 'stem too short'},
                               {'q': '5', 'gate': 'G-STEM', 'finding': 'other q'}],
             'amber_findings': [{'q': '4', 'gate': 'A-FIGLABELPX', 'finding': 'label 6 px'},
                                {'q': '4', 'gate': 'A-SOMETHINGELSE', 'finding': 'not a pre-review gate'}]}
    _g_ok = bc_prereview_gaps({'organic': True, 'stem_text': 'Identify the product of the reaction shown.',
                               'figure_files': ['f1.png'],
                               'figure_dicts': [{'file': 'f1.png', 'smiles': 'C[C@H](O)CC', 'stereo_mode': 'abs'}]},
                              '4', None)
    _g_list = bc_prereview_gaps({'stem_text': 'Match List-I with List-II.'}, '4', None)
    _g_shown = bc_prereview_gaps({'stem_text': 'The compound shown below is treated with HBr.'}, '4', None)
    _g_fig = bc_prereview_gaps({'stem_text': 'Which figure of merit is largest?'}, '4', None)
    _g_doc = bc_prereview_gaps({'stem_text': 'Plain stem.'}, '4', _fdoc)
    _g_bad = bc_prereview_gaps({'organic': True, 'stem_text': 'x', 'figure_files': ['f9.png'],
                                'figure_dicts': [{'file': 'f9.png', 'kind': 'chair_conformation', 'smiles': 'C1CCCCC1'}]},
                               '4', None)
    _bs_sf = {'stimulus_groups': {'g1': {'qnums': [4, 5], 'stimulus': 'PASSAGE TEXT'}, 'g2': {'qnums': [6], 'stimulus': None}}}
    check('v124_stimulus_fill', bc_stimulus_fill({'stem_text': 'x'}, '4', _bs_sf).get('stimulus_text') == 'PASSAGE TEXT'
          and bc_stimulus_fill({'stem_text': 'x', 'stimulus_text': 'own'}, '4', _bs_sf)['stimulus_text'] == 'own'
          and 'stimulus_text' not in bc_stimulus_fill({'stem_text': 'x'}, '6', _bs_sf)
          and 'stimulus_text' not in bc_stimulus_fill({'stem_text': 'x'}, '7', _bs_sf)
          and bc_stimulus_fill({'stem_text': 'x'}, 'Q?', _bs_sf) == {'stem_text': 'x'}
          and bc_stimulus_fill(None, '4', None) == {}
          and bc.op_content_sha(bc_stimulus_fill({'stem_text': 'x'}, '4', _bs_sf)) == bc.op_content_sha({'stem_text': 'x'}))
    check('v124_shown_cue_is_narrow', all(bc_prereview_gaps({'stem_text': t}, '1') == [] for t in (
              'Consider the statements given below and choose the correct option.',
              'It has been shown that the rate doubles; find the order.',
              'Which figure of merit is largest?', 'The structure of benzene has how many pi electrons?'))
          and all(len(bc_prereview_gaps({'stem_text': t}, '1')) == 1 for t in (
              'The compound shown undergoes ozonolysis.', 'In the graph drawn below, find the slope.',
              'Study the following figure and answer.', 'The pedigree shown is for a rare trait.'))
          and bc_prereview_gaps({'stem_text': 'The compound shown undergoes ozonolysis.', 'given_smiles': 'C=C'}, '1') == [])
    _e_rs = {'stem_text': 'Plain stem here', 'option_texts': ['1', '2'], 'bv': {'grades': {'grader_1': {}}}}
    check('v124_text_has_results', bc_text_has_results(_e_rs) is True and bc_text_has_results({'bv': {}}) is False
          and bc_text_has_results(None) is False
          and bc_text_has_results(dict(_e_rs, bv={'grades': {'g': {}}, 'content_sha': 'other-text'})) is False
          and bc_text_has_results(dict(_e_rs, bv={'grades': {'g': {}}, 'content_sha': bc.op_content_sha(_e_rs)})) is True)
    check('v124_prereview_gaps', _g_ok == [] and len(_g_list) == 1 and 'list_columns' in _g_list[0]
          and len(_g_shown) == 1 and 'figure_files' in _g_shown[0] and _g_fig == []
          and _g_doc == ['G-STEM: stem too short', 'A-FIGLABELPX (AMBER): label 6 px']
          and len(_g_bad) == 1 and 'not proven' in _g_bad[0]
          and bc_prereview_gaps(None, '4', 'junk') == []
          and bc_prereview_gaps({'stem_text': 'Match List-I with List-II.', 'list_columns': [['a'], ['b']]}, '4') == [])
    with _bv_tf.TemporaryDirectory() as _h:
        _rp = _bv_os.path.join(_h, 'EX_registry.json')
        check('v124_registry_offsets_absent', bc_registry_author_offsets(_rp, 'M2') == [])
        _bv_js.dump({'question_index': [
            {'paper_id': 'M1', 'difficulty_state': {'author_offset': {'org|Hard': {'n': 4, 'steps': 2, 'concepts': 0},
                                                                      '_note': 'x'}}},
            {'paper_id': 'M2', 'difficulty_state': {'author_offset': {'org|Hard': {'n': 3, 'steps': 1, 'concepts': 0}}}},
            {'paper_id': 'M0'}, 'junk',
            {'paper_id': 'M3', 'difficulty_state': {'author_offset': {'org|Hard': {'n': 9, 'steps': -2, 'concepts': 0,
                                                                                   'from': 'earlier paper'}}}}]},
                    open(_rp, 'w'))
        check('v124_registry_offsets', bc_registry_author_offsets(_rp, 'M2')
              == [{'org|Hard': {'n': 4, 'steps': 2, 'concepts': 0}}]
              and len(bc_registry_author_offsets(_rp)) == 2
              and bc.bc_author_offsets({}, {}, {}, L, seed=bc_registry_author_offsets(_rp, 'M4'))['org|Hard']['steps'] == 1)
        open(_rp, 'w').write('{bad')
        check('v124_registry_offsets_bad_file', bc_registry_author_offsets(_rp, 'M2') == [])
        _base = bv_budget_value('review_qs_per_job', bc.BV_REVIEW_QS_PER_JOB)
        _fb = bv_budget_value('review_qs_per_job_fallback', _base)
        _r1 = bv_review_qs_per_job(_h)
        _bv_js.dump({'available': True}, open(_bv_os.path.join(_h, 'fw_lean_agents.json'), 'w'))
        _r2 = bv_review_qs_per_job(_h)
        _bv_js.dump({'available': False}, open(_bv_os.path.join(_h, 'fw_lean_agents.json'), 'w'))
        _r3 = bv_review_qs_per_job(_h)
        open(_bv_os.path.join(_h, 'fw_lean_agents.json'), 'w').write('{bad')
        _r4 = bv_review_qs_per_job(_h)
        check('v124_lean_fallback_job_size', _r1 == _r2 == _r4 == _base and _r3 == _fb and _fb >= _base)
    # v1.25.0 Cluster R3 (GAP-2026-11-16): the whole STEP A2 path in mode 'ladder' through job folders — a hard item
    # settles Hard by placement, a padded one is measured below Hard, a dead row goes back before review, and a
    # hostile reviewer (void placements + a blocking code every time) still ends DONE within the round budget
    _lad_r3, _ = bc._ld_synthetic_ladder(L)
    _rr3 = __import__('random').Random(4)
    _true3 = {'1': 0.93, '2': 0.62, '3': 0.93}
    for _hostile in (False, True):
        with _bv_tf.TemporaryDirectory() as _h:
            _cm3 = {q: {'stem_text': f'Question {q} about the scope', 'option_texts': ['w', 'x', 'y', 'z'],
                        'subtopic_id': 's.t1.u1', 'qtype': 'mcq', 'subject': 's', 'ask_format': 'direct'} for q in ('1', '2')}
            if not _hostile:
                _cm3['3'] = {'stem_text': 'Match List-I with List-II.', 'subtopic_id': 's.t1.u1', 'qtype': 'mcq',
                             'subject': 's', 'option_texts': ['A-III, B-I, C-II, D-IV', 'A-II, B-I, C-III, D-IV',
                                                              'A-III, B-II, C-I, D-IV', 'A-I, B-III, C-II, D-IV']}
            _bv_js.dump({'concept_map': _cm3, 'answers': {q: 1 for q in _cm3}}, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
            _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': len(_cm3)}], 'current_batch': 1,
                         'difficulty_labels': L, 'difficulty_plan_target': {q: 'Hard' for q in _cm3}},
                        open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
            _bv_js.dump(_lad_r3, open(_bv_os.path.join(_h, 'EX_difficulty_ladder.json'), 'w'))
            _hist3, _r3s = [], None
            _anc3 = None                                # release 2026.11.24 (B1): each reviewer's own anchor draw
            for _stp in range(80):
                _r3s = bv_batch_step('EX', 1, home=_h, echo=False)
                if _anc3 is None and _r3s['status'] == 'jobs_out':
                    _anc3 = {_jx['role']: tuple(sorted(((_jx.get('tasks') or {}).get('1') or {}).get('meta') or {}))
                             for _jx in _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))['bv']['jobs']
                             if str(_jx.get('role')).startswith('reviewer_')}
                _hist3.append(_r3s['status'])
                if _r3s['status'] != 'jobs_out' and _r3s['status'] != 'rewrite':
                    break
                if _r3s['status'] == 'rewrite':
                    _k3 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))
                    for _q3 in set(_r3s['rewrite']) | {x.split('PRE-REVIEW Q')[1].split(' ')[0] for x in _r3s['lines'] if 'PRE-REVIEW Q' in x}:
                        _k3['concept_map'][_q3]['stem_text'] += f' r{_stp}'
                    _bv_js.dump(_k3, open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
                    continue
                _b3 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
                _ln3 = []
                for _jb in _b3['bv']['jobs']:
                    if _jb['role'] == 'adjudicator':
                        _bv_js.dump({'verdict': 'author_correct', 'correct_answer': 1, 'single_answer': 'yes',
                                     'missing_condition': '', 'reason': 'r', 'confidence': 'high'},
                                    open(_bv_os.path.join(_jb['dir'], 'result.json'), 'w'))
                        _ln3.append(_jb['dir'] + ' ADJUDICATE DONE')
                        continue
                    _out3 = {'items': {}}
                    for _row in _bv_js.load(open(_bv_os.path.join(_jb['dir'], 'packet.json')))['items']:
                        _q3 = _row['q']
                        _rec3 = {'answer': 1, 'confidence': 'high', 'assumptions': [], 'single_answer': 'yes',
                                 'defects': [], 'depth': 3}
                        _tk3 = (_jb.get('tasks') or {}).get(_q3)
                        if _hostile:
                            _rec3.update(ranking=['A'], defects=[{'code': 'D-AMBIGUOUS', 'evidence': 'always'}])
                        elif _tk3:
                            _rec3['ranking'] = sorted(_tk3['map'], key=lambda lb, t=_tk3, q=_q3: (
                                _true3[q] if t['map'][lb] == 'ITEM' else t['meta'][t['map'][lb]]['p']) + _rr3.gauss(0, 0.03))
                        _out3['items'][_q3] = _rec3
                    _bv_js.dump(_out3, open(_bv_os.path.join(_jb['dir'], 'result.json'), 'w'))
                    _ln3.append(_jb['dir'] + ' REVIEW DONE')
                open(_bv_os.path.join(_h, 'EX_M1_bv', 'returned.txt'), 'a').write('\n'.join(_ln3) + '\n')
            _c3 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))['concept_map']
            _s3 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_batch_state.json')))
            if _hostile:
                check('r3_hostile_reviewer_ends_done_within_budget', _r3s['status'] == 'done'
                      and _s3['bv']['round'] <= bc.BV_MAX_ROUNDS and _c3['1'].get('difficulty') != 'Hard')
            else:
                check('r31_each_reviewer_gets_its_own_anchor_draw', isinstance(_anc3, dict) and len(_anc3) == 3
                      and all(_anc3.values()) and len(set(_anc3.values())) >= 2)
                check('r3_ladder_flow_hard_padded_deadrow', _r3s['status'] == 'done' and _s3['difficulty_mode'] == 'ladder'
                      and _c3['1'].get('difficulty') == 'Hard'
                      and (_c3['1'].get('difficulty_check') or {}).get('measure') == 'placement_r3'
                      and _c3['2'].get('difficulty') in ('Easy', 'Medium')
                      and (_c3['3'].get('bv_state') == 'disclosed' or int(_s3['bv']['items']['3'].get('rung') or 0) >= 1))
                _rep3 = bv_r3_report(_s3, _c3, _lad_r3)
                check('r3_report_count_rule', isinstance(_rep3.get('count_rule'), dict) and _rep3['count_rule']['ok'] is False
                      and any('RED' in x for x in _rep3['amber']))
                # release 2026.11.25 (P13, T-U11): in mode 'ladder' the ENGINE writes difficulty_obs on every entry
                check('s13loop_TU11_batch_step_engine_owns_obs',
                      all((_c3[_q].get('difficulty_obs') or {}).get('mode') == 'ladder'
                          and not bc.difficulty_obs_signature(_c3[_q].get('difficulty_obs')) for _q in _c3 if isinstance(_c3[_q], dict)))
    # ── release 2026.11.26 — GAP-2026-11-20-RUNG3-BIND-DEADLOCK (F1 / F9): STEP A3 binds every rung-3 question that
    # keeps its figure by design; a TEXT fallback still carrying a figure is repaired by STEP A2 (bounded), so the
    # pair STEP A2 DONE -> STEP A3 BOUND is always reached — also for an EARLIER batch's question, worker ignoring
    # every order (worst case) ──
    with _bv_tf.TemporaryDirectory() as _h:
        _sv9 = {r: {'answer': 2, 'confidence': 'high', 'single_answer': 'yes', 'leak_or_paraphrase': 'none',
                    'distractor_existence_and_class': 'ok', 'consistency_and_names': 'ok', 'selectivity_basis': 'clean'}
                for r in bc.BV_ROLES_SOLVE}
        _png9 = _bv_os.path.join(_h, 'q_fig.png')
        open(_png9, 'wb').write(b'png')
        _kinds9 = {'1': ('fallback', None), '2': ('text_rebuild', None), '3': ('fig_rebuild', None),
                   '4': ('fallback', {'rung': 1}), '5': ('fallback', None)}
        _ents9 = {}
        for _q9, (_k9, _rs9) in _kinds9.items():
            _e9 = {'stem_text': f'Rung three question {_q9} on the acidity order of substituted phenols',
                   'option_texts': ['a', 'b', 'c', 'd'], 'qtype': 'mcq',
                   'figure_files': [] if _q9 == '5' else [_png9]}
            _e9 = _bc_render_shas(_e9)
            _b9 = {'rule': bc.BC_RULE, 'state': 'settled', 'rung': 3, 'rung3_kind': _k9, 'solvers': _sv9,
                   'grades': {}, 'packets': {}, 'meta': {}, 'vision': {}, 'versions': [],
                   'key': {'state': 'settled', 'certified_by': 'unanimous', 'decided_key': 2},
                   'content_sha': _bc_entry_sha(_bc_render_shas(_e9))}
            if _rs9:
                _b9['restore'] = _rs9
            _e9['bv'] = _b9
            _e9['bv_state'] = 'settled'
            _ents9[_q9] = _e9
        _bv_js.dump({'concept_map': _ents9, 'answers': {q: 2 for q in _ents9}},
                    open(_bv_os.path.join(_h, 'EX_M1_answer_key.json'), 'w'))
        # the five questions belong to batch 1; batch 2 is current (an EARLIER batch's question must be repaired too)
        _bv_js.dump({'batch_plan': [{'batch_id': 1, 'q_start': 1, 'q_end': 5}, {'batch_id': 2, 'q_start': 6, 'q_end': 6}],
                     'current_batch': 2, 'difficulty_labels': L,
                     'bv': {'items': {q: v['bv'] for q, v in _ents9.items()}}},
                    open(_bv_os.path.join(_h, 'EX_M1_batch_state.json'), 'w'))
        _bv_js.dump({q: 'h' + q for q in _ents9}, open(_bv_os.path.join(_h, 'ih9.json'), 'w'))
        _a3a = bc_bind_batch('EX', 1, _bv_os.path.join(_h, 'ih9.json'), home=_h, echo=False, upto=5)
        check('gap1120_F1_bind_only_refuses_the_text_fallback_with_a_figure',
              sorted(_a3a['bound'], key=int) == ['2', '3', '4', '5'] and list(_a3a['refused']) == ['1']
              and 'run STEP A2 again' in _a3a['refused']['1'])
        _trail9, _st9 = [], None
        for _i9 in range(4 * (bc.BC_FALLBACK_FIGURE_ORDERS + 1) * (bc.BC_REWRITE_REISSUE_MAX + 2)):
            _st9 = bv_batch_step('EX', 1, home=_h, echo=False)
            _trail9.append(_st9['status'])
            if _i9 == 0:
                _rw9 = list(_st9.get('rewrite') or [])
            if _st9['status'] == 'done':
                break
        _c9 = _bv_js.load(open(_bv_os.path.join(_h, 'EX_M1_answer_key.json')))['concept_map']
        check('gap1120_F9_step_a2_orders_the_repair_of_an_earlier_batch_question',
              _trail9[0] == 'rewrite' and _rw9 == ['1'])
        check('gap1120_F9_worker_ignoring_every_order_still_ends_done',
              _trail9[-1] == 'done' and 'fallback_figure_kept' in (_c9['1']['bv'].get('amber') or [])
              and _c9['1'].get('bv_state') == 'disclosed' and not bc.bc_fallback_figure_open(_c9['1'])
              and _trail9.count('rewrite') <= bc.BC_FALLBACK_FIGURE_ORDERS * (bc.BC_REWRITE_REISSUE_MAX + 1))
        _a3b = bc_bind_batch('EX', 1, _bv_os.path.join(_h, 'ih9.json'), home=_h, echo=False, upto=5)
        check('gap1120_F9_step_a3_binds_after_the_repair', _a3b['status'] == 'bound'
              and sorted(_a3b['bound'], key=int) == ['1', '2', '3', '4', '5'])
        check('gap1120_F9_footer_discloses_the_kept_figure',
              any(c == 'AMBER' and 'kept its figure' in t for c, t in bc.bc_amber_lines('1', _c9['1']))
              and not any('replaced by a text question' in t for c, t in bc.bc_amber_lines('2', _c9['2'])))
    print(f"SELF-TEST: {passed}/{total} PASS")
    if fails:
        print("FAILED: " + ", ".join(fails))
    return passed == total


def dg_fleet_scan(root, apply=False, out=print):
    """GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER §9 fleet scanner / healer — the
    file-I/O wrapper around paper_pipeline.dg_fleet_heal (pure). Lives here because
    this engine already owns the difficulty_gate BIRTH write and imports
    paper_pipeline at module level. Scans every *_registry.json under root; with
    apply=True heals per DG-INVARIANT, writes a .bak beside every changed file and
    logs each change in the record's migrations[]. Never touches a record it cannot
    interpret (unknown status → reported under 'escalate'). Returns the totals.
        python3 final_assembly.py --dg-fleet-scan /path/to/projects            # report
        python3 final_assembly.py --dg-fleet-scan /path/to/projects --apply    # heal"""
    import glob
    import json
    import os
    import shutil
    tot = {'illegal': 0, 'healed': 0, 'stuck_scoped': 0, 'pending': 0, 'escalate': 0}
    for path in sorted(glob.glob(os.path.join(root, '**', '*_registry.json'), recursive=True)):
        try:
            with open(path, encoding='utf-8') as fh:
                reg = json.load(fh)
        except (OSError, ValueError) as e:
            out(f"[SKIP] {path}: {e}")
            continue
        r = pp.dg_fleet_heal(reg, apply=apply)
        for pid, st, n, fld, fr, to in r['illegal']:
            out(f"[ILLEGAL] {path} :: {pid} :: status={st!r} rounds={n} -> {fld} {fr}->{to}")
        for pid, st, n in r['escalate']:
            out(f"[ESCALATE] {path} :: {pid} :: status={st!r} rounds={n} -> NO AUTO-REPAIR")
        for pid in r['stuck_scoped']:
            out(f"[STUCK-SCOPED] {path} :: {pid} :: PENDING on a scoped paper -> DORMANT/scoped_paper")
        for pid in r['pending']:
            out(f"[PENDING] {path} :: {pid} :: gate not yet run (expected if TestExplain has not run)")
        if r['changed']:
            shutil.copy2(path, path + '.bak')
            with open(path, 'w', encoding='utf-8') as fh:
                json.dump(reg, fh, ensure_ascii=False, indent=1)
            out(f"[HEALED] {path} (backup: {path}.bak)")
        for k in tot:
            tot[k] += len(r[k])
    out("DG-FLEET-SCAN " + " ".join(f"{k}={v}" for k, v in tot.items()))
    return tot


if __name__ == '__main__':
    import sys
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    if '--dg-fleet-scan' in sys.argv:
        _i = sys.argv.index('--dg-fleet-scan')
        _root = sys.argv[_i + 1] if len(sys.argv) > _i + 1 and not sys.argv[_i + 1].startswith('--') else '.'
        _t = dg_fleet_scan(_root, apply='--apply' in sys.argv)
        sys.exit(1 if (_t['illegal'] or _t['stuck_scoped'] or _t['escalate']) and '--apply' not in sys.argv else 0)
    print("final_assembly.py — Step 7 Final Assembly engine. Run with --self-test.")
