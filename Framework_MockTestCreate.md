# Framework_MockTestCreate v5.75
# v5.75 — 2026-08-27 — GAP-2026-08-27-DIFFICULTY-PROFILE (paired with Blueprint v1.57.0,
#   blueprint_core Cluster DP, MockTestAnalyse v2.55). S3: the difficulty plan is built PER
#   SECTION when difficulty_schedule[N].by_section is present (bc.assign_difficulty_bands_by_
#   section; paper-wide plan kept for progressive/legacy schedules); the optional difficulty
#   profile is loaded and validated (bc.dp_check_profile). S7 CHECK 3c reads calibration
#   examples from bc.dp_calibration instead of section_rules' retired PYQ_DIFFICULTY_
#   CALIBRATION. Quotas, gates and repair unchanged.
# v5.74 — 2026-08-26 — GAP-2026-08-26-REPAIR-BATCH-LAW (paired with DeliveryFooter v1.28;
#   spec only, no engine change). §S16 repair mode regenerated EVERY rework_q in ONE
#   response ("PARTS: 1") while the Batch Stop Law (S4-4, B-1..B-8) forbids exactly that
#   for a fresh paper — and for the same reason: generation quality decays with the
#   number of questions authored in one context. The reference paper's gate flagged 32
#   questions, i.e. more than a whole fresh batch three times over. FIX: NEW S16-1b — the
#   REPAIR BATCH PLAN: rework_qs (ascending) are split into batches of at most
#   MAX_BATCH_SIZE (S4-2's ceiling, 10), written to [ExamCode]_M[N]_repair_state.json;
#   one batch per response, the S4-6 continue contract between batches, B-1..B-7 by
#   reference, B-8's analogue = the final repair batch auto-advances to S16-3. The
#   pre-repair snapshot is taken ONCE, at S16-1b, BEFORE the first regeneration, on the
#   registry working copy. MID-BATCH DELIVERABLE: the cumulative paper as
#   [ExamCode]_[slug]_Create_Repaired_PARTIAL_[k]of[K].docx (F1 footer) — a name Step 9-R
#   REFUSES, so a half-repaired paper can never be explained; the registry is WITHHELD
#   mid-batch by design (a partial registry beside a partial paper would let 9-R run on
#   it). FINAL batch: S16-3 exactly as v5.73 — _Create_Repaired.docx + registry.json
#   (Replace), F2. A rework list of ≤ 10 is a single batch and behaves exactly as before.
#   S16-1 P0 now loads the WORKING copy on a continue/resume turn while the fingerprint
#   is always the PROJECT copy's. `TestCreateRepair P[N] resume` rebuilds from
#   repair_state.json (S4-12 analogue).
# v5.73 — 2026-08-26 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM (paired with MockTestExplain
#   v1.46.0, MockDeliver v1.16.0, DeliveryFooter v1.27, paper_pipeline v5.74 Cluster RH,
#   final_assembly v5.60, explain_engine v2.9; LAW_REGISTRY REGISTRY-HANDOFF-LAW,
#   mock_sync_audit MS-14). P0, every exam. registry.json is written by FOUR mock-track
#   steps and only THIS step's Final Assembly told the operator to put it back; the
#   §S16 repair mode rewrote stems, re-sealed keys and added the pre-repair snapshot,
#   then listed ONLY the `_Repaired` docx as its deliverable — so the snapshot §7A-R R3
#   depends on never reached the project and the repair pair dead-looped. FIX: (1) §S16-3
#   gains a delivery contract — the closed set is pp.handoff_set('TestCreateRepair', …)
#   = repaired docx + registry.json (Replace in Project Files), verified by
#   pp.verify_handoff_outputs, one present_files call, F2 footer, handoff lines from
#   pp.handoff_footer_lines. (2) OPERATOR DECISION 2026-08-26: the Tier-A audit dossier is
#   NOT a deliverable. S13-4b writes it to /home/claude; S13-4c reads it there; it joins
#   the DO-NOT-DELIVER list; S13-6 / S13-7 / S13-8 / S13-9 / R-DELIVER / G-DELIVERY-SET /
#   §17 DoD all state the closed set as EXACTLY {Create.docx, registry.json} — the
#   count-drift the v5.54.1 entry patched is gone because the set no longer varies.
#   final_assembly.predelivery_checklist treats `_audit_dossier.json` as an internal
#   sidecar (check 5) so a staged dossier is a LEAK, never a deliverable. No
#   allocation, quota, axis, gate-count or generation change.
# v5.72 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS (paired with MockTestExplain
#   v1.45.0, MockDeliver v1.15.0, DeliveryFooter v1.26, blueprint_core Cluster E2d,
#   paper_pipeline v5.72). §S16 repair mode becomes DIRECTION-AWARE: the windowed gate
#   record carries rework_directions ('harder' | 'easier') because the acceptance-window
#   rule can flag a middle-band question as too HARD; S16-2 reads the direction per q and
#   asserts the rewrite's own CHECK 3c obs lands inside the label's window before
#   committing. S16-1 P1: a FAILED record without pp.dg_is_windowed (retired band-equality
#   rule) is never repaired — the operator is sent to re-run TestExplain. Completion line
#   reports harder/easier counts. No allocation, quota, axis, or gate-count change.
# v5.71 — 2026-08-25 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER (paired with
#   paper_pipeline v5.71 Cluster DG, final_assembly v5.58, MockTestExplain v1.44.0,
#   MockDeliver v1.14.0, DeliveryFooter v1.25, audit_canonical v2.19). P0. A
#   TestCreateRepair session, while adding rework_stem_hashes at §S16-3, ALSO set
#   repair_rounds_used=1 on the still-FAILED difficulty_gate record — a pair no step
#   can produce on purpose — and deadlocked TestExplainRepair, TestDeliver and this
#   step's own §S16-1 P1 ("consumed") with no exit. The only guard was the clause
#   "UNTOUCHED except adding rework_stem_hashes", one line of prose next to this
#   step's own `'round': 1` session_log entry and "REPAIR COMPLETE" print. FIX: §S16-3
#   writes the snapshot ONLY through pp.dg_add_rework_snapshot (write-once; cannot
#   touch status or the counter; refuses off a FAILED record) using the ONE shared
#   digest pp.dg_stem_hash (raw first paragraph, label included — the algorithm §7A-R
#   R3 also calls, previously unspecified and described two contradictory ways); a
#   named ⛔ prohibition on both fields replaces the exception clause; §S16-1 gains P0
#   = pp.dg_preflight (heals a corrupt record with mandatory disclosure, refuses an
#   unknown status) and P1 branches on the state PAIR with every next step from
#   pp.dg_next_step. Engine twin: final_assembly v5.58 stamps the birth record via
#   pp.dg_stamp_pending (mock → PENDING, scoped → DORMANT/scoped_paper — every scoped
#   paper was previously born PENDING and undeliverable). Superseded v5.59 entry moved
#   verbatim to SPEC_HISTORY.md (EC-P42).
# v5.70 — 2026-08-24 — CHG-2026-08-24-FIG-NOLABEL + GAP-2026-08-24-MATH-RESIDUE-SHIPPED
#   (paired with audit_canonical v2.17). Two operator-driven fixes, both measured on
#   the delivered IIT_JAM_CHEMISTRY Mock 01 and both exam-agnostic (~200 exams).
#   (1) NO "Problem Figure:" LABEL LINE. S10-8/S10-8A hardcoded the label as the
#   problem_label DEFAULT and emitted it before every problem image — 18 label
#   paragraphs in the reference paper. Default is now None and the emission is
#   guarded, so a figural block reads Q.N stem -> problem image(s) directly. Safe by
#   construction: no gate reads the label (audit_canonical carries the string only
#   as inert self-test fixture filler; G-FIGURAL-COMPOSITE counts IMAGES, never
#   label paragraphs), and the S12-NEW-13 cue regex keeps its 'problem figure'
#   alternative so pre-v5.70 papers still identify. An explicit caller-passed
#   label still renders (call-compatible, the render_figural_image `transparent`
#   precedent).
#   (2) FLAT SUB/SUPERSCRIPT NOTATION SHIPPED. Q.12/Q.46 stems+options carried
#   0 OMML islands with literal-underscore orbital labels (plus one half-Unicode
#   t2g-style form) while the SAME questions' Step-9 explanations carried 12
#   proper OMML islands — the S10-4 funnel existed and NOTHING enforced it: MC3
#   was WARN-and-deliver, the S4-11 checklist had no residue item, audit.py had
#   no flat-subscript arm, and MATH_TRIGGER_RE missed the half-Unicode spelling.
#   FIXES: MC3 SPLIT SEVERITY — detected ASCII-dialect residue in a stem/option is
#   NEW GATE G-MATH-RESIDUE (S12-NEW-30), a per-batch FIXABLE FAIL that FORBIDS
#   present_files (S12-0 Zero-Warning Policy); the t3 compile-failure fallback
#   KEEPS the v5.47 forgiving-boundary AMBER. S4-11 gains its 43rd item; STEP D
#   report, §13 sweep, §17 DoD and §18 glossary register the gate (80 -> 81).
#   MATH_TRIGGER_RE and the residue detector gain the half-Unicode subscript
#   alternative (a Unicode subscript digit followed by a LOWERCASE letter —
#   t2g/C2v-style labels; H2O-style single trailing subscripts stay plain per
#   rule 2, the case split that makes the pattern false-positive-free). Rule 3a
#   gains explicit chemistry examples. Engine twin: audit_canonical v2.17 gate
#   A-SUBFLAT (FAIL) + catch/clean self-test fixtures — the enforcement of record.
# v5.69 — 2026-08-24 — GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING (paired with MockTestExplain v1.42.0, MockDeliver
#   v1.13.0). New §S16 repair mode: TestCreateRepair/MockCreateRepair P[N] Q…
#   rewrites ONLY the gate's rework_qs, harder, at the same slots — label,
#   quota, axes untouched; stem-supplied-relation rule enforced in repair
#   CHECK 3c; surgical S13-4 update; '_Repaired' deliverable; keys re-sealed.
# v5.68 — 2026-08-24 — GAP-2026-08-24-AXIS-PAPER-SERIES-COLLISION (paired with
#   final_assembly v5.57, audit_seam v1.2). The SECOND instance of the v5.67 class,
#   found by the cross-step field-contract sweep: the S13-4 axis snapshots were
#   persisted as reg['axis1_paper'][str(N)] / reg['axis3_paper'][str(N)] — the paper
#   ORDINAL — on a registry shared across series, so a scoped paper of the same
#   ordinal silently destroyed the mock's snapshot (and two scoped series destroyed
#   each other). The field exists to be a HISTORICAL LEDGER (v5.49); on any exam
#   mixing mocks and scoped papers it had silently reverted to the rolling snapshot
#   v5.49 fixed. Now paper_id-keyed, ordinal key MOCK-only — the options_by_q shape.
#   Machine-checked from now on by audit_seam v1.2's KEY-SHAPE gate.
# v5.67 — 2026-08-24 — GAP-2026-08-24-OPTIONS-BY-Q-SERIES-COLLISION (paired with
#   final_assembly v5.56, audit_canonical v2.16, MockTestExplain v1.41.0). The ND6
#   contract keyed options_by_q by the paper ORDINAL ("N"); on the SHARED registry a
#   scoped paper with the same ordinal overwrote the mock's map (measured: Step 9 on
#   Mock 1 hard-stopped after SUBJ:PHYS:01 was committed). options_by_q is now keyed
#   by paper_id (authority) with the ordinal key retained for the MOCK series only.
#   Spec text only — the writer is final_assembly.regcheck (S13-REGCHECK).

# v5.65 — 2026-08-23 — HYGIENE-2026-08-23-STEP6-AUDIT companion (one dead fallback
#   tier removed; NO behaviour change on any conforming exam). §2 R24's option-label
#   chain read bp.get('option_label_format') — a blueprint key NO writer produces:
#   Framework_Blueprint §14 writes option_label and documents it visibility-only
#   (this step's authority is section_rules R10, with exam_config as override).
#   The dead tier is the exact v1.38 class ("a silently dead fallback tier is worse
#   than no tier — it looks like a supported override") and could never have been
#   correct even if wired: option_label's value shape ("1/2/3/4") is a label LIST,
#   not a '{i}.  {text}' TEMPLATE. Tier removed; the chain is now exam_config ->
#   section_rules -> hardcoded default. section_rules always carries
#   option_label_format (Step 5 CATEGORY C mandatory), so the removed tier was
#   unreachable on every conforming exam — output byte-identical.
# v5.64 — 2026-08-22 — GAP-1C-OMATH-SQRT-DELEGATION (Item 1c). The S10-4 OMML
#   helpers sqrt and omath were re-localised copies of explain_engine's — output
#   byte-identical, bodies cosmetically drifted (*p vs *parts; f-string wrapping) —
#   entered as inherited_pre_existing debt in XSPEC_DIVERGENCE_BASELINE.json at
#   2026.08.20.3. Paid down per the DELEGATION contract: both are now assignment
#   aliases (sqrt = explain_engine.sqrt; omath = explain_engine.omath), so no spec
#   FunctionDef exists to drift and the engine is the single authority.
#   explain_engine.py added to the MockCreate/TestCreate routes (routes.json),
#   matching the MockExplain/TestExplain/PYQExplain precedent. Both baseline
#   entries DELETED in the same release — the baseline's stale rule requires it.
#   Byte-identity proven over 9 cases incl. None, empty, pre-wrapped OMML and
#   escaping. frac/sup/_r/_r_wrap/_esc/add_math are already fingerprint-identical
#   to the engine and stay local. No artefact moves.
# v5.63 — 2026-08-22 — GAP-1B-STEP7-READ-SET (Item 1b; the MockTestExplain S0-3
#   precedent applied to Step 7). NEW S1-0 — SESSION CLASS AND READ SET: the axis is
#   FINAL vs NON-FINAL (never fresh/resume). A NON-FINAL batch session skips exactly
#   the Final-Assembly family (S13-1..S13-9, S13-4b/4c, S13-REGCHECK, S13-QINDEX) and
#   the close-out pair (S17-1 DoD, S17-2 downstream handoff) — every reference to
#   those sections from the per-batch path is a "commits at Final Assembly" pointer,
#   verified, not per-batch execution. S13-9A (F1 footer after EVERY batch) and all
#   S4/gate law stay in every read. FINAL = last planned batch OR plan unknown
#   (fresh mock before S3-16) OR Final-Assembly re-run; unknown -> FINAL, escalation
#   mandatory and one-way BEFORE S4-9 hands to Final Assembly. Ranges GENERATED into
#   SPEC_SECTIONS.json (spec_sections.py v3); bootstrap.py --trigger MockCreate
#   decides the class from batch_state.json (is_final / remaining<=1). MockCreate
#   and TestCreate DELETED from SPEC_BUDGET_BASELINE (audit_specs_ext.py) — the
#   route is now covered by design (has_read_set), not by exemption; the ratchet
#   keeps MockBlueprint only. No artefact moves.
# v5.62 — 2026-08-22 — GAP-1A-STEP7-UNBOUND-NAMES (Wave: grandfathered-NameError
#   payoff, Release A). The ten GRANDFATHERED_MUST_FIX names in generate_subtopic /
#   controlled_reuse / pick_presentation / scenario_iterator — every one a guaranteed
#   NameError under execution — are now bound, split by the EXECUTION-BOUNDARY LAW:
#   REAL python where drift between sessions would corrupt persisted state
#   (canonical: deterministic per-'|'-segment key normaliser feeding the RULE B/C
#   ledgers in batch_state.json; flag: byte-identical to ScopedBlueprint's, XSPEC
#   silent by identity; weighted_patterns: sorts on the fields Step 5 ACTUALLY emits
#   — frequency/raw_count — and drops deprecated + 'absent'-placeholder entries), and
#   pass-bodied CLASS: J stubs for the six judgment operations (build_question,
#   cross_mock_duplicate, passes_quality_gates, invent_distinct_scenario,
#   widen_scenario_space, derive_scenario_from_pattern) in a NEW column-0 fence —
#   C6-PRE requires any fence carrying a model-agency marker to parse RAW, which an
#   indented body never does. The two ledgers are bound at SESSION START in S3-1
#   with an IDEMPOTENT init (globals().get) so a re-read after S4-12 rehydration
#   cannot wipe a resumed session's state. CROSS-STEP SYNC FIX folded in:
#   scenario_iterator read pk['operation']/pk['structural_shape'], two fields NO
#   Step-5 producer has ever written (analyse_engine emits template/approach/
#   frequency/raw_count/confidence/deprecated) — a guaranteed KeyError against every
#   section_rules.md in the estate; the (operation, shape) pair is now DERIVED from
#   the pattern text by derive_scenario_from_pattern (CLASS: J). Baseline: the ten
#   entries deleted from spec_name_audit_baseline.json (dict + _grandfathered);
#   147 baselined, 2 grandfathered remain (Blueprint EXAM, PYQScan
#   MIN_PATTERN_SIZE — Release B). No engine changes. No artefact moves.
# v5.61 — 2026-08-22 — GAP-2026-08-22-FIGASPECT-SELF-FULFILLING (figural_core, 124
#   fixtures). The option-set canvas-aspect derivation was circular: it measured the
#   union of pass-1 data_windows, which apply_data_window() had already inflated to the
#   canvas aspect pass 1 rendered on — so square molecule sets stayed on the 0.72
#   landscape default forever (measured live: hexagon set, true aspect 2/sqrt(3), derived
#   0.69, set fill 41% < the 45% floor, G-FIGFIT BLOCKING a correct drawing), and an
#   author-declared canvas_aspect was silently clobbered. Fix (Q12.1): the fitter records
#   fit.content_window and fit.stroke_window (raw data-coordinate extents); the set
#   aspect derives from zoom-invariant STROKE geometry (content, then window, fallback);
#   a unanimous declared aspect is honoured exactly; pass 2 seeds from the content
#   union. Same fixture now: aspect 1.1547 exact, fill 70%, gate clean. Single problem
#   figures unchanged (declared or 0.72 default, as documented since v5.55).
# v5.60 — 2026-08-21 — GAP-2026-08-21-DIFFICULTY-STICKER-LABELS (blueprint_core
#   Cluster E2c, final_assembly v1.6, audit_canonical v2.15, Blueprint v1.51.0,
#   TestExplain §7A-M, PYQExplain divergence note resolved). THE DEFECT, measured on
#   IIT_JAM_CHEMISTRY M01: the difficulty quota said HOW MANY of each band but nothing
#   defined WHAT a band meant, so labels were slot names — 14/60 agreed with the shared
#   Tier-1 rubric (bc.assess_difficulty), at least 32 'Hard' labels sat on questions
#   that measure Medium, and 4 'Easy' labels sat on MSQ/NAT positions where the
#   rubric's qtype floor makes that band unreachable. Every count-based gate (G-QINDEX,
#   A-QINDEX 1-6, K-BAL) passed, because every gate measured the DISTRIBUTION, not the
#   QUESTIONS — the same defect class as G-FIGINK and the axis sentinel: the declared
#   property, not the artefact. THE FIX — one scale, four layers, user ratio untouched:
#   the trigger/band ratio remains the LAW for counts (deliberately hard series stay
#   fully supported); bc.assess_difficulty becomes the DEFINITION of the label on both
#   pipelines (the §7A divergence note's adopted contract: same RUBRIC, different
#   mechanisms). (1) S3 builds difficulty_plan via bc.assign_difficulty_bands —
#   deterministic, seed-rotated per mock, bottom band only on positions whose floor
#   allows it — after bc.difficulty_feasibility HARD STOPS any count the exam shape
#   cannot honestly hold (with the achievable maximum named). (2) CHECK 3c / G-DIFF:
#   author TO the band via bc.difficulty_authoring_profile, record difficulty_obs from
#   the derivation already performed for the sidecar, and accept only when
#   bc.verify_difficulty_obs(label, obs) agrees — MAX_DIFF_TRIES=6, then a quota-
#   preserving band-swap escape, then HARD STOP; a label an evidence contradicts never
#   ships. (3) write_q_to_sidecar carries difficulty_obs (keyword-only, NO default —
#   the v5.52 argument) into concept_map; final_assembly v1.6 carries it into
#   registry.question_index. (4) A-QINDEX check 7 FAILs bottom-band labels on MSQ/NAT
#   positions on EVERY registry (zero-judgment, catches legacy data), check 8
#   recomputes label == rubric(obs) on evidence-bearing entries via the same engine
#   call as G-DIFF so gate and audit cannot drift. DORMANCY: no difficulty_schedule
#   entry or a non-3-band vocabulary ⇒ plan None, G-DIFF off, pre-v5.60 behaviour
#   byte-for-byte; legacy registries without obs skip check 8 and keep check 7.
#   LEVEL ANCHOR: step/concept units are level-relative (bp_level + the subtopic's
#   calibration examples from the difficulty profile, v5.75); assumed prerequisite knowledge = recall (0 steps),
#   so one rubric serves grade-10 through post-graduation with honest labels.
# v5.58 — 2026-08-20 — GAP-2026-08-20-AXIS1-EMPTY-SCHEDULE-SENTINEL (blueprint_core
#   +1 fixture). A paper whose blueprint predates Blueprint v1.45 renders ZERO figures
#   against a real Axis-1 budget, on every mock, silently. S7-NEW-B0 reads the per-mock
#   figural schedule and guards it `if figural_slots else None`, with the promise "empty
#   schedule (pre-v1.45 blueprint) => fall through ... every un-remeasured exam keeps its
#   current behaviour exactly". ROOT CAUSE, reproduced: for an empty quota
#   bc.schedule_figural_slots returns `[{}, {}, ... x n]` — a TRUTHY list of EMPTY dicts,
#   never []. The sentinel therefore never fires, the per-mock filter runs with an empty
#   allowance, `_left.get(sid, 0) > 0` is false for every candidate, and the whole
#   figural-capable set is discarded BEFORE rank_figural_candidates and BEFORE
#   axis_grant_figural — so neither the ranking nor the budget nor the irreducible
#   exemption is ever consulted, and no gate fires because the generator "chose" text.
#   MEASURED (IIT_JAM_CHEMISTRY Mock 01, blueprint v1.35, axis1_figural_quota={}):
#   capable 21/5/14 by section -> 0/0/0 granted, against an Axis-1 FIGURAL budget of
#   9/3/6. A-AXIS1 would report an 18-figure shortfall on every mock of the series with
#   the generator structurally unable to comply — the permanent-failure shape v5.43
#   exists to remove, reintroduced by its own guard.
#   THIS IS THE v5.57 DEFECT ONE LAYER UP. G-FIGINK found a census that measured a
#   DECLARED extent instead of where ink landed; this is a sentinel that measured a
#   DECLARED property (the list is non-empty) instead of the actual CONTENT (the
#   schedule carries slots). Same class, same remedy: ask the artefact, not the wrapper.
#   FIX, two independent layers: (1) PRODUCER — blueprint_core.schedule_figural_slots
#   returns [] when `not any(out)`, so "no schedule" is FALSY and every caller's plain
#   truthiness test is correct by construction (a populated quota is byte-identical);
#   (2) CONSUMER — both call sites in this spec test `any(...)`, not truthiness. The DI
#   fork at S4-7 carried the identical bug by copy and is fixed in the same release; it
#   was latent only because every exam to hand has a DI budget of 0, and PASSAGE
#   inherits that fork's shape via axis1_*_by_class, so it had to be fixed before that
#   class ships. NO exam with a measured quota changes by one figure.
# v5.57 — 2026-08-20 — GAP-2026-08-20-FIGURAL-INK-CENSUS (figural_core v5.57, self-test
#   103 -> 117). A delivered paper carried a problem figure whose substituent bond ran
#   off the canvas with no label, and — found by the new gate on the same paper — FIVE
#   option canvases whose horizontal substituent bond was clipped at the frame. Every
#   Step-7 gate had passed. ROOT CAUSE, reproduced: the v5.55 fitter measures a CENSUS
#   of artists and G-FIGFIT is arithmetic over that record; the census (a) rejected
#   any artist whose extent had zero height or width — an axis-parallel bond drawn as
#   a Patch (the `ax.annotate('', xy, xytext, arrowprops)` idiom) is exactly that — and
#   (b) never looked inside an Annotation for its arrow_patch, nor at ax.artists /
#   tables / legend. Ink the census could not see was windowed out and CLIPPED, the
#   record said clearance OK, and the arithmetic gate was correct about an incomplete
#   input. The v5.55 run-report finding "gates measured declared metadata rather than
#   where ink landed" recurred one level up — at stroke PRESENCE. FIX: (1) the census
#   keeps degenerate extents (padded by stroke width) and walks Annotation arrows,
#   ax.artists, tables and legend; (2) the fit record now carries content_bbox_px /
#   axes_bbox_px / axis_on; (3) NEW Q13 gate G-FIGINK (BLOCKING on v5.57+ axis-off
#   renders; W-FIGINK AMBER on axis-on renders and, in its frame-edge form, on LEGACY
#   framed canvases — the form that found the five shipped options without a
#   re-render). Q10's "arithmetic, not pixels" stands: G-FIGINK asks only whether ink
#   lies OUTSIDE the measured box, a question the extent bias cannot false-positive.
# v5.56 — 2026-08-19 — GAP-2026-08-19-LEARNINGS-FILENAME-SEAM (paired with Blueprint
#   v1.50.0). The GAP-07 learnings load read {EXAM}_ExplainLearnings.md — the legacy
#   name Blueprint Step 6 generated — while Step 9's loader globs
#   [ExamCode]_EXPLAIN_LEARNINGS_v*.md (S24 schema). One file, three names estate-wide:
#   the Step-6 stub never reached Step 9, and an exam adopting the correct versioned
#   name silently lost THIS step's load. FIX: S1's copy and S3's load now glob
#   {EXAM}_EXPLAIN_LEARNINGS_v*.md and read the HIGHEST version (same rule as
#   parse_learnings); the BANNED:/VERIFIED DEFECT: extraction is unchanged (an EX-rule
#   author may include those markers for Step-7 enforcement; S24 prose fields are
#   Step-9 authoring guidance, not generation bans). A project carrying ONLY the
#   legacy-named file still loads it, with a printed one-line migration warning to
#   rename — loud, never silent (§16 exam-agnostic mandate: the convention is single;
#   the legacy path exists only to not strand pre-v5.56 projects mid-series).
# v5.55 — 2026-08-19 — GAP-2026-08-19-FIGFIT: FIGURE LAYOUT IS NOW MEASURED, NOT ASSUMED
#   Every figure gate from v5.33 to v5.54 measured METADATA — canvas pixels, DPI,
#   placement scale, REQUESTED font points, DECLARED hues, alt text. Nothing measured
#   WHERE THE INK LANDED. Measured on the reference delivery (IIT_JAM_CHEMISTRY Mock01,
#   42 drawings): 3 of 24 option canvases carried ink OUTSIDE the drawn frame (worst
#   4.06% of the image's ink); 10 of 24 had content within 12 px (0.04 in) of it, some
#   with a white label bbox punching a visible hole THROUGH the border stroke; two
#   option canvases printed CH3 on top of CH3; the frame occupied 252 of 390 canvas px
#   (64.6% of width) and the median problem figure's ink covered 29.6% of its canvas,
#   so ~70% of every figure's page allocation was white space; and one portrait
#   structure used 33% of its canvas width against 97% of its height inside the
#   hardcoded 0.72 landscape aspect. EVERY ONE OF THOSE FIGURES PASSED EVERY GATE.
#   ROOT CAUSE IS ARCHITECTURAL. draw_fn is authored per question at generation time,
#   so layout correctness was delegated to hand-written drawing code, once per
#   question, across ~200 exams, with no safety net and no measurement. Authoring
#   discipline does not scale to that; a renderer-side invariant does.
#   THE FIX, in four parts: (1) S10-7 Q10 FIT CONTRACT — the renderer measures every
#   artist's rendered extent and fits the data window so all ink clears the frame by
#   FIG_MIN_CLEARANCE_IN; (2) S10-7 Q11 LABEL DECONFLICT — measured label repulsion,
#   capped so a label is never silently dragged off the atom it names, with a bounded
#   ring-expansion escalation; (3) S10-7 Q12 + S10-8 — an option SET renders in ONE
#   shared window on ONE canvas via render_option_set(), and the FRAME belongs to the
#   renderer, drawn last above every artist, at the canvas edge; (4) S10-7C — a domain
#   drawing contract, because a layout engine cannot separate labels that are
#   superimposed by definition (eclipsed Newman) and must not pretend otherwise.
#   New gates: G-FIGFIT (BLOCKING on v5.55+ output, AMBER for legacy under EC-V18),
#   G-FIGCOLLIDE (VOID_ITEM), G-FIGOPTWINDOW (VOID_ITEM), W-FIGFITPX (AMBER, and the
#   only one auditable from a delivered .docx with no sidecar — which is what makes
#   ~200 existing exams auditable without re-rendering them).
# v5.54.1 — 2026-08-13 — SYNC AUDIT ROUND 2: three prose desyncs fixed (no logic change)
#   (1) S13-6 + DoD said "EXACTLY TWO files", contradicting the dossier-conditional 3-file
#   closed set R-DELIVER/S13-7/G-DELIVERY-SET already agree on; both sites now state the
#   derived set. (2) S13-6's file list showed the literal Mock[N] name; now slug-form,
#   matching S13-7/S13-4b. (3) The trigger-contract [N] rule said "must ≤ total_mocks/
#   n_papers" — wrong for offset-resumed blueprints (apply_mock_offset relabels mocks[].mock
#   beyond total_mocks); the binding check is mocks[] MEMBERSHIP, now stated correctly.
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
#     WARN (not HARD STOP) + manual checklist — but the warning must state explicitly,
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
hash-tracked in MANIFEST.json — never hand-maintained here. Read ranges with
`sed -n 'START,ENDp'` in bash (the view tool truncates ~16,000 chars per call;
SPEC_SECTIONS.json records both stride constants). `bootstrap.py --trigger MockCreate`
(or TestCreate) prints the class, both read budgets and the skipped sections; pass
`--progress [ExamCode]_M[N]_batch_state.json` so the class is decided from the frozen
plan rather than defaulting.

WHAT THIS DOES NOT CHANGE. Not one byte of any artefact: the same questions, the same
gates, the same batch deliveries, the same Final Assembly. It moves the CLOSING
sections off the per-batch execution path — it does not shrink, soften or delete them.
```

## S1-1 — Pipeline position

  Step 5 (PYQExtract)  → produces [ExamCode]_section_rules.md
  Step 6 (MockBlueprint) → produces [ExamCode]_blueprint.json,
                               [ExamCode]_registry.json (empty template),
                               [ExamCode]_EXPLAIN_LEARNINGS_v1.md,
                               [ExamCode]_mock_test_audit.py
  THIS STEP — Step 7 (MockCreate) → produces [ExamCode]_Mock[N]_Create.docx,
                               updated [ExamCode]_registry.json
  THIS STEP, repair mode (§S16, TestCreateRepair) → [ExamCode]_Mock[N]_Create_Repaired.docx,
                               updated [ExamCode]_registry.json (pre-repair snapshot)
  REGISTRY-HANDOFF-LAW (v5.73): every step that CHANGES registry.json DELIVERS it, badge
  "Replace in Project Files", in the same present_files call as its primary artefact —
  decided by pp.registry_changed (a fingerprint), never by prose. Steps 7, 7-repair, 9,
  9-repair are the writers; Step 11 reads it. LAW_REGISTRY.json / mock_sync_audit MS-14.
  Step 9 (MockExplain) → consumes outputs of this step (v5.36: directly — the former
                               Step 8 audit between them has been retired)

  PREREQUISITE: Step 0 AND Step 1 must both be complete.
  section_rules.md AND blueprint.json must both be in project knowledge.

## S1-2 — Sources of truth (strict priority order)

  Priority 1: This spec (Framework_MockTestCreate.md)
  Priority 2: [ExamCode]_blueprint.json  — allocation, format, structure
  Priority 3: [ExamCode]_section_rules.md — subtopic rules, templates, patterns
  Priority 4: [ExamCode]_registry.json   — cross-mock dedup state

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
    PickError and Claude HARD STOPS with its actionable message (does not guess).
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

  R1:  Never copy PYQ verbatim or near-verbatim.
  R2:  No question repeated across mocks (registry dedup L1-L18).
  R3:  No image reused across any 2 questions (dHash + MD5).
  R4:  Every question has exactly 4 unique options (unless options_count≠4).
       — v4.7 NAT EXEMPTION: a NAT question (answer_type=='numerical') has ZERO options.
         R4 does not apply to it; option-count is governed by G-NAT-NOOPT instead.
  R5:  No answer key, correct marker, or hint anywhere in the paper.
       — INCLUDES: no answer key page at end of docx
       — INCLUDES: no asterisk, no bold correct option, no "correct" annotation
       — DETECTION: scan docx for "Answer Key", "Answers:", "Key:", "Q\.\d+.*→.*[1-4]"
       — HARD STOP if found: do not deliver until removed.
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
       — HARD STOP. Detection: scan all body paragraphs (a header may sit before the first Q
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
       — HARD STOP. Detection: scan every paragraph before the first "Q.<N>" stem, before and
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
  R-DELIVER (v5.36, HARD STOP): Step 7 delivers EXACTLY the CLOSED SET at Final
       Assembly and NOTHING else. The set is the CLOSED pair below (v5.73):
         1. [ExamCode]_Mock[N]_Create.docx        — always (scoped slug for a scoped paper)
         2. [ExamCode]_registry.json              — always (Replace in Project Files)
       "EXACTLY" is the operative word in BOTH directions: nothing missing and
       nothing extra. The Tier-A audit dossier ([ExamCode]_M[N]_audit_dossier.json)
       is INTERNAL from v5.73 (operator decision 2026-08-26): S13-4b writes it to
       /home/claude and S13-4c reads it there; staged in outputs it is a LEAK
       (final_assembly.predelivery_checklist check 5). Because the set no longer
       varies, the v5.35/v5.36/v5.54.1 count-drift class cannot recur. Producing a standalone answer-key file (any format:
       .docx/.pdf/.json/.txt) as a deliverable is forbidden with the same force
       as R5 (no answer key in the paper). Internal sidecars (answer_key.json,
       fig_manifest.json, batch_state.json, progress.json, audit_dossier.json) are NEVER delivered.
       The learner-facing answer key is a Step-4 (MockExplain) artefact, not
       a Step-7 one. Enforced by S13-6, S13-7, and gate G-DELIVERY-SET.
  R-LINKED (v3.6, HARD STOP): Every question must be SELF-CONTAINED for
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
       — Q.N-FIRST (v3.7, HARD STOP): every question block — single OR linked —
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
  R-FIGURAL (v4.0, HARD STOP): Every figural MCQ must be DECOMPOSED, not a
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
  R-UNDERLINE (v4.1, HARD STOP): Every question that asks about an UNDERLINED
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
  R-OPTREF (v4.2, HARD STOP): A stem may not REFERENCE a terminal/escape option
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
  R-ANSWER (v4.5, HARD STOP at generation — generalises v4.2 R-UNIQUE; single source
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
           (k=0 "empty" and k=n "all-correct" are HARD-STOP defects by default);
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
           figure, missing unit) is a HARD-STOP defect — DISAMBIGUATE the stem;
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
  HARD-STOP defect on the QUESTION, not a formatting bug — DISAMBIGUATE/rework the stem's
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
  R-MATH-OMML (v4.3, HARD STOP): Every algebraic/symbolic expression that
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

  /mnt/project/ (read-only) → /home/claude/ (working dir)
  /mnt/user-data/outputs/ (delivery)

  ```python
  import shutil, os, json, re, glob
  from pathlib import Path
  EXAM = "[ExamCode]"  # from trigger

  # Ledgers — session state (RULE B / RULE C). Initialised EMPTY here at session
  # start, exactly as the §6-3 contract states; persisted to batch_state.json
  # after every batch (S4-8a) and REHYDRATED by S4-12 step 4b on resume. The
  # init is IDEMPOTENT (globals().get) so re-reading this fence after an S4-12
  # rehydration cannot wipe a resumed session's state. Previously these two
  # names were read in S4-8a/S4-12/§6-3 but bound NOWHERE
  # (GRANDFATHERED_MUST_FIX, fixed v5.62).
  mock_scenario_ledger     = globals().get('mock_scenario_ledger', set())
  mock_presentation_ledger = globals().get('mock_presentation_ledger', set())

  # MANDATORY COPIES (non-blueprint) — HARD STOP if any missing:
  required = [
      f'{EXAM}_registry.json',
      f'{EXAM}_section_rules.md',
      f'{EXAM}_subtopic_manifest.json',   # v3.4 — cross-step contract (REQUIRED)
  ]
  for f in required:
      src = f'/mnt/project/{f}'
      if not os.path.exists(src):
          raise SystemExit(f"HARD STOP: {f} not found in project knowledge. "
                           f"Upload it to [{EXAM}] project Files, then retry.")
      shutil.copy(src, f'/home/claude/{f}')

  # BLUEPRINT DISCOVERY (v5.28, paper_pipeline.py): copy EVERY [ExamCode]*_blueprint.json
  # present in project knowledge — the mock blueprint ([ExamCode]_blueprint.json) AND any
  # scoped blueprints ([ExamCode]_[SCOPETAG]_blueprint.json from ScopedBlueprint). §3 S3-2
  # (pp.pick_blueprint) decides which ONE of these this trigger actually generates from.
  blueprint_srcs = sorted(glob.glob(f'/mnt/project/{EXAM}*_blueprint.json'))
  if not blueprint_srcs:
      raise SystemExit(f"HARD STOP: no {EXAM}*_blueprint.json found in project knowledge. "
                       f"Run MockBlueprint or ScopedBlueprint first, then retry.")
  BLUEPRINT_PATHS = []
  for src in blueprint_srcs:
      fname = os.path.basename(src)
      shutil.copy(src, f'/home/claude/{fname}')
      BLUEPRINT_PATHS.append(f'/home/claude/{fname}')

  # OPTIONAL — audit script (Layer 2 guard — not required for Layer 1):
  audit_py = f'/mnt/project/{EXAM}_mock_test_audit.py'
  AUDIT_AVAILABLE = os.path.exists(audit_py)
  if AUDIT_AVAILABLE:
      shutil.copy(audit_py, f'/home/claude/{EXAM}_mock_test_audit.py')
  else:
      print(f"NOTE: {EXAM}_mock_test_audit.py not found in project. "
            f"This file is auto-generated by Step 6 (MockBlueprint) v1.20+. "
            f"Verify Step 6 outputs were uploaded to project Files. "
            f"Layer 1 batch enforcement (spec-level STOP) will be used. "
            f"Manual gate checklist (S4-11) will replace script gates.")

  # OPTIONAL — figural manifest from prior session:
  fig_src = f'/mnt/project/{EXAM}_fig_manifest.json'
  if os.path.exists(fig_src):
      shutil.copy(fig_src, f'/home/claude/{EXAM}_fig_manifest.json')

  # OPTIONAL — EXPLAIN_LEARNINGS (v2.0 GAP-07 fix; v5.56 filename seam fix):
  # One name estate-wide: {EXAM}_EXPLAIN_LEARNINGS_v*.md (S24 convention, highest
  # version wins — same rule as Step 9's parse_learnings). Legacy-named file
  # loads with a MIGRATION warning; never silently ignored.
  import glob
  learn_srcs = sorted(glob.glob(f'/mnt/project/{EXAM}_EXPLAIN_LEARNINGS_v*.md'))
  legacy_src = f'/mnt/project/{EXAM}_ExplainLearnings.md'
  if learn_srcs:
      shutil.copy(learn_srcs[-1], f'/home/claude/{os.path.basename(learn_srcs[-1])}')
  elif os.path.exists(legacy_src):
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
      raise SystemExit(f"HARD STOP: {e}")

  # v5.29 SAFETY CHECK: the {EXAM}*_blueprint.json glob (S3-1) is a PREFIX match — if a
  # different ExamCode's files were ever uploaded into this same project (e.g. "SSC_CGL"
  # vs "SSC_CGL_TIER1"), the glob could sweep in a blueprint that isn't this exam's. The
  # exact-filename match this replaced made that structurally impossible; the glob does
  # not, so it must be checked explicitly rather than trusted implicitly.
  if bp['exam_code'] != EXAM:
      raise SystemExit(
          f"HARD STOP: selected blueprint's exam_code {bp['exam_code']!r} does not "
          f"match the trigger's ExamCode {EXAM!r}. A blueprint file from a different "
          f"ExamCode may have been picked up by the {EXAM}*_blueprint.json glob (S3-1) "
          f"— check this project for a similarly-prefixed ExamCode's files.")

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
          raise SystemExit(f"HARD STOP: {e}")
  # v5.65: the former bp.get('option_label_format') tier is REMOVED — no writer
  # emits that blueprint key (Blueprint §14 writes option_label, visibility-only),
  # so the tier could never fire; chain: exam_config -> section_rules -> default.
  # v5.66 (GAP-2026-08-23-ECFG-LABEL-PARITY) — THE OVERRIDE GOES THROUGH THE
  # SAME RESOLVER. Family is derived from the resolved template's TOKEN (never
  # from option_label_family on a template string — its pass-through branch
  # falls back to 'num' for alpha/roman templates) and asserted equal to the
  # family the auditor will classify from section_rules (or its '1/2/3/4'
  # default when section_rules declares no label). Refuse at PRE-GENERATION —
  # a guessed label reaches the delivered paper; this HARD STOP happens before Q1.
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
          raise SystemExit(f"HARD STOP: {e}")
      _ecfg_family = _label_family_of_template(_ecfg_label)
      if _ecfg_family is None:
          raise SystemExit(
              "HARD STOP (ECFG-LABEL PARITY): exam_config option_label_format "
              f"{_ecfg.get('option_label_format')!r} resolves to a template with no "
              "recognised label token ({i}/{alpha_*}/{roman_*}) — it cannot be "
              "rendered or audited. Declare a supported notation or template.")
      _audit_family = _resolved_family or 'num'
      if _ecfg_family != _audit_family:
          raise SystemExit(
              "HARD STOP (ECFG-LABEL PARITY): exam_config option_label_format "
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
      raise SystemExit(f"HARD STOP: Mock {N} not found in blueprint.json mocks[].")

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
          # will HARD STOP; do not silently fall back to name matching.
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
  if diff_entry and len(difficulty_labels) == 3:
      _dcounts = {'simple': n_simple, 'medium': n_medium, 'hard': n_hard}
      _dshort = bc.difficulty_feasibility(_dcounts, _qtype_by_q, difficulty_labels)
      if _dshort:
          _lab, _d = next(iter(_dshort.items()))
          raise SystemExit(
              f"HARD STOP (S3 difficulty feasibility, v5.60): the schedule asks for "
              f"{_d['requested']} '{_lab}' questions but this exam's shape can honestly "
              f"hold at most {_d['max_achievable']} — the shared rubric's qtype floor "
              f"makes '{_lab}' unreachable on MSQ/NAT positions (an options-free or "
              f"choose-all mechanic is never bottom-band work). Re-run Step 6 with "
              f"'{_lab}' <= {_d['max_achievable']} for this mock (any Medium/Hard "
              f"split is unrestricted), or drop position-based typing. Do NOT relabel "
              f"around this.")
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
          try:
              difficulty_plan = bc.assign_difficulty_bands_by_section(
                  _by_sec, _qtype_by_q, _ecfg.get('sections'), difficulty_labels, seed=N)
          except bc.DPError as _e:
              raise SystemExit(f"HARD STOP (S3 per-section difficulty plan, v5.75): {_e}")
      else:
          difficulty_plan = bc.assign_difficulty_bands(_dcounts, _qtype_by_q,
                                                       difficulty_labels, seed=N)
      difficulty_plan = {q: lab for q, lab in difficulty_plan.items()}
      # v5.75: the profile for CHECK 3c calibration examples — optional, validated
      import os as _os, json as _json
      _pf_p = f'/mnt/project/{EXAM}_difficulty_profile.json'
      PROFILE_CFG = {'exam_code': EXAM, 'total_questions': total_questions,
                     'sections': _ecfg.get('sections'), 'cycle_gap_days': _ecfg.get('cycle_gap_days'),
                     'difficulty_labels': difficulty_labels}
      DIFFICULTY_PROFILE = None
      if _os.path.exists(_pf_p):
          try:
              DIFFICULTY_PROFILE = bc.dp_check_profile(_json.load(open(_pf_p, encoding='utf-8')),
                                                       EXAM, difficulty_labels)
          except bc.DPError as _e:
              raise SystemExit(f"HARD STOP (S3 difficulty profile, v5.75): {_e}")
      # Persisted as batch_state.json['difficulty_plan'] = {str(q): label} alongside
      # the rest of the S3 state (same write, same file) so `continue` resumes the
      # identical plan and the CHECK 3c band-swap escape can update it in place.
  # DORMANT (difficulty_plan is None) when the exam declares no difficulty_schedule
  # entry for this mock OR a non-3-band vocabulary — the documented fall-through of
  # every Cluster-E2 function. Dormant means: no plan, no G-DIFF, labels assigned
  # exactly as pre-v5.60 (and A-QINDEX checks 7/8 stay proportionate: 7 needs a
  # marking_scheme, 8 needs recorded obs).
  ```

  LOAD EXPLAIN_LEARNINGS for quality constraints (GAP-07 fix; v5.56 filename seam fix):
  ```python
  learnings_bans = []  # Extra banned patterns from prior Explain sessions
  import glob
  _lf = sorted(glob.glob(f'/home/claude/{EXAM}_EXPLAIN_LEARNINGS_v*.md')) \
        or [f'/home/claude/{EXAM}_ExplainLearnings.md']   # legacy fallback (S1 warned)
  for learn_file in [_lf[-1]]:
      if os.path.exists(learn_file):
          content = open(learn_file, encoding='utf-8').read()
          # Extract explicit BANNED/VERIFIED DEFECT markers (an EX-rule author may
          # include them for Step-7 enforcement; S24 prose fields are Step-9 guidance)
          bans = re.findall(r'(?:BANNED|VERIFIED DEFECT):\s*(.+)', content)
          learnings_bans.extend(bans)
  # learnings_bans added to quality gate checks during generation
  ```

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

## S3-6 — ExamCode cross-verification

  ```python
  bp_code  = bp['exam_code']
  reg_code = reg.get('exam_code', bp_code)
  assert bp_code == EXAM, \
      f"HARD STOP: trigger ExamCode '{EXAM}' != blueprint '{bp_code}'"
  assert bp_code == reg_code, \
      f"HARD STOP: blueprint exam_code '{bp_code}' != registry '{reg_code}'"
  ```

## S3-7 — Blueprint version compatibility check

  ```python
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
          f"HARD STOP: blueprint_version '{blueprint_version}' < minimum "
          f"'{'.'.join(str(x) for x in MIN_BLUEPRINT_VERSION)}'. "
          f"Regenerate the blueprint with Framework_Blueprint v1.7+ (subtopic_id contract required).")
  ```

## S3-8 — Subtopic join via subtopic_id (v3.4 — CONTRACT GATE, replaces string-match)

  v3.4 CHANGE: Step 7 no longer matches subtopics by display-name string. It
  joins blueprint ↔ section_rules ON subtopic_id, the stable key minted by Step 0.
  This permanently fixes the ~70% name-mismatch that caused false "subtopic
  unrecognised" and false "mandatory subtopic absent" hard stops.

  ```python
  # Load the Step 0 manifest (authoritative id registry). REQUIRED.
  manifest_path = f'/home/claude/{EXAM}_subtopic_manifest.json'
  if not os.path.exists(manifest_path):
      # Try project dir as a fallback location
      alt = f'/mnt/project/{EXAM}_subtopic_manifest.json'
      if os.path.exists(alt):
          shutil.copy(alt, manifest_path)
  if not os.path.exists(manifest_path):
      raise SystemExit(
          f"HARD STOP (S3-8 contract): {EXAM}_subtopic_manifest.json not found. "
          f"Step 0 publishes it and the user uploads it to the {EXAM} project "
          f"Files section alongside section_rules.md. Upload it, then retry.")
  manifest = json.load(open(manifest_path, encoding='utf-8'))
  MANIFEST_IDS = manifest['subtopics']           # id -> {display_name, section, ...}

  # Build the section_rules id index: parse subtopic_id: from each block.
  # (Step 0 v2.4+ writes 'subtopic_id:' as the first field of every block.)
  sr_block_ids = set(re.findall(r'^subtopic_id:\s*(\S+)\s*$', sr_text, re.MULTILINE))

  # CONTRACT GATE — every blueprint id must exist in BOTH the manifest AND
  # section_rules. A missing id = HARD STOP naming the exact id (no silent fallback).
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
          "HARD STOP (S3-8 contract): this blueprint has subtopic_allocations "
          "without 'subtopic_id'. It predates the v1.7 contract. Regenerate the "
          "blueprint with Framework_Blueprint v1.7+ (which reads the Step 0 "
          "manifest and emits subtopic_id), OR run the one-time migration to add "
          "ids. Step 7 will not string-match — it requires ids.")
  if contract_failures:
      raise SystemExit(
          "HARD STOP (S3-8 contract): these blueprint subtopic_ids are not "
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

## S3-9 — Section allocation sum verification

  ```python
  for section in sections:
      sec_name = section['name']
      expected = section['total_qs']
      actual   = sum(allocations.get(sec_name, {}).values())
      if actual != expected:
          raise SystemExit(
              f"HARD STOP: Section '{sec_name}' allocations sum={actual}, "
              f"expected={expected}. Blueprint may be corrupt or wrong mock.")
  ```

## S3-10 — Audit script self-test (Layer 2 — when audit.py exists)

  ```python
  if AUDIT_AVAILABLE:
      import subprocess
      result = subprocess.run(
          ['python3', f'/home/claude/{EXAM}_mock_test_audit.py', '--self-test'],
          capture_output=True, text=True
      )
      if result.returncode != 0:
          raise SystemExit(
              f"HARD STOP: Audit script self-test failed.\n{result.stdout}\n{result.stderr}")
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
  points to a nonexistent subtopic_id → HS-16 HARD STOP:
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

## S3-13 — Build answer position budget (PRE-Q1 — v2.0 GAP-08 fix)

  CRITICAL: Budget MUST be built before Q1, not post-generation.
  Assign answer positions for ALL N questions before generating any content.

  ```python
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
  # false ⇒ build_answer_budget behaves exactly as v4.4. Defensive: if the placement plan
  # is not yet materialised at budget-build time, msq_positions stays empty and the MSQ
  # builder simply does not consume its budget slot (it self-assigns the set), so K-BAL/
  # K-PAT are never corrupted by a multi Q either way.
  msq_positions = set()
  if multi_present:
      if _position_based_typing:
          # v5.X: for position-based exams, MSQ positions come from marking_scheme Q-ranges,
          # not from per-subtopic answer_cardinality. Every Q in an MSQ range is MSQ regardless
          # of which subtopic is placed there.
          msq_positions = {q for q in range(1, total_questions + 1) if _type_for_q(q) == 'MSQ'}
      else:
          multi_ids = {sid for sid, am in answer_cardinality_by_id.items() if am == 'multi'}
          try:
              # subtopic_by_qnum[q] = subtopic_id assigned to Q q (same map fixed_positions uses)
              msq_positions = {q for q, sid in subtopic_by_qnum.items() if sid in multi_ids}
          except NameError:
              msq_positions = set()   # plan not materialised yet → MSQ Qs self-skip the budget
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
          try:
              nat_positions = {q for q, sid in subtopic_by_qnum.items() if sid in nat_ids}
          except NameError:
              nat_positions = set()   # plan not materialised yet → NAT Qs self-skip the budget
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

## S3-16 — Build batch plan → write batch_state.json

  ```python
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
      'total_questions': total_questions,
      'batch_plan': batch_plan,
      'batches_completed': [],
      'current_batch': 1,
      'mechanics_used': {},
      'templates_used': {},
      'rotation_state': {},
      'passage_linked_qs': [],
      'cloze_linked_qs': [],
      'concept_ledger': [],          # v5.4 FIX: was missing from init (present in S4-3 schema)
      'presentation_ledger': [],     # v5.4 FIX: was missing from init (present in S4-3 schema)
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
          "HARD STOP (S3-17): blueprint mandate/alternation violations for Mock "
          f"{N}:\n  - " + "\n  - ".join(problems) +
          "\n\nThese are BLUEPRINT defects (Step 1 should prevent them at build "
          "time under Framework_Blueprint v1.11 RULE M1/M2/M4/M5/M6). Fix: "
          "regenerate the blueprint with v1.11 (enforces mandates by construction), "
          "or correct this mock's allocation, then retry. Step 7 does not auto-edit "
          "the blueprint.")
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

  ADVISORY ONLY — never a HARD STOP, mirroring `axis1_feasibility`'s own established
  contract exactly ("Subtopic is hard #1"; Axis-1/Axis-3 are locked CONSEQUENCES of
  allocation, steered and audited within tolerance, never force-blocking on it).
  Absent-safe: no `axis_schedule` (pre-v1.23 blueprint), a section whose status isn't
  'ok', or no target for an axis ⇒ silently skipped for that axis/section,
  byte-identical to every exam that predates this.

  ```python
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
  whose section_rules format == FIGURAL. For each, read image_role from
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
  The Q# assignment is determined by the subtopic's position within the
  section's Q-range (subtopics assigned to Q positions in blueprint order).
  This manifest is INFORMATIONAL — the authoritative format source remains
  section_rules format field per subtopic_id.
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

## S3-19 — HARD STOP conditions

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
        Non-blocking WARN (not HARD STOP): figural_present may be series-level
        — this specific mock simply has no figural Qs while others in the series do.
  HS-15a: (v5.13 REVERSE) figural_present is False but ≥1 subtopic in this mock
        has section_rules format==FIGURAL. The blueprint flag is wrong — should be
        True. Non-blocking WARN: the FORMAT DISPATCH (S4-7) and G-FIGTEXT (S12-NEW-5)
        still operate independently of figural_present and will attempt image
        generation. But the FIGURAL MANIFEST (S3-18) and CHECK 5 (S4-5) will be
        skipped, reducing early warning. Fix blueprint.json for the next series.
  HS-16: (v5.13) FIGURAL_BANNED subtopic has no valid REPLACEMENT_RULE. See S3-11.
        HARD STOP — S7-NEW-B OPTION B replacement will fail silently without it.


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

  B-7: present_files is FORBIDDEN until the batch passes gate checks
       (Layer 2 audit script exit 0, OR Layer 1 manual checklist all-pass).

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
             If figural_present is False: skip CHECK 5 silently.

  Only after all 5 checks pass does generation begin.

## S4-6 — The continue contract (exact behaviour)

  ACCEPTED CONTINUE TRIGGERS (case-insensitive, trimmed):
    "continue", "go", "next", "continue.", "go ahead", "next batch", "proceed"

  IF the user message IS a continue trigger:
    → Run S4-5 pre-batch self-check.
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
           Write them to the cumulative docx (append to prior batches' Qs).
           Write each question's answer to the sidecar immediately (S11-2).
           Apply ALL generation rules (§7), format rules (§8, §10),
           dedup (§6), self-containment (§9).

           FORMAT DISPATCH (v5.13 — per question, mandatory decision point):
             Read the subtopic's format from section_rules (by subtopic_id).
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

               profile = bc.figural_generation_profile(pyq_image_analysis)

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
               → Record figural_qs[str(qnum)].object_type = the type this figure was
                 generated AS, drawn from profile['dominant'] / profile['observed']
                 (omit when mode == 'unconstrained'). audit.py A-FIGPROFILE audits this
                 recorded intent against the same profile via the SAME engine function,
                 bc.check_figural_conformance — one rule, so the generator and its
                 auditor cannot drift apart.
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

  STEP B — GATE CHECK:
           If AUDIT_AVAILABLE: run audit script on cumulative docx → capture STDOUT.
           If NOT: run the Manual Gate Checklist (S4-11).
           If any fixable WARN/FAIL: fix it, re-run. Iterate to clean.
           present_files is FORBIDDEN until clean (B-7).

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

## S4-11 — Manual Gate Checklist (Layer 1 — used when audit.py absent)

  When AUDIT_AVAILABLE is False, Claude runs these checks itself before
  each batch delivery. All must PASS before present_files.

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
                  semantic object per role; STRUCTURE/REACTION roles rendered via
                  corpus_io.structure_draw_fn (S7-NEW-B2).
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
  [ ] G-CLUSTER:  No two same-CONCEPT_GROUP Qs adjacent; no contiguous run > 2
                  from one PRESENTATION_FAMILY; each subtopic's N Qs spread across
                  its section, not stacked. (R19 v3.8)
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

  All 43 items must PASS. If any FAIL: fix in this batch, re-check, then deliver.
  ```

## S4-12 — Session recovery / resume (v3.0)

  TRIGGER: MockCreate M[N] resume
  OR: batch_state.json indicates an incomplete mock (batches_completed not full).

  RECOVERY PROCEDURE:
    1. Load batch_state.json. Read current_batch and batches_completed.
    2. If batch_state.json is missing:
         - Load the most recent cumulative docx for Mock N.
         - Count Q paragraphs to find last completed Q number.
         - Map last Q to its batch using the freshly-rebuilt batch_plan.
         - Set current_batch = that batch + 1; batches_completed accordingly.
         - Rewrite batch_state.json.
    3. Load the existing cumulative docx as the base (do NOT regenerate prior Qs).
    4. Load answer_key.json (has all prior answers).
    4b. REHYDRATE THE LEDGERS (v3.9 G3 — mandatory, else resume can clone):
        mock_scenario_ledger     = set(bs.get('concept_ledger', []))
        mock_presentation_ledger = {tuple(s.split('||', 1))
                                    for s in bs.get('presentation_ledger', [])}
        If batch_state.json was missing (step 2), rebuild BOTH ledgers from the
        answer_key concept_map instead (scenario_key values, and (concept_group,
        presentation_key) pairs for every CLASS-2/3 question). Without this, RULE B
        and RULE C are blind to everything generated before the interruption.
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
    S7-CONCEPT asserts it is present before generating; absence is a HARD STOP
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
        bc.difficulty_authoring_profile(band, qtype, difficulty_labels) names the
        class facets, deduction-step range and concept count that provably land
        in the band — write the question AND its solution inside that profile
        (a bottom-band slot is recall/one-principle and NEVER computational or
        figural; a top-band slot is a genuinely long or multi-concept
        derivation — more Hard in the trigger means AUTHORING harder questions,
        never renaming easier ones).
        While deriving the answer for the sidecar (the derivation already
        happens — §S7-NEW-A), RECORD the observations the derivation revealed:
          difficulty_obs = {'question_class': [facet, ...],   # incl. C-FIGURAL
                            'deduction_steps': <int>,          # steps actually needed
                            'axiom_concepts': <int>,           # distinct principles
                            'speed_hack_exists': <bool>,
                            'is_negative': <bool>,             # NOT/EXCEPT polarity
                            'qtype': 'mcq'|'msq'|'nat'}
        Count honestly — steps a competent candidate needs, not padding; the
        count is evidence, and A-QINDEX check 8 re-runs the same arithmetic on
        it forever.
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
        THE GATE: ok, measured = bc.verify_difficulty_obs(difficulty_plan[q],
        difficulty_obs, difficulty_labels). If not ok:
          → REJECT. Regenerate TOWARD the band using the profile (add or remove
            derivation load; change class facets). Bound: MAX_DIFF_TRIES = 6
            per slot, counted separately from MAX_SCENARIO_TRIES.
          → BAND-SWAP ESCAPE (after MAX_DIFF_TRIES): if another not-yet-accepted
            slot q' exists in the SAME section with difficulty_plan[q'] ==
            measured and difficulty_min_band allows this slot's band at q',
            swap the two plan entries (quota unchanged, floors re-checked) and
            accept; update batch_state['difficulty_plan']. Otherwise HARD STOP
            naming q, the band, the measured label and the six profiles tried —
            never accept a question whose label its own evidence contradicts.
        On ACCEPT: pass difficulty=difficulty_plan[q] AND difficulty_obs to
        write_q_to_sidecar — the label and its evidence travel together into
        registry.question_index (S13-4) and are what A-QINDEX checks 7/8 and
        Step 9's advisory re-measure (TestExplain §7A-M) verify downstream.

        THE GATE, executable (called once per slot when difficulty_plan is set;
        `diff_tries` is the batch_state.json['_diff_tries'] dict, persisted with
        the rest of the S3 state):
        ```python
        def g_diff_gate(q, band, qtype, difficulty_obs, difficulty_labels,
                        diff_tries):
            """Returns 'ACCEPT' | 'RETRY' | 'SWAP_OR_STOP' for this candidate."""
            import blueprint_core as bc          # S1-2b engine (already on sys.path)
            MAX_DIFF_TRIES = 6
            profile = bc.difficulty_authoring_profile(band, qtype,
                                                      difficulty_labels)
            # profile is None ONLY for a bottom-band MSQ/NAT slot, which the S3
            # plan can never produce (floors) — None here means the plan was
            # modified outside bc.assign_difficulty_bands: a tamper HARD STOP,
            # never a skip.
            if profile is None:
                raise SystemExit(f"HARD STOP (G-DIFF, v5.60): no authoring "
                                 f"profile for band {band!r} at Q{q} ({qtype}) "
                                 f"— rebuild the difficulty_plan.")
            # (the candidate was authored INSIDE `profile`, its answer derived,
            #  and difficulty_obs recorded from that derivation — shape above)
            ok_d, measured = bc.verify_difficulty_obs(band, difficulty_obs,
                                                      difficulty_labels)
            if ok_d:
                return 'ACCEPT'
            diff_tries[str(q)] = diff_tries.get(str(q), 0) + 1
            if diff_tries[str(q)] < MAX_DIFF_TRIES:
                return 'RETRY'          # regenerate toward `band`, per profile['note']
            return 'SWAP_OR_STOP'       # band-swap escape, else HARD STOP (rules above)
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
  parity table. It carries NO mutual-exclusion HARD STOP. It mirrors S3-17's
  contract: read structured policy from config (manifest + section_rules) by
  subtopic_id; if the config declares nothing, this is a no-op (never a stop).

  READ FROM batch_state.json rotation_state{} — not from memory.

  ── A. MUTUAL EXCLUSION (members must NOT co-occur in one mock) ──
    NOT enforced here. This invariant is owned SOLELY by S3-17, which reads
    manifest.alternation_groups by subtopic_id BEFORE generation and HARD STOPs
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

## S7-NEW-A — Per-question answer key sidecar write (v2.0 GAP-18 fix; v3.3 concept map; v5.52 mandatory concept_map)

  IMMEDIATELY after each question is accepted and added to docx:
  ```python
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
                          subtopic_id, difficulty, difficulty_obs):
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
  figural_slots = bc.schedule_figural_slots(
      (axis_schedule.get(sec_name) or {}).get('axis1_figural_quota') or {},
      (axis_schedule.get(sec_name) or {}).get('axis1_target_series') or [],
      bc.figural_band(
          (axis_schedule.get(sec_name) or {}).get('axis1_target_per_mock', {}).get('FIGURAL', 0),
          (axis_schedule.get(sec_name) or {}).get('axis1_observed_figural')),
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

  ordered = bc.rank_figural_candidates(
      figural_capable_slots,                      # [(qnum, subtopic_id), ...]
      rates={sid: SR[sid].get('figural_rate', 0.0)      for sid in capable_ids},
      reducible={sid: SR[sid].get('figural_reducible', True) for sid in capable_ids})

  for qnum, sid in ordered:
      granted, why = bc.axis_grant_figural(
          axis1_trackers[sec_name], sid,
          reducible=SR[sid].get('figural_reducible', True))
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
    DECOMPOSITION MANDATE (R-FIGURAL — HARD STOP): a figural MCQ is rendered as
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
    Nothing in between. HARD STOP if a text placeholder is found before delivery.

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
  STRUCTURE / REACTION FIGURES ARE RENDERED FROM THEIR CANONICAL FORM. The draw_fn
  passed to figural_core.render_figure / render_option_set for such a role is
  `cio.structure_draw_fn(obj['canonical'])` — rdkit rasterises the molecule inside
  the axes, the frame and every v5.57 gate apply unchanged, and `draw.canonical`
  is what gets registered. Hand-placed bonds (ring_pts / bond / substituent
  helpers) for a STRUCTURE role are a G-FIGSEM HARD FAIL: that is exactly the
  drawing whose carboxyl was read as a ketone because nothing recorded otherwise.
  A SMILES rdkit rejects (valence / syntax) never renders — fix the molecule.
  Other kinds register a descriptor the explaining step can compare (a NEWMAN's
  front/back substituents and dihedral; an MO_DIAGRAM's occupancy by level; a
  COORDINATION's ligand set and arrangement). GENERIC is the floor, never the
  default for a kind the list names.
  GATE G-FIGSEM (S12, batch + Final Assembly): every rendered figural Q carries
  ≥1 validated semantic object per role; every STRUCTURE/REACTION role's canonical
  canonicalises through cio.canonical_structure; its PNG was produced by
  structure_draw_fn (fig spec engine tag). EC-V18: exams whose figures are not typed
  objects register GENERIC with a descriptor — nothing halts for lack of chemistry.

## S7-24 — QA mandatory-topic tracking (v4.9 — exam-agnostic; names removed)

  v4.9 CHANGE: no QA subtopic name is hardcoded here. Every QA mandate is DATA,
  owned by the manifest + gates, mirroring the v4.4 alternation migration.

  ── MANDATORY-EVERY-MOCK presence ──
    NOT restated by name. A QA subtopic that must appear in every mock is declared
    once as DATA (Step 0 emits mandate_every_mock=true → manifest.mandatory_every_mock;
    Framework_MockTestAnalyse v2.10). Enforcement:
      • Step 1 RULE M1 force-places 1Q of each mandated id in every mock;
      • Step 7 S3-17 HARD STOPs pre-generation if a mandated id is absent (HS-8);
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
  import figural_core as fc

  def build_di_chart(doc, qnum, chart, *, role="stim"):
      """
      chart : {'kind': 'line'|'bar'|'scatter'|'pie',
               'series': [{'label':..., 'x':[...], 'y':[...]}, ...],
               'axes'  : {'x': {'title':..., 'units':...},
                          'y': {'title':..., 'units':...}}}
      Returns the FigureSpec, having emitted the image into `doc`.
      """
      n = len(chart["series"])
      cls = "data_series" if n >= 2 else "data_single"
      spec = fc.make_figure_spec(qnum, cls, fc.FIG_PROBLEM_DISPLAY_IN,
                                 series=fc.series_defaults(n),
                                 axes=chart.get("axes", {}),
                                 key_mode="legend" if n >= 2 else "none",
                                 role=role)
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
    2. Places them via add_figural_question() (§10-S10-8): Q.N-first stem text,
       the problem image(s), then the N option images stacked SINGLE-COLUMN, each
       bound 1:1 to its "i." label (one option image per line; never two on a
       line, never a table row of options).
    3. Records the question in the figural manifest; the per-block image count
       (≥ n_options + 1) and one-image-per-option-line invariant are enforced by
       G-FIGURAL-COMPOSITE (S12-NEW-13). HARD STOP on a single-image (composite)
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
  happened to run — a HARD STOP arrived hundreds of questions later.

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
    def add_carrier_sentence_stem(doc, qnum, instruction, sentence, bold=True):
        p1 = doc.add_paragraph(); r1 = p1.add_run(f"Q.{qnum}  {instruction}")
        r1.bold = bold; r1.font.name = FONT_NAME; r1.font.size = Pt(FONT_SIZE_PT)
        p2 = doc.add_paragraph(); r2 = p2.add_run(sentence)
        r2.bold = bold; r2.font.name = FONT_NAME; r2.font.size = Pt(FONT_SIZE_PT)
        return p1, p2
    ```

## S10-3 — Python helpers (v2.0 — Calibri enforced)

  ```python
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
  # HARD STOP) tests THIS, not the widened MATH_TRIGGER_RE: normalised-axis
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
      NEVER reach the raster pipeline. R-MATH-OMML HARD STOP."""
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
  is emitted via add_math_stem / emit_math_inline (OMML). It is a HARD STOP to
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
  A defaulted class is how a scientific data figure ended up on the geometry
  path in the first place.

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
        1. Palette MUST be Okabe-Ito unless overridden by
           `exam_config.figure_palette` (v5.46 STATUS: render_figure() now
           accepts an optional palette= parameter — the engine plumbing exists —
           but the exam_config wiring is RESERVED for a future rich-colour
           release; until then every Step-7 render uses OKABE_ITO):
           #0072B2 #D55E00 #009E73 #CC79A7 #E69F00 #56B4E9 #F0E442 #000000
           (colour-blind safe across deuteranopia/protanopia/tritanopia, print
           safe, 8 hues). Defined once in figural_core.OKABE_ITO.
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
        and HARD-STOPS if handed a math expression.
    Q8b. SEVERITY — NO COLOUR CONDITION MAY EVER HALT A RUN (v5.33, owner
        directive). This is not a concession to convenience; it is this
        framework's own doctrine, stated in CLAUDE.md: "A CLASS T failure must
        be LOUD, and must NOT halt. These are separate properties and the corpus
        conflated them... Silence is the defect; a halt is not the remedy." A
        grey figure is a DEGRADED paper, never a void one. Three modes, defined
        in figural_core.SEVERITY:
          AMBER      — report at FAIL severity, force the amber delivery footer
                       (Framework_DeliveryFooter §5), ALWAYS complete. Every
                       colour and accessibility condition lives here:
                       G-FIGCOLOUR, G-FIGCVD, G-FIGSERIES, G-FIGGLYPH,
                       G-FIGALT, W-FIGLABELPX.
          VOID_ITEM  — the rendering leaks an ANSWER CUE or is unreadable, so
                       this QUESTION is invalid: G-FIGMONO (colour in a
                       reasoning glyph), G-FIGOPTUNIF (option canvases not
                       uniform), and from v5.55 G-FIGCOLLIDE (labels
                       overprinted — an option a candidate cannot read is not
                       a degraded option, it is an unanswerable one) and
                       G-FIGOPTWINDOW (options drawn at divergent scales, so
                       relative size — which in a structure question is
                       MEANING — became a renderer artefact). Drop or
                       regenerate the single question. The paper continues.
                       Never halts the run.
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
        EC-V18 LEGACY TOLERANCE, NON-NEGOTIABLE: output with no FigureSpec
        sidecar predates v5.33. Every BLOCKING gate downgrades to AMBER for it,
        so roughly 200 existing exams keep auditing and delivering untouched
        while still reporting the defect loudly. figural_core.triage() NEVER
        raises and NEVER halts.
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

    spec = fc.make_figure_spec(qnum, "data_series", fc.FIG_PROBLEM_DISPLAY_IN,
                               series=fc.series_defaults(2),
                               axes={"x": {"title": ..., "units": ...},
                                     "y": {"title": ..., "units": ...}},
                               key_mode="legend")
    fc.render_figure(draw_fn, png_path, spec)   # MUTATES spec with png_px,
                                                # png_dpi, placed_in,
                                                # placement_scale, font_pt_native
                                                # and (v5.55) spec['fit']
    fc.write_spec_sidecar(spec, png_path)       # the audit reads this
    ```
    OPTION SETS USE render_option_set(), NOT render_figure() IN A LOOP (Q12):
    ```python
    import figural_core as fc

    opt_specs = [fc.make_figure_spec(qnum, "option_canvas",
                                     fc.FIG_OPT_DISPLAY_IN, role="option")
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
      # v4.3 R-MATH-OMML HARD STOP: the figural path is geometry-only. A built-up
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
  A draw_fn that honours C1-C6 needs no repair; the fitter then only maximises
  fill. A draw_fn that does not is repaired where possible and REPORTED where
  not. Neither path can ship a silent defect, which is the whole objective.

## S10-8 — FIGURAL PLACEMENT (v4.0 — single-column, label-bound; was a v1.0 stub)

  Lays a figural MCQ into the docx as DISCRETE images. Enforces R-FIGURAL: stem is
  Q.N-first document text (R14); problem image(s) next; then the option images
  stacked ONE PER LINE, each bound 1:1 to its "i." label. There is exactly one
  image per option line — never two options on a line, never a table row of
  options, never a composite panel.

  ```python
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
      if spec is not None:
          _set_last_drawing_alt(doc, figural_core.alt_text(spec))   # Q9.5
      return p

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

      # Options: SINGLE COLUMN — one option per line, label bound to its image.
      for i, opt_png in enumerate(option_pngs, 1):
          lp = doc.add_paragraph()                  # the "i." label line
          lr = lp.add_run(f"{_option_label(i)}.")     # option label (configured format)
          lr.bold = False; lr.font.name = FONT_NAME; lr.font.size = Pt(FONT_SIZE_PT)
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

  COMPOSITE BAN: a figural block that contains only ONE image (problem + options
  fused) is a hard defect — the online engine renders one option region per screen
  and cannot slice a baked panel, and the figures are decoupled from their labels.
  G-FIGURAL-COMPOSITE fails any figural block with < (n_options + 1) images.

## S10-8A — FIGURAL STEM placement helper (v5.13 — stem_only variant)

  Handles format=FIGURAL + image_role='stem_only' MCQ: the problem/series
  figure(s) are images, but the options are TEXT (numbers, words, phrases).
  E.g., "How many triangles are in the given figure?" with text options.

  ```python
  def add_figural_stem_question(doc, qnum, stem, problem_pngs, text_options,
                                problem_label=None):
      """
      qnum         : int
      stem         : str   — the question instruction (DOCUMENT text, Q.N-first)
      problem_pngs : [bytes] — 1+ problem/series images (geometry only, 300 DPI)
      text_options : [str]  — text option strings (NOT images)
      Layout (R-FIGURAL stem_only / R14 / G-QNUM-FIRST):
        Q.N stem  →  problem image(s)   (v5.70: NO label line by default)
                  →  text options via add_text_options()
                  →  blank separator
      v5.13: new helper for the stem_only variant. Figural questions where only the
      stem has a visual element and options are text. Without this helper, the only
      path was add_figural_question() which HARD ASSERTs option images.
      """
      assert len(problem_pngs) >= 1, "stem_only figural MCQ needs ≥1 problem image"
      assert len(text_options) >= 2, "MCQ needs ≥2 text options"

      # LINE 1 — Q.N stem (BOLD, configured font) — Q.N FIRST, no image precedes it.
      add_question_stem(doc, qnum, stem)                # S10-3

      # Problem figure(s) (v5.70 CHG-2026-08-24-FIG-NOLABEL: NO label line by
      # default — a label renders only when a caller explicitly passes one).
      if problem_label:
          lab = doc.add_paragraph(); r = lab.add_run(problem_label)
          r.bold = True; r.font.name = FONT_NAME; r.font.size = Pt(FONT_SIZE_PT)
      for k, pb in enumerate(problem_pngs, 1):
          _add_image_para(doc, pb, FIG_PROBLEM_DISPLAY_IN)
          nm = (f"q{qnum}_problem.png" if len(problem_pngs) == 1
                else f"q{qnum}_problem_{k}.png")
          _name_last_drawing(doc, nm)                   # canonical name (S10-7 Q8)

      # Options: TEXT, not images. Standard text option placement.
      add_text_options(doc, text_options)                # S10-3

      add_blank_separator(doc)                           # R13

  # USAGE (per stem_only figural question, from S8-6):
  #   prob = render_figural_image(draw_problem, kind="problem")
  #   add_figural_stem_question(doc, q.num, q.stem, [prob], text_options)
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
  If this returns False → HARD STOP. Remove answer key from docx before delivery.

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
      For every subtopic in this mock whose section_rules format==FIGURAL:
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
            raise SystemExit(f"G-ALTGROUP: Mock {N} — alternation group '{group}' has "
                     f"{len(present)} members present ({', '.join(disp)}); ≤1 allowed.")
    ```
    Empty alternation_groups ⇒ nothing to enforce ⇒ pass (no false stop).
    Zero hardcoded subtopic names. Fixable: drop the member that the blueprint
    parity assigns to the other mock, then regenerate (Step 7 does not auto-edit
    the blueprint).

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
            raise SystemExit(f"G-GROUPMANDATE: Mock {N} — group '{group}' has {have} of "
                     f"[{', '.join(disp)}] present; needs >={need}.")  # v5.53.2: was sys.exit, sys never imported
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
            raise SystemExit(f"G-MINCOUNT: Mock {N} — {mid} ('{disp}') has {c}Q generated; "
                     f"needs >={k}.")  # v5.53.2: was sys.exit, sys never imported
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

  S12-NEW-10 — G-STIMULUS-ORPHAN (v3.6 — linked self-containment, HARD STOP):
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

  S12-NEW-11 — G-QNUM-FIRST (v3.7 — Q.N-FIRST block contract, HARD STOP):
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

  S12-NEW-12 — G-FORMATDUP (v3.8; v3.9 hardened — RULE C, HARD STOP):
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

  S12-NEW-13 — G-FIGURAL-COMPOSITE (v5.13 — image_role-aware, HARD STOP):
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

  S12-NEW-14 — G-UNDERLINE (v4.1 — underline-span rendering, HARD STOP):
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

  S12-NEW-15 — G-OPTREF (v4.2 — stem↔option reference consistency, HARD STOP):
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

  S12-NEW-16 — G-UNIQUE (v4.5 — answer-contract record, HARD STOP; generalises v4.2):
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

  S12-NEW-18 — G-MSQ-SET (v4.5 — MSQ set well-formedness, HARD STOP; MULTI ONLY):
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

  S12-NEW-19 — G-MSQ-CARD (v4.5 — MSQ fixed-k cardinality, HARD STOP; MULTI + FIXED ONLY):
    Runs ONLY when answer_cardinality=='multi' AND section_rules msq_k_mode=='fixed'.
    ALGORITHM: if |answers[q]| != msq_k → Exit 1.
    For "Select TWO"/"Select THREE" exams this guarantees the rendered set matches the
    instructed count. Variable-k exams skip this gate (no fixed cardinality to check).
    Report: "G-MSQ-CARD: Q.[n] has |S|=[got], expected msq_k=[k]."

  S12-NEW-20 — G-MSQ-INSTR (v4.5 — MSQ instruction line present, HARD STOP; MULTI ONLY):
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

  S12-NEW-21 — G-NAT-NOOPT (v4.7 — NAT zero-option, HARD STOP; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. A NAT question is a typed-value
    question with NO options (R4 / R13 NAT exemption). AUTHORITATIVE: scans the rendered
    docx, locates the question's Q.<N> block, and counts option-label paragraphs (the R10
    "N.  " pattern). If a NAT question carries ANY option paragraph → Exit 1 (a generation
    routing bug — the NAT path must emit only the bold Q.<N> stem + blank separator).
    Fully dormant when nat_present=false. EXAM-AGNOSTIC.
    Report: "G-NAT-NOOPT: Q.[n] (NAT) has [k] option paragraph(s); must have none."

  S12-NEW-22 — G-NAT-ANSWER (v4.7 — NAT value well-formed, HARD STOP; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. Reads the stored answer VALUE
    (answers[q], tested 'is None' so 0/negative/fractional are valid) and the per-Q
    ca_range, against nat_meta.nat_answer_type. Exit 1 when: (a) no value recorded; (b)
    value is non-numeric; (c) nat_answer_type=='integer' but the value is not integral;
    (d) ca_range present but malformed (not exactly (lo,hi) with lo<=hi). This is the
    generation-side backstop for R-ANSWER's numerical branch; audit.py A-NAT-ANSWER
    independently RE-DERIVES the value and checks it lies in the band. EXAM-AGNOSTIC.
    Report: "G-NAT-ANSWER: Q.[n] [value/ca_range problem]."

  S12-NEW-23 — G-NAT-INSTR (v4.7 — NAT instruction line present, HARD STOP; NUMERICAL ONLY):
    Runs ONLY for answer_type=='numerical' questions. The nat_instruction (blueprint
    nat_contract; e.g. "Enter your answer as a numerical value.", localized) MUST appear
    INSIDE the bold Q.<N>-first stem paragraph (R14 / G-QNUM-FIRST — no paper-level
    instructions page). Record-presence backstop here (the per-Q nat_instr_in_stem flag);
    audit.py A-NAT-INSTR re-checks the rendered docx. NOT FIXABLE by a separate paragraph
    (breaks R14): re-emit the stem with the instruction appended to the Q.<N> line.
    Fully dormant when nat_present=false. EXAM-AGNOSTIC.
    Report: "G-NAT-INSTR: Q.[n] (NAT) has no numerical-entry instruction in its Q.N stem line."

  S12-NEW-29 — G-NAT-GRADE (v5.25 — NAT portal grading value well-formed, HARD STOP;
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

  S12-NEW-30 — G-MATH-RESIDUE (v5.70 — ASCII-dialect math residue, HARD STOP per
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


  S12-NEW-17 — G-MATH-RASTER (v4.3 — math-as-OMML routing, HARD STOP):
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
            raise SystemExit(1)                      # Exit 1 — HARD STOP
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

  S12-NEW-26 — G-QINDEX (v5.2 — question-index certification, HARD STOP; runs at Final
    Assembly; executable home S13-QINDEX, after S13-REGCHECK). Certifies the mock-N
    registry.question_index this session built (S13-4) — the per-question {subtopic_id,
    difficulty} record Step 6 renders as the five tags. Six checks, all HARD STOP:
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

  S12-NEW-27 — G-PREQ1 (v5.18 — pre-Q.1 body-block ban, HARD STOP; per-batch S4-11 AND the
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
  _di_manifest = None
  if di_present and os.path.exists(f'/home/claude/{EXAM}_di_manifest.json'):
      _di_manifest = json.load(open(f'/home/claude/{EXAM}_di_manifest.json'))

  # Figural manifest + the FigureSpec sidecars (v5.34, GAP-2026-08-01-FIGSPEC-TRANSPORT D2),
  # keyed by the CANONICAL PNG name S10-8 stamps on the drawing.
  _fig_manifest, _figure_specs = None, None
  if figural_present and os.path.exists(f'/home/claude/{EXAM}_fig_manifest.json'):
      _fig_manifest = json.load(open(f'/home/claude/{EXAM}_fig_manifest.json'))
      _figure_specs = {
          os.path.basename(_fs)[:-len('.figspec.json')] + '.png':
              json.load(open(_fs, encoding='utf-8'))
          for _fs in sorted(glob.glob('/home/claude/*.figspec.json'))
      }

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

  _commit = fa.commit_registry(
      registry, pending_registry, bp, N,
      paper_id=paper_id, batches_completed=batches_completed,
      axis2_window_counts=axis2_window_counts,
      passage_present=passage_present, di_present=di_present, figural_present=figural_present,
      concept_map=_cm, passage_linked_qs=passage_linked_qs, cloze_linked_qs=cloze_linked_qs,
      di_manifest=_di_manifest, fig_manifest=_fig_manifest, figure_specs=_figure_specs,
      axis1_snapshots=_ax1, axis3_snapshots=_ax3,
      answer_key=_akd)                      # v5.59 — key commitments (S13-4 / Explain §7-8)
  if not _commit['ok']:
      raise SystemExit(_commit['fails'][0])
  registry = _commit['registry']
  paper_id = _commit['paper_id']

  # v5.52 (GAP-2026-08-12-S13-COMMIT-COMPLETE) — ATOMICITY MANDATE: fa.commit_registry() is
  # PURE (accumulates every field into a NEW in-memory dict, mutates nothing) — this remains
  # the single terminal write to registry.json for this mock's S13-4 commit. There must be NO
  # other json.dump of registry.json anywhere else in this block: an FK failure returns
  # {'ok': False, 'registry': <the ORIGINAL, unmodified registry>} instead of raising mid-write,
  # so registry.json on disk is COMPLETELY UNTOUCHED on failure — never partially written.
  # G-COMMIT-COMPLETE (S13-REGCHECK) is the downstream detector if this rule is ever violated
  # by a future edit; this comment is the upstream prevention.
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
  `final_assembly.regcheck()`. THIS mock's own commit is a HARD STOP if incomplete; a
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
  (not a false HARD STOP) when an exam's blueprint declares no difficulty_schedule at all;
  IIT_JAM_BIOTECHNOLOGY always declares one, so nothing changes for this exam.

  ```python
  _qi = fa.qindex_certify(registry, bp, N)
  if not _qi['ok']:
      raise SystemExit("HARD STOP (G-QINDEX): " + "; ".join(_qi['fails'])
                       + ". Fix the per-Q subtopic_id/difficulty capture (S7-NEW-A) or the "
                       + "schedule-first assignment, rebuild question_index (S13-4), re-run.")
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
      --blueprint /mnt/project/[ExamCode]_blueprint.json \
      --mockN [N]
  ```
  ([paper_slug] = pp.paper_slug(paper_id) — "Mock01" for a mock, "SUBJ_Physics_01" for a
  scoped paper; v5.54, GAP-2026-08-12-S13-4B-SCOPED-PATH. The executed block below uses
  `_docx` carried from S13-4b, which is already slug-derived.)

  Executed as:

  ```python
  if AUDIT_AVAILABLE and os.path.exists(_out):
      _r = subprocess.run(
          ['python3', f'/home/claude/{EXAM}_mock_test_audit.py',
           _docx, '--dossier', _out,
           # v5.48.0 — arm A-QINDEX: engine-enforced FK certification of the
           # question_index this session just committed (S13-4). The exit code
           # below is the durably-logged verdict; a bad index can no longer
           # coexist with a clean audit log.
           '--registry', f'/home/claude/{EXAM}_registry.json',
           '--blueprint', f'/mnt/project/{EXAM}_blueprint.json',
           '--mockN', str(N)],
          capture_output=True, text=True)
      print(_r.stdout)          # real STDOUT — never a paraphrase (B-7)
      if _r.returncode != 0:
          raise SystemExit(
              "HARD STOP (S13-4c re-sweep, v5.48.0): auditor FAILed — see STDOUT "
              "above (A-QINDEX FK violations are listed by Q-number). Fix and "
              "re-run; present_files is forbidden until clean (B-7).")
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
          raise SystemExit(
              f"HARD STOP (S13-4c, v5.48.0): {EXAM}_mock_test_audit.py printed no "
              "A-QINDEX line, so it predates the FK gate and the question_index "
              "was NOT certified — a clean exit code here would be meaningless. "
              "Refresh the per-exam auditor (re-run Step 6 B3, or replace the "
              "project file with the current repo audit_canonical.py verbatim "
              "under the same [ExamCode]_ name), then re-run. present_files is "
              "forbidden until clean (B-7).")
  ```

  v5.48.0: this re-sweep now ALSO arms A-QINDEX (the engine-enforced FK gate over the
  question_index committed at S13-4) via --registry/--blueprint/--mockN, and a nonzero
  exit here is a HARD STOP. For the dossier-fed gates it remains the same auditor, the
  same A-* catalogue, and the same paper that S13-2 already swept clean — run once more so
  those two gates read facts rather than defaults. A FAIL here is handled exactly as a
  FAIL in S13-2 is handled (fix, re-run, present_files forbidden until clean, B-7).
  If AUDIT_AVAILABLE is False the dossier is still written and this re-sweep is skipped,
  with the S4-11 absence note (see the audit.py requirement block at the head of this
  spec) already stating that no machine audit ran.

## S13-5 — Registry integrity check (unchanged)

## S13-6 — THE DELIVERABLE SET IS CLOSED (v3.5 — read before delivering)

  At Final Assembly, Step 7 delivers the CLOSED SET to the user, and NOTHING
  ELSE — EXACTLY the two files below. This is an exhaustive, closed list — not a
  minimum. (v5.73: the dossier left the set by operator decision; the set no
  longer varies, so the v5.54.1 count-drift cannot recur.)

  DELIVER (mandatory, both via the SAME present_files call):
    1. [ExamCode]_[paper_slug]_Create.docx  — the final paper ("Mock[N]"
                                              zero-padded for a mock; scoped slug otherwise)
                                              → Use locally
    2. [ExamCode]_registry.json             — updated dedup/tracking registry
                                              → Replace in Project Files (REGISTRY-HANDOFF-LAW)

  DO NOT DELIVER (internal — never passed to present_files):
    ✗ [ExamCode]_M[N]_audit_dossier.json    — Tier-A dossier, /home/claude (S13-4b, v5.73)
    ✗ [ExamCode]_M[N]_answer_key.json       — internal sidecar (S3-14)
    ✗ any standalone answer-key file in ANY format (.docx/.pdf/.json/.txt)
    ✗ [ExamCode]_fig_manifest.json          — internal
    ✗ [ExamCode]_M[N]_batch_state.json      — internal
    ✗ [ExamCode]_M[N]_progress.json         — internal
    ✗ any per-batch cumulative docx (Q1to[k]) — superseded by _Create.docx

  This is the inline anchor for R-DELIVER. The answers exist ONLY in the
  internal answer_key.json sidecar (S3-14), which is NEVER delivered. If the
  user wants a learner-facing answer key, that is a Step-4 (MockExplain)
  artefact, not a Step-7 one. Step 7 ships the paper + registry, full stop.

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

  _pdc = fa.predelivery_checklist(
      out, docx_name=docx_name, reg_name=reg_name, dossier_name=dossier_name,
      regcheck_ok=globals().get('REGCHECK_OK'), qindex_ok=globals().get('QINDEX_OK'))
  if not _pdc['ok']:
      raise SystemExit(
          "HARD STOP (S13-7): pre-delivery checklist failed: "
          + "; ".join(_pdc['fails'])
          + ". Fix each, then re-run S13-7. Do NOT call present_files yet. "
          + "If item 4 fails, DELETE the off-spec answer-key file from outputs. "
          + "If item 2/3 fails, re-run S13-4 + S13-REGCHECK. "
          + "If item 5/6 fails, move internal files back to /home/claude.")
  print("S13-7: all 7 pre-delivery checks PASS. Cleared to deliver.")
  ```

  Stage ONLY the deliverables in /mnt/user-data/outputs; keep every internal file
  in /home/claude. Item 6 enforces the closed set.
  THE CLOSED SET (v5.73): the rectified docx + registry.json. Nothing else, ever.
  A staged [ExamCode]_M[N]_audit_dossier.json fails item 5 (internal sidecar leak).

## S13-8 — Deliver (v3.5 — the SINGLE present_files call)

  Call present_files ONCE, with BOTH files, docx first (most relevant):
    present_files([
        docx_path,        # C2: paper-scoped ({EXAM}_{paper_slug}_Create.docx — zero-padded mock or scoped slug)
        reg_path
    ])

  This is the ONLY present_files call at Final Assembly. Do NOT call it once
  per file. Do NOT call it for any internal file. The per-batch habit of "one
  docx per present_files" does NOT apply here — Final Assembly ships TWO files.

## S13-9 — Handoff message (v3.5 — print after present_files, then END)

  Print exactly this block (no question content — MANDATE 0), filling brackets:

  ```
  === MOCK [N] COMPLETE — Step 7 done ===
  Delivered (2 files):
    • [ExamCode]_Mock[N]_Create.docx   — the mock paper            → Use locally
    • [ExamCode]_registry.json           — updated registry           → Replace in Project Files

  ⚠ REGISTRY HANDOFF — REQUIRED before generating the next mock:
    Replace registry.json in your [ExamCode] project knowledge with the one
    just delivered. The next mock's dedup depends on it. If you skip this,
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

  After printing the handoff: END THE RESPONSE. Write nothing more.

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

  DELIVERY (v3.5 — closed contract):
  □ The closed set delivered: EXACTLY final .docx + registry.json (S13-6, R-DELIVER; v5.73 — the audit dossier is internal)  **
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
  | G-DELIVERY-SET | Outputs dir holds EXACTLY the closed set: docx + registry (v5.73 — the audit dossier is internal; the set no longer varies) | YES  | Remove stray/internal files; add reg |

  G-DELIVERY-SET (definition): at Final Assembly, /mnt/user-data/outputs must
  contain exactly { [ExamCode]_Mock[N]_Create.docx, [ExamCode]_registry.json }
  — no more, no fewer. A standalone answer-key file, a leaked internal sidecar,
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
# §S16 — REPAIR MODE (TestCreateRepair / MockCreateRepair, v5.69 —
#         GAP-2026-08-24-DIFFICULTY-GATE-BLOCKING)
# ════════════════════════════════════════════════════════════════════════

## S16-1 — Trigger and preflight

  TRIGGER: `TestCreateRepair P[N] Q4 Q8 Q20 …` or `MockCreateRepair M[N] Q…`
  (Q-list separators: spaces or commas; "Q4"/"4" both accepted).
  CONTINUE: the S4-6 continue triggers ("continue" / "go" / "next" …) between repair
  batches (v5.74 — S16-1b). RESUME: `TestCreateRepair P[N] resume` (re-enter a repair
  mid-way: reload [ExamCode]_M[N]_repair_state.json + the working registry, S16-1b).
  ATTACH: the CURRENT question paper docx for paper N (this step's own
  earlier deliverable). The registry and blueprint come from project
  knowledge as always.

  PREFLIGHT (HARD STOP on any failure — malformed-input stops are exempt
  from the no-stop rule, which governs gate VERDICTS only):
    P0  Load the PROJECT copy of the registry and fingerprint it BEFORE any write
        (v5.73 — S16-3's handoff decision compares against this value):

        ```python
        import os, json, shutil
        import paper_pipeline as pp
        REG_PROJECT = f'/mnt/project/{EXAM}_registry.json'        # what Step 9-R will read
        REG_WORK    = f'/home/claude/{EXAM}_registry.json'        # this repair's working copy
        _reg_fp_loaded = pp.registry_fingerprint(json.load(open(REG_PROJECT, encoding='utf-8')))
        if not os.path.exists(REG_WORK):
            shutil.copy(REG_PROJECT, REG_WORK)                    # first turn of the repair only
        reg = json.load(open(REG_WORK, encoding='utf-8'))         # continue/resume: carries the
                                                                  # S16-1b snapshot + batches done
        rec, disclosure = pp.dg_preflight(reg, paper_id, where='S16-1 P0')
        ```
        (v5.71 — GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER). Runs FIRST.
        A corrupt (status, repair_rounds_used) pair is healed per
        DG-INVARIANT and disclosure is printed VERBATIM in chat (never
        silent); the registry is persisted with the S16-3 commit. A
        DGIllegalState (unknown status) is a HARD STOP — print its message
        verbatim; never proceed on an illegal record.
    P1  BRANCH ON THE STATE PAIR pp.dg_state(rec), never on one field.
        Absent → "This paper has no gate record — run TestExplain P[N] first
        (or this is a legacy paper; deliver as usual)."
        ('FAILED', 0) → PROCEED only if pp.dg_is_windowed(rec) (v5.72 —
        GAP-2026-08-25-DIFFICULTY-GATE-WINDOWS). A FAILED record WITHOUT the
        'windows' stamp was judged under the retired band-equality rule and
        its rework_qs are NOT an order: HARD STOP with "This paper was judged
        under the old difficulty rule — nothing is rewritten on its say-so.
        Next step: " + pp.dg_next_step(...) (the Explain trigger, which re-
        judges the verdict under the windows). pp.dg_add_rework_snapshot
        refuses such a record too, so the stop cannot be bypassed.
        Any other legal pair → "Nothing to repair — next step: " +
        pp.dg_next_step(reg, paper_id, N, mock=<Mock* trigger>) — the SAME
        function Step 9 and Step 11 print from, so this step can never name a
        next step that refuses. (Legal pairs and the state machine:
        MockTestExplain §7A-M "THE RECORD IS SINGLE-WRITER".)
    P2  THE Q-LIST OF RECORD IS THE REGISTRY'S rework_qs — the operator's
        typed list is a CONFIRMATION, not a selection. Empty typed list →
        use rework_qs verbatim. Typed list ≠ subset of rework_qs → HARD
        STOP naming the extras ("Q7 is not in the rework order — the gate
        flagged only Q…"). Typed list a strict subset → HARD STOP: partial
        repairs would leave the band over-limit by construction; repair all
        of rework_qs in one run.
    P3  The attached paper parses (§P3 machinery) and its stems hash-match
        registry stem_texts for paper N (the operator attached the right
        file and the right version). On a continue/resume turn the paper of
        record is the cumulative repaired docx in /home/claude (S16-1b), not a
        new attachment.

## S16-1b — REPAIR BATCH PLAN + PRE-REPAIR SNAPSHOT (v5.74 — GAP-2026-08-26-REPAIR-BATCH-LAW)

  THE LAW, RESTATED FOR REPAIR. S4-4 B-1..B-7 apply to a repair exactly as to a
  fresh paper: a batch is at most MAX_BATCH_SIZE questions (S4-2's ceiling), ONE batch
  per response, auto-advance BANNED, the next batch only on an S4-6 continue trigger,
  present_files only after the batch passes gate checks. B-8's analogue: the FINAL
  repair batch auto-advances to S16-3 in the same response. A rework list of ≤
  MAX_BATCH_SIZE is one batch and the run is a single response, as it was in v5.73.
  The plan is built ONCE (first turn) and read from the file on every later turn —
  never recomputed, never "the last q + 1".

  ```python
  import os, json
  import paper_pipeline as pp
  MAX_BATCH_SIZE = 10                     # S4-2 ceiling — the same number, by reference
  STATE = f'/home/claude/{EXAM}_M{N}_repair_state.json'
  if not os.path.exists(STATE):           # FIRST TURN — plan + snapshot, once
      # old_stems[q] = the raw first paragraph of q in the ATTACHED paper, "Q.<n>" label
      # included — python-docx paragraph.text, the SAME extraction §7A-R R3 applies to the
      # repaired paper, so both sides of pp.dg_stem_hash see identical bytes.
      import re as _re
      from docx import Document as _Doc
      # The attachment is addressed by its EXACT contract name — never a glob — so a
      # stray _Repaired / _PARTIAL / sibling-paper upload can never be picked up.
      ATTACHED_PAPER = f'/mnt/user-data/uploads/{EXAM}_{pp.paper_slug(paper_id)}_Create.docx'
      if not os.path.exists(ATTACHED_PAPER):
          raise SystemExit(f"HARD STOP (S16-1b): {os.path.basename(ATTACHED_PAPER)} is not "
                           f"attached. Attach the CURRENT question paper for paper {N} (not a "
                           f"_Repaired / _PARTIAL file) and re-trigger.")
      _QRE = _re.compile(r'^\s*Q\.?\s*(\d+)\b')
      old_stems = {}
      for _para in _Doc(ATTACHED_PAPER).paragraphs:
          _m = _QRE.match(_para.text)
          if _m and int(_m.group(1)) not in old_stems:
              old_stems[int(_m.group(1))] = _para.text
      if sorted(old_stems) != list(range(1, int(bp['total_questions']) + 1)):
          raise SystemExit(f"HARD STOP (S16-1b): the attached paper yields stems for "
                           f"{len(old_stems)} questions, blueprint says "
                           f"{bp['total_questions']} — the baseline snapshot must cover "
                           f"EVERY question or §7A-R R3 cannot prove the repair touched "
                           f"nothing else. Attach the complete paper.")
      rework_qs = sorted(int(q) for q in rec['rework_qs'])
      if not rework_qs:
          raise SystemExit('HARD STOP (S16-1b): the gate record carries an empty rework_qs — '
                           'nothing to repair; run pp.dg_next_step for the next step.')
      batches = [rework_qs[i:i + MAX_BATCH_SIZE] for i in range(0, len(rework_qs), MAX_BATCH_SIZE)]
      # PRE-REPAIR SNAPSHOT — write-once, BEFORE any stem is regenerated (§7A-R R3 evidence).
      # old_stems[q] = the raw first paragraph of q in the attached paper, "Q.<n>" label
      # included, for EVERY q in 1..total_questions (P3 parsed it).
      pp.dg_add_rework_snapshot(reg, paper_id,
                                {q: pp.dg_stem_hash(old_stems[q]) for q in rework_qs},
                                all_stem_hashes={q: pp.dg_stem_hash(t) for q, t in old_stems.items()})
      json.dump(reg, open(f'/home/claude/{EXAM}_registry.json', 'w', encoding='utf-8'),
                indent=2, ensure_ascii=False)               # working copy only — NOT delivered yet
      repair_state = {'exam_code': EXAM, 'mock_n': N, 'paper_id': paper_id,
                      'rework_qs': rework_qs,
                      'batches': [{'batch_id': i + 1, 'qs': b, 'is_final': i == len(batches) - 1}
                                  for i, b in enumerate(batches)],
                      'batches_completed': [], 'current_batch': 1, 'snapshot_taken': True}
      json.dump(repair_state, open(STATE, 'w', encoding='utf-8'), indent=2)
  repair_state = json.load(open(STATE, encoding='utf-8'))
  # CONTINUE / RESUME GUARDS (B-1 analogue): the working registry must carry the
  # snapshot S16-1b took on the first turn — a working copy lost between turns (fresh
  # container, deleted /home/claude) cannot be re-snapshotted from a half-repaired paper.
  _snap = (reg.get('difficulty_gate', {}).get(paper_id, {}) or {}).get('rework_stem_hashes') or {}
  if set(_snap) != {str(q) for q in repair_state['rework_qs']}:
      raise SystemExit(f"HARD STOP (S16-1b): repair_state.json exists but the working "
                       f"registry has no pre-repair snapshot for {repair_state['rework_qs']}. "
                       f"The working copy was lost mid-repair. Delete "
                       f"{EXAM}_M{N}_repair_state.json, restore the PROJECT registry and "
                       f"the ORIGINAL paper, and re-run TestCreateRepair P{N} from batch 1.")
  if repair_state['current_batch'] > len(repair_state['batches']):
      raise SystemExit(f"HARD STOP (S16-1b): every repair batch is already completed — "
                       f"S16-3 has (or should have) delivered. Next step: "
                       + pp.dg_next_step(reg, paper_id, N, mock=False))
  _b = repair_state['batches'][repair_state['current_batch'] - 1]
  BATCH_QS, REPAIR_FINAL = _b['qs'], _b['is_final']
  K_TOTAL, K_NOW = len(repair_state['batches']), repair_state['current_batch']
  print(f"REPAIR BATCH {K_NOW} of {K_TOTAL}: Q{' Q'.join(map(str, BATCH_QS))}"
        f"{' (final)' if REPAIR_FINAL else ''}")
  ```
  Then S16-2 regenerates ONLY BATCH_QS. After the batch passes the self-audit
  (S4-7 STEP B) the response delivers and ENDS per S16-3.

## S16-2 — Regeneration (the only questions touched are rework_qs)

  For each q in BATCH_QS (v5.74 — this batch's slice of rework_qs; every q in
  rework_qs is reached across the batches), run the FULL S7 single-question flow (scenario →
  CHECK 1/1b/2/3/3c → sidecar) with these bindings:
    band     = difficulty_plan-of-record = question_index[q].difficulty
               (the label does not change; the QUESTION moves to it)
    direction= rec['rework_directions'][str(q)] (v5.72): 'harder' — the
               question measured BELOW its label's window (the common case);
               'easier' — it measured ABOVE it (possible for a middle-band
               question under the windowed rule). Missing for a listed q →
               HARD STOP naming q (a windowed FAILED record always carries
               it — pp.dg_write_verdict refuses to write one without).
               The rewrite must land INSIDE the label's acceptance window
               (bc.DIFFICULTY_GATE_BAND_WINDOWS by band position — middle
               2–6, top ≥5) as measured by CHECK 3c's own obs: assert
               bc.difficulty_score_from_obs(obs) lies in the window before
               committing the slot, else redo the slot. CHECK 3c still
               verifies the authored label against the strict authoring
               bands (G-DIFF) exactly as for a fresh slot.
    subtopic = question_index[q].subtopic_id (slot allocation unchanged —
               quota, axis schedules, figural counts all stay intact)
    qtype    = marking_scheme position type (unchanged)
  CHECK 3c runs with the standing rules PLUS, in repair mode:
    (a) STEM-SUPPLIED RELATION RULE (the reason most 'harder' reworks
        exist): the stem may not donate the governing relation of the asked
        quantity —
        no "Given that ∫…", no quoting the formula whose recall/derivation
        the steps count, no handing over a counted intermediate. If the
        subtopic genuinely requires a supplied constant (physical data),
        supply the CONSTANT, never the RELATION.
    (b) the superseded question's semantic tuple joins the dedup set — the
        repair must be a genuinely different question (harder or easier per
        direction), not a reworded twin.
    (c) an 'easier' rework removes load, never content: drop a concept or a
        derivation stage; do not hand over the governing relation in the
        stem (rule (a) still binds) and do not change the subtopic.
  Dedup, key derivation (§S7-NEW-A/C), figure generation (if the slot is
  FIGURAL) all run exactly as in a normal S7 slot.

## S16-3 — Commit and deliverable

  THE CUMULATIVE PAPER (v5.74): /home/claude/[ExamCode]_[paper_slug]_Create_Repaired.docx —
  created on the first turn as a byte copy of the attached paper, then every batch's
  regenerated questions are spliced into it in place. It persists across turns (S4-8
  cross-batch persistence); the final turn copies it to outputs under the same name.
  MID-BATCH (v5.74 — REPAIR_FINAL is False): after the batch's self-audit, splice the
  regenerated questions into the cumulative repaired paper above, apply the
  per-question registry updates below for THIS batch's qs on the WORKING copy, then
  deliver ONLY the cumulative paper, named
  [ExamCode]_[paper_slug]_Create_Repaired_PARTIAL_[k]of[K].docx (F1 amber footer,
  DeliveryFooter §3 "STEP 7-R"). The registry is WITHHELD mid-batch BY DESIGN — this is
  the one deliberate exception to "changed ⇒ delivered", and it is still the law's
  intent: a registry beside a half-repaired paper would let Step 9-R run on that paper
  (its R3 check would pass for the batches done and fail for the rest as "unchanged
  listed"), so the working copy travels only with the COMPLETE paper. The PARTIAL name
  is one Step 9-R's S2-1 REFUSES, so the same half-paper cannot be attached by mistake.
  Then update repair_state.json (batches_completed += k, current_batch += 1 — B-6),
  print "Repair batch [k] of [K] delivered — Q… rewritten. Type 'continue' for batch
  [k+1]." and END the response (B-4). Nothing below runs on a non-final batch.

  FINAL BATCH (REPAIR_FINAL is True) — everything below, in the same response (B-8):
  S13-4 UPDATE SEMANTICS (surgical — the registry is shared state):
    question_index[q]      → replaced entry (new difficulty_obs from the
                             repair derivation; label unchanged)
    stem_texts / question_hashes / semantic_tuples / semantic_usage
                           → replaced at q's position
    key_commitments[q]     → re-sealed for the new answer (fresh salt)
    options_by_q, figural manifests, image phashes
                           → updated for q only
    difficulty_gate record → ALREADY holds the pre-repair snapshot: S16-1b
                             called pp.dg_add_rework_snapshot ONCE on the
                             first turn, BEFORE any stem was regenerated
                             (v5.74; v5.69–v5.73 took it here, which is
                             equivalent only when the repair is one batch).
                             H(q) = pp.dg_stem_hash(<old first-paragraph text
                             of q, raw, "Q.<n>" label included>); the
                             all-question baseline lets §7A-R R3 prove NO
                             question outside rework_qs was touched. The
                             helper is WRITE-ONCE — a re-run returns the
                             original snapshot and never hashes repaired
                             stems — and refuses unless the record is a legal
                             FAILED state. Assert here that
                             reg['difficulty_gate'][paper_id] carries
                             rework_stem_hashes for every q in rework_qs;
                             if not, HARD STOP: "snapshot missing — re-run
                             TestCreateRepair P[N] from a fresh session".

      ⛔ THIS STEP NEVER WRITES `status` AND NEVER WRITES
         `repair_rounds_used` — not by hand, not "defensively", not to mark
         the round complete. Both belong to Step 9 alone
         (Framework_MockTestExplain §7A-M / §7A-R), which writes them
         TOGETHER in one atomic pp.dg_write_verdict call. Setting
         repair_rounds_used here — however natural it looks next to this
         step's own `'round': 1` session_log entry and its "REPAIR COMPLETE"
         print — produced status=FAILED + rounds=1: a pair no step can
         produce on purpose, which DEADLOCKED TestExplainRepair, TestDeliver
         and TestCreateRepair with no exit and cost a completed 60-question
         paper plus its full explanation run
         (GAP-2026-08-25-DIFFICULTY-GATE-ROUND-COUNTER). paper_pipeline
         Cluster DG now enforces this mechanically: pp.dg_add_rework_snapshot
         cannot touch either field, and pp.dg_write_verdict refuses the pair.
         audit_canonical A-DGATE (armed by --registry at the S13-4c
         re-sweep) FAILS the audit on any record outside the six legal
         states.

      NOTE — this step's `'round': 1` session_log entry counts THIS step's
      regeneration runs. It is NOT the difficulty-gate repair-round counter
      and the two are never reconciled with each other.
    Every other question's data: byte-identical. The S13 ledger gains a
    'repair' session_log entry (round 1, qs listed).
  DELIVERABLES (v5.73 — GAP-2026-08-26-REGISTRY-HANDOFF-SEAM; the CLOSED SET,
  one present_files call, F2 footer):
    1. [ExamCode]_[paper_slug]_Create_Repaired.docx — the full re-assembled
       question paper (every question, repaired ones spliced in place; same
       slug rule as S13-7, "_Repaired" suffix)                → Use locally
    2. [ExamCode]_registry.json — the registry this step just changed
       (replaced stems/hashes/tuples, re-sealed key_commitments, updated
       question_index[q], and the WRITE-ONCE pre-repair snapshot that §7A-R R3
       verifies against)                                     → Replace in Project Files
  WHY 2 IS NOT OPTIONAL. Through v5.72 this line named ONLY the docx. The
  snapshot then lived in /home/claude, the project registry never received it,
  TestExplainRepair R3 raised missing_snapshot → "re-run TestCreateRepair" →
  whose P3 no longer hash-matched the (already repaired) paper: a dead loop on
  every exam that ever reached a FAILED gate. REGISTRY-HANDOFF-LAW: a step that
  CHANGES registry.json DELIVERS it. The decision is mechanical:

  ```python
  import os, json, shutil
  import paper_pipeline as pp
  # _reg_fp_loaded was taken at S16-1 P0 from the PROJECT copy; `reg` is the working
  # copy that carries the S16-1b snapshot and every batch's updates.
  assert REPAIR_FINAL, 'S16-3 delivery runs on the FINAL repair batch only (S16-1b)'
  out = '/mnt/user-data/outputs'
  repaired_name = f'{EXAM}_{pp.paper_slug(paper_id)}_Create_Repaired.docx'
  reg_name = f'{EXAM}_registry.json'
  json.dump(reg, open(f'/home/claude/{reg_name}', 'w'), indent=2, ensure_ascii=False)
  hs = pp.handoff_set('TestCreateRepair', primary_docx=repaired_name, reg_name=reg_name,
                      registry_changed=pp.registry_changed(_reg_fp_loaded, reg), final=True)
  if not hs['registry_delivered']:
      # S16-3 ALWAYS writes the snapshot; an unchanged registry here is a caller bug.
      raise SystemExit('HARD STOP (S16-3): registry unchanged after a repair commit — '
                       'pp.dg_add_rework_snapshot did not run; nothing is delivered.')
  shutil.copy(f'/home/claude/{reg_name}', f'{out}/{reg_name}')
  v = pp.verify_handoff_outputs(os.listdir(out), hs)
  if not v['ok']:
      raise SystemExit(f"HARD STOP (S16-3): outputs != closed set — missing {v['missing']}, "
                       f"stray {v['stray']}. Fix, then re-run. Do NOT call present_files.")
  print('S16-3: closed set verified —', hs['files'])
  for _line in pp.handoff_footer_lines(hs):
      print(_line)
  ```
  Then present_files([f'{out}/{repaired_name}', f'{out}/{reg_name}']) — ONE call, docx
  first. No dossier, no sidecar, no PARTIAL file (remove any *_Create_Repaired_PARTIAL_*
  from outputs before S16-3's verify — pp.verify_handoff_outputs treats it as stray). The self-audit (S4-7 STEP B)
  runs on the repaired docx exactly as on a fresh paper — including A-QINDEX
  checks 7/8/9 — BEFORE this block.
  PRINT (operator-facing, last lines of the run, then the F2 footer per
  Framework_DeliveryFooter.md "STEP 7-R — TestCreateRepair"):
      ════════════════════════════════════════════════════════════
        REPAIR COMPLETE — [k] questions rewritten toward their labels
        ([k_h] harder · [k_e] easier) across [K] batch(es).
        Delivered (2 files):
          • [ExamCode]_[paper_slug]_Create_Repaired.docx  → Use locally
          • [ExamCode]_registry.json                      → Replace in Project Files
        ⚠ REPLACE registry.json in Project Files NOW — TestExplainRepair
          reads the pre-repair snapshot from the project copy and HARD-STOPS
          (missing_snapshot) if you skip this.
        Next step: copy-paste this, attaching the repaired paper
        + the previous explanation Word file:

           TestExplainRepair P[N]
      ════════════════════════════════════════════════════════════

# END OF Framework_MockTestCreate v5.75
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
#       Cone" etc.), so the literal check FALSELY reported it absent → HARD STOP.
#   v3.4 removes string-matching entirely. Joins are by subtopic_id, which all
#   three steps now share via the manifest. False "absent" alarms are impossible.
#
# THE THREE GUARANTEES (why this never breaks again, for 100 exams):
#   1. JOIN BY ID: S3-8 joins blueprint ↔ section_rules on subtopic_id. The
#      display name is decorative; nothing matches on it.
#   2. CONTRACT GATE: every blueprint id must exist in BOTH the manifest AND
#      section_rules, else HARD STOP naming the exact id (no silent Zero-PYQ
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
